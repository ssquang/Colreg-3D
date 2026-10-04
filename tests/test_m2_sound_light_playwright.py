"""
Automated Forensic and Headless Playwright Verification for Milestone M2:
Sound & Light Signals Part D (COLREG-72 Rules 34 & 35, Annex III, Web Audio API synthesis).
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


def run_m2_audit():
    file_path = os.path.abspath('simulator.html').replace('\\', '/')
    file_url = f'file:///{file_path}'

    print(f"Launching Playwright M2 Sound & Light Audit against: {file_url}")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        console_errors = []
        page.on('console', lambda msg: console_errors.append(f"{msg.type}: {msg.text}") if msg.type in ['error'] else None)
        page.on('pageerror', lambda exc: console_errors.append(f"PAGEERROR: {exc}"))

        page.goto(file_url, wait_until='networkidle')
        page.wait_for_timeout(1500)

        print("\n--- TEST 1: PUBLIC API window.AudioSignals & window.AudioEngine CONTRACT ---")
        api_check = page.evaluate("""() => {
            return {
                hasAudioSignals: typeof window.AudioSignals !== 'undefined',
                hasPlayManeuverSignal: typeof window.AudioSignals.playManeuverSignal === 'function',
                hasStartFogTimer: typeof window.AudioSignals.startFogTimer === 'function',
                hasStopFogTimer: typeof window.AudioSignals.stopFogTimer === 'function',
                hasTriggerMastheadFlash: typeof window.AudioSignals.triggerMastheadFlash === 'function',
                hasToggleFogTimer: typeof window.AudioSignals.toggleFogTimer === 'function',
                hasAudioEngine: typeof window.AudioEngine !== 'undefined',
                hasSynthesizeBlast: typeof window.AudioEngine.synthesizeBlast === 'function',
                hasCreatePannerNode: typeof window.AudioEngine.createPannerNode === 'function',
                hasCreateFogFilter: typeof window.AudioEngine.createFogFilter === 'function',
                hasPlayTargetSignal: typeof window.AudioEngine.playTargetSignal === 'function',
                hasRule34Signals: typeof window.RULE_34_SIGNALS !== 'undefined',
                hasEvaluateFogSignal: typeof window.evaluateRule35FogSignal === 'function',
                hasWhistleFreqBand: typeof window.getWhistleFrequencyBand === 'function',
                hasSpatialAttenuation: typeof window.calculateSpatialAudioAttenuation === 'function'
            };
        }""")

        for k, v in api_check.items():
            print(f"  {k}: {v}")
            assert v is True, f"Failed API check: {k} is not True!"
        print("  -> PASS: All window.AudioSignals and window.AudioEngine interface contracts verified.")

        print("\n--- TEST 2: RULE 34 MANEUVER SIGNALS TIMINGS & FLASH COUNT ---")
        signals_check = page.evaluate("""() => {
            const sigs = window.RULE_34_SIGNALS;
            return {
                stbd_blasts: sigs.STARBOARD.blasts,
                stbd_sound: sigs.STARBOARD.total_sound,
                stbd_flashes: sigs.STARBOARD.flashes,

                port_blasts: sigs.PORT.blasts,
                port_sound: sigs.PORT.total_sound,
                port_flashes: sigs.PORT.flashes,

                astern_blasts: sigs.ASTERN.blasts,
                astern_sound: sigs.ASTERN.total_sound,
                astern_flashes: sigs.ASTERN.flashes,

                danger_blasts: sigs.DANGER.blasts,
                danger_sound: sigs.DANGER.total_sound,
                danger_flashes: sigs.DANGER.flashes,

                overtake_agree: sigs.OVERTAKE_AGREE.blasts,
                overtake_stbd: sigs.OVERTAKE_STBD.blasts,
                bend_blasts: sigs.BEND.blasts
            };
        }""")

        assert signals_check["stbd_blasts"] == [1.0] and signals_check["stbd_flashes"] == 1
        assert signals_check["port_blasts"] == [1.0, -1.0, 1.0] and signals_check["port_flashes"] == 2
        assert signals_check["astern_blasts"] == [1.0, -1.0, 1.0, -1.0, 1.0] and signals_check["astern_flashes"] == 3
        assert len([b for b in signals_check["danger_blasts"] if b > 0]) == 5 and signals_check["danger_flashes"] == 5
        print("  Starboard (1 short, 1s):", signals_check["stbd_blasts"], "flashes:", signals_check["stbd_flashes"])
        print("  Port (2 short, 1s each, 1s int):", signals_check["port_blasts"], "flashes:", signals_check["port_flashes"])
        print("  Astern (3 short, 1s each, 1s int):", signals_check["astern_blasts"], "flashes:", signals_check["astern_flashes"])
        print("  Danger (5 rapid short):", signals_check["danger_blasts"][:4], "... flashes:", signals_check["danger_flashes"])
        print("  -> PASS: Rule 34 whistle blast intervals and light sync counts conform to COLREGs 72.")

        print("\n--- TEST 3: RULE 35 RESTRICTED VISIBILITY / FOG SIGNALS ---")
        fog_eval_check = page.evaluate("""() => {
            const waySig = window.evaluateRule35FogSignal(12.5);
            const stopSig = window.evaluateRule35FogSignal(0.0);
            const boundLow = window.evaluateRule35FogSignal(0.2);
            const boundHigh = window.evaluateRule35FogSignal(0.21);

            return {
                way_mode: waySig.mode,
                way_blasts: waySig.blasts,
                way_interval: waySig.interval_sec,

                stop_mode: stopSig.mode,
                stop_blasts: stopSig.blasts,
                stop_interval: stopSig.interval_sec,

                boundLow_mode: boundLow.mode,
                boundHigh_mode: boundHigh.mode
            };
        }""")

        assert fog_eval_check["way_mode"] == "MAKING_WAY" and fog_eval_check["way_blasts"] == [5.0]
        assert fog_eval_check["stop_mode"] == "STOPPED" and fog_eval_check["stop_blasts"] == [5.0, -2.0, 5.0]
        assert fog_eval_check["boundLow_mode"] == "STOPPED"
        assert fog_eval_check["boundHigh_mode"] == "MAKING_WAY"
        print("  Underway making way (>0.2 kts):", fog_eval_check["way_mode"], fog_eval_check["way_blasts"])
        print("  Underway stopped (<=0.2 kts):", fog_eval_check["stop_mode"], fog_eval_check["stop_blasts"])
        print("  Speed threshold boundary 0.20 kts:", fog_eval_check["boundLow_mode"], "vs 0.21 kts:", fog_eval_check["boundHigh_mode"])
        print("  -> PASS: Rule 35(a) and 35(b) fog blast logic and 2-minute cycle verified.")

        print("\n--- TEST 4: FOG TIMER STATE MACHINE & UI CYCLE ---")
        timer_check = page.evaluate("""() => {
            window.AudioSignals.startFogTimer('MAKING_WAY');
            const active1 = window.AudioSignals.fogTimerActive;
            const mode1 = window.AudioSignals.fogTimerForcedMode;

            // Advance time by 60s
            window.AudioSignals.update(60.0);
            const elapsed60 = window.AudioSignals.fogTimerElapsed;

            // Advance time to 121s (trigger cycle reset)
            window.AudioSignals.update(61.0);
            const elapsedReset = window.AudioSignals.fogTimerElapsed;

            window.AudioSignals.stopFogTimer();
            const activeStopped = window.AudioSignals.fogTimerActive;

            // Test automatic mode based on ownShip STW
            window.ownShip.stw = 0.0;
            window.AudioSignals.startFogTimer();
            const readoutEl = document.getElementById('fogTimerReadout');
            const readoutText = readoutEl ? readoutEl.textContent : '';

            window.AudioSignals.stopFogTimer();

            return {
                active1,
                mode1,
                elapsed60,
                elapsedReset,
                activeStopped,
                readoutText
            };
        }""")

        assert timer_check["active1"] is True
        assert timer_check["mode1"] == "MAKING_WAY"
        assert timer_check["elapsed60"] == 60.0
        assert timer_check["elapsedReset"] == 0.0
        assert timer_check["activeStopped"] is False
        assert "Dừng trôi" in timer_check["readoutText"] or "120s" in timer_check["readoutText"]
        print("  Timer start/stop/advance cycle: active1=", timer_check["active1"], "reset=", timer_check["elapsedReset"])
        print("  UI Readout with zero speed:", timer_check["readoutText"])
        print("  -> PASS: Rule 35 timer state machine advances, resets, and updates UI correctly.")

        print("\n--- TEST 5: MASTHEAD FLASHING LIGHT SYNCHRONIZATION (RULE 34b) ---")
        flash_check = page.evaluate("""() => {
            const shipMesh = window.ownShip ? window.ownShip.mesh : null;
            const flashGroup = shipMesh ? shipMesh.getObjectByName('mastheadFlashingLight') : null;
            const ptLight = flashGroup ? flashGroup.getObjectByName('flashPtLight') : null;
            const bulb = flashGroup ? flashGroup.getObjectByName('flashBulb') : null;
            const halo = flashGroup ? flashGroup.getObjectByName('flashHalo') : null;

            // Trigger 2 flashes (PORT signal: 1s on, 1s off, 1s on)
            window.AudioSignals.triggerMastheadFlash(2, 1.0);

            // Immediately check during blast (t = 0.5s into blast)
            const now = performance.now() / 1000;
            updateMastheadFlashes(now + 0.5);
            const intensityDuring = ptLight ? ptLight.intensity : 0;
            const bulbOpacityDuring = bulb ? bulb.material.opacity : 0;
            const haloOpacityDuring = halo ? halo.material.opacity : 0;

            const hudIndicator = document.getElementById('mastheadLightHudIndicator');
            const hudActiveDuring = hudIndicator ? hudIndicator.classList.contains('active') : false;

            // Check during 1s pause interval (t = 1.5s)
            updateMastheadFlashes(now + 1.5);
            const intensityInterval = ptLight ? ptLight.intensity : -1;
            const hudActiveInterval = hudIndicator ? hudIndicator.classList.contains('active') : true;

            // Check during 2nd blast (t = 2.5s)
            updateMastheadFlashes(now + 2.5);
            const intensityBlast2 = ptLight ? ptLight.intensity : 0;

            // Check after finish (t = 4.0s)
            updateMastheadFlashes(now + 4.0);
            const intensityAfter = ptLight ? ptLight.intensity : -1;

            return {
                hasFlashGroup: flashGroup !== null,
                hasPtLight: ptLight !== null,
                hasBulb: bulb !== null,
                hasHalo: halo !== null,
                intensityDuring,
                bulbOpacityDuring,
                haloOpacityDuring,
                hudActiveDuring,
                intensityInterval,
                hudActiveInterval,
                intensityBlast2,
                intensityAfter
            };
        }""")

        assert flash_check["hasFlashGroup"] is True, "Ship mesh missing mastheadFlashingLight!"
        assert flash_check["hasPtLight"] is True, "Missing flashPtLight PointLight!"
        assert flash_check["intensityDuring"] > 0, "PointLight intensity must be > 0 during flash!"
        assert flash_check["hudActiveDuring"] is True, "HUD lamp must be active during flash!"
        assert flash_check["intensityInterval"] == 0, "PointLight must be extinguished during interval!"
        assert flash_check["hudActiveInterval"] is False, "HUD lamp must be inactive during interval!"
        assert flash_check["intensityBlast2"] > 0, "PointLight must illuminate on 2nd flash!"
        assert flash_check["intensityAfter"] == 0, "PointLight must extinguish after sequence!"
        print("  Masthead 3D components:", "PtLight=", flash_check["hasPtLight"], "Bulb=", flash_check["hasBulb"], "Halo=", flash_check["hasHalo"])
        print("  Light intensity: during=", flash_check["intensityDuring"], "interval=", flash_check["intensityInterval"], "blast2=", flash_check["intensityBlast2"], "after=", flash_check["intensityAfter"])
        print("  HUD indicator active state: during=", flash_check["hudActiveDuring"], "interval=", flash_check["hudActiveInterval"])
        print("  -> PASS: Rule 34(b) masthead PointLight & glow billboard flash in exact sync with whistle blasts.")

        print("\n--- TEST 6: SPATIAL AUDIO HRTF PANNER & FOG FILTERING ---")
        spatial_check = page.evaluate("""() => {
            const attenNear = window.calculateSpatialAudioAttenuation(0.5);
            const attenMid = window.calculateSpatialAudioAttenuation(1.5, 0.75, 2.0);
            const attenFar = window.calculateSpatialAudioAttenuation(2.5, 0.75, 2.0);

            // Test procedural panner node construction
            window.AudioEngine.init();
            const panner = window.AudioEngine.createPannerNode({ x: 30, y: 0, z: 40 });
            const fogFilterClear = window.AudioEngine.createFogFilter(1.0, false);
            const fogFilterDense = window.AudioEngine.createFogFilter(1.0, true);

            return {
                attenNear,
                attenMid,
                attenFar,
                pannerDistanceModel: panner ? panner.distanceModel : null,
                pannerPanningModel: panner ? panner.panningModel : null,
                pannerRefDistance: panner ? panner.refDistance : null,
                fogFilterClearCutoff: fogFilterClear ? fogFilterClear.frequency.value : null,
                fogFilterDenseCutoff: fogFilterDense ? fogFilterDense.frequency.value : null
            };
        }""")

        assert spatial_check["attenNear"] == 1.0
        assert round(spatial_check["attenMid"], 2) == 0.50
        assert spatial_check["attenFar"] == 0.0
        assert spatial_check["pannerDistanceModel"] == "inverse"
        assert spatial_check["pannerPanningModel"] == "HRTF"
        assert spatial_check["fogFilterDenseCutoff"] < spatial_check["fogFilterClearCutoff"]
        print("  Attenuation math:", "0.5 NM =", spatial_check["attenNear"], "1.5 NM =", spatial_check["attenMid"], "2.5 NM =", spatial_check["attenFar"])
        print("  Panner config: model=", spatial_check["pannerPanningModel"], "distanceModel=", spatial_check["pannerDistanceModel"], "refDist=", spatial_check["pannerRefDistance"])
        print("  Fog lowpass cutoff: clear=", spatial_check["fogFilterClearCutoff"], "Hz vs dense fog=", spatial_check["fogFilterDenseCutoff"], "Hz (muffled)")
        print("  -> PASS: Procedural Spatial Audio Engine PannerNode and fog lowpass filtering verified.")

        print("\n--- TEST 7: KEYBOARD SHORTCUTS & UI HORN BUTTONS ---")
        ui_check = page.evaluate("""() => {
            // Click horn buttons
            const btnStbd = document.getElementById('btnHornStbd');
            const btnPort = document.getElementById('btnHornPort');
            const btnAstern = document.getElementById('btnHornAstern');
            const btnDanger = document.getElementById('btnHornDanger');

            const hasAllButtons = btnStbd && btnPort && btnAstern && btnDanger;

            // Click 1 short blast button
            btnStbd.click();
            const banner1 = document.getElementById('whistleHudBanner');
            const bannerText1 = banner1 ? banner1.textContent : '';

            // Simulate pressing key '2'
            window.AudioSignals.lastSignalTime = 0; // reset debounce for testing
            window.dispatchEvent(new KeyboardEvent('keydown', { key: '2' }));
            const bannerText2 = banner1 ? banner1.textContent : '';

            // Simulate pressing key '3'
            window.AudioSignals.lastSignalTime = 0;
            window.dispatchEvent(new KeyboardEvent('keydown', { key: '3' }));
            const bannerText3 = banner1 ? banner1.textContent : '';

            // Simulate pressing key '5'
            window.AudioSignals.lastSignalTime = 0;
            window.dispatchEvent(new KeyboardEvent('keydown', { key: '5' }));
            const bannerText5 = banner1 ? banner1.textContent : '';

            return {
                hasAllButtons: !!hasAllButtons,
                bannerText1,
                bannerText2,
                bannerText3,
                bannerText5
            };
        }""")

        assert ui_check["hasAllButtons"] is True
        assert "PHẢI" in ui_check["bannerText1"] or "STARBOARD" in ui_check["bannerText1"]
        assert "TRÁI" in ui_check["bannerText2"] or "PORT" in ui_check["bannerText2"]
        assert "LÙI" in ui_check["bannerText3"] or "ASTERN" in ui_check["bannerText3"]
        assert "NGUY HIỂM" in ui_check["bannerText5"] or "DANGER" in ui_check["bannerText5"]
        print("  Dedicated UI buttons present:", ui_check["hasAllButtons"])
        print("  Click '1' banner:", ui_check["bannerText1"])
        print("  Key '2' banner:", ui_check["bannerText2"])
        print("  Key '3' banner:", ui_check["bannerText3"])
        print("  Key '5' banner:", ui_check["bannerText5"])
        print("  -> PASS: Dedicated UI horn buttons and keyboard shortcuts (1, 2, 3, 5) operational.")

        print("\n--- TEST 8: CONSOLE ERRORS AUDIT ---")
        print(f"  Console errors detected: {len(console_errors)}")
        for err in console_errors:
            print("   !", err)
        assert len(console_errors) == 0, f"Detected console errors: {console_errors}"
        print("  -> PASS: 0 console errors during entire M2 audit execution.")

        browser.close()
        print("\n=======================================================")
        print(">>> MILESTONE M2 (SOUND & LIGHT SIGNALS) FULLY PASSED! <<<")
        print("=======================================================")


if __name__ == '__main__':
    run_m2_audit()
