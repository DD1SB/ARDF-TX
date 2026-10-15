# M5A-R1 — final and driver selection

Date: **2026-10-15**. **M5A-R1 electrical evaluation candidate — NOT RELEASED. All physical tests NOT_RUN.**

Select **PD54008L-E plus PHA-1+ as a plausible, unqualified economical evaluation chain**. Keep the complete PD55008-E/PHA-13HLN+ R0 implementation at tag `m5a-r0` (commit`ea671c1`) and in [native archive](../hardware/2m/archive/M5A-R0/). Selection is conditional on measured final gain, envelope transfer and matching; it is not approval of a buildable reference clone while the [source-trace blocker](M5A_R1_ST_REFERENCE_AUDIT.md) remains.

## Drive calculation at identical functional scope

Connector carrier 1.258925 W,80% PEP4.078918 W,1 dB capability 5.135054 W. Retaining 0.75 dB output-loss allowance gives **6.103 W final-plane capability**. Allow 1.25 dB driver-to-final input loss and 3 dB driver output backoff. No whole-board gain is assigned to the final alone.

| Assumed final gain dB | Required driver output dBm | Required driver P1dB dBm |
| --- | --- | --- |
| 15 | 24.11 | 27.11 |
| 17 | 22.11 | 25.11 |
| 20 | 19.11 | 22.11 |
| 22 | 17.11 | 20.11 |


PHA-1+ published 50 MHz/800 MHz P1dB values bracket the band but provide no guaranteed 144 MHz result. Its 22.2 dBm typical 50 MHz value implies a measured final-gain requirement near 19.91 dB at the capability plane; if actual driver P1dB is only 20 dB m, the gain requirement rises to 22.11 dB. Include uncertainty and loss measurements; neither number is a promised gain.

| Driver | Evidence and evaluation decision | q6/10/20 EUR/device |
| --- | --- | --- |
| PHA-1+ | Preferred conditional candidate; 5V146mA typical,110–180 mA range; 17.2/15.7 dB typical gain at 50/800 MHz. P1dB must be measured at 144 MHz. |2.82/2.82/2.82 observed display; tax confirmation pending |
| GVA-84+ | R0-researched 20.73 dBm example leaves less margin; no revised 144 MHz minimum verified. Gain floor≈21.38 dB if that P1dB holds. Not selected. | historical/unresolved exact EU basket |
| MMBTH10LT1G discrete | Active manufacturer family, cheap transistor; complete stable linear driver/matching not demonstrated. Do not replace a supported MMIC with an invented discrete stage. | whole-stage 1–1.5 estimate, not quotation |
| PHA-13HLN+ | Stronger fallback; 8V234.1 mA typical, R0 estimated P1dB27.3–28.4 dBm bracketing frequencies. Exact 144 MHz compression still measured. |14.6047 historical converted allowance |

[PHA-1+ manufacturer data](https://www.minicircuits.com/pdfs/PHA-1%2B.pdf) describes 4.8–5.2 V operation,146 mA typical and 60 °C/W junction-to-ground-lead thermal resistance; its 6 V absolute limit is not an operating target. Current PDF text was searchable but binary access returned 403; earlier pin table identifies 1RF_IN,2GND,3RF_OUT/DC,4 ground paddle. Exact DF782/PL523 landing remains OPEN. [Mouser EU](https://eu.mouser.com/en/ProductDetail/Mini-Circuits/PHA-1%2B?qs=xZ%2FP%252Ba9zWqYz5cEhj1ZlVg%3D%3D) lists 139-PHA-1, cut tape MOQ/multiple 1, €2.82 at 1, €2.11 at 50; indexed 4662 stock, no reservation. No50-piece break is booked for a 20-unit fleet.

PD54008L-E's manufacturer 15 dB/8 W result is at 500 MHz/7.5 V, not 144 MHz. Its 25 V drain,−0.5..15 V gate and 3 °C/W case thermal ratings do not establish AM stability. PD84001 is never fitted. The ST reference's5W connector result is 0.116 dB short of our 5.135 W capability investigation before changed losses; it neither proves full margin nor proves failure.

## Actual R1 RF implementation

Local source/filter retained; R602/R603/R604 now form a 3 dB candidate pad 17.8 Ω/287 Ω/287 Ω, adjustable by population after measurement. First testing uses the external generator or a 12 dB pad. Do not assume Si5351 available power: at 20 dB final gain,19.11 dBm driver output requires approximately 2–4 dBm input for 15–17 dB MMIC gain, plus source filter/pad loss. Verify this budget at the actual port and configure drive strength accordingly.

U501 is replaced, its supply becomes a 5 V LDO, and Q501 is a functional-terminal PD54008L-E symbol. R606 bias feed is now VMOD, independent of the 5 V driver rail; start trim grounded and investigate 50–200 mA quiescent drain current with bounded energy. Gate clamp 6.2 V, inhibit clamp and stopper remain. Bias must remain fixed during supply AM; any thermal bias drift or low-drain gate behavior is a coupon measurement. Original APC circuitry is not claimed reused.

C605/L605 and L608/C610 are explicitly OPEN tuning positions. The illustrative input impedance 5−j10Ω plus 1 Ω stopper is an assumption, not measured S-parameters. The [calculation](../hardware/2m/review/M5A-R1/calculations.json) gives 28.87 nH/59.57 pF; output 3.5 Ω/60 pF hypothesis gives 14.51 nH/81.74 pF. These numbers do not qualify the network, its topology or stability. Do not populate for RF operation until the source trace is closed. The existing nine-pole ladder retains its R0 values only as an interim output-filter budget; it is not the ST−70 dBc filter.

Measure small-signal stability with varying drain/gate bias, driven behavior through the envelope, out-of-band spectrum and mismatch. No unconditional stability factor can be calculated without relevant device S-parameters. Two-stage ST gain does not supply them.
