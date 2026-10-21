#!/usr/bin/env python3
"""Export this independent project. No uploads, ordering, programming or RF."""
import subprocess,zipfile,json,csv,tempfile
from pathlib import Path
P=Path(__file__).resolve().parents[1];B=P/'Mini80.kicad_pcb';F=P/'fabrication';R=P/'review';A=P/'assembly'
def run(*a):subprocess.run(list(map(str,a)),check=True)
def main():
 for d in [F,F/'gerbers',F/'stencil',R,A]:d.mkdir(exist_ok=True)
 run('kicad-cli','sch','export','pdf','--output',R/'Mini80-schematic.pdf',P/'Mini80.kicad_sch')
 run('kicad-cli','sch','export','netlist','--format','kicadxml','--output',R/'netlist.xml',P/'Mini80.kicad_sch')
 run('kicad-cli','pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen,Edge.Cuts','--subtract-soldermask','--check-zones','--output',F/'gerbers',B)
 run('kicad-cli','pcb','export','drill','--format','excellon','--excellon-units','mm','--excellon-separate-th','--generate-map','--generate-report','--report-path',F/'drill-report.txt','--output',F/'gerbers',B)
 # Remove DNP bodies from a disposable copy, so the supplied bench stencil
 # needs no tape over unused antenna-bank apertures. Copper CAD stays intact.
 import pcbnew as pcb
 with tempfile.TemporaryDirectory(prefix='mini80-stencil-')as td:
  tb=pcb.LoadBoard(str(B));removed=[]
  for fp in list(tb.GetFootprints()):
   if fp.IsDNP():tb.Remove(fp);removed.append(fp)
  temp=Path(td)/B.name;pcb.SaveBoard(str(temp),tb)
  run('kicad-cli','pcb','export','gerbers','--layers','F.Paste,B.Paste,Edge.Cuts','--output',F/'stencil',temp)
 run('kicad-cli','pcb','export','pdf','--layers','F.Fab','--common-layers','Edge.Cuts','--crossout-DNP-footprints-on-fab-layers','--mode-single','--scale','4','--output',A/'Mini80-top-assembly.pdf',B)
 run('kicad-cli','pcb','export','pdf','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Silkscreen,B.Silkscreen','--common-layers','Edge.Cuts','--mode-multipage','--scale','4','--output',R/'Mini80-copper-mask-silk.pdf',B)
 run('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--smd-only','--exclude-dnp','--output',A/'MINI50-bench-positions.csv',B)
 with (A/'MINI50-bench-positions.csv').open()as f:pos=list(csv.DictReader(f))
 # JLC review coordinates: board lower-left=(0,0), X right, Y up.
 with (A/'JLC-bench-centroids-REVIEW.csv').open('w')as f:
  w=csv.writer(f);w.writerow(['Designator','Mid X','Mid Y','Layer','Rotation'])
  for row in pos:w.writerow([row['Ref'],f"{float(row['PosX'])-50:.6f}mm",f"{float(row['PosY'])+85:.6f}mm",'Top',row['Rot']])
 for variant in ['MINI50-bench','FOX10-bench']:
  with (A/(variant+'-BOM.csv')).open()as f:parts=list(csv.DictReader(f))
  with (A/('JLC-'+variant+'-BOM-REVIEW.csv')).open('w')as f:
   w=csv.writer(f);w.writerow(['Comment','Designator','Footprint','LCSC Part #','Manufacturer Part Number'])
   for row in parts:
    if row['population']!='DNP':w.writerow([row['value'],row['ref'],row['footprint'],{'U1':'C62244','U2':'C2842395','Q1':'C110499','Q2':'C110499','Q4':'C110499','C6':'C1525','C11':'C1525','C12':'C1525','C15':'C1525'}.get(row['ref'],''),row['mpn']])
 for folder,name in [('gerbers','Mini80-M80-E1-JLCPCB-bare.zip'),('stencil','Mini80-M80-E1-stencil.zip')]:
  with zipfile.ZipFile(F/name,'w',zipfile.ZIP_DEFLATED)as z:
   for f in sorted((F/folder).iterdir()):z.write(f,f.name)
 print('Exports complete. These packages have not been submitted to a manufacturer.')
if __name__=='__main__':main()
