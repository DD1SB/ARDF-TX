# Three-board prototype manufacturing review

All three ZIPs are isolated five-individual-board datasets. Other designs and their historical exports were inspected read-only; copied entries are byte-identical to their authoritative commits. No supplier upload or quotation occurred.

| PCB | Source | Size mm | ZIP | Qualification |
| --- | --- | --- | --- | --- |
| RF80-V1R1 | M4A-V1R1 candidate; baseline4d2f592 | 150 × 110 | [RF80-V1R1_JLCPCB_5boards.zip](fabrication/RF80-V1R1_JLCPCB_5boards.zip) | NOT_RUN |
| Controller | M6-L1 / d94dabd0e40137dc44b2bb94f3707ad4636ca65f | 100 × 100 | [CTRL_M6-L1_JLCPCB_5boards.zip](three-board-order/CTRL_M6-L1_JLCPCB_5boards.zip) | NOT_RUN |
| RF2M | M5B-E4R1 / 2f9982c1b72cd97ba4dad6c992143032b309cca7 | 180 × 140 | [RF2M_M5B-E4R1_JLCPCB_5boards.zip](three-board-order/RF2M_M5B-E4R1_JLCPCB_5boards.zip) | NOT_RUN |

All: two-layer standardFR4,1.6mm,1oz,green/white,lead-freeHASL,ordinarythroughvias. Five each as separate items; no factory assembly or premium service. Detailed source hashes and CAM questions: [JSON](three-board-order-readiness.json).

RF80 transition from the old E2-first sequence is **PROPOSED**, not approved. Controller and RF2M statuses are inherited independent-review candidates, not transmitter operational approvals. Supplier price/CAM, purchasing and all physical gates are separate.
