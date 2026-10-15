# M5A-R1 — engineering review decision

Date: **2026-10-15**. **M5A-R1 electrical evaluation candidate — NOT RELEASED. All physical tests NOT_RUN.**

**NO-GO for PA/AM coupon layout today; GO for independent review of the revised electrical candidate.** The necessary source-tracing and final-package evidence could not be retrieved as readable images. This milestone therefore has **open acceptance items**, not a completed manufacturer-derived RF implementation. Close the original ST circuit/net trace and exact physical landing first; then a small externally driven PA coupon is the next bounded step. No further architecture study is recommended.

## Recommendation and economic result

Prefer evaluation of **PD54008L-E/PHA-1+**, fixed 5 V driver LDO, final-only drain AM through ST D45H11/BD139 and exclusive 2S boost or 4S buck at 10 V full/7.5 V reduced. Maintain the fully separate training branch and all R0 fail-off functions. Conditional means measured gain/backoff, matching, crest, trough and hot SOA can reject this candidate. The old PD55008-E/PHA-13HLN+ design remains the fallback, not a validated release.

At 10 units the actual component allowances are **€52.63 (2S), €50.70 (4S), €16.37 (training)** net, versus €74.61/€72.77/€16.37 R0. The 2S reduction is €21.97 (29.5%). The complete stronger-driver PD54008 basket is €65.43 (2S) or €63.50 (4S), including its different indispensable 8 V supply. All contain normal full-system functions where applicable. The €36 goal is not achieved. Filters/matching, training, conversion and AM/protection remain significant; 36 preferred 2S MPN positions are unresolved; roughly €43.80 of the €52.63 total remains estimated/family-allowance material. These are partly estimated budgets, not proven repeatable prices.

Desired connector carrier is 1.258925 W for an **assumed**−1 dBd antenna/feed system; 80% AM needs 4.078918 W PEP and a 5.135054 W capability investigation. With 0.75 dB output loss, final-plane capability must be 6.103 W. A 20 dB final-gain assumption requires 19.11 dBm driver output and 22.11 dBm P1dB for 3 dB backoff. Neither final gain nor driver compression has been measured at 144 MHz. Original fixed-supply ST performance does not establish AM or capability reserve.

The low-voltage RF-transfer hypothesis suggests center 3.912 V, crest 6.561 V, trough 1.262 V at 1 ERP/m=0.8, but it is not a characterized transfer law. Pass heat is modeled 4.50 W average under full AM and 5.17 W carrier-only. The sensor trip remains≈66 °C; a specified cooler shared assembly is required. No thermal or SOA PASS is claimed. The modeled 2S3P/M35A target candidate gives 17.3 h full/30.2 h reduced under base assumptions; poor efficiency/current trips can invalidate it.4S1P/M35A gives only 12.4/21.2 h and is not a robust two-target pack.

## Delivered and verified

- [Editable existing KiCad project](../hardware/2m/RF2M.kicad_pro), [R1 PDF](../hardware/2m/review/M5A-R1/RF2M.pdf), actual XML netlist, revised manifest/local symbols and 6/10/20 variant/counterfactual BOMs.
- [Reference audit](M5A_R1_ST_REFERENCE_AUDIT.md), [RF choice](M5A_R1_RF_SELECTION.md), [AM feasibility](M5A_R1_AM_FEASIBILITY.md), [power/thermal](M5A_R1_POWER_THERMAL.md), [cost delta](M5A_R1_COST_DELTA.md), [schematic review](M5A_R1_SCHEMATIC_REVIEW.md) and [coupon gates](M5A_R1_PA_TEST_PLAN.md).
- Actual KiCad 10.0.6 ERC:0 errors/3 documented OPEN-footprint warnings. Netlist/manifest parity; 4096 digital combinations,36 state scenarios,14 detected mutations; 34 critical audit entries with explicit functional-only/open geometry states. This is not physical pinout qualification of Q501.
- R0 preserved at commit`ea671c1`, tag `m5a-r0`, native archive and unchanged historical reports.335 frozen 80 m/ADR/project-baseline files are checked unchanged. The R1 preservation adapter permits only the explicitly new ADR0013 file; the original R0 snapshot is not rewritten. Full and training variants remain one primary 2 m PCB; no second MCU or controller redesign.

## Acceptance status and smallest remaining corrections

| User criterion | Status | Remaining action |
| --- | --- | --- |
| 1. Actual original ST topology trace | **OPEN/blocking** | Readable Figures 12–17 and original Gerber net/line inspection; values alone are insufficient |
| 2. Separate reference from AM capability | DONE/documented | Physical AM/capability still NOT_RUN |
| 3. Obsolete-driver replacement strategy | DONE/conditional | PHA-1+ selected for evaluation; measure gain/P1dB before acceptance |
| 4. PD54008 physical package audit | **OPEN/blocking** | Exact G/D/S pad/source thermal land/orientation from manufacturer drawing |
| 5. Matching justified | **OPEN/blocking** | Replace labelled OPEN harness with traced ST derivative; account for stack-up |
| 6. True AM implementation path | PLAUSIBLE/unqualified | RF transfer and 70–80% clean modulation measurements |
| 7. Crest/trough/dropout | DONE/calculated | Confirm actual low-drain transfer/hot base drive |
| 8. Thermal/sensor consistency | DONE/as a conditional assembly requirement | Hot SOA, thermal attachment and trip delay NOT_RUN |
| 9. Complete 2S/4S comparison | DONE/modeled | Efficiency, cutoff energy and pack tests NOT_RUN |
| 10. Itemized savings | DONE/provisional | Exact quotes/36 OPEN 2S MPN positions remain |
| 11. Actual editable R1 | DONE/evaluation candidate | RF matching and final landing intentionally OPEN |
| 12. Pin/logic regressions | DIGITAL PASS; PHYSICAL PARTIAL | Numeric final map remains blocking |
| 13. Minimum experiment | DONE/specification only | Layout is not authorized in this milestone |
| 14. Unmeasured unqualified | DONE | No invented physical pass |
| 15. No purchasing/fabrication/RF | DONE | No procurement or operation occurred |

Controller 20-pin assignment is retained; module-ID codes 12.1k/27.4k distinguish revised normal populations from R0, training remains 47k. Future controller firmware must recognize the new gain/rail calibration and keep unknown country/frequency/module profiles unarmed. Existing S3/RTC/optional Silicontra hardware is unchanged. Proposed [ADR0013](decisions/ADR-0013-vhf-low-voltage-evaluation-candidate.md) records this candidate without accepting or overwriting earlier decisions.

The retained [2025 rulebook](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf), Appendix 1 T2.8, specifies 144.500–144.900 MHz, better-than 50 ppm,>200 kHz simultaneous-transmitter separation,0.25–1 W carrier ERP, A2A 70–80% AM,8–15 WPM, horizontal antenna 2–3m. Guarded 0.90/0.30 ERP settings are examples only:±0.4 dB gives≈0.821–0.987/0.274–0.329ERP. Actual antenna/feeder uncertainty must fit the limits. IARU rules do not authorize transmission; country profile and applicable unwanted-emission rules remain separate gates. No antenna or legal authorization is inferred.

Next required inputs are specifically the readable original ST circuit/package drawings and original artwork, not approval to manufacture. Once traced and independently checked, review the narrowly scoped coupon layout proposal. No integrated PCB layout, Gerber generation, component purchasing, manufacture, assembly, RF operation or production firmware occurred. Stop for review with the source/package blockers explicit.
