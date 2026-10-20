"""Read-only native population costing; observations and estimates stay separate."""
import collections
import csv
import math
from m5b_e6_common import *
from m5a_r1_costs import VARIANTS,physical,effective,price


def main():
    guard();rows=[];summary=[]
    for variant,allowed in VARIANTS.items():
        fitted=[p for p in parts().values() if physical(p) and p['population'] in allowed]
        demand=collections.Counter(effective(p,variant)[1] for p in fitted)
        for fleet in [1,5,7,10]:
            classes=collections.defaultdict(float);total=0
            for p in fitted:
                value,mpn=effective(p,variant);needed=demand[mpn]*fleet
                ordered=math.ceil(max(needed,p['moq'])/p['multiple'])*p['multiple']
                allocated=price(p,ordered)*ordered/needed
                kind='historical_supplier_index' if p['evidence'].startswith('OBSERVED') else 'estimate_unquoted'
                classes[kind]+=allocated;total+=allocated
                rows.append(dict(population=variant,fleet=fleet,ref=p['ref'],MPN=mpn,value=value,
                    footprint=p['footprint'],population_tag=p['population'],MPN_fleet_demand=needed,
                    MOQ=p['moq'],multiple=p['multiple'],ordered_MPN_quantity=ordered,
                    allocated_EUR_net_per_board=allocated,classification=kind,evidence=p['evidence'],
                    source=p.get('price_source_url',p['source_url'])))
            # Manufacturing planning allowances, no live supplier quote. Charge
            # full minimum five-board cash against the number actually needed.
            pcb_batches=math.ceil(fleet/5);pcb=[60*pcb_batches/fleet,100*pcb_batches/fleet]
            sk=7.30/1.19;sk100=15.17 if fleet>=10 else 16.48
            # One 100x100 sheet yields >=10 usable 15x44 blanks with scrap
            # allowance. Full MOQ sheet cash charged; leftovers are not free.
            pad_sheet=22.59*math.ceil(fleet/10)/fleet
            old_thermal=[sk+sk100+1.5+1+2+4,sk+sk100+3+2+4+7]
            proposed_thermal=[sk+1+pad_sheet+1+4,sk+2+pad_sheet+3+7]
            if variant=='TRAIN_ONLY':old_thermal=[0,0];proposed_thermal=[0,0];pad_sheet=0
            # Electronics+PCB+cooling+enclosure+consumables; excludes separately
            # itemized controller, pack/BMS, harness, antenna and labor below.
            subtotal=[total+pcb[0]+proposed_thermal[0]+5+1,total+pcb[1]+proposed_thermal[1]+15+3]
            summary.append(dict(population=variant,fleet=fleet,fitted_parts=len(fitted),electrical_EUR_net=total,
                electrical_price_evidence=dict(classes),PCB_used_unit_cash_EUR_net=pcb,
                PCB_purchased=5*pcb_batches,PCB_leftovers=5*pcb_batches-fleet,
                E5_cooling_EUR_net_estimate=old_thermal,E6_concept_cooling_EUR_net_estimate=proposed_thermal,
                insulating_sheet_cash_per_used_unit_EUR_net=pad_sheet,
                proposed_RF_board_cooling_case_consumables_EUR_net=subtotal,
                concept_not_implemented=True))
    with (OUT/'population-costs.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    save('cost-comparison.json',dict(date='2026-10-21',currency='EUR',VAT='Net; Germany19% only for explicit gross observation conversion',
        status='UNQUOTED_PLANNING_COMPARISON_NOT_A_RELEASED_BOM',summary=summary,
        observations=[dict(MPN='SK81 100 SA',gross_EUR=7.30,net_EUR=7.30/1.19,MOQ=1,multiple=1,
            availability='Indexed in stock1-2business days, no reservation',source='https://www.reichelt.com/de/en/shop/product/heat_sink_100_mm_aluminium_2_2_k_w-227984'),
            dict(MPN='SK10075SA',net_EUR_breaks={'1':16.48,'10':15.17},MOQ=1,multiple=1,
            availability='Indexed temporarily unavailable; Nov10forecast, not a promise',source='https://de.rs-online.com/web/p/kuhlkorper/1898088'),
            dict(MPN='KERATHERM86/82 100x100 .25mm',net_EUR=22.59,MOQ=1,multiple=1,
            availability='Indexed available; basket not checked',source='https://cls-computer.de/cls-hardware/kerafol-86-82-w-rmeleitfolie-0-25-mm-6-5-w-mk-l-x-b-100-mm-x-100-mm-pcs5901102')],
        unquoted=dict(FK213SA32_EUR_net=[1.5,3],aluminium_bar_EUR_net=[1,2],
            E5_mica_grease_EUR_net=[2,4],E6_mica_grease_excluding_source_sheet_EUR_net=[1,3],
            E5_hardware_spacers_EUR_net=[4,7],E6_independent_support_hardware_EUR_net=[4,7],
            enclosure_EUR_net=[5,15],consumables_EUR_net=[1,3],shipping_per_order_EUR_net=[10,25],
            labor_E5_minutes=[45,75],labor_E6_concept_minutes=[25,45],labor_rate_illustration_EUR_hour=25,
            labor_E5_EUR=[18.75,31.25],labor_E6_concept_EUR=[10.4167,18.75],
            controller_EUR_net=[15,25],harness_EUR_net=[3,6],antenna_feeder_EUR_net=[8,15],pack_BMS_EUR_net=[15,35]),
        omissions='Instrumented first article RF tuning, Xray, tools, charger, rework, packaging, freight and destination VAT must be costed separately; no complete transmitter120/150EUR claim',
        economic_result='One heatsink removes two coolers and assembly operations; a source insulation sheet has MOQ cash and thermal penalties. Concept saving is neither a completed design nor a quote.'))
    for x in summary:
        print(x['population'],x['fleet'],'electrical',round(x['electrical_EUR_net'],2),'E5cool',list(map(lambda v:round(v,2),x['E5_cooling_EUR_net_estimate'])),'E6concept',list(map(lambda v:round(v,2),x['E6_concept_cooling_EUR_net_estimate'])))


if __name__=='__main__':main()
