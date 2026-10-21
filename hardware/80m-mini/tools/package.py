#!/usr/bin/env python3
"""Preserve a portable review archive and assert isolation from existing designs."""
from pathlib import Path
import hashlib,json,subprocess,zipfile
P=Path(__file__).resolve().parents[1];ROOT=P.parents[1];BASE='8a83ea0381dfeaca8f4627353cbfec9a5f2a0e33'
def git(*a):return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
def main():
 changed=git('diff','--name-only',BASE,'--').splitlines()
 outside=[f for f in changed if not f.startswith('hardware/80m-mini/')]
 assert not outside,outside
 scope={'base_commit':BASE,'branch':git('branch','--show-current'),'existing_tracked_files_changed':outside,'scope':'Only hardware/80m-mini/ added. Existing accepted history and manufacturing files preserved.','publication':'Local review only; no push/tag/order/hardware activation performed.'}
 (P/'review/scope-guard.json').write_text(json.dumps(scope,indent=2)+'\n')
 zipname='Mini80-M80-E1-review.zip';skip={zipname,zipname+'.sha256','package-SHA256SUMS.txt'}
 files=[]
 for f in P.rglob('*'):
  rel=f.relative_to(P)
  if not f.is_file()or f.name in skip or any(q in ['build','__pycache__']for q in rel.parts)or f.suffix in ['.kicad_prl','.lck']:continue
  files.append(f)
 files.sort();manifest=P/'review/package-SHA256SUMS.txt'
 manifest.write_text(''.join(hashlib.sha256(f.read_bytes()).hexdigest()+'  '+str(f.relative_to(P))+'\n'for f in files));files.append(manifest)
 dest=P/'review'/zipname
 with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED)as z:
  for f in files:z.write(f,'80m-mini/'+str(f.relative_to(P)))
 dest.with_name(zipname+'.sha256').write_text(hashlib.sha256(dest.read_bytes()).hexdigest()+'  '+zipname+'\n')
 print(json.dumps({'archive':str(dest),'files':len(files),'bytes':dest.stat().st_size,'scope_guard':scope},indent=2))
if __name__=='__main__':main()
