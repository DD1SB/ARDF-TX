#!/usr/bin/python3
"""Write R4 review documents from verified CAD, population and cost ledgers."""
import csv
import json
from m5a_r4_design import ROOT, OUT


def table(header, rows):
    return '\n'.join(['| ' + ' | '.join(header) + ' |',
                      '| ' + ' | '.join(['---'] * len(header)) + ' |'] +
                     ['| ' + ' | '.join(map(str, row)) + ' |' for row in rows]) + '\n'


def read_csv(name):
    with (OUT / name).open() as stream:
        return list(csv.DictReader(stream))


def main():
    costs = json.loads((OUT / 'costs.json').read_text())
    verified = json.loads((OUT / 'verification.json').read_text())
    calc = json.loads((OUT / 'calculations.json').read_text())
    erc = json.loads((OUT / 'erc.json').read_text())
    issues = [issue for sheet in erc['sheets'] for issue in sheet['violations']]
    assert not any(issue['severity'] == 'error' for issue in issues)
    warnings = sum(issue['severity'] == 'warning' for issue in issues)

    def basket(variant, quantity=10):
        return next(row for row in costs['summary']
                    if row['variant'] == variant and row['fleet'] == quantity)

    full, buck, train = [basket(var) for var in ['BOOST2S', 'BUCK4S', 'TRAIN_ONLY']]
    prices = table(['Population', '6 units: EUR/board', '10 units', '20 units', 'Physical parts / ICs'],
                   [[var] + [f'{basket(var, q)["component_net_EUR"]:.2f}' for q in [6, 10, 20]] +
                    [f'{basket(var)["physical_components"]} / {basket(var)["IC_count"]}']
                    for var in ['BOOST2S', 'BUCK4S', 'TRAIN_ONLY']])
    prefix = '''Dated **2026-10-16**. **M5A-R4 electrical candidate — NOT RELEASED.**
All physical tests are **NOT_RUN**. No purchasing, fabrication, assembly or RF operation has occurred.
RF80, M4A and accepted ADRs are unchanged. R3 is preserved at tag `m5a-r3`
(`daf994c`); R0/R1 tags and the R1 native archive remain available.

'''
    docs = {}
    docs['MODERNIZATION'] = f'''# M5A-R4 — practical modernization

{prefix}The implemented candidate is **Si5351 → gated fundamental filter → PHA-1+ → ST-derived interstage → PD54008L-E → ST output matching → ST elliptic LPF**. It retains the independent training branch and common controller. The changed driver/interstage boundary remains an electrical hold before layout. No RF performance has been measured on this derivative.

| Historical/R3 block | Implemented R4 disposition | Consequence |
| --- | --- | --- |
| Crystal oscillator, first doubler and local timer | Omitted | ESP32/RTC and Si5351 already perform these functions |
| BF981 last doubler, 2N4427 and MRF237 | Removed | Direct 144 MHz replaces the 72 MHz multiplier chain; one economical MMIC drives the active ST final |
| Five Neosid modules and two RF trimmers | Removed | Their original multiplier/bipolar matching functions disappear; no arbitrary power-inductor substitution |
| Historical collector modulation | Supply-modulation principle retained | R1 D45H11/BD139 voltage servo controls drain supply; gate bias and RF drive stay fixed |
| R1 assumed output network/nine-pole LPF | Replaced | Actual ST Figures 17/14 provide output matching and elliptic filtering |
| Discrete driver supply switch | TPS22919 on regulated 5 V | Removes Q304, Q308, R408–R412 and D308; adds U305, C940 and R940 |
| Cascaded permissions | Repacked into HC21/HC11 | One fewer permission IC; captured path/profile and deliberate rearm retained |
| Boost reduced setting at 7.5 V | Fixed 9.021 V for 2S | A boost cannot regulate below a charged 8.4 V pack; Q307/R414 removed |
| Driver reservoir charged every slot | Precharged before ARM | Pass, bias, driver and clock controls stop RF; analog faults still disconnect the upstream rail |
| Expensive low-drive RF inductor allowances | Murata RF wirewound family | Exact 56 nH price observed; other values remain estimates |

The ESP32 owns scheduling, frequency/legal-profile validation, PWM references and ordinary power sequencing. No RF-side MCU, local RTC, EEPROM, scheduler or precision RF detector is added.

| Supporting function | Classification/disposition | Distinct purpose |
| --- | --- | --- |
| Si5351, reference and source filter | Essential RF performance: retain | Programmable VHF carrier, stability and harmonic control |
| Source power/I²C isolation | Essential protection: retain | Avoid source backpower and uncontrolled RF during reset/configuration |
| Watchdog and POR | Essential protection: retain | Stop RF after controller loss/brownout independently |
| ARM/path latch and final permissions | Essential protection: simplify gates | Prevent held-ARM recovery and live normal/training transfer |
| Pack window, current, PA/driver OV, thermistor window | Essential protection: retain | Battery BMS protection does not replace RF-stage protection |
| PWM filters, selector and voltage feedback | Essential AM performance candidate: retain | Filter the S3 reference and control drain waveform under load |
| Independent training buffer/BJT/filter/pad | Essential separate output: retain | Training works with watt PA and converter absent |
| Permanent RF metrology/laboratory connectors | Omitted | Shared instruments perform acceptance |

The full assembly has **{full['physical_components']} physical parts / {full['IC_count']} ICs**, versus 247 / 22 in R3. Training has **{train['physical_components']} / {train['IC_count']}**, versus 102 / 14. There is no claimed total-part-count saving: a MOSFET bias network, actual MMIC supply and true-AM servo need support parts. Cost falls mainly by eliminating obsolete RF prices. Permission gate packing removes one IC relative to the unreduced modern implementation. Five HC gate/register packages plus POR/watchdog implement permissions, not another contest scheduler.

## Controller interface

The existing 20-pin logical interface remains. Signals are 3.3 V. Current figures below are design budgets requiring qualification.

'''
    contract = [
        ['1', '3.3 V', 'Controller → RF', '3.135–3.465 V; budget ≤150 mA, not measured'],
        ['2', 'GND', 'Return', 'Logic return; separate PA current return'],
        ['3', 'SDA', 'Bidirectional', 'Dedicated/module-selected I²C at 0x60'],
        ['4', 'SCL', 'Controller → RF', 'Any low clears ARM; idle high alone grants no permission'],
        ['5', 'ARM', 'Controller → RF', 'Fresh edge captures valid context/path/profile; default low'],
        ['6', 'SLOT', 'Controller → RF', 'Scheduled carrier window; default low'],
        ['7', 'KEY', 'Controller → RF', 'Within SLOT: 0 carrier reference, 1 sine reference; low while arming'],
        ['8', 'PROGRESS', 'Controller → RF', 'Application progress edges ≤100 ms; never a free-running PWM'],
        ['9', 'MUTE_N', 'Controller → RF', 'Low inhibits; 100 kΩ default pulldown'],
        ['10', 'PA_RAIL_ADC', 'RF → controller', 'Scaled upstream rail; verify acquisition and calibration'],
        ['11', 'PATH_TRAIN', 'Controller → RF', 'Captured: 0 normal, 1 training; no live transfer'],
        ['12', 'PROFILE_FULL', 'Controller → RF', 'Captured; host applies corresponding DC/AF calibration'],
        ['13', 'AF_PWM', 'Controller → RF', 'Offset plus sine; initial PWM carrier 312.5 kHz'],
        ['14', 'LEVEL_PWM', 'Controller → RF', 'Carrier reference; same DC offset as AF_PWM'],
        ['15', 'PREPARE', 'Controller → RF', 'Source/configuration permission; default low'],
        ['16', 'FAULT_N', 'RF → controller', 'Actually VALID_ARM through 1 kΩ: low also means unarmed'],
        ['17/18', 'GND', 'Return', 'Additional logic returns'],
        ['19', 'MODULE_ID', 'Passive', 'R4: 18.2 kΩ 2S / 39.2 kΩ 4S / 82 kΩ training; controller pullup/ADC'],
        ['20', 'PA_PREPARE', 'Controller → RF', 'Precharge normal rail; keep low for training']]
    docs['MODERNIZATION'] += table(['Pin', 'Signal', 'Direction', 'Contract'], contract) + '''
Protected power enters J301 with its own return. Establish 3.3 V before raw PA power and remove raw power first until sequencing/backpower behavior is qualified. Do not drive arbitrary GPIOs into an unpowered module. Si5351 uses a switched, isolated bus. Both CLK0 and CLK2 now produce the actual RF frequency: PLL = 6 × RF, multisynth divide-by-6, CLK1 disabled. R3's half-frequency configuration and IDs are incompatible.

For configuration, hold ARM/SLOT low, release MUTE_N high and assert PREPARE. **MUTE_N low turns the source off**, so it cannot remain low during programming. I²C activity clears the context. Configure/read back frequency and establish genuine progress pulses. PA_PREPARE may precharge the normal rail while RF clamps remain asserted. Raise ARM only with KEY/SLOT low and settled references. Captured 4S profile can change the buck setpoint: wait for ADC-confirmed settling before SLOT. To retune/change path/profile, withdraw SLOT, assert MUTE_N low and lower ARM; then power the source with ARM/SLOT still low, configure and deliberately rearm. A held ARM must not recover after a fault.

Training omits the entire PA/MMIC, converter/LDO, normal matching/filter/connector and PA monitoring/heat hardware. R519 links RUN_HEALTH to 3.3 V only when normal U207 is omitted. Training-only R517 is a 0 Ω link from MOD_DRIVE to VPA_FB, closing unity feedback around unused U401C; R518 grounds its positive input. R932 defines the unused normal RC input. Never fit these links across the full assembly's feedback. Watchdog, POR, fresh ARM, path selection, KEY/SLOT and independent training RF remain active.

[Native schematic](../hardware/2m/RF2M.kicad_sch), [PDF](../hardware/2m/review/M5A-R4/RF2M.pdf), [component delta](../hardware/2m/review/M5A-R4/component-delta.json). R3 retains the historical DL3BBX permission restrictions. R4 independently transcribes attributed manufacturer circuit facts; complete third-party articles, artwork and Gerbers are not redistributed or relicensed. No accepted ADR is changed.
'''

    docs['RF_STAGE'] = f'''# M5A-R4 — RF stage and reference evidence

{prefix}Select **ST PD54008L-E**, with **PHA-1+ as the conditional economical driver**. ST lists the final as active/volume production in PowerFLAT 5×5. Mouser's dated cut-tape listing has MOQ 1, €7.35 at one/€5.30 at ten and indexed stock 3,430. This does not reserve inventory. [ST product](https://www.st.com/en/radio-frequency-transistors/pd54008l-e.html), [Mouser](https://www.mouser.de/de/ProductDetail/STMicroelectronics/PD54008L-E).

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
'''

    comparison = table(['Population/fleet', 'R3 EUR', 'R4 EUR', 'Saving', 'Parts R3 → R4', 'ICs R3 → R4'],
                       [[f'{r["variant"]}/{r["fleet"]}', f'{r["R3_EUR"]:.2f}', f'{r["R4_EUR"]:.2f}',
                         f'{r["saving_vs_R3_EUR"]:.2f}', f'{r["R3_parts"]} → {r["R4_parts"]}',
                         f'{r["R3_IC"]} → {r["R4_IC"]}'] for r in costs['comparison']])
    blocks = table(['Block at ten', '2S EUR', '4S EUR'],
                   [[k, f'{full["blocks"].get(k, 0):.2f}', f'{buck["blocks"].get(k, 0):.2f}']
                    for k in sorted(full['blocks'])])
    evidence = table(['Population', 'Current indexed EUR', 'Historical observed EUR', 'Estimated EUR', 'OPEN MPN/landing amount EUR'],
                     [[r['variant'], f'{r["price_evidence"].get("CURRENT_INDEXED_OBSERVATION", 0):.2f}',
                       f'{r["price_evidence"].get("HISTORICAL_INDEXED_OBSERVATION", 0):.2f}',
                       f'{r["price_evidence"].get("ESTIMATE", 0):.2f}',
                       f'{r["amount_with_OPEN_MPN_or_footprint_EUR"]:.2f}'] for r in [full, buck, train]])
    docs['COST_RECONCILIATION'] = f'''# M5A-R4 — cost reconciliation

{prefix}The complete candidate basket is **€{full['component_net_EUR']:.2f} for 2S / €{buck['component_net_EUR']:.2f} for 4S at ten**. It meets the €40–50 target as an estimate, not as a fully quoted or electrically qualified buildable price. All amounts are net EUR; VAT, PCB, controller, battery, antenna, enclosure and labor are separate.

{prices}
The RF core—source, driver/final, bias, matching, LPF, AM and indispensable driver rail—is **€{full['RF_core_net_EUR']:.2f} at ten**. It excludes training, controller interface, pack conversion and remaining protection. [Itemized 6/10/20 BOM](../hardware/2m/review/M5A-R4/RF2M_BOM.csv), [population list](../hardware/2m/review/M5A-R4/positions.csv), [ledger](../hardware/2m/review/M5A-R4/costs.json) and [all changed/added/deleted R3 parts](../hardware/2m/review/M5A-R4/component-delta.json) are generated from the implemented manifest.

{comparison}
{blocks}
The entire **€57.60 obsolete bundle** is removed: MRF237 €31.90, 2N4427 €5.90, BF981 €3.00, Neosid modules €15.00 and RF trimmers €1.80. The replacement includes €5.30 final, €2.88 MMIC, actual ST networks, fixed bias and AM servo. It is not a drop-in final in the old match. Lower-cost low-drive RF inductors also replace expensive generic allowances. No filter, training capability or independent fail-off is silently omitted.

## Price evidence and gaps

{evidence}
The last column overlaps the first three; do not add it again. An exact proposed MPN does not convert an allowance into a quote. Each BOM row records supplier identifier, quantity, MOQ/multiple, URL, evidence class and unresolved status. Estimated MOQ 1 is not supplier confirmation. Identical MPNs are pooled within each fleet/variant and priced consistently using the highest applicable allowance. No unearned reel discount is booked.

The final's €5.30 cut-tape price is observed. PHA-1+ is €2.88, with no 50-piece break booked for twenty boards. A05T rises from the old €0.55 estimate to €1.28; the low-ESR reservoir is now **€1.50 estimated**, replacing a €0.45 generic allowance. Current converter observations replace carried prices: TPS54302DDCR €0.879 and TPS611781RNWR €2.031 at ten. Most supporting costs remain estimated; see the dated [source log](../hardware/2m/review/M5A-R4/sources.json).

Full purchased count rises from R3's 247/22 ICs to {full['physical_components']}/{full['IC_count']}; training changes from 102/14 to {train['physical_components']}/{train['IC_count']}. Savings are monetary, not a false count reduction. Permission packing removes one IC relative to the unreduced modern implementation. Test pads, PWR_FLAG and transmission-line copper are not purchased components.

## Other installed materials

These are estimates pending the actual outline, stack-up and quote:

| Additional material, EUR/unit | 6 | 10 | 20 |
| --- | --- | --- | --- |
| Two-layer bare PCB | 6.00 | 4.50 | 3.50 |
| RF pigtails/mating harness beyond board connectors | 3.00 | 3.00 | 3.00 |
| Antenna/feed system | 12.00 | 12.00 | 12.00 |
| Sink, insulators and fixings | 7.00 | 7.00 | 7.00 |

At ten the installed RF module allowance is **€{buck['component_net_EUR']+26.5:.2f} for 4S / €{full['component_net_EUR']+26.5:.2f} for 2S**, before controller, pack, charging, enclosure and labor. Board connectors are already in components. PCB allowance is not a promotional quote. One-time engineering/tooling and shared fleet costs remain separate. Assembly, winding, alignment and test labor are unpriced until the first complete build is timed; no fictitious labor saving is assigned.

The retained [M2 battery ledger](M2_BATTERY_COST_COMPARISON.md), dated 2026-10-14, supplies system context. These are its historical observed/estimated mix, including stated protection/keying/qualification allowances, not new quotes:

| Pack/cell basis, EUR | 6 | 10 | 20 |
| --- | --- | --- | --- |
| 2S2P, 2450 mAh class | 15.38 | 15.38 | 15.02 |
| 2S3P, 2450 mAh class | 20.68 | 20.14 | 19.66 |
| 2S4P, 2450 mAh class | 25.98 | 25.26 | 24.62 |
| 4S1P, 2450 mAh class | 18.64 | 18.64 | 18.28 |
| 4S2P, 2450 mAh class | 29.24 | 28.52 | 27.88 |
| 2S2P, M35A | 21.66 | 21.10 | 21.10 |
| 2S3P, M35A | 29.26 | 29.26 | 28.30 |
| 2S4P, M35A | 37.42 | 37.42 | 36.14 |
| 4S1P, M35A | 24.92 | 24.36 | 24.36 |
| 4S2P, M35A | 40.68 | 40.68 | 39.40 |

That ledger separately allocates shared charging/provisioning/freight: 2S €13.50/8.10/4.85 and 4S €14.33/8.60/5.35 per unit at 6/10/20. The older common-controller component allowance is €16.70/14.93/14.83, with its own PCB/enclosure separate. Do not add an entire prior transmitter basket again when using these pack rows. RF80 and reconciled Foxoring accounting are unchanged.
'''

    states = read_csv('operating-states.csv')
    end = read_csv('endurance.csv')
    pack_rows = []
    for pack in ['2S2P', '2S3P', '2S4P', '4S1P', '4S2P']:
        for cell in ['2450mAh_min', 'M35A_min_energy']:
            rows = [r for r in end if r['pack'] == pack and r['cell_class'] == cell and r['LoRa'] == 'absent']
            high = next(r for r in rows if r['profile'] == 'full')
            low = next(r for r in rows if r['profile'] == 'reduced')
            pack_rows.append([pack, cell, f'{float(high["hours_MODELED"]):.1f}',
                              f'{float(low["hours_MODELED"]):.1f}', f'{float(high["continuous_beacon_h"]):.1f}',
                              'Yes' if high['margin20percent'] == low['margin20percent'] == 'True' else 'No'])
    state_table = table(['Profile', 'Variant', 'Active upstream W', 'Mean battery W', '12 h Wh', '24 h Wh'],
                        [[r['profile'], r['variant'], f'{float(r["active_upstream_W_CALCULATED"]):.2f}',
                          f'{float(r["mean_battery_W"]):.2f}', f'{float(r["need12_Wh"]):.2f}',
                          f'{float(r["need24_Wh"]):.2f}'] for r in states])
    docs['AM_POWER'] = f'''# M5A-R4 — true AM, power and endurance

{prefix}The retained historical principle is **constant RF drive and gate bias, with final drain-supply modulation**. R1's quad-opamp reconstruction/feedback and D45H11/BD139 are reused. There is no RF-envelope detector. A clean drain-voltage waveform alone does not prove clean RF AM.

## Modulation circuit and power

The ESP32-S3 supplies 312.5 kHz PWM; no internal DAC is assumed. Two unity Sallen-Key sections use 10 kΩ/10 kΩ and 4.7 nF/4.7 nF, approximately 3.39 kHz corner and Q 0.5. LEVEL_PWM supplies carrier DC; AF_PWM supplies the same offset plus a configurable sine, initially 800 Hz. The tone is not an IARU mandate. U402 selects DC for KEY = 0 and sine for KEY = 1 within SLOT. The carrier persists only inside SLOT; keyed AF implements A2A. The controller ramps transitions and applies calibration; no production firmware is implemented.

U401C controls BD139 and the D45H11 pass device so VPA ≈2.8 × MOD_COMMAND. R507/Q403 limit helper current to approximately 73 mA, not a precision PA trip. R505 returns pass base to emitter. Q404/Q405 clamp helper drive and command; Q502 grounds final bias; U305 disconnects the 5 V driver; U601 mutes its clock. The upstream rail stays precharged to avoid inrush every slot. Analog faults open upstream isolation and clear ARM. A pass short must still be contained by bias/driver/clock shutdown; off-slot feedthrough and oscillation remain physical gates.

The initial full **voltage** envelope is 7.2 V crest, 4 V center and 0.8 V trough at 80% depth. MOD_COMMAND is 1.429 ±1.143 V, range 0.286–2.571 V. Reduced candidate is 4 V crest, 2.222 V center and 0.444 V trough. These are starting calculations, not calibrated RF settings. Knee voltage, impedance, gain and AM-to-PM vary during the envelope. Require actual 70–80% RF depth and initially ≤5% envelope THD. Clipped/non-monotonic behavior is a NO_GO. Modest reference correction may follow measured transfer; no elaborate new servo is assumed.

[IARU Region 1 2025 Part B](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf), Appendix 1 T2.8, specifies 144.500–144.900 MHz, stability better than 50 ppm, simultaneous spacing **more than** 200 kHz, 0.25–1 W carrier ERP, A2A at 70–80%, 8–15 WPM, horizontal polarization and 2–3 m antenna height. T2.4 prohibits unscheduled RF. National operating permission, frequencies and emissions are separate obligations; rules are not legal transmitter authorization.

`PEP = Pc × (1+m)²`; mean AM RF is `Pc × (1+m²/2)`. At −1 dBd net antenna/feed gain, 1 W ERP needs 1.259 W conducted carrier and 4.079 W connector PEP at 80%. At 0 dBd: 1 W and 3.24 W. With 0.75 dB combined output loss the final needs 4.848/3.851 W crest. Extra 1 dB capability reserve is optional, not another championship limit. Neither antenna scenario is measured. Proposed full calibration is 0.90 W ERP with ≤0.4 dB total uncertainty, upper bound 0.987 W; reduced 0.30 W gives lower bound 0.274 W. A missing near-upper capability must be reported, not hidden by lowering the setting.

## Supply, protection and heat

Protected 2S at 6.0–8.4 V uses TPS611781 boost at **{calc['boost_nominal_V']:.3f} V** for both profiles. Protected 4S at 12.0–16.8 V uses TPS54302 buck at **{calc['buck_full_nominal_V']:.3f} V full / {calc['buck_reduced_nominal_V']:.3f} V reduced**. These are exclusive populations with different pack IDs/windows. A 7.5 V boost setting is invalid at charged 2S voltage. The 4S buck avoids the former 13.5 V rail's lost discharge window; raw 4S never reaches the 9 V circuit. Reduced 4S voltage saves pass heat without universal buck-boost.

R413 is 8.2 Ω/1 W. Initial reservoir charging is bounded to approximately 1.14 A at 9.2 V, below the nominal 1.8 A trip before tolerance/dynamics. Precharge with command/bias/clock clamped, verify the rail, then ARM. At 180 mA the resistor dissipates 0.266 W; full LDO input is approximately 7.54 V before upstream drops. Reduced-rail dropout/ripple at high temperature must be checked. The selected reservoir candidate is Panasonic **25SVPG150M**, 150 µF/25 V ±20%, 13 mΩ at 100 kHz, 6.3 mm diameter/9.9 mm height. Its manufacturer specification closes the generic identity gap, but effective capacitance ≥120 µF and ESR 2–100 mΩ across the qualified temperature/life window remain assumptions. Exact C10 landing, available stock and EUR quote remain OPEN; the €1.50 allowance is an estimate.

Driver OV uses 0.1% dividers. Nominal trip is **{calc['driver_OV_nominal_V']:.3f} V**; an assumed ±1.5% reference bound gives **{calc['driver_OV_min_V_under_assumed_1p5percent_reference']:.3f}–{calc['driver_OV_max_V_under_same']:.3f} V**. With 8.118 Ω, 120 µF, 0.1 Ω ESR and a 16.8 V fault, the conditional upper calculation is **{calc['driver_20us_RC_plus_ESR_upper_calculation_V']:.3f} V** if isolation completes within 20 µs after threshold crossing. Require measured rail ≤5.9 V. Arithmetic does not qualify surge immunity or actual latency. An 18 V TVS is not a precision clamp below every part rating. Input hot-plug/FET transients remain OPEN; initial commissioning uses a bounded laboratory supply.

ST D45H11 and BD139 are base pin 1, collector/tab pin 2, emitter pin 3. The pass tab is live VPA and needs insulation from grounded RF thermal hardware. D45H11 RθJC is 2.5 K/W. The consistent loss/efficiency assumptions give full/reduced carrier drain currents approximately 0.748/0.505 A. Full 80% crest is approximately 1.347 A plus driver current; the nominal 1.8 A trip has no qualified transient margin. Full pass mean AM loss is approximately 2.80 W, or 3.76 W without tone. Reduced 2S pass loss is approximately 3.07 W, or 3.43 W without tone. Lower RF power does not automatically lower pass heat.

Keep the approximately 66°C sensor trip. Engineering targets are case ≤60°C and estimated junction ≤125°C, with sensor coupling qualified over 60 s on/240 s off. A dedicated 2 K/W sink and ≤1 K/W insulated interface at 40°C give approximately 51°C case/61°C junction in the full no-tone example. A shared sink must include PA/driver heat; a generic shared 5 K/W sink is not automatically adequate. Continuous beacons need separate cooling. Sensor open/short trips; an intact but detached sensor requires mounting inspection and lag qualification. Hot DC/repetitive SOA and helper heat remain OPEN; headline 50 W/10 A ratings are not linear-SOA proof.

## Modeled endurance

Carrier final power is `ERP × 10^0.175`; carrier current is `Pfinal/(Vcenter × PA efficiency)`; mean upstream is `Vup × (Icarrier + 0.146 A driver) + 0.10 W`. This includes linear-pass loss. Full/reduced PA efficiency is assumed 50%/40%, boost/buck 87%/91%. The 0.10 W active allowance covers helper/reference/source increment. Controller 0.14 W and RF idle 0.04 W are continuous. Duty is 20%, without Morse discount. Actual bias and waveform behavior may worsen these values.

{state_table}
Usable energy is cell count ×8.82 Wh for the 2450 mAh minimum class or ×11.90 Wh for M35A minimum-energy basis, multiplied by 0.8 aging ×0.9 temperature ×0.9 endpoint margin. The 3.0 V/cell endpoint and margins are inherited assumptions, not measured discharge integration. Equal cell counts give equal nominal energy for 2S2P/4S1P and 2S4P/4S2P.

{table(['Pack', 'Cell basis', 'Full modeled h', 'Reduced modeled h', 'Full beacon h', '20% margin on both targets'], pack_rows)}
Use the 20% margin column rather than a marginal arithmetic pass. Under these assumptions, high-capacity 2S2P/4S1P meets 12 h full; robust 24 h reduced needs high-capacity 2S3P, 2450-class 2S4P or 4S2P. A high-capacity 4S1P is marginal for the reduced target, not qualified. Continuous full beacons do not inherit competition endurance.

LoRa absent is baseline; add 6 mW intermittent or about 45.6 mW continuous receive plus bursts. Controller/RF idle alone use 4.32 Wh/day; continuous LoRa adds about 1.09 Wh/day. [Pack table](../hardware/2m/review/M5A-R4/endurance.csv), [states](../hardware/2m/review/M5A-R4/operating-states.csv), [coarse sensitivity](../hardware/2m/review/M5A-R4/sensitivity.csv), [reduced-efficiency sensitivity](../hardware/2m/review/M5A-R4/reduced-efficiency-sensitivity.csv), [thermal calculations](../hardware/2m/review/M5A-R4/thermal.csv). Poorer PA efficiency, 500 mW controller idle or cold-cell sag can invalidate the minimum. No endurance PASS is claimed.
'''

    docs['BUILD_AND_TEST'] = f'''# M5A-R4 — one complete-device build and acceptance

{prefix}The next physical implementation is **one integrated transmitter**, not separate coupons. Close the input-network and package holds, review the complete PCB, then obtain manufacturing authorization. This future procedure does not authorize construction or RF operation.

Shared equipment: bounded current-limited DC supply; 50 Ω dummy load rated ≥10 W; calibrated CW/PEP meter or RF envelope detector/scope; spectrum analyzer and suitable attenuation; VNA for limited input/filter alignment; current and temperature logging. An RF generator may inject an existing integrated driver test node. Protect instruments from watt-level RF and drain-node DC. Record exact MPNs, serial, variant, calibration, ambient, pack, antenna/feed and uncertainty.

1. **Inspect unpowered.** Confirm gate-left/drain-right/center-source orientation, source soldering, ST pass/helper pinouts and live tabs. Verify exclusive converter population, pack ID/UV settings, DNPs and independent connectors. Check no normal-to-training conductive RF connection. Inspect sink insulation and thermistor attachment. Never install a generic unverified final footprint.
2. **Commission 3.3 V.** Disconnect the PA pack. Start at 3.30 V with 100 mA limit and raise only after demand is explained; the ≤150 mA header budget is not measured. Configure clocks into bounded loads. Check fresh ARM with KEY/SLOT low, heartbeat expiry, reset, I²C activity/stuck levels, held-ARM recovery, invalid requests and captured selections. Fault/reset must remove both permits. Scope clear, clock/OE and driver timing; Boolean tests do not prove it.
3. **Check supply and AM using temporary loads on the same board.** Ground bias trim and inhibit RF. Start 2S at 6 V or 4S at 12 V with 100 mA limit and no final conduction. Verify 9.02 V boost or 9.00/7.51 V buck, initially ±3%. Increase to 0.5 A only for explained bounded loads. Precharge the reservoir before ARM; measure inrush, 5 V stability and reduced-rail dropout. Calibrate current/OV trips. Observe pass center/crest/trough and ringing into a temporary resistive load. No unrestricted pack.
4. **Align normal RF at low energy.** Connect dummy load and protected meters. Enable the driver only after rail qualification; start low source drive. Establish gate Idq from 50 mA; exceeding 200 mA requires thermal justification. Begin with low drain command and ≤0.5 A PSU limit. Increase only as demand is explained; never bypass the nominal 1.8 A trip. Adjust documented input-network positions in one integrated alignment. If gain/backoff cannot be met with a small documented change, stop instead of silently adding a premium chain.
5. **Calibrate carrier/AM.** Measure carrier, PEP and envelope at 144.5/144.7/144.9 MHz and battery endpoints. Establish final gain and ≥3 dB driver backoff. Nominal depth 75%, acceptance 70–80%; initial engineering limits are THD ≤5%, sideband asymmetry ≤1 dB and no clipping. PEP must agree with carrier ×(1+m)² within uncertainty. Measured antenna/feed gain must yield ERP upper bound ≤1 W, reduced lower bound ≥0.25 W. Do not label full power until near-upper performance is demonstrated. Frequency error must stay better than 50 ppm over the temperature/aging budget.
6. **Run one spectrum, shutdown, training and thermal acceptance.** Apply the national emission mask; initially screen harmonics at ≤−60 dBc as an engineering target, not an IARU legal limit. Inspect fractional/PWM products. Exercise SLOT, MUTE, reset, heartbeat loss, I²C and bounded analog faults. Held ARM must not recover. Record off-slot output floor and RBW; initial internal goals normal ≤−70 dBm/training ≤−90 dBm are not literal zero-RF proof. Calibrate training to nominal 1 µW carrier (−30 dBm), declared tolerance and 70–80% AM with the PA/converter off. Measure maximum normal-to-training leakage and bounded-fault isolation. Require no damaging power or uncommanded output. Run 60 s on/240 s off at worst ambient: case ≤60°C, estimated junction ≤125°C, no ordinary thermal trip. Continuous beacons have separate limits.
7. **Qualify bounded faults/endurance.** Initially disconnect the RF driver when injecting representative converter/LDO faults at existing nodes. Require isolation ≤20 µs from worst threshold crossing, driver ≤5.9 V and no reverse/backpower. Qualify input hot-plug before unrestricted 4S use; never short a pack to test the fuse. Measure current and sensor open/short response, RF/drain withdrawal and real 12 h full/24 h reduced profiles under stated cell, aging, temperature and LoRa conditions. Replace assumed currents/efficiencies before selecting fleet packs.

Every hardware test is **NOT_RUN**. A failed envelope, drive, thermal or off-state test blocks replication. The first complete unit may require a recorded correction; original ST fixed-supply results do not validate this derivative. After acceptance, freeze actual alignment values, traces, tolerances and test minutes for repeatable fleet assembly.
'''

    docs['REVIEW_DECISION'] = f'''# M5A-R4 — review decision

{prefix}**GO for independent electrical review. NO_GO for PCB commitment or manufacturing release.** The editable lower-cost schematic and reconciled material model exist. A fully sourced, buildable integrated PCB is not complete: the changed interstage and listed landings remain unresolved. No PCB, DRC result or Gerbers are invented.

The preferred candidate is direct 144 MHz Si5351, PHA-1+, active PD54008L-E, actual ST output matching/elliptic LPF, fixed gate bias and D45H11 drain sine modulation. **4S buck is the normal-power preference**; 2S boost is an alternate population. Independent µW training uses regulated 3.3 V with normal PA/converter omitted. MRF237, BF981, 2N4427, Neosid modules and RF trimmers are removed.

{prices}
At ten, 2S saves **€{93.15756811076373-full['component_net_EUR']:.2f} versus R3** and **€{52.633704332291344-full['component_net_EUR']:.2f} versus R1**. The 4S savings are €{91.22756811076374-buck['component_net_EUR']:.2f} and €{50.703704332291345-buck['component_net_EUR']:.2f}. RF core is €{full['RF_core_net_EUR']:.2f}; installed 4S module allowance is €{buck['component_net_EUR']+26.5:.2f} before controller, battery, enclosure and labor. Most supporting prices remain estimates; [cost reconciliation](M5A_R4_COST_RECONCILIATION.md) quantifies the unquoted amount. These are not achieved purchase prices.

The original ST circuit/layout and final package drawings were recovered and inspected. Twenty-six network positions are checked in exported CAD. Their fixed-supply evidence does not prove our sine AM. At −1 dBd/1 W ERP/80%, the final needs 4.848 W PEP with the stated output loss and ≥18.86 dB gain for 19 dBm drive/1 dB input loss; at 0 dBd it needs ≥17.86 dB. These are unqualified targets. Optional extra 1 dB margin is not a championship rule.

Implemented changes remove obsolete RF stages, restore the actual elliptic filter, reduce low-drive inductor cost, replace a discrete driver switch, remove one permission IC, fix boost downregulation, precharge the driver reservoir and improve the conditional driver-OV bound. Slot shutdown uses pass/helper, gate bias, driver and clock controls while the upstream rail is precharged. That sequencing needs off-slot/pass-short testing. Full count is {full['physical_components']}/{full['IC_count']} ICs versus R3's 247/22; no false count saving is claimed.

## Checks and open gates

- **KiCad 10.0.6 ERC: zero errors, {warnings} visible footprint warnings.** Pin-to-pin/sheet-name errors were corrected, not waived. Default informational exclusions are recorded.
- Export/manifest parity covers **{verified['manifest_positions']} positions**. **{verified['logic']['combinations']} static combinations, {len(verified['logic']['scenarios'])} states, {len(verified['mutation_tests'])} deliberate mutations, 35 pin maps and 26 ST assertions pass.** These do not prove analog startup or timing.
- [Native schematic](../hardware/2m/RF2M.kicad_sch), [PDF](../hardware/2m/review/M5A-R4/RF2M.pdf), [netlist](../hardware/2m/review/M5A-R4/RF2M.net.xml), [BOM](../hardware/2m/review/M5A-R4/RF2M_BOM.csv), [pin audit](../hardware/2m/review/M5A-R4/pinout-audit.json), [reproducible checks](../hardware/2m/review/M5A-R4/final-checks.json).
- **Electrical hold:** the 50 Ω PHA-1+ cannot simply inherit the original PD84001 drain interstage. Establish the integrated input match and final gain/drive margin before routing. A small integrated alignment is acceptable; a fundamentally different PA is not silently substituted.
- **Physical holds:** the selected reservoir's C10 landing and temperature/stock confirmation, RF feed/air-coil landings and keyed connectors remain OPEN. Manufacturer-derived DF782 and RNW candidate landings now have dimensional checks; their stencil/thermal/assembly integration still needs review. Define final-source stencil/vias and actual stack-up. No unverified generic final pads.
- **Physical qualification:** drain-AM knee/linearity/stability, pass/helper hot SOA, sensor mounting, ≤20 µs isolation/≤5.9 V driver, input transients, RF/ERP/spectrum, off-slot silence, training isolation and 12 h/24 h endurance. All remain NOT_RUN. The consistent power model does not certify a small pack.

Close these specific input-network and physical landing definitions, then make **one integrated transmitter PCB**, review it and commission one complete unit using [one acceptance procedure](M5A_R4_BUILD_AND_TEST.md). No separate coupon program or broad architecture study is proposed. R1/R3 remain archived engineering fallbacks. Procurement/fabrication require explicit authorization; stop for review.
'''
    for name, content in docs.items():
        (ROOT / 'docs' / f'M5A_R4_{name}.md').write_text(content)
    print(f'Generated {len(docs)} R4 documents from verified CAD and ledgers')


if __name__ == '__main__':
    main()
