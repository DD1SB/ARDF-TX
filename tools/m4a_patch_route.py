#!/usr/bin/python3
"""Finish explicitly reported compact-board airwires on a fine two-layer grid.
This is a CAD routing aid, not an RF-performance or clearance proof. Native
KiCad DRC is authoritative. Frozen E2 is never written. No via-in-pad.
"""
import argparse,heapq,json,math,time
import pcbnew as pcb
from PIL import Image,ImageDraw
from m4a_design import P,D,NAME,MM
from m3b_pcb import pt,xy
STEP=.05;X0=20.;Y0=20.;NX=3001;NY=2201;N=NX*NY

def ij(v):return(round((v[0]-X0)/STEP),round((v[1]-Y0)/STEP))
def pos(i):return(X0+(i%NX)*STEP,Y0+(i//NX)*STEP)
def uid(x):return x.m_Uuid.AsString()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('report');ap.add_argument('--limit',type=int,default=100);ap.add_argument('--keep-ground',action='store_true');ap.add_argument('--fine',action='store_true');ap.add_argument('--ground',action='store_true');ap.add_argument('--ground-width',type=float,default=.25);a=ap.parse_args()
    global STEP,NX,NY,N
    if a.fine:STEP=.025;NX=6001;NY=4401;N=NX*NY
    b=pcb.LoadBoard(str(P/(NAME+'.kicad_pcb')))
    removed=[]if a.keep_ground else[t for t in b.GetTracks()if t.GetNetname()=='GND']+list(b.Zones())
    for x in removed:b.Remove(x)
    items={uid(t):t for t in b.GetTracks()};pads=[p for f in b.GetFootprints()for p in f.Pads()];items.update({uid(p):p for p in pads})
    report=json.load(open(a.report));logs=[]
    for case in report['unconnected_items'][:a.limit]:
        ends=case['items']
        if any(x['uuid']not in items for x in ends):continue
        objs=[items[x['uuid']]for x in ends];net=objs[0].GetNetname();assert all(o.GetNetname()==net for o in objs)
        if net=='GND'and not a.ground:continue
        t0=time.monotonic();width=a.ground_width if net=='GND'else .15;gap=.15;extra=0.
        ims=[Image.new('L',(NX,NY),0)for _ in range(2)];vims=[Image.new('L',(NX,NY),0)for _ in range(2)];ds=[ImageDraw.Draw(q)for q in ims];vs=[ImageDraw.Draw(q)for q in vims]
        def rect(draw,box,r):
            x0,y0=ij((box[0]-r,box[1]-r));x1,y1=ij((box[2]+r,box[3]+r));draw.rectangle((x0,y0,x1,y1),fill=1)
        def line(draw,c,d,r):
            c=ij(c);d=ij(d);rad=round(r/STEP);draw.line([c,d],fill=1,width=2*rad+1)
            for x,y in(c,d):draw.ellipse((x-rad,y-rad,x+rad,y+rad),fill=1)
        for p in pads:
            q=p.GetBoundingBox();box=[pcb.ToMM(q.GetLeft()),pcb.ToMM(q.GetTop()),pcb.ToMM(q.GetRight()),pcb.ToMM(q.GetBottom())];layers=[0,1]if p.GetAttribute()!=pcb.PAD_ATTRIB_SMD else[0 if p.IsOnLayer(pcb.F_Cu)else 1]
            g=.62 if p.GetNetname()=='DRAIN_PA'else gap
            for layer in layers:
                if p.GetNetname()!=net:rect(ds[layer],box,g+width/2+extra)
                # All SMD pads remain a via exclusion, including this net's pads.
                rect(vs[layer],box,.20 if p.GetNetname()==net else g+.30+extra)
        for t in b.GetTracks():
            if t.GetNetname()==net:
                if isinstance(t,pcb.PCB_VIA):
                    for vdraw in vs:line(vdraw,xy(t.GetPosition()),xy(t.GetPosition()),.56)
                continue
            via=isinstance(t,pcb.PCB_VIA);layers=[0,1]if via else[0 if t.GetLayer()==pcb.F_Cu else 1];w=pcb.ToMM(t.GetWidth(pcb.F_Cu)if via else t.GetWidth());g=.62 if t.GetNetname()=='DRAIN_PA'else gap
            for layer in layers:
                line(ds[layer],xy(t.GetStart()),xy(t.GetEnd()),w/2+g+width/2+extra)
                line(vs[layer],xy(t.GetStart()),xy(t.GetEnd()),w/2+g+.30+extra)
        for d in ds+vs:
            # Board edge plus minimum copper-edge clearance and conservative margin.
            d.rectangle((0,0,NX-1,12),fill=1);d.rectangle((0,NY-13,NX-1,NY-1),fill=1);d.rectangle((0,0,12,NY-1),fill=1);d.rectangle((NX-13,0,NX-1,NY-1),fill=1)
        masks=[q.tobytes()for q in ims];vm=[q.tobytes()for q in vims]
        endpoints=[(e['pos']['x'],e['pos']['y'])for e in ends];cells=[iy*NX+ix for ix,iy in map(ij,endpoints)]
        def layers(o):return[0,1]if isinstance(o,pcb.PCB_VIA)or(isinstance(o,pcb.PAD)and o.GetAttribute()!=pcb.PAD_ATTRIB_SMD)else[0 if o.IsOnLayer(pcb.F_Cu)else 1]
        sl=layers(objs[0]);gl=layers(objs[1]);starts=[l*N+cells[0]for l in sl if not masks[l][cells[0]]];goals={l*N+cells[1]for l in gl if not masks[l][cells[1]]}
        if not starts or not goals:
            logs.append(dict(net=net,status='blocked endpoint',start=bool(starts),goal=bool(goals)));print(net,logs[-1],flush=True);continue
        gx,gy=ij(endpoints[1])
        def h(i):
            z=i%N;dx=abs(z%NX-gx);dy=abs(z//NX-gy);return 10*max(dx,dy)+4*min(dx,dy)
        best={s:0 for s in starts};prev={};queue=[(h(s),0,s)for s in starts];heapq.heapify(queue);found=None;expanded=0
        moves=[(1,0,10),(-1,0,10),(0,1,10),(0,-1,10),(1,1,14),(1,-1,14),(-1,1,14),(-1,-1,14)]
        while queue:
            _,cost,i=heapq.heappop(queue)
            if cost!=best.get(i):continue
            if i in goals:found=i;break
            expanded+=1
            if expanded>1800000:break
            layer=i//N;z=i%N;x=z%NX;y=z//NX;mask=masks[layer]
            for dx,dy,w in moves:
                xx=x+dx;yy=y+dy
                if not(0<=xx<NX and 0<=yy<NY):continue
                zz=yy*NX+xx;j=layer*N+zz
                if mask[zz]or(dx and dy and(mask[y*NX+xx]or mask[yy*NX+x])):continue
                c=cost+w
                if c<best.get(j,10**12):best[j]=c;prev[j]=i;heapq.heappush(queue,(c+h(j),c,j))
            if not vm[0][z]and not vm[1][z]:
                j=(1-layer)*N+z;c=cost+650
                if c<best.get(j,10**12):best[j]=c;prev[j]=i;heapq.heappush(queue,(c+h(j),c,j))
        if found is None:
            logs.append(dict(net=net,status='no path',expanded=expanded));print(net,'no path',expanded,flush=True);continue
        ids=[found]
        while ids[-1]in prev:ids.append(prev[ids[-1]])
        ids.reverse();pieces=[];vias=[];points=[];layer=ids[0]//N
        def emit(points,l):
            # Compress only collinear grid steps; retain actual off-grid endpoints.
            if len(points)<2:return
            out=[points[0]]
            for j in range(1,len(points)-1):
                a,b1,c=out[-1],points[j],points[j+1]
                if abs((b1[0]-a[0])*(c[1]-b1[1])-(b1[1]-a[1])*(c[0]-b1[0]))<1e-8:continue
                out.append(b1)
            out.append(points[-1])
            for a0,b0 in zip(out,out[1:]):
                if math.dist(a0,b0)<.00001:continue
                t=pcb.PCB_TRACK(b);t.SetStart(pt(*a0));t.SetEnd(pt(*b0));t.SetWidth(MM(width));t.SetLayer(pcb.F_Cu if l==0 else pcb.B_Cu);t.SetNet(b.FindNet(net));b.Add(t);items[uid(t)]=t;pieces.append(dict(start=a0,end=b0,layer=l))
        points=[endpoints[0],pos(ids[0]%N)]
        for i in ids[1:]:
            l=i//N;v=pos(i%N)
            if l!=layer:
                emit(points,layer);via=pcb.PCB_VIA(b);via.SetPosition(pt(*v));via.SetWidth(MM(.6));via.SetDrill(MM(.3));via.SetLayerPair(pcb.F_Cu,pcb.B_Cu);via.SetNet(b.FindNet(net));via.SetFrontTentingMode(1);via.SetBackTentingMode(1);b.Add(via);items[uid(via)]=via;vias.append(v);points=[v];layer=l
            else:points.append(v)
        points.append(endpoints[1]);emit(points,layer)
        logs.append(dict(net=net,status='routed',width_mm=width,endpoints_mm=endpoints,segments=pieces,vias_mm=vias,expanded=expanded,elapsed_s=round(time.monotonic()-t0,3)));print(net,'routed',len(pieces),'segments',len(vias),'vias',expanded,'nodes',flush=True)
        pcb.SaveBoard(str(P/(NAME+'.kicad_pcb')),b)
    old=json.loads((D/'local-route-completion.json').read_text())if(D/'local-route-completion.json').exists()else[];old.extend(logs);(D/'local-route-completion.json').write_text(json.dumps(old,indent=2)+'\n')
if __name__=='__main__':main()
