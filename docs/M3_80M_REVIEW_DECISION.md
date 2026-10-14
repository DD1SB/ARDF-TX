# M3A — current electrical review decision

Date: **2026-10-14**. Current revision **M3A-R1**; R0 remains in Git tag `m3a-r0`.

The [R1 review decision](M3A_R1_REVIEW_DECISION.md) supersedes R0 functional-check and cost claims. [Editable schematic](../hardware/80m/RF80.kicad_sch), [PDF](../hardware/80m/review/RF80.pdf), [logic audit](M3A_R1_LOGIC_AUDIT.md), [simplification](M3A_R1_SIMPLIFICATION.md), [BOM](M3_80M_BOM.md), [cost delta](M3A_R1_COST_DELTA.md) and [verification](M3A_R1_VERIFICATION.md) describe the current candidate.

U202 polarities and additional startup/rearm/path-transfer defects are corrected; ERC is zero. Full/Fox populations have18/13 ICs. At quantity ten: €26.60/€10.80 component estimates, complete Fox€59.43 materials. No RF, timing, thermal, antenna or endurance hardware qualification exists. Current digital and passive simulations do not establish analog fail-off.

Conditional recommendation: review this schematic, then authorize one small evaluation layout with accessible logic/power/RF tests. No PCB/layout/ordering/fabrication/assembly is performed here. Product release is NO-GO pending the [physical gates](M3A_R1_VERIFICATION.md) and [E0–E9](M3_80M_TEST_PLAN.md). Architecture/2 m true-AM targets remain unchanged; ADR-0012's R1 amendment remains proposed.
