"""Dimensioned solid thermal assembly. Project models use manufacturer envelopes;
formed leads/hardware are explicit workshop geometry, fin detail simplified.
"""
import math
import cadquery as cq
from m5b_e6r2_common import *
from m5b_e6r2_geometry import geometry
MODEL=HW/'ARDF_2M.3dshapes'
def box(bounds):
 x0,y0,z0,x1,y1,z1=bounds
 return cq.Workplane('XY').box(x1-x0,y1-y0,z1-z0).translate(((x0+x1)/2,(y0+y1)/2,(z0+z1)/2)).val()
def cyl(x,y,z,r,h):return cq.Solid.makeCylinder(r,h,cq.Vector(x,y,z))
def cut_holes(shape,holes,r,z,h):
 for x,y in holes:shape=shape.cut(cyl(x,y,z,r,h))
 return shape
def components():
 g=geometry();a={};colors={}
 def add(n,s,color):a[n]=s;colors[n]=color
 s=g['sink'];base=box([42,20,-11.9,142,120,-7.9])
 for x,y in g['source_bar']['holes']+ [d['hole'] for d in g['devices'].values()]:
  base=base.cut(cyl(x,y,-12,1.25 if x==133 else 1.5,4.3))
 for y in [22.0+i*4.8 for i in range(21)]:base=base.fuse(box([42,y-.85,-22.9,142,y+.85,-11.9]))
 # Side tapped holes in4mm base: ordinary hand drilling/tapping, not pockets.
 for x in [42.,142.]:
  for y in [40.,100.]:
   direction=cq.Vector(1 if x==42 else -1,0,0)
   base=base.cut(cq.Solid.makeCylinder(1.5,5,cq.Vector(x,y,-9.9),direction))
 add('SK81_100',base,(.14,.14,.15))
 bar=cut_holes(box(g['source_bar']['bounds']),g['source_bar']['holes'],1.65,-8,7)
 add('source_bar_15x44x6',bar,(.7,.72,.75))
 tim=cut_holes(box([84.5,28,-1.85,99.5,72,-1.6]),g['source_bar']['holes'],1.7,-2,.5)
 add('source_insulating_TIM',tim,(.25,.65,.45))
 for ref,d in g['devices'].items():
  x,y=d['hole'];w,l,t=d['mica_size'];top=y-d['mica_top_offset']
  mica=cut_holes(box([x-w/2,top,-7.875,x+w/2,top+l,-7.825]),[[x,y]],1.55,-8,1)
  add(ref+'_mica',mica,(.72,.63,.4))
  b=d['body_bounds'];body=box(b).cut(cyl(x,y,-8,1.9 if ref=='Q401' else 1.5,6))
  metal=box([b[0],b[1],b[2],b[3],b[4],b[2]+(1.3 if ref=='Q401' else .2)]).cut(cyl(x,y,-8,1.9 if ref=='Q401' else 1.5,3))
  if ref=='Q401':
   plastic=box([b[0],y+3.2,b[2]+1.3,b[3],b[4],b[5]])
  else:plastic=body.cut(metal)
  add(ref+'_tab',metal,(.68,.68,.7));add(ref+'_body',plastic,(.1,.1,.12))
  # Actual centreline bend,4.5mm supported straight before2mm radius.
  for i in [-1,0,1]:
   px=x+i*d['lead_pitch'];yb=b[4];z=d['lead_plane_Z'];bend=yb+4.5
   edges=[cq.Edge.makeLine(cq.Vector(px,yb,z),cq.Vector(px,bend,z)),
    cq.Edge.makeThreePointArc(cq.Vector(px,bend,z),cq.Vector(px,bend+math.sqrt(2),z+2-math.sqrt(2)),cq.Vector(px,bend+2,z+2)),
    cq.Edge.makeLine(cq.Vector(px,bend+2,z+2),cq.Vector(px,bend+2,1.))]
   wire=cq.Wire.assembleEdges(edges)
   lead=cq.Workplane('XZ',origin=(px,yb,z)).rect(d['lead_width'],d['lead_thickness']).sweep(cq.Workplane(obj=wire),transition='round').val()
   pin=(i+2) if ref=='Q401' else (2-i)
   add(ref+'_lead'+str(pin),lead,(.72,.72,.74))
  if ref=='Q401':
   # Tabfront=-6.5;IB6flange from-6.5 to-5.5,shoulder down1.2.
   shoulder=cyl(x,y,-7.7,1.75,1.2).fuse(cyl(x,y,-6.5,3,1)).cut(cyl(x,y,-7.8,1.55,2.5))
   add(ref+'_IB6',shoulder,(.8,.8,.72))
   screw=cyl(x,y,-11.5,1.5,6).fuse(cyl(x,y,-5.5,2.75,3))
   add(ref+'_M3x6',screw,(.55,.55,.58))
  else:
   washer=cyl(x,y,-4.9,2.5,.5).cut(cyl(x,y,-5,1.35,.8))
   screw=cyl(x,y,-10.4,1.25,6).fuse(cyl(x,y,-4.4,2.25,2))
   add(ref+'_PA66washer',washer,(.8,.8,.72));add(ref+'_M2p5x6_PA66',screw,(.8,.8,.72))
 for x in [42,142]:
  for y in [40,100]:
   left=x==42;x0,x1=(40,42) if left else (142,144);foot=[22,y-6,-33.6,42,y+6,-31.6] if left else [142,y-6,-33.6,162,y+6,-31.6]
   angle=box([x0,y-6,-33.6,x1,y+6,-3.6]).fuse(box(foot))
   angle=angle.cut(cq.Solid.makeCylinder(1.7,4,cq.Vector(x0-1,y,-9.9),cq.Vector(1,0,0)))
   angle=angle.cut(cyl(30 if left else 154,y,-34,1.7,4))
   add(f'bracket_{x}_{y}',angle,(.65,.67,.7))
   shaft_start=cq.Vector(x-2 if left else x-4,y,-9.9)
   screw=cq.Solid.makeCylinder(1.5,6,shaft_start,cq.Vector(1,0,0))
   head=cq.Solid.makeCylinder(2.75,3,cq.Vector(x-5 if left else x+2,y,-9.9),cq.Vector(1,0,0))
   add(f'support_M3_{x}_{y}',screw.fuse(head),(.5,.5,.53))
 for x,y in g['source_bar']['holes']:
  washer=cyl(x,y,0,4.5,.5).cut(cyl(x,y,-.1,1.6,.8));add(f'barwasher_{y}',washer,(.55,.55,.58))
  screw=cyl(x,y,-11.5,1.5,12).fuse(cyl(x,y,.5,2.75,3));add(f'bar_M3x12_{y}',screw,(.5,.5,.53))
 for x,y in g['independent_support']['foot_holes']:
  add(f'foot_M3x12_{x}_{y}',cyl(x,y,-43.6,1.5,12).fuse(cyl(x,y,-31.6,2.75,3)),(.5,.5,.53))
  add(f'foot_washer_{x}_{y}',cyl(x,y,-37.1,3.5,.5).cut(cyl(x,y,-37.2,1.6,.8)),(.55,.55,.58))
  nut=cq.Workplane('XY').polygon(6,5.5/math.cos(math.pi/6)).extrude(4).translate((x,y,-41.1)).val().cut(cyl(x,y,-41.2,1.5,4.2))
  add(f'foot_locknut_{x}_{y}',nut,(.55,.55,.58))
 return g,a,colors

def export_assembly(path,parts,colors,offset=(0,0,0),native=False):
 asm=cq.Assembly()
 for n,s in parts.items():
  shape=s.translate(offset)
  if native:shape=shape.mirror('XZ') # STEPmodelY is opposite native PCBscreenY.
  asm.add(shape,name=n,color=cq.Color(*colors[n]))
 asm.save(str(path))

def main():
 guard();MODEL.mkdir(exist_ok=True);g,parts,colors=components()
 for ref,d in g['devices'].items():
  own={k:v for k,v in parts.items() if k.startswith(ref+'_') and any(k.startswith(ref+'_'+s) for s in ['body','tab','lead'])}
  x,y=d['pin1'];export_assembly(MODEL/(ref+'_CommonPlane_E6R2.step'),own,colors,(-x,-y,0),native=True)
 cool={k:v for k,v in parts.items() if not (k.startswith('Q401_body') or k.startswith('Q401_tab') or k.startswith('Q401_lead') or k.startswith('Q402_body') or k.startswith('Q402_tab') or k.startswith('Q402_lead'))}
 export_assembly(MODEL/'E6R2_unified_cooling.step',cool,colors,(-92,-32,0),native=True)
 export_assembly(OUT/'mechanical/thermal-assembly.step',parts,colors)
 save('mechanical-source.json',g)
 save('solid-model-audit.json',dict(solids={k:dict(volume_mm3=v.Volume(),valid=v.isValid()) for k,v in parts.items()},
  details='Manufacturer maximum body/hole envelope; formed leads and mounting hardware are dimensioned project geometry. SK81 exterior/base accurate;21fins approximated, not machining profile.',
  units='mm',native_model_origin='Each TO device pin1;cooling H5=(92,32);native boardZ0',physical='NOT_RUN'))
 print('Dimensioned STEP models exported:',len(parts),'parts')

if __name__=='__main__':main()
