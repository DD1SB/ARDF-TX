# M5B-E2 component and mechanical fit

The schematic, symbols, local footprint files, embedded footprint geometry, pad nets, placement and model transforms remain identical to E1. Fresh [pinout-audit.json](../hardware/2m/review/M5B-E2/pinout-audit.json) and [critical-package-audit.json](../hardware/2m/review/M5B-E2/critical-package-audit.json) compare actual exported nets and native pads. All **42 critical manufacturer maps and 320 schematic package/pad sets** pass. No new pinout defect was found.

Manufacturer drawing revisions remain linked in [the preserved E1 qualification](M5B_E1_COMPONENT_QUALIFICATION.md) and its source log. These findings apply only to the exact listed manufacturers and orderable packages.

| Part | Rechecked construction | Disposition |
| --- | --- | --- |
| Q501 ST PD54008L-E | ST January 2007 Rev2 top view: G left at −2.25 mm, D right at +2.25 mm, source center. G/D lands 0.5 × 5 mm, S 2.7 × 5 mm. Source is electrical RF ground. | Verified CAD; hidden-pad reflow, paste/void and thermal inspection required. |
| U501 PHA-1+ | DF782 RevG, 2017-02-08: 1 RF_IN, 2 GND lead, 3 RF_OUT/DC, 4 GND flange. Manufacturer polygon and ground landing retained. | Verified with reflow/RF-return constraint. |
| TPS611781RNWR | RNW0013A 4222804/C, Nov2019: separate center contacts 6 GND / 7 SW / 8 VOUT, each 0.35 × 3.5 mm. | Verified; never merge as a common exposed pad. |
| TPS54302DDCR / inductors | DDC6 mapping; exact Bourns SRP1265A lands and selected 10 µH/4.7 µH parts. | Verified CAD. |
| U950 TLV76701DRVR | 1 OUT, 2 FB, 3 GND, 4 EN, 5 GND, 6 IN, 7 ground EP. | Verified; sourcing and ≥1 µF effective capacitance require confirmation. |
| U303 TLV76150DCYR | 1 GND, 2 OUT/tab, 3 IN. Tab is live 5 V. | Verified with electrical clearance constraint. |
| U305 TPS22810DBVR | 1 VIN, 2 GND, 3 ON, 4 CT open, 5 QOD / 6 OUT tied. | Verified; retain the E1 replacement of TPS22919. |
| Q401 ST D45H11 | DocID4213 Rev5: 1 B, 2 C/tab = VPA, 3 E = VMOD. | Verified with insulated sink/shoulder washer. |
| Q402 ST BD139 | May2008 Rev5: 1 B, 2 C = MOD_SINK, 3 E. | Verified; exact ST device, live collector mounting. |
| Si5351/crystal, references/sensors/FETs | Same exact maps as E1. TL431DBZ: 1 K / 2 REF / 3 A. AO3401A: 1 G / 2 S / 3 D. Nexperia 2N7002: 1 G / 2 S / 3 D. | Verified net/pad maps; no unsupported manufacturer interchangeability. |
| J301 JST VH | B2P-VH(LF)(SN), 1 BAT_RAW+, 2 GND; VHR-2N/SVH mating harness. | Verified landing; incoming polarity, mating and finished-hole inspection. |
| J101 Wurth IDC | 61202021621, 20 ways, 2.54 mm pitch; 1.10 mm holes, 9.1 × 33.06 × 8.75 mm body. | Verified with notch, pin1 and cable-orientation checks. |
| J501 Amphenol 132134 | Center1 NORMAL_RF, shell2 GND; 1.50/1.70 mm finished holes. | Verified map; incoming lead/mating fit and hole tolerance. |
| J701 Wurth 66012102111404 | MMCX center1 TRAIN_RF, shell2 GND; exact SMT landing and 5 mm height. | Verified; mechanically different from normal SMA. |
| C409 and RF inductors | Exact Panasonic and Coilcraft landings/rating evidence retained. | Verified CAD; sourcing holds remain visible. |

The twelve 0.60/0.30 mm PD source vias remain GND. The bottom 14 × 12 mm contact window, x105–119/y49–61 mm, contains no foreign B.Cu. Source paste segmentation and masked via columns are unchanged. Controlled reflow is required; ordinary external visual inspection cannot establish hidden solder-void percentage.

The lower spreader proposal is **16 × 44 × 8 mm**, mounted through existing NPTH centers (112,32)/(112,68). Use a **0.15–0.25 mm electrically insulating thermal sheet**, conductivity ≥3 W/mK and dielectric rating ≥100 V, over its entire face, plus a separately verified metal-ground strap. Exact sheet, flatness and contact resistance remain assembly qualifications. Do not rely on solder mask for electrical insulation.

With a 20 mm lower sink and 40 mm corner standoffs, approximately 12 mm remains below the sink. Trim bottom leads ≤2.5 mm and retain ≥5 mm clearance from unrelated metal. Q401 uses a separate upright sink beyond the upper board edge, lower edge ≥2 mm above the board; drill its device hole near the lower end to fit the actual TO220. The proposed top fixture envelope is approximately 52 mm. Q402 must not share uninsulated conductive mounting with Q401 or the grounded RF assembly. Provide independent insulated cooling if measured dissipation requires it.

Bond the insulated NTC bead to the pass case and strain-relieve its wires. Electrical open/short checks do not detect physical detachment with intact wires. Connector strain relief, cable exits, lead bending and incoming dimensional fit need inspection on the adjustable bench support. No final enclosure is qualified.

Custom 3D models are sourced dimensional envelopes, not certified vendor STEP files. J301/J501/J701 bodies are missing from the installed standard model library; fresh actual KiCad renders disclose that gap. Their 2D landing/hole evidence is independent of visualization. Physical fit, insulation, reflow, thermal contact and temperatures remain **NOT_RUN**, rather than being inferred from a render.
