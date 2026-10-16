# M5A-R4 — true AM, power and endurance

Dated **2026-10-16**. **M5A-R4 electrical candidate — NOT RELEASED.**
All physical tests are **NOT_RUN**. No purchasing, fabrication, assembly or RF operation has occurred.
RF80, M4A and accepted ADRs are unchanged. R3 is preserved at tag `m5a-r3`
(`daf994c`); R0/R1 tags and the R1 native archive remain available.

The retained historical principle is **constant RF drive and gate bias, with final drain-supply modulation**. R1's quad-opamp reconstruction/feedback and D45H11/BD139 are reused. There is no RF-envelope detector. A clean drain-voltage waveform alone does not prove clean RF AM.

## Modulation circuit and power

The ESP32-S3 supplies 312.5 kHz PWM; no internal DAC is assumed. Two unity Sallen-Key sections use 10 kΩ/10 kΩ and 4.7 nF/4.7 nF, approximately 3.39 kHz corner and Q 0.5. LEVEL_PWM supplies carrier DC; AF_PWM supplies the same offset plus a configurable sine, initially 800 Hz. The tone is not an IARU mandate. U402 selects DC for KEY = 0 and sine for KEY = 1 within SLOT. The carrier persists only inside SLOT; keyed AF implements A2A. The controller ramps transitions and applies calibration; no production firmware is implemented.

U401C controls BD139 and the D45H11 pass device so VPA ≈2.8 × MOD_COMMAND. R507/Q403 limit helper current to approximately 73 mA, not a precision PA trip. R505 returns pass base to emitter. Q404/Q405 clamp helper drive and command; Q502 grounds final bias; U305 disconnects the 5 V driver; U601 mutes its clock. The upstream rail stays precharged to avoid inrush every slot. Analog faults open upstream isolation and clear ARM. A pass short must still be contained by bias/driver/clock shutdown; off-slot feedthrough and oscillation remain physical gates.

The initial full **voltage** envelope is 7.2 V crest, 4 V center and 0.8 V trough at 80% depth. MOD_COMMAND is 1.429 ±1.143 V, range 0.286–2.571 V. Reduced candidate is 4 V crest, 2.222 V center and 0.444 V trough. These are starting calculations, not calibrated RF settings. Knee voltage, impedance, gain and AM-to-PM vary during the envelope. Require actual 70–80% RF depth and initially ≤5% envelope THD. Clipped/non-monotonic behavior is a NO_GO. Modest reference correction may follow measured transfer; no elaborate new servo is assumed.

[IARU Region 1 2025 Part B](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf), Appendix 1 T2.8, specifies 144.500–144.900 MHz, stability better than 50 ppm, simultaneous spacing **more than** 200 kHz, 0.25–1 W carrier ERP, A2A at 70–80%, 8–15 WPM, horizontal polarization and 2–3 m antenna height. T2.4 prohibits unscheduled RF. National operating permission, frequencies and emissions are separate obligations; rules are not legal transmitter authorization.

`PEP = Pc × (1+m)²`; mean AM RF is `Pc × (1+m²/2)`. At −1 dBd net antenna/feed gain, 1 W ERP needs 1.259 W conducted carrier and 4.079 W connector PEP at 80%. At 0 dBd: 1 W and 3.24 W. With 0.75 dB combined output loss the final needs 4.848/3.851 W crest. Extra 1 dB capability reserve is optional, not another championship limit. Neither antenna scenario is measured. Proposed full calibration is 0.90 W ERP with ≤0.4 dB total uncertainty, upper bound 0.987 W; reduced 0.30 W gives lower bound 0.274 W. A missing near-upper capability must be reported, not hidden by lowering the setting.

## Supply, protection and heat

Protected 2S at 6.0–8.4 V uses TPS611781 boost at **9.021 V** for both profiles. Protected 4S at 12.0–16.8 V uses TPS54302 buck at **9.000 V full / 7.510 V reduced**. These are exclusive populations with different pack IDs/windows. A 7.5 V boost setting is invalid at charged 2S voltage. The 4S buck avoids the former 13.5 V rail's lost discharge window; raw 4S never reaches the 9 V circuit. Reduced 4S voltage saves pass heat without universal buck-boost.

R413 is 8.2 Ω/1 W. Initial reservoir charging is bounded to approximately 1.14 A at 9.2 V, below the nominal 1.8 A trip before tolerance/dynamics. Precharge with command/bias/clock clamped, verify the rail, then ARM. At 180 mA the resistor dissipates 0.266 W; full LDO input is approximately 7.54 V before upstream drops. Reduced-rail dropout/ripple at high temperature must be checked. The selected reservoir candidate is Panasonic **25SVPG150M**, 150 µF/25 V ±20%, 13 mΩ at 100 kHz, 6.3 mm diameter/9.9 mm height. Its manufacturer specification closes the generic identity gap, but effective capacitance ≥120 µF and ESR 2–100 mΩ across the qualified temperature/life window remain assumptions. Exact C10 landing, available stock and EUR quote remain OPEN; the €1.50 allowance is an estimate.

Driver OV uses 0.1% dividers. Nominal trip is **5.383 V**; an assumed ±1.5% reference bound gives **5.285–5.481 V**. With 8.118 Ω, 120 µF, 0.1 Ω ESR and a 16.8 V fault, the conditional upper calculation is **5.851 V** if isolation completes within 20 µs after threshold crossing. Require measured rail ≤5.9 V. Arithmetic does not qualify surge immunity or actual latency. An 18 V TVS is not a precision clamp below every part rating. Input hot-plug/FET transients remain OPEN; initial commissioning uses a bounded laboratory supply.

ST D45H11 and BD139 are base pin 1, collector/tab pin 2, emitter pin 3. The pass tab is live VPA and needs insulation from grounded RF thermal hardware. D45H11 RθJC is 2.5 K/W. The consistent loss/efficiency assumptions give full/reduced carrier drain currents approximately 0.748/0.505 A. Full 80% crest is approximately 1.347 A plus driver current; the nominal 1.8 A trip has no qualified transient margin. Full pass mean AM loss is approximately 2.80 W, or 3.76 W without tone. Reduced 2S pass loss is approximately 3.07 W, or 3.43 W without tone. Lower RF power does not automatically lower pass heat.

Keep the approximately 66°C sensor trip. Engineering targets are case ≤60°C and estimated junction ≤125°C, with sensor coupling qualified over 60 s on/240 s off. A dedicated 2 K/W sink and ≤1 K/W insulated interface at 40°C give approximately 51°C case/61°C junction in the full no-tone example. A shared sink must include PA/driver heat; a generic shared 5 K/W sink is not automatically adequate. Continuous beacons need separate cooling. Sensor open/short trips; an intact but detached sensor requires mounting inspection and lag qualification. Hot DC/repetitive SOA and helper heat remain OPEN; headline 50 W/10 A ratings are not linear-SOA proof.

## Modeled endurance

Carrier final power is `ERP × 10^0.175`; carrier current is `Pfinal/(Vcenter × PA efficiency)`; mean upstream is `Vup × (Icarrier + 0.146 A driver) + 0.10 W`. This includes linear-pass loss. Full/reduced PA efficiency is assumed 50%/40%, boost/buck 87%/91%. The 0.10 W active allowance covers helper/reference/source increment. Controller 0.14 W and RF idle 0.04 W are continuous. Duty is 20%, without Morse discount. Actual bias and waveform behavior may worsen these values.

| Profile | Variant | Active upstream W | Mean battery W | 12 h Wh | 24 h Wh |
| --- | --- | --- | --- | --- | --- |
| full | BOOST2S | 8.17 | 2.06 | 24.69 | 49.37 |
| full | BUCK4S | 8.15 | 1.97 | 23.65 | 47.29 |
| reduced | BOOST2S | 5.97 | 1.55 | 18.64 | 37.27 |
| reduced | BUCK4S | 4.99 | 1.28 | 15.32 | 30.63 |

Usable energy is cell count ×8.82 Wh for the 2450 mAh minimum class or ×11.90 Wh for M35A minimum-energy basis, multiplied by 0.8 aging ×0.9 temperature ×0.9 endpoint margin. The 3.0 V/cell endpoint and margins are inherited assumptions, not measured discharge integration. Equal cell counts give equal nominal energy for 2S2P/4S1P and 2S4P/4S2P.

| Pack | Cell basis | Full modeled h | Reduced modeled h | Full beacon h | 20% margin on both targets |
| --- | --- | --- | --- | --- | --- |
| 2S2P | 2450mAh_min | 11.1 | 14.7 | 2.4 | No |
| 2S2P | M35A_min_energy | 15.0 | 19.9 | 3.2 | No |
| 2S3P | 2450mAh_min | 16.7 | 22.1 | 3.6 | No |
| 2S3P | M35A_min_energy | 22.5 | 29.8 | 4.8 | Yes |
| 2S4P | 2450mAh_min | 22.2 | 29.4 | 4.8 | Yes |
| 2S4P | M35A_min_energy | 30.0 | 39.7 | 6.4 | Yes |
| 4S1P | 2450mAh_min | 11.6 | 17.9 | 2.5 | No |
| 4S1P | M35A_min_energy | 15.7 | 24.2 | 3.4 | No |
| 4S2P | 2450mAh_min | 23.2 | 35.8 | 5.0 | Yes |
| 4S2P | M35A_min_energy | 31.3 | 48.3 | 6.8 | Yes |

Use the 20% margin column rather than a marginal arithmetic pass. Under these assumptions, high-capacity 2S2P/4S1P meets 12 h full; robust 24 h reduced needs high-capacity 2S3P, 2450-class 2S4P or 4S2P. A high-capacity 4S1P is marginal for the reduced target, not qualified. Continuous full beacons do not inherit competition endurance.

LoRa absent is baseline; add 6 mW intermittent or about 45.6 mW continuous receive plus bursts. Controller/RF idle alone use 4.32 Wh/day; continuous LoRa adds about 1.09 Wh/day. [Pack table](../hardware/2m/review/M5A-R4/endurance.csv), [states](../hardware/2m/review/M5A-R4/operating-states.csv), [coarse sensitivity](../hardware/2m/review/M5A-R4/sensitivity.csv), [reduced-efficiency sensitivity](../hardware/2m/review/M5A-R4/reduced-efficiency-sensitivity.csv), [thermal calculations](../hardware/2m/review/M5A-R4/thermal.csv). Poorer PA efficiency, 500 mW controller idle or cold-cell sag can invalidate the minimum. No endurance PASS is claimed.
