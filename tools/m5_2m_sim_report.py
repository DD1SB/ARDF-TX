#!/usr/bin/python3
import math,json,bisect
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'analysis/m5_2m';r=[list(map(float,x.split()))for x in(D/'am_loop_behavioral.dat').read_text().splitlines()];t=[x[0]for x in r];n=16000;dt=.01/n;ys=[]
for k in range(n):
 tt=.020+k*dt;j=max(1,min(len(r)-1,bisect.bisect_left(t,tt)));a,b=r[j-1],r[j];ys.append(a[3]+(b[3]-a[3])*(tt-a[0])/(b[0]-a[0]))
amp=[]
for h in range(1,9):amp.append(2/n*abs(sum(y*complex(math.cos(2*math.pi*800*h*k*dt),-math.sin(2*math.pi*800*h*k*dt))for k,y in enumerate(ys))))
x=dict(classification='SIMULATION ideal one-pole opamp/transconductance plant, not vendor semiconductor model or hardware',mean_v=sum(ys)/n,min_v=min(ys),max_v=max(ys),depth=(max(ys)-min(ys))/(max(ys)+min(ys)),fundamental=amp[0],thd_h2_h8=math.sqrt(sum(a*a for a in amp[1:]))/amp[0],ngspice='42',plant_pass_beta_assumption=50,driver_gm_a_per_v=6.1,limitations=['No RF/nonlinear PD model','No BJT capacitance, beta rolloff, hot SOA or stored charge','No actual opamp output/load stability model','No analog startup/fault proof'])
(R/'hardware/2m/review/M5A-R0/am-loop-result.json').write_text(json.dumps(x,indent=2)+'\n');print(json.dumps(x,indent=2))
