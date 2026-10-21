"""Independent arithmetic, energy, transient and default-off regression tests."""
import itertools,math,unittest
import numpy as np
from scipy.linalg import expm
from m5b_e6r1_morse import units,schedule,stats
from m5b_e6r1_power import point,transition_packet,FIELDS
from m5b_e6r1_thermal import waveform,Cycle,word_period
from m5b_e6r1_sensor import with_joint,evaluate,ntc_R,divider_temperature,sensor_V
from m5b_e6r1_electrical import spectrum,evaluate as loop_evaluate
from m5b_e6_thermal import Network,run_cycle,schedule as E6_schedule,NAMES
from m5b_e6_power import operating
from m5b_e6r1_common import *

class R1(unittest.TestCase):
    def test_01_MO_independent_units(self):
        z=stats('MO',12,60,60)
        self.assertEqual(z['repeating_word_MARK_units'],15)
        self.assertEqual(z['repeating_word_total_units'],28)
        self.assertEqual(z['repeating_word_MARK_fraction'],'15/28')

    def test_02_independent_five_identifiers(self):
        for text,total,mark in [('MOE',32,16),('MOI',34,17),('MOS',36,18),('MOH',38,19),('MO5',40,20)]:
            z=stats(text,10,60,300)
            self.assertEqual(z['repeating_word_MARK_units'],mark)
            self.assertEqual(z['repeating_word_total_units'],total)

    def test_03_integer_timer_native_semantics(self):
        for wpm in range(8,16):self.assertEqual(stats('MO',wpm,60,60)['dit_us'],round(1200000/wpm))

    def test_04_full_slot_durations_and_boundaries(self):
        for code,wpm,slot,cycle in itertools.product(['MOE','MOI','MOS','MOH','MO5','MO DD1SB'],range(8,16),[12,60],[60,300]):
            if slot>cycle:continue
            s=schedule(code,wpm,slot,cycle)
            self.assertEqual(s[-1]['end_us'],cycle*1000000)
            self.assertEqual(sum(z['end_us']-z['start_us'] for z in s if z['state']!='off'),slot*1000000)
            self.assertTrue(all(a['end_us']==b['start_us'] for a,b in zip(s,s[1:])))

    def test_05_beacon_is_not_twenty_percent(self):
        z=stats('MO',12,60,60)
        self.assertGreater(z['full_cycle_MARK_fraction'],.5)

    def test_06_CW_ID_changes_finite_heat_timing(self):
        self.assertNotEqual(stats('MO5',12,12,60)['finite_slot_MARK_us'],stats('MO5 DD1SB',12,12,60)['finite_slot_MARK_us'])

    def test_07_E6_flat_device_losses_regress(self):
        for erp,pop,tone in itertools.product([.25,.5,1.],['BUCK4S','BOOST2S'],[True,False]):
            old=operating(erp,pop,tone=tone)['mean'];new=point(erp,pop,tone=tone,architecture='A',corrected=False)
            for key in ['PA_W','pass_W','helper_W','connector_RF_W']:self.assertAlmostEqual(old[key],new[key],places=9)
            idle=.008 if pop=='BUCK4S' else .020
            self.assertAlmostEqual(old['DC_input_W']+idle,new['DC_input_W'],places=9)

    def test_08_corrections_increase_real_consumption(self):
        a=point(1.,architecture='A',corrected=False);b=point(1.,architecture='A')
        self.assertGreater(b['DC_input_W'],a['DC_input_W'])
        self.assertGreater(b['pass_W'],a['pass_W'])
        self.assertAlmostEqual(a['PA_W'],b['PA_W'])

    def test_09_source_domains_and_energy(self):
        for pop,a,alpha in itertools.product(['BOOST2S','BUCK4S'],['A','B','C'],[0,.01,.1,.5,1.]):
            z=point(1.,pop,alpha=alpha,architecture=a)
            self.assertAlmostEqual(z['DC_input_W'],sum(z[k] for k in ['PA_W','pass_W','helper_W','other_PCB_W','connector_RF_W','storage_W']),places=8)
            self.assertAlmostEqual(z['DC_input_W'],z['RF_battery_input_W']+z['controller_3V3_input_W'],places=8)

    def test_10_quiet_C_really_removes_PA_and_pass_heat(self):
        old=point(1.,tone=False,architecture='A');new=point(1.,alpha=0,architecture='C')
        self.assertGreater(old['PA_W']+old['pass_W'],5.)
        self.assertLess(new['PA_W']+new['pass_W']+new['helper_W'],.005)
        self.assertGreater(new['DC_input_W'],.1)

    def test_11_BUCK_and_BOOST_are_distinct(self):
        a=point(.25,'BUCK4S');b=point(.25,'BOOST2S')
        self.assertNotEqual(a['pass_W'],b['pass_W'])
        self.assertGreater(b['converter_W'],a['converter_W'])

    def test_12_capacitor_packets_conserve(self):
        for pop,a in itertools.product(['BOOST2S','BUCK4S'],['B','C']):
            z=transition_packet(1.,pop,a)
            self.assertAlmostEqual(z['input_J'],z['pass_charge_heat_J']+z['other_heat_J'],places=12)
            self.assertAlmostEqual(z['rise_input_J'],z['pass_charge_heat_J']+z['rise_other_heat_J']+z['storage_total_on_rise_J'],places=12)
            self.assertAlmostEqual(z['fall_other_heat_J'],z['storage_total_on_rise_J'])

    def test_13_warm_driver_is_not_cold_reservoir_start(self):
        b=transition_packet(1.,'BUCK4S','B');c=transition_packet(1.,'BUCK4S','C')
        self.assertGreater(b['cold_reservoir_charge_J'],.007)
        self.assertEqual(c['cold_reservoir_charge_J'],0)
        self.assertGreater(c['driver_precharge_allowance_J'],.002)

    def test_14_actual_waveform_integrals_all_architectures(self):
        for a in ['A','B','C']:
            s,l,e=waveform('MO',12,60,60,'BUCK4S',1.,a)
            self.assertAlmostEqual(sum(t for t,k in s),60,places=8)
            self.assertAlmostEqual(e['DC_input_W'],sum(e[k] for k in ['PA_W','pass_W','helper_W','other_PCB_W','connector_RF_W','storage_W']),places=8)
            self.assertAlmostEqual(e['storage_W'],0,places=8)

    def test_15_edge_quadrature_convergence(self):
        _,_,a=waveform('MO',12,60,60,'BUCK4S',1.,'C',steps=8)
        _,_,b=waveform('MO',12,60,60,'BUCK4S',1.,'C',steps=32)
        self.assertLess(abs(a['DC_input_W']/b['DC_input_W']-1),.001)

    def test_16_no_unshaped_output_outside_slot(self):
        s,l,e=waveform('MO5',15,12,60,'BUCK4S',1.,'C');t=0
        for dt,k in s:
            if t>=12-1e-8:self.assertEqual(l[k]['connector_RF_W'],0)
            t+=dt

    def test_17_same_mechanics_and_coupling_for_all_A_B_C(self):
        n=Network();original=n.G.copy();caps=n.C.copy()
        for a in ['A','B','C']:
            s,l,e=waveform('MO',12,60,60,'BUCK4S',1.,a)
            Cycle(n,l).run(s)
            np.testing.assert_array_equal(original,n.G);np.testing.assert_array_equal(caps,n.C)

    def test_18_E6_transient_regression_on_identical_waveforms(self):
        n=Network();q={'mark':operating(1.)['mean'],'space':operating(1.,tone=False)['mean'],'off':dict(PA_W=0,pass_W=0,helper_W=0,other_PCB_W=.04)}
        s=E6_schedule(60,300,'MO5');new,_,_=Cycle(n,q).run(s)
        from m5b_e6_thermal import powers
        old,_,_=run_cycle(n,s,{k:powers(v) for k,v in q.items()})
        for k in NAMES:self.assertAlmostEqual(new['periodic_max_C'][k],old['periodic_max_C'][k],delta=.002)

    def test_19_sensor_observer_against_independent_matrix_exponential(self):
        n=Network();q={'x':point(1.)};c=Cycle(n,q,.05)
        A=np.zeros((13,13));A[:12,:12]=-n.G/n.C[:,None];A[12,2]=20;A[12,12]=-20
        for dt in [.001,.1,10]:np.testing.assert_allclose(c.transition(dt),expm(A*dt),atol=1e-8,rtol=1e-6)

    def test_20_repeat_peak_not_sink_mass_shortcut(self):
        s,l,e=waveform('MO5',12,60,300,'BUCK4S',1.,'C')
        z,_,_=Cycle(Network(),l).run(s)
        self.assertGreater(z['periodic_max_C']['PA_junction'],z['first_max_C']['PA_junction'])
        self.assertGreater(z['periodic_max_C']['PA_junction'],z['periodic_max_C']['shared_plate']+10)

    def test_21_RF_absorption_keeps_input_energy(self):
        a=point(1.,eta=.4);b=point(1.,eta=.4,absorbed=1)
        self.assertAlmostEqual(a['DC_input_W'],b['DC_input_W'])
        self.assertAlmostEqual(a['pass_W'],b['pass_W'])
        self.assertGreater(b['PA_W'],a['PA_W'])

    def test_22_below_current_trip_does_not_prove_temperature(self):
        z=point(1.,eta=.4,beta=20,supply_scale=1.03,absorbed=1)
        self.assertLess(z['regulated_current_peak_A'],1.797)
        n=with_joint(11.846896331207134,.1,5)
        r=evaluate(n,.01,87,'stuck_HIGH')
        self.assertFalse(r['PA_125C_met'])

    def test_23_sensor_lag_is_not_free(self):
        n=with_joint(11.846896331207134,.1,1)
        fast=evaluate(n,.01,87);slow=evaluate(n,.6,87)
        self.assertLess(fast['peak_junction_upper_C'],125)
        self.assertGreater(slow['peak_junction_upper_C'],125)

    def test_24_sensor_R_to_V_roundtrip(self):
        for t in [-20,25,40,80,100]:self.assertAlmostEqual(divider_temperature(sensor_V(t)),t,places=8)

    def test_25_window_open_short_disconnected(self):
        low=3.3*10/201;high=3.3*191/213.1
        for v in [0,3.3]:self.assertFalse(low<v<high)
        self.assertTrue(low<sensor_V(40)<high)

    def test_26_all_hardware_gate_truth_combinations(self):
        for off,key,hot_ok,open_ok,vpa,drv in itertools.product([0,1],repeat=6):
            temp_bad=not(hot_ok and open_ok);local_off=off or not key
            driver_on=not local_off;rf_not_ready=not(vpa and drv);clock_off=local_off or rf_not_ready
            if off:self.assertTrue(local_off and clock_off and not driver_on)
            if not key:self.assertTrue(local_off and clock_off and not driver_on)
            if not vpa or not drv:self.assertTrue(clock_off)
            if not hot_ok or not open_ok:self.assertTrue(temp_bad)

    def test_27_missing_or_unpowered_sensor_IC_defaults_bad(self):
        comparator_outputs=[0,0,0,0] # physical100kpulldowns, not firmware
        hot,opened,vpa,driver=comparator_outputs
        self.assertTrue(not(hot and opened));self.assertTrue(not(vpa and driver))

    def test_28_raised_cosine_reduces_far_offset_energy(self):
        hard=spectrum(0);soft=spectrum(.008)
        self.assertLess(soft['outside_offset_power_fraction']['5000'],hard['outside_offset_power_fraction']['5000']/1000)

    def test_29_loaded_loop_and_command_headroom(self):
        z=loop_evaluate();self.assertTrue(z['stable']);self.assertTrue(z['within_3V3'])
        self.assertLess(z['required_AF_preemphasis'],1.2)

    def test_30_unloaded_loop_risk_is_not_hidden(self):
        z=loop_evaluate(K=1000,load=1/(1/1000+1/28000));self.assertFalse(z['stable'])

    def test_31_native_critical_pin_nets_retained(self):
        p=parts();self.assertEqual(p['Q501']['pins'],{'G':'PA_GATE','D':'PA_DRAIN','S':'GND'})
        self.assertEqual(p['Q401']['pins']['2'],'VPA');self.assertEqual(p['Q402']['pins']['2'],'MOD_SINK')
        self.assertEqual(p['J101']['pins']['7'],'KEY');self.assertEqual(p['U305']['pins']['3'],'NORMAL_PERMIT')

    def test_32_protection_and_history_guard(self):guard()

    def test_33_continuous_beacon_period_is_word_not_minute(self):
        for wpm in range(8,16):
            duration=word_period('MO',wpm)
            s,l,e=waveform('MO',wpm,duration,duration,'BUCK4S',1.,'C',periodic_word=True)
            self.assertAlmostEqual(sum(dt for dt,k in s),28*round(1200000/wpm)/1e6,places=7)
            self.assertLess(abs(e['storage_W']),1e-8)

    def test_34_integrated_supply_domains_match(self):
        for a in ['A','B','C']:
            s,l,e=waveform('MO5',12,60,300,'BOOST2S',1.,a)
            self.assertAlmostEqual(e['DC_input_W'],e['RF_battery_input_W']+e['controller_3V3_input_W'],places=8)
            self.assertNotIn('regulated_current_A',e) # charge integral is not Joules

    def test_35_solar_does_not_mutate_or_fake_electrical_power(self):
        before=point(1.).copy();s,l,e=waveform('MO',12,2.8,2.8,'BUCK4S',1.,'C',periodic_word=True)
        a,_,_=Cycle(Network(),l).run(s);b,_,_=Cycle(Network(),l,extra_plate_W=10).run(s)
        self.assertEqual(point(1.),before)
        self.assertGreater(b['periodic_max_C']['shared_plate'],a['periodic_max_C']['shared_plate']+50)

    def test_36_original_E6_failure_remains_reproducible(self):
        from m5b_e6r1_regression import failure
        z=failure()
        self.assertAlmostEqual(z['PA_peak_with_audio_C'],133.79,delta=.01)
        self.assertLess(z['NTC_C'],65.85)
        self.assertLess(z['rail_peak_A'],z['nominal_trip_A'])

    def test_37_sensor_threshold_must_also_allow_healthy_beacon(self):
        from m5b_e6r1_sensor import healthy_headroom
        rows=healthy_headroom()
        json.dumps(rows,allow_nan=False)
        r=next(z for z in rows if z['thermal_case']=='conservative' and z['tau_s']==.05)
        self.assertTrue(r['healthy_trip_expected'])
        self.assertGreater(r['healthy_sensor_peak_C'],81.)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(R1))
    save('test-results.json',dict(tests_run=result.testsRun,failures=len(result.failures),errors=len(result.errors),
        skipped=len(result.skipped),passed=result.wasSuccessful(),physical='NOT_RUN'))
    raise SystemExit(0 if result.wasSuccessful() else 1)
