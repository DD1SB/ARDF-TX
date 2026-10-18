# M6-L1 hardware contract foundation (M6-C1R1 electrical baseline)

This directory contains host-executable state/timer fixtures, the generated physical GPIO/shift-register contract and a small C waveform reference. It is not operating firmware and does not connect to hardware.

Run from this directory:

```
python3 -m unittest discover -s . -p 'test_*.py' -v
cc -std=c11 -Wall -Wextra -Werror contract.c test_contract.c -lm -o /tmp/m6-c1-contract
/tmp/m6-c1-contract
```

`Context` carries externally validated RTC/pack/module/calibration/frequency evidence. Test booleans are fixtures, not implementations of ADC calibration, I²C readback or module detection. RF80 presence additionally requires a fitted-assembly record and source readback: its low disarmed FAULT signal does not identify an absent module. RF2M resistor identity is decoded separately. USB-only configuration is allowed; arming requires a validated common pack.

The target firmware must implement separate RF80 and RF2M state machines, atomically latch595 words while sharing SPI with optional LoRa, and establish application-owned20Hz progress. Hardware timers never substitute for that progress. Use two LEDC8bit channels at312.5kHz with an80MHz APB frequency lock, a31.25kHz DDS update timer and a separate1MHz key/slot timer or RMT. Replace the C `sin()` reference with an IRAM/RAM LUT before target ISR use. Timing under USB/LoRa load is NOT_RUN.

GPIO37 is inverted USB VBUS presence; poll RTC wall time over I²C. RTC INT is unconnected; read its hundredths/time registers on the host bus. Initialize RV3032 backup BSM=10, charger OFF, CLKOUT disabled and validate readback/POR/time. USB PHY must detach while VBUS is absent. Read a trusted fitted LoRa population record and separate chip status; chip status cannot distinguish433/868. Absence is normal. Remote commands pass the same frequency, timing, pack and fault validation as local/USB commands.

Frequency allowlists are provisioned for the actual country/operator/event and qualified RF calibration. IARU event ranges are additional restrictions, not a transmission licence. Clock corrections never extend a live monotonic slot deadline. Physical RF, thermal, battery, USB and electrical behavior remain NOT_RUN.

Normal RF2M slot entry additionally requires an explicit `pa_rail_valid` fixture; live rail loss disarms. On target this must come from a fresh calibrated PA_RAIL_ADC sample and the commissioned converter/profile range, not a constant boolean. Training requires no watt rail and retains PA_PREPARE low. Host tests cannot establish actual ADC scaling, settling or fault timing.

M6-C1R1 changes only pack identification: frontend revision2 uses protected-pack excitation and180k/33k attenuation, with100k ADC load. `identify_pack` requires an explicit qualified calibration record and rejects ambiguous codes, wrong frontend versions, invalid voltage and absent3.3V. The fixture bounds are not physical calibration data. Confirm the record across the intended temperature/voltage range before INIT_OK; revalidate fresh samples with meaningful progress and latch a fault on identity loss. The legacy3.3V-pull-up equation must not be used. USB/RF GPIO allocation and C waveform/control interface are unchanged. See docs/M6_C1R1_INPUT_PROTECTION.md and the staged review bring-up.

R1 PACK_ID uses27k pack-derived excitation,180k/33k protection and100k switched-side loading. Select calibrated ATTEN1/2.5dB on GPIO2; reject saturation and>=930mV before the interval decoder. External10k/22k identities remain. The example calibration record is not measured evidence and cannot be used as a production default. The10mV ID and100mV PACK_PROT error allowances require qualification across the intended temperature range.

M6-L1 adds the optional-radio contract in `lora.py`: NONE, SX1262TR4_GC_433 or SX1262TR8_GC_868. Unknown/inconsistent band, antenna, commissioning, frequency/power or airtime evidence disables LoRa TX. A radio outage does not invalidate autonomous ARDF operation. The46 host tests retain all40 R1 tests. This is no LoRa protocol stack and sends no hardware commands. Exact assembly record, firmware bus locking and all physical RF behavior remain commissioning work.
