# M1 — Feasibility and Architecture acceptance criteria

M1 is a research/design-decision milestone. It **must not** produce PCB gerbers or claim a tested RF design.

**Revised M1 architectural baseline conditionally accepted 2026-10-13. M2 circuit/evaluation preparation is authorized; complete layout/procurement and a full transmitter set remain gated.** Checked documents do not mean feasibility gates have passed. VHF AM/driver suitability, supporting prices, compact field qualification, actual energy measurements and country/referee inputs remain unresolved.

## Deliverables (docs)

- [x] `docs/M1_FEASIBILITY.md`: candidate 80 m and 2 m RF solutions with source-based evidence; AM approach and risks; hard disqualifiers.
- [x] `docs/M1_SYSTEM_ARCHITECTURE.md`: 3-board split, synthesis placement proposal, safe inhibit, synchronization and electrical functions without footprint lock.
- [x] `docs/M1_REQUIREMENTS_TRACE.md`: all requirement IDs, rule sections, derived tests, open assumptions.
- [x] `docs/M1_POWER_BUDGET.md`: all packs/profiles/standby/LoRa/losses/peaks and conditional 24 h model; continuous beacons separate.
- [x] `docs/M1_BOM_CANDIDATES.md`: revised material scope and itemized 6/10/20 quantities/MPNs/supplier codes/stock/prices, with estimates and unresolved supporting codes/values. Candidate, not price-closed ordering BOM.
- [x] `docs/M1_REGULATORY.md`: competition distinct from national law, conditional Germany example and unresolved mask/country inputs.
- [x] `docs/M1_RISK_REGISTER.md`: scored risks and prevention/verification/owner gates.
- [x] `docs/M1_VALIDATION_PLAN.md`: independent measurable methods, instruments and required field tests; no passed hardware assertions.
- [x] `docs/M1_DECISION.md`: revised cost/architecture review summary, endurance and explicit decisions. Conditional architecture acceptance; no manufacturing readiness.

## Cost-rework additions

- [x] `docs/M1_COST_REWORK.md`: architectural reconsideration, minimal historical RF evidence, cost drivers, alternative/population/synthesis comparisons and budget feasibility limits.
- [x] `docs/M1_COSTED_BOM.md`: generated itemized candidate workbook; CSV/catalog/JSON retain quantities, observed price breaks, estimates and source URLs.
- [x] `docs/M1_COST_SOURCES.md`: dated primary design/component/distributor evidence, conflicting inventory/prices and unavailable sources.
- [x] ADR-0007 conditionally accepted at architecture level; ADR-0008 remains proposed; earlier implementation proposals reconciled; required RF/antenna/timing/safety preserved and power model revised without invented current savings.

The rework is delivered for review, but target prices are not validated: VHF's EUR30 ceiling remains missed with the presently sourced MMIC driver; the fitting discrete alternative relies on EOL stock. Unquoted material and measured RF performance remain gates. Current driver policy excludes BFP650; its cost comparison is historical.

## Hard gates

1. 2 m A2A transmission topology and power-vs-ERP-to-PEP budget physically plausible, with cited reference or clearly flagged R&D experiment.
2. 80 m Classic/Sprint and 10 mW continuous Foxoring levels plausible, including **two distinct physical antenna installations**: longer Classic/Sprint wire + counterpoise and approximately 30 cm Foxoring vertical + compact counterpoise. Include independently justified matching/loading/coupling, conducted-power reference, environmental sensitivity and a repeatable 30 m/250 m field test. A 10 mW dummy-load measurement is necessary but not sufficient.
2a. Choose or propose a safe, costed antenna-interface strategy (shared port + adapter, separately switched match, or separate ports) and address accidental full-power drive into the Foxoring radiator/matching path; no unexplained accessory cost exclusions.
3. Two-frequency-group Sprint schedule models 12 s slots correctly and autonomous timing possible without LoRa.
4. Battery sizing includes 2S1P–2S4P and 24 h requirements with explicit idle-power sensitivity; cannot claim a 2S1P pass without computation.
5. Connector and fail-off philosophy documented; RF tests are repeatable.
6. Two or more synthesis/topology alternatives compared, plus low-cost handheld modification as baseline.
7. Cost estimates have realistic parts/MOQ/distributor evidence and disclose unknown costs.
8. Conditional M1 acceptance permits circuit/evaluation preparation. No complete layout/procurement or full-set manufacture before the relevant measured RF gates and subsequent review; no hardware validation claim.
