# M3A-R1 — reproducible verification and limits

Date: **2026-10-14**. **No assembled prototype or measured RF/thermal/safety results.** R1 supersedes R0's functional-check claims; historic R0 remains tagged in Git. The primary defect escaped ERC and the old intended-signal Boolean model. The replacement checks read actual connected physical pins.

## Reproduce

From the repository root, KiCad CLI 10.0.6, Python 3 standard library and ngspice are required:

```sh
kicad-cli sch erc hardware/80m/RF80.kicad_sch --output hardware/80m/review/ERC.json --format json --severity-all --exit-code-violations
kicad-cli sch export netlist hardware/80m/RF80.kicad_sch --output hardware/80m/review/RF80.xml --format kicadxml
kicad-cli sch export pdf hardware/80m/RF80.kicad_sch --output hardware/80m/review/RF80.pdf
python3 tools/m3a_r1_logic.py
python3 tools/m3a_r1_driver_fault.py
python3 tools/m3a_r1_report.py
python3 tools/m3_80m_checks.py
python3 tools/m3a_r1_documentation.py
```

`--write` on the Python scripts regenerates reports after deliberate changes; default checks reject stale generated results. [Design generator](../tools/m3_80m_design.py) replaces generated CAD/workbooks only with `--write`; reconcile manual CAD edits first. [Delta report](../tools/m3a_r1_report.py) needs the preserved `m3a-r0` tag. No PCB or production firmware is emitted.

| Verification layer | Evidence | Limit |
| --- | --- | --- |
| Actual KiCad connectivity | Manifest matched against exported XML; 597 connected pins and 218 footprint-pad maps | Pad numbering is checked; not every land's thermal/mechanical/voltage property |
| ERC | Zero violations, no new exclusions | Installed default-disabled rules listed in M3 checks; functional defects are not ERC rules |
| Pin-derived static logic | 256 combinations of ARM, requests, mode, guards, KEY/tail | Ideal gate truth and pull/clamp behavior; no diode-voltage or analog pulse proof |
| Pin-derived sequential model | 31 named scenarios including actual HC123 reset/trigger/retrigger and HC74/174 asynchronous clear | Ideal zero-delay propagation; asynchronous feedback pulse width/metastability not certified |
| Timing sensitivity | 16 assumed K/RC/Schmitt corners; both paths key/pause and fault during pending ARM | Assumed bounds, not manufacturer guaranteed worst cases |
| Negative regression | Both U202 output-polarity swaps rejected; inverted-watchdog no-progress RF permission reproduced | Regression is deliberately limited, not complete arbitrary-fault coverage |
| Actual ngspice run | R410/C401/C402/C404 linear transient sensitivity, CSV and circuit saved | Input failure and switch removal imposed; no comparator/FET/RF model or measured result |
| Arithmetic/population | 18 cost baskets, pooled MPNs/MOQ, actual full/Fox fit counts and Git baseline delta | Many quotations open; low-current hundred-piece price estimated |

Detailed scenario names and assumptions: [logic JSON](M3A_R1_LOGIC_RESULTS.json). Power-fault results: [simulation JSON](M3A_R1_DRIVER_SIMULATION.json), [ngspice circuit](../analysis/m3a_r1_driver_fault.cir), [waveform CSV](../analysis/m3a_r1_driver_fault.csv). Every temporary ngspice run is fresh; scripts compare saved results for staleness.

The logic engine separately publishes actual Q and /Q outputs, reads gate/FF/monostable nets from XML and traverses the real diode/FET paths. Comparator results are external ideal test stimuli applied to their **physical output pins**; PA guards are not assumed healthy by a label. A voltage-domain analog model is not present. The Fox run omits the watt comparators and implements fitted R228's ground clamp. HC174 inputs/outputs, heartbeat witness and delayed arm are modeled as state. Manufacturer pin tables are independent of the generator, so swapping labels on an incorrect device pin fails the test.

## Driver-fault sensitivity and physical stop gate

Minimum R410=4.653 Ω, bulk C404=37.6 µF, high-frequency C401/C402 total=0.88 µF. Initial driver voltage 8.6 V. Assume 0.5 Ω bulk ESR and **force isolation after 20 µs**:

| Imposed case | Simulated peak VDRV | Assessment |
| --- | ---: | --- |
| Buck fault to 16.8 V pack | 10.082 V | Below 12.6 V only for imposed bound |
| Isolated passive28 V surrogate; outside system rating | 12.107 V | Below 12.6 V; small margin, bound must be measured |
| 28 V, slower isolation 50 µs | 14.347 V | FAIL |
| 28 V, bulk ESR 1.5 Ω, 20 µs | 14.414 V | FAIL |

Panasonic's low-ESR polymer is selected instead of relying on an unqualified cheap wet capacitor. Its quoted 30 mΩ is at 100 kHz/20°C, not proof of the entire transient/temperature bound. TI gives typical load-switch timing under particular conditions; it does **not** guarantee this complete OV comparator/logic/load-switch path meets 20 µs. [LM5134B](https://www.ti.com/lit/ds/symlink/lm5134.pdf) operates at 4–12.6 V; 14 V absolute maximum is not an acceptable operating goal. The simulated28 V is an isolated passive sensitivity envelope, **outside the system rating**, not a proven TVS/cable clamp. TPS22810 permits18 V operating/20 V absolute; INA180 inputs permit26 V and upstream PA ceramics are25 V. A reservoir keeping the driver below12.6 V does not protect those other components. Before unrestricted power, qualify input hot-plug/cable/fault voltage so the failed-buck path stays≤18 V; the provisional SMBJ17A clamp alone does not establish that. Do not inject28 V into the complete assembly; surrogate passive-network tests use separate rated fixtures. Input-clamp coordination remains an explicit pre-layout review risk.

**Before unrestricted 4S or armed RF:** test power-only with current limiting and dummy driver load, inject a bounded converter-short stimulus, scope VPA/VDRV/PA_GUARD/PA_PERMIT/INB/switch output simultaneously. Require complete input isolation≤20 µs, VDRV≤12.6 V, transient ESR≤0.5 Ω over 0–50°C, acceptable R410 pulse energy/temperature, no avalanche/backfeed, and no false OC during capacitor charging. Start limited; the test must not destroy an unqualified real driver. C306 changed to 4.7 nF for slower load-switch ramp; require measured rise≈1 ms or longer subject to no OC/inrush and startup settling. If bounds fail, STOP and revise rail protection before attaching RF. Do not turn the simulation into a hardware PASS.

## Physical conditions still OPEN

| Gate | Measurement / objective acceptance |
| --- | --- |
| R1-L1 | Scope HC123 Q13,/Q12, witness, ARM_ACCEPT, ARMED, INB and Fox buffer enables through slow/fast rail startup/collapse, controller unplug/reset and missing/stuck heartbeat. No RF pulse at either port. Genuine 50 ms rising-edge cadence retained; stop≤250 ms; quiet≥1.5 ms. |
| R1-L2 | Inject every comparator trip during keyed RF and during the delayed-ARM interval. Hold ARM high while clearing the fault; neither path may rearm. Measure HC174 MR pulse width, CLR recovery and glitch response against datasheet limits; sweep relative edge phase. |
| R1-L3 | SCL/SDA stuck low/high, bursts, line release and failed readback. Either low inhibits; activity requires disarm/rearm. Demonstrate firmware progress ceases on bus failure. Both-high alone is not a hardware fault detector. |
| R1-L4 | Sweep diode pull/clamp networks and stack gates at 3.135–3.465 V/0–50°C with measured input/output thresholds, leakage and noise margin. Probe negative/positive VGS. No tied CMOS outputs, backfeed or reliance on indeterminate ramps. |
| R1-P1 | Power-only driver OV/short test and capacitor/startup tests above; ≤20 µs interruption and ≤12.6 V at all bounded corners. Independent disconnect and mute must both work. |
| R1-P2 | Capture input/hot-plug/cable transients and failed-buck routing; TPS22810 input≤18 V, all parts within operating limits. SMBJ17A is provisional. If the measured/input-source bound cannot ensure this, revise clamp/disconnect ratings before unrestricted power; 28 V sensitivity is not system acceptance. |
| R1-R1 | Key tail 10–80 ms after key-up, RF rise/fall 3–8 ms on **both** paths, no carrier during integrator precharge. Continuous source/clock alone must not transmit unarmed. Faults override tail. |
| R1-R2 | Fox VFOX ramp and AC00 operation below 2 V; source-following input/backpower, ballast currents, individual output mismatch, shaper short. Measure 10 mW at calibrated 50 Ω and fault bound/accessory withstand. Use BJT fallback if logic buffer cannot pass. |
| R1-T1 | Hot repetitive BD140/IRF610 SOA, drain/gate peaks, attached NTC hot/open/short and physically detached-but-wired sensor, dummy load and antenna mismatch. Trip lag and junction temperature must pass the existing RF/thermal gates. |
| R1-I1 | Physical isolation: normal-port full RF/faults cannot energize J502. Measure inactive-port leakage, startup bursts, grounding/harness injection and pad protection; no safety inference from absence of a drawn wire alone. |
| E0–E9 retained | Full 3.510–3.600 MHz output/calibration (3 W/1.2 W/Sprint), spectrum/key clicks, efficiency/thermal, long-wire match, separate 30 cm Fox match/return, 30 m audible/250 m not audible field tests, timing, 12/24 h battery profiles and LoRa immunity. All NOT RUN. |

The [original detailed test plan](M3_80M_TEST_PLAN.md) supplies instrument requirements and numerical RF gates. RF circuitry/transformer/LPF were not retuned in this milestone; no simulation establishes actual conducted power, harmonic suppression or compact-antenna range. Keep original conservative controller/source/idle consumption until measured; no savings are inferred from fewer logic packages. All eight preserved M1/M2/audit check scripts passed. The current documentation check passed77 Markdown files,505 local links and30 hardware artifact hashes; all baseline73 traced requirements remain.

Product release is **NO-GO**. A tightly scoped evaluation board can follow explicit electrical review/layout authorization, with the above power-only and logic tests preceding unrestricted RF. No manufacture/procurement is authorized here.
