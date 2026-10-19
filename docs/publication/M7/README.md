# M7 publication audit

Date: 2026-10-19. Destination: [DD1SB/ARDF-TX](https://github.com/DD1SB/ARDF-TX).
This milestone publishes the existing project history; it changes no circuit,
PCB routing, component value, accepted ADR or manufacturing dataset. No hardware
acceptance tag or production release is created.

## Sources and preserved history

The pre-publication `main` is `3b84366caa985fac67fbdfbb60c4ede751b3a13e`.
The history audit initially covered **21 commits**, **2,439 unique blobs** and
ten tags, all reachable from one established branch (`main`). There were no
existing remotes. The public destination was empty (`git ls-remote` returned
no refs; the GitHub API reported public visibility and size zero). Existing
SSH credentials authenticated as DD1SB; no token was copied into files/logs.
The read URL uses HTTPS and the authenticated push URL uses SSH.

The publication commit preserves all ancestry and tag objects. No squash,
rebase, force push, author rewrite or history filtering is used. The final
remote SHA, tags and fresh-clone checks are verified after the push and reported
at task completion; this pre-push audit does not claim that an attempted push
alone proves publication.

## Content and licensing audit

[history-audit.json](history-audit.json) records the heuristic scan and inventory.
All reachable Git blobs, commit/tag text and ZIP/tar member data were scanned
for common credential/key patterns, credentials embedded in URLs and private
IPv4 addresses. Selected pre-existing handoff material was scanned too. No
matches were found. This is a bounded heuristic plus manual provenance review,
not a guarantee that pattern matching detects every possible secret.

The largest existing blob is about 4.38 MiB; no blob reaches GitHub's 50 MiB
warning or 100 MiB file limit. Git LFS is unnecessary. The untracked handoff
contains a 13.04 MiB intentionally self-contained source archive, also below
those limits. Native project files, BOMs, reports, fabrication data, historical
reviews and original research are retained. Existing execution logs include
local paths/tool metadata; these are reproducibility records, not credentials.
Git's existing public contributor identity is preserved.

Root [MIT licensing](../../../LICENSE) covers contributor-owned work with
[explicit third-party exceptions](../../../THIRD_PARTY_NOTICES.md). OpenARDF
notices remain; KiCad libraries keep their CC-BY-SA terms and exception; the
sliver helper keeps GPL-2.0-or-later; historical DL3BBX-derived R3 keeps its
private-construction/commercial-permission limitations. Complete GPL v2 and
CC-BY-SA-4.0 texts are supplied. The original DL3BBX article permits attributed
copying/private construction, but that is not a commercial open-hardware grant.
Manufacturer PDFs and original third-party product CAD were reference downloads,
not a vendored document collection. All history's PDF/document names were
inventoried; PDFs are project schematic/assembly/drill-map exports. Official
vendor documents remain links under their owners' terms.

License references were checked against the official KiCad library-license page,
the original DL3BBX permission paragraph and the standard MIT text on 2026-10-19.
The CC legal text came from `https://creativecommons.org/licenses/by-sa/4.0/legalcode.txt`;
GPL v2 is the complete installed Debian common-license text. Optional GitHub
description/topics require an authenticated repository-settings API, which is
not available through the installed Git/SSH publication tooling; they are not
required for source publication. GitHub can identify the root MIT license.

## Uncommitted material and housekeeping

- The pre-existing `hardware/80m/handoff/M4A-E2/` is relevant historical work,
  deliberately included after inspecting its README, procurement/assembly
  records and all 63 manifest entries. All 317 files in its source tar archive
  equal commit `1245023`. Its copied exports were not regenerated. See
  [handoff audit](historical-handoff.json). It is not the current RF80 order set.
- The live `~RF2M.kicad_pro.lck` remains local and ignored; it is not deleted
  or committed.
- Active `hardware/2m/RF2M.kicad_prl` and `hardware/80m/RF80.kicad_prl` are
  removed only from tracking, not from the local filesystem. Their historical
  blobs remain. Three archived/review-bound `.kicad_prl` snapshots remain
  explicit historical exceptions, including the two E5 checksum-bound snapshots.
  They contain UI state, not credentials. New workspace files are ignored.
- Ignore rules cover Python caches, environments, editor state, local builds,
  KiCad recovery/locks and local credential files. Authoritative native sources,
  libraries and review/fabrication files remain versioned.
- Attributes preserve exact historical bytes. No global line-ending conversion
  or `git add --renormalize` is performed. This matters for checksum-bound CSVs,
  Gerbers and archives on a fresh clone.

## Manufacturing integrity

[publication-integrity.json](publication-integrity.json) binds the three current
projects to their milestone commits and verifies all archive SHA-256 values,
ZIP CRCs, required layers, separate PTH/NPTH and byte equality with final review
exports. Each archive contains nine Gerbers and two drill files, no reports or
historical alternatives. The controller archive's existing location in RF80's
three-board handoff is retained.

| Candidate | Archive SHA-256 |
| --- | --- |
| Controller M6-L1 | `e1745a8b8b42c15e024315d58749bbdfe019745e0e48bf055e65a02977dd36e6` |
| RF80 M4A-V1R1 | `8cdb21e278e9120abc81b594516f8498a1110df3ce50d845d4922c161f510a92` |
| RF2M M5B-E5 | `c2ef2ccdf80098a82fac2e0cd843a725c830f4d1e55f2acb2ae521c40c5e270a` |

All current native project/PCB/root-sheet bytes equal their identified milestone
commits. Existing hardware/firmware/ADRs are unchanged apart from the two personal
workspace files no longer tracked. No current or historical fabrication ZIP is
regenerated. Historical review manifests validate: controller 125 entries,
RF80 78, RF2M 379; historical handoff 63.

## Verification actually rerun

| Check | M7 result |
| --- | --- |
| Three current native projects and milestone ancestry | PASS |
| Three current fabrication ZIPs, layers/drills and source review bytes | PASS |
| Current review/handoff manifests | PASS |
| New public-entry-point relative links/headings | PASS; count in integrity report |
| KiCad 10.0.6 ERC, all three boards | 0 errors / 0 warnings |
| KiCad 10.0.6 DRC, controller / RF80 | 0 errors / 0 warnings |
| KiCad 10.0.6 DRC, RF2M | 0 errors / 11 retained intentional missing-courtyard warnings |
| Unrouted / schematic parity, all three boards | 0 / 0 |
| Controller host tests | 46 PASS |
| Strict C11 waveform/control fixture | Compile/run PASS with `-Wall -Wextra -Werror` |
| Historical full RF/thermal/DFM suite replay | NOT_RERUN; retained reports hash-verified |
| Physical qualification | NOT_RUN |

[CAD-rerun.json](CAD-rerun.json) records exact commands, counts and inherited
ignored categories. [Raw CAD reports](cad/) are fresh publication outputs;
no project settings or exclusions changed. Existing ERC ignores include singleton
global labels, four-way junctions and simulation-model checks; controller/RF2M
also ignore footprint filters. Their DRC ignores only the unused tuning-profile
category; RF80 has no ignored DRC category. These inherited settings are disclosed,
not silently treated as checks that passed. No zones were refilled/saved.
[host-tests.json](host-tests.json) preserves actual test commands and outputs.
No complete hardware qualification is inferred from old PASS reports.

## Reproduce without changing historical data

[file-inventory.json](file-inventory.json) and [SHA256SUMS](SHA256SUMS) bind the
publication changes and preserved handoff. They exclude their own two inventory
files to avoid circular hashes. Verify from the repository root with
`sha256sum -c docs/publication/M7/SHA256SUMS`.

Run from the repository root:

```sh
python3 tools/m7_publication.py verify
python3 tools/m7_publication.py history --output /tmp/ardf-history-audit.json
python3 tools/m7_publication.py cad --cad-dir /tmp/ardf-cad-checks --output /tmp/ardf-cad-summary.json
python3 -m unittest discover -s firmware/controller_hw -p 'test_*.py' -v
cc -std=c11 -Wall -Wextra -Werror firmware/controller_hw/contract.c firmware/controller_hw/test_contract.c -lm -o /tmp/ardf-controller-contract
/tmp/ardf-controller-contract
```

`verify` and `history` need Git and the Python standard library. `cad` needs
KiCad 10.0.6 and installed project libraries; it writes reports only to the
explicit output directory. Use the historical revision instructions in disposable
worktrees for complete engineering replay. Do not run old exporters on current
hardware as part of publication verification.

## Remaining gates

Publication grants no PCB supplier upload/order or physical operation authority.
Independent hardware review, RF80 sequencing amendment, supplier CAM/quotation,
component fit, controlled protection/USB/pack/RTC/ESD tests, source-joint assembly,
RF/AM/spectrum/thermal/endurance/antenna/field tests remain separate. RF2M's
conservative 110°C target remains unmet; the 125°C engineering operating gate
remains open. No physical PASS or manufacturing/delivery is claimed.
