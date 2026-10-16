#!/usr/bin/python3
"""One deterministic RF2M evaluation placement, protected RF copper, offline routing.
Run with system Python/KiCad10. Does not touch RF80 or send data anywhere.
"""
import argparse,json,math,statistics,re,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as pcb
from m5b_footprints import width50
P=Path(__file__).resolve().parents[1]/'hardware/2m';D=P/'review/M5B-E1';MM=pcb.FromMM

def pt(x,y):return pcb.VECTOR2I(MM(x),MM(y))
def xy(p):return(pcb.ToMM(p.x),pcb.ToMM(p.y))
def box(f,gap=.3):
    b=f.GetBoundingBox(False,False);return [pcb.ToMM(b.GetLeft())-gap,pcb.ToMM(b.GetTop())-gap,pcb.ToMM(b.GetRight())+gap,pcb.ToMM(b.GetBottom())+gap]
def overlap(a,b):return a[0]<b[2]and a[2]>b[0]and a[1]<b[3]and a[3]>b[1]

class Board:
    def __init__(self,load=False):
        self.m=json.loads((P/'RF2M.electrical.json').read_text());self.parts={p['ref']:p for p in self.m['parts']if not p['ref'].startswith('#')}
        self.manual=[];self.placed=set();self.occupied=[];self.gvias=[]
        if load:
            self.b=pcb.LoadBoard(str(P/'RF2M.kicad_pcb'));self.f={f.GetReference():f for f in self.b.GetFootprints()};self.nets={pad.GetNetname():pad.GetNet()for f in self.f.values()for pad in f.Pads()if pad.GetNetname()};return
        self.b=pcb.BOARD();self.b.SetFileName(str(P/'RF2M.kicad_pcb'));self.b.SetCopperLayerCount(2);self.b.GetDesignSettings().SetBoardThickness(MM(.8))
        tb=self.b.GetTitleBlock();tb.SetTitle('RF2M 144MHz TRUE-AM INTEGRATED EVALUATION');tb.SetRevision('M5B-E1');tb.SetDate('2026-10-16');tb.SetCompany('ARDF-TX');tb.SetComment(0,'NOT RELEASED / UNBUILT / REVIEW FILES ONLY');self.b.SetTitleBlock(tb)
        tree=ET.parse(D/'RF2M.net.xml');comps={c.get('ref'):c for c in tree.findall('./components/comp')};netpins={};self.nets={}
        for i,n in enumerate(tree.findall('./nets/net'),1):
            name=n.get('name');self.nets[name]=pcb.NETINFO_ITEM(self.b,name,i);self.b.Add(self.nets[name])
            for nd in n.findall('node'):netpins[(nd.get('ref'),nd.get('pin'))]=name
        self.f={}
        for r,p in self.parts.items():
            lib,name=p['footprint'].split(':');folder=P/'ARDF_2M.pretty'if lib=='ARDF_2M'else Path('/usr/share/kicad/footprints')/(lib+'.pretty')
            f=pcb.FootprintLoad(str(folder),name);assert f,(r,p['footprint']);f.SetReference(r);f.SetValue(p['value']);f.SetFPID(pcb.LIB_ID(lib,name))
            c=comps[r];f.SetPath(pcb.KIID_PATH(c.find('sheetpath').get('tstamps')+c.findtext('tstamps')))
            for prop in c.findall('./fields/field'):
                label=prop.get('name');value=prop.text or''
                if label in ['Datasheet','Description']:continue
                fld=pcb.PCB_FIELD(f,pcb.FIELD_T_USER,label);fld.SetText(value);fld.SetVisible(False);f.Add(fld)
            for label,kind in [('Datasheet',pcb.FIELD_T_DATASHEET),('Description',pcb.FIELD_T_DESCRIPTION)]:
                prop=c.find('./fields/field[@name="'+label+'"]');f.GetField(kind).SetText((prop.text or'')if prop is not None else'')
            for pa in f.Pads():
                n=netpins.get((r,pa.GetNumber()))
                if n:pa.SetNet(self.nets[n])
            f.SetDNP(p['population']in ['BUCK4S','TRAIN_ONLY','DNP'])
            f.Reference().SetLayer(pcb.F_Fab);f.Reference().SetTextSize(pt(.8,.8));f.Reference().SetTextThickness(MM(.12));f.Value().SetVisible(False)
            if r.startswith('TL'):f.SetAttributes(f.GetAttributes()|pcb.FP_EXCLUDE_FROM_BOM|pcb.FP_EXCLUDE_FROM_POS_FILES)
            self.b.Add(f);self.f[r]=f
        for a,b in [((20,20),(200,20)),((200,20),(200,160)),((200,160),(20,160)),((20,160),(20,20))]:
            g=pcb.PCB_SHAPE();g.SetShape(pcb.SHAPE_T_SEGMENT);g.SetStart(pt(*a));g.SetEnd(pt(*b));g.SetLayer(pcb.Edge_Cuts);g.SetWidth(MM(.05));self.b.Add(g)
        # Four bench-support holes and two independent grounded PA heat-spreader screws.
        for i,(x,y)in enumerate([(25,25),(195,25),(195,155),(25,155),(112,32),(112,68)],1):
            f=pcb.FootprintLoad('/usr/share/kicad/footprints/MountingHole.pretty','MountingHole_3.2mm_M3');f.SetReference('H'+str(i));f.SetPosition(pt(x,y));f.SetAttributes(pcb.FP_BOARD_ONLY|pcb.FP_EXCLUDE_FROM_BOM|pcb.FP_EXCLUDE_FROM_POS_FILES);self.b.Add(f);self.occupied.append(box(f,.5))
    def pad(self,r,n):return next(p for p in self.f[r].Pads()if p.GetNumber()==str(n))
    def place(self,r,x,y,angle=0,fixed=False):
        f=self.f[r];f.SetOrientationDegrees(angle);f.SetPosition(pt(x,y));bb=box(f)
        if not fixed:
            opts=[]
            for radius in range(0,36):
                dirs=[(0,0)]if radius==0 else [(i,radius)for i in range(-radius,radius+1)]+[(i,-radius)for i in range(-radius,radius+1)]+[(radius,i)for i in range(-radius+1,radius)]+[(-radius,i)for i in range(-radius+1,radius)]
                for dx,dy in dirs:
                    xx=x+dx*.7;yy=y+dy*.7;f.SetPosition(pt(xx,yy));bb=box(f)
                    if bb[0]<28 or bb[1]<28 or bb[2]>192 or bb[3]>151:continue
                    if any(overlap(bb,b)for b in self.occupied):continue
                    # Reserve whole RF strip against unrelated components.
                    if r not in self.rfrefs and overlap(bb,[48,45,188,63]):continue
                    opts.append((dx*dx+dy*dy,xx,yy,bb))
                if opts:break
            if not opts:raise ValueError(('placement exhausted',r,x,y))
            _,x,y,bb=min(opts);f.SetPosition(pt(x,y))
        if not r.startswith('TL'):self.occupied.append(bb)
        self.placed.add(r);return f
    def portplace(self,r,pn,x,y,angle=0):
        f=self.f[r];f.SetOrientationDegrees(angle);f.SetPosition(pt(0,0));px,py=xy(self.pad(r,pn).GetPosition());return self.place(r,x-px,y-py,angle,True)
    def track(self,n,points,width=.25,layer=pcb.F_Cu,locked=True):
        for a,b in zip(points,points[1:]):
            if math.dist(a,b)<.001:continue
            t=pcb.PCB_TRACK(self.b);t.SetStart(pt(*a));t.SetEnd(pt(*b));t.SetWidth(MM(width));t.SetLayer(layer);t.SetNet(self.nets[n]);t.SetLocked(locked);self.b.Add(t)
        self.manual.append(dict(net=n,points=points,width_mm=width,layer=pcb.LayerName(layer)))
    def join(self,r,p,s,q,width=.25,way=()):
        a=self.pad(r,p);b=self.pad(s,q);assert a.GetNetname()==b.GetNetname(),(r,p,s,q);self.track(a.GetNetname(),[xy(a.GetPosition()),*way,xy(b.GetPosition())],width)
    def via(self,n,x,y,d=.6,drill=.3):
        v=pcb.PCB_VIA(self.b);v.SetPosition(pt(x,y));v.SetWidth(MM(d));v.SetDrill(MM(drill));v.SetViaType(pcb.VIATYPE_THROUGH);v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(self.nets[n]);v.SetLocked(True);self.b.Add(v);return v
    def shunt(self,r,node,x,y,side=1,offset=2.6):
        # Signal at x,y; body goes vertically away from RF trace.
        self.portplace(r,'1',x,y-side*offset,90 if side>0 else -90)
        self.track(node,[(x,y),xy(self.pad(r,'1').GetPosition())],.35)
    def place_all(self):
        self.rfrefs={r for r,p in self.parts.items()if p['group']in ['pa','pa_match','output_filter','source_filter','driver','bias']or r.startswith('TL')or r in ['U103','Y101','U601','C941','C101','C102','C103','C635']}
        # Core placement follows ST input and output electrical lengths.
        self.place('Q501',112,55,0,True)
        xg,yg=xy(self.pad('Q501','G').GetPosition());xd,yd=xy(self.pad('Q501','D').GetPosition())
        self.portplace('TL605','2',xg,yg);x,y=xy(self.pad('TL605','1').GetPosition())
        self.portplace('L634','2',x,y);x,y=xy(self.pad('L634','1').GetPosition())
        self.portplace('TL604','2',x,y);xc,yc=xy(self.pad('TL604','2').GetPosition());self.shunt('C633','ST_IS_C',xc,yc,-1)
        x,y=xy(self.pad('TL604','1').GetPosition());self.portplace('C632','2',x,y)
        x,y=xy(self.pad('C632','1').GetPosition());self.portplace('TL603','2',x,y);self.shunt('C631','ST_IS_A',x,y,1)
        x,y=xy(self.pad('TL603','1').GetPosition());self.portplace('R650','2',x,y)
        x,y=xy(self.pad('R650','1').GetPosition());self.portplace('C602','2',x-1.7,y)
        x,y=xy(self.pad('C602','1').GetPosition());self.portplace('U501','3',x-2.,y)
        self.join('U501','3','C602','1',.7)
        self.portplace('R651','1',x+1,y+3.5,-90);self.join('R651','1','C602','2',.25)
        self.portplace('TL606','1',xd,yd);x,y=xy(self.pad('TL606','2').GetPosition());self.shunt('C636','ST_O_A',x,y,-1,3.4)
        self.portplace('TL607','1',x,y);x,y=xy(self.pad('TL607','2').GetPosition());self.shunt('C637','ST_O_B',x,y,-1,3.4)
        self.portplace('L638','1',x,y);x,y=xy(self.pad('L638','2').GetPosition());self.shunt('C638','ST_O_C',x,y,1,3.4)
        self.portplace('TL608','1',x,y);x,y=xy(self.pad('TL608','2').GetPosition());self.portplace('C639','1',x,y)
        x,y=xy(self.pad('C639','2').GetPosition());self.portplace('TL609','1',x,y);x,y=xy(self.pad('TL609','2').GetPosition())
        # Three parallel-resonant series arms; shunts return directly to plane.
        for i in range(3):
            l='L'+str(641+i);c='C'+str(641+i);sh='C'+str(644+i);node=['ST_LPF_IN','ST_F1','ST_F2'][i]
            self.shunt(sh,node,x,y,1)
            self.portplace(l,'1',x+2.2,y);self.track(node,[(x,y),xy(self.pad(l,'1').GetPosition())],width50())
            a,b=xy(self.pad(l,'1').GetPosition()),xy(self.pad(l,'2').GetPosition())
            self.portplace(c,'1',a[0],a[1]+3.,0);self.join(c,'1',l,'1',.4);self.join(c,'2',l,'2',.4)
            x,y=b
        self.shunt('C647','NORMAL_RF',x+2,y,1)
        self.place('J501',185,y,0,True);self.track('NORMAL_RF',[(x,y),(185,y)],width50())
        # Bias and drain feeds attach from opposite sides of the core.
        self.portplace('L606','2',107,46,0);self.join('L606','2','Q501','G',.35,[(107,51),(xg,52.5)])
        self.portplace('L635','2',117,46,180);self.join('L635','2','Q501','D',.5,[(117,50),(xd,52.5)])
        # Simple linear source filter / fixed pad, immediately before MMIC input.
        xin,yin=xy(self.pad('U501','1').GetPosition())
        for ref in ['C615','R602','L613','L612','L611','C601']:
            self.portplace(ref,'2',xin-2.3,yin);xin,yin=xy(self.pad(ref,'1').GetPosition())
        for ref,node,series,side in [('C614','SRC_FILT','R602',1),('R603','SRC_FILT','R602',-1),('R604','DRIVER_PAD','R602',-1),('C613','61B','L613',1),('C612','61A','L612',-1),('C611','SRC_RF','L611',1)]:
            pn='2'if ref=='R604'else'1';xx,yy=xy(self.pad(series,pn).GetPosition());self.shunt(ref,node,xx,yy,side)
        self.portplace('U601','4',xin-2.0,yin,0)
        anchors={'J101':(30,80,0),'J301':(34,139,0),'J302':(65,117,0),
            'U103':(42,48,0),'Y101':(41,40,0),'U101':(40,61,0),'U102':(42,68,0),
            'U201':(48,83,0),'U208':(42,78,0),'U202':(61,85,0),'U203':(76,85,0),'U204':(91,85,0),'U205':(61,101,0),'U206':(76,101,0),'U207':(91,101,0),
            'U301':(51,122,0),'L301':(51,133,-90),'U302':(76,129,0),'L302':(76,139,90),
            'U304':(44,111,0),'Q401':(154,26,0),'Q402':(148,39,0),'U401':(124,85,0),'U402':(112,85,0),
            'U950':(99,126,0),'U303':(111,129,180),'C409':(110,141,0),'U305':(101,114,0),
            'U801':(124,118,0),'U802':(140,111,0),'U803':(154,111,0),'U804':(128,133,0),
            'U701':(156,134,0),'Q701':(172,140,0),'J701':(190,140,0),'RV501':(93,32,0),'TH801':(168,33,0)}
        for r,(x,y,a)in anchors.items():
            if r not in self.placed:self.place(r,x,y,a,True)
        # Explicit regulator decoupling, power loops and bias auxiliaries.
        hints={'C634':(115,45,90),'C635':(119,39,90),'C607':(104,44,90),'Q502':(101,40,0),'D501':(98,34,90),'R606':(98,38,0),
          'L604':(84,61,90),'C604':(87,63,90),'C603':(90,63,90),'R952':(92,67,0),
          'C950':(96,124,90),'C951':(102,126,90),'R950':(101,130,0),'R951':(100,133,90),
          'C940':(98,115,90),'R940':(101,110,90),'R413':(94,138,90),'C407':(94,131,90),'D309':(117,138,90),
          'C960':(71,133,90),'C961':(47,118,90),'F301':(42,140,0),'Q309':(41,133,0),'Q305':(40,124,0),'D302':(33,129,90),'C301':(35,120,90),'C302':(37,116,90),
          'C303':(50,119,0),'C304':(57,140,90),'C305':(61,145,90),'C401':(76,124,90),'C402':(79,125,0),'C403':(83,129,90),'C404':(87,132,90),
          'Q302':(115,120,0),'R309':(124,125,0),'C306':(128,121,90),'C307':(130,126,90),
          'R505':(153,35,0),'R506':(147,31,0),'R507':(143,42,0),'R508':(143,46,0),'Q403':(139,41,0),'Q404':(139,46,0),
          'R511':(130,77,0),'R512':(130,80,90),'C505':(126,80,0),'C506':(138,33,90),'R513':(138,29,0),
          'R930':(90,95,0),'C931':(96,95,90),'R931':(90,92,0),'D930':(95,92,0),'R932':(98,98,90),
          'C101':(37,70,0),'C102':(47,46,90),'C103':(47,50,90),'C941':(58,58,90)}
        # Each local logic/comparator decoupler sits near the actual power pin.
        for r,u in [('C201','U201'),('C203','U202'),('C204','U203'),('C205','U204'),('C206','U205'),('C207','U206'),('C208','U207'),('C310','U304'),('C507','U401'),('C508','U402'),('C801','U801'),('C802','U802'),('C803','U803')]:
            candidates=[p for p in self.f[u].Pads()if p.GetNetname()=='V3V3'];x,y=xy(candidates[0].GetPosition())if candidates else xy(self.f[u].GetPosition());hints[r]=(x+2.2,y,90)
        for r,(x,y,a)in hints.items():
            if r not in self.placed:self.place(r,x,y,a)
        # Training filter stages laid out in a compact single row on independent corner.
        for r,x,y,a in [('C706',176,139,0),('L721',178,139,0),('L722',181,139,0),('L723',184,139,0),('R711',187,139,0),('C721',176,135,90),('C722',179,135,90),('C723',182,135,90),('C724',185,135,90),('R712',187,135,90),('R713',190,135,90),('C701',156,140,0),('L711',159,140,0),('L712',162,140,0),('L713',165,140,0),('C711',156,144,90),('C712',159,144,90),('C713',162,144,90),('C714',165,144,90)]:
            self.place(r,x,y,a)
        defaults={'01_interface_source':(40,91),'02_interlocks':(53,82),'02_interlocksb1':(70,95),'03_input_power':(46,119),'03_input_powerb1':(118,119),'04_boost_driver_supply':(86,120),'05_am':(121,94),'05_amb1':(135,93),'06_source_driver_bias':(107,36),'08_protection':(142,124),'08_protectionb1':(155,123),'10_enable_detail':(94,90),'12_m5b_qualification':(101,121),'07_training':(168,146),'07_trainingb1':(180,147)}
        globalnets={'GND','V3V3','VCLK','VIN_PROT','VIN_CONV','VMOD','VPA','VREG_RAW','POWER_FAULT_N','VREF2V5','VREF1V0','NORMAL_OFF','CONV_EN'}
        for r,p in self.parts.items():
            if r in self.placed or r.startswith('TP'):continue
            locations=[];ns={n for n in p['pins'].values()if n and n not in globalnets}
            for rr in self.placed:
                if rr.startswith(('TP','TL')):continue
                # Same block or an actual connected IC gets priority.
                if self.parts[rr]['sheet']!=p['sheet']and not rr.startswith('U'):continue
                for pa in self.f[rr].Pads():
                    if pa.GetNetname()in ns:locations.append(xy(pa.GetPosition()))
            x,y=defaults.get(p['sheet'],(132,100))
            if locations:
                x=statistics.median(t[0]for t in locations);y=statistics.median(t[1]for t in locations)
            self.place(r,round(x,1),round(y,1));
        # Compact test pads beside nodes; drain/gate observation never creates long stubs.
        pref={'TP601':('Q501','G'),'TP602':('Q501','D'),'TP603':('TL609','2'),'TP604':('TL603','1'),'TP101':('U103','10'),'TP102':('U103','6'),'TP502':('Q401','2')}
        for r,p in self.parts.items():
            if not r.startswith('TP'):continue
            if r in ['TP601','TP602','TP603','TP604']:
                rr,pn=pref[r];x,y=xy(self.pad(rr,pn).GetPosition());x+=dict(TP601=-1.25,TP602=.95,TP603=-1.021,TP604=.83)[r];self.place(r,x,y,0,True)
                # Dedicated board-feature footprint already has the exact probe size.
                continue
            if r in pref:
                rr,pn=pref[r];x,y=xy(self.pad(rr,pn).GetPosition())
            else:
                ns=p['pins']['1'];pa=next(p for rr in self.placed for p in self.f[rr].Pads()if p.GetNetname()==ns);x,y=xy(pa.GetPosition())
            self.place(r,x,y+3)
        self.b.BuildConnectivity()
        # Preserve an uninterrupted lower RF return and an insulated heat-block
        # contact area. No routing beneath RF traces or the PA ground spreader.
        for layer,rect,tracks,fills in [(pcb.B_Cu,[49,43,190,65],True,False),(pcb.B_Cu,[104,29,120,73],True,False),(pcb.F_Cu,[48,48,190,59],False,True)]:
            z=pcb.ZONE(self.b);z.SetLayer(layer);z.SetIsRuleArea(True);z.SetDoNotAllowTracks(tracks);z.SetDoNotAllowVias(False);z.SetDoNotAllowPads(False);z.SetDoNotAllowFootprints(False);z.SetDoNotAllowZoneFills(fills);o=z.Outline();o.NewOutline()
            x0,y0,x1,y1=rect
            for x,y in [(x0,y0),(x1,y0),(x1,y1),(x0,y1)]:o.Append(MM(x),MM(y))
            self.b.Add(z)
    def grounds(self):
        allpads=[p for f in self.f.values()for p in f.Pads()]
        # Thermal/RF source ground: eight small ordinary PTH vias, bottom tented.
        for dy in [-2.,-1.2,-.4,.4,1.2,2.]:self.via('GND',112,55+dy,d=.6,drill=.3);self.gvias.append((112,55+dy))
        for r,f in self.f.items():
            for pad in f.Pads():
                if pad.GetNetname()!='GND'or pad.GetAttribute()!=pcb.PAD_ATTRIB_SMD:continue
                if r=='Q501':continue
                x,y=xy(pad.GetPosition());best=None
                if r=='U302'and pad.GetNumber()=='6':
                    self.via('GND',x,y+2.4);self.gvias.append((x,y+2.4));self.track('GND',[(x,y),(x,y+2.4)],.25);continue
                if r=='U501'and pad.GetNumber()=='4':
                    for dy in [-.8,.0,.8]:self.via('GND',x,y+dy);self.gvias.append((x,y+dy))
                    continue
                for dist in [.8,1.1,1.4,1.8,2.2]:
                    for dx,dy in [(0,dist),(0,-dist),(dist,0),(-dist,0),(dist,dist),(-dist,-dist),(dist,-dist),(-dist,dist)]:
                        pos=pt(x+dx,y+dy);safe=True
                        for q in allpads:
                            if q.GetNetname()=='GND':continue
                            b=q.GetBoundingBox();b.Inflate(MM(.51))
                            if b.Contains(pos):safe=False;break
                        if safe:best=(x+dx,y+dy);break
                    if best:break
                assert best,('noGNDvia',r,pad.GetNumber())
                near=next((p for p in self.gvias if math.dist(p,best)<.65),None)
                if near:best=near
                else:self.via('GND',*best);self.gvias.append(best)
                self.track('GND',[(x,y),best],.25)
        # Via fence over core section; actual clearance is checked by DRC.
        for x in range(52,187,4):
            for y in [43,65]:
                pos=pt(x,y)
                if any(math.dist((x,y),v)<1. for v in self.gvias):continue
                unsafe=False
                for q in allpads:
                    if q.GetNetname()=='GND':continue
                    bb=q.GetBoundingBox();bb.Inflate(MM(.6))
                    if bb.Contains(pos):unsafe=True;break
                if unsafe:continue
                self.via('GND',x,y);self.gvias.append((x,y))
    def rf_links(self):
        # All RF nets in protected region use nearest-node top copper. This is
        # explicit routing, not an autorouter's interpretation of microstrip.
        ns={'NORMAL_CLOCK_BUF','SRC_RF','61A','61B','SRC_FILT','DRIVER_PAD','DRIVER_IN','MMIC_RF_DC','MMIC_COUPLED','MMIC_AC','ST_IS_A','ST_IS_B','ST_IS_C','ST_IS_D','PA_GATE','PA_DRAIN','ST_O_A','ST_O_B','ST_O_C','ST_O_D','ST_DC_BLOCK','ST_LPF_IN','ST_F1','ST_F2','NORMAL_RF'}
        for n in sorted(ns):
            ps=[p for r,f in self.f.items()for p in f.Pads()if p.GetNetname()==n];seen={0}
            while len(seen)<len(ps):
                _,i,j=min((math.dist(xy(ps[i].GetPosition()),xy(ps[j].GetPosition())),i,j)for i in seen for j in range(len(ps))if j not in seen);seen.add(j)
                a,b=xy(ps[i].GetPosition()),xy(ps[j].GetPosition())
                if math.dist(a,b)<.001:continue
                # Measured copper ports and shunts; only actual route endpoints.
                self.track(n,[a,b],.35 if n not in ['NORMAL_RF']else width50())
    def power_links(self):
        from m3b_pcb import Layout
        for n in ['SW4S','BOOT4S','BOOST_SW','BOOST_BST','BOOST_VCC','XTAL1','XTAL2','CLK_NORMAL','VCLK','VDRV_MMIC','VDRV_RF','VDRV_FILTER','VDRV_PREREG','VDRV_LDO_IN','VMOD','VREG_SWITCH','VREG_RAW','VBOOST','VBUCK','VIN_CONV','VIN_PROT','BAT_FUSED','BAT_RAW','VPA']:
            ps=[p for f in self.f.values()for p in f.Pads()if p.GetNetname()==n];seen={0}
            while len(seen)<len(ps):
                _,i,j=min((math.dist(xy(ps[i].GetPosition()),xy(ps[j].GetPosition())),i,j)for i in seen for j in range(len(ps))if j not in seen);seen.add(j)
                a,b=xy(ps[i].GetPosition()),xy(ps[j].GetPosition());path=None
                widths=[.25]if n.startswith(('XTAL','BOOT','BOOST_BST','VCLK'))else [.75,.5,.3]if n in ['SW4S','BOOST_SW','VMOD','VIN_CONV','VIN_PROT','BAT_FUSED','BAT_RAW','VPA','VBUCK','VBOOST','VREG_SWITCH','VREG_RAW']else [.5,.3,.25]
                for w in widths:
                    path=Layout.route_path(self,n,a,b,w)
                    if path and all(21<=x<=199 and 21<=y<=159 for x,y in path)and(n=='CLK_NORMAL'or not any(48<x<190 and 48<y<59 for x,y in path)):break
                    path=None
                if path:self.track(n,path,w)
                else:print('General route required:',n,flush=True)
            print('Top power/clock tree',n,flush=True)
    def zones(self):
        for layer in [pcb.B_Cu,pcb.F_Cu]:
            z=pcb.ZONE(self.b);z.SetLayer(layer);z.SetNet(self.nets['GND']);z.SetLocalClearance(MM(.25));z.SetThermalReliefGap(MM(.3));z.SetThermalReliefSpokeWidth(MM(.35));z.SetPadConnection(pcb.ZONE_CONNECTION_FULL if layer==pcb.B_Cu else pcb.ZONE_CONNECTION_THERMAL);z.SetMinThickness(MM(.2));z.SetIslandRemovalMode(pcb.ISLAND_REMOVAL_MODE_ALWAYS)
            poly=z.Outline();poly.NewOutline()
            for x,y in [(20.5,20.5),(199.5,20.5),(199.5,159.5),(20.5,159.5)]:poly.Append(int(MM(x)),int(MM(y)))
            self.b.Add(z)
    def save(self):
        ds=self.b.GetDesignSettings();ds.m_NetSettings.GetDefaultNetclass().SetClearance(MM(.15));ds.m_MinClearance=MM(.15);ds.m_CopperEdgeClearance=MM(.5);ds.m_TrackMinWidth=MM(.15);ds.m_ViasMinSize=MM(.6);ds.m_ViasMinAnnularWidth=MM(.15);ds.m_MinThroughDrill=MM(.3);ds.m_HoleClearance=MM(.25);ds.m_HoleToHoleMin=MM(.25)
        pcb.SaveBoard(str(P/'RF2M.kicad_pcb'),self.b)
    def dsn(self):
        self.b.BuildConnectivity()
        # Specctra cannot express a zone-fill-only keepout; omit only that
        # non-routing restriction in the transient DSN, retaining it natively.
        omit=[z for z in self.b.Zones()if z.GetIsRuleArea()and z.GetDoNotAllowZoneFills()and not z.GetDoNotAllowTracks()]
        for z in omit:self.b.Remove(z)
        assert pcb.ExportSpecctraDSN(self.b,str(D/'RF2M.dsn'))
        for z in omit:self.b.Add(z)
        path=D/'RF2M.dsn';s=path.read_text();s=s.replace('(clearance 200)','(clearance 150)').replace('(clearance 50 (type smd_smd))','(clearance 150 (type smd_smd))')
        a=s.index('    (class kicad_default');b=s.index('  (wiring',a);section=s[a:b]
        rails=['VMOD','VPA','VREG_SWITCH','VREG_RAW','VBOOST','VBUCK','VIN_CONV','VIN_PROT','BAT_FUSED','BAT_RAW']
        for n in rails+['GND']:section=re.sub(r'(?<![\w])'+re.escape(n)+r'(?![\w])','',section)
        extra=''
        for cls,ns,w in [('POWER',rails,750),('GROUND',['GND'],300)]:extra+='    (class '+cls+' '+' '.join(ns)+' (circuit(use_via "Via[0-1]_600:300_um"))(rule(width '+str(w)+')(clearance 150)))\n'
        pos=section.rfind('  )');section=section[:pos]+extra+section[pos:];s=s[:a]+section+s[b:]
        # Copper graphics inside net-tie footprints have no Specctra net.
        # Protect their actual line bodies against the general router explicitly.
        import m5a_r1_design as cad
        ds=cad.parse(s.replace('(string_quote ")','(string_quote QUOTE_CHARACTER)'));structure=cad.child(ds,'structure')
        def obstacle(layer,kind,args):structure.append(cad.parse('(keepout "" ('+kind+' '+layer+' '+' '.join(map(str,args))+'))'))
        for ref in [r for r in self.f if r.startswith('TL')]:
            a,b=xy(self.pad(ref,'1').GetPosition()),xy(self.pad(ref,'2').GetPosition());w=width50()/2
            obstacle('F.Cu','rect',[1000*(a[0]+.35),-1000*(a[1]+w),1000*(b[0]-.35),-1000*(b[1]-w)])
        # Ground tails/vias remain protected in the native board; the eventual
        # ground pour, checked by native DRC, connects them. Treat them as copper
        # obstacles in DSN rather than asking the router to build a redundant
        # 200-via ground wire tree across the plane.
        network=cad.child(ds,'network')
        for net in cad.children(network,'net'):
            if net[1]=='GND':net[:]=[net[0],net[1]]
        wiring=cad.child(ds,'wiring')
        for item in list(wiring[1:]):
            nn=cad.child(item,'net')if isinstance(item,list)else None
            if not nn or nn[1]!='GND':continue
            if item[0]=='via':
                x,y=map(float,item[2:4])
                for layer in ['F.Cu','B.Cu']:obstacle(layer,'circle',[600,x,y])
            elif item[0]=='wire':
                pa=cad.child(item,'path');layer=str(pa[1]);w=float(pa[2])/2;coords=list(map(float,pa[3:]));pts=list(zip(coords[::2],coords[1::2]))
                for a,b in zip(pts,pts[1:]):obstacle(layer,'rect',[min(a[0],b[0])-w,min(a[1],b[1])-w,max(a[0],b[0])+w,max(a[1],b[1])+w])
            wiring.remove(item)
        path.write_text(cad.dump(ds).replace('(string_quote QUOTE_CHARACTER)','(string_quote ")')+'\n')
    def imp(self,file):
        for t in list(self.b.GetTracks()):
            if not t.IsLocked():self.b.Remove(t)
        for z in list(self.b.Zones()):
            if not z.GetIsRuleArea():self.b.Remove(z)
        assert pcb.ImportSpecctraSES(self.b,str(file));self.save()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--place',action='store_true');ap.add_argument('--power',action='store_true');ap.add_argument('--dsn',action='store_true');ap.add_argument('--import-session');ap.add_argument('--zones',action='store_true');a=ap.parse_args();b=Board(not a.place)
    if a.place:
        b.place_all();b.grounds();b.rf_links();b.save();(D/'manual-routes.json').write_text(json.dumps(b.manual,indent=2)+'\n')
        (D/'placement.json').write_text(json.dumps({r:dict(position_mm=xy(f.GetPosition()),angle=f.GetOrientationDegrees(),footprint=str(f.GetFPID()))for r,f in b.f.items()},indent=2)+'\n')
    if a.import_session:b.imp(a.import_session)
    if a.power:b.power_links();b.save();(D/'power-routes.json').write_text(json.dumps(b.manual,indent=2)+'\n')
    if a.zones:b.zones();b.save()
    if a.dsn:b.dsn()
if __name__=='__main__':main()
