# M5A-R1 — itemized cost comparison

Date: **2026-10-15**. **M5A-R1 electrical evaluation candidate — NOT RELEASED. All physical tests NOT_RUN.**

These are **provisional net EUR component allowances**, not completed supplier quotes or a release ordering list. R0 accounting is preserved. The lower-cost R1 basket includes source, filters, training, AM, converters, enable/protection and board connectors. Unretrieved ST matching is **not** credited with imagined component savings: interim tuning/matching allowances remain. Actual ST network reconstruction may change them.

## Function-normalized baskets, EUR per board

| Complete basket | 6 | 10 | 20 |
| --- | --- | --- | --- |
| R0_2S | 74.61 | 74.61 | 74.61 |
| R0_4S | 72.77 | 72.77 | 72.77 |
| R1_2S_PHA1 | 54.41 | 52.63 | 52.63 |
| R1_4S_PHA1 | 52.48 | 50.70 | 50.70 |
| R1_2S_PHA13_strong | 67.08 | 65.43 | 65.43 |
| R1_4S_PHA13_strong | 65.15 | 63.50 | 63.50 |
| R1_training | 16.37 | 16.37 | 16.37 |


Quantity-ten 2S savings are **€21.97 /29.5%**; 4S saves **€22.06**. Training remains €16.37. The approximately €36 target has **not** been achieved, and even €45–50 is not established for the 2S implementation.

The conservative PD54008/PHA13 counterfactual includes the 8 V buck, its RC components and corresponding OV threshold, with 10 V upstream for **both** RF profiles. Its driver cannot run from the preferred 5 V LDO or 7.5 V reduced rail. Only the economical design is implemented in native KiCad. The counterfactual is a complete cost basket for review, not a second secretly qualified circuit; reduced-profile heat/endurance must be recalculated if selected.

## Actual component/count change

| Population | R0 physical/IC | R1 physical/IC | q10 component delta |
| --- | --- | --- | --- |
| BOOST2S | 267/23 | 264/23 | €-21.97 |
| BUCK4S | 263/23 | 258/23 | €-22.06 |
| TRAIN_ONLY | 104/14 | 104/14 | €+0.00 |


Test pads, flags and footprint assignments are not purchased ICs. Removed driver L303, C408, R406, R407; replaced U303 with a fixed LDO and added reverse-discharge D309. Removed 4S threshold R830/Q801 because 10 V can be supported near 12 V input. Safety IC count remains unchanged; no independent function is deleted to manufacture a saving. Exact changes, including values/pins, are in [component-delta.json](../hardware/2m/review/M5A-R1/component-delta.json).

## Functional block totals, preferred 2S population

| Functional block | q6 | q10 | q20 |
| --- | --- | --- | --- |
| am | 1.04 | 1.04 | 1.04 |
| bias | 1.43 | 1.43 | 1.43 |
| connector | 3.00 | 3.00 | 3.00 |
| converter | 4.09 | 4.09 | 4.09 |
| decoupling | 0.81 | 0.81 | 0.81 |
| driver | 3.82 | 3.82 | 3.82 |
| driver_supply | 1.62 | 1.49 | 1.49 |
| input | 1.80 | 1.79 | 1.79 |
| interface | 0.35 | 0.34 | 0.34 |
| interlock | 3.12 | 3.12 | 3.12 |
| modulator | 1.90 | 1.90 | 1.90 |
| output_filter | 5.43 | 5.43 | 5.43 |
| pa | 7.32 | 5.68 | 5.68 |
| pa_match | 2.73 | 2.73 | 2.73 |
| passive | 0.10 | 0.10 | 0.10 |
| power | 0.33 | 0.33 | 0.33 |
| protection | 2.08 | 2.08 | 2.08 |
| source | 2.28 | 2.28 | 2.28 |
| source_filter | 2.98 | 2.98 | 2.98 |
| supply_isolation | 0.56 | 0.56 | 0.56 |
| training | 7.65 | 7.65 | 7.65 |


The necessary fuse correction adds €0.30 against the old €0.20 estimate; no actual supplier saving is implied. The remaining costs include €7.65 training circuitry, €5.43 normal harmonic filter, €2.98 source filter, €4.09 main boost, €2.73 provisional matching, €1.43 bias, €2.94 AM/pass functions and €3 connector allowance. These are complete functions, not just silicon. RF magnetics and exact RF capacitor/current/Q ratings remain unquoted; do not replace them with arbitrary cheap parts. A simpler verified ST filter could save material, but no saving is booked before its circuit is traced.

## Supplier evidence and MOQ

| Item | Supplier/order identifier | Observed display / availability | Accounting |
| --- | --- | --- | --- |
| PD54008L-E | [DigiKey IT](https://www.digikey.it/de/products/detail/stmicroelectronics/PD54008L-E/1038978),497-6471-1-ND | Net €7.32/5.677/5.266 at 1/10/25; indexed 1988 stock, last-month crawl | q6 uses 1-break, q10/20 uses 10-break; CT MOQ1, not 3000-reel MOQ |
| PD54008L-E alternate | [Mouser DE](https://www.mouser.de/de/ProductDetail/STMicroelectronics/PD54008L-E?qs=sGAEpiMZZMsPo2fL1zXfdqEwePZnwSUq%2Fv1gNDbGsv4%3D),511-PD54008L-E | Display≈€5.30 at 10; locale/tax/stock need checkout confirmation | Alternative observation, no unverified lower net cost booked |
| PHA-1+ | [Mouser EU](https://eu.mouser.com/en/ProductDetail/Mini-Circuits/PHA-1%2B?qs=xZ%2FP%252Ba9zWqYz5cEhj1ZlVg%3D%3D),139-PHA-1 | Display €2.82 at 1, €2.11 at 50; CT MOQ/multiple 1, indexed 4662 stock, two-day crawl | Provisionally held as net; no unsupported 10/20 break |
| TLV76150DCYR | [DigiKey DE](https://www.digikey.de/en/products/detail/texas-instruments/TLV76150DCYR/18115428),296-TLV76150DCYRCT-ND | Net €0.47/0.334 at 1/10, indexed 8483; page has marketplace flag | No stock guarantee; direct-distributor fulfillment/freight must be reconfirmed |
| Other positions | Per-reference CSV | R0 historical observations/family allowances and estimates | No new verified basket invented; exact MPNs/geometry marked OPEN |

Sources were reviewed 2026-10-15. Indexed stock is not a current cart reservation. Cut tape is chosen; no reel conversion/reeling fee assumed. Do not buy 25 finals to obtain its price for 20 boards unless leftover inventory is separately approved/accounted. All prices exclude VAT; illustrative 19% VAT is applied once to the taxable total, not selectively deducted from uncertain display prices. Freight/fees remain separate.

The [actual R1 BOM](../hardware/2m/review/M5A-R1/RF2M_BOM.csv) gives every fitted line at 6/10/20 with MPN/value/footprint, pooled demand, MOQ, multiple, source, supplier identifier, stock qualification and evidence class. [All four required function-normalized baskets](../hardware/2m/review/M5A-R1/comparison-baskets.csv) are also itemized.36 preferred 2S MPN positions remain OPEN; quotations and physical qualification are still required. A numeric allowance for an OPEN position is explicitly an estimate, not a sourced component.

## Materials outside the component total

At 6/10/20, use the same unquoted bare-board allowance €2–6/module until coupon stack-up/area is known; no promotional fabrication claim. Add external RF harness €2–4, antenna/feed €8–15, thermal/insulation €8–14. Board connectors are already counted. Thus installed module allowance is components **+€20–39**, excluding labor/enclosure/controller/pack. Changed thermal expectations can consume part of the board saving; the former €4–7 cooling allowance is not assumed qualified.

For supply comparison, reuse **historical** M5/M2 cell prices, not new observations. Six tagged M35A cells at 6/10/20 fleets cost €22.68/22.68/21.72; estimated 2SBMS €3 and insulation/interconnect €3 give 2S3P material €28.68/28.68/27.72. Eight cells plus 4SBMS €4.50 and interconnect €3 give 4S2P €37.74/37.74/36.46. These are a separate illustrative pack scope; the more detailed M2 pack model uses different mechanical allowances and is not silently rewritten.4S's €1.93 board saving is less than the approximately €9 pack increase if eight rather than six cells are needed. Equal-cell packs have equal nominal energy; chemistry, pack state and cutoff determine accessible energy.

At quantity 10, full 2S material with the illustrative 2S3P pack, €15–20 shared controller and €3–6 enclosure is approximately €119.31–146.31, before labor, fleet charging, freight or shielding. This remains a budget; no completed transmitter cost is implied. Optional shield material €1–3 is separate and conditional. One charger per four units is the retained M5 fleet-turnaround estimate:6/10/20 need 2/3/5 chargers at estimated €15 (2S)/€20 (4S) each; this shared equipment is not charged inside each PCB BOM. No tooling/provisioning/labor is disguised as purchased unit material. The Foxoring-only 80m audit is untouched and is not reinterpreted as this VHF training cost.
