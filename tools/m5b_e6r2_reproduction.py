"""Fresh independent CAM/netlist export comparison; no archived file replacement."""
import subprocess,re,xml.etree.ElementTree as ET
from m5b_e6r2_common import *
TMP=Path('/tmp/m5b-e6r2-final-reproduction')
def run(cmd):
 r=subprocess.run(list(map(str,cmd)),capture_output=True,text=True);assert r.returncode==0,(cmd,r.stdout,r.stderr);return dict(command=list(map(str,cmd)),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr)
def canonical(path):
 s=path.read_text()
 # Only specifically identified creation-time records are non-geometric.
 rows=[]
 for l in s.splitlines():
  if l.startswith(('%TF.CreationDate,','; #@! TF.CreationDate,','; Creation date')):continue
  if l.startswith(('G04 Created by KiCad (PCBNEW','; DRILL file KiCad ')):
   l=re.sub(r' date \d{4}-\d\d-\d\d[ T]\d\d:\d\d:\d\d',' date <EXPORT_TIMESTAMP>',l)
  rows.append(l)
 return '\n'.join(rows)
def nets(path):
 tree=ET.parse(path);return dict(nets=sorted((n.get('name'),sorted((v.get('ref'),v.get('pin')) for v in n.findall('node'))) for n in tree.findall('./nets/net')),components=sorted((c.get('ref'),c.findtext('value'),c.findtext('footprint'),sorted((v.get('name'),v.text or '')for v in c.findall('./fields/field')))for c in tree.findall('./components/comp')))
def main():
 guard();before=sha(HW/'RF2M.kicad_pcb');TMP.mkdir(exist_ok=True);cmd=[]
 cmd.append(run(['kicad-cli','pcb','export','gerbers','-o',str(TMP)+'/', '--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts','--subtract-soldermask',HW/'RF2M.kicad_pcb']))
 cmd.append(run(['kicad-cli','pcb','export','drill','-o',str(TMP)+'/', '--format','excellon','--excellon-units','mm','--excellon-separate-th',HW/'RF2M.kicad_pcb']))
 cmd.append(run(['kicad-cli','sch','export','netlist','--format','kicadxml','-o',TMP/'RF2M.net.xml',HW/'RF2M.kicad_sch']))
 compare=[]
 for old in sorted((OUT/'gerbers').iterdir()):
  if old.suffix not in ['.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1','.drl']:continue
  fresh=TMP/old.name;assert fresh.exists(),fresh
  exact=old.read_bytes()==fresh.read_bytes();equivalent=canonical(old)==canonical(fresh);assert equivalent,('Actual CAM content differs',old.name)
  compare.append(dict(file=old.name,archived_SHA256=sha(old),fresh_SHA256=sha(fresh),classification='BYTE_IDENTICAL' if exact else 'IDENTICAL_GEOMETRY_CREATION_TIMESTAMP_ONLY'))
 assert len(compare)==11 and nets(OUT/'RF2M.net.xml')==nets(TMP/'RF2M.net.xml')
 assert before==sha(HW/'RF2M.kicad_pcb')
 # Independently bind source paste/mask geometry to actual freshly exported CAM.
 from m5b_e4r1_common import PASTE,SOLDER
 def regions(f):
  rows=[]
  for region in re.findall(r'G36\*.*?G37\*',f.read_text(),re.S):
   pts=[(int(x)/1e6,-int(y)/1e6)for x,y in re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',region)]
   if pts:rows.append((tuple([min(x for x,y in pts),min(y for x,y in pts),max(x for x,y in pts),max(y for x,y in pts)]),abs(sum(a[0]*b[1]-b[0]*a[1]for a,b in zip(pts,pts[1:]+pts[:1])))/2))
  return rows
 shift=lambda r:tuple(v-20 if i in [0,2]else v for i,v in enumerate(r));windows=[shift(r)for r in PASTE];opening=shift(SOLDER)
 found=[(r,a)for r,a in regions(TMP/'RF2M-F_Paste.gtp')if any(all(abs(u-v)<1e-5 for u,v in zip(r,q))for q in windows)]
 assert len(found)==5 and abs(sum(a for r,a in found)-6.765)<1e-5
 assert sum(all(abs(u-v)<1e-5 for u,v in zip(r,opening)) for r,a in regions(TMP/'RF2M-F_Mask.gts'))==1
 save('final-reproduction.json',dict(status='PASS',native_SHA256=before,commands=cmd,CAM_comparisons=compare,netlist_semantics_equal=True,source_paste_windows=5,source_paste_area_mm2=6.765,source_mask_mm=opening,output= str(TMP),archived_files_replaced=False,physical='NOT_RUN'))
 print('PASS fresh11CAMfiles,netlist,andcriticalsourcepaste/mask geometry')
if __name__=='__main__':main()
