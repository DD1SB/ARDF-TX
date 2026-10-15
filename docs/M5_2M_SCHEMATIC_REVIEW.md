# M5A RF2M electrical review

Date: **2026-10-15**. **M5A-R0 — EVALUATION SCHEMATIC, NOT RELEASED.** The [native project](../hardware/2m/RF2M.kicad_pro), [editable schematic](../hardware/2m/RF2M.kicad_sch), [PDF](../hardware/2m/review/M5A-R0/RF2M.pdf), [XML netlist](../hardware/2m/review/M5A-R0/RF2M.net.xml) and [electrical manifest](../hardware/2m/RF2M.electrical.json) are actual generated KiCad artifacts. No PCB exists. The common controller and all80m design/artifact bytes are preserved; the335-file starting hash inventory verifies that boundary.

## Circuit organization and reference conditions

The16 functional/continuation sheets separate source/interface, fail-off, pack/converter isolation, driver rail, AM, normal RF, training RF, analog trips and external test-power declarations. The two normal-RF sheets have physically connected signal chains, not schematic-free block diagrams. Other sheets use explicit pin-level named nets; there are no hidden power pins. Every component has a value, candidate MPN or OPEN position, footprint or explicitly empty/OPEN footprint, and population field. Default CAD population is full2S; alternative populations use the exported variant BOM and explicit resistor substitutions.

Si5351 uses a25 MHz/10 pF candidate crystal. At144–148 MHz a divide-by6 plan puts the VCO at864–888 MHz; fractional PLL resolution is more than adequate. The crystal's listed10 ppm initial/10 ppm temperature figures do not alone qualify total drift, pulling, aging or phase noise. Unpowered source pins are isolated through U102; a single switched VCLK supplies core and outputs. CLK1 is unused; enable only the selected normal/training clock. An explicit immediate input DC block follows the normal driver pad so the pad cannot ground a MMIC input's bias node.

RF input filtering uses a seven-element50 Ω low-pass ladder. The normal output has a calculated nine-element ladder, with two93 nH series arms built from82+11 nH obtainable HP parts. Normal RF filter capacitors require appropriate C0G voltage/Q ratings; exact100 V output-capacitor procurement remains OPEN. The current pure-passive model assumes component Q, excludes PCB/pad/package parasitics, and is not a spur measurement. At144.9 MHz the chosen normal filter is about−0.55 dB for assumedQ80; the0.75 dB budget is conditional. Q40 and148 MHz cases are separately recorded. Output-capacitor RF currents, mismatch voltages and inductor temperature must be checked from actual waveforms.

Q501 is the formed-lead ST PD55008-E. Its symbol uses manufacturer functional terminals G,D,S deliberately: the accessible Figure1 did not provide a trustworthy numbered ten-pad mapping. **No invented PowerSO10RF footprint is supplied.** Source flange/landing, orientation and thermal implementation must be resolved from the actual package drawing/AN1294 before layout. The small-signal-based matching and the RF gain floor are evaluated in the PA selection document; neither is a validated144 MHz large-signal network.

Training uses a3.3 V-only, separately inhibited clock buffer and MMBTH10 current-servo RF stage. A100 Ω collector feed, attenuation, DC blocking, its own filter/pad and separate MCX candidate connector limit available energy. There is no normal-output switch, transformer or conductor feeding that port. Nominal1 µW/optional1–10 µW carrier calibration is provisional. Normal power parts are omitted in TRAIN_ONLY; U207 and its decoupling are omitted too, with an explicitly exclusive R519 health strap. The watchdog, captured arm context, mute/SCL clear, slot gating and output-clock inhibition remain fitted.

## Independent protection, with a reason for every block

| Block | Role and failure addressed | Cost/complexity disposition |
| --- | --- | --- |
| TPS3431 | Independent missing-application-progress shutdown,170–230 ms | Retained; S3 firmware watchdog is not an RF hardware shutdown. No RC watchdog/first-edge latch duplication. |
| TLV803E | Clears CMOS context before an invalid3.3 V brownout region | Retained; watchdog minimum supply threshold alone is too low. |
| HC174 and compact gate decode | Captured valid ARM/path/profile; clear on faults; no live path transfer or automatic rearm | One context register, not a local contest controller. Six HC gate/register ICs plus one small dual LVC final gate implement the documented equations. |
| ARM RC/Schmitt | Separates raw edge capture from RF permission/rail settling; raw ARM still removes RF immediately | Retained; not repeated quiet/key-tail latches. Actual thresholds/delays remain physical gates. |
| U209 direct common-inhibit gate | Prevents register-output reset skew from becoming the only shutdown path | Retained small dual gate; propagation/supply behavior still requires measurement. |
| I²C SCL clear | Makes configuration activity destroy ARM context | Uses the existing decoder; no second bus-quiet monostable. |
| Q309/Q305 | Reverse connection and wrong-pack input isolation before boost VIN | Separate from output isolation; an output switch cannot protect an overvolted boost input. |
| Q302/Q304 | Hard converter-output isolation and physical MMIC enable | Separate from converter EN; stored energy and a stuck converter need independent treatment. Low-cost repeated PFET/NPN parts, not a hot-swap subsystem. |
| Two LM339B, INA180, TL431 | Pack UV/OV; converter OV; driver OV; modulated-rail OV; current; sensor-hot/open/short window | Each channel has a named failure. BMS protects cells, not these RF/driver limits. No local ADC, DAC, RF detector or precision power servo; converter readiness uses the controller ADC. |
| U304 fault-qualified input/rail switches | Converts pack/hard-fault conditions into defined low NPN-drive levels instead of uncertain diode-clamped base voltage | One dual gate replaces two clamp diodes; 4.7 kΩ gate pull-ups and 1 kΩ sink resistors reduce withdrawal delay. Actual timing is OPEN. |
| Training source inhibit/base clamp/pad | Si5351 clock alone cannot intentionally energize the low port; no watt PA dependency | Retained. Layout coupling and unpowered-device leakage remain measurements. |
| U207 normal-health OR | Qualifies normal supply faults after captured context has settled | DNP in TRAIN_ONLY with exclusive R519 strap. Retaining it in a PA-free assembly is unjustified. |
| Test pads | External measurement access, not permanent instruments | Board features, excluded from purchased-part/IC counts. |

The locally fitted safety and analog protection material is a small fraction of the cost overrun; its removal cannot deliver a€36 module. Optional permanent RF detectors, ADCs, DACs, extra MCU/RTC/EEPROM, display and local scheduling have been excluded. The full circuit is still more populated than the original optimistic VHF basket; its actual count and cost are disclosed, not described as a tiny bare PA.

## Confirmed issues corrected during this draft

- TPS22919 physical pins corrected to1IN,2GND,3ON,4NC,5QOD,6OUT. A similar-looking switch pinout would have been wrong.
- ST BD139 and D45H11 use1B,2C,3E, including the live collector tab. Generic EBC symbols were remapped explicitly.
- TVS and gate-clamp cathodes face the positive rail/source, not ground.
- Pack faults and hard rail/current/thermal faults are distinct open-drain buses. Converter readiness is read through PA_RAIL_ADC after ARM capture and before SLOT, so an initially empty output capacitor cannot create a hardware startup deadlock. The freed comparator now detects VPA overvoltage at about 12.63 V, including a shorted series pass device.
- Immediate driver input DC blocking added after the grounded pad; duplicate source termination removed.
- Gate-stopper/input loss is included in the drive calculation, and output matching includes a stated nominal Coss assumption.
- Bias ceiling permits a device requiring up to5 V quiescent gate bias; no unsupported3.3 V bias guarantee.
- Normal pass/command clamps and training base/command clamps address stored command at enable.
- The loaded training-inhibit node uses a 1 kΩ pull-up, giving a conservative DC high above 2.84 V at minimum logic supply, exceeding the LVC buffer’s 2.0 V VIH. This is a DC calculation, not a turn-off timing measurement. All high-side FETs exposed to elevated voltage have explicit gate-voltage treatment. Driver filtering and a hard trip remain conditional on measured isolation time.

## Verification and limits

[Verification JSON](../hardware/2m/review/M5A-R0/verification.json) records actual manifest/XML parity,4096 settled logic combinations,36 state scenarios,8 rejected mutations and the frozen-file check. [Pinout audit](../hardware/2m/review/M5A-R0/pinout-audit.json) compares independent manufacturer-specific assertions with the exported netlist. ERC was actually run with KiCad10.0.6: zero errors and two documented OPEN-connector footprint warnings (J301/J701); no per-item exclusions were added. Empty footprints are intentional OPEN items and do not become qualified because ERC is clean.

The logic evaluator first settles gates and then applies asynchronous clear; it does not turn its Python evaluation order into fictional propagation glitches. It proves the stated ideal discrete model only. Actual HC174 setup/hold, clear recovery/removal, Schmitt thresholds, analog output levels, diode fault-bus VOL, supply collapse and driver turn-off remain unverified. Watchdog release provides a grace period, not evidence of a genuine first application heartbeat; arming still requires a raw edge after reset with valid context.

## Blocking and experimental items

1. **Package closure before layout:** PowerSO10RF formed lead, DF782/PL523, RNW13-terminal landing, selected power magnetics, fuse/shunt pulse ratings, connector mating/holes and crystal package/load/ordering suffix. Standard footprint names are candidates, not qualified vendor geometry.
2. **Stability/matching:** manufacturer K<1 near band; gate stopper and pads do not prove unconditional stability. Verify biased input/output behavior and load-pull with bounded supplies before committing fixed matching. Output Coss and load impedance vary over the envelope.
3. **AM:** physical servo loop, sine reconstruction, RF-envelope transfer,70–80% depth, distortion, carrier/PEP and AM-to-PM. A voltage sine and an ideal behavioral result cannot close these gates.
4. **SOA/thermal:** hot ST pass/helper trajectories, current-trip energy, actual heat-sink interface and detached-contact risk. One thermistor must represent the hottest relevant surface, not ambient air.
5. **Protection:** raw transients/reverse/wrong pack, buck/boost failures, driver voltage≤9.5 V under the defined fault, ≤20 µs disconnect assumption and input/fault-bus tolerances.
6. **Controller:** proposed pin budget, dedicated I²C, country/profile ARM validation, deterministic PWM/slot timing and no backpower through independently driven GPIO. These are future controller integration obligations, not completed firmware.
7. **RF silence/isolation:** source running during configuration, PA unpowered, stuck GPIO, main-output fault, near-field coupling, LoRa TX and port mating. There is no existing PCB or physical isolation result.

These OPEN items are visible design conditions, not omitted supplies or an invented validated matching value. The next review should close package/pulse component choices and authorize a staged RF evaluation fixture. This schematic does not authorize layout or procurement by itself.

Si5351's6×carrier VCO lies around867–869.4 MHz in the championship range, overlapping potential868 MHz LoRa operation; the PA's sixth harmonic is another coupling source. Output-filter arithmetic does not remove internal source/harness radiation. Optional Silicontra coexistence therefore needs a measured blocking/spur test and possibly shielding or a reviewed channel/listening policy. LoRa absence remains supported; no concurrent-RF immunity is claimed.

## ERC coverage and retained warnings

Footprint-filter checking is explicitly enabled. It exposed DIP-only filter metadata inherited with generic logic drawings; those filters now describe the selected HC SOIC packages without changing their pin numbers. The two remaining warnings are the deliberately unresolved J301 battery and J701 MCX footprints. They are purchase/layout blockers, not waived geometry checks. Other critical empty footprints are additionally listed by the machine-readable BOM and pin audit; ERC does not discover a physical pad map that has not been specified.

KiCad defaults still ignore `single_global_label`, `four_way_junction` and `simulation_model_issue`. Single global names are used for explicit named terminal stubs; actual pin/net membership is checked independently against the exported XML. Deliberate bus junctions are drawn explicitly; a four-way crossing style warning is not a connectivity test. This schematic has no embedded SPICE models; the separately executed behavioral deck is not a vendor model. These limitations and the absence of PCB DRC remain explicit. A clean electrical-net check cannot qualify footprints, parasitics, waveforms or analog fault response.


Final comparator margin correction: LM339B's hot common-mode limit is VCC−2 V, or1.135 V at the specified3.135 V logic minimum. R802=620 Ω/R803=470 Ω now produces a loaded approximately1.03 V reference; R828=10 kΩ/R829=7.5 kΩ preserves the approximately1.2 A trip. The original approximately1.2 V reference would not have enough hot/low-supply margin. The DC check evaluates the fitted divider, while threshold offsets/tolerances, brownout and propagation still need measurement. Pack sensing R805 now starts at VIN_PROT, ahead of Q305 but behind Q309 reverse protection; it cannot intentionally apply a negative raw-pack voltage to a comparator. Quoted UV/OV thresholds refer to VIN_PROT, with the reverse-FET/wiring drop added at the external battery. No new comparator or MCU was introduced.


## Earlier-work regression checks actually run

The read-only baseline checks also passed: `tools/m3a_r1_logic.py` (256 physical-pin cases,31 scenarios,16 RC corners and watchdog-polarity mutations), `tools/m3a_r1_driver_fault.py` (conditional model and rejected slow/ESR cases), `tools/m2_checks.py`, `tools/m1_analysis.py --check` (109 Markdown files,695 local links,73 traced requirements), and `tools/m1_costs.py --check` (117 BOM lines/68 catalog entries). They were invoked with `/usr/bin/python3`. None is a new hardware test. The final preservation check confirms335 earlier RF80/ADR/README files unchanged, including the pre-existing M4A working-tree artifacts.
