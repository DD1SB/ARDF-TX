# Revised 80 m consumption and endurance

Date: **2026-10-13**. **Calculated scenarios, not measured compliance.** [Reproducible tables](M2_80M_POWER_TABLES.md) and [numeric ledger](M2_80M_TOTALS.json) use `tools/m2_80m_analysis.py`. The prior [M2 budget](M2_POWER_BUDGET.md) and [Fox audit](FOXORING_COST_AUDIT.md) remain historical baselines. No 2 m power model or hardware selection is changed.

## Power required versus optional capability

The current [IARU Part B](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf), T2.6/S6/FT2.6, allows a common approximately 1 W Classic/Sprint PA. **Exactly 1 W is both Classic's lower boundary and Sprint's upper boundary**, leaving no finite two-sided calibration/measurement margin for one identical setting. Recommend separate settings near **1.2 W Classic and 0.85 W Sprint**, with capability and tolerance verified over 6–8.4 V.2–3 W and 5 W are optional headroom populations, not mandatory championship minima. This amendment needs architectural review; the earlier 5 W objective is retained as an alternative, not silently deleted.

RF power here means **post-filter conducted A1A mark power at 50Ω**, not ERP or field reach. PEP equals mark carrier power for this unmodulated CW signal. We conservatively assume continuous carrier during each scheduled slot and ignore additional Morse spaces:20% scheduled duty for Classic/Sprint, 100% for Foxoring and beacons. Do not apply 20% duty to spectator/finish beacons or to continuously coded Foxoring.

## Inputs and evidence classes

| Input, battery-input power unless stated | Value | Evidence / scope |
| --- | --- | --- |
| Controller/RTC/sensing, Wi-Fi off during contest | 0.120 W | Preserved M2 engineering allowance; includes controller regulator losses. Not an ESP32-S3 measured operating mode. |
| RF module/common standby, guard/lease/latch, references, regulator leakage and BMS reserve | 0.020 W | Engineering allowance. Source/driver/PA rails are off between slots. Exact idle current remains NOT RUN. Extra installed inactive 2 m board adds the preserved 0.010 W sensitivity. |
| Active Si5351/reference/quiet feed | 25 mA×3.3 V /0.90 =0.0917 W | Assumed whole source current and 90% quiet-feed efficiency, not measured single-output low-frequency consumption. Crystal itself passive. Source startup time/energy must be measured. |
| Economy PA efficiency | 55% Classic, 50% Sprint | Assumed **PA feed-rail input upstream of the shaper to post-filter RF**, including shaper/base-network/filter loss, excluding separately counted gate driver. SignalSlinger publishes voltage/power, not this efficiency. |
| Economy normal buck | 90% | Assumed efficiency. TPS62160's 17 µA typical IQ is a datasheet fact, not the full system's idle current or 90% proof. |
| Active driver allowance | 0.220 W economy; 0.400 W higher-power | Assumed dynamic gate-drive plus driver static loss. Gate charge varies with voltage/drain swing; input capacitance alone is not an adequate current calculation. |
| Higher-power conversion | 85% boost ×90% adjustable buck =76.5% | Assumed boost+LTC3600 chain. Higher-power gate driver is upstream of the variable buck and gets 85% conversion, not the double-converted rail. |
| Higher-power PA efficiency | 60% | Assumed shaper/filter-inclusive value. ON7YD's 61/65% observations use another topology, fixed 12 V driver and specific loads; not transferred as measured IRF610 efficiency. |
| Foxoring RF conversion / small shaping overhead | 25% /0.015 W | Conservative tentative buffer/pad conversion plus overhead; no watt boost or driver. Current-limit/clamp/shaping behavior still open. Source/controller remain active. |
| Optional LoRa | +0.006 W at 10% listening; +0.045 W continuous receive | Preserved assumptions; includes standby/listening distinction. Exact Silicontra variant/TCXO/RF switch and measured currents OPEN. TX burst adds about 0.44 W transient allowance, not a verified module measurement. |
| Battery usable-energy factors | 80% aged capacity ×90% operating window ×90% temperature =64.8% | Planning margins; not actual Samsung cycle/cold/discharge data. No double subtraction of regulator losses from usable battery Wh. |

Two cell cases are retained: **audited 25R conservative 2.45 Ah/cell**, and previous **3.4 Ah reference**. Nominal 2S voltage 7.2 V gives **11.431 Wh usable per parallel string** for 2.45 Ah and 15.863 Wh for 3.4 Ah.1P/2P/3P/4P mean-power ceilings for 24 h are **0.476/0.953/1.429/1.905 W** or 0.661/1.322/1.983/2.644 W respectively. Supplier 25R tab/cell prices and protection qualification remain in the completed audit; “20 A cell rating” does not qualify our pack fuse/BMS/wiring.

The calculation is:

```text
Pmean = 0.140W + duty × [P_RF / (eta_PA × eta_conversion)
                       + P_driver / eta_driver_conversion + 0.0917W]
Eusable = 7.2V × cell_Ah × parallel_count × 0.648
runtime = Eusable / Pmean
```

## Principal results

| Normal profile | Mean W /24 h Wh | 2.45 Ah pack, smallest modeled pass | 3.4 Ah pack, smallest modeled pass |
| --- | --- | --- | --- |
| Classic 1 W comparison | .611 /14.67 | 2P, 37.4 h | 1P, 25.9 h |
| **Classic 1.2 W preferred** | **.692 /16.61** |**2P, 33.0 h** |**2P, 45.8 h** |
| Classic 2 W | 1.124 /26.97 | 3P, 30.5 h | 2P, 28.2 h |
| Classic 3 W | 1.560 /37.43 | 4P, 29.3 h | 3P, 30.5 h |
| Classic 5 W | 2.431 /58.35 |**No 1P–4P pass**; 4P18.8 h | 4P, 26.1 h |
| Sprint 0.85 W |.588 /14.11 | 2P, 38.9 h | 1P, 27.0 h |
| Sprint 1 W comparison |.652 /15.64 | 2P, 35.1 h | 1P, 24.3 h; continuous LoRa RX pushes to 2P |
| **Foxoring 10 mW continuous** |**.293 /7.03** |**1P, 39.0 h** |**1P, 54.2 h** |

Smallest modeled pack is not a qualified minimum. At 1.2 W the 2.45 Ah 1P model needs almost 99% shaper/filter-inclusive PA efficiency with the other allowances held fixed, so do not promise the cheapest 25R1P for Classic. A 3.4 Ah 1P would need about 59% efficiency and tight controller/LoRa control; measurement could justify it, but the conservative recommendation remains 2P.5 W imposes both higher supply material and a larger high-capacity pack; the cheap 25R4P still fails the modeled 24 h requirement.

Relative to the audited 25R 2S1P pack, two additional tabbed 25R cells in a 10-unit 2P fleet add about€4.70 plus pack restraint/insulation.3P/4P add four/six cells plus mechanical material. Larger fleets reach only **observed** quantity breaks:40 cells at ten 2P packs still use the 25R ten-cell price; 80 cells at twenty 2P packs reach the 50-cell tier. Capacity, pack protection and sourcing may dominate the small RF-silicon saving. An unavailable 35E listing is not a procurement solution.

The new Fox model is lower than the audited 0.350 W assumption because it separately models a small buffer and clock rather than retaining the old overhead allowance. **This is an estimate revision, not measured energy savings.** Keep the audit's 0.350 W qualification budget:2.45 Ah 1P32.7 h, or 28.9 h with continuous LoRa RX. A measured mean below 0.476 W is still necessary for 24 h with those usable-energy margins.

## Continuous beacons, peaks and sensitivity

Continuous 1.2 W mean input is 2.900 W:4P lasts **15.8 h with 2.45 Ah**, 21.9 h with 3.4 Ah. Continuous 5 W mean 11.596 W gives **3.9/5.5 h** on 4P. Separate spectator/finish frequencies and service duration must be planned; no 24 h full-power-beacon promise or larger-than 4P pack is introduced. A continuous Sprint setting must also be measured separately; at 0.85 W it would average about 2.38 W and still miss 24 h on 25R4P.

Calculated active currents at 6 V are about 0.48 A for 1.2 W, 0.84 A for 2 W, 1.21 A for 3 W and 1.93 A for 5 W; Fox about 0.05 A. The table's **0.85/1.38/1.93/3.02 A** respective peak provisions are 1.5× calculated active current plus 0.12 A assumed controller/transient allowance, **not measured converter startup peaks**. LoRa TX adds about 0.073 A at 6 V. Supply current limit, inrush, converter switches, winding saturation and actual BMS/connector drop require oscilloscope/current logging; do not size protection from average current alone.

Always-receiving LoRa and an installed inactive VHF board can move a near-boundary pack result. Controller input rising from 0.120 to 0.300 W adds 4.32 Wh/day. For 1.2 W with PA 40% and buck 85%, keeping the other allowances gives about 0.917 W mean:25R2P only 24.9 h before LoRa, and continuously listening LoRa makes 2P fail. Recalculate from measured inputs rather than calling nominal efficiencies a 24 h pass. Solar heating, aging, cold and mismatched cells remain hardware qualification variables.

No new nonlinear or power-converter simulation was run. The earlier ideal passive filter simulation is preserved and applies only to that previous seven-pole network; it says nothing about the reference transformer's efficiency, this LPF's real loss, battery life or field range.
