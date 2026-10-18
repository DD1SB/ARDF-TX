#!/usr/bin/python3
"""Controller-only land patterns; vendor documents in source/package audit."""
from pathlib import Path
import pcbnew as pcb
P=Path(__file__).resolve().parents[1]/'hardware/controller';F=P/'ARDF_CTL.pretty';MM=pcb.FromMM
def write():
    F.mkdir(parents=True,exist_ok=True)
    removed=[]
    for lib,original,name in [('Connector_JST','JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical','JST_XH_B3B_Standard'),('Connector_PinHeader_2.54mm','PinHeader_1x03_P2.54mm_Vertical','UART_61300311121')]:
        f=pcb.FootprintLoad('/usr/share/kicad/footprints/'+lib+'.pretty',original);f.SetFPID(pcb.LIB_ID('ARDF_CTL',name))
        for a in f.Pads():a.SetDrillSize(pcb.VECTOR2I(MM(1.1),MM(1.1)))
        f.SetLibDescription('Standard JLC finished hole1.10nominal ->1.02..1.23. JST XH0.64square leads, enlarged hard-FR4 soldering hole (JST layout guideline note2); UART Wurth recommended1.1+/-0.15. No press-fit/tight custom tolerance. Inspect first mating parts.')
        pcb.PCB_IO_KICAD_SEXPR().FootprintSave(str(F),f)
    f=pcb.FootprintLoad('/usr/share/kicad/footprints/RF_Module.pretty','ESP32-S3-WROOM-1')
    f.SetFPID(pcb.LIB_ID('ARDF_CTL','ESP32_S3_WROOM_1_Standard'))
    for p in list(f.Pads()):
        if p.GetAttribute()==pcb.PAD_ATTRIB_PTH:removed.append(p);f.Remove(p)
    f.SetLibDescription('Espressif WROOM-1 manufacturer land geometry; KiCad optional0.2mm thermal PTH removed. All SMD pad41 lands retained. Ground stitching OUTSIDE hidden solder land, ordinary reflow. No filled/tented via assumption.')
    pcb.PCB_IO_KICAD_SEXPR().FootprintSave(str(F),f)
    f=pcb.FootprintLoad('/usr/share/kicad/footprints/Connector_USB.pretty','USB_C_Receptacle_GCT_USB4105-xx-A_16P_TopMnt_Horizontal');f.SetFPID(pcb.LIB_ID('ARDF_CTL','USB4105_Standard'))
    for p in f.Pads():
        if p.GetNumber()=='SH':p.SetSize(pcb.VECTOR2I(p.GetSize().x+MM(.1),p.GetSize().y+MM(.1)))
        if p.GetNumber() in ['A1','B12','A12','B1']:
            # Local land end trim: 1.15->1.05, back edge remains unchanged;
            # gives locator-hole/copper clearance >0.25mm. Tail width unchanged.
            p.SetSize(pcb.VECTOR2I(p.GetSize().x,MM(1.05)));p.SetPosition(pcb.VECTOR2I(p.GetPosition().x,p.GetPosition().y-MM(.05)))
    pcb.PCB_IO_KICAD_SEXPR().FootprintSave(str(F),f)
    f=pcb.FootprintLoad('/usr/share/kicad/footprints/Connector_Coaxial.pretty','U.FL_Hirose_U.FL-R-SMT-1_Vertical');f.SetFPID(pcb.LIB_ID('ARDF_CTL','UFL_Standard'))
    for g in list(f.GraphicalItems()):
        if g.GetLayer()==pcb.F_Mask:removed.append(g);f.Remove(g)
    pcb.PCB_IO_KICAD_SEXPR().FootprintSave(str(F),f)
    for src,name in [(P.parents[0]/'80m/production/ARDF_TX.pretty/Wurth_61201621621.kicad_mod','IDC16_61201621621'),(P.parents[0]/'2m/ARDF_2M.pretty/WR_BHD_61202021621.kicad_mod','IDC20_61202021621')]:
        f=pcb.FootprintLoad(str(src.parent),src.stem);f.SetFPID(pcb.LIB_ID('ARDF_CTL',name));f.SetLibDescription('Wurth keyed WR-BHD; controller finished hole 1.10mm nominal, JLC +0.13/-0.08 ->1.02..1.23 within maker0.95..1.25. Straight-through 1:1 cable.')
        for p in f.Pads():p.SetDrillSize(pcb.VECTOR2I(MM(1.1),MM(1.1)));p.SetSize(pcb.VECTOR2I(MM(1.9),MM(1.9)))
        pcb.PCB_IO_KICAD_SEXPR().FootprintSave(str(F),f)
    def save(name,body,pads,descr,extra=''):
        x,y=body;s=f'''(footprint "{name}"(version 20260206)(generator "pcbnew")(layer "F.Cu")(attr smd)(descr "{descr}")
        (property "Reference" "REF**"(at 0 {-y/2-1})(layer "F.SilkS")(effects(font(size 1 1)(thickness .15))))
        (property "Value" "{name}"(at 0 {y/2+1})(layer "F.Fab")(effects(font(size 1 1)(thickness .15))))
        (fp_rect(start {-x/2} {-y/2})(end {x/2} {y/2})(stroke(width .1)(type default))(layer "F.Fab"))
        (fp_rect(start {-x/2-.5} {-y/2-.7})(end {x/2+.5} {y/2+.7})(stroke(width .05)(type default))(layer "F.CrtYd"))
        {pads}{extra})\n''';(F/(name+'.kicad_mod')).write_text(s)
    def pad(n,x,y,w,h):return f'(pad "{n}" smd rect(at {x} {y})(size {w} {h})(layers "F.Cu" "F.Paste" "F.Mask"))\n'
    pads=''
    # Manufacturer page145 is BOTTOM view. Mirrored about X for top-board view.
    for i in range(4):pads+=pad(i+1,-1.35+i*.9,.6,.5,.8)+pad(8-i,-1.35+i*.9,-.6,.5,.8)
    save('RV3032_C7',(3.2,2.0),pads,'Micro Crystal app manual Rev1.3 p145; 0.5x0.8 lands,0.9pitch,0.4rowgap. Bottom-view numbering mirrored Y into top-board view. Metal lid pin5 VSS.', '(fp_circle(center -1.75 1.1)(end -1.6 1.1)(stroke(width .15)(type default))(fill none)(layer "F.SilkS"))')
    pads=''
    for i in range(11):
        x=-6.38+i*1.27;pads+=pad(i+1,x,7.25,.8,2.2)+pad(22-i,x,-7.25,.8,2.2)
    save('Silicontra_SX1262ZTR8_GC',(15,16.7),pads,'OPTIONAL DNP / OPEN land-pattern qualification. Maker V1.0 15x15,1.27pitch,0.8terminal,1.37depth,1.12end offset. Drawing lacks tolerances, distributor TR8 suffix not verified as ZTR8. Do not populate without dimensional check.', '(fp_circle(center -7.1 7.25)(end -6.95 7.25)(stroke(width .15)(type default))(fill none)(layer "F.SilkS"))')
    (P/'fp-lib-table').write_text('(fp_lib_table (version 7) (lib (name "ARDF_CTL") (type "KiCad") (uri "${KIPRJMOD}/ARDF_CTL.pretty") (options "") (descr "M6-C1 verified lands plus explicitly OPEN optional LoRa landing")))\n')
if __name__=='__main__':write()
