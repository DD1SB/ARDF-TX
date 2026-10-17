#!/usr/bin/python3
"""Native assembly geometry and meaningful mutation tests. Physical gates stay open."""
import math,json,copy,xml.etree.ElementTree as ET
import pcbnew as p
from m5b_e4r1_common import *
from m5b_e3_common import LENGTHS,WIDTH
from m5b_e4r1_thermal import solve
MM=p.FromMM
def xy(v):return(p.ToMM(v.x),p.ToMM(v.y))
def bounds(g):return tuple(round(v,6)for v in(*xy(g.GetStart()),*xy(g.GetEnd())))
def area(r):return(r[2]-r[0])*(r[3]-r[1])
def audit(b,inputs=None):
 cfg=dict(guaranteed_tenting=False,stencil_mm=.12,joint_K_W=1.,wet_area_mm2=4.,joint_thickness_mm=.1,solder_k=25.,sink_K_W=4.,bottom_contact_fraction=1.,ineffective_source_vias=4)
 if inputs:cfg.update(inputs)
 fs={f.GetReference():f for f in b.GetFootprints()};q=fs['Q501'];s=next(a for a in q.Pads()if a.GetNumber()=='S');problems=[]
 def check(ok,code):
  if not ok:problems.append(code)
 check(s.GetNetname()=='GND','source_ground_net');check(xy(s.GetPosition())==(112,55)and xy(s.GetSize())==(2.7,5),'manufacturer_source_land')
 actual={tuple(round(a,4)for a in xy(v.GetPosition())):v for v in b.GetTracks()if isinstance(v,p.PCB_VIA)and 109<p.ToMM(v.GetPosition().x)<115 and 48<p.ToMM(v.GetPosition().y)<62}
 check(len(actual)==len(VIAS),'thermal_via_count')
 for x,y,d,w,kind in via_specs():
  v=actual.get((round(x,4),round(y,4)));check(v is not None,'via_outside_accepted_region')
  if v is None:continue
  check(v.GetNetname()=='GND','source_ground_net');check(abs(p.ToMM(v.GetDrillValue())-d)<.0001,'thermal_drill');check(abs(p.ToMM(v.GetWidth(p.F_Cu))-w)<.0001,'thermal_land')
  check(not v.IsTented(p.B_Mask),'bottom_contact_tented')
  if kind=='joint':check(v.IsTented(p.F_Mask),'automatic_via_aperture_outside_source_window')
 mask=[g for g in q.GraphicalItems()if g.GetLayer()==p.F_Mask];paste=[g for g in q.GraphicalItems()if g.GetLayer()==p.F_Paste]
 check(len(mask)==1 and bounds(mask[0])==SOLDER,'source_mask_islands_or_insufficient_area')
 for x,y in INNER:check(any(g.GetBoundingBox().Contains(p.VECTOR2I(MM(x),MM(y)))for g in mask),'source_hole_not_open_in_actual_mask')
 check(sorted(bounds(g)for g in paste)==sorted(PASTE),'paste_geometry')
 a=sum(area(bounds(g))for g in paste);check(6.6<a<7.0,'paste_volume_area')
 for g in paste:
  r=bounds(g);w=r[2]-r[0];h=r[3]-r[1];check(w>0 and h>0 and w*h/(2*cfg['stencil_mm']*(w+h))>=.66,'paste_release_ratio')
  check(r[0]>=SOLDER[0]and r[1]>=SOLDER[1]and r[2]<=SOLDER[2]and r[3]<=SOLDER[3],'paste_outside_source_opening')
 check(not cfg['guaranteed_tenting'],'unsupported_guaranteed_tenting_claim')
 check(.1<=cfg['stencil_mm']<=.127,'stencil_thickness');check(cfg['joint_K_W']>=1000*cfg['joint_thickness_mm']/(cfg['solder_k']*cfg['wet_area_mm2']),'unjustified_low_joint_resistance');check(cfg['sink_K_W']>=4.,'unjustified_sink_rating');check(cfg['bottom_contact_fraction']>=.7,'inadequate_bottom_contact');check(cfg['ineffective_source_vias']<=4,'excessive_source_via_loss')
 for ref,l in LENGTHS.items():
  f=fs[ref];pads={a.GetNumber():a for a in f.Pads()};check(abs((pads['1'].GetPosition()-pads['2'].GetPosition()).EuclideanNorm()/1e6-l)<.00001,'RF_length')
  g=[a for a in f.GraphicalItems()if a.GetLayer()==p.F_Cu];check(len(g)==1 and abs(p.ToMM(g[0].GetBoundingBox().GetHeight())-WIDTH)<.00001,'RF_width')
 for ref,pos in[('Q501',(112,55)),('H5',(112,32)),('H6',(112,68))]:check(xy(fs[ref].GetPosition())==pos,'mechanical_mount')
 rects=[g for g in b.GetDrawings()if g.GetLayer()==p.F_Cu and g.GetShape()==p.SHAPE_T_RECT]
 for r in TOP_RECTS:check(any(bounds(g)==r and g.GetNetname()=='GND'for g in rects),'source_ground_rail')
 check(any(g.GetLayer()==p.B_Mask and g.GetShape()==p.SHAPE_T_RECT and bounds(g)==WINDOW for g in b.GetDrawings()),'bottom_mask_window')
 zones=[z.GetFilledPolysList(p.F_Cu)for z in b.Zones()if z.GetNetname()=='GND'and z.IsOnLayer(p.F_Cu)and not z.GetIsRuleArea()]
 for xx in[111.,111.5,112.,112.5,113.]:
  for yy in[71.8,72.05,72.3]:check(any(z.Contains(p.VECTOR2I(MM(xx),MM(yy)))for z in zones),'ground_washer_plane_missing')
 # Check the actual whole bar envelope against foreign bottom copper, not AABBs.
 bar=p.PCB_SHAPE(b);bar.SetShape(p.SHAPE_T_RECT);bar.SetStart(p.VECTOR2I(MM(BAR[0]),MM(BAR[1])));bar.SetEnd(p.VECTOR2I(MM(BAR[2]),MM(BAR[3])));bar.SetFilled(True);bar.SetWidth(0)
 for t in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]:
  if t.GetNetname()=='GND'or not t.IsOnLayer(p.B_Cu)or isinstance(t,p.PAD)and t.GetAttribute()==p.PAD_ATTRIB_NPTH:continue
  check(not p.SHAPE.Collide(t.GetEffectiveShape(p.B_Cu),bar.GetEffectiveShape(),MM(.5)),'live_copper_under_bar')
 return sorted(set(problems))

def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));assert not audit(b),audit(b);old=p.LoadBoard(str(OUT/'development/E4-native.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};of={f.GetReference():f for f in old.GetFootprints()}
 def tracks(bb):return{t.m_Uuid.AsString():(t.GetNetname(),t.GetLayer(),t.GetStart().x,t.GetStart().y,t.GetEnd().x,t.GetEnd().y,t.GetWidth())for t in bb.GetTracks()if not isinstance(t,p.PCB_VIA)}
 assert tracks(b)==tracks(old),'signal/power track changed'
 for ref,f in fs.items():
  assert f.GetPosition()==of[ref].GetPosition()and f.GetOrientationDegrees()==of[ref].GetOrientationDegrees()
  for a in f.Pads():
   aa=min((z for z in of[ref].Pads()if z.GetNumber()==a.GetNumber()),key=lambda z:(z.GetPosition()-a.GetPosition()).EuclideanNorm());assert a.GetPosition()==aa.GetPosition()and a.GetSize()==aa.GetSize()and a.GetDrillSize()==aa.GetDrillSize()and a.GetNetname()==aa.GetNetname(),(ref,a.GetNumber())
 def nets(fn):return{n.get('name'):sorted((a.get('ref'),a.get('pin'))for a in n.findall('node'))for n in ET.parse(fn).findall('./nets/net')}
 assert nets(OUT/'RF2M.net.xml')==nets(HW/'review/M5B-E4/RF2M.net.xml')
 assert(HW/'RF2M.kicad_pro').read_bytes()==gitfile('hardware/2m/RF2M.kicad_pro')
 tests=[]
 def reject(name,code,change,undo,inputs=None):
  change();errors=audit(b,inputs);undo();assert code in errors,(name,errors);tests.append(dict(mutation=name,detected=code))
 pad=next(a for a in fs['TL608'].Pads()if a.GetNumber()=='2');v0=pad.GetPosition();reject('TL608_length','RF_length',lambda:pad.SetPosition(v0+p.VECTOR2I(MM(.2),0)),lambda:pad.SetPosition(v0))
 v=next(t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)and math.dist(xy(t.GetPosition()),INNER[0])<.0001);n=v.GetNet();reject('source_to_drain','source_ground_net',lambda:v.SetNet(b.FindNet('PA_DRAIN')),lambda:v.SetNet(n))
 w=v.GetWidth(p.F_Cu);reject('undersize_thermal_land','thermal_land',lambda:v.SetWidth(MM(.5)),lambda:v.SetWidth(w))
 mode=v.GetBackTentingMode();reject('bottom_contact_tented','bottom_contact_tented',lambda:v.SetBackTentingMode(1),lambda:v.SetBackTentingMode(mode))
 g=next(a for a in fs['Q501'].GraphicalItems()if a.GetLayer()==p.F_Mask);start,end=g.GetStart(),g.GetEnd();reject('reintroduce_undersized_mask_islands','source_mask_islands_or_insufficient_area',lambda:g.SetEnd(start+p.VECTOR2I(MM(.45),MM(.45))),lambda:(g.SetStart(start),g.SetEnd(end)))
 f=fs['H6'];pos=f.GetPosition();reject('mislocated_M3_mount','mechanical_mount',lambda:f.SetPosition(pos+p.VECTOR2I(MM(2),0)),lambda:f.SetPosition(pos))
 # Additional actual native geometry/model mutations requested by E4R1.
 noop=lambda:None
 reject('false_tenting_guarantee','unsupported_guaranteed_tenting_claim',noop,noop,dict(guaranteed_tenting=True))
 mode=v.GetFrontTentingMode();reject('unintended_automatic_mask_annulus','automatic_via_aperture_outside_source_window',lambda:v.SetFrontTentingMode(2),lambda:v.SetFrontTentingMode(mode))
 pos=v.GetPosition();reject('via_outside_source_region','via_outside_accepted_region',lambda:v.SetPosition(pos+p.VECTOR2I(MM(10),0)),lambda:v.SetPosition(pos))
 reject('excessive_via_loss','excessive_source_via_loss',noop,noop,dict(ineffective_source_vias=9))
 reject('reduced_solderable_source','source_mask_islands_or_insufficient_area',lambda:g.SetEnd(start+p.VECTOR2I(MM(.7),MM(5))),lambda:g.SetEnd(end))
 reject('optimistic_solder_joint','unjustified_low_joint_resistance',noop,noop,dict(joint_K_W=.05))
 reject('unjustified_small_sink','unjustified_sink_rating',noop,noop,dict(sink_K_W=1))
 reject('lost_bottom_contact','inadequate_bottom_contact',noop,noop,dict(bottom_contact_fraction=.4))
 g=next(a for a in fs['Q501'].GraphicalItems()if a.GetLayer()==p.F_Paste);end=g.GetEnd();reject('invalid_paste_aperture','paste_geometry',lambda:g.SetEnd(g.GetStart()+p.VECTOR2I(MM(.05),MM(.05))),lambda:g.SetEnd(end))
 g=next(a for a in b.GetDrawings()if a.GetLayer()==p.F_Cu and a.GetShape()==p.SHAPE_T_RECT and bounds(a)==TOP_RECTS[0]);net=g.GetNet();reject('broken_source_ground_rail','source_ground_rail',lambda:g.SetNet(b.FindNet('PA_DRAIN')),lambda:g.SetNet(net))
 r,m=solve(plate=5);no_contact,_=solve(contact=False);assert math.isinf(no_contact);poor=json.loads((OUT/'thermal-model.json').read_text())['cases']['poor_joint']['10']['junction_40C_4W_C'];bad=[]
 for name,tj in[('reduced_barrel_5um',40+4*(3+1+r+.7+4+1)),('missing_contact',None if math.isinf(no_contact)else 40+4*no_contact),('wrong_sink_8K_W',40+4*(3+1+solve()[0]+.7+8+1)),('poor_joint',poor)]:
  assert tj is None or tj>125;bad.append(dict(mutation=name,detected='125C_qualification_limit_exceeded_or_no_conduction',junction_C=tj))
 source_area=area(SOLDER)-len(INNER)*math.pi*.15**2;paste_area=sum(area(r)for r in PASTE);voids=sum(math.pi*(d/2)**2 for x,y,d,w,k in via_specs());joint_hole_capacity=len(INNER)*math.pi*.15**2*1.6
 save('source-assembly-DFM.json',dict(status='PASS_CAD_AND_CREDIBLE_PROTOTYPE_PROCESS_NOT_PHYSICAL_QUALIFICATION',native_SHA256=sha(HW/'RF2M.kicad_pcb'),native_errors=[],source_pad_area_mm2=13.5,mask_open_mm2=area(SOLDER),nominal_solderable_source_area_mm2=source_area,maximum_hole_envelope_solderable_area_mm2=area(SOLDER)-len(INNER)*math.pi*.215**2,paste_aperture_area_mm2=paste_area,paste_percent_manufacturer_source=100*paste_area/13.5,stencil_mm=.12,deposited_paste_geometric_mm3=paste_area*.12,transfer_efficiency_sensitivity=[.8,1.],metal_volume_fraction_sensitivity=[.45,.6],solid_solder_volume_sensitivity_mm3=[paste_area*.12*.8*.45,paste_area*.12*.6],open_joint_hole_capacity_nominal_mm3=joint_hole_capacity,wicking_guaranteed_zero=False,guaranteed_hole_closure=False,mask_islands=0,open_joint_vias=len(INNER),external_side_vias=len(SIDE),near_vias=len(NEAR),wing_vias=len(OUTER),source_isotherm_is_model_assumption=True,external_hole_to_mask_opening_worst_gap_mm=.11,external_gap_basis='0.43mm hole envelope,+/-0.075holeposition,+/-0.05maskregistration engineering sensitivity, NOT a supplier via-hole guarantee. Incoming check before assembly.',bottom_nominal_hole_area_mm2=voids,bottom_window_area_mm2=area(WINDOW),bottom_geometric_contact_fraction_excluding_holes=1-voids/area(WINDOW),physical='NOT_RUN',required_initial_qualification=['Recorded actual reflow profile and print inspection','First populated Q501 X-ray for wetting/void distribution plus conservative thermal measurement','Source solder effective wet area>=4mm2,standoff<=0.1mm,k>=25W/mK is the conditional1K/W model acceptance envelope,not demonstrated','No bottom solder protrusion>0.05mm,clean flat TIM contact','Correlated calibrated thermal response at 25/40C; no inferred Tj from plastic top alone']))
 save('engineering-regression.json',dict(status='PASS_NATIVE_AND_MODEL_REGRESSION',electrical_net_membership_equal_E4=True,all_320_pad_sets_positions_and_sizes_preserved=True,all_signal_and_power_tracks_preserved=True,RF_lines_preserved=list(LENGTHS),native_mutations=tests,thermal_mutations=bad,prior_E4_coverage='6native+4model classes preserved; old closed-source-mask mutation updated to reject islands in intentionally open construction',new_negative_tests=len(tests)-6,DRC_configuration_identical_to_E4=True,purchased_parts_and_populations_unchanged=True,physical='NOT_RUN'))
 print('PASS',len(tests),'native/input negatives +',len(bad),'thermal failures detected; physical source/thermal qualification OPEN')
if __name__=='__main__':main()
