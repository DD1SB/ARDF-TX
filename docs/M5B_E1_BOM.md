# M5B-E1 material budget

2026-10-16. EUR net, VAT/shipping/labor separate. These are candidate material budgets, not purchase quotations. No procurement is authorized. The complete per-position, MPN, footprint, population, supplier, MOQ, pooled-order, price-break and evidence ledger is [RF2M_BOM.csv](../hardware/2m/review/M5B-E1/RF2M_BOM.csv); the three population CSVs provide quantity-ten assembly lists. Do not count test pads, TL copper features or footprint assignments as purchased ICs.

| Population | 6 each | 10 each | 20 each | Fitted parts | ICs | Unquoted at10 | Delta/R4 at10 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| BOOST2S | €54.33 | €50.27 | €49.94 | 272 | 25 | €28.09 | €+6.95 |
| BUCK4S | €52.76 | €49.03 | €48.71 | 268 | 25 | €27.95 | €+7.01 |
| TRAIN_ONLY | €14.11 | €14.11 | €14.11 | 103 | 13 | €10.02 | €+2.83 |

The original R4 quantity-ten baselines are€43.32/€42.03/€11.28. Normal populations add eight fitted parts and one IC: the preregulator, divider/bypass parts, liftable driver/RF links and selected local converter reservoir. R651 is DNP and optional test-only. No component is counted twice because two footprints share an MPN. Price pooling and MOQ rounding use the actual fleet demand; no speculative discount is booked. Deltas are calculated before displayed-cent rounding.

The increase also includes the exact MMCX rather than an unspecified cheap connector, the low-DCR RF choke and corrected current shunt/divider. The two-stage driver protection costs more than the old marginal circuit. It is not hidden in a blanket allowance. The full RF/source/matching/AM/driver-supply core is approximately€28.56 at ten; that is not the complete transmitter.

| Functional block | 2S at10 | 4S at10 | Training at10 |
| --- | --- | --- | --- |
| am | €1.040 | €1.040 | €1.080 |
| bias | €2.005 | €2.005 | €0.000 |
| connector | €5.780 | €5.780 | €4.330 |
| converter | €3.915 | €2.684 | €0.000 |
| decoupling | €0.765 | €0.765 | €0.540 |
| driver | €4.380 | €4.380 | €0.000 |
| driver_supply | €3.333 | €3.333 | €0.000 |
| input | €1.795 | €1.795 | €0.000 |
| interface | €0.345 | €0.345 | €0.300 |
| interlock | €3.075 | €3.075 | €2.680 |
| modulator | €1.980 | €1.980 | €0.000 |
| output_filter | €2.950 | €2.950 | €0.000 |
| pa | €5.300 | €5.300 | €0.000 |
| pa_match | €4.250 | €4.250 | €0.000 |
| passive | €0.100 | €0.100 | €0.100 |
| power | €0.390 | €0.390 | €0.000 |
| protection | €2.195 | €2.195 | €0.020 |
| source | €2.280 | €2.280 | €2.280 |
| source_filter | €1.044 | €1.044 | €0.000 |
| supply_isolation | €0.560 | €0.560 | €0.000 |
| training | €2.783 | €2.783 | €2.783 |

Current indexed observations include Panasonic C409, Coilcraft33 nH/150 nH feeds, Wurth MMCX and the Bourns power inductors. Earlier distributor observations remain HISTORICAL; unquoted passives, protection and control positions remain ESTIMATE_UNQUOTED. At ten the unquoted amounts above remain visible rather than being treated as verified procurement. Exact priced observations can be stale by ordering time.

**Supply holds:** L301 has indexed zero stock/backorder; L6340603HC-47NXJRW is a documented current manufacturer configuration with a cut-MOQ1 non-stocked distributor offering and approximately9-week indicated factory lead time. Its€0.75 budget is an estimate, not a EUR quotation. U950's regional inventory caches conflict and require confirmation. The active PD54008 and PHA-1+ baseline sourcing evidence is retained; verify all final suffixes, authenticity, temperature grades and spares before purchase. No broker substitution is assumed.

Bare-board estimate: **five180×140 mm,0.8 mm,2oz two-layer boards:€60–100 net per batch**, shipping approximately€10–25. This is an engineering estimate, not an uploaded fabrication quote or promotion. Production-context estimates per board at6/10/20 are€12/€9/€7, conditional on actual stack-up and panel rules. Obtain a supplier quote after independent review.

External thermal material allowance is€12 net per full board for two independent sinks, spreader, insulation and mounting hardware. A Fischer SK48 50SA comparator was indexed at€3.7128 gross individually/€3.4391 gross at ten, approximately€3.12/€2.89 net using19% German VAT; the remaining hardware is estimated. Harness allowance€3, antenna/feeder€12 are separate. At ten a4S installed-module allowance is therefore€73.03 including€9 PCB,€12 thermal and€3 harness, or€85.03 including the provisional antenna/feeder. Controller, battery/BMS, charging, enclosure and labor are excluded. Training-only does not need PA heat hardware.

The optional driver load is approximately€0.025 plus temporary coax/probes, all estimated and reusable. The26 probe contacts are bare-board features with no separately purchased component cost. RF instruments/dummy loads belong to shared commissioning equipment. Measure actual assembly/alignment time before assigning labor or claiming savings. Manufacturing VAT is jurisdiction-dependent; a19% illustration is not a tax-inclusive procurement commitment.
