# M5B-E1 component qualification

2026-10-16. Landings and pin-to-net checks concern the exact listed manufacturers. They do not authorize undocumented substitutes. Procurement remains unapproved. Indexed stock is not reserved stock; confirm every orderable suffix, price and delivery date before purchase.

## Seven R4 open positions

| Ref | Selected part and landing | Electrical/mechanical evidence | Supply status |
| --- | --- | --- | --- |
| J301 | JST B2P-VH(LF)(SN), native JST VH 2-way 3.96 mm top entry | [JST eVH drawing](https://www.jst.com/wp-content/uploads/2025/06/eVH.pdf); 1 BAT_RAW+, 2 GND; VHR-2N housing and appropriate SVH contacts; harness polarity is an assembly check. Header approximately 9.4 mm high, mated envelope approximately 14.6 mm. | Credible MOQ1 distributor listing; finish/suffix and mating contacts require procurement confirmation. €0.35 is an estimate. |
| J701 | Wurth 66012102111404, exact native MMCX footprint | [Drawing](https://www.we-online.com/components/products/datasheet/66012102111404.pdf), Rev001.000, 2019-03-13; center RF, shell GND, 50 Ω/6 GHz, approximately 5 mm height. Distinct from normal SMA. | Indexed European cut-quantity stock, MOQ1; €3.68 through quantities 6/10/20 is an observation, not a quote. |
| C409 | Panasonic 25SVPG150M, local C10 landing | [Manufacturer dimensional sheet](https://industrial.panasonic.com/cdbs/www-data/pdf/AAB8000/AAB8000COL10.pdf), 2025-10-31; 150 µF/25 V, 13 mΩ at 100 kHz, Ø6.3 × 9.9 mm. C10 gap 2.1 mm, total land length 9.1 mm, width 1.6 mm. | DigiKey DE indexed752, cut MOQ1; €1.47@1, €0.95@10. Confirm voltage/temperature/lot. |
| L606, L635 | Coilcraft 1812SMS-33NJLC, local Doc184 staggered landing | [Doc184](https://www.coilcraft.com/getmedia/c6fe1f83-b176-469d-a071-e2edb068fef2/midi.pdf), 2021-12-02; 33 nH, Q≥100 at 150 MHz, SRF2.5 GHz, 3 A temperature-rise rating. Body4.95 × 6.35 × 4.2 mm. | Indexed MOQ1 stock; €1.64@1, €1.40@10, €1.29@25. |
| L634 | Coilcraft 0603HC-47NXJRW, local Doc218 landing | [Doc218](https://www.coilcraft.com/pdfs/0603hc.pdf), 2022-08-08; 47 nH, Q≥40 at250 MHz, SRF1.53 GHz, 0.85 A temperature-rise rating. Body1.8 × 1.12 mm; max assembled height approximately1.172 mm. | **Non-stocked**, indexed9-week factory lead time, cut MOQ1. €0.75 remains an estimate. W is the current termination suffix; do not source obsolete U without review. |
| L638 | Coilcraft A05TJLC, local Doc107 staggered air-core landing | [Doc107](https://www.coilcraft.com/getmedia/43c5dfe5-bff4-43e2-bb28-73b5766b7523/mini.pdf), 2021-07-23; 18.5 nH original ST value, body3.94 × 4.45 × 3.15 mm. Keep coil orientation and pad geometry. | Exact series documented; current price/stock unquoted. |

These Coilcraft parts are purchased RF inductors, not arbitrary power chokes or unexplained self-wound substitutions. No new winding is required in the VHF matching chain.

## Other critical landings

| Device | Physical mapping and disposition |
| --- | --- |
| ST PD54008L-E, PowerFLAT5×5 | ST January2007 Rev2 top-view gate-left, drain-right, source-center; local continuous functional pads G/D/S follow manufacturer landing. Gate/drain 0.5 × 5 mm centered at±2.25 mm, source2.7 × 5 mm. The source is electrical RF ground. Segmented paste, twelve ground vias and grounded spreader are explicit. No invented numeric pin-group order. |
| Mini-Circuits PHA-1+ | DF782 RevG, 2017-02-08; 1 RF_IN, 2 ground lead, 3 RF_OUT/DC, 4 grounded flange. Manufacturer polygon/pads are asserted, including the common2/4 ground. Package/flange maximum envelope is represented in 3D. |
| TI TPS611781RNWR | RNW0013A, 4222804/C 2019-11; center6 GND, 7 SW, 8 VOUT are separate 0.35 × 3.5 mm bars with isolated paste apertures. No shorted common EP. |
| TI TPS54302DDCR | Exact DDC6 pin functions retained. Converter-inductor landing now follows Bourns SRP1265A drawing: inner gap8 mm, outer14.2 mm, pad3.1 × 5 mm. |
| L301 SRP1265A-100M / L302 SRP1265A-4R7M | 10 µH: 10 A RMS/15.5 A saturation; 4.7 µH:13.5 A RMS/28 A saturation under manufacturer conditions. Max body14 × 12.8 × 6.5 mm. L301 indexed zero stock/backorder; L302 indexed EU stock. Both MOQ1 listings; delivery confirmation required. |
| TI TLV76701DRVR U950 | WSON6 2×2 mm:1 OUT,2 FB,3 GND,4 EN,5 GND,6 IN,7 exposed ground. Minimum effective output capacitance≥1 µF must be checked with the selected4.7 µF/25 V X7R capacitor over bias/temperature. Regional stock caches conflict; source confirmation remains open. |
| TI TLV76150DCYR U303 | SOT223:1 GND,2 OUT/tab,3 IN. Tab is 5 V, not ground. TI SBVS349D May2025 recommended input18 V/absolute20 V. |
| TI TPS22810DBVR U305 | TI SLVSDH0C January2018 DBV6 physical pin table. CT open is permitted; QOD tied to OUT implements discharge. Recommended18 V, absolute20 V. |
| ST D45H11 Q401 | ST DocID4213 Rev5 October2009:1 BASE,2 COLLECTOR/tab,3 EMITTER. Collector/tab is VPA and requires insulation from grounded sink/fastener. TO220 vertical footprint pitch2.54 mm. |
| ST BD139 Q402 | ST May2008 Rev5 SOT32:1 BASE,2 COLLECTOR,3 EMITTER; exposed collector is MOD_SINK. The perspective package view must be read with terminal numbers. Do not substitute an E1/B3 manufacturer variant. Inspect and diode-test incoming parts before soldering. |
| TL431DBZ | Physical1 cathode,2 REF,3 anode verified. Generic TL431 symbols/packages are not interchangeable evidence. |
| J101 | Wurth61202021621 keyed20-way IDC; source002.001, 2026-08-30. Qualified1.1 mm finished PTH holes; body33.06 × 9.1 × 8.75 mm. Harness contact numbers, notch, strain relief and cable exit require incoming inspection. |
| J501 | Amphenol132134 vertical SMA, manufacturer drawing linked by native footprint. Center finished hole1.5 mm, grounds1.7 mm in installed KiCad footprint. Incoming mating/lead-size inspection and fabricator finished-hole confirmation remain required. |
| J302 | Samtec TSW-103-07-G-S with SNT-100-BK-G shunt. Fit1–2 only for2S boost or2–3 only for4S buck. Never fit both converter populations. |
| TH801 | Vishay NTCLE100E3103JB0, insulated remote10 kΩ/B3977 bead; custom two-wire landing. Bond to the pass-device case and strain-relieve wires. A detached bead with intact wires cannot be detected by an electrical open/short check. |

L604 uses the same Doc184 land as the33 nH feeds, with150 nH/33 mΩ max DCR. L641–643 retain ST39/22/27 nH values but now use exact Coilcraft1008CS Doc101 lands (2022-08-05), rather than a merely similar generic1008 footprint. R506's10 Ω/1 W rating is implemented with a2512 resistor. Transistor tabs, shunt Kelvin sense and converter ground returns are reviewed separately from nominal pin count.

[pinout-audit.json](../hardware/2m/review/M5B-E1/pinout-audit.json) compares manufacturer-specific maps against the exported netlist and native PCB pads. The complete BOM supplies every populated MPN, footprint and evidence category. ERC alone is not a manufacturer pinout check.

Custom 3D models are sourced **dimensional envelopes**, explicitly marked as such in `3D-model-status.json`; they are not claimed to be qualified vendor STEP models. Standard KiCad models are also visualization aids. Actual mounting, solderability, lead bending, thermal interfaces and incoming component identity remain physical inspection requirements.

The installed standard STEP library lacks J301/J501/J701 visualization models; the actual KiCad renders therefore show their board lands/outline without a qualified connector body. This is a disclosed visualization gap. It does not substitute for the manufacturer2D land/hole audit or establish a final enclosure height. The open bench fixture has adjustable cable/headroom clearance.
