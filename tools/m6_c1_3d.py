#!/usr/bin/python3
"""Original dimension-only envelopes where vendor/stock STEP is unavailable.
These are not manufacturer-qualified models; actual KiCad render remains CAD.
"""
import json
from pathlib import Path
import pcbnew as p
from m5_2m_design import parse,dump,child
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1'
def main():
 folder=P/'ARDF_CTL.3dshapes';folder.mkdir(exist_ok=True);b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};record=[]
 for r,name,w,l,h,cx,cy in [('U20','RV3032_envelope',3.2,1.5,.8,0,0),('J4','WR_BHD16_envelope',8.86,23.88,9.1,1.27,8.89),('J5','WR_BHD20_envelope',8.86,28.96,9.1,1.27,11.43)]:
  text='#VRML V2.0 utf8\n# DIMENSIONAL ENVELOPE ONLY / NOT MANUFACTURER STEP\n'
  text+=f'Transform {{ translation {cx/2.54} {-cy/2.54} {h/5.08} children [ Shape {{ appearance Appearance {{ material Material {{ diffuseColor .2 .22 .24 }} }} geometry Box {{ size {w/2.54} {l/2.54} {h/2.54} }} }} ] }}\n';(folder/(name+'.wrl')).write_text(text)
  filename='${KIPRJMOD}/ARDF_CTL.3dshapes/'+name+'.wrl';fp=fs[r]
  if not any(m.m_Filename==filename for m in fp.Models()):
   m=p.FP_3DMODEL();m.m_Filename=filename;fp.Models().push_back(m)
  lib=P/'ARDF_CTL.pretty'/(str(fp.GetFPID().GetLibItemName())+'.kicad_mod');sx=parse(lib.read_text())
  if not any(isinstance(x,list) and x and x[0]=='model' and x[1]==filename for x in sx):sx.append(parse('(model "'+filename+'" (offset(xyz 0 0 0))(scale(xyz 1 1 1))(rotate(xyz 0 0 0)))'));lib.write_text(dump(sx)+'\n')
  record.append({'ref':r,'dimensions_mm':[w,l,h],'model':filename,'status':'DIMENSION_ONLY_ENVELOPE_NOT_QUALIFIED_STEP'})
 p.SaveBoard(str(P/'CTRL.kicad_pcb'),b);(D/'3D-model-status.json').write_text(json.dumps({'envelopes':record,'other_models':'Stock KiCad STEP references retained where supplied. LoRa body height/identity remains OPEN; DNP option has no qualified model.','physical_fit':'NOT_RUN'},indent=2)+'\n')
if __name__=='__main__':main()
