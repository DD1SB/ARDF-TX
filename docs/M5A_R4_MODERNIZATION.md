# M5A-R4 — practical modernization

Dated **2026-10-16**. **M5A-R4 electrical candidate — NOT RELEASED.**
All physical tests are **NOT_RUN**. No purchasing, fabrication, assembly or RF operation has occurred.
RF80, M4A and accepted ADRs are unchanged. R3 is preserved at tag `m5a-r3`
(`daf994c`); R0/R1 tags and the R1 native archive remain available.

The implemented candidate is **Si5351 → gated fundamental filter → PHA-1+ → ST-derived interstage → PD54008L-E → ST output matching → ST elliptic LPF**. It retains the independent training branch and common controller. The changed driver/interstage boundary remains an electrical hold before layout. No RF performance has been measured on this derivative.

| Historical/R3 block | Implemented R4 disposition | Consequence |
| --- | --- | --- |
| Crystal oscillator, first doubler and local timer | Omitted | ESP32/RTC and Si5351 already perform these functions |
| BF981 last doubler, 2N4427 and MRF237 | Removed | Direct 144 MHz replaces the 72 MHz multiplier chain; one economical MMIC drives the active ST final |
| Five Neosid modules and two RF trimmers | Removed | Their original multiplier/bipolar matching functions disappear; no arbitrary power-inductor substitution |
| Historical collector modulation | Supply-modulation principle retained | R1 D45H11/BD139 voltage servo controls drain supply; gate bias and RF drive stay fixed |
| R1 assumed output network/nine-pole LPF | Replaced | Actual ST Figures 17/14 provide output matching and elliptic filtering |
| Discrete driver supply switch | TPS22919 on regulated 5 V | Removes Q304, Q308, R408–R412 and D308; adds U305, C940 and R940 |
| Cascaded permissions | Repacked into HC21/HC11 | One fewer permission IC; captured path/profile and deliberate rearm retained |
| Boost reduced setting at 7.5 V | Fixed 9.021 V for 2S | A boost cannot regulate below a charged 8.4 V pack; Q307/R414 removed |
| Driver reservoir charged every slot | Precharged before ARM | Pass, bias, driver and clock controls stop RF; analog faults still disconnect the upstream rail |
| Expensive low-drive RF inductor allowances | Murata RF wirewound family | Exact 56 nH price observed; other values remain estimates |

The ESP32 owns scheduling, frequency/legal-profile validation, PWM references and ordinary power sequencing. No RF-side MCU, local RTC, EEPROM, scheduler or precision RF detector is added.

| Supporting function | Classification/disposition | Distinct purpose |
| --- | --- | --- |
| Si5351, reference and source filter | Essential RF performance: retain | Programmable VHF carrier, stability and harmonic control |
| Source power/I²C isolation | Essential protection: retain | Avoid source backpower and uncontrolled RF during reset/configuration |
| Watchdog and POR | Essential protection: retain | Stop RF after controller loss/brownout independently |
| ARM/path latch and final permissions | Essential protection: simplify gates | Prevent held-ARM recovery and live normal/training transfer |
| Pack window, current, PA/driver OV, thermistor window | Essential protection: retain | Battery BMS protection does not replace RF-stage protection |
| PWM filters, selector and voltage feedback | Essential AM performance candidate: retain | Filter the S3 reference and control drain waveform under load |
| Independent training buffer/BJT/filter/pad | Essential separate output: retain | Training works with watt PA and converter absent |
| Permanent RF metrology/laboratory connectors | Omitted | Shared instruments perform acceptance |

The full assembly has **264 physical parts / 24 ICs**, versus 247 / 22 in R3. Training has **103 / 13**, versus 102 / 14. There is no claimed total-part-count saving: a MOSFET bias network, actual MMIC supply and true-AM servo need support parts. Cost falls mainly by eliminating obsolete RF prices. Permission gate packing removes one IC relative to the unreduced modern implementation. Five HC gate/register packages plus POR/watchdog implement permissions, not another contest scheduler.

## Controller interface

The existing 20-pin logical interface remains. Signals are 3.3 V. Current figures below are design budgets requiring qualification.

| Pin | Signal | Direction | Contract |
| --- | --- | --- | --- |
| 1 | 3.3 V | Controller → RF | 3.135–3.465 V; budget ≤150 mA, not measured |
| 2 | GND | Return | Logic return; separate PA current return |
| 3 | SDA | Bidirectional | Dedicated/module-selected I²C at 0x60 |
| 4 | SCL | Controller → RF | Any low clears ARM; idle high alone grants no permission |
| 5 | ARM | Controller → RF | Fresh edge captures valid context/path/profile; default low |
| 6 | SLOT | Controller → RF | Scheduled carrier window; default low |
| 7 | KEY | Controller → RF | Within SLOT: 0 carrier reference, 1 sine reference; low while arming |
| 8 | PROGRESS | Controller → RF | Application progress edges ≤100 ms; never a free-running PWM |
| 9 | MUTE_N | Controller → RF | Low inhibits; 100 kΩ default pulldown |
| 10 | PA_RAIL_ADC | RF → controller | Scaled upstream rail; verify acquisition and calibration |
| 11 | PATH_TRAIN | Controller → RF | Captured: 0 normal, 1 training; no live transfer |
| 12 | PROFILE_FULL | Controller → RF | Captured; host applies corresponding DC/AF calibration |
| 13 | AF_PWM | Controller → RF | Offset plus sine; initial PWM carrier 312.5 kHz |
| 14 | LEVEL_PWM | Controller → RF | Carrier reference; same DC offset as AF_PWM |
| 15 | PREPARE | Controller → RF | Source/configuration permission; default low |
| 16 | FAULT_N | RF → controller | Actually VALID_ARM through 1 kΩ: low also means unarmed |
| 17/18 | GND | Return | Additional logic returns |
| 19 | MODULE_ID | Passive | R4: 18.2 kΩ 2S / 39.2 kΩ 4S / 82 kΩ training; controller pullup/ADC |
| 20 | PA_PREPARE | Controller → RF | Precharge normal rail; keep low for training |

Protected power enters J301 with its own return. Establish 3.3 V before raw PA power and remove raw power first until sequencing/backpower behavior is qualified. Do not drive arbitrary GPIOs into an unpowered module. Si5351 uses a switched, isolated bus. Both CLK0 and CLK2 now produce the actual RF frequency: PLL = 6 × RF, multisynth divide-by-6, CLK1 disabled. R3's half-frequency configuration and IDs are incompatible.

For configuration, hold ARM/SLOT low, release MUTE_N high and assert PREPARE. **MUTE_N low turns the source off**, so it cannot remain low during programming. I²C activity clears the context. Configure/read back frequency and establish genuine progress pulses. PA_PREPARE may precharge the normal rail while RF clamps remain asserted. Raise ARM only with KEY/SLOT low and settled references. Captured 4S profile can change the buck setpoint: wait for ADC-confirmed settling before SLOT. To retune/change path/profile, withdraw SLOT, assert MUTE_N low and lower ARM; then power the source with ARM/SLOT still low, configure and deliberately rearm. A held ARM must not recover after a fault.

Training omits the entire PA/MMIC, converter/LDO, normal matching/filter/connector and PA monitoring/heat hardware. R519 links RUN_HEALTH to 3.3 V only when normal U207 is omitted. Training-only R517 is a 0 Ω link from MOD_DRIVE to VPA_FB, closing unity feedback around unused U401C; R518 grounds its positive input. R932 defines the unused normal RC input. Never fit these links across the full assembly's feedback. Watchdog, POR, fresh ARM, path selection, KEY/SLOT and independent training RF remain active.

[Native schematic](../hardware/2m/RF2M.kicad_sch), [PDF](../hardware/2m/review/M5A-R4/RF2M.pdf), [component delta](../hardware/2m/review/M5A-R4/component-delta.json). R3 retains the historical DL3BBX permission restrictions. R4 independently transcribes attributed manufacturer circuit facts; complete third-party articles, artwork and Gerbers are not redistributed or relicensed. No accepted ADR is changed.
