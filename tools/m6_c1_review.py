#!/usr/bin/python3
"""Final controller artifact audit and review records. No hardware access.

Run after the commands in REPRODUCE.md; no historical RF files are written.
"""
import collections,csv,hashlib,json,math,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1'
def save(name,value):(D/name).write_text(json.dumps(value,indent=2)+'\n')
def load(name):return json.loads((D/name).read_text())
def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def main():
    cad=load('CAD-results.json')
    assert all(cad[k]==0 for k in ['ERC_violations','DRC_errors','DRC_warnings','unrouted','parity'])
    assert cad['exclusions']==[] and cad['ignored_categories']==['tuning_profile_track_geometries']
    dfm=load('JLCPCB-DFM.json');assert not dfm['errors']
    b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));assert sha(P/'CTRL.kicad_pcb')==dfm['native_sha256']
    fps={f.GetReference():f for f in b.GetFootprints()}
    # Final native rail margin includes copper, a hot switch envelope and harness.
    paths=load('power-native-main-paths.json')['paths'];rail=[]
    for switch,header in [('U40','J4'),('U50','J5')]:
        main=next(x for x in paths if x['from_pin']=='L1.2' and x['to_pin']==switch+'.1')
        branch=next(x for x in paths if x['from_pin']==switch+'.6' and x['to_pin']==header+'.1')
        minimum=3.2505-main['drop_bound_V']-branch['drop_bound_V']-.15*(.088+.08)-.005
        assert minimum>=3.135,(switch,minimum)
        rail.append({'port':header,'regulator_min_V':3.2505,'main_copper_drop_V':main['drop_bound_V'],'port_copper_drop_V':branch['drop_bound_V'],'switch_hot_envelope_ohm':.088,'harness_allowance_ohm':.08,'ground_offset_allowance_V':.005,'connector_min_V_calculated':minimum,'required_min_V':3.135})
    save('connector-rail-budget.json',{'classification':'Calculated native copper and hot-component/harness envelope, not measured rail compliance','source':'TPS22918 datasheet RON table;88mohm worst1.8V/-40..105C,80mohm2.5/3.3V. Use88mohm conservative interval envelope.','ports':rail,'physical':'NOT_RUN; verify rail at150mA and additional ground offset<=5mV'})
    usb=collections.defaultdict(lambda:dict(length_mm=0,via_count=0,width_mm=set()))
    for t in b.GetTracks():
        n=t.GetNetname()
        if n.startswith('USB_') and ('DP' in n or 'DM' in n):
            if isinstance(t,p.PCB_VIA):usb[n]['via_count']+=1
            else:usb[n]['length_mm']+=p.ToMM(t.GetLength());usb[n]['width_mm'].add(p.ToMM(t.GetWidth()))
    for z in usb.values():z['width_mm']=sorted(z['width_mm'])
    save('USB-native-routing.json',{'classification':'Native geometry, not a USB eye measurement','signals':dict(usb),'assessment':'Full-speed12Mb/s only; approximately30mm data paths. No claimed controlled90ohm impedance on1.6mm FR4. Series22ohm damping, ESD, attach/eye/EMI qualification required. No480Mb/s support.','physical':'NOT_RUN'})
    # Rebuild unambiguous short test-net names from actual native pad/via nets.
    # KiCad's raw IPC truncates long names, so it is evidence, not the E-test map.
    raw=(D/'CTRL-KiCad.ipc').read_text().splitlines()
    nets=sorted({a.GetNetname() for f in fps.values() for a in f.Pads() if a.GetNetname()})
    aliases={n:'N'+str(i+1).zfill(5) for i,n in enumerate(nets)}
    pads={};vias=[]
    for f in fps.values():
        for a in f.Pads():
            if a.GetNumber():pads.setdefault((f.GetReference(),a.GetNumber()),[]).append(a)
    for t in b.GetTracks():
        if isinstance(t,p.PCB_VIA):vias.append(t)
    result=[];counts=collections.Counter();seen=set()
    for line in raw:
        if line[:3] not in ['317','327','367']:result.append(line);continue
        pos=re.search(r'X([+-]\d+)Y([+-]\d+)',line[35:]);assert pos,line
        x,y=int(pos[1])*.00254,-int(pos[2])*.00254
        ref=line[20:26].strip();pin=line[27:31].strip()
        if ref=='VIA':
            candidates=vias
        else:
            candidates=pads.get((ref,pin),[])
            if not pin:result.append(line);counts['NPTH']+=1;continue
        assert candidates,(ref,pin,line)
        obj=min(candidates,key=lambda a:math.hypot(p.ToMM(a.GetPosition().x)-x,p.ToMM(a.GetPosition().y)-y))
        assert math.hypot(p.ToMM(obj.GetPosition().x)-x,p.ToMM(obj.GetPosition().y)-y)<.003,(ref,pin,x,y)
        n=obj.GetNetname();short=aliases[n] if n else 'N/C'
        result.append(line[:3]+short.ljust(14)+line[17:]);counts['vias' if ref=='VIA' else 'pads']+=1
        if ref!='VIA':seen.add((ref,pin))
    assert counts['vias']==len(vias)
    assert counts['pads']==sum(len(a) for a in pads.values())
    physical='\n'.join(result)+'\n'
    (D/'CTRL-physical.ipc').write_text(physical)
    (D/'CTRL-logical.ipc').write_text(physical)
    save('electrical-test-net-aliases.json',{'classification':'Native pad/via-derived unique IPC names; no intentional net ties on controller','full_to_short':aliases,'records_verified':dict(counts),'logical_and_physical_connectivity':'identical; raw KiCad IPC retained to expose name truncation','physical_tests':'NOT_RUN'})
    # Verify exported drill dimensions/counts against native holes, including slots.
    expected=collections.defaultdict(collections.Counter)
    for t in vias:expected['PTH'][round(p.ToMM(t.GetDrillValue()),3)]+=1
    for f in fps.values():
        for a in f.Pads():
            d=a.GetDrillSize()
            if d.x and d.y:expected['NPTH' if a.GetAttribute()==p.PAD_ATTRIB_NPTH else 'PTH'][round(p.ToMM(min(d.x,d.y)),3)]+=1
    drills={}
    for kind in ['PTH','NPTH']:
        text=(D/'fabrication'/('CTRL-'+kind+'.drl')).read_text();tools={};active=None;actual=collections.Counter()
        assert ('NonPlated' if kind=='NPTH' else 'Plated') in text
        for line in text.splitlines():
            m=re.fullmatch(r'T(\d+)C([\d.]+)',line)
            if m:tools[m[1]]=float(m[2]);continue
            m=re.fullmatch(r'T(\d+)',line)
            if m:active=m[1];continue
            if line.startswith('X'):actual[tools[active]]+=1
        assert actual==expected[kind],(kind,actual,expected[kind]);drills[kind]=dict(actual)
    g=D/'fabrication';job=load('fabrication/CTRL-job.gbrjob');assert job['GeneralSpecs']['BoardThickness']==1.6 and job['GeneralSpecs']['LayerNumber']==2
    files=[f for f in g.iterdir() if f.suffix in ['.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1']]
    assert len(files)==9
    functions=[]
    for f in files:
        text=f.read_text();assert '%FSLAX46Y46*%' in text and '%MOMM*%' in text and 'M02*' in text
        assert 'M6-C1 CANDIDATE' in text
        functions.append({'file':f.name,'function':re.search(r'%TF.FileFunction,(.*?)\*%',text)[1],'sha256':sha(f)})
    edge=(g/'CTRL-Edge_Cuts.gm1').read_text();pts=re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',edge)
    assert {int(x) for x,y in pts}=={20000000,120000000}
    assert {int(y) for x,y in pts}=={-20000000,-120000000}
    placements={}
    variants=load('population-variants.json')
    parts=json.loads((P/'CTRL.electrical.json').read_text())['parts'];partmap={z['ref']:z for z in parts}
    for variant in ['FOX_MIN','RF80_FULL','RF2M_FULL','UNIVERSAL']:
        rows=list(csv.DictReader((D/('placement-'+variant+'.csv')).open()))
        refs={row.get('Ref',row.get('Reference','')) for row in rows}
        assert set(variants[variant]['fitted'])<=refs,(variant,set(variants[variant]['fitted'])-refs)
        assert not refs.intersection(variants[variant]['DNP']),variant
        placements[variant]={'placed':len(refs),'fitted_purchased':len(variants[variant]['fitted']),'note':'copper test pads are excluded from purchased BOM and placement export'}
    # All packages are inventoried; OPEN optional footprints cannot become base parts.
    packages=[]
    for f in fps.values():
        r=f.GetReference();part=partmap.get(r,{})
        packages.append({'ref':r,'MPN':part.get('mpn','PCB mounting feature'),'landing':f.GetFPIDAsString(),'rotation_degrees':f.GetOrientationDegrees(),'source':part.get('source_url','stock KiCad mechanical footprint'),'population':part.get('population','BOARD_ONLY'),'status':'OPEN_OPTION_DO_NOT_POPULATE' if r=='U70' else 'CAD_LANDING_SELECTED_PHYSICAL_FIT_NOT_RUN','pads':[{'number':a.GetNumber(),'net':a.GetNetname(),'at_mm':[p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)],'size_mm':[p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)],'hole_mm':[p.ToMM(a.GetDrillSize().x),p.ToMM(a.GetDrillSize().y)]} for a in f.Pads()]})
    save('package-and-pad-audit.json',{'classification':'Native landing geometry and manufacturer source register; independent electrical assertions separately recorded','packages':packages,'manual_checks':'Actual component fit, stencil release, HASL flatness, backup-cell pressure and insulation NOT_RUN; optional U70 drawing/order suffix unresolved'})
    save('artifact-audit.json',{'status':'PASS_LOCAL_EXPORT_CONSISTENCY','board_sha256':sha(P/'CTRL.kicad_pcb'),'Gerbers':functions,'drill_counts_by_diameter_mm':drills,'native_IPC_records':dict(counts),'placement_populations':placements,'outline_centerline_mm':[100,100],'gbrjob_bbox_mm':[100.05,100.05],'bbox_note':'job includes0.05mm Edge.Cuts stroke; route centerline is100.00mm square','factory_CAM':'NOT_SUBMITTED','physical_tests':'NOT_RUN'})
    # Repeat host tests, preserving real commands/output and status.
    fw=ROOT/'firmware/controller_hw';runs=[]
    for cmd in [['/usr/bin/python3','-m','unittest','-v','test_model.py'],['cc','-std=c11','-Wall','-Wextra','-Werror','contract.c','test_contract.c','-lm','-o','/tmp/m6-c1-contract'],['/tmp/m6-c1-contract']]:
        r=subprocess.run(cmd,cwd=fw,capture_output=True,text=True);runs.append({'command':cmd,'exit_code':r.returncode,'stdout':r.stdout,'stderr':r.stderr});assert r.returncode==0
    save('host-test-results.json',{'status':'PASS','classification':'host simulation/compilation; no target firmware or electrical measurements','commands':runs})
    save('final-checks.json',{'revision':'M6-C1 engineering candidate, no acceptance tag','KiCad':cad,'native_DFM':dfm['status'],'electrical':load('electrical-regression.json'),'RF80_read_only_regression':load('RF80-protocol-regression.json'),'RF2M_read_only_regression':load('RF2M-protocol-regression.json'),'DFM_mutations':load('DFM-regression.json'),'host_tests':'32 Python tests plus strict C waveform/GPIO fixture','artifact_consistency':'PASS','LoRa_population':'HOLD: exact ZTR8/TR8 identity, manufacturer land tolerance and RF launch not qualified','physical_qualification':'NOT_RUN','manufacturing_release':'NOT_AUTHORIZED'})
    print('Artifacts, unique electrical-test nets, packages, drill/placement and host tests: PASS')
if __name__=='__main__':main()
