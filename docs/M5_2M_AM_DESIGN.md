# M5A genuine A2A modulation circuit

Date: **2026-10-15**. The [actual schematic](../hardware/2m/RF2M.kicad_sch) implements **continuous carrier only inside SLOT, with keyed sinusoidal audio modulation**. This is one of the two T2.8 alternatives. KEY changes tone presence; it does not FM-modulate the carrier or replace AM with on/off RF. SLOT, mute, watchdog and captured arming independently withdraw RF permission.

## Sine generation and reconstruction

ESP32-S3 supplies two 0–3.3 V PWM signals; an older ESP32 DAC is not assumed. A candidate uses the 80 MHz APB clock, 8-bit PWM at 312.5 kHz, and 32 sine samples per 800 Hz period (25.6 ksample/s). Future firmware must demonstrate coherent duty updates under LoRa/interrupt load; this milestone implements no firmware. Tone frequency is configurable, initially 600–1000 Hz around an 800 Hz default. No IARU tone-frequency rule is invented.

LEVEL_PWM reconstructs the carrier reference. AF_PWM reconstructs the same DC offset plus a sine. U401A/B are unity-gain Sallen-Key sections, each with two 10 kΩ resistors and two 4.7 nF capacitors: f0≈3386 Hz, Q=0.5, ideal amplitude0.947 at800 Hz and about−78.6 dB at the PWM carrier. Sampling images, quantization, board feedthrough and finite op-amp response still need measurement. Approximately 0.5 LSB at the full-power carrier command is a 0.5% level uncertainty, before calibration.

U402 selects LEVEL_DC on KEY=0 and AF_DC on KEY=1. At tone start, both commands must match; select at zero phase, then ramp tone amplitude over approximately3 ms. Ramp it to zero before deselection. For scheduled carrier start/stop, commands start at zero and ramp over approximately3–5 ms while SLOT brackets the allowed interval. Fault withdrawal is immediate and can have a different spectrum. A permanent tone or free-running PWM is not a valid application-progress heartbeat.

## Series modulator

U401C compares MOD_COMMAND with VPA/5.02. Q402 ST BD139 sinks the base current of Q401 ST D45H11 through100 Ω (R506, minimum1 W/pulse-qualified2010 candidate); Q401 emitter is VMOD, collector VPA, base PASS_BASE. The BD139 emitter has8.2 Ω and Q403 clamps base drive when its emitter reaches approximately0.6 V, giving an approximate73 mA helper-current ceiling. This is temperature dependent, not a precision PA current limit. The separate shunt/INA180/comparator trips excessive upstream current.

The pass base has a4.7 kΩ emitter pull-up. Q404 clamps the helper base, and Q405 clamps its command, when NORMAL_PERMIT is withdrawn; this reduces error-amplifier windup and prevents an intentionally stored full command at enable. Driver supply and PA gate bias are disabled independently. Output capacitance is approximately101 nF plus parasitics, with1 kΩ bleed; upstream bulk storage is kept before the pass transistor. Peak discharge current for a12 V-crest,800 Hz,80% envelope is under1 mA for this capacitance, unlike a large electrolytic on VPA.

C505=4.7 nF provides a starting local compensation path from MOD_DRIVE to VPA_FB. The executed [ngspice deck](../analysis/m5_2m/am_loop_behavioral.cir) uses a one-pole,1 MHz ideal op amp and a bounded transconductance plant. It gives a mean6.6665 V and approximately76.33% depth for a75% command, with negligible harmonic distortion in that deliberately ideal plant. **This is not a transistor macromodel, RF-AM result, loop-stability qualification or startup test.** It omits stored charge, changing beta, actual op-amp output behavior and voltage-dependent RF loading. Tune compensation only after bounded dummy-load step/loop tests.

## Voltage and RF envelope

For initial calculations only, full V0=6.667 V and m=0.80 give trough1.333 V/crest12.000 V; m=0.75 gives1.667/11.667 V. The reduced0.30 ERP example starts at V0=3.651 V and m=0.80 gives0.730/6.573 V. These voltages are calibration starting points, not a measured RF power law.

Supply modulation requires a suitable voltage-limited RF operating regime. An RF-linear PA with ample voltage headroom can produce too little AM when its supply is varied. Conversely, clipping, low-voltage capacitance changes and gate-bias variation can distort a voltage-limited final. The hardware investigation must establish a monotonic usable RF-envelope transfer, adequate crest capability and acceptable AM-to-PM conversion. Calibrated crest voltage may be below12 V. The 1 dB RF capability reserve is tested separately; it does not require operating the final RF waveform linearly through every part of its supply-modulation cycle.

Use `m=(Amax−Amin)/(Amax+Amin)` on RF **voltage** envelope, not on power readings. At the defined output plane the targets are70–80% depth, nominal75%, with an initial engineering envelope-THD target≤5%. Sidebands at±tone frequency should be symmetric within an initial1 dB gate. THD and symmetry gates are engineering criteria, not additional IARU wording. A sine-shaped supply alone is insufficient evidence of sine AM.

## Dissipation and SOA

The reproducible model in [calculations.json](../hardware/2m/review/M5A-R0/calculations.json) uses `I(V)=Iq+gV`, Iq=150 mA, with g set by42% full-carrier drain efficiency. Reduced-power efficiency is therefore lower, rather than held constant. At full power/m.8, estimated pass dissipation is about2.83 W; carrier-only/no-tone is a separate hotter case. Tables include32/42/52% full-carrier-efficiency assumptions and the entire envelope trajectory. A guessed efficiency is not measured current.

Use a pass-device heat sink no worse than approximately10°C/W, with an initially budgeted1°C/W insulated interface. The thermal arithmetic uses `Tj=Ta+Pavg(10+1+2.5)` at45°C ambient and a conservative125°C design gate. Neither this equation nor the nominal10 A/50 W rating proves hot DC/repetitive SOA. Review each `(VCE,Ic)` trajectory against the exact ST graph, derate for actual case temperature, and verify the bounded current-trip energy. Q402 can dissipate appreciable power while sinking base current and also needs a thermal review.

**D45H11 tab is collector/VPA; BD139 exposed collector is MOD_SINK; PD55008 source thermal contact is ground. These cannot share an uninsulated conductive heat sink.** Include insulating pads, sleeves and retention in cost and prototype mechanics. An electrically open/shorted thermistor is detected; a mechanically detached but electrically intact thermistor is not. Thermal attachment is an inspection and physical qualification gate.

## Low-power AM

U401D controls Q701 MMBTH10 emitter current using the same reconstructed command, scaled by27 kΩ/10 kΩ. RF excitation comes from a separately inhibited CLK2 buffer through attenuation and DC blocking. Its collector uses a100 Ω feed from3.3 V, its own LPF and fixed output pad. Calibration targets nominal1 µW carrier, with1–10 µW settings by fixed pad population. No normal PA, converter or VMOD connection is needed. RF gain versus emitter current, rectification, output depth, distortion, off leakage and exact maximum remain NOT_RUN. The uncalibrated branch is not called a qualified1 mW transmitter.

## Calibration caution: voltage depth is not RF depth

The initial voltage examples above are zero-knee budgeting points, not released duty settings. If RF amplitude is approximately proportional to`VPA−Vknee`, then`mRF=mV×V0/(V0−Vknee)`. An0.8 V knee makes a75% RF envelope require about66% voltage modulation at V0=6.667 V; at reduced voltage the correction is larger. The independent PWM DC and sine amplitude permit this simple calibration. Voltage-dependent matching/capacitance can require further measured correction; a non-monotonic transfer or excess distortion is a NO-GO. Applying80% voltage modulation without measuring the RF trough can overmodulate the transmitter.

| Full-carrier efficiency assumption / mode | Pass mean W | Pass instantaneous peak W | Max collector A | Calculated case / junction °C |
| --- | ---: | ---: | ---: | --- |
| 32% / ERP1 / m0 | 4.79 | 4.79 | 0.701 | 97.7 / 109.7 |
| 32% / ERP1 / m0.8 | 3.62 | 4.85 | 1.142 | 84.8 / 93.8 |
| 32% / ERP0.3 / m0 | 2.87 | 2.87 | 0.452 | 76.6 / 83.7 |
| 32% / ERP0.3 / m0.8 | 2.52 | 2.89 | 0.694 | 72.7 / 79.0 |
| 42% / ERP1 / m0 | 3.65 | 3.65 | 0.534 | 85.2 / 94.3 |
| 42% / ERP1 / m0.8 | 2.83 | 3.74 | 0.842 | 76.1 / 83.2 |
| 42% / ERP0.3 / m0 | 2.29 | 2.29 | 0.361 | 70.2 / 75.9 |
| 42% / ERP0.3 / m0.8 | 2.04 | 2.29 | 0.529 | 67.5 / 72.6 |

These continuous thermal arithmetic cases assume the pass sink alone. They are not shared-spreader results or hot SOA passes; the no-tone case bounds higher pass heat when the calibrated voltage depth is smaller. The approximately66°C sensor trip can precede the listed steady-state case temperature. A mechanically detached but electrically connected sensor remains a physical failure concern.

For the training branch alone, a3.465 V maximum logic rail and99 Ω minimum collector feed give an approximate30 mW available-power ceiling before the pad. A16 dB pad reduces this toward a sub-mW reference-load energy bound, with nominalµW calibration. This is not a guarantee against supply overvoltage, RF coupling or every internal-device fault; verify the actual port and pad over frequency/load.

Power-resistor review also assigns R513’s1 kΩ VPA bleed to a≥0.25 W1206 part (0.144 W at12 Vdc), and R704’s100 Ω training collector feed to≥0.25 W1206 (approximately0.121 W under a collector short at maximum logic voltage). Resistor MPN package codes now follow the actual selected footprint; no0603 MPN is silently paired with a larger pad. R506’s exact1 W ordering suffix remains OPEN.
