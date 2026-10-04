"""
Master COLREGS-3D E2E Test Suite.
Aggregates all 4 Tiers (T1: Feature Coverage, T2: Boundary Cases, T3: Combinations, T4: Scenarios).
Total Test Count: 230 test cases.
"""

import os
import sys
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Import all tier suites

from tests.test_tier1_features import *
from tests.test_tier2_boundaries import *
from tests.test_tier3_combinations import *
from tests.test_tier4_scenarios import *


def suite():
    loader = unittest.TestLoader()
    e2e_suite = unittest.TestSuite()
    e2e_suite.addTests(loader.loadTestsFromName("tests.test_tier1_features"))
    e2e_suite.addTests(loader.loadTestsFromName("tests.test_tier2_boundaries"))
    e2e_suite.addTests(loader.loadTestsFromName("tests.test_tier3_combinations"))
    e2e_suite.addTests(loader.loadTestsFromName("tests.test_tier4_scenarios"))
    return e2e_suite


if __name__ == "__main__":
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite())
    import sys
    sys.exit(0 if result.wasSuccessful() else 1)
