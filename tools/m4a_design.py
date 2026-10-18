#!/usr/bin/python3
"""Derive the separate V1 candidate from frozen E2. Never writes reference CAD.

--derive copies library/models and removes only explicitly classified test pads.
--place starts NEW compact routing input; never run after review without backup.
"""
import argparse,copy,json,math,re,shutil,subprocess
from pathlib import Path
import pcbnew as pcb
from m3_80m_design import parse,dump,child,children,Atom
from m3b_pcb import pt,xy,bbox,intersects
R=Path(__file__).resolve().parents[1];E=R/'hardware/80m';P=E/'production';D=P/'review/M4A-V1'
KEEP={'TP101','TP102','TP103','TP105','TP403','TP414','TP501','TP513','TP703','TP706','TP716','TP717','TP721','TP723'}
SERVICE={'TP104','TP401','TP402','TP450','TP451','TP704','TP708','TP710','TP711','TP712','TP718','TP722'}
REV='M4A-V1';NAME='RF80_V1';MM=pcb.FromMM
def frozen():
    # Check every tracked file in the evaluation project, not merely a tag name.
    names=subprocess.check_output(['git','ls-tree','-r','--name-only','1245023','hardware/80m'],cwd=R,text=True).splitlines()
    for n in names:
        assert (R/n).read_bytes()==subprocess.check_output(['git','show','1245023:'+n],cwd=R),('Frozen E2 changed',n)
    return names
def derive():
    frozen();P.mkdir(exist_ok=True);D.mkdir(parents=True,exist_ok=True)
    m=json.loads((E/'RF80.electrical.json').read_text());removed={x['ref']for x in m['parts']if x['ref'].startswith('TP')and x['ref']not in KEEP}
    features=[]
    for p in m['parts']:
        if p['ref'].startswith('TP'):
            cat='Essential production test access'if p['ref']in KEEP else'Useful optional service access'if p['ref']in SERVICE else'Evaluation-only'
            features.append(dict(reference=p['ref'],net=p['pins']['1'],classification=cat,retained=p['ref']in KEEP,alternative='Existing RF connector'if p['pins']['1']in('RF_NORMAL','RF_FOX')else'Controller connector or accessible component pad'if p['ref']not in KEEP else'Compact local bare pad'))
    for src in E.glob('*.kicad_sch'):
        sch=parse(src.read_text());gone=set();vertices=set()
        for s in children(sch,'symbol'):
            ref=next((x[2]for x in children(s,'property')if x[1]=='Reference'),'')
            if ref in removed:gone.add(id(s));a=child(s,'at');vertices.add((round(float(a[1]),4),round(float(a[2]),4)))
        # Each TP has its own label stub; delete exactly its geometric island.
        wires=children(sch,'wire');again=True
        while again:
            again=False
            for w in wires:
                points=children(child(w,'pts'),'xy');a,b=[(round(float(z[1]),4),round(float(z[2]),4))for z in points]
                if a in vertices or b in vertices:
                    gone.add(id(w))
                    for v in(a,b):
                        if v not in vertices:vertices.add(v);again=True
        for key in('global_label','label','no_connect','junction'):
            for x in children(sch,key):
                a=child(x,'at')
                if a and(round(float(a[1]),4),round(float(a[2]),4))in vertices:gone.add(id(x))
        sch=[x for x in sch if id(x)not in gone]
        tb=child(sch,'title_block');child(tb,'rev')[1]=REV;child(tb,'date')[1]='2026-10-15'
        comment=child(tb,'comment')
        if comment:comment[2]='PRODUCTION-INTENT - NOT RELEASED - NO HARDWARE RESULTS'
        else:tb.append([Atom('comment'),Atom('1'),'PRODUCTION-INTENT - NOT RELEASED - NO HARDWARE RESULTS'])
        for t in children(sch,'text'):
            if 'M3B-E2: REVIEW'in t[1]:t[1]=REV+': PRODUCTION-INTENT - NOT RELEASED / all physical gates NOT_RUN.'
            if src.name=='12_evaluation.kicad_sch':t[1]=t[1].replace('Evaluation','Production test access').replace('evaluation','production test access')
        # Project identity changes; UUID/pin instance paths are deliberately stable.
        def project_name(x):
            if isinstance(x,list):
                if x and x[0]=='project'and x[1]=='RF80':x[1]=NAME
                for y in x:project_name(y)
        project_name(sch)
        dst=NAME+'.kicad_sch'if src.name=='RF80.kicad_sch'else src.name
        (P/dst).write_text(dump(sch)+'\n')
    shutil.copyfile(E/'RF80.kicad_pro',P/(NAME+'.kicad_pro'))
    shutil.copyfile(E/'RF80.kicad_dru',P/(NAME+'.kicad_dru'))
    for n in('ARDF_TX.kicad_sym','sym-lib-table','fp-lib-table','LICENSES.md'):shutil.copyfile(E/n,P/n)
    for n in('ARDF_TX.pretty','3dmodels'):shutil.copytree(E/n,P/n,dirs_exist_ok=True)
    m.update(revision=REV,date='2026-10-15',project=NAME,derived_from=dict(commit='1245023',tag='m3b-e2'),scope='PRODUCTION-INTENT - NOT RELEASED; test-pad-only electrical delta')
    m['parts']=[p for p in m['parts']if p['ref']not in removed]
    (P/(NAME+'.electrical.json')).write_text(json.dumps(m,indent=2)+'\n');(D/'test-feature-disposition.json').write_text(json.dumps(features,indent=2)+'\n')
    print('Derived V1; removed',len(removed),'test pads; retained',len(KEEP),'all non-TP values/parts/nets untouched')

class Compact:
    def __init__(self):
        self.b=pcb.LoadBoard(str(E/'RF80.kicad_pcb'));self.b.SetFileName(str(P/(NAME+'.kicad_pcb')))
        m=json.loads((P/(NAME+'.electrical.json')).read_text());self.parts={p['ref']:p for p in m['parts']if not p['ref'].startswith('#')};self.old={f.GetReference():dict(pos=xy(f.GetPosition()),angle=f.GetOrientationDegrees())for f in self.b.GetFootprints()}
        # Retain old wrappers until save: SWIG must not dereference freed items.
        self.deleted=list(self.b.GetTracks())+list(self.b.Zones())+list(self.b.GetDrawings())
        for x in self.deleted:self.b.Remove(x)
        for f in list(self.b.GetFootprints()):
            if f.GetReference().startswith('TP')and f.GetReference()not in KEEP:self.deleted.append(f);self.b.Remove(f)
        self.f={f.GetReference():f for f in self.b.GetFootprints()};self.occupied=[];self.placed=set()
        for f in self.f.values():
            f.SetLocked(False)
            for x in f.GraphicalItems():
                if isinstance(x,pcb.PCB_TEXT):x.SetVisible(True)
        tb=self.b.GetTitleBlock();tb.SetTitle('RF80 V1 - PRODUCTION-INTENT - NOT RELEASED');tb.SetRevision(REV);tb.SetDate('2026-10-15');tb.SetComment(0,'Electrical derivative of frozen M3B-E2; all physical qualification OPEN');self.b.SetTitleBlock(tb)
        for a,b in [((20,20),(170,20)),((170,20),(170,130)),((170,130),(20,130)),((20,130),(20,20))]:
            s=pcb.PCB_SHAPE();s.SetShape(pcb.SHAPE_T_SEGMENT);s.SetStart(pt(*a));s.SetEnd(pt(*b));s.SetLayer(pcb.Edge_Cuts);s.SetWidth(MM(.05));self.b.Add(s)
        for r,a in zip(('H1','H2','H3','H4'),((25,25),(165,25),(165,125),(25,125))):self.put(r,*a,0,True)
    def put(self,r,x,y,a=0,fixed=False):
        f=self.f[r];f.SetOrientationDegrees(a);found=[]
        for radius in range(0,55):
            steps=[(0,0)]if radius==0 else[(i,radius)for i in range(-radius,radius+1)]+[(i,-radius)for i in range(-radius,radius+1)]+[(radius,i)for i in range(-radius+1,radius)]+[(-radius,i)for i in range(-radius+1,radius)]
            for dx,dy in steps:
                xx,yy=x+dx*.5,y+dy*.5;f.SetPosition(pt(xx,yy));bb=bbox(f,.20)
                if not fixed and(bb[0]<21 or bb[1]<24 or bb[2]>169 or bb[3]>128):continue
                if any(intersects(bb,b)for b in self.occupied):continue
                found.append((dx*dx+dy*dy,xx,yy,bb))
            if found or fixed:break
        if not found:raise RuntimeError(('No safe compact placement',r,x,y,a,bbox(f),[(rr,bbox(self.f[rr],.20))for rr in sorted(self.placed)if intersects(bbox(f,.20),bbox(self.f[rr],.20))]))
        _,x,y,bb=min(found);f.SetPosition(pt(x,y));self.occupied.append(bb);self.placed.add(r)
    def place(self):
        anchors={'J101':(27,55,0),'J301':(81,28,0),'J401':(160,91,90),'J502':(150,122,0),
          'U201':(36,29,0),'U202':(44,39,0),'U203':(65,39,0),'U211':(43,62,0),'U212':(63,62,0),'U221':(43,86,0),'U222':(63,86,0),'U223':(43,109,0),'U224':(67,109,0),
          'U311':(89,73,0),'U312':(93,61,0),'U314':(94,83,0),'U313':(115,50,0),'U301':(98,31,0),'U302':(109,51,0),'U401':(124,36,180),'Q402':(130,27,0),'Q403':(114.56,75,180),
          'T401':(139,41,0),'L410':(130,70,0),'L411':(155,70,0),'U101':(106,93,0),'Y101':(106,86,0),'U501':(116,109,0),'L510':(130,111,0),'L511':(145,111,0)}
        for r,v in anchors.items():self.put(r,*v,True)
        hints={'L301':(109,36,0),'F301':(90,26,0),'D301':(93,26,90),'D302':(80,40,90),'R350':(93,35,90),'C350':(85,42,0),
          'C301':(96,27,0),'C302':(95,35,0),'C303':(100,34,0),'C304':(114,37,0),'C305':(115,42,0),
          'R301':(96,30,90),'R302':(101,39,90),'R303':(96,40,0),'R304':(95,45,0),'Q301':(99,44,0),'R305':(101,46,0),'Q302':(105,45,0),
          'C306':(110,55,90),'R306':(113,54,90),'R307':(107,48,0),'R330':(115,46,0),'R331':(114,51,90),'R332':(119,51,90),'C320':(117,54,0),
          'R410':(116,37,0),'C404':(119,29,0),'C401':(127,36,0),'C402':(122,40,0),'R403':(130,31,90),'R404':(125,27,0),'R401':(121,34,90),'Q401':(120,45,0),'Q405':(124,48,0),'R409':(125,45,0),'R402':(117,44,0),'R408':(128,48,0),
          'C405':(133,48,90),'Q404':(107,81,0),'R406':(106,75,90),'R405':(119,70,90),'C403':(121,76,0),'R407':(120,80,0),'TH301':(145,26,0),
          'C410':(150,54,90),'C411':(124,62,0),'C412':(124,66,0),'C413':(144,79,90),'C414':(147,56,0),'C415':(159,77,0),'C416':(163,79,90),
          'R451':(78,52,0),'D451':(82,56,0),'R452':(86,52,0),'C451':(82,51,0),'R453':(84,59,0),'Q406':(78,63,0),
          'Q225':(79,103,0),'Q226':(85,103,0),'Q227':(79,113,0),'Q228':(85,113,0),'Q229':(88,109,0),
          'R501':(96,104,90),'Q501':(100,110,0),'R502':(96,109,0),'R503':(96,115,0),'Q502':(95,120,0),'C501':(102,114,0),'C502':(105,114,90),'R504':(107,116,0),
          'R505':(102,101,0),'R506':(106,103,90),'Q503':(108,106,0),'R507':(111,104,0),'D501':(110,110,0),'R508':(113,119,0),'Q504':(119,122,0),'R509':(122,122,0),
          'R510':(110,109,0),'R511':(110,112,0),'R512':(110,115,0),'C510':(123,111,90),'C511':(126,115,90),'C512':(126,118,90),'C513':(138,117,90),'C514':(147,104,0),'C515':(153,115,90),'C516':(155,118,90),'R513':(145,122,90),'R514':(147,119,90),'R515':(159,122,90),'R516':(158,126,0),'C517':(158,119,90)}
        bypass={'C101':'U101','C102':'U101','C103':'J101','C210':'U201','C211':'U202','C212':'U203','C220':'U211','C222':'U212','C230':'U221','C231':'U222','C232':'U223','C233':'U224','C313':'U312','C323':'U314','C322':'U313'}
        for r,parent in bypass.items():
            p=next((p for p in self.f[parent].Pads()if p.GetNetname()=='V3V3'),None)
            if p:
                x,y=xy(p.GetPosition());hints.setdefault(r,(x+2.5,y,0))
        for r,v in hints.items():self.put(r,*v)
        nonglobal={'V3V3','GND','VIN_PA','VIN_PACK','VPA','VPA_LOAD','VREF_2V5'}
        for r,p in self.parts.items():
            if r in self.placed or r.startswith('TP'):continue
            ns=set(p['pins'].values())-nonglobal-{None};locations=[]
            for rr in sorted(self.placed):
                if rr not in self.parts:continue
                if self.parts[rr]['sheet']!=p['sheet']and not rr.startswith('U'):continue
                locations.extend(xy(pad.GetPosition())for pad in self.f[rr].Pads()if pad.GetNetname()in ns)
            if locations:x=sum(q[0]for q in locations)/len(locations);y=sum(q[1]for q in locations)/len(locations)
            else:x,y=80,70
            self.put(r,round(x,1),round(y,1))
        priorities={'V3V3':'J101','CLK_PA':'U401','CLK_FOX':'U101','VPA_SHAPED':'Q403','VPA':'U302','VDRV':'U401','ARMED':'U223','RESET_N':'U223','LEASE_OK':'U202','PA_GUARD_RAW':'U312','VFOX':'U501'}
        for r in sorted(KEEP):
            n=self.parts[r]['pins']['1'];rr=priorities.get(n)
            if n=='GND':x,y={'TP105':(34,83),'TP414':(127,57),'TP513':(120,116)}[r]
            else:
                pad=next(p for p in self.f[rr].Pads()if p.GetNetname()==n);x,y=xy(pad.GetPosition());x+=2;y+=2
            self.put(r,x,y)
        self.b.BuildConnectivity();pcb.SaveBoard(str(P/(NAME+'.kicad_pcb')),self.b)
        (D/'placement-plan.json').write_text(json.dumps({r:dict(position_mm=xy(f.GetPosition()),angle_deg=f.GetOrientationDegrees())for r,f in self.f.items()},indent=2)+'\n')
        print('Placed',len(self.f),'footprints,150x110mm; retained all non-TP hardware')
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--derive',action='store_true');ap.add_argument('--place',action='store_true');a=ap.parse_args()
    if a.derive:derive()
    if a.place:Compact().place()
