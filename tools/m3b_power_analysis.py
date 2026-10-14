#!/usr/bin/env python3
"""Reproducible bounded input/driver calculations and actual passive ngspice runs."""
import argparse,csv,json,math,subprocess,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def calc():
 m={p['ref']:p for p in json.loads((ROOT/'hardware/80m/RF80.electrical.json').read_text())['parts']}
 assert m['R350']['pins']=={'1':'VIN_PACK','2':'VIN_PA'}and m['C350']['value']=='100u / 35V'
 assert m['R313']['pins']['1']=='VIN_PACK'
 corners=[]
 # Entire circuit is NOT SPICE-modelled. Ignore diode drop conservatively.
 for supply in (16.8,17.0):
  for l in (1e-7,1e-6,10e-6,100e-6):
   for c in (80e-6,145e-6):
    for rs in (.02,1.0):
     rr=1.5*.985+rs;z=rr/(2*math.sqrt(l/c))
     overshoot=0 if z>=1 else math.exp(-math.pi*z/math.sqrt(1-z*z))
     corners.append(dict(step_v=supply,cable_L_H=l,C_F=c,source_R_ohm=rs,damper_R_min_ohm=1.4775,damping_ratio=z,peak_v=supply*(1+overshoot)))
 inrush=145e-6*17**2/(2*(1.4775+.02))
 # Actual ngspice runs: parasitic inductance, minimum C, ESR and imposed opening.
 simulations=[];wave=None;circuit=None
 for vin,off,esr,ls,hf in [(16.8,20,.03,10e-9,.88),(18,20,.5,100e-9,.88),(18,100,.5,100e-9,.88),(18,20,1.5,100e-9,.88),(18,20,.5,100e-9,0.000001)]:
  cir=f'''RF80 M3B driver rail surrogate: imposed opening, no semiconductor timing guarantee
VPA LOAD 0 PWL(0 8.6 1u 8.6 1.0001u {vin} {1+off}u {vin} {1+off+.0001}u 0)
L_LAYOUT LOAD DAMPER {ls}
R410 DAMPER VDRV 4.653
C_HF VDRV 0 {hf}u
R_ESR VDRV BULK {esr}
L_ESL BULK BULK_C 10n
C404 BULK_C 0 37.6u
.control
set wr_singlescale
set wr_vecnames
tran 0.01u 250u
wrdata result.dat v(VDRV) i(VPA)
quit
.endc
.end
'''
  with tempfile.TemporaryDirectory(prefix='rf80-m3b-')as tmp:
   p=Path(tmp);(p/'test.cir').write_text(cir);r=subprocess.run(['ngspice','-b','test.cir'],cwd=p,capture_output=True,text=True);assert r.returncode==0,r.stderr
   rows=[list(map(float,x.split()))for x in (p/'result.dat').read_text().splitlines()[1:]]
  simulations.append(dict(step_v=vin,imposed_opening_us=off,credited_HF_uF=hf,bulk_ESR_ohm=esr,layout_L_H=ls,driver_max_v=max(a[1]for a in rows),driver_min_v=min(a[1]for a in rows),within_12_6_v=max(a[1]for a in rows)<=12.6))
  if vin==18 and off==20 and esr==.5 and hf>.1:wave=rows;circuit=cir
 r=dict(date='2026-10-14',revision='M3B-E1',classification='DESIGN CALCULATIONS AND LINEAR-PASSIVE NGSPICE; NO HARDWARE MEASUREMENTS',input_corners=corners,input_max_qualified_cable_L_H=10e-6,nominal_pack_limit_v=16.8,analysis_margin_step_v=17,input_max_v_in_stated_envelope=max(x['peak_v']for x in corners if x['cable_L_H']<=10e-6),input_stress_100uH_max_v=max(x['peak_v']for x in corners),inrush_i2t_upper_a2s=inrush,nominal_fuse_i2t_a2s=.0766,fuse_nominal_i2t_fraction=inrush/.0766,damper_active_loss_at_060A_w=.6**2*1.5,damper_20percent_loss_w=.2*.6**2*1.5,disconnect_energy_at_10uH_080A_j=.5*10e-6*.8**2,driver_surrogates=simulations,open=['Cable/source model is assumed and must be measured; not a surge-standard rating','TVS17V does not guarantee18/20V clamp; wrong-source DC overvoltage excluded','Input fuse interrupt35A requires upstream protected-pack fault-current coordination; first tests current-limited lab only','20us switch/comparator timing imposed, not simulated or guaranteed','Capacitor ESR/ESL0-50C and pulse resistor SOA require qualification','No transistor RF, AM, CW, antenna, thermal, safety or endurance measurement'])
 # Passive hot-plug sensitivity including the *upstream* small capacitor.
 # The generic diode is an approximation, not a vendor SS34 model.
 hot=[];hotcir=None
 for ll in (.1,1,10,100):
  for cs in (.00001,.04,.11):
   for rs in (.02,1.):
    ci=f'''RF80 input surrogate; generic diode, not manufacturer validated
V1 SRC 0 PWL(0 0 1n 17)
RS SRC CABLE {rs}
L1 CABLE DIODE {ll}u
D1 DIODE PACK DMOD
.model DMOD D(Is=1m Rs=.02 N=1 Cjo=50p)
C314 PACK 0 {cs}u
R350 PACK VIN 1.4775
R_ESR VIN BULK .03
C350 BULK 0 80u
.control
set wr_singlescale
set wr_vecnames
tran .02u 2m
wrdata out.dat v(PACK) v(VIN)
quit
.endc
.end
'''
    with tempfile.TemporaryDirectory(prefix='rf80-m3b-input-')as tmp:
     pp=Path(tmp);(pp/'in.cir').write_text(ci);pr=subprocess.run(['ngspice','-b','in.cir'],cwd=pp,capture_output=True,text=True);assert pr.returncode==0,pr.stderr
     rows=[[float(x)for x in l.split()]for l in(pp/'out.dat').read_text().splitlines()[1:]]
    hot.append(dict(cable_L_uH=ll,upstream_C_uF=cs,source_R_ohm=rs,VIN_PACK_max_V=max(v[1]for v in rows),VIN_PA_max_V=max(v[2]for v in rows)))
    if ll==.1 and cs==.11 and rs==.02:hotcir=ci
 r['input_ngspice_surrogates']=hot;r['upstream_node_max_surrogate_V']=max(q['VIN_PACK_max_V']for q in hot)
 r['post_damper_max_surrogate_V']=max(q['VIN_PA_max_V']for q in hot)
 r['input_model_limitations']='Generic diode, assumed wiring/ESR, no connector arc, source surge or component-failure qualification. VIN_PACK and VIN_PA are distinct.100uH analytic stress is outside the allowed cable envelope.'
 return r,circuit,wave,hotcir
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();r,c,w,h=calc();f=ROOT/'docs/M3B_POWER_ANALYSIS.json';s=json.dumps(r,indent=2)+'\n'
 if a.write:
  (ROOT/'analysis/m3b_input_surrogate.cir').write_text(h)
  f.write_text(s);(ROOT/'analysis/m3b_driver_surrogate.cir').write_text(c)
  with(ROOT/'analysis/m3b_driver_surrogate.csv').open('w')as p:
   v=csv.writer(p,lineterminator='\n');v.writerow(['time_s','driver_V','source_A']);v.writerows(w)
 else:assert f.read_text()==s,'Power report stale'
 print('PASS passive analysis:',len(r['input_corners']),'input corners, maximum stated envelope',r['input_max_v_in_stated_envelope'],'V; inrush',r['inrush_i2t_upper_a2s'],'A2s; driver',r['driver_surrogates'])
