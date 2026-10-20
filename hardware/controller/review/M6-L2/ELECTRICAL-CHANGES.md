# M6-L1 to M6-L2 electrical changes

The reference is controller M6-L1, commit `d94dabd0e40137dc44b2bb94f3707ad4636ca65f`, published in M7 `387f275dd4c6ad715a25c0b092961ed36f407833`. The native project is [CTRL.kicad_pro](../../CTRL.kicad_pro). RF80, RF2M and historical review files are frozen by `frozen-files.json`.

| Area | M6-L1 | M6-L2 |
|---|---|---|
| U10 | ESP32-S3-WROOM-1-N4 | ESP32-S3-WROOM-1U-N4, C2980296, 4 MB flash, no PSRAM |
| Module lands | 40 perimeter lands and ground | All perimeter positions/functions preserved; dedicated shorter body; exposed land corrected to manufacturer's 3.7 mm square; nine 0.9 mm paste windows |
| ESP32 antenna | On-module PCB antenna | Accessible external 2.4 GHz connector; separate from unchanged LoRa J7 |
| Recovery UART | Direct J3 | Default R300/R301 links; physical alternative R302/R303 selects optional FoxPro |
| FoxPro | Absent | DNP three-wire PH connector, grounded-source open-drain MOS transmitter with hardware gate shunt, insulated-gate inverted receiver and passive fault limiting |
| Legacy battery display | Absent | Explicitly unavailable on both pack types; voltage contact bonded to the protected FoxPro return; no battery rail exported |
| General GPIO | No expansion | DNP TCA9534APWR at 0x38 through TCA9517DR; LM66100 reverse blocking; eight individually limited GPIOs and limited header power |
| Spare module pins | Three reserved straps | GPIO3/46 isolated by open service links; GPIO45 retained NC without accessory access |
| Safety and RF interfaces | Accepted default-off architecture | Same GPIO assignments, protection, static shift registers, branch isolation, RF connector functions and independent RF power |

`L1-L2-change-audit.json` compares every historical pad's actual position, size, drill and net, every non-digital original track/via UUID, both 18-pin RF connectors, mounting holes, USB/RTC facilities and LoRa placement/feed geometry. Local digital rerouting is allowed only for the enumerated UART, SPI, RTC I²C, KEY, SLOT and SHIFT_LATCH nets; their terminal functions are preserved. The report lists replaced original copper explicitly. No RF-board source is an output of any L2 reproduction command.

The new 0.60/0.30 mm through-vias have a 0.15 mm annulus and use the ordinary process already accepted on RF80. Original power/ground and component through-hole geometry stays intact. There are no blind vias, filled via-in-pad requirements or new DRC exclusions. Board outline and material construction remain 100 × 100 mm, two layers, FR4, 1.6 mm, 1 oz, green mask, white legend and lead-free HASL.

The portable FoxPro core stages configuration, validates bounds and delegates RTC, native scheduling, persistence and test-transmit authorization through explicit application hooks. It neither creates a second authoritative clock nor directly drives an RF signal. The adapter is a timing reference with target GPIO/timer hooks; real ESP32 interrupt latency and genuine FoxPro interoperability remain NOT_RUN.

Read the actual [gate decision](../../../../docs/M6_L2_REVIEW_DECISION.md) and the machine-readable native/test evidence. This change report does not itself authorize manufacturing or operation.
