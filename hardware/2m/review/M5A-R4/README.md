# M5A-R4 electrical review — pre-layout hold

One actual integrated-transmitter schematic; **no RF2M PCB/DRC/Gerbers** are claimed. No purchases, manufacture, assembly or RF operation.

Start with the [decision](../../../../docs/M5A_R4_REVIEW_DECISION.md), [modernization/interface](../../../../docs/M5A_R4_MODERNIZATION.md), [traced ST RF stage](../../../../docs/M5A_R4_RF_STAGE.md), [costs](../../../../docs/M5A_R4_COST_RECONCILIATION.md), [AM/power](../../../../docs/M5A_R4_AM_POWER.md) and [one-device acceptance](../../../../docs/M5A_R4_BUILD_AND_TEST.md).

[Editable schematic](../../RF2M.kicad_sch), [PDF](RF2M.pdf), [exported netlist](RF2M.net.xml), [itemized BOM](RF2M_BOM.csv), [population list](positions.csv), [pinout audit](pinout-audit.json). sources.json records obtained manufacturer PDFs, dates, hashes and failed original downloads; whole third-party PDFs/artwork are not redistributed.

verification.json is Boolean/connectivity/physical-landing assertion evidence only; analog/RF/thermal/endurance remain NOT_RUN. ERC footprint warnings and remaining missing landings are explicitly retained. The 50-ohm MMIC-to-ST-interstage adaptation and listed reservoir/coil/connector definitions block a credible integrated PCB release. DF782 and TI RNW candidate lands are manufacturer-derived and dimensionally checked; their thermal/stencil/assembly integration remains unqualified. No coupons or competing boards are proposed.

R3 is preserved at Git tag m5a-r3(daf994c); R1/R0 tags and R1 native archive remain unchanged. R4 checks verify the old R3 hashes IN THAT TAG. Historical root-relative R3 hashes naturally refer to old CAD, not current R4 files. RF80/M4A/accepted ADR files are hash-preserved.

Reproduce from repository root: `python3 tools/m5a_r4_review.py`; then `python3 tools/m5a_r4_review.py --check`. Review status is not manufacturing authorization.
