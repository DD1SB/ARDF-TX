"""Executable M6-C1 hardware contract, not production competition firmware.

Time is monotonic integer microseconds. No sleeps, network, hardware activation,
or free-running application heartbeat. All radio methods are simulated fixtures.
"""
from dataclasses import dataclass,field
from enum import Enum
class Band(Enum): RF80='RF80'; RF2M='RF2M'
class State(Enum): SAFE='SAFE'; PREPARING='PREPARING'; CONFIGURED='CONFIGURED'; ARMED='ARMED'; TX='TX'; FAULT='FAULT'
@dataclass
class Context:
    band:Band; path:str; pack:str; volts:float; module:str; frequency:int
    time_valid:bool; present:bool=True; bus_ok:bool=True; full:bool=False
    allowed:tuple=(); event:bool=True; rf80_code:tuple=(0,0)
    lora_present:bool=False; calibrated:bool=False
    def validate(self):
        if self.pack not in ('2S','4S'):raise ValueError('unknown pack')
        if not ((6<=self.volts<=8.4) if self.pack=='2S' else (12<=self.volts<=16.8)):raise ValueError('pack voltage/identity mismatch')
        if not self.present:raise ValueError('missing module')
        if not self.time_valid:raise ValueError('invalid RTC')
        if not self.calibrated:raise ValueError('missing qualified power/modulation calibration')
        if not self.bus_ok:raise ValueError('stuck I2C')
        if not any(lo<=self.frequency<=hi for lo,hi in self.allowed):raise ValueError('no locally permitted frequency')
        if self.band is Band.RF80:
            if self.module not in ('RF80_FULL','RF80_FOX'):raise ValueError('wrong module family')
            if self.path not in ('PA','FOX'):raise ValueError('contradictory paths')
            if self.path=='PA' and (self.module!='RF80_FULL' or self.pack!='4S'):raise ValueError('PA requires full RF80/4S')
            if self.module=='RF80_FULL' and self.pack!='4S':raise ValueError('full RF80 assembly requires commissioned4S profile')
            if self.module=='RF80_FOX' and self.pack!='2S':raise ValueError('FOX_MIN qualified pack profile is 2S')
            if self.rf80_code not in ((0,0),(1,0),(0,1)):raise ValueError('invalid PWR0/PWR1')
            if not 3500000<=self.frequency<=3800000:raise ValueError('unsupported RF80 frequency')
            if self.event and not 3510000<=self.frequency<=3600000:raise ValueError('championship RF80 range')
        else:
            if self.module not in ('BOOST2S','BUCK4S','TRAIN_ONLY'):raise ValueError('unknown RF2M population')
            if self.path not in ('NORMAL','TRAIN'):raise ValueError('invalid path')
            if self.path=='TRAIN' and self.full:raise ValueError('training/full contradiction')
            if self.path=='NORMAL':
                if self.module=='TRAIN_ONLY':raise ValueError('normal PA absent')
                if (self.module=='BOOST2S')!=(self.pack=='2S'):raise ValueError('wrong converter/pack')
            if not 144000000<=self.frequency<=148000000:raise ValueError('outside modeled synthesizer training range')
            if self.event and not 144500000<=self.frequency<=144900000:raise ValueError('championship VHF range')
@dataclass
class Controller:
    state:State=State.SAFE; now:int=0; context:Context|None=None
    arm_at:int=0; last_progress:int=0; progress_level:int=0; latched:bool=False
    configured_at:int=0; progress_edges:int=0
    signals:dict=field(default_factory=dict); events:list=field(default_factory=list)
    def __post_init__(self):self.safe()
    def safe(self):
        self.progress_level=0
        self.signals={n:0 for n in ('INIT_OK','ARM','MUTE_RELEASE','KEY','SLOT','PROGRESS','PREPARE','PA_PREPARE','PA_REQ','FOX_REQ','PACK4_SOFT','BUS80','BUS2M','POWER80','POWER2M','AF_PWM','LEVEL_PWM','PWR0','PWR1','PATH_TRAIN','PROFILE_FULL','BAND2')}
        self.state=State.SAFE if not self.latched else State.FAULT
    def reset(self):
        self.latched=False;self.context=None;self.safe();self.events.append('RESET: no auto rearm')
    def stop(self,reason):
        self.latched=True;self.safe();self.events.append('FAULT:'+reason)
    def recover(self):
        # Deliberate operator action only; no automatic heartbeat/LoRa recovery.
        self.latched=False;self.safe();self.context=None;self.now+=50000
    def configure(self,c):
        if self.latched or self.signals['ARM']:raise ValueError('explicit disarm/recovery required')
        c.validate();self.safe();self.context=c
        self.signals['INIT_OK']=1;self.signals['POWER80' if c.band is Band.RF80 else 'POWER2M']=1
        self.signals['BAND2']=int(c.band is Band.RF2M)
        self.signals['PWR0'],self.signals['PWR1']=c.rf80_code
        self.signals['PATH_TRAIN']=int(c.band is Band.RF2M and c.path=='TRAIN')
        self.signals['PROFILE_FULL']=int(c.band is Band.RF2M and c.full)
        self.state=State.PREPARING
        self.step(250000) # local watchdog/reset startup, progress remains application-owned
        self.signals['BUS80' if c.band is Band.RF80 else 'BUS2M']=1
        if c.band is Band.RF2M:
            # Native SRC_ON = PREPARE & SAFE_N & MUTE_N. ARM/SLOT remain low.
            self.signals['MUTE_RELEASE']=1;self.signals['PREPARE']=1;self.signals['PA_PREPARE']=int(c.path=='NORMAL')
        self.events.append('configure isolated Si5351; output disabled; readback')
        self.now+=20000;self.signals['BUS80']=self.signals['BUS2M']=0
        self.configured_at=self.now;self.last_progress=self.now;self.progress_edges=0
        if c.band is Band.RF80:
            self.signals['PA_REQ']=int(c.path=='PA');self.signals['FOX_REQ']=int(c.path=='FOX');self.signals['PACK4_SOFT']=int(c.pack=='4S')
        self.state=State.CONFIGURED
    def progress(self):
        if self.state in (State.PREPARING,State.CONFIGURED,State.ARMED,State.TX):
            try:self.context.validate()
            except ValueError as exc:self.stop(str(exc));return
            self.progress_level^=1;self.signals['PROGRESS']=self.progress_level;self.last_progress=self.now;self.progress_edges+=1
    def arm(self,accepted_before=False,accepted_after=True):
        if self.state is not State.CONFIGURED:raise ValueError('not configured')
        if accepted_before:self.stop('unexpected status high before arm');return
        if self.now-self.configured_at<100000 or self.progress_edges<4:raise ValueError('establish genuine progress before ARM')
        self.context.validate();self.progress();self.signals['MUTE_RELEASE']=1;self.now+=10000;self.signals['ARM']=1;self.arm_at=self.now
        # Model acceptance observation only. Real input must be sampled and stable.
        if not accepted_after:self.stop('arm not accepted');return
        self.state=State.ARMED
    def start_slot(self,pa_rail_valid=False):
        if self.state is not State.ARMED:raise ValueError('not armed')
        delay=250000 if self.context.band is Band.RF80 else 50000
        if self.now-self.arm_at<delay:raise ValueError('stabilization interval')
        if self.context.band is Band.RF2M and self.context.path=='NORMAL' and not pa_rail_valid:
            self.stop('PA rail absent/outside commissioned range');return
        self.signals['SLOT']=int(self.context.band is Band.RF2M);self.state=State.TX
    def key(self,value):
        if self.state is not State.TX:raise ValueError('no slot')
        self.signals['KEY']=int(bool(value))
    def step(self,us,application_healthy=True):
        end=self.now+us
        while self.now<end:
            self.now=min(end,self.now+25000)
            if application_healthy and self.now-self.last_progress>=25000:self.progress()
            if self.signals['ARM'] and self.now-self.last_progress>(250000 if self.context.band is Band.RF80 else 230000):self.stop('local module watchdog expires')
    def status(self,high):
        if self.signals['ARM'] and not high:self.stop('lost local arm acceptance')
    def pa_rail_sample(self,valid):
        if self.context and self.context.band is Band.RF2M and self.context.path=='NORMAL' and self.state in (State.ARMED,State.TX) and not valid:self.stop('lost qualified PA rail')
    def communication_loss(self,kind):
        # Optional LoRa loss alone must not disable a valid autonomous RTC event.
        self.events.append(kind+' absent/lost; autonomous schedule continues')
    def usb(self,present):self.events.append('USB '+str(present)+'; no auto arm')
    def physical_bus_enabled(self,band):return bool(self.signals['BUS80' if band is Band.RF80 else 'BUS2M'] and not self.signals['ARM'])

def morse_edges(text,wpm=12):
    """Minimal deterministic SOS timer fixture; 1MHz timer integer timestamps."""
    if not 8<=wpm<=15:raise ValueError('unsupported key speed')
    unit=round(1200000/wpm);codes={'S':'...','O':'---'};t=0;edges=[]
    for c in text:
        for symbol in codes[c]:edges.extend([(t,1),(t+unit*(3 if symbol=='-' else 1),0)]);t=edges[-1][0]+unit
        t+=2*unit
    return edges

def identify_rf2m(v,rail=3.3):
    if not 0<v<rail*.97:return None
    r=33000*v/(rail-v)
    return next((name for name,target in [('BOOST2S',18200),('BUCK4S',39200),('TRAIN_ONLY',82000)] if abs(r/target-1)<.14),None)


def rtc_fields_valid(year,month,day,hour,minute,second,por=False,voltage_low=False):
    """Decoded register validity fixture; real I2C/BCD decoding stays target work."""
    import datetime
    if por or voltage_low:return False
    try:datetime.datetime(year,month,day,hour,minute,second)
    except (ValueError,TypeError):return False
    return 2026<=year<=2099

def detect_lora(status,busy_stuck=False):
    """SX1262 GetStatus response fixture. Follow with identity/config readback."""
    return not busy_stuck and status not in (None,0,255) and ((status>>4)&7) in (2,3,4,5,6)

def identify_pack(v_id,protected_sense,rail=3.3):
    """Calibrated ADC fixture; measured sense is after reverse diode."""
    if not 0<v_id<rail*.97:return None
    resistance=10000*v_id/(rail-v_id)
    name=next((n for n,r in [('2S',10000),('4S',22000)] if abs(resistance/r-1)<.1),None)
    # Refuse contradictory bands. Actual raw voltage is interval sense+diode drop.
    if name=='2S' and 5.21<=protected_sense<=8.3:return name
    if name=='4S' and 11.21<=protected_sense<=16.7:return name
    return None
