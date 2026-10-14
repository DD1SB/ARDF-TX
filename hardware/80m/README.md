# RF80 — M3B-E1 evaluation PCB

Date: **2026-10-14**. **Engineering review only; unbuilt and unenergized.** Open [RF80.kicad_pro](RF80.kicad_pro), [schematic](RF80.kicad_sch) and [native PCB](RF80.kicad_pcb) in KiCad10.0.6. Three primary PCBs and the separate VHF true-AM design are unchanged.

Two-layer210×160 mm evaluation board: protected4S normal Si5351/LM5134B/IRF610 path, approximately3 W full/1.2 W extended/calibrated Sprint targets; separate nominal10 mW Fox path, controller3.3 V/protected2S compatible reduced population. Fifteen schematic pages,273 electrical footprints/four mounting holes,74 test pads. Normal and Fox connectors remain independent. No measured target achievement is claimed.

Current [review package](review/M3B-E1/README.md): [schematic PDF](review/M3B-E1/RF80.pdf), [3D view](review/M3B-E1/RF80-3D.png), [assembly](review/M3B-E1/assembly.pdf), [top copper](review/M3B-E1/top-copper.svg), [bottom copper](review/M3B-E1/bottom-copper.svg), [ERC](review/M3B-E1/ERC.json), [DRC](review/M3B-E1/DRC.rpt), [netlist](review/M3B-E1/RF80.xml), [probe map](review/M3B-E1/probe-map.csv), [populations](review/M3B-E1/population-map.csv), [Gerbers/drills](review/M3B-E1/gerbers/). These are **review artifacts**, not a manufacturing release.

Read the [decision](../../docs/M3B_REVIEW_DECISION.md), [layout review](../../docs/M3B_PCB_LAYOUT_REVIEW.md), [qualification](../../docs/M3B_COMPONENT_QUALIFICATION.md), [safety gates](../../docs/M3B_SAFETY_GATES.md), [staged bring-up](../../docs/M3B_BRINGUP_PLAN.md), [BOM](../../docs/M3B_EVALUATION_BOM.md) and [checks](../../docs/M3B_CHECKS.md). Current ERC/DRC/parity/unrouted0 and pin-derived R1 regression256/31/16 do not prove analog/RF/thermal operation. Driver and PA must remain absent until bounded power-only fault tests pass.

M3A-R1 is preserved at commit`0dfd224` and [archived review files](review/M3A-R1/); R0 at tag`m3a-r0`. Legacy files directly under `review/` and M3A cost workbooks remain historical. Current M3B outputs use the revision directory. [Electrical manifest](RF80.electrical.json) matches current schematic/PCB.

Reproduce from repo root:

```sh
python3 tools/m3b_exports.py --render
/usr/bin/python3 tools/m3b_verify.py
python3 tools/m3b_bom.py
python3 tools/m3b_power_analysis.py
python3 tools/m3b_documentation.py
```

Rendering requires a working display/Mesa; omit `--render` for nonvisual exports. The checked-in PCB is authoritative for final routing. `m3b_pcb.py --place` **replaces it** with initial placement/routing input; do not run it on the reviewed board. Likewise schematic regeneration requires reconciliation with the PCB before exports. Scripts do not upload, order or energize anything. [Attribution/licences](LICENSES.md).
