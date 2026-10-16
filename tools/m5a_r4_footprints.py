"""Manufacturer-derived candidate landings; no PCB or assembly qualification.

Dimensions: Mini-Circuits DF782 Rev G (02/08/17), suggested land pattern,
and TI RNW0013A drawing 4222804/C (11/2019). All units below are mm.
"""
from pathlib import Path


def write(directory):
    directory = Path(directory)
    directory.mkdir(exist_ok=True)
    # DF782 inch dimensions: side pitch .059, side land .028 x .059,
    # ground stem .036, wide ground .075, overall land height .210,
    # lower shoulder .095 REF and 45-degree chamfers. Pins 2/4 share ground.
    inch = 25.4
    half_stem, half_wide = .036 * inch / 2, .075 * inch / 2
    shoulder = .095 * inch
    chamfer = half_wide - half_stem
    top = .210 * inch
    stem_end = .059 * inch
    points = [(-half_stem, -stem_end), (half_stem, -stem_end),
              (half_stem, -(shoulder-chamfer)), (half_wide, -shoulder),
              (half_wide, -(top-chamfer)), (half_stem, -top),
              (-half_stem, -top), (-half_wide, -(top-chamfer)),
              (-half_wide, -shoulder), (-half_stem, -(shoulder-chamfer))]
    s = ['(footprint "PHA1_DF782_RevG" (version 20241229)(generator "pcbnew")',
         '(layer "F.Cu")(attr smd)',
         '(descr "Mini-Circuits DF782 RevG 02/08/17 suggested land. 2/4 common GND. REF shoulder dimension and stencil/vias require review.")',
         '(fp_rect(start -2.6 -5.65)(end 2.6 .3)(stroke(width .05)(type default))(layer "F.CrtYd"))',
         '(fp_circle(center -2 -.2)(end -1.85 -.2)(stroke(width .1)(type default))(fill none)(layer "F.SilkS"))',
         '(fp_text reference "REF**"(at 0 -6.1)(layer "F.SilkS")(effects(font(size 1 1)(thickness .15))))',
         '(fp_text value "PHA-1+"(at 0 .9)(layer "F.Fab")(effects(font(size 1 1)(thickness .15))))']
    for pin, x in [('1', -.059*inch), ('3', .059*inch)]:
        s.append(f'(pad "{pin}" smd rect(at {x} {-stem_end/2})(size {.028*inch} {stem_end})(layers "F.Cu" "F.Paste" "F.Mask"))')
    s.append(f'(pad "2" smd rect(at 0 {-stem_end/2})(size {half_stem*2} {stem_end})(layers "F.Cu" "F.Paste" "F.Mask"))')
    polygon = ' '.join(f'(xy {x:.6f} {y+3:.6f})' for x, y in points)
    # Paddle paste is deliberately not fabricated: layout must define via/stencil
    # coverage. Copper polygon meets pin-2 copper at the shared ground boundary.
    s.append(f'(pad "4" smd custom(at 0 -3)(size .1 .1)(layers "F.Cu" "F.Mask")(options(clearance outline)(anchor rect))(primitives(gr_poly(pts {polygon})(width 0)(fill yes))))')
    s.append(')')
    (directory/'PHA1_DF782_RevG.kicad_mod').write_text('\n'.join(s)+'\n')

    # RNW is NOT a conventional QFN with a grounded center pad: bars 6,7,8
    # carry PGND, SW and VOUT independently. The TI mask-defined center openings
    # are .25 x 3.4; copper extends .05 beyond each edge.
    s = ['(footprint "TI_RNW0013A_4222804C" (version 20241229)(generator "pcbnew")',
         '(layer "F.Cu")(attr smd)',
         '(descr "TI RNW0013A 4222804/C 11/2019 board/stencil example. Separate 6PGND 7SW 8VOUT bars; never a common EP.")',
         '(fp_rect(start -1.75 -1.5)(end 1.75 1.5)(stroke(width .1)(type default))(layer "F.Fab"))',
         '(fp_rect(start -2.2 -2)(end 2.2 2)(stroke(width .05)(type default))(layer "F.CrtYd"))',
         '(fp_circle(center -2.15 -1)(end -2.05 -1)(stroke(width .1)(type default))(fill none)(layer "F.SilkS"))',
         '(fp_text reference "REF**"(at 0 -2.5)(layer "F.SilkS")(effects(font(size 1 1)(thickness .15))))',
         '(fp_text value "TPS611781RNWR"(at 0 2.5)(layer "F.Fab")(effects(font(size 1 1)(thickness .15))))']
    for i in range(5):
        for pin, x in [(i+1, -1.6), (13-i, 1.6)]:
            s.append(f'(pad "{pin}" smd roundrect(at {x} {-1+i*.5})(size .7 .25)(layers "F.Cu" "F.Paste" "F.Mask")(roundrect_rratio .2)(solder_mask_margin .05))')
    for pin, x in [(6, -.55), (7, 0), (8, .55)]:
        s.append(f'(pad "{pin}" smd roundrect(at {x} 0)(size .35 3.5)(layers "F.Cu" "F.Mask")(roundrect_rratio .142857)(solder_mask_margin -.05))')
        for y in [-1.2, 0, 1.2]:
            s.append(f'(pad "" smd roundrect(at {x} {y})(size .25 1)(layers "F.Paste")(roundrect_rratio .2))')
    s.append(')')
    (directory/'TI_RNW0013A_4222804C.kicad_mod').write_text('\n'.join(s)+'\n')


def check(directory, parse, child, children):
    report = {}
    for name, expected in [
        ('PHA1_DF782_RevG', {'1':([-1.4986,-.7493],[.7112,1.4986]),
                           '2':([0.,-.7493],[.9144,1.4986]),
                           '3':([1.4986,-.7493],[.7112,1.4986])}),
        ('TI_RNW0013A_4222804C', {str(i+1):([-1.6,-1+i*.5],[.7,.25]) for i in range(5)} |
         {str(13-i):([1.6,-1+i*.5],[.7,.25]) for i in range(5)} |
         {'6':([-.55,0.],[.35,3.5]),'7':([0.,0.],[.35,3.5]),'8':([.55,0.],[.35,3.5])})]:
        source = parse((Path(directory)/(name+'.kicad_mod')).read_text())
        pads = {p[1]:p for p in children(source, 'pad') if p[1]}
        assert set(pads) == (set(expected)|{'4'} if name.startswith('PHA') else set(expected))
        for pin, (at, size) in expected.items():
            for key, value in [('at',at),('size',size)]:
                actual = list(map(float, child(pads[pin],key)[1:]))
                assert all(abs(a-b)<1e-7 for a,b in zip(actual,value)), (name,pin,key,actual,value)
        if name.startswith('PHA'):
            polygon = child(child(pads['4'],'primitives'),'gr_poly')
            xy = [list(map(float,p[1:])) for p in children(child(polygon,'pts'),'xy')]
            assert list(map(float,child(pads['4'],'at')[1:]))==[0.,-3.]
            assert abs(min(p[1] for p in xy)-3+5.334)<1e-7 and max(abs(p[0])for p in xy)==.9525
        else:
            for pin in ['6','7','8']:
                assert float(child(pads[pin],'solder_mask_margin')[1])==-.05
            assert sum(not p[1] for p in children(source,'pad'))==9
        report[name] = {'physical_pad_count':len(pads),'dimensional_assertions':'PASS',
                        'qualification':'Manufacturer-derived candidate; stencil/thermal/board integration not physically qualified'}
    return report
