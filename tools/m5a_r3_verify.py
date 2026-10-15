#!/usr/bin/python3
"""Netlist-derived checks for the private DL3BBX derivative, not RF proof."""
import copy
import hashlib
import itertools
import json
import subprocess
import xml.etree.ElementTree as ET
from pathlib import Path
import m5a_r1_verify as old
from m5a_r3_design import preserved, OUT, DEST

def load():
    parts={p['ref']:p for p in json.loads((DEST/'RF2M.electrical.json').read_text())['parts']}
    nets={}
    for net in ET.parse(OUT/'RF2M.net.xml').findall('./nets/net'):
        for node in net.findall('node'):
            nets.setdefault(node.attrib['ref'],{})[node.attrib['pin']]=None if net.attrib['name'].startswith('unconnected-') else net.attrib['name']
    for r,p in parts.items():
        if not r.startswith('#'):assert nets[r]==p['pins'],('CAD/manifest',r,nets.get(r),p['pins'])
    return parts,nets

NEW={
 'Q901':('Philips BF981 Dec1990 p155 SOT103',{'1':'T3_S','2':'T3_D','3':'T3_G2','4':'T3_G1'},'NUMERIC_VERIFIED_FOOTPRINT_OPEN'),
 'Q902':('Central2N4427 R1 4Jun2013p2; PDN01114 EOL2019',{'1':'T4_E','2':'T4_B','3':'T4_C'},'NUMERIC_VERIFIED_SUPPLIER_MANUFACTURER_OPEN'),
 'Q903':('ASI MRF237 RevA1/1; Motorola case79-03 is NOT substituted',{'1':'GND','2':'T5_B','3':'T5_C'},'ASI_NUMERIC_VERIFIED_SUPPLY_AND_LANDING_OPEN'),
 'Q904':('ST TIP127 DS0854 Rev5 May2021p1/TO220 drawing',{'1':'PASS_BASE','2':'VPA','3':'VMOD'},'NUMERIC_VERIFIED_LIVE_COLLECTOR_TAB'),
 'U901':('TI SN74LVC1G125 SCES223U DBV',{'1':'NORMAL_OFF','2':'CLK_NORMAL','3':'GND','4':'CLK72_BUF','5':'V3V3'},'NUMERIC_VERIFIED'),
 'U304':('TI SN74LVC2G08 DCU pin functions; R3 rail timing change',{'1':'CONV_EN','2':'PACK_OK_N','3':'RAIL_RUN','4':'GND','5':'NORMAL_PERMIT','6':'HARD_OK_N','7':'PACK_RUN','8':'V3V3'},'NUMERIC_VERIFIED'),
 'U401':('TI TLV9004 SOIC14; unused channel grounded follower',{'1':'LEVEL_DC','2':'LEVEL_DC','3':'LEVEL_F2','4':'V3V3','5':'AF_F2','6':'AF_DC','7':'AF_DC','8':'UNUSED_OP_OUT','9':'UNUSED_OP_OUT','10':'GND','11':'GND','12':'TRAIN_COMMAND','13':'TRAIN_EMITTER_DC','14':'TRAIN_BASE_DRIVE'},'NUMERIC_VERIFIED'),
 'U802':('TI LM339B SOIC14; formerly driverOV channel safely unused',{'1':'PACK_OK_N','2':'PACK_OK_N','3':'V3V3','4':'UV_REF','5':'VBAT_S','6':'VBAT_S','7':'OV_REF','8':'GND','9':'VREF1V0','10':'VREG_S','11':'REG_OV_REF','12':'GND','13':'HARD_OK_N','14':'HARD_OK_N'},'NUMERIC_VERIFIED'),
 'U203':('Nexperia74HC14 SOIC14 Schmitt inputs; R3 RC to last inverter',{'1':'KEY','2':'KEY_N','3':'SLOT','4':'SLOT_N','5':'PATH_Q','6':'NORMAL_Q','9':'ARM_RC','8':'ARM_DELAY_N','11':'ARM_DELAY_N','10':'ARM_DELAY','13':'NORMAL_RC','12':'NORMAL_OFF','7':'GND','14':'V3V3'},'NUMERIC_VERIFIED_RC_TIMING_UNQUALIFIED'),
}

def audit(parts,nets):
    result=[]
    for r,(source,expected,status) in {**old.AUDIT,**NEW}.items():
        if r not in parts:continue
        assert nets[r]==expected,('manufacturer-specific pins',r,nets[r],expected)
        result.append(dict(ref=r,mpn=parts[r]['mpn'],source=source,pins=expected,status=status,footprint=parts[r]['footprint']))
    return result

def reference(parts,nets):
    expected={
      'C911':('1.2p','LP72_OUT','T3_G1'),'L904':('170n original L4 green','T3_G1','GND'),
      'C913':('18p','T3_G1','GND'),'R909':('33k','T3_G2','GND'),'R910':('33k','VMOD','T3_G2'),
      'C912':('1n','T3_G2','GND'),'R911':('47','TP5_ORIGINAL','T3_D'),
      'R912':('100','T3_S','GND'),'C916':('1n','T3_S','GND'),
      'R914':('100','VMOD','T3_FEED'),'C914':('1n','T3_FEED','GND'),
      'L905':('51n original L5 red; catalog55-70n','T3_FEED','TP5_ORIGINAL'),
      'C915':('15p','TP5_ORIGINAL','T4_B'),'R913':('100','T4_B','GND'),
      'R915':('47','T4_E','GND'),'C918':('1n','T4_E','GND'),
      'L909':('10u original DR2','VMOD','T4_FEED'),'C917':('1n','T4_FEED','GND'),
      'L906':('34n original L6 yellow','T4_FEED','T4_C'),
      'C919':('25p original C19','T4_C','T5_B'),'R916':('100','T5_B','GND'),
      'L911':('VK200 original DR4','VPA','T5_FEED'),'L910':('4.7u original DR3','T5_FEED','T5_C'),
      'C920':('1n','VPA','GND'),'C922':('1n','T5_FEED','GND'),
      'C921':('33p','T5_C','OUT_MID'),'L907':('51n original L7 red; catalog55-70n','OUT_MID','OUT_TRIM'),
      'C923':('39p','OUT_TRIM','GND'),'C924':('45p original C23','OUT_TRIM','GND'),
      'L908':('34n original L8 yellow','OUT_TRIM','NORMAL_RF'),'C925':('33p','NORMAL_RF','GND'),
      'R926':('10k','VMOD','PASS_BASE'),'R924':('2.2k','AF_ATTEN','AF_RC'),
      'C927':('100n','AF_RC','GND'),'R925':('2.2k','AF_RC','AF_COUPLE'),
      'C928':('330n film original C26','AF_COUPLE','PASS_BASE'),
    }
    for r,(value,a,b) in expected.items():
        assert parts[r]['value']==value,(r,'reference value',value,parts[r]['value'])
        assert nets[r]=={'1':a,'2':b},(r,'reference connection',nets[r])
    assert nets['RV902']=={'1':'PASS_BASE','2':'PASS_BASE','3':'VPA'}
    assert all(p['mpn']not in ('PHA-1+','PHA-13HLN+','PD54008L-E','PD55008-E','D45H11') for p in parts.values())
    assert 'U303'not in parts # no separate5V MMIC regulator
    assert not any({'NORMAL_RF','TRAIN_RF'}<=set(p['pins'].values()) for p in parts.values())
    return len(expected)

def physical_switches(nets):
    # Evaluate actual physical gate pins; independent of intended signal names.
    n=nets['U304'];cases=0
    for conv,pack,normal,hard in itertools.product([0,1],repeat=4):
        v={'GND':0,'V3V3':1,'CONV_EN':conv,'PACK_OK_N':pack,'NORMAL_PERMIT':normal,'HARD_OK_N':hard}
        v[n['7']]=v[n['1']]and v[n['2']];v[n['3']]=v[n['5']]and v[n['6']]
        assert v['PACK_RUN']==bool(conv and pack)
        assert v['RAIL_RUN']==bool(normal and hard)
        # U203 pin13/12 inverter physically controls normal source OE.
        assert nets['U203']['13']=='NORMAL_RC' and nets['U203']['12']=='NORMAL_OFF'
        assert nets['R930']=={'1':'NORMAL_PERMIT','2':'NORMAL_RC'}
        assert nets['R932']=={'1':'NORMAL_RC','2':'GND'}
        oe=not normal
        assert nets['U901']['1']=='NORMAL_OFF'
        if not normal:assert oe and not v['RAIL_RUN']
        cases+=1
    return cases

def main():
    parts,nets=load();report=audit(parts,nets);num=reference(parts,nets)
    logic=old.tests(nets);switches=physical_switches(nets);mutations=[]
    for ref,pin,wrong in [('Q903','2','T5_C'),('Q902','1','T4_C'),('Q904','1','VMOD'),('Q901','3','T3_G1'),('U901','1','GND'),('U304','5','CONV_EN'),('U103','10','CLK_TRAIN')]:
        n=copy.deepcopy(nets);n[ref][pin]=wrong
        try:audit(parts,n)
        except AssertionError:mutations.append(ref+':'+pin)
        else:raise AssertionError('Pin mutation escaped')
    for ref,pin,wrong in [('C917','2','T4_C'),('R911','2','T3_G1'),('C924','1','T5_C')]:
        n=copy.deepcopy(nets);n[ref][pin]=wrong
        try:reference(parts,n)
        except AssertionError:mutations.append(ref+':'+pin)
        else:raise AssertionError('Reference topology mutation escaped')
    p=copy.deepcopy(parts);p['R913']['value']='33k'
    try:reference(p,nets)
    except AssertionError:mutations.append('R913:wrong100ohm')
    else:raise AssertionError('Reference value mutation escaped')
    n=copy.deepcopy(nets);n['U205']['10']='PATH_Q'
    try:old.tests(n)
    except AssertionError:mutations.append('normal_permit_wrong_path')
    else:raise AssertionError('Path mutation escaped')
    e=json.loads((OUT/'erc.json').read_text());violations=[v for s in e['sheets']for v in s['violations']]
    assert not [v for v in violations if v['severity']=='error']
    assert all(v['type']=='footprint_filter'for v in violations)
    assert 'footprint_filter'not in {x['key']for x in e['ignored_checks']}
    assert json.loads((OUT/'preserved-baseline.json').read_text())==preserved()
    # Every remaining original training component retains R1 value, pins and footprint.
    r1={p['ref']:p for p in json.loads((DEST/'archive/M5A-R1/RF2M.electrical.json').read_text())['parts']}
    changed_train=[]
    for r,p in parts.items():
        if p['population']not in ('ALL','TRAIN_ONLY') or r.startswith(('#','TP')):continue
        if r not in r1 or any(p[k]!=r1[r][k]for k in ['pins','value','footprint','population']):changed_train.append(r)
    assert changed_train==['R101','U203','U401','R932'],changed_train # new revisionID and unused normal input terminations
    assert parts['R101']['value']=='15k'and parts['R101']['variant_values']=={'BUCK4S':'33.2k','TRAIN_ONLY':'75k'}
    result=dict(status='PASS netlist-derived static checks ONLY; hardware NOT_RUN',revision='M5A-R3',parts_manifest=len(parts),erc_errors=0,erc_open_footprint_warnings=len(violations),logic=logic,physical_enable_truth_rows=switches,original_network_checks=num,mutation_tests=mutations,pin_assertion_count=len(report),training_changed_parts=changed_train,frozen_file_count=len(preserved()),PCB='NOT_CREATED: exact final manufacturer/lot and physical landings unresolved',RF_AM_thermal='NOT_RUN',timing='R1 settling model only; no new timing or analog simulation claimed')
    (OUT/'verification.json').write_text(json.dumps(result,indent=2)+'\n')
    (OUT/'pinout-audit.json').write_text(json.dumps(dict(scope='Manufacturer-specific schematic numeric pins only; physical landing approval separate',devices=report),indent=2)+'\n')
    print('PASS',logic['combinations'],'logic combinations;',len(logic['scenarios']),'state scenarios;',len(mutations),'mutations;',len(report),'pin maps;',len(violations),'OPEN footprint warnings')
if __name__=='__main__':main()
