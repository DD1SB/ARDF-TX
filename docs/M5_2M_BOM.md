# M5A itemized candidate BOM and cost scope

Date: **2026-10-15**. **Candidate materials, not an ordering list.** The authoritative itemization is [RF2M_BOM.csv](../hardware/2m/review/M5A-R0/RF2M_BOM.csv): every fitted reference at6/10/20, full MPN or OPEN, footprint, value, population, supplier/identifier, demand, assumed MOQ/multiple, price basis, stock status and source. [Master positions](../hardware/2m/review/M5A-R0/RF2M_positions.csv) also disclose omitted/test/non-physical references. [Costs JSON](../hardware/2m/review/M5A-R0/costs.json) and [generator](../tools/m5_2m_costs.py) reproduce totals.

| Population | Fitted physical parts | ICs | 6 units EUR/board | 10 units EUR/board | 20 units EUR/board |
| --- | --- | --- | --- | --- | --- |
| BOOST2S | 267 | 23 | 74.61 | 74.61 | 74.61 |
| BUCK4S | 263 | 23 | 72.77 | 72.77 | 72.77 |
| TRAIN_ONLY | 104 | 14 | 16.37 | 16.37 | 16.37 |


Test pads and power declarations are not purchased ICs or separately purchased parts. The variants include normal/training RF connectors, fuse and mandatory board-level enables. TRAIN_ONLY omits the final, driver, normal converters, high-power filter, input power chain and local PA monitors; it is the same RF2M product PCB population. R517/R518 give the unused main op-amp inputs defined levels in this population. R101/R807/R809 value substitutions are explicit; do not fit the2S values on a4S assembly.

## Evidence and procurement limits

All comparison totals are provisional **net EUR material budgets**. VAT is excluded; at an illustrative19% tax, multiply the applicable taxable basket by1.19, rather than adding tax to selected lines twice. Destination VAT, freight, currency settlement and any import charges remain separate. U501 uses observedUS$16.35 divided by ECB14October2026's1.1195USD/EUR; this€14.6047 is an informational conversion, not a supplierEUR invoice. Q501 retains the observed€15.06 single figure as a conservative net allowance without an unverified tax deduction. No new stock reservation or cart was made.

RF inductor allowances use the observedCoilcraft familyUS$0.92/ECB equivalent; exact value/region checkout remains OPEN. Other lines are estimates, not verified quotes. Estimated MOQ1/multiple1 means an intended cut-tape/manual-assembly route requiring confirmation, not evidence of available cut tape. No3,000-piece reel is required by a claimed achieved price. Identical MPN demand is aggregated across a fleet before applying observed breaks; no discount is invented at6/10/20, so several totals are flat.

There are35 OPEN-MPN reference positions in full2S, including RF capacitors, power magnetics, fuse/shunt, thermistor and mating connectors. An existing generic footprint is not exact package qualification. The critical remaining footprint blockers are PD55008 formed-lead PowerSO10RF, Mini-CircuitsDF782/PL523, TI RNW boost, connector geometry and certain power magnetics. They are named in the pinout audit and schematic review. Current/EOL status is not inferred merely from an old datasheet. No obsolete transistor is selected to make the total look lower.

| Function, full2S | EUR/board at10 |
| --- | --- |
| connector | 3.00 |
| interface | 0.34 |
| source | 2.28 |
| decoupling | 0.81 |
| interlock | 3.12 |
| passive | 0.10 |
| input | 1.50 |
| supply_isolation | 0.56 |
| converter | 4.09 |
| protection | 2.08 |
| power | 0.33 |
| driver_supply | 2.59 |
| am | 1.04 |
| modulator | 1.90 |
| training | 7.65 |
| source_filter | 2.98 |
| driver | 15.61 |
| pa_match | 2.73 |
| pa | 15.06 |
| bias | 1.43 |
| output_filter | 5.43 |


## Why the old€36 estimate is not met

The selected final and driver alone are approximately€29.66. The driver's stronger compression capability, actual small-quantity formed-lead PA price, explicit matching/chokes/filter inductors, AM/pass circuitry and real power/protection parts exceed the old incompletely qualified basket. This schematic has not achieved a low-cost production target. Removing roughly€3 of digital fail-off or€2 of analog protection would not close the gap and would create distinct failure paths.

The [PA comparison](M5_2M_PA_SELECTION.md) identifies the concrete saving route: measured high PA gain could permit the old€2.82 PHA-1+ candidate, saving about€11.78 before its rail/drive changes. Even that substitution needs measured144MHz compression and source drive. Cheaper qualified wirewound RF parts or reproducible wound coils could reduce magnetic material cost, but current/Q, parasitics and tuning labor must be included. These are conditional alternatives, not achieved savings. The affordable legacy ATX2/DL3BBX final devices and reported powers cannot simply replace the selected capability.

The RD07/RD12 function-normalized baskets have OPEN final sourcing,144MHz match and driver requirements. No complete price is manufactured for those missing lines. PHA-101's observedUSD comparator saves only about€1.46 against the selected lower PHA13 sourcing, with less margin. A5W-FM handheld price is not a true-AM materials baseline.

## Separate installed and fleet costs

The table above is components only. Since noPCB is laid out, a standard two-layer bare-board allowance is **€2–6 per module**, explicitly unquoted and dependent on eventual area/panel/freight. Add **€2–4 RF harness**, **€8–15 antenna/feed materials** and **€4–7 heat spreader/sinks, insulating pads/sleeves and mounting**. Mandatory board RF connectors are already in the component total; do not count them again as an external antenna connector allowance. Installed module allowance is therefore component total **+€16–32**; no labor or enclosure is concealed there.

Controller/RTC material remains a separate shared€15–20 allowance; existing source budgets are historical, not rewritten. Enclosure adds€3–6. A protected pack includes cells, BMS, insulating/weld/connector material and labor separately. Reuse datedM2 cell observations:25R net€1.73≥10/1.64≥50/1.56≥100, M35A€3.16≥30/3.00≥100, plus€0.62 per cell for supplier tags. Stock/pack qualification is not established by those historical observations.

Example2S3P/M35A pack material: at6/10/20 transmitters, cell demand36/60/120 gives tagged-cell material€22.68/22.68/21.72 per pack; add estimated€3 BMS and€3 insulation/interconnect for **€28.68/28.68/27.72**, excluding welding/assembly labor.4S2P/M35A has48/80/160 cells, tagged material€30.24/30.24/28.96, plus€4.50 BMS and€3 interconnect: **€37.74/37.74/36.46**. These do not assume identical charger/BMS for2S and4S.

For10 full2S systems, component allowance plus installed accessories, shared controller,2S3P pack and enclosure is approximately **€137.29–161.29 each**, before labor, freight and charging; the range is a budget, not a purchased-material receipt. One qualified1 A charger per four units is a separate shared-fleet assumption:2S€15 /4S€20 each estimated, so6/10/20 units need2/3/5 chargers. Slow charge turnaround and spare packs must be planned; a charger allocation is not a second battery cost inside every RFPCB.

Assembly, winding, rework and VNA/RF/AM calibration labor is **unquoted**, with no fictitious zero-hour production claim. Shared test instruments, RF fixtures and one-time engineering are outside per-unit material. The completed Foxoring audit and all80m material numbers remain unchanged.

If isolation/coexistence testing requires shielding, add an explicitly provisional€1–3 material allowance; this is not an achieved quote or already qualified shield. The present cost is a conservative candidate basket, not proof that no cheaper compliant design exists.
