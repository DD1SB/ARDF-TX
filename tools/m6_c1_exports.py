#!/usr/bin/python3
"""Local reproducible M6-C1 checks/exports only. No external submission."""
import argparse,subprocess,json,os,hashlib,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1';B=P/'CTRL.kicad_pcb';S=P/'CTRL.kicad_sch'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('action',choices=['checks','exports','manifest']);ap.add_argument('--render',action='store_true');a=ap.parse_args();logs=[];log_name='check-commands.json' if a.action=='checks' else 'export-commands.json'
    def run(*cmd,allowed=(0,),env=None):
        r=subprocess.run(list(map(str,cmd)),cwd=ROOT,capture_output=True,text=True,env=env);logs.append(dict(command=list(map(str,cmd)),returncode=r.returncode,stdout=r.stdout,stderr=r.stderr));(D/log_name).write_text(json.dumps(logs,indent=2)+'\n');print(r.returncode,*list(map(str,cmd))[1:4],flush=True)
        if r.returncode not in allowed:raise RuntimeError(r.stdout+r.stderr)
    if a.action=='checks':
        run('kicad-cli','sch','erc','--format','json','--severity-all','--exit-code-violations','-o',D/'ERC.json',S)
        run('kicad-cli','sch','export','netlist','--format','kicadxml','-o',D/'CTRL.net.xml',S)
        run('kicad-cli','pcb','drc','--format','json','--severity-all','--exit-code-violations','--schematic-parity','--refill-zones','--save-board','-o',D/'DRC.json',B,allowed=(0,5))
        run('kicad-cli','pcb','drc','--format','report','--severity-all','--schematic-parity','-o',D/'DRC.rpt',B)
        r=json.loads((D/'DRC.json').read_text());e=json.loads((D/'ERC.json').read_text());viol=r['violations'];unr=r['unconnected_items'];par=r.get('schematic_parity',[])
        result={'kicad':subprocess.check_output(['kicad-cli','version'],text=True).strip(),'ERC_violations':sum(len(x.get('violations',[])) for x in e.get('sheets',[])),'DRC_errors':sum(v['severity']=='error' for v in viol),'DRC_warnings':sum(v['severity']=='warning' for v in viol),'unrouted':len(unr),'parity':len(par),'physical_tests':'NOT_RUN'}
        pro=json.loads((P/'CTRL.kicad_pro').read_text())['board']['design_settings'];result['exclusions']=pro['drc_exclusions'];result['ignored_categories']=[k for k,v in pro['rule_severities'].items() if v=='ignore'];(D/'CAD-results.json').write_text(json.dumps(result,indent=2)+'\n');print(result);return
    if a.action=='manifest':
        rows=[]
        for f in sorted(D.rglob('*')):
            if not f.is_file() or f.name in ['SHA256SUMS','inventory.json'] or '__pycache__' in str(f):continue
            rows.append({'path':str(f.relative_to(D)),'bytes':f.stat().st_size,'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
        native=[]
        for f in sorted(P.rglob('*')):
            if f.is_file() and 'review' not in f.relative_to(P).parts and f.suffix not in ['.kicad_prl','.lck'] and '__pycache__' not in str(f):native.append({'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
        repro=[]
        for folder,pattern in [(ROOT/'tools','m6_c1*.py'),(ROOT/'docs','M6_C1*.md'),(ROOT/'firmware/controller_hw','*')]:
            for f in sorted(folder.glob(pattern)):
                if f.is_file():repro.append({'path':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()})
        (D/'inventory.json').write_text(json.dumps({'review_files':rows,'native_sources':native,'reproduction_sources':repro},indent=2)+'\n');(D/'SHA256SUMS').write_text(''.join(x['sha256']+'  '+x['path']+'\n' for x in rows));print('Inventory',len(rows),'files');return
    run('kicad-cli','sch','export','pdf','-o',D/'CTRL.pdf',S)
    g=D/'fabrication';g.mkdir(exist_ok=True)
    run('kicad-cli','pcb','export','gerbers','-o',str(g)+'/', '--layers','F.Cu,B.Cu,F.Mask,B.Mask,F.Paste,B.Paste,F.Silkscreen,B.Silkscreen,Edge.Cuts','--subtract-soldermask',B)
    run('kicad-cli','pcb','export','drill','-o',str(g)+'/', '--format','excellon','--excellon-units','mm','--excellon-separate-th','--generate-map','--map-format','pdf','--generate-report','--report-path',D/'drill-report.rpt',B)
    run('kicad-cli','pcb','export','ipcd356','-o',D/'CTRL-KiCad.ipc',B)
    for name,layers in [('top-copper','F.Cu,Edge.Cuts'),('bottom-copper','B.Cu,Edge.Cuts'),('assembly-top','F.Fab,F.Silkscreen,Edge.Cuts'),('assembly-bottom','B.Fab,B.Silkscreen,B.Mask,Edge.Cuts')]:
        args=['kicad-cli','pcb','export','svg','--mode-single','--fit-page-to-board','--exclude-drawing-sheet','--layers',layers,'-o',D/(name+'.svg')]
        if name=='assembly-top':args+=['--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers']
        run(*args,B)
        svg=D/(name+'.svg');svg.write_text('\n'.join(line.rstrip() for line in svg.read_text().splitlines())+'\n')
    import pcbnew as p
    from m6_c1_analysis import VARIANTS,fitted_part
    parts={x['ref']:x for x in json.loads((P/'CTRL.electrical.json').read_text())['parts']}
    for variant,groups in VARIANTS.items():
        if variant.endswith('_OPEN'):continue
        b=p.LoadBoard(str(B))
        for f in b.GetFootprints():
            if f.GetReference() in parts:f.SetDNP(not fitted_part(parts[f.GetReference()],variant))
        temp=P/('CTRL_'+variant+'_export.tmp.kicad_pcb')
        try:
            p.SaveBoard(str(temp),b)
            run('kicad-cli','pcb','export','pdf','--layers','F.Fab,F.Silkscreen,Edge.Cuts','--sketch-pads-on-fab-layers','--crossout-DNP-footprints-on-fab-layers','-o',D/('assembly-'+variant+'.pdf'),temp)
            run('kicad-cli','pcb','export','pos','--format','csv','--units','mm','--exclude-dnp','-o',D/('placement-'+variant+'.csv'),temp)
        finally:
            temp.unlink(missing_ok=True);temp.with_suffix('.kicad_pro').unlink(missing_ok=True);temp.with_suffix('.kicad_prl').unlink(missing_ok=True)
    if a.render:
        env=os.environ.copy();env['DISPLAY']=':97';env['LIBGL_ALWAYS_SOFTWARE']='1'
        for n,args in [('CTRL-3D.png',['--rotate','325,0,25']),('CTRL-3D-top.png',[]),('CTRL-3D-bottom.png',['--side','bottom'])]:run('kicad-cli','pcb','render','--width','1600','--height','1400','--quality','high','--zoom','0.75','--background','opaque',*args,'-o',D/n,B,env=env)
if __name__=='__main__':main()
