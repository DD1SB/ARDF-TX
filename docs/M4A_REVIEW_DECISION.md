# M4A — prototype transition and compact-board review decision

Date: **2026-10-15**. **GO for review of the frozen E2 prototype handoff and the compact V1 engineering candidate. Conditional GO for five bare E2 boards after supplier confirmations, a quote and explicit user authorization. NO-GO for V1 manufacture or production release until the reference hardware is qualified and resulting corrections are incorporated.** No purchase, manufacturer upload, fabrication, population, power-up or RF activation occurred.

The authoritative evaluation reference remains **1245023 / m3b-e2**, unchanged byte-for-byte, including its native CAD and exports. The new [supplier-neutral handoff](M4A_E2_PROTOTYPE_HANDOFF.md) contains the exact Git archive, all original review files, manufacturing/finished-hole requirements, checksums, critical procurement candidates and staged assembly allocations. Intended scope is **five bare boards, one initially populated in stages**. The user's prior independent E2 review is preserved; this milestone does not claim another independent engineering approval or a physical test.

## Delivered compact candidate

[RF80_V1.kicad_pro](../hardware/80m/production/RF80_V1.kicad_pro), [editable PCB](../hardware/80m/production/RF80_V1.kicad_pcb), [schematic PDF](../hardware/80m/production/review/M4A-V1/RF80_V1.pdf) and [complete review package](../hardware/80m/production/review/M4A-V1/README.md) are explicitly **PRODUCTION-INTENT — NOT RELEASED**.

- **150 × 110 mm**, two layers, versus 210 × 160 mm E2: **50.9% less board area**. Four M3 mounting holes use a proposed 140 × 100 mm pattern. Final enclosure/controller alignment, heatsink and cable envelopes remain adjustable assumptions.
- Same Si5351–LM5134B–IRF610, BD140 shaping, bifilar transformer, elliptic filter, independent SN74AC00 Fox path and hardware interlocks. No electrical values, purchased components or functional connections changed. Controller and 2 m true AM hardware are untouched.
- **14 of 74 test pads retained**; all 74 classified. RF calibration uses the existing independent ports. Full/Fox purchased populations remain **196/115**, with **18/13 ICs**; the three Fox-only links and normal-path DNP contract are explicit.
- Critical ST BD140 **1B/2C/3E** and TI TL431 DBZ **1K/2REF/3A** mappings are preserved in symbols, actual native pads, copper Gerber flashes and IPC output.

## Actual verification

| Check | Result and limit |
| --- | --- |
| KiCad 10.0.6 ERC | **0 violations**; three inherited informational defaults are disclosed: single global label, four-way junction, absent SPICE model |
| All-severity, all-track-error DRC | **0 violations / 0 unrouted / 0 schematic-parity issues**; all 62 configured DRC categories enabled, no exclusions or ignored DRC checks |
| Electrical equivalence | Every non-TP component/value/population/net matches E2; **604 native pad memberships**, 217 footprints including four mounts |
| Manufacturer checks / mutations | **55 critical devices**, **12 accidental-regression mutations rejected**, including an actual in-memory Q403 PCB-net mutation |
| R1 logic on V1's exported netlist | **256 combinations / 31 state scenarios / 16 timing corners**, including polarity mutations and deliberate rearm; ideal logic/timing evidence only |
| Filled ground / model references | **One connected network across 41 filled polygon regions**, 112 ground vias; all 199 model references resolve. Resolved envelope models are not supplier or thermal qualification |
| Fabrication consistency | Nine fresh Gerber layers/job, separate **397 PTH / 4 NPTH** drills/maps, all **401 hole positions/sizes** checked against native CAD, max export quantization 0.0005 mm; 195 full / 115 Fox placement rows |
| Historical suites | R1 and E1 suites pass in temporary archived checkouts; those results are version-specific and do not reinstate E1's defective manufacturer mappings |
| Electrical protection, reset races, RF, thermal, antennas, endurance | **All NOT_RUN** |

The [equivalence report](M4A_ELECTRICAL_EQUIVALENCE.md) and package verification record distinguish static checks from physical qualification. No passing DRC or netlist comparison establishes RF, thermal or analog equivalence. Local routing corrections established ground stitching rather than suppressing isolated-region findings. No proposed ADR was silently accepted or amended; the circuit is unchanged.

## Cost and manufacturability

Net EUR per board, excluding VAT:

| Quantity | Full components | Fox components | Bare compact PCB base allowance |
| --- | ---: | ---: | ---: |
| 6 | 31.896 | 12.081 | 5.34–10.66 |
| 10 | 27.311 | 10.815 | 4.54–9.00 |
| 20 | 27.311 | 10.468 | 3.94–7.75 |

There is **no component saving versus E2**. The PCB numbers are unquoted setup/area assumptions, not supplier offers; mandatory tight-hole processing, freight, yield and tax remain **OPEN**. At quantity ten, the installed RF-module base allowance is **€56.40–70.06 full** including both antenna/matching accessories, or **€27.36–36.01 Fox-only**, before those open items and labor. Shared controller, battery, charging and enclosure costs remain separate. See the [itemized variant/installed-cost analysis](M4A_VARIANT_BOM.md).

The frozen E2 five-board allowance remains **€45–90 net**, PCB freight **€10–25** and one full component basket **€32.317**: **€87.32–147.32** before tolerance surcharges, component freight, fixtures, labor and tax. This is a planning allowance, not a confirmed cash ceiling. Exact LM5134B cut-tape stock/price, core supply, capacitor ESR, real mating parts and incoming lead fits still require confirmation.

## Required next steps

1. Review the compact placement, ground returns, RF paths, thermal/cable envelope and population drawings. Accept or revise the adjustable 150 × 110 mm mechanical interface; do not lock an unmeasured heatsink into an enclosure.
2. For **E2 bare manufacture**, obtain explicit supplier acceptance of finished-hole/mask/drill/finish requirements and a real five-board quote through an authorized communication step. Obtain explicit user purchasing/file-transfer authorization. No compact Gerber is part of that order.
3. Separately approve low-voltage procurement/population, high-energy population, controlled power-up and RF activation. Use current-limited laboratory supplies and staged fixtures; a bare-board approval grants none of those permissions.
4. Measure E2 input transients/TPS22810 margins, **≤20 µs isolation and VDRV≤12.6 V**, real ARM/reset/fault/rearm timing, BD140/IRF610 hot SOA, 3 W/1.2 W/Sprint output, CW/spectrum, independent 10 mW Fox power/isolation/compact-antenna field behavior and defined 12 h/24 h endurance. Keep U401/Q402 absent until the corresponding gates pass.
5. Incorporate any measured E2 electrical corrections into V1 through explicit change control. Independently review and qualify V1's altered parasitics, return paths, heating and near-field coupling; repeat driver-absent fault qualification before fitting its driver. Only after all user release gates and explicit approval can it become production hardware.

The next physical activity is controlled evaluation of E2, once authorized. M4A has produced a real compact candidate and a reproducible transition package; it has not bypassed the first hardware measurements.
