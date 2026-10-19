# RF80 E2 — reproducible verification record

Date: **2026-10-15**. Tools: **KiCad CLI/pcbnew10.0.6**, Python3.12.3, **ngspice42**, Git, Mesa software rendering/Xvfb display:93. No rerouting, manufacturer API, component order or physical test is part of verification. Native board is the routing authority.

## Current E2 commands

From repository root:

```sh
python3 tools/m3b_exports.py --render
/usr/bin/python3 tools/m3b_verify.py
/usr/bin/python3 tools/m3be2_pinouts.py
python3 tools/m3b_bom.py
python3 tools/m3be2_power.py
/usr/bin/python3 tools/m3be2_audit.py
/usr/bin/python3 tools/m3be2_regressions.py
python3 tools/m1_analysis.py --check
git diff m3b-e1 --check
/usr/bin/python3 tools/m3be2_audit.py --manifest
sha256sum --check hardware/80m/review/M3B-E2/SHA256SUMS
```

The exporter executes `kicad-cli sch erc --format json --severity-all --exit-code-violations`, XML/PDF exports and `kicad-cli pcb drc --format json --severity-all --exit-code-violations --schematic-parity --refill-zones --save-board` followed by the text DRC, Gerbers, metric separate PTH/NPTH drills/maps, IPC, position, SVG and assembly PDF commands. Exact arguments are in [exporter](../../../../tools/m3b_exports.py); all commands target this manifest's revision directory. `--render` needs a display/Mesa and generates actual KiCad views, not image-generation substitutes. For nonvisual exports omit it. A Q403 detail was additionally rendered with:

```sh
DISPLAY=:93 LIBGL_ALWAYS_SOFTWARE=1 kicad-cli pcb render --width 1600 --height 1200 --quality high --background opaque --zoom 4 --pivot '3.328,3.1,0' --rotate '325,0,25' --output hardware/80m/review/M3B-E2/RF80-Q403-3D.png hardware/80m/RF80.kicad_pcb
```

Do not reapply `m3be2_pcb.py` (one-shot E1 correction), regenerate initial placement with `m3b_pcb.py --place`, or run the old E1 `m3b_documentation.py --write` on the reviewed native E2 board. No generator is permission to discard the final routing. The model-only `m3be2_models.py` creates the explicitly labeled ST dimensional envelope; source regeneration must be reconciled with native PCB before re-export.

## Checked evidence

| Evidence | Coverage |
| --- | --- |
| [ERC](ERC.json), [DRC](DRC.json), [coverage](drc-coverage.json) |0violations/0unrouted/0parity, no ignored DRC checks/exclusions; three informational ERC defaults explicitly recorded |
| [Current PCB/logic results](../../../../docs/M3B_E2_CHECK_RESULTS.json) |664 XML/native physical pad memberships,277footprints,329vias,74test pads,all declared model paths resolve |
| [Current pin-derived logic](../../../../docs/M3B_E2_LOGIC_RESULTS.json) |256static combinations,31state scenarios,16timing corners; unsafe U202 output-polarity mutants rejected, path/power/rearm/retune/key-tail contract retained |
| [Manufacturer roles](critical-pinouts.json) |55critical devices; XML/PCB/symbol/approved footprint; independent ST/TI application nets and Q403 installed orientation;10incorrect vendor/foot/pin/E1 cases rejected |
| [Native E1/E2 copper comparison](connectivity-change-audit.json) |4old local U311 segments removed,8local segments+1via added; all other track/via geometries and other footprint positions preserved; ground zones refilled |
| [Fabrication checks](fabrication-audit.json), [drills](drill-report.rpt) |9E2Gerber layers,372PTH/4NPTH,195placement rows,revision metadata,IPC exported; archived E1 files byte-identical |
| [Power results](../../../../docs/M3B_E2_POWER_RESULTS.json) |32analytic/24input-SPICE/5driver-SPICE corners; imposed20µs condition separated from100µs failure; no active device/PCB parasitic qualification |
| [BOM](../../../../docs/M3B_E2_COSTS.json), [cost comparison](cost-delta.json) |Same196full/115Fox purchased parts,18/13ICs;1/6/10/20basket deltas0; historical observations versus estimates retained |

The manufacturer regression's negative cases reject wrong XML pad1/pad3, wrong actual PCB pad1/pad3, old TL431groundpin2, an unverified BD140 vendor/footprint/symbol, and the actual archived E1 Q403/U311. This directly addresses the defect that the old “expected pin mapping” test encoded the same wrong assumption as the design.

No static/surrogate result proves power-on/reset pulse widths, metastability, real watchdog tolerance, analog reference startup, physical comparator/switch delay, driver-rail limits, CW edges, RF power/harmonics, thermal SOA, antenna field range or endurance. Those are **NOT_RUN**, subject to [E2 power/safety gates](../../../../docs/M3B_E2_POWER_PROTECTION.md).

The installed pcbnew binding emits nonfatal `PROPERTY_ENUM: No enum choices defined` startup diagnostics and duplicate-image-handler debug messages. These are retained in the command logs, not counted as electrical findings or silently suppressed. Processes return0 and the native CLI ERC/DRC JSONs explicitly contain zero violations; the diagnostic is a tool limitation, not evidence that analog/RF checks occurred. Exported drills are read back against all376 native hole locations/diameters (maximum coordinate quantization0.0005mm); six Q403/U311 Gerber-X2 flashes and IPC net labels are separately compared to native pad coordinates/nets.

## Version-aware preserved suite

[Historical-version command outputs](historical-version-regressions.json) run a temporary **0dfd224** archive for `m3_80m_checks.py`, `m3a_r1_logic.py`, `m3a_r1_driver_fault.py`, `m3a_r1_report.py`, `m3a_r1_documentation.py`; an **m3b-e1** archive runs frozen `m3b_verify.py` and `m3b_documentation.py`. Read-only Git metadata is supplied so the archived R1 cost report can compare tagm3a-r0. The first archive-only run lacked that metadata; the harness was corrected and the suite rerun. No historical ledger was rewritten to force a pass.

Those frozen suites intentionally assert historical counts/hashes/no-PCB state or the now-refuted E1 manufacturer pin assumption. Their historical pass means **reproducibility**, not safe E1 hardware. On current E2, the retained physical-pin digital engine and new independent manufacturer test are the applicable contracts. E1's actual Q403/U311 are expressly rejected by E2.

[Preserved M1/M2/Fox model regressions](preserved-model-regressions.json) record exact commands/outputs for `m1_costs --check`, `m2_rf_analysis --check`, `m2_system_costs --check`, `m2_checks`, `foxoring_costs --check`, `m2_80m_analysis --check`, `m2_power_architecture --check`. Local document/anchor consistency is checked with `m1_analysis --check` and an additional hardware-package link pass; external source fetch failures remain disclosed, not converted into successful link checks.

Final [SHA256SUMS](SHA256SUMS) and [manifest](file-manifest.json) cover native CAD, local library/models, E2 documents/BOM, scripts and review outputs. Generated artifacts carry E2 revision and are rebuilt after the final orientation correction. Hashes verify identity, not suitability for manufacture. No independent CAM etch simulation or hardware qualification is implied.

KiCad SVG previews are postprocessed only to remove trailing whitespace from exported lines. The exporter preserves every non-whitespace drawing token; no native board, fabrication layer, drill coordinate, PDF or3D image is changed by this normalization. The complete E1→E2 Git diff is checked, including newly added review files.
