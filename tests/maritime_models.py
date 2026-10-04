"""
Authoritative Maritime Mathematics, Rules & System Models for COLREGS-3D.
Provides ground-truth oracles, specifications, and validators for Tiers 1-4.
"""

import math
import json
import base64
import numpy as np
from typing import Dict, List, Tuple, Any, Optional

# Constants
NM_IN_METERS = 1852.0
THREE_JS_SCALE = 20.0  # 1 NM = 20 Three.js units
COLLISION_DISTANCE_NM = 0.16
SAFE_PASSING_DISTANCE_NM = 1.0


# ---------------------------------------------------------------------------
# F1.6: Vector Mechanics (Water Velocity, Current Drift, Wind Leeway, COG/SOG)
# ---------------------------------------------------------------------------
def velocity_water(hdg: float, stw: float) -> np.ndarray:
    """
    Calculate water velocity vector [vx, vy] (knots).
    000° is North (+Y), 090° is East (+X).
    """
    rad = math.radians(hdg % 360)
    return np.array([stw * math.sin(rad), stw * math.cos(rad)], dtype=float)


def vector_current(set_dir: float, drift: float) -> np.ndarray:
    """
    Current vector [vx, vy] in knots.
    set_dir: Direction current flows towards (degrees true).
    drift: Current speed (knots).
    """
    rad = math.radians(set_dir % 360)
    return np.array([drift * math.sin(rad), drift * math.cos(rad)], dtype=float)


def vector_wind_leeway(hdg: float, stw: float, wind_from: float, wind_speed: float, k_leeway: float = 0.04) -> np.ndarray:
    """
    Aerodynamic leeway vector [vx, vy] (knots).
    wind_from: Direction wind blows from (degrees true).
    Pushes vessel downwind (towards wind_from + 180°).
    """
    downwind_dir = (wind_from + 180.0) % 360.0
    downwind_rad = math.radians(downwind_dir)
    speed = k_leeway * wind_speed
    return np.array([speed * math.sin(downwind_rad), speed * math.cos(downwind_rad)], dtype=float)



def calculate_ground_motion(
    hdg: float, stw: float,
    current_set: float = 0.0, current_drift: float = 0.0,
    wind_dir: float = 0.0, wind_spd: float = 0.0, k_leeway: float = 0.04
) -> Tuple[np.ndarray, float, float, float]:
    """
    Vector summation: V_g = V_w + V_current + V_leeway.
    Returns: (V_g, SOG, COG, Crab_Angle)
    """
    v_w = velocity_water(hdg, stw)
    v_c = vector_current(current_set, current_drift)
    v_l = vector_wind_leeway(hdg, stw, wind_dir, wind_spd, k_leeway)
    v_g = v_w + v_c + v_l

    sog = float(np.linalg.norm(v_g))
    if sog < 1e-6:
        cog = hdg
        crab = 0.0
    else:
        cog = (math.degrees(math.atan2(v_g[0], v_g[1])) + 360.0) % 360.0
        crab = ((cog - hdg + 180.0) % 360.0) - 180.0

    return v_g, sog, cog, crab


# ---------------------------------------------------------------------------
# F1.1: Multi-Target CPA/TCPA & Collision Engine
# ---------------------------------------------------------------------------
def calculate_cpa_tcpa_single(
    p_own: np.ndarray, v_own: np.ndarray,
    p_tgt: np.ndarray, v_tgt: np.ndarray
) -> Dict[str, float]:
    """Compute relative distance, bearing, relative speed, TCPA, and CPA."""
    rel_pos = p_tgt - p_own
    rel_vel = v_tgt - v_own
    current_dist = float(np.linalg.norm(rel_pos))
    rel_speed = float(np.linalg.norm(rel_vel))

    bearing = (math.degrees(math.atan2(rel_pos[0], rel_pos[1])) + 360.0) % 360.0

    rel_vel_sq = float(np.dot(rel_vel, rel_vel))
    if rel_vel_sq < 1e-9:
        return {
            "dist": current_dist,
            "bearing": bearing,
            "rel_speed": rel_speed,
            "tcpa": 0.0,
            "cpa": current_dist
        }

    dot_product = float(np.dot(rel_pos, rel_vel))
    tcpa = -dot_product / rel_vel_sq  # in hours

    if tcpa <= 0.0:
        cpa = current_dist
    else:
        cpa_pos = rel_pos + rel_vel * tcpa
        cpa = float(np.linalg.norm(cpa_pos))

    return {
        "dist": current_dist,
        "bearing": bearing,
        "rel_speed": rel_speed,
        "tcpa": tcpa * 60.0,  # in minutes
        "cpa": cpa
    }


def evaluate_multi_target_kinematics(
    own_pos: np.ndarray, own_vel: np.ndarray,
    targets: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """Evaluates CPA/TCPA and risk level for 3 to 5 targets concurrently."""
    results = []
    for tgt in targets:
        p_tgt = np.array([tgt["x"], tgt["z"]], dtype=float)
        v_tgt = velocity_water(tgt["course"], tgt["speed"])
        telemetry = calculate_cpa_tcpa_single(own_pos, own_vel, p_tgt, v_tgt)

        cpa = telemetry["cpa"]
        dist = telemetry["dist"]
        tcpa = telemetry["tcpa"]

        if dist <= COLLISION_DISTANCE_NM:
            status = "COLLISION"
        elif cpa < 0.5 and tcpa > 0:
            status = "CRITICAL"
        elif cpa < 1.0 and tcpa > 0:
            status = "WARNING"
        elif tcpa <= 0 and dist >= SAFE_PASSING_DISTANCE_NM:
            status = "SAFE_PASSED"
        else:
            status = "SAFE"

        telemetry["id"] = tgt.get("id", "UNKNOWN")
        telemetry["name"] = tgt.get("name", "Target")
        telemetry["status"] = status
        results.append(telemetry)
    return results


# ---------------------------------------------------------------------------
# F1.2: Rule 9 Narrow Channel Navigation
# ---------------------------------------------------------------------------
def evaluate_rule9_channel(
    ship_pos: np.ndarray,
    channel_start: np.ndarray,
    channel_bearing: float,
    channel_half_width: float
) -> Dict[str, Any]:
    """
    Evaluates Rule 9 fairway keeping:
    - Along-track distance.
    - Cross-track distance: d_stbd > 0 indicates starboard fairway; < 0 indicates port fairway (violation).
    """
    dx = ship_pos[0] - channel_start[0]
    dy = ship_pos[1] - channel_start[1]
    rad = math.radians(channel_bearing % 360)
    u_along = np.array([math.sin(rad), math.cos(rad)])
    u_stbd = np.array([math.cos(rad), -math.sin(rad)])

    d_along = dx * u_along[0] + dy * u_along[1]
    d_stbd = dx * u_stbd[0] + dy * u_stbd[1]

    if abs(d_stbd) > channel_half_width:
        status = "GROUNDING_RISK_OUT_OF_CHANNEL"
        compliant = False
    elif d_stbd >= 0:
        status = "COMPLIANT_STARBOARD_FAIRWAY"
        compliant = True
    else:
        status = "VIOLATION_PORT_SIDE_FAIRWAY"
        compliant = False

    return {
        "d_along": float(d_along),
        "d_stbd": float(d_stbd),
        "status": status,
        "compliant": compliant
    }


# ---------------------------------------------------------------------------
# F1.3: Rule 10 TSS Verification
# ---------------------------------------------------------------------------
def evaluate_tss_flow(hdg: float, lane_bearing: float) -> Dict[str, Any]:
    """Rule 10(b)(i): Proceed in general direction of traffic flow."""
    delta = abs(((hdg - lane_bearing + 180.0) % 360.0) - 180.0)
    if delta <= 15.0:
        status = "COMPLIANT_FLOW"
        score = 100
    elif delta <= 30.0:
        status = "MINOR_DEVIATION"
        score = 80
    elif delta <= 90.0:
        status = "MAJOR_DEVIATION"
        score = 40
    else:
        status = "WRONG_WAY_VIOLATION"
        score = 0
    return {"delta_deg": delta, "status": status, "score": score}


def evaluate_tss_crossing(hdg: float, lane_bearing: float) -> Dict[str, Any]:
    """Rule 10(c): Cross as nearly as practicable at right angles."""
    perp1 = (lane_bearing + 90.0) % 360.0
    perp2 = (lane_bearing - 90.0) % 360.0
    err1 = abs(((hdg - perp1 + 180.0) % 360.0) - 180.0)
    err2 = abs(((hdg - perp2 + 180.0) % 360.0) - 180.0)
    min_err = min(err1, err2)

    if min_err <= 10.0:
        status = "RIGHT_ANGLE_COMPLIANT"
        compliant = True
    elif min_err <= 20.0:
        status = "MARGINAL_CROSSING"
        compliant = True
    else:
        status = "VIOLATION_OBLIQUE_CROSSING"
        compliant = False
    return {"perpendicular_error_deg": min_err, "status": status, "compliant": compliant}


def evaluate_tss_separation_zone(d_stbd: float, sep_width: float, is_crossing: bool = False) -> Dict[str, Any]:
    """Rule 10(e): Separation zone intrusion check."""
    half_sep = sep_width / 2.0
    inside = abs(d_stbd) <= half_sep
    if inside and not is_crossing:
        return {"inside_zone": True, "violation": True, "status": "VIOLATION_SEPARATION_ZONE_INTRUSION"}
    elif inside and is_crossing:
        return {"inside_zone": True, "violation": False, "status": "AUTHORIZED_CROSSING"}
    return {"inside_zone": False, "violation": False, "status": "CLEAR_OF_SEPARATION_ZONE"}


# ---------------------------------------------------------------------------
# F1.4: IALA Buoyage Specifications (Regions A & B)
# ---------------------------------------------------------------------------
def get_iala_lateral_mark(region: str, mark_type: str) -> Dict[str, str]:
    """Returns official IALA lateral mark specification."""
    region = region.upper()
    mark_type = mark_type.lower()
    if region == "A":
        if mark_type == "port":
            return {"color": "RED", "topmark": "CAN", "light_color": "RED", "shape": "CYLINDER"}
        elif mark_type == "starboard":
            return {"color": "GREEN", "topmark": "CONE_POINT_UP", "light_color": "GREEN", "shape": "CONICAL"}
    elif region == "B":
        if mark_type == "port":
            return {"color": "GREEN", "topmark": "CAN", "light_color": "GREEN", "shape": "CYLINDER"}
        elif mark_type == "starboard":
            return {"color": "RED", "topmark": "CONE_POINT_UP", "light_color": "RED", "shape": "CONICAL"}
    raise ValueError(f"Unknown IALA combination: region {region}, type {mark_type}")


def get_iala_cardinal_mark(quadrant: str) -> Dict[str, str]:
    """Returns official IALA cardinal mark specifications (identical in Regions A & B)."""
    quad = quadrant.upper()
    specs = {
        "NORTH": {"topmark": "CONES_BOTH_UP", "colors": "BLACK_OVER_YELLOW", "light": "WHITE_Q_OR_VQ"},
        "EAST": {"topmark": "CONES_BASE_TO_BASE", "colors": "BLACK_YELLOW_BLACK", "light": "WHITE_Q3_10S"},
        "SOUTH": {"topmark": "CONES_BOTH_DOWN", "colors": "YELLOW_OVER_BLACK", "light": "WHITE_Q6_LFL15S"},
        "WEST": {"topmark": "CONES_POINT_TO_POINT", "colors": "YELLOW_BLACK_YELLOW", "light": "WHITE_Q9_15S"}
    }
    if quad not in specs:
        raise ValueError(f"Unknown cardinal quadrant: {quad}")
    return specs[quad]


# ---------------------------------------------------------------------------
# F1.5: 3D Fog & Restricted Visibility (Rule 19)
# ---------------------------------------------------------------------------
def calculate_fog_visibility(fog_density: float) -> float:
    """
    Computes visual extinction distance (NM) in THREE.FogExp2.
    Contrast threshold: e^(-density * distance * 20) <= 0.05.
    distance_units = -ln(0.05) / density
    distance_NM = distance_units / 20.0
    """
    if fog_density <= 0:
        return 50.0  # Clear weather visual horizon
    dist_units = -math.log(0.05) / fog_density
    return dist_units / THREE_JS_SCALE


# ---------------------------------------------------------------------------
# F2.1, F2.2, F2.3, F2.4: Sound Signals & Light Timing Engine
# ---------------------------------------------------------------------------
def get_whistle_frequency_band(vessel_length_m: float) -> Tuple[float, float]:
    """Annex III Whistle fundamental frequency bands."""
    if vessel_length_m >= 200.0:
        return (70.0, 200.0)
    elif vessel_length_m >= 75.0:
        return (130.0, 350.0)
    else:
        return (250.0, 700.0)


RULE_34_SIGNALS = {
    "STARBOARD": {"blasts": [1.0], "total_sound": 1.0, "duration": 1.0, "flashes": 1},
    "PORT": {"blasts": [1.0, -1.0, 1.0], "total_sound": 2.0, "duration": 3.0, "flashes": 2},
    "ASTERN": {"blasts": [1.0, -1.0, 1.0, -1.0, 1.0], "total_sound": 3.0, "duration": 5.0, "flashes": 3},
    "DANGER": {"blasts": [0.6, -0.4] * 5, "total_sound": 3.0, "duration": 5.0, "flashes": 5},
    "OVERTAKE_STBD": {"blasts": [5.0, -1.0, 5.0, -1.0, 1.0], "total_sound": 11.0, "duration": 13.0, "flashes": 0},
    "OVERTAKE_PORT": {"blasts": [5.0, -1.0, 5.0, -1.0, 1.0, -1.0, 1.0], "total_sound": 12.0, "duration": 15.0, "flashes": 0},
    "OVERTAKE_AGREE": {"blasts": [5.0, -1.0, 1.0, -1.0, 5.0, -1.0, 1.0], "total_sound": 12.0, "duration": 15.0, "flashes": 0},
    "BEND": {"blasts": [5.0], "total_sound": 5.0, "duration": 5.0, "flashes": 0}
}


def evaluate_rule35_fog_signal(stw: float) -> Dict[str, Any]:
    """Rule 35(a) vs 35(b) automatic fog signals."""
    if stw > 0.2:
        return {
            "rule": "Rule 35(a)",
            "mode": "MAKING_WAY",
            "interval_sec": 120,
            "blasts": [5.0],
            "description": "1 prolonged blast every 2 minutes"
        }
    else:
        return {
            "rule": "Rule 35(b)",
            "mode": "STOPPED",
            "interval_sec": 120,
            "blasts": [5.0, -2.0, 5.0],
            "description": "2 prolonged blasts separated by 2 seconds every 2 minutes"
        }


def calculate_spatial_audio_attenuation(distance_nm: float, ref_distance_nm: float = 0.75, max_distance_nm: float = 2.0) -> float:
    """Computes inverse distance attenuation for 3D sound."""
    if distance_nm <= ref_distance_nm:
        return 1.0
    if distance_nm >= max_distance_nm:
        return 0.0
    return ref_distance_nm / distance_nm


# ---------------------------------------------------------------------------
# F3.1, F3.2: VDR Telemetry Buffer & Replay Engine
# ---------------------------------------------------------------------------
class VDRCircularBuffer:
    """Fixed-capacity 1,800-frame (30 minute) 1Hz telemetry buffer."""
    def __init__(self, capacity: int = 1800):
        self.capacity = capacity
        self.buffer: List[Optional[Dict[str, Any]]] = [None] * capacity
        self.head = 0
        self.count = 0

    def record_frame(self, frame: Dict[str, Any]):
        self.buffer[self.head] = frame
        self.head = (self.head + 1) % self.capacity
        if self.count < self.capacity:
            self.count += 1

    def get_history(self) -> List[Dict[str, Any]]:
        if self.count < self.capacity:
            return [f for f in self.buffer[:self.count] if f is not None]
        # Full circular buffer: unwind from oldest to newest
        return [self.buffer[(self.head + i) % self.capacity] for i in range(self.capacity)]

    def seek_to_second(self, target_sec: int) -> Optional[Dict[str, Any]]:
        history = self.get_history()
        for f in history:
            if f and f.get("t") == target_sec:
                return f
        return history[-1] if history else None


# ---------------------------------------------------------------------------
# F3.3: Client-Side PDF Certificate Specifications
# ---------------------------------------------------------------------------
def validate_certificate_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Validates certificate data payload for ISO A4 rendering."""
    required = ["candidate_name", "scenario_name", "safety_score", "min_cpa"]
    for field in required:
        if field not in data:
            return {"valid": False, "error": f"Missing field: {field}"}

    score = data["safety_score"]
    min_cpa = data["min_cpa"]
    has_collision = data.get("has_collided", False)

    passed = (score >= 70) and (min_cpa >= 1.0) and (not has_collision)
    return {
        "valid": True,
        "passed": passed,
        "format": "ISO_A4_PORTRAIT",
        "dimensions_mm": (210, 297),
        "standard": "STCW_A_II_1"
    }


# ---------------------------------------------------------------------------
# F4.1, F4.2: Instructor LMS & QR / PIN Schema Engine
# ---------------------------------------------------------------------------
def encode_compact_scenario(scenario: Dict[str, Any]) -> str:
    """Serializes scenario into compact JSON format (<150 chars)."""
    compact = {
        "v": 1,
        "id": scenario["id"][:8],
        "own": [round(scenario["own"]["x"], 2), round(scenario["own"]["z"], 2), int(scenario["own"]["course"]), round(scenario["own"]["speed"], 1)],
        "tgts": [
            [t["id"][:4], t["type"][0], round(t["x"], 2), round(t["z"], 2), int(t["course"]), round(t["speed"], 1)]
            for t in scenario.get("targets", [])
        ],
        "env": [
            int(scenario.get("environment", {}).get("fog", 0)),
            int(scenario.get("environment", {}).get("wind", {}).get("dir", 0)),
            int(scenario.get("environment", {}).get("wind", {}).get("spd", 0))
        ]
    }
    return json.dumps(compact, separators=(',', ':'))


def decode_compact_scenario(compact_str: str) -> Dict[str, Any]:
    """Decodes compact scenario JSON."""
    data = json.loads(compact_str)
    own = data["own"]
    tgts = []
    for t in data["tgts"]:
        tgts.append({
            "id": t[0],
            "type_code": t[1],
            "x": float(t[2]),
            "z": float(t[3]),
            "course": float(t[4]),
            "speed": float(t[5])
        })
    return {
        "version": data["v"],
        "id": data["id"],
        "own": {"x": own[0], "z": own[1], "course": own[2], "speed": own[3]},
        "targets": tgts,
        "env": {"fog": bool(data["env"][0]), "wind_dir": data["env"][1], "wind_spd": data["env"][2]}
    }


# ---------------------------------------------------------------------------
# F4.3: Leaderboard Scoring Oracle
# ---------------------------------------------------------------------------
def compute_total_eval_score(quiz_score: int, navigation_score: int, min_cpa: float, rule_violations: int = 0) -> int:
    """Calculates combined classroom assessment score (0 - 100)."""
    # 40% Quiz theory, 60% Navigation practical
    score = 0.4 * quiz_score + 0.6 * navigation_score
    if min_cpa < 0.5:
        score -= 30
    elif min_cpa < 1.0:
        score -= 15
    score -= rule_violations * 20
    return int(max(0, min(100, round(score))))


# ---------------------------------------------------------------------------
# F5.1, F5.2: WebXR Rig & 360° Gyroscope Mathematics
# ---------------------------------------------------------------------------
def calculate_bridge_camera_position(own_x: float, own_z: float, hdg: float, height: float = 0.88, offset: float = 0.30) -> Tuple[np.ndarray, np.ndarray]:
    """
    Computes bridge camera location and look-at point in Three.js coordinates.
    Scale: 1 NM = 20 units.
    pos.x = -x * 20, pos.z = z * 20.
    """
    world_x = -own_x * THREE_JS_SCALE
    world_z = own_z * THREE_JS_SCALE

    rad = math.radians(hdg % 360)
    cam_x = world_x - math.sin(rad) * offset
    cam_y = height
    cam_z = world_z + math.cos(rad) * offset

    look_x = cam_x - math.sin(rad) * 30.0
    look_y = height
    look_z = cam_z + math.cos(rad) * 30.0

    return np.array([cam_x, cam_y, cam_z]), np.array([look_x, look_y, look_z])


def orientation_euler_to_quaternion(alpha_deg: float, beta_deg: float, gamma_deg: float) -> Tuple[float, float, float, float]:
    """Converts mobile device orientation angles into Three.js Quaternion (x, y, z, w)."""
    a = math.radians(alpha_deg) / 2.0
    b = math.radians(beta_deg) / 2.0
    g = math.radians(gamma_deg) / 2.0

    c1 = math.cos(b)
    c2 = math.cos(g)
    c3 = math.cos(a)
    s1 = math.sin(b)
    s2 = math.sin(g)
    s3 = math.sin(a)

    qx = s1 * c2 * c3 - c1 * s2 * s3
    qy = c1 * s2 * c3 + s1 * c2 * s3
    qz = c1 * c2 * s3 + s1 * s2 * c3
    qw = c1 * c2 * c3 - s1 * s2 * s3

    norm = math.sqrt(qx * qx + qy * qy + qz * qz + qw * qw)
    return (qx / norm, qy / norm, qz / norm, qw / norm)
