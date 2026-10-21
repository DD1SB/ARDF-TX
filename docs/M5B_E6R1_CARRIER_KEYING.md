# M5B-E6R1 — carrier-keying circuit feasibility

**Architecture C is the preferred investigation proposal. It is not implemented or electrically qualified.** The [machine-readable circuit proposal](../hardware/2m/review/M5B-E6R1/circuit-proposal.json) records exact new package pins, resistor values, timing and affected native nets. The existing E5 native sources are unchanged.

Exactly three approaches were examined:

| Architecture | MARK | SPACE | Decision |
| --- | --- | --- | --- |
| A — existing | Prepared PA and sinusoidal AM | Carrier and PA bias retained; tone absent | Reference; wastes substantial pass/PA power |
| B — keyed modulated carrier, cold domains | Restart normal converter/driver domains for each element | Normal domains off | Thermal lower bound only; repeated converter soft-start and reservoir charging are unproved; reject as implementation choice |
| C — hybrid | Converter/reference/bias stay prepared in SLOT; drive and drain command follow shaped key | Zero drain command with hardware clamp, RF clock inhibited, small MMIC domain off | Preferred precise proposal; startup, unloaded-loop and local PA safety gates remain OPEN |

Native review finds KEY at J101 pin 7, AF_PWM driving the AF filter, U402 selecting LEVEL_DC/MOD_COMMAND, U305 enabling the MMIC supply, U601 inhibiting the RF clock, and NORMAL_OFF/NORMAL_PERMIT qualifying normal transmission. No spare controller GPIO is assumed. Keep synthesizer frequency, converter preparation, bias setting and high-level safety permission stable through normal Morse gaps. TRAIN_ONLY routing, independent CLR/PA permissions and the static controller interface are preserved.

| Proposed change | Reason |
| --- | --- |
| U402 pin 3: LEVEL_DC → GND | KEY-low selects zero VPA command |
| R509 pin 1: NORMAL_OFF → LOCAL_MOD_OFF | Existing Q404/Q405 clamps also act during ordinary SPACE; zero-command offset cannot sustain normal pass loss |
| U305 pin 3: NORMAL_PERMIT → DRIVER_ON | Switch only C603 100 nF + C604 1 nF/MMIC; keep upstream C409 150 µF charged |
| U601 pin 1: NORMAL_OFF → CLOCK_OFF | Drive inhibited until drain and driver supply are ready |
| AF_PWM waveform | Calibrated 800 Hz sine multiplied by raised-cosine key envelope, with AF-chain precompensation |

Proposed U970 TLV7034PWR, push-pull quad comparator, uses two channels for PA-temperature window and two for readiness. U971 SN74LVC2G00DCUR provides `TEMP_BAD = NAND(TEMP_HOT_OK,TEMP_OPEN_OK)` and `RF_NOT_READY = NAND(VPA_READY,DRIVER_READY)`. U972 SN74LVC2G32DCUR gives `LOCAL_MOD_OFF = NORMAL_OFF OR KEY_N` and `CLOCK_OFF = LOCAL_MOD_OFF OR RF_NOT_READY`. U973 SN74LVC1G04DBVR gives DRIVER_ON. Q970 2N7002,215 sinks existing HARD_OK_N on TEMP_BAD. Its gate has a 100 kΩ pull-up; U970 healthy outputs each have 100 kΩ pull-downs. Missing/unpowered monitor therefore inhibits. Driver enable has a pull-down and clock inhibit a pull-up. Each new IC has 100 nF bypass. Exact manufacturer pin maps are in the proposal and primary references in the [review index](../hardware/2m/review/M5B-E6R1/REFERENCES.md).

Readiness candidates: VPA divider 100 kΩ/33 kΩ against a 330 kΩ/2.49 kΩ 3.3 V reference, about 0.10 V drain threshold; VDRV divider 10 kΩ/10 kΩ against 10 kΩ/21.5 kΩ reference, about 4.50 V. Comparator offset/hysteresis are significant at the VPA threshold; 0.02/0.10/0.20 V thresholds are sensitivity cases. A 2 ms driver lead is a budget, not guaranteed TPS22810/MMIC settling. KEY can provide the coarse preparation window while AF_PWM carries the shaped envelope. This requires future target-firmware integration and hardware-version configuration; it does not add a connector signal or modify M6-L2 now.

The original NORMAL_OFF qualification delay and fast kill remain in series with this logic. Q502's existing bias clamp, watchdog, independent power isolation, default-off, reset and rearm logic remain authoritative. Normal Morse SPACE is not a fault; Q970 thermal faults enter the existing latched/rearm path. No firmware poll is credited toward the 1 ms proposed emergency-actuation budget.

The independent [reduced-order loop model](../hardware/2m/review/M5B-E6R1/electrical-model.json) uses actual R511 18 kΩ/R512 10 kΩ/C505 4.7 nF and C506+C634 100.33 nF. TLV9004 GBW is 0.8–1 MHz in the sensitivity; transistor gains/poles are explicitly assumed. All 48 loaded cases are stable. Of three unloaded high-gain cases, two are unstable: total **49/51 stable**. Clamping ordinary SPACE addresses one no-load state but does not prove safe behavior for a disconnected/faulted PA load. No nonlinear saturation, storage-charge, hot SOA or compensation qualification follows from this linear model.

Nominal 800 Hz loop gain is 2.830, AF reconstruction gain 0.9471 and calculated precompensation 1.0446. At 80% depth the PWM-equivalent command is 0.235–2.622 V, within 3.3 V. Both steady AM trough and full crest remain required. The passive [ngspice tail fixture](../hardware/2m/review/M5B-E6R1/spice-tail-result.json) discharges 7.2 V through native bleeder/feedback to 0.1 V in 0.4143 ms, releasing 2.600 µJ; it is not a full modulator simulation. The closed-loop fall is the shaped command; fault kill is faster and bypasses normal shaping.

Ideal 8 ms edges greatly reduce far-offset envelope energy; calculated 99% bandwidth is about 1.61 kHz. This is not a 144 MHz PA or emission-mask validation. Readiness clipping and driver feedthrough are also swept: with an unattenuated 19 dBm feedthrough component, constructive-envelope depth falls from 75% to about 60%, showing why drain gating alone cannot establish AM quality or leakage. Actual gate/drain parasitics, stability, bias recovery, RF clock transitions, converter light-load overshoot, PA saturation, filter transients, harmonics, distortion and clean 5.135 W PEP reserve remain unverified.

Gate B has a specific circuit proposal and a genuine loss-reduction mechanism, but acceptance is OPEN. Gate E is OPEN. [Thermal protection](M5B_E6R1_PA_THERMAL_SAFETY.md) is the decisive unresolved constraint; native PCB implementation remains HOLD.
