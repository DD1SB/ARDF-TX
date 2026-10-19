#!/usr/bin/python3
"""Explicit local CAD repairs; never change net assignment or RF line bodies."""
import argparse,collections,types,sys
from m5b_e5_common import *
REMOVED=[]
def uid(x):return x.m_Uuid.AsString()
def fix():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};d=json.loads((OUT/'DRC.json').read_text());items={uid(t):t for t in b.GetTracks()};items.update({uid(a):a for f in fs.values()for a in f.Pads()});logs=[]
 # The offline router's automatic neckdown is below this project's minimum.
 # Restore the actual copper width, then use native clearance checks again.
 for t in b.GetTracks():
  if not isinstance(t,p.PCB_VIA)and t.GetWidth()<MM(.15):t.SetWidth(MM(.15));logs.append('width:'+uid(t))
 for case in d['violations']:
  if case['type']=='starved_thermal':
   for i in case['items']:
    o=items.get(i['uuid'])
    if isinstance(o,p.PAD)and o.GetNetname()=='GND':o.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL);logs.append('ground solid contact:'+uid(o))
 # Move the live-tab pass-device assembly clear of the common corner pillar.
 # Its separate SK48 extrusion is above the front edge; PA SK81 is unchanged.
 if xy(fs['Q401'].GetPosition())==(139.,26.):
  fs['Q401'].Move(pt(-24,0));fs['R506'].Move(pt(-14,0))
  nets={a.GetNetname()for r in['Q401','R506']for a in fs[r].Pads()}
  for t in list(b.GetTracks()):
   if t.GetNetname()in nets and not t.IsLocked():b.Remove(t);REMOVED.append(t)
  logs.append('Q401 -24X / R506 -14X; local supply/base routes rebuilt')
 if xy(fs['R509'].GetPosition())==(118.1,65.4):
  fs['R509'].Move(pt(2,0))
  for t in list(b.GetTracks()):
   if t.GetNetname()in['NORMAL_OFF']and not t.IsLocked():b.Remove(t);REMOVED.append(t)
  logs.append('R509 +2X for physical clearance')
 # Nonessential old footprint text goes to the assembly drawing. Mandatory
 # new board legend is placed once the routing/clearance work is complete.
 for f in fs.values():
  for g in f.GraphicalItems():
   if isinstance(g,p.PCB_TEXT)and g.GetLayer()in[p.F_SilkS,p.B_SilkS]:g.SetLayer(p.F_Fab if g.GetLayer()==p.F_SilkS else p.B_Fab)
 for g in b.GetDrawings():
  if g.GetLayer()in[p.F_SilkS,p.B_SilkS]:g.SetLayer(p.F_Fab if g.GetLayer()==p.F_SilkS else p.B_Fab)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('local-repair-log.json',dict(actions=logs,RF_signal_geometry='not edited',electrical_nets='not edited',ordinary_ground_joint='Direct pour contacts on reported starved pads; assembly preheat required.'))
def complete(args):
 report=OUT/'DRC.json'
 if '--report'in args:
  i=args.index('--report');report=Path(args[i+1]);args=args[:i]+args[i+2:]
 code=(ROOT/'tools/m5b_route_completion.py').read_text().replace('from m5b_pcb import P,D,MM','from m5b_e5_common import HW as P,OUT as D,MM').replace('NX=1801;NY=1401','NX=1501;NY=1101').replace('STEP=.025;NX=7201;NY=5601','STEP=.05;NX=3001;NY=2201').replace('[:256]','[:16]').replace('expanded>1000000','expanded>500000')
 # Native source copper is net-connected conductive geometry, not artwork.
 needle='        for zone in b.Zones():'
 insert='''        for shape in b.GetDrawings():
            if shape.GetLayer()!=pcb.F_Cu or not hasattr(shape,'GetNetname') or shape.GetNetname()==net:continue
            if shape.GetShape()==pcb.SHAPE_T_POLY:
                from PIL import ImageChops
                for target,rr in [(ims[0],gap+width/2+extra),(vims[0],gap+.3+extra)]:
                    poly=pcb.SHAPE_POLY_SET();shape.TransformShapeToPolygon(poly,pcb.F_Cu,0,MM(.002),pcb.ERROR_OUTSIDE);poly.Inflate(MM(rr),pcb.CORNER_STRATEGY_ROUND_ALL_CORNERS,MM(.004));mask=Image.new('L',(NX,NY),0);dr=ImageDraw.Draw(mask)
                    for oi in range(poly.OutlineCount()):
                        chain=poly.COutline(oi);dr.polygon([ij(xy(chain.CPoint(k)))for k in range(chain.PointCount())],fill=1)
                        for hi in range(poly.HoleCount(oi)):
                            chain=poly.CHole(oi,hi);dr.polygon([ij(xy(chain.CPoint(k)))for k in range(chain.PointCount())],fill=0)
                    target.paste(ImageChops.lighter(target,mask))
                continue
            box=shape.GetBoundingBox();bb=[pcb.ToMM(box.GetLeft()),pcb.ToMM(box.GetTop()),pcb.ToMM(box.GetRight()),pcb.ToMM(box.GetBottom())]
            rect(ds[0],bb,gap+width/2+extra);rect(vs[0],bb,gap+.3+extra)
'''
 code=code.replace(needle,insert+needle)
 code=code.replace('                ww=pcb.ToMM(shape.GetWidth())/2\n', '''                if shape.GetShape()in[pcb.SHAPE_T_RECT,pcb.SHAPE_T_POLY]:
                    bb=shape.GetBoundingBox();box=[pcb.ToMM(bb.GetLeft()),pcb.ToMM(bb.GetTop()),pcb.ToMM(bb.GetRight()),pcb.ToMM(bb.GetBottom())]
                    rect(ds[0],box,gap+width/2+extra);rect(vs[0],box,gap+.30+extra);continue
                ww=pcb.ToMM(shape.GetWidth())/2
''')
 code=code.replace("        for d in ds+vs:\n", "        edgecells=int(math.ceil((.5+max(width/2,.3)+.025)/STEP))\n        for d in ds+vs:\n").replace('(0,0,NX-1,12)','(0,0,NX-1,edgecells)').replace('(0,NY-13,NX-1,NY-1)','(0,NY-1-edgecells,NX-1,NY-1)').replace('(0,0,12,NY-1)','(0,0,edgecells,NY-1)').replace('(NX-13,0,NX-1,NY-1)','(NX-1-edgecells,0,NX-1,NY-1)')
 mod=types.ModuleType('compact_route_completion');mod.__file__=str(ROOT/'tools/m5b_route_completion.py');exec(compile(code,mod.__file__,'exec'),mod.__dict__);sys.argv=[sys.argv[0],str(report)]+args;mod.main()
def converter():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
 for t in list(b.GetTracks()):
  if t.GetNetname()in['BOOST_SW','BOOST_BST']:b.Remove(t);REMOVED.append(t)
 fs['C401'].SetOrientationDegrees(270 if fs['C401'].GetOrientationDegrees()==90 else fs['C401'].GetOrientationDegrees()+180)
 def line(net,pts,width,layer=p.F_Cu):
  for aa,zz in zip(pts,pts[1:]):
   t=p.PCB_TRACK(b);t.SetStart(pt(*aa));t.SetEnd(pt(*zz));t.SetWidth(MM(width));t.SetLayer(layer);t.SetNet(b.FindNet(net));b.Add(t)
 # Separate, electrically isolated RNW centre contacts remain independent.
 sw=next(a for a in fs['C401'].Pads()if a.GetNumber()=='2');x,y=xy(sw.GetPosition())
 line('BOOST_SW',[(75,109),(75,107.4),(75,105.8),(x,y)],.3)
 line('BOOST_SW',[(75,109),(75,110.4),(75,111.1)],.3);line('BOOST_SW',[(75,111.1),(75,113.45)],1.)
 line('VBOOST',[(75.55,109),(75.55,107.4),(75.55,106.75)],.25)
 v=p.PCB_VIA(b);v.SetPosition(pt(75.55,106.75));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('VBOOST'));v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.Add(v)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
 save('converter-local-correction.json',dict(C401='rotated180degrees for short switch-node connection; same2pins/value',switch_path='F.Cu;0.30mm RNW contacts escaping to1mm inductor feed; no switch-node vias',VBOOST='0.25mm RNW north escape split at pad edge;0.6/0.3ordinary transition via',electrical_change=False))
def powerrequests():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};out=[]
 for r,pin,s,k in[('R309','2','Q401','3'),('Q401','2','L635','1')]:
  ends=[next(a for a in fs[x].Pads()if a.GetNumber()==n)for x,n in[(r,pin),(s,k)]]
  out.append(dict(items=[dict(uuid=uid(a),pos=dict(zip(['x','y'],xy(a.GetPosition()))))for a in ends]))
 save('power-route-requests.json',dict(unconnected_items=out))
def stitch():
 src=(ROOT/'tools/m5b_stitch.py').read_text().replace('from m5b_pcb import P,D,MM','from m5b_e5_common import HW as P,OUT as D,MM').replace("g=-.33 if pad.GetNetname()=='GND'else .92 if pad.GetNetname()=='DRAIN_PA'else .47","g=.47").replace('        for pad in pads:\n            bb=',"        if 84<x<100 and 27<y<73:return False\n        for pad in pads:\n            bb=")
 src=src.replace('p.ZONE_FILLER(b).Fill(b.Zones());','')
 # A drilled hole is absent from filled copper: sampling only its centre
 # misses the annular connection. Sample the actual surrounding copper too.
 src=src.replace('for i in at(v,l)', 'for dx,dy in [(0,0),(.22,0),(-.22,0),(0,.22),(0,-.22)] for i in at(v+pt(dx,dy),l)')
 src=src.replace("if pad.GetNetname()=='GND':join(at(pad.GetPosition(),p.F_Cu)+([]if pad.GetAttribute()==p.PAD_ATTRIB_SMD else at(pad.GetPosition(),p.B_Cu)))", "if pad.GetNetname()=='GND':\n            size=max(p.ToMM(pad.GetSize().x),p.ToMM(pad.GetSize().y))/2+.1\n            join([i for l in ([p.F_Cu]if pad.GetAttribute()==p.PAD_ATTRIB_SMD else[p.F_Cu,p.B_Cu])for dx,dy in[(0,0),(size,0),(-size,0),(0,size),(0,-size)]for i in at(pad.GetPosition()+pt(dx,dy),l)])")
 mod=types.ModuleType('compact_stitch');mod.__file__=str(ROOT/'tools/m5b_stitch.py');exec(compile(src,mod.__file__,'exec'),mod.__dict__);mod.main()
def ground():
 import math
 from m3b_ground_fanout import point_segment,seg_box,segdist
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));d=json.loads((OUT/'DRC.json').read_text());wanted={i['uuid']for c in d['unconnected_items']for i in c['items']if '[GND]'in i['description']};pads=[a for f in b.GetFootprints()for a in f.Pads()];obs=[]
 for a in pads:
  bb=a.GetBoundingBox();obs.append((a.GetNetname(),[p.ToMM(v)for v in[bb.GetLeft(),bb.GetTop(),bb.GetRight(),bb.GetBottom()]]))
 tracks=[(t.GetNetname(),xy(t.GetStart()),xy(t.GetEnd()),p.ToMM(t.GetWidth()),t.GetLayer())for t in b.GetTracks()if not isinstance(t,p.PCB_VIA)];vias=[t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)];log=[]
 for pad in pads:
  if pad.GetNetname()!='GND'or uid(pad)not in wanted or pad.GetAttribute()!=p.PAD_ATTRIB_SMD:continue
  a=xy(pad.GetPosition());choice=None
  for dist in[.8,1.,1.2,1.4,1.8,2.2,2.6,3.,3.6,4.2]:
   for dx,dy in[(dist,0),(-dist,0),(0,dist),(0,-dist),(dist,dist),(-dist,-dist),(dist,-dist),(-dist,dist)]:
    v=(a[0]+dx,a[1]+dy)
    if not(21<v[0]<169 and 21<v[1]<129)or 84<v[0]<100 and 27<v[1]<73:continue
    if any(r[0]-.47<v[0]<r[2]+.47 and r[1]-.47<v[1]<r[3]+.47 or n!='GND'and seg_box(a,v,[r[0]-.32,r[1]-.32,r[2]+.32,r[3]+.32])for n,r in obs):continue
    if any(n!='GND'and(point_segment(v,c,e)<w/2+.47 or l==p.F_Cu and segdist(a,v,c,e)<w/2+.31)for n,c,e,w,l in tracks):continue
    if any(math.dist(v,xy(t.GetPosition()))<.62 for t in vias):continue
    if any(z.GetIsRuleArea()and z.GetDoNotAllowTracks()and z.GetBoundingBox().Contains(pt(*v))for z in b.Zones()):continue
    choice=v;break
   if choice:break
  if choice:
   v=p.PCB_VIA(b);v.SetPosition(pt(*choice));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.Add(v);vias.append(v)
   t=p.PCB_TRACK(b);t.SetStart(pad.GetPosition());t.SetEnd(pt(*choice));t.SetWidth(MM(.28));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet('GND'));b.Add(t);tracks.append(('GND',a,choice,.28,p.F_Cu))
  log.append(dict(ref=pad.GetParentFootprint().GetReference(),pad=pad.GetNumber(),via=choice,status='routed'if choice else'needs_grid_route'))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('ground-pad-fanout.json',log);print('Ground direct fanout',sum(x['via']is not None for x in log),'of',len(log),flush=True)
def dense():
 import math
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));zones={z.GetLayer():z for z in b.Zones()if not z.GetIsRuleArea()};original=zones[p.F_Cu].GetFilledPolysList(p.F_Cu);top=p.SHAPE_POLY_SET(original);bot=p.SHAPE_POLY_SET(zones[p.B_Cu].GetFilledPolysList(p.B_Cu));top.Inflate(-MM(.32),p.CORNER_STRATEGY_ROUND_ALL_CORNERS,MM(.005));bot.Inflate(-MM(.32),p.CORNER_STRATEGY_ROUND_ALL_CORNERS,MM(.005));vias=[t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)];holes=[a for f in b.GetFootprints()for a in f.Pads()if a.GetDrillSize().x];log=[]
 for i in range(top.OutlineCount()):
  poly=top.COutline(i);vs=[xy(poly.CPoint(j))for j in range(poly.PointCount())];xx=[v[0]for v in vs];yy=[v[1]for v in vs];x0,x1,y0,y1=min(xx),max(xx),min(yy),max(yy);cx=(x0+x1)/2;cy=(y0+y1)/2;points=[(x/5,y/5)for x in range(int(x0*5),int(x1*5)+1)for y in range(int(y0*5),int(y1*5)+1)];points.sort(key=lambda q:(q[0]-cx)**2+(q[1]-cy)**2)
  for x,y in points:
   if 84<x<100 and 27<y<73:continue
   v=pt(x,y)
   if not top.Contains(v,i)or not bot.Contains(v):continue
   if any(math.dist((x,y),xy(q.GetPosition()))<.65 for q in vias):continue
   if any(math.dist((x,y),xy(q.GetPosition()))<p.ToMM(q.GetDrillSize().x)/2+.15+.46 for q in holes):continue
   if any(z.GetIsRuleArea()and z.GetDoNotAllowVias()and z.GetBoundingBox().Contains(v)for z in b.Zones()):continue
   via=p.PCB_VIA(b);via.SetPosition(v);via.SetWidth(MM(.6));via.SetDrill(MM(.3));via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(b.FindNet('GND'));via.SetFrontTentingMode(1);via.SetBackTentingMode(1);b.Add(via);vias.append(via);log.append([x,y]);break
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('ground-fill-intersection-stitches.json',dict(vias_mm=log,method='Native F/Bfilledcopper both eroded0.32mm;ordinary0.6/0.3outsidepads/holes;sourcebar region excluded',note='AdditionalnativeDRCrequired'));print('Native filled polygon stitches',len(log),flush=True)
def legend():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'))
 for g in list(b.GetDrawings()):
  if g.GetLayer()in[p.F_SilkS,p.B_SilkS]:b.Remove(g);REMOVED.append(g)
 for text,x,y in[('ARDF-TX RF2M M5B-E5',90,22),('CTL J101 / PIN1',30,75),('J301 1=PACK+ 2=GND',38,115.5),('NORMAL 50R',154,62),('TRAIN ONLY',152,122),('2S BOOST OR 4S BUCK: EXCLUSIVE',90,125),('EVALUATION: POWER GATES BEFORE PA',95,128)]:
  g=p.PCB_TEXT(b);g.SetText(text);g.SetPosition(pt(x,y));g.SetLayer(p.B_SilkS);g.SetTextSize(pt(1,1));g.SetTextThickness(MM(.15));g.SetMirrored(True);b.Add(g)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
def thermal_contacts():
 import math
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));removed=[];lands=[]
 for x,y in[(92,32),(92,68)]:
  poly=p.SHAPE_POLY_SET();outer=p.SHAPE_LINE_CHAIN();inner=p.SHAPE_LINE_CHAIN()
  for i in range(180):
   t=2*math.pi*i/180;outer.Append(pt(x+4.75*math.cos(t),y+4.75*math.sin(t)));inner.Append(pt(x+2.15*math.cos(-t),y+2.15*math.sin(-t)))
  outer.SetClosed(True);inner.SetClosed(True);poly.AddOutline(outer);poly.AddHole(inner,0)
  for t in list(b.GetTracks()):
   if t.GetNetname()=='GND'or not t.IsOnLayer(p.F_Cu):continue
   if p.SHAPE.Collide(t.GetEffectiveShape(p.F_Cu),poly,MM(.15)):
    assert t.GetNetname()in['VPA','NORMAL_OFF','KEY'],'Unexpected RF conductor at metalwasher:'+t.GetNetname()
    removed.append(dict(uuid=uid(t),net=t.GetNetname(),old_start_mm=xy(t.GetStart()),old_end_mm=xy(t.GetEnd())));b.Remove(t);REMOVED.append(t)
  g=p.PCB_SHAPE(b);g.SetShape(p.SHAPE_T_POLY);g.SetPolyShape(poly);g.SetFilled(True);g.SetWidth(0);g.SetLayer(p.F_Cu);g.SetNet(b.FindNet('GND'));b.Add(g);lands.append(dict(centre_mm=[x,y],outer_mm=9.5,inner_mm=4.3,uuid=uid(g)))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('ground-washer-correction.json',dict(status='IMPLEMENTED_NATIVE_GROUND_LAND_REQUIRES_REFILL_DRC',reason='H6groundwasher contactpatch was cut by a newly routedKEY trace. Audit also found inheritedVPA feed under H5OD9metalwasher. Mask alone is not insulation.',lands=lands,removed_for_local_reroute=removed,matching_RF_lines_changed=False,thermal_source_joint_changed=False,thermal_model_credit_for_added_copper=False,H6_mask_opening='Original2x0.5mm groundingpatch preserved',corner_supports='M3 insulating standoffs/washers;grounded bar hardware onlyH5/H6.'))
def main():
 guard();ap=argparse.ArgumentParser();ap.add_argument('action',choices=['fix','complete','stitch','ground','converter','powerrequests','dense','legend','thermal_contacts']);a,rest=ap.parse_known_args()
 if a.action=='fix':fix()
 elif a.action=='stitch':stitch()
 elif a.action=='ground':ground()
 elif a.action=='converter':converter()
 elif a.action=='powerrequests':powerrequests()
 elif a.action=='dense':dense()
 elif a.action=='legend':legend()
 elif a.action=='thermal_contacts':thermal_contacts()
 else:complete(rest)
if __name__=='__main__':main()
