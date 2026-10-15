#!/usr/bin/python3
"""Pin-explicit XML netlist/logic tests. No analog startup or RF safety proof."""
import copy,itertools,json,xml.etree.ElementTree as ET
from pathlib import Path
from m5_freeze import check as freeze
R=Path(__file__).resolve().parents[1];D=R/'hardware/2m';O=D/'review/M5A-R0'
def load():
    m=json.loads((D/'RF2M.electrical.json').read_text());parts={p['ref']:p for p in m['parts']};root=ET.parse(O/'RF2M.net.xml');nets={}
    for net in root.findall('./nets/net'):
        for node in net.findall('node'):nets.setdefault(node.attrib['ref'],{})[node.attrib['pin']]=None if net.attrib['name'].startswith('unconnected-') else net.attrib['name']
    for ref,p in parts.items():
        if ref.startswith('#'):continue
        assert nets[ref]==p['pins'],('manifest/netlist parity',ref,nets[ref],p['pins'])
    assert nets['C615']=={'1':'DRIVER_PAD','2':'DRIVER_IN'}
    assert not any(p['ref'].startswith('R')and 'DRIVER_IN'in p['pins'].values()and'GND'in p['pins'].values()for p in parts.values()),'MMIC input DC shunt'
    for p in parts.values():
        if p['mpn'].startswith('CC0805'):assert '0805'in p['footprint'],('package',p['ref'])
        if p['mpn'].startswith('GRM31'):assert '1206'in p['footprint'],('package',p['ref'])
        if p['mpn'].startswith(('GRM32','C3225')):assert '1210'in p['footprint'],('package',p['ref'])
        if p['mpn'].startswith('RC'):
            assert p['mpn'][2:6]in p['footprint'],('resistor package',p['ref'])
    return parts,nets
# These assertions are independently transcribed from named manufacturer pin tables.
AUDIT={
'U101':('TI TPS22919 SLVSEN5B p3',{'1':'V3V3','2':'GND','3':'SRC_ON','4':None,'5':'VCLK','6':'VCLK'},'NUMERIC_VERIFIED'),
'U102':('TI SN74LVC2G66 SCES325N p3',{'1':'I2C_SCL','2':'SCL_CLK','3':'SRC_ON','4':'GND','5':'I2C_SDA','6':'SDA_CLK','7':'SRC_ON','8':'V3V3'},'NUMERIC_VERIFIED'),
'U103':('Skyworks Si5351-B Rev1.3 table20',{'1':'VCLK','2':'XTAL1','3':'XTAL2','4':'SCL_CLK','5':'SDA_CLK','6':'CLK_TRAIN','7':'VCLK','8':'GND','9':None,'10':'CLK_NORMAL'},'NUMERIC_VERIFIED'),
'U201':('TI TPS3431 SNVSB66A table5-1',{'1':'V3V3','2':'CWD','3':'V3V3','4':'GND','5':'V3V3','6':'PROGRESS','7':'SAFE_N','8':'SAFE_N','9':'GND'},'NUMERIC_VERIFIED_PAD_GEOMETRY_OPEN'),
'U202':('Nexperia 74HC174 pin configuration',{'1':'CLR_N','2':'VALID_ARM','3':'ARM_CONTEXT','4':'PATH_TRAIN','5':'PATH_Q','6':'PROFILE_FULL','7':'PROFILE_Q','8':'GND','9':'ARM','10':None,'11':'GND','12':None,'13':'GND','14':'GND','15':None,'16':'V3V3'},'NUMERIC_VERIFIED'),
'U304':('TI SN74LVC2G08 SCES198N DCU',{'1':'CONV_EN','2':'PACK_OK_N','3':'RAIL_RUN','4':'GND','5':'CONV_EN','6':'HARD_OK_N','7':'PACK_RUN','8':'V3V3'},'NUMERIC_VERIFIED'),
'U209':('TI SN74LVC2G08 SCES198 DBV/DCU pin table',{'1':'NORMAL_RAW','2':'CLEAR_A','3':'TRAIN_PERMIT','4':'GND','5':'TRAIN_RAW','6':'CLEAR_A','7':'NORMAL_PERMIT','8':'V3V3'},'NUMERIC_VERIFIED'),
'U208':('TI TLV803E SLVSES2J table6-1 standard DBZ, no V/R pinout suffix',{'1':'GND','2':'SAFE_N','3':'V3V3'},'NUMERIC_VERIFIED'),
'U301':('TI TPS54302 SLVSDG6C table4-1',{'1':'GND','2':'SW4S','3':'VIN_CONV','4':'FB4S','5':'CONV_EN','6':'BOOT4S'},'NUMERIC_VERIFIED_GEOMETRY_OPEN'),
'U302':('TI TPS61178 SLVSDA7E table6 pin functions',{'1':'BOOST_FREQ','2':'GND','3':'BOOST_ILIM','4':'BOOST_COMP','5':'BOOST_FB','6':'GND','7':'BOOST_SW','8':'VBOOST','9':None,'10':'BOOST_VCC','11':'CONV_EN','12':'VIN_CONV','13':'BOOST_BST'},'NUMERIC_VERIFIED_FOOTPRINT_OPEN'),
'U303':('TI TPS54302 SLVSDG6C table4-1',{'1':'GND','2':'DRV_SW','3':'VMOD','4':'DRV_FB','5':'CONV_EN','6':'DRV_BOOT'},'NUMERIC_VERIFIED_GEOMETRY_OPEN'),
'U401':('TI TLV9004 SBOS833R table6-5 SOIC14',{'1':'LEVEL_DC','2':'LEVEL_DC','3':'LEVEL_F2','4':'V3V3','5':'AF_F2','6':'AF_DC','7':'AF_DC','8':'MOD_DRIVE','9':'VPA_FB','10':'MOD_COMMAND','11':'GND','12':'TRAIN_COMMAND','13':'TRAIN_EMITTER_DC','14':'TRAIN_BASE_DRIVE'},'NUMERIC_VERIFIED'),
'U402':('TI SN74LVC1G3157 SCES424O table4-1 DBV',{'1':'AF_DC','2':'GND','3':'LEVEL_DC','4':'AM_COMMAND','5':'V3V3','6':'KEY'},'NUMERIC_VERIFIED'),
'U501':('Mini-Circuits PHA13HLN+ RevOR M159854 p2',{'1':'DRIVER_IN','2':'GND','3':'MMIC_RF_DC','4':'GND'},'NUMERIC_VERIFIED_FOOTPRINT_OPEN'),
'Q501':('ST PD55008-E DocID12259 Rev2 Figure1 functional G/S/D; AN1294 geometry pending',{'G':'PA_GATE','D':'PA_DRAIN','S':'GND'},'FUNCTIONAL_ONLY_NUMERIC_FOOTPRINT_OPEN'),
'Q401':('ST D45H11 DocID4213 Rev5 Figure1 B1 C2/TAB E3',{'1':'PASS_BASE','2':'VPA','3':'VMOD'},'NUMERIC_VERIFIED_TAB_LIVE'),
'Q402':('ST BD139/140 May2008 Rev5 Figure1 B1 C2 E3',{'1':'MOD_BASE','2':'MOD_SINK','3':'MOD_E'},'NUMERIC_VERIFIED_ASSEMBLY_CONSTRAINT'),
'U701':('TI SN74LVC1G125 SCES223U DBV pin functions',{'1':'TRAIN_OFF','2':'CLK_TRAIN','3':'GND','4':'TRAIN_CLOCK_BUF','5':'V3V3'},'NUMERIC_VERIFIED'),
'Q701':('onsemi MMBTH10LT1/D CASE318 STYLE6',{'1':'TRAIN_BASE','2':'TRAIN_EMITTER','3':'TRAIN_COLLECTOR'},'NUMERIC_VERIFIED'),
'U801':('TI TL431 DBZ SLVS543 manufacturer-specific1K2REF3A',{'1':'VREF2V5','2':'VREF2V5','3':'GND'},'NUMERIC_VERIFIED'),
'U804':('TI INA180A1 SBOS741H DBV1OUT2GND3IN+4IN-5VS',{'1':'ISENSE','2':'GND','3':'VREG_SWITCH','4':'VMOD','5':'V3V3'},'NUMERIC_VERIFIED'),
'Q309':('AOS AO3401A SOT23 1G2S3D, reverse blocking body diode D->S',{'1':'REVERSE_GATE','2':'VIN_PROT','3':'BAT_FUSED'},'NUMERIC_MAPPING_ASSEMBLY_OPEN'),
'Q302':('AOS AO3401A SOT23 1G2S3D',{'1':'REG_GATE','2':'VREG_RAW','3':'VREG_SWITCH'},'NUMERIC_MAPPING_ASSEMBLY_OPEN'),
'Q304':('AOS AO3401A SOT23 1G2S3D',{'1':'DRV_GATE','2':'VDRV_FILTER','3':'VDRV_RF'},'NUMERIC_MAPPING_ASSEMBLY_OPEN'),
'Q305':('AOS AO3401A SOT23 1G2S3D',{'1':'INPUT_GATE','2':'VIN_PROT','3':'VIN_CONV'},'NUMERIC_MAPPING_ASSEMBLY_OPEN'),
'D302':('Vishay SMBJ18A cathode stripe, positive clamp',{'1':'VIN_PROT','2':'GND'},'POLARITY_VERIFIED'),
'D304':('Nexperia BZT52H-C10 K1 A2 SOD123F',{'1':'VREG_RAW','2':'REG_GATE'},'POLARITY_VERIFIED'),
}
# Quad comparator functional pins transcribed independently of the CAD library.
AUDIT.update({
'U802':('TI LM339B SOIC14 pin functions',{'1':'PACK_OK_N','2':'PACK_OK_N','3':'V3V3','4':'UV_REF','5':'VBAT_S','6':'VBAT_S','7':'OV_REF','8':'DRV_S','9':'DRV_OV_REF','10':'VREG_S','11':'REG_OV_REF','12':'GND','13':'HARD_OK_N','14':'HARD_OK_N'},'NUMERIC_VERIFIED'),
'U803':('TI LM339B SOIC14 pin functions',{'1':'HARD_OK_N','2':'HARD_OK_N','3':'V3V3','4':'ISENSE_F','5':'VREF1V0','6':'TEMP_LOW','7':'TEMP_S','8':'VPA_S','9':'VPA_OV_REF','10':'TEMP_S','11':'TEMP_HIGH','12':'GND','13':'HARD_OK_N','14':'HARD_OK_N'},'NUMERIC_VERIFIED'),
'Q403':('Nexperia MMBT3904 SOT23 1B2E3C',{'1':'MOD_E','2':'GND','3':'MOD_BASE'},'NUMERIC_VERIFIED'),
'Q308':('Nexperia MMBT3904 SOT23 1B2E3C',{'1':'DRV_ENABLE_BASE','2':'GND','3':'DRV_SINK'},'NUMERIC_VERIFIED'),
'Q307':('Nexperia2N7002 SOT23 1G2S3D',{'1':'PROFILE_Q','2':'GND','3':'BOOST_FB_SWITCH'},'NUMERIC_VERIFIED'),
'Q801':('Nexperia2N7002 SOT23 1G2S3D',{'1':'PROFILE_Q','2':'UV_REF','3':'UV_FULL_SWITCH'},'NUMERIC_VERIFIED'),
'D308':('Nexperia BZT52H source/cathode gate/anode',{'1':'VDRV_FILTER','2':'DRV_GATE'},'POLARITY_VERIFIED'),
})
def audit(nets,parts):
    out=[]
    for ref,(source,expected,status)in AUDIT.items():
        assert nets[ref]==expected,('critical pin mapping',ref,nets[ref],expected)
        out.append(dict(ref=ref,mpn=parts[ref]['mpn'],source=source,pins=expected,status=status,footprint=parts[ref]['footprint']))
    return out
GATE_PINS=[('1','2','3'),('4','5','6'),('9','10','8'),('12','13','11')]
class Logic:
    def __init__(self,nets):self.n=copy.deepcopy(nets);self.q=[0]*6;self.previous_arm=0
    def settle(self,i):
        v={'GND':0,'V3V3':1,**i}
        # U203 Schmitt gates modeled as Boolean after RC threshold crossing only.
        for _ in range(40):
            old=copy.deepcopy(v)
            for pin,state in zip(['2','5','7','10','12','15'],self.q):
                if self.n['U202'][pin]:v[self.n['U202'][pin]]=state
            def assign(net,state):
                if net is not None:v[net]=int(bool(state))
            def val(net):return v.get(net,0)
            n=self.n['U203']
            for a,b in [('1','2'),('3','4'),('5','6'),('9','8'),('11','10'),('13','12')]:assign(n[b],not val(n[a]))
            n=self.n['U204']
            for a,b,c,y in [('1','2','13','12'),('3','4','5','6'),('9','10','11','8')]:assign(n[y],val(n[a])and val(n[b])and val(n[c]))
            for ref,op in [('U205',all),('U206',all),('U207',any)]:
                n=self.n[ref]
                for a,b,y in GATE_PINS:assign(n[y],op([val(n[a]),val(n[b])]))
            n=self.n['U209']
            for a,b,y in [('1','2','7'),('5','6','3')]:assign(n[y],val(n[a])and val(n[b]))
            if old==v:
                if not v.get(self.n['U202']['1'],0) and any(self.q):
                    self.q=[0]*6;return self.settle(i)
                return v
        raise AssertionError('Combinational/asynchronous state did not converge')
    def step(self,**i):
        v=self.settle(i);arm=i.get('ARM',0)
        if arm and not self.previous_arm and v[self.n['U202']['1']]:
            self.q=[v.get(self.n['U202'][p],0)for p in ['3','4','6','11','13','14']]
        self.previous_arm=arm
        return self.settle(i)
BASE=dict(SAFE_N=1,MUTE_N=1,I2C_SCL=1,POWER_FAULT_N=1,KEY=0,SLOT=0,ARM=0,ARM_RC=0,PATH_TRAIN=0,PROFILE_FULL=0,PREPARE=0,PA_PREPARE=0)
def tests(nets):
    combos=0
    # Check settled gate logic for every input/state combination, independent of intended equations.
    ins=['SAFE_N','MUTE_N','I2C_SCL','POWER_FAULT_N','SLOT','ARM','ARM_RC','PREPARE','PA_PREPARE']
    for bits in itertools.product([0,1],repeat=len(ins)):
      for q in itertools.product([0,1],repeat=3):
        m=Logic(nets);m.q=list(q)+[0]*3;i={**BASE,**dict(zip(ins,bits))};v=m.settle(i);combos+=1
        if not i['SAFE_N']:assert not v['SRC_ON']and not v['CONV_EN']
        a,b=v['NORMAL_PERMIT'],v['TRAIN_PERMIT'];assert not(a and b)
        if not(i['SAFE_N']and i['MUTE_N']and i['I2C_SCL']and i['SLOT']and i['ARM']and i['ARM_RC']):assert not(a or b)
        if not i['POWER_FAULT_N']:assert not a
        if a:assert not v['PATH_Q']
        if b:assert v['PATH_Q']
    cases=[]
    def scenario(name,path=0,profile=0,changes=None):
        m=Logic(nets);i={**BASE,'PATH_TRAIN':path,'PROFILE_FULL':profile,'PREPARE':1,'PA_PREPARE':1-path}
        m.step(**i);i['ARM']=1;v=m.step(**i);assert not(v['NORMAL_PERMIT']or v['TRAIN_PERMIT'])
        i['ARM_RC']=1;v=m.step(**i);assert v['VALID_ARM']
        i['SLOT']=1;v=m.step(**i);assert v['TRAIN_PERMIT'if path else'NORMAL_PERMIT']
        if changes:
            i.update(changes);v=m.step(**i)
            if name.startswith('live_'):
                assert v['PATH_Q']==path and v['PROFILE_Q']==profile
            else:
                assert not(v['NORMAL_PERMIT']or v['TRAIN_PERMIT'])
                # Restore health with ARM still high: no rearm.
                i.update({k:BASE[k]for k in changes});i['SLOT']=1;v=m.step(**i);assert not(v['NORMAL_PERMIT']or v['TRAIN_PERMIT'])
                i.update(ARM=0,ARM_RC=0,SLOT=0,KEY=0);m.step(**i)
                i['ARM']=1;m.step(**i);i['ARM_RC']=1;m.step(**i);i['SLOT']=1;v=m.step(**i);assert v['TRAIN_PERMIT'if path else'NORMAL_PERMIT']
        cases.append(name)
    for path in [0,1]:
      for profile in [0,1]:
        scenario(f'arm_path{path}_profile{profile}',path,profile)
        for fault,ch in [('watchdog',{'SAFE_N':0}),('mute',{'MUTE_N':0}),('i2c_stuck_low',{'I2C_SCL':0}),('reset',{'SAFE_N':0})]:scenario(f'{fault}_path{path}_profile{profile}',path,profile,ch)
        scenario(f'live_selection_path{path}_profile{profile}',path,profile,{'PATH_TRAIN':1-path,'PROFILE_FULL':1-profile})
    scenario('normal_analog_fault',0,1,{'POWER_FAULT_N':0})
    for key,slot,config in itertools.product([0,1],repeat=3):
      if not key and not slot and config:continue
      m=Logic(nets);i={**BASE,'KEY':key,'SLOT':slot,'PREPARE':config};m.step(**i);i['ARM']=1;m.step(**i);i['ARM_RC']=1;v=m.step(**i);assert not v['VALID_ARM'];cases.append(f'invalid_arm_key{key}_slot{slot}_config{config}')
    for path in [0,1]:
        m=Logic(nets);i={**BASE,'PATH_TRAIN':path,'PREPARE':1,'PA_PREPARE':1-path};m.step(**i);i['ARM']=1;m.step(**i);i['ARM_RC']=1;m.step(**i);i['SLOT']=1
        for key in [1,0,1,0]:
            i['KEY']=key;v=m.step(**i);assert v['TRAIN_PERMIT'if path else'NORMAL_PERMIT']
        cases.append('keyed_AF_continuous_carrier_path'+str(path))
    m=Logic(nets);i={**BASE,'ARM':1,'ARM_RC':1,'SAFE_N':0};m.step(**i);i['SAFE_N']=1;v=m.step(**i);assert not v['VALID_ARM'];cases.append('reset_release_ARM_held_high')
    m=Logic(nets);i={**BASE,'PREPARE':1,'PATH_TRAIN':1,'POWER_FAULT_N':0};m.step(**i);i['ARM']=1;m.step(**i);i['ARM_RC']=1;m.step(**i);i['SLOT']=1;v=m.step(**i);assert v['TRAIN_PERMIT']and not v['CONV_EN'];cases.append('training_without_raw_PA_power')
    return dict(combinations=combos,scenarios=cases)
def power_checks(parts,nets):
    """Independent final-switch truth tables and conservative DC loading arithmetic.

    No propagation, brownout or transistor turn-off guarantee follows from this.
    """
    checks=0
    for conv,pack,hard in itertools.product([0,1],repeat=3):
        v={'CONV_EN':conv,'PACK_OK_N':pack,'HARD_OK_N':hard}
        n=nets['U304']
        got={n[y]:v[n[a]]and v[n[b]]for a,b,y in [('1','2','7'),('5','6','3')]}
        assert got=={'PACK_RUN':bool(conv and pack),'RAIL_RUN':bool(conv and hard)}
        checks+=1
    assert nets['R312']['1']=='PACK_RUN'and nets['R307']['1']=='RAIL_RUN'
    assert set(nets['R709'].values())=={'V3V3','TRAIN_OFF'}
    assert set(nets['R708'].values())=={'TRAIN_OFF','TRAIN_OFF_BASE'}
    assert parts['R709']['value']=='1k'and parts['R708']['value']=='10k'
    # Pull-up min logic rail and max resistance, clamp resistor min, VBE=0.
    # The zero VBE bound is deliberately more severe than a conducting clamp.
    voh=3.135*(10000*.99)/(1000*1.01+10000*.99)
    assert voh>2.0,('LVC1G125 inhibit VIH',voh)
    assert nets['J101']['10']=='PA_RAIL_ADC'
    assert nets['R805']['1']=='VIN_PROT'
    assert parts['R802']['value']=='620'and parts['R829']['value']=='7.5k'
    # Loaded reference includes NTC/window dividers. Common-mode check is a DC
    # engineering bound, not an analog startup/fault propagation simulation.
    rlow=1/(1/470+1/20000+1/59900+1/11000)
    reference=2.495*rlow/(620+rlow)
    trip_a=reference/(2*7500/(10000+7500))
    assert reference<3.135-2.0 and 1.15<trip_a<1.25
    assert nets['U803']['14']=='HARD_OK_N'and nets['U803']['8']=='VPA_S'
    return dict(switch_truth_rows=checks,training_inhibit_min_calculated_v=voh,
                inhibit_required_vih_v=2.0,loaded_current_reference_v=reference,current_trip_nominal_a=trip_a,scope='Static logic and DC bounds only; turn-off timing NOT_VERIFIED')
def main():
    parts,nets=load();report=audit(nets,parts);logic=tests(nets);power=power_checks(parts,nets);mutations=[]
    for ref,pin,wrong in [('Q401','1','VMOD'),('U101','6','GND'),('U202','1','ARM'),('U501','4','MMIC_RF_DC'),('Q701','2','TRAIN_COLLECTOR'),('U209','2','V3V3')]:
        n=copy.deepcopy(nets);n[ref][pin]=wrong
        try:audit(n,parts)
        except AssertionError:mutations.append(ref+':'+pin)
        else:raise AssertionError('Pin mutation escaped')
    n=copy.deepcopy(nets);n['U205']['10']='PATH_Q'
    try:tests(n)
    except AssertionError:mutations.append('normal_permit_wrong_path')
    else:raise AssertionError('Logic mutation escaped')
    n=copy.deepcopy(nets);n['U304']['2']='HARD_OK_N'
    try:power_checks(parts,n)
    except AssertionError:mutations.append('pack_switch_wrong_fault_bus')
    else:raise AssertionError('Power-switch mutation escaped')
    erc=json.loads((O/'erc.json').read_text())
    violations=[v for s in erc['sheets']for v in s['violations']]
    assert len(violations)==2
    for v in violations:
        assert v['severity']=='warning'and v['type']=='footprint_filter'
        assert any(ref in v['items'][0]['description']for ref in ['J301','J701'])
    assert 'footprint_filter'not in {x['key']for x in erc['ignored_checks']}
    assert not list(D.rglob('*.kicad_pcb'))and not list(D.rglob('*.gbr'))
    (O/'pinout-audit.json').write_text(json.dumps(dict(date='2026-10-15',scope='Schematic only. No PCB or qualified footprint geometry implied.',devices=report),indent=2)+'\n')
    (O/'verification.json').write_text(json.dumps(dict(status='PASS limited digital/netlist checks',manifest_parity_parts=len(parts),erc_errors=0,erc_open_connector_warnings=len(violations),logic=logic,power_switch_checks=power,detected_mutations=mutations,frozen_files=freeze(),physical_tests='NOT_RUN',analog_startup='NOT_VERIFIED'),indent=2)+'\n')
    print('PASS',logic['combinations'],'logic combinations,',len(logic['scenarios']),'state scenarios,',len(mutations),'mutations;',len(report),'pin assertions;',freeze(),'HF/ADR files unchanged')
if __name__=='__main__':main()
