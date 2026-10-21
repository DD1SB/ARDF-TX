# M5B-E6R2 bare evaluation manufacture

The authoritative native project is[RF2M.kicad_pro](../hardware/2m/RF2M.kicad_pro).
Current review package:[M5B-E6R2](../hardware/2m/review/M5B-E6R2/README.md).
The[historical E5 dataset](../hardware/2m/review/M5B-E5/) remains unchanged.
E6 and E6R1 analysis packages remain immutable historical HOLD evidence.

- [Five bare boards ZIP](../hardware/2m/review/M5B-E6R2/fabrication/RF2M-M5B-E6R2_JLCPCB_5boards.zip).
- [Full top stencil ZIP](../hardware/2m/review/M5B-E6R2/fabrication/RF2M-M5B-E6R2_FULL_TOP_STENCIL.zip).
- [Reproduction](../hardware/2m/review/M5B-E6R2/REPRODUCE.md),[SHA inventory](../hardware/2m/review/M5B-E6R2/SHA256SUMS).

150×110mm,140×100mm four-hole pattern,2layers,FR4,1.6mm,1oz,green mask,white
legend,lead-free HASL. Ordinary PTH/NPTH drills and two R1 routed cutouts;
no controlled-impedance service,filled/capped vias,blind/buried vias,embedded
metal or special laminate. Copper-to-cutout≥0.5mm is independently checked.
Keep separate plated/nonplated drill files and complete outline with both
internal loops. Review the actual Gerber/drill consistency audit and file hashes.
The bare-board ZIP has9Gerbers+2drills; stencil ZIP contains full F.Paste and
Edge.Cuts only.0.12mm stencil is the source-joint process basis. It is not a
Q501-only stencil. Via filling/tenting is not a guaranteed solder-wicking remedy.

The independent DFM checker uses actual geometry,mask unions,hole spacing,
foreign copper,slivers and legend openings. Existing and added ordinary0.6/0.3mm vias use0.15mm nominal annuli, retained
as explicit design-margin exceptions relative to preferred0.25mm lands, not a
special manufacturing process or DRC waiver. Component PTH minimum is reported
separately. Standard supplier tolerances still require incoming inspection.
Commercial CAM acceptance/quotation/upload/order are NOT_RUN.

Use the three separate BOMs and assembly drawings. Do not mix BUCK4S/BOOST2S
conversion populations. TRAIN_ONLY omits NORMAL PA/keying parts. Native source,
revision-specific output hashes and physical net-tie IPC aliases are supplied.
No acceptance tag or production release is created. Bare-board evaluation GO
is separate from powered/operational qualification; follow the first-article plan.

All physical RF, thermal, shutdown timing and outdoor qualification remains **NOT_RUN**. No boards or stencils ordered; no hardware energized.
