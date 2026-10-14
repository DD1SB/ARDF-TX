# ADR-0009 — Foxoring fleet cost scope and shared charging

Status: **Proposed; accounting corrected, procurement/circuit choices not released.**  
Date: 2026-10-13

## Context

The user rejects an unexplained €77.11 Foxoring estimate and requires preservation of ESP32-S3/RTC, optional unpopulated Silicontra footprint, the existing 80m board's Fox-only population and a protected two-18650 2S1P pack. M1's €29.06 ten-unit material baseline includes the compact antenna but excludes fabrication, external pack, outer case and transmitter harness.

## Proposal

Maintain separate cost scopes: per-unit materials/functional provisions, protected-pack material, shared charging/provisioning equipment, fleet freight, unspent qualification reserves, labor and workshop/instrument capital. Preserve original M1/M2 figures as historical scopes; the audit closes the €48.05 difference without a new RF electronics premium.

Propose new regular-listing 25R cells with priced supplier tabs, and a separately qualified external protection/balancing candidate with a €3 protection budget retained. Check 24h Foxoring with the new capacity explicitly. Retain compact matching and existing safety/timing. No fourth transmitter board or replacement MCU.

Use one independently qualified external charger and keyed adapter per ten packs as the economical fleet proposal. Show individual-charger pricing and serial-charge turnaround. More chargers or a specified overnight turnaround changes equipment allocation; packs are never paralleled to avoid this cost. Exact BMS/charger stock, function, trip/termination and mechanical qualification remain open.

## Consequences and gates

Ten/twenty-unit material budgets are about €55.24/€55.20; conservative fleet cash allocations €63.34/€60.05 net, before labor/instruments/spares/VAT. These mix observed prices and estimates; no ordering release or price ceiling is implied. Candidate lowest-priced protection circuit requires exact-lot qualification; documented substitutes may increase its budget. Shared charging reduces purchased equipment count while requiring longer preparation.

See [cost audit](../FOXORING_COST_AUDIT.md), [itemized bill](../FOXORING_COST_BOM.md), [sources](../FOXORING_COST_SOURCES.md) and existing [RF gates](../M2_RF_EVALUATION.md). Source/low-path/field/pack/timing gates remain unpassed. Complete PCB design, manufacture, purchases and a full transmitter set remain outside this audit.
