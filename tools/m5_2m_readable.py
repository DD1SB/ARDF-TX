"""Arrange the actual RF symbols into connected signal chains (no PCB operations)."""
import math,copy
from m5_2m_design import parse,dump,child,children,Atom,uid,q

def reflow(d):
    pages=[s for s in d.sheets if s.name.startswith('06_normal_rf')];assert len(pages)==2
    symbols={}
    for s in pages:
        for item in s.items:
            if item.startswith('(symbol '):
                v=parse(item);ref=next(p[2]for p in children(v,'property')if p[1]=='Reference');symbols[ref]=v
    out={'C609','L608','C610','L621','L622','L623','L624','L625','L626','C621','C622','C623','C624','C625','J501','TP603'}
    loc={
      'C601':(40,80,90),'L611':(80,80,90),'L612':(120,80,90),'L613':(160,80,90),
      'C611':(60,110,0),'C612':(100,110,0),'C613':(140,110,0),'C614':(180,110,0),
      'R602':(215,80,90),'R603':(195,110,0),'R604':(235,110,0),'C615':(260,80,90),'U501':(310,80,0),
      'C602':(360,80,90),'C605':(380,110,0),'L605':(410,80,90),'C606':(450,80,90),'R605':(490,80,90),'Q501':(540,80,0),
      'C609':(45,100,90),'L608':(90,100,90),'C610':(110,130,0),
      'C621':(130,130,0),'L621':(160,100,90),'C622':(185,130,0),'L622':(215,100,90),'L625':(255,100,90),
      'C623':(280,130,0),'L623':(310,100,90),'L626':(350,100,90),'C624':(380,130,0),'L624':(410,100,90),'C625':(440,130,0),'J501':(495,100,0),
    }
    core=set(loc)-out
    for index,s in enumerate(pages):
        s.items=[];s.used=set();s.placements=[]
        s.text(('06a Source / driver / PA, actual connected RF chain'if index==0 else'06b Output matching and nine-pole LPF, actual connected chain'),15,14,2)
        s.text('CALCULATED EVALUATION VALUES: tune only with bounded power and calibrated loads; no144MHz hardware result exists.\nGlobal labels connect bias, protection and supply sheets. Native symbols/pin assignments are electrically authoritative.',18,27,1.1)
        refs=[r for r in symbols if(r in out)==bool(index)];other=[r for r in refs if r not in loc]
        for k,r in enumerate(other):loc[r]=(60+(k%5)*110,215+(k//5)*65,0)
        pincoords={}
        for ref in refs:
            v=copy.deepcopy(symbols[ref]);typ=str(child(v,'lib_id')[1]).split(':',1)[1];unit=int(child(v,'unit')[1]);ox,oy=map(float,child(v,'at')[1:3]);x,y,angle=loc[ref];x=round(x/1.27)*1.27;y=round(y/1.27)*1.27
            child(v,'at')[1:]=[Atom(str(x)),Atom(str(y)),Atom(str(angle))]
            for p in children(v,'property'):
                at=child(p,'at')
                if p[1] in('Reference','Value'):
                    at[1:]=[Atom(str(x+3)),Atom(str(y-8+(1.8 if p[1]=='Value'else 0))),Atom('0')]
                else:at[1:]=[Atom(str(x)),Atom(str(y)),Atom('0')]
            for ins in children(v,'instances'):
                for pr in children(ins,'project'):
                    path=child(pr,'path');path[1]='/'+d.root_uuid+'/'+s.uuid
            s.items.append(dump(v));s.used.add(typ);d.parts[ref]['sheet']=s.name;s.placements.append(dict(ref=ref,unit=unit,x=x,y=y,type=typ))
            for num,px,py,pa,et in d.lib.pins(typ,unit):
                a=math.radians(angle);xx=x+px*math.cos(a)-py*math.sin(a);yy=y-px*math.sin(a)-py*math.cos(a)
                pincoords[(ref,num)]=(xx,yy,(pa+angle)%360,d.parts[ref]['pins'][num])
        # RF chain nets join directly; bias/supply and external terminals keep explicit labels.
        selected=(out if index else core)-{'TP603'}
        chain={}
        for (ref,num),(x,y,a,net)in pincoords.items():
            if ref in selected and net and net not in('GND','CLK_NORMAL','PA_GATE','PA_DRAIN'):
                chain.setdefault(net,[]).append((ref,num,x,y))
        bus_y=round((100 if index else 80)/1.27)*1.27;done=set()
        def junction(x,y):s.items.append('(junction (at '+str(round(x,4))+' '+str(round(y,4))+') (diameter 0) (color 0 0 0 0)(uuid '+q(uid(s.name+':junction:'+str(len(s.items))))+'))')
        for net,points in chain.items():
            # Single terminals attach to other sheets by label, not dangling local wires.
            if len(points)<2:continue
            xs=sorted(set(round(p[2],4)for p in points))
            for a,b in zip(xs,xs[1:]):s.wire(a,bus_y,b,bus_y)
            for x in xs:junction(x,bus_y)
            for ref,num,x,y in points:
                if abs(y-bus_y)>.001:s.wire(x,y,x,bus_y)
                done.add((ref,num))
            s.label(net,min(xs),bus_y,0)
        # Ground bus applies to source/filter shunts only. Other cells retain short named connections.
        grounds=[(ref,num,x,y)for(ref,num),(x,y,a,n)in pincoords.items()if n=='GND'and ref in selected]
        ground_y=round((160 if index else 145)/1.27)*1.27
        if grounds:
            xs=sorted(set(round(t[2],4)for t in grounds))
            for a,b in zip(xs,xs[1:]):s.wire(a,ground_y,b,ground_y)
            for x in xs:junction(x,ground_y)
            s.label('GND',min(xs),ground_y,0)
            for ref,num,x,y in grounds:s.wire(x,y,x,ground_y);done.add((ref,num))
        for key,(x,y,a,net)in pincoords.items():
            if key in done:continue
            if net is None:s.items.append(f'(no_connect(at {x:.4f} {y:.4f})(uuid {q(uid(s.name+str(key)+"nc"))}))');continue
            dx,dy={0:(-1,0),90:(0,1),180:(1,0),270:(0,-1)}[a];xx=x+dx*3.81;yy=y+dy*3.81;s.wire(x,y,xx,yy)
            if dy:s.wire(xx,yy,xx+5.08,yy);xx+=5.08
            s.label(net,xx,yy,180 if dx>0 or dy>0 else 0)
        # Source/gate/stability annotations travel with the connected CAD rather than an unrelated drawing.
        s.text('The normal connector has no RF switch or conductor to the training connector.\nOutput match is a replaceable 144MHz starting network, not the ST500MHz test network.\nLPF inductors93nH are82nH+11nH in series for current margin and obtainable values.',20,365,1.1)
