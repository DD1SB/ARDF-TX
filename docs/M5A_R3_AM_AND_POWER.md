# M5A-R3 — sine AM, power and endurance

Dated 2026-10-15. **PRIVATE CONSTRUCTION DERIVATIVE / NOT RELEASED. All ARDF-TX hardware tests NOT_RUN.** No orders, PCB fabrication, assembly or transmission. M5A-R1 remains the archived fallback; RF80, M4A, the controller and accepted ADRs are unchanged.

## Requirements remain unchanged

[IARU PartB2025 Appendix1 T2.8/T2.4](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf),p10, rechecked2026-10-15:144.500–144.900MHz championship carrier, stability better than50ppm, concurrent transmitter spacing **>200kHz**,0.25–1W carrierERP,A2A,70–80%AM,8–15WPM,horizontal antenna at2–3m, applicable national unwanted-emission limits, no unscheduled radiation. This competition document does not grant legal transmitter authorization. Existing country/profile/legal requirements remain in [M1 regulatory baseline](M1_REGULATORY.md).

Using the **unqualified**−1dBd net antenna/feed assumption:

| ERP carrier | Conducted carrier | Mean RF at75%AM | PEP at80%AM | Capability with1dB reserve |
| --- | --- | --- | --- | --- |
|1W|1.2589W|1.6130W|4.0789W|5.1351W|
|0.90W|1.1330W|1.4517W|3.6710W|4.6215W|
|0.30W|0.3777W|0.4839W|1.2237W|1.5405W|

`PEP=Pc(1+m)^2`; mean RF=`Pc(1+m²/2)`. Published DL3BBX output is at its50ohm connector after its original matching/filter; do not subtract that same network twice. Any subsequently added output filter/cable loss must be charged separately. At−1dBd,3WPEP is1.33dB short of4.079W,2.33dB short of5.135W. MaxiTX1.2W is5.31dB/6.31dB short respectively. **DL3BBX reports greater than3W, not an upper ceiling of3W.** Its actual maximum clean sineAM PEP remains unknown. A positive antenna-gain assumption must not be invented to close this gap.

The upper target stays open; the schematic is not silently redefined as a0.58W transmitter. A measured lower level could be competition-appropriate, but adopting it as the normal product target requires explicit review. A0.30W reducedERP setting with±0.4dB total uncertainty would span0.274–0.329W; a0.90W full setting spans0.821–0.987W. These are calibration examples; neither actual uncertainty nor antenna gain has been measured.

## Actual AM implementation

ESP32-S3 provides coherent `LEVEL_PWM` DC/carrier-reference and `AF_PWM` offset+sine, initially800Hz at312.5kHz PWM. Two unity Sallen-Key sections use10k/10k and4.7n/4.7n with TLV9004. Their equal-component unity-gain Q=0.5 and natural frequency3386Hz give calculated attenuation0.947 at800Hz and0.000117 at312.5kHz, approximately−78.6dB ideal PWM-frequency attenuation. These are small-signal filter calculations, not measured switching spur levels.

KEY selects AF or equal-offset carrier reference via SN74LVC1G3157. SLOT keeps a carrier present for the scheduled interval; KEY keys the sine tone, not RF/FM/FSK. **No RF outside SLOT.** Match both DC offsets and ramp audio over a few tone cycles in future firmware to avoid steps; no production firmware is implemented.

The command feeds original VR1=47k →R24=2.2k →C27=100n film shunt →R25=2.2k →C26=330n film →TIP127 base. Original R26=10k to emitter and VR2=100k base/collector set carrier supply by negative collector feedback. **Before power, set VR2 for approximately100k from PASS_BASE to VPA; a short increases conduction.** Wiper2 is tied to end1; wiper at end1 gives maximum effective resistance to end3. The pot cannot guarantee RF-off; source/rail hardware interlocks do that. The source is AC-coupled; a steady failed PWM does not create steady full modulation. PWM/carrier bias faults cannot be treated as protection against arbitrary mistimed SLOT; independent lease/mute remains essential.

At800Hz the extra original R24/C27 pole is near723Hz **only with low source impedance**; VR1 wiper resistance can lower it further. Tone amplitude must be calibrated after all filters. Available3.3V command peak, attenuation and Darlington beta may limit depth: **no assertion that3.3V automatically yields75%AM**. If the inherited input cannot reach70–80% without clipping, the smallest required audio-level correction must be reviewed. No high-power op-amp servo is reintroduced speculatively. RF envelope depth is measured from RF maxima/minima, not inferred from the supply waveform. THD≤5% is an initial engineering criterion, not an IARU rule.

## Envelope headroom and thermal limits

Original no-tone8V collector setting is not automatically suitable for80% sineAM. Ideal13.8V upstream with assumed2V pass dropout gives11.8V crest; for linear voltage transfer this implies6.56V center and1.31V trough. At8V center an80% ideal crest would be14.4V, already above the supply even before dropout. Actual RF amplitude-versus-collector-voltage transfer, knee and compression remain unknown; VR2 must be set from the RF envelope. Original rectangular >90% modulation does not prove sine linearity.

TIP127 replaces only the old PNP Darlington: ST1B/2C-tab/3E, live modulated collector tab,1.92°C/W junction-case,150°C maximum. At an **assumed**0.30A center current proportional to voltage, ideal pass dissipation is1.54W under80% AM,2.17W no-tone and2.18W maximum instantaneous. An overload illustration0.60A center doubles these losses and would exceed the present AM crest-current trip; it is not an operating setting. Exact hot DC/repetitive SOA is an OPEN acceptance gate; single-pulse curves cannot prove continuous audio safety.

A sizing example with3°C/W sink+1°C/W insulating interface,40°C ambient and4.35W no-tone overload gives57.4°C case and65.7°C junction. This is **not a qualified sink or sensor measurement**. Keep the approximate66°C NTC trip; do not raise it to accommodate an undersized sink. Thermal contact must represent the hottest case/spreader and account for delay, final-device junction/case rise and insulation. With ASI's22°C/W final junction-case,3W final waste alone adds66°C. The final and pass device cannot be declared safe from the same remote sensor without proving the case gradients and worst no-load/mismatch condition.

The original0.5–0.6A adjustment instruction is reconciled with Motorola's640mA maximum instead of copying the article's1A claim. R3's loaded-reference current trip is **0.5936A nominal total normal-rail current**. RF AM crests plus driver current may reach this limit before the desired upper PEP. That is an explicit performance blocker; do not raise the limit or replace the final silently to force a number. ASI1A rating does not establish matching or thermal equivalence.

## Supply and safe sequencing

2S boost is preferred for a possible integrated private build: protected6.0–8.4V, TPS611781 fixed-population boost, captured profile selects nominal **10.901/13.815V**. 4S alternative TPS54302 selects **10.788/13.785V** from12.0–16.8V; full cannot be maintained below approximately14.4V loaded input. Refuse full-power SLOT when measured rail is low. Reduced4S is intended across the12V endpoint, subject to dropout validation. Do not book all4S capacity as full-power usable. Neither raw4S nor the wrong charger is allowed into a2S population; fixed assembly voltage windows and separate protected pack wiring remain.

Original470uF C25 is **upstream** of slot isolation/current sensing; local switched rail uses1uF plus bypass. Slot permission controls the normal rail as well as the72MHz source. Added1uF gate-source capacitor slows the isolation FET, and the existing final HC14 inverter gets10k/100n startup delay with Schottky/330ohm fast discharge. The100k RC pull-down is populated in training-only too. These prevent a known capacitor-inrush/startup ordering problem by design intent, **not measured timing qualification**. Approximate source delay is sub-ms to a fewms with thresholds/tolerances; rail withdrawal can take severalms. Require measured source-before-rail shutdown, bounded inrush, no self-oscillation, and deliberate rearm. The original self-oscillation warning makes source-only inhibit insufficient.

Nominal regulator and PA-rail OV trip is15.04V. TVS18V is not a precision clamp, converter failure/lead transients remain unqualified, and only a bounded current-limited bench supply may be considered for future initial bring-up. No unrestricted pack connection is approved. Reverse/input/rail FETs, comparator/INA180 and thermal window remain; no extra RF detector/ADC/controller added.

## Reproducible energy model — estimates only

Original500–600mA is a no-tone **alignment** current range. Budget0.55A at13.8V throughout each active slot as a conservative scenario; reduced0.30A at10.9V is **assumed**, not measured at0.30WERP. Add0.10W active source/audio allowance; converter efficiency87% boost/91% buck. Controller0.14W and RF idle0.04W are continuous assumptions. Duty20%, with no Morse discount. LoRa absent baseline; add0.006W intermittent or0.045587W continuous-RX plus modeled bursts scenario. Regulator idle is included in the0.04W allowance and must be measured separately.

2S full mean1.948W:12h23.37Wh; reduced0.955W:24h22.91Wh. Continuous full beacon9.019W; reduced4.054W. 4S model1.870/0.921W saves only about4% before inaccessible full-power capacity. Battery usable energy is cell-count×8.82Wh(2450mAh minimum class) or11.90Wh(M35A minimum-energy basis),×0.8aging×0.9temperature×0.9discharge-window. These inherited factors are assumptions; capacity datasheet endpoints and BMS voltage sag differ from the3V/cell design endpoint.

| 2S pack / cell basis | Full hours, modeled | Reduced hours, modeled | 12h /24h arithmetic |
| --- | --- | --- | --- |
| 2S2P / 25R_2450mAh_min | 11.7 | 23.9 | NOT qualified hardware |
| 2S2P / M35A_min_energy | 15.8 | 32.3 | NOT qualified hardware |
| 2S3P / 25R_2450mAh_min | 17.6 | 35.9 | NOT qualified hardware |
| 2S3P / M35A_min_energy | 23.8 | 48.5 | NOT qualified hardware |
| 2S4P / 25R_2450mAh_min | 23.5 | 47.9 | NOT qualified hardware |
| 2S4P / M35A_min_energy | 31.7 | 64.6 | NOT qualified hardware |


Under this model2S2P2450 fails12h full and is just short of24h reduced; do not call it a robust minimum. **2S3P2450 or2S2P high-capacity** are the smallest modeled combinations with20% margin for both targets, not qualified packs. Exact current, cell resistance/cold behavior and achieved RF settings may change this result. At full budget and6V input, active battery current is about1.47A plus0.03A idle/controller; cell current divides by P. Converter/AM startup peaks require separate measurement.

4S1P and2S2P contain the same energy for the same cells. Full4S accessible fractions0.5/0.7/0.9 are sensitivity examples, not measured discharge integration.4S2P gives more modeled margin but cannot be guaranteed without a voltage-window capacity trace. Reduced4S1P2450 gives24.8h with little margin; high-capacity gives33.5h. Continuous full beacon on2S4P2450 is only5.1h, high-capacity6.8h; neither meets12h continuous. No endurance/RF-compliance PASS is claimed.

[RF arithmetic](../hardware/2m/review/M5A-R3/rf-power.json), [operating states](../hardware/2m/review/M5A-R3/operating-states.csv), [all packs and4S windows](../hardware/2m/review/M5A-R3/endurance.csv), [sensitivity](../hardware/2m/review/M5A-R3/sensitivity.csv), [thermal examples](../hardware/2m/review/M5A-R3/thermal-examples.json) are generated by `python3 tools/m5a_r3_models.py`. No transistor large-signal or analog transient simulation is claimed.
