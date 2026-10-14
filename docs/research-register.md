# Research and evidence register

## M2 power reassessment — 2026-10-14

The [dated power-source register](M2_POWER_ARCHITECTURE_SOURCES.md) supplements all previous observations. It rechecks IARU 2025 limits and examines cell capacity/energy/temperature, 2S/4S converter/device ratings, protection/balancing and charger sourcing. The [review decision](M2_POWER_ARCHITECTURE_DECISION.md) and [trace supplement](M2_POWER_REQUIREMENTS_TRACE.md) record the user's new 12 h full / 24 h reduced objective explicitly; prior accepted architecture and historical calculations remain preserved. New 4S implementation is proposed, not accepted or measured.

## M2 proven 80 m comparison — 2026-10-13

The [dated source/requirement matrix](M2_80M_REFERENCE_COMPARISON.md) adds actual DF1FO Midi/Sprint/Fixle drawings and legacy Eagle downloads, ON7YD ATX80B revision1.4, TinyFox hardware2.0, FlexFox80 commit `a4969f60f30ed87df2e0e8c1e6cdbc852b6f40bb` and SignalSlinger commit `4d6d66fb83b76b17be3886c718f90a273225c2e5` / hardware3.5. Original schematics, BOM variants and PCB layouts were inspected read-only. Google BOM and current KiCad discrepancies are recorded rather than merged silently. QCX contributes a measured shaping reference.

LM5134's primary datasheet confirms that **B is TTL-input and A is supply-relative CMOS-input**; A is rejected for direct 3.3 V drive at the proposed rails. Component observations, unquoted positions, hashes, license notices and quantity arithmetic accompany the six M2 documents. Adapted hardware and H0–H9 remain NOT RUN. Accepted ADRs and the completed Foxoring accounting baseline are preserved.

**M1 inspection date: 2026-10-13.** The initial seed below is retained as provenance. The inspected-source log following it supersedes its tentative statements. No ARDF-TX hardware measurements exist.

Sources below are candidates; M1 must inspect the primary content and give section/page references for every quantitative claim. Do not treat an original author's claim as a laboratory verification of a derivative design.

| Ref | Primary source | Why it matters | Confidence/limitation |
| --- | --- | --- | --- |
| IARU-B-2025 | https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf | Rules: Appendix 1 §§T2.4/T2.6/T2.8, Sprint Appendix 5 §§S6.1–S6.4, Foxoring Appendix 6 §§F27.3/FT2.6. | Authoritative for 2025 IARU Region 1 competitions, **not** local legal compliance. |
| NL-HISTORY | https://fox.ardf.veron.nl/Documenten/Hall_of_Fame/ARDF_ontwikkeling_in_Nederland.pdf | G3ZOI diagram Fig. 33 on printed p. 12; 70 cm BF-888S example on p. 18; UV-3R 2 m/70 cm supply-modulated AM approach Fig. 60–62 on p. 19. | Real examples but no verified UV-K5/UV-5R or component-identical implementation. |
| SMARTFOX | https://github.com/Guru-RF/SmartFOX | MIT firmware: Si5351 control, Morse, schedule, USB config; RP2040 dual hardware detection; 2 m **FM**, 80 m direct Si5351 CW. | Software reference, not a complete open, reproducible RF hardware design (no KiCad/Gerbers in examined root tree). |
| HG0HK-80M | https://ardf.hu/content/technika/UTX80m/andras_paal.html | Published 80 m Classic/Sprint/Foxoring transmitter (1.7 W / 0.5 W, 1S cell, modes and timings). | Useful hardware reference; confirm circuit availability, rules conformity for 10 mW Foxoring and actual measurement evidence separately. |
| G3ZOI | https://www.qsl.net/g3zoi/ | Compact 2 m AM transmitter background and newer RF projects. | Need the original schematics and test evidence per project version. |
| SX1262 | Silicontra SX1262 module, exact MPN/footprint from the existing station design | Optional LoRa 868 MHz, connector and software driver reuse. | Exact variant, BOM, legal radio settings and busy/IRQ pinout need verification. |

## Evidence policy

For each RF topology candidate, record: (a) original drawing/version, (b) measured power and spectrum (if published), (c) known AM linearity or CW shaping evidence, (d) parts sourcing/price/MOQ, (e) expected 2S operating voltage, (f) PCB/layout accessibility, (g) testability, (h) license rights, (i) derivative changes needed, (j) unknowns and bench tests.

## Dated primary-source log

Evidence classes: **RULE**, **DATASHEET**, **AUTHOR** (publisher assertion), **MEASURED-PUBLISHED** (original reported measurement, conditions limited), **MODEL**, **ASSUMPTION**, **OPEN**. Published measurements do not validate a derivative. Distributor observations retrieved on this date can be cached; they are not binding quotes or reserved inventory.

| Ref | Attributed primary source | Inspected location / evidence | Access / limitation on 2026-10-13 |
| --- | --- | --- | --- |
| IARU-B-2025 | [IARU Part B 2025](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf) | Printed pp.7,10,14–15,16–17; §§27,28,T2,T3,T4,S3.4,S6,F27.3,F28.2,FT2.6,FT2.9. | Downloaded and read directly; digest in [checks](M1_CHECKS.md). Competition authority, not permission to radiate. |
| DE-AFUV | [German AFuV consolidated text](https://www.gesetze-im-internet.de/afuv_2005/BJNR024200005.html) | §§2,10,11,13,16; Anlage 1 rows 6/17 and notes 3/6. | Read. Germany is provisional; country/operator OPEN. |
| DE-ID | [AFuV §11](https://www.gesetze-im-internet.de/afuv_2005/__11.html) and [§10](https://www.gesetze-im-internet.de/afuv_2005/__10.html) | Conditional low-power direction-finding identification exception; simultaneous callsign use. | Read; no blanket exception claimed. |
| DE-AUTO | [AFuV §13](https://www.gesetze-im-internet.de/afuv_2005/__13.html) | Automatic/remote station allocation and location conditions. | Read; guarded temporary ARDF versus unattended beacon classification OPEN. |
| DE-EMF | [BEMFV §9](https://www.gesetze-im-internet.de/bemfv/__9.html) | Fixed amateur installations at ≥10 W EIRP: notification/exposure documentation. | Read; conditional applicability. |
| DE-SRD | [BNetzA Vfg.91/2025](https://www.bundesnetzagentur.de/DE/Fachthemen/Telekommunikation/Frequenzen/Allgemeinzuteilungen/_DL/vfg91_2025.pdf) | SRD rows 48/50/54; ERP, access and duty conditions. | Primary PDF text read via browser. |
| R1-BANDPLAN | [IARU VHF bandplanning](https://www.iaru-r1.org/about-us/committees-and-working-groups/vhf-uhf-shf-committee-c5/vhf-up-bandplanning/) and [Handbook 10.02](https://www.iaru-r1.org/wp-content/uploads/2024/11/VHF_Handbook_V10_02.pdf) | Current page updated 2026-09-19; 144 MHz table/notes. | Page and indexed handbook table inspected. Recheck latest version before operating. |
| EU-RED | [Directive 2014/53/EU](https://eur-lex.europa.eu/eli/dir/2014/53/oj/eng) | Annex I(1), amateur kits/modifications/individual experiments and market availability. | Direct opens hit robot checks. Primary indexed Annex I excerpt available; full current consolidated text **not verified**. |
| NL-HISTORY | [VERON Netherlands history PDF](https://fox.ardf.veron.nl/Documenten/Hall_of_Fame/ARDF_ontwikkeling_in_Nederland.pdf) | p.12 Fig.33 G3ZOI ICS525/PIC series modulation; pp.15–16 Figs.43–48 built sets; p.18 BF-888S 70 cm; p.19 Figs.60–62 PA0JBG/PA0DFN UV-3R AM and 2025 controller update. | Browser error recovered by download. Built-use evidence; no calibrated AM/spectrum report; not UV-5R. Licence OPEN. |
| G3ZOI-80 | [G3ZOI ATX80](https://www.qsl.net/g3zoi/docs/80m-atx/) | Combined ON7YD transmitter/timer; unsafe manual keying order noted; download link exists. | Direct download read; browser failed. Exact version/licence required before copying. |
| G3ZOI-ANT | [G3ZOI short-wire antenna](https://www.qsl.net/g3zoi/docs/80m-ant/) | Longer-wire L match, reported 150–180 mA using MFJ-853; capacitor arcing warning. | Direct download read. Not a qualified 30 cm match. |
| G3ZOI-MICRO | [G3ZOI getting started](https://www.qsl.net/g3zoi/docs/getting-started/) | ON7YD microtransmitters, pseudo AM/FM VHF oscillator. | Read; no 70–80% AM certification. |
| SMARTFOX | [Guru-RF / ON6URE repository](https://github.com/Guru-RF/SmartFOX) | README, root listing, detection, HF Si5351 keying, VHF VCXO FM sidetone, MIT notice. | Software reference. README also asserts MIT for schematics/documentation, but complete RF CAD package not established in inspected tree. Audit files/dependencies separately. |
| HG0HK-80M | [Andras Paal HG0HK UTX80m](https://ardf.hu/content/technika/UTX80m/andras_paal.html) | Specifications: 1S, 1.7/0.5 W, maximum 0.8 A at 4 V; separate long/0.3 m antennas. | AUTHOR specifications; no calibrated 10 mW or spectrum report. Additional files identified by [technical index](https://www.ardf.hu/index.php/letoltesek/technika), circuit/licence not established. |
| DF1FO-VHF | [Nick Roethe DF1FO 2 m TX](https://df1fo.darc.de/DOC/2mTX.doc) | Midi/maxi chapters; four-prototype voltage/power/current table; square collector modulation and ICS525 noise. | Downloaded/read with antiword. Embedded diagrams not adopted as released circuit. Eagle links on [index](https://df1fo.darc.de/); licence OPEN. |
| DF1FO-FOX | [DF1FO Foxoring designs](https://df1fo.darc.de/DOC/80mMiniTX.doc) | “Reichweiten” wet-woodland table, loading/counterpoise and reach. | Original field comparison with limited receiver/calibration detail; some configurations exceed 250 m. |
| DF1FO-FIXLE | [Fixle, September 2026](https://df1fo.darc.de/DOC/Fixle.doc) | Claimed compact size, 1.5–3 mA mean, 80–150 h, 6 EUR materials, ~300 m with Spätzle receiver. | AUTHOR figures, not current quotation; wire installation is longer than 30 cm. |
| QCX-PA | [QRP Labs QCX Rev.1.22](https://www.qrp-labs.com/images/qcx/assembly_A4-Rev-5e.pdf), [QCX+ Rev.1.03](https://www.qrp-labs.com/images/qcxp/manual1.03.pdf) | QCX §7.3 power-versus-supply measurements; QCX+ class-E waveform/explanation, three BS170s and shaping. | Measured reference; five watts often requires 15–16 V. Thermal/mismatch changes need testing and licence review. |
| QRP-SYNTH | [QRP Labs synthesizer](https://www.qrp-labs.com/synth.html) | Tested implementations, kit/manual/reference options, public 7.75 USD kit price. | Not spectral-compliance proof; kit cost ≠ bare IC cost. |
| RA3APW-SPECTRUM | [Karen RA3APW spectra](http://www.ra3apw.ru/proekty/si5351-spectrum/) and [author follow-up](https://groups.google.com/g/2-meter-wspr/c/TK0KupEoucw/m/64DpDbLT8fsJ) | 2015 §§2–4/Figs.8–21 at 144.490 MHz with attenuators and Anritsu reference; −110 dBc/Hz at 10 kHz; follow-up reports −41 dBc spur at 997 kHz. | HTTPS certificate mismatch; HTTP download succeeded. Measurements specific to configuration, not every Si5351. |
| SI5351-DS | [Skyworks Rev.1.3](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/data-sheets/Si5351-B.pdf), [AN619 Rev.0.8](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/application-notes/AN619.pdf) | Frequency/package/electrical/pin conditions and divider programming. | Read; 10-MSOP variant lacks dedicated external OEB pin. Clock specs do not certify an RF transmitter. |
| TI-PLL | [TIDA-00886](https://www.ti.com/tool/TIDA-00886), [TIDUC19A](https://www.ti.com/lit/pdf/TIDUC19), [LMX2571 datasheet](https://www.ti.com/lit/ds/symlink/lmx2571.pdf) | Guide §§4.1–4.2 pp.8–10: measured **480 MHz** noise, regulator/PFM effects and bead mitigation; datasheet §6.5 currents. | Measured PLL reference, not 144 MHz AM. 39 mA is conditional typical current. TI reference-design terms apply. |
| ADI-PLL | [ADF4351 Rev.A](https://www.analog.com/media/en/technical-documentation/data-sheets/adf4351.pdf) | Range, divider/output, lock detect and supply conditions. | Datasheet read; generic modules' provenance/performance unverified. |
| PA-RD06 | [Mitsubishi datasheet at RF Parts](https://www.rfparts.com/fileuploader/download/download/?d=0&file=custom%2Fupload%2FFile-1374623485.pdf), [seller](https://www.rfparts.com/rftransistors/transistor-rd/rd06hvf1.html) | 6 W at 175 MHz/12.5 V; package/pins; seller **NOS**, 9.91 USD, in stock. | Bench-reference candidate; active production and 144 MHz AM transfer unknown. |
| PA-AFT | [NXP AFT05MS006N status](https://www.nxp.com/products/radio-frequency-rf/legacy-rf/legacy-rf-power/136-941-mhz-6-0-w-7-5-v-wideband-rf-power-ldmos-transistor%3AAFT05MS006N?tab=Package_Quality_Tab), [datasheet](https://www.nxp.com/docs/en/data-sheet/AFT05MS006N.pdf) | 6 W/7.5 V VHF reference; manufacturer **End of Life**. | Excluded from repeatable fleet baseline; aggregator stock is insufficient. |
| PA-CURRENT | [Ampleon BLP5LA55S](https://www.ampleon.com/products/general-purpose-wideband/12.5-14-v/BLP5LA55S.html), [Rev.4 datasheet](https://www.ampleon.com/documents/data-sheet/BLP5LA55S.pdf); [BLP9LA25S](https://www.ampleon.com/products/general-purpose-wideband/12.5-14-v/BLP9LA25S.html) | Active current devices. BLP5 data pp.1,8–11: VHF CW/two-tone measurements at 15 V, 893 mA quiescent; BLP9 is active 25 W family. | Good availability/performance comparators, oversized for cost/idle target. BLP5 small quantity observed; BLP9 Mouser reel-only and DK detailed page inaccessible. Neither efficiency extrapolated to 1 W ERP. |
| ESP-DS | [Espressif S3-WROOM datasheet](https://www.espressif.com/sites/default/files/documentation/esp32-s3-wroom-1_wroom-1u_datasheet_en.pdf) | GPIO/peripherals, dimensions, land pattern. | Application current remains ASSUMPTION. |
| RTC-DS | [Micro Crystal RV-3032-C7](https://www.microcrystal.com/fileadmin/Media/Products/RTC/Datasheet/RV-3032-C7.pdf), [manual](https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3032-C7_App-Manual.pdf) | 160 nA typical/3 V; ±2.5 ppm −40…85°C; registers, backup and clock. | Initial sync/aging/software additional. |
| SX-DS | [Semtech SX1262](https://www.semtech.com/products/wireless-rf/lora-connect/sx1262) | Datasheet link, command/BUSY/DIO interface and RX-current headline. | Exact Silicontra board/pinout/TCXO/switch/standby/price **not provided**. Chip ≠ module. |
| BOOST-DS | [TI TPS61178 family](https://www.ti.com/lit/ds/symlink/tps61178.pdf) | Up to 20 V output; external load-disconnect FET driver; forced-PWM TPS611781 option. | External isolation FET still required; project efficiency unmeasured. |
| WDT-DS | [TI TPS3431](https://www.ti.com/lit/ds/symlink/tps3431.pdf), [EVM guide](https://www.ti.com/lit/ug/snvu614/snvu614.pdf) | Timeout, startup/reset pulse and WDO behavior. | WDO releases after pulse: separate fault latch required for persistent fail-off. |

## Cost rework evidence — 2026-10-13

The [dated cost supplement](M1_COST_SOURCES.md) adds primary ON7YD instrument measurements, DL3BBX/Hoogeveen six-unit AM experience, ST PA data, driver lifecycle evidence, cheap PLL/logic alternatives and supplier conflicts. [Itemized material](M1_COSTED_BOM.md) replaces broad cost envelopes; [ADR-0007](decisions/ADR-0007-cost-optimized-m1.md) records conditional architectural acceptance. Detailed RF circuits and complete layout/procurement remain gated by [M2 preparation](M2_PREPARATION.md). Supporting values/order codes and measured RF/antenna/energy results remain OPEN. No third-party circuit or layout is copied.

## Pricing, failures and licences

The [candidate BOM](M1_BOM_CANDIDATES.md) logs exact observed prices, quantities, packaging and primary distributor links. EUR and USD are kept separate; no exchange rate, quantity discount or module price is invented. Conflicting/cached inventory is disclosed.

Failed attempts: browser Netherlands/G3ZOI/DF1FO opens recovered with downloads; initially guessed DF1FO `2mMaxiTX.doc` returned 404, correct linked `2mTX.doc` recovered. PE5EDW's XS4ALL page redirects to a provider 404, so its indexed excerpt is not inspected primary evidence. OZ2M's indexed 2018 presentation URL returned 404; no conclusion depends on those slides. EUR-Lex full/consolidated text hit robot checks. No live checkout/reservation or quote request was performed.

The final automated link sweep encountered NXP product/datasheet HTTP 404 despite primary indexed content being available, DigiKey HTTP 403 restrictions, EUR-Lex HTTP 202 challenge, and some PDF timeouts. See [checks](M1_CHECKS.md) and its machine-readable report; direct access and indexed primary evidence are distinguished. An inaccessible old source is not silently replaced by an invented URL.

M1 commits original analysis and short attributed factual summaries, **no third-party schematics, Gerbers, footprints, source code or complete documents**. Temporary downloads are not deliverables. Before copying in M2, record exact version, copyright holder, licence/permission and dependencies. Public availability is not a reuse licence. The user was asked for country/licence, Silicontra part/pinout and battery preference; these remain OPEN without an answer.

## Conditional acceptance and preparation evidence

The user conditionally accepted M1 on 2026-10-13. [M2 sources](M2_SOURCES.md) extend this log with GVA drive/PD55008 near-band matching, modulator thermal/SOA alternatives, actual ideal-passive simulation and current-source observations. [M2 preparation](M2_PREPARATION.md) preserves architecture and excludes BFP650 selection; no project hardware measurements or full-set orders occurred.

## Foxoring cost audit — 2026-10-13

[Audit sources](FOXORING_COST_SOURCES.md) distinguish the original EUR29.06 material scope from EUR77.11's pack/case/fabrication/wiring and per-unit charging/freight/tooling allocations. New regular 25R cells and supplier tabs are priced; a stocked protection/balancing candidate retains qualification/replacement provision. The previously indexed in-stock 35E observation is superseded by its direct out-of-stock page. Cheap discontinued NKON protection is excluded. TinyFox's historical author cost/field report and DF1FO's downloaded Fixle cost/scope are assessed without copying circuits or changing the common MCU/PCB architecture. [Itemized bill](FOXORING_COST_BOM.md) remains a candidate; no purchases or hardware passes occurred.


## M3A narrow electrical review — 2026-10-14

[Source log](M3_80M_SOURCES.md), [PA selection](M3_80M_PA_SELECTION.md) and [electrical review](M3_80M_SCHEMATIC_REVIEW.md) retain actual QCX/ON7YD/OpenARDF evidence. New checked device details include STBD140 HF-shaper pinout/thermal data, TPS54302 input/EN bounds, INA180A physical pins, loaded-reference/common-mode arithmetic, power-inductor saturation margin and stronger SN74AC00DR Fox drive. These are design inputs, not measured RF results. ERC/netlist/Boolean checks and explicit unquoted positions are in [M3 checks](M3_80M_CHECKS.md); physical gates are allNOTRUN.
