#!/usr/bin/python3
"""Manufacturer-specific physical role assertions on real symbols, XML and PCB.

Expected BD140/TL431 physical roles/application nets are independent of the CAD
manifest. Negative cases never mutate the design. No physical assembly claim.
"""
import copy,hashlib,json,math,subprocess,sys,tempfile
from pathlib import Path
import xml.etree.ElementTree as ET
import pcbnew as pcb
from m3_80m_design import parse,children,child,walk
R=Path(__file__).resolve().parents[1];H=R/'hardware/80m';D=H/'review/M3B-E2'
S23='Package_TO_SOT_SMD:SOT-23';S6='Package_TO_SOT_SMD:SOT-23-6';SO14='Package_SO:SOIC-14_3.9x8.7mm_P1.27mm';SO16='Package_SO:SOIC-16_3.9x9.9mm_P1.27mm'
# Pin names here are manufacturer roles. Empty CAD pin labels on standard logic
# are verified by physical input/output types and the independent gate model.
def spec(maker,foot,names,url,package,**extra):return dict(manufacturer=maker,footprint=foot,roles={str(i):n for i,n in names.items()},source=url,package=package,**extra)
CAT={
 'BD140':spec('STMicroelectronics','ARDF_TX:ST_BD140_SOT32_1p3Drill',{1:'B',2:'C',3:'E'},'https://www.st.com/resource/en/datasheet/bd140.pdf','SOT-32, drawing0016114E, May2008 Rev5 p1/p7',symbol='BD140_ST',nets={'1':'SHAPE_BASE','2':'VPA_SHAPED','3':'VPA_LOAD'}),
 'TL431AIDBZR':spec('Texas Instruments',S23,{1:'K',2:'REF',3:'A'},'https://www.ti.com/lit/ds/symlink/tl431.pdf','DBZ, SLVS543S May2024 Table5-1 p4',symbol='TL431_TI_DBZ',nets={'1':'VREF_2V5','2':'VREF_2V5','3':'GND'}),
 'LM5134BMF/NOPB':spec('Texas Instruments',S6,{1:'VDD',2:'PILOT',3:'OUT',4:'VSS',5:'INB',6:'IN'},'https://www.ti.com/lit/ds/symlink/lm5134.pdf','DBV0006A/SOT23-6, SNVS808C Feb2016 p3'),
 'TPS22810DBVR':spec('Texas Instruments',S6,{1:'VIN',2:'GND',3:'EN/UVLO',4:'CT',5:'QOD',6:'VOUT'},'https://www.ti.com/lit/ds/symlink/tps22810.pdf','DBV0006A/SOT23-6, SLVSDH0C Jan2018 p3'),
 'TPS54302DDCT':spec('Texas Instruments','Package_TO_SOT_SMD:TSOT-23-6',{1:'GND',2:'SW',3:'VIN',4:'FB',5:'EN',6:'BOOT'},'https://www.ti.com/lit/ds/symlink/tps54302.pdf','DDC0006A/SOT23-THIN; SLVSD26C'),
 'INA180A1IDBVT':spec('Texas Instruments','Package_TO_SOT_SMD:SOT-23-5',{1:'OUT',2:'GND',3:'IN+',4:'IN-',5:'VS'},'https://www.ti.com/lit/ds/symlink/ina180.pdf','DBV0005A, not alternate pin-compatible assumption'),
 'SI5351A-B-GT':spec('Skyworks','Package_SO:MSOP-10_3x3mm_P0.5mm',{1:'VDD',2:'XA',3:'XB',4:'SCL',5:'SDA',6:'CLK2',7:'VDDO',8:'GND',9:'CLK1',10:'CLK0'},'https://www.skyworksinc.com/-/media/SkyWorks/SL/documents/public/data-sheets/Si5351-B.pdf','10-MSOP, 3x3mm/0.5mm pitch'),
 'IRF610PBF-BE3':spec('Vishay','ARDF_TX:TO220_Vertical_1p3Drill',{1:'G',2:'D',3:'S'},'https://www.vishay.com/docs/91023/irf610.pdf','TO220AB; tab D; exact incoming lead fit required'),
 'MCP100T-300I/TT':spec('Microchip',S23,{1:'RESET_N',2:'VDD',3:'VSS'},'https://ww1.microchip.com/downloads/en/DeviceDoc/11187f.pdf','SOT23-3, DS11187F p1/mechanical p9'),
 'MMBT3904,215':spec('Nexperia',S23,{1:'B',2:'E',3:'C'},'https://assets.nexperia.com/documents/data-sheet/MMBT3904.pdf','SOT23 top view'),
 'MMBT3906,215':spec('Nexperia',S23,{1:'B',2:'E',3:'C'},'https://assets.nexperia.com/documents/data-sheet/MMBT3906.pdf','SOT23 top view'),
 'BSS138BK,215':spec('Nexperia',S23,{1:'G',2:'S',3:'D'},'https://assets.nexperia.com/documents/data-sheet/BSS138BK.pdf','SOT23, gate +/-20V'),
 'DMN2056U-7':spec('Diodes Incorporated',S23,{1:'G',2:'S',3:'D'},'https://www.diodes.com/datasheet/download/DMN2056U.pdf','SOT23; gate +/-8V, only3.3V control'),
 'LM339BIDR':spec('Texas Instruments',SO14,{1:'OUT',2:'OUT',3:'V+',4:'-',5:'+',6:'-',7:'+',8:'-',9:'+',10:'-',11:'+',12:'V-',13:'OUT',14:'OUT'},'https://www.ti.com/lit/ds/symlink/lm339.pdf','D0014A SOIC14; compare physical polarity, not channel naming'),
 'LM393BIDR':spec('Texas Instruments','Package_SO:SOIC-8_3.9x4.9mm_P1.27mm',{1:'OUT',2:'-',3:'+',4:'V-',5:'+',6:'-',7:'OUT',8:'V+'},'https://www.ti.com/lit/ds/symlink/lm393.pdf','D0008A SOIC8'),
 '74HC123D,653':spec('Nexperia',SO16,{1:'A',2:'B',3:'Clr',4:'~{Q}',5:'Q',6:'Cext',7:'RCext',8:'GND',9:'A',10:'B',11:'Clr',12:'~{Q}',13:'Q',14:'Cext',15:'RCext',16:'VCC'},'https://assets.nexperia.com/documents/data-sheet/74HC_HCT123.pdf','SOT109-1 SO16'),
 '74HC174D,653':spec('Nexperia',SO16,{1:'~{Mr}',2:'Q0',3:'D0',4:'D1',5:'Q1',6:'D2',7:'Q2',8:'GND',9:'Cp',10:'Q3',11:'D3',12:'Q4',13:'D4',14:'D5',15:'Q5',16:'VCC'},'https://assets.nexperia.com/documents/data-sheet/74HC_HCT174.pdf','SOT109-1 SO16')}
for mpn in ('BAT54WS-7-F','SS34-E3/57T','SMBJ17A'):
 url={'BAT54WS-7-F':'https://www.diodes.com/datasheet/download/BAT54WS.pdf','SS34-E3/57T':'https://www.vishay.com/docs/88751/ss32.pdf','SMBJ17A':'https://www.littelfuse.com/assetdocs/littelfuse_tvs_diode_smbj_datasheet.pdf?assetguid=09a6ae9a-73cb-4ac4-acac-e6dab92ab953'}[mpn]
 CAT[mpn]=spec('Diodes Incorporated'if mpn.startswith('BAT')else'Vishay'if mpn.startswith('SS34')else'Littelfuse',{'BAT54WS-7-F':'Diode_SMD:D_SOD-323','SS34-E3/57T':'Diode_SMD:D_SMC','SMBJ17A':'Diode_SMD:D_SMB'}[mpn],{1:'K',2:'A'},url,'Cathode band->pad1; exact package, no generic SS34-SMA substitution')
# Logic packages and pins by actual manufacturer gates.
from m3a_r1_logic import GATES,FF74
for mpn in ['74HC00D,653','74HC08D,653','74HC11D,653','74HC21D,653','74HC32D,653','74HC14D,653','74HC74D,653','SN74AC00DR']:
 typ=mpn.split('D,')[0]if mpn.startswith('74')else'74HC00';roles={'7':'GND','14':'VCC'}
 if typ in GATES:
  for _,layout in [GATES[typ]]:
   for ins,out in layout:
    for i in ins:roles[i]='INPUT'
    roles[out]='OUTPUT'
 else:
  for clr,d,cp,pr,q,qb in FF74:
   for i in (clr,d,cp,pr):roles[i]='INPUT'
   for i in (q,qb):roles[i]='OUTPUT'
 CAT[mpn]=spec('Texas Instruments'if mpn=='SN74AC00DR'else'Nexperia',SO14,roles,'https://www.ti.com/lit/ds/symlink/sn74ac00.pdf'if mpn=='SN74AC00DR'else'https://assets.nexperia.com/documents/data-sheet/'+typ.replace('74HC','74HC_HCT')+'.pdf','SOIC14 top view; independent gate logic regression verifies functions')

for mpn,maker,foot,count,url in [
 ('Littelfuse 046701.5NR','Littelfuse','ARDF_TX:Fuse_467_0603',2,'https://www.littelfuse.com/assetdocs/fuse-467-datasheet?assetguid=4a59f034-1cca-460e-a5ba-e1e66247c76d'),
 ('Wurth 61201621621','Wurth','ARDF_TX:Wurth_61201621621',16,'https://www.we-online.com/components/products/datasheet/61201621621.pdf'),
 ('B2P-VH(LF)(SN)','JST','Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical',2,'https://www.jst-mfg.com/product/pdf/eng/eVH.pdf'),
 ('B3B-XH-A(LF)(SN)','JST','Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical',3,'https://www.jst-mfg.com/product/pdf/eng/eXH.pdf'),
 ('1727010','Phoenix Contact','TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1-2-3.81_1x02_P3.81mm_Horizontal',2,'https://www.mouser.com/datasheet/2/324/3/ItemDetail_1727010-929404.pdf'),
 ('ABM3B-25.000MHZ-10-1-U-T','Abracon','Crystal:Crystal_SMD_5032-4Pin_5.0x3.2mm',4,'https://abracon.com/Resonators/abm3b.pdf'),
 ('Amidon FT-50A-43 + AWG24 enamel Cu','Amidon core; own formed winding','ARDF_TX:FT50A43_Inline_4Terminal',4,'https://github.com/OpenARDF/SignalSlinger')]:
 CAT[mpn]=spec(maker,foot,{k:'CONTACT'for k in range(1,count+1)},url,'Exact physical landing; key/lead-forming constraints in mechanical report')
CAT['ABM3B-25.000MHZ-10-1-U-T']['footprint']='Crystal:Crystal_SMD_5032-4Pin_5.0x3.2mm'
CAT['B2P-VH(LF)(SN)']['nets']={'1':'VBAT','2':'GND'}
CAT['B3B-XH-A(LF)(SN)']['nets']={'1':'RF_FOX','2':'GND','3':'FOX_ID'}
CAT['Amidon FT-50A-43 + AWG24 enamel Cu']['nets']={'1':'VPA_SHAPED','2':'DRAIN_PA','3':'DRAIN_PA','4':'RF_RAW'}

def collect(xml,board):
 tree=ET.parse(xml);comps={x.attrib['ref']:x for x in tree.findall('./components/comp')};n={}
 for net in tree.findall('./nets/net'):
  for p in net.findall('node'):n[(p.attrib['ref'],p.attrib['pin'])]=net.attrib['name'].removeprefix('/')
 syms={x[1]:x for x in children(parse((H/'ARDF_TX.kicad_sym').read_text()),'symbol')};fs={f.GetReference():f for f in board.GetFootprints()};out={}
 for ref,c in comps.items():
  mpn=next((p.attrib.get('value')for p in c.findall('property')if p.attrib['name']=='MPN'),None)
  if mpn not in CAT:continue
  name=c.find('libsource').attrib['part'];s=syms.get(name);sp={}
  if s:
   for pin in walk(s,'pin'):
    if child(pin,'number'):sp[child(pin,'number')[1]]=dict(name=child(pin,'name')[1],electrical_type=pin[1])
  f=fs[ref];out[ref]=dict(mpn=mpn,manufacturer_field=next((p.attrib.get('value','')for p in c.findall('property')if p.attrib['name']=='Manufacturer'),''),symbol=name,symbol_pins=sp,footprint=str(f.GetFPID().GetLibNickname())+':'+str(f.GetFPID().GetLibItemName()),netlist={k:v for (r,k),v in n.items()if r==ref},pcb={p.GetNumber():p.GetNetname()for p in f.Pads()},pad_mm={p.GetNumber():[round(pcb.ToMM(p.GetPosition().x),4),round(pcb.ToMM(p.GetPosition().y),4)]for p in f.Pads()},drills_mm={p.GetNumber():pcb.ToMM(p.GetDrillSize().x)for p in f.Pads()},rotation=f.GetOrientationDegrees())
 return out

def check_one(ref,a,roles=True):
 s=CAT[a['mpn']];assert a['footprint']==s['footprint'],(ref,'unverified footprint',a['footprint'])
 if ref in('Q403','U311','D302'):assert a['manufacturer_field']==s['manufacturer'],(ref,'unverified manufacturer')
 if 'symbol'in s:assert a['symbol']==s['symbol'],(ref,'manufacturer symbol')
 for pin,role in s['roles'].items():
  net=a['netlist'].get(pin,'');assert a['pcb'].get(pin,'')==net,(ref,pin,'netlist/PCB disagreement')
  if pin in s.get('nets',{}):assert net==s['nets'][pin],(ref,pin,'wrong manufacturer physical net',net)
  if not roles:continue
  sp=a['symbol_pins'][pin]
  if role=='CONTACT':continue
  if role in('INPUT','OUTPUT'):assert sp['electrical_type']==role.lower(),(ref,pin,'gate pin type')
  else:
   nm=sp['name'];aliases={'OUT':['','OUT'],'IN+':['+','IN+'],'IN-':['-','IN-'],'VS':['V+','VS'],'VCC':['VCC','VFOX']};assert nm in aliases.get(role,[role]),(ref,pin,role,nm)
 if ref=='Q403':
  assert a['rotation']==180 and a['pad_mm']=={'1':[160.56,69.0],'2':[158.28,69.0],'3':[156.0,69.0]},'Wrong ST installed orientation'
  # With +PCB-Y toward viewer and Z up, viewer-right is +PCB-X.
  # ST's illustrated face therefore reads 3,2,1 left-to-right, as p7.
  assert [k for k,v in sorted(a['pad_mm'].items(),key=lambda z:z[1][0])]==['3','2','1']
  assert all(v>=1.299 for v in a['drills_mm'].values())
 return True

def main():
 b=pcb.LoadBoard(str(H/'RF80.kicad_pcb'));a=collect(D/'RF80.xml',b);rows=[]
 for ref,v in sorted(a.items()):
  check_one(ref,v)
  state='Requires incoming dimensional inspection'if ref in('Q402','T401')else'Verified with assembly constraint'if ref in('Q403','J101','J301','J401','J502','Y101')else'Verified'
  rows.append(dict(reference=ref,**CAT[v['mpn']],observed=v,status=state,scope='Manufacturer-document/CAD mapping; no incoming identity or hardware qualification'))
 q=next(f for f in b.GetFootprints()if f.GetReference()=='Q403')
 assert [m.m_Filename for m in q.Models()]==['${KIPRJMOD}/3dmodels/ST_BD140_envelope.wrl'],'Wrong ST envelope/orientation model'
 assert any(isinstance(t,pcb.PCB_TEXT)and t.GetText()=='ST BD140: DRAWING FACE TOWARD +Y'for t in b.GetDrawings()),'ST assembly face annotation disagrees'
 rejected=[]
 tests=[('Q403 XML pad1 emitter','Q403','netlist','1','VPA_LOAD'),('Q403 XML pad3 base','Q403','netlist','3','SHAPE_BASE'),('Q403 PCB pad1 emitter','Q403','pcb','1','VPA_LOAD'),('Q403 PCB pad3 base','Q403','pcb','3','SHAPE_BASE'),('TL431 old ground pin2','U311','pcb','2','GND')]
 for label,ref,key,pin,value in tests:
  bad=copy.deepcopy(a[ref]);bad[key][pin]=value
  try:check_one(ref,bad)
  except AssertionError:rejected.append(label)
  else:raise AssertionError('Mutation escaped: '+label)
 for key,value in [('manufacturer_field','Unverified vendor'),('footprint','Package_TO_SOT_THT:TO-126-3_Vertical'),('symbol','BD140')]:
  bad=copy.deepcopy(a['Q403']);bad[key]=value
  try:check_one('Q403',bad)
  except AssertionError:rejected.append('Q403 unverified '+key)
  else:raise AssertionError('Unverified substitution escaped')
 # Real archived E1 XML + PCB must be rejected, not only artificial mutations.
 with tempfile.TemporaryDirectory(prefix='m3be2-negative-')as tmp:
  p=Path(tmp)/'E1.kicad_pcb';p.write_bytes(subprocess.check_output(['git','show','m3b-e1:hardware/80m/RF80.kicad_pcb'],cwd=R));old=collect(H/'review/M3B-E1/RF80.xml',pcb.LoadBoard(str(p)))
  for ref in ('Q403','U311'):
   try:check_one(ref,old[ref],roles=False)
   except AssertionError:rejected.append('actual E1 '+ref)
   else:raise AssertionError('Historical faulty component escaped '+ref)
 result=dict(date='2026-10-15',revision='M3B-E2',classification='MANUFACTURER DOCUMENT / CAD PIN ASSERTIONS; NO HARDWARE VALIDATION',devices=rows,count=len(rows),negative_cases_rejected=rejected,assembly_constraints=['Q403 drawing face toward board+Y; 180deg footprint; verify actual ST device, no alternate-vendor substitution','IRF610 tab is drain: insulated heatsink/thermocouple','Connector keys/contact identities and winding lead forming require incoming dimensional inspection'])
 (D/'critical-pinouts.json').write_text(json.dumps(result,indent=2)+'\n');print('PASS manufacturer pin audit:',len(rows),'devices;',len(rejected),'negative cases including real E1 Q403/U311 rejected')
if __name__=='__main__':main()
