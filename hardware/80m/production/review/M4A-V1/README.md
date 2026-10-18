# RF80 M4A-V1 engineering review package

**PRODUCTION-INTENT — NOT RELEASED. All physical tests NOT_RUN.**
Reference: frozen **1245023 / m3b-e2**. Candidate: `RF80_V1`, 150 × 110 mm,
1.6 mm nominal, two outer copper layers. The native project is [two directories
above](../../RF80_V1.kicad_pro). No supplier upload, purchase, manufacture,
assembly or hardware activation has occurred.

Start with the [M4A decision](../../../../../docs/M4A_REVIEW_DECISION.md),
[layout](../../../../../docs/M4A_COMPACT_LAYOUT.md),
[mechanical assumptions](../../../../../docs/M4A_MECHANICAL_INTERFACE.md),
[BOM/costs](../../../../../docs/M4A_VARIANT_BOM.md) and
[equivalence boundary](../../../../../docs/M4A_ELECTRICAL_EQUIVALENCE.md).

Review files:

- `RF80_V1.pdf`, `RF80_V1.xml`, `RF80_V1.ipc`: fresh schematic, electrical netlist and IPC.
- `top-copper.svg`, `bottom-copper.svg`: actual filled native-board copper previews.
- `assembly.pdf/.svg`, `assembly-bottom.pdf/.svg`: component placement and lead/pad artwork.
- `RF80_V1-3D.png`, `RF80_V1-3D-top.png`, `RF80_V1-3D-bottom.png`: actual KiCad renders; dimensional-envelope/model limitations remain.
- `gerbers/`: nine Gerber layers/job, separate PTH/NPTH drills and PDF maps. **Engineering inspection only, not production release.**
- `RF80_V1-position-full.csv`, `RF80_V1-position-fox.csv`, `population.csv`: full/Fox populations; full=195 board placements plus remote TH301, Fox=115 board placements.
- `production-test-pads.csv`, `test-feature-disposition.json`: 14 retained pads, all 74 original probe features classified.
- `mechanical-interface.svg`, `mechanical-stackup.json`: native mounting/footprint envelope and drill data; adjustable thermal/harness allowances are identified.
- `ERC.json`, `DRC.json`, `DRC.rpt`, `drc-coverage.json`: actual check results/coverage; three inherited informational ERC defaults disclosed.
- `electrical-equivalence.json`, `logic-results.json`, `fabrication-audit.json`, `ground-connectivity.json`, `routing-summary.json`: automated evidence and explicit limits.
- `physical-qualification.json`: **NOT_RUN** physical gates; no simulation result is a measurement.
- `source-status.json`: targeted dated supplier/manufacturer access, failed retrieval and unquoted positions.
- `verification.md`, `verification-commands.log`, `export-commands.log`: exact reproducible commands and tool diagnostics.
- `file-manifest.json`, `SHA256SUMS`: native/review/document/tool hashes, relative to repository root.

`RF80_V1.dsn` is an optional **final-state offline interchange export**, not a
manufacturing layer. `routing-history/` contains intermediate route/debug
records, including intentional temporary gaps that are now closed; those
records are not the final connectivity report. Use DRC/XML/native PCB above.

The native DNP flags and full render represent the full assembly. Fox-only
requires its own population list and R228/R348/R349 links, with all NORMAL
parts absent. TH301 is one remote insulated PA-case sensor, not a parallel
board-mounted second sensor. No layout-only removal changes protective circuits.

From repository root, verification/export commands are:

```sh
/usr/bin/python3 tools/m4a_exports.py --render
/usr/bin/python3 tools/m4a_verify.py --logic
/usr/bin/python3 tools/m4a_artifact_audit.py
/usr/bin/python3 tools/m4a_geometry_review.py
/usr/bin/python3 tools/m4a_document_checks.py
/usr/bin/python3 tools/m4a_artifact_audit.py --manifest
sha256sum -c hardware/80m/production/review/M4A-V1/SHA256SUMS
```

The render needs a local X display (the recorded run used `DISPLAY=:93`) and
software Mesa. Do not run placement/derive/import/ground-repair commands as
verification: they are CAD mutation tools. Native CAD is the routing authority;
the local offline router is not required to inspect or reproduce exports.
The reviewed E2 handoff is a separate directory and must never be regenerated
from the compact board.
