#!/usr/bin/env python3
"""Current review links, revision/count/cost consistency and hardware hashes."""
import argparse,hashlib,json,re
from pathlib import Path
from urllib.parse import unquote
ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware/80m'
def report():
    m=json.loads((HW/'RF80.electrical.json').read_text())
    costs=json.loads((ROOT/'docs/M3_80M_COSTS.json').read_text())['scopes']
    delta=json.loads((ROOT/'docs/M3A_R1_DELTA.json').read_text())
    assert m['revision']=='M3A-R1'
    for name,pops in [('Full module components',('BOTH','NORMAL')),('Foxoring-only components',('BOTH','FOX'))]:
        physical=[p for p in m['parts']if p['population']in pops and not p['ref'].startswith(('#','TP'))]
        assert delta['configurations'][name]['after']['purchased_components']==len(physical)
        for n in ('6','10','20'):
            assert delta['configurations'][name]['batches'][n]['after_eur']==costs[name][n]['per_unit_eur']
    required=['LOGIC_AUDIT','SIMPLIFICATION','COST_DELTA','VERIFICATION','REVIEW_DECISION']
    for name in required:
        text=(ROOT/f'docs/M3A_R1_{name}.md').read_text()
        assert '2026-10-14'in text and 'M3A-R1'in text,name
    decision=(ROOT/'docs/M3A_R1_REVIEW_DECISION.md').read_text()
    for name in costs:
        if name not in delta['configurations']:continue
        for n in ('6','10','20'):assert f"{costs[name][n]['per_unit_eur']:.2f}"in decision,(name,n)
    paths=[ROOT/'README.md',*sorted((ROOT/'docs').glob('*.md')),*sorted((ROOT/'docs/decisions').glob('*.md')),*sorted(HW.glob('*.md'))]
    total=0;hardware_links=0
    for path in paths:
        for target in re.findall(r'\[[^\]]*\]\(([^\s)]+)(?:\s+"[^"]*")?\)',path.read_text()):
            if re.match(r'^[a-zA-Z][\w+.-]*:',target)or target.startswith('#'):continue
            target=unquote(target.split('#')[0].strip('<>'))
            if not target:continue
            assert (path.parent/target).exists(),(path.relative_to(ROOT),target)
            total+=1
            if path.parent==HW:hardware_links+=1
    assert not list(HW.rglob('*.kicad_pcb'))
    assert not list(HW.rglob('*.gbr'))
    files=[]
    for path in sorted(HW.rglob('*')):
        if not path.is_file():continue
        assert not path.name.endswith(('.lck','.bak'))
        data=path.read_bytes();files.append(dict(path=str(path.relative_to(ROOT)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest()))
    return dict(date='2026-10-14',revision='M3A-R1',status='Review artifacts; no layout, manufacture or physical validation',markdown_files_checked=len(paths),local_links_checked=total,hardware_local_links_checked=hardware_links,files=files)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');a=p.parse_args()
    r=report();s=json.dumps(r,indent=2)+'\n';path=ROOT/'docs/M3_80M_ARTIFACT_HASHES.json'
    if a.write:path.write_text(s)
    else:assert path.read_text()==s,'Stale hardware hashes/review link report'
    print(f"PASS: {r['markdown_files_checked']} Markdown files, {r['local_links_checked']} local links, {len(r['files'])} hardware hashes; revision/population/cost scope; no PCB")
