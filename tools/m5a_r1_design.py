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
DEST = ROOT / 'hardware/2m'
LIB = Path('/usr/share/kicad/symbols')
DATE = '2026-10-15'
NAMESPACE = uuid.UUID('a4e579ae-51fa-472c-95eb-83847ab72452')
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
        self.items.append(f'(symbol (lib_id {q("ARDF_2M:"+typ)}) (at {x} {y} {angle}) (unit {unit}) (in_bom {"no" if ref.startswith("TP") else "yes"}) (on_board yes) (dnp {"yes" if pop not in ("ALL","NORMAL","BOOST2S") else "no"}) (uuid {q(ident)}) '+
            ''.join(f'(property {q(k)} {q(v)} (at {x+5 if typ in ("R","C","L") else x} {y-h-4+i*1.6 if i<2 else y} 0) '+
            f'(effects (font (size {1.0 if i<2 else 1.27} {1.0 if i<2 else 1.27})) '+ ('(hide yes)' if i>=2 else '') + ')) '
            for i,(k,v) in enumerate([('Reference',ref),('Value',value),('Footprint',foot),('Datasheet',source),('MPN',mpn),('Population',pop),('Function',group),('Engineering_Note',note),('Status','EVALUATION / NOT RELEASED')]))+
            f'(instances (project "RF2M" (path {q("/"+self.d.root_uuid+"/"+self.uuid)} (reference {q(ref)}) (unit {unit})))) )')
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
                    for variant,value in p.get('variant_values',{}).items():
                        sx.append(parse('(property '+q('Variant_'+variant+'_Value')+' '+q(value)+' (at 0 0 0)(effects(font(size 1 1))(hide yes)))'))
                    if p.get('manufacturer'):
                        old=next((v for v in children(sx,'property')if v[1]=='Manufacturer'),None)
                        if old:old[2]=p['manufacturer']
                        else:sx.append(parse('(property \"Manufacturer\" '+q(p['manufacturer'])+' (at 0 0 0)(effects(font(size 1 1))(hide yes)))'))
                    item=dump(sx)
            revised.append(item)
        self.items=revised
        defs=' '.join(dump(self.d.lib.defs[t]).replace('(symbol '+q(t)+' ', '(symbol '+q('ARDF_2M:'+t)+' ',1) for t in sorted(self.used))
        header=f'(kicad_sch (version 20250114) (generator "eeschema") (generator_version "10.0") (uuid {q(self.uuid)}) (paper "A2") (title_block (title {q(self.title)}) (date "{DATE}") (rev {q(self.d.revision)}) (company "ARDF-TX") (comment 1 "Evaluation review only; no ordering or manufacture")) (lib_symbols {defs}) '
        self.text(self.d.revision+': REVIEW / ALL hardware measurements NOT RUN / no ordering or manufacture.',15,397,0.95)
        (DEST/(self.name+'.kicad_sch')).write_text(header.rstrip()+'\n'+'\n'.join(self.items)+'\n(embedded_fonts no))\n')

class Design:
    def __init__(self):
        self.lib=Library(); self.parts={}; self.sheets=[]; self.root_uuid=uid('root');self.revision='M3A-R1'
        self.revision='M5A-R1'
        for spec in ['Device:R','Device:R_Potentiometer','Device:C','Device:C_Polarized','Device:L','Device:Crystal_GND24','Device:D','Device:D_Zener','Device:Fuse','Device:Thermistor_NTC','Transistor_FET:2N7002','Transistor_FET:AO3401A','Transistor_BJT:MMBT3904','Transistor_BJT:MMBT3906','Transistor_BJT:BD139','Device:Q_PNP','Device:Q_NMOS','Oscillator:Si5351A-B-GT','Regulator_Switching:TPS54302','Amplifier_Current:INA180A1','Reference_Voltage:TL431DBZ','74xx:74HC14','Comparator:LM339','Connector_Generic:Conn_01x02','Connector_Generic:Conn_01x03','Connector_Generic:Conn_02x10_Odd_Even','Connector:Conn_Coaxial','Connector:TestPoint','power:PWR_FLAG']:
            self.lib.native(spec)
        for n in ['174','08','32','86','11']:
            self.lib.native('74xx:74LS'+n,'74HC'+n)
        # Same physical logic pins, selected HC SOIC orderable variants. The
        # inherited generic LS/DIP drawing filter must describe that package.
        for typ in ['74HC174','74HC14','74HC11','74HC08','74HC32']:
            child_filter=next(p for p in children(self.lib.defs[typ],'property')if p[1]=='ki_fp_filters')
            child_filter[2]='SOIC*3.9x9.9mm*'if typ=='74HC174'else'SOIC*3.9x8.7mm*'
        self.lib.native('Device:Q_PNP','D45H11_ST',{'B':'1','C':'2','E':'3'})
        self.lib.native('Transistor_BJT:BD139','BD139_ST',{'1':'3','3':'1'})
        self.lib.native('Device:Q_NMOS','PD54008_Functional')
    def sheet(self,name,title):
        s=Sheet(self,name,title,len(self.sheets)+2); self.sheets.append(s); s.text(title,15,12,2); return s
    def save(self):
        DEST.mkdir(parents=True,exist_ok=True)
        for s in self.sheets:s.save()
        self.lib_path=DEST/'ARDF_2M.kicad_sym'
        self.lib_path.write_text('(kicad_symbol_lib (version 20231120) (generator "kicad_symbol_editor")\n'+'\n'.join(dump(d) for d in self.lib.defs.values())+'\n)\n')
        (DEST/'sym-lib-table').write_text('(sym_lib_table (lib (name "ARDF_2M") (type "KiCad") (uri "${KIPRJMOD}/ARDF_2M.kicad_sym") (options "") (descr "Flattened KiCad symbols plus pin-verified review symbols")))\n')
        sheets=[]
        for i,s in enumerate(self.sheets):
            x=20+(i%3)*190; y=65+(i//3)*65
            sheets.append(f'(sheet (at {x} {y}) (size 170 34) (stroke (width 0.254) (type default)) (fill (color 0 0 0 0)) (uuid {q(s.uuid)}) (property "Sheetname" {q(s.title)} (at {x} {y-1.27} 0) (effects (font (size 1.27 1.27)) (justify left bottom))) (property "Sheetfile" {q(s.name+".kicad_sch")} (at {x} {y+36} 0) (effects (font (size 1.27 1.27)) (justify left top))) (instances (project "RF2M" (path {q("/"+self.root_uuid)} (page {q(str(i+2))})))))')
        note='M5A-R1: 144 MHz TRUE AM / EVALUATION SCHEMATIC / NOT RELEASED\\n1 W ERP sizing: 1.259 W connector carrier, 4.079 W PEP at m=0.80.\\n2S BOOST or 4S BUCK exclusive populations; training needs only controller 3.3 V.\\nBLOCKING: ST VHF matching not traced; PD54008 PowerFLAT numeric pads OPEN. NO LAYOUT.\\nOPEN: hot SOA, analog loop, RF AM and physical driver-fault response.\\nNo PCB/layout/Gerbers/procurement. All physical results NOT_RUN. See docs/M5A_R1_REVIEW_DECISION.md.'
        note=note.replace(chr(92)+'n',chr(10))
        root=f'(kicad_sch (version 20250114) (generator "eeschema") (uuid {q(self.root_uuid)}) (paper "A2") (title_block (title "ARDF-TX 2 m A2A evaluation schematic") (date "{DATE}") (rev {q(self.revision)}) (company "ARDF-TX / NOT RELEASED")) (lib_symbols) '+'\n'.join(sheets)
        root+='(text '+q(note)+' (at 20 30 0)(effects(font(size 2 2))(justify left top))(uuid '+q(uid('root-note'))+')) (embedded_fonts no))\n'
        (DEST/'RF2M.kicad_sch').write_text(root)
        # Do not overwrite a reviewer-edited project settings file on regeneration.
        if not (DEST/'RF2M.kicad_pro').exists():
            (DEST/'RF2M.kicad_pro').write_text(json.dumps({'meta':{'filename':'RF2M.kicad_pro','version':1},'erc':{'erc_exclusions':[],'rule_severities':{'footprint_filter':'warning'}},'schematic':{'meta':{'version':1}}},indent=2)+'\n')
        (DEST/'RF2M.electrical.json').write_text(json.dumps({'date':DATE,'revision':self.revision,'status':'REVIEW / ALL HARDWARE MEASUREMENTS NOT RUN','parts':list(self.parts.values()),'placements':{s.name:s.placements for s in self.sheets}},indent=2)+'\n')


FP_R='Resistor_SMD:R_0603_1608Metric'
FP_C='Capacitor_SMD:C_0603_1608Metric'
FP_SO14='Package_SO:SOIC-14_3.9x8.7mm_P1.27mm'
FP_SO16='Package_SO:SOIC-16_3.9x9.9mm_P1.27mm'
TI='https://www.ti.com/lit/ds/symlink/'

def build():
    d=Design()
    # Functional terminal labels intentionally avoid inventing numeric PowerSO-10RF pads.
    # No fabricated footprint is supplied for unresolved RF package geometry.
    custom={
      'TPS3431':{'1':('VDD','power_in'),'2':('CWD','input'),'3':('EN','input'),'4':('GND','power_in'),'5':('SET1','input'),'6':('WDI','input'),'7':('WDO_N','open_collector'),'8':('ENOUT_N','open_collector'),'9':('PAD_GND','passive')},
      'TLV803E':{'1':('GND','power_in'),'2':('RESET_N','open_collector'),'3':('VDD','power_in')},
      'TPS611781':{'1':('FREQ','input'),'2':('AGND','power_in'),'3':('ILIMIT','input'),'4':('COMP','output'),'5':('FB','input'),'6':('PGND','power_in'),'7':('SW','power_out'),'8':('VOUT','power_in'),'9':('DISDRV','output'),'10':('VCC','power_out'),'11':('EN','input'),'12':('VIN','power_in'),'13':('BST','passive')},
      'TLV761':{'1':('GND','power_in'),'2':('OUT_TAB','power_out'),'3':('IN','power_in')},
      'PHA1':{'1':('RF_IN','input'),'2':('GND_LEAD','power_in'),'3':('RF_OUT_DC5V','output'),'4':('GROUND_PADDLE','passive')},
      'TLV9004_SO14':{'1':('OUT_A','output'),'2':('IN_A_N','input'),'3':('IN_A_P','input'),'4':('VDD','power_in'),'5':('IN_B_P','input'),'6':('IN_B_N','input'),'7':('OUT_B','output'),'8':('OUT_C','output'),'9':('IN_C_N','input'),'10':('IN_C_P','input'),'11':('VSS','power_in'),'12':('IN_D_P','input'),'13':('IN_D_N','input'),'14':('OUT_D','output')},
      'LVC3157':{'1':('B2_KEY1','passive'),'2':('GND','power_in'),'3':('B1_KEY0','passive'),'4':('A_COMMON','passive'),'5':('VCC','power_in'),'6':('SELECT','input')},
      'LVC2G66':{'1':('1Y','passive'),'2':('1Z','passive'),'3':('2E','input'),'4':('GND','power_in'),'5':('2Y','passive'),'6':('2Z','passive'),'7':('1E','input'),'8':('VCC','power_in')},
      'LVC2G08':{'1':('1A','input'),'2':('1B','input'),'3':('2Y','output'),'4':('GND','power_in'),'5':('2A','input'),'6':('2B','input'),'7':('1Y','output'),'8':('VCC','power_in')},
      'LVC125':{'1':('OE_N','input'),'2':('A','input'),'3':('GND','power_in'),'4':('Y','output'),'5':('VCC','power_in')},
      'TPS22919':{'1':('VIN','power_in'),'2':('GND','power_in'),'3':('ON','input'),'4':('NC','no_connect'),'5':('QOD','passive'),'6':('VOUT','power_out')},
    }
    for n,p in custom.items():d.lib.box(n,p)
    state={'s':None,'i':0,'n':0,'section':''}
    def section(name,title,note=''):
        state.update(s=d.sheet(name,title),i=0,n=0,section=name,title=title)
        if note:state['s'].text(note,18,24,1.1)
    def p(ref,typ,value,pins,fp,mpn,group,pop='ALL',cost=.03,price=None,source='',evidence='ESTIMATE',supplier='OPEN',code='OPEN',stock='Not independently basket-confirmed',note='',unit=1):
        if state['i']>=30:
            state['n']+=1;state['s']=d.sheet(state['section']+'b'+str(state['n']),state['title']+' continued');state['i']=0
        i=state['i'];state['i']+=1
        state['s'].place(ref,typ,value,pins,62+(i%5)*112,65+(i//5)*57,fp,mpn,group,pop,unit=unit,price=price or {'1':cost},source=source,evidence=evidence,supplier=supplier,code=code,availability=stock,note=note)
    def r(ref,v,a,b,g='passive',pop='ALL',cost=.02,fp=FP_R,mpn=None,note=''):
        code=v.replace('.','R') if '.' in v else v+'R'
        if v.endswith('k'):
            raw=v[:-1];code=raw.replace('.','K') if '.' in raw else raw+'K'
        elif v.endswith('M'):code=v[:-1]+'M'
        elif v=='0':code='0R'
        package=re.search(r'R_(\d{4})_',fp).group(1)
        p(ref,'R',v,{'1':a,'2':b},fp,mpn or ('RC'+package+'JR-070RL'if v=='0'else'RC'+package+'FR-07'+code+'L'),g,pop,cost=cost,note=note,source='https://www.yageo.com/en/ProductCategory/Resistors')
    def c(ref,v,a,b,g='decoupling',pop='ALL',rf=False,cost=.045,mpn=None,fp=FP_C,note=''):
        known={'100n':'CC0603KRX7R8BB104','1n':'CC0603JRNPO9BN102','4.7n':'CC0603JRNPO9BN472','1u':'CC0805KKX7R9BB105','4.7u':'GRM31CR71E475KA88L','22u':'GRM32ER71E226KE15L','10u':'C3225X7R1V106M250AC'}
        if v.endswith('p'):
            pf=float(v[:-1]);digits=(str(int(pf))+'0')if pf<100 else str(int(pf/10))+'1'
            # RF capacitors use exact family/nominal, vendor MPN remains OPEN unless checked.
            chosen=mpn or ('OPEN: C0G100V '+v if g in('output_filter','pa_match')else'OPEN: 0603 C0G50V '+v)
        else:chosen=mpn or known.get(v,'OPEN: '+v+' voltage/ESR qualification')
        if fp==FP_C and v in('1u','4.7u','22u','10u'):
            fp={'1u':'Capacitor_SMD:C_0805_2012Metric','4.7u':'Capacitor_SMD:C_1206_3216Metric','22u':'Capacitor_SMD:C_1210_3225Metric','10u':'Capacitor_SMD:C_1210_3225Metric'}[v]
        p(ref,'C_Polarized'if v in('100u','150u','330u')else'C',v,{'1':a,'2':b},fp,chosen,g,pop,cost=cost,note=note+(' VHF C0G; Q/SRF and exact MPN OPEN.'if rf else''))
    def l(ref,v,a,b,g,pop='ALL',power=False):
        selected={'24n':'0805CS-240XJRC','11n':'0805HP-11NXJRC','27n':'0805HP-27NXJRC','47n':'0805HP-47NXJRC','56n':'0805HP-56NXJRC','82n':'0805HP-82NXJRC','91n':'0805CS-910XJRC','180n':'0805HP-181XJRC'}
        p(ref,'L',v,{'1':a,'2':b},'Inductor_SMD:L_0805_2012Metric'if not power else'Inductor_SMD:L_Bourns_SRR1260',selected.get(v,'OPEN: '+('shielded power inductor 'if power else'RF tuning inductor ')+v),g,pop,cost=.92/1.1195 if not power else.85,source=('https://www.coilcraft.com/en-us/products/rf/ceramic-core-chip-inductors/0805-%282012%29/0805cs/0805cs-240/'if v=='24n'else'https://www.coilcraft.com/en-us/products/rf/ceramic-core-chip-inductors/0805-%282012%29/0805cs/0805cs-910/'if v=='91n'else'https://www.coilcraft.com/en-us/products/rf/ceramic-core-chip-inductors/0805-%282012%29/0805hp/')if not power else'',supplier='Coilcraft / authorized distributor'if not power else'OPEN',code=selected.get(v,'OPEN'),note='Manufacturer family verified.USD0.92 family price /ECB1.1195 conversion is an allowance, exact value checkout OPEN; footprint pad geometry OPEN before layout.91n CS used only low-drive filters. Power inductors require Isat>=6A boost or>=3A buck.' )
    def bjt(ref,typ,b,cc,e,g,pop='ALL',mpn=None,cost=.07):
        mpn=mpn or ('MMBT3904,215'if typ=='MMBT3904'else typ)
        pins={'1':b,'2':e,'3':cc}
        fp='Package_TO_SOT_SMD:SOT-23'
        if typ=='BD139_ST':pins={'1':b,'2':cc,'3':e};fp='Package_TO_SOT_THT:TO-126-3_Vertical';mpn='BD139';cost=.34
        if typ=='D45H11_ST':pins={'1':b,'2':cc,'3':e};fp='Package_TO_SOT_THT:TO-220-3_Vertical';mpn='D45H11';cost=.95
        p(ref,typ,mpn,pins,fp,mpn,g,pop,cost=cost,source='https://www.st.com/resource/en/datasheet/d45h11.pdf'if typ=='D45H11_ST'else'https://www.st.com/resource/en/datasheet/bd139.pdf'if typ=='BD139_ST'else'https://assets.nexperia.com/documents/data-sheet/MMBT3904.pdf'if typ=='MMBT3904'else'')
    def fet(ref,g,dr,so,group,pop='ALL',pfet=False):
        typ='AO3401A'if pfet else'2N7002'
        p(ref,typ,typ,{'1':g,'2':so,'3':dr},'Package_TO_SOT_SMD:SOT-23',typ if pfet else'2N7002,215',group,pop,cost=.18 if pfet else.07,source='https://www.aosmd.com/res/data_sheets/AO3401A.pdf'if pfet else'https://assets.nexperia.com/documents/data-sheet/2N7002.pdf',note='AO3401A -30V, +/-12VGS; clamp required. Exact manufacturer/suffix before ordering.'if pfet else'1G 2S 3D; manufacturer fixed before ordering.')
    def gate(ref,typ,unit,pins):
        p(ref,typ,typ+'D,653',pins,FP_SO16 if typ=='74HC174'else FP_SO14,typ+'D,653','interlock',cost=.28 if typ!='74HC174'else .48,source='https://assets.nexperia.com/documents/data-sheet/'+('74HC_HCT'+typ[4:]if typ not in('74HC11',)else'74HC_HCT11')+'.pdf',unit=unit,note='3.3 V CMOS. Each physical package counted once; every unused input tied.')
    def dec(ref,rail='V3V3',pop='ALL'):c(ref,'100n',rail,'GND',pop=pop)
    def tp(ref,net):p(ref,'TestPoint',net,{'1':net},'TestPoint:TestPoint_Pad_D1.0mm','PCB feature','test',cost=0,evidence='BOARD_FEATURE',note='High impedance probing. No terminated 50-ohm scope on logic/PA drain.')

    section('01_interface_source','01 Interface and local Si5351 source','144.5-144.9 MHz championship; other channels only under valid country profile.\nSCL activity clears ARM. Source supply/bus isolated when off. No RF claims until spectrum measurements.')
    interface=['V3V3','GND','I2C_SDA','I2C_SCL','ARM','SLOT','KEY','PROGRESS','MUTE_N','PA_RAIL_ADC','PATH_TRAIN','PROFILE_FULL','AF_PWM','LEVEL_PWM','PREPARE','FAULT_N','GND','GND','MODULE_ID','PA_PREPARE']
    p('J101','Conn_02x10_Odd_Even','Controller 20 pin',dict(zip(map(str,range(1,21)),interface)),'Connector_IDC:IDC-Header_2x10_P2.54mm_Vertical','OPEN keyed 20pin 2.54mm','connector',cost=.65,note='Controller input maximum 3.465V; power/ground sequencing in interface document. No battery current in this header.')
    r('R101','12.1k','MODULE_ID','GND','interface');r('R102','4.7k','V3V3','I2C_SCL','interface');r('R103','4.7k','V3V3','I2C_SDA','interface')
    for i,n in enumerate(['ARM','SLOT','KEY','PROGRESS','MUTE_N','PATH_TRAIN','PROFILE_FULL','PREPARE','PA_PREPARE'],104):r('R'+str(i),'100k',n,'GND','interface')
    for i,n in enumerate(['AF_PWM','LEVEL_PWM'],115):r('R'+str(i),'100k',n,'GND','interface')
    p('U101','TPS22919','TPS22919DCKR',{'1':'V3V3','2':'GND','3':'SRC_ON','4':None,'5':'VCLK','6':'VCLK'},'Package_TO_SOT_SMD:SOT-363_SC-70-6','TPS22919DCKR','source',cost=.25,source=TI+'tps22919.pdf',note='SLVSEN5B table:1IN2GND3ON4NC5QOD6OUT; no substituted similar switch pinout.')
    p('U102','LVC2G66','SN74LVC2G66DCUR',{'1':'I2C_SCL','2':'SCL_CLK','3':'SRC_ON','4':'GND','5':'I2C_SDA','6':'SDA_CLK','7':'SRC_ON','8':'V3V3'},'Package_SO:VSSOP-8_2.3x2mm_P0.5mm','SN74LVC2G66DCUR','source',cost=.33,source=TI+'sn74lvc2g66.pdf',note='OFF isolation avoids Si5351 I2C backpower; bus <400kHz, pullups host side.')
    p('U103','Si5351A-B-GT','Si5351A-B-GT',{'1':'VCLK','2':'XTAL1','3':'XTAL2','4':'SCL_CLK','5':'SDA_CLK','6':'CLK_TRAIN','7':'VCLK','8':'GND','9':None,'10':'CLK_NORMAL'},'Package_SO:MSOP-10_3x3mm_P0.5mm','Si5351A-B-GT','source',cost=1.35,source='https://www.skyworksinc.com/-/media/SkyWorks/SL/documents/public/data-sheets/Si5351-B.pdf',note='Divide-by-6 MS0 and MS2, shared PLL 6*f; CLK1 disabled. Internal crystal load selected/calibrated. Initial/temp/aging total gate <50ppm.')
    p('Y101','Crystal_GND24','25MHz CL10p 10/10ppm',{'1':'XTAL1','2':'GND','3':'XTAL2','4':'GND'},'Crystal:Crystal_SMD_3225-4Pin_3.2x2.5mm','ABM8-25.000MHZ-10-B1U-T','source',cost=.35,note='10pF load matches Si5351 setting; 10ppm initial/10ppm temperature listing, aging/pulling calibration and manufacturer footprint confirmation OPEN.')
    dec('C101');dec('C102','VCLK');c('C103','1u','VCLK','GND');tp('TP101','CLK_NORMAL');tp('TP102','CLK_TRAIN')

    section('02_interlocks','02 Minimal independent fail-off and captured ARM context','Raw ARM rising edge captures valid context, path and profile. ARM RC delays RF permission only.\nNo live path transfer. Any fault, reset, SCL-low or heartbeat expiry clears context; recovery needs a fresh ARM edge.')
    p('U201','TPS3431','TPS3431SDRBR',{'1':'V3V3','2':'CWD','3':'V3V3','4':'GND','5':'V3V3','6':'PROGRESS','7':'SAFE_N','8':'SAFE_N','9':'GND'},'Package_SON:VSON-8-1EP_3x3mm_P0.65mm_EP1.65x2.4mm','TPS3431SDRBR','interlock',cost=.85,source=TI+'tps3431.pdf',note='Fixed 200ms via CWD 10k to VDD. Falling WDI every <=100ms; tWD170-230ms. No first-edge witness claim; 170-230ms startup reset.')
    r('R201','10k','CWD','V3V3');r('R202','10k','SAFE_N','V3V3');dec('C201')
    p('U208','TLV803E','TLV803EA29DBZR',{'1':'GND','2':'SAFE_N','3':'V3V3'},'Package_TO_SOT_SMD:SOT-23','TLV803EA29DBZR','interlock',cost=.19,source=TI+'tlv803e.pdf',note='Open-drain reset; exact A29 threshold/delay and 1GND2RESET3VDD table verification required.')
    gate('U202','74HC174',1,{'1':'CLR_N','2':'VALID_ARM','3':'ARM_CONTEXT','4':'PATH_TRAIN','5':'PATH_Q','6':'PROFILE_FULL','7':'PROFILE_Q','8':'GND','9':'ARM','10':None,'11':'GND','12':None,'13':'GND','14':'GND','15':None,'16':'V3V3'})
    for u,ins,out in [(1,'KEY','KEY_N'),(2,'SLOT','SLOT_N'),(3,'PATH_Q','NORMAL_Q'),(4,'ARM_RC','ARM_DELAY_N'),(5,'ARM_DELAY_N','ARM_DELAY'),(6,'NORMAL_PERMIT','NORMAL_OFF')]:
        pins=[(1,2),(3,4),(5,6),(9,8),(11,10),(13,12)][u-1];gate('U203','74HC14',u,{str(pins[0]):ins,str(pins[1]):out})
    gate('U203','74HC14',7,{'7':'GND','14':'V3V3'})
    for u,pins in [(1,{'1':'PREPARE','2':'KEY_N','13':'SLOT_N','12':'ARM_CONTEXT'}),(2,{'3':'SAFE_N','4':'MUTE_N','5':'I2C_SCL','6':'CLEAR_A'}),(3,{'9':'VALID_ARM','10':'ARM_DELAY','11':'SLOT','8':'TX_A'}),(4,{'7':'GND','14':'V3V3'})]:gate('U204','74HC11',u,pins)
    for ref,units in [('U205',[(1,'CLEAR_A','RUN_HEALTH','CLR_N'),(2,'TX_A','ARM','TX_OK'),(3,'TX_OK','NORMAL_Q','NORMAL_BASE'),(4,'NORMAL_BASE','POWER_FAULT_N','NORMAL_RAW')]),('U206',[(1,'TX_OK','PATH_Q','TRAIN_RAW'),(2,'PREPARE','MUTE_N','PREPARE_OK'),(3,'PA_PREPARE','SRC_ON','CONV_EN'),(4,'PREPARE_OK','SAFE_N','SRC_ON')])]:
        for u,a,b,y in units:
            pp=[(1,2,3),(4,5,6),(9,10,8),(12,13,11)][u-1];gate(ref,'74HC08',u,dict(zip(map(str,pp),[a,b,y])))
        gate(ref,'74HC08',5,{'7':'GND','14':'V3V3'})
    for u,a,b,y in [(1,'POWER_FAULT_N','PATH_Q','PWR_OR_TRAIN'),(2,'PWR_OR_TRAIN','ARM_DELAY_N','RUN_HEALTH'),(3,'GND','GND',None),(4,'GND','GND',None)]:
        pp=[(1,2,3),(4,5,6),(9,10,8),(12,13,11)][u-1];gate('U207','74HC32',u,dict(zip(map(str,pp),[a,b,y])))
    gate('U207','74HC32',5,{'7':'GND','14':'V3V3'})
    p('U209','LVC2G08','SN74LVC2G08DCUR',{'1':'NORMAL_RAW','2':'CLEAR_A','3':'TRAIN_PERMIT','4':'GND','5':'TRAIN_RAW','6':'CLEAR_A','7':'NORMAL_PERMIT','8':'V3V3'},'Package_SO:VSSOP-8_2.3x2mm_P0.5mm','SN74LVC2G08DCUR','interlock',cost=.18,source=TI+'sn74lvc2g08.pdf',note='Direct common inhibit ahead of physical enables, independent of HC174 asynchronous output skew. Final-gate propagation/reset timing still physical tests.')
    dec('C209')
    r('R203','10k','ARM','ARM_RC');c('C202','1u','ARM_RC','GND');r('R204','100k','NORMAL_PERMIT','GND');r('R205','100k','TRAIN_PERMIT','GND')
    for i in range(203,209):dec('C'+str(i))
    # Fault feedback is low for invalid/cleared ARM, wired separately from analog comparator bus.
    r('R206','1k','VALID_ARM','FAULT_N','interlock')
    for i,n in enumerate(['SAFE_N','CLR_N','VALID_ARM','ARM_DELAY','NORMAL_PERMIT','TRAIN_PERMIT'],201):tp('TP'+str(i),n)

    section('03_input_power','03 External protected pack and exclusive conversion populations','J301: 2S 6.0-8.4V for BOOST population OR 4S 12.0-16.8V for BUCK population.\nNever fit both J302 straps. Pack/window component population is a hardware configuration, not automatic universal routing.')
    p('J301','Conn_01x02','Protected pack',{'1':'BAT_RAW','2':'GND'},'','OPEN keyed 2S/4S power connector','connector','NORMAL',cost=.40)
    p('F301','Fuse','4A fast / qualify I2t',{'1':'BAT_RAW','2':'BAT_FUSED'},'Fuse:Fuse_1206_3216Metric','0466004.NRHF','input','NORMAL',cost=.50,source='https://www.littelfuse.com/assetdocs/fuse-466-datasheet?assetguid=dbe9bcd7-6072-4adf-bf5b-d33e52a6b90f',note='Littelfuse466series32VAC/DC50Ainterrupt,1206,4A code004. Candidate selected from manufacturer2023table; stock/price/landing and prospective fault-current coordination OPEN. Old2A lacks low-battery transmit-slot margin.0.50EUR ESTIMATE, not quote. Local1.8A PA trip retained; fuse is wiring/secondary fault protection, not PA current control.')
    # Reverse PFET: drain faces battery; source body diode initially charges protected rail.
    fet('Q309','REVERSE_GATE','BAT_FUSED','VIN_PROT','input','NORMAL',True)
    r('R314','10k','REVERSE_GATE','GND','input','NORMAL')
    p('D307','D_Zener','10V reverse-FET gate clamp',{'1':'VIN_PROT','2':'REVERSE_GATE'},'Diode_SMD:D_SOD-123F','BZT52H-C10,115','input','NORMAL',cost=.05,note='Source-to-gate clamp; raw16.8V never applied as full VGS. Reverse body diode oriented BAT_FUSED->VIN_PROT.')
    p('D302','D_Zener','SMBJ18A',{'1':'VIN_PROT','2':'GND'},'Diode_SMD:D_SMB','SMBJ18A-E3/52','input','NORMAL',cost=.20,source='https://www.vishay.com/docs/88392/smbj.pdf',note='Not guaranteed to clamp below 20V. 30V frontend/fault test gate; no direct unrestricted Li-ion bringup.')
    c('C301','10u','VIN_PROT','GND','input','NORMAL',cost=.30);c('C302','100n','VIN_PROT','GND','input','NORMAL')
    fet('Q305','INPUT_GATE','VIN_CONV','VIN_PROT','input','NORMAL',True)
    r('R310','4.7k','INPUT_GATE','VIN_PROT','input','NORMAL');r('R311','1k','INPUT_GATE','INPUT_SINK','input','NORMAL');bjt('Q306','MMBT3904','INPUT_ENABLE_BASE','INPUT_SINK','GND','input','NORMAL');r('R312','4.7k','PACK_RUN','INPUT_ENABLE_BASE','input','NORMAL');r('R313','100k','INPUT_ENABLE_BASE','GND','input','NORMAL')
    p('D306','D_Zener','10V input gate clamp',{'1':'VIN_PROT','2':'INPUT_GATE'},'Diode_SMD:D_SOD-123F','BZT52H-C10,115','input','NORMAL',cost=.05)
    p('U304','LVC2G08','SN74LVC2G08DCUR',{'1':'CONV_EN','2':'PACK_OK_N','3':'RAIL_RUN','4':'GND','5':'CONV_EN','6':'HARD_OK_N','7':'PACK_RUN','8':'V3V3'},'Package_SO:VSSOP-8_2.3x2mm_P0.5mm','SN74LVC2G08DCUR','supply_isolation','NORMAL',cost=.18,source=TI+'sn74lvc2g08.pdf',note='Direct comparator logic-low to defined NPN-base low; replaces diode clamps whose residual VBE was not guaranteed off at temperature.')
    dec('C310',pop='NORMAL')
    p('J302','Conn_01x03','Exclusive converter link',{'1':'VBOOST','2':'VREG_RAW','3':'VBUCK'},'Connector_PinHeader_2.54mm:PinHeader_1x03_P2.54mm_Vertical','OPEN keyed exclusive shunt','input','NORMAL',cost=.12,note='1-2 BOOST (2S); 2-3 BUCK (4S). Never bridge both; DNP other converter. Incoming pack window population must agree.')
    p('U301','TPS54302','TPS54302DDCR',{'1':'GND','2':'SW4S','3':'VIN_CONV','4':'FB4S','5':'CONV_EN','6':'BOOT4S'},'Package_TO_SOT_SMD:SOT-23-6_Handsoldering','TPS54302DDCR','converter','BUCK4S',cost=.55,source=TI+'tps54302.pdf')
    l('L301','10u','SW4S','VBUCK','converter','BUCK4S',True);c('C303','100n','BOOT4S','SW4S','converter','BUCK4S');c('C304','22u','VBUCK','GND','converter','BUCK4S',cost=.28);c('C305','22u','VBUCK','GND','converter','BUCK4S',cost=.28)
    r('R301','116k','VBUCK','FB4S','converter','BUCK4S');r('R302','10k','FB4S','GND','converter','BUCK4S') # 7.5096V reduced
    r('R303','27.8k','FB4S','FB4S_SWITCH','converter','BUCK4S');fet('Q301','PROFILE_Q','FB4S_SWITCH','GND','converter','BUCK4S') #9.9965V full
    r('R304','100k','CONV_EN','GND','converter','NORMAL')
    # Upstream overvoltage disconnect is independent of converter EN.
    fet('Q302','REG_GATE','VREG_SWITCH','VREG_RAW','supply_isolation','NORMAL',True)
    r('R305','4.7k','REG_GATE','VREG_RAW','supply_isolation','NORMAL');r('R306','1k','REG_GATE','REG_SINK','supply_isolation','NORMAL');bjt('Q303','MMBT3904','NORMAL_ENABLE_BASE','REG_SINK','GND','supply_isolation','NORMAL');r('R307','4.7k','RAIL_RUN','NORMAL_ENABLE_BASE','supply_isolation','NORMAL');r('R308','100k','NORMAL_ENABLE_BASE','GND','supply_isolation','NORMAL')
    # Hard fault pulls the switch's NPN base down (separate from converter control).
    p('D304','D_Zener','10V gate clamp',{'1':'VREG_RAW','2':'REG_GATE'},'Diode_SMD:D_SOD-123F','BZT52H-C10,115','supply_isolation','NORMAL',cost=.05)
    r('R309','0.1','VREG_SWITCH','VMOD','protection','NORMAL',cost=.20,fp='Resistor_SMD:R_2512_6332Metric',mpn='OPEN 0.1ohm 1% 1W Kelvin layout')
    c('C306','22u','VMOD','GND','power','NORMAL',cost=.28);c('C307','100n','VMOD','GND','power','NORMAL');tp('TP301','VIN_PROT');tp('TP302','VREG_RAW');tp('TP303','VMOD')

    section('04_boost_driver_supply','04 2S boost and regulated MMIC rail','BOOST or BUCK:10.0V full /7.5V reduced, captured profile. No universal buck-boost.\nTPS611781 reference-derived starting compensation: must qualify loop, ripple and peak current on dummy load before PA connection.')
    p('U302','TPS611781','TPS611781RNWR',{'1':'BOOST_FREQ','2':'GND','3':'BOOST_ILIM','4':'BOOST_COMP','5':'BOOST_FB','6':'GND','7':'BOOST_SW','8':'VBOOST','9':None,'10':'BOOST_VCC','11':'CONV_EN','12':'VIN_CONV','13':'BOOST_BST'},'','TPS611781RNWR','converter','BOOST2S',cost=2.25,source=TI+'tps61178.pdf',note='13-terminal RNW VQFN-HR; footprint OPEN, not a generic QFN. DISDRV unused: separate upstream-output disconnect implemented. 20V output-capable; not TPS61088.')
    l('L302','4.7u','VIN_CONV','BOOST_SW','converter','BOOST2S',True);c('C401','100n','BOOST_BST','BOOST_SW','converter','BOOST2S');c('C402','4.7u','BOOST_VCC','GND','converter','BOOST2S',cost=.08);c('C403','22u','VBOOST','GND','converter','BOOST2S',cost=.28);c('C404','22u','VBOOST','GND','converter','BOOST2S',cost=.28)
    r('R401','510k','VBOOST','BOOST_FB','converter','BOOST2S');r('R402','100k','BOOST_FB','GND','converter','BOOST2S',note='VREF1.229V ->7.4969V reduced; PROFILE_Q250k shunt gives10.004V full. Tolerance/calibration gate.')
    r('R414','250k','BOOST_FB','BOOST_FB_SWITCH','converter','BOOST2S');fet('Q307','PROFILE_Q','BOOST_FB_SWITCH','GND','converter','BOOST2S')
    r('R403','150k','BOOST_ILIM','GND','converter','BOOST2S',note='745/Rk ~4.97A nominal switch-current limit; duty/tolerance verification gate.')
    r('R404','340k','BOOST_FREQ','GND','converter','BOOST2S',note='342k corresponds typical500kHz;340k E96 starting value. Tolerance400-600kHz characterization; measure spread/noise.')
    r('R405','10k','BOOST_COMP','COMP_C','converter','BOOST2S');c('C405','4.7n','COMP_C','GND','converter','BOOST2S');c('C406','100p','BOOST_COMP','GND','converter','BOOST2S',note='Starting compensation, not validated for selected L/C/load.')
    r('R413','2.2','VMOD','VDRV_LDO_IN','driver_supply','NORMAL',cost=.08,fp='Resistor_SMD:R_1206_3216Metric',mpn='OPEN2.2ohm1%0.5W',note='Input damping before LDO. At180mA0.071W; fault-pulse rating and<=20us external disconnect qualification required.')
    c('C407','1u','VDRV_LDO_IN','GND','driver_supply','NORMAL',note='Effective>=1uF at10.5V input; choose25V X7R with DC-bias qualification.')
    p('U303','TLV761','TLV76150DCYR',{'1':'GND','2':'VDRV_FILTER','3':'VDRV_LDO_IN'},'Package_TO_SOT_SMD:SOT-223-3_TabPin2','TLV76150DCYR','driver_supply','NORMAL',price={'1':.47,'10':.334,'25':.2988},source=TI+'tlv761.pdf',evidence='OBSERVED_EUR_NET',supplier='DigiKey DE indexed EUR net',code='296-TLV76150DCYRCT-ND',stock='8483 indexed;CT MOQ1;EUR0.47/0.334 at1/10;2026-10-15 observation, no reservation',note='SBVS349D May2025 DCY1GND2OUT/tab3IN.18V recommended20V absolute. Fixed5V +/-1.75% full temperature. Require thermal path<=80C/W at180mA/10.5V upstream. Mating manufacturer landing dimensions OPEN before layout. Replaces second buck and magnetics.')
    c('C409','150u','VDRV_FILTER','GND','driver_supply','NORMAL',cost=.45,mpn='OPEN150uF25V ESR<=0.1ohm min120uF',fp='',note='Exact package/MPN OPEN. LDO recommended1-220uF capacitance and ESR2-500mohm: require120-180uF, ESR2-100mohm. Conditional LDO-short fault:initial5.0875V,step10.5V,Rmin2.178ohm,Cmin120uF,ESRmax0.1ohm,disconnect<=20us. Measure Vdriver<=5.9V; no simulated hardware guarantee.')
    p('D309','D','SS14 LDO reverse discharge',{'1':'VDRV_LDO_IN','2':'VDRV_FILTER'},'Diode_SMD:D_SMA','SS14-E3/61T','driver_supply','NORMAL',cost=.18,source='https://www.vishay.com/docs/88746/ss12.pdf',note='Cathode1 at IN, anode2 at OUT; external bypass per TLV761 section7.1.3. Exact suffix/package/surge confirmation OPEN. Limits reverse-current stress during reservoir discharge, not an OV clamp; measure reverse transient.')
    fet('Q304','DRV_GATE','VDRV_RF','VDRV_FILTER','driver_supply','NORMAL',True);r('R408','4.7k','DRV_GATE','VDRV_FILTER','driver_supply','NORMAL');r('R409','1k','DRV_GATE','DRV_SINK','driver_supply','NORMAL');bjt('Q308','MMBT3904','DRV_ENABLE_BASE','DRV_SINK','GND','driver_supply','NORMAL');r('R410','10k','NORMAL_PERMIT','DRV_ENABLE_BASE','driver_supply','NORMAL');r('R411','100k','DRV_ENABLE_BASE','GND','driver_supply','NORMAL');r('R412','1k','VDRV_RF','GND','driver_supply','NORMAL');tp('TP401','VDRV_RF')

    p('D308','D_Zener','10V driver-switch gate clamp',{'1':'VDRV_FILTER','2':'DRV_GATE'},'Diode_SMD:D_SOD-123F','BZT52H-C10,115','driver_supply','NORMAL',cost=.05)

    section('05_am','05 Sine reconstruction and series AM modulator','True AM: within SLOT the carrier is continuous; KEY selects filtered sine or carrier-only reference.\nThe controller supplies coherent LEVEL_PWM and AF_PWM (carrier offset plus sine), default800Hz. No ESP32-S3 internal DAC assumed.')
    p('U401','TLV9004_SO14','TLV9004IDR',{'1':'LEVEL_DC','2':'LEVEL_DC','3':'LEVEL_F2','4':'V3V3','5':'AF_F2','6':'AF_DC','7':'AF_DC','8':'MOD_DRIVE','9':'VPA_FB','10':'MOD_COMMAND','11':'GND','12':'TRAIN_COMMAND','13':'TRAIN_EMITTER_DC','14':'TRAIN_BASE_DRIVE'},FP_SO14,'TLV9004IDR','am',cost=.60,source=TI+'tlv9004.pdf',note='RRIO1MHz3.3V; quad SOIC. Exact IDR orderable suffix verify. Loop compensation/load stability OPEN.')
    for prefix,inp,out,base in [('LEVEL','LEVEL_PWM','LEVEL_DC',501),('AF','AF_PWM','AF_DC',503)]:
        r('R'+str(base),'10k',inp,prefix+'_F1','am');r('R'+str(base+1),'10k',prefix+'_F1',prefix+'_F2','am');c('C'+str(base),'4.7n',prefix+'_F1',out,'am');c('C'+str(base+1),'4.7n',prefix+'_F2','GND','am')
    p('U402','LVC3157','SN74LVC1G3157DBVR',{'1':'AF_DC','2':'GND','3':'LEVEL_DC','4':'AM_COMMAND','5':'V3V3','6':'KEY'},'Package_TO_SOT_SMD:SOT-23-6','SN74LVC1G3157DBVR','am',cost=.18,source=TI+'sn74lvc1g3157.pdf')
    r('R516','1k','AM_COMMAND','MOD_COMMAND','modulator','NORMAL');bjt('Q405','MMBT3904','MOD_OFF_BASE','MOD_COMMAND','GND','modulator','NORMAL')
    bjt('Q401','D45H11_ST','PASS_BASE','VPA','VMOD','modulator','NORMAL')
    r('R505','4.7k','PASS_BASE','VMOD','modulator','NORMAL');r('R506','10','PASS_BASE','MOD_SINK','modulator','NORMAL',cost=.10,fp='Resistor_SMD:R_2010_5025Metric',mpn='OPEN10ohm1W2010',note='At73mA helper limit:0.053W.1W pulse allowance retained;10ohm instead100ohm restores low-voltage pass headroom. Hot beta/SOA remain OPEN.')
    bjt('Q402','BD139_ST','MOD_BASE','MOD_SINK','MOD_E','modulator','NORMAL');r('R507','8.2','MOD_E','GND','modulator','NORMAL',cost=.035,fp='Resistor_SMD:R_0805_2012Metric');r('R508','1k','MOD_DRIVE','MOD_BASE','modulator','NORMAL');bjt('Q403','MMBT3904','MOD_E','MOD_BASE','GND','modulator','NORMAL');bjt('Q404','MMBT3904','MOD_OFF_BASE','MOD_BASE','GND','modulator','NORMAL');r('R509','10k','NORMAL_OFF','MOD_OFF_BASE','modulator','NORMAL');r('R510','100k','MOD_BASE','GND','modulator','NORMAL')
    r('R511','18k','VPA','VPA_FB','modulator','NORMAL');r('R512','10k','VPA_FB','GND','modulator','NORMAL');c('C505','4.7n','MOD_DRIVE','VPA_FB','modulator','NORMAL',note='Dominant compensation candidate; loop dynamics OPEN, test with bounded dummy current load.');c('C506','100n','VPA','GND','modulator','NORMAL');r('R513','1k','VPA','GND','modulator','NORMAL',cost=.035,fp='Resistor_SMD:R_1206_3216Metric',note='0.144W at12Vdc capability test; require>=0.25W.')
    r('R517','100k','VPA_FB','GND','am','TRAIN_ONLY');r('R518','100k','MOD_COMMAND','GND','am','TRAIN_ONLY')
    # Training uses the same reconstructed true sine, attenuated for a 5mA emitter-current servo.
    r('R514','27k','AM_COMMAND','TRAIN_COMMAND','training');r('R515','10k','TRAIN_COMMAND','GND','training');dec('C507');dec('C508');tp('TP501','AM_COMMAND');tp('TP502','VPA');tp('TP503','MOD_E')

    section('06_normal_rf','06 144MHz source, driver, final matching and output filter','50ohm fundamental filter -> pad -> PHA-1+ -> TUNE match -> PD54008L-E -> TUNE match -> LPF.\nMatching below is an explicit ASSUMED-IMPEDANCE test harness, NOT traced ST135-175MHz matching. ST drawing retrieval BLOCKED. No measured 144MHz gain or AM linearity exists.')
    # 7-pole Butterworth 180MHz 50ohm lowpass, shunt-first ladder: 7.87p/55.13n/31.87p/88.42n/31.87p/55.13n/7.87p.
    def filt(prefix,src,dst,pop='ALL',group='source_filter'):
        nodes=[src,prefix+'A',prefix+'B',dst]
        for i,(a,b,v)in enumerate(zip(nodes,nodes[1:],['56n','91n','56n']),1):l('L'+prefix+str(i),v,a,b,group,pop)
        for i,(node,v)in enumerate(zip(nodes,['8.2p','33p','33p','8.2p']),1):c('C'+prefix+str(i),v,node,'GND',group,pop,True,cost=.10)
    c('C601','100p','CLK_NORMAL','SRC_RF','source_filter','NORMAL',True)
    filt('61','SRC_RF','SRC_FILT','NORMAL')
    r('R602','17.8','SRC_FILT','DRIVER_PAD','source_filter','NORMAL',cost=.03,note='3dB pi-pad candidate17.6/292.4 theoretical, rounded17.8/287. First characterization uses external generator and/or12dB pad, then measured3-12dB calibration. Si5351 fundamental power and MMIC gain must meet drive budget; no guaranteed source power assumed. PHA-1+ input absolute24dBm is not operating target.');r('R603','287','SRC_FILT','GND','source_filter','NORMAL');r('R604','287','DRIVER_PAD','GND','source_filter','NORMAL')
    c('C615','1n','DRIVER_PAD','DRIVER_IN','driver','NORMAL',True,note='Immediate MMIC input DC block after shunt pi-pad; prevents pad from clamping internal input bias.')
    p('U501','PHA1','PHA-1+',{'1':'DRIVER_IN','2':'GND','3':'MMIC_RF_DC','4':'GND'},'','PHA-1+','driver','NORMAL',price={'1':2.82,'50':2.11},source='https://www.minicircuits.com/WebStore/dashboardPdf?model=PHA-1%2B',evidence='OBSERVED_EUR_PROVISIONAL_NET',supplier='Mouser EU observed EUR display; tax confirmation OPEN',code='139-PHA-1',stock='EUR2.82 at1;2.11 at50;cut-tape MOQ1;4662 indexed stock;2026-10-15 observation, no reservation',note='PHA-1+ DF782:1IN2GND3OUT/DC4paddleGND. Exact landing OPEN.5V146mA catalog. Selected economical EVALUATION driver;144MHz measured P1dB and final gain must close3dB backoff before acceptance. Not PHA-1H+ data.')
    l('L604','180n','VDRV_RF','MMIC_RF_DC','driver','NORMAL');c('C602','1n','MMIC_RF_DC','PA_IN50','driver','NORMAL',True);c('C603','100n','VDRV_RF','GND','driver','NORMAL');c('C604','1n','VDRV_RF','GND','driver','NORMAL',True)
    # ASSUMPTION only: Zin=5-j10ohm plus1ohm stopper; L=28.870nH,C=59.571pF. NOT manufacturer matching.
    c('C605','OPEN 59.6p TUNE','PA_IN50','GND','pa_match','NORMAL',True);l('L605','OPEN 28.9n TUNE','PA_IN50','GATE_AC','pa_match','NORMAL');c('C606','1n','GATE_AC','GATE_STOP','pa_match','NORMAL',True);r('R605','1','GATE_STOP','PA_GATE','pa_match','NORMAL',cost=.035,note='Stability stopper; exact loss included in measured gain qualification.')
    p('Q501','PD54008_Functional','PD54008L-E',{'G':'PA_GATE','D':'PA_DRAIN','S':'GND'},'','PD54008L-E','pa','NORMAL',price={'1':7.32,'10':5.677,'25':5.266},source='https://www.st.com/resource/en/datasheet/pd54008l-e.pdf',evidence='OBSERVED_EUR_NET',supplier='DigiKey IT EUR net display',code='497-6471-1-ND',stock='1988 indexed stock;CT MOQ1,multiple1;EUR7.32/5.677 at1/10;2026-10-15, not reserved',note='PD54008L-E PowerFLAT5x5. Functional G/D/S only until original package drawing can be visually inspected. Numeric pad map and source thermal landing OPEN; never use a generic powerMOSFET pad map. ST VHF reference fixed-supply5W is not AM qualification.')
    # Bias bounded by a6.2V shunt, manual current adjustment, default-grounded when inhibited.
    r('R606','1k','VMOD','BIAS_TOP','bias','NORMAL');p('RV501','R_Potentiometer','10k bias trim',{'1':'BIAS_TOP','2':'BIAS_WIPER','3':'GND'},'Potentiometer_THT:Potentiometer_Bourns_3296W_Vertical','3296W-1-103LF','bias','NORMAL',cost=.42,note='Pot represented by explicit end/wiper pins. Start wiper grounded. Start Idq50mA; investigate100-200mA only after drain rail qualification.')
    p('D501','D_Zener','6.2V bias ceiling',{'1':'BIAS_TOP','2':'GND'},'Diode_SMD:D_SOD-123F','BZT52H-C6V2,115','bias','NORMAL',cost=.05)
    l('L606','180n','BIAS_WIPER','PA_GATE','bias','NORMAL');c('C607','100n','BIAS_WIPER','GND','bias','NORMAL');fet('Q502','NORMAL_OFF','BIAS_WIPER','GND','bias','NORMAL')
    l('L607','180n','VPA','PA_DRAIN','pa_match','NORMAL');c('C608','1n','VPA','GND','pa_match','NORMAL',True)
    c('C609','1n','PA_DRAIN','OUT_MATCH','pa_match','NORMAL',True,mpn='C0805C102J1GACTU',fp='Capacitor_SMD:C_0805_2012Metric',note='100V C0G candidate inherited qualified family; exact stock OPEN.')
    # ASSUMPTION only: RF load3.5ohm with nominal60pF Coss; values calculated in analysis. NOT ST reference match.
    l('L608','OPEN output-L TUNE','OUT_MATCH','OUT50','pa_match','NORMAL');c('C610','OPEN output-C TUNE','OUT50','GND','pa_match','NORMAL',True,note='OPEN: actual ST output-match topology not retrieved. Empty tuning positions do not authorize PA energization. Assumed3.5ohm load/60pF Coss calculation is only a feasibility illustration; no144MHz large-signal evidence.')
    outnodes=['OUT50','OUT9A','OUT9B','OUT9C','NORMAL_RF']
    l('L621','47n','OUT50','OUT9A','output_filter','NORMAL')
    l('L622','82n','OUT9A','OUT9AB','output_filter','NORMAL');l('L625','11n','OUT9AB','OUT9B','output_filter','NORMAL')
    l('L623','82n','OUT9B','OUT9BC','output_filter','NORMAL');l('L626','11n','OUT9BC','OUT9C','output_filter','NORMAL')
    l('L624','47n','OUT9C','NORMAL_RF','output_filter','NORMAL')
    for i,(node,v) in enumerate(zip(outnodes,['6.8p','27p','33p','27p','6.8p']),1):c('C62'+str(i),v,node,'GND','output_filter','NORMAL',True,cost=.10)
    p('J501','Conn_Coaxial','NORMAL 50ohm SMA',{'1':'NORMAL_RF','2':'GND'},'Connector_Coaxial:SMA_Amphenol_132134_Vertical','132134','connector','NORMAL',cost=1.10,note='Exact vendor geometry/price OPEN; evaluate horizontal omnidirectional antenna separately.')
    tp('TP601','PA_GATE');tp('TP602','PA_DRAIN');tp('TP603','OUT50');tp('TP604','PA_IN50')

    section('07_training','07 Independent very-low-power sine-AM training path','Separate source CLK2, current-modulated small RF BJT, own filter/pad and incompatible MCX port.\nNo connection to watt PA drain/output. Target1uW carrier, optional1-10uW via calibrated fixed pad; actual calibration and isolation OPEN.')
    p('U701','LVC125','SN74LVC1G125DBVR',{'1':'TRAIN_OFF','2':'CLK_TRAIN','3':'GND','4':'TRAIN_CLOCK_BUF','5':'V3V3'},'Package_TO_SOT_SMD:SOT-23-5','SN74LVC1G125DBVR','training',cost=.12,source=TI+'sn74lvc1g125.pdf',note='OE_N high unless TRAIN_PERMIT; TTL input, partial-power-down/Ioff; measured144MHz edge/purity gate.')
    r('R714','100','TRAIN_CLOCK_BUF','TRAIN_CLOCK_LIMIT','training')
    c('C701','100p','TRAIN_CLOCK_LIMIT','TRAIN_SRC','training',rf=True)
    filt('71','TRAIN_SRC','TRAIN_FILT','ALL','training')
    # Fixed input attenuation limits RF voltage at RF transistor base.
    r('R715','51.1','TRAIN_FILT','GND','training');r('R702','680','TRAIN_FILT','TRAIN_BASE_RF','training');r('R703','10','TRAIN_BASE_RF','GND','training');c('C702','100p','TRAIN_BASE_RF','TRAIN_BASE','training',rf=True)
    d.lib.native('Transistor_BJT:MMBT3904','MMBTH10')
    p('Q701','MMBTH10','MMBTH10LT1G',{'1':'TRAIN_BASE','2':'TRAIN_EMITTER','3':'TRAIN_COLLECTOR'},'Package_TO_SOT_SMD:SOT-23','MMBTH10LT1G','training',cost=.16,source='https://www.onsemi.com/download/data-sheet/pdf/mmbth10lt1-d.pdf',note='1B2E3C verified onsemi CASE318 STYLE6 manufacturer PDF; exact suffix/temperature stock gate remains. fT>=650MHz published family; no measured144MHz performance.')
    r('R704','100','V3V3','TRAIN_COLLECTOR','training',cost=.035,fp='Resistor_SMD:R_1206_3216Metric',note='Collector-short dissipation up to0.121W at3.465V/99ohm; require>=0.25W.');r('R705','47','TRAIN_EMITTER','GND','training');c('C703','1n','TRAIN_EMITTER','GND','training',rf=True);r('R706','10k','TRAIN_BASE_DRIVE','TRAIN_BIAS','training');l('L704','180n','TRAIN_BIAS','TRAIN_BASE','training');c('C704','100p','TRAIN_BIAS','GND','training');r('R707','1k','TRAIN_EMITTER','TRAIN_EMITTER_DC','training');c('C705','1n','TRAIN_EMITTER_DC','GND','training')
    # Hardware inhibit clamps base. Slow base current servo cannot defeat collector/clock isolation.
    bjt('Q704','MMBT3904','TRAIN_OFF_BASE','TRAIN_COMMAND','GND','training')
    bjt('Q702','MMBT3904','TRAIN_OFF_BASE','TRAIN_BASE','GND','training');r('R708','10k','TRAIN_OFF','TRAIN_OFF_BASE','training')
    # Reuse spare OR as inverter would be wrong; explicit NPN inversion with default pull-up.
    r('R709','1k','TRAIN_OFF','V3V3','training');r('R710','4.7k','TRAIN_PERMIT','TRAIN_INVERT_BASE','training');bjt('Q703','MMBT3904','TRAIN_INVERT_BASE','TRAIN_OFF','GND','training')
    c('C706','1n','TRAIN_COLLECTOR','TRAIN_OUT_RAW','training',rf=True)
    filt('72','TRAIN_OUT_RAW','TRAIN_OUT_FILT','ALL','training')
    r('R711','154','TRAIN_OUT_FILT','TRAIN_RF','training',note='16dB pi-pad candidate:154/68.1 rounded. Calibrate nominal1uW carrier; optional1-10uW by fixed pad population, no1mW guarantee.')
    r('R712','68.1','TRAIN_OUT_FILT','GND','training');r('R713','68.1','TRAIN_RF','GND','training')
    p('J701','Conn_Coaxial','TRAIN MCX 50ohm',{'1':'TRAIN_RF','2':'GND'},'','OPEN MCX 50ohm PCB connector','connector',cost=.85,note='Physically incompatible with normal SMA. Exact manufacturer MPN/geometry OPEN. No RF switch bridges normal port.')
    tp('TP701','TRAIN_OUT_RAW');tp('TP702','TRAIN_RF')

    section('08_protection','08 Local voltage, current and thermal trip','Analog faults only affect normal PA population; training uses bounded3.3V and protected host pack.\nEight comparators, one current amplifier, one common reference: distinct voltage/current/sensor functions. No permanent RF detector or ADC.')
    p('U801','TL431DBZ','TL431BIDBZR',{'1':'VREF2V5','2':'VREF2V5','3':'GND'},'Package_TO_SOT_SMD:SOT-23','TL431BIDBZR','protection','NORMAL',cost=.18,source=TI+'tl431.pdf',note='TI DBZ1K2REF3A; manufacturer-specific mapping retained from E2.')
    r('R801','150','V3V3','VREF2V5','protection','NORMAL');r('R802','620','VREF2V5','VREF1V0','protection','NORMAL');r('R803','470','VREF1V0','GND','protection','NORMAL')
    p('U804','INA180A1','INA180A1IDBVR',{'1':'ISENSE','2':'GND','3':'VREG_SWITCH','4':'VMOD','5':'V3V3'},'Package_TO_SOT_SMD:SOT-23-5','INA180A1IDBVR','protection','NORMAL',cost=.39,source=TI+'ina180.pdf',note='A1gain20 x0.1ohm =>2V/A; ISENSE divider10k/4.02k against loaded~1.03V reference gives nominal1.80A trip, including driver current. 5us RC limits RF pickup; no Morse/AM crest averaging credit.')
    r('R804','10k','POWER_FAULT_N','V3V3','protection');r('R805','160k','VIN_PROT','VBAT_S','protection','NORMAL');r('R806','10k','VBAT_S','GND','protection','NORMAL')
    # Populated threshold top/bottom sets differ by battery/converter variant; explicit machine-readable alternates below.
    r('R807','58.3k','VREF2V5','UV_REF','protection','NORMAL',note='2S58.3k gives6.210V raw UV. BUCK4S24.9k gives12.15V for both profiles; no full-power voltage-window shunt, nominal tolerance guard required.')
    r('R808','10k','UV_REF','GND','protection','NORMAL');r('R809','39.2k','VREF2V5','OV_REF','protection','NORMAL',note='2S:8.621V raw trip. 4S:14.7k ->17.172V. Exact variant threshold stuffing mandatory.');r('R810','10k','OV_REF','GND','protection','NORMAL')
    r('R811','120k','VREG_RAW','VREG_S','protection','NORMAL');r('R812','10k','VREG_S','GND','protection','NORMAL');r('R813','20.9k','VREF2V5','REG_OV_REF','protection','NORMAL');r('R814','10k','REG_OV_REF','GND','protection','NORMAL')
    r('R815','80.6k','VDRV_FILTER','DRV_S','protection','NORMAL');r('R816','10k','DRV_S','GND','protection','NORMAL');r('R817','29.4k','VREF2V5','DRV_OV_REF','protection','NORMAL');r('R818','10k','DRV_OV_REF','GND','protection','NORMAL')
    r('R819','110k','VPA','VPA_S','protection','NORMAL');r('R820','10k','VPA_S','GND','protection','NORMAL');r('R821','26.5k','VREF2V5','VPA_OV_REF','protection','NORMAL',note='VPA overvoltage8.20V nominal: catches pass E-C short independently of commanded zero. Converter readiness is a controller ADC pre-SLOT function after captured profile settles.');r('R822','10k','VPA_OV_REF','GND','protection','NORMAL')
    r('R823','10k','VREF1V0','TEMP_S','protection','NORMAL');p('TH801','Thermistor_NTC','10k NTC B3950',{'1':'TEMP_S','2':'GND'},'Resistor_THT:R_Axial_DIN0207_L6.3mm_D2.5mm_P7.62mm_Horizontal','OPEN insulated contact NTC10k B3950','protection','NORMAL',cost=.18,note='Bond to PA/modulator thermal spreader; open and short detected by window. Geometry/adhesive/placement OPEN.')
    r('R824','49.9k','VREF1V0','TEMP_LOW','protection','NORMAL');r('R825','10k','TEMP_LOW','GND','protection','NORMAL');r('R826','1k','VREF1V0','TEMP_HIGH','protection','NORMAL');r('R827','10k','TEMP_HIGH','GND','protection','NORMAL')
    # Full4S now reaches10V upstream over the12V pack window; no profileUV shunt required.
    # Correct polarity: comparator output pulls low when plus < minus.
    comps=[('VBAT_S','UV_REF'),('OV_REF','VBAT_S'),('REG_OV_REF','VREG_S'),('DRV_OV_REF','DRV_S'),('VREF1V0','ISENSE_F'),('TEMP_S','TEMP_LOW'),('TEMP_HIGH','TEMP_S'),('VPA_OV_REF','VPA_S')]
    for k,(plus,minus)in enumerate(comps):
        ref='U802'if k<4 else'U803';u=k%4+1
        pp=[('5','4','2'),('7','6','1'),('11','10','13'),('9','8','14')][u-1]
        p(ref,'LM339','LM339BDR',dict(zip(pp,[plus,minus,'PACK_OK_N'if k<2 else'HARD_OK_N'])),FP_SO14,'LM339BDR','protection','NORMAL',cost=.18,source=TI+'lm339b.pdf',unit=u,note='3.3V; reference nodes below1.135V hot common-mode limit at3.135V supply; current reference~1.03V. One input must remain valid during positive overvoltage. Severe overvoltage beyond sense range must be bounded externally.')
    for n,ref in [('PACK_OK_N','R832'),('HARD_OK_N','R833')]:r(ref,'10k',n,'V3V3','protection','NORMAL')
    for n,ref in [('PACK_OK_N','D801'),('HARD_OK_N','D802')]:p(ref,'D','BAT54 fault AND',{'1':n,'2':'POWER_FAULT_N'},'Diode_SMD:D_SOD-323','BAT54WS-7-F','protection','NORMAL',cost=.05,note='Low-level max comparatorVOL+diodeVf must remain <0.3VDD; no converter-startup deadlock from rail undervoltage.')
    for ref in ['U802','U803']:p(ref,'LM339','LM339BDR',{'3':'V3V3','12':'GND'},FP_SO14,'LM339BDR','protection','NORMAL',cost=.18,source=TI+'lm339b.pdf',unit=5)
    for ref in ['C801','C802','C803']:dec(ref,pop='NORMAL')
    r('R828','10k','ISENSE','ISENSE_F','protection','NORMAL');r('R829','4.02k','ISENSE_F','GND','protection','NORMAL');c('C804','1n','ISENSE_F','GND','protection','NORMAL');tp('TP801','ISENSE');tp('TP802','POWER_FAULT_N')
    r('R117','1k','VREG_S','PA_RAIL_ADC','interface','NORMAL');c('C104','1n','PA_RAIL_ADC','GND','interface','NORMAL',note='Controller ADC acquisition/attenuation calibrated for ~10k source impedance. Read before ARM and SLOT; no I2C transaction needed.')
    r('R118','100k','PA_RAIL_ADC','GND','interface','TRAIN_ONLY')
    # Explicit voltage sources from protected controller/lab supplies for ERC.
    section('09_test_power','09 External supply declarations and measurement contract','No RF2M PCB exists in M5A-R1. All RF/thermal/safety tests NOT_RUN.\nPWR_FLAG declares a measured external source; it does not validate protection or a supply rating.\nRead OPEN items in docs/M5A_R1_SCHEMATIC_REVIEW.md before an evaluation PCB.')
    for i,n in enumerate(['GND','V3V3','BAT_RAW','VIN_PROT','VIN_CONV','VREG_RAW','VMOD','VBUCK','VBOOST','VDRV_LDO_IN','VDRV_RF'],901):p('#FLG'+str(i),'PWR_FLAG','PWR_FLAG',{'1':n},'','NOT_PURCHASED','declaration',cost=0,evidence='NON_PHYSICAL')
    for i,n in enumerate(['V3V3','GND','VPA','VDRV_LDO_IN','LEVEL_DC','AF_DC','VPA_FB','TRAIN_EMITTER'],901):tp('TP'+str(i),n)
    d.parts['U207']['population']='NORMAL'
    d.parts['C208']['population']='NORMAL'
    # In TRAIN_ONLY there is no analog PA power chain: its health input is a hard safe constant.
    r('R519','0','V3V3','RUN_HEALTH','interlock','TRAIN_ONLY',note='Fit only with U207 and every normal power-stage part omitted. Equivalent to POWER_FAULT_N=1; watchdog/mute/SCL/fresh ARM still active.')
    d.parts['R101']['variant_values']={'BUCK4S':'27.4k','TRAIN_ONLY':'47k'}
    d.parts['R807']['variant_values']={'BUCK4S':'24.9k'}
    d.parts['R809']['variant_values']={'BUCK4S':'14.7k'}
    # Converter-dependent value substitutions remain explicit candidate assembly data.
    from m5a_r1_readable import reflow
    reflow(d)
    d.save()
    return d

if __name__=='__main__':
    d=build();print('Generated RF2M electrical candidate',len(d.parts),'positions,',len(d.sheets),'sheets')
