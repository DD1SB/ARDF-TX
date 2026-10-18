import unittest
from dataclasses import replace
from model import *
class Safety(unittest.TestCase):
    def context(self,band=Band.RF2M):
        return Context(band,'NORMAL' if band is Band.RF2M else 'PA','2S' if band is Band.RF2M else '4S',7.4 if band is Band.RF2M else 14.8,'BOOST2S' if band is Band.RF2M else 'RF80_FULL',144700000 if band is Band.RF2M else 3550000,True,allowed=((144000000,146000000),(3500000,3800000)),calibrated=True)
    def ready(self,band=Band.RF2M):
        c=Controller();c.configure(self.context(band));c.step(100000);c.arm();c.step(300000);c.start_slot(pa_rail_valid=True);return c
    def test_wrong_battery(self):
        for p,v in [('4S',14.8),('unknown',7.4),('2S',16.8)]:
            with self.assertRaises(ValueError):Controller().configure(replace(self.context(),pack=p,volts=v))
    def test_missing_module(self):
        with self.assertRaises(ValueError):Controller().configure(replace(self.context(),present=False))
    def test_contradictory_population(self):
        for module in ['TRAIN_ONLY','RF80_FULL','unknown']:
            with self.assertRaises(ValueError):Controller().configure(replace(self.context(),module=module))
    def test_stuck_i2c(self):
        with self.assertRaises(ValueError):Controller().configure(replace(self.context(),bus_ok=False))
    def test_invalid_rtc(self):
        with self.assertRaises(ValueError):Controller().configure(replace(self.context(),time_valid=False))
    def test_missing_calibration(self):
        with self.assertRaises(ValueError):Controller().configure(replace(self.context(),calibrated=False))
    def test_runtime_validation_failure(self):
        c=self.ready();c.context.volts=16.8;c.step(25000);self.assertEqual(c.state,State.FAULT);self.assertFalse(c.signals['ARM'])
    def test_frequency(self):
        for f in [0,143000000,144400000,145000000,3550000]:
            with self.assertRaises(ValueError):Controller().configure(replace(self.context(),frequency=f))
        with self.assertRaises(ValueError):Controller().configure(replace(self.context(),allowed=()))
    def test_reset_while_transmitting(self):
        c=self.ready();c.key(1);c.reset();self.assertFalse(any(c.signals.values()));self.assertEqual(c.state,State.SAFE)
    def test_lost_progress(self):
        for b in Band:
            c=self.ready(b);c.step(300000,False);self.assertEqual(c.state,State.FAULT);self.assertFalse(c.signals['ARM']);c.step(300000);self.assertEqual(c.state,State.FAULT)
    def test_unexpected_fault_status(self):
        c=self.ready();c.status(False);self.assertEqual(c.state,State.FAULT)
        c=Controller();c.configure(self.context());c.arm(accepted_before=True);self.assertEqual(c.state,State.FAULT)
    def test_disarmed_low_is_not_missing(self):
        c=Controller();c.status(False);self.assertEqual(c.state,State.SAFE)
    def test_profile_combinations(self):
        with self.assertRaises(ValueError):Controller().configure(replace(self.context(),path='TRAIN',full=True))
        with self.assertRaises(ValueError):Controller().configure(replace(self.context(Band.RF80),rf80_code=(1,1)))
    def test_lora_absence_and_loss(self):
        c=self.ready();c.communication_loss('LoRa');self.assertEqual(c.state,State.TX)
    def test_usb_plug_unplug(self):
        c=Controller();c.usb(True);c.usb(False);self.assertFalse(c.signals['ARM'])
    def test_brownout_and_startup(self):
        c=self.ready();c.reset();self.assertFalse(c.signals['INIT_OK']);self.assertFalse(c.signals['MUTE_RELEASE'])
    def test_unpowered_module(self):
        with self.assertRaises(ValueError):Controller().configure(replace(self.context(),present=False))
        c=Controller();self.assertFalse(c.signals['POWER2M']);self.assertFalse(c.physical_bus_enabled(Band.RF2M))
    def test_controller_supply_loss(self):
        c=self.ready();c.reset();self.assertFalse(c.signals['POWER2M']);self.assertFalse(c.signals['ARM'])
    def test_conflicting_band_requests(self):
        c=self.ready()
        with self.assertRaises(ValueError):c.configure(self.context(Band.RF80))
    def test_deliberate_rearm(self):
        c=self.ready();c.stop('test')
        with self.assertRaises(ValueError):c.configure(self.context())
        c.recover();c.configure(self.context());c.step(100000);c.arm();self.assertEqual(c.state,State.ARMED)
    def test_rtc_bus_isolation(self):
        c=Controller();c.configure(self.context(Band.RF80));c.signals['BUS80']=1;c.step(100000);c.arm();self.assertFalse(c.physical_bus_enabled(Band.RF80))
    def test_stabilization(self):
        for b in Band:
            c=Controller();c.configure(self.context(b));c.step(100000);c.arm()
            with self.assertRaises(ValueError):c.start_slot()
    def test_module_id_current_values(self):
        for r,n in [(18200,'BOOST2S'),(39200,'BUCK4S'),(82000,'TRAIN_ONLY')]:self.assertEqual(identify_rf2m(3.3*r/(33000+r)),n)
        for v in [0,3.3,1.65]:self.assertIsNone(identify_rf2m(v))
    def test_native_prepare_sequence(self):
        c=Controller();c.configure(self.context())
        self.assertEqual([c.signals[x] for x in ['PREPARE','PA_PREPARE','MUTE_RELEASE','ARM','SLOT','KEY']],[1,1,1,0,0,0])
        c=Controller();c.configure(replace(self.context(),path='TRAIN',module='TRAIN_ONLY'))
        self.assertEqual([c.signals[x] for x in ['PREPARE','PA_PREPARE','PATH_TRAIN','PROFILE_FULL','ARM']],[1,0,1,0,0])
    def test_power_codes_are_written(self):
        for code in [(0,0),(1,0),(0,1)]:
            c=Controller();c.configure(replace(self.context(Band.RF80),rf80_code=code));self.assertEqual((c.signals['PWR0'],c.signals['PWR1']),code)
    def test_progress_establishment(self):
        c=Controller();c.configure(self.context())
        with self.assertRaises(ValueError):c.arm()
    def test_rtc_validity(self):
        self.assertTrue(rtc_fields_valid(2026,10,18,12,30,0))
        for x in [(2026,2,30,0,0,0),(2026,10,18,24,0,0),(2000,1,1,0,0,0)]:self.assertFalse(rtc_fields_valid(*x))
        self.assertFalse(rtc_fields_valid(2026,10,18,0,0,0,por=True))
    def test_lora_detect(self):
        for s in [None,0,255,16]:self.assertFalse(detect_lora(s))
        self.assertTrue(detect_lora(0x24));self.assertFalse(detect_lora(0x24,True))
    def test_pack_identity(self):
        cal=PackIDCalibration((.4,1.0),.2e-6,.01,qualified=True)
        self.assertEqual(identify_pack(.20,7,calibration=cal),'2S');self.assertEqual(identify_pack(.68,14,calibration=cal),'4S')
        for v,s in [(0,7),(3.3,7),(1.65,14),(2.269,7),(-.24,14)]:self.assertIsNone(identify_pack(v,s,calibration=cal))
    def test_pa_rail_required(self):
        c=Controller();c.configure(self.context());c.step(100000);c.arm();c.step(300000);c.start_slot()
        self.assertEqual(c.state,State.FAULT);self.assertFalse(c.signals['SLOT'])
        c=Controller();c.configure(replace(self.context(),path='TRAIN',module='TRAIN_ONLY'));c.step(100000);c.arm();c.step(300000);c.start_slot()
        self.assertEqual(c.state,State.TX);self.assertFalse(c.signals['PA_PREPARE'])
    def test_pa_rail_loss(self):
        c=self.ready();c.pa_rail_sample(False);self.assertEqual(c.state,State.FAULT);self.assertFalse(c.signals['ARM'])
    def test_timer_morse(self):
        e=morse_edges('SOS',12);self.assertEqual(len(e),18);self.assertEqual(e[1][0]-e[0][0],100000);self.assertTrue(all(t%100000==0 for t,_ in e))
if __name__=='__main__':unittest.main()
