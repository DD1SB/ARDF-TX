# M5A-R2 pre-CAD gate review — NOT A MANUFACTURING PACKAGE

Date2026-10-15. **SOURCING GATE OPEN / MILESTONE INCOMPLETE.**

The native project remains M5A-R1, preserved at commit`4785057`, tag`m5a-r1`. This directory does not contain a Mitsubishi PCB or pretend that R1 exports describe R2. See [decision](../../../../docs/M5A_R2_REVIEW_DECISION.md).

- `sources.json`: dated primary/supplier URLs and downloaded-source hashes. Third-party drawings/artwork/full inventory are not redistributed.
- `supplier-observations.json`: manufacturer production rows, GLYN counted alternative inventory, actual retail tiers and unresolved fulfillment.
- `manufacturer-pin-record.json`: RA07 drawing transcription, **not** an actual CAD pinout assertion.
- `inputs.json`, `calculations.json`, `rf-budget.csv`, `source-power-bound.csv`, `operating-states.csv`, `endurance.csv`, `sensitivity.csv`: explicit assumptions and calculations; no measured outcomes.
- `accounting-bridge.csv`, `cost-comparison.json`: itemized R1-derived cost bridge, **not** a new procurement BOM.2S conversion and ancillary circuit costs remain open.
- `preserved-baseline.json`, `verification.json`: original hardware/decision preservation and limited R1 logic/pin regressions. R2 ERC/DRC/layout/pinout tests are **NOT_RUN**.
- `r1-regression-erc.json`, `r1-regression.net.xml`: fresh checks on the preserved fallback, never relabeled as R2 CAD.
- `file-manifest.json`, `SHA256SUMS`: integrity of the review artifacts.

Reproduce from repository root:

```sh
python3 tools/m5a_r2_review.py --cad-regression
(cd hardware/2m/review/M5A-R2 && sha256sum -c SHA256SUMS)
```

`--initialize` is only for the original immutable snapshot and must not be repeated. Ordinary reruns check it. A passing script means review integrity/calculations and preserved R1 regression, **not completion of M5A-R2 or hardware validation**.

No new schematic, netlist, PCB,3D view, Gerber, drill or assembly export exists for Mitsubishi R2. No ordering, fabrication, assembly, power-up or RF transmission occurred. The exact sourcing confirmation required before resuming PCB commitment is documented in the decision.
