# M3A-R1 — itemized 80 m material review

**Historical M3A-R1 record.** M3B now has an evaluation PCB; current CAD/cost/checks are in [M3B review](M3B_REVIEW_DECISION.md). R1 artifacts are preserved in commit`0dfd224` and the [R1 snapshot](../hardware/80m/review/M3A-R1/). The commands/counts/scope below apply to that revision.


Date: **2026-10-14**. **Candidate BOM; no ordering or fabrication.** EUR **net**, VAT/labor/tooling separate. [Workbook](M3_80M_COMPONENT_WORKBOOK.md), [CSV](M3_80M_BOM.csv), [cost JSON](M3_80M_COSTS.json) and [electrical manifest](../hardware/80m/RF80.electrical.json) remain the single component ledger. MPN, footprint, population, supplier ID or OPEN, MOQ, pooled quantities, price breaks and evidence are explicit. Unquoted cut-tape/bulk MOQ1 remains an assumption; factory reel quantities are not customer MOQs. R0 is preserved at `m3a-r0`.

## Current component totals

| Scope, net EUR/board |6|10|20|
| --- | ---: | ---: | ---: |
| Full module components | 31.18 | 26.60 | 26.60 |
| Foxoring-only components | 12.01 | 10.80 | 10.46 |
| RF final transistor alone | 1.11 | 0.62 | 0.62 |
| RF power stage: final + gate links/bleed + transformer | 2.18 | 1.61 | 1.61 |
| Normal stage + drive/shaper/filter/supply/input and output hardware | 17.75 | 15.07 | 15.04 |
| Incremental NORMAL population; shared circuits excluded | 19.43 | 16.41 | 16.39 |

At ten, full cost is **€26.60**, **€9.37 observed /€17.23 estimates**. Mixed prices are conservatively estimated. The €20 target is exceeded by **€6.60**. Full fit: **193 purchased parts/18 ICs**; Fox: **115/13**. Pads/flags are excluded from purchases. Full increases €1.25, Fox €0.25 versus R0 at ten; no saving is claimed from assumed assembly reductions.

## Cost by block, quantity ten

| Group | EUR/full board |
| --- | ---: |
| connectors | 1.875 |
| decoupling | 0.510 |
| fox | 2.775 |
| interlocks | 3.243 |
| normal_driver | 3.051 |
| normal_filter | 3.510 |
| normal_final | 0.622 |
| normal_shaper | 1.021 |
| normal_supply | 3.786 |
| protection | 3.519 |
| source | 1.788 |
| supply | 0.900 |

The partial PA scopes exclude synthesis/common logic/other module protections. A €0.62 transistor is not a transmitter. Watt-only parts DNP in Fox, including U312/reference/thermal branches. [R1 delta](M3A_R1_COST_DELTA.md) lists every removed/introduced/modified reference and full/Fox 6/10/20 evidence splits. [Simplification](M3A_R1_SIMPLIFICATION.md) states failure consequences; filters and independent fail-off are retained.

## Supply evidence and procurement gates

| Part / supplier identifier | Price and availability evidence | Before ordering |
| --- | --- | --- |
| SI5351A-B-GT; DigiKey 336-2399-5-ND | M2 €1.87/€1.388 at 1/10; indexed stock 10,254 | Current basket, blank factory variant and MSOP pin/footprint |
| LM5134BMF/NOPB; Mouser 595-LM5134BMF/NOPB | TI Active; retained €2.17/€1.62 at 1/10. EU index 231 conflicts with US 510 and German incoming 30 November 2026. Cut tape MOQ 1. | **Local stock unresolved.** Do not substitute A thresholds; review alternate B packaging. |
| IRF610PBF-BE3; Farnell 4853567 | €1.11/€0.622 at 1/10; German indexed stock 614; ordinary PBF elsewhere out of stock | Exact lot/PCN and current stock; no broker strategy |
| ST BD140; Mouser 511-BD140 | Active; indexed stock 5,060; €0.585/€0.264 at 1/10 | ST pin map and hot repetitive SOA; another manufacturer's pinout cannot be inferred |
| TPS54302DDCT; Mouser 595-TPS54302DDCT | €1.59/€1.18 at 1/10; new EUR listing 3,137, direct fetch failed | Current cut-tape basket; cheaper OOS DDCR price not used |
| SRP7050TA-100M; Mouser 652-SRP7050TA-100M | Indexed €0.963/€0.792 at 1/10; exact stock count OPEN | Land pattern reviewed; hot saturation/current-limit qualification remains |
| Q404 only: DMN2056U-7; Mouser 621-DMN2056U-7 | Stock 95,248 indexed; €0.335/€0.147/€0.128 at 1/10/100; MOQ 1 | Guaranteed 2.5 V drive; 1G/2S/3D physical map. Native 2N7002 drawing is not the ordered device. |
| INA180A1IDBVT; Mouser 595-INA180A1IDBVT | Stock 2,890 at Mouser and 1,082–2,990 at DigiKey; €0.96 single observed, €0.70 at ten **estimated** | Correct A1/DBV map and price; OOS R-package price not used |
| SN74AC00DR; Mouser 595-SN74AC00DR | Active DR cut tape; stock 2,369 indexed; €0.404/€0.278/€0.248 at 1/10/25 | Loaded 10 mW/current/shaping evidence. EOL D-tube SKU not substituted. |
| Nexperia HC logic; exact codes in workbook | M2 observations retained. HC14 new index 862,904, €0.118 at ten; HC21 €0.166 with stock 18,895 in another locale | Local baskets. LS-derived drawings represent actual **HC** parts/thresholds/pins. HC21 NC pads 3/11 documented. |
| ABM3B-25.000MHZ-10-1-U-T; Mouser 815-ABM3B-25-T / DigiKey 300-8218-1-ND | Active; indexed stock 2,381; €0.40 **estimated** | CL, aging/temperature, pad map and calibration |
| FT-50A-43 / T60-2 plus wire | Manufacturer/supplier routes established; EUR quote OPEN | €0.95/€0.85 core/wire estimates **exclude winding labor**. Core identity mandatory. |
| 78F2R7J-RC | Manufacturer specs and distributor listings found; exact distributor SKU/stock OPEN | €0.30 **estimate**, 3.55 MHz loss measurement; no factory-bag MOQ assumption |
| Capacitors, reference/TVS/fuse/NTC, connectors/mates | Candidate MPN/package specified; many supplier codes, prices and stocks **OPEN** | Exact suffixes, ratings/effective capacitance, geometry and quotations |

The [dated source log](M3_80M_SOURCES.md) and workbook link the sources. Failed retrievals and conflicting stock remain explicit. **Not every BOM line is currently basket-verified.**

## R1 selected supporting parts

| Part / supplier | Evidence | Gate |
| --- | --- | --- |
| BSS138BK,215; Mouser771-BSS138BK215 | Manufacturer current data, ±20 V gate, 2.5 V RDS(on); indexed ten-price€0.099, single/hundred prices estimated | Local quantity/stock quotation and transient gates; applies to low-current sinks only |
| 74HC174D,653; exact supplier SKU OPEN | Nexperia Production;€0.35/€0.25 at1/10 **estimated** | Five captured context bits; exact cut tape basket required; no Toshiba NRND substitution |
| 25SVPF47M; DigiKeyP16513CT-ND | DE index48,247/Active, net€1.50/€0.973 at1/10; direct fetch failed | Native CP_Elec_6.3x5.9 verified against maker C6 lands; physical ESR/transient isolation gate |
| CRCW25124R70FKEG R410; exact supplier basket OPEN | 4.7 Ω/1 W2512,€0.10 **estimated** | Hot pulse derating/energy and correct part suffix must qualify |

## External materials and complete-unit bridge

Bare PCB fabrication, battery/BMS, harness/mates, antenna/matching, enclosure, thermal/mechanical hardware and shared charging remain outside component totals. Retained estimates: RF bare PCB€3 +€0.25 area provision (six usable boards need ten at planning order multiple5), thermal provision€2, long matcher/wire/return€10.25 plus€3 supports, compact30 cm matcher/radiator/return€8.38. These are allowances, not new quotes; winding/calibration/assembly labor, instruments and engineering separate.

Historical quantity-ten Fox audit **€29.06 core+compact antenna /€55.24 materials /€63.34 with fleet** remains unchanged. Replace M2 RF€8.50 with current RF€10.804; remove PCB socket€0.40 and power-connector half€0.60 already included here; add€0.30 mating-harness upgrade:

`57.83 − 8.50 + 10.804 − 0.40 − 0.60 + 0.30 = €59.434 net materials`.

| Complete Fox scope |6|10|20|
| --- | ---: | ---: | ---: |
| Materials: S3/RTC, RF, compact matcher/antenna, protected2S1P, case, hardware, harness, two bare PCBs | 66.38 | 59.43 | 59.15 |
| Shared charging/provisioning/freight | 13.50 | 8.10 | 4.85 |
| Materials plus shared fleet | 79.88 | 67.53 | 64.00 |

The normal complete-unit bridge retains the R0 scopes (4S1P25R, both antenna accessories, case/harness/thermal parts) and changes only RF components. At ten: `102.566 + (26.600 − 25.346) = €103.820 materials`, plus unchanged€8.60 shared infrastructure =€112.420. Approximate net material at6/20 is€113.37/€103.33 using rounded R0 bridge totals plus actual RF delta. Long-only subtracts the same€8.38 compact accessory; no new full-system quote or procurement is implied.

Illustrative German19% VAT at ten: full RF components€31.65 gross, Fox components€12.86, complete Fox materials€70.73. Actual VAT treatment depends on purchaser/invoice. Current low-ESR capacitor and context/withdrawal protection drive the increase; hundred-piece MOSFET discount remains an estimate, not secured savings.
