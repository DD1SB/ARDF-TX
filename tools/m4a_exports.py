#!/usr/bin/python3
"""Generate only V1 local engineering-review exports, never frozen E2.
No vendor communication, orders, physical measurements or release action.
"""
import argparse,csv,json,os,subprocess
from pathlib import Path
from m4a_design import R,P,D,NAME
B=str(P/(NAME+'.kicad_pcb'));S=str(P/(NAME+'.kicad_sch'))
def run(*args,env=None):
    r=subprocess.run(list(args),cwd=R,capture_output=True,text=True,env=env)
    with(D/'export-commands.log').open('a')as out:out.write(' '.join(args)+'\n'+r.stdout+r.stderr+'\nEXIT '+str(r.returncode)+'\n')
    if r.returncode:raise RuntimeError(' '.join(args)+'\n'+r.stdout+r.stderr)
    print('OK',' '.join(args[1:4]),flush=True)
def main():
    a=argparse.ArgumentParser();a.add_argument('--render',action='store_true');a.add_argument('--only-render',action='store_true');args=a.parse_args();D.mkdir(exist_ok=True)
    if not args.only_render:
        (D/'export-commands.log').write_text('V1 local exports; frozen reference not changed\n')
        run('kicad-cli','sch','erc','--format','json','--severity-all','--exit-code-violations','--output',str(D/'ERC.json'),S)
        run('kicad-cli','sch','export','netlist','--format','kicadxml','--output',str(D/(NAME+'.xml')),S)
        run('kicad-cli','sch','export','pdf','--output',str(D/(NAME+'.pdf')),S)
        run('kicad-cli','pcb','drc','--format','json','--all-track-errors','--severity-all','--exit-code-violations','--schematic-parity','--refill-zones','--save-board','--output',str(D/'DRC.json'),B)
        run('kicad-cli','pcb','drc','--format','report','--all-track-errors','--severity-all','--exit-code-violations','--schematic-parity','--output',str(D/'DRC.rpt'),B)
        g=D/'gerbers';g.mkdir(exist_ok=True)
        run('kicad-cli','pcb','export','gerbers','--output',str(g)+'/', '--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts','--subtract-soldermask',B)
        run('kicad-cli','pcb','export','drill','--output',str(g)+'/', '--format','excellon','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',str(D/'drill-report.rpt'),B)
        run('kicad-cli','pcb','export','ipcd356','--output',str(D/(NAME+'.ipc')),B)
        run('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--exclude-dnp','--output',str(D/(NAME+'-position-full.csv')),B)
        # One physical PCB, explicit Fox-only assembly list; do not change native DNP.
        fitted={p['ref']for p in json.loads((P/(NAME+'.electrical.json')).read_text())['parts']if p['population']in('BOTH','FOX')and not p['ref'].startswith(('TP','#'))}
        full=list(csv.DictReader((D/(NAME+'-position-full.csv')).open()));fields=list(full[0])
        # Full placement export omits the three Fox-only links; obtain all positions once.
        run('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--output',str(D/(NAME+'-position-all.csv')),B)
        allrows=list(csv.DictReader((D/(NAME+'-position-all.csv')).open()))
        with(D/(NAME+'-position-fox.csv')).open('w')as out:
            w=csv.DictWriter(out,fieldnames=fields,lineterminator='\n');w.writeheader();w.writerows(x for x in allrows if x.get('Ref',x.get('Reference',''))in fitted)
        for name,layers in [('top-copper','F.Cu,Edge.Cuts'),('bottom-copper','B.Cu,Edge.Cuts'),('assembly','F.Fab,F.Silkscreen,Edge.Cuts'),('assembly-bottom','B.Fab,B.Silkscreen,B.Mask,Edge.Cuts')]:
            cmd=['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layers,'--output',str(D/(name+'.svg'))]
            if name=='assembly':cmd+=['--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers']
            run(*cmd,B);svg=D/(name+'.svg');svg.write_text('\n'.join(line.rstrip()for line in svg.read_text().splitlines())+'\n')
        run('kicad-cli','pcb','export','pdf','--layers','F.Fab,F.Silkscreen,Edge.Cuts','--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers','--output',str(D/'assembly.pdf'),B)
        run('kicad-cli','pcb','export','pdf','--layers','B.Fab,B.Silkscreen,B.Mask,Edge.Cuts','--output',str(D/'assembly-bottom.pdf'),B)
    if args.render or args.only_render:
        env=os.environ.copy();env.setdefault('DISPLAY',':93');env['LIBGL_ALWAYS_SOFTWARE']='1'
        for name,rot in [(NAME+'-3D.png','325,0,25'),(NAME+'-3D-top.png','0,0,0')]:
            run('kicad-cli','pcb','render','--width','2100','--height','1500','--quality','high','--background','opaque','--rotate',rot,'--output',str(D/name),B,env=env)
        run('kicad-cli','pcb','render','--width','2100','--height','1500','--quality','high','--background','opaque','--side','bottom','--output',str(D/(NAME+'-3D-bottom.png')),B,env=env)
if __name__=='__main__':main()
