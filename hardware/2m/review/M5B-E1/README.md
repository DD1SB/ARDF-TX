# RF2M M5B-E1 independent review package

**REVIEW ONLY — NOT RELEASED — HARDWARE TESTS NOT_RUN.** Native project: `../../RF2M.kicad_pro`, `../../RF2M.kicad_sch`, `../../RF2M.kicad_pcb`; prior electrical baseline tag `m5a-r4`, commit `b44fe3b`. RF80 is unchanged.

Start with `final-checks.json`, `DRC.rpt`, `DRC-coverage.json` and `MANUFACTURING.md`. Zero DRC errors/unrouted/parity is accompanied by12 visible warnings, not a clean-checker claim. The unlocated F.Cu sliver needs independent CAM closure before ordering. Courtyard warnings concern eleven bodyless copper features.

- `RF2M.pdf`: complete editable-source schematic export.
- `top-copper.svg`, `bottom-copper.svg`, assembly PDFs/SVGs and actual KiCad `RF2M-3D*.png`: placement/routing review. Dimensional-envelope and missing visualization status is in `3D-model-status.json`; renders do not qualify footprints or thermal performance.
- `gerbers/`: fresh GerberX2, separate PTH/NPTH Excellon,PDF drill maps and job file; no files were submitted anywhere.
- `RF2M.net.xml`, `pad-connectivity.csv`, `pinout-audit.json`, `verification.json`, `power-path-widths.json`: electrical/physical assertions and mutations.
- `RF2M-logical.ipc`, `RF2M-physical-netties.ipc`, `fabrication-net-aliases.json`: schematic versus actual net-tie E-test definitions.
- `BOM_*.csv`, `RF2M_BOM.csv`, `costs.json`: explicit2S/4S/training populations and6/10/20 fleet costs, observed versus unquoted positions.
- `stackup-mechanical.json`, `thermal-contact.json`, `transmission-lines.csv`, `calculations.json`, `input-match-sensitivity.csv`, power/thermal/endurance tables: estimates and fabrication assumptions.
- `SHA256SUMS`, `file-inventory.json`, `native-inputs.json`: exact local revision identity; `preserved-baseline.json` protects historical/RF80 files. `development/` contains non-final routing history; its intermediate DRC reports are not final acceptance results.

Reproduce final checks from repository root with KiCad10.0.6/systemPython: `tools/m5b_exports.py --checks`, `tools/m5b_verify.py`, `tools/m5b_power_widths.py`, `tools/m5b_models.py`, then `tools/m5b_exports.py --render` with a local X display and `tools/m5b_review.py`. Prefix Python tools with `/usr/bin/python3`; model-only script also works with `python3`. DRC code5 means retained warnings, not zero violations. Inspect reports. Rendering uses local softwareGL/Xvfb. Routing/construction helper scripts are development tools, not an instruction to regenerate or overwrite the reviewed native PCB.

Read the seven `docs/M5B_E1_*.md` documents for corrections, packages, input matching, safety, costs, commissioning and decision. GO for independent evaluation-board review; no procurement, manufacture, assembly or energizing is authorized. Commercial/source rights are inherited from the documented reference provenance; no third-party datasheets or historical articles are redistributed here.
