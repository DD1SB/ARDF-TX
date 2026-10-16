# M5B-E2 fabrication review

**Review and quote preparation only. Five bare boards, one initially populated in stages. No files were sent to a fabricator.** Only the final `review/M5B-E2/gerbers/` set is a manufacturing candidate. Comparison Gerbers under `copper-investigation/` must never be ordered.

| Item | Requirement / status |
| --- | --- |
| Outline | 180 × 140 mm; x20–200 / y20–160 mm; one routed rectangle. No customer panel outline. Supplier rails/tooling outside this outline require review. |
| Construction | Two copper layers, FR4, ENIG proposed, green LPI mask on both sides, white legend. No blind/buried vias or impedance-control premium assumed. |
| Finished board | Nominal 0.80 mm. Overall ±0.10 mm tolerance does not define the RF dielectric spacing. |
| Dielectric | Design model 0.640 mm between facing copper surfaces. Request 0.640 ±0.050 mm and named laminate/Dk information near VHF. Supplier confirmation pending. |
| External copper | **Finished** 70 µm per side, initial analysis window 60–80 µm. State finished thickness after plating, not simply starting foil weight. |
| Mask | CAD nominal 10 µm per side; actual supplier value pending. Expansion 0; minimum web 0.10 mm. Preserve the thermal window and source-via tents. |
| Track / clearance / connection | Minimum 0.15 / 0.15 / 0.15 mm. Matching lines 1.102 mm. No generic CAM resizing of RF copper. |
| Ordinary vias | 0.60 mm land / 0.30 mm nominal finished PTH; nominal annulus 0.15 mm. Confirm drill compensation and registration allowance. |
| Other constraints | Copper-edge ≥0.50 mm; hole-to-copper and hole-to-hole rules 0.25 mm. Six 3.20 mm NPTH mounting holes. |
| Critical finished holes | J101 1.10 mm; J501 center 1.50 mm / grounds 1.70 mm. All sizes and counts are in the drill report and stackup-mechanical.json. |
| Requested hole tolerances | PTH ±0.08 mm / NPTH ±0.05 mm where supported. Compare maximum lead diagonal against minimum finished hole. |
| Legend | Actual minimum visible text height 0.80 mm, text stroke 0.12 mm, graphic stroke 0.10 mm. Confirm the supplier can retain readable polarity/orientation marks; do not silently erase them. |
| Paste | Initial 100 µm stencil proposal; segmented PD source paste and isolated RNW6/7/8 apertures. Requires assembly review. |
| Bare-board E-test | Use RF2M-physical-netties.ipc; TL copper intentionally merges logical nets. Retain RF2M-logical.ipc for schematic review. |

Starting copper is foil before plating. Finished outer copper includes plating. The core dielectric is neither the finished board thickness nor an automatically fixed fraction of it. CAD's 0.64 + 0.07 + 0.07 + 0.01 + 0.01 = 0.80 mm is a model, not a supplier guarantee. ENIG and solder-mask effects are omitted from the simple microstrip model.

Ordinary prototype services offer plausible manufacturing routes, but no supplier has accepted this combined specification. [PCBWay's capability table](https://www.pcbway.com/capabilities.html) lists 0.8 mm/70 µm options, 0.15 mm annuli and PTH ±0.08 mm / NPTH ±0.05 mm. Confirm the combined 0.15 mm/70 µm process, mask webs and core before ordering. [JLCPCB's copper guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight) specifies a 0.16 mm minimum for 2 oz: this 0.15 mm board must not be assumed compatible with that standard service. [Its thickness table](https://jlcpcb.com/capabilities/pcb-capabilities/) gives ±0.1 mm overall for 0.8 mm, which does not establish core spacing. These are read-only capability observations, not quotations or correspondence.

RF geometry remains as in E1: **1.102 mm width**, assumed Dk 4.3, dielectric 0.64 mm and finished copper 0.07 mm. The retained quasi-static model gives approximately 50.000 Ω. TL603–609 physical lengths are **6.23 / 6.62 / 5.80 / 2.20 / 11.00 / 12.40 / 2.00 mm**. Their calculated 144.7 MHz phases are in `transmission-lines.csv`; the maximum modeled change from the original ST substrate is approximately 0.0122°. This is not measured matching. Pads, mask, package parasitics, losses and actual returns remain physical qualification items.

`stackup-sensitivity.csv` sweeps dielectric 0.59–0.69 mm, Dk 4.1–4.5, copper 60–80 µm and etched width 1.052–1.152 mm. `alternative-stackup-proposals.csv` provides concrete proposed widths for other dielectric spacings and length scaling by √(effective-Dk-E1/effective-Dk-new). No proposal is applied. If a supplier cannot provide a compatible stack, review these local corrections before generating another revision. A blind substitution of 1.6 mm FR4 is prohibited.

The quote request must confirm the laminate/core/Dk and finished copper; 0.15 mm features and annuli; 0.10 mm mask webs; finished holes; source-via tents and segmented paste; ENIG; electrical testing with aliases; panel handling; no unsolicited RF CAM edits; net cost, shipping and lead time. No special tolerance or process premium is booked as zero. A supplier unable to confirm these requirements is unsuitable for ordering this revision.

The native ground-polygon comparison in `RF-ground-geometry.json` finds zero symmetric-difference area in the RF core F.Cu window x49–190/y43–63 mm and bottom RF-return window x49–190/y43–65 mm. All RF tracks and embedded footprint geometry are identical to E1. Control-region fill updates are outside those windows. This verifies CAD preservation, not RF performance.
