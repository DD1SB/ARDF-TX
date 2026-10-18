# RF80-V1R1 — standard-JLCPCB prototype manufacturing review

**Active150×110mm engineering candidate; GO for independent bare-board review only.** No acceptance tag, supplierupload/order or physicalactivity. The first80mprototype transition fromE2 toV1R1 is a proposal awaiting review, not a deleted historical requirement.

Native authority: [project](../../RF80_V1.kicad_pro), [schematic](../../RF80_V1.kicad_sch), [PCB](../../RF80_V1.kicad_pcb), [electricalmanifest](../../RF80_V1.electrical.json). BaselineV1 preserved at4d2f592; E2 at1245023/m3b-e2. Revision/documentation is M4A-V1R1; no disconnectedproject or largerE2board is being released.

- [Decision](../../../../../docs/M4A_V1R1_REVIEW_DECISION.md), [change report](CHANGE_REPORT.md), [manufacturing settings](manufacturing-notes.md).
- [Finished-hole audit](finished-hole-audit.json), [native before/after](finished-hole-comparison.svg), [controller match](controller-compatibility.json), [mechanical/insulation review](mechanical-fit-review.json), [connector and local-copper discussion](CONNECTOR_AND_MECHANICAL.md).
- [ERC](ERC.json), [DRC](DRC.rpt), [nativeDFM](JLCPCB-DFM.json), [coverage](drc-coverage.json), [electrical equivalence](electrical-equivalence.json), [logic](logic-results.json), [verification](verification.md).
- [SchematicPDF](RF80_V1.pdf), [assemblyPDF](assembly.pdf), [bottomassembly](assembly-bottom.pdf), [topcopper](top-copper.svg), [bottomcopper](bottom-copper.svg), actualKiCad [top3D](RF80_V1-3D-top.png), [angled3D](RF80_V1-3D.png), [bottom3D](RF80_V1-3D-bottom.png). Envelope-only models remain labeled, not supplier-fit proof.
- [FULL BOM](BOM-FULL.csv), [FOX_ONLY BOM](BOM-FOX_ONLY.csv), [population](population.csv), [cost/evidence categories](costs.json), [source status](source-status.json).
- **[RF80 five-board fabrication ZIP](fabrication/RF80-V1R1_JLCPCB_5boards.zip)**: onlynineGerbers+twoDRLs. Analysis and final proposed fabrication datasets are separated. [Exportaudit](fabrication-audit.json).
- [Three-board order-readiness matrix](THREE_BOARD_ORDER_READINESS.md): controller andRF2M exports inspectedread-only/copiesbyte-identical. Three separatefive-board items, not acombinedpromotion/panel.
- [Proposed E2-first transition](../../../../../docs/M4A_V1R1_PROTOTYPE_TRANSITION.md), [single-board stagedbring-up](BRINGUP.md), [physicalgateplan](physical-qualification.json), [reproductioncommands](REPRODUCE.md).

ERC/DRC0;unrouted0;parity0;all 401holesexportchecked. No custom process. SupplierCAM/quoteNOT_SUBMITTED. AllphysicalresultsNOT_RUN. File/sourceSHA256 inventory isgeneratedlast; noactualquote or performance result is invented.
