#!/usr/bin/env python3
"""Re-run unchanged E1 passive models; add E2-specific protection limits.
No measured parasitic, switch/comparator delay, surge or RF qualification.
"""
import argparse,json,math
from pathlib import Path
from m3b_power_analysis import calc
R=Path(__file__).resolve().parents[1];D=R/'hardware/80m/review/M3B-E2'
def main():
 a=argparse.ArgumentParser();a.add_argument('--write',action='store_true');args=a.parse_args();r,c,w,h=calc();r['date']='2026-10-15';r['revision']='M3B-E2';r['input_model_cable_limit_H']=r.pop('input_max_qualified_cable_L_H');r['qualification']='ALL PHYSICAL GATES NOT_RUN; model envelope only'
 r['input_protection']=dict(chain='J301/F301/SS34 -> VIN_PACK -> R3501.5ohm -> VIN_PA/C350100u/SMBJ17A -> TPS54302 -> VPA -> TPS22810 -> VPA_ISO/R330 -> VPA_LOAD/R410 -> VDRV',TVS=dict(manufacturer='Littelfuse',mpn='SMBJ17A',stand_off_V=17,breakdown_at_1mA_V=[18.9,20.9],clamp_at_21_8A_V=27.6,not_credited_as_18V_clamp=True),load_switch=dict(operating_max_V=18,absolute_max_V=20,typical_turnoff_us=3.3,guaranteed_complete_isolation_us=None,QOD_R_typ_ohm_at_12V=265,QOD_R_max_ohm_at_12V=350),wrong_24V_source_example=dict(status='NOT PERMITTED OR QUALIFIED',assumed_TVS_node_V=20.9,approx_current_A=(24-20.9)/1.5,damper_W=((24-20.9)/1.5)**2*1.5,TVS_W=20.9*(24-20.9)/1.5,limitation='Example only: nonlinear TVS DC behavior/fuse timing not simulated; no coordination guarantee'),charged_reverse_example=dict(charged_cap_V=16.8,reversed_source_V=-16.8,diode_reverse_V=33.6,SS34_VRRM_V=40,status='Static voltage comparison only; ringing/leakage/connector fault NOT_RUN'))
 cmax=(47*1.2+1*1.2+.1*1.1)*1e-6
 r['driver_discharge_examples']=[]
 for rpd in (265,350,1000):
  rr=rpd+101+4.747+.0505
  r['driver_discharge_examples'].append(dict(QOD_R_assumed_ohm=rpd,total_R_ohm=rr,direct_C_max_F=cmax,t_8_6V_to_4V_ms=rr*cmax*math.log(8.6/4)*1000,limitation='QOD guaranteed maximum quoted only at12V, not an8V/low-Vout turnoff guarantee; coupled shaper capacitance/backfeed omitted'))
 r['clamp_comparison']=dict(candidate='10V nominal500mW shunt zener, external fixture study only',assumed_clamp_V=10,stuck_18V_current_A=(18-10)/4.653,clamp_W=10*(18-10)/4.653,series_resistor_W=(18-10)**2/4.653,decision='Do not add an unqualified small zener: needs guaranteed dynamic clamp, pulse SOA and sustained-fault clearing; cannot guarantee12.6V. Retain removable driver/PA and bounded power-only prequalification.')
 r['scope_of_electrical_change']='Q403 physical B/E mapping and U311 REF/anode corrected; input/driver circuit component values unchanged; D302 exact manufacturer specified; input/driver protection remains conditional.'
 out=R/'docs/M3B_E2_POWER_RESULTS.json';s=json.dumps(r,indent=2)+'\n'
 if args.write:
  out.write_text(s);(D/'input-surrogate.cir').write_text(h);(D/'driver-surrogate.cir').write_text(c)
 else:assert out.read_text()==s,'E2 power model stale'
 print('PASS E2 passive models:',len(r['input_corners']),'analytic;',len(r['input_ngspice_surrogates']),'input SPICE;',len(r['driver_surrogates']),'driver SPICE; physical protection NOT qualified')
if __name__=='__main__':main()
