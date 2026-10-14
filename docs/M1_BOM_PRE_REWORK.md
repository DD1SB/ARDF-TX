# Historical M1 BOM before cost rework

**Superseded; retained for audit only.** Use [revised BOM](M1_BOM_CANDIDATES.md) and [cost rework](M1_COST_REWORK.md) for current proposals. The old ranges/component choices below are not current recommendations.

Date: **2026-10-13**. **Candidate functional BOM, not an ordering list.** No netlist/reference-designator BOM exists because electrical design is outside M1. Quantities below are architecture allowances, not proof that a circuit contains exactly that count. Every required cost function is included, including off-board matching and protection. **OPEN** rows require MPN/value/footprint/price resolution before M2 design release; do not substitute fictitious quotes for them.

Prices are distributor page/index observations retrieved on this date; some are cached weeks/months earlier. Stock changes and conflicting observations are disclosed. EUR prices below are ex-VAT where distributor states this; USD remains USD. No FX conversion, reel discount, shipping or tax savings assumed. MOQ means customer minimum, distinct from manufacturer reel size. Fleet of six: use quantity-one ceilings until the basket reaches ten; fleet ten: use listed ten break only for identical MPNs with aggregate quantity ≥10. Cut tape/tube costs avoid unnecessary reeling fees.

## Observed critical components and alternates

| ID / use | Manufacturer / exact candidate MPN | Package / footprint to inspect | Distributor evidence; observed availability | MOQ / packaging | Unit price at 1 / 10 | Decision / provenance |
| --- | --- | --- | --- | --- | --- | --- |
| Q01 controller MCU | Espressif ESP32-S3-WROOM-1-N4 | 18×25.5 mm module, 40 edge pads + exposed pad; vendor land pattern/antenna keepout | [Mouser DE](https://www.mouser.de/de/ProductDetail/Espressif-Systems/ESP32-S3-WROOM-1-N4?qs=Li%252BoUPsLEnsO%2FkiJOUK0FQ%3D%3D), 3,318 listed | 1 / cut tape | EUR 4.48 / 3.88 | Candidate; enough interface pins, no wireless use required. ESP-DS for physical data. |
| Q02 cheaper MCU alternate | Espressif ESP32-C3-MINI-1-N4 | 53-pad SMD module; exact vendor pattern differs from replacement N4X | [DigiKey DE](https://www.digikey.de/en/products/detail/espressif-systems/ESP32-C3-MINI-1-N4/13877574), 9,309 listed, **not for new designs** | 1 / cut tape, full reel 650 unnecessary | EUR 2.79 / 2.413 | Not selected: pin budget/lifecycle. Do not silently use N4X footprint as same. |
| Q03 RTC option A | Micro Crystal RV-3032-C7-32.768KHZ-2.5PPM-TA-QA | C7 8-pad ceramic SON, 3.2×1.5×0.8 mm | [DigiKey DE](https://www.digikey.de/en/products/detail/micro-crystal-ag/RV-3032-C7-32-768KHZ-2-5PPM-TA-QA/16273065), 759 listed | 1 / cut tape, reel 1,000 unnecessary | EUR 2.71 / 2.032 | Preferred RTC family; RTC-DS. Supplier punctuation/order code to reconcile at order. |
| Q04 RTC option B | Micro Crystal RV-3032-C7 32.768kHz-2.5PPM-TA-QC | Same C7 land pattern; temperature/qualification suffix review | [Mouser DE](https://www.mouser.de/de/ProductDetail/Micro-Crystal/RV-3032-C7-32.768kHz-2.5PPM-TA-QC?qs=MyNHzdoqoQI0ah9ohGRrVw%3D%3D), 16,637 listed | 1 / cut tape | EUR 3.57 / 2.68 | Independent distributor/family alternate; verify exact suffix characteristics. |
| Q05 RTC cost comparator | ADI/Maxim DS3231SN# | 16-SOIC wide, 7.5 mm body, external backup | [Mouser DE](https://www.mouser.de/de/ProductDetail/Analog-Devices-Maxim-Integrated/DS3231SN?qs=sGAEpiMZZMuMkwKcEjFF1GtcHqpbrLRsqovgWKfSoN0%3D), 2,808 listed | 1 / small quantity | EUR 15.02 / 11.87 | Too expensive/large versus RV3032. Other packaging observations differ; do not quote cheapest without checking. |
| Q06 uncompensated RTC alternate | Micro Crystal RV-3028-C7 32.768KHZ 1PPM-TA-QC | C7 8-SON 3.2×1.5 mm | [DigiKey](https://www.digikey.de/en/products/detail/micro-crystal-ag/RV-3028-C7-32-768KHZ-1PPM-TA-QC/10431070), 1,609 listed; [Mouser](https://www.mouser.de/de/ProductDetail/Micro-Crystal/RV-3028-C7-32.768kHz-1ppm-TA-QC?qs=u16ybLDytRaU7ZFJl2AxfQ%3D%3D) lists zero | 1 / cut tape | DK EUR 2.18 / 1.621; Mouser 2.75 / 2.05 | Room-temperature accuracy not all-temperature guarantee; not selected. Stock conflict disclosed. |
| Q07 common buck | TI TPS62160DGKT | 8-VSSOP/MSOP, 3 mm body, 0.65 mm pitch, vendor DGK pattern | [DigiKey DE](https://www.digikey.de/de/products/detail/texas-instruments/TPS62160DGKT/3074519), 4,588 listed; [Mouser DGKT](https://www.mouser.de/de/ProductDetail/Texas-Instruments/TPS62160DGKT?qs=2UFnnMkojnVQry4yr%2Fdsnw%3D%3D) ten EUR 1.42 | 1 / cut tape; full reel 250 unnecessary | DK EUR 1.90 / 1.408 | 3–17 V input, 1 A output candidate; inductor/capacitors extra. |
| Q08 80 m boost | TI TPS611781RNWT | RNW 13-pad HotRod QFN, 3×3.5 mm; vendor-specific land pattern | [Mouser DE](https://www.mouser.de/de/ProductDetail/Texas-Instruments/TPS611781RNWT?qs=sGAEpiMZZMvAX9OfPh%252B2NTRTUzqTannr7HswSSR5aF8a4%252B0ItKMTKw%3D%3D), 333 listed | 1 / cut tape; reel 250 unnecessary | EUR 4.90 / 3.73 | Up to 20 V, forced PWM; external disconnect FET/inductor/caps extra. R-suffix [Mouser US](https://www.mouser.com/ProductDetail/Texas-Instruments/TPS611781RNWR?qs=Mv7BduZupUjx2ZfyDo32jQ%3D%3D) USD 3.17/2.38, 1,820 listed; do not mix currencies. |
| Q09 lower rail boost alternate | TI TPS61088RHLR | RHL 20-VQFN 3.5×4.5 mm | [Mouser DE](https://www.mouser.de/de/ProductDetail/Texas-Instruments/TPS61088RHLR?qs=MiqG6Kq1qKNjgpnslrNKug%3D%3D), 99 listed | 1 / cut tape; reel 3,000 **not required** | EUR 2.36 / 1.76 | ≤12.6 V output; suitable VHF rail candidate, not 15 V QCX supply. No true output-off without external isolation. |
| Q10 HF synthesizer | Skyworks SI5351A-B-GT | 10-MSOP, 3×3 mm body, 0.5 mm pitch | [DigiKey DE](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847), 10,254 listed; [Mouser family](https://www.mouser.de/c/semiconductors/integrated-circuits-ics/clock-timer-ics/clock-generators-support-products/?series=Si5351), 3,736 listed | 1 / tube | DK EUR 1.87 / 1.388; Mouser 1.88 / 1.39 | Preferred HF; VHF cheap experimental alternate. 25/27 MHz crystal, quiet rail and filters extra. |
| Q11 VHF PLL | TI LMX2571NJKT | NJK 36-WQFN exposed pad, 6×6 mm | [Mouser EU observation](https://www.mouser.es/es/ProductDetail/Texas-Instruments/LMX2571NJKT?qs=sGAEpiMZZMug9GoBKXZ755TkJLGfYfNSW6JqdkucdhWCK5QsTVf8eQ%3D%3D), 1,382 listed | 1 / cut tape, reel 250 unnecessary | EUR 14.61 / 11.58 | Reference/loop/filter/quiet rail extra. Other country/index prices conflict; use this higher observed EU basis until live basket confirmed. |
| Q12 local module MCU | ST STM32C011F6P6 | TSSOP-20, vendor package; fit GPIO/private buses before lock | [Mouser DE](https://www.mouser.de/de/ProductDetail/STMicroelectronics/STM32C011F6P6?qs=IPgv5n7u5Qb445hYVpG9pg%3D%3D), 315 listed | 1 / tube | EUR 1.32 / 0.929 | One each RF board candidate. F4 TR shows no stock; do not assume that alternate available. |
| Q13 independent watchdog | TI TPS3431SDRBR | DRB 8-VSON exposed pad, 3×3 mm | [DigiKey DE](https://www.digikey.de/en/products/detail/texas-instruments/TPS3431SDRBR/9597847) zero, expected Jan 2027; [Mouser DE](https://www.mouser.de/ProductDetail/Texas-Instruments/TPS3431SDRBR?qs=w%2Fv1CP2dgqr73oCnz11srA%3D%3D) older index 4,772 | 1 / cut tape | DK EUR 1.78 / 1.313 | Availability **unresolved conflict**, not reserved. Persistent latch/gates/POR extra. Select stocked equivalent or validate direct evidence before M2. |
| Q14 DAC setpoint | Microchip MCP4725A0T-E/CH | SOT-23-6, vendor pinout | [Mouser DE](https://www.mouser.de/de/ProductDetail/Microchip-Technology/MCP4725A0T-E-CH?qs=vkMqrgFpRajeQECZ3goc0A%3D%3D); family lists 40,212 | 1 / cut tape, reel 3,000 unnecessary | EUR 1.09 / **not published at ten**; retain 1.09 ceiling assumption | Optional setpoint, not waveform streaming dependency. PWM/filter alternative tested for ripple. EEPROM power-on value cannot arm RF. |
| Q15 low-voltage op amp | TI TLV9002IDR | SOIC-8, 3.9 mm body | [Mouser DE](https://www.mouser.de/ProductDetail/Texas-Instruments/TLV9002IDR?qs=xhbEVWpZdWdPu%252BhBN%252BBREg%3D%3D), 11,215 listed | 1 / cut tape | EUR 0.593 / 0.421 | Low-voltage sensing/tone; cannot directly swing 12 V modulator. |
| Q16 HF PA devices | onsemi BS170 (bulk) | TO-92-3; manufacturer D/G/S orientation checked in M2 | [Mouser bulk category](https://www.mouser.de/de/c/semiconductors/discrete-semiconductors/transistors/mosfets/?package+%2F+case=TO-92-3&packaging=Bulk&transistor+polarity=N-Channel), 85,463 listed | 1 / bulk | EUR 0.387 / 0.237 from other family observation; newer listing ten missing | Three per watt PA; ten price **cached family observation**. Different suffixes change package/dissipation; no automatic substitution. |
| Q17 raw-pack P-FET | Nexperia PMPB20XPE,115 | DFN2020MD-6, 2×2 mm | [DigiKey DE](https://www.digikey.de/en/products/detail/nexperia-usa-inc/PMPB20XPE-115/4021003), 6,245 listed | 1 / cut tape | EUR 0.72 / 0.446 | Candidate raw 2S reverse/isolation pair; **not** qualified for boosted 15 V transient margin or linear AM SOA. |
| Q18 modulator transistor alternate | onsemi BD140G | TO-225-3, exact pin order unlike generic assumptions | [Mouser DE](https://www.mouser.de/en/ProductDetail/onsemi/BD140G?qs=sGAEpiMZZMvplms98TlKY3rIOtqo%252BKm6JDlFQpN8CxQ%3D), 5,071 listed | 1 / bulk | EUR 1.34 / 0.851 | Candidate series device; current/SOA/headroom/heat sink unvalidated. [ST BD140](https://www.mouser.de/ProductDetail/STMicroelectronics/BD140?qs=ljbEvF4DwOOQh3TFtIzRQQ%3D%3D) 0.585/0.264, TO-126, 5,060 listed: **different footprint**. |
| Q19 obsolete driver reference | Infineon BFR 106 E6327 | SOT-23, vendor lead assignment | [Mouser DE](https://www.mouser.de/ProductDetail/Infineon-Technologies/BFR-106-E6327?qs=OWKQh20chup4oQOMFBQE5g%3D%3D), 5,850 listed, NRND/EOL indications | 1 / cut tape | EUR 0.98 / 0.679 | Bench reference only, not repeatable fleet selection. Active driver MPN OPEN. |
| Q20 historical VHF PA | Mitsubishi RD06HVF1 | Manufacturer TO-220-style **G/S/D**, source tab; use exact drawing | [RF Parts](https://www.rfparts.com/rftransistors/transistor-rd/rd06hvf1.html), in stock **NOS**, exact count not visible | 1 observed / individual | USD 9.91 / ten **not quoted** | Bench reference only. Fleet active PA MPN/price OPEN; no EUR conversion assumed. |
| Q21 excluded PA | NXP AFT05MS006NT1 | PLD-1.5W/SOT1811-2 4-terminal RF package | [Manufacturer EOL](https://www.nxp.com/products/radio-frequency-rf/legacy-rf/legacy-rf-power/136-941-mhz-6-0-w-7-5-v-wideband-rf-power-ldmos-transistor%3AAFT05MS006N?tab=Package_Quality_Tab); [Mouser](https://www.mouser.ca/ProductDetail/NXP-Semiconductors/AFT05MS006NT1?qs=7imfUp6rdT2w95RI2BA6Jw%3D%3D) nonstocked/reel-only | Observed 1,000 reel on cited listing | No usable small-quantity quote | **Excluded**, no broker/aggregator price in baseline. |
| Q22 active, oversized VHF comparator | Ampleon BLP5LA55SXY | TO-270-2F-1, 2 RF leads + source flange; vendor drawing | [Mouser US](https://www.mouser.com/ProductDetail/Ampleon/BLP5LA55SXY?qs=NeOn4crkEusdJXa%252BhqL4DQ%3D%3D), 62 listed; manufacturer Active | 1 / cut tape despite factory reel 100 | USD 28.62 / 22.91 | Measured VHF reference exists but 55 W device/bias too large for unchanged low-power design. Price does not close 8–15 EUR PA allowance. |
| Q23 active, oversized alternative | Ampleon BLP9LA25SXY / BLP9LA25SZ | TO-270-2F-1, vendor drawing; 25 W at 13.6 V | [Mouser DE XY](https://www.mouser.de/de/ProductDetail/Ampleon/BLP9LA25SXY?qs=sGAEpiMZZMs8PWDkLjJX9UHKR5EdyjgoBUpe3SpeBr%2FcebSEH0f3Rg%3D%3D) zero; [DigiKey Z](https://www.digikey.de/de/products/detail/ampleon-usa-inc/BLP9LA25SZ/12675591) indexed cut-tape listing, detail access failed | Mouser XY MOQ 100, Z 500; DK small-quantity stock/MOQ unresolved | No 1/10 price captured; XY EUR 11.46 **at 100 only**, not fleet price | Manufacturer Active; exclude observed reel-only offer. Investigate a real cut-tape quote only if PA transfer/bias merits it. |

For Q21 the distributor query-encoded link may fail; manufacturer EOL evidence is sufficient for exclusion. Footprint data above names packages/vendor patterns, **not downloaded or approved CAD library files**. Manufacturer land patterns/pin maps, not distributor ECAD thumbnails, govern M2.

## Complete functional BOM coverage

Range totals below deliberately exceed the seed stretch targets. Q references give exact candidate MPNs where evidence supports them. **TBD** means no defensible MPN/value/quote yet, with a cost allowance rather than a fabricated price. Generic connector/current/voltage ratings are procurement requirements, not footprint decisions. All allowances are per unit at six-to-ten fleet scale.

| Assembly / function | Candidate / count | Package or required footprint function | Unquoted allowance EUR / remaining action |
| --- | --- | --- | --- |
| Controller MCU/RTC/buck | Q01/Q03/Q07 ×1 each | Vendor module/C7/DGK | Observed core ~7.32 EUR at ten, excluding supporting parts. |
| Controller protection/branch switches | Q17 ×2 plus additional branch FETs/TVS/fuse TBD | 20 V raw-pack FET pair; separately rated fused feeds | 2–4; true reverse/backfeed/short protection. |
| Controller bus isolation | TCA9543A-family ×1 or two branch isolators; exact MPN TBD | Resettable I2C branch switch | 1–3; family and RESET/default behavior must be checked. |
| Controller safety/POR/latch | Q13 ×1 candidate + gates/POR TBD | VSON plus logic gates; latch persistent | 2–4; stocked watchdog alternative needed if conflict unresolved. |
| Controller monitoring | Battery divider/RC, current sensor/shunt/NTC TBD | ADC/filter/Kelvin shunt; temperature limits | 1–2; resistor errors and input protection included. |
| Controller RTC backup | Small primary cell/holder or qualified capacitor TBD | Backup device + isolation; charger disabled for primary cell | 1–2; no unsafe charging of primary cell. |
| Controller connectors/UI | Two module harness interfaces, battery connector, USB, sync, button/LED/ESD | Keyed/polarized power; nine logic functions/module | 3–5; mating cable contacts included in allowance. |
| Controller passives/inductor | Buck inductor, decoupling, bulk caps, pulls/RC, regulator passives TBD | 0603/0805 default, vendor-rated magnetics | 2–3; capacitor bias and inductor saturation qualification. |
| 80 m local source/bridge | Q10/Q12 ×1, 25/27 MHz crystal TBD | MSOP/TSSOP/crystal + private bus | 3–5 including crystal and quiet regulator allowance. |
| 80 m watt PA | Q16 ×3, logic driver e.g. 74ACT-family, shaping transistor/setpoint Q14 optional | TO-92 plus verified 3.3-to-5 V logic input stage | 2–4; driver exact MPN/thermal arrangement TBD. |
| 80 m boost/rail control | Q08 ×1 + external isolation FET + power inductor/caps/compensation | RNW + disconnect FET rated for 15 V/transients | 6–9; do not omit external FET. |
| 80 m LPF/matching to reference port | Toroids/air coils, C0G RF capacitors and damping TBD | Watt-rated/Q/SRF verified, 50 Ω test plane | 3–5; values and manufacturer codes await RF design. |
| 80 m bounded Foxoring source | Small buffer, permanent pad, own LPF, bounded rail/clamp TBD | 10 mW mark calibration plane | 1–3; includes pads/test points, not loading cartridge. |
| 80 m safety and sensing | Q13, gates/POR/latch, current/temperature/reflected sensor TBD | Independent supply/input gates and cartridge inhibit | 3–5; coupling and envelope level calibration. |
| 80 m connectors/shield/passives | Normal+keyed Fox ports, harness, shield/return components TBD | Dissimilar mating paths; low-capacitance protection | 4–6; RF connector package deliberately OPEN. |
| VHF local PLL/bridge/reference | Q11/Q12 + XO/TCXO, PLL loop/quiet rail TBD | QFN/TSSOP/reference package | 14–20; includes source filter/reference. |
| VHF low-level AM/driver | Tone PWM/filter or Q14 setpoint, Q15 sensing; active RF driver TBD | RF-rated transistor/MMIC, exact gain/power/SOA OPEN | 3–6; do not adopt obsolete Q19 for fleet. |
| VHF PA | **Active-production ≥5.14 W clean-envelope device TBD**; Q20 bench reference | Rated at chosen VHF/supply; thermal pad + heat sink | **8–15 allowance, not quote**; dominant sourcing blocker. |
| VHF supply modulator/boost | Q09 candidate, high-voltage op amp/level shift, Q18 candidate, isolation/inductor/caps TBD | Linear SOA plus ~12 V headroom | 6–10; low-voltage TLV9002 cannot alone drive high rail. |
| VHF normal filter/sensing | BPF/LPF, forward/reflected detector/coupler, NTC TBD | 144–146 MHz ratings, own quiet returns | 3–5; filter values/layout/uncertainty OPEN. |
| VHF bounded training branch | Low-level AM buffer, permanent attenuation, own LPF, bounded rail and interlock TBD | 1 µW–1 mW carrier; never normal PA route | 2–4; PEP/normal-PA coupling tests required. |
| VHF safety/ports/shield/passives | Q13 candidate + latch/POR/gates, two dissimilar RF ports, harness/shield TBD | Low-capacitance protection; thermal/mechanical isolation | 8–12; ensures training connector/protection not omitted. |

These functional allowances are **additive cost envelopes, not distributor quotations**. Controller core plus allowances is about 19–31 EUR before rounded sourcing reserve (headline 22–32); HF envelopes sum 22–37 EUR before reserve (headline 26–42); VHF envelopes sum **44–72 EUR**. No fully price-closed RF BOM is established. Every TBD row is a procurement/design gate; available oversized PA alternatives Q22/Q23 do not establish a cheap low-power PA price or efficiency.

## Costed antenna and compact-mode accessories

| Mode accessory | Required items / candidate quantities | Footprint/ratings / unresolved MPNs | Allowance EUR |
| --- | --- | --- | --- |
| Long-wire 80 m match | One loading/tuner coil/core, adjustable RF capacitor plus fixed C0G caps, tune indicator, enclosure, normal RF mating connector, radiator and symmetric radials/terminals | Coil/capacitor Q and RF voltage/power ratings; MPNs/values TBD after measurements. Long antenna must be costed even off-board. | **8–18** |
| Long-wire support | Pole/tree attachment, strain relief and ties | Installation option; no fixed 8 m/6 m rule | **5–15**, separate mechanical allowance |
| Compact Foxoring loading/coupling | One loading/tuned network (experiment 134–402 µH bracket), tap/coupling capacitor, trimmer/fixed C0G caps, damping, insulation, low-capacitance protection, keyed plug/identity contact, cartridge enclosure | Coil SRF/Q at 3.5 MHz, pF loading, capacitor voltage/insulation; no selected windings or part codes yet | **5–11** |
| Compact radiator/counterpoise | ~30 cm wire/rod, mounting/strain relief, three compact radial wires or ground plate candidate, dedicated return terminal | Actual dimensions/material/attachment must match field-qualified recipe | **2–4**; Foxoring accessory total **7–15** |
| VHF competition antenna | Horizontal ring/turnstile, balun/feedline/connectors, mounting | 2–3 m placement; gain/pattern/feed loss measured, MPNs TBD | **10–20**, support allowance **5–15** separately |
| VHF training antenna | Short antenna with known coupling/gain and separate connector | Field range TBD | **2–5** separately if not included in local training kit |

Single-port adapter, switched onboard match and separate paths were compared in [feasibility](M1_FEASIBILITY.md). Separate paths spend an extra connector/interlock but avoid a watt-rated pad/switch in the fragile compact network. Allowances include protective hardware; advertised tiny-transmitter prices without matching hardware are not the modular Foxoring cost.

## Per-board and configuration ranges

Electronics totals include protection, RF sockets, primary module interface mating parts and shielding, **exclude bare PCB manufacture/assembly, packs, charger, LoRa, enclosure and installed antenna accessories**. They are feasibility allowances supported by the critical quotes and explicit TBDs, not a promised purchase price.

| Board population | Candidate EUR/unit |
| --- | --- |
| Controller without LoRa | **22–32** |
| Universal 80 m RF (both paths) | **26–42** |
| Foxoring-only population of same 80 m PCB, watt branch omitted | **10–18** |
| VHF PLL/A2A/isolated training | **44–72** |
| VHF Si5351 experimental alternate | ~10–14 less than PLL version **only if full spectrum gate passes** |
| All three, PLL VHF, electronics | **92–146** |

| Hardware configuration, without pack/enclosure/LoRa/PCB/labour | Included costed antenna system | Candidate EUR/unit |
| --- | --- | --- |
| 80 m Classic/Sprint | Controller+universal HF+long match/wire/radials | **56–92** |
| Compact Foxoring, universal HF board | Controller+universal HF+compact match/radiator/counterpoise | **55–89** |
| Compact Foxoring, reduced HF population | Controller+Fox-only HF+compact match/radiator/counterpoise | **39–65** |
| VHF Classic + training electronics | Controller+VHF+competition antenna | **76–124**; training antenna/support separate |
| Universal unit, both 80 m antenna options and VHF antenna | All three boards+long match+compact cartridge+VHF antenna | **117–199**; support separate |

The original EUR 43–75 all-board stretch target is **not evidenced**. Main drivers are VHF PLL, real AM headroom, safety/connectors and dedicated matches. Six universal units at these ranges: **702–1,194 EUR**; ten: **1,170–1,990 EUR**, excluding the stated common additions. No volume beyond ten is used to justify prices.

Bare PCB allowances: controller/HF 2–5 EUR each, VHF 3–7 EUR each at fleet panel scale; **unquoted**, layer count and assembly process OPEN. Enclosure/weatherproof seals/heat sink/mountings: 8–18 EUR per single-band unit or 12–25 universal, unquoted; assembly/test labour and instruments separately. A universal package is not a compact Foxoring package even with a small radiator.

## Cells, pack hardware, charger and LoRa

[NKON cell listings](https://www.nkon.nl/en/rechargeable/li-ion.html?brand%5B0%5D=Samsung&brand%5B1%5D=Panasonic&ratings_summary=80&soortbatterij=18650&stock_availability=In+Stock) show Samsung INR18650-35E 3400 mAh at EUR 2.59 incl./2.14 excl. tax and Panasonic NCR18650B 3350 mAh at 5.45 incl./4.50 excl. No ten-piece discount verified; use base-price ceilings, no old-stock/reclaimed bargain assumptions. Manufacturer cell/lot/rating evidence must precede pack selection. Cells are unprotected individually; **a bare pair is not the required protected pack**.

| Item | Candidate / MOQ and price evidence | Material allowance, ex-VAT EUR |
| --- | --- | --- |
| Pack cells | 2P-count×2 cells, MOQ 1 on listings; 1/10 price breaks not fully captured | 4.28–9.00 per parallel pair |
| Per-pack BMS/balance/temperature/fuse | External protected 2S pack; exact qualified supplier/MPN OPEN | 5–10 |
| Pack wiring/connector/insulation/mechanics | Matched cells, nickel/wire, keyed connector, securing/strain relief; no arbitrary parallel loose packs | 6–13 |
| 2S1P / 2S2P / 2S3P / 2S4P materials | Rounded cells+protection/mechanics, **not assembled-pack quotes** | **15–32 / 20–41 / 24–50 / 28–59** |
| External 2S CC/CV charger | Qualified 8.4 V charger, exact MPN/charge current OPEN | 7–15; fleet can share chargers, throughput to plan |
| Silicontra SX1262 | Exact module, distributor, footprint, MOQ and 1/10 prices **OPEN** | 10–20 **allowance only**, not quote |
| LoRa antenna/mating/mount/filter | Variant/band-specific parts OPEN | 2–6 separately |

Bare SX1262 IC reel size is irrelevant to an optional purchased module; never assume 3,000 chips must be bought. No compatible Silicontra pinout/price is invented. An assembled protected-pack and module quote are explicit M2 sourcing gates.

## Modified handheld baseline

[Airsoftmania UV-5R listing](https://airsoftmania.eu/products/baofeng-uv-5r-8w-radio-vhf-uhf-black): **EUR 29.00**, 232 units advertised, MOQ one; [Skirmshop](https://www.skirmshop.nl/en-nl/products/uv5r-profesional-two-way-radio-black/): **EUR 29.95**, advertised in stock. Retail VAT basis/revision/genuine component identity require basket inspection; no quantity-ten discount observed. “8 W” is a retailer claim, not measured output. BTECH's UV-5R page is a discontinued-product archive, not proof of present production/revision availability.

| Conversion function | Candidate EUR allowance |
| --- | --- |
| Radio at observed retail unit price | 29–30 (retail tax basis not harmonized) |
| Shared ESP32 timing/controller | 22–32 |
| Actual AM modulator/tone/PA rail work | 5–12 |
| RF filter, hard mute and isolation | 6–12 |
| Protected separate low-power training path | 5–10 |
| External 2S power adapter/wiring | 3–6 |
| Conversion subtotal, no external pack/antenna/labour | **70–102**, mixed retail tax basis disclosed |
| Horizontal antenna | +10–20 |

Unmodified FM-only timed radio is cheaper but does not meet the product. The compliant conversion is an **unvalidated cost allowance**, not a known successful mod, and overlaps the new VHF system's 76–124 EUR range. Benchmark includes the radio's stock battery/chassis but does not claim its 1.8 Ah battery meets endurance. Conversion labour, destructive rework, revision control, thermal/spectrum tests and spares must be counted separately. Do not claim new PCB wins on price before that comparison is measured.

## Sourcing policy before design release

Use two reputable distributor paths for critical parts where possible; inspect exact live small-quantity packaging/status at freeze, not 1,000-unit manufacturer list prices. Q13 stock conflict, active VHF PA/driver, exact Silicontra module and protected-pack sourcing are unresolved. Do not use brokers, unexplained legacy substitutions or purported pin equivalents as accepted stock. PA/PLL/coil/crystal substitutions invalidate relevant RF calibration/spectrum/thermal tests; passives and connector alternatives need rating/fit checks. A complete circuit BOM with designators, approved footprints and every part quote belongs after M2 circuit decisions, not this candidate document.
