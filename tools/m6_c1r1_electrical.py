#!/usr/bin/python3
"""Native-net checks and bounded DC/RC calculations. No physical qualification."""
import json,math,itertools,hashlib,subprocess,copy,sys
from pathlib import Path
import pcbnew as p
ROOT=Path(__file__).resolve().parents[1];P=ROOT/'hardware/controller';D=P/'review/M6-C1R1'
def save(name,data):(D/name).write_text(json.dumps(data,indent=2)+'\n')
def ohm(v):return float(v[:-1])*{'k':1000,'M':1e6}.get(v[-1],1) if v[-1] in 'kM' else float(v)
def network(vb=14,rid=22000,raw=None,on=True,vf=.65,leak=0,rs=27000,ri=180000,rd=33000,ra=100000,negative_vf=.24):
    """Two-node resistive solve; diode VF/leak are explicit bounded inputs."""
    gd=1/rd+(1/ra if on else 0);ge=0 if rid is None else 1/rid if rid else 1e9
    vs=max(0,vb-vf)
    if raw is not None:
        v=(raw/ri-leak)/(1/ri+gd);u=raw
    else:
        g1=1/rs+ge+1/ri;g2=1/ri+gd;det=g1*g2-1/ri**2
        u=(vs/rs*g2-leak/ri)/det;v=(vs/rs/ri-leak*g1)/det
    if v< -negative_vf:v=-negative_vf
    return dict(J1_3_V=u,TMUX_5_V=v,ESP_ADC_V=v if on else None,R8_current_A=(u-v)/ri,R8_power_W=(u-v)**2/ri,R9_current_A=v/rd,R9_power_W=v*v/rd,R19_current_A=v/ra if on else 0,R19_power_W=v*v/ra if on else 0,R3_current_A=max(0,(vs-u)/rs),R3_power_W=max(0,vs-u)**2/rs,diode_excitation_reverse_A=80e-9 if u>vb else 0,D22_forward_current_A=max(0,(vs-u)/rs),D23_forward_current_A=max(0,(v-u)/ri+v*gd+leak) if v<0 else 0)
def recognition_bounds(vb,rid,cal):
    vals=[]
    for vbb,vf,leak,rs,ri,rd,ra,re in itertools.product([vb-cal['sense_error_V'],vb+cal['sense_error_V']],cal['vf_bounds_V'],[0,cal['leak_max_A']],[.983,1.017],[.983,1.017],[.983,1.017],[.983,1.017],[.983,1.017]):
        v=network(vb=vbb,rid=rid*re,vf=vf,leak=leak,rs=27000*rs,ri=180000*ri,rd=33000*rd,ra=100000*ra)['TMUX_5_V'];vals.extend([v-cal['adc_error_V'],v+cal['adc_error_V']])
    return min(vals),max(vals)
def pincheck(b):
    n={f.GetReference():{a.GetNumber():a.GetNetname() for a in f.Pads()} for f in b.GetFootprints()};v={f.GetReference():f.GetValue() for f in b.GetFootprints()};errors=[]
    expected={'J1':{'1':'PACK_RAW','2':'GND','3':'PACK_ID_RAW'},'R3':{'1':'PACK_ID_EXC','2':'PACK_ID_RAW'},'D22':{'1':'PACK_PROT','2':'unconnected-(D22-2_NC-Pad2)','3':'PACK_ID_EXC'},'R8':{'1':'PACK_ID_RAW','2':'PACK_ID_SAFE'},'R9':{'1':'PACK_ID_SAFE','2':'GND'},'R19':{'1':'PACK_ID_ADC','2':'GND'},'D23':{'1':'PACK_ID_SAFE','2':'GND'},'C25':{'1':'PACK_ID_SAFE','2':'GND'},'U21':{'5':'PACK_ID_SAFE','6':'PACK_ID_ADC','7':'GND','14':'V3V3'},'U3':{'1':'USB_DP_CONN','2':'GND','3':'USB_DM_CONN','4':'USB_DM_CONN','5':'V3V3','6':'USB_DP_CONN'},'C10':{'1':'V3V3','2':'GND'}}
    for r,pp in expected.items():
        for pin,net in pp.items():
            if n.get(r,{}).get(pin)!=net:errors.append(r+'.'+pin+':'+net)
    for r,val in [('R3','27k'),('R8','180k'),('R9','33k'),('R19','100k')]:
        if v.get(r)!=val:errors.append(r+':value')
    for r in ['R3','R8','R9','R19','D22','D23']:
        fp=next(f for f in b.GetFootprints() if f.GetReference()==r)
        if not any(x.GetName()=='Population' and x.GetText()=='ALL' for x in fp.GetFields()):errors.append(r+':must_fit_all_base_variants')
    fs={f.GetReference():f for f in b.GetFootprints()}
    for r,mpn in [('D22','BAS116,235'),('D23','BAT54H,115')]:
        if not any(x.GetName()=='MPN' and x.GetText()==mpn for x in fs[r].GetFields()):errors.append(r+':MPN')
    return errors

def main():
    b=p.LoadBoard(str(P/'CTRL.kicad_pcb'));assert not pincheck(b),pincheck(b)
    cases=[]
    for name,vb,rid,raw in [('correct_2S',7,10000,None),('correct_4S',14,22000,None),('ID_open',14,None,None),('ID_ground',14,0,None),('ID_to_8p4V',7,None,8.4),('ID_to_16p8V',16,None,16.8),('ID_negative_16p8V',0,None,-16.8),('USB_only_pack_absent',.5008,None,None),('reverse_pack',0,10000,None)]:
        for on in [False,True]:
            z=network(vb,rid,raw,on);cases.append(dict(case=name,U21_powered=on,PACK_PROT_V=vb,ESP_off_interval_V=None if on else ([-.29,.204] if raw is not None and raw<0 else [-.204,.204]),off_interval_basis='negative clamp engineering sensitivity, not IPOFF guarantee' if raw is not None and raw<0 else 'TI IPOFF2uA atVDD0 timesR19 tolerance',**z))
    worst=[]
    for on in [False,True]:
        vv=[];power=[]
        for a,c,e,leak in itertools.product([.983,1.017],[.983,1.017],[.983,1.017],[-.25e-6,.25e-6] if on else [-2e-6,2e-6]):
            z=network(raw=16.8,on=on,ri=180000*a,rd=33000*c,ra=100000*e,leak=leak);vv.append(z['TMUX_5_V']);power.append(z['R8_power_W'])
        worst.append(dict(powered=on,TMUX_5_max_V=max(vv),R8_max_W=max(power)))
    assert max(x['TMUX_5_max_V'] for x in worst)<3.0
    assert max(x['R8_max_W'] for x in worst)<.01
    max_neg=(16.8-.24)/(180000*.983);assert max_neg<.0001
    # Calibrated engineering fixture. These bounds are commissioning criteria,
    # not unstated manufacturer guarantees for a diode at every temperature.
    cal={'vf_bounds_V':[.4,1.0],'leak_max_A':.2e-6,'adc_error_V':.01,'sense_error_V':.10}
    full={'vf_bounds_V':[0,1.25],'leak_max_A':2e-6,'adc_error_V':.01,'sense_error_V':.10}
    margins=[]
    for vb in [5.21,7,8.3,11.21,14,16.7]:
        a=recognition_bounds(vb,10000,cal);c=recognition_bounds(vb,22000,cal);assert a[1]<c[0],(vb,a,c)
        margins.append(dict(PACK_PROT_V=vb,ID_10k_V=a,ID_22k_V=c,separation_V=c[0]-a[1],full_unqualified_10k=recognition_bounds(vb,10000,full),full_unqualified_22k=recognition_bounds(vb,22000,full)))
    offmax=2e-6*100000*1.017
    negative_R3_max_W=(16.8+16.8)**2/(27000*.983)
    assert negative_R3_max_W < .1*(155-85)/(155-70)
    for name,value in [('CTL_PACK_ID_PULLUP_OHM',27000),('CTL_PACK_ID_ADC_ATTEN_MILLI_DB',2500),('CTL_PACK_ID_ADC_VALID_MAX_MV',930)]:
        assert '#define '+name+' '+str(value) in (ROOT/'firmware/controller_hw/pins.h').read_text(),name
    save('input-protection.json',{'classification':'BOUNDED CALCULATIONS; physical tests NOT_RUN','native_sha256':hashlib.sha256((P/'CTRL.kicad_pcb').read_bytes()).hexdigest(),'normal_cases':cases,'positive_fault_worst':worst,'resistor_corner_basis':'1.7%=1% initial plus100ppm/K*65K rounded outward; conditional-40..85C controller envelope. External ID resistor must meet equivalent tolerance/TCR.','positive_fault_leak_basis':'Off +/-2uA input leakage sensitivity from TI IPOFF magnitude atVDD0. On +/-0.25uA engineering envelope includes ON leakage/ADC/board uncertainties; diode reverse leakage alone only lowers positive voltage. Resistor-only bounds remain2.647114V off/2.071290V on at initial1% only. Neither envelope is a transient qualification.','fault_definition':'Continuous ID conductor shorts to0,+8.4,+16.8,-16.8V referenced to controller GND; arbitrary connector permutations/ground loss are not guaranteed. Upstream pack protection/fusing remains required.','TMUX_ratings':{'recommended_powered':'0..min(2*VDD,5.5)V','recommended_VDD_below1p5':'0..3.6V','signal_absolute_V':[-.5,6],'IPO_off_max_A':2e-6},'ESP_unpowered_ADC_bound_V':offmax,'negative_fault':{'D23_MPN':'BAT54H,115','maximum_current_A':max_neg,'R3_max_fault_W_conservative_no_diode_drop':negative_R3_max_W,'R3_voltage_upper_V':33.6,'R3_allowance_W_at85C':.1*(155-85)/(155-70),'manufacturer_VF_max_25C_at100uA_V':.24,'cold_sensitivity_V':.29,'ESP_absolute_lower_V':-.3,'TMUX_absolute_lower_V':-.5,'limitation':'25C pulsed VF rating, not guaranteed continuous full-temperature clamp. Qualify negative miswire current/voltage across intended temperature before operational use; never apply unqualified fault with MCU fitted.'},'negative_unpowered_PACK_PROT_sensitivity':{'cause':'D22/R3 can pull an otherwise unpowered PACK_PROT negative; existing unidirectional D2 then conducts forward. Normal-case ideal source rows do not bound this coupling.','assumed_D2_forward_V':1.0,'BAT_DIV_V':-1/11,'Q1_base_V':-.5,'manufacturer_guarantee':'NOT_ESTABLISHED at this small current/temperature','qualification':'Measure PACK_PROT,BAT_ADC andPACK_ID_ADC during negative fault before fitting U21/U10. No RF permission for this state.'},'backfeed':{'V3V3_resistive_path':'NONE; R3 excitation moved fromV3V3 toPACK_PROT throughD22','D22_max_hot_reverse_A':80e-9,'PACK_PROT_USB_upper_V_with_D4_50uA':.5008,'Q1_base_upper_V':.2504,'U21_ADC_off_leak_max_V':offmax,'RF_ports':'No changes; Ioff digital buffers/TMUX/local RF gating retained.'},'recognition_calibration_required':cal,'unqualified_component_envelope':full,'recognition_margins':margins,'warning':'Full uncalibrated diode/ADC envelope can overlap identities. Reader must reject ambiguous/missing qualification, not force nearest code. Physical ID/ADC/leakage calibration is a Gate D prerequisite, not an achieved measurement. External10k/22k protocol and J1 pinout unchanged; raw-ID normal bias is explicitly changed.','ADC_policy':{'attenuation_dB':2.5,'datasheet_effective_range_V':[0,1.1],'valid_ID_V':[0,.93],'reject_saturation':True,'basis':'ESP32-S3 datasheet v2.2 table5-6 ATTEN1: +/-6mV after calibration at25C with100nF/WiFi off. Total10mV and100mV PACK_PROT allowances require commissioning qualification across actual temperature; not guaranteed here.'},'settling':{'C25_F':1e-7,'max_Thevenin_ohm_bound':33000*1.017,'9tau_upper_s':9*33000*1.017*1.2e-7,'policy':'Wait>=40ms after stable pack/logic or ID transition; require repeated consistent fresh samples before INIT_OK. Revalidate every meaningful progress commit; invalid sample withdraws INIT_OK/ARM and latches fault.'}})
    # Numerical and actual pad-net negative tests, none saved over the candidate.
    tests=[];fs={f.GetReference():f for f in b.GetFootprints()}
    for name,r,pin,net in [('missing_series_protection','R8','2','PACK_ID_RAW'),('missing_shunt','R9','2','PACK_ID_EXC'),('unsafe_excitation_rail','R3','1','V3V3'),('fault_bypasses_switch','U21','5','PACK_ID_RAW'),('wrong_USB_ESD_rail','U3','5','USB_VBUS'),('wrong_USB_ground','U3','2','V3V3'),('RF80_connector_modified','J4','3','RF80_SDA'),('ID_excitation_reverse_path','D22','1','PACK_ID_EXC'),('negative_clamp_wrong_ground','D23','2','V3V3'),('unpowered_ADC_shunt_removed','R19','2','PACK_ID_EXC')]:
        pad=next(a for a in fs[r].Pads() if a.GetNumber()==pin);old=pad.GetNet();pad.SetNet(b.FindNet(net));e=pincheck(b)
        if r=='J4':
            import m6_c1r1 as wrapper
            m=wrapper.adapted('m6_c1_verify',[("'5':'PACK_ID_RAW','6':'PACK_ID_ADC'","'5':'PACK_ID_SAFE','6':'PACK_ID_ADC'")]);e=m.verify(b)[0]
        pad.SetNet(old);assert e,name;tests.append(dict(mutation=name,detected=e))
    field=next(x for x in fs['R8'].GetFields() if x.GetName()=='Population');old=field.GetText();field.SetText('RF2M');e=pincheck(b);field.SetText(old);assert e;tests.append(dict(mutation='protection_omitted_in_FOX_variant',detected=e))
    for name,kw in [('series_short',{'ri':1}),('shunt_open',{'rd':1e99}),('wrong_divider',{'ri':1000})]:
        z=network(raw=16.8,on=False,**kw);assert z['TMUX_5_V']>3.6;tests.append(dict(mutation=name,violating_voltage=z['TMUX_5_V']))
    for name,kw in [('unpowered_ID_fault',{'on':False}),('powered_ID_fault',{'on':True})]:
        z=network(raw=16.8,**kw);assert z['TMUX_5_V']<3.0;tests.append(dict(safe_fault=name,voltage=z['TMUX_5_V']))
    save('protection-regression.json',{'status':'PASS','native_and_numeric_checks':tests,'physical':'NOT_RUN'})
    print('Protection model PASS',worst,'minimum calibrated ID gap',min(x['separation_V'] for x in margins))
if __name__=='__main__':main()
