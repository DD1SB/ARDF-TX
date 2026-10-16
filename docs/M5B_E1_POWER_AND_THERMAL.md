# M5B-E1 power and thermal review

2026-10-16. All numbers below are datasheet limits, calculations or engineering assumptions. **Physical qualification: NOT_RUN.** Use current-limited laboratory supplies for initial commissioning; no unrestricted Li-ion fault testing is authorized.

## Assembly and voltage boundaries

The full populations are mutually exclusive. BOOST2S uses protected6.0–8.4 V nominal pack range, TPS611781 boost and L302; BUCK4S uses protected12.0–16.8 V, TPS54302 and L301. J302 routes only the selected output. R101 IDs are18.2 kΩ/39.2 kΩ respectively; training-only82 kΩ. R807/R809 are58.3 kΩ/39.2 kΩ for2S and24.9 kΩ/14.7 kΩ for4S. Nominal UV thresholds approximately6.21/12.15 V intentionally inhibit before the conservative absolute discharge endpoints; RF acceptance uses voltages above these thresholds. A voltage-window circuit plus correct assembly prevents the intended wrong-pack activation; no protection against arbitrary unlimited external voltage is claimed.

The full upstream modulation rail is approximately9.021 V. Reduced4S uses approximately7.510 V;2S retains its fixed higher rail. Raw4S never reaches PA gate/drain or MMIC. The 2S boost's low-power/dropout population rules remain as corrected in R4. The added C960/C961 reservoirs sit at their own converter inputs; each is DNP in the other population.

Input fuse, reverse MOSFET, voltage windows and TVS are retained. A TVS working-voltage label does not guarantee a clamp below every downstream absolute maximum. Long-lead insertion, disconnect, wrong supply, ESR and ground bounce require bounded tests. In particular a full4S pack with ringing is not equivalent to a16.8 V laboratory source at device pins. First tests use short leads, current limit and monitored input voltage. A pack-protection BMS does not replace RF-stage protection. The actual fitted F301 is the retained4 A Littelfuse466 candidate; its interrupt rating/I²t and external pack/BMS prospective fault current require coordination before pack testing. Laboratory source/load limits are independent of that fuse;raw2S input may require3.5 A after staged qualification while the protected regulated-rail load is bounded≤2 A.

## MMIC driver supply

The physical chain is upstream VMOD → R4134.7 Ω/1 W and reservoir → TLV76701 preregulator → TLV76150 5 V regulator → TPS22810 → liftable R952 → low-DCR L604/PHA-1+. U950's0.8 V reference and58.2k/10k divider set5.456 V. With±1% reference and0.1% resistors, the simple tolerance range is5.392–5.520 V. This does not include every load/transient error; verify the actual part's complete accuracy and effective capacitor limits.

| Element | Normal/fault boundary |
| --- | --- |
| TLV767 U950 | Normal VIN approximately8–9 V, recommended max16 V, absolute18 V. A bounded16.8 V converter fault exceeds recommended VIN but remains below absolute; it is fault-only exposure requiring a power-only test, not a guaranteed continuous operating point. |
| TLV761 U303 | Normal input5.392–5.520 V; recommended18 V/absolute20 V. It is the independent remaining barrier if U950 shorts. Its guaranteed high-current dropout cannot be linearly scaled and called a guarantee at180 mA; actual output at worst load/temperature must pass before MMIC fitting. |
| TPS22810 U305 | Recommended2.7–18 V, absolute20 V. It replaces the marginal TPS22919. Both the normal regulated rail and the defined16.8 V fault are within its input rating. Its propagation time remains a measured shutdown item. |
| PHA-1+ | Normal target4.8–5.2 V at its physical feed; absolute6 V is not a normal operating target. Fault acceptance is≤5.7 V at the isolated MMIC node with the MMIC absent, plus correct inhibit and discharge. |

If U303 alone fails short, U950 limits the source near5.52 V and OV detection withdraws permission. If U950 alone shorts, U303 sees a rated input and regulates. A simultaneous short of both regulators is outside this single-fault argument; do not call it redundant surge immunity. The old≤20 µs assumption is no longer the sole voltage barrier. Detector, switch, inhibit and discharge times must still be measured. Their failure behavior, rapid collapse and repeated cycling are not proven by a DC tolerance calculation. Initial power-only fault pulses are≤100 µs,≤0.25 A,≤1 Hz (≤0.42 mJ supplied at16.8 V);longer or continuous faults require a separate regulator dissipation/temperature assessment. Approximately2.1 W could be dissipated by a surviving5 V regulator at16.8 V/180 mA. The normal isolated-regulator-short case at the9 V rail is less demanding than this combined fault fixture.

Driver OV nominal is5.269 V, tolerance estimate5.173–5.365 V. C409 is150 µF25SVPG150M with13 mΩ specified100 kHz ESR; capacitance bias/temperature, wiring inductance and switch layout are physical qualifications. C950/C951 require≥1 µF **effective**, not just printed capacitance.

The old180 nH choke could drop0.297 V at180 mA. New150 nH/33 mΩ max loses5.94 mV; allowing30% hot DCR rise and TLV761−1.75% yields approximately4.905 V before switch/trace losses. Verify≥4.8 V under actual maximum RF current. The selected choke's RF loading is not qualified merely by its DC improvement.

## Current trip and modulation

The original current divider required3.752 V INA output from a3.3 V supply. R309=0.068 Ω and R828=5.11 kΩ correct the nominal threshold to1.797 A at2.443 V INA output. Shunt1% and amplifier/reference/divider tolerances set the actual threshold spread. Test the trip and latch using a bounded electronic load≤2 A on the protected regulated rail before RF;after preceding checks allow up to3.5 A raw2S input or2 A raw4S input as needed. Do not use the fuse as a fast semiconductor current limiter.

Initial full-envelope voltage commands are7.2 V crest,4.0 V center,0.8 V trough at80% **voltage** modulation. Reduced starts4.0/2.222/0.444 V. These are not calibrated RF modulation settings: PA knee, bias, gain compression and impedance change with drain voltage. The retained filtered PWM, op-amp feedback, D45H11 pass device and BD139 helper provide a concrete sine-supply circuit. Verify feedback polarity, loop stability, PWM ripple, crest dropout, no-tone current and shutdown. The ESP32-S3 has no assumed original-ESP32 DAC.

At−1 dBd net antenna/feed gain,1 W ERP requires1.259 W connector carrier. At80% AM, PEP=Pc(1+m)²=4.079 W; with0.75 dB matching/filter loss the final must supply4.848 W. Optional1 dB extra capability would require approximately6.10 W at the final and is not an additional championship requirement. ST's approximately5 W fixed-supply reference is not evidence of clean80% AM. Calibration should target approximately0.9 W ERP nominal if combined uncertainty is0.4 dB (upper bound approximately0.987 W); capability for the requested upper-range profile is still tested. Reduced0.30 W ERP remains above the0.25 W minimum with a suitable measured uncertainty budget.

## Feasible thermal assembly

Q401's exposed collector/tab carries VPA. Use a flat insulating thermal pad, shoulder washer and continuity test before attaching to the external pass-device sink. Q402's exposed collector carries MOD_SINK; never bolt it bare onto the same conductive grounded sink. The upright top-edge devices permit separate clamped sinks without crossing the RF strip. Mount heatsinks/supports before soldering leads; do not use the thin PCB as a lever.

The grounded PD source has twelve0.6/0.3 mm through-vias into the lower ground plane, a14 ×12 mm bottom ground-copper contact window (with two mask strips preserving source-via tents), and a proposed16 ×44 ×8 mm grounded spreader secured at(112,32)/(112,68)mm. Use a separately supported bottom sink and insulating clearance from protruding component leads. Four cornerM3 holes support approximately40 mm bench standoffs; trim bottom leads≤2.5 mm and maintain≥5 mm sink clearance away from the intended grounded contact. The proposed spreader is a dimensional machining assumption, not an ordered part or a demonstrated thermal resistance.

Two separate Fischer SK48 50SA-class sinks fit the external fixture. Use conservative3.5 K/W, not the best end of the catalog2–3.5 K/W range. The estimated full-power pass dissipation is approximately2.8 W with80% AM,3.76 W no-tone. At40°C ambient,3.5 K/W sink plus assumed1 K/W interface gives approximately57°C case and66°C junction using2.5 K/W junction-to-case. Reduced2S no-tone is approximately3.43 W. These are thermal models, not hot DC/repetitive SOA qualification. Measure BD139 dissipation as well.

NTC nominal trip is65.85°C; require normal measured pass case≤60°C at the chosen worst ambient, leaving margin for sensor lag and tolerances. Bond the insulated bead to the pass case near its heat source. Open/short sensor faults inhibit normal RF; an intact-wire detached bead is **not** electrically detected. Do not raise the trip to conceal inadequate cooling. Proposed PA via conduction is approximately7.35 K/W for twelve parallel ideal25 µm-plated barrels, before spreading/contact/solder voids; it is not a proven PA-to-sink resistance. PA temperature and source solder quality are mandatory measurements.

## Energy model

The reproducible [power-state](../hardware/2m/review/M5B-E1/power-states.csv), [endurance](../hardware/2m/review/M5B-E1/endurance.csv) and [sensitivity](../hardware/2m/review/M5B-E1/sensitivity.csv) tables separate estimates from measurements. Assumptions:20% scheduled transmission, controller0.14 W, RF idle0.04 W with PREPARE/PA_PREPARE off between slots, driver146.3 mA, PA efficiency50% full/40% reduced, boost87%/buck91%, battery aging80% × cold90% × reserve90%. The RF chain is not assumed equally efficient at both power settings.

| Profile | Mean battery W | 12 h Wh | 24 h Wh | Continuous beacon W |
| --- | ---: | ---: | ---: | ---: |
| Full2S | 2.058 | 24.69 | 49.39 | 9.569 |
| Full4S | 1.975 | 23.70 | 47.41 | 9.156 |
| Reduced2S | 1.554 | 18.64 | 37.29 | 7.048 |
| Reduced4S | 1.277 | 15.32 | 30.65 | 5.664 |

Four minimum-energyM35A-class cells provide30.845 Wh after those deratings. High-capacity2S2P/4S1P are plausible12 h full candidates. For24 h reduced,2S3P provides useful modeled margin;4S1P is approximately24.16 h with negligible margin and is **not** a robust qualified minimum, so4S2P is preferred. The2450 mAh class, LoRa absent/intermittent/continuous receive and poorer PA/controller/converter assumptions are separately tabulated. Continuous beacon endurance is far shorter; eight cells do not meet the corresponding12/24 h cases under this model. The actual smallest acceptable pack depends on measured current, idle state, temperature, aging and cutoff. No endurance result is measured.

The bottom-source spreader proposal is16×44×8mm,covering x104–120/y29–73mm with the existing M3 centers at(112,32)/(112,68). Its8mm thickness leaves≥5.5mm clearance above a lower sink when protruding leads are trimmed≤2.5mm. With a20mm-deep lower sink and40mm bench supports,approximately12mm remains below the sink. Use an electrically insulating,thermally conductive sheet across the whole spreader face;do not rely on solder mask as the electrical insulator. Initial fixture specification:0.15–0.25mm thickness,conductivity≥3W/mK,dielectric rating≥100V. Exact sheet/price is OPEN external fixture material,not a PCB footprint blocker. At0.25mm and14×12mm contact,the ideal bulk term is approximately0.50K/W before contact resistance;the total1K/W interface assumption still requires measurement. Ground the metal block separately with a verified strap;the twelve PCB source vias carry the primary RF return. Flatness,insulation and continuity must pass before power. The pass sink is a separate65mm-wide×50mm-tall vertical SK48 extrusion,with its lower edge≥2mm above the PCB and fins extending beyond the top board edge. Drill its device hole near the lower end to match the actual installed TO220 hole height;do not center the device on the sink and intersect the PCB. This creates a roughly52mm top-side fixture envelope,not a finalized enclosure. BD139 can remain separately cooled only if measured dissipation/temperature permits;otherwise use its own suitably insulated clip sink.
