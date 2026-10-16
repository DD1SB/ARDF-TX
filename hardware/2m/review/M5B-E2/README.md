# RF2M M5B-E2 manufacturing review package

**REVIEW ONLY — NOT RELEASED — ALL HARDWARE TESTS NOT_RUN.**

Native project: `../../RF2M.kicad_pro`, `../../RF2M.kicad_sch`, `../../RF2M.kicad_pcb`. E1 is preserved at `m5b-e1` / `6931260`. E2 changes localized control copper, one ground-fill notch, PCB revision marking and the minimum connection-width threshold. Electrical schematic, BOM, RF structures and RF80 remain unchanged.

Start with `final-checks.json`, `DRC.rpt`, `DRC-coverage.json` and `MANUFACTURING.md`. The result is zero errors/unrouted/parity and eleven explicitly retained non-component courtyard warnings. No exclusion or severity reduction conceals a finding.

- `RF2M.pdf`: fresh complete 20-page schematic export. The E1 electrical title is intentionally retained; E2 identifies the PCB revision.
- `top-copper.svg`, `bottom-copper.svg`, assembly PDFs/SVGs and variant placement CSVs: final copper and assembly data.
- `RF2M-3D*.png`: fresh actual KiCad renders. `3D-model-status.json` identifies dimensional envelopes and three missing connector-body models.
- `gerbers/`: **the final E2 manufacturing-review set**, including Gerber X2, separate PTH/NPTH Excellon, drill maps and job data. Nothing was uploaded.
- `copper-investigation/`: native analysis copies and freshly generated comparison Gerbers. **Never manufacture these files.** `before` is E1; `sliver-only` isolates the original correction; `strict-before` activates the 0.15 mm neck check; `after` represents E2.
- `copper-before.png`, `copper-after.png`, `copper-investigation.json`, `layout-delta.json`, `connection-width-before.json`: exact findings and correction evidence.
- `RF2M.net.xml`, `pad-connectivity.csv`, `pinout-audit.json`, `critical-package-audit.json`, `verification.json`, `power-path-widths.json`: electrical, manufacturer and package checks.
- `RF2M-logical.ipc`, `RF2M-physical-netties.ipc`, `fabrication-net-aliases.json`: schematic versus intentional physical TL net ties. Use the physical version for bare-board E-test.
- `RF2M_BOM.csv`, `BOM_*.csv`, `costs.json`, `COST_SUMMARY.md`, `E1-E2-cost-delta.*`: itemized 6/10/20 costs and unchanged E1-to-E2 material. `R4-context-cost-delta.csv` is historical context, not the E2 delta.
- `stackup-mechanical.json`, `stackup-sensitivity.csv`, `alternative-stackup-proposals.csv`, `transmission-lines.csv`, `RF-ground-geometry.json`, `thermal-contact.json`: fabrication assumptions and native geometry checks.
- `acceptance-register.csv`: every physical test is NOT_RUN.
- `native-inputs.json`, `file-inventory.json`, `SHA256SUMS`: exact final file identity. `preserved-baseline.json` protects E1, RF80 and historical work.

Reproduce sequentially from the repository root using system Python and KiCad 10.0.6:

```sh
/usr/bin/python3 tools/m5b_e2.py checks
/usr/bin/python3 tools/m5b_e2.py verify
/usr/bin/python3 tools/m5b_e2.py evidence
DISPLAY=:97 LIBGL_ALWAYS_SOFTWARE=1 /usr/bin/python3 tools/m5b_e2.py exports --render
/usr/bin/python3 tools/m5b_e2.py reports
/usr/bin/python3 tools/m5b_e2.py artifacts
sha256sum -c hardware/2m/review/M5B-E2/SHA256SUMS
```

Use a working local X display for rendering. `correct` is the separate idempotent E1-to-E2 patch, not ordinary verification. CLI DRC exit5 represents retained warnings. Zone refill saves the board; do not run board writers concurrently. Do not run E1 export generators against its frozen package.

Read the seven `docs/M5B_E2_*.md` documents for findings, fabrication, fit, cost and commissioning. **GO for independent manufacturing review and quote preparation.** A compatible stack/process, actual quote and explicit user approval are still required before any order. No procurement, fabrication, assembly, power-up or RF transmission occurred.
