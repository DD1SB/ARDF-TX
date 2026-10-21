"""Bind native sources, populations, assembly and reproducible evaluation CAM."""
import csv,math,zipfile,subprocess,re,collections
from m5b_e6r2_common import *
from m5a_r1_costs import effective,price
from m5b_e3_common import aliases
from m5b_e6r2_geometry import geometry

def table(path,rows):
 path=OUT/path;path.parent.mkdir(exist_ok=True,parents=True)
 with path.open('w') as f:
  w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def archive(path,files):
 with zipfile.ZipFile(path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
  for n,f in sorted(files):
   info=zipfile.ZipInfo(n,(2026,10,21,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,Path(f).read_bytes())
def inputs():
 files=list(HW.glob('*.kicad_sch'))+list(HW.glob('*.kicad_sym'))+[HW/n for n in ['RF2M.kicad_pcb','RF2M.kicad_pro','RF2M.electrical.json','fp-lib-table','sym-lib-table']]+list((HW/'ARDF_2M.pretty').glob('*.kicad_mod'))+list((HW/'ARDF_2M.3dshapes').glob('*'))
 if (HW/'RF2M.kicad_dru').exists():files.append(HW/'RF2M.kicad_dru')
 save('native-inputs.json',{str(f.relative_to(ROOT)):sha(f) for f in sorted(files)})
 save('verification-inputs.json',{str(f.relative_to(ROOT)):sha(f) for f in sorted((ROOT/'tools').glob('m5b_e6r2*')) if f.suffix in ['.py','.cpp']})
 docs=list((ROOT/'docs').glob('M5B_E6R2*.md'))+[ROOT/'README.md',ROOT/'docs/README.md',HW/'README.md']
 save('documentation-inputs.json',{str(f.relative_to(ROOT)):sha(f) for f in sorted(docs)})
 return files

def bom():
 parts=manifest()['parts'];rows=[];summary=[]
 for v,pops in {'BUCK4S':{'ALL','NORMAL','BUCK4S'},'BOOST2S':{'ALL','NORMAL','BOOST2S'},'TRAIN_ONLY':{'ALL','TRAIN_ONLY'}}.items():
  ps=[d for d in parts if d['population']in pops and not d['ref'].startswith(('#','TP','TL'))]
  demand=collections.Counter(effective(d,v)[1] for d in ps)
  for q in [1,5,7,10]:
   cost=0;added=0
   for d in ps:
    value,mpn=effective(d,v);need=demand[mpn]*q;order=math.ceil(max(need,d['moq'])/d['multiple'])*d['multiple'];unit=max(price(e,order) for e in ps if effective(e,v)[1]==mpn);allocated=unit*order/need
    cost+=allocated
    if d['group']=='carrier_keying':added+=allocated
    rows.append(dict(variant=v,fleet=q,ref=d['ref'],value=value,MPN=mpn,footprint=d['footprint'],quantity_board=1,order_pooled=order,MOQ=d['moq'],multiple=d['multiple'],unit_net_EUR=unit,allocated_net_EUR=allocated,evidence=d['evidence'],supplier=d['supplier'],availability=d['availability'],source=d['source_url']))
   batches=math.ceil(q/5)
   summary.append(dict(variant=v,fleet=q,electrical_net_EUR=cost,keying_added_net_EUR=added,parts=len(ps),PCB_ordered=batches*5,PCB_batch_cash_ESTIMATE_net_EUR=[batches*60,batches*100],PCB_allocated_required_each_ESTIMATE_net_EUR=[batches*60/q,batches*100/q],enclosure_UNQUOTED=True,labor_NOT_MEASURED=True))
  table('BOM_'+v+'.csv',[r for r in rows if r['variant']==v and r['fleet']==7])
 table('RF2M_BOM_all_quantities.csv',rows)
 mech=[
  ('SK81 100 SA',1,7.30/1.19,9.,'Historical indexed7.30gross fromE6R1, not current quote','214g;100x100x15mm'),
  ('Al flat15x44x6mm',1,.3,1.,'ESTIMATE','Drill2x3.3mm;10.7g before holes'),
  ('KERATHERM86/82 .25mm15x44',1,22.59/10,22.59/10,'HISTORICAL_INDEXED_E6_2026_10_21','100x100sheet22.59net;10 usable blanks, charged full sheets per fleet below'),
  ('GS220P .05mm12x18 mica',2,.2,.45,'ESTIMATE','Separate oversized pads forbothlive tabs'),
  ('Fischer IB6 insulating bush',1,.1,.3,'ESTIMATE','Q401 only'),
  ('M3x6 steel Q401 screw',1,.04,.1,'ESTIMATE','3.6mm threaded engagement'),
  ('M2.5x6PA66 screw andwasher',1,.1,.3,'ESTIMATE','Q402 insulating fastener'),
  ('Al angle30x20x2x12mm',4,.15,.45,'ESTIMATE','Independent side support;12.4g total'),
  ('M3x6 side screw',4,.04,.1,'ESTIMATE','4mm thread engagement'),
  ('M3x12 foot screw+washer+4mm locknut',4,.12,.25,'ESTIMATE','2mm angle+3mm carrier+.5mm washer+4mm locknut;2.5mm protrusion'),
  ('M3x12 bar screw+OD9washer',2,.1,.2,'ESTIMATE','Light localclamp, not mass support'),
  ('Ground braid andringterminal',1,.15,.4,'ESTIMATE','Controlled ground bond'),
  ('Thermal compound allocated',1,.1,.3,'ESTIMATE','Thinfilm onmica/barinterfaces')]
 mr=[dict(item=n,qty=q,unit_low_net_EUR=lo,unit_high_net_EUR=hi,evidence=e,note=note) for n,q,lo,hi,e,note in mech]
 table('shared-heatsink-BOM.csv',mr);low=sum(r['qty']*r['unit_low_net_EUR'] for r in mr);high=sum(r['qty']*r['unit_high_net_EUR'] for r in mr)
 thermal=[]
 for quantity in [1,5,7,10]:
  allocation=math.ceil(quantity/10)*22.59/quantity
  thermal.append(dict(fleet=quantity,source_sheet_cash_net_EUR=math.ceil(quantity/10)*22.59,spare_TIM_blanks=math.ceil(quantity/10)*10-quantity,cooler_each_low=low-22.59/10+allocation,cooler_each_high=high-22.59/10+allocation))
 seven=next(r for r in thermal if r['fleet']==7)
 save('costs.json',dict(date=DATE,currency='EUR net, shipping/VAT excluded;historical SK81gross converted19%illustratively',electrical=summary,thermal_by_quantity=thermal,cooler_material_each_estimate=[seven['cooler_each_low'],seven['cooler_each_high']],cooler_fleet7_estimate=[7*seven['cooler_each_low'],7*seven['cooler_each_high']],cooling_mass_g=[248,270],carrier_base_additional_estimate_EUR=[3,7],corner_posts_andfeet_additional_estimate_EUR=[2,5],carrier_mass_g=113,unique_cooling_BOM_lines=len(mr),cooling_quantity=sum(r['qty'] for r in mr),historical_E5_each=[31.11,38.61],historical_E6_each=[15.36,21.36],historical_E6R1_including_electronics_each=[16.89,24.97],qualification='Historical net ranges not refreshedquotes;no booked cashsaving. Full source sheets charged. Bar/angle minimumstock,exact basket,stock andPCBslotquote OPEN.',labor_estimate_minutes_each=[30,50],labor_includes='Cut/drill/tap/deburr cooler,insulators,fasteners,bond/isolationchecks;PCBassembly/RFalignment/instrumentation excluded',enclosure_UNQUOTED=True,complete_transmitter_120_150_EUR_NOT_DEMONSTRATED=True))

def fabrication():
 guard();native=inputs();drc=json.loads((OUT/'DRC.json').read_text());dfm=json.loads((OUT/'JLCPCB-DFM.json').read_text())
 assert not [x for x in drc['violations'] if x['severity']=='error'];assert not drc['unconnected_items'] and not drc['schematic_parity']
 assert dfm['status'].startswith('PASS') and dfm['native_sha256']==sha(HW/'RF2M.kicad_pcb')
 b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));expect={'PTH':set(),'NPTH':set()}
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA):expect['PTH'].add((*xy(t.GetPosition()),p.ToMM(t.GetDrillValue())))
 for f in b.GetFootprints():
  for a in f.Pads():
   if a.GetDrillSize().x:
    assert a.GetDrillSize().x==a.GetDrillSize().y;expect['NPTH' if a.GetAttribute()==p.PAD_ATTRIB_NPTH else 'PTH'].add((*xy(a.GetPosition()),p.ToMM(a.GetDrillSize().x)))
 from m5b_e3_delivery import drill
 rounding=[]
 for kind,rows in expect.items():
  actual=drill(OUT/'gerbers'/('RF2M-'+kind+'.drl'));assert len(actual)==len(rows),(kind,len(actual),len(rows))
  for x,y,d in rows:
   dist=min(math.dist((x,y),(a,c)) for a,c,dd in actual if abs(dd-d)<1e-6);assert dist<=.00072;rounding.append(dist)
 job=json.loads((OUT/'gerbers/RF2M-job.gbrjob').read_text())['GeneralSpecs'];assert job['LayerNumber']==2 and job['BoardThickness']==1.6 and job['Finish']=='Lead-free HASL' and job['ProjectId']['Revision']==REV
 assert abs(job['Size']['X']-150)<.1 and abs(job['Size']['Y']-110)<.1
 files=[f for f in (OUT/'gerbers').iterdir() if f.suffix in ['.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1','.drl']];assert len(files)==11
 folder=OUT/'fabrication';folder.mkdir(exist_ok=True)
 archive(folder/'RF2M-M5B-E6R2_JLCPCB_5boards.zip',[(f.name,f) for f in files])
 archive(folder/'RF2M-M5B-E6R2_FULL_TOP_STENCIL.zip',[(n,(OUT/'gerbers'/n)) for n in ['RF2M-F_Paste.gtp','RF2M-Edge_Cuts.gm1']])
 archive(OUT/'RF2M-M5B-E6R2-native.zip',[(str(f.relative_to(HW)),f) for f in native])
 aa=aliases();ipc=[]
 for line in (OUT/'RF2M-logical.ipc').read_text().splitlines():
  if line[:3]in ['317','327','367']:line=line[:3]+aa.get(line[3:17].strip(),line[3:17].strip()).ljust(14)+line[17:]
  ipc.append(line)
 (OUT/'RF2M-physical-netties.ipc').write_text('\n'.join(ipc)+'\n');save('fabrication-net-aliases.json',dict(aliases=aa,reason='Declared distributedRFnet-tie copper only;logical schematic remainsseparate'))
 save('fabrication-data-audit.json',dict(status='PASS',native_SHA256=sha(HW/'RF2M.kicad_pcb'),Gerbers=9,separate_drills=2,PTH_hits=len(expect['PTH']),NPTH_hits=len(expect['NPTH']),max_drill_rounding_mm=max(rounding),outline_mm=[150,110],cutouts=2,stencil='FullF.Paste+Edge.Cuts;0.12mm specification;NOT Q501-only',upload_order_energize=False))
 print('PASS actual native/drill/CAM consistency and deterministic ZIP contents')

def inventory():
 guard();inputs()
 files=sorted(f for f in OUT.rglob('*') if f.is_file() and f.name not in ['SHA256SUMS','SHA256SUMS.json'])
 rows={str(f.relative_to(OUT)):sha(f) for f in files};save('SHA256SUMS.json',rows)
 (OUT/'SHA256SUMS').write_text(''.join(h+'  '+n+'\n' for n,h in rows.items()))
 print('SHA256 inventory',len(files),'files')
if __name__=='__main__':globals()[__import__('sys').argv[1]]()
