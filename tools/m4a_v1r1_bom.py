#!/usr/bin/python3
"""Complete per-reference populations and honest historical/index/estimate baskets."""
import csv,math,copy
from m4a_v1r1_common import *
# USD conversions below are explicit planning assumptions, NOT a EUR supplier quote.
OBS={
 'J301':dict(breaks={1:.16*.90,10:.134*.90},kind='ESTIMATE_USD_INDEX_FX0p90',supplier='Mouser',code='306-B2P-VHLFSN',stock='Exact suffix indexed108313 last week; bulk MOQ1/multiple1; actual EUR cart not submitted',url='https://www.mouser.com/en/ProductDetail/JST-Commercial/B2P-VHLFSN?qs=QpmGXVUTftEIUcnoKC896A%3D%3D'),
 'J401':dict(breaks={1:.960,10:.788},kind='INDEXED_EUR_NOT_QUOTE',supplier='DigiKey DE',code='277-1947-ND',stock='Indexed9060 two weeks ago; bulkMOQ1; actual cart not submitted',url='https://www.digikey.de/en/products/detail/phoenix-contact/1727010/348696'),
 'J101':dict(breaks={1:.530,10:.516},kind='INDEXED_EUR_NOT_QUOTE',supplier='DigiKey DE',code='Maker61201621621; distributor SKU OPEN',stock='Indexed7021; cart not submitted; MOQ1',url='https://www.digikey.de/de/products/detail/w%C3%BCrth-elektronik/61201621621/2060591'),
 'F301':dict(breaks={1:1.55,5:1.284,10:1.184},kind='INDEXED_EUR_NOT_QUOTE',supplier='DigiKey BE',code='046701.5NR',stock='Indexed11638; cut MOQ1; no reservation',url='https://www.digikey.be/en/products/detail/littelfuse-inc/046701-5NR/555282'),
 'U401':dict(breaks={1:2.52*.90,10:1.873*.90},kind='ESTIMATE_USD_INDEX_FX0p90',supplier='DigiKey US',code='296-40244-1-ND',stock='Indexed972 cut MOQ1; EU availability/landed cost OPEN; TI direct out of stock',url='https://www.digikey.com/en/products/detail/texas-instruments/LM5134BMF-NOPB/3727251'),
 'Q403':dict(breaks={1:1.23*.90,10:.85*.90},kind='ESTIMATE_USD_INDEX_FX0p90',supplier='ST eStore',code='BD140 / ST only',stock='ST indexedActive/in stock; EU cart OPEN',url='https://estore.st.com/en/bd140-cpn.html'),
 'L411':dict(breaks={1:1.65,5:1.29},kind='ESTIMATE_CORE_PLUS_WIRE_NO_LABOR',supplier='TME/core and enamel wire',code='MicrometalsT60-2 plus20T AWG24, not a complete purchased winding',stock='TME regional stock conflict64/0; core indexedEUR1.40/q1,1.04/q5, tax/cart OPEN; wire allowance0.25',url='https://www.tme.eu/en/details/t60-2/ring-ferrites/micrometals/'),
 'L410':dict(breaks={1:1.65,5:1.29},kind='ESTIMATE_CORE_PLUS_WIRE_NO_LABOR',supplier='TME/core and enamel wire',code='MicrometalsT60-2 plus20T AWG24, not a complete purchased winding',stock='Same asL411; unquoted, hand winding labor separate',url='https://www.tme.eu/en/details/t60-2/ring-ferrites/micrometals/'),
 'J502':dict(breaks={10:.0463*.90},kind='ESTIMATE_USD_INDEX_FX0p90',supplier='LCSC',code='C144394 / B3B-XH-A(LF)(SN)',stock='Indexed151440; MOQ10/multiple10. Mouser0 stock/incomingNov10; no reservation',url='https://lcsc.com/product-detail/Wire-To-Board-Wire-To-Wire-Connector_JST-Sales-America-B3B-XH-A-LF-SN_C144394.html',moq=10,multiple=10)}

def main():
 frozen();a=json.loads((P/(NAME+'.electrical.json')).read_text());parts={x['ref']:x for x in a['parts']if not x['ref'].startswith(('#','TP'))};old=json.loads((R/'docs/M3B_E2_COSTS.json').read_text());batches={};allrows=[]
 for pop,key in [('FULL','Full'),('FOX_ONLY','Fox')]:
  poprows=[];budget={}
  for n in [1,5,10,20]:
   previous=old['scopes'][key]['batches'][str(n)];ledger={};historical=0;unquoted=0;indexed=0;total=0
   for line in previous['lines']:
    refs=[r.strip()for r in line['refs'].split(',')]
    for ref in refs:
     unit=line['allocated_per_board_eur']/len(refs);obs=OBS.get(ref)
     typ='HISTORICAL_OBSERVATION_NOT_REQUOTED'if line['evidence'].startswith('OBSERVED')else'UNQUOTED_ESTIMATE'
     order=line['ordered'];left=line['leftover'];moq=line['moq'];multiple=line['multiple'];src=line['source'];supplier=line['supplier'];code=line['supplier_code'];stock=line['stock']
     if obs:
      moq=obs.get('moq',1);multiple=obs.get('multiple',1);order=math.ceil(max(n,moq)/multiple)*multiple;left=order-n
      v=obs['breaks'][max(k for k in obs['breaks']if k<=order)];unit=v*order/n;typ=obs['kind'];src=obs['url'];supplier=obs['supplier'];code=obs['code'];stock=obs['stock']
     if typ=='INDEXED_EUR_NOT_QUOTE':indexed+=unit
     elif typ.startswith('HISTORICAL'):historical+=unit
     else:unquoted+=unit
     total+=unit;ledger[ref]=dict(allocated_component_eur_per_board=round(unit,6),pricing=typ,ordered_units_for_batch=order,leftover_units_for_batch=left,MOQ=moq,multiple=multiple,supplier=supplier,supplier_code=code,stock_evidence=stock,source=src)
   expected={r for r,p in parts.items()if p['population']in(['BOTH','NORMAL']if pop=='FULL'else['BOTH','FOX'])};assert set(ledger)==expected,(pop,set(ledger)^expected)
   for r,prices in ledger.items():
    p=parts[r];row=dict(variant=pop,batch=n,ref=r,MPN=p['mpn'],value=p['value'],footprint=p['footprint'],group=p['group'],assembly='OFFBOARD_SENSOR'if r=='TH301'else'PCB',**prices);poprows.append(row)
   budget[str(n)]=dict(components_eur_per_board=round(total,3),batch_eur=round(total*n,2),recent_indexed_EUR_eur_per_board=round(indexed,3),historical_observed_unrequoted_eur_per_board=round(historical,3),unquoted_including_FX_estimates_eur_per_board=round(unquoted,3),M4A_V1_historical_component_eur=previous['per_board_eur'],engineering_component_delta_eur=0,repricing_and_realistic_core_material_delta_eur=round(total-previous['per_board_eur'],3))
  batches[pop]=budget;allrows+=poprows
  with(D/('BOM-'+pop+'.csv')).open('w')as f:
   w=csv.DictWriter(f,fieldnames=list(poprows[0]),lineterminator="\n");w.writeheader();w.writerows(poprows)
 populations=[]
 for r,p in parts.items():
  populations.append(dict(ref=r,MPN=p['mpn'],footprint=p['footprint'],FULL='FIT'if p['population']in['BOTH','NORMAL']else'DNP',FOX_ONLY='FIT'if p['population']in['BOTH','FOX']else'DNP',population=p['population'],note=p['note']))
 with(D/'population.csv').open('w')as f:
  w=csv.DictWriter(f,fieldnames=list(populations[0]),lineterminator="\n");w.writeheader();w.writerows(populations)
 assert sum(x['FULL']=='FIT'for x in populations)==196 and sum(x['FOX_ONLY']=='FIT'for x in populations)==115
 boards={str(n):dict(total_bare_board_eur_range=[round(12+180*.0165*n,2),round(25+350*.0165*n,2)],method='Unquoted area/setup planning model, NOT JLCPCB price; setupEUR12-25 +EUR180-350/m2;150x110mm each, standard process. ShippingEUR10-25 separate. Tax/import/payment not included.')for n in [5,10,20]}
 save('costs.json',dict(date=DATE,currency='EUR net planning; supplier VAT treatment/cart must be checked',classification='NO_QUOTE_NO_CAM_ACCEPTANCE',batch_sizes=[1,5,10,20],populations=batches,bare_PCB=boards,USD_conversion='0.90EUR/USD planning assumption +/-10%; not an observed exchange rate or EUR quote',engineering_material_delta='0.00EUR: same MPNs/quantities; only PTH/legend/native manufacturing settings changed. Repricing separated from design delta.',extras=dict(controller='Excluded;M6-L1 separately',battery_charger='Excluded',antenna_coax='Excluded',harness_connectors_crimps='UnquotedEUR3-6/unit allowance, not PCB BOM',IRF610_heatsink_insulator_hardware='UnquotedEUR3-7/FULL allowance, not a guaranteed cooling rating',remote_sensor_attachment='UnquotedEUR0.5-1.5/FULL attachment in addition to TH301 component',winding_labor='Excluded; hand20T+20T and9+9 bifilar as documented',assembly_test_labor='Not priced or invented',PCB_stencil='Optional manual assembly consumable, not a required PCB service')))
 sources=[]
 for ref,obs in OBS.items():sources.append(dict(ref=ref,review_date=DATE,**obs))
 sources+= [dict(ref='Q402',review_date=DATE,url='https://www.digikey.it/de/products/detail/vishay-siliconix/IRF610PBF-BE3/12396470',status='Exact part indexed2718 several weeks old. Mouser exact0stock; priceUSD1.39/.967 nonstock comparator only. Historical FarnellEUR0.622/q10 retained as aged observation, not purchasable-price guarantee.'),
 dict(ref='U311',url='https://www.ti.com/lit/ds/symlink/tl431.pdf',status='Exact TL431AIDBZR remains unquoted. TI DBZ1K2REF3A. Do not substitute other manufacturers/G4 ordering price silently. DBZT cut supply is potential same TI die/package alternative requiring documented procurement check.'),
 dict(ref='T401',url='https://www.rf-microwave.com/de/fair-rite/5943001101/ferrit-ringkern-43/ft-50a-43/',status='FT-50A-43/Fair-Rite5943001101 comparator indexed576,MOQ1,EUR0.430/q1 and0.304/q10. Existing complete windingEUR0.95 remains estimate. Check exact core size/material/AL before procurement equivalence; no RF substitution implemented.'),
 dict(ref='J502 mating',url='https://www.jst.co.uk/downloads/series/eXH_1.pdf',status='XHP-3 housing / SXH-001T-P0.6 contacts for selected manufacturer wire range; compact accessory shorts3to2. Not PCB BOM.'),
 dict(ref='J101 mating',url='https://www.we-online.com/components/products/datasheet/61201621621.pdf',status='Maker recommends61201623021 IDC female counterpart. Ribbon 2.54mm dualrow,1.27mm conductor pitch, pin1-to-pin1 continuity; cable/housing/crimp cost OPEN.'),
 dict(ref='all_other_parts',status='Complete exact MPN population and historical supplier metadata in BOM CSVs. Substantial unquoted material remains. No live stock reservation, cart, order or quotation. Existing source_status fields in native manifest are inherited historical data, not refreshed claims.')]
 save('source-status.json',dict(review_date=DATE,status='DATED_INDEX_AND_MANUFACTURER_EVIDENCE_NOT_QUOTES',sources=sources,missing_manufacturer_lead_tolerances=['J301','J401','J502'],availability='Every stock index must be reconfirmed before authorized purchasing. No supplier contacted. Some source indexes are weeks/months old or regionally inconsistent.',pricing='Current-index Euro comparator is separated from old observations and unquoted/FX/core estimates. No invented quantity breaks: use preceding published break only.'))
 print(json.dumps(batches,indent=2));print('CompleteBOM populations196/115 incl offboardTH301; per-reference all batch sizes; no design-material delta')
if __name__=='__main__':main()
