"""Independent native output-capacitor kill-tail check; not a full PA model."""
import re,subprocess,math
from m5b_e6r1_common import *

def main():
    guard();d=OUT/'simulation';d.mkdir(exist_ok=True)
    deck='''* E6R1 native VPA passive tail after independent hard clamp/clock kill
* Pass and RF sources removed. This checks only remaining native stored energy.
C506 vpa 0 100n IC=7.2
C634 vpa 0 330p IC=7.2
R513 vpa 0 1k
R511 vpa fb 18k
R512 fb 0 10k
.control
tran 0.5u 2m uic
let dissipated_power=v(vpa)*v(vpa)*(1/1000+1/28000)
meas tran fall_to_100mV WHEN v(vpa)=0.1 FALL=1
meas tran released_energy INTEG dissipated_power FROM=0 TO=0.002
quit
.endc
.end
'''
    (d/'native-kill-tail.cir').write_text(deck)
    run=subprocess.run(['ngspice','-b',str(d/'native-kill-tail.cir')],capture_output=True,text=True)
    (d/'ngspice.log').write_text(run.stdout+run.stderr);assert run.returncode==0
    fall=float(re.search(r'fall_to_100mv\s*=\s*([\deE+.-]+)',run.stdout,re.I).group(1))
    energy=float(re.search(r'released_energy\s*=\s*([\deE+.-]+)',run.stdout,re.I).group(1))
    analytical=.10033e-6/(1/1000+1/28000)*math.log(72)
    initial=.5*.10033e-6*7.2**2
    assert abs(fall/analytical-1)<.01 and abs(energy/initial-1)<.01
    save('spice-tail-result.json',dict(ngspice_returncode=run.returncode,fall_to_0p1V_s=fall,
        analytical_s=analytical,released_J=energy,initial_stored_J=initial,
        limitation='Passive output capacitance only. Not a modulator stability, converter startup, RF leakage or junction qualification.',physical='NOT_RUN'))
    print('ngspice passive tail PASS',fall,energy)

if __name__=='__main__':main()
