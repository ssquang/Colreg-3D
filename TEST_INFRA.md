# Testing Infrastructure & Methodology: COLREGS-3D Upgrade

## 1. Overview & Strategy
The COLREGS-3D automated test infrastructure provides rigorous, opaque-box, requirement-driven validation across the maritime simulation platform. The testing framework exercises 100% offline verification across all 20 features identified in `PROJECT.md` and `ORIGINAL_REQUEST.md`.

All tests execute without network access, third-party cloud services, or headless browser requirements by leveraging deterministic mathematical models, specification validators, kinematic oracles, schema parsers, and static contract auditors in Python 3 standard library (`unittest`) and `numpy`.

---

## 2. 4-Tier Testing Methodology

```
+-------------------------------------------------------------------------+
|                  TIER 4: REAL-WORLD OPERATIONAL SCENARIOS               |
|      (10 End-to-End Maritime Missions: Dover TSS, Singapore Strait,     |
|             Van Don Fog, STCW OOW Certification Exam, etc.)             |
+-------------------------------------------------------------------------+
                                    ▲
+-------------------------------------------------------------------------+
|                TIER 3: CROSS-FEATURE SYSTEM COMBINATIONS                |
|      (20 Multi-Subsystem Interactions: TSS + Fog + Sound Signals,       |
|        Leeway + 5 Ships + VDR, Instructor QR + WebXR View, etc.)        |
+-------------------------------------------------------------------------+
                                    ▲
+-------------------------------------------------------------------------+
|                TIER 2: BOUNDARY CONDITIONS & CORNER CASES               |
|    (100 Stress Tests: Extreme Speeds, Zero Rudder, CPA = 0.16 NM,       |
|      Buffer Full 1,800 Frames, QR Overflows, Oblique Crossings)         |
+-------------------------------------------------------------------------+
                                    ▲
+-------------------------------------------------------------------------+
|                     TIER 1: FEATURE ISOLATION COVERAGE                  |
|     (100 Tests: 5 Tests per Feature for all 20 Features F1.1 - F6.2,     |
|          Validating Contract Compliance and Happy Path Logic)           |
+-------------------------------------------------------------------------+
```

### Tier 1: Feature Coverage (Isolation)
- **Scope**: 5 isolated tests per feature across all 20 features = **100 tests**.
- **Objective**: Validate core functionality, input-output transforms, contract adherence, and baseline behavior under standard conditions.

### Tier 2: Boundary & Corner Cases
- **Scope**: 5 edge-case tests per feature across all 20 features = **100 tests**.
- **Objective**: Stress each feature against boundary limits, mathematical singularities (division by zero relative speed, zero ground speed, negative rudder, 1,800 circular buffer wraps, QR schema truncation, IALA region swaps, fog opacity thresholds, extreme wind leeway).

### Tier 3: Cross-Feature System Combinations
- **Scope**: **20 multi-subsystem interaction tests**.
- **Objective**: Validate interplay between interconnected features:
  1. TSS lane keeping in dense fog with Rule 35 sound signals and ARPA tracking.
  2. Multi-vessel 5-ship encounter under wind leeway and current drift recorded in 1Hz VDR.
  3. Instructor Studio exported compact QR scenario loaded into 3D scene and WebXR cockpit rig.
  4. VDR replay scrub synchronized with 2D radar echoes, CPA time graph, and PDF Certificate export.
  5. Rule 9 narrow channel overtaking whistle exchange with synchronized masthead light flash and LMS score penalty for early turn.

### Tier 4: Real-World Operational Scenarios
- **Scope**: **10 complex end-to-end maritime scenarios**.
- **Objective**: Validate realistic multi-faceted navigation passages:
  1. Dover Strait TSS crossing at right angles under tidal stream.
  2. Singapore Strait narrow channel overtaking with opposing container ship.
  3. Van Don coastal archipelago in restricted visibility (dense fog) with fishing flotilla.
  4. Malacca Strait congested night transit with Not Under Command (NUC) vessel.
  5. English Channel blind bend approach in narrow channel with horn sound warning.
  6. STCW Regulation II/1 Officer of the Watch (OOW) practical certification examination.
  7. High-speed container ship avoidance in restricted visibility with Rule 19 radar plotting.
  8. Shallow bank narrow channel navigation respecting IALA Region A lateral marks.
  9. Combined Current Drift and Wind Leeway compensation in Traffic Separation Scheme.
  10. Full instructor-to-candidate pipeline: Authoring -> QR Scan -> Simulation -> VDR Black Box -> Client-Side PDF Certificate.

**Total Target Test Count**: $\ge 230$ tests (Actual: **230 automated test cases**).

---

## 3. 20-Feature Traceability Matrix

| Feature ID | Feature Name | Tier 1 (Iso) | Tier 2 (Edge) | Tier 3 (Cross) | Tier 4 (Scenario) | Total Tests |
|:---|:---|:---:|:---:|:---:|:---:|:---:|
| **F1.1** | Multi-Target Engine (3-5 Ships) | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F1.2** | Rule 9 Narrow Channel | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F1.3** | Rule 10 TSS Schemes | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F1.4** | IALA Buoyage (Regions A & B) | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F1.5** | 3D Fog & Restricted Visibility | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F1.6** | Leeway & Current Drift Physics | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F2.1** | Procedural Spatial Audio Engine | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F2.2** | Rule 34 Maneuver Sound Signals | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F2.3** | Rule 35 Fog Sound Timer | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F2.4** | Masthead Light Synchronization | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F3.1** | 1Hz VDR Telemetry Circular Buffer | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F3.2** | VDR Replay & CPA Time Graph | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F3.3** | Client-Side PDF Certificate Export | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F4.1** | Instructor Studio Scenario Designer| 5 | 5 | Yes | Yes | $\ge 10$ |
| **F4.2** | Compact QR / JSON / PIN Engine | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F4.3** | Offline LMS Leaderboard & Quiz | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F5.1** | WebXR VR Cockpit Rig | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F5.2** | Mobile Gyroscope 360° Tracking | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F6.1** | 100% Offline Asset Suite | 5 | 5 | Yes | Yes | $\ge 10$ |
| **F6.2** | Capacitor 6.2.0 & Android Sync | 5 | 5 | Yes | Yes | $\ge 10$ |
| **Cross** | Cross-Feature Interactions | - | - | 20 | - | 20 |
| **E2E** | Operational Scenarios | - | - | - | 10 | 10 |
| **TOTAL** | | **100** | **100** | **20** | **10** | **230** |

---

## 4. Test Suite Architecture & Directory Layout

```
d:/marine/
├── TEST_INFRA.md                   # This document
├── TEST_READY.md                   # Final readiness declaration
├── test_marine_colregs.py          # Unified root CLI test script
└── tests/
    ├── __init__.py                 # Test package initialization
    ├── maritime_models.py          # Ground-truth mathematical & specification oracles
    ├── test_tier1_features.py      # Tier 1: 100 feature coverage test cases
    ├── test_tier2_boundaries.py    # Tier 2: 100 boundary & corner test cases
    ├── test_tier3_combinations.py  # Tier 3: 20 cross-feature combination test cases
    ├── test_tier4_scenarios.py     # Tier 4: 10 real-world operational scenarios
    ├── test_colregs_e2e.py         # Complete aggregate test suite
    └── run_all_tests.py            # Standalone test runner with rich terminal reporting
```

---

## 5. Execution Guide

### Option 1: Dedicated Custom Test Runner (Recommended)
```bash
python tests/run_all_tests.py
```
Outputs colored, structured progress for Tiers 1-4, test execution metrics, and exits with code 0 on success.

### Option 2: Standard Python Unittest Discovery
```bash
python -m unittest discover tests -p "test_*.py" -v
```

### Option 3: Unified Root Runner
```bash
python test_marine_colregs.py
```
Runs legacy mathematical verification alongside all 230 tests across Tiers 1-4.
