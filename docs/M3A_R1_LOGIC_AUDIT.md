# M3A-R1 — RF80 logic audit

Date: **2026-10-14**. Status: **electrical correction for review; unbuilt**. Baseline: Git tag `m3a-r0`, commit `dba9236`. The [current PDF](../hardware/80m/review/RF80.pdf), [XML netlist](../hardware/80m/review/RF80.xml) and [electrical manifest](../hardware/80m/RF80.electrical.json) describe R1. Accepted architecture and VHF are unchanged; ADR-0012 remains proposed.

## Confirmed defects and corrections

The R0 watchdog used **/Q1 pin 4** as positive `LEASE_OK`; the bus inhibit used **Q2 pin 5** as positive quiet. These were critical polarity defects: absent progress could produce a permission, and SCL activity could assert the intended quiet signal. The previous Boolean check accepted those signal names as external inputs and therefore failed to detect the defect. R1 evaluates the actual timer output pins. Mutation tests reject both original polarities and reproduce unsafe no-progress permission with inverted watchdog wiring.

[Nexperia 74HC123, Rev. 13](https://assets.nexperia.com/documents/data-sheet/74HC_HCT123.pdf) specifies Q1=13, /Q1=4, Q2=5, /Q2=12. Its reset-release can trigger a pulse with A low/B high. Merely swapping the outputs would therefore leave another startup problem. A spare U223 flip-flop now records a real rising heartbeat: /Q8=`LEASE_SEEN_N`, D12=3.3 V, CLK11=`LEASE`, CLR13=`POR_N`, PRE10=3.3 V. U202 A1 receives this witness. Before the first edge A1 is high, so a heartbeat stuck high through reset release cannot create permission. A real edge sets the witness and triggers the first lease. [HC74 pin/reset specification](https://assets.nexperia.com/documents/data-sheet/74HC_HCT74.pdf).

Additional findings addressed in the same design:

- A delayed ARM clock could arrive after a transient health fault had cleared. U224 now captures a valid/key-low ARM context on the **raw** ARM edge; health loss asynchronously clears that context. U223's delayed clock can only accept a still-valid context. Recovery with ARM high cannot fabricate a new raw edge.
- Requests were live rather than captured; a new path could inherit a key tail. Path bits are now captured with power bits. Withdrawal of the selected request clears the context through Q225–Q229. The opposite path needs deliberate rearming.
- An unarmed high KEY could charge the tail capacitor near a Schmitt threshold with the old 1 kΩ reset. R453 is now 100 Ω; captured KEY-low acceptance also rejects ARM with KEY high. Raw KEY feeds one tail; no extra one-shot is added.
- Floating stacked switch nodes could stress the old ±8 V gates. Low-current sinks now use **BSS138BK,215 (±20 V gate)** and the driver stack midpoint has R409. DMN2056U remains only for the high-current shaper-base sink.
- Driver VDD directly followed a buck fault until isolation. R410/C404 now slow the driver rise; their quantitative safety limit is a separate **OPEN physical gate**, not a digital proof.

## Physical inputs and positive meanings

| Signal | Physical origin / polarity | Safe startup / effect |
| --- | --- | --- |
| POR_N | U201 pin 1, active-low local reset | Low during startup/brownout; resets both timers and heartbeat witness |
| LEASE | J101 pin 6, rising-edge progress waveform | Local pull-down; must have a genuine edge after reset |
| SCL / SDA | J101 pins 3/5, open-drain, powered 3.3 V bus | Either low inhibits RF; high/high alone is insufficient to arm |
| ARM | J101 pin 7, positive request | Pulled low; low clears ARMED; raw rising edge captures context |
| CW_KEY | J101 pin 8, positive key | Pulled low; KEY high at raw ARM is rejected |
| PA_REQ / FOX_REQ | J101 pins 9/10 | Both low initially; both high invalid |
| PWR0 / PWR1 | J101 pins 11/12 | 00 Sprint, 01 extended, 10 full; 11 invalid; captured at raw ARM |
| MUTE_N | J101 pin 13, low means inhibit | Pulled low; loss clears permission |
| PACK4_OK | J101 pin 15, positive controller validation | Pulled low; PA also requires a separate local voltage check |
| FOX_ID | Compact connector contact/pull-up, high means absent | Compact accessory contact grounds it; blocks PA, not Fox |
| UV_POR_N | U314 pin 1 open collector plus D219 from POR_N | Positive only above local 2S UV and outside reset |
| PA_GUARD_RAW | U312 pins 1/2/13/14 and U314 pin 7 open collectors, D221/222 | Positive only if local 4S, OV, OC, hot/open sensor, PACK4_OK and no compact accessory are healthy |
| FAULT_N | Q201 open-drain status | Low whenever unarmed; not a coded fault diagnosis |

The pack BMS protects cell groups; it does not replace buck-overvoltage, local PA current or attached-sensor trips. UV threshold is nominal 5.810 V **after reverse protection**, local 4S backstop 11.070 V, PA OV 8.973 V, PA OC 1.251 A. Controller operational endpoints remain 6.0/12.0 V raw pack with hysteresis. Comparator offsets/divider/reference tolerances are not bench-qualified.

## Exact timer behavior

| Half / pins | R1 connection | Reset / event / expired |
| --- | --- | --- |
| U202 first A1/B2/RD3/Q13 | LEASE_SEEN_N / LEASE / POR_N / LEASE_OK | Reset Q=0; valid positive B or qualifying falling A triggers/retriggers Q=1; timeout Q=0; /Q4 NC |
| U202 second A9/B10/RD11//Q12 | GND / SCL / POR_N / BUS_HOLDOFF_N | Reset /Q=1, but POR qualification blocks quiet; startup release with SCL high or SCL rise triggers holdoff low; expiry high; Q5 NC |
| U221 first gate pins 1/2/13→12 | POR_N / BUS_HOLDOFF_N / BUS_LINES_HIGH → BUS_QUIET | Quiet high only when reset released, holdoff expired and both lines high |
| U222 fourth gate pins 12/13→11 | SCL / SDA → BUS_LINES_HIGH | Either low forces quiet low even if a monostable has expired |

R201 changed 390 kΩ→**330 kΩ**, C201=1 µF. With **assumed** K=0.45–0.60, R±1%, C±10%, `t=KRC` gives **132.3–220.0 ms**. R202=47 kΩ/C202=100 nF gives **1.884–3.133 ms**. These are design sensitivity ranges; Nexperia's typical timing curves do not guarantee these corners at 3.3 V or temperature. X7R bias, leakage and retrigger recovery must be measured. Required progress is a **20 Hz complete waveform: rising edges every 50 ms**, not a 20-toggle/s ambiguity. Require hardware timeout≤250 ms and quiet period≥1.5 ms in qualification. D201/202 follow the maker's timing-capacitor discharge protection; rapid collapse remains unmeasured.

Both bus lines stuck high are electrically indistinguishable from legal idle. Hardware cannot prove successful configuration or correct frequency. Firmware must issue progress only after contest/task and bus/readback checks; a blind timer interrupt is prohibited. A frozen controller's remaining Si5351 clock is muted when the lease expires. Stuck-low either line trips immediately in the static model, with propagation time still unmeasured.

## Pin-derived equations and state

The simulator derives gate connections and asynchronous controls from the exported XML, with independently specified manufacturer truth tables. The readable reduction is:

```text
BUS_QUIET = POR_N & BUS_HOLDOFF_N & SCL & SDA
CORE_OK = UV_POR_N & LEASE_OK & BUS_QUIET & MUTE_N
EXCLUSIVE_OK = !(PA_REQ & FOX_REQ)
MODE_OK = !(PWR0 & PWR1)
PA_CONDITION_OK = !PA_REQ | PA_GUARD_RAW
SAFE_RAW = CORE_OK & EXCLUSIVE_OK & MODE_OK & PA_CONDITION_OK
HEALTH_N = SAFE_RAW & !selected_request_withdrawn
RESET_N = ARM & HEALTH_N

U224: on raw ARM rise, if HEALTH_N, capture:
  SEL_EXT=PWR0; SEL_FULL=PWR1; PATH_PA=PA_REQ; PATH_FOX=FOX_REQ;
  ARM_ACCEPT=!CW_KEY. HEALTH_N low clears all six Q outputs.
U223A: RESET_N low clears ARMED; delayed ARM rise samples ARM_ACCEPT.
PA_PERMIT = ARMED & PATH_PA & ARM_ACCEPT
FOX_PERMIT = ARMED & PATH_FOX & ARM_ACCEPT
PA_KEY = PA_PERMIT & CW_KEY; FOX_KEY = FOX_PERMIT & CW_KEY
normal driver clock permission = PA_PERMIT & KEY_TAIL
Fox buffer clock permission = FOX_PERMIT & KEY_TAIL
```

U224 is **74HC174D,653**, /MR1/CP9; physical D→Q pairs 3→2, 4→5, 6→7, 11→10, 13→12; unused D14 grounded/Q15 NC. This captures five bits with one package. [Manufacturer data](https://assets.nexperia.com/documents/data-sheet/74HC_HCT174.pdf). U223A /CLR1=`RESET_N`, D2=`ARM_ACCEPT`, CLK3=`ARM_CLK`, /PRE4=3.3 V, Q5=`ARMED`, /Q6=`NOT_ARMED`.

Selected withdrawal is implemented by two open-drain FET stacks gated by captured path and inverse live request, with a common ARM_ACCEPT-controlled return. It clears U224 context as well as U223. Clearing ARM_ACCEPT masks both permits even during U223 reset propagation. **Reset pulse width, feedback propagation, asynchronous recovery, metastability and glitch behavior are OPEN**: ideal logic tests do not guarantee physical pulse timing. Schottky wire-AND/OR high/low margins and edge slew must also pass at temperature. No push-pull CMOS outputs are tied together.

| Mode inputs / requests | Captured result when healthy/key-low ARM rises |
| --- | --- |
| PA=1, Fox=0, PWR=00/01/10, PA guards healthy | PA-only at captured Sprint/extended/full setting |
| PA=0, Fox=1, PWR≠11 | Fox-only; watt guard irrelevant |
| PA=0, Fox=0 | No RF path; adding a request later cannot transfer a captured path |
| PA=1, Fox=1 or PWR=11 | Fault; acceptance clears; no RF |
| KEY=1 or no genuine lease or busy/stuck-low bus | No accepted arm; recovery alone cannot arm |

## Required state progression

| Event | Result / deliberate recovery |
| --- | --- |
| 1 Battery attached, controller absent | Pull-downs/reset/no witness leave both paths inhibited |
| 2 Controller starts | Stable bounded 3.3 V, ARM/KEY/requests low; no RF |
| 3 Si5351 configuration | ARM low/MUTE low; SCL activity and line-low qualification inhibit |
| 4 First progress edge | Lease becomes high; quiet must separately establish; still unarmed |
| 5 Arm | Stable valid path/mode, KEY low, health true; fresh ARM captures context; delayed arm follows |
| 6 CW on | Selected shaper keys; genuine tail releases that path's RF mute |
| 7 CW pause | Shaper falls; selected driver/buffer retained only during the qualified tail; no path transfer |
| 8 Retune | Disarm and MUTE before I²C; unsolicited line activity clears acceptance |
| 9 Profile change | Captured rail stays fixed; disarm/configure/rearm to change; code 11 faults |
| 10 Path change | Withdraw selected request clears context; opposite request needs a new ARM cycle |
| 11 Controller reset | Default controls/reset/lease loss inhibit; clock activity alone does not authorize RF |
| 12 Heartbeat loss | Timeout clears both; resumed heartbeat does not rearm |
| 13 I²C clocks | Immediate line-low inhibit plus retriggered quiet holdoff; no automatic rearm |
| 14 Bus stuck low/high | Either low inhibits; both high require progress contract and fresh arm; no hardware transaction authentication |
| 15 PA rail OV | Open collector pulls PA guard low; context clear, INB high, buck/switch off |
| 16 Pack UV | Common UV trips both; additional 4S backstop applies to PA |
| 17 PA OC | Local trip disconnects and clears; BMS alone cannot cover this |
| 18 Hot/open/short NTC | PA guard trips; sensor attachment/lag require physical test; Fox population has no watt sensor |
| 19 Conflicting requests | Invalid request clears acceptance; clearing conflict with ARM high does not rearm |
| 20 Clear fault | KEY low; ARM low≥20 ms; restore/verify health, path, source and mode; ARM high; wait≥250 ms before first key |

Loss of health takes priority over a graceful CW tail: emergency shutdown may truncate an edge. Supply collapse may leave digital devices outside characterized operation; measure rail crossings, backfeed and RF bursts. Digital PASS is not proof of analog startup safety.

[Reproducible verification](M3A_R1_VERIFICATION.md), [component disposition](M3A_R1_SIMPLIFICATION.md) and [review decision](M3A_R1_REVIEW_DECISION.md).
