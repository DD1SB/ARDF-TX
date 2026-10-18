"""R1 host fixtures. None constitutes a physical fault or IEC ESD test."""
import unittest,itertools
from dataclasses import replace
from model import *
class InputProtection(unittest.TestCase):
    def setUp(self):self.cal=PackIDCalibration((.4,1.0),.2e-6,.01,qualified=True)
    def test_missing_calibration(self):
        for c in [None,replace(self.cal,qualified=False),replace(self.cal,leakage_max=3e-6),replace(self.cal,adc_error=.03),replace(self.cal,frontend_revision=1)]:self.assertIsNone(identify_pack(.77,14,calibration=c))
    def test_powered_off_fault(self):self.assertIsNone(identify_pack(.204,14,rail=0,calibration=self.cal))
    def test_positive_faults(self):
        for vb,raw,a,b,c,error in itertools.product([5.21,7,8.3,11.21,14,16.7],[8.4,16.8],[.983,1.017],[.983,1.017],[.983,1.017],[-.01,.01]):
            rd=1/(1/(33000*b)+1/(100000*c));v=raw*rd/(180000*a+rd)+error
            for sample in [v,min(v,1.1),1.1]:self.assertIsNone(identify_pack(sample,vb,calibration=self.cal))
    def test_open_and_short(self):
        for vb in [5.21,7,8.3,11.21,14,16.7]:
            rd=1/(1/33000+1/100000);v=(vb-.65)*rd/(27000+180000+rd)
            for raw in [0,v]:self.assertIsNone(identify_pack(raw,vb,calibration=self.cal))
    def test_wrong_resistor_and_pack(self):
        for name,r,vb in [('4S',22000,7),('2S',10000,14)]:
            lo,hi=pack_id_bounds(vb,r,self.cal)
            self.assertIsNone(identify_pack((lo+hi)/2,vb,calibration=self.cal))
    def test_brownout_and_USB_only(self):
        for vb,rail in [(0,3.3),(.5008,3.3),(7,0),(14,3.0)]:self.assertIsNone(identify_pack(.77,vb,rail=rail,calibration=self.cal))
    def test_invalid_sample_disarms(self):
        c=Controller();c.context=Context(Band.RF2M,'NORMAL','4S',14,'BUCK4S',144700000,True);c.signals['ARM']=1;c.signals['INIT_OK']=1
        c.battery_sample(None);self.assertEqual(c.state,State.FAULT);self.assertFalse(any(c.signals.values()))
    def test_ambiguous_reading_rejected(self):
        c=PackIDCalibration((0,1.25),2e-6,.01,qualified=True)
        a=pack_id_bounds(5.21,10000,c);b=pack_id_bounds(5.21,22000,c)
        if max(a[0],b[0])<=min(a[1],b[1]):self.assertIsNone(identify_pack((max(a[0],b[0])+min(a[1],b[1]))/2,5.21,calibration=c))
if __name__=='__main__':unittest.main()
