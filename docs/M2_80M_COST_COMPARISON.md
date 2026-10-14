# 80 m reference and derived-module cost comparison

Date: **2026-10-13**. **Candidate material analysis, not quotes for completed units or an ordering list.** EUR **ex VAT** for component planning. Labor, calibration, yield/spares, freight and instrument capital are separate. Retail/historical comparators have their own tax basis. [Itemized workbook](M2_80M_BOM.md), [quantity ledger](M2_80M_BOM.csv), [catalog/count inputs](M2_80M_INPUTS.json) and [exact arithmetic](M2_80M_TOTALS.json) make every allowance inspectable. Source counts/variants are in [the reference comparison](M2_80M_REFERENCE_COMPARISON.md).

## Scope-normalized results at 6, 10 and 20

| Basket, EUR/unit before bare PCB fabrication | 6 | 10 | 20 | What the total establishes |
| --- | ---: | ---: | ---: | --- |
| DF1FO MidiTX RF section | 6.17 | 5.83 | 5.79 | Native fixed-frequency antenna-tuned core; indicators included, variometer/accessory extra. Not complete ARDF-TX. |
| DF1FO MidiTX complete native material estimate | 18.17 | 17.76 | 17.73 | Original TTL-oscillator population, ATtiny/time base, indicator/variometer, case/controls/header/socket allowances. Cells and antenna wire excluded. Mostly unquoted. |
| DF1FO Sprint 50–80 mW RF section | 3.73 | 3.73 | 3.68 | Does not meet modern 0.3 W Sprint minimum. |
| DF1FO Sprint complete native material estimate | 12.10 | 12.10 | 12.05 | Controller/crystals/regulator/case included; 9 V cell/antenna wire excluded. Matching-value discrepancy unresolved. |
| ON7YD ATX80 original RF board | 6.01 | 5.52 | 5.52 | Includes IRF610,CD4001/crystal/trimmer/filter/heat sink, not contest controller, battery or external tuner. |
| FlexFox80 whole listed native PCB/component envelope | 87.27 | 83.99 | 83.84 | Whole MCU/RTC/Wi-Fi, original supplies, sockets and outer-case estimate. Optional populated functions are included; no external operating pack/antenna/shared configuration tools/fabrication/labor. **€72.70 of ten-unit total is estimated.** |
| SignalSlinger whole listed native PCB/component envelope | 50.80 | 49.06 | 49.06 | MCU/time base, supplies, optional regulator/fan switches/headers, backup cell/charger, case allowance included; external operating pack, antenna, shared cable/fabrication/labor excluded. **€43.35 at ten is estimated.** |
| FlexFox80 extracted RF source/driver/final/filter | 12.26 | 10.45 | 10.45 | 22 named source/driver/RF reference positions, excludes native adjustable PA power supply/MCU/RTC/Wi-Fi. Native source TCXO included; an adequately supplied reference core, not a complete safe module. |
| SignalSlinger extracted RF source/driver/final/filter | 12.24 | 10.42 | 10.42 | 24 named reference positions, source TCXO/driver-switch included, excludes external source of Vdrive and local controller. |
| FlexFox80 extracted core **plus native adjustable supply** | 32.55 | 28.98 | 28.98 | Adds actualLTC3600/OPA171/MIC2196/FET/magnetics/feedback/reservoir positions; no host/controller. This is the material complexity to avoid in the economy variant. |
| Existing ARDF-TX M1 full 80 m board, preserved | 20.13 | 17.88 | 17.80 | Earlier functional counts/prices, without subsequent circuit/thermal increments. |
| Existing ARDF-TX M2 full 80 m candidate, preserved | 25.95 | 23.33 | 23.25 | Added TC4427A, feedback shaper, extra filter/match/thermal/guard provisions; unmeasured. |
| **Proposed SignalSlinger core, 1.2 W/.85 W plus separate Fox** | **22.41** | **19.76** | **19.68** | Full candidate RF-board component/functions budget;RTC/MCU remain on existing controller. Includes low guard reserve, interlocks, filters and local heat/shield material. |
| Adapted DF1FO mechanism with the same protected programmable module scope | 21.91 | 19.68 | 19.61 | Adds 9 V boost, 5 V logic rail, modern 50Ω filter/matching allowance, source, shaped-level/safety and Fox branch. New 50Ω matching/level control unresolved; no 5 W growth on native final. |
| Higher-output shared IRF610 core with boost+variable buck | 35.48 | 30.86 | 30.79 | Same protected branches;LTC3600/OPA171/second conversion stage/extra thermal provision.2–3 W and 5 W use the same counted high-power population. |
| Proposed Fox-only reduced population | 9.40 | 8.50 | 8.44 | Includes **€0.75 guard completion reserve**. Compare old M1 Fox-only €7.92 plus guard 0.75, not 7.92 alone. |
| TinyFox native complete material allowance | 13.03 | 12.96 | 12.93 | Includes original MCU/AA boost/crystal/case/compact antenna/stake, excludes AA cell/fabrication; exact life cycle/stock unquoted. |
| Fixle native complete material allowance | 6.72 | 6.67 | 6.67 | Includes original MCU/crystal/BC846/coil/trimmer/case/wires/CR2032 allowance, excludes fabrication. A different platform/performance scope. |

These reference “complete” estimates are **reconstruction baskets with explicit unquoted positions**, not factory quotes or proof that every listing can be ordered today. Current KiCad inventory, old BOM and default kit populations differ. We price all listed physical PCB options in native envelope comparisons and list exclusions; solder bridges/test pads are not purchased parts. RF-only row boundaries enumerate exact designators in the workbook. Fabrication and native external matching remain separate below. Native functional group allocations are not evidence of national emissions compliance.

DF1FO's apparently much cheaper bare RF core loses most of its advantage when programmable synthesis, regulated depleted-battery performance, two antenna ports, 50Ω filtering, shaping and autonomous protection are restored. Its adapted allowance is only **€0.08 less at ten** than the preferred IRF610 core, smaller than quote/matching uncertainty. Published 50Ω programmable-core evidence, current driver support, explicit filter/winding recipe and higher-power reuse make SignalSlinger preferable. No EOL device is selected to achieve these totals.

## Essential categories and real cost drivers

| Preferred full module category at ten | EUR/unit | Basis |
| --- | ---: | --- |
| Si5351 + crystal | 1.79 | Source 1.388 observed; reference 0.40 estimate. |
| RF final + logic low-power buffer | 0.725 | IRF610: €0.622 observed; HC00: €0.103 indexed. |
| LM5134B driver | 1.62 | Observed BMF quantity-ten price; exact EU stock/suffix conflict OPEN. |
| Normal matching/filter, including 3 wound cores/block/caps | 2.70 | Unquoted materials; winding labor separate. |
| Separate Fox LPF | 0.64 | 2 coil/four cap allowances; matching cartridge extra. |
| Normal buck/inductor/feedback | 2.31 | TPS62160: €1.408 observed; magnetics/passives estimated. |
| CW shaping across paths | 1.28 | MPS751: €0.72 observed, small switch/RC/BJT allowances; edges unverified. |
| Safety/enable/bus isolation and guard reserve | 3.69 | Lease,latch,POR,gates,comparators,disconnects and guard completion. Distinct functions retained. |
| Current/temp/RF monitors | 0.35 | Shared bench calibration; no precision SWR meter/DAC/EEPROM. |
| Interface PCB socket | 0.45 | Footprint/quote OPEN. RF/power harness sockets below. |
| Beads/clamps + RF shield + heat material | 2.02 | 0.72/0.70/0.60 estimated; do not remove until tests support it. |
| Other resistors/decoupling, pad/calibration selections | remainder | Itemized; fixed calibration does not remove a power test. |

At ten, **€8.59 observed + €11.17 estimated = €19.76**. Increasing only estimates 50% gives **€25.34**. Six-unit nominal 22.41 misses the€20 target; ten/twenty fit only near the upper limit, before sourcing/qualification changes. This is not proof of an achieved budget or the cheapest possible transmitter.

Higher-power material adds **€13.07 /11.10 /11.11 at 6/10/20**. The main incremental driver is LTC3600:€6.13 instead of TPS62160€1.408 at ten, plus OPA171€1.20 allowance, boost€2.09, additional inductor/caps/compensation and€1.50 thermal increment. The ordinary TPS62160 and TPS62130 families stop at 6 V output; do not price either as a 7.6/10.2 V regulator. The old M2 boost/discrete shaper is cheaper on paper at 23.33, but lacks the complete modern reference's measured low-voltage/matching evidence. Keep it as a comparator if higher power becomes a priority, not as a qualified substitute.

## Sourcing and package evidence

| Critical item / exact observed supplier identifier | Observed EUR1 /10 / next break | Availability/MOQ and qualification |
| --- | --- | --- |
| LM5134BMF/NOPB; Mouser 595-LM5134BMF/NOPB | 2.17 /1.62 /1.48@25 | TI Active. Factory reel 1000; cut-tape MOQ1/multiple 1. Recent US family index 510 stock versus older EU 1197 and DE incoming 30 November 2026; exact EU basket OPEN. BMFX is same electrical B with different reel suffix; do not infer a 3,000-piece customer MOQ or transfer another SKU's stock. |
| Rejected LM5134AMF/NOPB; Mouser 595-LM5134AMF/NOPB | 1.78 /1.49 /1.35@25 | 615 indexed, but CMOS threshold unsuitable for direct 3.3 V drive at these rails. Saving€0.13 is not a valid substitution. |
| IRF610PBF-BE3; Farnell 4853567 | 1.110 /.622 /.522@100 | 614 indexed, MOQ1; current manufacturer datasheet, no EOL notice found. Original Mouser IRF610PBF listing has zero stock/future 2027 delivery; do not use its price as availability. Genuine suffix/PCN/pinout and exact local stock must close. |
| Si5351A-B-GT; DigiKey 336-2399-5-ND | 1.87 /1.388 |Preserved dated distributor observation, 10254 older index, live basket OPEN.10-MSOP, fixed I²C address; source/reference spectra remain unmeasured. |
| 74HC00D, 653; Mouser 771-74HC00D-T | .172 /.103 /.081@100 | 70271 indexed, manufacturer family current; cut-tape MOQ1, factory reel 2500. SOIC14; do not mix HCT/HC supply/input characteristics. |
| MPS751 PBFREE; Mouser 610-MPS751 | 1.04 /.72 /.456@100 |[Central manufacturer listing](https://my.centralsemi.com/product/partpage2.php?part=MPS751) Active; 6570 indexed. Exact-vendor TO-92 pinout/hot SOA required. Onsemi counterpart €0.372 at ten indexed is an alternative requiring its own datasheet/life cycle confirmation; not a silent swap. |
| TPS62160DGKT; DigiKey 296-30318-1-ND | 1.90 /1.408 |Manufacturer Active; 4588 older index, cut-tape MOQ1. VSSOP8,1 A/6 V output. Inductor DCR/saturation and input headroom OPEN. |
| LTC3600EMSE#PBF | 7.89 /6.13 /5.54@25 | 125 indexed; exposed-pad MSOP12. Exact supplier ordering code not captured and marked OPEN. TRPBF stock 1432 is another packaging listing, not the same basket. |
| SN75452BP; Farnell UK3118981 | GBP1.020 /.738 | 1186 indexed,MOQ1. EUR1.2074/.8736 calculated using [ECB 12 October 2026 GBP/EUR .84478](https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.fr.html); UK freight/tax separate. Exact manufacturer life cycle and RF large-signal performance need closure. |

URLs, stocks, observation classes and all remaining supplier codes are in [the catalog](M2_80M_INPUTS.json) and [preserved M1 catalog](M1_COST_PARTS.json). Current/indexed observation means the page/index was consulted on this date; it does not make a months-old crawl live inventory. Unquoted wound cores, exact RF cap values/ratings, crystal, connectors, shield and thermal parts are explicitly OPEN. No unauthorized reel minimum or invented quantity-20 discount is used. Native BOM SKU fields identify source parts but have not been repriced when marked ESTIMATE.

## Fabrication, antennas, interconnect and all-in accounting

| Material outside PCB-only component target | 6 /10 /20 EUR/unit | Scope/evidence |
| --- | --- | --- |
| Candidate 80 m bare PCB | 5 /3 /3 |Unquoted €3 per fabricated board, assumed MOQ/order multiple 5: six usable units require ten boards, €5 per usable unit. Other native rows use the same assumed order multiple; exact fab quotes remain OPEN. No panel design or fab quote. Two/four-layer feasibility/size remains OPEN; preserve common outline in Fox-only population. |
| Native FlexFox80 four-layer PCB | 13.33 /8 /8 |Estimate only, 111.35×80.15mm; no supplier quote/volume discount. |
| Native SignalSlinger four-layer PCB | 8.33 /5 /5 |Estimate only, 94.22×59.155mm. |
| Legacy native PCB | 3.33 /2 /2 |Estimate only; Fixle historical.75 fabrication is separately identified and not a current quote. |
| Normal+Fox RF sockets and detachable module power pair | 2.30 /2.30 /2.30 |.70 normal + .40 compact + 1.20 power pair; unquoted. PCB logic socket already included. Fox-only omits normal. |
| Harness power/logic/RF/strain relief | 2.50 /2.50 /2.50 |Fox audit retained allowance; actual universal harness extra remains OPEN. |
| Complete long-wire match/accessory | 10.25 /10.25 /10.25 |Retained M1 estimate including match/connector/wire/return/support; erection pole extra. Native DF variometer already in its complete basket; do not add another copy. |
| Complete compact match/radiator/return/cartridge | 8.38 /8.38 /8.38 |Retained all protective/connective parts; no assumed Classic antenna. |

Panelization and consolidated sourcing are quote opportunities, not savings already credited: combine controller/RF fabrication where the eventual stackup permits, use the same RF outline for Fox-only population, and pool identical stocked MPNs. For example, reducing the two-board fabricated-material allowance from €6 to €4 would save €2 per Fox unit, but no panel, dimensions or supplier quote exists to support that number. Do not retain a promotional first-order price for a repeatable fleet budget.

No fabrication total is a verified panel price. Order minimums/roll material leftovers are still cost risks, not free spares. Contract assembly/setup, winding/programming/calibration/field labor and instruments are **unquoted and excluded**, not assumed free. Shared fixtures/chargers/freight do not become additional PCB material.

The [completed Fox audit](FOXORING_COST_AUDIT.md) remains the accepted accounting reference: **29.06 core+compact /55.24 unit materials /63.34 fleet allocation at ten**, and 29.02/55.20/60.05 at twenty. The tentative NAND/no opamp/fixed calibration population changes only about **−€0.17**:

| Fox scope | 10 | 20 | Interpretation |
| --- | ---: | ---: | --- |
| Candidate core+compact, excluding guard reserve | 28.89 | 28.86 |Same controller/RTC/unpopulated LoRa, same RF PCB, independent compact antenna. |
| Candidate unit budget including guard/protection reserve | 55.07 | 55.04 |Protected two-new 18650 cells in 2S1P, fabrication/case/wiring unchanged. Conditional RF deletions require tests. |
| Candidate with shared charging/provisioning/freight | 63.17 | 59.89 |Same fleet allocation; no repeated 77.11 accounting error. |

Until the NAND/shaping/guard tests pass, **retain 55.24/55.20 and 63.34/60.05 as working budgets**. Restoring the €0.142 op-amp or calibration trim nearly eliminates the tentative saving; no larger reduction is evidenced. A cheap low-voltage trimmer might save up to€2.60 versus the€3 allowance, and two fewer HV caps another€0.50, but **voltage/Q/SRF/availability/field proof is missing**: these are experiments, not booked savings.

For an all-in 1.2 W Classic/Sprint-only unit, an illustrative ten-unit material budget is **about€74.60**: Fox candidate 55.07 +full RF population delta 11.26 +long-versus compact accessory delta 1.87 +normal port.70 +2S2P pack increment 5.70. The latter includes two additional new tabbed 25R cells at €4.70 and additional pack restraint/insulation 1.00 estimate; exact pack construction is unquoted. Add shared fleet infrastructure 8.10/unit if unchanged, about 82.70. This is not an order quote. Higher power changes RF and selected battery costs; a 3 W, 25R 2S4P example is about 96.30 materials with 16.10 pack increment.5 W needs qualified higher-capacity cells or better measured efficiency; its available pack/price is OPEN. Optional LoRa module and 2 m board remain separate, unchanged budgets.

Fox-only still uses the common controller and the same 80 m board outline. DNP watt circuitry reduces component height, heat and mass; it does not establish a smaller bare PCB. Omitting the independent 2 m board and its antenna/heat hardware reduces the universal configuration substantially. The approximately 30 cm radiator, compact return and loading cartridge remain part of the installed dimensions. TinyFox/Fixle's smaller one-board cases do not demonstrate the size of our common-platform assembly.

## Real-world comparators

[SignalSlinger kit](https://backwoodsok.org/store/SignalSlinger-Transmitter-Kit-p799230332) is **USD90** advertised, approximately**€80.49** at ECB 12 October 2026 USD/EUR 1.1181; **USD80≈€71.55** without backup cell. Retail tax/import VAT/freight not specified; this is not an ex-VAT manufacturing BOM. Kit includes hand assembly parts/case/internal backup cell; external operating 12 V pack, antenna and shared configuration cable are extra. Do not compare its 90-dollar price to our 19.76-euro RF board or claim equivalent complete-system cost.

Fixle author's **€5.65/~€6** material calculation includes PCB/crystal/MCU/case/wires, uses author/bulk stock prices and does not price CR2032; no RTC/programmed frequency/2S protection/common controller or calibrated 10 mW/spectral dataset. TinyFox **historical€15–30** includes a different AA/crystal/ATtiny compact construction, without our common platform functions; current complete kit quote unavailable. They show that low-power RF silicon/matching can be simple, not that ARDF-TX's controller/battery/mechanics scope costs zero.
