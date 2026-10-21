"""Reproduction/check entry points. Historical tools are imported read-only."""
import sys,types,shutil,subprocess
from m5b_e6r2_common import *
def exports(render=False,checks=False):
 import m5b_pcb as board;board.D=OUT
 import m5b_exports as e;e.D=OUT;e.LOG=OUT/('check-commands.json' if checks else 'export-commands.json');e.logs=[]
 sys.argv=[sys.argv[0]]+(['--checks'] if checks else [])+(['--render'] if render else []);e.main()
def dfm():
 profile=json.loads((HW/'review/M5B-E5/JLCPCB-standard-profile.json').read_text());profile['revision']=REV;save('JLCPCB-standard-profile.json',profile)
 profile['manual_review'][-1]='E6R2 shared100x100x15sink,15x44x6bar,insulatedcommon-planeTOdevices,roundedcutouts andindependentcarrier supports; first-articlethermal/RF qualification remainsNOT_RUN.'
 profile['configuration']['internal_routed_cutouts']=2
 save('JLCPCB-standard-profile.json',profile)
 src=(ROOT/'tools/m5b_e3_dfm.py').read_text().replace('from m5b_e3_common import *','from m5b_e6r2_common import *').replace('edge[2]-edge[0]-180','edge[2]-edge[0]-150').replace('edge[3]-edge[1]-140','edge[3]-edge[1]-110').replace('for xx in[193.,193.55]','for xx in[155.,155.55]').replace('MM(150.)','MM(126.)').replace('MM(150.5)','MM(126.5)')
 src=src.replace('text=next(g for g in b.GetDrawings()if isinstance(g,p.PCB_TEXT)and g.GetLayer()==p.F_SilkS)','text=next(g for g in b.GetDrawings()if isinstance(g,p.PCB_TEXT)and g.GetLayer()in[p.F_SilkS,p.B_SilkS])')
 m=types.ModuleType('E6R2_native_DFM');m.__file__=str(ROOT/'tools/m5b_e3_dfm.py');exec(compile(src,m.__file__,'exec'),m.__dict__)
 m.gitfile=lambda path:subprocess.check_output(['git','show','2ca4c8e:'+path],cwd=ROOT)
 sys.argv=[sys.argv[0],'--regression'];m.main()
 # Internal routed cutouts are additional to the original rectangle checker.
 from m5b_e6r2_geometry import geometry
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));rows=[]
 for d in geometry()['devices'].values():
  # Conservative rectangular envelope includes rounded corners. No source/RF
  # geometry is near either cutout. Native DRC tests true routed arcs too.
  x0,y0,x1,y1=d['cutout'];box=p.PCB_SHAPE(b);box.SetShape(p.SHAPE_T_RECT);box.SetStart(pt(x0,y0));box.SetEnd(pt(x1,y1));box.SetFilled(True);box.SetWidth(0)
  for obj in list(b.GetTracks())+[a for f in b.GetFootprints() for a in f.Pads() if a.GetAttribute()!=p.PAD_ATTRIB_NPTH]:
   for l in [p.F_Cu,p.B_Cu]:
    if obj.IsOnLayer(l):assert not p.SHAPE.Collide(obj.GetEffectiveShape(l),box.GetEffectiveShape(),MM(.499)),('Cutout copper',obj.m_Uuid.AsString())
  rows.append(dict(cutout=d['cutout'],copper_clearance_mm=.5,corner_radius_mm=1.,ordinary_route=True))
 save('cutout-DFM.json',dict(status='PASS',cutouts=rows,physical='NOT_RUN'))
def source():
 # Reuse all source-joint native mutation assertions, with canonical coordinates.
 from m5b_e5_common import translate_board
 from m5b_e4r1_engineering import audit,bounds
 import math
 b=translate_board(p.LoadBoard(str(HW/'RF2M.kicad_pcb')),20,0);fs=fps(b)
 errors=audit(b);assert set(errors)<= {'live_copper_under_bar'},errors
 # Full-area electrically rated86/82 TIM now explicitly isolates underside;
 # it replaces the old uninsulated bare-bar requirement, not a mask waiver.
 from m5b_e6r2_geometry import geometry
 assert geometry()['source_bar']['TIM_thickness']==.25
 src=(ROOT/'tools/m5b_e4r1_engineering.py').read_text();start=src.index(' tests=[]\n');end=src.index(' source_area=',start);block=src[start:end].replace("(OUT/'thermal-model.json')","(HW/'review/M5B-E5/thermal-model.json')")
 from m5b_e4r1_common import INNER,TOP_RECTS
 from m5b_e4r1_thermal import solve
 context=dict(b=b,fs=fs,p=p,MM=MM,xy=xy,bounds=bounds,math=math,audit=audit,json=json,OUT=OUT,HW=HW,INNER=INNER,TOP_RECTS=TOP_RECTS,solve=solve)
 exec(compile('if True:\n'+block,'E6R2_source_joint_regression','exec'),context)
 save('source-assembly-regression.json',dict(status='PASS',native_tests=context['tests'],thermal_model_negative_cases=context['bad'],change='Full-rated TIM beneath entire bar; no reliance on solder mask. Source/paste/98via geometry preserved.',historical_poor_joint_case='E5 preserved numerical result; other numerical mutations solve afresh',physical='NOT_RUN'))
def power():
 src=(ROOT/'tools/m5b_e3_power_paths.py').read_text().replace('from m5b_e3_common import *','from m5b_e6r2_common import *\nfrom m5b_e3_common import POWER_INPUT')
 src=src.replace("('Q401','2','L635','1')","('Q401','2','R970','1'),('R970','2','L635','1')")
 m=types.ModuleType('E6R2_actual_main_power_paths');m.__file__=str(ROOT/'tools/m5b_e3_power_paths.py');exec(compile(src,m.__file__,'exec'),m.__dict__);m.main()
if __name__=='__main__':
 guard();action=sys.argv[1]
 if action in ['exports','checks']:exports('--render' in sys.argv,action=='checks')
 else:globals()[action]()
