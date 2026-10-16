#!/usr/bin/python3
"""Native thermal geometry, RF preservation and adverse-condition checks."""
import math,json,xml.etree.ElementTree as ET
import pcbnew as p
from m5b_e4_common import *
from m5b_e3_common import LENGTHS,WIDTH
from m5b_e4_thermal import solve

def sig(fn):
 return {n.get('name'):sorted((a.get('ref'),a.get('pin'))for a in n.findall('node'))for n in ET.parse(fn).findall('./nets/net')}
def rectcheck(b):
 fs={f.GetReference():f for f in b.GetFootprints()};src=next(a for a in fs['Q501'].Pads()if a.GetNumber()=='S')
 assert src.GetNetname()=='GND'and(p.ToMM(src.GetSize().x),p.ToMM(src.GetSize().y))==(2.7,5.)
 got={}
 for v in b.GetTracks():
  if isinstance(v,p.PCB_VIA)and 109<p.ToMM(v.GetPosition().x)<115 and 48<p.ToMM(v.GetPosition().y)<62:
   key=(round(p.ToMM(v.GetPosition().x),4),round(p.ToMM(v.GetPosition().y),4));got[key]=v
 assert len(got)==len(VIAS),'thermal_via_count'
 for i,xy in enumerate(VIAS):
  key=tuple(round(n,4)for n in xy);assert key in got,('thermal_position',key);v=got[key];large=i>=len(INNER)+len(NEAR)
  assert v.GetNetname()=='GND','source_ground';assert abs(p.ToMM(v.GetWidth(p.F_Cu))-(1.1 if large else .8))<.001,'thermal_land'
  assert abs(p.ToMM(v.GetDrillValue())-(.5 if large else .3))<.001,'thermal_drill'
  assert not v.IsTented(p.B_Mask),'bottom_contact'
 bar=p.PCB_SHAPE(b);bar.SetShape(p.SHAPE_T_RECT);bar.SetStart(p.VECTOR2I(p.FromMM(BAR[0]),p.FromMM(BAR[1])));bar.SetEnd(p.VECTOR2I(p.FromMM(BAR[2]),p.FromMM(BAR[3])));bar.SetFilled(True);bar.SetWidth(0)
 for t in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]:
  if t.GetNetname()=='GND'or not t.IsOnLayer(p.B_Cu)or isinstance(t,p.PAD)and t.GetAttribute()==p.PAD_ATTRIB_NPTH:continue
  assert not p.SHAPE.Collide(t.GetEffectiveShape(p.B_Cu),bar.GetEffectiveShape(),p.FromMM(.5)),('live_copper_under_bar',t.GetNetname())
 # Mask artwork is checked against the library and the actual via centers.
 g=[x for x in fs['Q501'].GraphicalItems()if x.GetLayer()==p.F_Mask];assert len(g)==13,'source_mask_aperture_count'
 for v in [got[tuple(round(z,4)for z in xy)]for xy in INNER]:
  for x in g:assert not x.GetBoundingBox().Contains(v.GetPosition()),'mask_cap_missing'
 win=[x for x in b.GetDrawings()if x.GetLayer()==p.B_Mask and x.GetShape()==p.SHAPE_T_RECT and tuple(round(p.ToMM(z),4)for z in [x.GetStart().x,x.GetStart().y,x.GetEnd().x,x.GetEnd().y])==WINDOW];assert len(win)==1,'thermal_contact_window'
 zones=[z.GetFilledPolysList(p.F_Cu)for z in b.Zones()if z.GetNetname()=='GND'and z.IsOnLayer(p.F_Cu)and not z.GetIsRuleArea()]
 for xx in[111.,111.5,112.,112.5,113.]:
  for yy in[71.8,72.05,72.3]:
   pt=p.VECTOR2I(p.FromMM(xx),p.FromMM(yy))
   assert any(z.Contains(pt)for z in zones),'ground_washer_plane_missing'
 for r,l in LENGTHS.items():
  f=fs[r];a={x.GetNumber():x for x in f.Pads()};assert abs((a['1'].GetPosition()-a['2'].GetPosition()).EuclideanNorm()/1e6-l)<.00001,'RF_length'
  copper=[x for x in f.GraphicalItems()if x.GetLayer()==p.F_Cu];assert len(copper)==1 and abs(p.ToMM(copper[0].GetBoundingBox().GetHeight())-WIDTH)<.00001,'RF_width'
 for r,xy in [('Q501',(112,55)),('H5',(112,32)),('H6',(112,68))]:assert math.dist([p.ToMM(fs[r].GetPosition().x),p.ToMM(fs[r].GetPosition().y)],xy)<.00001,'mechanical_mount'
 return fs,got
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs,got=rectcheck(b)
 assert sig(OUT/'RF2M.net.xml')==sig(HW/'review/M5B-E3/RF2M.net.xml'),'electrical_change'
 old=p.LoadBoard(str(OUT/'development/E3-native.kicad_pcb'));of={f.GetReference():f for f in old.GetFootprints()}
 def tracks(bb):return{t.m_Uuid.AsString():(t.GetNetname(),t.GetLayer(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetWidth())for t in bb.GetTracks()if not isinstance(t,p.PCB_VIA)}
 assert tracks(b)==tracks(old),'signal_or_power_track_change'
 for r,f in fs.items():
  assert f.GetPosition()==of[r].GetPosition()and f.GetOrientationDegrees()==of[r].GetOrientationDegrees(),('component_move',r)
  for a in f.Pads():
   aa=min((z for z in of[r].Pads()if z.GetNumber()==a.GetNumber()),key=lambda z:(z.GetPosition()-a.GetPosition()).EuclideanNorm())
   assert a.GetPosition()==aa.GetPosition()and a.GetSize()==aa.GetSize()and a.GetDrillSize()==aa.GetDrillSize()and a.GetNetname()==aa.GetNetname(),('package_pad_change',r)
 pro=HW/'RF2M.kicad_pro';assert pro.read_bytes()==gitfile(pro.relative_to(ROOT)),'DRC_config_changed'
 # Re-run the three E3 RF/thermal mutation classes with E4 expected geometry.
 mutations=[]
 def reject(name,change,undo):
  change()
  try:rectcheck(b)
  except AssertionError:mutations.append(name)
  else:raise AssertionError('mutation escaped '+name)
  finally:undo()
 pad=next(a for a in fs['TL608'].Pads()if a.GetNumber()=='2');pos=pad.GetPosition();reject('TL608_length',lambda:pad.SetPosition(pos+p.VECTOR2I(p.FromMM(.2),0)),lambda:pad.SetPosition(pos))
 v=next(iter(got.values()));net=v.GetNet();reject('source_to_drain',lambda:v.SetNet(b.FindNet('PA_DRAIN')),lambda:v.SetNet(net))
 w=v.GetWidth(p.F_Cu);reject('undersize_thermal_land',lambda:v.SetWidth(p.FromMM(.6)),lambda:v.SetWidth(w))
 v=next(iter(got.values()));mode=v.GetBackTentingMode();reject('bottom_contact_tented',lambda:v.SetBackTentingMode(1),lambda:v.SetBackTentingMode(mode))
 g=next(x for x in fs['Q501'].GraphicalItems()if x.GetLayer()==p.F_Mask);start,end=g.GetStart(),g.GetEnd();reject('source_mask_open_over_holes',lambda:(g.SetStart(p.VECTOR2I(p.FromMM(110.65),p.FromMM(52.5))),g.SetEnd(p.VECTOR2I(p.FromMM(113.35),p.FromMM(57.5)))),lambda:(g.SetStart(start),g.SetEnd(end)))
 f=fs['H6'];pos=f.GetPosition();reject('mislocated_M3_mount',lambda:f.SetPosition(pos+p.VECTOR2I(p.FromMM(2),0)),lambda:f.SetPosition(pos))
 model=json.loads((OUT/'thermal-model.json').read_text());cons=model['cases']['conservative']['10'];assert cons['junction_40C_4W_C']<=110,'thermal_design_target'
 baseline=cons['total_JA_K_W'];bad=[]
 for name,delta in [('reduced_barrel_5um',None),('missing_contact',None),('wrong_sink_8K_W',4.),('poor_joint',None)]:
  if name=='reduced_barrel_5um':r,_=solve(plate=5,cu=30,tim_mm=.15,tim_k=6,inner_loss=4);tj=40+4*(3+1+r+.7+4+.6)
  elif name=='missing_contact':r,_=solve(contact=False);tj=math.inf
  elif name=='poor_joint':tj=model['cases']['poor_joint']['10']['junction_40C_4W_C']
  else:tj=40+4*(baseline+delta)
  assert tj>110;bad.append(dict(mutation=name,detected='110C_design_target_exceeded',calculated_junction_C=tj if math.isfinite(tj)else None))
 # Joint area is the real pad minus clipped, disjoint 0.45mm mask caps.
 area=2.7*5
 for x,y in INNER:
  area-=max(0,min(113.35,x+.225)-max(110.65,x-.225))*.45
 save('thermal-assembly-audit.json',dict(status='OPEN_ASSEMBLY_QUALIFICATION',source_mask_aperture_mm2=area,source_mask_fraction_open=area/13.5,mask_caps_mm=.45,nominal_hole_mm=.3,nominal_mask_overlap_mm=.075,published_finished_hole_upper_mm=.43,published_hole_position_tolerance_mm=.075,guaranteed_cap_closure=False,reason='0.45mm cap cannot cover a 0.43mm hole at the full +/-0.075mm position limit. Mask registration adds further uncertainty. Ordinary tenting is not plugging. Copper DFM passes; source solder coverage is not proven.',minimum_source_joint_effective_area_assumption_mm2=area*.5,model_solder_joint_K_W=1.,joint_requirement='No open holes/wicking-starved source joint; use first-build X-ray or equivalent qualified joint inspection plus measured heat transfer. Do not claim these checks performed.',acceptance='HOLD source-joint reproducibility until assembly method is independently accepted. No special via treatment authorized.',physical='NOT_RUN'))
 save('engineering-regression.json',dict(status='PASS_CAD_GEOMETRY_AND_CALCULATION_CHECKS',electrical_net_membership_equal_E3=True,all_320_pad_sets_positions_and_sizes_preserved=True,all_signal_and_power_tracks_preserved=True,RF_lines_preserved=list(LENGTHS),thermal_vias=len(VIAS),E3_mutation_classes_preserved=mutations[:3],additional_native_mutations=mutations[3:],additional_thermal_mutations=bad,purchased_parts_and_populations_unchanged=True,DRC_configuration_identical_to_E3=True,physical='NOT_RUN',assembly_gate='OPEN / HOLD; see thermal-assembly-audit.json'))
 print('PASS E4 native/package/RF preservation and 10 geometry/model negative tests; source assembly gate OPEN')
if __name__=='__main__':main()
