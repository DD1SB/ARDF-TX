#!/usr/bin/python3
"""Finite-volume copper sheets, distributed ordinary via barrels and perforated TIM.

No solder-fill, FR4, plastic-top or air-conduction credit. Source is isothermal
over the mask opening (an approximation, not proof of partial solder wetting).
Via conduction is distributed around the hole circumference instead of a
mesh-dependent point contact. Hole areas reduce sheet/TIM conductance. Actual
die heat flux, localized voids and Cu/via transitions remain unvalidated.
"""
import math,csv,itertools,json
from m5b_e4r1_common import *
import m5b_e4_common as old

def geometry(name='selected'):
 if name=='E4':return dict(vias=[(x,y,.5 if i>=50 else .3,1.1 if i>=50 else .8,'joint'if i<40 else'other')for i,(x,y)in enumerate(old.VIAS)],rects=old.TOP_RECTS,source=SOURCE)
 if name=='A_ST18':inside=[(111.15+.85*c,53+.8*r,.3,.8,'joint')for c in range(3)for r in range(6)]
 elif name=='B_outside_only':inside=[]
 elif name=='C_open40':inside=[(x,y,.3,.8,'joint')for x,y in old.INNER]
 else:inside=[v for v in via_specs()if v[-1]=='joint']
 tail=[v for v in via_specs()if v[-1]!='joint']
 # A is a direct18-via reduction, keeping E4 external copper/vias unchanged.
 if name in['A_ST18','C_open40']:tail=[(x,y,.3,.8,'near')for x,y in old.NEAR]+[(x,y,.5,1.1,'wing')for x,y in old.OUTER]
 return dict(vias=inside+tail,rects=old.TOP_RECTS if name in['A_ST18','C_open40']else TOP_RECTS,source=SOURCE if name in['A_ST18','C_open40']else SOLDER)

def solve(plate=10,cu=30,tim_mm=.15,tim_k=6,step=.2,loss=4,layout='selected',contact_fraction=1.,thickness=1.6,contact=True):
 gg=geometry(layout);spec=gg['vias'];rects=gg['rects'];source=gg['source'];x0,y0,x1,y1=WINDOW;nx=round((x1-x0)/step);ny=round((y1-y0)/step)
 nodes={};xy=[];diag=[];rhs=[];fixed=set();edges=[];fractions={}
 def inside(x,y,r):return r[0]-1e-8<=x<=r[2]+1e-8 and r[1]-1e-8<=y<=r[3]+1e-8
 # Fractional cell area;16 subcells resolve hole area without crediting solder fill.
 for x,y,d,w,kind in spec:
  for j in range(max(0,int((y-d/2-y0)/step)-1),min(ny,int((y+d/2-y0)/step)+2)):
   for i in range(max(0,int((x-d/2-x0)/step)-1),min(nx,int((x+d/2-x0)/step)+2)):
    removed=sum((x0+(i+(a+.5)/4)*step-x)**2+(y0+(j+(b+.5)/4)*step-y)**2<(d/2)**2 for a in range(4)for b in range(4))/16
    fractions[i,j]=min(1.,fractions.get((i,j),0.)+removed)
 for side in[0,1]:
  for j in range(ny):
   for i in range(nx):
    x=x0+(i+.5)*step;y=y0+(j+.5)*step;frac=1-fractions.get((i,j),0.)
    if frac<=0 or side==0 and not any(inside(x,y,r)for r in rects):continue
    a=len(xy);nodes[side,i,j]=a;xy.append((x,y));diag.append(0.);rhs.append(0.)
    if side==0 and inside(x,y,source):fixed.add(a)
 def edge(a,b,g):
  if a==b or a in fixed and b in fixed:return
  if a in fixed:a,b=b,a
  if b in fixed:diag[a]+=g;rhs[a]+=g
  else:diag[a]+=g;diag[b]+=g;edges.append((a,b,g))
 sheet=385*cu*1e-6
 for (side,i,j),a in nodes.items():
  fa=1-fractions.get((i,j),0.)
  for key in[(side,i+1,j),(side,i,j+1)]:
   if key in nodes:
    fb=1-fractions.get(key[1:],0.);edge(a,nodes[key],sheet*2*fa*fb/(fa+fb))
  if side==1 and contact:diag[a]+=tim_k*(step*.001)**2/(tim_mm*.001)*fa*contact_fraction
 # Uniformly spread imperfect-via loss over the source field, not a helpful edge.
 joints=[i for i,v in enumerate(spec)if v[-1]=='joint'];lost=set(joints[round(i*(len(joints)-1)/max(1,loss-1))]for i in range(min(loss,len(joints))))
 for idx,(x,y,d,w,kind)in enumerate(spec):
  if idx in lost:continue
  weights={}
  for a in range(64):
   angle=2*math.pi*(a+.5)/64;xx=x+(d/2+.035)*math.cos(angle);yy=y+(d/2+.035)*math.sin(angle)
   i=int((xx-x0)/step);j=int((yy-y0)/step)
   # Select nearest remaining sheet cell if sample lands in a cut-out cell.
   candidates=[(di,dj)for di in range(i-1,i+2)for dj in range(j-1,j+2)if(0,di,dj)in nodes and(1,di,dj)in nodes]
   assert candidates,('via outside source copper',x,y)
   i,j=min(candidates,key=lambda q:(x0+(q[0]+.5)*step-xx)**2+(y0+(q[1]+.5)*step-yy)**2);weights[i,j]=weights.get((i,j),0)+1/64
  g=385*math.pi*d*.001*plate*1e-6/(thickness*.001)
  for (i,j),weight in weights.items():edge(nodes[0,i,j],nodes[1,i,j],g*weight)
 if not contact:return math.inf,dict(reason='no thermal contact')
 for a in fixed:diag[a]=1;rhs[a]=0
 def mv(v):
  z=[d*t for d,t in zip(diag,v)]
  for a,b,g in edges:z[a]-=g*v[b];z[b]-=g*v[a]
  return z
 dot=lambda a,b:sum(x*y for x,y in zip(a,b))
 v=[0.]*len(diag);r=rhs[:];z=[a/b for a,b in zip(r,diag)];d=z[:];rz=dot(r,z);norm=dot(rhs,rhs)
 for iteration in range(3500):
  ad=mv(d);alpha=rz/dot(d,ad);v=[a+alpha*b for a,b in zip(v,d)];r=[a-alpha*b for a,b in zip(r,ad)]
  if dot(r,r)<norm*1e-17:break
  z=[a/b for a,b in zip(r,diag)];rz1=dot(r,z);beta=rz1/rz;d=[a+beta*b for a,b in zip(z,d)];rz=rz1
 else:raise AssertionError('thermal solver failed convergence')
 heat=sum(v[a]*tim_k*(step*.001)**2/(tim_mm*.001)*(1-fractions.get((i,j),0.))*contact_fraction for(side,i,j),a in nodes.items()if side==1)
 return 1/heat,dict(nodes=len(nodes),iterations=iteration+1,relative_residual=math.sqrt(dot(r,r)/norm),grid_mm=step)

def main():
 guard();cases={};rows=[]
 boundary=[('nominal',35,.05,10,.25,.25,2.2,0,1.),('conservative',30,.15,6,1.,.7,4.,4,1.),('poor_joint',30,.25,5,1.5,.7,5.5,8,.7)]
 for name,cu,tm,tk,joint,bar,sink,loss,contact in boundary:
  cases[name]={}
  for plate in[10,15,18,25]:
   rr,meta=solve(plate=plate,cu=cu,tim_mm=tm,tim_k=tk,loss=loss,contact_fraction=contact);mesh=1.;total=3+joint+rr+bar+sink+mesh
   cases[name][str(plate)]=dict(source_to_bar_K_W=rr,total_JA_K_W=total,junction_40C_4W_C=40+4*total,solver=meta,Cu_um=cu,TIM_mm=tm,TIM_k_W_mK=tk,joint_K_W=joint,bar_and_second_interface_K_W=bar,sink_K_W=sink,missing_inner_vias=loss,TIM_contact_fraction=contact,mesh_allowance_K_W=mesh)
   print(name,plate,round(rr,3),round(40+4*total,2),flush=True)
   for ambient,heat in itertools.product([25,40],[2,3,4,5]):rows.append(dict(case=name,barrel_um=plate,ambient_C=ambient,heat_W=heat,total_JA_K_W=total,junction_C=ambient+heat*total,physical='NOT_RUN'))
 comparison={}
 for layout in['E4','A_ST18','B_outside_only','C_open40','selected']:
  r,m=solve(layout=layout);comparison[layout]=dict(geometry=geometry(layout),source_to_bar_K_W=r,total_JA_K_W=3+1+r+.7+4+1,junction_40C_4W_C=40+4*(3+1+r+.7+4+1),solver=m)
 conv=[]
 for layout in['E4','selected']:
  for step in[.4,.2,.1,.05]:
   r,m=solve(layout=layout,step=step);conv.append(dict(layout=layout,source_to_bar_K_W=r,**m));print('mesh',layout,step,round(r,5),flush=True)
 sensitivities=[]
 for name,kw,joint,sink in [('board_upper_thickness',dict(thickness=1.76),1,4),('30percent_contact_loss',dict(contact_fraction=.7),1,4),('half_contact',dict(contact_fraction=.5),1,4),('eight_joint_vias_lost',dict(loss=8),1,4),('source_joint_50percent_effective',{},2,4),('horizontal_or_restricted_convection',{},1,5.5),('improved_ordinary_grease_film',dict(tim_mm=.075,tim_k=6),1,4),('combined_thickness_contact_and_joint',dict(thickness=1.76,contact_fraction=.7),2,4)]:
  r,m=solve(**kw);sensitivities.append(dict(case=name,inputs=kw,joint_K_W=joint,sink_K_W=sink,source_to_bar_K_W=r,junction_40C_4W_C=40+4*(3+joint+r+.7+sink+1),solver=m))
 joint_sweep=[dict(effective_wet_area_mm2=a,joint_thickness_mm=t,solder_k_W_mK=k,one_dimensional_joint_K_W=1000*t/(k*a),limitation='No void-location/contact/spreading guarantee')for a,t,k in itertools.product([2,4,6,8],[.025,.05,.1],[25,50])]
 save('thermal-model.json',dict(status='CALCULATED_CONDITIONAL_PHYSICAL_GATE_OPEN',native_input_SHA256=sha(HW/'RF2M.kicad_pcb'),geometry_input_SHA256=sha(ROOT/'tools/m5b_e4r1_common.py'),solver_input_SHA256=sha(Path(__file__)),method=__doc__,cases=cases,convergence=conv,sensitivities=sensitivities,source_joint_area_sweep=joint_sweep,comparison_same_new_model_and_boundary=comparison,historical_E4=json.loads((HW/'review/M5B-E4/thermal-model.json').read_text())['cases'],physical='NOT_RUN',numerical_allowance_K_W=1.,limitations=['Joint resistance and wetting NOT measured;1K/W is an acceptance assumption, not a guaranteed joint','Isothermal source and homogeneous Cu cannot bound localized void hot spots','No solder fill credited; barrel10um is a sensitivity, not a guaranteed JLC minimum','Circumferential via coupling, perforated sheet approximation and mesh extrapolation are not validated FEM','Sink natural convection depends on orientation and enclosure. No closed enclosure performance claimed']))
 with(OUT/'thermal-sensitivity.csv').open('w')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 save('source-construction-comparison.json',dict(status='CALCULATED_NOT_MEASURED',thermal=comparison,selection='selected',criteria='See SOURCE_JOINT documentation;thermal calculation alone does not establish joint reliability',physical='NOT_RUN'))
if __name__=='__main__':main()
