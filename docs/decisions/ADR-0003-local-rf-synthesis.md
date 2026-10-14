# ADR-0003 — Local synthesis on each RF board

Status: **Conditionally accepted at architecture level via ADR-0007; detailed electrical implementation remains Proposed**
Date: 2026-10-13

## Context and evidence

ADR-0001 accepts three independently testable boards but leaves synthesis placement open. [M1 architecture](../M1_SYSTEM_ARCHITECTURE.md) compares total cost, harness/return/shielding, variants, spurs and independent tests. [RA3APW spectra](http://www.ra3apw.ru/proekty/si5351-spectrum/) show VHF Si5351 spectral risks; [TI reference measurements](https://www.ti.com/lit/pdf/TIDUC19) support a PLL alternative at 480 MHz, not validation at 144 MHz.

## Proposal

Keep 3.5/144 MHz synthesis local to each RF PCB. The [cost-rework proposal](ADR-0007-cost-optimized-m1.md) evaluates Si5351 on VHF first, then ADF4002/discrete VCO before LMX2571 if spectra fail. Retain Si5351 on HF. Direct controller configuration replaces local MCU bridges; independent tests use a host fixture. No 144 MHz on a general-purpose digital harness. Exact source/reference/footprint remain open.

## Alternatives

Revised shared-Si comparison saves about €1.79 source/reference gross but adds estimated €0.8–2 board hardware and €0.5–2 coax wiring plus test dependency. The previous unquoted €4–10 interconnect penalty is withdrawn as a decisive argument. Shared HF source or reference still needs noise/variant/test evaluation; excluded wiring is not free.

## Consequences and gates

More duplicated small references/quiet rails, easier module omission/replacement/test isolation and band-specific filtering. Output LPF is insufficient for close-in spurs. User acceptance chooses placement only; V80P/V2AM/VSPEC/VLORA still required, and no schematic/board manufacture is authorized by this ADR.
