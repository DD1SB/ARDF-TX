"""Dimensioned source-coordinate mechanical drawings and actual solid views.
The fin profile and package plastic details are identified simplifications;
mounting/back/lead/hole/cutout dimensions are explicit design geometry.
"""
import math
import numpy as np
import matplotlib;matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle,Circle,FancyBboxPatch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import cadquery as cq
from m5b_e6r2_common import *
from m5b_e6r2_geometry import geometry
from m5b_e6r2_models import components,box,cyl,export_assembly
D=OUT/'mechanical'
def savefig(fig,name):
 fig.savefig(D/(name+'.pdf'),bbox_inches='tight');fig.savefig(D/(name+'.png'),dpi=160,bbox_inches='tight');plt.close(fig)
def outline(ax,rect,color,label=None,zorder=1):
 x0,y0,x1,y1=rect;ax.add_patch(Rectangle((x0,y0),x1-x0,y1-y0,fill=False,color=color,lw=1,zorder=zorder))
 if label:ax.text((x0+x1)/2,(y0+y1)/2,label,ha='center',va='center',fontsize=7,color=color)
def plan():
 g=geometry();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs=fps(b)
 fig,ax=plt.subplots(figsize=(12,9));outline(ax,[20,20,170,130],'green','')
 outline(ax,[42,20,142,120],'black','');outline(ax,[84.5,28,99.5,72],'orange','15 x44 x6 bar')
 for i,(x,y) in enumerate(g['PCB']['corner_holes']):ax.add_patch(Circle((x,y),1.6,fill=False));ax.text(x,y+4,f'H{i+1} ({x},{y})',fontsize=7,ha='center')
 for ref,d in g['devices'].items():
  x0,y0,x1,y1=d['cutout'];ax.add_patch(FancyBboxPatch((x0,y0),x1-x0,y1-y0,boxstyle='round,pad=0,rounding_size=1',fill=False,color='red'))
  bb=d['body_bounds'];outline(ax,[bb[0],bb[1],bb[3],bb[4]],'blue',ref+'\n'+d['part'])
  x,y=d['hole'];ax.add_patch(Circle((x,y),d['hole_diameter_min']/2,fill=False,color='blue'));ax.text(x,y-5,f'{ref} axis ({x:g},{y:g})',fontsize=7,ha='center')
  for a in fs[ref].Pads():
   x,y=xy(a.GetPosition());ax.add_patch(Circle((x,y),1,fill=False,color='green'));ax.text(x,y+2.5,a.GetNumber(),ha='center',fontsize=7)
 for x,y in g['source_bar']['holes']:ax.add_patch(Circle((x,y),1.6,fill=False,color='orange'));ax.text(x-5,y,f'M3 ({x:g},{y:g})',ha='right',fontsize=7)
 for h in g['independent_support']['side_taps']:ax.plot(h['X'],h['Y'],'kx');ax.text(h['X'],h['Y']+3,'side M3, Z=-9.9',ha='center',fontsize=6)
 for x,y in g['independent_support']['foot_holes']:ax.add_patch(Circle((x,y),1.7,fill=False));ax.text(x,y+4,f'foot ({x:g},{y:g})',fontsize=6,ha='center')
 ax.plot(92,55,'ro');ax.text(92,58,'Q501 unchanged (92,55)',fontsize=7,ha='center')
 ax.annotate('150 mm',xy=(20,136),xytext=(170,136),arrowprops={'arrowstyle':'<->'},ha='center');ax.text(95,139,'PCB150 x110; corner pattern140 x100; coordinates mm',ha='center',fontsize=9)
 ax.set(xlim=(14,177),ylim=(143,13),aspect='equal',xlabel='Native PCB X (mm)',ylabel='Native PCB Y (mm)',title='M5B-E6R2 common-heatsink mounting plan — PCB TOP projection')
 ax.grid(alpha=.15);savefig(fig,'dimensioned-mounting')
def solids():
 g,parts,colors=components();b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'))
 pcb=box(g['PCB']['bounds'])
 for d in g['devices'].values():
  x0,y0,x1,y1=d['cutout'];tool=cq.Workplane('XY').rect(x1-x0,y1-y0).extrude(3).edges('|Z').fillet(1).translate(((x0+x1)/2,(y0+y1)/2,-2)).val();pcb=pcb.cut(tool)
 for f in b.GetFootprints():
  for a in f.Pads():
   if a.GetDrillSize().x:
    x,y=xy(a.GetPosition());pcb=pcb.cut(cyl(x,y,-2,p.ToMM(a.GetDrillSize().x)/2,3))
 parts['RF2M_native_board']=pcb;colors['RF2M_native_board']=(.12,.42,.21)
 # Same5x5x1mm dimensional envelope as the preserved native Q501 WRL.
 # Die/junction geometry is not invented from the exterior package.
 parts['Q501_package_envelope']=box([89.5,52.5,0,94.5,57.5,1]);colors['Q501_package_envelope']=(.2,.23,.27)
 base=box([15,15,-36.6,185,135,-33.6])
 feet=[(20,20),(180,20),(180,130),(20,130)]
 for x,y in g['PCB']['corner_holes']+g['independent_support']['foot_holes']+feet:base=base.cut(cyl(x,y,-37,1.7,4))
 parts['insulating_carrier_170x120x3']=base;colors['insulating_carrier_170x120x3']=(.5,.5,.25)
 for i,(x,y) in enumerate(g['PCB']['corner_holes']):
  parts['PCB_post_'+str(i)]=cyl(x,y,-31.6,3,30).cut(cyl(x,y,-32,1.5,32));colors['PCB_post_'+str(i)]=(.8,.8,.72)
  parts['PCB_spacer_'+str(i)]=cyl(x,y,-33.6,3,2).cut(cyl(x,y,-34,1.6,3));colors['PCB_spacer_'+str(i)]=(.8,.8,.72)
  parts['PCB_top_PA66bolt_'+str(i)]=cyl(x,y,-7.5,1.5,8).fuse(cyl(x,y,.5,2.75,3));colors['PCB_top_PA66bolt_'+str(i)]=(.8,.8,.72)
  parts['PCB_top_PA66washer_'+str(i)]=cyl(x,y,0,3.5,.5).cut(cyl(x,y,-.1,1.6,.8));colors['PCB_top_PA66washer_'+str(i)]=(.8,.8,.72)
  parts['PCB_bottom_PA66bolt_'+str(i)]=cyl(x,y,-37.1,1.5,10).fuse(cyl(x,y,-40.1,2.75,3));colors['PCB_bottom_PA66bolt_'+str(i)]=(.8,.8,.72)
  parts['PCB_bottom_PA66washer_'+str(i)]=cyl(x,y,-37.1,3.5,.5).cut(cyl(x,y,-37.2,1.6,.8));colors['PCB_bottom_PA66washer_'+str(i)]=(.8,.8,.72)
 for i,(x,y) in enumerate(feet):
  parts['protected_foot_'+str(i)]=cyl(x,y,-51.6,3,15).cut(cyl(x,y,-52,1.5,16));colors['protected_foot_'+str(i)]=(.3,.3,.3)
  parts['foot_PA66bolt_'+str(i)]=cyl(x,y,-41.1,1.5,8).fuse(cyl(x,y,-33.1,2.75,3));colors['foot_PA66bolt_'+str(i)]=(.8,.8,.72)
  parts['foot_PA66washer_'+str(i)]=cyl(x,y,-33.6,3.5,.5).cut(cyl(x,y,-33.7,1.6,.8));colors['foot_PA66washer_'+str(i)]=(.8,.8,.72)
 # Read actual controller outline/holes; E5 carrier reference has controller
 # lower plane53mm above RF2M. Components remain in native KiCad render.
 cb=p.LoadBoard(str(ROOT/'hardware/controller/CTRL.kicad_pcb'));holeloc=[xy(f.GetPosition()) for f in cb.GetFootprints() if f.GetReference() in ['H1','H2','H3','H4']]
 # Preserve the E5 carrier's180deg transform and RF-local origin(65,20),
 # adding the RF native origin(20,20). NativeCTRL(x,y)->(205-x,160-y).
 ctrl=box([85,40,53,185,140,54.6]);controller_holes=[(205-x,160-y)for x,y in holeloc]
 for x,y in controller_holes:ctrl=ctrl.cut(cyl(x,y,52.5,1.6,3))
 parts['controller_stack_reference_M6L2']=ctrl;colors['controller_stack_reference_M6L2']=(.2,.5,.3)
 carrier=box([20,20,45,190,140,48]).cut(box([129,130,44,182,141,49]))
 for x,y in g['PCB']['corner_holes']+controller_holes:carrier=carrier.cut(cyl(x,y,44,1.7,5))
 parts['existing_upper_carrier_reference']=carrier;colors['existing_upper_carrier_reference']=(.65,.65,.4)
 for i,(x,y)in enumerate(controller_holes):
  parts['controller_reference_post_'+str(i)]=cyl(x,y,48,3,5).cut(cyl(x,y,47,1.5,7));colors['controller_reference_post_'+str(i)]=(.8,.8,.72)
 export_assembly(D/'complete-mechanical-stack.step',parts,colors)
 # Validate actual solid intersections at all deliberately insulating faces.
 pairs=[]
 for ref in ['Q401','Q402']:
  for tab in [ref+'_tab',ref+'_body']:
   for sink in ['SK81_100','source_bar_15x44x6']:
    vol=parts[tab].intersect(parts[sink]).Volume();assert vol<1e-6,(tab,sink,vol);pairs.append(dict(a=tab,b=sink,intersection_mm3=vol))
  assert parts['RF2M_native_board'].intersect(parts[ref+'_body']).Volume()<1e-6
 for name in parts:
  assert parts[name].isValid(),name
 for name,part in parts.items():
  if name.startswith('bracket_'):
   assert part.intersect(base).Volume()<1e-6,('Bracket/carrier collision',name)
   assert part.intersect(parts['RF2M_native_board']).Volume()<1e-6,('Bracket/PCB collision',name)
 assert parts['Q401_M3x6'].intersect(parts['Q401_tab']).Volume()<1e-6,'Steel screw/live tab contact'
 for name,part in parts.items():
  if name.startswith('protected_foot_'):
   for screw,solid in parts.items():
    if screw.startswith('PCB_bottom_PA66bolt_'):assert part.intersect(solid).Volume()<1e-6,('Foot/post bolt collision',name,screw)
 # Actual rejected solid placements exercise collision checks, not a report flag.
 wrong_base=base.translate((0,0,2));overlap=sum(s.intersect(wrong_base).Volume() for n,s in parts.items() if n.startswith('bracket_'));assert overlap>10
 live_touch=parts['Q401_tab'].translate((0,0,-.15)).intersect(parts['SK81_100']).Volume();assert live_touch>1
 assert min(geometry()['devices'][r]['back_Z'] for r in ['Q401','Q402'])>-7.9
 save('mechanical-solid-checks.json',dict(status='PASS_DIMENSIONED_SOLIDS',insulated_contact_pairs=pairs,parts=len(parts),negative_solid_tests=[dict(name='carrier2mmtoo_high',intersection_mm3=overlap),dict(name='live_tab_moved_through_insulator',intersection_mm3=live_touch)],PCB_cutouts='Actual native component/NPTH drills and cutouts; via holes omitted from mechanical envelope, present in native3D/CAM',controller='Read-only native board holes; envelope at53mm per preserved carrier reference, full components in native board renders',physical='NOT_RUN'))
 return g,parts,colors

def view(parts,colors,name,elev=25,azim=-55,explode=False,controller=False):
 fig=plt.figure(figsize=(11,9));ax=fig.add_subplot(111,projection='3d');limits=[]
 for n,s in parts.items():
  if ('controller_' in n or 'upper_carrier_' in n) and not controller:continue
  if explode:
   dz=30 if n=='RF2M_native_board' or n.startswith('PCB_post') else -25 if n.startswith('SK81') or n.startswith('bracket') else 10 if n.startswith('Q') else 0
   s=s.translate((0,0,dz))
  vertices,tri=s.tessellate(.3,.4);v=np.array([[q.x,q.y,q.z] for q in vertices]);limits.extend(v.tolist());polys=v[np.array(tri)]
  ax.add_collection3d(Poly3DCollection(polys,facecolor=colors[n],edgecolor=(0,0,0,.08),linewidth=.08,alpha=.78 if n=='RF2M_native_board' else 1))
 limits=np.array(limits);lo=limits.min(0);hi=limits.max(0);ax.set(xlim=(lo[0],hi[0]),ylim=(hi[1],lo[1]),zlim=(lo[2],hi[2]));ax.set_box_aspect(hi-lo);ax.view_init(elev,azim);ax.set(xlabel='X mm',ylabel='Y mm',zlabel='Z mm',title='E6R2 '+name.replace('-',' ')+'\nDimensioned solids; fin/plastic detail simplified; not physical qualification');savefig(fig,name)
def section(parts,colors,axis,coord,name):
 fig,ax=plt.subplots(figsize=(12,5))
 # True section via solid common with a0.02mm slab; project vertices only.
 slab=box([coord-.01,0,-60,coord+.01,150,10]) if axis=='X' else box([0,coord-.01,-60,190,coord+.01,10])
 for n,s in parts.items():
  if 'controller' in n:continue
  cut=s.intersect(slab)
  for face in cut.Faces():
   pts=[v.toTuple() for v in face.Vertices()]
   if len(pts)<3:continue
   xx=[v[1 if axis=='X' else 0] for v in pts];zz=[v[2] for v in pts]
   ax.fill(xx,zz,color=colors[n],alpha=.75);ax.plot(xx,zz,color='black',lw=.3)
 ax.axhline(-7.9,color='r',ls='--',lw=.7,label='Common aluminum mounting plane Z=-7.9')
 ax.axhline(-1.6,color='g',ls=':',lw=.7,label='PCB bottom Z=-1.6')
 ax.set(xlabel=('Y' if axis=='X' else 'X')+' (mm)',ylabel='Z (mm)',title=f'E6R2 {name}; section {axis}={coord:g} mm',ylim=(-55,7),aspect='equal');ax.legend(fontsize=7,loc='lower right');ax.grid(alpha=.15);savefig(fig,name)
def plots():
 s=OUT/'simulation/BUCK4S-beta60-normal-8ms.csv'
 if not s.exists():return
 z=np.loadtxt(s,delimiter=',',skiprows=1);fig,ax=plt.subplots(3,1,figsize=(11,8),sharex=True)
 ax[0].plot(z[:,0]*1000,z[:,4],label='VPA');ax[0].plot(z[:,0]*1000,z[:,6],label='MMIC5V');ax[0].legend();ax[0].set_ylabel('V')
 ax[1].plot(z[:,0]*1000,z[:,10]/.068,label='Regulated rail');ax[1].plot(z[:,0]*1000,z[:,11]/.05,label='PA drain shunt');ax[1].legend();ax[1].set_ylabel('A')
 ax[2].plot(z[:,0]*1000,z[:,9],label='CLOCK_OFF');ax[2].plot(z[:,0]*1000,z[:,12],label='Slot bias');ax[2].legend();ax[2].set(xlabel='Time ms',ylabel='V')
 fig.suptitle('Native-value ngspice envelope model — assumed BJT/load parameters; RF NOT_RUN');savefig(fig,'keying-transient')
def main():
 guard();D.mkdir(exist_ok=True);plan();g,parts,colors=solids();view(parts,colors,'complete-isometric');view(parts,colors,'exploded-cooling',explode=True);view(parts,colors,'carrier-stack',controller=True);view(parts,colors,'underside',elev=-35)
 section(parts,colors,'X',92,'section-Q501');section(parts,colors,'Y',28,'section-Q401-Q402');section(parts,colors,'X',116,'section-Q401');section(parts,colors,'X',133,'section-Q402');plots();print('PASS drawings/sections/complete-stack solids')
if __name__=='__main__':main()
