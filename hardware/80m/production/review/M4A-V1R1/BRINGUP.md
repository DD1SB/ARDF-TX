# RF80-V1R1 — one integrated staged commissioning plan

**Plan only. All stages NOT_RUN.** No procurement, assembly, power-up or RF activation is authorized by this CAD milestone. The proposed first-article substitution for E2 requires review before fabrication. Later approvals for purchase, staged population, energy and RF are separate.

Use one complete V1R1, populated progressively, rather than separate RF coupons. Preserve all seventeen physical gates in physical-qualification.json and every numerical method in the original [M4A production test plan](../../../../../docs/M4A_PRODUCTION_TEST_PLAN.md) and [E2 power restrictions](../../../../../docs/M3B_E2_POWER_PROTECTION.md). Substituting the compact article changes the board under test, not the protection acceptance limits.

## Shared instruments and records

Current-limited isolated 3.3 V and bounded 0–18 V laboratory supplies; calibrated DMM/current measurement; oscilloscope with suitable differential/low-capacitance probes; the retained ≥500 MHz asynchronous reset method; LCR meter; calibrated RF wattmeter capable of 10 mW, counter/reference and spectrum analyzer with suitable attenuation; normal ≥10 W / 50 Ω dummy load and separate low-power Fox load; insulated thermocouples and safe nonconductive support. VNA or equivalent characterization is useful for winding/filter/antenna work. Shared instruments are not installed on each transmitter.

Record board/source revision, serial, actual maker/lot, component values, winding photos and polarity, all fixture/probe/calibration details, supply/current/duty, temperature, raw waveforms and uncertainty. Each result is PASS/FAIL/NOT_RUN. Fixture current cutoff must not be confused with measured board isolation.

## Progression and stop conditions

| Stage | Required activity before moving on | Result |
| --- | --- | --- |
| 1 | Bare-board visual/dimensional/continuity inspection: 150×110 mm, four 3.2 mm NPTH, all finished-hole sizes/registration, masks, annular rings, no copper defects or incorrect revision | NOT_RUN |
| 2 | Incoming connector and lead fit: exact six audited MPNs, lead measurements against disclosed screens, dry-fit all arrays without force; inspect keyed mates, pin1 and cable continuity. Do not drill plated holes after fabrication | NOT_RUN |
| 3 | Unpowered component pinout/variant verification: ST BD140 1B/2C/3E; TI TL431 DBZ 1K/2REF/3A; Vishay IRF610 1G/2D/3S/tab drain. Full DNP R228/R348/R349; Fox-only fits them and omits normal PA | NOT_RUN |
| 4 | Populate low-voltage control/protection first; U401 driver and Q402 final absent. Apply isolated current-limited 3.3 V through J101; verify local defaults, all grounds and no PA request during reset/disconnect | NOT_RUN |
| 5 | Real ARM/LEASE/mute/key/path/profile/bus/fault tests: watchdog ≤250 ms, quiet interval ≥1.5 ms, no false permission or spontaneous rearm; ≥500 MHz/low-capacitance capture of asynchronous reset races. FAULT_N low while disarmed is normal | NOT_RUN |
| 6 | Selected pack input/regulators using a bounded laboratory source, not a Li-ion pack. Full requires validated 4S/PACK4_OK, never a constant high. Confirm J301 1VBAT/2GND and controller 3.3 V range. TPS22810 must remain within its recommended ≤18 V input envelope; no 24/28 V whole-board fault test inferred from TVS rating | NOT_RUN |
| 7 | Controlled UV/OV/OC/hot, sensor open/short, detached sensor, isolation, discharge and shutdown tests. Observe actual rails and inhibit behavior rather than only FAULT_N | NOT_RUN |
| 8 | **Driver-absent failed-buck surrogate:** qualify the retained capacitor ESR/hot tolerance and board fault response. Require **board isolation ≤20 µs and VDRV ≤12.6 V including measurement uncertainty**. Keep U401/Q402 absent until passed; no unrestricted battery-based fault tests | NOT_RUN |
| 9 | Low-power Si5351 source/frequency/stability and I²C programming with ARM low. Verify silent retune, quiet holdoff, held-ARM recovery prohibited and default-off sequencing with actual controller M6-L1 | NOT_RUN |
| 10 | Separately approve/fill driver and representative bounded gate/shaper loads after rail gates pass. Verify drive/inhibit/ringing, BD140 shaping and hot SOA before fitting IRF610. Initial RF only after separate authorization and dummy load connected | NOT_RUN |
| 11 | Populate IRF610 with electrically insulated sink hardware and remote insulated TH301 on its case, strain relieved. Verify tab isolation/thermal attachment. Start normal RF at 12 V lab input, lowest rail, ≤200 mA and ≤1% marks; increase only after recorded passes. Bounded short tests up to 0.8 A still respect R350/pulse/SOA limits | NOT_RUN |
| 12 | Calibrated normal RF into 50 Ω over low/mid/high 3.510–3.600 MHz and applicable input/temperature corners. Full target 3.0–3.3 W, extended 1.10–1.30 W with uncertainty ≥1 W, independently adjusted Sprint 0.75–0.95 W within permitted 0.3–1 W. These are targets, not measured results | NOT_RUN |
| 13 | Independently calibrate Fox output 9–11 mW reference-load window around nominal 10 mW; verify FOX_ONLY works without normal power hardware and follows its allowed protected-pack contract | NOT_RUN |
| 14 | Normal/Fox isolation including key/fault/retune transients: compact port ≤66 µW at maximum normal output; never attach compact accessory to watt port. Bounded separate-source 100 mW accessory fault-withstand check only after review | NOT_RUN |
| 15 | CW envelope 3–8 ms rise/fall, ≤10% overshoot; retained ±20 kHz click method; harmonics/spurs project target ≤−50 dBc with adequate analyzer floor. Off-slot search aim ≤−70 dBm at recorded settings. Actual national operating authorization remains separate | NOT_RUN |
| 16 | IRF610/BD140/driver/buck/R350/coils/caps temperatures, drain/gate waveforms and hot SOA. Initial 25°C case ≤70°C / junction estimate ≤110°C, then 50°C hot qualification. Initial VDS ≤100 V and VGS ≤12 V conservative gates. Start bounded 2:1, then 3:1 VSWR phase sweeps; open/short tests only if separately justified | NOT_RUN |
| 17 | Record supply consumption and actual 12 h full / 24 h reduced endurance using chosen protected pack, aging/temperature assumptions and contest duty. Continuous spectator/finish beacon is a separate model. No runtime claim from a component-current calculation | NOT_RUN |
| 18 | Normal antenna/matching versus independent compact Fox radiator/return/accessory; reproducible Fox 30 m audible / 250 m not-audible method with recorded receiver/environment; controller/LoRa coexistence and field range. Independent second build required before fleet reproduction | NOT_RUN |

A failed stage stops progression. Do not bypass a safety gate by raising supply current, fitting the driver early or replacing a measurement with simulation. No automatic fault recovery into an armed state. Gate and source monitoring must cease when meaningful controller progress stops; the module keeps its local autonomous inhibit.

The compact layout lacks a measured E2 comparison. All absolute safety/RF criteria therefore apply directly to V1R1, with its supply/ground ringing, coupling, thermal gradients and port leakage recorded explicitly. Correct any actual failure through controlled changes before reproducing a fleet. Bare-PCB manufacturing review is not production or transmitter approval.
