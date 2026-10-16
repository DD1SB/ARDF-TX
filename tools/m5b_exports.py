#!/usr/bin/python3
"""Rebuild local M5B review exports. No uploads, orders or fabrication release."""
import argparse,os,subprocess,json,tempfile,sys
from pathlib import Path
from m5b_pcb import P,D
R=P.parents[1];B=P/'RF2M.kicad_pcb';S=P/'RF2M.kicad_sch';LOG=D/('check-commands.json'if '--checks'in sys.argv else'export-commands.json');logs=json.loads(LOG.read_text())if LOG.exists()else[]
def run(*args,allowed=(0,),env=None):
 r=subprocess.run([str(x)for x in args],cwd=R,capture_output=True,text=True,env=env);logs.append(dict(command=[str(x)for x in args],returncode=r.returncode,stdout=r.stdout,stderr=r.stderr,render_environment={k:env.get(k)for k in ['DISPLAY','LIBGL_ALWAYS_SOFTWARE']}if env else None));LOG.write_text(json.dumps(logs,indent=2)+'\n')
 if r.returncode not in allowed:raise RuntimeError(str(args)+'\n'+r.stdout+r.stderr)
 print('OK',*list(map(str,args))[1:4],flush=True)
def main():
 a=argparse.ArgumentParser();a.add_argument('--render',action='store_true');a.add_argument('--checks',action='store_true');x=a.parse_args();D.mkdir(exist_ok=True)
 if x.checks:
  run('kicad-cli','sch','erc','--format','json','--severity-all','--exit-code-violations','-o',D/'ERC.json',S)
  run('kicad-cli','sch','export','netlist','--format','kicadxml','-o',D/'RF2M.net.xml',S)
  # Native warnings remain visible and are individually dispositioned; code5 is not a PASS.
  run('kicad-cli','pcb','drc','--format','json','--severity-all','--exit-code-violations','--schematic-parity','--refill-zones','--save-board','-o',D/'DRC.json',B,allowed=(0,5))
  run('kicad-cli','pcb','drc','--format','report','--severity-all','--schematic-parity','-o',D/'DRC.rpt',B)
  return
 run('kicad-cli','sch','export','pdf','-o',D/'RF2M.pdf',S)
 g=D/'gerbers';g.mkdir(exist_ok=True)
 run('kicad-cli','pcb','export','gerbers','-o',str(g)+'/', '--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts','--subtract-soldermask',B)
 run('kicad-cli','pcb','export','drill','-o',str(g)+'/', '--format','excellon','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',D/'drill-report.rpt',B)
 run('kicad-cli','pcb','export','ipcd356','-o',D/'RF2M-logical.ipc',B)
 for name,layers in [('top-copper','F.Cu,Edge.Cuts'),('bottom-copper','B.Cu,Edge.Cuts'),('assembly-top','F.Fab,F.Silkscreen,Edge.Cuts'),('assembly-bottom','B.Fab,B.Silkscreen,B.Mask,Edge.Cuts')]:
  args=['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layers,'-o',D/(name+'.svg')]
  if name=='assembly-top':args+=['--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers']
  run(*args,B);svg=D/(name+'.svg');svg.write_text('\n'.join(t.rstrip()for t in svg.read_text().splitlines())+'\n')
 run('kicad-cli','pcb','export','pdf','--layers','B.Fab,B.Silkscreen,B.Mask,Edge.Cuts','-o',D/'assembly-bottom.pdf',B)
 # Generate distinct assembly/placement instructions from the same final board.
 import pcbnew as p
 from m5a_r1_costs import effective
 parts={q['ref']:q for q in json.load(open(P/'RF2M.electrical.json'))['parts']}
 for v,pops in {'BOOST2S':{'ALL','NORMAL','BOOST2S'},'BUCK4S':{'ALL','NORMAL','BUCK4S'},'TRAIN_ONLY':{'ALL','TRAIN_ONLY'}}.items():
  b=p.LoadBoard(str(B))
  for f in b.GetFootprints():
   if f.GetReference()in parts:
    part=parts[f.GetReference()];f.SetDNP(part['population']not in pops);f.SetValue(effective(part,v)[0])
  temporary=P/('RF2M_'+v+'_export.tmp.kicad_pcb')
  try:
   p.SaveBoard(str(temporary),b)
   run('kicad-cli','pcb','export','pdf','--layers','F.Fab,F.Silkscreen,Edge.Cuts','--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers','-o',D/('assembly-'+v+'.pdf'),temporary)
   run('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--exclude-dnp','-o',D/('placement-'+v+'.csv'),temporary)
  finally:
   temporary.unlink(missing_ok=True)
   temporary.with_suffix('.kicad_pro').unlink(missing_ok=True)
   temporary.with_suffix('.kicad_prl').unlink(missing_ok=True)
 if x.render:
  env=os.environ.copy();env.setdefault('DISPLAY',':96');env['LIBGL_ALWAYS_SOFTWARE']='1'
  for name,extra in [('RF2M-3D.png',['--rotate','325,0,25']),('RF2M-3D-top.png',[]),('RF2M-3D-bottom.png',['--side','bottom'])]:
   run('kicad-cli','pcb','render','--width','2000','--height','1550','--quality','high','--background','opaque',*extra,'-o',D/name,B,env=env)
if __name__=='__main__':main()
