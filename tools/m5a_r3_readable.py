"""Connected RF circuit drawings; values/pin connectivity remain authoritative."""
import math
import m5a_r1_design as b

LAYOUTS={
'06_dl3_rf':(
 {'U901':(65,85,0),'R900':(120,100,90),'C900':(155,100,90),'L900':(210,100,90),'L901':(290,100,90),'L902':(370,100,90),'C901':(180,185,0),'C902':(250,185,0),'C903':(330,185,0),'C904':(410,185,0),'R901':(450,185,0)},
 {'CLK72_BUF':95,'CLK72_LIMIT':100,'LP72_IN':100,'LP72_A':100,'LP72_B':100,'LP72_OUT':100,'GND':240}),
'06b_dl3_doubler_driver':(
 {'C911':(55,140,90),'L904':(90,200,0),'C913':(110,200,0),'Q901':(130,140,0),'R909':(35,200,0),'R910':(35,80,0),'C912':(45,200,0),'R911':(132.08,105,0),'R912':(132.08,185,0),'C916':(155,185,0),'R914':(132.08,48,0),'C914':(160,85,0),'L905':(132.08,75,0),'C915':(225,140,90),'R913':(260,200,0),'Q902':(295,140,0),'R915':(297.18,185,0),'C918':(320,185,0),'L909':(297.18,50,0),'C917':(330,100,0),'L906':(297.18,100,0),'C919':(370,135,90),'R916':(420,200,0)},
 {'VMOD':35,'T3_G1':140,'T3_G2':120,'T3_D':112,'T3_S':170,'T3_FEED':60,'TP5_ORIGINAL':90,'T4_B':140,'T4_E':170,'T4_C':125,'T4_FEED':70,'T5_B':150,'GND':250}),
'06c_dl3_final':(
 {'Q903':(85,145,0),'L910':(87.63,100,0),'L911':(87.63,60,0),'C920':(105,60,0),'C922':(120,90,0),'C921':(155,140,90),'L907':(215,140,90),'C923':(260,190,0),'C924':(285,190,0),'L908':(340,140,90),'C925':(385,190,0),'C926':(485,190,0),'J501':(430,140,0)},
 {'VPA':45,'T5_FEED':80,'T5_C':140,'OUT_MID':140,'OUT_TRIM':140,'NORMAL_RF':140,'GND':250})}

def reflow(d):
    # Use a dual-gate transistor drawing, not a box, with independently verified
    # BF981 physical numbers. BF994S provides GRAPHICS ONLY, not a substitution.
    d.lib.native('Transistor_FET:BF994S','BF981_PHILIPS')
    for prop in b.children(d.lib.defs['BF981_PHILIPS'],'property'):
        if prop[1]=='ki_fp_filters':prop[2]='SOT*103*'
        if prop[1]=='Description':prop[2]='Philips BF981 dual-gate,1S2D3G2 4G1; landing OPEN'
    for page in d.sheets:
        if page.name not in LAYOUTS:continue
        loc,buses=LAYOUTS[page.name]
        old=list(page.placements);title=page.title
        page.items=[];page.used=set();page.placements=[]
        page.text(title,18,15,2)
        page.text('Actual connected RF network. Pin numbers and named supply/interface crossings are explicit.\nDL3BBX CQ-DL5/1992 reference; PRIVATE CONSTRUCTION ONLY. Derivative RF performance NOT_RUN.',18,25,1.15)
        coords={}
        for pl in old:
            ref=pl['ref'];p=d.parts[ref];x,y,angle=loc[ref]
            page.place(ref,pl['type'],p['value'],p['pins'],x,y,p['footprint'],p['mpn'],p['group'],p['population'],unit=pl['unit'],angle=angle,note=p['note'],source=p['source_url'],price=p['price_breaks_eur'],evidence=p['evidence'],supplier=p['supplier'],code=p['supplier_part_number'],availability=p['availability'],moq=p['moq'])
            x=round(x/1.27)*1.27;y=round(y/1.27)*1.27;a=math.radians(angle)
            for num,px,py,pa,et in d.lib.pins(pl['type'],pl['unit']):
                coords[ref,num]=(x+px*math.cos(a)-py*math.sin(a),y-px*math.sin(a)-py*math.cos(a),(pa+angle)%360,p['pins'][num])
        page.items=[i for i in page.items if i.startswith(('(symbol ','(text '))]
        done=set()
        def junction(x,y):page.items.append(f'(junction(at {x:.4f} {y:.4f})(diameter 0)(color 0 0 0 0)(uuid {b.q(b.uid(page.name+":j:"+str(len(page.items))))}))')
        for net,yy in buses.items():
            points=[(key,x,y)for key,(x,y,a,n)in coords.items()if n==net]
            if len(points)<2:continue
            if net=='CLK72_BUF':
                adjusted=[]
                for key,x,y in points:
                    if key[0]=='U901':
                        page.wire(x,y,95.25,y);x=95.25
                    adjusted.append((key,x,y))
                points=adjusted
            yy=round(yy/1.27)*1.27;xs=sorted({round(x,4)for key,x,y in points})
            for x1,x2 in zip(xs,xs[1:]):page.wire(x1,yy,x2,yy)
            for x in xs:junction(x,yy)
            for key,x,y in points:
                if abs(y-yy)>.001:page.wire(x,y,x,yy)
                done.add(key)
            page.label(net,min(xs),yy)
        for key,(x,y,a,net)in coords.items():
            if key in done:continue
            if net is None:
                page.items.append(f'(no_connect(at {x:.4f} {y:.4f})(uuid {b.q(b.uid(page.name+str(key)+"nc"))}))');continue
            dx,dy={0:(-1,0),90:(0,1),180:(1,0),270:(0,-1)}[a]
            xx=x+dx*3.81;yy=y+dy*3.81;page.wire(x,y,xx,yy)
            if dy:page.wire(xx,yy,xx+5.08,yy);xx+=5.08
            page.label(net,xx,yy,180 if dx>0 or dy>0 else 0)
        page.text('OPEN: exact RF transistor supplier/manufacturer and landings; actual source drive, tuning, sineAM power, spectrum and stability.\nDo not infer validated performance or manufacture readiness from the original circuit or a passing ERC.',18,330,1.15)
