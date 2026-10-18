"""Optional-radio configuration contract, host only; never transmits/probes RF."""
from dataclasses import dataclass
from enum import Enum
import math
class LoRaPopulation(Enum):
    NONE='NONE'
    TR4='SX1262TR4_GC_433'
    TR8='SX1262TR8_GC_868'
@dataclass(frozen=True)
class RegionalPolicy:
    allowed_hz:tuple=()
    max_dbm:float=-100
    approved:bool=False
@dataclass(frozen=True)
class LoRaAssembly:
    population:LoRaPopulation=LoRaPopulation.NONE
    trusted:bool=False
    antenna_band:int|None=None
    commissioned:bool=False
    def band(self):
        if not isinstance(self.population,LoRaPopulation):return None
        return {LoRaPopulation.TR4:433,LoRaPopulation.TR8:868}.get(self.population)
    def valid(self):
        return (self.trusted is True and self.band() is not None and self.antenna_band==self.band())
    def permits_tx(self,hz,dbm,policy,*,responding=False,initialized=False,power_stable=False,main_pack_valid=False,airtime_ok=False):
        if not isinstance(policy,RegionalPolicy):return False
        if not (self.valid() and self.commissioned is True and responding is True and initialized is True and power_stable is True and main_pack_valid is True and airtime_ok is True and policy.approved is True):return False
        if not all(isinstance(v,(int,float)) and math.isfinite(v) for v in [hz,dbm,policy.max_dbm]):return False
        lo,hi=(410000000,525000000) if self.band()==433 else (862000000,960000000)
        try:
            allowed=any(all(isinstance(v,(int,float)) and not isinstance(v,bool) and math.isfinite(v) for v in (a,b)) and lo<=a<=hz<=b<=hi for a,b in policy.allowed_hz)
        except (TypeError,ValueError):return False
        return lo<=hz<=hi and -9<=dbm<=min(22,policy.max_dbm) and allowed
# SX1262 GetStatus demonstrates response, never identifies the module RF band.
# Unusable/absent LoRa has no authority to invalidate autonomous ARDF operation.
