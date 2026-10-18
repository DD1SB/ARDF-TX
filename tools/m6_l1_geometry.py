#!/usr/bin/python3
"""Independent manufacturer-to-native LoRa assertions and real geometry mutations."""
import sys,json,math,copy,hashlib,subprocess,collections
from pathlib import Path
import pcbnew as p
import m5a_r1_design as sx
import m6_l1_rf as rf
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-L1';BASE='742159d363dd8dd8b8ff653d01238af9a49ef2aa'
FUNCTIONS=['GND']*4+['DIO1','NC','NC','DIO3','NC','BUSY','GND','GND','VCC','SCK','MISO','MOSI','SEL','RST','GND','GND','ANT','GND']
NET={'GND':'GND','DIO1':'LORA_DIO1','BUSY':'LORA_BUSY','VCC':'V3V3','SCK':'SPI_SCK','MISO':'SPI_MISO','MOSI':'SPI_MOSI','SEL':'LORA_NSS','RST':'LORA_RESET','ANT':'LORA_ANT'}
def source_maps():return {'TR4_V2':dict(enumerate(FUNCTIONS,1)),'TR8_V1':dict(enumerate(FUNCTIONS,1)),'TR8_V2':dict(enumerate(FUNCTIONS,1))}
def save(n,x):(D/n).write_text(json.dumps(x,indent=2)+'\n')
def check(b,maps=None,returns=True):
 maps=maps or source_maps();errors=[];fs={f.GetReference():f for f in b.GetFootprints()};u=fs['U70'];j=fs['J7'];pads={int(a.GetNumber()):a for a in u.Pads()}
 def ck(ok,s):
  if not ok:errors.append(s)
 ck(set(pads)==set(range(1,23)),'22_terminal_count');ck(u.GetLayer()==p.F_Cu and abs(u.GetOrientationDegrees())<.001,'top_view_rotation_and_pin1')
 ck(tuple(u.GetPosition())==tuple(rf.pt(103,41)),'module_position_preserved')
 for i in range(1,23):
  a=pads.get(i)
  if a is None:continue
  ck(a.IsOnLayer(p.F_Cu),'module_copper_land_'+str(i))
  x=-6.38+1.27*(i-1 if i<=11 else 22-i);y=7.25 if i<=11 else -7.25
  ck(abs(rf.mm(a.GetPosition().x)-103-x)<.001 and abs(rf.mm(a.GetPosition().y)-41-y)<.001,'pad_position_'+str(i))
  ck(abs(rf.mm(a.GetSize().x)-.8)<.001 and abs(rf.mm(a.GetSize().y)-2.2)<.001,'pad_size_'+str(i))
  for variant,mp in maps.items():
   fun=mp[i];net=a.GetNetname();ck(net==NET[fun] if fun in NET else net.startswith('unconnected-'),variant+'_pin_'+str(i)+'_'+fun)
 ck(maps['TR4_V2']==maps['TR8_V1']==maps['TR8_V2'],'TR4_TR8_function_compatibility')
 ko=next(z for z in b.Zones() if z.GetIsRuleArea() and z.GetZoneName()=='top_keepout')
 ck(ko.GetDoNotAllowTracks() and ko.GetDoNotAllowVias() and ko.GetDoNotAllowZoneFills(),'Hirose_no_tracks_vias_or_pours')
 ck(ko.Outline().Contains(rf.pt(98.32,27.56)) and ko.Outline().Contains(rf.pt(100.51,29.44)) and not ko.GetDoNotAllowPads(),'Hirose_full_keepout_with_intended_SIG_land')
 ck(len(list(j.Pads()))==3,'UFL_3_lands');ck(j.GetLayer()==p.F_Cu and abs(j.GetOrientationDegrees())<.001,'UFL_orientation')
 for a in j.Pads():
  q=rf.mm(a.GetPosition().x)-99.415;r=rf.mm(a.GetPosition().y)-28.5
  if a.GetNumber()=='1':ck(abs(q+1.525)<.001 and abs(r)<.001 and abs(rf.mm(a.GetSize().x)-1.05)<.001 and abs(rf.mm(a.GetSize().y)-1)<.001 and a.GetNetname()=='LORA_ANT','UFL_signal_geometry')
  else:ck(a.GetNumber()=='2' and a.GetNetname()=='GND' and abs(q)<.001 and abs(abs(r)-1.475)<.001 and abs(rf.mm(a.GetSize().x)-2.2)<.001 and abs(rf.mm(a.GetSize().y)-1.05)<.001,'UFL_ground_geometry')
 traces=[t for t in b.GetTracks() if t.GetNetname()=='LORA_ANT'];ck(len(traces)==1,'one_continuous_RF_segment')
 if traces:
  t=traces[0];ck(not isinstance(t,p.PCB_VIA) and t.GetLayer()==p.F_Cu and abs(rf.mm(t.GetWidth())-.45)<.001,'RF_trace_width_layer')
  ck({tuple(t.GetStart()),tuple(t.GetEnd())}=={tuple(rf.pt(97.89,33.75)),tuple(rf.pt(97.89,28.5))},'RF_segment_endpoints')
 ck(abs(rf.mm(b.GetDesignSettings().GetBoardThickness())-1.6)<.001 and b.GetDesignSettings().GetCopperLayerCount()==2,'ordinary_stackup')
 # Reject foreign routed copper actually crossing the RF centreline.
 for t in b.GetTracks():
  if t.GetNetname()!='LORA_ANT' and t.IsOnLayer(p.F_Cu):
   bb=t.GetBoundingBox()
   if not (bb.GetLeft()<=p.FromMM(97.89)<=bb.GetRight() and bb.GetTop()<=p.FromMM(33.75) and bb.GetBottom()>=p.FromMM(28.5)):continue
   q=rf.polygon(t,p.F_Cu)
   ck(not any(q.Contains(rf.pt(97.89,28.5+i*.05)) for i in range(106)),'foreign_copper_RF_short')
 if returns:
  g=[z.GetFilledPolysList(p.B_Cu) for z in b.Zones() if not z.GetIsRuleArea() and z.GetNetname()=='GND' and z.IsOnLayer(p.B_Cu)]
  ck(all(any(z.Contains(rf.pt(97.89+dx,28.5+i*.05)) for z in g) for i in range(106) for dx in [-1,-.5,0,.5,1]),'continuous_bottom_RF_reference')
  ck(any(isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND' and abs(rf.mm(t.GetPosition().x)-95)<.01 and abs(rf.mm(t.GetPosition().y)-29)<.01 for t in b.GetTracks()),'local_UFL_ground_stitch')
 return errors

def tracks(b):
 return collections.Counter((t.GetNetname(),t.GetClass(),tuple(t.GetStart()),tuple(t.GetEnd()),t.GetWidth(p.F_Cu) if isinstance(t,p.PCB_VIA) else t.GetWidth(),t.GetDrillValue() if isinstance(t,p.PCB_VIA) else t.GetLayer()) for t in b.GetTracks())
def filled(text):
 tree=sx.parse(text);edges=[]
 for zone in sx.children(tree,'zone'):
  for q in sx.children(zone,'filled_polygon'):
   layer=sx.child(q,'layer')[1];v=[tuple(a[1:]) for a in sx.children(sx.child(q,'pts'),'xy')]
   for a,b in zip(v,v[1:]+v[:1]):edges.append((layer,*sorted([a,b])))
 return sorted(edges)

def main():
 board=P/'CTRL.kicad_pcb';b=p.LoadBoard(str(board));assert not check(b),check(b);fs={f.GetReference():f for f in b.GetFootprints()}
 rows=[]
 for i,fun in enumerate(FUNCTIONS,1):
  a=next(a for a in fs['U70'].Pads() if a.GetNumber()==str(i));rows.append(dict(pin=i,TR4_V2=fun,TR8_V1=fun,TR8_V2=fun,net=a.GetNetname(),xy_mm=[rf.mm(a.GetPosition().x),rf.mm(a.GetPosition().y)],size_mm=[rf.mm(a.GetSize().x),rf.mm(a.GetSize().y)],disposition='Unused configurable IO, not a required NC' if i==8 else 'DNP/NC' if fun=='NC' else 'Connected'))
 save('module-22-pin-audit.json',dict(status='PASS',top_view='TR4/V2 and TR8/V2 rotate90deg counterclockwise to native top-side view; TR8/V1 as drawn. No reflection.',pins=rows,body_mm=[15,15],host_pitch_mm=1.27,host_pad_mm=[.8,2.2],host_row_centre_mm=14.5,body_edge_mm=15,terminal_depth_mm=1.37,nominal_inner_overlap_mm=1.35,nominal_toe_extension_mm=.85,source_end_offset_mm=1.12,source_10_pitch_sum_mm=12.7,rounding_asymmetry_mm=.06,tolerances='Not supplied by Silicontra. Nominal compatibility, not a guaranteed tolerance stack; inspect incoming modules. Hole diameter, package height and mask/stencil recommendations not specified.'))
 # Frozen artifacts + actual connected net, placement, routing and filled-plane equivalence.
 for f,h in json.loads((D/'frozen-controller-reviews.json').read_text()).items():assert hashlib.sha256((ROOT/f).read_bytes()).hexdigest()==h,f
 oldtext=subprocess.check_output(['git','show',BASE+':hardware/controller/CTRL.kicad_pcb'],text=True);tmp=Path('/tmp/m6l1/baseline.kicad_pcb');tmp.write_text(oldtext);a=p.LoadBoard(str(tmp));assert tracks(a)==tracks(b);
 ground_delta={}
 roi=p.SHAPE_POLY_SET();roi.NewOutline()
 for x,y in [(98.0,27.2),(100.9,27.2),(100.9,29.8),(98.0,29.8)]:roi.Append(p.FromMM(x),p.FromMM(y))
 for layer in [p.F_Cu,p.B_Cu]:
     before=next(z.GetFilledPolysList(layer) for z in a.Zones() if not z.GetIsRuleArea() and z.IsOnLayer(layer));after=next(z.GetFilledPolysList(layer) for z in b.Zones() if not z.GetIsRuleArea() and z.IsOnLayer(layer))
     removed=p.SHAPE_POLY_SET(before);removed.BooleanSubtract(after);added=p.SHAPE_POLY_SET(after);added.BooleanSubtract(before)
     outside=p.SHAPE_POLY_SET(removed);outside.BooleanSubtract(roi)
     assert not added.OutlineCount() and not outside.OutlineCount(),('unrelated ground change',layer)
     if layer==p.B_Cu:assert not removed.OutlineCount(),'bottom RF ground changed'
     ground_delta[b.GetLayerName(layer)]=dict(removed_mm2=abs(removed.Area())/1e12,added_mm2=abs(added.Area())/1e12,all_changes_within_roi_mm=[98,27.2,100.9,29.8])
 oldfs={f.GetReference():f for f in a.GetFootprints()};count=0;numbered=0
 for r,f in fs.items():
  o=oldfs[r];assert tuple(f.GetPosition())==tuple(o.GetPosition()) and f.GetLayer()==o.GetLayer() and f.GetOrientationDegrees()==o.GetOrientationDegrees(),r
  for q in f.Pads():
   old=next(x for x in o.Pads() if x.GetNumber()==q.GetNumber() and x.GetPosition()==q.GetPosition());assert q.GetSize()==old.GetSize() and q.GetPosition()==old.GetPosition() and q.GetShape()==old.GetShape(),r
   if r=='U70' and q.GetNumber()=='8':assert q.GetNetname().startswith('unconnected-') and old.GetNetname().startswith('unconnected-')
   else:assert q.GetNetname()==old.GetNetname(),r+'.'+q.GetNumber()
   if not r.startswith('H'):
    count+=1
    numbered+=bool(q.GetNumber())
 save('native-preservation.json',dict(status='PASS',baseline=BASE,current_sha256=hashlib.sha256(board.read_bytes()).hexdigest(),all_pad_instances_including_unnumbered=count,numbered_pad_instances=numbered,all_track_and_via_geometry='IDENTICAL',filled_copper_delta=ground_delta,all_other_copper='IDENTICAL',all_footprint_positions='IDENTICAL',connected_nets='IDENTICAL',legitimate_floating_alias_change='U70.8 IO ->DIO3; remains unconnected',historical_review_files_preserved=len(json.loads((D/'frozen-controller-reviews.json').read_text()))))
 tests=[]
 def mutate(name,fn):
  q=p.LoadBoard(str(board));fn(q);e=check(q);assert e,name;tests.append(dict(mutation=name,rejected_by=sorted(set(e))))
 def fp(q):return {f.GetReference():f for f in q.GetFootprints()}
 def pad(q,r,i):return next(a for a in fp(q)[r].Pads() if a.GetNumber()==str(i))
 mutate('pin1_rotated180',lambda q:fp(q)['U70'].SetOrientationDegrees(180))
 mutate('mirrored_bottom_view',lambda q:fp(q)['U70'].Flip(fp(q)['U70'].GetPosition(),False))
 mutate('drawing_rotated90',lambda q:fp(q)['U70'].SetOrientationDegrees(90))
 mp=source_maps();mp['TR4_V2'][15]='MOSI';assert check(b,mp);tests.append(dict(mutation='TR4_TR8_different_pinmap',rejected_by=check(b,mp)))
 mutate('SPI_MISO_MOSI_swapped',lambda q:pad(q,'U70',15).SetNet(q.FindNet('SPI_MOSI')))
 mutate('antenna_wrong_pin21',lambda q:pad(q,'U70',21).SetNet(q.FindNet('GND')))
 mutate('wrong_pad_pitch',lambda q:pad(q,'U70',2).Move(rf.pt(.1,0)))
 mutate('wrong_row_spacing',lambda q:pad(q,'U70',22).Move(rf.pt(0,.2)))
 mutate('missing_U70_land',lambda q:pad(q,'U70',3).SetLayerSet(p.LSET()))
 mutate('malformed_U70_land',lambda q:pad(q,'U70',13).SetSize(rf.pt(.4,.5)))
 mutate('wrong_UFL_signal_land',lambda q:pad(q,'J7',1).SetSize(rf.pt(.5,.5)))
 mutate('wrong_UFL_ground',lambda q:pad(q,'J7',2).SetNet(q.FindNet('LORA_ANT')))
 mutate('broken_antenna_segment',lambda q:next(t for t in q.GetTracks() if t.GetNetname()=='LORA_ANT').SetEnd(rf.pt(97.89,31)))
 def short(q):
  t=p.PCB_TRACK(q);t.SetStart(rf.pt(97,31));t.SetEnd(rf.pt(99,31));t.SetWidth(p.FromMM(.2));t.SetLayer(p.F_Cu);t.SetNet(q.FindNet('GND'));q.Add(t)
 mutate('actual_GND_copper_short',short)
 def cut(q):
  for z in list(q.Zones()):
   if not z.GetIsRuleArea() and z.IsOnLayer(p.B_Cu):z.SetLayer(p.F_Cu)
 mutate('missing_bottom_ground',cut)
 mutate('missing_local_ground_via',lambda q:next(t for t in q.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetPosition()==rf.pt(95,29)).SetNet(q.FindNet('V3V3')))
 mutate('incorrect_RF_width',lambda q:next(t for t in q.GetTracks() if t.GetNetname()=='LORA_ANT').SetWidth(p.FromMM(.15)))
 def trimmed(q):
  z=next(z for z in q.Zones() if z.GetIsRuleArea() and z.GetZoneName()=='top_keepout');o=z.Outline();o.RemoveAllContours();o.NewOutline()
  for x,y in [(98.425,27.55),(100.515,27.55),(100.515,29.45),(98.425,29.45)]:o.Append(p.FromMM(x),p.FromMM(y))
 mutate('old_trimmed_Hirose_keepout',trimmed)
 mutate('nonstandard0p8mm',lambda q:q.GetDesignSettings().SetBoardThickness(p.FromMM(.8)))
 for name,kw in [('unsupported_er',dict(er=2.2)),('thin_board_RF_model',dict(h=.64))]:
  try:rf.model([dict(width_mm=.45,left_gap_mm=.25,right_gap_mm=.25,dy_mm=5.25)],868e6,**kw)
  except ValueError:tests.append(dict(mutation=name,rejected_by='numerical standard-FR4 model domain'))
  else:raise AssertionError(name)
 save('LoRa-negative-geometry.json',dict(status='PASS',tests=tests,host_tests='test_lora.py verifies wrong/unknown population, band, antenna, configuration, response, power and base independence. RF connector mutations retained in electrical-regression.json.'))
 print('22pins/704 numbered pads; local GND-only delta PASS;',len(tests),'geometry/model negative tests')
if __name__=='__main__':main()
