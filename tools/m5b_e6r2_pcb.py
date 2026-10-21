"""Local native placement/cutouts; existing RF signal copper/source array retained."""
import math,xml.etree.ElementTree as ET
import m5a_r1_design as c
from m5b_e6r2_common import *
from m5b_e6r2_geometry import geometry
KEEP=[]
def graphic(fp,a,b,layer,width=.1):
 g=p.PCB_SHAPE(fp);g.SetShape(p.SHAPE_T_SEGMENT);g.SetStart(pt(*a));g.SetEnd(pt(*b));g.SetLayer(layer);g.SetWidth(MM(width));fp.Add(g)
def rectangle(fp,b,layer,width=.1):
 x0,y0,x1,y1=b
 for a,z in [((x0,y0),(x1,y0)),((x1,y0),(x1,y1)),((x1,y1),(x0,y1)),((x0,y1),(x0,y0))]:graphic(fp,a,z,layer,width)
def power_footprints():
 for r,d in geometry()['devices'].items():
  f=p.FOOTPRINT(None);f.SetFPID(p.LIB_ID('ARDF_2M',d['footprint']));f.SetReference(r);f.SetValue(d['part']);f.SetAttributes(p.FP_THROUGH_HOLE)
  x0,y0=d['pin1'];bounds=d['body_bounds'];rectangle(f,[bounds[0]-x0,bounds[1]-y0,bounds[3]-x0,bounds[4]-y0],p.B_Fab)
  rectangle(f,[min(0,2*d['lead_step'])-1.3,-1.3,max(0,2*d['lead_step'])+1.3,1.3],p.F_CrtYd,.05)
  rectangle(f,[bounds[0]-x0-.25,bounds[1]-y0-.25,bounds[3]-x0+.25,bounds[4]-y0+.25],p.B_CrtYd,.05)
  for i in range(3):
   a=p.PAD(f);a.SetNumber(str(i+1));a.SetAttribute(p.PAD_ATTRIB_PTH);a.SetShape(p.PAD_SHAPE_RECT if i==0 else p.PAD_SHAPE_CIRCLE);a.SetPosition(pt(i*d['lead_step'],0));a.SetSize(pt(2,2));a.SetDrillSize(pt(1.3,1.3));a.SetLayerSet(p.PAD.PTHMask());f.Add(a)
  circle=p.PCB_SHAPE(f);circle.SetShape(p.SHAPE_T_CIRCLE);circle.SetStart(pt(d['hole'][0]-x0,d['hole'][1]-y0));circle.SetEnd(pt(d['hole'][0]-x0+d['hole_diameter_min']/2,d['hole'][1]-y0));circle.SetLayer(p.B_Fab);circle.SetWidth(MM(.1));f.Add(circle)
  for field in [f.Reference(),f.Value()]:field.SetLayer(p.F_Fab);field.SetVisible(True);field.SetTextSize(pt(1,1));field.SetTextThickness(MM(.15))
  f.Reference().SetPosition(pt(d['lead_step'],2.5));f.Value().SetPosition(pt(d['lead_step'],4.))
  model=p.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/ARDF_2M.3dshapes/'+r+'_CommonPlane_E6R2.step';f.Models().push_back(model)
  f.SetLibDescription('E6R2 flat underside mounting. Pin1B2C3E; formed leads Rcenter2mm/straight4.5mm; commonbackZ-7.8; mounting planeZ-7.9. See mechanical-source.json.')
  p.FootprintSave(str(HW/'ARDF_2M.pretty'),f)
 # Library filters must agree with the embedded, deliberately revised symbols.
 lib=c.parse((HW/'ARDF_2M.kicad_sym').read_text())
 for d in c.children(lib,'symbol'):
  if d[1] in ['D45H11_ST','BD139_ST']:
   pp=next((z for z in c.children(d,'property') if z[1]=='ki_fp_filters'),None)
   if pp and 'CommonPlane_E6R2' not in pp[2]:pp[2]+=' ARDF_2M:'+geometry()['devices']['Q401' if d[1]=='D45H11_ST' else 'Q402']['footprint']
 (HW/'ARDF_2M.kicad_sym').write_text(c.dump(lib)+'\n')
def cutout(b,rect,r=1.):
 x0,y0,x1,y1=rect
 for a,z in [((x0+r,y0),(x1-r,y0)),((x1,y0+r),(x1,y1-r)),((x1-r,y1),(x0+r,y1)),((x0,y1-r),(x0,y0+r))]:graphic(b,a,z,p.Edge_Cuts,.05)
 for a,mid,z in [((x1-r,y0),(x1-r+r/math.sqrt(2),y0+r-r/math.sqrt(2)),(x1,y0+r)),((x1,y1-r),(x1-r+r/math.sqrt(2),y1-r+r/math.sqrt(2)),(x1-r,y1)),((x0+r,y1),(x0+r-r/math.sqrt(2),y1-r+r/math.sqrt(2)),(x0,y1-r)),((x0,y0+r),(x0+r-r/math.sqrt(2),y0+r-r/math.sqrt(2)),(x0+r,y0))]:
  g=p.PCB_SHAPE(b);g.SetShape(p.SHAPE_T_ARC);g.SetArcGeometry(pt(*a),pt(*mid),pt(*z));g.SetLayer(p.Edge_Cuts);g.SetWidth(MM(.05));b.Add(g)
def main():
 guard();power_footprints();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));assert b.GetTitleBlock().GetRevision()!=REV,'Floorplan already applied; use native board authority'
 fs=fps(b);j=manifest();parts={d['ref']:d for d in j['parts']};g=geometry()
 netlist=ET.parse(OUT/'RF2M.net.xml');comps={x.get('ref'):x for x in netlist.findall('./components/comp')}
 for n in {v for part in parts.values() for v in part['pins'].values() if v}:
  if b.FindNet(n) is None:b.Add(p.NETINFO_ITEM(b,n))
 # Save only cuts to old routes; never touch normal144MHz/training signal nets.
 electrical_changes=json.loads((OUT/'electrical-change.json').read_text())['changes'];removed=[]
 for z in electrical_changes:
  f=fs[z['ref']];pad=next(a for a in f.Pads() if a.GetNumber()==z['pin']);oldnet=pad.GetNetname();pos=pad.GetPosition();bb=pad.GetBoundingBox();bb.Inflate(MM(.3))
  for t in list(b.GetTracks()):
   if t.GetNetname()==oldnet and t.GetBoundingBox().Intersects(bb):removed.append(dict(net=oldnet,uuid=t.m_Uuid.AsString(),reason='Changed pin isolation'));b.Remove(t);KEEP.append(t)
  pad.SetNet(b.FindNet(z['net']))
 moved={'Q401':(*g['devices']['Q401']['pin1'],0),'Q402':(*g['devices']['Q402']['pin1'],0),
  'R506':(125.25,31.5,90),'R513':(141,35,0),'C506':(141,38,0),'Q403':(142,42,0),'Q404':(149,42,0),'R505':(141,32,0),'R510':(146,38,0),'R507':(133,45,0),'R508':(151,38,0)}
 # Local pass/helper nets are rerouted deliberately; matching/feed topology is untouched.
 localnets={'PASS_BASE','MOD_SINK','MOD_BASE','MOD_E','MOD_CLAMP_BASE','MOD_CLAMP','MOD_OFF_BASE'}
 for t in list(b.GetTracks()):
  xx,yy=xy(t.GetStart());xe,ye=xy(t.GetEnd());bb=t.GetBoundingBox()
  inbay=(bb.GetRight()>MM(105) and bb.GetLeft()<MM(156) and bb.GetBottom()>MM(21) and bb.GetTop()<MM(47))
  power=t.GetNetname() in ['VMOD','VPA'] and inbay
  if t.GetNetname() in localnets or power:
   if t.IsLocked() and t.GetNetname() not in localnets:continue
   removed.append(dict(net=t.GetNetname(),uuid=t.m_Uuid.AsString(),reason='Common-plane device bay reroute'));b.Remove(t);KEEP.append(t)
 for ref,pose in moved.items():
  f=fs[ref]
  if ref in ['Q401','Q402']:
   old=f;d=g['devices'][ref];f=p.FootprintLoad(str(HW/'ARDF_2M.pretty'),d['footprint']);f.SetReference(ref);f.SetValue(parts[ref]['value']);f.SetPath(old.GetPath());f.SetUuid(old.m_Uuid);b.Remove(old);KEEP.append(old);b.Add(f);fs[ref]=f
   for a in f.Pads():a.SetNet(b.FindNet(parts[ref]['pins'][a.GetNumber()]))
  f.SetOrientationDegrees(pose[2]);f.SetPosition(pt(*pose[:2]))
 for d in g['devices'].values():cutout(b,d['cutout'])
 # Mark thermocouple attachment with a native fabrication-layer target; no
 # extra hole or change to the critical source/mask/paste/via arrangement.
 for ref,loc in g['TC_locations'].items():
  t=p.PCB_TEXT(b);t.SetText('TC '+ref);t.SetPosition(pt(loc[0],loc[1]+2));t.SetLayer(p.F_Fab);t.SetTextSize(pt(1,1));t.SetTextThickness(MM(.15));b.Add(t)
  graphic(b,(loc[0]-.6,loc[1]),(loc[0]+.6,loc[1]),p.F_Fab);graphic(b,(loc[0],loc[1]-.6),(loc[0],loc[1]+.6),p.F_Fab)
 places={'U970':(139,65,0),'U971':(147,65,0),'U972':(155,65,0),'U973':(147,75,0),
  'R970':(125.25,42.5,90),'R971':(132,61,0),'R972':(132,64,0),'R973':(132,67,0),'R974':(132,70,0),'R975':(139,70,0),'R976':(143,70,0),'R977':(151,70,0),'R978':(155,70,0),'R979':(139,74,0),'R980':(139,77,0),'R981':(162,61,0),'R982':(155,75,0),'R983':(162,65,0),'R984':(162,69,0),
  'C970':(139,61,0),'C971':(147,61,0),'C972':(155,61,0),'C973':(147,79,0),'TP970':(128.1,45.8,0),'TP971':(121.0,106,0),'TP972':(162,75,0),'TP973':(155,79,0),'TP974':(162,79,0),'TP975':(135,75,0),'TP976':(143,74,0)}
 for ref,pose in places.items():
  part=parts[ref];lib,name=part['footprint'].split(':');folder=HW/(lib+'.pretty') if lib=='ARDF_2M' else Path('/usr/share/kicad/footprints')/(lib+'.pretty')
  f=p.FootprintLoad(str(folder),name);assert f,ref;f.SetReference(ref);f.SetValue(part['value']);f.SetFPID(p.LIB_ID(lib,name));co=comps[ref];f.SetPath(p.KIID_PATH(co.find('sheetpath').get('tstamps')+co.findtext('tstamps')))
  for a in f.Pads():
   n=part['pins'].get(a.GetNumber());a.SetNet(b.FindNet(n) if n else b.FindNet('unconnected-('+ref+'-NC-Pad'+a.GetNumber()+')'))
  for fld in f.GetFields():fld.SetLayer(p.F_Fab);fld.SetVisible(fld.GetName() in ['Reference','Value'])
  for sh in f.GraphicalItems():
   if sh.GetLayer()==p.F_SilkS:sh.SetLayer(p.F_Fab)
  f.SetOrientationDegrees(pose[2]);f.SetPosition(pt(*pose[:2]));f.SetDNP(False);b.Add(f);fs[ref]=f
 fs['H5'].Models().clear();model=p.FP_3DMODEL();model.m_Filename='${KIPRJMOD}/ARDF_2M.3dshapes/E6R2_unified_cooling.step';fs['H5'].Models().push_back(model)
 for sh in b.GetDrawings():
  if isinstance(sh,p.PCB_TEXT) and 'M5B-E5' in sh.GetText():sh.SetText(sh.GetText().replace('M5B-E5',REV))
 tb=b.GetTitleBlock();tb.SetRevision(REV);tb.SetDate(DATE);tb.SetComment(0,'CONTROLLED EVALUATION / ONE SHARED COOLER / PHYSICAL NOT_RUN')
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
 save('floorplan-change.json',dict(moved=moved,added=places,removed_routes=removed,cutouts=[d['cutout'] for d in g['devices'].values()],critical_RF='Q501 and RF matching/filter signal geometry retained; ground-boundary impact reviewed separately',status='NATIVE_PLACEMENT_CUTOUTS_IMPLEMENTED_ROUTING_PENDING'))
 print('Native common-plane footprints/cutouts,30new footprints installed; local routes opened',len(removed))

if __name__=='__main__':main()
