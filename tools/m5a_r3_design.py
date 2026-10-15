#!/usr/bin/python3
"""DL3BBX-derived review schematic. Does not create PCB files or orders.

R1 is generated ONLY in a temporary directory to reuse its tested interface,
training and fail-off circuits. Historical R1 exports are never regenerated.
"""
import copy
import hashlib
import json
import tempfile
from pathlib import Path
import m5a_r1_design as b

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'hardware/2m'
OUT = DEST / 'review/M5A-R3'
ARTICLE = 'https://www.robkalmeijer.nl/techniek/electronica/radiotechniek/hambladen/cq-dl/1992/page289/index.html'

def preserved():
    paths = [ROOT/'README.md']
    for folder in ['hardware/80m', 'hardware/2m/archive', 'docs/decisions']:
        paths += list((ROOT/folder).rglob('*'))
    for revision in ['M5A-R0', 'M5A-R1', 'M5A-R2']:
        paths += list((DEST/'review'/revision).rglob('*'))
    paths += list((ROOT/'docs').glob('M5_2M*')) + list((ROOT/'docs').glob('M5A_R1*')) + list((ROOT/'docs').glob('M5A_R2*'))
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in sorted(set(paths)) if p.is_file() and p.suffix not in ['.pyc','.kicad_prl']}

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    freeze = OUT/'preserved-baseline.json'
    if not freeze.exists():freeze.write_text(json.dumps(preserved(),indent=2)+'\n')
    assert json.loads(freeze.read_text()) == preserved(), 'Unrelated/historical files changed'
    with tempfile.TemporaryDirectory(prefix='ardf-r3-') as tmp:
        b.DEST=Path(tmp)
        d=b.build()
    b.DEST=DEST
    d.revision='M5A-R3'
    old_parts=copy.deepcopy(d.parts)
    old_placements=[(s,pl) for s in d.sheets for pl in s.placements]
    keep = {p['ref'] for p in d.parts.values() if not p['sheet'].startswith(('04_', '05_', '06_', '09_'))}
    keep |= {'U302','L302','C401','C402','C403','C404','R401','R402','R414','Q307','R403','R404','R405','C405','C406'}
    keep |= {'U401','U402','R501','R502','R503','R504','C501','C502','C503','C504','R514','R515','C507','C508'}
    keep -= {'R815','R816','R817','R818'} # no MMIC supply exists in R3
    keep -= {'TP401','TP501','TP502','TP503','TP601','TP602','TP603','TP604'}
    d.parts={r:p for r,p in d.parts.items() if r in keep}
    def change(r,**kw):d.parts[r].update(kw)
    def value(r,v,mpn=None):
        change(r,value=v,mpn=mpn or 'OPEN: '+v+' 1% package as shown')
    # Two upstream settings; independent RF calibration remains mandatory.
    value('R301','171k','RC0603FR-07171KL')
    value('R303','34k','RC0603FR-0734KL')
    value('R401','787k','RC0603FR-07787KL')
    value('R414','332k','RC0603FR-07332KL')
    change('R301',note='Buck reduced10.7876V nominal. Full PROFILE_Q shunts34k into feedback bottom ->13.7851V. 4S full requires adequate battery headroom; controller must refuse SLOT on low rail.')
    change('R401',note='Boost reduced10.90123V nominal. PROFILE_Q332k shunt ->13.8145V. No assumption that RF power scales linearly with rail.')
    change('U304',pins={**d.parts['U304']['pins'],'5':'NORMAL_PERMIT'},note='R3: physical5/6->3 RAIL_RUN requires NORMAL_PERMIT and HARD_OK_N. Physical1/2->7 PACK_RUN still CONV_EN and PACK_OK_N. Source blanking plus drain isolation addresses original self-oscillation warning.')
    change('U203',pins={**d.parts['U203']['pins'],'13':'NORMAL_RC'},note='Last Schmitt inverter receives RC-delayed normal permission: delayed RF-clock start, diode-accelerated withdrawal. Other five gates unchanged. RC timing is not hardware-qualified.')
    change('C306',value='1u',mpn='CC0805KKX7R9BB105',footprint='Capacitor_SMD:C_0805_2012Metric',price_breaks_eur={'1':.08},note='R3 switched-rail local1uF; original470uF bulk is upstream of isolation/sense. Effective DC-bias capacitance and inrush require measurement.')
    change('U103',note='R3: PLL_A=6*desired RF; MS0=12 -> RF/2 for retained DL3BBX T3 doubler. MS2=6 -> RF for training. CLK1 disabled. Source purity and doubler drive NOT_MEASURED.')
    change('R101',value='15k',mpn='RC0603FR-0715KL',variant_values={'BUCK4S':'33.2k','TRAIN_ONLY':'75k'},note='R3 distinct passive ID:15k2S,33.2k4S,75ktraining. Do not arm using old R1ID/calibration; R3 normal clock is half the RF. Controller ADC windows/tolerances remain to qualify.')
    value('R811','160k','RC0603FR-07160KL');value('R813','18.2k','RC0603FR-0718K2L')
    value('R819','160k','RC0603FR-07160KL');value('R821','18.2k','RC0603FR-0718K2L')
    value('R828','1.5k','RC0603FR-071K5L');value('R829','10k','RC0603FR-0710KL')
    change('R828',note='R3 total normal-rail current trip approximately0.593A using loaded reference. Conservative original500-600mA adjustment ceiling, not proof of attainable target PEP.')
    change('R309',note='0.1ohm high-side normal-rail sense. Approx0.6A trip. Exact resistor MPN/Kelvin landing and fault latency remain OPEN.')
    change('F301',note='Wiring/secondary protection only; 4A fuse does not protect the RF final at0.6A. INA180/comparator trip is separate. Exact battery prospective fault coordination OPEN.')
    change('U803',note='R3: approximately0.593A current trip; original ~66C NTC window unchanged. Sensor coupling, lag, DC SOA and thermal rise remain unmeasured.')
    change('U802',note='R3 unused former MMIC-OV comparator tied to valid common-mode references; regulator-OV nominal15.04V. No extra MMIC regulator/supervisor fitted.')
    d.parts['U802']['pins'].update({'9':'VREF1V0','8':'GND'})
    # Quad amplifier retains the reconstruction and training servo only.
    d.parts['U401']['pins'].update({'8':'UNUSED_OP_OUT','9':'UNUSED_OP_OUT','10':'GND'})
    change('U401',note='A/B unity Sallen-Key PWM reconstruction; C unused follower at ground; D training emitter-current servo. NO high-power supply feedback op-amp in R3.')
    # Rebuild retained sheets; no obsolete RF/matching or driver page survives.
    d.sheets=[]
    sheets={}
    for old,pl in old_placements:
        r=pl['ref']
        if r not in d.parts:continue
        name=old.name
        if name.startswith('04_'):name='04_boost'
        if name.startswith('05_'):name='05_pwm_training_command'
        if name not in sheets:
            title={'04_boost':'04 2S boost,10.9/13.8V candidate','05_pwm_training_command':'05 Sine reconstruction and training command'}.get(name,old.title)
            sheets[name]=d.sheet(name,title)
            sheets[name].text('R3: no RF/analog/thermal hardware validation. Original RF attribution and open procurement in M5A_R3 documents.',18,25,1.05)
        s=sheets[name];p=d.parts[r];unit=pl['unit']
        nums={x[0] for x in d.lib.pins(pl['type'],unit)}
        pins={n:p['pins'][n] for n in nums}
        # Regenerated parts use original component data, with approved changes above.
        i=len(s.placements)
        x,y=(62+(i%5)*112,65+(i//5)*57) if name=='05_pwm_training_command' else (pl['x'],pl['y'])
        s.place(r,pl['type'],p['value'],pins,x,y,p['footprint'],p['mpn'],p['group'],p['population'],unit=unit,note=p['note'],source=p['source_url'],price=p['price_breaks_eur'],evidence=p['evidence'],supplier=p['supplier'],code=p['supplier_part_number'],availability=p['availability'],moq=p['moq'])
        p['sheet']=name
    # Custom physical pin maps: manufacturer-specific, never generic device names.
    d.lib.native('Device:Q_NPN','2N4427_CENTRAL',{'B':'2','C':'3','E':'1'})
    d.lib.native('Device:Q_NPN','MRF237_ASI',{'B':'2','C':'3','E':'1'})
    d.lib.native('Device:Q_PNP','TIP127_ST',{'B':'1','C':'2','E':'3'})
    d.lib.box('BF981_PHILIPS',{'1':('SOURCE','passive'),'2':('DRAIN','passive'),'3':('GATE2','input'),'4':('GATE1','input')},left=['3','4'])
    d.lib.native('Device:C_Variable','C_Trim')
    def new_sheet(name,title,note):
        s=d.sheet(name,title);s.text(note,18,24,1.05);return s
    s=new_sheet('06_dl3_rf','06 DL3BBX retained72MHz doubler, driver, final and output network','PRIVATE CONSTRUCTION REFERENCE: Siegfried Pomplun DL3BBX,CQ-DL5/1992pp289-292, Fig2/Fig3/Fig4.\nT3/T4/T5 retained. Source coupling is modified; no renewed RF performance claimed. Red-core Neosid range discrepancy and exact RF semiconductor procurement OPEN.')
    n=[0]
    def part(ref,typ,val,pins,fp,mpn,group='reference_rf',cost=.03,pop='NORMAL',source=ARTICLE,note='',price=None,evidence='ESTIMATE',supplier='OPEN',code='OPEN',availability='Exact stocked manufacturer/lot/quantity not verified',moq=1,xy=None,angle=0):
        i=n[0];n[0]+=1;x,y=xy or (60+(i%5)*110,65+(i//5)*57)
        s.place(ref,typ,val,pins,x,y,fp,mpn,group,pop,angle=angle,note=note,source=source,price=price or {'1':cost},evidence=evidence,supplier=supplier,code=code,availability=availability,moq=moq)
    def r(ref,val,a,c,note='',xy=None):
        code=val[:-1].replace('.','K') if val.endswith('k') else val.replace('.','R') if '.' in val else val+'R'
        if val.endswith('k') and '.'not in val:code+='K'
        part(ref,'R',val,{'1':a,'2':c},b.FP_R,'RC0603FR-07'+code+'L',note=note,xy=xy)
    def c(ref,val,a,costnet,xy=None):
        part(ref,'C',val,{'1':a,'2':costnet},b.FP_C,'OPEN: '+val+' C0G50V 0603',cost=.10,xy=xy)
    def coil(ref,mpn,a,z,label):
        part(ref,'L',label,{'1':a,'2':z},'',mpn,cost=3.00,note='Original '+ref.replace('L9','L')+' Neosid7.1E. No generic chip substitute. Manufacturer bottom-view A/E geometry and can clearance require local footprint and exact purchased part confirmation.',source='https://neosid.de/import-data/product-pdf/neoFilterspulen_5_7_10.pdf')
    # Source filter is calculated90MHz50ohm, followed by retained original C11/L4/C13.
    part('U901','LVC125','SN74LVC1G125DBVR',{'1':'NORMAL_OFF','2':'CLK_NORMAL','3':'GND','4':'CLK72_BUF','5':'V3V3'},'Package_TO_SOT_SMD:SOT-23-5','SN74LVC1G125DBVR','source_filter',cost=.12,source=b.TI+'sn74lvc1g125.pdf',note='Physical active-low OE, disabled independent of clock register state. 72MHz drive/purity require acceptance measurement.')
    r('R900','47','CLK72_BUF','CLK72_LIMIT')
    c('C900','1n','CLK72_LIMIT','LP72_IN')
    for ref,val,a,z in [('L900','110n','LP72_IN','LP72_A'),('L901','180n','LP72_A','LP72_B'),('L902','110n','LP72_B','LP72_OUT')]:
        part(ref,'L',val,{'1':a,'2':z},'Inductor_SMD:L_0805_2012Metric','OPEN: VHF high-Q '+val,'source_filter',cost=.82,source='',note='Calculated seven-pole90MHz Butterworth50ohm. Exact MPN/Q/SRF and terminated insertion loss OPEN.')
    for ref,val,node in [('C901','16p','LP72_IN'),('C902','68p','LP72_A'),('C903','68p','LP72_B'),('C904','16p','LP72_OUT')]:c(ref,val,node,'GND')
    r('R901','51.1','LP72_OUT','GND')
    s=new_sheet('06b_dl3_doubler_driver','06b Retained DL3BBX T3 doubler and T4 driver','Original C11/L4/C13 input tank; T3 BF981 drain47ohm isolation; original L5/C15/T4/L6/C19.\nR13 is100ohm, not33k. C14/C17 are feed decouplers to ground, not resonant capacitors across tuning coils.');n[0]=0
    c('C911','1.2p','LP72_OUT','T3_G1') # original C11 retained as coupling
    coil('L904','00511732','T3_G1','GND','170n original L4 green')
    c('C913','18p','T3_G1','GND')
    part('Q901','BF981_PHILIPS','BF981 Philips',{'1':'T3_S','2':'T3_D','3':'T3_G2','4':'T3_G1'},'','BF981','reference_rf',cost=3.00,source='https://datasheet.octopart.com/BF981-NXP-Semiconductors-datasheet-180991380.pdf',evidence='OBSERVED_NET_PACK5_MANUFACTURER_LISTED',supplier='Dönberg',code='BF981 / pack5',moq=5,note='Original T3, Philips SOT103 Dec1990. Physical1S2D3G2 4G1. NOS; supplier lists PHILIPS. Five-piece lot, fleet stock/reserve OPEN.')
    r('R909','33k','T3_G2','GND');r('R910','33k','VMOD','T3_G2');c('C912','1n','T3_G2','GND')
    r('R911','47','TP5_ORIGINAL','T3_D');r('R912','100','T3_S','GND');c('C916','1n','T3_S','GND')
    r('R914','100','VMOD','T3_FEED');c('C914','1n','T3_FEED','GND')
    coil('L905','00511830','T3_FEED','TP5_ORIGINAL','51n original L5 red; catalog55-70n')
    c('C915','15p','TP5_ORIGINAL','T4_B');r('R913','100','T4_B','GND')
    part('Q902','2N4427_CENTRAL','2N4427 Central',{'1':'T4_E','2':'T4_B','3':'T4_C'},'','2N4427','reference_rf',cost=5.90,source='https://my.centralsemi.com/datasheets/2n4427.PDF',evidence='OBSERVED_NET_MANUFACTURER_UNRESOLVED',supplier='Dönberg',code='2N 4427',note='Original T4. Central datasheet1E2B3C but supplier manufacturer unspecified. Central PDN01114 2019EOL. Raise body>=10mm per article; heat sink if required. No manufacturer interchangeability approved.')
    r('R915','47','T4_E','GND');c('C918','1n','T4_E','GND')
    part('L909','L','10u original DR2',{'1':'VMOD','2':'T4_FEED'},'','OPEN: RF choke10uH >=0.3A',cost=.40,note='Original DR2 allows6.8-10uH. Actual self-resonance/lead geometry/stock OPEN; not tuning coil.')
    c('C917','1n','T4_FEED','GND');coil('L906','00511631','T4_FEED','T4_C','34n original L6 yellow')
    part('C919','C_Trim','25p original C19',{'1':'T4_C','2':'T5_B'},'','OPEN: C0G/air RF trimmer25p',cost=.90,note='Original interstage coupling trimmer. Exact capacitance range, Q, footprint and genuine supplier OPEN.')
    r('R916','100','T5_B','GND')
    s=new_sheet('06c_dl3_final','06c Retained DL3BBX MRF237 final and output matching/filter','T5 and original collector chokes,C21,L7,C23x||C23,L8,C24 retained electrically. No invented50ohm transistor match.\nASI evaluation symbol is manufacturer-specific; exact final supplier/manufacturer and physical footprint remain blockers.');n[0]=0
    part('Q903','MRF237_ASI','MRF237 ASI candidate',{'1':'GND','2':'T5_B','3':'T5_C'},'','MRF237 ASI','reference_rf',cost=31.90,source='https://pdf.dzsc.com/F23/MRF237.pdf',evidence='OBSERVED_NET_MANUFACTURER_UNRESOLVED',supplier='Dönberg price comparator ONLY',code='MRF 237 (manufacturer unspecified)',note='ASI RevA 1E2B3C. NOT assumed identical to Motorola case79-03 STYLE5. EUR31.90 is an unbranded listing comparator, not an ASI quote. No qualified physical footprint. Final procurement/manufacturer/layout blocker.')
    part('L910','L','4.7u original DR3',{'1':'T5_FEED','2':'T5_C'},'','OPEN: RF choke4.7uH >=0.8A',cost=.40,note='Original2.2-6.8uH range; exact SRF/current/geometry OPEN.')
    part('L911','L','VK200 original DR4',{'1':'VPA','2':'T5_FEED'},'','OPEN: VK200 current manufacturer',cost=.50,note='Original six-hole ferrite choke, not a generic4.7uH replacement. Exact construction/source OPEN.')
    c('C920','1n','VPA','GND');c('C922','1n','T5_FEED','GND');c('C921','33p','T5_C','OUT_MID')
    coil('L907','00511830','OUT_MID','OUT_TRIM','51n original L7 red; catalog55-70n')
    c('C923','39p','OUT_TRIM','GND')
    part('C924','C_Trim','45p original C23',{'1':'OUT_TRIM','2':'GND'},'','OPEN: RF trimmer45p',cost=.90,note='In parallel with39p C23x. Article adjustment text calls C20 a trimmer once, but schematic/BOM identify C23. Never replace1n C20 with a trimmer.')
    coil('L908','00511631','OUT_TRIM','NORMAL_RF','34n original L8 yellow');c('C925','33p','NORMAL_RF','GND')
    part('C926','C','5.6p optional original correction',{'1':'T4_B','2':'GND'},b.FP_C,'OPEN:5.6p C0G50V',cost=.10,pop='OPTIONAL',note='Documented DL3BBX off-state oscillation correction, normally DNP; fit only under recorded alignment/quiet acceptance.')
    part('J501','Conn_Coaxial','NORMAL50ohm SMA',{'1':'NORMAL_RF','2':'GND'},'Connector_Coaxial:SMA_Amphenol_132134_Vertical','132134','connector',cost=1.10,note='Preserved normal port. Exact incoming drawing/board-fit qualification OPEN.')
    s=new_sheet('10_original_modulator','10 Original Darlington collector-supply AM, PWM sine input','Original T8/R24-26/VR1/VR2/C26/C27 mechanism retained; ST TIP127 replaces obsolete BD676 with documented different package/pins.\nNo new RF final, premium MMIC or high-power op-amp servo. Profile setting changes converter rail, not live RF path. RF75% AM remains NOT_MEASURED.');n[0]=0
    part('Q904','TIP127_ST','TIP127 ST',{'1':'PASS_BASE','2':'VPA','3':'VMOD'},'Package_TO_SOT_THT:TO-220-3_Vertical','TIP127','modulator',cost=.75,source='https://www.st.com/resource/en/datasheet/tip127.pdf',note='ST DS0854 Rev5May2021:1B2C/tab3E. Tab at modulatedVPA, electrically isolate sink. Hot DC SOA/sensor contact not qualified. Original BD676 pin1E2C3B is NOT drop-in.')
    r('R926','10k','VMOD','PASS_BASE')
    part('RV902','R_Potentiometer','100k original VR2',{'1':'PASS_BASE','2':'PASS_BASE','3':'VPA'},'Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical','3296W-1-104LF','modulator',cost=.42,note='Wiper2 tied to base-side end1. Before power measure approximately100k PASS_BASE-to-VPA (wiper at1) for minimum conduction. A zero-ohm setting INCREASES conduction. Trim is not an RF-off interlock. Original8V center is not automatically valid for80% sine; calibrate actual RF envelope.')
    part('RV901','R_Potentiometer','47k original VR1',{'1':'AM_COMMAND','2':'AF_ATTEN','3':'GND'},'Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical','3296W-1-473LF','modulator',cost=.42,note='Minimum audio at wiper ground. Controller scales AF sine separately by profile; no-tone command same DC offset, C26 blocks steadyDC.')
    r('R924','2.2k','AF_ATTEN','AF_RC');c('C927','100n','AF_RC','GND');r('R925','2.2k','AF_RC','AF_COUPLE')
    part('C928','C','330n film original C26',{'1':'AF_COUPLE','2':'PASS_BASE'},'','OPEN:330nF film>=50V','modulator',cost=.20,note='Original MKH330nF; film preserves intended characteristics. Exact package/MPN OPEN.')
    part('C929','C_Polarized','470u25V original C25',{'1':'VREG_RAW','2':'GND'},'','OPEN:470u25V radial','modulator',cost=.35,note='Original upstream470uF reservoir placed BEFORE slot isolation/sense. Not across modulatedVPA or switchedVMOD. Effective ESR and converter response OPEN.')
    part('C930','C','1u gate slew',{'1':'REG_GATE','2':'VREG_RAW'},'Capacitor_SMD:C_0805_2012Metric','CC0805KKX7R9BB105','supply_isolation',cost=.08,note='Added isolation-FET slew control. SimpleRC estimates do NOT bound Miller plateau/inrush. Measure startup and turn-off before RF. Gate pullup4.7k gives several-ms withdrawal, source blanking is faster.')
    part('R930','R','10k',{'1':'NORMAL_PERMIT','2':'NORMAL_RC'},b.FP_R,'RC0603FR-0710KL','interlock',cost=.02,pop='NORMAL',note='WithC931 nominal1ms RF source startup delay, Schmitt U203 pin13/12. Physical timing and race gate OPEN.')
    part('C931','C','100n',{'1':'NORMAL_RC','2':'GND'},b.FP_C,'CC0603KRX7R8BB104','interlock',cost=.045,note='Source startup delay only; not an independent watchdog.')
    part('D901','D','BAT54WS-7-F',{'1':'NORMAL_FAST_OFF','2':'NORMAL_RC'},'Diode_SMD:D_SOD-323','BAT54WS-7-F','interlock',cost=.05,note='Cathode1 toward permission through330ohm; anode2 atRC. Accelerates source inhibit on falling permission without overloading HC output.')
    part('R931','R','330',{'1':'NORMAL_FAST_OFF','2':'NORMAL_PERMIT'},b.FP_R,'RC0603FR-07330RL','interlock',cost=.02,note='Bounds initial capacitor discharge toapproximately10mA; propagation/brownout behavior unmeasured.')
    part('R932','R','100k',{'1':'NORMAL_RC','2':'GND'},b.FP_R,'RC0603FR-07100KL','interlock',cost=.02,pop='ALL',note='Required even in training-only population: no floating unused Schmitt input when normal RC/diode parts are omitted.')
    r('R927','1k','VPA','GND',note='R3 added discharge/load, rated>=0.5W1206 rather than0603.')
    d.parts['R927'].update(footprint='Resistor_SMD:R_1206_3216Metric',mpn='OPEN:1k 1% >=0.5W 1206',price_breaks_eur={'1':.06},group='modulator')
    s=new_sheet('11_external_contract','11 External supply declarations and qualification boundary','No PCB is released: exact final manufacturer/lot, some magnetic/choke/trimmer geometry and RF source coupling remain OPEN.\nNo physical measurements exist. See M5A_R3_REVIEW_DECISION.md. PWR_FLAG is an ERC declaration, not a safety approval.');n[0]=0
    for i,net in enumerate(['GND','V3V3','BAT_RAW','VIN_PROT','VIN_CONV','VREG_RAW','VMOD','VBUCK','VBOOST'],950):
        part('#FLG'+str(i),'PWR_FLAG','PWR_FLAG',{'1':net},'','NOT_PURCHASED','declaration',cost=0,pop='ALL',source='')
    # Consistent fields after the initial placement data were reused.
    d.parts['Q901']['multiple']=5
    for r in ['R900','R901','L900','L901','L902','C900','C901','C902','C903','C904']:
        d.parts[r]['group']='source_filter'
        d.parts[r]['source_url']=''
    for r in ['R926','R924','R925','C927']:d.parts[r]['group']='modulator'
    for r in ['R927','C930','R930','C931','D901','R931','R932']:d.parts[r]['source_url']=''
    # C27 is explicitly MKH film in the reference, not an assumed X7R substitute.
    d.parts['C927'].update(mpn='OPEN:100nF MKH film>=50V',footprint='',price_breaks_eur={'1':.15},note='Original C27 is film; keep dielectric/function, exact package and source OPEN.')
    from m5a_r3_readable import reflow
    reflow(d)
    d.save()
    for page in d.sheets:
        path=DEST/(page.name+'.kicad_sch');tree=b.parse(path.read_text())
        for symbol in b.children(tree,'symbol'):
            props={p[1]:p for p in b.children(symbol,'property')};ref=props['Reference'][2]
            props['Function'][2]=d.parts[ref]['group']
        path.write_text(b.dump(tree)+'\n')
    root=DEST/'RF2M.kicad_sch'
    text=root.read_text()
    start=text.index('(text ')
    note='M5A-R3 PRIVATE DL3BBX REFERENCE DERIVATIVE / NOT RELEASED\nOriginal72-to144MHz doubler,2N4427 driver,MRF237 final and matching retained.\nSi5351 CLK0=RF/2; CLK2=RF. No premium MMIC and no speculative LDMOS matching.\nBLOCKING: exact RF transistor procurement/manufacturer and some package/magnetic geometry.\nPublished >3WPEP is not proof of requested5.135WPEP connector capability.\nAll RF/AM/thermal/endurance hardware tests NOT_RUN. No PCB or procurement authorized.\nPrivate construction permission only; commercial derivatives require author written permission.'
    # Root has just one text item, generated by base.Design.save.
    tree=b.parse(text)
    text_item=b.child(tree,'text');text_item[1]=note
    for i,sheet in enumerate(b.children(tree,'sheet')):
        at=b.child(sheet,'at');old_y=float(at[2]);new_y=65+(i//3)*55;at[2]=b.Atom(str(new_y))
        for prop in b.children(sheet,'property'):
            pos=b.child(prop,'at');pos[2]=b.Atom(str(float(pos[2])+new_y-old_y))
    root.write_text(b.dump(tree)+'\n')
    # Remove stale inactive R1 sheet files only after archiving; no historical exports touched.
    active={p.name+'.kicad_sch' for p in d.sheets}|{'RF2M.kicad_sch'}
    for path in DEST.glob('*.kicad_sch'):
        if path.name not in active:path.unlink()
    return d

if __name__=='__main__':
    d=build();print('R3 schematic generated:',len(d.parts),'positions,',len(d.sheets),'pages; no PCB generated')
