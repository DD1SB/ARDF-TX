#!/usr/bin/python3
"""Attach explicitly identified dimensional envelopes to custom RF landings.
These original VRML boxes are not qualified manufacturer STEP models. KiCad
renders the real PCB/copper and these physical envelopes without AI imagery.
"""
import json
from pathlib import Path
import m5a_r1_design as c
from m5b_pcb import P,D

MODELS={
 'PD54008L_ST_GDS_5x5':(5,5,1,0,0,'ST PD54008L-E Rev2 package; max envelope'),
 'PHA1_DF782_RevG':(4.6,4.24,1.6,0,2.12,'Mini-Circuits DF782 RevG max overall envelope; lead/flange detail omitted'),
 'TI_RNW0013A_4222804C':(3.5,3,.8,0,0,'TI RNW0013A package max envelope; isolated lands remain real copper'),
 'Bourns_SRP1265A':(14,12.8,6.5,0,0,'Bourns SRP1265A maximum dimensions'),
 'Coilcraft_1812SMS_Doc184':(4.95,6.35,4.2,0,0,'Coilcraft Doc184 overall coil envelope; solid box is not core material'),
 'Coilcraft_A05T_Doc107':(3.94,4.45,3.15,0,0,'Coilcraft Doc107 A05T overall coil envelope'),
 'Coilcraft_0603HC_Doc218':(1.8,1.12,1.172,0,0,'Coilcraft Doc218 body plus 0.152mm solder allowance'),
 'Coilcraft_1008CS_Doc101':(2.92,2.79,2.182,0,0,'Coilcraft Doc101 body plus 0.152mm solder allowance'),
 'CP_Panasonic_OSCON_C10':(6.3,6.3,9.9,0,0,'Panasonic25SVPG150M C10 maximum cylindrical envelope represented by box'),
 'WR_BHD_61202021621':(9.1,33.06,8.75,1.27,-11.43,'Wurth61202021621 drawing002.001 body envelope; cable/mate additional'),
}

def main():
 folder=P/'ARDF_2M.3dshapes';folder.mkdir(exist_ok=True);record=[]
 for name,(w,h,z,x,y,source)in MODELS.items():
  # KiCad VRML dimensions are 0.1 inch = 2.54mm. +y in model is -y PCB.
  scale=2.54
  text='#VRML V2.0 utf8\n# DIMENSIONAL ENVELOPE ONLY / NOT A MANUFACTURER MODEL\n'
  text+=f'Transform {{ translation {x/scale:.6f} {y/scale:.6f} {z/(2*scale):.6f} children [ Shape {{ appearance Appearance {{ material Material {{ diffuseColor 0.20 0.23 0.27 }} }} geometry Box {{ size {w/scale:.6f} {h/scale:.6f} {z/scale:.6f} }} }} ] }}\n'
  (folder/(name+'.wrl')).write_text(text)
  fp=P/'ARDF_2M.pretty'/(name+'.kicad_mod');s=c.parse(fp.read_text())
  if name=='TI_RNW0013A_4222804C':
   for mark in c.children(s,'fp_circle'):
    c.child(mark,'center')[1]=c.Atom('-2.5');c.child(mark,'end')[1]=c.Atom('-2.4')
  for old in list(c.children(s,'model')):s.remove(old)
  s.append(c.parse(f'(model "${{KIPRJMOD}}/ARDF_2M.3dshapes/{name}.wrl" (offset(xyz 0 0 0))(scale(xyz 1 1 1))(rotate(xyz 0 0 0)))'))
  fp.write_text(c.dump(s).replace('smd roundrect (at','smd roundrect(at')+'\n');record.append(dict(footprint=name,model=name+'.wrl',dimensions_mm=[w,h,z],status='SOURCED_DIMENSIONAL_ENVELOPE_NOT_QUALIFIED_STEP',source=source))
 board=P/'RF2M.kicad_pcb';s=c.parse(board.read_text())
 for f in c.children(s,'footprint'):
  name=f[1].split(':')[-1]
  if name not in MODELS:continue
  for old in list(c.children(f,'model')):f.remove(old)
  source=c.parse((P/'ARDF_2M.pretty'/(name+'.kicad_mod')).read_text());f.append(c.child(source,'model'))
 board.write_text(c.dump(s)+'\n')
 (D/'3D-model-status.json').write_text(json.dumps(dict(custom_models=record,standard_models='Installed KiCad10 library models are visualization aids, not manufacturer dimensional qualification.',remote_sensor='TH801 is two wires to a separately bonded insulated bead; no fictitious axial body.'),indent=2)+'\n')
 print('Attached',len(record),'identified custom dimensional envelopes')

if __name__=='__main__':main()
