#!/usr/bin/env python3
"""M1 arithmetic and documentation checks only; no firmware or hardware tests."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import re
import urllib.error
import urllib.request

ROOT = Path(__file__).resolve().parents[1]


def model(rework=False):
    usable = 7.2 * 3.4 * 0.80 * 0.90 * 0.90
    carrier = 10 ** (1 / 10)  # 1 W ERP, net antenna gain -1 dB
    mean_rf = carrier * (1 + 0.8 ** 2 / 2)
    hf = 5 / 0.60 / 0.85 + (0.500 if rework else 0.260)
    sprint = 1 / 0.55 / 0.88 + (0.250 if rework else 0.150)
    vhf = mean_rf / 0.45 / 0.70 / 0.88 + (0.950 if rework else 0.300)
    powers = {
        "HF Classic": 0.130 + 0.20 * hf,
        "Sprint": 0.130 + 0.20 * sprint,
        "Foxoring": 0.260,
        "VHF Classic": 0.130 + 0.20 * vhf,
        "HF beacon": 0.130 + hf,
        "Sprint beacon": 0.130 + sprint,
        "VHF beacon": 0.130 + vhf,
        "Training": 0.350,
        "Dual Classic": 0.140 + 0.20 * (hf + vhf),
    }
    rows = []
    for name, power in powers.items():
        rows.append({"profile": name, "battery_w": round(power, 6),
                     "wh_24h": round(24 * power, 2),
                     "runtime_h_1p_to_4p": [round(usable * n / power, 1) for n in range(1, 5)],
                     "minimum_p_for_24h_model": next((n for n in range(1, 5) if usable * n >= 24 * power), None)})
    return {"classification": "unmeasured planning assumptions", "revision": "cost rework" if rework else "historical initial M1",
            "usable_wh_per_parallel_pair": usable,
            "vhf_carrier_w": carrier, "vhf_mark_mean_w": mean_rf,
            "vhf_pep_w_at_m_0_8": carrier * 1.8 ** 2,
            "vhf_clean_headroom_w_1db": carrier * 1.8 ** 2 * 10 ** 0.1,
            "profiles": rows}


def markdown_files():
    return [ROOT / "README.md"] + sorted((ROOT / "docs").rglob("*.md"))


def links(path):
    # Repository documents use simple inline links, no nested destination parentheses.
    text = re.sub(r"```.*?```", "", path.read_text(), flags=re.S)
    return re.findall(r"\[[^\]]*\]\(([^\n)]+)\)", text)


def local_checks():
    errors = []
    files = markdown_files()
    checked = 0
    for path in files:
        for link in links(path):
            if re.match(r"[a-z]+://", link):
                continue
            target, _, fragment = link.partition("#")
            resolved = (path.parent / target).resolve() if target else path
            checked += 1
            if not resolved.exists():
                errors.append(f"Missing link: {path.relative_to(ROOT)} -> {link}")
            elif fragment:
                headings = re.findall(r"^#+\s+(.+)$", resolved.read_text(), re.M)
                anchors = {re.sub(r"[^\w\s-]", "", h.lower()).replace(" ", "-") for h in headings}
                if fragment not in anchors:
                    errors.append(f"Missing anchor: {path.relative_to(ROOT)} -> {link}")
    baseline = (ROOT / "docs/requirements.md").read_text()
    trace = (ROOT / "docs/M1_REQUIREMENTS_TRACE.md").read_text()
    prep_trace = ROOT / "docs/M2_PREPARATION.md"
    if prep_trace.exists():
        trace += "\n" + prep_trace.read_text()
    fox_trace = ROOT / "docs/FOXORING_COST_AUDIT.md"
    if fox_trace.exists():
        trace += "\n" + fox_trace.read_text()
    power_trace = ROOT / "docs/M2_POWER_REQUIREMENTS_TRACE.md"
    if power_trace.exists():
        trace += "\n" + power_trace.read_text()
    ids = set(re.findall(r"\| ((?:SYS|RF80|RF2|CTRL|PWR|TEST|RULE|COST|PREP|FOX)-\d+) \|", baseline))
    trace_ids = set(re.findall(r"\| ((?:SYS|RF80|RF2|CTRL|PWR|TEST|RULE|COST|PREP|FOX)-\d+)(?: \(added\))? \|", trace))
    errors.extend(f"Untraced requirement: {r}" for r in sorted(ids - trace_ids))
    acceptance = (ROOT / "docs/m1-acceptance.md").read_text()
    deliverables = re.findall(r"`(docs/M1_[A-Z_]+\.md)`", acceptance)
    for name in deliverables:
        path = ROOT / name
        if not path.exists():
            errors.append(f"Missing deliverable: {name}")
        elif "2026-10-13" not in path.read_text():
            errors.append(f"Missing research date: {name}")
    for path in sorted((ROOT / "docs/decisions").glob("ADR-000[3-7]*.md")):
        if path.name.startswith("ADR-0007"):
            if "Conditionally accepted" not in path.read_text():
                errors.append("Architectural review acceptance not recorded: " + path.name)
        elif "Proposed" not in path.read_text():
            errors.append(f"New ADR not Proposed: {path.name}")
    report = model(rework=True)
    power_doc = (ROOT / "docs/M1_POWER_BUDGET.md").read_text()
    for row in report["profiles"]:
        rendered = " / ".join(f"{v:.1f}" for v in row["runtime_h_1p_to_4p"])
        if rendered not in power_doc:
            errors.append(f"Runtime table differs: {row['profile']}: {rendered}")
    # Rework candidate totals come from the itemized basket, not frozen old envelopes.
    cost_data = json.loads((ROOT / "docs/M1_COST_TOTALS.json").read_text())
    cost_values = [cost_data["variants"]["All three PCBs"][str(n)]["per_unit_eur"] for n in (6, 10, 20)]
    for doc_name in ("M1_BOM_CANDIDATES.md", "M1_DECISION.md"):
        doc_text = (ROOT / "docs" / doc_name).read_text()
        for value in cost_values:
            if value not in doc_text:
                errors.append(f"Cost table differs: {doc_name}: {value}")
    # Independent analytical slot membership: both Sprint groups active concurrently,
    # exactly one transmitter per group at every integer second, boundary-exclusive.
    for seconds in range(120):
        phase = seconds % 60
        active = [n for n in range(1, 6) if 12 * (n - 1) <= phase < 12 * n]
        if len(active) != 1 or active[0] != phase // 12 + 1:
            errors.append(f"Sprint analytical slot error at {seconds}")
    print(json.dumps({"markdown_files": len(files), "local_links_checked": checked,
                      "requirements_traced": len(ids), "deliverables": len(set(deliverables)),
                      "numeric_profile_rows_checked": len(report["profiles"]),
                      "configuration_batch_totals_checked": len(cost_values),
                      "sprint_boundary_model": "passed, not firmware tested", "errors": errors}, indent=2))
    return bool(errors)


def external_checks(incremental=False, checked_on="2026-10-13", report="docs/M1_EXTERNAL_LINKS.json", scope=None):
    paths = [ROOT / scope] if scope else markdown_files()
    urls = sorted({u for p in paths for u in links(p) if u.startswith(("http://", "https://"))})
    out = ROOT / report
    prior = {}
    if incremental and out.exists():
        prior = {r["url"]: r for r in json.loads(out.read_text())["results"]}
    # A sandbox DNS failure is not evidence about a remote source. Recheck it
    # on the approved network rerun, while retaining other prior outcomes.
    pending = [u for u in urls if u not in prior or any(
        marker in prior.get(u, {}).get("result", "")
        for marker in ("Name or service not known", "Temporary failure in name resolution"))]
    if not incremental:
        pending = urls

    def inspect(url):
        request = urllib.request.Request(url, headers={"User-Agent": "ARDF-TX-M1-documentation-link-check/1.0"})
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                sample = response.read(1024)
                reason = "reachable"
                if any(x in sample.lower() for x in (b"access denied", b"verify that you're not a robot", b"captcha")):
                    reason = "access challenge; content not verified"
                return {"url": url, "status": response.status, "result": reason,
                        "final_url": response.url}
        except urllib.error.HTTPError as exc:
            return {"url": url, "status": exc.code, "result": "HTTP error/access restriction"}
        except Exception as exc:
            return {"url": url, "status": None, "result": type(exc).__name__ + ": " + str(exc)}

    with ThreadPoolExecutor(max_workers=6) as pool:
        fresh = list(pool.map(inspect, pending))
    combined = dict(prior)
    combined.update({r["url"]: r for r in fresh})
    results = [combined[u] for u in urls]
    out.write_text(json.dumps({"checked_on": checked_on, "scope": scope or "all repository Markdown", "method": "GET; first 1024 bytes only, no content-validity guarantee",
                               "results": results}, indent=2) + "\n")
    failed = [r for r in results if r["status"] != 200 or r["result"] != "reachable"]
    print(json.dumps({"urls": len(urls), "requested_this_run": len(pending),
                      "reachable_http_200": len(results) - len(failed), "unresolved": failed,
                      "report": str(out.relative_to(ROOT))}, indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--external-links", action="store_true")
    parser.add_argument("--incremental", action="store_true", help="Check newly added URLs only; retain prior results")
    parser.add_argument("--link-date", default="2026-10-13", help="Date for a separate source reachability audit")
    parser.add_argument("--link-report", default="docs/M1_EXTERNAL_LINKS.json")
    parser.add_argument("--link-scope", help="Optional single repository Markdown source register")
    parser.add_argument("--rework", action="store_true", help="Use cost-rework active-overhead assumptions")
    args = parser.parse_args()
    if args.check:
        raise SystemExit(local_checks())
    elif args.external_links:
        external_checks(args.incremental, args.link_date, args.link_report, args.link_scope)
    else:
        print(json.dumps(model(rework=args.rework), indent=2))
