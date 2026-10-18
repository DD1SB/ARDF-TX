# RF80 V1R1 — standard prototype manufacturing candidate

Open **RF80_V1.kicad_pro** here. The active M4A-V1R1 is a **150 × 110 mm**, two-layer, 1.6 mm / 1 oz standard FR4 candidate with lead-free HASL. It preserves the Si5351–LM5134B–IRF610/BD140 circuit, independent Fox path and controller/protection contracts. The changes concern local THT landings, legend and manufacturing settings.

- [Current engineering decision](../../../docs/M4A_V1R1_REVIEW_DECISION.md)
- [Current review and five-board package](review/M4A-V1R1/README.md)
- [Ordinary finished-hole audit](../../../docs/M4A_V1R1_HOLE_AND_FOOTPRINT_AUDIT.md)
- [Proposed first-evaluation transition](../../../docs/M4A_V1R1_PROTOTYPE_TRANSITION.md)
- Preserved [original M4A-V1 review](review/M4A-V1/README.md) and [original decision](../../../docs/M4A_REVIEW_DECISION.md), baseline 4d2f592. Frozen E2 at 1245023 / m3b-e2 remains unchanged one directory above.

**GO for independent bare-PCB manufacturing review.** The old E2-first restriction remains historical evidence: the V1R1-first proposal requires user review before upload/fabrication approval. No accepted ADR or historical evidence changed. Physical fit, power, protection, RF, thermal, spectrum and endurance tests are all **NOT_RUN**.

FULL and FOX_ONLY are explicit populations of the same PCB. Full omits R228/R348/R349; Fox fits these links and omits the normal PA. Full includes the off-board insulated TH301 sensor. Use current population/placement records for Fox assembly. No acceptance tag, order, upload, assembly, power-up or RF is authorized.

Do not run old derivation/placement scripts on the candidate. They recreate obsolete routing input. Use the dedicated `m4a_v1r1` wrapper and current reproduction instructions; historical exporters would overwrite preserved review data. [Licence and attribution](LICENSES.md).
