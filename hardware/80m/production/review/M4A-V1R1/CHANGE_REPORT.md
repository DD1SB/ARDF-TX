# V1 → V1R1 engineering changes

Baseline preservation commit **4d2f592** records the previously untracked original M4A-V1 project/tools/evidence before edits. Frozen E2 is 1245023 / m3b-e2. Existing M6-L1 is d94dabd0; RF2M-E4R1 is 2f9982c1. The 1,421 read-only evidence files in frozen-inputs.json remain byte-identical, plus every tracked E2 hardware file checked against its commit.

- Revised six local through-hole landings: J101 1.4, J502 1.3, Q402/Q403 1.4, J301 1.9, J401 1.3 mm finished nominal. J502 land width1.7→1.9mm. New per-maker footprint IDs/filters in native symbols/sheets/manifest, same MPNs and nets. No historical footprint or review evidence rewritten.
- Moved 812 small footprint graphic items and small reference text to Fab/assembly layers. Added26 essential≥1mm/0.15mm white marks. Project-local artwork library overlays keep native-vs-library comparison clean; no DRC suppression.
- Explicit standard 1.6mm/1oz/green/white/lead-free-HASL native metadata, no constrained custom dielectric. Mask expansion0.025mm/web0.10mm retained.
- Outline, mounting holes, component centres/rotations, all signal tracks/vias, values, full/Fox links and functional nets unchanged. Fresh zone fill only changes material clearance locally atJ502; numerical polygon roundoff quantified separately.
- Added actual native DFM, hole-fit, interface, silkscreen/Gerber, archive and source/cost tooling. No factory CAM, quote, physical fitting, assembly or RF measurement claimed.

[Detailed lead-fit](../../../../../docs/M4A_V1R1_HOLE_AND_FOOTPRINT_AUDIT.md), [DFM](../../../../../docs/M4A_V1R1_DFM_REVIEW.md), [manufacturing options](../../../../../docs/M4A_V1R1_MANUFACTURING.md) and [transition proposal](../../../../../docs/M4A_V1R1_PROTOTYPE_TRANSITION.md). Only the proposal asks to replace the E2-first sequence; historical M4A decisions remain unchanged.
