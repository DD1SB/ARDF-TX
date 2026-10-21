"""Record actual run results; successful execution does not grant engineering GO."""
import datetime,platform,re,sys
from importlib.metadata import version
from m5b_e6r1_common import *

def main():
    guard();logs=OUT/'logs';counts={}
    for name,expected in [('E6',25),('R1',37)]:
        log=(logs/f'reproduction-{name}-tests.log').read_text()
        count=int(re.search(r'Ran (\d+) tests',log).group(1))
        assert count==expected and '\nOK\n' in log and '\nFAILED' not in log
        counts[name]=dict(tests=count,passed=True,raw_log=f'logs/reproduction-{name}-tests.log')
    thermal=json.loads((OUT/'thermal-results.json').read_text());sensor=json.loads((OUT/'sensor-fault-results.json').read_text())
    electrical=json.loads((OUT/'electrical-model.json').read_text());system=json.loads((OUT/'system-power.json').read_text())
    run=lambda args:subprocess.check_output(args,cwd=ROOT,text=True).strip()
    save('execution-results.json',dict(executed=datetime.datetime.now().astimezone().isoformat(),starting_commit=START,
        branch=run(['git','branch','--show-current']),analysis_parent_HEAD=run(['git','rev-parse','HEAD']),
        host=platform.platform(),python=sys.version,kicad=run(['kicad-cli','version']),
        ngspice=run(['ngspice','--version']).splitlines()[1],
        numerical_versions={k:version(k) for k in ['numpy','scipy','matplotlib']},tests=counts,
        normal_thermal_rows=len(thermal['rows']),thermal_sensitivity_rows=len(thermal['sensitivities']),
        sensor_fault_cases=len(sensor['cases']),healthy_sensor_cases=len(sensor['healthy_threshold_headroom']),
        linear_loop_cases=len(electrical['cases']),linear_loop_stable=sum(z['stable'] for z in electrical['cases']),
        system_power_scenarios=len(system['rows']),
        starting_files_unchanged=len(json.loads((OUT/'preserved-start.json').read_text())),
        source_guard='PASS except explicitly permitted README.md/docs/README.md index updates',
        ERC_DRC='NOT_RERUN; native CAD unchanged, previous E6/E5 evidence preserved',
        disposition='HOLD_FOR_NATIVE_PCB_IMPLEMENTATION',physical='NOT_RUN',
        fabrication='NOT_CREATED',publication='NO_PUSH_NO_TAG'))
    print('Actual execution evidence recorded; HOLD for native PCB implementation')

if __name__=='__main__':main()
