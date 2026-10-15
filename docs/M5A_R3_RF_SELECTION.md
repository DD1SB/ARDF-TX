# M5A-R3 — reference selection

Dated 2026-10-15. **PRIVATE CONSTRUCTION DERIVATIVE / NOT RELEASED. All ARDF-TX hardware tests NOT_RUN.** No orders, PCB fabrication, assembly or transmission. M5A-R1 remains the archived fallback; RF80, M4A, the controller and accepted ADRs are unchanged.

**Select DL3BBX as the one schematic foundation. Do not adopt this BOM as the fleet replacement.** It is the only fully traced mandatory candidate that publishes several watts PEP with working supply AM. It still does not prove the retained upper-ERP/headroom target and it is presently more expensive than R1.

| Same-scope consideration | DF1FO MaxiTX | DL3BBX derivative selected for review | G3ZOI historical1W |
| --- | --- | --- | --- |
| Built evidence | Four prototypes and several named reproductions | Article reports real construction and >3WPEP/>90% AM | Dutch documentation shows schematic/completed sets |
| Maximum reported power |1.2W **peak**,12V,rectangular modulation |**>3WPEP**,13.8V; lower bound, not a maximum measurement |1W label without usable calibrated sineAM carrier/PEP conditions |
| At−1dBd/80%AM |1.2W permits0.294WERP,0.234W with1dB reserve |3W reference permits0.736WERP,0.584W with1dB reserve; actual maximum unknown |No justified4–5W PEP evidence |
| RF adaptation | ICS525→Si5351; KT610 drive/cooling, sine modulator changes | Remove first oscillator/doubler; retain T3/T4/T5, original L4–8 and matches; replace tone source/pass package | Incomplete original construction pack, legacy final |
| Tuning/construction | One principal trimmer plus reproducible wound coils | Seven adjustments, legacy factory coils, TO39 heat/stand-off; more work | Complete current alignment/layout source not found |
| Current parts | KT610b genuine fleet supply/pin map unresolved | BF981 NOS, Central2N4427 EOL, exact MRF237 maker/lot unresolved | BFW16A/2N4427 legacy sourcing unresolved |
| Normalized complete cost |Not quoteable: KT610 identity/source and original source-interface adaptation unresolved; historical bare design prices excluded|Full2S **€93.16** at10 including common source/safety/training; conditional allowances|Not quoteable from incomplete source/BOM; no invented quantity discounts |

## Precisely what is reused

Three of the five original RF stages remain: BF981 second doubler,2N4427 driver and MRF237 final. The five retained adjustable coils, interstage trimmer and output network retain original identities and connectivity. **36 two-terminal reference positions** plus two pots are regression checked. Original Darlington collector-supply modulation, DC collector-feedback trim and audio RC/AC-coupling path remain. The proposed TIP127 is a package/current-source modernization; it has not inherited the original's RF/thermal measurements.

The removed T1/T2 crystal/multiplier circuitry, NE555 audio oscillator, and external historical timer are replaced by the existing common controller and synthesizer. A72MHz fundamental filter and source gate are new. Keeping one multiplier is deliberate: TP5 is not a documented50ohm node, and replacing everything with Si5351 at144MHz would introduce a new drive/matching problem. The revised source drive is still an acceptance gate, not presumed identical to the original tuned oscillator amplitude.

The existing separate training RF circuit and independently tested VHF interlocks remain. There is no new PA coupon, PA-family search, new MCU or fourth board. The GPIO connector is unchanged, but **passive revision IDs change**. **Normal CLK0 programming changes from RF to RF/2**, so R1 configuration must not run against R3. Same PLL can feed direct-RF training CLK2.

## Complete R3 controller contract

J101 remains a20pin2.54mm keyed header candidate; exact manufacturer/mating geometry OPEN. Logic is0–3.3V, maximum intended3.465V. Host must not drive an unpowered RF board; no arbitrary hot-plug/backpower tolerance is promised. Separate J301 carries protected battery and its power return; no PA current in J101. Target3.3V budget≤150mA, to be measured. Ground contacts2/17/18 serve logic/AF return; RF/PA currents return separately to the battery star, not through them.

| Pin | Net / direction at module | R3 behavior |
| --- | --- | --- |
|1|V3V3 input|Regulated logic/source supply; ground first|
|2|GND|Logic return|
|3,4|I2C_SDA/SCL bidirectional|Dedicated VHF bus0x60,≤400kHz; RF80 also uses0x60, so do not share unisolated sources. Local source/I2C switching retained|
|5|ARM input|Fresh rising edge captures valid context/path/profile;100k pull-down; no automatic rearm|
|6|SLOT input|Scheduled carrier permit,100k pull-down; hardware gates normal source and rail|
|7|KEY input|Sine-tone Morse key inside SLOT; inactive during ARM;100k pull-down|
|8|PROGRESS input|Application progress edges≤100ms apart; independent TPS3431 lease/POR fail-off. Never free-run a hardware timer as application-liveness substitute|
|9|MUTE_N input|Low inhibits; defaults low|
|10|PA_RAIL_ADC output|Raw regulator rail divided by17,then1k series; about0.812V at13.8V. Verify before SLOT; train-only hard pull-down. ADC source impedance/acquisition calibration OPEN|
|11|PATH_TRAIN input|0normal/1training captured at ARM; default0|
|12|PROFILE_FULL input|0reduced/1full captured at ARM; default0; live changes do not transfer path/profile|
|13|AF_PWM input|Offset+sine312.5kHz PWM,initial800Hz tone;3.3V logic. Calibrated amplitude per profile; no S3DAC assumed|
|14|LEVEL_PWM input|Equal-offset no-tone reference; **not** the old D45H11 servo voltage-to-PA calibration|
|15|PREPARE input|Allows powered source/configuration; defaults0|
|16|FAULT_N output|Captured valid-arm indication through1k; low when disarmed/faulted, not a multiplexed telemetry bus|
|17,18|GND|Adjacent AF/control returns|
|19|MODULE_ID passive|**15k2S /33.2k4S /75ktraining R3**. Reserve distinct IDs; reject unknown/ambiguous readings and old R1 IDs12.1k/27.4k/47k. Host pull-up/ADC windows need qualification|
|20|PA_PREPARE input|Converter preparation;0in training. Cannot by itself enable RF|

Firmware must bind decoded R3 ID, pack population, source half-frequency mapping, legal country/profile, carrier/AM/ERP calibration and RTC schedule before ARM. No such firmware is implemented here. Supply raw/control independently only under the documented grounding/sequencing constraints. Do not share the normal-mode PWM scale or calibration from R0/R1's closed-loop supply modulator.

Sequence: controls low →stable3.3V/POR/progress →MUTE_N+PREPARE with ARM/SLOT/KEY low →configure/read back source with RF gates off →prepare converter →check correct regulator rail/profile →fresh ARM with valid context →wait≥50ms/confirm status and rail →scheduled SLOT →key only sine tone →clear SLOT,ARM,PA_PREPARE,PREPARE before retuning. After any fault diagnose and repeat from controls low; restoring health with ARM high never rearms. Physical RC/reset/inrush/quiet timing still requires measurement.

## Why no integrated PCB is claimed

The exact purchasable RF-device manufacturer/physical package is unresolved, and the Neosid current red-core range conflicts with the historical nominal. No final footprint is assigned by generic transistor name. Original Eagle4.16 binary import was unavailable; original DL3BBX layout is a published raster, not a calibrated native PCB file. A fabricated complete board with guessed pin order/coil geometry would violate this task.

The shortest practical correction is **one confirmed RF component set with spare quantities and exact package evidence**, plus Neosid range/geometry confirmation, followed by one integrated board using the original RF placement. It is not a separate RF-transistor characterization program. The present result is a complete editable **candidate schematic**, with explicitly OPEN physical implementation. It is neither proof of a low-cost fleet nor authority to lay out/order unresolved parts.
