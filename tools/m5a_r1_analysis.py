#!/usr/bin/python3
"""Explicit hypotheses, not a measured PA model. No hardware/firmware/PCB work."""
import csv,json,math,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];O=R/'hardware/2m/review/M5A-R1';A=R/'analysis/m5a_r1';A.mkdir(exist_ok=True)
M={p['ref']:p for p in json.loads((R/'hardware/2m/RF2M.electrical.json').read_text())['parts']}
def res(ref):
 s=M[ref]['value'];return float(s[:-1])*1000 if s.endswith('k')else float(s)
def writecsv(path,rows):
 with path.open('w')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
carrier=10**.1;pep=carrier*1.8**2;capability=pep*10**.1;outloss=10**.075
buck0=.596*(1+res('R301')/res('R302'));buck1=buck0+.596*res('R301')/res('R303')
boost0=1.229*(1+res('R401')/res('R402'));boost1=boost0+1.229*res('R401')/res('R414')
# Deliberately unqualified knee-aware RF transfer hypothesis; ST supplies NO AM curve.
knee=.6;vfull=knee+(7.2-knee)*math.sqrt(carrier/5)
def profile(erp,m,arch,eta=.45,iq=.1,idrv=.146,ctrl=.14,lora=0,knee=knee):
 v0=knee+(7.2-knee)*math.sqrt(carrier*erp/5);a=m*(v0-knee);up=10 if erp>=.9 else 7.5
 # Same affine I(V) shape retained from R0, recalibrated for new assumed voltage/efficiency.
 g=((carrier*outloss)/eta/vfull-iq)/vfull
 i0=iq+g*v0;imax=iq+g*(v0+a);pdc=iq*v0+g*(v0*v0+a*a/2)
 prf=carrier*erp*outloss*(1+m*m/2)
 ppass=up*i0-pdc;pdnotone=(up-v0)*i0
 driver_input=up*(idrv+.0001);helper=.30
 rail=up*i0+driver_input+helper
 etaf=.87 if arch=='BOOST2S'else .91;vbat=7.2 if arch=='BOOST2S'else 14.4
 ptx=rail/etaf+1.3*(rail/etaf/vbat)**2*.15+.10+.11/.9
 idle=.03 if arch=='BOOST2S'else .04
 avg=ctrl+idle+lora+.2*(ptx-idle)
 peak=imax+idrv+.05
 # Additional worst-case helper assumption beta40, VBEpass1, VCEhelper0.3, shunt/FET0.20V.
 ib=imax/40;drop=1+ib*(res('R506')+res('R507'))+.3+.20
 return dict(arch=arch,erp=erp,m=m,vcenter=v0,vcrest=v0+a,vtrough=v0-a,upstream_v=up,carrier_connector_w=carrier*erp,pep_connector_w=carrier*erp*(1+m)**2,rf_mean_connector_w=carrier*erp*(1+m*m/2),pa_carrier_efficiency=(carrier*erp*outloss)/(v0*i0),pa_current_center_a=i0,pa_current_crest_a=imax,upstream_current_crest_a=peak,current_trip_risk=peak>1.8,pa_dc_mean_w=pdc,pa_heat_mean_w=pdc-prf,pass_mean_w=ppass,pass_no_tone_w=pdnotone,driver_dc_w=5*idrv,driver_ldo_heat_w=(up-5)*idrv-idrv*idrv*2.2,helper_allowance_w=helper,tx_battery_w=ptx,average_battery_w=avg,need12_wh=12*avg,need24_wh=24*avg,beacon_w=.30+lora+ptx,headroom_assumed_hot_beta40_v=drop,crest_margin_v=up*.97-(v0+a)-drop,eta_full_assumed=eta,iq_assumed_a=iq)
profiles=[profile(p,m,a)for a in ['BOOST2S','BUCK4S']for p in [1,.9,.3]for m in [.75,.8]]
packs={'2S2P':(2,2),'2S3P':(2,3),'2S4P':(2,4),'4S1P':(4,1),'4S2P':(4,2)};cells={'25R_min':8.82,'M35A_min':11.9}
rows=[]
for p in profiles:
 for pack,(s,par)in packs.items():
  if (s==2)!=(p['arch']=='BOOST2S'):continue
  for cell,wh in cells.items():
   e=s*par*wh*.8*.9*.9;h=e/p['average_battery_w'];goal=12 if p['erp']>=.9 else 24
   rows.append(dict(**p,pack=pack,cell=cell,usable_energy_wh=e,modeled_hours=h,beacon_hours=e/p['beacon_w'],goal_h=goal,model_pass=h>=goal,margin20_pass=h>=goal*1.2))
sensitivity=[]
for a,p,eta,iq,ctrl,idrv,lora in itertools.product(['BOOST2S','BUCK4S'],[1,.3],[.32,.45,.55],[.1,.2],[.14,.28],[.146,.18],[0,.006,.045]):
 x=profile(p,.8,a,eta,iq,idrv,ctrl,lora);sensitivity.append(dict(arch=a,erp=p,eta=eta,iq=iq,controller_w=ctrl,driver_a=idrv,lora_w=lora,average_w=x['average_battery_w'],peak_a=x['upstream_current_crest_a'],current_trip_risk=x['current_trip_risk']))
thermal=[]
for eta,erp,m in itertools.product([.32,.45,.55],[1,.3],[0,.75,.8]):
 x=profile(erp,m,'BUCK4S',eta);v0=x['vcenter'];a=m*(v0-knee);g=((carrier*outloss)/eta/vfull-.1)/vfull
 tr=[]
 for k in range(360):
  v=v0+a*math.sin(2*math.pi*k/360);i=.1+g*v;ib=i/40;ve=ib*8.2;vc=x['upstream_v']-1-ib*10;tr.append(dict(vce=x['upstream_v']-v,ic=i,watts=(x['upstream_v']-v)*i,base_current_beta40=ib,helper_w=max(vc-ve,0)*ib,helper_opamp_command_v=ve+.9+ib/100*1000))
 # Shared spreader, repeated 60s on /240s off, lumped assumption R3C80, zero interslot heat.
 pon=x['pass_mean_w']+x['pa_heat_mean_w']+x['helper_allowance_w']+x['driver_dc_w']+x['driver_ldo_heat_w'];rt=3;ct=80
 aa=math.exp(-60/(rt*ct));bb=math.exp(-240/(rt*ct));rise=rt*pon*(1-aa)/(1-aa*bb)
 case=45+rise+x['pass_mean_w']*1
 thermal.append(dict(eta=eta,erp=erp,m=m,pass_mean_w=x['pass_mean_w'],pass_no_tone_w=x['pass_no_tone_w'],pass_peak_w=max(t['watts']for t in tr),helper_mean_w=sum(t['helper_w']for t in tr)/len(tr),helper_peak_w=max(t['helper_w']for t in tr),helper_opamp_peak_v=max(t['helper_opamp_command_v']for t in tr),hot_case_estimate_c=case,junction_estimate_c=case+max(t['watts']for t in tr)*2.5,spreader_peak_c=45+rise,shared_on_heat_w=pon,trajectory=tr,SOA='OPEN: each hot VCE/IC trajectory requires exact ST DC/repetitive graph and hardware review'))
# LDO short fault, ESR resolved exactly; ideal step then external Q304 disconnect at t.
fault=[]
for t,r,c,esr in itertools.product([5,10,20,50,100],[2.178,2.2,2.222],[120,150,180],[.002,.1]):
 v0=5*1.0175;vf=10.5;tau=(r+esr)*c;v=v0+(vf-v0)*(1-r/(r+esr)*math.exp(-t/tau))
 fault.append(dict(us=t,r=r,c_uf=c,esr=esr,driver_v=v,scope='Ideal LDO-short bounded fixture; assumes Q304 physically opens at t, no parasitic ringing'))
# Zero-copper-thickness microstrip estimate: approximate only, manufacturer stack-up required.
def micro(w,h,er):
 u=w/h;ee=(er+1)/2+(er-1)/2*(1/math.sqrt(1+12/u)+(.04*(1-u)**2 if u<1 else 0))
 z=60/math.sqrt(ee)*math.log(8/u+u/4)if u<=1 else 120*math.pi/math.sqrt(ee)/(u+1.393+.667*math.log(u+1.444))
 return z,ee
def width50(h,er):
 lo,hi=.01,10
 for _ in range(80):
  mi=(lo+hi)/2
  if micro(mi,h,er)[0]>50:lo=mi
  else:hi=mi
 return (lo+hi)/2
lines=[]
for h,er in itertools.product([.508,1.6],[4.2,4.5,4.8]):
 z,ee=micro(.92,h,er);lines.append(dict(h_mm=h,er=er,z_at_0p92mm=z,width50_mm=width50(h,er),epsilon_eff_at0p92=ee,phase_deg_per_mm=360*144.7e6*math.sqrt(ee)/299792458/1000))
w=2*math.pi*144.7e6;rin=6;xx=math.sqrt(rin*(50-rin));ze=1/(1/3.5-1j*w*60e-12);xo=math.sqrt(ze.real*(50-ze.real))
result=dict(classification='CALCULATIONS / ASSUMPTIONS, NO measured RF or thermal performance',erp=dict(connector_carrier_w=carrier,pep80_w=pep,connector_capability_w=capability,final_capability_0p75db_loss_w=capability*outloss,st_reference_shortfall_db=10*math.log10(capability/5)),supply_settings=dict(buck_reduced_v=buck0,buck_full_v=buck1,boost_reduced_v=boost0,boost_full_v=boost1,am_feedback_gain=1+res('R511')/res('R512'),driver_output_v=5,driver_ov_v=2.495*10000/(res('R817')+10000)*(res('R815')+10000)/10000,vpa_ov_v=2.495*12*10000/(res('R821')+10000)),driver=[dict(final_gain_db=g,required_driver_dbm=10*math.log10(capability*outloss*1000)+1.25-g,p1db_required_dbm=10*math.log10(capability*outloss*1000)+1.25-g+3)for g in [15,17,20,22]],capability_voltage_hypothesis=knee+(7.2-knee)*math.sqrt(capability/5),gain_floor_if_p1db22p2=10*math.log10(capability*outloss*1000)+1.25+3-22.2,profiles=profiles,endurance=rows,sensitivity=sensitivity,thermal=thermal,driver_fault=fault,microstrip=lines,matching_hypothesis=dict(status='NOT ST matching; net topology and impedances OPEN',f_mhz=144.7,input_assumed_z_ohm=[5,-10],input_stopper_ohm=1,input_l_nh=(xx+10)/w*1e9,input_c_pf=xx/(50*rin)/w*1e12,output_assumed_r_ohm=3.5,output_assumed_coss_pf=60,output_l_nh=(xo+ze.imag)/w*1e9,output_c_pf=xo/(50*ze.real)/w*1e12),assumptions=dict(cell_energy_wh=cells,aging=.8,temperature=.9,accessible_endpoint=.9,duty=.2,controller_w=.14,rf_idle_2s_w=.03,rf_idle_4s_w=.04,front_eff_boost=.87,front_eff_buck=.91,pa_full_carrier_eff=.45,pa_iq_a=.1,rf_knee_v=.6,st_anchor='Hypothesis: 5W connector at7.2V; no derivative transfer guarantee',full_4s_energy_window=1.0,shared_spreader_c_per_w=3,thermal_capacitance_j_per_k=80,ambient_c=45,pass_interface_c_per_w=1))
(O/'calculations.json').write_text(json.dumps(result,indent=2)+'\n');writecsv(O/'endurance.csv',rows);writecsv(O/'sensitivity.csv',sensitivity);writecsv(A/'driver-fault.csv',fault)
assert abs(carrier-1.2589254118)<1e-8 and abs(pep-4.078918334)<1e-8
assert max(x['driver_v']for x in fault if x['us']<=20)<5.9
assert 4.9<5*(1-.0175)and 5*(1+.0175)<5.2
for p in profiles:
 if p['m']==.8:print(p['arch'],p['erp'],round(p['average_battery_w'],3),'W average',round(p['pass_mean_w'],2),'W pass',round(p['upstream_current_crest_a'],2),'A crest')
print('CALCULATED',len(rows),'pack rows;',len(sensitivity),'sensitivity rows; NO measured results')
