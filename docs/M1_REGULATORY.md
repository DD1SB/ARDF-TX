# M1 competition rules and legal operation

Date: 2026-10-13. **Country/operator licence OPEN.** Germany is a provisional example because of workspace context; it is not an inferred user authorization. Primary sources and access limitations are in [source log](research-register.md). Technical rules were checked directly against the specified **2025 Part B** even where more recent band-planning material exists.

## Competition envelope

The [requirements trace](M1_REQUIREMENTS_TRACE.md) is the authoritative matrix for RF/frequency/antenna/timing constraints. IARU T2.1 explicitly places national electric-parameter, identification and authorized-operator compliance with the organiser. T2.4 silence, T2.2 uniform installations, T2.5 horizontal omnidirectionality and T4.1 ancillary-radio immunity apply in addition to mode-specific tables. National unwanted-emission requirements are not replaced by a single IARU dBc number.

Conducted output is measured at a defined 50 Ω post-filter reference for reproducibility. ERP references a half-wave dipole and includes installed antenna gain/feed loss. PEP is the highest RF-cycle average at the envelope peak; it is not mean AM power. Field audibility is a receiver/site condition. None of these four can stand in for another. T2.8 does not resolve carrier/mean ERP terminology; referee agreement and reporting all quantities are required before contest calibration. Foxoring rules do not define 50 Ω/tolerance either.

## Germany: primary-document obligations to resolve

| Topic | Verified primary provision / engineering consequence |
| --- | --- |
| Frequencies/licence | [AFuV Anlage 1](https://www.gesetze-im-internet.de/afuv_2005/anlage_1.html), rows 6/17: 3.5–3.8 MHz and 144–146 MHz, with class-dependent privileges. Class A/E list 80 m 750/100 W PEP; Class N has no 80 m entry. 2 m A/E 750/75 W PEP; N 6.1 W ERP. These national ceilings differ from competition levels. Verify actual licence and conditions; do not assume Class N can use 80 m. |
| Bandwidth/interference | Anlage 1 notes 3/6: 80 m occupied bandwidth ≤2.7 kHz; 2 m ≤40 kHz. [AFuV §16](https://www.gesetze-im-internet.de/afuv_2005/__16.html): accepted technical practice, minimize unwanted emissions, further technical provisions may apply. The project spectrum targets are not a verified legal mask. Obtain applicable authority/standard/test conditions before release. |
| Identification | [AFuV §11](https://www.gesetze-im-internet.de/afuv_2005/__11.html): ordinary identification rules plus §11(2) conditional exception for low-power direction-finding transmitters using prescribed identifiers. “Low-power” applicability is not established here. §11(6) simultaneous use of one callsign at different sites needs prior authority consent unless applicable exception permits. Resolve fleet identities rather than auto-inserting one callsign everywhere. |
| Automatic/unattended operation | [AFuV §13](https://www.gesetze-im-internet.de/afuv_2005/__13.html): separate callsign/location conditions for remote/automatic stations. A guarded temporary ARDF fox, autonomous unattended field unit and permanent beacon may be classified differently. Ask organiser/authority to establish applicable treatment; LoRa absence does not settle legal status. |
| Exposure/site | [BEMFV §9](https://www.gesetze-im-internet.de/bemfv/__9.html): fixed amateur installations at ≥10 W EIRP need notification/exposure documentation. Applicability depends on installation, gain and combined emissions, not just 5 W connector power. Access, forest/land permission and antenna safety also need organiser review. |
| Band planning | [IARU VHF bandplanning](https://www.iaru-r1.org/about-us/committees-and-working-groups/vhf-uhf-shf-committee-c5/vhf-up-bandplanning/) and national practice: full allocation is not an instruction to use every frequency/emission freely. Avoid beacon/repeater/satellite and other incompatible segments. Country profile and championship profile remain independent. |

The technical mask for German unwanted emissions is **not fully closed** by the inspected AFuV text alone. Record current applicable BNetzA provisions and, where relevant, ETSI EN 301 783 edition/test mask before declaring legal compliance. Do not invent an AFuV annex or treat a proposed −60 dBc target as sufficient law. Other countries require their own allocation/operator/ID/automatic-station/exposure review.

## Optional LoRa is a separate authorization path

[BNetzA Vfg.91/2025](https://www.bundesnetzagentur.de/DE/Fachthemen/Telekommunikation/Frequenzen/Allgemeinzuteilungen/_DL/vfg91_2025.pdf), SRD rows 48/50/54: general-purpose 868.0–868.6 MHz uses 25 mW ERP with specified access/mitigation or alternative ≤1% duty; 868.7–869.2 MHz uses 25 mW ERP with specified access or alternative ≤0.1%; 869.4–869.65 MHz has 500 mW ERP with corresponding conditions or alternative ≤10%. Reserved alarm bands are not generic LoRa channels. Read full footnotes/category/bandwidth conditions for chosen mode; no automatic LoRaWAN-default approval.

Semtech's +22 dBm capability is not permission to radiate that level. Module antenna gain, bandwidth and actual airtime (preamble/retries/ACKs) must fit the selected national SRD profile. Receiving continuously does not consume legal TX airtime but consumes battery power. Exact Silicontra RF-switch/TCXO/antenna/certification/configuration remains OPEN. LoRa must also satisfy IARU T4.1 receiver-interference requirements; competitor communications restrictions (24.4) require organiser operational policy distinct from transmitter-control capability.

## Construction/licensing and user actions

The [EU RED](https://eur-lex.europa.eu/eli/dir/2014/53/oj/eng), Annex I(1), distinguishes amateur construction/modification/kit cases from equipment made available on the market. Only the primary indexed Annex I excerpt was accessible; direct full/consolidated text hit robot checks. **Do not assume a club fleet, sale or complete ready-made product automatically gets an exemption.** Market placement, EMC/electrical/battery obligations and national implementation require review if product is supplied beyond own amateur experimental use. A component's certification does not certify the whole transmitter.

Before on-air prototype tests: establish countries/operator privileges, event/channel coordination, identification/automatic-station treatment and any allocation; set legal power/bandwidth/antenna limits, document site/exposure permission and applicable spectrum mask; complete conducted qualification; configure LoRa independently or leave it absent. These are actual unresolved operating inputs, not extra purchase/PCB approvals. No on-air operation, purchase or publication is authorized by this M1 document.
