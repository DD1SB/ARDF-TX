# M5B-E6R1 — seven-transmitter cost impact

All amounts below are **EUR net estimates per unit at quantity seven**, unless identified as an indexed gross supplier price. No order, quote or procurement occurred. E5/E6 historical costing is preserved and imported rather than silently recalculated with current prices.

| Arrangement | Separate coolers | Cooling materials /unit | Proposed added electronics /unit | Combined material /unit | Seven-unit combined materials |
| --- | ---: | ---: | ---: | ---: | ---: |
| E5 SK81 +SK10075SA +FK213SA32 | 3 | 31.11–38.61 | — | 31.11–38.61 | 217.77–270.27 |
| E6 common SK81 100 concept | 1 | 15.36–21.36 | — | 15.36–21.36 | 107.52–149.52 |
| E6R1 retained SK81 100 + keying/protection proposal | 1 | 15.36–21.36 | 1.53–3.61 | 16.89–24.97 | 118.23–174.79 |
| E6R1 SK81 75 comparator | 1 | 13.89–19.89 | 1.53–3.61 | 15.42–23.50 | 107.94–164.50 |
| E6R1 flat-stock comparator | 1 | 11.23–20.23 | 1.53–3.61 | 12.76–23.84 | 89.32–166.88 |

Smaller comparators fail parts of the thermal envelope and are not selected to claim savings. The retained R1 material allowance is lower than E5's historical budget, but installed savings remain estimates because protection is not yet accepted. An additional circuit required to close the thermal gate could change them.

The [machine-readable costing](../hardware/2m/review/M5B-E6R1/cost-impact.json) includes TLV7034PWR €0.70–1.50, SN74LVC2G00DCUR €0.12–0.30, SN74LVC2G32DCUR €0.12–0.30, SN74LVC1G04DBVR €0.06–0.18, 2N7002 €0.03–0.08, NCP15XH103F03RC €0.05–0.15, resistor/capacitor/pad allowance €0.30–0.60 and sensor-bond consumables €0.15–0.50. **All new-part prices and seven-unit availability are unquoted estimates**, not a confirmed supplier cart. Exact selected push-pull comparator is TLV7034PWR; an earlier open-drain candidate is not the selected BOM. Ordinary packages are intended; no exotic controller or transceiver is added.

[SK81 100](https://www.reichelt.com/de/en/shop/product/heat_sink_100_mm_aluminium_2_2_k_w-227984) was indexed at €7.30 gross, approximately €6.13 net at 19% VAT; [SK81 75](https://www.reichelt.com/de/en/shop/product/heat_sink_75_mm_aluminum_2_5_k_w_-227987) €5.55 gross /€4.66 net. Indexed availability/minimum-one listings do not establish a seven-unit reservation. [100×4 flat stock](https://www.dold-mechatronik.de/Flachstange-100x4mm-Aluminium-EN-AW-6060-T66-AlMgSi05-1112kg-m-Zuschnitt-20-6000mm) has a minimum configurable cut; the displayed €1.32 was not a 100 mm quote. €2–5 net for that cut is a budget only. Bar, two insulating interfaces, shoulder hardware, brackets, guard and consumables remain in cooling allowances. No enclosure thermal credit or free hardware is assumed.

E5 thermal assembly allowance is 45–75 minutes; E6 single-cooler concept 25–45 minutes, both engineering estimates rather than timed work. R1 sensor bonding/inspection and keying setup add 5–12 minutes. At an illustrative €25/hour, this adds €2.08–5.00/unit, or €14.58–35.00/fleet, beyond E6 thermal assembly labor. Guard/enclosure fabrication, RF alignment, isolation test, source-joint inspection/X-ray and first-article instrumentation require separate allowance. Service access remains a concept, not demonstrated repair time.

The unchanged historical seven-unit electrical BOM planning bases are BUCK4S €52.76, BOOST2S €54.33, TRAIN_ONLY €14.11 before this new-part delta. Bare-board quantity-five procurement, controller, pack/BMS, antenna/feed, harness, enclosure, freight, VAT, RF calibration and prototype inspection are not included in the thermal subtotal. PCB outline/layer/process remain unchanged in this analysis, but no new populated-PCB or routed revision quote exists. No claim of a complete €120 or €150 transmitter follows. The modest estimated electrical delta is justified by real loss reduction and the PA protection gap, but it buys no qualified protection until the coupling/threshold gate is resolved.
