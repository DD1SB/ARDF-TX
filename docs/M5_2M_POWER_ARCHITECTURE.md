# M5A VHF supply and modeled endurance

Date: **2026-10-15**. **Prefer the exclusive2S boost population for the first normal-power evaluation; retain an exclusive4S buck population.** This implements the existing dual-voltage proposal without a universal buck-boost. An assembled board must match its pack/window stuffing and J302 link. The controller can power training from either protected pack through regulated3.3 V; raw4S must never enter a2S-populated converter.

## Actual electrical implementation

Q309 is a30 V P-channel reverse protector, drain facing the fused battery and source facing VIN_PROT, with a10 V gate clamp. Q305 independently disconnects a wrong/unsafe pack before the converters. Q302 disconnects converter output on hard rail/current/thermal faults; Q304 separately gates the MMIC supply. Each has default gate bias and a gate clamp where its source can exceed the gate rating. U304 qualifies input and output-switch drive with the distinct PACK_OK_N/HARD_OK_N buses. Gate pull-ups are 4.7 kΩ, with 1 kΩ collector-to-gate resistors; uncertain diode-clamped NPN base drive was removed. The nominal VPA overvoltage trip is 12.63 V, independent of the PWM command, to detect a shorted pass device. Converter readiness is checked after profile capture and before SLOT at the controller through PA_RAIL_ADC; it is not another local safety state machine. They address distinct failure paths; an external battery BMS does not replace PA-current, waveform or driver-voltage protection.

TPS611781 is the20 V-capable forced-PWM2S boost. Starting settings are4.7 µH,340 kΩ frequency resistor near the published500 kHz point,150 kΩ current limit near5 A nominal, and a marked provisional compensation network. The feedback is715 kΩ/100 kΩ for approximately10.02 V, with249 kΩ switched across the bottom leg for approximately13.55 V full. **Exact power inductor, effective capacitors, RNW landing and loop compensation remain OPEN.** Shutdown alone does not block a synchronous boost's through path; the external isolation is intentional.

The alternative TPS54302 buck uses10 µH and158 kΩ/10 kΩ for approximately10.01 V; a27 kΩ switched branch gives approximately13.50 V. Only this converter or the boost is fitted, with one exclusive J302 strap. R807/R809 substitutions and the full-profile threshold switches are explicit in the manifest/BOM. Nominal VIN_PROT cutoffs (after reverse protection) are approximately6.21/8.62 V for2S and12.15 V reduced or14.51 V full /17.17 V maximum for4S. Divider/reference/comparator tolerances must be included in actual thresholds. The4S full cutoff is deliberately higher than the old14.2 V estimate to allow input loss and dropout margin; it is still a measurement gate.

The driver uses a second small TPS54302 at approximately8.523 V, followed by2.2 Ω/100 µF and Q304. At234.1 mA, nominal filtered voltage is approximately8.008 V. This is a necessary driver rail, not a second programmable PA supply. The series resistor dissipates about0.14 W at251 mA, so its selected pulse/power rating remains a sourcing gate. The100 µF reservoir must retain at least80 µF and have qualified ESR; ordinary schematic capacitance is not that qualification.

A hard driver-rail comparator nominally trips near8.90 V. For a bounded14.5 V failed-driver-buck step, worst starting8.3 V, R≥2.178 Ω and C≥80 µF, the ideal20 µs RC result is below9.0 V; an ESR≤0.2 Ω allowance adds an initial step of about0.52 V. This leaves conditional margin below the PHA13's10 V absolute maximum. **Isolation including driver switch turn-off≤20 µs is unmeasured.** A50–100 µs response can violate the limit. Qualify with the MMIC omitted and an energy-limited fault fixture before exposing it to this fault; no simulated surge immunity is claimed.

Raw input transients, reverse insertion, capacitor inrush, fuse coordination and ground bounce remain bounded-lab gates. Use3.3 V current-limited logic and separately bounded pack-equivalent supplies first. No unrestricted Li-ion fault test or direct16.8 V driver/modulator feed is authorized.

## Reused model, explicit updates

[The calculation script](../tools/m5_2m_analysis.py), [JSON](../hardware/2m/review/M5A-R0/calculations.json) and [60-row CSV](../hardware/2m/review/M5A-R0/endurance.csv) preserve the M2 cell/aging/temperature framework. Actual circuit updates are the selected driver's234.1 mA, its90% buck allowance,87% boost/91% buck assumptions, input path0.15 Ω with a1.3 RMS-loss factor, source/dynamic overhead0.11 W, helper allowance0.15 W and RF idle0.03 W (2S) or0.04 W (4S), plus0.10 W active gate/sense allowance. These are not measured board currents.

Controller average is now0.14 W: S3 active80 mA for20% and idle25 mA for80%, at3.3 V, approximately90% conversion plus RTC/monitor allowance. This is more conservative than the old10%-active/0.12 W model because tone updates occupy the RF slot. Continuous beacons use0.30 W controller allowance. RF duty is20% for the entire slot, with **no RF Morse-mark discount**. Source/converter/driver are off between slots; their idle losses and local sensing are included in the0.03/0.04 W allowances; the larger4S term includes reverse-protection gate-clamp current. A firmware policy that leaves PREPARE/PA_PREPARE high invalidates these figures.

The PA model is `I(V)=0.15+gV`; g is calibrated from assumed42% full-carrier efficiency at the PA plane. At reduced voltage its calculated carrier efficiency falls, rather than remaining fixed. Actual output need not follow V²; both the voltage calibration and this consumption model require hardware data.75% and80% AM rows are retained; constant-drive driver DC remains present during carrier-only Morse gaps.

| Supply/profile, m=0.80 | TX battery W | Contest average W | 12 h Wh | 24 h Wh |
| --- | --- | --- | --- | --- |
| BOOST2S / 1 W ERP | 11.52 | 2.468 | 29.62 | 59.24 |
| BOOST2S / 0.9 W ERP | 11.19 | 2.402 | 28.83 | 57.65 |
| BOOST2S / 0.3 W ERP | 7.10 | 1.584 | 19.01 | 38.01 |
| BUCK4S / 1 W ERP | 10.70 | 2.313 | 27.75 | 55.50 |
| BUCK4S / 0.9 W ERP | 10.40 | 2.253 | 27.03 | 54.07 |
| BUCK4S / 0.3 W ERP | 6.67 | 1.507 | 18.08 | 36.16 |


## Battery energy and cutoff

25R uses2.45 Ah×3.6 V=8.82 Wh minimum-capacity proxy per cell, not measured energy to our cutoff. M35A uses its11.9 Wh minimum-energy figure, not12.5 Wh typical. Both are multiplied by aging0.8, temperature0.9 and an accessible-discharge allowance0.9. The latter is only an estimate for these voltage windows.25R high-current ratings and AC impedance are not assigned to M35A; lot DC resistance, temperature behavior and aging curves remain separate measurements.

A further **0.60 full-power4S energy window** accounts for the approximately14.5 V cutoff; it is an unmeasured assumption, with0.40–0.80 sensitivity. Equal-cell2S2P/4S1P or2S4P/4S2P have equal nominal energy. Higher voltage provides no extra energy and cannot restore the inaccessible bottom of the full-power discharge.

| Pack / cell minimum | Full 1 W ERP model h | Reduced0.30 W ERP model h | Full / reduced beacon h |
| --- | --- | --- | --- |
| 2S2P / 25R_min | 9.3 | 14.4 | 1.9 / 3.1 |
| 2S2P / M35A_min | 12.5 | 19.5 | 2.6 / 4.2 |
| 2S3P / 25R_min | 13.9 | 21.6 | 2.9 / 4.6 |
| 2S3P / M35A_min | 18.7 | 29.2 | 3.9 / 6.3 |
| 2S4P / 25R_min | 18.5 | 28.9 | 3.9 / 6.2 |
| 2S4P / M35A_min | 25.0 | 38.9 | 5.2 / 8.3 |
| 4S1P / 25R_min | 5.9 | 15.2 | 1.2 / 3.3 |
| 4S1P / M35A_min | 8.0 | 20.5 | 1.7 / 4.4 |
| 4S2P / 25R_min | 11.9 | 30.3 | 2.5 / 6.6 |
| 4S2P / M35A_min | 16.0 | 40.9 | 3.4 / 8.8 |


These are **modeled hours, not compliance or qualified minimum packs**. In the base model2S2P/M35A barely passes12 h full and fails24 h reduced.2S3P/25R passes12 h with modest margin but fails24 h; it is not a robust two-target minimum.2S3P/M35A and2S4P/25R are candidate two-target packs.4S1P fails the full target even with M35A;4S2P/25R's approximately12 h full is marginal and must not be marketed as qualified.4S2P/M35A has more useful margin but still depends strongly on cutoff energy.

The144 sensitivity cases vary full-carrier efficiency32/42/52%, controller0.14/0.28 W, driver234.1/251 mA, and LoRa absent/intermittent/continuous RX. Optional LoRa adds0/0.006/0.045 W;0.44 W for80 ms each minute adds0.000587 W average. Exact Silicontra current and simultaneous RF immunity remain OPEN. RF-on consumption dominates the current budget, but double controller idle can remove several hours. Poor PA efficiency can invalidate an otherwise passing pack; measure before choosing the minimum.

For a4S full-energy window of0.40 instead of0.60, full runtime drops by one third. An0.80 window increases it by one third. Continuous beacon rows show that even eight cells do not provide12 h full-power or24 h reduced continuous service in this model. A beacon duration requirement, larger external supply or a different qualified setting must be specified separately.

## Power cost and restrictions

The buck population saves about€1.84 in component allowances, but equal-cell4S batteries/BMS/charging can cost more and the full-voltage window can require eight cells instead of six. Do not select4S merely because its RF converter is cheaper. No full-power capability is promised from the wrong assembly/pack combination. No automatic in-contest reduction follows undervoltage; stop RF and require deliberate profile selection/rearming.

Proposed clarification to still-proposed ADR0011: prefer the2S VHF boost population for the first full/extended evaluation; retain the4S buck variant with the declared high full-power cutoff. No accepted ADR, controller supply or80m design is changed.

The source/dynamic0.11 W is charged through a separate90%-efficient3.3 V supply in the calculation, matching J101 power; it is not physically supplied by the PA converter. At6 V input/13.5 V output,400 kHz and80% of4.7 µH, nominal boost ripple is about2.2 A peak-to-peak. With an approximately2.5 A envelope-crest input requirement the estimated peak is about3.6 A, below a nominal5 A switch limit. Exact duty-dependent minimum limit, saturation current, DC loss and loop response still require the selected inductor/data and measurements.

The32%-efficiency full-AM stress case can exceed the nominal approximately1.2 A local current-trip threshold after including driver current. Those cases are flagged `current_trip_risk` in the sensitivity data: their energy arithmetic is not a sustainable full-power operating claim. No automatic RF power reduction is used to make them pass.

Beacon runtime values are **energy upper bounds**. The thermistor divider's nominal hot threshold is about66°C; a10°C/W pass-device sink alone can exceed that case temperature during continuous full power at45°C ambient. A shared PA/pass spreader sees their combined heat. Continuous beacons need a separately qualified larger sink/thermal arrangement and may stop before the calculated battery time. For training-only continuous AF, a conservative approximately0.52 W whole-system budget (controller0.30 W plus source/buffer/BJT/regulation) gives about22 h from2S1P/25R or30 h from2S1P/M35A; these are rough calculations, not qualified training runtime.

The local current reference is approximately1.03 V after divider loading, with a10 kΩ/7.5 kΩ sense divider preserving approximately1.2 A trip. This fits the LM339B hot common-mode bound at the specified minimum logic voltage. The pack thresholds are measured at VIN_PROT; external battery cutoff is slightly higher by the reverse-FET/wiring drop. Actual input faults, cold/aging behavior and accessible energy remain measurements.
