#!/usr/bin/python3
"""Read-only V1 fabrication/coverage checks and M4A package checksums.
Requires completed review exports. Does not write the E2 baseline.
"""
import argparse,collections,csv,hashlib,json,re,subprocess,tarfile
import pcbnew as pcb
from m4a_design import R,E,P,D,NAME,frozen
from m3be2_audit import mm,xy,fp

def dump(name,x):(D/name).write_text(json.dumps(x,indent=2)+'\n')
def audit():
    frozen();b=pcb.LoadBoard(str(P/(NAME+'.kicad_pcb')));fs={f.GetReference():f for f in b.GetFootprints()};settings=json.loads((P/(NAME+'.kicad_pro')).read_text())['board']['design_settings'];drc=json.loads((D/'DRC.json').read_text());erc=json.loads((D/'ERC.json').read_text());ds=b.GetDesignSettings()
    assert not settings['drc_exclusions']and all(v!='ignore'for v in settings['rule_severities'].values())
    assert not drc['ignored_checks']and not drc['violations']and not drc['unconnected_items']and not drc['schematic_parity']
    assert erc['ignored_checks']==json.loads((E/'review/M3B-E2/ERC.json').read_text())['ignored_checks'],'Inherited informational ERC defaults changed'
    assert {x['key']for x in erc['ignored_checks']}=={'single_global_label','four_way_junction','simulation_model_issue'}
    assert not[v for s in erc['sheets']for v in s['violations']]
    dump('drc-coverage.json',dict(revision='M4A-V1',tool=drc['kicad_version'],full_design_settings=settings,custom_rules=(P/(NAME+'.kicad_dru')).read_text(),board_soldermask=dict(expansion_mm=mm(ds.m_SolderMaskExpansion),minimum_web_mm=mm(ds.m_SolderMaskMinWidth)),ignored_DRC=drc['ignored_checks'],ignored_ERC=erc['ignored_checks'],limitation='Native KiCad rule table/CLI reports; no claim of an independently enumerated undocumented check registry',result=dict(violations=0,unrouted=0,parity=0)))
    expected=collections.Counter();holes=collections.Counter();models={};padboxes=[]
    for f in fs.values():
        if len(f.Models()):models[f.GetReference()]=[m.m_Filename for m in f.Models()]
        for pad in f.Pads():
            if pad.GetDrillSize().x:
                kind='NPTH'if pad.GetAttribute()==pcb.PAD_ATTRIB_NPTH else'PTH';v=pad.GetPosition();expected[(kind,mm(pad.GetDrillSize().x),mm(v.x),mm(v.y))]+=1;holes[(kind,mm(pad.GetDrillSize().x))]+=1
            if pad.GetAttribute()==pcb.PAD_ATTRIB_SMD:padboxes.append(pad.GetBoundingBox())
    nets=collections.defaultdict(lambda:dict(length_mm=0.,widths_mm=set(),vias=0));via_count=0;minwidth=10.
    for t in b.GetTracks():
        n=nets[t.GetNetname()]
        if isinstance(t,pcb.PCB_VIA):
            via_count+=1;v=t.GetPosition();expected[('PTH',mm(t.GetDrill()),mm(v.x),mm(v.y))]+=1;holes[('PTH',mm(t.GetDrill()))]+=1;n['vias']+=1
            assert all(not box.Contains(v)for box in padboxes),'Unqualified via in SMD pad'
        else:
            w=mm(t.GetWidth());minwidth=min(minwidth,w);n['length_mm']+=pcb.ToMM(t.GetLength());n['widths_mm'].add(w)
    assert minwidth>=.15 and b.GetCopperLayerCount()==2
    for x in nets.values():x['length_mm']=round(x['length_mm'],3);x['widths_mm']=sorted(x['widths_mm'])
    dump('routing-summary.json',dict(nets=nets,ordinary_vias=via_count,min_trace_mm=minwidth,RF_limitation='Summed trace length is not an RF impedance/loop-inductance or thermal measurement. Ground plane continuity and compact coupling require physical qualification.'))
    g=D/'gerbers';gers=[q for q in g.iterdir()if q.suffix in('.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1')];assert len(gers)==9
    for q in gers:assert 'M4A-V1'in q.read_text(),q
    actual=collections.Counter()
    for q in g.glob('*.drl'):
        text=q.read_text();assert 'M48'in text and'METRIC'in text and'M30'in text;tools={};active=None;kind='NPTH'if'NPTH'in q.name else'PTH'
        for line in text.splitlines():
            z=re.fullmatch(r'T(\d+)C([\d.]+)',line)
            if z:tools[z[1]]=float(z[2]);continue
            z=re.fullmatch(r'T(\d+)',line)
            if z:active=tools[z[1]];continue
            z=re.fullmatch(r'X([-\d.]+)Y([-\d.]+)',line)
            if z:actual[(kind,active,float(z[1]),-float(z[2]))]+=1
    assert sum(actual.values())==sum(expected.values());remaining=actual.copy();max_quantization=0
    for key,n in expected.items():
        for _ in range(n):
            candidates=[k for k,v in remaining.items()if v and k[:2]==key[:2]and max(abs(k[2]-key[2]),abs(k[3]-key[3]))<=.00101];assert candidates,('Native hole absent/wrong export',key)
            match=min(candidates,key=lambda k:(k[2]-key[2])**2+(k[3]-key[3])**2);remaining[match]-=1;max_quantization=max(max_quantization,abs(match[2]-key[2]),abs(match[3]-key[3]))
    assert not any(remaining.values())
    flashes={};ref=pin=net=None
    for line in(g/(NAME+'-F_Cu.gtl')).read_text().splitlines():
        z=re.fullmatch(r'%TO.P,([^,]+),([^,*]+)(?:,[^*]*)?\*%',line)
        if z:ref,pin=z[1],z[2]
        z=re.fullmatch(r'%TO.N,([^*]+)\*%',line)
        if z:net=z[1]
        if line=='%TD*%':ref=pin=net=None
        z=re.fullmatch(r'X(-?\d+)Y(-?\d+)D03\*',line)
        if z and ref in('Q403','U311'):flashes[(ref,pin)]=dict(net=net,position_mm=[int(z[1])/1e6,-int(z[2])/1e6])
    assert len(flashes)==6
    for(ref,pin),obs in flashes.items():
        native=fp(fs[ref])['pads'][pin];assert obs['net']==native['net']and obs['position_mm']==native['position_mm']
    ipc={}
    for line in(D/(NAME+'.ipc')).read_text().splitlines():
        z=re.match(r'^(?:317|327)(\S+)\s+(Q403|U311)\s+-(\d+)\s',line)
        if z:ipc[(z[2],z[3])]=z[1]
    assert len(ipc)==6 and all(ipc[k]==v['net']for k,v in flashes.items())
    positions={}
    for pop,want in[('full',195),('fox',115)]:
        rows=list(csv.DictReader((D/(NAME+'-position-'+pop+'.csv')).open()));assert len(rows)==want,(pop,len(rows));positions[pop]=len(rows)
    assert set(str(q.GetNetname())for q in fs['J502'].Pads())=={'RF_FOX','GND','FOX_ID'}
    for r in('Q403','U311'):assert fs[r].GetReference()==r
    dump('mechanical-stackup.json',dict(revision='M4A-V1',size_mm=[150,110],thickness_mm=mm(ds.GetBoardThickness()),copper_layers=2,nominal_outer_copper_um=35,stackup='FR4 1.6mm nominal,35um outer copper; ordinary PTH; no blind/buried vias or paid impedance control; supplier confirmation/quote pending',drill_table=[dict(type=k[0],nominal_mm=k[1],quantity=v)for k,v in sorted(holes.items())],mounting_holes_native_mm={r:xy(fs[r].GetPosition())for r in('H1','H2','H3','H4')},critical_finished_holes={'J101':'1.20+/-0.05mm','J502':'0.95+/-0.05mm','Q402/Q403':'1.30+/-0.05mm; incoming lead/body fit required'},models=models,model_limit='Copied qualified geometry/dimensional envelope classifications remain E2 limitations; actual windings, heatsinks and harnesses NOT_RUN',physical_tests='NOT_RUN'))
    dump('fabrication-audit.json',dict(status='CAD/export checks PASS; PRODUCTION-INTENT NOT RELEASED',Gerber_layers=9,separate_PTH_NPTH=True,native_drill_coordinates_verified=sum(expected.values()),maximum_drill_coordinate_quantization_mm=round(max_quantization,6),corrected_pin_copper_flashes_and_IPC={r:{pin:flashes[(r,pin)]for pin in('1','2','3')}for r in('Q403','U311')},placement_rows=positions,limitations='No independent raster/etch simulation, physical dimensional/RF/thermal tests or supplier approval',tool_versions=dict(kicad_cli=subprocess.check_output(['kicad-cli','version'],text=True).strip(),pcbnew=pcb.GetBuildVersion())))
    probes=[]
    for r,f in sorted(fs.items()):
        if r.startswith('TP'):probes.append(dict(reference=r,net=next(iter(f.Pads())).GetNetname(),native_x_mm=xy(f.GetPosition())[0],native_y_mm=xy(f.GetPosition())[1]))
    with(D/'production-test-pads.csv').open('w')as out:
        w=csv.DictWriter(out,fieldnames=list(probes[0]),lineterminator='\n');w.writeheader();w.writerows(probes)
    print('PASS V1 manufacturing exports/coverage;',sum(expected.values()),'drills;',via_count,'vias; no via-in-SMD-pad')
def manifests():
    frozen()
    paths=list(P.rglob('*'))+list((R/'docs').glob('M4A*'))+list((R/'tools').glob('m4a*.py'))+[R/'README.md']
    rows=[]
    for q in sorted(set(paths)):
        if not q.is_file()or q.name in('SHA256SUMS','file-manifest.json')or q.suffix=='.kicad_prl'or'__pycache__'in q.parts:continue
        rows.append(dict(path=str(q.relative_to(R)),bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
    dump('file-manifest.json',dict(revision='M4A-V1',reference_commit='1245023',classification='PRODUCTION-INTENT - NOT RELEASED',files=rows));(D/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n'for x in rows))
    h=E/'handoff/M4A-E2';hrows=[]
    with tarfile.open(h/'ARDF-TX_E2_1245023_source.tar.gz')as tar:
        assert tar.extractfile('hardware/80m/RF80.kicad_pcb').read()==(E/'RF80.kicad_pcb').read_bytes()
    for q in sorted(h.rglob('*')):
        if q.is_file()and q not in(h/'SHA256SUMS',h/'file-manifest.json'):hrows.append(dict(path=str(q.relative_to(h)),bytes=q.stat().st_size,sha256=hashlib.sha256(q.read_bytes()).hexdigest()))
    (h/'file-manifest.json').write_text(json.dumps(dict(reference_commit='1245023',reference_tag='m3b-e2',files=hrows),indent=2)+'\n');(h/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n'for x in hrows));print('Hashed',len(rows),'V1/reproducibility files and',len(hrows),'standalone E2 handoff files')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--manifest',action='store_true');args=a.parse_args();manifests()if args.manifest else audit()
