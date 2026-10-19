#!/usr/bin/python3
"""Common platform and ordinary metalwork, in board-local millimetres.

Own VRML models are clearance envelopes, not manufacturer STEP or machining
drawings. Frozen controller/RF80 sources are loaded read-only.
"""
import math,argparse
from m5b_e5_common import *
def mounts(board):
 fs={f.GetReference():f for f in board.GetFootprints()};return{r:xy(fs[r].GetPosition())for r in['H1','H2','H3','H4']}
def models(install=False):
 folder=HW/'ARDF_2M.3dshapes';folder.mkdir(exist_ok=True)
 def box(x,y,z,w,d,h,color=(.2,.2,.21),transparent=0):
  # Coordinates relative to the owning footprint; VRML uses .1-inch units.
  return f'Transform {{ translation {x/2.54:.7f} {-y/2.54:.7f} {z/2.54:.7f} children [ Shape {{ appearance Appearance {{ material Material {{ diffuseColor {color[0]} {color[1]} {color[2]} transparency {transparent} }} }} geometry Box {{ size {w/2.54:.7f} {d/2.54:.7f} {h/2.54:.7f} }} }} ] }}\n'
 text='#VRML V2.0 utf8\n# E5 envelope only. SK81 square base unchanged; fins run along boardX.\n'
 text+=box(0,18,-6.7,15,44,10,(.65,.67,.69))+box(0,38,-13.8,100,100,4)
 for i in range(21):text+=box(0,-10+4.8*i,-21.3,100,1,11)
 (folder/'E5_PA_cooling_envelope.wrl').write_text(text)
 text='#VRML V2.0 utf8\n# E5 SK10075SA75X40Y66Z envelope; fin detail illustrative. Passive channels alongX.\n# 15X20X5 stock spacer; no pressure on PA or transistor solder joints.\n'
 text+=box(2.54,-6,13,15,5,20,(.65,.67,.69))+box(2.54,-13.5,13,75,10,66)
 for i in range(13):text+=box(2.54,-33.5,-18+5*i,75,30,1)
 (folder/'E5_pass_cooling_envelope.wrl').write_text(text)
 text='#VRML V2.0 utf8\n# BD139 raised assembly envelope, not manufacturer STEP.8.5mm body standoff.\n# Helper heat sink is a conservative installed clearance box, not its fin profile.\n'
 text+=box(2.28,0,14.05,7.8,2.8,11.1,(.12,.12,.13))
 for x in[0,2.28,4.56]:text+=box(x,0,2.75,.8,.8,11.5,(.7,.7,.72))
 text+=box(2.28,-8.85,22,18,15,40,(.4,.4,.42),.55)
 (folder/'E5_BD139_assembly_envelope.wrl').write_text(text)
 if install:
  b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
  fs['H5'].Models().clear();m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/ARDF_2M.3dshapes/E5_PA_cooling_envelope.wrl';fs['H5'].Models().push_back(m)
  if not any('E5_pass_cooling' in m.m_Filename for m in fs['Q401'].Models()):
   m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/ARDF_2M.3dshapes/E5_pass_cooling_envelope.wrl';fs['Q401'].Models().push_back(m)
  fs['Q402'].Models().clear();m=p.FP_3DMODEL();m.m_Filename='${KIPRJMOD}/ARDF_2M.3dshapes/E5_BD139_assembly_envelope.wrl';fs['Q402'].Models().push_back(m)
  p.SaveBoard(str(HW/'RF2M.kicad_pcb'),b)
def main(draw=None):
 guard();models(False)
 rf=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));b80=p.LoadBoard(str(ROOT/'hardware/80m/production/RF80_V1.kicad_pcb'));ctl=p.LoadBoard(str(ROOT/'hardware/controller/CTRL.kicad_pcb'))
 mh=mounts(rf);m80=mounts(b80);assert sorted(mh.values())==sorted(m80.values());ch=mounts(ctl)
 rfholes=[(r,x-20,y-20,3.2)for r,(x,y)in mh.items()];controller=[(r,65+100-(x-20),20+100-(y-20),3.2)for r,(x,y)in ch.items()]
 contacts=[]
 for r,x,y,d in rfholes:contacts.append(dict(ref=r,centre_mm=[x,y],SK81_to_OD9_washer_mm=math.hypot(max(22-x,0,x-122),max(-y,0,y-100))-4.5))
 source='https://docs.rs-online.com/0660/0900766b80f3d711.pdf'
 helper='https://www.farnell.com/datasheets/17590.pdf'
 save('common-mechanical-platform.json',dict(status='DIMENSIONED_PROTOTYPE_ENVELOPES_NOT_FINAL_ENCLOSURE',RF_native_origin_mm=[20,20],RF_outline_mm=[150,110],RF_pattern_mm=[140,100],RF_native_holes_mm=mh,RF80_native_holes_mm=m80,controller_native_holes_mm=ch,controller_rotation_deg=180,controller_board_local_origin_mm=[65,20],controller_independent_posts_mm=[list(a[1:3])for a in controller],controller_bottom_Z_mm=53,carrier=dict(material='Unclad FR4 or stiff insulating sheet;no metal in antenna cutout',size_mm=[170,120,3],bottom_Z_mm=45,RF_corner_posts='40mmnylon +5mmspacer',controller_posts_mm=5,antenna_notch_mm=[109,110,162,120],front_notch_required=False),case_internal_study_mm=[180,200,125],case_bounds_mm=dict(X=[-10,170],Y=[-55,145],Z=[-40,85]),installed_gravity='UP=-boardX;both large heat sinks have channels alongX',USB='Socketface nearRF-localX165,Y100;5mmopenservicebay towallX170,20x12opening;actualplugfit NOT_RUN',ESP_antenna=dict(keepout_local_mm=[111,111.75,159,132.75],vertical_air_clearance_mm=15,RF_board_separation_mm=53,metal_carrier=False,physical='NOT_RUN'),LoRa='U.FL near(85.585,111.5);routeleft/rear outsideESPkeepout;band-specificantenna',PA=dict(sink='Fischer SK81 100 SA',sink_local_mm=[22,0,122,100],bar_mm=[15,44,10],bar_local_mm=[64.5,8,79.5,52],underside_projection_mm=25.2,lowest_Z_mm=-26.8,fin_rotation_deg=90,tap_coordinates_extrusion_uv_mm=[[12,50],[48,50]],washer_clearances=contacts,rotation_sensitivity_extra_K_W=.25,rotation_measured=False),pass_device=dict(MPN='ST D45H11',sink='Fischer SK10075SA',manufacturer_source=source,sink_dimensions_boardXYZ_mm=[75,40,66],sink_native_bounds_mm=[80.04,-22.5,-20,155.04,17.5,46],stock_spacer_mm=[15,20,5],spacer_native_bounds_mm=[110.04,17.5,3,125.04,22.5,23],spacer_drill_mm=4.,fastener='M3x12 +GS220Pmica +IB6shoulder;check4..6mmthreadengagement',heatsink_mount='Independently support with ordinaryM3brackets. Do not hang from transistor leads.',case_stop_C=60,orientation='75mm extrusion along boardX,not PCBnormal;natural convection withXupright',physical='NOT_RUN'),helper=dict(MPN='ST BD139',heatsink_candidate='Fischer FK213SA32 SOT32',manufacturer_source=helper,catalogue_dimensions_mm=[25.4,18,13],catalogue_K_W=21,installed_envelope_native_mm=[126.28,22.55,2,144.28,37.55,42],body_standoff_mm=8.5,installation='Orient shorterverticalprojectionbelowmountinghole;verifybottom>=2mm/top<=42mm andleadprotrusion>=1mm. GS32P +nylonM3fastener;noIB6forcedintopackage.',case_limit_C=80,source_risk='Exactholepattern/tolerances/retailfleetstock still require incomingverification;no guaranteedjoint claim',physical='NOT_RUN'),clearances=dict(PA_vs_pass_metal_Y_mm=2.5,pass_vs_helper_metal_Y_mm=5.05,helper_vs_carrier_Z_mm=3.,pass_vs_controller_plan_Y_mm=22.5),corner_hardware='InsulatingM3posts/washers;metalwasherOD9onlyatH5/H6barfixings',battery='External protected2S/4Spack baseline. Internalpack capacity/heat/fit not qualified.',IDC=dict(RF2M_initial_mm=150,RF80_initial_mm=220,construction='Straightpin1-to-pin1,keyed,half-twistwhereorientationrequires;continuitytestallpins',I2C_initial_max_Hz=100000,example_rise_us=.8473*4700*200e-12*1e6),RF_outputs='Side-access right-angle SMA/MMCXpigtails;PAcurrent on separatefusedharness',side_by_side_min_plane_mm=[260,110],optional_dual=dict(status='HOLD_FOR_CASE_THERMAL_EMC_INTEGRATION',RF80_top_Z_mm=55,controller_bottom_Z_mm=100,minimum_case_depth_mm=170,simultaneous_fullpower_required=False),physical='NOT_RUN'))
 # Simple conduction/spreading allowance;not a validated3Dthermal solution.
 spacer_R=.005/(150*100e-6);nominal_R=1.;conservative_R=1.5;loss=4.24
 save('pass-spacer-thermal.json',dict(status='CALCULATED_CONDITIONAL_NOT_MEASURED',spacer=dict(thickness_mm=5,minimum_effective_area_mm2=100,aluminium_k_assumed_W_mK=150,one_dimensional_R_K_W=spacer_R,mica_reference_R_K_W=.4,other_contacts_and_spreading_allowance_K_W=.5,conservative_total_selected_K_W=conservative_R),sink=dict(catalogue_K_W=1.9,nominal_K_W=1.9,conservative_K_W=2.85,derating='1.5xengineeringallowance,not manufacturer guarantee;bothchannelsupright'),pass_loss_case_W=loss,case_40C_nominal_C=40+loss*(1.9+nominal_R),case_40C_conservative_C=40+loss*(2.85+conservative_R),stop_C=60,rows=[dict(ambient_C=a,loss_W=q,nominal_case_C=a+q*(1.9+nominal_R),conservative_case_C=a+q*(2.85+conservative_R))for a in[25,40]for q in[2,3,4.24,5.5]],helper=dict(loss_bound_W=1.1,nominal_case_C=40+1.1*(21+1),nominal_junction_C=40+1.1*(21+1+10),conservative_case_C=40+1.1*(31.5+1.5),conservative_junction_C=40+1.1*(31.5+1.5+10),case_limit_C=80,physical='NOT_RUN'),limitations=['Insulator/tapfit,contactarea,flatnessandpreload unmeasured','Naturalconvectionand enclosureinlet temperature unqualified','A5Cairriseor5.5Wpassloss violates60Ccase envelope;stopandreview','Bothcollector tabsinsulated;no soldermask/greaseas insulation']))
 if not draw:return
 common=[('RF150x110',0,0,150,110),('Insulatingcarrier170x120,Z45',0,0,170,120),('Controller100x100,rot180,bottomZ53',65,20,100,100),('ESPantennaCLEAR/notch',111,111.75,48,21),('USBopenservicebay',165,94,10,12)]
 note=['All dimensions mm,RF-local origin=native(20,20). UP=-X in service.','RFmounts(5,5),(145,5),(145,105),(5,105);controllerindependentasymmetricalposts.','CarrierrearcutoutX109..162/Y110..120;40+5mmnylonposts,3mmsheet,5mmcontrollerposts.','No finalenclosure/thermal/antennaqualification. Externalprotectedpack baseline.']
 draw('common-controller-RF2M-top.svg',common+[('SK81below,channelsX',22,0,100,100),('SK100front,channelsX,Z-20..46',60.04,-42.5,75,40)],rfholes+controller,note,size=(200,245))
 draw('common-controller-RF80-top.svg',common+[('RF80 fullboard30mm service allowance (not qualified)',0,0,150,110)],rfholes+controller,note,size=(200,245))
 draw('RF2M-thermal-bottom-dimensions.svg',[('RF150x110',0,0,150,110),('SK81,100x100,finchannelsX',22,0,100,100),('Bar15x44',64.5,8,15,44),('Contact14x16',65,27,14,16)],rfholes+[('BAR1',72,12,3.3),('BAR2',72,48,3.3)],['Original98thermalvias +2newwashergroundvias outsidejoint;no extra thermalcredit.','SquareSK81 rotated90;tapextrusion(u,v)=(12,50),(48,50).','MinSK81-to-OD9cornerwasherclearance12.5mm.25.2mm belowPCB.'],size=(200,220))
 draw('pass-spacer-section.svg',[('SK100baseface',-22.5,-46,40,66),('Alstockspacer5mm',17.5,-23,5,20),('D45case/insulatingmica',22.5,-19,3.5,17),('PCB1.6,Y>=20',20,0,90,1.6),('SK81rear,belowPCB',20,11.8,100,15)],notes=['Sectionhorizontal=boardY,vertical=-Z;Q401pinrowY26.','PassbackfaceY17.5;PAfrontY20=>2.5mmmetal clearance.','15x20x5stockspacer,4mmclearancehole;GS220P/IB6 andM3x12.','Both heat sinks independentlysupported;no lead/solderjoint mountingload.'],size=(170,150))
 draw('common-stack-section.svg',[('RFPCB1.6',0,0,150,1.6),('PAbar10',64.5,1.7,15,10),('PAheatsink15',22,11.8,100,15),('Carrier3',0,-48,170,3),('ControllerPCB1.6',65,-54.6,100,1.6),('Controller20mmservice',65,-74.6,100,20)],notes=['RFtopZ0,PAminZ-26.8,casebackZ-40,caselidZ85.','CarrierbottomZ45,controllerbottomZ53. Caseinternal180x200x125.','FrontpasssinkZ-20..46,entirelyY<0,clearscarrier/controller.','HelperinstalledenvelopeZ2..42,carrierbottom45=>3mmnominalclearance.'],size=(200,180))
 draw('side-by-side-alternative.svg',[('RF150x110',0,0,150,110),('Controller100x100',160,0,100,100),('Passfrontbay',60.04,-42.5,75,40)],notes=['10mmgap=>260x110minimumboardplane;not the150x110common footprint.','A widercase~280x200x100isanalternative,nofactoryPCBchange.'],size=(295,230))
 draw('optional-dual-stack-section.svg',[('RF2MtopZ0',0,0,150,1.6),('SK81below25.2',22,1.6,100,25.2),('RF80topZ55',0,-55,150,1.6),('RF80service30',0,-85,150,30),('ControllerbottomZ100',65,-101.6,100,1.6),('Controller20mmservice',65,-121.6,100,20)],notes=['Optionaldualcase depth>=170mm;not the125mmprimaryshell.','Separatefusedpower,onebandactive;shared4Srequirescompatiblepopulations.','HOLDforairflow,RFshielding,thermalandserviceintegration.'],size=(200,220))
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--install-models',action='store_true');opt=a.parse_args();guard();models(opt.install_models);main()
