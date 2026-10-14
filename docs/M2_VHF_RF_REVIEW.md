# 144 MHz RF-chain and AM-modulator review

Date: **2026-10-13**. **Design calculations and circuit proposals; no measured ARDF-TX performance.** M1 is conditionally accepted as architecture. This review does not release a layout or ordering BOM. Manufacturer conditions and access limits are in [M2 sources](M2_SOURCES.md); reproducible calculations are in [RF calculations](M2_RF_CALCULATIONS.json) and [analysis helper](../tools/m2_rf_analysis.py).

## Findings

The **MMIC-driver architecture remains preferred**. GVA-84+ is the first evaluation candidate, but sufficient drive with compression margin has **not** been established. With the previous 15–17 dB intrinsic PA-gain assumptions, a 3 dB driver margin fails the conservative budget below. Matching may improve available gain, but the manufacturer's near-band small-signal data also indicates conditional stability. Neither its 500 MHz gain rating nor small-signal maximum gain closes this issue.

A bare BD140 is **no-go** for the calculated continuous thermal duty. A heat-sunk **D45H11 with a separate base-current driver** is the proposed inexpensive alternative; TIP42C is a cheaper thermal comparator. Exact-vendor DC SOA, loop stability and heat-sink performance remain qualification gates. Discontinued BFP650 is excluded from current selection by the user's review, with its old comparison retained as historical evidence.

## Reference planes and drive budget

Maintain the conservative M1 convention: maximum **1 W carrier ERP**, net antenna/feed gain −1 dBd, sinusoidal m=0.80, and 1 dB clean PA capability reserve. The referee's ERP convention remains open. These calculations do not redefine a connector watt as ERP.

| Plane / quantity | Calculated value | Boundary |
| --- | ---: | --- |
| Normal RF connector carrier | 1.259 W / 31.00 dBm | Includes the assumed antenna/feed relationship. |
| Connector mean during tone mark | 1.662 W | Carrier plus both intended AM sidebands. |
| Connector PEP | 4.079 W / 36.11 dBm | RF-cycle power at envelope crest. |
| Required clean connector capability | 5.135 W / 37.11 dBm | Additional 1 dB reserve; not a higher permitted ERP setting. |
| PA output before filter | 5.762 W clean capability | Illustrative **0.5 dB output-filter loss**, unmeasured. |
| MMIC output to matched PA input | Additional **0.5 dB coupling/matching allowance** | Unmeasured; includes insertion loss, not an assumption of perfect device matching. |

For this table, `GPA` is intrinsic large-signal power gain between device reference planes. Required MMIC output is `5.135 × 10^((Lout + Lin − GPA)/10)` W. Measure actual losses; do not count them twice when measuring gain through the complete PA coupon.

The manufacturer's typical GVA data at 5 V/25°C reports 100/200 MHz compression near 20.7 dBm and gain near 24 dB. Use **20.73 dBm as a comparison input**, not a guaranteed 144 MHz minimum. A 3 dB output backoff permits about **59.3 mW** before considering lot/temperature uncertainty.

| Assumed intrinsic PA gain | Required MMIC CW output, including reserve/losses | Margin below typical 20.73 dBm P1dB | 3 dB margin? |
| ---: | ---: | ---: | --- |
| 15 dB | 204.4 mW / 23.11 dBm | −2.38 dB | No |
| 17 dB | 129.0 mW / 21.11 dBm | −0.38 dB | No |
| 20 dB | 64.6 mW / 18.11 dBm | 2.62 dB | No |
| 21 dB | 51.4 mW / 17.11 dBm | 3.62 dB | Conditional numerical fit |
| 23 dB | 32.4 mW / 15.11 dBm | 5.62 dB | Conditional numerical fit |

The required intrinsic gain is about **20.38 dB** under these assumptions, or **19.88 dB measured PA-coupon gain including its output filter**, with 0.5 dB additional MMIC coupling loss. These are gate thresholds derived from a typical driver input. Replace them with the **lowest measured driver P1dB** over frequency, rail, temperature and samples, and require actual gain compression ≤0.2 dB at the reserved drive point. Backoff alone does not prove that limit.

The driver carries **constant CW drive** in a drain-modulated PA. It does not itself deliver the normal port's AM PEP. Nevertheless, its fixed drive must support the PA at maximum envelope voltage, including the reserve above. Budgeting drive from the carrier-center output alone can underestimate it by `(1+m)^2`.

Source chain proposal:

```text
local Si5351 -> DC block / fundamental filter -> adjustable source pad
            -> GVA-84+ on gated quiet 5 V -> coupling / optional small stability pad
            -> replaceable 144 MHz gate match -> PD55008TR-E
            -> replaceable drain match -> output LPF -> normal connector

separate source branch -> bounded low-level sine-AM buffer -> permanent pad
                      -> its own filter -> mechanically distinct training connector
```

Si5351 CMOS drive settings are not calibrated 50 Ω power settings. The approximately −7 dBm source needed for a 17 dBm MMIC output with 24 dB gain is a **calculation**, not measured source power. Provide pad range and test source loading, fundamental level, harmonics and close-in spurs at every selectable channel. Output filtering cannot repair close-in clock spurs. ADF4002/discrete VCO remains the fallback if the local Si5351 fails; no unreviewed band restriction is substituted for full required tuning capability.

## PD55008 matching, gain and drain modulation

ST's 8 W / 15 dB minimum, 17 dB typical gain characterization is at **500 MHz, 12.5 V, 150 mA bias**. It does not establish large-signal 144 MHz gain at a 1.3–12 V modulated drain. The application circuit's 500 MHz transmission lines and substrate cannot be copied as the 144 MHz match.

Useful near-band evidence exists in **Table 10, formed-lead PD55008-E**, at 150 MHz/12.5 V/150 mA. From that rounded small-signal row, our calculations give:

- 50 Ω-terminated input about **5.60 − j7.82 Ω** and output about **9.03 − j9.85 Ω**. These are small-signal port impedances, **not large-signal optimum source/load impedances**.
- Unmatched S21 about **14.30 dB**, `|Δ|≈0.402`, and **K≈0.063**, indicating conditional stability for this row.
- Maximum stable-gain comparison about **22.10 dB**. This is neither a realizable guaranteed gain nor a stable conjugate-match recipe.

Use short, grounded RF evaluation coupons with replaceable L/π matching cells, gate damping and bias decoupling. Start with low drive and an RF generator; characterize 144–146 MHz before increasing power. Determine stable matching and drive experimentally over **drain voltages corresponding to trough, center and crest**, gate-bias settings, normal power range, hot/cold, source/load mismatch and complete input/output filters. Matching only at 12.5 V misses voltage-dependent output capacitance, gain, feedthrough at the trough and AM-to-PM distortion. Do not interpolate the 480 MHz large-signal impedance table down to 144 MHz. Other tables in this mixed-device datasheet have different device headings.

Keep independent normal PA source/drive shutdown and upstream supply isolation. Gate-bias enable must also default off. A drain-voltage regulator is not the RF safety disconnect. Check broadband parasitic oscillation with the intended source, dummy load and representative mismatches; a good 144 MHz output reading alone cannot establish stability.

## Boost-rail compatibility correction

The baseline **TPS61088RHLR is rejected for the proposed 13.5 V rail**: TI specifies 12.6 V maximum output and nominal 13.2 V overvoltage protection. Propose **TPS611781RNWR**, the already cataloged HF 20 V forced-PWM boost candidate, with a separately reviewed 13.5 V feedback/current-limit network and true downstream isolation. This preserves headroom without exceeding the converter specification. Its switch rating is not output current; verify switch/inductor peaks, loop/load transients, heat, RF ripple and actual efficiency. The provisional 88% efficiency stays an assumption. Retaining TPS61088 would require a lower crest/dropout design whose PA gain/PEP and modulator transfer are not established; it is not silently substituted.

The cost view replaces the exact converter MPN, pools identical HF/VHF TPS611781 purchases and retains support allowances subject to a fresh inductor/capacitor/isolation basket. Exact footprint and compensation remain open; this is not a drop-in replacement.

## AM modulator: full-envelope calculation

Proposed maximum-power bench envelope: `Vd = V0(1+m sin θ)`, **V0=6.667 V**, m=0.8, crest 12 V and trough 1.333 V. Start with **13.5 V upstream rail**; the 1.5 V difference is a provisional dropout allowance, not a measured transfer guarantee. Output-filter loss is 0.5 dB. Model the RF-conversion component with **45% dynamic efficiency**, plus a separate **0 or 150 mA bias allowance**. Neither is a measurement. The separate bias must not be added again if efficiency is later measured using total drain power.

With `k = Pc_before_filter/(ηdynamic V0²)`, use `Iload = k Vd + Iq` and `Ppass=(Vboost−Vd) Ipass`. Include `Cout dVd/dt` in pass-current demand. The proposed default is **100 nF total modulated-node capacitance**; bulk storage is upstream of the modulator. These are RF-cycle averaged load calculations, not transistor/SPICE or measured-envelope results.

| Case | Calculated pass mean / peak dissipation | Peak pass current | Implication |
| --- | ---: | ---: | --- |
| 1 W ERP, 80% tone, no extra bias | 2.21 / 3.24 W | 0.85 A | Already exceeds BD140 free-air thermal capability. |
| 1 W ERP, 80% tone, 150 mA allowance | 3.24 / 4.33 W | 1.00 A | Heat sink and exact DC SOA required. |
| 1 W ERP, **carrier without tone**, same bias | **4.24 / 4.24 W** | 0.62 A | Tone gaps are hotter for the pass device in this model. |
| Same no-tone case, dynamic efficiency 35% | **5.16 / 5.16 W** | 0.76 A | Thermal design stress case; not an actual PA efficiency result. |
| 0.25 W ERP, crest 6 V, fixed 13.5 V boost | 3.67 / 4.32 W | 0.57 A | Reduced RF setting does not guarantee a cool modulator. |
| Same quarter-power envelope, boost lowered to 9 V | 1.93 / 2.19 W | 0.57 A | Consider boost tracking between inhibited configuration changes. |

The full-power tone envelope visits approximately `(VCE, IC)` = **(12.17 V, 0.244 A)** at trough, **(6.83 V, 0.621 A)** around center, and **(1.50 V, 0.998 A)** at crest. Intermediate phases produce peak dissipation; the four endpoint/center samples are not the complete SOA curve. The script evaluates 7,200 phases per case; four phase samples and the peak-dissipation point are retained in the JSON, not the full sampled curve. Add startup, short-circuit and mismatch current separately.

BD140 has 10°C/W junction-to-case and 100°C/W junction-to-ambient thermal resistance, with 1.25 W free-air dissipation at 25°C. With a provisional **125°C junction target at 50°C ambient**, the 5.16 W stress case requires total thermal resistance ≤**14.53°C/W**. BD140 leaves only **4.53°C/W for interface plus sink**, before uncertainty; a bare device is definitively unsuitable. Its 12.5 W rating requires case held at 25°C. No 20% slot-duty discount qualifies a continuous beacon or eliminates heating during a long active slot.

The BD140 datasheet supplies an SOA graph, but numeric DC coordinates were **not reliably digitized** through the available image/download access. Therefore no quantitative SOA pass is claimed. The calculated trajectory must stay below the **exact-vendor, hot-case DC envelope** with a project margin of ≥2× current at the same VCE. Single nonrepetitive millisecond pulse curves do not qualify continuous 800 Hz modulation. A qualified current limit and measured cutoff must constrain fault trajectories too.

### Proposed alternative and circuit contract

Evaluate **ST D45H11 (TO-220)** first: active manufacturer status, published SOA graph and **2.5°C/W junction-to-case**. This leaves about **12.0°C/W interface plus sink** in the stress model; start with a **≤10°C/W dedicated sink** including installation allowance. A shared sink must be sized from combined PA, pass-device and driver heat; 10°C/W for the shared total would be insufficient in the stress example. Do not use different manufacturers' SOA curves interchangeably. Digitization/vendor evidence and measured hot operation remain open.

Original circuit proposal: D45H11 emitter to the independently isolated boost rail, collector to the modulated PA rail, base-to-emitter pullup; BD139-class NPN sinks bounded base current. An LM2904B error amplifier, on a gated quiet 5 V rail rather than 3.3 V, compares divided drain voltage to a filtered carrier-plus-keyed-sine command. Negative feedback polarity must raise PNP conduction when output falls. Reserve compensation and base-stop resistors; verify capacitive-load stability and RF rectification. Add analog overvoltage/current trips, rail readback and a discharge path. Allocate base drive up to **70 mA provisionally** rather than assuming favorable typical hFE. The helper can dissipate approaching 0.9 W at worst continuous base drive, so a tiny unqualified SOT-23 helper is insufficient. Measure helper dissipation and temperature too.

Reviewable starting connections: pass emitter at13.5 V, collector at `VPA`; 4.7 kΩ base-to-emitter pullup, 100 Ω base-stop to the helper collector; helper emitter through8.2 Ω to ground and base through1 kΩ from the error amplifier. A separate small NPN senses the helper-emitter resistor and diverts base command near0.6 V, giving an approximate73 mA base-drive ceiling. This is a temperature-dependent calculation; characterize the actual limit and main PA current trip. Use a drain divider near40.2 kΩ/10 kΩ (gain5.02): full-power carrier command≈1.328 V with0.265–2.39 V envelope at80% modulation. Connect command to the noninverting input and divided rail to the inverting input. Floating command, saturation or fault must not bypass the independent source/supply gates. The 2.39 V maximum divided rail/command stays below the TI full-temperature 5 V-supply common-mode ceiling of 3 V; control-rail tolerance and output/base-drive headroom still need verification. Compensation values remain open until the load-coupon loop measurement; these starting resistors do not constitute a stable released schematic.

TIP42C offers 1.92°C/W junction-to-case and lower observed silicon cost, but the inspected ST Rev.3 datasheet does not provide an explicit DC SOA plot. It is a comparator pending exact-vendor DC SOA evidence, not a thermal-rating-only approved substitute. A switching MOSFET is not automatically suitable for linear service. A switch-mode envelope supply or low-level AM plus linear RF PA remains a more complex fallback if simple series modulation fails efficiency or envelope gates.

Large PA-output bulk capacitors can demand sinking current and flatten the falling envelope. The quarter-power/no-extra-bias **22 µF** calculation demands negative pass current during part of a cycle: a PNP-only regulator cannot implement that ideal waveform. Keep bulk upstream; evaluate 100 nF plus essential RF bypass, and add controlled sinking only if measured load demands it. Fast hardware source/PA mute precedes discharge during retune or fault.

## Current-production alternatives and cost consequences

| Candidate | Evidence / trade-off | Disposition |
| --- | --- | --- |
| GVA-84+ | Existing €2.57 observation; adequate only if stable measured PA gain and losses satisfy the drive gate. | Preferred first MMIC coupon, **no adequacy claim**. |
| PHA-1+ | Current manufacturer catalog lists higher compression than GVA; observed Mouser **€2.82** flat for 6/10/20, MOQ1, indexed stock 4,662. About **€0.25 silicon premium**, with lower gain and higher current. | Worth evaluating if GVA fails. Exact 144 MHz P1dB/gain and source-drive needs remain open; no invented ten-piece discount. |
| PHA-1H+ | Published nearby-frequency data provides another MMIC margin comparison; local price not captured. | Secondary comparator; no automatic substitution or quoted saving. |
| Onsemi MMBTH10L family | Manufacturer active-filter results; inexpensive small-signal discrete approach. Exact suffix stock/price and power gain not closed. | Useful training/prebuffer research; a complete high-drive replacement is unproven. Check package-specific PCNs. |
| BFP650 / BFP420 / BFR93A / NXP BFU590 | Relevant stock may remain, but manufacturer lifecycle findings are discontinued/EOL. | **Excluded from new selection**; no cost-based EOL exception. |

D45H11 selected quote is **€1.71/€1.08 at 1/10**, supplier code 511-D45H11, MOQ1; lower country-view quote conflicts are logged. It adds €0.816 silicon at ten versus the M1 BD140 input. Extra base-drive/thermal material is estimated separately in the [all-in view](M2_SYSTEM_COST.md). Performance-driven cost increases must be visible, not hidden in the old €31.80 board total.

## Energy implication and decision gate

The M1 70% series-modulator efficiency assumption is not a safe conclusion from this topology. This model gives approximately 65% without extra bias and 61% with the separate bias allowance. With 88% boost efficiency and **1.55 W active overhead** (the earlier 0.95 W plus 0.60 W for pass base-drive/helper/feedback), VHF Classic ranges **1.885–2.345 W mean battery load**: modeled 3P runtime **25.3–20.3 h**, and 4P **33.7–27.1 h**. Use **4P as the conservative evaluation allowance**, while preserving compatibility with all packs. A measured low-bias implementation may restore a 3P pass. Continuous maximum VHF beacon runtime is only about **5.7–7.1 h on 4P** under these assumptions. No current or endurance has been measured. The complete revised pack/profile table is in the [preparation power budget](M2_POWER_BUDGET.md).

The 35% dynamic-efficiency/bias stress case gives about **23.0 h on 4P without LoRa**, a model fail even before extra listening or a higher-current MMIC. It is a **no-go if measured total mean power exceeds 2.644 W** for the stated 4P usable-energy model. Its crest-current estimate, LoRa provision and 25% transient margin approach **4.5 A at 6 V**, including 1 W peak helper/base-drive provision: provision **≥5 A single-band** evaluation power/connector/BMS paths, with **≥7 A** only for supported simultaneous dual-TX. These replace the earlier 4 A single-band planning minimum; ratings, inrush and cutoff are not measured.

**No-go for complete VHF layout/procurement today.** Proceed with evaluation planning using the MMIC chain and heat-sunk pass-device proposal. A subsequent measured go requires adequate driver compression margin, stable all-channel PA matching/gain, actual 70–80% envelope and PEP, unwanted-emission compliance, thermal/SOA/fault limits and battery power within the selected-pack ceiling. Exact acceptance gates and minimum hardware are in [RF evaluation](M2_RF_EVALUATION.md).
