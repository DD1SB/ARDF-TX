# M2 RF power modes and revised endurance targets

Date: **2026-10-14**. **Calculated scenarios, not certified RF performance or measured endurance.** [ADR-0011](decisions/ADR-0011-dual-voltage-power-and-endurance.md) proposes the supply architecture. The new user requirement is 12 h at the highest selected normal setting and 24 h at a defined sufficient reduced setting. Continuous Foxoring retains 24 h at nominal 10 mW. Continuous finish/spectator roles are separate.

## Requirement-to-source matrix

The [official IARU index](https://www.iaru-r1.org/about-us/committees-and-working-groups/ardf/documents/ardf-rules/) still lists Part B2025 as current on 2026-10-14. [Part B2025](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf) was reread; no endurance rule is inferred from it.

| Requirement | Primary location | Interpretation retained here |
| --- | --- | --- |
| Classic 80 m 1–5 W, A1A | T2.6, printed p.10 | Conducted RF output; not ERP. Carrier 3.510–3.600 MHz, stability better than 50 ppm, vertical antenna, simultaneous channels≥20 kHz. |
| Sprint 0.3–1 W | S6.1–S6.6, pp.14–15 | Two concurrent groups on separately configurable frequencies,12-second slots; distinct continuous finish/spectator frequencies where required. Symmetric grounding; long-wire matching remains separate from Foxoring. |
| Fox field 10 mW continuous | FT2.6/F28.2, p.17 | Approximately 30 cm vertical radiator, dedicated compact return/loading; nominal reference-load power is independent of radiated field. |
| Fox reach | F27.3, p.17 | Audible at marked position and 30 m; not audible at 250 m. Receiver/terrain protocol and installation must be measured. Finish uses normal 1–5 W and long antenna. |
| VHF 0.25–1 W ERP, A2A70–80% | T2.8, p.10 | Championship carrier 144.500–144.900 MHz, horizontal antenna at 2–3 m; simultaneous spacing **>200 kHz**. Broader lawful frequency capability remains separate. |
| Off-slot silence / uniform parameters | T2.2/T2.4 and 27.2 | Hardware mute retained. Select the power profile before deployment; do not secretly lower power as the battery empties. Obtain organiser interpretation of any in-event change; default is latch-off at the selected profile's cutoff. |
|12 h full /24 h reduced | USER,2026-10-14 | Explicit supersession of SYS-008's original maximum-power 24 h target; not an IARU or legal authorization. |

The [national regulatory review](M1_REGULATORY.md) remains applicable and unresolved where previously marked OPEN. Battery voltage does not grant amateur or LoRa transmission permission.

## Selected targets and modeled supply power

Propose **3 W Classic maximum for the normal-cost HF population,1.2 W for extended Classic**, retaining a separately qualified 5 W thermal option. The existing near-1 W2S population remains economical. Sprint uses the same PA at 0.85 W normally and 0.5 W extended. These settings provide margin above minimum power; exact calibration tolerances must ensure the measured output stays within the rule range. The 1 W and 5 W rows evaluate range endpoints, not tolerance-free field settings.

| HF conducted power | PA conversion allowance | Gate-drive W, before converter |2S high average W /12 h Wh /24 h Wh |4S buck average W /12 h Wh /24 h Wh |
| ---: | ---: | ---: | --- | --- |
|1.0 W |50% |0.220 |0.733 /8.80 /17.59 |0.659 /7.90 /15.81 |
|1.2 W |55% |0.220 |0.781 /9.37 /18.73 |0.699 /8.39 /16.78 |
|1.5 W |55% |0.220 |0.923 /11.08 /22.15 |0.820 /9.84 /19.69 |
|2 W |60% |0.300 |1.100 /13.20 /26.41 |0.973 /11.67 /23.35 |
|3 W |60% |0.300 |1.536 /18.43 /36.87 |1.343 /16.12 /32.23 |
|5 W |60% |0.400 |2.431 /29.17 /58.35 |2.106 /25.27 /50.55 |

The 2S economy buck gives 0.692 W mean at 1.2 W RF and 0.652 W at 1 W RF; it cannot supply 2–5 W at depleted 2S without a different supply. These are input allowances, not manufacturer efficiency claims. Reduced power uses lower drain/driver supply, not lossy RF attenuation. Gate-loss and effective PA efficiency change by power range; drive reduction alone may degrade switching efficiency and CW shaping. Compare those mechanisms on the bench before accepting efficiency.

| Sprint setting |2S economy mean W |4S buck mean W |12 /24 h Wh,2S economy | Interpretation |
| ---: | ---: | ---: | --- | --- |
|0.3 W |0.341 |0.348 |4.09 /8.17 | Rule minimum; no calibration margin |
|0.5 W |0.429 |0.436 |5.15 /10.31 | Proposed extended profile |
|0.85 W |0.585 |0.592 |7.02 /14.04 | Proposed normal profile |
|1 W |0.652 |0.659 |7.82 /15.64 | Rule maximum; use a calibrated setting below boundary |

Foxoring stays 10 mW continuous with a retained **0.350 W total battery allowance**,4.20/8.40 Wh for 12/24 h. A lower transmitter power is not the extended-life option. Neither lower current nor the new battery cancels compact-antenna matching, the independent port guard or the 30/250 m field test.

## VHF carrier, mean, PEP and headroom

Retain the explicitly assumed installed antenna/feed net gain **−1 dBd** and output-filter loss 0.5 dB. ERP interpretation as carrier remains an organiser/measurement gate; do not silently equate ERP with PEP. For ERP carrier `E`, connector carrier=`E×10^0.1`, full-tone mean=`carrier×1.32`, PEP=`carrier×3.24` at 80% modulation. Add 1 dB clean reserve; the internal PA must also cover filter loss.

| Carrier ERP W | Connector carrier /tone mean /PEP W |2S boost mean W |4S buck mean W |4S12 /24 h energy Wh | Carrier center /upstream V |
| ---: | --- | ---: | ---: | --- | --- |
|0.25 |0.315 /0.415 /1.020 |1.273 |1.244 |14.93 /29.86 |4.0 /9.0 |
|0.30 |0.378 /0.499 /1.224 |1.376 |1.343 |16.11 /32.22 |4.0 /9.0 |
|0.50 |0.629 /0.831 /2.039 |1.651 |1.605 |19.27 /38.53 |5.0 /10.5 |
|0.75 |0.944 /1.246 /3.059 |1.994 |1.934 |23.20 /46.40 |6.667 /13.5 |
|1.00 |1.259 /1.662 /4.079 |2.355 |2.279 |27.35 /54.70 |6.667 /13.5 |

**Every VHF row requires a measured RF transfer function.** At equal 4 V center,0.25 and 0.30 ERP settings change drive/bias while retaining headroom; neither is proved linear. Dynamic conversion assumptions are 35% for≤0.30 ERP,40% for 0.50,45% for≥0.75, plus 150 mA bias separately. The driver's 1.55 W active overhead remains at reduced power. Do not add this bias twice after measuring total efficiency. The 100 nF/800 Hz envelope current and feedback behavior retain earlier modulator qualification requirements.

Full 1 W ERP requires approximately 5.135 W clean connector PEP including 1 dB reserve, or 5.762 W before the assumed output filter. A square-voltage extrapolation from ST's 8 W at 12.5 V suggests a crest near 10.61 V to supply that internal figure. This is only a scaling check at a different frequency, not a 144 MHz guarantee; it shows why arbitrarily lowering crest to 9–10 V cannot be accepted from energy arithmetic. GVA-84+ drive margin, matching, envelope gain, distortion and AM-to-PM behavior remain gates.

Propose normal VHF 1 W ERP candidate and extended **0.30 W ERP**, calibrated to remain≥0.25 W including antenna and meter uncertainty. A strict 0.25 W endpoint is evaluated but not preferred for a fleet calibration margin. Select a common event power profile before deployment; all units maintain that profile to cutoff. Training retains its own boundedµW–mW AM branch and cannot substitute for championship operation.

## Which packs fit both targets?

All entries are model selections, **not runtime passes**. 4S full-VHF uses the unverified extra energy-window factor 0.65 for the provisional 14.2 V cutoff; HF/reduced VHF use the full 3.0 V/cell planning window.

| Configuration /selected 12 h and 24 h settings | Smallest modeled candidate satisfying both | Calculated runtime at full /reduced | Principal limitation |
| --- | --- | --- | --- |
| Fox 10 mW /10 mW |2S1P 25R |32.7 h at both | Measured controller idle and field reach |
| Economy HF 1.2 W /1.0 W |2S2P 25R |33.0 /35.1 h |1 W endpoint lacks lower-limit margin; prefer 1.2 W extended too on this pack |
| Sprint 0.85 W /0.5 W |2S1P 25R |19.5 /26.6 h | Cold/idle stress can fail 24 h; combine with larger Classic pack if needed |
| HF 3 W /1.2 W |4S1P 25R |17.0 /32.7 h | Poor 40% PA /85% buck case gives 11.4 h full; M35A alternative gives 23.0 /44.1 h nominal |
| HF 5 W /1.2 W |4S1P M35A |14.6 /44.1 h | Poor PA/converter case 9.8 h full;5 W thermal/shaper gate open |
| VHF 1 ERP /0.30 ERP,2S boost |2S3P M35A |19.6 /33.6 h | Six expensive cells; two-pair M35A meets 12 h full but only 22.4 h reduced |
| VHF 1 ERP /0.30 ERP,4S buck |4S2P 25R |13.0 /34.1 h | Early cutoff fraction/efficiency dominate;35% full PA case 11.1 h fails 12 h |
| Same VHF settings with larger-capacity reserve |4S2P M35A |17.6 /45.9 h | Costlier; extreme cold/aging can still fail; not mandatory default |
| Universal, one band active |4S2P 25R candidate |HF 5 about 21.7 h; VHF 1 about 13.0 h, less second-board idle | Shared pack qualification; no dual full-power 12 h claim |

The complete matrix includes all six packs,2.45/3.35/3.40/3.50 Ah, intermediate settings and both duration targets in [generated tables](M2_POWER_ARCHITECTURE_TABLES.md) and [JSON](M2_POWER_ARCHITECTURE_RESULTS.json). A modeled boundary pass is not a credible release without margin. 4S1P is not presently a full-power VHF replacement for 2S2P: the AM cutoff loses too much accessible energy. Successful lower-crest/gain testing could change this result.

## Continuous and simultaneous operation

The generated matrix explicitly includes continuous HF 1/1.2/3/5 W, Sprint 0.3/0.5/0.85/1 W and VHF 0.25/0.30/0.50/1 W ERP cases. For example, 4S Sprint 1 W continuous consumes 2.705 W and runs 16.9 h on 4S2P 25R; 0.5 W continuous consumes 1.594 W and runs 28.7 h on the same pack. A 0.30 W ERP VHF beacon still consumes 6.125 W in the fixed-bias model and runs only 7.5 h on that pack. These are modeled role-specific limits, not a general beacon 12/24 h promise.

Continuous beacons use 100% scheduled duty, with no Morse-space current credit. On eight minimum-capacity M35A cells,4S buck HF 1.2/3/5 W modeled runtime is 21.2/10.1/6.2 h; full VHF has only 3.7 h with the 0.65 cutoff-window scenario. None delivers 12 h full 5 W/1 ERP or 24 h continuous 1.2 W. A1 W HF beacon is modeled separately by applying 100% duty to the same 1 W load; do not count it as a twenty-percent fox. Sprint continuous 0.5 W may fit 24 h on larger packs, but must use the correct continuous role and required coverage. Event duration, service swap or external supply needs a separate decision.

Simultaneous 5 W HF and 1 W ERP VHF each at 20% gives 4.248 W mean on 4S,50.98 Wh for 12 h. Eight M35A cells provide only 40.10 Wh with the early-VHF cutoff scenario: **no 12 h pass**. The 2S boost counterpart gives 4.656 W and 13.2 h on 2S4P M35A because it accesses the full planning window. This is a meaningful 4S drawback, not additional battery energy. Default universal use remains one active band. Dual reduced 1.2 W HF +0.30 ERP gives 1.905 W on 4S and 45.71 Wh/24 h, a near-boundary 25R4S2P pass that loses margin with LoRa/idle changes; prefer measured reserve or M35A if dual 24 h becomes required.
