#!/usr/bin/python3
"""Local-only L2 production-data exports; never orders or uploads anything.

The native KiCad sources are authoritative. Exports do not replay exploratory
placement/routing operations. Packaging requires all native CAD gates to pass.
"""
import argparse, json, subprocess, os, zipfile, hashlib, csv, re
from pathlib import Path
import pcbnew as p
from m6_l2_design import P,D,ROOT
from m6_l2_bom import fitted, RF, LORA, OPTIONS
B=P/'CTRL.kicad_pcb';S=P/'CTRL.kicad_sch'

def main():
 ap=argparse.ArgumentParser();ap.add_argument('action',choices=['exports','render','package']);a=ap.parse_args();logs=[]
 def run(*cmd):
  r=subprocess.run(list(map(str,cmd)),cwd=ROOT,capture_output=True,text=True)
  logs.append(dict(command=list(map(str,cmd)),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr))
  (D/('L2-'+a.action+'-commands.json')).write_text(json.dumps(logs,indent=2)+'\n')
  assert r.returncode==0,r.stdout+r.stderr
  args=list(map(str,cmd))
  if '-o' in args:
   target=Path(args[args.index('-o')+1])
   if target.suffix=='.svg' and target.is_file():target.write_text('\n'.join(line.rstrip() for line in target.read_text().splitlines())+'\n')
  print('PASS',*list(map(str,cmd))[1:4],flush=True)
 if a.action=='exports':
  run('kicad-cli','sch','export','pdf','-o',D/'CTRL-M6-L2.pdf',S)
  fab=D/'fabrication';fab.mkdir(exist_ok=True)
  run('kicad-cli','pcb','export','gerbers','--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts','--subtract-soldermask','--check-zones','-o',str(fab)+'/',B)
  run('kicad-cli','pcb','export','drill','--format','excellon','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',D/'drill-report.rpt','-o',str(fab)+'/',B)
  run('kicad-cli','pcb','export','ipcd356','-o',D/'CTRL-M6-L2.ipc',B)
  for name,layers,mirror in [('PCB-top','F.Cu,F.Mask,F.Silkscreen,Edge.Cuts',False),('PCB-bottom','B.Cu,B.Mask,B.Silkscreen,Edge.Cuts',True),('assembly-top','F.Fab,F.Silkscreen,Edge.Cuts',False),('assembly-bottom','B.Fab,B.Silkscreen,Edge.Cuts',True)]:
   args=['--mirror'] if mirror else []
   run('kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layers,*args,'-o',D/(name+'.svg'),B)
   run('kicad-cli','pcb','export','pdf','--mode-single','--layers',layers,*args,'--sketch-pads-on-fab-layers','-o',D/(name+'.pdf'),B)
  parts={z['ref']:z for z in json.loads((P/'CTRL.electrical.json').read_text())['parts']}
  placement=[]
  native=p.LoadBoard(str(B))
  for f in native.GetFootprints():
   placement.append(dict(reference=f.GetReference(),x_mm=p.ToMM(f.GetPosition().x),y_mm=p.ToMM(f.GetPosition().y),rotation_deg=f.GetOrientationDegrees(),side='B' if f.GetLayer()==p.B_Cu else 'F',footprint=f.GetFPIDAsString()))
  with (D/'placement-all-native.csv').open('w') as out:
   w=csv.DictWriter(out,fieldnames=list(placement[0]),lineterminator='\n');w.writeheader();w.writerows(placement)
  temp=P/'CTRL_M6_L2_export.tmp.kicad_pcb'
  try:
   for rf in RF:
    for lora in LORA:
     for opt in OPTIONS:
      name=rf+'__'+lora+'__'+opt;b=p.LoadBoard(str(B))
      for f in b.GetFootprints():
       ref=f.GetReference()
       if ref in parts:f.SetDNP(not fitted(parts[ref],rf,lora,opt))
       if ref=='U70' and lora=='LORA_433':f.SetValue('Silicontra SX1262TR4-GC')
      p.SaveBoard(str(temp),b)
      run('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--exclude-dnp','-o',D/('placement-'+name+'.csv'),temp)
      if rf=='UNIVERSAL' and lora=='NO_LORA':
       for side,layer,mir in [('top','F',[]),('bottom','B',['--mirror'])]:
        run('kicad-cli','pcb','export','pdf','--mode-single','--layers',layer+'.Fab,'+layer+'.Silkscreen,Edge.Cuts',*mir,'--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers','-o',D/('assembly-'+opt+'-'+side+'.pdf'),temp)
   # Full top stencil intentionally includes optional SMD lands in one export.
   b=p.LoadBoard(str(B))
   for f in b.GetFootprints():f.SetDNP(False)
   p.SaveBoard(str(temp),b);st=D/'stencil';st.mkdir(exist_ok=True)
   run('kicad-cli','pcb','export','gerbers','--layers','F.Paste,Edge.Cuts','-o',str(st)+'/',temp)
  finally:
   for ext in ['.kicad_pcb','.kicad_pro','.kicad_prl']:temp.with_suffix(ext).unlink(missing_ok=True)
 elif a.action=='render':
  model=Path(os.environ.get('M6_L2_MODEL_DIR','/tmp/m6l2/references'))
  assert (model/'ESP32-S3-WROOM-1U.step').exists(),'Retrieve the manufacturer STEP per source-register.json and set M6_L2_MODEL_DIR'
  for name,args in [('assembly-3D-isometric',['--rotate','325,0,25']),('assembly-3D-top',[]),('assembly-3D-bottom',['--side','bottom'])]:
   run('kicad-cli','pcb','render','--define-var','M6_L2_MODEL_DIR='+str(model),'--width','1600','--height','1400','--quality','high','--zoom','0.8','--background','opaque',*args,'-o',D/(name+'.png'),B)
  temp=P/'CTRL_M6_L2_render.tmp.kicad_pcb'
  try:
   parts={z['ref']:z for z in json.loads((P/'CTRL.electrical.json').read_text())['parts']};board=p.LoadBoard(str(B))
   for fp in board.GetFootprints():
    if fp.GetReference() in parts:fp.SetDNP(not fitted(parts[fp.GetReference()],'UNIVERSAL','LORA_868','BOTH'))
   p.SaveBoard(str(temp),board)
   for name,args in [('assembly-3D-BOTH-top',['--rotate','325,0,25']),('assembly-3D-BOTH-bottom',['--side','bottom','--rotate','325,0,25'])]:
    run('kicad-cli','pcb','render','--define-var','M6_L2_MODEL_DIR='+str(model),'--width','1600','--height','1400','--quality','high','--zoom','0.8','--background','opaque',*args,'-o',D/(name+'.png'),temp)
  finally:
   for ext in ['.kicad_pcb','.kicad_pro','.kicad_prl']:temp.with_suffix(ext).unlink(missing_ok=True)

 else:
  cad=json.loads((D/'CAD-results.json').read_text())
  for k in ['ERC_violations','DRC_errors','DRC_warnings','unrouted','parity']:assert cad[k]==0,(k,cad[k])
  assert not cad['exclusions']
  native_hash=hashlib.sha256(B.read_bytes()).hexdigest()
  for report in ['L1-L2-change-audit.json','JLCPCB-DFM.json','L2-bus-power-layout-calculations.json']:
   assert json.loads((D/report).read_text())['native_sha256']==native_hash,report+' is stale'
  def zipout(name,files):
   rows=[]
   with zipfile.ZipFile(D/name,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
    for src,arc in sorted(files):
     data=src.read_bytes();info=zipfile.ZipInfo(arc,date_time=(2026,10,20,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,data)
     rows.append(dict(path=arc,sha256=hashlib.sha256(data).hexdigest(),bytes=len(data)))
   return dict(file=name,sha256=hashlib.sha256((D/name).read_bytes()).hexdigest(),entries=rows)
  fab=D/'fabrication';files=[(f,f.name) for f in fab.iterdir() if f.suffix in ['.gbr','.gbl','.gtl','.gbs','.gts','.gbo','.gto','.gko','.gm1','.drl'] and 'Paste' not in f.name]
  assert any('PTH' in f.name and 'NPTH' not in f.name for f,_ in files) and any('NPTH' in f.name for f,_ in files)
  assert len(files)==9,'Seven board layers and two separate drill files required'
  edge=(fab/'CTRL-Edge_Cuts.gm1').read_text();assert '%FSLAX46Y46*%' in edge and '%MOMM*%' in edge
  points=[tuple(int(v)/1e6 for v in xy) for xy in re.findall(r'X(-?\d+)Y(-?\d+)D0[12]\*',edge)]
  outline=[max(v[i] for v in points)-min(v[i] for v in points) for i in [0,1]]
  assert outline==[100,100],outline
  drills={}
  for f,_ in files:
   if f.suffix!='.drl':continue
   data=f.read_text();assert '\nMETRIC\n' in data
   plated='NPTH' not in f.name;assert ('Plated,1,2,PTH' if plated else 'NonPlated,1,2,NPTH') in data
   counts={};sizes={int(n):float(v) for n,v in re.findall(r'^T(\d+)C([\d.]+)$',data,re.M)};tool=None
   for line in data.splitlines():
    if re.fullmatch(r'T\d+',line):tool=int(line[1:])
    elif line.startswith('X'):
     assert tool in sizes;counts[tool]=counts.get(tool,0)+1
   drills[f.name]=dict(plated=plated,tools=[dict(diameter_mm=sizes[k],holes=v) for k,v in counts.items()])
  holes=sum(t['holes'] for v in drills.values() for t in v['tools'])
  assert holes==json.loads((D/'JLCPCB-DFM.json').read_text())['statistics']['holes'],holes
  paste=next((D/'stencil').glob('*F_Paste.gtp')).read_text();assert '%FSLAX46Y46*%' in paste
  flashes={tuple(map(int,xy)) for xy in re.findall(r'X(-?\d+)Y(-?\d+)D03\*',paste)}
  board=p.LoadBoard(str(B));paste_checks=[]
  for fp in board.GetFootprints():
   if fp.GetReference() not in ['U10','U82','C83','D82']:continue
   for pad in fp.Pads():
    if not pad.IsOnLayer(p.F_Paste):continue
    at=(pad.GetPosition().x,-pad.GetPosition().y);assert at in flashes,(fp.GetReference(),pad.GetNumber(),at)
    paste_checks.append(dict(reference=fp.GetReference(),pin=pad.GetNumber(),native_and_Gerber_mm=[at[0]/1e6,at[1]/1e6]))
  (D/'fabrication-geometry-audit.json').write_text(json.dumps(dict(status='PASS',native_sha256=native_hash,Gerber_outline_mm=outline,separate_drills=drills,native_and_exported_holes=holes,full_top_stencil_critical_flashes=paste_checks,limitation='Export integrity and native DFM; not supplier CAM acceptance or stencil/reflow qualification.'),indent=2)+'\n')
  files.append((D/'FABRICATION-INSTRUCTIONS.txt','FABRICATION-INSTRUCTIONS.txt'))
  reports=[zipout('ARDF_TX_CTRL_M6-L2_JLCPCB_5pcs_BARE.zip',files),zipout('ARDF_TX_CTRL_M6-L2_FULL_TOP_STENCIL.zip',[(f,f.name) for f in (D/'stencil').iterdir() if f.is_file()])]
  (D/'fabrication-package-audit.json').write_text(json.dumps(dict(status='PASS',native_sha256=native_hash,packages=reports,remote_upload=False,order=False),indent=2)+'\n')
if __name__=='__main__':main()
