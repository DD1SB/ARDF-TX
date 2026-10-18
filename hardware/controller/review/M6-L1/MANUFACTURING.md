# M6-L1 fabrication and population handoff — review only

Use the freshly exported files in `fabrication/`, not the diagrams or analysis
files. They belong to the active `../../CTRL.kicad_pcb`; `inventory.json`
binds the exact native source hashes. `fabrication-equivalence.json` identifies
the local difference from M6-C1R1.

| Web-order option | Selection |
|---|---|
| Quantity / size | Five bare boards / 100 × 100 mm |
| Construction | Two-layer standard FR4, 1.6 mm, 1 oz |
| Mask / legend | Green / white |
| Finish | Standard lead-free HASL |
| Via treatment | Ordinary unfilled plated through-vias |
| Impedance / stack-up | No controlled impedance, no custom stack-up |
| Assembly | Manual/staged; not manufacturer-assembly-dependent |

No physical fabrication, supplier upload, quote or CAM acceptance has occurred.
Published capability and locally checked DFM are distinct from factory acceptance.
Recheck current ordinary options before any separately authorized order.

`JLCPCB-standard-profile.json` separates vendor limits from project margins.
Actual native minima are 0.15 mm routed width/clearance, 0.25 mm via and PTH
annular rings, ordinary 0.80/0.30 mm vias, and a conservative 0.5 mm copper/edge
margin. The geometry checker checks copper, mask bridges, holes, pad-to-hole
spacing, legend and board construction, not only configured KiCad rules.
Current ERC/DRC errors/warnings, unrouted and parity counts are all zero. No
exclusions; only the inherited unused tuning-profile category is ignored.

Hirose's complete F.Cu underbody no-traces region is now enforced. Its intended
SIG land is allowed; separate native-polygon checks reject other copper in it.
Bottom GND remains continuous. Ordinary mask is not a guaranteed via plug.
There are no premium filled vias, RF laminates or factory matching services.

Select one of the twelve explicit `BOM-<base>_<radio>.csv` files. NO_LORA
leaves U70/J7/C70/C71/R70/R71 absent. Either fitted radio option uses all six,
with its exact band-specific U70 and external antenna. All use the same PCB;
do not order different copper for 433/868 MHz. Default native 3D/assembly data
shows the DNP radio state; the two UNIVERSAL_LORA assembly drawings/placements
are also supplied. Other base-specific options use their complete BOM and
the identical radio placement.

Read `BRINGUP.md` before selecting a stencil/process. For the documented manual
build, mask J7 apertures and hand-solder its three contacts; full-pad native
paste is not claimed to equal Hirose's reduced metal-mask recommendation.
Castellated U70 lands are accessible; profile and inspect the first assembly.
Actual incoming dimensions and module height remain physical checks. No hidden
centre-pad or special via process is required.

Bare-board planning allowances remain unquoted: €9/€14/€24 for batches of
5/10/20, excluding freight/VAT, plus an unquoted €8–20 standard stencil allowance.
These are inherited estimating formulas, not JLCPCB prices. Antenna, pigtail,
mounting, cells, cables, labor and physical RF qualification are separate.
