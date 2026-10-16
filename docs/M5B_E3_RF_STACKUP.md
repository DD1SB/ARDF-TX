# M5B-E3 RF and stackup redesign

The purchase configuration is ordinary **1.6 mm, two-layer FR4, 1 oz**, without controlled impedance or a named/custom core. The analytical nominal model is 1.50 mm copper-to-copper dielectric,35 µm copper, Dk4.5, tanδ0.02 and 15 µm mask per side. These sum to1.60 mm; they are **not separate fabrication tolerances**. Published finished thickness ±10% does not fix dielectric spacing. Ordinary outer1 oz copper includes plating;35 µm is nominal, not a minimum finished-thickness guarantee. [JLC capabilities](https://jlcpcb.com/capabilities/pcb-capabilities/), [copper guide](https://jlcpcb.com/help/article/jlcpcb-copper-weight) and [calculator guide](https://jlcpcb.com/help/article/user-guide-to-the-jlcpcb-impedance-calculator) were reviewed2026-10-16.

Finite-thickness Hammerstad/Jensen calculations give **2.741 mm width,50.005 Ω,εeff3.3947** uncoated. E2 was1.102 mm over0.64 mm/70 µm/Dk4.3. Scaling lengths by√(εeff_E2/εeff_E3)=**0.981206** preserves nominal144.7 MHz phase. Conventional microstrip fits; grounded coplanar geometry would add gap/fence/pad constraints without a demonstrated benefit, so no arbitrary CPW50 Ω claim is used.

| Line | E2 mm | E3 mm | Width mm |
| --- | --- | --- | --- |
| TL603 | 6.2300 | 6.1129 | 2.741 |
| TL604 | 6.6200 | 6.4956 | 2.741 |
| TL605 | 5.8000 | 5.691 | 2.741 |
| TL606 | 2.2000 | 2.1587 | 2.741 |
| TL607 | 11.0000 | 10.7933 | 2.741 |
| TL608 | 12.4001 | 12.167 | 2.741 |
| TL609 | 2.0000 | 1.9624 | 2.741 |

All line bodies are real copper, not zero-length schematic wires. Butt ends prevent round-cap shorts across series pads. Q501 remains fixed; matching components move outward by fractions of a millimetre. The normal output is a flat conductor with a1 mm initial transition and 8 mm taper to1.0 mm at the fixed SMA. A100-section lossless taper model gives about 40 dB return loss between50 Ω planes at 144.7 MHz. It omits the connector pin/via and pad fringing, so it is not a measured launch result.

The top fill-only keepout x48–190/y46–62 mm retains local grounded components while keeping adjacent plane copper away from the wide matching lines. Bottom signal-routing keepouts beneath the RF strip and thermal contact remain. The native copper preview and DRC check the resulting returns. Grounded component pads/stubs make the local field nonideal microstrip; their effects remain alignment requirements.

[RF-tolerance-sweep.csv](../hardware/2m/review/M5B-E3/RF-tolerance-sweep.csv) sweeps h1.30–1.70 mm, Dk4.1–4.8, copper30–50 µm and width±20%, at 144/144.5/144.7/144.9/146 MHz. The deliberately combined extremes span **39.39–63.44 Ω**. This is ordinary-FR4 uncertainty, not a supplier impedance tolerance. These matching lines are short; their impedance error must be considered with electrical length, not treated as a long50 Ω cable. [input-match-comparison.csv](../hardware/2m/review/M5B-E3/input-match-comparison.csv) shows near-identical nominal E2/E3 ABCD behavior with the same illustrative3 Ω/80 pF gate plus33 nH feed model. That load is not a measured144 MHz PD54008 impedance.

A disclosed first-order thin-mask perturbation predicts about 49.88 Ω at 15 µm and 49.75 Ω at 30 µm; this is approximate fringe-energy sensitivity, not a full-wave solution. Estimated dielectric loss is 0.044 dB/100 mm; a conductor lower bound is 0.020 dB/100 mm. Surface roughness, solder, component Q and RF grounding can increase losses. At144.7 MHz35 µm copper is several skin depths; its RF loss does not simply double relative to70 µm.

Source/filter junctions remain short lumped0.35 mm conductors, not claimed50 Ω lines. [source-and-stub-parasitics.csv](../hardware/2m/review/M5B-E3/source-and-stub-parasitics.csv) quantifies changed equivalent L/C; an approximate source-filter cascade predicts0.456 dB versus E2's0.510 dB at 144.7 MHz. Branch stubs, driver/source impedances and Q/SRF are omitted. This supports retaining the values, not an achieved drive or harmonic claim. The elliptic filter topology and values remain identical; its ideal transfer is separately exported and is not an emissions result.

The Si5351/PHA-1+/PD54008L-E architecture, initial 10 dB source pad,19 dBm driver target, tunable C631/C633/L634 and independent training output remain. Final gain, AM depth/PEP, stability, harmonic rejection and port isolation are **NOT_RUN**. Use the bounded original adjustment set and one complete-device acceptance procedure; no separate coupon program is introduced.
