# M5B-E6R1 — A2A requirements

Analysis executed 21 October 2026, starting at `85186204619edec32ad1bb2a3044bb55ea399658`. **Keyed-carrier A2A is permitted; circuit and thermal acceptance remain HOLD.**

The primary reference is the official [IARU Region 1 ARDF Rules Part B, 2025](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf), Appendix 1, printed page 10. T2.8 permits either an RF carrier keyed and modulated with an audio tone or a continuous carrier with keyed audio modulation. The independently written models compare those alternatives without changing the required on-MARK RF profile.

| Source requirement | Consequence for this proposal |
| --- | --- |
| T2.8: 144.500–144.900 MHz, stability better than 50 ppm | Keep the synthesizer/reference running during the allocated slot; verify frequency and settling physically |
| T2.8: 0.25–1 W ERP, 70–80% depth, 8–15 WPM | Retain all profiles and full 1 W capability; model 80% for the loss envelope and 75% as a modulation comparator |
| T2.8: simultaneous channels separated by more than 200 kHz; unwanted products meet national regulations | Channel separation is not an occupied-bandwidth mask. Ideal-envelope FFT results do not establish regulatory emission compliance |
| T2.8: horizontal polarization, antenna 2–3 m high | No antenna redesign or field-coverage claim |
| T2.2: common technical parameters and antenna installation for competition transmitters | Select and qualify a uniform competition configuration, rather than mixing keying characteristics arbitrarily |
| T2.3 and 28.2: beacon on a sufficiently different frequency; continuous MO | Continuous MO has no Classic 20% scheduled-duty discount |
| T2.4: no radiation during inactive periods, including antenna-system radiation | Independent slot/fault inhibition remains authoritative; ordinary Morse shaping cannot extend beyond SLOT |
| 27.3–27.4: start audibility including beacon, beacon operating until competitors finish | A lower-power beacon is an optional profile requiring event acceptance; it is not the sole thermal solution |
| 27.6: additional identification only within active allocated time | Example CW-ID is included within, and clipped by, the same slot |
| 28.2: MOE/MOI/MOS/MOH/MO5 in successive 60 s slots | Analyze each actual identifier, with 240 s inactive per 300 s cycle |

The supplied PDF moves from T2.6 to T2.8; it contains no separate T2.7 paragraph to interpret. T2.6 concerns the other band. Appendix 5 S6 describes Sprint, including 12 s / 60 s operation, slow/fast groups, a 0.3–1 W Sprint power range and separate beacon/spectator frequencies. Its S6.3 example is on 3.5 MHz. Applying a 12/48-second thermal profile to this 2 m engineering model does not establish that every event uses 2 m Sprint or that 0.25 W is a valid Sprint competition setting. The group suffix F is a label, not an added transmitted letter in our MO identifiers.

The retained approximately 5.135 W clean connector PEP capability includes 1 dB reserve over the 4.079 W modeled PEP at 1 W ERP/80% AM. It is not 5 W continuous carrier. Carrier is approximately 1.259 W at the connector, and full-tone mean RF approximately 1.662 W. These are planning calculations, not achieved RF measurements.

Existing project off-slot and unwanted-emission screening targets remain unchanged. No numeric national emission mask is invented here. Rise/fall shaping, spectrum, AM depth, clean PEP, stability and off-slot silence must be measured before operation. Regulatory method compatibility is Gate A PASS; [electrical feasibility](M5B_E6R1_CARRIER_KEYING.md) and [overall disposition](M5B_E6R1_REVIEW_DECISION.md) are separate gates.
