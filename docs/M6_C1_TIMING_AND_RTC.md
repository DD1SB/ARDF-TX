# M6-C1 — timekeeping and waveform resources

RV-3032-C7-32.768KHZ-2.5PPM-TA-QA is the selected compensated RTC. Manufacturer accuracy is±2.5ppm over−40..85°C. Initial drift bound is0.216s/day; adding a3ppm first-year aging allowance gives0.475s/day. With an assumed±0.25s synchronization error, the calculated24h budget is0.735s including10ms RTC-register quantization. Verify the actual applicable event's≤5s transmitter-timing and≤1s clock-reference requirements. Daily synchronization is the proposed practice; longer holdover, USB setting accuracy and outdoor temperature behavior remain physical tests.

| Candidate | Timing evidence | Selection |
|---|---|---|
|PCF85063-class crystal RTC|inexpensive, uncompensated crystal tolerance/temperature;20ppm alone1.73s/day|insufficient unqualified1s/day margin|
|DS3231|compensated, approximately±2ppm near room temperature; larger SOIC and higher unquoted cost|credible alternative, not selected|
|RV-3032-C7|±2.5ppm industrial range; integrated crystal; observed€2.75 at10|selected|

The primary CR1220 holder feeds VBACKUP through BAS116 and1k. The diode prevents charging the primary cell even if the RTC's charger configuration is accidentally changed. VBACKUP/GND are pins1/5; SDA2, INT3, EVI4, VDD6, CLKOUT7, SCL8. The metal lid is ground. The local land pattern mirrors the manufacturer's **bottom-view** pin diagram into the PCB top view;0.5×0.8mm lands,0.9mm pitch and0.4mm inter-row gap. No via filling is required.

Factory EEPROM has backup switching disabled. Commission **BSM=10 (level switching), TCM=OFF**, disable unnecessary CLKOUT and read the settings back. Configure with VDD present and observe the manufacturer's settling requirement before testing transfer. A newly inserted backup cell alone does not prove initialized timekeeping. POR/voltage-low/invalid BCD/date or failed communication prevents event arming. Backup keeps wall time; it does not retain permission to transmit after reset. Coin-cell lifetime and minimum backup voltage must be checked with the selected actual cell and diode drop; no battery-life measurement is claimed. Commission the primary cell at≥2.5V and verify actual VBACKUP against the RTC minimum during main-supply loss; replace a depleted cell rather than assuming its nominal3V remains available.

RTC shares I2C0 with the *host side* of the disabled RF80 branch. INT is unused; firmware reads the RTC hundredths/time registers for discipline; S3 hardware timers execute subsecond scheduling. RTC reads cannot clock an armed RF80. Clock correction must not extend an active slot: freeze the current monotonic deadline, apply small corrections off-slot and disarm for invalid/large corrections requiring reapproval.

## PWM and keying

ESP32-S3 has no original-ESP32 analog DAC. Two low-speed LEDC channels share timer0 with an APB power-management frequency lock (no dynamic clock changes):80MHz/256 gives **312.5kHz at8bits**, matching RF2M's existing contract. A separate GPTimer resource at1MHz provides32µs sampling (31.25kHz). Phase-accumulator sine generation supports a configurable tone, initially800Hz; frequency resolution is about7.28µHz. A target ISR must use an IRAM/RAM LUT and bounded peripheral writes; the supplied `sin()` C reference is explicitly a **host fixture**, not ISR code.

RF2M reconstructs LEVEL DC and AF DC+sine through its existing10k/4.7nF sections, approximately3.386kHz, Q0.5. Calculated800Hz gain is about0.947; calibration compensates it. Approximate312.5kHz attenuation is78.6dB for the ideal section. PWM quantization after ideal2.8×gain is about10.5mV RMS. Component tolerances, digital update artifacts, analog stability and RF-envelope transfer require measurement. The unfiltered bench examples110±82 and61±49 codes are **not** RF power/AM calibration values. At800Hz, an ideal75% sine after this filter needs about87 amplitude codes around110;80% needs about93. Those values still fit the8bit range, but actual supply/RF transfer must be calibrated.

KEY switches matching DC and sine on the RF board, with approximately3ms ramps and phase-coherent transitions supplied by firmware. SLOT controls scheduled carrier presence. Keep frequency and driver operation stable while the final supply carries genuine sinusoidal AM. Carrier ERP,70–80% depth, PEP and spectral purity are properties of the measured complete transmitter, not of a PWM formula.

A separate timer/RMT resource is reserved for deterministic Morse and slot edges: one dit is150000µs at8WPM or80000µs at15WPM;1µs quantization is negligible. SPI, LoRa and USB work must not run in that timing ISR. The host SOS fixture checks edge arithmetic; ESP interrupt latency under load is NOT_RUN. One station executes its assigned Classic/Sprint/Fox/beacon role; two Sprint groups exist across the fleet. Frequencies remain configurable and independently subject to legal/event/calibration allowlists.

The application toggles GPIO39 every25ms **only after meaningful control progress**. Complete waveform is20Hz; both rising and falling edge intervals are50ms. This satisfies RF80's rising-edge lease and RF2M's falling-edge progress contracts. Neither a free-running PWM nor a still-running Morse ISR is permitted to stand in for software health.

Sources: [Micro Crystal manual Rev1.3, pin map/backup/package](https://www.microcrystal.com/fileadmin/Media/Products/RTC/App.Manual/RV-3032-C7_App-Manual.pdf), [Espressif LEDC](https://docs.espressif.com/projects/esp-idf/en/stable/esp32s3/api-reference/peripherals/ledc.html). See generated timing JSON and the firmware foundation's README for test limits.
