"""Shared mounting geometry fixed before copper changes; millimetres, PCBtop Z0."""
from m5b_e6r2_common import *
SINK=dict(part='Fischer SK81 100 SA',bounds=[42.,20.,-22.9,142.,120.,-7.9],base_thickness=4.,mass_g=214.,fin_axis='X')
BAR=dict(bounds=[84.5,28.,-7.85,99.5,72.,-1.85],dimensions=[15.,44.,6.],holes=[[92.,32.],[92.,68.]],TIM_thickness=.25,grease_to_sink=.05)
DEVICES={
 'Q401':dict(part='ST D45H11',hole=[116.,28.],hole_diameter_min=3.75,body_width_max=10.4,body_length_max=15.75,hole_from_top=2.95,thickness_max=4.6,lead_pitch=2.54,lead_back_offset=2.5,lead_width=.88,lead_thickness=.70,available_lead_min=13.,
  footprint='TO220_Flat_CommonPlane_E6R2',cutout=[109.5,23.,122.5,42.3],mica='Fischer GS220P',mica_size=[12.,18.,.05],mica_top_offset=4.,screw='M3x6 steel + Fischer IB6',bush=dict(flange_OD=6.,bore=3.1,shoulder_OD=3.5,shoulder_length=1.2,flange_thickness=1.),tab_potential='VPA_PRE',tab_thickness=[1.23,1.32]),
 'Q402':dict(part='ST BD139',hole=[133.,27.5],hole_diameter_min=2.9,body_width_max=7.8,body_length_max=11.05,hole_from_top=3.8,thickness_max=2.9,lead_pitch=2.28,lead_back_offset=1.27,lead_width=.88,lead_thickness=.63,available_lead_min=15.3,
  footprint='TO126_Flat_CommonPlane_E6R2',cutout=[128.,22.5,138.,37.],mica='Fischer GS220P',mica_size=[12.,18.,.05],mica_top_offset=4.,screw='M2.5x6 PA66 + PA66 washer OD5/ID2.7/thickness0.5',tab_potential='MOD_SINK',tab_thickness=[2.4,2.9])}
def geometry():
 import math
 for r,d in DEVICES.items():
  x,y=d['hole'];d['back_Z']=-7.8 # mica50um+totalgrease50um
  d['lead_plane_Z']=d['back_Z']+d['lead_back_offset']
  d['body_bounds']=[x-d['body_width_max']/2,y-d['hole_from_top'],d['back_Z'],x+d['body_width_max']/2,y-d['hole_from_top']+d['body_length_max'],d['back_Z']+d['thickness_max']]
  d['bend_radius_center']=2.;d['straight_before_bend']=4.5
  d['pinrow_Y']=d['body_bounds'][4]+4.5+2.
  # ST front-side view: TO2201B-2C-3E; SOT32/BD1393E-2C-1B.
  # Both packages lie frontup/backdown, leads toward increasing nativeY.
  d['lead_step']=d['lead_pitch'] if r=='Q401' else -d['lead_pitch']
  d['pin1']=[x-d['lead_step'],d['pinrow_Y']]
  d['physical_left_to_right']=[1,2,3] if r=='Q401' else [3,2,1]
  d['lead_path_to_1mm_tip']=4.5+math.pi+1.-d['lead_plane_Z']-2.
  assert d['lead_path_to_1mm_tip']<d['available_lead_min']
  assert d['body_bounds'][5]<-1.6
 return dict(revision=REV,PCB=dict(bounds=[20,20,-1.6,170,130,0],corner_holes=[[25,25],[165,25],[165,125],[25,125]],thickness=1.6),
  sink=SINK,source_bar=BAR,devices=DEVICES,cutout_radius=1.,
  independent_support=dict(material='Al angle30x20x2mm,12mm wide,4pieces',side_taps=[dict(X=x,Y=y,Z=-9.9,axis='X',thread='M3',engagement=4.) for x in [42.,142.] for y in [40.,100.]],
   foot_holes=[[x,y] for x in [30.,154.] for y in [40.,100.]],angle_top_Z=-3.6,base_inner_Z=-33.6,PCB_posts='30mm insulating M3 +2mm insulating spacer at four existing corners',side_screws='4xM3x6 steel, from outside; enclosure shell fitted last',foot_screws='4xM3x12 with washer and4mm-high locknut through2mmangle+3mmcarrier',
   ground_bond='H6 native exposed ground land/washer and controlled ground strap; remove anodizing only at designated bond. Verify lead-compensated resistance.'),
  common_plane_Z=-7.9,assembly_mass_g_estimate=[248,270],TC_locations={'PA_source_adjacent':[97.,60.5,0.],'Q401_case':[116.,36.,-3.2],'Q402_case':[133.,31.,-4.9],'heatsink':[105.,75.,-7.9]},
  physical='NOT_RUN',CAD_basis='Manufacturer max package envelopes and independently modeled ordinary hardware; power-package lead forms are project geometry, not manufacturer preformed parts')
if __name__=='__main__':guard();save('mechanical-source.json',geometry());print('Common mounting plane established before routing')
