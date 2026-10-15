# RF2M M5A-R1 — review candidate, NOT RELEASED

See [engineering decision](../../../../docs/M5A_R1_REVIEW_DECISION.md). **NO-GO for coupon layout while ST reference topology/physical final landing are OPEN.** Actual KiCad ERC0errors/3OPEN-footprint warnings; digital regression 4096 combinations/36 scenarios/14 mutations. These are not physical passes.

Native project stays inhardware/2m; R0 native/archive and review files remain preserved at tagm 5a-r0. Root schematic is authoritative; OPEN matching values and footprints intentionally prevent manufacture. PDF/netlist/ERC/BOM/pin audit/cost/analysis files are generated from R1. No PCB/Gerbers exist.

Reproduce from repository root:

```sh
python3 tools/m5a_r1_design.py
kicad-cli sch erc --format json --output hardware/2m/review/M5A-R1/erc.json hardware/2m/RF2M.kicad_sch
kicad-cli sch export netlist --format kicadxml --output hardware/2m/review/M5A-R1/RF2M.net.xml hardware/2m/RF2M.kicad_sch
kicad-cli sch export pdf --output hardware/2m/review/M5A-R1/RF2M.pdf hardware/2m/RF2M.kicad_sch
python3 tools/m5a_r1_verify.py
python3 tools/m5a_r1_costs.py
python3 tools/m5a_r1_baskets.py
python3 tools/m5a_r1_analysis.py
python3 tools/m5a_r1_documents.py
python3 tools/m5a_r1_finish.py
```

Use KiCad 10.0.6/Python 3.12.3. No ngspice result is claimed for R1; analytical models are explicit assumptions. Preserve third-party source rights; sources.json distinguishes unread diagrams from retrieved text. All physical-gates.json entries are NOT_RUN.
