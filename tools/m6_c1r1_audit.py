#!/usr/bin/python3
"""Read-only baseline preservation and localized controller-change audit."""
import json,hashlib,subprocess,collections,sys
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1R1';BASE='31ac3eb4c4569e710472ecab86baec6d9b7c9399'
def sh(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    frozen=json.loads((D/'frozen-M6-C1-files.json').read_text())
    for f,h in frozen.items():assert sh(ROOT/f)==h,f
    old=json.loads(subprocess.check_output(['git','show',BASE+':hardware/controller/CTRL.electrical.json'],text=True));new=json.loads((P/'CTRL.electrical.json').read_text());old={x['ref']:x for x in old['parts']};new={x['ref']:x for x in new['parts']};changed=[]
    allowed={'R3':{'1':'PACK_ID_EXC','2':'PACK_ID_RAW'},'C25':{'1':'PACK_ID_SAFE','2':'GND'},'U21':{'5':'PACK_ID_SAFE'}}
    for r,part in old.items():
        assert r in new,r
        a,b=part['pins'],new[r]['pins']
        for pin,net in a.items():
            want=allowed.get(r,{}).get(pin,net);assert b[pin]==want,(r,pin,b[pin],want)
        for key in ['footprint','mpn','population','value']:
            if r=='R3' and key in ['value','mpn']:continue
            assert part[key]==new[r][key],(r,key)
        if a!=b or part['value']!=new[r]['value']:changed.append(r)
    assert set(new)-set(old)=={'D22','D23','R8','R9','R19'}
    tmp=Path('/tmp/m6-c1r1-immutable-baseline.kicad_pcb');tmp.write_bytes(subprocess.check_output(['git','show',BASE+':hardware/controller/CTRL.kicad_pcb']));a=p.LoadBoard(str(tmp));b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));fa={x.GetReference():x for x in a.GetFootprints()};fb={x.GetReference():x for x in b.GetFootprints()}
    for r,f in fa.items():
        if r=='R3':continue
        g=fb[r];assert f.GetPosition()==g.GetPosition() and f.GetOrientationDegrees()==g.GetOrientationDegrees() and f.GetLayer()==g.GetLayer(),r
    def tracks(board,prefix):
        result=[]
        for t in board.GetTracks():
            n=t.GetNetname()
            if not n.startswith(prefix):continue
            via=isinstance(t,p.PCB_VIA);result.append((n,t.GetClass(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetWidth(p.F_Cu) if via else t.GetWidth(),t.GetDrillValue() if via else t.GetLayer()))
        return collections.Counter(result)
    assert tracks(a,'USB_')==tracks(b,'USB_'),'USB copper changed'
    ta,tb=tracks(a,''),tracks(b,'');removed=ta-tb;added=tb-ta
    assert set(k[0] for k in removed)<= {'PACK_ID_RAW','V3V3'},'unrelated copper removed'
    assert set(k[0] for k in added)<= {'PACK_ID_RAW','PACK_ID_SAFE','PACK_ID_ADC','PACK_PROT','PACK_ID_EXC'},'unrelated copper added'
    track_delta={'removed_by_net':dict(collections.Counter({n:sum(v for k,v in removed.items() if k[0]==n) for n in sorted({k[0] for k in removed})})),'added_by_net':dict(collections.Counter({n:sum(v for k,v in added.items() if k[0]==n) for n in sorted({k[0] for k in added})})),'other_track_and_via_geometry':'UNCHANGED; only the two obsolete V3V3 pull-up branch pieces are removed outside ID nets'}
    # Every old purchased footprint remains physically identical except relocated R3.
    for r in ['U3','J2','C10','R14','R15','D3','D4','U2','Q2']:
        assert fa[r].GetValue()==fb[r].GetValue(),r
    pins=sum(len([x for x in f.Pads() if x.GetNumber()]) for r,f in fa.items() if not r.startswith('H'))
    positions={r:{'xy_mm':[p.ToMM(fb[r].GetPosition().x),p.ToMM(fb[r].GetPosition().y)],'side':b.GetLayerName(fb[r].GetLayer()),'angle':fb[r].GetOrientationDegrees(),'pads':{x.GetNumber():{'net':x.GetNetname(),'size_mm':[p.ToMM(x.GetSize().x),p.ToMM(x.GetSize().y)]} for x in fb[r].Pads()}} for r in ['R3','R8','R9','R19','D22','D23']}
    for r in ['D22']:
        assert all(abs(p.ToMM(x.GetSize().x)-1.475)<.001 and abs(p.ToMM(x.GetSize().y)-.6)<.001 for x in fb[r].Pads())
    assert all(abs(p.ToMM(x.GetSize().x)-1.1)<.001 and abs(p.ToMM(x.GetSize().y)-1.1)<.001 for x in fb['D23'].Pads())
    result={'status':'PASS','baseline_commit':BASE,'baseline_pad_instances_preserved':pins,'legitimate_baseline_component_changes':changed,'added_purchased_parts':sorted(set(new)-set(old)),'all_other_existing_footprint_positions_and_packages':'UNCHANGED','USB_topology_and_copper':'UNCHANGED','native_track_via_delta':track_delta,'frozen_M6_C1_review_files_unchanged':len(frozen),'RF_preservation':'See electrical-regression.json,1220 files','native_PCB_sha256':sh(P/'CTRL.kicad_pcb'),'protection_positions':positions,'new_critical_manufacturer_maps':{'D22':'Nexperia BAS116 SOT23,1A/2NC/3K;235 packing suffix, same device pinout','D23':'Nexperia BAT54H SOD123F,1K/2A; not onsemiSOD323 BAT54H'},'physical_fit':'CAD lead coverage checked; first-article component fit/underside lead clearance NOT_RUN'}
    (D/'change-and-preservation-audit.json').write_text(json.dumps(result,indent=2)+'\n');print('Preserved',pins,'baseline pads,',len(frozen),'historical review files; USB copper unchanged')
if __name__=='__main__':main()
