# E6R2 carrier-keyed A2A and control sequence

This implements the [E6R1 proposal](M5B_E6R1_CARRIER_KEYING.md), consistent with
[IARU Region1 PartB2025 Appendix1 T2](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf).
Required0.25–1W ERP,70–80% AM, selected Morse speed and full-profile beacon
capability are unchanged. Approximately5.135W clean connector PEP capability
with reserve remains a measurement requirement, not a result of ngspice.

| Native path | E6R2 control |
|---|---|
| U402 pin3 | GND; normal SPACE selects zero drain command |
| R509/Q404 | LOCAL_MOD_OFF clamps helper drive |
| Q405/R985/R986 | NORMAL_OFF emergency input clamp, separate from Q404 |
| U305 pin3 | DRIVER_ON keys small downstream MMIC domain |
| U601 pin1 | CLOCK_OFF inhibits normal RF clock unless both rails ready |
| Q502 gate | NORMAL_OFF retains independent slot-qualified bias clamp |

`LOCAL_MOD_OFF = NORMAL_OFF OR KEY_N`;
`DRIVER_ON = NOT LOCAL_MOD_OFF`;
`RF_NOT_READY = NAND(VPA_READY,DRV_READY)`;
`CLOCK_OFF = LOCAL_MOD_OFF OR RF_NOT_READY`.
U970 nominal thresholds are about0.100V drain and4.57V driver. Comparator
absence has output pulldowns; CLOCK_OFF and RF_NOT_READY have inhibit pullups;
DRIVER_ON has a pulldown. Do not interpret the low drain threshold as RF power
qualification. No new controller GPIO, I²C timing dependency or per-element
ARM reacquisition is introduced. TRAIN_ONLY omits NORMAL circuitry.

1. Configure source and power profile while inhibited; maintain safe retuning.
2. Prepare converter/reference during the allocated slot using the existing
   ARM/lease/progress sequence. PA bias preparation is not Morse keying.
3. Set AF_PWM to zero. Assert KEY approximately2ms before envelope onset.
   Driver small-signal supply starts; RF remains inhibited until readiness.
4. Supply reconstructed sinusoidal AM multiplied by an8ms raised-cosine
   envelope. Initial tests also simulate5/12ms edges. The fixture uses800Hz
   and filter-gain correction; actual amplitude/depth must be calibrated.
5. Ramp AF to zero before KEY falls; retain0.1ms nominal tail for the fixture.
   U402 then selects0V, Q404 disables helper and U305 removes MMIC supply.
6. Slot end/fault overrides shaping through native NORMAL_OFF/fastkill. Keep
   converter/reference preparation only as allowed by the original slot logic.

The target firmware must generate this sequence. No complete operational
firmware or RF waveform capability is claimed. An old continuous-carrier AF
waveform must not be used unchanged with this board.

Eight ngspice transient cases cover BUCK4S/BOOST2S, BF60/BF20, load removal,
overload latch, forced fault and three edge durations. Two AC return-ratio
cases use the TI TLV9002 per-amplifier macro-model as TLV9004 family proxy.
The external copyrighted model is downloaded separately, never MIT-vendored.
Generic BJT parameters, an averaged PA load and finite-impedance prepared
sources are assumptions; converter switching-loop stability and144MHz RF are
not modeled. The AC fixture holds digital safety enabled for linearization.
A1TΩ numerical shunt resolves floating internal model noise nodes; it is not
a physical resistor or alteration of protection. Logs preserve the initial failure.

Nominal modeled VPA spans approximately0.801–7.204V on MARKs and decays near
zero in SPACE. Bias/zenertop consumption remains about2.82mA BUCK/2.84mA BOOST
on the prepared9V rail; whole-transmitter idle power is not zero. Idealized
near-zero pass leakage is not a guaranteed physical leakage specification.
BF20 clips the crest near6.75V; hot gain/headroom needs measurement. A removed
PA load lets VPA reach8.96V, below the prepared9V rail; require transient and
spectrum measurements before RF use. Nominal envelope-model current peaks1.264A;
the assumed current detector/latch interrupts a3×conductance overload. Detector
latency is a modeled10µs scenario, not a measured protection guarantee.

All physical RF, thermal, shutdown timing and outdoor qualification remains **NOT_RUN**. No boards or stencils ordered; no hardware energized.
