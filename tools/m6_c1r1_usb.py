#!/usr/bin/python3
"""USB protection actual native routing audit; no IEC immunity claim."""
import pcbnew as p,json,collections,math,heapq,sys,hashlib
from pathlib import Path
from m5b_e3_dfm import nearby,bbox
P=Path(__file__).resolve().parents[1]/'hardware/controller';D=P/'review/M6-C1R1'
def main():
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};rows=[]
 for ref,pin,ref2,pin2 in [('U3','5','C10','1'),('J2','A6','U3','1'),('J2','A7','U3','3')]:
  a=next(x for x in fs[ref].Pads() if x.GetNumber()==pin);z=next(x for x in fs[ref2].Pads() if x.GetNumber()==pin2);net=a.GetNetname();assert net==z.GetNetname();objs=[];details={};cost={};graph=collections.defaultdict(set)
  for o in list(b.GetTracks())+[a for f in b.GetFootprints() for a in f.Pads()]:
   if o.GetNetname()!=net:continue
   uid=o.m_Uuid.AsString();via=isinstance(o,p.PCB_VIA);track=isinstance(o,p.PCB_TRACK) and not via
   length=1.6 if via else p.ToMM(o.GetLength()) if track else 0
   cost[uid]=length;details[uid]={'uuid':uid,'kind':'via' if via else 'track' if track else 'pad','length_mm':length}
   for layer in [p.F_Cu,p.B_Cu]:
    if o.IsOnLayer(layer):
     sh=o.GetEffectiveShape(layer);objs.append({'id':uid,'shape':sh,'bb':bbox(sh),'layer':layer})
  for c,e in nearby(objs,.01):
   if c['id']!=e['id'] and c['layer']==e['layer'] and p.SHAPE.Collide(c['shape'],e['shape'],p.FromMM(.002)):graph[c['id']].add(e['id']);graph[e['id']].add(c['id'])
  # Repeated USB connector contacts are internally the same terminal only where same pad number;
  # this graph also requires actual board copper; no connector schematic shortcut.
  aa=a.m_Uuid.AsString();zz=z.m_Uuid.AsString();dist={aa:0};prev={};q=[(0,aa)]
  while q:
   dd,u=heapq.heappop(q)
   if dd!=dist[u]:continue
   if u==zz:break
   for v in graph[u]:
    nd=dd+cost[v]
    if nd<dist.get(v,1e9):dist[v]=nd;prev[v]=u;heapq.heappush(q,(nd,v))
  assert zz in dist,(ref,pin,ref2,pin2)
  path=[zz]
  while path[-1]!=aa:path.append(prev[path[-1]])
  rows.append({'from':ref+'.'+pin,'to':ref2+'.'+pin2,'net':net,'full_segment_length_mm':dist[zz],'path':[details[x] for x in path[::-1]]})
 grounds=[]
 for r,pin in [('U3','2'),('C10','2')]:
  a=next(x for x in fs[r].Pads() if x.GetNumber()==pin);near=[]
  for v in b.GetTracks():
   if isinstance(v,p.PCB_VIA) and v.GetNetname()=='GND':near.append((math.dist((p.ToMM(a.GetPosition().x),p.ToMM(a.GetPosition().y)),(p.ToMM(v.GetPosition().x),p.ToMM(v.GetPosition().y))),v))
  distance,v=min(near,key=lambda x:x[0]);grounds.append({'pad':r+'.'+pin,'nearest_GND_via_distance_mm':distance,'via_xy_mm':[p.ToMM(v.GetPosition().x),p.ToMM(v.GetPosition().y)],'qualification':'Distance only; F.Cu/B.Cu filled-ground continuity confirmed by DRC and IPC. Not a measured inductance.'})
 out={'classification':'Actual native geometry plus manufacturer application comparison; NOT an ESD qualification','selected':'Retain U3 pin5=V3V3; no schematic or USB-layout change','ST_reference':'DS4260 Rev7 Figure13 upstream3.3V transceiver, Figure14 VCC-bias example, sections2.1..2.3 rail-to-rail mechanism/short VCC-GND-I/O connections','routes':rows,'ground_returns':grounds,'capacitance':{'C10_nominal_F':1e-7,'bounded_effective_design_scenario_F':.8e-7,'rail_bulk_nominal_F':44e-6,'bulk_at_ns_edge':'Not credited through board inductance','charge_scenarios':[{'charge_C':q,'ideal_C10_delta_V':q/.8e-7} for q in [1e-9,10e-9,100e-9]],'warning':'Charge division is illustrative only; package TVS, diode current sharing and PCB Ldi/dt dominate IEC pulses. No guaranteed3.3V rail clamp at IEC stress.'},'positive_current_path':'Connector data -> U3 upper steering diode -> local pin5/C10 rail -> internal transil and ground pin2; some charge may disturbV3V3. Main buck cannot be assumed to sink ESD.','negative_current_path':'LocalGND -> U3 lower steering diode -> data terminal; layout inductance adds residual voltage.','alternatives':{'A_V3V3':'Selected; documented rail-to-rail mechanism and5.25V working rating; common rail stays biased when battery-powered. Does not charge absentUSB_VBUS via self-powered data pull-up.','B_raw_USB_VBUS':'Not selected; absentVBUS can be charged by self-powered D+ upper steering, interfering with GPIO37 VBUS detection; higher powered clamp bias and no demonstrated benefit.','C_rail_less_ESD':'Would avoid rail charge-sharing but requires new MPN/landing and residual-clamp review; no demonstrated steady-state defect in A justifies that change.'},'unpowered_host':'Compliant host does not actively drive an unattached peripheral before pull-up. Host-signal misuse/3.3V regulator failure can inject through U3 intoV3V3; this is not an arbitrary-powered-off data isolation device. Verify attachment/reset/backfeed physically; no claim of zero leakage under an externally forced data line.','power_states':[{'battery':bat,'USB_host':usb,'V3V3':'3.3V' if bat or usb else '0V','ESD_pin5':'same V3V3','RF_permission':'inhibited' if not bat else 'requires valid pack/config/init/ARM','PHY':'detach whileVBUS absent; otherwise software-controlled attach after reset'} for bat,usb in [(0,0),(1,0),(0,1),(1,1)]],'physical_tests':'IEC ESD, rail overshoot, enumeration/eye, hotplug and hostile external data injection NOT_RUN'}
 (D/'USB-ESD-review.json').write_text(json.dumps(out,indent=2)+'\n');print([(r['from'],r['to'],round(r['full_segment_length_mm'],3)) for r in rows],grounds)
if __name__=='__main__':main()
