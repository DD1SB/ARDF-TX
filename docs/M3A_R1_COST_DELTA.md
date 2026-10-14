# M3A-R1 — component and cost delta

Date: **2026-10-14**. EUR **net**; VAT, labor, tooling and engineering separate. Current component lines/prices remain the single [M3 workbook](M3_80M_COMPONENT_WORKBOOK.md) and [CSV](M3_80M_BOM.csv). This comparison is generated from tagged **m3a-r0** and the current exported manifest/cost ledger; no manual price adjustment.

| Population | Purchased R0 → R1 | IC R0 → R1 | Pads R0 → R1 | Flags R0 → R1 | Positions R0 → R1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full module components | 185 → 193 | 20 → 18 | 22 → 22 | 7 → 8 | 214 → 223 |
| Foxoring-only components | 128 → 115 | 15 → 13 | 13 → 13 | 4 → 4 | 145 → 132 |

The R0 manifest has 215 total references: the full population fits 214 positions (R336 DNP), **185 purchased parts and 20 ICs**. Fox fits 145 positions, **128 purchased parts and 15 ICs**. Test pads, flags, multiunit gate symbols and footprint assignments are not separate purchases.

| Population / batch | R0 EUR/unit | R1 EUR/unit | Delta | Observed / estimate R1 |
| --- | ---: | ---: | ---: | --- |
| Full module components /6 | 28.54 | 31.18 | +2.64 | 13.13 /18.06 |
| Full module components /10 | 25.35 | 26.60 | +1.25 | 9.37 /17.23 |
| Full module components /20 | 25.14 | 26.60 | +1.46 | 9.37 /17.23 |
| Foxoring-only components /6 | 11.61 | 12.01 | +0.40 | 4.72 /7.29 |
| Foxoring-only components /10 | 10.55 | 10.80 | +0.25 | 3.62 /7.19 |
| Foxoring-only components /20 | 10.53 | 10.46 | -0.07 | 3.58 /6.88 |

## Full module components

Removed: #FLG211, #FLG212, #FLG213, #FLG214, C221, C223, R320, R322, R323, R341, R342, U213, U214.

Introduced: #FLG221, #FLG222, #FLG223, #FLG224, #FLG225, C404, D219, D220, D221, D222, D223, D224, Q225, Q226, Q227, Q228, Q229, R219, R220, R225, R409, R410.

Modified: C233, C306, C310, C313, C401, C402, Q201, Q301, Q302, Q401, Q405, Q406, Q502, R201, R311, R312, R317, R318, R321, R324, R325, R326, R327, R328, R329, R334, R335, R337, R338, R339, R340, R401, R451, R453, TH301, U202, U203, U211, U221, U222, U223, U224, U312, U314, U401.

| Block, quantity ten | Before | After | Delta |
| --- | ---: | ---: | ---: |
| connectors | 1.875 | 1.875 | +0.000 |
| decoupling | 0.558 | 0.510 | -0.048 |
| fox | 2.862 | 2.775 | -0.087 |
| interlocks | 2.597 | 3.243 | +0.646 |
| normal_driver | 2.122 | 3.051 | +0.929 |
| normal_filter | 3.510 | 3.510 | +0.000 |
| normal_final | 0.622 | 0.622 | +0.000 |
| normal_shaper | 1.021 | 1.021 | +0.000 |
| normal_supply | 3.960 | 3.786 | -0.174 |
| protection | 3.531 | 3.519 | -0.012 |
| source | 1.788 | 1.788 | +0.000 |
| supply | 0.900 | 0.900 | +0.000 |

## Foxoring-only components

Removed: #FLG214, C221, C223, C310, C313, R311, R312, R317, R318, R320, R321, R322, R323, R324, R325, R326, R327, R328, R329, R334, R335, R336, R337, R338, R339, R340, R341, R342, U213, U214, U312.

Introduced: #FLG224, C233, D219, D220, D223, D224, Q225, Q226, Q227, Q228, Q229, R219, R220, R225, R228, R348, R349, U224.

Modified: Q201, Q406, Q502, R201, R451, R453, U202, U203, U211, U221, U222, U223, U314.

| Block, quantity ten | Before | After | Delta |
| --- | ---: | ---: | ---: |
| connectors | 0.875 | 0.875 | +0.000 |
| decoupling | 0.510 | 0.438 | -0.072 |
| fox | 2.862 | 2.834 | -0.028 |
| interlocks | 2.474 | 3.351 | +0.877 |
| protection | 2.043 | 1.518 | -0.525 |
| source | 1.788 | 1.788 | +0.000 |

## Complete Fox unit — same accounting scope

| Batch | Materials | Shared fleet | Total including fleet |
| --- | ---: | ---: | ---: |
| 6 | 66.38 | 13.50 | 79.88 |
| 10 | 59.43 | 8.10 | 67.53 |
| 20 | 59.15 | 4.85 | 64.00 |

The historical €29.06/€55.24/€63.34 M1/Fox audit remains unchanged. R0 complete material at ten was €59.182; R1 changes only the RF component basket. S3/RTC, protected 2S1P, compact antenna/matching, case, wiring and fabrication scope are retained; socket halves already on the RF board are removed once. No fourth board or alternative MCU. No new assembly/fabrication quote. Component reduction is **not** a claim of labor savings.

The full board has fewer ICs but more individual protection/configuration parts. Corrections do **not** produce a quantity-ten material saving. Removing the selected-path/arming-context protection would lower the number but restore confirmed faults. At twenty, pooled low-current MOSFET purchasing gives a small estimated Fox saving; its hundred-piece price is estimated, so this is not secured savings.

BSS138BK replaces low-current switches and addresses stacked-gate stress; DMN2056U remains for the 70 mA shaper sink. Only its ten-piece EUR price is observed; one/hundred prices are estimates. 74HC174 price/stock is unquoted; manufacturer Production verified. Toshiba HC175 NRND and AP7384 NRND were rejected. C404 polymer pricing is an indexed distributor observation, not a reserved basket; pulse resistor/diode quotations remain OPEN. See [simplification](M3A_R1_SIMPLIFICATION.md) and [verification](M3A_R1_VERIFICATION.md).

[Machine comparison](M3A_R1_DELTA.json).
