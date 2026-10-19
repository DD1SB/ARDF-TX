#!/usr/bin/python3
"""Retained block routing and local offline Specctra support for E5 only."""
import argparse,re,math,collections
from m5b_e5_common import *
REMOVED=[]
def uid(x):return x.m_Uuid.AsString()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['prepare','restore','dsn','import','repair']);ap.add_argument('--report');ap.add_argument('--session');a=ap.parse_args();guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};work=OUT/'development'
 if a.action=='prepare':
  # The digital source buffer moved separately from the 50ohm filter. Its old
  # CLK_NORMAL input wire is re-routed; it is not an ST matching element.
  removed=[]
  for t in list(b.GetTracks()):
   if t.GetNetname()=='CLK_NORMAL':removed.append(uid(t));b.Remove(t);REMOVED.append(t)
  fs['R509'].Move(pt(2,1));
  # Reference fields remain available on assembly layers without crowding the
  # compact mandatory board legend. No copper/courtyard geometry is edited.
  for f in fs.values():
   if f.Reference().GetLayer()in[p.F_SilkS,p.B_SilkS]:f.Reference().SetLayer(p.F_Fab)
  save('source-input-local-change.json',dict(digital_wire_removed_for_reroute=removed,clock_filter_component_values='unchanged',RFmatching='rigid -20mmX translation',R509_additional_move_mm=[2,1],reference_text='Moved to Fab, copper and package geometry unchanged'))
 elif a.action=='restore':
  old=p.LoadBoard(str(work/'E4R1-baseline.kicad_pcb'));of={f.GetReference():f for f in old.GetFootprints()};parts=json.loads((HW/'RF2M.electrical.json').read_text())['parts'];netrefs=collections.defaultdict(set)
  for f in parts:
   if f['ref']in fs:
    for n in f['pins'].values():netrefs[n].add(f['ref'])
  existing={uid(t)for t in b.GetTracks()};by=collections.defaultdict(list)
  for t in old.GetTracks():by[t.GetNetname()].append(t)
  restored=[]
  for net,refs in netrefs.items():
   if net in['GND','CLK_NORMAL']or len(refs)<2:continue
   shifts={(round(xy(fs[r].GetPosition())[0]-xy(of[r].GetPosition())[0],5),round(xy(fs[r].GetPosition())[1]-xy(of[r].GetPosition())[1],5))for r in refs}
   if len(shifts)!=1 or any(fs[r].GetOrientationDegrees()!=of[r].GetOrientationDegrees()for r in refs):continue
   dx,dy=next(iter(shifts));tracks=by[net]
   if not tracks:continue
   def inside(t):
    z=t.GetBoundingBox();return p.ToMM(z.GetX())+dx>=20.6 and p.ToMM(z.GetY())+dy>=20.6 and p.ToMM(z.GetRight())+dx<=169.4 and p.ToMM(z.GetBottom())+dy<=129.4
   if not all(inside(t)for t in tracks):continue
   for t in tracks:
    if uid(t)in existing:continue
    q=t.Duplicate();q.SetParent(b);q.SetUuid(t.m_Uuid);q.SetNet(b.FindNet(net));q.Move(pt(dx,dy));q.SetLocked(True);b.Add(q);existing.add(uid(q));restored.append(dict(uuid=uid(q),net=net,translation_mm=[dx,dy]))
  save('restored-block-routing.json',dict(restored=restored,nets=len({x['net']for x in restored}),note='Only complete uniformly translated net trees inside target outline; collisions are checked next and affected ordinary nets re-routed. RF matching protected separately.'))
 elif a.action=='repair':
  drc=json.loads(Path(a.report).read_text());items={uid(t):t for t in b.GetTracks()};critical={'DRIVER_IN','MMIC_RF_DC','MMIC_COUPLED','MMIC_AC','PA_GATE','PA_DRAIN','NORMAL_RF'}|{n for n in b.GetNetsByName()if str(n).startswith(('ST_','LPF_'))};remove=set();reasons=[]
  for case in drc['violations']:
   if case['severity']!='error'or case['type']not in['clearance','shorting_items','hole_clearance','solder_mask_bridge','copper_edge_clearance']:continue
   choices=[items[z['uuid']]for z in case['items']if z['uuid']in items and items[z['uuid']].GetNetname()not in critical]
   if not choices:continue
   pick=choices[-1];net=pick.GetNetname()
   if net=='GND':
    x,y=xy(pick.GetPosition());assert not(89<x<95 and 48<y<62),'Never remove a source thermal via';remove.add(uid(pick))
   else:remove|={uid(t)for t in b.GetTracks()if t.GetNetname()==net}
   reasons.append(dict(reason=case['type'],net=net))
  for u in remove:q=items[u];b.Remove(q);REMOVED.append(q)
  save('routing-clearance-repair.json',dict(removed_objects=sorted(remove),reasons=reasons,critical_RF_preserved=True));print('Removed',len(remove),'clashing routing objects for actual re-route',flush=True)
 elif a.action=='dsn':
  import m5a_r1_design as cad
  # Use native routing areas, but not zones or manual GND trees as hundreds of
  # requested routes. They remain in the PCB and are independently verified.
  omitted=[z for z in b.Zones()if z.GetIsRuleArea()and z.GetDoNotAllowZoneFills()and not z.GetDoNotAllowTracks()]
  for z in omitted:b.Remove(z);REMOVED.append(z)
  dest=work/'RF2M-E5.dsn';assert p.ExportSpecctraDSN(b,str(dest))
  for z in omitted:b.Add(z)
  s=dest.read_text().replace('(clearance 200)','(clearance 150)').replace('(width 200)','(width 150)').replace('(clearance 50 (type smd_smd))','(clearance 150 (type smd_smd))')
  ds=cad.parse(s.replace('(string_quote ")','(string_quote QUOTE_CHARACTER)'));structure=cad.child(ds,'structure');network=cad.child(ds,'network');wiring=cad.child(ds,'wiring')
  def obstacle(layer,kind,args):structure.append(cad.parse('(keepout "" ('+kind+' '+layer+' '+' '.join(map(str,args))+'))'))
  for r,f in fs.items():
   if not r.startswith('TL'):continue
   pads={z.GetNumber():z for z in f.Pads()};x,y=xy(pads['1'].GetPosition());X,Y=xy(pads['2'].GetPosition());obstacle('F.Cu','rect',[1000*(x+.35),-1000*(y+WIDTH/2),1000*(X-.35),-1000*(Y-WIDTH/2)])
  for g in b.GetDrawings():
   if g.GetLayer()==p.F_Cu and g.GetShape()==p.SHAPE_T_RECT:
    x,y=xy(g.GetStart());X,Y=xy(g.GetEnd());obstacle('F.Cu','rect',[1000*min(x,X),-1000*max(y,Y),1000*max(x,X),-1000*min(y,Y)])
  for net in cad.children(network,'net'):
   if net[1]=='GND':net[:]=[net[0],net[1]]
  for item in list(wiring[1:]):
   nn=cad.child(item,'net')if isinstance(item,list)else None
   if not nn or nn[1]!='GND':continue
   if item[0]=='via':
    x,y=map(float,item[2:4]);w=int(re.search(r'_(\d+):',str(item[1]))[1])
    for layer in['F.Cu','B.Cu']:obstacle(layer,'circle',[w,x,y])
   elif item[0]=='wire':
    path=cad.child(item,'path');coords=list(map(float,path[3:]));ww=float(path[2])/2
    for (x,y),(X,Y)in zip(list(zip(coords[::2],coords[1::2])),list(zip(coords[::2],coords[1::2]))[1:]):obstacle(str(path[1]),'rect',[min(x,X)-ww,min(y,Y)-ww,max(x,X)+ww,max(y,Y)+ww])
   wiring.remove(item)
  classes=cad.children(network,'class');rails=['VMOD','VPA','VREG_SWITCH','VREG_RAW','VBOOST','VBUCK','VIN_CONV','VIN_PROT','BAT_FUSED','BAT_RAW','BOOST_SW','BUCK_SW'];logic=['V3V3','VDRV_PREREG','VDRV_FILTER','VDRV_RF','VDRV_MMIC','VDRV_LDO_IN']
  for c in classes:
   c[:]=[c[0],c[1]]+[n for n in c[2:]if not(isinstance(n,str)and n in rails+logic+['GND'])]
  for name,nets,w in[('POWER',rails,1000),('LOGICPOWER',logic,400),('GROUND',['GND'],300)]:network.append(cad.parse('(class '+name+' '+' '.join(nets)+' (circuit(use_via "Via[0-1]_600:300_um"))(rule(width '+str(w)+')(clearance 150)))'))
  dest.write_text(cad.dump(ds).replace('(string_quote QUOTE_CHARACTER)','(string_quote ")')+'\n');save('router-input.json',dict(path=str(dest.relative_to(ROOT)),sha256=sha(dest),power_width_mm=1.,logic_power_width_mm=.4,ground='Native zone connectivity, not a router wire tree',RF='Locked input conductors + exact native microstrip/source copper obstacles',external_upload=False));print('Exported protected local DSN',dest,flush=True);return
 elif a.action=='import':
  for t in list(b.GetTracks()):
   if not t.IsLocked():b.Remove(t);REMOVED.append(t)
  for z in list(b.Zones()):
   if not z.GetIsRuleArea():b.Remove(z);REMOVED.append(z)
  assert p.ImportSpecctraSES(b,str(a.session));print('Imported offline session',flush=True)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
if __name__=='__main__':main()
