"""Draw the traced RF matching and elliptic LPF as connected circuits."""
import math
import m5a_r1_design as b

def reflow(d):
    layouts={
      '06b_st_matching':(
        {'TL603':(50,95,0),'C631':(88,135,0),'C632':(125,95,90),'TL604':(190,95,0),'C633':(225,135,0),'L634':(265,95,90),'TL605':(330,95,0),'L635':(480,95,0),'C634':(515,135,0),'C635':(550,135,0),'TL606':(50,245,0),'C636':(88,285,0),'TL607':(155,245,0),'C637':(195,285,0),'L638':(245,245,90),'C638':(280,285,0),'TL608':(340,245,0),'C639':(405,245,90),'TL609':(470,245,0)},
        {'MMIC_AC':95,'ST_IS_A':95,'ST_IS_B':95,'ST_IS_C':95,'ST_IS_D':95,'PA_GATE':95,'PA_DRAIN':245,'ST_O_A':245,'ST_O_B':245,'ST_O_C':245,'ST_O_D':245,'ST_DC_BLOCK':245,'ST_LPF_IN':245}),
      '06c_st_lpf':(
        {'L641':(120,130,90),'C641':(120,90,90),'L642':(270,130,90),'C642':(270,90,90),'L643':(420,130,90),'C643':(420,90,90),'C644':(65,180,0),'C645':(195,180,0),'C646':(345,180,0),'C647':(490,180,0)},
        {'ST_LPF_IN':130,'ST_F1':130,'ST_F2':130,'NORMAL_RF':130})}
    for page in d.sheets:
        if page.name not in layouts:continue
        loc,buses=layouts[page.name];old=list(page.placements);title=page.title
        page.items=[];page.used=set();page.placements=[]
        page.text(title,18,15,2)
        page.text('ST DocID17343 Rev1 Figs16/17/14. Traced topology; changed MMIC drive and supplyAM remain UNQUALIFIED.\nTLine symbols are PCB microstrip lengths, NOT purchased components or zero-length wire. No hardware measurements exist.',18,28,1.1)
        coords={}
        for pl in old:
            ref=pl['ref'];p=d.parts[ref];x,y,angle=loc[ref]
            page.place(ref,pl['type'],p['value'],p['pins'],x,y,p['footprint'],p['mpn'],p['group'],p['population'],unit=pl['unit'],angle=angle,note=p['note'],source=p['source_url'],price=p['price_breaks_eur'],evidence=p['evidence'],supplier=p['supplier'],code=p['supplier_part_number'],availability=p['availability'],moq=p['moq'])
            x=round(x/1.27)*1.27;y=round(y/1.27)*1.27;a=math.radians(angle)
            for num,px,py,pa,et in d.lib.pins(pl['type'],pl['unit']):coords[ref,num]=(x+px*math.cos(a)-py*math.sin(a),y-px*math.sin(a)-py*math.cos(a),(pa+angle)%360,p['pins'][num])
        page.items=[x for x in page.items if x.startswith(('(symbol ','(text '))];done=set()
        for net,yy in buses.items():
            points=[(key,x,y)for key,(x,y,a,n)in coords.items()if n==net and key[0]!='L635']
            if len(points)<2:continue
            yy=round(yy/1.27)*1.27;xs=sorted({round(x,4)for key,x,y in points})
            for x1,x2 in zip(xs,xs[1:]):page.wire(x1,yy,x2,yy)
            for x in xs:page.items.append(f'(junction(at {x} {yy})(diameter 0)(color 0 0 0 0)(uuid {b.q(b.uid(page.name+net+str(x)))}))')
            for key,x,y in points:
                if abs(y-yy)>.001:page.wire(x,y,x,yy)
                done.add(key)
            page.label(net,min(xs),yy)
        for key,(x,y,a,net)in coords.items():
            if key in done:continue
            dx,dy={0:(-1,0),90:(0,1),180:(1,0),270:(0,-1)}[a];xx=x+dx*3.81;yy=y+dy*3.81;page.wire(x,y,xx,yy)
            if dy:page.wire(xx,yy,xx+5.08,yy);xx+=5.08
            page.label(net,xx,yy,180 if dx>0 or dy>0 else 0)
        page.text('Input matching: original interstage source was PD84001 drain, not a50ohm MMIC. No claim of unchanged match or sufficient gain.\nOutput matching/LPF retained. L63533n drain feed is a disclosed substitution for the contradictory35.5n/22n ST BOM entry.\nUse one integrated end-to-end commissioning procedure after independent electrical/layout review. No separate PA coupons.',18,345,1.1)
