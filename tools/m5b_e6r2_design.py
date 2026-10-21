"""Small E5 schematic delta plus native Architecture C and instrumentation sheet."""
import copy,math
import m5a_r1_design as c
from m5b_e6r2_common import *
from m5b_e6r2_geometry import geometry

def prop(s,n):return next(v for v in c.children(s,'property') if v[1]==n)
def pin_label(tree,ref,pin,new):
 sym=next(s for s in c.children(tree,'symbol') if prop(s,'Reference')[2]==ref)
 typ=c.child(sym,'lib_id')[1];lib=next(s for s in c.children(c.child(tree,'lib_symbols'),'symbol') if s[1]==typ)
 pp=next(z for z in c.walk(lib,'pin') if c.child(z,'number')[1]==pin)
 at=c.child(sym,'at');pa=c.child(pp,'at');angle=math.radians(float(at[3]));x=float(at[1])+float(pa[1])*math.cos(angle)-float(pa[2])*math.sin(angle);y=float(at[2])-float(pa[1])*math.sin(angle)-float(pa[2])*math.cos(angle)
 key=lambda v:tuple(round(float(a),4) for a in v)
 seen={key([x,y])};links=[]
 for w in c.children(tree,'wire'):
  pts=c.children(c.child(w,'pts'),'xy');links.append((key(pts[0][1:]),key(pts[1][1:])))
 while True:
  old=len(seen)
  for a,b in links:
   if a in seen or b in seen:seen.update([a,b])
  if len(seen)==old:break
 labels=[g for g in c.children(tree,'global_label') if key(c.child(g,'at')[1:3]) in seen]
 assert len(labels)==1,(ref,pin,labels)
 labels[0][1]=new

def main():
 guard();j=manifest();assert j['revision']!='M5B-E6R2','Implementation generator is one-shot; use committed native authority after layout'
 geom=geometry();parts={z['ref']:z for z in j['parts']}
 changes=[('U402','3','GND'),('U305','3','DRIVER_ON'),('U601','1','CLOCK_OFF'),('R509','1','LOCAL_MOD_OFF'),('Q401','2','VPA_PRE')]
 for file in HW.glob('*.kicad_sch'):
  sx=c.parse(file.read_text());changed=False
  for r,pin,net in changes:
   if any(prop(s,'Reference')[2]==r for s in c.children(sx,'symbol')):
    pin_label(sx,r,pin,net);parts[r]['pins'][pin]=net;changed=True
  for sym in c.children(sx,'symbol'):
   r=prop(sym,'Reference')[2]
   if r in geom['devices']:
    fp='ARDF_2M:'+geom['devices'][r]['footprint'];prop(sym,'Footprint')[2]=fp;parts[r]['footprint']=fp
    for lib in c.children(c.child(sx,'lib_symbols'),'symbol'):
     if lib[1]==c.child(sym,'lib_id')[1]:
      filt=next((q for q in c.children(lib,'property') if q[1]=='ki_fp_filters'),None)
      if filt:filt[2]+=' '+fp
    changed=True
  tb=c.child(sx,'title_block')
  if tb:
   rev=c.child(tb,'rev')
   if rev:rev[1]=REV
   date=c.child(tb,'date')
   if date:date[1]=DATE
  # Only current native titles/notes are normalized; historical evidence frozen.
  for text in c.children(sx,'text'):
   if 'M5B-E5' in text[1]:text[1]=text[1].replace('M5B-E5R1R1',REV).replace('M5B-E5R1',REV).replace('M5B-E5',REV)
  file.write_text(c.dump(sx)+'\n')
 c.DEST=HW;c.DATE=DATE
 d=c.Design();d.parts=parts;d.root_uuid=c.child(c.parse((HW/'RF2M.kicad_sch').read_text()),'uuid')[1];d.revision=REV
 lib=c.parse((HW/'ARDF_2M.kicad_sym').read_text())
 d.lib.defs.update({s[1]:s for s in c.children(lib,'symbol')})
 d.lib.box('TLV7032_DGK',{'1':('OUTA','output'),'2':('INA-','input'),'3':('INA+','input'),'4':('GND','power_in'),'5':('INB+','input'),'6':('INB-','input'),'7':('OUTB','output'),'8':('VCC','power_in')})
 d.lib.box('LVC1G00_DBV',{'1':('A','input'),'2':('B','input'),'3':('GND','power_in'),'4':('Y','output'),'5':('VCC','power_in')})
 d.lib.box('LVC2G32_DCU',{'1':('1A','input'),'2':('1B','input'),'3':('2Y','output'),'4':('GND','power_in'),'5':('2A','input'),'6':('2B','input'),'7':('1Y','output'),'8':('VCC','power_in')})
 d.lib.box('LVC1G04_DBV',{'1':('NC','no_connect'),'2':('A','input'),'3':('GND','power_in'),'4':('Y','output'),'5':('VCC','power_in')})
 s=d.sheet('13_carrier_keying','13 Carrier-keyed A2A: prepared converter, drain/driver readiness and probes')
 s.text('Architecture C: LOCAL_MOD_OFF=NORMAL_OFF OR KEY_N; DRIVER_ON=NOT LOCAL_MOD_OFF.\nCLOCK_OFF=LOCAL_MOD_OFF OR NOT(VPA_READY AND DRV_READY). Native safety delay/fastkill remain in series.\nAF_PWM must provide shaped sine envelope; KEY gives preparation lead. No converter re-start per Morse element.\nExisting thermal/current/lease protection preserved. Local PA sensor is instrumentation, not a new junction-temperature guarantee.',16,25,1.05)
 new=[]
 def add(ref,typ,value,pins,fp,mpn,cost=.03,note='',url='https://www.ti.com'):
  k=len(new);s.place(ref,typ,value,pins,62+(k%5)*112,85+(k//5)*49,fp,mpn,'carrier_keying','NORMAL',price={'1':cost},note=note,source=url);new.append(ref)
 add('U970','TLV7032_DGK','TLV7032DGKR',{'1':'VPA_READY','2':'VPA_READY_REF','3':'VPA_READY_S','4':'GND','5':'DRV_READY_S','6':'DRV_READY_REF','7':'DRV_READY','8':'V3V3'},'Package_SO:VSSOP-8_3x3mm_P0.65mm','TLV7032DGKR',.9,'Push-pull readiness only; no unqualified local PA temperature threshold. Outputs pulled low when absent.','https://www.ti.com/lit/ds/symlink/tlv7031.pdf')
 add('U971','LVC1G00_DBV','SN74LVC1G00DBVR',{'1':'VPA_READY','2':'DRV_READY','3':'GND','4':'RF_NOT_READY','5':'V3V3'},'Package_TO_SOT_SMD:SOT-23-5','SN74LVC1G00DBVR',.15,'NAND readiness. RF_NOT_READY has default pull-up.','https://www.ti.com/lit/ds/symlink/sn74lvc1g00.pdf')
 add('U972','LVC2G32_DCU','SN74LVC2G32DCUR',{'1':'NORMAL_OFF','2':'KEY_N','3':'CLOCK_OFF','4':'GND','5':'LOCAL_MOD_OFF','6':'RF_NOT_READY','7':'LOCAL_MOD_OFF','8':'V3V3'},'Package_SO:VSSOP-8_2.3x2mm_P0.5mm','SN74LVC2G32DCUR',.22,'Both emergency/slot inhibit and normal Morse key have priority over RF readiness.','https://www.ti.com/lit/ds/symlink/sn74lvc2g32.pdf')
 add('U973','LVC1G04_DBV','SN74LVC1G04DBVR',{'1':None,'2':'LOCAL_MOD_OFF','3':'GND','4':'DRIVER_ON','5':'V3V3'},'Package_TO_SOT_SMD:SOT-23-5','SN74LVC1G04DBVR',.1,'Driver enable defaults low; only small MMIC domain keyed.','https://www.ti.com/lit/ds/symlink/sn74lvc1g04.pdf')
 resistors=[('R970','0.05','VPA_PRE','VPA'),('R971','100k','VPA','VPA_READY_S'),('R972','33k','VPA_READY_S','GND'),('R973','330k','V3V3','VPA_READY_REF'),('R974','2.49k','VPA_READY_REF','GND'),('R975','100k','VDRV_MMIC','DRV_READY_S'),('R976','33k','DRV_READY_S','GND'),('R977','19.1k','V3V3','DRV_READY_REF'),('R978','10k','DRV_READY_REF','GND'),('R979','100k','VPA_READY','GND'),('R980','100k','DRV_READY','GND'),('R981','100k','CLOCK_OFF','V3V3'),('R982','100k','DRIVER_ON','GND'),('R983','100k','RF_NOT_READY','V3V3'),('R984','100k','LOCAL_MOD_OFF','V3V3')]
 for r,val,a,b in resistors:
  add(r,'R',val,{'1':a,'2':b},'ARDF_2M:R_2512_6332Metric_E3' if r=='R970' else 'ARDF_2M:R_0603_1608Metric_E3','WSL2512R0500FEA' if r=='R970' else 'RT0603BRD07'+{'100k':'100KL','33k':'33KL','330k':'330KL','2.49k':'2K49L','19.1k':'19K1L','10k':'10KL'}[val],.4 if r=='R970' else .04,'R970 50mohm1%1W: Kelvin across TP970 and TP502; outer feedback senses downstream VPA. Other dividers 0.1%.' if r=='R970' else '0.1% divider/default state; exact package/MPN audit in E6R2.',url='https://www.vishay.com/docs/30100/wsl.pdf' if r=='R970' else 'https://www.yageo.com/en/ProductCategory/Resistors')
 for i in range(4):add('C97'+str(i),'C','100n',{'1':'V3V3','2':'GND'},'ARDF_2M:C_0603_1608Metric_E3','GRM188R71H104KA93D',.04,'Local bypass at corresponding new IC.')
 for r,note,net in [('TP970','Pass collector before current shunt','VPA_PRE'),('TP971','Regulated current shunt upstream','VREG_SWITCH'),('TP972','RF inhibit','CLOCK_OFF'),('TP973','MMIC enable','DRIVER_ON'),('TP974','Modulator clamp','LOCAL_MOD_OFF'),('TP975','PA readiness','VPA_READY'),('TP976','Driver readiness','DRV_READY')]:
  add(r,'TestPoint',note,{'1':net},'ARDF_2M:TestPoint_Pad_D1.0mm_E3','PCB feature',0,'High-impedance probing; never attach an ammeter directly across a supply.')
 s.save()
 # Append only the new sheet; original hierarchy/UUIDs remain stable.
 root=c.parse((HW/'RF2M.kicad_sch').read_text());i=len(c.children(root,'sheet'));x=20+(i%3)*190;y=65+(i//3)*45
 root.append(c.parse(f'(sheet (at {x} {y}) (size 170 34) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid "{s.uuid}") (property "Sheetname" "{s.title}" (at {x} {y-1.27} 0) (effects (font (size 1.27 1.27)) (justify left bottom))) (property "Sheetfile" "{s.name}.kicad_sch" (at {x} {y+36} 0) (effects (font (size 1.27 1.27)) (justify left top))) (instances (project "RF2M" (path "/{d.root_uuid}" (page "{i+2}")))))'))
 (HW/'RF2M.kicad_sch').write_text(c.dump(root)+'\n')
 for name in s.used:
  if not any(t[1]==name for t in c.children(lib,'symbol')):lib.append(d.lib.defs[name])
 (HW/'ARDF_2M.kicad_sym').write_text(c.dump(lib)+'\n')
 j.update(date=DATE,revision=REV,status='CONTROLLED EVALUATION PCB; POWERED QUALIFICATION NOT_RUN',parts=list(d.parts.values()))
 j['placements'][s.name]=s.placements
 (HW/'RF2M.electrical.json').write_text(json.dumps(j,indent=2)+'\n')
 save('electrical-change.json',dict(changes=[dict(ref=r,pin=pin,net=n) for r,pin,n in changes],added=new,thermal='Existing TH801 retained; external thermocouple locations only. No new unqualified thermal trip.',controller_GPIO_change=False))
 print('Native Architecture C schematic and measurement sheet implemented',len(new),'new references')

if __name__=='__main__':main()
