# Mini80 universal AVR firmware

`main.c` targets ATTINY1616-MNR directly with AVR-LibC/device-pack headers. `core.c` contains the portable scheduler, settings validation, Morse sequencing and Si5351 register calculation. `power.c` is the RF/envelope state machine used by the target and host tests. One image supports all twelve roles; examples contain per-unit data, not twelve firmware builds.

## Build and verification

Use AVR-GCC with ATtiny1616 support and Microchip ATtiny DFP headers/startup libraries. The review build used AVR-GCC 7.3.0 and Microchip ATtiny_DFP 3.4.278; toolchain/vendor files are external, not included or relicensed. `make all test` uses `avr-gcc`, `avr-objcopy`, `avr-size` and host `gcc`. For an external extracted pack:

```sh
make AVR_PREFIX=/path/to/avr/bin/avr- DFP=/path/to/ATtiny_DFP all test
```

The [saved build/test log](../review/firmware/build-and-test.log), [universal Intel HEX](../review/firmware/mini80-universal.hex) and ELF support review. Hardware programming/execution has not occurred. The build uses `-Wall -Wextra -Werror`. Host tests exercise the actual shared core/power modules; they do not simulate AVR peripherals, analog envelope behavior or radio emissions.

Before programming, verify the device signature and exact package/pads. Use a suitable UPDI programmer with the **battery-powered target at 3.0 V logic**, a common ground and current limiting. J2 V3 is sense only; do not connect an independent programmer power output against the onboard LDO. Retain PA0 as UPDI. Select/read back the symbolic fuse settings: internal oscillator **20 MHz**, BOD **2.9 V active** with suitable standby sampling, reset/UPDI function retained. Main divides 20 MHz by four to 5 MHz. No unverified raw fuse byte is supplied. Firmware enables a nominal two-second watchdog; it is fed only when the external RTC ticks advance. A failed timing crystal consequently resets to hardware RF-off defaults.

## Pogo fixture

J2 is six bottom pads at 2 mm pitch; see the native PCB and assembly drawing for pad numbering and orientation. The B.Silk legend identifies:

| Pad | Signal | Connection |
|---|---|---|
| 1 | GND | Fixture/programmer ground |
| 2 | V3 | Target voltage sense, not an external power input |
| 3 | UPDI | Programmer data |
| 4 | FIX_RX / PA2 | 3 V UART fixture TX |
| 5 | FIX_TX / PA1 | 3 V UART fixture RX |
| 6 | SYNC / PA3 | Common 3 V rising edge; normally low |

Use 9600 baud, 8 data bits, no parity, one stop bit, no flow control. A programming adapter may implement UPDI with the normal appropriate interface; the PCB does not contain a USB bridge or bulky programming header. Legacy FoxPro2 is not implemented; a future external adapter would translate its timing/configuration protocol.

Workflow for twelve units: program and verify each with RF unarmed; write unique settings and read back exact bytes; explicitly ARM each; connect common ground/SYNC to all devices with SYNC initially low; deliver one common rising edge; disconnect fixture and deploy before the configured start delay expires. Do not join all V3 rails or all TX outputs. Use individually selected UART channels or configure sequentially while maintaining access to the shared SYNC line. A longer deployment delay is configurable.

After synchronization the MCU uses standby between RTC interrupts. UART wake/reception is **not guaranteed** in that state. For service, use a programmer reset/power cycle, which clears ARM/SYNC, then reconfigure. The unit remains autonomous after fixture removal.

## Configuration and protocol

`fixture.py fleet examples` generates twelve offline settings files. This command does not contact hardware. For one custom file use `fixture.py encode input.json output.bin`. `read`, `write`, `arm` and `stop` serial subcommands require explicit selection of a port and installed `pyserial`. **These commands have not been used on hardware during this development.** `write` verifies a byte-for-byte readback.

Settings are little-endian, packed, 45 bytes; CRC-16/CCITT polynomial 0x1021, initial 0xffff, no final XOR, covers all bytes before the CRC. `mini80.h` is the format authority:

| Field | Format / validation |
|---|---|
| magic, version | uint32 0x314d3830, uint8 1 |
| role | uint8 0–11: slow five, fast five, S, MO |
| mode | uint8 0 Sprint, 1 Foxoring, 2 independent continuous |
| profile | uint8 0 MINI50, 1 FOX10; must match physical eight-resistor population |
| slow_wpm, fast_wpm | uint8 each 8–15; defaults 10 and 15 |
| identifier | uint8 0..6 = MOE, MOI, MOS, MOH, MO5, S, MO |
| frequency[4] | uint32 Hz each; slow, S, fast, MO; 3,510,000–3,600,000 |
| delay_s, run_s | uint32 each 1–86,400 seconds |
| carrier_ppb | int32 −100,000..100,000; measured reference error in ppb |
| timing_ppm | int16 −200..200; measured RTC frequency error in ppm |
| battery_scale | uint16 4,200..4,800 mV full-scale, nominal 4,500 |
| crc | uint16 |

Positive calibration values describe an oscillator that runs fast. The carrier divider uses the corrected reference estimate; time uses `raw_ticks / (1 + timing_ppm/1e6)`. Carrier and RTC corrections are independent. Battery calibration describes the combined ADC/reference/divider gain, not a cell chemistry setting.

Frame layout is `A5 command payload_length payload CRC16_LO CRC16_HI`; CRC covers the header and payload. Commands: 1 WRITE (45-byte settings), 2 READ (no payload), 3 ARM (no payload), 4 STOP (no payload). Replies use `command | 0x80`; READ returns the settings, other replies one status byte (0 accepted, 1 rejected). Bounds, malformed frames, overrun, bad CRC and timeout have conservative RF-off handling. EEPROM is invalidated before a new write and read back afterward. No armed state is saved. **Invalid/blank EEPROM cannot be armed** merely by accepting the RAM fallback defaults; a valid persistent configuration must first be written.

Sprint settings require every configured frequency pair to differ by at least 20 kHz. Foxoring requires FOX10 profile, roles 0–9, IDs MOE through MO5 and at least 30 kHz from the configured external normal-power finish frequency. `examples/foxoring-MOE.json` demonstrates a 24-hour run. Other field frequencies may be selected per unit. Normal-power finish operation is outside this hardware.

## Timing and RF state behavior

Y1 drives the RTC at 32,768 Hz, divided to 128 interrupts/s. A common edge starts a fresh epoch only after ARM. The configured delay and run window are mandatory. Five exact nominal 12-second windows repeat every minute; identifiers start after a one-second guard and must finish before the one-second ending guard. Whole identifiers only; no clipped last letter. Three minutes of all-role sequencing and a final-minute simulation with opposite ±20 ppm errors after twelve hours are regression-tested, including two ticks of RF tail. The two-second combined guard exceeds the calculated 1.728-second relative drift plus tail/quantization. This requires a physically verified total residual RTC error ≤20 ppm over the intended temperature range; otherwise shorten the session or resynchronize. The oscillator tolerance alone does not establish that bound.

Morse dot time is 1.2/WPM seconds; cumulative rounding prevents one-tick rounding error from accumulating per element. Interelement/letter/word gaps are 1/3/7 units. S and MO repeatedly send their IDs without minute slots. Foxoring repeatedly sends its configured field ID throughout the scheduled run.

Power sequence: hardware RF/envelope/boost/clock defaults off → validate persisted configuration → ARM → SYNC → scheduled preparation (~500 ms lead) → boost rail check → clock supply/PLL configuration and lock → enable CLK0 and RF output only for a mark. Retuning always calls the inhibit/power-down path first. Key-off drops the envelope and waits two RTC ticks (15.625 ms), then inhibits the HCT and clock. Idle slots remove boost and synthesizer power. Faults bypass the smooth tail and remove RF immediately. Low battery below 3.2 V latches off; re-ARM needs at least 3.4 V. A watchdog/brownout/reset also requires a new ARM and SYNC.

The synthesizer uses PLLA at nominal 800 MHz and fractional MS0 with denominator 1,048,575; registers follow [Skyworks AN619](https://www.skyworksinc.com/-/media/Skyworks/SL/documents/public/application-notes/AN619.pdf). Disabled outputs are commanded low. Host decoding tests 361 frequencies and rejects out-of-band inputs. This does not measure actual crystal frequency, phase noise, spurs, lock timing or RF duty cycle. AVR peripheral behavior, fuse programming, brownout thresholds, serial fixture operation and first-article timing remain physical validation tasks in [FIRST_ARTICLE.md](../FIRST_ARTICLE.md).
