#!/usr/bin/python3
"""R4 actual-netlist Boolean and physical-region checks, not analog/RF proof."""
import copy,itertools,json,shutil,tempfile,xml.etree.ElementTree as ET
from m5a_r4_design import ROOT,DEST,OUT,frozen
import m5a_r1_verify as old
import m5a_r1_design as cad

class Logic(old.Logic):
    def settle(self,i):
        v={'GND':0,'V3V3':1,**i}
        for _ in range(40):
            prev=v.copy()
            # Settled digital endpoint only; explicit NORMAL_RC can model a pending edge.
            # This does not simulate RC thresholds, reset races or propagation delays.
            if 'NORMAL_RC'not in i:v['NORMAL_RC']=v.get('NORMAL_PERMIT',0)
            for pin,state in zip(['2','5','7','10','12','15'],self.q):
                if self.n['U202'][pin]:v[self.n['U202'][pin]]=state
            def put(n,val):
                if n is not None:v[n]=int(bool(val))
            def get(n):return v.get(n,0)
            n=self.n['U203']
            for a,y in [('1','2'),('3','4'),('5','6'),('9','8'),('11','10'),('13','12')]:put(n[y],not get(n[a]))
            for ref in ['U204','U206']:
                n=self.n[ref]
                for a,b,c,y in [('1','2','13','12'),('3','4','5','6'),('9','10','11','8')]:put(n[y],get(n[a])and get(n[b])and get(n[c]))
            n=self.n['U205']
            for a,b,c,d,y in [('1','2','4','5','6'),('9','10','12','13','8')]:put(n[y],get(n[a])and get(n[b])and get(n[c])and get(n[d]))
            n=self.n['U207']
            for a,b,y in old.GATE_PINS:put(n[y],get(n[a])or get(n[b]))
            if prev==v:
                if not get(self.n['U202']['1']) and any(self.q):
                    self.q=[0]*6;return self.settle(i)
                return v
        raise AssertionError('R4 combinational/reset feedback failed to settle')

PIN_UPDATES={
 'U204':('Nexperia74HC11 physical3input AND map',{'1':'PREPARE','2':'KEY_N','13':'SLOT_N','12':'ARM_CONTEXT','3':'SAFE_N','4':'MUTE_N','5':'I2C_SCL','6':'CLEAR_A','9':'PREPARE','10':'SAFE_N','11':'MUTE_N','8':'SRC_ON','7':'GND','14':'V3V3'},'DATASHEET_PIN_ASSERTION'),
 'U205':('Nexperia74HC21 Rev10 17Jan2024 Fig1/2, SO14',{'1':'VALID_ARM','2':'ARM_DELAY','4':'SLOT','5':'ARM','6':'TX_OK','9':'CLEAR_A','10':'RUN_HEALTH','12':'V3V3','13':'V3V3','8':'CLR_N','7':'GND','14':'V3V3'},'MANUFACTURER_PIN_ASSERTION'),
 'U206':('Nexperia74HC11D physical3input AND map',{'1':'TX_OK','2':'NORMAL_Q','13':'CLEAR_A','12':'NORMAL_PERMIT','3':'TX_OK','4':'PATH_Q','5':'CLEAR_A','6':'TRAIN_PERMIT','9':'PA_PREPARE','10':'SRC_ON','11':'V3V3','8':'CONV_EN','7':'GND','14':'V3V3'},'DATASHEET_PIN_ASSERTION'),
 'U203':('Nexperia74HC14 inverters physicalpinpairs',{'1':'KEY','2':'KEY_N','3':'SLOT','4':'SLOT_N','5':'PATH_Q','6':'NORMAL_Q','9':'ARM_RC','8':'ARM_DELAY_N','11':'ARM_DELAY_N','10':'ARM_DELAY','13':'NORMAL_RC','12':'NORMAL_OFF','7':'GND','14':'V3V3'},'PIN_ASSERTION_RC_TIMING_NOT_RUN'),
 'U304':('TI SN74LVC2G08 physical1/2->7;5/6->3',{'1':'CONV_EN','2':'PACK_OK_N','3':'RAIL_RUN','4':'GND','5':'CONV_EN','6':'HARD_OK_N','7':'PACK_RUN','8':'V3V3'},'DATASHEET_PIN_ASSERTION'),
 'Q501':('ST PD54008L-E Jan2007Rev2p1 TOP VIEW,p13 recommended landing, visually inspected',{'G':'PA_GATE','D':'PA_DRAIN','S':'GND'},'FUNCTIONAL_REGION_PHYSICAL_GEOMETRY_INSPECTED_NOT_GENERIC_NUMERIC_MAP'),
 'U305':('TI TPS22919DCK physicalpin table, identical source-switch type',{'1':'VDRV_FILTER','2':'GND','3':'NORMAL_PERMIT','4':None,'5':'VDRV_RF','6':'VDRV_RF'},'DATASHEET_PIN_ASSERTION'),
 'U601':('TI SN74LVC1G125DBVR physicalpin table',{'1':'NORMAL_OFF','2':'CLK_NORMAL','3':'GND','4':'NORMAL_CLOCK_BUF','5':'V3V3'},'DATASHEET_PIN_ASSERTION'),
}

def load():
    parts={p['ref']:p for p in json.loads((DEST/'RF2M.electrical.json').read_text())['parts']};nets={}
    tree=ET.parse(OUT/'RF2M.net.xml')
    for net in tree.findall('./nets/net'):
        for node in net.findall('node'):
            nets.setdefault(node.attrib['ref'],{})[node.attrib['pin']]=None if net.attrib['name'].startswith('unconnected-')else net.attrib['name']
    for ref,p in parts.items():
        if not ref.startswith('#'):assert nets.get(ref)==p['pins'],('exported CAD/manifest mismatch',ref,nets.get(ref),p['pins'])
    for component in tree.findall('./components/comp'):
        ref=component.get('ref');p=parts[ref];fields={f.get('name'):f.text or''for f in component.findall('./fields/field')}
        assert component.findtext('value')==p['value'],('CAD value',ref)
        assert (component.findtext('footprint')or'')==p['footprint'],('CAD footprint',ref)
        for field,key in [('MPN','mpn'),('Population','population'),('Function','group')]:assert fields[field]==p[key],('CAD field',ref,field)
    return parts,nets

def pins(parts,nets):
    audit=[]
    for ref,(source,expected,status)in (old.AUDIT|PIN_UPDATES).items():
        if ref not in parts:continue
        assert nets[ref]==expected,('physicalpin',ref,nets[ref],expected)
        audit.append(dict(ref=ref,mpn=parts[ref]['mpn'],source=source,pins=expected,status=status,footprint=parts[ref]['footprint']or'OPEN'))
    return audit

REF={
 'TL603':('50R 6.23mm','MMIC_AC','ST_IS_A'), 'C631':('56p','ST_IS_A','GND'),
 'C632':('330p','ST_IS_A','ST_IS_B'),'TL604':('50R 6.62mm','ST_IS_B','ST_IS_C'),
 'C633':('27p','ST_IS_C','GND'),'L634':('18n','ST_IS_C','ST_IS_D'),
 'TL605':('50R 5.8mm','ST_IS_D','PA_GATE'),
 'TL606':('50R 2.2mm','PA_DRAIN','ST_O_A'),'C636':('33p','ST_O_A','GND'),
 'TL607':('50R 11mm','ST_O_A','ST_O_B'),'C637':('100p','ST_O_B','GND'),
 'L638':('18.5n','ST_O_B','ST_O_C'),'C638':('39p','ST_O_C','GND'),
 'TL608':('50R 12.4mm','ST_O_C','ST_O_D'),'C639':('330p','ST_O_D','ST_DC_BLOCK'),
 'TL609':('50R 2mm','ST_DC_BLOCK','ST_LPF_IN'),
 'L641':('39n','ST_LPF_IN','ST_F1'),'C641':('3.3p','ST_LPF_IN','ST_F1'),
 'L642':('22n','ST_F1','ST_F2'),'C642':('18p','ST_F1','ST_F2'),
 'L643':('27n','ST_F2','NORMAL_RF'),'C643':('12p','ST_F2','NORMAL_RF'),
 'C644':('22p','ST_LPF_IN','GND'),'C645':('27p','ST_F1','GND'),
 'C646':('22p','ST_F2','GND'),'C647':('15p','NORMAL_RF','GND'),
}
def reference(parts,nets):
    for ref,(val,a,b)in REF.items():
        assert parts[ref]['value']==val,(ref,'value')
        assert nets[ref]=={'1':a,'2':b},(ref,'reference topology',nets[ref])
    assert parts['R301']['value']=='116k'and parts['R303']['value']=='46.4k'and parts['R401']['value']=='634k'
    assert not any(r in parts for r in ['Q307','R414','U209'])
    assert not any(p['mpn'].split()[0]in ['MRF237','2N4427','BF981','PD84001','PHA-13HLN+']for p in parts.values())
    assert not any({'NORMAL_RF','TRAIN_RF'}<=set(p['pins'].values())for p in parts.values())
    assert nets['C602']=={'1':'MMIC_RF_DC','2':'MMIC_AC'}
    assert nets['C601']=={'1':'NORMAL_CLOCK_BUF','2':'SRC_RF'}
    assert nets['R606']['1']=='VMOD' and nets['L635']=={'1':'VPA','2':'PA_DRAIN'}
    assert parts['R517']['value']=='0'and parts['R517']['population']=='TRAIN_ONLY'
    assert nets['R517']=={'1':'MOD_DRIVE','2':'VPA_FB'}
    assert nets['R518']=={'1':'MOD_COMMAND','2':'GND'}and parts['R518']['population']=='TRAIN_ONLY'
    assert nets['R519']=={'1':'V3V3','2':'RUN_HEALTH'}and parts['R519']['population']=='TRAIN_ONLY'
    assert parts['U207']['population']=='NORMAL'

def landing(text=None):
    s=cad.parse(text if text is not None else (DEST/'ARDF_2M.pretty/PD54008L_ST_GDS_5x5.kicad_mod').read_text())
    pads={p[1]:dict(at=list(map(float,cad.child(p,'at')[1:])),size=list(map(float,cad.child(p,'size')[1:])))for p in cad.children(s,'pad')}
    assert pads=={'G':{'at':[-2.25,0.0],'size':[.5,5.]},'D':{'at':[2.25,0.0],'size':[.5,5.]},'S':{'at':[0.,0.],'size':[2.7,5.]}},pads
    return pads

def main():
    parts,nets=load();report=pins(parts,nets);reference(parts,nets);pads=landing()
    from m5a_r4_footprints import check as check_package_landings
    package_landings=check_package_landings(DEST/'ARDF_2M.pretty',cad.parse,cad.child,cad.children)
    assert parts['U501']['footprint']=='ARDF_2M:PHA1_DF782_RevG'
    assert parts['U302']['footprint']=='ARDF_2M:TI_RNW0013A_4222804C'
    # Reuse independent behavioral expectations, but evaluate the REVISED physical gates.
    old.Logic=Logic;logic=old.tests(nets)
    m=Logic(nets);i={**old.BASE,'PREPARE':1,'MUTE_N':1,'SAFE_N':1,'ARM':0,'SLOT':0}
    z=m.step(**i);assert z['SRC_ON']and not z['NORMAL_PERMIT']and not z['TRAIN_PERMIT']and z['NORMAL_OFF']
    logic['scenarios'].append('powered_source_configuration_ARM_SLOT_low')
    for pth in [0,1]:
        m=Logic(nets);i={**old.BASE,'PREPARE':1,'PA_PREPARE':1-pth,'PATH_TRAIN':pth};m.step(**i)
        i['ARM']=1;m.step(**i);i['ARM_RC']=1;m.step(**i);i['SLOT']=1;z=m.step(**i)
        assert z['NORMAL_OFF']==bool(pth)
        assert nets['U305']['3']=='NORMAL_PERMIT'and nets['U601']['1']=='NORMAL_OFF'
        assert nets['Q502']['1']=='NORMAL_OFF'
        i['SAFE_N']=0;z=m.step(**i);assert z['NORMAL_OFF']and not z['SRC_ON']and not z['NORMAL_PERMIT']and not z['TRAIN_PERMIT']
        logic['scenarios'].append('physical_normal_clock_bias_driver_controls_path'+str(pth))
    mutations=[]
    for ref,pin,bad in [('Q501','G','GND'),('Q501','S','PA_DRAIN'),('Q401','1','VMOD'),('U501','1','MMIC_RF_DC'),('U205','1','V3V3'),('U205','5','V3V3'),('U206','13','V3V3'),('U206','4','NORMAL_Q'),('U304','5','NORMAL_PERMIT'),('U305','3','V3V3'),('U601','1','GND'),('C642','2','GND'),('C632','2','GND'),('TL607','2','NORMAL_RF'),('R517','1','GND')]:
        changed=copy.deepcopy(nets);changed[ref][pin]=bad
        try:pins(parts,changed);reference(parts,changed);old.tests(changed)
        except(AssertionError,KeyError):mutations.append(ref+':'+pin)
        else:raise AssertionError('Mutation escaped '+ref+':'+pin)
    footprint=(DEST/'ARDF_2M.pretty/PD54008L_ST_GDS_5x5.kicad_mod').read_text()
    try:landing(footprint.replace('(at -2.25 0)','(at 2.25 0)',1))
    except AssertionError:mutations.append('ST_G_landing_wrong_physical_side')
    else:raise AssertionError('Physical G/D-side mutation escaped')
    changed=copy.deepcopy(parts);changed['C632']['value']='390p'
    try:reference(changed,nets)
    except AssertionError:mutations.append('ST_330p_versus_conflicting_391_code')
    else:raise AssertionError('Value mutation escaped')
    # Exercise independent physical landing assertions against changed FILES,
    # not just the intended schematic pin dictionary.
    for name,original,bad in [
        ('PHA1_DF782_RevG.kicad_mod','(at -1.4986 -0.7493)','(at 1.4986 -0.7493)'),
        ('TI_RNW0013A_4222804C.kicad_mod','(pad "7" smd roundrect(at 0 0)','(pad "7" smd roundrect(at -0.55 0)')]:
        with tempfile.TemporaryDirectory(prefix='r4-landing-mutation-')as tmp:
            for fp in (DEST/'ARDF_2M.pretty').glob('*.kicad_mod'):shutil.copy(fp,tmp)
            from pathlib import Path
            fp=Path(tmp)/name;source=fp.read_text();assert original in source,(name,original)
            fp.write_text(source.replace(original,bad,1))
            try:check_package_landings(tmp,cad.parse,cad.child,cad.children)
            except AssertionError:mutations.append(name+':physical_pad_displacement')
            else:raise AssertionError('Physical landing mutation escaped '+name)
    # Independent supply-switch truth table follows actual physical pin numbers.
    rows=[]
    for a,b,c,d in itertools.product([0,1],repeat=4):
        v=dict(CONV_EN=a,PACK_OK_N=b,NORMAL_PERMIT=c,HARD_OK_N=d);n=nets['U304']
        got={n[y]:bool(v[n[x]]and v[n[z]])for x,z,y in [('1','2','7'),('5','6','3')]}
        assert got==dict(PACK_RUN=bool(a and b),RAIL_RUN=bool(a and d));rows.append(v|got)
    assert frozen()==json.loads((OUT/'preserved-baseline.json').read_text())
    (OUT/'pinout-audit.json').write_text(json.dumps(dict(devices=report,ST_physical_landing_regions=pads,additional_package_landings=package_landings,limitations='Numeric terminal-group numbers not invented; match ST G-left,D-right,source-center TOP VIEW. No PCB exists. Solder stencil/vias/thermal implementation OPEN.'),indent=2)+'\n')
    (OUT/'verification.json').write_text(json.dumps(dict(status='PASS_STATIC_AND_EXPORT_CHECKS_ONLY',manifest_positions=len(parts),logic=logic,mutation_tests=mutations,ST_reference_positions=len(REF),physical_switch_truth_rows=rows,unchanged_files=len(frozen()),physical_measurements='NOT_RUN',timing='Datasheet/RC estimates only; no new analog/timing simulation or hardware timing pass claimed'),indent=2)+'\n')
    print('PASS:',len(parts),'CAD positions,',logic['combinations'],'logic combinations,',len(logic['scenarios']),'states,',len(mutations),'mutations,',len(report),'pin maps,',len(REF),'ST network values/nets')

if __name__=='__main__':main()
