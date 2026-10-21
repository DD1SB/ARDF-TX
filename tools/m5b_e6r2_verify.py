"""Independent actual-netlist/native-pad and mechanical regression for E6R2.
Static logic and dimensional checks do not establish RF or thermal qualification.
"""
import copy,itertools,math,types,shutil,tempfile,xml.etree.ElementTree as ET
import m5a_r1_design as cad
import m5a_r4_verify as r4
import m5b_verify as vb
from m5b_e6r2_common import *
from m5b_e6r2_geometry import geometry as dimensions
from m5b_e3_common import LENGTHS,WIDTH
MAPS={
 'U970':{'1':'VPA_READY','2':'VPA_READY_REF','3':'VPA_READY_S','4':'GND','5':'DRV_READY_S','6':'DRV_READY_REF','7':'DRV_READY','8':'V3V3'},
 'U971':{'1':'VPA_READY','2':'DRV_READY','3':'GND','4':'RF_NOT_READY','5':'V3V3'},
 'U972':{'1':'NORMAL_OFF','2':'KEY_N','3':'CLOCK_OFF','4':'GND','5':'LOCAL_MOD_OFF','6':'RF_NOT_READY','7':'LOCAL_MOD_OFF','8':'V3V3'},
 'U973':{'1':None,'2':'LOCAL_MOD_OFF','3':'GND','4':'DRIVER_ON','5':'V3V3'},
 'Q401':{'1':'PASS_BASE','2':'VPA_PRE','3':'VMOD'},
 'Q402':{'1':'MOD_BASE','2':'MOD_SINK','3':'MOD_E'},
 'Q404':{'1':'MOD_OFF_BASE','2':'GND','3':'MOD_BASE'},
 'Q405':{'1':'MOD_COMMAND_OFF_BASE','2':'GND','3':'MOD_COMMAND'},
 'R970':{'1':'VPA_PRE','2':'VPA'},'R985':{'1':'NORMAL_OFF','2':'MOD_COMMAND_OFF_BASE'},'R986':{'1':'MOD_COMMAND_OFF_BASE','2':'GND'} }
MAPS['U402']={'1':'AF_DC','2':'GND','3':'GND','4':'AM_COMMAND','5':'V3V3','6':'KEY'}
def configure():
 vb.configure();r4.DEST=HW;r4.OUT=OUT
 for r,l in LENGTHS.items():
  v,a,b=r4.REF[r];r4.REF[r]=('50R '+str(l)+'mm',a,b)
 for ref,n in MAPS.items():r4.PIN_UPDATES[ref]=('ST/TI manufacturer pin table; E6R2 explicit electrical adaptation',n,'NATIVE_PIN_ASSERTION')
 for r,k,v in [('U305','3','DRIVER_ON'),('U601','1','CLOCK_OFF')]:
  source,n,status=r4.PIN_UPDATES[r];n=copy.deepcopy(n);n[k]=v;r4.PIN_UPDATES[r]=(source,n,status)

def circuit(parts,nets):
 r4.pins(parts,nets);r4.reference(parts,nets)
 assert nets['U402']['3']=='GND' and nets['U402']['6']=='KEY'
 assert nets['R509']=={'1':'LOCAL_MOD_OFF','2':'MOD_OFF_BASE'}
 assert nets['Q502']['1']=='NORMAL_OFF','Slot bias clamp must remain independent of KEY'
 for ref,n in MAPS.items():assert nets[ref]==n,(ref,nets[ref])
 for ref,mpn in [('Q501','PD54008L-E'),('Q401','D45H11'),('Q402','BD139'),('U970','TLV7032DGKR'),('U972','SN74LVC2G32DCTR')]:assert parts[ref]['mpn']==mpn,(ref,parts[ref]['mpn'])
 vals={'R970':'0.05','R971':'100k','R972':'33k','R973':'330k','R974':'2.49k','R975':'100k','R976':'33k','R977':'19.1k','R978':'10k','R985':'10k','R986':'100k'}
 for r,v in vals.items():assert parts[r]['value']==v,(r,v)
 assert parts['U972']['footprint']=='ARDF_2M:LVC2G32_DCT_E6R2'
 assert parts['R970']['population']=='NORMAL'

def physical(b,parts,nets):
 fs=fps(b);count=0
 for ref,part in parts.items():
  if ref.startswith('#'):continue
  f=fs[ref];got={}
  for a in f.Pads():
   pin=a.GetNumber()
   if not pin:continue
   if ref=='U205' and pin in ['3','11']:assert a.GetNetname()=='';continue
   net=a.GetNetname();got[pin]=None if net.startswith('unconnected-') else net
   assert got[pin]==nets[ref][pin],('native pad',ref,pin,net,nets[ref].get(pin))
  assert got==nets[ref],('native pad set',ref)
  assert f.GetFPIDAsString()==part['footprint'],('native footprint',ref)
  count+=1
 for r,pitch in [('U970',.65),('U972',.65)]:
  f=fs[r];a={q.GetNumber():q for q in f.Pads()};assert abs(math.dist(xy(a['1'].GetPosition()),xy(a['2'].GetPosition()))-pitch)<1e-6
 return count

def mechanical(b,g=None):
 g=copy.deepcopy(g or dimensions());fs=fps(b);errors=[]
 def ck(ok,code):
  if not ok:errors.append(code)
 eds=[d for d in b.GetDrawings() if d.GetLayer()==p.Edge_Cuts];points=[xy(v) for e in eds for v in [e.GetStart(),e.GetEnd()]]
 ck([min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points)]==[20,20,170,130],'outline')
 ck(len(eds)==20,'two_rounded_cutouts')
 for r,loc in zip(['H1','H2','H3','H4'],g['PCB']['corner_holes']):
  ck(math.dist(xy(fs[r].GetPosition()),loc)<1e-6,'mount_pattern')
  ck(all(a.GetAttribute()==p.PAD_ATTRIB_NPTH and abs(p.ToMM(a.GetDrillSize().x)-3.2)<1e-6 for a in fs[r].Pads()),'mount_drill')
 ck(g['sink']['part']=='Fischer SK81 100 SA' and g['sink']['bounds']==[42,20,-22.9,142,120,-7.9],'single_cooler_identity')
 ck(g['common_plane_Z']==g['sink']['bounds'][5],'common_plane')
 ck(len(g['independent_support']['side_taps'])==4 and len(g['independent_support']['foot_holes'])==4,'independent_support')
 ck(g['independent_support']['base_inner_Z']==-33.6,'fin_air_clearance')
 ck(g['source_bar']['TIM_thickness']>=.25,'insulated_full_bar_contact')
 ck(g['source_bar']['bounds']==[84.5,28,-7.85,99.5,72,-1.85],'source_path')
 for ref,loc in [('H5',[92,32]),('H6',[92,68])]:ck(math.dist(xy(fs[ref].GetPosition()),loc)<1e-6,'source_mount')
 for ref,d in g['devices'].items():
  f=fs[ref];ck(math.dist(xy(f.GetPosition()),d['pin1'])<1e-5 and f.GetOrientationDegrees()==0,'device_alignment')
  ck(f.GetFPIDAsString()=='ARDF_2M:'+d['footprint'],'formed_footprint')
  pads={a.GetNumber():a for a in f.Pads()};ck(pads['2'].GetNetname()==d['tab_potential'],'live_tab_potential')
  ck(d['mica_size'][2]>=.05 and d['mica'].startswith('Fischer GS'),'tab_insulator')
  ck(abs(d['back_Z']-g['common_plane_Z']-.1)<1e-6,'common_plane')
  ck(d['lead_path_to_1mm_tip']<=d['available_lead_min'] and d['straight_before_bend']>=4.5 and d['bend_radius_center']>=2,'lead_form')
  ck(d['body_bounds'][5]<-1.6,'body_PCB_clearance')
  for pin,a in pads.items():ck(math.dist(xy(a.GetPosition()),[d['pin1'][0]+(int(pin)-1)*d['lead_step'],d['pin1'][1]])<1e-5,'lead_pad_pitch')
  ck([int(q.GetNumber()) for q in sorted(pads.values(),key=lambda a:xy(a.GetPosition())[0])]==d['physical_left_to_right'],'manufacturer_front_lead_order')
  x0,y0,x1,y1=d['cutout']
  needed=[(x0+1,y0),(x1-1,y0),(x1,y0+1),(x1,y1-1),(x1-1,y1),(x0+1,y1),(x0,y1-1),(x0,y0+1)]
  ck(all(any(math.dist(q,k)<1e-5 for q in points) for k in needed),'native_cutout')
  bx0,by0,_,bx1,by1,_=d['body_bounds'];ck(x0<bx0 and bx1<x1 and y0<by0 and by1<y1,'body_cutout_fit')
  mx,my=d['hole'];mw,ml,mt=d['mica_size'];m_top=my-d['mica_top_offset']
  ck(mx-mw/2<bx0 and bx1<mx+mw/2 and m_top<by0 and by1<m_top+ml,'mica_full_tab_coverage')
 ck(g['devices']['Q401']['bush']['shoulder_OD']<g['devices']['Q401']['hole_diameter_min'],'shoulder_clearance')
 ck(g['devices']['Q401']['bush']['shoulder_length']<g['devices']['Q401']['tab_thickness'][0],'bush_bottoming')
 ck('PA66' in g['devices']['Q402']['screw'],'Q402_screw_insulation')
 ck(math.dist(xy(fs['Q501'].GetPosition()),[92,55])<1e-5 and fs['Q501'].GetOrientationDegrees()==0,'PA_RF_pose')
 models=[m.m_Filename for f in b.GetFootprints() for m in f.Models()]
 legacy=['SK100','FK213','E5_pass_cooling_envelope','E5_BD139_assembly_envelope','E5_PA_cooling_envelope','E4_PA_cooling_envelope']
 ck(sum('E6R2_unified_cooling.step' in x for x in models)==1 and not any(any(old in x for old in legacy) for x in models),'one_native_cooler_model')
 ck(all(r+'_CommonPlane_E6R2.step' in ''.join(models) for r in ['Q401','Q402']),'native_device_models')
 return sorted(set(errors))

def rf_preservation(b):
 fn=OUT/'development/E5-native.kicad_pcb';fn.write_bytes(gitfile('hardware/2m/RF2M.kicad_pcb'));old=p.LoadBoard(str(fn));of=fps(old);fs=fps(b)
 refs=set(r4.REF)|{'Q501','U501','L606','L635','J501','J701','C635','TP601','TP602','TP603','TP604','J101','J301'}
 for r in refs:
  assert fs[r].GetPosition()==of[r].GetPosition() and fs[r].GetOrientationDegrees()==of[r].GetOrientationDegrees(),('RF/access pose',r)
  assert sorted((a.GetNumber(),xy(a.GetPosition()),xy(a.GetSize()),a.GetNetname()) for a in fs[r].Pads())==sorted((a.GetNumber(),xy(a.GetPosition()),xy(a.GetSize()),a.GetNetname()) for a in of[r].Pads()),('RF pad',r)
 protected=set(json.loads(gitfile('hardware/2m/review/M5B-E5/normal-RF-copper-equivalence.json'))['RF_nets'])
 def tracks(bb):return sorted((t.GetNetname(),t.GetLayer(),xy(t.GetStart()),xy(t.GetEnd()),t.GetWidth()) for t in bb.GetTracks() if t.GetNetname() in protected)
 assert tracks(b)==tracks(old),'Critical RF copper changed'
 # Every source joint/via/mask/paste datum must remain present; no thermal fill.
 def vias(bb):return sorted((xy(v.GetPosition()),v.GetWidth(),v.GetDrillValue(),v.GetNetname(),v.GetFrontTentingMode(),v.GetBackTentingMode()) for v in bb.GetTracks() if isinstance(v,p.PCB_VIA) and 89<xy(v.GetPosition())[0]<95 and 48<xy(v.GetPosition())[1]<62)
 assert len(vias(b))==98 and vias(b)==vias(old),'98source vias'
 for layer in [p.F_Mask,p.F_Paste]:
  def shapes(f):return sorted((v.GetShape(),xy(v.GetStart()),xy(v.GetEnd()),v.GetWidth()) for v in f.GraphicalItems() if v.GetLayer()==layer)
  assert shapes(fs['Q501'])==shapes(of['Q501']),'Source mask/paste changed'
 controller=p.LoadBoard(str(ROOT/'hardware/controller/CTRL.kicad_pcb'));cn={a.GetNumber():a.GetNetname() for a in fps(controller)['J5'].Pads()};rn={a.GetNumber():a.GetNetname() for a in fs['J101'].Pads()}
 for pin in map(str,range(1,21)):assert rn[pin]==cn[pin] or rn[pin] in cn[pin],('Controller pin',pin,rn[pin],cn[pin])
 return dict(critical_parts=sorted(refs),RF_nets=sorted(protected),unchanged_RF_tracks=len(tracks(b)),source_vias=98,source_paste_mm2=6.765,connector_pins=rn,ground_review='Local source region and line keepouts retained. Two modulator cutouts outside RF signal corridor change remote ground boundary; physical stability/spectrum qualification remains NOT_RUN.')

def main():
 guard();configure();parts,nets=r4.load();circuit(parts,nets);b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));count=physical(b,parts,nets);assert not mechanical(b),mechanical(b);rf=rf_preservation(b)
 from m5a_r4_footprints import check
 packages=check(HW/'ARDF_2M.pretty',cad.parse,cad.child,cad.children)
 r4.old.Logic=r4.Logic;logic=r4.old.tests(nets)
 # Independent expected truth table; actual nets/pin numbers determine outputs.
 rows=[]
 for off,key,vr,dr in itertools.product([0,1],repeat=4):
  v={'GND':0,'V3V3':1,'NORMAL_OFF':off,'KEY_N':1-key,'VPA_READY':vr,'DRV_READY':dr}
  for unused in range(3):
   n=nets['U971'];v[n['4']]=int(not(v[n['1']] and v[n['2']]))
   n=nets['U972']
   for a,c,y in [('1','2','7'),('5','6','3')]:v[n[y]]=int(v.get(n[a],0) or v.get(n[c],0))
   n=nets['U973'];v[n['4']]=1-v[n['2']]
  assert v['DRIVER_ON']==int(not off and key)
  assert v['CLOCK_OFF']==int(off or not key or not vr or not dr)
  rows.append(dict(off=off,KEY=key,VPA_ready=vr,driver_ready=dr,clock_inhibited=v['CLOCK_OFF']))
 mutations=[]
 def rejected(name,fn):
  try:fn()
  except (AssertionError,KeyError):mutations.append(name)
  else:raise AssertionError('Mutation escaped '+name)
 for ref,pin,bad in [('Q501','G','GND'),('Q501','S','PA_DRAIN'),('Q401','2','GND'),('Q402','2','GND'),('U501','1','MMIC_RF_DC'),('U205','1','V3V3'),('U205','5','V3V3'),('U206','13','V3V3'),('U206','4','NORMAL_Q'),('U304','5','NORMAL_PERMIT'),('U305','3','V3V3'),('U601','1','GND'),('C642','2','GND'),('C632','2','GND'),('TL607','2','NORMAL_RF'),('R517','1','GND'),('U970','2','VPA_READY_S'),('U971','4','CLOCK_OFF'),('U972','2','V3V3'),('U973','2','NORMAL_OFF'),('Q405','1','MOD_OFF_BASE'),('R985','1','LOCAL_MOD_OFF'),('Q502','1','LOCAL_MOD_OFF'),('U402','3','LEVEL_DC'),('R970','2','GND'),('J101','7','ARM'),('R509','1','NORMAL_OFF')]:
  nn=copy.deepcopy(nets);nn[ref][pin]=bad;rejected(ref+'.'+pin,lambda:circuit(parts,nn))
 for ref,bad in [('R309','0.1'),('R828','10k'),('L604','180n'),('L634','18n'),('C633','27p'),('C631','56p'),('R970','0'),('R977','10k')]:
  pp=copy.deepcopy(parts);pp[ref]['value']=bad;rejected(ref+'_value',lambda:circuit(pp,nets))
 for ref,pin,bad in [('U950','6','VDRV_RF'),('U950','7','VDRV_LDO_IN'),('U303','3','VMOD'),('R952','2','VDRV_FILTER'),('R650','2','NORMAL_RF'),('C960','1','BAT_RAW'),('Q502','2','BIAS_WIPER'),('J101','3','I2C_SCL'),('J302','1','VBUCK')]:
  nn=copy.deepcopy(nets);nn[ref][pin]=bad;rejected(ref+'.'+pin,lambda:circuit(parts,nn))
 pp=copy.deepcopy(parts);pp['C632']['value']='390p';rejected('ST330p_conflicting391code',lambda:circuit(pp,nets))
 for name,original,bad in [('PHA1_DF782_RevG.kicad_mod','(at -1.4986 -0.7493)','(at 1.4986 -0.7493)'),('TI_RNW0013A_4222804C.kicad_mod','(pad "7" smd roundrect(at 0 0)','(pad "7" smd roundrect(at -0.55 0)')]:
  with tempfile.TemporaryDirectory(prefix='E6R2-manufacturer-pad-') as tmp:
   for f in (HW/'ARDF_2M.pretty').glob('*.kicad_mod'):shutil.copy(f,tmp)
   f=Path(tmp)/name;s=f.read_text();assert original in s;f.write_text(s.replace(original,bad,1));rejected(name+'_physical_displacement',lambda:check(tmp,cad.parse,cad.child,cad.children))
 a=next(a for a in fps(b)['Q501'].Pads() if a.GetNumber()=='G');pos=a.GetPosition();a.Move(pt(4.5,0));rejected('ST_gate_wrong_physical_side',lambda:rf_preservation(b));a.SetPosition(pos)
 for r in ['U970','U972','Q401','Q402']:
  a=next(q for q in fps(b)[r].Pads() if q.GetNumber()=='2');old=a.GetNet();a.SetNet(b.FindNet('GND'));rejected(r+'_physical_pin_swap',lambda:physical(b,parts,nets));a.SetNet(old)
 oldflat=OUT/'development/pre-flat-pin-correction/RF2M.kicad_pcb'
 if oldflat.exists():
  wrong=p.LoadBoard(str(oldflat));assert 'manufacturer_front_lead_order' in mechanical(wrong)
  mutations.append('actual_initial_flat_BD139_front_reversed')
 f=fps(b)['Q401'];legacy=p.FP_3DMODEL();legacy.m_Filename='${KIPRJMOD}/ARDF_2M.3dshapes/E5_pass_cooling_envelope.wrl';f.Models().push_back(legacy)
 assert 'one_native_cooler_model' in mechanical(b);mutations.append('actual_legacy_second_cooler_model_added');f.Models().pop_back()
 for path,bad in [('common_plane_Z',-9.9),('source_bar.TIM_thickness',0),('devices.Q401.back_Z',-4),('devices.Q402.screw','M2.5steel'),('devices.Q401.mica_size',[12,18,0]),('devices.Q401.bush.shoulder_length',2),('devices.Q402.lead_path_to_1mm_tip',30),('sink.part','Separate three coolers'),('independent_support.side_taps',[])]:
  g=copy.deepcopy(dimensions());node=g;keys=path.split('.')
  for k in keys[:-1]:node=node[k]
  node[keys[-1]]=bad
  rejected(path,lambda:(_ for _ in ()).throw(AssertionError()) if mechanical(b,g) else None)
 for ref in ['Q401','Q402','Q501','H1','H6']:
  f=fps(b)[ref];pos=f.GetPosition();f.Move(pt(1,0))
  rejected(ref+'_pose',lambda:(_ for _ in ()).throw(AssertionError()) if mechanical(b) else None)
  f.SetPosition(pos)
 save('verification.json',dict(status='PASS_NATIVE_STATIC_AND_NUMERICAL_GATES',native_sha256=sha(HW/'RF2M.kicad_pcb'),parts=count,manufacturer_pin_maps=len(r4.pins(parts,nets)),critical_package_landings=packages,logic=logic,keying_truth_rows=rows,negative_tests=mutations,RF=rf,physical='NOT_RUN',limitations='No fabricated assembly; DC/RF device parameters and converter switching loop require measurement. No claimed operational firmware completion.'))
 save('pinout-audit.json',dict(devices=r4.pins(parts,nets),physical_packages=count,RF=rf,physical='NOT_RUN'))
 print('PASS',count,'native packages;',logic['combinations'],'enable combinations;',len(logic['scenarios']),'safety scenarios;',len(rows),'keying rows;',len(mutations),'negative cases;',len(r4.pins(parts,nets)),'critical pin maps')
if __name__=='__main__':main()
