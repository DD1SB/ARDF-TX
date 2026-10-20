# M6-L2 final reproduction evidence

Read the [final report](../../M6_L2_FINAL_REPRODUCTION.md) for disposition, failures, exact commands and limits. This directory records the fresh 2026-10-20 execution separately from the immutable accepted [implementation review](../../../hardware/controller/review/M6-L2/README.md).

- `execution.json` and numbered `.log` files: complete successful sequence after the portability corrections.
- `initial-failure/` and `missing-input-failure/`: original failed attempts, retained in full.
- `fresh-results/`: CAD, host, electrical, mutation, DFM, manufacturer, population, geometry and export-command results executed in this run.
- `artifact-comparison.json`: SHA-256 and classification of all 191 accepted/regenerated files, including every ZIP entry.
- `classification-review.json`: explicit explanations/diffs for reporting and provenance differences.
- `hardware-preservation.json`, `native-input-preservation.json`: RF/historical and current-controller preservation checks.
- `frozen-validator-regression.json`: three additional negative tests for the narrowly scoped UI-state correction.
- `regenerated-inventory.json`, `regenerated-SHA256SUMS`: isolated-checkout output provenance. These describe the regenerated files, not copies stored in this evidence directory.
- `publication-inputs.json`: current input hashes after publication documentation changes. `SHA256SUMS` binds this evidence directory and excludes itself.

The runner and comparison scripts record the actual absolute checkout/cache paths used. They can be adapted to another isolated checkout; run `compare.py` before `finish-comparison.py`. The latter asserts each explicitly understood reporting difference. Original cache reference files, manufacturer STEP and duplicate manufacturing/render datasets are not redistributed here. Private regenerated output remains under `/tmp/ardf-m6-l2-final-reproduction`; equivalent accepted manufacturing data remains in the implementation review.

No CAD or population was changed. No physical measurement, procurement, supplier upload or production release is represented by these files.
