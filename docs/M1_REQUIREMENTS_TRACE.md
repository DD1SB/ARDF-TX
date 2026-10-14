# M1 requirements-to-source matrix

Date: 2026-10-13. Status: complete M1 research matrix for review; measured compliance and open decisions remain pending. No hardware has been validated.

Evidence classes: **RULE** (primary competition text), **DATASHEET** (manufacturer conditions), **AUTHOR** (publisher reports), **MEASURED-PUBLISHED** (original reported measurements), **MODEL** (our calculation), **ASSUMPTION** (unverified design input), **OPEN** (missing evidence/decision). Published measurements do not validate this project.

Primary rule source: [IARU Region 1 Part B, 2025](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf), downloaded and read directly on 2026-10-13. Page numbers below are printed PDF pages.

| Baseline IDs / subject | Primary source location | Initial verification / correction |
| --- | --- | --- |
| RF80-001, RF80-007 | Appendix 1 T2.6, p.10 | Range, A1A, watts and WPM confirmed; add stability better than 50 ppm and concurrent-channel spacing at least 20 kHz. |
| RF80-002, RF80-003 | Appendix 5 S6.1–S6.4, pp.14–15 | Concurrent groups confirmed. Separate spectator transmitter is conditional: none when spectator control and finish coincide (S3.4). Frequencies shown are examples. |
| RF80-004, RF80-005, RF80-008–011 | Appendix 6 FT2.6, FT2.9, F27.3, F28.2, p.17 | Field/finish distinction confirmed; add at least 30 kHz field-to-finish separation. Different neighbouring field frequencies are recommended, not mandatory. Compact counterpoise details are a project choice. |
| RF2-001, RF2-003, RF2-004, RF2-007 | Appendix 1 T2.8, p.10 | ERP, A2A, modulation, range and antenna confirmed; concurrent spacing is strictly greater than 200 kHz. Flexible local-band operation is a project requirement, subject to country law. |
| TEST-001, CTRL-005, RF2-006 | T2.4, p.10 | Off-slot silence applies to transmitter and antenna. A finite bench leakage threshold is an engineering test, not a rulebook exemption. |
| CTRL-003 / timing | T3.1–T3.3, p.10; S6.4, p.15 | Transmitter period deviation and overlap limits are 5 s; the 1 s requirement concerns start/finish clocks. Propose tighter Sprint timing independently. |
| Antenna installation / uniformity | T2.2, T2.5, p.10; 27.2–27.4, p.7; S6.6, p.15 | Add omnidirectional horizontal pattern and symmetric Sprint ground system. Illustrative single 6 m counterpoise cannot be presumed Sprint compliant. |
| National law / LoRa | T2.1, T4.1, p.10 | IARU assigns national compliance to organiser; it does not authorize transmissions. Country and Silicontra variant remain OPEN. |
| SYS-001–009, CTRL-001–007, PWR-001–003; training output | User kickoff; accepted ADR-0001/0002 | Product requirements, not attributed to IARU. Component/current/cost verification and tests pending. |

## Requirement-by-requirement trace

`USER` means kickoff/product requirement, not IARU. `A1`–`A9` refer to the assumption table below. Test IDs resolve to [validation plan](M1_VALIDATION_PLAN.md); decisions to [decision](M1_DECISION.md) and proposed ADRs. A research conclusion is not a hardware pass.

| ID | Source / state | M1 response and acceptance test | Open input |
| --- | --- | --- | --- |
| SYS-001 | USER / LOCKED; ADR-0001 | Three independent boards; VCTRL, V80P, V2AM | Board electrical design later |
| SYS-002 | USER / LOCKED | None/one/both module presence, one configuration scheme and direct source control; VCTRL | Actual electrical pin/peripheral fit |
| SYS-003 | USER / LOCKED; SX-DS | Optional functional detection, bounded command/BUSY/DIO handling; VLORA | A3 |
| SYS-004 | USER / LOCKED | Same protected 2S domain, 1P–4P current/energy tables; VPWR | A2 |
| SYS-005 | USER / LOCKED | 4P maximum, reduced-population 1P compact Foxoring candidate; V80F/VPWR | A1/A2 |
| SYS-006 | USER / LOCKED | Valid schedule survives missing network; authenticated remote/time messages; VCTRL/VLORA | A3 |
| SYS-007 | USER / LOCKED | Role/identity/timing/frequency/power capability contract; VCTRL | Country and reference convention |
| SYS-008 | USER / TARGET | Explicit 24 h model; beacons separate, simultaneous dual-band shortfall; VPWR | A2/A4/A7 |
| SYS-009 | USER / LOCKED | Six/ten/twenty itemized baskets, minimal circuits and revised handheld comparator; VFLEET | A5, actual quotes |
| RF80-001 | RULE T2.6 p.10 | 3.510–3.600 MHz, A1A, 1–5 W, 8–15 WPM; V80P/VSPEC | Measured limits/uncertainty |
| RF80-002 | RULE S6.1–S6.4 pp.14–15 | 0.3–1 W; two simultaneous groups/different speed, 12 s slots; VCTRL/V80P | Valid event frequencies |
| RF80-003 | RULE S3.4/S6.2–S6.3 p.14 | Continuous finish and conditional separate spectator, distinct frequencies; VCTRL/VPWR | Spectator role and required duration |
| RF80-004 | RULE FT2.6/F28.2 p.17 | 10 mW short field antenna vs 1–5 W vertical finish; V80F/VFIELD/V80A | A1/A8 |
| RF80-005 | RULE F27.3 p.17 | Map point+30 m audible, 250 m inaudible; finish audible at start; VFIELD | A1/A8, referee receiver protocol |
| RF80-006 | USER / TARGET | Separate low branch, bounded PA ranges, physical off; V80P/VSAFE | Calibration circuit |
| RF80-007 | USER + T2.6 / TARGET | Local programmable source; silent retune/acquisition; VSAFE/VSPEC | All-channel spectrum |
| RF80-008 | USER + T2.6/FT2.6 / LOCKED | Distinct long and compact systems; symmetric Sprint grounding; V80A/V80F | A1, exact lengths not rules |
| RF80-009 | USER / TARGET | Costed match/coupling alternatives, separate-path proposal ADR-0004; V80A/V80F | A1 |
| RF80-010 | USER + FT2.6/F27.3 / TARGET | Defined 50 Ω conducted plane and independent reach; V80F/VFIELD | A8 |
| RF80-011 | USER / TARGET | No watt RF route to Fox cartridge, mechanical ID/hardware interlock; VSAFE/V80F | Full-fault coupling evidence |
| RF2-001 | RULE T2.8 p.10 | 144.500–144.900 MHz, 0.25–1 W ERP, A2A, 70–80%, 8–15 WPM, horizontal at 2–3 m; V2AM | A6/A8 |
| RF2-002 | USER / LOCKED | Physically separate bounded 1 µW–1 mW provisional range; V2TRAIN | Training field acceptance |
| RF2-003 | USER + T2.8 / LOCKED | Sinusoidal amplitude envelope, not FM sidetone; V2AM | A6 |
| RF2-004 | USER + T2.8 / TARGET | Carrier/feed/gain to PEP model and ≥1 dB margin; V2AM/VTHERM | A6/A8 |
| RF2-005 | USER / TARGET | Pre-PA training branch/independent PA-disable; V2TRAIN/VSAFE | Coupling and single-fault tests |
| RF2-006 | USER + T2.4 / TARGET | Hardware source and supply mute, persistent fault latch; VSAFE | Component/timing tolerances |
| RF2-007 | USER + T2.8 / LOCKED | Local-band capability and independent competition restriction; VCTRL/V2AM | A9 |
| CTRL-001 | USER / LOCKED | ESP32 S3-class pin budget, local timers/optional SPI; VCTRL | Actual application current |
| CTRL-002 | USER / TARGET | Revised nine-signal contract: source bus, ARM, MOD, LEVEL, mode, lease, fault, analog ID/monitor; VCTRL/V2AM | GPIO/pull/protection and PWM filtering |
| CTRL-003 | USER + T3.1–T3.3 / TARGET | RTC/monotonic capture, drift/sync/error budget; VCTRL | A4, aging/initial sync |
| CTRL-004 | USER + SX-DS / TARGET | No invented identity register; bounded non-TX functional detection; VLORA | A3 |
| CTRL-005 | USER + T2.4 / TARGET | External lease watchdog, POR/latch, source+supply gates; VSAFE | Latch circuitry/stock |
| CTRL-006 | USER / TARGET | CRC/version/capabilities, durable stop/reset/update policy; VCTRL | Later implementation |
| CTRL-007 | USER / TARGET | Passive limited-current type ID, manual hardware calibration/printed serial; EEPROM automation optional; VCTRL/VSAFE | ID thresholds and calibration-record binding |
| PWR-001 | USER / TARGET | Provisional loaded 6.0–8.4 V, transient/reverse/boost gating; VPWR/VSAFE | A2 |
| PWR-002 | USER / TARGET | External matched protected/balanced pack and proper 2S charger; VPWR | A2, supplier/temperature data |
| PWR-003 | USER / TARGET | Peak currents, η/standby/LoRa duty sensitivity and thermal loss; VPWR/VTHERM | A2/A3/A4/A6 |
| TEST-001 | RULE T2.4/T2.1 p.10 | Off-slot/source/antenna leakage search, legal profile; VSAFE/VSPEC | A9, finite detection floor |
| TEST-002 | USER / TARGET | Separate 50 Ω planes, envelope/coupler/sense points and serial records; all tests | Instruments and measured data |
| RULE-001 (added) | RULE T2.6/FT2.6/T2.8 pp.10,17 | Frequency stability **better than 50 ppm**; V80P/V2AM | Reference drift |
| RULE-002 (added) | RULE T2.6/T2.8/FT2.6 | Concurrent HF ≥20 kHz, VHF **>200 kHz**, Fox finish-to-field ≥30 kHz; VCTRL/VSPEC | Event frequency plan |
| RULE-003 (added) | RULE T2.2/T2.5/27.2/S6.6 | Uniform applicable installations, horizontal omnidirectionality, no in-event change, symmetric Sprint ground; V80A/V2AM | A1/A6 |
| RULE-004 (added) | RULE T3.1–T3.3 p.10 | Separate transmitter ≤5 s and start/finish clocks ≤1 s; tighter project Sprint target; VCTRL | Initial clock sync |
| RULE-005 (added) | RULE 27.3–27.6/T4.1 | Start audibility/monitor recording/end operation/authorized ID windows, ancillary RF immunity; VFIELD/VLORA | Organiser operations |
| RULE-006 (added) | RULE FT2.9 p.17 | Different neighbouring Foxoring channels **recommended**; VCTRL | Site plan; no invented mandatory field-field spacing |
| COST-001 | USER cost rework / TARGET | Revised targets vs nominal/estimate sensitivity/tax/scope in cost analysis and workbook | All four ceilings not jointly proved |
| COST-002 | USER cost rework / LOCKED | Reproducible 6/10/20 identical-MPN baskets in m1_costs.py; customer MOQ and stock conflicts | Live baskets/spares/packing |
| COST-003 | USER cost rework / LOCKED | ON7YD measured HF; DL3BBX six-unit AM build; G3ZOI/Si5351 evidence matrix and dated supplement | CQ-DL original and adapted RF tests |
| COST-004 | USER cost rework / LOCKED | Cost-driver table, alternatives and optional/reduced populations; itemized off-board antennas/ports | Supporting quotes and calibration labor |
| COST-005 | USER cost rework / LOCKED | Three-PCB/LoRa/RF/timing/antenna/safety retained; revised energy model and original tests | Actual hardware performance/endurance |
| COST-006 | USER cost rework / TARGET | Counts CSV, part/source catalog, itemized Markdown and machine-readable baskets | OPEN supplier codes/stock/RF values are not an ordering list |
| COST-007 | USER cost rework / LOCKED | ADR-0007 proposed, explicit M2 hold in architecture/decision | User architecture review before later authorization |

## Role and frequency validation examples

These are example plans, not locked frequencies or permission. Every carrier remains programmable within profile/country constraints. RF80 normal allows 3.510–3.600 MHz; VHF capability proposed 144–146 MHz where lawful, championship carrier restriction enforced separately. The carrier range alone does not excuse out-of-band sidebands.

| Role plan | Example assignment | Validation |
| --- | --- | --- |
| Classic 80 m | Field 3.530 MHz; finish 3.600 MHz | Two concurrent carriers separated 70 kHz; field one minute per five, finish continuous. |
| Classic 2 m | Field 144.500; finish 144.900 MHz | 400 kHz >200 kHz. Pair 144.500/144.700 **fails** strict separation. |
| Sprint | Slow group 3.530, spectator 3.550, fast group 3.570, finish 3.600 MHz | IARU example; minimum pair difference ≥20 kHz, concurrent groups and continuous B/S. Colocated B/S omits S transmitter. |
| Foxoring | Field channels 3.510/3.550/3.570; finish 3.600 MHz | Closest field-to-finish 30 kHz; different neighbours recommended. Field 3.580 with 3.600 finish **fails**. FT2.6 gives finish-to-field spacing, not an invented 30 kHz between every field transmitter. |

## Unverified assumption register

| ID | Prominent unresolved input | Closure evidence / impact |
| --- | --- | --- |
| A1 | Compact counterpoise geometry, loading Q/coupling/loss and environment recipe | V80F/VFIELD across wet/dry sites; no accepted 30/250 m reach yet. |
| A2 | Cell/pack supplier/lot/capacity, cutoff, ESR/BMS/current/temperature/charger | VPWR; budget based on 3.4 Ah and 64.8% usable energy only. |
| A3 | Exact Silicontra MPN/pinout/TCXO/switch/current/prices/legal channel | User/vendor evidence plus VLORA; no invented module details. |
| A4 | Actual ESP32/local safety/standby/synth/driver/regulator currents and efficiency | VPWR/VCTRL; cost rework increases active-driver allowances, no measured current savings. |
| A5 | Supporting MPN/value/quote closure, PA/driver suitability and lifetime stock, shields/thermal/connector/winding costs | PD55008 active/priced but AM unverified; driver variants separated; live baskets and no released BOM. |
| A6 | Modern VHF AM PA/modulator clean PEP/headroom/thermal behavior and installed antenna gain | V2AM/VTHERM; historical AM concept supports R&D, not validation. |
| A7 | Need for simultaneous full-power dual-band 24 h or continuous full-power beacons | User scope decision; model fails within ≤4P for those cases. |
| A8 | ERP carrier/mean convention, Foxoring reference-plane/tolerance, audible receiver criteria | Organiser/referee agreement plus measured reports. |
| A9 | Countries/licence/identification/automatic-station treatment, current legal spectrum mask and market status | Country-specific primary legal review; [regulatory](M1_REGULATORY.md). |

## Corrections to the initial baseline

Added stability, strict/role-specific channel separations, uniformity/omnidirectionality and timing distinctions. Qualified RF80-003 to conditional separate spectator. Sprint counterpoise must be symmetrical; illustrative 8 m+6 m lengths are not a mandatory rule or proof of compliance. Preserved separate Foxoring field/finish, ERP/conducted distinction and optional LoRa. All unaccepted implementation choices are ADR proposals, not silently accepted decisions.
