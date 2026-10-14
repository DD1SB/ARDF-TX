# ADR-0008 — RF evaluation gates before complete layout

Status: **Proposed; detailed circuit choices require review and measured evidence.**  
Date: 2026-10-13

## Context

The user conditionally accepted M1's modular architecture and requested M2 preparation. Preserve local synthesis, optional LoRa, independent RF testing, 2S1P–4P and bounded low-power antenna paths. RF performance, reproducibility and maintenance take precedence over arbitrary silicon-cost ceilings. Do not select discontinued BFP650 to save roughly €2.

## Proposal

Evaluate the MMIC-driven PD55008 chain before complete VHF layout. GVA-84+ remains the first coupon candidate, conditional on measured compression/gain/loss. PHA is a current MMIC comparator if margin fails. Matching must address near-band conditional stability and changing drain voltage, not assume the 500 MHz gain number.

Replace the 12.6 V-limited TPS61088 with a 20 V TPS611781 candidate for the proposed 13.5 V VHF rail; verify converter ripple, transient/current behavior and efficiency. Same-MPN HF/VHF purchases pool in the updated cost view. Neither footprint nor compensation is released.

Reject free-air BD140 operation for the calculated thermal case. Evaluate heat-sunk D45H11, bounded base helper, voltage feedback/current trips and small modulated-node capacitance. TIP42C remains a lower-cost comparator requiring exact-vendor DC SOA evidence. No pass-device selection is released from a power-dissipation headline.

Develop HF with the single-IRF610 mechanism, protected AC gate drive, bounded shaped supply, an evaluated seven-pole filter and independent 10 mW source. Keep separate long-wire and compact loading/coupling networks. No routing of watt RF into compact/training ports.

Use reusable source/driver, PA, modulator/load, HF/low-path and safety fixtures; replicate key results on three samples after initial gates. Maintain all-in material costs and selected-pack power ceilings. Complete layout/procurement requires the relevant measured G0–G8 gates; G9/field/final-integration evidence remains required for product release.

## Consequences and evidence

Drive and thermal calculations show risks that M1 did not close. Safe shaping, filters and thermal material can increase nominal PCB material. The all-in view retains these costs and pack/antenna/fabrication/wiring scopes rather than forcing old targets. Conservative VHF evaluation uses 4P; 3P needs a measured low-bias/power pass, and poor efficiency fails even 4P. HF uses 4P, Sprint provisionally 2P, Foxoring 1P; all remain modeled allowances.

Only ideal passive LPF simulation has run. No transistor/supply-AM/field/thermal/battery hardware was measured, purchased or manufactured. Exact values, footprints, current/SOA/loop limits and sourcing remain open.

See [preparation review](../M2_PREPARATION.md), [VHF analysis](../M2_VHF_RF_REVIEW.md), [HF circuits](../M2_HF_CIRCUIT_PROPOSALS.md), [evaluation gates](../M2_RF_EVALUATION.md) and [all-in costs](../M2_SYSTEM_COST.md). This proposal does not authorize a full transmitter set or declare any gate passed.
