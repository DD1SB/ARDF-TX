import sys,math,json
sys.path.insert(0,'tools')
from m6_c1_pcb import *
b=Board(True);b.b.BuildConnectivity();root=b.pad('J1',2);
if b.pad('C10',2).m_Uuid.AsString() in {o.m_Uuid.AsString() for o in b.b.GetConnectivity().GetConnectedItems(root)}:
 print('C10 ground already connected');raise SystemExit(0)
allz=[z for z in b.b.Zones() if not z.GetIsRuleArea()];pads=[a for f in b.b.GetFootprints() for a in f.Pads()];obs=[t for t in b.b.GetTracks() if t.GetNetname()!='GND']+[a for a in pads if a.GetNetname()!='GND'];obs=[(o,o.GetBoundingBox()) for o in obs];out=[]
for x,y in sorted([(x/10,y/10) for x in range(334,355) for y in range(398,441)],key=lambda p:math.dist(p,(35.025,41.2))):
 pos=pt(x,y)
 if not all(any(z.IsOnLayer(l) and z.GetFilledPolysList(l).Contains(pos) for z in allz) for l in [pcb.F_Cu,pcb.B_Cu]):continue
 if any(abs(x-pcb.ToMM(a.GetPosition().x))<pcb.ToMM(a.GetSize().x)/2+.41 and abs(y-pcb.ToMM(a.GetPosition().y))<pcb.ToMM(a.GetSize().y)/2+.41 for a in pads):continue
 sh=pcb.SHAPE_CIRCLE(pos,MM(.4));bb=sh.BBox();bb.Inflate(MM(.18))
 if any(bb.Intersects(ob) and any(o.IsOnLayer(l) and pcb.SHAPE.Collide(sh,o.GetEffectiveShape(l),MM(.17)) for l in [pcb.F_Cu,pcb.B_Cu]) for o,ob in obs):continue
 out.append((x,y))
 if len(out)==1:break
assert out,'No ordinary0.8mm via fit in C10 ground island'
x,y=out[0];v=pcb.PCB_VIA(b.b);v.SetPosition(pt(x,y));v.SetWidth(MM(.8));v.SetDrill(MM(.3));v.SetViaType(pcb.VIATYPE_THROUGH);v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(b.nets['GND']);v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.b.Add(v);pcb.ZONE_FILLER(b.b).Fill(b.b.Zones());b.save();print('C10 local ground stitch',out)
(D/'C10-ground-return.json').write_text(json.dumps({'reason':'Moved USB ESD bypass ground pad was on isolated front fill; native connectivity identified C10.2 as sole missing GND pad.','ordinary_via_mm':out,'land_drill_mm':[.8,.3],'native_clearance_test_mm':.17,'manufacturing':'ordinary through via outside solder lands; no filled-via assumption'},indent=2)+'\n')
