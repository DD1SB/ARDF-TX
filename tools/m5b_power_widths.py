import pcbnew as p,json
b=p.LoadBoard('hardware/2m/RF2M.kicad_pcb');fs={f.GetReference():f for f in b.GetFootprints()}
pairs=[('J301','1','F301','1'),('F301','2','Q309','3'),('Q309','2','Q305','2'),('Q305','3','L302','1'),('Q305','3','U301','3'),('U302','8','J302','1'),('L301','2','J302','3'),('J302','2','Q302','2'),('Q302','3','R309','1'),('R309','2','Q401','3'),('Q401','2','L635','1')]
rm=[t for t in b.GetTracks()if not isinstance(t,p.PCB_VIA)and p.ToMM(t.GetWidth())<.5 and p.ToMM(t.GetLength())>2]
for t in rm:b.Remove(t)
b.BuildConnectivity();c=b.GetConnectivity();res=[]
for r,a,s,d in pairs:
 x=next(pa for pa in fs[r].Pads()if pa.GetNumber()==a);y=next(pa for pa in fs[s].Pads()if pa.GetNumber()==d);ok=y.m_Uuid.AsString()in{q.m_Uuid.AsString()for q in c.GetConnectedItems(x)};print(r,a,s,d,x.GetNetname(),ok);res.append(dict(from_ref=r,from_pad=a,to_ref=s,to_pad=d,net=x.GetNetname(),wide_or_short_neck_connected=ok))
open('hardware/2m/review/M5B-E1/power-path-widths.json','w').write(json.dumps(dict(policy='Main current paths retain >=0.5mm tracks or individual <=2mm pad necks;70um copper. Sense/control branches excluded from main load path, not from DRC.',paths=res,pass_all=all(x['wide_or_short_neck_connected']for x in res)),indent=2)+'\n')
import os,sys
sys.stdout.flush();os._exit(0)
