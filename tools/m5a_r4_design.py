#!/usr/bin/python3
"""One R4 electrical candidate; historical generators run only in a temp tree.

Manufacturer RF topology is transcribed from ST DocID17343 rev1 figs12-17.
No physical performance is inferred from this generator or ERC.
"""
import copy, hashlib, json, tempfile
from pathlib import Path
import m5a_r1_design as b

ROOT=Path(__file__).resolve().parents[1]
DEST=ROOT/'hardware/2m'; OUT=DEST/'review/M5A-R4'
ST='https://www.st.com/resource/en/datasheet/steval-tdr003v1.pdf'

def frozen():
    paths=[ROOT/'README.md']
    for folder in ['hardware/80m','hardware/2m/archive','docs/decisions']:
        paths.extend((ROOT/folder).rglob('*'))
    for rev in ['M5A-R0','M5A-R1','M5A-R2','M5A-R3']:
        paths.extend((DEST/'review'/rev).rglob('*'))
    for pattern in ['M5_2M*','M5A_R1*','M5A_R2*','M5A_R3*','M4A*']:
        paths.extend((ROOT/'docs').glob(pattern))
    return {str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(set(paths)) if p.is_file() and p.suffix not in ['.pyc','.kicad_prl']}

def build():
    OUT.mkdir(parents=True,exist_ok=True)
    snap=OUT/'preserved-baseline.json'
    if not snap.exists():snap.write_text(json.dumps(frozen(),indent=2)+'\n')
    assert json.loads(snap.read_text())==frozen()
    with tempfile.TemporaryDirectory(prefix='ardf-r4-base-') as tmp:
        b.DEST=Path(tmp); d=b.build()
    b.DEST=DEST; b.DATE='2026-10-16';d.revision='M5A-R4'
    oldparts=copy.deepcopy(d.parts)
    placements=[(s,pl)for s in d.sheets for pl in s.placements]
    keep={r for r,p in d.parts.items() if not p['sheet'].startswith(('06_','09_'))}
    keep|={'C601','L611','L612','L613','C611','C612','C613','C614','R602','R603','R604','C615','U501','L604','C602','C603','C604','Q501','R606','RV501','D501','L606','C607','Q502','J501','TP601','TP602','TP603','TP604','R519'}
    remove={'R414','Q307','Q304','Q308','R408','R409','R410','R411','R412','D308','U205','U206','U209','C209'}
    keep-=remove
    d.parts={r:p for r,p in d.parts.items()if r in keep}
    def change(r,**kw):d.parts[r].update(kw)
    def val(r,v,mpn=None):change(r,value=v,mpn=mpn or 'OPEN: '+v+' exact orderable MPN')
    val('R301','116k','RC0603FR-07116KL')
    val('R303','46.4k','RC0603FR-0746K4L')
    val('R401','634k','RC0603FR-07634KL') #1.229*(1+6.34)=9.02086V
    change('R301',note='R4 4S buck7.5096V reduced;capturedPROFILE_Q shunts46.4k ->8.9996V full. Both remain attainable across protected4S12-16.8V. RF calibration remains independent.')
    change('R401',note='R4 fixed9.02086V nominal, above fully charged2S8.4V. Removes invalid boost-only7.5V reduced setting. Both profiles use calibrated AF/LEVEL PWM.')
    change('U301',price_breaks_eur={'1':1.21,'10':.879,'25':.796},evidence='OBSERVED_2026_10_16_NET',supplier='DigiKey Germany',supplier_part_number='296-46237-1-ND',availability='Indexed6904stock,CT MOQ1;1.21@1/.879@10. Cached listing,not reservation.',source_url='https://www.digikey.de/en/products/detail/texas-instruments/TPS54302DDCR/6572466',note='Exact DDCR available in cut tape; no3000reel MOQ assumed. Replaces carried0.55EUR estimate with actual indexed CT break. TI DDC pin mapping unchanged.')
    change('U302',footprint='ARDF_2M:TI_RNW0013A_4222804C',price_breaks_eur={'1':2.71,'10':2.031,'25':1.86},evidence='OBSERVED_2026_10_16_NET',supplier='DigiKey France EUR net',supplier_part_number='296-48313-1-ND',availability='Indexed4371stock,CT MOQ1;2.71@1/2.031@10. RNW13 terminal land from TI4222804/C11/2019.',source_url='https://www.digikey.fr/en/products/detail/texas-instruments/TPS611781RNWR/7056156',note='TI SLVSDA7E p3 top view, package drawing4222804/C11/2019 visually inspected. Separate center bars6PGND7SW8VOUT, no fictitious common grounded EP. Candidate local copper/mask/paste geometry checked; board integration/assembly qualification OPEN.')
    change('U304',note='1/2->7 PACK_RUN=CONV_EN&PACK_OK_N;5/6->3 RAIL_RUN=CONV_EN&HARD_OK_N. Precharge driver BEFORE ARM; slot shutdown is pass-command clamp+helper clamp+gate-bias clamp+driver switch+clock mute. Faults independently disconnect9V. No heavy reservoir charging each slot.')
    change('C306',value='100n',mpn='CC0603KRX7R8BB104',footprint=b.FP_C,price_breaks_eur={'1':.045},note='Protected9V local bypass; converter bulk upstream, driver reservoirs after8.2ohm. Startup/loop stability NOT_RUN.')
    change('U203',pins={**d.parts['U203']['pins'],'13':'NORMAL_RC'},note='R4 final inverter: RC delayed clock startup, diode accelerated inhibit. Hardware analog timing NOT_RUN.')
    change('U204',pins={**d.parts['U204']['pins'],'9':'PREPARE','10':'SAFE_N','11':'MUTE_N','8':'SRC_ON'},note='Three triple AND gates: valid ARM context, direct shared inhibit, source permission. Scheduling remains in controller.')
    change('R101',value='18.2k',mpn='RC0603FR-0718K2L',variant_values={'BUCK4S':'39.2k','TRAIN_ONLY':'82k'},note='R4-only IDs18.2k2S/39.2k4S/82ktrain. Bind calibration/firmware contract; never accept R3 half-frequency setup.')
    change('R517',value='0',mpn='RC0603JR-070RL',pins={'1':'MOD_DRIVE','2':'VPA_FB'},note='TRAIN_ONLY0ohm closes negative feedback around otherwise-unusedU401C; NEVER fit in full assembly. Positive input MOD_COMMAND grounded viaR518. Avoid floating unused quad-opamp inputs.')
    change('U103',note='R4 PLL_A=6*fRF, both MS0 and MS2 divide6; CLK1 disabled. Local Si5351 remains, no crystal multipliers. Real VHF spurs/stability NOT_RUN.')
    change('R606',note='Fixed gate bias from upstream VMOD, not modulated VPA. Start trim grounded;50mA initial Idq, max200mA only after thermal/AM acceptance. Clamp and mute independent.')
    change('L606',value='33n',mpn='1812SMS-33NJLC',footprint='',price_breaks_eur={'1':.80},evidence='ESTIMATE',supplier='Coilcraft authorized channel; quote OPEN',supplier_part_number='OPEN',source_url='https://www.coilcraft.com/en-us/products/rf/air-core-inductors/midi-spring/1812sms/1812sms-33n/',note='ST Fig13 L2 final gate feed33nH retained; participates in input match. Current manufacturer JLC suffix verified, Qmin100@150MHz,SRF2.5GHz,Irms3A rise basis. Manufacturer online selected configuration not purchasable; exact CT quote/landing OPEN.0.80EUR is an estimate,not stock-backed price.')
    change('R309',note='High-side0.1ohm sense; nominal1.80A analog trip retained. Verify AM crest/inrush and actual fault latency; no fuse-as-PA-limiter assumption.')
    # Driver rail decoupling retains the existing explicit conditional fault gate.
    change('U303',note='Fixed5V TI DCY pin1GND2OUT/tab3IN. At9.02V and180mA approx0.724W: <=70C/W board thermal path required. Output-short/LDO-short protection remains a timed qualification gate.')
    change('C409',mpn='25SVPG150M',price_breaks_eur={'1':1.50},supplier='Panasonic via authorized distributor; EUR quote OPEN',supplier_part_number='10-25SVPG150MCT-ND',source_url='https://industrial.panasonic.com/sa/products/pt/os-con/models/25SVPG150M',availability='Manufacturer current catalog and DigiKey CT entry observed;actual stock,EUR price and MOQ confirmation OPEN.500factorypack is not asserted customer MOQ.',note='Panasonic25SVPG150M150uF25V+/-20percent,ESR13mohm@100kHz,4.2Arms@105C,C10 diameter6.3mm height9.9mm. Effective>=120uF andESR<=100mohm over temperature still qualification assumptions. Exact land OPEN.1.50EUR estimated;not observed price. Isolation<=20us remains unmeasured.')
    change('R413',value='8.2',mpn='OPEN:8.2ohm1percent1W2512',footprint='Resistor_SMD:R_2512_6332Metric',price_breaks_eur={'1':.12},evidence='ESTIMATE',note='0.266W at180mA;initial reservoir current<=1.14A at9.2V/8.118ohm. Preserves5V LDO headroom with7.5V4S reduced rail. Exact MPN/derating quote OPEN. Also bounds LDO-short rise during conditional20us shutdown.')
    change('U303',note='Fixed5V TI DCY1GND2OUT/tab3IN. After8.2ohm at180mA input~7.54V full or~6.03V reduced,before switch/sense drops;LDO~0.46W full,feed resistor0.266W. Verify worst dropout/ripple. No converter failure qualification from ERC.')
    for ref,value,mpn in [('R815','75k','RT0603BRD0775KL'),('R816','10k','RT0603BRD0710KL'),('R817','29.4k','RT0603BRD0729K4L'),('R818','10k','RT0603BRD0710KL')]:
        change(ref,value=value,mpn=mpn,price_breaks_eur={'1':.05},evidence='ESTIMATE',note='R4 driver OV divider:0.1percent thin film required, not1percent substitution. Nominal trip5.383V; calculate threshold extremes withreference drift. Shutdown<=20us anddriver<=5.9V still physical gates. Exact stock/quote OPEN.')
    change('R811',note='Raw upstream rail sense; controller confirms settled9V before slot. Independent OV comparator retained for converter faults.')
    change('TP603',pins={'1':'ST_LPF_IN'},value='ST_LPF_IN')
    change('TP604',pins={'1':'MMIC_AC'},value='MMIC_AC')
    change('C602',pins={'1':'MMIC_RF_DC','2':'MMIC_AC'},note='MMIC output DC block; connects to ST interstage derivative, not a verified50ohm final input.')
    change('J501',note='Normal SMA remains physically separate from training MCX. Exact drawing/incoming fit and RF launch qualification required.')
    # Manufacturer defines G/D/S landing regions, not a generic power-MOSFET EP.
    change('Q501',footprint='ARDF_2M:PD54008L_ST_GDS_5x5',price_breaks_eur={'1':7.35,'10':5.30,'100':4.78},supplier='Mouser Europe',supplier_part_number='511-PD54008L-E',availability='2026-10-16 indexed:3430 stock;CT MOQ1/multiple1. Reconfirm at procurement.',evidence='OBSERVED_2026_10_16_NET',note='ST January2007Rev2p1 TOP VIEW: four G contacts left, four D right, center SOURCE. p13 recommends continuous0.5x5mm G/D strips and2.7x5mm SOURCE. Local landing uses manufacturer G,D,S region names, NOT invented numeric pin groups. Thermal via/stencil qualification still OPEN.')
    change('U501',footprint='ARDF_2M:PHA1_DF782_RevG',price_breaks_eur={'1':2.88,'50':2.351},supplier='DigiKey Spain EUR net listing',supplier_part_number='3157-PHA-1+CT-ND',availability='2026-10-16 indexed12794 stock;CT MOQ1. EUR2.88@1; no50 break booked for20.',evidence='OBSERVED_2026_10_16_NET',note='Mini-Circuits PHA-1+ RevD;1IN2GND3OUT/DC4paddleGND. DF782RevG02/08/17 suggested land transcribed in local library; ground stencil/vias/incoming dimensions still require review. 19dBm CW output and3dB compression backoff are qualification targets, not measured.',source_url='https://pccomponents.com/datasheets/MINI_-PHA1.pdf')
    # Low-drive RF inductors: economical RF wirewound, never power inductors.
    for p in d.parts.values():
        if p['ref'].startswith('L') and p['value']in ['56n','91n','180n'] and p['group']not in ['converter']:
            value=p['value']; token={'56n':'56N','91n':'91N','180n':'R18'}[value]
            p.update(mpn='LQW18AN'+token+'G80D',footprint='Inductor_SMD:L_0603_1608Metric',price_breaks_eur={'1':.12,'10':.102,'100':.0839}if value=='56n'else{'1':.16},evidence='OBSERVED_2026_10_16_NET'if value=='56n'else'ESTIMATE',supplier='DigiKey EUR'if value=='56n'else'Murata authorized channel; exact quote OPEN',supplier_part_number='490-18135-1-ND'if value=='56n'else'OPEN',source_url='https://www.digikey.fr/fr/products/detail/murata-electronics/LQW18AN56NG80D/4422179'if value=='56n'else'https://www.mouser.com/datasheet/2/281/1/JELF243A_0102-3158940.pdf',availability='56n observed28315 CT MOQ1;91n/180n exact current stock OPEN',note='Low-power RF path only.56n Q>=38@200MHz SRF2.6GHz Imax770mA;91n Q33 SRF1.9GHz Imax520mA manufacturer family table.180n exact Q/current/SRF must close before layout; do not apply these prices/ratings to high-power LPF.')
    # Rebuild existing supporting circuits with changed physical nets before rendering.
    d.sheets=[];sheets={}
    for old,pl in placements:
        r=pl['ref']
        if r not in d.parts:continue
        name='02_interlocksb1' if r=='R519' else old.name
        if name.startswith('06_'):name='06_source_driver_bias'
        if name=='06_source_driver_bias' and name in sheets and len(sheets[name].placements)>=25:name+='b1'
        if name not in sheets:
            title=('06 Source filter, economical driver and fixed bias'+(' continued'if name.endswith('b1')else''))if name.startswith('06_source_driver_bias')else old.title
            sheets[name]=d.sheet(name,title);sheets[name].text('M5A-R4: hardware measurements NOT_RUN; source/reference and simplification in R4 documents.',18,26,1.1)
        s=sheets[name];p=d.parts[r];u=pl['unit'];nums={x[0]for x in d.lib.pins(pl['type'],u)}
        pins={n:p['pins'][n]for n in nums}
        i=len(s.placements);x,y=(62+(i%5)*112,65+(i//5)*57)if name.startswith('06_source_driver_bias')else(pl['x'],pl['y'])
        if r=='R519':x,y=285.75,293.37
        s.place(r,pl['type'],p['value'],pins,x,y,p['footprint'],p['mpn'],p['group'],p['population'],unit=u,note=p['note'],source=p['source_url'],price=p['price_breaks_eur'],evidence=p['evidence'],supplier=p['supplier'],code=p['supplier_part_number'],availability=p['availability'],moq=p['moq']);p['sheet']=name
    def section(name,title,note):
        nonlocal s
        s=d.sheet(name,title);s.text(note,18,27,1.1)
    def p(ref,typ,value,pins,fp,mpn,group='pa_match',pop='NORMAL',cost=.1,note='',source=ST,unit=1):
        i=len(s.placements)
        s.place(ref,typ,value,pins,62+(i%5)*112,70+(i//5)*58,fp,mpn,group,pop,price={'1':cost},note=note,source=source,unit=unit)
    def r(ref,v,a,z,group='interlock',pop='NORMAL',cost=.02):
        token=v[:-1].replace('.','K')if v.endswith('k')and'.'in v else(v[:-1]+'K'if v.endswith('k')else v.replace('.','R')+'R'if'.'not in v else v.replace('.','R'))
        p(ref,'R',v,{'1':a,'2':z},b.FP_R,'RC0603FR-07'+token+'L',group,pop,cost)
    def c(ref,v,a,z,group='pa_match',cost=.1,pop='NORMAL'):
        code={'330p':'331','56p':'560','27p':'270','33p':'330','100p':'101','39p':'390','3.3p':'3R3','18p':'180','12p':'120','22p':'220','15p':'150'}.get(v)
        mpn='GRM1885C1H'+code+'JA01D'if code and v!='3.3p'else('GRM1885C1H3R3CA01D'if v=='3.3p'else'OPEN: '+v+' rating/MPN')
        p(ref,'C',v,{'1':a,'2':z},b.FP_C,mpn,group,pop,cost,note='ST nominal value; exact suffix/current stock and RF Q/voltage qualification OPEN. C0G50V RF; do not silently order conflicting391-code330pF.')
    def l(ref,v,a,z,mpn,cost=.75,group='pa_match'):
        p(ref,'L',v,{'1':a,'2':z},'Inductor_SMD:L_1008_2520Metric'if group=='output_filter'else'',mpn,group,cost=cost,note='Original ST RF value/function. Exact manufacturer land/current stock OPEN; tune/validate on the ONE integrated transmitter. Not an ordinary power inductor.')
    d.lib.box('ST_TLINE',{'1':('IN','passive'),'2':('OUT','passive')})
    def tl(ref,length,a,z):
        p(ref,'ST_TLINE','50R '+str(length)+'mm',{'1':a,'2':z},'','PCB microstrip feature','transmission_line',cost=0,note='Original ST0.508mm FR4,70umCu,W0.92mm,L'+str(length)+'mm. Reference electrical geometry; not zero-length wire. Recalculate for actual stackup. Not a purchased part.')
        d.parts[ref]['evidence']='BOARD_FEATURE'
    section('06b_st_matching','06b ST final-stage matching derivative','Traced ST DocID17343Rev1 Figs16/17. Interstage originally connects PD84001 drain to final gate.\nPHA-1 substitution CHANGES source impedance: values are documented starting values, NOT a verified50ohm input match.\nOutput network retained. Transmission-line symbols are PCB features and lengths must survive layout.')
    tl('TL603',6.23,'MMIC_AC','ST_IS_A');c('C631','56p','ST_IS_A','GND');c('C632','330p','ST_IS_A','ST_IS_B');tl('TL604',6.62,'ST_IS_B','ST_IS_C');c('C633','27p','ST_IS_C','GND');l('L634','18n','ST_IS_C','ST_IS_D','0603HC-18NXJLU',.24);tl('TL605',5.8,'ST_IS_D','PA_GATE')
    # No original PD84001 drain supply at ST_IS_A; the MMIC DC is blocked at C602.
    l('L635','33n','VPA','PA_DRAIN','1812SMS-33NJ',.80)
    change('L635',mpn='1812SMS-33NJLC',supplier='Coilcraft authorized channel; exact CT quote OPEN',supplier_part_number='OPEN',availability='Current manufacturer part exists;selected online configuration not directly purchasable. No available-stock claim.',source_url='https://www.coilcraft.com/en-us/products/rf/air-core-inductors/midi-spring/1812sms/1812sms-33n/')
    d.parts['L635']['note']='Final drain feed only: ST L3 nominal35.5nH conflicts with1812SMS-22NJ code.33nH is EXPLICIT nearby engineering starting substitution, not silently resolved BOM. RF isolation/stability to qualify; do not substitute output matching L5.'
    c('C634','330p','VPA','GND');c('C635','1u','VMOD','GND',group='modulator',cost=.08)
    tl('TL606',2.2,'PA_DRAIN','ST_O_A');c('C636','33p','ST_O_A','GND');tl('TL607',11,'ST_O_A','ST_O_B');c('C637','100p','ST_O_B','GND');l('L638','18.5n','ST_O_B','ST_O_C','A05T',.55);c('C638','39p','ST_O_C','GND');tl('TL608',12.4,'ST_O_C','ST_O_D');c('C639','330p','ST_O_D','ST_DC_BLOCK');tl('TL609',2,'ST_DC_BLOCK','ST_LPF_IN')
    change('L638',mpn='A05TJLC',price_breaks_eur={'1':1.51,'10':1.28,'25':1.18},evidence='OBSERVED_2026_10_16_NET',supplier='Mouser Europe',supplier_part_number='994-A05TJLC',availability='Indexed331 stock Austria/110EU;CT MOQ1;1.51@1,1.28@10,1.18@25. Not reserved.',source_url='https://eu.mouser.com/ProductDetail/Coilcraft/A05TJLC?qs=zCSbvcPd3pYJqqPlmZ4EHA%3D%3D',note='Original ST A05T nominal18.5nH. Coilcraft confirms5turns,Qmin132@150MHz,SRF2.5GHz,Irms4A. Factory air-core part, not an invented DIY winding. Exact manufacturer mounting dimensions/landing must be transcribed before layout; distributor dimension fields conflict in axis ordering.')
    section('06c_st_lpf','06c Original ST elliptic harmonic LPF','ST Fig14: three series parallel-resonant L||C branches, four shunt capacitors.\nThis is NOT the previous9poleButterworth filter. Stock/derating and whole-system emissions NOT_RUN.')
    nodes=['ST_LPF_IN','ST_F1','ST_F2','NORMAL_RF']
    for i,(a,z,lv,cv)in enumerate(zip(nodes,nodes[1:],['39n','22n','27n'],['3.3p','18p','12p']),1):
        l('L64'+str(i),lv,a,z,'1008CS-'+{'39n':'390','22n':'220','27n':'270'}[lv]+'XJLC',.75,'output_filter');c('C64'+str(i),cv,a,z,'output_filter')
    for i,(a,cv)in enumerate(zip(nodes,['22p','27p','22p','15p']),4):c('C64'+str(i),cv,a,'GND','output_filter')
    section('10_enable_detail','10 Local physical switches and clock sequencing','One integrated transmitter, no separate coupon.9V fixed converter, separate filtered5V driver.\nTPS22919 replaces discrete driver-switch network. Source gate delays only turn-on; fail-off uses direct inhibit and rail isolation.\nRC timings, analog trip latency and real RF silence remain physical acceptance gates.')
    d.lib.native('74xx:74LS21','74HC21')
    for prop in b.children(d.lib.defs['74HC21'],'property'):
        if prop[1]=='ki_fp_filters':prop[2]='SOIC*3.9x8.7mm*'
    p('U205','74HC21','74HC21D,653',{'1':'VALID_ARM','2':'ARM_DELAY','4':'SLOT','5':'ARM','6':'TX_OK'},b.FP_SO14,'74HC21D,653','interlock','ALL',.26,unit=1,source='https://assets.nexperia.com/documents/data-sheet/74HC21.pdf',note='Nexperia Rev10 17Jan2024: physical1,2,4,5->6 four-input AND. Replaces cascaded redundant two-input permissions.')
    p('U205','74HC21','74HC21D,653',{'9':'CLEAR_A','10':'RUN_HEALTH','12':'V3V3','13':'V3V3','8':'CLR_N'},b.FP_SO14,'74HC21D,653','interlock','ALL',.26,unit=2)
    p('U205','74HC21','74HC21D,653',{'7':'GND','14':'V3V3'},b.FP_SO14,'74HC21D,653','interlock','ALL',.26,unit=3)
    for unit,pins in [(1,{'1':'TX_OK','2':'NORMAL_Q','13':'CLEAR_A','12':'NORMAL_PERMIT'}),(2,{'3':'TX_OK','4':'PATH_Q','5':'CLEAR_A','6':'TRAIN_PERMIT'}),(3,{'9':'PA_PREPARE','10':'SRC_ON','11':'V3V3','8':'CONV_EN'}),(4,{'7':'GND','14':'V3V3'})]:
        p('U206','74HC11','74HC11D,653',pins,b.FP_SO14,'74HC11D,653','interlock','ALL',.28,unit=unit,source='https://assets.nexperia.com/documents/data-sheet/74HC_HCT11.pdf',note='Final permissions retain direct CLEAR_A; analog faults clear latch and independently cut RAIL_RUN. Real propagation/reset races remain OPEN.')
    p('U305','TPS22919','TPS22919DCKR',{'1':'VDRV_FILTER','2':'GND','3':'NORMAL_PERMIT','4':None,'5':'VDRV_RF','6':'VDRV_RF'},'Package_TO_SOT_SMD:SOT-363_SC-70-6','TPS22919DCKR','driver_supply',cost=.25,source=b.TI+'tps22919.pdf',note='TI physical1VIN2GND3ON4NC5QOD6VOUT.5V switch only, never9V/rawpack.6V absolute; LDO-short rail qualification still required.')
    p('C940','C','100n',{'1':'VDRV_FILTER','2':'GND'},b.FP_C,'CC0603KRX7R8BB104','driver_supply',cost=.045)
    r('R940','100k','NORMAL_PERMIT','GND','driver_supply')
    r('R930','10k','NORMAL_PERMIT','NORMAL_RC');p('C931','C','100n',{'1':'NORMAL_RC','2':'GND'},b.FP_C,'CC0603KRX7R8BB104','interlock',cost=.045)
    r('R932','100k','NORMAL_RC','GND',pop='ALL')
    p('D930','D','BAT54WS',{'1':'NORMAL_FAST_OFF','2':'NORMAL_RC'},'Diode_SMD:D_SOD-323','BAT54WS-7-F','interlock',cost=.05,note='Cathode1 through330R to permission; anode2 RC. Fast discharge; no false inversion.')
    r('R931','330','NORMAL_FAST_OFF','NORMAL_PERMIT')
    p('U601','LVC125','SN74LVC1G125DBVR',{'1':'NORMAL_OFF','2':'CLK_NORMAL','3':'GND','4':'NORMAL_CLOCK_BUF','5':'V3V3'},'Package_TO_SOT_SMD:SOT-23-5','SN74LVC1G125DBVR','source_filter',cost=.12,source=b.TI+'sn74lvc1g125.pdf')
    p('C941','C','100n',{'1':'V3V3','2':'GND'},b.FP_C,'CC0603KRX7R8BB104','source_filter',cost=.045)
    p('TP940','TestPoint','Captured profile',{'1':'PROFILE_Q'},'TestPoint:TestPoint_Pad_D1.0mm','PCB feature','test','ALL',0)
    # R1 direct clock input is now connected only through the hardware mute buffer.
    d.parts['C601']['pins']['1']='NORMAL_CLOCK_BUF'
    # Redraw that changed symbol/wire before save (manifest-only edits are forbidden).
    for sheet in d.sheets:
        if any(pl['ref']=='C601'for pl in sheet.placements):
            for i,item in enumerate(sheet.items):
                if item.startswith('(global_label '+b.q('CLK_NORMAL')):
                    # This page has no other CLK_NORMAL label except C601.
                    sheet.items[i]=item.replace('(global_label '+b.q('CLK_NORMAL'),'(global_label '+b.q('NORMAL_CLOCK_BUF'),1)
    section('11_external_contract','11 External supplies and integrated commissioning','R4 MPN/landing blockers are explicit. No PCB manufacturing release. All physical RF/AM/thermal tests NOT_RUN.\nThe measured antenna gain sets ERP calibration;1dB reserve is optional engineering headroom, NOT an IARU rule.\nController: R4 IDs,144MHz direct clocks,2S fixed9V /4S9Vfull7.5Vreduced;AF/DC calibrated separately; keep20pin pinout.')
    for i,n in enumerate(['GND','V3V3','BAT_RAW','VIN_PROT','VIN_CONV','VREG_RAW','VMOD','VBUCK','VBOOST','VDRV_LDO_IN'],950):p('#FLG'+str(i),'PWR_FLAG','PWR_FLAG',{'1':n},'','NOT_PURCHASED','declaration','ALL',0)
    # p13 manufacturer-recommended footprint: continuous functional landing regions.
    fp=DEST/'ARDF_2M.pretty';fp.mkdir(exist_ok=True)
    from m5a_r4_footprints import write as write_manufacturer_landings
    write_manufacturer_landings(fp)
    (fp/'PD54008L_ST_GDS_5x5.kicad_mod').write_text('''(footprint "PD54008L_ST_GDS_5x5" (version 20241229)(generator "pcbnew")
 (layer "F.Cu")(descr "ST PD54008L-E Rev2 p1 TOP VIEW, p13 continuous G/D0.5x5 and SOURCE2.7x5; stencil/vias OPEN")
 (attr smd)(fp_rect(start -2.5 -2.5)(end 2.5 2.5)(stroke(width 0.1)(type default))(layer "F.Fab"))
 (fp_circle(center -2.9 -2.3)(end -2.75 -2.3)(stroke(width 0.1)(type default))(fill none)(layer "F.SilkS"))
 (fp_rect(start -2.9 -2.9)(end 2.9 2.9)(stroke(width 0.05)(type default))(layer "F.CrtYd"))
 (pad "G" smd rect(at -2.25 0)(size 0.5 5)(layers "F.Cu" "F.Paste" "F.Mask"))
 (pad "D" smd rect(at 2.25 0)(size 0.5 5)(layers "F.Cu" "F.Paste" "F.Mask"))
 (pad "S" smd rect(at 0 0)(size 2.7 5)(layers "F.Cu" "F.Mask"))
 (fp_text reference "REF**"(at 0 -3.5)(layer "F.SilkS")(effects(font(size 1 1)(thickness .15))))
 (fp_text value "PD54008L-E"(at 0 3.5)(layer "F.Fab")(effects(font(size 1 1)(thickness .15)))))
''')
    (DEST/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "ARDF_2M") (type "KiCad") (uri "${KIPRJMOD}/ARDF_2M.pretty") (options "") (descr "ST manufacturer functional landing regions; review only")))\n')
    # No source archive, old review export or RF80 file is changed.
    from m5a_r4_readable import reflow
    reflow(d)
    d.save()
    path=DEST/'RF2M.kicad_sch';root=b.parse(path.read_text())
    for i,sheet in enumerate(b.children(root,'sheet')):
        at=b.child(sheet,'at');oldy=float(at[2]);newy=65+(i//3)*45;at[2]=b.Atom(str(newy))
        for prop in b.children(sheet,'property'):
            pa=b.child(prop,'at');pa[2]=b.Atom(str(float(pa[2])+newy-oldy))
    for item in b.children(root,'text'):
        item[1]='M5A-R4 / ONE INTEGRATED TRUE-AM CANDIDATE / NOT RELEASED\nST PD54008L-E output network and elliptic LPF traced; PHA-1 interstage adaptation unqualified.\n2S BOOST9Vfixed OR4S BUCK9Vfull/7.5Vreduced;exclusive populations. Training3.3V only.\nNo obsolete multiplier chain or adjustable RF coils. Full RF/AM/thermal acceptance NOT_RUN.\nOPEN reservoir/coil/connector definitions and changed interstage match; NO MANUFACTURING.\nDF782 and TI RNW manufacturer-derived candidate lands checked; thermal/stencil review OPEN.\nSee docs/M5A_R4_REVIEW_DECISION.md.'
    path.write_text(b.dump(root)+'\n')
    # Remove only stale active sheets, already preserved at m5a-r3 and m5a-r1.
    names={s.name+'.kicad_sch'for s in d.sheets}|{'RF2M.kicad_sch'}
    for path in DEST.glob('*.kicad_sch'):
        if path.name not in names:path.unlink()
    assert frozen()==json.loads(snap.read_text())
    return d

if __name__=='__main__':
    d=build();print('Generated R4',len(d.parts),'positions,',len(d.sheets),'sheets. Hardware NOT_RUN.')
