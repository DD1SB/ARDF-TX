#!/usr/bin/env python3
"""Local engineering review exports only. Does not order, upload or regenerate PCB."""
import argparse,os,subprocess,json
from pathlib import Path
R=Path(__file__).resolve().parents[1];H=R/'hardware/80m';D=H/'review'/json.loads((H/'RF80.electrical.json').read_text())['revision'];B=str(H/'RF80.kicad_pcb');S=str(H/'RF80.kicad_sch')
def run(*args,env=None):
 r=subprocess.run(list(args),cwd=R,capture_output=True,text=True,env=env)
 if r.returncode:raise RuntimeError(' '.join(args)+'\n'+r.stdout+r.stderr)
 print('OK',' '.join(args[1:4]))
def main():
 p=argparse.ArgumentParser();p.add_argument('--render',action='store_true');a=p.parse_args();D.mkdir(exist_ok=True)
 run('kicad-cli','sch','erc','--format','json','--severity-all','--exit-code-violations','--output',str(D/'ERC.json'),S)
 run('kicad-cli','sch','export','netlist','--format','kicadxml','--output',str(D/'RF80.xml'),S)
 run('kicad-cli','sch','export','pdf','--output',str(D/'RF80.pdf'),S)
 run('kicad-cli','pcb','drc','--format','json','--severity-all','--exit-code-violations','--schematic-parity','--refill-zones','--save-board','--output',str(D/'DRC.json'),B)
 run('kicad-cli','pcb','drc','--format','report','--severity-all','--exit-code-violations','--schematic-parity','--output',str(D/'DRC.rpt'),B)
 g=D/'gerbers';g.mkdir(exist_ok=True)
 run('kicad-cli','pcb','export','gerbers','--output',str(g)+'/', '--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts','--subtract-soldermask',B)
 run('kicad-cli','pcb','export','drill','--output',str(g)+'/', '--format','excellon','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',str(D/'drill-report.rpt'),B)
 run('kicad-cli','pcb','export','ipcd356','--output',str(D/'RF80.ipc'),B)
 run('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--exclude-dnp','--output',str(D/'RF80-position-full.csv'),B)
 for name,layers in [('top-copper','F.Cu,Edge.Cuts'),('bottom-copper','B.Cu,Edge.Cuts'),('assembly','F.Fab,F.Silkscreen,Edge.Cuts'),('assembly-bottom','B.Fab,B.Silkscreen,B.Mask,Edge.Cuts')]:
  args=['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layers,'--output',str(D/(name+'.svg'))]
  if name=='assembly':args+=['--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers']
  run(*args,B)
  # KiCad emits trailing spaces on SVG path/DOCTYPE lines. Normalize whitespace
  # only so repository checks remain useful; keep all drawing tokens unchanged.
  svg=D/(name+'.svg');svg.write_text('\n'.join(line.rstrip()for line in svg.read_text().splitlines())+'\n')
 run('kicad-cli','pcb','export','pdf','--layers','F.Fab,Edge.Cuts','--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers','--output',str(D/'assembly.pdf'),B)
 run('kicad-cli','pcb','export','pdf','--layers','B.Fab,B.Silkscreen,B.Mask,Edge.Cuts','--output',str(D/'assembly-bottom.pdf'),B)
 if a.render:
  env=os.environ.copy();env.setdefault('DISPLAY',':93');env['LIBGL_ALWAYS_SOFTWARE']='1'
  for name,rot in [('RF80-3D.png','325,0,25'),('RF80-3D-top.png','0,0,0')]:
   run('kicad-cli','pcb','render','--width','2100','--height','1500','--quality','high','--background','opaque','--rotate',rot,'--output',str(D/name),B,env=env)
  run('kicad-cli','pcb','render','--width','2100','--height','1500','--quality','high','--background','opaque','--side','bottom','--output',str(D/'RF80-3D-bottom.png'),B,env=env)
if __name__=='__main__':main()
