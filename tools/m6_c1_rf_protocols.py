#!/usr/bin/python3
"""Read-only replay of RF2M native logic; never writes RF review history."""
import json,itertools,os
from pathlib import Path
import m5a_r4_verify as r4
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'hardware/controller/review/M6-C1'
def main():
 os.environ['RF80_NETLIST']=str(D/'inputs/RF80-interface.xml')
 from m3a_r1_logic import verify
 rf80=verify();assert rf80['truth_cases']==256 and len(rf80['state_scenarios'])==31 and len(rf80['timing_corners'])==16
 (D/'RF80-protocol-regression.json').write_text(json.dumps({'status':'PASS_READ_ONLY_NATIVE_PIN_MODEL','source':'inputs/RF80-interface.xml','result':rf80,'physical':'NOT_RUN'},indent=2)+'\n')
 print('RF80:256 truth cases,31 states,16 RC corners,2 polarity mutations')
 parts={p['ref']:p for p in json.loads((ROOT/'hardware/2m/RF2M.electrical.json').read_text())['parts']};n={r:p['pins'] for r,p in parts.items()};r4.old.Logic=r4.Logic;result=r4.old.tests(n)
 m=r4.Logic(n);v=m.step(**{**r4.old.BASE,'PREPARE':1,'MUTE_N':1,'SAFE_N':1,'ARM':0,'SLOT':0});assert v['SRC_ON'] and not v['NORMAL_PERMIT'] and not v['TRAIN_PERMIT'];result['scenarios'].append('powered_source_configuration_ARM_SLOT_low')
 for path in [0,1]:
  m=r4.Logic(n);i={**r4.old.BASE,'PREPARE':1,'PA_PREPARE':1-path,'PATH_TRAIN':path};m.step(**i);i['ARM']=1;m.step(**i);i['ARM_RC']=1;m.step(**i);i['SLOT']=1;v=m.step(**i);assert v['NORMAL_OFF']==bool(path);i['SAFE_N']=0;v=m.step(**i);assert v['NORMAL_OFF'] and not v['SRC_ON'] and not v['NORMAL_PERMIT'] and not v['TRAIN_PERMIT'];result['scenarios'].append('physical_normal_clock_bias_driver_controls_path'+str(path))
 rows=[]
 for prepare,safe,mute,pa in itertools.product([0,1],repeat=4):
  v=r4.Logic(n).step(**{**r4.old.BASE,'PREPARE':prepare,'SAFE_N':safe,'MUTE_N':mute,'PA_PREPARE':pa})
  assert v['SRC_ON']==bool(prepare and safe and mute);assert v['CONV_EN']==bool(prepare and safe and mute and pa);rows.append(dict(PREPARE=prepare,SAFE_N=safe,MUTE_N=mute,PA_PREPARE=pa,SRC_ON=v['SRC_ON'],CONV_EN=v['CONV_EN']))
 (D/'RF2M-protocol-regression.json').write_text(json.dumps({'status':'PASS_READ_ONLY_NATIVE_LOGIC','logic':result,'preparation_truth_rows':rows,'physical_timing':'NOT_RUN','RF_source_files_modified':False},indent=2)+'\n');print(result['combinations'],'combinations',len(result['scenarios']),'states,16source/converter cases')
if __name__=='__main__':main()
