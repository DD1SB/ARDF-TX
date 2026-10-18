# M6-L1 sourcing and material delta

Retrieved/indexed observations on 2026-10-18, not purchase quotes or stock reservations. LCSC prices are USD; EUR totals use an explicit 0.90 EUR/USD planning assumption with ±10% sensitivity. Shipping, import charges, VAT and labor are separate/unquoted. Neither a manufacturer reel nor an observed catalog stock guarantees later delivery.

| Position | Exact orderable item | Evidence | q1 | q10/q20 | MOQ / stock observation |
|---|---|---|---:|---:|---|
| U70, 433 | Silicontra SX1262TR4-GC, LCSC C42381681 | Indexed USD | $5.5656 | $4.7161 | 1 piece, 189 indexed |
| U70, 868 | Silicontra SX1262TR8-GC, LCSC C42381682 | Indexed USD | $5.6375 | $4.7854 | 1 piece, 170 indexed |
| J7 | Hirose U.FL-R-SMT-1(10), Mouser 798-U.FL-R-SMT-110 | German indexed net EUR; not live quote | €1.11 | €0.946 | Cut tape MOQ1, 175770 indexed; regional listing shows different stock/€1.42/€1.22 |
| R70/R71 | RC0603FR-0710KL, 10k | Existing unquoted allowance | €0.01 each | €0.01 each | Ordinary0603; recheck supplier |
| C70 | CL10B104KB8NNNC,100n | Existing unquoted allowance | €0.02 | €0.02 | Existing native BOM exact value/MPN authoritative |
| C71 | CL10A106KP8NNNC,10µF10V | Existing unquoted allowance | €0.08 | €0.08 | Existing native BOM; effective capacitance unqualified |

Sources: [TR4 listing](https://www.lcsc.com/de/product-detail/C42381681.html), [TR8 listing](https://www.lcsc.com/de/product-detail/C42381682.html), [exact Hirose cut-tape listing](https://www.mouser.de/ProductDetail/Hirose-Connector/U.FL-R-SMT-110?qs=kL1ClTr6oBoOdtqlGQpQrQ%3D%3D). Manufacturer/distributor PDF hashes resolve the TR/ZTR alias; incoming labels/geometry must still be inspected. No factory-reel MOQ is inferred. Hirose(01) is mechanically equivalent but observed MOQ100, so no reason to replace the available(10) cut-tape part.

The complete twelve base/radio BOMs contain FIT/DNP records and q1/10/20 costs. NO_LORA costs are unchanged from R1. The added populated option is approximately €5.31/€5.37 at q10 for433/868, before external antenna/pigtail. FX alone changes the q10 module estimate by about±€0.42/€0.43. The option's updated total is lower than the former unqualified868 allowance, but this is not an asserted purchase saving. Most base small-part material remains unquoted.

External materials are separate: a band-correct50Ω antenna, U.FL-to-SMA bulkhead pigtail, support/strain relief and enclosure feedthrough. Taoglas CAB.011 is a documented95mm U.FL-compatible/SMA-F example. TE ANT-433-CW-HWR-SMA and ANT-868-CW-HWR-SMA are band-specific antenna examples; their manufacturer pages say active but no direct-store supply. Current distributor price/stock remains OPEN, and suitable documented equivalents are permitted. Planning allowances only: €3–10 pigtail, €5–15 antenna, €1–3 mounting/strain relief per transmitter; not quoted quantity breaks. Verify the433 quarter-wave counterpoise and actual installation match. Do not silently buy RP-SMA or MHF4 instead of the specified interfaces.

Bare PCB processing, dimensions and standard options do not change. The inherited unquoted bare-board planning allowances are €9/€14/€24 for batches of5/10/20 before freight/VAT, not JLC quotations. Standard manual assembly/stencil is sufficient; no contract assembly line or special laminate is required. Procurement and fabrication are not authorized.
