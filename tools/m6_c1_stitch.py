#!/usr/bin/python3
"""Ordinary ground stitching from actual filled overlap and foreign copper.
Also removes an unused USB VBUS tail created by the ESD bias correction.
"""
import json
from m6_c1_pcb import *
def main():
 b=Board(True);r=json.loads((D/'DRC.json').read_text());remove={i['uuid'] for v in r['violations'] if v['type']=='track_dangling' for i in v['items']};sx=parse((P/'CTRL.kicad_pcb').read_text());sx[:]=[x for x in sx if not(isinstance(x,list) and x and x[0]=='segment' and child(x,'uuid') and str(child(x,'uuid')[1]) in remove)];(P/'CTRL.kicad_pcb').write_text(dump(sx)+'\n');b=Board(True)
 pads=[a for f in b.b.GetFootprints() for a in f.Pads()];vias=[t for t in b.b.GetTracks() if isinstance(t,pcb.PCB_VIA)];foreign=[t for t in b.b.GetTracks() if t.GetNetname()!='GND'];zs=[z for z in b.b.Zones() if not z.GetIsRuleArea()];rules=[z.GetBoundingBox() for z in b.b.Zones() if z.GetIsRuleArea() and z.GetDoNotAllowVias()];added=[]
 for x in range(23,119,6):
  for y in range(23,119,6):
   center=pt(x,y)
   if 40<x<60 and 21<y<49:continue # no additional vias under ESP body
   if any(z.Contains(center) for z in rules):continue
   if not all(any(z.GetLayer()==layer and z.GetFilledPolysList(layer).Contains(center) for z in zs) for layer in [pcb.F_Cu,pcb.B_Cu]):continue
   if any(abs(x-pcb.ToMM(a.GetPosition().x))<pcb.ToMM(a.GetSize().x)/2+.75 and abs(y-pcb.ToMM(a.GetPosition().y))<pcb.ToMM(a.GetSize().y)/2+.75 for a in pads):continue
   if any(math.dist((x,y),xy(v.GetPosition()))<.95 for v in vias):continue
   circle=pcb.SHAPE_CIRCLE(center,MM(.4))
   if any(any(t.IsOnLayer(l) and pcb.SHAPE.Collide(circle,t.GetEffectiveShape(l),MM(.18)) for l in [pcb.F_Cu,pcb.B_Cu]) for t in foreign):continue
   v=pcb.PCB_VIA(b.b);v.SetPosition(center);v.SetWidth(MM(.8));v.SetDrill(MM(.3));v.SetViaType(pcb.VIATYPE_THROUGH);v.SetLayerPair(pcb.F_Cu,pcb.B_Cu);v.SetNet(b.nets['GND']);v.SetFrontTentingMode(1);v.SetBackTentingMode(1);b.b.Add(v);vias.append(v);added.append((x,y))
 pcb.ZONE_FILLER(b.b).Fill(b.b.Zones());b.save();(D/'ground-stitching.json').write_text(json.dumps({'added_ordinary_0p8_0p3_vias_mm':added,'removed_unused_USB_tail_UUIDs':sorted(remove),'no_premium_via_treatment':True,'thermal_tent_closure_guarantee':False},indent=2)+'\n');print('Added',len(added),'ground stitches in native F/B ground overlap')
if __name__=='__main__':main()
