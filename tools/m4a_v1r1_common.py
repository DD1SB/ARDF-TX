"""Active RF80 manufacturing closure; historical M4A/E2 data stays read-only."""
import hashlib,json,subprocess
from pathlib import Path
import pcbnew as pcb
from m4a_design import R,E,P,NAME,KEEP,SERVICE
from m4a_design import frozen as frozen_e2
D=P/'review/M4A-V1R1';D.mkdir(parents=True,exist_ok=True)
BASE='4d2f592';REV='M4A-V1R1';DATE='2026-10-18'
ALIASES={
 'J101':('ARDF_TX:Wurth_61201621621',1.4,None),
 'J301':('ARDF_TX:JST_VH_B2P_StandardPTH',1.9,None),
 'J401':('ARDF_TX:Phoenix_1727010_StandardPTH',1.3,None),
 'J502':('ARDF_TX:JST_XH_B3B_StandardPTH',1.3,(1.9,1.95)),
 'Q402':('ARDF_TX:Vishay_IRF610_TO220_StandardPTH',1.4,None),
 'Q403':('ARDF_TX:ST_BD140_SOT32_StandardPTH',1.4,None)}
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def save(n,x):(D/n).write_text(json.dumps(x,indent=2)+'\n')
def gitfile(n):return subprocess.check_output(['git','show',BASE+':'+n],cwd=R)
def frozen():
 names=frozen_e2()
 f=D/'frozen-inputs.json'
 if f.exists():
  for n,h in json.loads(f.read_text()).items():assert sha(R/n)==h,('Read-only evidence changed',n)
 return names
