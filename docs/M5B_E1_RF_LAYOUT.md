# M5B-E1 RF layout

2026-10-16. One integrated RF2M evaluation PCB, **NOT RELEASED / UNBUILT**. The native design is [RF2M.kicad_pcb](../hardware/2m/RF2M.kicad_pcb). Final CAD reports and drawings reside in [M5B-E1](../hardware/2m/review/M5B-E1/). RF qualification is NOT_RUN.

## Stack-up and line geometry

The 180 × 140 mm board uses two copper layers. Proposed finished thickness is 0.8 mm: 70 µm top copper, **0.64 mm copper-to-copper FR4 dielectric**, 70 µm bottom copper and approximately 10 µm mask per side. ENIG is proposed for reproducible RF assembly. The fabricator must confirm the actual core, copper definition, finished thickness and mask. A generic 0.8 mm or 1.6 mm replacement stack-up is not equivalent.

A quasi-static Hammerstad/Jensen calculation assumes Dk=4.3, loss tangent 0.02, copper thickness 0.07 mm. The candidate 50 Ω width is approximately **1.102 mm**. This model excludes solder mask, component pads, local fringing, plating and dielectric tolerance. It is a fabrication starting point, not measured impedance certification. Two layers provide a continuous RF return without premium controlled-impedance or four-layer fabrication. The larger area accommodates ordinary assembly and the two independent heat paths.

The original [ST schematic](https://www.st.com/resource/en/schematic_pack/steval-tdr003v1_schematic.pdf) and layout use approximately 0.508 mm dielectric, 70 µm copper and 0.92 mm lines. These geometries are not copied blindly. The original electrical path lengths are preserved in dedicated copper net-tie footprints, with recalculated width:

| Section | Length, mm | Function |
| --- | ---: | --- |
| TL603 | 6.23 | Driver-side input-match section |
| TL604 | 6.62 | Input network between shunt/blocking and gate-series elements |
| TL605 | 5.80 | Final gate approach |
| TL606 | 2.20 | Drain-to-first output shunt |
| TL607 | 11.00 | Output impedance transformation |
| TL608 | 12.40 | Output matching after L638/C638 |
| TL609 | 2.00 | DC block to elliptic LPF |

[transmission-lines.csv](../hardware/2m/review/M5B-E1/transmission-lines.csv) records the original/derived impedance and phase estimates. The small effective-Dk phase difference is retained explicitly, rather than claiming exact physical equivalence. Pad discontinuities, folded current paths through inductors and actual substrate tolerance require RF alignment. No matching line is a zero-length wire.

The line footprints intentionally join logical net names across a copper body. Fabrication electrical testing must use the supplied physical net aliases/merged test netlist rather than treat these net ties as shorts. Logical KiCad net names remain intact for schematic parity.

## Input matching and drive

The PHA-1+ has nominal 50 Ω ports. ST's old PD84001 drain interstage is not evidence of a 50 Ω match. The localized M5B input network retains TL603/604/605, C632=330 pF and L606=33 nH, with **C631=22 pF, C633=22 pF and L634=47 nH** as initial values. A lossless inverse ABCD calculation at144.7 MHz finds a load near **9.64−j24.39 Ω** for a50 Ω input. The explicit intrinsic-gate assumption is3 Ω in series with80 pF; in parallel with the retained33 nH bias feed it becomes9.88−j23.55 Ω. This produces modeled input52.11−j4.03 Ω, approximately27 dB return loss. The80 pF CISS condition is1 MHz/zero gate bias, **not** a144 MHz large-signal device impedance. Coil losses, bias-decoupler ESL, pads, Miller feedback and bias dependence are omitted. This is a sensitivity model supporting initial alignment, not a physical match claim. An earlier simplified24 nH/47 pF estimate omitted the bias feed and is withdrawn.

Allowed first-alignment options are C631 DNP/22/33/47/56 pF, C633 DNP/22/27/33/39/47 pF and L63424/33/47 nH. Use actual available RF-inductor series values; no nonexistent0603HC27 nH MPN is specified. The three positions already exist in the reference; no extra tuning network is added. [input-match-sensitivity.csv](../hardware/2m/review/M5B-E1/input-match-sensitivity.csv) varies intrinsic gate resistance/capacitance and exposes model dependence. Stop and review if this bounded adjustment set cannot yield useful stable gain; do not silently redesign the ST output network.

C602 provides DC blocking, R650 is a liftable series link and R651 is a normally omitted 49.9 Ω driver test load. These features are on this board. A short coax lead and external RF generator may be connected at the lifted interface for diagnosis, without another PCB. Return the normal link/load population after alignment.

The initial 10 dB source pad protects first power-up. An **assumed matched-source available-power** budget of10.4 dBm fundamental, 1 dB source-filter loss, 6 dB calibrated pad and 16 dB driver gain predicts 19.4 dBm. PHA-1+ nearby manufacturer typical P1dB values are approximately 22.7 dBm at 50 MHz and 22.64 dBm at 200 MHz; neither is a guaranteed 144 MHz measurement. The 19 dBm target leaves approximately 3 dB typical compression margin. Measure source, filter, pad and MMIC output together. Finite LVC output resistance, the AC-coupled reactive filter load and harmonics must be included in the measured budget;10.4 dBm is not a claim of an ideal3.3 V square wave applied directly across50 Ω. Verify output-current/thermal behavior as part of source/driver acceptance. Changing Si5351 drive strength after the LVC buffer does not provide a calibrated RF attenuator.

## Placement, return and thermal paths

The source/filter/driver/final/match/filter/output chain occupies the upper RF strip. The driver-to-gate network is contiguous; the final drain copper is deliberately limited and the output filter follows the ST electrical topology, including parallel LC elliptic branches. L604's low-DCR feed and local C603/C604 are above the MMIC. Gate-bias and drain feeds approach from opposite sides. Ordinary component RF grounds have nearby vias; the PHA flange and PD source have explicit ground contacts.

Bottom signal routing is excluded under the main RF strip and the PA heat-spreader area. Top ground fill is excluded immediately beside the microstrip matching bodies so an accidental coplanar gap does not invalidate the width calculation. Bottom ground remains the intentional return. Outside this strip, both layers contain control/power routes and stitched ground; review actual copper previews, not an assumed unbroken plane across the entire board.

The normal SMA is near the upper right edge; the independent training MMCX/filter/buffer is near the lower right edge, approximately 88 mm away. The two branches share source, logic supply and ground only. There is no circuit element joining NORMAL_RF to TRAIN_RF. Clock feedthrough, common-ground coupling and physical port isolation remain measured acceptance gates.

The PD source uses twelve ordinary 0.6/0.3 mm ground vias, with bottom tenting and segmented source paste. A14 ×12 mm bottom GND contact window exposes the thermal contact around two masked via columns; use an electrically insulating thermal sheet and separate sink ground bond;inspect flatness/contact instead of relying on solder mask as insulation. The stencil proposal is approximately 39% source-land coverage, 100 µm stencil starting thickness. These are assembly proposals, not a demonstrated void-free thermal process. RNW boost center pads are three separate electrical contacts, never a common thermal slug.

Q401 D45H11 is upright at the top edge with its **live collector tab insulated** from an external pass-device sink. Q402 BD139 collector is also live and cannot share bare metal. The PD source connects to a separate grounded bottom spreader with two M3 clearance holes and a separate lower sink. The mechanical arrangement and 40 mm bench supports are described in the thermal document. RF compliance, isolation and temperature cannot be inferred from DRC.

RF probe contacts are offset onto exposed microstrip rather than hidden under packages:TP601(108.5,55),TP602(115.2,55),TP603(145.3,52.206),TP604(89.1,55)mm. Their0.6mm copper lies inside the existing wider RF line;short logical connection overlays do not create a stub or alter line length. These are nearby diagnostic planes,not intrinsic die terminals. Use a calibrated low-capacitance RF pickup/differential probe for active RF;ordinary passive-probe capacitance can detune the circuit. End-to-end acceptance normally uses the50Ω output and an envelope detector/coupler instead.
