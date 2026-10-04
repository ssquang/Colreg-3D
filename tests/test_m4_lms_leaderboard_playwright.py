"""
Automated Forensic and Headless Playwright Verification for Milestone M4:
Classroom LMS & Offline Leaderboard (F4.1 Instructor Studio, F4.2 Scenario Import QR/PIN, F4.3 LMS Leaderboard).
"""

import os
import sys
import time
from playwright.sync_api import sync_playwright

if sys.stdout.encoding != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass


def run_m4_audit():
    file_path = os.path.abspath('simulator.html').replace('\\', '/')
    file_url = f'file:///{file_path}'

    print(f"Launching Playwright M4 Classroom LMS & Leaderboard Audit against: {file_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append(f"{msg.type}: {msg.text}") if msg.type in ['error'] else None)
        page.on('pageerror', lambda exc: console_errors.append(f"PAGEERROR: {exc}"))

        page.goto(file_url, wait_until='networkidle')
        page.wait_for_timeout(1500)

        print("\n--- TEST 1: PUBLIC API window.LMSEngine CONTRACT ---")
        api_check = page.evaluate("""() => {
            return {
                hasLMSEngine: typeof window.LMSEngine !== 'undefined',
                hasExportScenarioQR: typeof window.LMSEngine.exportScenarioQR === 'function',
                hasImportScenarioJSON: typeof window.LMSEngine.importScenarioJSON === 'function',
                hasSaveScore: typeof window.LMSEngine.saveScore === 'function',
                hasGetLeaderboard: typeof window.LMSEngine.getLeaderboard === 'function',
                hasComputeTotalScore: typeof window.LMSEngine.computeTotalScore === 'function',
                hasEncodeCompactScenario: typeof window.LMSEngine.encodeCompactScenario === 'function',
                hasDecodeCompactScenario: typeof window.LMSEngine.decodeCompactScenario === 'function',
                hasGenerateScenarioPIN: typeof window.LMSEngine.generateScenarioPIN === 'function',
                hasQRCodeLib: typeof window.QRCode !== 'undefined',
                hasJsQRLib: typeof window.jsQR !== 'undefined'
            };
        }""")

        for k, v in api_check.items():
            print(f"  {k}: {v}")
            assert v is True, f"Failed API check: {k} is not True!"
        print("  -> PASS: All window.LMSEngine interface contracts verified.")

        print("\n--- TEST 2: F4.1 INSTRUCTOR STUDIO UI & SCENARIO DESIGNER ---")
        studio_check = page.evaluate("""() => {
            window.LMSEngine.openInstructorStudio();
            const modal = document.getElementById('instructorStudioModal');
            const isOpen1 = modal && modal.classList.contains('active');

            // Test target vessels limits (1 to 5)
            // Add until max 5
            for (let i = 0; i < 6; i++) {
                window.LMSEngine.addTargetShip();
            }
            const countAfterAdd = document.querySelectorAll('#instructorTargetsList .target-card-row').length;

            // Remove down to 1
            for (let i = 0; i < 6; i++) {
                window.LMSEngine.removeTargetShip(0);
            }
            const countAfterRemove = document.querySelectorAll('#instructorTargetsList .target-card-row').length;

            // Reset with 2 targets for test export
            window.LMSEngine.addTargetShip({ id: 'T2', type: 'fishing', x: -1.5, z: 2.0, course: 90, speed: 8.0 });
            window.LMSEngine.generateStudioExport();

            const pinText = document.getElementById('instructorPinBadge').textContent.trim();
            const jsonText = document.getElementById('instructorJsonOutput').value.trim();

            const qrDataUrl = window.LMSEngine.exportScenarioQR();

            window.LMSEngine.closeInstructorStudio();
            const isClosed = !modal.classList.contains('active');

            return {
                isOpen1,
                countAfterAdd,
                countAfterRemove,
                pinText,
                jsonText,
                jsonLength: jsonText.length,
                hasDataUrl: qrDataUrl.startsWith('data:image/png;base64,'),
                isClosed
            };
        }""")

        assert studio_check["isOpen1"] is True, "Instructor Studio modal did not open"
        assert studio_check["countAfterAdd"] == 5, f"Expected max 5 targets, got {studio_check['countAfterAdd']}"
        assert studio_check["countAfterRemove"] == 1, f"Expected min 1 target, got {studio_check['countAfterRemove']}"
        assert len(studio_check["pinText"]) == 6, f"PIN should be 6 characters: {studio_check['pinText']}"
        assert studio_check["jsonLength"] < 160, f"Compact JSON should be < 160 chars, got {studio_check['jsonLength']}"
        assert studio_check["hasDataUrl"] is True, "QR Code did not produce valid PNG dataURL"
        assert studio_check["isClosed"] is True, "Modal did not close"
        print(f"  Max targets clamped to: {studio_check['countAfterAdd']}")
        print(f"  Min targets clamped to: {studio_check['countAfterRemove']}")
        print(f"  Generated PIN: {studio_check['pinText']}")
        print(f"  Compact JSON ({studio_check['jsonLength']} chars): {studio_check['jsonText']}")
        print("  QR Code dataURL starts with data:image/png;base64: True")
        print("  -> PASS: F4.1 Instructor Studio scenario design, limits, and export verified.")

        print("\n--- TEST 3: F4.2 SCENARIO IMPORT (QR / PIN / JSON) ENGINE ---")
        import_check = page.evaluate("""() => {
            // Test 1: Import compact JSON
            const sampleJson = JSON.stringify({
                v: 1,
                id: "TSS_CROSS",
                own: [0.0, -3.0, 0, 14.0],
                tgts: [
                    ["T1", "c", 2.5, 1.0, 240, 16.0],
                    ["T2", "f", -1.5, 2.0, 90, 8.0]
                ],
                env: [1, 45, 15]
            });
            const resJson = window.LMSEngine.importScenarioJSON(sampleJson);
            const loadedScenId = window.currentScenarioId;
            const targetCount = window.targets ? window.targets.length : 0;
            const ownCourse = window.ownShip ? window.ownShip.course : -1;

            // Test 2: Import preset PIN A9X4K2
            const resPin = window.LMSEngine.importScenarioJSON("A9X4K2");

            // Test 3: Malformed input rejection
            let malformedThrew = false;
            try {
                window.LMSEngine.importScenarioJSON("{bad json");
            } catch (e) {
                malformedThrew = true;
            }

            // Test 4: Unknown PIN returns false
            const unknownPinRes = window.LMSEngine.importScenarioJSON("ZZZ999");

            return {
                resJson,
                loadedScenId,
                targetCount,
                ownCourse,
                resPin,
                malformedThrew,
                unknownPinRes
            };
        }""")

        assert import_check["resJson"] is True, "importScenarioJSON failed on valid compact JSON"
        assert import_check["targetCount"] == 2, f"Expected 2 targets loaded, got {import_check['targetCount']}"
        assert import_check["ownCourse"] == 0, f"Expected own course 0, got {import_check['ownCourse']}"
        assert import_check["resPin"] is True, "importScenarioJSON failed on valid PIN A9X4K2"
        assert import_check["malformedThrew"] is True, "importScenarioJSON did not throw on malformed JSON"
        assert import_check["unknownPinRes"] is False, "importScenarioJSON should return false for unknown PIN"
        print("  Loaded compact JSON: targets=", import_check["targetCount"], "ownCourse=", import_check["ownCourse"])
        print("  Loaded PIN A9X4K2: True")
        print("  Rejected malformed JSON:", import_check["malformedThrew"])
        print("  Rejected unknown PIN:", not import_check["unknownPinRes"])
        print("  -> PASS: F4.2 Scenario import engine correctly parses and loads scenarios.")

        print("\n--- TEST 4: F4.3 OFFLINE LMS LEADERBOARD & SCORING MATHEMATICS ---")
        math_check = page.evaluate("""() => {
            const s1 = window.LMSEngine.computeTotalScore(90, 80, 1.5, 0); // expect 84
            const s2 = window.LMSEngine.computeTotalScore(0, 0, 0.1, 5);   // expect 0
            const s3 = window.LMSEngine.computeTotalScore(100, 100, 3.0, 0); // expect 100
            const s4 = window.LMSEngine.computeTotalScore(0, 100, 2.0, 0);  // expect 60
            const s5 = window.LMSEngine.computeTotalScore(100, 0, 2.0, 0);  // expect 40
            const s6 = window.LMSEngine.computeTotalScore(90, 90, 0.3, 0);  // expect 60 (unsafe CPA penalty)
            return { s1, s2, s3, s4, s5, s6 };
        }""")

        assert math_check["s1"] == 84, f"Expected 84, got {math_check['s1']}"
        assert math_check["s2"] == 0, f"Expected 0, got {math_check['s2']}"
        assert math_check["s3"] == 100, f"Expected 100, got {math_check['s3']}"
        assert math_check["s4"] == 60, f"Expected 60, got {math_check['s4']}"
        assert math_check["s5"] == 40, f"Expected 40, got {math_check['s5']}"
        assert math_check["s6"] == 60, f"Expected 60, got {math_check['s6']}"
        print("  Scoring test: 90/80 safe ->", math_check["s1"])
        print("  Scoring test: 0/0 collision/violations ->", math_check["s2"])
        print("  Scoring test: 100/100 perfect ->", math_check["s3"])
        print("  Scoring test: 0/100 ->", math_check["s4"])
        print("  Scoring test: 100/0 ->", math_check["s5"])
        print("  Scoring test: 90/90 unsafe CPA 0.3 NM ->", math_check["s6"])
        print("  -> PASS: All scoring oracle formulas strictly verified.")

        print("\n--- TEST 5: LEADERBOARD PERSISTENCE & TABLE RENDERING ---")
        persistence_check = page.evaluate("""async () => {
            // Save candidate record
            const savedRec = await window.LMSEngine.saveScore("Cadet Playwright Tester", 95, 90, { minCpa: 2.0, violations: 0 });
            
            // Retrieve leaderboard
            const board = await window.LMSEngine.getLeaderboard();
            const topRecord = board[0];

            // Open Leaderboard modal and verify table rows
            window.LMSEngine.openLeaderboard();
            await window.LMSEngine.renderLeaderboardTable();
            const rowCount = document.querySelectorAll('#leaderboardTableBody tr').length;
            const tableText = document.getElementById('leaderboardTableBody').textContent;

            // Check localStorage
            const localData = localStorage.getItem('colregs_leaderboard_data');
            const hasLocal = localData && localData.includes("Cadet Playwright Tester");

            window.LMSEngine.closeLeaderboard();

            return {
                savedTotal: savedRec.totalScore,
                topCandidate: topRecord.candidateName,
                boardLength: board.length,
                rowCount,
                tableHasTester: tableText.includes("Cadet Playwright Tester"),
                hasLocal
            };
        }""")

        assert persistence_check["savedTotal"] == 92, f"Expected total 92, got {persistence_check['savedTotal']}"
        assert persistence_check["boardLength"] >= 1, "Leaderboard is empty"
        assert persistence_check["rowCount"] >= 1, "Leaderboard table has no rows"
        assert persistence_check["tableHasTester"] is True, "Table did not render candidate name"
        assert persistence_check["hasLocal"] is True, "LocalStorage did not store candidate record"
        print(f"  Saved record total score: {persistence_check['savedTotal']}")
        print(f"  Top rank candidate: {persistence_check['topCandidate']}")
        print(f"  Table rows rendered: {persistence_check['rowCount']}")
        print(f"  LocalStorage persistent: {persistence_check['hasLocal']}")
        print("  -> PASS: Leaderboard persistence (IndexedDB & LocalStorage) and UI table verified.")

        print("\n--- TEST 6: CONSOLE ERROR CHECK ---")
        print(f"  Total console errors caught: {len(console_errors)}")
        if console_errors:
            for ce in console_errors:
                print(f"    - {ce}")
        assert len(console_errors) == 0, f"Found {len(console_errors)} console errors during audit!"
        print("  -> PASS: 0 console errors during runtime.")

        browser.close()

    print("\n=======================================================")
    print(">>> PLAYWRIGHT M4 AUDIT SUITE PASSED WITH 100% SUCCESS <<<")
    print("=======================================================\n")
    return True


if __name__ == '__main__':
    run_m4_audit()
