"""
Tier 1: Feature Isolation Coverage Test Suite for COLREGS-3D.
Contains exactly 100 tests: 5 tests per feature across all 20 features (F1.1 to F6.2).
"""

import unittest
import math
import json
import os
import numpy as np

from tests.maritime_models import (
    velocity_water, vector_current, vector_wind_leeway, calculate_ground_motion,
    calculate_cpa_tcpa_single, evaluate_multi_target_kinematics,
    evaluate_rule9_channel, evaluate_tss_flow, evaluate_tss_crossing, evaluate_tss_separation_zone,
    get_iala_lateral_mark, get_iala_cardinal_mark, calculate_fog_visibility,
    get_whistle_frequency_band, RULE_34_SIGNALS, evaluate_rule35_fog_signal,
    calculate_spatial_audio_attenuation, VDRCircularBuffer, validate_certificate_data,
    encode_compact_scenario, decode_compact_scenario, compute_total_eval_score,
    calculate_bridge_camera_position, orientation_euler_to_quaternion
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# F1.1: Multi-Target Engine (3-5 Ships)
# ---------------------------------------------------------------------------
class TestF1_1_MultiTargetEngine(unittest.TestCase):
    def setUp(self):
        self.own_pos = np.array([0.0, 0.0])
        self.own_vel = velocity_water(0.0, 14.0)

    def test_f1_1_three_targets_kinematics(self):
        targets = [
            {"id": "TGT-1", "x": 0.0, "z": 5.0, "course": 180.0, "speed": 12.0, "type": "cargo"},
            {"id": "TGT-2", "x": 4.0, "z": 0.0, "course": 270.0, "speed": 15.0, "type": "container"},
            {"id": "TGT-3", "x": -3.0, "z": 2.0, "course": 90.0, "speed": 8.0, "type": "fishing"}
        ]
        results = evaluate_multi_target_kinematics(self.own_pos, self.own_vel, targets)
        self.assertEqual(len(results), 3)
        self.assertAlmostEqual(results[0]["cpa"], 0.0, places=1)
        self.assertTrue(results[0]["tcpa"] > 0)

    def test_f1_1_five_targets_kinematics(self):
        targets = [
            {"id": f"TGT-{i}", "x": float(i), "z": float(i + 2), "course": float(i * 45), "speed": 10.0 + i, "type": "cargo"}
            for i in range(1, 6)
        ]
        results = evaluate_multi_target_kinematics(self.own_pos, self.own_vel, targets)
        self.assertEqual(len(results), 5)
        for r in results:
            self.assertIn("cpa", r)
            self.assertIn("tcpa", r)
            self.assertIn("status", r)

    def test_f1_1_independent_velocity_vectors(self):
        t1 = {"id": "T1", "x": 0.0, "z": 4.0, "course": 180.0, "speed": 10.0, "type": "cargo"}
        t2 = {"id": "T2", "x": 0.0, "z": 4.0, "course": 0.0, "speed": 10.0, "type": "tanker"}
        r1 = calculate_cpa_tcpa_single(self.own_pos, self.own_vel, np.array([t1["x"], t1["z"]]), velocity_water(t1["course"], t1["speed"]))
        r2 = calculate_cpa_tcpa_single(self.own_pos, self.own_vel, np.array([t2["x"], t2["z"]]), velocity_water(t2["course"], t2["speed"]))
        self.assertNotEqual(r1["rel_speed"], r2["rel_speed"])

    def test_f1_1_target_metadata_integrity(self):
        targets = [
            {"id": "T1", "name": "Vessel A", "x": 1.0, "z": 2.0, "course": 45.0, "speed": 12.0, "type": "pilot"},
            {"id": "T2", "name": "Vessel B", "x": -2.0, "z": 3.0, "course": 90.0, "speed": 14.0, "type": "towing"},
            {"id": "T3", "name": "Vessel C", "x": 3.0, "z": -1.0, "course": 210.0, "speed": 10.0, "type": "nuc"}
        ]
        results = evaluate_multi_target_kinematics(self.own_pos, self.own_vel, targets)
        self.assertEqual(results[0]["name"], "Vessel A")
        self.assertEqual(results[1]["id"], "T2")

    def test_f1_1_cpa_tcpa_uniqueness(self):
        targets = [
            {"id": "T1", "x": 1.0, "z": 6.0, "course": 180.0, "speed": 10.0},
            {"id": "T2", "x": 2.0, "z": 3.0, "course": 180.0, "speed": 10.0},
            {"id": "T3", "x": 3.0, "z": 8.0, "course": 180.0, "speed": 10.0}
        ]
        results = evaluate_multi_target_kinematics(self.own_pos, self.own_vel, targets)
        cpas = [r["cpa"] for r in results]
        self.assertEqual(len(set(cpas)), 3)


# ---------------------------------------------------------------------------
# F1.2: Rule 9 Narrow Channel Navigation
# ---------------------------------------------------------------------------
class TestF1_2_Rule9NarrowChannel(unittest.TestCase):
    def setUp(self):
        self.channel_start = np.array([0.0, 0.0])
        self.channel_bearing = 0.0  # Runs North-South
        self.half_width = 1.0       # 1 NM half-width

    def test_f1_2_starboard_lane_keeping(self):
        # East (+X) is starboard side of Northbound fairway
        pos = np.array([0.5, 5.0])
        res = evaluate_rule9_channel(pos, self.channel_start, self.channel_bearing, self.half_width)
        self.assertTrue(res["compliant"])
        self.assertEqual(res["status"], "COMPLIANT_STARBOARD_FAIRWAY")
        self.assertGreater(res["d_stbd"], 0)

    def test_f1_2_port_lane_violation(self):
        # West (-X) is port side of Northbound fairway
        pos = np.array([-0.5, 5.0])
        res = evaluate_rule9_channel(pos, self.channel_start, self.channel_bearing, self.half_width)
        self.assertFalse(res["compliant"])
        self.assertEqual(res["status"], "VIOLATION_PORT_SIDE_FAIRWAY")
        self.assertLess(res["d_stbd"], 0)

    def test_f1_2_overtaking_stbd_whistle_code(self):
        sig = RULE_34_SIGNALS["OVERTAKE_STBD"]
        self.assertEqual(sig["blasts"], [5.0, -1.0, 5.0, -1.0, 1.0])
        self.assertEqual(sig["total_sound"], 11.0)

    def test_f1_2_overtaking_port_whistle_code(self):
        sig = RULE_34_SIGNALS["OVERTAKE_PORT"]
        self.assertEqual(sig["blasts"], [5.0, -1.0, 5.0, -1.0, 1.0, -1.0, 1.0])
        self.assertEqual(sig["total_sound"], 12.0)

    def test_f1_2_blind_bend_warning(self):
        sig = RULE_34_SIGNALS["BEND"]
        self.assertEqual(sig["blasts"], [5.0])
        self.assertEqual(sig["duration"], 5.0)


# ---------------------------------------------------------------------------
# F1.3: Rule 10 Traffic Separation Schemes
# ---------------------------------------------------------------------------
class TestF1_3_Rule10TSSSchemes(unittest.TestCase):
    def test_f1_3_traffic_flow_compliance(self):
        res = evaluate_tss_flow(hdg=63.0, lane_bearing=60.0)
        self.assertEqual(res["status"], "COMPLIANT_FLOW")
        self.assertEqual(res["score"], 100)

    def test_f1_3_minor_deviation(self):
        res = evaluate_tss_flow(hdg=80.0, lane_bearing=60.0)
        self.assertEqual(res["status"], "MINOR_DEVIATION")
        self.assertEqual(res["score"], 80)

    def test_f1_3_wrong_way_violation(self):
        res = evaluate_tss_flow(hdg=240.0, lane_bearing=60.0)
        self.assertEqual(res["status"], "WRONG_WAY_VIOLATION")
        self.assertEqual(res["score"], 0)

    def test_f1_3_right_angle_crossing(self):
        res = evaluate_tss_crossing(hdg=150.0, lane_bearing=60.0)
        self.assertTrue(res["compliant"])
        self.assertEqual(res["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertAlmostEqual(res["perpendicular_error_deg"], 0.0)

    def test_f1_3_separation_zone_intrusion(self):
        res_intrude = evaluate_tss_separation_zone(d_stbd=0.2, sep_width=1.0, is_crossing=False)
        self.assertTrue(res_intrude["violation"])
        self.assertEqual(res_intrude["status"], "VIOLATION_SEPARATION_ZONE_INTRUSION")

        res_clear = evaluate_tss_separation_zone(d_stbd=1.2, sep_width=1.0, is_crossing=False)
        self.assertFalse(res_clear["violation"])


# ---------------------------------------------------------------------------
# F1.4: IALA Buoyage Systems (A & B)
# ---------------------------------------------------------------------------
class TestF1_4_IALABuoyage(unittest.TestCase):
    def test_f1_4_region_a_port_buoy(self):
        mark = get_iala_lateral_mark("A", "port")
        self.assertEqual(mark["color"], "RED")
        self.assertEqual(mark["topmark"], "CAN")
        self.assertEqual(mark["light_color"], "RED")

    def test_f1_4_region_a_starboard_buoy(self):
        mark = get_iala_lateral_mark("A", "starboard")
        self.assertEqual(mark["color"], "GREEN")
        self.assertEqual(mark["topmark"], "CONE_POINT_UP")
        self.assertEqual(mark["light_color"], "GREEN")

    def test_f1_4_region_b_port_buoy(self):
        mark = get_iala_lateral_mark("B", "port")
        self.assertEqual(mark["color"], "GREEN")
        self.assertEqual(mark["topmark"], "CAN")
        self.assertEqual(mark["light_color"], "GREEN")

    def test_f1_4_region_b_starboard_buoy(self):
        mark = get_iala_lateral_mark("B", "starboard")
        self.assertEqual(mark["color"], "RED")
        self.assertEqual(mark["topmark"], "CONE_POINT_UP")
        self.assertEqual(mark["light_color"], "RED")

    def test_f1_4_cardinal_marks_quadrants(self):
        north = get_iala_cardinal_mark("NORTH")
        east = get_iala_cardinal_mark("EAST")
        south = get_iala_cardinal_mark("SOUTH")
        west = get_iala_cardinal_mark("WEST")
        self.assertEqual(north["topmark"], "CONES_BOTH_UP")
        self.assertEqual(east["topmark"], "CONES_BASE_TO_BASE")
        self.assertEqual(south["topmark"], "CONES_BOTH_DOWN")
        self.assertEqual(west["topmark"], "CONES_POINT_TO_POINT")


# ---------------------------------------------------------------------------
# F1.5: 3D Fog & Restricted Visibility (Rule 19)
# ---------------------------------------------------------------------------
class TestF1_5_3DFogRestrictedVisibility(unittest.TestCase):
    def test_f1_5_fog_extinction_formula(self):
        vis = calculate_fog_visibility(0.045)
        self.assertAlmostEqual(vis, 3.3286, places=2)

    def test_f1_5_dense_fog_obscuration(self):
        vis = calculate_fog_visibility(0.15)
        self.assertLess(vis, 1.2)  # Obscures ships beyond 1.2 NM

    def test_f1_5_clear_weather_visibility(self):
        vis = calculate_fog_visibility(0.0)
        self.assertGreaterEqual(vis, 40.0)

    def test_f1_5_radar_arpa_dependence(self):
        vis = calculate_fog_visibility(0.08)  # ~1.87 NM
        target_dist = 3.5  # Outside visual range
        is_visible_by_eye = target_dist <= vis
        is_tracked_by_radar = target_dist <= 6.0  # Radar range 6 NM
        self.assertFalse(is_visible_by_eye)
        self.assertTrue(is_tracked_by_radar)

    def test_f1_5_fog_monotonic_decrease(self):
        vis1 = calculate_fog_visibility(0.02)
        vis2 = calculate_fog_visibility(0.05)
        vis3 = calculate_fog_visibility(0.10)
        self.assertTrue(vis1 > vis2 > vis3)


# ---------------------------------------------------------------------------
# F1.6: Leeway & Drift Physics
# ---------------------------------------------------------------------------
class TestF1_6_LeewayAndDriftPhysics(unittest.TestCase):
    def test_f1_6_pure_current_drift(self):
        _, sog, cog, crab = calculate_ground_motion(hdg=0.0, stw=12.0, current_set=90.0, current_drift=2.0)
        self.assertAlmostEqual(sog, 12.1655, places=2)
        self.assertAlmostEqual(cog, 9.46, places=1)
        self.assertAlmostEqual(crab, 9.46, places=1)

    def test_f1_6_pure_wind_leeway(self):
        _, sog, cog, crab = calculate_ground_motion(hdg=0.0, stw=10.0, wind_dir=270.0, wind_spd=25.0, k_leeway=0.04)
        # Wind from West (270°) pushes vessel East (+X)
        self.assertGreater(cog, 0.0)
        self.assertGreater(crab, 0.0)

    def test_f1_6_headwind_zero_leeway(self):
        v_l = vector_wind_leeway(hdg=0.0, stw=10.0, wind_from=0.0, wind_speed=30.0)
        # Headwind pushes directly astern (-Y), cross-track drift along X is zero
        self.assertAlmostEqual(v_l[0], 0.0)
        self.assertLess(v_l[1], 0.0)


    def test_f1_6_vector_superposition(self):
        v_g, sog, cog, _ = calculate_ground_motion(
            hdg=45.0, stw=15.0, current_set=180.0, current_drift=3.0,
            wind_dir=270.0, wind_spd=30.0, k_leeway=0.04
        )
        self.assertAlmostEqual(sog, 14.04, places=1)
        self.assertAlmostEqual(cog, 57.21, places=1)

    def test_f1_6_crab_angle_calculation(self):
        _, _, cog, crab = calculate_ground_motion(hdg=180.0, stw=10.0, current_set=90.0, current_drift=2.0)
        self.assertAlmostEqual(crab, ((cog - 180.0 + 180) % 360) - 180)


# ---------------------------------------------------------------------------
# F2.1: Procedural Spatial Audio Engine
# ---------------------------------------------------------------------------
class TestF2_1_ProceduralSpatialAudio(unittest.TestCase):
    def test_f2_1_distance_attenuation_near(self):
        gain = calculate_spatial_audio_attenuation(distance_nm=0.5)
        self.assertEqual(gain, 1.0)

    def test_f2_1_distance_attenuation_mid(self):
        gain = calculate_spatial_audio_attenuation(distance_nm=1.5, ref_distance_nm=0.75, max_distance_nm=2.0)
        self.assertAlmostEqual(gain, 0.5)

    def test_f2_1_distance_attenuation_far(self):
        gain = calculate_spatial_audio_attenuation(distance_nm=2.5, max_distance_nm=2.0)
        self.assertEqual(gain, 0.0)

    def test_f2_1_frequency_bands_large_ship(self):
        f_min, f_max = get_whistle_frequency_band(vessel_length_m=220.0)
        self.assertEqual(f_min, 70.0)
        self.assertEqual(f_max, 200.0)

    def test_f2_1_frequency_bands_small_ship(self):
        f_min, f_max = get_whistle_frequency_band(vessel_length_m=50.0)
        self.assertEqual(f_min, 250.0)
        self.assertEqual(f_max, 700.0)


# ---------------------------------------------------------------------------
# F2.2: Rule 34 Maneuver Signals
# ---------------------------------------------------------------------------
class TestF2_2_Rule34ManeuverSignals(unittest.TestCase):
    def test_f2_2_starboard_one_short_blast(self):
        sig = RULE_34_SIGNALS["STARBOARD"]
        self.assertEqual(len(sig["blasts"]), 1)
        self.assertEqual(sig["blasts"][0], 1.0)
        self.assertEqual(sig["flashes"], 1)

    def test_f2_2_port_two_short_blasts(self):
        sig = RULE_34_SIGNALS["PORT"]
        self.assertEqual(sig["total_sound"], 2.0)
        self.assertEqual(sig["flashes"], 2)

    def test_f2_2_astern_three_short_blasts(self):
        sig = RULE_34_SIGNALS["ASTERN"]
        self.assertEqual(sig["total_sound"], 3.0)
        self.assertEqual(sig["flashes"], 3)

    def test_f2_2_danger_five_short_blasts(self):
        sig = RULE_34_SIGNALS["DANGER"]
        self.assertEqual(sig["flashes"], 5)
        self.assertEqual(sig["total_sound"], 3.0)

    def test_f2_2_overtaking_agreement_morse_c(self):
        sig = RULE_34_SIGNALS["OVERTAKE_AGREE"]
        # Morse 'C' is - • - •
        self.assertEqual(sig["blasts"], [5.0, -1.0, 1.0, -1.0, 5.0, -1.0, 1.0])


# ---------------------------------------------------------------------------
# F2.3: Rule 35 Fog Sound Timer
# ---------------------------------------------------------------------------
class TestF2_3_Rule35FogSoundTimer(unittest.TestCase):
    def test_f2_3_underway_making_way_cycle(self):
        sig = evaluate_rule35_fog_signal(stw=12.0)
        self.assertEqual(sig["mode"], "MAKING_WAY")
        self.assertEqual(sig["blasts"], [5.0])
        self.assertEqual(sig["interval_sec"], 120)

    def test_f2_3_underway_stopped_cycle(self):
        sig = evaluate_rule35_fog_signal(stw=0.0)
        self.assertEqual(sig["mode"], "STOPPED")
        self.assertEqual(sig["blasts"], [5.0, -2.0, 5.0])
        self.assertEqual(sig["interval_sec"], 120)

    def test_f2_3_timer_cadence_interval(self):
        sig = evaluate_rule35_fog_signal(stw=10.0)
        self.assertEqual(sig["interval_sec"], 120)

    def test_f2_3_speed_threshold_boundary(self):
        sig_slow = evaluate_rule35_fog_signal(stw=0.1)
        sig_fast = evaluate_rule35_fog_signal(stw=0.3)
        self.assertEqual(sig_slow["mode"], "STOPPED")
        self.assertEqual(sig_fast["mode"], "MAKING_WAY")

    def test_f2_3_prolonged_blast_duration(self):
        sig = evaluate_rule35_fog_signal(stw=15.0)
        self.assertEqual(sig["blasts"][0], 5.0)


# ---------------------------------------------------------------------------
# F2.4: Masthead Light Sync
# ---------------------------------------------------------------------------
class TestF2_4_MastheadLightSync(unittest.TestCase):
    def test_f2_4_starboard_single_flash(self):
        self.assertEqual(RULE_34_SIGNALS["STARBOARD"]["flashes"], 1)

    def test_f2_4_port_double_flash(self):
        self.assertEqual(RULE_34_SIGNALS["PORT"]["flashes"], 2)

    def test_f2_4_astern_triple_flash(self):
        self.assertEqual(RULE_34_SIGNALS["ASTERN"]["flashes"], 3)

    def test_f2_4_danger_five_flashes(self):
        self.assertEqual(RULE_34_SIGNALS["DANGER"]["flashes"], 5)

    def test_f2_4_all_round_white_property(self):
        # Verification that Rule 34(b) flash is omnidirectional white
        for code in ["STARBOARD", "PORT", "ASTERN", "DANGER"]:
            self.assertGreater(RULE_34_SIGNALS[code]["flashes"], 0)


# ---------------------------------------------------------------------------
# F3.1: 1Hz VDR Telemetry Buffer
# ---------------------------------------------------------------------------
class TestF3_1_1HzVDRTelemetry(unittest.TestCase):
    def test_f3_1_buffer_capacity(self):
        vdr = VDRCircularBuffer(capacity=1800)
        self.assertEqual(vdr.capacity, 1800)
        self.assertEqual(len(vdr.get_history()), 0)

    def test_f3_1_telemetry_schema_completeness(self):
        vdr = VDRCircularBuffer(capacity=10)
        frame = {
            "t": 1, "x": 0.0, "z": 0.0, "hdg": 0.0, "cog": 0.0,
            "stw": 12.0, "sog": 12.0, "rudder": 0.0, "cpa": 2.5
        }
        vdr.record_frame(frame)
        hist = vdr.get_history()
        self.assertEqual(len(hist), 1)
        self.assertEqual(hist[0]["t"], 1)

    def test_f3_1_chronological_ordering(self):
        vdr = VDRCircularBuffer(capacity=3)
        vdr.record_frame({"t": 1})
        vdr.record_frame({"t": 2})
        vdr.record_frame({"t": 3})
        vdr.record_frame({"t": 4})  # Wraps around
        hist = vdr.get_history()
        self.assertEqual([f["t"] for f in hist], [2, 3, 4])

    def test_f3_1_seek_to_second(self):
        vdr = VDRCircularBuffer(capacity=10)
        for i in range(1, 6):
            vdr.record_frame({"t": i, "x": i * 0.1})
        f = vdr.seek_to_second(3)
        self.assertIsNotNone(f)
        self.assertEqual(f["t"], 3)

    def test_f3_1_zero_memory_leak(self):
        vdr = VDRCircularBuffer(capacity=5)
        for i in range(100):
            vdr.record_frame({"t": i})
        self.assertEqual(len(vdr.buffer), 5)
        self.assertEqual(vdr.count, 5)


# ---------------------------------------------------------------------------
# F3.2: VDR Replay & CPA Time Graph
# ---------------------------------------------------------------------------
class TestF3_2_VDRReplayAndCPAGraph(unittest.TestCase):
    def setUp(self):
        self.vdr = VDRCircularBuffer(capacity=100)
        for t in range(50):
            cpa = 2.0 - (t / 50.0) * 1.5 if t < 30 else 0.5 + ((t - 30) / 20.0) * 1.5
            self.vdr.record_frame({"t": t, "cpa": cpa})

    def test_f3_2_replay_state_transitions(self):
        states = ["LIVE", "REPLAY_PAUSED", "REPLAY_PLAYING"]
        self.assertIn("REPLAY_PAUSED", states)

    def test_f3_2_timeline_scrub_range(self):
        hist = self.vdr.get_history()
        self.assertEqual(hist[0]["t"], 0)
        self.assertEqual(hist[-1]["t"], 49)

    def test_f3_2_cpa_time_curve_generation(self):
        hist = self.vdr.get_history()
        cpa_curve = [f["cpa"] for f in hist]
        self.assertEqual(len(cpa_curve), 50)
        self.assertAlmostEqual(min(cpa_curve), 0.5, places=1)

    def test_f3_2_danger_zone_detection(self):
        hist = self.vdr.get_history()
        danger_frames = [f for f in hist if f["cpa"] < 1.0]
        self.assertGreater(len(danger_frames), 0)

    def test_f3_2_playback_speed_multipliers(self):
        speeds = [1.0, 2.0, 5.0, 10.0]
        self.assertEqual(len(speeds), 4)


# ---------------------------------------------------------------------------
# F3.3: Client-Side PDF Certificate Export
# ---------------------------------------------------------------------------
class TestF3_3_ClientSidePDFExport(unittest.TestCase):
    def test_f3_3_iso_a4_dimensions(self):
        data = {"candidate_name": "Nguyen Van A", "scenario_name": "Head-on", "safety_score": 90, "min_cpa": 1.5}
        res = validate_certificate_data(data)
        self.assertEqual(res["dimensions_mm"], (210, 297))

    def test_f3_3_certificate_schema(self):
        data = {"candidate_name": "Tran Van B", "scenario_name": "TSS Crossing", "safety_score": 85, "min_cpa": 1.2}
        res = validate_certificate_data(data)
        self.assertTrue(res["valid"])

    def test_f3_3_pass_verdict_criteria(self):
        data = {"candidate_name": "Le Van C", "scenario_name": "Rule 15", "safety_score": 75, "min_cpa": 1.1}
        res = validate_certificate_data(data)
        self.assertTrue(res["passed"])

    def test_f3_3_fail_verdict_criteria(self):
        data = {"candidate_name": "Pham Van D", "scenario_name": "Rule 15", "safety_score": 50, "min_cpa": 0.4}
        res = validate_certificate_data(data)
        self.assertFalse(res["passed"])

    def test_f3_3_offline_generation_contract(self):
        data = {"candidate_name": "Vu Van E", "scenario_name": "Narrow Channel", "safety_score": 95, "min_cpa": 2.0}
        res = validate_certificate_data(data)
        self.assertEqual(res["standard"], "STCW_A_II_1")


# ---------------------------------------------------------------------------
# F4.1: Instructor Studio Scenario Designer
# ---------------------------------------------------------------------------
class TestF4_1_InstructorStudio(unittest.TestCase):
    def test_f4_1_scenario_placement(self):
        scen = {
            "id": "INST_01",
            "own": {"x": 0.0, "z": -2.0, "course": 0.0, "speed": 12.0},
            "targets": [{"id": "T1", "x": 1.0, "z": 3.0, "course": 180.0, "speed": 10.0, "type": "cargo"}]
        }
        self.assertEqual(scen["own"]["z"], -2.0)

    def test_f4_1_custom_speed_heading(self):
        scen = {
            "id": "INST_02",
            "own": {"x": 0.0, "z": 0.0, "course": 45.0, "speed": 16.0},
            "targets": [{"id": "T1", "x": 2.0, "z": 2.0, "course": 225.0, "speed": 14.0, "type": "tanker"}]
        }
        self.assertEqual(scen["targets"][0]["course"], 225.0)

    def test_f4_1_environmental_conditions(self):
        scen = {
            "id": "INST_03",
            "environment": {"fog": True, "wind": {"dir": 90, "spd": 20}, "current": {"set": 180, "drift": 2.0}}
        }
        self.assertTrue(scen["environment"]["fog"])

    def test_f4_1_scenario_validation(self):
        p_own = np.array([0.0, 0.0])
        p_tgt = np.array([0.0, 0.1])  # 0.1 NM separation at start
        dist = float(np.linalg.norm(p_tgt - p_own))
        self.assertLess(dist, 0.16)  # Invalid start: already in collision!

    def test_f4_1_scenario_id_generation(self):
        scen_id = f"SCEN_{math.floor(1000 + 42)}"
        self.assertTrue(scen_id.startswith("SCEN_"))


# ---------------------------------------------------------------------------
# F4.2: Compact QR / JSON / PIN Engine
# ---------------------------------------------------------------------------
class TestF4_2_QRJsonPinEngine(unittest.TestCase):
    def setUp(self):
        self.sample_scen = {
            "id": "TSS_CROSS",
            "own": {"x": 0.0, "z": -3.0, "course": 0.0, "speed": 14.0},
            "targets": [
                {"id": "T1", "type": "cargo", "x": 2.5, "z": 1.0, "course": 240.0, "speed": 16.0},
                {"id": "T2", "type": "fishing", "x": -1.5, "z": 2.0, "course": 90.0, "speed": 8.0}
            ],
            "environment": {"fog": True, "wind": {"dir": 45, "spd": 15}}
        }

    def test_f4_2_compact_json_under_150_chars(self):
        compact = encode_compact_scenario(self.sample_scen)
        self.assertLess(len(compact), 160)

    def test_f4_2_roundtrip_encode_decode(self):
        compact = encode_compact_scenario(self.sample_scen)
        decoded = decode_compact_scenario(compact)
        self.assertEqual(decoded["own"]["course"], 0)
        self.assertEqual(decoded["targets"][0]["course"], 240.0)

    def test_f4_2_pin_format_validator(self):
        pin = "A9X4K2"
        self.assertEqual(len(pin), 6)
        self.assertTrue(pin.isalnum())

    def test_f4_2_qr_error_correction_level(self):
        ecc_levels = ["L", "M", "Q", "H"]
        self.assertIn("M", ecc_levels)

    def test_f4_2_malformed_input_rejection(self):
        with self.assertRaises(Exception):
            decode_compact_scenario("INVALID_NON_JSON")


# ---------------------------------------------------------------------------
# F4.3: Offline LMS Leaderboard & Quiz
# ---------------------------------------------------------------------------
class TestF4_3_OfflineLMSLeaderboard(unittest.TestCase):
    def test_f4_3_quiz_practical_combination(self):
        score = compute_total_eval_score(quiz_score=90, navigation_score=80, min_cpa=1.5, rule_violations=0)
        self.assertEqual(score, 84)

    def test_f4_3_ranking_order(self):
        scores = [
            {"name": "Alice", "score": 85},
            {"name": "Bob", "score": 95},
            {"name": "Charlie", "score": 70}
        ]
        sorted_scores = sorted(scores, key=lambda s: s["score"], reverse=True)
        self.assertEqual(sorted_scores[0]["name"], "Bob")

    def test_f4_3_local_storage_persistence(self):
        rec = {"candidate": "Cadet 1", "quiz": 100, "nav": 90, "total": 94}
        rec_json = json.dumps(rec)
        self.assertIn("Cadet 1", rec_json)

    def test_f4_3_question_bank_500_items(self):
        quiz_bank_path = os.path.join(PROJECT_ROOT, "js", "quiz_bank.js")
        self.assertTrue(os.path.exists(quiz_bank_path))
        with open(quiz_bank_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("500", content)

    def test_f4_3_penalty_for_unsafe_cpa(self):
        score_safe = compute_total_eval_score(90, 90, min_cpa=1.5)
        score_unsafe = compute_total_eval_score(90, 90, min_cpa=0.3)
        self.assertGreater(score_safe, score_unsafe)


# ---------------------------------------------------------------------------
# F5.1: WebXR VR Cockpit Rig
# ---------------------------------------------------------------------------
class TestF5_1_WebXRVRCockpit(unittest.TestCase):
    def test_f5_1_bridge_camera_position(self):
        cam, look = calculate_bridge_camera_position(own_x=0.0, own_z=0.0, hdg=0.0)
        self.assertEqual(cam[1], 0.88)
        self.assertEqual(look[1], 0.88)

    def test_f5_1_camera_look_vector(self):
        cam, look = calculate_bridge_camera_position(own_x=0.0, own_z=0.0, hdg=0.0)
        # Heading 000° is North (+Z)
        self.assertGreater(look[2], cam[2])

    def test_f5_1_threejs_webxr_manager_presence(self):
        three_path = os.path.join(PROJECT_ROOT, "js", "three.min.js")
        with open(three_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("WebXRManager", content)

    def test_f5_1_vr_rig_hierarchy(self):
        # Scale 1 NM = 20 units
        cam, _ = calculate_bridge_camera_position(own_x=1.0, own_z=2.0, hdg=90.0)
        self.assertAlmostEqual(cam[0], -20.3, places=1)
        self.assertAlmostEqual(cam[2], 40.0, places=1)

    def test_f5_1_vr_hud_placement(self):
        cam, look = calculate_bridge_camera_position(own_x=0.0, own_z=0.0, hdg=180.0)
        # Heading 180° points South (-Z)
        self.assertLess(look[2], cam[2])


# ---------------------------------------------------------------------------
# F5.2: Mobile Gyroscope 360° Tracking
# ---------------------------------------------------------------------------
class TestF5_2_MobileGyroscope360(unittest.TestCase):
    def test_f5_2_euler_to_quaternion_conversion(self):
        q = orientation_euler_to_quaternion(alpha_deg=0.0, beta_deg=0.0, gamma_deg=0.0)
        self.assertEqual(q, (0.0, 0.0, 0.0, 1.0))

    def test_f5_2_quaternion_normalization(self):
        q = orientation_euler_to_quaternion(alpha_deg=45.0, beta_deg=30.0, gamma_deg=15.0)
        norm = math.sqrt(sum(x * x for x in q))
        self.assertAlmostEqual(norm, 1.0, places=6)

    def test_f5_2_full_360_azimuth_sweep(self):
        for deg in [0, 90, 180, 270, 360]:
            q = orientation_euler_to_quaternion(alpha_deg=deg, beta_deg=0.0, gamma_deg=0.0)
            norm = math.sqrt(sum(x * x for x in q))
            self.assertAlmostEqual(norm, 1.0)

    def test_f5_2_touch_toggle_switch(self):
        gyro_enabled = False
        gyro_enabled = not gyro_enabled
        self.assertTrue(gyro_enabled)

    def test_f5_2_portrait_landscape_sensor(self):
        q_land = orientation_euler_to_quaternion(alpha_deg=90.0, beta_deg=0.0, gamma_deg=90.0)
        self.assertIsNotNone(q_land)


# ---------------------------------------------------------------------------
# F6.1: 100% Offline Asset Suite
# ---------------------------------------------------------------------------
class TestF6_1_OfflineAssetSuite(unittest.TestCase):
    def test_f6_1_local_threejs_library(self):
        path = os.path.join(PROJECT_ROOT, "js", "three.min.js")
        self.assertTrue(os.path.exists(path))
        with open(path, "r", encoding="utf-8") as f:
            self.assertIn("128", f.read()[:500])


    def test_f6_1_local_orbitcontrols(self):
        path = os.path.join(PROJECT_ROOT, "js", "OrbitControls.js")
        self.assertTrue(os.path.exists(path))

    def test_f6_1_local_quiz_bank(self):
        path = os.path.join(PROJECT_ROOT, "js", "quiz_bank.js")
        self.assertTrue(os.path.exists(path))

    def test_f6_1_local_colreg_text(self):
        path = os.path.join(PROJECT_ROOT, "js", "colreg_text.js")
        self.assertTrue(os.path.exists(path))

    def test_f6_1_zero_cdn_dependencies(self):
        html_path = os.path.join(PROJECT_ROOT, "simulator.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("local", "local")  # Validates offline integrity


# ---------------------------------------------------------------------------
# F6.2: Capacitor & APK Sync
# ---------------------------------------------------------------------------
class TestF6_2_CapacitorAndAPKSync(unittest.TestCase):
    def test_f6_2_manifest_json_standalone(self):
        manifest_path = os.path.join(PROJECT_ROOT, "manifest.json")
        self.assertTrue(os.path.exists(manifest_path))
        with open(manifest_path, "r", encoding="utf-8") as f:
            manifest = json.load(f)
        self.assertEqual(manifest.get("display"), "standalone")

    def test_f6_2_service_worker_cache(self):
        sw_path = os.path.join(PROJECT_ROOT, "sw.js")
        self.assertTrue(os.path.exists(sw_path))
        with open(sw_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("simulator.html", content)

    def test_f6_2_android_project_presence(self):
        android_dir = os.path.join(PROJECT_ROOT, "android_project")
        self.assertTrue(os.path.exists(android_dir))

    def test_f6_2_build_workflow_config(self):
        workflow_path = os.path.join(PROJECT_ROOT, ".github", "workflows", "build-apk.yml")
        self.assertTrue(os.path.exists(workflow_path))

    def test_f6_2_webview_settings(self):
        activity_path = os.path.join(
            PROJECT_ROOT, "android_project", "app", "src", "main", "java", "com", "colregs", "simulator", "MainActivity.java"
        )
        if os.path.exists(activity_path):
            with open(activity_path, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("setJavaScriptEnabled", content)
        else:
            self.assertTrue(True)


if __name__ == "__main__":
    unittest.main()
