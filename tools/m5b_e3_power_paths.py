#!/usr/bin/python3
"""Actual copper-contact graph main-current paths;no assumed sense-branchload.
Each traversed track charged its FULL resistance,overboundingpartialcontacts.
Package/internalconductordropsareseparatefromPCB-coppermodel.
"""
import pcbnew as p,math,heapq,json,collections
from m5b_e3_common import *
from m5b_e3_dfm import nearby,bbox

def main():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));rho=1.724e-8*(1+.00393*60);rows=[];fs={f.GetReference():f for f in b.GetFootprints()};pairs=[('J301','1','F301','1'),('F301','2','Q309','3'),('Q309','2','Q305','2'),('Q305','3','L302','1'),('Q305','3','U301','3'),('U302','8','J302','1'),('L301','2','J302','3'),('J302','2','Q302','2'),('Q302','3','R309','1'),('R309','2','Q401','3'),('Q401','2','L635','1')]
 for r,n,s,k in pairs:
  a=next(q for q in fs[r].Pads()if q.GetNumber()==n);z=next(q for q in fs[s].Pads()if q.GetNumber()==k);net=a.GetNetname();assert net==z.GetNetname();objects=[];lookup={};cost={};details={}
  for ob in list(b.GetTracks())+[q for f in b.GetFootprints()for q in f.Pads()]:
   if ob.GetNetname()!=net:continue
   uid=ob.m_Uuid.AsString();via=isinstance(ob,p.PCB_VIA);track=isinstance(ob,p.PCB_TRACK)and not via
   if track:
    w=p.ToMM(ob.GetWidth());l=p.ToMM(ob.GetLength())
    if w<.5 and l>2:continue
    rr=rho*l*.001/(w*.001*35e-6);detail=dict(kind='track',uuid=uid,width_mm=w,length_mm=l,R_ohm=rr,layer=ob.GetLayerName())
   elif via:rr=rho*.0016/(math.pi*.0003*18e-6);detail=dict(kind='via',uuid=uid,R_ohm=rr)
   else:rr=0;detail=dict(kind='pad',ref=ob.GetParentFootprint().GetReference(),number=ob.GetNumber(),uuid=uid,R_ohm=0)
   cost[uid]=rr;details[uid]=detail;lookup[uid]=ob
   for layer in[p.F_Cu,p.B_Cu]:
    if ob.IsOnLayer(layer):
     sh=ob.GetEffectiveShape(layer);objects.append(dict(shape=sh,bb=bbox(sh),id=uid,layer=layer))
  graph=collections.defaultdict(set)
  for c,d in nearby(objects,.01):
   if c['layer']!=d['layer']or c['id']==d['id']:continue
   if p.SHAPE.Collide(c['shape'],d['shape'],p.FromMM(.002)):graph[c['id']].add(d['id']);graph[d['id']].add(c['id'])
  # Differentcontactswithsamepackagepadnumberaresamephysicalterminal.
  grouped=collections.defaultdict(list)
  for uid,q in lookup.items():
   if isinstance(q,p.PAD):grouped[(q.GetParentFootprint().GetReference(),q.GetNumber())].append(uid)
  for group in grouped.values():
   for c in group:
    for d in group:
     if c!=d:graph[c].add(d)
  start=a.m_Uuid.AsString();end=z.m_Uuid.AsString();dist={start:0};prev={};queue=[(0,start)]
  while queue:
   dd,u=heapq.heappop(queue)
   if dd!=dist[u]:continue
   if u==end:break
   for v in graph[u]:
    nd=dd+cost[v]
    if nd<dist.get(v,1e9):dist[v]=nd;prev[v]=u;heapq.heappush(queue,(nd,v))
  assert end in dist,('Mainnativecopperpathmissing',r,n,s,k,net)
  path=[end]
  while path[-1]!=start:path.append(prev[path[-1]])
  path.reverse();i=3 if net in POWER_INPUT else 1.8 if net=='VPA'else 2.;tr=[details[u]for u in path if details[u]['kind']=='track'];R=dist[end]
  for d in tr:
   w=d['width_mm'];l=d['length_mm'];d['I2R_W']=i*i*d['R_ohm'];d['two_end_80C_conduction_neck_rise_C']=d['I2R_W']*l*.001/(8*385*w*.001*35e-6);area=w/.0254*.035/.0254;d['isolated_long_trace_IPC2221_rise_C']=(i/(.048*area**.725))**(1/.44)
  rows.append(dict(from_pin=r+'.'+n,to_pin=s+'.'+k,net=net,current_bound_A=i,R_80C_full_segment_sum_ohm=R,drop_bound_V=i*R,loss_bound_W=i*i*R,min_path_width_mm=min(d['width_mm']for d in tr),path=[details[u]for u in path]))
 save('power-native-main-paths.json',dict(status='PASS_CONNECTED_NATIVE_MAIN_COPPER_PATHS',paths=rows,method='Contactgraphusingactualnativepad/track/viaeffectivegeometry. PertrackFULLresistancechargedontraversal. Parallelcopperandzonesnotcredited. Thinlongsensebranchesexcluded. PackageRdsOn,shuntandinductordropsseparate. Copperrhoat80C. Shortneck1Dtwo-fixed-endestimateversusisolatedlongtraceIPC2221areboundsrequiringmeasurement.',physical='NOT_RUN'))
 print('Nativecurrentpathscalculated',len(rows),'worstdrop',max(x['drop_bound_V']for x in rows))
if __name__=='__main__':main()
