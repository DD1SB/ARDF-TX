#!/usr/bin/python3
"""Read-only E2 CAD/change/manufacturing audit and review manifest.

Does not alter native CAD, route, suppress DRC or contact a manufacturer.
Run after final exports; --manifest refreshes hashes only (after documentation).
"""
import argparse, collections, csv, hashlib, json, re, subprocess, tempfile
from pathlib import Path
import pcbnew as p

R=Path(__file__).resolve().parents[1]; H=R/'hardware/80m'; D=H/'review/M3B-E2'
def dump(name,data): (D/name).write_text(json.dumps(data,indent=2)+'\n')
def mm(x): return round(p.ToMM(x),6)
def xy(v): return [mm(v.x),mm(v.y)]
def uid(x): return x.m_Uuid.AsString()
def tracks(b):
    rows={}
    for t in b.GetTracks():
        v=isinstance(t,p.PCB_VIA)
        rows[uid(t)]=dict(net=t.GetNetname(),kind='via' if v else 'track',start=xy(t.GetStart()),end=xy(t.GetEnd()),width_mm=mm(t.GetWidth(p.F_Cu) if v else t.GetWidth()),layer=b.GetLayerName(t.GetLayer()),drill_mm=mm(t.GetDrill()) if v else None)
    return rows
def fp(f): return dict(origin_mm=xy(f.GetPosition()),rotation=f.GetOrientationDegrees(),footprint=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),pads={q.GetNumber():dict(net=q.GetNetname(),position_mm=xy(q.GetPosition()),size_mm=xy(q.GetSize()),drill_mm=xy(q.GetDrillSize())) for q in f.Pads()})
def audit():
    project=json.loads((H/'RF80.kicad_pro').read_text()); settings=project['board']['design_settings']
    drc=json.loads((D/'DRC.json').read_text());erc=json.loads((D/'ERC.json').read_text())
    assert not drc['ignored_checks'] and not settings['drc_exclusions']
    assert all(v!='ignore' for v in settings['rule_severities'].values())
    assert not drc['violations'] and not drc['unconnected_items'] and not drc['schematic_parity']
    assert not [v for s in erc['sheets'] for v in s['violations']]
    b=p.LoadBoard(str(H/'RF80.kicad_pcb')); ds=b.GetDesignSettings()
    coverage=dict(revision='M3B-E2',tool=drc['kicad_version'],full_design_settings=settings,custom_rules=(H/'RF80.kicad_dru').read_text(),board_soldermask=dict(expansion_mm=mm(ds.m_SolderMaskExpansion),minimum_web_mm=mm(ds.m_SolderMaskMinWidth)),reported_ignored_DRC=drc['ignored_checks'],reported_ignored_ERC=erc['ignored_checks'],registry_limit='KiCad Python exposes no DRC-item registry; native project rule table and CLI ignored_checks are the reproducible coverage evidence. No claim of independently enumerating undocumented plugin tests.',result=dict(violations=0,unrouted=0,parity=0))
    dump('drc-coverage.json',coverage)
    oldsettings=json.loads((D/'E1_DRC_CONFIGURATION.json').read_text())
    with (D/'drc-coverage.csv').open('w')as out:
        w=csv.writer(out,lineterminator='\n');w.writerow(['native_check','E1_severity','E2_severity'])
        for k,v in sorted(settings['rule_severities'].items()):w.writerow([k,oldsettings['rule_severities'].get(k,'default'),v])
    with tempfile.TemporaryDirectory(prefix='m3be2-compare-')as tmp:
        q=Path(tmp)/'E1.kicad_pcb';q.write_bytes(subprocess.check_output(['git','show','m3b-e1:hardware/80m/RF80.kicad_pcb'],cwd=R));old=p.LoadBoard(str(q))
        ot,nt=tracks(old),tracks(b);removed={k:v for k,v in ot.items() if k not in nt};added={k:v for k,v in nt.items()if k not in ot};changed={k:dict(E1=ot[k],E2=nt[k])for k in ot.keys()&nt.keys()if ot[k]!=nt[k]}
        assert len(removed)==4 and not changed
        assert all(x['net'] in ('GND','VREF_2V5')for x in list(removed.values())+list(added.values()))
        of={f.GetReference():fp(f)for f in old.GetFootprints()};nf={f.GetReference():fp(f)for f in b.GetFootprints()}
        fc={r:dict(E1=of[r],E2=nf[r])for r in of if of[r]!=nf[r]};assert set(fc)=={'Q403','U311'},set(fc)
        assert all(of[r]['origin_mm']==nf[r]['origin_mm'] and of[r]['rotation']==nf[r]['rotation']for r in of if r!='Q403')
        dump('connectivity-change-audit.json',dict(baseline_tag='m3b-e1',baseline_commit='55a5b3f',revision='M3B-E2',removed_tracks=removed,added_tracks_and_via=added,changed_existing_tracks=changed,changed_footprint_geometry_or_nets=fc,all_other_tracks_and_vias_unchanged=True,RF_source_gate_drain_transformer_and_filters_unchanged=True,zone_refill='Both GND zones regenerated after local pad/track and mask changes; not byte-identical fill artwork.'))
    holes=collections.Counter()
    for f in b.GetFootprints():
        for q in f.Pads():
            if q.GetDrillSize().x:holes[('NPTH'if q.GetAttribute()==p.PAD_ATTRIB_NPTH else'PTH',mm(q.GetDrillSize().x))]+=1
    for t in b.GetTracks():
        if isinstance(t,p.PCB_VIA):holes[('PTH',mm(t.GetDrill()))]+=1
    models={f.GetReference():[m.m_Filename for m in f.Models()]for f in b.GetFootprints()if len(f.Models())}
    dump('mechanical-stackup.json',dict(revision='M3B-E2',size_mm=[210,160],thickness_mm=mm(ds.GetBoardThickness()),copper_layers=2,stackup='FR4, 1.6mm nominal, 35um nominal outer copper, ordinary plated through vias. No impedance-control premium. Supplier capability/quote pending.',drill_table=[dict(type=k[0],nominal_mm=k[1],quantity=v)for k,v in sorted(holes.items())],mounting_holes={r:nf[r]['origin_mm']for r in ('H1','H2','H3','H4')},critical_finished_hole_tolerances={'J101':'1.20 +/-0.05mm; maker recommended1.10+/-0.15mm','J502':'0.95 +/-0.05mm; maker PCB hole0.90+0.10/-0mm','Q403':'1.30mm nominal; require >=1.25mm finished, form 2.28mm pitch without body stress','Q402':'1.30mm nominal; require >=1.25mm finished; exact incoming Vishay lead-fit gate'},models=models,model_limit='Local WRL files are our dimensional envelopes, not qualified supplier CAD. IRF610 exact incoming case/lead fit and every connector mating envelope remain inspection gates.',probe_positions='probe-map.csv',physical_tests='NOT_RUN'))
    oldcost=json.loads((R/'docs/M3B_COSTS.json').read_text());cost=json.loads((R/'docs/M3B_E2_COSTS.json').read_text());delta={}
    for pop in ('Full','Fox'):
        delta[pop]=dict(purchased_parts=cost['scopes'][pop]['purchased_parts'],ICs=cost['scopes'][pop]['ICs'],quantities={})
        for n in ('1','6','10','20'):
            a=oldcost['scopes'][pop]['batches'][n];c=cost['scopes'][pop]['batches'][n];assert a['per_board_eur']==c['per_board_eur']
            delta[pop]['quantities'][n]=dict(E1_net_eur=a['per_board_eur'],E2_net_eur=c['per_board_eur'],delta_eur=round(c['per_board_eur']-a['per_board_eur'],3),historical_observation_eur=c['historical_observation_eur'],estimate_eur=c['estimate_eur'])
    dump('cost-delta.json',dict(currency='EUR net; VAT excluded',pricing='Preserved observations/estimates, not new quotes or reservations',populations=delta))
    # Required Gerbers, separate plated/nonplated drill, positions and electrical tests.
    g=D/'gerbers';gers=[q for q in g.iterdir()if q.suffix in ('.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1')];assert len(gers)==9
    for q in gers:assert 'M3B-E2'in q.read_text(),q
    assert (g/'RF80-PTH.drl').exists()and(g/'RF80-NPTH.drl').exists()
    # Independent exported drill coordinate/size inventory versus native holes.
    actual=collections.Counter();expected=collections.Counter()
    for f in b.GetFootprints():
        for pad in f.Pads():
            if pad.GetDrillSize().x:
                kind='NPTH'if pad.GetAttribute()==p.PAD_ATTRIB_NPTH else'PTH';v=pad.GetPosition()
                expected[(kind,mm(pad.GetDrillSize().x),mm(v.x),mm(v.y))]+=1
    for t in b.GetTracks():
        if isinstance(t,p.PCB_VIA):
            v=t.GetPosition();expected[('PTH',mm(t.GetDrill()),mm(v.x),mm(v.y))]+=1
    for q in g.glob('*.drl'):
        txt=q.read_text();assert 'M48'in txt and 'METRIC'in txt and 'M30'in txt;tools={};active=None;kind='NPTH'if'NPTH'in q.name else'PTH'
        for line in txt.splitlines():
            z=re.fullmatch(r'T(\d+)C([\d.]+)',line)
            if z:tools[z[1]]=float(z[2]);continue
            z=re.fullmatch(r'T(\d+)',line)
            if z:active=tools[z[1]];continue
            z=re.fullmatch(r'X([-\d.]+)Y([-\d.]+)',line)
            if z:actual[(kind,active,float(z[1]),-float(z[2]))]+=1
    # KiCad decimal Excellon export quantizes coordinates to .001mm (including
    # truncation at negative/positive half values). Do not compare Python's
    # banker's-rounded positions as if they were the exporter specification.
    assert sum(actual.values())==sum(expected.values())==376
    remaining=actual.copy();max_quantization=0
    for key,n in expected.items():
        for _ in range(n):
            candidates=[k for k,v in remaining.items()if v and k[:2]==key[:2]and max(abs(k[2]-key[2]),abs(k[3]-key[3]))<=.00101]
            assert candidates,('Native drill missing/wrong export',key)
            match=min(candidates,key=lambda k:(k[2]-key[2])**2+(k[3]-key[3])**2);remaining[match]-=1
            max_quantization=max(max_quantization,abs(match[2]-key[2]),abs(match[3]-key[3]))
    assert not any(remaining.values())
    # X2 copper flash and IPC assertions include both corrected devices.
    flashes={};ref=pin=net=None
    for line in (g/'RF80-F_Cu.gtl').read_text().splitlines():
        z=re.fullmatch(r'%TO.P,([^,]+),([^,*]+)(?:,[^*]*)?\*%',line)
        if z:ref,pin=z[1],z[2]
        z=re.fullmatch(r'%TO.N,([^*]+)\*%',line)
        if z:net=z[1]
        if line=='%TD*%':ref=pin=net=None
        z=re.fullmatch(r'X(-?\d+)Y(-?\d+)D03\*',line)
        if z and ref in ('Q403','U311'):flashes[(ref,pin)]=dict(net=net,position_mm=[int(z[1])/1e6,-int(z[2])/1e6])
    assert len(flashes)==6
    for (ref,pin),observed in flashes.items():
        native=nf[ref]['pads'][pin];assert observed['net']==native['net']and observed['position_mm']==native['position_mm'],(ref,pin,'Gerber flash mismatch')
    ipc={}
    for line in (D/'RF80.ipc').read_text().splitlines():
        z=re.match(r'^(?:317|327)(\S+)\s+(Q403|U311)\s+-(\d+)\s',line)
        if z:ipc[(z[2],z[3])]=z[1]
    assert len(ipc)==6 and all(ipc[k]==v['net']for k,v in flashes.items()),'IPC corrected-pin mismatch'
    pos=list(csv.DictReader((D/'RF80-position-full.csv').open()));assert len(pos)==195
    assert any('Q403'in str(x)for x in pos)
    assert 'SHAPE_BASE'in(D/'RF80.ipc').read_text()
    count=0
    for q in (H/'review/M3B-E1').rglob('*'):
        if q.is_file():
            old=subprocess.check_output(['git','show','m3b-e1:'+str(q.relative_to(R))],cwd=R);assert old==q.read_bytes(),q;count+=1
    dump('fabrication-audit.json',dict(status='CAD/export checks PASS; review only',Gerber_layers=len(gers),separate_PTH_NPTH=True,native_drill_positions_and_diameters_verified=sum(actual.values()),maximum_drill_coordinate_quantization_mm=round(max_quantization,6),corrected_pin_copper_flashes_and_IPC={r:{pin:flashes[(r,pin)]for pin in ('1','2','3')}for r in ('Q403','U311')},placement_rows=len(pos),not_in_placement='Remote thermistor TH301 is externally fitted; test pads/nonphysical features excluded. Use population-map.csv for reduced population and staged assembly.',E1_files_preserved_byte_identically=count,tool_versions={'kicad_cli':subprocess.check_output(['kicad-cli','version'],text=True).strip(),'pcbnew':p.GetBuildVersion()},checks='Netlist/664 native pad memberships/DRC enforce electrical parity; all376 drill coordinates/sizes and6 corrected Gerber-X2/IPC pins checked independently; no independent CAM raster/etch simulation.',supplier_quote='PENDING; manufacturing tolerances must be accepted explicitly.'))
    print('PASS E2 coverage/change/manufacturing audit; E1 files unchanged; nine E2 Gerber layers')
def manifest():
    paths=list(D.rglob('*'))+[H/'RF80.kicad_pcb',H/'RF80.kicad_pro',H/'RF80.kicad_sch',H/'RF80.electrical.json',H/'RF80.kicad_dru',H/'ARDF_TX.kicad_sym',H/'sym-lib-table',H/'fp-lib-table']
    paths+=list(H.glob('*.kicad_sch'))+list((H/'ARDF_TX.pretty').glob('*'))+list((H/'3dmodels').glob('*'))+list((R/'docs').glob('M3B_E2*'))+list((R/'tools').glob('m3be2*.py'))
    paths += [R/'tools'/n for n in ('m3b_exports.py','m3b_verify.py','m3b_bom.py','m3b_schematic.py','m3_80m_design.py','m3b_models.py','m3b_power_analysis.py','m3a_r1_logic.py')]
    rows=[]
    for q in sorted(set(paths)):
        if not q.is_file()or q.name in ('SHA256SUMS','file-manifest.json'):continue
        data=q.read_bytes();rows.append(dict(path=str(q.relative_to(R)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    dump('file-manifest.json',dict(revision='M3B-E2',baseline_tag='m3b-e1',date='2026-10-15',classification='ENGINEERING REVIEW ONLY; NOT A MANUFACTURING RELEASE',files=rows))
    (D/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n'for x in rows))
    print('Hashed',len(rows),'review/CAD/library/document files; verify from repository root')
if __name__=='__main__':
    arg=argparse.ArgumentParser();arg.add_argument('--manifest',action='store_true');a=arg.parse_args()
    if a.manifest:manifest()
    else:audit()
