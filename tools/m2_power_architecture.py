#!/usr/bin/env python3
"""Reproducible planning arithmetic only; no battery/RF simulation or hardware control."""
import argparse
import csv
import io
import json
import math
from pathlib import Path

import m1_costs
import m2_80m_analysis as hf
from m2_rf_analysis import envelope

ROOT = Path(__file__).resolve().parents[1]
DATE = '2026-10-14'
BATCHES = (6, 10, 20)
PACKS = {'2S1P': (2, 1), '2S2P': (2, 2), '2S3P': (2, 3),
         '2S4P': (2, 4), '4S1P': (4, 1), '4S2P': (4, 2)}
CAPACITIES = (2.45, 3.35, 3.40, 3.50)


def catalog():
    original = {**m1_costs.PARTS, **hf.inputs()['parts']}
    audit = json.loads((ROOT / 'docs/FOXORING_COST_PARTS.json').read_text())['parts']
    for pid, p in audit.items():
        if pid not in original:
            original[pid] = {**p, 'mpn': p['description'], 'package': 'external / OPEN',
                             'retrieved_on': '2026-10-13'}
    original['FABVHF'] = {**original['FABRF'], 'mpn': 'Independent 2m bare PCB fabrication',
                          'note': 'Separate design MOQ5/multiple5; never pooled with the HF artwork.'}

    def new(pid, mpn, prices, supplier='OPEN', code='OPEN', url='', status='ESTIMATE',
            availability='UNQUOTED', package='OPEN', note=''):
        original[pid] = dict(mpn=mpn, supplier=supplier, supplier_part_number=code,
                            source_url=url, price_breaks_eur=prices, moq=1, multiple=1,
                            evidence=status, availability=availability, package=package,
                            retrieved_on=DATE, note=note)

    new('WIDEBUCK', 'TPS54302DDCT', {'1': 1.59, '10': 1.18, '25': 1.08, '100': .955},
        'Mouser', '595-TPS54302DDCT',
        'https://www.mouser.de/ProductDetail/Texas-Instruments/TPS54302DDCT?qs=zEmsApcVOkXGTx6CMk2KtQ%3D%3D',
        'OBSERVED', 'Indexed 7661 (old cache), newer search 4639; live basket OPEN',
        'DDC SOT-23-THIN-6', 'Cut tape MOQ1; factory DDCT reel250, DDCR reel3000. DDCR price .86 at10 but incoming Dec2026; not booked.')
    new('CELL35A', 'Molicel INR18650-M35A', {'1': 3.30, '30': 3.16, '100': 3.00},
        'NKON', 'EAN7417940530154 / product4518',
        'https://www.nkon.nl/en/molicel-inr18650-m35a-3500mah-10a.html',
        'OBSERVED', 'In stock, quantity not shown; 3.35Ah minimum / 3.50Ah typical', '18650 flat top')
    original['CELL25R']['retrieved_on'] = DATE
    original['CELL25R']['price_breaks_eur'] = {'1': 1.94, '10': 1.73, '50': 1.64, '100': 1.56, '200': 1.48}
    new('PCM4', '4S protection comparator LA123070 (not approved)', {'1': 1.91},
        'LaskaKit', 'LA123070', 'https://www.laskakit.cz/en/ochrana-li-ion-baterie-4s-30a/',
        'OBSERVED', '27 indexed; balancing not established; thresholds incompatible with release',
        'external pack board', 'OV4.25+/-0.05V, UV2.54V, OC35A seller claims; exact S-8254 suffix and lot OPEN.')
    new('BAL4', '4S balance completion provision', {'1': 2.00}, note='No verified balancing on LA123070; exact device/threshold/bleed current OPEN.')
    new('PCM4RES', '4S protection replacement reserve', {'1': 2.00}, status='RESERVE', note='Unspent allowance; not a quoted safety ceiling.')
    new('CHARGE4', 'Qualified 16.8V 1A CC-CV charger', {'1': 20.00},
        url='https://www.laskakit.cz/en/nabijecka-li-ion-baterii-do-zasuvky-4s-16-8v-2a/',
        note='Final1A charger OPEN. Comparator2A LA123020C EUR8.07 net, stock1; exceeds M35A1P 1.7A maximum charge current, so not booked.')
    new('TVSNEW', 'SMBJ17A candidate, exact vendor OPEN', {'1': .35}, note='Replacement for SMBJ8.5A, not an extra parallel clamp. Loaded clamp must protect28V operation; charger tolerance, parasitic overshoot and fuse coordination OPEN.')
    new('HVCAPS', '35V input capacitor upgrade delta', {'1': .24}, note='Delta only; original bulk capacitor counts retained; effective capacitance at bias OPEN.')
    new('IDSOCKET', 'Pack identity contact and harness delta', {'1': .25}, note='Per transmitter or pack, not both halves hidden; mechanical design OPEN.')
    new('REFUV', 'Independent voltage reference and UV window support', {'1': .35}, note='Reference accuracy/MPN OPEN; thresholds not released.')
    new('GATECLAMP', 'Power FET VGS clamp', {'1': .10}, note='Exact12V clamp MPN and hot tolerance OPEN.')
    new('PASELECT', 'Bounded feedback power selection/support delta', {'1': .35}, note='Discrete selection, no DAC/MCU; safe minimum default and independent upper trip.')
    new('VHFHELP', 'BD139-class helper/base-drive material', {'1': .20}, note='Exact vendor/SOA OPEN, retained M2 allowance.')
    new('VHFEXTRA', 'VHF modulation/filter/thermal completion', {'1': 3.00}, note='Retained M2 support: not all an extra heatsink, no removal when boost deleted.')
    new('D45', 'D45H11', {'1': 1.71, '10': 1.08}, 'Mouser', '511-D45H11',
        'https://www.mouser.de/ProductDetail/STMicroelectronics/D45H11?qs=ljbEvF4DwOOSkQh0zZU4%2FQ%3D%3D', 'OBSERVED',
        'Prior2026-10-13 observation; new live basket OPEN', 'TO-220', 'Exact-vendor hot DC SOA remains open.')
    new('QUIET5', '5V buck and quiet-filter support excluding IC', {'1': 1.27},
        note='Inductor .60, two capacitors .32, bootstrap .025, divider .05, RF filter .275; no raw4S MCP1703A.')
    new('PACKLARGE', 'Additional pack restraints/sense leads/insulation', {'1': .60},
        note='Per additional cell pair beyond2; tabs separately purchased.')
    new('PACKKEY4', '4S-specific charger keying delta', {'1': .35}, note='No common bare barrel charging socket; final connector MPN OPEN.')
    new('MECHNORM', 'Normal-unit enclosure/support materials', {'1': 8.00}, note='Retained M2 net allowance; compact Fox case separately costed.')
    new('HARNESSNORM', 'Normal-unit wiring/coax/strain relief', {'1': 3.50})
    new('PCBADD', 'Incremental power-area fabrication provision', {'1': .25}, note='No layout/quote; area may fit same outline. Not a fourth PCB.')
    return original


def row(pid, qty, group, note=''):
    return hf.row(pid, qty, group, note)


def controller():
    rows = [row(r['part_id'], r['qty'], 'controller_' + r['cost_group'])
            for r in m1_costs.population(['controller']) if r['part_id'] not in ('BUCK', 'BUCKIND','RAWFET','TVS')]
    rows += [row('WIDEBUCK', 1, 'controller_power'), row('INDUCTOR', 1, 'controller_power'),
             row('RES', 2, 'controller_power'), row('C100N', 1, 'controller_power'),
             row('ISOFET', 2, 'controller_protection'),
             row('TVSNEW', 1, 'controller_protection'), row('HVCAPS', 1, 'controller_protection'),
             row('IDSOCKET', 1, 'pack_identity'), row('CMP', 1, 'pack_identity'),
             row('REFUV', 1, 'pack_identity'), row('RES', 6, 'pack_identity'),
             row('GATECLAMP', 2, 'controller_protection')]
    return rows


def hf_board(arch, fox=False):
    if fox:
        return hf.proposed(fox=True)
    if arch == '2S economy':
        rows = hf.proposed()
    elif arch == '2S high':
        rows = hf.proposed(high=True)
    else:
        rows = [r for r in hf.proposed() if r['part_id'] != 'BUCK']
        rows += [row('WIDEBUCK', 1, 'power_conversion'), row('PASELECT', 1, 'power_conversion'),
                 row('THERMALADD', 1, 'thermal'), row('HVCAPS', 1, 'protection'),
                 row('GATECLAMP', 2, 'protection')]
    return rows


def vhf_board(arch):
    rows = [row(r['part_id'], r['qty'], 'vhf_' + r['cost_group'])
            for r in m1_costs.population(['2m']) if r['part_id'] not in ('VBOOST', 'MODULATOR', 'LDO5')]
    # 4S-safe5V driver feed: own buck + quiet RF filter. Include it on both comparators.
    rows += [row('D45', 1, 'vhf_AM'), row('VHFHELP', 1, 'vhf_AM'),
             row('VHFEXTRA', 1, 'vhf_thermal_and_control'),
             row('WIDEBUCK', 1, 'vhf_driver_power'), row('QUIET5', 1, 'vhf_driver_power')]
    if arch == '2S boost':
        rows += [row('BOOST', 1, 'vhf_PA_supply')]
    elif arch == '4S buck':
        rows += [row('WIDEBUCK', 1, 'vhf_PA_supply'), row('PASELECT', 1, 'vhf_PA_supply'),
                 row('HVCAPS', 1, 'vhf_protection'), row('GATECLAMP', 2, 'vhf_protection')]
    else:
        # Only raw supply feeding the modulator, never an unbounded PA drain.
        rows = [r for r in rows if r['part_id'] != 'INDUCTOR']
        rows += [row('THERMALADD', 2, 'vhf_thermal_and_control'), row('HVCAPS', 1, 'vhf_protection'),
                 row('GATECLAMP', 2, 'vhf_protection')]
    return rows


def pack_rows(pack, cell):
    s, p = PACKS[pack]
    cells = s*p
    rows = [row(cell, cells, 'cells'), row('CELLTABS', cells, 'pack_tabs'),
            row('PACKFUSE', 1, 'pack_protection'), row('PACKPAPER', 1, 'pack_mechanics'),
            row('PACKSHRINK', 1, 'pack_mechanics'), row('PACKREST', 1, 'pack_mechanics'),
            row('PACKLEADS', 1, 'pack_wiring'), row('POWERPLUG', 1, 'pack_connector'),
            row('IDSOCKET', 1, 'pack_connector'), row('RES', 1, 'pack_identity'),
            row('PACKLARGE', (cells-2)//2, 'pack_mechanics')]
    if s == 2:
        rows += [row('PACKPCM', 1, 'pack_protection'), row('PCMRESERVE', 1, 'reserve')]
    else:
        rows += [row('PCM4', 1, 'pack_protection'), row('BAL4', 1, 'pack_balancing'),
                 row('PCM4RES', 1, 'reserve'), row('PACKKEY4', 1, 'pack_connector')]
    return [r for r in rows if r['qty'] > 0]


def cost_data(parts):
    variants = {'Controller 2S/4S': controller(),
                'HF 2S economy': hf_board('2S economy'), 'HF 2S high': hf_board('2S high'),
                'HF 4S buck': hf_board('4S buck'), 'Fox reduced HF': hf_board('', fox=True),
                'VHF 2S boost': vhf_board('2S boost'), 'VHF 4S buck': vhf_board('4S buck'),
                'VHF 4S direct modulator': vhf_board('4S direct')}
    variants['HF 4S 3W thermal population'] = [r for r in hf_board('4S buck') if r['part_id'] != 'THERMALADD']
    for name in PACKS:
        for cell in ('CELL25R', 'CELL35A'):
            variants[f'{name} {cell} pack'] = pack_rows(name, cell)
    reports = {name: {str(n): hf.basket(rows, n, parts) for n in BATCHES} for name, rows in variants.items()}
    configs = [
        ('Fox 2S1P 25R', 'fox', '', '2S1P', 'CELL25R'),
        ('HF economy 2S2P 25R', 'hf', '2S economy', '2S2P', 'CELL25R'),
        ('HF high 2S2P 25R', 'hf', '2S high', '2S2P', 'CELL25R'),
        ('HF high 4S1P 25R', 'hf', '4S buck', '4S1P', 'CELL25R'),
        ('HF 5W 2S2P M35A', 'hf', '2S high', '2S2P', 'CELL35A'),
        ('HF 5W 4S1P M35A', 'hf', '4S buck', '4S1P', 'CELL35A'),
        ('VHF 2S2P M35A', 'vhf', '2S boost', '2S2P', 'CELL35A'),
        ('VHF 2S3P 25R', 'vhf', '2S boost', '2S3P', 'CELL25R'),
        ('VHF 2S3P M35A', 'vhf', '2S boost', '2S3P', 'CELL35A'),
        ('VHF 2S4P 25R', 'vhf', '2S boost', '2S4P', 'CELL25R'),
        ('VHF 4S1P M35A', 'vhf', '4S buck', '4S1P', 'CELL35A'),
        ('VHF 4S2P 25R', 'vhf', '4S buck', '4S2P', 'CELL25R'),
        ('VHF direct 4S2P 25R', 'vhf', '4S direct', '4S2P', 'CELL25R'),
        ('Universal 2S4P 25R', 'dual', '2S', '2S4P', 'CELL25R'),
        ('Universal 4S2P 25R', 'dual', '4S', '4S2P', 'CELL25R'),
        ('Universal 4S2P M35A', 'dual', '4S', '4S2P', 'CELL35A'),
    ]
    systems = []
    for name, mode, arch, pack, cell in configs:
        rows = controller()
        rows += (hf_board('', fox=True) if mode == 'fox' else
                 hf_board(arch) if mode == 'hf' else vhf_board(arch) if mode == 'vhf' else
                 hf_board('4S buck' if arch == '4S' else '2S high') + vhf_board('4S buck' if arch == '4S' else '2S boost'))
        boards = 3 if mode == 'dual' else 2
        rf_count = boards-1
        rows += pack_rows(pack, cell)
        rows += [row('FABCTRL', 1, 'PCB_fabrication')]
        rows += [row('FABRF' if mode != 'vhf' else 'FABVHF', 1, 'PCB_fabrication')]
        if mode == 'dual':
            rows += [row('FABVHF', 1, 'PCB_fabrication')]
        rows += [
                 row('PCBADD', boards, 'PCB_fabrication'), row('POWERPLUG', 1+rf_count*2, 'transmitter_connectors'),
                 row('LOWPORT', rf_count, 'RF_connectors'), row('CONSUMABLE', 1, 'assembly_material'), row('LABEL', 1, 'assembly_material')]
        if mode == 'fox':
            rows += [row(r['part_id'], r['qty'], 'compact_antenna') for r in m1_costs.population(['compact80'])]
            rows += [row(pid, 1, 'mechanics_or_wiring') for pid in
                     ('SHELL', 'BOARDMOUNT', 'GROMMETS', 'CASESEAL', 'POWERWIRE', 'LOGICWIRE', 'RFWIRE', 'HARNESSREST')]
        else:
            rows += [row('MECHNORM', 1, 'enclosure'), row('HARNESSNORM', 1, 'wiring'),
                     row('NORMALPORT', rf_count, 'RF_connectors')]
            if mode in ('hf', 'dual'):
                rows += [row(r['part_id'], r['qty'], 'long_antenna') for r in m1_costs.population(['long80'])]
                rows += [row(r['part_id'], r['qty'], 'compact_antenna') for r in m1_costs.population(['compact80'])]
                rows += [row('HFSUPPORT', 1, 'antenna_support')]
            if mode in ('vhf', 'dual'):
                rows += [row('VHFANT', 1, 'VHF_antenna'), row('VHFSUPPORT', 1, 'antenna_support'), row('TRAINANT', 1, 'training_antenna')]
        for n in BATCHES:
            material = hf.basket(rows, n, parts)
            shared_rows = [row('CHARGE4' if pack.startswith('4') else 'CHARGER', math.ceil(n/10), 'shared_charging'),
                           row('CHARGEADAPTER', math.ceil(n/10), 'shared_charging'), row('PROVISION', 1, 'shared_provisioning')]
            # Shared quantities are per fleet, not per transmitter.
            shared = hf.basket(shared_rows, 1, parts)
            allocated = float(shared['batch_eur'])/n + 60/n
            systems.append(dict(name=name, batch=n, pack=pack, cell=cell, material=material,
                                fleet_shared=shared, freight_batch_eur=60,
                                fleet_per_unit_eur=hf.money(float(material['per_unit_eur'])+allocated)))
    return dict(variants=reports, systems=systems)


def usable(pack, capacity, extra_window=1, temp=.90, age=.80):
    s, p = PACKS[pack]
    # M35A manufacturer energy is slightly below nominal-voltage x capacity.
    # Retain historical3.40Ah reference; use specified11.9/12.5Wh for actual M35A cases.
    cell_wh = 11.9 if capacity == 3.35 else 12.5 if capacity == 3.50 else 3.6*capacity
    return s*p*cell_wh*age*.90*temp*extra_window


def hf_load(power, arch, duty=.2, stress=False):
    # PA efficiency includes shaping/filter but excludes explicit gate driver/source.
    eta = .50 if power <= 1 else .55 if power <= 1.5 else .60
    driver = .220 if power <= 1.5 else .30 if power <= 3 else .400
    conv = .90 if arch in ('2S economy', '4S buck') else .85*.90
    if stress:
        eta, conv = .40, .85 if arch != '2S high' else .75
    common = (.127 if arch == '4S buck' else .120)+.020
    gate_conv = conv if arch != '2S high' else .85
    active = power/(eta*conv)+driver/gate_conv+.025*3.3/.90
    return dict(mean_w=common+duty*active, active_extra_w=active, idle_w=common,
                eta_PA=eta, eta_conversion=conv, driver_w=driver, duty=duty, window=1)


def vhf_load(erp, arch, duty=.2, stress=False, low_bias=False, lower_crest=False):
    full = erp >= .75
    # Fixed bias and overhead retained even at low RF power: no free savings.
    center = 6.667 if full else 5.0 if erp >= .5 else 4.0
    rail = 13.5 if full else 10.5 if erp >= .5 else 9.0
    window = .65 if arch != '2S boost' and full else 1
    if lower_crest and full:
        center, rail, window = 6.0, 12.3, .85
    eta = .45 if full else .40 if erp >= .5 else .35
    iq, overhead = .15, 1.55
    if stress:
        eta = .35 if full else .25
    if low_bias:
        iq, overhead = .05, .85
    conv = .88 if arch == '2S boost' else .92 if arch == '4S buck' else 1
    if arch == '4S direct':
        rail = 14.4  # modeling point only; see endpoint rows, no invented SOC curve.
    e = envelope(erp=erp, efficiency=eta, iq=iq, boost=rail, center=center)
    common = (.120 if arch == '2S boost' else .127)+.020
    active = e['boost_mean_output_w']/conv+overhead
    return dict(mean_w=common+duty*active, active_extra_w=active, idle_w=common,
                erp_w=erp, carrier_connector_w=e['carrier_connector_w'], pep_connector_w=e['carrier_connector_w']*3.24,
                eta_dynamic=eta, eta_conversion=conv, iq_a=iq, overhead_w=overhead,
                center_v=center, upstream_v=rail, crest_v=center*1.8, duty=duty, window=window,
                pass_mean_w=e['pass_mean_w'], pass_peak_w=e['pass_peak_w'], crest_current_a=e['current_peak_a'])


def power_data():
    profiles = []
    for arch in ('2S economy', '2S high', '4S buck'):
        for watts in (1.0, 1.2, 1.5, 2, 3, 5):
            if arch == '2S economy' and watts > 1.2:
                continue
            profiles.append(dict(name=f'HF {watts:g}W {arch}', kind='HF', arch=arch, output_w=watts, **hf_load(watts,arch)))
        for watts in (.3, .5, .85, 1.0):
            profiles.append(dict(name=f'Sprint {watts:g}W {arch}', kind='Sprint', arch=arch, output_w=watts, **hf_load(watts,arch)))
    profiles.append(dict(name='Fox 10mW 2S', kind='Fox', arch='2S', output_w=.010, mean_w=.350, idle_w=.140, duty=1, window=1))
    for arch in ('2S boost', '4S buck', '4S direct'):
        for erp in (.25, .30, .50, .75, 1.0):
            profiles.append(dict(name=f'VHF {erp:g}W ERP {arch}', kind='VHF', arch=arch, **vhf_load(erp,arch)))
    for arch in ('2S high','4S buck'):
        for watts in (1.0,1.2,3,5):
            profiles.append(dict(name=f'HF beacon {watts:g}W {arch}', kind='HF beacon', arch=arch, output_w=watts, **hf_load(watts,arch,duty=1)))
    for arch in ('2S economy','4S buck'):
        for watts in (.3,.5,.85,1.0):
            profiles.append(dict(name=f'Sprint beacon {watts:g}W {arch}', kind='Sprint beacon', arch=arch,
                                 output_w=watts, **hf_load(watts,arch,duty=1)))
    for arch in ('2S boost','4S buck'):
        for erp in (.25,.3,.5,1):
            profiles.append(dict(name=f'VHF beacon {erp:g}W ERP {arch}', kind='VHF beacon', arch=arch, **vhf_load(erp,arch,duty=1)))
        h=hf_load(5,'2S high' if arch=='2S boost' else '4S buck')
        v=vhf_load(1,arch)
        # Both boards' standby included once, controller common once.
        common=(.120 if arch=='2S boost' else .127)+.030
        profiles.append(dict(name=f'Dual full 5W HF + 1W ERP {arch}', kind='dual', arch=arch,
                             mean_w=common+.2*(h['active_extra_w']+v['active_extra_w']),
                             idle_w=common,duty=.2,window=v['window']))
        h=hf_load(1.2,'2S economy' if arch=='2S boost' else '4S buck')
        v=vhf_load(.30,arch)
        profiles.append(dict(name=f'Dual reduced 1.2W HF + .30W ERP {arch}',kind='dual',arch=arch,
                             mean_w=common+.2*(h['active_extra_w']+v['active_extra_w']),
                             idle_w=common,duty=.2,window=1))
    for r in profiles:
        r['wh_12h'],r['wh_24h']=r['mean_w']*12,r['mean_w']*24
        compatible=[p for p in PACKS if (p.startswith('4') if r['arch'].startswith('4') else p.startswith('2'))]
        r['runtimes']={str(c): {p:usable(p,c,r['window'])/r['mean_w'] for p in compatible} for c in CAPACITIES}
        r['minimum_pack']={str(c):{str(hours):next((p for p in compatible if r['runtimes'][str(c)][p]>=hours),None)
                                           for hours in (12,24)} for c in CAPACITIES}
    sensitivity=[]
    for label,load,pack,cap in [
        ('HF3 4S nominal',hf_load(3,'4S buck'),'4S1P',2.45),
        ('HF3 4S poor PA/converter',hf_load(3,'4S buck',stress=True),'4S1P',2.45),
        ('HF5 4S nominal',hf_load(5,'4S buck'),'4S1P',3.35),
        ('HF5 4S poor PA/converter',hf_load(5,'4S buck',stress=True),'4S1P',3.35),
        ('VHF full 4S nominal',vhf_load(1,'4S buck'),'4S2P',2.45),
        ('VHF full 4S poor PA',vhf_load(1,'4S buck',stress=True),'4S2P',2.45),
        ('VHF reduced fixed bias',vhf_load(.3,'4S buck'),'4S1P',3.35),
        ('VHF reduced optimistic lower bias',vhf_load(.3,'4S buck',low_bias=True),'4S1P',3.35),
        ('VHF full lower crest, UNQUALIFIED',vhf_load(1,'4S buck',lower_crest=True),'4S1P',3.35),
        ('Fox retained audit allowance',dict(mean_w=.35,window=1),'2S1P',2.45)]:
        for extra,name in ((0,'absent'),(.006,'10% RX'),(.045,'continuous RX'),(.180,'poor controller idle')):
            power=load['mean_w']+extra
            sensitivity.append(dict(case=label,lora_or_stress=name,pack=pack,cell_ah=cap,
                                    mean_w=power,window=load['window'],runtime_h=usable(pack,cap,load['window'])/power))
    thermal=[]
    for erp,center in ((1,6.667),(.3,4.0)):
        for vin in (12,13.5,14.4,16.8):
            eta=.45 if erp==1 else .35
            e=envelope(erp=erp,center=center,boost=vin,efficiency=eta)
            thermal.append(dict(erp_w=erp,vin_v=vin,center_v=center,headroom_v=vin-center*1.8,
                                pass_mean_w=e['pass_mean_w'],pass_peak_w=e['pass_peak_w'],
                                pass_no_tone_w=envelope(erp=erp,center=center,boost=vin,modulation=0,efficiency=eta)['pass_mean_w'],
                                current_peak_a=e['current_peak_a']))
    peak={}
    for arch,vmin in (('2S',6),('4S',12)):
        h=hf_load(5,'2S high' if arch=='2S' else '4S buck')
        v=vhf_load(1,'2S boost' if arch=='2S' else '4S buck',stress=True)
        source=v['upstream_v']*v['crest_current_a']/v['eta_conversion']+1.55
        peak[arch]=dict(HF5_A=1.25*(h['active_extra_w']+.147+.44)/vmin,
                        VHF1_A=1.25*(source+.147+.44)/vmin,
                        dual_A=1.25*(h['active_extra_w']+source+.157+.44)/vmin)
    environment={name:{str(c):{p:usable(p,c,temp=temp,age=age) for p in PACKS} for c in CAPACITIES}
                 for name,temp,age in [('nominal reserve',.9,.8),('cold sensitivity',.6,.8),
                                       ('aging sensitivity',.9,.6),('cold and aging',.6,.6)]}
    return dict(profiles=profiles,sensitivity=sensitivity,thermal=thermal,peak_current=peak,
                environment_energy=environment,
                pack_energies={str(c):{p:usable(p,c) for p in PACKS} for c in CAPACITIES},
                full_VHF_window_sweep={str(w):{p:usable(p,3.35,w)/vhf_load(1,'4S buck')['mean_w']
                                               for p in ('4S1P','4S2P')} for w in (.45,.55,.65,.75,.85)})


def output_tables(data):
    out=['# Reproducible power and material tables','',f'Date: {DATE}. **MODELED / ESTIMATED, NOT MEASURED.**',
         '', 'Generated by `python3 tools/m2_power_architecture.py --write`. Read the five power-review documents for qualifications.',
         '', '## Profiles and minimum modeled packs','',
         '| Profile | Mean W | 12h Wh | 24h Wh | 2.45Ah minimum 12 / 24h | 3.35Ah minimum 12 / 24h | Energy window |',
         '| --- | ---: | ---: | ---: | --- | --- | ---: |']
    for r in data['power']['profiles']:
        packs=[' / '.join(r['minimum_pack'][str(c)][str(h)] or 'NONE' for h in (12,24)) for c in (2.45,3.35)]
        out.append(f"| {r['name']} | {r['mean_w']:.3f} | {r['wh_12h']:.2f} | {r['wh_24h']:.2f} | {packs[0]} | {packs[1]} | {r['window']:.2f} |")
    out += ['', '## Complete candidate material and shared fleet allocations','',
            '| Configuration | Batch | Unit material EUR | Fleet cash EUR/unit | Observed material EUR | Estimates/reserves EUR |',
            '| --- | ---: | ---: | ---: | ---: | ---: |']
    for r in data['cost']['systems']:
        m=r['material']
        out.append(f"| {r['name']} | {r['batch']} | {m['per_unit_eur']} | {r['fleet_per_unit_eur']} | {m['observed_eur']} | {m['estimated_eur']} |")
    out += ['', '## Thermal calculations (same assumed PA conversion component)','',
            '| ERP W | Upstream V | Center V | Crest headroom V | Tone pass mean / peak W | No-tone pass W |',
            '| ---: | ---: | ---: | ---: | --- | ---: |']
    for r in data['power']['thermal']:
        out.append(f"| {r['erp_w']:.2f} | {r['vin_v']:.1f} | {r['center_v']:.3f} | {r['headroom_v']:.3f} | {r['pass_mean_w']:.2f} / {r['pass_peak_w']:.2f} | {r['pass_no_tone_w']:.2f} |")
    out += ['', '## Sensitivity','', '| Case | Added state | Pack | Cell Ah | W | Runtime h |', '| --- | --- | --- | ---: | ---: | ---: |']
    for r in data['power']['sensitivity']:
        out.append(f"| {r['case']} | {r['lora_or_stress']} | {r['pack']} | {r['cell_ah']} | {r['mean_w']:.3f} | {r['runtime_h']:.1f} |")
    return '\n'.join(out)+'\n'


def cost_csv(data, parts):
    stream=io.StringIO()
    fields=['scope','batch','group','part_id','mpn','supplier','supplier_part_number','package',
            'qty_per_unit','needed','ordered','leftover','price_break','unit_eur','line_per_unit_eur',
            'evidence','availability','moq','multiple','retrieved_on','source_url','note']
    w=csv.DictWriter(stream,fieldnames=fields,lineterminator='\n');w.writeheader()
    for name, batches in data['cost']['variants'].items():
        for n, b in batches.items():
            for r in b['lines']:
                p=parts[r['part_id']]
                w.writerow({k:v for k,v in {**r,**p,'scope':name,'batch':n,'qty_per_unit':r['qty']}.items() if k in fields})
    for system in data['cost']['systems']:
        for r in system['material']['lines']:
            p=parts[r['part_id']]
            w.writerow({k:v for k,v in {**r,**p,'scope':system['name'],'batch':system['batch'],'qty_per_unit':r['qty']}.items() if k in fields})
    return stream.getvalue()


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');ap.add_argument('--check',action='store_true');args=ap.parse_args()
    parts=catalog()
    # Additional system allowances preserve existing M2 scope.
    for pid,price,description in [('NORMALPORT',.70,'Normal RF socket'),('HFSUPPORT',3,'HF support/line'),
                                  ('VHFANT',15,'VHF antenna/feed/balun'),('VHFSUPPORT',8,'VHF 2-3m support'),('TRAINANT',3,'Training antenna')]:
        parts[pid]=dict(mpn=description+' exact MPN OPEN',supplier='OPEN',supplier_part_number='OPEN',package='external',
                        price_breaks_eur={'1':price},moq=1,multiple=1,evidence='ESTIMATE',availability='UNQUOTED',
                        source_url='',retrieved_on='2026-10-13',note='Retained M2 net material allowance.')
    # Existing cost helper treats reserves separately; normalize here solely for its uncertainty accounting.
    reserve_ids=[k for k,v in parts.items() if v['evidence']=='RESERVE']
    for pid in reserve_ids:
        parts[pid]['evidence']='ESTIMATE';parts[pid]['note']='UNSPENT RESERVE. '+parts[pid]['note']
    data=dict(date=DATE,classification='PLANNING CALCULATIONS AND CANDIDATE COSTS; NOT MEASURED OR SIMULATED',
              inputs=dict(age=.80,temperature=.90,discharge_window=.90,full_VHF_extra_window=.65,
                          VHF_extra_window_unverified=True,LoRa_RX10_extra_W=.006,LoRa_RX_extra_W=.045,
                          LoRa_TX_burst_W=.44,controller_2S_W=.120,controller_4S_W=.127,RF_idle_W=.020),
              reserve_part_ids=reserve_ids,power=power_data(),cost=cost_data(parts))
    files={'docs/M2_POWER_ARCHITECTURE_INPUTS.json':json.dumps(dict(date=DATE,parts=parts),indent=2)+'\n',
           'docs/M2_POWER_ARCHITECTURE_RESULTS.json':json.dumps(data,indent=2)+'\n',
           'docs/M2_POWER_ARCHITECTURE_TABLES.md':output_tables(data),
           'docs/M2_POWER_ARCHITECTURE_BOM.csv':cost_csv(data,parts)}
    if args.write:
        for name,body in files.items():(ROOT/name).write_text(body)
    if args.check:
        for name,body in files.items():
            assert (ROOT/name).read_text()==body, f'Stale generated file: {name}'
        assert abs(usable('4S1P',2.45)-usable('2S2P',2.45))<1e-12
        assert abs(usable('4S2P',3.35)-usable('2S4P',3.35))<1e-12
        assert abs(usable('4S1P',3.35)-4*11.9*.648)<1e-12
        for r in data['power']['profiles']:
            assert abs(r['wh_24h']-2*r['wh_12h'])<1e-10
        assert vhf_load(1,'4S buck')['crest_v']+1.5>12
        assert vhf_load(.3,'4S buck')['mean_w']>vhf_load(.3,'4S buck',low_bias=True)['mean_w']
        for variant in data['cost']['variants'].values():
            for b in variant.values():
                assert abs(sum(float(r['line_per_unit_eur']) for r in b['lines'])-float(b['per_unit_eur']))<.011
        required=('M2_BATTERY_ARCHITECTURE.md','M2_POWER_MODE_COMPARISON.md',
                  'M2_BATTERY_COST_COMPARISON.md','M2_ENDURANCE_REWORK.md','M2_POWER_ARCHITECTURE_DECISION.md')
        for name in required:
            assert DATE in (ROOT/'docs'/name).read_text(), f'Missing review date: {name}'
        cost_text=(ROOT/'docs/M2_BATTERY_COST_COMPARISON.md').read_text().replace(' ','')
        for name,batches in data['cost']['variants'].items():
            values='/'.join(batches[str(n)]['per_unit_eur'] for n in BATCHES)
            assert values in cost_text, f'Board/pack summary differs: {name}: {values}'
        published=('Fox 2S1P 25R','HF economy 2S2P 25R','HF high 2S2P 25R','HF high 4S1P 25R',
                   'HF 5W 2S2P M35A','HF 5W 4S1P M35A','VHF 2S3P 25R','VHF 2S4P 25R',
                   'VHF 4S2P 25R','Universal 2S4P 25R','Universal 4S2P 25R')
        for name in published:
            values='/'.join(r['material']['per_unit_eur'] for r in data['cost']['systems'] if r['name']==name)
            assert values in cost_text, f'Complete-system summary differs: {name}: {values}'
        assert 'Proposed amendment' in (ROOT/'docs/decisions/ADR-0011-dual-voltage-power-and-endurance.md').read_text()
        print(f'PASS: {len(data["power"]["profiles"])} profiles, {len(data["cost"]["systems"])} fleet baskets; equal-energy and AM-headroom checks. Hardware gates NOT RUN.')
    if not args.write and not args.check:print(json.dumps(data['power']['peak_current'],indent=2))


if __name__=='__main__':main()
