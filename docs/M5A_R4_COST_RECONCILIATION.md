# M5A-R4 — cost reconciliation

Dated **2026-10-16**. **M5A-R4 electrical candidate — NOT RELEASED.**
All physical tests are **NOT_RUN**. No purchasing, fabrication, assembly or RF operation has occurred.
RF80, M4A and accepted ADRs are unchanged. R3 is preserved at tag `m5a-r3`
(`daf994c`); R0/R1 tags and the R1 native archive remain available.

The complete candidate basket is **€43.32 for 2S / €42.03 for 4S at ten**. It meets the €40–50 target as an estimate, not as a fully quoted or electrically qualified buildable price. All amounts are net EUR; VAT, PCB, controller, battery, antenna, enclosure and labor are separate.

| Population | 6 units: EUR/board | 10 units | 20 units | Physical parts / ICs |
| --- | --- | --- | --- | --- |
| BOOST2S | 46.41 | 43.32 | 43.21 | 264 / 24 |
| BUCK4S | 44.77 | 42.03 | 41.92 | 260 / 24 |
| TRAIN_ONLY | 11.28 | 11.28 | 11.28 | 103 / 13 |

The RF core—source, driver/final, bias, matching, LPF, AM and indispensable driver rail—is **€24.83 at ten**. It excludes training, controller interface, pack conversion and remaining protection. [Itemized 6/10/20 BOM](../hardware/2m/review/M5A-R4/RF2M_BOM.csv), [population list](../hardware/2m/review/M5A-R4/positions.csv), [ledger](../hardware/2m/review/M5A-R4/costs.json) and [all changed/added/deleted R3 parts](../hardware/2m/review/M5A-R4/component-delta.json) are generated from the implemented manifest.

| Population/fleet | R3 EUR | R4 EUR | Saving | Parts R3 → R4 | ICs R3 → R4 |
| --- | --- | --- | --- | --- | --- |
| BOOST2S/6 | 95.16 | 46.41 | 48.75 | 247 → 264 | 22 → 24 |
| BOOST2S/10 | 93.16 | 43.32 | 49.84 | 247 → 264 | 22 → 24 |
| BOOST2S/20 | 93.16 | 43.21 | 49.95 | 247 → 264 | 22 → 24 |
| BUCK4S/6 | 93.23 | 44.77 | 48.46 | 241 → 260 | 22 → 24 |
| BUCK4S/10 | 91.23 | 42.03 | 49.20 | 241 → 260 | 22 → 24 |
| BUCK4S/20 | 91.23 | 41.92 | 49.31 | 241 → 260 | 22 → 24 |
| TRAIN_ONLY/6 | 16.33 | 11.28 | 5.05 | 102 → 103 | 14 → 13 |
| TRAIN_ONLY/10 | 16.33 | 11.28 | 5.05 | 102 → 103 | 14 → 13 |
| TRAIN_ONLY/20 | 16.33 | 11.28 | 5.05 | 102 → 103 | 14 → 13 |

| Block at ten | 2S EUR | 4S EUR |
| --- | --- | --- |
| am | 1.04 | 1.04 |
| bias | 1.41 | 1.41 |
| connector | 3.00 | 3.00 |
| converter | 3.78 | 2.48 |
| decoupling | 0.77 | 0.77 |
| driver | 3.22 | 3.22 |
| driver_supply | 2.49 | 2.49 |
| input | 1.79 | 1.79 |
| interface | 0.34 | 0.34 |
| interlock | 3.08 | 3.08 |
| modulator | 1.98 | 1.98 |
| output_filter | 2.95 | 2.95 |
| pa | 5.30 | 5.30 |
| pa_match | 3.12 | 3.12 |
| passive | 0.10 | 0.10 |
| power | 0.09 | 0.09 |
| protection | 2.19 | 2.19 |
| source | 2.28 | 2.28 |
| source_filter | 1.04 | 1.04 |
| supply_isolation | 0.56 | 0.56 |
| training | 2.78 | 2.78 |

The entire **€57.60 obsolete bundle** is removed: MRF237 €31.90, 2N4427 €5.90, BF981 €3.00, Neosid modules €15.00 and RF trimmers €1.80. The replacement includes €5.30 final, €2.88 MMIC, actual ST networks, fixed bias and AM servo. It is not a drop-in final in the old match. Lower-cost low-drive RF inductors also replace expensive generic allowances. No filter, training capability or independent fail-off is silently omitted.

## Price evidence and gaps

| Population | Current indexed EUR | Historical observed EUR | Estimated EUR | OPEN MPN/landing amount EUR |
| --- | --- | --- | --- | --- |
| BOOST2S | 12.10 | 0.33 | 30.88 | 9.59 |
| BUCK4S | 10.95 | 0.33 | 30.74 | 9.55 |
| TRAIN_ONLY | 0.41 | 0.00 | 10.87 | 2.44 |

The last column overlaps the first three; do not add it again. An exact proposed MPN does not convert an allowance into a quote. Each BOM row records supplier identifier, quantity, MOQ/multiple, URL, evidence class and unresolved status. Estimated MOQ 1 is not supplier confirmation. Identical MPNs are pooled within each fleet/variant and priced consistently using the highest applicable allowance. No unearned reel discount is booked.

The final's €5.30 cut-tape price is observed. PHA-1+ is €2.88, with no 50-piece break booked for twenty boards. A05T rises from the old €0.55 estimate to €1.28; the low-ESR reservoir is now **€1.50 estimated**, replacing a €0.45 generic allowance. Current converter observations replace carried prices: TPS54302DDCR €0.879 and TPS611781RNWR €2.031 at ten. Most supporting costs remain estimated; see the dated [source log](../hardware/2m/review/M5A-R4/sources.json).

Full purchased count rises from R3's 247/22 ICs to 264/24; training changes from 102/14 to 103/13. Savings are monetary, not a false count reduction. Permission packing removes one IC relative to the unreduced modern implementation. Test pads, PWR_FLAG and transmission-line copper are not purchased components.

## Other installed materials

These are estimates pending the actual outline, stack-up and quote:

| Additional material, EUR/unit | 6 | 10 | 20 |
| --- | --- | --- | --- |
| Two-layer bare PCB | 6.00 | 4.50 | 3.50 |
| RF pigtails/mating harness beyond board connectors | 3.00 | 3.00 | 3.00 |
| Antenna/feed system | 12.00 | 12.00 | 12.00 |
| Sink, insulators and fixings | 7.00 | 7.00 | 7.00 |

At ten the installed RF module allowance is **€68.53 for 4S / €69.82 for 2S**, before controller, pack, charging, enclosure and labor. Board connectors are already in components. PCB allowance is not a promotional quote. One-time engineering/tooling and shared fleet costs remain separate. Assembly, winding, alignment and test labor are unpriced until the first complete build is timed; no fictitious labor saving is assigned.

The retained [M2 battery ledger](M2_BATTERY_COST_COMPARISON.md), dated 2026-10-14, supplies system context. These are its historical observed/estimated mix, including stated protection/keying/qualification allowances, not new quotes:

| Pack/cell basis, EUR | 6 | 10 | 20 |
| --- | --- | --- | --- |
| 2S2P, 2450 mAh class | 15.38 | 15.38 | 15.02 |
| 2S3P, 2450 mAh class | 20.68 | 20.14 | 19.66 |
| 2S4P, 2450 mAh class | 25.98 | 25.26 | 24.62 |
| 4S1P, 2450 mAh class | 18.64 | 18.64 | 18.28 |
| 4S2P, 2450 mAh class | 29.24 | 28.52 | 27.88 |
| 2S2P, M35A | 21.66 | 21.10 | 21.10 |
| 2S3P, M35A | 29.26 | 29.26 | 28.30 |
| 2S4P, M35A | 37.42 | 37.42 | 36.14 |
| 4S1P, M35A | 24.92 | 24.36 | 24.36 |
| 4S2P, M35A | 40.68 | 40.68 | 39.40 |

That ledger separately allocates shared charging/provisioning/freight: 2S €13.50/8.10/4.85 and 4S €14.33/8.60/5.35 per unit at 6/10/20. The older common-controller component allowance is €16.70/14.93/14.83, with its own PCB/enclosure separate. Do not add an entire prior transmitter basket again when using these pack rows. RF80 and reconciled Foxoring accounting are unchanged.
