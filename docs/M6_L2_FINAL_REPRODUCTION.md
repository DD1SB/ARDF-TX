# M6-L2 final reproduction — 2026-10-20

**GO for five controlled bare M6-L2 controller evaluation boards.** All mandatory software, electrical, CAD and local manufacturing reproduction gates passed. This is not production qualification, an order, or authorization to operate hardware.

The user supplied the independent review conclusion after review of native KiCad sources, exported connectivity, PCB geometry, manufacturing archives and population variants. That independent conclusion is separate from the commands executed and results recorded here. No independent physical measurements are claimed.

## Starting state and execution environment

The working tree was clean on `m6-l2-controller-candidate`, at implementation commit `89f5a7df6ccb4dec8fcea10e7c810a9981342ce4`. Fetching `origin` branches and tags found public `main` at `387f275dd4c6ad715a25c0b092961ed36f407833`: an ancestor exactly one implementation commit behind. Ten existing milestone tag objects were snapshotted. No unrelated changes or divergence were present.

Host: Pop!_OS 24.04 LTS, x86-64 Linux 7.1.5-76070105-generic. Toolchain: KiCad CLI 10.0.6; pcbnew `10.0.6-10.0.6~ubuntu24.04.1`; `/usr/bin/python3` 3.12.3; Pillow 10.2.0; GCC/cc 13.3.0. See [starting environment and refs](publication/M6-L2/starting-environment.json).

The complete `REPRODUCE.md`, review README, review decision and manufacturing document were read before verification. Testing and exports ran in `/tmp/ardf-m6-l2-final-reproduction`, cloned with:

```sh
git fetch origin --tags
git clone --no-hardlinks /home/stefan/src/ardf-tx /tmp/ardf-m6-l2-final-reproduction
```

The private reference-cache validation block from `REPRODUCE.md` was executed as `/usr/bin/python3 /tmp/ardf-m6-l2-final-evidence/validate-references.py`. All 12 cached, hash-recorded references passed SHA-256 validation; no changed upstream reference was accepted. Original DF1FO ASM/DOC contents and manufacturer STEP were neither copied into the repository nor relicensed. The manufacturer STEP was available in the documented default `/tmp/m6l2/references` model directory.

## Actual reproduction commands and results

After the two portability corrections below, the entire sequence was restarted and all 18 commands, including reference validation, completed with return code zero. The [runner](publication/M6-L2/run.py), [reference validator](publication/M6-L2/validate-references.py), [timestamped command ledger](publication/M6-L2/execution.json) and complete numbered logs preserve actual execution. Commands after reference validation, in order:

```sh
/usr/bin/python3 tools/m6_l2.py checks
/usr/bin/python3 tools/m6_l2.py verify
/usr/bin/python3 tools/m6_l2.py protocols
/usr/bin/python3 tools/m6_l2.py protection
/usr/bin/python3 tools/m6_l2.py usb
/usr/bin/python3 tools/m6_l2.py powerpaths
/usr/bin/python3 tools/m6_l2.py dfm
/usr/bin/python3 tools/m6_l2.py host
/usr/bin/python3 tools/m6_l2_audit.py
/usr/bin/python3 tools/m6_l2_metrics.py
/usr/bin/python3 tools/m6_l2_documents.py
/usr/bin/python3 tools/m6_l2_bom.py
/usr/bin/python3 tools/m6_l2_references.py /tmp/m6l2/references
/usr/bin/python3 tools/m6_l2_exports.py exports
/usr/bin/python3 tools/m6_l2_exports.py render
/usr/bin/python3 tools/m6_l2_exports.py package
/usr/bin/python3 tools/m6_l2.py manifest
```

| Gate executed in this run | Actual result |
| --- | --- |
| Native hierarchy, ERC, DRC and parity | PASS; complete schematic PDF/netlist exported; ERC zero violations; DRC zero errors/warnings; zero unrouted and parity errors; exclusions empty |
| Host suite | **75 tests passed**: 29 FoxPro2 and 46 inherited tests |
| Strict C11 fixture | Compile with `-std=c11 -Wall -Wextra -Werror`, then execute: both return zero |
| M6-L2 native mutations | **32/32 rejected** using actual native pads, package fields, nets, geometry and electrical models |
| Inherited electrical regression | **4,096 enable combinations**, 36 RF connector assignments, 38 manufacturer-critical package maps, 841 numbered terminal keys and 20 inherited native mutations PASS |
| RF protocol replay | RF80: 256 truth cases, 31 states, 16 timing corners, two polarity mutations; RF2M: 4,096 combinations, 39 states and 16 source/converter cases PASS |
| Protection, USB, RTC, recovery and power paths | PASS; battery-ID/USB-only restrictions, reset/fail-off, branch isolation, static controls, LoRa TR4/TR8, GPIO35–37 and strapping preserved |
| New hardware models and populations | PASS; exact non-PSRAM 1U-N4 footprint/antenna access, hardware-exclusive UART routing, open-drain/receive/off-state protection, TCA9534APWR 0x38 and RTC isolation; 48 RF/LoRa/interface populations reproduced |
| Manufacturer module drawings | PASS; both independent DXFs: 80 perimeter-land and 18 paste-window comparisons; 3.7 mm exposed ground land |
| Standard JLCPCB DFM | PASS, zero errors; 171,441 independent copper-pair checks and seven DFM mutations |
| Frozen evidence | 1,865 committed RF/historical-controller files hash-identical; 1,534 committed files in the older subset; ten tag objects preserved |

[Fresh result reports](publication/M6-L2/fresh-results/) are distinct from historical PASS logs. pcbnew emits headless wx enum/image-handler initialization diagnostics, also observed by a standalone version import; full stderr is retained. These are not ERC/DRC violations, no return code was masked, and no exclusion or safety threshold was added. The existing ignored tuning-profile category remains unchanged.

The controller PCB after refill remains byte-identical to the implementation: SHA-256 `2d7a22b3e2991f22e7a22243ff0ce810e52bcec38fae6658edd631c6b9d22842`. All 70 inventoried controller native/library/electrical-manifest inputs match. All original RF geometry, thermal construction, controller connectors and fabrication datasets remain unchanged, as do M6-L1/C1/C1R1 historical evidence and costs. See [native input hashes](publication/M6-L2/native-input-preservation.json) and [Git/hash preservation checks](publication/M6-L2/hardware-preservation.json).

## Failures investigated and minimal corrections

1. **Unpublished personal state in frozen inventories.** A fresh clone lacked three `.kicad_prl` UI files and one `~RF2M.kicad_pro.lck` lock file accidentally recorded by the older inventories. Both inventories remain untouched. `m6_l2_frozen.py` requires those exact four paths to be untracked and ignored, rejects any additional untracked inventory entry, and verifies every remaining committed file hash. L2 replay/audit now use that validator. Thus the accurate committed counts are 1,534/1,865 rather than the original 1,538/1,869 including private UI state. Three additional validator mutations reject a changed committed RF hash, an arbitrary missing design file, and an undeclared exception. [Original failure](publication/M6-L2/initial-failure/02-m6_l2-verify.log), [validator checks](publication/M6-L2/frozen-validator-regression.json).
2. **Missing RF protocol input copy.** The L2 replay pointed to an absent `M6-L2/inputs/RF80-interface.xml`. It now reads the already committed, frozen `M6-L1/inputs/RF80-interface.xml`; its result identifies that source correctly. No RF source or historical input changed. [Original failure](publication/M6-L2/missing-input-failure/03-m6_l2-protocols.log).

Both failures were deterministic reproduction-tooling defects, not electrical defects. The final sequence was run afresh after both corrections. No CAD, BOM population, component value, safety threshold or manufacturing geometry changed. The comparison utility initially flagged renderer reload-runtime text; its preserved [diagnostic](publication/M6-L2/comparison-initial-diagnostic.log) was resolved by explicitly classifying that runtime metadata, without changing any hardware check.

## Manufacturing comparison and archive disposition

All 191 review files were compared: **133 byte-identical (category 1); 58 equivalent geometry/electrical content with metadata, rendering or explicitly described reporting/provenance differences (category 2); zero manufacturing/electrical differences (category 3)**. There are no extra or missing review files. The [file/ZIP-entry hash comparison](publication/M6-L2/artifact-comparison.json), [strict comparison scripts](publication/M6-L2/compare.py), [classification checks](publication/M6-L2/finish-comparison.py) and [individual difference explanations](publication/M6-L2/classification-review.json) preserve the basis for each difference.

All nine Gerber layers and both separate PTH/NPTH drill files match after removing only creation-date header records; no coordinate, aperture, net, tool or hole record was discarded. The board outline is 100 × 100 mm; all 677 native/exported holes agree. Full top paste, including optional SMD lands, matches. The exported netlist differs only in source path/date; IPC356, all BOM/population and placement records match. Schematic, assembly, PCB and drill-map PDFs have pixel-identical pages at 72 dpi. SVG differences are title timestamps/final newlines. Five real 3D renders use the same native inputs, model and commands; stochastic pixel differences have mean channel error below 0.142 on a 0–255 scale. The BOTH top view was also visually compared. Render progress/runtime and old temporary-lock cleanup diagnostics differ without geometry changes.

Both archived and regenerated 189-file manifests validate. Downstream hashes reflect export metadata/runtime, the two corrected replay inputs and the added validator. The accepted review inventory remains an implementation-commit snapshot; this publication's separate evidence has its own SHA-256 list.

| Archive | Entries | Accepted SHA-256, retained for publication | Regenerated SHA-256 |
| --- | ---: | --- | --- |
| Five bare boards | 10: seven board Gerbers, two drills, instructions | `a33c41efa3d5cfaee3374b687bdd82f754fadf42462efa53b493dd5699d5051d` | `47f89e653d8e3640b29ed166da2c0f1d8e402346b89e265e4a86bcb892c909d8` |
| Full top stencil | 3: paste, outline, Gerber job | `65bc0851025f3554c6c1615ac4f4b9f173fcaeacb0767f53501db181a9e75908` | `b797c0e0107ef926ff5ab5ab8f5a4a503d80e89f8165c0c0840df1c4436b44cd` |

ZIP entry sets/CRC checks pass; payload hash differences are limited to export creation metadata. **The complete accepted M6-L2 review directory and its manufacturing archives were preserved**, as were all earlier reviews. Regenerated outputs stayed in the isolated checkout; fresh reports, hashes and comparison evidence are published separately.

The profile remains ordinary JLCPCB: 100 × 100 mm, two layers, standard FR4, 1.6 mm, 1 oz, green mask, white legend, lead-free HASL and ordinary plated through-vias; no premium stackup, controlled-impedance service or filled/capped vias. The existing 202 signal vias with 0.6/0.3 mm land/drill have 0.15 mm annular rings; 410 preferred vias use 0.8/0.3 mm. These margins remain explicitly listed in DFM, with no DRC exclusions. Component PTH annuli are at least 0.25 mm. This local DFM result is separate from supplier CAM acceptance.

## Publication scope and remaining qualification

Publication adds the reproduction-tooling fixes, this report/evidence and current README/index/manufacturing/review-decision updates. The original implementation commit and all prior commits/tags remain intact. Publication uses the existing candidate branch and a normal fast-forward of public main, after rechecking remote ancestry. No acceptance tag or production release is created. Post-push refs, public file availability and a fresh GitHub clone are checked by the publication procedure; the final remote SHA is reported with the completed publication.

Gate G remains **NOT_RUN**: ESP32 USB/boot/recovery/brownout, antenna access/cable/strain relief and coexistence, genuine FoxPro2/cable continuity, battery/contact-fault and powered/unpowered measurements, GPIO accessories/shorts, RTC loading, power sequencing, RF and thermal qualification. FoxPro battery-voltage reporting is unavailable for both 2S and 4S; oscillator calibration is unsupported; test transmit is safety-gated and limited to 30 seconds. Target RTC/scheduler/persistence/transport integration remains incomplete: the firmware is a compatibility/test foundation, not operational contest firmware. No PCB or stencil was ordered, no hardware was energized, and no physical result is inferred from simulation or CAD.

These remaining physical tasks do not block controlled bare evaluation boards. **Final engineering disposition: GO for five bare controller evaluation boards.**
