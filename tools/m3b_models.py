#!/usr/bin/env python3
"""Dimension-envelope VRML for wound/custom parts; not manufacturer CAD."""
from pathlib import Path
import math
ROOT=Path(__file__).resolve().parents[1];D=ROOT/'hardware/80m/3dmodels'
def torus(ro,ri,h,color,center=(0,0,0),upright=False):
 verts=[];faces=[];N=48
 for z,r in [(-h/2,ri),(-h/2,ro),(h/2,ro),(h/2,ri)]:
  for i in range(N):
   a=2*math.pi*i/N;x,y=r*math.cos(a),r*math.sin(a);zz=z
   if upright:y,zz=-zz,y
   verts.append(tuple((v+c)/2.54 for v,c in zip((x,y,zz),center)))
 for ring in range(4):
  for i in range(N):faces.append([ring*N+i,ring*N+(i+1)%N,((ring+1)%4)*N+(i+1)%N,((ring+1)%4)*N+i,-1])
 vv=', '.join(' '.join(f'{x:.6f}'for x in v)for v in verts);ff=', '.join(' '.join(map(str,f))for f in faces)
 return f'Shape {{ appearance Appearance {{ material Material {{ diffuseColor {color} }} }} geometry IndexedFaceSet {{ solid FALSE coord Coordinate {{ point [ {vv} ] }} coordIndex [ {ff} ] }} }}\n'
def box(s,c,color):
 return 'Transform { translation '+' '.join(str(x/2.54)for x in c)+' children [ Shape { appearance Appearance { material Material { diffuseColor '+color+' } } geometry Box { size '+' '.join(str(x/2.54)for x in s)+' } } ] }\n'
def main():
 D.mkdir(exist_ok=True)
 for name,body in {
  'FT50A43_envelope':torus(7.35,2.96,8.35,'0.4 0.2 0.08',(0,-8,4.5)),
  'T60_2_flat_envelope':torus(8.8,3.1,8.3,'0.7 0.12 0.12',(0,0,4.6)),
  'T60_2_upright_envelope':torus(8.8,3.1,8.3,'0.7 0.12 0.12',(0,0,9.3),True),
  'SRP7050TA_envelope':box((7.6,6.9,5.0),(0,0,2.5),'0.22 0.22 0.22'),
  'Fuse467_envelope':box((1.70,.89,.44),(0,0,.25),'0.4 0.65 0.3'),
  'JST_VH_envelope':box((7.86,8.5,10.9),(1.98,-.55,5.45),'0.88 0.86 0.78'),
  'ABM3B_envelope':box((5.1,3.3,1.3),(0,0,.65),'0.62 0.62 0.62'),
  '78F_envelope':box((7.11,2.79,2.79),(0,0,1.8),'0.2 0.25 0.2'),
 }.items():(D/(name+'.wrl')).write_text('#VRML V2.0 utf8\n# ARDF-TX mechanical dimension envelope; NOT supplier CAD or validated winding geometry.\n'+body)
 print('Eight dimension-envelope VRML models generated')
if __name__=='__main__':main()
