#!/usr/bin/python3
"""Run preserved-version suites without overwriting historical review ledgers.

An old suite passing on its own revision is historical reproducibility only;
E2 manufacturer tests deliberately reject the faulty E1 Q403/U311.
"""
import io,json,os,subprocess,tarfile,tempfile
from pathlib import Path
R=Path(__file__).resolve().parents[1];D=R/'hardware/80m/review/M3B-E2'
def main():
    results=[]
    jobs={
      '0dfd224':['m3_80m_checks.py','m3a_r1_logic.py','m3a_r1_driver_fault.py','m3a_r1_report.py','m3a_r1_documentation.py'],
      'm3b-e1':['m3b_verify.py','m3b_documentation.py']}
    for revision,scripts in jobs.items():
        with tempfile.TemporaryDirectory(prefix='rf80-regression-')as tmp:
            data=subprocess.check_output(['git','archive',revision],cwd=R)
            with tarfile.open(fileobj=io.BytesIO(data))as archive:archive.extractall(tmp,filter='data')
            env=os.environ.copy();env['GIT_DIR']=str(R/'.git');env['GIT_WORK_TREE']=tmp
            for script in scripts:
                cmd=['/usr/bin/python3','tools/'+script];r=subprocess.run(cmd,cwd=tmp,capture_output=True,text=True,env=env)
                results.append(dict(version=revision,command=' '.join(cmd),exit_code=r.returncode,stdout=r.stdout,stderr=r.stderr,scope='Historical reproducibility, NOT physical pinout validation of E1'))
                print(revision,r.returncode,script,flush=True)
    (D/'historical-version-regressions.json').write_text(json.dumps(results,indent=2)+'\n')
    assert all(x['exit_code']==0 for x in results),'See historical-version-regressions.json'
if __name__=='__main__':main()
