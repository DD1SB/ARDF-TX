# M6-L1 module and connector compatibility

The existing single U70 landing is nominally compatible with **SX1262TR4-GC / SX1262ZTR4-GC** and **SX1262TR8-GC / SX1262ZTR8-GC**. This is a documented supplier alias, not an inference from the SX1262 chip name. LCSC C42381681 links a manufacturer ZTR4 V2.0 PDF byte-identical to the official download. C42381682 links ZTR8 V2.0, also byte-identical to Silicontra's newer official download. The requested ZTR8 V1.0 has the same pin/land topology. Revision V2.0 versus V1.0 is a document revision; no TR-prefix-specific alternate package is indicated. The source URLs and exact downloaded hashes are in [manufacturer-evidence.json](../hardware/controller/review/M6-L1/manufacturer-evidence.json).

Normalize **TR4 V2 and TR8 V2 by a 90° counterclockwise rotation**, with no reflection, to the native F.Cu/top-side view: pin 1 lower-left, pins 1–11 left-to-right on the lower row, pins 12–22 right-to-left on the upper row. TR8 V1 is already drawn in that orientation. The older blank outline alone does not explicitly label its viewing side; the later component-side/pin-function drawings supply the cross-check. A bottom PCB/service view is mirrored for viewing only, not a different footprint. See [normalized drawing](../hardware/controller/review/M6-L1/normalized-module-views.svg).

| Dimension | Manufacturer evidence | Implemented carrier land |
|---|---|---|
| Body | 15 × 15 mm, no mechanical tolerance or height specified | F.Fab corrected from 15 × 16.7 to 15 × 15 mm; position unchanged |
| Terminal count / pitch | 22 / 1.27 mm | All 22 verified; 1.27 mm |
| Terminal width | 0.80 mm nominal | 0.80 mm copper width |
| Terminal depth | 1.37 mm nominal | 2.20 mm land length; 1.35 mm nominal inner overlap, 0.85 mm outer toe |
| First terminal offset | 1.12 mm callout | First centre X = −6.38 mm; last +6.32 mm |
| Row spacing | Body outer edges 15 mm; no recommended carrier pad-centre spacing | Pad centres Y = ±7.25 mm, separation 14.50 mm |
| Hole / castellation | Illustrated, diameter/tolerances not dimensioned | No carrier drilled holes or via-in-pad |
| Mask / stencil | Not prescribed by Silicontra | Mask expansion 0.03 mm, nominal mask web 0.41 mm; standard paste lands |
| Assembly clearance | Not prescribed | Conservative existing 16 × 18.1 mm courtyard retained |

Ten pitches plus twice 1.12 mm equal 14.94 mm, not exactly 15 mm: a 0.06 mm drawing/rounding residual. The carrier's 0.03 mm row-centroid offset is retained, rather than inventing a tighter package tolerance. The 14.50 mm number is **our carrier land placement**, not a manufacturer-specified terminal-centre distance. First incoming modules must be checked against these dimensions and pin 1 before soldering. Absence of manufacturer tolerances remains explicit; it is not evidence of a different TR4/TR8 package.

All 22 native pad numbers, nets and functions pass [the pin matrix](../hardware/controller/review/M6-L1/module-pin-matrix.csv). Pins 6/7/9 are NC. Pin 8 is **DIO3, unused configurable IO**, with a no-connect usage marker; its old generic IO label is clarified to DIO3, not reclassified as a required NC. No external TCXO driven from DIO3 is fitted. Pins 5/10 carry DIO1/BUSY, 14/15/16/17 are SCK/MISO/MOSI/NSS, 18 reset, 21 antenna; all specified ground contacts and VCC 13 remain.

J7 remains **Hirose U.FL-R-SMT-1(10)**. Its nominal recommended PCB pattern is verified from Hirose's drawing/catalog: signal 1.05 × 1.00 mm at (−1.525, 0), ground 2.20 × 1.05 mm at (0, ±1.475), in the native rotated orientation. The ground separation derives from the 4.00/1.90 mm outer/inner pattern dimensions. Native rounded corners are retained; these are ordinary land shapes, not a claim that the maker specifies those radii. The maker uses SIG/GND terminology; carrier pad numbers 1 and duplicated 2 map those contacts explicitly. The underbody top-copper keep-out is corrected to the full 2.20 × 1.90 mm rectangle, permitting the explicitly intended SIG land. The old 0.11 mm trimming left unintended GND fill; it is removed. Bottom ground remains. Solder mask over the insulating underbody is allowed; unnecessary exposed-mask windows are not added.

The historical Hirose catalog explicitly includes (10), 2500/reel. The current series catalog corroborates the pattern, while newer packing options differ. Mouser's exact (10) listing offers individual cut tape, MOQ 1: a full reel is not required. The (01) bag version uses the same landing but its observed MOQ 100 is less practical here; no substitution is needed. Sources and procurement limitations are in [SOURCING.md](../hardware/controller/review/M6-L1/SOURCING.md).

Copper lands, pitch, RF signal feed, solder mask, paste and drills are retained. A narrow top-ground strip inside the full Hirose no-traces rectangle is removed by a localized keep-out correction. Bottom ground and the ground stitch remain. The body drawing, optional-population/symbol metadata and PCB revision legend also change. These are CAD compatibility findings; actual module identity, solder fit and RF performance remain physical acceptance tasks.
