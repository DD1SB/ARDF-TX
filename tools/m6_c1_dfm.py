#!/usr/bin/python3
"""Controller-specific native-geometry JLC gate, reusing frozen polygon engine."""
import json,types,hashlib,copy
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1'
code=(ROOT/'tools/m5b_e3_dfm.py').read_text().split('\ndef main():')[0]
code=code.replace('from m5b_e3_common import *','REV="M6-C1"').replace('from m5b_e3_common import aliases','def aliases():return {}')
code=code.replace('edge[2]-edge[0]-180','edge[2]-edge[0]-100').replace('edge[3]-edge[1]-140','edge[3]-edge[1]-100')
mod=types.ModuleType('m6_native_geometry');exec(code,mod.__dict__)
PROFILE={'revision':'M6-C1','retrieved':'2026-10-18','source_urls':['https://jlcpcb.com/capabilities/pcb-capabilities/','https://jlcpcb.com/help/article/jlcpcb-copper-weight'],
 'order':{'layers':2,'thickness_mm':1.6,'material':'standard FR4','copper_oz':1,'mask':'green','legend':'white','finish':'Lead-free HASL','via_treatment':'ordinary unfilled through-vias; no guaranteed tent closure','controlled_impedance':False},
 'vendor_absolute':{'track_space_mm':.1,'SMD_pad_space_mm':.15,'PTH_annulus_mm':.18,'PTH_hole_to_track_mm':.28,'via_to_track_mm':.2,'mask_web_mm':.1,'mask_to_foreign_copper_mm':.09,'copper_to_edge_mm':.2,'NPTH_min_mm':.5,'plated_slot_width_min_mm':.5,'legend_height_mm':1,'legend_stroke_mm':.15,'hole_size_tolerance_mm':[-.08,.13],'hole_position_mm':.075,'thickness_tolerance_percent':10},
 'design_margins':{'track_min_mm':.15,'track_typical_mm':.2,'space_min_mm':.15,'via_land_drill_mm':[.8,.3],'annulus_mm':.25,'edge_clearance_mm':.5,'mask_expansion_mm':.03},
 'manual_review':['HASL/reflow quality on RTC and ESP32 lands; no physical assembly yet','Check connector mating/cable polarity, finished-hole fit against actual parts','Optional LoRa module identity/land-pattern tolerance hold; DNP base variants','USB full-speed eye/routing and power enumeration measurements NOT_RUN','No factory CAM or commercial quote has been requested']}
def evaluate(board,full=True):
    r=mod.evaluate(board,PROFILE,full)
    return r
def main():
    (D/'JLCPCB-standard-profile.json').write_text(json.dumps(PROFILE,indent=2)+'\n')
    board=P/'CTRL.kicad_pcb';r=evaluate(board);r['native_sha256']=hashlib.sha256(board.read_bytes()).hexdigest();(D/'JLCPCB-DFM.json').write_text(json.dumps(r,indent=2)+'\n')
    print(r['status'],'errors',len(r['errors']),r['statistics'])
    if r['errors']:print(json.dumps(r['errors'][:20],indent=2));raise SystemExit(1)
    tests=[];b=p.LoadBoard(str(board));ds=b.GetDesignSettings()
    def fails(name,action,restore,key):
        action();z=evaluate(b,False);restore();assert any(e['check']==key for e in z['errors']),name;tests.append({'mutation':name,'detected':key})
    old=ds.GetBoardThickness();fails('0p8mm_special_stackup',lambda:ds.SetBoardThickness(p.FromMM(.8)),lambda:ds.SetBoardThickness(old),'standard_1p6mm')
    via=next(t for t in b.GetTracks() if isinstance(t,p.PCB_VIA));old=via.GetWidth(p.F_Cu);fails('small_annulus',lambda:via.SetWidth(p.FromMM(.45)),lambda:via.SetWidth(old),'via_annulus_design_minimum')
    old=via.GetDrillValue();fails('microdrill',lambda:via.SetDrill(p.FromMM(.1)),lambda:via.SetDrill(old),'no_premium_micro_drill_or_small_land')
    old=via.GetFillingMode();fails('premium_filled_via',lambda:via.SetFillingMode(p.FILLING_MODE_FILLED),lambda:via.SetFillingMode(old),'no_premium_via_protection')
    old=via.GetViaType();fails('blind_via',lambda:via.SetViaType(p.VIATYPE_BLIND),lambda:via.SetViaType(old),'ordinary_through_via')
    tr=next(t for t in b.GetTracks() if not isinstance(t,p.PCB_VIA));old=tr.GetWidth();fails('thin_track',lambda:tr.SetWidth(p.FromMM(.08)),lambda:tr.SetWidth(old),'actual_track_width')
    # Spatial mutations use real native geometry. Never saved over candidate.
    test_tracks=[]
    for y,net in [(117,'V3V3'),(117.2,'GND')]:
        t=p.PCB_TRACK(b);t.SetStart(p.VECTOR2I(p.FromMM(108),p.FromMM(y)));t.SetEnd(p.VECTOR2I(p.FromMM(111),p.FromMM(y)));t.SetWidth(p.FromMM(.15));t.SetLayer(p.F_Cu);t.SetNet(b.FindNet(net));b.Add(t);test_tracks.append(t)
    z=evaluate(b);assert any(e['check']=='native_foreign_copper_clearance' for e in z['errors']);tests.append({'mutation':'real_0p05mm_copper_gap','detected':'native_foreign_copper_clearance'})
    (D/'DFM-regression.json').write_text(json.dumps({'status':'PASS','mutations':tests},indent=2)+'\n')
if __name__=='__main__':main()
