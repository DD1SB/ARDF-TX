# M2 80 m architecture review recommendation

Date: **2026-10-13**. **Proposal for review; no hardware gate passed.** The completed comparison covers actual ON7YD, FlexFox80 and SignalSlinger IRF610 circuits, DF1FO Classic/Sprint and TinyFox/Fixle drawings/BOMs. Reference hardware was inspected read-only, including original PCB layouts. No ARDF-TX PCB, Gerber, purchase, fabrication or full firmware implementation was produced.

Recommend the **SignalSlinger / FlexFox80 Si5351–LM5134B–IRF610 bifilar-transformer RF core and its original two-inductor elliptic filter**, with the common ESP32-S3/RTC controller. Prefer **1.2 W Classic and 0.85 W Sprint** as separately calibrated settings on one normal PA. This addresses the actual championship minimum without imposing 5 W power conversion on every unit. Preserve 2–3 W and 5 W as separately costed supply/population alternatives. [ADR-0010](decisions/ADR-0010-proven-80m-core-and-power-target.md) proposes the required amendment; earlier accepted decisions are not overwritten.

Use a normal-only 2S-to-approximately-5.5 V buck and the documented **QCX integrator shaping mechanism** as the economy candidate. The reference's typical 1 W at 5 V is an evidence anchor, not our measured 1.2 W guarantee. LM5134 **B** matters: its TTL thresholds accept 3.3 V; the cheaper A variant does not reliably do so at these supply rails. Driver suffix/stock, minimum-input headroom, loaded gate drive and shaper SOA remain open.

For Foxoring, evaluate **TinyFox's three parallel HC00 buffer gates driven by a second output of the same local Si5351**, on the existing RF PCB with its own bounded rail, LPF/pad, power detector/guard and protected compact port. The watt PA, driver and converter are DNP in Fox-only assemblies. Keep the existing BJT-buffer population as the fallback if the logic version fails 10 mW, shaped edges or silence. Foxoring key shaping and input backpower are explicit unresolved adaptations. Preserve the independent approximately 30 cm radiator, compact counterpoise and loading/coupling cartridge; a Classic wire at reduced power is not a substitute.

| Candidate component scope; EUR ex VAT/unit | 6 boards | 10 | 20 |
| --- | ---: | ---: | ---: |
| Preferred full 80 m module, both antenna paths | 22.41 | **19.76** | **19.68** |
| Fox-only RF population, including 0.75 guard reserve | 9.40 | 8.50 | 8.44 |
| Higher-power core with boost/variable buck | 35.48 | 30.86 | 30.79 |

At ten, the preferred board is **€3.57 below the old M2 €23.33 proposal**. Only €8.59 is observed-price material; €11.17 remains estimated. A 50% increase in those estimates gives €25.34. Native bare-core prices of €5–10 omit functions supplied elsewhere; restoring them gives the DF1FO adapted allowance €19.68 versus €19.76 preferred, too small a difference to justify its unresolved 50 Ω adaptation and limited power growth. This is the lowest-cost reviewed candidate with concrete programmable IRF610/50 Ω reference evidence, not a proven global price minimum.

The completed Fox audit remains **€55.24 / €55.20 unit material**, or **€63.34 / €60.05 with shared fleet charging/provisioning/freight at 10/20**. The tentative simpler population gives €55.07 / €55.04 and €63.17 / €59.89, saving only about €0.17. Keep the audited working budget until the proposed deletions pass tests. Batteries, enclosure, two fabricated PCBs, wiring and compact matching dominate the remaining cost; no large additional saving was established. An illustrative 1.2 W unit with long antenna and protected 25R 2S2P is about €74.60 in materials at ten, excluding labor and shared infrastructure.

| 24 h normal profile | Smallest modeled 2.45 Ah pack | Smallest modeled 3.4 Ah pack |
| --- | --- | --- |
| Classic 1.2 W | 2S2P, 33.0 h | 2S2P, 45.8 h |
| Classic 2 W | 2S3P, 30.5 h | 2S2P, 28.2 h |
| Classic 3 W | 2S4P, 29.3 h | 2S3P, 30.5 h |
| Classic 5 W | None through 4P | 2S4P, 26.1 h |
| Sprint 0.85 W | 2S2P, 38.9 h | 2S1P, 27.0 h |
| Foxoring 10 mW continuous | 2S1P | 2S1P |

No row is a measured endurance pass. Retain the Fox audit's conservative 0.350 W allowance: 25R 1P about 32.7 h before LoRa. Full-power continuous beacons require separate service planning; even the 1.2 W beacon misses 24 h on 4P in this model.

Principal risks are low-voltage PA capability, real harmonic suppression, CW shaping on both paths, Fox buffer backpower/power bound, passive component/winding availability, shaper SOA, compact tuning and 30/250 m reach, exact driver stock, and unmeasured efficiencies. Shared equipment must measure loaded power, spectrum, keying, faults, thermal stress and field behavior; simulations cannot close those gates.

**GO:** architectural review and specification of shared RF evaluation coupons. **NO-GO:** complete product layout, ordering/manufacture, a transmitter fleet or declaring compliance. [H0–H9](M2_80M_VALIDATION_GATES.md) remain NOT RUN. User decisions required: accept the near-1 W standard target amendment; choose whether higher-power population is needed in the first evaluation; approve the bounded-buffer experiment/fallback and retained audit budget; establish intended beacon service duration and instrument access before physical evaluation. The three-PCB, optional LoRa, RTC, protected-pack and isolated-port decisions remain unchanged; the 2 m architecture is outside this review.

Detailed evidence: [reference comparison](M2_80M_REFERENCE_COMPARISON.md), [annotated topology](M2_80M_RF_TOPOLOGY.md), [cost comparison](M2_80M_COST_COMPARISON.md), [power assumptions](M2_80M_POWER_COMPARISON.md) and [validation gates](M2_80M_VALIDATION_GATES.md).
