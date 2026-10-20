# M5B-E6 cost comparison — unquoted concept

The shared-cooler concept removes two extrusions and the old pass spacer, but is **not a completed BOM or a complete-transmitter budget**. [Read-only cost source](../tools/m5b_e6_costs.py), [all populations and quantities](../hardware/2m/review/M5B-E6/population-costs.csv), [cost model](../hardware/2m/review/M5B-E6/cost-comparison.json). EUR net except explicitly labeled gross observations; shipping and destination VAT are separate. No procurement was performed.

Native electrical BOM costs are unchanged. MPN pooling, existing MOQ/multiples and recorded price tiers are recalculated for 1/5/7/10 units. Existing electronics observations retain their original dates; unquoted positions remain estimates. No quantity interpolation masquerades as a supplier tier.

| Units | BOOST2S electrical / unit | BUCK4S electrical / unit | TRAIN_ONLY electrical / unit | E5 cooling / unit | E6 concept cooling / unit |
| --- | --- | --- | --- | --- | --- |
| 1 | €54.92 | €53.35 | €14.18 | €31.11–38.61 | €34.72–40.72 |
| 5 | €54.33 | €52.76 | €14.11 | €31.11–38.61 | €16.65–22.65 |
| 7 | €54.33 | €52.76 | €14.11 | €31.11–38.61 | €15.36–21.36 |
| 10 | €50.27 | €49.03 | €14.11 | €29.80–37.30 | €14.39–20.39 |

Cooling columns apply to NORMAL full-power builds; TRAIN_ONLY omits the PA/modulator and their cooling. The native BOM/populations are preserved, not proposed for substitution. E6 mechanical lines remain unselected at HOLD.

The 21 October source check indexed [SK81](https://www.reichelt.com/de/en/shop/product/heat_sink_100_mm_aluminium_2_2_k_w-227984) at €7.30 gross = €6.134 net, MOQ 1, in-stock indication. [SK10075SA](https://de.rs-online.com/web/p/kuhlkorper/1898088) indexed €16.48 net (1–9), €15.17 (10–24), temporarily unavailable with a forecast date. [KERATHERM 86/82 100 × 100 mm sheet](https://cls-computer.de/cls-hardware/kerafol-86-82-w-rmeleitfolie-0-25-mm-6-5-w-mk-l-x-b-100-mm-x-100-mm-pcs5901102) indexed €22.59 net, MOQ 1 sheet, availability indication. These are displayed/indexed observations, not basket-confirmed quotes or reserved stock. Ten usable 15 × 44 blanks per sheet are budgeted with scrap allowance; the full sheet cash is charged to the units needed. This explains the expensive one-off E6 case. Thermal contact suitability is not established by price/availability.

FK213SA32 €1.50–3, bar €1–2, E5 interfaces €2–4, E6 tab mica/grease €1–3 excluding the source sheet, E5/E6 support hardware €4–7 are **unquoted estimates**, with MOQ/stock unresolved. A qualified direct-ground bar layout could avoid the source sheet, but that is not implemented or booked as a saving. The earlier €12 thermal allowance omitted the subsequently selected SK100 construction; it is historical evidence, not today's complete three-cooler basket.

| Category | E5 | E6 preferred concept |
| --- | --- | --- |
| Separate heatsinks | 3 | 1 required; not yet built |
| Main semiconductor paths | PA→bar→sink; pass→mica→spacer→sink; helper→mica→sink | PA→sheet→bar→same sink; pass/helper→mica→same plane |
| Intermediate stock pieces | Source bar + pass spacer | Source bar; independent cooler support still required |
| Attachment operations | Three cooler alignments, tab insulation and separate supports | One cooler alignment plus two formed devices/insulated tabs; new jig qualification |
| Thermal assembly time | 45–75 min estimate | 25–45 min estimate; unmeasured |
| Labor at illustrative €25/hour | €18.75–31.25 | €10.42–18.75; not measured saving |
| Cooler hardware count | Baseline drawings contain multiple arrangements; full counted assembly BOM not established | Target 2 source clamp +2 tab +4 support screws (8), pending actual support design |
| Volume / mass | Old separate cooler envelopes overlap enclosure allowances; summed volume is misleading; complete mass not measured | Cooler 150 cm³ envelope, bar 4.092 cm³; assembly estimate 245–270 g, enclosure/guard separate |
| Service | Several awkward orientations | Ordinary removable screws and solder access required; not yet validated |

Exact bracket/unique-part/screw counts, torque operations and total E5 mass are not known well enough for a released percentage labor/mass saving. They remain explicit unquoted/unmeasured items.

The model separately includes minimum-five bare-PCB batch allowance €60–100, ordered in five-board lots, and €10–25 shipping per order. For seven required boards it charges ten purchased boards (three leftovers), not a fictional seven-board quote. Enclosure €5–15, consumables €1–3, controller €15–25, RF harness €3–6, antenna/feeder €8–15 and pack/BMS €15–35 are planning estimates; charger/tools, first-article X-ray/RF alignment, rework, freight and tax remain additional. The electrical+PCB+cooler+case subtotal is not a complete transmitter. **Neither €120 nor €150 complete cost is demonstrated.** The fleet concept is economically promising but cannot override the thermal HOLD.
