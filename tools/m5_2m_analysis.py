#!/usr/bin/python3
"""Reproducible calculations, ideal passive networks and explicit endurance assumptions."""
import csv,json,math,cmath,itertools
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'hardware/2m/review/M5A-R0';A=R/'analysis/m5_2m';A.mkdir(parents=True,exist_ok=True)
def solve(a,b):
 a=[list(row)+[v]for row,v in zip(a,b)];n=len(b)
 for i in range(n):
  k=max(range(i,n),key=lambda j:abs(a[j][i]));a[i],a[k]=a[k],a[i];z=a[i][i];assert abs(z)>1e-30;a[i]=[x/z for x in a[i]]
  for j in range(n):
   if j!=i:
    z=a[j][i];a[j]=[x-z*y for x,y in zip(a[j],a[i])]
 return[row[-1]for row in a]
def lpf(f,ls,cs,pavail=1,q=80):
 w=2*math.pi*f;n=len(cs);a=[[0j]*n for _ in range(n)];b=[0j]*n
 a[0][0]+=.02;a[-1][-1]+=.02;b[0]=math.sqrt(4*pavail*50)/50
 for i,c in enumerate(cs):a[i][i]+=1j*w*c*1e-12
 for i,l in enumerate(ls):
  z=1j*w*l*1e-9 +w*l*1e-9/q;y=1/z;a[i][i]+=y;a[i+1][i+1]+=y;a[i][i+1]-=y;a[i+1][i]-=y
 v=solve(a,b)
 return dict(f_hz=f,s21_db=10*math.log10(abs(v[-1])**2/50/pavail),volts_rms=[abs(x)for x in v],inductor_current_rms=[abs((v[i]-v[i+1])/(1j*w*l*1e-9+w*l*1e-9/q))for i,l in enumerate(ls)])
loss=10**(.75/10);gainant=10**(-1/10)
carrier=1/gainant;pep=carrier*1.8**2;cap=pep*10**(.1)
def supply(erp,m,arch,eta_carrier=.42,iq=.15,idriver=.2341,controller=.14,idle=None,lora=0):
 # I(V)=Iq+gV; g calibrated at FULL carrier only. Efficiency changes at reduced power.
 if idle is None:idle=.03 if arch=='BOOST2S'else .04
 full_pa_carrier=carrier*loss;vfull=12/1.8;v0=vfull*math.sqrt(erp)
 if erp>=.9:vup=13.5
 else:vup=10
 i0full=full_pa_carrier/eta_carrier/vfull;g=(i0full-iq)/vfull;i0=iq+g*v0
 ppa=iq*v0+g*v0*v0*(1+m*m/2);pcpa=full_pa_carrier*erp
 prf=pcpa*(1+m*m/2);ppass=vup*i0-ppa
 pdriver=8*idriver/.90;extra=.15 # helper base current/rail sensing incremental; source has separate3.3V regulator
 rail=vup*i0+pdriver+extra
 eta_front=.87 if arch=='BOOST2S'else .91
 vbat=7.2 if arch=='BOOST2S'else 14.4;rseries=.15
 # Diode + FET/shunt source loss: solve conservative approximately at nominal battery.
 pideal=rail/eta_front;ptx=pideal+1.3*(pideal/vbat)**2*rseries+.10+.11/.90
 avg=controller+idle+lora+.20*(ptx-idle)
 ipeak=iq+g*v0*(1+m)+pdriver/vup+.02
 return dict(upstream_crest_a=ipeak,current_trip_risk=ipeak>1.20,erp_carrier=erp,m=m,arch=arch,vcarrier=v0,vcrest=v0*(1+m),vtrough=v0*(1-m),conducted_carrier=carrier*erp,conducted_mean=carrier*erp*(1+m*m/2),conducted_pep=carrier*erp*(1+m)**2,pa_carrier_efficiency=pcpa/(v0*i0),upstream_v=vup,pa_mean_w=ppa,pass_mean_w=ppass,pass_no_tone_w=(vup-v0)*i0,driver_rail_w=8*idriver,driver_converter_input_w=pdriver,rail_input_w=rail,tx_battery_w=ptx,average_battery_w=avg,need12_wh=avg*12,need24_wh=avg*24,beacon_average_w=.30+lora+ptx)
profiles=[supply(p,m,a)for a in ['BOOST2S','BUCK4S']for p in [1,.9,.30]for m in [.75,.8]]
packs={'2S2P':(2,2),'2S3P':(2,3),'2S4P':(2,4),'4S1P':(4,1),'4S2P':(4,2)}
cells={'25R_min':8.82,'M35A_min':11.9}
rows=[]
for p in profiles:
 for pack,(s,par)in packs.items():
  if(s==2)!=(p['arch']=='BOOST2S'):continue
  for cell,ecell in cells.items():
   energy=s*par*ecell*.8*.9*.9
   window=.60 if(s==4 and p['erp_carrier']>=.9)else 1
   e=energy*window;h=e/p['average_battery_w'];hb=e/p['beacon_average_w']
   rows.append(dict(**p,pack=pack,cell=cell,usable_energy_wh=e,full_voltage_window=window,modeled_hours=h,modeled_beacon_hours=hb,target_hours=12 if p['erp_carrier']>=.9 else 24,model_pass=h>=(12 if p['erp_carrier']>=.9 else 24),reserve20_pass=h>=(14.4 if p['erp_carrier']>=.9 else 28.8)))
sens=[]
for a in ['BOOST2S','BUCK4S']:
 for erp in [1,.3]:
  for eta,ctrl,idrv,lora in itertools.product([.32,.42,.52],[.14,.28],[.2341,.251],[0,.006,.045]):
   x=supply(erp,.8,a,eta_carrier=eta,controller=ctrl,idriver=idrv,lora=lora)
   sens.append(dict(arch=a,erp=erp,eta_full_carrier=eta,controller_w=ctrl,driver_a=idrv,lora_w=lora,average_w=x['average_battery_w'],current_trip_risk=x['current_trip_risk'],upstream_crest_a=x['upstream_crest_a']))
thermal=[]
for eta in [.32,.42,.52]:
 for erp in [1,.3]:
  for m in [0,.75,.8]:
   x=supply(erp,m,'BOOST2S',eta_carrier=eta);v0=x['vcarrier'];g=((carrier*loss)/eta/(12/1.8)-.15)/(12/1.8)
   trajectory=[]
   for k in range(360):
    v=v0*(1+m*math.sin(2*math.pi*k/360));i=.15+g*v;trajectory.append(dict(vce=x['upstream_v']-v,ic=i,watts=(x['upstream_v']-v)*i))
   thermal.append(dict(eta_full=eta,erp=erp,m=m,mean_w=x['pass_mean_w'],peak_w=max(t['watts']for t in trajectory),max_ic=max(t['ic']for t in trajectory),case_c=45+x['pass_mean_w']*11,junction_c=45+x['pass_mean_w']*13.5,trajectory=trajectory))
filters={}
for name,ls,cs in [('source7',[56,91,56],[8.2,33,33,8.2]),('normal9',[47,93,93,47],[6.8,27,33,27,6.8])]:
 filters[name]=[lpf(f,ls,cs,cap*loss if name=='normal9'else 1,q=q)for q in [40,80,1000]for f in [144e6,144.5e6,144.7e6,144.9e6,148e6,289.4e6,434.1e6]]
rc=[dict(t_us=t,r_ohm=r,c_uf=c,vpeak=8.3+(14.5-8.3)*(1-math.exp(-t/(r*c))))for t,r,c in itertools.product([5,10,20,50,100],[2.178,2.2,2.222],[80,100,120])]
# Worst theoretical envelope node discharge: 101nF, 800Hz, m.8, vcarrier6.667.
calc=dict(date='2026-10-15',classification='CALCULATIONS / ASSUMPTIONS; NOT MEASURED',erp=dict(antenna_net_dbd=-1,conducted_carrier_w=carrier,pep_m80_w=pep,capability_plus1db_w=cap,pa_stage_capability_with_0p75db_output_loss=cap*loss),driver=[dict(pa_gain_db=g,required_driver_dbm=10*math.log10(cap*10**((2.0-g)/10)*1000),required_p1db_dbm=10*math.log10(cap*10**((2.0-g)/10)*1000)+3)for g in [15,17,20]],profiles=profiles,packs=rows,sensitivity=sens,thermal=thermal,passive_filters=filters,passive_filter_power_basis=dict(normal9_available_input_w=cap*loss,source7_available_input_w=1,scope='CW capability stress calculation, not AM mean or measured RF current'),driver_fault_rc=rc,assumptions=dict(aging=.8,endpoint_energy=.9,temperature=.9,cell_min_wh=cells,controller_w=.14,rf_idle_w={'BOOST2S':.03,'BUCK4S':.04},active_gate_sense_allowance_w=.10,driver_typ_a=.2341,front_boost_eff=.87,front_buck_eff=.91,driver_buck_eff=.90,series_input_ohm=.15,competition_duty=.20,full_4s_window=.60,lora_intermittent_w=.006,lora_rx_w=.045,lora_burst_extra_w=.44*.08/60),audio_filter=dict(f0_hz=1/(2*math.pi*10000*4.7e-9),q=.5,gain800=1/(1+(800*2*math.pi*10000*4.7e-9)**2),pwm312k_atten_db=20*math.log10(1/(1+(312500*2*math.pi*10000*4.7e-9)**2))))
s11=cmath.rect(.803,math.radians(-162));s21=cmath.rect(5.19,math.radians(67));s12=cmath.rect(.032,math.radians(-18));s22=cmath.rect(.704,math.radians(-157));delta=s11*s22-s12*s21
zin=50*(1+s11)/(1-s11);zout=50*(1+s22)/(1-s22);w=2*math.pi*144.7e6
rin=zin.real+1;xx=math.sqrt(rin*(50-rin));zexternal=1/(1/10-1j*w*38e-12);xo=math.sqrt(zexternal.real*(50-zexternal.real))
calc['matching_calculation']=dict(classification='Small-signal/calculated starting network, not optimal144MHz large-signal match',zin_150=[zin.real,zin.imag],zout_150=[zout.real,zout.imag],k=(1-abs(s11)**2-abs(s22)**2+abs(delta)**2)/(2*abs(s12*s21)),delta_abs=abs(delta),msg_db=10*math.log10(abs(s21/s12)),input_l_nh=(xx-zin.imag)/w*1e9,input_c_pf=xx/(50*rin)/w*1e12,output_target_ohm=10,output_coss_pf=38,output_knee_assumption_v=.8,output_l_nh=(xo+zexternal.imag)/w*1e9,output_c_pf=xo/(50*zexternal.real)/w*1e12)
(D/'calculations.json').write_text(json.dumps(calc,indent=2)+'\n')
with (D/'endurance.csv').open('w')as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
with(A/'ideal_filter.csv').open('w')as f:
 w=csv.writer(f);w.writerow(['filter','q_assumed','frequency_hz','insertion_db','max_vrms','max_L_current_rms'])
 for name,rr in filters.items():
  for j,x in enumerate(rr):w.writerow([name,[40,80,1000][j//7],x['f_hz'],x['s21_db'],max(x['volts_rms']),max(x['inductor_current_rms'])])
print('CALCULATED',len(rows),'pack/profile rows;',len(sens),'sensitivity cases; no measured endurance')
for x in profiles:
 if x['m']==.8:print(x['arch'],x['erp_carrier'],round(x['average_battery_w'],3),'W average; TX',round(x['tx_battery_w'],2),'pass',round(x['pass_mean_w'],2))
