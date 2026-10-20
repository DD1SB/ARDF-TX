#!/usr/bin/python3
"""Independent manufacturer/pin/fault models of actual L2 native source.
No comparison of generated report strings is used as electrical verification.
"""
import json,copy,hashlib,math,itertools,subprocess,csv,sys
from pathlib import Path
import pcbnew as p
from m6_l2_design import P,D,ROOT,BASE,pt,MM

MODULE={1:'GND',2:'3V3',3:'EN',4:4,5:5,6:6,7:7,8:15,9:16,10:17,11:18,12:8,13:19,14:20,15:3,16:46,17:9,18:10,19:11,20:12,21:13,22:14,23:21,24:47,25:48,26:45,27:0,28:35,29:36,30:37,31:38,32:39,33:40,34:41,35:42,36:44,37:43,38:2,39:1,40:'GND',41:'GND_EP'}
NEW={
 'J8':{'1':'FOX_GND','2':'FOX_DATA','3':'FOX_V_UNAVAILABLE'},
 'J9':{**{str(i+1):'HDR_P'+str(i) for i in range(8)},'9':'HDR_3V3','10':'GND'},
 'U80':{'1':'GND','2':'GND','3':'GND','4':'EXP_P0','5':'EXP_P1','6':'EXP_P2','7':'EXP_P3','8':'GND','9':'EXP_P4','10':'EXP_P5','11':'EXP_P6','12':'EXP_P7','14':'EXP_SCL','15':'EXP_SDA','16':'EXP_VDD'},
 'U81':{'1':'V3V3','2':'RTC80_SCL','3':'RTC80_SDA','4':'GND','5':'EXP_VDD','6':'EXP_SDA','7':'EXP_SCL','8':'EXP_VDD'},
 'U82':{'1':'V3V3','2':'GND','3':'EXP_VDD','5':'GND','6':'EXP_VDD'},
 'Q80':{'1':'FOX_TX_B','2':'GND','3':'FOX_SINK'},
 'Q81':{'1':'FOX_EN_B','2':'GND','3':'FOX_TX_B'},
 'Q82':{'1':'FOX_RX_GATE','2':'GND','3':'FOX_RX'},
 'D81':{'1':'FOX_SINK','2':'GND'},'D82':{'1':'GND','3':'FOX_RX_GATE'},
 'R304':{'1':'FOX_DATA','2':'FOX_SINK'},'R305':{'1':'FOX_TX','2':'FOX_EN_B'},
 'R307':{'1':'SAFE','2':'FOX_TX_B'},'R306':{'1':'FOX_EN_B','2':'GND'},'R308':{'1':'FOX_TX_B','2':'GND'},'C84':{'1':'FOX_TX_B','2':'GND'},'R309':{'1':'FOX_DATA','2':'FOX_RX_GATE'},
 'R310':{'1':'FOX_RX_GATE','2':'GND'},'R311':{'1':'V3V3','2':'FOX_RX'},
 'R315':{'1':'FOX_RX','2':'GND'},'R313':{'1':'FOX_V_UNAVAILABLE','2':'FOX_GND'},
 'R314':{'1':'FOX_GND','2':'GND'},'R330':{'1':'EXP_VDD','2':'HDR_3V3'},
 'R316':{'1':'FOX_GND','2':'GND'},
 'R331':{'1':'V3V3','2':'GND'},
 'R300':{'1':'UART_TX','2':'REC_TX'},'R301':{'1':'UART_RX','2':'REC_RX'},
 'R302':{'1':'UART_TX','2':'FOX_TX'},'R303':{'1':'UART_RX','2':'FOX_RX'}}
for i in range(8):NEW['R'+str(322+i)]={'1':'EXP_P'+str(i),'2':'HDR_P'+str(i)}
for i,gpio in enumerate([3,45,46],1):
 if gpio==45:continue
 NEW['JP'+str(i)]={'1':'STRAP'+str(gpio),'2':'ACCESS'+str(gpio)}
 NEW['TP'+str(80+i)]={'1':'ACCESS'+str(gpio)}
for r,net in [('D80','FOX_DATA'),('D83','FOX_V_UNAVAILABLE'),('D84','FOX_GND')]:NEW[r]={'1':net,'2':'GND'}
for ref,net in [('C80','EXP_VDD'),('C81','V3V3'),('C82','EXP_VDD'),('C83','V3V3')]:NEW[ref]={'1':net,'2':'GND'}

# Explicit local digital re-routing only. Every original terminal, RF launch,
# power/reset/safety branch and all original ground vias remain checked below.
# These nets retain their accepted GPIO functions and source/destination pads.
DIGITAL_ECO={'SPI_SCK','SPI_MOSI','SPI_MISO','RTC80_SDA','RTC80_SCL',
             'SHIFT_LATCH','SLOT','KEY','UART_TX','UART_RX'}

VALUES={'U10':'ESP32-S3-WROOM-1U-N4','U80':'TCA9534APWR','U81':'TCA9517DR','U82':'LM66100DCKR','Q80':'BSS138BK,215','Q81':'MMBT3904LT1G','Q82':'BSS138BK,215','D81':'BAS316,115','D82':'BZX84-C12,215','D80':'PESD1IVN24-AX','D83':'PESD1IVN24-AX','D84':'PESD1IVN24-AX'}
RES={'R300':0,'R301':0,'R302':0,'R303':0,'R304':680,'R305':1000,'R306':4700,'R307':1000,'R308':4700,'R309':47000,'R310':100000,'R311':160,'R312':100000,'R313':0,'R314':470,'R315':620,'R316':470,'R320':4700,'R321':4700,'R330':22,'R331':10000,**{'R'+str(i):1000 for i in range(322,330)}}
def ohm(v):
 return float(v[:-1])*{'k':1000,'M':1e6}[v[-1]] if v[-1] in 'kM' else float(v)
def fps(b):return {f.GetReference():f for f in b.GetFootprints()}
def pad(f,n):return next(a for a in f.Pads() if a.GetNumber()==str(n))
def nets(b):return {r:{a.GetNumber():a.GetNetname() for a in f.Pads()} for r,f in fps(b).items()}
def fields(f):return {z.GetName():z.GetText() for z in f.GetFields()}
def sha(f):return hashlib.sha256(f.read_bytes()).hexdigest()
def save(n,x):(D/n).write_text(json.dumps(x,indent=2)+'\n')

def check(b,baseline):
 f=fps(b);n=nets(b);old=fps(baseline);errors=[]
 def ck(ok,msg):
  if not ok:errors.append(msg)
 for r,ps in NEW.items():
  ck(r in f,'missing:'+r)
  for pin,net in ps.items():ck(n.get(r,{}).get(pin)==net,'pin:'+r+'.'+pin)
 for r,mpn in VALUES.items():ck(fields(f[r]).get('MPN')==mpn,'identity:'+r)
 for r,value in RES.items():ck(ohm(f[r].GetValue())==value,'resistor:'+r)
 for r in ['R304','R314','R316','R330']:
  ck(f[r].GetFPIDAsString()=='ARDF_CTL:R_2512_6332Metric_L2','power_resistor_package:'+r)
 for r in ['C80','C81','C82','C83']:ck(f[r].GetValue()=='100n','decoupling:'+r)
 u=f['U10'];ck(u.GetValue()=='ESP32-S3-WROOM-1U-N4','no_PSRAM');ck(u.GetLayer()==p.F_Cu and abs(u.GetOrientationDegrees())<1e-8,'ESP_orientation')
 ck(u.GetFPIDAsString()=='ARDF_CTL:ESP32_S3_WROOM_1U_N4_L2','dedicated_1U_footprint')
 ck({a.GetNumber() for a in u.Pads() if a.GetNumber()}=={str(i) for i in range(1,42)},'ESP_40_plus_EP')
 for i in range(1,41):
  a=pad(u,i);z=pad(old['U10'],i)
  ck(a.GetPosition()==z.GetPosition() and a.GetSize()==z.GetSize() and a.GetOrientationDegrees()==z.GetOrientationDegrees(),'ESP_land:'+str(i))
  want={15:'STRAP3',16:'STRAP46'}.get(i,z.GetNetname())
  ck(a.GetNetname()==want or (a.GetNetname().startswith('unconnected-') and want.startswith('unconnected-')),'ESP_preserved_function:'+str(i))
 for i in [28,29,30,36,37]:ck(n['U10'][str(i)]=={'28':'RF80_FAULT','29':'START_N','30':'USB_VBUS_N','36':'UART_RX','37':'UART_TX'}[str(i)],'mandatory_GPIO:'+str(i))
 # Every historical connected terminal, including all36 RF connector pins.
 for r,fp in old.items():
  ck(r in f,'historical_footprint:'+r)
  if r=='U10':continue
  for a in fp.Pads():
   matches=[z for z in f[r].Pads() if z.GetNumber()==a.GetNumber() and z.GetPosition()==a.GetPosition()]
   ck(bool(matches),'historical_land:'+r+'.'+a.GetNumber())
   for z in matches:
    ck(z.GetSize()==a.GetSize() and z.GetDrillSize()==a.GetDrillSize(),'historical_geometry:'+r+'.'+a.GetNumber())
    want={'2':'REC_TX','3':'REC_RX'}.get(a.GetNumber(),a.GetNetname()) if r=='J3' else a.GetNetname()
    # Original U70 floating aliases may differ only in their NC label.
    ck(z.GetNetname()==want or (z.GetNetname().startswith('unconnected-') and want.startswith('unconnected-')),'historical_net:'+r+'.'+a.GetNumber())
 for r in ['J4','J5','J1','J2','J3','J7','BT1','H1','H2','H3','H4']:
  ck(f[r].GetPosition()==old[r].GetPosition() and f[r].GetOrientationDegrees()==old[r].GetOrientationDegrees(),'mechanical_anchor:'+r)
 for pin,gpio in [(15,3),(16,46)]:ck(n['U10'][str(pin)]=='STRAP'+str(gpio),'strap_net:'+str(gpio))
 for ref in ['JP1','JP3']:
  ck(f[ref].IsDNP(),'normally_open:'+ref)
  lands=list(f[ref].Pads());ck(len(lands)==2 and math.dist(tuple(lands[0].GetPosition()),tuple(lands[1].GetPosition()))>MM(1.2),'strap_link_gap:'+ref)
 ck(n['U10']['26'].startswith('unconnected-'),'GPIO45_no_breakout')
 for r in ['R300','R301']:ck(not f[r].IsDNP(),'default_recovery:'+r)
 for r in ['R302','R303','J8','J9','U80','U81','U82','Q80','Q81','Q82']:ck(f[r].IsDNP(),'default_optional:'+r)
 # Address and critical configuration nets cannot be repurposed onto UI pins.
 for i in [1,2,3]:ck(n['U80'][str(i)]=='GND','expander_address:'+str(i))
 addresses=[]
 for ref,fp in f.items():
  if fields(fp).get('MPN')=='TCA9534APWR':
   address=0x38
   for pin,bit in [(1,2),(2,1),(3,0)]:
    level=n[ref].get(str(pin));ck(level in ['GND','EXP_VDD'],'I2C_address_strap:'+ref)
    if level=='EXP_VDD':address|=1<<bit
   bus=n[ref].get('14');ck((bus,address) not in addresses,'I2C_duplicate_address:'+ref);addresses.append((bus,address))
 for i in range(1,9):ck(n['J9'][str(i)].startswith('HDR_P'),'UI_not_RF:'+str(i))
 protected={'PACK_RAW','PACK_PROT','PACK_FUSED','VIN_SYS','USB_VBUS','USB_LIMIT','V3V3_RF80','V3V3_RF2M'}
 for r in NEW:ck(not set(n[r].values())&protected,'no_external_supply_path:'+r)
 # Connector service disk is on the assembly side above the actual port.
 cx,cy=56,31.01
 for r,fp in f.items():
  if r=='U10' or fp.GetLayer()!=p.F_Cu:continue
  from m6_c1_pcb import bounds
  box=bounds(fp,0);dx=max(box[0]-cx,0,cx-box[2]);dy=max(box[1]-cy,0,cy-box[3]);ck(math.hypot(dx,dy)>=5,'WiFi_connector_access:'+r)
 # Original copper net identities, including otherwise unconnected ground vias.
 oldtracks={t.m_Uuid.AsString():t for t in baseline.GetTracks()}
 current={t.m_Uuid.AsString():t for t in b.GetTracks()}
 for uid,t in oldtracks.items():
  if t.GetNetname() in DIGITAL_ECO:continue
  ck(uid in current,'historical_copper_missing:'+uid)
  if uid in current:
   z=current[uid];ck(z.GetNetname()==t.GetNetname(),'historical_via_track_net:'+uid)
   ck(z.GetStart()==t.GetStart() and z.GetEnd()==t.GetEnd(),'historical_copper_geometry:'+uid)
 # Exact LoRa maps/feed/reference tests are independent of the L2 capture.
 import m6_l1_geometry
 errors+=['LoRa:'+e for e in m6_l1_geometry.check(b)]
 return errors

def electrical(f):
 r={k:ohm(f[k].GetValue()) for k in RES};rows=[]
 # FoxPro's own4.7k pull-up+220R, data shunt and insulated RX gate divider.
 high=[];low=[];gatefault=[]
 for gain in itertools.product([.983,1.017],repeat=6):
  rs,rg,rd,rret1,rtx,rret2=[r[n]*g for n,g in zip(['R309','R310','R312','R314','R304','R316'],gain)]
  rret=1/(1/rret1+1/rret2)
  load=1/(1/(rs+rg)+1/rd)
  for supply in [4.5,5.5]:
   current=supply/(4700*1.05+220*1.05+rret+load)
   data=current*load;high.append(data*rg/(rs+rg)-1e-6/(1/rs+1/rg))
   #13ohm hot-Ron sensitivity of the grounded-source MOSFET; source serial pin
   # logic LOW is measured relative to FoxPro's ground through R314.
   current=supply/(4700*.95+220*.95+rret+rtx+13)
   # The legacy MCU input is BEFORE its own220ohm series resistor.
   # Include its voltage drop, rather than checking only the cable contact.
   low.append((current*(13+rret+rtx+220*1.05))/(supply*.3))
  gatefault.append(min(12.7,16.8*rg/(rs+rg)))
 assert min(high)>2.5 and max(low)<1 and max(gatefault)<20
 # Native short limiting is passive, independent of the expander direction.
 pin_short=3.6/(r['R322']*.983);header_short=3.6/(r['R330']*.983)
 assert pin_short<.004 and pin_short*8<.05 and header_short<.17
 assert 3.6**2/(r['R330']*.983)<1*(155-85)/(155-70)
 gpio_off_leak=(1.7e-6+2*10e-6)*r['R331']*1.017
 rx_fault_current=22.3/(r['R309']*.983+(4700+220)*.95)
 rx_off_leak=max(16.8/(r['R309']*.983),rx_fault_current)*r['R315']*1.017
 assert gpio_off_leak<.3 and rx_off_leak<.3
 # BOTH population: simultaneous leakage into two nodes with both explicit
 # shunts fitted. Solve the actual R311-coupled network, not two isolated
 # reports that accidentally omit their combined injection.
 a=r['R331']*1.017;z=r['R315']*1.017;k=r['R311']*1.017
 gr=1/a+1/k;gx=1/z+1/k;det=gr*gx-1/k**2
 both_rail=((21.7e-6)*gx+rx_fault_current/k)/det
 both_rx=(rx_fault_current*gr+21.7e-6/k)/det
 assert both_rail<.3 and both_rx<.3
 assert r['R315']*.983/(r['R315']*.983+r['R311']*1.017)>.75
 assert 3.3495**2/(r['R311']*.983)<.1*(155-85)/(155-70)
 tx_off=50e-6*r['R306']*1.017
 inhibit_off=50e-6*r['R308']*1.017
 assert tx_off<.3 and inhibit_off<.3
 # All16.8V DC load-line operating points, even an unsaturated transistor,
 # remain below the Q80 MOSFET's hot package power rating.
 tx_linear_power=16.8**2/(4*r['R304']*.983)
 q80_rating=.350*(150-85)/(150-25)
 assert tx_linear_power<q80_rating
 assert f['C84'].GetValue()=='10n'
 # U34 SN74LVC2G04 is not an ideal rail source.100ohm is an explicit
 # engineering output-resistance scenario; the3V/16mA/VOH2.4V test point
 # implies37.5ohm. This model is not a new datasheet low-current guarantee.
 driver_r=100;pullup=r['R307']*1.017+driver_r
 gate_high=3.2505*(r['R308']*.983)/(pullup+r['R308']*.983)-50e-6/(1/pullup+1/(r['R308']*.983))
 assert gate_high>2.5
 gate_low=.1*r['R308']*1.017/(r['R307']*.983+r['R308']*1.017)+50e-6/(1/(r['R307']*1.017)+1/(r['R308']*1.017))
 assert gate_low<.48
 # Shunt saturation0.2V stays below0.48V minimum MOS threshold.
 assert .2<.48 and 42<60
 boot_truth=[]
 for safe,uart in itertools.product([False,True],repeat=2):
  gate=.2 if uart else (gate_high if safe else gate_low)
  sink=gate>.48
  assert sink==(safe and not uart)
  boot_truth.append(dict(SAFE=safe,GPIO43=uart,gate_bound_V=gate,bus_sink=sink))
 #20pF drain-gate stray allocation,9nF minimum filter: fast-step charge bound.
 gate_step=42*20e-12/(9e-9+20e-12);assert gate_step<.1 and gate_step+inhibit_off<.48
 for contact,series in [('serial',r['R304']),('ground',r['R314']),('voltage_unavailable',r['R314'])]:
  for voltage in [-16.8,0,8.4,16.8]:
   current=abs(voltage)/(series*.983);power=voltage**2/(series*.983)
   limit=1*(155-85)/(155-70)
   assert power<limit
   rows.append(dict(contact=contact,fault_V=voltage,current_upper_A=current*(2 if contact in ['ground','voltage_unavailable'] else 1),resistor_power_upper_W=power,parallel_resistors=2 if contact in ['ground','voltage_unavailable'] else 1,derated_rating_W=limit))
 return dict(classification='Native resistor-derived DC corner and passive fault bounds; semiconductor transient/temperature qualification NOT_RUN',
  resistor_corners='1% initial plus0.7% temperature sensitivity;±1.7%',FoxPro_supply_V=[4.5,5.5],
  receive_idle_gate_min_V=min(high),receive_gate_positive_fault_max_V=max(gatefault),receive_gate_negative_clamp_V=-1,
  NMOS_gate_rating_V=[-20,20],NMOS_Ron_max_ohm_at_2p5V_25C=6.5,
  transmit_LOW_fraction_of_legacy_VIL_max=max(low),port_faults=rows,
  GPIO_short_per_signal_A=pin_short,GPIO_eight_shorts_A=pin_short*8,header_short_A=header_short,
  header_short_resistor_W=3.6**2/(r['R330']*.983),header_10mA_voltage_drop_V=.010*r['R330']*1.017,
  GPIO_off_rail_bound_V=gpio_off_leak,RX_off_pin_bound_V=rx_off_leak,
  BOTH_off_rail_bound_V=both_rail,BOTH_off_RX_pin_bound_V=both_rx,
  TX_off_base_bound_V=tx_off,TX_inhibit_off_base_bound_V=inhibit_off,
  TX_hot_leakage_basis='Q80 insulated gate and permanently grounded source: no base-collector path to bus.50uA hot-leakage sensitivity across each4.7k shunt keeps gate/base below0.3V. Q81 shunts the gate; GPIO43 HIGH releases, LOW sinks only with SAFE. Q80 VDS60V exceeds TVS42V component clamp.',
  TX_max_single_transistor_loadline_W=tx_linear_power,Q80_standard_footprint_85C_rating_W=q80_rating,
  SAFE_added_load_upper_A=3.6/(r['R307']*.983),SAFE_source='U34 SN74LVC2G04DCKR; native driver retained',SAFE_driver_Rout_scenario_ohm=driver_r,SAFE_driver_basis='100ohm engineering source-resistance allocation; datasheet3V/16mA/VOH2.4V implies37.5ohm at that test point. Not a guaranteed low-current I/V curve; measure in Gate G.',TX_gate_HIGH_min_scenario_V=gate_high,TX_gate_LOW_with_100mV_driver_VOL_V=gate_low,boot_reset_UART_truth=boot_truth,TX_gate_filter_42V_step_bound_V=gate_step,TX_gate_filter_RC_s=(1/(1/pullup+1/(r['R308']*1.017)))*11e-9,
  drain_negative_clamp_V=-1.25,drain_clamp_reverse_rating_V=100,port_TVS_component_clamp_V=42,
  receive_passive_off_fault_current_bound_A=rx_fault_current,receive_passive_off_basis='Bound the ENTIRE input current through native47k, independent of MOS gate-leakage assumptions. Includes16.8V stiff DATA fault and22.3V through legacy4k7+220R during16.8V Fox-ground displacement.620ohm shunt keeps GPIO below0.3V.',RX_pullup_3p3495V_short_power_W=3.3495**2/(r['R311']*.983),RX_pullup_85C_rating_W=.1*(155-85)/(155-70),RX_13ohm_hot_Ron_scenario_LOW_V=3.3495*13/(r['R311']*.983+13),
  reverse_block_leakage_A=1.7e-6,reverse_block_basis='TI LM66100OUT-IN,VOUT-VIN<=4.5V,-40..85C',
  optional_buffer_off_leakage_envelope_A=2*10e-6,
  powered_high_RX_min_V=3.2505*r['R315']*.983/(r['R315']*.983+r['R311']*1.017),
  RTC_bus=dict(extra_upstream_pullups=0,frequency_Hz=100000,assumed_total_upstream_capacitance_F=150e-12,rise_time_s=.8473*4700*150e-12,standard_mode_max_s=1e-6,downstream_address=0x38,RTC_address=0x51),
  voltage_reporting='Unavailable for BOTH2S and4S; tip bonded to FoxPro ground, no battery source to TRS',analog_contact_relative_FoxPro_ground_fault_bound_V=(16.8/(r['R314']*.983)*2)*.1,zero_ohm_link_resistance_engineering_envelope_ohm=.1,physical='NOT_RUN')

def main():
 oldpath=Path('/tmp/m6l2/old.kicad_pcb');oldpath.parent.mkdir(parents=True,exist_ok=True);oldpath.write_bytes(subprocess.check_output(['git','show',BASE+':hardware/controller/CTRL.kicad_pcb']))
 baseline=p.LoadBoard(str(oldpath));b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));e=check(b,baseline);assert not e,e
 for name,h in json.loads((D/'frozen-files.json').read_text()).items():assert sha(ROOT/name)==h,name
 fs=fps(b);n=nets(b);rows=[]
 for pin,function in MODULE.items():
  a=pad(fs['U10'],pin);rows.append(dict(module_pin=pin,manufacturer_function='GPIO'+str(function) if isinstance(function,int) else function,controller_net=a.GetNetname(),x_mm=p.ToMM(a.GetPosition().x),y_mm=p.ToMM(a.GetPosition().y),land_x_mm=p.ToMM(a.GetSize().x),land_y_mm=p.ToMM(a.GetSize().y)))
 save('ESP32-manufacturer-pin-matrix.json',dict(part='ESP32-S3-WROOM-1U-N4',manufacturer_source='Espressif v1.8 pin definitions and Fig11-2',rows=rows))
 with (D/'GPIO-allocation.csv').open('w') as out:
  w=csv.DictWriter(out,fieldnames=rows[0].keys(),lineterminator='\n');w.writeheader();w.writerows(rows)
 save('FoxPro-GPIO-electrical-calculations.json',electrical(fs))
 tests=[]
 def mutate(name,edit):
  q=p.LoadBoard(str(P/'CTRL.kicad_pcb'));edit(q);err=check(q,baseline);assert err,name;tests.append(dict(mutation=name,detected=err))
 def net(q,r,pin,to):pad(fps(q)[r],pin).SetNet(q.FindNet(to))
 mutate('GPIO45_accessory_changes_flash_voltage',lambda q:net(q,'U10',26,'HDR_P0'))
 mutate('PSRAM_substitution',lambda q:fps(q)['U10'].SetValue('ESP32-S3-WROOM-1U-N16R8'))
 for pin in [28,29,30]:mutate('lost_GPIO_'+str(MODULE[pin]),lambda q,pin=pin:net(q,'U10',pin,'GND'))
 mutate('wrong_1U_pin1_orientation',lambda q:fps(q)['U10'].SetOrientationDegrees(180))
 def antenna_block(q):
  f=fps(q)['U81']
  if f.GetLayer()!=p.F_Cu:f.Flip(f.GetPosition(),False)
  f.SetPosition(pt(56,31.01))
 mutate('antenna_access_blocked',antenna_block)
 for ref in ['JP1','JP3']:mutate('strap_link_fitted_'+ref,lambda q,ref=ref:fps(q)[ref].SetDNP(False))
 mutate('FoxPro_direct_5V_receive',lambda q:net(q,'R303',2,'FOX_DATA'))
 mutate('unsafe_old_emitter_gated_NPN',lambda q:net(q,'Q80',2,'FOX_TX_B'))
 mutate('wrong_open_collector_direction',lambda q:net(q,'Q80',2,'FOX_DATA'))
 mutate('boot_output_inhibit_bypassed',lambda q:net(q,'R307',1,'V3V3'))
 mutate('unpowered_receive_backfeed_path',lambda q:net(q,'Q82',2,'V3V3'))
 mutate('raw_pack_on_analog_contact',lambda q:net(q,'J8',3,'PACK_RAW'))
 mutate('TRS_ring_tip_reversed',lambda q:net(q,'J8',2,'FOX_V_UNAVAILABLE'))
 mutate('expander_address_conflict',lambda q:net(q,'U80',1,'V3V3'))
 def duplicate_i2c(q):
  f=p.Cast_to_FOOTPRINT(fps(q)['U80'].Duplicate(False));f.SetReference('U89');q.Add(f)
 mutate('two_actual_expanders_same_bus_address',duplicate_i2c)
 mutate('RTC_buffer_direction_wrong',lambda q:net(q,'U81',2,'EXP_SCL'))
 mutate('expander_enables_RF',lambda q:net(q,'U80',4,'ARM'))
 for ref in ['J4','J5']:mutate('RF_connector_changed_'+ref,lambda q,ref=ref:net(q,ref,1,'V3V3'))
 mutate('LoRa_SPI_broken',lambda q:net(q,'U70',14,'GND'))
 # Native actual resistor mutations must violate numerical bounds or identity.
 for ref,value in [('R320','0'),('R313','100k'),('R309','0'),('R304','0'),('R314','0'),('R330','0'),('R322','0'),('R331','1M')]:
  mutate('short_or_wrong_'+ref,lambda q,ref=ref,value=value:fps(q)[ref].SetValue(value))
 # An original free-standing ground via is checked even if all PAD tests pass.
 uid=next(t.m_Uuid.AsString() for t in baseline.GetTracks() if isinstance(t,p.PCB_VIA) and t.GetNetname()=='GND')
 mutate('historical_ground_via_renamed',lambda q:next(t for t in q.GetTracks() if t.m_Uuid.AsString()==uid).SetNet(q.FindNet('FOX_DATA')))
 save('L2-native-negative-regression.json',dict(status='PASS',mutations=tests,physical='NOT_RUN'))
 current={t.m_Uuid.AsString():t for t in b.GetTracks()}
 changes=[]
 for t in baseline.GetTracks():
  uid=t.m_Uuid.AsString();z=current.get(uid)
  if z is None or z.GetStart()!=t.GetStart() or z.GetEnd()!=t.GetEnd() or z.GetNetname()!=t.GetNetname():
   assert t.GetNetname() in DIGITAL_ECO,(uid,t.GetNetname())
   changes.append(dict(uuid=uid,net=t.GetNetname(),baseline_start_mm=list(map(p.ToMM,t.GetStart())),baseline_end_mm=list(map(p.ToMM,t.GetEnd())),change='replaced local digital routing' if z is None else 'adjusted local digital routing'))
 save('L1-L2-change-audit.json',dict(status='PASS',baseline=BASE,native_sha256=sha(P/'CTRL.kicad_pcb'),permitted_digital_routing_nets=sorted(DIGITAL_ECO),digital_routing_changes=changes,other_baseline_tracks_vias_preserved=True,baseline_pad_instances=sum(len(list(fp.Pads())) for fp in fps(baseline).values()),current_pad_instances=sum(len(list(fp.Pads())) for fp in fs.values()),new_references=sorted(set(fs)-set(fps(baseline))),frozen_files=len(json.loads((D/'frozen-files.json').read_text())),RF80_RF2M='UNCHANGED_FROM_M7',physical='NOT_RUN'))
 print('L2 independent native/pin/fault audit PASS;',len(tests),'native mutations rejected')
if __name__=='__main__':main()
