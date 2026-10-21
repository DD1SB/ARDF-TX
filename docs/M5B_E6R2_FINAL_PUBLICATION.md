# M5B-E6R2 final reproduction and reviewed publication — 2026-10-21

**GO for five bare RF2M M5B-E6R2 evaluation PCBs only.** The project owner
reported that independent engineering review found no concrete blocker for this
scope. That review conclusion is separate from the fresh checks executed here.
Physical RF, thermal and operational qualification remains **NOT_RUN**.
No board or stencil was ordered and no hardware energized.

The starting working tree was clean on `m5b-e6-unified-heatsink`, at reviewed
implementation commit `2fff32131dd0f7da3c46fef47c04713a55df89d8`. Fetching GitHub
verified the same candidate SHA and `origin/main` at
`256c64888b680f5152e92f035e2ea0676a83630a`. Main is an ancestor of the candidate;
all ten existing milestone tags were unchanged. Publication preserves the E5,
E6, E6R1 and E6R2 commits and uses a normal fast-forward, with no acceptance tag
or production release. The final publication SHA is recorded in Git history.

Reproduction ran in the actual development environment in a disposable clone:

```sh
git fetch origin --tags
git clone --shared --single-branch --branch m5b-e6-unified-heatsink /home/stefan/src/ardf-tx /tmp/ardf-tx-e6r2-main-reproduction-20261021
python3 /tmp/m5b-e6r2-main-evidence/run.py
python3 /tmp/m5b-e6r2-main-evidence/compare.py
python3 /tmp/m5b-e6r2-main-evidence/test_comparison.py
```

The [executed runner](publication/M5B-E6R2/run.py),
[timestamped command ledger](publication/M5B-E6R2/execution.json), numbered logs
and [comparison utility](publication/M5B-E6R2/compare.py) preserve exact commands.
All **19 entry points** in the [reproduction procedure](../hardware/2m/review/M5B-E6R2/REPRODUCE.md)
ran successfully: native CAD, electrical/native verification, power, ground,
source, DFM, simulations, numerical tests, models, drawings, BOMs, exports,
three native renders, independent CAM reproduction, packaging, review and inventory.
No hardware source or existing verification-tool correction was required.

Host: x86-64 Linux 7.1.5-76070105-generic; Python 3.12.3; KiCad CLI/pcbnew
10.0.6; ngspice 42. Geometry/plot environment: CadQuery 2.8.0, NumPy 2.5.4,
SciPy 1.18.1, Matplotlib 3.11.2 and Pillow 13.0.0. See the
[environment record](publication/M5B-E6R2/environment.json). The external TI
model ZIP passed its documented SHA-256 check; its contents are not republished.

| Check executed in this run | Actual result |
|---|---|
| Complete native schematic ERC | 0 errors, 0 warnings |
| Native DRC and schematic parity | 0 errors, 0 unrouted, 0 parity issues |
| Inherited warnings | Exactly the same 11 missing-courtyard warnings as E5 |
| Rules and exclusions | Project configuration unchanged; no new exclusions |
| Electrical/native checks | 352 footprints, 51 critical manufacturer maps, all 20 controller contacts |
| Safety and keying | 4,096 enable combinations, 36 safety scenarios, 16 local-keying rows |
| Electrical/native negative cases | 68 detected |
| Source-joint regression | 16 native/input mutations and 4 adverse thermal-model cases detected |
| Actual copper continuity | One GND component; all 12 main-current paths connected |
| Standard-process DFM | PASS; all 11 native mutations detected |
| Mechanical solids | PASS; both deliberate collision cases rejected |
| Ngspice and numerical tests | 8 transient cases, 2 AC cases, 14 tests passed |
| Publication comparison controls | 5 tests reject altered STEP coordinates/colors, Gerber coordinates, drill diameter and BOM part identity |

[Fresh reports](publication/M5B-E6R2/fresh-results/) and the
[summary](publication/M5B-E6R2/summary.json) identify this run. The headless
pcbnew enum/image-handler diagnostics remain visible in logs; they are not CAD
violations. DRC's warning exit code is explicitly validated against the inherited
warning set. No failed hardware check was converted into a warning or excluded.
Thermal-model negatives are numerical checks, not measured fault detection.
The review generator's `pushed`/`ordered` fields are implementation-workflow
defaults; they do not record this publication's remote Git state. Ref verification
and the final publication commit establish that state separately.

The [artifact comparison](publication/M5B-E6R2/artifact-comparison.json) found
**no electrical or manufacturing geometry difference**. The refilled PCB is
byte-identical, SHA-256 `0bdf01a6907b35927f6f1d9ad55acf9c7eb7e893835982afc9e9652c51417baf`.
Of 114 native inputs, 111 reproduce byte-for-byte. The three generated STEP
library models retain identical geometric/topological entities and per-shape
colors; creation dates, product UUIDs and presentation-record ordering differ.
Both complete mechanical assembly STEP exports pass the same comparison.

All nine Gerbers and separate PTH/NPTH drills match after removing only creation
timestamps. All 953 PTH and 6 NPTH hits, the 150×110 mm outline, two cutouts and
full top paste match. The five source-paste windows still total 6.765 mm².
Netlist component, field and pin/net semantics match. The three population
placement files, thermal BOM and cost ledger are byte-identical.

Three BOM reports differ only in the `source` URL for C970–C973: the archived
reports contain a generic TI URL, while fresh generation uses the Murata URL
already present in the committed native manifest. Part numbers, values,
footprints, populations, quantities and costs are identical. The comparison
permits only that exact four-reference URL substitution, not arbitrary BOM
changes. Archived BOM files remain unchanged.

The initial strict comparison flagged STEP presentation ordering and the BOM
URL differences. Original diffs and comparison diagnostics are retained beside
the comparison utility. Its STEP graph comparison preserves every geometric
entity and resolves all presentation/color assignments; it does not discard
color information or geometric records. Five negative controls passed.

| Archive retained for publication | Entries | Reviewed SHA-256 |
|---|---:|---|
| Five bare boards | 11 | `4cde1a85fbc5a4af92302dba723644863a9656446d047e470af38f5a22ca67b8` |
| Full top stencil | 2 | `f89e9492844b6e869900565874d19c0af0cd922670c78801520668e6e5900d7b` |
| Native project snapshot | 114 | `4b51a07b7b900845d749d95438fb580bea0f459422bd105ce3ff7770948dae7a` |

All ZIP entry sets and CRCs pass. Fresh ZIP hashes differ because payload export
timestamps and STEP presentation metadata differ, as individually recorded in
the comparison. **The reviewed ZIPs, CAM, native project, libraries, mechanical
drawings and original CAD/numerical evidence were not replaced.** Fresh exports
remain in the disposable clone. Controller M6-L2, RF80 and historical E5/E6/E6R1
sources/evidence remain unchanged.

Manufacturing stays ordinary two-layer FR4, 1.6 mm, 1 oz, green mask, white
legend and lead-free HASL. No special stackup or filled/capped vias is required.
Existing 0.15 mm via annuli remain explicitly listed preferred-margin exceptions;
minimum component PTH annulus is 0.275 mm. Supplier CAM acceptance is not claimed.

Publication changes only current README/index/decision/manufacturing prose,
this separate reproduction evidence and documentation hash entries. The review
inventory is refreshed for its README, reproduction note and documentation-input
manifest; all other reviewed payload hashes remain unchanged. Its original
implementation inventory is preserved in commit `2fff321`. The separate
[publication evidence inventory](publication/M5B-E6R2/SHA256SUMS) covers this run.

The [first-article plan](M5B_E6R2_FIRST_ARTICLE_TEST.md) remains mandatory before
powered evaluation. Target firmware integration, RF/AM/spectrum, insulation,
source-joint/contact performance, thermal shutdown, outdoor behavior and
continuous-beacon qualification remain unmeasured. Continuous 1 W MO has only
0.49°C calculated Q401 margin; the 134.72°C degraded-contact scenario and the
low-gain crest-clipping sensitivity remain documented. No thermal threshold
was raised. **GO applies to five bare evaluation PCBs only.**
