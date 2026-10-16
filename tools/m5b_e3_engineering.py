#!/usr/bin/python3
"""Native E2/E3 electricalequivalenceandchangedRF/thermalgeometryregression."""
import pcbnew as p,json,math,copy,xml.etree.ElementTree as ET
from m5b_e3_common import *
def signature(fn):
 root=ET.parse(fn);return {n.get('name'):sorted((a.get('ref'),a.get('pin'))for a in n.findall('node'))for n in root.findall('./nets/net')}
def native(b):
 fs={f.GetReference():f for f in b.GetFootprints()}
 for ref,l in LENGTHS.items():
  f=fs[ref];pads={a.GetNumber():a for a in f.Pads()};dist=(pads['1'].GetPosition()-pads['2'].GetPosition()).EuclideanNorm()/1e6;assert abs(dist-l)<.00001,('TLlength',ref)
  g=[g for g in f.GraphicalItems()if g.GetLayer()==p.F_Cu];assert len(g)==1;box=g[0].GetBoundingBox();assert abs(p.ToMM(box.GetHeight())-WIDTH)<.00001,('TLwidth',ref)
  assert not any(a.IsOnLayer(p.F_Mask)or a.IsOnLayer(p.F_Paste)for a in pads.values())
 source=[t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)and abs(p.ToMM(t.GetPosition().x)-112)<1 and abs(p.ToMM(t.GetPosition().y)-55)<2.2];assert len(source)==32,'sourcecount'
 for v in source:assert not v.IsTented(p.B_Mask)and v.GetNetname()=='GND'and abs(p.ToMM(v.GetWidth(p.F_Cu))-.8)<.001 and abs(p.ToMM(v.GetDrillValue())-.3)<.001,'sourcevia'
 s=next(a for a in fs['Q501'].Pads()if a.GetNumber()=='S');assert not s.IsOnLayer(p.F_Mask),'unmaskedsourceholes'
 for ob in list(b.GetTracks())+[a for f in b.GetFootprints()for a in f.Pads()]:
  if ob.GetNetname()=='GND'or not ob.IsOnLayer(p.B_Cu):continue
  box=ob.GetBoundingBox();assert not(p.ToMM(box.GetRight())>=105 and p.ToMM(box.GetLeft())<=119 and p.ToMM(box.GetBottom())>=49 and p.ToMM(box.GetTop())<=61),'foreignthermalcopper'
 for ref,drill in[('J101',1.3),('J301',1.8)]:assert all(abs(p.ToMM(a.GetDrillSize().x)-drill)<.001 for a in fs[ref].Pads()),('connectorhole',ref)
 return fs,source

def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs,source=native(b);oldparts={a['ref']:a for a in json.loads(gitfile('hardware/2m/RF2M.electrical.json'))['parts']};parts={a['ref']:a for a in json.loads((HW/'RF2M.electrical.json').read_text())['parts']};assert parts.keys()==oldparts.keys()
 for r,a in parts.items():
  for key in['mpn','pins','population','group','price_breaks_eur']:assert a[key]==oldparts[r][key],('electrical/populationchange',r,key)
  if r not in LENGTHS:assert a['value']==oldparts[r]['value'],('purchasedvalue',r)
 assert signature(OUT/'RF2M.net.xml')==signature(HW/'review/M5B-E2/RF2M.net.xml'),'netschanged'
 # Realnativepad/dimensioncomparison:onlytwofinished-holemarginschange.
 fn=OUT/'development/E2-native.kicad_pcb';old=p.LoadBoard(str(fn));ofs={f.GetReference():f for f in old.GetFootprints()};padchanges=[]
 for r,f in fs.items():
  if r.startswith('TL'):continue
  for a in f.Pads():
   other=min((q for q in ofs[r].Pads()if q.GetNumber()==a.GetNumber()),key=lambda q:((q.GetPosition()-ofs[r].GetPosition())-(a.GetPosition()-f.GetPosition())).EuclideanNorm());assert a.GetNetname()==other.GetNetname(),('padnet',r,a.GetNumber());assert a.GetShape()==other.GetShape(),('padshape',r)
   delta=(a.GetPosition()-f.GetPosition())-(other.GetPosition()-ofs[r].GetPosition());assert delta.EuclideanNorm()<100,('relativepadplacement',r)
   if a.GetSize()!=other.GetSize()or a.GetDrillSize()!=other.GetDrillSize():
    assert r in['J101','J301'],('unexpectedlandingchange',r);padchanges.append(dict(ref=r,pad=a.GetNumber(),drill_mm=p.ToMM(a.GetDrillSize().x),land_mm=[p.ToMM(a.GetSize().x),p.ToMM(a.GetSize().y)]))
 def tracks(board):
  return {t.m_Uuid.AsString():dict(net=t.GetNetname(),type=t.GetClass(),layer=t.GetLayerName(),start_mm=[p.ToMM(t.GetStart().x),p.ToMM(t.GetStart().y)],end_mm=[p.ToMM(t.GetEnd().x),p.ToMM(t.GetEnd().y)],width_mm=p.ToMM(t.GetWidth(p.F_Cu)if isinstance(t,p.PCB_VIA)else t.GetWidth()),drill_mm=p.ToMM(t.GetDrillValue())if isinstance(t,p.PCB_VIA)else None)for t in board.GetTracks()}
 before,after=tracks(old),tracks(b)
 save('E2-E3-native-layout-delta.json',dict(baseline_commit=BASE,modified={k:dict(before=before[k],after=after[k])for k in before.keys()&after.keys()if before[k]!=after[k]},added={k:after[k]for k in after.keys()-before.keys()},removed={k:before[k]for k in before.keys()-after.keys()},footprint_moves=[dict(ref=r,from_mm=[p.ToMM(ofs[r].GetPosition().x),p.ToMM(ofs[r].GetPosition().y)],to_mm=[p.ToMM(f.GetPosition().x),p.ToMM(f.GetPosition().y)])for r,f in fs.items()if(f.GetPosition()-ofs[r].GetPosition()).EuclideanNorm()>100],electrical_net_membership_unchanged=True))
 mutations=[]
 f=fs['TL608'];pa=next(a for a in f.Pads()if a.GetNumber()=='2');oldpos=pa.GetPosition();pa.SetPosition(oldpos+p.VECTOR2I(p.FromMM(.2),0))
 try:native(b)
 except AssertionError:mutations.append('TL608electrical_length')
 else:raise AssertionError('lengthmutationescaped')
 pa.SetPosition(oldpos);via=source[0];oldnet=via.GetNet();via.SetNet(b.FindNet('PA_DRAIN'))
 try:native(b)
 except AssertionError:mutations.append('sourcevia_to_drain')
 else:raise AssertionError('sourcephysicalmutationescaped')
 via.SetNet(oldnet);oldsize=via.GetWidth(p.F_Cu);via.SetWidth(p.FromMM(.6))
 try:native(b)
 except AssertionError:mutations.append('thermal_source_old_land')
 else:raise AssertionError('thermalmutationescaped')
 via.SetWidth(oldsize)
 # Range/thermal/powercalculationsareboundedmodels,notphysicalpasses.
 paths=json.loads((OUT/'power-native-main-paths.json').read_text());assert len(paths['paths'])==11 and all(x['drop_bound_V']<.35 for x in paths['paths'])
 rf=json.loads((OUT/'RF-analysis.json').read_text());assert abs(rf['nominal']['Z0_ohm']-50)<.1 and WIDTH>2.5
 save('engineering-regression.json',dict(status='PASS_NATIVE_ELECTRICAL_AND_GEOMETRY_CHECKS',net_membership_identical_to_E2=True,purchased_MPN_values_populations_prices_unchanged=True,RF_line_changes=list(LENGTHS),connector_pad_changes=padchanges,all_other_package_copper_geometry_preserved=True,additional_native_mutations=mutations,main_power_paths=11,source_vias=32,physical='NOT_RUN'))
 print('PASSnativeE3RF/thermalgeometry,E2electricalequivalenceand3additionalphysicalmutations')
if __name__=='__main__':main()
