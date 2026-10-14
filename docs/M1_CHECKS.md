# M1 documentation and analysis checks

Date: **2026-10-13**. This preserves the M1 check record; [M2 preparation checks](M2_CHECKS.md) contain the current combined results and expanded external audit. These are documentation and arithmetic checks only. **No ARDF-TX RF hardware, firmware or battery life has been validated.**

The initial repository had no documentation/test/build scripts. The [analysis helper](../tools/m1_analysis.py) and [cost workbook helper](../tools/m1_costs.py) use the Python standard library. They perform no procurement, firmware build or hardware control.

## Historical M1 check record

Commands:

```text
python3 tools/m1_analysis.py --check
python3 tools/m1_costs.py --check
python3 tools/m1_analysis.py --rework
```

- All twelve M1 deliverables exist and carry the research date: nine original deliverables and three cost-rework documents.
- All 52 baseline requirement IDs appear in traceability, including six rule corrections and seven cost-rework requirements.
- Relative Markdown destinations and referenced anchors resolve.
- Nine revised energy-profile runtime rows agree with the model. Pack energy, VHF carrier/mean/PEP/headroom and the revised driver overheads are calculated from explicitly unmeasured inputs.
- Candidate board/configuration baskets use real observed price breaks where available, assumed MOQ1 for estimates, and batches of 6/10/20. No selected customer MOQ or order multiple requires a 1,000/3,000-piece reel. Ordered counts cover modeled demand.
- The generated Markdown/JSON workbooks agree with their CSV and part catalog. Mandatory detachable power connectors and both RF port families are included in the separately disclosed wiring scope.
- Analytical Sprint half-open slots pass over two cycles, with one transmitter active in each concurrent frequency group. This is a schedule calculation, not a firmware test.
- At this historical check, ADR-0003 through ADR-0007 were Proposed. The later user review conditionally accepted the architecture; [current preparation checks](M2_CHECKS.md) record the updated disposition and results.

Nominal universal electronics are **€69.54 / 62.33 / 61.90** per unit at 6/10/20. Mandatory power/RF connector material adds **€5.20 estimated**, giving **€74.74 / 67.53 / 67.10** before actual cable/crimps/strain relief. The VHF board's target miss, EOL alternative and unquoted supporting material remain explicit in the [review summary](M1_DECISION.md). These checks establish arithmetic consistency, not attainable manufacturing prices.

## Historical M1 external link audit

Command: `python3 tools/m1_analysis.py --external-links --incremental`. The original audit covered 80 URLs; the rework checked 52 new URLs, then five references added by final sourcing reconciliation. One superseded category URL was retired, and unchanged results were retained. Initial sandbox network failure was rerun with approved network access.

**136 distinct URLs: 104 reachable HTTP 200; 32 unresolved.** Full dated statuses and redirects are in the [link audit](M1_EXTERNAL_LINKS.json). The checker performs GET and reads only the first 1,024 bytes. HTTP success does not authenticate complete source content, licenses, stock or prices.

| Unresolved group | Count | Treatment |
| --- | ---: | --- |
| DigiKey product links, HTTP 403 | 16 | Script access blocked; inspected indexed distributor excerpts remain labeled observations, with inventory/price conflicts open. |
| Farnell selected HF offer, HTTP 403 | 1 | Indexed price/stock inspected; browser cache miss and direct script restriction disclosed. Live basket still required. |
| Microchip product links, HTTP 403 | 2 | Primary indexed product evidence recorded; detailed thresholds/order verification remain open. |
| Onsemi datasheet / TME offer, HTTP 403 | 2 | Indexed evidence and rejected offer recorded; no missing measurements or prices invented. |
| NXP historical AFT links, HTTP 404 | 2 | Legacy/EOL evidence only; excluded from current-production selection. |
| EUR-Lex, HTTP 202 challenge | 1 | Consolidated legal text not fully verified; no blanket legal authorization claimed. |
| ADI PDFs timed out | 2 | Primary browser PDF evidence was inspected; script failures remain disclosed. |
| Micro Crystal PDFs timed out | 2 | Browser primary documentation inspected earlier; complete script fetch failed. |
| ST product/datasheet links timed out | 3 | Manufacturer product/datasheet evidence inspected in browser; this audit failed separately. |
| DL7VDB bibliography, certificate hostname mismatch | 1 | Indexed bibliography used with explicit access limitation; CQ-DL original article not obtained. |

Manual/browser findings, licenses and access boundaries are in the [research register](research-register.md) and [dated cost sources](M1_COST_SOURCES.md). A browser or search-index observation can differ from a direct script fetch; neither turns an unmeasured derivative into validated hardware. Earlier failed PE5EDW/OZ2M historical links are recorded but are not active supporting links. Netherlands/G3ZOI/DF1FO downloads recovered earlier browser failures; RA3APW's HTTP page recovered its HTTPS mismatch.

## Primary PDF identity

Downloaded and read on 2026-10-13; SHA-256:

```text
IARU ARDF-Rules_B_2025.pdf
9e4f0760f166124fcb2d0443860dcaa539fbadb00b9bf0f4390c5e1ba45ebd09

VERON ARDF_ontwikkeling_in_Nederland.pdf
399529dc70a39381f9c25579040d69f668cfdf30d9cf5295c7d10d185047c95d
```

Downloaded third-party research copies remain temporary files. No third-party CAD/firmware was copied into the deliverables. A hash establishes identity, not redistribution rights.

## Historical M1 local result

Final counts are recorded after this report's own links are checked: **26 Markdown files, 108 local links, 52 requirements, twelve deliverables, nine profile rows, three combined batch totals, 117 BOM rows and 68 catalog entries; zero local errors.** All price-closure, hardware, country and referee gates remain open as stated in the review summary. External access failures remain unresolved.
