# RF80 M3B-E2 — independent review package

Date: **2026-10-15**. **REVIEW ONLY; NOT A MANUFACTURING RELEASE.** No order, upload, fabrication, assembly or power-up occurred. This is the existing210×160mm,2layer evaluation board with focused corrections. E1 is preserved at Git tag **m3b-e1**, commit **55a5b3f**; its review files are unchanged and must not be used as E2 assembly instructions.

Q403 ST BD140 physical **1B/2C/3E** now has **1SHAPE_BASE/2VPA_SHAPED/3VPA_LOAD**, with real180° footprint rotation and1.30mm holes. The face illustrated in ST drawing0016114E points toward **PCB+Y/bottom edge**: with that face toward the viewer, pin3west/left,pin2middle,pin1east/right. Additional U311 TI TL431DBZ wiring is corrected to **1K+2REF reference /3A ground**. Only local U311 copper was rerouted; normal/Fox RF topology and routing are preserved. All five formerly ignored DRC categories are now enabled. See [corrections](../../../../docs/M3B_E2_CORRECTIONS.md).

## Review files

| Artifact | File |
| --- | --- |
| Editable project / PCB / electrical manifest | [project](../../RF80.kicad_pro), [schematic](../../RF80.kicad_sch), [PCB](../../RF80.kicad_pcb), [manifest](../../RF80.electrical.json) |
| Fresh fifteen-page schematic / actual netlist | [PDF](RF80.pdf), [XML](RF80.xml) |
| Copper previews | [top](top-copper.svg), [bottom](bottom-copper.svg); native coordinate views, not ambiguous flipped assembly photographs |
| Assembly / placement | [top PDF](assembly.pdf), [top SVG](assembly.svg), [bottom PDF](assembly-bottom.pdf), [bottom SVG](assembly-bottom.svg), [full placement CSV](RF80-position-full.csv), [population map](population-map.csv) |
| Actual KiCad3D renders | [isometric](RF80-3D.png), [top](RF80-3D-top.png), [bottom](RF80-3D-bottom.png), [Q403 detail](RF80-Q403-3D.png). Own dimensional envelopes are identified in the mechanical report; no qualified supplier CAD claim |
| Fabrication / drill | [Gerber/drill directory](gerbers/), [drill report](drill-report.rpt); separate PTH/NPTH and PDF drill maps. Gerber job includes revisionE2 |
| Connectivity / tests | [IPC-D-356](RF80.ipc), [ERC](ERC.json), [DRC](DRC.rpt), [DRC JSON](DRC.json), [probe map](probe-map.csv), [manufacturer pinout checks](critical-pinouts.json) |
| Audits / physical limits | [DRC coverage](drc-coverage.json), [all check severities](drc-coverage.csv), [E1/E2 geometry changes](connectivity-change-audit.json), [local branch changes](local-copper-changes.json), [mechanical/stack-up](mechanical-stackup.json), [fabrication checks](fabrication-audit.json), [sources](source-identities.json), [verification guide](verification.md), [executed command logs](verification-results.json) |
| Manufacturing / assembly restrictions | [manufacturing notes](manufacturing-notes.md), [bounded bring-up](../../../../docs/M3B_E2_POWER_PROTECTION.md) |
| Cost / BOM | [E1/E2 delta](cost-delta.json), [itemized E2 BOM](../../../../docs/M3B_E2_BOM.csv), [workbook](../../../../docs/M3B_E2_COMPONENT_WORKBOOK.md) |
| Integrity | [file manifest](file-manifest.json), [SHA-256 list](SHA256SUMS); verify from repository root |

Current **ERC/DRC/parity/unrouted0**,664 physical pad memberships,55 manufacturer device assertions/10 negative cases, retained R1 **256/31/16** ideal logic regressions. These do not establish hardware safety. Independent engineering review and explicit user approval are required before any order. Finished-hole capability/quote is pending; current supplier observations are dated rather than reserved stock. All physical RF/power/thermal/timing gates are **NOT_RUN**.

[Review decision](../../../../docs/M3B_E2_REVIEW_DECISION.md). The prior `M3B-E1` files and the archived R1/R0 artifacts remain for comparison, not current instructions. Do not regenerate the initial-placement PCB or reapply the one-shot E1→E2 patch to this routed revision.
