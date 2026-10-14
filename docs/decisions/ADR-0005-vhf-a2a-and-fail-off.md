# ADR-0005 — VHF A2A experiment and persistent hardware fail-off

Status: **Conditionally accepted at architecture level via ADR-0007; detailed electrical implementation remains Proposed**
Date: 2026-10-13

## Context and sources

IARU T2.8 permits continuous carrier with keyed AF tone or keyed carrier with AF tone, at 70–80% AM. [Netherlands primary history](https://fox.ardf.veron.nl/Documenten/Hall_of_Fame/ARDF_ontwikkeling_in_Nederland.pdf), Figs.33/43/60–62, documents supply modulation in built G3ZOI/PA0JBG examples. SmartFOX VHF is FM, and historic square modulation requires changes. Current derivative PA and envelope are unvalidated.

## Proposal

First VHF experiment: local Si5351 carrier with sinusoidal series drain/collector modulation; continuous carrier inside active slot, shaped keyed ~800 Hz AF. ADF4002/discrete VCO is the lower-cost source fallback if spectral tests fail. Low-level AM plus a linear class-AB chain is the alternative modulation topology. Outside slots shut down source/input drive and true PA power path. Size for carrier ERP with separately reported mean/PEP: assumed net antenna gain −1 dB yields 1.259 W carrier and 4.079 W PEP at 1 W ERP/m=0.8; ≥1 dB clean headroom requires ≥5.14 W capability. Gain/reference convention must be confirmed before calibration.

Use external health lease watchdog, power-good/POR and analogue fault inputs feeding persistent latch, plus independent RF-input and PA-supply gates. Retuning requires silent/discharged path and fresh qualification. Watchdog pulse recovery alone must not rearm. [TPS3431 EVM guide](https://www.ti.com/lit/ug/snvu614/snvu614.pdf) explains why a separate latch/startup qualification is necessary.

## Alternatives / consequences

FM sidetone and unverified 100% chopping are rejected for Classic. Series modulation has SOA/thermal/trough-leakage/AM-to-PM risk; linear RF chains add bias/current. [ADR-0007](ADR-0007-cost-optimized-m1.md) removes MCU bridges and proposes low-cost monostable/latch/POR/gates while retaining independent source/supply shutdown. PD55008 is now a priced active PA candidate; its 144 MHz AM/drive behavior is unverified. Stocked BFP650 is an explicit EOL-dependent driver comparison, not a repeatable-production choice. RD06/AFT remain historical/excluded references.

## Required decisions and tests

The user conditionally accepted the architecture and MMIC preference. Antenna/gain/power convention closure remains open. [VHF preparation](../M2_VHF_RF_REVIEW.md) and [ADR-0008](ADR-0008-rf-evaluation-gates.md) supersede the earlier drive/modulator assumptions and explicitly exclude BFP650. RF analysis and evaluation preparation are authorized; complete product layout and procurement require measured G0–G9 gates. No radiation or hardware validation is implied.
