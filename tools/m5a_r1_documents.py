#!/usr/bin/python3
"""Render R1 review tables from the actual CAD manifest/calculations/cost ledgers."""
import json,csv,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'hardware/2m/review/M5A-R1';D=R/'docs'
def read(n):return json.loads((O/n).read_text())
def table(head,rows):return '| '+' | '.join(head)+' |\n| '+' | '.join(['---']*len(head))+' |\n'+'\n'.join('| '+' | '.join(map(str,row))+' |'for row in rows)+'\n'
def write(n,s): (D/n).write_text(s.strip()+'\n')
c=read('costs.json');a=read('calculations.json');v=read('verification.json');b=read('comparison-baskets.json')
old=json.loads((R/'hardware/2m/archive/M5A-R0/RF2M.electrical.json').read_text());new=json.loads((R/'hardware/2m/RF2M.electrical.json').read_text());op={p['ref']:p for p in old['parts']};np={p['ref']:p for p in new['parts']}
base='Date: **2026-10-15**. **M5A-R1 electrical evaluation candidate — NOT RELEASED. All physical tests NOT_RUN.**'
rel='../hardware/2m/review/M5A-R1/'
write('M5A_R1_ST_REFERENCE_AUDIT.md',f'''# M5A-R1 — ST reference audit

{base}

**Reference reconstruction is incomplete.** Original document text and tables were retrieved, but the raster circuit/package drawings could not be inspected. Direct binary downloads failed with HTTP/2 errors,403 responses or timeouts, including approved network retries. Browser screenshot calls supplied image markers without usable image pixels. The original Gerber ZIP was located but not downloaded. No connection trace, pad numbering or Gerber inspection is claimed from those unavailable images. This blocks acceptance criteria1 and4–5 and the coupon layout.

## Dated primary-source log

| Source | Version/evidence available on2026-10-15 | Disposition |
| --- | --- | --- |
| [ST board page](https://www.st.com/en/evaluation-tools/steval-tdr003v1.html) | NRND; original PD84001/PD54008L-E board | Historical RF evidence; not production procurement |
| [Full board document](https://www.st.com.cn/resource/en/datasheet/steval-tdr003v1.pdf) | DocID17343 Rev1,31-Mar-2010; text/tables retrieved | Figures12–17 require visual tracing; layout figures10–11 unavailable as pixels |
| [Original schematic](https://www.st.com/resource/en/schematic_pack/steval-tdr003v1_schematic.pdf) | Raster circuit not recoverable in this environment | OPEN, do not infer nets from BOM |
| [Original BOM](https://www.st.com/resource/en/bill_of_materials/steval-tdr003v1_bom.pdf) | Two-page spreadsheet export, no visible revision/date | Values and discrepancies below; topology not established |
| [Original Gerber ZIP](https://www.st.com/resource/en/board_manufacturing_specification/steval-tdr003v1_gerber.zip) | Manufacturer link found; binary inaccessible | NOT_INSPECTED; no guessed aperture/line endpoints |
| [Final datasheet](https://www.st.com/resource/en/datasheet/pd54008l-e.pdf) | January2007 Rev2; text retrieved, package picture unavailable | Functional G/D/S only; numeric landing OPEN |
| [Final product status](https://www.st.com/en/radio-frequency-transistors/pd54008l-e.html) | Active, volume production, PowerFLAT5×5HV | Current device candidate; not the obsolete PD84001 |

The2010 document reports5W,135–175MHz at7.2V with5–10dBm input,≤1.5A and47–52% PAE under its table conditions. These apply to the complete original two-stage assembly. Its harmonic and mismatch claims cannot transfer to changed matching, driver or AM operation. No RF AM transfer curve or isolated144MHz final gain was retrieved.

## Component evidence and contradictions

Standalone BOM positions, values only: C1/C5/C6=1µF; C16=NC; C2/C3/C4/C7/C8/C9/C10=330pF; C11=56pF,C12=27pF,C13=33pF,C14=100pF,C15=39pF. L1=24nH,L2=33nH,L3=35.5nH,L4/L5=18nH. R1/R4=62kΩ,R2=430kΩ,R3=240Ω,R5=150kΩ,R6=11Ω. Filter C1F..C7F=3.3/18/12/22/27/22/15pF; L1F/L2F/L3F=39/22/27nH. This is an inventory, not a netlist.

The standalone BOM labels the final PD54008L but gives part-code PD54003L. The2010 document title/component table and current board page identify **PD54008L-E**. Therefore choose that exact device; actual characterization-lot markings remain unknown. Never substitute PD54003L.

Other conflicts:330pF versus Murata391 code;2010 C1/C5=NC instead of1µF; L1 nominal24nH with33nH code; L3 nominal35.5nH with22nH code; L5 differs between18nH0603 and18.5nH minispring. Connector codes differ801/881. Resolve from actual drawings/layout and supplier data before copying any order list.

## Transmission-line inventory and reuse matrix

The BOM specifies0.508mm FR4/70µm copper,0.92mm nominal50Ω lines, TL1..TL9 lengths3/7.2/6.23/6.62/5.8/2.2/11/12.4/2mm. **Endpoints and stage assignment are OPEN.** Numbers alone cannot reconstruct their matching function.

'''+table(['Original block','Disposition','Exact remaining evidence'],[
['RF input/PD84001 matching','Incompatible with substituted MMIC','Read Figure15; retain50Ω boundary only after verification'],
['PD84001','Not reusable','Obsolete; no old-stock production strategy'],
['Interstage','Recalculate/measure','Figure16 endpoints and final gate impedance; MMIC output differs'],
['PD54008L-E final','Preferred evaluation candidate','Physical terminal map, thermal land and144MHz gain OPEN'],
['Drain supply/decoupling','Modify for AM','Figure12/13; fixed bias and no bulk capacitor on modulated drain'],
['APC/bias','Not copied blindly','Identify gates controlled by APC before deciding removal; no servo-modulation assertion'],
['Final matching','Potentially reusable after stack-up validation','Figure17 and Gerber endpoints OPEN'],
['Harmonic LPF','Potentially reusable','Figure14 topology OPEN; R1 retains explicitly interim R0 ladder'],
['Ground/thermal vias','Reuse principles after drawings','Package/land images and actual stack-up mandatory']])+'''

R1 deliberately contains OPEN matching positions rather than falsely claiming the original ST network. Close this narrowly: obtain readable Figures12–20 and original manufacturing archive; trace named nodes and physical G/D/S lands; replace the marked R1 matching harness/LPF with the verified reference derivative. No broader architecture study is required.

The calculation script evaluates microstrip impedance with zero-thickness formulas only. At1.6mm,0.92mm copper is far above50Ω; line width and phase must be recalculated. Proposed coupon substrate remains0.508mm FR4/70µm copper, supplier-declared dielectric/mask/tolerances. Copper-thickness and launch/via corrections require EM or VNA confirmation. Original artwork is manufacturer copyright; linked, not relicensed or reproduced as project-owned CAD.
''')
write('M5A_R1_RF_SELECTION.md',f'''# M5A-R1 — final and driver selection

{base}

Select **PD54008L-E plus PHA-1+ as a plausible, unqualified economical evaluation chain**. Keep the complete PD55008-E/PHA-13HLN+ R0 implementation at tag`m5a-r0` (commit`ea671c1`) and in [native archive](../hardware/2m/archive/M5A-R0/). Selection is conditional on measured final gain, envelope transfer and matching; it is not approval of a buildable reference clone while the [source-trace blocker](M5A_R1_ST_REFERENCE_AUDIT.md) remains.

## Drive calculation at identical functional scope

Connector carrier1.258925W,80% PEP4.078918W,1dB capability5.135054W. Retaining0.75dB output-loss allowance gives **6.103W final-plane capability**. Allow1.25dB driver-to-final input loss and3dB driver output backoff. No whole-board gain is assigned to the final alone.

'''+table(['Assumed final gain dB','Required driver output dBm','Required driver P1dB dBm'],[[x['final_gain_db'],f"{x['required_driver_dbm']:.2f}",f"{x['p1db_required_dbm']:.2f}"]for x in a['driver']])+'''

PHA-1+ published50MHz/800MHz P1dB values bracket the band but provide no guaranteed144MHz result. Its22.2dBm typical50MHz value implies a measured final-gain requirement near19.91dB at the capability plane; if actual driver P1dB is only20dBm, the gain requirement rises to22.11dB. Include uncertainty and loss measurements; neither number is a promised gain.

| Driver | Evidence and evaluation decision | q6/10/20 EUR/device |
| --- | --- | --- |
| PHA-1+ | Preferred conditional candidate;5V146mA typical,110–180mA range;17.2/15.7dB typical gain at50/800MHz. P1dB must be measured at144MHz. |2.82/2.82/2.82 observed display; tax confirmation pending |
| GVA-84+ | R0-researched20.73dBm example leaves less margin; no revised144MHz minimum verified. Gain floor≈21.38dB if that P1dB holds. Not selected. | historical/unresolved exact EU basket |
| MMBTH10LT1G discrete | Active manufacturer family, cheap transistor; complete stable linear driver/matching not demonstrated. Do not replace a supported MMIC with an invented discrete stage. | whole-stage1–1.5 estimate, not quotation |
| PHA-13HLN+ | Stronger fallback;8V234.1mA typical, R0 estimated P1dB27.3–28.4dBm bracketing frequencies. Exact144MHz compression still measured. |14.6047 historical converted allowance |

[PHA-1+ manufacturer data](https://www.minicircuits.com/pdfs/PHA-1%2B.pdf) describes4.8–5.2V operation,146mA typical and60°C/W junction-to-ground-lead thermal resistance; its6V absolute limit is not an operating target. Current PDF text was searchable but binary access returned403; earlier pin table identifies1RF_IN,2GND,3RF_OUT/DC,4ground paddle. Exact DF782/PL523 landing remains OPEN. [Mouser EU](https://eu.mouser.com/en/ProductDetail/Mini-Circuits/PHA-1%2B?qs=xZ%2FP%252Ba9zWqYz5cEhj1ZlVg%3D%3D) lists139-PHA-1,cut tape MOQ/multiple1,€2.82 at1,€2.11 at50; indexed4662 stock, no reservation. No50-piece break is booked for a20-unit fleet.

PD54008L-E's manufacturer15dB/8W result is at500MHz/7.5V, not144MHz. Its25V drain,−0.5..15V gate and3°C/W case thermal ratings do not establish AM stability. PD84001 is never fitted. The ST reference's5W connector result is0.116dB short of our5.135W capability investigation before changed losses; it neither proves full margin nor proves failure.

## Actual R1 RF implementation

Local source/filter retained; R602/R603/R604 now form a3dB candidate pad17.8Ω/287Ω/287Ω, adjustable by population after measurement. First testing uses the external generator or a12dB pad. Do not assume Si5351 available power: at20dB final gain,19.11dBm driver output requires approximately2–4dBm input for15–17dB MMIC gain, plus source filter/pad loss. Verify this budget at the actual port and configure drive strength accordingly.

U501 is replaced, its supply becomes a5V LDO, and Q501 is a functional-terminal PD54008L-E symbol. R606 bias feed is now VMOD, independent of the5V driver rail; start trim grounded and investigate50–200mA quiescent drain current with bounded energy. Gate clamp6.2V, inhibit clamp and stopper remain. Bias must remain fixed during supply AM; any thermal bias drift or low-drain gate behavior is a coupon measurement. Original APC circuitry is not claimed reused.

C605/L605 and L608/C610 are explicitly OPEN tuning positions. The illustrative input impedance5−j10Ω plus1Ω stopper is an assumption, not measured S-parameters. The [calculation](../hardware/2m/review/M5A-R1/calculations.json) gives28.87nH/59.57pF; output3.5Ω/60pF hypothesis gives14.51nH/81.74pF. These numbers do not qualify the network, its topology or stability. Do not populate for RF operation until the source trace is closed. The existing nine-pole ladder retains its R0 values only as an interim output-filter budget; it is not the ST−70dBc filter.

Measure small-signal stability with varying drain/gate bias, driven behavior through the envelope, out-of-band spectrum and mismatch. No unconditional stability factor can be calculated without relevant device S-parameters. Two-stage ST gain does not supply them.
''')
write('M5A_R1_AM_FEASIBILITY.md',f'''# M5A-R1 — low-voltage true-AM feasibility

{base}

**Plausible but unqualified evaluation candidate.** There is no retrieved manufacturer result demonstrating70–80% sinusoidal RF AM from the changed chain. The integrated schematic implements supply feedback and tone reconstruction; only a measured RF-envelope transfer can show that it produces the required emission.

Use continuous carrier within SLOT and keyed sine audio; outside SLOT both branches are inhibited. Preserve the [R0 PWM/controller contract](M5_2M_CONTROLLER_INTERFACE.md): ESP32-S3 supplies coherent LEVEL_PWM and AF_PWM, initially800Hz tone,312.5kHz PWM and appropriately scheduled samples. Two10kΩ/4.7nF unity-gain Sallen-Key stages reconstruct the waveform; no S3 internal DAC is assumed. KEY switches carrier-only reference versus sine at matching phase, with approximately3ms amplitude ramp. No IARU-mandated tone frequency is invented.

R1 changes normal feedback to18kΩ/10kΩ, gain2.8, improving low-voltage PWM resolution. U401C drives ST BD139/Q402 and D45H11/Q401; R506 falls100Ω→10Ω. The previous100Ω lost3.4V at34mA base current, enough to prevent the intended low-voltage crest. R5078.2Ω/helper clamp remains an approximate73mA limit, not a precision RF current regulator. Retain separate1.8A upstream-current trip, default base pull-up, command/helper clamps, driver switch and gate-bias inhibit. Feedback compensation4.7nF and101nF drain decoupling are starting values; no large electrolytic belongs on the modulated drain.

## Explicit transfer hypothesis

Illustrate, do not assert, `A_RF ∝ max(Vdrain−0.6V,0)`, anchored to the original5W/7.2V connector point. With this hypothetical knee, the required supply waveform is `Vcenter + m_RF(Vcenter−0.6)sin(ωt)`; supply fractional modulation is smaller than RF depth. A naïve4V center/0.8V trough is not evidence of usable RF behavior.

'''+table(['ERP carrier','Assumed center V','Crest/trough V at RF m.8','Upstream V'],[[p['erp'],f"{p['vcenter']:.3f}",f"{p['vcrest']:.3f} / {p['vtrough']:.3f}",p['upstream_v']]for p in a['profiles']if p['arch']=='BUCK4S'and p['m']==.8])+'''

The1dB capability investigation corresponds to roughly7.288V drain under this same hypothesis. This is independent of normal operating crest and must include actual output losses. If the PA acts as a voltage-independent linear amplifier, supply modulation will be too shallow. If it enters the knee, changes bias, oscillates, or has a nonlinear transfer, a sine supply can give clipped or distorted RF. A monotonic inverse calibration is permissible only after measured amplitude/phase maps show an acceptable waveform; it must not mask missing crest capability or unsafe trough bias.

Only the final drain is modulated. PHA-1+ runs from fixed5V, its output drive calibrated; gate bias has its own filtered fixed setting. Do not modulate APC, driver rail or gate threshold to hide an unusable drain transfer. The provisional R0 bias network needs temperature and low-drain review against the actual ST arrangement before RF layout.

## Headroom and low-voltage base drive

At full modeled crest, PA current is about1.36A and β40 implies34mA D45 base drive. With1V pass VBE,10Ω base resistor,8.2Ω emitter resistor,0.3V helper VCE and0.2V path allowance, required headroom is approximately2.12V. A10V rail−3% leaves about2.21V above the7.288V capability illustration: approximately0.29V remains under that particular crest-current bound. At the reserve-capability current it is smaller; margin is conditional. β20 can consume the margin or helper-current ceiling; it is not accepted automatically. Measure hot beta, op-amp drive, crest droop and loop recovery. R506's dissipation at73mA is0.053W; its1W/pulse allowance is retained pending exact part selection.

Use `m=(Amax−Amin)/(Amax+Amin)` from RF voltage envelope. Gates:70–80% depth at every supported channel/profile, nominal75%, no trough clipping or RF bursts, envelope THD≤5% and sideband imbalance≤1dB as initial engineering targets. These last two are project criteria, not IARU rules. Measure crest4.079W connector and test5.135W capability with the stated uncertainty/loss budgets. Neither supply oscilloscope shape nor an ideal op-amp simulation proves this.

D45 tab is collector/VPA; BD139 collector/tab is MOD_SINK. Neither may share an uninsulated grounded PA spreader. The [power/thermal review](M5A_R1_POWER_THERMAL.md) retains the66°C sensor trip and specifies a cooler assembly. Training still uses the independent current-modulated BJT; its104 fitted physical positions are electrically unchanged after effective variant values are applied.

The previous R0 ideal behavioral simulation is archived. R1 provides analytical envelope trajectories and passive transient calculations; no new transistor/RF AM simulation or physical distortion pass is claimed. Vendor RF/nonlinear models, feedback phase margin and real component beta/storage remain OPEN.
''')
# Power and thermal tables are read from the executable model, never hand-patched.
write('M5A_R1_POWER_THERMAL.md',f'''# M5A-R1 — power, thermal and endurance

{base}

Prefer the **2S boost population for a six-cell2S3P/M35A endurance evaluation**, with an exclusive4S buck alternative. The lower-voltage PA has not made a boost-free2S AM design credible: low pack voltage cannot deliver a roughly7.3V capability crest plus series-pass headroom. A4S buck can maintain10V throughout the proposed12–16.8V window, avoiding R0's high full-power cutoff. It saves approximately€1.93 on the board, but may require two more cells for robust extended endurance.

## Actual converter and rail changes

'''+table(['Rail','Native R1 feedback parts','Calculated settings'],[
['2S TPS611781','R401510k/R402100k, R414250k switched',f"{a['supply_settings']['boost_reduced_v']:.4f} / {a['supply_settings']['boost_full_v']:.4f} V"],
['4S TPS54302','R301116k/R30210k, R30327.8k switched',f"{a['supply_settings']['buck_reduced_v']:.4f} / {a['supply_settings']['buck_full_v']:.4f} V"],
['Driver TLV76150DCYR','Fixed5V; R4132.2Ω input; C409150µF output','5V±1.75% full temperature; Q304 switched separately'],
['Normal AM feedback','R51118k/R51210k','Gain2.8'],
['Protection','R81729.4k/R81580.6k; R82126.5k; R81320.9k',f"Driver OV{a['supply_settings']['driver_ov_v']:.3f}V, drain OV{a['supply_settings']['vpa_ov_v']:.3f}V, main OV≈10.50V"],
['Current/4SUV','R8294.02k; R807 variant24.9k; removeR830/Q801','Nominal1.80A trip;4SUV≈12.15V in both profiles']])+'''

Keep the R0 reverse/input/rail switches and window protection; replace the2A fuse candidate with Littelfuse `0466004.NRHF` (4A fast,1206). The manufacturer466series table (GD21-Jun-2023) specifies32VDC/50A interruption; actual BMS/pack prospective fault current, fuseI²t/temperature derating and trace coordination remain OPEN. A4A fuse is not the PA protection: the independent1.8A current trip remains. At6V, full-slot battery current can exceed2A, so the old rating lacked derating margin. The new fuse has a€0.50 estimate, not a quote. Other and converter compensation as candidates. TPS611781 remains4.7µH/approximately500kHz,5A nominal switch limit; current slope, compensation and effective capacitance need exact-component qualification. At6V input,10V output and80% of4.7µH at400kHz, ripple≈1.60A p-p. A1.55A output crest needs≈2.97A input at87%, giving≈3.77A switch peak before losses/tolerances. The lower-efficiency cases can trip the1.8A local limit: their calculated endurance is not sustainable operation. Fuse4A input/its I²t, wiring and BMS must support intended crest pulses without sacrificing fault interruption; exact fuse remains OPEN.

## Driver simplification and fault limits

The former driver buck/magnetic/feedback is removed. [TI TLV761](https://www.ti.com/lit/ds/symlink/tlv761.pdf), SBVS349D May2025, supports18V input/20V absolute, DCY pins1GND,2OUT/tab,3IN, with1–220µF and2–500mΩ output-capacitor ESR. Exact5V part is orderable; LD1117 was rejected because its ordinary15V absolute input limit is insufficient for a16.8V upstream fault. The new live LDO tab is5V, not ground.

At180mA and10.5V VMOD, R413 drops0.396V and LDO heat is about0.92W. Require effective thermal resistance≤80°C/W at45°C local ambient (estimated Tj≤119°C), or change package/cooling after measurement. The generic95.4°C/W datasheet fixture would be too hot near this worst condition. At7.5V−3%, after damping and a0.2V path allowance, LDO input remains≈6.68V; verify regulation under load/startup. Power-on inrush into150µF is not a qualified normal transient.

C409 requires120–180µF actual capacitance, ESR2–100mΩ, exact part and footprint OPEN. D309 is a Schottky output-to-input bypass per TI reverse-current guidance; its actual current/voltage/surge and package remain sourcing/measurement gates. Q304 independently isolates RF drive. For an LDO-short fault with10.5V source,5.0875V initial rail,R≥2.178Ω,C≥120µF,ESR≤0.1Ω and **Q304 physically open within20µs**, the ideal RC/ESR calculation peaks at5.691V. At100µs it can exceed the6V absolute limit. Overshoot, MOSFET delays, surviving VMOD storage and ground bounce are not included. Q302 opening alone does not remove energy already in C306; measure Q304 isolation itself. Test with MMIC omitted, equivalent load and bounded fault source before connecting it. This is a conditional calculation, not protection qualification.

## Thermal discrepancy resolved as an assembly requirement

Do not raise the approximately66°C thermistor threshold. The lower-voltage PA draws more current and does **not** automatically reduce pass heat. Preserve ST D45H11, RθJC2.5°C/W, and its live collector tab; hot DC/repetitive SOA remains OPEN until the exact graph is assessed against the full trajectory. Device nominal current/power ratings do not close that gate. The model includes BD139 base-drive heat and fixed5V driver losses.

'''+table(['Assumedη/full-carrier','ERP/m','Pass mean/peak W','Helper mean/peak W','Case/Tj estimate °C'],[[t['eta'],f"{t['erp']}/{t['m']}",f"{t['pass_mean_w']:.2f}/{t['pass_peak_w']:.2f}",f"{t['helper_mean_w']:.2f}/{t['helper_peak_w']:.2f}",f"{t['hot_case_estimate_c']:.1f}/{t['junction_estimate_c']:.1f}"]for t in a['thermal']if t['eta']==.45 and t['m']in[0,.8]])+'''

These illustrative periodic results require a shared3°C/W spreader,80J/K thermal capacity,1°C/W insulated pass interface,45°C ambient and60s on/240s off. They are not a10°C/W isolated sink or continuous-carrier result. Require measured pass case and correctly bonded sensor≤60°C during normal profiles, measured junction estimate≤125°C with margin, and trip before hot SOA is exceeded. Validate sensor-to-case offset, mounting tolerance and response delay; electrical open/short detection does not detect a detached intact sensor. The unqualified spreader/insulation costs€8–14 outside PCB components. Actual pass/PA heat, case-to-spreader contact and hot SOA can require more cooling.

Carrier-only within a slot is hotter for the pass transistor than the modeled AM mean. Continuous full-power beacon dissipates roughly8.6W in the shared assembly in the no-tone example:3°C/W gives a spreader near71°C before interfaces, so that arrangement is NO-GO for continuous service at45°C. A separately qualified≈1°C/W or better thermal assembly is required; battery-only beacon hours below are energy upper bounds.

## Endurance — modeled, not measured

[Analysis script](../tools/m5a_r1_analysis.py), [JSON](../hardware/2m/review/M5A-R1/calculations.json), [60-row pack CSV](../hardware/2m/review/M5A-R1/endurance.csv) and [288 sensitivities](../hardware/2m/review/M5A-R1/sensitivity.csv) retain the M2/R0 cell framework. Assumed current is `I=0.1+gV`, g calibrated at45% full-carrier PA efficiency; reduced efficiency changes with voltage. The RF amplitude law is explicitly hypothetical. Main boost/buck efficiencies87/91%, controller0.14W, RF idle0.03/0.04W, driver146mA, source0.11W/90%, helper/bias0.30W and20% complete-slot RF duty are included. PREPARE must be withdrawn between slots. Morse-space carrier remains powered, so no mark-duty credit is taken.

'''+table(['Supply/ERP,m.8','TX/average W','12h/24h Wh'],[[p['arch']+'/'+str(p['erp']),f"{p['tx_battery_w']:.2f}/{p['average_battery_w']:.3f}",f"{p['need12_wh']:.2f}/{p['need24_wh']:.2f}"]for p in a['profiles']if p['m']==.8])+'''

Cells remain25R minimum-capacity proxy8.82Wh and M35A minimum-energy11.9Wh. Multiply by0.8 aging×0.9 temperature×0.9 accessible-endpoint allowance. These are not equal-resistance/current-rated cells. R1 has no additional R0-style0.60 high4S cutoff-window factor, but the remaining0.9 accessible-energy factor is unmeasured at12.15V cutoff; validate actual discharge curves, sag and cold cutoffs.

'''+table(['Pack/cell','Full1ERP h','Reduced.30ERP h','Full/reduced continuous beacon h'],[
[pack+'/'+cell,
 f"{next(x for x in a['endurance']if x['pack']==pack and x['cell']==cell and x['erp']==1 and x['m']==.8)['modeled_hours']:.1f}",
 f"{next(x for x in a['endurance']if x['pack']==pack and x['cell']==cell and x['erp']==.3 and x['m']==.8)['modeled_hours']:.1f}",
 f"{next(x for x in a['endurance']if x['pack']==pack and x['cell']==cell and x['erp']==1 and x['m']==.8)['beacon_hours']:.1f}/"+f"{next(x for x in a['endurance']if x['pack']==pack and x['cell']==cell and x['erp']==.3 and x['m']==.8)['beacon_hours']:.1f}"]for pack in ['2S2P','2S3P','2S4P','4S1P','4S2P']for cell in ['25R_min','M35A_min']])+'''

2S2P/M35A fails the modeled full target;4S1P/M35A barely passes full but fails24h reduced.2S3P/25R fails extended. The smallest two-target base-model candidate is2S3P/M35A;2S4P/25R and4S2P with either class also pass this model. None is a qualified minimum. Both1ERP and guarded0.9ERP calculations exist; choose actual settings from calibrated antenna/feeder uncertainty, not runtime convenience.

Sensitivity variesη32/45/55%,Iq100/200mA,driver146/180mA,controller0.14/0.28W and LoRa absent/intermittent0.006W/continuous receive0.045W. Poor-efficiency cases may exceed current trip and cannot sustain full output. LoRa bursts0.44W×80ms/min add0.000587W as an additional allowance; exact Silicontra currents remain OPEN. Double controller overhead removes3.36Wh/day; PA/linear-pass loss dominates this candidate. Radio-absent is supported; source/regulator idle is not assumed zero. Standby measurements and thermal/inhibit behavior must precede endurance claims.

No new accepted ADR is changed. This is a proposed VHF-specific operating-point update within the existing dual-voltage architecture; neither controller hardware nor80m power circuits are edited.
''')
# Compare complete module baskets; retain estimates for OPEN tuning positions.
q10={s['variant']:s for s in c['summary']if s['fleet']==10}
oldcost=json.loads((R/'hardware/2m/review/M5A-R0/costs.json').read_text());old10={s['variant']:s for s in oldcost['summary']if s['fleet']==10}
removed=sorted(set(op)-set(np));added=sorted(set(np)-set(op));changed=[ref for ref in sorted(set(op)&set(np))if any(op[ref].get(k)!=np[ref].get(k)for k in ['value','mpn','pins','footprint','variant_values'])]
write('M5A_R1_COST_DELTA.md',f'''# M5A-R1 — itemized cost comparison

{base}

These are **provisional net EUR component allowances**, not completed supplier quotes or a release ordering list. R0 accounting is preserved. The lower-cost R1 basket includes source, filters, training, AM, converters, enable/protection and board connectors. Unretrieved ST matching is **not** credited with imagined component savings: interim tuning/matching allowances remain. Actual ST network reconstruction may change them.

## Function-normalized baskets, EUR per board

'''+table(['Complete basket','6','10','20'],[[name]+[f"{next(s for s in b['summary']if s['basket']==name and s['fleet']==q)['net_eur']:.2f}"for q in [6,10,20]]for name in ['R0_2S','R0_4S','R1_2S_PHA1','R1_4S_PHA1','R1_2S_PHA13_strong','R1_4S_PHA13_strong','R1_training']])+f'''

Quantity-ten2S savings are **€{old10['BOOST2S']['component_allowance_net_eur']-q10['BOOST2S']['component_allowance_net_eur']:.2f} /{100*(1-q10['BOOST2S']['component_allowance_net_eur']/old10['BOOST2S']['component_allowance_net_eur']):.1f}%**;4S saves **€{old10['BUCK4S']['component_allowance_net_eur']-q10['BUCK4S']['component_allowance_net_eur']:.2f}**. Training remains€16.37. The approximately€36 target has **not** been achieved, and even€45–50 is not established for the2S implementation.

The conservative PD54008/PHA13 counterfactual includes the8V buck, its RC components and corresponding OV threshold, with10V upstream for **both** RF profiles. Its driver cannot run from the preferred5V LDO or7.5V reduced rail. Only the economical design is implemented in native KiCad. The counterfactual is a complete cost basket for review, not a second secretly qualified circuit; reduced-profile heat/endurance must be recalculated if selected.

## Actual component/count change

'''+table(['Population','R0 physical/IC','R1 physical/IC','q10 component delta'],[[var,f"{old10[var]['fitted_physical']}/{old10[var]['ic_count']}",f"{q10[var]['fitted_physical']}/{q10[var]['ic_count']}",f"€{q10[var]['component_allowance_net_eur']-old10[var]['component_allowance_net_eur']:+.2f}"]for var in ['BOOST2S','BUCK4S','TRAIN_ONLY']])+'''

Test pads, flags and footprint assignments are not purchased ICs. Removed driver L303,C408,R406,R407; replaced U303 with a fixed LDO and added reverse-discharge D309. Removed4S threshold R830/Q801 because10V can be supported near12V input. Safety IC count remains unchanged; no independent function is deleted to manufacture a saving. Exact changes, including values/pins, are in [component-delta.json](../hardware/2m/review/M5A-R1/component-delta.json).

## Functional block totals, preferred2S population

'''+table(['Functional block','q6','q10','q20'],[[g]+[f"{next(s for s in c['summary']if s['variant']=='BOOST2S'and s['fleet']==q)['blocks'].get(g,0):.2f}"for q in [6,10,20]]for g in sorted(q10['BOOST2S']['blocks'])])+'''

The necessary fuse correction adds€0.30against the old€0.20estimate; no actual supplier saving is implied. The remaining costs include€7.65 training circuitry,€5.43 normal harmonic filter,€2.98 source filter,€4.09 main boost,€2.73 provisional matching,€1.43 bias,€2.94 AM/pass functions and€3 connector allowance. These are complete functions, not just silicon. RF magnetics and exact RF capacitor/current/Q ratings remain unquoted; do not replace them with arbitrary cheap parts. A simpler verified ST filter could save material, but no saving is booked before its circuit is traced.

## Supplier evidence and MOQ

| Item | Supplier/order identifier | Observed display / availability | Accounting |
| --- | --- | --- | --- |
| PD54008L-E | [DigiKey IT](https://www.digikey.it/de/products/detail/stmicroelectronics/PD54008L-E/1038978),497-6471-1-ND | Net€7.32/5.677/5.266 at1/10/25; indexed1988 stock,last-month crawl | q6 uses1-break,q10/20 uses10-break; CT MOQ1, not3000-reelMOQ |
| PD54008L-E alternate | [Mouser DE](https://www.mouser.de/de/ProductDetail/STMicroelectronics/PD54008L-E?qs=sGAEpiMZZMsPo2fL1zXfdqEwePZnwSUq%2Fv1gNDbGsv4%3D),511-PD54008L-E | Display≈€5.30 at10; locale/tax/stock need checkout confirmation | Alternative observation, no unverified lower net cost booked |
| PHA-1+ | [Mouser EU](https://eu.mouser.com/en/ProductDetail/Mini-Circuits/PHA-1%2B?qs=xZ%2FP%252Ba9zWqYz5cEhj1ZlVg%3D%3D),139-PHA-1 | Display€2.82 at1,€2.11 at50; CT MOQ/multiple1,indexed4662 stock,two-day crawl | Provisionally held as net; no unsupported10/20 break |
| TLV76150DCYR | [DigiKey DE](https://www.digikey.de/en/products/detail/texas-instruments/TLV76150DCYR/18115428),296-TLV76150DCYRCT-ND | Net€0.47/0.334 at1/10,indexed8483; page has marketplace flag | No stock guarantee; direct-distributor fulfillment/freight must be reconfirmed |
| Other positions | Per-reference CSV | R0 historical observations/family allowances and estimates | No new verified basket invented; exact MPNs/geometry marked OPEN |

Sources were reviewed2026-10-15. Indexed stock is not a current cart reservation. Cut tape is chosen; no reel conversion/reeling fee assumed. Do not buy25 finals to obtain its price for20 boards unless leftover inventory is separately approved/accounted. All prices exclude VAT; illustrative19% VAT is applied once to the taxable total, not selectively deducted from uncertain display prices. Freight/fees remain separate.

The [actual R1 BOM](../hardware/2m/review/M5A-R1/RF2M_BOM.csv) gives every fitted line at6/10/20 with MPN/value/footprint, pooled demand, MOQ, multiple, source, supplier identifier, stock qualification and evidence class. [All four required function-normalized baskets](../hardware/2m/review/M5A-R1/comparison-baskets.csv) are also itemized.37 preferred2S MPN positions remain OPEN; quotations and physical qualification are still required. A numeric allowance for an OPEN position is explicitly an estimate, not a sourced component.

## Materials outside the component total

At6/10/20, use the same unquoted bare-board allowance€2–6/module until coupon stack-up/area is known; no promotional fabrication claim. Add external RF harness€2–4,antenna/feed€8–15,thermal/insulation€8–14. Board connectors are already counted. Thus installed module allowance is components **+€20–39**, excluding labor/enclosure/controller/pack. Changed thermal expectations can consume part of the board saving; the former€4–7 cooling allowance is not assumed qualified.

For supply comparison, reuse **historical** M5/M2 cell prices, not new observations. Six tagged M35A cells at6/10/20 fleets cost€22.68/22.68/21.72; estimated2SBMS€3 and insulation/interconnect€3 give2S3P material€28.68/28.68/27.72. Eight cells plus4SBMS€4.50 and interconnect€3 give4S2P€37.74/37.74/36.46. These are a separate illustrative pack scope; the more detailed M2 pack model uses different mechanical allowances and is not silently rewritten.4S's€1.93 board saving is less than the approximately€9 pack increase if eight rather than six cells are needed. Equal-cell packs have equal nominal energy; chemistry, pack state and cutoff determine accessible energy.

At quantity10, full2S material with the illustrative2S3P pack,€15–20 shared controller and€3–6 enclosure is approximately€119.01–146.01, before labor,fleet charging,freight or shielding. This remains a budget; no completed transmitter cost is implied. Optional shield material€1–3 is separate and conditional. One charger per four units is the retained M5 fleet-turnaround estimate:6/10/20 need2/3/5 chargers at estimated€15(2S)/€20(4S) each; this shared equipment is not charged inside each PCB BOM. No tooling/provisioning/labor is disguised as purchased unit material. The Foxoring-only80m audit is untouched and is not reinterpreted as this VHF training cost.
''')
# Machine-readable changed positions, preserving provenance to the old native snapshot.
(O/'component-delta.json').write_text(json.dumps(dict(baseline_commit='ea671c1',baseline_tag='m5a-r0',removed={k:op[k]for k in removed},introduced={k:np[k]for k in added},changed={k:dict(before=op[k],after=np[k])for k in changed}),indent=2)+'\n')
write('M5A_R1_SCHEMATIC_REVIEW.md',f'''# M5A-R1 — schematic review and verification

{base}

The [existing editable project](../hardware/2m/RF2M.kicad_pro) is evolved in place; [PDF](../hardware/2m/review/M5A-R1/RF2M.pdf), [XML netlist](../hardware/2m/review/M5A-R1/RF2M.net.xml), [manifest](../hardware/2m/RF2M.electrical.json), [position list](../hardware/2m/review/M5A-R1/RF2M_positions.csv) and [variant BOM](../hardware/2m/review/M5A-R1/RF2M_BOM.csv) come from that revision. R0 remains native in its archive and tag`m5a-r0`. RF80/M4 and existing ADR files are unchanged. This is **not** a completed, traced reproduction of the ST RF artwork.

## Implemented changes

- U501PHA-13HLN+→PHA-1+, with correctly named functional symbol and same1IN/2GND/3OUT+DC/4ground-paddle connection. DF782 landing OPEN.
- Q501PD55008-E→PD54008L-E functional G/D/S symbol. PowerFLAT5×5HV numeric pad map, thermal source lands and orientation remain **blocking OPEN**. No generic MOSFET footprint is substituted.
- R301/R303 and R401/R414 set7.5V reduced/10V full.4S no longer has a separate high full-power cutoff; remove R830/Q801. Main pack/window, current, OV and independent switches remain.
- U303 becomes TLV76150DCYR with1GND,2OUT/tab,3IN. Remove driver-buck L303,C408,R406,R407. R413 moves to LDO input. C407 is1µF input; C409150µF/25V output with qualified ESR requirement; D309 bypasses LDO reverse current. Exact C409 part/geometry OPEN. No driver-buck fault model is misrepresented as qualification of the new LDO.
- R506100Ω→10Ω restores modulator headroom. R51118k sets normal feedback gain2.8. R606 now feeds fixed bias from VMOD rather than the new5V driver rail. Output bulk capacitance is kept upstream of the pass transistor.
- F301 becomes4Afast0466004.NRHF because low-battery transmit-slot current can exceed2A. Exact supplier quote, footprint/temperature and50A-interrupt coordination with the protected pack remain OPEN; the1.8A PA trip is preserved.
- Analog thresholds updated: driver≈5.737V,main≈10.50V,drain≈8.203V,upstream current≈1.80A. Hot comparator common-mode/current-reference regression retained. The increased current threshold requires actual fuse, magnetics and thermal qualification.
- Source pad changes to3dB candidate17.8/287/287Ω. First tests use larger attenuation/external RF generator. Matching C605/L605/L608/C610 marked OPEN; inherited R0 large-signal estimates are no longer silently labelled PD54008 matching. LPF unchanged pending original-ST trace, with no imported ST harmonic claim.
- TP604 exposes PA_IN50; remove C602 for external final-drive injection so the generator cannot back-drive the MMIC. Test points add no purchased IC or connector.
- MODULE_ID becomes12.1k(2S) or27.4k(4S); training remains47k. Controller pinout unchanged, but new revision/calibration tables are mandatory. Firmware for R0 must refuse an unknown R1ID rather than applying old levels. Controller hardware is not changed here.

The removed overflow supply sheet is preserved in the R0 archive/history. The active hierarchy is15sheets plus root,16PDF pages. Regeneration tools use a new R1 output path; frozen R0 tools/reports are not rewritten.

## Supply and enable behavior

20-pin connector assignment remains [R0 contract](M5_2M_CONTROLLER_INTERFACE.md). Logic is3.3V; battery current uses separate keyed J301/return. Power and logic can be present separately only with the existing bias/pull-down/isolation behavior verified. SRC_ON isolates the source/bus; NORMAL_PERMIT gates MMIC supply, normal bias and AM command; TRAIN_PERMIT gates the separate buffer and current-modulated BJT. Source clocks alone are not a digital permission to energize the final. Analog off-slot RF leakage and capacitive feedthrough remain measurements.

Raw ARM captures path/profile/context with KEY=0 and SLOT=0. PREPARE, valid heartbeat, mute and SCL-high health qualify the context; delayed ARM gives settling time. Keep SLOT low for at least50ms and verify PA_RAIL_ADC after profile capture/rail change. A fault clears context; ARM held high cannot automatically rearm. Retuning first withdraws SLOT/ARM and drive; I²C activity clears permission. No live profile/path transfer is allowed. PREPARE must be withdrawn between scheduled slots for the endurance model to apply.

The RF outputs have independent conductive branches and different SMA/MCX connectors; no watt-output RF selector feeds the training port. Training-only assembly omits all normal power parts and uses R519 in place of U207's normal-health function. Effective training values/net connectivity/MPNs/footprints are checked against R0 for all104 fitted physical parts. Isolation under coupling/device faults still needs physical measurements.

## Actual checks and limits

KiCad10.0.6 ERC was run: **0errors,3warnings**. Warnings are the intentionally OPEN footprint selections J301,J701 and C409; they are not excluded. Empty RF device footprints do not necessarily trigger ERC, so their separate audit remains essential. No PCB exists and no DRC result is claimed.

The actual exported XML is checked against every manifest pin. Netlist-derived digital tests pass **{v['logic']['combinations']} combinations,{len(v['logic']['scenarios'])} scenarios,{len(v['detected_mutations'])} rejected mutations**. These cover captured selection, heartbeat/mute/reset/I²C loss, invalid arming, no dual path, faults requiring fresh ARM, keyed tone with in-slot carrier, absent PA population, physical-terminal mutations and revised value regressions. There are33 audited critical-device entries: **Q501 is functional-only**, and several numeric mappings still have OPEN geometry. “PASS” in [verification.json](../hardware/2m/review/M5A-R1/verification.json) means these limited checks passed, not physical-package or analog qualification.

[Pinout-audit.json](../hardware/2m/review/M5A-R1/pinout-audit.json) explicitly sets physical release BLOCKED. D45H11 and ST BD139 remain1B/2C/tab/3E. TI TL431 remains1K/2REF/3A. LDO pad2/tab is5V. The new final must not inherit PD55008 numeric pads or a generic8-power-pin assumption. No PD84001 footprint or obsolete part is introduced.

Remaining analog items: real watchdog/ARM propagation and supply collapse, comparator VOL/common-mode/tolerance, D309 reverse discharge, LDO fault isolation≤20µs, source feedthrough, hot pass SOA, AM-loop phase margin, gate-bias thermal stability, RF matching/stability and port isolation. The tests do not model those behaviors. Source classification is detailed in the [reference audit](M5A_R1_ST_REFERENCE_AUDIT.md); all physical gates remain NOT_RUN.
''')
write('M5A_R1_PA_TEST_PLAN.md',f'''# M5A-R1 — smallest decisive PA/AM coupon

{base}

**No PCB is laid out or authorized for fabrication.** The coupon layout is currently NO-GO until readable original ST circuit/package drawings close the named topology/pad/land blockers. Thereafter a small standalone PA coupon, not the integrated transmitter PCB, is the next useful engineering step. Its purpose is to settle final-stage gain, drain-to-RF transfer, stability and crest capability. It may omit the controller/source/watchdog because laboratory enable/current limits control this isolated fixture; the integrated R1 schematic retains full-system interlocks.

## Coupon scope and interfaces

- One PD54008L-E, exact verified PowerFLAT land and source thermal contact, removable/tunable144MHz input and output matches, gate stopper/bias isolation, output LPF and50Ω SMA reference port. Original ST final/output topology must first be traced; do not manufacture the OPEN assumed-impedance harness.
- Separate50Ω drive input for a laboratory generator. The PHA-1+ driver may be evaluated on a removable adjoining fixture later; no need to populate both complete alternative MMICs. Keep a calibrated interstage measurement plane and DC block. Integrated board test injection uses C602 omitted and TP604/PA_IN50; never connect a source across an active MMIC output.
- Independent adjustable gate bias with default ground, measurable drain current and separate bounded drain supply. External modulated supply can characterize AM before D45H11/BD139 or a battery converter is fitted. Start gate trim grounded; constrain VGS from−0.5to+15V, and use a much lower conservative practical drive/bias limit.
- Target the original0.508mm FR4/70µm construction, supplier-declared dielectric/mask. Recalculate every changed microstrip width/length/launch. No0.92mm trace copied to1.6mm FR4. RF ground/vias, exposed source land, thermal attachment and tunable-value pads must be reviewed before routing approval.
- Kelvin DC current connection, drain RF choke/bypass arrangement verified for AM bandwidth, removable load/filter links, thermocouple attachment and short RF probe ground. No large capacitor on the modulated drain. External lab enclosure/attenuation prevents unintended radiation.

## Shared instruments

Current-limited0–12V lab supply with bounded overshoot, gate-bias supply, RF generator with calibrated output (external laboratory booster if more drive is needed), VNA with bias isolation, spectrum analyzer through rated40–60dB attenuation, calibrated≥10W50Ω dummy load, carrier/PEP power meter, oscilloscope with RF envelope detector, active RF probes≤0.5pF where needed and appropriate differential voltage probes and current/temperature logging. Use a calibrated directional coupler for mismatch/reflected power. Account for load/filter/cable loss and detector response. Bench connections are conducted into loads; no antenna/RF transmission authorization is implied.

## Staged gates — all NOT_RUN

| Stage | Bounded method | Objective pass/stop criteria |
| --- | --- | --- |
|0Package/continuity | Microscope, meter; verify exact installed marking/orientation and source thermal land | Exact physical G/D/S assignment agrees with audited symbol/PCB. Any unknown land is STOP. |
|1Bias only | RF input terminated; drain1V/current limit50mA, bias0V; increase drain toward4V in small steps with≤100mA initial limit | No unexpected current/oscillation; then set proposed Idq50mA and investigate100–200mA only intentionally. Never turn the trim while unrestricted. |
|2Small-signal/stability | Low drive, drain2/4/6/7.2V, selected biases; VNA/calibrated gain plus wideband spectrum | Measured match/gain repeatable across144.5–144.9MHz; no autonomous oscillation over50MHz–1GHz initially, extend analyzer range for harmonics.50Ω stability alone does not qualify mismatch. |
|3CW map | Start−20dBm input, increase stepwise with output load; drain bounded≤7.5V initially and current≤1.8A | Map connector power/gain/current/compression versus voltage. Demonstrate4.079W operational crest and investigate5.135W connector capability; stop if gain/temperature/current precludes it. Final plane must cover measured filter loss. |
|4Driver | Independently measure PHA-1+ gain/P1dB at4.8/5.0/5.2V and hot/cold conditions | At actual required final drive, ≥3dB backoff including1.25dB input-loss budget/uncertainty. At20dB final gain this needs P1dB≥22.11dBm at the capability test. If failed, retain stronger driver/fallback basket; do not call a cheap MMIC adequate. |
|5Drain transfer | Fixed drive/bias; slow sweep≈0.5–7.5V, monitor gate/drain currents and output amplitude/phase | Reproducible monotonic usable transfer; map RF knee, trough leakage and AM-to-PM. Record changing input/output match. No irreversible current, oscillation or hysteresis. |
|6Low AM | External bounded supply, initially10%,then30% RF depth at800Hz | No envelope clipping, unstable sidebands or bias runaway. Calibrate from RF amplitude, not supply percentage. |
|7Full AM | Calibrated75% target, prove70–80% across band/profile/supply/temperature; then integrate pass loop | RF-envelope THD≤5%,sidebands symmetric≤1dB initially; maintain carrier/crest capability. Reject if an inverse command cannot produce a sine safely or if trough behavior is unstable. |
|8Carrier/PEP/ERP | Calibrated carrier, true PEP detector/coupler; actual antenna/feeder measured separately |1.259W connector carrier corresponds to1ERP only under unqualified−1dBd assumption. Guard event setting below1ERP and reduced setting above0.25ERP including uncertainty. |
|9Thermal/SOA | Log1min on/4min off, carrier-only and80% AM at45°C intended ambient; energy-limited soak | Case/sensor≤60°C normal target, estimated Tj≤125°C, no hot DC/repetitive SOA violation; verify66°C sensor trip with mounting delay. No continuous beacon approval from contest test. |
|10Spectrum | Source, driver and output analyzer measurements; safe attenuators | Applicable country unwanted-emission mask plus project headroom; no imported ST−70dBc claim. Initial harmonic target≤−60dBc and no anomalous out-of-band oscillation, revise only to justified stricter legal/project mask. |
|11Faults/shutdown | Dummy-load rail, MMIC/PA omitted first; bounded LDO-short and converter fault fixtures | Driver≤5.9V until physical Q304 isolation≤20µs under defined10.5V fixture; no VGS breach, pass short caught, thermal/current/window trip clears ARM. Fault recovery requires deliberate rearm. |
|12Integrated isolation | Normal output loaded; training port terminated/detected, both directions and off-slot cases | No simultaneous permission; off-slot/inhibited connector output initially≤−60dBc relative to active carrier and≤1µW absolute. These are engineering detection gates, not a definition of legal silence. If coupling fails, investigate shielding/layout before release. |

Mismatch testing starts at low voltage/power with a tunable load and reflected-power monitoring, never the original board's claimed20:1 test applied blindly. Establish a conservative2:1 all-phase survival gate first; severe/open/short cases require a separate bounded plan. No unrestricted Li-ion fault injection. Check source waveform, local bias/decoupling and switcher spur interaction before connecting the synthesized chain. Training retains calibrated nominal1µW/optional1–10µW output and true keyed-tone AM; calibrate at its own reference connector.

## Decisive outcome

Accept the economical chain only if the same configuration simultaneously closes gain/backoff, connector carrier/PEP, full70–80% RF sine AM, spectral, thermal and supply gates. If required gain is too low, use the stronger driver basket and recompute heat/endurance. If the low-voltage final cannot provide the RF envelope or crest safely, return to preserved R0; do not lower the competition requirement to save money. Document raw instrument files, calibration planes, firmware/generator settings, temperature and uncertainty. No test is PASS until actual data exists.
''')
write('M5A_R1_REVIEW_DECISION.md',f'''# M5A-R1 — engineering review decision

{base}

**NO-GO for PA/AM coupon layout today; GO for independent review of the revised electrical candidate.** The necessary source-tracing and final-package evidence could not be retrieved as readable images. This milestone therefore has **open acceptance items**, not a completed manufacturer-derived RF implementation. Close the originalST circuit/net trace and exact physical landing first; then a small externally driven PA coupon is the next bounded step. No further architecture study is recommended.

## Recommendation and economic result

Prefer evaluation of **PD54008L-E/PHA-1+**, fixed5V driver LDO, final-only drain AM through ST D45H11/BD139 and exclusive2Sboost or4Sbuck at10Vfull/7.5Vreduced. Maintain the fully separate training branch and all R0 fail-off functions. Conditional means measured gain/backoff, matching, crest, trough and hot SOA can reject this candidate. The oldPD55008-E/PHA-13HLN+ design remains the fallback, not a validated release.

At10 units the actual component allowances are **€52.33(2S),€50.40(4S),€16.37(training)** net, versus€74.61/€72.77/€16.37R0. The2S reduction is€22.27(29.9%). The complete stronger-driverPD54008 basket is€65.13(2S) or€63.20(4S), including its different indispensable8V supply. All contain normal full-system functions where applicable. The€36 goal is not achieved. Filters/matching,training,conversion and AM/protection remain significant;37preferred2S MPN positions are unresolved; roughly€43.50of the€52.33total remains estimated/family-allowance material. These are partly estimated budgets, not proven repeatable prices.

Desired connector carrier is1.258925W for an **assumed**−1dBd antenna/feed system;80%AM needs4.078918W PEP and a5.135054W capability investigation. With0.75dB output loss, final-plane capability must be6.103W. A20dB final-gain assumption requires19.11dBm driver output and22.11dBm P1dB for3dB backoff. Neither final gain nor driver compression has been measured at144MHz. Original fixed-supply ST performance does not establish AM or capability reserve.

The low-voltage RF-transfer hypothesis suggests center3.912V,crest6.561V,trough1.262V at1ERP/m.8, but it is not a characterized transfer law. Pass heat is modeled4.50W average under full AM and5.17W carrier-only. The sensor trip remains≈66°C; a specified cooler shared assembly is required. No thermal or SOA PASS is claimed. The modeled2S3P/M35A target candidate gives17.6hfull/30.9hreduced under base assumptions; poor efficiency/current trips can invalidate it.4S1P/M35A gives only12.5/21.6h and is not a robust two-target pack.

## Delivered and verified

- [Editable existing KiCad project](../hardware/2m/RF2M.kicad_pro), [R1 PDF](../hardware/2m/review/M5A-R1/RF2M.pdf), actual XML netlist, revised manifest/local symbols and 6/10/20 variant/counterfactual BOMs.
- [Reference audit](M5A_R1_ST_REFERENCE_AUDIT.md), [RF choice](M5A_R1_RF_SELECTION.md), [AM feasibility](M5A_R1_AM_FEASIBILITY.md), [power/thermal](M5A_R1_POWER_THERMAL.md), [cost delta](M5A_R1_COST_DELTA.md), [schematic review](M5A_R1_SCHEMATIC_REVIEW.md) and [coupon gates](M5A_R1_PA_TEST_PLAN.md).
- Actual KiCad10.0.6 ERC:0errors/3documented OPEN-footprint warnings. Netlist/manifest parity;4096digital combinations,36state scenarios,13detected mutations;33critical audit entries with explicit functional-only/open geometry states. This is not physical pinout qualification of Q501.
- R0 preserved at commit`ea671c1`,tag`m5a-r0`,native archive and unchanged historical reports.335frozen80m/ADR/project-baseline files are checked unchanged. The R1 preservation adapter permits only the explicitly new ADR0013 file; the original R0 snapshot is not rewritten. Full and training variants remain one primary2mPCB; no secondMCU or controller redesign.

## Acceptance status and smallest remaining corrections

| User criterion | Status | Remaining action |
| --- | --- | --- |
| 1. Actual original ST topology trace | **OPEN/blocking** | Readable Figures12–17 and original Gerber net/line inspection; values alone are insufficient |
| 2. Separate reference from AM capability | DONE/documented | Physical AM/capability still NOT_RUN |
| 3. Obsolete-driver replacement strategy | DONE/conditional | PHA-1+ selected for evaluation; measure gain/P1dB before acceptance |
| 4. PD54008 physical package audit | **OPEN/blocking** | Exact G/D/S pad/source thermal land/orientation from manufacturer drawing |
| 5. Matching justified | **OPEN/blocking** | Replace labelled OPEN harness with traced ST derivative; account for stack-up |
| 6. TrueAM implementation path | PLAUSIBLE/unqualified | RF transfer and70–80% clean modulation measurements |
| 7. Crest/trough/dropout | DONE/calculated | Confirm actual low-drain transfer/hot base drive |
| 8. Thermal/sensor consistency | DONE/as a conditional assembly requirement | Hot SOA, thermal attachment and trip delay NOT_RUN |
| 9. Complete2S/4S comparison | DONE/modeled | Efficiency,cutoff energy and pack tests NOT_RUN |
| 10. Itemized savings | DONE/provisional | Exact quotes/37OPEN2S MPN positions remain |
| 11. Actual editable R1 | DONE/evaluation candidate | RF matching and final landing intentionally OPEN |
| 12. Pin/logic regressions | DIGITAL PASS;PHYSICAL PARTIAL | Numeric final map remains blocking |
| 13. Minimum experiment | DONE/specification only | Layout is not authorized in this milestone |
| 14. Unmeasured unqualified | DONE | No invented physical pass |
| 15. No purchasing/fabrication/RF | DONE | No procurement or operation occurred |

Controller20-pin assignment is retained; module-ID codes12.1k/27.4k distinguish revised normal populations from R0,training remains47k. Futurecontroller firmware must recognize the new gain/rail calibration and keep unknown country/frequency/module profiles unarmed. ExistingS3/RTC/optionalSilicontra hardware is unchanged. Proposed [ADR0013](decisions/ADR-0013-vhf-low-voltage-evaluation-candidate.md) records this candidate without accepting or overwriting earlier decisions.

The retained [2025rulebook](https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf),Appendix1T2.8, specifies144.500–144.900MHz,better-than50ppm,>200kHz simultaneous-transmitter separation,0.25–1WcarrierERP,A2A70–80%AM,8–15WPM,horizontal antenna2–3m. Guarded0.90/0.30ERP settings are examples only:±0.4dB gives≈0.821–0.987/0.274–0.329ERP. Actual antenna/feeder uncertainty must fit the limits. IARU rules do not authorize transmission; country profile and applicable unwanted-emission rules remain separate gates. No antenna or legal authorization is inferred.

Next required inputs are specifically the readable original ST circuit/package drawings and original artwork, not approval to manufacture. Once traced and independently checked, review the narrowly scoped coupon layout proposal. No integratedPCB layout,Gerber generation,component purchasing,manufacture,assembly,RF operation or production firmware occurred. Stop for review with the source/package blockers explicit.
''')
# Pinout/source/measurement trace is machine-readable and can never be mistaken for hardware passes.
sources=[
 dict(id='ST_BOARD',url='https://www.st.com/en/evaluation-tools/steval-tdr003v1.html',status='PRIMARY_TEXT_RETRIEVED',revision='NRND page, historical reference',scope='Original complete board claims, not derivative'),
 dict(id='ST_DS',url='https://www.st.com.cn/resource/en/datasheet/steval-tdr003v1.pdf',status='TEXT_TABLES_ONLY_IMAGES_NOT_INSPECTED',revision='DocID17343Rev1 31Mar2010',scope='Figures12-20 OPEN'),
 dict(id='ST_SCHEMATIC',url='https://www.st.com/resource/en/schematic_pack/steval-tdr003v1_schematic.pdf',status='BINARY_UNAVAILABLE_RASTER_NOT_INSPECTED',scope='HTTP2/403/timeouts; approved retries also failed'),
 dict(id='ST_BOM',url='https://www.st.com/resource/en/bill_of_materials/steval-tdr003v1_bom.pdf',status='TEXT_RETRIEVED',scope='PD54003L code conflict; not a netlist'),
 dict(id='ST_GERBER',url='https://www.st.com/resource/en/board_manufacturing_specification/steval-tdr003v1_gerber.zip',status='LINK_FOUND_BINARY_NOT_RETRIEVED',scope='No original Gerber geometry inspected or copied'),
 dict(id='PD54008_DS',url='https://www.st.com/resource/en/datasheet/pd54008l-e.pdf',status='TEXT_RETRIEVED_PIN_IMAGE_OPEN',revision='Jan2007Rev2',scope='No numeric PowerFLAT map fabricated'),
 dict(id='PHA1',url='https://www.minicircuits.com/pdfs/PHA-1%2B.pdf',status='PRIMARY_SEARCHABLE_TEXT_DIRECT_BINARY403',scope='5Vcurrent/P1dB tables;144MHz compression and landing OPEN'),
 dict(id='TLV761',url='https://www.ti.com/lit/ds/symlink/tlv761.pdf',status='PRIMARY_TEXT_RETRIEVED',revision='SBVS349DMay2025',scope='DCYpin1GND2OUT/tab3IN,voltage/capacitance/ESR/reverse-current/thermal data'),
 dict(id='IARU',url='https://www.iaru-r1.org/wp-content/uploads/2025/01/ARDF-Rules_B_2025.pdf',status='PRIMARY_TEXT_RETRIEVED',scope='T2.8 event requirements, not legal authorization')]
(O/'sources.json').write_text(json.dumps(dict(date='2026-10-15',sources=sources,third_party_license='Original documents linked/attributed; no relicensing or unread artwork claimed.'),indent=2)+'\n')
gates=['physical_package_mapping','RF_matching_and_stability','driver_compression','RF_AM_depth_and_THD','carrier_and_PEP','hot_pass_SOA','thermal_attachment_and_trip','driver_OV_Q304_20us','startup_reset_timing','offslot_silence','training_output_isolation','antenna_ERP','battery_endurance']
(O/'physical-gates.json').write_text(json.dumps({k:dict(status='NOT_RUN',evidence=None)for k in gates},indent=2)+'\n')
# These are proposals; original ADRs remain byte-for-byte untouched.
(D/'decisions/ADR-0013-vhf-low-voltage-evaluation-candidate.md').write_text('''# ADR-0013 — low-voltage VHF evaluation candidate

Status: **Proposed — blocked on source/package trace; not accepted.**
Date:2026-10-15.

Proposed implementation amendment to ADR0007's VHF candidate and still-proposed ADR0008/0011 details: investigate PD54008L-E/PHA-1+ with fixed5V driver LDO and10Vfull/7.5Vreduced upstream rails, preserving genuine final-drain AM, isolated training output, controller interface and autonomous fail-off. Existing architecture and all accepted requirements remain.

Rationale: quantity-ten component allowance52.33/50.40EURnet for2S/4S versus74.61/72.77R0. Stocked cut-tape final and economical MMIC provide most of the conditional saving; no obsolete PD84001. Neither gain nor clean70–80%RF AM is established. Original matching drawings/PowerFLAT land remain blocking OPEN.

No final-device substitution is accepted for production. Preserve R0 at tagm5a-r0 as fallback. Close the reference trace/pin map, then review a small externally driven coupon layout; measure gain/compression,crest,RF envelope,stability,spectrum and hot SOA before committing the integrated PCB. Reject the cheap chain if those gates fail rather than weakening carrierERP/PEP requirements.

See [review decision](../M5A_R1_REVIEW_DECISION.md), [cost delta](../M5A_R1_COST_DELTA.md), [reference audit](../M5A_R1_ST_REFERENCE_AUDIT.md). No procurement,manufacturing or RF authorization follows from this proposal.
''')
# Review landing page and reproducibility; the frozen R0 docs are historical, not overwritten.
(O/'README.md').write_text('''# RF2M M5A-R1 — review candidate, NOT RELEASED

See [engineering decision](../../../../docs/M5A_R1_REVIEW_DECISION.md). **NO-GO for coupon layout while ST reference topology/physical final landing are OPEN.** Actual KiCad ERC0errors/3OPEN-footprint warnings; digital regression4096combinations/36scenarios/13mutations. These are not physical passes.

Native project stays inhardware/2m; R0 native/archive and review files remain preserved at tagm5a-r0. Root schematic is authoritative; OPEN matching values and footprints intentionally prevent manufacture. PDF/netlist/ERC/BOM/pin audit/cost/analysis files are generated from R1. No PCB/Gerbers exist.

Reproduce from repository root:

```sh
python3 tools/m5a_r1_design.py
kicad-cli sch erc --format json --output hardware/2m/review/M5A-R1/erc.json hardware/2m/RF2M.kicad_sch
kicad-cli sch export netlist --format kicadxml --output hardware/2m/review/M5A-R1/RF2M.net.xml hardware/2m/RF2M.kicad_sch
kicad-cli sch export pdf --output hardware/2m/review/M5A-R1/RF2M.pdf hardware/2m/RF2M.kicad_sch
python3 tools/m5a_r1_verify.py
python3 tools/m5a_r1_costs.py
python3 tools/m5a_r1_baskets.py
python3 tools/m5a_r1_analysis.py
python3 tools/m5a_r1_documents.py
python3 tools/m5a_r1_finish.py
```

Use KiCad10.0.6/Python3.12.3. No ngspice result is claimed for R1; analytical models are explicit assumptions. Preserve third-party source rights; sources.json distinguishes unread diagrams from retrieved text. All physical-gates.json entries are NOT_RUN.
''')
print('WROTE eight requested R1 review documents, proposedADR0013, sources/gates/change ledgers')

# Refresh concise numeric statements from the same generated ledgers as the tables.
prices={x['variant']:x['component_allowance_net_eur']for x in c['summary']if x['fleet']==10}
strong={x['basket']:x['net_eur']for x in b['summary']if x['fleet']==10}
replacements={
 '€52.33':f"€{prices['BOOST2S']:.2f}",'€50.40':f"€{prices['BUCK4S']:.2f}",
 '€22.27':f"€{74.60743858865546-prices['BOOST2S']:.2f}",'29.9%':f"{100*(1-prices['BOOST2S']/74.60743858865546):.1f}%",
 '€65.13':f"€{strong['R1_2S_PHA13_strong']:.2f}",'€63.20':f"€{strong['R1_4S_PHA13_strong']:.2f}",
 '€119.01–146.01':f"€{prices['BOOST2S']+66.68:.2f}–{prices['BOOST2S']+93.68:.2f}",
 '€43.50':f"€{next(x for x in c['summary']if x['fleet']==10 and x['variant']=='BOOST2S')['remaining_estimates_net_eur']:.2f}",
 '37preferred':'36preferred','37OPEN':'36OPEN','37 preferred':'36 preferred',
 '13detected mutations':'14detected mutations','13mutations':'14mutations',
 '33critical':'34critical','There are33':'There are34','1.53A':'1.55A','8.6W':'8.7W',
}
for pack,erp,oldtext in [('2S3P',1,'17.6hfull'),('2S3P',.3,'30.9hreduced'),('4S1P',1,'12.5/21.6h')]:
 x=next(x for x in a['endurance']if x['pack']==pack and x['cell']=='M35A_min'and x['erp']==erp and x['m']==.8)
 if '/'in oldtext:
  y=next(x for x in a['endurance']if x['pack']==pack and x['cell']=='M35A_min'and x['erp']==.3 and x['m']==.8)
  replacements[oldtext]=f"{x['modeled_hours']:.1f}/{y['modeled_hours']:.1f}h"
 else:replacements[oldtext]=f"{x['modeled_hours']:.1f}h"+('full'if erp==1 else'reduced')
for path in list(D.glob('M5A_R1_*.md'))+[D/'decisions/ADR-0013-vhf-low-voltage-evaluation-candidate.md',O/'README.md']:
 text=path.read_text()
 for before,after in replacements.items():text=text.replace(before,after)
 path.write_text(text)
# Apply readable SI spacing without changing file paths, URLs, MPNs or code blocks.
import re
for path in [D/('M5A_R1_'+n+'.md')for n in ['ST_REFERENCE_AUDIT','RF_SELECTION','AM_FEASIBILITY','POWER_THERMAL','COST_DELTA','SCHEMATIC_REVIEW','PA_TEST_PLAN','REVIEW_DECISION']]+[D/'decisions/ADR-0013-vhf-low-voltage-evaluation-candidate.md']:
    text=path.read_text()
    for before,after in {
        'at10':'at 10','at1':'at 1','at6':'at 6','at20':'at 20',
        'At10':'At 10','at144':'at 144','at500':'at 500','of4':'of 4',
        'originalST':'original ST','the2010':'the 2010','The2010':'The 2010',
        'the66':'the 66','the73':'the 73','the5':'the 5','the7':'the 7',
        'requires19':'requires 19','requires22':'requires 22','gives17':'gives 17',
        'with10':'with 10','with0':'with 0','with1':'with 1','with3':'with 3',
        'at0':'at 0','approximately1':'approximately 1','approximately2':'approximately 2',
        'approximately3':'approximately 3','approximately5':'approximately 5',
        'approximately6':'approximately 6','approximately7':'approximately 7',
        'approximately8':'approximately 8','approximately€':'approximately €',
        'roughly€':'roughly €','of the€':'of the €','€43.50of':'€43.50 of',
        'full2S':'full 2S','full4S':'full 4S','exclusive2S':'exclusive 2S',
        'a20':'a 20','A20':'A 20','0errors':'0 errors','3warnings':'3 warnings',
        '3documented':'3 documented','33critical':'33 critical','13detected':'13 detected',
        '36state':'36 state','4096digital':'4096 digital','104fitted':'104 fitted',
        '37preferred':'37 preferred','335frozen':'335 frozen','Controller20':'Controller 20',
        'source/filter':'source/filter','Current2S':'Current 2S','Both1':'Both 1',
        'tag`':'tag `','tagm5a':'tag m5a','full2':'full 2','upstream10':'upstream 10',
        'R0existing':'R0 existing','R0-style0.60':'R0-style 0.60','R0PD':'R0 PD',
        'firmware0':'firmware 0','Rev1,31':'Rev 1, 31','at1/10':'at 1/10',
        'counterfactualPD':'counterfactual PD','stronger-driverPD':'stronger-driver PD',
        'normal full-system':'normal full-system','remaining0.9':'remaining 0.9',
        'and20':'and 20','and70':'and 70','and80':'and 80','and10':'and 10',
        'both1':'both 1','Both1':'Both 1','only12':'only 12','need2':'need 2',
        '6/10/20fleets':'6/10/20 fleets','bothRF':'both RF','goes0':'goes 0',
        'trueAM':'true AM','TrueAM':'True AM','newR1':'new R1','oldPD':'old PD',
        'newR0':'new R0','ExistingS3':'Existing S3','optionalSilicontra':'optional Silicontra',
        'still-proposedADR':'still-proposed ADR','NoGPIO':'No GPIO','source3':'source 3'
    }.items():text=text.replace(before,after)
    text=re.sub(r'(?<![A-Za-z0-9_])(\d+(?:\.\d+)?)(MHz|kHz|GHz|µF|µW|µm|mΩ|kΩ|°C|ppm|dBm|dBc|dBd|dB|mA|nH|pF|mm|Wh|WPM|V|W|A|h|Ω)\b',r'\1 \2',text)
    text=re.sub(r',(?=[A-Za-z])',', ',text)
    # Common word/number transitions only; never edit identifiers or filenames.
    text=re.sub(r'\b(assumed|at|near|about|within|than|above|below|to|from|and|is|gives|set|part|of|only|per|first|all|needs|need|R0|R1)(?=\d)',r'\1 ',text)
    text=re.sub(r'(?<=\d)(units|stock|errors|warnings|combinations|scenarios|mutations|digital|state|detected|physical|fitted|entries|component|preferred|full|reduced|pin|part|normal|test|documented|frozen|gate|profile|beat|input|output|rail|counterfactual|cutoff|power|reel|boards|data|cold|hot|minimum|maximum|typical)\b',r' \1',text)
    path.write_text(text)
# Final prose formatting protects links, identifiers in code spans and URLs.
for path in list(D.glob('M5A_R1_*.md'))+[D/'decisions/ADR-0013-vhf-low-voltage-evaluation-candidate.md',O/'README.md']:
    text=path.read_text().replace('Other and converter compensation as candidates.', 'Keep converter compensation and other input parts as candidates.').replace('exact fuse remains OPEN.', 'fuse sourcing and fault coordination remain OPEN.')
    fragments=re.split(r'(`[^`]*`|\]\([^)]*\)|https?://[^\s)>]+)',text)
    for i,fragment in enumerate(fragments):
        if fragment.startswith(('`','](','http://','https://')):continue
        fragment=re.sub(r'\b([Aa]|At)(?=\d)',r'\1 ',fragment)
        fragment=re.sub(r'\b([A-Z]?[a-z]{2,})(?=\d)',r'\1 ',fragment)
        fragment=re.sub(r'(?<![A-Za-z0-9_])(\d+(?:\.\d+)?)(MHz|kHz|GHz|µF|µH|µs|µW|µm|mΩ|kΩ|°C|ppm|dBm|dBc|dBd|dB|mA|nH|pF|mm|Wh|WPM|V|W|A|h|Ω)(?=[a-z])',r'\1 \2 ',fragment)
        fragment=re.sub(r'(?<![A-Za-z0-9_])(\d+(?:\.\d+)?)(MHz|kHz|GHz|µF|µH|µs|µW|µm|mΩ|kΩ|°C|ppm|dBm|dBc|dBd|dB|mA|nH|pF|mm|Wh|WPM|V|W|A|h|Ω)\b',r'\1 \2',fragment)
        fragment=re.sub(r'(?<![A-Za-z0-9_])(\d+(?:\.\d+)?)([a-z][A-Za-z]{2,})\b',r'\1 \2',fragment)
        fragment=re.sub(r'\b([24]S(?:[1-4]P)?)([a-z]{2,})\b',r'\1 \2',fragment)
        fragment=re.sub(r'([a-z]{2,})([A-Z]{2,})\b',r'\1 \2',fragment)
        fragment=re.sub(r';(?=\S)','; ',fragment)
        fragment=re.sub(r',(?=[€A-Za-z])',', ',fragment)
        fragment=re.sub(r'(?<=[A-Za-z])(?=€)',' ',fragment)
        fragment=re.sub(r'\|(?=\d+[A-Z])','| ',fragment)
        for before,after in {'KiCad10':'KiCad 10','PA4':'PA 4','2Sboost':'2S boost','4Sbuck':'4S buck','or4S':'or 4S','Futurecontroller':'Future controller','primary2mPCB':'primary 2 m PCB','secondMCU':'second MCU','controller20':'controller 20','80m/':'80 m/','34critical':'34 critical','36preferred':'36 preferred','36OPEN2S':'36 OPEN 2S','1ERP':'1 ERP','0.30ERP':'0.30 ERP','0.9ERP':'0.9 ERP','carrierERP':'carrier ERP','Wcarrier':'W carrier','%AM':'% AM','A2A70':'A2A 70','antenna2':'antenna 2','Appendix1T2.8':'Appendix 1 T2.8','2025rulebook':'2025 rulebook','PHYSICAL PARTIAL':'PHYSICAL PARTIAL','0.45|':'0.45 |'}.items():fragment=fragment.replace(before,after)
        fragment=re.sub(r'(€\d+(?:\.\d+)?)(?=[A-Za-z(])',r'\1 ',fragment)
        fragment=fragment.replace('preferred2S','preferred 2S').replace('2 mPCB','2 m PCB').replace('m.8','m=0.8')
        for ref,part in np.items():
            value=part['value']
            fragment=re.sub(r'\b'+re.escape(ref)+re.escape(value)+r'\b',ref+' = '+value,fragment)
        fragments[i]=fragment
    path.write_text(''.join(fragments))
# Extra source/analysis detail belongs in the matching audit, not an invented artwork clone.
path=D/'M5A_R1_ST_REFERENCE_AUDIT.md'
with path.open('a')as f:
 f.write('\n## Calculated substrate sensitivity\n\nZero-thickness, unmasked microstrip approximation, not a qualified fabrication stack-up. The original70µm copper correction is intentionally not hidden in these numbers. Supplier dielectric and actual launch/via geometry remain required.\n\n'+table(['Height mm','Assumedεr','Z at0.92mm Ω','Approximate50Ω width mm','Phase deg/mm at144.7MHz'],[[x['h_mm'],x['er'],f"{x['z_at_0p92mm']:.1f}",f"{x['width50_mm']:.3f}",f"{x['phase_deg_per_mm']:.3f}"]for x in a['microstrip']]))
path=D/'M5A_R1_POWER_THERMAL.md'
with path.open('a')as f:
 f.write('\nBoth75% and80% AM rows are retained. Their mean DC input is identical in this affine-current model because the sine current averages to the same Icenter; RF sideband power and pass/PA heat redistribute. This is a consequence of the assumed model, not evidence that the real amplifier draws equal current at both depths. No full-power efficiency or battery curve is measured.\n')
path=D/'M5A_R1_PA_TEST_PLAN.md'
with path.open('a')as f:
 f.write('\nThermal instruments must have insulated junctions or appropriate isolation: D45H11 and BD139 exposed collectors are different live nets. Never infer PA junction temperature from plastic-top temperature using a source-land RθJC without the actual package heat-flow definition. Use de-embedded couplers at50Ω ports; an ordinary10pF probe can substantially change144MHz matching. A separateDC-coupled modulation amplifier/supply must provide the proposed0–8V envelope at≥2A with sufficient audio bandwidth (initially≥20kHz) and bounded current; an ordinary bench supply is not assumed to follow800Hz. Use insulated thermocouple junctions/isolated logging on live tabs.\n')
src=read('sources.json');src['sources'].append(dict(id='FUSE466',url='https://www.littelfuse.com/assetdocs/fuse-466-datasheet?assetguid=dbe9bcd7-6072-4adf-bf5b-d33e52a6b90f',revision='GD21Jun2023',status='PRIMARY_TEXT_RETRIEVED',scope='4A32V50Ainterrupt1206 candidate; stock/quote/land and actual battery interruption coordination OPEN'))
(O/'sources.json').write_text(json.dumps(src,indent=2)+'\n')

# Preserve the emission designator when article/number spacing is applied.
for path in list(D.glob('M5A_R1_*.md'))+[D/'decisions/ADR-0013-vhf-low-voltage-evaluation-candidate.md']:
 text=path.read_text().replace('A 2A','A2A').replace('A2A70','A2A 70').replace('Appendix 1T2.8','Appendix 1 T2.8')
 path.write_text(text)
