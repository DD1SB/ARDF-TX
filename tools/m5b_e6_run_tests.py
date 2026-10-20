"""Run and record actual numerical unittest results, including expected risk cases."""
import unittest
from m5b_e6_common import *
import test_m5b_e6_analysis as checks


def main():
    guard();suite=unittest.defaultTestLoader.loadTestsFromModule(checks)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    save('analysis-test-results.json',dict(tests_run=result.testsRun,failures=len(result.failures),
        errors=len(result.errors),skipped=len(result.skipped),successful=result.wasSuccessful(),
        source_sha256={p.name:sha(p) for p in (ROOT/'tools').glob('*m5b_e6*.py')},
        interpretation='Numerical/regression tests can PASS while engineering safety envelope remains HOLD. Expected unsafe sensitivities are detected, not approved.',
        physical='NOT_RUN'))
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__=='__main__':main()
