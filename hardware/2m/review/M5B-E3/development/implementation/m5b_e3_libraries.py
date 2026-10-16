#!/usr/bin/python3
"""Make documented E3 legend adaptations real local library footprints.
Copper, drills, pin numbering and mechanical envelopes are retained exactly.
Thin supplier artwork is retained onFab;manufacturableboardlegend isseparate.
"""
import pcbnew as p,json,re,copy
import m5a_r1_design as c
from m5b_e3_common import *
def main():
 guard();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));data=json.loads((HW/'RF2M.electrical.json').read_text());parts={a['ref']:a for a in data['parts']};changes=[];done={};lib=HW/'ARDF_2M.pretty'
 for f in b.GetFootprints():
  orig=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName());ref=f.GetReference()
  if ref.startswith('TL')or ref in ['TP601','TP602','TP603','TP604']:continue
  oldmeta=json.loads((OUT/'legend-library-delta.json').read_text())if(OUT/'legend-library-delta.json').exists()else{'changes':[]}
  original=next((z['before']for z in oldmeta['changes']if z['ref']==ref),orig)
  name=original.split(':')[1]if original.startswith('ARDF_2M:')else original.split(':')[1]+'_E3'
  new='ARDF_2M:'+name
  if name not in done:
   z=p.FOOTPRINT(f);z.SetPosition(p.VECTOR2I(0,0));z.SetOrientationDegrees(0);z.SetFPID(p.LIB_ID('ARDF_2M',name));z.SetReference('REF**');z.SetValue(name)
   # Board-specific user fields and padnets do not belong in reusablelibrary.
   for pad in z.Pads():pad.SetNetCode(0)
   p.FootprintSave(str(lib),z);done[name]=True
  f.SetFPID(p.LIB_ID('ARDF_2M',name));
  if ref in parts:parts[ref]['footprint']=new
  changes.append(dict(ref=ref,before=orig,after=new,change='Legend-onlylocalvariant;padcopper/drillsandmanufacturerpinorderunchanged'))
 p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b);(HW/'RF2M.electrical.json').write_text(json.dumps(data,indent=2)+'\n')
 for fn in HW.glob('*.kicad_sch'):
  tree=c.parse(fn.read_text());changed=False
  for sym in c.children(tree,'symbol'):
   props={a[1]:a for a in c.children(sym,'property')};ref=props.get('Reference',[None,None,''])[2]
   if ref in parts and'Footprint'in props and props['Footprint'][2]!=parts[ref]['footprint']:props['Footprint'][2]=parts[ref]['footprint'];changed=True
  if changed:fn.write_text(c.dump(tree)+'\n')
 save('legend-library-delta.json',dict(unique_footprints=len(done),changes=changes,qualification='Copperanddrillgeometrycomparisonsandrelevantpinassertionsrequired;manufactureridentityunchanged.'))
 print('Local legendlibraryvariants',len(done))
if __name__=='__main__':main()
