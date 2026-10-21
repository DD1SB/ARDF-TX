#!/usr/bin/python3
"""Read-only CAD/netlist/fixture/DFM checks, then a machine-readable report.
Manufacturer pin evidence is maintained separately in review/pinout-review.csv.
"""
import csv,json,hashlib,subprocess,sys,xml.etree.ElementTree as E
from pathlib import Path
import pcbnew as p
P=Path(__file__).resolve().parents[1]
def main():
 b=p.LoadBoard(str(P/'Mini80.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()};m=json.loads((P/'Mini80.electrical.json').read_text());errors=[];checks={}
 def ok(name,condition):
  checks[name]=bool(condition)
  if not condition:errors.append(name)
 for kind in ['drc','erc']:
  args=['kicad-cli','pcb'if kind=='drc'else'sch',kind,'--format','json','--output',str(P/'review'/f'{kind}.json')]
  if kind=='drc':args+=['--schematic-parity']
  args+=[str(P/('Mini80.kicad_pcb'if kind=='drc'else'Mini80.kicad_sch'))];subprocess.run(args,check=True)
  r=json.loads((P/'review'/f'{kind}.json').read_text())
  if kind=='drc':ok('DRC zero errors/warnings/unconnected/parity',not(r['violations']or r['unconnected_items']or r['schematic_parity']))
  else:ok('ERC zero errors/warnings',not any(s['violations']for s in r['sheets']))
 net={}
 for n in E.parse(P/'review/netlist.xml').findall('./nets/net'):
  for v in n.findall('node'):net[(v.attrib['ref'],v.attrib['pin'])]=n.attrib['name'].lstrip('/')
 count=0
 for comp in m['parts']:
  if comp['ref'].startswith('#'):continue
  ref=comp['ref'];ok(ref+' present',ref in fs)
  if ref not in fs:continue
  actual={q.GetNumber():q.GetNetname()for q in fs[ref].Pads()if q.GetNumber()}
  for pin,want in comp['pins'].items():
   if want is None:continue
   count+=1;ok(ref+'.'+pin+' net agrees in manifest/schematic/PCB',actual.get(pin)==want and net.get((ref,pin))==want)
 pinchecks=0
 for row in csv.DictReader((P/'review/pinout-review.csv').open()):
  ref,pin,want=row['reference'],row['pad'],row['net'];q=next(q for q in fs[ref].Pads()if q.GetNumber()==pin);ok('manufacturer '+ref+'.'+pin,(q.GetNetCode()==0 or q.GetNetname().startswith('unconnected-'))if want=='NC'else q.GetNetname()==want);pinchecks+=1
 # Native outline coordinates, not a screenshot-derived dimension.
 bb=b.GetBoardEdgesBoundingBox();dims=[p.ToMM(bb.GetWidth()),p.ToMM(bb.GetHeight())]
 ok('35mm native outline',all(abs(x-35)<.06 for x in dims));ok('1.6mm thickness',abs(p.ToMM(b.GetDesignSettings().GetBoardThickness())-1.6)<.001);ok('two copper layers',b.GetCopperLayerCount()==2)
 vias=[t for t in b.GetTracks()if t.GetClass()=='PCB_VIA'];tracks=[t for t in b.GetTracks()if t.GetClass()=='PCB_TRACK'];pads=[q for f in fs.values()for q in f.Pads()]
 mintrack=min(p.ToMM(t.GetWidth())for t in tracks);mindrill=min(p.ToMM(t.GetDrillValue())for t in vias);minann=min((p.ToMM(t.GetWidth(p.F_Cu))-p.ToMM(t.GetDrillValue()))/2 for t in vias)
 smd=[q for q in pads if q.GetAttribute()==p.PAD_ATTRIB_SMD and(q.IsOnLayer(p.F_Cu)or q.IsOnLayer(p.B_Cu))];minpad=min(min(p.ToMM(q.GetSize().x),p.ToMM(q.GetSize().y))for q in smd)
 ok('JLC trace >=0.10mm',mintrack>=.0999);ok('JLC via drill >=0.20mm',mindrill>=.1999);ok('JLC via annulus >=0.10mm',minann>=.0999);ok('JLC SMD pad width >=0.25mm',minpad>=.2499)
 ok('JLC minimum mask web configured >=0.10mm',p.ToMM(b.GetDesignSettings().m_SolderMaskMinWidth)>=.0999)
 ok('mounting holes 2x2.2mm NPTH',len([q for q in pads if q.GetAttribute()==p.PAD_ATTRIB_NPTH and abs(p.ToMM(q.GetDrillSize().x)-2.2)<.001])==2)
 # Distinct-lead pad gap at the widened QFN is 0.15mm (0.4 pitch-0.25 width).
 u3=fs['U3'];ok('QFN20 JLC widened land',all(abs(p.ToMM(q.GetSize().y)-.25)<.001 or abs(p.ToMM(q.GetSize().x)-.25)<.001 for q in u3.Pads()if q.GetNumber()and q.GetNumber()!='21'))
 sys.path.insert(0,str(P/'firmware'));from fixture import encode,crc,ROLES
 files=list((P/'firmware/examples').glob('*.json'));fleet=[]
 for role in ROLES:
  path=P/'firmware/examples'/f'{role}.json';c=json.loads(path.read_text());data=encode(c);ok('fixture '+role,data==path.with_suffix('.bin').read_bytes()and len(data)==45 and crc(data[:-2])==int.from_bytes(data[-2:],'little'));fleet.append(c['role'])
 ok('twelve unique roles',sorted(fleet)==list(range(12)))
 for variant in ['MINI50-bench','FOX10-bench']:
  with (P/'assembly'/(variant+'-BOM.csv')).open()as f:rows=list(csv.DictReader(f))
  fitted={r['ref']:r for r in rows if r['population']!='DNP'}
  want='560'if variant.startswith('FOX')else'100'
  ok(variant+' eight consistent ballast values',all(fitted['R'+str(i)]['value']==want for i in range(31,39)))
  ok(variant+' bench matching bypassed',all('R'+str(i)in fitted and'L'+str(i-20)not in fitted for i in range(50,55))and'C30'not in fitted)
 with (P/'assembly/JLC-bench-centroids-REVIEW.csv').open()as f:centroids=list(csv.DictReader(f))
 ok('JLC centroid coordinates inside board',all(0<float(r['Mid X'][:-2])<35 and 0<float(r['Mid Y'][:-2])<35 for r in centroids))
 with (P/'assembly/MINI50-bench-BOM.csv').open()as f:fitted={r['ref']for r in csv.DictReader(f)if r['population']!='DNP'}
 ok('centroids cover fitted electrical BOM',fitted=={r['Designator']for r in centroids})
 inputs=[P/'Mini80.kicad_pcb',P/'Mini80.kicad_pro',P/'Mini80.kicad_dru',P/'Mini80.kicad_sym',P/'Mini80.electrical.json',*P.glob('*.kicad_sch'),*P.glob('Mini80.pretty/*'),*P.glob('firmware/*.c'),*P.glob('firmware/*.h'),P/'review/firmware/mini80-universal.hex',*P.glob('fabrication/*.zip')]
 hashes={str(f.relative_to(P)):hashlib.sha256(f.read_bytes()).hexdigest()for f in sorted(inputs)}
 result={'status':'PASS'if not errors else'FAIL','checks':checks,'errors':errors,'connected_pin_comparisons':count,'independent_manufacturer_pin_comparisons':pinchecks,'PCB':{'outline_with_stroke_mm':dims,'tracks':len(tracks),'vias':len(vias),'footprints':len(fs),'min_track_mm':mintrack,'min_via_drill_mm':mindrill,'min_via_annulus_mm':minann,'min_SMD_pad_dimension_mm':minpad},'physical_measurements':'NOT RUN','DFM_limit':'Local checks against published JLC capabilities; no manufacturer CAM/assembly approval or checkout','input_SHA256':hashes}
 (P/'review/verification.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k!='checks'},indent=2));return bool(errors)
if __name__=='__main__':raise SystemExit(main())
