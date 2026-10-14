# ADR-0007 — Cost-optimized control and RF topology

Status: **Conditionally accepted — architectural baseline only; detailed RF/layout/procurement gates remain open.**  
Date: 2026-10-13

**Pending power amendment, 2026-10-14:** [ADR-0011](ADR-0011-dual-voltage-power-and-endurance.md) proposes a dual-voltage controller and mode-specific 2S/4S RF supplies under the user's revised endurance target. Conditional acceptance and the original text below remain intact; no 4S implementation is accepted by this annotation.

**Pending HF amendment:** [ADR-0010](ADR-0010-proven-80m-core-and-power-target.md) proposes the proven SignalSlinger/FlexFox80 core, near-1 W normal target and separately costed higher-power population. This ADR's conditional acceptance and original proposal remain intact pending review; its VHF architecture is unchanged.

## Context

The revised optimization targets are controller €8–15, HF €10–20, VHF €15–30 and combined €33–65 for batches of 6, 10 and 20. Preserve three primary PCBs, optional LoRa and all RF, timing, antenna and safety requirements. The [cost rework](../M1_COST_REWORK.md) and [itemized materials](../M1_COSTED_BOM.md) replace the earlier candidate architecture and broad allowances. Target costs remain unproven.

## User review record

The user conditionally accepted the three-PCB/local-synthesis/optional-LoRa/protected-pack/separate-low-path architecture on 2026-10-13 and authorized M2 circuit/evaluation preparation. MMIC drive is preferred; discontinued BFP650 is not selected. Historical cost comparisons below remain evidence only. Detailed RF circuitry and evaluation choices are proposed in [ADR-0008](ADR-0008-rf-evaluation-gates.md).

## Proposal

Use one ESP32-S3 controller, a compensated RTC, regulated and protected power, and wired provisioning. Control the two local RF sources directly on independent buses. Remove RF processors, DACs and precision digital meters; retain passive identity, manual calibration and basic analog monitoring. EEPROM, RTC backup, USB socket/ESD and pack-current logging are optional populations.

HF: compare the ON7YD single-IRF610 shaped class-C reference with QCX class-E, using a Si5351 programmable source, adequate 15–16 V boost and a separately bounded 10 mW Foxoring path. Include the dedicated loading/coupling cartridge, short radiator and compact counterpoise. Use the RNWR cut-tape converter offer in the cost model.

VHF: evaluate Si5351 first, with a filtered driver, available PD55008 discrete final and true sine supply AM. Evaluate ADF4002 with a discrete VCO as the lower-cost fallback before LMX2571. All source, AM and PEP acceptance criteria remain.

Use an inexpensive local monostable, persistent latch, POR and gates with analog trips. Retain independent source/PA shutdown, source-bus isolation, retune mute, a bounded training AM branch and physically distinct antenna ports. Strain-relieved RF pigtails terminate at incompatible bulkhead sockets. Detachable raw-power plugs and RF sockets are itemized in wiring; logic PCB sockets are included in board costs. Connector footprints remain open. No fourth primary PCB is proposed.

## Alternatives and consequences

Shared controller synthesis saves about €1.79 gross source/reference material, but adds estimated €0.8–2 board hardware and €0.5–2 coax wiring, plus controller and test dependencies. Local sources remain preferred for research. Each RF board is independently testable with a host fixture.

The currently sourced MMIC driver gives combined PCB estimates of **€69.54 / 62.33 / 61.90** for 6/10/20; VHF alone costs **€36.38 / 31.80 / 31.73**, above its ceiling. A stocked discontinued BFP650 discrete-driver alternative gives VHF **€33.90 / 29.32 / 29.18** and combined **€67.07 / 59.86 / 59.36**, but requires an explicit finite-batch/spares policy and RF qualification. A future current-production discrete replacement remains unresolved. Many supporting rows are estimates, so neither route establishes all budgets.

Mandatory power/RF connector material adds **€5.20 estimated** per universal unit under the wiring exclusion, before cables, crimps and strain relief. Antenna networks are separately itemized. Moving these parts outside board scope does not eliminate their cost.

Manual calibration and shared fixtures reduce material cost but add calibration labor and record discipline. Without RTC backup, cold pack changes require resynchronization. Cheap logic must pass the same fail-off tests, including startup, tolerances, latching and backfeed. Thermal, spectral or antenna results may require revised costs.

## Required review and closure

Direct control/local synthesis and protected low paths are conditionally accepted. Driver policy requires current manufacture; BFP650 is excluded. Detailed circuits, exact stock/quotes, VAT/wiring scope and performance-driven costs remain open.

Resolve quotes/stock, all-channel spurs, HF 5 W/clicks/efficiency, VHF AM/PEP/drive/thermal behavior, separate HF matching and field reach, low-port isolation, fail-off/retune, timing, endurance and LoRa immunity.

This ADR revises the proposals in ADR-0003 and ADR-0005 while preserving accepted ADR-0001/0002 and the protected-path/pack requirements in ADR-0004/0006. It does not accept a production BOM or authorize complete layout, full-set fabrication/purchases, production firmware or radiation. Circuit/evaluation preparation is authorized by the user review.
