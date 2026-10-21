"""Native local repairs and grid routing; historical helpers imported read-only."""
import argparse,sys,types,math,xml.etree.ElementTree as ET
import m5a_r1_design as c
from m5b_e6r2_common import *
from m5b_e6r2_geometry import geometry
REMOVED=[]
def repair():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs=fps(b);j=manifest();parts={d['ref']:d for d in j['parts']};log=[]
 for ref,x,y in [('TP970',129,45.2),('TP971',129.5,79),('Q404',152,38.5),('R508',146,35)]:fs[ref].SetPosition(pt(x,y))
 # Use local copies for intentionally changed legend layers. Copper/package
 # geometry remains the manufacturer standard and is independently compared.
 for ref,name in [('U970','TLV7032_DGK_E6R2'),('U971','LVC1G00_DBV_E6R2'),('U972','LVC2G32_DCU_E6R2'),('U973','LVC1G04_DBV_E6R2')]:
  f=fs[ref];f.SetFPID(p.LIB_ID('ARDF_2M',name));parts[ref]['footprint']='ARDF_2M:'+name
  local=p.Cast_to_FOOTPRINT(f.Duplicate(False));local.SetPosition(pt(0,0));local.SetOrientationDegrees(0);p.FootprintSave(str(HW/'ARDF_2M.pretty'),local)
 for ref in ['Q401','Q402']:fs[ref].SetFPID(p.LIB_ID(*parts[ref]['footprint'].split(':')))
 tree=ET.parse(OUT/'RF2M.net.xml');comps={x.get('ref'):x for x in tree.findall('./components/comp')}
 expected={(nd.get('ref'),nd.get('pin')):n.get('name') for n in tree.findall('./nets/net') for nd in n.findall('node')}
 for ref in list(json.loads((OUT/'electrical-change.json').read_text())['added'])+['Q401','Q402']:
  f=fs[ref]
  for field in comps[ref].findall('./fields/field'):
   n=field.get('name');v=field.text or ''
   if n in ['Datasheet','Description']:continue
   if n=='Footprint':v=parts[ref]['footprint']
   present=next((a for a in f.GetFields() if a.GetName()==n),None)
   if present:present.SetText(v)
   else:
    fld=p.PCB_FIELD(f,p.FIELD_T_USER,n);fld.SetText(v);fld.SetVisible(False);f.Add(fld)
  for a in f.Pads():
   net=expected.get((ref,a.GetNumber()))
   if net:
    if b.FindNet(net) is None:b.Add(p.NETINFO_ITEM(b,net))
    a.SetNet(b.FindNet(net))
 # Native sheet and manifest updated together; no netlist normalization tricks.
 fn=HW/'13_carrier_keying.kicad_sch';sx=c.parse(fn.read_text())
 for sy in c.children(sx,'symbol'):
  ref=next(v[2] for v in c.children(sy,'property') if v[1]=='Reference')
  for v in c.children(sy,'property'):
   if v[1]=='Footprint':v[2]=parts[ref]['footprint']
 fn.write_text(c.dump(sx)+'\n');j['parts']=list(parts.values());(HW/'RF2M.electrical.json').write_text(json.dumps(j,indent=2)+'\n')
 protected=set(json.loads(gitfile('hardware/2m/review/M5B-E5/normal-RF-copper-equivalence.json'))['RF_nets'])
 newrefs=set(json.loads((OUT/'electrical-change.json').read_text())['added'])|set(json.loads((OUT/'floorplan-change.json').read_text())['moved'])
 pads=[a for r in newrefs for a in fs[r].Pads()]
 for t in list(b.GetTracks()):
  bad=False;reason=''
  for d in geometry()['devices'].values():
   x0,y0,x1,y1=d['cutout'];bb=p.BOX2I(pt(x0-.85,y0-.85),pt(x1-x0+1.7,y1-y0+1.7))
   if t.GetBoundingBox().Intersects(bb):bad=True;reason='Routed cutout clearance'
  if not bad:
   for a in pads:
    if a.GetNetname()==t.GetNetname():continue
    for layer in [p.F_Cu,p.B_Cu]:
     if a.IsOnLayer(layer) and t.IsOnLayer(layer) and p.SHAPE.Collide(a.GetEffectiveShape(layer),t.GetEffectiveShape(layer),MM(.19)):
      bad=True;reason='New/moved physical pad clearance';break
    if bad:break
  if bad:
   assert t.GetNetname() not in protected,('RF copper conflict requires explicit review',t.GetNetname(),xy(t.GetPosition()))
   # Source array is outside all new bays; do not sacrifice source vias.
   if isinstance(t,p.PCB_VIA):assert not(85<=xy(t.GetPosition())[0]<=99 and 47<=xy(t.GetPosition())[1]<=63)
   log.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),reason=reason));b.Remove(t);REMOVED.append(t)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('local-clearance-repair.json',log);print('New-bay native clearance repairs',len(log))

def route(args):
 guard();report=OUT/'DRC.json'
 debug='--debug' in args
 if debug:args.remove('--debug')
 if '--report' in args:
  i=args.index('--report');report=Path(args[i+1]);args=args[:i]+args[i+2:]
 # Reuse the existing exact-native obstacle extensions, redirecting all output
 # to this revision. The source helper is frozen and never executed directly.
 source=(ROOT/'tools/m5b_e5_finish.py').read_text().replace('from m5b_e5_common import *','from m5b_e6r2_common import *').replace('from m5b_e5_common import HW as P,OUT as D,MM','from m5b_e6r2_common import HW as P,OUT as D,MM')
 module=types.ModuleType('E6R2_route_helper');module.__file__=str(ROOT/'tools/m5b_e5_finish.py');exec(compile(source,module.__file__,'exec'),module.__dict__)
 # Patch only routing-tool defects/features: true connected-component anchors,
 # and obstacles for the new internal cutouts on both layers.
 original_exec=__builtins__['exec'] if isinstance(__builtins__,dict) else __builtins__.exec
 original_compile=compile
 def compile_route(code,filename,mode,*extra,**kw):
  if filename.endswith('m5b_route_completion.py'):
   if not debug:
    start=code.index('        best={s:0 for s in starts};')
    end=code.index('        ids.reverse();pieces=[];',start)
    code=code[:start]+'''        from m5b_e6r2_route_backend import solve as native_grid_route
        ids,expanded=native_grid_route(masks,vm,NX,NY,starts,goals)
        if ids is None:
            logs.append(dict(net=net,status='no path in complete grid'));print(net,'no path in complete grid',flush=True);continue
'''+code[end:]
   if debug:
    code=code.replace('        best={s:0 for s in starts};', '''        for li in [0,1]:
            (D/'development'/('route-mask-'+net+'-'+str(li)+'.raw')).write_bytes(masks[li])
            (D/'development'/('route-vias-'+net+'-'+str(li)+'.raw')).write_bytes(vm[li])
            im=ims[li].point(lambda x:180 if x else 255).convert('RGB');dd=ImageDraw.Draw(im)
            for index,group in enumerate(candidates):
                for (ll,cell),loc in group.items():
                    if ll!=li:continue
                    xx=cell%NX;yy=cell//NX;dd.ellipse((xx-5,yy-5,xx+5,yy+5),fill='red' if index==0 else 'blue')
            im.save(str(D/'development'/('route-mask-'+net+'-'+str(li)+'.png')))
        (D/'development'/('route-anchors-'+net+'.json')).write_text(json.dumps(dict(NX=NX,NY=NY,starts=starts,goals=list(goals))))
        print('DEBUG',net,[len(q)for q in candidates],[(len(sk),len(gk))],flush=True)
        continue
        best={s:0 for s in starts};''')
   code=code.replace('expanded>500000','expanded>2000000').replace('[:16]','[:128]')
   code=code.replace("b.BuildConnectivity();conn=b.GetConnectivity();groups=[[o]for o in objs]if a.direct else[list(conn.GetConnectedItems(o))for o in objs]", """b.BuildConnectivity();conn=b.GetConnectivity()
        def component(root):
            seen={};pending=[root]
            while pending:
                q=pending.pop();key=uid(q)
                if key in seen:continue
                if q.GetClass()=='PCB_VIA':q=pcb.Cast_to_PCB_VIA(q)
                elif q.GetClass()=='PAD':q=pcb.Cast_to_PAD(q)
                elif q.GetClass()=='PCB_TRACK':q=pcb.Cast_to_PCB_TRACK(q)
                seen[key]=q
                pending.extend(x for x in conn.GetConnectedItems(q) if uid(x)not in seen and x.GetNetname()==net)
            return list(seen.values())
        groups=[[o]for o in objs]if a.direct else[component(o)for o in objs]""")
   needle="        for d in ds+vs:\n"
   addition="        for d in ds+vs:\n            for x0,y0,x1,y1 in "+repr([q['cutout'] for q in geometry()['devices'].values()])+":\n                rect(d,[x0,y0,x1,y1],.55+max(width/2,.30))\n"
   code=code.replace(needle,addition)
   code=code.replace("ids.reverse();pieces=[];vias=[];points=[];layer=ids[0]//N", "ids.reverse();endpoints=[candidates[0][(ids[0]//N,ids[0]%N)],candidates[1][(ids[-1]//N,ids[-1]%N)]];pieces=[];vias=[];points=[];layer=ids[0]//N")
  return original_compile(code,filename,mode,*extra,**kw)
 module.compile=compile_route
 module.complete(['--report',str(report)]+args)

def prune():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));j=json.loads((OUT/'DRC.json').read_text());bad={i['uuid'] for v in j['violations'] if v['type'] in ['track_dangling','via_dangling'] for i in v['items']};removed=[]
 assert all(all('[GND]' in i['description'] for i in v['items']) for v in j['unconnected_items']), 'Complete signal routes before removing provisional via escapes'
 for t in list(b.GetTracks()):
  if t.m_Uuid.AsString() in bad:
   if t.IsLocked():
    # Explicitly reviewed obsolete ends at moved Q401/helper and changed
    # U601/U402 control pins. Never prune protected RF/source conductors.
    if t.GetNetname() not in ['VPA','NORMAL_OFF','MOD_DRIVE','LEVEL_DC']:continue
   removed.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname()));b.Remove(t);REMOVED.append(t)
 for v in j['violations']:
  if v['type']=='starved_thermal':
   for i in v['items']:
    for f in b.GetFootprints():
     for a in f.Pads():
      if a.m_Uuid.AsString()==i['uuid'] and a.GetNetname()=='GND':a.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('pruned-dangling.json',removed);print('Removed obsolete native dangling items',len(removed))

def metadata():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs=fps(b);tree=ET.parse(OUT/'RF2M.net.xml')
 for co in tree.findall('./components/comp'):
  if co.get('ref') not in fs:continue
  f=fs[co.get('ref')]
  for n,kind in [('Datasheet',p.FIELD_T_DATASHEET),('Description',p.FIELD_T_DESCRIPTION)]:
   field=co.find('./fields/field[@name="'+n+'"]');value=(field.text or '') if field is not None else (co.findtext(n.lower()) or '')
   f.GetField(kind).SetText(value)
  for field in co.findall('./fields/field'):
   n=field.get('name');value=field.text or ''
   if n in ['MPN','Population','Function','Engineering_Note','Status']:
    old=next((x for x in f.GetFields() if x.GetName()==n),None)
    if old:old.SetText(value)
    else:
     item=p.PCB_FIELD(f,p.FIELD_T_USER,n);item.SetText(value);item.SetVisible(False);f.Add(item)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);print('Native standard metadata synchronized')

def dense():
 guard()
 source=(ROOT/'tools/m5b_e5_finish.py').read_text().replace('from m5b_e5_common import *','from m5b_e6r2_common import *')
 module=types.ModuleType('E6R2_ground_helper');module.__file__=str(ROOT/'tools/m5b_e5_finish.py');exec(compile(source,module.__file__,'exec'),module.__dict__)
 module.dense()

def stitch():
 guard()
 source=(ROOT/'tools/m5b_e5_finish.py').read_text().replace('m5b_e5_common','m5b_e6r2_common')
 module=types.ModuleType('E6R2_region_helper');module.__file__=str(ROOT/'tools/m5b_e5_finish.py');exec(compile(source,module.__file__,'exec'),module.__dict__)
 module.stitch()

def clamp_place():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs=fps(b)
 fs['R985'].SetPosition(pt(128,75));fs['R986'].SetPosition(pt(128,72))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
if __name__=='__main__':
 action=sys.argv[1]
 if action=='route':route(sys.argv[2:])
 else:globals()[action]()
