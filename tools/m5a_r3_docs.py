#!/usr/bin/python3
"""Write the requested R3 engineering review from final machine-readable ledgers."""
import csv
import hashlib
import json
from pathlib import Path
from m5a_r3_design import ROOT,DEST,OUT,ARTICLE

def write(name,text):(ROOT/'docs'/name).write_text(text.strip()+'\n')
def table(head,rows):return '| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+''.join('| '+' | '.join(map(str,r))+' |\n'for r in rows)

def main():
    costs=json.loads((OUT/'costs.json').read_text());v=json.loads((OUT/'verification.json').read_text())
    calc=json.loads((OUT/'electrical-calculations.json').read_text())
    parts=json.loads((DEST/'RF2M.electrical.json').read_text())['parts']
    full=next(x for x in costs['summary']if x['variant']=='BOOST2S'and x['fleet']==10)
    buck=next(x for x in costs['summary']if x['variant']=='BUCK4S'and x['fleet']==10)
    train=next(x for x in costs['summary']if x['variant']=='TRAIN_ONLY'and x['fleet']==10)
    budget=table(['Population','6 boards, EUR/unit','10 boards','20 boards','Physical parts / IC'],[[mode]+[f"{next(x for x in costs['summary']if x['variant']==mode and x['fleet']==q)['net_eur_allowance']:.2f}"for q in [6,10,20]]+[f"{next(x for x in costs['summary']if x['variant']==mode)['physical_components']} / {next(x for x in costs['summary']if x['variant']==mode)['IC_count']}"] for mode in ['BOOST2S','BUCK4S','TRAIN_ONLY']])
    common='Dated 2026-10-15. **PRIVATE CONSTRUCTION DERIVATIVE / NOT RELEASED. All ARDF-TX hardware tests NOT_RUN.** No orders, PCB fabrication, assembly or transmission. M5A-R1 remains the archived fallback; RF80, M4A, the controller and accepted ADRs are unchanged.'
    write('M5A_R3_PROVEN_TRANSMITTER_AUDIT.md',f'''# M5A-R3 — proven transmitter audit

{common}

The strongest complete AM construction is **DL3BBX, CQ-DL 5/1992 pp.289–292**. It is selected as the schematic foundation, **not accepted as a low-cost fleet implementation**. Its real circuit is preferable evidence to a transistor maximum-rating exercise. Present-day procurement and the requested maximum PEP are still open. No new final transistor has been invented.

## Sources actually inspected

| Source | What was inspected | Evidence and limits |
| --- | --- | --- |
| [DF1FO construction document](https://df1fo.darc.de/DOC/2mTX.doc), Word last-save2011-06-24 | Complete document converted to13-page PDF; MaxiTX schematic, assembly, winding, adjustment, power table and BOM | Publisher tested four prototypes; rectangular modulation, not measured70–80% sineAM |
| [MaxiTX Eagle schematic](https://df1fo.darc.de/Platinen/2mMaxiTX.sch), [board](https://df1fo.darc.de/Platinen/2mMaxiTX.brd) | Original binary files retrieved, headers inspected and hashed | Legacy Eagle4.16 binary; installed KiCad10 CLI could not load/export it. **Native Eagle net connectivity/layout NOT independently decoded.** Actual circuit traced from the author's construction schematic; no claim of successful Eagle import |
| [DF1FO corrections](https://df1fo.darc.de/Sender/SenderErgaenzungen.html), [build gallery](https://df1fo.darc.de/Sender/SenderGalerie.html) | Author corrections and named completed builds | Earlier OE6GC2N5109 power report was not reproduced by other builders; this is not a qualified substitute for KT610b |
| [DL3BBX full article]({ARTICLE}) | Entire article, Fig2 schematic, Fig3 two copper views, Fig4 placement, Fig5 BOM, alignment and permission paragraph | Author-reported >3WPEP at13.8V, >90% modulation and real construction. No independent calibrated RF measurements supplied |
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

Native R3 reference assertions check{v['original_network_checks']} original two-terminal value/net positions and pot connectivity. This is a transcription regression test; it cannot prove physical performance.

Seven alignment adjustments remain: L4,L5,L6,C19,L7,C23,L8. Original T4 must stand≥10mm above board and may need cooling; T5 was mounted against top ground copper. Fig3/4 give practical placement, but no calibrated CAD land pattern or native DL3BBX board file was located.

The original Fig5 union BOM counts90 references:28 resistors including optional R22x,2pots,35capacitors including C23x,12coils/chokes,8transistors,2ICs,1crystal and2detector diodes. The external detector consumes R27/C33/C34/D1/D2; excluding it and optional R22x gives84 main-circuit electronic positions, before connectors/cooling. Original contest scheduling is external and there is no separate training output or Li-ion conversion. These counts are not comparable to a complete247-position ARDF-TX assembly without those scope differences. R3 retains34 positions in its reference-RF block; frequency/source/safety/conversion/AM/training account for the rest. This records the complexity rather than claiming the integrated design has the historical bare circuit's parts count.

Two important discrepancies remain visible: the article once calls **C20** an initial trimmer, whereas schematic/BOM clearly identify **C23**; and current Neosid catalog p3.29 gives00511830 **55–70nH**, while the historical article labels it51nH. Original part number is retained; nominal range/actual core must be confirmed rather than silently using a51nH chip. Yellow00511631 is29–34nH with3.5turns; red00511830 is4.5turns/F100b in the current catalog.

Original warning: sharply tuned hardware may self-oscillate while the original oscillator is disabled. Author remedies: adjust L5 or add5.6p from T4 base to ground. R3 retains a DNP position for that documented correction **and independently interrupts the normal rail and source outside SLOT**.

## G3ZOI and Dutch supporting experience

Fig43 is the real2004 TRO-2, not the tiny training transmitter:5V ICS525 → tuned input →BFW16A, with BD682 series collector-supply modulation driven by the tone signal and separate level adjustment. PIC16F84 timing is unrelated to ARDF-TX's RF requirement. Text also describes an earlier2N4427 version with TO39 heat sink at12V; PA3BWD built a set. The1W label has no calibrated sine-AM carrier/PEP conditions in this source, so it cannot fill a4–5W PEP evidence gap.

PA0DFN Bosch KF163 reuse shows final-stage supply modulation and adjustable power in operational transmitters. UV-3R modification experience supports the mechanism, not a5W AM carrier claim. No UV-K5/K6 revision investigation was reopened. The incomplete historical G3ZOI construction archive is supporting evidence, not the selected production schematic.

## Evidence and permissions

Publisher reports and build photographs establish that the **original circuits worked**. No independent measurement establishes ARDF-TX power, AM depth, thermal behavior, spectral compliance or endurance. All derivative measurements remain NOT_RUN. The DL3BBX permission paragraph permits attributed private construction; commercial exploitation needs the author's written permission. See [license scope](../hardware/2m/LICENSE-REFERENCE-DL3BBX.md). Author/private-construction permission is not an open-hardware commercial license or legal radio authorization.
''')
    write('M5A_R3_COMPONENT_MODERNIZATION.md',f'''# M5A-R3 — component modernization and sourcing

{common}

**No current-production, quote-backed fleet RF component set was established.** The chosen circuit is a faithful review candidate with a blocked physical implementation, not a claim that NOS labels prove reproducibility.

| Original function | R3 choice | Why/change | Current evidence and pin/package consequence |
| --- | --- | --- | --- |
| Crystal oscillator/first doubler | Si5351 plus gated72MHz fundamental filter | Programmability; removes T1/T2 and original local scheduler | CLK0=RF/2, retained T3 doubles; CLK2=RF for training. Same PLL_A=6×RF with MS0=12/MS2=6. New input level requires end-to-end alignment |
| T3 BF981 | Philips BF981 retained | Retain original doubler and matching; do not substitute an unqualified BF998 | [Dönberg](https://www.donberg.ie/search?group=&maxlines=100&page=1&query=PHILIPS&wordflag=and) lists Philips,pack5/€15net. Six boards allocate10devices,€5/board;10/20 allocate€3. NOS quantity/spares not confirmed. [Philips Dec1990](https://datasheet.octopart.com/BF981-NXP-Semiconductors-datasheet-180991380.pdf),p155:1S2D3G2 4G1,SOT103; physical landing OPEN |
| T4 2N4427 | Central2N4427 numeric symbol; exact supplier manufacturer OPEN | Retain RF stage, not a new MMIC | [Central datasheet/PDN](https://my.centralsemi.com/datasheets/2n4427.PDF):1E2B3C,TO39,400mA. Appended PDN01114(2019) explicitly EOL. [Dönberg](https://www.donberg.ie/catalogue/semiconductors/semiconductors_2-2n/2n_4427.html) €5.90net,pack1,unidentified maker. **Not a Central quote**;≥10mm body stand-off/possible sink retained |
| T5 MRF237 | ASI MRF237 evaluation symbol ONLY | Exact original part family, not a newly designed LDMOS PA; manufacturer remains unresolved at available EU listing | [ASI manufacturer datasheet RevA, mirror](https://pdf.dzsc.com/F23/MRF237.pdf):1E2B3C,TO39,1A,22°C/W. [Manufacturer MRF catalog](https://www.adsemi.com/families/MRF) lists device, no fleet quote or delivery commitment. [Dönberg](https://www.donberg.ie/catalogue/semiconductors/semiconductors_md-mz/mrf_237.html) €31.90net,pack1 but maker unspecified. **Cannot apply that listing to ASI as verified sourcing** |
| Motorola MRF237 alternative identity | Not substituted into ASI symbol/PCB | User warned physical manufacturer variants differ | [Original Motorola sheet](https://datasheet4u.com/pdf/1114783/MRF237.pdf) specifies case79-03 STYLE5 and **640mA** continuous, not ASI1A. Retrieved two-page sheet lacks the separate complete case-style pin legend. Motorola numeric pin mapping remains UNVERIFIED. Original article's1A statement cannot override the exact maker's sheet |
| L4–8 | Original Neosid00511732 /00511830 /00511631 | Keep factory tuning coils and original coupling/placement | [Neosid geometry/table](https://neosid.de/import-data/product-pdf/neoFilterspulen_5_7_10.pdf),p3.29,7.1E:bottom view A/E,7.5mm can dimension,12mm height,3.5±0.3mm leads. Current [red-coil listing](https://neosid.de/produkte/filter-und-spulenbausaetze/abgleichbare-filterspulen/53506/helix-filter-7.1e/51-nh) conflicts in nominal label with catalog range. [BEC](https://bec.co.uk/product-category/neosid/helix-filter-7-1e-51-nh/) says in stock,price by request. €3 each is **estimate**, not quote; count/lot/landing confirmation OPEN |
| DR2/3/4 | Original choke ranges and VK200 construction | No arbitrary RF chip substitution | Exact current maker, SRF/current, mechanical outline and supply OPEN. Minimum requirements and ranges are on schematic. Not counted as qualified magnetics |
| BD676 T8 | ST TIP127 | Currently listed ST Darlington; same series collector-supply mechanism, different package | [ST product](https://www.st.com/en/power-transistors/tip127.html), [DS0854 Rev5](https://www.st.com/resource/en/datasheet/tip127.pdf):1B2C/tab3E,TO220. Original onsemi BD6761E2C3B is **not pin-compatible**. Retain bias/filter values; recalibrate current, carrier and sine depth. €0.75 estimate,not factory500-unit price |
| NE555/local timing | Common ESP32-S3 filteredPWM, existing RF2M reconstruction | Avoid duplicate contest controller; provide sineAM | No S3 analog DAC assumed. Preserve AF filter and Darlington input mechanism; controller must store new revision-specific calibration |
| R0/R1 premium driver/final chain | Removed from active R3 | Not the selected proven RF circuit | PHA-1+/PHA-13HLN+,PD54008/PD55008,D45H11 and dedicated5V MMIC regulator absent from fitted R3 positions; original fallback archived |

RF Parts genuine Motorola/Microsemi listings encountered export restrictions; they are not booked as a German fleet source. Marketplace assertions and broker inventories were not accepted as production sourcing. No contacts or quote requests were sent.

## Physical pin audit versus actual footprint readiness

[Machine-readable pin audit](../hardware/2m/review/M5A-R3/pinout-audit.json) checks **{v['pin_assertion_count']} numeric schematic device maps** against actual exported nets. It explicitly separates verified terminal numbers from approved PCB landings. Mutations swapping ASI base/collector, Central emitter/collector, TIP127 base/emitter and BF981 gates must fail.

**No RF power footprint is guessed.** Q901/Q902/Q903 lack approved footprints. SOT103 lead trimming, original TO39 height/cooling and exact final manufacturer must be resolved together. The ASI drawing does not authorize placing a different MRF237 maker on its pin numbering. TIP127 tab is modulatedVPA; use electrical insulation from ground/other live devices and account for interface thermal resistance. Choke/trimmer/connector geometry and TPS611781 RNW landing are also OPEN.

There are{len([p for p in parts if not p['footprint']and not p['ref'].startswith(('#','TP'))])} unset physical footprint fields, including optional populations; ERC's warning count is smaller because some custom symbols have no footprint filter. **An unflagged custom symbol is not a qualified footprint.** The PDF/netlist are electrically reviewable; a manufacture-ready PCB is not defensible yet.
''')
    write('M5A_R3_RF_SELECTION.md',f'''# M5A-R3 — reference selection

{common}

**Select DL3BBX as the one schematic foundation. Do not adopt this BOM as the fleet replacement.** It is the only fully traced mandatory candidate that publishes several watts PEP with working supply AM. It still does not prove the retained upper-ERP/headroom target and it is presently more expensive than R1.

| Same-scope consideration | DF1FO MaxiTX | DL3BBX derivative selected for review | G3ZOI historical1W |
| --- | --- | --- | --- |
| Built evidence | Four prototypes and several named reproductions | Article reports real construction and >3WPEP/>90% AM | Dutch documentation shows schematic/completed sets |
| Maximum reported power |1.2W **peak**,12V,rectangular modulation |**>3WPEP**,13.8V; lower bound, not a maximum measurement |1W label without usable calibrated sineAM carrier/PEP conditions |
| At−1dBd/80%AM |1.2W permits0.294WERP,0.234W with1dB reserve |3W reference permits0.736WERP,0.584W with1dB reserve; actual maximum unknown |No justified4–5W PEP evidence |
| RF adaptation | ICS525→Si5351; KT610 drive/cooling, sine modulator changes | Remove first oscillator/doubler; retain T3/T4/T5, original L4–8 and matches; replace tone source/pass package | Incomplete original construction pack, legacy final |
| Tuning/construction | One principal trimmer plus reproducible wound coils | Seven adjustments, legacy factory coils, TO39 heat/stand-off; more work | Complete current alignment/layout source not found |
| Current parts | KT610b genuine fleet supply/pin map unresolved | BF981 NOS, Central2N4427 EOL, exact MRF237 maker/lot unresolved | BFW16A/2N4427 legacy sourcing unresolved |
| Normalized complete cost |Not quoteable: KT610 identity/source and original source-interface adaptation unresolved; historical bare design prices excluded|Full2S **€{full['net_eur_allowance']:.2f}** at10 including common source/safety/training; conditional allowances|Not quoteable from incomplete source/BOM; no invented quantity discounts |

## Precisely what is reused

Three of the five original RF stages remain: BF981 second doubler,2N4427 driver and MRF237 final. The five retained adjustable coils, interstage trimmer and output network retain original identities and connectivity. **{v['original_network_checks']} two-terminal reference positions** plus two pots are regression checked. Original Darlington collector-supply modulation, DC collector-feedback trim and audio RC/AC-coupling path remain. The proposed TIP127 is a package/current-source modernization; it has not inherited the original's RF/thermal measurements.

The removed T1/T2 crystal/multiplier circuitry, NE555 audio oscillator, and external historical timer are replaced by the existing common controller and synthesizer. A72MHz fundamental filter and source gate are new. Keeping one multiplier is deliberate: TP5 is not a documented50ohm node, and replacing everything with Si5351 at144MHz would introduce a new drive/matching problem. The revised source drive is still an acceptance gate, not presumed identical to the original tuned oscillator amplitude.

The existing separate training RF circuit and independently tested VHF interlocks remain. There is no new PA coupon, PA-family search, new MCU or fourth board. The GPIO connector is unchanged, but **passive revision IDs change**. **Normal CLK0 programming changes from RF to RF/2**, so R1 configuration must not run against R3. Same PLL can feed direct-RF training CLK2.

## Complete R3 controller contract

J101 remains a20pin2.54mm keyed header candidate; exact manufacturer/mating geometry OPEN. Logic is0–3.3V, maximum intended3.465V. Host must not drive an unpowered RF board; no arbitrary hot-plug/backpower tolerance is promised. Separate J301 carries protected battery and its power return; no PA current in J101. Target3.3V budget≤150mA, to be measured. Ground contacts2/17/18 serve logic/AF return; RF/PA currents return separately to the battery star, not through them.

| Pin | Net / direction at module | R3 behavior |
| --- | --- | --- |
|1|V3V3 input|Regulated logic/source supply; ground first|
|2|GND|Logic return|
|3,4|I2C_SDA/SCL bidirectional|Dedicated VHF bus0x60,≤400kHz; RF80 also uses0x60, so do not share unisolated sources. Local source/I2C switching retained|
|5|ARM input|Fresh rising edge captures valid context/path/profile;100k pull-down; no automatic rearm|
|6|SLOT input|Scheduled carrier permit,100k pull-down; hardware gates normal source and rail|
|7|KEY input|Sine-tone Morse key inside SLOT; inactive during ARM;100k pull-down|
|8|PROGRESS input|Application progress edges≤100ms apart; independent TPS3431 lease/POR fail-off. Never free-run a hardware timer as application-liveness substitute|
|9|MUTE_N input|Low inhibits; defaults low|
|10|PA_RAIL_ADC output|Raw regulator rail divided by17,then1k series; about0.812V at13.8V. Verify before SLOT; train-only hard pull-down. ADC source impedance/acquisition calibration OPEN|
|11|PATH_TRAIN input|0normal/1training captured at ARM; default0|
|12|PROFILE_FULL input|0reduced/1full captured at ARM; default0; live changes do not transfer path/profile|
|13|AF_PWM input|Offset+sine312.5kHz PWM,initial800Hz tone;3.3V logic. Calibrated amplitude per profile; no S3DAC assumed|
|14|LEVEL_PWM input|Equal-offset no-tone reference; **not** the old D45H11 servo voltage-to-PA calibration|
|15|PREPARE input|Allows powered source/configuration; defaults0|
|16|FAULT_N output|Captured valid-arm indication through1k; low when disarmed/faulted, not a multiplexed telemetry bus|
|17,18|GND|Adjacent AF/control returns|
|19|MODULE_ID passive|**15k2S /33.2k4S /75ktraining R3**. Reserve distinct IDs; reject unknown/ambiguous readings and old R1 IDs12.1k/27.4k/47k. Host pull-up/ADC windows need qualification|
|20|PA_PREPARE input|Converter preparation;0in training. Cannot by itself enable RF|

Firmware must bind decoded R3 ID, pack population, source half-frequency mapping, legal country/profile, carrier/AM/ERP calibration and RTC schedule before ARM. No such firmware is implemented here. Supply raw/control independently only under the documented grounding/sequencing constraints. Do not share the normal-mode PWM scale or calibration from R0/R1's closed-loop supply modulator.

Sequence: controls low →stable3.3V/POR/progress →MUTE_N+PREPARE with ARM/SLOT/KEY low →configure/read back source with RF gates off →prepare converter →check correct regulator rail/profile →fresh ARM with valid context →wait≥50ms/confirm status and rail →scheduled SLOT →key only sine tone →clear SLOT,ARM,PA_PREPARE,PREPARE before retuning. After any fault diagnose and repeat from controls low; restoring health with ARM high never rearms. Physical RC/reset/inrush/quiet timing still requires measurement.

## Why no integrated PCB is claimed

The exact purchasable RF-device manufacturer/physical package is unresolved, and the Neosid current red-core range conflicts with the historical nominal. No final footprint is assigned by generic transistor name. Original Eagle4.16 binary import was unavailable; original DL3BBX layout is a published raster, not a calibrated native PCB file. A fabricated complete board with guessed pin order/coil geometry would violate this task.

The shortest practical correction is **one confirmed RF component set with spare quantities and exact package evidence**, plus Neosid range/geometry confirmation, followed by one integrated board using the original RF placement. It is not a separate RF-transistor characterization program. The present result is a complete editable **candidate schematic**, with explicitly OPEN physical implementation. It is neither proof of a low-cost fleet nor authority to lay out/order unresolved parts.
''')
    # Energy table from the reproducible rows, no endurance claim.
    erows=list(csv.DictReader((OUT/'endurance.csv').open()))
    energy_table=table(['2S pack / cell basis','Full hours, modeled','Reduced hours, modeled','12h /24h arithmetic'],[[pack+' / '+cell]+[f"{float(next(x for x in erows if x['pack']==pack and x['cell_basis']==cell and x['profile']==mode)['hours_calculated']):.1f}"for mode in ['full','reduced']]+['NOT qualified hardware']for pack in ['2S2P','2S3P','2S4P']for cell in ['25R_2450mAh_min','M35A_min_energy']])
    write('M5A_R3_AM_AND_POWER.md',f'''# M5A-R3 — sine AM, power and endurance

{common}

## Requirements remain unchanged

[IARU PartB2025 Appendix1 T2.8/T2.4](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf),p10, rechecked2026-10-15:144.500–144.900MHz championship carrier, stability better than50ppm, concurrent transmitter spacing **>200kHz**,0.25–1W carrierERP,A2A,70–80%AM,8–15WPM,horizontal antenna at2–3m, applicable national unwanted-emission limits, no unscheduled radiation. This competition document does not grant legal transmitter authorization. Existing country/profile/legal requirements remain in [M1 regulatory baseline](M1_REGULATORY.md).

Using the **unqualified**−1dBd net antenna/feed assumption:

| ERP carrier | Conducted carrier | Mean RF at75%AM | PEP at80%AM | Capability with1dB reserve |
| --- | --- | --- | --- | --- |
|1W|1.2589W|1.6130W|4.0789W|5.1351W|
|0.90W|1.1330W|1.4517W|3.6710W|4.6215W|
|0.30W|0.3777W|0.4839W|1.2237W|1.5405W|

`PEP=Pc(1+m)^2`; mean RF=`Pc(1+m²/2)`. Published DL3BBX output is at its50ohm connector after its original matching/filter; do not subtract that same network twice. Any subsequently added output filter/cable loss must be charged separately. At−1dBd,3WPEP is1.33dB short of4.079W,2.33dB short of5.135W. MaxiTX1.2W is5.31dB/6.31dB short respectively. **DL3BBX reports greater than3W, not an upper ceiling of3W.** Its actual maximum clean sineAM PEP remains unknown. A positive antenna-gain assumption must not be invented to close this gap.

The upper target stays open; the schematic is not silently redefined as a0.58W transmitter. A measured lower level could be competition-appropriate, but adopting it as the normal product target requires explicit review. A0.30W reducedERP setting with±0.4dB total uncertainty would span0.274–0.329W; a0.90W full setting spans0.821–0.987W. These are calibration examples; neither actual uncertainty nor antenna gain has been measured.

## Actual AM implementation

ESP32-S3 provides coherent `LEVEL_PWM` DC/carrier-reference and `AF_PWM` offset+sine, initially800Hz at312.5kHz PWM. Two unity Sallen-Key sections use10k/10k and4.7n/4.7n with TLV9004. Their equal-component unity-gain Q=0.5 and natural frequency3386Hz give calculated attenuation0.947 at800Hz and0.000117 at312.5kHz, approximately−78.6dB ideal PWM-frequency attenuation. These are small-signal filter calculations, not measured switching spur levels.

KEY selects AF or equal-offset carrier reference via SN74LVC1G3157. SLOT keeps a carrier present for the scheduled interval; KEY keys the sine tone, not RF/FM/FSK. **No RF outside SLOT.** Match both DC offsets and ramp audio over a few tone cycles in future firmware to avoid steps; no production firmware is implemented.

The command feeds original VR1=47k →R24=2.2k →C27=100n film shunt →R25=2.2k →C26=330n film →TIP127 base. Original R26=10k to emitter and VR2=100k base/collector set carrier supply by negative collector feedback. **Before power, set VR2 for approximately100k from PASS_BASE to VPA; a short increases conduction.** Wiper2 is tied to end1; wiper at end1 gives maximum effective resistance to end3. The pot cannot guarantee RF-off; source/rail hardware interlocks do that. The source is AC-coupled; a steady failed PWM does not create steady full modulation. PWM/carrier bias faults cannot be treated as protection against arbitrary mistimed SLOT; independent lease/mute remains essential.

At800Hz the extra original R24/C27 pole is near723Hz **only with low source impedance**; VR1 wiper resistance can lower it further. Tone amplitude must be calibrated after all filters. Available3.3V command peak, attenuation and Darlington beta may limit depth: **no assertion that3.3V automatically yields75%AM**. If the inherited input cannot reach70–80% without clipping, the smallest required audio-level correction must be reviewed. No high-power op-amp servo is reintroduced speculatively. RF envelope depth is measured from RF maxima/minima, not inferred from the supply waveform. THD≤5% is an initial engineering criterion, not an IARU rule.

## Envelope headroom and thermal limits

Original no-tone8V collector setting is not automatically suitable for80% sineAM. Ideal13.8V upstream with assumed2V pass dropout gives11.8V crest; for linear voltage transfer this implies6.56V center and1.31V trough. At8V center an80% ideal crest would be14.4V, already above the supply even before dropout. Actual RF amplitude-versus-collector-voltage transfer, knee and compression remain unknown; VR2 must be set from the RF envelope. Original rectangular >90% modulation does not prove sine linearity.

TIP127 replaces only the old PNP Darlington: ST1B/2C-tab/3E, live modulated collector tab,1.92°C/W junction-case,150°C maximum. At an **assumed**0.30A center current proportional to voltage, ideal pass dissipation is1.54W under80% AM,2.17W no-tone and2.18W maximum instantaneous. An overload illustration0.60A center doubles these losses and would exceed the present AM crest-current trip; it is not an operating setting. Exact hot DC/repetitive SOA is an OPEN acceptance gate; single-pulse curves cannot prove continuous audio safety.

A sizing example with3°C/W sink+1°C/W insulating interface,40°C ambient and4.35W no-tone overload gives57.4°C case and65.7°C junction. This is **not a qualified sink or sensor measurement**. Keep the approximate66°C NTC trip; do not raise it to accommodate an undersized sink. Thermal contact must represent the hottest case/spreader and account for delay, final-device junction/case rise and insulation. With ASI's22°C/W final junction-case,3W final waste alone adds66°C. The final and pass device cannot be declared safe from the same remote sensor without proving the case gradients and worst no-load/mismatch condition.

The original0.5–0.6A adjustment instruction is reconciled with Motorola's640mA maximum instead of copying the article's1A claim. R3's loaded-reference current trip is **{calc['rail_current_trip_a']:.4f}A nominal total normal-rail current**. RF AM crests plus driver current may reach this limit before the desired upper PEP. That is an explicit performance blocker; do not raise the limit or replace the final silently to force a number. ASI1A rating does not establish matching or thermal equivalence.

## Supply and safe sequencing

2S boost is preferred for a possible integrated private build: protected6.0–8.4V, TPS611781 fixed-population boost, captured profile selects nominal **{calc['boost_reduced_v']:.3f}/{calc['boost_full_v']:.3f}V**. 4S alternative TPS54302 selects **{calc['buck_reduced_v']:.3f}/{calc['buck_full_v']:.3f}V** from12.0–16.8V; full cannot be maintained below approximately14.4V loaded input. Refuse full-power SLOT when measured rail is low. Reduced4S is intended across the12V endpoint, subject to dropout validation. Do not book all4S capacity as full-power usable. Neither raw4S nor the wrong charger is allowed into a2S population; fixed assembly voltage windows and separate protected pack wiring remain.

Original470uF C25 is **upstream** of slot isolation/current sensing; local switched rail uses1uF plus bypass. Slot permission controls the normal rail as well as the72MHz source. Added1uF gate-source capacitor slows the isolation FET, and the existing final HC14 inverter gets10k/100n startup delay with Schottky/330ohm fast discharge. The100k RC pull-down is populated in training-only too. These prevent a known capacitor-inrush/startup ordering problem by design intent, **not measured timing qualification**. Approximate source delay is sub-ms to a fewms with thresholds/tolerances; rail withdrawal can take severalms. Require measured source-before-rail shutdown, bounded inrush, no self-oscillation, and deliberate rearm. The original self-oscillation warning makes source-only inhibit insufficient.

Nominal regulator and PA-rail OV trip is{calc['reg_and_VPA_OV_nominal_v']:.2f}V. TVS18V is not a precision clamp, converter failure/lead transients remain unqualified, and only a bounded current-limited bench supply may be considered for future initial bring-up. No unrestricted pack connection is approved. Reverse/input/rail FETs, comparator/INA180 and thermal window remain; no extra RF detector/ADC/controller added.

## Reproducible energy model — estimates only

Original500–600mA is a no-tone **alignment** current range. Budget0.55A at13.8V throughout each active slot as a conservative scenario; reduced0.30A at10.9V is **assumed**, not measured at0.30WERP. Add0.10W active source/audio allowance; converter efficiency87% boost/91% buck. Controller0.14W and RF idle0.04W are continuous assumptions. Duty20%, with no Morse discount. LoRa absent baseline; add0.006W intermittent or0.045587W continuous-RX plus modeled bursts scenario. Regulator idle is included in the0.04W allowance and must be measured separately.

2S full mean1.948W:12h23.37Wh; reduced0.955W:24h22.91Wh. Continuous full beacon9.019W; reduced4.054W. 4S model1.870/0.921W saves only about4% before inaccessible full-power capacity. Battery usable energy is cell-count×8.82Wh(2450mAh minimum class) or11.90Wh(M35A minimum-energy basis),×0.8aging×0.9temperature×0.9discharge-window. These inherited factors are assumptions; capacity datasheet endpoints and BMS voltage sag differ from the3V/cell design endpoint.

{energy_table}

Under this model2S2P2450 fails12h full and is just short of24h reduced; do not call it a robust minimum. **2S3P2450 or2S2P high-capacity** are the smallest modeled combinations with20% margin for both targets, not qualified packs. Exact current, cell resistance/cold behavior and achieved RF settings may change this result. At full budget and6V input, active battery current is about1.47A plus0.03A idle/controller; cell current divides by P. Converter/AM startup peaks require separate measurement.

4S1P and2S2P contain the same energy for the same cells. Full4S accessible fractions0.5/0.7/0.9 are sensitivity examples, not measured discharge integration.4S2P gives more modeled margin but cannot be guaranteed without a voltage-window capacity trace. Reduced4S1P2450 gives24.8h with little margin; high-capacity gives33.5h. Continuous full beacon on2S4P2450 is only5.1h, high-capacity6.8h; neither meets12h continuous. No endurance/RF-compliance PASS is claimed.

[RF arithmetic](../hardware/2m/review/M5A-R3/rf-power.json), [operating states](../hardware/2m/review/M5A-R3/operating-states.csv), [all packs and4S windows](../hardware/2m/review/M5A-R3/endurance.csv), [sensitivity](../hardware/2m/review/M5A-R3/sensitivity.csv), [thermal examples](../hardware/2m/review/M5A-R3/thermal-examples.json) are generated by `python3 tools/m5a_r3_models.py`. No transistor large-signal or analog transient simulation is claimed.
''')
    blocks=table(['Block, full2S at10','EUR/unit'],[[k,f'{value:.2f}']for k,value in full['blocks'].items()])
    delta=table(['Population','Fleet','R1 EUR','R3 EUR','Increase EUR','Parts R1→R3','IC R1→R3'],[[x['variant'],x['fleet'],f"{x['R1_net_eur']:.2f}",f"{x['R3_net_eur']:.2f}",f"{x['delta_net_eur']:+.2f}",f"{x['R1_parts']}→{x['R3_parts']}",f"{x['R1_IC']}→{x['R3_IC']}"]for x in costs['comparison']])
    write('M5A_R3_BOM.md',f'''# M5A-R3 — candidate BOM and economic result

{common}

**The low-cost replacement objective is not achieved.** At10 units the conditional full2S allowance is€{full['net_eur_allowance']:.2f}net, not€36 or€52.63. This is not a supplier-quoted buildable basket. MRF237/2N4427 listing manufacturers are unresolved; five adjustable coils are unquoted. No fictitious discounts or labor savings are booked.

{budget}

[Itemized6/10/20 BOM](../hardware/2m/review/M5A-R3/RF2M_BOM.csv) contains every fitted physical reference, exact/OPEN MPN, footprint, pooled demand, purchase-quantity allocation, MOQ/multiple, supplier identifier, price class and note. [Master positions](../hardware/2m/review/M5A-R3/RF2M_positions.csv) additionally shows DNP/test/declaration positions. Test pads/PWR_FLAG are not ICs or separately purchased components. Optional5.6p original correction is excluded from fitted totals and adds€0.10 allowance if fitted.

{blocks}

RF core cost drivers: MRF237 unbranded comparator€31.90;2N4427 unbranded comparator€5.90; Philips BF981 pack5,€3/unit at10; five Neosid adjustable coils **estimated€15 total**; two RF trimmers estimated€1.80 plus chokes/passives. The remainder includes complete programmable source, PWM/audio, training output, power conversion, ports and independent shutdown—not a bare PA comparison.

At10 the evidence split is€3.00 supplier-listed Philips BF981 with stock-count confirmation OPEN;€37.80 current **manufacturer-unmatched** price comparators;€{full['evidence_classes']['ESTIMATE_NOT_QUOTED']:.2f} estimates. None is a reservation or checkout quote. The actual RF-device purchase may cost differently or be unavailable. Dönberg's global€50 minimum is met by these fleet baskets, but it does not prove stock. Six transmitters need ten BF981 from five-piece packs; the four spare devices are fully allocated to the six-unit materials price, explaining€2/board difference. No discounts at20 are assumed.

## Before/after at identical functional scope

{delta}

R0 quantity-ten2S€74.61/4S€72.77, R1€52.63/€50.70, and R2's incomplete provisional module bridge€66.40 are historical candidate allowances, not validated prices. R3 costs more than all three. R2 never produced a new schematic/PCB. No new Mitsubishi pricing study was undertaken.

{full['physical_components']} fitted positions and{full['IC_count']} ICs compare with264/23 in R1 full2S. The RF-only replacement reduces an MMIC and its supply, but old power semiconductors and adjustable components dominate price. Common VHF logic uses six HC gate/register packages plus the small final gate, watchdog and POR—not a second contest processor. Existing VHF fail-off is retained rather than copying RF80's monostable system. The training population changes only unused normal inputs/terminations and keeps its independent RF branch; see [component delta](../hardware/2m/review/M5A-R3/component-delta.json).

Removing the€31.90 final entirely would still leave approximately€{full['net_eur_allowance']-31.9:.2f}; removing its cost **and all five€3 coil allowances** leaves€{full['net_eur_allowance']-31.9-15:.2f}. To match R1's€52.63, the final plus all five coils would have only€{52.6337-(full['net_eur_allowance']-31.9-15):.2f} combined. That is a transparent quote threshold, not a claim that such a price exists. Cheaper unknown MRF237 clones or invented coil substitutions are not the solution.

## Complete installed module scope

These additional **estimates**, not quotes, remain separate:

| External material per module |6|10|20|
| --- | --- | --- | --- |
| Two-layer bare PCB allowance, outline not designed |€6.00|€4.50|€3.50|
| External RF harness/strain relief, beyond board connectors |€3.00|€3.00|€3.00|
| Antenna/feed hardware allowance |€12.00|€12.00|€12.00|
| Heat sink, insulation, mounting allowance |€7.00|€7.00|€7.00|
| Full2S installed module including above |€{next(x for x in costs['summary']if x['variant']=='BOOST2S'and x['fleet']==6)['net_eur_allowance']+28:.2f}|€{full['net_eur_allowance']+26.5:.2f}|€{full['net_eur_allowance']+25.5:.2f}|

Bare-board numbers are planning placeholders because no qualified R3 layout/size exists; they are **not fabrication estimates from Gerbers**. Heat allowance does not establish thermal adequacy. Board RF connectors are already in component totals and not charged twice. Training-only excludes normal heat/supply/antenna hardware; add its own PCB, low-power antenna and harness, none of which has a current quote.

Controller, external protected battery/BMS, pack wiring, enclosure, charger/shared infrastructure, freight and labor are excluded from these module totals and remain separate system costs in [M2 battery cost](M2_BATTERY_COST_COMPARISON.md). Example controller€18/enclosure€5 allowances would add€23 before battery/charger. No complete finished transmitter price is claimed. Assembly/winding/alignment/testing minutes remain unknown; this historically proven circuit has **seven RF adjustments**, so lower labor than R1 cannot be asserted without evidence.

All values EUR net. Dönberg pages display23%VAT and state EU private-customer conditions; actual German checkout/OSS treatment must be confirmed. No universal19% addition or unsupported gross-to-net conversion was used. Freight, import and quotes remain OPEN.
''')
    write('M5A_R3_BUILD_PLAN.md',f'''# M5A-R3 — one integrated build and acceptance plan

{common}

**Build is presently NO_GO.** No PA coupon or repeated transistor-development program is requested. Resolve the short purchasing/package list and independent schematic review first; only then prepare one integrated PCB following the original RF placement. No procurement/layout/fabrication is authorized by this document.

## Before a board can be prepared

1. Confirm one genuine manufacturer-specific BF981/2N4427/MRF237 fleet set and spare stock, with supplier price/quantity/lead time and actual package drawings. An unbranded listing cannot be placed on the ASI pin map. Resolve Neosid00511830 range/core and all five coil outlines; approve original chokes/trimmers or explicitly re-review any change. Do not substitute another PA type.
2. Close the defined OPEN landings, particularly RF power packages, coils/trimmers, TPS611781 RNW and connectors. Preserve private-use attribution and obtain written author permission before commercial distribution. No article is copied into the handoff.
3. Independent reviewer checks the editable [RF2M schematic](../hardware/2m/RF2M.kicad_sch), [PDF](../hardware/2m/review/M5A-R3/RF2M.pdf), physical pin report and source-to-net table. Retain RF placement/ground copper from original Fig3/4; keep switching converter/source apart from final/output and training port. Do not assert the raster is a calibrated CAD board.

## Limited-step commissioning of that one board — all NOT_RUN

| Step | Action and limit | Pass / stop condition |
| --- | --- | --- |
|1 Inspection | Check actual device makers/pins; coil colors/values; TO39 geometry, T4≥10mm stand-off, final-to-ground thermal contact, TIP127 live-tab insulation; continuity/shorts | Every actual lead matches signed pin report; unconfirmed manufacturer STOP |
|2 Low-voltage control | Bounded3.3V bench supply initially100mA limit, PA battery absent. Configure clocks only into fixtures/dummy loads. Exercise reset, missing progress, MUTE, SCL, rawARM, invalid modes, heldARM recovery | Normal/training enables never overlap; no heldARM recovery after fault; RF normal source gate inhibited. Any unexpected state STOP |
|3 Power only | No RF source/final activation. Current-limited6–8.4V for2S population, initially0.1A input then raise only for dummy-load tests;4S only correct assembly. Verify rails on dummy load before RF; no direct pack | Boost10.90/13.81V or buck10.79/13.79V within reviewed tolerance; measure current trip≈0.594A, OV≈15.04V, NTC window/open/short. No oscillatory restart or overshoot exposing parts |
|4 Slot supply sequencing | Scope permit, NORMAL_RC/NORMAL_OFF, VMOD/VPA/current and source. Bound inrush at low energy; inspect470u upstream,1u switched rail and gateRC. Measure shutdown as well as start | RF source starts only after stable rail; clock disables promptly and drain discharges within a bounded interval. Initial engineering shutdown gate≤20ms total, source≤1ms, no unscheduled emission above documented analyzer floor. These are targets, not simulated PASS |
|5 Original RF alignment | One integrated board,50ohm≥10W load. Start reduced rail/current limit; original L4/L5 with≤1pF weak RF probe, then L6/C19, then L7/C23/L8. Do not confuse fixed C20 with C23 trimmer. Initial tuning pulses≤2s with cooling; no unattended carrier | Desired doubled RF, adequate drive and no self-oscillation. Do not exceed approved current/temperature. If source adaptation cannot drive retained chain, STOP for the smallest reviewed correction; do not start a separate PA redesign |
|6 Carrier and AM calibration | Set both PWM offsets equal, KEY initially0; set VR2 from RF carrier. Increase sine from small depth; use RF detector/oscilloscope at calibrated connector. Calibrate full/reduced converter and AF amplitude profiles |70–80% depth, nominal75%;≤5% engineering envelope THD; sidebands within1dB engineering symmetry; no clipping/strong AM-to-PM impairment. Expected ERP includes measured antenna/feed and uncertainty. Full target capability5.135W connectorPEP at m=.8 sizing basis, not claimed from original3W lower bound. If missing, do not silently lower target |
|7 Spectrum/thermal/faults | All required frequencies, both supply endpoints/profiles, carrier-only and sineAM; long active slot and continuous-beacon special case. Controlled mismatch/low-energy faults only; no destructive pack faults | Legal national unwanted-emission mask, <50ppm stability, output belowERP ceiling with uncertainty; safe maker-specific junction/SOA/case limits and66C sensor response. Inhibit/reset/lease/bus faults must remove both source and supply and require a fresh ARM |
|8 Training and final installation | Normal PA off/DNP; calibrate separateMCX1uW nominal, optional1–10uW fixed-pad variants. Exercise normal PA while observing isolated training port on one complete board. Horizontal omnidirectional antenna at2–3m | No electrical watt-path transfer, bounded off/normal-to-training coupling; initial isolation goal≥60dB and no damaging leaked power. Finite sensitivity/noise floor documented. Field range as separately agreed; no invented IARU2mtraining distance |
|9 Endurance and records | Log actual power, currents, temperatures, cell voltage/cutoff and modulation over12h full/24h reduced at20% scheduled duty; run continuous beacon separately | Both RF settings remain compliant for required duration under defined cell/temperature conditions. One serial-numbered end-to-end record per transmitter; modeled hours do not pass this test |

## Necessary shared instruments

Current-limited adjustable laboratory supply; calibrated50ohm≥10W dummy load; VHF power meter plus calibrated RF detector/oscilloscope or a power instrument that measures PEP; spectrum analyzer with suitable attenuation/protection; counter/reference; low-capacitance RF probe; DMM/current and temperature logging. VNA is useful to resolve a failed output/input alignment, not a separate mandatory development board. Use a rated low-capacitance probe for final collector peaks: probe capacitance itself alters VHF tuning. Exact instrument frequency/accuracy/noise floors must be recorded.

One full commissioning process may be performed by an experienced amateur-radio technician. Batch units then use the same recorded reference settings plus per-unit carrier/depth, spectrum, quiet/fault and thermal acceptance. Assembly/calibration labor remains unmeasured; it cannot be booked as savings. Unrestricted field use, continuous beacon operation and Li-ion pack activation require the prior safety/RF gates to pass and separate user authorization.
''')
    write('M5A_R3_REVIEW_DECISION.md',f'''# M5A-R3 — review decision

{common}

**NO_GO for integrated PCB commitment, procurement or replacing M5A-R1 as the fleet design.** A concrete DL3BBX-derived editable RF2M schematic and review package now exist. The evidence does not establish an affordable, currently sourceable near-upper-ERP transmitter, so the requested buildable-PCB outcome is **not complete**. No speculative PA has been substituted to hide the deficit.

The selected construction foundation is DL3BBX's physically built CQ-DL5/1992 circuit. Retained: BF981 last doubler,2N4427 driver,MRF237 final, five original adjustable coils and exact interstage/output network, collector-supply Darlington AM mechanism. New: local72MHz Si5351 drive/filter, filtered ESP32 sine, TIP127 package modernization, existing common-controller/training/fail-off integration and bounded startup sequencing. No premium driver chain, separate coupon, new MCU, Mitsubishi study or RF80 change.

## Concrete artifacts and verification

- [Editable root schematic](../hardware/2m/RF2M.kicad_sch),16 hierarchical sheets, [17-page PDF](../hardware/2m/review/M5A-R3/RF2M.pdf), [netlist](../hardware/2m/review/M5A-R3/RF2M.net.xml), [electrical manifest](../hardware/2m/RF2M.electrical.json).
- Actual KiCad10.0.6 ERC: **{v['erc_errors']} errors,{v['erc_open_footprint_warnings']} visible OPEN footprint-filter warnings**, no suppressed footprint check. Custom symbols can have unset landings without that warning; total unset physical footprint positions is separately audited. **ERC is not physical pin/AM/RF proof.**
- Exported-netlist/manifest parity across{v['parts_manifest']} positions; **{v['logic']['combinations']}** static logic combinations,**{len(v['logic']['scenarios'])}** state scenarios,**{len(v['mutation_tests'])}** deliberate mutations,**{v['pin_assertion_count']}** manufacturer-specific numeric pin maps,**{v['original_network_checks']}** reference value/net positions and{v['physical_enable_truth_rows']} physical enable truth rows pass.
- R1 original fallback remains at tag`m5a-r1` and [native archive](../hardware/2m/archive/M5A-R1/README.md). R0/R1/R2 review exports, RF80/M4A, README and accepted ADRs are hash-frozen. Existing R1 tests are rerun read-only against its archived native manifest/export; no historical PASS report is rewritten.
- **No PCB, DRC, Gerbers or 3D manufacturing views are claimed.** No board exists on which those checks could be meaningful. No hardware test, analog startup simulation or actual RF measurement was performed.

## Economics and performance conclusion

{budget}

R3 at10 costs€{full['net_eur_allowance']-52.6337:.2f} more than R1 full2S despite fewer parts ({full['physical_components']} vs264) and one fewer IC ({full['IC_count']} vs23). €31.90 final/€5.90 driver listings lack exact maker confirmation; coils estimated€15. Complete installed2S module allowance is€{full['net_eur_allowance']+26.5:.2f} at10, before controller/battery/enclosure/labor. These are conditional costs, not quotes. See [itemized BOM](M5A_R3_BOM.md).

MaxiTX cannot support the unchanged upper objective from its published1.2W peak. DL3BBX's **>3WPEP** with AM is the best primary evidence, but does not establish5.135W connector capability at the−1dBd/80% sizing basis. At exactly3WPEP that basis gives0.736WERP without reserve,0.584W with1dB reserve; no silent target reduction is accepted. Original rectangular modulation and substituted Darlington/source have **not** demonstrated70–80% sinusoidal RF AM. Current-limit crest margin, source coupling, stability and hot SOA remain open.

The2S boost is the preferred potential build supply;4S buck full-power capacity is constrained by≈14.4V loaded dropout. In the stated unmeasured budget2S3P2450 or2S2P high-capacity are the smallest packs with20% energy margin; RF output/endurance compliance is not established. Continuous full beacon endurance is far shorter. See [AM and power](M5A_R3_AM_AND_POWER.md).

## Smallest path to one complete transmitter

1. Obtain **one exact manufacturer-specific RF set and a priced6/10/20+spares supply strategy**, not broker claims; confirm the Neosid nominal/core/landings and original chokes/trimmers. This is a procurement-evidence/geometry gap, not an invitation to design a different PA. No quote requests have been sent without authorization.
2. Independently review this schematic and its source adaptation/current/thermal limits. Decide explicitly whether the actual legacy-parts price and seven adjustments are acceptable. If only a lower verifiedERP can be achieved, that requires an explicit product-target decision; the present target stays open.
3. Only after those blockers close, lay out **one integrated transmitter** using the original RF placement, prepare manufacturing review and obtain user authorization before purchase/fabrication. Commission it through the single [build/acceptance process](M5A_R3_BUILD_PLAN.md); no separate coupons or transistor-characterization program.

Private attributed construction is the only documented DL3BBX permission. Commercial distribution requires written author permission. Proposed ADR-0013 remains proposed; this milestone records a candidate/procurement NO_GO rather than silently amending an accepted architecture. R1 remains the fallback, also unqualified hardware.

The required owner review is therefore concrete: accept or reject the legacy construction's actual economic/supply constraints, and retain or explicitly revise the upper-power objective. **No manufacturing authorization is requested or assumed.**
''')
    (DEST/'LICENSE-REFERENCE-DL3BBX.md').write_text('''# DL3BBX reference restrictions

The M5A-R3 RF and Darlington modulation circuit is derived from Siegfried Pomplun, DL3BBX, “Leistungsfähiger UKW-Sender für Peilwettbewerbe”, CQ-DL 5/1992, pp.289–292. Original: https://www.robkalmeijer.nl/techniek/electronica/radiotechniek/hambladen/cq-dl/1992/page289/index.html

The article expressly permits attributed copying/printing and private construction. Commercial use requires the author's written permission. No commercial permission has been obtained. This is not an open-hardware commercial license. Do not assume the repository's software license grants rights in this reference-derived hardware. No full original article is redistributed. KiCad standard-symbol licensing is recorded separately in LICENSE-KICAD-SYMBOLS.md.

R3 is an unvalidated private-construction engineering candidate. Earlier R0/R1 files and their provenance remain separate. No statement here is a substitute for checking applicable permissions before external commercial distribution.
''')
    print('Seven requested M5A-R3 documents and reference-license notice generated')

if __name__=='__main__':main()
