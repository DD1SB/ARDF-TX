# M6-L2 ESP32 module and antenna

M6-L2 selects **Espressif ESP32-S3-WROOM-1U-N4**, LCSC **C2980296**: 4 MB quad-SPI flash, **no PSRAM**, external 2.4 GHz antenna. The previous independently reviewed controller is M6-L1, `d94dabd0e40137dc44b2bb94f3707ad4636ca65f`. RF80 and RF2M remain the M7 publication versions.

The engineering source is [Espressif's current combined module datasheet v1.8](https://documentation.espressif.com/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf), particularly the ordering tables, pin definitions, figures 10-1/10-2/10-3 and 11-1/11-2. The two actual manufacturer DXFs were retrieved separately. Their URLs and hashes are recorded in the revision review. Distributor descriptions of the entire product family are not authority to fit a PSRAM variant.

The native footprint is `ARDF_CTL:ESP32_S3_WROOM_1U_N4_L2`. Perimeter lands are 1.5 × 0.9 mm at 1.27 mm pitch, with the original pin-1 orientation. All 40 perimeter contacts retain their absolute board coordinates. The 1U footprint origin moves from (50,35) to (50,38.15) mm because the body is shorter; the lands do not move. The exposed ground centre retains its original absolute coordinates. Its solid land is corrected from the baseline3.9mm square to the manufacturer3.7mm envelope, with nine0.9mm paste windows at the documented centres. The body changes from 18 × 25.5 mm to 18 × 19.2 mm. This is a dedicated 1U body/footprint comparison, not an assumption that two recommended drawings are interchangeable.

The solid exposed ground land and windowed paste pattern are retained. Optional thermal holes in the stock footprint are omitted, as in M6-L1: no filled via, plugged via, via-in-pad, premium drilling or guaranteed tent closure is assumed. Native solder-mask expansion remains 0.03 mm. Ground vias must remain outside solder lands. Inspect HASL flatness, solder wetting, module seating and stencil release on the first assembly. Manufacturer stencil/process guidance still applies; these CAD results are not reflow qualification.

The manufacturer pin matrix and the exported schematic/PCB pad matrix are separate review artifacts. In particular:

| Module contact | ESP32 GPIO | Controller function |
|---|---|---|
| 28 | 35 | RF80_FAULT |
| 29 | 36 | START_N |
| 30 | 37 | USB_VBUS_N |
| 37 | 43 | UART_TX |
| 36 | 44 | UART_RX |
| 15 | 3 | Reserved strap, normally open service link |
| 26 | 45 | Reserved flash-voltage strap, NC; no breakout |
| 16 | 46 | Reserved, input-only strap, normally open service link |

No existing function is assigned a different GPIO. N16R8, N4R8 and other PSRAM substitutions are prohibited; octal PSRAM consumes GPIO35–37. The exact N4 order code is checked in both source metadata and native PCB fields.

The 2.4 GHz port is the connector on U10, approximately (56,31.01) mm in the board coordinate system. It takes first-generation Hirose U.FL / I-PEX MHF I / Amphenol AMC compatible mating plugs, **not MHF4**. The separate J7 connector is for the optional Silicontra **433/868 MHz** module. Do not interchange antennas or infer the LoRa RF band from a chip response. NO_LORA, LORA_433 and LORA_868 remain explicit assembly choices; U70 and its RF feed remain unchanged.

Allow a 10 mm diameter tool/mating area above the U10 antenna connector, at least 8 mm clear height above the PCB locally, and an unobstructed route to the north enclosure panel. With 1.13 mm coax, use a conservative 6 mm minimum bend radius; verify the selected cable's own specification. Seat and extract the plug vertically using the correct tool, support the module, and do not lever the cable against its connector. Clamp the cable to the enclosure after a small service loop; the module connector is not strain relief. No new mounting holes are needed. Keep this area accessible before installing an overlapping RF board or enclosure lid.

The accepted installation uses independently supported side-by-side boards and IDC cables; their mounting holes are not a common direct-stacking pattern. An optional overlapping installation needs an independent carrier: begin with at least20mm spacing for RF80 above the controller, and40mm for RF2M above it to clear its25.2mm downward cooling envelope plus controller components and service space. Keep high-current wiring and the RF2M heatsink away from the Wi-Fi plug and service loop. Prefer the antenna outside the metal enclosure and at least 50 mm from the RF2M heatsink and RF antenna feed wiring as a commissioning starting point, not a proven RF separation. Neither heatsink dimensions nor RF-board copper are changed. Final harness, plug height, extraction-tool access and enclosure dimensions require physical fit checks. Do not route Wi-Fi coax across the PA, converter switch node, RF80 matching network, RF2M output network or RF IDC contact area.

The old PCB-antenna keepout can be removed because that antenna is absent. The LoRa connector underbody keepout and its bottom ground-reference corridor are retained. The two RF ports are labeled and separately illustrated in the revision review. The manufacturer's actual STEP model is downloaded for real KiCad assembly renders; it is not relicensed as project MIT source. Existing dimension-only connector/RTC envelopes retain their explicit qualifications.

Both antenna variants share the datasheet's supply/current specifications: 3.0–3.6 V, 355 mA peak Wi-Fi TX in the listed 802.11b condition and 344 mA peak BLE TX. These are operating-characterization points, not a universal maximum. Retain a 500 mA ESP32 design allowance, local 10 µF plus 100 nF decoupling and the existing 2 A AP63203 supply. The expansion option has a 10 mA header allowance, plus bounded low-current GPIO loads; neither option adds an RF supply path. Reserve1.15A as a short aggregate burst scenario (500mA MCU,300mA RF logic reservations,120mA LoRa and230mA option/fault allowance), within the2A regulator and inductor electrical limits; this is not an approved continuous thermal load. Retain the normal400mA continuous design allowance and qualify actual temperature/transients. The original USB current-limit policy remains: Wi-Fi/RF transmission is disabled on USB-only power. Brownout/reset qualification, INIT_OK, SAFE_OE_N and pack-presence gating are unchanged. Actual rail transient, boot, brownout, antenna gain, matching, coexistence and RF performance are **NOT_RUN**.
