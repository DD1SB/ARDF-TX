#!/usr/bin/python3
"""Independent native-geometry gate for ordinary JLCPCB2L1oz manufacture.
KiCadDRC is an additional gate,not the geometry input to this checker.
No quotation,CAM acceptance or measured performance is asserted.
"""
import argparse,collections,json,math,itertools,copy
from pathlib import Path
import pcbnew as p
import m5a_r1_design as c
from m5b_e3_common import *
from m5b_e3_common import aliases
MM=p.FromMM

def bbox(shape):
 z=shape.BBox();return[p.ToMM(z.GetLeft()),p.ToMM(z.GetTop()),p.ToMM(z.GetRight()),p.ToMM(z.GetBottom())]
def nearby(rows,gap=.5):
 idx=collections.defaultdict(list);seen=set()
 for i,a in enumerate(rows):
  x0,y0,x1,y1=a['bb'];keys=[(x,y)for x in range(math.floor((x0-gap)/4),math.floor((x1+gap)/4)+1)for y in range(math.floor((y0-gap)/4),math.floor((y1+gap)/4)+1)]
  for k in keys:
   for j in idx[k]:
    pair=(j,i)
    if pair not in seen:seen.add(pair);yield rows[j],a
   idx[k].append(i)
def polygon(g,layer):
 z=p.SHAPE_POLY_SET();g.TransformShapeToPolygon(z,layer,0,MM(.002),p.ERROR_OUTSIDE);return z

def evaluate(board,profile,full=True):
 b=p.LoadBoard(str(board))if isinstance(board,(str,Path))else board;aa=aliases();errors=[];warnings=[];stats={};cfg=b.GetDesignSettings();tree=c.parse(Path(board).read_text())if isinstance(board,(str,Path))else None
 def issue(check,**kw):errors.append(dict(check=check,**kw))
 def check(ok,name,**kw):
  if not ok:issue(name,**kw)
 def alias(n):return aa.get(n,n)
 check(cfg.GetCopperLayerCount()==2,'two_copper_layers',actual=cfg.GetCopperLayerCount());check(abs(p.ToMM(cfg.GetBoardThickness())-1.6)<.001,'standard_1p6mm',actual=p.ToMM(cfg.GetBoardThickness()))
 if tree:
  setup=c.child(tree,'setup');stack=c.child(setup,'stackup');cu=[]
  for l in c.children(stack,'layer'):
   if l[1]in['F.Cu','B.Cu']:cu.append(float(c.child(l,'thickness')[1]))
   if l[1].startswith('dielectric'):check(c.child(l,'material')[1]=='FR4','standard_FR4')
  check(cu==[.035,.035],'standard_1oz',actual_mm=cu)
  check(c.child(stack,'copper_finish')[1]=='Lead-free HASL','ordinary_finish');check(str(c.child(stack,'dielectric_constraints')[1])=='no','no_custom_core_or_impedance')
  check(not c.child(setup,'pad_to_paste_clearance_ratio')or abs(float(c.child(setup,'pad_to_paste_clearance_ratio')[1]))<1,'paste_definition')
 copper={p.F_Cu:[],p.B_Cu:[]};holes=[];mask={p.F_Mask:[],p.B_Mask:[]};silk=[];viaexceptions=[];via_sizes=collections.Counter();trackmin=100;ringmin=100;pthring=100
 def addcu(ob,n,ident,layer):
  sh=ob.GetEffectiveShape(layer)if isinstance(ob,(p.PAD,p.PCB_TRACK))else polygon(ob,layer)
  copper[layer].append(dict(shape=sh,net=alias(n),id=ident,bb=bbox(sh),object=ob))
 for t in b.GetTracks():
  ident=t.m_Uuid.AsString();via=isinstance(t,p.PCB_VIA);w=p.ToMM(t.GetWidth(p.F_Cu)if via else t.GetWidth())
  if via:
   d=p.ToMM(t.GetDrillValue());ring=(w-d)/2;ringmin=min(ringmin,ring);via_sizes[str(round(w,3))]+=1
   check(t.GetViaType()==p.VIATYPE_THROUGH,'ordinary_through_via',id=ident)
   for method,setting in[('GetFillingMode','m_FillVias'),('GetCappingMode','m_CapVias'),('GetFrontPluggingMode','m_PlugViasFront'),('GetBackPluggingMode','m_PlugViasBack'),('GetFrontCoveringMode','m_CoverViasFront'),('GetBackCoveringMode','m_CoverViasBack')]:
    mode=getattr(t,method)();check(mode!=1 and not(mode==0 and getattr(cfg,setting)),'no_premium_via_protection',id=ident,feature=method)
   for ml,cl in[(p.F_Mask,p.F_Cu),(p.B_Mask,p.B_Cu)]:
    if not t.IsTented(ml):
     z=p.SHAPE_POLY_SET();t.TransformShapeToPolygon(z,cl,0,MM(.002),p.ERROR_OUTSIDE);mask[ml].append(dict(shape=z,bb=bbox(z),id=ident+'.mask',net=alias(t.GetNetname())))
   check(d>=.25 and w>=.45,'no_premium_micro_drill_or_small_land',id=ident,land=w,drill=d);check(ring>=.1499,'via_annulus_design_minimum',id=ident,ring_mm=ring)
   if ring<.2499:viaexceptions.append(dict(uuid=ident,net=t.GetNetname(),at_mm=[p.ToMM(t.GetPosition().x),p.ToMM(t.GetPosition().y)],land_mm=w,drill_mm=d,annulus_mm=round(ring,3),disposition='Congestedstandardvia;largerpreferredlandwouldencroachadjacentcopper;acceptedlocaldesignmarginexception,nofabricationexception'))
   sh=p.SHAPE_CIRCLE(t.GetPosition(),MM(d/2));holes.append(dict(shape=sh,bb=bbox(sh),kind='via',id=ident,net=alias(t.GetNetname()),diameter_mm=d))
  else:
   trackmin=min(trackmin,w);check(w>=.1499,'actual_track_width',id=ident,width_mm=w)
  for layer in copper:
   if t.IsOnLayer(layer):addcu(t,t.GetNetname(),ident,layer)
 for f in b.GetFootprints():
  ref=f.GetReference()
  for a in f.Pads():
   ident=ref+'.'+a.GetNumber();size=a.GetDrillSize();d=min(p.ToMM(size.x),p.ToMM(size.y));npth=a.GetAttribute()==p.PAD_ATTRIB_NPTH
   if d>0:
    hole=p.SHAPE_POLY_SET();a.TransformHoleToPolygon(hole,0,MM(.002),p.ERROR_OUTSIDE);holes.append(dict(shape=hole,bb=bbox(hole),id=ident,net=alias(a.GetNetname()),kind='NPTH'if npth else'PTH',diameter_mm=d))
    if npth:check(d>=.5,'standard_NPTH_drill',id=ident)
    else:
     ring=min((p.ToMM(a.GetSize().x)-p.ToMM(size.x))/2,(p.ToMM(a.GetSize().y)-p.ToMM(size.y))/2);pthring=min(pthring,ring);check(ring>=.2499,'component_PTH_annulus',id=ident,annulus_mm=ring)
   if not npth:
    for layer in copper:
     if a.IsOnLayer(layer):addcu(a,a.GetNetname(),ident,layer)
   for layer in mask:
    if a.IsOnLayer(layer):
     z=polygon(a,layer);exp=a.GetSolderMaskExpansion(layer)
     if exp:z.Inflate(exp,p.CORNER_STRATEGY_ROUND_ALL_CORNERS,MM(.002))
     mask[layer].append(dict(shape=z,bb=bbox(z),id=ident,net=alias(a.GetNetname())))
  for g in f.GraphicalItems():
   if g.GetLayer()in copper:
    ns={a.GetNetname()for a in f.Pads()};n=next(iter(ns))if ns else'';check(ref.startswith('TL'),'copper_graphic_has_declared_net_tie',ref=ref)
    addcu(g,n,ref+'.copper',g.GetLayer())
   if g.GetLayer()in mask:
    z=polygon(g,g.GetLayer());mask[g.GetLayer()].append(dict(shape=z,bb=bbox(z),id=ref+'.mask',net='GND'if ref=='Q501'else''))
   if g.GetLayer()in[p.F_SilkS,p.B_SilkS]:silk.append(g)
  for g in f.GetFields():
   if g.IsVisible()and g.GetLayer()in[p.F_SilkS,p.B_SilkS]:silk.append(g)
 for g in b.GetDrawings():
  if g.GetLayer()in copper:
   check(hasattr(g,'GetNetname')and bool(g.GetNetname()),'native_copper_graphic_net',id=g.m_Uuid.AsString())
   addcu(g,g.GetNetname(),g.m_Uuid.AsString(),g.GetLayer())
  if g.GetLayer()in mask:
   z=polygon(g,g.GetLayer());mask[g.GetLayer()].append(dict(shape=z,bb=bbox(z),id='board_mask',net='GND'))
  if g.GetLayer()in[p.F_SilkS,p.B_SilkS]:silk.append(g)
 for g in silk:
  if isinstance(g,(p.PCB_TEXT,p.PCB_FIELD)):
   check(p.ToMM(g.GetTextHeight())>=.999,'legend_height',text=g.GetText());check(p.ToMM(g.GetTextThickness())>=.149,'legend_stroke',text=g.GetText())
  elif hasattr(g,'GetWidth'):check(p.ToMM(g.GetWidth())>=.149,'legend_graphic_stroke')
 # Actual routededge and copper bounding geometry (rectangularboardonly).
 eds=[g for g in b.GetDrawings()if g.GetLayer()==p.Edge_Cuts];pts=[g.GetStart()for g in eds]+[g.GetEnd()for g in eds];edge=[min(p.ToMM(v.x)for v in pts),min(p.ToMM(v.y)for v in pts),max(p.ToMM(v.x)for v in pts),max(p.ToMM(v.y)for v in pts)];stats['outline_mm']=edge;check(abs(edge[2]-edge[0]-180)<.01 and abs(edge[3]-edge[1]-140)<.01,'known_outline')
 for rows in copper.values():
  for a in rows:
   x0,y0,x1,y1=a['bb'];dist=min(x0-edge[0],y0-edge[1],edge[2]-x1,edge[3]-y1);check(dist>=.199,'actual_copper_to_edge',id=a['id'],mm=dist)
 if full:
  tested=0
  for layer,rows in copper.items():
   for a,z in nearby(rows,.16):
    if a['net']==z['net']or a['id']==z['id']:continue
    tested+=1
    if p.SHAPE.Collide(a['shape'],z['shape'],MM(.099)):issue('native_foreign_copper_clearance',layer=b.GetLayerName(layer),items=[a['id'],z['id']],threshold_mm=.10)
    elif p.SHAPE.Collide(a['shape'],z['shape'],MM(.149)):issue('native_preferred_copper_clearance',layer=b.GetLayerName(layer),items=[a['id'],z['id']],threshold_mm=.15)
  stats['independent_copper_pair_tests']=tested
  for a,z in nearby(holes,.5):
   limit=.20 if a['kind']==z['kind']=='via'else.45
   if p.SHAPE.Collide(a['shape'],z['shape'],MM(limit-.002)):issue('native_hole_spacing',items=[a['id'],z['id']],threshold_mm=limit)
  for layer,rows in copper.items():
   for a,z in nearby(holes+rows,.4):
    if ('kind'in a)==('kind'in z):continue
    h,cu=(a,z)if'kind'in a else(z,a)
    if h['net']and h['net']==cu['net']or h['id']==cu['id']:continue
    limit=.28 if h['kind']=='PTH'else.2
    if p.SHAPE.Collide(h['shape'],cu['shape'],MM(limit-.002)):issue('native_copper_to_hole',layer=b.GetLayerName(layer),hole=h['id'],copper=cu['id'],threshold_mm=limit)
  # Maskis a UNIONofallapertures. A sourceviaopeninginsideanexisting
  # thermalwindowdoesnotcreateawebbetweenrawoverlappingprimitives.
  for layer,rows in mask.items():
   union=p.SHAPE_POLY_SET()
   for row in rows:union.Append(row['shape'])
   union.Simplify();islands=[]
   for i in range(union.OutlineCount()):
    shape=p.SHAPE_POLY_SET();shape.AddOutline(union.Outline(i))
    for j in range(union.HoleCount(i)):shape.AddHole(union.Hole(i,j),0)
    islands.append(dict(shape=shape,bb=bbox(shape),id='mask-aperture-'+str(i)))
   for a,z in nearby(islands,.11):
    if p.SHAPE.Collide(a['shape'],z['shape'],MM(.098)):issue('native_mask_web',layer=b.GetLayerName(layer),items=[a['id'],z['id']],threshold_mm=.10)
  for ml,cl in[(p.F_Mask,p.F_Cu),(p.B_Mask,p.B_Cu)]:
   for a,z in nearby(mask[ml]+copper[cl],.1):
    if ('object'in a)==('object'in z):continue
    opening,cu=(z,a)if'object'in a else(a,z)
    if opening['net']==cu['net']:continue
    if p.SHAPE.Collide(opening['shape'],cu['shape'],MM(.088)):issue('native_mask_opening_to_foreign_copper',opening=opening['id'],copper=cu['id'])
  # Check filled zones using nativepolygon union as well as routed features.
  from m5b_e2_sliver import polygons,locate
  slivers={b.GetLayerName(l):locate(polygons(b,l))for l in copper};stats['slivers']=slivers
  for l,found in slivers.items():
   if found:issue('filled_copper_sliver',layer=l,findings=found)
  # Independently test legend outlines against actual openings.
  for g in silk:
   layer=p.F_Mask if g.GetLayer()==p.F_SilkS else p.B_Mask
   sh=g.GetEffectiveTextShape()if isinstance(g,(p.PCB_TEXT,p.PCB_FIELD))else g.GetEffectiveShape()
   bb0=bbox(sh)
   for z in mask[layer]:
    q=z['bb']
    if bb0[2]+.15<q[0]or q[2]+.15<bb0[0]or bb0[3]+.15<q[1]or q[3]+.15<bb0[1]:continue
    if p.SHAPE.Collide(sh,z['shape'],MM(.149)):issue('native_legend_to_mask',text=g.GetText()if hasattr(g,'GetText')else'graphic',aperture=z['id'])
 stats.update(track_minimum_mm=round(trackmin,4),via_annulus_min_mm=round(ringmin,4),component_PTH_annulus_min_mm=round(pthring,4),via_land_counts=dict(via_sizes),holes=len(holes),copper_objects={b.GetLayerName(k):len(v)for k,v in copper.items()},legend_items=len(silk))
 return dict(revision=REV,status='PASS_AUTOMATED_NATIVE_GEOMETRY'if not errors else'FAIL',errors=errors,preferred_margin_exceptions=viaexceptions,manual_review=profile['manual_review'],statistics=stats,limitations='NOTcommercialCAMacceptance. Filledzoneacutegeometryandroutepairchecksareindependentofprojectrules;nativeKiCadnarrow-neck/thermalcheckerremainsadditionalmandatorygate. Pastejointquality,HASLflatness,drillregistration,thermalcontactandRFperformancerequireinspection/measurement.')

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--board',default=str(HW/'RF2M.kicad_pcb'));ap.add_argument('--quick',action='store_true');ap.add_argument('--regression',action='store_true');x=ap.parse_args();profile=json.loads((OUT/'JLCPCB-standard-profile.json').read_text());r=evaluate(x.board,profile,not x.quick);r['native_sha256']=sha(Path(x.board));save('JLCPCB-DFM.json',r);print(r['status'],'errors',len(r['errors']),r['statistics'])
 if x.regression:
  # Deliberate realnative mutations,neverwrittenoveractiveboard.
  tests=[];b=p.LoadBoard(x.board)
  def fails(name,action,undo,code):
   action();z=evaluate(b,profile,False);undo();assert any(e['check']==code for e in z['errors']),name;tests.append(dict(mutation=name,detected=code))
  ds=b.GetDesignSettings();old=ds.GetBoardThickness();fails('wrong_thickness',lambda:ds.SetBoardThickness(MM(.8)),lambda:ds.SetBoardThickness(old),'standard_1p6mm')
  t=next(t for t in b.GetTracks()if not isinstance(t,p.PCB_VIA));old=t.GetWidth();fails('subminimum_track',lambda:t.SetWidth(MM(.08)),lambda:t.SetWidth(old),'actual_track_width')
  v=next(t for t in b.GetTracks()if isinstance(t,p.PCB_VIA));old=v.GetWidth(p.F_Cu);fails('insufficient_annulus',lambda:v.SetWidth(MM(.45)),lambda:v.SetWidth(old),'via_annulus_design_minimum')
  oldfill=v.GetFillingMode();fails('filled_via',lambda:v.SetFillingMode(p.FILLING_MODE_FILLED),lambda:v.SetFillingMode(oldfill),'no_premium_via_protection')
  oldtype=v.GetViaType();fails('blind_via',lambda:v.SetViaType(p.VIATYPE_BLIND),lambda:v.SetViaType(oldtype),'ordinary_through_via')
  old=v.GetDrillValue();fails('premium_micro_drill',lambda:v.SetDrill(MM(.15)),lambda:v.SetDrill(old),'no_premium_micro_drill_or_small_land')
  text=next(g for g in b.GetDrawings()if isinstance(g,p.PCB_TEXT)and g.GetLayer()==p.F_SilkS);old=text.GetTextHeight();fails('undersize_legend',lambda:text.SetTextHeight(MM(.8)),lambda:text.SetTextHeight(old),'legend_height')
  # Actualforeign-coppermutation,notachangedconfiguredclearancerule.
  for yy,net in[(30.,'V3V3'),(30.2,'GND')]:
   q=p.PCB_TRACK(b);q.SetStart(p.VECTOR2I(MM(30),MM(yy)));q.SetEnd(p.VECTOR2I(MM(33),MM(yy)));q.SetWidth(MM(.15));q.SetLayer(p.F_Cu);q.SetNet(b.FindNet(net));b.Add(q)
  spatial=evaluate(b,profile,True);assert any(e['check']=='native_foreign_copper_clearance'for e in spatial['errors']);tests.append(dict(mutation='real0p05mmcoppergap',detected='native_foreign_copper_clearance'))
  for xx in[193.,193.55]:
   q=p.PCB_SHAPE(b);q.SetShape(p.SHAPE_T_RECT);q.SetStart(p.VECTOR2I(MM(xx),MM(150.)));q.SetEnd(p.VECTOR2I(MM(xx+.5),MM(150.5)));q.SetLayer(p.F_Mask);q.SetFilled(True);q.SetWidth(0);b.Add(q)
  aperture=evaluate(b,profile,True);assert any(e['check']=='native_mask_web'for e in aperture['errors']);tests.append(dict(mutation='real0p05mmmaskweb',detected='native_mask_web'))
  # E2 is a strictnegativeundernewprofile,notrewrittenorrelabeled.
  fn=OUT/'development/E2-native.kicad_pcb';fn.write_bytes(gitfile('hardware/2m/RF2M.kicad_pcb'));e2=evaluate(fn,profile,False);codes={e['check']for e in e2['errors']};assert {'standard_1p6mm','standard_1oz','legend_height','legend_stroke'}<=codes
  for label,old,new,code in [('2oz','.035','.07','standard_1oz'),('special_finish','Lead-free HASL','Immersiongold','ordinary_finish')]:
   path=OUT/('development/dfm-'+label+'.kicad_pcb');txt=Path(x.board).read_text()
   if label=='2oz':txt=txt.replace('(thickness 0.035)','(thickness 0.07)')
   else:txt=txt.replace('Lead-free HASL','Immersiongold')
   path.write_text(txt);rr=evaluate(path,profile,False);assert any(e['check']==code for e in rr['errors']);tests.append(dict(mutation=label,detected=code))
  save('DFM-regression.json',dict(status='PASS',mutations=tests,E2_rejected_checks=sorted(codes),E3_status=r['status']))
 if r['errors']:
  print(json.dumps(r['errors'][:15],indent=2));raise SystemExit(1)
if __name__=='__main__':main()
