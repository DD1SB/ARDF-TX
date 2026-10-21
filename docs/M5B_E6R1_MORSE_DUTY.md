# M5B-E6R1 — exact Morse duty and timing

The [integer-microsecond generator](../tools/m5b_e6r1_morse.py) calculates every identifier at 8–15 WPM. A dit is `round(1200000 / WPM)` µs, matching the controller's PARIS timing convention. Dots/dashes are 1/3 dits, inter-element space 1, letter space 3 and repeated-word space 7. No firmware implementation is changed. The [CSV](../hardware/2m/review/M5B-E6R1/morse-duty.csv) records exact finite-slot MARK/SPACE durations and interval counts; [JSON](../hardware/2m/review/M5B-E6R1/morse-duty.json) includes timing assumptions.

| Repeated identifier | MARK units | SPACE units | Repetition units | MARK fraction |
| --- | ---: | ---: | ---: | ---: |
| MOE | 16 | 16 | 32 | 1/2 |
| MOI | 17 | 17 | 34 | 1/2 |
| MOS | 18 | 18 | 36 | 1/2 |
| MOH | 19 | 19 | 38 | 1/2 |
| MO5 | 20 | 20 | 40 | 1/2 |
| MO | 15 | 13 | 28 | 15/28 = 53.5714% |
| S | 3 | 9 | 12 | 1/4 |
| MO5 DD1SB, representative additional ID | 52 | 52 | 104 | 1/2 |

The last row is an example licensed identifier, not a mandated call sign or a claim all calls have 50% duty. Slot truncation changes the actual fraction even for identifiers whose complete repetitions are exactly half MARK. At 12 WPM:

| Code | Classic MARK / SPACE within 60 s | Sprint MARK / SPACE within 12 s |
| --- | --- | --- |
| MOE | 30.3 / 29.7 s | 6.3 / 5.7 s |
| MOI | 30.4 / 29.6 s | 6.3 / 5.7 s |
| MOS | 30.3 / 29.7 s | 6.2 / 5.8 s |
| MOH | 30.3 / 29.7 s | 6.2 / 5.8 s |
| MO5 | 30.0 / 30.0 s | 6.0 / 6.0 s |
| MO5 DD1SB | 30.3 / 29.7 s | 6.3 / 5.7 s |

Classic adds 240 s OFF; Sprint adds 48 s OFF. Slow/fast group examples use 10/15 WPM with the same transmitted MO identifiers. S is included as an optional spectator identifier. The thermal solver also checks all five codes at 12 WPM and MO5 at 8/15 WPM. It does not extrapolate an arbitrary 50% waveform to every call sign or clipped slot.

Continuous MO repeats every 28 dits: 4.2 s at 8 WPM, 2.8 s at 12 WPM and 2.24 s at 15 WPM. Its periodic thermal state is solved on that true period. The 60 s beacon observation in the duty CSV is only a finite observation window, not a shutdown/restart every minute. E6 used a finite 60 s MO window; the R1 periodic correction is explicit and the original result remains preserved.

Interior carrier ramps are centered on logical MARK boundaries. Full raised-cosine durations 5/8/12 ms correspond to 10–90% durations 2.952/4.723/7.084 ms. The 8 ms candidate has a 2 ms driver lead. Coarse KEY spans the preparation and ramp interval; the AF envelope determines RF timing. At slot start/end, ramps are clipped inside the allocated slot, so the first/last element may have a shortened shaped area. Normal gaps do not release and reacquire ARM. Emergency inhibition overrides shaping immediately.

Heat is integrated over the shaped waveform, including transitions and residual loads. Logical MARK fraction alone is not used as a thermal-power multiplier. [Energy integrals](../hardware/2m/review/M5B-E6R1/energy-integrals.csv) contain all three architectures, both supply populations and three power profiles. Additional call signs and actual target-firmware timing must be checked when configured; this repository remains a firmware foundation.
