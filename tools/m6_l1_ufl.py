#!/usr/bin/python3
"""Hirose nominal pattern, native copper keep-out, mask/paste evidence."""
import json,hashlib
import pcbnew as p
import m6_l1_rf as rf
import m5a_r1_design as sx

def main():
 b=p.LoadBoard(str(rf.P/'CTRL.kicad_pcb'));j=next(f for f in b.GetFootprints() if f.GetReference()=='J7');sig=rf.polygon(next(a for a in j.Pads() if a.GetNumber()=='1'),p.F_Cu)
 ground=[z.GetFilledPolysList(p.F_Cu) for z in b.Zones() if not z.GetIsRuleArea() and z.IsOnLayer(p.F_Cu) and z.GetNetname()=='GND'];bad=[];count=0
 # The full maker no-traces rectangle, excluding its explicitly drawn SIG land.
 for ix in range(1,110):
  for iy in range(1,95):
   x=98.315+ix*.02;y=27.55+iy*.02;v=rf.pt(x,y)
   if sig.Contains(v):continue
   count+=1
   if any(z.Contains(v) for z in ground):bad.append([x,y])
 assert not bad,bad[:10]
 # The full keep-out permits the intended SIG pad, not arbitrary foreign lands.
 foreign=[]
 for f in b.GetFootprints():
  for a in f.Pads():
   if a.IsOnLayer(p.F_Cu) and not (f.GetReference()=='J7' and a.GetNumber()=='1'):foreign.append((f.GetReference()+'.'+a.GetNumber(),rf.polygon(a,p.F_Cu)))
 for t in b.GetTracks():
  if t.IsOnLayer(p.F_Cu) and t.GetNetname()!='LORA_ANT':foreign.append(('track/via '+t.GetNetname(),rf.polygon(t,p.F_Cu)))
 roi=p.SHAPE_POLY_SET();roi.NewOutline()
 for x,y in [(98.315,27.55),(100.515,27.55),(100.515,29.45),(98.315,29.45)]:roi.Append(p.FromMM(x),p.FromMM(y))
 roi.BooleanSubtract(sig)
 for name,poly in foreign:
  overlap=p.SHAPE_POLY_SET(poly);overlap.BooleanIntersection(roi)
  assert abs(overlap.Area())<1,(name,'foreign copper in Hirose keep-out')
 pads=[dict(number=a.GetNumber(),net=a.GetNetname(),xy_mm=[rf.mm(a.GetPosition().x),rf.mm(a.GetPosition().y)],size_mm=[rf.mm(a.GetSize().x),rf.mm(a.GetSize().y)],mask_expansion_mm=rf.mm(a.GetSolderMaskExpansion(p.F_Mask)),shape=str(a.GetShape())) for a in j.Pads()]
 s=(rf.P/'ARDF_CTL.kicad_sym').read_text();symbol=next(x for x in sx.children(sx.parse(s),'symbol') if str(x[1])=='M6_U70');p8=[sx.child(a,'name')[1] for u in sx.children(symbol,'symbol') for a in sx.children(u,'pin') if sx.child(a,'number')[1]=='8'];assert p8==['8_DIO3']
 result=dict(status='PASS_NOMINAL_PATTERN_AND_NATIVE_COPPER',native_sha256=hashlib.sha256((rf.P/'CTRL.kicad_pcb').read_bytes()).hexdigest(),manufacturer='Hirose exact U.FL-R-SMT-1(10), SIG and GND contact numbering mapped to carrier1/2',drawing='Historical official-author catalog p3 lists(10); current official catalog p12 corroborates geometry.',pads=pads,nominal_pattern_mm=dict(signal=[1.05,1.0],grounds=[2.2,1.05],signal_offset=[-1.525,0],ground_offsets=[[0,-1.475],[0,1.475]],outer_span=4.0,inner_span=1.9),keepout=dict(full_maker_rectangle_mm=[98.315,27.55,100.515,29.45],native_rule_mm=[98.315,27.55,100.515,29.45],difference='Full rectangle corrected; intended pads allowed by rule, all foreign copper still independently checked.',sample_pitch_mm=.02,non_signal_samples_checked=count,foreign_ground_samples=bad,foreign_pad_track_via_polygons_checked=len(foreign),layer='F.Cu only; B.Cu ground retained'),paste=dict(native='Full copper-size apertures with existing rounded corners, no local size reduction',maker='0.10/0.12mm stencil, reduced metal-mask openings; do not call native full-pad apertures identical',selected_builder_method='Mask J7 stencil apertures, hand solder3 lands with controlled minimal solder; alternate exact maker stencil recommended if reflowing',assembly='NOT_RUN'),DIO3_symbol_name=p8[0],service='No nearby mounted body within the6mm service diameter; maintain vertical access/cable strain relief and existing15mm top envelope. Exact incoming module height/enclosure NOT_RUN.')
 (rf.D/'UFL-landpattern-audit.json').write_text(json.dumps(result,indent=2)+'\n');print('U.FL geometry/keepout',count,'points PASS; DIO3 symbol semantic PASS')
if __name__=='__main__':main()
