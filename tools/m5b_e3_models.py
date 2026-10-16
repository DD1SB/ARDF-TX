#!/usr/bin/python3
"""Reproducible E3 analytical models;allRF/thermalhardwaretestsNOT_RUN."""
import math,itertools,json,csv,cmath,collections,subprocess
import pcbnew as p
from m5b_e3_common import *

def table(name,rows):
 with(OUT/name).open('w')as f:w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def mul(a,b):return[[sum(a[i][k]*b[k][j]for k in range(2))for j in range(2)]for i in range(2)]
def cascade(*stages):
 m=[[1+0j,0j],[0j,1+0j]]
 for a in stages:m=mul(m,a)
 return m
def series(z):return[[1,z],[0,1]]
def shunt(y):return[[1,0],[y,1]]
def line(l,w=WIDTH,h=H,t=T,er=ER,f=144.7e6):
 z,ee=microstrip(w,h,t,er);q=2*math.pi*f*l*.001*math.sqrt(ee)/299792458
 return[[math.cos(q),1j*z*math.sin(q)],[1j/z*math.sin(q),math.cos(q)]]
def s21(m):return 2/(m[0][0]+m[0][1]/50+m[1][0]*50+m[1][1])
def rf():
 z,ee=microstrip(WIDTH,H,T,ER);oldz,olde=microstrip(1.102,.64,.07,4.3);rows=[]
 for ref,l in LENGTHS.items():
  orig=l/LENGTH_SCALE;rows.append(dict(ref=ref,E2_length_mm=round(orig,4),E3_length_mm=l,E3_width_mm=WIDTH,E2_phase_deg=360*144.7e6*orig*.001*math.sqrt(olde)/299792458,E3_phase_deg=360*144.7e6*l*.001*math.sqrt(ee)/299792458,Z0_ohm=z))
 table('transmission-lines.csv',rows);sweep=[]
 for h,er,t,w,f in itertools.product([1.3,1.5,1.7],[4.1,4.5,4.8],[.030,.035,.041,.050],[WIDTH*.8,WIDTH,WIDTH*1.2],[144.,144.5,144.7,144.9,146.]):
  zz,e=microstrip(w,h,t,er);gamma=(zz-50)/(zz+50);sweep.append(dict(h_mm=h,Dk=er,Cu_mm=t,width_mm=w,MHz=f,Z0_ohm=zz,epsilon_effective=e,single_transition_return_loss_dB=-20*math.log10(max(1e-12,abs(gamma))),longest_TL608_phase_deg=360*f*1e6*LENGTHS['TL608']*.001*math.sqrt(e)/299792458,physical='NOT_RUN'))
 table('RF-tolerance-sweep.csv',sweep)
 # First-order thin-superstrate energyparticipation bound:theuncoatedmodel
 # has anairfringefraction. Perturb0..2*tm/hofthatfractionwithmaskDk3.8.
 # Thisis anexplicit approximate sensitivity,notfullwaveorfieldsolution.
 masks=[]
 for tm in[0,.015,.030]:
  fraction=min(1,2*tm/H);e=ee+(ER-ee)/(ER-1)*(3.8-1)*fraction
  masks.append(dict(mask_mm=tm,approx_effective_Dk=e,approx_Z0_ohm=z*math.sqrt(ee/e),phase_factor=math.sqrt(e/ee),method='First-orderthincoatingair-fringeenergyparticipationbound;notvalidatedEMmodel'))
 table('mask-sensitivity.csv',masks)
 # Reference-network comparisonwithallknownlumpedvaluespreserved.
 network=[]
 for f in[144e6,144.5e6,144.7e6,144.9e6,146e6]:
  om=2*math.pi*f
  def match(e3):
   kw={}if e3 else dict(w=1.102,h=.64,t=.07,er=4.3)
   lens=[LENGTHS[r]for r in['TL603','TL604','TL605']]if e3 else[6.23,6.62,5.8]
   return cascade(line(lens[0],f=f,**kw),shunt(1j*om*22e-12),series(1/(1j*om*330e-12)),line(lens[1],f=f,**kw),shunt(1j*om*22e-12),series(1j*om*47e-9),line(lens[2],f=f,**kw))
  load=3+1/(1j*om*80e-12);bias=1j*om*33e-9;load=load*bias/(load+bias)
  for label,m in[('E2',match(False)),('E3',match(True))]:
   zin=(m[0][0]*load+m[0][1])/(m[1][0]*load+m[1][1]);rl=-20*math.log10(abs((zin-50)/(zin+50)));network.append(dict(revision=label,MHz=f/1e6,assumed_intrinsic_gate='3ohmseries80pFparallel33nHbiasfeed',Zin_real=zin.real,Zin_imag=zin.imag,return_loss_dB=rl,status='ASSUMEDLOADNOTMEASUREDDEVICEIMPEDANCE'))
 table('input-match-comparison.csv',network)
 # New8mmSMA taper modeledas100shortquasi-staticsections.
 taper=[]
 for f in[144e6,144.7e6,146e6]:
  m=cascade(*[line(8/100,w=WIDTH+(1-WIDTH)*(i+.5)/100,f=f)for i in range(100)])
  den=m[0][0]+m[0][1]/50+m[1][0]*50+m[1][1];g=(m[0][0]+m[0][1]/50-m[1][0]*50-m[1][1])/den
  taper.append(dict(MHz=f/1e6,return_loss_dB_50ohm_planes=-20*math.log10(abs(g)),mismatch_loss_dB=-20*math.log10(abs(s21(m))),phase_deg=cmath.phase(s21(m))*180/math.pi,status='Losslessquasistaticsegmentedtaper;SMAvialaunchparasiticsomitted'))
 table('SMA-taper.csv',taper)
 filters=[]
 for f in[144e6,144.7e6,146e6,289.4e6,434.1e6]:
  om=2*math.pi*f
  def parallel_lc(l,cc):return 1/(1/(1j*om*l)+1j*om*cc)
  m=cascade(shunt(1j*om*22e-12),series(parallel_lc(39e-9,3.3e-12)),shunt(1j*om*27e-12),series(parallel_lc(22e-9,18e-12)),shunt(1j*om*22e-12),series(parallel_lc(27e-9,12e-12)),shunt(1j*om*15e-12))
  filters.append(dict(MHz=f/1e6,ideal_LPF_insertion_dB=-20*math.log10(abs(s21(m))),status='Originaltopologyvalues;ideallossless50ohmplanes,noSRF/Q/padparasitics'))
 table('LPF-reference-model.csv',filters)
 # Dielectricattenuationlow-lossquasiTEMandconductorlower-boundestimate.
 beta=2*math.pi*144.7e6*math.sqrt(ee)/299792458;ad=beta*ER/(2*(ER-1))*(ee-1)/ee*.02
 skin=math.sqrt(math.pi*144.7e6*4e-7*math.pi*1.724e-8);ac=skin/(50*WIDTH*.001)
 save('RF-analysis.json',dict(status='CALCULATED_NOT_MEASURED',nominal=dict(h_mm=H,copper_mm=T,Dk=ER,width_mm=WIDTH,Z0_ohm=z,effective_Dk=ee,length_factor=LENGTH_SCALE),Z0_sweep_ohm=[min(x['Z0_ohm']for x in sweep),max(x['Z0_ohm']for x in sweep)],dielectric_loss_dB_per100mm=ad*.1*8.686,conductor_lower_bound_dB_per100mm=ac*.1*8.686,mask=masks,selected_geometry='Conventionalmicrostripwithdeliberatetop-fillkeepout,continuousbottomRFreturn;noimpedancecontrol',GCPW_disposition='Notselected:wideconventionalmicrostripfits;GCPWwouldaddgap/fenceandcomponent-junctionconstraints. NoarbitraryGCPW50ohmclaim.',limitations=['HJfinite-thicknessquasistaticmodel;ordinaryFR4variationnotcontrolledimpedance','Groundedcomponentstubs,padsteps,PApackageandSMAinductancearenotqualifiedbythelinecalculation','Inputcomparisonloadisillustrative;notmanufacturer144MHzlarge-signaldata','LPFidealtransferisnotaharmonicmeasurement;actualcoilsQ/SRFandstubsrequireend-to-endalignment']))

def source_parasitics():
 rows=[]
 for w,l in[(.35,7.5),(.35,12.7),(.4,3.)]:
  for tag,h,t,er in[('E2',.64,.07,4.3),('E3',1.5,.035,4.5)]:
   z,e=microstrip(w,h,t,er);vel=299792458/math.sqrt(e);rows.append(dict(revision=tag,width_mm=w,length_mm=l,Z0_ohm=z,L_equivalent_nH=z/vel*l*.001*1e9,C_equivalent_pF=l*.001/(z*vel)*1e12,phase_at144p7MHz_deg=360*144.7e6*l*.001/vel,interpretation='Shortlumpedjunction/branchupperlength;notadesigned50ohmline. Totallengthcanincludeparallel/shuntstubs.'))
 table('source-and-stub-parasitics.csv',rows)
 # End-to-end sensitivity oftheknownsourcefilterincludingrepresentative
 # seriesjunctionlengths. AllL/Cvaluesareactualschematicvalues.
 results=[]
 for tag,h,t,er in[('E2',.64,.07,4.3),('E3',1.5,.035,4.5)]:
  for f in[144e6,144.7e6,146e6,289.4e6,434.1e6]:
   om=2*math.pi*f;stages=[series(1/(1j*om*100e-12))]
   for l,cc,ll in[(7.5,8.2e-12,56e-9),(7.5,33e-12,91e-9),(7.5,33e-12,56e-9)]:stages.extend([line(l,w=.35,h=h,t=t,er=er,f=f),shunt(1j*om*cc),series(1j*om*ll)])
   stages.extend([line(7.5,w=.35,h=h,t=t,er=er,f=f),shunt(1j*om*8.2e-12)])
   m=cascade(*stages);results.append(dict(revision=tag,MHz=f/1e6,insertion_dB=-20*math.log10(abs(s21(m))),scope='Approximateallseriesjunctionlengths;sourcebufferoutputR,branchstubs,coilQ/SRFandpadsomitted;notarealdrivebudgetmeasurement'))
 table('source-filter-layout-model.csv',results)

def power():
 # Reuse complete main-current pathconnectivitycheckwithoutputredirected.
 src=(ROOT/'tools/m5b_power_widths.py').read_text().replace("open('hardware/2m/review/M5B-E1/", "open('hardware/2m/review/M5B-E3/").replace('70um copper','35um copper;separatenative-resistanceanalysis')
 subprocess.run(['/usr/bin/python3','-c',src],cwd=ROOT,check=True);b=p.LoadBoard(str(HW/'RF2M.kicad_pcb'));rho=1.724e-8*(1+.00393*60);rows=[];totals=collections.defaultdict(lambda:dict(R=0,loss=0,drop=0,length=0,minw=10,maxrise=0))
 currents={'BAT_RAW':3.,'BAT_FUSED':3.,'VIN_PROT':3.,'VIN_CONV':3.,'VBOOST':2.,'VBUCK':2.,'VREG_RAW':2.,'VREG_SWITCH':2.,'VMOD':2.,'VPA':1.8}
 for t in b.GetTracks():
  if isinstance(t,p.PCB_VIA)or t.GetNetname()not in currents:continue
  w=p.ToMM(t.GetWidth());l=p.ToMM(t.GetLength())
  if w<.5 and l>2:continue # sensebranch;mainpathcheckaboveprovesitisnotrequiredforload.
  i=currents[t.GetNetname()];r=rho*l*.001/(w*.001*35e-6);area_mils=(w/.0254)*(.035/.0254);rise=(i/(.048*area_mils**.725))**(1/.44)
  row=dict(uuid=t.m_Uuid.AsString(),net=t.GetNetname(),layer=t.GetLayerName(),length_mm=l,width_mm=w,current_A_BOUND=i,R_at80C_ohm=r,drop_V=i*r,I2R_W=i*i*r,IPC2221_external_rise_C=rise,thermal='Empiricalestimateonly;shortnecksheatspreadintowidercopper,notisolatedtracks')
  rows.append(row);z=totals[t.GetNetname()];z['R']+=r;z['loss']+=i*i*r;z['drop']+=i*r;z['length']+=l;z['minw']=min(z['minw'],w);z['maxrise']=max(z['maxrise'],rise)
 table('power-native-segments.csv',rows);table('power-native-net-bounds.csv',[dict(net=n,current_A_BOUND=currents[n],**z)for n,z in totals.items()])
 save('power-analysis.json',dict(status='CALCULATED_NOT_MEASURED',copper_um=35,resistivity_80C_ohm_m=rho,net_bounds={n:dict(current_A=currents[n],**z)for n,z in totals.items()},method='Sumallwide/shortnecktrackresistancespernet;thisovercountsparallel/unloadedbranchesandboundsaresistivepathbecauseindependentwidepathconnectivitypasses. Fullboundcurrentisassignedtoeacheligiblesegment. Thinlongsensebranchesexcludedonlyfromloadmodel,notDRC.',ground_return_model=dict(effective_length_mm=150,effective_width_mm=10,copper_um=35,R_at80C_ohm=rho*.15/(.010*35e-6),I2R_at2A_W=4*rho*.15/(.010*35e-6),qualification='Conservativegeometryallowance;nativeGNDzonecontinuitychecked. Currentdistribution/neckspreadingnotafield-solvedresult.'),via_electrical=dict(length_mm=1.6,drill_mm=.3,plating_um=18,R_80C_each_ohm=rho*.0016/(math.pi*.0003*18e-6)),R309_shunt_W_at2A=4*.068,R413_W_at180mA=.18**2*4.7,qualification='SupplydroopandtemperatureunderactualAMloadNOT_RUN;commissionfirstatboundedcurrent,nounrestrictedLiionfaulttest.'))

def thermal():
 k=385;rows=[]
 for thickness,count,plate in itertools.product([.8,1.6],[12,32],[10,15,18,25]):
  rv=thickness*.001/(k*math.pi*.0003*plate*1e-6*count)
  for loss in[2.,3.7,4.,5.]:
   rt=3+rv+2+1+3.5;rows.append(dict(PCB_mm=thickness,vias=count,barrel_um=plate,PA_heat_W=loss,barrel_parallel_K_per_W=rv,assumed_total_JA_K_per_W=rt,junction_at40C_C=40+loss*rt,status='BARREL_ONLY_MODEL_NO_SOLDER_FILL_CREDIT;NOT_RUN'))
 table('thermal-via-sensitivity.csv',rows)
 vals={}
 for plate in[10,15,18,25]:vals[str(plate)]=.0016/(k*math.pi*.0003*plate*1e-6*32)
 # PAaverageRFat1WERP,-1dBd,.75dBfilterloss,80percentAM.
 rfavg=10**.175*(1+.8**2/2);heat={str(eta):rfavg*(1/eta-1)for eta in[.3,.35,.4,.5]}
 # TrueRF AMdoesnotfollowvoltagebydefinition;retainE2operatingpointmodel.
 ntc=1/(1/298.15+math.log(10/49.9)/3977)-273.15
 save('thermal-mechanical.json',dict(status='ANALYTIC_AND_DIMENSIONAL_REVIEW_ONLY',source_array=dict(count=32,land_mm=.8,drill_mm=.3,pitch_mm=.6,rows=8,columns=4,PCB_mm=1.6,barrel_K_per_W_by_plating_um=vals,source_copper_mm=[2.7,5],bottom_window_mm=[14,12],source_mask='0.4mmsquaremaskcapsoverholes;ordinarytentingisnotplugging. Openbottomvias. Sourcepastegridreduced25umperedge.',minimum_barrel_scenario_um=10,claim='Noassuranceofminimumbarrelplatingfrompublished18umaverage;measurethermalpath. No solder-fillcredit.'),PA_RF_average_model_W=rfavg,PA_heat_model_by_efficiency=heat,assumed_other_thermal_K_per_W=dict(junction_to_case=3,spreading_and_contact=2,TIM=1,sink=3.5),qualification_heat_budget_W=4,engineering_Tj_limit_C=125,ambient_design_C=40,NTC_nominal_trip_C=ntc,pass_device=dict(RthJC=2.5,sink_max_K_per_W=3.5,interface_K_per_W=1,case_acceptance_C=60,NTC='Bondinsulatedbeadtolivepasscase;do notraisetrip. Mechanicaldetachmentwithintactwireisnotdetected.',insulation='ST D45H11 pin2/tabVPA andSTBD139pin2/tabMOD_SINKarelive. Separateinsulatedsinks/shoulderwashers;no baremetalconnectiontogroundedPAspreader.'),mechanical=dict(outline_mm=[180,140],spreader_mm=[16,44,8],window_coordinates_mm=[105,49,119,61],spreader_holes_mm=[[112,32],[112,68]],corner_standoffs_mm=40,sink_below_spreader_mm=20,minimum_bottom_lead_clearance_mm=5,maximum_trimmed_leads_mm=2.5,thickness_change_mm=.8,fixture='Adjustclampingstackby+0.8mm;no1.6mmboardbendingloadonQ501. 0.15-0.25mmTIMk>=3W/mK,>=100Vinsulation,groundstrapindependentofTIM.'),qualification='At18umaveragebarrelmodel4Wheatpredicts~109Cjunction. At10um4Wexceeds125C;thisisameasuredthermalgate,notaminimumplatingrequest. Stagewithreducedenergy;stopifcase60C/passlimit,PAcalculatedTj125C or4Wheatbudgetexceeded. Do not rely on dutycycletohidecontinuousfaultheat.',all_hardware_tests='NOT_RUN'))

def cost():
 # Transparentallowances,notquotes:boardarea0.0252m2 + ordinarysetup.
 rows=[]
 for q in[5,10,20]:
  # Engineeringbudgetrate250..500EUR/m2 plus10..20batchsetup.
  area=.180*.140;lo=10+250*area*q;hi=20+500*area*q
  rows.append(dict(boards=q,width_mm=180,height_mm=140,area_m2_each=area,E3_bare_batch_low_EUR=lo,E3_bare_batch_high_EUR=hi,E3_each_low_EUR=lo/q,E3_each_high_EUR=hi/q,shipping_separate_EUR_low=10,shipping_separate_EUR_high=25,VAT='excluded',basis='Unquotedsupplier-neutralbudget10-20setup+250-500EUR/m2;NOTJLCpublishedpriceorquote'))
 table('PCB-cost-estimate.csv',rows);save('manufacturing-cost.json',dict(status='ESTIMATE_NOT_QUOTATION',standard_options=dict(layers=2,thickness_mm=1.6,copper_oz=1,mask='green',legend='white',finish='lead-freeHASL',impedance_control=False,special_process=False),estimates=rows,E2_five_board_estimate_EUR=[60,100],E2_confirmation_dependencies='0.8mmcore0.64+-0.05/70umfinished/.15mmfeatures;superseded',interpretation='E3standardconfigurationremovesnegotiatedstack/processdependencies;nosavingbookeduntilactualautomatedquote. BoardarearetainedforRFreturn,separateportsandtwothermalassemblies.',actual_quote=None,factory_CAM_acceptance=None,submitted_files=False))
def main():
 rf();source_parasitics();power();thermal();cost()
 fn=OUT/'costs.json'
 if fn.exists():
  material=json.loads(fn.read_text());old=material['external'];material['historical_E2_external_estimates']={k:v for k,v in json.loads((HW/'review/M5B-E2/costs.json').read_text())['external'].items()if k.startswith(('evaluation_PCB','production_bare_PCB'))}
  material['external']={k:v for k,v in old.items()if not k.startswith(('evaluation_PCB','production_bare_PCB'))};material['external']['E3_bare_PCB_estimates']='See manufacturing-cost.json / PCB-cost-estimate.csv;unquotedstandard-processbudgetfor5/10/20,notcommercialpricing';save('costs.json',material)

 import m5b_e3_power_paths;m5b_e3_power_paths.main()
 print('E3 RF,power,thermalandcostcalculationswritten;physicalNOT_RUN')
if __name__=='__main__':main()
