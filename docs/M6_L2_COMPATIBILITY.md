# M6-L2 compatibility contract

M6-L2 is a local revision of the 100×100 mm, two-layer universal ESP32-S3 controller. It replaces U10 with ESP32-S3-WROOM-1U-N4 and adds optional FoxPro2/GPIO circuits and normally open strap service access. It does not replace the static shift-register architecture, scheduling authority, arm state machine, RF interfaces or pack-identification protection.

The baseline is M6-L1 (`d94dabd0e40137dc44b2bb94f3707ad4636ca65f`) as published in M7 (`387f275dd4c6ad715a25c0b092961ed36f407833`). RF80 M4A-V1R1 and RF2M M5B-E5 stay at their accepted publication versions. A new frozen-file inventory captures the actual M7 RF and historical-review trees: M6-L1's older frozen RF hash list predates those subsequently accepted RF revisions and is not silently treated as the current publication baseline.

The independent review checks every historical controller pad and connected function, all original power, ground, reset, protection and RF-branch copper identities, both RF connector pin matrices, USB copper, LoRa U70/J7 placement/pin maps and RF-feed geometry, all four mounting holes, and unchanged project rule exclusions. Only U10 identity/body/model, two isolated strap-service nets (GPIO45 stays NC), J3 selection-link nets, intentional UART link insertion and the new option nets are permitted electrical differences. Local digital SPI, RTC-side I²C, KEY, SLOT and SHIFT_LATCH routing is adjusted around the added option escapes without changing any source/destination pad function. The native change audit enumerates every replaced baseline track UUID. New signal escapes may use ordinary 0.60/0.30 mm through-vias (0.15 mm annulus); historical 0.80/0.30 mm ground and power vias and component PTH lands remain. No special drilling, blind vias or filled via-in-pad process is required.

The complete GPIO allocation is exported from the actual native MCU pad map. GPIO35/36/37 and recovery GPIO43/44 are explicitly protected against PSRAM and reallocation mutations.

INIT_OK qualification, SAFE_OE_N, PACK_PRESENT, protected battery ID, hardware default-off, separate RF power switches, RF80/RF2M branch isolation, reset/brownout behavior, application-owned progress, shared-SPI static controls and LoRa safety remain mandatory. Neither new interface supplies RF battery power. FoxPro traffic and UI pins never directly drive ARM, KEY, PROGRESS, PREPARE or a PA enable. Accepted configuration is not permission to transmit.

Population is the product of the existing controller choice, LoRa choice and new option choice:

| Dimension | Choices |
|---|---|
| Controller/RF assembly | FOX_MIN, RF80_FULL, RF2M_FULL, UNIVERSAL |
| Optional radio | NO_LORA, LORA_433, LORA_868 |
| New interfaces | BASE, GPIO, FOXPRO, BOTH |

A no-LoRa/no-FoxPro/no-GPIO build is valid. The new options may be omitted completely. The recovery links are fitted in BASE/GPIO; FoxPro routing links replace them in FOXPRO/BOTH. Strap links are open in all standard builds. Antenna, jack, cable, crimp contacts, RF modules, battery and enclosure are separate assembly/procurement items, not magically included by a PCB BOM.

The host fixtures and C11 protocol core are reviewable foundations, not a full contest firmware release. Required application hooks retain native validation and expose failure. FoxPro supports identification, FoxID, program load/verify/clone, CW-ID transfer/readback, compatibility ID and status. Unsupported oscillator output and over-limit legacy test durations are explicit limitations. Legacy battery display is unavailable for both pack types. No physical test is reported as executed.

Independent review must assess Gates A–F from native CAD, exported connectivity and numerical bounds. Gate G (real ESP32 boot/USB/recovery, actual antennas, genuine FoxPro, voltage faults, GPIO accessories, sequencing, RF/thermal integration) remains NOT_RUN. Gate G measurements are prerequisites for assembled operation, not an automatic blocker to controlled bare evaluation-board manufacture. An unresolved electrical defect or nonzero required CAD result remains a legitimate HOLD.
