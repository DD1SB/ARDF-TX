"""Assertions on executed ngspice traces, independent of deck construction."""
import unittest,json
import numpy as np
from pathlib import Path
P=Path(__file__).resolve().parents[1]/'hardware/2m/review/M5B-E6R2'
class EnvelopeTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.j=json.loads((P/'simulation-results.json').read_text())
 def case(self,pop='BUCK4S',beta=60,mode='normal',edge=.008):return next(x for x in self.j['cases'] if x['population']==pop and x['pass_beta_assumed']==beta and x['mode']==mode and x['edge_s']==edge)
 def test_executed_cases(self):
  self.assertEqual(len(self.j['cases']),8)
  for x in self.j['cases']:self.assertEqual(x['ngspice_returncode'],0);self.assertGreater(x['points'],100000)
 def test_BUCK_AM_depth(self):self.depth('BUCK4S')
 def test_BOOST_AM_depth(self):self.depth('BOOST2S')
 def depth(self,pop):
  c=self.case(pop);m=(c['mark_envelope_max_V']-c['mark_envelope_min_V'])/(c['mark_envelope_max_V']+c['mark_envelope_min_V']);self.assertGreater(m,.7);self.assertLessEqual(m,.801);self.assertGreater(c['mark_envelope_max_V'],7.1)
 def test_spaces_really_remove_load(self):
  for p in ['BUCK4S','BOOST2S']:
   c=self.case(p);self.assertLess(c['VPA_space_max_V'],.02);self.assertLess(c['pass_space_mean_A'],.005);self.assertLess(c['driver_space_max_V'],.02)
 def test_bias_preparation_is_not_zero_power(self):
  for p in ['BUCK4S','BOOST2S']:self.assertGreater(self.case(p)['rail_space_mean_A'],.002);self.assertLess(self.case(p)['rail_space_mean_A'],.004)
 def test_normal_current_below_trip(self):
  for p in ['BUCK4S','BOOST2S']:c=self.case(p);self.assertGreater(c['rail_peak_A'],1.2);self.assertLess(c['rail_peak_A'],c['nominal_current_threshold_A'])
 def test_overload_latches(self):
  c=self.case(mode='overload');self.assertTrue(c['overcurrent_threshold_crossed']);self.assertTrue(c['latch_remains_faulted']);self.assertGreater(c['trip_time_s'],.014);self.assertLess(c['trip_time_s'],.025)
 def test_forced_fault_overrides_envelope(self):
  c=self.case(mode='fault');self.assertTrue(c['clock_inhibited_after_fault']);self.assertLess(c['VPA_after_fault_max_V'],.02);self.assertLess(c['PA_gate_after_fault_max_V'],.02)
 def test_load_removal_bounded_by_prepared_rail(self):self.assertLess(self.case(mode='load_removal')['VPA_max_V'],9.05)
 def test_load_returns(self):
  c=self.case(mode='load_removal');self.assertGreater(c['recovered_window_max_V'],7.1);self.assertLess(c['recovered_window_min_V'],.9)
 def test_low_beta_clipping_is_visible(self):self.assertLess(self.case(beta=20)['mark_envelope_max_V'],7.)
 def test_edge_sensitivity_no_high_rail_restart(self):
  for e in [.005,.008,.012]:c=self.case(edge=e);self.assertLess(c['VPA_max_V'],7.3);self.assertLess(c['rail_peak_A'],1.4)
 def test_return_ratios(self):
  self.assertEqual(len(self.j['loop_gain']),2)
  for row in self.j['loop_gain']:self.assertTrue(row['positive_margin']);self.assertGreater(min(row['phase_margin_deg']),45)
 def test_flat_space_clock_inhibited(self):
  z=np.loadtxt(P/'simulation/BUCK4S-beta60-normal-8ms.csv',delimiter=',',skiprows=1);s=z[(z[:,0]>.11)&(z[:,0]<.17)];self.assertGreater(s[:,9].min(),3.);self.assertGreater(s[:,12].min(),.1)
if __name__=='__main__':unittest.main(verbosity=2)
