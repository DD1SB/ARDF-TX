# RF2M M5B-E4 thermal candidate — HOLD

Active native project: `hardware/2m/RF2M.*`. Baseline `m5b-e3` / `95f189c`. No E4 acceptance tag: source-joint reproducibility remains unresolved. No manufacturing or operational release.

Read `../../../../docs/M5B_E4_REVIEW_DECISION.md` first. `gerbers/` contains freshly generated E4 review data, not a manufacturing release. `development/` contains analysis inputs and deliberate rejected DFM mutations; never fabricate them. `thermal-model.json` and `thermal-sensitivity.csv` are calculations; all physical tests NOT_RUN. `thermal-assembly-audit.json` explains the source mask/solder HOLD. `final-checks.json` separates passing CAD checks from the acceptance decision.

Mechanical drawings: `mechanical-top.svg`, `mechanical-bottom.svg`, `mechanical-section.svg`. Actual KiCad views: `RF2M-3D*.png`; the added heatsink is an explicitly identified dimensional envelope, not qualified manufacturer fin CAD. Existing component envelopes/missing connector bodies remain disclosed by E3. Native/assembly drawings and audits govern fit.

Manufacturing options remain standard JLC2LFR4,180x140,1.6mm,1oz,green/white,lead-freeHASL; no controlled impedance or premium via treatment. Separate PTH/NPTH drills and physical-net-tie IPC accompany logical netlist. Do not upload or order. Cost estimates are not quotations. Source/inspection limitations preclude acceptance even though native bare-copper DFM passes.

Reproduce from repository root using `/usr/bin/python3 tools/m5b_e4.py checks`, then `verify`, `dfm`, `models`, `thermal`, `engineering`; `DISPLAY=:97 /usr/bin/python3 tools/m5b_e4.py exports --render`; then `reports` and `delivery`. KiCad10.0.6 and its Python pcbnew binding are required. Rendering needs a working X display/software OpenGL; set DISPLAY appropriately. No tool performs external submission or physical operations. Source artwork implementation is `tools/m5b_e4_design.py`, which derives from frozen E3; do not run it on unrelated user changes.
