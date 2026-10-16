# M5A-R4 — RF stage and reference evidence

Dated **2026-10-16**. **M5A-R4 electrical candidate — NOT RELEASED.**
All physical tests are **NOT_RUN**. No purchasing, fabrication, assembly or RF operation has occurred.
RF80, M4A and accepted ADRs are unchanged. R3 is preserved at tag `m5a-r3`
(`daf994c`); R0/R1 tags and the R1 native archive remain available.

Select **ST PD54008L-E**, with **PHA-1+ as the conditional economical driver**. ST lists the final as active/volume production in PowerFLAT 5×5. Mouser's dated cut-tape listing has MOQ 1, €7.35 at one/€5.30 at ten and indexed stock 3,430. This does not reserve inventory. [ST product](https://www.st.com/en/radio-frequency-transistors/pd54008l-e.html), [Mouser](https://www.mouser.de/de/ProductDetail/STMicroelectronics/PD54008L-E).

## Recovered circuit and exact reuse

**ST DocID17343 Rev 1, March 2010** was recovered through DatasheetArchive after direct ST binary downloads failed. Printed pages 9–11 were visually inspected. PD54008L-E January 2007 Rev 2 top view, mechanical drawing and recommended landing were also inspected. Original ST Gerbers remain inaccessible; no exact Gerber reconstruction is claimed. The [source log](../hardware/2m/review/M5A-R4/sources.json) records retrieval paths, hashes and failures. [Original ST document](https://www.st.com/resource/en/datasheet/steval-tdr003v1.pdf).

The original complete PD84001/PD54008L-E board has publisher-reported 5 W across 135–175 MHz at 7.2 V, input below 10 dBm and supply below 1.5 A. Its harmonic result belongs to that board. These are not isolated-final gain, sine-AM or independent ARDF-TX measurements. The board is NRND and PD84001 obsolete. The recovered 2010 table identifies **PD54008L-E in both device and part-code columns**; the older standalone/AB BOM's PD54003L discrepancy is not copied.

| Block | Original signal path | R4 disposition |
| --- | --- | --- |
| Figure 15 input | RF_IN → TL1 3 mm → C8 330 pF → TL2 7.2 mm → R6 11 Ω → PD84001 gate | Entire obsolete driver block removed |
| Figure 16 interstage | Driver drain → TL3 6.23 mm → C11 56 pF shunt/drain-feed node → C9 330 pF series → TL4 6.62 mm → C12 27 pF shunt → L4 18 nH → TL5 5.8 mm → final gate | TL603/C631/C632/TL604/C633/L634/TL605; C602 blocks MMIC DC and original driver drain injection is removed |
| Figure 13 final feeds | Gate L2 33 nH; drain L3 labelled 35.5 nH with contradictory 22 nH part code | L606 retains gate value; L635 is an explicit 33 nH drain-feed starting substitution |
| Figure 17 output | Drain → TL6 2.2 mm → C13 33 pF shunt → TL7 11 mm → C14 100 pF shunt → L5 18.5 nH → C15 39 pF shunt → TL8 12.4 mm → C10 330 pF DC block → TL9 2 mm → LPF | TL606/C636/TL607/C637/L638/C638/TL608/C639/TL609 retain the actual network |
| Figure 14 LPF | Series parallel resonators 39 nH ∥ 3.3 pF, 22 nH ∥ 18 pF, 27 nH ∥ 12 pF; shunts 22/27/22/15 pF | L641–643/C641–647 replace the arbitrary nine-pole filter |

The original interstage is **not a demonstrated 50 Ω input match**. A 50 Ω MMIC changes the original PD84001 drain source impedance. The schematic retains documented starting values, not a proven adaptation. Final input impedance/drive and the necessary small matching adjustment must be established before committing copper. Complete-amplifier gain cannot be assigned to its final alone. The explicit drain-feed substitution also requires current/RF-isolation validation.

Original line width is 0.92 mm on **0.508 mm FR4 / 70 µm copper**, with lengths above. Seven two-terminal transmission-line symbols are PCB features, not purchased parts or zero-length wires. Actual layout must use the original electrical stack-up or recalculate geometry, net-tie construction, ground/vias and thermal landing. Copying the width onto 1.6 mm FR4 changes the circuit.

The [LPF ABCD calculation](../hardware/2m/review/M5A-R4/LPF_model.csv) gives about 0.52/0.30 dB loss at 144.9 MHz for assumed inductor Q 40/80. Nominal second/third harmonic attenuation is about 58/71 dB. It excludes pads, tolerance and actual PA impedance. This is an analytical model, not SPICE or a physical emissions result.

## Driver capability

PHA-1+ manufacturer Rev D, expanded sample data and DF782 Rev G drawing were recovered through distributor mirrors. At 5 V/+25°C the examples give gain/P1dB of 17.64 dB/22.70 dBm at 50 MHz and 16.30 dB/22.64 dBm at 200 MHz. These are not guaranteed 144 MHz/hot minima. Initially limit output to **19 dBm** and require measured P1dB ≥22 dBm for 3 dB backoff. Estimated driver input is 2–3 dBm plus source-filter/pad loss; Si5351/buffer fundamental output must be measured.

At −1 dBd antenna/feed gain, 1 W carrier ERP with 80% AM needs **4.079 W connector PEP**. With 0.75 dB output matching/filter loss, the final needs 4.848 W PEP. A 1 dB input-match allowance and 19 dBm drive require **18.86 dB effective final gain**, or 17.86 dB at 0 dBd. Optional 1 dB reserve raises these by 1 dB; it is not an IARU minimum. [Drive matrix](../hardware/2m/review/M5A-R4/driver_budget.csv). The final's 500 MHz rating does not establish its 144 MHz gain. **Driver adequacy remains OPEN.**

GVA-84+ has no established advantage here. PHA-13HLN+ is not the default and no expensive cascade is added. The narrow [RD06HVF1 alternative](https://www.rfparts.com/old_site/pdf_docs/RD/rd06hvf1.pdf) has an actual 175 MHz/6 W/12.5 V reference and pins 1 gate/2 source/3 drain. Its [manufacturer EOL notice](https://www.anglia.com/registration/pcn_ptn/docs/ptn/SiRF%20TO-220%20EOL%20announcement_20220511.pdf) ended orders in December 2022. An SDR-Kits listing does not establish fleet-plus-spares allocation. It is not selected; there is no second full design.

## Coils and manufacturer pinout

L638 is **A05TJLC**, the original factory air-core family: 18.5 nH, five turns, Q ≥132 at 150 MHz, SRF 2.5 GHz and 4 A rise-current rating basis. Indexed cut-tape pricing is €1.51 at one/€1.28 at ten. Manufacturer landing dimensions still need transcription; inconsistent distributor axis ordering is insufficient. No invented wire diameter, pitch or DIY winding is claimed equivalent. Low-drive Murata 56 nH uses observed €0.102 pricing; 91/180 nH and exact bias-feed/LPF suffix availability remain explicit gaps. No ordinary power inductor replaces an RF part.

PD54008L-E top view has four gate contacts left, four drain contacts right and center SOURCE. Manufacturer page 13 recommends continuous 0.5 × 5 mm gate/drain regions and 2.7 × 5 mm source. The [local footprint](../hardware/2m/ARDF_2M.pretty/PD54008L_ST_GDS_5x5.kicad_mod) uses **G/D/S functional region names**, not invented generic numeric groups. Source paste/via/thermal construction remains OPEN. PHA-1+ is 1 input, 2 ground, 3 output/DC, 4 ground paddle. Its local candidate landing now transcribes DF782 Rev G (02/08/17): 1.4986 mm side pitch, 0.7112 × 1.4986 mm side lands and the dimensioned 5.334 mm ground pattern with 45° shoulders. Ground stencil/vias and the reference shoulder dimension require final review. TI's boost landing is also transcribed from RNW0013A drawing 4222804/C (11/2019): side pitch 0.5 mm, 0.7 × 0.25 mm lands at ±1.6 mm, three independent center bars at −0.55/0/+0.55 mm. Those bars are **6 PGND, 7 SW, 8 VOUT**, not a common grounded thermal pad. Mask-defined center openings and nine paste windows follow the drawing. ST D45H11 and BD139 are 1 base, 2 collector/tab, 3 emitter. The [pin audit](../hardware/2m/review/M5A-R4/pinout-audit.json) checks these landing dimensions separately from inherited pin assertions. No PCB pad audit is claimed without a PCB.
