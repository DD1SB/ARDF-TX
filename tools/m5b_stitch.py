#!/usr/bin/python3
"""Connect actual filled compact ground regions with ordinary clear stitching vias.
Reports remaining disconnected regions rather than suppressing them. Retains
all existing signal routes; native DRC must pass after this geometry operation.
"""
import collections,json,math
import pcbnew as p
from m5b_pcb import P,D,MM
NAME='RF2M'
from m3b_pcb import pt,xy
from m3b_ground_fanout import point_segment

def main():
    b=p.LoadBoard(str(P/(NAME+'.kicad_pcb')));removed=[];moved=[]
    # Consolidate duplicate same-net through-vias: preserve the pre-existing
    # drill landing and join every affected endpoint to that landing.
    # Preserve deliberately placed component/source vias; add stitches only.
    zs=list(b.Zones());parent={};details={}
    def find(i):
        parent.setdefault(i,i)
        if parent[i]!=i:parent[i]=find(parent[i])
        return parent[i]
    def join(ids):
        if ids:
            root=find(ids[0])
            for i in ids[1:]:parent[find(i)]=root
    def at(v,layer):
        return[(zi,i)for zi,z in enumerate(zs)if z.GetLayer()==layer for i in range(z.GetFilledPolysList(layer).OutlineCount())if z.GetFilledPolysList(layer).Contains(v,i)]
    for zi,z in enumerate(zs):
        ps=z.GetFilledPolysList(z.GetLayer())
        for i in range(ps.OutlineCount()):
            key=(zi,i);find(key);poly=ps.COutline(i);vs=[poly.CPoint(j)for j in range(poly.PointCount())];details[key]=[min(v.x for v in vs),min(v.y for v in vs),max(v.x for v in vs),max(v.y for v in vs)]
    for t in b.GetTracks():
        if t.GetNetname()=='GND':join([i for l in([p.F_Cu,p.B_Cu]if isinstance(t,p.PCB_VIA)else[t.GetLayer()])for v in(t.GetStart(),t.GetEnd())for i in at(v,l)])
    pads=[q for f in b.GetFootprints()for q in f.Pads()if q.IsOnLayer(p.F_Cu)or q.IsOnLayer(p.B_Cu)]
    for pad in pads:
        if pad.GetNetname()=='GND':join(at(pad.GetPosition(),p.F_Cu)+([]if pad.GetAttribute()==p.PAD_ATTRIB_SMD else at(pad.GetPosition(),p.B_Cu)))
    obstacles=[t for t in b.GetTracks()if t.GetNetname()!='GND'];stitches=[]
    def safe(v):
        x,y=xy(v)
        for pad in pads:
            bb=pad.GetBoundingBox();g=-.33 if pad.GetNetname()=='GND'else .92 if pad.GetNetname()=='DRAIN_PA'else .47
            if p.ToMM(bb.GetLeft())-g<x<p.ToMM(bb.GetRight())+g and p.ToMM(bb.GetTop())-g<y<p.ToMM(bb.GetBottom())+g:return False
        for t in obstacles:
            rad=p.ToMM(t.GetWidth(p.F_Cu)if isinstance(t,p.PCB_VIA)else t.GetWidth())/2;gap=.62 if t.GetNetname()=='DRAIN_PA'else .17
            if point_segment((x,y),xy(t.GetStart()),xy(t.GetEnd()))<rad+.30+gap:return False
        for t in b.GetTracks():
            if isinstance(t,p.PCB_VIA)and math.dist((x,y),xy(t.GetPosition()))<.60:return False
        return True
    mainkey=max(details,key=lambda k:(details[k][2]-details[k][0])*(details[k][3]-details[k][1]))
    for key,bb in sorted(details.items(),key=lambda kv:(kv[1][2]-kv[1][0])*(kv[1][3]-kv[1][1])):
        if len({find(k)for k in parent})==1:break
        if find(key)==find(mainkey):continue
        cx=(bb[0]+bb[2])/2;cy=(bb[1]+bb[3])/2;points=[]
        for x in range(int(p.ToMM(bb[0])*5)+1,int(p.ToMM(bb[2])*5)):
            for y in range(int(p.ToMM(bb[1])*5)+1,int(p.ToMM(bb[3])*5)):
                v=pt(x/5,y/5);points.append(((v.x-cx)**2+(v.y-cy)**2,v))
        for _,v in sorted(points,key=lambda q:q[0]):
            ids=at(v,p.F_Cu)+at(v,p.B_Cu)
            if key not in ids or len({find(k)for k in ids})<2 or not safe(v):continue
            via=p.PCB_VIA(b);via.SetPosition(v);via.SetWidth(MM(.6));via.SetDrill(MM(.3));via.SetLayerPair(p.F_Cu,p.B_Cu);via.SetNet(b.FindNet('GND'));via.SetFrontTentingMode(1);via.SetBackTentingMode(1);b.Add(via);join(ids);stitches.append(xy(v));break
    groups=collections.defaultdict(list)
    for key,bb in details.items():groups[str(find(key))].append([round(p.ToMM(x),3)for x in bb])
    b.BuildConnectivity();p.ZONE_FILLER(b).Fill(b.Zones());p.SaveBoard(str(P/(NAME+'.kicad_pcb')),b)
    report=dict(stitch_vias_mm=stitches,same_net_drill_consolidation=moved,ground_region_groups=len(groups),remaining_regions=dict(groups));(D/'ground-region-stitching.json').write_text(json.dumps(report,indent=2)+'\n');print('Added',len(stitches),'ground stitching vias; ground groups',len(groups),'consolidated',len(moved),'duplicate drills')
if __name__=='__main__':main()
