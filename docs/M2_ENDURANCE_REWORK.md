# M2 endurance rework: reproducible model

Date: **2026-10-14**. **No transmitter currents, efficiencies, discharge curves or runtime have been measured by this project.** These calculations select experiments and expose margins. They cannot pass the RF/endurance gates. The only retained circuit simulation is the earlier ideal-filter analysis; it does not validate these battery, PA or AM calculations.

Run `python3 tools/m2_power_architecture.py --write`, then `--check`. The [script](../tools/m2_power_architecture.py) imports the existing M1 cost catalog, proven-HF comparison and M2 AM envelope function. [Inputs/catalog](M2_POWER_ARCHITECTURE_INPUTS.json), [results](M2_POWER_ARCHITECTURE_RESULTS.json), [readable tables](M2_POWER_ARCHITECTURE_TABLES.md) and [itemized CSV](M2_POWER_ARCHITECTURE_BOM.csv) reproduce the analysis. Old scripts/results remain unchanged.

## Battery energy and operating limits

`E_nominal = cells × 3.6 V × capacity_Ah` for historical reference/25R cases; use the manufacturer's **11.9 Wh minimum / 12.5 Wh typical per cell** for actual M35A cases, slightly below nominal-voltage × Ah.

`E_usable = E_nominal × age_factor × discharge_window × temperature_factor × RF_window`

Default provisions are 0.80 aging, 0.90 window to the assumed 3.0 V/cell endpoint, 0.90 temperature. These are **unverified planning factors**, not manufacturer guarantees. Conversion losses are calculated in load power, not deducted from energy again. Cell/BMS/wiring losses are provisioned within the window/conversion uncertainty; the illustrative I²R example is not an additional deduction. Validate the actual terminal-energy integral and replace these provisions with measurements before asserting endurance.

| Cell basis | Two cells nominal / usable Wh | Four cells usable Wh | Eight cells usable Wh | Status |
| --- | --- | ---: | ---: | --- |
| 2.45 Ah | 17.64 / 11.43 | 22.86 | 45.72 | Conservative 25R capacity basis, not a measured pack |
| 3.35 Ah | 23.80 / 15.42 | 30.84 | 61.69 | M35A manufacturer minimum basis |
| 3.40 Ah | 24.48 / 15.86 | 31.73 | 63.45 | Retained historical M1/M2 assumption |
| 3.50 Ah | 25.00 / 16.20 | 32.40 | 64.80 | Typical-only sensitivity; not guaranteed selection |

The 0.90 discharge factor provisionally replaces missing cell curves at the selected current/endpoint; it must not be applied again after integrating a measured usable-energy curve. Manufacturer capacity tests end at 2.5 V; capacity at 3.0 V is unknown at our loads. Temperature and age are independent scenario allowances, not proven independent physical effects.

Full 4S VHF at a 13.5 V AM supply has an additional **RF_window = 0.65**, provisionally representing operation only above a 14.2 V pack cutoff. This is not an inferred percentage of charge from voltage. Evaluate 0.45–0.85: true energy depends on current, cell type, temperature, imbalance and sag. Reduced VHF/HF use RF_window = 1 down to the separate 12 V planning cutoff. This prevents granting full 3.0 V/cell energy to a design that stops RF earlier.

For full VHF, minimum accessible fraction for 12 h on four M35A cells is `12×2.279/30.845 = 0.887`; the 0.65 scenario fails. Eight 25R cells need fraction ≥0.598; eight M35A cells need ≥0.443, before additional idle/LoRa losses. A lower-crest 12.3 V supply scenario with a 13.0 V input cutoff and RF_window 0.85 yields only 11.6 h on four M35A cells. These thresholds tell us what discharge/headroom measurements must establish.

## Operating states, including idle

| State/input | Assumed battery/load provision | How it is used |
| --- | --- | --- |
| Controller/RTC/monitoring, 2S | 0.120 W battery average | Retained M2 allowance; includes its regulator loss |
| Same controller, 4S | 0.127 W battery average | Allows lower light-load efficiency; not a claimed saving |
| MCU active/idle decomposition | 80 mA / 25 mA at 3.3 V, weighted 10% / 90% | Example operating-state allocation, **not measured ESP32 states**; 0.10065 W mean MCU load |
| RTC/safety/monitor load | 0.00001 / 0.005 / 0.001 W | Allocation totaling about 0.1067 W with MCU; 90%/85% controller conversion gives 0.119/0.125 W, with retained rounding reserve |
| RF board idle | 0.020 W single board; 0.030 W two boards | Hardware lease/latch/sense, disabled-rail leakage, local regulators; initial allowance only |
| Synthesizer/reference on | 25 mA at 3.3 V / 90% quiet-rail conversion = 0.0917 W | Extra during HF scheduled slots; reference/clock current must be measured by output settings |
| Synth off | Included in RF idle provision | Power cut and I²C isolation assumed; confirm leakage and receiver silence |
| HF driver | 0.220 / 0.300 / 0.400 W for ≤1.5 / 2–3 / 5 W RF | Explicit gate/quiescent provision, upstream conversion applied separately |
| VHF source/driver/helper/control | 1.55 W active overhead | Retained M2 provision; already includes source, so no extra Si5351 current added |
| LoRa absent | +0 W | Full autonomous contest functionality |
| LoRa 10% listening | +0.006 W mean | Retained whole-module/MCU wake allowance, not 10% of a bare-chip current alone |
| LoRa continuous receive | +0.045 W mean | Whole-system allowance; exact Silicontra module remains OPEN |
| LoRa TX burst | +0.44 W peak | At assumed 80 ms/min, adds 0.00059 W average; wakes/airtime profile must be specified separately |

Semtech's typical bare-chip receive figure and Micro Crystal's timekeeping figure are primary evidence, but neither specifies the complete populated controller/module current. Silicontra TCXO, RF switch, regulators and firmware wakes can change the total. MCU light sleep is a possible optimization, not credited as a measured power saving. RF trips/lease and timebase must remain functional during sleep.

Classic and Sprint scheduled duty is 20%; no Morse mark-space discount is credited. Synth/driver/PA are powered only during the scheduled slot, including key-up and retuning allowance, with RF envelope hardware-muted during retuning. Model converter warm-up/clock settling inside this provision and test slot-start compliance. Foxoring/beacons use 100%. Slot warm-up, converter pulse-skip, optional LoRa TX or stalled firmware cannot be assumed free.

## HF calculation

`P_mean = P_common_idle + duty × [P_RF/(eta_PA × eta_conversion) + P_gate/eta_gate_conversion + P_source]`

The effective PA efficiency includes shaping/pass loss, RF transistor, transformer and output filter, excluding gate/source. New conservative power bins are 50% at ≤1 W, 55% at 1.2–1.5 W, 60% at 2–5 W; these are **assumptions**, not curves. The earlier near-1 W comparison used 55% for Classic and 50% for Sprint; this rework consistently uses 50% for the same 1 W stage. It also uses a 0.300 W driver allowance at 2–3 W instead of 0.400 W. Neither revision proves an efficiency improvement; both are explicit sensitivity inputs.

Conversion is 90% for one buck, versus 85% boost × 90% adjustable buck = 76.5% for the higher-power 2S alternative. Its gate rail uses the upstream 85% boost separately. At 3 W, total input mean is 1.536 W for 2S high and 1.343 W for 4S buck: **12.6% less input**, equal cells. At 5 W it is 2.431 versus 2.106 W: **13.4% less**. A direct-drain ON7YD alternative may save a buck but varies RF output with voltage and needs separate gate regulation; it has no constant-power/endurance proof.

The 2S comparator supplying LTC3600 must regulate its upstream rail below the manufacturer's **15 V operating ceiling**, including tolerance/transients (nominal 14 V candidate), rather than retain an unsafe 15–16 V setting. The old higher-power proposal remains historical; its price basket is reused, not its unchecked voltage setting.

## VHF calculation and temperature stress

Raw 4S mean-power rows use 14.4 V as an explicitly chosen calculation point, rather than a discharge-curve average. The thermal endpoint sweep includes 12.0/13.5/14.4/16.8 V; 12 V with the retained full crest is an invalid-headroom case. Raw-feed runtimes are provisional point estimates; measured energy/headroom and hot-case behavior must replace them before selecting a smaller pack.

Reuse the existing M2 envelope calculation:

`V_PA = V0 × (1 + m sin(theta))`

`P_carrier_internal = ERP × 10^(1/10) × 10^(0.5/10)`

`k = P_carrier_internal/(eta_dynamic × V0²)`

`I_load = k × V_PA + I_bias`

`P_upstream_mean = V_supply × (k × V0 + I_bias)`

`P_mean = P_common_idle + duty × [P_upstream_mean/eta_supply + P_driver_control]`

The modulator equation includes both PA and pass losses; no guessed fixed modulator efficiency is multiplied into it. Separate 150 mA bias is added only because eta_dynamic describes the voltage-dependent component, not measured total drain efficiency. Envelope-capacitor current is `C×V0×m×2π×800×cos(theta)`, evaluated at 7,200 phases for pass stress; 100 nF is a starting case, not a qualified modulated-rail reservoir. Larger capacitance, negative current and loop dynamics remain existing gates.

Eta_dynamic is 45% at 0.75–1 ERP, 40% at 0.5, 35% at 0.25–0.30. Supply efficiencies are 88% boost / 92% buck, both assumptions. Carrier center/rail choices are documented in [power modes](M2_POWER_MODE_COMPARISON.md); RF gain/matching at each setting remains unknown. The 2S result at full ERP is 2.355 W instead of old 2.345 W because single-board idle provision is now 0.020 W rather than 0.010 W. Reduced-power efficiency is explicitly poorer, and the original bias/driver overhead stays present.

At 0.30 ERP, driver overhead contributes 0.310 W and bias contributes approximately 0.293 W to average 4S input; controller/RF idle adds 0.147 W. Together these account for **56% of 1.343 W**. Lowering radiated power alone does not remove them. An experimental lower-bias/overhead case (50 mA, 0.85 W active overhead) gives 1.007 W and 30.6 h on 4S1P M35A, but AM linearity, gain and hardware safety must pass before crediting that saving.

## Sensitivity and peak current

| Case | Pack | Nominal h | Stress h / implication |
| --- | --- | ---: | --- |
| HF 3 W full | 4S1P 25R | 17.0 | 11.4 at 40% PA / 85% buck: fails 12 h |
| HF 5 W full | 4S1P M35A | 14.6 | 9.6 with same poor conversion assumptions: fails 12 h |
| VHF 1 ERP full, RF_window 0.65 | 4S2P 25R | 13.0 | 11.1 at 35% dynamic conversion: fails 12 h |
| VHF 0.30 ERP reduced | 4S1P M35A | 23.0 | Already fails 24 h; no unmeasured bias saving credited |
| Fox 10 mW | 2S1P 25R | 32.7 | 28.9 with continuous LoRa RX; 21.6 with +0.180 W poor controller idle |
| Sprint 0.5 W extended | 2S1P 25R | 26.6 | 24.1 with continuous RX, 18.8 with +0.180 W poor idle |

The JSON additionally supplies cold factor 0.60, aging factor 0.60 and combined cases for every pack/capacity. At cold factor 0.60 versus default 0.90, usable energy/runtime becomes two-thirds; with age 0.60 versus 0.80 it becomes three-quarters; together one-half. Samsung documents only 60% capacity at−20 °C under its 10 A test; our lower-current performance is unknown. The default 90% temperature allowance cannot support an unrestricted−20 °C endurance claim. Define the actual operating-temperature envelope before release.

Calculated crest/startup provisions (25% transient margin and LoRa burst) are about **2.51 / 4.41 / 6.80 A at 6 V** for HF 5 / VHF 1 / simultaneous full operation; corresponding 4S bounds are **1.08 / 2.12 / 3.14 A at 12 V**. Full 4S VHF is actually inhibited below its higher cutoff, so 12 V is a conservative path-rating case, not permission to transmit the full envelope there. These are external pack-current provisions, not converter inductor peak ratings. Initial qualification limits remain ≥5 A for 2S single-band and ≥7 A simultaneous, and ≥3 A / ≥4 A for 4S respectively, with actual fuse/BMS/cable/connector and cold-cell checks. Capacitor inrush and fault-current time-to-trip need independent measurements.

Output during the entire specified 12/24 h interval must remain at the selected conducted power or installed ERP, with frequency, CW/AM envelope and timing inside limits. Controller survival after RF droop is a failed endurance test. Fixed preselected profiles stop at cutoff; no unreviewed automatic power changes during competition. Measurements must replace load allowances and RF-window factors before making pack promises.
