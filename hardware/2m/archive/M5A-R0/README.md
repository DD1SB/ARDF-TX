# RF2M — M5A-R0 electrical evaluation candidate

**NOT RELEASED. No PCB, fabrication, purchasing, assembly or RF activation is authorized. All physical tests NOT_RUN.**

Open [RF2M.kicad_pro](RF2M.kicad_pro) in KiCad10. The [complete schematic PDF](review/M5A-R0/RF2M.pdf) and [review decision](../../docs/M5_2M_REVIEW_DECISION.md) explain open RF, power and package conditions. RF80/M4A files are unchanged.

Implemented: local Si5351, filtered single-MMIC drive, PD55008-E final, ST D45H11/BD139 series sine AM, exclusive2S-boost/4S-buck supply populations, captured hardware ARM/lease/fault gating, separate3.3 V-onlyµW training branch. No local MCU/RTC or RF power detector. Functional RF terminal symbols and empty critical footprints are deliberately OPEN, not fake qualified land patterns.

The default schematic population is full2S. The [itemized variant BOM](review/M5A-R0/RF2M_BOM.csv) governs BOOST2S,BUCK4S andTRAIN_ONLY. Population fields and R101/R807/R809 substitutions must be honored. TRAIN_ONLY fits R517/R518/R519 and omits U207/C208 and all normal power parts. These are assembly definitions, not evidence that an assembled variant works.

Reproduce from repository root, using the actual tools installed here:

```sh
/usr/bin/python3 tools/m5_freeze.py
/usr/bin/python3 tools/m5_2m_design.py
kicad-cli sch export netlist --format kicadxml --output hardware/2m/review/M5A-R0/RF2M.net.xml hardware/2m/RF2M.kicad_sch
kicad-cli sch erc --format json --output hardware/2m/review/M5A-R0/erc.json hardware/2m/RF2M.kicad_sch
kicad-cli sch export pdf --output hardware/2m/review/M5A-R0/RF2M.pdf hardware/2m/RF2M.kicad_sch
/usr/bin/python3 tools/m5_2m_verify.py
/usr/bin/python3 tools/m5_2m_analysis.py
/usr/bin/python3 tools/m5_2m_costs.py
/usr/bin/python3 tools/m5_2m_document_tables.py
ngspice -b analysis/m5_2m/am_loop_behavioral.cir
/usr/bin/python3 tools/m5_2m_sim_report.py
/usr/bin/python3 tools/m5_2m_finish.py
```

The generator rebuilds native schematic/library/manifest files; preserve reviewer edits before regeneration. The default ngspice deck writes only the stated analysis output. Never regenerate RF80 to update this project. The final finish script checks documents and artifacts; it does not qualify hardware or create a PCB.

KiCad library material is copied/flattened from the installed official libraries, including explicit manufacturer-specific pin remaps. See the supplied [KiCad library CC-BY-SA4.0 license and design exception](LICENSE-KICAD-SYMBOLS.md). The new circuit/analysis is project-authored, with primary reference attribution in [M5 sources](../../docs/M5_2M_SOURCES.md). No proprietary third-party schematic/PCB, firmware or PDF was copied into this project. Empty footprints have not been filled with unverified substitute package geometry.
