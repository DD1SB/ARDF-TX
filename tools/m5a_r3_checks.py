#!/usr/bin/python3
"""Read-only final checks; reports are written only in the R3 review directory."""
import copy
import csv
import hashlib
import json
import re
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import m5a_r1_verify as old
from m5a_r3_design import ROOT,DEST,OUT,preserved

def fallback():
    parts={p['ref']:p for p in json.loads((DEST/'archive/M5A-R1/RF2M.electrical.json').read_text())['parts']}
    nets={}
    for net in ET.parse(OUT/'fallback-r1.net.xml').findall('./nets/net'):
        for node in net.findall('node'):
            nets.setdefault(node.attrib['ref'],{})[node.attrib['pin']]=None if net.attrib['name'].startswith('unconnected-')else net.attrib['name']
    for r,p in parts.items():
        if not r.startswith('#'):assert nets[r]==p['pins'],r
    assert old.revised_checks(parts,nets);pins=old.audit(nets,parts);logic=old.tests(nets);power=old.power_checks(parts,nets)
    mutations=[]
    for ref,pin,wrong in [('U303','3','VDRV_FILTER'),('Q501','D','GND'),('Q501','S','PA_DRAIN'),('Q401','1','VMOD'),('U101','6','GND'),('U202','1','ARM'),('U501','4','MMIC_RF_DC'),('Q701','2','TRAIN_COLLECTOR'),('U209','2','V3V3')]:
        n=copy.deepcopy(nets);n[ref][pin]=wrong
        try:old.audit(n,parts)
        except AssertionError:mutations.append(ref+':'+pin)
        else:raise AssertionError('ArchivedR1 pin mutation escaped')
    for kind in ['path','switch']:
        n=copy.deepcopy(nets)
        if kind=='path':n['U205']['10']='PATH_Q'
        else:n['U304']['2']='HARD_OK_N'
        try:old.tests(n)if kind=='path'else old.power_checks(parts,n)
        except AssertionError:mutations.append(kind)
        else:raise AssertionError('ArchivedR1 logic mutation escaped')
    for ref,value in [('R506','100'),('C409','10u'),('F301','2A fast')]:
        p=copy.deepcopy(parts);p[ref]['value']=value
        try:old.revised_checks(p,nets)
        except AssertionError:mutations.append(ref)
        else:raise AssertionError('ArchivedR1 value mutation escaped')
    e=json.loads((OUT/'fallback-r1-erc.json').read_text());violations=[v for s in e['sheets']for v in s['violations']]
    assert len(violations)==3 and all(v['severity']=='warning'and v['type']=='footprint_filter'for v in violations)
    result=dict(status='PASS archivedR1 regression; historical reports unchanged',logic_combinations=logic['combinations'],state_scenarios=len(logic['scenarios']),mutations=mutations,pin_maps=len(pins),power_switch_checks=power,erc_errors=0,erc_open_warnings=3)
    (OUT/'fallback-r1-regression.json').write_text(json.dumps(result,indent=2)+'\n')
    return result

def main():
    f=fallback()
    docs=sorted((ROOT/'docs').glob('M5A_R3_*.md'))
    assert len(docs)==7
    links=0
    for path in docs:
        for target in re.findall(r'\]\(([^)]+)\)',path.read_text()):
            if '://'in target:continue
            target=target.split('#')[0]
            assert (path.parent/target).exists(),(path.name,'broken local link',target)
            links+=1
    costs=json.loads((OUT/'costs.json').read_text());rows=list(csv.DictReader((OUT/'RF2M_BOM.csv').open()))
    for s in costs['summary']:
        matches=[r for r in rows if r['variant']==s['variant']and int(r['fleet'])==s['fleet']]
        assert len(matches)==s['physical_components']
        assert abs(sum(float(r['allocated_per_board_net_eur'])for r in matches)-s['net_eur_allowance'])<1e-8
        assert sum(r['ref'].startswith('U')for r in matches)==s['IC_count']
    text=subprocess.check_output(['pdftotext',str(OUT/'RF2M.pdf'),'-'],text=True)
    assert 'M5A-R3'in text and 'MRF237'in text and 'TIP127'in text
    assert 'PD54008L-E'not in text and 'PHA-1+'not in text
    assert not list(DEST.glob('*.kicad_pcb'))
    assert json.loads((OUT/'preserved-baseline.json').read_text())==preserved()
    # All assigned footprints refer to an installed native library/file.
    manifest=json.loads((DEST/'RF2M.electrical.json').read_text())
    footprint_files=0
    for p in manifest['parts']:
        if not p['footprint']:continue
        lib,name=p['footprint'].split(':',1)
        assert (Path('/usr/share/kicad/footprints')/(lib+'.pretty')/(name+'.kicad_mod')).exists(),p['ref']
        footprint_files+=1
    result=dict(status='PASS scoped document/BOM/CAD checks; PCB blocked, hardware NOT_RUN',local_markdown_links_checked=links,requested_documents=len(docs),assigned_footprint_files_exist=footprint_files,fallback=f,unchanged_preserved_files=len(preserved()),external_links='Source access and failures recorded in sources.json; no claim of all external URLs passing',PCB_DRC='NOT_RUN: no defensible PCB created')
    (OUT/'final-checks.json').write_text(json.dumps(result,indent=2)+'\n')
    print('PASS',links,'local links;',len(docs),'requested documents; BOM row/totals/count parity;',footprint_files,'assigned footprint files; archivedR1',f['logic_combinations'],'combinations/',len(f['mutations']),'mutations')

if __name__=='__main__':main()
