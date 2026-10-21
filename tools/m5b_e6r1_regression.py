"""Re-execute the E6 failure using frozen sources, never their output writers."""
import numpy as np
from m5b_e6r1_common import *
from m5b_e6_power import operating
from m5b_e6_thermal import Network,NAMES,powers,run_cycle,schedule
from m5b_e6_faults import absorbed
from m5b_e6_stress import audio

def failure():
    source_R=11.846896331207134
    n=Network(source_R=source_R)
    mark=operating(1.,eta=.4,waveform=True,phases=256)
    space=operating(1.,eta=.4,tone=False)
    fault=absorbed(mark,1.)
    q={'mark':powers(fault['mean']),'space':powers(absorbed(space,1.)['mean']),'off':np.zeros(len(NAMES))}
    result,_,_=run_cycle(n,schedule(60,300,'MO5'),q)
    ripple=audio(n,fault,256)['positive_ripple_C']['PA_junction']
    peak=result['periodic_max_C']['PA_junction']+ripple
    historical=json.loads((HW/'review/M5B-E6/native-fault-envelope.json').read_text())['operating_efficiency_sweep']
    old=next(z for z in historical if z['eta_carrier_assumed']==.4 and abs(z['source_to_bar_K_W']-source_R)<1e-8 and z['capacity_scale']==1 and z['absorbed_fraction']==1)
    assert abs(peak-old['PA_peak_with_audio_C'])<1e-8
    return dict(architecture='Original E6 A with DD1SB, not corrected R1A',source_to_bar_K_W=source_R,
        PA_peak_with_audio_C=peak,pass_case_C=result['periodic_max_C']['pass_case'],NTC_C=result['periodic_max_C']['NTC'],
        rail_peak_A=mark['maximum']['regulated_current_A'],nominal_trip_A=1.797,
        historical_difference_C=peak-old['PA_peak_with_audio_C'],limits_not_relaxed=True,physical='NOT_RUN')

if __name__=='__main__':
    guard();z=failure();save('E6-failure-reproduction.json',z);print(json.dumps(z,indent=2))
