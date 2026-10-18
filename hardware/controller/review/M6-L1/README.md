# M6-L1 dual-band LoRa CAD closure

Active native sources remain ../../CTRL.kicad_pro, ../../CTRL.kicad_sch and ../../CTRL.kicad_pcb. Electrical/physical copper baseline is M6-C1R1, commit742159d363dd8dd8b8ff653d01238af9a49ef2aa. M6-L1 clarifies optional part/population metadata, unused DIO3 labeling and the 15 mm module body drawing. It retains the RF signal geometry and corrects only a small Hirose underbody ground-fill intrusion; the board revision mark is L1.

Read the [decision](../../../../docs/M6_L1_REVIEW_DECISION.md), [module compatibility](../../../../docs/M6_L1_MODULE_COMPATIBILITY.md), [feed calculation](../../../../docs/M6_L1_ANTENNA_FEED.md), [population contract](../../../../docs/M6_L1_LORA_VARIANTS.md), [sourcing](SOURCING.md), [assembly/qualification](BRINGUP.md) and [reproduction](REPRODUCE.md).

module-22-pin-audit.json and module-pin-matrix.csv cover all terminals. The normalized-module-views.svg is an original dimension reconstruction; LoRa-native-overview.svg and antenna-feed-detail.svg use actual copper/lands/vias. Manufacturer-evidence hashes identify reference downloads; copyrighted full datasheets are linked, not redistributed. The native-preservation and fabrication-equivalence reports distinguish unchanged geometry from changed metadata and byte hashes. The SHA inventory binds final sources and outputs.

Fresh fabrication/ contains the proposed bare-board Gerbers and separate PTH/NPTH drills. Analysis files, annotated views and BOMs are review data. Default native population is NO_LORA; choose the exact base/radio BOM. Both radio options use one PCB. The original M6-C1/R1 directories are preserved.

Gates A–D pass for independent evaluation review. Gate E and earlier controlled electrical commissioning remain NOT_RUN. No acceptance tag, factory CAM/quote, supplier upload, purchase or hardware operation has occurred.
