#!/usr/bin/env python3
"""
COLREGS-3D Comprehensive Offline Test Runner.
Executes all 4 Tiers (230 test cases) with structured reporting and exits with code 0 on success.
100% Offline execution, zero network calls.
"""

import os
import sys
import time
import unittest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

if sys.stdout.encoding != 'utf-8':

    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_tier(tier_name: str, module_name: str) -> tuple:
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(module_name)
    test_count = suite.countTestCases()

    print(f"\n{'='*75}")
    print(f"▶ EXECUTING {tier_name} ({test_count} tests)")
    print(f"{'='*75}")

    runner = unittest.TextTestRunner(verbosity=1)
    start_t = time.perf_counter()
    result = runner.run(suite)
    duration = time.perf_counter() - start_t

    return result, test_count, duration


def main():
    print("=" * 75)
    print("   COLREGS-3D COMPREHENSIVE AUTOMATED E2E TEST SUITE (TIERS 1-4)")
    print("   Platform: 100% Offline | Framework: Python unittest | Engine: NumPy")
    print("=" * 75)

    tiers = [
        ("TIER 1: FEATURE ISOLATION COVERAGE (F1.1 - F6.2)", "tests.test_tier1_features"),
        ("TIER 2: BOUNDARY & CORNER CASES (F1.1 - F6.2)", "tests.test_tier2_boundaries"),
        ("TIER 3: CROSS-FEATURE SYSTEM COMBINATIONS", "tests.test_tier3_combinations"),
        ("TIER 4: REAL-WORLD OPERATIONAL SCENARIOS", "tests.test_tier4_scenarios"),
    ]

    tier_results = []
    total_tests = 0
    total_failures = 0
    total_errors = 0
    start_all = time.perf_counter()

    for title, module in tiers:
        res, count, dur = run_tier(title, module)
        tier_results.append({
            "title": title,
            "count": count,
            "passed": count - len(res.failures) - len(res.errors),
            "failed": len(res.failures),
            "errors": len(res.errors),
            "duration": dur
        })
        total_tests += count
        total_failures += len(res.failures)
        total_errors += len(res.errors)

    total_time = time.perf_counter() - start_all

    print(f"\n{'='*75}")
    print("                        TEST EXECUTION SUMMARY REPORT")
    print(f"{'='*75}")
    print(f"{'Tier Name':<50} | {'Tests':<6} | {'Passed':<6} | {'Failed':<6} | {'Time (s)':<8}")
    print("-" * 75)

    for tr in tier_results:
        print(f"{tr['title']:<50} | {tr['count']:<6} | {tr['passed']:<6} | {tr['failed']:<6} | {tr['duration']:<8.3f}")

    print("-" * 75)
    print(f"{'TOTAL TEST CASES EVALUATED':<50} | {total_tests:<6} | {total_tests - total_failures - total_errors:<6} | {total_failures + total_errors:<6} | {total_time:<8.3f}")
    print("=" * 75)

    if total_failures == 0 and total_errors == 0:
        print("\n>>> ALL 230+ TEST CASES PASSED WITH 100% SUCCESS! (CLEAN EXIT 0) <<<")
        print(">>> PLATFORM UPGRADE FULLY VERIFIED READY FOR CERTIFICATION! <<<\n")
        return 0
    else:
        print(f"\n>>> TEST SUITE FAILED: {total_failures} failures, {total_errors} errors! <<<\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
