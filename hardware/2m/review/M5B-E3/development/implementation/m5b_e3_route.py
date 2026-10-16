#!/usr/bin/python3
"""Finish explicitly reported compact-board airwires on a fine two-layer grid.
This is a CAD routing aid, not an RF-performance or clearance proof. Native
KiCad DRC is authoritative. Historical/RF80 files are never written. Only GND may use an ordinary tented via in a pad;inspect soldering.
"""
import argparse,heapq,json,math,time
import pcbnew as pcb
from PIL import Image,ImageDraw
from m5b_e3_common import HW as P,OUT as D
MM=pcb.FromMM
NAME='RF2M'
from m3b_pcb import pt,xy
STEP=.1;X0=20.;Y0=20.;NX=1801;NY=1401;N=NX*NY

def ij(v):return(round((v[0]-X0)/STEP),round((v[1]-Y0)/STEP))
def pos(i):return(X0+(i%NX)*STEP,Y0+(i//NX)*STEP)
def uid(x):return x.m_Uuid.AsString()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('report');ap.add_argument('--limit',type=int,default=100);ap.add_argument('--keep-ground',action='store_true',default=True);ap.add_argument('--fine',action='store_true');ap.add_argument('--width',type=float,default=.15);ap.add_argument('--ground',action='store_true');ap.add_argument('--ground-width',type=float,default=.25);ap.add_argument('--power-widths',action='store_true');ap.add_argument('--direct',action='store_true');a=ap.parse_args()
    global STEP,NX,NY,N
    if a.fine:STEP=.025;NX=7201;NY=5601;N=NX*NY
    b=pcb.LoadBoard(str(P/(NAME+'.kicad_pcb')))
    if a.power_widths:
        # Main current buses must not depend on long thin control-router traces.
        power_nets={'VIN_CONV','VBOOST','VREG_RAW','VMOD'}
        removed_power=[t for t in b.GetTracks()if t.GetNetname()in power_nets and not isinstance(t,pcb.PCB_VIA)and pcb.ToMM(t.GetWidth())<.5 and pcb.ToMM(t.GetLength())>2]
        for t in removed_power:b.Remove(t)
        b.BuildConnectivity()
    removed=[]if a.keep_ground else[t for t in b.GetTracks()if t.GetNetname()=='GND']+list(b.Zones())
    for x in removed:b.Remove(x)
    items={uid(t):t for t in b.GetTracks()};pads=[p for f in b.GetFootprints()for p in f.Pads()if p.IsOnLayer(pcb.F_Cu)or p.IsOnLayer(pcb.B_Cu)];items.update({uid(p):p for p in pads})
    report=json.load(open(a.report));logs=[]
    for case in report['unconnected_items'][:a.limit]:
        ends=case['items']
        if any(x['uuid']not in items for x in ends):continue
        objs=[items[x['uuid']]for x in ends];net=objs[0].GetNetname();assert all(o.GetNetname()==net for o in objs)
        if net=='GND'and not a.ground:continue
        t0=time.monotonic();width=a.ground_width if net=='GND'else a.width;gap=.15;extra=.02
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
                if not(net=='GND'and p.GetNetname()=='GND'):
                    rect(vs[layer],box,.20 if p.GetNetname()==net else g+(.3 if net=='GND'else .4)+extra)
        # Native RF copper graphics are conductive net-tie line bodies, not
        # decorative footprint outlines. Keep alien nets away from them.
        for fp in b.GetFootprints():
            if not fp.GetReference().startswith('TL'):continue
            ns={p.GetNetname()for p in fp.Pads()}
            if net in ns:continue
            for shape in fp.GraphicalItems():
                if shape.GetLayer()!=pcb.F_Cu:continue
                box=shape.GetBoundingBox(); bb=[pcb.ToMM(box.GetLeft()),pcb.ToMM(box.GetTop()),pcb.ToMM(box.GetRight()),pcb.ToMM(box.GetBottom())]
                rect(ds[0],bb,gap+width/2+extra);rect(vs[0],bb,gap+.4+extra)
        # Flat-ended RF polygons are physical copper,not annotation.
        for shape in b.GetDrawings():
            if shape.GetLayer()not in[pcb.F_Cu,pcb.B_Cu]or not hasattr(shape,'GetNetname')or shape.GetNetname()==net:continue
            q=shape.GetBoundingBox();bb=[pcb.ToMM(q.GetLeft()),pcb.ToMM(q.GetTop()),pcb.ToMM(q.GetRight()),pcb.ToMM(q.GetBottom())];l=0 if shape.GetLayer()==pcb.F_Cu else 1
            rect(ds[l],bb,gap+width/2+extra);rect(vs[l],bb,gap+.4+extra)
        for zone in b.Zones():
            if not zone.GetIsRuleArea()or not zone.GetDoNotAllowTracks():continue
            bb=zone.GetBoundingBox();layer=0 if zone.GetLayer()==pcb.F_Cu else 1
            rect(ds[layer],[pcb.ToMM(bb.GetLeft()),pcb.ToMM(bb.GetTop()),pcb.ToMM(bb.GetRight()),pcb.ToMM(bb.GetBottom())],width/2)
        for t in b.GetTracks():
            if t.GetNetname()==net:
                if isinstance(t,pcb.PCB_VIA):
                    for vdraw in vs:line(vdraw,xy(t.GetPosition()),xy(t.GetPosition()),.56)
                continue
            via=isinstance(t,pcb.PCB_VIA);layers=[0,1]if via else[0 if t.GetLayer()==pcb.F_Cu else 1];w=pcb.ToMM(t.GetWidth(pcb.F_Cu)if via else t.GetWidth());g=.62 if t.GetNetname()=='DRAIN_PA'else gap
            for layer in layers:
                line(ds[layer],xy(t.GetStart()),xy(t.GetEnd()),w/2+g+width/2+extra)
                line(vs[layer],xy(t.GetStart()),xy(t.GetEnd()),w/2+g+(.3 if net=='GND'else .4)+extra)
        for d in ds+vs:
            # Board edge plus minimum copper-edge clearance and conservative margin.
            d.rectangle((0,0,NX-1,12),fill=1);d.rectangle((0,NY-13,NX-1,NY-1),fill=1);d.rectangle((0,0,12,NY-1),fill=1);d.rectangle((NX-13,0,NX-1,NY-1),fill=1)
        masks=[q.tobytes()for q in ims];vm=[q.tobytes()for q in vims]
        endpoints=[(e['pos']['x'],e['pos']['y'])for e in ends]
        # Route between actual connected COPPER components, not only the one
        # representative track endpoint printed by DRC. Existing through-vias
        # are legitimate entrances on BOTH layers; do not trap an F.Cu anchor.
        b.BuildConnectivity();conn=b.GetConnectivity();groups=[[o]for o in objs]if a.direct else[list(conn.GetConnectedItems(o))for o in objs]
        if net=='GND' and (D/'development/GND-components-fast.json').exists():
            physical=json.loads((D/'development/GND-components-fast.json').read_text())['groups'];island_ids={r['id']for r in physical[-1]if r['kind']!='zone'};other_ids={r['id']for group in physical[:-1]for r in group if r['kind']!='zone'}
            if uid(objs[0])in island_ids and uid(objs[1])in other_ids:groups=[[items[k]for k in island_ids if k in items],[items[k]for k in other_ids if k in items]]
        if objs[1].m_Uuid.AsString()in{x.m_Uuid.AsString()for x in groups[0]}:
            logs.append(dict(net=net,status='already connected by previous completion'));continue
        def layers(o):return[0,1]if isinstance(o,pcb.PCB_VIA)or(isinstance(o,pcb.PAD)and o.GetAttribute()!=pcb.PAD_ATTRIB_SMD)else[0 if o.IsOnLayer(pcb.F_Cu)else 1]
        candidates=[]
        for group in groups:
            points={}
            for ob in group:
                if ob.GetClass()not in ['PAD','PCB_TRACK','PCB_VIA','PCB_ARC']or ob.GetNetname()!=net:continue
                locs=[xy(ob.GetPosition())]if ob.GetClass()in ['PAD','PCB_VIA']else[xy(ob.GetStart()),xy(ob.GetEnd())]
                for loc in locs:
                    ix,iy=ij(loc)
                    if not(0<=ix<NX and 0<=iy<NY):continue
                    cell=iy*NX+ix
                    for layer in layers(ob):
                        if not masks[layer][cell]:points[(layer,cell)]=loc
            candidates.append(points)
        if not all(candidates):
            logs.append(dict(net=net,status='no clear copper-component anchor'));print(net,logs[-1],flush=True);continue
        ranked=sorted((math.dist(aa,bb),ka,kb)for ka,aa in candidates[0].items()for kb,bb in candidates[1].items())[:256]
        sk={x[1]for x in ranked};gk={x[2]for x in ranked};starts=[l*N+z for l,z in sk];goals={l*N+z for l,z in gk};goalxy=[(z%NX,z//NX)for l,z in gk]
        def h(i):
            z=i%N;xx=z%NX;yy=z//NX
            return min(10*max(abs(xx-gx),abs(yy-gy))+4*min(abs(xx-gx),abs(yy-gy))for gx,gy in goalxy)
        best={s:0 for s in starts};prev={};queue=[(h(s),0,s)for s in starts];heapq.heapify(queue);found=None;expanded=0
        moves=[(1,0,10),(-1,0,10),(0,1,10),(0,-1,10),(1,1,14),(1,-1,14),(-1,1,14),(-1,-1,14)]
        while queue:
            _,cost,i=heapq.heappop(queue)
            if cost!=best.get(i):continue
            if i in goals:found=i;break
            expanded+=1
            if expanded>1000000:break
            layer=i//N;z=i%N;x=z%NX;y=z//NX;mask=masks[layer]
            for dx,dy,w in moves:
                xx=x+dx;yy=y+dy
                if not(0<=xx<NX and 0<=yy<NY):continue
                zz=yy*NX+xx;j=layer*N+zz
                if mask[zz]or(dx and dy and(mask[y*NX+xx]or mask[yy*NX+x])):continue
                c=cost+w
                if c<best.get(j,10**12):best[j]=c;prev[j]=i;heapq.heappush(queue,(c+2*h(j),c,j))
            if not vm[0][z]and not vm[1][z]:
                j=(1-layer)*N+z;c=cost+650
                if c<best.get(j,10**12):best[j]=c;prev[j]=i;heapq.heappush(queue,(c+2*h(j),c,j))
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
        startkey=(ids[0]//N,ids[0]%N);endkey=(ids[-1]//N,ids[-1]%N);endpoints=[candidates[0][startkey],candidates[1][endkey]]
        points=[endpoints[0],pos(ids[0]%N)]
        for i in ids[1:]:
            l=i//N;v=pos(i%N)
            if l!=layer:
                emit(points,layer);via=pcb.PCB_VIA(b);via.SetPosition(pt(*v));via.SetWidth(MM(.6 if net=='GND'else .8));via.SetDrill(MM(.3));via.SetLayerPair(pcb.F_Cu,pcb.B_Cu);via.SetNet(b.FindNet(net));via.SetFrontTentingMode(1);via.SetBackTentingMode(1);b.Add(via);items[uid(via)]=via;vias.append(v);points=[v];layer=l
            else:points.append(v)
        points.append(endpoints[1]);emit(points,layer)
        logs.append(dict(net=net,status='routed',width_mm=width,endpoints_mm=endpoints,segments=pieces,vias_mm=vias,expanded=expanded,elapsed_s=round(time.monotonic()-t0,3)));print(net,'routed',len(pieces),'segments',len(vias),'vias',expanded,'nodes',flush=True)
        pcb.SaveBoard(str(P/(NAME+'.kicad_pcb')),b)
    old=json.loads((D/'local-route-completion.json').read_text())if(D/'local-route-completion.json').exists()else[];old.extend(logs);(D/'local-route-completion.json').write_text(json.dumps(old,indent=2)+'\n')
if __name__=='__main__':main()
