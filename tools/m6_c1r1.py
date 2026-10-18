#!/usr/bin/python3
"""M6-C1R1 orchestration. Reuse CAD engines, never write historical review data."""
import sys,types,json,hashlib,subprocess,shutil
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1R1'
D.mkdir(exist_ok=True)
def adapted(name,replace=()):
    code=(ROOT/'tools'/(name+'.py')).read_text().replace("review/M6-C1'","review/M6-C1R1'")
    for a,b in replace:code=code.replace(a,b)
    m=types.ModuleType(name+'_r1');m.__file__=str(ROOT/'tools'/(name+'.py'));sys.modules[m.__name__]=m;exec(compile(code,m.__file__,'exec'),m.__dict__)
    for key in ['D','OUT']:
        if key in m.__dict__:assert Path(m.__dict__[key]).resolve()==D.resolve(),(name,key,'historical output path rejected')
    return m
def capture():
    import m6_c1_contracts as contracts
    contracts.OUT=D;contracts.extract()
    repl=[("self.revision='M6-C1 candidate'","self.revision='M6-C1R1 candidate'"),
    ("        return r\n    def boxpart","        if mpn=='BAS116,235':part.update(supplier='Mouser DE indexed observation',supplier_part_number='771-BAS116235',moq=1)\n        if mpn=='BAT54H,115':part.update(supplier='Mouser regional indexed comparator; EU stock recheck required',supplier_part_number='771-BAT54H-T/R',moq=1)\n        return r\n    def boxpart"),
    ("d.r('R3','10k','V3V3','PACK_ID_RAW',bi)","d.add('R3','R','27k',{1:'PACK_ID_EXC',2:'PACK_ID_RAW'},RFP,'RC0603FR-0727KL',bi,cost=.01,note='1%,0.1W; pack-derived ID excitation, no V3V3 connection')\n    d.boxpart('D22','BAS116 ID excitation isolation',{1:'PACK_PROT',2:None,3:'PACK_ID_EXC'},{'1':('A','passive'),'2':('NC','no_connect'),'3':('K','passive')},SOT,'BAS116,235',bi,cost=.13,prices={'1':.224,'10':.13,'20':.13},evidence='OBSERVED_2026-10-18',stock='Mouser771-BAS116235 cut tape MOQ1 indexed58175, unreserved',src='https://assets.nexperia.com/documents/data-sheet/BAS116.pdf',note='Pin1A/3K. Blocks ID fault backfeeding PACK_PROT;80nA maximum leakage at150C/75V.')\n    d.add('R8','R','180k',{1:'PACK_ID_RAW',2:'PACK_ID_SAFE'},RFP,'RC0603FR-07180KL',bi,cost=.01,note='1%,0.1W; limits negative16.8V miswire to below0.1mA')\n    d.add('R9','R','33k',{1:'PACK_ID_SAFE',2:'GND'},RFP,'RC0603FR-0733KL',bi,cost=.01,note='1%,0.1W. Positive fault divider independent of powered rails.')\n    d.r('R19','100k','PACK_ID_ADC','GND',bi)\n    d.add('D23','D_Schottky','BAT54H negative ID clamp',{1:'PACK_ID_SAFE',2:'GND'},'Diode_SMD:D_SOD-123F','BAT54H,115',bi,cost=.12,prices={'1':.20,'10':.12,'20':.12},evidence='ESTIMATE_2026-10-18',stock='Mouser771-BAT54H-T/R regional indexed stock60194..75213, MOQ1; EUR price unquoted, recheck live EU availability',src='https://assets.nexperia.com/documents/data-sheet/BAT54H.pdf',note='Pin1K,2A. Negative miswire clamp; positive protection is resistive, not diode dependent.')"),
    ("5:'PACK_ID_RAW',6:'PACK_ID_ADC'","5:'PACK_ID_SAFE',6:'PACK_ID_ADC'"),
    ("('C25','PACK_ID_RAW')","('C25','PACK_ID_SAFE')"),
    ('Signals remain <=5.5V while VDD absent.','Signal limit3.6V for VDD<1.5V; powered limit min(2*VDD,5.5V). R1 PACK_ID protected independently of rail.'),
    ('calibrated 11dB ADC1.','PACK_ID: calibrated2.5dB ADC1, reject >=930mV; other ADC channels separately qualified'),
    ('M6-C1 UNIVERSAL CONTROLLER / ENGINEERING CANDIDATE','M6-C1R1 UNIVERSAL CONTROLLER / ENGINEERING CANDIDATE')]
    # Preserve project design rules. Capture only refreshes schematic/library/manifest.
    pro=(P/'CTRL.kicad_pro').read_bytes();m=adapted('m6_c1_design',repl);m.build();(P/'CTRL.kicad_pro').write_bytes(pro)
    # Correct the locally generated note, which describes the original ID scheme.
    for f in P.glob('*.kicad_sch'):
        text=f.read_text();text=text.replace('M6-C1 candidate','M6-C1R1 candidate');f.write_text(text)
def sync():
    import pcbnew as p,xml.etree.ElementTree as ET
    b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));f={x.GetReference():x for x in b.GetFootprints()};xml=ET.parse(D/'CTRL.net.xml');cs={x.get('ref'):x for x in xml.findall('./components/comp')};nets={}
    for n in xml.findall('./nets/net'):
        name=n.get('name');ni=b.FindNet(name)
        if not ni:ni=p.NETINFO_ITEM(b,name,b.GetNetCount());b.Add(ni)
        nets[name]=ni
    pins={(nd.get('ref'),nd.get('pin')):n.get('name') for n in xml.findall('./nets/net') for nd in n.findall('node')}
    parts=json.loads((P/'CTRL.electrical.json').read_text())['parts']
    # New parts lie in unused lower-left analog space; established connectors stay fixed.
    positions={'D22':(41,99,90),'R8':(45,115,0),'R9':(49,116.5,0),'R19':(89,54.5,0),'D23':(54,116.5,0)}
    for part in parts:
        r=part['ref']
        if r.startswith('#'):continue
        if r not in f:
            lib,name=part['footprint'].split(':');folder=P/(lib+'.pretty') if lib=='ARDF_CTL' else Path('/usr/share/kicad/footprints')/(lib+'.pretty');fp=p.FootprintLoad(str(folder),name);assert fp;fp.SetReference(r);fp.SetFPID(p.LIB_ID(lib,name));b.Add(fp);f[r]=fp
            x,y,a=positions[r];fp.SetPosition(p.VECTOR2I(p.FromMM(x),p.FromMM(y)));fp.Flip(fp.GetPosition(),False);fp.SetOrientationDegrees(a)
            for g in fp.GraphicalItems():
                if g.GetLayer()==p.F_SilkS:g.SetLayer(p.F_Fab)
        fp=f[r];c=cs[r];fp.SetValue(part['value']);fp.SetPath(p.KIID_PATH(c.find('sheetpath').get('tstamps')+c.findtext('tstamps')));fp.Reference().SetLayer(p.B_Fab if fp.GetLayer()==p.B_Cu else p.F_Fab);fp.Value().SetVisible(False)
        for a in fp.Pads():
            if (r,a.GetNumber()) in pins:a.SetNet(nets[pins[(r,a.GetNumber())]])
        for fld in c.findall('./fields/field'):
            k=fld.get('name');v=fld.text or ''
            if k in ('Datasheet','Description'):fp.GetField(p.FIELD_T_DATASHEET if k=='Datasheet' else p.FIELD_T_DESCRIPTION).SetText(v);continue
            z=next((x for x in fp.GetFields() if x.GetName()==k),None)
            if z is None:z=p.PCB_FIELD(fp,p.FIELD_T_USER,k);fp.Add(z)
            z.SetText(v);z.SetVisible(False)
    # Synchronization changes metadata/pad identities only. Copper remains the
    # reviewed native design; intentional electrical edits require fresh DRC.
    tb=b.GetTitleBlock();tb.SetRevision('M6-C1R1 CANDIDATE');b.SetTitleBlock(tb)
    for z in b.GetDrawings():
        if isinstance(z,p.PCB_TEXT) and z.GetText()=='ARDF-TX M6-C1':z.SetText('ARDF-TX C1R1')
    p.SaveBoard(str(P/'CTRL.kicad_pcb'),b)

def main():
    action=sys.argv[1]
    if action=='capture':capture();return
    if action=='sync':sync();return
    if action=='contracts':
        import m6_c1_contracts as m;m.OUT=D;m.extract()
        for f in D.glob('*interface*'):
            if f.is_file() and f.suffix in ['.json','.csv']:
                f.write_text(f.read_text().replace('TMUX1511 powered-off input limit5.5V','TMUX1511 powered-off input limit3.6V'))
        return
    if action=='verify':
        m=adapted('m6_c1_verify',[("'5':'PACK_ID_RAW','6':'PACK_ID_ADC'","'5':'PACK_ID_SAFE','6':'PACK_ID_ADC'")]);m.main()
        h=ROOT/'firmware/controller_hw/pins.h';h.write_text('/* M6-C1R1: pack-ID decoder must use frontend revision2. */\n#define CTL_HW_REV_M6_C1R1 1\n#define CTL_PACK_ID_FRONTEND_REV 2\n#define CTL_PACK_ID_PULLUP_OHM 27000\n#define CTL_PACK_ID_ADC_ATTEN_MILLI_DB 2500\n#define CTL_PACK_ID_ADC_VALID_MAX_MV 930\n'+h.read_text())
        return
    if action=='route':
        import m6_c1_pcb;m6_c1_pcb.D=D
        sys.argv=[sys.argv[0]]+sys.argv[2:];adapted('m6_c1_route_completion').main();return
    if action=='checks' or action=='exports' or action=='manifest':
        m=adapted('m6_c1_exports',[("if name=='assembly-top':args+=", "if name in ['assembly-bottom','bottom-copper']:args+=['--mirror']\n        if name=='assembly-bottom':args+=['--sketch-pads-on-fab-layers']\n        if name=='assembly-top':args+=")]);sys.argv=[sys.argv[0],action]+sys.argv[2:];m.main()
        if action=='exports':
            cmd=['kicad-cli','pcb','export','pdf','--mode-single','--mirror','--layers','B.Fab,B.Silkscreen,Edge.Cuts','--sketch-pads-on-fab-layers','-o',str(D/'assembly-bottom.pdf'),str(P/'CTRL.kicad_pcb')]
            r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);assert r.returncode==0,r.stderr
            f=D/'export-commands.json';a=json.loads(f.read_text());a.append(dict(command=cmd,returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));f.write_text(json.dumps(a,indent=2)+'\n')
        return
    name={'analysis':'m6_c1_analysis','dfm':'m6_c1_dfm','review':'m6_c1_review','mechanical':'m6_c1_mechanical','protocols':'m6_c1_rf_protocols','powerpaths':'m6_c1_route_audit'}[action]
    replacements=[]
    if action=='review':
        replacements=[("['/usr/bin/python3','-m','unittest','-v','test_model.py']","['/usr/bin/python3','-m','unittest','discover','-s','.','-p','test_*.py','-v']"),('32 Python tests','40 Python tests'),('M6-C1 CANDIDATE','M6-C1R1 CANDIDATE'),('M6-C1 engineering candidate','M6-C1R1 engineering candidate')]
    if action=='dfm':replacements=[("'revision':'M6-C1'","'revision':'M6-C1R1'")]
    m=adapted(name,replacements);m.main()
    if action=='analysis':
        f=D/'power-analysis.json';a=json.loads(f.read_text());a['ADC']['power_off_protection']='TMUX1511 signal0..3.6V for VDD<1.5V; powered0..min(2*VDD,5.5V). R1 input-protection.json supersedes original ID circuit.';f.write_text(json.dumps(a,indent=2)+'\n')
if __name__=='__main__':main()
