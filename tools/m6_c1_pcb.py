#!/usr/bin/python3
"""100x100mm controller placement, protected local loops, offline DSN/SES."""
import argparse,json,math,statistics,re,xml.etree.ElementTree as ET
from pathlib import Path
import pcbnew as pcb
from m5_2m_design import parse,dump,child,children
P=Path(__file__).resolve().parents[1]/'hardware/controller';D=P/'review/M6-C1';MM=pcb.FromMM
def pt(x,y):return pcb.VECTOR2I(MM(x),MM(y))
def xy(p):return pcb.ToMM(p.x),pcb.ToMM(p.y)
def bounds(f,g=.25):
    # Antenna rule areas extend well beyond the module body. They are separate
    # placement constraints, not a rectangular body that pushes decouplers away.
    boxes=[v.GetBoundingBox() for v in f.GraphicalItems() if v.GetLayer() in [pcb.F_CrtYd,pcb.B_CrtYd]]
    if boxes:return [min(pcb.ToMM(v.GetLeft()) for v in boxes)-g,min(pcb.ToMM(v.GetTop()) for v in boxes)-g,max(pcb.ToMM(v.GetRight()) for v in boxes)+g,max(pcb.ToMM(v.GetBottom()) for v in boxes)+g]
    b=f.GetBoundingBox(False,False);return [pcb.ToMM(b.GetLeft())-g,pcb.ToMM(b.GetTop())-g,pcb.ToMM(b.GetRight())+g,pcb.ToMM(b.GetBottom())+g]
def overlap(a,b):return a[0]<b[2] and a[2]>b[0] and a[1]<b[3] and a[3]>b[1]
class Board:
    def __init__(self,load=False):
        self.parts={p['ref']:p for p in json.loads((P/'CTRL.electrical.json').read_text())['parts'] if not p['ref'].startswith('#')};self.occupied=[];self.placed=set();self.manual=[]
        if load:
            self.b=pcb.LoadBoard(str(P/'CTRL.kicad_pcb'));self.f={f.GetReference():f for f in self.b.GetFootprints()};self.nets={p.GetNetname():p.GetNet() for f in self.f.values() for p in f.Pads() if p.GetNetname()};return
        self.b=pcb.BOARD();self.b.SetFileName(str(P/'CTRL.kicad_pcb'));self.b.SetCopperLayerCount(2);self.b.GetDesignSettings().SetBoardThickness(MM(1.6))
        tb=self.b.GetTitleBlock();tb.SetTitle('ARDF-TX UNIVERSAL CONTROLLER');tb.SetRevision('M6-C1 CANDIDATE');tb.SetDate('2026-10-18');tb.SetCompany('ARDF-TX');tb.SetComment(0,'ENGINEERING REVIEW ONLY / PHYSICAL TESTS NOT_RUN');self.b.SetTitleBlock(tb)
        xml=ET.parse(D/'CTRL.net.xml');comps={c.get('ref'):c for c in xml.findall('./components/comp')};netpins={};self.nets={}
        for i,n in enumerate(xml.findall('./nets/net'),1):
            self.nets[n.get('name')]=pcb.NETINFO_ITEM(self.b,n.get('name'),i);self.b.Add(self.nets[n.get('name')])
            for nd in n.findall('node'):netpins[(nd.get('ref'),nd.get('pin'))]=n.get('name')
        self.f={}
        for r,p in self.parts.items():
            lib,name=p['footprint'].split(':');folder=P/'ARDF_CTL.pretty' if lib=='ARDF_CTL' else Path('/usr/share/kicad/footprints')/(lib+'.pretty');f=pcb.FootprintLoad(str(folder),name);assert f,(r,p['footprint']);f.SetReference(r);f.SetValue(p['value']);f.SetFPID(pcb.LIB_ID(lib,name));c=comps[r];f.SetPath(pcb.KIID_PATH(c.find('sheetpath').get('tstamps')+c.findtext('tstamps')))
            for field in c.findall('./fields/field'):
                label=field.get('name');value=field.text or ''
                if label in ['Datasheet','Description']:continue
                prop=pcb.PCB_FIELD(f,pcb.FIELD_T_USER,label);prop.SetText(value);prop.SetVisible(False);f.Add(prop)
            for label,kind in [('Datasheet',pcb.FIELD_T_DATASHEET),('Description',pcb.FIELD_T_DESCRIPTION)]:
                fld=c.find('./fields/field[@name="'+label+'"]');f.GetField(kind).SetText(fld.text or '' if fld is not None else '')
            for pad in f.Pads():
                net=netpins.get((r,pad.GetNumber()))
                if net:pad.SetNet(self.nets[net])
            f.SetDNP(p['population'] in ['DEBUG','LORA_OPTION_OPEN']);f.Reference().SetLayer(pcb.F_Fab);f.Reference().SetVisible(True);f.Value().SetVisible(False)
            self.b.Add(f);self.f[r]=f
        for a,b in [((20,20),(120,20)),((120,20),(120,120)),((120,120),(20,120)),((20,120),(20,20))]:
            g=pcb.PCB_SHAPE(self.b);g.SetShape(pcb.SHAPE_T_SEGMENT);g.SetStart(pt(*a));g.SetEnd(pt(*b));g.SetLayer(pcb.Edge_Cuts);g.SetWidth(MM(.05));self.b.Add(g)
        for i,(x,y) in enumerate([(25,62),(115,25),(115,115),(25,115)],1):
            f=pcb.FootprintLoad('/usr/share/kicad/footprints/MountingHole.pretty','MountingHole_3.2mm_M3');f.SetReference('H'+str(i));f.SetPosition(pt(x,y));f.SetAttributes(pcb.FP_BOARD_ONLY|pcb.FP_EXCLUDE_FROM_BOM|pcb.FP_EXCLUDE_FROM_POS_FILES);f.Reference().SetLayer(pcb.F_Fab);f.Value().SetVisible(False);self.b.Add(f);self.occupied.append(bounds(f,.5))
    def pad(self,r,n):return next(p for p in self.f[r].Pads() if p.GetNumber()==str(n))
    def place(self,r,x,y,angle=0,fixed=False):
        f=self.f[r];f.SetOrientationDegrees(angle)
        for radius in range(0,55):
            opts=[(0,0)] if radius==0 else [(i,radius) for i in range(-radius,radius+1)]+[(i,-radius) for i in range(-radius,radius+1)]+[(radius,i) for i in range(-radius+1,radius)]+[(-radius,i) for i in range(-radius+1,radius)]
            good=[]
            for dx,dy in opts:
                xx=x+dx*.6;yy=y+dy*.6;f.SetPosition(pt(xx,yy));bb=bounds(f)
                if fixed:good=[(0,xx,yy,bb)];break
                if bb[0]<21 or bb[1]<21 or bb[2]>119 or bb[3]>119:continue
                if overlap(bb,[26,0,74,28.5]):continue
                if any(overlap(bb,b) for b in self.occupied):continue
                good.append((dx*dx+dy*dy,xx,yy,bb))
            if good:break
        if not good:raise ValueError(('Placement exhausted',r))
        _,x,y,bb=min(good);f.SetPosition(pt(x,y));self.occupied.append(bb);self.placed.add(r)
    def track(self,net,pts,width=.2,layer=pcb.F_Cu):
        for a,b in zip(pts,pts[1:]):
            if math.dist(a,b)<.001:continue
            t=pcb.PCB_TRACK(self.b);t.SetStart(pt(*a));t.SetEnd(pt(*b));t.SetWidth(MM(width));t.SetLayer(layer);t.SetNet(self.nets[net]);t.SetLocked(True);self.b.Add(t)
        self.manual.append(dict(net=net,points=pts,width_mm=width,layer=pcb.LayerName(layer)))
    def join(self,r,p,s,q,w=.2):
        a=self.pad(r,p);b=self.pad(s,q);assert a.GetNetname()==b.GetNetname();self.track(a.GetNetname(),[xy(a.GetPosition()),xy(b.GetPosition())],w)
    def place_all(self):
        anchors={'U10':(50,35,0),'J2':(23.675,40,-90),'U3':(32,40,0),'R14':(36,46.4,0),'R15':(36,44.8,0),
        'C20':(38,31,180),'C21':(38,33,180),'U4':(61,52,0),'R16':(63,49.5,0),'C12':(65,52,0),
        'J4':(27,76,0),'J5':(109,76,0),'U40':(39,66,0),'U41':(48,75,0),'U42':(46,94,0),'U43':(42,57,0),
        'U50':(101,65,0),'U51':(92,76,0),'U52':(92,95,0),'U53':(98,57,0),
        'U30':(61,63,0),'U31':(77,63,0),'U20':(73,46,0),'U21':(78,55,0),'BT1':(78,110,0),
        'U32':(55,91,0),'U33':(61,91,0),'U34':(67,91,0),'U35':(66,81,0),'U36':(73,91,0),'U37':(78,81,0),'U60':(62,49,0),
        'J1':(39,113,0),'U1':(48,107,0),'L1':(54,110,0),'C1':(52,105.7,0),'C2':(40.5,106,90),'C3':(43.25,108,180),'C4':(59.5,109,90),'C5':(64,109,90),'C6':(48,102,0),
        'C24':(72,53.7,180),'C25':(72,56.6,180),'C26':(84,56.3,0),'C27':(84,53.5,0),
        'D1':(32,107,90),'D4':(38,97,0),'D2':(39,103,90),'D3':(35,59,90),'F1':(32,113,0),'U2':(28,49,90),
        'SW1':(26,53,0),'SW2':(36,54,0),'SW3':(94,112,0),'SW4':(105,110,0),
        'U70':(103,41,0),'J7':(99.415,28.5,0),'C70':(111.5,32,90),'C71':(115.5,34,90)}
        fixed={'U10','J1','J2','J4','J5','U70','J7','R14','R15','U1','L1','C1','C3','C4','C5','C20','C21','U3','U20','U21','C24','C25','C26','C27','SW1','SW2','SW3','SW4'}
        for r,(x,y,a) in sorted(anchors.items(),key=lambda item:item[0] not in fixed):self.place(r,x,y,a,r in fixed)
        bypass={'C10':('U2','1'),'C11':('U2','1'),'C22':('U20','1'),'C23':('U20','6'),'C28':('U21','14'),
        'C30':('U30','16'),'C31':('U31','16'),'C32':('U32','5'),'C33':('U33','5'),'C34':('U34','6'),'C35':('U35','14'),'C36':('U36','5'),'C37':('U37','14'),
        'C40':('U40','1'),'C41':('U40','6'),'C42':('U41','20'),'C43':('U42','14'),'C44':('U43','8'),'C45':('U43','1'),
        'C50':('U50','1'),'C51':('U50','6'),'C52':('U51','20'),'C53':('U52','14'),'C54':('U53','8'),'C55':('U53','1'),'C60':('U60','6')}
        for r,(u,pn) in bypass.items():
            if r in self.placed:continue
            x,y=xy(self.pad(u,pn).GetPosition());cx,cy=xy(self.f[u].GetPosition());side=1 if x>=cx else -1
            self.place(r,x+side*2.5,y,0 if side>0 else 180)
        common={'GND','V3V3','V3V3_RF80','V3V3_RF2M'}
        defaults={'01_power':(46,109),'02_USB_reset':(32,44),'03_MCU':(54,47),'04_RTC_analog':(80,49),'05_static_safety':(68,84),'06_RF80':(40,83),'07_RF2M':(99,86),'08_status':(64,50),'09_LoRa':(102,53),'10_test':(63,105)}
        for r,p in self.parts.items():
            if r in self.placed or r.startswith('TP'):continue
            ns=set(p['pins'].values())-common-{None};locations=[]
            for rr in self.placed:
                if not rr.startswith('U'):continue
                for pad in self.f[rr].Pads():
                    if pad.GetNetname() in ns:locations.append(xy(pad.GetPosition()))
            x,y=defaults.get(p['group'],(68,85))
            if locations:x=statistics.median(a[0] for a in locations);y=statistics.median(a[1] for a in locations)
            self.place(r,x,y,90 if r.startswith('C') else 0)
        for i,r in enumerate(sorted(r for r in self.parts if r.startswith('TP'))):self.place(r,63+i*3,117,0)
        # Keep the source-to-connector USB path short at full speed, not high-speed USB.
        # Only the local series termination segments are fixed initially; router handles pair fanout.
        self.join('R14','2','U10','14',.2);self.join('R15','2','U10','13',.2)
        # Explicit short boot capacitor and switch-node connections, fixed prior to autoroute.
        self.join('U1','6','C1','1',.25)
        sw=xy(self.pad('U1','5').GetPosition());self.track('BUCK_SW',[sw,(51,sw[1]),xy(self.pad('L1','1').GetPosition())],.5)
        self.join('L1','2','C4','1',.5);self.join('C4','1','C5','1',.5)
        # Small LoRa output launch to nearby U.FL; optional module package remains OPEN.
        self.join('U70','21','J7','1',.45)
    def save(self):
        ds=self.b.GetDesignSettings();nc=ds.m_NetSettings.GetDefaultNetclass();nc.SetClearance(MM(.15));nc.SetTrackWidth(MM(.2));nc.SetViaDiameter(MM(.8));nc.SetViaDrill(MM(.3));ds.m_MinClearance=MM(.15);ds.m_TrackMinWidth=MM(.15);ds.m_CopperEdgeClearance=MM(.5);ds.m_ViasMinSize=MM(.8);ds.m_ViasMinAnnularWidth=MM(.25);ds.m_MinThroughDrill=MM(.3);ds.m_HoleClearance=MM(.25);ds.m_HoleToHoleMin=MM(.25);ds.m_SolderMaskExpansion=MM(.03);ds.m_SolderMaskMinWidth=MM(.1)
        pcb.SaveBoard(str(P/'CTRL.kicad_pcb'),self.b)
    def dsn(self,ground=False):
        self.b.BuildConnectivity();path=D/'analysis/CTRL.dsn';path.parent.mkdir(exist_ok=True)
        omit=[z for z in self.b.Zones() if not z.GetIsRuleArea()]
        for z in omit:self.b.Remove(z)
        assert pcb.ExportSpecctraDSN(self.b,str(path))
        for z in omit:self.b.Add(z)
        s=path.read_text();s=s.replace('(clearance 50 (type smd_smd))','(clearance 150 (type smd_smd))')
        a=s.index('    (class kicad_default');b=s.index('  (wiring',a);section=s[a:b]
        power=['PACK_RAW','PACK_FUSED','PACK_PROT','VIN_SYS','USB_VBUS','USB_LIMIT','BUCK_SW','V3V3','V3V3_RF80','V3V3_RF2M']
        for n in power+['GND']:section=re.sub(r'(?<![\w])'+re.escape(n)+r'(?![\w])','',section)
        extra=''
        for cls,ns,w in [('POWER',power,500),('GROUND',['GND'],200)]:extra+='    (class '+cls+' '+' '.join(ns)+' (circuit(use_via "Via[0-1]_800:300_um"))(rule(width '+str(w)+')(clearance 150)))\n'
        pos=section.rfind('  )');section=section[:pos]+extra+section[pos:];s=s[:a]+section+s[b:]
        # Plane connections are completed with filled F/B ground and inspected native DRC.
        sx=parse(s.replace('(string_quote ")','(string_quote QUOTE_CHARACTER)'));network=child(sx,'network')
        # GCT USB outer terminals are coincident A/B copper lands. Native board
        # keeps both physical pin identities. The offline router needs one shape.
        alias={'B12':'A1','B1':'A12','B9':'A4','B4':'A9'}
        for im in children(child(sx,'library'),'image'):
            if str(im[1]).endswith('USB4105_Standard'):
                for pin in list(children(im,'pin')):
                    if pin[2] in alias:im.remove(pin)
        for net in children(network,'net'):
            if net[1]=='GND' and not ground:net[:]=[net[0],net[1]]
            else:
                pins=child(net,'pins')
                if pins:pins[:]=[pins[0]]+[v for v in pins[1:] if v not in ['J2-'+n for n in alias]]
        path.write_text(dump(sx).replace('(string_quote QUOTE_CHARACTER)','(string_quote ")')+'\n')
    def zones(self):
        from m3b_ground_fanout import point_segment
        for layer in [pcb.F_Cu,pcb.B_Cu]:
            z=pcb.ZONE(self.b);z.SetLayer(layer);z.SetNet(self.nets['GND']);z.SetLocalClearance(MM(.25));z.SetMinThickness(MM(.2));z.SetThermalReliefGap(MM(.25));z.SetThermalReliefSpokeWidth(MM(.25));z.SetPadConnection(pcb.ZONE_CONNECTION_THERMAL);poly=z.Outline();poly.NewOutline()
            for x,y in [(20.6,20.6),(119.4,20.6),(119.4,119.4),(20.6,119.4)]:poly.Append(MM(x),MM(y))
            self.b.Add(z)
        # Ground stitching outside all pads and antenna keepout; avoid hidden via-in-pad joints.
        pads=[p for f in self.b.GetFootprints() for p in f.Pads()]
        for x in range(23,119,6):
            for y in range(23,119,6):
                if 25<x<75 and y<29:continue
                if any(abs(x-pcb.ToMM(p.GetPosition().x))<pcb.ToMM(p.GetSize().x)/2+.75 and abs(y-pcb.ToMM(p.GetPosition().y))<pcb.ToMM(p.GetSize().y)/2+.75 for p in pads):continue
                if any(t.GetNetname()!='GND' and point_segment((x,y),xy(t.GetStart()),xy(t.GetEnd()))<pcb.ToMM(t.GetWidth(pcb.F_Cu) if isinstance(t,pcb.PCB_VIA) else t.GetWidth())/2+.59 for t in self.b.GetTracks()):continue
                if any(isinstance(t,pcb.PCB_VIA) and math.dist((x,y),xy(t.GetPosition()))<.56 for t in self.b.GetTracks()):continue
                v=pcb.PCB_VIA(self.b);v.SetPosition(pt(x,y));v.SetWidth(MM(.8));v.SetDrill(MM(.3));v.SetViaType(pcb.VIATYPE_THROUGH);v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(self.nets['GND']);self.b.Add(v)
        pcb.ZONE_FILLER(self.b).Fill(self.b.Zones())
    def imp(self,path):
        assert pcb.ImportSpecctraSES(self.b,str(path));self.save()
def main():
    a=argparse.ArgumentParser();a.add_argument('--place',action='store_true');a.add_argument('--dsn',action='store_true');a.add_argument('--route-ground',action='store_true');a.add_argument('--import-session');a.add_argument('--zones',action='store_true');args=a.parse_args();b=Board(not args.place)
    if args.place:b.place_all();b.save();(D/'analysis').mkdir(exist_ok=True);(D/'analysis/manual-routes.json').write_text(json.dumps(b.manual,indent=2)+'\n')
    if args.dsn:b.dsn(args.route_ground)
    if args.import_session:b.imp(args.import_session)
    if args.zones:b.zones();b.save()
if __name__=='__main__':main()
