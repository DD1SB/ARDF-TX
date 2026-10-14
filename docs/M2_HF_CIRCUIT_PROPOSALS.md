# 80 m circuit proposals: watt CW and independent Foxoring

**Review update, 2026-10-13:** The [proven-circuit comparison](M2_80M_REFERENCE_COMPARISON.md) and [new topology proposal](M2_80M_RF_TOPOLOGY.md) propose a documented SignalSlinger/FlexFox80 core and a near-1 W economy population. [ADR-0010](decisions/ADR-0010-proven-80m-core-and-power-target.md) requires review before changing the baseline. The earlier 5 W/AC-drive/seven-pole/feedback-shaper proposal below is preserved as historical analysis; its simulation does not validate the new circuit. No VHF decision changes.

Date: **2026-10-13**. **Review proposals, not released schematics or validated RF hardware.** These original functional connections and starting values implement the conditionally accepted three-PCB/local-synthesis architecture. No PCB outline, connector footprint or manufacturing file is fixed. Evidence is in [M2 sources](M2_SOURCES.md); tests are in [RF evaluation](M2_RF_EVALUATION.md).

## HF-W1: programmable IRF610 watt stage

Use the ON7YD single-IRF610 **class-C mechanism** as the reference, replacing its crystal oscillator and unsafe direct key/drive behavior. Its published complete transmitter measurements support plausibility; they do not validate this derivative. Its combined filter/match is not a ready-made separate 50 Ω filter plus long-wire tuner. Preserve that distinction when comparing power and efficiency.

```text
protected raw 2S -> boost, about 15–16 V -> true supply isolation
               -> shaped high-side CW rail -> RF drain choke -> IRF610 drain

quiet gated 3.3 V -> local Si5351 -> hardware RF gate -> 12 V gate driver
                -> AC coupling / negative clamp / gate-stop -> IRF610 gate
IRF610 source -> short RF ground and calibrated low-side current sense
drain -> rated DC block -> drain-to-50-ohm matching cell -> output filter -> normal RF port
      -> separate longer-wire matching network -> vertical wire / symmetric radials
```

| Connection / component | Starting proposal | Review and measurement requirement |
| --- | --- | --- |
| Local source | Si5351A with its own reference, switched source supply and powered-off bus isolation | Program while PA muted; verify actual frequency/settling/spurs. No 3.5 MHz carried from the controller. |
| Gate driver | **TC4427A industrial-temperature suffix** comparison against the M1 IRS4427 candidate; approximately 12 V gated rail | Microchip confirms in-production family and TTL input threshold; measure actual 3.6 MHz drive current/temperature/edges. Commercial 0–70°C suffix is not selected for the provisional outdoor range. |
| IRF610 gate | 10 nF AC coupling starting value, 10–33 Ω gate-stop, 2.2 kΩ gate-to-source bleed, negative Schottky clamp and positive gate-voltage clamp | Original proposal, not ON7YD copied circuitry. Clamp ratings/loading/driver reverse-current behavior require review. Target usable positive gate swing without exceeding ±20 V device limit. |
| IRF610 device | Stock-listed IRF610PBF-BE3, same candidate family as M1 | Verify exact suffix datasheet and PCNs. Measure drain overshoot and load sensitivity; do not infer ruggedness from its 200 V headline alone. |
| Drain choke | About 5 µH starting reference, initially provision ≥2 A peak for evaluation | Original reference's 1 A allowance is not transferred to this new match. Actual saturation, Q, SRF, heating and current-limit response must be measured. Choke current is not pack current. |
| CW shaping | Filtered LEVEL sets bounded rail; KEY controls a smooth 3–8 ms raised envelope through a high-side shaping device | Use a device with documented linear SOA for the edge interval, or characterize bounded converter/setpoint shaping. The existing isolation FET is not automatically a qualified linear pass device. |
| Drain feed/filter DC block | RF-rated capacitor with measured reactance and ≥100 V initial rating; actual drain stress can require more | Source-side output voltage differs from drain voltage; match/filter must be measured together. |
| Current/temperature/rail sensing | Analog comparator trips feeding persistent fault latch; set by calibration and component stress | Include mismatch, gate loss/stuck drive, boost overvoltage and startup. Exact thresholds depend on measured normal peaks/SOA. |
| Test points | Source fundamental, driver output, gate, drain, shaped rail, shunt, post-filter 50 Ω plane | RF-safe probing and de-embedding are required; a long probe ground can invent ringing. |

The AC-coupled gate with clamp/bleed is intended to remove sustained DC gate drive if the clock sticks. Its approximate 10 nF×2.2 kΩ time constant is **22 µs**; this is a calculation, not proven protection. Loss-of-drive qualification and analog current cutoff remain necessary. A static clock transition can still deposit charge before it decays. Source/PA muting must not rely on that RC alone.

At 3.6 MHz, even an illustrative 8.2 nC gate-charge input gives `Qg×Vdrive×f≈0.35 W` at 12 V, before driver/source losses. Actual gate charge at the chosen waveform, ringing and temperature are unknown; the nominal 1.5 A driver rating does not establish its continuous-frequency power. Allow **1.00 W active HF Classic overhead and 0.65 W Sprint overhead**, including gate/source and the additional shaping pass-device base/helper losses. Modeled HF Classic 4P endurance is about **27.7 h**, while conservatively budgeted Sprint requires 2P; 1P remains measurement-dependent. See the [preparation power budget](M2_POWER_BUDGET.md); these are not measured passes.

ON7YD reports 4.8 W at 15 V. Square-law interpolation alone suggested 15.3 V for 5 W, but the new gate waveform and output loss invalidate treating that as a guaranteed setpoint. Begin with low current limits and lower rail, then characterize enough clean **post-filter 5 W** with stress margin. Sprint 0.3–1 W and Classic 1–5 W use calibrated rail/drive limits; changing ranges occurs inhibited. Do not claim 5 W from raw 2S. No adaptive retuning is allowed to radiate between channels.

**PA load transformation is essential.** For an illustrative sinusoidal drain swing equal to 15.5 V and 5 W connector output with 0.5 dB output loss, `Rdrain≈Vrail²/(2×Pbefore_filter)≈21.4 Ω`. An unmatched 50 Ω load would yield only about 2.4 W under that swing assumption. A starting low-pass L transform from roughly 21.4 Ω to 50 Ω at 3.55 MHz is about **1.11 µH series inductance and 1.04 nF shunt capacitance on the 50 Ω side**. These ideal resistive-load calculations do not include transistor capacitance or class-C conduction angle; jointly tune the drain match, DC block, choke and filter into loads. Keep the external antenna tuner separate. Add **€0.20–0.50 output-match material allowance** in the cost view, not an omitted connection.

Use a D45H11-class shaping pass device as an initial candidate requiring SOA qualification with helper/feedback; this is an **additional functional device** beyond the two isolation FETs. Track the unmodulated boost/setpoint between inhibited power-range changes to avoid dropping a fixed 16 V rail across the Sprint pass device. A plain boost cannot regulate below the charged pack, so preserve the downstream shaping/regulating element. Exact rail headroom, repetitive edge SOA and heat are measured gates.

Initial shaping connection: pass emitter at the isolated boost rail, collector at the drain-choke supply; base pullup and bounded NPN helper as in the VHF proposal. Power the HF LM2904B feedback amplifier from the gated quiet 12 V driver rail: a 3.09 V command is outside its full-temperature common-mode range on 5 V, and a 3.3 V supply is unsuitable. A rail divider near40.2 kΩ/10 kΩ gives a command about3.09 V for15.5 V PA supply. LEVEL sets the bounded command ceiling; KEY supplies the shaped transition and then mutes RF drive after the allowed fall. Do not charge a large downstream capacitor and rely on its discharge to define CW edges. The loop compensation and shaping time constant are separate from the gate-protection22 µs RC and require measurement. A high-rate digital PWM on a DC setpoint needs its own filtering; it must not become unqualified RF amplitude ripple.

## Output-filter proposal and actual simulation boundary

Two **original ideal passive models** were run in ngspice-42. They include matched 50 Ω source/load and exact lumped L/C values; they contain **no IRF610, clock, core losses, component parasitics, PCB or antenna model**. Netlist and actual simulated samples are [here](../analysis/hf_lpf_ideal.cir) and [here](../analysis/hf_lpf_ideal.csv). Reproduce with `python3 tools/m2_rf_analysis.py --simulate --write`.

| Ideal model | Transfer at 3.510 / 3.600 MHz | Transfer at 7.020 / 10.530 MHz | Disposition |
| --- | --- | --- | --- |
| Fifth-order Butterworth, 4.2 MHz | −0.67 / −0.84 dB | −22.33 / −39.92 dB | Weak second-harmonic rejection and unnecessary fundamental loss; **not the preferred final proposal**. |
| Seventh-order 0.1 dB Chebyshev, 4.1 MHz | About −0.06 / −0.09 dB | About −46.48 / −74.70 dB | Preferred passive-filter evaluation start, with one extra winding/capacitor group costed. |

Seventh-order **π ladder**: shunt C1≈917 pF; series L2≈2.762 µH; shunt C3≈1.628 nF; series L4≈3.054 µH; shunt C5≈1.628 nF; series L6≈2.762 µH; shunt C7≈917 pF. These are calculated targets, not selected stock values or winding recipes. Use C0G/NP0 RF capacitors with voltage margin and characterized windings; start with adjustment allowance rather than claiming these decimal values are build accuracy. Separate the windings physically to reduce bypass coupling. Real insertion loss and harmonic rejection require a VNA and powered spectral tests.

Filter attenuation alone is **not** transmitter harmonic suppression. Measure the actual source/PA harmonic levels and total post-filter emissions. An ideal 46 dB stopband cannot close the national mask or project −50 dBc target without source data. Retain provision for a second-harmonic trap or a different filter if needed; do not waive the mask to preserve the old two-core count. Allow **€0.80–1.20 incremental filter material**, unquoted, before winding/calibration labor.

## HF-L1: independent nominal 10 mW source

Foxoring has a **separate RF-generating buffer path**, low rail, current limit, filter and permanently populated pad. It shares only the local frequency reference/source with the watt chain. Neither normal PA drain nor watt-filter output has a routing switch, tee or electrical connection to the compact port.

```text
Si5351 output -> separate DC block / gated low buffer on bounded 3.3 V
             -> independent low-power LPF -> fixed pad + manual fine calibration
             -> defined 50-ohm 10 mW reference port -> compact cartridge

bounded low rail + current trip + RF level guard -> fault latch -> source hard mute
compact cartridge auxiliary identity/contact -> hardware NORMAL inhibit
```

Starting low-buffer experiment: a small complementary BJT emitter-follower pair or tuned single-BJT buffer, driven by the source at 3.5 MHz, with local rail/current restriction. Exact transistor, bias and matching depend on measured gain and efficiency; no unsupported 50 Ω power claim is made for a Si5351 pin. Use the external fixture to characterize this branch **without any watt-stage population**.

An original matched **4 dB π pad** has two shunt resistors about **221 Ω** and series resistance about **23.8 Ω** (`K=10^(4/20)`). Select actual values after loss/tolerance calibration. To obtain 10 mW after pad/filter requires ≥25.1 mW before the pad, plus measured filter loss. The proposed rail has a **3.6 V hardware ceiling and 20 mA current limit**: steady rail input ≤72 mW. **This excludes energy entering from the synthesizer drive or backfeed.** A 28.7 mW matched-pad output follows only for that rail-energy contribution at hypothetical 100% conversion; it is not a bound on the complete branch. Budget the measured maximum incoming drive power separately and provide an input resistor/pad and voltage clamp; include startup and bus/control backfeed. For total bounded incoming drive `Pdrive`, the ideal matched-load energy bound is `(72 mW + Pdrive) × 10^(−4/10)`. Arbitrary mismatches do not inherit that pad factor. The circuit-level guard allowance includes this input limiting support; values and a complete fault-energy bound remain open. These are protection bounds, **not the nominal 10 mW acceptance limit** and not PEP bounds for stored-energy transients. Local capacitors and cutoff transients require peak measurements.

Normal operation uses a fixed manual bias/pad calibration and a local RF-level comparator guarding a provisional ≤11 mW post-filter mark limit. Controller LEVEL cannot raise the Foxoring branch limit. Calibration uncertainty and the referee's reference/tolerance convention must be agreed; a guard which permits 28.7 mW as normal operation fails the nominal 10 mW requirement. RF fault/rail trips latch off. The design target is a tens-of-milliwatts fault ceiling even for a wrong-range command; establish the complete input-energy bound and independently measure it, including high-PA RF feedthrough.

Expected low-buffer DC demand is **unmeasured**. If pad/filter/buffer losses exceed the M1 Foxoring overhead, update the M2 0.350 W total allowance (M1 used 0.260 W) rather than inventing efficiency. Qualification ceiling for the modeled **3.4 Ah reference-cell** 1P 24 h profile is **0.661 W total mean battery power**, including optional LoRa when fitted. The [audited lower-cost 25R pack](FOXORING_COST_AUDIT.md), using 2.45 Ah conservatively, has a **0.476 W** ceiling instead; capacity/cold qualification remains mandatory. Preserve a small low-energy branch; do not create a watt PA plus 27 dB attenuator.

## A80-L: conventional wire match

The normal port feeds a separate adjustable L-network, longer upright wire and defined ground/radials. Example 8 m+6 m lengths remain examples; **Sprint grounding must be symmetric**. Include insulation, strain relief and coil/capacitor RF ratings in the installation cost.

Reviewable **calculation example only**: if the installed antenna measures `20−j300 Ω` at 3.55 MHz, a low-pass L match with source-side shunt capacitance and series antenna inductance gives approximately **14.55 µH** and **1.098 nF**. With assumed winding Q=100, the series coil loss is about 3.25 Ω; it is not lossless. At watt-level antenna current, the inductor/antenna reactive voltage can exceed **150 V RMS** in this example. Use appropriately rated parts and inspect tuning/mismatch stress. Actual impedance could be very different, so these values are not an ordering recipe.

Measure installed complex impedance, tuner loss, coil/capacitor voltage/current and radiation pattern in dry/wet sites and across 3.510–3.600 MHz. Tune independently from PA transistor matching. Source-side VSWR≤2:1 is a project target subject to PA characterization; low VSWR alone does not prove efficiency or competitive reach.

## A80-F: short-radiator cartridge

Use a **~30 cm vertical radiator**, reproducible compact counterpoise, separate loading/coupling coil and adjustable low-capacitance coupling. The compact return, battery/enclosure and nearby ground form part of the RF installation. A large Classic counterpoise is not silently attached to make the compact tests pass.

Starting experiment: source to an adjustable coil tap or small **2–20 pF coupling capacitor**, loading coil around **134–402 µH** depending on measured total 5–15 pF capacitance, and limited RF tuning capacitance at the high-impedance radiator node. These ranges derive from a short-antenna model; actual Q/SRF and stray capacitance can invalidate them. Keep a replaceable damping/coupling element to adjust reach at a **fixed calibrated 10 mW reference setting**. Do not require a perfect match if controlled coupling/loss is the validated field recipe.

For the illustrative 10 pF/Q50 model at 3.55 MHz, L≈201 µH, reactance≈4.48 kΩ and coil loss≈89.7 Ω. If this branch accepts 10 mW, reactive voltage is around **47 V RMS**. Specify RF-voltage margin and insulation despite the low connector power. A 1 pF parasitic change shifts resonance by roughly 4.7%; choose capacitor/clamp placement carefully. Put ordinary ESD clamps on the **low-impedance source side**, not blindly across the sensitive high-Q radiator node. Any high-node protection must have measured capacitance/leakage and be included in tuning.

The complete cartridge includes radiator, compact counterpoise, loading/coupling/tuning components, necessary damping/protection, incompatible mating connector, independent identity/contact, insulation and mechanical restraint. Existing **€8.38 material estimate** is retained as an estimate and must be revised if stress/Q or construction demands larger parts. Long-wire accessory **€10.25** is separate. Installation recipes, soil/wetness, hands and 1P–4P pack geometry must be logged for repeatability.

## Hardware fail-off and interlocks

Retain the [nine-function interface](M1_SYSTEM_ARCHITECTURE.md), separate protected raw-power pair, POR, application-health lease, persistent fault latch, analog trips and direct ARM inhibit. Each RF board is testable with a host fixture. Source shutdown includes bus isolation to prevent pullup backpower.

| Hardware state | Watt path | Foxoring path |
| --- | --- | --- |
| POR, missing lease, fault or ARM low; controller holds ARM low for invalid time/profile | Source/drive and actual supply disconnected | Source/low rail muted; discharge characterized |
| Valid Classic/Sprint + normal installation | Bounded normal setpoint and shaped keying | Muted |
| Compact cartridge present / Foxoring selected | **Hardware blocked**, even for a normal-power command | Fixed low calibration, bounded rail and RF guard |
| Conflicting requests, bad identity or retune | Both paths inhibited | Both paths inhibited |

An identity-wire fault cannot create a watt RF route to the compact network because none exists. Physical keying and the auxiliary inhibit provide additional protection; do not treat either as proof of RF isolation. Test normal PA into a dummy load with the cartridge attached, control/ID shorts, stuck drive, open return and maximum boost. Candidate HF leakage budget is ≤0.1 mW into the compact port, corresponding to **≥47 dB isolation from 5 W**; measured total branch ceiling and field behavior govern acceptance.

**Go/no-go:** HF-W1 must meet 1–5 W Classic/0.3–1 W Sprint, spectral/keying/efficiency/thermal/mismatch limits and hardware shutdown. HF-L1 plus A80-F must meet nominal conducted power, separate low-source safety and **mapped-point/30 m audible, 250 m not-audible field tests**. Neither a simulated filter nor a dummy-load 10 mW result substitutes for the installed compact field qualification. Complete system layout remains on hold pending these measured gates.
