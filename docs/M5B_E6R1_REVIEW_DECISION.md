# M5B-E6R1 — HOLD for native PCB implementation

Starting commit **`85186204619edec32ad1bb2a3044bb55ea399658`**, branch **`m5b-e6-unified-heatsink`**. Analysis executed 21 October 2026. This is a local engineering study, not independent acceptance, manufacturing authorization or operational qualification.

**Carrier-keyed hybrid Architecture C is the preferred circuit proposal. Proceeding to native E6R1 PCB implementation remains HOLD.** Its nominal loss reduction is credible and substantial, but it does not establish a safe full-profile adverse operating envelope or a source-joint fault interrupt. No native KiCad, fabrication archive, controller or RF80 file was changed.

The single most important unresolved constraint is the **installed Q501 junction/source-joint-to-sensor thermal transfer and the resulting safe threshold/delay window**. The source-region observer can be too hot during healthy 1 W continuous MO for the proposed nominal threshold, yet too slow or too weakly coupled to interrupt a degraded joint before 125°C. The original E6 133.79°C counterexample remains exactly reproducible. A fast 10 ms source sensor with an 87°C trip budget still permits approximately 134.72°C in the modeled 5 K/W joint fault. A lower nominal average temperature does not close this gate.

| Gate | Disposition | Evidence / boundary |
| --- | --- | --- |
| A — regulatory compatibility | PASS for method | Official T2.8 permits keyed modulated carrier; all ERP/AM/timing/off-slot/event requirements retained |
| B — electrical keying | Specific proposal; acceptance OPEN | Existing KEY/AF plus local clamp, driver and RF-ready logic; no extra GPIO. 48 loaded loop cases stable, 2 unloaded cases unstable; startup and nonlinear behavior unqualified |
| C — thermal profiles | Conditional nominal benefit; HOLD for complete envelope | At 1 W/40°C nominal BUCK Classic/Sprint/MO PA peaks about 74.31/73.72/87.76°C. Q401 MO 59.51°C has little margin; valid loss/supply and poor-contact scenarios exceed 60°C |
| D — local PA safety | HOLD | Fault lag/joint counterexamples and healthy threshold conflict; no established assembly transfer bound |
| E — RF preservation | Model foundation only; OPEN | Flat-MARK capability retained; ideal envelope/AF headroom calculated. Real AM, RF stability, clean PEP, leakage and spectrum NOT_RUN |
| F — mechanics | Common-cooler concept feasible | Retain one independently supported SK81 100 assembly, estimated 245–270 g; no separate pass/helper coolers or released native geometry |
| G — standard manufacturing | Proposed process compatible; implementation NOT_CREATED | Two-layer 1.6 mm/1 oz FR4, ordinary vias/HASL; no new ERC/DRC, cutouts or manufacturing dataset |
| H — physical qualification | NOT_RUN | No powered, thermal, RF, outdoor, isolation or emissions test |

The completed package contains 37 fresh R1 tests, 25 replayed E6 numerical tests, an independently written ngspice passive-tail fixture, 612 normal thermal rows, 108 thermal sensitivity rows, 288 sensor-fault cases, 18 healthy sensor checks, 54 exact energy rows and 486 explicit whole-system overhead scenarios. Tests pass while preserving unsafe cases; they do not declare thermal qualification. [Execution evidence and reproduction](../hardware/2m/review/M5B-E6R1/REPRODUCE.md) distinguish actual execution from prior review evidence. The frozen-start inventory checks every starting tracked file except the two current documentation indexes.

The smallest next action is bounded source-stack/junction-proxy/sensor step characterization, including a controlled degraded-joint/contact bound and measured hardware interruption latency. Establish a threshold/lag interval that both permits healthy continuous full-profile MO and bounds the 125°C fault ceiling. If it cannot, require a defensible independent hardware PA power/energy restriction. Do not buy a larger cooler, raise thresholds, silently reduce beacon ERP or begin PCB routing to bypass that decision. The [PA closure note](M5B_E6R1_PA_THERMAL_SAFETY.md) gives exact assumptions and experiment boundaries.

Additional qualification remains for converter/MMIC preparation, unloaded modulator recovery and SOA, AF precompensation, drive feedthrough and switching spectrum. The three cooler comparisons are complete; no unlimited topology or component search is proposed. All native RF geometry, controller interfaces, NORMAL/TRAIN_ONLY populations, source-via geometry and existing safety architecture remain the immutable E5 baseline. Prior E6 failure evidence and historical manufacturing archives remain intact. No E6R1 Gerbers, drills, fabrication/stencil ZIP or operational firmware is falsely released. No push, tag, order or hardware operation occurred.

See [rules](M5B_E6R1_A2A_REGULATORY.md), [Morse](M5B_E6R1_MORSE_DUTY.md), [circuit](M5B_E6R1_CARRIER_KEYING.md), [power](M5B_E6R1_POWER_BUDGET.md), [transients](M5B_E6R1_TRANSIENT_THERMAL.md), [protection](M5B_E6R1_PA_THERMAL_SAFETY.md), [cooler](M5B_E6R1_COOLING_DECISION.md), [cost](M5B_E6R1_COST_IMPACT.md) and the [review package](../hardware/2m/review/M5B-E6R1/README.md).
