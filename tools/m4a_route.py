#!/usr/bin/python3
"""Local compact-board routing support; never accesses the E2 file for writing.
Critical RF/power trees are placed before the local offline general router.
"""
import argparse,json,math,re
from pathlib import Path
import pcbnew as pcb
from m3b_pcb import Layout,pt,xy
from m4a_design import P,D,NAME,MM
class Router(Layout):
    def __init__(self):
        self.b=pcb.LoadBoard(str(P/(NAME+'.kicad_pcb')));self.f={f.GetReference():f for f in self.b.GetFootprints()};self.nets={p.GetNetname():p.GetNet()for f in self.f.values()for p in f.Pads()if p.GetNetname()};self.manual=[]
    def route_path(self,n,a,b,width):
        path=super().route_path(n,a,b,width)
        if path and all(21<=x<=169 and 21<=y<=129 for x,y in path):return path
        return None
    def critical(self):
        priority=['DRAIN_PA','GATE_PA','GATE_DRV','SW_PA','BOOT_PA','VDRV','VPA_SHAPED','RF_RAW','LPF_N1','LPF_N2','RF_NORMAL','VPA_ISO','VPA_LOAD','SENSE_PLUS','SENSE_MINUS','VPA','VIN_PA','VIN_PACK','VBAT_FUSED','VBAT','FOX_GATE1','FOX_GATE2','FOX_GATE3','FOX_SUM','FOX_LPF1','FOX_LPF2','FOX_PAD_IN','RF_FOX','FOX_CLK','FOX_GATE_EN','CLK_PA','CLK_FOX','XA','XB']
        for n in priority:
            pads=[p for f in self.f.values()for p in f.Pads()if p.GetNetname()==n]
            if len(pads)<2:continue
            width=1.0 if n=='DRAIN_PA'else .75 if n in('VPA_SHAPED','VPA_LOAD','VPA_ISO','VPA','VIN_PA','VIN_PACK','VBAT_FUSED','VBAT')else .55 if n in('RF_RAW','LPF_N1','LPF_N2','RF_NORMAL','SW_PA')else .30
            seen={0};pairs=[]
            while len(seen)<len(pads):
                _,i,j=min((math.dist(xy(pads[i].GetPosition()),xy(pads[j].GetPosition())),i,j)for i in seen for j in range(len(pads))if j not in seen);seen.add(j);pairs.append((i,j))
            root={'VPA_LOAD':('R330','2'),'VPA_ISO':('R330','1')}.get(n)
            if root:
                k=next(i for i,p in enumerate(pads)if p.GetParentFootprint().GetReference()==root[0]and p.GetNumber()==root[1]);pairs=[(k,j)for j in range(len(pads))if j!=k]
            for i,j in pairs:
                a,b=xy(pads[i].GetPosition()),xy(pads[j].GetPosition());path=None
                # Keep the whole drain at1mm; other PA rails >=.55mm. Never
                # accept a narrow arbitrary escape just to claim manual routing.
                ws=[width]if n=='DRAIN_PA'else[width,.55]if width==.75 else[width,.30]if width==.55 else[width,.20]
                for w in sorted(set(ws),reverse=True):
                    path=self.route_path(n,a,b,w)
                    if path:break
                if path:self.track(n,path,w)
                else:print('General route required',n,a,b,flush=True)
            print('RF/power tree',n,flush=True)
        pcb.SaveBoard(str(P/(NAME+'.kicad_pcb')),self.b);(D/'critical-routes.json').write_text(json.dumps(self.manual,indent=2)+'\n')
    def dsn(self):
        path=D/'RF80_V1.dsn';assert pcb.ExportSpecctraDSN(self.b,str(path));s=path.read_text().replace('(clearance 200)','(clearance 150)').replace('(width 200)','(width 150)').replace('(clearance 50 (type smd_smd))','(clearance 150 (type smd_smd))')
        a=s.index('    (class kicad_default');b=s.index('  (wiring',a);section=s[a:b]
        rails=['VBAT','VBAT_FUSED','VIN_PACK','VIN_PA','VPA','VPA_ISO','VPA_LOAD','VPA_SHAPED'];rf=['RF_RAW','LPF_N1','LPF_N2','RF_NORMAL','SW_PA'];special=['DRAIN_PA','GND']+rails+rf
        for n in special:section=re.sub(r'(?<![\w])'+re.escape(n)+r'(?![\w])','',section)
        extra=''
        for cls,ns,w,c in [('GROUND',['GND'],300,150),('HV_RF',['DRAIN_PA'],1000,600),('POWER',rails,300,150),('RF50',rf,550,150)]:
            extra+='    (class '+cls+' '+' '.join(ns)+' (circuit(use_via "Via[0-1]_600:300_um"))(rule(width '+str(w)+')(clearance '+str(c)+')))\n'
        pos=section.rfind('  )');section=section[:pos]+extra+section[pos:];path.write_text('\n'.join(line.rstrip()for line in(s[:a]+section+s[b:]).splitlines())+'\n');print('Exported offline DSN with explicit RF/power/ground classes')
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--critical',action='store_true');ap.add_argument('--dsn',action='store_true');ap.add_argument('--import-session');a=ap.parse_args();r=Router()
    if a.critical:r.critical()
    if a.import_session:
        # A SES contains new routing, not the protected input RF trees. Remove
        # previous unprotected imports/planes before replacing that routing.
        deleted=[t for t in r.b.GetTracks()if not t.IsLocked()]+list(r.b.Zones())
        for t in deleted:r.b.Remove(t)
        assert pcb.ImportSpecctraSES(r.b,a.import_session);pcb.SaveBoard(str(P/(NAME+'.kicad_pcb')),r.b);print('Imported local offline session')
    if a.dsn:r.dsn()
if __name__=='__main__':main()
