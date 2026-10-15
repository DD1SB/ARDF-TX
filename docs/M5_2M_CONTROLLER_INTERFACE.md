# M5A proposed VHF controller electrical contract

Date: **2026-10-15**. This defines a candidate interface for the existing ESP32-S3 controller; it does not redesign or qualify that board. RF2M has no MCU, RTC, EEPROM, DAC or contest scheduler. The RF80 connector is unchanged and is not mechanically interchangeable with this20-pin proposal.

## J101, keyed2×10,2.54 mm candidate

Physical mating part/footprint remains OPEN. Pin numbers are explicit in the native schematic; do not build an unkeyed guessed harness.

| Pin | Signal | Direction at RF2M | Electrical/default |
| ---: | --- | --- | --- |
| 1 | V3V3 | Power in |3.3 V±5%, budget150 mA normal-source/config or training; bounded lab supply initially |
| 2 | GND | Return | Logic return; not PA battery current |
| 3 | I2C_SDA | Bidirectional |3.3 V open drain, local4.7 kΩ pull-up |
| 4 | I2C_SCL | In |3.3 V open drain; any low clears ARM |
| 5 | ARM | In | Rising edge captures context;100 kΩ pull-down |
| 6 | SLOT | In | Positive scheduled RF permission; pull-down; only allowed contest interval |
| 7 | KEY | In | Positive Morse-tone request, not carrier gating; pull-down |
| 8 | PROGRESS | In | Application-generated falling edge≤100 ms; pull-down, no free-running peripheral heartbeat |
| 9 | MUTE_N | In | Low=hard mute; pull-down; host must actively release |
| 10 | PA_RAIL_ADC | Out | VREG_RAW/13 through 1 kΩ, nominal 0–1.12 V; source impedance about 10 kΩ. Controller ADC acquisition/accuracy must be qualified; TRAIN_ONLY pulls this low. |
| 11 | PATH_TRAIN | In |0normal/1training, captured at ARM; pull-down |
| 12 | PROFILE_FULL | In |0reduced/1full, captured at ARM; pull-down |
| 13 | AF_PWM | In |0–3.3 V offset+sine duty waveform;100 kΩ pull-down |
| 14 | LEVEL_PWM | In |0–3.3 V carrier-reference duty;100 kΩ pull-down |
| 15 | PREPARE | In | Allows source/configuration; required in ARM context; pull-down |
| 16 | FAULT_N / arm accepted | Out | High only while captured VALID_ARM remains set; low also means normally disarmed;1 kΩ series |
| 17,18 | GND | Return | Adjacent control/AF returns |
| 19 | MODULE_ID | Passive |10 kΩ2S normal,22 kΩ4S normal,47 kΩtraining-only population; host ADC/pull-up interpretation must be qualified |
| 20 | PA_PREPARE | In | Enables selected converter only with prepared/live source; pull-down; keep0 for training |

The two PWM duties are calibrated to local3.3 V. With gain5.02, initial full-carrier command is1.328 V; reduced example0.727 V. Maximum command, sine amplitude and crest are bounded by the selected RF calibration, never arbitrary duty255. Power-profile changes require disarm/rearm; changes on live PATH/PROFILE inputs cannot transfer the captured RF path or supply profile.

J101 has three logic-return contacts (2,17,18); qualify at least 1 A contact ratings even though its total 3.3 V budget is only 150 mA. J301 is separate protected battery input/PA return, with an initial3 A transient harness budget and2 A fast-fuse candidate whose interruption/I²t remain OPEN. Normal2S and4S converter populations are mutually exclusive and have different hardware voltage windows and assembly IDs. Training-only needs regulated3.3 V, not raw PA supply. No unsafe raw voltage is shared through J101.

## Bus and pin budget

Both RF sources otherwise use Si5351 address0x60. RF80's source is not redesigned here. **Use a dedicated VHF I²C bus**, rather than putting two powered0x60 sources on one unisolated bus. RTC can remain on the existing controller/HF bus. U102 isolates RF2M's unpowered source pins; it is not a complete arbitrary-voltage hot-plug interface.

The proposal consumes14 GPIO/ADC functions including presence/status and rail sense, plus its SDA/SCL pair. Sharing application progress, global mute, Morse timing, two captured profile/path bits and PA_PREPARE with the inactive HF module is possible under a one-band-at-a-time controller policy. A shared PA_PREPARE alone cannot enable the inactive VHF converter: CONV_EN also requires its separate PREPARE/source permission. PREPARE must remain independently controlled to keep the inactive source off. A provisional system budget is35 GPIO including both I²C buses,7 LoRa signals,RTC interrupt,USB,pack sense and basic controls. This depends on the non-PSRAM S3 module's available pins, strap/input-only restrictions and the final controller allocation. **Do not assume an octal-PSRAM variant or an exact controller pin assignment has been qualified.** Controller pin allocation is a pre-layout system review gate, not a hidden new RF processor.

ARM itself is the software certificate that country, role, timing, legal frequency, championship range/separation, modulation and calibration were validated and registers read back. A separate CONFIG_VALID GPIO would repeat the same firmware assertion without measuring RF frequency; it was removed. **No implemented firmware or independent frequency counter currently enforces this certificate.** An unset country or unsupported profile must refuse ARM. No radiated operation is approved by this schematic or by IARU rules.

## Hardware semantics

TPS3431 watchdog and TLV803E reset outputs form SAFE_N. A6-bit HC174 captures only valid ARM context, RF path and profile; unused D inputs are grounded. A Schmitt-conditioned10 ms nominal RC delays RF permission so captured outputs and selected rails can settle. It is not in the asynchronous clear-release path. Raw ARM low immediately removes permission, independent of RC decay.

The principal settled equations, checked from the exported physical gate pins, are:

```text
ARM_CONTEXT = PREPARE & !KEY & !SLOT
CLEAR_A = SAFE_N & MUTE_N & I2C_SCL
RUN_HEALTH = POWER_FAULT_N | PATH_Q | !ARM_DELAY
CLR_N = CLEAR_A & RUN_HEALTH
TX_OK = VALID_ARM & ARM_DELAY & SLOT & ARM
NORMAL_PERMIT = TX_OK & !PATH_Q & POWER_FAULT_N & CLEAR_A
TRAIN_PERMIT = TX_OK & PATH_Q & CLEAR_A
SRC_ON = PREPARE & MUTE_N & SAFE_N
CONV_EN = PA_PREPARE & SRC_ON
PACK_RUN = CONV_EN & PACK_OK_N
RAIL_RUN = CONV_EN & HARD_OK_N
```

On a fault, asynchronous clear destroys the captured valid context. Returning health while ARM stays high cannot recapture it. Both paths are inhibited on reset, expired progress, mute or I²C activity. A missing normal battery does not block a deliberately armed training-only configuration. Analog power faults directly inhibit normal permission as well as clearing context after the ARM delay.

U209 applies CLEAR_A directly to both physical enables ahead of asynchronous register-output skew. No I²C quiet monostable, extra safety MCU or second contest state machine is fitted. SCL stuck low locks out; stuck high cannot retune the source, and genuine missing application progress expires the watchdog. No circuit can diagnose a healthy-looking but incorrect firmware progress pulse as a valid schedule.

## Sequencing and independent supplies

1. Connect ground and3.3 V first. Keep all outgoing controls low. Battery may be present independently: reverse/input FET gates and base pull-downs must keep normal power off without3.3 V.
2. Wait for reset/watchdog startup; begin genuine progress pulses. Keep ARM/SLOT/KEY low. Set path/profile and bounded PWM commands to zero.
3. Release mute; assert PREPARE, configure Si5351 with outputs disabled, read back legal/profile settings, then enable only the selected clock. For normal power assert PA_PREPARE and read PA_RAIL_ADC for unexpected overvoltage. The initial rail may reflect the previous captured profile or remain off at its pack cutoff; do not require the new profile before the ARM edge that captures it. Raw-pack UV/OV remains independent hardware protection.
4. Raise raw ARM with KEY/SLOT low. Keep SLOT low for at least50 ms, confirm FAULT_N/arm-accepted high, and qualify the newly selected10/13.5 V rail using PA_RAIL_ADC before SLOT. Missing/low/out-of-range rail must refuse SLOT and disarm. This controller-level readiness check replaces a redundant local UV comparator. The nominal RC is not a measured minimum delay.
5. Assert SLOT only in the scheduled interval. Ramp carrier command and tone as specified in the AM document. KEY changes audio inside SLOT.
6. Ramp carrier down, clear SLOT, ARM,PA_PREPARE and PREPARE. The volatile source must be configured again for the next interval. For retuning first mute/disarm and wait≥10 ms; SCL clear is a hardware backup.
7. After any fault: controls low, diagnose, wait≥50 ms for discharge/RC recovery, configure/read back again and issue a fresh ARM edge. No automatic rearm or in-contest power reduction.

The future controller must never drive these HC inputs when module3.3 V is absent; no arbitrary hot-plug/backpower tolerance is claimed. Its final interface must provide sequencing or Ioff buffering as appropriate. Local source-switch and I²C isolation prevent the intended gated-Si5351 backpower path. VHF raw power without logic, rapid collapse, broken supply/ground and pin sequencing remain physical gates; default-off Boolean logic is not proof of brownout behavior.
