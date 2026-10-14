# M2 preparation checks and evidence boundary

Date: **2026-10-13**. M1 architecture is conditionally accepted; detailed RF proposals remain subject to review and measured gates. **No ARDF-TX hardware, RF performance, battery endurance or production firmware has been validated.** No procurement, full-set manufacture, PCB routing or fabrication export occurred.

This preserves the M2 preparation check record. The later [Foxoring audit checks](FOXORING_COST_CHECKS.md) contain current combined counts and the expanded source audit. [Historical M1 checks](M1_CHECKS.md) and original calculations are preserved. [Preparation review](M2_PREPARATION.md) identifies the authorized scope and open inputs.

## Completed local checks

```text
python3 tools/m1_analysis.py --check
python3 tools/m1_costs.py --check
python3 tools/m2_rf_analysis.py --check
python3 tools/m2_system_costs.py --check
python3 tools/m2_checks.py
```

Results: **35 Markdown files, 196 local links and zero local errors** after the final reconciliation. Checks cover the original twelve M1 deliverables, all 60 requirement IDs including PREP-001–008, relative Markdown destinations/anchors and ADR disposition. ADR-0007 records conditional architectural acceptance; detailed implementation remains Proposed in ADR-0003–0006/0008.

The preserved M1 candidate workbook has 117 rows, 68 catalog entries and batches of 6/10/20. Updated calculations check eight sampled AM-envelope cases against their closed-form mean where the assumed one-way pass regulator can realize the requested current. Nine revised profile rows include shaping/helper/standby loads, with four additional universal-board idle sensitivity rows. Cost checks cover 48 all-in configuration/batch/pack baskets and twelve standalone PCB/batch comparisons, ordered quantities, assumed fabrication leftovers, estimate sensitivity and generated-file freshness. None proves live prices, stock, efficiency or runtime.

## Actual simulation and its limits

The original [ideal LPF deck](../analysis/hf_lpf_ideal.cir) ran in **ngspice-42**:

```text
python3 tools/m2_rf_analysis.py --simulate --write
```

All **496 simulated frequency samples** agree with independent Butterworth/Chebyshev transfer formulas to a maximum **0.000451 dB** difference. This verifies the ideal matched passive model only. No transistor, PCB parasitic, core-loss, thermal, modulation-loop or antenna model was simulated. [Recorded samples](../analysis/hf_lpf_ideal.csv) are simulation data, not bench measurements. RF gain/compression, AM quality, unwanted emissions, shutdown, heat/SOA and compact field behavior remain **NOT RUN** under [G0–G9](M2_RF_EVALUATION.md).

## External reachability and inaccessible evidence

Command: `python3 tools/m1_analysis.py --external-links --incremental`. The combined dated audit contains **160 distinct URLs: 118 reachable HTTP 200; 42 unresolved**. Newly added references were checked; unchanged earlier results were retained. The checker uses GET/first 1,024 bytes, so success does not authenticate complete content, licenses, inventory or prices. [Full statuses](M1_EXTERNAL_LINKS.json) and [primary/browser evidence](M2_SOURCES.md) are separate records.

| Unresolved group | Count | Treatment |
| --- | ---: | --- |
| DigiKey product links, HTTP 403 | 16 | Indexed observations labeled; live comparable baskets remain open. |
| Farnell product link, HTTP 403 | 1 | Selected old observation preserved, no binding stock/price claim. |
| Microchip product links, HTTP 403 | 3 | Primary browser/indexed findings recorded separately. |
| Onsemi / TME links, HTTP 403 | 3 | Exact suffix lifecycle and prices remain open where not inspected. |
| NXP historical/EOL links, HTTP 404 | 3 | Excluded from new selection; missing pages not reconstructed. |
| TI TPS61088 product page, script HTTP 404 | 1 | Browser primary page was inspected; script result disagrees, with no reconstruction of missing content. |
| EUR-Lex, HTTP 202 challenge | 1 | Full consolidated legal text not verified. |
| ADI PDF timeouts | 2 | Earlier primary browser evidence retained with limitations. |
| Micro Crystal PDF timeouts | 2 | Earlier primary browser findings retained separately. |
| ST product/datasheet timeouts | 9 | Primary PDF text inspected through browser; direct download failed. |
| DL7VDB certificate hostname mismatch | 1 | Original CQ-DL article not obtained. |

Direct Mini-Circuits PDF access also failed despite an indexed primary typical-data table. BD140 mirror download failed by protocol error/timeout. **Numeric hot-case DC SOA graphs were not reliably digitized; no quantitative SOA pass is claimed.** These manual-access failures are not erased by a separate successful reachability status.

## Final disposition

Documentation/arithmetic/ideal-passive simulation checks permit continued circuit and minimum-fixture review. They do not release complete PCB layout, procurement or a full transmitter set. Preserve separate bounded low-power sources, autonomous hardware fail-off and the original RF/rule requirements. Every measurement gate is open; sourcing, country/referee conventions, exact Silicontra module and protected-pack/charger choices remain explicit inputs.
