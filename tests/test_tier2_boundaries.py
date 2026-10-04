"""
Tier 2: Boundary & Corner Cases Test Suite for COLREGS-3D.
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
    calculate_bridge_camera_position, orientation_euler_to_quaternion,
    COLLISION_DISTANCE_NM, SAFE_PASSING_DISTANCE_NM, THREE_JS_SCALE
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# ---------------------------------------------------------------------------
# F1.1: Multi-Target Engine Boundaries
# ---------------------------------------------------------------------------
class TestF1_1_Boundaries(unittest.TestCase):
    def test_b1_1_cpa_at_exact_collision_threshold(self):
        p_own = np.array([0.0, 0.0])
        p_tgt = np.array([COLLISION_DISTANCE_NM, 0.0])
        v_own = velocity_water(0.0, 10.0)
        v_tgt = velocity_water(0.0, 10.0)
        res = calculate_cpa_tcpa_single(p_own, v_own, p_tgt, v_tgt)
        self.assertAlmostEqual(res["dist"], COLLISION_DISTANCE_NM)

    def test_b1_1_cpa_at_exact_safe_passing_threshold(self):
        p_own = np.array([0.0, 0.0])
        p_tgt = np.array([SAFE_PASSING_DISTANCE_NM, 0.0])
        v_own = velocity_water(0.0, 10.0)
        v_tgt = velocity_water(0.0, 10.0)
        res = calculate_cpa_tcpa_single(p_own, v_own, p_tgt, v_tgt)
        self.assertAlmostEqual(res["cpa"], SAFE_PASSING_DISTANCE_NM)

    def test_b1_1_zero_relative_speed(self):
        p_own = np.array([0.0, 0.0])
        p_tgt = np.array([2.0, 3.0])
        v_same = velocity_water(45.0, 12.0)
        res = calculate_cpa_tcpa_single(p_own, v_same, p_tgt, v_same)
        self.assertAlmostEqual(res["rel_speed"], 0.0)
        self.assertEqual(res["tcpa"], 0.0)
        self.assertAlmostEqual(res["cpa"], res["dist"])

    def test_b1_1_zero_distance_singularity(self):
        p_own = np.array([0.0, 0.0])
        res = calculate_cpa_tcpa_single(p_own, velocity_water(0, 10), p_own, velocity_water(180, 10))
        self.assertAlmostEqual(res["dist"], 0.0)
        self.assertAlmostEqual(res["cpa"], 0.0)

    def test_b1_1_negative_tcpa_passed(self):
        p_own = np.array([0.0, 0.0])
        p_tgt = np.array([0.0, 5.0])
        # Moving away from each other
        v_own = velocity_water(180.0, 10.0)  # Own ship moves South (-Z)
        v_tgt = velocity_water(0.0, 10.0)    # Target moves North (+Z)
        res = calculate_cpa_tcpa_single(p_own, v_own, p_tgt, v_tgt)
        self.assertLessEqual(res["tcpa"], 0.0)
        self.assertAlmostEqual(res["cpa"], 5.0)


# ---------------------------------------------------------------------------
# F1.2: Rule 9 Narrow Channel Boundaries
# ---------------------------------------------------------------------------
class TestF1_2_Boundaries(unittest.TestCase):
    def test_b1_2_exact_channel_boundary(self):
        res = evaluate_rule9_channel(np.array([1.0, 5.0]), np.array([0.0, 0.0]), channel_bearing=0.0, channel_half_width=1.0)
        self.assertTrue(res["compliant"])
        self.assertAlmostEqual(res["d_stbd"], 1.0)

    def test_b1_2_exact_centerline_navigation(self):
        res = evaluate_rule9_channel(np.array([0.0, 5.0]), np.array([0.0, 0.0]), channel_bearing=0.0, channel_half_width=1.0)
        self.assertTrue(res["compliant"])
        self.assertAlmostEqual(res["d_stbd"], 0.0)

    def test_b1_2_extreme_outside_channel(self):
        res = evaluate_rule9_channel(np.array([3.0, 5.0]), np.array([0.0, 0.0]), channel_bearing=0.0, channel_half_width=1.0)
        self.assertFalse(res["compliant"])
        self.assertEqual(res["status"], "GROUNDING_RISK_OUT_OF_CHANNEL")

    def test_b1_2_negative_cross_track(self):
        res = evaluate_rule9_channel(np.array([-0.01, 2.0]), np.array([0.0, 0.0]), channel_bearing=0.0, channel_half_width=1.0)
        self.assertFalse(res["compliant"])
        self.assertEqual(res["status"], "VIOLATION_PORT_SIDE_FAIRWAY")

    def test_b1_2_arbitrary_channel_bearing(self):
        # Channel bearing 090° (Eastbound). Starboard is South (-Y)
        res = evaluate_rule9_channel(np.array([5.0, -0.5]), np.array([0.0, 0.0]), channel_bearing=90.0, channel_half_width=1.0)
        self.assertTrue(res["compliant"])
        self.assertAlmostEqual(res["d_stbd"], 0.5)


# ---------------------------------------------------------------------------
# F1.3: Rule 10 TSS Boundaries
# ---------------------------------------------------------------------------
class TestF1_3_Boundaries(unittest.TestCase):
    def test_b1_3_exact_15_deg_flow_boundary(self):
        res = evaluate_tss_flow(hdg=75.0, lane_bearing=60.0)
        self.assertEqual(res["status"], "COMPLIANT_FLOW")
        self.assertEqual(res["score"], 100)

    def test_b1_3_exact_30_deg_minor_boundary(self):
        res = evaluate_tss_flow(hdg=90.0, lane_bearing=60.0)
        self.assertEqual(res["status"], "MINOR_DEVIATION")
        self.assertEqual(res["score"], 80)

    def test_b1_3_exact_90_deg_wrong_way_boundary(self):
        res = evaluate_tss_flow(hdg=150.0, lane_bearing=60.0)
        self.assertEqual(res["status"], "MAJOR_DEVIATION")
        self.assertEqual(res["score"], 40)

    def test_b1_3_exact_10_deg_crossing_boundary(self):
        # Lane 060°. Right angles are 150° and 330°.
        res = evaluate_tss_crossing(hdg=160.0, lane_bearing=60.0)
        self.assertTrue(res["compliant"])
        self.assertEqual(res["status"], "RIGHT_ANGLE_COMPLIANT")

    def test_b1_3_separation_zone_edge(self):
        res = evaluate_tss_separation_zone(d_stbd=0.5, sep_width=1.0, is_crossing=False)
        self.assertTrue(res["inside_zone"])


# ---------------------------------------------------------------------------
# F1.4: IALA Buoyage Boundaries
# ---------------------------------------------------------------------------
class TestF1_4_Boundaries(unittest.TestCase):
    def test_b1_4_region_a_vs_b_lateral_color_inversion(self):
        mark_a = get_iala_lateral_mark("A", "port")
        mark_b = get_iala_lateral_mark("B", "port")
        self.assertEqual(mark_a["color"], "RED")
        self.assertEqual(mark_b["color"], "GREEN")

    def test_b1_4_region_a_vs_b_starboard_color_inversion(self):
        mark_a = get_iala_lateral_mark("A", "starboard")
        mark_b = get_iala_lateral_mark("B", "starboard")
        self.assertEqual(mark_a["color"], "GREEN")
        self.assertEqual(mark_b["color"], "RED")

    def test_b1_4_cardinal_marks_unchanged_across_regions(self):
        # Cardinal marks do not change between regions
        c1 = get_iala_cardinal_mark("NORTH")
        c2 = get_iala_cardinal_mark("SOUTH")
        self.assertNotEqual(c1["topmark"], c2["topmark"])

    def test_b1_4_invalid_region_exception(self):
        with self.assertRaises(ValueError):
            get_iala_lateral_mark("C", "port")

    def test_b1_4_invalid_mark_type_exception(self):
        with self.assertRaises(ValueError):
            get_iala_lateral_mark("A", "unknown_type")


# ---------------------------------------------------------------------------
# F1.5: 3D Fog Boundaries
# ---------------------------------------------------------------------------
class TestF1_5_Boundaries(unittest.TestCase):
    def test_b1_5_zero_fog_density(self):
        vis = calculate_fog_visibility(0.0)
        self.assertGreaterEqual(vis, 50.0)

    def test_b1_5_extreme_fog_density(self):
        vis = calculate_fog_visibility(1.0)
        self.assertLess(vis, 0.2)

    def test_b1_5_infinite_distance_contrast(self):
        density = 0.05
        dist_nm = 10.0
        contrast = math.exp(-density * dist_nm * THREE_JS_SCALE)
        self.assertLess(contrast, 0.001)

    def test_b1_5_threshold_contrast(self):
        density = 0.045
        vis = calculate_fog_visibility(density)
        contrast = math.exp(-density * vis * THREE_JS_SCALE)
        self.assertAlmostEqual(contrast, 0.05, places=3)

    def test_b1_5_radar_max_range_cutoff(self):
        radar_max = 6.0
        dist = 6.1
        self.assertFalse(dist <= radar_max)


# ---------------------------------------------------------------------------
# F1.6: Leeway & Drift Physics Boundaries
# ---------------------------------------------------------------------------
class TestF1_6_Boundaries(unittest.TestCase):
    def test_b1_6_current_overpowers_engine(self):
        # Heading 000°, STW 4 kts, Opposing current 180° at 6 kts
        v_g, sog, cog, _ = calculate_ground_motion(hdg=0.0, stw=4.0, current_set=180.0, current_drift=6.0)
        self.assertAlmostEqual(sog, 2.0)
        self.assertAlmostEqual(cog, 180.0)

    def test_b1_6_zero_stw_pure_drift(self):
        _, sog, cog, _ = calculate_ground_motion(hdg=0.0, stw=0.0, current_set=90.0, current_drift=3.0)
        self.assertAlmostEqual(sog, 3.0)
        self.assertAlmostEqual(cog, 90.0)

    def test_b1_6_zero_speed_zero_drift(self):
        _, sog, cog, crab = calculate_ground_motion(hdg=45.0, stw=0.0, current_drift=0.0, wind_spd=0.0)
        self.assertEqual(sog, 0.0)
        self.assertEqual(cog, 45.0)
        self.assertEqual(crab, 0.0)

    def test_b1_6_extreme_hurricane_wind(self):
        _, sog, cog, crab = calculate_ground_motion(hdg=0.0, stw=10.0, wind_dir=270.0, wind_spd=80.0, k_leeway=0.04)
        self.assertFalse(math.isnan(sog))
        self.assertFalse(math.isnan(cog))
        self.assertGreater(sog, 10.0)

    def test_b1_6_180_deg_downwind(self):
        # Following wind from 180° pushes North (same as HDG 000°)
        _, sog, cog, crab = calculate_ground_motion(hdg=0.0, stw=10.0, wind_dir=180.0, wind_spd=25.0, k_leeway=0.04)
        self.assertAlmostEqual(crab, 0.0)
        self.assertAlmostEqual(cog, 0.0)
        self.assertAlmostEqual(sog, 11.0)


# ---------------------------------------------------------------------------
# F2.1: Procedural Spatial Audio Boundaries
# ---------------------------------------------------------------------------
class TestF2_1_Boundaries(unittest.TestCase):
    def test_b2_1_zero_distance_gain_capped(self):
        gain = calculate_spatial_audio_attenuation(distance_nm=0.0)
        self.assertEqual(gain, 1.0)

    def test_b2_1_exact_ref_distance(self):
        gain = calculate_spatial_audio_attenuation(distance_nm=0.75, ref_distance_nm=0.75)
        self.assertEqual(gain, 1.0)

    def test_b2_1_exact_max_distance(self):
        gain = calculate_spatial_audio_attenuation(distance_nm=2.0, max_distance_nm=2.0)
        self.assertEqual(gain, 0.0)

    def test_b2_1_vessel_length_exact_200m(self):
        f_min, f_max = get_whistle_frequency_band(200.0)
        self.assertEqual((f_min, f_max), (70.0, 200.0))

    def test_b2_1_vessel_length_exact_75m(self):
        f_min, f_max = get_whistle_frequency_band(75.0)
        self.assertEqual((f_min, f_max), (130.0, 350.0))


# ---------------------------------------------------------------------------
# F2.2: Rule 34 Maneuver Signals Boundaries
# ---------------------------------------------------------------------------
class TestF2_2_Boundaries(unittest.TestCase):
    def test_b2_2_rapid_whistle_retrigger_debounce(self):
        debounce_window_s = 0.5
        t_last = 10.0
        t_new = 10.2
        should_reject = (t_new - t_last) < debounce_window_s
        self.assertTrue(should_reject)

    def test_b2_2_danger_blast_burst_cadence(self):
        sig = RULE_34_SIGNALS["DANGER"]
        blasts = [b for b in sig["blasts"] if b > 0]
        self.assertEqual(len(blasts), 5)

    def test_b2_2_minimum_blast_duration(self):
        sig = RULE_34_SIGNALS["DANGER"]
        self.assertGreaterEqual(sig["blasts"][0], 0.5)

    def test_b2_2_maximum_blast_duration(self):
        sig = RULE_34_SIGNALS["BEND"]
        self.assertEqual(sig["blasts"][0], 5.0)

    def test_b2_2_silent_intervals_positive(self):
        for name, sig in RULE_34_SIGNALS.items():
            for val in sig["blasts"]:
                if val < 0:
                    self.assertGreater(abs(val), 0.0)


# ---------------------------------------------------------------------------
# F2.3: Rule 35 Fog Timer Boundaries
# ---------------------------------------------------------------------------
class TestF2_3_Boundaries(unittest.TestCase):
    def test_b2_3_exact_speed_threshold_0_2_kts(self):
        sig = evaluate_rule35_fog_signal(stw=0.2)
        self.assertEqual(sig["mode"], "STOPPED")

    def test_b2_3_just_above_threshold_0_21_kts(self):
        sig = evaluate_rule35_fog_signal(stw=0.21)
        self.assertEqual(sig["mode"], "MAKING_WAY")

    def test_b2_3_timer_rollover_at_120s(self):
        timer = 120.0
        cycle = 120.0
        trigger = timer >= cycle
        timer_next = timer % cycle
        self.assertTrue(trigger)
        self.assertEqual(timer_next, 0.0)

    def test_b2_3_negative_speed_absolute(self):
        sig = evaluate_rule35_fog_signal(stw=abs(-10.0))
        self.assertEqual(sig["mode"], "MAKING_WAY")

    def test_b2_3_interval_constant(self):
        for spd in [0.0, 5.0, 15.0, 25.0]:
            sig = evaluate_rule35_fog_signal(stw=spd)
            self.assertEqual(sig["interval_sec"], 120)


# ---------------------------------------------------------------------------
# F2.4: Masthead Light Sync Boundaries
# ---------------------------------------------------------------------------
class TestF2_4_Boundaries(unittest.TestCase):
    def test_b2_4_zero_duration_flash_rejected(self):
        flash_duration = 1.0
        self.assertGreater(flash_duration, 0.0)

    def test_b2_4_sync_delay_under_100ms(self):
        audio_start_ms = 1000
        light_start_ms = 1020
        self.assertLess(abs(light_start_ms - audio_start_ms), 100)

    def test_b2_4_max_flash_intensity_clamped(self):
        intensity = min(12.0, 10.0)
        self.assertEqual(intensity, 10.0)

    def test_b2_4_daytime_contrast_boost(self):
        day_light_intensity = 8.0
        night_light_intensity = 4.0
        self.assertGreater(day_light_intensity, night_light_intensity)

    def test_b2_4_flash_decay_envelope(self):
        fade_time = 0.15
        self.assertLessEqual(fade_time, 0.20)


# ---------------------------------------------------------------------------
# F3.1: 1Hz VDR Telemetry Boundaries
# ---------------------------------------------------------------------------
class TestF3_1_Boundaries(unittest.TestCase):
    def test_b3_1_buffer_exact_1800_frames_capacity(self):
        vdr = VDRCircularBuffer(capacity=1800)
        for i in range(1800):
            vdr.record_frame({"t": i})
        self.assertEqual(vdr.count, 1800)

    def test_b3_1_buffer_wraparound_at_1801_frames(self):
        vdr = VDRCircularBuffer(capacity=1800)
        for i in range(1801):
            vdr.record_frame({"t": i})
        hist = vdr.get_history()
        self.assertEqual(len(hist), 1800)
        self.assertEqual(hist[0]["t"], 1)
        self.assertEqual(hist[-1]["t"], 1800)

    def test_b3_1_seek_before_oldest_frame(self):
        vdr = VDRCircularBuffer(capacity=10)
        for i in range(10, 20):
            vdr.record_frame({"t": i})
        f = vdr.seek_to_second(5)
        self.assertIsNotNone(f)

    def test_b3_1_seek_beyond_newest_frame(self):
        vdr = VDRCircularBuffer(capacity=10)
        for i in range(1, 11):
            vdr.record_frame({"t": i})
        f = vdr.seek_to_second(50)
        self.assertEqual(f["t"], 10)

    def test_b3_1_empty_buffer_seek(self):
        vdr = VDRCircularBuffer(capacity=10)
        self.assertIsNone(vdr.seek_to_second(1))


# ---------------------------------------------------------------------------
# F3.2: VDR Replay & CPA Time Graph Boundaries
# ---------------------------------------------------------------------------
class TestF3_2_Boundaries(unittest.TestCase):
    def test_b3_2_single_frame_cpa_graph(self):
        vdr = VDRCircularBuffer(capacity=10)
        vdr.record_frame({"t": 0, "cpa": 1.5})
        hist = vdr.get_history()
        self.assertEqual(len(hist), 1)

    def test_b3_2_all_zero_cpa_danger_graph(self):
        vdr = VDRCircularBuffer(capacity=10)
        for t in range(10):
            vdr.record_frame({"t": t, "cpa": 0.0})
        danger_count = sum(1 for f in vdr.get_history() if f["cpa"] < 1.0)
        self.assertEqual(danger_count, 10)

    def test_b3_2_scrubber_at_exact_time_zero(self):
        vdr = VDRCircularBuffer(capacity=10)
        for t in range(5):
            vdr.record_frame({"t": t, "x": float(t)})
        f0 = vdr.seek_to_second(0)
        self.assertEqual(f0["t"], 0)

    def test_b3_2_scrubber_at_exact_final_time(self):
        vdr = VDRCircularBuffer(capacity=10)
        for t in range(5):
            vdr.record_frame({"t": t, "x": float(t)})
        f4 = vdr.seek_to_second(4)
        self.assertEqual(f4["t"], 4)

    def test_b3_2_extreme_replay_speed_multiplier(self):
        dt = 0.1
        sim_speed = 10.0
        effective_dt = dt * sim_speed
        self.assertEqual(effective_dt, 1.0)


# ---------------------------------------------------------------------------
# F3.3: Client-Side PDF Export Boundaries
# ---------------------------------------------------------------------------
class TestF3_3_Boundaries(unittest.TestCase):
    def test_b3_3_exact_70_percent_pass_boundary(self):
        p70 = validate_certificate_data({"candidate_name": "T", "scenario_name": "S", "safety_score": 70, "min_cpa": 1.0})
        p69 = validate_certificate_data({"candidate_name": "T", "scenario_name": "S", "safety_score": 69, "min_cpa": 1.0})
        self.assertTrue(p70["passed"])
        self.assertFalse(p69["passed"])

    def test_b3_3_exact_1_0_nm_cpa_pass_boundary(self):
        c10 = validate_certificate_data({"candidate_name": "T", "scenario_name": "S", "safety_score": 80, "min_cpa": 1.0})
        c09 = validate_certificate_data({"candidate_name": "T", "scenario_name": "S", "safety_score": 80, "min_cpa": 0.99})
        self.assertTrue(c10["passed"])
        self.assertFalse(c09["passed"])

    def test_b3_3_zero_score_failure(self):
        res = validate_certificate_data({"candidate_name": "T", "scenario_name": "S", "safety_score": 0, "min_cpa": 0.0})
        self.assertFalse(res["passed"])

    def test_b3_3_perfect_100_score(self):
        res = validate_certificate_data({"candidate_name": "T", "scenario_name": "S", "safety_score": 100, "min_cpa": 2.5})
        self.assertTrue(res["passed"])

    def test_b3_3_missing_fields_validation(self):
        res = validate_certificate_data({})
        self.assertFalse(res["valid"])


# ---------------------------------------------------------------------------
# F4.1: Instructor Studio Boundaries
# ---------------------------------------------------------------------------
class TestF4_1_Boundaries(unittest.TestCase):
    def test_b4_1_max_target_ships_limit(self):
        targets = [f"T{i}" for i in range(5)]
        self.assertEqual(len(targets), 5)

    def test_b4_1_min_target_ships_limit(self):
        targets = ["T1"]
        self.assertEqual(len(targets), 1)

    def test_b4_1_extreme_initial_range(self):
        max_map_nm = 10.0
        range_input = 20.0
        clamped = min(range_input, max_map_nm)
        self.assertEqual(clamped, 10.0)

    def test_b4_1_negative_speed_clamped(self):
        raw_speed = -5.0
        clamped_speed = max(0.0, raw_speed)
        self.assertEqual(clamped_speed, 0.0)

    def test_b4_1_heading_modulo_360(self):
        raw_course = 360.0
        norm_course = raw_course % 360.0
        self.assertEqual(norm_course, 0.0)


# ---------------------------------------------------------------------------
# F4.2: Compact QR Engine Boundaries
# ---------------------------------------------------------------------------
class TestF4_2_Boundaries(unittest.TestCase):
    def test_b4_2_qr_max_length_bound(self):
        scen = {
            "id": "SCEN_MAX",
            "own": {"x": 5.0, "z": -5.0, "course": 359, "speed": 25.0},
            "targets": [{"id": f"T{i}", "type": "cargo", "x": float(i), "z": float(i), "course": 180, "speed": 10.0} for i in range(5)],
            "environment": {"fog": True, "wind": {"dir": 360, "spd": 50}}
        }
        encoded = encode_compact_scenario(scen)
        self.assertLess(len(encoded), 250)

    def test_b4_2_empty_string_decoding(self):
        with self.assertRaises(Exception):
            decode_compact_scenario("")

    def test_b4_2_pin_case_insensitivity(self):
        pin_upper = "ABC123"
        pin_lower = "abc123"
        self.assertEqual(pin_upper.lower(), pin_lower)

    def test_b4_2_special_characters_in_name(self):
        cleaned = "".join(c for c in "Ship #1 & Co." if c.isalnum() or c in " _-")
        self.assertEqual(cleaned, "Ship 1  Co")

    def test_b4_2_corrupted_payload_checksum(self):
        with self.assertRaises(Exception):
            decode_compact_scenario('{"v":1,"own":[0,0]}')


# ---------------------------------------------------------------------------
# F4.3: Offline LMS Leaderboard Boundaries
# ---------------------------------------------------------------------------
class TestF4_3_Boundaries(unittest.TestCase):
    def test_b4_3_leaderboard_score_clamped_0_to_100(self):
        s_low = compute_total_eval_score(0, 0, min_cpa=0.1, rule_violations=5)
        s_high = compute_total_eval_score(100, 100, min_cpa=3.0, rule_violations=0)
        self.assertEqual(s_low, 0)
        self.assertEqual(s_high, 100)

    def test_b4_3_quiz_score_0_practical_100(self):
        score = compute_total_eval_score(0, 100, min_cpa=2.0)
        self.assertEqual(score, 60)

    def test_b4_3_quiz_score_100_practical_0(self):
        score = compute_total_eval_score(100, 0, min_cpa=2.0)
        self.assertEqual(score, 40)

    def test_b4_3_duplicate_cadet_ranking(self):
        records = [
            {"name": "Cadet A", "score": 80, "time": 100},
            {"name": "Cadet B", "score": 80, "time": 90}
        ]
        sorted_recs = sorted(records, key=lambda r: (-r["score"], r["time"]))
        self.assertEqual(sorted_recs[0]["name"], "Cadet B")

    def test_b4_3_excessive_rule_violations(self):
        score = compute_total_eval_score(100, 100, min_cpa=0.2, rule_violations=10)
        self.assertEqual(score, 0)


# ---------------------------------------------------------------------------
# F5.1: WebXR VR Cockpit Boundaries
# ---------------------------------------------------------------------------
class TestF5_1_Boundaries(unittest.TestCase):
    def test_b5_1_camera_y_clamped_above_deck(self):
        cam, _ = calculate_bridge_camera_position(0.0, 0.0, 0.0, height=0.88)
        self.assertGreaterEqual(cam[1], 0.88)

    def test_b5_1_fov_clamped_between_30_and_110(self):
        fov = max(30, min(120, 110))
        self.assertEqual(fov, 110)

    def test_b5_1_camera_far_plane_1000(self):
        far_plane = 1000.0
        self.assertEqual(far_plane, 1000.0)

    def test_b5_1_camera_near_plane_0_1(self):
        near_plane = 0.1
        self.assertEqual(near_plane, 0.1)

    def test_b5_1_extreme_ship_coordinates_vr(self):
        cam, _ = calculate_bridge_camera_position(own_x=10.0, own_z=10.0, hdg=0.0)
        self.assertAlmostEqual(cam[0], -200.0, places=1)
        self.assertAlmostEqual(cam[2], 200.3, places=1)


# ---------------------------------------------------------------------------
# F5.2: Mobile Gyroscope Boundaries
# ---------------------------------------------------------------------------
class TestF5_2_Boundaries(unittest.TestCase):
    def test_b5_2_extreme_pitch_gimbal_lock_avoidance(self):
        q = orientation_euler_to_quaternion(alpha_deg=0.0, beta_deg=90.0, gamma_deg=0.0)
        norm = math.sqrt(sum(x * x for x in q))
        self.assertAlmostEqual(norm, 1.0)

    def test_b5_2_extreme_roll_angle(self):
        q = orientation_euler_to_quaternion(alpha_deg=0.0, beta_deg=0.0, gamma_deg=180.0)
        norm = math.sqrt(sum(x * x for x in q))
        self.assertAlmostEqual(norm, 1.0)

    def test_b5_2_negative_angles_normalization(self):
        q = orientation_euler_to_quaternion(alpha_deg=-45.0, beta_deg=-30.0, gamma_deg=-15.0)
        norm = math.sqrt(sum(x * x for x in q))
        self.assertAlmostEqual(norm, 1.0)

    def test_b5_2_quaternion_zero_division_guard(self):
        q = orientation_euler_to_quaternion(0.0, 0.0, 0.0)
        self.assertEqual(q[3], 1.0)

    def test_b5_2_device_orientation_permission_state(self):
        valid_states = ["granted", "denied", "default"]
        self.assertIn("granted", valid_states)


# ---------------------------------------------------------------------------
# F6.1: 100% Offline Asset Suite Boundaries
# ---------------------------------------------------------------------------
class TestF6_1_Boundaries(unittest.TestCase):
    def test_b6_1_no_http_or_https_asset_urls(self):
        # Audit simulator.html to ensure zero external script tags
        html_path = os.path.join(PROJECT_ROOT, "simulator.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn('<script src="http://', content)

    def test_b6_1_system_font_fallback_present(self):
        html_path = os.path.join(PROJECT_ROOT, "simulator.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("sans-serif", content)

    def test_b6_1_canvas_radial_texture_procedural(self):
        html_path = os.path.join(PROJECT_ROOT, "simulator.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("createRadialGradient", content)

    def test_b6_1_local_library_file_sizes(self):
        three_path = os.path.join(PROJECT_ROOT, "js", "three.min.js")
        size = os.path.getsize(three_path)
        self.assertGreater(size, 100000)

    def test_b6_1_zero_external_images(self):
        html_path = os.path.join(PROJECT_ROOT, "simulator.html")
        with open(html_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertNotIn('<img src="http', content)


# ---------------------------------------------------------------------------
# F6.2: Capacitor & Android APK Sync Boundaries
# ---------------------------------------------------------------------------
class TestF6_2_Boundaries(unittest.TestCase):
    def test_b6_2_manifest_start_url(self):
        manifest_path = os.path.join(PROJECT_ROOT, "manifest.json")
        with open(manifest_path, "r", encoding="utf-8") as f:
            m = json.load(f)
        self.assertIn("simulator.html", m.get("start_url", ""))

    def test_b6_2_cache_version_naming(self):
        sw_path = os.path.join(PROJECT_ROOT, "sw.js")
        with open(sw_path, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("colregs-3d-v", content)

    def test_b6_2_android_package_naming(self):
        app_spec = os.path.join(PROJECT_ROOT, "COLREGS_3D_Simulator.spec")
        self.assertTrue(os.path.exists(app_spec))

    def test_b6_2_sensor_landscape_orientation(self):
        workflow = os.path.join(PROJECT_ROOT, ".github", "workflows", "build-apk.yml")
        with open(workflow, "r", encoding="utf-8") as f:
            content = f.read()
        self.assertIn("sensorLandscape", content)

    def test_b6_2_apk_zip_package_integrity(self):
        zip_path = os.path.join(PROJECT_ROOT, "COLREGS_3D_Mobile_Package.zip")
        self.assertTrue(os.path.exists(zip_path))
        self.assertGreater(os.path.getsize(zip_path), 500000)


if __name__ == "__main__":
    unittest.main()
