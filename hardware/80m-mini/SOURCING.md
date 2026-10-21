# Sourcing and fleet cost review — 2026-10-21

All figures are USD catalog observations accessed on the stated date, excluding taxes, shipping and tariffs. Search/catalog caches may be older; no inventory was reserved and no checkout was performed. Exact sources, breaks, MOQ, multiples, required quantity, purchased quantity and excess are preserved in [cost-review.json](assembly/cost-review.json). An `ALLOWANCE` is a budgeting assumption, not a supplier quotation. There are no 2016-price quotations in this estimate.

| Part | Supplier observation / unit price | MOQ / small-fleet consequence | Comparison / disposition |
|---|---|---|---|
| ATtiny1616-MNR | [Mouser](https://www.mouser.com/en/ProductDetail/Microchip-Technology/ATTINY1616-MNR?qs=HXFqYaX1Q2yKNpuKQU9qww%3D%3D): $0.90 at 1, $0.872 at 25 | 1 cut tape; full reel 6,000 is not required | German EUR listing is a separate currency, not silently mixed into USD. |
| Si5351A-B-GT | [DigiKey](https://www.digikey.com/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): $2.33 at 1, $1.718 at 10 | 1; tube pack size 95 is not an MOQ | Alternate Mouser/catalog observations $2.19 / $1.62; use higher observed prices and refresh. |
| HCT240PW,118 | [Mouser](https://www.mouser.com/ProductDetail/Nexperia/74HCT240PW118?qs=P62ublwmbi%252BM8OUN39MiMw%3D%3D): $0.38 at 1, $0.262 at 10 | 1 cut tape; 4,580 shown | BQ alternative had JLC stock 0, MOQ10 ~$0.9425; other channels required large marketplace/reel quantities. PW selected. |
| TPS61099DRVR | [LCSC C2842395](https://www.lcsc.com/product-image/C2842395.html): $0.9925 at 1, $0.8432 at 10 | Current image catalog MOQ1; 1,293 shown | Alternate cached page MOQ10 / ~$1.09. Basket refresh required; no assumption of JLC assembly stock. |
| MCP1700T-3002E/TT | [LCSC C62244](https://www.lcsc.com/product-image/C62244.html): $0.5207 at 1, $0.4123 at 10 | 1; 2,186 shown | DigiKey listing approximately $0.51 at 1. |
| DMP2035U-7 | [LCSC C110499](https://lcsc.com/product-detail/MOSFETs_Diodes-Incorporated-DMP2035U-7_C110499.html): $0.0569 at 10 | MOQ/multiple10; three per board require 20 pieces for five boards or 40 for twelve | This cached observation is stale. DigiKey showed no stock, ~$0.52/$0.318 at 1/10 and long lead time. Refresh or qualify an exact pin-compatible replacement before assembly. |
| ABS07-32.768KHZ-T | [Mouser](https://www.mouser.com/en/ProductDetail/ABRACON/ABS07-32.768KHZ-T?qs=3SpAxaLJ01g8GJWeO3sA3Q%3D%3D): $0.61 / $0.528 at 1/10 | 1 cut tape | Symmetry observation $0.61/$0.53 supports the same price scale. |
| CX3225FB25000F0FZZH1 | [Mouser](https://www.mouser.com/ProductDetail/KYOCERA-AVX/CX3225FB25000F0FZZH1?qs=Tc%252BHE9vUsnv4CjUnsmTvrA%3D%3D): $0.36 / $0.31 at 1/10 | 1; stock observations disagree between detail/list | Selected instead of a difficult Abracon carrier-reference SKU; exact 10pF load and crystal pads verified. |
| 1008LS RF coils | [Coilcraft](https://www.coilcraft.com/en-us/products/rf/ferrite-core-chip-inductors/1008-%282520%29/1008ls/1008ls-332/): $1 at 1, $0.78 only from 200 | Less-than-reel tape offered; selected stock must be checked | 1µH Mouser observation $1.48 and 1,134 available; budget uses that for L20/L23. The 4.7µH direct page requests a quotation, so its $1.50 allowance is explicitly unquoted. |
| 1812LS-333XJRC | [Mouser](https://www.mouser.com/ProductDetail/Coilcraft/1812LS-333XJRC?qs=lc2O%252BfHJPVbUeCCXE6deKw%3D%3D): $1.18 / $0.99 at 1/10 | 1; 397 shown | Direct catalog ~$0.77, selected configuration availability uncertain. Avoid full reels for five prototypes. |
| 100nF CL05B104KO5NNNC | [LCSC C1525](https://www.lcsc.com/de/product-detail/C1525.html): $0.0045 at 100 | MOQ/multiple100; excess explicitly costed | Other locales show lower prices; higher figure used. Replaces an unattractive old Murata 100nF SKU. |
| MF-FSMF020X-2 | [DigiKey](https://www.digikey.com/en/products/detail/bourns-inc/MF-FSMF020X-2/2039254): $0.448 at 5 / $0.414 at 10 | 1 cut tape | 85,792 shown; 0603 part uses manufacturer land pattern, not an assumed 0805 package. |

Each exact resistor/capacitor MPN is in the electrical BOM. Remaining prices use explicit allowances: resistors $0.005 with MOQ100 per value, Murata small capacitors $0.08 with MOQ10, bulk capacitors $0.12 with MOQ10, 2N7002 $0.08 with MOQ10, JST $0.95 with MOQ1, power inductor $0.10 with MOQ10 and unquoted optional RF coils $1.50 with MOQ1. These limits deliberately avoid claiming a fully supplier-priced basket.

| Population | Five-board parts basket | Per board | Twelve-board parts basket | Per board |
|---|---:|---:|---:|---:|
| MINI50 bench, 50Ω | $80.04 | $16.01 | $170.80 | $14.23 |
| FOX10 bench, 50Ω | $80.04 | $16.01 | $170.80 | $14.23 |
| MINI50 initial wire match | $99.24 | $19.85 | $214.28 | $17.86 |

The bench baskets contain $20.95/$43.90 of unquoted allowances at five/twelve boards; their remainder uses the cited observations. Variant differences are the eight ballast values and optional matching population, not separate firmware. A fleet with ten slotted foxes plus S/MO uses the same board parts; battery sizes differ. FOX antenna tuning parts remain per-installation selections.

Bare PCB, stencil, assembly, panel tooling, shipping, taxes, battery, enclosure, antenna, fixture and testing are **not included**. A real JLC quotation needs a shipping destination and final panel/assembly choices. No invented fabrication quote is added to the parts estimate. Prefer five bare PCBs, a fine-pitch stencil and local reflow for first articles. Standard JLC fabrication does not imply every part is in the JLC assembly library; consignment or local placement will be needed for some coils/crystals. Coilcraft machine-ready leader/trailer service can add $25 for less-than-reel orders; hand-placement cut tape avoids that service charge.

Current manufacturer catalog families were selected; long-tail stock, exact approval sheets and supplier basket revalidation remain assembly-release tasks. A supply substitution must preserve electrical characteristics and verified numeric pads. This procurement HOLD does not prevent independent review of, or making five unpopulated copies of, the native PCB candidate.
