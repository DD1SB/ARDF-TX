# M1 conditional acceptance and M2 preparation review

Date: **2026-10-13**. **M1 architectural baseline conditionally accepted by the user.** Authorized next work is RF analysis, reviewable circuit proposals and evaluation preparation. Complete system/module layout, procurement and a full transmitter set are **not released**. No hardware was built, ordered or measured in this preparation.

Preserve the three primary PCBs, optional exact Silicontra SX1262 module, local synthesis, independently testable RF boards, protected external 2S1P–2S4P packs, autonomous timing/fail-off and separate physically protected low-power outputs. All original RF, frequency, timing and antenna requirements remain. MMIC drive is preferred; discontinued BFP650 is **not selected**.

## Findings for review

1. **GVA-84+ adequacy remains open.** With 0.5 dB coupling and 0.5 dB output-filter loss, the 15–17 dB intrinsic PA-gain assumptions need 129–204 mW at the driver, above nearby typical P1dB. A 3 dB driver backoff requires about 20.38 dB intrinsic large-signal gain under the conservative power convention. PD55008 near-band small-signal data gives conditional stability, so matching cannot be assumed to recover that gain safely. Measure the chain; stronger current MMICs are available comparators.
2. **The boost/modulator combination requires changes.** TPS61088's 12.6 V output limit cannot supply the proposed 13.5 V rail; propose the cataloged 20 V TPS611781 with separately reviewed feedback/current limits. **BD140 free-air operation is rejected.** Calculated dissipation reaches4.24 W for carrier/no tone and 5.16 W in an efficiency stress case. Propose heat-sunk D45H11 plus a bounded base-current helper; exact hot-case DC SOA and measured envelope/thermal behavior remain gates. Large modulated-node capacitors can require active sinking.
3. **HF proposals now specify original functional connections and starting values.** IRF610 gate AC protection, shaped isolated supply, seven-pole filter, separate low buffer/pad/current/RF-level limits, and two independent antenna networks are reviewable. The compact antenna remains~30 cm with its own counterpoise/loading/coupling, never a reduced-power Classic installation.
4. **Only passive filter simulation has run.** Ngspice-42 compared ideal fifth/seventh-order filters. There is no nonlinear transistor, thermal or antenna simulation, and no measured RF result. Calculation artifacts retain all assumptions.
5. **Costs and endurance are reopened where circuit physics requires it.** The all-in material view includes additional pass/drive/filter/thermal material, mandatory wiring/connectors, bare-board fabrication, enclosure, complete antenna systems and every pack size. A conservative VHF 4P allowance replaces the unconditional use of the earlier 3P estimate during evaluation; it remains conditional on actual current/efficiency.

## Reviewable deliverables

- [144 MHz chain and modulator review](M2_VHF_RF_REVIEW.md): drive/gain/loss/compression calculation, small-signal stability/matching limits, full-envelope/no-tone thermal/SOA trajectory, alternative devices and revised energy sensitivity.
- [80 m circuit proposals](M2_HF_CIRCUIT_PROPOSALS.md): original functional circuits, component/value starting points, two output paths and separate long/compact matches, protection and filter simulation boundaries.
- [Minimum RF evaluation and go/no-go gates](M2_RF_EVALUATION.md): reusable fixtures, instrument methods, sequenced acceptance and measurements simulation cannot replace.
- [All-in system material cost](M2_SYSTEM_COST.md): 48 configuration/batch/pack baskets beside unchanged M1 component costs, estimates and exclusions.
- [Revised power budget](M2_POWER_BUDGET.md): shaping/helper/low-path overhead, all packs/profiles and stress cases; no measured runtime.
- [Dated source/evidence log](M2_SOURCES.md): primary documentation, actual simulation outputs, indexed prices and failed access.
- [RF calculations](M2_RF_CALCULATIONS.json), [cost calculations](M2_SYSTEM_COST.json), [original simulation deck](../analysis/hf_lpf_ideal.cir) and [actual simulated samples](../analysis/hf_lpf_ideal.csv).
- [ADR-0008](decisions/ADR-0008-rf-evaluation-gates.md): proposed detailed RF evaluation choices. ADR-0007 now records conditional architectural acceptance; detailed circuits remain proposals.

## Requirement-to-source/test trace for this review

| ID | User requirement / state | Response and evidence | Measured gate |
| --- | --- | --- | --- |
| PREP-001 | Re-evaluate144 MHz chain and supply-AM power/PEP / TARGET | PREP-GVA/PA/BOOST data; VHF reference planes, gain/backoff table, stability and voltage-dependent match analysis | G1–G3/G8 |
| PREP-002 | BD140 envelope thermal/SOA and credible alternative / TARGET | PREP-BD/D45/TIP; complete sampled envelope, no-tone/low-power/capacitance cases, exact-vendor SOA closure and D45H11 proposal | G4/G0 |
| PREP-003 | Prefer MMIC; reject discontinuedBFP650 savings / LOCKED | GVA first coupon, PHA current-source comparator, current small-signal BJT investigation and excluded lifecycle table | G2, fresh sourcing |
| PREP-004 | Reviewable IRF610 and independent 10 mW/matching proposals / TARGET | HF-W1/HF-L1/A80-L/A80-F; PREP-HF/GATE; original ideal LPF simulation and calculated antenna examples | G5–G7/G8 |
| PREP-005 | Minimum RF evaluation before fullPCB / LOCKED | E0–E5 fixtures/instruments and staged sample replication; no fleet build | G0–G8 before complete layout |
| PREP-006 | Autonomous hardware fail-off/testable low-power interlocks / LOCKED | Persistent local latch/lease/POR, source+PA shutdown, bounded low rails, no watt RF routing, hardware cartridge inhibit | G0/G6/G8 |
| PREP-007 | All-in cost besidePCB BOM including connectors/matches/fab/packs / LOCKED | M1 catalog preserved; 48 material baskets, same-MPN deltas/packing, full accessory/pack scopes and explicit estimates | Fresh comparable baskets, G9 |
| PREP-008 | Module go/no-go and irreplaceable measurements; no fullset / LOCKED | G0–G9 matrix, seven measurement categories; no measured passes or fullset orders | Documented bench reports and review |

Evidence words have strict meanings: **DATASHEET/PUBLISHED** describe the source's conditions; **CALCULATION** is our model; **SIMULATION** here is the actually run ideal passive network; **MEASURED** would require project hardware and recorded instruments. No MEASURED project entry exists.

Current conservative normal-profile allowances are **HF 4P, Sprint 2P, Foxoring 1P and VHF 4P**. Sprint 1P and VHF 3P require actual efficiency/current closure. Low-bias VHF can fit 3P in the model; its poor-efficiency case fails even 4P. No pack runtime is guaranteed.

## Current disposition and next review

**Go:** continue circuit review and design the minimum evaluation fixtures under this preparation scope. **No-go:** commit the complete module/system layout, buy/manufacture a full transmitter set or declare hardware validated. RF coupons themselves need a reviewed electrical/ground/thermal implementation before later fabrication or parts commitment; no files or orders are generated here.

Architectural acceptance does not settle exact PA matching, driver gain, pass-device compensation, cutoff/current thresholds, connector footprints or stock. Required next evidence is driver/PA compression/gain, actual AM/PEP and modulator heat/SOA, HF clean5 W/keying/filter/efficiency, low-path isolation and hardware startup/fault/retune behavior. Compact field, installedERP, pack/timing/LoRa/fleet gates precede product release. Full system costs must be recalculated from the circuit that passes.

User inputs still open: operating country/legal mask, referee ERP/Foxoring reference/audibility conventions, exact Silicontra MPN, selected protected pack/cell/charger and desired continuous-beacon duration. Their absence does not prevent dummy-load circuit/evaluation preparation; it does prevent a final legal/radiated qualification claim.
