"""Compare fresh reproduction against the immutable reviewed implementation."""
from pathlib import Path
import hashlib,json,re,zipfile,csv,io,xml.etree.ElementTree as ET
OLD=Path('/tmp/m5b-e6r2-main-reviewed-baseline')
NEW=Path('/tmp/ardf-tx-e6r2-main-reproduction-20261021')
DEST=Path('/tmp/m5b-e6r2-main-evidence')
REL=Path('hardware/2m/review/M5B-E6R2')
sha=lambda b:hashlib.sha256(b).hexdigest()
def cam(data):
 rows=[]
 for line in data.decode().splitlines():
  if line.startswith(('%TF.CreationDate,','; #@! TF.CreationDate,','; Creation date')):continue
  if line.startswith(('G04 Created by KiCad (PCBNEW','; DRILL file KiCad ')):
   line=re.sub(r' date \d{4}-\d\d-\d\d[ T]\d\d:\d\d:\d\d',' date <EXPORT_TIMESTAMP>',line)
  rows.append(line)
 return '\n'.join(rows)
def step(data):
 text=data.decode()
 text=re.sub(r"(FILE_NAME\('[^']*',)'\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d'",r"\1'<CREATION_DATE>'",text)
 text=re.sub(r'\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b','<PRODUCT_UUID>',text,flags=re.I)
 # OCCT emits presentation records in hash-map order. Compare every geometric
 # entity verbatim by ID, then resolve the style graph onto those same IDs.
 # This retains per-shape RGB assignments instead of dropping color records.
 presentation={'MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION',
  'STYLED_ITEM','PRESENTATION_STYLE_ASSIGNMENT','SURFACE_STYLE_USAGE',
  'SURFACE_SIDE_STYLE','SURFACE_STYLE_FILL_AREA','FILL_AREA_STYLE',
  'FILL_AREA_STYLE_COLOUR','COLOUR_RGB'}
 compact=lambda value:re.sub(r"'(?:''|[^'])*'|\s+",lambda m:m.group(0)if m.group(0).startswith("'")else '',value)
 definitions={int(k):compact(v)for k,v in re.findall(r'#(\d+)\s*=\s*(.*?);',text,re.S)}
 style={k for k,v in definitions.items()if any(v.startswith(t+'(')for t in presentation)}
 geometry={k:v for k,v in definitions.items()if k not in style}
 assert all(not any(int(ref)in style for ref in re.findall(r'#(\d+)',v))for v in geometry.values()),'Unexpected geometry reference to a style entity'
 def resolve(k):
  if k not in style:
   assert k in geometry
   return '<GEOMETRY#'+str(k)+'>'
  return re.sub(r'#(\d+)',lambda m:resolve(int(m.group(1))),definitions[k])
 roots=sorted(resolve(k)for k in style if definitions[k].startswith('MECHANICAL_DESIGN_GEOMETRIC_PRESENTATION_REPRESENTATION('))
 assert roots
 return compact(text.split('DATA;')[0]),geometry,roots,sorted(resolve(k)for k in style)
def entry(name,a,b):
 exact=a==b
 if exact:kind='BYTE_IDENTICAL'
 elif Path(name).suffix.lower()in ['.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1','.drl']:
  assert cam(a)==cam(b),('MANUFACTURING_DIFFERENCE',name);kind='IDENTICAL_GEOMETRY_CREATION_TIMESTAMP_ONLY'
 elif Path(name).suffix.lower()in ['.step','.stp']:
  assert step(a)==step(b),('STEP_GEOMETRY_OR_TOPOLOGY_DIFFERENCE',name);kind='IDENTICAL_GEOMETRY_COLORS_TIMESTAMP_UUID_PRESENTATION_ORDER_ONLY'
 elif str(name)in ['BOM_BUCK4S.csv','BOM_BOOST2S.csv','RF2M_BOM_all_quantities.csv']:
  aa=list(csv.DictReader(io.StringIO(a.decode())));bb=list(csv.DictReader(io.StringIO(b.decode())))
  assert len(aa)==len(bb)
  changed=[]
  for old,new in zip(aa,bb):
   if old==new:continue
   assert old.keys()==new.keys() and {k for k in old if old[k]!=new[k]}=={'source'}
   assert old['ref']in ['C970','C971','C972','C973'] and old['MPN']=='GRM188R71H104KA93D'
   assert old['source']=='https://www.ti.com' and new['source']=='https://www.murata.com/en-global/products/capacitor/ceramiccapacitor'
   changed.append(dict(ref=old['ref'],variant=old['variant'],fleet=old['fleet'],field='source',reviewed=old['source'],fresh=new['source']))
  assert changed
  return dict(file=str(name),classification='IDENTICAL_PARTS_QUANTITIES_COSTS_CAPACITOR_REFERENCE_URL_ONLY',reviewed_SHA256=sha(a),reproduced_SHA256=sha(b),reference_URL_changes=changed)
 else:raise AssertionError(('UNCLASSIFIED_DIFFERENCE',name))
 return dict(file=str(name),classification=kind,reviewed_SHA256=sha(a),reproduced_SHA256=sha(b))
def nets(path):
 tree=ET.parse(path)
 return dict(nets=sorted((n.get('name'),sorted((v.get('ref'),v.get('pin'))for v in n.findall('node')))for n in tree.findall('./nets/net')),components=sorted((c.get('ref'),c.findtext('value'),c.findtext('footprint'),sorted((v.get('name'),v.text or '')for v in c.findall('./fields/field')))for c in tree.findall('./components/comp')))
def main():
 ledger=json.loads((DEST/'execution.json').read_text());assert len(ledger)==19 and all(r['returncode']==0 for r in ledger),'Full reproduction must complete first'
 rows=[]
 for name,expected in json.loads((OLD/REL/'native-inputs.json').read_text()).items():
  a=(OLD/name).read_bytes();assert sha(a)==expected
  rows.append(entry(name,a,(NEW/name).read_bytes()))
 assert nets(OLD/REL/'RF2M.net.xml')==nets(NEW/REL/'RF2M.net.xml')
 cams=[]
 for path in sorted((OLD/REL/'gerbers').iterdir()):
  if path.suffix in ['.gtl','.gbl','.gts','.gbs','.gtp','.gbp','.gto','.gbo','.gm1','.drl']:cams.append(entry(path.name,path.read_bytes(),(NEW/REL/'gerbers'/path.name).read_bytes()))
 assert len(cams)==11
 archives=[]
 for name in ['fabrication/RF2M-M5B-E6R2_JLCPCB_5boards.zip','fabrication/RF2M-M5B-E6R2_FULL_TOP_STENCIL.zip','RF2M-M5B-E6R2-native.zip']:
  original=OLD/REL/name;fresh=NEW/REL/name
  with zipfile.ZipFile(original)as a,zipfile.ZipFile(fresh)as b:
   assert a.testzip()is None and b.testzip()is None and sorted(a.namelist())==sorted(b.namelist())
   entries=[entry(n,a.read(n),b.read(n))for n in sorted(a.namelist())]
  archives.append(dict(file=name,reviewed_SHA256=sha(original.read_bytes()),reproduced_SHA256=sha(fresh.read_bytes()),entries=entries))
 bom=[]
 for name in ['BOM_BUCK4S.csv','BOM_BOOST2S.csv','BOM_TRAIN_ONLY.csv','RF2M_BOM_all_quantities.csv','shared-heatsink-BOM.csv','costs.json','placement-BUCK4S.csv','placement-BOOST2S.csv','placement-TRAIN_ONLY.csv']:
  bom.append(entry(name,(OLD/REL/name).read_bytes(),(NEW/REL/name).read_bytes()))
 mechanical=[]
 for name in ['mechanical/thermal-assembly.step','mechanical/complete-mechanical-stack.step']:
  mechanical.append(entry(name,(OLD/REL/name).read_bytes(),(NEW/REL/name).read_bytes()))
 # Both exact-byte inventory files must describe their respective review trees.
 for base in [OLD,NEW]:
  for name,h in json.loads((base/REL/'SHA256SUMS.json').read_text()).items():assert sha((base/REL/name).read_bytes())==h,(str(base),'Inventory',name)
 report=dict(status='PASS',candidate_commit='2fff32131dd0f7da3c46fef47c04713a55df89d8',native_inputs=rows,CAM=cams,netlist_semantics_equal=True,archives=archives,BOM_and_positions=bom,mechanical_STEP=mechanical,reviewed_manufacturing_files_replaced=False,physical_qualification='NOT_RUN')
 (DEST/'artifact-comparison.json').write_text(json.dumps(report,indent=2)+'\n')
 print('PASS:114 native inputs;11 CAM files;netlist;3ZIPs;9BOM/position/cost outputs;2assemblySTEP;both inventories')
if __name__=='__main__':main()
