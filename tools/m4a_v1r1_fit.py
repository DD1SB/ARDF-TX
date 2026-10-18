#!/usr/bin/python3
"""Real PTH geometry, explicit manufacturer/screening envelopes and regressions."""
import math,copy,collections,subprocess
from m4a_v1r1_common import *
DATA={
 'J101':dict(mpn='61201621621',lead_nominal_mm=[.64,.64],lead_max_mm=[.79,.79],limit_kind='MANUFACTURER: square0.64+/-0.15',source='https://www.we-online.com/components/products/datasheet/61201621621.pdf',drawing='002.001,2026-08-30,p1',hole=1.4),
 'J502':dict(mpn='B3B-XH-A(LF)(SN)',lead_nominal_mm=[.64,.64],lead_max_mm=[.79,.79],limit_kind='ENGINEERING INCOMING SCREEN, not manufacturer guaranteed maximum. Published lead tolerance missing; accept <=0.79mm square and dry-fit.',source='https://www.jst.co.uk/downloads/series/eXH_1.pdf',drawing='XH top-entry header/circuit3: square0.64; note2 hard-FR4 holes may need enlargement. Individual2D drawing requires email request; not requested.',hole=1.3),
 'Q402':dict(mpn='IRF610PBF-BE3',lead_nominal_mm=None,lead_max_mm=[.91,.61],limit_kind='MANUFACTURER: external b/c maxima, not base-metal b1/c1',source='https://www.vishay.com/docs/92506/packageinformation_to-220ab_highvoltage.pdf',drawing='92506,6031,S24-0989 RevF,2024-09-30,p2; linked from exact IRF610 product91023',hole=1.4),
 'Q403':dict(mpn='BD140',lead_nominal_mm=None,lead_max_mm=[.88,.63],limit_kind='MANUFACTURER: SOT32 B/B1 maxima',source='https://www.st.com/resource/en/datasheet/bd140.pdf',drawing='0016114E,May2008 Rev5,p7; pin1B/2C/3E',hole=1.4),
 'J301':dict(mpn='B2P-VH(LF)(SN)',lead_nominal_mm=[1.14,1.14],lead_max_mm=[1.19,1.19],limit_kind='ENGINEERING INCOMING SCREEN, not manufacturer guaranteed maximum. Square1.14 published; lead tolerance missing. Added0.05mm to each full lead dimension as a screening bound and dry-fit.',source='https://www.jst-mfg.com/product/pdf/eng/eVH.pdf',drawing='VH header square1.14; same part and mating VHR-2N retained',hole=1.9),
 'J401':dict(mpn='1727010',lead_nominal_mm=[.5,.9],lead_max_mm=[.55,.95],limit_kind='ENGINEERING INCOMING SCREEN, not manufacturer guaranteed maximum. Published0.5x0.9 without lead tolerance; added0.05mm each dimension.',source='https://www.phoenixcontact.com/en-us/products/printed-circuit-board-terminal-mkds-1-2-381-1727010?type=pdf',drawing='MKDS1/2-3.81,1727010,p4 pin dimensions; ordinary1.1mm suggested hole does not cover JLC negative tolerance',hole=1.3)}
def check(b,data=None):
 data=data or DATA;errors=[];rows=[];fs={f.GetReference():f for f in b.GetFootprints()}
 for r,s in data.items():
  maximum=math.hypot(*s['lead_max_mm']);pads=list(fs[r].Pads())
  for a in pads:
   d=pcb.ToMM(a.GetDrillSize().x);sz=[pcb.ToMM(a.GetSize().x),pcb.ToMM(a.GetSize().y)];ring=(min(sz)-d)/2
   clearance=d-.08-maximum
   if clearance<.0999:errors.append(r+'.'+a.GetNumber()+':undersized_finished_hole')
   if d>s['hole']+.001:errors.append(r+'.'+a.GetNumber()+':oversized_unreviewed_hole')
   if ring<.2499:errors.append(r+'.'+a.GetNumber()+':annulus')
   if fs[r].GetFPIDAsString()!=ALIASES[r][0]:errors.append(r+':unreviewed_footprint')
   if not a.IsOnLayer(pcb.F_Cu)or not a.IsOnLayer(pcb.B_Cu):errors.append(r+':not_ordinary_PTH')
  a=pads[0];d=pcb.ToMM(a.GetDrillSize().x);sz=[pcb.ToMM(a.GetSize().x),pcb.ToMM(a.GetSize().y)]
  rows.append(dict(ref=r,**s,pad_count=len(pads),native_finished_hole_mm=d,ordinary_finished_range_mm=[round(d-.08,3),round(d+.13,3)],maximum_lead_diagonal_mm=maximum,minimum_diametric_insertion_clearance_mm=d-.08-maximum,native_lands_mm=sz,nominal_artwork_annulus_mm=(min(sz)-d)/2,geometric_residual_annulus_at_max_hole_and075_offset_mm=(min(sz)-(d+.13))/2-.075,residual_limit='Sensitivity only; nominal CAD annulus is the vendor DFM quantity. Drill registration/etch/finished copper require incoming inspection.',solderability='Hand solder with fixture support; full barrel wetting/fillets inspected. Max hole is not a precision mechanical locator. No forced insertion or drilling after plating.'))
 return errors,rows
def tracks(b):return collections.Counter((t.GetNetname(),t.GetClass(),tuple(t.GetStart()),tuple(t.GetEnd()),t.GetWidth(pcb.F_Cu)if isinstance(t,pcb.PCB_VIA)else t.GetWidth(),t.GetDrillValue()if isinstance(t,pcb.PCB_VIA)else t.GetLayer())for t in b.GetTracks())
def main():
 frozen();path=P/(NAME+'.kicad_pcb');b=pcb.LoadBoard(str(path));e,rows=check(b);assert not e,e
 save('finished-hole-audit.json',dict(status='PASS_NATIVE_GEOMETRY_WITH_DISCLOSED_INCOMING_SCREEN_LIMITS',native_sha256=sha(path),component_PTH_tolerance_mm=[-.08,.13],minimum_insertion_target_mm=.1,holes_audited=sum(x['pad_count']for x in rows),rows=rows,missing_manufacturer_tolerances=['J301','J401','J502'],assembly_fit='NOT_RUN. Missing supplier tolerances are not invented guarantees; measure/screen actual parts and dry-fit before any staged soldering. No special board tolerance required.'))
 tmp=Path('/tmp/m4av1r1/baseline.kicad_pcb');tmp.parent.mkdir(exist_ok=True);tmp.write_bytes(gitfile('hardware/80m/production/RF80_V1.kicad_pcb'));old=pcb.LoadBoard(str(tmp));of={f.GetReference():f for f in old.GetFootprints()};fs={f.GetReference():f for f in b.GetFootprints()};assert tracks(old)==tracks(b)
 count=0;approved=[]
 for r,f in fs.items():
  o=of[r];assert f.GetPosition()==o.GetPosition()and f.GetOrientationDegrees()==o.GetOrientationDegrees(),r
  for a in f.Pads():
   z=next(q for q in o.Pads()if q.GetNumber()==a.GetNumber());assert a.GetPosition()==z.GetPosition()and a.GetNetname()==z.GetNetname()and a.GetShape()==z.GetShape(),r;count+=1
   if r not in ALIASES:assert a.GetSize()==z.GetSize()and a.GetDrillSize()==z.GetDrillSize(),r
   else:
    assert pcb.ToMM(a.GetDrillSize().x)==ALIASES[r][1]
    if ALIASES[r][2]:assert tuple(pcb.ToMM(v)for v in a.GetSize())==ALIASES[r][2]
    else:assert a.GetSize()==z.GetSize(),r
    approved.append(dict(ref=r,pin=a.GetNumber(),old_drill_mm=pcb.ToMM(z.GetDrillSize().x),new_drill_mm=pcb.ToMM(a.GetDrillSize().x),old_land_mm=[pcb.ToMM(v)for v in z.GetSize()],new_land_mm=[pcb.ToMM(v)for v in a.GetSize()]))
 save('V1-layout-preservation.json',dict(status='PASS',baseline=BASE,native_sha256=sha(path),all_track_via_objects='IDENTICAL',all_component_positions_orientations='IDENTICAL',all_pad_centres_nets_shapes='IDENTICAL',total_pads_compared=count,approved_pad_changes=approved,zone_fill='Refilled after local J502 pad enlargement; local changed pour geometry separately bounded, not assumed identical.'))
 tests=[]
 def reject(label,fn,code):
  q=pcb.LoadBoard(str(path));fn(q);errors,_=check(q);assert any(code in x for x in errors),(label,errors);tests.append(dict(mutation=label,detected=code))
 def pad(q,r):return next(a for f in q.GetFootprints()if f.GetReference()==r for a in f.Pads())
 reject('old_IDC1p2_hole',lambda q:pad(q,'J101').SetDrillSize(pcb.VECTOR2I(pcb.FromMM(1.2),pcb.FromMM(1.2))),'undersized_finished_hole')
 reject('old_XH0p95_hole',lambda q:pad(q,'J502').SetDrillSize(pcb.VECTOR2I(pcb.FromMM(.95),pcb.FromMM(.95))),'undersized_finished_hole')
 reject('oversized_Fox_hole',lambda q:pad(q,'J502').SetDrillSize(pcb.VECTOR2I(pcb.FromMM(1.7),pcb.FromMM(1.7))),'oversized_unreviewed_hole')
 reject('thin_PTH_land',lambda q:pad(q,'Q402').SetSize(pcb.VECTOR2I(pcb.FromMM(1.65),pcb.FromMM(1.65))),'annulus')
 bad=copy.deepcopy(DATA);bad['J101']['lead_max_mm']=[1.1,1.1];assert any('undersized' in x for x in check(b,bad)[0]);tests.append(dict(mutation='manufacturer_lead_incompatibility',detected='computed_diagonal_and_finished_minimum'))
 save('hole-regression.json',dict(status='PASS',tests=tests));print('Lead/finished-hole audit',sum(x['pad_count']for x in rows),'holes;',len(tests),'negative tests; routing/placements preserved')
if __name__=='__main__':main()
