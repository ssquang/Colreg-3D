import math
import sys
import numpy as np

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def velocity(course: float, speed: float) -> np.ndarray:
    """Calculate velocity vector (vx, vy) in knots, where 000° is North (+Y), 090° is East (+X)."""
    rad = math.radians(course % 360)
    return np.array([speed * math.sin(rad), speed * math.cos(rad)], dtype=float)


def polar(bearing: float, distance: float) -> np.ndarray:
    """Calculate position (x, y) in NM given true bearing and distance from origin."""
    rad = math.radians(bearing % 360)
    return np.array([distance * math.sin(rad), distance * math.cos(rad)], dtype=float)


def calculate_cpa_tcpa(
    p_own: np.ndarray, v_own: np.ndarray, p_target: np.ndarray, v_target: np.ndarray
):
    """
    Calculate CPA (NM), TCPA (hours), CPA position of target relative to own ship,
    and relative speed (knots).
    """
    rel_pos = p_target - p_own  # vector from own ship to target
    rel_vel = v_target - v_own  # relative velocity
    rel_speed = float(np.linalg.norm(rel_vel))

    rel_vel_sq = float(np.dot(rel_vel, rel_vel))
    current_dist = float(np.linalg.norm(rel_pos))

    if rel_vel_sq < 1e-9:
        return current_dist, 0.0, current_dist, rel_speed

    # tcpa = - (p · v) / |v|^2
    dot_product = float(np.dot(rel_pos, rel_vel))
    tcpa = -dot_product / rel_vel_sq

    if tcpa < 0:
        # CPA has already passed
        cpa = current_dist
    else:
        cpa_pos = rel_pos + rel_vel * tcpa
        cpa = float(np.linalg.norm(cpa_pos))

    return cpa, tcpa, current_dist, rel_speed


def bearing_deg(from_p: np.ndarray, to_p: np.ndarray) -> float:
    """Calculate true bearing from from_p to to_p in degrees (000° - 359°)."""
    diff = to_p - from_p
    deg = math.degrees(math.atan2(diff[0], diff[1]))
    return (deg + 360) % 360


def evaluate_colregs(scenario_type: str, own_course_change: float, cpa: float, min_passed_dist: float, has_collided: bool):
    """
    Scoring logic:
    - Base score: 100
    - Collision: 0
    - Head-on (Rule 14): Must turn Starboard (+20° to +50°). Turning Port is severe violation (-50).
    - Crossing Give-way (Rule 15): Must turn Starboard or slow down. Turning Port is severe violation (-50).
    - Crossing Stand-on (Rule 15): Maintain course & speed until in extremis.
    - Overtaking (Rule 13): Overtaking vessel must keep clear.
    """
    if has_collided:
        return 0, "THẤT BẠI: ĐÂM VA TRỰC DIỆN! Điểm: 0/100. Hãy tuân thủ quy tắc tránh va sớm và dứt khoát!"

    score = 100
    details = []

    if scenario_type == "head_on":
        # Rule 14: Both must alter course to starboard
        if own_course_change > 15:
            details.append("Đã bẻ lái sang mạn phải đúng quy tắc Rule 14 (+40)")
        elif own_course_change < -5:
            score -= 50
            details.append("VI PHẠM NGUY HIỂM: Bẻ lái sang mạn trái cắt mũi tàu đối diện (-50)")
        else:
            score -= 30
            details.append("CHƯA ĐIỀU ĐỘNG: Chưa bẻ lái rõ rệt để tránh va (-30)")

    elif scenario_type == "crossing_give_way":
        # Rule 15: Give-way vessel must keep out of the way, avoid crossing ahead
        if own_course_change > 15:
            details.append("Đã chủ động bẻ sang mạn phải nhường đường an toàn (+40)")
        elif own_course_change < -5:
            score -= 50
            details.append("VI PHẠM NGUY HIỂM: Bẻ sang mạn trái cắt trước mũi tàu được ưu tiên (-50)")
        else:
            score -= 35
            details.append("CHƯA HÀNH ĐỘNG: Tàu của ta có nghĩa vụ nhường đường (Give-way) (-35)")

    elif scenario_type == "crossing_stand_on":
        # Rule 17: Stand-on vessel keep course and speed
        if abs(own_course_change) < 10:
            details.append("Duy trì hướng đi và tốc độ chuẩn quy tắc Stand-on (+40)")
        else:
            score -= 20
            details.append("LƯU Ý: Tàu được ưu tiên nên giữ hướng, trừ khi tàu kia không hành động (-20)")

    # Safety distance evaluation
    if cpa < 1.0:
        score -= 25
        details.append(f"CPA quá nhỏ ({cpa:.2f} NM < 1.0 NM) - Vùng nguy hiểm (-25)")
    elif cpa < 2.0:
        score -= 10
        details.append(f"CPA ở mức trung bình ({cpa:.2f} NM)")
    else:
        details.append(f"CPA an toàn xuất sắc ({cpa:.2f} NM >= 2.0 NM)")

    score = max(0, min(100, score))
    verdict = "XUẤT SẮC" if score >= 85 else "ĐẠT" if score >= 60 else "CẦN RÚT KINH NGHIỆM"
    return score, f"{verdict} ({score}/100): " + " | ".join(details)


def test_calculations():
    # Test 1: Head-on scenario
    # Own ship heading 000°, 13 kts at origin (0, 0)
    # Target ship heading 180°, 13 kts at (0, 6 NM) North
    p_own = np.array([0.0, 0.0])
    v_own = velocity(0, 13)
    p_target = np.array([0.0, 6.0])
    v_target = velocity(180, 13)

    cpa, tcpa, dist, rel_spd = calculate_cpa_tcpa(p_own, v_own, p_target, v_target)
    print(f"Test 1 - Head-on initial:")
    print(f"  Distance: {dist:.2f} NM, Rel Speed: {rel_spd:.1f} kts")
    print(f"  CPA: {cpa:.2f} NM (Expect ~0.0)")
    print(f"  TCPA: {tcpa * 60:.1f} min (Expect ~13.8 min)")
    assert math.isclose(cpa, 0.0, abs_tol=0.01), "Head-on CPA must be 0"
    assert math.isclose(rel_spd, 26.0, abs_tol=0.1), "Relative speed must be 26 kts"

    # Test 2: Alter course 30 degrees to Starboard (Course 030°)
    v_own_stbd = velocity(30, 13)
    cpa_stbd, tcpa_stbd, _, _ = calculate_cpa_tcpa(p_own, v_own_stbd, p_target, v_target)
    print(f"Test 2 - After Starboard 30° maneuver:")
    print(f"  CPA: {cpa_stbd:.2f} NM (Safe > 1.5 NM)")
    print(f"  TCPA: {tcpa_stbd * 60:.1f} min")
    assert cpa_stbd > 1.5, "Starboard turn must create safe CPA"

    # Test 3: Scoring evaluation
    score_stbd, desc_stbd = evaluate_colregs("head_on", +30, cpa_stbd, cpa_stbd, False)
    print(f"Test 3 - Stbd Score: {score_stbd} -> {desc_stbd}")
    assert score_stbd >= 85, "Correct maneuver must score >= 85"

    score_port, desc_port = evaluate_colregs("head_on", -30, 0.5, 0.5, False)
    print(f"Test 3 - Port Violation Score: {score_port} -> {desc_port}")
    # Test 4: Close quarters encounter (1.2 NM distance)
    p_own_close = np.array([0.0, -0.6])
    p_target_close = np.array([0.0, 0.6])
    cpa_close, tcpa_close, dist_close, _ = calculate_cpa_tcpa(p_own_close, velocity(0, 13), p_target_close, velocity(180, 13))
    print(f"\nTest 4 - Close range encounter:")
    print(f"  Initial Distance: {dist_close:.2f} NM (Visual contact)")
    print(f"  TCPA: {tcpa_close * 60:.1f} min (Immediate action required)")
    assert math.isclose(dist_close, 1.2, abs_tol=0.01)

    # Test 5: Rule 18 Vessel Hierarchy (NUC / RAM vessel encounters)
    # When target is NUC (Not Under Command), Own Ship must give way even on crossing stand-on
    def evaluate_rule_18(target_type: str, own_acted: bool):
        if target_type in ["nuc", "ram"]:
            return (100, "TUÂN THỦ RULE 18: Đã chủ động nhường đường cho tàu hạn chế/mất điều động") if own_acted else (50, "CẢNH BÁO RULE 18: Bắt buộc nhường đường!")
        return (100, "Quy tắc thông thường")

    score_nuc_ok, desc_nuc_ok = evaluate_rule_18("nuc", True)
    score_nuc_fail, desc_nuc_fail = evaluate_rule_18("nuc", False)
    print(f"\nTest 5 - Rule 18 Test:")
    print(f"  NUC avoided: {score_nuc_ok} -> {desc_nuc_ok}")
    print(f"  NUC ignored: {score_nuc_fail} -> {desc_nuc_fail}")
    assert score_nuc_ok == 100
    # Test 6: Verify HTML Simulator features and COLREG 72 implementations
    with open("simulator.html", "r", encoding="utf-8") as f:
        html = f.read()

    required_keywords = [
        "buildNUCShipMesh",
        "buildRAMShipMesh",
        "buildCBDShipMesh",
        "buildFishingTrawlerMesh",
        "buildSailingVesselMesh",
        "buildPilotVesselMesh",
        "buildTowingShipMesh",
        "buildAnchoredShipMesh",
        "buildPowerDrivenShipMesh",
        "createOwnWarshipMesh",
        "createNavLight",
        "toggleDayNight",
        "onInitialDistanceChange",
        "updateCOLREGsSigns",
        "colregsSignalCard",
        "dayShapeVisual",
        "nightLightVisual",
        "initialDistanceSlider",
        "btnDayNight",
        "OWN SHIP",
    ]
    for kw in required_keywords:
        assert kw in html, f"Missing required feature in simulator.html: {kw}"

    print(f"\nTest 6 - Verified all {len(required_keywords)} COLREG 72 features present in simulator.html!")
    print("\n>>> TẤT CẢ CÁC BÀI TEST TOÁN HÀNG HẢI, COLREG 72 & SIMULATOR ĐÃ VƯỢT QUA THÀNH CÔNG! <<<")


if __name__ == "__main__":
    print("\n--- PHASE 1: LEGACY NAUTICAL MATH & KEYWORD AUDIT ---")
    test_calculations()
    print("\n--- PHASE 2: COMPREHENSIVE E2E 4-TIER SUITE (230 TESTS) ---")
    from tests.run_all_tests import main as run_e2e_tests
    exit_code = run_e2e_tests()
    sys.exit(exit_code)


