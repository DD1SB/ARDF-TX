# Requirements baseline — reconciled at M1

Reconciled 2026-10-13 against the primary 2025 rulebook. Full [source/test trace](M1_REQUIREMENTS_TRACE.md), [conditional decision](M1_DECISION.md) and assumptions supersede initial unverified feasibility expectations. RULE means a competition requirement, not legal transmission authority or demonstrated hardware compliance.

Status labels: **LOCKED** = established project requirement; **RULE** = extracted from cited IARU Part B (2025); **TARGET** = design objective requiring feasibility; **OPEN** = must be decided by M1.

**Conditional acceptance 2026-10-13:** M1 architecture is accepted as the baseline for circuit/evaluation preparation. [M2 preparation](M2_PREPARATION.md) governs the added review requirements below. Complete layout/procurement and a full transmitter set remain gated; original numerical costs/energy are research inputs, not validation.

**User requirement change, 2026-10-14:** [power reassessment](M2_POWER_ARCHITECTURE_DECISION.md) evaluates protected 2S/4S packs and replaces the blanket 24 h maximum-power objective with **12 h at the highest selected normal setting and 24 h at a defined reduced competition-appropriate setting**. Continuous 10 mW Foxoring retains 24 h; continuous beacons remain separate. Original research and accepted ADR texts are preserved; [ADR-0011](decisions/ADR-0011-dual-voltage-power-and-endurance.md) is a **proposed implementation amendment**, not acceptance of a 4S circuit. The [dated trace supplement](M2_POWER_REQUIREMENTS_TRACE.md) records these changes explicitly.

## Modular product and modes

| ID | State | Requirement |
| --- | --- | --- |
| SYS-001 | LOCKED | Three primary, separately testable boards: ESP32 control, 80 m RF and 2 m RF. |
| SYS-002 | LOCKED | Any RF board may be omitted; one firmware supports all installed configurations. |
| SYS-003 | LOCKED | Silicontra SX1262 module optional; detect functionality robustly; no LoRa dependency for contests. |
| SYS-004 | LOCKED | Retain protected 2S1P–2S4P and evaluate added 4S1P/4S2P support; module capability, power setting and endurance may depend on pack class. Do not require full RF output from every combination. |
| SYS-005 | LOCKED | Eight cells remain the maximum candidate: retained 2S4P or proposed 4S2P universal configuration; neither mandatory. Prefer compact 2S1P Foxoring. Exact 4S implementation requires ADR review. |
| SYS-006 | LOCKED | Remote configuration/enable/disable and time synchronization are desired with LoRa installed; autonomous schedule continues if radio unavailable. |
| SYS-007 | LOCKED | Role, identification, timing, RF frequency and power state must be configurable. |
| SYS-008 | TARGET | USER 2026-10-14 supersedes the prior blanket target: at least 12 h at the highest selected normal RF setting, and 24 h at a defined reduced setting that still meets the applicable competition minimum. Preserve 24 h continuous 10 mW Foxoring; model continuous beacons separately at 100% duty. No measured endurance claimed. |
| SYS-009 | LOCKED | Favor cost, ease of sourcing and repeatability; compare batches of 6, 10 and 20 identical boards under the cost-rework request. |

## 80 m RF

| ID | State | Requirement |
| --- | --- | --- |
| RF80-001 | RULE | Classic carrier range 3.510–3.600 MHz; 1–5 W RF output, A1A; 8–15 WPM. IARU Part B §T2.6. |
| RF80-002 | RULE | Sprint uses 0.3–1 W output; two five-transmitter groups on different frequencies, with different WPM, simultaneous slots of 12 s each in a 60 s cycle. IARU Part B §S6.1–S6.4. |
| RF80-003 | RULE | Sprint finish and a **separate spectator transmitter, when needed**, operate continuously on frequencies distinct from the groups and each other. No spectator transmitter when its control coincides with finish (§S3.4); example 3.530/3.550/3.570/3.600 MHz frequencies are not mandatory. |
| RF80-004 | RULE | Foxoring **field** transmitters: 10 mW RF output, A1A, continuous operation, short vertical antenna approximately 30 cm. Foxoring **finish beacon**: 1–5 W RF output and a vertical antenna; do not apply field-transmitter antenna/power assumptions to the finish beacon. IARU Part B Appendix 6 §FT2.6. |
| RF80-005 | RULE | Foxoring signal must be audible at marked position and at 30 m from antenna but not audible at 250 m; terrain/antenna conditions matter; §F27.3. |
| RF80-006 | TARGET | Fully off (no radiation), low-power Foxoring, Sprint and Classic power ranges, plus optional calibration or fine adjustment that does not replace hard safety limits. |
| RF80-007 | TARGET | Frequency programmable without crystal or PCB change; retune before TX starts and prohibit unsafe on-air frequency hopping. |
| RF80-008 | LOCKED | Distinguish **two 80 m antenna installations**: Classic/Sprint uses a conventional longer vertical wire and a suitable ground/counterpoise (example field installation: approximately 8 m wire plus 6 m counterpoise); Foxoring uses a very short vertical radiator (IARU example approximately 30 cm) and a compact, defined counterpoise. The longer-wire system is **not** the Foxoring antenna. |
| RF80-009 | TARGET | Evaluate distinct matching/loading/coupling and shielding/grounding for the 80 m Classic/Sprint and Foxoring antenna configurations. Whether to switch internal matching paths, use external matching adapters, or use separate antenna connectors remains OPEN and must be decided from performance, size, protection, and BOM cost. |
| RF80-010 | TARGET | Verify **10 mW at the defined RF measurement/reference point** separately from radiated field performance of the installed Foxoring antenna. Document reference impedance and method, matching losses, environmental sensitivity, and a repeatable 30 m audible / 250 m not-audible field test. Neither 10 mW nor the 30 cm antenna alone guarantees the required reach. |
| RF80-011 | TARGET | Prevent or protect against applying the Classic/Sprint watt-range output to an attached compact Foxoring antenna/matching network. Any additional loading network or connector necessary for Foxoring must be included in the cost and size analysis (not silently excluded as an accessory). |

## 2 m RF

| ID | State | Requirement |
| --- | --- | --- |
| RF2-001 | RULE | Classic IARU carrier range 144.500–144.900 MHz, ERP 0.25–1 W, horizontally polarized antenna at 2–3 m, A2A, 70–80% AM modulation depth, 8–15 WPM; §T2.8. |
| RF2-002 | LOCKED | Separate very-low-power training RF output for areas approximately the size of a football field. Target range µW–mW is provisional and must be field-validated. |
| RF2-003 | LOCKED | True AM/A2A for 2 m Classic. An FM sidetone beacon is not a substitute. |
| RF2-004 | TARGET | Adjustable carrier/output with modest headroom, while meeting ERP and spectrum requirements with the intended antenna. PA sized for PEP; RF output ≠ ERP. |
| RF2-005 | TARGET | Normal power and training output electrically interlocked, filtered, protected and proof against unintended full-power routing to training connector. |
| RF2-006 | TARGET | Hardware RF mute/inhibit during startup, shutdown, fault and retuning; all RF boards silent when not scheduled. |
| RF2-007 | LOCKED | User-selectable 2 m carrier frequency across the applicable amateur band for permitted local/training use (e.g. 144–146 MHz in Region 1), with a separately enforced championship profile restricted to the IARU range; confirm lawful national allocations and band plan before operation. |

## Control, communications and safety

| ID | State | Requirement |
| --- | --- | --- |
| CTRL-001 | LOCKED | ESP32-class MCU with nonblocking, deterministic Morse/schedule timing and spare interfaces for optional SPI LoRa. |
| CTRL-002 | TARGET | 80 m KEY, 2 m A2A control, low/normal power selection; precise semantics/number of pins determined after RF-module design. |
| CTRL-003 | TARGET | Choose calibrated local timebase (RTC or TCXO) and unattended holdover; LoRa assists synchronization but is not a live timing dependency. |
| CTRL-004 | TARGET | LoRa optional auto-detection must not assume a nonexistent identification register; explicitly handle BUSY/DIO/timeout/absent module. |
| CTRL-005 | TARGET | Fail-safe hardware TX_EN gating independent of an ESP32 application task. Brownouts/boots/wiring faults cannot accidentally transmit. |
| CTRL-006 | TARGET | Config/data validation, firmware upgrade path, status and diagnostics, and deterministic restart behavior. |
| CTRL-007 | TARGET | RF board presence/fault identification without potentially energizing an unknown board; define polarity, default pull resistors and connector protection. |
| PWR-001 | TARGET | Evaluate controller operation at approximately 6.0–16.8 V, retained 2S and proposed 4S; all raw-input devices, startup/transients and pack-dependent RF capabilities require qualification. |
| PWR-002 | TARGET | External 2S/4S packs require proper individual-cell protection/balancing and mechanically incompatible 8.4/16.8 V charging interfaces, with cell-specific charge/discharge limits. |
| PWR-003 | TARGET | Validate all six proposed pack geometries, peak/weakest-cell currents, thermal limits, conversion/idle/LoRa losses and 12/24 h RF performance; modeled runtime is not validation. |
| PWR-004 | TARGET | Independently verify pack identity, voltage and module capability; missing/incorrect ID, undervoltage or unsafe supply configuration defaults RF off. Do not infer weakest-cell voltage from pack sum alone. |
| PWR-005 | TARGET | Compare equal-cell-count 2S/4S cost and energy, including converters, magnetics, cooling, BMS/balance, wiring/keying and shared charging at 6/10/20. |
| PWR-006 | TARGET | Retain measured-reference versus calculated assumptions; quantify PA efficiency versus setting, early RF cutoff energy, aging/temperature/controller-idle/LoRa sensitivity. |
| PWR-007 | LOCKED | A reduced competition profile must retain the relevant conducted-power/ERP minimum and all modulation/timing/antenna requirements. Select fixed event parameters; undervoltage latches off rather than silently changing coverage. |
| PWR-008 | LOCKED | Reassessment ends at documented comparison/proposed ADR review. No layout, Gerbers, procurement, fabrication or production firmware authorized. |
| TEST-001 | RULE | Suppress RF emission outside scheduled TX windows; IARU Part B §T2.4; satisfy applicable local radio rules. |
| TEST-002 | TARGET | Design-for-test: RF test pads/50 Ω ports, power/sense points, repeatable calibrated test procedure; require measured output, envelope, unwanted products and endurance before declaring the RF validated. |

## Costs (challenge targets, not verified quotes)

The user's cost rework replaces the original stretch targets. The [revised M1 analysis](M1_COST_REWORK.md) and [itemized candidate BOM](M1_COSTED_BOM.md) preserve the baseline; earlier EUR 92–146 envelopes are historical. Baseline combined PCB material is **EUR 69.54 / 62.33 / 61.90 ex VAT at 6/10/20**. The [M2 all-in view](M2_SYSTEM_COST.md) adds proposed drive, shaping, filter and thermal material; current nominal universal PCB components are **EUR 77.46 / 72.13 / 71.36**. Unknown prices and RF qualification prevent a proven cost claim. Conditional architectural acceptance satisfies COST-007's review prerequisite, while PREP-001–008 retain circuit/layout/procurement gates.

| Variant (PCB material excluding bare PCB fabrication, batteries, enclosure, antennas and wiring) | Revised optimization target |
| --- | --- |
| Control electronics (LoRa cost quoted separately) | EUR 8–15 |
| Complete 80 m RF board | EUR 10–20 |
| Complete 2 m AM RF board | EUR 15–30 |
| Combined base electronics | EUR 33–65 |

M1 must generate a BOM with manufacturer part numbers, footprints, distributors, stock status, minimum-order quantities, non-reel pricing, substitution policy and date. Reject unrealistic 3,000-piece MOQ components or hidden module costs. Stretch targets are **not** proof of achievable pricing.

| ID | State | Cost-rework requirement |
| --- | --- | --- |
| COST-001 | TARGET | Controller EUR 8–15, complete HF EUR 10–20, complete VHF EUR 15–30 and combined EUR 33–65 material targets; state tax/scope and uncertainty. |
| COST-002 | LOCKED | Compare realistic identical-board batches of 6, 10 and 20, correct aggregated quantities/customer MOQ, available cut tape/tube and no invented breaks or reel assumptions. |
| COST-003 | LOCKED | Reconsider architecture using tested minimal discrete RF precedents including G3ZOI, DL3BBX, ON7YD and relevant Si5351 designs. |
| COST-004 | LOCKED | Identify all material cost drivers, quantify lower-cost alternatives, distinguish essential/optional functions and economical reduced populations. |
| COST-005 | LOCKED | Preserve three primary PCBs, optional LoRa and required RF modulation/power/frequency/antenna/timing/endurance/safety; do not silently derate to meet cost. |
| COST-006 | TARGET | Full itemized candidate BOM with supplier order codes, batch quantities, prices, availability and explicit estimates/unknowns. Exact RF values/connector footprints remain proposals pending electrical design. |
| COST-007 | LOCKED | Keep M2 design/implementation on hold until the revised architecture has been reviewed; no routing/Gerbers/orders/production BOM or validation claim in M1. |

## Conditional-review preparation requirements

| ID | State | Requirement |
| --- | --- | --- |
| PREP-001 | TARGET | Re-evaluate the complete144 MHz drive/PA chain, compression margin, matching and carrier/PEP under supply AM before complete layout/procurement. |
| PREP-002 | TARGET | Analyze BD140 thermal/DC SOA over the whole envelope and carrier-only intervals; propose a credible qualified alternative if needed. |
| PREP-003 | LOCKED | Prefer MMIC drive and currently manufactured alternatives; do not select discontinuedBFP650 for minor savings. |
| PREP-004 | TARGET | Reviewable IRF610 watt and independent10 mW circuits with separate long/compact matching and physically distinct installations. |
| PREP-005 | LOCKED | Define minimum reusable RF evaluation hardware/instruments and measured gates before committing complete system PCB. |
| PREP-006 | LOCKED | Preserve autonomous local hardware fail-off, persistent interlocks and physical/electrical protection of low-power ports against watt RF. |
| PREP-007 | LOCKED | Maintain all-in system material cost besidePCB BOM, including connectors/wiring, antenna networks, bare fabrication and all1P–4P packs. |
| PREP-008 | LOCKED | Explicit RF-module go/no-go and measurements simulation cannot replace; no fullset manufacture/order; distinguish calculations/simulation/measurement. |

## Foxoring-only cost audit requirements

The [Foxoring cost audit](FOXORING_COST_AUDIT.md) preserves the accepted architecture and adds these accounting requirements; its itemized BOM remains a candidate.

| ID | State | Foxoring audit requirement |
| --- | --- | --- |
| FOX-001 | LOCKED | Preserve ESP32-S3 controller, RTC and optional unpopulated Silicontra footprint contract. |
| FOX-002 | LOCKED | Preserve the common 80 m PCB with its existing Foxoring-only component population; no smaller replacement board or MCU platform. |
| FOX-003 | LOCKED | Use a protected balanced external 2S1P pack with two new standard 18650 cells and qualified charging. |
| FOX-004 | TARGET | Reconcile the EUR29.06 baseline to EUR77.11 and itemize all cells/BMS/charging/connectors/fabrication/case/mechanics/assembly material. |
| FOX-005 | LOCKED | Separate observed price candidates, unquoted allowances, unspent reserves, shared equipment, one-time costs and labor; no claim that anything was purchased. |
| FOX-006 | TARGET | Optimize batches of ten/twenty Foxoring units using realistic demand, customer MOQ, same-MPN aggregation and explicit fleet logistics. |
| FOX-007 | TARGET | Compare TinyFox/Fixle cost, scope and evidence without replacing the common ARDF-TX architecture or inventing current quotes. |
| FOX-008 | LOCKED | Preserve nominal10 mW A1A, compact matching/approximately30 cm radiator/defined return, 30/250 m field criteria, autonomous fail-off and accurate timing; no fourth transmitter PCB. |

## Additional primary-rule constraints verified at M1

| ID | State | Requirement / primary location |
| --- | --- | --- |
| RULE-001 | RULE | Frequency stability better than 50 ppm on both bands and Foxoring; T2.6/T2.8/FT2.6. |
| RULE-002 | RULE | Simultaneous 80 m normal channels ≥20 kHz apart; VHF channels **more than** 200 kHz apart; Foxoring finish-to-field ≥30 kHz. FT2.6 does not set a new field-to-field separation. |
| RULE-003 | RULE | Applicable uniform transmitter parameters/antenna installations and omnidirectional horizontal pattern (T2.2/T2.5); no antenna change during contest (27.2); symmetric Sprint grounding (S6.6). One illustrative 6 m return wire cannot be assumed Sprint compliant. |
| RULE-004 | RULE | Transmitting-period deviation and overlap ≤5 s relative to official time (T3.3); start/finish clocks ≤1 s (T3.2). Tighter project Sprint target is separate. |
| RULE-005 | RULE | Applicable start audibility, organiser monitoring/recording, operation duration and identification windows (27.3–27.6), ancillary equipment no audible receiver interference (T4.1). Foxoring field reach replaces general start audibility for those field units. |
| RULE-006 | RULE | Different neighbouring Foxoring field frequencies recommended, not compulsory (FT2.9). |

The approximately 30 cm radiator is rule-derived; compact counterpoise geometry, 50 Ω power reference/tolerance, exact ERP carrier/mean convention and audibility-test receiver protocol remain engineering/referee inputs. Proposed electrical interfaces/footprints and modelled currents are not locked requirements or measured facts.

## Source boundaries and regulatory caveat

IARU Region 1 Part B (2025) is a championship rulebook, not a radio transmitter authorization. All country-specific band, emissions, station identification, and operator regulations require separate review before radiating.

Official rules: https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf

