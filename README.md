# ARDF-TX

**Hardware evaluation stage — physical transmitter qualification pending.**

ARDF-TX is a modular open-source transmitter platform for Amateur Radio Direction
Finding (ARDF), with separate 80 m and 2 m RF boards and a common ESP32-S3
controller. Its goals are affordable reproduction, ordinary PCB manufacturing,
autonomous contest timing, optional remote operation and explicit hardware
transmitter interlocks.

**Mini80-SMD is a fourth, independent transmitter family:** a standalone,
low-power 80 m board with its own AVR firmware and protected 1S battery. Its
35 × 35 mm evaluation design operates without the ESP32 controller. Mini80's
sources and manufacturing review are published on `mini80-smd-evaluation`; the
Mini80 links below are pinned to the published review commit so they also work
from `main`, where the experimental hardware files are not included.

The repository contains editable KiCad sources, development history, engineering
decisions, population BOMs, verification tools and revision-specific fabrication
data. The RF designs and M6-L2 controller have independent CAD reviews. The fresh
[M6-L2 final reproduction](docs/M6_L2_FINAL_REPRODUCTION.md) supports **GO for five
controlled bare controller evaluation boards**. Physical qualification and release
for operation remain pending. No PCB has been ordered or tested.

The current RF2M revision is **M5B-E6R2**, with carrier-keyed A2A,
one shared heatsink and instrumented bring-up access. Independent engineering
review found no concrete blocker for **five bare evaluation PCBs**. See the
[E6R2 decision](docs/M5B_E6R2_REVIEW_DECISION.md) and
[final reproduction](docs/M5B_E6R2_FINAL_PUBLICATION.md). Physical RF, thermal
and operational qualification remains **NOT_RUN**. The earlier
[E6](docs/M5B_E6_REVIEW_DECISION.md) and
[E6R1](docs/M5B_E6R1_REVIEW_DECISION.md) HOLD studies remain preserved evidence.
Controller M6-L2 and RF80 are unchanged. No board or stencil has been ordered.

## Hardware architecture

| Module | Current candidate / source commit | PCB | Main functions | Native KiCad project | Engineering review |
| --- | --- | --- | --- | --- | --- |
| Common controller | **M6-L2 — ESP32 external antenna, FoxPro2 compatibility and optional GPIO expansion** / [`89f5a7d`](https://github.com/DD1SB/ARDF-TX/commit/89f5a7df6ccb4dec8fcea10e7c810a9981342ce4); previous baseline [`d94dabd`](https://github.com/DD1SB/ARDF-TX/commit/d94dabd0e40137dc44b2bb94f3707ad4636ca65f) | 100 × 100 mm | External-antenna ESP32-S3, RTC, USB-C, optional LoRa/FoxPro2/GPIO expansion and default-off interlocks | [CTRL.kicad_pro](hardware/controller/CTRL.kicad_pro) | [M6-L2](hardware/controller/review/M6-L2/README.md), previous [M6-L1](hardware/controller/review/M6-L1/README.md) |
| 80 m RF | M4A-V1R1 / [`f86684b`](https://github.com/DD1SB/ARDF-TX/commit/f86684b9ef45eec3ca4ce52edcb62896a847f1d7) | 150 × 110 mm | Si5351, LM5134B, IRF610, Classic/Sprint profiles and independent Foxoring output | [RF80_V1.kicad_pro](hardware/80m/production/RF80_V1.kicad_pro) | [M4A-V1R1](hardware/80m/production/review/M4A-V1R1/README.md) |
| 2 m RF | **M5B-E6R2 — reviewed evaluation candidate** / [`2fff321`](https://github.com/DD1SB/ARDF-TX/commit/2fff32131dd0f7da3c46fef47c04713a55df89d8); historical E5 / [`3b84366`](https://github.com/DD1SB/ARDF-TX/commit/3b84366caa985fac67fbdfbb60c4ede751b3a13e) | 150 × 110 mm | Carrier-keyed A2A, Si5351, PHA-1+, PD54008L-E, unified cooling and independent training output | [RF2M.kicad_pro](hardware/2m/RF2M.kicad_pro) | [E6R2](hardware/2m/review/M5B-E6R2/README.md); preserved [E5](hardware/2m/review/M5B-E5/README.md) |
| Standalone 80 m Mini80 | **M80-E1 hardware / M80-E2 bare-board review** / [hardware `bdac015`][mini80-e1-commit], [review `2bf55b5`][mini80-e2-commit] | **35 × 35 mm**, two layers | ATtiny1616-MNR, Si5351A-B-GT, 74HCT240PW; autonomous MINI50 training / FOX10 candidate; independent battery and fixture | [Mini80.kicad_pro][mini80-project] | [M80-E2: GO for five bare evaluation PCBs][mini80-review] |

The RF80 and RF2M boards share a **140 × 100 mm four-point M3 mounting pattern**.
The controller mounts independently and connects through short keyed IDC cables:
16 pins for RF80, 20 pins for RF2M. Their interfaces must not be interchanged.
RF battery power uses separate connectors, never the IDC cable. Normally only
one band/path transmits at a time.

The common footprint does not establish a qualified enclosure or three-board
stack. Cooling, controller antenna clearance and cable access are described in
the [historical common-enclosure study](docs/M5B_E5_COMMON_ENCLOSURE.md) and
[E6R2 mechanical assembly](docs/M5B_E6R2_MECHANICAL_ASSEMBLY.md). E6R2 places its
cooler below the board, with a protected carrier and independent supports. A
stack with both RF modules remains a physical qualification item.

Mini80 uses its own battery, two M2 mounting holes and six-pad bottom-side pogo
interface. It does not use the shared ESP32 controller, either IDC interface or
the RF80/RF2M mounting pattern.

## Intended operating modes

| Band | Intended modes |
| --- | --- |
| 80 m RF80 | Classic, Sprint, and Foxoring through a separate nominal 10 mW path |
| 2 m RF2M | Classic with genuine sinusoidal A2A amplitude modulation, and an independent very-low-power training path |
| Standalone 80 m Mini80 | Informal Sprint/training with MINI50; continuous FOX10 Foxoring candidate pending calibration and field verification |

For the controller/RF80/RF2M system, the controller contract supports configurable
schedules, Morse identification, Sprint slow/fast groups and spectator/finish-beacon
roles. Simultaneous Sprint
groups operate across a fleet; one station executes its assigned role.
Frequencies and operating profiles are configurable. Continuous beacons need
their own power/endurance model.

RF power, 70–80% AM, ERP and 12 h full / 24 h reduced-power endurance remain
**targets requiring measurement**. Antenna/feed gain, legal frequencies/power
and country/operator authorization must be established separately. IARU event
rules do not grant permission to transmit.

## Standalone 80 m Mini80 transmitter

[Mini80-SMD][mini80-readme] is an autonomous **35 × 35 mm, two-layer** low-power
80 m transmitter inspired by DF1FO's 80mSprintTX. An **ATtiny1616-MNR** controls
the **Si5351A-B-GT** programmable carrier source and **74HCT240PW,118** output
stage. Eight HCT outputs each have their own ballast resistor before the RF
signal is combined and passed through the output low-pass filter. A protected
**1S Li-ion/LiPo battery** supplies onboard **3.0 V logic** and a switched,
nominal 5 V RF supply. Charging is external; no charger is fitted, and the board's
protection circuitry does not replace a protected cell.

![Mini80 native KiCad mechanical rendering][mini80-render]

The rendering includes optional component envelopes; it is not a photograph of
assembled hardware or a statement that every shown matching component is fitted.

The two populations share the same PCB and firmware. Their nominal power
estimates use a **50 Ω reference load**, 3.55 MHz, a 4.95 V RF rail and assumed
HCT output resistance:

| Population | Eight ballast resistors | Calculated nominal RF power | Intended use |
| --- | --- | --- | --- |
| **MINI50** | 8 × 100 Ω | **47.4 mW into 50 Ω** | Informal Sprint/training only; below the official Sprint 0.3–1 W output requirement and not competition-compliant Sprint output |
| **FOX10** | 8 × 560 Ω | **10.16 mW into 50 Ω** | Foxoring candidate pending conducted-power calibration, real-antenna tuning and field verification |

Optional antenna matching populations provide impedance transformation and
selectable loading for wire training antennas. A short Foxoring antenna needs
its own selected coupling/matching setup; one population is not assumed optimal
for both. The FOX10 first-article bench population bypasses the optional matching
bank; testing requires a characterized 50 Ω dummy load. RF power, runtime estimates and antenna
models are **calculations, not physical measurements**. Adjusting conducted
power alone does not establish the required Foxoring field range.

One universal AVR firmware image supports per-unit settings for carrier
frequencies from **3.510–3.600 MHz**, role, Morse identifier, keying speed,
physical power profile, schedule and calibration. The twelve Sprint roles are
five slow and five fast transmitters, each using **MOE, MOI, MOS, MOH, MO5**,
plus spectator **S** and finish/training **MO**. Default group speeds are 10/15
WPM. The slotted roles use nominal 12-second windows in a 60-second cycle;
continuous Foxoring identifiers and independent continuous S/MO modes are also
supported. The low-power MO training role does not cover a normal-power
competition Foxoring finish beacon.

The AVR runs autonomous scheduling, Morse generation, separate carrier/timing
calibration and synchronized starting. Persistent configuration does not retain
an armed state; startup, invalid configuration and faults leave RF disabled.
**J2** provides UPDI programming, **3 V UART** configuration and a **3 V SYNC**
edge through six bottom-side pogo pads: GND, target V3 sense, UPDI, RX, TX and
SYNC. V3 is a programmer voltage reference, not an external power input.
Mini80 uses its own fixture protocol and **does not implement FoxPro2
compatibility**. See the [firmware and configuration instructions][mini80-firmware]
and [first-article/fixture guide][mini80-first-article].

| Engineering milestone | Published scope |
| --- | --- |
| **M80-E1**, [hardware commit `bdac015`][mini80-e1-commit] | Original native KiCad hardware and universal AVR firmware |
| **M80-E2**, [review commit `2bf55b5`][mini80-e2-commit] | Final bare-board manufacturing review; **no copper or firmware revision** |

KiCad 10 ERC/DRC, design verification and firmware host checks passed.
**GO: five unpopulated evaluation PCBs. HOLD: populated fleet release,
competition claims and operational compliance.** No Mini80 hardware has yet
been ordered or energized. Physical checks remain for HCT output skew/current,
spectrum, RF power, power consumption, frequency/timing stability, keying-envelope
behavior and FOX10 audibility at **30 m** with no audibility at **250 m**. The
[M80-E2 manufacturing review][mini80-review] records these limits and the
U2 exposed-pad solder-wicking and J2 fixture-orientation assembly risks.

Native sources: [KiCad project][mini80-project],
[schematic][mini80-schematic] and [PCB][mini80-pcb]. Start with the
[Mini80 design notes][mini80-readme], [exact order instructions][mini80-order]
and [FOX10 first-article plan][mini80-first-article].

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

The common controller/RF80/RF2M system uses externally protected/balanced
**2S or 4S Li-ion packs**, with compatible
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

The controller, RF80 and RF2M candidates use ordinary JLCPCB options:
**two-layer standard FR4, 1.6 mm, 1 oz copper, green mask, white legend, lead-free
HASL and ordinary plated through vias**. No special stackup, controlled-impedance service, filled/capped
vias or precision press-fit process is required. Published capability, local DFM,
supplier CAM acceptance and an actual quotation are separate evidence.

Authentic archives for **five individual bare evaluation boards** of each design:

| Module | Fabrication ZIP | Manufacturing instructions |
| --- | --- | --- |
| Controller M6-L2, GO for controlled bare evaluation | [ARDF_TX_CTRL_M6-L2_JLCPCB_5pcs_BARE.zip](hardware/controller/review/M6-L2/ARDF_TX_CTRL_M6-L2_JLCPCB_5pcs_BARE.zip) | [M6-L2](docs/M6_L2_MANUFACTURING.md), [decision](docs/M6_L2_REVIEW_DECISION.md) |
| Controller M6-L1, preserved historical baseline | [CTRL_M6-L1_JLCPCB_5boards.zip](hardware/80m/production/review/M4A-V1R1/three-board-order/CTRL_M6-L1_JLCPCB_5boards.zip) | [M6-L1](hardware/controller/review/M6-L1/MANUFACTURING.md) |
| RF80 M4A-V1R1 | [RF80-V1R1_JLCPCB_5boards.zip](hardware/80m/production/review/M4A-V1R1/fabrication/RF80-V1R1_JLCPCB_5boards.zip) | [V1R1](docs/M4A_V1R1_MANUFACTURING.md) |
| RF2M M5B-E6R2, GO for five bare evaluation PCBs | [RF2M-M5B-E6R2_JLCPCB_5boards.zip](hardware/2m/review/M5B-E6R2/fabrication/RF2M-M5B-E6R2_JLCPCB_5boards.zip) | [E6R2 manufacturing](docs/M5B_E6R2_MANUFACTURING.md), [full top stencil](hardware/2m/review/M5B-E6R2/fabrication/RF2M-M5B-E6R2_FULL_TOP_STENCIL.zip) |
| RF2M M5B-E5, preserved historical archive | [RF2M-M5B-E5_JLCPCB_5boards.zip](hardware/2m/review/M5B-E5/fabrication/RF2M-M5B-E5_JLCPCB_5boards.zip) | Historical [E5](docs/M5B_E5_MANUFACTURING.md); E6/E6R1 studies remain unchanged |
| Standalone Mini80 M80-E1, M80-E2 GO for five bare evaluation PCBs | [Mini80-M80-E1-JLCPCB-bare.zip][mini80-bare] | [M80-E2 order specification][mini80-order], [FOX10 first article][mini80-first-article] |

Mini80's separate order is **five 35 × 35 mm bare evaluation boards**, using
standard **1.6 mm FR4, two layers, 1 oz copper, ENIG, green solder mask and white
silkscreen**. Use the existing immutable **M80-E1 bare-board ZIP** linked above;
M80-E2 did not regenerate or revise it. The optional
[0.10 mm top-side stencil][mini80-stencil] matches the bench population. Assemble
**one FOX10 first article before any further population**. No filled/capped vias
or special stackup is required. This independent five-board GO does not change
the controller, RF80 or RF2M manufacturing statuses or packages.

RF2M E6R2 also includes the [mechanical STEP assembly](hardware/2m/review/M5B-E6R2/mechanical/complete-mechanical-stack.step),
[mounting drawing](hardware/2m/review/M5B-E6R2/mechanical/dimensioned-mounting.pdf),
[first-article test plan](docs/M5B_E6R2_FIRST_ARTICLE_TEST.md) and
[review/reproduction evidence](hardware/2m/review/M5B-E6R2/README.md).

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
- [RF2M-E6R2 first-article plan](docs/M5B_E6R2_FIRST_ARTICLE_TEST.md).
- Preserved [RF2M-E5 bring-up](hardware/2m/review/M5B-E5/BRINGUP.md).

Qualify low-voltage logic and protection with bounded laboratory supplies before
high-energy population or PA operation. Measure RF output, spectrum, off-slot
silence and port isolation into suitable dummy loads. True AM, PA thermal
behavior, endurance, antennas and field performance are **NOT_RUN**.
RF2M's E5 steady-state stress calculation is preserved in the
[thermal review](docs/M5B_E5_THERMAL_MECHANICAL.md). It is not a one-minute
Morse temperature prediction. The [E6 transient study](docs/M5B_E6_TRANSIENT_THERMAL.md)
and E6R1 calculations retain the degraded-contact protection limitation. The
[E6R2 decision](docs/M5B_E6R2_REVIEW_DECISION.md) separates controlled bare-board
evaluation from measured powered and operational qualification.

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
footprint and 3D libraries. Open the controller, RF80 and RF2M `.kicad_pro` files
above; project-local libraries are included. Mini80's separate branch and pinned
native project are described in its section. CAD Python checks need matching
`pcbnew` bindings
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

[mini80-readme]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/README.md
[mini80-project]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/Mini80.kicad_pro
[mini80-schematic]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/Mini80.kicad_sch
[mini80-pcb]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/Mini80.kicad_pcb
[mini80-firmware]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/firmware/README.md
[mini80-review]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/review/M80-E2/README.md
[mini80-order]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/review/M80-E2/JLCPCB-ORDER.md
[mini80-first-article]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/review/M80-E2/FOX10-FIRST-ARTICLE.md
[mini80-bare]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/fabrication/Mini80-M80-E1-JLCPCB-bare.zip
[mini80-stencil]: https://github.com/DD1SB/ARDF-TX/blob/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/fabrication/Mini80-M80-E1-stencil.zip
[mini80-render]: https://raw.githubusercontent.com/DD1SB/ARDF-TX/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f/hardware/80m-mini/render/Mini80-isometric.png
[mini80-e1-commit]: https://github.com/DD1SB/ARDF-TX/commit/bdac015766cab5aa62fc106aefb151f634e7f109
[mini80-e2-commit]: https://github.com/DD1SB/ARDF-TX/commit/2bf55b56cbd1029870b401ccb81eaf3c1fcbf11f
