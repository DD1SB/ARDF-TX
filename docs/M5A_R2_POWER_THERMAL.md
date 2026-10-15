# M5A-R2 supply, thermal and endurance review

2026-10-15. **Planning calculations only. No supply, bias, heat or runtime measurement exists. No R2 power circuit has been released or implemented.** Inputs/results are reproducible with `python3 tools/m5a_r2_review.py`.

## Supply consequences

RA07 requires a bounded supply around its characterized 7.2 V point. **Never connect 4S directly.** A 4S buck has useful headroom over the 12.0–16.8 V pack window. Final setpoint, tolerance, local overvoltage threshold, disconnect response and effective reservoir capacitance must be designed together. A nominal 7.2 V setting is not a worst-case bound. The conditional drain/gate ratings in the [manufacturer datasheet](https://www.mitsubishielectric.com/semiconductors/hf/products/datasheet/ra07m1317m.pdf) must be retained; its off-state 12 V rating is not an active-RF operating permission.

Direct 2S spans 6.0–8.4 V and cannot be called a calibrated constant-power 7.2 V supply. At low voltage the available crest can fall; at full charge current/heat and gate-bias conditions change. Mitsubishi's portable-battery application and 9.2 V tests are useful evidence, but do not guarantee our linear-AM envelope throughout that window. Direct 2S therefore remains unqualified rather than declared impossible.

A boost alone cannot regulate **7.2 V below an 8.4 V input**. The R1 TPS611781 boost cannot simply be retargeted to 7.2 V. A regulated 2S RA07 solution needs buck-boost, a higher rail followed by a drop, or a documented restricted-voltage profile. None is selected merely to make a table pass. The 2S energy rows below assume 87% net regulation and are explicitly conditional on a valid economical circuit. RA08N's 9.6 V alternative can use boost from 2S and buck from 4S, but has a different bias/thermal model. It remains a sourcing alternative, not a second PCB design.

Battery protection and charging remain external. Pack identity, incompatible-rail lockout, fuse/inrush coordination, reverse polarity and independent RF rail OV/OC/thermal shutdown are still required. The old 1.8 A R1 trip cannot be copied blindly: this model estimates about 1.98 A at the full envelope crest, before reservoir/inrush uncertainty. A future threshold must stay compatible with the module's 3 A maximum and actual fault energy.

## Explicit model, inherited energy margins

Use fixed drain voltage and input AM, not the old series-pass supply-AM equation:

```text
P_RF_module_mean = ERP × 10^0.1 × 10^(filter_loss/10) × (1+m²/2)
P_PA_DC = VDD × Iq + P_RF_module_mean / eta_dynamic
P_battery_mean = P_controller + P_idle + P_LoRa
                 + duty × (P_PA_DC + P_source_AM) / eta_conversion
E_usable = cell_count × cell_energy × 0.80(age) × 0.90(temp) × 0.90(endpoint)
```

`eta_dynamic` excludes the separately added quiescent draw. These efficiencies are **not Mitsubishi's saturated/FM efficiency**. Base assumptions: 7.2 V, Iq=0.30 A, full dynamic efficiency 40%, reduced 28%, output loss 0.75 dB, controller 0.14 W, RF idle 0.04 W, active source/modulator 0.15 W, duty 20%; no Morse discount. Conversion 87% conditional 2S/91% 4S. Idle covers powered safety/sensing with converter, source and main module off. Leaving PA bias or PREPARE on between slots invalidates the budget.

Inherited cell energy: conservative 2.45 Ah/25R 8.82 Wh and M35A **minimum 11.9 Wh** per cell. Capacity tests end at 2.5 V; the 0.90 provision to a 3.0 V endpoint is unmeasured. No extra discharge-curve energy is claimed. See the [existing cell model and provenance](M2_ENDURANCE_REWORK.md). Different cells' current capability, resistance and cold behavior are not treated as equivalent.

| Base case, m=80% | 2S regulation, conditional | 4S buck, conditional |
| --- | ---: | ---: |
| Full 1 W ERP mean battery power | 1.846 W | 1.773 W |
| Energy for 12 h full | 22.15 Wh | 21.27 Wh |
| Reduced 0.30 W ERP mean | 1.197 W | 1.153 W |
| Energy for 24 h reduced | 28.74 Wh | 27.67 Wh |

| Pack | 25R modeled full/reduced h | M35A modeled full/reduced h | Interpretation |
| --- | ---: | ---: | --- |
| 2S2P | 12.38 /19.09 | 16.71 /25.76 | M35A arithmetic targets only; reduced margin is small; 2S circuit OPEN |
| 2S3P | 18.58 /28.64 | 25.06 /38.64 | 25R misses illustrative 20% reduced reserve; 2S circuit OPEN |
| 2S4P | 24.77 /38.18 | 33.42 /51.52 | Larger conditional energy margin |
| 4S1P | 12.90 /19.83 | 17.40 /26.76 | Four M35A cells are a plausible minimum; not robust 24 h qualification |
| 4S2P | 25.79 /39.66 | 34.80 /53.51 | Smallest 4S case with modeled 20% reserve for both cell classes |

Equal-cell 2S2P/4S1P and 2S4P/4S2P have equal energy. Differences above come from assumed conversion, not extra energy. All rows are **NOT_RUN**, not compliance passes. [Full 75/80% table and continuous beacons](../hardware/2m/review/M5A-R2/endurance.csv) are separate. For M35A, 4S1P continuous full/reduced beacon is only 3.79/6.12 h; 4S2P is 7.57/12.23 h. Normal contest endurance cannot be advertised for continuous beacons.

## Bias sensitivity and cooling

The [sensitivity sweep](../hardware/2m/review/M5A-R2/sensitivity.csv) varies Iq=0.15/0.30/0.75/2.0 A, efficiency=25/40/50%, controller=0.14/0.28 W and LoRa=absent/0.006 W listening/0.045587 W continuous-receive-plus-bursts. These are whole-system provisions. Optional LoRa remains fully omittable; no measured Silicontra current is invented.

The RA07 typical curves at VGG=3.5 V show roughly 2 A at small input. **Do not set VGG=3.5 V as the linear bias by default or credit the 0.30 A budget without testing.** At Iq=2 A the assumed full 4S mean rises to about 4.46 W; eight M35A cells give about 13.8 h full and only 16.1 h reduced. The reduced 24 h target then fails even with the largest permitted eight-cell pack. Linear crest quality and low idle current must coexist.

Base active module heat is approximately 5.12 W full AM and 3.68 W reduced; fixed bias dominates the reduced setting. At 45°C ambient, a 10 W cooling provision and 60°C case target require ≤1.5°C/W total case-to-air including interface. This is a required cooler capability, not a qualified small heatsink. Mounting-flatness/grease/screw instructions and grounded flange contact are essential. Use measured case temperature, sensor offset and shutdown delay; do not reuse the R1 66°C remote-sensor threshold without a new thermal error budget.

The series D45H11/BD139 modulator would disappear in a completed input-AM design, removing its live tab and linear SOA burden. Heat has moved into a fixed-supply, backed-off RF amplifier; it has not disappeared. Actual Iq, DC input, case rise, clean PEP, fault shutdown and accessible battery energy remain physical acceptance gates.
