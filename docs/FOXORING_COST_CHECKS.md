# Foxoring audit checks and current evidence boundary

Date: **2026-10-13**. Documentation and cost/energy arithmetic only. **No parts bought, RF hardware built/measured, firmware implemented, PCB layout generated or hardware qualification passed.** Original M1/M2 calculations, documents and passive simulation artifacts are preserved.

## Local checks

```text
python3 tools/m1_analysis.py --check
python3 tools/m1_costs.py --check
python3 tools/m2_rf_analysis.py --check
python3 tools/m2_system_costs.py --check
python3 tools/m2_checks.py
python3 tools/foxoring_costs.py --check
```

The [Foxoring helper](../tools/foxoring_costs.py) checks both old M1→M2 bridges, fresh generated Markdown/CSV/JSON, per-part quantities/customer minimums, exact CSV-ledger closure and price-summary consistency. It verifies the locked MCU/RTC/source/fail-off/matching components remain, watt/VHF components are excluded and the 20/40-cell demand uses only the observed ten-cell break. Reserves have no fictitious physical purchase count. Each batch has **77 unit material/provision rows, three shared-equipment rows and one fleet freight row**, for **162 exported ledger rows**. The ten-unit bridge closes at **€48.05**; the twenty-unit bridge at **€44.80**.

All prior documentation/model checks remain required: twelve M1 deliverables, 117 original BOM rows/68 catalog entries, eight AM calculation cases, 48 original all-in baskets/twelve standalone comparisons and the previously recorded 496 ideal passive simulation samples. **No new simulation was run in this cost audit.** The new pack runtime is a calculation using smaller cell capacity, not a measured current/endurance pass. BMS, charging, mechanical fit, RF/calibration/field, timing and optional-LoRa gates remain open.

## External evidence and access

Command: `python3 tools/m1_analysis.py --external-links --incremental`. New source references are checked for reachability while prior outcomes are preserved. The first audit attempt encountered sandbox DNS failures; the approved network rerun retries those errors rather than presenting them as remote source failures. GET/first1,024-byte status does not authenticate full content, prices, stock, copyright or qualification. Full current results are in [the dated audit](M1_EXTERNAL_LINKS.json); browser/download evidence and manual access failures are separately recorded in [Foxoring sources](FOXORING_COST_SOURCES.md).

Current audit: **173 distinct URLs, 129 reachable HTTP200, 44 unresolved**. Thirteen new URLs were checked on the network rerun; eleven were reachable and two remained unresolved. Original non-DNS outcomes were retained. Manual TinyFox website and other content-access limitations remain separately disclosed; an HTTP200 result does not turn supplier/index data into a live quote.

TinyFox's current site could not be inspected; its historical author manual/report were used with dates and scope limitations. Fixle's Word document was downloaded/read via antiword and its identity hash recorded, with no source copy committed. The direct NKON protection listing overrides its category: discontinued/out of stock, excluded. The direct 35E page overrides the older in-stock index. LaskaKit's live-price claim is distinct from its missing manufacturer datasheet and unpassed pack qualification.

## Result

Current local result: **40 Markdown files, 233 relative destinations/anchors, all 68 requirements traced, zero local errors**. All six commands above passed. Accounting and documentation consistency do not prove prices, physical fit, build yield or the 10mW/30m/250m requirements. Labor, instruments, actual bulk-material minimums and rejected/spare material are OPEN, not free. [Audit](FOXORING_COST_AUDIT.md), [itemized bill](FOXORING_COST_BOM.md) and [ADR-0009](decisions/ADR-0009-foxoring-fleet-cost-scope.md) are reviewable; no full set or ordering release is authorized.
