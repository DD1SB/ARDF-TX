#!/usr/bin/python3
"""M5B actual exported-netlist, physical-pad, population and mutation regression.
Does not model analog/RF performance or assert hardware qualification.
"""
import copy,json,math,xml.etree.ElementTree as ET
from pathlib import Path
import m5a_r4_verify as r4
from m5b_design import HW,OUT,preserved

def configure():
    r4.DEST=HW;r4.OUT=OUT;r4.frozen=preserved
    r4.REF['L634']=('47n','ST_IS_C','ST_IS_D')
    r4.REF['C631']=('22p','ST_IS_A','GND')
    r4.REF['C633']=('22p','ST_IS_C','GND')
    r4.PIN_UPDATES['U305']=('TI TPS22810 SLVSDH0C DBV physicalpin table1VIN2GND3ON4CT5QOD6OUT',{'1':'VDRV_FILTER','2':'GND','3':'NORMAL_PERMIT','4':None,'5':'VDRV_RF','6':'VDRV_RF'},'MANUFACTURER_PIN_ASSERTION')
    r4.PIN_UPDATES['U303']=('TI TLV761 SBVS349D May2025 DCY1GND2OUT/TAB3IN',{'1':'GND','2':'VDRV_FILTER','3':'VDRV_PREREG'},'MANUFACTURER_PIN_ASSERTION_OUTPUT_TAB_LIVE_5V')
    r4.PIN_UPDATES['U950']=('TI TLV767 SLVSE84D July2021 DRV Figure5-1/table5-1',{'1':'VDRV_PREREG','2':'DRV_PRE_FB','3':'GND','4':'CONV_EN','5':'GND','6':'VDRV_LDO_IN','7':'GND'},'MANUFACTURER_PIN_ASSERTION_GROUND_EP')
    r4.PIN_UPDATES['J301']=('JST VH top-entry B2P-VH(LF)(SN);drawingeVH,mating harness pin1identified',{'1':'BAT_RAW','2':'GND'},'KEYED_CONNECTOR_ASSEMBLY_CONSTRAINT')
    r4.PIN_UPDATES['J701']=('Wurth66012102111404 Rev001.00013Mar2019 drawing',{'1':'TRAIN_RF','2':'GND'},'MANUFACTURER_PIN_ASSERTION_SHELL_GROUND')
    r4.PIN_UPDATES['U501']=('Mini-Circuits PHA-1+ DF782 RevG 02/08/17; original manufacturer RF1 ground2 RF/DC3 flange4',{'1':'DRIVER_IN','2':'GND','3':'MMIC_RF_DC','4':'GND'},'MANUFACTURER_PIN_AND_GEOMETRY_ASSERTION')
    for ref in ['U201','U301','U302','Q309','Q302','Q305','F301']:
        src,pins,status=r4.old.AUDIT[ref]
        r4.PIN_UPDATES[ref]=(src,pins,'MANUFACTURER_PIN_ASSERTION_WITH_NATIVE_PAD_PARITY;ASSEMBLY_AND_THERMAL_NOT_RUN')
    r4.PIN_UPDATES['Q502']=('Nexperia2N7002,215 SOT23 physical1G2S3D;gate-bias clamp',{'1':'NORMAL_OFF','2':'GND','3':'BIAS_WIPER'},'MANUFACTURER_PIN_ASSERTION')
    r4.PIN_UPDATES['J501']=('Amphenol132134 exact customer drawing;center1,shell contacts2',{'1':'NORMAL_RF','2':'GND'},'MANUFACTURER_CONNECTOR_MAP')
    r4.PIN_UPDATES['J302']=('SamtecTSW-103-07-G-S 2.54mm1/2/3 inline;factory-exclusive shunt',{'1':'VBOOST','2':'VREG_RAW','3':'VBUCK'},'MANUFACTURER_CONNECTOR_MAP_AND_ASSEMBLY_RULE')
    r4.PIN_UPDATES['J101']=('Wurth61202021621 drawing002.001;20pin numbering/component-side pin1,RF2M interface contract',{'1':'V3V3','2':'GND','3':'I2C_SDA','4':'I2C_SCL','5':'ARM','6':'SLOT','7':'KEY','8':'PROGRESS','9':'MUTE_N','10':'PA_RAIL_ADC','11':'PATH_TRAIN','12':'PROFILE_FULL','13':'AF_PWM','14':'LEVEL_PWM','15':'PREPARE','16':'FAULT_N','17':'GND','18':'GND','19':'MODULE_ID','20':'PA_PREPARE'},'MANUFACTURER_CONNECTOR_MAP_AND_CONTRACT')
    # Preserve all original R4 reference assertions. Normalize only the one
    # expressly changed DC-block node AFTER asserting its actual new topology.
    original=r4.reference
    def reference(parts,nets):
        assert nets['C602']=={'1':'MMIC_RF_DC','2':'MMIC_COUPLED'}
        assert nets['R650']=={'1':'MMIC_COUPLED','2':'MMIC_AC'}
        assert nets['R651']=={'1':'MMIC_COUPLED','2':'GND'}and parts['R651']['population']=='DNP'
        assert nets['R952']=={'1':'VDRV_RF','2':'VDRV_MMIC'}
        assert nets['L604']['1']=='VDRV_MMIC'and nets['C603']['1']=='VDRV_MMIC'
        assert nets['R950']=={'1':'VDRV_PREREG','2':'DRV_PRE_FB'}and parts['R950']['value']=='58.2k'
        assert nets['R951']=={'1':'DRV_PRE_FB','2':'GND'}and parts['R951']['value']=='10k'
        assert parts['U305']['mpn']=='TPS22810DBVR'and parts['U950']['mpn']=='TLV76701DRVR'
        assert parts['R413']['value']=='4.7'and parts['R815']['value']=='73.2k'
        assert parts['R309']['value']=='0.068'and parts['R828']['value']=='5.11k'
        assert parts['L604']['mpn']=='1812SMS-R15JLC'and parts['L604']['value']=='150n'
        assert parts['R602']['value']=='71.5'and parts['R603']['value']==parts['R604']['value']=='96.5'
        assert nets['C960']==nets['C961']=={'1':'VIN_CONV','2':'GND'}
        assert parts['C960']['population']=='BOOST2S'and parts['C961']['population']=='BUCK4S'
        c=copy.deepcopy(nets);c['C602']={'1':'MMIC_RF_DC','2':'MMIC_AC'};original(parts,c)
    r4.reference=reference

def main():
    configure();r4.main();p,n=r4.load();v=json.loads((OUT/'verification.json').read_text());audit=json.loads((OUT/'pinout-audit.json').read_text());mut=[]
    for ref,pin,bad in [('U950','6','VDRV_RF'),('U950','7','VDRV_LDO_IN'),('U303','3','VMOD'),('R952','2','VDRV_FILTER'),('R650','2','NORMAL_RF'),('U305','3','V3V3'),('Q501','S','PA_DRAIN'),('C960','1','BAT_RAW'),('Q502','2','BIAS_WIPER'),('J101','3','I2C_SCL'),('J302','1','VBUCK')]:
        nn=copy.deepcopy(n);nn[ref][pin]=bad
        try:r4.pins(p,nn);r4.reference(p,nn)
        except AssertionError:mut.append(ref+':'+pin)
        else:raise AssertionError('M5B mutation escaped '+ref+':'+pin)
    for ref,badvalue in [('R309','0.1'),('R828','10k'),('L604','180n'),('L634','18n'),('C633','27p'),('C631','56p')]:
        pp=copy.deepcopy(p);pp[ref]['value']=badvalue
        try:r4.reference(pp,n)
        except AssertionError:mut.append(ref+':value')
        else:raise AssertionError('Value mutation escaped '+ref)
    assert preserved()==json.loads((OUT/'preserved-baseline.json').read_text())
    board=HW/'RF2M.kicad_pcb';physical=[]
    if board.exists():
        import pcbnew as pcb
        b=pcb.LoadBoard(str(board));fs={f.GetReference():f for f in b.GetFootprints()};tree=ET.parse(OUT/'RF2M.net.xml');expected={}
        for net in tree.findall('./nets/net'):
            for nd in net.findall('node'):expected.setdefault(nd.get('ref'),{})[nd.get('pin')]=net.get('name')
        for ref,part in p.items():
            if ref.startswith('#'):continue
            f=fs[ref];got={}
            for pa in f.Pads():
                if not pa.GetNumber():continue
                if ref=='U205'and pa.GetNumber()in ['3','11']:
                    assert pa.GetNetname()=='';continue
                number=pa.GetNumber();name=pa.GetNetname();got[number]=name
                assert name==expected[ref][number],('PCB/manufacturer net',ref,number,name,expected[ref][number])
            assert set(got)==set(expected[ref]),('physical package pad set',ref)
            assert str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())==part['footprint'],('package identity',ref)
            if ref in (r4.old.AUDIT|r4.PIN_UPDATES):
                physical.append(dict(ref=ref,MPN=part['mpn'],footprint=part['footprint'],pads=got,orientation_deg=f.GetOrientationDegrees(),status='EXPORTED_NETLIST_AND_NATIVE_PCB_MATCH'))
        for ref,point in {'TP601':(108.5,55),'TP602':(115.2,55),'TP603':(145.3,52.206),'TP604':(89.1,55)}.items():
            at=fs[ref].GetPosition();assert math.dist((pcb.ToMM(at.x),pcb.ToMM(at.y)),point)<.001,('Accessible RF probe plane',ref)
        # Verify actual geometry, not merely names. Continuous ST terminal groups
        # are intentionally G/D/S; no fictional discrete numeric pad order.
        f=fs['Q501'];g=f.GetPosition();coords={pa.GetNumber():(round(pcb.ToMM(pa.GetPosition().x-g.x),4),round(pcb.ToMM(pa.GetPosition().y-g.y),4))for pa in f.Pads()}
        assert coords=={'G':(-2.25,0),'D':(2.25,0),'S':(0,0)}
        # RNW center6/7/8 are three DIFFERENT electrically isolated contacts.
        f=fs['U302'];center={pa.GetNumber():pa for pa in f.Pads()if pa.GetNumber()in ['6','7','8']};assert {pa.GetNetname()for pa in center.values()}=={'GND','BOOST_SW','VBOOST'}
        assert all(abs(pcb.ToMM(pa.GetSize().x)-.35)<.001 for pa in center.values())
        # Physical gate/drain swaps must be caught even with an unchanged schematic.
        fp=fs['Q501'];pg=next(pa for pa in fp.Pads()if pa.GetNumber()=='G');saved=pg.GetNet();pg.SetNet(next(pa.GetNet()for pa in fp.Pads()if pa.GetNumber()=='D'))
        try:assert pg.GetNetname()==expected['Q501']['G']
        except AssertionError:mut.append('PCB_Q501_gate_to_drain')
        else:raise AssertionError('PCB mutation escaped')
        pg.SetNet(saved)
        for ref,part in p.items():
            assert not part['mpn'].startswith('OPEN:'),('unresolved MPN',ref)
            if not ref.startswith('#'):assert part['footprint']
        audit['PCB_physical_devices']=physical;audit['limitations']='Manufacturer pin and landing assertions are CAD checks. Physical soldering, heat transfer, RF, startup/timing and protection tests remain NOT_RUN.'
    v['M5B_additional_mutations']=mut;v['native_PCB_package_checks']=len([r for r in p if not r.startswith('#')]);v['hardware_tests']='NOT_RUN';v['status']='PASS_STATIC_NETLIST_AND_NATIVE_PAD_CHECKS';audit['revision']='M5B-E1'
    (OUT/'verification.json').write_text(json.dumps(v,indent=2)+'\n');(OUT/'pinout-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
    print('M5B PASS:',v['logic']['combinations'],'logic,',len(v['logic']['scenarios']),'states,',len(v['mutation_tests']),'preserved mutations +',len(mut),'new;all native packages/pads checked')
if __name__=='__main__':main()
