# M5A 2 m PA and driver selection

Date: **2026-10-15**. **Selected for electrical evaluation: Si5351 → fundamental filter/pad → PHA-13HLN+ → PD55008-E → matching/filter.** This is a sourceable candidate with a credible output route, not a measured 144 MHz transmitter. The editable implementation is [RF2M](../hardware/2m/RF2M.kicad_sch); [primary sources and access failures](M5_2M_SOURCES.md) distinguish published evidence from our calculations.

## Output reference planes

The user specifies carrier ERP. With the unqualified antenna/feed assumption of −1 dBd, 1 W ERP requires **1.258925 W conducted carrier**. Sinusoidal AM has mean RF power `Pc(1+m²/2)` and PEP `Pc(1+m)²`: at m=0.80 these are **1.661782 W mean and 4.078918 W PEP**. A 1 dB capability reserve gives **5.135054 W at the connector**. It is capability, not permission to exceed the ERP limit.

The implemented filter's nominal allowance is 0.75 dB, increasing the final-device capability investigation to **6.103 W**. Matching/stability/coupling loss before the device is budgeted at **1.25 dB**, including the 1 Ω gate stopper: even its resistive loss is about 0.71 dB against a 5.6 Ω input. The earlier 0.5 dB input allowance would be optimistic for this circuit. These are engineering allowances; measured losses replace them.

| Intrinsic PA gain assumption | Required MMIC output at reserved capability | Minimum measured P1dB for 3 dB backoff |
| --- | ---: | ---: |
| 15 dB | 24.11 dBm / 257 mW | 27.11 dBm |
| 17 dB | 22.11 dBm / 162 mW | 25.11 dBm |
| 20 dB | 19.11 dBm / 81 mW | 22.11 dBm |

The normal operating AM crest requires 1 dB less drive than this reserved-capability test. Require **measured driver P1dB ≥27.2 dBm** and intrinsic PA gain ≥15 dB at the tested crest/load, or recompute the combined gate from measured values. Backoff alone does not prove low distortion; measure compression at the actual constant-drive operating point too.

## Focused alternatives

| Candidate | Published conditions / sourcing | Disposition at equal scope |
| --- | --- | --- |
| **PD55008-E, selected** | ST active formed-lead PowerSO-10RF. Published 8 W, 15 dB minimum/17 dB typical gain and 50/55% efficiency are at 500 MHz, 12.5 V, 150 mA bias. Near-band small-signal data exists. | Modern single final with plausible 6.1 W capability route. Actual 144 MHz matching, stability, voltage-modulated transfer and heat remain experiments. Exact formed-lead thermal landing is OPEN. |
| RD07MVS1 | Current Dec2025 sheet characterizes 520 MHz, 7.2 V, 7 W minimum at 0.7 W drive and 750 mA bias. Older 175 MHz curves exist. Cheap $3.90 RFParts stock is NOS/no-export. | No current repeatable EU quote or 144 MHz AM evidence. Current gain/drive conditions would demand a stronger driver; old data cannot silently replace them. Not selected solely for cheap residual stock. |
| RD12MVS1 | Jan2026 sheet: 175 MHz, 7.2 V, 11.5 W minimum at 1 W input, 1 A bias. | VHF evidence is useful, but more drive/bias, unquoted sourcing and unqualified AM erase a demonstrated system saving. No completed-cost total is invented for missing positions. |
| GVA-84+ | Nearby typical P1dB ≈20.73 dBm. | Would require about 21.38 dB intrinsic PA gain under the revised loss budget. Rejected as the preferred driver. |
| PHA-1+ / PHA-1H+ | Prior PHA-1+ observation €2.82, MOQ1. Different 1H nearby compression data cannot qualify 1+. | Potential saving about €11.78 against the selected driver. Needs roughly 19.6 dB gain if driver P1dB is 22.5 dBm, plus measured source drive. A future measured substitution, not today's guaranteed chain. |
| PHA-101+ | Current 9 V/182 mA, catalog P1dB25.8 dBm; observed US$14.71 single comparator. | About €1.46 silicon saving at the same ECB conversion, with weaker compression and more source drive. Exact hot 144 MHz data missing; not worthwhile as the primary choice. |
| **PHA-13HLN+, selected** | 8 V/234.1 mA typical; published typical compression27.3 dBm at20 MHz and28.4 dBm at250 MHz; observed US$16.35 cut tape. | One driver, without stacking MMICs. The bracketing data suggests useful margin but does not guarantee a 144 MHz minimum. Qualify at the actual 7.75–8.25 V rail and hot ground-lead temperature. |

PD55008L-E/straight-lead substitutions, discontinued BFP650 and out-of-band or discontinued MMICs are not production solutions.

## Matching and stability implemented, not declared qualified

ST Table10 at 150 MHz gives S11=0.803∠−162°, S21=5.19∠67°, S12=0.032∠−18°, S22=0.704∠−157°, at 12.5 V/150 mA. This reproduces the retained approximate `Zin=5.60−j7.82 Ω`, `Zout=9.03−j9.85 Ω`, K≈0.063 and maximum stable gain≈22.1 dB. **K<1: arbitrary source/load stability is not established.** Later differently captioned tables are not used.

With the 1 Ω stopper, a unilateral starting input transformation for `6.6−j7.82 Ω` gives about **27.2 nH series/56.4 pF shunt**, hence L605=27 nH/C605=56 pF. Mutual feedback, bias choke, package and large-signal input impedance are omitted from that simple calculation. The output starts at a 10 Ω drain-load investigation with manufacturer nominal 38 pF Coss: about **24.5 nH/47.2 pF**, selected 24 nH/47 pF. Coss varies substantially over the envelope; actual LPF input impedance is not an ideal resistor. These are replaceable, explicitly marked **EVAL TUNE** networks, not validated matching or the unchanged 500 MHz reference circuit.

Bias trim spans up to a bounded approximately 6.2 V ceiling, allowing the manufacturer's possible 5 V quiescent-gate requirement. Start grounded with a current-limited drain source. The bias setting, thermal drift and suitable operating class are measurement decisions, not a claimed fixed 150 mA operating requirement.

## Economical next experiment

Measure one PA coupon first with a calibrated RF generator and variable drain supply; the schematic's source/driver can be bypassed in that fixture. Establish gain, stability and the voltage-to-RF-envelope transfer before buying an expensive driver fleet. If measured gain permits PHA-1+, substitute its verified bias/footprint and recost that exact circuit. The selected stronger driver protects the present conservative gain floor; it is not a claim that the global cheapest possible PA has been proven.

The legacy ON7YD, Dutch/G3ZOI/PA0JBG and DL3BBX sets demonstrate economical supply modulation. Their legacy semiconductors, lower reported carrier power and absent modern sine-AM/PEP measurements prevent component-identical reuse for this requirement. A modified FM handheld is not the implemented transmitter.

The10 Ω output starting load includes an assumed0.8 V knee: at a12 V drain crest its simple voltage-limited capability is `(12−0.8)^2/(2×10)≈6.27 W`, before the filter. This is a calculation supporting the capability investigation, not a measured optimum. L608 is the sourceable0805CS24 nH candidate. Its current figure is a15°C-rise reference, not an absolute peak-current rating: normal AM mean current and short capability-test crests need a thermal calculation and measurement. It is not silently equated to the higher-current HP family.
