#!/usr/bin/python3
"""Read-only compact-board ground-region and mechanical-interface evidence.
Filled-polygon connectivity is CAD evidence, not RF return impedance validation.
"""
import collections,json,math
import pcbnew as p
from m4a_design import P,D,NAME
from m3b_pcb import xy

def main():
    b=p.LoadBoard(str(P/(NAME+'.kicad_pcb')));zs=list(b.Zones());parent={};details={}
    def find(i):
        parent.setdefault(i,i)
        if parent[i]!=i:parent[i]=find(parent[i])
        return parent[i]
    def join(ids):
        if ids:
            a=find(ids[0])
            for i in ids[1:]:parent[find(i)]=a
    def at(v,layer):
        return[(zi,i)for zi,z in enumerate(zs)if z.GetLayer()==layer for i in range(z.GetFilledPolysList(layer).OutlineCount())if z.GetFilledPolysList(layer).Contains(v,i)]
    for zi,z in enumerate(zs):
        ps=z.GetFilledPolysList(z.GetLayer())
        for i in range(ps.OutlineCount()):
            key=(zi,i);find(key);poly=ps.COutline(i);vs=[poly.CPoint(j)for j in range(poly.PointCount())];details[key]=dict(layer=b.GetLayerName(z.GetLayer()),bounds_mm=[round(p.ToMM(x),4)for x in(min(v.x for v in vs),min(v.y for v in vs),max(v.x for v in vs),max(v.y for v in vs))],pads=[])
    vias=[];returns=[]
    for t in b.GetTracks():
        if t.GetNetname()!='GND':continue
        ids=[i for l in([p.F_Cu,p.B_Cu]if isinstance(t,p.PCB_VIA)else[t.GetLayer()])for v in(t.GetStart(),t.GetEnd())for i in at(v,l)];join(ids)
        if isinstance(t,p.PCB_VIA):vias.append(xy(t.GetPosition()))
    for f in b.GetFootprints():
        for pad in f.Pads():
            if pad.GetNetname()!='GND':continue
            ids=at(pad.GetPosition(),p.F_Cu)+([]if pad.GetAttribute()==p.PAD_ATTRIB_SMD else at(pad.GetPosition(),p.B_Cu));assert ids,(f.GetReference(),pad.GetNumber(),'ground pad outside connected pour');join(ids)
            for i in ids:details[i]['pads'].append(f.GetReference()+'.'+pad.GetNumber())
            v=xy(pad.GetPosition());near=min(vias,key=lambda q:math.dist(v,q));returns.append(dict(reference=f.GetReference(),pin=pad.GetNumber(),position_mm=v,nearest_ground_via_mm=near,straight_distance_mm=round(math.dist(v,near),3),metric_limit='Euclidean distance only; not routed loop length/inductance'))
    groups=collections.defaultdict(list)
    for k,v in details.items():groups[str(find(k))].append(v)
    assert len(groups)==1,('Disconnected filled ground regions',len(groups))
    report=dict(revision='M4A-V1',filled_ground_region_groups=len(groups),polygon_regions=len(details),ordinary_ground_vias=len(vias),regions=dict(groups),ground_pad_nearest_via=returns,physical_return_impedance='NOT_RUN; connected polygons do not prove low-inductance RF return or acceptable digital ground bounce')
    (D/'ground-connectivity.json').write_text(json.dumps(report,indent=2)+'\n')
    fs={f.GetReference():f for f in b.GetFootprints()};svg=['<svg xmlns="http://www.w3.org/2000/svg" viewBox="-15 -15 185 155">','<rect x="-15" y="-15" width="185" height="155" fill="white"/>','<g font-family="sans-serif" font-size="2.5" fill="#111">','<text x="0" y="-8">RF80 V1 / 150 x 110 mm / PRODUCTION-INTENT - NOT RELEASED</text>','<rect width="150" height="110" fill="#f0f5f0" stroke="#111" stroke-width="0.3"/>']
    for r in('H1','H2','H3','H4'):
        x,y=xy(fs[r].GetPosition());x-=20;y-=20;svg.append(f'<circle cx="{x}" cy="{y}" r="1.6" fill="white" stroke="black" stroke-width="0.2"/><text x="{x+2}" y="{y}">{r} ({x:g},{y:g})</text>')
    for r in('J101','J301','J401','J502','Q402','Q403','T401','L410','L411','U101','U501'):
        f=fs[r];q=f.GetBoundingBox(False,False);x,y=p.ToMM(q.GetLeft())-20,p.ToMM(q.GetTop())-20;w,h=p.ToMM(q.GetWidth()),p.ToMM(q.GetHeight());svg.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="#b8cad5" fill-opacity="0.5" stroke="#345" stroke-width="0.15"/><text x="{x}" y="{y-1}">{r}</text>')
    svg+=['<text x="0" y="116">Module coordinates: top view, upper-left profile origin; +X right, +Y down.</text>','<text x="0" y="121">M3: 4 x 3.20 mm NPTH; mounting pattern 140 x 100 mm. Thickness 1.6 mm nominal.</text>','<text x="0" y="126">Rects show native footprint drawing envelopes; actual heatsink/harness volumes remain OPEN.</text>','<text x="0" y="131">Initial allowances: 25 mm thermal height / 30 mm cable height / 20 mm exit / 10 mm below.</text>','<text x="0" y="136">ST Q403 illustrated face +Y; insulated IRF610 drain tab; remote insulated NTC.</text>','</g></svg>']
    (D/'mechanical-interface.svg').write_text('\n'.join(svg)+'\n')
    # All 3D filenames must resolve; a resolved envelope is not supplier qualification.
    resolved=0
    from pathlib import Path
    for f in b.GetFootprints():
        for m in f.Models():
            q=m.m_Filename.replace('${KIPRJMOD}',str(P)).replace('${KICAD10_3DMODEL_DIR}','/usr/share/kicad/3dmodels');assert Path(q).is_file(),q;resolved+=1
    print('PASS one connected ground network;',len(details),'filled polygons;',len(vias),'ground vias;',resolved,'3D model references resolve')
if __name__=='__main__':main()
