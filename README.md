# ARDF-TX

**Hardware evaluation stage — physical transmitter qualification pending.**

ARDF-TX is a modular open-source transmitter platform for Amateur Radio Direction
Finding (ARDF), with separate 80 m and 2 m RF boards and a common ESP32-S3
controller. Its goals are affordable reproduction, ordinary PCB manufacturing,
autonomous contest timing, optional remote operation and explicit hardware
transmitter interlocks.

The repository contains editable KiCad sources, development history, engineering
decisions, population BOMs, verification tools and revision-specific fabrication
data. The RF designs and M6-L2 controller have independent CAD reviews. The fresh
[M6-L2 final reproduction](docs/M6_L2_FINAL_REPRODUCTION.md) supports **GO for five
controlled bare controller evaluation boards**. Physical qualification and release
for operation remain pending. No PCB has been ordered or tested.

## Hardware architecture

| Module | Current candidate / source commit | PCB | Main functions | Native KiCad project | Engineering review |
| --- | --- | --- | --- | --- | --- |
| Common controller | **M6-L2 — ESP32 external antenna, FoxPro2 compatibility and optional GPIO expansion** / [`89f5a7d`](https://github.com/DD1SB/ARDF-TX/commit/89f5a7df6ccb4dec8fcea10e7c810a9981342ce4); previous baseline [`d94dabd`](https://github.com/DD1SB/ARDF-TX/commit/d94dabd0e40137dc44b2bb94f3707ad4636ca65f) | 100 × 100 mm | External-antenna ESP32-S3, RTC, USB-C, optional LoRa/FoxPro2/GPIO expansion and default-off interlocks | [CTRL.kicad_pro](hardware/controller/CTRL.kicad_pro) | [M6-L2](hardware/controller/review/M6-L2/README.md), previous [M6-L1](hardware/controller/review/M6-L1/README.md) |
| 80 m RF | M4A-V1R1 / [`f86684b`](https://github.com/DD1SB/ARDF-TX/commit/f86684b9ef45eec3ca4ce52edcb62896a847f1d7) | 150 × 110 mm | Si5351, LM5134B, IRF610, Classic/Sprint profiles and independent Foxoring output | [RF80_V1.kicad_pro](hardware/80m/production/RF80_V1.kicad_pro) | [M4A-V1R1](hardware/80m/production/review/M4A-V1R1/README.md) |
| 2 m RF | M5B-E5 / [`3b84366`](https://github.com/DD1SB/ARDF-TX/commit/3b84366caa985fac67fbdfbb60c4ede751b3a13e) | 150 × 110 mm | Si5351, PHA-1+, PD54008L-E, sinusoidal drain AM and independent training output | [RF2M.kicad_pro](hardware/2m/RF2M.kicad_pro) | [M5B-E5](hardware/2m/review/M5B-E5/README.md) |

Both RF boards share a **140 × 100 mm four-point M3 mounting pattern**. The
controller mounts independently and connects through short keyed IDC cables:
16 pins for RF80, 20 pins for RF2M. Their interfaces must not be interchanged.
RF battery power uses separate connectors, never the IDC cable. Normally only
one band/path transmits at a time.

The common footprint does not establish a qualified enclosure or three-board
stack. Cooling, controller antenna clearance and cable access are described in
the [common-enclosure study](docs/M5B_E5_COMMON_ENCLOSURE.md). RF2M's cooling
assembly projects approximately 25.2 mm below its board. A stack with both RF
modules remains a mechanical feasibility item.

## Intended operating modes

| Band | Intended modes |
| --- | --- |
| 80 m | Classic, Sprint, and Foxoring through a separate nominal 10 mW path |
| 2 m | Classic with genuine sinusoidal A2A amplitude modulation, and an independent very-low-power training path |

The controller contract supports configurable schedules, Morse identification,
Sprint slow/fast groups and spectator/finish-beacon roles. Simultaneous Sprint
groups operate across a fleet; one station executes its assigned role.
Frequencies and operating profiles are configurable. Continuous beacons need
their own power/endurance model.

RF power, 70–80% AM, ERP and 12 h full / 24 h reduced-power endurance remain
**targets requiring measurement**. Antenna/feed gain, legal frequencies/power
and country/operator authorization must be established separately. IARU event
rules do not grant permission to transmit.

## Controller and optional LoRa

The M6-L2 controller uses an **ESP32-S3-WROOM-1U-N4**, 4 MB flash with no PSRAM,
and an **RV-3032-C7 RTC** with
isolated CR1220 backup. USB-C provides programming, configuration, diagnostics
and time setting. Standalone operation does not require a network. The firmware
currently supplied is a hardware-contract/test foundation, not complete contest
firmware.

The ESP32's external **2.4 GHz** antenna port is separate from optional LoRa.
The optional FoxPro2 interface uses isolated population routing and protected
open-drain signalling; legacy battery reporting is unavailable for both 2S and
4S. Optional TCA9534A expansion provides eight limited 3.3 V GPIOs at address
0x38. Both options may remain completely unpopulated. The controller safety architecture
is unchanged. See the [M6-L2 review](hardware/controller/review/M6-L2/README.md)
for exact module lands, cable wiring, boot restrictions and test limitations.
Genuine FoxPro2 interoperability remains physically untested. Legacy oscillator
calibration is unsupported; test transmission requires native safety authorization
and is limited to 30 seconds. Target firmware integration remains incomplete.

| Radio population | Module | External antenna |
| --- | --- | --- |
| `NO_LORA` | U70 unpopulated | None required |
| `LORA_433` | Silicontra SX1262TR4-GC | Suitable 433 MHz antenna and U.FL pigtail |
| `LORA_868` | Silicontra SX1262TR8-GC | Suitable 868 MHz antenna and U.FL pigtail |

One PCB, footprint and RF feed support all options. The band comes from a
trusted assembly/configuration record; SX1262 chip identity cannot distinguish
the bands. Unknown/inconsistent configuration disables LoRa TX. Missing LoRa
does not prevent valid autonomous operation. See [LoRa variants](docs/M6_L1_LORA_VARIANTS.md)
and the [controller interface specification](docs/M6_C1_RF_INTERFACE.md).

Default-off hardware gating and local RF-board watchdogs inhibit transmission
during startup, reset and faults. Application progress owns the lease/heartbeat;
a continuously running PWM does not prove software health. Retuning, path
changes and faults require the documented disarm/rearm sequence.

## Power architecture

Use externally protected/balanced **2S or 4S Li-ion packs**, with compatible
RF-board populations and validated pack identity. The controller's intended
input is approximately 6.0–16.8 V. This does not make every RF population
compatible with every pack. RF2M `BOOST2S`, `BUCK4S`, `TRAIN_ONLY` and RF80
`FULL`/`FOX_ONLY` have distinct population and operating restrictions.

Logic power is separate from dedicated RF battery connections. Use the specified
separately fused power harness and ground returns. USB-only configuration must
not energize a PA or backfeed a pack. Charging electronics are out of scope.

Read the [controller power contract](docs/M6_C1_POWER_AND_BATTERY.md),
[corrected pack-ID protection](docs/M6_C1R1_INPUT_PROTECTION.md),
[power architecture decision](docs/M2_POWER_ARCHITECTURE_DECISION.md) and
[ADR-0011](docs/decisions/ADR-0011-dual-voltage-power-and-endurance.md).
Their recorded acceptance statuses remain authoritative; publication does not
accept proposed decisions.

## Manufacturing data

All three candidates use ordinary JLCPCB options: **two-layer standard FR4,
1.6 mm, 1 oz copper, green mask, white legend, lead-free HASL and ordinary plated
through vias**. No special stackup, controlled-impedance service, filled/capped
vias or precision press-fit process is required. Published capability, local DFM,
supplier CAM acceptance and an actual quotation are separate evidence.

Authentic archives for **five individual bare evaluation boards** of each design:

| Module | Fabrication ZIP | Manufacturing instructions |
| --- | --- | --- |
| Controller M6-L2, GO for controlled bare evaluation | [ARDF_TX_CTRL_M6-L2_JLCPCB_5pcs_BARE.zip](hardware/controller/review/M6-L2/ARDF_TX_CTRL_M6-L2_JLCPCB_5pcs_BARE.zip) | [M6-L2](docs/M6_L2_MANUFACTURING.md), [decision](docs/M6_L2_REVIEW_DECISION.md) |
| Controller M6-L1, preserved historical baseline | [CTRL_M6-L1_JLCPCB_5boards.zip](hardware/80m/production/review/M4A-V1R1/three-board-order/CTRL_M6-L1_JLCPCB_5boards.zip) | [M6-L1](hardware/controller/review/M6-L1/MANUFACTURING.md) |
| RF80 M4A-V1R1 | [RF80-V1R1_JLCPCB_5boards.zip](hardware/80m/production/review/M4A-V1R1/fabrication/RF80-V1R1_JLCPCB_5boards.zip) | [V1R1](docs/M4A_V1R1_MANUFACTURING.md) |
| RF2M M5B-E5 | [RF2M-M5B-E5_JLCPCB_5boards.zip](hardware/2m/review/M5B-E5/fabrication/RF2M-M5B-E5_JLCPCB_5boards.zip) | [E5](docs/M5B_E5_MANUFACTURING.md) |

The M6-L2 [full top-stencil ZIP](hardware/controller/review/M6-L2/ARDF_TX_CTRL_M6-L2_FULL_TOP_STENCIL.zip)
includes optional SMD lands. Its contents and the bare-board archive were regenerated
and compared in the [final reproduction](docs/M6_L2_FINAL_REPRODUCTION.md); the accepted
archives remain unchanged. No stencil order is authorized.

The historical M6-L1 ZIP remains in the existing three-board handoff; its
entries match the final M6-L1 fabrication directory. The [publication verifier](tools/m7_publication.py)
checks all three hashes and their layers/drills. Revisions are not interchangeable:
the older 210 × 160 mm RF80 E2 and 180 × 140 mm RF2M E4R1 packages are historical.
No historical manufacturing archive was regenerated for publication or M6-L2.
M6-L2 has separate fresh exports and is not included in the frozen M7 hashes.

Review the [three-board matrix](hardware/2m/review/M5B-E5/THREE_BOARD_READINESS.md)
before a separately authorized quotation/order. No supplier quote or CAM
acceptance is asserted. RF80's [V1R1-first proposal](docs/M4A_V1R1_PROTOTYPE_TRANSITION.md)
still requires review of the original E2-first sequencing restriction.

## Assembly and qualification

Use the integrated staged procedures:

- [Controller M6-L1 bring-up](hardware/controller/review/M6-L1/BRINGUP.md).
- [M6-L2 qualification additions and limits](docs/M6_L2_REVIEW_DECISION.md).
- [RF80-V1R1 bring-up](hardware/80m/production/review/M4A-V1R1/BRINGUP.md).
- [RF2M-E5 bring-up](hardware/2m/review/M5B-E5/BRINGUP.md).

Qualify low-voltage logic and protection with bounded laboratory supplies before
high-energy population or PA operation. Measure RF output, spectrum, off-slot
silence and port isolation into suitable dummy loads. True AM, PA thermal
behavior, endurance, antennas and field performance are **NOT_RUN**.
RF2M's analytical conservative 110°C thermal target remains unmet; its 125°C
engineering operating gate remains open. See the [thermal review](docs/M5B_E5_THERMAL_MECHANICAL.md).

## Getting started

```sh
git clone https://github.com/DD1SB/ARDF-TX.git
cd ARDF-TX
git log --oneline --decorate
git tag --list
```

Use the [M6-L2 reproduction commands](hardware/controller/review/M6-L2/REPRODUCE.md)
for the current controller. The frozen `m7_publication.py verify` command applies
to publication commit `387f275dd4c6ad715a25c0b092961ed36f407833`; run it at that
revision to verify its original three-board hashes and entry points.

The recorded CAD toolchain is **KiCad 10.0.6**, with its standard symbol,
footprint and 3D libraries. Open the three `.kicad_pro` files above; project-local
libraries are included. CAD Python checks need matching `pcbnew` bindings
(the recorded Debian installation uses `/usr/bin/python3`). Host fixtures need
a C11 compiler:

```sh
python3 -m unittest discover -s firmware/controller_hw -p 'test_*.py' -v
cc -std=c11 -Wall -Wextra -Werror firmware/controller_hw/contract.c firmware/controller_hw/test_contract.c -lm -o /tmp/ardf-controller-contract
/tmp/ardf-controller-contract
```

Find current BOMs, sourcing records and reproduction commands in the
[documentation index](docs/README.md). Prices contain unquoted estimates and
must be rechecked; they are not purchase quotations. For full CAD re-export or
historical regressions use the pinned revision instructions in a disposable
worktree. Old capture, placement and routing scripts can overwrite newer sources
or frozen reviews. Inspect the checked-in fabrication ZIPs first.

## Project status and history

The complete local development history and ten existing milestone tags are
preserved. A historical tag identifies evidence at that milestone, not a current
manufacturing or operational release. Current candidates are identified by the
commits above; publication adds no hardware acceptance tag.

Requirements, research, proposed/accepted ADRs, superseded circuits and review
findings remain discoverable through the [documentation index](docs/README.md).
The [M7 publication audit](docs/publication/M7/README.md) records checks actually
rerun and their limitations.

## License

Original contributor-owned firmware, tooling, documentation and KiCad design
work are under the [MIT License](LICENSE), except where separate notices apply.
MIT does not relicense third-party material.

[Third-party notices](THIRD_PARTY_NOTICES.md) cover OpenARDF MIT attribution,
KiCad-derived library data under CC-BY-SA-4.0 with its exception, and the
GPL-2.0-or-later sliver helper. Historical DL3BBX-derived M5A-R3 retains its
private-construction/commercial-permission restrictions; it is not unrestricted
MIT hardware. Manufacturer documents remain linked under their owners' terms.

## Contributions

Issues and pull requests are welcome. Identify the board/revision, provide
reproduction steps and distinguish calculations from measurements. Schematic
changes need manufacturer pin/land evidence, interface implications, population
updates and relevant regressions. PCB changes also need native geometry/DFM
checks and a new revision-specific artifact manifest.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before regenerating manufacturing data.
Preserve historical evidence and decision status. Share qualification results
with instrument details, uncertainty and test configurations.
