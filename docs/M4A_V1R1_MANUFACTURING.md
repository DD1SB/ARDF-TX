# M4A-V1R1 — standard five-board manufacturing candidate

Date: 2026-10-18. **GO for independent bare-PCB manufacturing review; no upload, quote, purchase or fabrication authorization.** The proposed change from E2-first evaluation still requires explicit review. Open [RF80_V1.kicad_pro](../hardware/80m/production/RF80_V1.kicad_pro), not the older 210 × 160 mm RF80 project.

| Standard order option | Selection |
| --- | --- |
| Quantity / design | Five individual boards / one design; no panel |
| Outline | 150 × 110 mm Edge.Cuts centreline |
| Layers / material | Two / standard FR4 |
| Finished thickness / copper option | 1.6 mm nominal / 1 oz outer copper |
| Mask / legend | Green / white |
| Finish | Lead-free HASL |
| Holes | Ordinary PTH and separate NPTH, standard component-hole tolerance |
| Impedance / special services | None; no press-fit, special drilling, via filling or custom stackup |
| Assembly | Bare boards only; later manual staged population, separately authorized |

The native nominal stackup is two 35 µm copper layers and nominal FR4 metadata. It is **not a custom-core purchase specification**. Finished thickness is nominal and subject to standard tolerance. Starting foil, finished external copper and hole-wall plating are different quantities; selecting 1 oz is not a guaranteed minimum via-wall thickness. This HF design uses no RF controlled-impedance ordering requirement.

Use only [RF80-V1R1_JLCPCB_5boards.zip](../hardware/80m/production/review/M4A-V1R1/fabrication/RF80-V1R1_JLCPCB_5boards.zip) after independent review and explicit upload authorization. Its eleven entries are nine Gerbers and separate PTH/NPTH drills. Do not submit the historical E2 set, the M4A-V1 set, analysis SVGs, drill-map PDFs or a two-up panel. Detailed checksums are in the [review package](../hardware/80m/production/review/M4A-V1R1/README.md).

## Standard capability and engineering margins

The [current JLCPCB capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/) and [pad/via-hole tolerance explanation](https://jlcpcb.com/help/article/difference-and-tolerance-explanation-between-via-and-pad-holes) were reviewed on 2026-10-18. Ordinary component PTH finished-hole tolerance is **−0.08/+0.13 mm**; it must not be replaced with ±0.05 mm press-fit processing. Electrical via holes do not carry a component-insertion-fit guarantee. Lead diagonal, negative hole tolerance and practical clearance are calculated per package in the [hole audit](M4A_V1R1_HOLE_AND_FOOTPRINT_AUDIT.md).

The board retains 0.15 mm minimum signal traces/clearance targets, 354 ordinary 0.60/0.30 mm vias with 0.15 mm nominal rings, and component PTH rings at least 0.25 mm. The existing vias satisfy the ordinary process and are not enlarged indiscriminately. Green 1 oz mask web is 0.10 mm; expansion remains 0.025 mm. Essential silk is at least 1.0 mm high / 0.15 mm stroke / 0.15 mm mask clearance. These are checked on native geometry and final export artwork, not only configured rules. The machine-readable [profile](../hardware/80m/production/review/M4A-V1R1/JLCPCB-standard-profile.json) distinguishes published limits and design margins.

The Gerber Edge.Cuts centreline is exactly X20–170/Y20–130 mm. Its 0.05 mm outline stroke is artwork, not an increase to 150.05 × 110.05 mm finished dimensions. Four 3.2 mm NPTH mounting holes remain on a 140 × 100 mm pattern. There are 397 PTH holes including 354 vias, plus four NPTH; all 401 native hole centres and sizes match the final drills.

## Authorized next-step boundary

[Ordering instructions](https://jlcpcb.com/help/article/instructions-for-ordering) and [copper-weight explanation](https://jlcpcb.com/help/article/jlcpcb-copper-weight) are references, not evidence that this dataset has passed factory CAM. After explicit authorization, check automatic size recognition, two layers, five separate boards, nominal 1.6 mm / 1 oz, lead-free HASL, no premium services, separate PTH/NPTH recognition and standard component-hole compensation. Obtain a real quote and review CAM feedback before separate purchasing approval.

No negotiated process is part of this candidate. Incoming lead measurements, solderability, heatsink insulation, RF/protection qualification and endurance are physical commissioning work, **NOT_RUN**. [Prototype-transition proposal](M4A_V1R1_PROTOTYPE_TRANSITION.md) and [review decision](M4A_V1R1_REVIEW_DECISION.md) define the remaining approvals.
