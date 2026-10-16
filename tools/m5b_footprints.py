"""M5B manufacturer-derived physical landings and explicit microstrip net ties.

No third-party drawings are redistributed. Sources/dimensions are in the review.
"""
from pathlib import Path
import math


def microstrip(w, h=.64, t=.07, er=4.3):
    # Hammerstad/Jensen quasi-static, finite-copper thickness correction.
    u=w/h
    du=t/h/math.pi*math.log(1+4*math.e/(t/h*math.cosh(math.sqrt(6.517*u))**-2))
    ur=u+du/2*(1+1/math.cosh(math.sqrt(er-1)))
    a=1+math.log((ur**4+(ur/52)**2)/(ur**4+.432))/49+math.log(1+(ur/18.1)**3)/18.7
    b=.564*((er-.9)/(er+3))**.053
    ee=(er+1)/2+(er-1)/2*(1+10/ur)**(-a*b)
    f=6+(2*math.pi-6)*math.exp(-(30.666/ur)**.7528)
    z=60/math.sqrt(ee)*math.log(f/ur+math.sqrt(1+(2/ur)**2))
    return z,ee


def width50():
    lo,hi=.5,3.
    for _ in range(60):
        mid=(lo+hi)/2
        if microstrip(mid)[0]>50:lo=mid
        else:hi=mid
    return round((lo+hi)/2,3)


def write(folder):
    folder=Path(folder);folder.mkdir(exist_ok=True)
    def save(name,pads,body,description,extra=''):
        x,y=body
        s=f'''(footprint "{name}" (version 20241229)(generator "pcbnew")
 (layer "F.Cu")(attr smd)(descr "{description}")
 (fp_rect(start {-x/2} {-y/2})(end {x/2} {y/2})(stroke(width .1)(type default))(layer "F.Fab"))
 (fp_rect(start {-x/2-.35} {-y/2-.35})(end {x/2+.35} {y/2+.35})(stroke(width .05)(type default))(layer "F.CrtYd"))
 (fp_text reference "REF**"(at 0 {-y/2-.9})(layer "F.SilkS")(effects(font(size .8 .8)(thickness .12))))
 (fp_text value "{name}"(at 0 {y/2+.9})(layer "F.Fab")(effects(font(size .8 .8)(thickness .12))))
 {pads}{extra})\n'''
        (folder/(name+'.kicad_mod')).write_text(s)
    def pad(n,x,y,w,h):
        return f'(pad "{n}" smd rect(at {x} {y})(size {w} {h})(layers "F.Cu" "F.Paste" "F.Mask"))\n'
    # Coilcraft107-1 size A: .050 lands, .065 inner horizontal gap,
    # .110 vertical offset, .130 land height; diagonal leads must be preserved.
    save('Coilcraft_A05T_Doc107',pad(1,-1.4605,1.397,1.27,3.302)+pad(2,1.4605,-1.397,1.27,3.302),(4.6,6.3),
         'Coilcraft107-1Rev07/23/21 size A;staggered .050x.130 inch lands,.065 gap,.110 vertical offset;body3.94x4.45 H3.15max')
    # Coilcraft184-2: .058x.203 lands, .170 outer-edge horizontal span,
    # .103 vertical stagger. Horizontal centers are +/- (.170-.058)/2 inch.
    save('Coilcraft_1812SMS_Doc184',pad(1,-1.4224,1.3081,1.4732,5.1562)+pad(2,1.4224,-1.3081,1.4732,5.1562),(5.5,8.),
         'Coilcraft184-2Rev12/02/21 staggered1.4732x5.1562 lands;outer span4.318;offset2.6162;body4.95x6.35 H4.20max')
    # Coilcraft218-2: H1.02 x I.64 lands separated J.64, long axis X.
    save('Coilcraft_0603HC_Doc218',pad(1,-.64,0,.64,1.02)+pad(2,.64,0,.64,1.02),(2.1,1.35),
         'Coilcraft218-2Rev08/08/22;H1.02 I.64 J.64;body1.80x1.12 H1.02 plus solder.152')
    save('Coilcraft_1008CS_Doc101',pad(1,-1.145,0,1.02,2.54)+pad(2,1.145,0,1.02,2.54),(2.92,2.79),
         'Coilcraft101-1Rev08/05/22;H2.54 I1.02 J1.27;body2.92x2.79 H2.03 plus solder.152')
    # Panasonic C10: gap a2.1,total b9.1,width c1.6.
    save('Panasonic_OSCON_C10',pad(1,-2.8,0,3.5,1.6)+pad(2,2.8,0,3.5,1.6),(9.5,6.8),
         'Panasonic AAB8000COL10 31Oct2025 C10 a2.1 b9.1 c1.6;25SVPG150M diameter6.3 H9.9',
         '(fp_text user "+"(at -3 -2)(layer "F.SilkS")(effects(font(size 1 1)(thickness .15))))')
    save('NTC_Remote_2Wire','''(pad "1" thru_hole rect(at 0 0)(size 1.5 1.5)(drill .8)(layers "*.Cu" "*.Mask"))
 (pad "2" thru_hole circle(at 2.54 0)(size 1.5 1.5)(drill .8)(layers "*.Cu" "*.Mask"))''',(6.,3.),
         'Insulated VishayNTCLE100E3103JB0 remote sensor wire termination;NOT axial resistor body;mount sensor on pass case')
    path=folder/'NTC_Remote_2Wire.kicad_mod';path.write_text(path.read_text().replace('(attr smd)','(attr through_hole)'))
    save('Bourns_SRP1265A',pad(1,-5.55,0,3.1,5.)+pad(2,5.55,0,3.1,5.),(14.,12.8),
         'Bourns SRP1265A manufacturer recommended layout14.2outside8.0inside5.0height;body13.5+-.5x12.5+-.3,H6.2+-.3')
    (folder/'Probe_Pad_0p6.kicad_mod').write_text('''(footprint "Probe_Pad_0p6"(version 20241229)(generator "pcbnew")(layer "F.Cu")
 (attr board_only exclude_from_bom exclude_from_pos_files)(descr "Bare0.6mm probe contact;no physical component/courtyard;inline RF observation")
 (pad "1" smd circle(at 0 0)(size .6 .6)(layers "F.Cu" "F.Mask")))\n''')
    # Native IDC pattern is the same pin grid; qualify exact holes and body.
    import pcbnew as pcb
    f=pcb.FootprintLoad('/usr/share/kicad/footprints/Connector_IDC.pretty','IDC-Header_2x10_P2.54mm_Vertical')
    f.SetFPID(pcb.LIB_ID('ARDF_2M','WR_BHD_61202021621'))
    f.SetLibDescription('Wurth61202021621 drawing002.00130Aug2026;2x10pitch2.54;33.06x9.1x8.75;1.1finishedholes')
    for p in f.Pads():p.SetDrillSize(pcb.VECTOR2I(pcb.FromMM(1.1),pcb.FromMM(1.1)))
    # Grid origin pin1; body is centered at1.27,11.43.
    for g in list(f.GraphicalItems()):
        if g.GetLayer()==pcb.F_Fab:f.Remove(g)
    g=pcb.PCB_SHAPE(f);g.SetShape(pcb.SHAPE_T_RECT);g.SetStart(pcb.VECTOR2I(pcb.FromMM(-3.28),pcb.FromMM(-5.10)));g.SetEnd(pcb.VECTOR2I(pcb.FromMM(5.82),pcb.FromMM(27.96)));g.SetLayer(pcb.F_Fab);g.SetWidth(pcb.FromMM(.1));f.Add(g)
    pcb.PCB_IO_KICAD_SEXPR().FootprintSave(str(folder),f)
    w=width50()
    for length in [6.23,6.62,5.8,2.2,11.,12.4,2.]:
        name='TL50_'+str(length).replace('.','p')+'mm'
        # Physical RF ports are the line ENDPOINTS, not midpoint anchors.
        p1=f'(pad "1" smd rect(at 0 0)(size .2 {w})(layers "F.Cu"))'
        p2=f'(pad "2" smd rect(at {length} 0)(size .2 {w})(layers "F.Cu"))'
        copper=f'(fp_line(start 0 0)(end {length} 0)(stroke(width {w})(type solid))(layer "F.Cu"))'
        save(name,p1+p2+copper,(length+.1,w+.1),'Actual50ohm copper line;0.8mmfinishedPCB core0.64mm er4.3 Cu70um;no zero-length wire',
             '(net_tie_pad_groups "1,2")')
        path=folder/(name+'.kicad_mod');s=path.read_text().splitlines()
        # There is no physical component body/courtyard for a copper feature.
        s=[line for line in s if 'F.CrtYd'not in line and 'F.Fab'not in line and 'F.SilkS'not in line]
        path.write_text('\n'.join(s)+'\n')
    # Separate bare G-S-G contact, optional probe only, not an RF product port.
    save('RF_GSG_Test',pad(1,0,0,.7,.7)+pad(2,0,-1.3,.8,.8)+pad(2,0,1.3,.8,.8),(1.2,3.8),
         'Temporary0.7mm RF probe pad,1signal2ground;no permanent coax stub')
    return w


if __name__=='__main__':
    print(write(Path(__file__).resolve().parents[1]/'hardware/2m/ARDF_2M.pretty'))
