# M3A component workbook

Date: 2026-10-14. EUR net. **Candidate, no ordering authorization.** Estimates are unquoted; observed rows retain index/date/localization limits. Repeated MPN order quantities are purchase pools: sum line_per_unit_eur, never repeated ordered_mpn.

| Scope | 6 EUR/unit | 10 | 20 | Observed / estimate at ten |
| --- | ---: | ---: | ---: | --- |
| Full module components | 28.54 | 25.35 | 25.14 | 9.75 / 15.60 |
| Foxoring-only components | 11.61 | 10.55 | 10.53 | 4.31 / 6.25 |
| RF final transistor alone | 1.11 | 0.62 | 0.62 | 0.62 / 0.00 |
| RF power stage: final + gate links/bleed + transformer | 2.18 | 1.61 | 1.61 | 0.63 / 0.98 |
| Normal stage + drive/shaper/filter/supply/input and output hardware | 16.12 | 14.16 | 14.03 | 5.47 / 8.69 |
| Incremental NORMAL population; shared circuits excluded | 17.03 | 14.78 | 14.63 | 5.52 / 9.26 |

Full scope includes all populated PCB connectors. Excludes bare PCB, sinks/insulators, battery, antenna accessories, wiring/harness mates, enclosure, charging, labor and shared instruments; these are separately budgeted in [BOM review](M3_80M_BOM.md).

| Group / full module | 6 | 10 | 20 |
| --- | ---: | ---: | ---: |
| connectors | 1.90 | 1.88 | 1.88 |
| source | 2.27 | 1.79 | 1.79 |
| protection | 3.85 | 3.53 | 3.53 |
| normal_shaper | 1.34 | 1.02 | 1.00 |
| fox | 2.99 | 2.86 | 2.84 |
| normal_supply | 4.54 | 3.96 | 3.92 |
| normal_driver | 2.67 | 2.12 | 2.08 |
| decoupling | 0.56 | 0.56 | 0.56 |
| interlocks | 2.90 | 2.60 | 2.50 |
| supply | 0.90 | 0.90 | 0.90 |
| normal_final | 1.11 | 0.62 | 0.62 |
| normal_filter | 3.51 | 3.51 | 3.51 |

| Refs | Value; MPN | Footprint | Source / supplier code / MOQ | Evidence / stock | Unit EUR 6 / 10 / 20 | Full row EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | ---: | ---: |
| C101, C102, C202, C203, C210, C211, C212, C220, C221, C222, C223, C230, C231, C232, C233, C303, C310, C313, C314, C322, C323, C401, C451, C502 | 100n; CC0603KRX7R8BB104 | Capacitor_SMD:C_0603_1608Metric | [source](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D); Mouser 603-CC603KRX7R8BB104; MOQ1 | OBSERVED_M2; 20401272 newer EU index; DE20582958 | 0.0240 / 0.0240 / 0.0240 | 0.576 / 0.576 / 0.576 |
| C103, C201, C402, C501 | 1u; CC0805KKX7R9BB105 | Capacitor_SMD:C_0805_2012Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0800 / 0.0800 / 0.0800 | 0.320 / 0.320 / 0.320 |
| C301, C302 | 10u35; C3225X7R1V106M250AC | Capacitor_SMD:C_1210_3225Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.4500 / 0.4500 / 0.4500 | 0.900 / 0.900 / 0.900 |
| C304, C305, C403 | 22u25; GRM32ER71E226KE15L | Capacitor_SMD:C_1210_3225Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.4500 / 0.4500 / 0.4500 | 1.350 / 1.350 / 1.350 |
| C306, C321 | 1n; CC0603JRNPO9BN102 | Capacitor_SMD:C_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0400 / 0.0400 / 0.0400 | 0.080 / 0.080 / 0.080 |
| C311, C312, C320, C517 | 10n; CC0603KRX7R9BB103 | Capacitor_SMD:C_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0350 / 0.0350 / 0.0350 | 0.140 / 0.140 / 0.140 |
| C410, C510 | 470n; C3216X7R2A474K160AB | Capacitor_SMD:C_1206_3216Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.2200 / 0.2200 / 0.2200 | 0.440 / 0.440 / 0.440 |
| C411, C415, C511, C515 | 1000p; C0805C102J1GACTU | Capacitor_SMD:C_0805_2012Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1000 / 0.1000 / 0.1000 | 0.400 / 0.400 / 0.400 |
| C412, C416, C512, C516 | 100p; C0805C101J1GACTU | Capacitor_SMD:C_0805_2012Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1000 / 0.1000 / 0.1000 | 0.400 / 0.400 / 0.400 |
| C413, C513 | 1800p; C0805C182J1GACTU | Capacitor_SMD:C_0805_2012Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1200 / 0.1200 / 0.1200 | 0.240 / 0.240 / 0.240 |
| C414, C514 | 91p; C0805C910J1GACTU | Capacitor_SMD:C_0805_2012Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1200 / 0.1200 / 0.1200 | 0.240 / 0.240 / 0.240 |
| D201, D202, D451, D501 | BAT54WS-7-F; BAT54WS-7-F | Diode_SMD:D_SOD-323 | [source](https://www.diodes.com/datasheet/download/BAT54WS.pdf); OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1000 / 0.1000 / 0.1000 | 0.400 / 0.400 / 0.400 |
| D301 | SS34; SS34-E3/57T | Diode_SMD:D_SMC | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1800 / 0.1800 / 0.1800 | 0.180 / 0.180 / 0.180 |
| D302 | SMBJ17A TVS; SMBJ17A | Diode_SMD:D_SMB | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.3500 / 0.3500 / 0.3500 | 0.350 / 0.350 / 0.350 |
| F301 | 1.5 A fast / 32V; Littelfuse 046701.5NR | Fuse:Fuse_1206_3216Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.3000 / 0.3000 / 0.3000 | 0.300 / 0.300 / 0.300 |
| J101 | IDC16 controller; Wurth 61201621621 | Connector_IDC:IDC-Header_2x08_P2.54mm_Vertical | Unquoted; manufacturer/supplier check OPEN; Wurth/Mouser OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.6000 / 0.6000 / 0.6000 | 0.600 / 0.600 / 0.600 |
| J301 | RAW protected pack; B2P-VH(LF)(SN) | Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical | [source](https://www.jst-mfg.com/product/pdf/eng/eVH.pdf); Mouser 306-B2P-VHLFSN; MOQ1 | OBSERVED_M3; 108526 indexed EUR MOQ1 | 0.1380 / 0.1150 / 0.1150 | 0.138 / 0.115 / 0.115 |
| J401 | NORMAL 50ohm reference; 1727010 | TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1-2-3.81_1x02_P3.81mm_Horizontal | [source](https://www.phoenixcontact.com/en-us/products/pcb-terminal-block-mkds-1-2-381-1727010); Phoenix/TME/DigiKey 1727010; distributorcode OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 1.0000 / 1.0000 / 1.0000 | 1.000 / 1.000 / 1.000 |
| J502 | FOX ONLY / compact; B3B-XH-A(LF)(SN) | Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical | [source](https://www.jst-mfg.com/product/pdf/eng/eXH.pdf); Mouser 306-B3BXHALFSNP; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1600 / 0.1600 / 0.1600 | 0.160 / 0.160 / 0.160 |
| L301 | 10 uH >=3 A; SRP7050TA-100M | ARDF_TX:SRP7050TA | [source](https://www.bourns.com/docs/product-datasheets/srp7050ta.pdf); Mouser 652-SRP7050TA-100M; MOQ1 | OBSERVED_M3; CurrentEURindex; exactstocknumberOPEN | 0.9630 / 0.7920 / 0.7920 | 0.963 / 0.792 / 0.792 |
| L410, L411 | 2.7 uH / 20T T60-2; Micrometals T60-2 + AWG24 Cu | ARDF_TX:T60_2_20T | [source](https://datasheets.micrometals.com/T60-2-DataSheet.pdf); TME T60-2; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.8500 / 0.8500 / 0.8500 | 1.700 / 1.700 / 1.700 |
| L510, L511 | 2.7uH +/-5%; 78F2R7J-RC | ARDF_TX:78F_Axial | [source](https://www.bourns.com/docs/product-datasheets/78f_series.pdf); DigiKey/Mouser OPEN; exactSKU78F2R7J-RC; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.3000 / 0.3000 / 0.3000 | 0.600 / 0.600 / 0.600 |
| Q201, Q301, Q302, Q401, Q405, Q404, Q406, Q502 | DMN2056U-7; DMN2056U-7 | Package_TO_SOT_SMD:SOT-23 | [source](https://www.diodes.com/datasheet/download/DMN2056U.pdf); Mouser 621-DMN2056U-7; MOQ1 | OBSERVED_M3; 95248 indexed14Oct; cuttapeMOQ1 | 0.1470 / 0.1470 / 0.1280 | 1.176 / 1.176 / 1.024 |
| Q402 | IRF610PBF-BE3; IRF610PBF-BE3 | Package_TO_SOT_THT:TO-220-3_Vertical | [source](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567); Farnell 4853567; MOQ1 | OBSERVED_M2; 614 in Farnell DE index (about 2-month-old cache); no reservation | 1.1100 / 0.6220 / 0.6220 | 1.110 / 0.622 / 0.622 |
| Q403 | BD140 / ST; BD140 | Package_TO_SOT_THT:TO-126-3_Vertical | [source](https://www.st.com/resource/en/datasheet/bd140.pdf); Mouser 511-BD140; MOQ1 | OBSERVED_M3; STActive;MouserDEindexed5060;basketOPEN | 0.5850 / 0.2640 / 0.2640 | 0.585 / 0.264 / 0.264 |
| Q501 | MMBT3906,215; MMBT3906,215 | Package_TO_SOT_SMD:SOT-23 | [source](https://assets.nexperia.com/documents/data-sheet/MMBT3906.pdf); OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1000 / 0.1000 / 0.1000 | 0.100 / 0.100 / 0.100 |
| Q503, Q504 | MMBT3904,215; MMBT3904,215 | Package_TO_SOT_SMD:SOT-23 | [source](https://assets.nexperia.com/documents/data-sheet/MMBT3904.pdf); OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1000 / 0.1000 / 0.1000 | 0.200 / 0.200 / 0.200 |
| R101, R102, R407 | 4.7k; RC0603FR-074K7L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.090 / 0.090 / 0.090 |
| R103, R506 | 100k; RC0603FR-07100KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.060 / 0.060 / 0.060 |
| R110, R111, R112, R113, R114, R115, R116, R117, R118, R202, R203, R301, R307, R402, R408 | 47k; RC0603FR-0747KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.450 / 0.450 / 0.450 |
| R201 | 390k; RC0603FR-07390KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R302 | 137k; RC0603FR-07137KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R303 | 20k; RC0603FR-0720KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R304 | 91k; RC0603FR-0791KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R305 | 24.9k; RC0603FR-0724K9L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R306 | 100; RC0603FR-07100RL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R310 | 180; RC0603FR-07180RL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R311, R503 | 1.5k; RC0603FR-071K5L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.060 / 0.060 / 0.060 |
| R312, R405, R451, R453, R502, R504 | 1k; RC0603FR-071KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.180 / 0.180 / 0.180 |
| R313, R324 | 309k; RC0603FR-07309KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.060 / 0.060 / 0.060 |
| R314, R320, R321, R322, R323, R325, R316, R318, R327, R329, R334, R335, R338, R340, R341, R342, R401, R404, R505, R508, R509, R516 | 10k; RC0603FR-0710KL | Resistor_SMD:R_0603_1608Metric | [source](https://www.mouser.de/en/ProductDetail/YAGEO/RC0603FR-0710KL?qs=sGAEpiMZZMtlubZbdhIBIAhzU1Tw%252BHVakiDuQ4Zki0U%3D); Mouser 603-RC0603FR-0710KL; MOQ1 | OBSERVED_M2; 3405942 cached DE | 0.0070 / 0.0070 / 0.0070 | 0.154 / 0.154 / 0.154 |
| R315 | 127k; RC0603FR-07127KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R317 | 61.9k; RC0603FR-0761K9L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R326 | 78.7k; RC0603FR-0778K7L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R328 | 69.8k; RC0603FR-0769K8L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R330 | 0.05 ohm / 1% / 1W; WSL2512R0500FEA | Resistor_SMD:R_2512_6332Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1800 / 0.1800 / 0.1800 | 0.180 / 0.180 / 0.180 |
| R331, R332 | 10; RC0603FR-0710RL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.060 / 0.060 / 0.060 |
| R333 | 30k; RC0603FR-0730KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R337 | 60.4k; RC0603FR-0760K4L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R339 | 1.3k; RC0603FR-071K3L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R403 | 0; RC0603JR-070RL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R406 | 100; CRCW2512100RFKEG | Resistor_SMD:R_2512_6332Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1000 / 0.1000 / 0.1000 | 0.100 / 0.100 / 0.100 |
| R452 | 330k; RC0603FR-07330KL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R501 | 27; RC2512FR-0727RL | Resistor_SMD:R_2512_6332Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0800 / 0.0800 / 0.0800 | 0.080 / 0.080 / 0.080 |
| R507 | 470; RC0603FR-07470RL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| R510, R511, R512 | 22; RC0603FR-0722RL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.090 / 0.090 / 0.090 |
| R513, R515 | 750; RC0603FR-07750RL | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.060 / 0.060 / 0.060 |
| R514 | 6.8; RC0603FR-076R8L | Resistor_SMD:R_0603_1608Metric | Unquoted; manufacturer/supplier check OPEN; OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.0300 / 0.0300 / 0.0300 | 0.030 / 0.030 / 0.030 |
| T401 | 9T + 9T bifilar / FT-50A-43; Amidon FT-50A-43 + AWG24 enamel Cu | ARDF_TX:FT50A43_Bifilar_4Terminal | [source](https://www.amidoncorp.com/ft-50a-43/); Amidon/Akizuki FT-50A-43 / Akizuki131662; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.9500 / 0.9500 / 0.9500 | 0.950 / 0.950 / 0.950 |
| TH301 | 10k NTC / B25-50=3380; NCP18XH103F03RB | Resistor_SMD:R_0603_1608Metric | [source](https://www.murata.com/en-us/products/productdetail?partno=NCP18XH103F03RB); OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1000 / 0.1000 / 0.1000 | 0.100 / 0.100 / 0.100 |
| U101 | SI5351A-B-GT; SI5351A-B-GT | Package_SO:MSOP-10_3x3mm_P0.5mm | [source](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847); DigiKey 336-2399-5-ND; MOQ1 | OBSERVED_M2; 10254 earlier index | 1.8700 / 1.3880 / 1.3880 | 1.870 / 1.388 / 1.388 |
| U201 | MCP100T-300I/TT; MCP100T-300I/TT | Package_TO_SOT_SMD:SOT-23 | [source](https://www.mouser.it/ProductDetail/Microchip-Technology/MCP100T-300I-TT?qs=8U9qMIGhlkokseONjNxnUg%3D%3D); Mouser 579-MCP100T-300I/TT; MOQ1 | OBSERVED_M2; 3723 US vs3538 AU indexed; EU live basket OPEN; aggregator counts excluded | 0.3610 / 0.3610 / 0.3610 | 0.361 / 0.361 / 0.361 |
| U202 | 74HC123D,653; 74HC123D,653 | Package_SO:SOIC-16_3.9x9.9mm_P1.27mm | [source](https://eu.mouser.com/en/ProductDetail/Nexperia/74HC123D653?qs=P62ublwmbi%2FMZUrC9zEqyg%3D%3D); Mouser 771-74HC123D-T; MOQ1 | OBSERVED_M2; 1037 newer EU vs zero older NL/BR; conflict | 0.3270 / 0.2190 / 0.2190 | 0.327 / 0.219 / 0.219 |
| U203 | 74HC14D,653; 74HC14D,653 | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://www.mouser.es/ProductDetail/Nexperia/74HC14D653?qs=P62ublwmbi8OHaKXqv2GmQ%3D%3D); Mouser 771-74HC14D-T; MOQ1 | OBSERVED_M3; Mouser indexed862904; actualbasketOPEN | 0.1720 / 0.1180 / 0.1180 | 0.172 / 0.118 / 0.118 |
| U211 | 74HC21D,653; 74HC21D,653 | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://assets.nexperia.com/documents/data-sheet/74HC21.pdf); Mouser 771-74HC21D-T; MOQ1 | OBSERVED_M3; IndexedCanada18895,EURSpainprice; localizedbasketOPEN | 0.2410 / 0.1660 / 0.1660 | 0.241 / 0.166 / 0.166 |
| U212 | 74HC00D,653; 74HC00D,653 | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://assets.nexperia.com/documents/data-sheet/74HC_HCT00.pdf); Mouser 771-74HC00D-T; MOQ1 | OBSERVED_M2; M2 indexedNexperia SOICstock; exactcurrentcut-tapebasketOPEN | 0.1720 / 0.1030 / 0.1030 | 0.172 / 0.103 / 0.103 |
| U213, U222 | 74HC08D,653; 74HC08D,653 | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://eu.mouser.com/ProductDetail/Nexperia/74HC08D653?qs=P62ublwmbi%2FQCxm29EB%2FyA%3D%3D); Mouser 771-74HC08D-T; MOQ1 | OBSERVED_M2; 37703 cached EU | 0.1140 / 0.1140 / 0.1010 | 0.228 / 0.228 / 0.202 |
| U214 | 74HC32D,653; 74HC32D,653 | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://assets.nexperia.com/documents/data-sheet/74HC_HCT32.pdf); Mouser 771-74HC32D-T; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1600 / 0.1600 / 0.1600 | 0.160 / 0.160 / 0.160 |
| U221 | 74HC11D,653; 74HC11D,653 | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://assets.nexperia.com/documents/data-sheet/74HC_HCT11.pdf); Mouser 771-74HC11D-T; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.1600 / 0.1600 / 0.1600 | 0.160 / 0.160 / 0.160 |
| U223, U224 | 74HC74D,653; 74HC74D,653 | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://nl.mouser.com/ProductDetail/Nexperia/74HC74D653?qs=P62ublwmbi8VnJ1KG1%2FblQ%3D%3D); Mouser 771-74HC74D-T; MOQ1 | OBSERVED_M2; 623 older NL;1590 newer USD | 0.1230 / 0.1230 / 0.1080 | 0.246 / 0.246 / 0.216 |
| U301 | TPS54302DDCT; TPS54302DDCT | Package_TO_SOT_SMD:TSOT-23-6 | [source](https://www.ti.com/lit/ds/symlink/tps54302.pdf); Mouser 595-TPS54302DDCT; MOQ1 | OBSERVED_M2; New EUR index3137; direct browser failed; basket OPEN | 1.5900 / 1.1800 / 1.1800 | 1.590 / 1.180 / 1.180 |
| U302 | TPS22810DBVR; TPS22810DBVR | Package_TO_SOT_SMD:SOT-23-6 | [source](https://www.ti.com/lit/ds/symlink/tps22810.pdf); OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.5200 / 0.5200 / 0.5200 | 0.520 / 0.520 / 0.520 |
| U311 | TL431AIDBZR; TL431AIDBZR | Package_TO_SOT_SMD:SOT-23 | [source](https://www.ti.com/lit/ds/symlink/tl431.pdf); OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.2500 / 0.2500 / 0.2500 | 0.250 / 0.250 / 0.250 |
| U312 | LM339BIDR; LM339BIDR | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://www.ti.com/lit/ds/symlink/lm339b.pdf); OPEN OPEN; MOQ1 | ESTIMATE; Exact basket/stock OPEN | 0.2500 / 0.2500 / 0.2500 | 0.250 / 0.250 / 0.250 |
| U313 | INA180A1IDBVT; INA180A1IDBVT | Package_TO_SOT_SMD:SOT-23-5 | [source](https://www.ti.com/lit/ds/symlink/ina180.pdf); Mouser/DigiKey 595-INA180A1IDBVT / exact DigiKey code OPEN; MOQ1 | MIXED_ESTIMATE; Mouser indexed2890; price0.96 one observed, ten0.70 ESTIMATE; R package OOS not substituted | 0.9600 / 0.7000 / 0.7000 | 0.960 / 0.700 / 0.700 |
| U314 | LM393BIDR; LM393BIDR | Package_SO:SOIC-8_3.9x4.9mm_P1.27mm | [source](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM393BIDR?qs=BJlw7L4Cy78N8CV%252BGpRosA%3D%3D); Mouser 595-LM393BIDR; MOQ1 | OBSERVED_M2; 6986 cached EU vs7644 US; basket OPEN | 0.1980 / 0.1400 / 0.1400 | 0.198 / 0.140 / 0.140 |
| U401 | LM5134BMF/NOPB; LM5134BMF/NOPB | Package_TO_SOT_SMD:SOT-23-6 | [source](https://www.ti.com/lit/ds/symlink/lm5134.pdf); Mouser 595-LM5134BMF/NOPB; MOQ1 | OBSERVED_M2; EU stock conflict:510 US indexed; DE incoming30Nov. Local basket MUST close. | 2.1700 / 1.6200 / 1.6200 | 2.170 / 1.620 / 1.620 |
| U501 | SN74AC00DR; SN74AC00DR | Package_SO:SOIC-14_3.9x8.7mm_P1.27mm | [source](https://www.ti.com/lit/ds/symlink/sn74ac00.pdf); Mouser 595-SN74AC00DR; MOQ1 | OBSERVED_M3; 2369EUindexed;ActiveDRcut-tapeMOQ1;D-tubeEOLnotselected | 0.4040 / 0.2780 / 0.2780 | 0.404 / 0.278 / 0.278 |
| Y101 | 25 MHz / CL10 pF; ABM3B-25.000MHZ-10-1-U-T | Crystal:Crystal_SMD_5032-4Pin_5.0x3.2mm | [source](https://abracon.com/parametric/crystals/ABM3B-25.000MHZ-10-1-U-T); Mouser/DigiKey 815-ABM3B-25-T / 300-8218-1-ND; MOQ1 | ESTIMATE; Mouser indexed 2381; net EUR price not captured | 0.4000 / 0.4000 / 0.4000 | 0.400 / 0.400 / 0.400 |

Each component and pin mapping is in [electrical manifest](../hardware/80m/RF80.electrical.json). CSV has per-reference population/order/quantity information. Fixed calibration resistor replacements and spare winding material are additional prototype material, not implicit free items.
