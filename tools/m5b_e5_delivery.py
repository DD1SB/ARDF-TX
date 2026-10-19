#!/usr/bin/python3
"""Bind final E5 CAD, source-joint artwork, drill data and review-only archives."""
import re,csv,zipfile,subprocess,types,shutil,xml.etree.ElementTree as ET
from m5b_e5_common import *
def table(name,rows):
 with(OUT/name).open('w')as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def native_inputs():
 files=list(HW.glob('*.kicad_sch'))+[HW/'RF2M.kicad_pro',HW/'RF2M.kicad_pcb',HW/'RF2M.electrical.json',HW/'fp-lib-table',HW/'sym-lib-table']
 files+=list(HW.glob('*.kicad_sym'))+list((HW/'ARDF_2M.pretty').glob('*.kicad_mod'))+list((HW/'ARDF_2M.3dshapes').glob('*'))
 if(HW/'RF2M.kicad_dru').exists():files.append(HW/'RF2M.kicad_dru')
 assert all(f.is_file()for f in files);data={str(f.relative_to(ROOT)):sha(f)for f in sorted(set(files))};save('native-inputs.json',data);save('verification-inputs.json',{str(f.relative_to(ROOT)):sha(f)for f in sorted((ROOT/'tools').glob('m5b_e5*.py'))});return data
def source_artwork():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));q=next(f for f in b.GetFootprints()if f.GetReference()=='Q501');sb=p.BOARD();sb.GetTitleBlock().SetRevision(REV);sb.GetDesignSettings().SetBoardThickness(MM(1.6));sb.Add(q.Duplicate(False));fn=OUT/'development/Q501-stencil-native.kicad_pcb';p.SaveBoard(str(fn),sb);dest=OUT/'stencil';dest.mkdir(exist_ok=True)
 cmd=['kicad-cli','pcb','export','gerbers','--layers','F.Paste','-o',str(dest)+'/',str(fn)];r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0,(r.stdout,r.stderr)
 for job in dest.glob('*.gbrjob'):job.unlink()
 (dest/'README.md').write_text('Q501-only paste, freshly exported from final E5 native footprint. Ordinary0.12mm frameless stainless local stencil. Five source windows plus gate/drain apertures. Separate from bare-PCBZIP. Reflow/wetting/firstjointXray/thermal qualification NOT_RUN. No order authorized.\n')
 def regions(file):
  rows=[]
  for region in re.findall(r'G36\*.*?G37\*',file.read_text(),re.S):
   pts=[(int(x)/1e6,-int(y)/1e6)for x,y in re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',region)]
   if pts:rows.append(((min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)),abs(sum(a[0]*z[1]-z[0]*a[1]for a,z in zip(pts,pts[1:]+pts[:1])))/2))
  return rows
 from m5b_e4r1_common import SOLDER,PASTE
 shift=lambda r:tuple(v-20 if i in[0,2]else v for i,v in enumerate(r));opening=shift(SOLDER);windows=[shift(r)for r in PASTE]
 assert sum(all(abs(x-y)<1e-5 for x,y in zip(r,opening))for r,a in regions(OUT/'gerbers/RF2M-F_Mask.gts'))==1
 for file in[OUT/'gerbers/RF2M-F_Paste.gtp',dest/'Q501-stencil-native-F_Paste.gtp']:
  found=[(r,a)for r,a in regions(file)if any(all(abs(x-y)<1e-5 for x,y in zip(r,w))for w in windows)];assert len(found)==5 and abs(sum(a for r,a in found)-6.765)<1e-5
 save('source-Gerber-geometry-audit.json',dict(status='PASS_ACTUAL_NATIVE_AND_EXPORTED_SOURCE_GEOMETRY',native_sha256=sha(HW/'RF2M.kicad_pcb'),mask_opening_mm=opening,paste_windows_mm=windows,paste_area_mm2=6.765,stencil_mm=.12,open_source_vias=16,guaranteed_tenting=False,source98unchanged=True,physical='NOT_RUN'))
 # Fresh actual CAD source-region plots;viewport cropping changes no geometry.
 evidence=OUT/'development/source-evidence';evidence.mkdir(exist_ok=True)
 for revision,board,crop in[('E4R1',OUT/'development/E4R1-baseline.kicad_pcb','104 46 16 18'),('E5',HW/'RF2M.kicad_pcb','84 46 16 18')]:
  for layer in['F.Cu','F.Mask','F.Paste','B.Cu','B.Mask']:
   fn=evidence/(revision+'-'+layer.replace('.','-')+'.svg');cmd=['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layer,'-o',str(fn),str(board)];r=subprocess.run(cmd,capture_output=True,text=True);assert r.returncode==0;txt=fn.read_text();txt=re.sub(r'<!DOCTYPE.*?>','',txt,flags=re.S);txt=re.sub(r'width="[^"]+" height="[^"]+" viewBox="[^"]+"',f'width="800" height="900" viewBox="{crop}"',txt,count=1);fn.write_text(txt)
 (evidence/'README.md').write_text('Fresh native plots,translated coordinate frames E4R1vsE5. Colored mask is opening,not ink. Via automatic mask suppression is not guaranteed closure:one explicit opening exposes16holes. Analysis only,not fabrication data.\n')
def connectivity():
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));rows=[]
 for f in b.GetFootprints():
  for a in f.Pads():rows.append(dict(ref=f.GetReference(),pin=a.GetNumber(),net=a.GetNetname(),x_mm=p.ToMM(a.GetPosition().x),y_mm=p.ToMM(a.GetPosition().y),footprint=f.GetFPIDAsString()))
 table('pad-connectivity.csv',rows);table('via-connectivity.csv',[dict(uuid=v.m_Uuid.AsString(),net=v.GetNetname(),x_mm=p.ToMM(v.GetPosition().x),y_mm=p.ToMM(v.GetPosition().y),land_mm=p.ToMM(v.GetWidth(p.F_Cu)),drill_mm=p.ToMM(v.GetDrillValue()))for v in b.GetTracks()if isinstance(v,p.PCB_VIA)])
 aa=aliases();lines=[]
 for line in(OUT/'RF2M-logical.ipc').read_text().splitlines():
  if line[:3]in['317','327','367']:line=line[:3]+aa.get(line[3:17].strip(),line[3:17].strip()).ljust(14)+line[17:]
  lines.append(line)
 (OUT/'RF2M-physical-netties.ipc').write_text('\n'.join(lines)+'\n');save('fabrication-net-aliases.json',dict(aliases=aa,reason='Only declared distributed copper/net-tie features merge for physicalbareboardEtest. Logicalschematicmembership remainsseparate.'))
 audit=json.loads((OUT/'pinout-audit.json').read_text());save('critical-package-audit.json',dict(revision=REV,manufacturer_maps=42,pad_sets=320,devices=audit['PCB_physical_devices'],mapping='Actualnativepads checkedagainstschematicandmanufacturer-specificassertions. Translation/rotationchanges listedincomponentdisplacement;none ofthe electricalpinidentities changed.',physical='NOT_RUN'))
 table('component-displacement.csv',json.loads((OUT/'component-displacement.json').read_text())['parts'])
def readiness():
 files=[dict(PCB='Controller',revision='M6-L1',commit='d94dabd0e40137dc44b2bb94f3707ad4636ca65f',board_mm=[100,100],archive='hardware/80m/production/review/M4A-V1R1/three-board-order/CTRL_M6-L1_JLCPCB_5boards.zip'),dict(PCB='RF80',revision='M4A-V1R1',commit='f86684b9ef45eec3ca4ce52edcb62896a847f1d7',board_mm=[150,110],archive='hardware/80m/production/review/M4A-V1R1/fabrication/RF80-V1R1_JLCPCB_5boards.zip'),dict(PCB='RF2M',revision=REV,commit='CandidatecommitrecordedinGit;noacceptancetag',board_mm=[150,110],archive='hardware/2m/review/M5B-E5/fabrication/RF2M-M5B-E5_JLCPCB_5boards.zip')]
 for row in files:
  f=ROOT/row['archive'];assert f.exists(),f;row.update(SHA256=sha(f),quantity=5,layers=2,thickness_mm=1.6,copper_oz=1,finish='Lead-free HASL',mask='Green',legend='White',CAM_quote='NOT_RUN',physical='NOT_RUN',authorization='Independentreviewandexplicituserauthorizationbeforeupload/order')
 save('three-board-manufacturing-readiness.json',dict(boards=files,E4R1_archived_SHA256=sha(HW/'review/M5B-E4R1/RF2M-M5B-E4R1-fabrication-review.zip'),other_archives_modified=False,new_E5_not_yet_independently_accepted=True))
 text='# Three separate five-board prototype datasets\n\nNo combined promotional order,upload,CAMacceptance,quote orpurchase is implied.\n\n|PCB|Revision|Dimensions|Five-boardarchive|Physical|\n|---|---|---|---|---|\n'
 for row in files:text+='|'+ '|'.join([row['PCB'],row['revision'],str(row['board_mm']),row['archive'],'NOT_RUN'])+'|\n'
 (OUT/'THREE_BOARD_READINESS.md').write_text(text+'\nAll2L/1.6mm/1oz/green/white/lead-freeHASL. SourcecommitsandhashesareintheJSONmatrix. Controller/RF80archivesandE4R1remainimmutable. SupplierCAMmustcheckordinaryholes/mask/drillinterpretation;sourceassemblyreflowandthermalqualificationremainOPEN. E5 replacesE4R1onlyafterindependentreviewanduserauthorization.\n')
def main():
 guard();native_inputs();connectivity();source_artwork();(OUT/'fabrication').mkdir(exist_ok=True)
 src=(ROOT/'tools/m5b_e3_delivery.py').read_text().replace('from m5b_e3_common import *','from m5b_e5_common import *').replace('M5B-E3','M5B-E5').replace('M5B-E2','M5B-E4R1').replace("g['Size']['X']-180","g['Size']['X']-150").replace("g['Size']['Y']-140","g['Size']['Y']-110").replace('180x140mm','150x110mm').replace("OUT/'RF2M-M5B-E5-fabrication-review.zip'","OUT/'fabrication/RF2M-M5B-E5_JLCPCB_5boards.zip'")
 ns={'__name__':'E5_fabrication_delivery'};exec(compile(src,'E5_fabrication_delivery','exec'),ns);ns['main']();readiness()
 save('stackup-mechanical.json',dict(revision=REV,outline_mm=[150,110],mount_pattern_mm=[140,100],native_origin_mm=[20,20],holes_native_mm=[[25,25],[165,25],[165,125],[25,125]],layers=2,finished_thickness_mm=1.6,copper_oz=1,finish='Lead-free HASL',mask='green',legend='white',premium=False,source_thermal_vias=98,PA_sink='Fischer SK81 100 SA',bar_mm=[15,44,10],below_board_mm=25.2,mechanical='Dimensionedengineeringenvelopes,not finalenclosure qualification',physical='NOT_RUN'))
 save('source-log.json',dict(review_date='2026-10-19',JLCPCB=dict(url='https://jlcpcb.com/capabilities/pcb-capabilities/',retrieved='2026-10-19',facts='Standard2L/1.6mm±10%/1oz/green/white/HASL;ordinaryPTH+0.13/-0.08mm;position±.075;averagebarrel18umNOTminimum;no premiumvia treatment. Absoluteprocessminimumnotprojectmargin.'),heatsinks=dict(SK81='https://cdn-reichelt.de/documents/datenblatt/C800/OJSK81_D_E_F.pdf',SK100='https://docs.rs-online.com/0660/0900766b80f3d711.pdf',FK213='https://www.farnell.com/datasheets/17590.pdf'),manufacturer_source_joint='PreservedE4R1STPD54008landandAN5046evidence;notreplacedbyassumedassemblyguarantees',controller_antenna='https://docs.espressif.com/projects/esp-hardware-design-guidelines/en/latest/esp32s3/pcb-layout-design.html',supplier_CAM='NOT_RUN'))
 print('PASS E5 freshnative/source-artwork/drill/archives;controller/RF80read-only',flush=True)
if __name__=='__main__':main()
