#!/usr/bin/python3
"""Two copper-sheet resistor network. No FR4/solder-fill/air credit.

Finite volumes solve -div(k*t*grad(T)) + g_TIM*T + via couplings = Q.
Source land is isothermal at 1 K; conductance gives source-to-bar R.
Explicit solder, bar/interface and sink terms are then added in SERIES.
No second spreading term is added to the solved copper/TIM path.
Only Python standard library is required; native geometry checked separately.
"""
import math,json,csv,itertools
from m5b_e4_common import *

def solve(plate=10,cu=30,tim_mm=.15,tim_k=6,step=.2,inner_loss=0,external=True,contact=True):
 x0,y0,x1,y1=WINDOW if external else(105,49,119,61);nx=round((x1-x0)/step);ny=round((y1-y0)/step)
 nodes={};xy=[];fixed=set();diag=[];rhs=[];edges=[]
 def inside(x,y,rect):return rect[0]-1e-8<=x<=rect[2]+1e-8 and rect[1]-1e-8<=y<=rect[3]+1e-8
 for side in [0,1]:
  for j in range(ny):
   for i in range(nx):
    x=x0+(i+.5)*step;y=y0+(j+.5)*step
    if side==0 and not any(inside(x,y,r)for r in (TOP_RECTS if external else [(110.65,52.5,113.35,57.5)])):continue
    key=(side,i,j);nodes[key]=len(xy);xy.append((x,y));diag.append(0.);rhs.append(0.)
    if side==0 and inside(x,y,(110.65,52.5,113.35,57.5)):fixed.add(nodes[key])
 def edge(a,b,g):
  if a==b:return
  if a in fixed and b in fixed:return
  if a in fixed:a,b=b,a
  if b in fixed:diag[a]+=g;rhs[a]+=g
  else:diag[a]+=g;diag[b]+=g;edges.append((a,b,g))
 sheet=385*cu*1e-6
 for (side,i,j),a in nodes.items():
  for key in [(side,i+1,j),(side,i,j+1)]:
   if key in nodes:edge(a,nodes[key],sheet)
  if side==1 and contact:diag[a]+=tim_k*(step*.001)**2/(tim_mm*.001)
 lost=set(range(inner_loss))
 oldinner=[(111.1+.6*c,52.9+.6*r)for c in range(4)for r in range(8)]
 for idx,(x,y)in enumerate(VIAS if external else oldinner):
  if idx in lost:continue
  i=min(nx-1,max(0,int((x-x0)/step)));j=min(ny-1,max(0,int((y-y0)/step)))
  assert(0,i,j)in nodes,('via outside top copper',x,y)
  drill=.5 if idx>=len(INNER)+len(NEAR) else .3
  via_g=385*math.pi*drill*.001*plate*1e-6/.0016
  edge(nodes[0,i,j],nodes[1,i,j],via_g)
 # Diagonal-preconditioned conjugate gradient on sparse symmetric graph.
 for a in fixed:diag[a]=1;rhs[a]=0
 if not contact:return math.inf,dict(nodes=len(nodes),reason='No sink contact')
 def mv(v):
  z=[d*t for d,t in zip(diag,v)]
  for a,b,g in edges:z[a]-=g*v[b];z[b]-=g*v[a]
  return z
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))
 v=[0.]*len(diag);r=rhs[:];z=[a/b for a,b in zip(r,diag)];d=z[:];rz=dot(r,z);norm=dot(rhs,rhs)
 for iteration in range(2500):
  ad=mv(d);alpha=rz/dot(d,ad);v=[a+alpha*b for a,b in zip(v,d)];r=[a-alpha*b for a,b in zip(r,ad)]
  if dot(r,r)<norm*1e-17:break
  z=[a/b for a,b in zip(r,diag)];rz1=dot(r,z);beta=rz1/rz;d=[a+beta*b for a,b in zip(z,d)];rz=rz1
 else:raise AssertionError('thermal solver convergence')
 gtotal=sum(v[a]*tim_k*(step*.001)**2/(tim_mm*.001)for (side,i,j),a in nodes.items()if side==1)
 return 1/gtotal,dict(nodes=len(diag),iterations=iteration+1,relative_residual=math.sqrt(dot(r,r)/norm),grid_mm=step)

def main():
 guard();rows=[];cases={}
 for name,cu,tm,tk,solder,bar,sink,loss in [('nominal',35,.05,10,.25,.25,2.2,0),('conservative',30,.15,6,1.,.7,4.,4),('poor_joint',30,.25,5,1.5,.7,5.5,8)]:
  cases[name]={}
  for plate in [10,15,18,25]:
   rr,meta=solve(plate,cu,tm,tk,inner_loss=loss);mesh=.6 if name!='nominal'else 0.;total=3+solder+rr+bar+sink+mesh;cases[name][str(plate)]=dict(source_to_bar_K_W=rr,total_JA_K_W=total,junction_40C_4W_C=40+4*total,solver=meta,Cu_um=cu,TIM_mm=tm,TIM_k_W_mK=tk,joint_K_W=solder,bar_and_second_interface_K_W=bar,sink_K_W=sink,missing_inner_vias=loss,mesh_allowance_K_W=mesh)
   for ambient,heat in itertools.product([25,40],[2,3,4,5]):rows.append(dict(case=name,barrel_um=plate,ambient_C=ambient,heat_W=heat,total_JA_K_W=total,junction_C=ambient+heat*total,physical='NOT_RUN'))
 conv=[]
 for h in [.4,.2,.1,.05]:
  rr,meta=solve(step=h,inner_loss=4);conv.append(dict(source_to_bar_K_W=rr,**meta))
 old=13.779648752545052
 a,ameta=solve(plate=10,cu=30,tim_mm=.15,tim_k=6,inner_loss=4,external=False)
 save('cooling-architecture-comparison.json',dict(status='CALCULATED_NOT_MEASURED',A_unchanged_E3_vias_with_same_new_grease_bar_and_sink=dict(source_to_bar_K_W=a,total_JA_K_W=3+1+a+.7+4+.6,junction_at40C_4W_C=40+4*(3+1+a+.7+4+.6),solver=ameta),B_implemented_wings_and_more_vias=cases['conservative']['10'],C_solder_filled_vias=dict(selected=False,solder_volume32_holes_mm3=32*math.pi*.15**2*1.6,reason='No reliable fill/void bound; no credited solder-fill conduction. Ordinary manual assembly must not be treated as factory plugged/capped vias.'),top_package_contact=dict(selected=False,reason='No qualified plastic-top Rjc path. No unsupported package force or altered under-pad metal bridge.')))
 save('thermal-model.json',dict(status='CALCULATED_NOT_PHYSICALLY_QUALIFIED',method=__doc__,cases=cases,convergence=conv,E3_10um_40C_4W_C=40+4*(3+old+2+1+3.5),E3_18um_40C_4W_C=40+4*(3+old*10/18+2+1+3.5),all_hardware_tests='NOT_RUN',limitations=['Copper sheets homogeneous; omitted board FR4/air paths cannot improve claimed bound','Source land is isothermal: real die/solder heat spreading and localized voids remain unknown','Via-to-sheet transitions discretized; mesh sensitivity is reported, not calibrated against hardware','Sink catalogue rating depends on orientation, temperature rise and unrestricted airflow; enclosure not qualified','Grease bond line, bar flatness and surviving solder joint are assembly acceptance conditions, not guaranteed manufacturing specifications']))
 with(OUT/'thermal-sensitivity.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 print(json.dumps(cases,indent=2));print('convergence',conv)
if __name__=='__main__':main()
