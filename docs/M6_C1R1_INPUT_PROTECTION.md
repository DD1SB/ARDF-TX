# M6-C1R1 battery-identification correction

The M6-C1 direct connection from J1.3 to U21.5 was unsafe for a continuous ID-to-4S-positive short. TMUX1511 permits source/drain signals up to min(2×VDD, 5.5 V) while powered, 0–3.6 V below 1.5 V supply, and −0.5–6 V as absolute stress limits. The old note claiming 5.5 V powered-off protection is superseded. [TI SCDS390B, §§4–5](https://www.ti.com/lit/ds/symlink/tmux1511.pdf).

The corrected circuit uses five additional purchased parts and no new IC:

| Element | Implemented function |
|---|---|
| D22 BAS116,235 | PACK_PROT → pin 1 anode; pin 3 cathode → PACK_ID_EXC; pin 2 NC. Prevents ID fault feeding the excitation supply. |
| R3 27 kΩ, 1% | PACK_ID_EXC → PACK_ID_RAW. Replaces the former 10 kΩ connection to V3V3. |
| R8 180 kΩ, 1% | J1.3/PACK_ID_RAW → PACK_ID_SAFE. Limits continuous fault current. |
| R9 33 kΩ, 1% | PACK_ID_SAFE → GND. Defines the rail-independent positive voltage limit. |
| D23 Nexperia BAT54H,115 | Cathode pin 1 PACK_ID_SAFE; anode pin 2 GND. Negative-fault clamp. **Not** onsemi BAT54H, which has a different package. |
| C25 100 nF | PACK_ID_SAFE → GND, upstream of U21.5. |
| R19 100 kΩ, 1% | PACK_ID_ADC/U21.6 → GND. Bounds the unpowered ADC leakage voltage. |

The J1 pinout and external passive codes remain 10 kΩ for 2S and 22 kΩ for 4S. This is an explicit change to **host excitation and ADC decoding**: the ID wire is no longer a 3.3 V node. It may reach several volts in normal operation and must connect only to its passive coded harness and the protected front end. It is not a digital input, battery balance lead or RF-board signal. Existing M6-C1 ADC thresholds must not be used with R1 hardware. RF connectors and MCU GPIO assignments are unchanged.

For a forced raw-ID voltage, ignoring leakage that only lowers the positive voltage:

```
U21 off: Vsafe = Vid × R9 / (R8 + R9)
U21 on:  Vsafe = Vid × (R9 || R19) / (R8 + (R9 || R19))
```

At +16.8 V, the 1% resistor-only corner bounds are **2.6472 V off** and **2.0713 V on**. Including1.7% resistor/temperature corners, ±2µA off-input leakage sensitivity and a conservative ±0.25µA powered leakage/error envelope gives **less than2.74 V off and2.11 V on**. The powered envelope is an engineering allowance, not a newly invented manufacturer guarantee. Both are below 3.0 V, including the transition into the powered specification at VDD=1.5 V. Maximum calculated R8 dissipation is 1.23 mW; its 0.1 W/ordinary 0603 rating is ample. For a simultaneous positive excitation and −16.8 V ID fault, R3 dissipates at most approximately 43 mW and sees less than 34 V; retain the specified voltage/power rating and temperature derating. Normal ID resistor dissipation is only milliwatts. These are circuit calculations, not fault measurements.

R19 bounds the specified U21 powered-off leakage of ±2 µA to ±0.204 V with 1.7% initial/temperature allowance at the specified VDD=0 condition. That DC bound does not establish rail-ramp isolation timing; startup, brownout and abrupt supply loss remain oscilloscope qualification gates before fitting/using the MCU. There is no resistive ID path to V3V3. D22's 80 nA maximum reverse leakage at 150°C/75 V adds at most 0.8 mV to the prior PACK_PROT USB-only leakage bound: 0.5008 V, Q1 base ≤0.2504 V. [Nexperia BAS116](https://assets.nexperia.com/documents/data-sheet/BAS116.pdf).

At −16.8 V, R8 limits current below 0.1 mA. D23 specifies ≤0.24 V forward drop at 0.1 mA and 25°C, leaving the TMUX and ESP32 negative absolute limits unexceeded in that stated test condition. A 0.29 V cold/continuous sensitivity is included; it is **not a manufacturer full-temperature guarantee**. Negative-fault clamp voltage, diode temperature behavior and rail-collapse transients must be measured with bounded energy before fitting/enabling the MCU. With the battery present, its PACK_PROT source also supplies the small D22/R3 current. With the battery absent and an independent negative ID source attached, that branch can pull PACK_PROT below ground: existing unidirectional D2 then conducts forward. Do not model the unpowered PACK_PROT node as an ideal0V source. A−1.0V PACK_PROT sensitivity would give BAT_DIV approximately−91mV and Q1 base approximately−0.5V; these are estimates, not guaranteed D2 forward limits. Measure PACK_PROT, BAT_ADC and PACK_ID_ADC together during the staged negative fault before fitting U10/U21. Positive ID backfeed is blocked by D22; negative-current return through D2 is a different case. Recommended normal input range remains nonnegative. [BAT54H package, pinning and characteristics](https://assets.nexperia.com/documents/data-sheet/BAT54H.pdf).

## Identification and fail-safe behavior

Ratiometric decoding uses measured PACK_PROT from the existing 470 kΩ/47 kΩ divider. The two-node model includes the external code resistor, all four1% resistors with temperature allowance, D22 forward drop, D23/input leakage, and calibrated ADC error. The unqualified component envelope can overlap codes; **a nearest-code decoder is forbidden**. The host fixture requires an explicit qualified calibration record, computes possible codes, rejects ambiguous observations and then cross-checks pack voltage and RF-module population. No default calibration is installed.

The illustrative qualified-process bounds are D22 VF 0.4–1.0 V, leakage ≤0.2 µA, ADC error ≤10 mV and PACK_PROT measurement error ≤100 mV. These are commissioning acceptance requirements, not manufacturer-guaranteed diode characteristics. The numerical and host reports include the100mV sense allowance and independent1.7% resistor corners (1% initial plus100ppm/K over65K, rounded outward) across−40..85°C. External ID resistors must meet the same tolerance/TCR envelope. The minimum calculated interval separation is approximately13mV at the low-voltage endpoint. Confirm the bounds across the intended operating temperature range before permitting RF. A failed qualification leaves the identity invalid and INIT_OK inactive. Record actual ADC transfer, diode behavior and reference resistor readings; do not simply assert the calibration flag.

PACK_ID ADC1 uses **ATTEN1/2.5dB** with calibrated readings. Reject saturation and values≥0.93V before comparing codes. With the stated corner/calibration envelope, normal codes span approximately0.109–0.893V across the full analyzed voltage span; the8.4V conductor fault is above the acceptance ceiling. The larger27k excitation resistor prevents an8.4V fault overlapping the4S window at the upper battery limit. The [current ESP32-S3 datasheet, table5-6](https://documentation.espressif.com/esp32_s3_datasheet_en.pdf) specifies calibrated ATTEN1 error±6mV over0–1.1V at25°C,100nF input capacitance and Wi-Fi disabled. This supports the selected range; it does not establish the complete10mV/error-temperature budget. Qualify the actual board and reject readings when the channel setting/calibration is wrong. ADC clipping is an invalid measurement, never a nearest valid identity.

Open, GND-short, +8.4 V and +16.8 V faults are rejected by the actual numerical reader. A wrong code/voltage combination is rejected. Wait ≥40 ms after stable power or ID transition, take repeated consistent samples, and revalidate with meaningful application progress. An invalid or changed identity withdraws INIT_OK/ARM and latches a fault; deliberate recovery is required. The local RF lease/progress watchdog remains independent. USB-only operation cannot satisfy PACK_PRESENT or pack identity.

The audit covers defined conductor faults relative to controller GND. Arbitrary connector permutations, loss of ground, shorts bypassing the fuse, and an earth-referenced USB cable across a reversed external pack are not covered by an ID divider. Retain keyed harness construction, external pack protection and branch fusing.

Reproducible values, fault rows, sensitivity inputs and tests are in [input-protection.json](../hardware/controller/review/M6-C1R1/input-protection.json), generated by `tools/m6_c1r1_electrical.py`. Physical measurements remain NOT_RUN.
