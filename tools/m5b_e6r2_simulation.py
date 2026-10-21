"""Native-value AM/driver/keying ngspice fixtures, with TI TLV900x macro-model.
External licensed model stays outside MIT source. PA/converter are envelope
loads and finite-impedance sources, not a fabricated144MHz transistor model.
"""
import os,math,json,subprocess,hashlib,zipfile,re
import numpy as np
from m5b_e6r2_common import *
SIM=OUT/'simulation'
TI_ZIP=Path(os.environ.get('ARDF_TLV9002_ZIP','/tmp/m5b-e6r2/references/TLV9002-model.zip'))
TI_ZIP_SHA256='516e3f6405b699003d94840520966d7599c6c3af37f37c69541f9ed7ae211fe6'

def make(pop='BUCK4S',beta=60.,mode='normal',edge=.008):
 assert sha(TI_ZIP)==TI_ZIP_SHA256,'External TI model changed; review before using another revision'
 parts={z['ref']:z for z in manifest()['parts']}
 # Values are read from active native manifest and checked against exported
 # netlist by the independent electrical suite before final acceptance.
 val=lambda r:parts[r]['value']
 rail=8.9996 if pop=='BUCK4S' else 9.02086
 SIM.mkdir(exist_ok=True)
 model=Path('/tmp/m5b-e6r2/references/tlv9002.lib')
 with zipfile.ZipFile(TI_ZIP) as z:model.write_bytes(z.read('tlv9002.lib'))
 times=np.unique(np.r_[np.arange(0,.500001,.000025),[.385,.385001]])
 af=[];key=[]
 for t in times:
  envelope=0.;coarse=False
  for a,b in [(.02,.10),(.18,.26),(.34,.42)]:
   start=a-edge/2;end=b+edge/2
   if start-.002<=t<end+.0001:coarse=True
   if start<=t<end:
    envelope=1.
    if t<start+edge:envelope=.5-.5*math.cos(math.pi*(t-start)/edge)
    if t>end-edge:envelope=.5-.5*math.cos(math.pi*(end-t)/edge)
  af.append((t,envelope*4/2.8*(1+.8*1.0446*math.sin(2*math.pi*800*t))))
  key.append((t,3.3 if coarse else 0.))
 def pwl(rows):return 'PWL('+ ' '.join(f'{t:.9f} {v:.9g}' for t,v in rows)+')'
 # Coarse KEY transitions supplied as edges, rather than a20k-entry digitalPWL.
 kr=[(0,0)]
 for a,b in [(.02,.10),(.18,.26),(.34,.42)]:
  st=a-edge/2-.002;en=b+edge/2+.0001
  kr.extend([(st-1e-7,0),(st,3.3),(en-1e-7,3.3),(en,0)])
 kr.append((.5,0))
 fault='PWL(0 0 .384999 0 .385 3.3 .5 3.3)' if mode=='fault' else 'DC 0'
 load_gate='if(time>0.21 && time<0.24,0,1)' if mode=='load_removal' else '1'
 load_k='3' if mode=='overload' else '0.149529'
 deck=f'''* E6R2 native-value transient, {pop}, BFpass{beta:g}, {mode}, edge{edge:g}s
* TI model per-amplifier family proxy: not a package-coupling model.
.include {model}
.options reltol=.002 abstol=1n vntol=10u method=gear
Vlogic V3V3 0 3.3
Vconv vsource 0 {rail}
Rconv vsource vreg .12
Lfeed vreg vreg_l 100n
Creservoir vreg_l 0 44u
Vfault EXTERNAL_FAULT 0 {fault}
* Behavioral proxy of native INA180/LM339 and asynchronous fault latch.
*10us detector RC is a sensitivity assumption, not a measured delay guarantee.
BCURRENT raw_current_fault 0 V=if(v(VREG_SWITCH,VMOD)>.122196,3.3,0)
Rdelay raw_current_fault current_fault_delay 10k
Cdelay current_fault_delay 0 1n
BLATCH latch_drive 0 V=if(v(current_fault_delay)>1.65 || v(FAULT_LATCH)>1.65,3.3,0)
Rlatch latch_drive FAULT_LATCH 1k
Clatch FAULT_LATCH 0 1n
BEMERGENCY NORMAL_OFF 0 V=if(v(EXTERNAL_FAULT)>1.65 || v(FAULT_LATCH)>1.65,3.3,0)
Vkey KEY 0 {pwl(kr)}
BkeyN KEY_N 0 V=3.3-v(KEY)
Boff LOCAL_MOD_OFF 0 V=if(v(NORMAL_OFF)>1.65 || v(KEY_N)>1.65,3.3,0)
Bdriver DRIVER_ON 0 V=3.3-v(LOCAL_MOD_OFF)
Smain vreg_l VREG_SWITCH V3V3 NORMAL_OFF SWMAIN
.model SWMAIN SW(Ron=.03 Roff=1G Vt=1.65 Vh=.05)
R309 VREG_SWITCH VMOD {val('R309')}
C635 VMOD 0 1u
C306 VMOD 0 100n
C307 VMOD 0 100n
* Prepared independent driver regulators, reservoir upstream of U305.
Vdriver drvsource 0 5
Rdriver drvsource VDRV_FILTER .12
C409 VDRV_FILTER 0 150u
S305 VDRV_FILTER VDRV_MMIC DRIVER_ON 0 SWDRV
.model SWDRV SW(Ron=.079 Roff=1G Vt=1.65 Vh=.05)
C603 VDRV_MMIC 0 100n
C604 VDRV_MMIC 0 1n
Bmmic VDRV_MMIC 0 I=.1463*max(v(VDRV_MMIC),0)/5
Bqod VDRV_MMIC 0 I=if(v(DRIVER_ON)<1.65,v(VDRV_MMIC)/120,0)
* Existing slot-qualified gate-bias clamp remains independent of MorseKEY.
R606 VMOD BIAS_TOP 1k
D501 0 BIAS_TOP DBIAS
.model DBIAS D(IS=1p N=1 BV=6.2 IBV=5m)
Rpot_top BIAS_TOP BIAS_WIPER 7k
Rpot_bottom BIAS_WIPER 0 3k
C607 BIAS_WIPER 0 100n
L606 BIAS_WIPER PA_GATE_DC 33n
Cgate PA_GATE_DC 0 80p
M502 BIAS_WIPER NORMAL_OFF 0 0 NCLAMP
.model NCLAMP NMOS(LEVEL=1 VTO=1.5 KP=.1 RD=1 RS=1)
* Actual divider thresholds;3us typical comparator pole is a scenario.
R971 VPA VPA_READY_S 100k
R972 VPA_READY_S 0 33k
R973 V3V3 VPA_READY_REF 330k
R974 VPA_READY_REF 0 2.49k
R975 VDRV_MMIC DRV_READY_S 100k
R976 DRV_READY_S 0 33k
R977 V3V3 DRV_READY_REF 19.1k
R978 DRV_READY_REF 0 10k
BVREADY vr_raw 0 V=if(v(VPA_READY_S)>v(VPA_READY_REF),3.3,0)
Rvr vr_raw VPA_READY 3k
Cvr VPA_READY 0 1n
BDREADY dr_raw 0 V=if(v(DRV_READY_S)>v(DRV_READY_REF),3.3,0)
Rdr dr_raw DRV_READY 3k
Cdr DRV_READY 0 1n
BCLOCK CLOCK_OFF 0 V=if(v(LOCAL_MOD_OFF)>1.65 || v(VPA_READY)<1.65 || v(DRV_READY)<1.65,3.3,0)
Vaf AF_PWM 0 {pwl(af)}
R503 AF_PWM AF_F1 {val('R503')}
R504 AF_F1 AF_F2 {val('R504')}
C503 AF_F1 AF_DC {val('C503')}
C504 AF_F2 0 {val('C504')}
X401B AF_F2 AF_DC V3V3 0 AF_DC TLV9002
* U402 selects reconstructed AF or0V, as actual E6R2 schematic.
B402 AM_COMMAND 0 V=if(v(KEY)>1.65,v(AF_DC),0)
R516 AM_COMMAND MOD_COMMAND {val('R516')}
Q405 MOD_COMMAND MOD_COMMAND_OFF_BASE 0 M3904
R985 NORMAL_OFF MOD_COMMAND_OFF_BASE {val('R985')}
R986 MOD_COMMAND_OFF_BASE 0 {val('R986')}
R509 LOCAL_MOD_OFF MOD_OFF_BASE {val('R509')}
Q404 MOD_BASE MOD_OFF_BASE 0 M3904
R508 MOD_DRIVE MOD_BASE {val('R508')}
R510 MOD_BASE 0 {val('R510')}
X401C MOD_COMMAND VPA_FB V3V3 0 MOD_DRIVE TLV9002
C505 MOD_DRIVE VPA_FB {val('C505')}
R511 VPA VPA_FB {val('R511')}
R512 VPA_FB 0 {val('R512')}
Q402 MOD_SINK MOD_BASE MOD_E NHELP
Q403 MOD_BASE MOD_E 0 M3904
R507 MOD_E 0 {val('R507')}
R506 PASS_BASE MOD_SINK {val('R506')}
R505 PASS_BASE VMOD {val('R505')}
Q401 VPA_PRE PASS_BASE VMOD PPASS
R970 VPA_PRE VPA {val('R970')}
C506 VPA 0 {val('C506')}
C634 VPA 0 330p
R513 VPA 0 {val('R513')}
BPA VPA 0 I=({load_k}*max(v(VPA),0)+.15*min(max(v(VPA)/.2,0),1))*({load_gate})
* Gummel-Poon parameter sensitivities; not ST-characterized models.
.model PPASS PNP(IS=1e-12 BF={beta:g} VAF=50 IKF=4 RB=.2 RC=.04 RE=.02 CJE=500p CJC=150p TF=100n TR=1u)
.model NHELP NPN(IS=1e-13 BF=40 VAF=50 IKF=1 RB=2 RC=.1 RE=.05 CJE=100p CJC=40p TF=10n TR=100n)
.model M3904 NPN(IS=6.7e-15 BF=150 VAF=75 CJE=4.5p CJC=3.6p TF=300p TR=20n)
.control
set wr_singlescale
set wr_vecnames
tran 10u .5 0 5u
wrdata TRACE_PATH v(KEY) v(LOCAL_MOD_OFF) v(AF_DC) v(VPA) v(VMOD) v(VDRV_MMIC) v(MOD_DRIVE) v(MOD_E) v(CLOCK_OFF) v(VREG_SWITCH,VMOD) v(VPA_PRE,VPA) v(PA_GATE_DC) v(FAULT_LATCH)
meas tran VPAmax MAX v(VPA)
meas tran VMODmax MAX v(VMOD)
meas tran VPAspace MAX v(VPA) FROM=.11 TO=.17
meas tran driverSPACE MAX v(VDRV_MMIC) FROM=.11 TO=.17
quit
.endc
.end
'''
 return deck

def run_case(pop,beta,mode,edge=.008):
 name=f'{pop}-beta{beta:g}-{mode}-{edge*1000:g}ms';tmp=Path('/tmp/m5b-e6r2')/(name+'.dat');deck=make(pop,beta,mode,edge).replace('TRACE_PATH',str(tmp));(SIM/(name+'.cir')).write_text(deck)
 run=subprocess.run(['ngspice','-D','ngbehavior=ps','-b',str(SIM/(name+'.cir'))],capture_output=True,text=True)
 (SIM/(name+'.log')).write_text(run.stdout+run.stderr);assert run.returncode==0,(name,run.stderr[-2000:]);assert tmp.exists(),name
 data=np.loadtxt(tmp,skiprows=1);t=data[:,0];vpa=data[:,4];mod=data[:,5];current=data[:,10]/.068
 space=(t>=.11)&(t<=.17);mark=(t>.04)&(t<.09);after=(t>.245)&(t<.255)
 reduced=data[::max(1,len(data)//5000)];np.savetxt(SIM/(name+'.csv'),reduced,delimiter=',',fmt='%.9g',header='t,KEY,LOCAL_MOD_OFF,AF_DC,VPA,VMOD,VDRV_MMIC,MOD_DRIVE,MOD_E,CLOCK_OFF,shunt68mV,shunt50mV,PA_GATE_DC,FAULT_LATCH',comments='')
 result=dict(population=pop,pass_beta_assumed=beta,mode=mode,edge_s=edge,ngspice_returncode=run.returncode,points=len(t),
  VPA_max_V=float(vpa.max()),VMOD_max_V=float(mod.max()),VPA_space_max_V=float(vpa[space].max()),driver_space_max_V=float(data[space,6].max()),
  rail_peak_A=float(current.max()),pass_current_peak_A=float((data[:,11]/.05).max()),
  rail_space_mean_A=float(current[space].mean()),pass_space_mean_A=float((data[space,11]/.05).mean()),
  nominal_current_threshold_A=1.797,overcurrent_threshold_crossed=bool(current.max()>1.797),
  mark_envelope_min_V=float(vpa[mark].min()),mark_envelope_max_V=float(vpa[mark].max()),
  recovered_window_min_V=float(vpa[after].min()),recovered_window_max_V=float(vpa[after].max()),
  physical='NOT_RUN')
 if mode=='fault':
  sel=t>.386;result['VPA_after_fault_max_V']=float(vpa[sel].max());result['clock_inhibited_after_fault']=bool(np.min(data[sel,9])>3.);result['PA_gate_after_fault_max_V']=float(data[sel,12].max())
 if mode=='overload':
  triggered=np.flatnonzero(data[:,13]>1.65);result['trip_time_s']=float(t[triggered[0]]) if len(triggered) else None
  result['latch_remains_faulted']=bool(np.min(data[t>.1,13])>3.)
 print(name,result,flush=True);return result

def ac_case(unloaded=False):
 name='loop-unloaded' if unloaded else 'loop-loaded';deck=make().split('.control')[0]
 # TI noise-generator internal nodes are floating at DC in ngspice42.
 # A1T numerical shunt regularizes them (<=3.3pA per external node).
 deck=deck.replace('method=gear','method=gear rshunt=1e12')
 # Linearize the AM loop in its enabled operating state. A regenerative
 # fault latch has no unique DC solution and is tested in transient analysis.
 deck=re.sub(r'BCURRENT .*?BEMERGENCY [^\n]+',
  'Vacfault FAULT_LATCH 0 DC 0\nVacenable NORMAL_OFF 0 DC 0',deck,flags=re.S)
 # Separate continuously enabled analog return-ratio fixture. Digital
 # switching, bias zener and latch transients belong to the transient deck;
 # holding their topology here avoids a discontinuous DC switching solution.
 deck=re.sub(r'Vfault .*?(?=Vaf )',
  'Vacenable NORMAL_OFF 0 0\nVackey KEY 0 3.3\nVaclocal LOCAL_MOD_OFF 0 0\n'
  'Rmain vreg_l VREG_SWITCH .03\nR309 VREG_SWITCH VMOD '+manifest_value('R309')+'\n'
  'C635 VMOD 0 1u\nC306 VMOD 0 100n\nC307 VMOD 0 100n\n',deck,flags=re.S)
 deck=re.sub(r'^Vaf .*$', 'Vaf AF_PWM 0 DC 1.42857143',deck,flags=re.M)
 deck=re.sub(r'^Vkey .*$', 'Vkey KEY 0 DC 3.3',deck,flags=re.M)
 if unloaded:deck=re.sub(r'^BPA .*$', 'RnoPA VPA 0 1G',deck,flags=re.M)
 deck=deck.replace('X401C MOD_COMMAND VPA_FB','Vinject VFB_AMP VPA_FB DC 0 AC 1\nX401C MOD_COMMAND VFB_AMP')
 path=Path('/tmp/m5b-e6r2')/(name+'.dat')
 deck+=f'''.control
set wr_singlescale
set wr_vecnames
ac dec 100 1 100Meg
let returnratio=-v(VPA_FB)/v(VFB_AMP)
let realpart=real(returnratio)
let imagpart=imag(returnratio)
wrdata {path} realpart imagpart
quit
.endc
.end
'''
 (SIM/(name+'.cir')).write_text(deck);run=subprocess.run(['ngspice','-D','ngbehavior=ps','-b',str(SIM/(name+'.cir'))],capture_output=True,text=True)
 (SIM/(name+'.log')).write_text(run.stdout+run.stderr);assert run.returncode==0 and path.exists()
 data=np.loadtxt(path,skiprows=1);freq=data[:,0];z=data[:,1]+1j*data[:,2];mag=np.abs(z);phase=np.unwrap(np.angle(z))*180/np.pi
 cross=np.flatnonzero((mag[:-1]>=1)&(mag[1:]<1));margins=[180+float(phase[k]) for k in cross]
 np.savetxt(SIM/(name+'.csv'),data,delimiter=',',fmt='%.9g',header='frequency_Hz,real_return_ratio,imag_return_ratio',comments='')
 result=dict(unloaded=unloaded,crossover_Hz=[float(freq[k]) for k in cross],phase_margin_deg=margins,positive_margin=bool(margins and min(margins)>0),
  method='Voltage injection at high-impedance opamp negative input; includes native C505 feedback and transistor stage; TI per-amplifier model and assumed BJT parameters')
 print(name,result,flush=True);return result

def manifest_value(ref):return next(z['value'] for z in manifest()['parts'] if z['ref']==ref)

def main():
 guard();rows=[]
 for pop,beta,mode in [('BUCK4S',60.,'normal'),('BOOST2S',60.,'normal'),('BUCK4S',20.,'normal'),('BUCK4S',60.,'load_removal'),('BUCK4S',60.,'overload'),('BUCK4S',60.,'fault')]:rows.append(run_case(pop,beta,mode))
 for edge in [.005,.012]:rows.append(run_case('BUCK4S',60.,'normal',edge))
 ac=[ac_case(False),ac_case(True)]
 save('simulation-results.json',dict(cases=rows,loop_gain=ac,TI_source='https://www.ti.com/lit/zip/sbomal2',TI_zip_sha256=sha(TI_ZIP),
  assumptions='TI TLV9002 per-amplifier family proxy for TLV9004; generic bounded BJT parameters; average PA DC load; prepared converter/driver finite-impedance source;3us readiness pole; no144MHz transistor model or converter switching-loop validation',
  safety='Native current threshold plus behavioral10usdetectorRC/latch proxy interrupts overload; actual analog/fault latch netlist checked independently. Delays/semiconductor parameters require first-article measurement; no guaranteed response claimed. Forced fault overrides all keying.',physical='NOT_RUN'))
if __name__=='__main__':main()
