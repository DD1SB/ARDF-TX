"""Native-obstacle grid search, C++17 backend; final DRC is authoritative."""
import hashlib,subprocess
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];TMP=Path('/tmp/m5b-e6r2/grid');TMP.mkdir(exist_ok=True,parents=True)
def solve(masks,vm,nx,ny,starts,goals):
 src=ROOT/'tools/m5b_e6r2_grid.cpp';binary=TMP/'route';signature=hashlib.sha256(src.read_bytes()).hexdigest();stamp=TMP/'source.sha'
 if not binary.exists() or not stamp.exists() or stamp.read_text()!=signature:
  subprocess.run(['g++','-std=c++17','-O2','-Wall','-Wextra',str(src),'-o',str(binary)],check=True);stamp.write_text(signature)
 pre=TMP/'case'
 for i in [0,1]:
  Path(str(pre)+f'-m{i}.raw').write_bytes(masks[i]);Path(str(pre)+f'-v{i}.raw').write_bytes(vm[i])
 Path(str(pre)+'.txt').write_text(f'{nx} {ny} {len(starts)} {len(goals)}\n'+' '.join(map(str,starts))+'\n'+' '.join(map(str,goals))+'\n')
 out=TMP/'path';r=subprocess.run([str(binary),str(pre),str(out)],capture_output=True,text=True);print(r.stderr.strip(),flush=True)
 if r.returncode==4:return None,0
 assert r.returncode==0,(r.returncode,r.stderr)
 return [int(x)for x in out.read_text().splitlines()],int(r.stderr.split()[1])
