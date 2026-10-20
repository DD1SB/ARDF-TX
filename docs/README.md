# Documentation index

The [root README](../README.md) identifies the current CAD evaluation candidates.
Physical RF, AM, thermal, emissions and endurance qualification remains NOT_RUN.
Historical reports and decision statuses have not been rewritten.

## Current hardware

| Board | Decision and design | BOM / sourcing | Bring-up and reproduction |
| --- | --- | --- | --- |
| Controller M6-L2, independently reviewed; final reproduction PASS | [Decision](M6_L2_REVIEW_DECISION.md), [project](../hardware/controller/CTRL.kicad_pro), [review](../hardware/controller/review/M6-L2/README.md) | [48 populations](../hardware/controller/review/M6-L2/population-variants.json), [sourcing](../hardware/controller/review/M6-L2/sourcing-index.json), [manufacturing](M6_L2_MANUFACTURING.md) | [Physical gates](M6_L2_REVIEW_DECISION.md), [reproduce](../hardware/controller/review/M6-L2/REPRODUCE.md) |
| Controller M6-L1, previous independently reviewed baseline | [Decision](M6_L1_REVIEW_DECISION.md), [review](../hardware/controller/review/M6-L1/README.md) | [Population BOMs](../hardware/controller/review/M6-L1/), [sourcing](../hardware/controller/review/M6-L1/SOURCING.md), [LoRa](M6_L1_LORA_VARIANTS.md) | [Bring-up](../hardware/controller/review/M6-L1/BRINGUP.md), [reproduce](../hardware/controller/review/M6-L1/REPRODUCE.md) |
| RF80 M4A-V1R1 | [Decision](M4A_V1R1_REVIEW_DECISION.md), [project](../hardware/80m/production/RF80_V1.kicad_pro), [review](../hardware/80m/production/review/M4A-V1R1/README.md) | [Review BOMs](../hardware/80m/production/review/M4A-V1R1/), [variant analysis](M4A_VARIANT_BOM.md) | [Bring-up](../hardware/80m/production/review/M4A-V1R1/BRINGUP.md), [reproduce](../hardware/80m/production/review/M4A-V1R1/REPRODUCE.md) |
| RF2M M5B-E5 | [Decision](M5B_E5_REVIEW_DECISION.md), [project](../hardware/2m/RF2M.kicad_pro), [review](../hardware/2m/review/M5B-E5/README.md) | [Review BOMs/costs](../hardware/2m/review/M5B-E5/), [manufacturing](M5B_E5_MANUFACTURING.md) | [Bring-up](../hardware/2m/review/M5B-E5/BRINGUP.md), [reproduce](../hardware/2m/review/M5B-E5/REPRODUCE.md) |

Current fabrication ZIPs and settings are in [Manufacturing data](../README.md#manufacturing-data).
M6-L2: [five bare boards](../hardware/controller/review/M6-L2/ARDF_TX_CTRL_M6-L2_JLCPCB_5pcs_BARE.zip),
[full top stencil](../hardware/controller/review/M6-L2/ARDF_TX_CTRL_M6-L2_FULL_TOP_STENCIL.zip),
[final reproduction and disposition](M6_L2_FINAL_REPRODUCTION.md).
The historical M6-L1 ZIP's location in RF80's three-board handoff is intentional.
The [M7 audit](publication/M7/README.md) binds all three hashes without re-export.
It describes the frozen M7 publication; M6-L2 has a separate current-controller review.

## Interfaces, safety and mechanics

- M6-L2 [ESP32/antenna](M6_L2_ESP32_MODULE.md), [FoxPro2 protocol](M6_L2_FOXPRO2_PROTOCOL.md),
  [FoxPro hardware/wiring](M6_L2_FOXPRO2_HARDWARE.md), [GPIO expansion/straps](M6_L2_GPIO_EXPANSION.md)
  and [compatibility](M6_L2_COMPATIBILITY.md).
- [Controller architecture](M6_C1_CONTROLLER_ARCHITECTURE.md),
  [RF interfaces](M6_C1_RF_INTERFACE.md), [power](M6_C1_POWER_AND_BATTERY.md),
  [RTC/timing](M6_C1_TIMING_AND_RTC.md), [safe states](M6_C1_SAFETY_AND_FAULTS.md).
- [Corrected battery ID](M6_C1R1_INPUT_PROTECTION.md),
  [USB ESD](M6_C1R1_USB_ESD_REVIEW.md),
  [LoRa compatibility](M6_L1_MODULE_COMPATIBILITY.md), [feed](M6_L1_ANTENNA_FEED.md).
- [RF80 holes/footprints](M4A_V1R1_HOLE_AND_FOOTPRINT_AUDIT.md),
  [DFM](M4A_V1R1_DFM_REVIEW.md), [first-hardware proposal](M4A_V1R1_PROTOTYPE_TRANSITION.md).
- [RF2M layout](M5B_E5_COMPACT_LAYOUT.md), [RF preservation](M5B_E5_RF_PRESERVATION.md),
  [thermal/mechanics](M5B_E5_THERMAL_MECHANICAL.md), [common enclosure](M5B_E5_COMMON_ENCLOSURE.md).

## Requirements and decisions

[Requirements](requirements.md), [architecture](architecture.md),
[research register](research-register.md) and [ADRs](decisions/) distinguish
accepted, proposed and superseded work. Later native interface contracts and
current decisions identify implemented hardware; old proposals are not its
replacement.

The [2S/4S decision](M2_POWER_ARCHITECTURE_DECISION.md),
[battery architecture](M2_BATTERY_ARCHITECTURE.md) and
[endurance analysis](M2_ENDURANCE_REWORK.md) retain assumptions and unmeasured
targets. Supplier observations have dates and unquoted positions.

## Historical evidence

- [RF80 M3B-E2](../hardware/80m/review/M3B-E2/README.md) and
  [original M4A decision](M4A_REVIEW_DECISION.md) remain references. The
  [self-contained E2 handoff](../hardware/80m/handoff/M4A-E2/README.md) is preserved;
  its oversized PCB and tight-hole requirements are superseded for the current
  manufacturing candidate.
- [RF2M E4R1](../hardware/2m/review/M5B-E4R1/README.md) is the old 180 × 140 mm
  candidate. [Review history](../hardware/2m/review/) retains the RF studies,
  original E4 HOLD evidence and source-joint correction. M5A-R3 restrictions remain.
- [Controller C1](../hardware/controller/review/M6-C1/README.md) and
  [C1R1](../hardware/controller/review/M6-C1R1/README.md) retain electrical history.
  M6-L1 is the previous independently reviewed optional-LoRa closure; M6-L2
  preserves its radio interface and original electrical protections.

Do not run old generators over current sources or overwrite historical reviews.
See [contribution guidance](../CONTRIBUTING.md) and
[third-party notices](../THIRD_PARTY_NOTICES.md).
