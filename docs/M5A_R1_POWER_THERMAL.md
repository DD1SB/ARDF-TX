# M5A-R1 — power, thermal and endurance

Date: **2026-10-15**. **M5A-R1 electrical evaluation candidate — NOT RELEASED. All physical tests NOT_RUN.**

Prefer the **2S boost population for a six-cell 2S3P/M35A endurance evaluation**, with an exclusive 4S buck alternative. The lower-voltage PA has not made a boost-free 2S AM design credible: low pack voltage cannot deliver a roughly 7.3 V capability crest plus series-pass headroom. A 4S buck can maintain 10 V throughout the proposed 12–16.8 V window, avoiding R0's high full-power cutoff. It saves approximately €1.93 on the board, but may require two more cells for robust extended endurance.

## Actual converter and rail changes

| Rail | Native R1 feedback parts | Calculated settings |
| --- | --- | --- |
| 2S TPS611781 | R401 = 510k/R402 = 100k, R414 = 250k switched | 7.4969 / 10.0041 V |
| 4S TPS54302 | R301 = 116k/R302 = 10k, R303 = 27.8k switched | 7.5096 / 9.9965 V |
| Driver TLV76150DCYR | Fixed 5 V; R413 = 2.2 Ω input; C409150µF output | 5 V±1.75% full temperature; Q304 switched separately |
| Normal AM feedback | R511 = 18k/R512 = 10k | Gain 2.8 |
| Protection | R817 = 29.4k/R815 = 80.6k; R821 = 26.5k; R813 = 20.9k | Driver OV5.737 V, drain OV8.203 V, main OV≈10.50 V |
| Current/4SUV | R829 = 4.02k; R807 variant 24.9k; removeR830/Q801 | Nominal 1.80 A trip; 4SUV≈12.15 V in both profiles |


Keep the R0 reverse/input/rail switches and window protection; replace the 2 A fuse candidate with Littelfuse `0466004.NRHF` (4 A fast,1206). The manufacturer 466 series table (GD21-Jun-2023) specifies 32VDC/50 A interruption; actual BMS/pack prospective fault current, fuseI²t/temperature derating and trace coordination remain OPEN. A 4 A fuse is not the PA protection: the independent 1.8 A current trip remains. At 6 V, full-slot battery current can exceed 2 A, so the old rating lacked derating margin. The new fuse has a €0.50 estimate, not a quote. Keep converter compensation and other input parts as candidates. TPS611781 remains 4.7 µH/approximately 500 kHz,5 A nominal switch limit; current slope, compensation and effective capacitance need exact-component qualification. At 6 V input,10 V output and 80% of 4.7 µH at 400 kHz, ripple≈1.60 A p-p. A 1.55 A output crest needs≈2.97 A input at 87%, giving≈3.77 A switch peak before losses/tolerances. The lower-efficiency cases can trip the 1.8 A local limit: their calculated endurance is not sustainable operation. Fuse 4 A input/its I²t, wiring and BMS must support intended crest pulses without sacrificing fault interruption; fuse sourcing and fault coordination remain OPEN.

## Driver simplification and fault limits

The former driver buck/magnetic/feedback is removed. [TI TLV761](https://www.ti.com/lit/ds/symlink/tlv761.pdf), SBVS349D May 2025, supports 18 V input/20 V absolute, DCY pins 1GND,2OUT/tab,3IN, with 1–220 µF and 2–500 mΩ output-capacitor ESR. Exact 5 V part is orderable; LD1117 was rejected because its ordinary 15 V absolute input limit is insufficient for a 16.8 V upstream fault. The new live LDO tab is 5 V, not ground.

At 180 mA and 10.5 V VMOD, R413 drops 0.396 V and LDO heat is about 0.92 W. Require effective thermal resistance≤80 °C/W at 45 °C local ambient (estimated Tj≤119 °C), or change package/cooling after measurement. The generic 95.4 °C/W datasheet fixture would be too hot near this worst condition. At 7.5 V−3%, after damping and a 0.2 V path allowance, LDO input remains≈6.68 V; verify regulation under load/startup. Power-on inrush into 150 µF is not a qualified normal transient.

C409 requires 120–180 µF actual capacitance, ESR2–100 mΩ, exact part and footprint OPEN. D309 is a Schottky output-to-input bypass per TI reverse-current guidance; its actual current/voltage/surge and package remain sourcing/measurement gates. Q304 independently isolates RF drive. For an LDO-short fault with 10.5 V source,5.0875 V initial rail, R≥2.178 Ω, C≥120 µF, ESR≤0.1 Ω and **Q304 physically open within 20 µs**, the ideal RC/ESR calculation peaks at 5.691 V. At 100 µs it can exceed the 6 V absolute limit. Overshoot, MOSFET delays, surviving VMOD storage and ground bounce are not included. Q302 opening alone does not remove energy already in C306; measure Q304 isolation itself. Test with MMIC omitted, equivalent load and bounded fault source before connecting it. This is a conditional calculation, not protection qualification.

## Thermal discrepancy resolved as an assembly requirement

Do not raise the approximately 66 °C thermistor threshold. The lower-voltage PA draws more current and does **not** automatically reduce pass heat. Preserve ST D45H11, RθJC2.5 °C/W, and its live collector tab; hot DC/repetitive SOA remains OPEN until the exact graph is assessed against the full trajectory. Device nominal current/power ratings do not close that gate. The model includes BD139 base-drive heat and fixed 5 V driver losses.

| Assumedη/full-carrier | ERP/m | Pass mean/peak W | Helper mean/peak W | Case/Tj estimate °C |
| --- | --- | --- | --- | --- |
| 0.45 | 1/0 | 5.17/5.17 | 0.18/0.18 | 58.3/71.2 |
| 0.45 | 1/0.8 | 4.50/5.31 | 0.18/0.28 | 57.2/70.4 |
| 0.45 | 0.3/0 | 2.86/2.86 | 0.09/0.09 | 52.6/59.8 |
| 0.45 | 0.3/0.8 | 2.66/3.08 | 0.09/0.13 | 52.3/60.0 |


These illustrative periodic results require a shared 3 °C/W spreader,80J/K thermal capacity,1 °C/W insulated pass interface,45 °C ambient and 60s on/240s off. They are not a 10 °C/W isolated sink or continuous-carrier result. Require measured pass case and correctly bonded sensor≤60 °C during normal profiles, measured junction estimate≤125 °C with margin, and trip before hot SOA is exceeded. Validate sensor-to-case offset, mounting tolerance and response delay; electrical open/short detection does not detect a detached intact sensor. The unqualified spreader/insulation costs €8–14 outside PCB components. Actual pass/PA heat, case-to-spreader contact and hot SOA can require more cooling.

Carrier-only within a slot is hotter for the pass transistor than the modeled AM mean. Continuous full-power beacon dissipates roughly 8.7 W in the shared assembly in the no-tone example:3 °C/W gives a spreader near 71 °C before interfaces, so that arrangement is NO-GO for continuous service at 45 °C. A separately qualified≈1 °C/W or better thermal assembly is required; battery-only beacon hours below are energy upper bounds.

## Endurance — modeled, not measured

[Analysis script](../tools/m5a_r1_analysis.py), [JSON](../hardware/2m/review/M5A-R1/calculations.json), [60-row pack CSV](../hardware/2m/review/M5A-R1/endurance.csv) and [288 sensitivities](../hardware/2m/review/M5A-R1/sensitivity.csv) retain the M2/R0 cell framework. Assumed current is `I=0.1+gV`, g calibrated at 45% full-carrier PA efficiency; reduced efficiency changes with voltage. The RF amplitude law is explicitly hypothetical. Main boost/buck efficiencies 87/91%, controller 0.14 W, RF idle 0.03/0.04 W, driver 146 mA, source 0.11 W/90%, helper/bias 0.30 W and 20% complete-slot RF duty are included. PREPARE must be withdrawn between slots. Morse-space carrier remains powered, so no mark-duty credit is taken.

| Supply/ERP, m=0.8 | TX/average W | 12 h/24 h Wh |
| --- | --- | --- |
| BOOST2S/1 | 12.54/2.672 | 32.06/64.13 |
| BOOST2S/0.9 | 12.13/2.590 | 31.09/62.17 |
| BOOST2S/0.3 | 6.84/1.531 | 18.37/36.74 |
| BUCK4S/1 | 11.62/2.496 | 29.95/59.89 |
| BUCK4S/0.9 | 11.25/2.422 | 29.07/58.14 |
| BUCK4S/0.3 | 6.43/1.458 | 17.50/34.99 |


Cells remain 25R minimum-capacity proxy 8.82 Wh and M35A minimum-energy 11.9 Wh. Multiply by 0.8 aging×0.9 temperature×0.9 accessible-endpoint allowance. These are not equal-resistance/current-rated cells. R1 has no additional R0-style 0.60 high 4S cutoff-window factor, but the remaining 0.9 accessible-energy factor is unmeasured at 12.15 V cutoff; validate actual discharge curves, sag and cold cutoffs.

| Pack/cell | Full 1 ERP h | Reduced.30ERP h | Full/reduced continuous beacon h |
| --- | --- | --- | --- |
| 2S2P/25R_min | 8.6 | 14.9 | 1.8/3.2 |
| 2S2P/M35A_min | 11.5 | 20.1 | 2.4/4.3 |
| 2S3P/25R_min | 12.8 | 22.4 | 2.7/4.8 |
| 2S3P/M35A_min | 17.3 | 30.2 | 3.6/6.5 |
| 2S4P/25R_min | 17.1 | 29.9 | 3.6/6.4 |
| 2S4P/M35A_min | 23.1 | 40.3 | 4.8/8.6 |
| 4S1P/25R_min | 9.2 | 15.7 | 1.9/3.4 |
| 4S1P/M35A_min | 12.4 | 21.2 | 2.6/4.6 |
| 4S2P/25R_min | 18.3 | 31.4 | 3.8/6.8 |
| 4S2P/M35A_min | 24.7 | 42.3 | 5.2/9.2 |


2S2P/M35A fails the modeled full target; 4S1P/M35A barely passes full but fails 24 h reduced.2S3P/25R fails extended. The smallest two-target base-model candidate is 2S3P/M35A; 2S4P/25R and 4S2P with either class also pass this model. None is a qualified minimum. Both 1 ERP and guarded 0.9 ERP calculations exist; choose actual settings from calibrated antenna/feeder uncertainty, not runtime convenience.

Sensitivity variesη32/45/55%, Iq100/200 mA, driver 146/180 mA, controller 0.14/0.28 W and LoRa absent/intermittent 0.006 W/continuous receive 0.045 W. Poor-efficiency cases may exceed current trip and cannot sustain full output. LoRa bursts 0.44 W×80ms/min add 0.000587 W as an additional allowance; exact Silicontra currents remain OPEN. Double controller overhead removes 3.36 Wh/day; PA/linear-pass loss dominates this candidate. Radio-absent is supported; source/regulator idle is not assumed zero. Standby measurements and thermal/inhibit behavior must precede endurance claims.

No new accepted ADR is changed. This is a proposed VHF-specific operating-point update within the existing dual-voltage architecture; neither controller hardware nor 80m power circuits are edited.

Both75% and80% AM rows are retained. Their mean DC input is identical in this affine-current model because the sine current averages to the same Icenter; RF sideband power and pass/PA heat redistribute. This is a consequence of the assumed model, not evidence that the real amplifier draws equal current at both depths. No full-power efficiency or battery curve is measured.
