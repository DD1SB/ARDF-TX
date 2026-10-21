#!/usr/bin/env python3
"""Reproducible linear RF, loss and energy estimates. No hardware claims.

Coilcraft Doc158 topology: R2 + [(k sqrt(f)+jωL) || (R1+1/jωC)].
Manufacturer model parameters are numerical facts; PDFs remain outside MIT tree.
"""
import cmath,csv,itertools,json,math,random
from pathlib import Path
P=Path(__file__).resolve().parents[1];OUT=P/'analysis'
# R1 ohm, R2 ohm, C pF, L uH, skin k. Manufacturer Doc158.
MODELS={'1008-102':(150,.62,.21,1,.0007),'1008-332':(261,1.4,.309,3.3,.00145),'1008-222':(384,1.1,.168,2.2,.00094),'1008-103':(300,2.9,.385,10,.00389),'1008-472':(273,1.6,.285,4.7,.00179),'1812-333':(354,4,.47,33,.00973),'1812-153':(292,2,.26,15,.00653)}
def coil(name,f,scale=1):
 r1,r2,c,l,k=MODELS[name];w=2*math.pi*f;a=k*math.sqrt(f)+1j*w*l*1e-6*scale;b=r1+1/(1j*w*c*1e-12)
 return r2+1/(1/a+1/b)
def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def series(z):return (1,z,0,1)
def shunt(y):return (1,0,y,1)
def network(f,tol=None):
 w=2*math.pi*f;t=tol or [1]*7;a=series(1/(1j*w*10e-9))
 for i,name in enumerate(['1008-102','1008-332','1008-332','1008-102']):
  a=mul(a,series(coil(name,f,t[2*i])))
  if i<3:a=mul(a,shunt(1j*w*[1200e-12,1000e-12,820e-12][i]*t[2*i+1]))
 return a
def power(f,ballast=100,ron=30,load=50,tol=None,rail=4.95):
 a,b,c,d=network(f,tol);rs=(ballast+ron)/8;voc=rail*math.sqrt(2)/math.pi
 v=voc/(a+b/load+rs*(c+d/load));return abs(v)**2/load
def s21(f):
 a,b,c,d=network(f);return 20*math.log10(abs(2/(a+b/50+c*50+d)))
def transfer(f,rs=16.25,load=50):
 a,b,c,d=network(f);return 1/(a+b/load+rs*(c+d/load))
def main():
 OUT.mkdir(exist_ok=True);f=3550000;results={'status':'CALCULATED CANDIDATE / NOT MEASURED','model_sources':{'1008':'https://www.coilcraft.com/getmedia/7d978b1b-134f-445c-9d2b-c682ece55405/spice_1008ls.pdf','1812':'https://www.coilcraft.com/pdfs/spice_1812ls.pdf'},'coil_impedance_3p55MHz':{k:{'R_ohm':coil(k,f).real,'X_ohm':coil(k,f).imag,'Q_model':coil(k,f).imag/coil(k,f).real} for k in MODELS}}
 results['nominal_mW']={k:1000*power(f,r) for k,r in [('MINI50',100),('FOX10',560)]}
 results['load_sweep_mW']=[{'ohm':r,'MINI50':1000*power(f,100,30,r),'FOX10':1000*power(f,560,30,r)}for r in [25,50,100,150,200]]
 results['harmonics']=[{'harmonic':n,'filter_50ohm_S21_dB':s21(n*f),'actual_source_transfer_relative_dB':20*math.log10(abs(transfer(n*f)/transfer(f))),'ideal_square_relative_dBc':None if n%2==0 else 20*math.log10(abs(transfer(n*f)/transfer(f))/n)}for n in range(1,8)]
 results['duty_error_second_harmonic_dBc']=20*math.log10(abs(transfer(2*f)/transfer(f))*abs(math.sin(2*math.pi*.45)/(2*math.sin(math.pi*.45))))
 losses={}
 for name,ballast in [('MINI50',100),('FOX10',560)]:
  a,b,c,d=network(f);vo=4.95*math.sqrt(2)/math.pi*transfer(f,(ballast+30)/8);io=vo/50;ii=c*vo+d*io;vi=a*vo+b*io
  losses[name]={'load_mW':abs(vo)**2/50*1000,'source_fundamental_mArms':abs(ii)*1000,'per_output_fundamental_mArms':abs(ii)*1000/8,'ballast_total_mW':abs(ii)**2*ballast/8*1000,'ballast_per_resistor_mW':abs(ii)**2*ballast/64*1000,'assumed_driver_conduction_mW':abs(ii)**2*30/8*1000,'filter_loss_mW':(vi*ii.conjugate()).real*1000-abs(vo)**2/50*1000,'output_Vrms':abs(vo),'PA_rail_budget_mW':4.95*(30 if name=='MINI50'else 20)}
 results['fundamental_losses']=losses
 # 5% L/C, 10-70 ohm per-output R_on (sizing assumptions, not guaranteed RF models).
 rng=random.Random(80);samples=[1000*power(rng.uniform(3510000,3600000),100,rng.uniform(10,70),tol=[rng.uniform(.95,1.05)for _ in range(7)],rail=rng.uniform(4.8,5.2))for _ in range(2000)]
 results['monte_carlo_MINI50_mW']={'minimum':min(samples),'median':sorted(samples)[1000],'maximum':max(samples),'draws':2000,'meaning':'sensitivity study only, no production yield prediction'}
 # Antenna model: loading follows the optional 50->100 ohm L-match.
 loads=[]
 # First-order thin short monopole, image ground, triangular current. Ground
 # loss is an explicit scenario; this is not a NEC/site propagation solution.
 wire=[];wavelength=299792458/f
 for h in [6,7.5,9,.3]:
  capacitance=2*math.pi*8.8541878128e-12*h/(math.log(2*h/.0005)-1)*1e12
  radiation=40*math.pi**2*(h/wavelength)**2
  wire.append({'height_m':h,'wire_radius_mm':.5,'C_pF':capacitance,'radiation_R_ohm':radiation,'ground_loss_scenarios_ohm':[20,100],'limit':'short thin vertical against image ground; no real counterpoise, soil, feed or mutual coupling model'})
 results['thin_vertical_models']=wire
 scenarios=[(50,None),(100,33),(150,33),(100,50),(50,80),(100,3)]+[(x['radiation_R_ohm']+loss,x['C_pF'])for x in wire for loss in x['ground_loss_scenarios_ohm']]
 for resistance,cap in scenarios:
  candidates=[]
  for bits in itertools.product([0,1],repeat=4):
   w=2*math.pi*f;z=complex(resistance,0) if cap is None else resistance+1/(1j*w*cap*1e-12)
   z+=sum(coil(k,f) for k,v in zip(['1812-333','1008-103','1008-472','1812-153'],bits)if v)
   # Optional shunt 470p and series 2.2u transformer, both fitted together.
   z=1/(1/z+1j*w*470e-12)+coil('1008-222',f)
   gamma=(z-50)/(z+50);candidates.append((abs(gamma),bits,z))
  g,bits,z=min(candidates)
  # A 50ohm Thevenin source with 50mW available, for stress comparison only.
  iin=math.sqrt(4*.05*50)/(50+z);vmatch=iin*(z-coil('1008-222',f))
  za=complex(resistance,0)if cap is None else resistance+1/(1j*2*math.pi*f*cap*1e-12)
  names=[k for k,v in zip(['1812-333','1008-103','1008-472','1812-153'],bits)if v]
  ia=vmatch/(za+sum(coil(k,f)for k in names))
  loads.append({'R_ohm':resistance,'C_pF':cap,'bits_33_10_4p7_15':bits,'input_R':z.real,'input_X':z.imag,'return_loss_dB':-20*math.log10(g),'matched':g<.5,'antenna_current_mArms_at_50mW_available':abs(ia)*1000,'delivered_resistive_mW_at_50mW_available':abs(ia)**2*resistance*1000,'loading_coil_Vpeak':{k:abs(ia*coil(k,f))*math.sqrt(2)for k in names},'external_series_C_Vpeak':None if cap is None else abs(ia/(1j*2*math.pi*f*cap*1e-12))*math.sqrt(2)})
 results['antenna_candidates']=loads
 results['skew_bound']={'rail_max_V':5.2,'ballast_min_ohm':99,'worst_4_vs_4_ballast_only_mA':1000*5.2/(99/4+99/4),'note':'Worst skew current exceeds the 70mA DC package rating. Pulse behavior is unspecified. Measure switching currents and obtain manufacturer clarification before a populated fleet release; use conservative current limiting for first articles.'}
 # Budget includes 22mA clock while prepared, 0.2mA MCU overhead, 80% usable capacity.
 runtime=[]
 for name,prepared,key,current5 in [('slow/fast MINI50',.2084,.5,30),('S MINI50',1,.25,30),('MO MINI50',1,15/28,30),('FOX10',1,.5,20)]:
  current=.2+prepared*(22+key*4.95*current5/(.85*3.7))
  for cell in [150,300,560,1200,1500]:runtime.append({'mode':name,'cell_mAh':cell,'average_mA':current,'useful_hours':cell*.8/current})
 results['runtime']=runtime
 (OUT/'electrical-estimates.json').write_text(json.dumps(results,indent=2)+'\n')
 with (OUT/'filter-sweep.csv').open('w') as q:
  w=csv.writer(q);w.writerow(['frequency_Hz','S21_dB','MINI50_mW_50ohm','FOX10_mW_50ohm'])
  for f in range(1000000,30000001,25000):w.writerow([f,s21(f),power(f)*1000,power(f,560)*1000])
 print(json.dumps({k:results[k]for k in ['nominal_mW','monte_carlo_MINI50_mW','harmonics','antenna_candidates']},indent=2))
if __name__=='__main__':main()
