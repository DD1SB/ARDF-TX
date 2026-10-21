# One FOX10 first article — procurement and pogo fixture

**Procure for one populated board initially**, with handling/rework spares. The five-board bare order does not authorize a populated fleet. The [grouped electrical procurement CSV](FOX10-one-unit-procurement.csv) preserves every fitted reference and exact MPN from the committed [FOX10 bench BOM](../../assembly/FOX10-bench-BOM.csv). It specifies fitted quantity, extra pieces, proposed buy quantity, supplier observations and unresolved MOQs separately.

Fit **R31–R38: 8 × 560 Ω, `RC0402FR-07560RL`**. Fit **R50–R54: 5 × 0 Ω, `RC0402JR-070RL`**. Leave **L30–L34 and C30 DNP**. There are **74 fitted SMD components**; J2 and test pads are bare copper, J3 takes two hand-soldered wires, and H1/H2 are unplated holes. Use a known 50 Ω dummy load for initial RF work. A radiating Foxoring antenna/coupling population is not yet released.

**Spare policy**

Proposed quantities are a handling/rework allowance, not claimed supplier MOQs: at least 10 per small R/C value or fitted count plus five, **20 of the 560 Ω ballast**, two of each IC/crystal/power inductor/JST, four of each fitted RF-coil value (two fitted, two spare), and three PPTCs. The 100 nF LCSC option requires **100** pieces. Buy ten DMP2035U-7 (three fitted, seven spare) to satisfy the observed multiple of five. No optional antenna coils are required for this first bench assembly.

**Supplier observations accessed 22 October 2026**

These are public catalog/search observations, sometimes cached. They are **not confirmed quotations, reserved inventory or a checkout**. Prices exclude shipping, tax and any tariff. The older fleet estimate remains a budget document; it is not an exact one-unit purchase order. No fully quoted basket total is available.

| Item | Observation | Remaining procurement action |
|---|---|---|
| U2 TPS61099DRVR | [LCSC C2842395](https://www.lcsc.com/product-detail/C2842395.html): minimum/multiple **1/1**, 8,626 shown, **USD 1.3671** at 1 | Refresh at checkout. This supersedes the earlier USD 0.9925 observation for this gate. Buy two. |
| Q1/Q2/Q4 DMP2035U-7 | [LCSC C110499](https://www.lcsc.com/product-detail/C110499.html): minimum/multiple **5/5**, 275,585 shown, **USD 0.1348** at 5 | Buy ten for three fitted plus spares. Earlier MOQ10/price information was stale. |
| C6/C11/C12/C15 100 nF | [LCSC C1525](https://www.lcsc.com/product-detail/C1525.html): minimum/multiple **100/100**, USD **0.0038** at 100 | Buy 100 if using this channel; four fitted, 96 spare. |
| U3 ATtiny1616-MNR | [Mouser](https://www.mouser.com/en/ProductDetail/Microchip-Technology/ATTINY1616-MNR?qs=HXFqYaX1Q2yKNpuKQU9qww%3D%3D): minimum/multiple **1/1 cut tape**, USD **0.90** at 1, 16,509 shown | Search result was cached about a month; refresh stock/price. Buy two. |
| U4 SI5351A-B-GT | [DigiKey 336-2399-5-ND](https://www.digikey.com/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): quantity-one price **USD 2.33**, 3,080 shown, listed active | Buy two exact unprogrammed MSOP-10 parts; the tube's standard pack is not an MOQ. No automatic substitution with preprogrammed suffixes. |
| U5 74HCT240PW,118 | [Mouser](https://www.mouser.com/ProductDetail/Nexperia/74HCT240PW118?qs=P62ublwmbi%252BM8OUN39MiMw%3D%3D): cached catalog minimum/multiple **1/1 cut tape**, USD **0.38** at 1, 4,580 shown | Refresh direct listing; buy two TSSOP-20 parts, not BQ/HC substitutes. |
| L21/L22 1008LS-332XJRC | [Coilcraft](https://www.coilcraft.com/en-us/products/rf/ferrite-core-chip-inductors/1008-%282520%29/1008ls/1008ls-332/) lists quantity-one USD 1.00, but selected-configuration availability is unresolved. [Mouser UK exact listing](https://www.mouser.co.uk/en/ProductDetail/Coilcraft/1008LS-332XJRC?qs=sGAEpiMZZMv126LJFLh8y5AxJ2uVJ%252BbH2vzUslxMWb4%3D) has cached cut-tape stock; marketplace pages disagree on stock. | **OPEN:** confirm four exact parts, cut-tape minimum and delivery. No 2,000-piece reel is justified. Do not treat the direct series price as a confirmed deliverable quotation. |
| U1, Y1/Y2, F1, L1/L20/L23, J1, 2N7002 and other R/C values | Exact MPNs and existing candidate links retained in CSV; many entries were only budget allowances | **OPEN:** current stock, cut-tape MOQ/multiple and landed prices. Earlier assumed R MOQ100 / capacitor MOQ10 are not supplier confirmations. Check C4's effective capacitance and exact coil/crystal specifications before any substitution. |
| Fixture probes/receptacles | Manufacturer catalog identifies suitable exact parts below; price requires login/quotation | **OPEN:** MOQ, stock, delivery, reusable programmer/adapter availability. This does not block bare PCBs. |

The current confirmed observations only cover part of the basket. For every OPEN line, select a cut-tape distributor or existing verified stock, round the buy quantity to its real multiple and record that result before purchasing. Do not replace electrical parts merely to use an available reel. Local hand placement/reflow avoids assembly-library and machine-reel leader charges.

**Exact J2 contact map**

Reference **J2**, footprint **`Mini80:Pogo6`**, **bottom side**, 180° native rotation and flipped. Six **1.10 × 1.10 mm** rectangular pads/mask openings on a **2.00 × 2.00 mm grid**, B.Cu + B.Mask, no paste. All six exposed mask openings were checked against the actual Gerber. Copper connectivity below was checked through the routed net, not merely by equal net labels.

| J2 pad | Net | Native CAD X,Y (mm) | Actual connection | Fixture wire |
|---|---|---|---|---|
| **1** | GND | **60,74** | U3 pin 3 and EP pin 21; U1 pin 1 | Programmer/UART/SYNC ground |
| **2** | V3, nominal 3.0 V | **58,74** | U3 pin 4; U1 pin 2 output | Programmer **VTref sense only** |
| **3** | UPDI | **56,74** | U3 **pin 19 / PA0** | UPDI data, target-referenced 3.0 V compatible |
| **4** | FIX_RX | **60,76** | U3 pin 1 / PA2 | Fixture UART **TX**, 3.0 V logic |
| **5** | FIX_TX | **58,76** | U3 pin 20 / PA1 | Fixture UART **RX**, target-referenced input |
| **6** | SYNC | **56,76** | U3 pin 2 / PA3; R11 pull-down | Normally-low, common-ground **3.0 V** rising edge |

Viewed directly at the board bottom with the printed legend upright:

```text
       1 GND       2 V3       3 UPDI
       4 RX        5 TX       6 SYNC
```

Native coordinates use X right/Y down in the top CAD view. In the above direct bottom view, measured from its upper-left board corner with Y down, pad centers are **(25,24), (27,24), (29,24), (25,26), (27,26), (29,26) mm**. A mating fixture drawing must account for the view reversal; do not apply another arbitrary mirror to the Gerbers.

Power the target through J1 from a protected 1S pack or current-limited bench source in the battery range. Verify the JST harness polarity: **J1 pin 1 is positive**, irrespective of wire colors. **Do not connect programmer power against the onboard 3.0 V LDO, do not apply 5 V or high-voltage UPDI, and retain PA0's UPDI fuse function.** Three wires (J2 1/2/3) program the MCU; all six support UART configuration/readback and synchronization. Use 9600 baud 8N1 and the existing [firmware/fixture instructions](../../firmware/README.md).

**Fixture procurement**

The [fixture procurement CSV](UPDI-fixture-procurement.csv) separates reusable tools and bench accessories from board parts. A suitable identified probe is **INGUN GKS-075 214 064 A 2000**, item **GKS-075-0007**, with **0.64 mm tip**, minimum grid **1.91 mm**, working stroke **4.3 mm**, nominal working force **2 N**; matching receptacle **KS-075 47 G**, item **KS-07547G**. Buy **8 probes + 8 receptacles** (six used, two spare) if no existing fixture stock is available. Manufacturer details: [probe](https://ingun.com/en/products/GKS-075-series/GKS-075-0007) and [receptacle](https://ingun.com/en/products/KS-075-series).

The 1.47 mm receptacle collar fits the 2 mm grid. Its press-fit bore must follow the [manufacturer's receptacle drawing](https://ingun.com/media/6a/9e/65/1752274157/INGUN_KS-075_47_G_KS-07547G_EN_Datasheet.pdf?ts=1764417664), not the Mini80 board's 2.2 mm mounting-hole drill. This is a reusable external fixture, not extra circuitry on Mini80. Probe prices/MOQs are OPEN, so no fixture cost is invented.

Use an insulating fixture plate, supported clamp with a stroke stop, adjustable registration, two insulating M2 guides and an **asymmetric orientation stop**. The two diagonal board holes alone allow a 180° reversal. Six probes require roughly **12 N** at their recommended working stroke; support the board without pressing on top-side components. A 0.64 mm tip has only ±0.23 mm ideal centering margin on each 1.10 mm contact, so include hole/fixture tolerances in alignment. Check every wire with a meter before powering the first board. ENIG is suitable for evaluation contacts; repeated-contact life has not been measured.

Required reusable bench items: target-referenced UPDI programmer, 3.0 V-compatible UART/SYNC interface, common-ground wiring, protected 1S battery/JST-PH harness, fine-pitch paste/reflow tools, microscope, and 50 Ω dummy-load/coax pigtail. A 3.3 V adapter is not automatically a 3.0 V-safe output; use verified levels or a target-referenced adapter. Availability of these tools is OPEN; reuse existing verified equipment where available.

Follow the existing [ten-stage first-article procedure](../../FIRST_ARTICLE.md). Inspect U2/U3 EP wetting and measure rails/currents before enabling RF. Only after dummy-load tests should antenna coupling and Foxoring 30 m/250 m field measurements proceed. The eight 560 Ω resistors set the candidate profile; firmware cannot substitute for their physical population or field calibration.
