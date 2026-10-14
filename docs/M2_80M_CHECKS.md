# M2 80 m comparison verification record

Date: **2026-10-13**. Documentation, arithmetic and source-access checks only. **All hardware gates NOT RUN.**

## Commands and results

| Check | Result / scope |
| --- | --- |
| `python3 tools/m1_analysis.py --check` | PASS: 51 Markdown files, 292 local links/anchors, 68 traced requirements;12 preserved M1 deliverables and9 historical profile rows. |
| `python3 tools/m1_costs.py --check` | PASS: 117 historical BOM rows, 68 catalog parts,6/10/20 arithmetic unchanged. |
| `python3 tools/m2_rf_analysis.py --check` | PASS: 8 preserved RF/envelope calculation cases; no new transistor simulation. |
| `python3 tools/m2_system_costs.py --check` | PASS: 48 historical all-in baskets retained. |
| `python3 tools/m2_checks.py` | PASS: 8 preparation documents,8 review requirements,10 historical gates,496 existing ideal-passive SPICE samples and preserved power/cost checks. |
| `python3 tools/foxoring_costs.py --check` | PASS: 77 material rows per batch,162 ledger rows, original €48.05 bridge and55.24/63.34 ten-unit scopes unchanged. |
| `python3 tools/m2_80m_analysis.py --check` | PASS: 16 new comparison baskets at 6/10/20,1845 cost-ledger rows,10 profiles, both 1P–4P capacity cases, canonical CSV, MPN purchase allocation, TTL driver selection and six deliverables. |

The new checker verifies170/131 upstream schematic inventory records, absence of normal PA/driver/converters from Fox-only population, retention of hardware lease/bus isolation, unchanged Fox baseline and exact cost/energy arithmetic. Shaper stress calculations independently check 0.57/2.45 W resistive-surrogate peaks; these are estimates, not SOA tests. It does not prove schematic correctness or stock.

## Primary evidence and access limitations

Original reference schemes, BOM variants and PCB layouts were inspected read-only. FlexFox80 and SignalSlinger commits are pinned; source hashes include their original CAD/BOM files. Licensed schematic renderings and metadata are attributed in [the MIT notices](assets/80m-reference/LICENSES.md). No project CAD, Gerber, firmware binary or production firmware source was created. Temporary upstream downloads are outside the project.

DF1FO/Fixle MS Word drawings were recovered through temporary PDF conversion; Eagle4 binary files were retrieved but electrical import/version matching remains OPEN. ON7YD's HTTPS drawing/ZIP returned 403; its HTTP drawing was retrieved/viewed, while ZIP terms remain inaccessible. Google documents/workbook exports were readable; the 2025 BOM differs from current SignalSlinger hardware3.5. No price, performance or revision equivalence was invented to fill these gaps.

Final incremental GET audit: **206 distinct URLs, 161 HTTP200/reachable, 45 unresolved**; detailed statuses are in [the extended source audit](M1_EXTERNAL_LINKS.json). Existing cached failures remain visible. A successful first 1024-byte GET does not validate page content, prices, inventory, manufacturer lifetime or publisher measurements. Browser/index observations and direct downloads can differ from that generic checker; source-specific limitations are recorded in [the comparison](M2_80M_REFERENCE_COMPARISON.md).

## Evidence boundary and disposition

Publisher measurements/claims, actual source inspection, historical/current pricing observations and our estimates remain separate. No new RF/antenna/thermal/efficiency/battery/timing/fault/LoRa experiment ran. The old seven-pole ideal simulation does not validate the new reference filter or PA. [H0–H9](M2_80M_VALIDATION_GATES.md) all remain NOT RUN. [ADR-0010](decisions/ADR-0010-proven-80m-core-and-power-target.md) is proposed; accepted architecture and 2 m decisions are preserved. Stop for architectural review before physical development.
