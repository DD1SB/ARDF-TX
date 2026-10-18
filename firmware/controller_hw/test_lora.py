"""LoRa host-only negative fixtures. No target firmware/RF qualification."""
import unittest
from dataclasses import replace
from lora import *
from model import *
class LoRaContract(unittest.TestCase):
 def setUp(self):
  self.p=RegionalPolicy(((433500000,433500000),),10,True) # synthetic policy, not legal advice
  self.a=LoRaAssembly(LoRaPopulation.TR4,True,433,True)
  self.k=dict(responding=True,initialized=True,power_stable=True,main_pack_valid=True,airtime_ok=True)
 def test_unknown_population(self):
  for a in [LoRaAssembly(),replace(self.a,population='UNKNOWN'),replace(self.a,trusted=False),replace(self.a,population=LoRaPopulation.NONE)]:self.assertFalse(a.permits_tx(433500000,10,self.p,**self.k))
 def test_antenna_population(self):
  for a in [replace(self.a,antenna_band=868),replace(self.a,antenna_band=None),replace(self.a,commissioned=False)]:self.assertFalse(a.permits_tx(433500000,10,self.p,**self.k))
  self.assertTrue(self.a.permits_tx(433500000,10,self.p,**self.k))
  b=LoRaAssembly(LoRaPopulation.TR8,True,868,True);p=RegionalPolicy(((868300000,868300000),),10,True)
  self.assertTrue(b.permits_tx(868300000,10,p,**self.k));self.assertFalse(b.permits_tx(433500000,10,self.p,**self.k))
 def test_regional_policy_and_power(self):
  for hz,power in [(868300000,10),(433500001,10),(433500000,22),(433500000,float('nan')),(433500000,-10)]:self.assertFalse(self.a.permits_tx(hz,power,self.p,**self.k))
  for p in [None,{},RegionalPolicy(),replace(self.p,approved=False),replace(self.p,max_dbm=9),replace(self.p,allowed_hz=None),replace(self.p,allowed_hz=((1,),)),replace(self.p,allowed_hz=((float('nan'),433500000),))]:self.assertFalse(self.a.permits_tx(433500000,10,p,**self.k))
 def test_no_blind_band_detection(self):
  self.assertTrue(detect_lora(0x24))
  for pop in [LoRaPopulation.NONE,'SX1262']:
   a=replace(self.a,population=pop);self.assertFalse(a.permits_tx(433500000,10,self.p,**self.k))
 def test_reset_loss_and_absence(self):
  for k in self.k:
   kw=dict(self.k);kw[k]=False;self.assertFalse(self.a.permits_tx(433500000,10,self.p,**kw))
 def test_base_operation_independent(self):
  c=Context(Band.RF80,'FOX','2S',7,'RF80_FOX',3550000,True,allowed=((3500000,3800000),),calibrated=True)
  for fitted in [False,True]:replace(c,lora_present=fitted).validate()
if __name__=='__main__':unittest.main()
