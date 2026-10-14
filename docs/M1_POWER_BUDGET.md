# M1 energy and peak-current budget

Date: 2026-10-13. **Calculated planning budget, not measured currents or demonstrated battery life.** See [RF feasibility](M1_FEASIBILITY.md), [source log](research-register.md) and [analysis script](../tools/m1_analysis.py). All efficiencies/application currents are explicitly unverified inputs. **This cost-rework budget governs current estimates**; `python3 tools/m1_analysis.py --rework` reproduces it. The script's default output retains the original arithmetic for historical comparison, not the current recommendation. Cheaper control does not earn unmeasured standby savings.

## Pack and voltage assumptions

**Conditional-review update:** the original calculations below are retained as the M1 baseline. [M2 VHF analysis](M2_VHF_RF_REVIEW.md) now derives series-modulator losses explicitly and uses a conservative **4P evaluation allowance**; the earlier VHF3P result is not a current unconditional recommendation. [M2 RF calculations](M2_RF_CALCULATIONS.json) give the sensitivity. The [M2 power budget](M2_POWER_BUDGET.md) includes shaping/helper losses with 1.00 W HF Classic and 0.65 W Sprint active overhead, plus revised low-path reserves. It plans HF/VHF 4P, Sprint 2P and Foxoring 1P; smaller-pack passes remain measurement-dependent. Actual current/efficiency remain unmeasured.

Reference cell capacity **3.4 Ah at 3.6 V nominal** is a planning input, compatible with the advertised Samsung 35E capacity class; manufacturer cell/lot data and tested pack remain OPEN. NCR18650B listings at 3.35 Ah are an alternative, reducing calculated runtimes by 1.47%. No current or capacity measurement is invented. Packs are **external, protected and balanced**, assembled from matched cells; no charging on controller in this proposal. A 2S CC/CV charger, BMS, cell temperature limits and wiring must match the selected pack.

Use 80% capacity for aging/lot margin ×90% usable discharge window ×90% temperature allowance = **64.8% nominal energy**. Converter losses are in loads, not applied twice. These multiplicative allowances are design assumptions; severe cold or higher cutoff may require more margin. Model uses 6.0 V pack at peak load; actual cutoff follows cell/BMS/loaded voltage and may be above 6 V. Fully charged maximum is 8.4 V. Provisional target ambient −10…+50°C requires pack-specific confirmation.

| Pack | Cells / nominal Ah | Nominal Wh | Usable Wh (model) | Maximum mean battery power for 24 h |
| --- | --- | --- | --- | --- |
| 2S1P | 2 / 3.4 | 24.48 | 15.863 | 0.661 W |
| 2S2P | 4 / 6.8 | 48.96 | 31.726 | 1.322 W |
| 2S3P | 6 / 10.2 | 73.44 | 47.589 | 1.983 W |
| 2S4P | 8 / 13.6 | 97.92 | 63.452 | 2.644 W |

## Every steady-state load accounted for

| Load / state | Budget input | Classification / boundary |
| --- | --- | --- |
| ESP32, wireless off | 20 mA average at 3.3 V =66 mW; sensitivity at 60 mA | ASSUMPTION, must measure actual schedule/interrupt/USB-off behavior. |
| Timebase | Allow 10 µA at 3.3 V including output/interface; device headline 160 nA typical at 3 V | RTC-DS is conditional DATASHEET, allowance includes operation beyond bare timekeeping. |
| Monitoring, pulls, status, controller safety | Remaining controller rail allowance to 100 mW total | ASSUMPTION includes ADC dividers, voltage sensing, protected branches, LEDs with low duty and optional pack-current sensor. RF-local safety is budgeted on each module. |
| Logic regulator | 90% conversion; additional battery-side/BMS/switch loss allowance 9 mW | ASSUMPTION, not vendor peak-efficiency claim. Total common battery load rounded to **0.120 W**. |
| Installed RF board idle | **0.010 W each** at battery | ASSUMPTION includes monostable/latch/POR/sensors and quiet-rail leakage with synth/PA off. Single-board fixed total **0.130 W**, dual **0.140 W**. Omitted board draws zero. |
| 80 m synth active | 25 mA at 3.3 V /90% ≈0.092 W | ASSUMPTION; not a universal datasheet current. Must measure chosen outputs/reference. |
| 80 m driver/shaping active | Rounded active synth+driver overhead **0.500 W Classic**, **0.250 W Sprint** | ASSUMPTION beyond RF PA conversion; prevents hiding gate-drive/rail overhead. |
| Foxoring complete | **0.260 W battery** continuously, including common/idle, synth, low buffer/attenuator and rail losses | ASSUMPTION, conservative key-down; watt boost/PA off. Dedicated match is passive but reduces radiated efficiency. |
| VHF source/reference active | Budget 0.150 W battery for Si5351/reference/control support | ASSUMPTION, not measured; alternate PLL/VCO requires recalculation. |
| VHF drive/tone/sensing active | Another 0.800 W battery; total additional active overhead **0.950 W** | ASSUMPTION, includes GVA-84 typical 106–108 mA at 5 V (~0.53 W) plus raw-2S LDO loss, tone/sensing and margin. Manufacturer nearby-frequency data is not our measured driver current. |
| Training continuous | **0.350 W battery total**, common/idle+source+low-level A2A/filter/attenuator | ASSUMPTION; maximum selected 1 mW carrier, not normal PA. |
| LoRa absent | Increment 0 | Fully supported baseline. |
| LoRa fitted standby/duty listen | Increment **0.006 W**, 10% RX target | ASSUMPTION including MCU wakes/module TCXO/switch; exact Silicontra implementation missing. |
| LoRa continuous listening | Increment **0.045 W** | ASSUMPTION includes chip RX, module extras and controller wakes. Chip headline 4.6 mA alone is insufficient. |
| LoRa transmit burst | Provision 120 mA×3.3 V /90% ≈0.44 W peak | ASSUMPTION worst provision, not measured or authorization for +22 dBm. Airtime capped by legal profile. Add `0.44×TX_fraction` W conservatively if listening budget excludes bursts. |

No undocumented display, GNSS receiver or permanently lit LED is included. Adding them requires recalc. Converter sleep/force-PWM behavior is tested because reduced noise can increase idle power. Retune/source warm-up belongs in measured active duty; allow 0.1 s prewarm per slot in final integration budget (≤0.01 W correction at these source overheads).

## RF conversion inputs and method

Classic/Sprint field window duty `d=0.20`. To avoid optimistic Morse savings, assume key-down/tone throughout the entire active window. Foxoring and all beacon estimates use `d=1`. Model:

`Pavg_battery = Pcommon + Nboards×Pidle + d×(PRF/(ηPA×ηconverter) + Pactive_overhead)`.

80 m Classic: RF mark=5 W, ηPA=60%, boost=85%; Sprint: 1 W, ηPA=55%, converter=88%. These efficiencies are ASSUMPTIONS and include output-filter loss in effective PA efficiency. The compact branch is budgeted separately, not as a watt PA plus pad.

VHF: assume antenna 0 dBd, feeder loss 1 dB, m=0.80; carrier=1.259 W, mark mean=1.662 W, PEP=4.079 W. ηPA=45%, series modulator=70%, boost=88%, plus active overhead. These are ASSUMPTIONS. They size thermal/battery needs for real AM. Continuous carrier with keyed tone can consume less than this bound in spaces, but no credit is taken.

## Results: LoRa absent, one board unless stated

| Profile / maximum setting | Mean battery W | 24 h Wh | Runtime hours: 1P / 2P / 3P / 4P | Minimum pack meeting 24 h **in model** |
| --- | --- | --- | --- | --- |
| 80 m Classic 5 W, 20% | 2.191 | 52.58 | 7.2 / 14.5 / 21.7 / 29.0 | 2S4P |
| 80 m Sprint 1 W, 20% | 0.593 | 14.24 | 26.7 / 53.5 / 80.2 / 107.0 | 2S1P, margin modest |
| Foxoring 10 mW, continuous | 0.260 | 6.24 | 61.0 / 122.0 / 183.0 / 244.0 | 2S1P |
| 2 m Classic 1 W carrier ERP, 20% | 1.519 | 36.46 | 10.4 / 20.9 / 31.3 / 41.8 | 2S3P |
| 80 m full-power finish beacon 5 W | 10.434 | 250.41 | 1.5 / 3.0 / 4.6 / 6.1 | None ≤2S4P |
| Sprint finish/spectator beacon 1 W | 2.446 | 58.71 | 6.5 / 13.0 / 19.5 / 25.9 | 2S4P |
| 2 m continuous beacon, 1 W carrier ERP | 7.075 | 169.80 | 2.2 / 4.5 / 6.7 / 9.0 | None ≤2S4P |
| VHF training 1 mW carrier, continuous | 0.350 | 8.40 | 45.3 / 90.6 / 136.0 / 181.3 | 2S1P |
| Both Classic bands, each 20%, all three PCBs | 3.590 | 86.15 | 4.4 / 8.8 / 13.3 / 17.7 | None ≤2S4P |

**These are conditional model passes, not validation.** Highest scheduled normal settings fit within maximum pack only if efficiency/idle assumptions hold. A universal unit with one active band adds only other-board idle ~0.01 W; 24 h simultaneous full-power dual-band service does not fit this model. User must decide whether that is required. Finish beacons may need a shorter event-specific runtime or external source; 2S4P is not a universal 24 h beacon solution.

## Sensitivity and LoRa impact

Continuous RX adds 1.08 Wh/day; duty listening adds 0.144 Wh/day. With continuous RX: Classic 4P ~28.4 h; Sprint 1P ~24.9 h; Foxoring 1P ~52.0 h; VHF Classic 3P ~30.4 h. Continuous 1 W Sprint beacon 4P ~25.5 h. Fitted module current must be measured; absent operation requires no reservation for nonexistent LoRa hardware.

If MCU average rises 20→60 mA, increment ~0.147 W battery: Sprint 1P falls to ~21.4 h; Foxoring still ~39.0 h; Classic 4P ~27.1 h. Thus unoptimized MCU can eliminate the cheapest Sprint pack. If 80 m effective PA efficiency=50% and boost=80%, Classic mean≈2.730 W and 4P only ~23.2 h. Do not claim an unconditional 24 h full-power pass. Acceptance mean-power ceilings in pack table, including LoRa and other standby, are the measurable contract. Cold-capacity margin must be revisited if product temperature extends.

## Peak current and thermal requirements

At 6 V, single-band Classic 80 m key-down is ~10.4 W input; add LoRa burst provision then 25% transient/inrush margin → **2.3 A pack design estimate**. VHF envelope peak bound uses **PEP**, not 1.662 W mean: `4.079/(0.45×0.70×0.88)` plus overhead/LoRa/transient → **3.4 A** estimate. Both RF peaks aligned → about **5.6 A**. Capacitor/converter dynamics may change instantaneous current; no measurement exists. Propose ≥4 A rated protected path for one active band, ≥7 A only if dual-TX experiment is allowed. Verify at cutoff/high ESR and fresh full charge.

| Pack | 80 m peak current per cell | VHF peak per cell | Aligned dual peaks per cell |
| --- | --- | --- | --- |
| 2S1P | 2.3 A | 3.4 A | 5.6 A |
| 2S2P | 1.15 A | 1.70 A | 2.8 A |
| 2S3P | 0.77 A | 1.13 A | 1.87 A |
| 2S4P | 0.58 A | 0.85 A | 1.40 A |

Parallel sharing/temperature/BMS contact limits must be demonstrated; 1P is not rejected merely for capacity if current rating suffices. Peak RF current is distinct from converter-inductor switch current. Fuse/current-limit response must tolerate normal inrush and modulation but interrupt faults; no fuse value locked.

At 5 W CW/60% effective PA efficiency, ~3.33 W is lost in PA/filter continuously; boost adds ~1.47 W. For VHF mark mean, PA loss≈2.03 W, modulator≈1.58 W and boost≈0.72 W under these assumptions, plus driver/source overhead. Continuous beacon heat is materially larger than 20%-duty service. Thermal gating, capacitor derating and enclosed tests are necessary even where energy fails first.
