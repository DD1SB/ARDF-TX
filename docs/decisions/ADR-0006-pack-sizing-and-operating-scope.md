# ADR-0006 — Pack sizing and operating scope

Status: **Pack compatibility conditionally accepted via ADR-0007; measured sizing and operating scope remain Proposed**  
Date: 2026-10-13

**Dated requirement supersession, 2026-10-14:** the user replaces the former blanket 24 h maximum-power target with 12 h full / 24 h sufficient reduced output. The original text below remains history. [ADR-0011](ADR-0011-dual-voltage-power-and-endurance.md) proposes adding 4S and revised pack/supply implementation; it is **not accepted** by this annotation.

## Context

User accepts interchangeable protected 2S1P–2S4P, with 4P maximum, and 24 h normal contest/Foxoring targets. [Power budget](../M1_POWER_BUDGET.md) explicitly models standby, real A2A and continuous roles. Actual currents/capacity/efficiency remain assumptions.

## Current preparation recommendation

The [M2 power budget](../M2_POWER_BUDGET.md) includes shaping/helper losses and supersedes the historical runtime assumptions below. Current conservative normal-profile allowances are **Classic HF 4P (27.7 h), Sprint 2P (47.1 h), Foxoring 1P (45.3 h), VHF 4P (27.1 h)**. These are calculations, not measured passes. Sprint 1P is about 23.6 h; VHF 3P about 20.3 h with the bias allowance. Poorer VHF efficiency can fail even 4P. Continuous maximum HF/VHF beacons give about 5.8/5.7 h on 4P; continuous Sprint about 22.3 h and dual Classic about 14.1 h. Preserve 1P–4P compatibility and qualify actual pack/charger/current before purchase.

## Historical M1 proposal — retained for provenance

For the reference 3.4 Ah/cell and 64.8% usable-energy model, recommend: Classic HF 5 W/20% **4P**; Sprint 1 W/20% **1P** subject to idle margin; Foxoring continuous 10 mW **1P**; VHF 1 W carrier ERP/20% **3P**. All smaller packs remain electrically supported subject to actual current and reduced runtime; no firmware assertion that every pack delivers 24 h.

Default normal operation has one active RF band even in universal hardware. The cost-rework overhead model gives simultaneous full-power dual Classic ~17.7 h on 4P; it is an optional scope decision, not a 24 h promise. Continuous HF/VHF beacons give ~6.1/~9.0 h on 4P; Sprint continuous 1 W gives ~25.9 h. Establish event-specific beacon duration/external supply policy. No increase beyond 4P proposed.

Use externally assembled protected/balanced packs with proper external 2S charger; no integrated charging in first controller candidate. Operational voltage/cutoff/current and pack ID/reporting follow exact pack selection.

## Alternatives / gates

Larger pack conflicts with accepted maximum; lowering maximum RF changes target scope; improved efficiency/idle may allow smaller packs but requires measurement. Full-power beacon 24 h would require different supply/service plan. VPWR/VTHERM must close measured mean-power ceilings, peak current and cold/aging capacity. User decides simultaneous-TX/endurance scope, required beacon duration, pack/cell supplier and charger preference before the relevant integration/release gates. No pack purchase/release implied.
