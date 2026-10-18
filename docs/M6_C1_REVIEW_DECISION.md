# M6-C1 — controller engineering review decision

**GO for independent review of the base controller PCB. HOLD the optional LoRa population. No manufacturing, acceptance tag or operational release is authorized.**

The implementation is a native KiCad 10.0.6 controller with a fully routed **100 × 100 mm**, two-layer, 1.6 mm standard FR4 / 1 oz PCB. It uses green mask, white legend, lead-free HASL and ordinary 0.80/0.30 mm through vias. No custom stackup, controlled-impedance service, filled vias or factory assembly is required. The [review package](../hardware/controller/review/M6-C1/README.md) contains the fresh fabrication dataset, schematic PDF, assembly variants, actual KiCad renders, electrical-test netlists and reproduction commands.

## Implemented hardware

- **ESP32-S3-WROOM-1-N4**, 4 MB flash and no PSRAM; GPIO35–37 are required. GPIO3/45/46 remain unused straps. GPIO0 is recovery BOOT. [Every GPIO and static-output bit](../hardware/controller/review/M6-C1/GPIO-allocation.json) is allocated explicitly.
- **RV-3032-C7-32.768KHZ-2.5PPM-TA-QA** RTC with CR1220 primary backup through BAS116 and 1 kΩ. The diode prevents charging the primary cell. Commission BSM=10, charger OFF and read back; factory defaults do not establish working backup. The calculated daily timing budget is 0.735 s including synchronization, aging allowance and register quantization; actual timing is NOT_RUN.
- Two independent ESP I²C controllers, with TCA9517 isolation on each RF branch. RTC shares only the RF80 host side. Hardware disables both RF bus branches while ARM is high. Identical Si5351 addresses remain isolated; an RF branch can be disconnected over SPI without communicating on its stuck bus.
- Separate TPS22918DBVR switched logic rails with documented hot resistance, Ioff control/status buffers, powered-off-protected analog inputs, and reset/pack-present/INIT gating. One BAND2 bit selects mutually exclusive control banks. Local RF watchdogs consume application-owned progress, not autonomous PWM.
- Protected 6.0–16.8 V controller input, 1 A /63 V Bourns fuse, reverse blocking, TVS, AP63203 buck, battery/identity measurement and USB current limiting/diode isolation. The dedicated RF pack currents use an external fused star harness, not IDC cables or controller tracks. One identified common pack is supported; independent mixed packs are not.
- Native USB-C, CC resistors, USBLC6 protection, VBUS detection, reset/BOOT recovery, STOP/START and minimal status LEDs. LED states are software indications, not measured RF output.

The RF80 16-pin and RF2M 20-pin connectors match fresh exports from their actual native schematics. SCL/SDA order differs and is preserved. RF80's open-drain FAULT and RF2M's push-pull VALID_ARM semantics remain distinct. PREPARE, PA_PREPARE, SLOT and KEY are separate. The [binding interface specification](M6_C1_RF_INTERFACE.md) resolves obsolete RF2M identity values, RF80 power-bit ordering and the source-preparation sequence against native circuits.

RF80, RF2M, accepted ADRs and the supplied M4A working changes are unchanged. SHA-256 preservation checks cover 1,220 supplied RF files. The supplied RF80 production candidate is working-tree input outside this controller commit; its fresh interface netlist and hashes are frozen in the review package for traceability. Strict re-extraction/preservation reproduction requires that supplied RF baseline, as documented.

## Verification

| Check | Actual result |
|---|---|
| KiCad ERC | 0 errors, 0 warnings |
| KiCad DRC | 0 errors, 0 warnings |
| Unrouted / schematic parity | 0 /0 |
| Exclusions | none |
| Ignored category | default `tuning_profile_track_geometries`; no tuning patterns exist |
| Native JLC geometry audit | PASS; 51,466 foreign-copper pair tests; no copper slivers |
| Manufacturing margins | 0.15 mm minimum track; 0.25 mm minimum nominal via/PTH annulus |
| Physical electrical assertions | 693 pad instances, 38 independent critical package maps, 36 RF connector pins |
| Controller logic | 4,096 enable combinations; 20 native electrical/value/population mutations rejected |
| Native DFM mutations | 7 rejected |
| RF80 read-only replay | 256 truth cases, 31 states, 16 RC corners, 2 polarity mutations |
| RF2M read-only replay | 4,096 combinations, 39 states, 16 preparation truth rows |
| Host HAL/state foundation | 32 Python tests; strict C11 waveform/GPIO fixture passes |
| Export audit | 9 Gerbers, 427 PTH /6 NPTH, 693 pad /381 via IPC records checked |

These are CAD, calculation and host-model results. No firmware-only test proves power sequencing, timing latency, backfeed, RF silence or analog behavior. Exact reports are in [final-checks.json](../hardware/controller/review/M6-C1/final-checks.json).

## Cost and mechanics

Candidate component costs below are **net EUR/unit**, excluding VAT, freight, cell, cables, harness, PCB, labor, RF boards and enclosure. Most small parts remain unquoted allowances; quantity20 uses the observed10-price where no supported20-break exists.

| Population | Quantity1 | Quantity10 | Quantity20 | Unquoted allowance at10 |
|---|---:|---:|---:|---:|
| FOX_MIN | 21.07 | 18.71 | 18.71 | 10.87 |
| RF80_FULL | 21.34 | 18.98 | 18.98 | 11.14 |
| RF2M_FULL | 21.38 | 19.02 | 19.02 | 11.18 |
| UNIVERSAL, no LoRa | 24.97 | 22.06 | 22.06 | 13.41 |
| UNIVERSAL + LoRa, **HOLD** | 31.39 | 27.68 | 27.68 | 19.03 |

The historical €14.93 controller estimate is not achieved. Compensated RTC, safe I/O isolation and current sourcing observations account for the revised basket. FOX_MIN has140 fitted positions versus185 universal, with no separate PCB or MCU platform. Its100 ×100 mm outline remains a mechanical overhead to evaluate during compact Fox integration. The unquoted bare-board planning model is €9 /€14 /€24 for5 /10 /20 boards, plus €10–25 freight allowance and optional €8–20 stencil; it is not a JLC quotation or CAM acceptance.

The initial installation uses independently supported boards and short, continuity-tested keyed IDC cables. Four3.2 mm mounting holes do not imply a common RF-board bolt pattern. Use nylon M3 supports initially, preserve ESP antenna clearance and USB access, and keep the RF2M's25.2 mm underside cooler projection with at least30 mm mechanical support space. Airflow and final enclosure fit remain unqualified.

## Open items and release gates

1. **Optional LoRa population HOLD:** manufacturer `SX1262ZTR8-GC` versus distributor `SX1262TR8-GC` equivalence, exact land tolerances/end-offset and the short RF launch are unresolved. The nominal optional landing is explicitly OPEN; all base variants omit this group. Autonomous operation remains available without it.
2. Reconfirm exact non-E4 LVC244, other unquoted small-part prices, connector/cell-holder stock and harness parts. AP63203 has an observed LCSC channel while the observed Mouser page is out of stock. No stock has been reserved.
3. Qualify USB-only startup/current, full-speed enumeration/eye behavior, hot reverse leakage/clamp and VBUS detach. The short data routes are not claimed to be factory-controlled90Ω lines.
4. Measure 3.3 V at each RF connector, cable ground offsets, reset/brownout decay, Ioff/backfeed and actual regulator/diode temperature. Normal controller steady design budget is0.40 A; the0.92 A allocation is a short burst, not a continuous thermal rating.
5. Qualify RTC initialization/backup/drift, target PWM/timer latency, genuine-progress failure, actual module arming/fault sequences and cable-loss silence. Target production firmware is not part of this milestone.
6. Retain all RF80/RF2M RF, AM, thermal, antenna, spectral and12 h/24 h physical qualification gates. RF2M-E4R1's existing thermal/assembly qualifications are not closed by this controller.

**Shortest next step:** independent controller schematic/layout/interface review, resolve any findings, then obtain explicit authorization for a five-board quotation. Build one controller in stages using [BRINGUP](../hardware/controller/review/M6-C1/BRINGUP.md); begin with RF raw power disconnected and LoRa DNP. All physical gates remain **NOT_RUN**.
