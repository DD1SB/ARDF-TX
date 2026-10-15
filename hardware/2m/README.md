# RF2M electrical candidates

The active editable project is **M5A-R3**, a private-construction DL3BBX-derived schematic. It is **NOT RELEASED** and **NO_GO for PCB commitment**: exact legacy RF-device supply/manufacturer, some physical landings, upper-power AM headroom and thermal behavior remain unresolved. There is no RF2M PCB or manufacturing package.

Start with [the R3 review decision](../../docs/M5A_R3_REVIEW_DECISION.md) and [schematic PDF](review/M5A-R3/RF2M.pdf). The [itemized BOM](review/M5A-R3/RF2M_BOM.csv) is a conditional allowance, not an order list. Source rights are recorded in [LICENSE-REFERENCE-DL3BBX.md](LICENSE-REFERENCE-DL3BBX.md).

R1 remains at Git tag `m5a-r1` and [its native archive](archive/M5A-R1/README.md); its review exports remain unchanged under `review/M5A-R1/`. R0 is similarly archived. R2 produced research documents only. Do not run the historical R0/R1 generator against the active project to review an older revision; open its archive instead.

Reproduce the R3 artifacts from the repository root:

```sh
python3 tools/m5a_r3_design.py
kicad-cli sch erc --format json --output hardware/2m/review/M5A-R3/erc.json hardware/2m/RF2M.kicad_sch
kicad-cli sch export netlist --format kicadxml --output hardware/2m/review/M5A-R3/RF2M.net.xml hardware/2m/RF2M.kicad_sch
kicad-cli sch export pdf --output hardware/2m/review/M5A-R3/RF2M.pdf hardware/2m/RF2M.kicad_sch
python3 tools/m5a_r3_verify.py
python3 tools/m5a_r3_models.py
python3 tools/m5a_r3_docs.py
kicad-cli sch erc --format json --output hardware/2m/review/M5A-R3/fallback-r1-erc.json hardware/2m/archive/M5A-R1/RF2M.kicad_sch
kicad-cli sch export netlist --format kicadxml --output hardware/2m/review/M5A-R3/fallback-r1.net.xml hardware/2m/archive/M5A-R1/RF2M.kicad_sch
python3 tools/m5a_r3_checks.py
```

KiCad CLI 10.0.6, Python 3.12 and Poppler were used. Only standard installed symbol/footprint libraries and the local symbol file are needed. The inherited R1 generator is imported into a temporary directory for template reuse; R1 review artifacts are not overwritten. External source hashes/access failures are in the R3 review package. No calculation or CAD check is an RF, analog startup, thermal or endurance measurement.
