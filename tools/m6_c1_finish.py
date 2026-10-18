#!/usr/bin/python3
"""Preserve routed geometry; sync capture fields, add final status pull, artwork."""
import json,xml.etree.ElementTree as ET,math,argparse
from pathlib import Path
import pcbnew as pcb
from m6_c1_pcb import Board,P,D,MM,pt,xy,bounds,overlap
from m5_2m_design import parse,dump,child,children,Atom
def sync():
    b=Board(True);xml=ET.parse(D/'CTRL.net.xml');cs={c.get('ref'):c for c in xml.findall('./components/comp')};netpins={}
    for n in xml.findall('./nets/net'):
        for v in n.findall('node'):netpins[(v.get('ref'),v.get('pin'))]=n.get('name')
    b.occupied=[bounds(f) for f in b.b.GetFootprints()];b.placed=set(b.f)
    removed=[b.f[r] for r in b.f if r not in b.parts and not r.startswith('H')]
    for item in removed:b.b.Remove(item)
    if removed:
        pcb.SaveBoard(str(P/'CTRL.kicad_pcb'),b.b);b=Board(True);b.occupied=[bounds(f) for f in b.b.GetFootprints()];b.placed=set(b.f)
    for nn in set(netpins.values()):
        if nn not in b.nets:
            item=pcb.NETINFO_ITEM(b.b,nn,b.b.GetNetCount());b.b.Add(item);b.nets[nn]=item
    for r,part in b.parts.items():
        if r not in b.f:
            lib,name=part['footprint'].split(':');f=pcb.FootprintLoad('/usr/share/kicad/footprints/'+lib+'.pretty',name);f.SetReference(r);f.SetFPID(pcb.LIB_ID(lib,name));b.b.Add(f);b.f[r]=f;b.place(r,*{'D21':(32,64),'Q2':(31,57),'R63':(24,46),'R64':(28,58),'R65':(30,60),'R66':(33,57)}.get(r,(64,50)))
        f=b.f[r];lib,name=part['footprint'].split(':');f.SetFPID(pcb.LIB_ID(lib,name));c=cs[r];f.SetValue(part['value']);f.SetPath(pcb.KIID_PATH(c.find('sheetpath').get('tstamps')+c.findtext('tstamps')));f.SetDNP(part['population'] in ['DEBUG','LORA_OPTION_OPEN']);f.Reference().SetLayer(pcb.F_Fab);f.Value().SetVisible(False)
        for pad in f.Pads():
            key=(r,pad.GetNumber())
            if key in netpins:pad.SetNet(b.nets[netpins[key]])
        for prop in c.findall('./fields/field'):
            name=prop.get('name');value=prop.text or ''
            if name in ['Datasheet','Description']:
                f.GetField(pcb.FIELD_T_DATASHEET if name=='Datasheet' else pcb.FIELD_T_DESCRIPTION).SetText(value);continue
            fld=next((x for x in f.GetFields() if x.GetName()==name),None)
            if not fld:fld=pcb.PCB_FIELD(f,pcb.FIELD_T_USER,name);f.Add(fld)
            fld.SetText(value);fld.SetVisible(False)
    b.save()
def stack():
    path=P/'CTRL.kicad_pcb';sx=parse(path.read_text());s=child(sx,'setup');old=child(s,'stackup')
    if old:s.remove(old)
    s.insert(1,parse('''(stackup (layer "F.SilkS" (type "Top Silk Screen") (color "White")) (layer "F.Paste" (type "Top Solder Paste"))
    (layer "F.Mask"(type "Top Solder Mask")(color "Green")(thickness .01))
    (layer "F.Cu"(type "copper")(thickness .035))
    (layer "dielectric 1"(type "core")(thickness 1.51)(material "FR4")(epsilon_r 4.5)(loss_tangent .02))
    (layer "B.Cu"(type "copper")(thickness .035))
    (layer "B.Mask"(type "Bottom Solder Mask")(color "Green")(thickness .01))
    (layer "B.Paste"(type "Bottom Solder Paste")) (layer "B.SilkS"(type "Bottom Silk Screen")(color "White"))
    (copper_finish "Lead-free HASL")(dielectric_constraints no))'''))
    path.write_text(dump(sx)+'\n')
def artwork():
    b=Board(True);removed=[]
    # Crowded vendor outlines become assembly artwork. Only legible, clear
    # references are placed on the final legend; no silkscreen DRC exclusions.
    for f in b.b.GetFootprints():
        for g in f.GraphicalItems():
            if g.GetLayer()==pcb.F_SilkS:g.SetLayer(pcb.F_Fab)
    mask=[]
    for f in b.b.GetFootprints():
        for a in f.Pads():
            if a.IsOnLayer(pcb.F_Mask):
                bb=a.GetBoundingBox();bb.Inflate(MM(.24));mask.append(bb)
    placed=[];labels=[]
    def okay(t):
        box=t.GetBoundingBox();box.Inflate(MM(.05))
        return pcb.ToMM(box.GetLeft())>20.3 and pcb.ToMM(box.GetTop())>20.3 and pcb.ToMM(box.GetRight())<119.7 and pcb.ToMM(box.GetBottom())<119.7 and not any(box.Intersects(z) for z in mask+placed)
    def label(text,x,y,size=1):
        t=pcb.PCB_TEXT(b.b);t.SetText(text);t.SetPosition(pt(x,y));t.SetTextSize(pt(size,size));t.SetTextThickness(MM(.15));t.SetLayer(pcb.F_SilkS)
        if okay(t):b.b.Add(t);placed.append(t.GetBoundingBox());return True
        return False
    for f in sorted(b.b.GetFootprints(),key=lambda f:(not f.GetReference().startswith(('J','U','SW')),f.GetReference())):
        r=f.GetReference();x,y=xy(f.GetPosition());bb=bounds(f,0)
        for xx,yy in [(x,bb[1]-.8),(x,bb[3]+.8),(bb[0]-1.8,y),(bb[2]+1.8,y)]+[(x+dx,y+dy) for dy in [-3,3,-5,5] for dx in [-2,2,-4,4]]:
            if label(r,xx,yy):labels.append(r);break
    for text,x,y,size in [('ARDF-TX M6-C1',88,22.5,1.2),('REVIEW ONLY',92,60,1),('STOP',108,101.5,1),('START',100,117.5,1),('1',25.5,74,1),('1',107.5,74,1)]:label(text,x,y,size)
    pcb.SaveBoard(str(P/'CTRL.kicad_pcb'),b.b);(D/'legend-coverage.json').write_text(json.dumps({'silk_references':labels,'other_references':'F.Fab assembly drawings; no purchasing symbol implied for copper test points'},indent=2)+'\n')
def settings():
    path=P/'CTRL.kicad_pro';d=json.loads(path.read_text());ds=d['board']['design_settings'];sev=ds['rule_severities']
    for k in ['missing_courtyard','footprint_filters_mismatch','footprint_type_mismatch','track_not_centered_on_via']:sev[k]='warning'
    sev['connection_width']='error';sev['copper_sliver']='error';sev['hole_to_hole']='error';ds['drc_exclusions']=[];r=ds['rules'];r.update(min_connection=.15,min_text_height=1.0,min_text_thickness=.15,min_silk_clearance=.15,solder_mask_to_copper_clearance=.09,min_hole_clearance=.25,min_hole_to_hole=.25)
    path.write_text(json.dumps(d,indent=2)+'\n')
def main():
    a=argparse.ArgumentParser();a.add_argument('--sync',action='store_true');a.add_argument('--artwork',action='store_true');a.add_argument('--stack',action='store_true');a.add_argument('--settings',action='store_true');x=a.parse_args()
    if x.sync:sync()
    if x.artwork:artwork()
    if x.stack:stack()
    if x.settings:settings()
if __name__=='__main__':main()
