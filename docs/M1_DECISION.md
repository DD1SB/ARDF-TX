# M1 decision and review summary — cost rework

Date: **2026-10-13**. **M1 architecture conditionally accepted; complete layout/procurement remains gated by RF evaluation.** The rework is a reviewable M1 research package, not an approved electrical design or validated transmitter. No PCB design, routing, fabrication exports, purchases or firmware implementation occurred.

## Conditional review record

The user accepted the architecture and authorized circuit/evaluation preparation on 2026-10-13. [M2 preparation](M2_PREPARATION.md) now governs the next work. MMIC drive is preferred; BFP650 is excluded from selection. The [VHF review](M2_VHF_RF_REVIEW.md) exposes drive/thermal limits and uses a conservative 4P evaluation allowance. The [all-in cost view](M2_SYSTEM_COST.md) includes the necessary new circuit/thermal material. Cost/energy tables below preserve the M1 baseline, not a newly validated circuit.

## Recommended topology

Preserve the accepted three primary PCBs and optional LoRa. Propose one ESP32-S3 controller with compensated RTC, direct independent RF configuration buses and external test fixture; omit both RF processors, DACs and precision digital meters. Keep inexpensive local hardware lease, persistent latch/POR, analog current/thermal/rail trips, source-bus isolation and independent source/PA shutdown.

HF: compare ON7YD single-IRF610 shaped class-C reference with QCX class-E, use local Si5351 and adequately boosted supply, and retain a separate bounded 10 mW Foxoring source plus dedicated loading/coupling cartridge. VHF: evaluate local Si5351 first, filtered RF driver, priced PD55008 discrete final and real sine supply AM; compare ADF4002/discrete VCO if Si5351 fails spectra. LMX2571 is a higher-cost fallback. Normal and low-power ports remain physically distinct and interlocked. Reduced Fox-only population keeps the short radiator, compact counterpoise and matching network.

Primary rulebook verification remains in the [requirements trace](M1_REQUIREMENTS_TRACE.md). New primary evidence includes ON7YD instrument-attributed HF results, an actual six-unit DL3BBX-derived AM build, ST active PA availability and concrete cut-tape price alternatives. None validates the new programmable/2S/AM derivative. Exact CQ-DL original, full-band spectra, VHF envelope/drive, compact field recipe and many supporting component quotes remain unknown.

## Candidate materials for six, ten and twenty

EUR/unit ex VAT; observed distributor prices plus explicit estimates. Full [itemized BOM](M1_COSTED_BOM.md) gives part/order numbers where verified, counts, stock/MOQ and line prices. RF ports use soldered pigtails to keyed bulkhead sockets; required sockets/wiring are costed separately under the user's wiring exclusion. Local shields/thermal/protection and logic sockets are included. PCB fabrication, batteries, enclosure, antennas and assembly/test labor are excluded.

| Hardware configuration | Six | Ten | Twenty |
| --- | ---: | ---: | ---: |
| Controller without LoRa | 15.01 | 12.88 | 12.82 |
| Complete 80 m RF PCB | 20.13 | 17.88 | 17.80 |
| Complete 2 m AM/training PCB, MMIC driver | 36.38 | 31.80 | 31.73 |
| 2 m AM/training PCB, stocked EOL discrete driver | 33.90 | 29.32 | 29.18 |
| All three PCB materials, MMIC driver | **69.54** | **62.33** | **61.90** |
| All three PCBs plus required power/port sockets | 74.74 | 67.53 | 67.10 |
| Controller + full 80 m RF | 35.00 | 30.61 | 30.61 |
| Controller + 2 m RF | 51.18 | 44.53 | 44.53 |
| Controller + Fox-only RF + complete compact antenna | 31.94 | 29.06 | 29.02 |

The combined upper €65 PCB-material target is plausible at ten/twenty, **not proved**. VHF's individual €30 ceiling still misses by €1.80/€1.73; six-unit combined pricing misses by €4.54. A stocked discontinued BFP650 driver variant meets VHF's nominal ceiling at ten/twenty, but needs an explicit finite-batch/spares policy and RF qualification. No evidence supports the €33 combined floor with these requirements.

At ten, combined **€26.02** is unquoted estimated material; varying estimates −25%/+50% gives **€55.83–75.34**, with further RF redesign/stock/tax/shipping risks outside that sensitivity. Power/port sockets add €5.20 estimate; cable/contacts/strain relief add €2–5 estimate. The six optional population rows add approximately €1.65/unit. Complete long-wire accessory estimate €10.25; compact accessory €8.38; both require sourced parts/qualified winding and field recipes. VHF antenna/feed allowance €10–20 plus support remains unquoted. No accessory safety/matching function has been silently omitted.

Modified UV-5R conversion comparator is approximately **€51–64** materials using the revised controller, observed retail radio and estimated AM/safety/training additions, on a mixed retail-tax/ex-VAT basis. Its exact AM revision is unvalidated and it does not replace the three-PCB contract. Pack/LoRa exact suppliers remain open.

## Energy budget by pack and profile

The [revised power budget](M1_POWER_BUDGET.md) increases HF gate-drive and VHF buffer overhead; cheaper control earns no invented current savings. Reference 3.4 Ah cells, 64.8% usable nominal energy, all controller/RTC/regulator/RF standby loads and unmeasured efficiencies are included. Hours below are model results; bold values meet 24 h in this model only.

| Maximum setting/profile | 2S1P | 2S2P | 2S3P | 2S4P |
| --- | ---: | ---: | ---: | ---: |
| HF Classic 5 W,20% | 7.2 | 14.5 | 21.7 | **29.0** |
| Sprint 1 W,20% | **26.7** | **53.5** | **80.2** | **107.0** |
| Foxoring 10 mW continuous | **61.0** | **122.0** | **183.0** | **244.0** |
| VHF Classic 1 W carrier ERP,20% | 10.4 | 20.9 | **31.3** | **41.8** |
| HF 5 W continuous beacon | 1.5 | 3.0 | 4.6 | 6.1 |
| Sprint 1 W continuous beacon | 6.5 | 13.0 | 19.5 | **25.9** |
| VHF1 W carrier ERP continuous beacon | 2.2 | 4.5 | 6.7 | 9.0 |
| Training 1 mW continuous | **45.3** | **90.6** | **136.0** | **181.3** |
| Both Classic bands, each20% | 4.4 | 8.8 | 13.3 | 17.7 |

Required modeled normal packs remain **HF 4P, Sprint 1P, Foxoring 1P, VHF 3P**; 4P is maximum, not mandatory. Continuous LoRa RX adds 1.08 Wh/day, reducing Sprint 1P to about 24.9 h. MCU/current/efficiency measurements can invalidate that small margin. Peak design estimates with LoRa/transients are **HF 2.3 A, VHF 3.4 A, aligned dual 5.6 A**. Continuous full-power HF/VHF beacons and dual Classic do not meet 24 h within 4P.

## Unresolved gates and review decisions

The largest unresolved risks are all-channel Si5351 spurs, 144 MHz PA gain/drive and 70–80% AM/PEP/heat, 5 W HF drain stress/clicks/efficiency, low-port RF isolation, cheap-watchdog startup/timeout/latch recovery, and compact antenna/environment field reach. Support-part prices, stock conflicts and EOL policy prevent a released ordering BOM. Country/licence, legal spectrum mask, exact Silicontra module and referee power/audibility conventions remain open.

The existing [qualification plan](M1_VALIDATION_PLAN.md) retains separate HF long/compact matching tests, 50 Ω 10 mW calibration and 30 m audible/250 m not-audible trials; actual AM envelope/PEP/unwanted emissions; startup/fault/retune; timing/thermal/endurance; optional LoRa and RF/LoRa immunity. Documentation checks do not close these hardware gates.

Review decisions remaining after conditional acceptance:

1. ADR-0007 is conditionally accepted at architecture level. Review detailed [ADR-0008](decisions/ADR-0008-rf-evaluation-gates.md) and RF coupon/circuit choices; no complete layout is released.
2. Driver policy is settled: prefer MMIC and currently manufactured alternatives; do not select BFP650 for minor cost savings. Close measured drive/gain/compression before choosing the exact MMIC.
3. Agree ex-VAT/gross target basis and PCB-versus-wiring scope; accept the approximately €1.8 VHF-board overrun at ten or keep the cost gate open for further sourcing/topology evidence. The six-unit target remains unresolved.
4. Confirm operating country/licence, exact Silicontra variant, pack/cell/charger, referee ERP/reference-load/field protocol, desired continuous-beacon duration and whether simultaneous dual-band 24 h is required.
5. Circuit/evaluation preparation is now authorized. Subsequent coupon implementation/commitment requires its review; complete layout/procurement requires the defined measured RF gates. **Do not manufacture or order a full transmitter set.**

Check results and source access limits are documented in [M1 checks](M1_CHECKS.md) and the [dated cost source supplement](M1_COST_SOURCES.md).
