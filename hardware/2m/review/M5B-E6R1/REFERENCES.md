# Primary references and evidence boundaries

Accessed/reviewed 21 October 2026. Manufacturer/rule documents are technical references, not project-licensed source files. Full third-party PDFs remain outside this repository. Downloaded-document hashes are in `reference-downloads.json`; supplier web observations are not binding quotes.

| Reference | Use / limitation |
| --- | --- |
| [IARU Region 1 Part B 2025](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf) | Appendix 1 p10 T2.2–T2.8, section 27/28, Appendix 5 S6. Exact source-backed requirements distinguished in regulatory note |
| [ST PD54008L-E](https://www.st.com/resource/en/datasheet/pd54008l-e.pdf) | PowerFLAT 5×5 source path and RθJC 3 K/W. Historical E5/E6 manufacturer audit retained; no new 144 MHz efficiency or transient-Zth guarantee |
| [ST D45H11](https://www.st.com/resource/en/datasheet/d45h11.pdf) | TO-220 tab/pin and RθJC basis; hot SOA still requires actual operating-point qualification |
| [ST BD139](https://www.st.com/resource/en/datasheet/bd139.pdf) | SOT-32/TO-126 pin/tab and RθJC basis; existing package audit unchanged |
| [TI TLV9004](https://www.ti.com/lit/ds/symlink/tlv9004.pdf) | Actual amplifier family; 1 MHz typical GBW. Whole pass/helper feedback poles, saturation and loading are separate assumptions |
| [TI TPS22810](https://www.ti.com/lit/ds/symlink/tps22810.pdf) | Driver switch CT/start/discharge behavior; 2 ms is an unqualified system budget, not a datasheet-guaranteed MMIC settling time |
| [TI TLV703x/TLV704x family](https://www.ti.com/lit/ds/symlink/tlv7031.pdf) | Final selected **TLV7034PWR push-pull**, TSSOP14. Pin 4 supply, 11 ground, outputs 1/7/8/14. ±8 mV offset and quad 3/10/25 mV hysteresis figures; no guaranteed installed thermal delay |
| [TI SN74LVC2G00](https://www.ti.com/lit/ds/symlink/sn74lvc2g00.pdf) | DCUR VSSOP8: 1A1,1B2,1Y7,2A5,2B6,2Y3,GND4,VCC8 |
| [TI SN74LVC2G32](https://www.ti.com/lit/ds/symlink/sn74lvc2g32.pdf) | DCUR VSSOP8 has same dual-gate pin arrangement; OR function differs from NAND |
| [TI SN74LVC1G04](https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf) | DBVR SOT23-5: NC1,A2,GND3,Y4,VCC5 |
| [Murata NCP15 series](https://www.murata.com/-/media/webrenewal/products/thermistor/ntc/ncp/ncp15.ashx?la=en) | NCP15XH103F03RC row: 10 kΩ1%, B25/50 3380 K1%, B25/85 3434 K typical. 1.0/2.5 figures are dissipation constants in mW/K, not seconds |
| [SK81 100 supplier index](https://www.reichelt.com/de/en/shop/product/heat_sink_100_mm_aluminium_2_2_k_w-227984) | €7.30 gross observed/indexed, 214 g, 100×100×15 mm; preserve title/property thermal discrepancy and use 2.2 K/W comparator |
| [SK81 75 supplier index](https://www.reichelt.com/de/en/shop/product/heat_sink_75_mm_aluminum_2_5_k_w_-227987) | €5.55 gross indexed, 75 mm length, 2.5 K/W; 160.5 g is estimated from length, not weighed |
| [Dold EN AW6060 100×4 stock](https://www.dold-mechatronik.de/Flachstange-100x4mm-Aluminium-EN-AW-6060-T66-AlMgSi05-1112kg-m-Zuschnitt-20-6000mm) | 1.112 kg/m indexed and configurable cuts; minimum displayed price does not quote the selected 100 mm cut |

Existing authoritative project references were read before selecting a keying proposal: `docs/M2_POWER_MODE_COMPARISON.md`, `docs/M2_ENDURANCE_REWORK.md`, E5 thermal/mechanical and E4 correction notes; E5 `thermal-model.json`, `pass-spacer-thermal.json`, `common-mechanical-platform.json`; actual RF2M electrical JSON, native netlist, PCB and control contract; complete E6 review decision/transient note/README/common-cooler PDF and numerical sources. They remain frozen under `preserved-start.json`.

No manufacturer datasheet establishes all new system-level corners. Missing data are explicit: PA efficiency at actual AM operation, reflected-power/current trajectory, source-joint thermal transient, installed sensor coupling/lag, converter light-load transients, loaded/unloaded nonlinear modulator behavior, driver feedthrough, actual spectrum and enclosure convection. Model scenarios bound known uncertainties for decision-making; they do not turn assumptions into measured facts.
