# M5B-E6 — power/transient study and common-cooler HOLD

**Engineering HOLD before native PCB modification. No E6 manufacturing candidate.**

Starting source: `256c64888b680f5152e92f035e2ea0676a83630a`, local branch `m5b-e6-unified-heatsink`. Active RF2M native CAD remains E5. Controller M6-L2, RF80 and all historical reviews remain unchanged. No hardware was ordered, energized or pushed to public main.

The [decision](../../../../docs/M5B_E6_REVIEW_DECISION.md) explains the unresolved ordinary-process PA source/interface and RF-loss/protection envelope. The normal-duty calculation supports considering one small common cooler; it does not establish a released safe assembly. Gate H remains NOT_RUN and is distinct from this pre-manufacture closure gap.

| Evidence | Entry points |
| --- | --- |
| Native-derived power ledger | [Power audit](../../../../docs/M5B_E6_THERMAL_POWER_AUDIT.md), [JSON](power-audit.json), [state CSV](power-states.csv) |
| Coupled transient calculation | [Method](../../../../docs/M5B_E6_TRANSIENT_THERMAL.md), [curves](transient-responses.pdf), [all scenarios](transient-results.json), [summary](transient-summary.csv) |
| PA bottleneck/interfaces | [Initial source-sheet FVM](E6-source-path-FVM.json), [alternatives](source-interface-alternatives.json), [same-point fault envelope](native-fault-envelope.json), [closure](thermal-path-closure.json) |
| Mechanical/cost feasibility | [Common cooler](../../../../docs/M5B_E6_UNIFIED_HEATSINK.md), [simplified concept sections](common-cooler-concept.pdf), [assembly limits](../../../../docs/M5B_E6_MECHANICAL_ASSEMBLY.md), [costs](cost-comparison.json) |
| Populations | [Native read-only costing CSV](population-costs.csv), [cost explanation](../../../../docs/M5B_E6_COST_COMPARISON.md); no E6 electrical BOM changes |
| Actual fresh checks | [Execution counts](execution-results.json), [25 numerical tests](analysis-test-results.json), [unchanged E5 native replay](baseline-regression/), [raw logs including failures](logs/) |
| Preservation/reproduction | [Native hashes](native-preservation.json), [historical hashes](preserved-baseline.json), [commands](REPRODUCE.md), [SHA-256](SHA256SUMS.txt) |

Fresh E5 checks: ERC 0/0; DRC 0 errors, **11 preserved courtyard warnings**, zero unrouted/parity; no exclusions; 4,096 combinations; standard DFM PASS. The requested E6 zero-warning/mechanical/cutout/insulation gates are not claimed passed. Numerical tests check actual native geometry/input values and physical equations; they include detection of unsafe sensitivity cases, so a passing test suite is not thermal acceptance.

Native E6 sources, Gerbers, drills, stencil/fabrication ZIP, final machining drawings, full native 3D assembly/exploded/enclosure views: **NOT_CREATED at HOLD**. Concept plots are simplified feasibility geometry and explicitly marked accordingly. Existing E5 fabrication files are historical, temporarily HOLD for manufacturing under this task. No historical archive was regenerated.
