# Power-reassessment requirement trace supplement

Date: **2026-10-14**. This supplements [M1 trace](M1_REQUIREMENTS_TRACE.md); earlier IDs/observations remain history. The user explicitly supersedes endurance and requests added battery classes, while circuit implementation remains proposed in [ADR-0011](decisions/ADR-0011-dual-voltage-power-and-endurance.md).

| ID | Source / status | Current evidence / verification route | Remaining closure |
| --- | --- | --- | --- |
| SYS-004 | USER 2026-10-14 / LOCKED | Six-pack comparison and module capability matrix in battery architecture; P4/P5 | Hardware identity/current/voltage compatibility |
| SYS-005 | USER / LOCKED | Eight-cell maximum candidates, separate compact 2S1P Fox; new ADR proposal | Review actual 4S implementation |
| SYS-008 | USER / TARGET, explicitly replaces earlier 24 h maximum objective | 12/24 h matrix in power modes and reproducible endurance results; P5 | Selected output/profile, measured full-period RF output |
| PWR-001 | USER / TARGET | Battery architecture component-rating audit, 6.0–16.8 V controller; P1/P4 | Startup/transient/dropout/temperature |
| PWR-002 | USER + selected cell primary documents / TARGET | Source register, external protection/balancing and charger incompatibility; P5 | Exact BMS lot/thresholds/charger current/termination |
| PWR-003 | USER / TARGET | All-pack/capacity results, peak estimates, idle/LoRa and sensitivity; P3/P5 | Actual efficiency/ESR/current/weakest-group energy |
| PWR-004 | USER / TARGET | Passive pack ID plus independent voltage/capability checks, fail-off contract; P4 | Wrong-ID/open/short/brownout/legacy-module tests |
| PWR-005 | USER / TARGET | Same-cell comparison, 6/10/20 itemized CSV with actual demand/price breaks and external costs | Live baskets and unquoted material/fabrication |
| PWR-006 | USER / TARGET | Explicit model classes, 0.65 unverified RF-window sweep, minimum/typical cell separation and poor-efficiency/idle sensitivity | Hardware measurements; no battery/RF simulation pass |
| PWR-007 | USER + IARU T2.2/T2.4/T2.6/T2.8/S6/FT2.6 / LOCKED | Fixed event profiles; valid range/AM/antenna definitions, UV stops RF; P1/P2/P6 | Organiser ERP convention, calibration uncertainty, field protocol |
| PWR-008 | USER / LOCKED | Five requested documents + sources/workbook + proposed ADR; review stop | User review before physical development |

Unchanged RF80/RF2/CTRL/RULE/PREP/FOX requirements retain earlier source/test mappings, including separate compact matching/10 mW reference/30–250 m field tests, MMIC compression, true A2A, RTC and optional Silicontra. Neither new supply voltage nor reduced endurance relaxes those requirements. All physical P1–P6/H0–H9 gates are **NOT RUN**.
