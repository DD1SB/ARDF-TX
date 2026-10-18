# M6-C1R1 controller fabrication-review candidate

Active native sources are ../../CTRL.kicad_pro, CTRL.kicad_sch and CTRL.kicad_pcb in the controller directory. The inventory hashes those files and all local libraries. This package is regenerated from R1; review/M6-C1 remains immutable baseline evidence.

Read [decision](../../../../docs/M6_C1R1_REVIEW_DECISION.md), [input correction](../../../../docs/M6_C1R1_INPUT_PROTECTION.md), [USB assessment](../../../../docs/M6_C1R1_USB_ESD_REVIEW.md), [validation](../../../../docs/M6_C1R1_ELECTRICAL_VALIDATION.md), [changes](change-and-preservation-audit.json), [bring-up](BRINGUP.md), [costs](COST_DELTA.md), [manufacturing](MANUFACTURING.md) and [reproduction](REPRODUCE.md).

Only fabrication/ contains the proposed Gerbers/drills. CTRL.pdf, copper/assembly views, actual KiCad3D PNGs, per-population placements/BOMs and logical/physical IPC files are fresh exports. Analysis/model JSONs are review evidence, not extra fabrication layers. No routing-session or abandoned construction geometry is part of this dataset. Bottom assembly is common to the four base populations; LoRa is HOLD/DNP.

Gate A/B local checks pass; Gate C is GO for independent five-bare-board review only. Gates D/E remain NOT_RUN. Supplier quote/CAM, purchasing, manufacture and power-up require separate authorization. No acceptance tag or manufacturing release exists.

SHA256SUMS and inventory.json bind the final dataset and native/reproduction sources. Fresh export timestamps can legitimately change file hashes; rerun the inventory after regeneration. Native geometry, pad/net and drill/Gerber consistency are checked independently.
