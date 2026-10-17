# M5B-E4R1 engineering decision

**GO for independent review of five unpopulated evaluation boards. No upload, purchasing or fabrication is authorized.** The source-joint layout and a controlled prototype assembly process are now defined. This is a candidate commit; no acceptance tag is created. E4's original HOLD evidence remains at `920da7b`. The last accepted CAD baseline remains `m5b-e3` / `95f189c`.

| Gate | Status |
|---|---|
| A — ordinary PCB geometry | PASS local CAD/DFM checks |
| B — credible prototype assembly process | Defined, with initial inspection and qualification required |
| C — five bare evaluation boards | GO for independent manufacturing review only |
| D — physically qualified PA assembly | NOT_RUN |
| E — operational transmitter approval | NOT_RUN |

The **110 °C conservative design target is NOT_MET**. The **125 °C physical qualification gate remains OPEN**. Unrestricted 4 W operation is not approved.

Implemented: **16 open source vias + 20 side vias + 8 end vias + 54 wing vias = 98 thermal vias**. One 2.1 × 5 mm source-mask opening and five paste windows replace the mask islands. Nominal solderable copper is **9.37 mm²**, which is not measured solder coverage. The assembly uses a standard 0.12 mm stainless local stencil, controlled reflow, first-board X-ray and thermal correlation. No closure, plugging or solder-fill conduction is credited.

The 180 × 140 mm board remains standard two-layer FR4, 1.6 mm / 1 oz, green/white, lead-free HASL. The Fischer SK 81 100 SA, 15 × 44 × 10 mm bar and M3 mounts remain. Electrical values, signal traces, component positions, controller interface, protection and population exclusivity are unchanged. Local source-ground rails widen from 3.2 to 3.6 mm; nominal adjacent G/D clearance is 0.20 mm. RF parasitics and stability require the same integrated-board commissioning checks.

At 40 °C ambient and 4 W continuous PA heat, calculated junction temperatures round to **91 °C nominal / 122 °C conservative / 138 °C poor contact**. Combined thickness, contact and joint degradation reaches approximately **129 °C**. These are conditional predictions, not physical passes. The corrected model includes hole-area loss and distributed via coupling. The 0.10-to-0.05 mm mesh change is 0.02 K/W; the retained numerical allowance is 1 K/W. Physical joint, plating, TIM and convection uncertainty dominates.

KiCad 10.0.6: **ERC 0 errors / 0 warnings; DRC 0 errors; 0 unrouted; 0 parity; 11 individually justified bodyless-feature courtyard warnings; 0 exclusions.** Only the unused tuning-profile category is ignored. Coverage remains 4,096 logic combinations, 39 states, 37 baseline mutations, 42 manufacturer maps, 26 ST positions and 320 package/pad sets. Eleven standard DFM mutations and 20 source/RF/mechanical/model negative tests pass. Delivery checks bind the fresh Gerbers, drills, variants, IPC and native hashes; they do not claim supplier CAM acceptance.

Electrical BOM and PA cooling costs are unchanged. The new explicit stencil/paste allowance is **€30 for one batch / €3 per board at ten**, estimated. E4 did not quote those items, so this is not a demonstrated purchase-cost increase. Inspection, X-ray, rework, shipping, VAT and labor remain unquoted or separate. The five-board allowance of €41.50–83 is an estimate, not a JLCPCB quote. No stock was reserved or data submitted.

Next: independently review the source joint, process and conditional thermal result; authorize a bare-board quote/order separately; then authorize staged first-board assembly and qualification. Only afterward perform the existing RF, AM, protection and endurance acceptance. Read the [source-joint analysis](M5B_E4R1_SOURCE_JOINT.md), [thermal review](M5B_E4R1_THERMAL_REVIEW.md), [manufacturing and assembly process](M5B_E4R1_MANUFACTURING.md) and [review package](../hardware/2m/review/M5B-E4R1/README.md). No hardware activity has occurred.
