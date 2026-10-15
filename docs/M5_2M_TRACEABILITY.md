# M5A requirements and baseline trace

Date:2026-10-15. Existing80m/controller/ADRs are preserved by335 starting SHA256 hashes. The requested baseline document paths exist; `hardware/2m/` had no earlier native project, so RF2M is the first VHF implementation. No accepted ADR is overwritten; ADR0011 remains proposed.

| Requirement | Direct authority / implementation | Verification and remaining gate |
| --- | --- | --- |
| RF2-001 championship | IARU PartB2025 Appendix1T2.8, printedp10:144.500–144.900MHz; better50ppm; simultaneous separation>200kHz;0.25–1W ERP;A2A70–80%;8–15WPM;horizontal2–3m | Rechecked primary rules; carrierERP interpretation is the user's explicit sizing convention. Actual antenna/ERP not measured. |
| RF2-003/004 trueAM and PEP | User requirement; Q401/Q402/U401/U402; calculated1.259W carrier/4.079W PEP at−1dBd,m.8 | Sine-voltage servo implemented; actual RF transfer, gain, distortion and PEP NOT_RUN. |
| RF2-006 off-slot / national rules | T2.4 no unscheduled transmitter/antenna RF;T2.1 country law;T2.5 horizontal omnidirectionality | Hardware path gating plus source shutdown; no finite leakage test is a rulebook exemption. Country/mask/license OPEN. |
| RF2-007 training frequency flexibility | User locally permitted band; hardware144–148MHz evaluation range, independent championship validation | ARM contract requires country/profile/register checks. No firmware or legal-frequency validator has been implemented; country unset must prevent arming. |
| RF2-002/005 protected low output | User; U701/Q701/J701 separate from Q501/J501 | Independent clock inhibit/base clamp/fixed pad; no conductive watt-output transfer. Calibration/isolation/field tests NOT_RUN. |
| SYS-001/CTRL-001/003 | Accepted3PCBs, S3/RTC/optionalSilicontra | No new MCU/RTC/board; no80m changes. Actual Silicontra MPN still OPEN. |
| CTRL-002/005 fail-off and interface |20-pin proposed VHF contract, separate pack connector, dedicated VHF I2C, watchdog/HC174 captured ARM |4096 static combinations,36 scenarios and8 mutations; analog delays and controllerGPIO allocation remain review gates. |
| SYS-008 endurance supersession | User12h full/24h reduced, preservedM2 cell/state assumptions |60pack/profile rows plus144sensitivity cases; calculations only, no qualified battery minimum. |
| SYS-009 repeatable cost | User6/10/20 units; actual position-derived variant CSV |ObservedUSD/ECB conversion and explicit estimates separated. Original€15–30/€36 goals are not achieved by the current conservative candidate. |
| CAD implementation | UserM5A, actualRF2M hierarchical native schematic/library/manifest |ERC/netlist/pin audits and readablePDF; noPCB, Gerbers, procurement or physical test. |

The2025 rulebook is the specifically requested championship baseline, not a claim that no later federation amendment exists. Event organisers must confirm the governing edition and national obligations before radiated use. The source log records what was accessed and what could not be recovered.
