# M5A-R2 controller contract disposition

2026-10-15. **R1 contract preserved; R2 changes below are proposals, not implemented hardware.** No ESP32-S3/controller/RF80 changes, second MCU, RTC or contest scheduler are introduced.

The [R0 interface document](M5_2M_CONTROLLER_INTERFACE.md), superseded for R1 population codes/rails by the [R1 decision](M5A_R1_REVIEW_DECISION.md), remains the electrical starting point. The [RF80 interface](M3_80M_SCHEMATIC_REVIEW.md) uses a different16-pin connector and different KEY meaning; do not cross-connect it to RF2M. No assertion of a finalized common-controller GPIO allocation or mating harness is made.

| RF2M J101 pin | Signal at RF board | Direction and behavior |
| ---: | --- | --- |
| 1 | V3V3 | In, regulated3.3 V±5%; provisional150 mA budget; actual current must be measured |
| 2 | GND | Logic return |
| 3 /4 | I2C_SDA /I2C_SCL |3.3 V open drain; configure local Si5351; any SCL-low inhibits RF |
| 5 | ARM | In, rising-edge context acceptance; pull-down/default0 |
| 6 | SLOT | In, positive scheduled RF permission, default0 |
| 7 | KEY | In, Morse tone request inside SLOT; it does not mean FM or simple CW carrier switching |
| 8 | PROGRESS | In, genuine application progress falling edge≤100 ms; no free-running peripheral heartbeat |
| 9 | MUTE_N | In, low=independent mute; default low |
| 10 | PA_RAIL_ADC | Out, scaled main rail; new divider/range would require documentation and calibration |
| 11 | PATH_TRAIN | In, captured on ARM;0normal/1training |
| 12 | PROFILE_FULL | In, captured on ARM;0reduced/1full |
| 13 | AF_PWM | In, reconstructed audio/envelope command; encoding change below |
| 14 | LEVEL_PWM | In, reconstructed carrier-level command |
| 15 | PREPARE | In, source/configuration permission; default0 |
| 16 | FAULT_N /arm accepted | Out, high while accepted context survives; low also means ordinary disarm |
| 17 /18 | GND | Adjacent analog/digital signal returns |
| 19 | MODULE_ID | Passive ID; a new module circuit needs a new unambiguous value/code, **OPEN** |
| 20 | PA_PREPARE | In, main converter/bias preparation; default0, not sufficient alone to radiate |

J301 remains separate protected battery input and dedicated PA return; no PA current goes through J101. A module's3 A absolute current rating is not a recommended current-limit setting or qualified harness rating. Exact mating power/control connectors are still pre-existing open items. Independent ground, reverse/voltage protection and sequencing must be reviewed before a PCB.

Input-AM would change normal AF_PWM/LEVEL_PWM calibration: a sine RF voltage envelope requires inverse attenuation mapping, not an assumed sine control voltage. KEY can select a constant carrier command versus the tone waveform, with a shaped transition. Training retains its independent low-power modulation law; the controller must know which branch is selected. The existing pins are sufficient in principle, but no R2 analog summing/clamping/bias circuit or firmware implementation is claimed. VGG adjustment and shutdown are local hardware functions; no additional controller MCU is needed.

The independent fail-off model remains: local supervisor and external watchdog, fresh valid ARM edge with SLOT/KEY inactive, captured path/profile, asynchronous clear on health/mute/bus activity, and deliberate rearming after a fault. The R1 exported-netlist tests pass4096 combinations/36 scenarios. **They validate R1 only.** They do not prove any unimplemented Mitsubishi bias/drain/source shutdown sequence. Retain source inhibit, zero-gate default, drain isolation and physically separate output paths; do not use a complex contest-state machine in gates.

Keep controls low until3.3 V is valid. Supply the gate/attenuator commands in their specified zero state during local-rail ramps. Configure with RF muted and main bias zero, verify legal frequency/profile/calibration, prepare rails, then ARM with SLOT/KEY low. After readiness checks and settling, SLOT may enable RF only in its scheduled interval. Withdraw RF before retuning, changing path/profile or collapsing supplies. Remove ARM and issue a new deliberate edge after faults; restoring power or heartbeat alone must not rearm.

Both local Si5351 devices otherwise share address0x60: use the dedicated VHF I²C bus/isolation policy already recorded. Neither the IARU profile nor a hardware watchdog proves legal frequency authorization. Future software must reject unknown country, invalid channel range/separation, unsupported module ID, uncalibrated ERP and stale configuration before ARM.

No arbitrary hot-plug/backpower tolerance is claimed. Controller outputs must not drive an unpowered module; raw battery may only coexist with unpowered logic when the RF hardware remains safely off. Brownout, lost communication, pulse timing, supply ramps and off-slot residual carrier require the single integrated board's acceptance test once the sourcing gate permits its design.
