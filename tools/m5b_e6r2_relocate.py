"""Resolve control-fanout conflict with preserved RF bottom-track keepout.
One-time local5mm shift; native PCB is authoritative after application.
"""
from m5b_e6r2_common import *
from m5b_e6r2_local_routes import escape
HELD=[]
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs=fps(b);assert xy(fs['U970'].GetPosition())==(139.,65.),'Already shifted'
 parts={z['ref']:z for z in manifest()['parts']};refs={r for r in parts if r[0]in 'URCT' and r in fs and ((r.startswith('TP') and 970<=int(r[2:])<=976) or (not r.startswith('TP') and r[1:].isdigit() and 970<=int(r[1:])<=986))}-{'R970','TP970','TP971'}
 # All unique new logic nets are rerouted; existing KEY/NORMAL_OFF/V3V3 feeds
 # are cut only in the local cluster. RF nets/source array are never altered.
 special={'KEY_N','NORMAL_OFF','V3V3','GND','VPA','VDRV_MMIC','VREG_SWITCH'};nets={n for r in refs for n in parts[r]['pins'].values() if n};removed=[]
 for t in list(b.GetTracks()):
  if t.GetNetname() not in nets:continue
  bb=t.GetBoundingBox();inbay=bb.Intersects(p.BOX2I(pt(126,58),pt(40,32)))
  if t.GetNetname() in special and not inbay:continue
  assert not(85<xy(t.GetPosition())[0]<99 and 47<xy(t.GetPosition())[1]<63)
  if t.IsLocked():continue # historical ground stitching retained
  removed.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname()));b.Remove(t);HELD.append(t)
 moved=[]
 for r in sorted(refs):
  f=fs[r];old=xy(f.GetPosition());f.Move(pt(0,5));moved.append(dict(ref=r,old=old,new=xy(f.GetPosition())))
 # Local earlier routes belonging to other nets may no longer clear a moved
 # pad. Open only the impacted control traces; source/RF geometry is guarded.
 protected=set(json.loads(gitfile('hardware/2m/review/M5B-E5/normal-RF-copper-equivalence.json'))['RF_nets']);pads=[a for r in refs for a in fs[r].Pads()]
 for t in list(b.GetTracks()):
  if any(a.GetNetname()!=t.GetNetname() and any(a.IsOnLayer(l) and t.IsOnLayer(l) and p.SHAPE.Collide(a.GetEffectiveShape(l),t.GetEffectiveShape(l),MM(.17)) for l in [p.F_Cu,p.B_Cu]) for a in pads):
   assert t.GetNetname() not in protected and not t.IsLocked(),('Explicit RF review needed',t.GetNetname())
   removed.append(dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),reason='Moved pad clearance'));b.Remove(t);HELD.append(t)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('logic-cluster-shift.json',dict(reason='Respect preserved B.Cu RF ground-reference no-track bandY43..65; new fanouts now below band',moved=moved,removed_routes=removed))
 escape(False,True);escape(True,True)
if __name__=='__main__':main()
