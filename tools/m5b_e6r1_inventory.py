"""Inventory analysis evidence; does not regenerate historical or CAD exports."""
from m5b_e6r1_common import *

def main():
    guard()
    files=list(OUT.rglob('*'))+list((ROOT/'docs').glob('M5B_E6R1_*.md'))+list((ROOT/'tools').glob('m5b_e6r1_*'))
    files += [ROOT/'tools/test_m5b_e6r1_analysis.py',ROOT/'README.md',ROOT/'docs/README.md']
    files=sorted(set(p for p in files if p.is_file() and p.name!='SHA256SUMS.txt'))
    records=[f'{sha(p)}  {p.relative_to(ROOT)}' for p in files]
    (OUT/'SHA256SUMS.txt').write_text('\n'.join(records)+'\n')
    print(f'Inventory: {len(files)} files; starting {START} source guard PASS')

if __name__=='__main__':main()
