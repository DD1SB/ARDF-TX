# M5A-R3 review package — NO_GO for PCB commitment

The active project is a complete, editable **private DL3BBX-derived candidate schematic**, not a qualified/buildable production design. No RF2M PCB, DRC report, Gerbers or3D manufacturing files exist: exact RF-device supply/manufacturer and physical landings are unresolved. Upper-power sineAM headroom is not proved. No purchases, fabrication, assembly or RF operation occurred.

Start with [review decision](../../../../docs/M5A_R3_REVIEW_DECISION.md), [reference audit](../../../../docs/M5A_R3_PROVEN_TRANSMITTER_AUDIT.md), [selection/controller contract](../../../../docs/M5A_R3_RF_SELECTION.md), [AM/power](../../../../docs/M5A_R3_AM_AND_POWER.md), [modernization](../../../../docs/M5A_R3_COMPONENT_MODERNIZATION.md), [BOM](../../../../docs/M5A_R3_BOM.md) and [one-board build plan](../../../../docs/M5A_R3_BUILD_PLAN.md).

CAD: [native project](../../RF2M.kicad_pro), [schematic](../../RF2M.kicad_sch), [PDF](RF2M.pdf), [netlist](RF2M.net.xml), [manifest](../../RF2M.electrical.json). The three RF pages are wired circuit drawings; named nets cross supply/control sheets. All hardware measurements are NOT_RUN.

Evidence: erc.json; verification.json (static logic, state, pin/value mutation tests); pinout-audit.json; final-checks.json; sources.json (including native-Eagle import failure); fallback-r1-* read-only regression; costs.json and per-reference RF2M_BOM.csv; RF/thermal/endurance CSV/JSON models. Footprint warnings are visible, not waived. Missing custom-symbol landings are separately listed because ERC does not warn on all of them.

R1 remains at Git tag m5a-r1 (4785057) and ../../archive/M5A-R1/. R0/R1/R2 review exports, RF80/M4A/controller/accepted ADRs remain unchanged; preserved-baseline.json records the starting467-file snapshot. Starting Git HEAD was1d8d88f; this package describes the working-treeR3 revision, not a claimed new commit.

Reproduction commands are in [RF2M README](../../README.md). Run `python3 tools/m5a_r3_package.py` after exports/checks to reseal; then `python3 tools/m5a_r3_package.py --check` from the repository root. SHA256SUMS paths are root-relative. Manufacturer and third-party source permissions remain separate from project code licensing; see ../../LICENSE-REFERENCE-DL3BBX.md.
