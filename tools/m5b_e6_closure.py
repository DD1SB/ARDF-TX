"""Bound the local thermal-path requirement; do not certify unmeasured RF faults."""
import numpy as np
from m5b_e6_common import *
from m5b_e6_power import operating
from m5b_e6_thermal import Network,NAMES,run_cycle,powers,schedule
from m5b_e6_stress import audio
from m5b_e6_faults import absorbed


def calculate(r,split,cap,ceiling=125):
    n=Network(source_R=r,source_split=split,capacity_scale=cap)
    z=absorbed(operating(1.,eta=.4,waveform=True,phases=256),1.)
    s=absorbed(operating(1.,eta=.4,tone=False),1.)
    q={'mark':powers(z['mean']),'space':powers(s['mean']),'off':np.zeros(len(NAMES))}
    out,_,_=run_cycle(n,schedule(60,300,'MO5'),q)
    peak=out['periodic_max_C']['PA_junction']+audio(n,z,256)['positive_ripple_C']['PA_junction']
    return dict(source_to_bar_K_W=r,split=split,capacity_scale=cap,PA_peak_C=peak,
                pass_case_C=out['periodic_max_C']['pass_case'],NTC_C=out['periodic_max_C']['NTC'],
                design_limit_C=ceiling,meets_limit=peak<=ceiling)


def main():
    guard();rows=[];required=[]
    for split in [.2,.6,.9]:
        for cap in [.1,1.,3.]:
            rows.append(calculate(11.846896331207134,split,cap))
    for cap in [.1,1.,3.]:
        for ceiling in [110,125]:
            lo,hi=1.,20.
            for i in range(12):
                mid=(lo+hi)/2
                if calculate(mid,.6,cap,ceiling)['meets_limit']:lo=mid
                else:hi=mid
            required.append(dict(capacity_scale=cap,PA_limit_C=ceiling,source_to_bar_required_max_K_W=lo,
                bisection_width_K_W=hi-lo,assumption='Same-point full RF absorption sensitivity,40% carrier efficiency,40C,5.5K/W,Classic MO5; not an RF load-pull prediction'))
    save('thermal-path-closure.json',dict(disposition='HOLD_BEFORE_CAD',FVM_split_sensitivity=rows,
        required_source_path=required,physical='NOT_RUN',
        limits='This envelope shows why a qualified source/contact/loss bound or justified fast fault interruption is needed. It does not prove every single-heatsink architecture infeasible.',
        next_closure=['Establish manufacturer-supported or conservative RF loss/current envelope at144MHz andnative4V centre/7.2Vcrest',
            'Demonstrate an ordinary-fabrication source joint/via/interface resistance and transient bound that meets110Ctarget/125Cceiling',
            'If those bounds require it, propose a separately justified PA-specific fault interruption change without raising thresholds',
            'Then finalize common mounting hardware, native slots, copper clearance, zero-warning CAD and fabrication data']))
    print('HOLD: source-path closure not established. Calculated requirements',required)


if __name__=='__main__':main()
