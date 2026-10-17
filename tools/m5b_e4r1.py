#!/usr/bin/python3
"""Dedicated E4R1 actions; frozen E3/E4 evidence is never an output."""
import argparse,sys,subprocess,json
from m5b_e4r1_common import *
def inherited(action,render=False):
 src=(ROOT/'tools/m5b_e4.py').read_text().replace('from m5b_e4_common import *','from m5b_e4r1_common import *').replace('from m5b_e4_common import *\\n','from m5b_e4r1_common import *\\n').replace("hardware/2m/review/M5B-E4/'","hardware/2m/review/M5B-E4R1/'")
 ns={'__name__':'e4r1_reused_actions'};exec(compile(src,'m5b_e4.py','exec'),ns)
 if action in['checks','verify','dfm']:ns[action]()
 elif action=='exports':ns[action](render)
 elif action=='models':
  src=(ROOT/'tools/m5b_e3_models.py').read_text().replace('from m5b_e3_common import *','from m5b_e3_common import *\nfrom m5b_e4r1_common import *').replace('hardware/2m/review/M5B-E3/','hardware/2m/review/M5B-E4R1/')
  z={'__name__':'r1_RF_power'};exec(compile(src,'m5b_e3_models.py','exec'),z)
  for n in['rf','source_parasitics','power']:z[n]()
  import m5b_e3_power_paths as pw;pw.OUT=OUT;pw.save=save;pw.main()
def main():
 a=argparse.ArgumentParser();a.add_argument('action',choices=['checks','verify','dfm','models','thermal','engineering','exports','reports','delivery']);a.add_argument('--render',action='store_true');x=a.parse_args();guard()
 if x.action in['checks','verify','dfm','models','exports']:inherited(x.action,x.render)
 else:__import__('m5b_e4r1_'+x.action).main()
if __name__=='__main__':main()
