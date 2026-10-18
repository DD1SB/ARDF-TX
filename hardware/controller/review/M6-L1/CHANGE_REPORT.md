# M6-C1R1 to M6-L1

Comparison baseline: `742159d363dd8dd8b8ff653d01238af9a49ef2aa`.
There is no acceptance tag. Original M6-C1/R1 review evidence is unchanged.

| Item | Implemented change | Electrical consequence |
|---|---|---|
| U70 pads | None: all 22 numbered lands retained | Same SPI, supply, control, ANT and ground mapping |
| U70 body | F.Fab 15 × 16.7 → 15 × 15 mm | Corrects body drawing; original courtyard retained |
| U70 identity | Explicit distributor TR8 default, TR4 alternate; both manufacturer ZTR PDFs verified | NO_LORA remains default DNP |
| U70.8 | Generic IO symbol name clarified to DIO3 | Still unused configurable IO, no functional connection change |
| J7 lands | None | Hirose nominal SIG/GND pattern verified |
| J7 top keep-out | X-min 98.425 → 98.315 mm; Y 27.55–29.45 mm, X-max 100.515 mm | Removes unintended GND strip within full 2.20 × 1.90 mm maker no-traces rectangle |
| J7 keep-out pad rule | Permits the intended Hirose SIG land, independently audits foreign copper | Tracks/vias/pours remain prohibited in the region |
| RF signal route | None: 5.25 × 0.45 mm | No reroute, tuning network, signal via or new stub |
| PCB legend | C1R1 → L1 | Revision traceability only |
| Schematics / manifest | Current option notes, MPN, populations and source evidence | No functional netlist change; only unused U70.8 net alias changes |
| Host fixtures | Trusted band/antenna/policy contract and six tests | No target driver or radio transmission implemented |

Native polygon subtraction finds **0.024722676988 mm²** of F.Cu GND removed,
zero added copper and zero B.Cu change. All differences are inside
X 98.0–100.9 / Y 27.2–29.8 mm. The intended signal pad, nearby ground lands,
local ground stitch and bottom reference remain intact. The change removes
copper already prohibited by Hirose, rather than weakening RF signal clearance.
See [before/after native polygons](Hirose-keepout-comparison.svg),
[native preservation](native-preservation.json) and
[full-area independent audit](UFL-landpattern-audit.json). The latter samples
10,075 non-SIG positions and checks actual foreign pad/track/via polygons.

All track/via objects and all 704 numbered pad instances are geometrically
identical to R1. Including unnumbered mechanical contacts, 715 lands are
compared. All footprint positions/rotations, mask/paste, mounting holes,
connectors, physical GPIOs and functional net assignments remain.

Freshly generated Gerbers confirm identical B.Cu, mask, paste, underside
silkscreen and outline drawing streams after removal of provenance attributes.
F.Cu changes locally as above; F.Silkscreen changes the revision marking.
PTH/NPTH tool and hole commands are identical; their timestamp comments differ.
Raw file hashes are recorded without claiming byte equivalence.

The RF model at the extraction resolution gives the same nominal results before
and after the small keep-out correction. This is a model comparison, not proof
of unchanged physical RF performance. Local return inductance, connector/module
parasitics and ordinary-material variation are disclosed in the RF report.

No base BOM addition or special fabrication process is introduced. Twelve
orthogonal base/radio BOMs replace the old unresolved-radio allowance; price
observations, FX assumptions and unquoted material remain separate. RF80,
RF2M, RTC, pack-ID, USB, safe gating and base standalone operation are unchanged.
