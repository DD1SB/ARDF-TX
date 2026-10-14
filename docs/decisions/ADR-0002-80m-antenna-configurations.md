# ADR-0002 — Distinct 80 m antenna configurations

Status: **Requirement accepted; implementation OPEN**  
Date: 2026-10-13

## Context

The modular 80 m board must serve Classic, Sprint, and Foxoring. The user identified an important system distinction: Classic/Sprint can use a long vertical wire and counterpoise (illustrative field example: 8 m radiator and 6 m ground wire), whereas Foxoring field transmitters use much smaller antennas. IARU Region 1 Part B (2025), Appendix 6 §FT2.6 specifies approximately 30 cm vertical antennas and 10 mW RF output for Foxoring field transmitters, separate from the 1–5 W finish beacon. §F27.3 requires the field transmitters to be audible at the mapped location and at 30 m but not audible at 250 m. This constrains the *installed antenna system*, not just the PA dial setting.

Primary rule source: https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf

## Decision already accepted

- Two physical antenna installations are supported by one 80 m RF PCB: longer-wire Classic/Sprint and compact shortened-vertical Foxoring.
- Conducted RF power and actual field audibility are **separate** verification requirements.
- Antenna loading/matching/coupling and necessary connectors, counterpoise, protection and mechanics are in scope for both cost and qualification.
- 2S1P compact Foxoring configurations should not require the normal long-wire antenna setup.

## M1 decision outstanding

Compare: (a) single connector with purpose-built passive matching adapters, (b) switched on-board matching, (c) separate antenna connectors/paths. For each, document practical installation, attenuation and PA efficiency, radiation/ground coupling, environmental sensitivity, current/voltage stress, full-power misconnection risks, field evaluation, cost and repairability. Do not assume 50-ohm resistive antenna behavior for an approximately 30 cm radiator at 3.5 MHz.

Do not release a chosen circuit or claim range compliance without measured verification.

## M1 follow-up (2026-10-13)

[Feasibility](../M1_FEASIBILITY.md) compares adapter, onboard switching and independent source/port paths with compact counterpoise/loading/cost. [ADR-0004](ADR-0004-protected-low-power-antenna-paths.md) proposes separate bounded paths and a compact cartridge. It remains Proposed; the accepted physical-antenna distinction does not validate range or approve matching values.
