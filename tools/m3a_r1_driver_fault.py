#!/usr/bin/env python3
"""Linear passive ngspice sensitivity from RF80 R410/C401/C402/C404.

The interruption is imposed, NOT a simulated comparator/load-switch guarantee.
No transistor model, RF measurements or physical safe-operating-area validation.
"""
import argparse,csv,json,subprocess,tempfile
from pathlib import Path
from m3a_r1_logic import number
ROOT=Path(__file__).resolve().parents[1]
def run():
    m={p['ref']:p for p in json.loads((ROOT/'hardware/80m/RF80.electrical.json').read_text())['parts']}
    assert m['R410']['pins']=={'1':'VPA_LOAD','2':'VDRV'}
    assert all(m[r]['pins']=={'1':'VDRV','2':'GND'}for r in ('C401','C402','C404'))
    rr=number(m['R410']['value'])*.99;cb=number(m['C404']['value'])*.8
    cf=sum(number(m[r]['value'])for r in ('C401','C402'))*.8
    cases=[];saved=None
    for vin,off,esr,label in [(16.8,20,.5,'pack-step'),(28.,20,.5,'28V-surrogate-OUTSIDE-SYSTEM-RATING'),(28.,50,.5,'slow-isolation-NO-GO'),(28.,20,1.5,'excess-ESR-NO-GO')]:
        text=f'''RF80 R1 linear driver rail failure sensitivity: {label}
VPA VPA_LOAD 0 PWL(0 8.6 1u 8.6 1.0001u {vin} {1+off}u {vin} {1+off+.0001}u 0)
R410 VPA_LOAD VDRV {rr}
C_HF VDRV 0 {cf}
R_ESR VDRV BULK {esr}
C404 BULK 0 {cb}
.control
set wr_singlescale
set wr_vecnames
tran 0.02u 150u
wrdata result.dat v(VDRV) i(VPA)
quit
.endc
.end
'''
        with tempfile.TemporaryDirectory(prefix='ardf-r1-spice-')as d:
            d=Path(d);p=d/'fault.cir';p.write_text(text)
            r=subprocess.run(['ngspice','-b',str(p)],cwd=d,capture_output=True,text=True)
            assert r.returncode==0,(r.stdout,r.stderr)
            data=[]
            for line in (d/'result.dat').read_text().splitlines()[1:]:
                vals=list(map(float,line.split()));data.append(vals)
            peak=max(x[1]for x in data);energy=sum(((a[2]**2+b[2]**2)/2)*rr*(b[0]-a[0])for a,b in zip(data,data[1:]))
            case=dict(label=label,within_load_switch_operating_range=vin<=18.0,input_step_v=vin,imposed_isolation_us=off,bulk_esr_assumed_ohm=esr,peak_driver_v=peak,within_12_6V=peak<=12.6,resistor_total_pulse_energy_j=energy)
            cases.append(case)
            if label=='28V-surrogate-OUTSIDE-SYSTEM-RATING':saved=(text,data)
    assert cases[0]['within_12_6V']and cases[1]['within_12_6V']
    assert not cases[2]['within_12_6V']and not cases[3]['within_12_6V']
    result=dict(date='2026-10-14',revision='M3A-R1',classification='ACTUAL NGSPICE LINEAR-PASSIVE SIMULATION; IMPOSED ISOLATION; NOT MEASURED',series_R_min_ohm=rr,bulk_C_min_f=cb,HF_C_min_f=cf,cases=cases,limitations=['Switch/comparator/gate timing imposed20us, not proven','28V is isolated passive stress only: TPS22810 operating18V/absolute20V; not valid system stimulus or protection proof','Capacitor ESR over0-50C must be measured; high ESR fails','R410 pulse energy/thermal derating and actual charge/discharge path remain open','RF gate voltage, PA power/efficiency, key edges and emissions not simulated'])
    return result,saved
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');a=ap.parse_args();r,(c,data)=run()
    ss=json.dumps(r,indent=2)+'\n';p=ROOT/'docs/M3A_R1_DRIVER_SIMULATION.json'
    if a.write:
        p.write_text(ss);(ROOT/'analysis/m3a_r1_driver_fault.cir').write_text(c)
        with (ROOT/'analysis/m3a_r1_driver_fault.csv').open('w')as f:
            w=csv.writer(f,lineterminator='\n');w.writerow(['time_s','driver_V','source_A']);w.writerows(data)
    else:assert p.read_text()==ss,'Stale driver sensitivity report'
    print('PASS: bounded20us cases;',[(x['label'],round(x['peak_driver_v'],3),x['within_12_6V'])for x in r['cases']])
