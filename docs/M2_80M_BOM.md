# M2 80 m candidate cost workbook

Date: 2026-10-13. **Generated analysis, not an ordering BOM.** Current/indexed observations and explicit estimates; EUR ex VAT. Reference counts are inspected facts; unquoted prices, population choices and all derived RF performance remain unverified. See [comparison](M2_80M_COST_COMPARISON.md).

| Scope | 6 EUR/unit | 10 | 20 | Observed / estimated at ten |
| --- | ---: | ---: | ---: | --- |
| FlexFox80 complete native listed PCB envelope | 87.27 | 83.99 | 83.84 | 11.29 / 72.70 |
| FlexFox80 RF source/driver/PA/filter only | 12.26 | 10.45 | 10.45 | 4.40 / 6.05 |
| FlexFox80 RF core plus native adjustable supply | 32.55 | 28.98 | 28.98 | 10.53 / 18.45 |
| SignalSlinger complete native listed PCB envelope | 50.80 | 49.06 | 49.06 | 5.71 / 43.35 |
| SignalSlinger RF source/driver/PA/filter only | 12.24 | 10.42 | 10.42 | 4.40 / 6.03 |
| ON7YD ATX80 original RF board | 6.01 | 5.52 | 5.52 | 0.70 / 4.82 |
| DF1FO MidiTX RF section | 6.17 | 5.83 | 5.79 | 1.03 / 4.80 |
| DF1FO SprintTX 50-80mW RF section | 3.73 | 3.73 | 3.68 | 0.16 / 3.57 |
| Fixle complete reference estimate | 6.72 | 6.67 | 6.67 | 0.04 / 6.63 |
| DF1FO MidiTX complete reference estimate excluding cells/antenna | 18.17 | 17.76 | 17.73 | 1.07 / 16.69 |
| DF1FO SprintTX 50-80mW complete reference estimate excluding cells/antenna | 12.10 | 12.10 | 12.05 | 0.16 / 11.94 |
| TinyFox complete reference estimate excluding AA cell | 13.03 | 12.96 | 12.93 | 0.22 / 12.74 |
| Proposed Fox-only RF | 9.40 | 8.50 | 8.44 | 2.71 / 5.79 |
| Proposed 1.2W Classic/Sprint + Fox RF | 22.41 | 19.76 | 19.68 | 8.59 / 11.17 |
| Proposed 2-3W/5W supply alternative + Fox RF | 35.48 | 30.86 | 30.79 | 15.40 / 15.46 |
| DF1FO mechanism adapted to protected programmable module allowance | 21.91 | 19.68 | 19.61 | 8.04 / 11.64 |

Identical MPNs pool only within each basket; different values do not share hypothetical breaks. Estimates assume MOQ1/multiple1 unless stated; stock and minimum bulk purchases remain open. A reference scope is described in the comparison; it is not an alternative complying ARDF-TX BOM.

## FlexFox80 complete native listed PCB envelope

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| filter_matching_and_decoupling / C101 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C117 22uF | 1; 6 / 10 / 20 | CL32A226MAJNNNE; Original BOM identifier; price OPEN: 1276-3373-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C119 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C120 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C122 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C123 1100pF | 1; 6 / 10 / 20 | C0805C112J5GAC7800; Original BOM identifier; price OPEN: 399-14552-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C126 1800pF | 1; 6 / 10 / 20 | CGA4F2C0G2A182J085AA; Original BOM identifier; price OPEN: 445-5752-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C128 91pF | 1; 6 / 10 / 20 | 06031U910FAT2A; Original BOM identifier; price OPEN: 478-10247-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C131 1100pF | 1; 6 / 10 / 20 | C0805C112J5GAC7800; Original BOM identifier; price OPEN: 399-14552-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D101 MBD54DWT1G_Schottky_Ind-ARDF-2-Band-MiniTx-rescue | 1; 6 / 10 / 20 | MBD54DWT1G; Original BOM identifier; price OPEN: MBD54DWT1GOSCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D102 4.7V | 1; 6 / 10 / 20 | BZT52C4V7-13-F; Original BOM identifier; price OPEN: BZT52C4V7-13FDICT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D104 ESD | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / HS101 Heatsink | 1; 6 / 10 / 20 | TH; Original BOM identifier; price OPEN: HS220-ND | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| connectors / J101 DIN-5_180degree | 1; 6 / 10 / 20 | TH; Original BOM identifier; price OPEN: CP-7050-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J102 Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: np | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| filter_matching / L104 | 1; 6 / 10 / 20 | FT-50A-43 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| filter_matching / L106 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| filter_matching / L108 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| RF_semiconductors / Q102 | 1; 6 / 10 / 20 | IRF610PBF-BE3; [Farnell](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567): 4853567 | OBSERVED; 1/1 | 1.11 / 0.622 / 0.622 | 1.11 / 0.62 / 0.62 |
| power_and_other_ICs / U101 | 1; 6 / 10 / 20 | TPS22810DBVT; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/TPS22810DBVT?qs=34RfhUjJmKcpY51nBe7C4Q%3D%3D): 595-TPS22810DBVT | OBSERVED; 1/1 | 0.765 / 0.765 / 0.692 | 0.77 / 0.77 / 0.69 |
| drivers / U107 | 1; 6 / 10 / 20 | LM5134BMF/NOPB; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM5134BMF-NOPB?qs=2k4gZbgf%2F9lRirSLUMpZrA%3D%3D): 595-LM5134BMF/NOPB | OBSERVED; 1/1 | 2.17 / 1.62 / 1.62 | 2.17 / 1.62 / 1.62 |
| filter_matching_and_decoupling / C202 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C204 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C205 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C206 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C207 270pF | 1; 6 / 10 / 20 | CL21C271GBANNNC; Original BOM identifier; price OPEN: 1276-2624-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C208 10pF | 1; 6 / 10 / 20 | 08052U100FAT2A; Original BOM identifier; price OPEN: 478-10457-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C209 150uF low ESR | 1; 6 / 10 / 20 | TPME157K020R0035; Original BOM identifier; price OPEN: 478-5253-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C210 22uF | 1; 6 / 10 / 20 | CL32A226MAJNNNE; Original BOM identifier; price OPEN: 1276-3373-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C211 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C212 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C213 1uF | 1; 6 / 10 / 20 | CC0805KKX7R7BB105; Original BOM identifier; price OPEN: 311-1365-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C214 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C215 150uF low ESR | 1; 6 / 10 / 20 | TPME157K020R0035; Original BOM identifier; price OPEN: 478-5253-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C216 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C217 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C218 10nF | 1; 6 / 10 / 20 | 08055A103JAT2A; Original BOM identifier; price OPEN: 478-10068-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C219 1uF | 1; 6 / 10 / 20 | CC0805KKX7R7BB105; Original BOM identifier; price OPEN: 311-1365-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| other_safety_passives / D201 B530 | 1; 6 / 10 / 20 | B530C-13-F; Original BOM identifier; price OPEN: B530C-FDICT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D202 B530 | 1; 6 / 10 / 20 | B530C-13-F; Original BOM identifier; price OPEN: B530C-FDICT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| connectors / J203 V4 | 1; 6 / 10 / 20 | V4; MPN OPEN; Original BOM identifier; price OPEN: np | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J? Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| filter_matching_and_decoupling / L202 6.8uH | 1; 6 / 10 / 20 | CDR7D28MNNP-6R8NC; Original BOM identifier; price OPEN: 308-1328-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / L203 6.8uH | 1; 6 / 10 / 20 | CDR7D28MNNP-6R8NC; Original BOM identifier; price OPEN: 308-1328-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| connectors / P201 Power Pole | 1; 6 / 10 / 20 | TH; Original BOM identifier; price OPEN: 2243-ASMPP30-1X2-RK-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / P203 Power Pole | 1; 6 / 10 / 20 | TH; Original BOM identifier; price OPEN: 2243-ASMPP30-1X2-RK-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / Q201 MUN5213DW1 | 1; 6 / 10 / 20 | MUN5213DW1T1G; Original BOM identifier; price OPEN: MUN5213DW1T1GOSCT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / Q202 DMP4025LSD | 1; 6 / 10 / 20 | DMP4025LSD-13; Original BOM identifier; price OPEN: DMP4025LSD-13DICT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / Q203 RJK0354DSP | 1; 6 / 10 / 20 | RJK0354DSP-00#J0; Original BOM identifier; price OPEN: RJK0354DSP-00#J0CT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| other_safety_passives / R201 162k | 1; 6 / 10 / 20 | RC0805FR-07162KL; Original BOM identifier; price OPEN: 311-162KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R202 49.9k | 1; 6 / 10 / 20 | RT0805BRE0749K9L; Original BOM identifier; price OPEN: YAG4990CT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R203 27k | 1; 6 / 10 / 20 | RC0805FR-0727KL; Original BOM identifier; price OPEN: 311-27.0KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R204 392k | 1; 6 / 10 / 20 | RC0805FR-07392KL; Original BOM identifier; price OPEN: 311-392KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R205 162k | 1; 6 / 10 / 20 | RC0805FR-07162KL; Original BOM identifier; price OPEN: 311-162KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R206 27k | 1; 6 / 10 / 20 | RC0805FR-0727KL; Original BOM identifier; price OPEN: 311-27.0KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R207 100k | 1; 6 / 10 / 20 | RC0805FR-07100KL; Original BOM identifier; price OPEN: 311-100KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R208 27k | 1; 6 / 10 / 20 | RC0805FR-0727KL; Original BOM identifier; price OPEN: 311-27.0KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R209 100k | 1; 6 / 10 / 20 | RC0805FR-07100KL; Original BOM identifier; price OPEN: 311-100KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R210 100k | 1; 6 / 10 / 20 | RC0805FR-07100KL; Original BOM identifier; price OPEN: 311-100KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R211 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R212 162k | 1; 6 / 10 / 20 | RC0805FR-07162KL; Original BOM identifier; price OPEN: 311-162KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R213 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R214 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R215 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R216 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R217 1.1k | 1; 6 / 10 / 20 | RC0805FR-071K1L; Original BOM identifier; price OPEN: 311-1.10KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R218 0.01 0.5W | 1; 6 / 10 / 20 | KRL1220E-M-R010-F-T5; Original BOM identifier; price OPEN: 408-1544-1-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| power_and_other_ICs / U202 | 1; 6 / 10 / 20 | OPA171AIDBVR; OPEN: OPEN | ESTIMATE; 1/1 | 1.2 / 1.2 / 1.2 | 1.20 / 1.20 / 1.20 |
| power_and_other_ICs / U203 | 1; 6 / 10 / 20 | LTC3600EMSE#PBF; [Mouser](https://www.mouser.de/c/power/power-management-ics/voltage-regulators-switching-regulators/?series=LTC3600): OPEN: exact supplier SKU not captured | OBSERVED; 1/1 | 7.89 / 6.13 / 6.13 | 7.89 / 6.13 / 6.13 |
| power_and_other_ICs / U204 MIC2196 | 1; 6 / 10 / 20 | MIC2196YM-TR; Original BOM identifier; price OPEN: MIC2196YM-CT-ND | ESTIMATE; 1/1 | 2.8 / 2.8 / 2.8 | 2.80 / 2.80 / 2.80 |
| other_safety_passives / BT301 CR1220 | 1; 6 / 10 / 20 | BC501SM; Original BOM identifier; price OPEN: BC501SM-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C301 1uF | 1; 6 / 10 / 20 | CC0805KKX7R7BB105; Original BOM identifier; price OPEN: 311-1365-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C302 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C303 4.7uF | 1; 6 / 10 / 20 | TMK212AB7475KG-T; Original BOM identifier; price OPEN: 587-2990-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C304 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C305 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C306 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C307 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C308 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C310 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C311 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C312 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C313 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C314 4.7uF | 1; 6 / 10 / 20 | TMK212AB7475KG-T; Original BOM identifier; price OPEN: 587-2990-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C315 4.7uF | 1; 6 / 10 / 20 | TMK212AB7475KG-T; Original BOM identifier; price OPEN: 587-2990-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C317 4.7uF | 1; 6 / 10 / 20 | TMK212AB7475KG-T; Original BOM identifier; price OPEN: 587-2990-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C318 4.7uF | 1; 6 / 10 / 20 | TMK212AB7475KG-T; Original BOM identifier; price OPEN: 587-2990-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C319 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C320 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D301 MBD54 | 1; 6 / 10 / 20 | MBD54DWT1G; Original BOM identifier; price OPEN: MBD54DWT1GOSCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D304 GREEN | 1; 6 / 10 / 20 | 150080GS75000; Original BOM identifier; price OPEN: 732-4983-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D305 RED | 1; 6 / 10 / 20 | 150080RS75000; Original BOM identifier; price OPEN: 732-4984-1-ND  | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D306 ESD | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D307 ESD | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| connectors / J301 DB9_Female | 1; 6 / 10 / 20 | DE09S064TLF; Original BOM identifier; price OPEN: 609-1525-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J302 Conn_01x06 | 1; 6 / 10 / 20 | TH; Original BOM identifier; price OPEN: 929550-01-06-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J303 DB9_Male | 1; 6 / 10 / 20 | DE09P065TXLF; Original BOM identifier; price OPEN: 609-5908-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J304 Conn_01x10 | 1; 6 / 10 / 20 | Conn_01x10; MPN OPEN; Original BOM identifier; price OPEN: np | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J305 Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J306 Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J307 Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J308 Conn_01x03 | 1; 6 / 10 / 20 | Conn_01x03; MPN OPEN; Original BOM identifier; price OPEN: np | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / MOD301 HUZZAH_ESP8266_Breakout | 1; 6 / 10 / 20 | 2471; Original BOM identifier; price OPEN: 1528-1223-ND | ESTIMATE; 1/1 | 8.5 / 8.5 / 8.5 | 8.50 / 8.50 / 8.50 |
| connectors / P301 ISP/PDI | 1; 6 / 10 / 20 | 95278-101A06LF; Original BOM identifier; price OPEN: 609-3487-1-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / P302 Thru | 1; 6 / 10 / 20 | Thru; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / P304 Header | 1; 6 / 10 / 20 | Header; MPN OPEN; Original BOM identifier; price OPEN: np | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / Q301 PN2222A | 1; 6 / 10 / 20 | MMBT2222A-TP; Original BOM identifier; price OPEN: MMBT2222ATPMSCT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| other_safety_passives / R301 470 | 1; 6 / 10 / 20 | RK73H2ATTD4700F; Original BOM identifier; price OPEN: 2019-RK73H2ATTD4700FCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R302 470 | 1; 6 / 10 / 20 | RK73H2ATTD4700F; Original BOM identifier; price OPEN: 2019-RK73H2ATTD4700FCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R303 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R304 10 | 1; 6 / 10 / 20 | RC0805FR-0710RL; Original BOM identifier; price OPEN: 311-10.0CRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R306 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R307 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R308 100k | 1; 6 / 10 / 20 | RC0805FR-07100KL; Original BOM identifier; price OPEN: 311-100KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R309 2.2k | 1; 6 / 10 / 20 | RC0805FR-072K2L; Original BOM identifier; price OPEN: 311-2.2KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R310 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R311 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R312 560k | 1; 6 / 10 / 20 | RT0805FRE07560KL; Original BOM identifier; price OPEN: 13-RT0805FRE07560KLCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R313 100k | 1; 6 / 10 / 20 | RC0805FR-07100KL; Original BOM identifier; price OPEN: 311-100KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R314 560k | 1; 6 / 10 / 20 | RT0805FRE07560KL; Original BOM identifier; price OPEN: 13-RT0805FRE07560KLCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R315 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R316 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / RV301 10k Pot | 1; 6 / 10 / 20 | TC33X-2-103E; Original BOM identifier; price OPEN: TC33X-103ECT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / SJ301 SolderJumper_2_Open | 1; 6 / 10 / 20 | SolderJumper_2_Open; MPN OPEN; Original BOM identifier; price OPEN: np | ESTIMATE; 1/1 | 0.2 / 0.2 / 0.2 | 0.20 / 0.20 / 0.20 |
| other_safety_passives / SW301 SPST | 1; 6 / 10 / 20 | PTS645SL50SMTR92 LFS; Original BOM identifier; price OPEN: CKN9088CT-ND | ESTIMATE; 1/1 | 0.2 / 0.2 / 0.2 | 0.20 / 0.20 / 0.20 |
| controller_RTC / U301 DS3231 | 1; 6 / 10 / 20 | DS3231S#T&R; Original BOM identifier; price OPEN: DS3231S#T&RCT-ND | ESTIMATE; 1/1 | 5.0 / 5.0 / 5.0 | 5.00 / 5.00 / 5.00 |
| controller_RTC / U302 AVR128DA48 | 1; 6 / 10 / 20 | AVR128DA48T-E/PT; Original BOM identifier; price OPEN: 150-AVR128DA48T-E/PTCT-ND | ESTIMATE; 1/1 | 3.5 / 3.5 / 3.5 | 3.50 / 3.50 / 3.50 |
| power_and_other_ICs / U303 LD2985BM33R | 1; 6 / 10 / 20 | LD2985BM33R; Original BOM identifier; price OPEN: 497-3499-1-ND | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| synth_reference / U304 | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| power_and_other_ICs / U305 74HC1G08 | 1; 6 / 10 / 20 | MC74HC1G08DTT1G; Original BOM identifier; price OPEN: MC74HC1G08DTT1GOSCT-ND | ESTIMATE; 1/1 | 0.15 / 0.15 / 0.15 | 0.15 / 0.15 / 0.15 |
| power_and_other_ICs / U306 LT1763CS8-5 | 1; 6 / 10 / 20 | LT1763CS8-5#TRPBF; Original BOM identifier; price OPEN: LT1763CS8-5#TRPBFCT-ND | ESTIMATE; 1/1 | 2.8 / 2.8 / 2.8 | 2.80 / 2.80 / 2.80 |
| power_and_other_ICs / U307 | 1; 6 / 10 / 20 | TPS22810DBVT; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/TPS22810DBVT?qs=34RfhUjJmKcpY51nBe7C4Q%3D%3D): 595-TPS22810DBVT | OBSERVED; 1/1 | 0.765 / 0.765 / 0.692 | 0.77 / 0.77 / 0.69 |
| power_and_other_ICs / U308 LD2985BM33R | 1; 6 / 10 / 20 | LD2985BM33R; Original BOM identifier; price OPEN: 497-3499-1-ND | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| synth_reference / X301 25.MHZ TCXO | 1; 6 / 10 / 20 | I537-2O7-25.000 MHZ; Original BOM identifier; price OPEN: 2780-I537-2O7-25.000MHZCT-ND | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| mechanical / Native case/mounting | 1; 6 / 10 / 20 | Native outer case/mounting allowance; OPEN: OPEN | ESTIMATE; 1/1 | 20 / 20 / 20 | 20.00 / 20.00 / 20.00 |
| backup_battery / CR1220 cell, holder BT301 separately costed | 1; 6 / 10 / 20 | CR1220 backup cell exact source OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |

## FlexFox80 RF source/driver/PA/filter only

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| drivers / U107 | 1; 6 / 10 / 20 | LM5134BMF/NOPB; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM5134BMF-NOPB?qs=2k4gZbgf%2F9lRirSLUMpZrA%3D%3D): 595-LM5134BMF/NOPB | OBSERVED; 1/1 | 2.17 / 1.62 / 1.62 | 2.17 / 1.62 / 1.62 |
| RF_semiconductors / Q102 | 1; 6 / 10 / 20 | IRF610PBF-BE3; [Farnell](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567): 4853567 | OBSERVED; 1/1 | 1.11 / 0.622 / 0.622 | 1.11 / 0.62 / 0.62 |
| filter_matching / L104 | 1; 6 / 10 / 20 | FT-50A-43 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| filter_matching / L106 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| filter_matching / L108 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| filter_matching_and_decoupling / C117 22uF | 1; 6 / 10 / 20 | CL32A226MAJNNNE; Original BOM identifier; price OPEN: 1276-3373-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C119 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C120 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C122 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C123 1100pF | 1; 6 / 10 / 20 | C0805C112J5GAC7800; Original BOM identifier; price OPEN: 399-14552-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C126 1800pF | 1; 6 / 10 / 20 | CGA4F2C0G2A182J085AA; Original BOM identifier; price OPEN: 445-5752-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C128 91pF | 1; 6 / 10 / 20 | 06031U910FAT2A; Original BOM identifier; price OPEN: 478-10247-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C131 1100pF | 1; 6 / 10 / 20 | C0805C112J5GAC7800; Original BOM identifier; price OPEN: 399-14552-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| synth_reference / U304 | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| synth_reference / X301 25.MHZ TCXO | 1; 6 / 10 / 20 | I537-2O7-25.000 MHZ; Original BOM identifier; price OPEN: 2780-I537-2O7-25.000MHZCT-ND | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| filter_matching_and_decoupling / C318 4.7uF | 1; 6 / 10 / 20 | TMK212AB7475KG-T; Original BOM identifier; price OPEN: 587-2990-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C308 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / R306 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R307 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| power_and_other_ICs / U101 | 1; 6 / 10 / 20 | TPS22810DBVT; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/TPS22810DBVT?qs=34RfhUjJmKcpY51nBe7C4Q%3D%3D): 595-TPS22810DBVT | OBSERVED; 1/1 | 1.06 / 0.765 / 0.765 | 1.06 / 0.77 / 0.77 |
| filter_matching_and_decoupling / C101 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| other_safety_passives / D102 4.7V | 1; 6 / 10 / 20 | BZT52C4V7-13-F; Original BOM identifier; price OPEN: BZT52C4V7-13FDICT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |

## FlexFox80 RF core plus native adjustable supply

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| drivers / U107 | 1; 6 / 10 / 20 | LM5134BMF/NOPB; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM5134BMF-NOPB?qs=2k4gZbgf%2F9lRirSLUMpZrA%3D%3D): 595-LM5134BMF/NOPB | OBSERVED; 1/1 | 2.17 / 1.62 / 1.62 | 2.17 / 1.62 / 1.62 |
| RF_semiconductors / Q102 | 1; 6 / 10 / 20 | IRF610PBF-BE3; [Farnell](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567): 4853567 | OBSERVED; 1/1 | 1.11 / 0.622 / 0.622 | 1.11 / 0.62 / 0.62 |
| filter_matching / L104 | 1; 6 / 10 / 20 | FT-50A-43 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| filter_matching / L106 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| filter_matching / L108 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| filter_matching_and_decoupling / C117 22uF | 1; 6 / 10 / 20 | CL32A226MAJNNNE; Original BOM identifier; price OPEN: 1276-3373-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C119 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C120 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C122 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C123 1100pF | 1; 6 / 10 / 20 | C0805C112J5GAC7800; Original BOM identifier; price OPEN: 399-14552-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C126 1800pF | 1; 6 / 10 / 20 | CGA4F2C0G2A182J085AA; Original BOM identifier; price OPEN: 445-5752-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C128 91pF | 1; 6 / 10 / 20 | 06031U910FAT2A; Original BOM identifier; price OPEN: 478-10247-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C131 1100pF | 1; 6 / 10 / 20 | C0805C112J5GAC7800; Original BOM identifier; price OPEN: 399-14552-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| synth_reference / U304 | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| synth_reference / X301 25.MHZ TCXO | 1; 6 / 10 / 20 | I537-2O7-25.000 MHZ; Original BOM identifier; price OPEN: 2780-I537-2O7-25.000MHZCT-ND | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| filter_matching_and_decoupling / C318 4.7uF | 1; 6 / 10 / 20 | TMK212AB7475KG-T; Original BOM identifier; price OPEN: 587-2990-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C308 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / R306 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R307 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| power_and_other_ICs / U101 | 1; 6 / 10 / 20 | TPS22810DBVT; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/TPS22810DBVT?qs=34RfhUjJmKcpY51nBe7C4Q%3D%3D): 595-TPS22810DBVT | OBSERVED; 1/1 | 1.06 / 0.765 / 0.765 | 1.06 / 0.77 / 0.77 |
| filter_matching_and_decoupling / C101 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| other_safety_passives / D102 4.7V | 1; 6 / 10 / 20 | BZT52C4V7-13-F; Original BOM identifier; price OPEN: BZT52C4V7-13FDICT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| power_and_other_ICs / U202 | 1; 6 / 10 / 20 | OPA171AIDBVR; OPEN: OPEN | ESTIMATE; 1/1 | 1.2 / 1.2 / 1.2 | 1.20 / 1.20 / 1.20 |
| power_and_other_ICs / U203 | 1; 6 / 10 / 20 | LTC3600EMSE#PBF; [Mouser](https://www.mouser.de/c/power/power-management-ics/voltage-regulators-switching-regulators/?series=LTC3600): OPEN: exact supplier SKU not captured | OBSERVED; 1/1 | 7.89 / 6.13 / 6.13 | 7.89 / 6.13 / 6.13 |
| power_and_other_ICs / U204 MIC2196 | 1; 6 / 10 / 20 | MIC2196YM-TR; Original BOM identifier; price OPEN: MIC2196YM-CT-ND | ESTIMATE; 1/1 | 2.8 / 2.8 / 2.8 | 2.80 / 2.80 / 2.80 |
| filter_matching_and_decoupling / L202 6.8uH | 1; 6 / 10 / 20 | CDR7D28MNNP-6R8NC; Original BOM identifier; price OPEN: 308-1328-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / L203 6.8uH | 1; 6 / 10 / 20 | CDR7D28MNNP-6R8NC; Original BOM identifier; price OPEN: 308-1328-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| power_and_other_ICs / Q201 MUN5213DW1 | 1; 6 / 10 / 20 | MUN5213DW1T1G; Original BOM identifier; price OPEN: MUN5213DW1T1GOSCT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / Q202 DMP4025LSD | 1; 6 / 10 / 20 | DMP4025LSD-13; Original BOM identifier; price OPEN: DMP4025LSD-13DICT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / Q203 RJK0354DSP | 1; 6 / 10 / 20 | RJK0354DSP-00#J0; Original BOM identifier; price OPEN: RJK0354DSP-00#J0CT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| other_safety_passives / R204 392k | 1; 6 / 10 / 20 | RC0805FR-07392KL; Original BOM identifier; price OPEN: 311-392KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R206 27k | 1; 6 / 10 / 20 | RC0805FR-0727KL; Original BOM identifier; price OPEN: 311-27.0KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R207 100k | 1; 6 / 10 / 20 | RC0805FR-07100KL; Original BOM identifier; price OPEN: 311-100KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R208 27k | 1; 6 / 10 / 20 | RC0805FR-0727KL; Original BOM identifier; price OPEN: 311-27.0KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R209 100k | 1; 6 / 10 / 20 | RC0805FR-07100KL; Original BOM identifier; price OPEN: 311-100KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R210 100k | 1; 6 / 10 / 20 | RC0805FR-07100KL; Original BOM identifier; price OPEN: 311-100KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R211 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R212 162k | 1; 6 / 10 / 20 | RC0805FR-07162KL; Original BOM identifier; price OPEN: 311-162KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R213 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R214 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R215 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R216 10k | 1; 6 / 10 / 20 | AC0805FR-0710KL; Original BOM identifier; price OPEN: 311-10KLGCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R217 1.1k | 1; 6 / 10 / 20 | RC0805FR-071K1L; Original BOM identifier; price OPEN: 311-1.10KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R218 0.01 0.5W | 1; 6 / 10 / 20 | KRL1220E-M-R010-F-T5; Original BOM identifier; price OPEN: 408-1544-1-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| filter_matching_and_decoupling / C202 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C204 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C205 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C206 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C207 270pF | 1; 6 / 10 / 20 | CL21C271GBANNNC; Original BOM identifier; price OPEN: 1276-2624-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C208 10pF | 1; 6 / 10 / 20 | 08052U100FAT2A; Original BOM identifier; price OPEN: 478-10457-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C209 150uF low ESR | 1; 6 / 10 / 20 | TPME157K020R0035; Original BOM identifier; price OPEN: 478-5253-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C210 22uF | 1; 6 / 10 / 20 | CL32A226MAJNNNE; Original BOM identifier; price OPEN: 1276-3373-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C211 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C212 100nF | 1; 6 / 10 / 20 | 08055C104KAT2A; Original BOM identifier; price OPEN: 478-1395-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C213 1uF | 1; 6 / 10 / 20 | CC0805KKX7R7BB105; Original BOM identifier; price OPEN: 311-1365-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C214 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C215 150uF low ESR | 1; 6 / 10 / 20 | TPME157K020R0035; Original BOM identifier; price OPEN: 478-5253-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C216 10uF | 1; 6 / 10 / 20 | GRM21BR61E106KA73L; Original BOM identifier; price OPEN: 490-5523-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C217 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C218 10nF | 1; 6 / 10 / 20 | 08055A103JAT2A; Original BOM identifier; price OPEN: 478-10068-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C219 1uF | 1; 6 / 10 / 20 | CC0805KKX7R7BB105; Original BOM identifier; price OPEN: 311-1365-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |

## SignalSlinger complete native listed PCB envelope

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| filter_matching_and_decoupling / C101 100nF | 1; 6 / 10 / 20 | CL21B104KACNNNC; Original BOM identifier; price OPEN: 1276-1099-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C102 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C103 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C104 100nF | 1; 6 / 10 / 20 | CL21B104KACNNNC; Original BOM identifier; price OPEN: 1276-1099-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C105 100nF | 1; 6 / 10 / 20 | CL21B104KACNNNC; Original BOM identifier; price OPEN: 1276-1099-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C106 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C107 100nF | 1; 6 / 10 / 20 | CL21B104KACNNNC; Original BOM identifier; price OPEN: 1276-1099-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C108 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C109 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C110 22uF | 1; 6 / 10 / 20 | CL32A226MAJNNNE; Original BOM identifier; price OPEN: 1276-3373-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C111 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C112 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D101 1N914WT | 1; 6 / 10 / 20 | 1N4148WT-7; Original BOM identifier; price OPEN: 1N4148WTDICT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D102 1N914WT | 1; 6 / 10 / 20 | 1N4148WT-7; Original BOM identifier; price OPEN: 1N4148WTDICT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D103 Red LED | 1; 6 / 10 / 20 | LTST-C170KRKT; Original BOM identifier; price OPEN: 160-1415-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D104 Green LED | 1; 6 / 10 / 20 | LTST-C170KGKT; Original BOM identifier; price OPEN: 160-1414-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D105 ESD9B5.0ST5G_1 | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D106 ESD9B5.0ST5G_1 | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D107 Schottky Diode | 1; 6 / 10 / 20 | CRS09(TE85L,Q,M); Original BOM identifier; price OPEN: CRS09QCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D108 ESD9B5.0ST5G_1 | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D109 ESD9B5.0ST5G_1 | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D110 ESD9B5.0ST5G_1 | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D111 ESD9B5.0ST5G_1 | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D112 ESD9B5.0ST5G_1 | 1; 6 / 10 / 20 | CG0603MLC-05LE; Original BOM identifier; price OPEN: CG0603MLC-05LECT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D115 Schottky Diode | 1; 6 / 10 / 20 | CRS09(TE85L,Q,M); Original BOM identifier; price OPEN: CRS09QCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| connectors / J101 Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J102 Conn_01x03 | 1; 6 / 10 / 20 | Conn_01x03; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J103 Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J104 Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J105 Conn_01x04 | 1; 6 / 10 / 20 | Conn_01x04; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J106 Conn_01x02 | 1; 6 / 10 / 20 | Conn_01x02; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J107 DB9 Female | 1; 6 / 10 / 20 | TH; Original BOM identifier; price OPEN: 609-1525-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| filter_matching / L101 | 1; 6 / 10 / 20 | FT-50A-43 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| connectors / P101 ISP/PDI | 1; 6 / 10 / 20 | 95278-101A06LF; Original BOM identifier; price OPEN: 609-3487-1-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / Q101 NTS4173PT1G | 1; 6 / 10 / 20 | NTS4173PT1G; Original BOM identifier; price OPEN: NTS4173PT1GOSCT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| power_and_other_ICs / Q102 BSS138W-7-F | 1; 6 / 10 / 20 | BSS138W-7-F; Original BOM identifier; price OPEN: BSS138W-FDICT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| RF_semiconductors / Q103 | 1; 6 / 10 / 20 | IRF610PBF-BE3; [Farnell](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567): 4853567 | OBSERVED; 1/1 | 1.11 / 0.622 / 0.622 | 1.11 / 0.62 / 0.62 |
| other_safety_passives / R101 105k | 1; 6 / 10 / 20 | RC0805FR-07105KL; Original BOM identifier; price OPEN: 311-105KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R102 162k | 1; 6 / 10 / 20 | RC0805FR-07162KL; Original BOM identifier; price OPEN: 311-162KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R103 12.4k | 1; 6 / 10 / 20 | RC0805FR-0712K4L; Original BOM identifier; price OPEN: 311-12.4KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R104 1k | 1; 6 / 10 / 20 | RMCF0805FT1K00; Original BOM identifier; price OPEN: RMCF0805FT1K00CT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R105 220 | 1; 6 / 10 / 20 | RC0805FR-10220RL; Original BOM identifier; price OPEN: 13-RC0805FR-10220RLCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R106 47k | 1; 6 / 10 / 20 | RC0805FR-0747KL; Original BOM identifier; price OPEN: 311-47.0KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R107 10k | 1; 6 / 10 / 20 | RNCP0805FTD10K0; Original BOM identifier; price OPEN: RNCP0805FTD10K0CT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R108 10k | 1; 6 / 10 / 20 | RNCP0805FTD10K0; Original BOM identifier; price OPEN: RNCP0805FTD10K0CT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R109 47 0.5W | 1; 6 / 10 / 20 | 47 0.5W; MPN OPEN; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R110 162k | 1; 6 / 10 / 20 | RC0805FR-07162KL; Original BOM identifier; price OPEN: 311-162KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / SW101 SW_SPST | 1; 6 / 10 / 20 | TL1014BF160QG; Original BOM identifier; price OPEN: EG5042CT-ND | ESTIMATE; 1/1 | 0.2 / 0.2 / 0.2 | 0.20 / 0.20 / 0.20 |
| controller_RTC / U101 AVR128DA28 | 1; 6 / 10 / 20 | AVR128DA28T-E/SO; Original BOM identifier; price OPEN: 150-AVR128DA28T-E/SOCT-ND | ESTIMATE; 1/1 | 3.5 / 3.5 / 3.5 | 3.50 / 3.50 / 3.50 |
| synth_reference / U102 | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| power_and_other_ICs / U103 | 1; 6 / 10 / 20 | TPS22810DBVT; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/TPS22810DBVT?qs=34RfhUjJmKcpY51nBe7C4Q%3D%3D): 595-TPS22810DBVT | OBSERVED; 1/1 | 0.765 / 0.692 / 0.692 | 0.77 / 0.69 / 0.69 |
| drivers / U104 | 1; 6 / 10 / 20 | LM5134BMF/NOPB; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM5134BMF-NOPB?qs=2k4gZbgf%2F9lRirSLUMpZrA%3D%3D): 595-LM5134BMF/NOPB | OBSERVED; 1/1 | 2.17 / 1.62 / 1.62 | 2.17 / 1.62 / 1.62 |
| synth_reference / X101 ECS-327TXO-30-TR | 1; 6 / 10 / 20 | ECS-327TXO-30-TR; Original BOM identifier; price OPEN: 50-ECS-327TXO-30-CT-ND | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| synth_reference / X102 25 MHz | 1; 6 / 10 / 20 | TXETCLSANF-25.000000; Original BOM identifier; price OPEN: 1664-1273-1-ND | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| filter_matching_and_decoupling / C201 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C202 10nF | 1; 6 / 10 / 20 | C0805C103J5GEC7800; Original BOM identifier; price OPEN: 399-C0805C103J5GEC7800CT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C203 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C204 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C205 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C206 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C207 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C208 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C209 10nF | 1; 6 / 10 / 20 | C0805C103J5GEC7800; Original BOM identifier; price OPEN: 399-C0805C103J5GEC7800CT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C210 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C215 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C216 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C217 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C218 100nF | 1; 6 / 10 / 20 | CL21B104KACNNNC; Original BOM identifier; price OPEN: 1276-1099-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C299 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| other_safety_passives / D201 BAT54C | 1; 6 / 10 / 20 | BAT54C,215; Original BOM identifier; price OPEN: 1727-2902-1-ND  | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D202 B330A Schottky Diode | 1; 6 / 10 / 20 | S3AB-13-F; Original BOM identifier; price OPEN: S3AB-FDICT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D203 Schottky Diode | 1; 6 / 10 / 20 | CRS09(TE85L,Q,M); Original BOM identifier; price OPEN: CRS09QCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D204 Schottky Diode | 1; 6 / 10 / 20 | CRS09(TE85L,Q,M); Original BOM identifier; price OPEN: CRS09QCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D206 Schottky Diode | 1; 6 / 10 / 20 | CRS09(TE85L,Q,M); Original BOM identifier; price OPEN: CRS09QCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D207 Schottky Diode | 1; 6 / 10 / 20 | CRS09(TE85L,Q,M); Original BOM identifier; price OPEN: CRS09QCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D208 1N4001 | 1; 6 / 10 / 20 | HS1AFL; Original BOM identifier; price OPEN: HS1AFLCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / D209 1N4001 | 1; 6 / 10 / 20 | HS1AFL; Original BOM identifier; price OPEN: HS1AFLCT-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / F201 2.6A | 1; 6 / 10 / 20 | 0ZCG0260BF2B; Original BOM identifier; price OPEN: 0ZCG0260BF2B | ESTIMATE; 1/1 | 0.2 / 0.2 / 0.2 | 0.20 / 0.20 / 0.20 |
| connectors / J201 Barrel_Jack_Switch | 1; 6 / 10 / 20 | PJ-036AH-SMT-TR; Original BOM identifier; price OPEN: CP-036AHPJCT-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J203 External Fan Power | 1; 6 / 10 / 20 | External Fan Power; MPN OPEN; Original BOM identifier; price OPEN: np | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J204 Controlled Fan Power | 1; 6 / 10 / 20 | Controlled Fan Power; MPN OPEN; Original BOM identifier; price OPEN: np | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| connectors / J205 Controlled Bat Pwr | 1; 6 / 10 / 20 | Controlled Bat Pwr; MPN OPEN; Original BOM identifier; price OPEN: AdaFruit 724 | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| filter_matching_and_decoupling / L201 2.2uH | 1; 6 / 10 / 20 | WPN4020H2R2MT; Original BOM identifier; price OPEN: 3442-WPN4020H2R2MTCT-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| power_and_other_ICs / MOD201 AdaFruit Charger | 1; 6 / 10 / 20 | Product ID: 1904; Original BOM identifier; price OPEN: 1528-1833-ND | ESTIMATE; 1/1 | 5.0 / 5.0 / 5.0 | 5.00 / 5.00 / 5.00 |
| other_safety_passives / R1 TBD | 1; 6 / 10 / 20 | TBD; MPN OPEN; Original BOM identifier; price OPEN: TBD | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R2 TBD | 1; 6 / 10 / 20 | TBD; MPN OPEN; Original BOM identifier; price OPEN: TBD | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R204 162k | 1; 6 / 10 / 20 | RC0805FR-07162KL; Original BOM identifier; price OPEN: 311-162KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R205 12.4k | 1; 6 / 10 / 20 | RC0805FR-0712K4L; Original BOM identifier; price OPEN: 311-12.4KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| power_and_other_ICs / U201 LP2985-3.3 | 1; 6 / 10 / 20 | LP2985A-33DBVR; Original BOM identifier; price OPEN: 296-18479-1-ND | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| power_and_other_ICs / U202 LP2985-3.3 | 1; 6 / 10 / 20 | LP2985A-33DBVR; Original BOM identifier; price OPEN: 296-18479-1-ND | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| power_and_other_ICs / U203 TO-220 ADJ Reg. | 1; 6 / 10 / 20 | LT1086CT#PBF; Original BOM identifier; price OPEN: 505-LT1086CT#PBF-ND | ESTIMATE; 1/1 | 2.0 / 2.0 / 2.0 | 2.00 / 2.00 / 2.00 |
| power_and_other_ICs / U204 | 1; 6 / 10 / 20 | TPS22810DBVT; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/TPS22810DBVT?qs=34RfhUjJmKcpY51nBe7C4Q%3D%3D): 595-TPS22810DBVT | OBSERVED; 1/1 | 0.765 / 0.692 / 0.692 | 0.77 / 0.69 / 0.69 |
| power_and_other_ICs / U205 uA7805 | 1; 6 / 10 / 20 | UA78M05IDCYR; Original BOM identifier; price OPEN: 296-17616-1-ND | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| power_and_other_ICs / U206 | 1; 6 / 10 / 20 | TPS22810DBVT; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/TPS22810DBVT?qs=34RfhUjJmKcpY51nBe7C4Q%3D%3D): 595-TPS22810DBVT | OBSERVED; 1/1 | 0.765 / 0.692 / 0.692 | 0.77 / 0.69 / 0.69 |
| filter_matching_and_decoupling / C301 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C302 1100pF | 1; 6 / 10 / 20 | GRM2195C2A112JA01D; Original BOM identifier; price OPEN: GRM2195C2A112JA01D-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C303 1800pF | 1; 6 / 10 / 20 | GCM2165C2A182GA16D; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C304 91pF | 1; 6 / 10 / 20 | 08051A910FAT2A; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C305 1100pF | 1; 6 / 10 / 20 | GRM2195C2A112JA01D; Original BOM identifier; price OPEN: GRM2195C2A112JA01D-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| connectors / J301 To Antenna | 1; 6 / 10 / 20 | 31-5431; Original BOM identifier; price OPEN: ARF1065-ND | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| filter_matching / L301 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| filter_matching / L302 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| mechanical / Native case/mounting | 1; 6 / 10 / 20 | Native outer case/mounting allowance; OPEN: OPEN | ESTIMATE; 1/1 | 5.0 / 5.0 / 5.0 | 5.00 / 5.00 / 5.00 |
| backup_battery / Backup cell, external operating battery excluded | 1; 6 / 10 / 20 | Adafruit1570 3.7V100mAh backup cell; OPEN: OPEN | ESTIMATE; 1/1 | 5 / 5 / 5 | 5.00 / 5.00 / 5.00 |

## SignalSlinger RF source/driver/PA/filter only

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| synth_reference / U102 | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| synth_reference / X102 25 MHz | 1; 6 / 10 / 20 | TXETCLSANF-25.000000; Original BOM identifier; price OPEN: 1664-1273-1-ND | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| filter_matching_and_decoupling / C105 100nF | 1; 6 / 10 / 20 | CL21B104KACNNNC; Original BOM identifier; price OPEN: 1276-1099-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C106 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C107 100nF | 1; 6 / 10 / 20 | CL21B104KACNNNC; Original BOM identifier; price OPEN: 1276-1099-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C108 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| other_safety_passives / R107 10k | 1; 6 / 10 / 20 | RNCP0805FTD10K0; Original BOM identifier; price OPEN: RNCP0805FTD10K0CT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| other_safety_passives / R108 10k | 1; 6 / 10 / 20 | RNCP0805FTD10K0; Original BOM identifier; price OPEN: RNCP0805FTD10K0CT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |
| drivers / U104 | 1; 6 / 10 / 20 | LM5134BMF/NOPB; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM5134BMF-NOPB?qs=2k4gZbgf%2F9lRirSLUMpZrA%3D%3D): 595-LM5134BMF/NOPB | OBSERVED; 1/1 | 2.17 / 1.62 / 1.62 | 2.17 / 1.62 / 1.62 |
| RF_semiconductors / Q103 | 1; 6 / 10 / 20 | IRF610PBF-BE3; [Farnell](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567): 4853567 | OBSERVED; 1/1 | 1.11 / 0.622 / 0.622 | 1.11 / 0.62 / 0.62 |
| filter_matching / L101 | 1; 6 / 10 / 20 | FT-50A-43 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| filter_matching_and_decoupling / C109 10uF | 1; 6 / 10 / 20 | C2012X5R1V106K125AC; Original BOM identifier; price OPEN: 445-14418-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C110 22uF | 1; 6 / 10 / 20 | CL32A226MAJNNNE; Original BOM identifier; price OPEN: 1276-3373-1-ND | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| filter_matching_and_decoupling / C111 47uF low ESR | 1; 6 / 10 / 20 | T495X476K020ATE150; Original BOM identifier; price OPEN: 399-3904-1-ND | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| filter_matching_and_decoupling / C112 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| power_and_other_ICs / U103 | 1; 6 / 10 / 20 | TPS22810DBVT; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/TPS22810DBVT?qs=34RfhUjJmKcpY51nBe7C4Q%3D%3D): 595-TPS22810DBVT | OBSERVED; 1/1 | 1.06 / 0.765 / 0.765 | 1.06 / 0.77 / 0.77 |
| filter_matching_and_decoupling / C301 470nF | 1; 6 / 10 / 20 | 08051C474K4Z2A; Original BOM identifier; price OPEN: 478-9924-1-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C302 1100pF | 1; 6 / 10 / 20 | GRM2195C2A112JA01D; Original BOM identifier; price OPEN: GRM2195C2A112JA01D-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C303 1800pF | 1; 6 / 10 / 20 | GCM2165C2A182GA16D; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C304 91pF | 1; 6 / 10 / 20 | 08051A910FAT2A; Original BOM identifier; price OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching_and_decoupling / C305 1100pF | 1; 6 / 10 / 20 | GRM2195C2A112JA01D; Original BOM identifier; price OPEN: GRM2195C2A112JA01D-ND | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching / L301 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| filter_matching / L302 | 1; 6 / 10 / 20 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| other_safety_passives / R110 162k | 1; 6 / 10 / 20 | RC0805FR-07162KL; Original BOM identifier; price OPEN: 311-162KCRCT-ND | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.03 / 0.03 / 0.03 |

## ON7YD ATX80 original RF board

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| RF_semiconductors / IRF610 | 1; 6 / 10 / 20 | IRF610PBF-BE3; [Farnell](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567): 4853567 | OBSERVED; 1/1 | 1.11 / 0.622 / 0.622 | 1.11 / 0.62 / 0.62 |
| drivers / CD4001 CMOS quad NOR | 1; 6 / 10 / 20 | CD4001 CMOS quad NOR; OPEN: OPEN | ESTIMATE; 1/1 | 0.35 / 0.35 / 0.35 | 0.35 / 0.35 / 0.35 |
| synth_reference / Fixed3.5MHz crystal stock OPEN | 1; 6 / 10 / 20 | Fixed3.5MHz crystal stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| synth_reference / 10-60p RF trimmer stock OPEN | 1; 6 / 10 / 20 | 10-60p RF trimmer stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| filter_matching / 5uH RFC >=1A | 1; 6 / 10 / 20 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.12 / 0.12 / 0.12 |
| filter_matching / T50-6 26T/24T | 2; 12 / 20 / 40 | T50-6 reference core; exact supplier/winding OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 1.40 / 1.40 / 1.40 |
| filter_matching / Original RF capacitors | 8; 48 / 80 / 160 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.80 / 0.80 / 0.80 |
| passive / 100n block/decoupling | 2; 12 / 20 / 40 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.04 / 0.04 / 0.04 | 0.08 / 0.08 / 0.08 |
| passive / 10u25V | 1; 6 / 10 / 20 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| safety / 1M8/15k and bleed;diagram R2=1k/list15k conflict | 4; 24 / 40 / 80 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.10 / 0.10 / 0.10 |
| thermal / IRF610 sink | 1; 6 / 10 / 20 | Local heat spreader/insulator/mounting pieces OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |

## DF1FO MidiTX RF section

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| RF_semiconductors / SN75452BP | 1; 6 / 10 / 20 | SN75452BP; [Farnell UK](https://uk.farnell.com/texas-instruments/sn75452bp/ic-peripheral-driver-2ch-0-3a/dp/3118981): 3118981 | OBSERVED; 1/1 | 1.2074 / 0.8736 / 0.8736 | 1.21 / 0.87 / 0.87 |
| synth_reference / 3.579545MHz TTL oscillator stock OPEN | 1; 6 / 10 / 20 | 3.579545MHz TTL oscillator stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 1 / 1 / 1 | 1.00 / 1.00 / 1.00 |
| power_conversion / LP2950CZ5 | 1; 6 / 10 / 20 | LP2950CZ5; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |
| filter_matching / 10u RFC/3.3u pi coil | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| filter_matching / FT23-43 1:10 current transformer material | 1; 6 / 10 / 20 | FT23-43 1:10 current transformer material; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |
| filter_matching / 560p/330p/1n/block | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| passive / Decoupling | 4; 24 / 40 / 80 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.04 / 0.04 / 0.028 | 0.16 / 0.16 / 0.11 |
| passive / Rail capacitors | 2; 12 / 20 / 40 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.50 / 0.50 / 0.50 |
| safety / ZF39/1N4148 | 2; 12 / 20 / 40 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.16 / 0.16 / 0.16 |
| mechanical / 300uA meter+trim | 1; 6 / 10 / 20 | 300uA meter+trim; OPEN: OPEN | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |

## DF1FO SprintTX 50-80mW RF section

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| RF_semiconductors / 74HC240 | 1; 6 / 10 / 20 | 74HC240; OPEN: OPEN | ESTIMATE; 1/1 | 0.35 / 0.35 / 0.35 | 0.35 / 0.35 / 0.35 |
| synth_reference / Fixed3.5MHz crystal | 1; 6 / 10 / 20 | Fixed3.5MHz crystal stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| synth_reference / 30p trimmer | 1; 6 / 10 / 20 | 10-60p RF trimmer stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| power_conversion / LP2950CZ5 | 1; 6 / 10 / 20 | LP2950CZ5; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |
| filter_matching / 2.2u/33u/10u/4.7u | 4; 24 / 40 / 80 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.48 / 0.48 / 0.48 |
| filter_matching / 560p/47p/22p | 3; 18 / 30 / 60 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.30 / 0.30 / 0.30 |
| passive / Decoupling | 4; 24 / 40 / 80 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.04 / 0.04 / 0.028 | 0.16 / 0.16 / 0.11 |
| passive / Rail capacitors | 2; 12 / 20 / 40 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.50 / 0.50 / 0.50 |
| safety / Clamp | 2; 12 / 20 / 40 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.16 / 0.16 / 0.16 |
| passive / RF feedback/control | 3; 18 / 30 / 60 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.08 / 0.08 / 0.08 |

## Fixle complete reference estimate

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| controller_RTC / ATtiny25 SMD | 1; 6 / 10 / 20 | ATtiny25 SMD; OPEN: OPEN | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| RF_semiconductors / BC846B | 1; 6 / 10 / 20 | BC846B; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| synth_reference / 3.5795MHz crystal; author .05 limited stock not used | 1; 6 / 10 / 20 | 3.5795MHz crystal; author .05 limited stock not used; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| filter_matching / 20p trimmer current stock/rating OPEN | 1; 6 / 10 / 20 | 20p trimmer current stock/rating OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| filter_matching / 68u/100u | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| passive / 330p x2 | 2; 12 / 20 / 40 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| passive / 10u | 1; 6 / 10 / 20 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.16 / 0.16 / 0.16 |
| passive / 100n | 1; 6 / 10 / 20 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.086 / 0.04 / 0.04 | 0.09 / 0.04 / 0.04 |
| passive / 470x2/33kx2/10k/47 | 6; 36 / 60 / 120 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.15 / 0.15 / 0.15 |
| safety / 1N4001 | 1; 6 / 10 / 20 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.08 / 0.08 / 0.08 |
| mechanical / Case/CR2032 holder/wires/LED/switch/ISP/mounts | 1; 6 / 10 / 20 | Case/CR2032 holder/wires/LED/switch/ISP/mounts; OPEN: OPEN | ESTIMATE; 1/1 | 2.5 / 2.5 / 2.5 | 2.50 / 2.50 / 2.50 |
| battery / NewCR2032 allowance | 1; 6 / 10 / 20 | NewCR2032 allowance; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |

## DF1FO MidiTX complete reference estimate excluding cells/antenna

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| synth_reference / IC1 TTL oscillator | 1; 6 / 10 / 20 | 3.579545MHz TTL oscillator stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 1 / 1 / 1 | 1.00 / 1.00 / 1.00 |
| RF_semiconductors / IC2 | 1; 6 / 10 / 20 | SN75452BP; [Farnell UK](https://uk.farnell.com/texas-instruments/sn75452bp/ic-peripheral-driver-2ch-0-3a/dp/3118981): 3118981 | OBSERVED; 1/1 | 1.2074 / 0.8736 / 0.8736 | 1.21 / 0.87 / 0.87 |
| power_conversion / IC3 | 1; 6 / 10 / 20 | LP2950CZ5; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |
| controller_RTC / IC4 | 1; 6 / 10 / 20 | ATTINY25-20PU native PDIP; OPEN: OPEN | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| safety / D1,D2,D4 | 3; 18 / 30 / 60 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.24 / 0.24 / 0.24 |
| controller_RTC / T1 BC327 | 1; 6 / 10 / 20 | MMBT3904/MMBT3906 equivalent stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| filter_matching / L1/L2 | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| filter_matching / L3/L4 current transformer | 1; 6 / 10 / 20 | FT23-43 1:10 current transformer material; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |
| antenna_matching / External native variometer; wire excluded | 1; 6 / 10 / 20 | Native15-50uH variometer former/core/wire; OPEN: OPEN | ESTIMATE; 1/1 | 2.0 / 2.0 / 2.0 | 2.00 / 2.00 / 2.00 |
| filter_matching / C4,C5,C6 >=500V | 3; 18 / 30 / 60 | RF C0G capacitor >=500 V candidate, exact values/MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.75 / 0.75 / 0.75 |
| passive / C3,C8,C12-C16 | 7; 42 / 70 / 140 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.04 / 0.028 / 0.024 | 0.28 / 0.20 / 0.17 |
| passive / C9,C11 | 2; 12 / 20 / 40 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.50 / 0.50 / 0.50 |
| passive / C10 | 1; 6 / 10 / 20 | 470uF16V electrolytic; OPEN: OPEN | ESTIMATE; 1/1 | 0.35 / 0.35 / 0.35 | 0.35 / 0.35 / 0.35 |
| controller_RTC / C18,C19 | 2; 12 / 20 / 40 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| controller_RTC / C17 | 1; 6 / 10 / 20 | 10-60p RF trimmer stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| passive / C1/C20 price allowance only; actual22n capacitors | 2; 12 / 20 / 40 | 22nF X7R capacitor exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| controller_RTC / Q2 timing4.9152MHz | 1; 6 / 10 / 20 | Fixed3.5MHz crystal stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| passive / R3-R7 | 5; 30 / 50 / 100 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.13 / 0.13 / 0.13 |
| monitor / R2 | 1; 6 / 10 / 20 | Calibration trimmer exact MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.18 / 0.18 / 0.18 | 0.18 / 0.18 / 0.18 |
| mechanical / Meter; trim allocation bundled allowance | 1; 6 / 10 / 20 | 300uA meter+trim; OPEN: OPEN | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| connectors / Two8pin sockets | 2; 12 / 20 / 40 | IC socket; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| connectors / ANT/DIVERSE | 2; 12 / 20 / 40 | Header pair/connection allowance; OPEN: OPEN | ESTIMATE; 1/1 | 0.2 / 0.2 / 0.2 | 0.40 / 0.40 / 0.40 |
| mechanical / Case, LEDD3, controls, FOXPROjack, batteryholder, mounting; no cells | 1; 6 / 10 / 20 | Native case/controls/battery holder/mount material; OPEN: OPEN | ESTIMATE; 1/1 | 5 / 5 / 5 | 5.00 / 5.00 / 5.00 |

## DF1FO SprintTX 50-80mW complete reference estimate excluding cells/antenna

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| power_conversion / IC1 | 1; 6 / 10 / 20 | LP2950CZ5; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |
| RF_semiconductors / IC2 | 1; 6 / 10 / 20 | 74HC240; OPEN: OPEN | ESTIMATE; 1/1 | 0.35 / 0.35 / 0.35 | 0.35 / 0.35 / 0.35 |
| controller_RTC / IC3 | 1; 6 / 10 / 20 | ATTINY25-20PU native PDIP; OPEN: OPEN | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| passive / C1/C3/C5/Csmd | 4; 24 / 40 / 80 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.04 / 0.04 / 0.028 | 0.16 / 0.16 / 0.11 |
| passive / C2/C4 | 2; 12 / 20 / 40 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.50 / 0.50 / 0.50 |
| synth_reference / C6/C11 | 2; 12 / 20 / 40 | 10-60p RF trimmer stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 1.20 / 1.20 / 1.20 |
| filter_matching / C8/C9/C12/C13 | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| passive / C10 22n capacitor price allowance only | 1; 6 / 10 / 20 | 22nF X7R capacitor exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| safety / D1/D2 | 2; 12 / 20 / 40 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.16 / 0.16 / 0.16 |
| filter_matching / L1-L4 | 4; 24 / 40 / 80 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.48 / 0.48 / 0.48 |
| passive / R1-R6 | 6; 36 / 60 / 120 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.15 / 0.15 / 0.15 |
| synth_reference / Q1/Q2 | 2; 12 / 20 / 40 | Fixed3.5MHz crystal stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 1.20 / 1.20 / 1.20 |
| connectors / 20pin/8pin | 2; 12 / 20 / 40 | IC socket; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| connectors / ST1 | 1; 6 / 10 / 20 | Header pair/connection allowance; OPEN: OPEN | ESTIMATE; 1/1 | 0.2 / 0.2 / 0.2 | 0.20 / 0.20 / 0.20 |
| mechanical / Case, LED, controls/2poleDILswitch, terminals, jack, clip and mounts; no9V cell | 1; 6 / 10 / 20 | Native case/controls/battery holder/mount material; OPEN: OPEN | ESTIMATE; 1/1 | 5 / 5 / 5 | 5.00 / 5.00 / 5.00 |

## TinyFox complete reference estimate excluding AA cell

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| RF_semiconductors / 74HC00 | 1; 6 / 10 / 20 | 74HC00D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC00D653?qs=P62ublwmbi%252BGrKfwQ5QbbA%3D%3D): 771-74HC00D-T | OBSERVED; 1/1 | 0.172 / 0.103 / 0.103 | 0.17 / 0.10 / 0.10 |
| controller_RTC / ATtiny13A PU | 1; 6 / 10 / 20 | ATtiny13A PU; OPEN: OPEN | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |
| power_conversion / MAX1724EZK33 lifecycle/stock OPEN | 1; 6 / 10 / 20 | MAX1724EZK33 lifecycle/stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 2 / 2 / 2 | 2.00 / 2.00 / 2.00 |
| synth_reference / Fixed3.579MHz crystal | 1; 6 / 10 / 20 | Fixed3.5MHz crystal stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| filter_matching / 1.6-15p trimmer | 1; 6 / 10 / 20 | 10-60p RF trimmer stock OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| filter_matching / 100u RF/10u boost | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| passive / 33p x2 | 2; 12 / 20 / 40 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| passive / 100n x3 | 3; 18 / 30 / 60 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.04 / 0.04 / 0.028 | 0.12 / 0.12 / 0.08 |
| passive / 10u lowESR x2 | 2; 12 / 20 / 40 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.50 / 0.50 / 0.50 |
| passive / Resistors | 4; 24 / 40 / 80 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.10 / 0.10 / 0.10 |
| mechanical / AA holder/case/30cm antenna24cm stake/switch/headers/LED/mounts | 1; 6 / 10 / 20 | AA holder/case/30cm antenna24cm stake/switch/headers/LED/mounts; OPEN: OPEN | ESTIMATE; 1/1 | 7 / 7 / 7 | 7.00 / 7.00 / 7.00 |

## Proposed Fox-only RF

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| source / SYNTH | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| source / CRYSTAL | 1; 6 / 10 / 20 | 25/27MHz crystal exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| safety / MONO | 1; 6 / 10 / 20 | 74HC123D,653; [Mouser](https://eu.mouser.com/en/ProductDetail/Nexperia/74HC123D653?qs=P62ublwmbi%2FMZUrC9zEqyg%3D%3D): 771-74HC123D-T | OBSERVED; 1/1 | 0.327 / 0.219 / 0.219 | 0.33 / 0.22 / 0.22 |
| safety / LATCH | 1; 6 / 10 / 20 | 74HC74D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC74D653?qs=P62ublwmbi8VnJ1KG1%2FblQ%3D%3D): 771-74HC74D-T | OBSERVED; 1/1 | 0.181 / 0.123 / 0.123 | 0.18 / 0.12 / 0.12 |
| safety / AND | 1; 6 / 10 / 20 | 74HC08D,653; [Mouser](https://eu.mouser.com/ProductDetail/Nexperia/74HC08D653?qs=P62ublwmbi%2FQCxm29EB%2FyA%3D%3D): 771-74HC08D-T | OBSERVED; 1/1 | 0.163 / 0.114 / 0.114 | 0.16 / 0.11 / 0.11 |
| safety / POR | 1; 6 / 10 / 20 | MCP100T-300I/TT; [Mouser](https://www.mouser.it/ProductDetail/Microchip-Technology/MCP100T-300I-TT?qs=8U9qMIGhlkokseONjNxnUg%3D%3D): 579-MCP100T-300I/TT | OBSERVED; 1/1 | 0.361 / 0.361 / 0.361 | 0.36 / 0.36 / 0.36 |
| safety / CMP | 1; 6 / 10 / 20 | LM393BIDR; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM393BIDR?qs=BJlw7L4Cy78N8CV%252BGpRosA%3D%3D): 595-LM393BIDR | OBSERVED; 1/1 | 0.198 / 0.14 / 0.14 | 0.20 / 0.14 / 0.14 |
| connector / INTERFACE | 1; 6 / 10 / 20 | Polarized logic PCB connector candidate family OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.45 / 0.45 / 0.45 | 0.45 / 0.45 / 0.45 |
| monitor / SHUNT | 1; 6 / 10 / 20 | Low-ohm1% current shunt MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| monitor / NTC | 1; 6 / 10 / 20 | 10k NTC MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| protection / BEAD | 3; 18 / 30 / 60 | Ferrite bead exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.24 / 0.24 / 0.24 |
| protection / DIODE | 6; 36 / 60 / 120 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.48 / 0.48 / 0.48 |
| safety / SMALLFET | 3; 18 / 30 / 60 | 2N7002 equivalent exact stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.30 / 0.30 / 0.30 |
| shield / SHIELD | 1; 6 / 10 / 20 | RF shield frame/lid material exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| passive / R10K | 8; 48 / 80 / 160 | RC0603FR-0710KL; [Mouser](https://www.mouser.de/en/ProductDetail/YAGEO/RC0603FR-0710KL?qs=sGAEpiMZZMtlubZbdhIBIAhzU1Tw%252BHVakiDuQ4Zki0U%3D): 603-RC0603FR-0710KL | OBSERVED; 1/1 | 0.012 / 0.012 / 0.007 | 0.10 / 0.10 / 0.06 |
| filter / RFCOIL | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| filter / C0G | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| monitor / RFDET | 1; 6 / 10 / 20 | RF Schottky detector exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.15 / 0.15 / 0.15 | 0.15 / 0.15 / 0.15 |
| shape / SMALLBJT | 2; 12 / 20 / 40 | MMBT3904/MMBT3906 equivalent stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| fox / PADRES | 6; 36 / 60 / 120 | RF pad/current-limit resistor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.06 / 0.06 / 0.06 | 0.36 / 0.36 / 0.36 |
| passive / C100N | 6; 36 / 60 / 120 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.04 / 0.028 / 0.024 | 0.24 / 0.17 / 0.14 |
| passive / CBULK | 2; 12 / 20 / 40 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.32 / 0.32 / 0.32 |
| passive / RES | 12; 72 / 120 / 240 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.30 / 0.30 / 0.30 |
| safety / Source rail hard-off without I2C backfeed | 1; 6 / 10 / 20 | Dual I2C bus isolation switch e.g. SN74LVC2G66DCUR; exact selection OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| fox / TinyFox buffer mechanism; no local crystal/MCU/AA boost | 1; 6 / 10 / 20 | 74HC00D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC00D653?qs=P62ublwmbi%252BGrKfwQ5QbbA%3D%3D): 771-74HC00D-T | OBSERVED; 1/1 | 0.172 / 0.103 / 0.103 | 0.17 / 0.10 / 0.10 |
| fox / Fixed calibration selections replace trimmer; values OPEN | 2; 12 / 20 / 40 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.05 / 0.05 / 0.05 |
| safety / Preserved unquoted guard/limit completion provision | 1; 6 / 10 / 20 | Bounded low-path guard/limit completion provision; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |

## Proposed 1.2W Classic/Sprint + Fox RF

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| source / SYNTH | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| source / CRYSTAL | 1; 6 / 10 / 20 | 25/27MHz crystal exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| safety / MONO | 1; 6 / 10 / 20 | 74HC123D,653; [Mouser](https://eu.mouser.com/en/ProductDetail/Nexperia/74HC123D653?qs=P62ublwmbi%2FMZUrC9zEqyg%3D%3D): 771-74HC123D-T | OBSERVED; 1/1 | 0.327 / 0.219 / 0.219 | 0.33 / 0.22 / 0.22 |
| safety / LATCH | 1; 6 / 10 / 20 | 74HC74D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC74D653?qs=P62ublwmbi8VnJ1KG1%2FblQ%3D%3D): 771-74HC74D-T | OBSERVED; 1/1 | 0.181 / 0.123 / 0.123 | 0.18 / 0.12 / 0.12 |
| safety / AND | 1; 6 / 10 / 20 | 74HC08D,653; [Mouser](https://eu.mouser.com/ProductDetail/Nexperia/74HC08D653?qs=P62ublwmbi%2FQCxm29EB%2FyA%3D%3D): 771-74HC08D-T | OBSERVED; 1/1 | 0.163 / 0.114 / 0.114 | 0.16 / 0.11 / 0.11 |
| safety / POR | 1; 6 / 10 / 20 | MCP100T-300I/TT; [Mouser](https://www.mouser.it/ProductDetail/Microchip-Technology/MCP100T-300I-TT?qs=8U9qMIGhlkokseONjNxnUg%3D%3D): 579-MCP100T-300I/TT | OBSERVED; 1/1 | 0.361 / 0.361 / 0.361 | 0.36 / 0.36 / 0.36 |
| safety / CMP | 1; 6 / 10 / 20 | LM393BIDR; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM393BIDR?qs=BJlw7L4Cy78N8CV%252BGpRosA%3D%3D): 595-LM393BIDR | OBSERVED; 1/1 | 0.14 / 0.14 / 0.124 | 0.14 / 0.14 / 0.12 |
| connector / INTERFACE | 1; 6 / 10 / 20 | Polarized logic PCB connector candidate family OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.45 / 0.45 / 0.45 | 0.45 / 0.45 / 0.45 |
| monitor / SHUNT | 1; 6 / 10 / 20 | Low-ohm1% current shunt MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| monitor / NTC | 1; 6 / 10 / 20 | 10k NTC MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| protection / BEAD | 3; 18 / 30 / 60 | Ferrite bead exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.24 / 0.24 / 0.24 |
| protection / DIODE | 6; 36 / 60 / 120 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.48 / 0.48 / 0.48 |
| safety / SMALLFET | 3; 18 / 30 / 60 | 2N7002 equivalent exact stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.30 / 0.30 / 0.30 |
| shield / SHIELD | 1; 6 / 10 / 20 | RF shield frame/lid material exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| passive / R10K | 8; 48 / 80 / 160 | RC0603FR-0710KL; [Mouser](https://www.mouser.de/en/ProductDetail/YAGEO/RC0603FR-0710KL?qs=sGAEpiMZZMtlubZbdhIBIAhzU1Tw%252BHVakiDuQ4Zki0U%3D): 603-RC0603FR-0710KL | OBSERVED; 1/1 | 0.012 / 0.012 / 0.007 | 0.10 / 0.10 / 0.06 |
| filter / RFCOIL | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| filter / C0G | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| monitor / RFDET | 1; 6 / 10 / 20 | RF Schottky detector exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.15 / 0.15 / 0.15 | 0.15 / 0.15 / 0.15 |
| shape / SMALLBJT | 2; 12 / 20 / 40 | MMBT3904/MMBT3906 equivalent stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| fox / PADRES | 6; 36 / 60 / 120 | RF pad/current-limit resistor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.06 / 0.06 / 0.06 | 0.36 / 0.36 / 0.36 |
| passive / C100N | 6; 36 / 60 / 120 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.028 / 0.024 / 0.024 | 0.17 / 0.14 / 0.14 |
| passive / CBULK | 2; 12 / 20 / 40 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.32 / 0.32 / 0.32 |
| passive / RES | 12; 72 / 120 / 240 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.30 / 0.30 / 0.30 |
| safety / Source rail hard-off without I2C backfeed | 1; 6 / 10 / 20 | Dual I2C bus isolation switch e.g. SN74LVC2G66DCUR; exact selection OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| fox / TinyFox buffer mechanism; no local crystal/MCU/AA boost | 1; 6 / 10 / 20 | 74HC00D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC00D653?qs=P62ublwmbi%252BGrKfwQ5QbbA%3D%3D): 771-74HC00D-T | OBSERVED; 1/1 | 0.172 / 0.103 / 0.103 | 0.17 / 0.10 / 0.10 |
| fox / Fixed calibration selections replace trimmer; values OPEN | 2; 12 / 20 / 40 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.05 / 0.05 / 0.05 |
| safety / Preserved unquoted guard/limit completion provision | 1; 6 / 10 / 20 | Bounded low-path guard/limit completion provision; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| RF_semiconductors / HFPA | 1; 6 / 10 / 20 | IRF610PBF-BE3; [Farnell](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567): 4853567 | OBSERVED; 1/1 | 1.11 / 0.622 / 0.622 | 1.11 / 0.62 / 0.62 |
| drivers / LM5134B | 1; 6 / 10 / 20 | LM5134BMF/NOPB; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM5134BMF-NOPB?qs=2k4gZbgf%2F9lRirSLUMpZrA%3D%3D): 595-LM5134BMF/NOPB | OBSERVED; 1/1 | 2.17 / 1.62 / 1.62 | 2.17 / 1.62 / 1.62 |
| safety / Actual PA rail disconnect, not converter EN alone | 2; 12 / 20 / 40 | DMP4015SPS-13; [Mouser](https://eu.mouser.com/en/ProductDetail/Diodes-Incorporated/DMP4015SPS-13?qs=gfe7vQ8txpUdN3mXhLzzsQ%3D%3D): 621-DMP4015SPS-13 | OBSERVED; 1/1 | 0.646 / 0.646 / 0.646 | 1.29 / 1.29 / 1.29 |
| safety / Additional watt OC/temperature channels | 1; 6 / 10 / 20 | LM393BIDR; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM393BIDR?qs=BJlw7L4Cy78N8CV%252BGpRosA%3D%3D): 595-LM393BIDR | OBSERVED; 1/1 | 0.14 / 0.14 / 0.124 | 0.14 / 0.14 / 0.12 |
| filter_matching / SignalSlinger L101 9T #24 FT-50A-43 | 1; 6 / 10 / 20 | FT-50A-43 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| filter_matching / SignalSlinger L301/L302 20T #24 T60-2 | 2; 12 / 20 / 40 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 1.40 / 1.40 / 1.40 |
| filter_matching / 1100p x2,1800p,91p; voltage/MPNs OPEN | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| filter_matching / 470nF RF DC block | 1; 6 / 10 / 20 | 470nF 100V RF block MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.15 / 0.15 / 0.15 | 0.15 / 0.15 / 0.15 |
| shape / QCX integrator pass transistor; exact-vendor SOA gate | 1; 6 / 10 / 20 | MPS751 PBFREE; [Mouser](https://www.mouser.fr/fr/ProductDetail/Central-Semiconductor/MPS751-PBFREE?qs=u16ybLDytRaifCWlk5BiIw%3D%3D): 610-MPS751 | OBSERVED; 1/1 | 1.04 / 0.72 / 0.72 | 1.04 / 0.72 / 0.72 |
| shape / QCX Q4 function; substitute 2N7002 needs qualification | 1; 6 / 10 / 20 | 2N7002 equivalent exact stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| shape / RC integrator + gate bleed/stop; values OPEN | 4; 24 / 40 / 80 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.10 / 0.10 / 0.10 |
| shape / 2.2uF RC capacitor starting value, not PA reservoir | 1; 6 / 10 / 20 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.16 / 0.16 / 0.16 |
| passive / C100N | 4; 24 / 40 / 80 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.028 / 0.024 / 0.024 | 0.11 / 0.10 / 0.10 |
| passive / CBULK | 2; 12 / 20 / 40 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.32 / 0.32 / 0.32 |
| passive / Local rail reservoirs upstream of shaped drain | 2; 12 / 20 / 40 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.50 / 0.50 / 0.50 |
| power_conversion / INDUCTOR | 1; 6 / 10 / 20 | Power inductor exact MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| thermal / SINK | 1; 6 / 10 / 20 | Local heat spreader/insulator/mounting pieces OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| power_conversion / TPS62160: output <=6V; not a higher-power supply | 1; 6 / 10 / 20 | TPS62160DGKT; [DigiKey](https://www.digikey.de/de/products/detail/texas-instruments/TPS62160DGKT/3074519): 296-30318-1-ND | OBSERVED; 1/1 | 1.9 / 1.408 / 1.408 | 1.90 / 1.41 / 1.41 |
| power_conversion / Bounded two-level feedback and bleeders | 4; 24 / 40 / 80 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.10 / 0.10 / 0.10 |

## Proposed 2-3W/5W supply alternative + Fox RF

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| source / SYNTH | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| source / CRYSTAL | 1; 6 / 10 / 20 | 25/27MHz crystal exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| safety / MONO | 1; 6 / 10 / 20 | 74HC123D,653; [Mouser](https://eu.mouser.com/en/ProductDetail/Nexperia/74HC123D653?qs=P62ublwmbi%2FMZUrC9zEqyg%3D%3D): 771-74HC123D-T | OBSERVED; 1/1 | 0.327 / 0.219 / 0.219 | 0.33 / 0.22 / 0.22 |
| safety / LATCH | 1; 6 / 10 / 20 | 74HC74D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC74D653?qs=P62ublwmbi8VnJ1KG1%2FblQ%3D%3D): 771-74HC74D-T | OBSERVED; 1/1 | 0.181 / 0.123 / 0.123 | 0.18 / 0.12 / 0.12 |
| safety / AND | 1; 6 / 10 / 20 | 74HC08D,653; [Mouser](https://eu.mouser.com/ProductDetail/Nexperia/74HC08D653?qs=P62ublwmbi%2FQCxm29EB%2FyA%3D%3D): 771-74HC08D-T | OBSERVED; 1/1 | 0.163 / 0.114 / 0.114 | 0.16 / 0.11 / 0.11 |
| safety / POR | 1; 6 / 10 / 20 | MCP100T-300I/TT; [Mouser](https://www.mouser.it/ProductDetail/Microchip-Technology/MCP100T-300I-TT?qs=8U9qMIGhlkokseONjNxnUg%3D%3D): 579-MCP100T-300I/TT | OBSERVED; 1/1 | 0.361 / 0.361 / 0.361 | 0.36 / 0.36 / 0.36 |
| safety / CMP | 1; 6 / 10 / 20 | LM393BIDR; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM393BIDR?qs=BJlw7L4Cy78N8CV%252BGpRosA%3D%3D): 595-LM393BIDR | OBSERVED; 1/1 | 0.14 / 0.14 / 0.124 | 0.14 / 0.14 / 0.12 |
| connector / INTERFACE | 1; 6 / 10 / 20 | Polarized logic PCB connector candidate family OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.45 / 0.45 / 0.45 | 0.45 / 0.45 / 0.45 |
| monitor / SHUNT | 1; 6 / 10 / 20 | Low-ohm1% current shunt MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| monitor / NTC | 1; 6 / 10 / 20 | 10k NTC MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| protection / BEAD | 3; 18 / 30 / 60 | Ferrite bead exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.24 / 0.24 / 0.24 |
| protection / DIODE | 6; 36 / 60 / 120 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.48 / 0.48 / 0.48 |
| safety / SMALLFET | 3; 18 / 30 / 60 | 2N7002 equivalent exact stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.30 / 0.30 / 0.30 |
| shield / SHIELD | 1; 6 / 10 / 20 | RF shield frame/lid material exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| passive / R10K | 8; 48 / 80 / 160 | RC0603FR-0710KL; [Mouser](https://www.mouser.de/en/ProductDetail/YAGEO/RC0603FR-0710KL?qs=sGAEpiMZZMtlubZbdhIBIAhzU1Tw%252BHVakiDuQ4Zki0U%3D): 603-RC0603FR-0710KL | OBSERVED; 1/1 | 0.012 / 0.012 / 0.007 | 0.10 / 0.10 / 0.06 |
| filter / RFCOIL | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| filter / C0G | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| monitor / RFDET | 1; 6 / 10 / 20 | RF Schottky detector exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.15 / 0.15 / 0.15 | 0.15 / 0.15 / 0.15 |
| shape / SMALLBJT | 2; 12 / 20 / 40 | MMBT3904/MMBT3906 equivalent stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| fox / PADRES | 6; 36 / 60 / 120 | RF pad/current-limit resistor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.06 / 0.06 / 0.06 | 0.36 / 0.36 / 0.36 |
| passive / C100N | 6; 36 / 60 / 120 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.028 / 0.024 / 0.024 | 0.17 / 0.14 / 0.14 |
| passive / CBULK | 2; 12 / 20 / 40 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.32 / 0.32 / 0.32 |
| passive / RES | 12; 72 / 120 / 240 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.30 / 0.30 / 0.30 |
| safety / Source rail hard-off without I2C backfeed | 1; 6 / 10 / 20 | Dual I2C bus isolation switch e.g. SN74LVC2G66DCUR; exact selection OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| fox / TinyFox buffer mechanism; no local crystal/MCU/AA boost | 1; 6 / 10 / 20 | 74HC00D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC00D653?qs=P62ublwmbi%252BGrKfwQ5QbbA%3D%3D): 771-74HC00D-T | OBSERVED; 1/1 | 0.172 / 0.103 / 0.103 | 0.17 / 0.10 / 0.10 |
| fox / Fixed calibration selections replace trimmer; values OPEN | 2; 12 / 20 / 40 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.05 / 0.05 / 0.05 |
| safety / Preserved unquoted guard/limit completion provision | 1; 6 / 10 / 20 | Bounded low-path guard/limit completion provision; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| RF_semiconductors / HFPA | 1; 6 / 10 / 20 | IRF610PBF-BE3; [Farnell](https://de.farnell.com/vishay/irf610pbf-be3/mosfet-n-kanal-200v-3-3a-to-220ab/dp/4853567): 4853567 | OBSERVED; 1/1 | 1.11 / 0.622 / 0.622 | 1.11 / 0.62 / 0.62 |
| drivers / LM5134B | 1; 6 / 10 / 20 | LM5134BMF/NOPB; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM5134BMF-NOPB?qs=2k4gZbgf%2F9lRirSLUMpZrA%3D%3D): 595-LM5134BMF/NOPB | OBSERVED; 1/1 | 2.17 / 1.62 / 1.62 | 2.17 / 1.62 / 1.62 |
| safety / Actual PA rail disconnect, not converter EN alone | 2; 12 / 20 / 40 | DMP4015SPS-13; [Mouser](https://eu.mouser.com/en/ProductDetail/Diodes-Incorporated/DMP4015SPS-13?qs=gfe7vQ8txpUdN3mXhLzzsQ%3D%3D): 621-DMP4015SPS-13 | OBSERVED; 1/1 | 0.646 / 0.646 / 0.646 | 1.29 / 1.29 / 1.29 |
| safety / Additional watt OC/temperature channels | 1; 6 / 10 / 20 | LM393BIDR; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM393BIDR?qs=BJlw7L4Cy78N8CV%252BGpRosA%3D%3D): 595-LM393BIDR | OBSERVED; 1/1 | 0.14 / 0.14 / 0.124 | 0.14 / 0.14 / 0.12 |
| filter_matching / SignalSlinger L101 9T #24 FT-50A-43 | 1; 6 / 10 / 20 | FT-50A-43 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| filter_matching / SignalSlinger L301/L302 20T #24 T60-2 | 2; 12 / 20 / 40 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 1.40 / 1.40 / 1.40 |
| filter_matching / 1100p x2,1800p,91p; voltage/MPNs OPEN | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| filter_matching / 470nF RF DC block | 1; 6 / 10 / 20 | 470nF 100V RF block MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.15 / 0.15 / 0.15 | 0.15 / 0.15 / 0.15 |
| shape / QCX integrator pass transistor; exact-vendor SOA gate | 1; 6 / 10 / 20 | MPS751 PBFREE; [Mouser](https://www.mouser.fr/fr/ProductDetail/Central-Semiconductor/MPS751-PBFREE?qs=u16ybLDytRaifCWlk5BiIw%3D%3D): 610-MPS751 | OBSERVED; 1/1 | 1.04 / 0.72 / 0.72 | 1.04 / 0.72 / 0.72 |
| shape / QCX Q4 function; substitute 2N7002 needs qualification | 1; 6 / 10 / 20 | 2N7002 equivalent exact stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| shape / RC integrator + gate bleed/stop; values OPEN | 4; 24 / 40 / 80 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.10 / 0.10 / 0.10 |
| shape / 2.2uF RC capacitor starting value, not PA reservoir | 1; 6 / 10 / 20 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.16 / 0.16 / 0.16 |
| passive / C100N | 4; 24 / 40 / 80 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.028 / 0.024 / 0.024 | 0.11 / 0.10 / 0.10 |
| passive / CBULK | 2; 12 / 20 / 40 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.32 / 0.32 / 0.32 |
| passive / Local rail reservoirs upstream of shaped drain | 2; 12 / 20 / 40 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.50 / 0.50 / 0.50 |
| power_conversion / INDUCTOR | 1; 6 / 10 / 20 | Power inductor exact MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| thermal / SINK | 1; 6 / 10 / 20 | Local heat spreader/insulator/mounting pieces OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| power_conversion / LTC3600 | 1; 6 / 10 / 20 | LTC3600EMSE#PBF; [Mouser](https://www.mouser.de/c/power/power-management-ics/voltage-regulators-switching-regulators/?series=LTC3600): OPEN: exact supplier SKU not captured | OBSERVED; 1/1 | 7.89 / 6.13 / 6.13 | 7.89 / 6.13 / 6.13 |
| power_conversion / OPA171 | 1; 6 / 10 / 20 | OPA171AIDBVR; OPEN: OPEN | ESTIMATE; 1/1 | 1.2 / 1.2 / 1.2 | 1.20 / 1.20 / 1.20 |
| power_conversion / BOOST | 1; 6 / 10 / 20 | TPS611781RNWR; [Mouser](https://www.mouser.ee/ProductDetail/Texas-Instruments/TPS611781RNWR?qs=Mv7BduZupUjx2ZfyDo32jQ%3D%3D): 595-TPS611781RNWR | OBSERVED; 1/1 | 2.79 / 2.09 / 2.09 | 2.79 / 2.09 / 2.09 |
| power_conversion / INDUCTOR | 1; 6 / 10 / 20 | Power inductor exact MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| power_conversion / CBULK | 2; 12 / 20 / 40 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.32 / 0.32 / 0.32 |
| power_conversion / CELECT | 1; 6 / 10 / 20 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| power_conversion / RES | 8; 48 / 80 / 160 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.20 / 0.20 / 0.20 |
| power_conversion / RFCOIL | 1; 6 / 10 / 20 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.12 / 0.12 / 0.12 |
| thermal / Continuous 5W thermal provision | 1; 6 / 10 / 20 | 5W thermal/mounting increment; OPEN: OPEN | ESTIMATE; 1/1 | 1.5 / 1.5 / 1.5 | 1.50 / 1.50 / 1.50 |

## DF1FO mechanism adapted to protected programmable module allowance

| Category / reference function | Qty/unit; needed 6 / 10 / 20 | MPN / supplier code | Price evidence; MOQ/multiple | Unit EUR 6 / 10 / 20 | Extended EUR 6 / 10 / 20 |
| --- | --- | --- | --- | --- | --- |
| source / SYNTH | 1; 6 / 10 / 20 | SI5351A-B-GT; [DigiKey](https://www.digikey.de/en/products/detail/skyworks-solutions-inc/SI5351A-B-GT/3679847): 336-2399-5-ND | OBSERVED; 1/1 | 1.87 / 1.388 / 1.388 | 1.87 / 1.39 / 1.39 |
| source / CRYSTAL | 1; 6 / 10 / 20 | 25/27MHz crystal exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.4 / 0.4 / 0.4 | 0.40 / 0.40 / 0.40 |
| safety / MONO | 1; 6 / 10 / 20 | 74HC123D,653; [Mouser](https://eu.mouser.com/en/ProductDetail/Nexperia/74HC123D653?qs=P62ublwmbi%2FMZUrC9zEqyg%3D%3D): 771-74HC123D-T | OBSERVED; 1/1 | 0.327 / 0.219 / 0.219 | 0.33 / 0.22 / 0.22 |
| safety / LATCH | 1; 6 / 10 / 20 | 74HC74D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC74D653?qs=P62ublwmbi8VnJ1KG1%2FblQ%3D%3D): 771-74HC74D-T | OBSERVED; 1/1 | 0.181 / 0.123 / 0.123 | 0.18 / 0.12 / 0.12 |
| safety / AND | 1; 6 / 10 / 20 | 74HC08D,653; [Mouser](https://eu.mouser.com/ProductDetail/Nexperia/74HC08D653?qs=P62ublwmbi%2FQCxm29EB%2FyA%3D%3D): 771-74HC08D-T | OBSERVED; 1/1 | 0.163 / 0.114 / 0.114 | 0.16 / 0.11 / 0.11 |
| safety / POR | 1; 6 / 10 / 20 | MCP100T-300I/TT; [Mouser](https://www.mouser.it/ProductDetail/Microchip-Technology/MCP100T-300I-TT?qs=8U9qMIGhlkokseONjNxnUg%3D%3D): 579-MCP100T-300I/TT | OBSERVED; 1/1 | 0.361 / 0.361 / 0.361 | 0.36 / 0.36 / 0.36 |
| safety / CMP | 1; 6 / 10 / 20 | LM393BIDR; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM393BIDR?qs=BJlw7L4Cy78N8CV%252BGpRosA%3D%3D): 595-LM393BIDR | OBSERVED; 1/1 | 0.14 / 0.14 / 0.124 | 0.14 / 0.14 / 0.12 |
| connector / INTERFACE | 1; 6 / 10 / 20 | Polarized logic PCB connector candidate family OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.45 / 0.45 / 0.45 | 0.45 / 0.45 / 0.45 |
| monitor / SHUNT | 1; 6 / 10 / 20 | Low-ohm1% current shunt MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| monitor / NTC | 1; 6 / 10 / 20 | 10k NTC MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| protection / BEAD | 3; 18 / 30 / 60 | Ferrite bead exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.24 / 0.24 / 0.24 |
| protection / DIODE | 6; 36 / 60 / 120 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.48 / 0.48 / 0.48 |
| safety / SMALLFET | 3; 18 / 30 / 60 | 2N7002 equivalent exact stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.30 / 0.30 / 0.30 |
| shield / SHIELD | 1; 6 / 10 / 20 | RF shield frame/lid material exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 0.70 / 0.70 / 0.70 |
| passive / R10K | 8; 48 / 80 / 160 | RC0603FR-0710KL; [Mouser](https://www.mouser.de/en/ProductDetail/YAGEO/RC0603FR-0710KL?qs=sGAEpiMZZMtlubZbdhIBIAhzU1Tw%252BHVakiDuQ4Zki0U%3D): 603-RC0603FR-0710KL | OBSERVED; 1/1 | 0.012 / 0.012 / 0.007 | 0.10 / 0.10 / 0.06 |
| filter / RFCOIL | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| filter / C0G | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| monitor / RFDET | 1; 6 / 10 / 20 | RF Schottky detector exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.15 / 0.15 / 0.15 | 0.15 / 0.15 / 0.15 |
| shape / SMALLBJT | 2; 12 / 20 / 40 | MMBT3904/MMBT3906 equivalent stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.20 / 0.20 / 0.20 |
| fox / PADRES | 6; 36 / 60 / 120 | RF pad/current-limit resistor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.06 / 0.06 / 0.06 | 0.36 / 0.36 / 0.36 |
| passive / C100N | 6; 36 / 60 / 120 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.028 / 0.024 / 0.024 | 0.17 / 0.14 / 0.14 |
| passive / CBULK | 2; 12 / 20 / 40 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.32 / 0.32 / 0.32 |
| passive / RES | 12; 72 / 120 / 240 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.30 / 0.30 / 0.30 |
| safety / Source rail hard-off without I2C backfeed | 1; 6 / 10 / 20 | Dual I2C bus isolation switch e.g. SN74LVC2G66DCUR; exact selection OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.25 / 0.25 / 0.25 |
| fox / TinyFox buffer mechanism; no local crystal/MCU/AA boost | 1; 6 / 10 / 20 | 74HC00D,653; [Mouser](https://nl.mouser.com/ProductDetail/Nexperia/74HC00D653?qs=P62ublwmbi%252BGrKfwQ5QbbA%3D%3D): 771-74HC00D-T | OBSERVED; 1/1 | 0.172 / 0.103 / 0.103 | 0.17 / 0.10 / 0.10 |
| fox / Fixed calibration selections replace trimmer; values OPEN | 2; 12 / 20 / 40 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.05 / 0.05 / 0.05 |
| safety / Preserved unquoted guard/limit completion provision | 1; 6 / 10 / 20 | Bounded low-path guard/limit completion provision; OPEN: OPEN | ESTIMATE; 1/1 | 0.75 / 0.75 / 0.75 | 0.75 / 0.75 / 0.75 |
| safety / Actual PA rail disconnect, not converter EN alone | 2; 12 / 20 / 40 | DMP4015SPS-13; [Mouser](https://eu.mouser.com/en/ProductDetail/Diodes-Incorporated/DMP4015SPS-13?qs=gfe7vQ8txpUdN3mXhLzzsQ%3D%3D): 621-DMP4015SPS-13 | OBSERVED; 1/1 | 0.646 / 0.646 / 0.646 | 1.29 / 1.29 / 1.29 |
| safety / Additional watt OC/temperature channels | 1; 6 / 10 / 20 | LM393BIDR; [Mouser](https://eu.mouser.com/en/ProductDetail/Texas-Instruments/LM393BIDR?qs=BJlw7L4Cy78N8CV%252BGpRosA%3D%3D): 595-LM393BIDR | OBSERVED; 1/1 | 0.14 / 0.14 / 0.124 | 0.14 / 0.14 / 0.12 |
| filter_matching / SignalSlinger L301/L302 20T #24 T60-2 | 2; 12 / 20 / 40 | T60-2 + #24 wire; OPEN: OPEN | ESTIMATE; 1/1 | 0.7 / 0.7 / 0.7 | 1.40 / 1.40 / 1.40 |
| filter_matching / 1100p x2,1800p,91p; voltage/MPNs OPEN | 4; 24 / 40 / 80 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.40 / 0.40 / 0.40 |
| filter_matching / 470nF RF DC block | 1; 6 / 10 / 20 | 470nF 100V RF block MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.15 / 0.15 / 0.15 | 0.15 / 0.15 / 0.15 |
| shape / QCX integrator pass transistor; exact-vendor SOA gate | 1; 6 / 10 / 20 | MPS751 PBFREE; [Mouser](https://www.mouser.fr/fr/ProductDetail/Central-Semiconductor/MPS751-PBFREE?qs=u16ybLDytRaifCWlk5BiIw%3D%3D): 610-MPS751 | OBSERVED; 1/1 | 1.04 / 0.72 / 0.72 | 1.04 / 0.72 / 0.72 |
| shape / QCX Q4 function; substitute 2N7002 needs qualification | 1; 6 / 10 / 20 | 2N7002 equivalent exact stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| shape / RC integrator + gate bleed/stop; values OPEN | 4; 24 / 40 / 80 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.10 / 0.10 / 0.10 |
| shape / 2.2uF RC capacitor starting value, not PA reservoir | 1; 6 / 10 / 20 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.16 / 0.16 / 0.16 |
| passive / C100N | 4; 24 / 40 / 80 | CC0603KRX7R8BB104; [Mouser](https://www.mouser.de/de/ProductDetail/YAGEO/CC0603KRX7R8BB104?qs=sGAEpiMZZMvsSlwiRhF8qj9NgEuXmwzvrkjJ%252BgSm7QM%3D): 603-CC603KRX7R8BB104 | OBSERVED; 1/1 | 0.028 / 0.024 / 0.024 | 0.11 / 0.10 / 0.10 |
| passive / CBULK | 2; 12 / 20 / 40 | 10-22uF25V X7R MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.16 / 0.16 / 0.16 | 0.32 / 0.32 / 0.32 |
| passive / Local rail reservoirs upstream of shaped drain | 2; 12 / 20 / 40 | 100-220uF25V lowESR MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.25 / 0.25 / 0.25 | 0.50 / 0.50 / 0.50 |
| power_conversion / INDUCTOR | 1; 6 / 10 / 20 | Power inductor exact MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.8 / 0.8 / 0.8 | 0.80 / 0.80 / 0.80 |
| thermal / SINK | 1; 6 / 10 / 20 | Local heat spreader/insulator/mounting pieces OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.6 / 0.6 / 0.6 | 0.60 / 0.60 / 0.60 |
| power_conversion / Bounded two-level feedback and bleeders | 4; 24 / 40 / 80 | E24/E96 resistor other values MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.025 / 0.025 / 0.025 | 0.10 / 0.10 / 0.10 |
| RF_semiconductors / Native DF1FO output mechanism | 1; 6 / 10 / 20 | SN75452BP; [Farnell UK](https://uk.farnell.com/texas-instruments/sn75452bp/ic-peripheral-driver-2ch-0-3a/dp/3118981): 3118981 | OBSERVED; 1/1 | 1.2074 / 0.8736 / 0.8736 | 1.21 / 0.87 / 0.87 |
| power_conversion / Regulated9V output, no direct depleted2S claim | 1; 6 / 10 / 20 | TPS611781RNWR; [Mouser](https://www.mouser.ee/ProductDetail/Texas-Instruments/TPS611781RNWR?qs=Mv7BduZupUjx2ZfyDo32jQ%3D%3D): 595-TPS611781RNWR | OBSERVED; 1/1 | 2.79 / 2.09 / 2.09 | 2.79 / 2.09 / 2.09 |
| power_conversion / Required5V logic rail | 1; 6 / 10 / 20 | LP2950CZ5; OPEN: OPEN | ESTIMATE; 1/1 | 0.5 / 0.5 / 0.5 | 0.50 / 0.50 / 0.50 |
| filter_matching / Drain feed/native matching adjustment | 2; 12 / 20 / 40 | VHF aircoil/80m choke MPN or winding recipe OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.12 / 0.12 / 0.12 | 0.24 / 0.24 / 0.24 |
| filter_matching / Native matching retained before50ohm LPF | 3; 18 / 30 / 60 | C0G50-100V RF capacitor MPN/value OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.30 / 0.30 / 0.30 |
| safety / Native drain spike clamp | 1; 6 / 10 / 20 | Small signal/clamp diode exact MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.08 / 0.08 / 0.08 | 0.08 / 0.08 / 0.08 |
| shape / Bounded mode adjustment | 1; 6 / 10 / 20 | 2N7002 equivalent exact stocked MPN OPEN; OPEN: OPEN | ESTIMATE; 1/1 | 0.1 / 0.1 / 0.1 | 0.10 / 0.10 / 0.10 |
| shape / DC mode adjustment allowance; implementation OPEN | 1; 6 / 10 / 20 | LM2904BIDR; [Mouser](https://eu.mouser.com/ProductDetail/Texas-Instruments/LM2904BIDR?qs=9r4v7xj2LnnFewvbXZMeJA%3D%3D): 595-LM2904BIDR | OBSERVED; 1/1 | 0.206 / 0.142 / 0.142 | 0.21 / 0.14 / 0.14 |
