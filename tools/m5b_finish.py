#!/usr/bin/python3
"""Synchronize exact landings, qualified solder proposal, thermal access and labels.
Native files only. Does not touch earlier review packages or RF80.
"""
import copy,json,math,uuid
from pathlib import Path
import pcbnew as pcb
import m5a_r1_design as c
from m5b_pcb import P,D,MM,pt,xy,box,overlap

def paste(s,x,y,w,h):
    s.append(c.parse('(fp_rect(start '+str(x-w/2)+' '+str(y-h/2)+')(end '+str(x+w/2)+' '+str(y+h/2)+')(stroke(width 0)(type default))(fill solid)(layer "F.Paste"))'))
def landings():
    # Geometry from manufacturers remains unchanged; only explicit segmented
    # stencil windows are added. These are engineering stencil proposals.
    for name in ['PD54008L_ST_GDS_5x5','PHA1_DF782_RevG']:
        path=P/'ARDF_2M.pretty'/(name+'.kicad_mod');s=c.parse(path.read_text())
        for g in list(c.children(s,'fp_rect')):
            if c.child(g,'layer')[1]=='F.Paste':s.remove(g)
        if name.startswith('PD'):
            for yy in [-1.6,0,1.6]:paste(s,0,yy,.6,1.2)
            for xx in [-1.125,1.125]:paste(s,xx,0,.35,4.4)
        else:
            for xx in [-.6,.6]:paste(s,xx,-3.6,.4,1.95)
            paste(s,0,-4.95,1.3,.4);paste(s,0,-1.78,.65,.25)
            for g in c.children(s,'fp_circle'):
                c.child(g,'center')[1:]=[c.Atom('-2.65'),c.Atom('-.2')];c.child(g,'end')[1:]=[c.Atom('-2.5'),c.Atom('-.2')]
        path.write_text(c.dump(s)+'\n')

def synchronize():
    landings();path=P/'RF2M.kicad_pcb';s=c.parse(path.read_text());parts={p['ref']:p for p in json.load(open(P/'RF2M.electrical.json'))['parts']};moved=[]
    for old in list(c.children(s,'footprint')):
        props={p[1]:p for p in c.children(old,'property')};ref=props['Reference'][2]
        if ref not in parts:continue
        p=parts[ref]
        if ref in ['L604','L641','L642','L643','Q501','U501']or ref.startswith('TL'):
            netmap={a[1]:copy.deepcopy(c.child(a,'net'))for a in c.children(old,'pad')if a[1]and c.child(a,'net')}
            lib,name=p['footprint'].split(':');new=c.parse((P/(lib+'.pretty')/(name+'.kicad_mod')).read_text());new[1]=p['footprint']
            if ref.startswith('TL'):
                attr=c.child(new,'attr');attr.extend([c.Atom('exclude_from_bom'),c.Atom('exclude_from_pos_files')])
            for it in list(new[2:]):
                if isinstance(it,list)and(it[0]=='property'or(it[0]=='fp_text'and it[1]in ['reference','value'])):new.remove(it)
            for it in old[2:]:
                if isinstance(it,list)and it[0]in ['at','uuid','path','property','dnp']:new.append(copy.deepcopy(it))
            for pa in c.children(new,'pad'):
                if pa[1]in netmap:pa.append(netmap[pa[1]])
            idx=s.index(old);s[idx]=new;old=new;props={p[1]:p for p in c.children(old,'property')}
        for label,key in [('Value','value'),('MPN','mpn'),('Population','population'),('Function','group'),('Engineering_Note','note'),('Datasheet','source_url')]:
            if label in props:props[label][2]=p[key]
        if ref in ['L604','C603','C604']:
            target={'L604':[84.8,45.2,180],'C603':[90,39,90],'C604':[90,43,90]}[ref];a=c.child(old,'at');prev=list(map(float,a[1:]))
            if prev[:2]!=target[:2]:moved.append(dict(ref=ref,old=prev,new=target));a[1:]=[c.Atom(str(v))for v in target]
    # Remove former feed traces when the changed physical choke was first moved.
    # Recreate only the fixed RF connection; supply/return gaps use native DRC.
    if moved:
        for t in list(c.children(s,'segment')):
            netcode=c.child(t,'net')[1]
            # KiCad10 emits net codes; retrieve exact names from pad records.
            netmap={c.child(pa,'net')[1]:(c.child(pa,'net')[2]if len(c.child(pa,'net'))>2 else c.child(pa,'net')[1])for fp in c.children(s,'footprint')for pa in c.children(fp,'pad')if c.child(pa,'net')}
            n=netmap.get(netcode,'')
            if n in ['MMIC_RF_DC','VDRV_MMIC']:s.remove(t)
            elif n=='GND':
                pts=[list(map(float,c.child(t,k)[1:]))for k in ['start','end']]
                old_ground=[(90,62.225),(87,62.225)]
                if any(math.dist(p,q)<.01 for p in pts for q in old_ground):s.remove(t)
        (D/'localized-placement-changes.json').write_text(json.dumps(moved,indent=2)+'\n')
    # Explicit stack-up, ordinary two-layer 0.8mm nominal finished board.
    setup=c.child(s,'setup');st=c.child(setup,'stackup')
    if st:setup.remove(st)
    setup.append(c.parse('''(stackup
      (layer "F.SilkS"(type "Top Silk Screen"))
      (layer "F.Paste"(type "Top Solder Paste"))
      (layer "F.Mask"(type "Top Solder Mask")(thickness 0.01))
      (layer "F.Cu"(type "copper")(thickness 0.07))
      (layer "dielectric 1"(type "core")(thickness 0.64)(material "FR4")(epsilon_r 4.3)(loss_tangent 0.02))
      (layer "B.Cu"(type "copper")(thickness 0.07))
      (layer "B.Mask"(type "Bottom Solder Mask")(thickness 0.01))
      (layer "B.Paste"(type "Bottom Solder Paste"))
      (layer "B.SilkS"(type "Bottom Silk Screen"))
      (copper_finish "ENIG")(dielectric_constraints no))'''))
    # h is copper-to-return-plane spacing, not finished thickness. The RF
    # calculation uses this exact0.64mm dielectric proposal, not0.8mm finished.
    path.write_text(c.dump(s)+'\n')
    b=pcb.LoadBoard(str(path));fs={f.GetReference():f for f in b.GetFootprints()}
    if moved:
        def pa(r,pn):return next(p for p in fs[r].Pads()if p.GetNumber()==pn)
        def link(a,b1,width=.4):
            t=pcb.PCB_TRACK(b);t.SetStart(a.GetPosition());t.SetEnd(b1.GetPosition());t.SetWidth(MM(width));t.SetLayer(pcb.F_Cu);t.SetNet(a.GetNet());t.SetLocked(True);b.Add(t)
        link(pa('U501','3'),pa('C602','1'));link(pa('L604','2'),pa('C602','1'))
        for ref in ['C603','C604']:
            g=pa(ref,'2');x,y=xy(g.GetPosition());v=pcb.PCB_VIA(b);v.SetPosition(pt(x+.8,y));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(b.FindNet('GND'));v.SetLocked(True);b.Add(v)
            t=pcb.PCB_TRACK(b);t.SetStart(g.GetPosition());t.SetEnd(v.GetPosition());t.SetWidth(MM(.25));t.SetLayer(pcb.F_Cu);t.SetNet(b.FindNet('GND'));t.SetLocked(True);b.Add(t)
    # Replace six centered source vias with twelve ordinary .6/.3mm contacts.
    remove=[t for t in b.GetTracks()if isinstance(t,pcb.PCB_VIA)and abs(pcb.ToMM(t.GetPosition().x)-112)<.01 and 52.8<pcb.ToMM(t.GetPosition().y)<57.2]
    for t in remove:b.Remove(t)
    existing=[xy(t.GetPosition())for t in b.GetTracks()if isinstance(t,pcb.PCB_VIA)]
    for x in [111.35,112.65]:
      for y in [53,53.8,54.6,55.4,56.2,57.0]:
        if any(math.dist((x,y),a)<.1 for a in existing):continue
        v=pcb.PCB_VIA(b);v.SetPosition(pt(x,y));v.SetWidth(MM(.6));v.SetDrill(MM(.3));v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(b.FindNet('GND'));v.SetFrontTentingMode(1);v.SetBackTentingMode(1);v.SetLocked(True);b.Add(v)
    from m5b_footprints import width50
    for t in b.GetTracks():
        if not isinstance(t,pcb.PCB_VIA)and abs(pcb.ToMM(t.GetWidth())-1.409)<.001:t.SetWidth(MM(width50()))
    pcb.SaveBoard(str(path),b)
    print('Synchronized footprints/values;source stencil and12source vias;localized moves',len(moved))

def labels():
    b=pcb.LoadBoard(str(P/'RF2M.kicad_pcb'));parts={p['ref']:p for p in json.load(open(P/'RF2M.electrical.json'))['parts']}
    removed=[x for x in b.GetDrawings()if isinstance(x,pcb.PCB_TEXT)]
    for x in removed:b.Remove(x)
    pads=[];texts=[];skipped=[]
    for f in b.GetFootprints():
      for p in f.Pads():
        if not(p.IsOnLayer(pcb.F_Cu)or p.IsOnLayer(pcb.F_Mask)):continue
        q=p.GetBoundingBox();pads.append([pcb.ToMM(q.GetLeft())-.22,pcb.ToMM(q.GetTop())-.22,pcb.ToMM(q.GetRight())+.22,pcb.ToMM(q.GetBottom())+.22])
      for g in f.GraphicalItems():
        if g.GetLayer()!=pcb.F_SilkS:continue
        q=g.GetBoundingBox();texts.append([pcb.ToMM(q.GetLeft())-.2,pcb.ToMM(q.GetTop())-.2,pcb.ToMM(q.GetRight())+.2,pcb.ToMM(q.GetBottom())+.2])
    def put(text,x,y,size=.8,layer=pcb.F_SilkS):
        t=pcb.PCB_TEXT(b);t.SetText(text);t.SetPosition(pt(x,y));t.SetTextSize(pt(size,size));t.SetTextThickness(MM(.12));t.SetLayer(layer);b.Add(t);return t
    for text,x,y,size in [('ARDF-TX RF2M / M5B-E1 EVALUATION',108,23,1.2),('NOT RELEASED / UNBUILT / REVIEW ONLY',112,157,1),('3V3 LOGIC ONLY',38,73,.8),('PACK +1 GND2',35,146,.8),('2S BOOST OR 4S BUCK / EXCLUSIVE',78,152,.9),('NORMAL 50R',186,62,.9),('TRAIN uW MMCX',187,148,.9),('INSULATED PASS SINK',180,23,.8),('NTC TO PASS CASE',174,30,.8)]:
        t=put(text,x,y,size);q=t.GetBoundingBox();texts.append([pcb.ToMM(q.GetLeft())-.2,pcb.ToMM(q.GetTop())-.2,pcb.ToMM(q.GetRight())+.2,pcb.ToMM(q.GetBottom())+.2])
    for f in b.GetFootprints():
        ref=f.GetReference()
        if ref.startswith(('H','TL')):continue
        q=f.GetBoundingBox(False,False);cx=(pcb.ToMM(q.GetLeft())+pcb.ToMM(q.GetRight()))/2;cy=(pcb.ToMM(q.GetTop())+pcb.ToMM(q.GetBottom()))/2
        for d in [1.1,1.6,2.1,2.8,3.6,4.5,6.]:
            options=[(cx,pcb.ToMM(q.GetTop())-d),(cx,pcb.ToMM(q.GetBottom())+d),(pcb.ToMM(q.GetRight())+len(ref)*.26+d,cy),(pcb.ToMM(q.GetLeft())-len(ref)*.26-d,cy)]
            chosen=None
            for x,y in options:
                bb=[x-len(ref)*.36-.3,y-.8,x+len(ref)*.36+.3,y+.8]
                if bb[0]<21 or bb[2]>199 or bb[1]<27 or bb[3]>154:continue
                if any(overlap(bb,v)for v in pads+texts):continue
                chosen=(x,y,bb);break
            if chosen:break
        if chosen:
            x,y,bb=chosen;put(ref,x,y);texts.append(bb)
        else:skipped.append(ref)
    pcb.SaveBoard(str(P/'RF2M.kicad_pcb'),b);(D/'silkscreen-disposition.json').write_text(json.dumps(dict(omitted_ref_labels=skipped,reason='Crowded references remain on complete F.Fab assembly drawing;no suppression of mask/silk checks'),indent=2)+'\n')
if __name__=='__main__':
    import argparse
    a=argparse.ArgumentParser();a.add_argument('--labels',action='store_true');x=a.parse_args();labels()if x.labels else synchronize()
