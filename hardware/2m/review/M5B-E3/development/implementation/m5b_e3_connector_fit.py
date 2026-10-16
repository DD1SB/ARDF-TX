#!/usr/bin/python3
"""ConnectorholemarginforstandardJLCfinished-hole/boardtolerances."""
import pcbnew as p,json
import m5a_r1_design as c
from m5b_e3_common import *
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));data=json.loads((HW/'RF2M.electrical.json').read_text());parts={a['ref']:a for a in data['parts']};changes=[]
 for f in b.GetFootprints():
  ref=f.GetReference()
  if ref not in['J101','J301']:continue
  drill=1.3 if ref=='J101'else 1.8
  for a in f.Pads():
   a.SetDrillSize(p.VECTOR2I(p.FromMM(drill),p.FromMM(drill)))
   if ref=='J101':a.SetSize(p.VECTOR2I(p.FromMM(1.9),p.FromMM(1.9)))
  note=parts[ref]['note']
  if ref=='J101':note=note.replace('1.1mm drills','1.30mm drills').replace('1.10mm drills','1.30mm drills');note+=' E3:1.30mmfinishedhole/1.90mmland. WEmax0.79mmsquarelead diagonal1.117mm;JLCminhole1.22mm. Tailmin2.85mmminusboardmax1.76mm=1.09mmprotrusion.'
  else:note+=' E3:1.80mmfinishedhole(retainland),JLCminimum1.72mmversusnominal1.14mmsquarelead1.612mmdiagonal. JSTspecifies1.6mmboard;incomingfit/polarityinspectionrequired.'
  parts[ref]['note']=note
  for fld in f.GetFields():
   if fld.GetName()=='Engineering_Note':fld.SetText(note)
  z=p.FOOTPRINT(f);z.SetPosition(p.VECTOR2I(0,0));z.SetOrientationDegrees(0);z.SetReference('REF**')
  for a in z.Pads():a.SetNetCode(0)
  p.FootprintSave(str(HW/'ARDF_2M.pretty'),z);changes.append(dict(ref=ref,drill_mm=drill,MPN_unchanged=parts[ref]['mpn'],electrical_net_change=False))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);(HW/'RF2M.electrical.json').write_text(json.dumps(data,indent=2)+'\n')
 for fn in HW.glob('*.kicad_sch'):
  tree=c.parse(fn.read_text());changed=False
  for sym in c.children(tree,'symbol'):
   props={a[1]:a for a in c.children(sym,'property')};ref=props.get('Reference',[None,None,''])[2]
   if ref in['J101','J301']and'Engineering_Note'in props:props['Engineering_Note'][2]=parts[ref]['note'];changed=True
  if changed:fn.write_text(c.dump(tree)+'\n')
 save('connector-fit-changes.json',dict(changes=changes,manufacturer_evidence=dict(J101='https://www.we-online.com/components/products/datasheet/61202021621.pdf Rev002.0012026-08-30p1',J301='https://www.jst.com/wp-content/uploads/2025/06/eVH.pdf;p1applicablePCB1.6,p3square1.14;cachedE1PDFSHAinretainedsourcelog'),J501='Retained1.50mmcenter/1.70mmgroundholes;Amphenol132134catalog1.02mmsquaregroundlead/3.94mmtail;physicalincomingfitNOT_RUN'))
 print('J101/J301standardholemarginsupdated;pinmapsunchanged')
if __name__=='__main__':main()
