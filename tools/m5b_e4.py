#!/usr/bin/python3
"""Dedicated E4 reproduction; frozen E3 tooling/data never written."""
import argparse,sys,json,subprocess
from m5b_e4_common import *
from m5b_e3_common import LENGTHS
def checks():
 import m5b_pcb;m5b_pcb.D=OUT
 sys.argv=[sys.argv[0],'--checks'];import m5b_exports as e
 e.D=OUT;e.LOG=OUT/'check-commands.json';e.logs=[];e.main()
def verify():
 import m5b_verify as v
 v.OUT=OUT;v.preserved=preserved;orig=v.configure
 def configure():
  orig()
  for r,l in LENGTHS.items():
   val,a,z=v.r4.REF[r];v.r4.REF[r]=('50R '+str(l)+'mm',a,z)
 v.configure=configure;v.main()
 a=json.loads((OUT/'pinout-audit.json').read_text());a['revision']=REV;save('pinout-audit.json',a)
 import m5b_models as m;m.OUT=OUT;m.costs()
 (OUT/'cost-delta.csv').rename(OUT/'R4-context-cost-delta.csv')
 assert json.loads((OUT/'costs.json').read_text())['summary']==json.loads((HW/'review/M5B-E3/costs.json').read_text())['summary']
def dfm():
 # Run the full preserved eleven negative tests against the E4 native board.
 import m5b_e3_dfm as d
 d.OUT=OUT;d.REV=REV;d.save=save;d.gitfile=lambda path:subprocess.check_output(['git','show','2ca4c8e:'+str(path)],cwd=ROOT)
 sys.argv=[sys.argv[0],'--regression'];d.main()
def exports(render):
 import m5b_pcb;m5b_pcb.D=OUT
 sys.argv=[sys.argv[0]]+(['--render']if render else[]);import m5b_exports as e
 e.D=OUT;e.LOG=OUT/'export-commands.json';e.logs=[];e.main()
def main():
 a=argparse.ArgumentParser();a.add_argument('action',choices=['checks','verify','dfm','exports','thermal','engineering','reports','delivery','models']);a.add_argument('--render',action='store_true');x=a.parse_args();guard()
 if x.action=='checks':checks()
 elif x.action=='verify':verify()
 elif x.action=='dfm':dfm()
 elif x.action=='exports':exports(x.render)
 elif x.action=='thermal':
  import m5b_e4_thermal as t;t.main()
 elif x.action=='models':
  # Reproduce unchanged E3 RF and main-power analyses on the E4 native PCB.
  # Redirect every output before invoking functions; do not invoke E3 main.
  src=(ROOT/'tools/m5b_e3_models.py').read_text().replace('from m5b_e3_common import *','from m5b_e3_common import *\nfrom m5b_e4_common import *').replace('hardware/2m/review/M5B-E3/','hardware/2m/review/M5B-E4/')
  ns={'__name__':'e4_reused_RF_power_models'};exec(compile(src,'m5b_e3_models.py','exec'),ns)
  for n in ['rf','source_parasitics','power']:ns[n]()
  import m5b_e3_power_paths as pw;pw.OUT=OUT;pw.save=save;pw.main()
 else:
  m=__import__('m5b_e4_'+x.action);m.main()
if __name__=='__main__':main()
