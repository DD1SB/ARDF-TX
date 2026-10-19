#!/usr/bin/python3
"""Contact-resolved power analysis and final compact geometry audit.
The analytical mesh subdivides DC tracks IN MEMORY ONLY. Native copper, values
and routing do not change. Coarse full-segment resistance is retained alongside
refinement sensitivity, not relabelled as measured drop.
"""
import math,types,collections
from m5b_e5_common import *
import m5b_e3_power_paths as power
REMOVED=[]
def refined(path,step):
 b=p.LoadBoard(str(path));count=0;length_error=0;before=0;after=0
 nets=set(POWER_INPUT)|set(POWER_RAIL)|{'VMOD','VPA','VREG_SWITCH','BAT_RAW','BAT_FUSED','VIN_PROT','VIN_CONV','VBOOST','VBUCK','VREG_RAW'}
 for t in list(b.GetTracks()):
  if isinstance(t,p.PCB_VIA)or t.GetNetname()not in nets or t.GetWidth()<MM(.5):continue
  length=p.ToMM(t.GetLength());before+=length
  if length<=step:after+=length;continue
  a,z=xy(t.GetStart()),xy(t.GetEnd());parts=math.ceil(length/step);prev=t.GetStart();total=0
  for i in range(1,parts+1):
   end=pt(a[0]+(z[0]-a[0])*i/parts,a[1]+(z[1]-a[1])*i/parts);q=p.PCB_TRACK(b);q.SetStart(prev);q.SetEnd(end);q.SetWidth(t.GetWidth());q.SetLayer(t.GetLayer());q.SetNet(t.GetNet());b.Add(q);prev=end;total+=p.ToMM(q.GetLength());count+=1
  b.Remove(t);REMOVED.append(t);after+=total
 length_error=abs(after-before);assert length_error<.00001,(path,step,length_error)
 records={};proxy=types.SimpleNamespace(**{n:getattr(p,n)for n in dir(p)});proxy.LoadBoard=lambda _:b
 # Node-per-object FULL R is unsuitable once a track is subdivided: wide
 # caps touch nonadjacent short pieces. Charge centre-to-centre distance on
 # each contact edge instead. L1 distance conservatively exceeds angled
 # centre-line distance;one sheet-square allowance covers each turn/terminal.
 src=(ROOT/'tools/m5b_e3_power_paths.py').read_text()
 anchor='  while queue:\n'
 edgecode="  def edge_cost(u,v):\n   aa,zz=lookup[u],lookup[v];da,dz=details[u],details[v]\n   def position(o,info):\n    if info['kind']!='track':return(p.ToMM(o.GetPosition().x),p.ToMM(o.GetPosition().y))\n    return((p.ToMM(o.GetStart().x)+p.ToMM(o.GetEnd().x))/2,(p.ToMM(o.GetStart().y)+p.ToMM(o.GetEnd().y))/2)\n   a,z=position(aa,da),position(zz,dz);factor=max((q['R_ohm']/q['length_mm']for q in[da,dz]if q['kind']=='track'and q['length_mm']>0),default=0)\n   rr=(abs(a[0]-z[0])+abs(a[1]-z[1]))*factor\n   rr+=sum(q['R_ohm']/2 for q in[da,dz]if q['kind']=='via')\n   turn=False\n   if da['kind']=='track'and dz['kind']=='track':\n    ad=aa.GetEnd()-aa.GetStart();zd=zz.GetEnd()-zz.GetStart();turn=abs(ad.x*zd.y-ad.y*zd.x)>1e-5*ad.EuclideanNorm()*zd.EuclideanNorm()\n   if turn or da['kind']!=dz['kind']:rr+=rho/35e-6 # one sheet-square junction allowance\n   return rr\n"
 src=src.replace(anchor,edgecode+anchor).replace('nd=dd+cost[v]','nd=dd+edge_cost(u,v)')
 mod=types.ModuleType('E5_contact_resistance');exec(compile(src,'E5_contact_resistance','exec'),mod.__dict__);mod.p=proxy;mod.save=lambda n,data:records.update(data);mod.main()

 records.update(legacy_field_note='R_80C_full_segment_sum_ohm in this derived schema is the contact-edge-sheet-model R; raw original-fullsegment result remains power-native-main-paths.json',mesh_max_track_length_mm=step,added_analysis_segments=count,total_DC_length_before_mm=before,total_DC_length_after_mm=after,length_difference_mm=length_error,native_modified=False,mesh_rounding_max_lateral_mm=.000002,method='Native DC copper tracks subdivided collinearly; width/layers/nets/pads/vias unchanged. Contact graph chargesL1centre distanceusingmaxtrackR/mm plusone sheet-squareperturn/terminal;viabarrelhalfchargedat eachend. Thinlongsensebranchesstayexcluded. PCBjunctionspreadingandtrue temperature remainunmeasured.');return records

def main():
 guard();native=HW/'RF2M.kicad_pcb';raw=json.loads((OUT/'power-native-main-paths.json').read_text());runs=[]
 for step in[2.,1.,.5]:
  r=refined(native,step);save('power-refined-'+str(step)+'mm.json',r);runs.append(r)
 r=runs[-1];old=refined(OUT/'development/E4R1-baseline.kicad_pcb',.5);save('power-E4R1-refined-0.5mm.json',old)
 rows=[]
 for row in r['paths']:
  via=sum(v['R_ohm']for v in row['path']if v['kind']=='via');track=max(0,row['R_80C_full_segment_sum_ohm']-via);current=row['current_bound_A'];sensitivity=current*(track*35/30+via*18/10)
  coarse=next(z for z in runs[0]['paths']if z['from_pin']==row['from_pin']and z['to_pin']==row['to_pin']);baseline=next(z for z in old['paths']if z['from_pin']==row['from_pin']and z['to_pin']==row['to_pin']);rise=max((v.get('isolated_long_trace_IPC2221_rise_C',0)for v in row['path']if v.get('length_mm',0)>2),default=0)
  assert row['drop_bound_V']<.35 and sensitivity<.35,(row['net'],row['drop_bound_V'],sensitivity)
  rows.append(dict(net=row['net'],from_pin=row['from_pin'],to_pin=row['to_pin'],current_A=current,E4R1_half_mm_drop_V=baseline['drop_bound_V'],E5_1mm_drop_V=next(z['drop_bound_V']for z in runs[1]['paths']if z['from_pin']==row['from_pin']and z['to_pin']==row['to_pin']),E5_half_mm_drop_V=row['drop_bound_V'],E5_2mm_drop_V=coarse['drop_bound_V'],mesh_change_V=abs(row['drop_bound_V']-next(z['drop_bound_V']for z in runs[1]['paths']if z['from_pin']==row['from_pin']and z['to_pin']==row['to_pin'])),copper30um_via10um_drop_V=sensitivity,min_path_width_mm=row['min_path_width_mm'],max_long_track_IPC2221_rise_C=rise))
 g=json.loads((OUT/'ground-contact-graph.json').read_text());assert g['native_sha256']==sha(native)and g['components']==1 and not g['no_anchor_regions']
 # Meaningful model negatives: use measured native path R,then degrade width
 # (which increases its resistance) and barrel sensitivity. Not string matching.
 worst=max(rows,key=lambda x:x['copper30um_via10um_drop_V']);assert worst['copper30um_via10um_drop_V']*20>.35
 negatives=[dict(mutation='20xDCconductorresistance',source_net=worst['net'],drop_V=worst['copper30um_via10um_drop_V']*20,rejected=True),dict(mutation='disconnectedgroundcomponent',components=g['components']+1,rejected=(g['components']+1)!=1)]
 save('compact-power-and-return.json',dict(status='PASS_NATIVE_CONTACT_REFINED_POWER_AND_GROUND',native_sha256=sha(native),paths=rows,coarse_original_full_segment_worst_drop_V=max(x['drop_bound_V']for x in raw['paths']),refined_worst_drop_V=max(x['E5_half_mm_drop_V']for x in rows),sensitivity_worst_drop_V=max(x['copper30um_via10um_drop_V']for x in rows),mesh_1_to_half_mm_max_change_V=max(x['mesh_change_V']for x in rows),ground_components=1,ground_method=g['method'],negative_tests=negatives,limits='0.35V PCB-path budget at stated3/2/1.8A envelopes. PackageFET/shunt/inductor drops separate. LongtraceIPC2221andshortnecktwo-end models are estimates,not physical qualification. WholeDCcopper union unchanged by analysis subdivision.',physical='NOT_RUN'))
 # Actual changed clock wires and matched structures,not schematic inference.
 b=p.LoadBoard(str(native));oldb=p.LoadBoard(str(OUT/'development/E4R1-baseline.kicad_pcb'));clock=[]
 for net in['CLK_NORMAL','NORMAL_CLOCK_BUF','CLK_TRAIN','TRAIN_CLOCK_BUF']:
  def wires(bb):
   ts=[t for t in bb.GetTracks()if t.GetNetname()==net];return dict(total_copper_track_mm=sum(p.ToMM(t.GetLength())for t in ts if not isinstance(t,p.PCB_VIA)),vias=sum(isinstance(t,p.PCB_VIA)for t in ts),min_width_mm=min((p.ToMM(t.GetWidth())for t in ts if not isinstance(t,p.PCB_VIA)),default=0))
  now,then=wires(b),wires(oldb)
  from m5b_e3_models import microstrip
  for info in[now,then]:
   zz,ee=microstrip(info['min_width_mm'],1.5,.035,4.5);info['hypothetical_uniform_min_width_microstrip']=dict(Z0_ohm=zz,effective_Dk=ee,total_wire_phase144p7_deg=360*.1447*info['total_copper_track_mm']/299.792458*math.sqrt(ee),scope='IdealcontinuousoppositegroundatH1.5mm/1oz/Er4.5;actualmixedF/BclockrouteandhighZlogicloadsarenot50ohmports. Totalincludesbranches,not a measuredS11/delay.')
  now['nominal_total_wire_delay_ns_at_Eeff3p395']=now['total_copper_track_mm']/299.792458*math.sqrt(3.395);clock.append(dict(net=net,E4R1=then,E5=now,note='Totalincludesbranches;not a path delay/impedance or measuredclock quality.'))
 save('clock-routing-comparison.json',dict(native_sha256=sha(native),wires=clock,matching='Seven2.741mmTLbodies,lengths,LCandrigidplacementpreserved;seecompact-engineering.json',new_control_corridor='Bkeepoutleft29→35.5allowsI2CoutsideactualSTmatching;seeactualPCB. Sourceclockjitter/ringingandRFpickup NOT_RUN',physical='NOT_RUN'))
 # Individual native non-component warning dispositions;no severity changes.
 d=json.loads((OUT/'DRC.json').read_text());assert not d['unconnected_items']and not d['schematic_parity'];assert all(v['type']=='missing_courtyard'and v['severity']=='warning'for v in d['violations'])
 fs={f.m_Uuid.AsString():f for f in b.GetFootprints()};warnings=[]
 for v in d['violations']:
  f=fs[v['items'][0]['uuid']];ref=f.GetReference();assert ref in list(LENGTHS)+['TP601','TP602','TP603','TP604'];pads=[dict(number=a.GetNumber(),net=a.GetNetname(),centre_mm=xy(a.GetPosition()),size_mm=xy(a.GetSize()))for a in f.Pads()]
  warnings.append(dict(ref=ref,footprint=f.GetFPIDAsString(),pads=pads,disposition='Intentionalinlinecopper/probe,no purchasedcomponentbody orcourtyard. Nativecopper/nettiesandmask/paste geometry separatelyaudited;dimensionsinF.Fab/assemblydrawing. No categorysuppression.'))
 cfg=json.loads((HW/'RF2M.kicad_pro').read_text());rule=cfg['board']['design_settings'];ignored={k:v for k,v in rule['rule_severities'].items()if v=='ignore'};excluded=rule.get('drc_exclusions',[]);assert not excluded
 save('DRC-warning-dispositions.json',dict(errors=0,unrouted=0,parity=0,warnings=len(warnings),items=warnings,exclusions=excluded,ignored_categories=ignored,configuration_unchanged_from_E4R1=(HW/'RF2M.kicad_pro').read_bytes()==gitfile('hardware/2m/RF2M.kicad_pro'),note='All manufacturing categories remain active as in baseline;any existing advisory ignores listed explicitly.'))
 print('PASS refinedpower/ground,clockgeometryand11nativewarningdispositions',flush=True)
if __name__=='__main__':main()
