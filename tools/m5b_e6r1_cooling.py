"""Exactly three commercial thermal structures and same-point sensitivities."""
import itertools
from m5b_e6r1_common import *
from m5b_e6r1_thermal import waveform,Cycle,word_period
from m5b_e6r1_power import point
from m5b_e6_thermal import Network

STRUCTURES=[
 dict(name='SK81_100',part='Fischer SK81 100 SA',dimensions_mm=[100,100,15],mass_g=214.,
      total_assembly_mass_g_estimate=[245,270],catalogue_upright_K_W=2.2,orientation_sensitivity_K_W=[2.2,4.,5.5,8.,12.],
      heatsink_net_EUR_index=7.30/1.19,cooler_material_EUR_net_at7=[15.36,21.36],
      source='https://www.reichelt.com/de/en/shop/product/heat_sink_100_mm_aluminium_2_2_k_w-227984'),
 dict(name='SK81_75',part='Fischer SK81 75 SA',dimensions_mm=[100,75,15],mass_g=214.*.75,
      total_assembly_mass_g_estimate=[192,217],catalogue_upright_K_W=2.5,orientation_sensitivity_K_W=[2.5,4.54545,6.25,9.0909,13.636],
      heatsink_net_EUR_index=5.55/1.19,cooler_material_EUR_net_at7=[13.89,19.89],
      source='https://www.reichelt.com/de/en/shop/product/heat_sink_75_mm_aluminum_2_5_k_w_-227987',
      mass_basis='Extrusion length-scaled estimate, not weighed or supplier-certified'),
 dict(name='flat_6060',part='Commercial EN AW6060 100x4 flat stock,100mm cut',dimensions_mm=[100,100,4],mass_g=111.2,
      total_assembly_mass_g_estimate=[142,167],catalogue_upright_K_W=None,orientation_sensitivity_K_W=[8.,12.,20.],
      heatsink_net_EUR_estimate=[2,5],cooler_material_EUR_net_at7=[11.23,20.23],
      source='https://www.dold-mechatronik.de/Flachstange-100x4mm-Aluminium-EN-AW-6060-T66-AlMgSi05-1112kg-m-Zuschnitt-20-6000mm',
      thermal_basis='BareAl0.02m2 bothfaces,h~6W/m2K plus low-emissivity radiation gives~8K/W;12/20restricted/enclosed sensitivities, not a commercial rating')]

def main():
    guard();rows=[]
    for structure in STRUCTURES:
        for r,erp in itertools.product(structure['orientation_sensitivity_K_W'],[.25,.5,1.]):
            for a in ['A','B','C']:
                period=word_period('MO',8)
                seq,loads,energy=waveform('MO',8,period,period,'BUCK4S',erp,a,periodic_word=True)
                net=Network(sink_R=r,mass_g=structure['mass_g'])
                result,_,_=Cycle(net,loads).run(seq)
                rows.append(dict(structure=structure['name'],sink_K_W=r,ERP_W=erp,architecture=a,**result))
        structure['thermal_capacity_J_K']=structure['mass_g']*.9
    electrical=[]
    for pop,mode,eta,beta,scale in itertools.product(['BUCK4S','BOOST2S'],['Classic','Sprint','MO'],[.4,.5],[20.,60.],[1.,1.03]):
        slot,period=(60,300) if mode=='Classic' else (12,60) if mode=='Sprint' else (word_period('MO',8),word_period('MO',8))
        for a in ['A','B','C']:
            seq,loads,energy=waveform('MO' if mode=='MO' else 'MO5',8,slot,period,pop,1.,a,eta=eta,beta=beta,supply_scale=scale,periodic_word=(mode=='MO'))
            result,_,_=Cycle(Network(),loads).run(seq)
            electrical.append(dict(population=pop,mode=mode,eta_carrier=eta,pass_beta=beta,supply_scale=scale,architecture=a,
                energy_J=energy,**result))
    cw=[]
    for pop,mode,a in itertools.product(['BUCK4S','BOOST2S'],['Classic','Sprint','MO'],['A','B','C']):
        slot,period=(60,300) if mode=='Classic' else (12,60) if mode=='Sprint' else (word_period('MO DD1SB',12),word_period('MO DD1SB',12))
        seq,loads,energy=waveform('MO DD1SB' if mode=='MO' else 'MO5 DD1SB',12,slot,period,pop,1.,a,periodic_word=(mode=='MO'))
        result,_,_=Cycle(Network(),loads).run(seq)
        cw.append(dict(population=pop,mode=mode,architecture=a,identifier='MO DD1SB' if mode=='MO' else 'MO5 DD1SB',energy_J=energy,**result))
    outdoor=[]
    for r,solar,tau in itertools.product([4.,5.5,8.,12.],[0.,10.],[1.,5.,15.]):
        period=word_period('MO',8)
        seq,loads,energy=waveform('MO',8,period,period,'BUCK4S',1.,'C',periodic_word=True)
        # Solar is an external thermal input, never fake converter consumption
        # and never a mutation of cached electrical point dictionaries.
        result,_,_=Cycle(Network(sink_R=r,sensor_tau=tau),loads,extra_plate_W=solar).run(seq)
        outdoor.append(dict(sink_K_W=r,solar_plate_W=solar,pass_sensor_tau_s=tau,**result))
    save('cooling-comparison.json',dict(structures=STRUCTURES,rows=rows,selection='Retain SK81_100 as comparator; do notdownsize while fault/interface envelope is open',
        mounting='All3devices one supportedplane. Stock15x44x6mm bar with.25mmsourceTIM and.05mminterface yieldsZ~-7.90mm; proposed only, no thermal credit versus E6bar6.2mm used in simulation',
        insulation='Q401VPA/Q402MOD_SINK remain separately insulated withmica/bushhardware; sourcebar ground bondcontrolled; no soldermask/anodizinginsulationcredit',physical='NOT_RUN'))
    save('operating-sensitivities.json',dict(electrical=electrical,CW_identification=cw,outdoor=outdoor,
        interpretation='Same E6boundary acrossA/B/C. No claim all adverse cases pass. Beacon must retain1Wcapability; inadequate thermal installation is a HOLD, not permission to silently reducepower.',physical='NOT_RUN'))
    # Budget includes new keying/protection components and installation labor.
    new=dict(TLV7034PWR_EUR_net=[.7,1.5],SN74LVC2G00DCUR=[.12,.3],SN74LVC2G32DCUR=[.12,.3],SN74LVC1G04DBVR=[.06,.18],
        Q970_2N7002=[.03,.08],NCP15XH103F03RC=[.05,.15],resistors_caps_pads=[.30,.60],sensor_bond_consumables=[.15,.5])
    delta=[sum(v[i] for v in new.values()) for i in [0,1]]
    save('cost-impact.json',dict(currency='EUR net',quantity=7,new_components_all_unquoted_estimates=new,
        electronics_material_delta_EUR_per_unit=delta,
        E5_thermal_material_EUR_per_unit=[31.11,38.61],E6_thermal_material=[15.36,21.36],
        E6R1_SK81_thermal_plus_new_electronics=[15.36+delta[0],21.36+delta[1]],
        extra_sensor_keying_labor_minutes_estimate=[5,12],labor_rate_illustration_EUR_hour=25,
        old_thermal_labor_minutes_E5=[45,75],single_cooler_thermal_labor_E6=[25,45],
        electrical_BOM_unchanged_base_EUR_net_at7={'BUCK4S':52.76,'BOOST2S':54.33,'TRAIN_ONLY':14.11},
        PCB='Existing minimum5batch estimates unchanged; no layoutquote. NewICs/NTC need ordinary footprints only.',
        observed='SK81prices indexed5.55/7.30gross19%VAT; no seven-unit quote. Allnewcomponents remain estimates, not confirmedbaskets.',
        caution='Controller,pack/BMS,antenna,harness,enclosure,PCB,freight,VAT,RFcalibration,Xrayandfirstarticlelabor remain separate. No complete120/150EUR claim.'))
    print('3structures analyzed; new electrical/material delta',delta,'C 1WbeaconR5.5 remains conditional',flush=True)

if __name__=='__main__':main()
