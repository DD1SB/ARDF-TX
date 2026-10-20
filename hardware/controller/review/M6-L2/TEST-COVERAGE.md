# Reproducible test coverage and limits

`host-test-results.json` contains the complete commands, output and return codes for 75 Python host tests and the strict C11 controller fixture. Twenty-nine tests in `firmware/controller_hw/test_foxpro2.py` exercise the separately compiled C implementation through `test_foxpro2_bridge.c`. Expected frames are constructed in the Python peer independently of the C encoder. Both directions exhaust all 16 commands × 256 data values; known literal words and every single-bit corruption provide additional checks.

| Requested behavior | Host test suffixes |
|---|---|
| Exact 1200 baud, start/stop, 16 MSB-first bits, checksums | 01–05 |
| Incomplete frame, reset, held LOW, stuck HIGH, simultaneous drivers | 06–09, 22, 27 |
| Interrupted request, readback timeout, approximately 33 ms cadence | 10–12 |
| Status read/write and coherent program verification | 13, 25 |
| Classic/Sprint/Foxoring FoxID representation | 14 |
| CW-ID limits/round trip and bounded persistence | 15–16, 29 |
| EEPROM pointer increment and read/clone | 17–18 |
| Invalid programs and unsupported calibration/commands | 19–20 |
| Unsafe/disarmed test requests and unknown RF/USB-only state | 21, 24, 28 |
| Boot UART isolation, inverted receive and response turnaround | 23, 26 |
| RTC phase/full-second view, monotonic test deadline and live fault cancellation | 25, 28 |

The peer models a wired-AND bus. Conflicting different frames are detected where observable; two identical simultaneous open-drain transmissions cannot be distinguished electrically. Stuck HIGH is absence of frames, not proof that a device exists. Timing tests verify rational timer-cycle scheduling and bit/sample ordering; they do not measure an ESP32 ISR.

`L2-native-negative-regression.json` records 32 mutations of actual native objects, not report text. These cover PSRAM substitution, missing GPIO35–37, pin orientation, antenna access, straps, direct overvoltage receive routing, wrong open-drain connections, missing hardware inhibit, unsafe emitter gating, off-state backfeed, raw battery export, TRS mapping, address conflicts, RTC isolation, GPIO-to-RF connections, RF connector changes and LoRa geometry. `FoxPro-GPIO-electrical-calculations.json` derives numerical corner bounds from actual resistor values and package identities. `L2-bus-power-layout-calculations.json` adds actual routed copper length, via counts and explicit capacitance/load scenarios.

Inherited electrical, protection, USB, power-path, RF protocol and DFM mutation suites remain required. Their reports retain all 36 RF connector contacts, 4,096 hardware enable combinations, historical critical package maps, LoRa TR4/TR8 maps and RF-feed geometry. The new native audit separately checks every historical pad and frozen RF/review file. ERC/DRC and schematic parity are evaluated by KiCad itself.

The application hooks are exercised with a fixture, not a complete contest application. Persistence storage backend, final RTC/scheduler mapping, target timer/IRAM implementation and actual RF test permission must be integrated and measured before assembled operation. No calibration output, RF transmission or hardware interoperability result is fabricated. All physical USB/boot, FoxPro, voltage fault, accessory, antenna/coexistence, thermal, ESD and power-sequencing tests remain **NOT_RUN**.
