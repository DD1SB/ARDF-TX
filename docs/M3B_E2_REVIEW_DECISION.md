# M3B-E2 — pre-manufacturing review decision

Date: **2026-10-15**. **CONDITIONAL GO for independent review of a small bare evaluation-PCB batch. NO-GO to place an order now, or to use an unrestricted4S pack, populate an unqualified driver/PA, or release a transmitter.** Independent engineering review, fabrication-capability confirmation and explicit user manufacturing authorization remain required. No file was sent to a manufacturer; no parts/boards ordered, fabricated, assembled or energized.

The existing **210×160mm two-layer RF80 board** has been corrected, not replaced. Native [schematic](../hardware/80m/RF80.kicad_sch), [PCB](../hardware/80m/RF80.kicad_pcb), [electrical manifest](../hardware/80m/RF80.electrical.json) and [complete E2 review package](../hardware/80m/review/M3B-E2/README.md) describe the same E2 revision. **m3b-e1 /55a5b3f** preserves E1 and all E1 review outputs; earlier R1/R0 history remains intact. Proposed ADR-0012 remains proposed.

## Confirmed defects resolved

1. **ST BD140 Q403 base/emitter were reversed.** Manufacturer Rev5 drawing0016114E requires1B2C3E. Correct symbol numbering plus180° real footprint rotation about the collector now give1SHAPE_BASE/2VPA_SHAPED/3VPA_LOAD, without RF rerouting. Holes enlarged1.00→1.30mm for actual maximum lead dimensions.
2. **TI TL431 U311 REF/anode application nets were wrong.** TI DBZ1K2REF3A now has1+2VREF_2V5,3GND. Four short tracks replaced locally and one ground via added. Its corrected reference is essential to the intended analog thresholds.
3. **Manufacturing coverage was incomplete.** All five ignored DRC categories enabled;69 inherited footprint-filter warnings resolved by exact real-land filters, not suppressed. Mask expansion/web and silk/annular/minimum constraints are explicit. D302 now specifies Littelfuse, with its real clamp limits documented.

[Corrections](M3B_E2_CORRECTIONS.md), [manufacturer/mechanical audit](M3B_E2_FOOTPRINT_AUDIT.md), [DRC coverage](M3B_E2_DRC_AUDIT.md), [power protection/gates](M3B_E2_POWER_PROTECTION.md), [cost delta](M3B_E2_COST_DELTA.md). All other existing track/via geometries, RF values/windings and independent R1 interlocks are preserved. No controller/VHF or architectural redesign occurred.

## Verification evidence and its boundary

| Check | Result |
| --- | --- |
| ERC / all-severity DRC / schematic parity / unrouted |**0 /0 /0 /0**; no ignored DRC checks or exclusions; three informational ERC defaults documented |
| Actual native PCB/netlist memberships |**664**,273electrical footprints+4mounts,74probe pads,329vias |
| Manufacturer physical mapping |**55 critical devices**, **10 negative cases rejected**, including real archived E1 Q403/U311; pinout test independent of ERC/DRC |
| Current-netlist R1 regression |**256 combinations,31 state scenarios,16 timing corners**; U202-polarity mutations, path/power inhibit, deliberate rearm retained |
| Preserved M1/M2/Fox arithmetic/document checks |Pass; version-specific R1/E1 suites and current E2 assertions are separately identified in package verification record |
| Passive protection models |32 analytic input corners,24 input and5 driver ngspice cases;100µs isolation counterexample fails12.6V gate as expected |
| Export consistency |Nine current Gerber layers, separate372PTH/4NPTH drill files/maps,195full-population placement rows,IPC/netlist, fresh schematic/assembly/copper/actual KiCad3D exports and checksums |
| Physical input, reset/ARM timing, driver fault, RF, thermal, field range, endurance |**NOT_RUN** |

The E1 passing manufacturer assertion was wrong; it did not establish the installed BD140 pinout or TL431 application. E2 tests explicitly reject those actual historical faults. Passing static logic cannot establish analog comparator thresholds or physical reset timing. Native KiCad/pcbnew10.0.6 and ngspice were used; no result is a hardware measurement.

## Readiness constraints and next steps

Before any **bare-board** order:

1. Independent reviewer inspects native E2 CAD, manufacturer pin/face evidence, filled copper, drill/assembly layers and exact E1/E2 change report. In particular confirm ST illustrated face toward PCB+Y and TI TL431DBZ1K2REF3A.
2. Confirm fabricator capability/quote:210×160mm outline,2layerFR4/1.6mm/35µm,0.15mm rules,0.30mm plated vias,0.075mm mask web and **J1011.20±0.05mm/J5020.95±0.05mm/Q402–Q4031.30±0.05mm finished holes**. Nominal profile vs Gerber stroke bounds and unspecified finish require ordinary CAM clarification, not fabrication guesswork. If tolerances cannot be met, a local landing correction is needed before ordering.
3. Confirm source/package readiness for critical components and mechanical fit: exact ST BD140/TI suffixes, IRF610-specific incoming lead/body envelope, custom cores, capacitor ESR/pulse resistor evidence, mating harnesses and insulated thermal hardware. No blanket “in stock” claim is made. Dry-fit/lot inspection remains Stage0.
4. Review bounded fixture and staged procedure. U401/Q402 stay absent until input/driver/reset gates pass. No unrestricted pack-based fault injection. Explicit user authorization is required before a purchase or manufacturer file transfer.

Bare-board estimate remains **€45–90 net for five**, freight€10–25, **unquoted**. Full components quantity1 **€32.317**; quantity10 **€27.311**. Fox-only quantity1 **€13.759**; quantity10 **€10.815**. No component cost delta from E1; exact fabrication tolerance/finish cost and current stock remain pending. One full-board experiment plus five bare boards/PCB freight is an allowance **€87.32–147.32 net**, excluding fixtures/labor/tax/component freight. No claim that the large evaluation board is a cost-optimized field product.

After separate authorization, the next engineering activity is staged qualification: unpowered pin/fit checks;3.3V logic/reset race tests; bounded input/buck/dummy-load tests; **driver-absent fault injection demonstrating≤20µs isolation and VDRV≤12.6V**; then driver/shaper and limited RF/thermal tests. The TVS is not an18/20V clamp and the100µs counterexample is a real model warning. BD140 hot SOA, actual current limits, clean keying/harmonics,3W/1.2W/Sprint output, Fox10mW and RF-port isolation/compact-antenna field criteria remain OPEN. **Bare-PCB manufacturing readiness is not assembled-transmitter safety or competition compliance.**
