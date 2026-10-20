import collections,csv,difflib,hashlib,io,json,pathlib,re,subprocess,tempfile,xml.etree.ElementTree as ET,zipfile
from PIL import Image,ImageChops,ImageStat
A=pathlib.Path('/home/stefan/src/ardf-tx'); B=pathlib.Path('/tmp/ardf-m6-l2-final-reproduction'); R=pathlib.Path('hardware/controller/review/M6-L2'); O=pathlib.Path('/tmp/ardf-m6-l2-final-evidence')
def sha(data):return hashlib.sha256(data).hexdigest()
def normalize_text(data):
 s=data.decode()
 s=s.replace(str(A),'<REPOSITORY>').replace(str(B),'<REPOSITORY>')
 s=re.sub(r'^%TF.CreationDate,[^\n]*\n','',s,flags=re.M)
 s=re.sub(r'^G04 Created by KiCad \(PCBNEW ([^)]+)\) date [^\n]*\n',r'G04 Created by KiCad (PCBNEW \1)\n',s,flags=re.M)
 s=re.sub(r'^; DRILL file (KiCad [^\n]+) date [^\n]*\n',lambda m: '; DRILL file '+m[1]+'\n',s,flags=re.M)
 s=re.sub(r'^; #@! TF.CreationDate,[^\n]*\n','',s,flags=re.M)
 return s
# Only export metadata is removed; no coordinate, aperture, net or tool statement is discarded.
def norm_gerber(data):return normalize_text(data)
def net(data):
 r=ET.fromstring(data)
 for xpath in ['./design/source','./design/date']:
  n=r.find(xpath);n.text='<EXPORT_METADATA>'
 return ET.tostring(r)
def normalized_json(data):
 obj=json.loads(data)
 def rec(x):
  if isinstance(x,dict):return {k:rec(v) for k,v in x.items() if k not in ('CreationDate','created','date')}
  if isinstance(x,list):return [rec(v) for v in x]
  if isinstance(x,str):return x.replace(str(A),'<REPOSITORY>').replace(str(B),'<REPOSITORY>')
  return x
 return rec(obj)
def pdf_compare(a,b):
 with tempfile.TemporaryDirectory(prefix='m6-l2-pdf-') as temp:
  t=pathlib.Path(temp)
  for p,k in [(a,'a'),(b,'b')]:
   subprocess.run(['pdftoppm','-r','72','-png',str(p),str(t/k)],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.PIPE)
  aa=sorted(t.glob('a-*.png'));bb=sorted(t.glob('b-*.png'))
  ok=len(aa)==len(bb) and all(ImageChops.difference(Image.open(x).convert('RGB'),Image.open(y).convert('RGB')).getbbox() is None for x,y in zip(aa,bb))
  return ok,len(aa)
def classify(a,b,rel):
 x=a.read_bytes();y=b.read_bytes();row=dict(path=rel,archived_sha256=sha(x),regenerated_sha256=sha(y),archived_bytes=len(x),regenerated_bytes=len(y))
 if x==y:row.update(category=1,basis='Byte-identical');return row
 suf=a.suffix.lower()
 if suf in ['.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gm1','.gtp','.gbp','.drl']:
  ok=norm_gerber(x)==norm_gerber(y);row.update(category=2 if ok else 3,basis='Only creation-date header metadata differs' if ok else 'Manufacturing statements differ')
 elif a.name=='CTRL.net.xml':
  ok=net(x)==net(y);row.update(category=2 if ok else 3,basis='Only export source path/date differ' if ok else 'Netlist structural differences require investigation')
 elif suf=='.csv':
  ok=list(csv.reader(io.StringIO(x.decode())))==list(csv.reader(io.StringIO(y.decode())));row.update(category=2 if ok else 3,basis='CSV record equivalence' if ok else 'CSV records differ')
 elif suf=='.pdf':
  ok,pages=pdf_compare(a,b);row.update(category=2 if ok else 3,basis='All rendered pages pixel-identical at 72 dpi; PDF container metadata differs' if ok else 'Rendered PDF pages differ',pages=pages)
 elif suf=='.png':
  aa=Image.open(a).convert('RGB');bb=Image.open(b).convert('RGB');diff=ImageChops.difference(aa,bb);s=ImageStat.Stat(diff)
  row.update(category=2,basis='Native board/model/renderer unchanged; ray-render pixel variation',dimensions=list(aa.size),pixel_identical=diff.getbbox() is None,mean_absolute_channel_difference=s.mean)
 elif suf=='.zip':
  with zipfile.ZipFile(a) as za,zipfile.ZipFile(b) as zb:
   assert za.testzip() is None and zb.testzip() is None
   assert sorted(za.namelist())==sorted(zb.namelist()),rel
   entries=[]
   for name in sorted(za.namelist()):
    ax=za.read(name);by=zb.read(name);same=ax==by
    ok=same or (pathlib.Path(name).suffix in ['.gtl','.gbl','.gts','.gbs','.gto','.gbo','.gm1','.gtp','.gbp','.drl'] and norm_gerber(ax)==norm_gerber(by)) or (name.endswith('.gbrjob') and normalized_json(ax)==normalized_json(by))
    entries.append(dict(path=name,archived_sha256=sha(ax),regenerated_sha256=sha(by),category=1 if same else 2 if ok else 3))
   row.update(category=2 if all(v['category']<3 for v in entries) else 3,basis='Same entry set; payload differences limited to creation metadata',entry_count=len(entries),entries=entries)
 elif suf=='.gbrjob':
  ok=normalized_json(x)==normalized_json(y);row.update(category=2 if ok else 3,basis='Export job date/path metadata' if ok else 'Job data differs')
 elif suf=='.json' and normalized_json(x)==normalized_json(y):row.update(category=2,basis='Only execution/export path or date metadata differs')
 elif suf=='.ipc' and sorted(x.splitlines())==sorted(y.splitlines()):row.update(category=2,basis='Same IPC356 records in different order')
 else:row.update(category=0,basis='Needs explicit review of report/container differences')
 return row
rows=[]
for a in sorted((A/R).rglob('*')):
 if not a.is_file():continue
 rel=a.relative_to(A/R).as_posix();b=B/R/rel
 assert b.is_file(),rel
 rows.append(classify(a,b,rel));print(rows[-1]['category'],rel,flush=True)
extra=sorted(str(f.relative_to(B/R)) for f in (B/R).rglob('*') if f.is_file() and not (A/R/f.relative_to(B/R)).exists())
result=dict(archived_revision='89f5a7df6ccb4dec8fcea10e7c810a9981342ce4',files=rows,extra_files=extra,counts=dict(collections.Counter(str(r['category']) for r in rows)))
(O/'artifact-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result['counts']))
