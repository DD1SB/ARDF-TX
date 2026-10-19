#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Read-only public-package checks. Never recapture CAD or overwrite a review.

verify: standard library + Git. history: heuristic all-reachable-object audit.
cad: installed KiCad; reports go to an explicit directory outside hardware/.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import tarfile
from urllib.parse import unquote, urlsplit
import zipfile

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "3b84366caa985fac67fbdfbb60c4ede751b3a13e"
UNTRACKED_PERSONAL_STATE = {"hardware/2m/RF2M.kicad_prl", "hardware/80m/RF80.kicad_prl"}
HISTORICAL_WORKSPACE_EVIDENCE = {
    "hardware/2m/archive/M5A-R1/RF2M.kicad_prl",
    "hardware/2m/review/M5B-E5/development/E4R1-baseline.kicad_prl",
    "hardware/2m/review/M5B-E5/development/Q501-stencil-native.kicad_prl",
}
BOARDS = [
    ("Controller", "d94dabd0e40137dc44b2bb94f3707ad4636ca65f",
     "hardware/controller/CTRL", "hardware/controller/review/M6-L1",
     "hardware/80m/production/review/M4A-V1R1/three-board-order/CTRL_M6-L1_JLCPCB_5boards.zip",
     "e1745a8b8b42c15e024315d58749bbdfe019745e0e48bf055e65a02977dd36e6"),
    ("RF80", "f86684b9ef45eec3ca4ce52edcb62896a847f1d7",
     "hardware/80m/production/RF80_V1", "hardware/80m/production/review/M4A-V1R1",
     "hardware/80m/production/review/M4A-V1R1/fabrication/RF80-V1R1_JLCPCB_5boards.zip",
     "8cdb21e278e9120abc81b594516f8498a1110df3ce50d845d4922c161f510a92"),
    ("RF2M", BASELINE, "hardware/2m/RF2M", "hardware/2m/review/M5B-E5",
     "hardware/2m/review/M5B-E5/fabrication/RF2M-M5B-E5_JLCPCB_5boards.zip",
     "c2ef2ccdf80098a82fac2e0cd843a725c830f4d1e55f2acb2ae521c40c5e270a"),
]


def git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def manifest_check(path, base):
    rows = []
    for line in path.read_text().splitlines():
        if not line.strip():
            continue
        digest, name = line.split(maxsplit=1)
        name = name.lstrip(" *")
        p = base / name
        require(p.is_file(), f"Missing manifest input: {p}")
        require(sha(p.read_bytes()) == digest, f"Manifest hash mismatch: {p}")
        rows.append(name)
    return len(rows)


def anchors(path):
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
    result, counts = set(), Counter()
    for heading in re.findall(r"^#{1,6}\s+(.+?)\s*#*\s*$", text, re.M):
        heading = re.sub(r"\[([^]]+)\]\([^)]*\)", r"\1", heading).lower()
        slug = re.sub(r"[^\w\- ]", "", heading).replace(" ", "-")
        n = counts[slug]
        counts[slug] += 1
        result.add(slug + (f"-{n}" if n else ""))
    return result


def public_links():
    paths = [ROOT / x for x in ("README.md", "CONTRIBUTING.md",
             "THIRD_PARTY_NOTICES.md", "docs/README.md")]
    paths += sorted((ROOT / "docs/publication/M7").glob("*.md"))
    count = 0
    for path in paths:
        text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
        for dest in re.findall(r"\[[^\]]*\]\(([^\s)]+)(?:\s+\"[^\"]*\")?\)", text):
            target = urlsplit(dest.strip("<>"))
            if target.scheme or target.netloc:
                continue
            p = (path.parent / unquote(target.path)).resolve() if target.path else path
            require(p.is_relative_to(ROOT), f"Link escapes repository: {path}: {dest}")
            require(p.exists(), f"Broken link: {path.relative_to(ROOT)} -> {dest}")
            if target.fragment and p.suffix == ".md":
                require(unquote(target.fragment) in anchors(p), f"Broken heading: {dest}")
            count += 1
    return {"documents": len(paths), "relative_links": count}


def verify():
    results = []
    for name, commit, native, review, archive, expected in BOARDS:
        git("cat-file", "-e", commit + "^{commit}")
        git("merge-base", "--is-ancestor", commit, "HEAD")
        sources = []
        for ext in (".kicad_pro", ".kicad_sch", ".kicad_pcb"):
            p = ROOT / (native + ext)
            require(p.is_file(), f"Missing native source: {p}")
            require(p.read_bytes() == git("show", f"{commit}:{native}{ext}"),
                    f"Source differs from current candidate: {p}")
            sources.append({"path": str(p.relative_to(ROOT)), "sha256": sha(p.read_bytes())})
        data = (ROOT / archive).read_bytes()
        require(sha(data) == expected, f"Archive checksum mismatch: {archive}")
        folder = ROOT / review / ("fabrication" if name == "Controller" else "gerbers")
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            names = z.namelist()
            require(z.testzip() is None, f"Archive CRC failure: {archive}")
            require(len(names) == len(set(names)) == 11, f"Wrong/duplicate archive entries: {archive}")
            require(all(Path(n).name == n for n in names), f"Unexpected archive paths: {archive}")
            require(Counter(Path(n).suffix for n in names) == Counter({
                ".gtl": 1, ".gbl": 1, ".gts": 1, ".gbs": 1, ".gto": 1,
                ".gbo": 1, ".gtp": 1, ".gbp": 1, ".gm1": 1, ".drl": 2}),
                f"Missing required manufacturing layer: {archive}")
            require(any(n.endswith("-PTH.drl") for n in names) and
                    any(n.endswith("-NPTH.drl") for n in names), "PTH/NPTH separation missing")
            for n in names:
                require(z.read(n) == (folder / n).read_bytes(),
                        f"Archive differs from final review export: {n}")
        review_root = ROOT if name == "RF2M" else ROOT / review
        count = manifest_check(ROOT / review / "SHA256SUMS", review_root)
        results.append(dict(board=name, commit=commit, native=sources,
                            archive=archive, sha256=expected, archive_entries=11,
                            review_manifest_entries=count))
    # No native hardware, firmware, historical review or accepted ADR altered by M7.
    changed = git("diff", "--name-only", "--diff-filter=MDRT", BASELINE,
                  "--", "hardware", "firmware", "docs/decisions").decode().splitlines()
    require(set(changed) <= UNTRACKED_PERSONAL_STATE,
            "Existing engineering sources changed during publication")
    for p in changed:
        require(subprocess.run(["git", "cat-file", "-e", f":{p}"], cwd=ROOT,
                               stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode != 0,
                "Personal workspace cleanup must only remove from version control")
    added = git("diff", "--diff-filter=A", "--name-only", BASELINE,
                "--", "hardware", "firmware", "docs/decisions").decode().splitlines()
    require(all(x.startswith("hardware/80m/handoff/M4A-E2/") for x in added),
            "Unexpected new hardware/firmware/ADR content during publication")
    require((ROOT / "LICENSE").read_text().startswith(
        "MIT License\n\nCopyright (c) 2026 DD1SB and ARDF-TX contributors\n"), "Wrong MIT notice")
    handoff = ROOT / "hardware/80m/handoff/M4A-E2"
    require(handoff.is_dir(), "Historical handoff absent")
    handoff_count = manifest_check(handoff / "SHA256SUMS", handoff)
    return dict(status="PASS_PUBLICATION_INTEGRITY", boards=results,
                links=public_links(), preserved_handoff_manifest_entries=handoff_count,
                existing_engineering_sources_unchanged=True,
                physical_qualification="NOT_RUN", limitations=[
                    "Not a full historical engineering-suite replay or physical qualification",
                    "Per-revision exporters/generators must run in a suitable historical worktree"])


PATTERNS = {
    "credential_token": rb"(?:gh[pousr]_[A-Za-z0-9]{25,}|github_pat_[A-Za-z0-9_]{40,}|AKIA[0-9A-Z]{16}|AIza[0-9A-Za-z_-]{30,}|sk-(?:proj-)?[A-Za-z0-9_-]{30,})",
    "private_key": rb"-----BEGIN (?:RSA |EC |OPENSSH |DSA )?PRIVATE KEY-----",
    "url_credentials": rb"https?://[^\s/\"<>:]{2,60}:[^\s/\"<>]{4,100}@",
    "credential_assignment": rb"(?i)(?:password|passwd|api_key|access_token|client_secret)\s*[=:]\s*[\x22\x27][^\x22\x27\n]{8,100}[\x22\x27]",
    "private_ipv4": rb"\b(?:10\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}|192\.168\.[0-9]{1,3}\.[0-9]{1,3}|172\.(?:1[6-9]|2[0-9]|3[01])\.[0-9]{1,3}\.[0-9]{1,3})\b",
}


def findings(data, path, blob):
    # Never emit matching values; locations only. Heuristic scan is not a guarantee.
    return [dict(kind=k, path=path, blob=blob, line=data[:m.start()].count(b"\n") + 1)
            for k, pattern in PATTERNS.items() for m in re.finditer(pattern, data)]


def nested_scan(data, path, blob):
    rows = findings(data, path, blob)
    if data.startswith(b"PK\x03\x04"):
        with zipfile.ZipFile(io.BytesIO(data)) as z:
            for n in z.namelist():
                rows += findings(z.read(n), path + "!" + n, blob)
    elif data.startswith(b"\x1f\x8b"):
        with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as t:
            for member in t.getmembers():
                if member.isfile():
                    rows += findings(t.extractfile(member).read(), path + "!" + member.name, blob)
    return rows


def classify(path):
    if path.endswith((".zip", ".gbl", ".gtl", ".gts", ".gbs", ".gto", ".gbo", ".gtp", ".gbp", ".gm1", ".drl")):
        return "fabrication_or_versioned_archive"
    if "review/" in path or "handoff/" in path:
        return "engineering_review_or_handoff_evidence"
    if path.startswith("docs/assets/") or "LICENSE" in path or "NOTICE" in path:
        return "reference_or_license_material"
    if path.startswith("hardware/"):
        return "native_hardware_or_local_library"
    if path.startswith(("tools/", "firmware/")):
        return "tooling_or_firmware_foundation"
    if path.startswith("docs/"):
        return "engineering_documentation"
    return "project_documentation_or_configuration"


def history():
    objects = {}
    for row in git("rev-list", "--objects", "--all").decode().splitlines():
        h, _, name = row.partition(" ")
        objects[h] = name
    proc = subprocess.Popen(["git", "cat-file", "--batch"], cwd=ROOT,
                            stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    blobs, hits, archived_members = [], [], 0
    for h, name in objects.items():
        proc.stdin.write((h + "\n").encode())
        proc.stdin.flush()
        header = proc.stdout.readline().split()
        data = proc.stdout.read(int(header[2]))
        proc.stdout.read(1)
        if header[1] in (b"commit", b"tag"):
            hits += findings(data, f"<{header[1].decode()}>", h)
        elif header[1] == b"blob":
            blobs.append(dict(path=name, blob=h, bytes=len(data)))
            hits += nested_scan(data, name, h)
            if data.startswith(b"PK\x03\x04"):
                archived_members += len(zipfile.ZipFile(io.BytesIO(data)).namelist())
    proc.stdin.close()
    require(proc.wait() == 0, "Git object audit failed")
    tracked = git("ls-files", "-z").decode().split("\0")[:-1]
    # Also inspect selected relevant untracked handoff/publication files, never .git or local locks.
    extras = [p for p in (ROOT / "hardware/80m/handoff").rglob("*") if p.is_file()]
    for p in extras:
        if str(p.relative_to(ROOT)) not in tracked:
            hits += nested_scan(p.read_bytes(), str(p.relative_to(ROOT)), "untracked-handoff")
    for n in tracked:
        hits += nested_scan((ROOT / n).read_bytes(), n, "worktree")
    temp = [p for p in tracked if re.search(
        r"(?:__pycache__/|\.pyc$|\.kicad_prl$|\.lck$|(?:^|/)\.env$|\.venv/|\.DS_Store$)", p)]
    unaccepted_temp = [p for p in temp if p not in HISTORICAL_WORKSPACE_EVIDENCE]
    return dict(status="REVIEW_REQUIRED" if hits or unaccepted_temp else "PASS_HEURISTIC_AUDIT",
                scope="all reachable commits/tags/blobs and archive members; tracked worktree; selected untracked handoff",
                commits=int(git("rev-list", "--all", "--count")),
                branches=git("branch", "--format=%(refname:short)").decode().splitlines(),
                tags=git("tag", "--list").decode().splitlines(),
                unique_blobs=len(blobs), total_blob_bytes=sum(x["bytes"] for x in blobs),
                largest_blobs=sorted(blobs, key=lambda x: x["bytes"], reverse=True)[:12],
                over_50_MiB=[x for x in blobs if x["bytes"] >= 50 * 1024**2],
                over_100_MiB=[x for x in blobs if x["bytes"] >= 100 * 1024**2],
                archive_members_scanned=archived_members,
                redacted_findings=hits, unexpected_tracked_temporary_files=unaccepted_temp,
                retained_historical_workspace_evidence=[p for p in temp if p in HISTORICAL_WORKSPACE_EVIDENCE],
                tracked_classification=dict(Counter(classify(p) for p in tracked)),
                limitations="Pattern matching cannot establish absence of every secret or settle third-party rights; manual provenance review also required.")


def cad(output):
    output = output.resolve()
    require(not output.is_relative_to(ROOT / "hardware"), "Do not overwrite hardware review evidence")
    output.mkdir(parents=True, exist_ok=True)
    paths = [ROOT / p for p in git("ls-files", "hardware").decode().splitlines()]
    before = {p: sha(p.read_bytes()) for p in paths}

    def check(board):
        name, _, base, _, _, _ = board
        rows = []
        for kind in ("erc", "drc"):
            report = output / f"{name}-{kind}.json"
            cmd = ["kicad-cli", "sch" if kind == "erc" else "pcb", kind,
                   "--format", "json", "--severity-all", "-o", str(report)]
            if kind == "drc":
                cmd += ["--schematic-parity"]
            cmd += [base + (".kicad_sch" if kind == "erc" else ".kicad_pcb")]
            run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            (output / f"{name}-{kind}.log").write_text(run.stdout + run.stderr)
            require(run.returncode == 0 and report.is_file(), f"CAD command failed: {cmd}")
            data = json.loads(report.read_text())
            groups = ({"violations": [v for s in data.get("sheets", [])
                                      for v in s.get("violations", [])]}
                      if kind == "erc" else
                      {k: data.get(k, []) for k in ("violations", "unconnected_items", "schematic_parity")})
            counts = {k: dict(Counter(x.get("severity", "unspecified") for x in v)) for k, v in groups.items()}
            require(not any(x.get("error", 0) for x in counts.values()), f"CAD errors: {name} {kind}")
            require(not data.get("unconnected_items") and not data.get("schematic_parity"),
                    f"Unrouted/parity defect: {name}")
            warnings = [x for v in groups.values() for x in v if x.get("severity") == "warning"]
            if name == "RF2M" and kind == "drc":
                require(len(warnings) == 11 and all(x.get("type") == "missing_courtyard" for x in warnings),
                        "Unexplained RF2M DRC warnings")
            else:
                require(not warnings, f"CAD warnings: {name} {kind}")
            rows.append(dict(kind=kind, command=cmd, counts=counts,
                             ignored_checks=data.get("ignored_checks", []),
                             included_severities=data.get("included_severities", [])))
        return dict(board=name, results=rows)

    with ThreadPoolExecutor(max_workers=3) as pool:
        result = list(pool.map(check, BOARDS))
    require(all(sha(p.read_bytes()) == v for p, v in before.items()), "CAD check changed hardware input")
    return dict(toolchain=subprocess.check_output(["kicad-cli", "version"], text=True).strip(),
                CAD=result, all_tracked_hardware_bytes_unchanged=True,
                zone_refill=False, save_board=False, physical_qualification="NOT_RUN")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=("verify", "history", "cad"))
    parser.add_argument("--output", type=Path, help="New JSON report, outside historical hardware reviews")
    parser.add_argument("--cad-dir", type=Path, default=Path("/tmp/ardf-m7-cad"))
    args = parser.parse_args()
    report = verify() if args.action == "verify" else history() if args.action == "history" else cad(args.cad_dir)
    text = json.dumps(report, indent=2) + "\n"
    if args.output:
        require(not args.output.resolve().is_relative_to(ROOT / "hardware"), "Never overwrite engineering evidence")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
        print(report.get("status", "CAD_REPORT_WRITTEN"), args.output)
    else:
        print(text, end="")
    if report.get("status") == "REVIEW_REQUIRED":
        raise SystemExit(1)


if __name__ == "__main__":
    main()
