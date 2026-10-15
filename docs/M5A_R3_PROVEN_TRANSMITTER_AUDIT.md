# M5A-R3 — proven transmitter audit

Dated 2026-10-15. **PRIVATE CONSTRUCTION DERIVATIVE / NOT RELEASED. All ARDF-TX hardware tests NOT_RUN.** No orders, PCB fabrication, assembly or transmission. M5A-R1 remains the archived fallback; RF80, M4A, the controller and accepted ADRs are unchanged.

The strongest complete AM construction is **DL3BBX, CQ-DL 5/1992 pp.289–292**. It is selected as the schematic foundation, **not accepted as a low-cost fleet implementation**. Its real circuit is preferable evidence to a transistor maximum-rating exercise. Present-day procurement and the requested maximum PEP are still open. No new final transistor has been invented.

## Sources actually inspected

| Source | What was inspected | Evidence and limits |
| --- | --- | --- |
| [DF1FO construction document](https://df1fo.darc.de/DOC/2mTX.doc), Word last-save2011-06-24 | Complete document converted to13-page PDF; MaxiTX schematic, assembly, winding, adjustment, power table and BOM | Publisher tested four prototypes; rectangular modulation, not measured70–80% sineAM |
| [MaxiTX Eagle schematic](https://df1fo.darc.de/Platinen/2mMaxiTX.sch), [board](https://df1fo.darc.de/Platinen/2mMaxiTX.brd) | Original binary files retrieved, headers inspected and hashed | Legacy Eagle4.16 binary; installed KiCad10 CLI could not load/export it. **Native Eagle net connectivity/layout NOT independently decoded.** Actual circuit traced from the author's construction schematic; no claim of successful Eagle import |
| [DF1FO corrections](https://df1fo.darc.de/Sender/SenderErgaenzungen.html), [build gallery](https://df1fo.darc.de/Sender/SenderGalerie.html) | Author corrections and named completed builds | Earlier OE6GC2N5109 power report was not reproduced by other builders; this is not a qualified substitute for KT610b |
| [DL3BBX full article](https://www.robkalmeijer.nl/techniek/electronica/radiotechniek/hambladen/cq-dl/1992/page289/index.html) | Entire article, Fig2 schematic, Fig3 two copper views, Fig4 placement, Fig5 BOM, alignment and permission paragraph | Author-reported >3WPEP at13.8V, >90% modulation and real construction. No independent calibrated RF measurements supplied |
| [Dutch historical documentation](https://fox.ardf.veron.nl/Documenten/Hall_of_Fame/ARDF_ontwikkeling_in_Nederland.pdf), printedpp15–16,19 | Actual G3ZOI TRO-2 schematic Fig43 and completed PA0DFN/PA7KY builds; PA0JBG/PA0DFN modulated VHF experience | Supporting circuit evidence. Current [G3ZOI document index](https://www.qsl.net/g3zoi/docs/) did not provide the complete historical1W2m construction pack. Unrelated micro-transmitters were excluded |

Downloaded-source hashes/access limitations are in [sources.json](../hardware/2m/review/M5A-R3/sources.json). No full article or copyrighted construction document is redistributed here.

## DF1FO MaxiTX: actual RF path

ICS525/5V source → C12,22pF trimmer → KT610b. Its base has L5, five turns0.8mm silver-plated wire,6mm inside diameter,0.8mm spacing, through DR2 to ground. Collector feed is BC328 high-side supply modulator T1 → DR1 → L1,12 turns0.4mm enamel wire,3mm inside diameter, close wound. Modulator R1=10k emitter/base, R2=1.5k toward key transistor, C7=1uF base/collector; C8/C10=22n supply bypass. Ferrite beads use the author's1.5-turn recipe.

Collector → C14=33p → L2,5turns → C16=22p shunt → L3,3turns → C17=22p shunt → L4,3turns → C18=22p shunt/output. L2–5 use0.8mm silver-plated wire,6mm ID/0.8mm spacing. Coils stand2mm above the board. The KT610b stud uses a4mm hole, body cooled into board ground, leads bent45° about2mm from body. Original B/C/E drawing exists, but an exact genuine stocked manufacturer package/pin-number specification was not established; **no generic TO39 substitution**.

The57×62mm board retains rectangular high-side supply modulation. Author measurements:

| Battery | RF peak | RF time-average under original rectangular modulation | Battery current |
| --- | --- | --- | --- |
|12V|1.2W|0.6W|150mA|
|10V|1.0W|0.5W|135mA|
|8V|0.7W|0.4W|120mA|
|6V|0.4W|0.2W|100mA|

These are **not AM carrier ratings**. At1.2W PEP,80% sineAM and−1dBd, the calculated ERP is only0.294W, or0.234W with1dB capability reserve. Native low-voltage operation is attractive but cannot preserve the upper-power objective. Published harmonic observations are approximately−40dBc second/−60dBc higher; original PLL products roughly−45…−50dBc. They do not qualify a Si5351 derivative. KT610 supply and the unreproduced2N5109 alternative prevent a current-production fleet recommendation.

The published MaxiTX union of electronic references is54 positions:25 capacitors,11 resistors/trim,4 transistors,3ICs,2diodes,2crystals,2ferrite chokes and5wound coils. It includes alternative crystal/measurement populations, so54 is **not one variant's fitted count**. Socket, headers, jumpers, mechanics and board are additional. Frequency/timer functionality is included there but training, ARDF-TX interlocks and battery conversion are not. Native Eagle count was not recovered; this is a manual published-BOM count, not a netlist assertion.

## DL3BBX: component-level reconstruction

Original chain:36MHz BFY90 oscillator → BF981 T2 doubler72MHz → BF981 T3 doubler144MHz →2N4427 T4 →MRF237 T5. Retain T3/T4/T5; drive the existing T3 input tank from a filtered programmable72MHz source through original C11=1.2p. This avoids inventing a144MHz driver for unknown TP5 impedance/drive. Original L4/C13 input resonator remains.

| Original block | Exact retained values/connections | Disposition |
| --- | --- | --- |
| T3 input | C11=1.2p coupling; L4=00511732 green,170nH catalog; C13=18p shunt; R9/R10=33k gate2 divider; C12=1n | Retain. New source voltage/termination is an explicit adaptation, not proved equivalent |
| T3 drain/source | R14=100ohm to feed,L5=00511830 red to TP5,R11=47ohm between TP5 and drain; C14=1n feed bypass; R12=100ohm source,C16=1n bypass | Retain; R11 is a drain-series resistor, not gate feedback |
| T4 | C15=15p TP5/base,R13=100ohm base/ground; emitter R15=47ohm||C18=1n; DR2=6.8–10uH feed,L6=00511631 yellow,C17=1n feed/ground,C19=25p trimmer collector/final base | Retain. **C17 is a feed bypass, not1n across L6. R13 is100ohm, not33k** |
| T5 | MRF237 emitter ground,R16=100ohm base/ground; modulated supply →VK200 DR4 → DR3=2.2–6.8uH →collector; C20/C22=1n feed bypass | Retain electrical circuit; exact manufacturer/package remains unresolved |
| Output | Collector C21=33p →L7=00511830 →(C23x=39p parallel C23=45p trim to ground)→L8=00511631→output,C24=33p shunt | Retain original matching/filter topology and tuning. No imported500MHz or guessed LDMOS impedances |
| AM | BD676 emitter UB,collector PA feed; R26=10k base/emitter,VR2=100k base/collector; VR1=47k audio divider,R24/R25=2.2k,C27=100n film shunt,C26=330n film AC coupling; C25=470u upstream | Retain mechanism. TIP127 package modernization and filtered sine replace BD676/NE555 respectively |

Native R3 reference assertions check36 original two-terminal value/net positions and pot connectivity. This is a transcription regression test; it cannot prove physical performance.

Seven alignment adjustments remain: L4,L5,L6,C19,L7,C23,L8. Original T4 must stand≥10mm above board and may need cooling; T5 was mounted against top ground copper. Fig3/4 give practical placement, but no calibrated CAD land pattern or native DL3BBX board file was located.

The original Fig5 union BOM counts90 references:28 resistors including optional R22x,2pots,35capacitors including C23x,12coils/chokes,8transistors,2ICs,1crystal and2detector diodes. The external detector consumes R27/C33/C34/D1/D2; excluding it and optional R22x gives84 main-circuit electronic positions, before connectors/cooling. Original contest scheduling is external and there is no separate training output or Li-ion conversion. These counts are not comparable to a complete247-position ARDF-TX assembly without those scope differences. R3 retains34 positions in its reference-RF block; frequency/source/safety/conversion/AM/training account for the rest. This records the complexity rather than claiming the integrated design has the historical bare circuit's parts count.

Two important discrepancies remain visible: the article once calls **C20** an initial trimmer, whereas schematic/BOM clearly identify **C23**; and current Neosid catalog p3.29 gives00511830 **55–70nH**, while the historical article labels it51nH. Original part number is retained; nominal range/actual core must be confirmed rather than silently using a51nH chip. Yellow00511631 is29–34nH with3.5turns; red00511830 is4.5turns/F100b in the current catalog.

Original warning: sharply tuned hardware may self-oscillate while the original oscillator is disabled. Author remedies: adjust L5 or add5.6p from T4 base to ground. R3 retains a DNP position for that documented correction **and independently interrupts the normal rail and source outside SLOT**.

## G3ZOI and Dutch supporting experience

Fig43 is the real2004 TRO-2, not the tiny training transmitter:5V ICS525 → tuned input →BFW16A, with BD682 series collector-supply modulation driven by the tone signal and separate level adjustment. PIC16F84 timing is unrelated to ARDF-TX's RF requirement. Text also describes an earlier2N4427 version with TO39 heat sink at12V; PA3BWD built a set. The1W label has no calibrated sine-AM carrier/PEP conditions in this source, so it cannot fill a4–5W PEP evidence gap.

PA0DFN Bosch KF163 reuse shows final-stage supply modulation and adjustable power in operational transmitters. UV-3R modification experience supports the mechanism, not a5W AM carrier claim. No UV-K5/K6 revision investigation was reopened. The incomplete historical G3ZOI construction archive is supporting evidence, not the selected production schematic.

## Evidence and permissions

Publisher reports and build photographs establish that the **original circuits worked**. No independent measurement establishes ARDF-TX power, AM depth, thermal behavior, spectral compliance or endurance. All derivative measurements remain NOT_RUN. The DL3BBX permission paragraph permits attributed private construction; commercial exploitation needs the author's written permission. See [license scope](../hardware/2m/LICENSE-REFERENCE-DL3BBX.md). Author/private-construction permission is not an open-hardware commercial license or legal radio authorization.
