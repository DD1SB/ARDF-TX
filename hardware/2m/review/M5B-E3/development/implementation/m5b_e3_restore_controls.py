#!/usr/bin/python3
"""Restore E2 control routes before selective standard-process via enlargement.
RF artwork, source thermal array, substrate and new matching placements remain.
This local rollback avoids retaining experimental wholesale via movement.
"""
import pcbnew as p,json,math
from m5b_e3_common import *
from m5b_e3_local import pt,xy,aliases
RF={'MMIC_COUPLED','MMIC_AC','ST_IS_A','ST_IS_B','ST_IS_C','ST_IS_D','PA_GATE','PA_DRAIN','ST_O_A','ST_O_B','ST_O_C','ST_O_D','ST_DC_BLOCK','ST_LPF_IN','ST_F1','ST_F2','NORMAL_RF'}
def main():
 guard();base=OUT/'development/E2-native.kicad_pcb';base.parent.mkdir(exist_ok=True);base.write_bytes(gitfile('hardware/2m/RF2M.kicad_pcb'));old=p.LoadBoard(str(base));b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'))
 oldpads={(f.GetReference(),a.GetNumber()):xy(a.GetPosition())for f in old.GetFootprints()for a in f.Pads()};newpads={(f.GetReference(),a.GetNumber()):xy(a.GetPosition())for f in b.GetFootprints()for a in f.Pads()};moves={oldpads[k]:newpads[k]for k in oldpads if k in newpads and math.dist(oldpads[k],newpads[k])>.001}
 import m5a_r1_design as c,copy
 tree=c.parse((HW/'RF2M.kicad_pcb').read_text());ot=c.parse(base.read_text())
 def take(t):
  if t[0]=='via':
   x,y=map(float,c.child(t,'at')[1:3]);return not(abs(x-112)<1 and abs(y-55)<2.2)
  return c.child(t,'net')[1]not in RF
 for t in list(tree):
  if isinstance(t,list)and t[0]in['segment','via','arc']and take(t):tree.remove(t)
 for t in ot:
  if not isinstance(t,list)or t[0]not in['segment','via','arc']or not take(t):continue
  q=copy.deepcopy(t)
  if q[0]=='segment':
   for end in ['start','end']:
    pos=c.child(q,end);xy0=tuple(map(float,pos[1:3]))
    if xy0 in moves:pos[1:3]=[c.Atom(str(v))for v in moves[xy0]]
  tree.append(q)
 (HW/'RF2M.kicad_pcb').write_text(c.dump(tree)+'\n');b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'))
 # Restore logical inline test contacts over RF copper. These are net-tie
 # aliases; physical artwork independently joins the line's two names.
 for r,n,x,y in [('TP601','PA_GATE',109.75,55),('TP602','PA_DRAIN',114.25,55),('TP603','ST_LPF_IN',145.802399,52.206),('TP604','MMIC_AC',88.4455,55)]:
  a=next(f for f in b.GetFootprints()if f.GetReference()==r);z=next(iter(a.Pads())).GetPosition();t=p.PCB_TRACK(b);t.SetStart(z);t.SetEnd(pt(x,y));t.SetWidth(p.FromMM(.15));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(n));b.Add(t)
 # Keep driver termination's ground connection robust inside local plane.
 f=next(f for f in b.GetFootprints()if f.GetReference()=='R651')
 for a in f.Pads():
  if a.GetNetname()=='GND':a.SetLocalZoneConnection(p.ZONE_CONNECTION_FULL)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
 cfg=json.loads((HW/'RF2M.kicad_pro').read_text());cfg['board']['design_settings']['rules']['min_via_diameter']=.6;cfg['board']['design_settings']['rules']['min_via_annular_width']=.15;(HW/'RF2M.kicad_pro').write_text(json.dumps(cfg,indent=2)+'\n')
 print('Restored control routes; retained RF and thermal E3 changes')
if __name__=='__main__':main()
