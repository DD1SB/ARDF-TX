# M5B-E6 common-heatsink feasibility

**Preferred concept A; no manufacturing selection released.** The [decision](M5B_E6_REVIEW_DECISION.md) stops before native PCB edits because the local PA path/protection envelope is unresolved. One independently supported cooler for Q501, Q401 and Q402 remains mandatory. No separate pass/helper cooler is selected for E6.

| Alternative | Mechanical result | Thermal uncertainty | Cost/assembly result | Disposition |
| --- | --- | --- | --- | --- |
| A: flat cooler below PCB | Existing PA region, horizontal formed-lead Q401/Q402; one common plane and local tool opening | Source/via/interface bottleneck; ordinary cooler orientation must be bounded | Reuses a small commercial extrusion; ordinary saw/drill/tap work | Preferred concept; HOLD |
| B: structural chassis-side plate | Continuous flat stock could support all three, but needs additional clearance/rerouting or longer PA path | Flat mass is not a qualified natural-convection exchanger; box coupling unknown | Low raw material cost, more enclosure-dependent assembly | No advantage established |
| C: commercial aluminum enclosure | Common inner wall can be a cooler if geometry and airflow support it | Solar absorption, accessible surface and enclosure heat rejection become coupled limits | Repeatable purchase possible, but enclosure/fin geometry/cost not selected or quoted | Not selected |

No custom extrusion, milled pocket, fan, heat pipe, new PA transistor or modulation change is proposed. B/C are conceptual alternatives, not falsely completed supplier/CAD designs. A is preferred for simplicity and retained RF geometry, not because it produces the lowest theoretical junction temperature.

The A comparator is **Fischer SK81 100 SA, 100 × 100 × 15 mm, 4 mm base**. The [manufacturer-authored drawing](https://www.farnell.com/datasheets/3625639.pdf) identifies the extrusion dimensions; the [retailer listing](https://www.reichelt.com/de/en/shop/product/heat_sink_100_mm_aluminium_2_2_k_w-227984) indexes 214 g and €7.30 including 19% VAT. Its title says 2.2 K/W while a generic property says 2 K/W; the analysis uses 2.2 only as an upright comparator, not a guaranteed installed rating. No item was bought or reserved.

Concept bounds X42..142/Y5..105, common upper plane Z≈−8 mm relative to RF PCB top. A 15 × 44 × 6.2 mm aluminum bar couples the PA source region to that same extrusion; there are no second or third coolers. The bar weighs approximately 11.05 g at 2700 kg/m³. Cooler+bar is 225.05 g. **Full assembly mass is not closed**: 245–270 g is an estimate including ordinary supports/fasteners/interfaces, excluding a final enclosure. It is not a weighed assembly.

The [feasibility sketch](../hardware/2m/review/M5B-E6/common-cooler-concept.pdf) labels simplified geometry and unapproved hole/tool positions. It is not a native KiCad assembly, STEP model or machining template. Final drill locations, bracket loads and tolerances are withheld at HOLD.

## Source bottleneck and insulation

Q501 remains at (92,55), angle 0, with unchanged RF source/matching geometry: 16 open source +20 side +8 end +54 wing vias, 98 total; 2.1 × 5 mm source mask opening, five paste windows totaling 6.765 mm² and 0.12 mm stencil. No solder-fill, plugged/capped vias or premium copper is assumed. First-article source-joint inspection/X-ray remains required.

At the same conservative 10 µm via wall/30 µm foil/four ineffective inner-via boundary, the unchanged E5 grease path is 10.773 K/W. A full electrically insulating [TSP1600](https://datasheets.tdx.henkel.com/BERGQUIST-SIL-PAD-TSP-1600-en_GL.pdf) sheet raises it to 15.896 K/W in the pressure-margin case; poor pressure reaches 18.402 K/W. The 0.127 mm sheet is rated 3 kVAC, but its manufacturer pressure-dependent impedance must be used, not just bulk conductivity. Contact terms are not added twice.

The [KERATHERM 86/82 manufacturer catalogue](https://www.kerafol.com/wp-content/uploads/2026/05/Kerafol_Katalog_Keratherm_Web_06-26.pdf) gives 0.25–0.30 mm, 6.5 W/mK and 1 kVAC. Bulk-only FVM gives 11.084 K/W; doubling bulk resistance as an assumed contact allowance gives 11.847 K/W, thicker/triple allowance 12.839 K/W. The catalogue's reference 0.09 K/W is not transferred to this bar without its test geometry/pressure. These are compared interfaces, not selected/qualified resistance guarantees. [Results](../hardware/2m/review/M5B-E6/source-interface-alternatives.json).

A conductive bar cannot simply press through solder mask: non-GND B.Cu routes cross the contact footprint. Grease and anodizing are not electrical insulation. Clearing/rerouting that region to permit verified ground-only metal contact is a possible future local alternative, **not implemented or declared RF-equivalent here**. It needs a native copper/ground/clearance audit and a conservative thermal proof. Changing source vias back to the old 40-open-hole pattern would revive the solder-wicking/source-joint problem; it is not a free thermal improvement. Reorienting Q501 rigidly does not change its local thermal impedance and could disturb RF geometry. Ordinary two-layer spreading alternatives must be evaluated against RF return and real source-joint manufacture before selection.

[JLCPCB's current capabilities](https://jlcpcb.com/capabilities/pcb-capabilities) specify **average** hole plating 18 µm; this does not justify assuming every local barrel is at least 18 µm. The existing 10 µm sensitivity cannot be deleted based on a marketing average. No normal-fabrication assembly bound has yet closed the source-path requirement in the [transient analysis](M5B_E6_TRANSIENT_THERMAL.md).
