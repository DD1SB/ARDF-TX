# Exact JLCPCB order specification — five bare Mini80 evaluation boards

Prepared 22 October 2026. **Instructions only; no order or quotation has been submitted.** Gate: [GO for five bare evaluation boards](README.md), copper baseline `bdac015766cab5aa62fc106aefb151f634e7f109`. M80-E2 is the review name; order the unchanged **M80-E1** artwork.

Upload [Mini80-M80-E1-JLCPCB-bare.zip](../../fabrication/Mini80-M80-E1-JLCPCB-bare.zip).

```text
SHA256 d55f8791e4e18c89d3279581073e86afd17dfd55340b3f0aaf3966afde356142
```

| Order field | Exact selection |
|---|---|
| Service | Standard rigid PCB fabrication; bare boards; no PCBA |
| Quantity | **5** |
| Delivery format / designs | Single PCB, **1 design**, no customer/JLC panelization |
| Finished size | **35.00 × 35.00 mm** |
| Layers | **2** |
| Material | **Standard FR4**, default standard Tg/laminate; no special RF laminate |
| Thickness | **1.6 mm**, standard tolerance |
| Outer copper | **1 oz on both sides** |
| Surface finish | **ENIG**, standard offered gold thickness |
| Solder mask / legend | **Green / white**, both sides as supplied |
| Via option | Minimum hole **0.20 mm**, minimum via diameter **0.45 mm**; ordinary mechanical through vias |
| Via covering | **Standard tenting according to supplied mask files**; EP top holes intentionally open; no resin/copper filling, plugging or capping |
| Profile | Standard CNC routed outline; regular precision; no V-score, slots, countersinks or special edge work |
| Other | No controlled impedance, blind/buried vias, HDI, gold fingers, castellations, edge plating, special stackup or electrical assembly |
| Board electrical test | Standard offered bare-board test |
| Order number marking | Accept normal factory marking only in a free legend area; keep it away from J2 contact pads and the pogo/battery legends |

The `.gm1` **path centerline** sets the 35 mm square. Do not interpret its 0.05 mm plotting stroke as a 35.05 mm board. Map the supplied `.gtl/.gbl`, `.gts/.gbs`, `.gto/.gbo`, `.gm1` and **separate PTH/NPTH metric drill files** to their named layers. The job JSON and PDF drill maps are explanatory, not extra copper layers. There are 109 PTH holes and two 2.20 mm NPTH mounting holes. Do not convert the mounting holes to plated holes.

Standard regular outline precision (±0.2 mm) and thickness tolerance (±10%, approximately 1.44–1.76 mm) are adequate; no precision-routing or custom-stackup surcharge is needed. The specified vias meet the published standard-size category. These settings follow [JLCPCB's current capabilities](https://jlcpcb.com/capabilities/pcb-capabilities), not a completed checkout price.

Suggested PCB remark, if needed:

```text
Mini80 M80-E1, five bare evaluation PCBs. Finished outline 35 x 35 mm from
GM1 centerline. Two NPTH mounting holes must remain unplated. Follow both
solder-mask layers: keep all six J2 bottom contact pads exposed. U2/U3 EP
top openings expose ordinary through vias; follow supplied bottom mask.
No filled/capped via-in-pad process. Standard fabrication only.
```

**Stencil recommendation**

Use [Mini80-M80-E1-stencil.zip](../../fabrication/Mini80-M80-E1-stencil.zip), SHA256:

```text
f8256e8e347b15e22c5a1f88ec1815c045123084d6db768ffcd33811f37cd860
```

Select **one top-side, 0.10 mm stainless-steel laser-cut stencil**, frameless for manual printing. A **100 × 100 mm custom sheet** centered on the 35 mm board is suitable for a small manual jig; it fits inside the 290 × 190 mm valid area of the standard 380 × 280 mm model. Select that model and the custom frameless cut size where offered. A full standard frameless sheet is an acceptable equivalent if required by the available holder. No stepped thickness, electroforming or nanocoating is necessary. This is a stencil recommendation; no stencil order was placed.

Use **F.Paste only** for apertures; B.Paste is intentionally empty. The released stencil already omits L30–L34/C30 and matches the FOX10 bench population; replacing eight 100 Ω resistors with eight 560 Ω resistors does not change apertures. Retain U2's two EP windows and U3's four. Do not add holes for J2, test points, optional matching components or J3. Review any proposed CAM aperture changes before accepting them.

Suggested stencil remark:

```text
Please follow the supplied solder paste layer only, and ignore the difference
between the solder mask layer and solder paste layer. Use top F.Paste exactly,
0.10 mm thickness. Preserve EP windowing and DNP omissions. No automatic
pad expansion/reduction or extra mask-derived apertures without agreement.
```

JLCPCB lists 0.10 mm as a standard stencil thickness and permits custom frameless sizes. See [stencil instructions](https://jlcpcb.com/help/article/instructions-for-stencil-order), [custom-size ordering](https://jlcpcb.com/help/article/how-to-order-a-stencil), and [standard aperture processing](https://jlcpcb.com/help/article/opening-process-standard-of-stencil). The explicit paste remark matters because their default aperture processing can modify fine-pitch openings.
