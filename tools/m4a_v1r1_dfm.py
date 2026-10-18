#!/usr/bin/python3
"""Independent RF80 native-geometry standard-JLCPCB gate and mutations."""
import types,copy
from m4a_v1r1_common import *
code=(R/'tools/m5b_e3_dfm.py').read_text().split('\ndef main():')[0]
code=code.replace('from m5b_e3_common import *','REV="M4A-V1R1"').replace('from m5b_e3_common import aliases','def aliases():return {}')
code=code.replace('edge[2]-edge[0]-180','edge[2]-edge[0]-150').replace('edge[3]-edge[1]-140','edge[3]-edge[1]-110')
code=code.replace('Congestedstandardvia;largerpreferredlandwouldencroachadjacentcopper;acceptedlocaldesignmarginexception,nofabricationexception','Existing0.60/0.30mmstandardviaretained;0.15mmannulusisordinaryprocess,notapremiumfabricationexception')
engine=types.ModuleType('rf80_v1r1_native_dfm');exec(code,engine.__dict__)
PROFILE=dict(revision=REV,retrieved=DATE,source_urls=['https://jlcpcb.com/capabilities/pcb-capabilities/','https://jlcpcb.com/help/article/difference-and-tolerance-explanation-between-via-and-pad-holes','https://jlcpcb.com/help/article/instructions-for-ordering','https://jlcpcb.com/help/article/jlcpcb-copper-weight'],
 order=dict(quantity=5,individual_boards=True,layers=2,thickness_mm=1.6,material='standard FR4',copper_oz=1,mask='green',legend='white',finish='Lead-free HASL',controlled_impedance=False,special_drilling=False,press_fit=False,premium_via_treatment=False),
 vendor_absolute=dict(track_space_mm=.10,SMD_pad_space_mm=.15,component_PTH_annulus_mm=.18,via_annulus_mm=.15,component_PTH_finished_tolerance_mm=[-.08,.13],hole_position_mm=.075,via_hole_tolerance='Electrical via, not a controlled component insertion hole; no finished-fit guarantee',via_hole_spacing_mm=.20,component_hole_spacing_mm=.45,mask_web_mm=.10,mask_to_foreign_copper_mm=.09,PTH_to_track_mm=.28,via_to_track_mm=.2,copper_to_edge_mm=.2,legend_height_mm=1,legend_stroke_mm=.15,legend_to_mask_mm=.15,outline_tolerance_mm=.2),
 design_margins=dict(track_space_min_mm=.15,component_PTH_annulus_mm=.25,existing_vias_mm=[.6,.3],mask_expansion_mm=.025,mask_web_mm=.1,edge_clearance_mm=.5,finished_hole_min_insertion_clearance_mm=.1),
 manual_review=['Actual incoming JST/Phoenix lead tolerance not published; engineering screening envelopes and dry-fit required, no factory special process','Ordinary HASL flatness/solder quality, winding forming and heatsink insulation remain physical checks','No guaranteed tent closure or plated-via thermal fill assumed','Quote/CAM and prototype transition require separate review and authorization'])
def evaluate(b,full=True,profile=None):
 profile=profile or PROFILE;r=engine.evaluate(b,profile,full)
 for k in ['controlled_impedance','special_drilling','press_fit','premium_via_treatment']:
  if profile['order'][k]:r['errors'].append(dict(check='no_premium_process',feature=k))
 if profile['vendor_absolute']['component_PTH_finished_tolerance_mm']!=[-.08,.13]:r['errors'].append(dict(check='ordinary_finished_hole_tolerance'))
 r['status']='FAIL'if r['errors']else'PASS_AUTOMATED_NATIVE_GEOMETRY';return r
def main():
 frozen();board=P/(NAME+'.kicad_pcb');r=evaluate(board);r['native_sha256']=sha(board);save('JLCPCB-standard-profile.json',PROFILE);save('JLCPCB-DFM.json',r)
 print(r['status'],len(r['errors']),r['statistics'],flush=True)
 if r['errors']:print(json.dumps(r['errors'][:30],indent=2));raise SystemExit(1)
 tests=[]
 def reject(label,fn,expected,full=False):
  b=pcb.LoadBoard(str(board));fn(b);x=evaluate(b,full);assert any(z['check']==expected for z in x['errors']),(label,x['errors']);tests.append(dict(mutation=label,detected=expected))
 reject('thin_special_board',lambda b:b.GetDesignSettings().SetBoardThickness(pcb.FromMM(.8)),'standard_1p6mm')
 reject('tiny_annulus',lambda b:next(t for t in b.GetTracks()if isinstance(t,pcb.PCB_VIA)).SetWidth(pcb.FromMM(.45)),'via_annulus_design_minimum')
 reject('microdrill',lambda b:next(t for t in b.GetTracks()if isinstance(t,pcb.PCB_VIA)).SetDrill(pcb.FromMM(.1)),'no_premium_micro_drill_or_small_land')
 reject('filled_via',lambda b:next(t for t in b.GetTracks()if isinstance(t,pcb.PCB_VIA)).SetFillingMode(pcb.FILLING_MODE_FILLED),'no_premium_via_protection')
 reject('blind_via',lambda b:next(t for t in b.GetTracks()if isinstance(t,pcb.PCB_VIA)).SetViaType(pcb.VIATYPE_BLIND),'ordinary_through_via')
 reject('thin_signal',lambda b:next(t for t in b.GetTracks()if not isinstance(t,pcb.PCB_VIA)).SetWidth(pcb.FromMM(.08)),'actual_track_width')
 reject('undersized_silk',lambda b:next(t for t in b.GetDrawings()if isinstance(t,pcb.PCB_TEXT)and t.GetLayer()==pcb.F_SilkS).SetTextHeight(pcb.FromMM(.8)),'legend_height')
 reject('thin_legend_stroke',lambda b:next(t for t in b.GetDrawings()if isinstance(t,pcb.PCB_TEXT)and t.GetLayer()==pcb.F_SilkS).SetTextThickness(pcb.FromMM(.1)),'legend_stroke')
 def gap(b):
  for xx in [167,167.55]:
   g=pcb.PCB_SHAPE(b);g.SetShape(pcb.SHAPE_T_RECT);g.SetStart(pcb.VECTOR2I(pcb.FromMM(xx),pcb.FromMM(126)));g.SetEnd(pcb.VECTOR2I(pcb.FromMM(xx+.5),pcb.FromMM(126.5)));g.SetLayer(pcb.F_Mask);g.SetFilled(True);g.SetWidth(0);b.Add(g)
 reject('real_mask_web_0p05',gap,'native_mask_web',True)
 for key in ['press_fit','special_drilling','controlled_impedance','premium_via_treatment']:
  profile=copy.deepcopy(PROFILE);profile['order'][key]=True;assert any(z['check']=='no_premium_process'for z in evaluate(pcb.LoadBoard(str(board)),False,profile)['errors']);tests.append(dict(mutation=key,detected='no_premium_process'))
 profile=copy.deepcopy(PROFILE);profile['vendor_absolute']['component_PTH_finished_tolerance_mm']=[-.05,.05];assert any(z['check']=='ordinary_finished_hole_tolerance'for z in evaluate(pcb.LoadBoard(str(board)),False,profile)['errors']);tests.append(dict(mutation='reintroduced_special_tolerance',detected='ordinary_finished_hole_tolerance'))
 save('DFM-regression.json',dict(status='PASS',mutations=tests));print('DFM negative cases',len(tests))
if __name__=='__main__':main()
