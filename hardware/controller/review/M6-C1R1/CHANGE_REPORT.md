# M6-C1 to M6-C1R1

Baseline31ac3eb4c4569e710472ecab86baec6d9b7c9399 is preserved. Original native schematic and PCB are available through that Git revision; the preserved [M6-C1 schematic PDF](../M6-C1/CTRL.pdf) and [R1 PDF](CTRL.pdf) provide the complete before/after circuits. The independent audit verifies all693 baseline pads, all other existing footprint locations, all USB conductors and111 original review files.

| Position | M6-C1 | M6-C1R1 |
|---|---|---|
|R3|10k fromV3V3 toPACK_ID_RAW|27k fromreverse-isolatedPACK_PROT excitation toPACK_ID_RAW; relocated to entry area|
|D22|absent|BAS116,235,1A/3K,2NC, excitation isolation|
|R8|absent|180k fromRAW toSAFE|
|R9|absent|33k SAFE-to-GND|
|D23|absent|Nexperia BAT54H,115,1K SAFE/2A GND, negative clamp|
|U21.5|PACK_ID_RAW|PACK_ID_SAFE|
|C25.1|PACK_ID_RAW|PACK_ID_SAFE; remains upstream of U21|
|R19|absent|100k PACK_ID_ADC-to-GND|
|U3/C10/USB power path|local3.3V steering reference|unchanged, justified review decision|

No new active IC or changed connector. External passive codes10k/22k remain, but host excitation/ADC decoding explicitly changes to frontend revision2. Do not connect an active3.3V ID accessory to this resistor-code input. PACK_ID_RAW now remains near the pack entry; the established long route is reused as protected SAFE. The exact final component sides/coordinates and land geometry are in change-and-preservation-audit.json. All existing footprints except R3 retain their locations.

The five new purchased positions plus relocated R3 form **six underside positions in total**: R3,D22,R8,R9,D23,R19. Purchased part count rises by five. The bottom assembly view is the authority for placement. All are small standard packages, within the prior10mm underside support envelope. No mounting-hole, RF connector, USB connector or outline movement. PCB process remains100×100mm standard2L1.6mm1oz green/white/lead-free HASL.

GPIOs, both isolated I²C branches, RTC/backup, mutually exclusive control banks, RESET/PACK_PRESENT/INIT gating, progress ownership, RF preparation/slot/key distinctions, RF module populations and LoRa HOLD remain. The firmware foundation adds the versioned interval ID reader and fresh-ID fault handling; it remains host code, not deployed firmware.

The native package/pad audit covers current geometry. D22 uses the existing SOT23 landing, whose1.475×0.6mm lands cover the manufacturer terminals. D23 uses the existing SOD123F landing:1.1×1.1mm pads at±1.4mm cover the package terminal span with approximately0.15mm toe allowance. This is a compatible stock land, not a claim that it duplicates every dimension of the larger manufacturer recommended solder land. Confirm wetting/fit during the first assembly. Never substitute onsemi's SOD323 BAT54H solely by name.

No RF80/RF2M/M4A source or historical tag changes. No files submitted, parts purchased or hardware tested.
