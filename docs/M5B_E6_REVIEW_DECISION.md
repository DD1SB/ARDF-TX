# M5B-E6 decision — HOLD before PCB modification

Starting commit `256c64888b680f5152e92f035e2ea0676a83630a`; local branch `m5b-e6-unified-heatsink`; analysis executed 21 October 2026, Europe/Berlin. **HOLD for five bare RF2M E6 evaluation boards.** This is a local engineering assessment, not independent acceptance or a production release.

Phase A corrects the steady-state interpretation: a 1 W ERP tone mark is modeled at approximately 1.863 W PA /2.985 W pass /0.101 W helper, not the unrelated simultaneous historical 4/4.24/1.1 W stress allowances. Native Morse spaces retain carrier, and pass loss rises. Classic/Sprint pulse accumulation is far below continuous-beacon equilibrium for nominal operation. A small single extrusion is therefore a credible concept; three separate heatsinks are not justified by simply treating the clean PEP requirement as continuous carrier.

Release is blocked by a narrower problem: the **ordinary-fabrication PA source/interface thermal bound and the valid RF-loss/protection envelope are not closed**. The same-input-energy 40%-efficiency/full-RF-absorption sensitivity produces approximately 133.79°C PA peak with an improved 11.847 K/W source path, while pass case is 56.90°C, NTC 56.44°C and current peak 1.736 A below the nominal 1.797 A trip. Local capacitance/path-allocation sweeps still exceed 125°C. This is not a measured antenna-fault prediction; it exposes uncertainty that cannot be covered by a Q401 sensor, assumed watchdog progress failure or added aluminum mass. The thermal model explicitly retains known copper/via storage.

A favorable source path or bounded lower RF-loss/current response could resolve it. The analysis does **not** prove every shared-heatsink architecture impossible. It does not require completion of all physical Gate H work before a bare-board GO. It requires a defensible pre-manufacturing heat/protection bound, followed by an actually implemented common assembly. No shutdown threshold was raised, power target reduced, independent stress maxima mixed, premium vias assumed or test weakened to claim acceptance.

| Gate | Disposition | Evidence / remaining work |
| --- | --- | --- |
| A — realistic power | Calculated ledger complete; physical envelope OPEN | Native rails, mark/space currents, consistent terminal energy; 144 MHz efficiency/reflection assumptions remain bounded sensitivities |
| B — transient credibility | Method/regressions PASS; safety closure HOLD | Local junction/case/copper/via/bar/plate/fin/sensor network; conditional scenarios exceed unchanged PA ceiling |
| C — unified mechanics | Preferred concept only; NOT_IMPLEMENTED | One SK81 plane, horizontal Q401/Q402 concept; final brackets/holes/lead form/tool access not released |
| D — electrical safety | Original preserved; E6 assembly OPEN | VPA/MOD_SINK isolation and source-ground attachment require actual approved mechanical implementation |
| E — outdoors | Scenarios considered; installation envelope OPEN | Orientation, obstruction, solar and guarded-surface requirements; no physical fire/outdoor claim |
| F — RF/electrical preservation | Unchanged baseline replay PASS | 4,096 logic combinations, package maps, controller connector and source/matching geometry retained |
| G — standard manufacturing | E5 DFM PASS; E6 NOT_CREATED | No special process proposed; no E6 native/fabrication dataset; 11 baseline courtyard warnings remain visible |
| H — physical thermal/RF | NOT_RUN | First instrumented assembly and staged RF/thermal tests still required |

Close the RF-loss/current envelope using defensible device/circuit evidence; close the source-joint/via/interface resistance/transient bound under ordinary fabrication and achievable contact pressure; if needed propose a separately justified fast PA-specific interruption without relaxing safety. Then complete native common-cooler supports/insulation/cutouts and independent mechanical/RF/DFM review. The final E6 assembly must use one independently supported thermal structure, with no separate Q401/Q402 sinks.

All native designs, historical E5 evidence, published commits and tags are preserved. E5 remains the active historical PCB, with manufacturing temporarily HOLD under this task. Controller M6-L2 and RF80 remain unchanged. No E6 manufacturing ZIP or native assembly is falsely released. No push, order, stencil purchase, acceptance tag or hardware operation occurred.

See [power audit](M5B_E6_THERMAL_POWER_AUDIT.md), [transients](M5B_E6_TRANSIENT_THERMAL.md), [common cooler](M5B_E6_UNIFIED_HEATSINK.md), [mechanics](M5B_E6_MECHANICAL_ASSEMBLY.md), [costs](M5B_E6_COST_COMPARISON.md), [regression](M5B_E6_RF_REGRESSION.md), [manufacturing](M5B_E6_MANUFACTURING.md) and the [review/reproduction package](../hardware/2m/review/M5B-E6/README.md).
