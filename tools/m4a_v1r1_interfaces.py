#!/usr/bin/python3
"""Native connector/physical maps, frozen-controller comparison and local copper delta."""
import copy,xml.etree.ElementTree as ET,re
from m4a_v1r1_common import *
EXPECTED={'J101':dict(zip(map(str,range(1,17)),['V3V3','GND','SCL','GND','SDA','LEASE','ARM','CW_KEY','PA_REQ','FOX_REQ','PWR0','PWR1','MUTE_N','FAULT_N','PACK4_OK','GND'])),
 'J301':{'1':'VBAT','2':'GND'},'J401':{'1':'RF_NORMAL','2':'GND'},'J502':{'1':'RF_FOX','2':'GND','3':'FOX_ID'},
 'Q403':{'1':'SHAPE_BASE','2':'VPA_SHAPED','3':'VPA_LOAD'},'U311':{'1':'VREF_2V5','2':'VREF_2V5','3':'GND'}}
def xmlpins(path,ref):
 root=ET.parse(path).getroot();return {a.get('pin'):n.get('name')for n in root.findall('nets/net')for a in n.findall('node')if a.get('ref')==ref}
def check(b,manifest):
 errors=[];fs={f.GetReference():f for f in b.GetFootprints()}
 for r,want in EXPECTED.items():
  if {a.GetNumber():a.GetNetname()for a in fs[r].Pads()}!=want:errors.append(r+':physical_pin_map')
 f=fs['J101'];xy={a.GetNumber():[pcb.ToMM(v)for v in a.GetFPRelativePosition()]for a in f.Pads()}
 for i in range(1,17):
  # Maker/component-top and carrier-top view: odd row X0, even row X2.54.
  if xy[str(i)]!=[0.0 if i%2 else 2.54,2.54*((i-1)//2)]:errors.append('J101:physical_orientation')
 if f.IsFlipped()or abs(f.GetOrientationDegrees())>.001:errors.append('J101:physical_orientation')
 parts={a['ref']:a for a in manifest['parts']}
 for r in ['R228','R348','R349']:
  if parts[r]['population']!='FOX':errors.append(r+':FOX_only_population_link')
 return errors

def main():
 frozen();path=P/(NAME+'.kicad_pcb');b=pcb.LoadBoard(str(path));manifest=json.loads((P/(NAME+'.electrical.json')).read_text());assert not check(b,manifest),check(b,manifest)
 for r in EXPECTED:assert xmlpins(D/(NAME+'.xml'),r)==EXPECTED[r],r
 ctrl=R/'hardware/controller';cb=pcb.LoadBoard(str(ctrl/'CTRL.kicad_pcb'));cf=next(f for f in cb.GetFootprints()if f.GetReference()=='J4');cp={a.GetNumber():a.GetNetname()for a in cf.Pads()};assert cp==xmlpins(ctrl/'review/M6-L1/CTRL.net.xml','J4')
 rows=[]
 for pin,n in EXPECTED['J101'].items():
  want='V3V3_RF80'if n=='V3V3'else'GND'if n=='GND'else'RF80_'+n
  assert cp[pin]==want,(pin,cp[pin],want);rows.append(dict(pin=int(pin),RF80_J101=n,controller_J4=cp[pin]))
 save('controller-compatibility.json',dict(status='PASS_16_NATIVE_AND_EXPORTED_PINS',controller_revision='d94dabd0e40137dc44b2bb94f3707ad4636ca65f / M6-L1, read-only',RF80_native_sha256=sha(path),controller_native_sha256=sha(ctrl/'CTRL.kicad_pcb'),rows=rows,mating='Wurth61201623021 female IDC; keyed straight-through ribbon pin1-to-pin1. Verify cable continuity at both ends, not red stripe alone.',geometry='RF80 J101 component top view, rotation0: pin1 at(27,55),pin2 at(29.54,55); odd pins along+Y at2.54mm. No footprint flip or pad-centre change.',electrical='3.3V nominal,3.135-3.465V; connector abs3.6V. FAULT_N open drain, low while disarmed; controller input is not module-presence proof. Native local pulldowns and controller isolation unchanged.',protocol='LEASE application progress; ARM0/MUTE_N0 before retune/path changes; I2C clocks while armed disarm locally; >=1.5ms quiet then deliberate ARM cycle, valid PACK4_OK only after pack validation. PA_REQ/FOX_REQ exclusive, PWR truth table retained in logic-results.json.',power='J301 separate fused protected pack:1VBAT/2GND. No PA current through ribbon. Full population requires4S/PACK4_OK; Fox-only2S or4S bounded by existing contract.',backfeed='Controller branch isolation and local RF80 input topology unchanged and regressions retained. Cable/power-sequencing measurements NOT_RUN.'))
 tests=[]
 def reject(n,fn,code):
  q=pcb.LoadBoard(str(path));m=copy.deepcopy(manifest);fn(q,m);e=check(q,m);assert code in e,(n,e);tests.append(dict(mutation=n,detected=code))
 def pa(q,r,n):return next(a for f in q.GetFootprints()if f.GetReference()==r for a in f.Pads()if a.GetNumber()==n)
 def swap(q,r,a,c):
  x,y=pa(q,r,a),pa(q,r,c);nx,ny=x.GetNetCode(),y.GetNetCode();x.SetNetCode(ny);y.SetNetCode(nx)
 reject('BD140_base_emitter_swapped',lambda q,m:swap(q,'Q403','1','3'),'Q403:physical_pin_map')
 reject('TL431_reference_anode_swapped',lambda q,m:swap(q,'U311','2','3'),'U311:physical_pin_map')
 reject('IDC_mirrored',lambda q,m:next(f for f in q.GetFootprints()if f.GetReference()=='J101').Flip(pcb.VECTOR2I(pcb.FromMM(27),pcb.FromMM(55)),False),'J101:physical_orientation')
 reject('IDC_SDA_SCL_swapped',lambda q,m:swap(q,'J101','3','5'),'J101:physical_pin_map')
 reject('battery_reversed',lambda q,m:swap(q,'J301','1','2'),'J301:physical_pin_map')
 reject('RF_output_swapped',lambda q,m:swap(q,'J401','1','2'),'J401:physical_pin_map')
 for r in ['R228','R348','R349']:
  reject(r+'_Fox_link_removed',lambda q,m,r=r:next(a for a in m['parts']if a['ref']==r).__setitem__('population','NORMAL'),r+':FOX_only_population_link')
 save('interface-regression.json',dict(status='PASS',mutations=tests))
 # Compare filled copper polygons, not merely zone outlines.
 oldpath=Path('/tmp/m4av1r1/baseline.kicad_pcb');oldpath.write_bytes(gitfile('hardware/80m/production/RF80_V1.kicad_pcb'));old=pcb.LoadBoard(str(oldpath));delta=[]
 for layer in [pcb.F_Cu,pcb.B_Cu]:
  def union(board):
   z=pcb.SHAPE_POLY_SET()
   for a in board.Zones():
    if not a.GetIsRuleArea()and a.IsOnLayer(layer):z.BooleanAdd(a.GetFilledPolysList(layer))
   return z
  a,c=union(old),union(b);z=pcb.SHAPE_POLY_SET(a);z.BooleanXor(c)
  box=z.BBox();bb=[pcb.ToMM(v)for v in [box.GetX(),box.GetY(),box.GetRight(),box.GetBottom()]]if z.OutlineCount()else None
  clip=pcb.SHAPE_POLY_SET();clip.NewOutline()
  for x,y in [(148,120),(157,120),(157,124),(148,124)]:clip.Append(pcb.FromMM(x),pcb.FromMM(y))
  local=pcb.SHAPE_POLY_SET(z);local.BooleanIntersection(clip);outside=pcb.SHAPE_POLY_SET(z);outside.BooleanSubtract(clip)
  assert outside.Area()/1e12<.00001,('Material nonlocal filled-copper change',layer,outside.Area()/1e12)
  delta.append(dict(layer=pcb.LayerName(layer),symmetric_difference_mm2=z.Area()/1e12,all_difference_bounds_mm=bb,local_J502_region_mm=[148,120,157,124],outside_region_difference_mm2=outside.Area()/1e12,comparison_resolution='Native1nm integer polygon roundoff produces zero-width-to-nm edge strips elsewhere; total outside delta <0.00001mm2, not a DRC exclusion. Tracks/vias/pads compared exactly separately.'))
 save('local-copper-delta.json',dict(status='PASS_ONLY_J502_LOCAL_CLEARANCE_CHANGE',baseline=BASE,layer_deltas=delta,all_signal_tracks_and_vias='Byte-value geometry identical; V1-layout-preservation.json',reason='Three J502 lands enlarged by0.20mm in X to preserve0.30mm nominal annulus around1.30mm holes. Refilled GND clearance local to J502. No RF topology/value/return-path relocation.',physical_RF='NOT_RUN'))
 # Artwork aperture widths and outline centreline from the final Gerbers.
 silk=[]
 for file in sorted((D/'gerbers').glob('*.g?o')):
  widths=[float(v)for v in re.findall(r'%ADD\d+C,([\d.]+)\*%',file.read_text())]
  assert all(v>=.1499 for v in widths),(file,widths);silk.append(dict(file=file.name,circular_stroke_apertures_mm=widths))
 edge=(D/'gerbers'/(NAME+'-Edge_Cuts.gm1')).read_text();pts=[(int(x)/1e6,-int(y)/1e6)for x,y in re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',edge)]
 box=[min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)];assert box==[20,20,170,130],box
 labels=[dict(text=x.GetText(),height_mm=pcb.ToMM(x.GetTextHeight()),stroke_mm=pcb.ToMM(x.GetTextThickness()),position_mm=[pcb.ToMM(v)for v in x.GetPosition()])for x in b.GetDrawings()if isinstance(x,pcb.PCB_TEXT)and x.GetLayer()in[pcb.F_SilkS,pcb.B_SilkS]]
 assert len(labels)==26 and all(x['height_mm']>=1 and x['stroke_mm']>=.15 for x in labels)
 save('silkscreen-audit.json',dict(status='PASS_NATIVE_AND_FINAL_GERBER',essential_marks=labels,Gerber_stroke_audit=silk,outline_centreline_mm=box,finished_dimensions_mm=[150,110],outline_stroke_is_not_board_size='Factory must route closed Edge.Cuts centreline; stroke envelope must not enlarge150x110mm',references_and_small_body_art='Moved to F.Fab/assembly overlays; not required on finished legend. DRC and independent native polygon gate check mask clearance.'))
 print('PASS 16 controller pins,',len(tests),'new interface mutations; copper delta',delta,';26 markings/actual Gerber apertures/outline')
if __name__=='__main__':main()
