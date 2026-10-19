#!/usr/bin/python3
"""Compact native/package/source-joint/mount assertions and negative tests."""
import math,copy,csv,collections,xml.etree.ElementTree as ET
from m5b_e5_common import *
from m5b_e4r1_engineering import audit as source_audit,bounds
from m5a_r4_verify import REF as ST_REF

def fps(b):return{f.GetReference():f for f in b.GetFootprints()}
def outline(b):
 a=[v for g in b.GetDrawings()if g.GetLayer()==p.Edge_Cuts for v in[g.GetStart(),g.GetEnd()]]
 return[min(xy(v)[0]for v in a),min(xy(v)[1]for v in a),max(xy(v)[0]for v in a),max(xy(v)[1]for v in a)]
def localpad(a,f):
 x,y=xy(a.GetPosition()-f.GetPosition());t=math.radians(f.GetOrientationDegrees());return(round(x*math.cos(t)-y*math.sin(t),5),round(x*math.sin(t)+y*math.cos(t),5))
def packages(b):
 return{f.GetReference():sorted((a.GetNumber(),a.GetNetname(),localpad(a,f),xy(a.GetSize()),xy(a.GetDrillSize()))for a in f.Pads())for f in b.GetFootprints()}
def geometry(b):
 fs=fps(b);bad=[]
 def ck(t,c):
  if not t:bad.append(c)
 ck(outline(b)==[20.,20.,170.,130.],'compact_outline');ck(abs(p.ToMM(b.GetDesignSettings().GetBoardThickness())-1.6)<1e-6,'stackup')
 for ref,pos in [('H1',(25,25)),('H2',(165,25)),('H3',(165,125)),('H4',(25,125))]:
  ck(xy(fs[ref].GetPosition())==pos,'common_mount');ck(all(abs(p.ToMM(a.GetDrillSize().x)-3.2)<1e-6 and a.GetAttribute()==p.PAD_ATTRIB_NPTH for a in fs[ref].Pads()),'mount_hole')
 for ref,length in LENGTHS.items():
  f=fs[ref];pads={a.GetNumber():a for a in f.Pads()};ck(abs((pads['1'].GetPosition()-pads['2'].GetPosition()).EuclideanNorm()/1e6-length)<1e-5,'RF_length');ck(all(abs(p.ToMM(g.GetBoundingBox().GetHeight())-WIDTH)<1e-5 for g in f.GraphicalItems()if g.GetLayer()==p.F_Cu),'RF_width')
 # Rigid local source/bar geometry: use the manufacturer's canonical frame.
 canonical=translate_board(p.LoadBoard(str(HW/'RF2M.kicad_pcb')),20,0)
 # The input b can be deliberately mutated. Transfer only its relevant local
 # source details through an on-disk-free clone for native negative tests.
 if b is not None:
  q=fps(canonical)['Q501'];cur=fs['Q501'];ck(xy(cur.GetPosition())==(92.,55.),'PA_position')
  ck(len([g for g in cur.GraphicalItems()if g.GetLayer()==p.F_Mask])==1,'source_mask')
  source=next(a for a in cur.Pads()if a.GetNumber()=='S');ck(source.GetNetname()=='GND','source_net')
  ck(sum(isinstance(v,p.PCB_VIA)and v.GetNetname()=='GND'and 89<p.ToMM(v.GetPosition().x)<95 and 48<p.ToMM(v.GetPosition().y)<62 for v in b.GetTracks())==98,'source_vias')
 for ref,pos,rot in[('J101',(27,80),0.0),('J301',(35,120),0.0),('J501',(165,52.206),0.0),('J701',(165,116),0.0)]:
  ck(math.dist(xy(fs[ref].GetPosition()),pos)<.00001 and abs(fs[ref].GetOrientationDegrees()-rot)<.0001,ref+'_connector_pose')
 for ref,y in[('H5',32),('H6',68)]:ck(xy(fs[ref].GetPosition())==(92.,float(y)),'bar_mount')
 # SK81 exact rigid position; M3 washer envelope includes tolerance margin.
 sink=[42.,20.,142.,120.]
 for ref in ['H1','H2','H3','H4']:
  x,y=xy(fs[ref].GetPosition());dist=math.hypot(max(sink[0]-x,0,x-sink[2]),max(sink[1]-y,0,y-sink[3]));ck(dist>=4.75+1.,'sink_pillar_collision')
 # Existing SK10075SA rotated in its mounting plane; ordinary stock spacer.
 x,y=xy(fs['Q401'].GetPosition());xc=x+2.54;passbox=[xc-37.5,y-48.5,xc+37.5,y-8.5]
 for ref in['H1','H2']:
  xx,yy=xy(fs[ref].GetPosition());dist=math.hypot(max(passbox[0]-xx,0,xx-passbox[2]),max(passbox[1]-yy,0,yy-passbox[3]));ck(dist>5.75,'pass_sink_pillar_collision')
 return sorted(set(bad))

def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));old=p.LoadBoard(str(OUT/'development/E4R1-baseline.kicad_pcb'));fs=fps(b);of=fps(old)
 assert not geometry(b),geometry(b)
 canonical=translate_board(p.LoadBoard(str(HW/'RF2M.kicad_pcb')),20,0);sa=source_audit(canonical);assert not sa,sa
 assert packages(b)==packages(old),'Package copper geometry, number or net altered'
 original=json.loads(gitfile('hardware/2m/RF2M.electrical.json'));current=json.loads((HW/'RF2M.electrical.json').read_text());assert original['parts']==current['parts'],'MPN/value/population/electrical change'
 def nets(path):return{n.get('name'):sorted((a.get('ref'),a.get('pin'))for a in n.findall('node'))for n in ET.parse(path).findall('./nets/net')}
 assert nets(OUT/'RF2M.net.xml')==nets(HW/'review/M5B-E4R1/RF2M.net.xml')
 # All twenty module pins, checked against the real native controller pads.
 cb=p.LoadBoard(str(ROOT/'hardware/controller/CTRL.kicad_pcb'));controller={a.GetNumber():a.GetNetname()for a in fps(cb)['J5'].Pads()};module={a.GetNumber():a.GetNetname()for a in fs['J101'].Pads()};mapping={}
 for n in range(1,21):
  a=module[str(n)];c=controller[str(n)];mapping[str(n)]={'RF2M':a,'controller':c};assert (a==c or a in c or a=='V3V3'and c=='V3V3' or a=='GND'and c=='GND'),(n,a,c)
 # Compare every RF object's relative position, rotation and each original
 # distributed copper shape; translation cannot establish measured RF gain.
 rf=[]
 for ref in list(ST_REF)+['Q501','U501','L606','L634','L635','L638','J501','C635','TP601','TP602','TP603','TP604']:
  f,o=fs[ref],of[ref];assert math.dist(xy(f.GetPosition()-o.GetPosition()),(-20.,0.))<.00001 and f.GetOrientationDegrees()==o.GetOrientationDegrees(),ref
  rf.append(ref)
 motion=[]
 for ref,f in fs.items():
  o=of[ref];motion.append(dict(ref=ref,old_mm=xy(o.GetPosition()),new_mm=xy(f.GetPosition()),delta_mm=xy(f.GetPosition()-o.GetPosition()),old_deg=o.GetOrientationDegrees(),new_deg=f.GetOrientationDegrees(),footprint=f.GetFPIDAsString()))
 save('component-displacement.json',dict(baseline=BASE,parts=motion))
 rf_nets={n for value,a,z in ST_REF.values()for n in[a,z]if n!='GND'}|{'NORMAL_CLOCK_BUF','SRC_RF','MMIC_IN','MMIC_RF_DC'}
 def rf_tracks(bb,dx=0):
  return sorted((t.GetNetname(),t.GetLayerName(),tuple(round(v+dx if i==0 else v,5)for i,v in enumerate(xy(t.GetStart()))),tuple(round(v+dx if i==0 else v,5)for i,v in enumerate(xy(t.GetEnd()))),round(p.ToMM(t.GetWidth(p.F_Cu)if isinstance(t,p.PCB_VIA)else t.GetWidth()),5))for t in bb.GetTracks()if t.GetNetname()in rf_nets)
 rf_before,rf_after=rf_tracks(old,-20),rf_tracks(b);assert rf_before==rf_after,'NormalRFsignaltrackgeometrychanged'
 save('normal-RF-copper-equivalence.json',dict(status='PASS_RIGID_NATIVE_RF_COPPER',native_sha256=sha(HW/'RF2M.kicad_pcb'),ST_positions=26,RF_nets=sorted(rf_nets),copper_tracks_and_vias=len(rf_after),translation_mm=[-20,0],geometry_quantization_mm=.00001,matching_width_mm=WIDTH,physical='NOT_RUN'))
 tests=[]
 def reject(name,code,mut,undo):
  mut();res=geometry(b);undo();assert code in res,(name,res);tests.append(dict(name=name,rejected=code))
 f=fs['H2'];v=f.GetPosition();reject('mount_moved_into_sink','common_mount',lambda:f.Move(pt(-25,0)),lambda:f.SetPosition(v))
 f=fs['Q401'];v=f.GetPosition();reject('old_pass_sink_corner_collision','pass_sink_pillar_collision',lambda:f.Move(pt(24,12)),lambda:f.SetPosition(v))
 f=fs['TL608'];a=next(z for z in f.Pads()if z.GetNumber()=='2');v=a.GetPosition();reject('shortened_matching_line','RF_length',lambda:a.Move(pt(-1,0)),lambda:a.SetPosition(v))
 g=next(g for g in f.GraphicalItems()if g.GetLayer()==p.F_Cu);w=g.GetWidth();reject('wrong_matching_width','RF_width',lambda:g.SetWidth(MM(.45)),lambda:g.SetWidth(w))
 a=next(a for a in fs['Q501'].Pads()if a.GetNumber()=='S');n=a.GetNet();reject('source_ground_to_drain','source_net',lambda:a.SetNet(b.FindNet('PA_DRAIN')),lambda:a.SetNet(n))
 via=next(v for v in b.GetTracks()if isinstance(v,p.PCB_VIA)and 91<p.ToMM(v.GetPosition().x)<93 and 53<p.ToMM(v.GetPosition().y)<56);v=via.GetPosition();reject('lost_local_thermal_via','source_vias',lambda:via.Move(pt(10,0)),lambda:via.SetPosition(v))
 for ref in['J101','J701']:
  a=next(iter(fs[ref].Pads()));n=a.GetNet();a.SetNet(b.FindNet('VPA'));assert packages(b)!=packages(old);a.SetNet(n);tests.append(dict(name=ref+'_wrong_net',rejected='package_net_equivalence'))
 # Additional compact/native negative cases. They mutate real geometry only.
 cfg=b.GetDesignSettings();v=cfg.GetBoardThickness();reject('nonstandard_board_thickness','stackup',lambda:cfg.SetBoardThickness(MM(.8)),lambda:cfg.SetBoardThickness(v))
 a=next(iter(fs['H1'].Pads()));v=a.GetDrillSize();reject('wrong_corner_drill','mount_hole',lambda:a.SetDrillSize(pt(2.9,2.9)),lambda:a.SetDrillSize(v))
 for ref in['J101','J301','J501','J701']:
  f=fs[ref];v=f.GetPosition();reject(ref+'_moved_into_inaccessible_pose',ref+'_connector_pose',lambda:f.Move(pt(-8,0)),lambda:f.SetPosition(v))
 f=fs['Q501'];v=f.GetPosition();reject('thermal_cluster_not_rigid','PA_position',lambda:f.Move(pt(1,0)),lambda:f.SetPosition(v))
 for ref in['J301','J501']:
  a=next(z for z in fs[ref].Pads()if z.GetNumber()=='1');n=a.GetNet();a.SetNet(b.FindNet('GND'));assert packages(b)!=packages(old);a.SetNet(n);tests.append(dict(name=ref+'_battery_or_RF_net_corruption',rejected='package_net_equivalence'))
 assert all(fs[r].GetValue()==of[r].GetValue()for r in fs),'PCBcomponentvalueschanged'
 f=fs['C401'];v=f.GetValue();f.SetValue('wrong_capacitance');assert any(fs[r].GetValue()!=of[r].GetValue()for r in fs);f.SetValue(v);tests.append(dict(name='wrong_component_value',rejected='native_value_equivalence'))
 save('compact-engineering.json',dict(status='PASS_NATIVE_COMPACT_EQUIVALENCE',native_sha256=sha(HW/'RF2M.kicad_pcb'),outline_mm=[150,110],area_reduction_percent=100*(1-150*110/(180*140)),RF80_mount_native_mm=[[25,25],[165,25],[165,125],[25,125]],pad_sets=len(packages(b))-6,electrical_parts=len(current['parts']),schematic_net_memberships_equal=True,MPN_values_populations_equal=True,connector_pins=mapping,rigid_RF=rf,source_assembly_E4R1_errors=sa,RF_ground='Source local geometry retained. Distributed line B.Cu keepouts preserve ground reference; assembled stability NOT_RUN.',source_thermal_vias=98,source_paste_windows=5,physical='NOT_RUN',negative_tests=tests))
 # Reuse the actual source-joint/mask/paste and all twenty E4R1 negatives on
 # canonical translated data without changing the active PCB or old reports.
 src=(ROOT/'tools/m5b_e4r1_engineering.py').read_text();start=src.index(' tests=[]\n');end=src.index(" source_area=",start);block=src[start:end]
 context=dict(b=canonical,fs=fps(canonical),p=p,MM=MM,xy=xy,bounds=bounds,math=math,audit=source_audit,json=json,OUT=OUT)
 from m5b_e4r1_common import INNER,TOP_RECTS
 from m5b_e4r1_thermal import solve
 context.update(INNER=INNER,TOP_RECTS=TOP_RECTS,solve=solve);exec(compile('if True:\n'+block,'source_joint_regression','exec'),context)
 save('source-assembly-regression.json',dict(status='PASS',native_tests=context['tests'],thermal_tests=context['bad'],physical='NOT_RUN'))
 # Preserve the complete quantitative E4R1 source process gate, now bound to E5.
 from m5b_e4r1_common import SOLDER,SIDE,NEAR,OUTER,WINDOW,PASTE,via_specs
 from m5b_e4r1_engineering import area
 tail=src[src.index(' source_area='):src.index(" save('engineering-regression.json'")]
 context.update(area=area,PASTE=PASTE,SOLDER=SOLDER,SIDE=SIDE,NEAR=NEAR,OUTER=OUTER,WINDOW=WINDOW,via_specs=via_specs,sha=sha,HW=HW,save=save)
 exec(compile('if True:\n'+tail,'source_process_gate','exec'),context)
 report=json.loads((OUT/'source-assembly-DFM.json').read_text());report.update(revision=REV,canonical_translation_mm=[20,0],actual_native_coordinates='Q501=(92,55);sourcewindow=(90.95,52.5)..(93.05,57.5);bottom=(85,47)..(99,63)',extra_washer_ground_vias=2,additional_thermal_credit=False);save('source-assembly-DFM.json',report)

 print('PASS compact equivalence,20controller pins,98thermal vias,RF rigid groups,18compact +20source negatives')
if __name__=='__main__':main()
