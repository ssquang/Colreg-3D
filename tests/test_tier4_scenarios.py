"""
Tier 4: Real-World Operational Scenarios Test Suite for COLREGS-3D.
Contains exactly 10 comprehensive end-to-end maritime scenarios.
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


class TestTier4RealWorldScenarios(unittest.TestCase):

    def test_scenario_01_dover_strait_tss_perpendicular_crossing(self):
        """Scenario 1: Dover Strait TSS right-angle crossing under tidal stream."""
        lane_bearing = 55.0  # Northeast traffic lane
        # Ferry heading 145° (perpendicular to 055° lane)
        ferry_hdg = 145.0
        ferry_stw = 18.0

        # Tidal stream 3.0 kts setting 055°
        v_g, sog, cog, crab = calculate_ground_motion(
            hdg=ferry_hdg, stw=ferry_stw, current_set=55.0, current_drift=3.0
        )

        # Rule 10(c) verification: Legal compliance is based on heading, not ground track
        cross_eval = evaluate_tss_crossing(hdg=ferry_hdg, lane_bearing=lane_bearing)
        self.assertTrue(cross_eval["compliant"])
        self.assertEqual(cross_eval["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertAlmostEqual(cross_eval["perpendicular_error_deg"], 0.0)

        # Check encounter with container ship in lane
        p_ferry = np.array([0.0, 0.0])
        p_container = np.array([1.5, 4.0])
        v_container = velocity_water(55.0, 19.0)
        telemetry = calculate_cpa_tcpa_single(p_ferry, v_g, p_container, v_container)
        self.assertGreater(telemetry["cpa"], 1.0)  # Safe crossing clearance

    def test_scenario_02_singapore_strait_narrow_channel_overtaking(self):
        """Scenario 2: Singapore Strait Phillips Channel overtaking with Rule 34 whistle signals."""
        ch_start = np.array([0.0, 0.0])
        ch_bearing = 70.0
        ch_half_width = 0.6  # 0.6 NM narrow fairway

        # Own ship at 16 kts on starboard fairway of 070° channel
        p_own = np.array([1.0, 0.15])  # Starboard side of channel (d_stbd > 0)
        ch_eval = evaluate_rule9_channel(p_own, ch_start, ch_bearing, ch_half_width)
        self.assertTrue(ch_eval["compliant"])
        self.assertGreater(ch_eval["d_stbd"], 0.0)


        # Overtaking intention whistle signal on starboard side (-- •)
        overtake_stbd = RULE_34_SIGNALS["OVERTAKE_STBD"]
        self.assertEqual(overtake_stbd["blasts"], [5.0, -1.0, 5.0, -1.0, 1.0])

        # Overtaken vessel agrees with Morse 'C' (- • - •)
        agree_morse_c = RULE_34_SIGNALS["OVERTAKE_AGREE"]
        self.assertEqual(agree_morse_c["blasts"], [5.0, -1.0, 1.0, -1.0, 5.0, -1.0, 1.0])

    def test_scenario_03_van_don_archipelago_restricted_visibility_fishing_flotilla(self):
        """Scenario 3: Van Don coastal waters in dense fog encountering fishing flotilla."""
        fog_density = 0.09
        vis_nm = calculate_fog_visibility(fog_density)
        self.assertLess(vis_nm, 1.7)  # Obscured to less than 1.7 NM

        # Rule 35(a) periodic sound signal every 120s
        fog_sig = evaluate_rule35_fog_signal(stw=11.0)
        self.assertEqual(fog_sig["mode"], "MAKING_WAY")
        self.assertEqual(fog_sig["interval_sec"], 120)

        # 3 fishing targets tracked simultaneously on ARPA Radar
        own_pos = np.array([0.0, 0.0])
        own_vel = velocity_water(0.0, 11.0)
        fishing_flotilla = [
            {"id": "FISH-1", "x": 0.8, "z": 2.2, "course": 190.0, "speed": 5.0, "type": "fishing"},
            {"id": "FISH-2", "x": -0.6, "z": 2.8, "course": 170.0, "speed": 6.0, "type": "fishing"},
            {"id": "FISH-3", "x": 1.2, "z": 3.5, "course": 210.0, "speed": 4.5, "type": "fishing"}
        ]
        results = evaluate_multi_target_kinematics(own_pos, own_vel, fishing_flotilla)
        self.assertEqual(len(results), 3)
        for tgt in results:
            self.assertTrue(tgt["tcpa"] > 0)

    def test_scenario_04_malacca_strait_night_transit_with_nuc_vessel(self):
        """Scenario 4: Malacca Strait night encounter with Not Under Command (NUC) vessel."""
        # Own ship on course 315° (Northwest bound) at 15 kts
        p_own = np.array([0.0, 0.0])
        v_own_initial = velocity_water(315.0, 15.0)

        # NUC vessel drifting dead ahead at 1.5 kts
        p_nuc = np.array([-1.414, 1.414])  # 2.0 NM along 315°
        v_nuc = velocity_water(220.0, 1.5)

        initial_telemetry = calculate_cpa_tcpa_single(p_own, v_own_initial, p_nuc, v_nuc)
        self.assertLess(initial_telemetry["cpa"], 0.2)  # Imminent collision without action

        # Rule 18 gives NUC precedence. Own ship makes bold alteration 35° to starboard (course 350°)
        v_own_evade = velocity_water(350.0, 15.0)
        evade_telemetry = calculate_cpa_tcpa_single(p_own, v_own_evade, p_nuc, v_nuc)
        self.assertGreater(evade_telemetry["cpa"], 1.0)  # Safe clearance achieved

    def test_scenario_05_english_channel_blind_bend_sound_protocol(self):
        """Scenario 5: Blind bend obstructed fairway warning protocol."""
        bend_warning = RULE_34_SIGNALS["BEND"]
        # Exactly 1 prolonged blast (5.0s) per Rule 34(e)
        self.assertEqual(bend_warning["blasts"], [5.0])
        self.assertEqual(bend_warning["duration"], 5.0)

        # Both vessels keeping outer starboard side
        res_v1 = evaluate_rule9_channel(np.array([0.2, 1.0]), np.array([0.0, 0.0]), 0.0, 0.5)
        res_v2 = evaluate_rule9_channel(np.array([0.2, 5.0]), np.array([0.0, 0.0]), 0.0, 0.5)
        self.assertTrue(res_v1["compliant"])
        self.assertTrue(res_v2["compliant"])

    def test_scenario_06_stcw_oow_certification_exam_pipeline(self):
        """Scenario 6: STCW Regulation II/1 OOW Examination Lifecycle."""
        # 1. 12-minute VDR buffer recorded (720 frames)
        vdr = VDRCircularBuffer(capacity=1800)
        for t in range(720):
            # Safe trajectory keeping CPA > 1.4 NM
            cpa = 1.45 + (t / 720.0) * 0.5
            vdr.record_frame({"t": t, "cpa": cpa, "stw": 14.0, "score": 94})

        hist = vdr.get_history()
        self.assertEqual(len(hist), 720)
        min_cpa = min(f["cpa"] for f in hist)

        # 2. Certificate generation
        cert = validate_certificate_data({
            "candidate_name": "Tran Van Duc",
            "scenario_name": "STCW OOW Assessment",
            "safety_score": 94,
            "min_cpa": min_cpa
        })
        self.assertTrue(cert["valid"])
        self.assertTrue(cert["passed"])
        self.assertEqual(cert["standard"], "STCW_A_II_1")

    def test_scenario_07_rule19_radar_plotting_high_speed_encounter(self):
        """Scenario 7: Restricted visibility high-speed encounter: avoid port turn forward of beam."""
        p_own = np.array([0.0, 0.0])
        v_own = velocity_water(0.0, 20.0)

        # Target approaching from 007°
        p_tgt = np.array([0.5, 4.0])
        v_tgt = velocity_water(190.0, 22.0)

        initial = calculate_cpa_tcpa_single(p_own, v_own, p_tgt, v_tgt)
        self.assertLess(initial["cpa"], 0.4)

        # Rule 19(d)(i): Do NOT alter course to port for a vessel forward of beam
        # Alter to STARBOARD (+40° -> course 040°)
        v_own_stbd = velocity_water(40.0, 20.0)
        stbd_res = calculate_cpa_tcpa_single(p_own, v_own_stbd, p_tgt, v_tgt)
        self.assertGreater(stbd_res["cpa"], 1.0)

    def test_scenario_08_shallow_bank_fairway_iala_region_a_navigation(self):
        """Scenario 8: Winding fairway navigation with IALA Region A lateral buoyage."""
        port_mark = get_iala_lateral_mark("A", "port")
        stbd_mark = get_iala_lateral_mark("A", "starboard")
        self.assertEqual(port_mark["color"], "RED")
        self.assertEqual(port_mark["topmark"], "CAN")
        self.assertEqual(stbd_mark["color"], "GREEN")
        self.assertEqual(stbd_mark["topmark"], "CONE_POINT_UP")

        # Vessel navigates along starboard side of channel
        fairway_pos = np.array([0.3, 2.5])
        res = evaluate_rule9_channel(fairway_pos, np.array([0.0, 0.0]), channel_bearing=0.0, channel_half_width=0.6)
        self.assertTrue(res["compliant"])

    def test_scenario_09_combined_current_and_leeway_tss_compensation(self):
        """Scenario 9: Compensation of current and wind in TSS to maintain true ground track."""
        lane_bearing = 0.0  # Due North TSS lane

        # Environmental forces: Current 2.0 kts setting 090°, Wind 30 kts from 270°
        # Both push vessel East (+X)
        # Navigator crabs heading to 347.0° (steers into wind/current)
        v_g, sog, cog, crab = calculate_ground_motion(
            hdg=347.0, stw=14.0, current_set=90.0, current_drift=2.0,
            wind_dir=270.0, wind_spd=30.0, k_leeway=0.04
        )

        # Resulting COG stays aligned with North lane (within 1 degree)
        self.assertAlmostEqual(cog, 0.0, delta=1.0)
        self.assertGreater(abs(crab), 10.0)


    def test_scenario_10_end_to_end_classroom_to_certificate_lifecycle(self):
        """Scenario 10: Complete Instructor authoring -> QR -> VDR -> Leaderboard -> PDF Certificate pipeline."""
        # 1. Author scenario in Instructor Studio
        authored = {
            "id": "CERT_E2E",
            "own": {"x": 0.0, "z": -3.0, "course": 0, "speed": 14.0},
            "targets": [
                {"id": "T1", "type": "cargo", "x": 0.5, "z": 3.0, "course": 180, "speed": 12.0},
                {"id": "T2", "type": "tanker", "x": 3.0, "z": 0.0, "course": 270, "speed": 15.0}
            ],
            "environment": {"fog": True, "wind": {"dir": 90, "spd": 15}}
        }

        # 2. Export to compact QR schema (<150 chars)
        qr_str = encode_compact_scenario(authored)
        self.assertLess(len(qr_str), 150)

        # 3. Student imports scenario
        imported = decode_compact_scenario(qr_str)
        self.assertEqual(imported["id"], "CERT_E2E")
        self.assertEqual(len(imported["targets"]), 2)

        # 4. Simulation run with 1Hz VDR recording
        vdr = VDRCircularBuffer(capacity=100)
        for t in range(50):
            vdr.record_frame({"t": t, "cpa": 1.7, "stw": 14.0})

        # 5. Score calculation and leaderboard entry
        final_score = compute_total_eval_score(quiz_score=95, navigation_score=90, min_cpa=1.7)
        self.assertEqual(final_score, 92)

        # 6. Official PDF certificate validation
        cert = validate_certificate_data({
            "candidate_name": "Pham Minh Tuan",
            "scenario_name": "End-to-End Maritime Assessment",
            "safety_score": final_score,
            "min_cpa": 1.7
        })
        self.assertTrue(cert["passed"])
        self.assertEqual(cert["dimensions_mm"], (210, 297))


if __name__ == "__main__":
    unittest.main()
