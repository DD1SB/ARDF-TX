# M6-L2 FoxPro2 compatibility protocol

This specification and the C11 implementation are independently written for ARDF-TX. The technical references are Nick Roethe / DF1FO's original [FJTX.asm](https://df1fo.darc.de/ASM/FJTX.asm), [FOXPRO2.asm](https://df1fo.darc.de/ASM/FOXPRO2.asm) and [Zeitsteuerung2G.doc](https://df1fo.darc.de/DOC/Zeitsteuerung2G.doc). Both assembler sources were read, including their receive/send paths, command handlers and FoxPro protocol states. Their retrieved versions and hashes are recorded in the review source register. The complete originals remain outside this public repository. **They are not claimed to be MIT-licensed.** First-generation FoxPro is incompatible and is excluded.

## Wire format

The bus is shared, bidirectional and open drain. A released bus is HIGH when the independently powered FoxPro is connected. Frames contain LOW start, 16 data bits, HIGH stop: exactly 18 bit periods at 1200 baud, nominally 15 ms. This is not UART 8N1. The first byte's high nibble is the checksum; its low nibble is the command/address. The second byte is data. Transmit bit 15 first and bit 0 last.

For command nibble `c` and data byte `d`, checksum is `(c XOR (d >> 4) XOR (d & 15) XOR pattern) & 15`. Pattern is `0xA` toward the transmitter, `0x5` toward FoxPro. The assembled word is `checksum<<12 | c<<8 | d`. Examples independently calculated from the format: read FoxID request `EF0B`; response for FoxID `71` is `8B71`. Writes have no protocol acknowledgement. Readback is required.

`fp_receive_tick` samples at 4800 Hz, validates the start and stop, and shifts sixteen bits MSB first. Invalid checksums never reach command processing. A framing error waits for an idle interval before accepting a new start. A stopped sampler cannot complete a frame; reset discards partial state. The ESP32 transport reference supplies an exact-average 80 MHz APB interval sequence of 16667,16667,16666 cycles. Four sampler ticks form one bit; twelve ticks take exactly 2500 µs. Target clock locking and ISR/task latency remain physical/target qualification work.

FoxPro advances protocol steps at about 30 Hz (33⅓ ms). The transport leaves one bit interval after stop-centre reception before starting a response. Request plus turnaround plus response fits within that cadence. The transport suppresses its receive decoder while sending and detects a released HIGH externally pulled LOW. Four checksum bits and wired-AND signalling cannot distinguish identical concurrent transmissions, and some multi-bit collisions can produce a valid checksum. Connect one transmitter at a time, perform semantic readback, and treat mismatch or timeout as failure. No unsupported collision-detection guarantee is made.

## Registers and operations

| Request | Semantics implemented |
|---|---|
| 0–9, data | Stage the corresponding status byte; only a complete, valid ordered load is imported atomically |
| A, data | Bounded protected test request; zero cancels |
| B, data | Stage FoxID/speed/modulation and its virtual EEPROM byte 0 |
| C | Unsupported legacy oscillator output; no RF operation and no success response |
| D, data | Select virtual EEPROM address |
| E, data | Stage CW-ID byte at addresses 1–18, then increment |
| F, 00–09 | Read a coherent native scheduler/RTC status view |
| F, 0A | Read accepted test timer, zero when inactive/rejected |
| F, 0B | Read FoxID and reset EEPROM pointer to 1 |
| F, 0C | Read compatibility feature floor `15` |
| F, 0D | Read the authoritative RTC subsecond phase scaled to 0–29 |
| F, 0E | Read virtual EEPROM at pointer, then increment |
| F, 0F or larger | Unsupported; no fabricated response |

Read responses put the requested register number in their command nibble and use the response checksum discriminator. `15` identifies the supported FoxPro2 feature floor, not authorship by DF1FO, a production firmware version, or implemented oscillator calibration. Native diagnostics must identify ARDF-TX and expose rejected/unsupported counters. No unused legacy bits are assigned ARDF-TX extensions.

FoxID has format `SSMM0FFF`: speed indexes 0–3 represent 72,60,51,45 BpM; modulation indexes represent 1200,800,600 Hz or A1; fox numbers 0–7 have the original MO/MOE…MO5/long-pause MO/S meanings. Bit 3 must be zero. Native module/profile capability validation remains authoritative before using any modulation or enabling RF. Reading and writing these configuration values does not transmit.

The ten-byte status representation is:

| Byte | Contents |
|---|---|
| 0 | Time of day in ten-minute units, 0–143 |
| 1 | Search/follow-on flag bit 7; highest fox number bits 6–4; minute units bits 3–0 |
| 2 | Slot-duration index bits 7–6 (60,30,15,12 s); seconds bits 5–0 |
| 3 | Mode bits 6–4 (prestart,test1,test2,contest,finished); current fox bits 2–0; other bits zero |
| 4,5 | Test 1 start/end in ten-minute units; paired FF means disabled |
| 6,7 | Test 2 start/end; paired FF means disabled |
| 8,9 | Contest start/end in ten-minute units |

Highest fox 1 represents Foxoring; ordinary Classic and Sprint use the corresponding slot duration and up to five foxes. Equal enabled test start/end retains the special ten 15-second test passes. Midnight-crossing schedules are allowed; a zero-duration contest and invalid ranges/combinations are rejected. Native configuration preserves features the legacy representation cannot express, including date, module identity, frequency, power, regulatory policy, LoRa and all commissioning evidence. Loading a legacy program never arms the transmitter.

## Time, configuration and safety integration

There is one authoritative application RTC and one native scheduler. The protocol does not run an independent ticking clock. Command 0 records the external RTC receive time, clears staged status/test timing, and starts an ordered ten-byte transaction. On byte 9, validation and the application's `program` hook atomically import the schedule and requested time-of-day at the load's elapsed phase. The hook must require a disarmed configuration state, preserve the current date under native policy, validate the RTC write/readback and reject atomically on failure. Arbitrary serial time writes never grant an arm/rearm transition.

The application's `status` hook projects its actual scheduler and RTC into the ten-byte representation. A read of byte 0 captures a snapshot; ordered reads of bytes 1–9 share it, with a 900 ms limit. FoxPro's normal verification starts around the middle of a second and compares the complete status. Its clone sequence first polls the 30 Hz phase for 0 or 1, then reads status. This representation avoids failures caused merely by ESP32 epoch/date storage differing from the ATtiny registers. Interrupted loads time out after one second and never partially update the scheduler. Clock discontinuity invalidates pending state. The host scheduler fixture exercises the legacy calendar/slot view; actual RV3032 integration remains target work.

Virtual EEPROM is exactly 19 bytes: byte 0 FoxID, bytes 1–18 CW-ID. The first CW byte contains position/speed/disabled parameters, the next duration, then sixteen encoded Morse bytes. The payload uses the legacy encoded-byte representation rather than inventing ASCII on the wire. Reserved control bits, duration and all indices are validated. Out-of-range accesses neither touch adjacent memory nor wrap into configuration byte 0. A fresh D=1 begins a new CW transfer. F/0B resets the read pointer to 1 as the original workflow requires.

Writes are staged for immediate protocol readback. Only a complete valid CW transfer or valid FoxID update reaches the configuration hook after 500 ms quiet. Incomplete or invalid transfers roll back. Persistence calls are limited to one per ten seconds after the first commit; the application must use its normal atomic configuration storage and handle reported failure. Reset discards staging. This avoids per-byte flash writes and prevents EEPROM pointer misuse from modifying native safety data.

Test codes 1–15 request 0.1-second carrier units; 16–17 request 15/30-second identification tests. Larger minute-style legacy requests exceed the 30 s limit and are rejected, not silently shortened or reported successful. An accepted test requires the native arm/rearm controller's authorization, a known selected RF module, valid battery ID, profile, PA/thermal/protection evidence, commissioned antenna/dummy load and USB restrictions. `test_safe` is rechecked during polling. A monotonic deadline cancels the test even if wall time changes. The compatibility core never writes RF-enable GPIOs or substitutes timer activity for application-owned progress. Oscillator calibration remains unsupported because generating the old CPU-clock output would be misleading and could invoke an unsafe RF path.

The C11 files are `firmware/controller_hw/foxpro2.{h,c}` and `foxpro2_transport.{h,c}`. The small pin adapter uses HIGH-idle GPIO43 transmit (LOW requests a SAFE-qualified sink) and inverted GPIO44 receive through the optional hardware. Its reference tick executor is host/task code; an ESP-IDF integration must queue complete frames from an IRAM-safe sampler/RMT implementation and run application callbacks in a task. It is not claimed to be a complete ESP32 contest firmware or a latency-qualified ISR.

`test_foxpro2.py` provides an independent timed peer against the compiled C implementation, exhaustive command/data/checksum vectors in both directions, negative line/transaction tests, normal identify/load/verify/clone/CW workflows, protection tests and persistence bounds. The complete relevant controller host suite is rerun in the revision package. Target timing under load and physical interoperability with a genuine FoxPro2 are **NOT_RUN**.
