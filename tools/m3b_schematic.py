#!/usr/bin/env python3
"""M3B evaluation additions to the existing RF80 hierarchy; no orders."""
import json
from pathlib import Path
from m3_80m_design import build,footprints,parse,dump,child,children,Atom
ROOT=Path(__file__).resolve().parents[1];HW=ROOT/'hardware/80m'
def design():
 d=build(m3b=True)
 old={p['ref']:p for p in json.loads((HW/'review/M3A-R1/RF80.electrical.json').read_text())['parts']}
 # Retain dated sourcing observations; never relabel a historical price current.
 for r,p in d.parts.items():
  if r in old and p['mpn']==old[r]['mpn']:
   for k in ('price_breaks_eur','evidence','supplier','supplier_part_number','availability','source_url','moq','multiple'):p[k]=old[r][k]
 d.parts['F301'].update(footprint='ARDF_TX:Fuse_467_0603',note='CORRECTED R1 footprint: actual467 family is0603. Own maker reflow lands2.54x1.02mm outer/gap0.36mm; retain1.5A32V, nominalI2t0.0766A2s. Fuse nuisance/pack coordination physical gate.',source_url='https://www.littelfuse.com/assetdocs/fuse-467-datasheet?assetguid=4a59f034-1cca-460e-a5ba-e1e66247c76d')
 d.parts['J101'].update(footprint='ARDF_TX:Wurth_61201621621',note='Maker61201621621:27.98mm length,17.78mm span,2.54mm pitch; hole recommendation1.1+/-0.15mm. M3B finished hole1.2mm/pads1.9mm, within recommendation; review board finished-hole tolerance. Same pinout/keying.')
 d.parts['Q402'].update(footprint='ARDF_TX:TO220_Vertical_1p3Drill',note=d.parts['Q402']['note']+' M3B:1.3mm finished holes/1.905mm lands,2.54mm pitch. Conservative fit against Vishay TO220AB envelope max lead1.01x0.61mm diagonal1.18mm; exact incoming IRF610 lead dry-fit still required.')
 d.parts['C314'].update(mpn='CC0603KRX7R9BB104',price_breaks_eur={'1':.035},evidence='ESTIMATE',source_url='https://yageogroup.com/download/specsheet/CC0603KRX7R9BB104',supplier_part_number='OPEN',note='50V version on undamped VIN_PACK node; avoids crediting the downstream damper for upstream capacitor voltage.100n±10%X7R0603; price estimate, current basketOPEN.')
 d.parts['T401'].update(footprint='ARDF_TX:FT50A43_Inline_4Terminal',note=d.parts['T401']['note']+' M3B formed leads on one edge:1,2,3,4 at5.08mm pitch;2/3 adjacent for short center join. Same core, turns, polarity and ratio; mechanical forming only.')
 s=d.sheet('12_evaluation','12 Evaluation input damper and low-capacitance probe access')
 s.text('M3B-E1: bounded12.0-16.8V protected4S only; first bring-up uses a CURRENT-LIMITED LAB SUPPLY.\nR350/C350 damp cable L<=10uH; pack sense remains ahead of R350. TVS is NOT an18V clamp.\nNo driver fitted until power-only OV withdrawal test proves VDRV<=12.6V. No physical tests performed.',15,22)
 s.place('R350','R','1.5 ohm / 1W',{'1':'VIN_PACK','2':'VIN_PA'},65,65,'Resistor_SMD:R_2512_6332Metric','CRCW25121R50FKEG','input_damper','NORMAL',price={'1':.15},source='https://www.vishay.com/docs/20035/dcrcwe3.pdf',supplier='Vishay/Mouser',code='OPEN',note='±1%; full PA supply damper.0.6A gives0.54W active/0.108W at20%; rated hot derating and insertion pulse must qualify. Not a universal overvoltage limiter.')
 s.place('C350','C_Polarized','100u / 35V',{'1':'VIN_PA','2':'GND'},175,65,'Capacitor_THT:CP_Radial_D8.0mm_P3.50mm','EEUFR1V101','input_damper','NORMAL',price={'1':.45},source='https://na.industrial.panasonic.com/products/capacitors/aluminum-electrolytic-capacitors/aluminum-electrolytic-capacitors-radial-lead-type/series/83367/model/83807',supplier='Panasonic/Mouser',code='OPEN; exact manufacturer MPN EEUFR1V101',note='FR100u35V±20%,8x11.5mm/P3.5mm,lead0.6mm. ESR/impedance0.056ohm at100kHz20C. Cmin80u used; no guaranteed extra ceramic capacitance credited. Inrush/ESR/temp remain physical gates.')
 s.place('C405','C','100n / 50V',{'1':'VPA_SHAPED','2':'GND'},285,65,'Capacitor_SMD:C_0805_2012Metric','GRM21BR71H104KA01L','normal_rf_bypass','NORMAL',price={'1':.10},source='https://www.murata.com/en-eu/products/productdetail?partno=GRM21BR71H104KA01L',note='Local transformer-feed RF bypass; NOT a drain reservoir.100n is negligible vs22u shaper integration but gives~0.45ohm at3.55MHz. RF ripple/heating/key-edge effect require measurement. X7R±10%; procurement quoteOPEN.')
 # Small pads: no permanent pin headers or coax stubs on drain/fast timing nodes.
 nets=['VBAT','VIN_PACK','VIN_PA','VPA','VPA_ISO','VPA_LOAD','VDRV','I_PA_RAW','I_PA_FILTER','FB_PA','PA_PERMIT','FOX_PERMIT','PA_INB','ARM','ARM_ACCEPT','ARM_CLK','ARMED','RESET_N','HEALTH_N','POR_N','LEASE','LEASE_OK','BUS_QUIET','PA_GUARD_RAW','PWR0','PWR1','SEL_EXT','SEL_FULL','PATH_PA','PATH_FOX','KEY_TAIL','FAULT_N','CLK_PA','CLK_FOX','GATE_DRV','GATE_PA','DRAIN_PA','VPA_SHAPED','RF_RAW','RF_NORMAL','FOX_SUM','FOX_PAD_IN','RF_FOX','VFOX','TEMP_SENSE','TEMP_HOT_REF','V_PA_OV','V_PACK_SCALED','GND','GND','GND','GND']
 for i,net in enumerate(nets):
  ref='TP'+str(700+i);col=i%9;row=i//9
  s.place(ref,'TestPoint',net,{'1':net},24+col*43,105+row*24,'ARDF_TX:Probe_Pad_0p8','PCB copper','evaluation_access','BOTH',price={'1':0},evidence='BOARD_FEATURE',note='Evaluation-only bare pad; active probe<=1pF for reset/drain, adjacent ground spring. No permanent connector purchase.')
 s.text('Population stages are assembly instructions, not bypasses of hardware interlocks.\nTH301 electrical sensor is remotely bonded to insulated PA case via test pads; do not fit a second NTC in parallel.\nR403 zero-ohm can be removed to isolate the gate driver during dummy-load tests.\nDo not inject28V into this board.16.8V failed-buck test uses rated surrogate load with U401/Q402 absent.',15,255,1.05)
 return d

def main():
 d=design();d.save();footprints()
 pp=HW/'RF80.kicad_pro';pj=json.loads(pp.read_text());pj['net_settings']['classes'][0]['clearance']=.15;pp.write_text(json.dumps(pj,indent=2)+'\n')
 # Freeze the standard body/keying, with maker-qualified hand-assembly holes.
 f=parse(Path('/usr/share/kicad/footprints/Connector_IDC.pretty/IDC-Header_2x08_P2.54mm_Vertical.kicad_mod').read_text());f[1]='Wurth_61201621621'
 for pad in children(f,'pad'):
  child(pad,'drill')[1]=Atom('1.2');sz=child(pad,'size');sz[1]=Atom('1.9');sz[2]=Atom('1.9')
 (HW/'ARDF_TX.pretty/Wurth_61201621621.kicad_mod').write_text(dump(f)+'\n')
 # Conservative hand-assembly drill; electrical pad spacing/body/model unchanged.
 f=parse(Path('/usr/share/kicad/footprints/Package_TO_SOT_THT.pretty/TO-220-3_Vertical.kicad_mod').read_text());f[1]='TO220_Vertical_1p3Drill'
 for pad in children(f,'pad'):child(pad,'drill')[1]=Atom('1.3')
 (HW/'ARDF_TX.pretty/TO220_Vertical_1p3Drill.kicad_mod').write_text(dump(f)+'\n')
 # Actual maker reflow land: length2.54, gap0.36, width1.02 mm.
 p=HW/'ARDF_TX.pretty/Fuse_467_0603.kicad_mod'
 (HW/'ARDF_TX.pretty/Probe_Pad_0p8.kicad_mod').write_text('''(footprint "Probe_Pad_0p8"(version 20240108)(generator "pcbnew")(layer "F.Cu")(attr smd exclude_from_bom exclude_from_pos_files)
(property "Reference" "REF**"(at 0 -1.2 0)(layer "F.SilkS")(effects(font(size 0.7 0.7)(thickness 0.12))))
(property "Value" "Probe"(at 0 1.2 0)(layer "F.Fab")(effects(font(size 0.7 0.7)(thickness 0.12))))
(fp_circle(center 0 0)(end 0.65 0)(stroke(width 0.05)(type default))(fill none)(layer "F.CrtYd"))
(pad "1" smd circle(at 0 0)(size 0.8 0.8)(layers "F.Cu" "F.Mask")))
''')
 p.write_text('''(footprint "Fuse_467_0603" (version 20240108) (generator "pcbnew") (layer "F.Cu") (descr "Littelfuse4670603; manufacturer p3 reflow lands; outer2.54 gap0.36 width1.02mm") (attr smd)
(property "Reference" "REF**" (at 0 -1.5 0) (layer "F.SilkS") (effects (font (size 0.8 0.8)(thickness 0.12))))
(property "Value" "Fuse_467_0603" (at 0 1.5 0) (layer "F.Fab") (effects (font (size 0.8 0.8)(thickness 0.12))))
(fp_rect (start -0.85 -0.45)(end 0.85 0.45)(stroke(width 0.1)(type default))(fill none)(layer "F.Fab"))
(fp_rect (start -1.52 -0.76)(end 1.52 0.76)(stroke(width 0.05)(type default))(fill none)(layer "F.CrtYd"))
(pad "1" smd rect (at -0.725 0)(size 1.09 1.02)(layers "F.Cu" "F.Paste" "F.Mask"))
(pad "2" smd rect (at 0.725 0)(size 1.09 1.02)(layers "F.Cu" "F.Paste" "F.Mask")))
''')
 (HW/'ARDF_TX.pretty/FT50A43_Inline_4Terminal.kicad_mod').write_text('''(footprint "FT50A43_Inline_4Terminal" (version 20240108)(generator "pcbnew")(layer "F.Cu")(attr through_hole)
(descr "FT50A43 unchanged9T bifilar; own formed-lead fixture5.08mm pitch1Astart2Afinish3Bstart4Bfinish;2+3center")
(property "Reference" "REF**"(at 0 -3 0)(layer "F.SilkS")(effects(font(size 1 1)(thickness 0.15))))
(property "Value" "9T+9T FT50A43"(at 0 17 0)(layer "F.Fab")(effects(font(size 1 1)(thickness 0.15))))
(fp_rect(start -8.8 -1.6)(end 8.8 16)(stroke(width 0.05)(type default))(fill none)(layer "F.CrtYd"))
(fp_circle(center 0 8)(end 6.35 8)(stroke(width 0.12)(type default))(fill none)(layer "F.SilkS"))
(fp_circle(center 0 8)(end 6.35 8)(stroke(width 0.1)(type default))(fill none)(layer "F.Fab"))
(pad "1" thru_hole rect(at -7.62 0)(size 2.2 2.2)(drill 1)(layers "*.Cu" "*.Mask"))
(pad "2" thru_hole circle(at -2.54 0)(size 2.2 2.2)(drill 1)(layers "*.Cu" "*.Mask"))
(pad "3" thru_hole circle(at 2.54 0)(size 2.2 2.2)(drill 1)(layers "*.Cu" "*.Mask"))
(pad "4" thru_hole circle(at 7.62 0)(size 2.2 2.2)(drill 1)(layers "*.Cu" "*.Mask")))
''')
 print('M3B-E1 schematic:',len(d.sheets)+1,'pages;',len(d.parts),'references; original R1 control nets unchanged')
if __name__=='__main__':main()
