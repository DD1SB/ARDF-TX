# M4A-V1R1 — independent manufacturing-review recommendation

Date: 2026-10-18. **GO for independent review of five standard-process RF80-V1R1 bare evaluation PCBs. No manufacturing release or acceptance tag.** Supplier upload/CAM/quote, purchasing and physical work require separate authorization. The proposed V1R1-first evaluation sequence needs explicit review; the original E2-first M4A restriction has not been unilaterally removed.

## Implemented result

The active [native project](../hardware/80m/production/RF80_V1.kicad_pro) and [PCB](../hardware/80m/production/RF80_V1.kicad_pcb) remain **150 × 110 mm**, two-layer standard FR4, **1.6 mm / 1 oz / green / white / lead-free HASL**. All 354 ordinary vias and the 140 × 100 mm four-hole mounting pattern remain. No special drilling, press-fit precision, controlled impedance, filling or custom stackup is required.

The original 25 tight holes and four additional connector holes now accommodate ordinary −0.08/+0.13 mm PTH variation: **J101/Q402/Q403 1.40 mm; J502/J401 1.30 mm; J301 1.90 mm**. Minimum calculated diametric lead clearance is 0.103 mm (J502), using disclosed incoming screening envelopes where manufacturer tolerances are missing. [Lead-fit audit](M4A_V1R1_HOLE_AND_FOOTPRINT_AUDIT.md). Package alignment, solderability and real dry-fit remain first-article checks, not a claim that every tolerance stack has been physically demonstrated.

Essential silk is now ≥1.0 mm / 0.15 mm; small references and outlines are on fabrication/assembly layers. All component positions and all tracks/vias are unchanged. Only J502 lands and their local ground-fill clearance changed. No electrical value, purchased MPN, RF topology, transformer winding, protection behavior, full/Fox population or controller pin contract changed. RF80 J101's **all 16 pins** match the actual M6-L1 controller.

## Nonphysical verification

| Check | Current result |
| --- | --- |
| KiCad 10.0.6 ERC | 0 errors / 0 warnings; three inherited informational defaults disclosed |
| DRC / unrouted / schematic parity | **0 / 0 / 0**, no DRC exclusions; all 62 configured categories enabled |
| Native electrical / critical manufacturer maps | **604 pad memberships / 55 devices**, exact ST BD140 and TI TL431 preserved |
| Logic / protection | **256 combinations / 31 states / 16 timing corners** |
| Negative tests | 12 retained + 5 lead-fit + 14 DFM + 9 interface/population = **40 rejected mutations** |
| Ground network / models | One connected network, 41 filled regions, 112 GND vias; all 199 model references resolve |
| Standard-JLCPCB native DFM | **PASS**; actual copper/mask/drill/legend/edge inspected |
| Final export consistency | All **401 holes** (397 PTH + 4 NPTH); Gerber/IPC key pin maps and populations checked |
| Physical fit, protection, RF, thermal, spectra, endurance | **NOT_RUN** |

## Costs and sourcing

Net-EUR planning per board; current indexed comparators, historical observations and unquoted materials remain separate. No commercial quotation exists.

| Batch | FULL components | FOX_ONLY components |
| --- | ---: | ---: |
| 1 | 35.94 | 15.20 |
| 5 | 34.28 | 12.92 |
| 10 | 29.23 | 11.50 |
| 20 | 29.23 | 11.15 |

The manufacturing correction adds **€0.00 component material**. Refreshed prices/core-wire allowances raise the quantity-ten planning basket relative to original M4A by approximately **€1.92 FULL / €0.69 FOX_ONLY**; this is repricing, not a design-part increase. Use [costs.json](../hardware/80m/production/review/M4A-V1R1/costs.json) for exact values and uncertainty categories. Substantial material is unquoted: at ten approximately **€19.40 FULL / €6.32 FOX_ONLY**. USD-index conversions use an explicit planning assumption, not a verified EUR supplier offer.

Five bare boards are budgeted **€26.85–53.88** before **€10–25** PCB freight, tax and payment fees, using an unquoted setup/area model. This is neither an actual JLCPCB quote nor factory CAM acceptance. Components, shared controller, batteries, charger, antennas, cable mates, heatsinking and labor are separate categories. See [source-status](../hardware/80m/production/review/M4A-V1R1/source-status.json) and complete full/Fox BOMs in the review package.

Exact LM5134B cut supply/EU cart, IRF610 exact-suffix stock, JST small-quantity stock, core material/AL and mates must be rechecked before purchasing. Three connector manufacturers omit lead tolerances; incoming screening/dry-fit is explicit. No premium PCB service is used to compensate for this uncertainty.

## Remaining approvals

1. Review the [V1R1-first proposal](M4A_V1R1_PROTOTYPE_TRANSITION.md) against the preserved M4A E2-first condition. No accepted ADR changed.
2. Independently inspect the [review package](../hardware/80m/production/review/M4A-V1R1/README.md), actual renders, fit/insulation and clearances. Final enclosure, heatsink thermal capacity and physical connector array fit are not qualified.
3. If separately authorized, upload the isolated [RF80 fabrication ZIP](../hardware/80m/production/review/M4A-V1R1/fabrication/RF80-V1R1_JLCPCB_5boards.zip) for standard-price/CAM review; then obtain separate purchase authorization.
4. Retain all staged driver-absent protection gates before fitting U401/Q402, then controlled dummy-load commissioning and all seventeen physical qualification tests.

The [three-board readiness matrix](../hardware/80m/production/review/M4A-V1R1/THREE_BOARD_ORDER_READINESS.md) provides separate five-board datasets for controller M6-L1, RF2M M5B-E4R1 and RF80-V1R1. Other boards and their historical exports are unchanged. Nothing here authorizes uploading, ordering, assembling, energizing or transmitting.
