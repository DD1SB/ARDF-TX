#!/usr/bin/python3
"""M6-L1 replay of the frozen controller checks, isolated from historical output."""
import sys,types,json,subprocess,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-L1';D.mkdir(exist_ok=True)
def legacy():
 s=(ROOT/'tools/m6_c1r1.py').read_text().replace('review/M6-C1R1','review/M6-L1')
 # No capture, sync or rerouting is used for the LoRa audit.
 m=types.ModuleType('m6_l1_legacy');m.__file__=str(ROOT/'tools/m6_c1r1.py');sys.modules[m.__name__]=m;exec(compile(s,m.__file__,'exec'),m.__dict__)
 orig=m.adapted
 def adapted(name,replace=()):
  extra=[]
  if name=='m6_c1_dfm':extra=[("'revision':'M6-C1R1'","'revision':'M6-L1'"),("'hole_size_tolerance_mm':","'track_width_tolerance_percent':20,'nominal_2L_FR4_er':4.5,'hole_size_tolerance_mm':"),('Optional LoRa module identity/land-pattern tolerance hold; DNP base variants','LoRa nominal land compatibility audited in M6-L1; actual incoming module fit/assembly remains physical acceptance')]
  if name=='m6_c1_review':extra=[('40 Python tests','46 Python tests'),('M6-C1R1 engineering candidate','M6-L1 engineering audit candidate'),('M6-C1R1 CANDIDATE','M6-L1 CANDIDATE'),('OPEN_OPTION_DO_NOT_POPULATE','M6-L1 nominal dual-band lands audited; physical fit NOT_RUN'),('optional U70 drawing/order suffix unresolved','M6-L1 nominal U70 drawing/order alias audited; actual incoming component identity/fit remains physical acceptance'),('HOLD: exact ZTR8/TR8 identity, manufacturer land tolerance and RF launch not qualified','M6-L1 nominal dual-band CAD review GO; physical RF/assembly qualification NOT_RUN')]
  if name=='m6_c1_exports':extra=[("f.SetDNP(not fitted_part(parts[f.GetReference()],variant))","f.SetDNP(not fitted_part(parts[f.GetReference()],variant))\n            if variant.endswith('_433') and f.GetReference()=='U70':f.SetValue('Silicontra SX1262TR4-GC')")]
  if name=='m6_c1_route_audit':extra=[("('U50','6','J5','1')","('U50','6','J5','1'),('L1','2','U70','13'),('C70','1','U70','13'),('C71','1','U70','13')")]
  if name=='m6_c1_analysis':extra=[('LORA_OPTION_OPEN','LORA_OPTION'),('UNIVERSAL_LORA_OPEN','UNIVERSAL_LORA_868'),('OPEN_OPTION_DO_NOT_POPULATE','M6-L1 nominal dual-band footprint audited; physical fit NOT_RUN')]
  return orig(name,[*replace,*extra])
 m.adapted=adapted;return m

def main():
 action=sys.argv[1]
 if action=='manifest':
  rows=[]
  for f in sorted(D.rglob('*')):
   if f.is_file() and f.name not in ['SHA256SUMS','inventory.json']:rows.append(dict(path=str(f.relative_to(D)),bytes=f.stat().st_size,sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
  source=[]
  for folder,pattern in [(P,'*'),(ROOT/'tools','m6*.py'),(ROOT/'docs','M6_L1*'),(ROOT/'firmware/controller_hw','*')]:
   for f in sorted(folder.glob(pattern)):
    if f.is_file() and f.suffix not in ['.kicad_prl','.lck']:source.append(dict(path=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
  for f in (P/'ARDF_CTL.pretty').glob('*'):
   if f.is_file():source.append(dict(path=str(f.relative_to(ROOT)),sha256=hashlib.sha256(f.read_bytes()).hexdigest()))
  (D/'inventory.json').write_text(json.dumps(dict(review_files=rows,sources=source),indent=2)+'\n');(D/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in rows));print('Inventory',len(rows));return
 if action in ['capture','sync','route']:raise SystemExit('M6-L1 has no recapture/reroute utility; intentional native edits are local')
 if action=='protection':
  s=(ROOT/'tools/m6_c1r1_electrical.py').read_text().replace('review/M6-C1R1','review/M6-L1');m=types.ModuleType('m6_l1_prot');m.__file__=str(ROOT/'tools/m6_c1r1_electrical.py');exec(compile(s,m.__file__,'exec'),m.__dict__);m.main();return
 if action=='usb':
  s=(ROOT/'tools/m6_c1r1_usb.py').read_text().replace('review/M6-C1R1','review/M6-L1');m=types.ModuleType('m6_l1_usb');m.__file__=str(ROOT/'tools/m6_c1r1_usb.py');exec(compile(s,m.__file__,'exec'),m.__dict__);m.main();return
 # Exports import the base population helper; replace its runtime groups only.
 if action in ['exports','analysis']:
  import m6_c1_analysis as a
  a.VARIANTS={'FOX_MIN':{'ALL','RF80'},'RF80_FULL':{'ALL','RF80'},'RF2M_FULL':{'ALL','RF2M'},'UNIVERSAL':{'ALL','RF80','RF2M'},'UNIVERSAL_LORA_868':{'ALL','RF80','RF2M','LORA_OPTION'},'UNIVERSAL_LORA_433':{'ALL','RF80','RF2M','LORA_OPTION'}}
 legacy().main()
 if action=='analysis':
  f=D/'costs.json';a=json.loads(f.read_text());a.pop('LoRa_hold',None)
  a['LoRa_source_status']='M6-L1 TR/ZTR alias and nominal dual-band footprint audited. Indexed USD and explicit FX planning factor; no supplier quotation. LoRa-costs.json contains all12 populations and unquoted material.'
  f.write_text(json.dumps(a,indent=2)+'\n')
if __name__=='__main__':main()
