"""Independent algebra/energy/periodicity tests, not generated-report matching."""
import math
import unittest
import numpy as np
from scipy.linalg import expm
from m5b_e6_power import native,operating
from m5b_e6_thermal import Network,NAMES,morse,schedule,powers,run_cycle
from m5b_e6_stress import audio
from m5b_e6_faults import absorbed


class Analysis(unittest.TestCase):
    def test_native_feedback_and_rails(self):
        z=native();self.assertAlmostEqual(z['feedback_gain'],2.8)
        self.assertAlmostEqual(z['full_buck_V'],8.9996)
        self.assertAlmostEqual(z['reduced_buck_V'],7.5096)
        self.assertAlmostEqual(z['full_rail_V'],9.02086)

    def test_known_ERP_carrier_mean_PEP(self):
        z=operating(1.)
        self.assertAlmostEqual(z['mean']['connector_RF_W'],1.2589254117941673*1.32,places=9)
        self.assertAlmostEqual(1.2589254117941673*3.24,4.078918334213102,places=9)
        self.assertLess(z['mean']['connector_RF_W'],2)

    def test_bias_is_not_added_twice(self):
        z=operating(1.,tone=False)
        self.assertAlmostEqual(z['mean']['PA_DC_W'],10**.175/.5,places=9)
        zz=operating(1.,tone=False,bias=.05)
        self.assertAlmostEqual(z['mean']['PA_DC_W'],zz['mean']['PA_DC_W'],places=9)

    def test_waveform_terminal_energy_conservation(self):
        for e in [.25,.3,.5,1.]:
            z=operating(e,waveform=True,phases=128)
            self.assertLess(max(abs(x['terminal_energy_balance_W']) for x in z['waveform']),1e-10)
            self.assertAlmostEqual(z['mean']['DC_input_W'],z['mean']['PA_W']+z['mean']['pass_W']+z['mean']['helper_W']+z['mean']['other_PCB_W']+z['mean']['connector_RF_W'],places=8)
            self.assertAlmostEqual(z['mean']['DC_input_W'],z['mean']['RF_battery_input_W']+z['mean']['controller_3V3_input_W'],places=8)

    def test_space_is_carrier_not_power_off(self):
        mark=operating(1.);space=operating(1.,tone=False)
        self.assertGreater(space['mean']['PA_W'],1.)
        self.assertGreater(space['mean']['pass_W'],mark['mean']['pass_W'])
        self.assertGreater(mark['mean']['PA_W'],space['mean']['PA_W'])

    def test_helper_is_derived_from_pass_base_current(self):
        a=operating(1.,tone=False,beta=60);b=operating(1.,tone=False,beta=20)
        self.assertGreater(b['mean']['helper_W'],a['mean']['helper_W']*2)
        self.assertLess(a['mean']['helper_W'],.2)

    def test_M2_different_family_must_not_hide_current_trip(self):
        z=operating(1.,eta=.45,model='M2_dynamic_efficiency_plus_bias')
        self.assertFalse(z['below_nominal_current_trip'])

    def test_morse_MOE_exact_symbols_and_gaps(self):
        z=morse('MOE',12);self.assertEqual(sum(s for d,s in z),6)
        self.assertAlmostEqual(sum(d for d,s in z if s),1.6)
        self.assertAlmostEqual(sum(d for d,s in z),3.2)

    def test_actual_MOE_MOI_MOS_MOH_MO5_differ(self):
        z=[sum(d for d,s in morse(t,12)) for t in ['MOE','MOI','MOS','MOH','MO5']]
        self.assertEqual(len(set(round(v,4) for v in z)),5)

    def test_full_slot_and_group_durations(self):
        for t in ['MOE','MOI','MOS','MOH','MO5']:
            for slot,cycle in [(60,300),(12,60)]:
                s=schedule(slot,cycle,t)
                self.assertAlmostEqual(sum(d for d,x in s),cycle)
                self.assertAlmostEqual(sum(d for d,x in s if x!='off'),slot)

    def test_spectral_propagator_against_independent_expm(self):
        n=Network();a=-n.G/n.C[:,None]
        for t in [.001,.1,60,300]:
            np.testing.assert_allclose(n.transition(t),expm(a*t),atol=3e-10,rtol=1e-7)

    def test_steady_energy_balance(self):
        n=Network();q=np.zeros(len(NAMES));q[[0,4,6]]=[2,3,.1];x=n.equilibrium(q)
        spread=next(e['K_W'] for e in n.edges if e['a']=='shared_plate' and e['b']=='fins')
        self.assertAlmostEqual(x[9]/(n.sink_R-spread),sum(q),places=9)

    def test_no_instantaneous_cold_junction_mass_shortcut(self):
        n=Network();q=np.zeros(len(NAMES));q[0]=4
        x=n.advance(np.zeros(len(NAMES)),q,.1)
        self.assertGreater(x[0],x[8]+5)

    def test_large_aluminium_mass_does_not_remove_local_resistance(self):
        q=np.zeros(len(NAMES));q[0]=2
        a=Network(mass_g=100);b=Network(mass_g=1000)
        x=a.equilibrium(q);y=b.equilibrium(q)
        self.assertAlmostEqual(x[0]-x[8],y[0]-y[8],places=8)
        self.assertGreater(x[0]-x[8],35)

    def test_first_pulse_is_below_repeated_warm_peak(self):
        n=Network();z=operating(1.)['mean'];s=operating(1.,tone=False)['mean']
        q={'mark':powers(z),'space':powers(s),'off':np.zeros(len(NAMES))}
        r,_,_=run_cycle(n,schedule(60,300,'MO5'),q)
        self.assertGreater(r['periodic_max_C']['PA_junction'],r['first_cycle_max_C']['PA_junction'])
        self.assertLess(r['periodic_residual_C'],1e-7)

    def test_power_off_cools_all_nodes_after_sufficient_time(self):
        n=Network();q=np.zeros(len(NAMES));q[0]=2;x=n.equilibrium(q)
        y=n.advance(x,np.zeros(len(NAMES)),10000)
        self.assertLess(max(y),.01)

    def test_ambient_changes_are_one_for_one(self):
        n=Network();q={'space':powers(operating(1.,tone=False)['mean'])}
        a,_,_=run_cycle(n,[(1,'space')],q,25);b,_,_=run_cycle(n,[(1,'space')],q,40)
        for key in NAMES:self.assertAlmostEqual(b['periodic_max_C'][key]-a['periodic_max_C'][key],15,places=7)

    def test_shared_coupling_exists(self):
        n=Network();q=np.zeros(len(NAMES));q[4]=3;x=n.equilibrium(q)
        self.assertGreater(x[0],10)
        self.assertAlmostEqual(x[0],x[8],places=8)

    def test_sensor_does_not_instantly_follow_fault(self):
        n=Network(sensor_tau=15);q=np.zeros(len(NAMES));q[4]=10
        x=n.advance(np.zeros(len(NAMES)),q,.1)
        self.assertGreater(x[5],x[10]*100)

    def test_AM_ripple_converges(self):
        n=Network(capacity_scale=.1)
        a=audio(n,operating(1.,waveform=True,phases=128),128)
        b=audio(n,operating(1.,waveform=True,phases=256),256)
        self.assertLess(a['unmodelled_harmonic_power_W'],1e-9)
        self.assertAlmostEqual(a['positive_ripple_C']['PA_junction'],b['positive_ripple_C']['PA_junction'],delta=.02)

    def test_known_native_copper_storage_never_scaled_away(self):
        a=Network(capacity_scale=.1);b=Network(capacity_scale=3)
        storage=a.config['known_Cu_via_storage'];self.assertEqual(storage['via_count'],98)
        self.assertGreater(storage['via_copper_J_K'],0)
        for n,key in [(2,'top_copper_J_K'),(11,'bottom_copper_J_K')]:
            self.assertGreater(a.C[n],storage[key]+storage['via_copper_J_K']/2)
            self.assertGreater(b.C[n],a.C[n])

    def test_reflected_RF_heat_conserves_input_energy(self):
        z=operating(1.,waveform=True,phases=128)
        for fraction in [0,.5,1]:
            a=absorbed(z,fraction)
            for x,y in zip(a['waveform'],z['waveform']):
                self.assertAlmostEqual(x['DC_input_W'],y['DC_input_W'])
                self.assertAlmostEqual(x['pass_W'],y['pass_W'])
                self.assertAlmostEqual(x['DC_input_W'],sum(x[k] for k in ['PA_W','pass_W','helper_W','other_PCB_W','connector_RF_W','envelope_storage_W']),places=8)

    def test_same_point_unsafe_PA_can_evade_existing_sensors(self):
        n=Network(source_R=11.846896331207134)
        mark=absorbed(operating(1.,eta=.4,waveform=True,phases=256),1)
        space=absorbed(operating(1.,eta=.4,tone=False),1)
        self.assertLess(mark['maximum']['regulated_current_A'],1.797)
        q={'mark':powers(mark['mean']),'space':powers(space['mean']),'off':np.zeros(len(NAMES))}
        r,_,_=run_cycle(n,schedule(60,300,'MO5'),q)
        self.assertGreater(r['periodic_max_C']['PA_junction']+audio(n,mark,256)['positive_ripple_C']['PA_junction'],125)
        self.assertLess(r['periodic_max_C']['pass_case'],60)
        self.assertLess(r['periodic_max_C']['NTC'],65.85)

    def test_temporal_sampling_converges(self):
        n=Network();q={'space':powers(operating(1.,tone=False)['mean']),'off':np.zeros(len(NAMES))}
        a,_,_=run_cycle(n,[(60,'space'),(240,'off')],q,samples=.5)
        b,_,_=run_cycle(n,[(60,'space'),(240,'off')],q,samples=.05)
        for name in NAMES:self.assertAlmostEqual(a['periodic_max_C'][name],b['periodic_max_C'][name],delta=.02)

    def test_manufacturer_resistance_cannot_be_replaced_by_sink_mass(self):
        n=Network();self.assertTrue(any(e['a']=='PA_junction' and e['K_W']==3 for e in n.edges))
        z=operating(1.,waveform=True,phases=256)
        bound=3*(z['maximum']['PA_W']-z['mean']['PA_W'])
        self.assertGreater(bound,5)


if __name__=='__main__':unittest.main(verbosity=2)
