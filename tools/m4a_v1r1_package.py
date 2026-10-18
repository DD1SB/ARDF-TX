#!/usr/bin/python3
"""Isolated fabrication archives and read-only three-board coordination, no upload."""
import zipfile,collections,csv
from m4a_v1r1_common import *
EXT={'.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gtp','.gbp','.gm1','.drl'}
def archive(folder,out):
 files=sorted(p for p in folder.iterdir()if p.suffix in EXT);assert len(files)==11 and sum(p.suffix=='.drl'for p in files)==2
 out.parent.mkdir(exist_ok=True,parents=True)
 with zipfile.ZipFile(out,'w',compression=zipfile.ZIP_DEFLATED)as z:
  for f in files:
   item=zipfile.ZipInfo(f.name,date_time=(2026,10,18,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o644<<16;z.writestr(item,f.read_bytes())
 with zipfile.ZipFile(out)as z:
  assert z.testzip()is None
  for f in files:assert z.read(f.name)==f.read_bytes()
 return dict(archive=str(out.relative_to(D)),sha256=sha(out),entries=[dict(source=str(f.relative_to(R)),name=f.name,sha256=sha(f))for f in files],classification='Nine production Gerbers and separatePTH/NPTH only. No report, drill map, job, alternative design or panel.')
def main():
 frozen();native=P/(NAME+'.kicad_pcb');review=(D/'README.md');assert review.exists(),'Write review before final package'
 records=[]
 configs=[('RF80-V1R1','M4A-V1R1 candidate; baseline4d2f592',P,native,D/'gerbers',D/'fabrication/RF80-V1R1_JLCPCB_5boards.zip',[150,110]),
 ('Controller','M6-L1 / d94dabd0e40137dc44b2bb94f3707ad4636ca65f',R/'hardware/controller',R/'hardware/controller/CTRL.kicad_pcb',R/'hardware/controller/review/M6-L1/fabrication',D/'three-board-order/CTRL_M6-L1_JLCPCB_5boards.zip',[100,100]),
 ('RF2M','M5B-E4R1 / 2f9982c1b72cd97ba4dad6c992143032b309cca7',R/'hardware/2m',R/'hardware/2m/RF2M.kicad_pcb',R/'hardware/2m/review/M5B-E4R1/gerbers',D/'three-board-order/RF2M_M5B-E4R1_JLCPCB_5boards.zip',[180,140])]
 for label,rev,project,nat,folder,out,size in configs:
  if label!='RF80-V1R1':
   commit=rev.split(' / ')[1];assert nat.read_bytes()==subprocess.check_output(['git','show',commit+':'+str(nat.relative_to(R))]),label
   for f in folder.iterdir():
    if f.suffix in EXT:assert f.read_bytes()==subprocess.check_output(['git','show',commit+':'+str(f.relative_to(R))]),(label,f.name)
  b=pcb.LoadBoard(str(nat));assert b.GetCopperLayerCount()==2 and pcb.ToMM(b.GetDesignSettings().GetBoardThickness())==1.6
  edges=[s for s in b.GetDrawings()if s.GetLayer()==pcb.Edge_Cuts];xs=[pcb.ToMM(t.x)for e in edges for t in[e.GetStart(),e.GetEnd()]];ys=[pcb.ToMM(t.y)for e in edges for t in[e.GetStart(),e.GetEnd()]];assert [max(xs)-min(xs),max(ys)-min(ys)]==size
  entry=archive(folder,out);records.append(dict(PCB=label,authoritative_revision=rev,native=str(nat.relative_to(R)),native_sha256=sha(nat),dimensions_mm=size,quantity=5,process='2L standard FR4 /1.6mm/1oz/green/white/lead-free HASL/ordinary PTH/no impedance control/no premium process',artifact_action='Fresh RF80 export'if label=='RF80-V1R1'else'Existing manufacturer layers and drills copied byte-for-byte into an isolated ZIP; NOT regenerated',**entry,CAM_and_quotation='NOT_SUBMITTED_NOT_QUOTED',physical_qualification='NOT_RUN',remaining_review='RF80 first-evaluation transition proposal requires review; incoming lead fit, winding/heatsink/protection commissioning'if label=='RF80-V1R1'else'Controller USB/pack-ID/power sequencing/RTC/failoff and optionalLoRa RF qualification'if label=='Controller'else'Hidden source-joint process and conservative thermal assembly qualification; RF/AM/PEP/isolation/endurance NOT_RUN'))
 save('three-board-order-readiness.json',dict(status='THREE_SEPARATE_ORDER_ITEMS_PREPARED_FOR_REVIEW_ONLY',records=records,authorization='No supplier upload/order/assembly/power/RF. Each item five individual boards; never one shared promotion or two-up panel.',supplier_CAM='File recognition, outline centreline dimensions,1oz ordinaryPTH hole compensation and standard green mask/HASL to be checked after separately authorized upload. No special hole tolerance requested.'))
 lines=['# Three-board prototype manufacturing review','','All three ZIPs are isolated five-individual-board datasets. Other designs and their historical exports were inspected read-only; copied entries are byte-identical to their authoritative commits. No supplier upload or quotation occurred.','','| PCB | Source | Size mm | ZIP | Qualification |','| --- | --- | --- | --- | --- |']
 for x in records:lines.append(f"| {x['PCB']} | {x['authoritative_revision']} | {' × '.join(map(str,x['dimensions_mm']))} | [{Path(x['archive']).name}]({x['archive']}) | NOT_RUN |")
 lines+=['','All: two-layer standardFR4,1.6mm,1oz,green/white,lead-freeHASL,ordinarythroughvias. Five each as separate items; no factory assembly or premium service. Detailed source hashes and CAM questions: [JSON](three-board-order-readiness.json).','','RF80 transition from the old E2-first sequence is **PROPOSED**, not approved. Controller and RF2M statuses are inherited independent-review candidates, not transmitter operational approvals. Supplier price/CAM, purchasing and all physical gates are separate.']
 (D/'THREE_BOARD_ORDER_READINESS.md').write_text('\n'.join(lines)+'\n')
 # Existing NOT_RUN plan is inherited as a plan, with current board scope and proposal status.
 plan=json.loads((P/'review/M4A-V1/physical-qualification.json').read_text());plan.update(date=DATE,scope='RF80-V1R1, proposed first80m evaluation article; transition pending independent/user review',source_plan='Preserved M4A-V1/M3B-E2 gates, not copied measurement results. All seventeen repeated on the compact board.');save('physical-qualification.json',plan)
 # Native mechanical audit, not a final enclosure assertion.
 b=pcb.LoadBoard(str(native));fs={f.GetReference():f for f in b.GetFootprints()};mounts={r:dict(centre_native_mm=[pcb.ToMM(v)for v in fs[r].GetPosition()],finished_NPTH_mm=pcb.ToMM(next(iter(fs[r].Pads())).GetDrillSize().x))for r in['H1','H2','H3','H4']}
 assert all(x['finished_NPTH_mm']==3.2 for x in mounts.values())
 save('mechanical-fit-review.json',dict(status='CAD_PRESERVED_PHYSICAL_FIT_NOT_RUN',mounts=mounts,pattern_mm=[140,100],outline_mm=[150,110],connectors='All original X/Y/rotation retained, actual pad centres and key orientation compared toV1. Dimensions/lead limits in finished-hole-audit.json; keyed mating housings require actual incoming fit.',envelope='Initial >=10mm underside lead/service clearance,<=25mm top power/coil envelope plus30mm mating-harness service allowance; not final enclosure acceptance.',cooling='IRF610 tabDRAIN and BD140 collector live. Electrically insulate from grounded M3 supports/sinks; stockTO220 mica/silicone pad, matching shoulder bush/screw, continuity test and measured thermal margin. No heatsink rating or deviceSOA inferred from3D render.',sensor='TH301 remains offboard insulated PA-case sensor with strain relief. ElectricalNTC open/short and detached-contact tests distinct.',windings='L410/L411 sameT60-2,20T AWG24; T4019+9AWG24 bifilar. 1/3 winding-start dots and2/3 centre join retained. No modified turns/core/filter values.',integration='Side-by-side flexible keyed cables; RF80/controller hole patterns not forced to align. RF2M underside25.2mm cooling envelope stays free; no stacking over its fins. Separate RF/battery cable exits and strain relief; no final enclosure designed.',physical_fit='Incoming parts,dry-fit all pins,no forced insertion; pin-position tolerance stack is not established by a diagonal calculation. Compliant formed leads and real array fit must be inspected before soldering. Never drill finishedPTH after plating.',models='199 resolved model references; custom WRL winding/connector/BD140 bounds are envelope-only, not certified supplier solids. Actual KiCad top/angled/bottom renders inspected; hand fit remainsNOT_RUN.'))
 print('PASS three isolated11-file fabricationZIPs; otherboards and sources byte-identical; mechanical/qualification plans generated')
if __name__=='__main__':main()
