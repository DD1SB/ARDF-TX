#!/usr/bin/python3
# SPDX-License-Identifier: GPL-2.0-or-later
# Geometry test adapted from KiCad 10.0.6 drc_test_provider_sliver_checker.cpp.
# Copyright The KiCad Developers; adaptation ARDF-TX contributors, 2026.
# This script's license does not relicense the hardware design.
"""Read native filled copper and reproduce KiCad's coordinate-less sliver test.
The CLI DRC remains authoritative. No board modification or error suppression.
Source and algorithm provenance are recorded in M5B_E2_COPPER_CORRECTION.md.
"""
import pcbnew as p,math,json,argparse
from pathlib import Path

def polygons(b,layer=p.F_Cu):
 poly=p.SHAPE_POLY_SET()
 for t in b.GetTracks():
  if t.IsOnLayer(layer):t.TransformShapeToPolygon(poly,layer,0,p.FromMM(p.ARC_LOW_DEF_MM),p.ERROR_INSIDE)
 for f in b.GetFootprints():
  for item in list(f.Pads())+list(f.GraphicalItems()):
   if item.IsOnLayer(layer):item.TransformShapeToPolygon(poly,layer,0,p.FromMM(p.ARC_LOW_DEF_MM),p.ERROR_INSIDE)
 for item in b.GetDrawings():
  if item.IsOnLayer(layer):item.TransformShapeToPolygon(poly,layer,0,p.FromMM(p.ARC_LOW_DEF_MM),p.ERROR_INSIDE)
 for z in b.Zones():
  if not z.GetIsRuleArea()and z.IsOnLayer(layer):poly.Append(z.GetFilledPolysList(layer))
 poly.Simplify();return poly

def locate(poly):
 out=[];min_len=800
 for jj in range(poly.OutlineCount()):
  c=poly.Outline(jj);pts=[(c.CPoint(i).x,c.CPoint(i).y)for i in range(c.PointCount())];n=len(pts)
  def area(a,b,c):return(b[1]-a[1])*(c[0]-b[0])-(b[0]-a[0])*(c[1]-b[1])
  def inside(a,b):
   prev=(a-1)%n;next=(a+1)%n
   if area(pts[prev],pts[a],pts[next])<0:return area(pts[a],pts[b],pts[next])>=0 and area(pts[a],pts[prev],pts[b])>=0
   return area(pts[a],pts[b],pts[prev])<0 or area(pts[a],pts[next],pts[b])<0
  def sub(a,b):return(a[0]-b[0],a[1]-b[1])
  if n<=5:continue
  kk=0
  while kk<n:
   prior_index=(n+kk-1)%n;next_index=(kk+1)%n;pt=pts[kk];ptPrior=pts[prior_index];vPrior=sub(ptPrior,pt);forward_offset=1;offset=1
   while abs(vPrior[0])<min_len and abs(vPrior[1])<min_len and offset<n:
    pt=pts[(kk+offset)%n];offset+=1;vPrior=sub(ptPrior,pt)
   if offset>=n:break
   ptAfter=pts[next_index];vAfter=sub(ptAfter,pt)
   while abs(vAfter[0])<min_len and abs(vAfter[1])<min_len and forward_offset<n:
    next_index=(kk+forward_offset)%n;forward_offset+=1;ptAfter=pts[next_index];vAfter=sub(ptAfter,pt)
   kk+=offset
   if vPrior[0]*vAfter[0]+vPrior[1]*vAfter[1]<=0 or not inside(prior_index,next_index):continue
   included=sub(ptAfter,ptPrior);arm1=sum(a*a for a in vPrior);arm2=sum(a*a for a in vAfter);opp=sum(a*a for a in included)
   co=abs((opp-arm1-arm2)/(math.sqrt(arm1)*math.sqrt(arm2)))
   if co>2*math.cos(math.radians(20))and 2-co>1.1920928955078125e-7 and opp>80000**2:
    out.append(dict(outline=jj,vertex=kk-offset,point_mm=[v/1e6 for v in pt],prior_mm=[v/1e6 for v in ptPrior],after_mm=[v/1e6 for v in ptAfter],angle_deg=math.degrees(math.acos(co/2)),base_mm=math.sqrt(opp)/1e6))
 return out

def image(poly,path,title):
 from PIL import Image,ImageDraw
 # Same physical scale and crop in both images; actual native polygon union.
 im=Image.new('RGBA',(1400,940),'white');scale=200;origin=(54.5,66.5)
 def xy(v):return((p.ToMM(v.x)-origin[0])*scale+40,(p.ToMM(v.y)-origin[1])*scale+110)
 for i in range(poly.OutlineCount()):
  layer=Image.new('RGBA',im.size);d=ImageDraw.Draw(layer)
  c=poly.Outline(i);vs=[xy(c.CPoint(k))for k in range(c.PointCount())]
  if len(vs)>2:d.polygon(vs,fill='#ba4b31')
  for j in range(poly.HoleCount(i)):
   c=poly.Hole(i,j);d.polygon([xy(c.CPoint(k))for k in range(c.PointCount())],fill=(0,0,0,0))
  im.alpha_composite(layer)
 d=ImageDraw.Draw(im)
 # Annotation area is outside copper crop.
 d.rectangle((0,0,1400,100),fill='white');d.text((35,25),title,fill='black',font_size=27)
 d.text((35,65),'F.Cu native copper union | origin x54.5,y66.5 mm | 200 px/mm',fill='black',font_size=19)
 d.rectangle((0,900,1400,940),fill='white')
 d.text((35,915),'PACK_OK_N: 0.15 mm tracks; existing via at (57,68) mm, diameter 0.60 mm',fill='black',font_size=20)
 for x,y,label in [(57,68,'via'),(58.6,68.75,'U304.2')]:
  px=(x-origin[0])*scale+40;py=(y-origin[1])*scale+110;d.text((px+15,py+40),label,fill='black',font_size=22)
 if 'before'in path.name:
  px=(55.991446-origin[0])*scale+40;py=(68.075-origin[1])*scale+110
  d.ellipse((px-13,py-13,px+13,py+13),outline='#0055ff',width=4);d.text((70,160),'17.354 degree tip at (55.991446,68.075)',fill='#0055ff',font_size=21)
 im.save(path)

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('board');a.add_argument('report');a.add_argument('--image');x=a.parse_args();b=p.LoadBoard(x.board);poly=polygons(b);out=locate(poly);Path(x.report).write_text(json.dumps(dict(algorithm='KiCad10.0.6 default sliver thresholds:20deg,.08mm base,.0008mm skipped edge',findings=out),indent=2)+'\n')
 if x.image:image(poly,Path(x.image),'E1 before correction'if'before'in x.image else'E2 after correction')
 print('Coordinate reproduction:',len(out),'candidates',out)
