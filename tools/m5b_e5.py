#!/usr/bin/python3
"""Current compact-candidate checks; historical review directories are read-only."""
import sys,types,argparse
from m5b_e5_common import *

def checks():
 import m5b_pcb as board;board.D=OUT
 import m5b_exports as e;e.D=OUT;e.LOG=OUT/'check-commands.json';e.logs=[];sys.argv=[sys.argv[0],'--checks'];e.main()
def verify():
 import m5b_verify as v
 code=(ROOT/'tools/m5b_verify.py').read_text().replace('from m5b_design import HW,OUT,preserved','from m5b_e5_common import HW,OUT,preserved').replace("{'TP601':(108.5,55),'TP602':(115.2,55),'TP603':(145.3,52.206),'TP604':(89.1,55)}","{'TP601':(88.5,55),'TP602':(95.2,55),'TP603':(125.3,52.206),'TP604':(69.1,55)}")
 mod=types.ModuleType('compact_native_verify');mod.__file__=str(ROOT/'tools/m5b_verify.py');exec(compile(code,mod.__file__,'exec'),mod.__dict__);orig=mod.configure
 def configure():
  orig()
  for r,l in LENGTHS.items():
   value,a,z=mod.r4.REF[r];mod.r4.REF[r]=('50R '+str(l)+'mm',a,z)
 mod.configure=configure;mod.main();v=json.loads((OUT/'verification.json').read_text());v.update(revision=REV,date=DATE,frame='Native E5 pad coordinates; RF probes translated -20mmX. Original package maps/logic/value assertions retained.');save('verification.json',v)
 import m5b_models as model;model.OUT=OUT;model.costs()
 (OUT/'cost-delta.csv').rename(OUT/'historical-R4-component-cost-context.csv')
 assert json.loads((OUT/'costs.json').read_text())['summary']==json.loads((HW/'review/M5B-E4R1/costs.json').read_text())['summary']
def dfm():
 src=(ROOT/'tools/m5b_e3_dfm.py').read_text().replace('from m5b_e3_common import *','from m5b_e5_common import *').replace('from m5b_e3_common import aliases','from m5b_e5_common import aliases').replace('edge[2]-edge[0]-180','edge[2]-edge[0]-150').replace('edge[3]-edge[1]-140','edge[3]-edge[1]-110').replace('for xx in[193.,193.55]','for xx in[155.,155.55]').replace('MM(150.)','MM(126.)').replace('MM(150.5)','MM(126.5)')
 src=src.replace('text=next(g for g in b.GetDrawings()if isinstance(g,p.PCB_TEXT)and g.GetLayer()==p.F_SilkS)','text=next(g for g in b.GetDrawings()if isinstance(g,p.PCB_TEXT)and g.GetLayer()in[p.F_SilkS,p.B_SilkS])')
 mod=types.ModuleType('compact_native_dfm');mod.__file__=str(ROOT/'tools/m5b_e3_dfm.py');exec(compile(src,mod.__file__,'exec'),mod.__dict__);mod.gitfile=lambda path:gitfile(path,'2ca4c8e');sys.argv=[sys.argv[0],'--regression'];mod.main()
def exports(render):
 import m5b_pcb as board;board.D=OUT
 import m5b_exports as e;e.D=OUT;e.LOG=OUT/'export-commands.json';e.logs=[];sys.argv=[sys.argv[0]]+(['--render']if render else[]);e.main()
def models():
 code=(ROOT/'tools/m5b_e3_models.py').read_text().replace('from m5b_e3_common import *','from m5b_e3_common import *\nfrom m5b_e5_common import *').replace('hardware/2m/review/M5B-E3/','hardware/2m/review/M5B-E5/')
 mod=types.ModuleType('compact_RF_models');mod.__file__=str(ROOT/'tools/m5b_e3_models.py');exec(compile(code,mod.__file__,'exec'),mod.__dict__)
 for name in['rf','source_parasitics']:mod.__dict__[name]()
 import m5b_e3_power_paths as power;power.OUT=OUT;power.save=save;power.main()
def thermal():
 # Local coordinates are identical after rigid translation. Geometry is
 # asserted separately from actual native mask/paste/vias/bar before accepting.
 src=(ROOT/'tools/m5b_e4r1_thermal.py').read_text().replace('from m5b_e4r1_common import *','from m5b_e5_common import *\nfrom m5b_e4r1_common import SOURCE,SOLDER,INNER,SIDE,NEAR,OUTER,VIAS,TOP_RECTS,WINDOW,BAR,PASTE,via_specs')
 mod=types.ModuleType('compact_thermal');mod.__file__=str(ROOT/'tools/m5b_e4r1_thermal.py');exec(compile(src,mod.__file__,'exec'),mod.__dict__);mod.main()
 t=json.loads((OUT/'thermal-model.json').read_text());t.update(revision=REV,geometry_basis='Actual source assembly and bar are a rigid(-20,0)mm translation, asserted by compact geometry gate. Translation-invariant local solver uses E4R1 coordinates; all prior boundary/uncertainty assumptions preserved.',native_source_geometry_checked='compact-engineering.json',physical='NOT_RUN');save('thermal-model.json',t)
def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['checks','verify','dfm','exports','models','thermal']);ap.add_argument('--render',action='store_true');a=ap.parse_args();guard()
 if a.action=='exports':exports(a.render)
 else:globals()[a.action]()
if __name__=='__main__':main()
