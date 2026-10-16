# M5B-E1 electrical corrections

2026-10-16. Evaluation candidate, **NOT RELEASED**. The M5A-R4 electrical baseline is commit `b44fe3b`, tag `m5a-r4`. RF80, M4A, earlier VHF review packages and accepted ADRs are preserved; the preservation check includes their file hashes. No parts, boards or physical tests were commissioned.

The selected architecture remains Si5351 → fundamental filter → PHA-1+ → PD54008L-E → ST output matching and elliptic filter, with final-drain sine modulation and a separate low-power training output. The changes below resolve implementation defects and define evaluation landings; they do not establish measured RF performance.

| Change from R4 | Reason and resulting behavior |
| --- | --- |
| U305 TPS22919 → TPS22810DBVR | Removes the 5.5 V recommended/6 V absolute-limit load switch from the driver fault path. The new switch is rated for 18 V recommended, 20 V absolute. DBV physical mapping is 1 VIN, 2 GND, 3 EN, 4 CT, 5 QOD, 6 OUT; it is verified in exported CAD and native pads. |
| U950 TLV76701DRVR, R950/R951, C950/C951 | Adds a 5.456 V preregulator ahead of the existing 5 V TLV761. A single regulator short no longer leaves only an assumed fast isolation time between the upstream rail and MMIC. This is a second barrier, not a comprehensive surge guarantee. |
| R413 8.2 Ω → 4.7 Ω, 1 W | Restores useful preregulator headroom at driver current. The reservoir still attenuates rapid faults. |
| R815 75 kΩ → 73.2 kΩ, 0.1% | Lowers driver OV threshold to approximately 5.269 V nominal, analytical 5.173–5.365 V including stated reference/divider tolerances. |
| R952, normally fitted 0 Ω | Separates the physical MMIC supply from the power-only qualification node. Omit it, and initially omit U501, during supply fault tests. |
| R309 0.1 Ω → 0.068 Ω; R828 10 kΩ → 5.11 kΩ | **Confirmed additional R4 defect:** the old comparator divider needed approximately 3.752 V from an INA180 powered at 3.3 V. The corrected scale needs 2.443 V and trips at approximately 1.797 A. Static scale is corrected; dynamic shutdown remains NOT_RUN. |
| L604 Murata 180 nH → Coilcraft 1812SMS-R15JLC 150 nH | **Confirmed bias-margin defect:** the old choke's maximum 1.65 Ω DCR could lose 0.297 V at 180 mA. The selected choke has 33 mΩ maximum DCR, approximately 5.94 mV at that current, Q≥100 at 150 MHz and 750 MHz SRF. The changed RF feed impedance remains an RF acceptance item. |
| L634 18 nH → 47 nH; C631 56 pF → 22 pF; C633 27 pF → 22 pF | A documented initial adaptation of the original PD84001 interstage to a nominal 50 Ω driver. The calculation includes the retained L606=33 nH bias feed. It is an assumed-device evaluation match, not a manufacturer-verified 50 Ω input. See the RF layout note. The ST output network is unchanged. |
| R650 series 0 Ω; R651 49.9 Ω DNP | A liftable DC-blocked driver/final interface. For driver-only alignment lift R650 and fit R651 as a temporary 50 Ω load. Never fit the load during normal PA operation. |
| R602 71.5 Ω, R603/R604 96.5 Ω | Initial 10 dB source π pad; R602 is the series element. Qualified 6/8/10 dB populations permit measured drive adjustment without a premium driver. |
| C960/C961 local 22 µF/35 V | Separate boost/buck input reservoirs close their respective converter current loops. Only the selected converter's capacitor is fitted. |

The seven R4 footprint warnings are closed with exact connector, capacitor and Coilcraft landings. Further physical corrections qualify Bourns converter-inductor lands, 1008CS filter-inductor lands, the controller header holes, the 10 Ω/1 W resistor package and the remote NTC attachment. Reference values in the final output match/filter are preserved.

U201/U304 and their decoupling were relocated locally to permit clean control-pin escapes. These are placement changes only. The PD54008/PHA source/ground solder apertures and thermal vias are explicit PCB features. Transmission-line symbols now have actual, length-defined copper footprints; they are excluded from purchased BOMs.

The controller contract remains the 20-pin RF2M interface. The older M5A interface document contains superseded 13.5 V command/rail examples and unidentified connectors. For M5B use the actual schematic, J101 Wurth 61202021621, module IDs 18.2 kΩ/39.2 kΩ/82 kΩ, nominal full converter rail 9.021 V and reduced 4S rail 7.510 V. Hardware equations, captured path/profile, watchdog, deliberate rearming and independent RF ports are retained. No new MCU or contest scheduler is added.

Reproducible calculations, netlist/pad assertions, original regression results and exact final CAD status are in [the review directory](../hardware/2m/review/M5B-E1/). [Power and thermal](M5B_E1_POWER_AND_THERMAL.md) defines fault boundaries; [bring-up](M5B_E1_BRINGUP.md) defines the single-board qualification sequence. No Boolean or ERC result proves analog startup, AM, hot SOA or safe battery transients.


## M5B controller connector contract

J101 Wurth61202021621 is a keyed2×10,2.54 mm header. Number contacts from the component-side pin1 marker; do not infer cable numbering from the back of the connector. Logic is3.3 V. Grounds2/17/18 carry logic/AF return; J301 carries PA current separately. Normal controller outputs default low, including MUTE_N low=muted. No RF-side scheduler is added.

| Pin | Net | Direction at RF2M / behavior |
| --- | --- | --- |
| 1 | V3V3 | Regulated3.3 V input,±5%,150 mA budget |
| 2 | GND | Logic return |
| 3 | I2C_SDA | Open-drain bidirectional,local4.7 kΩ pull-up |
| 4 | I2C_SCL | Open-drain input;low clears permission |
| 5 | ARM | Input,rising-edge valid context capture;pulldown |
| 6 | SLOT | Input,positive scheduled interval permission;pulldown |
| 7 | KEY | Input,selects sine rather than DC carrier reference inside SLOT;pulldown |
| 8 | PROGRESS | Input,genuine application progress edge≤100 ms;not a free-running PWM heartbeat |
| 9 | MUTE_N | Input,low hardware mute;pulldown |
| 10 | PA_RAIL_ADC | Output,regulated upstream rail/13 through1 kΩ;ADC acquisition still qualified by controller |
| 11 | PATH_TRAIN | Input,captured at ARM;0normal/1training |
| 12 | PROFILE_FULL | Input,captured at ARM;0reduced/1full |
| 13 | AF_PWM | Input,0–3.3 V PWM offset+sine reference |
| 14 | LEVEL_PWM | Input,0–3.3 V carrier reference PWM |
| 15 | PREPARE | Input,allows source configuration;pulldown |
| 16 | FAULT_N | Output,high only while valid ARM remains captured;low includes deliberately disarmed |
| 17,18 | GND | AF/control returns |
| 19 | MODULE_ID | Passive population resistor18.2k2S/39.2k4S/82k training;host interpretation unqualified |
| 20 | PA_PREPARE | Input,selected normal converter preparation;keep low for training |

Use a dedicated VHF I²C bus because both RF modules' Si5351 address is0x60. The existing local Ioff/bus isolation does not make arbitrary unpowered GPIO hotplug safe. Controller sequencing must keep inputs inactive without module3.3 V. Battery alone must not arm RF; verify actual brownout and ground sequencing during commissioning.

The retained312.5 kHz PWM reconstruction uses two unity Sallen-Key sections,10k/10k and4.7n/4.7n, approximately3.39 kHz/Q0.5. Start with800 Hz sine, configurable. The actual PA feedback gain is**2.8** (18k/10k), superseding older5.02-gain interface examples. Initial full MOD_COMMAND is1.429 V±1.143 V at80% voltage depth; reduced is0.794 V±0.635 V. Calibrate PWM duties to measured3.3 V and RF envelope, never arbitrary maximum duty. No production firmware is provided.

Before ARM, validate country/frequency/role/calibration, read back the source, keep KEY/SLOT inactive and set captured path/profile. After ARM keep SLOT low≥50 ms, confirm accepted state and qualified selected rail, then permit scheduled RF. For retuning/path/profile changes: mute/disarm first and require a fresh ARM edge. Timeout, reset, bus activity or fault destroys permission; recovering health while ARM stays high cannot rearm. This is the existing netlist-tested behavior, not a physical race-timing qualification. Frequency legality is the future controller's validated configuration responsibility, not an independent hardware frequency counter.

