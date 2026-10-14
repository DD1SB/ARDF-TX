# M3B — safety gates

> **2026-10-15 correction notice:** This is a historical pre-E2 record. E1/R1 ST BD140 pin/orientation claims and the E1 manufacturing recommendation are superseded by [M3B-E2 corrections](M3B_E2_CORRECTIONS.md) and the [E2 decision](M3B_E2_REVIEW_DECISION.md). Use E2 assembly/netlist files: Q403 **1B/2C/3E**, illustrated ST face toward **PCB+Y**, and U311 TI DBZ **1K/2REF/3A**. E1 drawings are not build instructions. Frozen historical checks are not current E2 verification.


Date: **2026-10-14**, M3B-E1. **Every physical test below is NOT_RUN.** CAD and passive simulations do not establish hardware safety. The first supply is a bounded, current-limited laboratory source; no unqualified Li-ion pack connection.

## Input correction and numerical limits

TPS22810 remains limited to **18 V operation / 20 V absolute maximum**. The **SMBJ17A is not an 18 V clamp**: stand-off, breakdown and pulse-clamp voltage differ. No switch margin is credited to its nameplate. Reverse polarity is still blocked by SS34 after F301; this does not protect against a wrong positive-voltage supply or a shorted diode.

M3B adds **R350 1.5 Ω/1 W ±1%** ahead of the normal rail and **C350 100 µF/35 V ±20%** after it. `VIN_PACK` (after reverse barrier) feeds pack sensing/C314; `VIN_PA` (after R350) feeds the buck and existing TVS. The operational input remains **12.0–16.8 V**. No universal surge rating or unsafe pack interchangeability is asserted.

[Reproducible model and results](M3B_POWER_ANALYSIS.json), [input SPICE deck](../analysis/m3b_input_surrogate.cir):

| Calculation / assumed envelope | Result and meaning |
| --- | --- |
| Source step | 16.8 V normal maximum; **17.0 V sensitivity margin**, not a permitted charger setting |
| Cable/source | L = 0.1/1/10 µH, source R = 0.02–1 Ω; **L ≤10 µH** is the proposed installation bound and needs measurement |
| Damper/bulk corners | R350 minimum 1.4775 Ω including extra tolerance allowance; bulk 80–145 µF; simple series-RLC maximum ≤17.0 V in the stated envelope |
| Full passive input surrogate | Generic diode, upstream capacitance nearly zero/40/110 nF, 80 µF bulk with 0.03 Ω ESR, 24 actual ngspice cases including 100 µH stress. At L≤10 µH, maximum `VIN_PA` **16.972 V**; maximum undamped upstream node across all cases **21.738 V** |
| Outside-envelope stress | Analytic 100 µH case **18.00013 V**, marginally above 18 V: **not accepted**. The generic-diode SPICE stress peaks 17.633 V downstream; model disagreement reinforces the wiring bound, not a qualification claim |
| C314 change | Upstream 100 nF is now **50 V**, not the prior 25 V; sense divider309k/10k limits the modeled21.738 V transient to0.682 V |
| Insertion upper I²t | `Cmax V²/(2 Rmin)` = **0.01399 A²s**, 18.3% of fuse nominal0.0766 A²s; this does not prove repetitive pulse life or minimum-melting margin |
| Damper loss | At0.6 A active:0.54 W; at20%:0.108 W average. At12 h this adds1.296 Wh. At0.8 A active:0.96 W before hot derating: **not a continuous rating** |
| Cable stored energy | 10 µH at0.8 A stores3.2 µJ; arcs, charger overshoot and supply-source energy are additional mechanisms, not bounded by this number |

For scale only, adding the conservative0.6 A/20% damper loss to the retained full-mode20.743 Wh/12 h model gives22.039 Wh versus22.861 Wh modeled usable4S1P energy: only0.822 Wh margin. This is not a revised endurance pass; real current, voltage drop and cutoff require measurement. The extended setting must use its own lower-current loss, not the full-power assumption.

This treatment reduces realistic insertion resonance without replacing the architecture with a universal converter. It is conditional on measured source/wiring impedance, capacitor behavior and resistor pulse/hot limits. F301's **35 A interrupt rating** must be coordinated with external pack/BMS fault current; the on-board fuse alone is not qualified to break an arbitrary multi-parallel Li-ion fault. Its nominal I²t cannot guarantee clearing before a semiconductor fails. Initial PSU limits avoid that assumption.

**Gate I:** Driver/PA absent; record VIN_PACK, VIN_PA and VPA_ISO during controlled connection/disconnection at12/14.4/16.8 V with representative wiring and capacitance. Require VIN_PA ≤18.0 V including probe uncertainty; reverse barrier leakage/no backpower acceptable; no fuse nuisance or damaging resistor pulse. Establish an upstream pack/BMS interrupt-current limit and connector polarity before a pack is permitted. Wrong-source DC overvoltage remains excluded; label and keyed pack/fixture routing are required. Failure means **NO-GO for pack/full-voltage operation**, not silently trusting the TVS.

## Driver overvoltage and layout parasitics

LM5134B: **4–12.6 V operating**,14 V absolute; VDD is not connected to raw4S. R4104.7 Ω and C40447 µF/25 V polymer remain the local delay reservoir. The comparator/switch **≤20 µs** interruption and C404 effective transient ESR **≤0.5 Ω** are **unverified physical assumptions**. Manufacturer typical switch turn-off is not a guaranteed complete fault-response bound.

Actual linear-passive ngspice results (initial rail8.6 V, R410 minimum4.653 Ω, C404 minimum37.6 µF, ideal imposed disconnection):

| Fault step / imposed delay | ESR / layout inductance | Peak VDRV |
| --- | --- | ---: |
|16.8 V /20 µs |0.03 Ω /10 nH |9.558 V |
|18 V /20 µs |0.5 Ω /100 nH |10.298 V |
|18 V /100 µs |0.5 Ω /100 nH |**12.864 V — FAIL** |
|18 V /20 µs |1.5 Ω /100 nH |11.417 V; does not waive the selected capacitor gate |
|18 V /20 µs; no useful ceramic capacitance credited |0.5 Ω /100 nH |10.989 V |

[Deck/waveform](../analysis/m3b_driver_surrogate.cir) and [CSV](../analysis/m3b_driver_surrogate.csv) are simulations. These are imposed timing surrogates, not models of TPS54302 failure, comparator delay, real switch turn-off, PCB inductance or semiconductor SOA. The layout places C404 and driver ceramics close to U401, retains low-inductance local returns and exposes VDRV/PA_INB/guard/switch nodes. Inductance100 nH is sensitivity input, not extracted board parasitics.

A passive clamp alone was **not** credited as a guaranteed fix: a nominal12 V zener's tolerance/dynamic resistance may allow >12.6/14 V, while a lower clamp can absorb sustained current if the switch sticks. Such a clamp would need guaranteed curves, pulse-energy and single-fault analysis; adding an unqualified zener is not safer evidence.

**Gate D:** With **U401 and Q402 absent**, perform a separate, bounded failed-buck rail injection after isolating the buck (remove L301 or disconnect its output). Use a current-limited source, external rated switch/fast step and representative dummy loads; do not drive against the buck. Supply the safety logic normally. Measure analog OV threshold → PA_INB and physical TPS22810 opening and VDRV. No whole-board28 V test. Require actual interruption ≤20 µs and VDRV ≤12.6 V including probe/temperature tolerances at every corner; separately confirm C404 ESR/temperature behavior and no unsafe post-trip reopening. Only then fit the driver. Failure requires a targeted electrical correction **before** high-voltage RF operation. Bounded passive testing can be performed without sacrificing a driver.

## ARM/reset and withdrawal

R1's Q1 pin13 lease, /Q2 pin12 quiet holdoff, heartbeat-edge witness, raw-ARM accepted context, key-low requirement, health clear, captured mode/path and key-tail withdrawal are preserved. The actual current-netlist automated suite passes, but ideal event ordering cannot establish asynchronous pulse widths or metastability.

**Gate L:** Observe raw ARM, ARM_ACCEPT, ARM_CLK, RESET_N, ARMED, LEASE_OK, BUS_QUIET, PA/FOX permits, PA_INB and physical rails. Use≤1 pF active probes; compare with probe removed/changed. Sweep fault/reset/LEASE/SCL edges across raw and delayed ARM, fast3.3 V ramps/collapse and stuck bus levels. Require clear pulses at the device pins longer than the relevant manufacturer minima with ≥2× measured margin; use a conservative100 ns clear-pulse target until the exact3.3 V/temperature requirement is established. No spurious permit, no false progress on reset release, and **no automatic rearm with ARM still high**. A fresh low/high ARM edge with KEY low and healthy captured context is required. This is a gate for a real device and scope record, not another truth-table claim.

## RF, port and thermal gates

**Gate R:** Correctly rated50 Ω loads; staged low-energy tests first. No normal PA beyond qualified rail/gate/drain limits. Record conducted3 W/1.2 W/Sprint calibration, spectrum, key edges and efficiency at3.510/3.550/3.600 MHz and battery corners. Drain peak must remain below the test-plan limit and within the transistor's voltage/current/SOA at temperature. Normal LPF and transformer remain the original reference arrangement; derived-board performance is unmeasured.

**Gate F:** Independently calibrate9–11 mW into50 Ω, verify no output when unarmed, startup/retune leakage and RF from the normal path at the Fox connector. At3.3 W normal output, the retained66 µW leakage ceiling requires approximately47 dB isolation; verify dynamically, not merely a DC continuity test. Verify the compact accessory100 mW fault-energy capability, source-current limit and backpower behavior. The compact30 cm radiator/counterpoise/loading network is a separate accessory; reference-load power is not field range. Preserve30 m audible/250 m not-audible evaluation from the retained rulebook methodology.

**Gate T:** Bonded remote NTC, thermocouples on IRF610/BD140/R350/buck/inductor/driver and hot SOA records. Open/short sensor electrical trips and **physical attachment failure** are separate tests. No thermal validation, heatsink-size claim, continuous-beacon endurance claim or12/24 h battery-life claim has been made.

[Staged procedure](M3B_BRINGUP_PLAN.md). **GO for engineering review of a small bare evaluation-PCB order only; NO-GO for unrestricted assembly/power/RF or production release.** Approval for ordering is still required from the user and is not implied by generating Gerbers.
