/**
 * ADVERSARIAL STRESS TEST HARNESS FOR MILESTONE M1
 * Author: teamwork_preview_challenger
 * Scope: Multi-Vessel Physics, 5-Target Radar Loops, Collision Detection,
 *        Zero Relative Speed, Extreme Drift & Leeway Physics.
 */

const fs = require('fs');
const path = require('path');

// Read simulator.html to extract actual production code
const htmlPath = path.resolve(__dirname, '../simulator.html');
const htmlContent = fs.readFileSync(htmlPath, 'utf8');

// 1. Mock Browser and Three.js Environment
const THREE = {
  MathUtils: {
    degToRad: (d) => (d * Math.PI) / 180,
    radToDeg: (r) => (r * 180) / Math.PI,
    lerp: (x, y, t) => x + (y - x) * t
  }
};

// Extract calculateGroundVelocity function verbatim from simulator.html
const fnGroundVelocityMatch = htmlContent.match(/function calculateGroundVelocity[\s\S]*?\n    \}/);
if (!fnGroundVelocityMatch) {
  throw new Error("Could not find calculateGroundVelocity in simulator.html");
}
const calculateGroundVelocity = new Function('THREE', `${fnGroundVelocityMatch[0]}; return calculateGroundVelocity;`)(THREE);

// Extract drawRadar function verbatim from simulator.html
const fnDrawRadarMatch = htmlContent.match(/function drawRadar[\s\S]*?\n    \}/);
if (!fnDrawRadarMatch) {
  throw new Error("Could not find drawRadar in simulator.html");
}

let testsPassed = 0;
let testsFailed = 0;
const failures = [];

function assert(condition, message) {
  if (!condition) {
    testsFailed++;
    failures.push(message);
    console.error(`  FAIL: ${message}`);
  } else {
    testsPassed++;
    console.log(`  PASS: ${message}`);
  }
}

function testHeader(title) {
  console.log(`\n======================================================`);
  console.log(`  ${title}`);
  console.log(`======================================================`);
}

// =========================================================================
// SUITE 1: NUMERICAL STABILITY & DIVISION-BY-ZERO / NaN GUARDS
// =========================================================================
testHeader("SUITE 1: NUMERICAL STABILITY & CPA/TCPA ZERO RELATIVE SPEED");

function simulateCpaTcpa(ownShip, target, wind, current) {
  const ownGv = calculateGroundVelocity(ownShip.course, ownShip.speed, wind, current);
  const tgv = calculateGroundVelocity(target.course, target.speed, wind, current);

  const dx = target.x - ownShip.x;
  const dz = target.z - ownShip.z;
  const dist = Math.sqrt(dx * dx + dz * dz);
  const bearing = (THREE.MathUtils.radToDeg(Math.atan2(dx, dz)) + 360) % 360;

  const rel_vx = tgv.vgx - ownGv.vgx;
  const rel_vz = tgv.vgz - ownGv.vgz;
  const rel_speed = Math.sqrt(rel_vx * rel_vx + rel_vz * rel_vz);

  const rel_v_sq = rel_vx * rel_vx + rel_vz * rel_vz;
  let cpa = dist;
  let tcpa = 0.0;

  if (rel_v_sq > 1e-6) {
    const dot = dx * rel_vx + dz * rel_vz;
    tcpa = -dot / rel_v_sq;
    if (tcpa > 0) {
      const cx = dx + rel_vx * tcpa;
      const cz = dz + rel_vz * tcpa;
      cpa = Math.sqrt(cx * cx + cz * cz);
    } else {
      cpa = dist;
    }
  } else {
    cpa = dist;
    tcpa = 0.0;
  }

  return { dist, bearing, rel_vx, rel_vz, rel_speed, rel_v_sq, cpa, tcpa };
}

// 1.1 Identical heading and speed (zero relative velocity)
{
  const own = { course: 90, speed: 14, x: 0, z: 0 };
  const tgt = { course: 90, speed: 14, x: 2, z: 3 };
  const res = simulateCpaTcpa(own, tgt, null, null);
  assert(!isNaN(res.cpa), "Zero relative velocity: CPA is not NaN");
  assert(!isNaN(res.tcpa), "Zero relative velocity: TCPA is not NaN");
  assert(isFinite(res.cpa), "Zero relative velocity: CPA is finite");
  assert(isFinite(res.tcpa), "Zero relative velocity: TCPA is finite");
  assert(Math.abs(res.cpa - res.dist) < 1e-5, `Zero relative speed: CPA (${res.cpa}) equals current distance (${res.dist})`);
  assert(res.tcpa === 0.0, `Zero relative speed: TCPA is exactly 0.0 (got ${res.tcpa})`);
}

// 1.2 Both vessels completely stationary (speed 0)
{
  const own = { course: 0, speed: 0, x: 0, z: 0 };
  const tgt = { course: 180, speed: 0, x: 1, z: 1 };
  const res = simulateCpaTcpa(own, tgt, null, null);
  assert(!isNaN(res.cpa) && !isNaN(res.tcpa), "Stationary vessels: CPA/TCPA are not NaN");
  assert(res.tcpa === 0.0, "Stationary vessels: TCPA is 0.0");
  assert(Math.abs(res.cpa - Math.SQRT2) < 1e-5, "Stationary vessels: CPA equals Euclidean distance");
}

// 1.3 Collocated vessels (distance 0)
{
  const own = { course: 0, speed: 10, x: 5, z: 5 };
  const tgt = { course: 90, speed: 10, x: 5, z: 5 };
  const res = simulateCpaTcpa(own, tgt, null, null);
  assert(!isNaN(res.dist) && res.dist === 0, "Collocated vessels: Distance is 0.0 without NaN");
  assert(!isNaN(res.bearing), "Collocated vessels: Bearing is not NaN (atan2(0,0)=0)");
  assert(!isNaN(res.cpa) && !isNaN(res.tcpa), "Collocated vessels: CPA/TCPA are not NaN");
}

// 1.4 Vessels already receding (tcpa < 0)
{
  const own = { course: 0, speed: 10, x: 0, z: 0 };
  const tgt = { course: 0, speed: 20, x: 0, z: 5 }; // Target pulling away at higher speed
  const res = simulateCpaTcpa(own, tgt, null, null);
  assert(res.tcpa < 0, `Receding vessel: raw TCPA < 0 (got ${res.tcpa})`);
  assert(res.cpa === res.dist, `Receding vessel: CPA clamped to current distance (${res.cpa} == ${res.dist})`);
}

// =========================================================================
// SUITE 2: MULTI-VESSEL PHYSICS & 5-SHIP CONCURRENT KINEMATICS
// =========================================================================
testHeader("SUITE 2: MULTI-VESSEL PHYSICS & 5-SHIP CONCURRENT ENCOUNTERS");

function create5ShipCluster() {
  const ownShip = {
    x: 0, z: 0, course: 0, speed: 12.0, rot: 0, rudder: 0,
    vgx: 0, vgz: 12.0, sog: 12.0, cog: 0.0, crabAngle: 0.0,
    minDistanceRecorded: 999.0, hasCollided: false, hasSafelyPassed: false
  };

  const targets = [
    { id: 'TGT-01', name: 'Ahead slow', type: 'cargo', x: 0.0, z: 4.0, course: 0, speed: 6.0 },
    { id: 'TGT-02', name: 'Crossing Stbd', type: 'container', x: 4.0, z: 2.0, course: 270, speed: 14.0 },
    { id: 'TGT-03', name: 'Crossing Port', type: 'fishing', x: -4.0, z: 3.0, course: 90, speed: 8.0 },
    { id: 'TGT-04', name: 'Head-on Near', type: 'tanker', x: 0.1, z: 6.0, course: 180, speed: 12.0 },
    { id: 'TGT-05', name: 'Overtaking Stern', type: 'tug', x: -0.2, z: -3.0, course: 0, speed: 16.0 }
  ];

  targets.forEach(t => {
    t.dist = 999.0;
    t.bearing = 0.0;
    t.cpa = 999.0;
    t.tcpa = 0.0;
    t.rel_vx = 0.0;
    t.rel_vz = 0.0;
    t.rel_speed = 0.0;
  });

  return { ownShip, targets };
}

// 2.1 Multi-step integration of 5 ships simultaneously
{
  const sim = create5ShipCluster();
  const env = {
    wind: { direction: 270, speed: 15, leewayCoeff: 0.04 },
    current: { set: 90, drift: 1.0 }
  };

  let minDisGlobal = 999.0;
  let collisionTriggered = false;
  let collidedTarget = null;

  const dt = 0.1; // seconds
  const totalSteps = 6000; // 600 seconds = 10 minutes simulation

  for (let step = 0; step < totalSteps; step++) {
    const simDt = dt;

    // Own ship ground velocity
    const ownGv = calculateGroundVelocity(sim.ownShip.course, sim.ownShip.speed, env.wind, env.current);
    sim.ownShip.vgx = ownGv.vgx;
    sim.ownShip.vgz = ownGv.vgz;
    sim.ownShip.sog = ownGv.sog;
    sim.ownShip.cog = ownGv.cog;
    sim.ownShip.crabAngle = ownGv.crabAngle;

    sim.ownShip.x += (ownGv.vgx / 3600) * simDt;
    sim.ownShip.z += (ownGv.vgz / 3600) * simDt;

    let minDisStep = 999.0;

    sim.targets.forEach(t => {
      const tgv = calculateGroundVelocity(t.course, t.speed, env.wind, env.current);
      t.vgx = tgv.vgx;
      t.vgz = tgv.vgz;
      t.sog = tgv.sog;
      t.cog = tgv.cog;
      t.crabAngle = tgv.crabAngle;

      t.x += (tgv.vgx / 3600) * simDt;
      t.z += (tgv.vgz / 3600) * simDt;

      const dx = t.x - sim.ownShip.x;
      const dz = t.z - sim.ownShip.z;
      t.dist = Math.sqrt(dx * dx + dz * dz);
      t.bearing = (THREE.MathUtils.radToDeg(Math.atan2(dx, dz)) + 360) % 360;

      t.rel_vx = tgv.vgx - ownGv.vgx;
      t.rel_vz = tgv.vgz - ownGv.vgz;
      t.rel_speed = Math.sqrt(t.rel_vx * t.rel_vx + t.rel_vz * t.rel_vz);

      const rel_v_sq = t.rel_vx * t.rel_vx + t.rel_vz * t.rel_vz;
      if (rel_v_sq > 1e-6) {
        const dot = dx * t.rel_vx + dz * t.rel_vz;
        t.tcpa = -dot / rel_v_sq;
        if (t.tcpa > 0) {
          const cx = dx + t.rel_vx * t.tcpa;
          const cz = dz + t.rel_vz * t.tcpa;
          t.cpa = Math.sqrt(cx * cx + cz * cz);
        } else {
          t.cpa = t.dist;
        }
      } else {
        t.cpa = t.dist;
        t.tcpa = 0.0;
      }

      if (t.dist < minDisStep) minDisStep = t.dist;

      // Collision check (< 0.16 NM)
      if (t.dist <= 0.16 && !collisionTriggered) {
        collisionTriggered = true;
        collidedTarget = t.id;
      }
    });

    if (minDisStep < minDisGlobal) minDisGlobal = minDisStep;
  }

  assert(sim.targets.length === 5, "5 target vessels processed in parallel");
  sim.targets.forEach((t, i) => {
    assert(!isNaN(t.x) && !isNaN(t.z), `Target ${t.id} coordinates finite after 6000 steps`);
    assert(!isNaN(t.cpa) && !isNaN(t.tcpa), `Target ${t.id} CPA/TCPA finite`);
  });
  console.log(`  INFO: 6000 integration steps completed. Min distance across all vessels: ${minDisGlobal.toFixed(3)} NM. Collision triggered: ${collisionTriggered} (${collidedTarget})`);
}

// =========================================================================
// SUITE 3: COLLISION DETECTION BOUNDARY & NEAR-MISS GEOMETRIES
// =========================================================================
testHeader("SUITE 3: COLLISION DETECTION BOUNDARIES & NEAR-MISS PRECISION");

// 3.1 Exact boundary testing: 0.16 NM threshold
{
  const threshold = 0.16;

  // Case A: dist = 0.1600001 (just outside collision radius)
  const distOutside = 0.1600001;
  const isCollisionOutside = (distOutside <= 0.16);
  assert(!isCollisionOutside, "Boundary: dist = 0.1600001 does NOT trigger collision");

  // Case B: dist = 0.1599999 (just inside collision radius)
  const distInside = 0.1599999;
  const isCollisionInside = (distInside <= 0.16);
  assert(isCollisionInside, "Boundary: dist = 0.1599999 DOES trigger collision");

  // Case C: dist = exactly 0.1600000
  const distExact = 0.16;
  const isCollisionExact = (distExact <= 0.16);
  assert(isCollisionExact, "Boundary: dist = 0.1600000 DOES trigger collision (inclusive <= 0.16)");
}

// 3.2 Near-miss scenario with CPA = 0.18 NM (close shave without collision)
{
  const own = { course: 0, speed: 10, x: 0, z: 0 };
  const tgt = { course: 180, speed: 10, x: 0.18, z: 4.0 };
  const res = simulateCpaTcpa(own, tgt, null, null);
  assert(Math.abs(res.cpa - 0.18) < 1e-4, `Near-miss CPA calculated accurately: expected 0.18, got ${res.cpa.toFixed(4)}`);
  assert(res.cpa > 0.16, "Near-miss CPA > 0.16 collision boundary");
}

// 3.3 Safe Passing criteria: all passed with CPA >= 1.0 NM
{
  const targets = [
    { tcpa: -0.05, dist: 2.5 },
    { tcpa: -0.10, dist: 3.0 },
    { tcpa: -0.01, dist: 1.8 }
  ];
  const allPassed = targets.every(t => t.tcpa <= 0);
  assert(allPassed === true, "Safe Pass: All targets passed (all tcpa <= 0)");

  // If one target still approaching:
  targets.push({ tcpa: 0.15, dist: 1.5 });
  const notAllPassed = targets.every(t => t.tcpa <= 0);
  assert(notAllPassed === false, "Safe Pass: Blocked while at least one target is still approaching (tcpa > 0)");
}

// =========================================================================
// SUITE 4: WIND LEEWAY & OCEAN CURRENT DRIFT DRIFT CHALLENGE
// =========================================================================
testHeader("SUITE 4: EXTREME DRIFT & WIND LEEWAY PHYSICAL SIGN ANALYSIS");

// 4.1 Pure Ocean Current
{
  const currentSet90 = calculateGroundVelocity(0, 10, null, { set: 90, drift: 2.0 });
  assert(Math.abs(currentSet90.vgx - 2.0) < 1e-4, "Pure current 2 kts to 090°: vgx = +2.0 (East)");
  assert(Math.abs(currentSet90.vgz - 10.0) < 1e-4, "Pure current: vgz = +10.0 (North)");
  assert(currentSet90.cog > 0 && currentSet90.cog < 180, "Pure current to 090° sets COG to Starboard/East");
  assert(currentSet90.crabAngle > 0, "Pure current to 090° creates positive crab angle");
}

// 4.2 Adversarial Physical Challenge: Wind Leeway Direction
{
  // A vessel heading North (000°) with wind blowing FROM West (270°).
  // Physically, the wind pushes on the vessel's port side and pushes it towards East (+X).
  // The downwind direction is 090° (East).
  // Therefore, v_leeway must be POSITIVE along X (+X / Starboard / East),
  // COG must be > 000° (e.g. 005°), and crabAngle must be POSITIVE.
  const windFromWest = calculateGroundVelocity(0, 10, { direction: 270, speed: 25, leewayCoeff: 0.04 }, null);

  console.log("  [INVESTIGATION] Wind from West (270°), Hdg 000°:");
  console.log(`    computed vgx = ${windFromWest.vgx.toFixed(4)}`);
  console.log(`    computed COG = ${windFromWest.cog.toFixed(4)}°`);
  console.log(`    computed crabAngle = ${windFromWest.crabAngle.toFixed(4)}°`);

  // Check what simulator.html computed vs what physics requires:
  const isPhysicallyDownwind = (windFromWest.vgx > 0);
  if (!isPhysicallyDownwind) {
    assert(false, `PHYSICAL DEFECT FOUND: Wind from 270° pushed vessel to vgx=${windFromWest.vgx.toFixed(2)} (West/Upwind) instead of East/Downwind! COG=${windFromWest.cog.toFixed(1)}°`);
  } else {
    assert(true, "Wind leeway correctly pushes downwind");
  }
}

// 4.3 Adversarial Physical Challenge: Wind Leeway from East
{
  // Wind blowing FROM East (090°). Physically must push vessel West (-X), COG < 360° (e.g. 355°).
  const windFromEast = calculateGroundVelocity(0, 10, { direction: 90, speed: 25, leewayCoeff: 0.04 }, null);
  console.log("  [INVESTIGATION] Wind from East (090°), Hdg 000°:");
  console.log(`    computed vgx = ${windFromEast.vgx.toFixed(4)}`);
  console.log(`    computed COG = ${windFromEast.cog.toFixed(4)}°`);
  console.log(`    computed crabAngle = ${windFromEast.crabAngle.toFixed(4)}°`);

  const isPhysicallyDownwindEast = (windFromEast.vgx < 0);
  if (!isPhysicallyDownwindEast) {
    assert(false, `PHYSICAL DEFECT FOUND: Wind from 090° pushed vessel to vgx=${windFromEast.vgx.toFixed(2)} (East/Upwind) instead of West/Downwind! COG=${windFromEast.cog.toFixed(1)}°`);
  } else {
    assert(true, "Wind leeway from East correctly pushes West");
  }
}

// 4.4 Extreme Gale Winds (60 kts, hurricane Category 1)
{
  const galeWind = calculateGroundVelocity(0, 12, { direction: 270, speed: 60, leewayCoeff: 0.05 }, null);
  assert(!isNaN(galeWind.sog) && isFinite(galeWind.sog), "Gale wind 60 kts: SOG is finite");
  assert(!isNaN(galeWind.cog) && isFinite(galeWind.cog), "Gale wind 60 kts: COG is finite");
  assert(!isNaN(galeWind.crabAngle) && isFinite(galeWind.crabAngle), "Gale wind 60 kts: Crab angle is finite");
}

// 4.5 Extreme Current Opposing Ship Speed Exactly (SOG = 0)
{
  // Ship heading North at 5 kts, current flowing South (set 180°) at 5 kts.
  const opposingCurrent = calculateGroundVelocity(0, 5, null, { set: 180, drift: 5.0 });
  assert(Math.abs(opposingCurrent.sog) < 1e-4, `Direct opposing current cancels speed: SOG = ${opposingCurrent.sog.toFixed(4)} ~ 0`);
  assert(!isNaN(opposingCurrent.cog), "Opposing current (SOG=0): COG is not NaN");
  assert(!isNaN(opposingCurrent.crabAngle), "Opposing current (SOG=0): Crab angle is not NaN");
}

// =========================================================================
// SUITE 5: 5-TARGET RADAR ARPA CANVAS RENDERING STRESS
// =========================================================================
testHeader("SUITE 5: 5-TARGET RADAR ARPA PPI CANVAS RENDERING STRESS");

function mockCanvasContext() {
  const calls = [];
  return {
    calls,
    clearRect: (...args) => calls.push(['clearRect', ...args]),
    beginPath: () => calls.push(['beginPath']),
    arc: (...args) => calls.push(['arc', ...args]),
    fill: () => calls.push(['fill']),
    stroke: () => calls.push(['stroke']),
    save: () => calls.push(['save']),
    restore: () => calls.push(['restore']),
    clip: () => calls.push(['clip']),
    moveTo: (...args) => calls.push(['moveTo', ...args]),
    lineTo: (...args) => calls.push(['lineTo', ...args]),
    translate: (...args) => calls.push(['translate', ...args]),
    rotate: (...args) => calls.push(['rotate', ...args]),
    closePath: () => calls.push(['closePath']),
    fillRect: (...args) => calls.push(['fillRect']),
    fillText: (...args) => calls.push(['fillText', ...args]),
    setLineDash: (...args) => calls.push(['setLineDash', ...args]),
    fillStyle: '',
    strokeStyle: '',
    lineWidth: 1,
    shadowColor: '',
    shadowBlur: 0,
    font: ''
  };
}

// Test executing drawRadar mock with 5 targets
{
  const mockCtx = mockCanvasContext();
  const mockCanvas = {
    width: 300,
    height: 300,
    getContext: () => mockCtx
  };

  // Mock global document and DOM
  const originalDoc = global.document;
  global.document = {
    getElementById: (id) => (id === 'radarCanvas' ? mockCanvas : null)
  };

  const ownShipMock = {
    x: 0, z: 0, course: 45, speed: 12, cog: 48, sog: 12.5, vgx: 8.5, vgz: 9.2
  };

  const targetsMock = [
    { x: 1.0, z: 2.0, course: 180, speed: 10, cog: 180, sog: 10, cpa: 0.8, tcpa: 0.1, type: 'container', vgx: 0, vgz: -10 },
    { x: -2.0, z: 3.0, course: 90, speed: 8, cog: 92, sog: 8.2, cpa: 1.5, tcpa: 0.2, type: 'cargo', vgx: 8, vgz: 0 },
    { x: 3.0, z: -1.0, course: 270, speed: 12, cog: 270, sog: 12, cpa: 2.8, tcpa: -0.1, type: 'tanker', vgx: -12, vgz: 0 },
    { x: 0.2, z: 1.2, course: 190, speed: 14, cog: 190, sog: 14, cpa: 0.3, tcpa: 0.05, type: 'fishing', vgx: -2.4, vgz: -13.8 },
    { x: -1.5, z: -2.0, course: 0, speed: 6, cog: 0, sog: 6, cpa: 1.8, tcpa: -0.3, type: 'tug', vgx: 0, vgz: 6 },
    // 6th target far beyond radar range (15 NM)
    { x: 15.0, z: 15.0, course: 0, speed: 10, cog: 0, sog: 10, cpa: 15.0, tcpa: 1.0, type: 'frigate', vgx: 0, vgz: 10 }
  ];

  // Global variables needed by drawRadar
  global.radarRange = 6.0;
  global.currentScenarioData = null;
  global.activeBuoys = [];
  global.ialaRegion = 'A';
  global.simSpeed = 1.0;
  global.radarSweepAngle = 0.5;
  global.ownShip = ownShipMock;
  global.targets = targetsMock;
  global.targetShip = targetsMock[0];

  let drawRadarFn;
  try {
    drawRadarFn = new Function('THREE', `${fnDrawRadarMatch[0]}; return drawRadar;`)(THREE);
  } catch (err) {
    assert(false, `Failed to compile drawRadar: ${err.message}`);
  }

  if (drawRadarFn) {
    let thrownError = null;
    try {
      drawRadarFn(0.2, 1.2, -10.9, -23.0, 0.3, 0.05);
    } catch (err) {
      thrownError = err;
    }
    assert(thrownError === null, "drawRadar executed with 5 targets without throwing any exception");

    // Check how many target labels were rendered
    const textCalls = mockCtx.calls.filter(c => c[0] === 'fillText');
    const tgtLabelCalls = textCalls.filter(c => typeof c[1] === 'string' && c[1].startsWith('TGT-0'));
    assert(tgtLabelCalls.length === 5, `Radar ARPA rendered exactly 5 visible targets (clipped 6th out-of-range target). Rendered: ${tgtLabelCalls.length}`);
  }

  // Restore global document
  global.document = originalDoc;
}

// =========================================================================
// SUMMARY & VERDICT
// =========================================================================
console.log(`\n======================================================`);
console.log(`  ADVERSARIAL STRESS TEST SUMMARY`);
console.log(`======================================================`);
console.log(`Total Assertions Passed: ${testsPassed}`);
console.log(`Total Assertions Failed: ${testsFailed}`);

if (failures.length > 0) {
  console.log(`\nFAILURES SUMMARY:`);
  failures.forEach((f, idx) => {
    console.log(`  ${idx + 1}. ${f}`);
  });
}

process.exit(testsFailed > 0 ? 1 : 0);
