#!/usr/bin/python3
"""Ordinary ground fanout/planes and readable compact assembly markings.
Read/write only production RF80_V1; frozen E2 never changed.
"""
import json,math
import pcbnew as pcb
from m4a_design import P,D,NAME,MM
from m3b_pcb import pt,xy,bbox,intersects
from m3b_ground_fanout import point_segment,segdist,seg_box
def main():
    b=pcb.LoadBoard(str(P/(NAME+'.kicad_pcb')));removed=[t for t in b.GetTracks()if t.GetNetname()=='GND']+list(b.Zones())
    for x in removed:b.Remove(x)
    f={q.GetReference():q for q in b.GetFootprints()};pads=[p for q in f.values()for p in q.Pads()];obstacles=[(p.GetNetname(),bbox_pad(p))for p in pads]
    tracks=[(t.GetNetname(),xy(t.GetStart()),xy(t.GetEnd()),pcb.ToMM(t.GetWidth()),t.GetLayer())for t in b.GetTracks()if not isinstance(t,pcb.PCB_VIA)]
    vias=[(t.GetNetname(),xy(t.GetPosition()),pcb.ToMM(t.GetWidth(pcb.F_Cu))/2)for t in b.GetTracks()if isinstance(t,pcb.PCB_VIA)]
    newvias=[];connections=[];plane_only=[]
    for pad in pads:
        if pad.GetNetname()!='GND'or pad.GetAttribute()!=pcb.PAD_ATTRIB_SMD:continue
        a=xy(pad.GetPosition());center=xy(pad.GetParentFootprint().GetPosition());choices=[v for v in newvias if math.dist(a,v)<5]+[center]
        for d in(1.,1.4,1.8,2.2,2.6,3.,3.6,4.2,5.,6.):choices.extend((a[0]+dx,a[1]+dy)for dx,dy in[(d,0),(-d,0),(0,d),(0,-d),(d,d),(-d,-d),(d,-d),(-d,d)])
        choice=None
        for v in choices:
            if not(21<v[0]<169 and 21<v[1]<129):continue
            bad=False
            for n,box in obstacles:
                g=.91 if n=='DRAIN_PA'else .47
                if box[0]-g<v[0]<box[2]+g and box[1]-g<v[1]<box[3]+g:bad=True;break
                if n!='GND':
                    g=.76 if n=='DRAIN_PA'else .30
                    if seg_box(a,v,[box[0]-g,box[1]-g,box[2]+g,box[3]+g]):bad=True;break
            if bad:continue
            for n,c,d,w,layer in tracks:
                g=.65 if n=='DRAIN_PA'else .17
                if point_segment(v,c,d)<w/2+.30+g or(layer==pcb.F_Cu and segdist(a,v,c,d)<w/2+.14+g):bad=True;break
            if bad:continue
            for n,c,rad in vias:
                g=.65 if n=='DRAIN_PA'else .17
                if math.dist(v,c)<rad+.30+g or point_segment(c,a,v)<rad+.14+g:bad=True;break
            if bad:continue
            choice=v;break
        if not choice:
            # A nearby continuous top pour can be the local return. Do not
            # force a via through another signal/pad; final DRC must establish
            # connectivity and the review records these plane-dependent pads.
            plane_only.append(dict(reference=pad.GetParentFootprint().GetReference(),pin=pad.GetNumber(),position_mm=a));continue
        if choice not in newvias:
            v=pcb.PCB_VIA(b);v.SetPosition(pt(*choice));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(b.FindNet('GND'));v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.Add(v);newvias.append(choice)
        t=pcb.PCB_TRACK(b);t.SetStart(pt(*a));t.SetEnd(pt(*choice));t.SetWidth(MM(.28));t.SetLayer(pcb.F_Cu);t.SetNet(b.FindNet('GND'));b.Add(t);connections.append(dict(reference=pad.GetParentFootprint().GetReference(),pin=pad.GetNumber(),pad_mm=a,via_mm=choice))
    for layer in(pcb.F_Cu,pcb.B_Cu):
        z=pcb.ZONE(b);z.SetLayer(layer);z.SetNet(b.FindNet('GND'));z.SetLocalClearance(MM(.20));z.SetPadConnection(pcb.ZONE_CONNECTION_FULL);z.SetThermalReliefGap(MM(.25));z.SetThermalReliefSpokeWidth(MM(.35));z.SetMinThickness(MM(.2));z.SetZoneName('V1 GND '+b.GetLayerName(layer));poly=z.Outline();poly.NewOutline()
        for x,y in((20.5,20.5),(169.5,20.5),(169.5,129.5),(20.5,129.5)):poly.Append(MM(x),MM(y))
        b.Add(z)
    ds=b.GetDesignSettings();ds.m_SolderMaskMinWidth=MM(.10)
    # Rebuild free labels; never alter component values, fields, pins or placement.
    deleted=[x for x in b.GetDrawings()if isinstance(x,pcb.PCB_TEXT)]
    for x in deleted:b.Remove(x)
    padboxes=[];occupied=[]
    for q in f.values():
        for p in q.Pads():
            a=bbox_pad(p);padboxes.append([a[0]-.2,a[1]-.2,a[2]+.2,a[3]+.2])
        for g in q.GraphicalItems():
            if g.GetLayer()==pcb.F_SilkS:
                q=g.GetBoundingBox();occupied.append([pcb.ToMM(q.GetLeft())-.2,pcb.ToMM(q.GetTop())-.2,pcb.ToMM(q.GetRight())+.2,pcb.ToMM(q.GetBottom())+.2])
    def label(text,x,y,size=.8,layer=pcb.F_SilkS):
        t=pcb.PCB_TEXT(b);t.SetText(text);t.SetPosition(pt(x,y));t.SetTextSize(pt(size,size));t.SetTextThickness(MM(.12));t.SetLayer(layer);b.Add(t);return t
    for text,x,y,size in [('RF80 V1 / PRODUCTION-INTENT - NOT RELEASED',96,21.4,.8),('CTRL 3V3',29,49,.8),('4S + PIN1',82,23,.8),('NORMAL',161,97,.8),('FOX 10mW',150,128,.8)]:
        t=label(text,x,y,size);q=t.GetBoundingBox();occupied.append([pcb.ToMM(q.GetLeft())-.2,pcb.ToMM(q.GetTop())-.2,pcb.ToMM(q.GetRight())+.2,pcb.ToMM(q.GetBottom())+.2])
    missing=[]
    for r,foot in sorted(f.items()):
        if r.startswith('H'):
            foot.Reference().SetLayer(pcb.F_Fab);continue
        q=foot.GetBoundingBox(False,False);cx=(pcb.ToMM(q.GetLeft())+pcb.ToMM(q.GetRight()))/2;cy=(pcb.ToMM(q.GetTop())+pcb.ToMM(q.GetBottom()))/2
        candidates=[]
        for d in(.8,1.2,1.8,2.4,3.2,4.):candidates.extend([(cx,pcb.ToMM(q.GetTop())-d),(cx,pcb.ToMM(q.GetBottom())+d),(pcb.ToMM(q.GetRight())+len(r)*.36+d,cy),(pcb.ToMM(q.GetLeft())-len(r)*.36-d,cy)])
        for x,y in candidates:
            rect=[x-len(r)*.36-.3,y-.8,x+len(r)*.36+.3,y+.8]
            if rect[0]<21 or rect[1]<23 or rect[2]>169 or rect[3]>128:continue
            if any(intersects(rect,o)for o in padboxes+occupied):continue
            label(r,x,y);occupied.append(rect);break
        else:missing.append(r)
    label('Q403 ST:1B2C3E; illustrated face +PCB Y',116,98,.8,pcb.F_Fab)
    label('TH301 remote on INSULATED PA case; board landing only',107,128,.8,pcb.F_Fab)
    b.BuildConnectivity();pcb.ZONE_FILLER(b).Fill(b.Zones());pcb.SaveBoard(str(P/(NAME+'.kicad_pcb')),b)
    (D/'ground-return.json').write_text(json.dumps(dict(vias_mm=newvias,pad_connections=connections,plane_connected_without_local_via=plane_only,non_VIP=True),indent=2)+'\n');(D/'assembly-markings.json').write_text(json.dumps(dict(silk_refs_without_free_space=missing,assembly_authority='F.Fab PDF retains all references; no suppressed DRC',mask_minimum_web_mm=.10),indent=2)+'\n')
    print('Ground planes/fanout:',len(newvias),'ordinary vias;',len(connections),'SMD returns;',len(missing),'refs use assembly artwork')
def bbox_pad(p):
    q=p.GetBoundingBox();return[pcb.ToMM(q.GetLeft()),pcb.ToMM(q.GetTop()),pcb.ToMM(q.GetRight()),pcb.ToMM(q.GetBottom())]
if __name__=='__main__':main()
