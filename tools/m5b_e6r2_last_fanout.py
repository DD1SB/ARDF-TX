"""Reserve U970 fine-pitch input escapes before routing its output net."""
from m5b_e6r2_common import *
from m5b_e6r2_local_routes import escape
HELD=[]
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));removed=[]
 for t in list(b.GetTracks()):
  bb=t.GetBoundingBox()
  if t.GetNetname()=='VPA_READY' or (t.GetNetname()=='LOCAL_MOD_OFF' and bb.Intersects(p.BOX2I(pt(129,66),pt(11,10)))):
   assert not t.IsLocked();removed.append(t.m_Uuid.AsString());b.Remove(t);HELD.append(t)
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);save('readiness-output-reroute.json',dict(reason='Reserve input fanout before auto-routing output under comparator',removed=removed))
 escape(False,True)
if __name__=='__main__':main()
