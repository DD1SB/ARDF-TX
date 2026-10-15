# M5A-R1 — schematic review and verification

Date: **2026-10-15**. **M5A-R1 electrical evaluation candidate — NOT RELEASED. All physical tests NOT_RUN.**

The [existing editable project](../hardware/2m/RF2M.kicad_pro) is evolved in place; [PDF](../hardware/2m/review/M5A-R1/RF2M.pdf), [XML netlist](../hardware/2m/review/M5A-R1/RF2M.net.xml), [manifest](../hardware/2m/RF2M.electrical.json), [position list](../hardware/2m/review/M5A-R1/RF2M_positions.csv) and [variant BOM](../hardware/2m/review/M5A-R1/RF2M_BOM.csv) come from that revision. R0 remains native in its archive and tag `m5a-r0`. RF80/M4 and existing ADR files are unchanged. This is **not** a completed, traced reproduction of the ST RF artwork.

## Implemented changes

- U501PHA-13HLN+→PHA-1+, with correctly named functional symbol and same 1IN/2GND/3OUT+DC/4 ground-paddle connection. DF782 landing OPEN.
- Q501PD55008-E→PD54008L-E functional G/D/S symbol. PowerFLAT5×5HV numeric pad map, thermal source lands and orientation remain **blocking OPEN**. No generic MOSFET footprint is substituted.
- R301/R303 and R401/R414 set 7.5 V reduced/10 V full.4S no longer has a separate high full-power cutoff; remove R830/Q801. Main pack/window, current, OV and independent switches remain.
- U303 becomes TLV76150DCYR with 1GND,2OUT/tab,3IN. Remove driver-buck L303, C408, R406, R407. R413 moves to LDO input. C407 is 1 µF input; C409150µF/25 V output with qualified ESR requirement; D309 bypasses LDO reverse current. Exact C409 part/geometry OPEN. No driver-buck fault model is misrepresented as qualification of the new LDO.
- R506100Ω→10 Ω restores modulator headroom. R511 = 18k sets normal feedback gain 2.8. R606 now feeds fixed bias from VMOD rather than the new 5 V driver rail. Output bulk capacitance is kept upstream of the pass transistor.
- F301 becomes 4 A fast0466004.NRHF because low-battery transmit-slot current can exceed 2 A. Exact supplier quote, footprint/temperature and 50 A-interrupt coordination with the protected pack remain OPEN; the 1.8 A PA trip is preserved.
- Analog thresholds updated: driver≈5.737 V, main≈10.50 V, drain≈8.203 V, upstream current≈1.80 A. Hot comparator common-mode/current-reference regression retained. The increased current threshold requires actual fuse, magnetics and thermal qualification.
- Source pad changes to 3 dB candidate 17.8/287/287 Ω. First tests use larger attenuation/external RF generator. Matching C605/L605/L608/C610 marked OPEN; inherited R0 large-signal estimates are no longer silently labelled PD54008 matching. LPF unchanged pending original-ST trace, with no imported ST harmonic claim.
- TP604 exposes PA_IN50; remove C602 for external final-drive injection so the generator cannot back-drive the MMIC. Test points add no purchased IC or connector.
- MODULE_ID becomes 12.1k(2S) or 27.4k(4S); training remains 47k. Controller pinout unchanged, but new revision/calibration tables are mandatory. Firmware for R0 must refuse an unknown R1ID rather than applying old levels. Controller hardware is not changed here.

The removed overflow supply sheet is preserved in the R0 archive/history. The active hierarchy is 15 sheets plus root,16PDF pages. Regeneration tools use a new R1 output path; frozen R0 tools/reports are not rewritten.

## Supply and enable behavior

20-pin connector assignment remains [R0 contract](M5_2M_CONTROLLER_INTERFACE.md). Logic is 3.3 V; battery current uses separate keyed J301/return. Power and logic can be present separately only with the existing bias/pull-down/isolation behavior verified. SRC_ON isolates the source/bus; NORMAL_PERMIT gates MMIC supply, normal bias and AM command; TRAIN_PERMIT gates the separate buffer and current-modulated BJT. Source clocks alone are not a digital permission to energize the final. Analog off-slot RF leakage and capacitive feedthrough remain measurements.

Raw ARM captures path/profile/context with KEY=0 and SLOT=0. PREPARE, valid heartbeat, mute and SCL-high health qualify the context; delayed ARM gives settling time. Keep SLOT low for at least 50ms and verify PA_RAIL_ADC after profile capture/rail change. A fault clears context; ARM held high cannot automatically rearm. Retuning first withdraws SLOT/ARM and drive; I²C activity clears permission. No live profile/path transfer is allowed. PREPARE must be withdrawn between scheduled slots for the endurance model to apply.

The RF outputs have independent conductive branches and different SMA/MCX connectors; no watt-output RF selector feeds the training port. Training-only assembly omits all normal power parts and uses R519 in place of U207's normal-health function. Effective training values/net connectivity/MPNs/footprints are checked against R0 for all 104 fitted physical parts. Isolation under coupling/device faults still needs physical measurements.

## Actual checks and limits

KiCad 10.0.6 ERC was run: **0 errors,3 warnings**. Warnings are the intentionally OPEN footprint selections J301, J701 and C409; they are not excluded. Empty RF device footprints do not necessarily trigger ERC, so their separate audit remains essential. No PCB exists and no DRC result is claimed.

The actual exported XML is checked against every manifest pin. Netlist-derived digital tests pass **4096 combinations,36 scenarios,14 rejected mutations**. These cover captured selection, heartbeat/mute/reset/I²C loss, invalid arming, no dual path, faults requiring fresh ARM, keyed tone with in-slot carrier, absent PA population, physical-terminal mutations and revised value regressions. There are 34 audited critical-device entries: **Q501 is functional-only**, and several numeric mappings still have OPEN geometry. “PASS” in [verification.json](../hardware/2m/review/M5A-R1/verification.json) means these limited checks passed, not physical-package or analog qualification.

[Pinout-audit.json](../hardware/2m/review/M5A-R1/pinout-audit.json) explicitly sets physical release BLOCKED. D45H11 and ST BD139 remain 1B/2C/tab/3E. TI TL431 remains 1K/2REF/3 A. LDO pad 2/tab is 5 V. The new final must not inherit PD55008 numeric pads or a generic 8-power-pin assumption. No PD84001 footprint or obsolete part is introduced.

Remaining analog items: real watchdog/ARM propagation and supply collapse, comparator VOL/common-mode/tolerance, D309 reverse discharge, LDO fault isolation≤20 µs, source feedthrough, hot pass SOA, AM-loop phase margin, gate-bias thermal stability, RF matching/stability and port isolation. The tests do not model those behaviors. Source classification is detailed in the [reference audit](M5A_R1_ST_REFERENCE_AUDIT.md); all physical gates remain NOT_RUN.
