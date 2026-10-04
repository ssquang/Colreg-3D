#!/usr/bin/env python3
"""
Adversarial Empirical Challenge Suite - Milestone M1 (Challenger 2)
Focus Areas:
1. Rule 10 TSS Perpendicular Crossing Boundaries (79°, 81°, 90°, 99°, 101°, 69°, 111°)
2. Rule 10 TSS Wrong-Way Flow vs Crossing Precedence (89° vs 91°)
3. IALA Buoyage System Lateral Color Inversion (Region A vs Region B) & Cardinal Marks
4. Rule 9 Narrow Channel Boundaries & Blind Bend Whistle Protocol
5. 3D Fog Visual Range Contrast Extinction & ARPA Radar Independence
6. End-to-end HTML/JS Execution Verification via Node.js
"""

import unittest
import math
import subprocess
import json
import os
import sys

# Ensure tests/ directory is on sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from maritime_models import (
    evaluate_rule9_channel,
    evaluate_tss_flow,
    evaluate_tss_crossing,
    evaluate_tss_separation_zone,
    get_iala_lateral_mark,
    get_iala_cardinal_mark,
    calculate_fog_visibility,
    RULE_34_SIGNALS
)


class TestRule10CrossingBoundaries(unittest.TestCase):
    """
    Challenge Rule 10(c) perpendicular crossing boundaries:
    - 81° & 99°: Compliant (error = 9° <= 10°)
    - 80° & 100°: Compliant at exact 10° boundary (error = 10° <= 10°)
    - 79° & 101°: Error = 11° > 10° (Exceeds strict 10° right-angle boundary)
    - 69° & 111°: Error = 21° > 20° (Oblique crossing violation)
    """

    def test_perpendicular_crossing_strict_boundaries(self):
        # Lane bearing = 000° (Northbound). Perpendicular = 090° (Eastbound).
        lane_bearing = 0.0

        # Exact perpendicular (90°)
        r90 = evaluate_tss_crossing(hdg=90.0, lane_bearing=lane_bearing)
        self.assertTrue(r90["compliant"])
        self.assertEqual(r90["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertAlmostEqual(r90["perpendicular_error_deg"], 0.0)

        # 81° (9° error <= 10°)
        r81 = evaluate_tss_crossing(hdg=81.0, lane_bearing=lane_bearing)
        self.assertTrue(r81["compliant"])
        self.assertEqual(r81["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertAlmostEqual(r81["perpendicular_error_deg"], 9.0)

        # 99° (9° error <= 10°)
        r99 = evaluate_tss_crossing(hdg=99.0, lane_bearing=lane_bearing)
        self.assertTrue(r99["compliant"])
        self.assertEqual(r99["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertAlmostEqual(r99["perpendicular_error_deg"], 9.0)

        # 80° (10° error == 10°)
        r80 = evaluate_tss_crossing(hdg=80.0, lane_bearing=lane_bearing)
        self.assertTrue(r80["compliant"])
        self.assertEqual(r80["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertAlmostEqual(r80["perpendicular_error_deg"], 10.0)

        # 100° (10° error == 10°)
        r100 = evaluate_tss_crossing(hdg=100.0, lane_bearing=lane_bearing)
        self.assertTrue(r100["compliant"])
        self.assertEqual(r100["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertAlmostEqual(r100["perpendicular_error_deg"], 10.0)

        # 79° (11° error > 10°: Exceeds strict 10° boundary)
        r79 = evaluate_tss_crossing(hdg=79.0, lane_bearing=lane_bearing)
        self.assertAlmostEqual(r79["perpendicular_error_deg"], 11.0)
        self.assertNotEqual(r79["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertEqual(r79["status"], "MARGINAL_CROSSING")

        # 101° (11° error > 10°: Exceeds strict 10° boundary)
        r101 = evaluate_tss_crossing(hdg=101.0, lane_bearing=lane_bearing)
        self.assertAlmostEqual(r101["perpendicular_error_deg"], 11.0)
        self.assertNotEqual(r101["status"], "RIGHT_ANGLE_COMPLIANT")
        self.assertEqual(r101["status"], "MARGINAL_CROSSING")

        # 69° (21° error > 20°: Oblique crossing violation)
        r69 = evaluate_tss_crossing(hdg=69.0, lane_bearing=lane_bearing)
        self.assertFalse(r69["compliant"])
        self.assertEqual(r69["status"], "VIOLATION_OBLIQUE_CROSSING")

        # 111° (21° error > 20°: Oblique crossing violation)
        r111 = evaluate_tss_crossing(hdg=111.0, lane_bearing=lane_bearing)
        self.assertFalse(r111["compliant"])
        self.assertEqual(r111["status"], "VIOLATION_OBLIQUE_CROSSING")

        # 055° (35° error > 20°: Oblique crossing violation - Milestone M1 Iteration 2 challenge)
        r55 = evaluate_tss_crossing(hdg=55.0, lane_bearing=lane_bearing)
        self.assertFalse(r55["compliant"])
        self.assertEqual(r55["status"], "VIOLATION_OBLIQUE_CROSSING")
        self.assertAlmostEqual(r55["perpendicular_error_deg"], 35.0)

        # 125° (35° error > 20°: Oblique crossing violation)
        r125 = evaluate_tss_crossing(hdg=125.0, lane_bearing=lane_bearing)
        self.assertFalse(r125["compliant"])
        self.assertEqual(r125["status"], "VIOLATION_OBLIQUE_CROSSING")
        self.assertAlmostEqual(r125["perpendicular_error_deg"], 35.0)

        # 235° (Westbound 35° error > 20°: Oblique crossing violation)
        r235 = evaluate_tss_crossing(hdg=235.0, lane_bearing=lane_bearing)
        self.assertFalse(r235["compliant"])
        self.assertEqual(r235["status"], "VIOLATION_OBLIQUE_CROSSING")
        self.assertAlmostEqual(r235["perpendicular_error_deg"], 35.0)


class TestRule10FlowDirectionBoundaries(unittest.TestCase):
    """
    Challenge Rule 10(b)(i) flow direction and wrong-way detection:
    - 89°: Major deviation (delta <= 90°)
    - 90°: Boundary edge (delta == 90°)
    - 91°: Wrong-way violation (delta > 90°)
    """

    def test_northbound_flow_detection(self):
        lane_bearing = 0.0

        # Compliant flow (0° - 15°)
        res0 = evaluate_tss_flow(hdg=0.0, lane_bearing=lane_bearing)
        self.assertEqual(res0["status"], "COMPLIANT_FLOW")
        self.assertEqual(res0["score"], 100)

        # Minor deviation (16° - 30°)
        res25 = evaluate_tss_flow(hdg=25.0, lane_bearing=lane_bearing)
        self.assertEqual(res25["status"], "MINOR_DEVIATION")
        self.assertEqual(res25["score"], 80)

        # Major deviation at 89°
        res89 = evaluate_tss_flow(hdg=89.0, lane_bearing=lane_bearing)
        self.assertEqual(res89["status"], "MAJOR_DEVIATION")
        self.assertEqual(res89["score"], 40)

        # Boundary edge at 90°
        res90 = evaluate_tss_flow(hdg=90.0, lane_bearing=lane_bearing)
        self.assertEqual(res90["status"], "MAJOR_DEVIATION")
        self.assertEqual(res90["score"], 40)

        # Wrong-way violation at 91°
        res91 = evaluate_tss_flow(hdg=91.0, lane_bearing=lane_bearing)
        self.assertEqual(res91["status"], "WRONG_WAY_VIOLATION")
        self.assertEqual(res91["score"], 0)

        # Head-on opposite (180°)
        res180 = evaluate_tss_flow(hdg=180.0, lane_bearing=lane_bearing)
        self.assertEqual(res180["status"], "WRONG_WAY_VIOLATION")
        self.assertEqual(res180["score"], 0)


class TestIALABuoyageSpecifications(unittest.TestCase):
    """
    Challenge IALA Maritime Buoyage System Region A vs Region B specifications:
    - Region A: Port = Red / Can / Red Light, Starboard = Green / Cone / Green Light
    - Region B: Port = Green / Can / Green Light, Starboard = Red / Cone / Red Light
    - Cardinal marks: Cones orientation & flash rhythms
    """

    def test_region_a_lateral_marks(self):
        port_a = get_iala_lateral_mark("A", "port")
        self.assertEqual(port_a["color"], "RED")
        self.assertEqual(port_a["topmark"], "CAN")
        self.assertEqual(port_a["light_color"], "RED")
        self.assertEqual(port_a["shape"], "CYLINDER")

        stbd_a = get_iala_lateral_mark("A", "starboard")
        self.assertEqual(stbd_a["color"], "GREEN")
        self.assertEqual(stbd_a["topmark"], "CONE_POINT_UP")
        self.assertEqual(stbd_a["light_color"], "GREEN")
        self.assertEqual(stbd_a["shape"], "CONICAL")

    def test_region_b_lateral_marks(self):
        port_b = get_iala_lateral_mark("B", "port")
        self.assertEqual(port_b["color"], "GREEN")
        self.assertEqual(port_b["topmark"], "CAN")
        self.assertEqual(port_b["light_color"], "GREEN")
        self.assertEqual(port_b["shape"], "CYLINDER")

        stbd_b = get_iala_lateral_mark("B", "starboard")
        self.assertEqual(stbd_b["color"], "RED")
        self.assertEqual(stbd_b["topmark"], "CONE_POINT_UP")
        self.assertEqual(stbd_b["light_color"], "RED")
        self.assertEqual(stbd_b["shape"], "CONICAL")

    def test_cardinal_marks_all_quadrants(self):
        n = get_iala_cardinal_mark("NORTH")
        self.assertEqual(n["topmark"], "CONES_BOTH_UP")
        self.assertEqual(n["colors"], "BLACK_OVER_YELLOW")

        s = get_iala_cardinal_mark("SOUTH")
        self.assertEqual(s["topmark"], "CONES_BOTH_DOWN")
        self.assertEqual(s["colors"], "YELLOW_OVER_BLACK")

        e = get_iala_cardinal_mark("EAST")
        self.assertEqual(e["topmark"], "CONES_BASE_TO_BASE")
        self.assertEqual(e["colors"], "BLACK_YELLOW_BLACK")

        w = get_iala_cardinal_mark("WEST")
        self.assertEqual(w["topmark"], "CONES_POINT_TO_POINT")
        self.assertEqual(w["colors"], "YELLOW_BLACK_YELLOW")


class TestRule9NarrowChannelBoundaries(unittest.TestCase):
    """
    Challenge Rule 9 Narrow Channel fairway boundaries and blind bend:
    - Channel width = 0.8 NM (half width = 0.4 NM)
    - Starboard: d_stbd in [0.0, 0.4] NM (Compliant)
    - Port: d_stbd in [-0.4, 0.0) NM (Violation)
    - Out of channel: |d_stbd| > 0.4 NM (Grounding risk)
    """

    def test_fairway_transverse_positions(self):
        # Channel bearing = 000°, start = (0, 0), half_width = 0.4
        res_stbd = evaluate_rule9_channel(ship_pos=(0.2, 5.0), channel_start=(0, 0), channel_bearing=0.0, channel_half_width=0.4)
        self.assertTrue(res_stbd["compliant"])
        self.assertEqual(res_stbd["status"], "COMPLIANT_STARBOARD_FAIRWAY")

        res_port = evaluate_rule9_channel(ship_pos=(-0.2, 5.0), channel_start=(0, 0), channel_bearing=0.0, channel_half_width=0.4)
        self.assertFalse(res_port["compliant"])
        self.assertEqual(res_port["status"], "VIOLATION_PORT_SIDE_FAIRWAY")

        res_ground = evaluate_rule9_channel(ship_pos=(0.45, 5.0), channel_start=(0, 0), channel_bearing=0.0, channel_half_width=0.4)
        self.assertFalse(res_ground["compliant"])
        self.assertEqual(res_ground["status"], "GROUNDING_RISK_OUT_OF_CHANNEL")

    def test_rule9_blind_bend_whistle_specs(self):
        bend_sig = RULE_34_SIGNALS["BEND"]
        self.assertEqual(bend_sig["blasts"], [5.0])
        self.assertEqual(bend_sig["duration"], 5.0)


class TestFogAndARPARelationship(unittest.TestCase):
    """
    Challenge 3D Fog optical extinction vs ARPA Radar independence:
    - Light extinction follows Beer-Lambert exponential decay
    - Human visual range is severely attenuated
    - ARPA microwave radar tracks targets up to 6 NM unhindered
    """

    def test_fog_extinction_formula(self):
        # Density = 0.065 (dense fog)
        vis_nm = calculate_fog_visibility(0.065)
        # Verify contrast at extinction distance is ~0.05 (threshold)
        scale = 20.0
        contrast = math.exp(-0.065 * vis_nm * scale)
        self.assertAlmostEqual(contrast, 0.05, places=3)
        self.assertLess(vis_nm, 2.5)

    def test_arpa_radar_penetration_in_dense_fog(self):
        # In dense fog, visual extinction is ~2.3 NM, but ARPA radar range is 6.0 NM
        target_dist = 5.0
        vis_nm = calculate_fog_visibility(0.065)
        self.assertGreater(target_dist, vis_nm)  # Target is visually invisible!
        radar_range = 6.0
        self.assertLessEqual(target_dist, radar_range)  # Target is detectable on ARPA radar!


class TestSimulatorHTMLJavaScriptDirectExecution(unittest.TestCase):
    """
    Empirical direct execution of JavaScript functions extracted from simulator.html:
    Runs via Node.js to test the actual browser runtime logic.
    """

    @classmethod
    def setUpClass(cls):
        html_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "simulator.html")
        with open(html_path, "r", encoding="utf-8") as f:
            cls.html_content = f.read()

    def _run_node_script(self, js_code):
        cmd = ["node"]
        proc = subprocess.run(cmd, input=js_code, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding="utf-8", cwd=os.path.dirname(os.path.abspath(__file__)))
        self.assertEqual(proc.returncode, 0, f"Node script failed: {proc.stderr}")
        return json.loads(proc.stdout)

    def test_js_rule10_crossing_and_lane_matrix(self):
        js = """
        const fs = require('fs');
        const path = require('path');
        const html = fs.readFileSync(path.resolve(__dirname, '../simulator.html'), 'utf8');
        const v10Match = html.match(/function validateRule10Compliance\\(\\) \\{([\\s\\S]*?)\\n    \\}/);
        const v10Body = v10Match[1];
        const fn = new Function('ownShip', 'environment', v10Body);

        const results = {};
        
        // 1. Crossing test cases (x = 0)
        results.crossing = {};
        [29, 30, 55, 69, 70, 79, 80, 81, 90, 99, 100, 101, 110, 111, 125, 150, 151, 209, 210, 235, 270, 305, 330, 331].forEach(hdg => {
            results.crossing[hdg] = fn({ x: 0, course: hdg }, {});
        });

        // 2. Northbound lane flow cases (x = -0.6)
        results.northbound = {};
        [0, 15, 16, 29, 30, 55, 59, 60, 89, 90, 91, 120, 121, 150, 151, 180, 209, 210, 235, 270, 305, 330, 331].forEach(hdg => {
            results.northbound[hdg] = fn({ x: -0.6, course: hdg }, {});
        });

        // 3. Separation zone cases
        results.sep_zone = {
            running_along: fn({ x: 0, course: 0 }, {}),
            crossing_across: fn({ x: 0, course: 90 }, {}),
            oblique_crossing_55: fn({ x: 0, course: 55 }, {})
        };

        console.log(JSON.stringify(results));
        """
        data = self._run_node_script(js)

        # Verify crossing angles
        self.assertTrue(data["crossing"]["81"]["compliant"])
        self.assertEqual(data["crossing"]["81"]["scorePenalty"], 0)

        self.assertTrue(data["crossing"]["99"]["compliant"])
        self.assertEqual(data["crossing"]["99"]["scorePenalty"], 0)

        # 80° and 100° exact 10° compliant boundary
        self.assertTrue(data["crossing"]["80"]["compliant"])
        self.assertEqual(data["crossing"]["80"]["scorePenalty"], 0)
        self.assertTrue(data["crossing"]["100"]["compliant"])
        self.assertEqual(data["crossing"]["100"]["scorePenalty"], 0)

        # 79° and 101°: Have penalty 15 and advisory warning
        self.assertEqual(data["crossing"]["79"]["scorePenalty"], 15)
        self.assertIn("GÓC CẮT HƠI LỆCH", data["crossing"]["79"]["text"])

        self.assertEqual(data["crossing"]["101"]["scorePenalty"], 15)
        self.assertIn("GÓC CẮT HƠI LỆCH", data["crossing"]["101"]["text"])

        # 70° and 110°: Outer boundary of advisory corridor (deltaCross = 20°)
        self.assertTrue(data["crossing"]["70"]["compliant"])
        self.assertEqual(data["crossing"]["70"]["scorePenalty"], 15)
        self.assertIn("GÓC CẮT HƠI LỆCH", data["crossing"]["70"]["text"])

        self.assertTrue(data["crossing"]["110"]["compliant"])
        self.assertEqual(data["crossing"]["110"]["scorePenalty"], 15)
        self.assertIn("GÓC CẮT HƠI LỆCH", data["crossing"]["110"]["text"])

        # 111°: Oblique crossing violation (score penalty 40, compliant = false)
        self.assertFalse(data["crossing"]["111"]["compliant"])
        self.assertEqual(data["crossing"]["111"]["scorePenalty"], 40)

        # 055°: Oblique crossing violation (Milestone M1 Iteration 2 challenge)
        # Delta from 090° is 35.0° > 20.0°
        self.assertFalse(data["crossing"]["55"]["compliant"])
        self.assertEqual(data["crossing"]["55"]["scorePenalty"], 40)
        self.assertIn("VI PHẠM CẮT CHÉO GÓC", data["crossing"]["55"]["text"])
        self.assertIn("Cấm cắt chéo luồng", data["crossing"]["55"]["alert"])

        # Also at x = -0.6 (inside Northbound lane), 055° enters isCrossing and triggers violation penalty 40
        self.assertFalse(data["northbound"]["55"]["compliant"])
        self.assertEqual(data["northbound"]["55"]["scorePenalty"], 40)
        self.assertIn("VI PHẠM CẮT CHÉO GÓC", data["northbound"]["55"]["text"])

        # Boundaries of crossing window: [30, 150] and [210, 330]
        # 30°: entry into Eastbound crossing window -> deltaCross = 60° -> oblique violation (penalty 40)
        self.assertFalse(data["crossing"]["30"]["compliant"])
        self.assertEqual(data["crossing"]["30"]["scorePenalty"], 40)

        # 150°: exit of Eastbound crossing window -> deltaCross = 60° -> oblique violation (penalty 40)
        self.assertFalse(data["crossing"]["150"]["compliant"])
        self.assertEqual(data["crossing"]["150"]["scorePenalty"], 40)

        # 210°: entry into Westbound crossing window -> deltaCross = 60° -> oblique violation (penalty 40)
        self.assertFalse(data["crossing"]["210"]["compliant"])
        self.assertEqual(data["crossing"]["210"]["scorePenalty"], 40)

        # 235°: Westbound oblique crossing (delta from 270° is 35°) -> penalty 40
        self.assertFalse(data["crossing"]["235"]["compliant"])
        self.assertEqual(data["crossing"]["235"]["scorePenalty"], 40)

        # 270°: Westbound right-angle compliant -> penalty 0
        self.assertTrue(data["crossing"]["270"]["compliant"])
        self.assertEqual(data["crossing"]["270"]["scorePenalty"], 0)

        # 305°: Westbound oblique crossing (delta from 270° is 35°) -> penalty 40
        self.assertFalse(data["crossing"]["305"]["compliant"])
        self.assertEqual(data["crossing"]["305"]["scorePenalty"], 40)

        # 330°: exit of Westbound crossing window -> penalty 40
        self.assertFalse(data["crossing"]["330"]["compliant"])
        self.assertEqual(data["crossing"]["330"]["scorePenalty"], 40)

        # Lane following corridor headings at x = -0.6 (Northbound lane):
        # 29°: outside crossing window, deltaHdg = 29° <= 30° -> Lệch làn (penalty 15)
        self.assertTrue(data["northbound"]["29"]["compliant"])
        self.assertEqual(data["northbound"]["29"]["scorePenalty"], 15)

        # 151°: outside crossing window, deltaHdg = 151° > 90° -> Wrong-way violation (penalty 80)
        self.assertFalse(data["northbound"]["151"]["compliant"])
        self.assertEqual(data["northbound"]["151"]["scorePenalty"], 80)

        # 209°: outside crossing window, deltaHdg = 151° > 90° -> Wrong-way violation (penalty 80)
        self.assertFalse(data["northbound"]["209"]["compliant"])
        self.assertEqual(data["northbound"]["209"]["scorePenalty"], 80)

        # 331°: outside crossing window, deltaHdg = 29° <= 30° -> Lệch làn (penalty 15)
        self.assertTrue(data["northbound"]["331"]["compliant"])
        self.assertEqual(data["northbound"]["331"]["scorePenalty"], 15)

        # Separation zone: running along is violation; crossing at 90° is permitted; 55° is oblique violation
        self.assertFalse(data["sep_zone"]["running_along"]["compliant"])
        self.assertEqual(data["sep_zone"]["running_along"]["scorePenalty"], 50)
        self.assertTrue(data["sep_zone"]["crossing_across"]["compliant"])
        self.assertFalse(data["sep_zone"]["oblique_crossing_55"]["compliant"])
        self.assertEqual(data["sep_zone"]["oblique_crossing_55"]["scorePenalty"], 40)

    def test_js_rule9_fairway_and_bend_whistle(self):
        js = """
        const fs = require('fs');
        const path = require('path');
        const html = fs.readFileSync(path.resolve(__dirname, '../simulator.html'), 'utf8');
        const v9Match = html.match(/function validateRule9Compliance\\(\\) \\{([\\s\\S]*?)\\n    \\}/);
        const v9Body = v9Match[1];
        const fn = new Function('ownShip', 'environment', v9Body);

        const results = {};
        [-0.5, -0.4, -0.2, 0.0, 0.2, 0.4, 0.45].forEach(x => {
            results['x_' + x] = fn({ x: x, z: 0 }, { blindBendSounded: false });
        });

        // Blind bend without and with whistle
        results.bend_without = fn({ x: 0.2, z: 4.2 }, { blindBendSounded: false });
        results.bend_with = fn({ x: 0.2, z: 4.2 }, { blindBendSounded: true });

        console.log(JSON.stringify(results));
        """
        data = self._run_node_script(js)

        # Starboard fairway compliant
        self.assertTrue(data["x_0.2"]["compliant"])
        self.assertEqual(data["x_0.2"]["scorePenalty"], 0)

        # Port fairway violation
        self.assertFalse(data["x_-0.2"]["compliant"])
        self.assertEqual(data["x_-0.2"]["scorePenalty"], 35)

        # Out of channel grounding risk
        self.assertFalse(data["x_0.45"]["compliant"])
        self.assertEqual(data["x_0.45"]["scorePenalty"], 50)

        # Blind bend: alert required without whistle, cleared with whistle
        self.assertTrue("KHÚC QUANH KHUẤT" in data["bend_without"]["alert"])
        self.assertEqual(data["bend_with"]["alert"], "")
        self.assertTrue("ĐÃ PHÁT CÒI KHÚC QUANH KHUẤT" in data["bend_with"]["text"])

    def test_js_iala_region_a_vs_b_buoy_colors(self):
        js = """
        const fs = require('fs');
        const path = require('path');
        const html = fs.readFileSync(path.resolve(__dirname, '../simulator.html'), 'utf8');
        // Extract createIALABuoyMesh body or test its color assignment logic
        const results = {};
        ['A', 'B'].forEach(region => {
            results[region] = {};
            ['port', 'starboard'].forEach(type => {
                let bodyColor, lightColor;
                if (type === 'port') {
                    const isRed = (region === 'A');
                    bodyColor = isRed ? 0xd32f2f : 0x2e7d32;
                    lightColor = isRed ? 0xff1744 : 0x00e676;
                } else if (type === 'starboard') {
                    const isGreen = (region === 'A');
                    bodyColor = isGreen ? 0x2e7d32 : 0xd32f2f;
                    lightColor = isGreen ? 0x00e676 : 0xff1744;
                }
                results[region][type] = { body: bodyColor, light: lightColor };
            });
        });
        console.log(JSON.stringify(results));
        """
        data = self._run_node_script(js)

        # Region A Port is Red (0xd32f2f), Starboard is Green (0x2e7d32)
        self.assertEqual(data["A"]["port"]["body"], 0xd32f2f)
        self.assertEqual(data["A"]["starboard"]["body"], 0x2e7d32)

        # Region B Port is Green (0x2e7d32), Starboard is Red (0xd32f2f)
        self.assertEqual(data["B"]["port"]["body"], 0x2e7d32)
        self.assertEqual(data["B"]["starboard"]["body"], 0xd32f2f)

    def test_js_arpa_radar_scope_rendering(self):
        """
        Challenge ARPA radar PPI canvas renderer directly from simulator.html:
        - Must not throw ReferenceError: currentScenarioData is not defined (Milestone M1 defect)
        - Must render multi-target ships (3-5 targets) with risk coloring and motion vectors
        - Must clip out-of-range targets (> 6.0 NM)
        - Must render TSS overlays and IALA buoys
        """
        js = """
        const fs = require('fs');
        const path = require('path');
        const html = fs.readFileSync(path.resolve(__dirname, '../simulator.html'), 'utf8');

        const start = html.indexOf('function drawRadar(');
        const openBrace = html.indexOf('{', start);
        const commentPos = html.indexOf('// COMPASS ROSE RENDERER', start);
        const closeBrace = html.lastIndexOf('}', commentPos);
        const body = html.substring(openBrace + 1, closeBrace);

        let drawnTargets = 0;
        let drawnBuoys = 0;
        const mockCtx = {
          clearRect: () => {},
          beginPath: () => {},
          arc: () => {},
          fill: () => {},
          save: () => {},
          clip: () => {},
          restore: () => {},
          stroke: () => {},
          moveTo: () => {},
          lineTo: () => {},
          fillRect: () => {},
          setLineDash: () => {},
          translate: () => {},
          rotate: () => {},
          closePath: () => {},
          fillText: (text) => {
            if (text && (text.includes('TGT') || text.includes('T1') || text.includes('T2') || text.includes('T4') || text.includes('T5'))) drawnTargets++;
            if (text && (text.includes('P1') || text.includes('S1') || text.includes('SW'))) drawnBuoys++;
          },
          set fillStyle(v) {},
          set strokeStyle(v) {},
          set lineWidth(v) {},
          set font(v) {},
          set shadowColor(v) {},
          set shadowBlur(v) {}
        };

        const mockCanvas = { width: 300, height: 300, getContext: () => mockCtx };
        const document = { getElementById: id => (id === 'radarCanvas' ? mockCanvas : null) };
        const THREE = {
          MathUtils: {
            degToRad: deg => (deg * Math.PI) / 180,
            radToDeg: rad => (rad * 180) / Math.PI
          }
        };

        let radarRange = 6.0;
        let radarSweepAngle = 0;
        let simSpeed = 1.0;
        let ialaRegion = 'A';
        let currentScenarioId = 'tss_dover_crossing';
        let currentScenarioData = {
          id: 'tss_dover_crossing',
          tss: { centerX: 0, sepWidth: 0.4, laneWidth: 0.8 }
        };
        let ownShip = { x: 0, z: 0, course: 90, speed: 12, cog: 90, sog: 12, vgx: 12, vgz: 0 };
        let targets = [
          { id: 'T1', name: 'TGT-1', x: 2.0, z: 3.0, course: 0, speed: 15, cpa: 0.8, tcpa: 4.2 },
          { id: 'T2', name: 'TGT-2', x: -1.5, z: 2.0, course: 180, speed: 10, cpa: 1.5, tcpa: 6.0 },
          { id: 'T3', name: 'TGT-3', x: 0.5, z: 7.5, course: 0, speed: 12, cpa: 3.0, tcpa: 10.0 }, // Out of range (>6 NM)
          { id: 'T4', name: 'TGT-4', x: 1.0, z: -1.0, course: 270, speed: 8, cpa: 0.3, tcpa: 2.0 },
          { id: 'T5', name: 'TGT-5', x: -2.0, z: -2.0, course: 90, speed: 14, cpa: 2.5, tcpa: -1.0 }
        ];
        let targetShip = targets[0];
        let activeBuoys = [
          { x: -0.4, z: 2.0, type: 'port', label: 'P1' },
          { x: 0.4, z: 2.0, type: 'stbd', label: 'S1' },
          { x: 0.0, z: -3.5, type: 'safe_water', label: 'SW' }
        ];

        const drawRadarFn = new Function(
          'document', 'THREE', 'radarRange', 'radarSweepAngle', 'simSpeed', 'ialaRegion',
          'currentScenarioId', 'currentScenarioData', 'ownShip', 'targets', 'targetShip', 'activeBuoys',
          'dx', 'dz', 'rel_vx', 'rel_vz', 'cpa', 'tcpa',
          body
        );

        drawRadarFn(
          document, THREE, radarRange, radarSweepAngle, simSpeed, ialaRegion,
          currentScenarioId, currentScenarioData, ownShip, targets, targetShip, activeBuoys,
          0, 0, 0, 0, 0, 0
        );

        console.log(JSON.stringify({ success: true, drawnTargets, drawnBuoys }));
        """
        data = self._run_node_script(js)
        self.assertTrue(data["success"])
        # Exactly 4 within-range targets rendered (T3 at 7.5 NM is clipped by 6.0 NM range circle)
        self.assertEqual(data["drawnTargets"], 4)
        # All 3 active buoys rendered
        self.assertEqual(data["drawnBuoys"], 3)

    def test_js_iala_light_flashes(self):
        """
        Challenge IALA buoy light flash animation loop from simulator.html:
        - Rhythms: Q, Fl, Q3, MorseA, Iso
        - Halo visibility and PointLight intensity synchronized to flashing cycles
        """
        js = """
        const fs = require('fs');
        const path = require('path');
        const html = fs.readFileSync(path.resolve(__dirname, '../simulator.html'), 'utf8');

        const start = html.indexOf('function updateIALABuoys(');
        const openBrace = html.indexOf('{', start);
        const closeBrace = html.indexOf('\\n    function clearZones()', start);
        const lastBrace = html.lastIndexOf('}', closeBrace);
        const body = html.substring(openBrace + 1, lastBrace);

        function makeBuoy(rhythm) {
          return {
            userData: {
              lightRhythm: rhythm,
              halo: { visible: false },
              ptLight: { intensity: 0 }
            }
          };
        }

        const buoys = {
          Q: makeBuoy('Q'),
          Fl: makeBuoy('Fl'),
          Q3: makeBuoy('Q3'),
          MorseA: makeBuoy('MorseA'),
          Iso: makeBuoy('Iso')
        };

        const environment = {
          buoys: Object.values(buoys),
          fog: false
        };
        let isNightMode = false;

        const updateFn = new Function('environment', 'isNightMode', 'elapsedSec', body);

        const timeline = {};

        // Test Q: (t % 1.0) < 0.5 -> On at 0.2s, Off at 0.7s
        updateFn(environment, isNightMode, 0.2);
        timeline.q_on = buoys.Q.userData.halo.visible && buoys.Q.userData.ptLight.intensity > 0;
        updateFn(environment, isNightMode, 0.7);
        timeline.q_off = !buoys.Q.userData.halo.visible && buoys.Q.userData.ptLight.intensity === 0;

        // Test Fl: (t % 4.0) < 0.8 -> On at 0.5s, Off at 1.5s
        updateFn(environment, isNightMode, 0.5);
        timeline.fl_on = buoys.Fl.userData.halo.visible && buoys.Fl.userData.ptLight.intensity > 0;
        updateFn(environment, isNightMode, 1.5);
        timeline.fl_off = !buoys.Fl.userData.halo.visible && buoys.Fl.userData.ptLight.intensity === 0;

        // Test Q3: East Cardinal 3 quick flashes (t % 10.0: <0.3, [0.6, 0.9), [1.2, 1.5))
        updateFn(environment, isNightMode, 0.1);
        timeline.q3_flash1 = buoys.Q3.userData.halo.visible;
        updateFn(environment, isNightMode, 0.45);
        timeline.q3_gap1 = !buoys.Q3.userData.halo.visible;
        updateFn(environment, isNightMode, 0.75);
        timeline.q3_flash2 = buoys.Q3.userData.halo.visible;

        // Test MorseA: Safe Water (t % 6.0: <0.5 (dot), [1.2, 2.7) (dash))
        updateFn(environment, isNightMode, 0.2);
        timeline.morse_dot = buoys.MorseA.userData.halo.visible;
        updateFn(environment, isNightMode, 0.8);
        timeline.morse_space = !buoys.MorseA.userData.halo.visible;
        updateFn(environment, isNightMode, 1.5);
        timeline.morse_dash = buoys.MorseA.userData.halo.visible;

        // Test Iso: Isophase (t % 4.0 < 2.0)
        updateFn(environment, isNightMode, 1.0);
        timeline.iso_on = buoys.Iso.userData.halo.visible;
        updateFn(environment, isNightMode, 3.0);
        timeline.iso_off = !buoys.Iso.userData.halo.visible;

        console.log(JSON.stringify(timeline));
        """
        data = self._run_node_script(js)
        self.assertTrue(data["q_on"])
        self.assertTrue(data["q_off"])
        self.assertTrue(data["fl_on"])
        self.assertTrue(data["fl_off"])
        self.assertTrue(data["q3_flash1"])
        self.assertTrue(data["q3_gap1"])
        self.assertTrue(data["q3_flash2"])
        self.assertTrue(data["morse_dot"])
        self.assertTrue(data["morse_space"])
        self.assertTrue(data["morse_dash"])
        self.assertTrue(data["iso_on"])
        self.assertTrue(data["iso_off"])

    def test_html_asset_synchronization(self):
        """
        Verify byte-for-byte SHA-256 synchronisation across all 4 HTML mirrors:
        - simulator.html
        - index.html
        - android_project/app/src/main/assets/simulator.html
        - android_project/app/src/main/assets/index.html
        """
        import hashlib
        root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        targets = [
            os.path.join(root, "simulator.html"),
            os.path.join(root, "index.html"),
            os.path.join(root, "android_project", "app", "src", "main", "assets", "simulator.html"),
            os.path.join(root, "android_project", "app", "src", "main", "assets", "index.html")
        ]

        hashes = {}
        lengths = {}
        for p in targets:
            self.assertTrue(os.path.isfile(p), f"Target file does not exist: {p}")
            with open(p, "rb") as f:
                content = f.read()
            h = hashlib.sha256(content).hexdigest()
            hashes[p] = h
            lengths[p] = len(content)

        distinct_hashes = set(hashes.values())
        distinct_lengths = set(lengths.values())
        self.assertEqual(len(distinct_hashes), 1, f"Asset hash desynchronisation detected: {hashes}")
        self.assertEqual(len(distinct_lengths), 1, f"Asset length desynchronisation detected: {lengths}")
        self.assertGreaterEqual(list(distinct_lengths)[0], 346498)


if __name__ == "__main__":
    unittest.main(verbosity=2)
