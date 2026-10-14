# RF80 M3B-E1 — engineering review package

2026-10-14. **NOT A MANUFACTURING RELEASE. No order/upload/fabrication/assembly/energizing authorized.** Native board is [RF80.kicad_pcb](../../RF80.kicad_pcb); root project/schematic and local libraries are two levels up. BaselineR1 is [archived separately](../M3A-R1/).

- [Schematic PDF](RF80.pdf), [KiCad XML netlist](RF80.xml), [ERC](ERC.json), [DRC text](DRC.rpt) and [DRC JSON](DRC.json).
- [Top copper](top-copper.svg), [bottom copper](bottom-copper.svg), [assembly SVG](assembly.svg), [assembly PDF](assembly.pdf), [3D isometric](RF80-3D.png), [3D top](RF80-3D-top.png). Bottom copper is plotted in the common top-view coordinate system, **not mirrored for manufacturing**; Gerbers are likewise standard factory coordinates. All fitted components are on top.
- [Review Gerbers/drills](gerbers/): nine layers, X2 attributes/job, separatePTH/NPTH inmm, PDF drill maps. [Drill report](drill-report.rpt). Outline210×160 mm, two copper layers1oz/1.6 mmFR4. No controlled impedance/blind vias. No upload has occurred.
- [IPC-D-356](RF80.ipc), [full placement](RF80-position-full.csv), [all population/position mappings](population-map.csv), [probe map](probe-map.csv). Full placement excludes DNP/test pads and remoteTH301. It is **not the Fox assembly list**; use the population map/current BOM. Holes/pads/flags are not purchased parts.
- [Checks/hashes](ARTIFACT_HASHES.json), [review decision](../../../../docs/M3B_REVIEW_DECISION.md), [layout](../../../../docs/M3B_PCB_LAYOUT_REVIEW.md), [component qualification](../../../../docs/M3B_COMPONENT_QUALIFICATION.md), [safety gates](../../../../docs/M3B_SAFETY_GATES.md), [bring-up](../../../../docs/M3B_BRINGUP_PLAN.md), [evaluation costs](../../../../docs/M3B_EVALUATION_BOM.md).

Routing-input DSN, local routing session and planning JSONs are provenance aids, not fabrication sources. The native board, current XML and Gerber/drill exports are authoritative. Wound bodies and two missing native models use own clearly identified dimensional envelopes; model availability is not incoming mechanical qualification. All physical safety/RF/thermal gates remain NOT_RUN.
