# ARDF-TX

**M6-L1, 2026-10-18:** the [common controller](hardware/controller/README.md)
supports NO_LORA, Silicontra 433 MHz or 868 MHz on one footprint and RF feed.
The Hirose underbody ground keep-out is locally corrected; the short RF signal
trace, RF80/RF2M interfaces and R1 battery-ID/USB corrections are preserved.
[Fresh CAD, population BOMs and fabrication review](hardware/controller/review/M6-L1/README.md).
[Decision](docs/M6_L1_REVIEW_DECISION.md): **GO for independent five-bare-board
review and optional LoRa assembly preparation only.** No acceptance tag or
manufacturing release; physical qualification remains NOT_RUN.

A modular, cost-conscious, field-deployable transmitter platform for amateur radio direction finding (ARDF).

**Current 2 m CAD status — M5B-E4R1 source-joint candidate:** the [RF2M evaluation PCB](hardware/2m/README.md) retains standard **two-layer 1.6 mm / 1 oz FR4** and implements 16 intentionally open source vias, external ground vias and a documented stencil/reflow process. **GO for independent five-bare-board review only.** The conservative 110°C thermal target is missed; the 125°C physical qualification gate remains OPEN. See the [review decision](docs/M5B_E4R1_REVIEW_DECISION.md) and [review package](hardware/2m/review/M5B-E4R1/README.md). E4 HOLD evidence is preserved at `920da7b`; the last accepted CAD baseline remains `m5b-e3` / `95f189c`. No new acceptance tag. **Physical tests NOT_RUN. No upload, purchasing or manufacturing is authorized.** Earlier hardware milestones are retained below.

**Earlier 80 m status:** M1 architectural baseline conditionally accepted; M2/M3A research preserved. **M3B-E2 corrects the routed 80 m evaluation PCB for engineering review.** E1 is preserved at tag `m3b-e1`; its BD140 and TL431 pin/net errors are corrected, and its earlier manufacturing recommendation is withdrawn. ERC/DRC/connectivity checks pass; physical qualification remains OPEN. No component order, manufacturer upload, fabrication, assembly, energizing or production firmware has occurred. Proposed ADRs remain proposed.

**M4A, 2026-10-15:** the frozen **1245023 / m3b-e2** reference now has a
[self-contained five-bare-board prototype handoff](docs/M4A_E2_PROTOTYPE_HANDOFF.md).
A separate **150 × 110 mm** [RF80 V1 KiCad candidate](hardware/80m/production/README.md)
reduces board area **50.9%**, preserves both populations and all functional
components/connections, and retains 14 of 74 test pads. See the
[review decision](docs/M4A_REVIEW_DECISION.md), [layout](docs/M4A_COMPACT_LAYOUT.md),
[mechanical interface](docs/M4A_MECHANICAL_INTERFACE.md),
[variant BOM/costs](docs/M4A_VARIANT_BOM.md),
[electrical equivalence](docs/M4A_ELECTRICAL_EQUIVALENCE.md) and
[production test plan](docs/M4A_PRODUCTION_TEST_PLAN.md).
**PRODUCTION-INTENT — NOT RELEASED; all physical qualification remains NOT_RUN.**
Purchasing, fabrication, population, power-up and RF activation need distinct
explicit authorization; none has occurred.

**Power reassessment, 2026-10-14:** the user now requires **12 h full-power / 24 h competition-appropriate reduced-power** operation. The completed [2S/4S review](docs/M2_POWER_ARCHITECTURE_DECISION.md) proposes mode-dependent supplies and packs; [ADR-0011](docs/decisions/ADR-0011-dual-voltage-power-and-endurance.md) awaits review. Earlier 24 h maximum-power tables below and in M1/M2 remain historical calculations, not current pack recommendations.

**M3A, 2026-10-14:** [schematic project and PDF](hardware/80m/README.md), [review decision](docs/M3_80M_REVIEW_DECISION.md), [circuit explanation](docs/M3_80M_SCHEMATIC_REVIEW.md), [PA choice](docs/M3_80M_PA_SELECTION.md), [BOM](docs/M3_80M_BOM.md), [prototype gates](docs/M3_80M_TEST_PLAN.md) and [checks](docs/M3_80M_CHECKS.md). Selected IRF610 normal path targets approximately3 W full /1.2 W extended on4S; separate10 mW Fox path supports2S reduced population. 2 m remains genuine A2A,1 W carrierERP with required AM PEP.

**M3A-R1 correction:** [logic audit](docs/M3A_R1_LOGIC_AUDIT.md), [simplification](docs/M3A_R1_SIMPLIFICATION.md), [cost delta](docs/M3A_R1_COST_DELTA.md), [verification](docs/M3A_R1_VERIFICATION.md) and [review decision](docs/M3A_R1_REVIEW_DECISION.md). Physical timer polarity/startup/rearm defects are corrected; ERC and pin-derived digital checks pass. Driver-fault timing and all RF/thermal gates remain OPEN. R0 is preserved at Git tag `m3a-r0`.

**M3B, 2026-10-14:** [evaluation PCB and review files](hardware/80m/README.md), [review decision](docs/M3B_REVIEW_DECISION.md), [layout](docs/M3B_PCB_LAYOUT_REVIEW.md), [critical packages](docs/M3B_COMPONENT_QUALIFICATION.md), [bring-up](docs/M3B_BRINGUP_PLAN.md), [safety gates](docs/M3B_SAFETY_GATES.md), [evaluation BOM](docs/M3B_EVALUATION_BOM.md) and [reproducible checks](docs/M3B_CHECKS.md). Two layers,210×160 mm; R1 safety logic preserved. Recommendation: independent review, then explicit user approval for a small bare-board batch; no unrestricted RF/hardware release.

**M3B-E2, 2026-10-15:** [review decision](docs/M3B_E2_REVIEW_DECISION.md), [electrical corrections](docs/M3B_E2_CORRECTIONS.md), [manufacturer/footprint audit](docs/M3B_E2_FOOTPRINT_AUDIT.md), [DRC coverage](docs/M3B_E2_DRC_AUDIT.md), [bounded power gates](docs/M3B_E2_POWER_PROTECTION.md), [cost delta](docs/M3B_E2_COST_DELTA.md) and [new E2 package](hardware/80m/review/M3B-E2/README.md). Conditional bare-board review only; finished-hole capability, independent review and explicit manufacturing authorization remain pending.

## Planned configurations

- Control PCB + 80 m RF PCB: 80 m Classic, Sprint, Foxoring and beacon roles, with **different antenna installations** for full-size Classic/Sprint versus compact 30 cm-class Foxoring.
- Control PCB + 2 m RF PCB: 2 m Classic A2A and very-low-power training.
- All three PCBs: universal dual-band transmitter.
- Silicontra SX1262 LoRa daughter module is optional on the control PCB and detected at runtime.
- Retained protected external 2S1P–2S4P Li-ion packs; added 4S1P/4S2P architectures are proposed for review. Eight cells remain a maximum candidate, not a prerequisite; compact Foxoring stays 2S1P.

## Project principles

1. Cost and repeatable sourcing are primary design objectives.
2. Reuse measured, published RF designs where suitable. Research is not validation.
3. Local autonomous, deterministic contest operation must work with no LoRa hardware or network.
4. All inactive RF stages must be silent by hardware design (fail-safe TX inhibit).
5. Each PCB must be developable, replaceable, independently testable and accompanied by a test specification.
6. Compare itemized material baskets for six, ten and twenty identical boards against modified low-cost handheld radios; do not assume an original PCB is cheaper.
7. Do not confuse RF connector power, ERP, PEP, antenna efficiency, or field-strength requirements. A 10 mW 80 m Foxoring field transmitter with an approximately 30 cm vertical antenna is **not** a full-size 80 m wire antenna merely driven at low power; matching and 30 m/250 m reach must be validated separately.

## Start here

- [`docs/M2_POWER_ARCHITECTURE_DECISION.md`](docs/M2_POWER_ARCHITECTURE_DECISION.md) — current 2S/4S recommendation, costs, pack/profile limits and review gates.
- [`docs/M2_BATTERY_ARCHITECTURE.md`](docs/M2_BATTERY_ARCHITECTURE.md) — RF supply ratings, controller distribution, pack identity and charging protection.
- [`docs/M2_POWER_MODE_COMPARISON.md`](docs/M2_POWER_MODE_COMPARISON.md) — verified competition limits and full/reduced/continuous profiles.
- [`docs/M2_BATTERY_COST_COMPARISON.md`](docs/M2_BATTERY_COST_COMPARISON.md) — itemized battery/conversion and complete material at 6/10/20.
- [`docs/M2_ENDURANCE_REWORK.md`](docs/M2_ENDURANCE_REWORK.md) — reproducible load, early-cutoff and sensitivity calculations.
- [`docs/M2_POWER_ARCHITECTURE_SOURCES.md`](docs/M2_POWER_ARCHITECTURE_SOURCES.md) — dated primary evidence, prices and unresolved sourcing.
- [`docs/M2_POWER_ARCHITECTURE_CHECKS.md`](docs/M2_POWER_ARCHITECTURE_CHECKS.md) — calculation/documentation checks and separately dated source-access results.

- [`docs/M2_80M_DECISION.md`](docs/M2_80M_DECISION.md) — proposed proven RF core, near-1 W standard target, costs, endurance and review disposition.
- [`docs/M2_80M_REFERENCE_COMPARISON.md`](docs/M2_80M_REFERENCE_COMPARISON.md) — actual schematics/BOMs/layouts, source versions and evidence gaps.
- [`docs/M2_80M_RF_TOPOLOGY.md`](docs/M2_80M_RF_TOPOLOGY.md) — original circuit sheets and annotated connections, separate Foxoring branch and safety contract.
- [`docs/M2_80M_COST_COMPARISON.md`](docs/M2_80M_COST_COMPARISON.md) — itemized 6/10/20 comparison and preserved all-in accounting.
- [`docs/M2_80M_POWER_COMPARISON.md`](docs/M2_80M_POWER_COMPARISON.md) — 1/1.2/2/3/5 W profiles and continuous beacons.
- [`docs/M2_80M_VALIDATION_GATES.md`](docs/M2_80M_VALIDATION_GATES.md) — shared evaluation hardware and measurable H0–H9 gates, all NOT RUN.
- [`docs/M2_80M_CHECKS.md`](docs/M2_80M_CHECKS.md) — arithmetic, documentation and source-link verification.

- [`docs/FOXORING_COST_AUDIT.md`](docs/FOXORING_COST_AUDIT.md) — reconciles EUR29.06 to EUR77.11 without replacing the common controller/RF architecture.
- [`docs/FOXORING_COST_BOM.md`](docs/FOXORING_COST_BOM.md) — complete itemized Fox-only material and separate fleet charging/equipment budgets at 10/20.
- [`docs/M2_PREPARATION.md`](docs/M2_PREPARATION.md) — conditional acceptance, new RF findings, circuit proposals and go/no-go disposition.
- [`docs/M2_SYSTEM_COST.md`](docs/M2_SYSTEM_COST.md) — all-in material view including circuit increments, antenna networks, fabrication, wiring and every pack size.
- [`docs/M2_CHECKS.md`](docs/M2_CHECKS.md) — current consistency, simulation and link checks, with evidence limitations.

- [`docs/M1_DECISION.md`](docs/M1_DECISION.md) — M1 review summary, costs, endurance, unresolved gates and user decisions before M2.
- [`docs/M1_COST_REWORK.md`](docs/M1_COST_REWORK.md) — revised minimal architecture, budget feasibility, cost drivers and alternatives.
- [`docs/M1_COSTED_BOM.md`](docs/M1_COSTED_BOM.md) — itemized 6/10/20 quantities/prices, supplier codes, stock and estimates.
- [`docs/M1_COST_SOURCES.md`](docs/M1_COST_SOURCES.md) — dated cost-rework primary evidence and access limitations.
- [`docs/M1_REQUIREMENTS_TRACE.md`](docs/M1_REQUIREMENTS_TRACE.md) — directly checked 2025 rulebook matrix and all product requirement IDs.
- [`docs/M1_FEASIBILITY.md`](docs/M1_FEASIBILITY.md) — RF evidence matrix, AM/PEP and separate antenna analysis.
- [`docs/M1_SYSTEM_ARCHITECTURE.md`](docs/M1_SYSTEM_ARCHITECTURE.md) — local/shared synthesis comparison, interface and fail-off proposals.
- [`docs/M1_POWER_BUDGET.md`](docs/M1_POWER_BUDGET.md) — 1P–4P profiles, peaks, margins and continuous-beacon exceptions.
- [`docs/M1_BOM_CANDIDATES.md`](docs/M1_BOM_CANDIDATES.md) — attributed distributor observations and explicit unquoted allowances.
- [`docs/M1_REGULATORY.md`](docs/M1_REGULATORY.md) — competition versus country law; Germany provisional.
- [`docs/M1_RISK_REGISTER.md`](docs/M1_RISK_REGISTER.md) — scored risks and closure paths.
- [`docs/M1_VALIDATION_PLAN.md`](docs/M1_VALIDATION_PLAN.md) — measurable qualification, including compact Foxoring field tests.
- [`docs/M1_CHECKS.md`](docs/M1_CHECKS.md) — consistency/link/numeric check results and access limitations.

- [`docs/requirements.md`](docs/requirements.md) — requirements and source distinctions.
- [`docs/architecture.md`](docs/architecture.md) — current logical interfaces and unresolved decisions.
- [`docs/research-register.md`](docs/research-register.md) — primary sources and evidence gaps.
- [`docs/decisions/ADR-0001-modular-hardware.md`](docs/decisions/ADR-0001-modular-hardware.md) — accepted initial choices.
- [`docs/m1-acceptance.md`](docs/m1-acceptance.md) — M1 exit criteria.
- [`prompts/M1_CODEX_TASK.md`](prompts/M1_CODEX_TASK.md) — complete initial task for Codex.

**Preserved M1 baseline**, before new RF circuit/thermal increments: nominal combined PCB material: **€69.54 / 62.33 / 61.90 ex VAT at 6/10/20**, with substantial unquoted estimates. The VHF board still exceeds its €30 target with the currently sourced MMIC driver; a stocked-EOL discrete-driver comparison is preserved as history and excluded from new selection. These are optimization candidates, not proven prices. M2 preparation uses conservative VHF 4P pending measured bias/efficiency; the earlier M1 3P result is only a historical assumption. The revised preparation budget plans HF/VHF 4P, Sprint 2P and Foxoring 1P, with smaller-pack passes measurement-dependent; measured efficiency/idle/pack tests are pending. Full-power continuous HF/VHF/Sprint beacons and simultaneous dual Classic fail 24 h in the reference 4P model.

## License and external references

The M2 review includes read-only OpenARDF schematic-page renderings and BOM metadata with [upstream MIT notices](docs/assets/80m-reference/LICENSES.md). Original complete CAD/layouts and firmware remain temporary research downloads. M3A supplies a new electrical schematic derived from the attributed OpenARDF RF core/filter, with [design/library licence notices](hardware/80m/LICENSES.md). No original complete product board or firmware is republished as ARDF-TX. Other source artwork has not been redistributed. Inspect the exact license before copying software, footprints or drawings. SmartFOX firmware's MIT declaration does not establish licensing for external components or vendor datasheets.

## Safety and regulations

RF transmission must comply with applicable national regulations and permissions. IARU championship rules are competition requirements, not a substitute for legal compliance. Begin transmit testing into a rated 50-ohm dummy load with suitable RF measurement equipment; do not radiate unverified prototypes.
