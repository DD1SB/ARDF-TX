# M1 candidate BOM and sourcing — revised

Date: **2026-10-13**. **Candidate material BOM; not an ordering list. Complete layout/procurement not released.** The [cost rework](M1_COST_REWORK.md) supersedes the [pre-rework ledger](M1_BOM_PRE_REWORK.md), which is retained only as historical evidence.

The full [itemized workbook](M1_COSTED_BOM.md) gives function, count per board, required quantities for 6/10/20, manufacturer/order code where verified, package, availability, evidence label, unit price and extended line price. The [counts CSV](M1_COST_BOM.csv), [source catalog](M1_COST_PARTS.json) and [calculated baskets](M1_COST_TOTALS.json) are machine-readable. OPEN values/order codes are explicitly unresolved, never invented prices or approval to buy.

The architecture is now conditionally accepted. [M2 preparation](M2_PREPARATION.md) governs the next stage; [all-in material costs](M2_SYSTEM_COST.md) add circuit/thermal changes. BFP650 comparisons remain historical and are excluded from current selection.

## Preserved M1 nominal costs

EUR/unit ex VAT, selected distributor cut tape/tube prices plus unquoted material estimates. Bare PCB fabrication, assembly/test labor, batteries, outer enclosure, antennas and wiring are excluded from these PCB targets. Local RF shields/heat spreaders and logic board sockets are included. Soldered RF pigtails/bulkhead sockets are costed separately as mandatory wiring.

| Candidate | Six | Ten | Twenty |
| --- | ---: | ---: | ---: |
| Controller without LoRa | 15.01 | 12.88 | 12.82 |
| Complete 80 m RF | 20.13 | 17.88 | 17.80 |
| Complete 2 m RF, MMIC driver | 36.38 | 31.80 | 31.73 |
| Complete 2 m RF, stocked EOL discrete driver | 33.90 | 29.32 | 29.18 |
| Combined three-PCB basket, MMIC driver | **69.54** | **62.33** | **61.90** |
| Combined three-PCB basket, EOL driver | 67.07 | 59.86 | 59.36 |
| Combined electronics plus required power/port sockets, MMIC driver | 74.74 | 67.53 | 67.10 |

All four user targets are not established together: VHF's €30 ceiling is missed with the presently sourced MMIC driver; the cheaper discrete candidate depends on discontinued stock and unverified RF drive. Quantity-six cost misses the combined ceiling. Ten/twenty nominal combined PCB material fits €65, but €26.02/unit at ten is unquoted. Estimate-only −25%/+50% sensitivity is **€55.83–75.34**, not a promised range or confidence interval.

## Essential functions included

Controller: ESP32-S3 module, compensated RV3032 RTC, TPS62160 buck/inductor/capacitors, reverse/backfeed protection, raw-input TVS, branch fuses, voltage sensing, POR/comparator, protected interface sockets and local button/LED. Native USB/service pads avoid a UART bridge. Firmware implementation is outside M1.

HF: local Si5351/reference, source-bus isolation, discrete IRF610 and gate driver, adequate boost with actual isolation devices, key shaping, rated LPF, independent bounded Foxoring buffer/pad/filter, analog sensing/trips, monostable/latch/POR/gates, protected returns and local shield/thermal material. VHF: local source/reference, genuine priced PD55008, driver, boost and true isolation, sine series AM hardware, input/output filtering, independent AM training branch/pads/filter, analog sensing/trips and the same hardware fail-off functions. Values/counts remain architectural candidates.

USB socket, RTC backup capacitor, pack-current shunt and RF EEPROMs are optional rows, totaling approximately €1.65/unit for the enhanced combined population. Omitting the pack-current shunt does not omit RF-local current cutoffs or current/endurance qualification. Omitting RTC backup requires resync after a cold pack swap. LoRa remains separately optional with exact Silicontra MPN/price OPEN. No display/GNSS/DAC/precision SWR meter is required in the base.

## Required off-board accessories

| Assembly / itemized scope | Nominal estimated EUR | Sourcing/qualification status |
| --- | ---: | --- |
| Long-wire 80 m system: loading/tuner coil, RF trimmer/fixed capacitors, tuning detector, RF mating connector, insulation/strain relief, longer radiator and symmetric counterpoise/radials | **10.25** | All material estimates; winding/capacitor voltage/Q/SRF and actual radial lengths open. Support pole extra. |
| Compact Foxoring: separate loading/coupling coil, RF trimmer/fixed capacitors, pad/damping, low-cap protection, keyed plug/identity, insulation/strain relief, approximately 30 cm radiator and compact counterpoise | **8.38** | Full functional material scope included, not a validated 10 mW/field-range recipe. |
| Required battery/module-power/RF port sockets for universal unit | **5.20** | Counted in separate wiring basket. Actual harness/cable/crimps/strain relief additional €2–5 estimate. |
| VHF horizontal competition antenna/feed/balun | **10–20** | Prior unquoted allowance retained; measured ERP gain/pattern and 2–3 m installation required. |
| VHF antenna support / training antenna | **5–15 / 2–5** | Separate unquoted mechanical/training scopes. |
| Shared controller/RF provisioning fixture | **3–6 once per fleet** | Estimated; avoids per-board USB-UART/programmer premium. Lab instruments/calibration labor separate. |

Fox-only RF population is **€8.82 / 7.92 / 7.86**. Controller plus that RF board and the **complete compact antenna** is **€31.94 / 29.06 / 29.02**, before the transmitter-side battery socket, detachable module-power pair and compact-port socket/wiring, external pack and outer enclosure. Full HF board costs roughly €10 more at ten. This still uses the same two-board modular architecture, short radiator, defined counterpoise and loading network.

## Procurement limitations and repeatability

The catalog distinguishes observed small-quantity prices from estimates. Cached stock is not a reservation. RF values, winding recipes, connector order codes and many supporting quotes remain OPEN because no electrical design has been performed. Estimated MOQ 1 and flat estimated prices are clearly marked. Manufacturer package drawings, pinout and land pattern must be checked before any footprint selection.

Critical gates: IRF610/driver/POR current stock/order codes; HC123 stock conflicts; PD55008TR-E stock 24 vs151 (Mouser tube variant1332 is an independent offer, not the same packaging order); GVA-84 pricing €2.57 versus earlier €4.88; actual inductor/MLCC/shield/connector costs. EOL BFP650 is a separately costed finite-stock experiment, not an active-production fleet selection. Its manufacturer status and 15 May 2027 distributor LTB are explicit.

The RNWR boost is genuinely offered cut tape at MOQ 1 despite factory reel 3000, so no reel savings are assumed. Available PD55008S-E MOQ 400, out-of-stock/reel-only parts, obsolete Central 2N3866 and unavailable old NXP/BFR93AW offers do not enter the baseline. All substitutions require source/spec/package/RF verification, not matching a generic transistor name.

The [source supplement](M1_COST_SOURCES.md) records inspected primary documentation and blocked/unobtained sources. Source/licence boundaries in the original research register still apply.
