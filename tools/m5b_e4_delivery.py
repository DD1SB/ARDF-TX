#!/usr/bin/python3
"""Fresh E4 export/native/drill checks, HOLD-labelled archives and manifest."""
import json,subprocess,re
from m5b_e4_common import *
def main():
 guard()
 # Native copper/mask/paste comparisons, explicitly labelled baseline/current.
 evidence=OUT/'development/evidence';evidence.mkdir(parents=True,exist_ok=True);logs=[]
 for revision,board in [('E3',OUT/'development/E3-native.kicad_pcb'),('E4',HW/'RF2M.kicad_pcb')]:
  for layer in ['F.Cu','F.Mask','F.Paste','B.Cu','B.Mask']:
   name=revision+'-'+layer.replace('.','-');fn=evidence/(name+'.svg');cmd=['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layer,'-o',str(fn),str(board)]
   r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True);assert r.returncode==0;logs.append(dict(command=cmd,returncode=r.returncode))
   txt=fn.read_text();txt=re.sub(r'<!DOCTYPE.*?>','',txt,flags=re.S);txt=re.sub(r'width="[^\"]+" height="[^\"]+" viewBox="[^\"]+"','width="750" height="800" viewBox="85 27 15 16"',txt,count=1);fn.write_text('\n'.join(x.rstrip()for x in txt.splitlines())+'\n')
 (evidence/'README.md').write_text('''# Native source-area comparison

E3 files are freshly plotted from the frozen E3 native board; E4 files are
freshly plotted from the active candidate. These are analysis views only.
Colored F.Mask regions are openings, and the white source squares are mask
islands. F.Paste shows the proposed stencil slots. SVG plotting can include
drill marks; the separate Gerber mask/paste layers are authoritative fabrication
artwork. Cropping changes the viewport only. No physical assembly is depicted.
''')
 save('before-after-evidence.json',dict(baseline_native_SHA256=sha(OUT/'development/E3-native.kicad_pcb'),current_native_SHA256=sha(HW/'RF2M.kicad_pcb'),commands=logs,viewBox='Native local area x~105..120/y~47..63; SVG origin translated by board minimum.',physical='NOT_RUN'))
 # KiCad UI state is transient, not an engineering input or review artifact.
 for fn in(OUT/'development').rglob('*.kicad_prl'):fn.unlink()
 # The frozen E3 delivery checker is reused with explicit E4 paths/labels.
 src=(ROOT/'tools/m5b_e3_delivery.py').read_text().replace('from m5b_e3_common import *','from m5b_e4_common import *').replace('M5B-E3','M5B-E4').replace('M5B-E2','M5B-E3').replace('-fabrication-review.zip','-DRAFT-HOLD-fabrication-review.zip').replace('-native.zip','-candidate-native.zip')
 ns={'__name__':'e4_delivery'};exec(compile(src,'m5b_e3_delivery.py','exec'),ns);ns['main']()
 for fn in OUT.rglob('*.csv'):fn.write_bytes(fn.read_bytes().replace(b'\r\n',b'\n'))
 # Strict inherited PDF/Gerber/variant/IPC/native/hash tests, with three E4 docs.
 src=(ROOT/'tools/m5b_artifacts.py').read_text().replace('from m5b_design import HW,OUT,ROOT,preserved','from m5b_e4_common import HW,OUT,ROOT,preserved').replace('M5B-E1','M5B-E4').replace('M5B_E1_','M5B_E4_').replace('assert len(docs)==7','assert len(docs)==3').replace("'FINAL_REVIEW'","'REVIEW_CANDIDATE_HOLD'").replace('Review only,no manufacture authorization','HOLD: unqualified source joint; no manufacture authorization')
 ns={'__name__':'e4_artifacts'};exec(compile(src,'m5b_artifacts.py','exec'),ns);ns['main']()
 subprocess.run(['sha256sum','-c',str(OUT/'SHA256SUMS')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
 print('PASS E4 fresh export/drill/BOM/IPC/checksum consistency. Acceptance remains HOLD; no tag.')
if __name__=='__main__':main()
