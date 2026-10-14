#!/usr/bin/env python3
"""Build the review schematic/BOM from a pin-explicit electrical manifest.

No PCB creation, routing, Gerbers, purchasing or production firmware. Standard
KiCad symbol drawings are flattened into a project library so the CAD remains
editable without the original research repositories. KiCad CLI performs ERC.
"""
import argparse
import copy
import csv
import json
import math
import re
import uuid
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEST = ROOT / 'hardware/80m'
LIB = Path('/usr/share/kicad/symbols')
DATE = '2026-10-14'
NAMESPACE = uuid.UUID('b38dce72-8155-4a48-9f25-6979b1b09f15')
def uid(s): return str(uuid.uuid5(NAMESPACE, s))
def q(s): return json.dumps(str(s), ensure_ascii=False)

class Atom(str): pass
def parse(s):
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[()]|[^\s()]+', s)
    stack = []
    result = None
    for t in tokens:
        if t == '(':
            x = []
            if stack: stack[-1].append(x)
            stack.append(x)
        elif t == ')': result = stack.pop()
        else: stack[-1].append(json.loads(t) if t.startswith('"') else Atom(t))
    if stack: raise ValueError('Unbalanced S-expression')
    return result
def dump(x):
    if isinstance(x, list): return '(' + ' '.join(dump(y) for y in x) + ')'
    if isinstance(x, Atom): return str(x)
    return q(x)
def child(x, key): return next((y for y in x if isinstance(y,list) and y and y[0] == key),None)
def children(x, key): return [y for y in x if isinstance(y,list) and y and y[0] == key]
def walk(x, key):
    if isinstance(x,list):
        if x and x[0] == key: yield x
        for y in x: yield from walk(y,key)

class Library:
    def __init__(self): self.files = {}; self.defs = {}
    def native(self, spec, new=None, pin_remap=None):
        lib,name = spec.split(':')
        if lib not in self.files:
            self.files[lib] = {x[1]:x for x in children(parse((LIB/(lib+'.kicad_sym')).read_text()),'symbol')}
        def resolve(n):
            x = copy.deepcopy(self.files[lib][n])
            ext = child(x,'extends')
            if ext:
                parent = resolve(ext[1])
                ownprops = {p[1]:p for p in children(x,'property')}
                out = [Atom('symbol'),n]
                for p in parent[2:]:
                    if isinstance(p,list) and p[0]=='property' and p[1] in ownprops:
                        out.append(ownprops.pop(p[1]))
                    else: out.append(p)
                out.extend(ownprops.values()); x=out
            return x
        x=resolve(name); new=new or name
        x[1]=new
        for s in children(x,'symbol'):
            s[1]=new+'_'+s[1].rsplit('_',2)[-2]+'_'+s[1].rsplit('_',2)[-1]
        if pin_remap:
            for p in walk(x,'pin'):
                number=child(p,'number'); number[1]=pin_remap.get(number[1],number[1])
        self.defs[new]=x
        return new
    def box(self,name,pins,left=None):
        # pins: physical number -> (name, electrical type); explicit datasheet mapping.
        left=left or list(pins)[:math.ceil(len(pins)/2)]
        right=[p for p in pins if p not in left]
        span=max(len(left),len(right)); h=max(5.08,(span+1)*1.27)
        s=f'(symbol {q(name)} (pin_names (offset 0.762)) (in_bom yes) (on_board yes) '
        s+=f'(property "Reference" "U" (at 0 {h+2} 0) (effects (font (size 1.27 1.27)))) '
        s+=f'(property "Value" {q(name)} (at 0 {-h-2} 0) (effects (font (size 1.27 1.27)))) '
        s+=f'(symbol {q(name+"_0_1")} (rectangle (start -13.97 {h}) (end 13.97 {-h}) (stroke (width 0.254) (type default)) (fill (type background)))) '
        s+=f'(symbol {q(name+"_1_1")} '
        for side,nums in [(1,left),(-1,right)]:
            for i,n in enumerate(nums):
                y=(len(nums)-1)*1.27-i*2.54; x=-side*19.05; angle=0 if side==1 else 180
                nm,typ=pins[n]
                s+=f'(pin {typ} line (at {x} {y} {angle}) (length 5.08) (name {q(nm)} (effects (font (size 1.016 1.016)))) (number {q(n)} (effects (font (size 1.016 1.016))))) '
        self.defs[name]=parse(s+'))'); return name
    def pins(self,name,unit=1):
        out=[]
        for s in children(self.defs[name],'symbol'):
            u=int(s[1].rsplit('_',2)[-2])
            style=int(s[1].rsplit('_',2)[-1])
            if u in (0,unit) and style in (0,1):
                for p in children(s,'pin'):
                    a=child(p,'at')
                    out.append((child(p,'number')[1],float(a[1]),float(a[2]),int(a[3]),str(p[1])))
        return out

class Sheet:
    def __init__(self,design,name,title,number):
        self.d=design; self.name=name; self.title=title; self.number=number
        self.uuid=uid('sheet:'+name); self.items=[]; self.used=set(); self.placements=[]
    def text(self,s,x,y,size=1.27):
        self.items.append(f'(text {q(s)} (at {x} {y} 0) (effects (font (size {size} {size})) (justify left top)) (uuid {q(uid(self.name+":text:"+str(len(self.items))))}))')
    def wire(self,x1,y1,x2,y2):
        self.items.append(f'(wire (pts (xy {x1:.4f} {y1:.4f}) (xy {x2:.4f} {y2:.4f})) (stroke (width 0) (type default)) (uuid {q(uid(self.name+":wire:"+str(len(self.items))))}))')
    def label(self,name,x,y,angle=0):
        # All sheet crossings explicit by unique global net name. No hidden power pins.
        self.items.append(f'(global_label {q(name)} (shape bidirectional) (at {x:.4f} {y:.4f} {angle}) (fields_autoplaced yes) (effects (font (size 0.9 0.9)) (justify {"right" if angle==0 else "left"})) (uuid {q(uid(self.name+":label:"+str(len(self.items))))}))')
    def place(self,ref,typ,value,pins,x,y,foot,mpn,group='shared',pop='BOTH',unit=1,angle=0,note='',source='',price=None,evidence='ESTIMATE',supplier='OPEN',code='OPEN',availability='Exact basket/stock OPEN',moq=1):
        x=round(x/1.27)*1.27; y=round(y/1.27)*1.27
        expected={p[0] for p in self.d.lib.pins(typ,unit)}
        assert set(pins)==expected, (ref,typ,unit,set(pins),expected)
        self.used.add(typ); ident=uid(self.name+':'+ref+':'+str(unit))
        h=0
        for _,_,py,_,_ in self.d.lib.pins(typ,unit): h=max(h,abs(py))
        self.items.append(f'(symbol (lib_id {q("ARDF_TX:"+typ)}) (at {x} {y} {angle}) (unit {unit}) (in_bom {"no" if ref.startswith("TP") else "yes"}) (on_board yes) (dnp {"yes" if pop in ("DNP","FOX") else "no"}) (uuid {q(ident)}) '+
            ''.join(f'(property {q(k)} {q(v)} (at {x+5 if typ in ("R","C","L") else x} {y-h-4+i*1.6 if i<2 else y} 0) '+
            f'(effects (font (size {1.0 if i<2 else 1.27} {1.0 if i<2 else 1.27})) '+ ('(hide yes)' if i>=2 else '') + ')) '
            for i,(k,v) in enumerate([('Reference',ref),('Value',value),('Footprint',foot),('Datasheet',source),('MPN',mpn),('Population',pop),('Function',group),('Engineering_Note',note)]))+
            f'(instances (project "RF80" (path {q("/"+self.d.root_uuid+"/"+self.uuid)} (reference {q(ref)}) (unit {unit})))) )')
        # Wire short stubs to named nets. Native transistor/passive drawings retain
        # their normal circuit meaning; multiunit logic is drawn as actual gates.
        rot=math.radians(angle)
        for num,px,py,pa,et in self.d.lib.pins(typ,unit):
            # Library y points upward; schematic screen y points downward.
            rx=px*math.cos(rot)-py*math.sin(rot); ry=px*math.sin(rot)+py*math.cos(rot)
            xx=x+rx; yy=y-ry; a=(pa+angle)%360
            net=pins.get(num)
            if net is None:
                self.items.append(f'(no_connect (at {xx:.4f} {yy:.4f}) (uuid {q(uid(ident+":NC:"+num))}))')
                continue
            outward={0:(-1,0),90:(0,1),180:(1,0),270:(0,-1)}[a]
            lx=xx+outward[0]*3.81; ly=yy+outward[1]*3.81
            self.wire(xx,yy,lx,ly)
            # Vertical pins bend to the left/right for readable horizontal labels.
            if outward[1]:
                nx=lx+(-5.08 if outward[1]<0 else 5.08); self.wire(lx,ly,nx,ly); lx=nx
            self.label(net,lx,ly,180 if outward[0]>0 or outward[1]>0 else 0)
        if ref not in self.d.parts:
            self.d.parts[ref]=dict(ref=ref,sheet=self.name,value=value,mpn=mpn,footprint=foot,group=group,population=pop,note=note,source_url=source,supplier=supplier,supplier_part_number=code,availability=availability,evidence=evidence,price_breaks_eur=price or {'1':0.03},moq=moq,multiple=1,pins={})
        self.d.parts[ref]['pins'].update(pins)
        self.placements.append(dict(ref=ref,unit=unit,x=x,y=y,type=typ))
    def save(self):
        # Keep fitted-population/MPN notes consistent with the costed manifest.
        revised=[]
        for item in self.items:
            if item.startswith('(symbol '):
                sx=parse(item);ref=next(p[2]for p in children(sx,'property')if p[1]=='Reference')
                if ref in self.d.parts:
                    p=self.d.parts[ref]
                    for prop in children(sx,'property'):
                        if prop[1]=='Population':prop[2]=p['population']
                        elif prop[1]=='MPN':prop[2]=p['mpn']
                        elif prop[1]=='Footprint':prop[2]=p['footprint']
                        elif prop[1]=='Engineering_Note':prop[2]=p['note']
                        elif prop[1]=='Datasheet'and p.get('manufacturer'):prop[2]=p['source_url']
                    if p.get('manufacturer'):
                        old=next((v for v in children(sx,'property')if v[1]=='Manufacturer'),None)
                        if old:old[2]=p['manufacturer']
                        else:sx.append(parse('(property \"Manufacturer\" '+q(p['manufacturer'])+' (at 0 0 0)(effects(font(size 1 1))(hide yes)))'))
                    item=dump(sx)
            revised.append(item)
        self.items=revised
        defs=' '.join(dump(self.d.lib.defs[t]).replace('(symbol '+q(t)+' ', '(symbol '+q('ARDF_TX:'+t)+' ',1) for t in sorted(self.used))
        header=f'(kicad_sch (version 20250114) (generator "eeschema") (generator_version "10.0") (uuid {q(self.uuid)}) (paper "A3") (title_block (title {q(self.title)}) (date "{DATE}") (rev {q(self.d.revision)}) (company "ARDF-TX") (comment 1 "Evaluation review only; no ordering or manufacture")) (lib_symbols {defs}) '
        self.text(self.d.revision+': REVIEW / ALL hardware measurements NOT RUN / no ordering or manufacture.',15,280,0.95)
        (DEST/(self.name+'.kicad_sch')).write_text(header.rstrip()+'\n'+'\n'.join(self.items)+'\n(embedded_fonts no))\n')

class Design:
    def __init__(self):
        self.lib=Library(); self.parts={}; self.sheets=[]; self.root_uuid=uid('root');self.revision='M3A-R1'
        for spec in ['Device:R','Device:C','Device:L','Device:Crystal_GND24','Device:D','Device:D_Zener','Device:Fuse','Device:Thermistor_NTC','Transistor_FET:2N7002','Transistor_BJT:MMBT3904','Transistor_BJT:MMBT3906','Transistor_BJT:BD140','Device:Transformer_1P_1S','Regulator_Switching:TPS54302','Oscillator:Si5351A-B-GT','Power_Management:TPS22810DBV','Amplifier_Current:INA180A1','Reference_Voltage:TL431DBZ','74xx:74HC00','74xx:74HC14','74xx:74HC123','Comparator:LM339','Comparator:LM393','Connector_Generic:Conn_01x02','Connector_Generic:Conn_01x03','Connector_Generic:Conn_02x08_Odd_Even','Connector:TestPoint','power:PWR_FLAG']:
            self.lib.native(spec)
        self.lib.native('74xx:74LS174','74HC174'); self.lib.native('Device:C_Polarized'); self.lib.native('74xx:74LS08','74HC08'); self.lib.native('74xx:74LS32','74HC32'); self.lib.native('74xx:74LS74','74HC74'); self.lib.native('74xx:74LS21','74HC21'); self.lib.native('74xx:74LS11','74HC11')
        self.lib.native('74xx:74HC00','74AC00')
        self.lib.native('Reference_Voltage:TL431DBZ','TL431_TI_DBZ') # TI SLVS543S Table5-1:1K2REF3A
        self.lib.native('Transistor_BJT:BD140','BD140_ST',{'1':'3','3':'1'}) # ST Rev5 Fig1/p7:1B2C3E
        self.lib.native('Device:Q_PNP','MPS751',{'B':'2','C':'3','E':'1'}) # Central MPS751 physical1E2B3C
        self.lib.native('Device:D','BAT54WS')
        self.lib.native('Device:Q_NMOS','Q_NMOS_GDS',{'G':'1','D':'2','S':'3'})
        self.lib.box('LM5134B',{'1':('VDD','power_in'),'2':('PILOT','output'),'3':('OUT','output'),'4':('VSS','power_in'),'5':('INB','input'),'6':('IN','input')},['6','5','1'])
        self.lib.box('MCP100T300',{'1':('RESET_N','output'),'2':('VDD','power_in'),'3':('VSS','power_in')},['2','3'])
    def sheet(self,name,title):
        s=Sheet(self,name,title,len(self.sheets)+2); self.sheets.append(s); s.text(title,15,12,2); return s
    def save(self):
        DEST.mkdir(parents=True,exist_ok=True)
        for s in self.sheets:s.save()
        self.lib_path=DEST/'ARDF_TX.kicad_sym'
        self.lib_path.write_text('(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n'+'\n'.join(dump(d) for d in self.lib.defs.values())+'\n)\n')
        (DEST/'sym-lib-table').write_text('(sym_lib_table (lib (name "ARDF_TX") (type "KiCad") (uri "${KIPRJMOD}/ARDF_TX.kicad_sym") (options "") (descr "Flattened KiCad symbols plus pin-verified review symbols")))\n')
        sheets=[]
        for i,s in enumerate(self.sheets):
            x=20+(i%3)*130; y=45+(i//3)*42
            sheets.append(f'(sheet (at {x} {y}) (size 112 24) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid {q(s.uuid)}) (property "Sheetname" {q(s.title)} (at {x} {y-1.27} 0) (effects (font (size 1.27 1.27)) (justify left bottom))) (property "Sheetfile" {q(s.name+".kicad_sch")} (at {x} {y+26.27} 0) (effects (font (size 1.27 1.27)) (justify left top))) (instances (project "RF80" (path {q("/"+self.root_uuid)} (page {q(str(i+2))})))))')
        root=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(self.root_uuid)}) (paper "A3") (title_block (title "ARDF-TX 80 m RF module") (date "{DATE}") (rev {q(self.revision)}) (company "ARDF-TX / review only")) (lib_symbols) '+'\n'.join(sheets)
        root+='(text "Classic 3 W / 1.2 W; Sprint calibrated; independent Fox 10 mW\nNORMAL: protected 4S, 12.0-16.8 V. FOX-only: controller 3.3 V from 2S.\nNo 2 m changes. No production PCB. No measured prototype results.\nInter-sheet connections use explicit named global nets.\nRead docs/M3_80M_SCHEMATIC_REVIEW.md before use." (at 25 18 0) (effects (font (size 1.25 1.25)) (justify left top)) (uuid '+q(uid('root-note'))+')) (embedded_fonts no))\n'
        root=root.replace('\nNORMAL:',r'\nNORMAL:').replace('\nNo 2 m',r'\nNo 2 m').replace('\nInter-sheet',r'\nInter-sheet').replace('\nRead docs',r'\nRead docs')
        (DEST/'RF80.kicad_sch').write_text(root)
        # Do not overwrite a reviewer-edited project settings file on regeneration.
        if not (DEST/'RF80.kicad_pro').exists():
            (DEST/'RF80.kicad_pro').write_text(json.dumps({'meta':{'filename':'RF80.kicad_pro','version':1},'erc':{'erc_exclusions':[]},'schematic':{'meta':{'version':1}}},indent=2)+'\n')
        (DEST/'RF80.electrical.json').write_text(json.dumps({'date':DATE,'revision':self.revision,'status':'REVIEW / ALL HARDWARE MEASUREMENTS NOT RUN','parts':list(self.parts.values()),'placements':{s.name:s.placements for s in self.sheets}},indent=2)+'\n')

FP_R='Resistor_SMD:R_0603_1608Metric'; FP_C='Capacitor_SMD:C_0603_1608Metric'
FP_SO14='Package_SO:SOIC-14_3.9x8.7mm_P1.27mm'
FP_SO16='Package_SO:SOIC-16_3.9x9.9mm_P1.27mm'
def resistor_mpn(v):
    code=v.upper().replace('.','R')
    # Yageo RC0603 part numbering uses 4K7, 12K4, etc.
    if '.' in v:
        if v.endswith('k'): code=v[:-1].replace('.','K')
        else: code=v.replace('.','R')
    elif v.endswith('k'): code=v[:-1]+'K'
    elif v.endswith('M'): code=v[:-1]+'M'
    elif v=='0': return 'RC0603JR-070RL'
    elif not any(c.isalpha() for c in v): code=v+'R'
    return 'RC0603FR-07'+code+'L'

def build(m3b=False):
    d=Design()
    if m3b:d.revision='M3B-E2'
    def r(s,ref,v,a,b,x,y,pop='BOTH',group='protection',note='',fp=FP_R,mpn=None,price=None):
        s.place(ref,'R',v,{'1':a,'2':b},x,y,fp,mpn or resistor_mpn(v),group,pop,note=note,price=price)
    caps={'100n':('CC0603KRX7R8BB104',FP_C,.024),'1n':('CC0603JRNPO9BN102',FP_C,.04),'10n':('CC0603KRX7R9BB103',FP_C,.035),'1u':('CC0805KKX7R9BB105','Capacitor_SMD:C_0805_2012Metric',.08),'470n':('C3216X7R2A474K160AB','Capacitor_SMD:C_1206_3216Metric',.22),'4.7n':('CC0603JRNPO9BN472',FP_C,.04),'4.7u':('GRM31CR71E475KA88L','Capacitor_SMD:C_1206_3216Metric',.16),'10u35':('C3225X7R1V106M250AC','Capacitor_SMD:C_1210_3225Metric',.45),'22u25':('GRM32ER71E226KE15L','Capacitor_SMD:C_1210_3225Metric',.45),'100p':('C0805C101J1GACTU','Capacitor_SMD:C_0805_2012Metric',.10),'1000p':('C0805C102J1GACTU','Capacitor_SMD:C_0805_2012Metric',.10),'1800p':('C0805C182J1GACTU','Capacitor_SMD:C_0805_2012Metric',.12),'91p':('C0805C910J1GACTU','Capacitor_SMD:C_0805_2012Metric',.12)}
    def c(s,ref,v,a,b,x,y,pop='BOTH',group='decoupling',note=''):
        mpn,fp,p=caps[v];s.place(ref,'C',v,{'1':a,'2':b},x,y,fp,mpn,group,pop,note=note,price={'1':p})
    def fet(s,ref,gate,drain,source,x,y,pop='BOTH',group='protection',note=''):
        high_current=ref=='Q404'
        mpn='DMN2056U-7' if high_current else 'BSS138BK,215'
        s.place(ref,'2N7002',mpn,{'1':gate,'2':source,'3':drain},x,y,'Package_TO_SOT_SMD:SOT-23',mpn,group,pop,
            price={'1':.335,'10':.147,'100':.128} if high_current else {'1':.22,'10':.099,'100':.06},
            evidence='OBSERVED_M3' if high_current else 'MIXED_ESTIMATE',supplier='Mouser',code='621-DMN2056U-7' if high_current else '771-BSS138BK215',
            availability='Retained R0 stock observation' if high_current else 'EUR ten-price indexed0.099; single/100 estimates; EU stock conflict OPEN',
            source='https://www.diodes.com/datasheet/download/DMN2056U.pdf' if high_current else 'https://assets.nexperia.com/documents/data-sheet/BSS138BK.pdf',
            note=note+(' 45mohm at2.5V, +/-8VGS; retained for70mA shaper base sink.' if high_current else ' 60VDS,+/-20VGS;6.5ohm max at2.5V/10mA. Low-current function only; 1G2S3D. Ten-price observed; other prices estimates.'))
    def tp(s,ref,net,x,y,pop='BOTH'):
        s.place(ref,'TestPoint',net,{'1':net},x,y,'TestPoint:TestPoint_Pad_D1.0mm', 'PCB pad / no purchased component','test',pop,price={'1':0},evidence='BOARD_FEATURE',note='High-impedance probe; not a 50-ohm terminated scope input')
    def logic(s,ref,typ,pinmap,x,y,unit=1,pop='BOTH',price=.16):
        if typ=='74AC00':
            s.place(ref,typ,'SN74AC00DR',pinmap,x,y,FP_SO14,'SN74AC00DR','fox',pop,unit=unit,price={'1':.404,'10':.278,'25':.248,'100':.213},evidence='OBSERVED_M3',supplier='Mouser',code='595-SN74AC00DR',source='https://www.ti.com/lit/ds/symlink/sn74ac00.pdf',availability='2369EUindexed;ActiveDRcut-tapeMOQ1;D-tubeEOLnotselected',note='TinyFoxNANDbuffermechanism,ACdriveadaptation.2-6V,+/-12mAoperatingat3V. HC00driveaftershaping/padismarginal;3.3VfamilythresholdsnotTTL. ActualRFperformanceNOTMEASURED.')
            return
        source_name=typ if typ=='74HC21' else typ.replace('74HC','74HC_HCT')
        s.place(ref,typ,typ+'D,653',pinmap,x,y,FP_SO16 if typ in ('74HC123','74HC174') else FP_SO14,typ+'D,653','interlocks',pop,unit=unit,price={'1':price},supplier='Mouser',code='771-'+typ+'D-T',source='https://assets.nexperia.com/documents/data-sheet/'+source_name+'.pdf',note='CMOS 3.3 V. Supply unit and all unused gates explicitly connected.')
    s=d.sheet('01_source_interface','01 Controller interface and local source')
    s.text('One local Si5351; no MCU/RTC/UI on RF PCB. Shared 3.3 V stays powered during inhibited I2C setup.\nController wide-input regulator remains a proposal: evaluation fixture supplies bounded 3.3 V separately.',15,22)
    pins={'1':'V3V3','2':'GND','3':'SCL','4':'GND','5':'SDA','6':'LEASE','7':'ARM','8':'CW_KEY','9':'PA_REQ','10':'FOX_REQ','11':'PWR0','12':'PWR1','13':'MUTE_N','14':'FAULT_N','15':'PACK4_OK','16':'GND'}
    s.place('J101','Conn_02x08_Odd_Even','IDC16 controller',pins,65,65,'Connector_IDC:IDC-Header_2x08_P2.54mm_Vertical','Wurth 61201621621','connectors',price={'1':.60},note='Exact Wurth drawing/key orientation to verify; candidate footprint held for evaluation, harness contacts separate.',supplier='Wurth/Mouser',code='OPEN')
    s.place('U101','Si5351A-B-GT','SI5351A-B-GT',{'1':'V3V3','2':'XA','3':'XB','4':'SCL','5':'SDA','6':'CLK_FOX','7':'V3V3','8':'GND','9':None,'10':'CLK_PA'},170,62,'Package_SO:MSOP-10_3x3mm_P0.5mm','SI5351A-B-GT','source',price={'1':1.87,'10':1.388},evidence='OBSERVED_M2',supplier='DigiKey',code='336-2399-5-ND',availability='M2 indexed 10254; exact current EU basket OPEN',source='https://www.skyworksinc.com/-/media/SkyWorks/SL/documents/public/data-sheets/Si5351-B.pdf',note='0x60; CLK0 PA, CLK2 FOX; CLK1 disabled/NC; blank factory part, no preprogrammed outputs. Internal crystal load 10 pF starting setting.')
    s.place('Y101','Crystal_GND24','25 MHz / CL10 pF',{'1':'XA','2':'GND','3':'XB','4':'GND'},275,60,'Crystal:Crystal_SMD_5032-4Pin_5.0x3.2mm','ABM3B-25.000MHZ-10-1-U-T','source',price={'1':.40},note='Active manufacturer: +/-10ppm initial and stability, -10 to +60 C. Calibration/aging/loading remain measured. Not a TCXO.',supplier='Mouser/DigiKey',code='815-ABM3B-25-T / 300-8218-1-ND',availability='Mouser indexed 2381; net EUR price not captured',source='https://abracon.com/parametric/crystals/ABM3B-25.000MHZ-10-1-U-T')
    for ref,v,a,b,x,y in [('R101','4.7k','V3V3','SCL',55,115),('R102','4.7k','V3V3','SDA',120,115),('R103','100k','V3V3','FAULT_N',190,115)]:r(s,ref,v,a,b,x,y)
    for i,net in enumerate(['LEASE','ARM','CW_KEY','PA_REQ','FOX_REQ','PWR0','PWR1','MUTE_N','PACK4_OK']):
        r(s,'R'+str(110+i),'47k',net,'GND',35+(i%6)*60,158+(i//6)*43,note='Local default-off pull-down; do not remove in reduced population')
    c(s,'C101','100n','V3V3','GND',230,112);c(s,'C102','100n','V3V3','GND',285,112);c(s,'C103','1u','V3V3','GND',340,112)
    for i,net in enumerate(['V3V3','CLK_PA','CLK_FOX','SCL','GND']):tp(s,'TP'+str(101+i),net,220+(i%3)*65,205+(i//3)*38)
    s.text('Logical contract: 3.3 V only; V3V3 3.135-3.465 V, absolute connector maximum 3.6 V.\nRoutePAcurrentthroughdedicatedJ301return; checkcontrollerground-harnesscurrent. PA raw power has separate J301 and return.\nLEASE 20 Hz software-progress toggles; ARM low before changing frequency, path or power.\nAny SCL activity while armed trips the local latch. FAULT_N open drain, low when unarmed.\nDo not connect TTL 5 V inputs or an unqualified controller raw supply to this connector.',15,239,1.05)
    # Explicit supply origin flags; downstream flags are named in the review.
    for i,net in enumerate(['V3V3','GND']):
        s.place('#FLG10'+str(i),'PWR_FLAG','PWR_FLAG',{'1':net},390,220+i*30,'','','test',price={'1':0},evidence='BOARD_FEATURE')

    s=d.sheet('02_interlocks','02 Autonomous lease, inhibit and rearm')
    s.text('Healthy-only asynchronous reset. Latched fault cannot recover while ARM remains high.\nARM RC/Schmitt delay releases CLR before clocking. Requests exclusive; both asserted trips.',15,23)
    s.place('U201','MCP100T300','MCP100T-300I/TT',{'1':'POR_N','2':'V3V3','3':'GND'},55,58,'Package_TO_SOT_SMD:SOT-23','MCP100T-300I/TT','interlocks',price={'1':.361},evidence='OBSERVED_M2',source='https://ww1.microchip.com/downloads/en/DeviceDoc/11187f.pdf',supplier='Mouser',code='579-MCP100T-300I/TT',note='SOT23 pin1 RESET,2 VDD,3 VSS; nominal3.0V. Controller POR cannot replace unplugged-module local reset.')
    logic(s,'U202','74HC123',{'1':'LEASE_SEEN_N','2':'LEASE','3':'POR_N','4':None,'13':'LEASE_OK','14':'GND','15':'LEASE_RC'},150,55,unit=1,price=.219)
    logic(s,'U202','74HC123',{'9':'GND','10':'SCL','11':'POR_N','12':'BUS_HOLDOFF_N','5':None,'6':'GND','7':'BUS_RC'},255,55,unit=2,price=.219)
    logic(s,'U202','74HC123',{'16':'V3V3','8':'GND'},350,54,unit=3,price=.219)
    r(s,'R201','330k','V3V3','LEASE_RC',45,103);c(s,'C201','1u','LEASE_RC','GND',100,103,group='interlocks',note='t=KRC approx0.165s at assumedK0.50; characterize 3.3V,tolerance,temperature. Hardware silence<=250ms requirement.')
    r(s,'R202','47k','V3V3','BUS_RC',170,103);c(s,'C202','100n','BUS_RC','GND',225,103,group='interlocks',note='Approx2.35ms quiet delay at assumedK0.50; risingSCL and qualifiedRD-release trigger; test actual bound.')
    r(s,'R203','47k','ARM','ARM_RC',300,103);c(s,'C203','100n','ARM_RC','GND',360,103,group='interlocks')
    # Actual logic gates, with physical pin numbers.
    logic(s,'U203','74HC14',{'1':'ARM_RC','2':'ARM_DELAY_N'},40,149,unit=1)
    logic(s,'U203','74HC14',{'3':'ARM_DELAY_N','4':'ARM_CLK'},105,149,unit=2)
    logic(s,'U203','74HC14',{'5':'PA_REQ','6':'PA_REQ_N'},175,149,unit=3)
    logic(s,'U203','74HC14',{'9':'FOX_REQ','8':'FOX_REQ_N'},245,149,unit=4)
    logic(s,'U203','74HC14',{'11':'CW_KEY','10':'KEY_N'},315,149,unit=5)
    logic(s,'U203','74HC14',{'13':'KEY_TAIL_C','12':'KEY_TAIL_N'},380,149,unit=6)
    logic(s,'U203','74HC14',{'14':'V3V3','7':'GND'},380,205,unit=7)
    for i,u in enumerate(['U201','U202','U203']):c(s,'C'+str(210+i),'100n','V3V3','GND',35+i*62,205)
    fet(s,'Q201','NOT_ARMED','FAULT_N','GND',260,203,group='interlocks',note='Open-drain status; unarmed, not only faults. Pull on controller rail.')
    for ref,net,x in [('D201','LEASE_RC',45),('D202','BUS_RC',160)]:
        s.place(ref,'BAT54WS','BAT54WS-7-F',{'1':'V3V3','2':net},x,265,'Diode_SMD:D_SOD-323','BAT54WS-7-F','interlocks',price={'1':.10},source='https://www.diodes.com/datasheet/download/BAT54WS.pdf',note='HC123 manufacturer Fig13 discharge clamp across external timing R; anodeRC/cathodeVCC. Fig11 CEXT6/14 directlygrounded fornoiseimmunity. Qualifypowerdownsurgewithactual3.3Vreservoirandcable.')
    s.text('U202: first Q=pin13, /A=LEASE_SEEN_N; first validLEASE edge witnesses progress. Second /Q=pin12, /A=0,B=SCL.\nNo blind ISR heartbeat: controller advances LEASE only after schedule and bus-state checks.\nLocal mute is independent of firmware; hardware does not verify the requested frequency value.\nNormal key-up leaves driver active through the measured drain-envelope tail. ARM/MUTE kill immediately.',15,239,1.1)

    s=d.sheet('03_safety_logic','03 Reduced permission logic and population-specific guards')
    s.text('Four redundant gate stages are replaced by one core tree and wired open-collector PA trips.\nSchottky logic margins and source loading remain E1 bench gates; no CMOS outputs are tied together.',15,23)
    logic(s,'U211','74HC21',{'1':'UV_POR_N','2':'LEASE_OK','4':'BUS_QUIET','5':'MUTE_N','6':'CORE_OK'},60,60,unit=1)
    logic(s,'U211','74HC21',{'9':'CORE_OK','10':'EXCLUSIVE_OK','12':'MODE_OK','13':'PA_CONDITION_OK','8':'SAFE_RAW'},175,60,unit=2)
    logic(s,'U211','74HC21',{'14':'V3V3','7':'GND'},350,57,unit=3)
    logic(s,'U212','74HC00',{'1':'PA_REQ','2':'FOX_REQ','3':'EXCLUSIVE_OK'},60,115,unit=1,price=.103)
    logic(s,'U212','74HC00',{'4':'PWR0','5':'PWR1','6':'MODE_OK'},150,115,unit=2,price=.103)
    logic(s,'U212','74HC00',{'9':'KEY_TAIL_N','10':'KEY_TAIL_N','8':'KEY_TAIL'},240,115,unit=3,price=.103)
    logic(s,'U212','74HC00',{'12':'FOX_PERMIT','13':'KEY_TAIL','11':'FOX_MUTE'},335,115,unit=4,price=.103)
    logic(s,'U212','74HC00',{'14':'V3V3','7':'GND'},380,211,unit=5,price=.103)
    r(s,'R219','2.2k','V3V3','HEALTH_N',45,175,group='interlocks')
    r(s,'R220','2.2k','V3V3','UV_POR_N',145,175,group='interlocks')
    r(s,'R225','10k','PA_CONDITION_OK','GND',240,175,group='interlocks')
    def sd(ref,k,a,x,y,pop='BOTH',note=''):
        s.place(ref,'BAT54WS','BAT54WS-7-F',{'1':k,'2':a},x,y,'Diode_SMD:D_SOD-323','BAT54WS-7-F','interlocks',pop,price={'1':.10},source='https://www.diodes.com/datasheet/download/BAT54WS.pdf',note=note+' pin1K/pin2A; price estimate, MOQ1 assumed.')
    sd('D219','POR_N','UV_POR_N',45,230,note='AND reset/POR with direct UV open collector; a low POR sinks through diode.')
    sd('D220','SAFE_RAW','HEALTH_N',150,230,note='Independent open-drain request-withdrawal faults may clamp RESET_N; CMOS CLR_CORE_N is isolated.')
    sd('D221','PACK4_OK','PA_GUARD_RAW',250,230,'NORMAL','Controller pack qualification AND local analog trips.')
    sd('D222','FOX_ID','PA_GUARD_RAW',350,230,'NORMAL','Compact accessory present inhibits the watt path.')
    sd('D223','PA_CONDITION_OK','PA_REQ_N',45,270,note='Diode OR allows the low path when PA request is absent.')
    sd('D224','PA_CONDITION_OK','PA_GUARD_RAW',160,270,note='Diode OR requires all watt guards when PA request is present.')
    c(s,'C220','100n','V3V3','GND',240,270);c(s,'C222','100n','V3V3','GND',280,270)
    r(s,'R228','0','PA_GUARD_RAW','GND',350,175,'FOX','interlocks',note='Fox-only: forces watt guard invalid. Full population MUST omit this link.')

    s=d.sheet('04_arm_key','04 Deliberate rearm, witnessed heartbeat and captured configuration')
    logic(s,'U221','74HC11',{'1':'POR_N','2':'BUS_HOLDOFF_N','13':'BUS_LINES_HIGH','12':'BUS_QUIET'},60,55,unit=1)
    logic(s,'U221','74HC11',{'3':'ARMED','4':'PATH_PA','5':'ARM_ACCEPT','6':'PA_PERMIT'},160,55,unit=2)
    logic(s,'U221','74HC11',{'9':'ARMED','10':'PATH_FOX','11':'ARM_ACCEPT','8':'FOX_PERMIT'},270,55,unit=3)
    logic(s,'U221','74HC11',{'14':'V3V3','7':'GND'},370,55,unit=4)
    logic(s,'U222','74HC08',{'1':'HEALTH_N','2':'ARM','3':'RESET_N'},55,115,unit=1,price=.114)
    logic(s,'U222','74HC08',{'4':'PA_PERMIT','5':'CW_KEY','6':'PA_KEY'},155,115,unit=2,price=.114)
    logic(s,'U222','74HC08',{'9':'FOX_PERMIT','10':'CW_KEY','8':'FOX_KEY'},255,115,unit=3,price=.114)
    logic(s,'U222','74HC08',{'12':'SCL','13':'SDA','11':'BUS_LINES_HIGH'},355,115,unit=4,price=.114)
    logic(s,'U222','74HC08',{'14':'V3V3','7':'GND'},370,220,unit=5,price=.114)
    logic(s,'U223','74HC74',{'1':'RESET_N','2':'ARM_ACCEPT','3':'ARM_CLK','4':'V3V3','5':'ARMED','6':'NOT_ARMED'},65,170,unit=1,price=.123)
    logic(s,'U223','74HC74',{'13':'POR_N','12':'V3V3','11':'LEASE','10':'V3V3','9':None,'8':'LEASE_SEEN_N'},180,170,unit=2,price=.123)
    logic(s,'U223','74HC74',{'14':'V3V3','7':'GND'},320,220,unit=3,price=.123)
    logic(s,'U224','74HC174',{'1':'HEALTH_N','2':'SEL_EXT','3':'PWR0','4':'PWR1','5':'SEL_FULL','6':'PA_REQ','7':'PATH_PA','8':'GND','9':'ARM','10':'PATH_FOX','11':'FOX_REQ','12':'ARM_ACCEPT','13':'KEY_N','14':'GND','15':None,'16':'V3V3'},335,173,price=.25)
    d.parts['U224'].update(price_breaks_eur={'1':.35,'10':.25},supplier='Nexperia/DigiKey/Mouser',supplier_part_number='OPEN exact74HC174D,653 cut-tape SKU',evidence='ESTIMATE',availability='Nexperia Production; exact local basket OPEN; 175/Toshiba NRND not substituted',source_url='https://assets.nexperia.com/documents/data-sheet/74HC_HCT174.pdf')
    for i in range(4):c(s,'C'+str(230+i),'100n','V3V3','GND',35+i*60,220)
    # A selected request withdrawal is a persistent open-drain fault. Capture new
    # context on RAW ARM first; delayed ARM clock only arms after it has settled.
    fet(s,'Q225','PATH_PA','HEALTH_N','PA_DROP_MID',45,264,group='interlocks')
    fet(s,'Q226','PA_REQ_N','PA_DROP_MID','DROP_RETURN',110,264,group='interlocks')
    fet(s,'Q227','PATH_FOX','HEALTH_N','FOX_DROP_MID',175,264,group='interlocks')
    fet(s,'Q228','FOX_REQ_N','FOX_DROP_MID','DROP_RETURN',240,264,group='interlocks')
    fet(s,'Q229','ARM_ACCEPT','DROP_RETURN','GND',255,198,group='interlocks',note='Request faults only when captured context valid. HEALTH MR clears acceptance, independently masking RF; no implicit rearm.')
    s.text('U224 captures path/mode/key-low on raw ARM; any health fault clears acceptance.\nU223 delayed clock can only arm an accepted context. A fault in the pending delay cannot rearm.\nWithdraw selected request: health clears context and RF permits. New raw ARM edge required.\nFresh ARM low>=20ms, configure requests/mode, then ARM high; wait>=250ms before first key.\nMode changes while armed are ignored; mode11, conflicting requests and SCL/SDA low fault immediately.\nNo recovery with ARM held high. U213/U214 deleted; their duplicated tree is not retained.',15,236,1.0)
    # Supply sheet: full population only, independently powered logic remains shared.
    s=d.sheet('05_power','05 4S input, one buck and independent rail isolation')
    s.text('Shared J301/F301/D301 input barrier; converter/loadswitch NORMAL only. Protected4S:12.0-16.8V.\nFox-only retains input barrier/sense bypass, omits buck/loadswitch and watt-rail parts;2S powerscontroller+input sense.\nTPS22810 VIN must stay<=18V, including failed-buck transients;20V is absolute maximum.\n28V passive simulation is NOT a system rating. Input clamp/fault coordination remains OPEN.',15,23)
    s.place('J301','Conn_01x02','RAW protected pack',{'1':'VBAT','2':'GND'},35,60,'Connector_JST:JST_VH_B2P-VH_1x02_P3.96mm_Vertical','B2P-VH(LF)(SN)','connectors','BOTH',price={'1':.138,'10':.115},evidence='OBSERVED_M3',supplier='Mouser',code='306-B2P-VHLFSN',source='https://www.jst-mfg.com/product/pdf/eng/eVH.pdf',availability='108526 indexed EUR MOQ1',note='Pin1 positive,2 power return. Module input must come from externally protected/fused pack.')
    s.place('F301','Fuse','1.5 A fast / 32V',{'1':'VBAT','2':'VBAT_FUSED'},100,60,'Fuse:Fuse_1206_3216Metric','Littelfuse 046701.5NR','protection','BOTH',price={'1':.30},note='Selection candidate; final interrupt/I2t and max16.8V qualification OPEN. External protected pack remains required.')
    pack_net='VIN_PACK' if m3b else 'VIN_PA'
    s.place('D301','D','SS34',{'1':pack_net,'2':'VBAT_FUSED'},165,60,'Diode_SMD:D_SMC','SS34-E3/57T','protection','BOTH',price={'1':.18},note='Schottky reverse polarity barrier. M3B sense is ahead of added input damper; no load-dependent UV threshold shift.')
    s.place('D302','D_Zener','SMBJ17A TVS',{'1':'VIN_PA','2':'GND'},230,60,'Diode_SMD:D_SMB','SMBJ17A','protection','NORMAL',price={'1':.35},note='Secondary surge absorber only; NOT an18/20V precision clamp. M3B R350/C350 damp specified cable hot-plug; TVS is downstream of damper. External sources restricted to qualified4S envelope.')
    c(s,'C301','10u35','VIN_PA','GND',295,60,'NORMAL','supply');c(s,'C302','10u35','VIN_PA','GND',360,60,'NORMAL','supply')
    s.place('U301','TPS54302','TPS54302DDCT',{'1':'GND','2':'SW_PA','3':'VIN_PA','4':'FB_PA','5':'PA_PERMIT','6':'BOOT_PA'},65,122,'Package_TO_SOT_SMD:TSOT-23-6','TPS54302DDCT','normal_supply','NORMAL',price={'1':1.59,'10':1.18,'25':1.08},evidence='OBSERVED_M2',source='https://www.ti.com/lit/ds/symlink/tps54302.pdf',supplier='Mouser',code='595-TPS54302DDCT',availability='New EUR index3137; direct browser failed; basket OPEN',note='4.5-28V/3A; EN max7V, local47k pull-down. 400kHz. No raw16.8V on EN.')
    c(s,'C303','100n','BOOT_PA','SW_PA',155,120,'NORMAL','normal_supply');r(s,'R301','47k','PA_PERMIT','GND',220,120,'NORMAL','normal_supply')
    s.place('L301','L','10 uH >=3 A',{'1':'SW_PA','2':'VPA'},290,120,'ARDF_TX:SRP7050TA','SRP7050TA-100M','normal_supply','NORMAL',price={'1':.963,'10':.792,'25':.691},evidence='OBSERVED_M3',supplier='Mouser',code='652-SRP7050TA-100M',availability='CurrentEURindex; exactstocknumberOPEN',source='https://www.bourns.com/docs/product-datasheets/srp7050ta.pdf',note='10uH +/-20%,4Athermal,7.5AIsat (-20%L),69mohmmax. Exceeds TPS54302 worstcurrent-limitpeak (verifyhot). SRP5030TA-100M rejected:3.5AIsat insufficient faultmargin.')
    c(s,'C304','22u25','VPA','GND',350,120,'NORMAL','normal_supply');c(s,'C305','22u25','VPA','GND',350,170,'NORMAL','normal_supply')
    r(s,'R302','137k','VPA','FB_PA',35,175,'NORMAL','normal_supply',note='0.596V feedback typical; not RF power calibration. Base20k gives4.6786V start.')
    r(s,'R303','20k','FB_PA','GND',95,175,'NORMAL','normal_supply',note='Sprint calibration by selected fixed E96 value after RF measurement. Open lower resistor is hazardous: OV/latch/isolation are indispensable.')
    r(s,'R304','91k','FB_PA','FB_EXT',155,175,'NORMAL','normal_supply',note='Extended calibration starting value, no DAC/trimmer.')
    fet(s,'Q301','SEL_EXT','FB_EXT','GND',210,175,'NORMAL','normal_supply')
    r(s,'R305','24.9k','FB_PA','FB_FULL',260,175,'NORMAL','normal_supply',note='Full calibration starting value; max target3W, not a5W carrier adaptation.')
    fet(s,'Q302','SEL_FULL','FB_FULL','GND',310,175,'NORMAL','normal_supply')
    s.place('U302','TPS22810DBV','TPS22810DBVR',{'1':'VPA','2':'GND','3':'PA_PERMIT','4':'CT_PA','5':'QOD_PA','6':'VPA_ISO'},75,232,'Package_TO_SOT_SMD:SOT-23-6','TPS22810DBVR','normal_supply','NORMAL',price={'1':.52},source='https://www.ti.com/lit/ds/symlink/tps22810.pdf',note='Independent physical load switch after buck. Shorted buck high-side can still be disconnected. Not reverse-blocking; no external rail injection.')
    c(s,'C306','4.7n','CT_PA','GND',175,231,'NORMAL','normal_supply',note='4.7n slows initial47uFdrivercharge; measure inrush belowOC threshold and outputsettling. OFF latency is separately<=20us gate.')
    r(s,'R306','100','QOD_PA','VPA_ISO',235,231,'NORMAL','normal_supply');r(s,'R307','47k','PA_PERMIT','GND',300,231,'NORMAL','normal_supply')
    s.place('#FLG301','PWR_FLAG','PWR_FLAG',{'1':'VBAT'},360,230,'','','test','BOTH',price={'1':0},evidence='BOARD_FEATURE')

    s=d.sheet('06_analog_protection','06 Reference, pack voltage and thermal/current trips')
    s.text('Real electrical trips; no RF power detector or continuous telemetry. Comparator inputs stay below1.5V.\nShared reverse-protected J301 pack input retained for Fox-only; all PA converter/driver/final components DNP.',15,23)
    s.place('U311','TL431_TI_DBZ'if m3b else'TL431DBZ','TL431AIDBZR',({'1':'VREF_2V5','2':'VREF_2V5','3':'GND'}if m3b else{'1':'VREF_2V5','2':'GND','3':'VREF_2V5'}),45,60,'Package_TO_SOT_SMD:SOT-23','TL431AIDBZR','protection',price={'1':.25},source='https://www.ti.com/lit/ds/symlink/tl431.pdf',note='1 REF,2 anode,3 cathode. >=1mA reference bias; no capacitor directly across TL431 until stability region checked.')
    r(s,'R310','180','V3V3','VREF_2V5',110,60);r(s,'R311','1.5k','VREF_2V5','VREF_TH',175,60);r(s,'R312','1k','VREF_TH','GND',240,60);c(s,'C310','100n','VREF_TH','GND',305,60)
    r(s,'R313','309k',pack_net,'V_PACK_SCALED',40,108);r(s,'R314','10k','V_PACK_SCALED','GND',100,108);c(s,'C311','10n','V_PACK_SCALED','GND',160,108)

    # LM339 native comparator unit mapping:1 +7/-6/out1,2 +5/-4/out2,3 +9/-8/out14,4 +11/-10/out13.
    s.place('U312','LM339','LM339BIDR',{'5':'TEMP_SENSE','4':'TEMP_HOT_REF','2':'PA_GUARD_RAW'},55,161,'Package_SO:SOIC-14_3.9x8.7mm_P1.27mm','LM339BIDR','protection','NORMAL',unit=1,price={'1':.25},source='https://www.ti.com/lit/ds/symlink/lm339b.pdf')
    s.place('U312','LM339','LM339BIDR',{'7':'V_PACK_SCALED','6':'PACK_4S_REF','1':'PA_GUARD_RAW'},150,161,FP_SO14,'LM339BIDR','protection',unit=2)
    s.place('U312','LM339','LM339BIDR',{'11':'PA_OV_REF','10':'V_PA_OV','13':'PA_GUARD_RAW'},245,161,FP_SO14,'LM339BIDR','protection',unit=3)
    s.place('U312','LM339','LM339BIDR',{'9':'PA_OC_REF','8':'I_PA_FILTER','14':'PA_GUARD_RAW'},345,161,FP_SO14,'LM339BIDR','protection',unit=4)
    s.place('U312','LM339','LM339BIDR',{'3':'V3V3','12':'GND'},345,230,FP_SO14,'LM339BIDR','protection',unit=5)
    r(s,'R321','2.2k','V3V3','PA_GUARD_RAW',100,211,'NORMAL')
    c(s,'C313','100n','V3V3','GND',285,210,'NORMAL')
    c(s,'C314','100n',pack_net,'GND',380,60,group='protection')
    r(s,'R324','309k','VPA','V_PA_OV',35,249);r(s,'R325','10k','V_PA_OV','GND',100,249)
    s.text('Nominal backup: commonUV5.810V/4Sbackup11.070V postreversebarrier; railOV8.973V.\nController operational endpoint remains6.0/12.0V with hysteresis; cell-group BMS external.\nLocal pack sensing does not prove weakest-cell voltage. Hysteresis implemented by fault latch;\nrearm only after input exceeds qualified margin. Fox-only: watt guards DNP, R228 clamps PA_GUARD_RAW; UV comparator remains local.',175,244,1.0)

    rs=d.sheet('06b_thresholds','06b Independent threshold dividers')
    rs.text('Independent reference dividers from regulated TL431 node, not a loaded shared half-reference.\nPack and PA voltage signals divideby31.9; INA current signal divides by4. No comparator pin exceeds1.05V\nfor28V input/rail or3.465V current-sense saturation. Thermal divider ratios sharetheir own<1.0V node.',15,23)
    r(rs,'R315','127k','VREF_2V5','PACK_2S_REF',50,75);r(rs,'R316','10k','PACK_2S_REF','GND',115,75);c(rs,'C312','10n','PACK_2S_REF','GND',180,75)
    r(rs,'R317','61.9k','VREF_2V5','PACK_4S_REF',270,75);r(rs,'R318','10k','PACK_4S_REF','GND',345,75)
    r(rs,'R326','78.7k','VREF_2V5','PA_OV_REF',50,135);r(rs,'R327','10k','PA_OV_REF','GND',115,135)
    r(rs,'R328','69.8k','VREF_2V5','PA_OC_REF',270,135);r(rs,'R329','10k','PA_OC_REF','GND',345,135)
    rs.text('Calculated at2.495V reference: commonUV5.810V protectedinput;4Sbackup11.070V protectedinput;\nOV8.973V rail; currenttrip1.251A. AddmeasuredSS34drop forrawpackthreshold.\nController operation stillstopsatapproximately6.0/12.0V; cell-group BMSexternal.\nReferencebias180ohm supports>=1mA TL431cathodecurrentafterallparallelreferencebranchloads.\nCold/hotreference, comparatoroffset/inputbias, resistor tolerances andtripresponse mustbe measured.',15,200,1.27)

    s=d.sheet('07_current_thermal','07 PA current trip and case-temperature interlock')
    s.place('R330','R','0.05 ohm / 1% / 1W',{'1':'VPA_ISO','2':'VPA_LOAD'},45,60,'Resistor_SMD:R_2512_6332Metric','WSL2512R0500FEA','protection','NORMAL',price={'1':.18},note='High-side Kelvin shunt. No low-side bypass through grounded RF instruments.')
    s.place('U313','INA180A1','INA180A1IDBVT',{'1':'I_PA_RAW','2':'GND','3':'SENSE_PLUS','4':'SENSE_MINUS','5':'V3V3'},150,60,'Package_TO_SOT_SMD:SOT-23-5','INA180A1IDBVT','protection','NORMAL',price={'1':.96,'10':.70},source='https://www.ti.com/lit/ds/symlink/ina180.pdf',supplier='Mouser/DigiKey',code='595-INA180A1IDBVT / exact DigiKey code OPEN',availability='Mouser indexed2890; price0.96 one observed, ten0.70 ESTIMATE; R package OOS not substituted',note='Gain20V/V; pin3 IN+,4 IN-,5 VS for DBV. 26V CM. A1T packaging differs from unavailable A1R, same pinout.')
    r(s,'R331','10','VPA_ISO','SENSE_PLUS',240,60,'NORMAL');r(s,'R332','10','VPA_LOAD','SENSE_MINUS',300,60,'NORMAL');c(s,'C320','10n','SENSE_PLUS','SENSE_MINUS',360,60,'NORMAL','protection')
    r(s,'R333','30k','I_PA_RAW','I_PA_FILTER',40,112,'NORMAL');c(s,'C321','1n','I_PA_FILTER','GND',100,112,'NORMAL','protection');r(s,'R334','10k','I_PA_FILTER','GND',160,112,note='Shared default0V OC input with sensor DNP; valid only when watt stage DNP.')
    c(s,'C322','100n','V3V3','GND',220,112,'NORMAL')
    r(s,'R335','10k','VREF_TH','TEMP_SENSE',40,167,note='Pull from bounded<1.0V reference keeps comparator inputs in range at cold/open NTC.')
    s.place('TH301','Thermistor_NTC','10k NTC / B25-50=3380',{'1':'TEMP_SENSE','2':'GND'},100,167,'Resistor_SMD:R_0603_1608Metric','NCP18XH103F03RB','protection',price={'1':.10},source='https://www.murata.com/en-us/products/productdetail?partno=NCP18XH103F03RB',note='B25/50=3380K;3434K25/85referenceusedforapproximate80Ctrip,notconstantovertemperature. Manufacturerproductpageunavailable; supplier-hostedMuratasheetreviewrequired. Attach sensor thermally to IRF610 case; board0603 placement cannot substitute case sensing. Fox-only DNP; normal PA and thermal sensing absent; unused dual-comparator inputs grounded via R348/R349.')
    r(s,'R337','60.4k','VREF_TH','TEMP_HOT_REF',220,167);r(s,'R338','10k','TEMP_HOT_REF','GND',280,167)
    r(s,'R339','1.3k','VREF_TH','TEMP_OPEN_REF',340,167);r(s,'R340','10k','TEMP_OPEN_REF','GND',380,215)
    s.place('U314','LM393','LM393BIDR',{'3':'V_PACK_SCALED','2':'PACK_2S_REF','1':'UV_POR_N'},55,224,'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm','LM393BIDR','protection',unit=1,price={'1':.198,'10':.14,'25':.124},evidence='OBSERVED_M2',source='https://www.ti.com/lit/ds/symlink/lm393b.pdf',supplier='Mouser',code='595-LM393BIDR')
    s.place('U314','LM393','LM393BIDR',{'5':'TEMP_OPEN_REF','6':'TEMP_SENSE','7':'PA_GUARD_RAW'},160,224,'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm','LM393BIDR','protection',unit=2)
    s.place('U314','LM393','LM393BIDR',{'8':'V3V3','4':'GND'},255,224,'Package_SO:SOIC-8_3.9x4.9mm_P1.27mm','LM393BIDR','protection',unit=3)
    c(s,'C323','100n','V3V3','GND',200,262)
    r(s,'R348','0','TEMP_OPEN_REF','GND',40,262,'FOX',note='Unused LM393 half input low in Fox-only; full DNP.')
    r(s,'R349','0','TEMP_SENSE','GND',110,262,'FOX',note='Unused LM393 half input low in Fox-only; full DNP.')
    s.text('Current trip nominal1.251A (20*0.05ohm=1V/A); targetfaultmute<=100us; dividergain0.25V/A;7.5ustau.\nTemperature window detects hot/short and detached/open sensor; nominalhot ~80C case.\nValues/thermal contact, comparator tolerance, filtering and trip latency are qualification gates.',280,245,1.0)

    s=d.sheet('08_normal_rf','08 Proven normal RF core and QCX-derived drain shaping')
    s.text('RF core adapted from OpenARDF SignalSlinger HW3.5 (MIT); shaper principle from QCX/W6JL.\nKeep clock running during graceful key tail; INB immediately mutes on fault. This is NOT the VHF AM modulator.',15,23)
    s.place('U401','LM5134B','LM5134BMF/NOPB',{'1':'VDRV','2':None,'3':'GATE_DRV','4':'GND','5':'PA_INB','6':'CLK_PA'},70,70,'Package_TO_SOT_SMD:SOT-23-6','LM5134BMF/NOPB','normal_driver','NORMAL',price={'1':2.17,'10':1.62,'25':1.48},evidence='OBSERVED_M2',supplier='Mouser',code='595-LM5134BMF/NOPB',source='https://www.ti.com/lit/ds/symlink/lm5134.pdf',availability='EU stock conflict:510 US indexed; DE incoming30Nov. Local basket MUST close.',note='B only: VIH2.4V, VIL0.8V. VDD4-12.6V; no raw4S. IN can be powered while VDD off per14V input rating; verify leakage.')
    r(s,'R401','10k','VDRV','PA_INB',180,65,'NORMAL','normal_driver');fet(s,'Q401','PA_PERMIT','PA_INB','PA_MUTE_MID',245,65,'NORMAL','normal_driver');r(s,'R402','47k','PA_PERMIT','GND',315,65,'NORMAL','normal_driver')
    fet(s,'Q405','KEY_TAIL','PA_MUTE_MID','GND',335,115,'NORMAL','normal_driver',note='Series driver-mute sink requires genuineKEYtail aswellasPApermission; prevents shaperstartup burst.')
    c(s,'C401','100n','VDRV','GND',180,111,'NORMAL','normal_driver');c(s,'C402','1u','VDRV','GND',240,111,'NORMAL','normal_driver')
    r(s,'R410','4.7','VPA_LOAD','VDRV',40,95,'NORMAL','normal_driver',fp='Resistor_SMD:R_2512_6332Metric',mpn='CRCW25124R70FKEG',price={'1':.10},note='1W/pulse-rated candidate; with C404 limits driver dV/dt during buck failure. Pulse energy/part qualification OPEN.')
    s.place('C404','C_Polarized','47u / 25V',{'1':'VDRV','2':'GND'},120,95,'Capacitor_SMD:CP_Elec_6.3x5.9','25SVPF47M','normal_driver','NORMAL',price={'1':1.50,'10':.973,'50':.7506},evidence='OBSERVED_R1_INDEX',source='https://www.digikey.de/en/products/detail/panasonic-electronic-components/25SVPF47M/4204845',supplier='DigiKey',code='P16513CT-ND',availability='DE index48247; direct fetch cache miss; Active/cut tape MOQ1; basket recheck',note='Panasonic polymer47u25V +/-20%,30mohm max100kHz20C;235uA leakage max. C6 maker land gap2.1/outer9.1/width1.6 agrees native pads. Cmin37.6u, ESR<=0.5ohm over0-50C and isolation<=20us must qualify; no safety proof from ideal RC.')
    r(s,'R409','100k','PA_MUTE_MID','GND',335,145,'NORMAL','normal_driver',note='Deterministic intermediate source bias; inhibit FETs now +/-20VGS rated.')
    r(s,'R403','0','GATE_DRV','GATE_PA',55,126,'NORMAL','normal_driver',note='Default0ohm like reference; optionally2.2ohm for ringing ONLY after waveforms. Do not attach50ohm scope termination.')
    r(s,'R408','47k','CLK_PA','GND',315,111,'NORMAL','normal_driver',note='Local low default on driver input if shared source is unplugged/unpowered.')
    r(s,'R404','10k','GATE_PA','GND',120,126,'NORMAL','normal_driver')
    s.place('Q402','Q_NMOS_GDS','IRF610PBF-BE3',{'1':'GATE_PA','2':'DRAIN_PA','3':'GND'},55,190,'Package_TO_SOT_THT:TO-220-3_Vertical','IRF610PBF-BE3','normal_final','NORMAL',price={'1':1.11,'10':.622},evidence='OBSERVED_M2',supplier='Farnell',code='4853567',source='https://www.vishay.com/docs/91023/irf610.pdf',availability='614 DE indexed M2, exactBE3 lot/basket OPEN',note='200V VDS, +/-20V gate. Tab=drain; electrically insulating sink hardware required. Prototype drain peak gate<=100V, junctiontarget<=110C.')
    s.place('T401','Transformer_1P_1S','9T + 9T bifilar / FT-50A-43',{'1':'VPA_SHAPED','2':'DRAIN_PA','3':'DRAIN_PA','4':'RF_RAW'},165,190,'ARDF_TX:FT50A43_Bifilar_4Terminal','Amidon FT-50A-43 + AWG24 enamel Cu','normal_filter','NORMAL',price={'1':.95},source='https://www.amidoncorp.com/ft-50a-43/',supplier='Amidon/Akizuki',code='FT-50A-43 / Akizuki131662',note='Astart1 dot; Afinish2; Bstart3 dot; Bfinish4; 2 and3 join drain, series-aiding.9 passes each,24cm each AWG24 0.51mm. AL480nH ->38.9uH per winding; source geometryverify.')
    s.place('Q403','BD140_ST'if m3b else'BD140','BD140 / ST',({'1':'SHAPE_BASE','2':'VPA_SHAPED','3':'VPA_LOAD'}if m3b else{'1':'VPA_LOAD','2':'VPA_SHAPED','3':'SHAPE_BASE'}),280,170,'Package_TO_SOT_THT:TO-126-3_Vertical','BD140','normal_shaper','NORMAL',price={'1':.585,'10':.264,'100':.232},evidence='OBSERVED_M3',supplier='Mouser',code='511-BD140',source='https://www.st.com/resource/en/datasheet/bd140.pdf',availability='STActive;MouserDEindexed5060;basketOPEN',note=('ST1B2C3E Rev5 Fig1/p7 0016114E; correction of E1. 'if m3b else'HISTORICAL R1/E1 INCORRECT ST MAPPING:1E2C3B; DO NOT BUILD. ')+'80V1.5A,TO126. ReplacesQCXMPS751mechanismwithoutchangingtopology;betterthermal/SOAdata. HF CWshaper only, NOT VHF AM substitute. MeasurehotSOAandedges.')
    r(s,'R405','1k','VPA_LOAD','SHAPE_BASE',350,170,'NORMAL','normal_shaper')
    r(s,'R406','100','SHAPE_BASE','KEY_DRAIN',280,225,'NORMAL','normal_shaper',fp='Resistor_SMD:R_2512_6332Metric',mpn='CRCW2512100RFKEG',price={'1':.10},note='1W thin/thick-film qualified part; at8.98V approx0.65W. Adapted forced-beta10 base budget, not copied1.2k QCX.')
    fet(s,'Q404','PA_KEY','KEY_DRAIN','GND',350,225,'NORMAL','normal_shaper')
    c(s,'C403','22u25','VPA_SHAPED','SHAPE_BASE',210,225,'NORMAL','normal_shaper',note='Nonpolar X7R Miller integration starting value; bias-dependent effectiveC and measured3-8ms edges OPEN.')
    r(s,'R407','4.7k','VPA_SHAPED','GND',140,245,'NORMAL','normal_shaper',note='Discharge only, not bulk PA capacitor; do not add reservoir after shaper.')
    for i,net in enumerate(['GATE_PA','DRAIN_PA','VPA_SHAPED','RF_RAW']):tp(s,'TP'+str(401+i),net,30+i*55,268,'NORMAL')
    s.text('No PA/drain reservoir after shaper. Driver reservoir is upstream.\n9+9 series autotransformer: effective voltage step2:1, load~12.5ohm beforefilter.\nTransformer drawing is coupled coils; center join is external and explicit.\nAll components on this sheet DNP on Fox-only. No watt-to-Fox RF switching.',15,145,1.0)

    ks=d.sheet('08b_key_tail','08b Shared key-tail and disarm reset')
    ks.text('Path permission alone must not startRF during drain-integrator charging.\nNormal series INB sink needsPA_PERMIT andKEY_TAIL; FoxRFmute also requiresFOX_PERMIT andKEY_TAIL.\nTail usesraw CW_KEY; disarm clampsmemorybelowSchmittlow. KEYhighcannotarm; capturedpath+withdrawaltrippreventsRFtransfer.',15,23)
    r(ks,'R451','1k','CW_KEY','KEY_TAIL_SRC',50,75,group='interlocks')
    ks.place('D451','BAT54WS','BAT54WS-7-F',{'1':'KEY_TAIL_C','2':'KEY_TAIL_SRC'},125,75,'Diode_SMD:D_SOD-323','BAT54WS-7-F','interlocks','BOTH',price={'1':.10},source='https://www.diodes.com/datasheet/download/BAT54WS.pdf',note='SchottkyfastchargepreservesHC14VIHmargin;hotleakagemustbemeasured.Anodefrompermittedkey; cathodeatcapacitor. Fixed100nF/330ktailneedshot/coldSchmittthresholdmeasurement.')
    r(ks,'R452','330k','KEY_TAIL_C','GND',205,75,group='interlocks',note='Sharedkeytaildefaultlow; no RF untilagenuinepermittedkey.')
    c(ks,'C451','100n','KEY_TAIL_C','GND',280,75,group='interlocks')
    r(ks,'R453','100','KEY_TAIL_C','KEY_TAIL_RESET_D',50,140,group='interlocks')
    fet(ks,'Q406','NOT_ARMED','KEY_TAIL_RESET_D','GND',150,140,group='interlocks',note='10usresetRCclampsrawKEYevenifheldhigh; KEYhighcannotarm. Verify thresholds/leakage attemperature.')
    tp(ks,'TP450','KEY_TAIL_C',250,145);tp(ks,'TP451','KEY_TAIL',330,145)
    ks.text('RCtailtau33ms; actualholddependsdiodedrop/HC14hysteresis. Benchqualify10-80mshold,\nlongerthanthe3-8msRFdecay. ShorterfallcanclipRF; excessiveholdraisesidle/leakage.\nARMlow>=20ms clearsmemory. Afterarming wait>=250msbeforefirstkey, thenverifysettleddrain.\nA fault bypassesgracefuldecay: PApermission/driver/railoff immediately.\nRFcalculation usesgatechargefortheentire20%scheduledslot, notonlyCWmarktime.',15,210,1.27)

    s=d.sheet('09_normal_filter','09 Original 80 m elliptic filter and normal port')
    s.text('Retain SignalSlinger 80m values/topology: series470nF, two2.7uH, 1100/1800/1100pF,91pF acrosssecondcoil.\nSplit1100pF into1000+100pF for obtainable capacitors. Coil recipe is mandatory; no generic power inductors.',15,23)
    c(s,'C410','470n','RF_RAW','LPF_N1',45,70,'NORMAL','normal_filter')
    c(s,'C411','1000p','LPF_N1','GND',110,70,'NORMAL','normal_filter');c(s,'C412','100p','LPF_N1','GND',170,70,'NORMAL','normal_filter')
    s.place('L410','L','2.7 uH / 20T T60-2',{'1':'LPF_N1','2':'LPF_N2'},245,70,'ARDF_TX:T60_2_20T','Micrometals T60-2 + AWG24 Cu','normal_filter','NORMAL',price={'1':.85},supplier='TME',code='T60-2',source='https://datasheets.micrometals.com/T60-2-DataSheet.pdf',note='20T throughholepasses,46cm wire starting. AL6.5nH ->2.60uH nominal; authorlabels2.7uH, measure and trim for passband. OD15.24/15.75max,ID8.53/8.03min,height5.94/6.45maxmm.')
    c(s,'C413','1800p','LPF_N2','GND',320,70,'NORMAL','normal_filter')
    s.place('L411','L','2.7 uH / 20T T60-2',{'1':'LPF_N2','2':'RF_NORMAL'},110,135,'ARDF_TX:T60_2_20T','Micrometals T60-2 + AWG24 Cu','normal_filter','NORMAL',price={'1':.85},supplier='TME',code='T60-2',source='https://datasheets.micrometals.com/T60-2-DataSheet.pdf',note='Same20T recipe; keep inductors apart/non-coplanar for parasitic coupling evaluation. Material/source identity must be retained.')
    c(s,'C414','91p','LPF_N2','RF_NORMAL',180,135,'NORMAL','normal_filter');c(s,'C415','1000p','RF_NORMAL','GND',250,135,'NORMAL','normal_filter');c(s,'C416','100p','RF_NORMAL','GND',320,135,'NORMAL','normal_filter')
    s.place('J401','Conn_01x02','NORMAL 50ohm reference',{'1':'RF_NORMAL','2':'GND'},55,205,'TerminalBlock_Phoenix:TerminalBlock_Phoenix_MKDS-1-2-3.81_1x02_P3.81mm_Horizontal','1727010','connectors','NORMAL',price={'1':1.00},supplier='Phoenix/TME/DigiKey',code='1727010; distributorcode OPEN',source='https://www.phoenixcontact.com/en-us/products/pcb-terminal-block-mkds-1-2-381-1727010',note='Low-cost screw terminal, not controlled50ohm coax. Define test plane atPCB terminals and de-embed <=20mm paired adapter. Different fromJSTXHFox; fieldwire/counterpoise accessory independent.')
    for i,net in enumerate(['RF_RAW','LPF_N1','LPF_N2','RF_NORMAL','GND']):tp(s,'TP'+str(410+i),net,140+i*50,205,'NORMAL')
    s.text('Reference50ohm power: J401, calibrated adapter+dummyload. No antenna gain/ERP conversion on80m.\nLong antenna matcher remains separate: measured verticalwire+defined counterpoise, L-match/variometer.\nNormal match START range15-50uH fromDF1FO; exacttap/cap values requireinstalledimpedance.\nA screwterminal can save~4EUR versus Amphenol132134 SMA; reference-plane calibration remains mandatory.\nHarmonics/spurs must be measured after this filter across3.510-3.600MHz and everycalibratedsetting.',15,242,1.1)

    s=d.sheet('10_fox_rf','10 Independent Foxoring shaper and rail-following clock buffer')
    s.text('TinyFox three-gate mechanism with stronger SN74AC00DR; new rail-following NPN input + QCX-style low-current envelope.\nNo electrical RF connection to RF_RAW/RF_NORMAL. Nominal10mW is calibrated at separate J502, not inferred.',15,23)
    r(s,'R501','27','V3V3','FOX_FEED',40,65,group='fox',fp='Resistor_SMD:R_2512_6332Metric',mpn='RC2512FR-0727RL',price={'1':.08},note='Maximum available resistive DC power3.6^2/(4*27)=120mW beforepad; fixed source bound, not10mWcalibration.>=1dBpadkeepsgrossfaultavailablepower<100mW.')
    s.place('Q501','MMBT3906','MMBT3906,215',{'1':'FOX_BASE','2':'FOX_FEED','3':'VFOX'},125,65,'Package_TO_SOT_SMD:SOT-23','MMBT3906,215','fox',price={'1':.10},source='https://assets.nexperia.com/documents/data-sheet/MMBT3906.pdf',note='SOT23 1B2E3C. Rail shaped from3.3V; no directrawbattery rail.')
    r(s,'R502','1k','FOX_FEED','FOX_BASE',220,65,group='fox');r(s,'R503','1.5k','FOX_BASE','FOX_KEY_D',290,65,group='fox')
    fet(s,'Q502','FOX_KEY','FOX_KEY_D','GND',360,65,group='fox')
    c(s,'C501','1u','VFOX','FOX_BASE',40,119,group='fox',note='Starting integratorC; rise/fall must be3-8ms measured, especiallyHCbelow2V analoginterval.')
    c(s,'C502','100n','VFOX','GND',105,119,group='fox');r(s,'R504','1k','VFOX','GND',170,119,group='fox',note='Stored rail discharge/bounded tail;1k alsoadds~3mA active overhead.')
    r(s,'R505','10k','CLK_FOX','FOX_CLK_B',235,119,group='fox');r(s,'R506','100k','FOX_CLK_B','GND',295,119,group='fox')
    s.place('Q503','MMBT3904','MMBT3904,215',{'1':'FOX_CLK_B','2':'GND','3':'FOX_CLK'},360,119,'Package_TO_SOT_SMD:SOT-23','MMBT3904,215','fox',price={'1':.10},source='https://assets.nexperia.com/documents/data-sheet/MMBT3904.pdf',note='Collectorpull-up tracksVFOX, never pushes3.3V intounpoweredHCinput. Saturation/Bakerclamp delay qualification needed.')
    r(s,'R507','470','VFOX','FOX_CLK',40,175,group='fox')
    s.place('D501','BAT54WS','BAT54WS-7-F',{'1':'FOX_CLK','2':'FOX_CLK_B'},110,175,'Diode_SMD:D_SOD-323','BAT54WS-7-F','fox',price={'1':.10},source='https://www.diodes.com/datasheet/download/BAT54WS.pdf',note='Diodes SOD323: cathode marking matchespad1K,2A. Schottky A=base,K=collector. NOT interchangeable with BAT54 SOT23 pin1A,2NC,3K.')
    logic(s,'U501','74AC00',{'1':'FOX_CLK','2':'FOX_GATE_EN','3':'FOX_GATE1'},210,177,unit=1)
    logic(s,'U501','74AC00',{'4':'FOX_CLK','5':'FOX_GATE_EN','6':'FOX_GATE2'},305,177,unit=2)
    logic(s,'U501','74AC00',{'9':'FOX_CLK','10':'FOX_GATE_EN','8':'FOX_GATE3'},70,235,unit=3)
    logic(s,'U501','74AC00',{'12':'GND','13':'GND','11':None},175,235,unit=4)
    logic(s,'U501','74AC00',{'14':'VFOX','7':'GND'},280,235,unit=5)
    # Correct function group on the single IC, separate from fixed3.3V safety gates.
    d.parts['U501']['note']+=' Three NAND outputs feed separate22ohm ballast resistors. Supplyrampbelow2Vuncharacterized; calibration/shaping/spectralgate.'
    tp(s,'TP501','VFOX',355,237);tp(s,'TP502','FOX_CLK',310,210)
    r(s,'R508','10k','FOX_MUTE','FOX_MUTE_B',40,263,group='fox')
    s.place('Q504','MMBT3904','MMBT3904,215',{'1':'FOX_MUTE_B','2':'GND','3':'FOX_GATE_EN'},135,263,'Package_TO_SOT_SMD:SOT-23','MMBT3904,215','fox',price={'1':.10},note='IndependentRFgateafterPNPshaper. Masklowwhenunarmed,evenifQ501short. Railfollowingcollector avoidsbackpowerHCinput.')
    r(s,'R509','10k','VFOX','FOX_GATE_EN',225,263,group='fox')

    s=d.sheet('11_fox_filter','11 Separate Foxoring filter, calibration pad and protected compact port')
    r(s,'R510','22','FOX_GATE1','FOX_SUM',40,60,group='fox');r(s,'R511','22','FOX_GATE2','FOX_SUM',100,60,group='fox');r(s,'R512','22','FOX_GATE3','FOX_SUM',160,60,group='fox')
    c(s,'C510','470n','FOX_SUM','FOX_LPF1',225,60,group='fox')
    c(s,'C511','1000p','FOX_LPF1','GND',290,60,group='fox');c(s,'C512','100p','FOX_LPF1','GND',355,60,group='fox')
    for ref,a,b,x,y in [('L510','FOX_LPF1','FOX_LPF2',45,122),('L511','FOX_LPF2','FOX_PAD_IN',235,122)]:
        s.place(ref,'L','2.7uH +/-5%',{'1':a,'2':b},x,y,'ARDF_TX:78F_Axial','78F2R7J-RC','fox',price={'1':.30},source='https://www.bourns.com/docs/product-datasheets/78f_series.pdf',supplier='DigiKey/Mouser',code='OPEN; exactSKU78F2R7J-RC',note='Q>=50 at7.9MHz,SRF>=95MHz,DCR<=0.28ohm. Notforwattstage. VerifyQ/spectralresponseat3.55MHz; datasheetgeometrymax7.11x2.79mmpads10.16.')
    c(s,'C513','1800p','FOX_LPF2','GND',105,122,group='fox');c(s,'C514','91p','FOX_LPF2','FOX_PAD_IN',170,122,group='fox');c(s,'C515','1000p','FOX_PAD_IN','GND',295,122,group='fox');c(s,'C516','100p','FOX_PAD_IN','GND',355,122,group='fox')
    r(s,'R513','750','FOX_PAD_IN','GND',40,181,group='fox',note='50ohm pi pad start1.17dB. Calibrate fixedset; no less1dB permitted onthisguardbudget.')
    r(s,'R514','6.8','FOX_PAD_IN','RF_FOX',105,181,group='fox',note='Seriespi pad6.8ohm; selectE96 during10mWcalibration. Source/current/lossmodelrequireshardwareevidence.')
    r(s,'R515','750','RF_FOX','GND',170,181,group='fox')
    s.place('J502','Conn_01x03','FOX ONLY / compact',{'1':'RF_FOX','2':'GND','3':'FOX_ID'},250,181,'Connector_JST:JST_XH_B3B-XH-A_1x03_P2.50mm_Vertical','B3B-XH-A(LF)(SN)','connectors',price={'1':.16},source='https://www.jst-mfg.com/product/pdf/eng/eXH.pdf',supplier='Mouser',code='306-B3BXHALFSNP',note='Plugshorts3to2. MismatchedwithJ401normalterminalandJ301VH. No wattroutingoption. CompactaccessoryandmatinghousingnotboardBOM.')
    r(s,'R516','10k','V3V3','FOX_ID',330,181,group='fox',note='Absent=high enables normalwhenrequested. Presentlow inhibitsnormalregardlessfirmware; Disarmbeforeplugchanges; JSTXHdoesnotguaranteesequentialmating.')
    c(s,'C517','10n','FOX_ID','GND',380,181,group='fox',note='Plugbouncefilter; no claimofsequentialcontactsforJSTXH, ARM mustbeinhibitedbeforeplugchanges.')
    for i,net in enumerate(['FOX_SUM','FOX_PAD_IN','RF_FOX','GND']):tp(s,'TP'+str(510+i),net,35+i*75,237)
    s.text('J502 reference plane: pin1 RF/pin2 definedreturn; use shorttwistedpair coaxadapter sharedfixture.\nCompactaccessory: ~30 cmradiator+definedcompactreturn; tune independentloading/couplingcartridge.\nStartingTinyFoxreference100uH plus1.6-15pF; effectiveC5-15pF mayrequire134-402uH.\nExact30cm geometry/tap/coil/capvalues OPEN untilantenna impedance measurement; no Classicwire substitute.\nNominal10mW in50ohm and30maudible/250minaudible are TWO distinct acceptance tests.',15,252,1.05)
    # Explicit downstream power flags identify passive/switched supply origins.
    for sname,net,x,y in [('05_power','VPA',40,255),('05_power','VIN_PA',140,255),('07_current_thermal','VPA_LOAD',240,260),('10_fox_rf','VFOX',380,215),('08_normal_rf','VDRV',390,140)]:
        sh=next(ss for ss in d.sheets if ss.name==sname)
        sh.place('#FLG'+str(len(d.parts)),'PWR_FLAG','PWR_FLAG',{'1':net},x,y,'','','test','NORMAL' if net!='VFOX' else 'BOTH',price={'1':0},evidence='BOARD_FEATURE')
    normal_refs={'U312','R311','R312','C310','R317','R318','R324','R325','R326','R327','R328','R329','R334','R335','R337','R338','R339','R340','TH301'}
    for ref in normal_refs:d.parts[ref]['population']='NORMAL'
    return d

def footprints():
    """Individual package land patterns; deliberately no board, outline or placement."""
    path=DEST/'ARDF_TX.pretty';path.mkdir(exist_ok=True)
    def make(name,desc,pads,body,kind='through_hole',radius=None):
        bx,by=body
        txt=f'(footprint {q(name)} (version 20240108) (generator "pcbnew") (layer "F.Cu") (descr {q(desc)}) (attr {"through_hole" if kind=="through_hole" else "smd"}) '
        for prop,y,layer in [('Reference',-by/2-2,'F.SilkS'),('Value',by/2+2,'F.Fab')]:
            txt+=f'(property {q(prop)} {q("REF**" if prop=="Reference" else name)} (at 0 {y} 0) (layer {q(layer)}) (effects (font (size 1 1) (thickness 0.15)))) '
        txt+=f'(fp_rect (start {-bx/2} {-by/2}) (end {bx/2} {by/2}) (stroke (width 0.1) (type default)) (layer "F.Fab")) '
        if radius:txt+=f'(fp_circle (center 0 0) (end {radius} 0) (stroke (width 0.12) (type default)) (fill none) (layer "F.SilkS")) '
        for n,x,y,w,h,drill in pads:
            txt+=f'(pad {q(n)} {"thru_hole" if drill else "smd"} {"rect" if n=="1" or not drill else "oval"} (at {x} {y}) (size {w} {h}) '
            if drill:txt+=f'(drill {drill}) (layers "*.Cu" "*.Mask")) '
            else:txt+='(layers "F.Cu" "F.Paste" "F.Mask")) '
        xs=[abs(x)+w/2 for _,x,_,w,_,_ in pads];ys=[abs(y)+h/2 for _,_,y,_,h,_ in pads]
        cx=max(bx/2,max(xs))+.5;cy=max(by/2,max(ys))+.5
        txt+=f'(fp_rect (start {-cx} {-cy}) (end {cx} {cy}) (stroke (width 0.05) (type default)) (layer "F.CrtYd")))\n'
        (path/(name+'.kicad_mod')).write_text(txt)
    make('SRP7050TA','Bourns SRP7050TA leadframe; manufacturer recommended outerwidth8.4,gap2.5,padheight3.5; 7.3x6.6mm body. Source srp7050ta.pdf p1.', [('1',-2.725,0,2.95,3.5,0),('2',2.725,0,2.95,3.5,0)],(7.6,6.9),kind='smd')
    make('78F_Axial','Bourns78F bodymax7.11x2.79mm,lead0.51mm. Axiallead forming10.16mm pitch; prototypebend verificationrequired.', [('1',-5.08,0,2,2,.9),('2',5.08,0,2,2,.9)],(7.11,2.79))
    make('FT50A43_Bifilar_4Terminal','HandwoundAmidonFT50A43,12.7OD7.92ID6.35H;9TtwoAWG24wires.1Astart/2Afinish/3Bstart/4Bfinish;2+3externalcenter. Own4leadprototypepattern; formingnotmanufacturerpackage.', [('1',-9,-3,2.2,2.2,1),('2',-9,3,2.2,2.2,1),('3',9,-3,2.2,2.2,1),('4',9,3,2.2,2.2,1)],(17,17),radius=7.4)
    make('T60_2_20T','HandwoundMicrometalsT60-2,maxcoated15.75OD6.45H;20TAWG24. Own20mmformedleadpitch,coreandleadgeometrymustbedry-fitted.', [('1',-10,0,2.2,2.2,1),('2',10,0,2.2,2.2,1)],(18,18),radius=8.4)
    (DEST/'fp-lib-table').write_text('(fp_lib_table (lib (name "ARDF_TX") (type "KiCad") (uri "${KIPRJMOD}/ARDF_TX.pretty") (options "") (descr "Four verified-dimension prototype packages; no PCB layout")))\n')

def cost_workbook(d):
    # Same-MPN purchasing is pooled per population. Estimates stay explicit;
    # no reel assumption and no invented distributor part numbers.
    parts=[p for p in d.parts.values() if not p['ref'].startswith('#') and not p['ref'].startswith('TP')]
    import m1_costs
    known={v['mpn']:v for v in m1_costs.PARTS.values()}
    for p in parts:
        if p['mpn'] in known and p['evidence'] in ('OBSERVED_M2','ESTIMATE'):
            previous=known[p['mpn']]
            for key in ('price_breaks_eur','supplier','supplier_part_number','availability','source_url'):
                p[key]=copy.deepcopy(previous[key])
            p['evidence']='OBSERVED_M2';p['note']+=' Dated M2 distributor observation; no fresh basket verification.'
        if p['ref']=='U313':p['evidence']='MIXED_ESTIMATE';p['note']+=' Quantity10EUR0.70 isESTIMATE; EUR0.96 at1 observed.'
        if p['ref']=='U203':
            p['price_breaks_eur']={'1':.172,'10':.118,'25':.104,'100':.086};p['evidence']='OBSERVED_M3';p['source_url']='https://www.mouser.es/ProductDetail/Nexperia/74HC14D653?qs=P62ublwmbi8OHaKXqv2GmQ%3D%3D';p['availability']='Mouser indexed862904; actualbasketOPEN'
        if p['ref']=='U211':
            p['price_breaks_eur']={'1':.241,'10':.166,'25':.148,'100':.127};p['evidence']='OBSERVED_M3';p['availability']='IndexedCanada18895,EURSpainprice; localizedbasketOPEN'
        if p['ref'] in ('U202','U212','U213','U222','U223'):
            # Mandatory actual1/10/25 breaks, not a ten-piece price applied at1.
            p['evidence']='OBSERVED_M2'
            if p['mpn'] not in known:
                p['price_breaks_eur']=({'1':.172,'10':.103,'100':.081}if p['ref']=='U212' else p['price_breaks_eur'])
                p['availability']='M2 indexedNexperia SOICstock; exactcurrentcut-tapebasketOPEN'
    sets={
      'Full module components':[p for p in parts if p['population'] in ('BOTH','NORMAL')],
      'Foxoring-only components':[p for p in parts if p['population'] in ('BOTH','FOX')],
      'RF final transistor alone':[p for p in parts if p['ref']=='Q402'],
      'RF power stage: final + gate links/bleed + transformer':[p for p in parts if p['ref'] in ('Q402','R403','R404','T401')],
      'Normal stage + drive/shaper/filter/supply/input and output hardware': [p for p in parts if p['group'] in ('normal_final','normal_driver','normal_shaper','normal_filter','normal_supply') or p['ref'] in ('F301','D301','D302','J301','J401','C301','C302','C314')],
      'Incremental NORMAL population; shared circuits excluded': [p for p in parts if p['population']=='NORMAL']
    }
    results={};csvrows=[]
    for name,ps in sets.items():
        results[name]={}
        for n in (6,10,20):
            pools=defaultdict(list)
            for p in ps:pools[p['mpn']].append(p)
            total=0;obs=0;groups=defaultdict(float);lines=[]
            for mpn,pp in pools.items():
                p=pp[0];needed=len(pp)*n;ordered=math.ceil(max(needed,p['moq'])/p['multiple'])*p['multiple']
                br=max(int(k)for k in p['price_breaks_eur']if int(k)<=ordered)
                price=p['price_breaks_eur'][str(br)];cash=ordered*price;total+=cash
                observed=p['evidence'].startswith('OBSERVED')
                if observed:obs+=cash
                for part in pp:
                    value=cash/len(pp)/n;groups[part['group']]+=value
                    line={**part,'scope':name,'batch':n,'needed_mpn':needed,'ordered_mpn':ordered,'leftover_mpn':ordered-needed,'unit_price_eur':price,'line_per_unit_eur':round(value,6),'price_break':br}
                    lines.append(line);csvrows.append(line)
            results[name][str(n)]=dict(per_unit_eur=round(total/n,4),batch_eur=round(total,4),observed_per_unit_eur=round(obs/n,4),estimate_per_unit_eur=round((total-obs)/n,4),groups={k:round(v,4)for k,v in groups.items()},lines=lines)
    output=ROOT/'docs/M3_80M_COSTS.json';output.write_text(json.dumps({'date':DATE,'currency':'EUR NET; VAT separate','status':'Engineering candidate, not released ordering list','scopes':results},indent=2)+'\n')
    fields=['scope','batch','ref','value','mpn','footprint','group','population','supplier','supplier_part_number','evidence','availability','source_url','moq','multiple','needed_mpn','ordered_mpn','leftover_mpn','price_break','unit_price_eur','line_per_unit_eur','note']
    with (ROOT/'docs/M3_80M_BOM.csv').open('w')as f:
        writer=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore',lineterminator='\n');writer.writeheader();writer.writerows(csvrows)
    out=['# M3A component workbook','',f'Date: {DATE}. EUR net. **Candidate, no ordering authorization.** Estimates are unquoted; observed rows retain index/date/localization limits. Repeated MPN order quantities are purchase pools: sum line_per_unit_eur, never repeated ordered_mpn.', '', '| Scope | 6 EUR/unit | 10 | 20 | Observed / estimate at ten |','| --- | ---: | ---: | ---: | --- |']
    for name,rr in results.items():out.append(f"| {name} | {rr['6']['per_unit_eur']:.2f} | {rr['10']['per_unit_eur']:.2f} | {rr['20']['per_unit_eur']:.2f} | {rr['10']['observed_per_unit_eur']:.2f} / {rr['10']['estimate_per_unit_eur']:.2f} |")
    out+=['','Full scope includes all populated PCB connectors. Excludes bare PCB, sinks/insulators, battery, antenna accessories, wiring/harness mates, enclosure, charging, labor and shared instruments; these are separately budgeted in [BOM review](M3_80M_BOM.md).','', '| Group / full module | 6 | 10 | 20 |','| --- | ---: | ---: | ---: |']
    for g in results['Full module components']['6']['groups']:
        out.append('| '+g+' | '+' | '.join(f"{results['Full module components'][str(n)]['groups'][g]:.2f}"for n in(6,10,20))+' |')
    out+=['','| Refs | Value; MPN | Footprint | Source / supplier code / MOQ | Evidence / stock | Unit EUR 6 / 10 / 20 | Full row EUR 6 / 10 / 20 |','| --- | --- | --- | --- | --- | ---: | ---: |']
    grouped=defaultdict(list)
    for p in sets['Full module components']:grouped[p['mpn']].append(p)
    for mpn,pp in sorted(grouped.items(),key=lambda kv:kv[1][0]['ref']):
        p=pp[0];prices=[];tot=[]
        for n in (6,10,20):
            ls=[l for l in results['Full module components'][str(n)]['lines']if l['mpn']==mpn]
            prices.append(f"{ls[0]['unit_price_eur']:.4f}");tot.append(f"{sum(l['line_per_unit_eur']for l in ls):.3f}")
        source=f"[source]({p['source_url']})"if p['source_url']else'Unquoted; manufacturer/supplier check OPEN'
        out.append(f"| {', '.join(p['ref']for p in pp)} | {p['value']}; {mpn} | {p['footprint']} | {source}; {p['supplier']} {p['supplier_part_number']}; MOQ{p['moq']} | {p['evidence']}; {p['availability']} | {' / '.join(prices)} | {' / '.join(tot)} |")
    out+=['','Each component and pin mapping is in [electrical manifest](../hardware/80m/RF80.electrical.json). CSV has per-reference population/order/quantity information. Fixed calibration resistor replacements and spare winding material are additional prototype material, not implicit free items.']
    (ROOT/'docs/M3_80M_COMPONENT_WORKBOOK.md').write_text('\n'.join(out)+'\n')
    return results

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    d=build()
    if args.write:
        # Population/evidence updates precede CAD manifest export.
        cost=cost_workbook(d);d.save();footprints()
        print(f'Wrote {len(d.sheets)+1} KiCad sheets, {len(d.parts)} manifest rows')
        print({k:{n:v['per_unit_eur']for n,v in b.items()}for k,b in cost.items()})
    else: print(f'Manifest constructed: {len(d.parts)} rows; use --write to regenerate review CAD')
if __name__=='__main__':main()
