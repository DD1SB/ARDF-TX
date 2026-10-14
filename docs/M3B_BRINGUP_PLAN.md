# M3B — staged laboratory bring-up plan

Date: **2026-10-14**, M3B-E1. **PREPARATION ONLY: no board has been fabricated, assembled or energized. All result fields start NOT_RUN.** Each stage requires a recorded pass and reviewer sign-off before the next; a failure stops the dependent stage. The [safety gates](M3B_SAFETY_GATES.md) are part of this procedure, not optional background.

## Bench equipment and fixture

Use an isolated0–18 V laboratory PSU with adjustable current limit and a separate bounded3.3 V source; calibrated DMMs/current shunt; ≥100 MHz scope for envelope/supply and **≥500 MHz scope/≤1 pF active probe** for asynchronous pulse/race evidence; appropriate voltage-rated low-capacitance differential/drain probe; spring grounds; calibrated50 Ω RF power measurement; ≥10 W normal dummy load; low-power50 Ω Fox load; ≥30 dB rated attenuator/DC block for the analyzer; spectrum analyzer covering fundamental through at least ten harmonics, with dynamic range verified against the intended−50 dBc project target; frequency counter/reference; LCR meter/VNA; thermocouples and nonconductive bonding material. A power meter that cannot resolve10 mW is inadequate for Fox calibration. Account for all cable/attenuator loss and uncertainty.

An existing ESP32/controller or shared external pulse/I²C fixture provides3.3 V signals and timestamps. No extra production MCU/RTC is added to RF80. Use an interlocked bench control panel, physical PSU disconnect and first-fault logging. Fixture outputs must be high impedance when RF80 is unpowered; do not feed I/O through protection diodes. External fast-step/dummy-load hardware is permitted for fault tests; it must be independently voltage/current rated.

| J101 pin | Contract |
| --- | --- |
|1 /2 /4 /16 |Regulated3.3 V / grounds. **No raw pack voltage on pin1**; multiple short ground returns, separate PA current route via J301 |
|3 /5 |SCL / SDA,3.3 V open-drain I²C; source address0x60; pull-ups already provided on module |
|6 |LEASE: rising progress pulses, initial20 Hz (50 ms spacing), tied to actual control progress |
|7 /8 |Raw ARM / positive CW_KEY; KEY must be low on a valid raw ARM edge |
|9 /10 |PA_REQ / FOX_REQ; exactly one captured path; neither/both cannot produce RF |
|11 /12 |PWR0 /PWR1, captured during arming; 00 Sprint,10 extended,01 full,11 invalid |
|13 |MUTE_N: high permits healthy context, low withdraws permission; default-low pulldown |
|14 |FAULT_N status,3.3 V logic; observe, do not drive against the RF module output |
|15 |PACK4_OK from system; local voltage comparator remains independent; pin15 alone cannot authorize a low-voltage normal PA |

J301 pin1 is positive **protected4S** for the normal build; pin2 return. Fox-only may use protected2S for sensing while logic/RF receive controller3.3 V. J401 is normalRF/return; J502 pin1Fox RF/pin2return/pin3identity. Pin1 marks, IDC key and cable continuity must be checked physically. [Probe map](../hardware/80m/review/M3B-E1/probe-map.csv) and [population map](../hardware/80m/review/M3B-E1/population-map.csv) are the measurement coordinates, in KiCad absolute mm.

## Stage 0 — unpowered inspection

1. Compare received copper/mask/drills with the review plots; measure outline, mounting centers and finished holes. Inspect mask bridges, annular rings, polarity and unintended shorts. No manufacturer substitution without exact drawing comparison.
2. Use the1:1 assembly drawing and actual lead gauges for LM5134B/DDC/DBV/SOIC pin1, fuse0603, IDC/VH/XH/3.81 mm terminals, IRF610G-D-S/tab and BD140E-C-B. Do not infer either transistor pinout from the symbol's graphical order.
3. Continuity-check each supply/return boundary, no direct normal-to-Fox RF connection, and no continuity from drain/tab to grounded mechanical supports. Identify every optional/DNP position. Keep nylon standoffs and an open bottom clearance≥10 mm.
4. Assemble transformer/inductor samples only when later authorized:9+9 bifilar phasing/series-aiding continuity and20Tfilter inductances/Q. No winding or physical work is authorized by this document itself.
5. Plan one remote TH301 bonded through insulation to IRF610 case; landing pads are the connection, not another fitted parallel NTC. Check bond lead strain relief. Keep all stage-off components in marked bags.

Pass: correct dimensions/pin mappings, no short, correct winding plan and isolation. Any wrong fuse/package/connector hole is a stop before soldering. Result **NOT_RUN**.

## Stage 1 — low-voltage logic and source

Populate BOTH logic/reference/source/interlocks and required decoupling only. Keep U301/U302/U401/Q402, PA shaper/normal filter and Fox buffer/shaper/output absent. Normal-population guards U312/U314 may be fitted and stimulated through a bounded fixture; do not fit Fox bias links R228/R348/R349 on a full build.

Power only V3V3 at3.30 V, current limit initially**100 mA**. Stop for steady limit, unexpected heating,3.3 V outside±5% or backpower. Source/logic expected current is to be measured, not assumed as a pass. With J301 unpowered, emulate pack-sense/temperature/current inputs using a≤0.7 V,≤1 mA stimulus through≥1 kΩ; no input may exceed its own powered-rail limits. Remove the fixture before a real pack input. This is an analog fault-test stimulus, not a permanent safety bypass.

Keep ARM/KEY/requests/MUTE_N low initially. Establish stable3.3 V/reference/POR, exercise reset with LEASE both low and high and then held. Require LEASE_OK low until a genuine new edge; holding LEASE high through reset must never manufacture progress. Program Si5351 with outputs disabled first. Measure SCL/SDA activity → BUS_QUIET withdrawal; stuck SCL/SDA low must inhibit, idle high alone must not fake a heartbeat.

Execute all31 [R1 scenarios on the current netlist](M3B_LOGIC_RESULTS.json) physically for both paths. First sequence: KEY low → configuration → I²C idle → progress pulses → ARM low≥20 ms → correct path/mode → MUTE_N high → raw ARM rising → wait≥250 ms before first KEY. The deliberately generous fixture waits are not proof of actual minimum timing. Lease loss must clear permissions no later than250 ms; measured SCL quiet interval must satisfy≥1.5 ms before permission; log actual tolerance across temperature/ramp tests. Bus activity withdraws RF even if the Si5351 clock keeps running.

Observe raw ARM, ARM_ACCEPT, ARM_CLK, RESET_N, ARMED, captured path/mode, permits and PA_INB together. Sweep reset/fault/bus/heartbeat edges through ARM; measure clear pulse widths and recovery. Require [Gate L](M3B_SAFETY_GATES.md): no false ARM, no held-ARM auto-recovery, no live path transfer, KEY-high arming rejected, captured values stable and conflicting requests fail off. Verify key-tail withdrawal on normal KEY-off versus fault withdrawal. All scope records must include probe loading and supply slope. Result **NOT_RUN**.

## Stage 2 — input and power conversion

Fit J301/F301/D301/R350/C350/input passives and buck/output isolation/sense circuitry. Driver and final remain absent. Use an appropriately rated resistive/electronic dummy load on the output. Never ground one side of the high-side shunt with an instrument.

Start at12.0 V with **50 mA limit/no load**, then100 mA. Keep RF disabled. Record VIN_PACK/VIN_PA/buck output/inrush. For enabled rail tests, maintain the genuine valid safety context and use a known10–20 mA load, then raise current limit only as needed, to≤200 mA initially. Do not bridge the rail switch or force the logic gate to pass. Verify each captured power setting after a deliberate disarm/rearm:

| PWR0 | PWR1 | Mode | Calculated nominal buck output; **not calibrated RF power** |
| ---: | ---: | --- | ---: |
|0 |0 |Sprint |4.679 V |
|1 |0 |Extended |5.576 V |
|0 |1 |Full |7.958 V |
|1 |1 |Invalid |Must stay off, irrespective of the feedback network's latent voltage |

Initial steady rail acceptance:±5% of design nominal and no peak>8.6 V in permitted operation; record comparator trip separately around the calculated8.973 V threshold. Verify startup charge current of C404 does not create a false overcurrent trip, and that fault clearing never reopens the switch with ARM held high. Load-step and PSU current-limit interaction are separate tests.

Progress12→14.4→16.8 V only with passing waveforms. Run **Gate I** insertion/removal with representative harness: VIN_PA≤18 V including uncertainty, input damping/fuse/resistor safe. Run **Gate D** with U401/Q402 absent and buck isolated before injecting a failed-buck surrogate; no backdrive into TPS54302, no28 V board injection. Do not fit driver unless≤20 µs withdrawal and VDRV≤12.6 V are demonstrated across stated temperature/ESR conditions. Result **NOT_RUN**.

## Stage 3 — driver and envelope shaper

Fit U401, bypasses, R410/C404, gate bleed/clamp and BD140 shaper/sink. Q402 stays absent; **lift R403** to isolate a representative capacitive gate-load fixture. Refit R403 only after safe gate-load testing. Do not operate the driver against a random short; document the dummy capacitance/series resistance and peak current.

Use source3.510/3.550/3.600 MHz and initial low rail/short marks. Measure VDRV, input thresholds, INB withdrawal, gate waveform, clamp ringing and thermal rise. Require VDRV≤12.6 V and actual VGS within the chosen≤12 V normal target, with no excursion approaching the IRF610±20 V absolute limit. Verify no carrier train when inhibited, including retuning, rail ramp and fault withdrawal.

Use a bounded shaper dummy load; verify3–8 ms envelope edge candidate and key-tail timing10–80 ms on ordinary KEY-off. A fault must withdraw clock/driver without waiting for the ordinary envelope tail. Record BD140 VCE/current trajectory and base resistor heating. A resistive dummy load does not establish switching-PA SOA. Result **NOT_RUN**.

## Stage 4 — normal RF

Fit IRF610, phased transformer, original elliptic LPF and normal connector. Use calibrated50 Ω load≥10 W, rated coax adapter/attenuator and drain probe. Remove temporary surrogate injection. Before KEY, confirm source settings, driver inhibit and current/fault response from previous stages.

Begin with12 V laboratory input, lowest rail,≤200 mA current limit, **≤1% marks** (e.g.10 ms each second). An initial current-limit excursion is a stop to inspect, not permission to jump to full current. After supply/waveform checks, raise the limit stepwise, at most**0.8 A** for short RF testing; hot R350 continuous rating and nominal1.25 A trip do not justify sustained0.8 A operation. Increase mark duration/duty only with measured losses/temperature. Do not hot-switch antenna ports; external50 Ω load must remain connected.

| Measurement | Evaluation acceptance / stop gate |
| --- | --- |
|Classic full |Calibrated target approximately3 W; initial engineering band **3.0–3.3 W** at50 Ω, with uncertainty and supply corners recorded; no implication of a new IARU3 W minimum |
|Extended Classic |**1.10–1.30 W**, uncertainty interval remains≥1.0 W for a championship-designated profile |
|Sprint |Independently calibrate **0.75–0.95 W** target; entire uncertainty interval inside retained0.3–1 W conducted limit |
|Frequency |3.510/3.550/3.600 MHz, initial calibrated error≤10 ppm over specified temperature/battery; retune only inhibited; legal/local profile validation separate |
|Drain/gate |Peak VDS initial limit **≤100 V** (retained E4 limit, below200 V device rating); VGS target≤12 V; no avalanche/unstable oscillation. If matching needs exceed the limit, stop and review rather than invoking the DC rating |
|Efficiency |Record PA, driver and complete-module DC separately. Initial normal-stage target≥50% at full,≥40% extended; lower results require thermal/endurance reassessment, not a false compliance claim |
|Unwanted output |Project gate harmonics/spurs≤−50 dBc at calibrated settings; analyzer floor/attenuation must support the result. Applicable national emission limits must also be identified; the project target is not legal authorization |
|CW/retune |3–8 ms RF envelope rise/fall, no overshoot burst, retained click/spectral method; configuration/lease/fault events leave no unintended RF beyond recorded withdrawal/tail contract |
|Thermal |Log cases and estimate junction using applicable package thermal paths/SOA; initial case≤70°C at25°C ambient and conservative estimatedjunction≤110°C. Remote NTC nominal80°C is a fault backstop, not normal operating-temperature approval |

The retained [E0–E9 plan](M3_80M_TEST_PLAN.md) remains authoritative: ≤10% envelope overshoot, adjacent±20 kHz click evaluation, off-slot search aim≤−70 dBm with stated analyzer settings,50°C hot testing and three independent builds before a fleet layout. These limits are not relaxed by the staged low-energy procedure. Repeat12/14.4/16.8 V, low/mid/high frequency and thermal duty. Contest20% and continuous beacon are different records. Test mismatch initially with external limiter at reduced energy, then controlled2:1 VSWR phases as an initial test, followed by the retained **3:1 phase sweep**; open/short testing only if bounded SOA/current/voltage evidence permits it. No blanket mismatch-survival claim until measured. Result **NOT_RUN**.

## Stage 5 — Foxoring branch

Populate Fox source-following input, shaped supply, SN74AC00 summing network, original Fox LPF/pad and J502. For a Fox-only assembly **all NORMAL parts absent**, fit R228/R348/R349 and use the generated Fox population list. Drive regulated3.3 V with current limit100 mA initially; protected2S sensing compatibility is tested separately from direct raw supply. The buck and watt PA must not be dependencies.

Calibrate **9–11 mW at the defined50 Ω reference port**, not at an arbitrary antenna terminal. Measure uncertainty, frequency, harmonics, RF edge shape, VFOX ramp, rail-following input/backpower and unarmed/startup/retune/heartbeat-loss output. Do not operate the SN74AC00 below its characterized supply range and claim its logic waveform guaranteed; the ramp crossing is specifically a physical test. If fixed calibration or clean edges fail, use the retained BJT-buffer fallback only after an explicit electrical revision.

For a full build, verify never-simultaneous port enable and normalRF→Fox isolation: retained≤66 µW leakage at maximum normalRF corresponds to≈47 dB. Repeat at all frequencies, key edges, supply faults and a detached compact accessory. Test the accessory's **100 mW fault-withstand** with a bounded source; no watt-PA injection into it. Later antenna tests use the independent≈30 cm radiator, compact counterpoise and loading/coupling network. Reference-load10 mW is distinct from the retained reproducible30 m audible/250 m not-audible field evaluation; record receiver, sensitivity, ground, weather, orientation and repeated placements. Result **NOT_RUN**.

## Stage 6 — bounded fault injection and records

Inject controller reset/disappearance, heartbeat held high/low, SCL/SDA stuck and active, high KEY during ARM, path/mode conflict, supply UV/OV, overcurrent surrogate, NTC short/open, and edge-coincident ARM/reset faults. Prefer≤1 mA comparator-input stimulus and representative loads when a real destructive mechanism is unnecessary. Keep driver/final absent for unqualified high-voltage fault tests. Require both physical RF permissions inactive, driver inhibited, rails appropriately withdrawn and **fresh deliberate rearm after every fault**. An electrically intact but detached NTC is an explicit mechanical failure: test bond retention and temperature correlation, not a comparator's nonexistent detachment detector.

Record board serial/revision, actual MPN/lot/values, winding photos, supply/current limits, instruments/calibration, probes, firmware/fixture version, ambient/case temperatures, all raw traces and failure notes. Use PASS/FAIL/NOT_RUN per gate. Only after all electrical/RF/thermal gates pass may measured current replace estimates in the12 h full/24 h reduced endurance model. No Li-ion destructive fault, fleet build, outdoor operation or manufacturing is authorized here.
