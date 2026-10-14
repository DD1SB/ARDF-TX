# M3A — itemized 80 m material review

Date: **2026-10-14**. **Candidate BOM for review, not a released ordering list.** Costs are EUR **net**. German 19% VAT is illustrated separately; invoice treatment depends on the purchaser. No parts ordered or PCB fabrication quoted.

The [component workbook](M3_80M_COMPONENT_WORKBOOK.md), [per-reference CSV](M3_80M_BOM.csv), [cost JSON](M3_80M_COSTS.json) and [electrical manifest](../hardware/80m/RF80.electrical.json) enumerate every fitted part. They identify MPN, footprint, supplier identifier or **OPEN**, population, required/purchased quantities, MOQ, price break, stock limitation and evidence class. Identical MPNs are pooled within each population and batch; different values are not pooled. Cut tape/bulk MOQ 1 is an **assumption** for unquoted positions. Factory reel quantities are not customer MOQs.

## Component totals

| Scope, EUR per board | Quantity 6 | Quantity 10 | Quantity 20 |
| --- | ---: | ---: | ---: |
| Full module: source, both RF paths, supply, protection, interlocks and PCB connectors | 28.54 | 25.35 | 25.14 |
| Fox-only population; normal path DNP and TH301 replaced by R336 | 11.61 | 10.55 | 10.53 |
| Final transistor alone — not a transmitter | 1.11 | 0.62 | 0.62 |
| RF power stage: final, gate links/bleed and transformer | 2.18 | 1.61 | 1.61 |
| Normal stage with driver, shaper, filter, supply, input barrier and output connector | 16.12 | 14.16 | 14.03 |

The partial RF scopes exclude shared synthesis, common interlocks and other module protection. They are not standalone transmitter prices. Fox-only uses the same RF PCB and ESP32-S3 controller, with no additional primary PCB or MCU.

At ten, the full module contains **€9.75 of observed-price positions and €15.60 of estimates**. Mixed-price positions are conservatively classified as estimates. Observations retain original dates and locale/cache limitations; they are not a current reserved basket.

## Where the €20 target is exceeded

The full module misses the target by **€5.35 per board at ten**. Generated categories make the overrun explicit:

| Full module category, quantity ten | EUR/unit | Function |
| --- | ---: | --- |
| Source and crystal | 1.79 | Local programmable frequency; no duplicate MCU/RTC |
| Normal driver and support | 2.12 | LM5134B and independent inhibit |
| Normal final | 0.62 | IRF610 |
| Normal drain shaper | 1.02 | BD140, integration capacitor and key drive |
| Normal transformer/filter | 3.51 | Defined windings and original elliptic LPF |
| Buck, isolation and selection | 3.96 | One 4S buck, disconnect and supply settings |
| Input reservoirs | 0.90 | Rated input capacitors; effective capacitance unqualified |
| Independent Fox circuit | 2.86 | Buffer, shaped rail, separate filter/pad and port |
| Lease, rearm, mode logic and shared key-tail | 2.60 | Hang/retune/conflict/startup fail-off |
| Analog/input protection | 3.53 | Fuse/reverse barrier, UV/OV/OC and thermal window |
| Decoupling | 0.56 | Local supply bypass |
| PCB connectors | 1.88 | Controller, pack and dissimilar RF ports |

Rounded categories sum to the unrounded €25.346 total within rounding. Incremental NORMAL population is **€14.78** at ten, excluding shared circuits. A further €5.35 saving is not demonstrated without changing functions or closing cheaper sourcing. Magnetics, passives, connectors and ancillary mechanics remain the largest pricing uncertainties.

Savings implemented: one buck replaces boost plus adjustable LTC3600; ST BD140 saves €0.456 versus MPS751 at ten with better thermal documentation; fixed feedback/pad values replace DACs and trimmers; a €1 **estimated** screw terminal replaces an observed €5.09 SMA. No local MCU, RTC, EEPROM, display, bus isolator, precision power loop or permanent RF meter. The shared key-tail uses spare gates and about €0.36 in parts at ten, preventing identified startup pulses on both paths and preserving graceful CW decay. Two €0.10 estimated timing-node diodes implement the HC123 manufacturer power-down protection; omitting them risks discharge damage during rapid supply collapse.

## Supply evidence and procurement gates

| Part / supplier identifier | Price and availability evidence | Before ordering |
| --- | --- | --- |
| SI5351A-B-GT; DigiKey 336-2399-5-ND | M2 €1.87/€1.388 at 1/10; indexed stock 10,254 | Current basket, blank factory variant and MSOP pin/footprint |
| LM5134BMF/NOPB; Mouser 595-LM5134BMF/NOPB | TI Active; retained €2.17/€1.62 at 1/10. EU index 231 conflicts with US 510 and German incoming 30 November 2026. Cut tape MOQ 1. | **Local stock unresolved.** Do not substitute A thresholds; review alternate B packaging. |
| IRF610PBF-BE3; Farnell 4853567 | €1.11/€0.622 at 1/10; German indexed stock 614; ordinary PBF elsewhere out of stock | Exact lot/PCN and current stock; no broker strategy |
| ST BD140; Mouser 511-BD140 | Active; indexed stock 5,060; €0.585/€0.264 at 1/10 | ST pin map and hot repetitive SOA; another manufacturer's pinout cannot be inferred |
| TPS54302DDCT; Mouser 595-TPS54302DDCT | €1.59/€1.18 at 1/10; new EUR listing 3,137, direct fetch failed | Current cut-tape basket; cheaper OOS DDCR price not used |
| SRP7050TA-100M; Mouser 652-SRP7050TA-100M | Indexed €0.963/€0.792 at 1/10; exact stock count OPEN | Land pattern reviewed; hot saturation/current-limit qualification remains |
| DMN2056U-7; Mouser 621-DMN2056U-7 | Stock 95,248 indexed; €0.335/€0.147/€0.128 at 1/10/100; MOQ 1 | Guaranteed 2.5 V drive; 1G/2S/3D physical map. Native 2N7002 drawing is not the ordered device. |
| INA180A1IDBVT; Mouser 595-INA180A1IDBVT | Stock 2,890 at Mouser and 1,082–2,990 at DigiKey; €0.96 single observed, €0.70 at ten **estimated** | Correct A1/DBV map and price; OOS R-package price not used |
| SN74AC00DR; Mouser 595-SN74AC00DR | Active DR cut tape; stock 2,369 indexed; €0.404/€0.278/€0.248 at 1/10/25 | Loaded 10 mW/current/shaping evidence. EOL D-tube SKU not substituted. |
| Nexperia HC logic; exact codes in workbook | M2 observations retained. HC14 new index 862,904, €0.118 at ten; HC21 €0.166 with stock 18,895 in another locale | Local baskets. LS-derived drawings represent actual **HC** parts/thresholds/pins. HC21 NC pads 3/11 documented. |
| ABM3B-25.000MHZ-10-1-U-T; Mouser 815-ABM3B-25-T / DigiKey 300-8218-1-ND | Active; indexed stock 2,381; €0.40 **estimated** | CL, aging/temperature, pad map and calibration |
| FT-50A-43 / T60-2 plus wire | Manufacturer/supplier routes established; EUR quote OPEN | €0.95/€0.85 core/wire estimates **exclude winding labor**. Core identity mandatory. |
| 78F2R7J-RC | Manufacturer specs and distributor listings found; exact distributor SKU/stock OPEN | €0.30 **estimate**, 3.55 MHz loss measurement; no factory-bag MOQ assumption |
| Capacitors, reference/TVS/fuse/NTC, connectors/mates | Candidate MPN/package specified; many supplier codes, prices and stocks **OPEN** | Exact suffixes, ratings/effective capacitance, geometry and quotations |

The [dated source log](M3_80M_SOURCES.md) and workbook link the sources. Failed retrievals and conflicting stock remain explicit. **Not every BOM line is currently basket-verified.**

## Supporting circuitry and deletion assessment

| Circuit | Requirement and controller overlap | Disposition / failure consequence |
| --- | --- | --- |
| Source and local POR | Controller owns timing/RTC; local POR covers module startup/unplug | Retain RF source/POR, no duplicate schedule processor |
| Progress lease, rearm and gates | Controller watchdog cannot guarantee shutdown when GPIO stays high | Retain. Removal permits stuck-key or automatic restart. |
| Mode latch and shared key-tail | Live GPIO glitches must not raise the supply; integration capacitors can create startup drain/rail pulses | Retain fixed mode latch and key-qualified mute using spare gates. Tail prevents clipping normal CW decay. |
| UV/OV/OC and disconnect | Pack ID does not verify supply; buck EN cannot interrupt a shorted converter | Retain independent trips/switch, one sensor and no ADC |
| Thermal window | Polling/detached sensors cannot ensure hot-PA protection | Retain hot/open/short detection; attachment ancillary OPEN. Fox substitutes a fixed resistor only when watt stage DNP. |
| Fox level shifts, ballast and pad | Rail backfeed, output sharing and shaper shorts | Retain bounded source and independent key/permission mute. Pad removal invalidates fault budget. |
| RF detector | Previously proposed output telemetry/protection | Omitted **conditionally**: bounded source, fixed pad, separate port and mute. External calibration, fault energy and layout isolation tests mandatory. |
| I²C isolator | Former allowance concerned switched logic domains | Omitted: source/control share powered 3.3 V. Driving unpowered bus lines is forbidden/tested; otherwise backfeed invalidates fail-off. |
| MCU/RTC/DAC/EEPROM/op-amp meter | Duplicates central configuration/external calibration | Omitted; fixed settings require calibration, no automatic RF normalization claimed |

These are implementation proposals with failure assessments, not silent ADR changes. See [ADR-0012](decisions/ADR-0012-m3a-hf-electrical-implementation.md).

## External materials and complete-unit reconciliation

Outside component totals: bare RF PCB **€3 + €0.25 area provision**, MOQ/order multiple five for planning (six usable boards require ten fabricated boards, €5 plus area provision per usable board), no quote; heat sink, insulation and NTC attachment **€2 estimated**; long matching/radiator/return **€10.25 plus €3 supports**; compact matching/radiator/return **€8.38**. Exact mechanical parts and tuned antenna recipes remain OPEN. Batteries/controller/enclosure/charging retain the [M2 power baseline](M2_BATTERY_COST_COMPARISON.md). Labor, instruments and one-time engineering are separate.

The quantity-ten Fox audit **€29.06 core/compact antenna, €55.24 materials, €63.34 with fleet allocation** remains intact. Later dual-voltage-controller M2 materials are €57.83. The old €77.11 estimate is not reintroduced.

For the **replacement-budget bridge**, replace M2 Fox RF €8.50 by M3 €10.552; remove external low-output PCB socket €0.40 and RF power-connector half €0.60, now on this board; add €0.30 for the 16-contact mating-harness upgrade. At ten:

`57.83 − 8.50 + 10.552 − 0.40 − 0.60 + 0.30 = €59.182 materials`.

| Fox-only complete-device planning scope | Quantity 6 | Quantity 10 | Quantity 20 |
| --- | ---: | ---: | ---: |
| Materials: S3/RTC, RF, compact antenna/matcher, protected 2S1P, case/hardware, harness and two bare PCBs | 65.97 | 59.18 | 59.22 |
| Shared charging/provisioning/freight allocation | 13.50 | 8.10 | 4.85 |
| Materials plus fleet allocation | 79.47 | 67.28 | 64.07 |

These use unrounded RF figures and retained M2 batch baselines; the small 10-to-20 increase follows retained scope/batch prices, not a new price curve. They are **planning budgets**, not newly pooled complete-system quotations. Matching is counted once; mates/harness remain outside the component-only total.

For the 3 W normal unit with 4S1P 25R and both antenna accessories, replace the old €20.32 RF board in M2's €96.74 quantity-ten 3 W materials baseline; remove old sockets/power half; add €2 thermal provision and €0.50 harness upgrade:

`96.74 − 20.32 + 25.346 − 0.70 − 0.40 − 0.60 + 2.00 + 0.50 = €102.566`.

| Normal complete-device planning scope | Quantity 6 | Quantity 10 | Quantity 20 |
| --- | ---: | ---: | ---: |
| Materials, 4S1P 25R and both antenna accessories | 110.73 | 102.57 | 101.87 |
| Shared 4S charging/provisioning/freight | 14.33 | 8.60 | 5.35 |
| Materials plus fleet allocation | 125.06 | 111.17 | 107.22 |

Long-only installation subtracts the **same €8.38 compact accessory**, retaining the independent Fox board circuit. Calibration spares, winding/assembly/calibration labor, instruments and engineering remain separate. Physical tests may require revised materials; no fictitious cost reserve is added.

Illustrative 19% VAT at ten: full board **€30.16 gross**, Fox-only board **€12.56 gross**, Fox complete materials **€70.43 gross**. This does not constitute a quotation. Purchasing/fabrication requires subsequent authorization.
