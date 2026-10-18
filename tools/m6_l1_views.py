#!/usr/bin/python3
"""Original annotated vectors derived from actual native geometry, not mockups."""
import math,json,html,subprocess,ctypes as C
from pathlib import Path
import pcbnew as p
import m6_l1_rf as rf
P=rf.P;D=rf.D

def svgpath(q):
 paths=[]
 for i in range(q.OutlineCount()):
  for c in [q.Outline(i)]+[q.Hole(i,j) for j in range(q.HoleCount(i))]:
   paths.append('M '+' L '.join(f'{rf.mm(c.CPoint(k).x)},{rf.mm(c.CPoint(k).y)}' for k in range(c.PointCount()))+' Z')
 return ' '.join(paths)

def png(name,w,h):
 # Render the vector with installed librsvg/cairo, not an invented PCB image.
 r=C.CDLL('librsvg-2.so.2');c=C.CDLL('libcairo.so.2');g=C.CDLL('libgobject-2.0.so.0');V=C.c_void_p
 class Rect(C.Structure):_fields_=[('x',C.c_double),('y',C.c_double),('width',C.c_double),('height',C.c_double)]
 r.rsvg_handle_new_from_file.argtypes=[C.c_char_p,C.POINTER(V)];r.rsvg_handle_new_from_file.restype=V
 r.rsvg_handle_render_document.argtypes=[V,V,C.POINTER(Rect),C.POINTER(V)];r.rsvg_handle_render_document.restype=C.c_int
 c.cairo_image_surface_create.argtypes=[C.c_int,C.c_int,C.c_int];c.cairo_image_surface_create.restype=V
 c.cairo_create.argtypes=[V];c.cairo_create.restype=V
 c.cairo_surface_write_to_png.argtypes=[V,C.c_char_p]
 for method in ['cairo_destroy','cairo_surface_destroy']:getattr(c,method).argtypes=[V]
 g.g_object_unref.argtypes=[V]
 handle=r.rsvg_handle_new_from_file(str(D/name).encode(),None);assert handle
 surface=c.cairo_image_surface_create(0,w,h);context=c.cairo_create(surface)
 assert r.rsvg_handle_render_document(handle,context,C.byref(Rect(0,0,w,h)),None)
 assert c.cairo_surface_write_to_png(surface,str(D/name.replace('.svg','.png')).encode())==0
 c.cairo_destroy(context);c.cairo_surface_destroy(surface);g.g_object_unref(handle)

def main():
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
 for name,box in [('LoRa-native-overview.svg',(93,25,118,51)),('antenna-feed-detail.svg',(94,25.5,102,35.5))]:
  x,y,X,Y=box;s=[f'<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="{1200*(Y-y)/(X-x)}" viewBox="{x} {y} {X-x} {Y-y}"><rect x="{x}" y="{y}" width="{X-x}" height="{Y-y}" fill="#f8f8ef"/>','<g>']
  for layer,col in [(p.B_Cu,'#b5d8ed'),(p.F_Cu,'#bad3b0')]:
   clip=p.SHAPE_POLY_SET();pts=[rf.pt(x,y),rf.pt(X,y),rf.pt(X,Y),rf.pt(x,Y)];clip.NewOutline()
   for z in pts:clip.Append(z.x,z.y)
   for z in b.Zones():
    if z.GetIsRuleArea() or not z.IsOnLayer(layer):continue
    q=p.SHAPE_POLY_SET(z.GetFilledPolysList(layer));q.BooleanIntersection(clip);paths=[]
    for i in range(q.OutlineCount()):
     for c in [q.Outline(i)]+[q.Hole(i,j) for j in range(q.HoleCount(i))]:
      vv=[c.CPoint(k) for k in range(c.PointCount())]
      if vv:paths.append('M '+' L '.join(f'{rf.mm(a.x)},{rf.mm(a.y)}' for a in vv)+' Z')
    if paths:s.append(f'<path d="{" ".join(paths)}" fill="{col}" fill-rule="evenodd"/>')
  for r in ['U70','J7','C70','C71']:
   f=fs[r]
   for a in f.Pads():
    xx,yy=rf.mm(a.GetPosition().x),rf.mm(a.GetPosition().y);w,h=rf.mm(a.GetSize().x),rf.mm(a.GetSize().y)
    if f.GetOrientationDegrees()%180:w,h=h,w
    col='#e2a83b' if a.GetNetname()=='LORA_ANT' else '#778d52' if a.GetNetname()=='GND' else '#b99871'
    s.append(f'<rect x="{xx-w/2}" y="{yy-h/2}" width="{w}" height="{h}" fill="{col}" stroke="#333" stroke-width=".025"/><text x="{xx}" y="{yy+.12}" text-anchor="middle" font-size=".32">{a.GetNumber()}</text>')
  s.append('<path d="M97.89,33.75 L97.89,28.5" stroke="#cc7622" stroke-width=".45" fill="none"/>')
  for t in b.GetTracks():
   if isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND':
    xx,yy=rf.mm(t.GetPosition().x),rf.mm(t.GetPosition().y)
    if x<xx<X and y<yy<Y:s.append(f'<circle cx="{xx}" cy="{yy}" r=".4" fill="#557447"/><circle cx="{xx}" cy="{yy}" r=".15" fill="white"/>')
  s.append('<rect x="95.5" y="33.5" width="15" height="15" fill="none" stroke="#333" stroke-width=".08"/><circle cx="96.62" cy="48.25" r=".6" fill="none" stroke="red" stroke-width=".08"/><text x="100" y="40.5" font-size=".7">U70: 15 x 15 mm</text>')
  s.append('<rect x="98.315" y="27.55" width="2.2" height="1.9" fill="none" stroke="#b4346a" stroke-width=".06" stroke-dasharray=".2 .15"/><text x="94.1" y="26.2" font-size=".32">Top view: native pads / planes / vias</text><text x="94.1" y="26.9" font-size=".32">Blue bottom GND; green top GND</text><text x="94.1" y="30.4" font-size=".32">0.45 mm / 5.25 mm feed</text><text x="94.1" y="34.9" font-size=".32">Pink: U.FL underbody keep-out</text></g></svg>')
  (D/name).write_text(''.join(s)+'\n')
 # Both original figure orientations normalized as a newly drawn dimension diagram.
 s=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 80 36"><rect width="80" height="36" fill="white"/>']
 for k,title in enumerate(['TR4 V2 after 90deg CCW','TR8 V1 as drawn','TR8 V2 after 90deg CCW']):
  xx=5+26*k;yy=8;s.append(f'<text x="{xx-2}" y="3" font-size="1.4">{title}</text><rect x="{xx}" y="{yy}" width="15" height="15" fill="none" stroke="black" stroke-width=".15"/>')
  for i in range(1,23):
   x0=xx+1.12+1.27*(i-1 if i<=11 else 22-i);y0=yy+15 if i<=11 else yy
   s.append(f'<rect x="{x0-.4}" y="{y0-(1.37 if i<=11 else 0)}" width=".8" height="1.37" fill="#cba34f"/><text x="{x0}" y="{y0+2 if i<=11 else y0-1}" text-anchor="middle" font-size=".9">{i}</text>')
  s.append(f'<text x="{xx}" y="28" font-size="1.2">15 mm; pitch 1.27 mm</text>')
 s.append('<text x="3" y="33" font-size="1.1">Component top / carrier F.Cu view, X right, Y down. No mirror. Native pad centres lie 0.25 mm inside body edge.</text></svg>')
 (D/'normalized-module-views.svg').write_text(''.join(s)+'\n')
 # Before/after polygons from the frozen native board, not a schematic sketch.
 old=Path('/tmp/m6l1/baseline.kicad_pcb');old.parent.mkdir(exist_ok=True)
 old.write_bytes(subprocess.check_output(['git','show','742159d363dd8dd8b8ff653d01238af9a49ef2aa:hardware/controller/CTRL.kicad_pcb']))
 before=p.LoadBoard(str(old));s=['<svg xmlns="http://www.w3.org/2000/svg" width="1400" height="800" viewBox="0 0 8.6 4.9"><rect width="8.6" height="4.9" fill="white"/>']
 for i,(board,title) in enumerate([(before,'R1: unintended top GND'),(b,'L1: full keep-out')]):
  clip=p.SHAPE_POLY_SET();clip.NewOutline()
  for xx,yy in [(97.1,26.7),(100.9,26.7),(100.9,30.7),(97.1,30.7)]:clip.Append(p.FromMM(xx),p.FromMM(yy))
  s.append(f'<text x="{i*4.3+.1}" y=".22" font-size=".17">{title}</text><g transform="translate({i*4.3-97.1},-26.35)">')
  q=p.SHAPE_POLY_SET(next(z.GetFilledPolysList(p.F_Cu) for z in board.Zones() if not z.GetIsRuleArea() and z.IsOnLayer(p.F_Cu)));q.BooleanIntersection(clip)
  s.append(f'<path d="{svgpath(q)}" fill="#bad3b0" fill-rule="evenodd"/>')
  j=next(f for f in board.GetFootprints() if f.GetReference()=='J7')
  for a in j.Pads():s.append(f'<path d="{svgpath(rf.polygon(a,p.F_Cu))}" fill="'+('#e2a83b' if a.GetNumber()=='1' else '#778d52')+'"/>')
  s.append('<rect x="98.315" y="27.55" width="2.2" height="1.9" fill="none" stroke="#b4346a" stroke-width=".02" stroke-dasharray=".06 .04"/></g>')
 s.append('<text x=".1" y="4.75" font-size=".16">Pink: full Hirose no-traces rectangle, with intended SIG land. Removed GND area 0.02472 mm²; no signal change.</text></svg>')
 (D/'Hirose-keepout-comparison.svg').write_text(''.join(s)+'\n')
 for n,w,h in [('antenna-feed-detail.svg',960,1200),('LoRa-native-overview.svg',1000,1040),('normalized-module-views.svg',1600,720),('Hirose-keepout-comparison.svg',1400,800)]:png(n,w,h)
 print('Annotated native and normalized manufacturer-dimension views generated')
if __name__=='__main__':main()
