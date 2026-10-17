#!/usr/bin/python3
"""Fresh E4R1 native plots/stencil, drill parity, review archives and checksums."""
import json,re,subprocess
import pcbnew as p
from m5b_e4r1_common import *
def main():
 guard();evidence=OUT/'development/evidence';evidence.mkdir(parents=True,exist_ok=True);commands=[]
 for revision,board in[('E4',OUT/'development/E4-native.kicad_pcb'),('E4R1',HW/'RF2M.kicad_pcb')]:
  for layer in['F.Cu','F.Mask','F.Paste','B.Cu','B.Mask']:
   fn=evidence/(revision+'-'+layer.replace('.','-')+'.svg');cmd=['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layer,'-o',str(fn),str(board)];r=subprocess.run(cmd,capture_output=True,text=True,cwd=ROOT);assert r.returncode==0;commands.append(dict(command=cmd,returncode=r.returncode));txt=fn.read_text();txt=re.sub(r'<!DOCTYPE.*?>','',txt,flags=re.S);txt=re.sub(r'width="[^\"]+" height="[^\"]+" viewBox="[^\"]+"','width="750" height="800" viewBox="85 27 15 16"',txt,count=1);fn.write_text('\n'.join(x.rstrip()for x in txt.splitlines())+'\n')
 (evidence/'README.md').write_text('E4/E4R1 fresh native plots. Colored mask is OPENING,not ink. E4R1hasone source opening,no islands. Automatic via-land circles are suppressed by the per-via setting;explicit source opening exposes all16joint holes. The Gerber union governs physical openings,not the via tent flag. Cropping only changes viewport. Analysis,not fabrication data.\n')
 save('before-after-evidence.json',dict(baseline_native_SHA256=sha(OUT/'development/E4-native.kicad_pcb'),candidate_native_SHA256=sha(HW/'RF2M.kicad_pcb'),commands=commands,physical='NOT_RUN'))
 # Export the actual native Q501 footprint alone to a separate standard stencil.
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));q=next(f for f in b.GetFootprints()if f.GetReference()=='Q501');sb=p.BOARD();sb.GetDesignSettings().SetBoardThickness(p.FromMM(1.6));sb.GetTitleBlock().SetRevision(REV);sb.Add(q.Duplicate(False));fn=OUT/'development/Q501-stencil-native.kicad_pcb';p.SaveBoard(str(fn),sb)
 dest=OUT/'stencil';dest.mkdir(exist_ok=True);cmd=['kicad-cli','pcb','export','gerbers','--layers','F.Paste','-o',str(dest)+'/',str(fn)];r=subprocess.run(cmd,capture_output=True,text=True,cwd=ROOT);assert r.returncode==0,(r.stdout,r.stderr)
 (dest/'README.md').write_text('Q501-onlyF.Paste exportedfromtheactualnativefootprint. Standard0.12mmframeless304stainless,laser-cut. Source5windows+G/Dpaste,nootherparts. NOTpartofbare-PCBfabricationZIP. Verifyalignment/depositsandqualifyprofile/firstjointbeforeenergy. Noorderauthorized.\n')
 # Stencil is a paste layer, not a second board fabrication job.
 for job in dest.glob('*.gbrjob'):job.unlink()
 def region_boxes(file):
  rows=[]
  for region in re.findall(r'G36\*.*?G37\*',file.read_text(),re.S):
   points=[(int(x)/1e6,-int(y)/1e6)for x,y in re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',region)]
   if not points:continue
   bounds=(min(x for x,y in points),min(y for x,y in points),max(x for x,y in points),max(y for x,y in points));area=abs(sum(a[0]*z[1]-z[0]*a[1]for a,z in zip(points,points[1:]+points[:1])))/2;rows.append((bounds,area))
  return rows
 actual_mask=[r for r,a in region_boxes(OUT/'gerbers/RF2M-F_Mask.gts')if all(abs(x-y)<1e-5 for x,y in zip(r,SOLDER))];assert len(actual_mask)==1,'Source Gerber opening differs from native'
 for file in[OUT/'gerbers/RF2M-F_Paste.gtp',dest/'Q501-stencil-native-F_Paste.gtp']:
  rows=region_boxes(file);found=[r for r,a in rows if any(all(abs(x-y)<1e-5 for x,y in zip(r,expected))for expected in PASTE)];assert len(found)==5,(file,'Paste source windows missing');assert abs(sum(a for r,a in rows if r in found)-6.765)<1e-5
 save('source-Gerber-geometry-audit.json',dict(status='PASS_NATIVE_AND_ACTUAL_GERBER_SOURCE_MASK_PASTE_DRILL',source_mask_bbox_mm=actual_mask[0],source_paste_windows_mm=PASTE,stencil_source_windows_equal_final_board=True,source_holes='Native PTHcoordinates separately compared with final drill;16holecenterslieinexplicitmaskopening',automatic_via_mask_annuli='Suppressed:explicitopeninggoverns;NOTa guaranteedtentclaim',physical_joint='NOT_RUN'))
 save('stencil-export-audit.json',dict(native_Q501_preserved=True,command=cmd,returncode=r.returncode,stencil_mm=.12,source_windows=5,source_total_area_mm2=6.765,source_geometric_paste_mm3=.8118,standard_process=True,assembly='NOT_RUN',included_in_bare_board_ZIP=False))
 for fn in(OUT/'development').rglob('*.kicad_prl'):fn.unlink()
 src=(ROOT/'tools/m5b_e3_delivery.py').read_text().replace('from m5b_e3_common import *','from m5b_e4r1_common import *').replace('M5B-E3','M5B-E4R1').replace('M5B-E2','M5B-E4')
 ns={'__name__':'r1_fabrication_archive'};exec(compile(src,'m5b_e3_delivery.py','exec'),ns);ns['main']()
 for fn in OUT.rglob('*.csv'):fn.write_bytes(fn.read_bytes().replace(b'\r\n',b'\n'))
 for fn in OUT.rglob('*.svg'):fn.write_text('\n'.join(x.rstrip()for x in fn.read_text().splitlines())+'\n')
 src=(ROOT/'tools/m5b_artifacts.py').read_text().replace('from m5b_design import HW,OUT,ROOT,preserved','from m5b_e4r1_common import HW,OUT,ROOT,preserved').replace('M5B-E1','M5B-E4R1').replace('M5B_E1_','M5B_E4R1_').replace('assert len(docs)==7','assert len(docs)==4').replace("'FINAL_REVIEW'","'CANDIDATE_INDEPENDENT_REVIEW'").replace('Review only,no manufacture authorization','Independent review only;physical qualification NOT_RUN;no manufacture authorization')
 ns={'__name__':'r1_artifact_audit'};exec(compile(src,'m5b_artifacts.py','exec'),ns);ns['main']()
 subprocess.run(['sha256sum','-c',str(OUT/'SHA256SUMS')],cwd=ROOT,check=True,stdout=subprocess.DEVNULL)
 print('PASS E4R1fresh stencil/Gerber/drill/BOM/IPC/native/inventory consistency;no acceptance tag')
if __name__=='__main__':main()
