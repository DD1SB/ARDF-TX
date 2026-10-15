# M5A-R3 — candidate BOM and economic result

Dated 2026-10-15. **PRIVATE CONSTRUCTION DERIVATIVE / NOT RELEASED. All ARDF-TX hardware tests NOT_RUN.** No orders, PCB fabrication, assembly or transmission. M5A-R1 remains the archived fallback; RF80, M4A, the controller and accepted ADRs are unchanged.

**The low-cost replacement objective is not achieved.** At10 units the conditional full2S allowance is€93.16net, not€36 or€52.63. This is not a supplier-quoted buildable basket. MRF237/2N4427 listing manufacturers are unresolved; five adjustable coils are unquoted. No fictitious discounts or labor savings are booked.

| Population | 6 boards, EUR/unit | 10 boards | 20 boards | Physical parts / IC |
| --- | --- | --- | --- | --- |
| BOOST2S | 95.16 | 93.16 | 93.16 | 247 / 22 |
| BUCK4S | 93.23 | 91.23 | 91.23 | 241 / 22 |
| TRAIN_ONLY | 16.33 | 16.33 | 16.33 | 102 / 14 |


[Itemized6/10/20 BOM](../hardware/2m/review/M5A-R3/RF2M_BOM.csv) contains every fitted physical reference, exact/OPEN MPN, footprint, pooled demand, purchase-quantity allocation, MOQ/multiple, supplier identifier, price class and note. [Master positions](../hardware/2m/review/M5A-R3/RF2M_positions.csv) additionally shows DNP/test/declaration positions. Test pads/PWR_FLAG are not ICs or separately purchased components. Optional5.6p original correction is excluded from fitted totals and adds€0.10 allowance if fitted.

| Block, full2S at10 | EUR/unit |
| --- | --- |
| connector | 3.00 |
| interface | 0.34 |
| source | 2.28 |
| decoupling | 0.81 |
| interlock | 3.28 |
| passive | 0.10 |
| input | 1.79 |
| supply_isolation | 0.64 |
| converter | 4.09 |
| protection | 2.00 |
| power | 0.12 |
| am | 1.04 |
| training | 7.65 |
| source_filter | 3.14 |
| reference_rf | 60.44 |
| modulator | 2.44 |


RF core cost drivers: MRF237 unbranded comparator€31.90;2N4427 unbranded comparator€5.90; Philips BF981 pack5,€3/unit at10; five Neosid adjustable coils **estimated€15 total**; two RF trimmers estimated€1.80 plus chokes/passives. The remainder includes complete programmable source, PWM/audio, training output, power conversion, ports and independent shutdown—not a bare PA comparison.

At10 the evidence split is€3.00 supplier-listed Philips BF981 with stock-count confirmation OPEN;€37.80 current **manufacturer-unmatched** price comparators;€52.36 estimates. None is a reservation or checkout quote. The actual RF-device purchase may cost differently or be unavailable. Dönberg's global€50 minimum is met by these fleet baskets, but it does not prove stock. Six transmitters need ten BF981 from five-piece packs; the four spare devices are fully allocated to the six-unit materials price, explaining€2/board difference. No discounts at20 are assumed.

## Before/after at identical functional scope

| Population | Fleet | R1 EUR | R3 EUR | Increase EUR | Parts R1→R3 | IC R1→R3 |
| --- | --- | --- | --- | --- | --- | --- |
| BOOST2S | 6 | 54.41 | 95.16 | +40.74 | 264→247 | 23→22 |
| BOOST2S | 10 | 52.63 | 93.16 | +40.52 | 264→247 | 23→22 |
| BOOST2S | 20 | 52.63 | 93.16 | +40.52 | 264→247 | 23→22 |
| BUCK4S | 6 | 52.48 | 93.23 | +40.74 | 258→241 | 23→22 |
| BUCK4S | 10 | 50.70 | 91.23 | +40.52 | 258→241 | 23→22 |
| BUCK4S | 20 | 50.70 | 91.23 | +40.52 | 258→241 | 23→22 |
| TRAIN_ONLY | 6 | 16.37 | 16.33 | -0.04 | 104→102 | 14→14 |
| TRAIN_ONLY | 10 | 16.37 | 16.33 | -0.04 | 104→102 | 14→14 |
| TRAIN_ONLY | 20 | 16.37 | 16.33 | -0.04 | 104→102 | 14→14 |


R0 quantity-ten2S€74.61/4S€72.77, R1€52.63/€50.70, and R2's incomplete provisional module bridge€66.40 are historical candidate allowances, not validated prices. R3 costs more than all three. R2 never produced a new schematic/PCB. No new Mitsubishi pricing study was undertaken.

247 fitted positions and22 ICs compare with264/23 in R1 full2S. The RF-only replacement reduces an MMIC and its supply, but old power semiconductors and adjustable components dominate price. Common VHF logic uses six HC gate/register packages plus the small final gate, watchdog and POR—not a second contest processor. Existing VHF fail-off is retained rather than copying RF80's monostable system. The training population changes only unused normal inputs/terminations and keeps its independent RF branch; see [component delta](../hardware/2m/review/M5A-R3/component-delta.json).

Removing the€31.90 final entirely would still leave approximately€61.26; removing its cost **and all five€3 coil allowances** leaves€46.26. To match R1's€52.63, the final plus all five coils would have only€6.38 combined. That is a transparent quote threshold, not a claim that such a price exists. Cheaper unknown MRF237 clones or invented coil substitutions are not the solution.

## Complete installed module scope

These additional **estimates**, not quotes, remain separate:

| External material per module |6|10|20|
| --- | --- | --- | --- |
| Two-layer bare PCB allowance, outline not designed |€6.00|€4.50|€3.50|
| External RF harness/strain relief, beyond board connectors |€3.00|€3.00|€3.00|
| Antenna/feed hardware allowance |€12.00|€12.00|€12.00|
| Heat sink, insulation, mounting allowance |€7.00|€7.00|€7.00|
| Full2S installed module including above |€123.16|€119.66|€118.66|

Bare-board numbers are planning placeholders because no qualified R3 layout/size exists; they are **not fabrication estimates from Gerbers**. Heat allowance does not establish thermal adequacy. Board RF connectors are already in component totals and not charged twice. Training-only excludes normal heat/supply/antenna hardware; add its own PCB, low-power antenna and harness, none of which has a current quote.

Controller, external protected battery/BMS, pack wiring, enclosure, charger/shared infrastructure, freight and labor are excluded from these module totals and remain separate system costs in [M2 battery cost](M2_BATTERY_COST_COMPARISON.md). Example controller€18/enclosure€5 allowances would add€23 before battery/charger. No complete finished transmitter price is claimed. Assembly/winding/alignment/testing minutes remain unknown; this historically proven circuit has **seven RF adjustments**, so lower labor than R1 cannot be asserted without evidence.

All values EUR net. Dönberg pages display23%VAT and state EU private-customer conditions; actual German checkout/OSS treatment must be confirmed. No universal19% addition or unsupported gross-to-net conversion was used. Freight, import and quotes remain OPEN.
