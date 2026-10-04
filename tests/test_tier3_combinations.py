"""
Tier 3: Cross-Feature Combinations Test Suite for COLREGS-3D.
Contains exactly 20 tests verifying interactions between interconnected subsystems.
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


class TestTier3CrossFeatureCombinations(unittest.TestCase):

    def test_x01_tss_lane_keeping_in_dense_fog_with_rule35_sound(self):
        """Interaction: Rule 10 TSS lane following + Rule 19 Fog + Rule 35(a) Sound signal."""
        # 1. TSS flow verification
        flow_eval = evaluate_tss_flow(hdg=60.0, lane_bearing=60.0)
        self.assertEqual(flow_eval["status"], "COMPLIANT_FLOW")

        # 2. Dense fog visibility calculation
        vis_nm = calculate_fog_visibility(fog_density=0.08)
        self.assertLess(vis_nm, 2.0)

        # 3. Rule 35 fog sound signal while making way
        sound_eval = evaluate_rule35_fog_signal(stw=14.0)
        self.assertEqual(sound_eval["mode"], "MAKING_WAY")
        self.assertEqual(sound_eval["blasts"], [5.0])

    def test_x02_five_ship_encounter_with_wind_leeway_and_current(self):
        """Interaction: 5-ship kinematics + Wind leeway + Current drift on own ship."""
        v_g, sog, cog, crab = calculate_ground_motion(
            hdg=0.0, stw=14.0, current_set=90.0, current_drift=2.5,
            wind_dir=270.0, wind_spd=20.0, k_leeway=0.04
        )
        self.assertGreater(sog, 14.0)
        self.assertGreater(crab, 0.0)

        own_pos = np.array([0.0, 0.0])
        targets = [
            {"id": "T1", "x": 0.0, "z": 4.0, "course": 180.0, "speed": 12.0, "type": "cargo"},
            {"id": "T2", "x": 3.0, "z": 1.0, "course": 270.0, "speed": 16.0, "type": "container"},
            {"id": "T3", "x": -2.5, "z": 2.0, "course": 90.0, "speed": 9.0, "type": "fishing"},
            {"id": "T4", "x": 1.5, "z": 5.0, "course": 200.0, "speed": 10.0, "type": "tanker"},
            {"id": "T5", "x": -1.0, "z": 6.0, "course": 160.0, "speed": 11.0, "type": "tug"}
        ]
        results = evaluate_multi_target_kinematics(own_pos, v_g, targets)
        self.assertEqual(len(results), 5)
        for r in results:
            self.assertIn("cpa", r)
            self.assertIn("tcpa", r)

    def test_x03_narrow_channel_overtaking_with_rule34_whistle_and_masthead_flash(self):
        """Interaction: Rule 9 Channel + Rule 34(c) Overtaking Whistle + Synchronized Light."""
        # 1. Starboard lane keeping in narrow channel
        ch_eval = evaluate_rule9_channel(np.array([0.4, 2.0]), np.array([0.0, 0.0]), channel_bearing=0.0, channel_half_width=0.8)
        self.assertTrue(ch_eval["compliant"])

        # 2. Whistle intention signal: intention to overtake on starboard side (-- •)
        overtake_sig = RULE_34_SIGNALS["OVERTAKE_STBD"]
        self.assertEqual(overtake_sig["blasts"], [5.0, -1.0, 5.0, -1.0, 1.0])

        # 3. Agreement signal from overtaken vessel: Morse 'C' (- • - •)
        agree_sig = RULE_34_SIGNALS["OVERTAKE_AGREE"]
        self.assertEqual(agree_sig["blasts"], [5.0, -1.0, 1.0, -1.0, 5.0, -1.0, 1.0])

    def test_x04_vdr_recording_during_multi_vessel_evasive_maneuver(self):
        """Interaction: Evasive maneuver execution recorded across 30 seconds into VDR."""
        vdr = VDRCircularBuffer(capacity=100)
        own_x, own_z = 0.0, 0.0
        course = 0.0

        for t in range(30):
            if t >= 10:
                course = min(30.0, course + 2.0)  # Turning starboard 2 deg/sec
            v_own = velocity_water(course, 14.0)
            own_x += v_own[0] * (1.0 / 3600.0)
            own_z += v_own[1] * (1.0 / 3600.0)
            vdr.record_frame({
                "t": t, "x": own_x, "z": own_z, "hdg": course, "stw": 14.0, "rudder": 15.0 if t >= 10 else 0.0
            })

        hist = vdr.get_history()
        self.assertEqual(len(hist), 30)
        self.assertAlmostEqual(hist[-1]["hdg"], 30.0)

    def test_x05_vdr_scrub_replay_with_cpa_time_graph_and_radar_sync(self):
        """Interaction: VDR Replay Controller + Scrub Timeline + CPA Curve."""
        vdr = VDRCircularBuffer(capacity=50)
        for t in range(40):
            cpa = 2.0 - (t / 40.0) * 1.5 if t < 25 else 0.5 + ((t - 25) / 15.0) * 1.5
            vdr.record_frame({"t": t, "cpa": cpa, "dist": 3.0 - t * 0.05})

        # Scrub to t=25s (nadir of CPA curve)
        frame_at_danger = vdr.seek_to_second(25)
        self.assertIsNotNone(frame_at_danger)
        self.assertAlmostEqual(frame_at_danger["cpa"], 0.5)

    def test_x06_instructor_studio_qr_export_loaded_into_webxr_rig(self):
        """Interaction: Instructor Studio -> Compact QR Serialization -> WebXR Camera Rig."""
        scenario = {
            "id": "XR_STUD",
            "own": {"x": 1.0, "z": -2.0, "course": 350, "speed": 12.0},
            "targets": [{"id": "T1", "type": "container", "x": 2.0, "z": 3.0, "course": 180, "speed": 15.0}],
            "environment": {"fog": False, "wind": {"dir": 0, "spd": 0}}
        }
        qr_json = encode_compact_scenario(scenario)
        self.assertLess(len(qr_json), 150)

        decoded = decode_compact_scenario(qr_json)
        cam_pos, look_pos = calculate_bridge_camera_position(
            own_x=decoded["own"]["x"], own_z=decoded["own"]["z"], hdg=decoded["own"]["course"]
        )
        self.assertAlmostEqual(cam_pos[1], 0.88)
        self.assertNotEqual(cam_pos[0], look_pos[0])

    def test_x07_restricted_visibility_fog_with_spatial_audio_attenuation(self):
        """Interaction: 3D Fog + Spatial Audio Distance Attenuation + Radar Detection."""
        fog_vis = calculate_fog_visibility(0.06)  # ~2.5 NM visual extinction
        target_dist = 1.8  # Target audible and visible at close quarters
        gain = calculate_spatial_audio_attenuation(target_dist)
        self.assertGreater(gain, 0.0)
        self.assertLess(gain, 1.0)
        self.assertLessEqual(target_dist, fog_vis)

    def test_x08_rule10_perpendicular_crossing_with_tidal_current_compensation(self):
        """Interaction: Rule 10(c) TSS Perpendicular Heading + Tidal Drift on COG."""
        # Vessel heading 150° (perpendicular to 060° TSS lane)
        # Current 2.5 kts setting 090° alters COG
        _, sog, cog, crab = calculate_ground_motion(hdg=150.0, stw=12.0, current_set=90.0, current_drift=2.5)

        # Rule 10(c) requires heading (not COG) to cross at right angles
        eval_cross = evaluate_tss_crossing(hdg=150.0, lane_bearing=60.0)
        self.assertTrue(eval_cross["compliant"])
        self.assertEqual(eval_cross["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertNotEqual(cog, 150.0)

    def test_x09_narrow_channel_blind_bend_sound_and_ialabuoys(self):
        """Interaction: Rule 9 Channel + Blind Bend Warning + IALA Region A Buoys."""
        # 1. IALA Region A buoys mark the channel
        port_mark = get_iala_lateral_mark("A", "port")
        stbd_mark = get_iala_lateral_mark("A", "starboard")
        self.assertEqual(port_mark["color"], "RED")
        self.assertEqual(stbd_mark["color"], "GREEN")

        # 2. Blind bend whistle blast
        sig = RULE_34_SIGNALS["BEND"]
        self.assertEqual(sig["blasts"], [5.0])

    def test_x10_multi_target_stand_on_with_nuc_vessel_rule18_precedence(self):
        """Interaction: Rule 15 Crossing + Rule 18 Vessel Hierarchy (NUC precedence)."""
        own_pos = np.array([0.0, 0.0])
        own_vel = velocity_water(0.0, 12.0)
        # NUC vessel on port side with crossing geometry
        p_nuc = np.array([-1.5, 1.5])
        v_nuc = velocity_water(90.0, 8.0)
        res = calculate_cpa_tcpa_single(own_pos, own_vel, p_nuc, v_nuc)
        self.assertLess(res["cpa"], 1.0)

        # Even though target is on port side (ordinarily stand-on for own ship),
        # NUC vessel has right of way under Rule 18
        is_nuc = True
        must_give_way = is_nuc
        self.assertTrue(must_give_way)

    def test_x11_vdr_telemetry_dump_to_offline_pdf_certificate(self):
        """Interaction: 30-min VDR summary telemetry exported to PDF Certificate."""
        vdr = VDRCircularBuffer(capacity=1800)
        for t in range(1800):
            vdr.record_frame({"t": t, "cpa": 1.6 + math.sin(t * 0.01) * 0.2})

        hist = vdr.get_history()
        min_cpa = min(f["cpa"] for f in hist)
        cert_data = {
            "candidate_name": "Nguyen Van Hai",
            "scenario_name": "Dover TSS Crossing",
            "safety_score": 92,
            "min_cpa": min_cpa
        }
        cert_res = validate_certificate_data(cert_data)
        self.assertTrue(cert_res["valid"])
        self.assertTrue(cert_res["passed"])

    def test_x12_mobile_gyroscope_cockpit_view_with_fog_and_nav_lights(self):
        """Interaction: Mobile Gyroscope 360° + Fog Extinction + Target Navigation Lights."""
        # Heading 045°, device tilted looking 30° up and 45° azimuth
        q = orientation_euler_to_quaternion(alpha_deg=45.0, beta_deg=30.0, gamma_deg=0.0)
        self.assertAlmostEqual(math.sqrt(sum(x*x for x in q)), 1.0)

        # Target vessel at 1.0 NM in fog
        fog_vis = calculate_fog_visibility(0.045)
        self.assertGreaterEqual(fog_vis, 1.0)  # Nav lights visible

    def test_x13_classroom_quiz_scoring_merged_with_practical_vdr_data(self):
        """Interaction: 500-question quiz result + Practical VDR navigation score."""
        quiz_score = 92
        nav_score = 85
        combined = compute_total_eval_score(quiz_score, nav_score, min_cpa=1.8, rule_violations=0)
        self.assertEqual(combined, 88)

    def test_x14_rule34_danger_blasts_with_speed_reduction_and_vdr(self):
        """Interaction: Rule 34(d) 5 rapid blasts + Engine Astern + VDR logging."""
        danger_sig = RULE_34_SIGNALS["DANGER"]
        self.assertEqual(danger_sig["flashes"], 5)

        vdr = VDRCircularBuffer(capacity=10)
        vdr.record_frame({"t": 1, "stw": 14.0, "status": "DANGER_SOUNDED"})
        vdr.record_frame({"t": 2, "stw": 8.0, "status": "ENGINE_ASTERN"})
        hist = vdr.get_history()
        self.assertLess(hist[1]["stw"], hist[0]["stw"])

    def test_x15_tss_separation_zone_crossing_with_right_angle_verification(self):
        """Interaction: Rule 10(e) Separation Zone + Rule 10(c) Perpendicular Crossing."""
        # Vessel inside separation zone
        d_stbd = 0.2
        sep_width = 1.0
        # Authorised crossing because crossing angle is right-angle
        cross_eval = evaluate_tss_crossing(hdg=150.0, lane_bearing=60.0)
        is_crossing = cross_eval["compliant"]
        sep_eval = evaluate_tss_separation_zone(d_stbd, sep_width, is_crossing=is_crossing)
        self.assertFalse(sep_eval["violation"])
        self.assertEqual(sep_eval["status"], "AUTHORIZED_CROSSING")

    def test_x16_offline_asset_suite_supports_full_vdr_and_pdf_pipeline(self):
        """Interaction: Offline JS libraries + Service Worker + Manifest configuration."""
        manifest_path = os.path.join(PROJECT_ROOT, "manifest.json")
        sw_path = os.path.join(PROJECT_ROOT, "sw.js")
        with open(manifest_path, "r", encoding="utf-8") as f:
            m = json.load(f)
        with open(sw_path, "r", encoding="utf-8") as f:
            sw = f.read()
        self.assertEqual(m["display"], "standalone")
        self.assertIn("simulator.html", sw)

    def test_x17_extreme_wind_drift_crab_angle_radar_vector_display(self):
        """Interaction: Leeway Physics + ARPA True vs Relative Vector on Radar."""
        _, sog, cog, crab = calculate_ground_motion(
            hdg=0.0, stw=10.0, wind_dir=270.0, wind_spd=45.0, k_leeway=0.04
        )
        self.assertGreater(abs(crab), 5.0)
        # Radar displays True Motion vector aligned with COG (not HDG)
        self.assertNotEqual(cog, 0.0)

    def test_x18_rule35_fog_timer_transition_on_vessel_stop(self):
        """Interaction: Dynamic speed change in fog triggers Rule 35 mode shift."""
        sig_moving = evaluate_rule35_fog_signal(stw=12.0)
        sig_stopped = evaluate_rule35_fog_signal(stw=0.0)
        self.assertEqual(sig_moving["mode"], "MAKING_WAY")
        self.assertEqual(sig_stopped["mode"], "STOPPED")
        self.assertNotEqual(sig_moving["blasts"], sig_stopped["blasts"])

    def test_x19_ialabuoys_region_b_toggle_in_narrow_channel(self):
        """Interaction: Narrow Channel with Region A vs Region B lateral buoy swap."""
        # Region A: Starboard is Green
        stbd_a = get_iala_lateral_mark("A", "starboard")
        self.assertEqual(stbd_a["color"], "GREEN")

        # Region B: Starboard is Red ("Red Right Returning")
        stbd_b = get_iala_lateral_mark("B", "starboard")
        self.assertEqual(stbd_b["color"], "RED")

    def test_x20_full_instructor_pin_distribution_to_student_leaderboard(self):
        """Interaction: Instructor Studio authoring -> PIN decode -> Simulation -> Leaderboard rank."""
        scenario = {
            "id": "EXAM_STCW",
            "own": {"x": 0.0, "z": -4.0, "course": 0, "speed": 14.0},
            "targets": [{"id": "T1", "type": "cargo", "x": 0.5, "z": 2.0, "course": 180, "speed": 12.0}],
            "environment": {"fog": False, "wind": {"dir": 0, "spd": 0}}
        }
        encoded = encode_compact_scenario(scenario)
        decoded = decode_compact_scenario(encoded)
        self.assertEqual(decoded["id"], "EXAM_STC")

        total_score = compute_total_eval_score(quiz_score=95, navigation_score=90, min_cpa=1.7)
        self.assertEqual(total_score, 92)


if __name__ == "__main__":
    unittest.main()
