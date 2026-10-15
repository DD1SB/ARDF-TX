#!/usr/bin/python3
"""Refresh only M5 Markdown numeric tables from the machine-readable ledgers."""
import json
from pathlib import Path

R=Path(__file__).resolve().parents[1]
D=R/'hardware/2m/review/M5A-R0'

def table(path,header,rows):
    lines=path.read_text().splitlines()
    start=lines.index(header)
    end=start
    while end<len(lines) and lines[end].startswith('|'):
        end+=1
    lines[start:end]=[header,lines[start+1]]+['| '+' | '.join(map(str,row))+' |'for row in rows]
    path.write_text('\n'.join(lines)+'\n')

def main():
    c=json.loads((D/'costs.json').read_text())
    p=json.loads((D/'calculations.json').read_text())
    summary={x['variant']:x for x in c['summary']if x['fleet']==10}
    table(R/'docs/M5_2M_BOM.md',
          '| Population | Fitted physical parts | ICs | 6 units EUR/board | 10 units EUR/board | 20 units EUR/board |',
          [(v,summary[v]['fitted_physical'],summary[v]['ic_count'])+
           tuple(f"{next(x['component_allowance_net_eur']for x in c['summary']if x['variant']==v and x['fleet']==q):.2f}"for q in [6,10,20])
           for v in ['BOOST2S','BUCK4S','TRAIN_ONLY']])
    table(R/'docs/M5_2M_BOM.md','| Function, full2S | EUR/board at10 |',
          [(k,f'{v:.2f}')for k,v in summary['BOOST2S']['blocks'].items()])
    table(R/'docs/M5_2M_POWER_ARCHITECTURE.md',
          '| Supply/profile, m=0.80 | TX battery W | Contest average W | 12 h Wh | 24 h Wh |',
          [(f"{x['arch']} / {x['erp_carrier']:g} W ERP",f"{x['tx_battery_w']:.2f}",
            f"{x['average_battery_w']:.3f}",f"{x['need12_wh']:.2f}",f"{x['need24_wh']:.2f}")
           for x in p['profiles']if x['m']==.8])
    rows=[]
    for pack in ['2S2P','2S3P','2S4P','4S1P','4S2P']:
        for cell in ['25R_min','M35A_min']:
            a=next(x for x in p['packs']if x['pack']==pack and x['cell']==cell and x['m']==.8 and x['erp_carrier']==1)
            b=next(x for x in p['packs']if x['pack']==pack and x['cell']==cell and x['m']==.8 and x['erp_carrier']==.3)
            rows.append((pack+' / '+cell,f"{a['modeled_hours']:.1f}",f"{b['modeled_hours']:.1f}",
                         f"{a['modeled_beacon_hours']:.1f} / {b['modeled_beacon_hours']:.1f}"))
    table(R/'docs/M5_2M_POWER_ARCHITECTURE.md',
          '| Pack / cell minimum | Full 1 W ERP model h | Reduced0.30 W ERP model h | Full / reduced beacon h |',rows)
    print('Updated four M5 numeric tables; no previous-milestone files changed')

if __name__=='__main__':main()
