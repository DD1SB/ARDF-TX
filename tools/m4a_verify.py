#!/usr/bin/python3
"""Frozen-reference electrical equivalence, real-pad checks and fault mutations.
No compact-layout RF/thermal/analog equivalence is implied by these checks.
"""
import argparse,copy,hashlib,json,os
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as pcb
from m4a_design import E,P,D,NAME,KEEP,frozen
import m3be2_pinouts as maker
def nets(path):
    tree=ET.parse(path);nn={}
    for n in tree.findall('./nets/net'):
        for p in n.findall('node'):nn[(p.attrib['ref'],p.attrib['pin'])]=n.attrib['name'].removeprefix('/')
    return tree,nn
def comparable(n):return{k:v for k,v in n.items()if not k[0].startswith('TP')}
def compare(a,b):assert comparable(a)==comparable(b),'Non-TP physical net membership differs from E2'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--logic',action='store_true');a=ap.parse_args();frozen()
    old=json.loads((E/'RF80.electrical.json').read_text());new=json.loads((P/(NAME+'.electrical.json')).read_text());om={x['ref']:x for x in old['parts']if not x['ref'].startswith('TP')};nm={x['ref']:x for x in new['parts']if not x['ref'].startswith('TP')}
    assert om==nm,'A non-test component identity/value/net/population was modified'
    ot,on=nets(E/'review/M3B-E2/RF80.xml');nt,nn=nets(D/(NAME+'.xml'));compare(on,nn)
    def identities(t):
        return{c.attrib['ref']:(c.findtext('value'),c.findtext('footprint'),{p.attrib['name']:p.attrib.get('value')for p in c.findall('property')if p.attrib['name']in('MPN','Population')})for c in t.findall('./components/comp')if not c.attrib['ref'].startswith('TP')}
    assert identities(ot)==identities(nt)
    b=pcb.LoadBoard(str(P/(NAME+'.kicad_pcb')));fs={f.GetReference():f for f in b.GetFootprints()};parts={x['ref']:x for x in new['parts']if not x['ref'].startswith('#')};assert set(fs)==set(parts)|{'H1','H2','H3','H4'}
    old_board=pcb.LoadBoard(str(E/'RF80.kicad_pcb'));old_fs={f.GetReference():f for f in old_board.GetFootprints()}
    def geometry(f):
        return{p.GetNumber():(tuple(round(pcb.ToMM(v),5)for v in(p.GetFPRelativePosition().x,p.GetFPRelativePosition().y)),tuple(p.GetSize()),tuple(p.GetDrillSize()),int(p.GetShape()),int(p.GetAttribute()),round(p.GetFPRelativeOrientation().AsDegrees()%360,4))for p in f.Pads()}
    for r,f in fs.items():
        if r.startswith('H'):continue
        part=parts[r]
        assert str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName())==part['footprint'],(r,'Native footprint identity')
        assert f.GetValue()==part['value'],(r,'Native value')
        assert f.IsDNP()==(part['population']in('FOX','DNP')),(r,'Native full-population DNP flag')
        assert geometry(f)==geometry(old_fs[r]),(r,'Footprint-local pad/lead/drill geometry changed from E2')
    checked=0
    def board_parity():
        count=0
        for r,f in fs.items():
            if r.startswith('H'):continue
            for p in f.Pads():assert p.GetNetname()==nn.get((r,p.GetNumber()),''),(r,p.GetNumber(),'PCB/XML mismatch');count+=1
        return count
    checked=board_parity();maker.H=P;physical=maker.collect(D/(NAME+'.xml'),b);audits=[]
    for r,v in physical.items():
        if r!='Q403':maker.check_one(r,v)
        else:
            assert v['symbol']=='BD140_ST'and v['manufacturer_field']=='STMicroelectronics'
            assert v['footprint']=='ARDF_TX:ST_BD140_SOT32_1p3Drill'and v['rotation']==180
            assert v['pcb']==v['netlist']=={'1':'SHAPE_BASE','2':'VPA_SHAPED','3':'VPA_LOAD'}
            assert {k:x['name']for k,x in v['symbol_pins'].items()}=={'1':'B','2':'C','3':'E'}
            assert v['pad_mm']['3'][0]<v['pad_mm']['2'][0]<v['pad_mm']['1'][0]
            assert all(abs(z-1.3)<.001 for z in v['drills_mm'].values())
        audits.append(dict(reference=r,mpn=v['mpn'],footprint=v['footprint'],physical_pins=v['pcb'],manufacturer=maker.CAT[v['mpn']]['manufacturer'],datasheet=maker.CAT[v['mpn']]['source'],package_evidence=maker.CAT[v['mpn']]['package'],status='CAD/manufacturer mapping verified; physical fit/operation NOT_RUN'))
    rejected=[]
    mutations=[('Q403 base/emitter','Q403','1','VPA_LOAD'),('TL431 anode','U311','3','VREF_2V5'),('watchdog inverted Q','U202','13','NC'),('driver inhibit','U401','5','CLK_PA'),('raw ARM capture','U224','9','ARM_CLK'),('Fox supply','U501','14','VPA_LOAD'),('Fox connector isolation','J502','1','RF_NORMAL'),('normal filter','C414','1','RF_FOX'),('Si5351 source clock','U101','10','CLK_FOX')]
    for label,ref,pin,net in mutations:
        bad=copy.deepcopy(nn);bad[(ref,pin)]=net
        try:compare(on,bad)
        except AssertionError:rejected.append(label)
        else:raise AssertionError('Equivalence mutation escaped '+label)
    # Mutate the actual native board instance, without saving it.
    pad=next(p for p in fs['Q403'].Pads()if p.GetNumber()=='1');original=pad.GetNet();pad.SetNet(b.FindNet('VPA_LOAD'))
    try:board_parity()
    except AssertionError:rejected.append('actual native Q403 pad1 net mutation')
    else:raise AssertionError('PCB mutation escaped')
    pad.SetNet(original)
    for field,value in [('population','BOTH'),('value','100k')]:
        bad=copy.deepcopy(nm);bad['R348'][field]=value
        try:assert om==bad
        except AssertionError:rejected.append('component '+field+' mutation')
        else:raise AssertionError('Component mutation escaped')
    pops={}
    for name,valid in [('Full',('BOTH','NORMAL')),('Fox',('BOTH','FOX'))]:
        refs=sorted(r for r,p in parts.items()if not r.startswith('TP')and p['population']in valid);pops[name]=dict(purchased_components=len(refs),ICs=sum(r.startswith('U')for r in refs),references=refs)
    assert pops['Full']['purchased_components']==196 and pops['Fox']['purchased_components']==115
    fox=set(pops['Fox']['references']);full=set(pops['Full']['references']);assert {'R228','R348','R349'}<=fox and not{'R228','R348','R349'}&full
    for r in('U301','U302','U312','U313','U401','Q402','Q403','T401','L410','L411','J401','TH301'):assert r not in fox,(r,'normal hardware fitted in Fox variant')
    assert nm['R228']['pins']=={'1':'PA_GUARD_RAW','2':'GND'}
    assert all(nm[r]['pins']['2']=='GND'for r in('R348','R349'))
    for r in fox:
        if parts[r]['group']=='fox':assert not set(parts[r]['pins'].values())&{'VPA','VPA_LOAD','VPA_SHAPED','DRAIN_PA','RF_NORMAL'},(r,'Fox depends on watt power path')
    erc=json.loads((D/'ERC.json').read_text());assert not[v for s in erc['sheets']for v in s['violations']]
    drc_path=D/'DRC.json';cad=None
    if drc_path.exists():
        q=json.loads(drc_path.read_text());cad=dict(violations=len(q['violations']),unrouted=len(q['unconnected_items']),parity=len(q['schematic_parity']),ignored=q['ignored_checks'])
        assert cad==dict(violations=0,unrouted=0,parity=0,ignored=[]),cad
    if a.logic:
        os.environ['RF80_NETLIST']=str(D/(NAME+'.xml'));from m3a_r1_logic import verify
        result=verify();assert result['truth_cases']==256 and len(result['state_scenarios'])==31 and len(result['timing_corners'])==16
        (D/'logic-results.json').write_text(json.dumps(result,indent=2)+'\n')
        (D/'logic-source.json').write_text(json.dumps(dict(candidate_revision='M4A-V1',engine='m3a_r1_logic.verify; engine revision retained in logic-results.json',netlist=str((D/(NAME+'.xml')).relative_to(P)),netlist_sha256=hashlib.sha256((D/(NAME+'.xml')).read_bytes()).hexdigest(),truth_cases=256,state_scenarios=31,timing_corners=16,classification='Ideal pin-derived logic/timing checks; physical tests NOT_RUN'),indent=2)+'\n')
    report=dict(date='2026-10-15',revision='M4A-V1',baseline='1245023/m3b-e2',status='ELECTRICAL CAD EQUIVALENCE PASS; PHYSICAL EQUIVALENCE NOT CLAIMED',non_TP_components=len(om),physical_pad_memberships=checked,all_native_footprint_local_geometries_unchanged=True,removed_test_pads=60,retained_test_pads=len(KEEP),critical_devices=audits,negative_cases_rejected=rejected,populations=pops,ERC_violations=0,DRC=cad,physical_gates='ALL NOT_RUN; compact parasitics/coupling/ground/thermal must be measured separately')
    (D/'electrical-equivalence.json').write_text(json.dumps(report,indent=2)+'\n');print('PASS: E2 non-TP manifest/XML equivalence;',checked,'native pads;',len(audits),'manufacturer devices;',len(rejected),'mutants rejected; full/Fox',len(full),len(fox))
if __name__=='__main__':main()
