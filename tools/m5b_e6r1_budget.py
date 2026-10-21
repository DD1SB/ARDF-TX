"""Fresh waveform energy tables and explicit transmitter overhead parameters."""
import csv,itertools
from m5b_e6r1_common import *
from m5b_e6r1_morse import stats,units
from m5b_e6r1_thermal import waveform,word_period
from m5b_e6r1_power import point,transition_packet

def main():
    guard();rows=[];system=[]
    for pop,e,a,mode in itertools.product(['BUCK4S','BOOST2S'],[.25,.5,1.],['A','B','C'],['Classic','Sprint','MO']):
        slot,cycle=(60,300) if mode=='Classic' else (12,60) if mode=='Sprint' else (word_period('MO',12),word_period('MO',12))
        code='MO' if mode=='MO' else 'MO5'
        seq,loads,energy=waveform(code,12,slot,cycle,pop,e,a,periodic_word=(mode=='MO'))
        output=dict(population=pop,ERP_W=e,architecture=a,mode=mode,cycle_s=cycle,
            MARK_us=stats(code,12,slot,cycle)['finite_slot_MARK_us'],
            MARK_mean_heat_W=point(e,pop,architecture=a)['PA_W']+point(e,pop,architecture=a)['pass_W']+point(e,pop,architecture=a)['helper_W'],
            PA_J=energy['PA_W'],pass_J=energy['pass_W'],helper_J=energy['helper_W'],other_PCB_J=energy['other_PCB_W'],
            RF_connector_J=energy['connector_RF_W'],RF_battery_J=energy['RF_battery_input_W'],RF_logic_3V3_J=energy['controller_3V3_input_W'],
            stored_net_J=energy['storage_W'],DC_input_J=energy['DC_input_W'])
        rows.append(output)
        for ctrl,eta in itertools.product([.2,.5,1.5],[.85,.90,.95]):
            pcb_logic=energy['controller_3V3_input_W']/cycle
            total=energy['RF_battery_input_W']/cycle+(pcb_logic+ctrl)/eta
            # Common precharge outside allocated slots: one complete cold-bank
            # charge/release packet and250ms logic/source/converter reserve.
            preparation=0. if mode=='MO' else transition_packet(e,pop,'B')['input_J']+.25*.15
            system.append(dict(population=pop,ERP_W=e,architecture=a,mode=mode,controller_delivered_power_W_assumed=ctrl,
                controller_conversion_efficiency_assumed=eta,RF_module_DC_W=energy['DC_input_W']/cycle,
                system_battery_W=total+preparation/cycle,common_prepare_energy_J_per_cycle=preparation,
                controller_local_heat_W=ctrl+(pcb_logic+ctrl)*(1/eta-1),
                note='Controller allowance is an explicit sensitivity, not measured ESP32 current. RFboard3V3 is not counted twice. Common preparatory packet is outside scheduled waveform.'))
    with (OUT/'energy-integrals.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]),lineterminator='\n');w.writeheader();w.writerows(rows)
    save('system-power.json',dict(rows=system,domain='Separate RFbattery and controller conversion domain; no single fixed whole-transmitter consumption claim',physical='NOT_RUN'))
    print('Integrated energy rows',len(rows),'system-overhead scenarios',len(system))

if __name__=='__main__':main()
