#!/usr/bin/python3
"""Dimensioned local before/after geometry from native KiCad pads, not a mockup."""
import math,html
from m4a_v1r1_common import *
from m4a_v1r1_fit import DATA

def path(q):
 s=[]
 for i in range(q.OutlineCount()):
  for c in [q.Outline(i)]+[q.Hole(i,j)for j in range(q.HoleCount(i))]:s.append('M '+' L '.join(f'{pcb.ToMM(c.CPoint(k).x)},{pcb.ToMM(c.CPoint(k).y)}'for k in range(c.PointCount()))+' Z')
 return ' '.join(s)
def main():
 frozen();b=pcb.LoadBoard(str(P/(NAME+'.kicad_pcb')));oldpath=Path('/tmp/m4av1r1/baseline.kicad_pcb');oldpath.write_bytes(gitfile('hardware/80m/production/RF80_V1.kicad_pcb'));old=pcb.LoadBoard(str(oldpath));s=['<svg xmlns="http://www.w3.org/2000/svg" width="1500" height="1260" viewBox="0 0 60 50.4"><rect width="60" height="50.4" fill="white"/><text x="1" y="1.5" font-size=".75">RF80 V1 to V1R1: actual pads, finished holes and top-view numbering</text>']
 for i,r in enumerate(['J101','J502','Q402','Q403','J301','J401']):
  xx=1+(i%2)*30;yy=3+(i//2)*15.5;s.append(f'<text x="{xx}" y="{yy}" font-size=".75">{r}: {html.escape(DATA[r]["mpn"])}</text>')
  for j,(board,title)in enumerate([(old,'V1'),(b,'V1R1')]):
   f=next(f for f in board.GetFootprints()if f.GetReference()==r);o=next(a for a in f.Pads()if a.GetNumber()=='1').GetPosition();ox,oy=pcb.ToMM(o.x),pcb.ToMM(o.y);dx=xx+2+12*j;dy=yy+4
   s.append(f'<text x="{dx-1}" y="{dy-2}" font-size=".65">{title} / drill {pcb.ToMM(list(f.Pads())[0].GetDrillSize().x):.2f}</text><g transform="translate({dx-ox},{dy-oy})">')
   for a in list(f.Pads())[:4 if r=='J101'else 99]:
    q=pcb.SHAPE_POLY_SET();a.TransformShapeToPolygon(q,pcb.F_Cu,0,pcb.FromMM(.002),pcb.ERROR_OUTSIDE);x,y=[pcb.ToMM(v)for v in a.GetPosition()]
    s.append(f'<path d="{path(q)}" fill="#b78e3e" stroke="#333" stroke-width=".025"/><circle cx="{x}" cy="{y}" r="{pcb.ToMM(a.GetDrillSize().x)/2}" fill="white" stroke="#444" stroke-width=".025"/><text x="{x}" y="{y+.15}" font-size=".45" text-anchor="middle">{a.GetNumber()}</text>')
   s.append('</g>')
  s.append(f'<text x="{xx}" y="{yy+12}" font-size=".53">Same lead centres/orientation/nets. J101 shows first4 of16.</text>')
 s.append('<text x="1" y="50" font-size=".55">Native-copper geometry and specified finished drills; not a photograph or fit measurement. Units mm.</text></svg>');(D/'finished-hole-comparison.svg').write_text(''.join(s)+'\n')
 print('Before/after native pad and finished-drill drawing generated')
if __name__=='__main__':main()
