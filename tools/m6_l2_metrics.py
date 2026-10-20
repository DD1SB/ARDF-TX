#!/usr/bin/python3
"""Native geometry-derived I2C, supply and decoupling review scenarios.
Electrical scenarios are calculated design bounds, not physical measurements.
"""
import json,math,hashlib
import pcbnew as p
from m6_l2_design import P,D

def main():
 b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));fs={f.GetReference():f for f in b.GetFootprints()}
 def pad(ref,num):return next(a for a in fs[ref].Pads() if a.GetNumber()==str(num))
 def xy(v):return list(map(p.ToMM,v))
 nets={}
 for name in ['RTC80_SCL','RTC80_SDA','EXP_SCL','EXP_SDA','EXP_VDD']:
  ts=[t for t in b.GetTracks() if t.GetNetname()==name];length=sum(p.ToMM(t.GetLength()) for t in ts if not isinstance(t,p.PCB_VIA));vias=sum(isinstance(t,p.PCB_VIA) for t in ts)
  if name!='EXP_VDD':
   cap=length*.2+vias*.5+50
   rise=.8473*4700*1.05*cap*1e-12
   assert rise<1e-6,(name,rise)
   nets[name]=dict(trace_length_mm=length,vias=vias,capacitance_scenario_pF=cap,rise_time_s=rise,standard_mode_limit_s=1e-6)
  else:
   widths=[p.ToMM(t.GetWidth()) for t in ts if not isinstance(t,p.PCB_VIA)]
   # Sum every branch length and via as an intentionally pessimistic single
   # source-to-load path. Actual branched load currents give smaller drops.
   resistance=.0175*length/1000/(min(widths)*.035)*(1+.00393*65)+vias*.005
   rail=3.2505-(.08+resistance)*.210
   assert rail>2.7,(rail,resistance)
   nets[name]=dict(total_branched_trace_length_mm=length,vias=vias,min_width_mm=min(widths),all_branches_in_series_85C_scenario_ohm=resistance,simultaneous_option_fault_allowance_A=.210,V3V3_input_min_V=3.2505,LM66100_Ron_scenario_ohm=.08,protected_rail_min_scenario_V=rail,buffer_B_minimum_V=2.7)
 distances=[]
 for cap,ic,pin in [('C80','U80',16),('C81','U81',1),('C82','U81',8),('C83','U82',1)]:
  a=pad(cap,1);z=pad(ic,pin);distances.append(dict(capacitor=cap,IC=ic,pin=pin,straight_distance_mm=math.dist(xy(a.GetPosition()),xy(z.GetPosition())),actual_pads_mm=[xy(a.GetPosition()),xy(z.GetPosition())]))
 report=dict(classification='CALCULATED native geometry and explicit component/load scenarios; NOT physical qualification',native_sha256=hashlib.sha256((P/'CTRL.kicad_pcb').read_bytes()).hexdigest(),bus_frequency_Hz=100000,capacitance_assumptions=dict(trace_pF_per_mm=.2,via_pF=.5,fixed_device_and_parasitic_pF_per_line=50,external_I2C_cable='None: header exposes GPIO, not I2C',status='Conservative engineering allocation, not a measured/vendor-guaranteed board capacitance'),nets=nets,decoupling=distances,power=dict(regulator='AP63203WU-7',IC_electrical_limit_A=2,ESP32_allowance_A=.5,both_RF_logic_reservations_A=.3,LoRa_TX_A=.12,option_fault_allowance_A=.23,reserved_short_burst_A=1.15,continuous_controller_budget_A=.4,header_operating_budget_A=.010,header_limiter_ohm=float(fs['R330'].GetValue()),policy='Short burst is not continuous thermal approval. Keep existing USB-only WiFi/RF restrictions; accessory faults may invoke current limiting/reset and must remain fail-off.',physical='NOT_RUN'))
 (D/'L2-bus-power-layout-calculations.json').write_text(json.dumps(report,indent=2)+'\n')
 print('Native I2C rise-time/supply geometry scenarios PASS')
if __name__=='__main__':main()
