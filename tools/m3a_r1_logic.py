#!/usr/bin/env python3
"""RF80 functional checks from physical KiCad net pins, including timer/FF state.

Ideal digital transitions plus RC/Schmitt engineering models, NOT transistor,
metastability, RF, thermal or measured safety validation. No firmware/PCB output.
"""
import argparse, copy, itertools, json, math, os
from pathlib import Path
import xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
HW=ROOT/'hardware/80m'
# Manufacturer physical pins, intentionally independent of CAD/generator.
GATES={
 '74HC00':('NAND',[(('1','2'),'3'),(('4','5'),'6'),(('9','10'),'8'),(('12','13'),'11')]),
 '74HC08':('AND',[(('1','2'),'3'),(('4','5'),'6'),(('9','10'),'8'),(('12','13'),'11')]),
 '74HC11':('AND',[(('1','2','13'),'12'),(('3','4','5'),'6'),(('9','10','11'),'8')]),
 '74HC21':('AND',[(('1','2','4','5'),'6'),(('9','10','12','13'),'8')]),
 '74HC32':('OR',[(('1','2'),'3'),(('4','5'),'6'),(('9','10'),'8'),(('12','13'),'11')]),
 '74HC14':('NOT',[(('1',),'2'),(('3',),'4'),(('5',),'6'),(('9',),'8'),(('11',),'10'),(('13',),'12')])}
FF74=[('1','2','3','4','5','6'),('13','12','11','10','9','8')]
FF174=[('3','2'),('4','5'),('6','7'),('11','10'),('13','12'),('14','15')]
MONOS=[('1','2','3','13','4','15'),('9','10','11','5','12','7')]

def number(s):
    s=s.split()[0].strip();suffix={'p':1e-12,'n':1e-9,'u':1e-6,'k':1e3,'M':1e6}
    return float(s[:-1])*suffix[s[-1]]if s[-1]in suffix else float(s)

class Circuit:
    def __init__(self,xml=None,mutation=None):
        tree=ET.parse(xml or os.environ.get('RF80_NETLIST') or HW/'review/RF80.xml');self.p={}
        for comp in tree.findall('./components/comp'):
            src=comp.find('libsource');self.p[comp.attrib['ref']]={'type':src.attrib['part'],'pins':{}}
        for n in tree.findall('./nets/net'):
            for nd in n.findall('node'):
                if n.attrib['name'].startswith('unconnected-'):continue
                self.p[nd.attrib['ref']]['pins'][nd.attrib['pin']]=n.attrib['name'].removeprefix('/')
        self.parts={p['ref']:p for p in json.loads((HW/'RF80.electrical.json').read_text())['parts']}
        if mutation:
            pp=self.p['U202']['pins'];a,b=mutation
            na,nb=pp.get(a),pp.get(b);pp.pop(a,None);pp.pop(b,None)
            if nb is not None:pp[a]=nb
            if na is not None:pp[b]=na
        self.gates=[]
        for ref,p in self.p.items():
            if p['type']in GATES:
                typ,layout=GATES[p['type']]
                for ins,out in layout:
                    if out in p['pins']:self.gates.append((typ,[p['pins'][i]for i in ins],p['pins'][out]))
        self.fets=[p['pins']for p in self.p.values()if p['type']=='2N7002']
    def net(self,ref,pin):return self.p[ref]['pins'].get(pin)
    def publish(self,v,ref,pin,value):
        n=self.net(ref,pin)
        if n is not None:v[n]=bool(value)
    def oc(self,v,ref,pin,healthy):
        n=self.net(ref,pin)
        if n is not None:v[n]=v.get(n,True)and bool(healthy)
    def combinational(self,x,ff=None,timers=None,arm_rc=False,key_c=False,fox=False):
        v={'V3V3':True,'GND':False,**x,'ARM_RC':arm_rc,'KEY_TAIL_C':key_c}
        ff=ff or [False,False];timers=timers or [False,False]
        for i,(_,_,_,_,q,qb) in enumerate(FF74):
            self.publish(v,'U223',q,ff[i]);self.publish(v,'U223',qb,not ff[i])
        for i,(_,_,_,q,qb,_)in enumerate(MONOS):
            self.publish(v,'U202',q,timers[i]);self.publish(v,'U202',qb,not timers[i])
        # Actual open-collector pin groups, avoiding assumed post-comparator inputs.
        v.update(HEALTH_N=True,UV_POR_N=True,PA_GUARD_RAW=True,PA_CONDITION_OK=False)
        self.oc(v,'U314','1',x.get('uv',True))
        if fox:v['PA_GUARD_RAW']=False # physically fitted R228, watt monitors DNP
        else:
            for pin,health in [('2','hot'),('1','local4'),('13','ov'),('14','oc')]:self.oc(v,'U312',pin,x.get(health,True))
            self.oc(v,'U314','7',x.get('sensor',True))
        for _ in range(25):
            old=v.copy()
            for typ,ins,out in self.gates:
                if all(n in v for n in ins):
                    vv=[v[n]for n in ins]
                    v[out]=not vv[0]if typ=='NOT'else any(vv)if typ=='OR'else not all(vv)if typ=='NAND'else all(vv)
            # Diode AND/OR direction follows actual physical K/A pins.
            def diode_and(ref):
                pp=self.p[ref]['pins'];v[pp['2']]=v.get(pp['2'],True)and v.get(pp['1'],False)
            diode_and('D219')
            if not fox:diode_and('D221');diode_and('D222')
            vv=[]
            for r in ('D223','D224'):
                pp=self.p[r]['pins'];vv.append(v.get(pp['2'],False))
            v[self.net('D223','1')]=any(vv)
            pp=self.p['D220']['pins'];v[pp['2']]=v.get(pp['1'],False)
            ground={'GND'}
            for _ in range(8):
                for p in self.fets:
                    if v.get(p['1'],False)and p['2']in ground:ground.add(p['3'])
            if 'HEALTH_N'in ground:v['HEALTH_N']=False
            v['PA_INB']='PA_INB'not in ground # own driver rail pull-up, rail retained in fault test
            if old==v:break
        else:raise AssertionError('Combinational network did not settle')
        v['NORMAL_CLOCK_ALLOWED']=not v['PA_INB']
        # Actual Fox mute NPN pulls NAND second inputs low. With low enable,
        # NAND outputs are constant, regardless of free-running Si5351.
        v['FOX_CLOCK_ALLOWED']=not v['FOX_MUTE']
        assert not(v['NORMAL_CLOCK_ALLOWED']and v['FOX_CLOCK_ALLOWED'])
        return v

class Model:
    def __init__(self,circuit=None,k=.50,rc_scale=1,vtp=.65,vtm=.30,fox=False):
        self.c=circuit or Circuit();self.k=k;self.scale=rc_scale;self.vtp=vtp;self.vtm=vtm;self.fox=fox
        self.t=0.;self.ff=[False,False];self.cfg=[False]*6;self.timer=[False,False];self.expiry=[0.,0.]
        self.arm_v=0.;self.key_v=0.;self.arm_bit=False;self.key_bit=False
        self.old={};self.v={};self.x=dict(POR_N=False,ARM=False,CW_KEY=False,PA_REQ=False,FOX_REQ=False,PWR0=False,PWR1=False,MUTE_N=False,PACK4_OK=False,FOX_ID=True,SCL=True,SDA=True,LEASE=False,uv=True,local4=True,ov=True,oc=True,hot=True,sensor=True)
        self.resolve()
    def cfg_publish(self,x):
        for i,(_,q)in enumerate(FF174):
            self.c.publish(x,'U224',q,self.cfg[i])
    def resolve(self):
        for _ in range(20):
            x=self.x.copy();self.cfg_publish(x)
            v=self.c.combinational(x,self.ff,self.timer,self.arm_bit,self.key_bit,self.fox)
            changed=False
            # Asynchronous controls dominate; positive clocks are tracked from
            # actual CP nets. Configuration captures RAW ARM before delayed arm.
            for i,(clr,d,cp,pre,_,_)in enumerate(FF74):
                rn=self.c.net('U223',clr);cn=self.c.net('U223',cp)
                val=self.ff[i]
                if not v[rn]:val=False
                elif not v[self.c.net('U223',pre)]:val=True
                elif v[cn]and not self.old.get(('ff',i),False):val=v[self.c.net('U223',d)]
                self.old[('ff',i)]=v[cn]
                if val!=self.ff[i]:self.ff[i]=val;changed=True
            cp=self.c.net('U224','9')
            if not v[self.c.net('U224','1')]:new=[False]*6
            elif v[cp]and not self.old.get('cfg',False):new=[v[self.c.net('U224',d)]for d,_ in FF174]
            else:new=self.cfg
            self.old['cfg']=v[cp]
            if new!=self.cfg:self.cfg=new;changed=True
            for i,(a,b,rd,_,_,_)in enumerate(MONOS):
                aa,bb,rr=[v[self.c.net('U202',p)]for p in(a,b,rd)]
                pa,pb,pr=self.old.get(('mono',i),(aa,bb,False))
                trigger=rr and ((pa and not aa and bb)or(not pb and bb and not aa)or(not pr and not aa and bb))
                oldq=self.timer[i]
                if not rr:self.timer[i]=False
                elif trigger:
                    r=number(self.c.parts['R201'if i==0 else'R202']['value']);cap=number(self.c.parts['C201'if i==0 else'C202']['value'])
                    self.expiry[i]=self.t+self.k*r*cap*self.scale*1000;self.timer[i]=True
                elif self.t>=self.expiry[i]:self.timer[i]=False
                self.old[('mono',i)]=(aa,bb,rr)
                if oldq!=self.timer[i]:changed=True
            self.v=v
            if not changed:return
        raise AssertionError('Sequential network did not settle')
    def set(self,**kw):self.x.update(kw);self.resolve();return self.v
    def advance(self,ms,hb=True,dt=.1):
        end=self.t+ms
        while self.t<end-1e-9:
            step=min(dt,end-self.t);self.t+=step
            if hb:self.x['LEASE']=((self.t-10)%50)<25 and self.t>=10
            ar=float(self.x['ARM']);tau=number(self.c.parts['R203']['value'])*number(self.c.parts['C203']['value'])*1000*self.scale
            self.arm_v=ar+(self.arm_v-ar)*math.exp(-step/tau)
            if self.arm_v>=self.vtp:self.arm_bit=True
            if self.arm_v<=self.vtm:self.arm_bit=False
            # Linear RC/key diode model. Drop=.25V at3.3V; no RF envelope model.
            rp=number(self.c.parts['R451']['value']);rb=number(self.c.parts['R452']['value'])
            cap=number(self.c.parts['C451']['value'])*self.scale
            gp=1/rp if self.x['CW_KEY']else 0
            gr=1/number(self.c.parts['R453']['value'])if not self.ff[0]else 0
            conductance=gp+1/rb+gr;target=(gp*(1-.25/3.3))/conductance
            self.key_v=target+(self.key_v-target)*math.exp(-step/(cap/conductance*1000))
            # tau=C/G for the summed resistor conductances.
            if self.key_v>=self.vtp:self.key_bit=True
            if self.key_v<=self.vtm:self.key_bit=False
            self.resolve()
        return self.v

def prepared(path='PA',**params):
    m=Model(**params);m.set(POR_N=True,MUTE_N=True,PACK4_OK=path=='PA',PA_REQ=path=='PA',FOX_REQ=path=='FOX',PWR1=path=='PA')
    m.advance(100);assert m.v['LEASE_OK']and m.v['BUS_QUIET']
    m.set(ARM=True);m.advance(250);assert m.ff[0]
    return m

def verify():
    c=Circuit();p=c.p
    assert c.net('U202','13')=='LEASE_OK' and c.net('U202','4')is None
    assert c.net('U202','12')=='BUS_HOLDOFF_N' and c.net('U202','5')is None
    assert c.net('U202','1')=='LEASE_SEEN_N' and c.net('U202','2')=='LEASE'
    assert c.net('U202','9')=='GND' and c.net('U202','10')=='SCL'
    assert c.net('U223','12')=='V3V3' and c.net('U223','11')=='LEASE' and c.net('U223','8')=='LEASE_SEEN_N'
    assert c.net('U224','9')=='ARM' and c.net('U224','1')=='HEALTH_N'
    assert c.net('U223','3')=='ARM_CLK' and c.net('U223','1')=='RESET_N' and c.net('U223','2')=='ARM_ACCEPT'
    # Truth tables include real timers' Q/Qbar pins and source FF, not assumed LEASE_OK.
    count=0
    for arm,pa,fox,mode0,mode1,guard,key,tail in itertools.product((False,True),repeat=8):
        x=dict(POR_N=True,ARM=arm,CW_KEY=key,PA_REQ=pa,FOX_REQ=fox,PWR0=mode0,PWR1=mode1,MUTE_N=True,PACK4_OK=guard,FOX_ID=True,SCL=True,SDA=True,uv=True,local4=guard,ov=True,oc=True,hot=True,sensor=True)
        x.update(PATH_PA=pa and not fox,PATH_FOX=fox and not pa,ARM_ACCEPT=arm)
        v=c.combinational(x,[arm,True],[True,False],True,tail)
        safe=not(pa and fox)and not(mode0 and mode1)and(not pa or guard)
        assert v['SAFE_RAW']==safe
        if not safe or not arm: # actual FF clear response
            v=c.combinational(x,[False,True],[True,False],True,tail)
            assert not(v['NORMAL_CLOCK_ALLOWED']or v['FOX_CLOCK_ALLOWED'])
        count+=1
    results=[]
    def record(name,fn):fn();results.append(name)
    def startup():
        for lease in (False,True):
            m=Model();m.set(ARM=True,CW_KEY=True,PA_REQ=True,PACK4_OK=True,MUTE_N=True,LEASE=lease)
            m.advance(10,hb=False);m.set(POR_N=True);m.advance(500,hb=False)
            assert not m.v['LEASE_OK'] and not m.ff[0]
    record('startup and stuck heartbeat, no fabricated reset-release progress',startup)
    for path in ('PA','FOX'):
        def tx(path=path):
            m=prepared(path,fox=path=='FOX');m.set(CW_KEY=True);m.advance(3)
            assert m.v['NORMAL_CLOCK_ALLOWED'if path=='PA'else'FOX_CLOCK_ALLOWED']
            m.set(CW_KEY=False);m.advance(8);assert m.v['KEY_TAIL']
            m.advance(80);assert not m.v['KEY_TAIL']
        record(path+' CW rise, pause and retained fall tail',tx)
        for fault,value in [('POR_N',False),('uv',False),('MUTE_N',False),('SCL',False),('SDA',False)]:
            def f(path=path,fault=fault,value=value):
                m=prepared(path,fox=path=='FOX');m.set(CW_KEY=True);m.advance(2);m.set(**{fault:value})
                assert not m.ff[0]and not(m.v['NORMAL_CLOCK_ALLOWED']or m.v['FOX_CLOCK_ALLOWED'])
                m.set(**{fault:True},CW_KEY=False);m.advance(300);assert not m.ff[0]
                m.set(ARM=False);m.advance(20);m.set(ARM=True);m.advance(250);assert m.ff[0]
            record(path+' fault '+fault+' and deliberate rearm',f)
        def timeout(path=path):
            m=prepared(path,fox=path=='FOX');m.set(CW_KEY=True);m.advance(2)
            start=m.t;m.advance(251,hb=False);assert not m.ff[0]
            m.advance(100);assert not m.ff[0] # restored progress alone cannot clock ARM
        record(path+' watchdog timeout, progress restoration does not rearm',timeout)
        def retune(path=path):
            m=prepared(path,fox=path=='FOX');m.set(SCL=False);m.advance(1);m.set(SCL=True);m.advance(.5)
            assert not m.v['BUS_QUIET'];m.advance(5);assert m.v['BUS_QUIET']and not m.ff[0]
        record(path+' I2C activity and quiet interval',retune)
        def switch(path=path):
            m=prepared(path,fox=path=='FOX');m.set(CW_KEY=True);m.advance(2)
            m.set(PA_REQ=False,FOX_REQ=False);assert not m.ff[0]
            m.set(PA_REQ=path=='FOX',FOX_REQ=path=='PA',PACK4_OK=True,CW_KEY=False)
            m.advance(100);assert not m.ff[0]
            m.set(ARM=False);m.advance(20);m.set(ARM=True);m.advance(250)
            # Fox-only cannot arm a watt request: its physical R228 guard is low.
            assert m.ff[0] == (not m.fox)
        record(path+' captured path, withdrawal fault, opposite path requires rearm',switch)
    for fault in ('local4','ov','oc','hot','sensor','PACK4_OK','FOX_ID'):
        def f(fault=fault):
            m=prepared();m.set(CW_KEY=True);m.advance(2);m.set(**{fault:False});assert not m.ff[0]
            m.set(**{fault:True},CW_KEY=False);m.advance(100);assert not m.ff[0]
        record('PA local trip '+fault,f)
    def invalid():
        for pa,fox,m0,m1 in [(True,True,False,False),(True,False,True,True)]:
            m=Model();m.set(POR_N=True,MUTE_N=True,PACK4_OK=True,PA_REQ=pa,FOX_REQ=fox,PWR0=m0,PWR1=m1);m.advance(100);m.set(ARM=True);m.advance(300);assert not m.ff[0]
        m=prepared();m.set(CW_KEY=True);m.advance(2);m.set(PWR0=True);assert not m.ff[0]
        m.set(PWR0=False,CW_KEY=False);m.advance(100);assert not m.ff[0]
    record('conflicting paths and invalid power code cannot arm or recover automatically',invalid)
    def mode():
        m=prepared();old=m.cfg[:];m.set(PWR0=False,PWR1=False);m.advance(100);assert m.cfg==old
        m.set(ARM=False);m.advance(20);m.set(ARM=True);m.advance(250);assert m.cfg[:2]==[False,False]
    record('profile held during ARM, deliberate cycle captures new profile',mode)
    def highkey():
        m=prepared();m.set(ARM=False,CW_KEY=True);m.advance(20);m.set(ARM=True);m.advance(300);assert not m.ff[0]
    record('KEY held high cannot arm',highkey)
    def pending():
        for late in (False,True):
            m=Model();m.set(POR_N=True,MUTE_N=True,PACK4_OK=True,PA_REQ=True);m.advance(100)
            if not late:m.set(MUTE_N=False)
            m.set(ARM=True)
            if late:m.advance(.2);m.set(MUTE_N=False)
            m.advance(.2);m.set(MUTE_N=True);m.advance(100)
            assert not m.ff[0] and not m.cfg[4], 'fault returned during pending ARM clock auto-armed'
    record('fault before or during delayed ARM is not recovered by a pending clock',pending)
    def no_progress():
        m=Model();m.set(POR_N=True,MUTE_N=True,PACK4_OK=True,PA_REQ=True);m.advance(300,hb=False)
        m.set(ARM=True);m.advance(250,hb=False);assert not m.ff[0]
    record('healthy idle bus plus fresh ARM still cannot arm without progress',no_progress)
    # Reproduce the critical consequence with the actual pin swap: inverted
    # watchdog output permits an idle controller with no progress after startup.
    bad=Model(circuit=Circuit(mutation=('13','4')))
    bad.set(POR_N=True,MUTE_N=True,PACK4_OK=True,PA_REQ=True);bad.advance(300,hb=False)
    bad.set(ARM=True);bad.advance(250,hb=False);bad.set(CW_KEY=True);bad.advance(3,hb=False)
    assert bad.v['NORMAL_CLOCK_ALLOWED'], 'regression stimulus did not reproduce unsafe inverted-watchdog permission'
    # Polarity mutations must fail, demonstrating the test is not blind to U202.
    mutations=[]
    for swap in [('13','4'),('12','5')]:
        failed=False
        try:prepared(circuit=Circuit(mutation=swap))
        except (AssertionError,KeyError):failed=True
        assert failed,('polarity mutation escaped',swap)
        mutations.append(list(swap))
    corners=[]
    for k,scale,vp,vm in itertools.product((.45,.60),(.9*.99,1.1*1.01),(.55,.75),(.25,.40)):
        m=prepared(k=k,rc_scale=scale,vtp=vp,vtm=vm);m.set(CW_KEY=True);m.advance(3)
        assert m.v['KEY_TAIL'];m.set(CW_KEY=False);m.advance(80);assert not m.v['KEY_TAIL']
        m.set(CW_KEY=True);m.advance(3);m.advance(251,hb=False);assert not m.ff[0]
        corners.append(dict(K_assumed=k,RC_multiplier=scale,VTplus_ratio_assumed=vp,VTminus_ratio_assumed=vm))
    return dict(date='2026-10-14',revision='M3A-R1',classification='PIN-DERIVED STATIC LOGIC AND IDEAL EVENT/RC SIMULATION; NO HARDWARE VALIDATION',truth_cases=count,state_scenarios=results,timing_corners=corners,polarity_mutations_rejected=mutations,inverted_watchdog_no_progress_unsafe_permission_reproduced=True,watchdog_ms_design_range=[.45*330000*.99*1e-6*.9*1000,.60*330000*1.01*1e-6*1.1*1000],quiet_ms_design_range=[.45*47000*.99*100e-9*.9*1000,.60*47000*1.01*100e-9*1.1*1000],not_proved=['K range is a design sensitivity envelope, not manufacturer guaranteed bounds','Propagation delays, races, asynchronous reset recovery and metastability','RC bias/leakage/Schmitt temperature corners and fast supply collapse','Driver OV interruption timing, shaper SOA, RF leakage/emissions/power/field/thermal/endurance'])

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--write',action='store_true');args=ap.parse_args()
    r=verify();out=ROOT/'docs/M3A_R1_LOGIC_RESULTS.json';s=json.dumps(r,indent=2)+'\n'
    if args.write:out.write_text(s)
    else:assert out.read_text()==s,'Stale R1 functional report'
    print('PASS:',r['truth_cases'],'physical-pin truth cases;',len(r['state_scenarios']),'state scenarios;',len(r['timing_corners']),'RC corners; U202 polarity mutations rejected')
