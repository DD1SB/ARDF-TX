# M3A-R1 — supporting-circuit simplification

Date: **2026-10-14**. Status: review proposal. Counts and costs come from the current manifest/workbook and Git-tagged R0; [generated delta](M3A_R1_COST_DELTA.md) contains every introduced, removed and modified reference. Prices are EUR net and often estimates. A footprint, test pad or multiunit gate drawing is not a separate IC purchase.

## Implemented simplifications

1. **Delete U213 HC08, U214 HC32 and C221/C223.** Replace duplicated permission aggregation with one two-stage HC21 core, spare gate bus qualification, wired open-collector PA guards and six Schottky qualification diodes. This reduces two packages, while preserving separate common UV and request-conditioned watt guards. Diode voltage/current/temperature margins remain mandatory physical checks.
2. **Remove five separate PA trip pull-ups** R320/R322/R323/R341/R342. LM339/LM393 open collectors now share R321 and PA_GUARD_RAW; each individual trip is exercised. Fault cause encoding is a controller/external-test convenience, not required local circuitry. Fault status remains an open-drain unarmed indication.
3. **Move common UV to U314's retained dual comparator; make U312 watt-only.** Fox omits the LM339, thermal/reference divider hub, PA-only reference branches and decoupling: references are enumerated in the population delta. R228 grounds the unused watt guard, and R348/R349 bias the unused U314 comparator input pair. R336 is removed; no dummy PA temperature sensor is needed without a PA. Common TL431/divider/UV remains as an independent pack backstop.
4. **Use the spare U223 half for a heartbeat witness** and spare HC14 gate for KEY-low qualification. No extra startup watchdog IC, one-shot or MCU is added.
5. **Replace U224 HC74 with one HC174** capturing path, mode and key-low acceptance together. This package is present in Fox too: after deleting two common gate packages and one watt-only comparator, Fox's new context latch is still justified by the confirmed pending-clock/path-transfer defects. Request-withdrawal sinks are shared across populations; they do not introduce a product-specific fourth board.
6. **One shared key tail**, raw KEY input, strengthened 100 Ω asynchronous discharge. Driver and Fox independently AND their captured permit with that tail. No redundant per-path timer is added.

## Functional block dispositions

Purchased counts are fitted physical parts, excluding pads/flags, at identical scope. Block prices are quantity-ten per board; observed/estimated distinction remains in the workbook.

| Block | Class / distinct function and overlap | Full / Fox parts; EUR full / Fox | Final disposition / removal consequence |
| --- | --- | --- | --- |
| Source | Essential RF performance: local Si5351/crystal; central ESP32 owns scheduling, RTC and UI | 2/2; 1.788/1.788 | Retain; duplicate MCU/RTC/EEPROM absent |
| Fixed-rail decoupling | Essential RF performance and digital integrity | 18/15; 0.510/0.438 | Remove deleted-package bypasses only; bulk/fast bypass retained |
| Interlocks | Essential independent protection: local POR, verified-progress lease, bus quiet, raw-edge context, fault clear, path mute and one tail | 35/34; 3.243/3.351 | Gate packages consolidated; deleting witness/context restores demonstrated unsafe transitions |
| Protection | Essential independent protection: local UV, PA OV/OC/thermal window, bounded Fox supply/pad and input protection | 52/27; 3.519/1.518 | PA-specific comparisons/references DNP on Fox; BMS does not cover RF rail/SOA |
| Normal supply | Essential RF performance/protection: one buck, fixed calibrated rails, independent load switch | 16/0; 3.786/0 | PA-only; buck EN cannot isolate a failed shorted converter |
| Normal driver | Essential RF performance plus deterministic INB; bounded driver supply | 13/0; 3.051/0 | LM5134B, bypass, R410/C404 and sinks retained; driver OV response OPEN |
| Normal final | Essential RF performance | 1/0; 0.622/0 | IRF610 unchanged; no cheaper EOL substitution |
| Normal shaper | Essential RF performance: clean CW envelope; sink handles ≈70 mA base current | 6/0; 1.021/0 | BD140/DMN2056U retained; hot repetitive SOA OPEN |
| Normal filter/transformer | Essential RF performance: load transformation and emissions | 10/0; 3.510/0 | Original winding/filter recipe unchanged |
| Fox RF/filter | Essential RF performance/protection: independent supply-following clock, AC00 ballast, LPF, fixed pad, separate mute | 34/34; 2.775/2.834 | DNP-compatible normal branch; hardware current/power shaping still requires measurement |
| Shared supply barrier | Essential independent protection: external protected/fused supply, local reverse barrier | 2/0 in this accounting group; 0.900/0 | Group labels differ from population: Fox's shared input fuse/diode costs reside in protection; no raw-power bypass |
| Connectors | Essential test/field interface; distinct shells, safe harness | 4/3; 1.875/0.875 | No watt-to-Fox switch. Mates/accessories separate; no cost duplication |

The **full population rises 185→193 purchased parts**, but ICs fall **20→18**. Fox falls **128→115 parts**, ICs **15→13**. Full component count increases because R0 lacked valid context/withdrawal/driver-fault protection. Correcting those omissions has priority over a cosmetic count reduction.

## Why retain particular protections?

Pack BMS guarantees neither the programmed PA rail nor hot transistor safety. The common UV backstop protects operation if controller sensing/logic fails; the PA local 4S divider prevents relying solely on PACK4_OK. Comparator outputs can be wired together because they are open collector; CMOS outputs cannot. OC protects PA/shaper/converter load faults faster than a cell BMS may respond. Hot/open/short sensor detection covers detached electrical wiring, but **not physical detachment with intact wires**: attachment/thermal-lag acceptance remains necessary.

TX inhibit is independent of buck enable: INB is pulled to its own rail, and two sinks require PA_PERMIT plus KEY_TAIL. Fox mute forces the NAND enable low; a continuing Si5351 clock then cannot modulate the output in characterized logic conditions. Fixed 27 Ω supply limitation, ballast, pad and compact accessory fault withstand address shaper/buffer faults. No serial RF path or switch can deliver watts to J502 by an enable request. Physical layout coupling, rail backpower and discrete failures still require tests.

R410/C404 add cost to solve a real driver-overvoltage exposure. C404 is Panasonic **25SVPF47M**, 47 µF/25 V polymer, ±20%, specified 30 mΩ at 100 kHz/20°C. Its current-production listing offers cut tape MOQ 1, not a required 1,000-piece reel. Native KiCad `CP_Elec_6.3x5.9` pads agree with the maker C6 land dimensions (outer 9.1 mm, inner gap 2.1 mm, width 1.6 mm). The28 V case stresses the isolated passive network; TPS22810 itself is limited to18 V operation/20 V absolute, so input-clamp coordination remains OPEN. Real transient ESR≤0.5 Ω over 0–50°C and interruption≤20 µs remain OPEN. A cheap wet electrolytic without that demonstrated ESR would invalidate the protective calculation; it was rejected rather than credited as a saving. Maximum capacitor leakage adds up to about 2 mW at the driver rail; no endurance saving is claimed.

BSS138BK replaces low-current sinks for ±20 V gate tolerance and a usable 2.5 V on-resistance specification. DMN2056U remains for Q404's higher current. R409 grounds the driver stack midpoint when inactive. Stacked gate waveforms and diode-recovery currents must still be probed; device DC ratings alone do not qualify transient safety.

## Alternatives investigated and disposition

| Alternative | Potential benefit | Why not substituted in R1 |
| --- | --- | --- |
| One dedicated watchdog/supervisor | Could reduce external lease logic | HC123 already supplies bus timing; spare HC74 witness costs no extra IC. A new watchdog would still need bus quiet, fault-cleared context and deliberate rearm. No basket or timing proof establishes a saving; retain as an unvalidated future alternative, not a second complete design. |
| Firmware-only lease/arming/mode safety | Lower part count | Stuck GPIO/free-running Si5351 or a pending delayed clock can transmit; fails independent fail-off requirement |
| Simple RC health memory replacing context FF | Fewer latch pins | Cannot yet prove fresh-edge recovery after brief faults/path changes or slow rails; confirmed failure exists in old arrangement |
| Omit Fox local UV/reference, rely on BMS/controller | Significant Fox part saving | Removes independent RF-off threshold under controller/pack faults; not accepted without a specified external hardware UV contract |
| Remove OC sensor, trust BMS | Saves INA180/comparator dividers | Cell protection is not RF-stage pulse/SOA protection; no measured mismatch-survival bound supports removal |
| Use only one thermal comparator | Fewer parts | May accept electrically open sensor; proposed window already shares a dual device |
| 74HC175 / Toshiba bargain stock | Cheap four-bit latch | Five captured bits needed; Toshiba current product is NRND. Nexperia HC174 is Production; exact basket remains open |
| AP7384 regulator for driver | More supply isolation | Current listing is NRND; fixed voltages/limited current not a qualified substitute; no extra unquoted LDO selected |
| BJT Fox buffer fallback | Avoid AC00 ramp uncertainties | Retained documented fallback; choose only after measured current/shaping/calibration failure, not speculative parallel product |

System-level operations stay in the ESP32: schedule, frequency readback, profile selection, calibrated output settings, pack identification, telemetry and normal sequence. Optional LoRa stays on the controller. Local power detectors, extra ADC/DAC, config processor and RF-board RTC remain absent. A shared fixture supplies diagnostics rather than charging each unit for permanent instrumentation.

[Cost delta](M3A_R1_COST_DELTA.md) identifies price overruns and estimates. [Verification](M3A_R1_VERIFICATION.md) keeps the remaining safety margins OPEN. No savings are assigned to assembly time, new fabrication or measured idle current.
