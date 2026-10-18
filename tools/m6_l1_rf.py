#!/usr/bin/python3
"""Native RF cross sections + conformal-map/ABCD calculations, not EM measurements."""
import sys,json,math,cmath,itertools,hashlib,csv
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-L1'
def save(n,x):(D/n).write_text(json.dumps(x,indent=2)+'\n')
def mm(v):return p.ToMM(v)
def pt(x,y):return p.VECTOR2I(p.FromMM(x),p.FromMM(y))
def polygon(o,l):
 q=p.SHAPE_POLY_SET();o.TransformShapeToPolygon(q,l,0,p.FromMM(.001),p.ERROR_OUTSIDE);return q

def extract(b):
 f={x.GetReference():x for x in b.GetFootprints()};sig=[polygon(a,p.F_Cu) for r in ['U70','J7'] for a in f[r].Pads() if a.GetNetname()=='LORA_ANT'];tracks=[x for x in b.GetTracks() if x.GetNetname()=='LORA_ANT'];sig += [polygon(x,p.F_Cu) for x in tracks]
 g={l:[z.GetFilledPolysList(l) for z in b.Zones() if not z.GetIsRuleArea() and z.GetNetname()=='GND' and z.IsOnLayer(l)] for l in [p.F_Cu,p.B_Cu]}
 def has(sh,x,y):return any(s.Contains(pt(x,y)) for s in sh)
 rows=[];N=105;dx=.005
 for i in range(N):
  y=28.5+(i+.5)*5.25/N;x=97.89;edges=[];gaps=[]
  for side in [-1,1]:
   edge=next((n*dx for n in range(1,401) if not has(sig,x+side*n*dx,y)),None)
   if edge is None:raise ValueError('RF signal width extraction failed')
   gap=next((n*dx for n in range(1001) if has(g[p.F_Cu],x+side*(edge+n*dx),y)),None)
   edges.append(edge-dx/2);gaps.append(gap)
  rows.append(dict(y_mm=y,dy_mm=5.25/N,width_mm=sum(edges),left_gap_mm=gaps[0],right_gap_mm=gaps[1],bottom_ground=all(has(g[p.B_Cu],x+d,y) for d in [-1,-.5,0,.5,1])))
 vias=[dict(x_mm=mm(t.GetPosition().x),y_mm=mm(t.GetPosition().y),land_mm=mm(t.GetWidth(p.F_Cu)),drill_mm=mm(t.GetDrillValue())) for t in b.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND' and 94<mm(t.GetPosition().x)<102 and 26<mm(t.GetPosition().y)<36]
 return dict(classification='Actual native filled-copper sampling,5um transverse/50um longitudinal resolution',track_records=[dict(start_mm=[mm(t.GetStart().x),mm(t.GetStart().y)],end_mm=[mm(t.GetEnd().x),mm(t.GetEnd().y)],width_mm=mm(t.GetWidth()),layer=b.GetLayerName(t.GetLayer())) for t in tracks],sections=rows,local_ground_vias=vias)

def K(k):
 a=1.;b=math.sqrt(1-k*k)
 for _ in range(50):
  aa=(a+b)/2;b=math.sqrt(a*b);a=aa
  if abs(a-b)<1e-14:break
 return math.pi/(2*a)
def R(k):return K(k)/K(math.sqrt(1-k*k))
def cpw(w,g,h,er,t):
 # Qucs12.10..13; first-order thickness widening12.14..17.
 delta=1.25*t/math.pi*(1+math.log(4*math.pi*w/t));we=w+delta;ge=g-delta
 if ge<=0:raise ValueError('thickness model outside applicability')
 a=R(we/(we+2*ge));b=R(math.tanh(math.pi*we/(4*h))/math.tanh(math.pi*(we+2*ge)/(4*h)))
 ee=1+(er-1)*b/(a+b);return 60*math.pi/(math.sqrt(ee)*(a+b)),ee

def micro(w,h,er,t):
 # Hammerstad/Wheeler quasi-static narrow-line comparison, not installed topology.
 u=(w+t/math.pi*(1+math.log(4*math.pi*w/t)))/h
 ee=(er+1)/2+(er-1)/2*(1/math.sqrt(1+12/u)+(.04*(1-u)**2 if u<1 else 0))
 z=60/math.sqrt(ee)*math.log(8/u+u/4) if u<=1 else 120*math.pi/(math.sqrt(ee)*(u+1.393+.667*math.log(u+1.444)))
 return z,ee

def mul(a,b):return (a[0]*b[0]+a[1]*b[2],a[0]*b[1]+a[1]*b[3],a[2]*b[0]+a[3]*b[2],a[2]*b[1]+a[3]*b[3])
def line(z,ee,length,f,tan=.02,w=.45,rough=2):
 beta=2*math.pi*f/299792458*math.sqrt(ee);rs=math.sqrt(math.pi*f*4e-7*math.pi*1.724e-8)
 # Total signal/return sheet-loss allowance; explicit roughness sensitivity.
 ac=rs*rough/(z*w*.001);ad=beta*tan/2;g=complex(ac+ad,beta)*length*.001
 return (cmath.cosh(g),z*cmath.sinh(g),cmath.sinh(g)/z,cmath.cosh(g)),(ac+ad)*length*.001*8.6858896

def S(a):
 A,B,C,E=a;den=A+B/50+C*50+E;s11=(A+B/50-C*50-E)/den;s21=2/den
 return dict(S11_abs=abs(s11),return_loss_dB=-20*math.log10(max(abs(s11),1e-15)),insertion_loss_dB=-20*math.log10(abs(s21)))

def model(rows,f,h=1.53,er=4.5,t=.035,etch=0,mask=0,tand=.02,rough=2,transition_L_nH=0,transition_C_pF=0,kind='coplanar',gap_error=0):
 if h<1.3 or h>1.8 or not 3.8<=er<=5.2 or t<.025 or t>.05:raise ValueError('unsupported standard-FR4 model input')
 a=(1,0,0,1);zs=[];ees=[];delay=0;loss=0
 for row in rows:
  w=row['width_mm']*(1+etch);g=max(row['left_gap_mm'],row['right_gap_mm'])-row['width_mm']*etch/2+gap_error # larger gap brackets launch asymmetry
  z,ee=(cpw(w,g,h,er,t) if kind=='coplanar' else micro(w,h,er,t))
  # Solder-mask uncertainty represented as an explicit effective-er increment.
  z*=math.sqrt(ee/(ee+mask));ee+=mask
  q,l=line(z,ee,row['dy_mm'],f,tand,w,rough);a=mul(a,q);loss+=l;zs.append(z);ees.append(ee);delay+=row['dy_mm']*.001*math.sqrt(ee)/299792458
 omega=2*math.pi*f;l=transition_L_nH*1e-9;c=transition_C_pF*1e-12
 tr=mul((1,1j*omega*l,0,1),(1,0,1j*omega*c,1));a=mul(mul(tr,a),tr)
 return dict(frequency_Hz=f,**S(a),local_Z_range_ohm=[min(zs),max(zs)],mean_Z_ohm=sum(zs)/len(zs),effective_er_range=[min(ees),max(ees)],delay_ps=delay*1e12,electrical_length_deg=360*f*delay,distributed_loss_dB=loss,transition_L_nH_each=l*1e9,transition_C_pF_each=c*1e12)

def main():
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));a=extract(b);assert all(x['bottom_ground'] for x in a['sections']);a['native_sha256']=hashlib.sha256((P/'CTRL.kicad_pcb').read_bytes()).hexdigest();save('antenna-native-geometry.json',a)
 with (D/'RF-cross-sections.csv').open('w') as f:w=csv.DictWriter(f,fieldnames=list(a['sections'][0]),lineterminator='\n');w.writeheader();w.writerows(a['sections'])
 rows=a['sections'];nom=[model(rows,f,mask=.10) for f in [433e6,868e6]];corners=[]
 for f,h,er,t,etch,gaperror,mask,tand,kind in itertools.product([433e6,868e6],[1.37,1.69],[4.0,5.0],[.03,.045],[-.20,.20],[-.05,.05],[0,.25],[.015,.03],['coplanar','microstrip']):
  r=model(rows,f,h,er,t,etch,mask,tand,3,kind=kind,gap_error=gaperror);r['inputs']=dict(h_mm=h,er=er,t_mm=t,etch_width_fraction=etch,gap_error_mm=gaperror,mask_delta_ee=mask,tand=tand,kind=kind);corners.append(r)
 transitions=[model(rows,f,mask=.10,transition_L_nH=l,transition_C_pF=c) for f,l,c in itertools.product([433e6,868e6],[0,.5,1.5],[0,.15,.35])]
 summary={str(int(f)):{'line_only_return_loss_min_dB':min(x['return_loss_dB'] for x in corners if x['frequency_Hz']==f),'line_only_insertion_loss_max_dB':max(x['insertion_loss_dB'] for x in corners if x['frequency_Hz']==f),'transition_sensitivity_return_loss_min_dB':min(x['return_loss_dB'] for x in transitions if x['frequency_Hz']==f)} for f in [433e6,868e6]}
 save('RF-analysis.json',dict(classification='CALCULATED quasi-static partial-geometry brackets; NOT S11 measurement/3D EM qualification',method_url='https://qucs.github.io/tech/node86.html',reference_planes='U70 terminal21 carrier solder-land centre -> J7 signal solder-land centre. Series-L/shunt-C sensitivities represent unresolved castellation/U.FL-to-cable transitions; physical cable reference planes require calibration.',nominal=nom,summary=summary,corners=corners,transition_sensitivities=transitions,limitations=['No guaranteed material-er/solder-mask RF bounds from standard order; ranges are engineering sensitivities','GCPW formula assumes infinite equipotential top grounds; larger local gap used for asymmetric U.FL launch','Microstrip comparison removes coplanar loading, not a prediction that actual top ground is absent','Ground-via/finite-plane inductance, actual module S11 and connector contact parasitics are unresolved; transition values are assumptions, not guaranteed bounds','HASL roughness and mask modeled by explicit allowances, not measured','No module RF compliance or legal permission implied']))
 print('RF nominal',nom,'sensitivity',summary)
if __name__=='__main__':main()
