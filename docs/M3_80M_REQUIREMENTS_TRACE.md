# M3A requirement and evidence trace

Date: 2026-10-14. Existing requirements/ADRs are retained; the current task authorizes the 80 m electrical schematic, not acceptance of all power proposals or hardware release.

| Current mission / existing baseline | Concrete deliverable / evidence | Closure |
| --- | --- | --- |
| Proven PA comparison, actual circuits | [Selection](M3_80M_PA_SELECTION.md); original QCX, ON7YD and pinned OpenARDF schematic/BOM references; HG0HK circuit unavailable | One IRF610 implementation selected; publisher data distinguished from our calculations |
| Three primary PCBs, S3/RTC/optionalLoRa/local synthesis; SYS-001/002/003 | [Editable RF schematic](../hardware/80m/RF80.kicad_sch), controller interface and separate local Si5351 | No new MCU/RTC/primary PCB; proposed controller supply still needs review |
| Classic approximately3 W /1.2 W extended, calibrated Sprint; RF80-001/002 | TPS54302 selectable rails, LM5134B/IRF610, transformer/filter and QCX-derived shaper | E0–E5 power/efficiency/shaping/mismatch gates NOT RUN |
| Independent nominal10 mW/compact antenna; RF80-004/005/008/009, FOX-008 | Separate AC00 branch, rail-following inputs/mute, own filter/pad/J502; explicit30 cm accessory/return/loading work | E6/E8 conducted calibration, fault/isolation and30/250 m field gates NOT RUN |
| Autonomous fail-off, safe startup/retune; RF80-006/007 | Progress lease/SCL inhibit, sticky rearm, exclusive requests, latched power modes, analog trips, independent normal switch/driver mute and shared key-tail with separate Fox mute | ERC/netlist/Boolean checks pass; E0/E1 physical tests remain mandatory |
| 4S normal /2S Fox, 12/24 h targets; PWR-001/002/003 | Bounded local buck, shared protected input, separately supplied3.3 V logic, detailed standby/shaper calculation | Modeled13.2/25.2 h on4S1P25R; poor efficiency fails; E9 NOT RUN |
| Minimal support with explicit deletion assessment; COST/FOX scope | [BOM review](M3_80M_BOM.md), generated per-reference CSV, detector/DAC/isolator deletion rationale | No price-closed purchasing claim; unused allowances not hidden |
| Actual editable CAD, MPNs/footprints, windings, ERC | Local library tables,4 custom component patterns, [PDF/ERC/netlist](../hardware/80m/README.md), winding/pin review | KiCad10.0.6 ERC0; package mapping checked; unquoted/mechanical gates explicit |
| Required interface/safety/test access | J10116-pin contract, J301 power/return, dissimilar J401/J502, probe and removable component access | Controller/fixture contract and physical keying/current-return checks before evaluation layout |
| Complete-system accounting, quantities6/10/20 | [Component workbook](M3_80M_COMPONENT_WORKBOOK.md) and explicit replacements of old socket/power-half allowances | Historical Fox audit intact; material/infrastructure/labor separate |
| VHF remains trueAM,1 W carrierERP/PEP | [Review decision](M3_80M_REVIEW_DECISION.md) explicitly preserves current VHF engineering | No VHF circuit/BOM/power change performed |
| Stop before manufacture | [ADR-0012 proposal](decisions/ADR-0012-m3a-hf-electrical-implementation.md), [test gates](M3_80M_TEST_PLAN.md) | Electrical review delivered; no PCB/Gerber/order/fabrication/assembly/production firmware |

Primary IARU sections and legal distinctions remain in [M1 trace](M1_REQUIREMENTS_TRACE.md) and [M2 power trace](M2_POWER_REQUIREMENTS_TRACE.md). M3 does not redefine conducted HF power as ERP, or a component's DC rating as measured RF survival.

## M3A-R1 correction trace — 2026-10-14

The original RF requirements above remain. Corrected control implementation and validation evidence:

| Review requirement | Actual implementation | Check / physical gate |
| --- | --- | --- |
| U202 polarity/progress fail-off | Q13 lease,/Q12 bus holdoff; spare HC74 heartbeat witness | Pin assertions, negative mutations and timeout/startup scenarios; R1-L1 |
| Safe retune/stuck bus | POR + SCL/SDA + holdoff qualification | Both line faults and retrigger model; R1-L1/L3; both-high needs software progress contract |
| Fresh deliberate arm after faults | HC174 raw-edge context, HC74 delayed acceptance, request-withdrawal reset | Pending-clock/held-ARM/KEY-high/path/profile scenarios; R1-L2/L4 pulse/race tests OPEN |
| Independent normal/Fox RF | Separate driver INB / Fox NAND mute and output networks | Connectivity/permit tests; R1-R1/R2/I1 and E6 physical isolation OPEN |
| Fox reduced population | U312/PA references/thermal DNP; U314 common UV retained | Actual full/Fox manifest comparison; R1-L1/P1, UV qualification OPEN |
| Driver voltage margin | R410/C404 low-ESR reservoir + independent switch/OV | Passive ngspice imposed20 µs bound; R1-P1 physical response OPEN |
| Cost simplification/provenance | U213/U214 deleted, PA open collectors combined, watt monitoring omitted on Fox | Git-tagged R0/current comparison and pooled6/10/20 baskets; supplier gaps OPEN |

[R1 audit](M3A_R1_LOGIC_AUDIT.md), [verification](M3A_R1_VERIFICATION.md), [generated cost delta](M3A_R1_COST_DELTA.md). No accepted ADR or physical qualification status changes.
