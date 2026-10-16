#!/usr/bin/python3
"""Manufacturing-driven E2->E3 native implementation;never writes history."""
import copy,json,math,uuid
import pcbnew as p
import m5a_r1_design as c
from m5b_e3_common import *
MM=p.FromMM

def pt(x,y):return p.VECTOR2I(MM(x),MM(y))
def xy(v):return(p.ToMM(v.x),p.ToMM(v.y))
def apply():
 guard();board=HW/'RF2M.kicad_pcb';b=p.LoadBoard(str(board));assert b.GetTitleBlock().GetRevision()=='M5B-E2','Apply once to E2;do not reset a partially revised board'
 fs={f.GetReference():f for f in b.GetFootprints()};data=json.loads((HW/'RF2M.electrical.json').read_text());parts={x['ref']:x for x in data['parts']};ports={};changes=[]
 def pad(ref,n):return next(a for a in fs[ref].Pads()if a.GetNumber()==n)
 # Capture original physical endpoints before any placement changes.
 oldpads={(ref,a.GetNumber()):(xy(a.GetPosition()),a.GetNetname())for ref,f in fs.items()for a in f.Pads()if a.GetNumber()}
 # Actual bodyless copper geometries,with butt ends to avoid wide round-cap
 # shorts across series matching capacitors. Pin planes remain explicit.
 for ref,length in LENGTHS.items():
  name='TL50_E3_'+str(length).replace('.','p')+'mm';fpath=HW/'ARDF_2M.pretty'/(name+'.kicad_mod')
  fpath.write_text(f'''(footprint "{name}"(version 20241229)(generator "pcbnew")(layer "F.Cu")
 (attr smd exclude_from_bom exclude_from_pos_files)
 (descr "M5B-E3 ordinary1.6mm1oz FR4 nominalh1.50 er4.5;butt-ended microstrip;NOT measured")
 (pad "1" smd rect(at 0 0)(size .2 {WIDTH})(layers "F.Cu"))
 (pad "2" smd rect(at {length} 0)(size .2 {WIDTH})(layers "F.Cu"))
 (fp_rect(start 0 {-WIDTH/2})(end {length} {WIDTH/2})(stroke(width 0)(type solid))(fill solid)(layer "F.Cu"))
 (net_tie_pad_groups "1,2"))\n''')
  old=fs[ref];f=p.FootprintLoad(str(fpath.parent),name);f.SetReference(ref);f.SetValue('50R '+str(length)+'mm');f.SetFPID(p.LIB_ID('ARDF_2M',name));f.SetPath(old.GetPath());f.SetPosition(old.GetPosition())
  for a in f.Pads():a.SetNet(pad(ref,a.GetNumber()).GetNet())
  for fld in old.GetFields():
   if fld.GetName()in['Reference','Value','Footprint']:continue
   nf=p.PCB_FIELD(f,p.FIELD_T_USER,fld.GetName());nf.SetText(fld.GetText());nf.SetVisible(False);f.Add(nf)
  f.Reference().SetLayer(p.F_Fab);f.Reference().SetVisible(True);f.Value().SetVisible(False);b.Remove(old);b.Add(f);fs[ref]=f
  part=parts[ref];part['value']=f.GetValue();part['footprint']='ARDF_2M:'+name;part['note']='E3 recalculated50ohm microstrip on ordinary1.6mm/1oz FR4;nominalh1.50,Dk4.5,width'+str(WIDTH)+'mm,length'+str(length)+'mm;length preserves E2calculatedphase. Butt endpoints avoid wide endcap shorts. RF qualification NOT_RUN.'
 def move(r,dx):
  if abs(dx)<1e-8:return
  f=fs[r];x,y=xy(f.GetPosition());f.SetPosition(pt(x+dx,y));changes.append(dict(ref=r,dx_mm=dx))
 def line_end(ref,end_x):
  f=fs[ref];x,y=xy(f.GetPosition());f.SetPosition(pt(end_x-LENGTHS[ref],y))
 # Anchor the PA gate and drain. Walk matching chain outward;all lumped
 # relative geometries remain unchanged;only line lengths and offsets change.
 line_end('TL605',oldpads['Q501','G'][0][0]);delta=xy(pad('TL605','1').GetPosition())[0]-oldpads['TL605','1'][0][0];move('L634',delta)
 line_end('TL604',xy(pad('L634','1').GetPosition())[0]);delta=xy(pad('TL604','1').GetPosition())[0]-oldpads['TL604','1'][0][0];move('C632',delta)
 # Shunt C633 follows its actual output reference plane,not the line start.
 move('C633',xy(pad('TL604','2').GetPosition())[0]-oldpads['TL604','2'][0][0])
 line_end('TL603',xy(pad('C632','1').GetPosition())[0]);delta=xy(pad('TL603','1').GetPosition())[0]-oldpads['TL603','1'][0][0]
 for r in ['R650','C602','R651']:move(r,delta)
 move('C631',xy(pad('TL603','2').GetPosition())[0]-oldpads['TL603','2'][0][0])
 # Output line starts at fixed drain;walk right keeping ST lumped network.
 f=fs['TL606'];x,y=oldpads['Q501','D'][0];f.SetPosition(pt(x,y));dx=xy(pad('TL606','2').GetPosition())[0]-oldpads['TL606','2'][0][0];move('C636',dx)
 fs['TL607'].SetPosition(pt(*xy(pad('TL606','2').GetPosition())));dx=xy(pad('TL607','2').GetPosition())[0]-oldpads['TL607','2'][0][0]
 for r in ['L638','C637','C638']:move(r,dx)
 fs['TL608'].SetPosition(pt(*xy(pad('L638','2').GetPosition())));dx=xy(pad('TL608','2').GetPosition())[0]-oldpads['TL608','2'][0][0];move('C639',dx)
 fs['TL609'].SetPosition(pt(*xy(pad('C639','2').GetPosition())));dx=xy(pad('TL609','2').GetPosition())[0]-oldpads['TL609','2'][0][0]
 for r in ['L641','L642','L643',*['C'+str(i)for i in range(641,648)]]:move(r,dx)
 # Retarget endpoints that terminate on the changed pin/reference planes.
 for ref,f in fs.items():
  for a in f.Pads():
   k=(ref,a.GetNumber())
   if k not in oldpads:continue
   at,net=oldpads[k];new=xy(a.GetPosition())
   if math.dist(at,new)>1e-7:ports[(round(at[0],6),round(at[1],6),net)]=new
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):continue
  for get,setter in [('GetStart','SetStart'),('GetEnd','SetEnd')]:
   at=xy(getattr(t,get)());k=(round(at[0],6),round(at[1],6),t.GetNetname())
   if k in ports:getattr(t,setter)(pt(*ports[k]))
  # Long50ohm output conductor;keep true components' short lumped junctions.
  if abs(p.ToMM(t.GetWidth())-1.102)<.001:t.SetWidth(MM(WIDTH))
 # PA source:replace12oldvias by32ordinary0.8/0.3vias,4x8 at0.6pitch.
 oldsource=[t for t in b.GetTracks()if isinstance(t,p.PCB_VIA)and xy(t.GetPosition())[0]in[111.35,112.65]and 52.9<xy(t.GetPosition())[1]<57.1]
 assert len(oldsource)==12
 for t in oldsource:b.Remove(t)
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):t.SetWidth(MM(.8));t.SetFrontTentingMode(1);t.SetBackTentingMode(1)
 for xx in [-.9,-.3,.3,.9]:
  for yy in [-2.1,-1.5,-.9,-.3,.3,.9,1.5,2.1]:
   v=p.PCB_VIA(b);v.SetPosition(pt(112+xx,55+yy));v.SetWidth(MM(.8));v.SetDrill(MM(.3));v.SetLayerPair(p.F_Cu,p.B_Cu);v.SetNet(b.FindNet('GND'));v.SetFrontTentingMode(1);v.SetBackTentingMode(0);b.Add(v)
 # Preserve manufacturer source copper2.7x5. Only its mask/stencil changes.
 # Source openings:0.4mm square mask caps over0.3mm holes;ordinaryLPI,
 # not filled/cappedvias. Bottom is open for inspection/TIM;no hermetic claim.
 path=HW/'ARDF_2M.pretty/PD54008L_ST_GDS_5x5.kicad_mod';src=c.parse(path.read_text())
 for a in c.children(src,'pad'):
  if a[1]=='S':c.child(a,'layers')[1:]=['F.Cu']
 for a in list(c.children(src,'fp_rect')):
  if c.child(a,'layer')[1]in['F.Paste','F.Mask']:src.remove(a)
 # Rectangular apertures form a connected grid around masked via caps.
 xs=[(-1.35,-1.1),(-.7,-.5),(-.1,.1),(.5,.7),(1.1,1.35)]
 ys=[(-2.5,-2.3),(-1.9,-1.7),(-1.3,-1.1),(-.7,-.5),(-.1,.1),(.5,.7),(1.1,1.3),(1.7,1.9),(2.3,2.5)]
 for layer in ['F.Mask','F.Paste']:
  # Paste narrower than mask;open grid fraction qualified during assembly.
  shrink=.025 if layer=='F.Paste'else 0
  for a,z in xs:
   src.append(c.parse(f'(fp_rect(start {a+shrink} -2.5)(end {z-shrink} 2.5)(stroke(width 0)(type solid))(fill solid)(layer "{layer}"))'))
  for a,z in ys:
   src.append(c.parse(f'(fp_rect(start -1.35 {a+shrink})(end 1.35 {z-shrink})(stroke(width 0)(type solid))(fill solid)(layer "{layer}"))'))
 path.write_text(c.dump(src)+'\n')
 # Update embedded Q501 mask/paste only via parsed replacement.
 p.SaveBoard(str(board),b);tree=c.parse(board.read_text())
 for f in c.children(tree,'footprint'):
  props={q[1]:q[2]for q in c.children(f,'property')}
  if props['Reference']=='Q501':
   for a in c.children(f,'pad'):
    if a[1]=='S':c.child(a,'layers')[1:]=['F.Cu']
   for a in list(c.children(f,'fp_rect')):
    if c.child(a,'layer')[1]in['F.Paste','F.Mask']:f.remove(a)
   for a in c.children(src,'fp_rect'):
    if c.child(a,'layer')[1]in['F.Paste','F.Mask']:f.append(copy.deepcopy(a))
 # Entire14x12bottom contact open;ordinaryholes may be open underTIM.
 for g in list(c.children(tree,'gr_rect')):
  if c.child(g,'layer')and c.child(g,'layer')[1]=='B.Mask':tree.remove(g)
 tree.append(c.parse('(gr_rect(start 105 49)(end 119 61)(stroke(width 0)(type solid))(fill solid)(layer "B.Mask"))'))
 # Ordinary stack,nominal model only. No dielectric constraints/impedance lock.
 c.child(tree,'general')[1]=[c.Atom('thickness'),c.Atom('1.6')]
 setup=c.child(tree,'setup');old=c.child(setup,'stackup')
 if old:setup.remove(old)
 setup.append(c.parse('''(stackup(layer "F.SilkS"(type "Top Silk Screen"))(layer "F.Paste"(type "Top Solder Paste"))(layer "F.Mask"(type "Top Solder Mask")(thickness .015)(epsilon_r 3.8))(layer "F.Cu"(type "copper")(thickness .035))(layer "dielectric 1"(type "core")(thickness 1.50)(material "FR4")(epsilon_r 4.5)(loss_tangent .02))(layer "B.Cu"(type "copper")(thickness .035))(layer "B.Mask"(type "Bottom Solder Mask")(thickness .015)(epsilon_r 3.8))(layer "B.Paste"(type "Bottom Solder Paste"))(layer "B.SilkS"(type "Bottom Silk Screen"))(copper_finish "Lead-free HASL")(dielectric_constraints no))'''))
 # Broad RF top-clearance channel avoids accidental uncontrolledCPW. Keep
 # local grounded shunt/via/source contacts;bottom return keepouts unchanged.
 for z in c.children(tree,'zone'):
  keep=c.child(z,'keepout')
  if keep and c.child(keep,'copperpour')[1]=='not_allowed'and c.child(z,'layer')and c.child(z,'layer')[1]=='F.Cu':
   pts=c.child(c.child(z,'polygon'),'pts');coords=[list(map(float,q[1:]))for q in c.children(pts,'xy')]
   if min(q[0]for q in coords)==48:
    for q in c.children(pts,'xy'):
     if float(q[2])==48:q[2]=c.Atom('46')
     elif float(q[2])==59:q[2]=c.Atom('62')
 board.write_text(c.dump(tree)+'\n');b=p.LoadBoard(str(board))
 # Copper resistance is halved by doubling trunk width,with short package
 # approaches preserved;each neck is explicitly included in the power model.
 wider=[]
 for t in list(b.GetTracks()):
  if isinstance(t,p.PCB_VIA)or t.GetNetname()not in POWER_INPUT|POWER_RAIL:continue
  w=p.ToMM(t.GetWidth());length=p.ToMM(t.GetLength());want=1.5 if t.GetNetname()in POWER_INPUT else 1.0
  if w<.49 or w>=want or length<=2:continue
  a,z=xy(t.GetStart()),xy(t.GetEnd());d=.8/length;pa=(a[0]+d*(z[0]-a[0]),a[1]+d*(z[1]-a[1]));pz=(z[0]-d*(z[0]-a[0]),z[1]-d*(z[1]-a[1]));t.SetStart(pt(*pa));t.SetEnd(pt(*pz));t.SetWidth(MM(want))
  for x,y in [(a,pa),(pz,z)]:
   n=p.PCB_TRACK(b);n.SetStart(pt(*x));n.SetEnd(pt(*y));n.SetWidth(MM(w));n.SetLayer(t.GetLayer());n.SetNet(t.GetNet());b.Add(n)
  wider.append(dict(net=t.GetNetname(),old_width_mm=w,new_width_mm=want,original_length_mm=length))
 tb=b.GetTitleBlock();tb.SetRevision(REV);b.SetTitleBlock(tb);b.GetDesignSettings().SetBoardThickness(MM(1.6));p.SaveBoard(str(board),b)
 # Fields in actualsheets,manifest andPCB must agree;no passive/device values change.
 for ref in LENGTHS:
  part=parts[ref]
  for f in HW.glob('*.kicad_sch'):
   root=c.parse(f.read_text());dirty=False
   for sy in c.children(root,'symbol'):
    props={q[1]:q for q in c.children(sy,'property')}
    if props.get('Reference',['','',''])[2]!=ref:continue
    for name,key in [('Value','value'),('Footprint','footprint'),('Engineering_Note','note')]:
     if name in props:props[name][2]=part[key]
    dirty=True
   if dirty:f.write_text(c.dump(root)+'\n')
 (HW/'RF2M.electrical.json').write_text(json.dumps(data,indent=2)+'\n')
 # Stronger margin rules,not category suppression.
 pro=HW/'RF2M.kicad_pro';q=json.loads(pro.read_text());rules=q['board']['design_settings']['rules'];rules.update(min_via_diameter=.8,min_via_annular_width=.25,min_hole_clearance=.30,min_hole_to_hole=.20,min_text_height=1.0,min_text_thickness=.15);q['board']['design_settings']['rule_severities']['connection_width']='error';pro.write_text(json.dumps(q,indent=2)+'\n')
 save('initial-implemented-changes.json',dict(revision=REV,moved_RF_parts=changes,RF_width_mm=WIDTH,lengths_mm=LENGTHS,source_vias=32,ordinary_vias='0.8/0.3',power_trunks=wider,values_changed=list(LENGTHS),circuit_topology_changes=[]))
 guard();print('E3 native stack/RF/thermal/power implementation saved')
if __name__=='__main__':apply()
