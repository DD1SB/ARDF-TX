"""Dimensioned feasibility sketches, explicitly NOT native assembly/release CAD."""
import os
from m5b_e6_common import *


def main():
    guard();os.environ.setdefault('MPLCONFIGDIR','/tmp/m5b-e6-matplotlib')
    import matplotlib;matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    from matplotlib.patches import Rectangle,Circle
    fig,axes=plt.subplots(2,2,figsize=(12,9),layout='constrained')
    a=axes[0,0]
    for box,color,label in [((20,20,150,110),'green','Unchanged E5 PCB150x110'),((42,5,100,100),'grey','One SK81 cooler100x100'),((84.5,28,15,44),'orange','PA bar15x44')]:
        x,y,w,h=box;a.add_patch(Rectangle((x,y),w,h,fill=False,edgecolor=color,lw=2,label=label))
    for x,y in [(25,25),(165,25),(25,125),(165,125)]:a.add_patch(Circle((x,y),1.6,fill=False))
    for x,y,r in [(92,55,'Q501 unchanged'),(117.54,26,'Q401 lead row'),(135.28,39,'Q402 lead row')]:
        a.plot(x,y,'ko');a.annotate(r,(x,y),xytext=(5,6),textcoords='offset points',fontsize=8)
    a.add_patch(Rectangle((112.34,5.25),10.4,15.75,fill=False,edgecolor='red'))
    a.add_patch(Rectangle((131.38,23.95),7.8,11.05,fill=False,edgecolor='red'))
    a.add_patch(Circle((135.28,27.75),4.5,fill=False,ls='--',edgecolor='red'))
    a.set(xlim=(15,175),ylim=(135,0),aspect='equal',title='Plan: projected device bodies below PCB',xlabel='native X / mm',ylabel='native Y / mm');a.legend(fontsize=7)
    a=axes[0,1]
    for y,h,color,label in [(-1.6,1.6,'green','PCB1.6'),(-1.727,.127,'red','TSP1600 sheet .127'),(-7.927,6.2,'orange','Aluminium bar6.2'),(-7.977,.05,'red','Grease allowance .05'),(-11.977,4,'grey','SK81 base4')]:
        a.add_patch(Rectangle((0,y),15,h,facecolor=color,alpha=.5,label=label))
    for x in range(1,15,2):a.add_patch(Rectangle((x,-22.977),.7,11,facecolor='grey',alpha=.5))
    a.plot([6.45,8.55],[.15,.15],lw=4,color='black',label='Q501 source solder / package above')
    a.set(xlim=(-1,26),ylim=(-26,4),aspect='equal',title='Q501 stack: interface/source resistance retained',xlabel='local X / mm',ylabel='Z from PCB top / mm');a.legend(fontsize=7,loc='lower right')
    a=axes[1,0]
    a.add_patch(Rectangle((0,-1.6),36,1.6,color='green',alpha=.5))
    a.add_patch(Rectangle((0,-12),36,4,color='grey',alpha=.5))
    for x,w,name in [(3,10.4,'Q401'),(22,7.8,'Q402')]:
        a.add_patch(Rectangle((x,-7.95),w,4.5 if name=='Q401' else 2.9,color='black',alpha=.6))
        a.plot([x,x+w],[-8,-8],color='red',lw=3)
        a.plot([x+w/2]*2,[-12,-4],color='blue',lw=1)
        a.text(x,-3,name,fontsize=9)
    a.set(xlim=(-1,37),ylim=(-15,3),aspect='equal',title='Tab plane concept; insulation under each live tab',xlabel='schematic section / mm',ylabel='Z / mm')
    a.text(0,1,'Tool holes / fastener details NOT released',fontsize=8)
    a=axes[1,1];a.axis('off')
    a.text(.02,.95,'Single independently supported structure',fontsize=13,va='top')
    a.text(.02,.85,'SK81 indexed mass214g; bar11.05g.\nHardware/guard mass not closed; assembly245–270g estimate.\n\nQ501=GND; Q401=VPA; Q402=MOD_SINK.\nMica + insulated fasteners required on both live tabs.\nSource-sheet contact/thermal path remains OPEN.\n\nGuard: shade, ventilation, raised>=15mm, no foliage\ncontact. No outdoor or fire qualification claimed.\n\nAll package shapes are simplified envelopes.\nNo E6 footprint, slot or machining drawing is released.',fontsize=10,va='top',linespacing=1.5)
    fig.suptitle('M5B-E6 FEASIBILITY CONCEPT — HOLD — NOT native KiCad / NOT a drilling template',fontsize=13)
    fig.savefig(OUT/'common-cooler-concept.pdf');fig.savefig(OUT/'common-cooler-concept.svg');fig.savefig(OUT/'common-cooler-concept.png',dpi=140);plt.close(fig)
    svg=OUT/'common-cooler-concept.svg'
    svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    save('mechanical-concept.json',dict(status='NOT_IMPLEMENTED_NOT_MACHINING_DATA',
        native_source_sha256=sha(HW/'RF2M.kicad_pcb'),one_heatsink_requirement=True,
        concept=dict(MPN='Fischer SK81 100 SA',dimensions_mm=[100,100,15],base_mm=4,mass_g_indexed=214,
                     planned_xy_mm=[42,5,142,105],plane_Z_mm=-8,bar_mm=[15,44,6.2],bar_mass_g=15*44*6.2*.0027,
                     assembly_mass_g_estimate=[245,270]),
        unchanged_native_Q_positions=dict(Q501=[92,55,0],Q401=[115,26,0],Q402=[133,39,0]),
        proposed_body_orientation='Q401/Q402 horizontal below PCB toward negativeY; lead rows unchanged, out-of-plane bend only',
        unapproved_access_opening=dict(centre_mm=[135.28,27.75],diameter_mm=9,
            status='Manufacturer hole reference, drill-tool envelope and copper clearance NOT closed; no native cutout added'),
        assembly_blockers=['Qualified common source thermal interface and RF-loss bound',
            'Independent cooler bracket/support design and tolerances; prevent board bending',
            'Exact manufacturer hole datum and lead-form jig qualification',
            'Fastener torque, insulating bush selection and pressure retention',
            'Carrier/enclosure/antenna cable tool-access collision audit'],physical='NOT_RUN'))


if __name__=='__main__':main()
