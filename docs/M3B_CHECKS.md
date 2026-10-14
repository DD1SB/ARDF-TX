# M3B — reproducible check record

Date: **2026-10-14**, M3B-E1. **CAD/logic/passive-model verification only. All hardware qualification NOT_RUN.** Native KiCad10.0.6, pcbnew Python binding from system Python, ngspice and standard Python3 are the check dependencies. Local FreeRouting2.5.0/Java25 were used for initial routing; the checked-in PCB is the final authority and export/check commands do not require rerouting.

```sh
python3 tools/m3b_exports.py --render
/usr/bin/python3 tools/m3b_verify.py
python3 tools/m3b_bom.py
python3 tools/m3b_power_analysis.py
python3 tools/m3b_documentation.py
python3 tools/m1_analysis.py --check
python3 tools/m1_costs.py --check
python3 tools/m2_checks.py
```

For a headless nonvisual export, omit`--render`; a working display/Mesa is needed for KiCad3D. The local rendering used a temporary Xvfb display and software rendering. No image-generation substitute or hand-drawn PCB picture is supplied as a3D render. To record new reviewed export hashes after an intentional CAD change, use`python3 tools/m3b_documentation.py --write`, then check again without`--write`.

| Check | Result |
| --- | --- |
|Current schematic ERC |0 reported violations across15 pages |
|Current all-severity DRC |0 violations;0 unrouted;0 schematic-parity differences; no DRC exclusions |
|Physical pad/net parity |664 memberships;273 schematic footprints,4 board-only mounting holes |
|Logical regression on **M3B XML** |256 static combinations,31 state scenarios,16 assumed timing corners; inverted-watchdog unsafe regression reproduced and both physical-polarity mutations rejected |
|R1 safety preservation |Every existing IC pin/net unchanged. Only old D301/R313/C314 pack-node connections change; new R350/C350/C405 and52 pads added |
|Geometry |2 layers,210×160×1.6 mm; minimum routed0.15 mm;328 ordinary0.6/0.3 vias; no via center inside an SMD land; all assigned3D model paths resolve |
|Fabrication exports |Nine Gerber layers/X2 plus job manifest; separate metricPTH/NPTH; drill maps/report;371 PTH/four3.2 mm NPTH; IPC-D-356 and full-population placement |
|BOM arithmetic |Actual196/115 physical purchases,18/13 ICs; six batch sizes per population, pooled MOQ/multiples/price breaks; no test-pad purchase |
|Passive input analysis |32 analytical corners and24 generic-diode ngspice cases; bounded-harness versus100 µH stress distinguished |
|Passive driver analysis |5 actual ngspice cases; imposed100 µs delay fails12.6 V, imposed20 µs examples pass; no timing guarantee inferred |
|Documentation |All local Markdown destinations/anchors checked, eight current review/check/source docs present; CAD/export hashes recorded |

KiCad's inherited ERC disables four informational/configuration checks: `single_global_label`, `four_way_junction`, `simulation_model_issue`, `footprint_filter`. This is **not all possible ERC rules enabled**. The explicit package/pin/net checks supplement those settings. No electrical pin conflict is waived as an ERC exclusion. Final DRC uses all severities and no excluded violation. Five inherited DRC checks remain disabled and are dispositioned explicitly:

| Disabled DRC category | Technical disposition |
| --- | --- |
|Footprint has no courtyard |Test/probe features have no purchased body; custom body/winding envelopes and native courtyard clearances are reviewed separately. No claim that every footprint has a complete assembly courtyard |
|Track endpoint not centered on via |Local routing may enter an ordinary via off-center; copper connectivity/clearance and drill annular ring remain checked. No high-speed tuning requirement depends on this cosmetic constraint |
|Tuning-profile geometry |No differential pairs/length-tuned timing or controlled-impedance profile on this3.5 MHz evaluation board; physical logic-race tests still required |
|Symbol footprint filters |Local manufacturer-specific/library-derived symbol names do not all match generic filter wildcards; actual MPN/package/pad mapping is checked explicitly |
|Component type versus pads |Probe/hybrid wound/landing features include deliberate mixed/manual assembly classifications; actual pad and population maps are checked. This is not permission to substitute an incompatible package |

The disabled categories do not hide an excluded short, unrouted connection, spacing violation or parity error. Their dispositions and all non-CAD physical gates remain part of independent review.

The complete historical R1 suite was run before work at`0dfd224` and again against a clean temporary archive of that commit after development: `m3_80m_checks.py`, `m3a_r1_logic.py`, `m3a_r1_driver_fault.py`, `m3a_r1_report.py`, `m3a_r1_documentation.py`. Those historical checks intentionally assert **no PCB** and frozen R1 hashes/counts; running them against M3B's new PCB/manifest would be the wrong version contract. The current board uses the same actual-pin logic implementation through`m3b_verify.py`, with `RF80_NETLIST` selecting the current XML; results are written separately to [M3B_LOGIC_RESULTS.json](M3B_LOGIC_RESULTS.json). Historical M3A files are not overwritten to create an artificial pass.

[CAD/geometry results](M3B_CHECK_RESULTS.json), [passive analysis](M3B_POWER_ANALYSIS.json), [artifact hashes](../hardware/80m/review/M3B-E1/ARTIFACT_HASHES.json). Source access failures are in the [dated log](M3B_SOURCES.md); no claim of universal external-link success or fresh distributor stock is made. Remaining analog reset, fault delay, RF, thermal, antenna, isolation and endurance tests are explicit in [safety gates](M3B_SAFETY_GATES.md) and [bring-up](M3B_BRINGUP_PLAN.md).
