
    const NM_SCALE = 35.0; // 1 NM in world coordinates is 35 units for realistic close visual rendering

    // Target Vessel Definitions with Rule 18 hierarchy & Visual Details
    const TARGET_VESSEL_TYPES = {
      power: {
        id: 'power',
        name: 'Tàu cơ giới thông thường',
        dayTitle: '☀️ DẤU HIỆU NGÀY: Tàu cơ giới thường',
        dayDesc: 'Không mang dấu hiệu đặc biệt trên cột buồm. Áp dụng quy tắc thông thường (Rule 14/15/13).',
        nightTitle: '🌙 ĐÈN ĐÊM: Đèn cột trắng + Đèn mạn Xanh/Đỏ',
        nightDesc: 'Đèn cột trắng chiếu trước (225°), đèn mạn Xanh phải / Đỏ trái (112.5°), đèn lái trắng (135°).',
        rhyme: 'Mạn trái gặp mạn phải: Tránh nhau mạn trái - mạn trái (Port to Port)',
        ruleText: 'Hai tàu cùng cấp cơ giới, áp dụng quy tắc hướng tiếp cận tiêu chuẩn.',
        ruleAlert: 'Tuân theo Rule 14 (Đối đầu), Rule 15 (Cắt hướng), Rule 13 (Vượt).',
        priority: 1, // Lowest priority (Power-driven)
        shapes: [],
        nightSpecials: []
      },
      nuc: {
        id: 'nuc',
        name: 'Tàu mất khả năng điều động (NUC - Rule 27a)',
        dayTitle: '☀️ DẤU HIỆU NGÀY: 2 Quả cầu đen thẳng đứng (● ●)',
        dayDesc: 'Hai quả cầu đen trên cột buồm ("Two black balls"). Tàu bị sự cố máy lái hoặc mất điện, KHÔNG THỂ chuyển hướng!',
        nightTitle: '🌙 ĐÈN ĐÊM: 2 Đèn ĐỎ thẳng đứng (🔴 🔴) [Đỏ trên Đỏ]',
        nightDesc: 'Hai đèn đỏ chiếu vòng 360°. Cùng đèn mạn khi đang còn trôi dạt trên mặt nước.',
        rhyme: 'Khẩu quyết: "ĐỎ TRÊN ĐỎ - TRỤC TRẶC TRÁNH XA!"',
        ruleText: 'Quy tắc 18(a)(i): Tàu cơ giới đang hành trình BẮT BUỘC PHẢI NHƯỜNG ĐƯỜNG cho tàu mất khả năng điều động (NUC).',
        ruleAlert: '⚠ BẮT BUỘC NHƯỜNG ĐƯỜNG (RULE 18): Tàu bạn không thể tránh ta. Tàu ta phải chủ động bẻ lái sang phải tránh xa, tuyệt đối không đòi quyền ưu tiên!',
        priority: 5, // Highest priority
        shapes: ['ball', 'ball'],
        nightSpecials: ['red', 'red']
      },
      ram: {
        id: 'ram',
        name: 'Tàu hạn chế điều động (RAM - Rule 27b)',
        dayTitle: '☀️ DẤU HIỆU NGÀY: Quả cầu - Quả trám - Quả cầu (● ◆ ●)',
        dayDesc: 'Đang làm công việc đặc biệt (đặt cáp ngầm, nạo vét luồng, tiếp dầu). Khả năng chuyển hướng bị hạn chế!',
        nightTitle: '🌙 ĐÈN ĐÊM: Đỏ - Trắng - Đỏ thẳng đứng (🔴 ⚪ 🔴)',
        nightDesc: 'Ba đèn chiếu vòng 360° xếp thẳng đứng. Đèn đỏ trên và dưới, đèn trắng ở giữa.',
        rhyme: 'Khẩu quyết: "ĐỎ - TRẮNG - ĐỎ: ĐANG LÀM VIỆC KHÓ!"',
        ruleText: 'Quy tắc 18(a)(ii): Tàu cơ giới BẮT BUỘC PHẢI TRÁNH ĐƯỜNG cho tàu bị hạn chế khả năng điều động (RAM).',
        ruleAlert: '⚠ BẮT BUỘC NHƯỜNG ĐƯỜNG (RULE 18): Tàu bạn đang thực hiện công vụ đặc biệt. Tàu ta phải đổi hướng tránh rộng ra xa!',
        priority: 4,
        shapes: ['ball', 'diamond', 'ball'],
        nightSpecials: ['red', 'white', 'red']
      },
      fishing: {
        id: 'fishing',
        name: 'Tàu đánh cá kéo lưới (Trawler - Rule 26)',
        dayTitle: '☀️ DẤU HIỆU NGÀY: Hai hình nón úp đỉnh vào nhau (▼▲)',
        dayDesc: 'Hình đồng hồ cát / 2 nón úp đỉnh. Đang kéo lưới rê ngầm dưới nước, khả năng cơ động rất kém.',
        nightTitle: '🌙 ĐÈN ĐÊM: Xanh lục trên - Trắng dưới (🟢 ⚪)',
        nightDesc: 'Hai đèn chiếu vòng 360°. Đèn xanh lục phía trên, đèn trắng phía dưới.',
        rhyme: 'Khẩu quyết: "GREEN OVER WHITE - TRAWLING AT NIGHT!"',
        ruleText: 'Quy tắc 18(a)(iii): Tàu cơ giới BẮT BUỘC PHẢI NHƯỜNG ĐƯỜNG cho tàu đang đánh cá.',
        ruleAlert: '⚠ NHƯỜNG ĐƯỜNG CHO TÀU CÁ (RULE 18): Chú ý cự ly an toàn tránh vướng vào lưới kéo của tàu bạn!',
        priority: 3,
        shapes: ['hourglass'],
        nightSpecials: ['green', 'white']
      },
      pilot: {
        id: 'pilot',
        name: 'Tàu hoa tiêu đang trực (Pilot - Rule 29)',
        dayTitle: '☀️ DẤU HIỆU NGÀY: Cờ hiệu hoa tiêu trắng/đỏ (Cờ Hotel)',
        dayDesc: 'Tàu đang làm nhiệm vụ hoa tiêu dẫn dắt tàu ra vào luồng lạch cảng biển.',
        nightTitle: '🌙 ĐÈN ĐÊM: Trắng trên - Đỏ dưới (⚪ 🔴)',
        nightDesc: 'Hai đèn chiếu vòng 360° ở cột buồm. Trắng ở trên, Đỏ ở dưới.',
        rhyme: 'Khẩu quyết: "WHITE OVER RED - PILOT AHEAD!"',
        ruleText: 'Quy tắc 29: Tàu làm nhiệm vụ hoa tiêu. Cần cảnh giới cao độ, giữ cự ly tiếp cận an toàn.',
        ruleAlert: 'ℹ TÀU HOA TIÊU ĐANG DẪN LUỒNG: Chủ động liên lạc VHF, giảm tốc độ và duy trì cảnh giới an toàn.',
        priority: 2,
        shapes: ['flag_pilot'],
        nightSpecials: ['white', 'red']
      },
      anchored: {
        id: 'anchored',
        name: 'Tàu đang thả neo (Anchored - Rule 30)',
        dayTitle: '☀️ DẤU HIỆU NGÀY: 1 Quả cầu đen ở mũi tàu (●)',
        dayDesc: 'Một quả cầu đen treo nơi dễ thấy nhất ở phần mũi tàu (forecastle).',
        nightTitle: '🌙 ĐÈN ĐÊM: Đèn trắng chiếu 360° ở mũi tàu (⚪)',
        nightDesc: 'Một hoặc hai đèn trắng chiếu vòng quanh 360°. Tàu đứng yên cố định dưới đáy biển.',
        rhyme: 'Khẩu quyết: "1 QUẢ CẦU MŨI: TÀU ĐANG ĐỨNG NEO!"',
        ruleText: 'Quy tắc 30: Tàu đang thả neo. Tàu không có vận tốc, đứng yên trên mặt nước.',
        ruleAlert: '⚠ TÀU ĐANG ĐỨNG NEO: Tàu bạn không thể di chuyển. Tàu ta bắt buộc phải chủ động bẻ lái tránh xa!',
        priority: 5,
        shapes: ['ball_bow'],
        nightSpecials: ['white_allround']
      }
    };

    // Scenarios Configuration (Visual encounter at ~1.0 - 1.2 NM)
    const SCENARIOS = {
      head_on: {
        id: 'head_on',
        name: 'Tình huống 1: Đối đầu trực diện (Head-on - Rule 14)',
        rule: 'Quy tắc 14: Tình huống Đối đầu Trực diện (Head-on Situation)',
        text: 'Hai tàu cơ giới đang đi ngược chiều hoặc gần ngược chiều, có nguy cơ đâm va trực tiếp. Cả hai tàu đều phải chủ động bẻ lái sang mạn phải (Starboard) để tránh nhau mạn trái - mạn trái (Port to Port).',
        alert: '⚠ BẮT BUỘC: Cả hai tàu đều là tàu phải hành động (Give-way). Nghiêm cấm bẻ lái sang mạn trái cắt mũi tàu đối diện!',
        own: { course: 0, speed: 13, x: 0, z: -0.6 },
        target: { course: 180, speed: 13, x: 0, z: 0.6 },
        type: 'head_on'
      },
      crossing_give_way: {
        id: 'crossing_give_way',
        name: 'Tình huống 2: Cắt hướng mạn phải - Nhường đường (Crossing Give-way - Rule 15)',
        rule: 'Quy tắc 15: Tình huống Cắt hướng - Tàu Nhường Đường (Give-way Vessel)',
        text: 'Tàu mục tiêu ở phía mạn phải (Starboard side) của Tàu ta. Tàu của ta BẮT BUỘC phải nhường đường và không được cắt ngang trước mũi tàu bạn.',
        alert: '⚠ QUY ĐỊNH: Bẻ lái dứt khoát sang mạn phải để vòng qua sau lái tàu mục tiêu hoặc giảm tốc độ an toàn.',
        own: { course: 0, speed: 13, x: 0, z: -0.5 },
        target: { course: 270, speed: 12, x: 0.9, z: 0.1 },
        type: 'crossing_give_way'
      },
      crossing_stand_on: {
        id: 'crossing_stand_on',
        name: 'Tình huống 3: Cắt hướng mạn trái - Giữ hướng (Crossing Stand-on - Rule 15)',
        rule: 'Quy tắc 15 & 17: Tình huống Cắt hướng - Tàu Được Ưu Tiên (Stand-on Vessel)',
        text: 'Tàu mục tiêu ở phía mạn trái của Tàu ta. Tàu của ta là tàu được quyền ưu tiên đường đi. Tàu ta phải duy trì ổn định hướng đi và vận tốc để tàu kia dễ dàng tính toán cơ động.',
        alert: 'ℹ NGHĨA VỤ: Giữ nguyên hướng và vận tốc (Stand-on). Sẵn sàng can thiệp nếu tàu nhường đường không hành động.',
        own: { course: 0, speed: 13, x: 0, z: -0.5 },
        target: { course: 090, speed: 12, x: -0.9, z: 0.1 },
        type: 'crossing_stand_on'
      },
      overtaking_give_way: {
        id: 'overtaking_give_way',
        name: 'Tình huống 4: Vượt tàu khác (Overtaking Give-way - Rule 13)',
        rule: 'Quy tắc 13: Tàu Vượt (Overtaking Vessel)',
        text: 'Tàu của ta đang tiếp cận từ sau góc 22.5° sau mạn ngang của tàu phía trước với vận tốc lớn hơn. Bất kể vị trí nào, tàu vượt luôn phải chủ động tránh đường cho tàu được vượt.',
        alert: '⚠ BẮT BUỘC: Giữ cự ly cách biệt an toàn sang mạn trái hoặc mạn phải cho đến khi vượt qua hoàn toàn.',
        own: { course: 0, speed: 18, x: 0, z: -0.7 },
        target: { course: 0, speed: 8, x: 0, z: 0.1 },
        type: 'overtaking_give_way'
      },
      overtaking_stand_on: {
        id: 'overtaking_stand_on',
        name: 'Tình huống 5: Bị tàu khác vượt (Being Overtaken Stand-on - Rule 13)',
        rule: 'Quy tắc 13 & 17: Tàu Được Vượt (Vessel Being Overtaken)',
        text: 'Tàu mục tiêu từ phía sau đang chạy nhanh hơn để vượt Tàu ta. Tàu ta có nghĩa vụ giữ nguyên hướng và tốc độ ổn định, hỗ trợ cho tàu vượt thao tác an toàn.',
        alert: 'ℹ NGHĨA VỤ: Duy trì hướng và vận tốc; không đổi hướng đột ngột cản trở tàu đang vượt.',
        own: { course: 0, speed: 8, x: 0, z: 0.1 },
        target: { course: 0, speed: 17, x: 0.15, z: -0.7 },
        type: 'overtaking_stand_on'
      },
      custom: {
        id: 'custom',
        name: 'Tình huống 6: Sa bàn tự do (Free Maneuvering)',
        rule: 'Mô phỏng Sa Bàn Tự Do - Thực Hành Tránh Va Tùy Biến',
        text: 'Tự do thay đổi hướng đi, vận tốc, góc lái và cự ly của cả hai tàu để nghiên cứu quy luật tiếp cận, tam giác vận tốc và điểm CPA trên biển.',
        alert: '💡 Thử nghiệm các tình huống tiếp cận đa dạng và theo dõi phản ứng trên Radar ARPA.',
        own: { course: 0, speed: 13, x: 0, z: -0.6 },
        target: { course: 180, speed: 13, x: 0.3, z: 0.6 },
        type: 'custom'
      }
    };

    // State Variables
    let currentScenarioId = 'head_on';
    let targetVesselType = 'power';
    let isDayMode = true;
    let initialDistSetting = 1.2;
    let simSpeed = 1.0;
    let isPaused = false;
    let radarRange = 1.5;
    let radarMode = 'north_up';
    let cameraMode = 'orbit';

    // Ship State (Coordinates in NM: +X = East, +Z = North)
    let ownShip = {
      x: 0, z: 0,
      course: 0,
      targetHeading: null,
      speed: 13.0,
      rudder: 0.0,
      rot: 0.0,
      mesh: null
    };

    let targetShip = {
      x: 0, z: 0,
      course: 180,
      speed: 13.0,
      mesh: null,
      dayShapesGroup: null,
      specialLights: []
    };

    let baseOwnCourse = 0;
    let baseOwnSpeed = 13;
    let minDistanceRecorded = 999.0;
    let hasCollided = false;
    let hasSafelyPassed = false;
    let score = 100;

    // Three.js Globals
    let scene, camera, renderer, controls;
    let waterMesh, sunLight, ambientLight;
    let wakeParticles = [];
    let explosionParticles = [];
    let safeSparkles = [];
    let radarSweepAngle = 0;
    let screenShake = 0;

    // Initialize 3D Engine
    function init3D() {
      const container = document.getElementById('canvas-container');
      const width = window.innerWidth;
      const height = window.innerHeight;

      scene = new THREE.Scene();
      scene.fog = new THREE.FogExp2(0x87ceeb, 0.0035);

      // Camera
      camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1500);
      camera.position.set(0, 14, -22);

      // Renderer
      renderer = new THREE.WebGLRenderer({ antialias: true, powerPreference: 'high-performance' });
      renderer.setSize(width, height);
      renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
      renderer.shadowMap.enabled = true;
      renderer.shadowMap.type = THREE.PCFSoftShadowMap;
      container.appendChild(renderer.domElement);

      // OrbitControls
      controls = new THREE.OrbitControls(camera, renderer.domElement);
      controls.enableDamping = true;
      controls.dampingFactor = 0.06;
      controls.maxPolarAngle = Math.PI / 2 - 0.02;
      controls.minDistance = 2;
      controls.maxDistance = 140;
      controls.target.set(0, 1, 0);

      // Lighting
      ambientLight = new THREE.AmbientLight(0xffffff, 1.25);
      scene.add(ambientLight);

      sunLight = new THREE.DirectionalLight(0xfffaed, 1.6);
      sunLight.position.set(50, 70, -40);
      sunLight.castShadow = true;
      sunLight.shadow.mapSize.width = 1024;
      sunLight.shadow.mapSize.height = 1024;
      scene.add(sunLight);

      // Ocean Plane & Grid
      createOcean();

      // Create Realistic 3D Ship Models
      ownShip.mesh = buildRealisticShip(0x1565c0, 0xf5f5f5, 'own');
      scene.add(ownShip.mesh);

      targetShip.mesh = buildRealisticShip(0xc62828, 0x37474f, 'target');
      scene.add(targetShip.mesh);

      // Apply initial day/night state
      applyDayNightTheme(true);

      // Window resize listener
      window.addEventListener('resize', onWindowResize);

      // Load First Scenario
      loadScenario('head_on');

      // Start Animation Loop
      animate();
    }

    function createOcean() {
      const gridHelper = new THREE.GridHelper(300, 150, 0x00e5ff, 0x194559);
      gridHelper.position.y = 0.01;
      gridHelper.name = 'oceanGrid';
      scene.add(gridHelper);

      const planeGeo = new THREE.PlaneGeometry(450, 450, 64, 64);
      planeGeo.rotateX(-Math.PI / 2);
      const planeMat = new THREE.MeshStandardMaterial({
        color: 0x0a3248,
        roughness: 0.25,
        metalness: 0.6,
      });
      waterMesh = new THREE.Mesh(planeGeo, planeMat);
      waterMesh.receiveShadow = true;
      scene.add(waterMesh);
    }

    // ========================================================
    // BUILD HIGHLY REALISTIC 3D SHIP MODEL
    // Detailed hull, flared bow, bulbous bow, bridge wings,
    // deck cranes, cargo container stacks, masts, and lights!
    // ========================================================
    function buildRealisticShip(hullColor, cabinColor, type) {
      const shipGroup = new THREE.Group();

      // 1. Sleek Realistic Hull (Length: 6.8 units, Width: 1.6 units)
      const hullGroup = new THREE.Group();

      // Main Topsides Hull
      const mainHullGeo = new THREE.BoxGeometry(1.6, 0.65, 6.4);
      const pos = mainHullGeo.attributes.position;
      for (let i = 0; i < pos.count; i++) {
        let z = pos.getZ(i);
        let x = pos.getX(i);
        let y = pos.getY(i);
        if (z > 1.2) {
          // Taper forward bow with flared sheer
          const f = (z - 1.2) / 2.0;
          pos.setX(i, x * (1 - f * 0.65));
        } else if (z < -2.4) {
          // Rounded transom stern
          const f = (-z - 2.4) / 0.8;
          pos.setX(i, x * (1 - f * 0.35));
        }
      }
      mainHullGeo.computeVertexNormals();
      const hullMat = new THREE.MeshStandardMaterial({ color: hullColor, roughness: 0.35, metalness: 0.35 });
      const hull = new THREE.Mesh(mainHullGeo, hullMat);
      hull.position.y = 0.5;
      hull.castShadow = true;
      hull.receiveShadow = true;
      hullGroup.add(hull);

      // Red Underwater Keel / Waterline (Anti-fouling red bottom)
      const keelGeo = new THREE.BoxGeometry(1.5, 0.3, 6.2);
      const keelMat = new THREE.MeshStandardMaterial({ color: 0x8b1a1a, roughness: 0.6 });
      const keel = new THREE.Mesh(keelGeo, keelMat);
      keel.position.y = 0.15;
      hullGroup.add(keel);

      // Bulbous Bow (Mũi quả lê ngầm rẽ sóng)
      const bulbGeo = new THREE.SphereGeometry(0.28, 12, 12);
      bulbGeo.scale(1, 0.8, 1.8);
      const bulb = new THREE.Mesh(bulbGeo, keelMat);
      bulb.position.set(0, 0.18, 3.2);
      hullGroup.add(bulb);

      // Forecastle raised bow deck (Boong mũi cao che sóng)
      const fcastleGeo = new THREE.BoxGeometry(1.45, 0.25, 1.4);
      const fcastle = new THREE.Mesh(fcastleGeo, hullMat);
      fcastle.position.set(0, 0.85, 2.5);
      hullGroup.add(fcastle);

      // Mooring Windlass on bow (Tời neo & xích neo)
      const windlassGeo = new THREE.CylinderGeometry(0.12, 0.12, 0.4);
      windlassGeo.rotateZ(Math.PI / 2);
      const windlassMat = new THREE.MeshStandardMaterial({ color: 0x222222, metalness: 0.7 });
      const windlass = new THREE.Mesh(windlassGeo, windlassMat);
      windlass.position.set(0, 1.05, 2.6);
      hullGroup.add(windlass);

      shipGroup.add(hullGroup);

      // 2. Multi-tier Navigation Bridge & Superstructure (Aft at -Z)
      const bridgeGroup = new THREE.Group();

      // Lower accommodation block
      const accomGeo = new THREE.BoxGeometry(1.4, 0.7, 1.6);
      const accomMat = new THREE.MeshStandardMaterial({ color: cabinColor, roughness: 0.3 });
      const accom = new THREE.Mesh(accomGeo, accomMat);
      accom.position.set(0, 1.15, -1.3);
      bridgeGroup.add(accom);

      // Navigation Bridge Deckhouse with extended Bridge Wings (Cánh buồng lái)
      const bridgeDeckGeo = new THREE.BoxGeometry(2.1, 0.45, 0.9); // Wings extend to 2.1 width!
      const bridgeDeck = new THREE.Mesh(bridgeDeckGeo, accomMat);
      bridgeDeck.position.set(0, 1.7, -1.1);
      bridgeGroup.add(bridgeDeck);

      // Slanted Panoramic Windows (Kính buồng lái)
      const winGeo = new THREE.BoxGeometry(1.3, 0.22, 0.3);
      const winMat = new THREE.MeshBasicMaterial({ color: 0x81d4fa });
      const win = new THREE.Mesh(winGeo, winMat);
      win.position.set(0, 1.72, -0.65);
      bridgeGroup.add(win);

      // Chimney / Exhaust Funnel (Ống khói tàu phía sau lái)
      const funnelGeo = new THREE.CylinderGeometry(0.18, 0.22, 0.9, 8);
      const funnelMat = new THREE.MeshStandardMaterial({ color: 0x212121, roughness: 0.5 });
      const funnel = new THREE.Mesh(funnelGeo, funnelMat);
      funnel.position.set(0, 2.1, -1.8);
      bridgeGroup.add(funnel);

      // Satellite Communication Domes (Vòm radar vệ tinh trắng Inmarsat)
      const domeGeo = new THREE.SphereGeometry(0.14, 10, 10);
      const domeMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const dome1 = new THREE.Mesh(domeGeo, domeMat);
      dome1.position.set(0.5, 2.05, -1.2);
      bridgeGroup.add(dome1);
      const dome2 = new THREE.Mesh(domeGeo, domeMat);
      dome2.position.set(-0.5, 2.05, -1.2);
      bridgeGroup.add(dome2);

      // Lifeboats on Davits (Xuồng cứu sinh cam hai bên mạn)
      const boatGeo = new THREE.CapsuleGeometry ? new THREE.CapsuleGeometry(0.1, 0.35, 4, 8) : new THREE.CylinderGeometry(0.1, 0.1, 0.4);
      boatGeo.rotateX(Math.PI / 2);
      const boatMat = new THREE.MeshStandardMaterial({ color: 0xff6d00, roughness: 0.4 });
      const boatL = new THREE.Mesh(boatGeo, boatMat);
      boatL.position.set(-0.85, 1.4, -1.3);
      bridgeGroup.add(boatL);
      const boatR = new THREE.Mesh(boatGeo, boatMat);
      boatR.position.set(0.85, 1.4, -1.3);
      bridgeGroup.add(boatR);

      shipGroup.add(bridgeGroup);

      // 3. Forward Cargo Containers & Deck Cranes (+Z Deck)
      const cargoGroup = new THREE.Group();

      // Colored Container Stacks
      const contColors = [0x00838f, 0xef6c00, 0x1565c0, 0x2e7d32, 0xc62828];
      for (let bay = 0; bay < 3; bay++) {
        const cGeo = new THREE.BoxGeometry(1.2, 0.5, 0.7);
        const cMat = new THREE.MeshStandardMaterial({
          color: contColors[(bay + (type === 'own' ? 0 : 2)) % contColors.length],
          roughness: 0.7
        });
        const cMesh = new THREE.Mesh(cGeo, cMat);
        cMesh.position.set(0, 1.05, 0.3 + bay * 0.8);
        cargoGroup.add(cMesh);

        // Top tier container
        const cTopGeo = new THREE.BoxGeometry(1.15, 0.4, 0.68);
        const cTopMat = new THREE.MeshStandardMaterial({
          color: contColors[(bay + 1) % contColors.length],
          roughness: 0.7
        });
        const cTop = new THREE.Mesh(cTopGeo, cTopMat);
        cTop.position.set(0, 1.45, 0.3 + bay * 0.8);
        cargoGroup.add(cTop);
      }

      // Deck Crane between bays
      const cranePostGeo = new THREE.CylinderGeometry(0.06, 0.07, 1.0);
      const cranePost = new THREE.Mesh(cranePostGeo, new THREE.MeshBasicMaterial({ color: 0xffeb3b }));
      cranePost.position.set(0, 1.3, 1.5);
      cargoGroup.add(cranePost);

      shipGroup.add(cargoGroup);

      // 4. Masts & Radar Scanners
      // Foremast (Cột mũi)
      const foremastGeo = new THREE.CylinderGeometry(0.04, 0.05, 1.8);
      const mastMat = new THREE.MeshBasicMaterial({ color: 0xeeeeee });
      const foremast = new THREE.Mesh(foremastGeo, mastMat);
      foremast.position.set(0, 1.8, 2.5);
      shipGroup.add(foremast);

      // Mainmast with Yardarm (Cột chính buồng lái có xà ngang)
      const mainmastGeo = new THREE.CylinderGeometry(0.04, 0.05, 2.4);
      const mainmast = new THREE.Mesh(mainmastGeo, mastMat);
      mainmast.position.set(0, 2.9, -1.0);
      shipGroup.add(mainmast);

      // Horizontal Yardarm on mainmast (Xà ngang treo đèn/dấu hiệu)
      const yardarmGeo = new THREE.CylinderGeometry(0.02, 0.02, 1.2);
      yardarmGeo.rotateZ(Math.PI / 2);
      const yardarm = new THREE.Mesh(yardarmGeo, mastMat);
      yardarm.position.set(0, 3.6, -1.0);
      shipGroup.add(yardarm);

      // Rotating ARPA Radar Scanner
      const scannerGeo = new THREE.BoxGeometry(0.65, 0.08, 0.12);
      const scanner = new THREE.Mesh(scannerGeo, new THREE.MeshBasicMaterial({ color: 0xffffff }));
      scanner.position.set(0, 4.2, -1.0);
      scanner.name = 'radarScanner';
      shipGroup.add(scanner);

      // Bow Arrow Heading Indicator
      const arrowGeo = new THREE.ConeGeometry(0.2, 0.6, 8);
      arrowGeo.rotateX(Math.PI / 2);
      const arrow = new THREE.Mesh(arrowGeo, new THREE.MeshBasicMaterial({ color: type === 'own' ? 0x00e5ff : 0xff5252 }));
      arrow.position.set(0, 1.2, 3.3);
      shipGroup.add(arrow);

      // 5. Navigation Lights with Dynamic PointLights
      const navLightsGroup = new THREE.Group();

      // Starboard Light (Green) on right bridge wing (+X)
      const stbdLight = new THREE.Mesh(new THREE.SphereGeometry(0.09, 8, 8), new THREE.MeshBasicMaterial({ color: 0x00e676 }));
      stbdLight.position.set(1.05, 1.8, -0.9);
      navLightsGroup.add(stbdLight);
      const stbdPoint = new THREE.PointLight(0x00e676, 1.5, 12);
      stbdPoint.position.set(1.1, 1.8, -0.9);
      navLightsGroup.add(stbdPoint);

      // Port Light (Red) on left bridge wing (-X)
      const portLight = new THREE.Mesh(new THREE.SphereGeometry(0.09, 8, 8), new THREE.MeshBasicMaterial({ color: 0xff1744 }));
      portLight.position.set(-1.05, 1.8, -0.9);
      navLightsGroup.add(portLight);
      const portPoint = new THREE.PointLight(0xff1744, 1.5, 12);
      portPoint.position.set(-1.1, 1.8, -0.9);
      navLightsGroup.add(portPoint);

      // Foremast White Headlight
      const whiteLightMat = new THREE.MeshBasicMaterial({ color: 0xffffff });
      const foreLight = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), whiteLightMat);
      foreLight.position.set(0, 2.6, 2.5);
      navLightsGroup.add(foreLight);

      // Mainmast White Headlight
      const mainLight = new THREE.Mesh(new THREE.SphereGeometry(0.09, 8, 8), whiteLightMat);
      mainLight.position.set(0, 3.9, -1.0);
      navLightsGroup.add(mainLight);

      // Stern Light (White)
      const sternLight = new THREE.Mesh(new THREE.SphereGeometry(0.08, 8, 8), whiteLightMat);
      sternLight.position.set(0, 1.1, -3.15);
      navLightsGroup.add(sternLight);

      // Special Vertical All-Round Signal Lights on Mainmast (for NUC, RAM, Pilot, Fishing, etc.)
      const specialLights = [];
      const specY = [3.5, 3.1, 2.7];
      for (let i = 0; i < 3; i++) {
        const specMesh = new THREE.Mesh(new THREE.SphereGeometry(0.1, 8, 8), new THREE.MeshBasicMaterial({ color: 0xffffff }));
        specMesh.position.set(0, specY[i], -0.85);
        specMesh.visible = false;
        navLightsGroup.add(specMesh);

        const specPoint = new THREE.PointLight(0xffffff, 1.0, 10);
        specPoint.position.set(0, specY[i], -0.75);
        specPoint.visible = false;
        navLightsGroup.add(specPoint);

        specialLights.push({ mesh: specMesh, point: specPoint });
      }

      shipGroup.add(navLightsGroup);
      if (type === 'target') {
        targetShip.specialLights = specialLights;
      }

      // 6. Day Shapes (Quả cầu đen, quả trám đen, hình nón)
      const dayShapesGroup = new THREE.Group();
      const dayMat = new THREE.MeshStandardMaterial({ color: 0x111111, roughness: 0.95 });

      // Top Shape: Sphere
      const shapeTop = new THREE.Mesh(new THREE.SphereGeometry(0.24, 12, 12), dayMat);
      shapeTop.position.set(0, 3.5, -0.85);
      shapeTop.name = 'shapeTop';
      shapeTop.visible = false;
      dayShapesGroup.add(shapeTop);

      // Middle Shape: Diamond (Octahedron)
      const shapeMid = new THREE.Mesh(new THREE.OctahedronGeometry(0.28, 0), dayMat);
      shapeMid.position.set(0, 2.9, -0.85);
      shapeMid.name = 'shapeMid';
      shapeMid.visible = false;
      dayShapesGroup.add(shapeMid);

      // Bottom Shape: Sphere
      const shapeBot = new THREE.Mesh(new THREE.SphereGeometry(0.24, 12, 12), dayMat);
      shapeBot.position.set(0, 2.3, -0.85);
      shapeBot.name = 'shapeBot';
      shapeBot.visible = false;
      dayShapesGroup.add(shapeBot);

      // Bow Anchor Ball
      const shapeBow = new THREE.Mesh(new THREE.SphereGeometry(0.26, 12, 12), dayMat);
      shapeBow.position.set(0, 2.5, 2.5);
      shapeBow.name = 'shapeBow';
      shapeBow.visible = false;
      dayShapesGroup.add(shapeBow);

      // Fishing Hourglass (Hai hình nón úp đỉnh)
      const coneTop = new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.38, 10), dayMat);
      coneTop.rotation.x = Math.PI;
      coneTop.position.set(0, 3.2, -0.85);
      const coneBot = new THREE.Mesh(new THREE.ConeGeometry(0.24, 0.38, 10), dayMat);
      coneBot.position.set(0, 2.82, -0.85);
      const hgGroup = new THREE.Group();
      hgGroup.name = 'shapeHourglass';
      hgGroup.add(coneTop);
      hgGroup.add(coneBot);
      hgGroup.visible = false;
      dayShapesGroup.add(hgGroup);

      shipGroup.add(dayShapesGroup);
      if (type === 'target') {
        targetShip.dayShapesGroup = dayShapesGroup;
      }

      return shipGroup;
    }

    // Toggle Day / Night Mode
    function toggleDayNight() {
      isDayMode = !isDayMode;
      applyDayNightTheme(isDayMode);
    }

    function applyDayNightTheme(day) {
      const btn = document.getElementById('btnDayNight');
      if (day) {
        btn.textContent = '☀️ Ban Ngày (Day)';
        btn.classList.remove('night');
        scene.background = new THREE.Color(0x7ac1eb);
        scene.fog.color = new THREE.Color(0x87ceeb);
        ambientLight.color.setHex(0xffffff);
        ambientLight.intensity = 1.35;
        sunLight.color.setHex(0xfffaed);
        sunLight.intensity = 1.7;
        waterMesh.material.color.setHex(0x0e3f5c);

        const grid = scene.getObjectByName('oceanGrid');
        if (grid) grid.material.color.setHex(0x0288d1);
      } else {
        btn.textContent = '🌙 Ban Đêm (Night)';
        btn.classList.add('night');
        scene.background = new THREE.Color(0x02070e);
        scene.fog.color = new THREE.Color(0x030d17);
        ambientLight.color.setHex(0x192d3f);
        ambientLight.intensity = 0.35;
        sunLight.color.setHex(0x81d4fa);
        sunLight.intensity = 0.45;
        waterMesh.material.color.setHex(0x011320);

        const grid = scene.getObjectByName('oceanGrid');
        if (grid) grid.material.color.setHex(0x00e5ff);
      }

      updateTargetVesselVisuals();
      drawVisualRecognitionDiagram();
    }

    // Target Vessel Type Changed Handler -> ADAPTS RULE 18 AND VISUALS!
    function setTargetVesselType(typeKey) {
      targetVesselType = typeKey;
      adaptScenarioRules();
      updateTargetVesselVisuals();
      drawVisualRecognitionDiagram();
    }

    // DYNAMIC RULE ADAPTATION: Rule 18 takes precedence over normal scenario rules
    function adaptScenarioRules() {
      const def = TARGET_VESSEL_TYPES[targetVesselType] || TARGET_VESSEL_TYPES.power;
      const s = SCENARIOS[currentScenarioId];

      const colregsTitle = document.getElementById('colregsTitle');
      const colregsText = document.getElementById('colregsText');
      const colregsAlert = document.getElementById('colregsAlert');

      if (def.priority >= 3) {
        // High priority vessel (NUC, RAM, Fishing, Anchored): OVERRIDES standard scenario
        colregsTitle.innerHTML = `<span>📖</span> ${def.ruleText.split(':')[0]}: ${def.name}`;
        colregsText.textContent = `${def.ruleText} Tàu mục tiêu hiện đang hiển thị dấu hiệu nhận diện: ${isDayMode ? def.dayTitle : def.nightTitle}.`;
        colregsAlert.textContent = def.ruleAlert;
      } else {
        // Standard power-driven vessel: follow scenario base rules
        colregsTitle.innerHTML = `<span>📖</span> ${s.rule}`;
        colregsText.textContent = s.text;
        colregsAlert.textContent = s.alert;
      }
    }

    function updateTargetVesselVisuals() {
      const def = TARGET_VESSEL_TYPES[targetVesselType] || TARGET_VESSEL_TYPES.power;

      // 1. Day Shapes on Target Ship 3D Mast
      if (targetShip.dayShapesGroup) {
        const top = targetShip.dayShapesGroup.getObjectByName('shapeTop');
        const mid = targetShip.dayShapesGroup.getObjectByName('shapeMid');
        const bot = targetShip.dayShapesGroup.getObjectByName('shapeBot');
        const bow = targetShip.dayShapesGroup.getObjectByName('shapeBow');
        const hg = targetShip.dayShapesGroup.getObjectByName('shapeHourglass');

        if (top) top.visible = false;
        if (mid) mid.visible = false;
        if (bot) bot.visible = false;
        if (bow) bow.visible = false;
        if (hg) hg.visible = false;

        if (isDayMode) {
          if (targetVesselType === 'nuc') {
            if (top) top.visible = true;
            if (bot) bot.visible = true;
          } else if (targetVesselType === 'ram') {
            if (top) top.visible = true;
            if (mid) mid.visible = true;
            if (bot) bot.visible = true;
          } else if (targetVesselType === 'fishing') {
            if (hg) hg.visible = true;
          } else if (targetVesselType === 'anchored') {
            if (bow) bow.visible = true;
          }
        }
      }

      // 2. Night Lights on Target Ship 3D Mast
      if (targetShip.specialLights && targetShip.specialLights.length >= 3) {
        targetShip.specialLights.forEach(l => {
          l.mesh.visible = false;
          l.point.visible = false;
        });

        if (!isDayMode) {
          if (targetVesselType === 'nuc') {
            setLightColor(targetShip.specialLights[0], 0xff1744);
            setLightColor(targetShip.specialLights[2], 0xff1744);
          } else if (targetVesselType === 'ram') {
            setLightColor(targetShip.specialLights[0], 0xff1744);
            setLightColor(targetShip.specialLights[1], 0xffffff);
            setLightColor(targetShip.specialLights[2], 0xff1744);
          } else if (targetVesselType === 'pilot') {
            setLightColor(targetShip.specialLights[0], 0xffffff);
            setLightColor(targetShip.specialLights[1], 0xff1744);
          } else if (targetVesselType === 'fishing') {
            setLightColor(targetShip.specialLights[0], 0x00e676);
            setLightColor(targetShip.specialLights[1], 0xffffff);
          } else if (targetVesselType === 'anchored') {
            setLightColor(targetShip.specialLights[0], 0xffffff);
          }
        }
      }
    }

    function setLightColor(lightObj, colorHex) {
      lightObj.mesh.material.color.setHex(colorHex);
      lightObj.mesh.visible = true;
      lightObj.point.color.setHex(colorHex);
      lightObj.point.visible = true;
    }

    // ========================================================
    // DRAW 2D VISUAL IDENTIFICATION DIAGRAM IN RIGHT PANEL
    // Illustrates Day Shapes on Mast or Glowing Night Lanterns!
    // ========================================================
    function drawVisualRecognitionDiagram() {
      const canvas = document.getElementById('recogCanvas');
      if (!canvas) return;
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;
      const def = TARGET_VESSEL_TYPES[targetVesselType] || TARGET_VESSEL_TYPES.power;

      ctx.clearRect(0, 0, w, h);

      // Update text in recognition card
      document.getElementById('recogModeTag').textContent = isDayMode ? '☀️ DẤU HIỆU NGÀY (DAY SHAPE)' : '🌙 ĐÈN HÀNH TRÌNH (NIGHT LIGHT)';
      document.getElementById('recogVesselTitle').textContent = def.name;
      document.getElementById('recogRhyme').textContent = def.rhyme;
      document.getElementById('recogDesc').textContent = isDayMode ? def.dayDesc : def.nightDesc;

      if (isDayMode) {
        // DAYTIME DIAGRAM: Sky background, Mast, and Black Shapes
        ctx.fillStyle = '#64b5f6';
        ctx.fillRect(0, 0, w, h);

        // Sea line at bottom
        ctx.fillStyle = '#0277bd';
        ctx.fillRect(0, h - 18, w, 18);

        // Ship hull profile silhouette
        ctx.fillStyle = '#263238';
        ctx.beginPath();
        ctx.moveTo(15, h - 18);
        ctx.lineTo(w - 15, h - 18);
        ctx.lineTo(w - 22, h - 6);
        ctx.lineTo(22, h - 6);
        ctx.closePath();
        ctx.fill();

        // Mast pole
        ctx.strokeStyle = '#37474f';
        ctx.lineWidth = 3;
        ctx.beginPath();
        ctx.moveTo(w / 2, h - 18);
        ctx.lineTo(w / 2, 12);
        ctx.stroke();

        // Draw Black Shapes
        ctx.fillStyle = '#111111';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 1;

        if (targetVesselType === 'nuc') {
          // 2 Black Balls
          drawCircle(ctx, w / 2, 26, 7);
          drawCircle(ctx, w / 2, 46, 7);
        } else if (targetVesselType === 'ram') {
          // Ball - Diamond - Ball
          drawCircle(ctx, w / 2, 22, 6);
          drawDiamond(ctx, w / 2, 38, 7);
          drawCircle(ctx, w / 2, 54, 6);
        } else if (targetVesselType === 'fishing') {
          // Hourglass
          drawHourglass(ctx, w / 2, 36, 8);
        } else if (targetVesselType === 'anchored') {
          // 1 Ball at bow
          drawCircle(ctx, 28, h - 28, 7);
        } else if (targetVesselType === 'pilot') {
          // Flag Hotel (White / Red)
          ctx.fillStyle = '#ffffff';
          ctx.fillRect(w / 2 + 2, 20, 10, 14);
          ctx.fillStyle = '#d32f2f';
          ctx.fillRect(w / 2 + 12, 20, 10, 14);
        } else {
          // Normal: Clean mast with small national flag
          ctx.fillStyle = '#e53935';
          ctx.fillRect(w / 2 + 2, 20, 14, 9);
        }
      } else {
        // NIGHTTIME DIAGRAM: Dark night sky and glowing navigation lanterns!
        ctx.fillStyle = '#020b14';
        ctx.fillRect(0, 0, w, h);

        // Waterline reflection
        ctx.fillStyle = '#011526';
        ctx.fillRect(0, h - 18, w, 18);

        // Ship silhouette
        ctx.fillStyle = '#0a1926';
        ctx.beginPath();
        ctx.moveTo(15, h - 18);
        ctx.lineTo(w - 15, h - 18);
        ctx.lineTo(w - 22, h - 6);
        ctx.lineTo(22, h - 6);
        ctx.closePath();
        ctx.fill();

        // Sidelights (Looking head-on: Port Red on left, Starboard Green on right)
        drawGlowLight(ctx, 24, h - 22, '#ff1744', 5); // Red (Port)
        drawGlowLight(ctx, w - 24, h - 22, '#00e676', 5); // Green (Starboard)

        // Foremast White light
        drawGlowLight(ctx, w / 2, 48, '#ffffff', 5);

        // Special Lights on mainmast
        if (targetVesselType === 'nuc') {
          // Red over Red
          drawGlowLight(ctx, w / 2, 18, '#ff1744', 6);
          drawGlowLight(ctx, w / 2, 32, '#ff1744', 6);
        } else if (targetVesselType === 'ram') {
          // Red - White - Red
          drawGlowLight(ctx, w / 2, 14, '#ff1744', 5);
          drawGlowLight(ctx, w / 2, 25, '#ffffff', 5);
          drawGlowLight(ctx, w / 2, 36, '#ff1744', 5);
        } else if (targetVesselType === 'fishing') {
          // Green over White
          drawGlowLight(ctx, w / 2, 18, '#00e676', 6);
          drawGlowLight(ctx, w / 2, 32, '#ffffff', 6);
        } else if (targetVesselType === 'pilot') {
          // White over Red
          drawGlowLight(ctx, w / 2, 18, '#ffffff', 6);
          drawGlowLight(ctx, w / 2, 32, '#ff1744', 6);
        } else if (targetVesselType === 'anchored') {
          // All-round White anchor light
          drawGlowLight(ctx, 26, h - 26, '#ffffff', 6);
        } else {
          // Normal Power-driven: Mainmast high white headlight
          drawGlowLight(ctx, w / 2, 22, '#ffffff', 6);
        }
      }
    }

    function drawCircle(ctx, x, y, r) {
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.stroke();
    }

    function drawDiamond(ctx, x, y, r) {
      ctx.beginPath();
      ctx.moveTo(x, y - r);
      ctx.lineTo(x + r, y);
      ctx.lineTo(x, y + r);
      ctx.lineTo(x - r, y);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }

    function drawHourglass(ctx, x, y, r) {
      ctx.beginPath();
      ctx.moveTo(x - r, y - r);
      ctx.lineTo(x + r, y - r);
      ctx.lineTo(x - r, y + r);
      ctx.lineTo(x + r, y + r);
      ctx.closePath();
      ctx.fill();
      ctx.stroke();
    }

    function drawGlowLight(ctx, x, y, color, r) {
      ctx.save();
      ctx.shadowColor = color;
      ctx.shadowBlur = 10;
      ctx.fillStyle = color;
      ctx.beginPath();
      ctx.arc(x, y, r, 0, Math.PI * 2);
      ctx.fill();
      ctx.restore();
    }

    // Wake Trail System
    function addWakePoint(ship, isOwn) {
      if (Math.random() > 0.4) return;
      const wakeGeo = new THREE.PlaneGeometry(1.4, 1.4);
      wakeGeo.rotateX(-Math.PI / 2);
      const wakeMat = new THREE.MeshBasicMaterial({
        color: isOwn ? 0xb3e5fc : 0xffcdd2,
        transparent: true,
        opacity: isDayMode ? 0.7 : 0.45,
        depthWrite: false
      });
      const wake = new THREE.Mesh(wakeGeo, wakeMat);

      const rad = THREE.MathUtils.degToRad(ship.course);
      wake.position.x = ship.x * NM_SCALE - Math.sin(rad) * 3.2;
      wake.position.z = ship.z * NM_SCALE - Math.cos(rad) * 3.2;
      wake.position.y = 0.02;
      wake.scale.set(1, 1, 1);
      scene.add(wake);

      wakeParticles.push({
        mesh: wake,
        life: 1.0,
        decay: 0.007 * simSpeed
      });
    }

    function updateWakes() {
      for (let i = wakeParticles.length - 1; i >= 0; i--) {
        const p = wakeParticles[i];
        p.life -= p.decay;
        p.mesh.scale.x += 0.02 * simSpeed;
        p.mesh.scale.z += 0.02 * simSpeed;
        p.mesh.material.opacity = p.life * (isDayMode ? 0.6 : 0.4);

        if (p.life <= 0) {
          scene.remove(p.mesh);
          p.mesh.geometry.dispose();
          p.mesh.material.dispose();
          wakeParticles.splice(i, 1);
        }
      }
    }

    // Collision Explosion Particles
    function triggerExplosion(x, z) {
      AudioEngine.playCrash();
      document.getElementById('collisionVignette').classList.add('active');
      screenShake = 1.3;

      for (let i = 0; i < 50; i++) {
        const pGeo = new THREE.DodecahedronGeometry(Math.random() * 0.4 + 0.15);
        const pMat = new THREE.MeshBasicMaterial({
          color: Math.random() > 0.4 ? 0xff5722 : (Math.random() > 0.5 ? 0xffeb3b : 0x424242),
          transparent: true,
          opacity: 0.95
        });
        const p = new THREE.Mesh(pGeo, pMat);
        p.position.set(x * NM_SCALE, 0.8, z * NM_SCALE);

        const angle = Math.random() * Math.PI * 2;
        const speed = Math.random() * 0.25 + 0.08;
        const vy = Math.random() * 0.25 + 0.1;

        scene.add(p);
        explosionParticles.push({
          mesh: p,
          vx: Math.cos(angle) * speed,
          vy: vy,
          vz: Math.sin(angle) * speed,
          life: 1.0
        });
      }
    }

    function updateExplosions() {
      for (let i = explosionParticles.length - 1; i >= 0; i--) {
        const p = explosionParticles[i];
        p.mesh.position.x += p.vx;
        p.mesh.position.y += p.vy;
        p.mesh.position.z += p.vz;
        p.vy -= 0.007;
        p.life -= 0.015;
        p.mesh.material.opacity = p.life;
        p.mesh.scale.multiplyScalar(0.97);

        if (p.life <= 0) {
          scene.remove(p.mesh);
          p.mesh.geometry.dispose();
          p.mesh.material.dispose();
          explosionParticles.splice(i, 1);
        }
      }
    }

    // Safe Passing Green Celebration Sparkles
    function triggerSafeSparkles(x, z) {
      for (let i = 0; i < 35; i++) {
        const sGeo = new THREE.SphereGeometry(0.18, 6, 6);
        const sMat = new THREE.MeshBasicMaterial({ color: 0x00e676, transparent: true, opacity: 0.9 });
        const s = new THREE.Mesh(sGeo, sMat);
        s.position.set(x * NM_SCALE + (Math.random() - 0.5) * 6, 1.2, z * NM_SCALE + (Math.random() - 0.5) * 6);
        scene.add(s);
        safeSparkles.push({
          mesh: s,
          vy: Math.random() * 0.12 + 0.05,
          life: 1.0
        });
      }
    }

    function updateSafeSparkles() {
      for (let i = safeSparkles.length - 1; i >= 0; i--) {
        const s = safeSparkles[i];
        s.mesh.position.y += s.vy;
        s.life -= 0.015;
        s.mesh.material.opacity = s.life;
        if (s.life <= 0) {
          scene.remove(s.mesh);
          s.mesh.geometry.dispose();
          s.mesh.material.dispose();
          safeSparkles.splice(i, 1);
        }
      }
    }

    // Load Scenario & Setup Distance
    function loadScenario(scenarioKey) {
      currentScenarioId = scenarioKey;
      const s = SCENARIOS[scenarioKey];
      if (!s) return;

      document.getElementById('scenarioSelect').value = scenarioKey;

      // Distance ratio
      const distRatio = initialDistSetting / 1.2;

      ownShip.x = s.own.x * distRatio;
      ownShip.z = s.own.z * distRatio;
      ownShip.course = s.own.course;
      ownShip.targetHeading = null;
      ownShip.speed = s.own.speed;
      ownShip.rudder = 0.0;
      ownShip.rot = 0.0;

      targetShip.x = s.target.x * distRatio;
      targetShip.z = s.target.z * distRatio;
      targetShip.course = s.target.course;
      targetShip.speed = s.target.speed;

      baseOwnCourse = s.own.course;
      baseOwnSpeed = s.own.speed;

      hasCollided = false;
      hasSafelyPassed = false;
      minDistanceRecorded = 999.0;
      score = 100;
      screenShake = 0;

      // Sync UI sliders
      document.getElementById('ownCourseSlider').value = Math.round(ownShip.course);
      document.getElementById('ownCourseVal').textContent = `${Math.round(ownShip.course).toString().padStart(3, '0')}°`;
      document.getElementById('ownSpeedSlider').value = ownShip.speed;
      document.getElementById('ownSpeedVal').textContent = `${ownShip.speed.toFixed(1)} kts`;

      document.getElementById('targetCourseSlider').value = Math.round(targetShip.course);
      document.getElementById('targetCourseVal').textContent = `${Math.round(targetShip.course).toString().padStart(3, '0')}°`;
      document.getElementById('targetSpeedSlider').value = targetShip.speed;
      document.getElementById('targetSpeedVal').textContent = `${targetShip.speed.toFixed(1)} kts`;

      updateRudderUI(0);
      updateStatusPill('safe', '● AN TOÀN (NO RISK DETECTED)');
      closeModals();

      // Clear particles
      wakeParticles.forEach(p => scene.remove(p.mesh));
      wakeParticles = [];
      explosionParticles.forEach(p => scene.remove(p.mesh));
      explosionParticles = [];
      safeSparkles.forEach(s => scene.remove(s.mesh));
      safeSparkles = [];

      document.getElementById('collisionVignette').classList.remove('active');
      document.getElementById('safeAura').classList.remove('active');

      adaptScenarioRules();
      updateTargetVesselVisuals();
      drawVisualRecognitionDiagram();
    }

    function setInitialDist(d) {
      initialDistSetting = d;
      const btns = document.querySelectorAll('.btn-dist');
      btns.forEach(b => {
        b.classList.toggle('active', parseFloat(b.textContent) === d);
      });
      loadScenario(currentScenarioId);
    }

    function resetExercise() {
      loadScenario(currentScenarioId);
    }

    function nextScenario() {
      const keys = Object.keys(SCENARIOS);
      const currIdx = keys.indexOf(currentScenarioId);
      const nextKey = keys[(currIdx + 1) % keys.length];
      loadScenario(nextKey);
    }

    // Kinematics and Physics Update Loop
    function updatePhysics(dt) {
      if (isPaused || hasCollided) return;

      const simDt = dt * simSpeed;

      // Autopilot: If a targetHeading is set
      if (ownShip.targetHeading !== null) {
        let diff = (ownShip.targetHeading - ownShip.course + 540) % 360 - 180;
        if (Math.abs(diff) < 1.0) {
          ownShip.targetHeading = null;
          ownShip.rudder = 0.0;
        } else {
          const desiredRudder = THREE.MathUtils.clamp(diff * 1.5, -25, 25);
          ownShip.rudder = THREE.MathUtils.lerp(ownShip.rudder, desiredRudder, 0.15);
        }
        updateRudderUI(ownShip.rudder);
      }

      // Realistic Rate of Turn (ROT)
      const rudderEffect = (ownShip.rudder / 35.0) * (ownShip.speed / 13.0) * 4.5;
      ownShip.rot = THREE.MathUtils.lerp(ownShip.rot, rudderEffect, 0.08);
      ownShip.course = (ownShip.course + ownShip.rot * simDt + 360) % 360;

      // Sync slider
      document.getElementById('ownCourseSlider').value = Math.round(ownShip.course);
      document.getElementById('ownCourseVal').textContent = `${Math.round(ownShip.course).toString().padStart(3, '0')}°`;

      // Movement in NM
      const ownSpeedNms = (ownShip.speed / 3600) * simDt;
      const ownRad = THREE.MathUtils.degToRad(ownShip.course);
      ownShip.x += ownSpeedNms * Math.sin(ownRad);
      ownShip.z += ownSpeedNms * Math.cos(ownRad);

      const targetSpeedNms = (targetShip.speed / 3600) * simDt;
      const targetRad = THREE.MathUtils.degToRad(targetShip.course);
      targetShip.x += targetSpeedNms * Math.sin(targetRad);
      targetShip.z += targetSpeedNms * Math.cos(targetRad);

      // Update 3D Meshes
      if (ownShip.mesh) {
        ownShip.mesh.position.set(ownShip.x * NM_SCALE, 0, ownShip.z * NM_SCALE);
        ownShip.mesh.rotation.y = ownRad;
        ownShip.mesh.rotation.z = -THREE.MathUtils.degToRad(ownShip.rot * 0.8);
      }

      if (targetShip.mesh) {
        targetShip.mesh.position.set(targetShip.x * NM_SCALE, 0, targetShip.z * NM_SCALE);
        targetShip.mesh.rotation.y = targetRad;
      }

      // Spin radar scanners
      radarSweepAngle += simDt * 3.5;
      const s1 = ownShip.mesh.getObjectByName('radarScanner');
      if (s1) s1.rotation.y = radarSweepAngle * 2;
      const s2 = targetShip.mesh.getObjectByName('radarScanner');
      if (s2) s2.rotation.y = radarSweepAngle * 2;

      // Particles
      addWakePoint(ownShip, true);
      addWakePoint(targetShip, false);
      updateWakes();
      updateExplosions();
      updateSafeSparkles();

      // Navigation Math
      const dx = targetShip.x - ownShip.x;
      const dz = targetShip.z - ownShip.z;
      const currentDist = Math.sqrt(dx * dx + dz * dz);

      if (currentDist < minDistanceRecorded) {
        minDistanceRecorded = currentDist;
      }

      const vx_own = ownShip.speed * Math.sin(ownRad);
      const vz_own = ownShip.speed * Math.cos(ownRad);

      const vx_target = targetShip.speed * Math.sin(targetRad);
      const vz_target = targetShip.speed * Math.cos(targetRad);

      const rel_vx = vx_target - vx_own;
      const rel_vz = vz_target - vz_own;
      const rel_speed = Math.sqrt(rel_vx * rel_vx + rel_vz * rel_vz);

      let cpa = currentDist;
      let tcpa = 0.0;
      const rel_v_sq = rel_vx * rel_vx + rel_vz * rel_vz;

      if (rel_v_sq > 1e-6) {
        const dot = dx * rel_vx + dz * rel_vz;
        tcpa = -dot / rel_v_sq;

        if (tcpa > 0) {
          const cpa_x = dx + rel_vx * tcpa;
          const cpa_z = dz + rel_vz * tcpa;
          cpa = Math.sqrt(cpa_x * cpa_x + cpa_z * cpa_z);
        } else {
          cpa = currentDist;
        }
      }

      let trueBearing = (THREE.MathUtils.radToDeg(Math.atan2(dx, dz)) + 360) % 360;
      let relBearing = (trueBearing - ownShip.course + 360) % 360;

      // Collision Detection (~0.07 NM / ~130 meters)
      if (currentDist < 0.07 && !hasCollided) {
        hasCollided = true;
        score = 0;
        triggerExplosion((ownShip.x + targetShip.x) / 2, (ownShip.z + targetShip.z) / 2);
        updateStatusPill('danger', '🚨 ĐÃ ĐÂM VA! (COLLISION DETECTED)');
        showCollisionModal();
      }

      // Safe Passing Detection
      if (!hasCollided && !hasSafelyPassed && tcpa <= 0.005 && minDistanceRecorded >= 0.35 && currentDist > minDistanceRecorded + 0.1) {
        hasSafelyPassed = true;
        AudioEngine.playChime();
        document.getElementById('safeAura').classList.add('active');
        triggerSafeSparkles((ownShip.x + targetShip.x) / 2, (ownShip.z + targetShip.z) / 2);
        updateStatusPill('success', '✅ ĐÃ VƯỢT QUA AN TOÀN (SAFE PASSING)');
        showSafePassModal(minDistanceRecorded);
      }

      // Scoring Evaluation
      evaluateScoring(cpa, tcpa, currentDist);

      // Update UI Telemetry
      updateTelemetryUI(currentDist, trueBearing, relBearing, cpa, tcpa, rel_speed);

      // Draw Radar (Own Ship at STRICT CENTER) & Compass
      drawRadar(dx, dz, rel_vx, rel_vz, cpa, tcpa);
      drawCompass(ownShip.course);
    }

    // Scoring System with Rule 18 Vessel Hierarchy
    function evaluateScoring(cpa, tcpa, currentDist) {
      if (hasCollided) {
        updateScoreUI(0, 'THẤT BẠI', 'Đâm va trực diện! 0/100 điểm. Vi phạm quy tắc tránh va trên biển.');
        return;
      }

      let currentScore = 100;
      let verdict = 'XUẤT SẮC';
      let reason = 'Đang điều động đúng chuẩn.';

      const courseChange = (ownShip.course - baseOwnCourse + 540) % 360 - 180;
      const s = SCENARIOS[currentScenarioId];
      const targetPriority = TARGET_VESSEL_TYPES[targetVesselType].priority;

      // Rule 18 Special Rule: If target is NUC, RAM, or Fishing, Own Ship MUST give way regardless of bearing!
      if (targetPriority >= 3) {
        // NUC, RAM, Fishing vessel: Own Ship MUST alter course to keep clear!
        if (Math.abs(courseChange) > 15) {
          verdict = 'XUẤT SẮC';
          reason = `Tuân thủ Quy tắc 18: Đã chủ động nhường đường cho tàu ${TARGET_VESSEL_TYPES[targetVesselType].name}.`;
        } else if (currentDist < 0.8) {
          currentScore -= 40;
          verdict = 'CẦN NHƯỜNG ĐƯỜNG';
          reason = `CẢNH BÁO RULE 18: Bắt buộc nhường đường cho tàu ${TARGET_VESSEL_TYPES[targetVesselType].name}!`;
          updateStatusPill('warning', '⚠ BẮT BUỘC NHƯỜNG ĐƯỜNG (RULE 18)');
        }
      } else if (s.type === 'head_on') {
        if (courseChange > 15) {
          verdict = 'XUẤT SẮC';
          reason = `Đã bẻ mạn phải +${Math.round(courseChange)}° đúng Rule 14.`;
        } else if (courseChange < -8) {
          currentScore -= 45;
          verdict = 'VI PHẠM';
          reason = 'CẢNH BÁO: Bẻ mạn trái cắt mũi tàu đối diện (-45đ)!';
          updateStatusPill('warning', '⚠ BẺ TRÁI NGUY HIỂM (RULE 14 VIOLATION)');
        } else if (currentDist < 1.0 && tcpa > 0) {
          currentScore -= 30;
          verdict = 'CẦN HÀNH ĐỘNG';
          reason = 'Hai tàu đang tiến gần, cần bẻ phải dứt khoát sớm (-30đ)!';
          updateStatusPill('warning', '⚠ NGUY CƠ ĐÂM VA (ACTION REQUIRED)');
        }
      } else if (s.type === 'crossing_give_way') {
        if (courseChange > 15) {
          verdict = 'XUẤT SẮC';
          reason = 'Đã nhường đường sang mạn phải an toàn.';
        } else if (courseChange < -8) {
          currentScore -= 50;
          verdict = 'VI PHẠM';
          reason = 'Cấm bẻ trái cắt trước mũi tàu được ưu tiên (-50đ)!';
          updateStatusPill('warning', '⚠ VI PHẠM QUY TẮC 15');
        } else if (currentDist < 1.0) {
          currentScore -= 35;
          verdict = 'CHƯA TRÁNH ĐƯỜNG';
          reason = 'Là tàu Give-way nhưng chưa đổi hướng rõ rệt (-35đ).';
        }
      } else if (s.type === 'crossing_stand_on') {
        if (Math.abs(courseChange) <= 10) {
          verdict = 'XUẤT SẮC';
          reason = 'Giữ nguyên hướng & tốc độ (Stand-on Vessel).';
        } else {
          currentScore -= 20;
          verdict = 'CHÚ Ý';
          reason = 'Tàu Stand-on nên duy trì hướng ổn định.';
        }
      }

      if (cpa < 0.25 && tcpa > 0) {
        currentScore -= 20;
      }

      score = Math.max(0, Math.min(100, currentScore));
      updateScoreUI(score, verdict, reason);
    }

    function updateScoreUI(sc, tag, desc) {
      document.getElementById('scoreBigVal').textContent = sc;
      const tagElem = document.getElementById('scoreVerdictTag');
      tagElem.textContent = tag;

      if (sc >= 80) {
        tagElem.style.color = 'var(--green-safe)';
        document.getElementById('scoreBigVal').style.color = 'var(--green-safe)';
      } else if (sc >= 50) {
        tagElem.style.color = 'var(--amber-warn)';
        document.getElementById('scoreBigVal').style.color = 'var(--amber-warn)';
      } else {
        tagElem.style.color = 'var(--red-danger)';
        document.getElementById('scoreBigVal').style.color = 'var(--red-danger)';
      }

      document.getElementById('scoreSubDesc').textContent = desc;
    }

    function updateStatusPill(type, text) {
      const pill = document.getElementById('navStatusPill');
      pill.className = 'nav-status-pill ' + (type === 'danger' ? 'danger' : type === 'warning' ? 'warning' : type === 'success' ? 'success' : '');
      pill.textContent = text;
    }

    // Telemetry UI
    function updateTelemetryUI(dist, trueBearing, relBearing, cpa, tcpa, relSpd) {
      document.getElementById('telemetryDist').textContent = `${dist.toFixed(2)} NM`;

      let relDesc = 'Chính Mũi';
      if (relBearing > 5 && relBearing < 175) relDesc = `Mạn Phải ${Math.round(relBearing)}°`;
      else if (relBearing > 185 && relBearing < 355) relDesc = `Mạn Trái ${Math.round(360 - relBearing)}°`;
      else if (relBearing >= 175 && relBearing <= 185) relDesc = 'Sau Lái';

      document.getElementById('telemetryBearing').textContent = `${Math.round(trueBearing).toString().padStart(3, '0')}° (${relDesc})`;

      const cpaElem = document.getElementById('telemetryCPA');
      cpaElem.textContent = `${cpa.toFixed(2)} NM`;
      if (cpa < 0.3) {
        cpaElem.className = 'telemetry-val cpa-danger';
      } else if (cpa < 0.6) {
        cpaElem.className = 'telemetry-val cpa-warn';
      } else {
        cpaElem.className = 'telemetry-val cpa-safe';
      }

      const tcpaElem = document.getElementById('telemetryTCPA');
      if (tcpa <= 0.005) {
        tcpaElem.textContent = 'ĐÃ VƯỢT QUA (PAST)';
        tcpaElem.style.color = 'var(--amber-warn)';
      } else {
        const mins = tcpa * 60;
        tcpaElem.textContent = `${mins.toFixed(1)} min`;
        tcpaElem.style.color = '#e3f5fd';
      }

      document.getElementById('telemetryRelSpeed').textContent = `${relSpd.toFixed(1)} kts`;
    }

    // Maneuver Handlers
    function maneuverQuick(dir) {
      if (dir === 'port') {
        ownShip.targetHeading = (ownShip.course - 30 + 360) % 360;
        applyManualRudder(-25);
        AudioEngine.playHorn(2);
      } else if (dir === 'stbd') {
        ownShip.targetHeading = (ownShip.course + 30) % 360;
        applyManualRudder(25);
        AudioEngine.playHorn(1);
      }
    }

    function applyManualRudder(angle) {
      ownShip.targetHeading = null;
      ownShip.rudder = THREE.MathUtils.clamp(angle, -35, 35);
      updateRudderUI(ownShip.rudder);
    }

    function updateRudderUI(angle) {
      const fill = document.getElementById('rudderFill');
      const text = document.getElementById('rudderReadout');

      if (angle > 0.5) {
        fill.style.left = '50%';
        fill.style.width = `${(angle / 35) * 50}%`;
        fill.style.background = 'var(--green-safe)';
        text.textContent = `BẺ PHẢI: ${Math.round(angle)}°`;
        text.style.color = 'var(--green-safe)';
      } else if (angle < -0.5) {
        const w = (Math.abs(angle) / 35) * 50;
        fill.style.left = `${50 - w}%`;
        fill.style.width = `${w}%`;
        fill.style.background = '#ff5252';
        text.textContent = `BẺ TRÁI: ${Math.abs(Math.round(angle))}°`;
        text.style.color = '#ff5252';
      } else {
        fill.style.width = '0%';
        text.textContent = 'LÁI GIỮA: 0°';
        text.style.color = 'var(--text-muted)';
      }
    }

    function slowDown50() {
      ownShip.speed = Math.max(1.0, ownShip.speed * 0.5);
      document.getElementById('ownSpeedSlider').value = ownShip.speed;
      document.getElementById('ownSpeedVal').textContent = `${ownShip.speed.toFixed(1)} kts`;
    }

    function onOwnCourseSliderInput(val) {
      ownShip.targetHeading = null;
      ownShip.course = parseFloat(val);
      document.getElementById('ownCourseVal').textContent = `${Math.round(ownShip.course).toString().padStart(3, '0')}°`;
    }

    function onOwnSpeedChange(val) {
      ownShip.speed = parseFloat(val);
      document.getElementById('ownSpeedVal').textContent = `${ownShip.speed.toFixed(1)} kts`;
    }

    function onTargetCourseChange(val) {
      targetShip.course = parseFloat(val);
      document.getElementById('targetCourseVal').textContent = `${Math.round(targetShip.course).toString().padStart(3, '0')}°`;
    }

    function onTargetSpeedChange(val) {
      targetShip.speed = parseFloat(val);
      document.getElementById('targetSpeedVal').textContent = `${targetShip.speed.toFixed(1)} kts`;
    }

    // Camera Modes
    function setCameraMode(mode) {
      cameraMode = mode;
      document.getElementById('btnViewOrbit').classList.toggle('active', mode === 'orbit');
      document.getElementById('btnViewBridge').classList.toggle('active', mode === 'bridge');
      document.getElementById('btnViewTop').classList.toggle('active', mode === 'top');

      if (mode === 'orbit') {
        controls.enabled = true;
        camera.position.set(ownShip.x * NM_SCALE, 14, ownShip.z * NM_SCALE - 22);
        controls.target.set(ownShip.x * NM_SCALE, 1, ownShip.z * NM_SCALE);
      } else if (mode === 'bridge') {
        controls.enabled = false;
      } else if (mode === 'top') {
        controls.enabled = false;
      }
    }

    function updateCameraView() {
      if (cameraMode === 'bridge') {
        // Eye position in the wheelhouse of Own Ship looking forward (+Z local)
        const rad = THREE.MathUtils.degToRad(ownShip.course);
        const camX = ownShip.x * NM_SCALE - Math.sin(rad) * 0.8;
        const camZ = ownShip.z * NM_SCALE - Math.cos(rad) * 0.8;
        const camY = 2.0; // Bridge window height

        camera.position.set(camX, camY, camZ);
        const lookX = camX + Math.sin(rad) * 50;
        const lookZ = camZ + Math.cos(rad) * 50;
        camera.lookAt(lookX, 1.7, lookZ);
      } else if (cameraMode === 'top') {
        const midX = (ownShip.x + targetShip.x) * (NM_SCALE / 2);
        const midZ = (ownShip.z + targetShip.z) * (NM_SCALE / 2);
        camera.position.set(midX, 70, midZ);
        camera.lookAt(midX, 0, midZ);
      }
    }

    // Simulation Speed Controls
    function setSimSpeed(spd) {
      simSpeed = spd;
      document.getElementById('simSpeedBadge').textContent = `SIM SPEED: ${spd.toFixed(1)}x`;
      ['btnSpd1', 'btnSpd2', 'btnSpd5', 'btnSpd10'].forEach(id => {
        const el = document.getElementById(id);
        if (el) el.classList.remove('active');
      });
      if (spd === 1.0) document.getElementById('btnSpd1').classList.add('active');
      if (spd === 2.0) document.getElementById('btnSpd2').classList.add('active');
      if (spd === 5.0) document.getElementById('btnSpd5').classList.add('active');
      if (spd === 10.0) document.getElementById('btnSpd10').classList.add('active');
    }

    function togglePause() {
      isPaused = !isPaused;
      const btn = document.getElementById('btnPause');
      btn.textContent = isPaused ? '▶ Tiếp tục' : '⏸ Tạm dừng';
      btn.classList.toggle('active', isPaused);
    }

    function setRadarRange(val) {
      radarRange = parseFloat(val);
    }

    function setRadarOrientation(mode) {
      radarMode = mode;
    }

    // ARPA Radar Scope Canvas Renderer: OWN SHIP IS ALWAYS AT EXACT CENTER!
    function drawRadar(dx, dz, rel_vx, rel_vz, cpa, tcpa) {
      const canvas = document.getElementById('radarCanvas');
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;
      const cx = w / 2;
      const cy = h / 2;
      const r = w / 2 - 4;

      ctx.clearRect(0, 0, w, h);

      // Dark PPI Scope Background
      ctx.fillStyle = '#01120a';
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.fill();

      // Range Rings (4 concentric rings)
      ctx.strokeStyle = '#0a3d24';
      ctx.lineWidth = 1;
      for (let i = 1; i <= 4; i++) {
        ctx.beginPath();
        ctx.arc(cx, cy, (r / 4) * i, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Azimuth radial lines (every 30°)
      ctx.strokeStyle = '#08331d';
      for (let a = 0; a < 360; a += 30) {
        const rad = THREE.MathUtils.degToRad(a);
        ctx.beginPath();
        ctx.moveTo(cx, cy);
        ctx.lineTo(cx + Math.sin(rad) * r, cy - Math.cos(rad) * r);
        ctx.stroke();
      }

      // Center Crosshair
      ctx.strokeStyle = '#105230';
      ctx.beginPath();
      ctx.moveTo(cx - r, cy); ctx.lineTo(cx + r, cy);
      ctx.moveTo(cx, cy - r); ctx.lineTo(cx, cy + r);
      ctx.stroke();

      // Rotating Radar Sweep Line with phosphor trail
      radarSweepAngle += 0.04 * simSpeed;
      const sweepRad = radarSweepAngle;
      ctx.strokeStyle = '#00e676';
      ctx.lineWidth = 1.8;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.sin(sweepRad) * r, cy - Math.cos(sweepRad) * r);
      ctx.stroke();

      // Scale: radarRange (NM) maps to radius r (px)
      const scale = r / radarRange;

      // Coordinate transformation based on Radar Orientation: North-Up vs Head-Up
      let rotOffset = 0;
      if (radarMode === 'head_up') {
        rotOffset = -THREE.MathUtils.degToRad(ownShip.course);
      }

      // 1. OWN SHIP IS PROMINENTLY AT EXACT CENTER (cx, cy)
      ctx.fillStyle = '#29b6f6';
      ctx.beginPath();
      ctx.arc(cx, cy, 4, 0, Math.PI * 2);
      ctx.fill();

      // Own Ship Heading Vector radiating from center
      const ownRad = THREE.MathUtils.degToRad(ownShip.course) + rotOffset;
      const ownVecLen = (ownShip.speed / 10) * 20;
      ctx.strokeStyle = '#29b6f6';
      ctx.lineWidth = 2.2;
      ctx.beginPath();
      ctx.moveTo(cx, cy);
      ctx.lineTo(cx + Math.sin(ownRad) * ownVecLen, cy - Math.cos(ownRad) * ownVecLen);
      ctx.stroke();

      // 2. TARGET SHIP ECHO POSITION RELATIVE TO CENTER
      let pX = dx;
      let pZ = dz;
      if (radarMode === 'head_up') {
        const cosR = Math.cos(rotOffset);
        const sinR = Math.sin(rotOffset);
        pX = dx * cosR - dz * sinR;
        pZ = dx * sinR + dz * cosR;
      }

      const tgtScreenX = cx + pX * scale;
      const tgtScreenY = cy - pZ * scale;

      const tgtDist = Math.sqrt(dx * dx + dz * dz);
      if (tgtDist <= radarRange) {
        // Target Echo Blip
        ctx.fillStyle = '#ff5252';
        ctx.shadowColor = '#ff5252';
        ctx.shadowBlur = 8;
        ctx.beginPath();
        ctx.arc(tgtScreenX, tgtScreenY, 5, 0, Math.PI * 2);
        ctx.fill();
        ctx.shadowBlur = 0;

        // Target Heading Vector
        const tgtRad = THREE.MathUtils.degToRad(targetShip.course) + rotOffset;
        const tgtVecLen = (targetShip.speed / 10) * 20;
        ctx.strokeStyle = '#ff6b81';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(tgtScreenX, tgtScreenY);
        ctx.lineTo(tgtScreenX + Math.sin(tgtRad) * tgtVecLen, tgtScreenY - Math.cos(tgtRad) * tgtVecLen);
        ctx.stroke();

        // Relative Vector Line (Cyan dashed)
        ctx.strokeStyle = '#00e5ff';
        ctx.lineWidth = 1.2;
        ctx.setLineDash([3, 3]);
        ctx.beginPath();
        ctx.moveTo(tgtScreenX, tgtScreenY);
        ctx.lineTo(tgtScreenX + rel_vx * 2.5, tgtScreenY - rel_vz * 2.5);
        ctx.stroke();
        ctx.setLineDash([]);

        // Target Label
        ctx.fillStyle = '#ffcdd2';
        ctx.font = 'bold 9px monospace';
        ctx.fillText('TGT-01', tgtScreenX + 7, tgtScreenY - 4);
      }

      // Outer Bezel Ring
      ctx.strokeStyle = '#00e676';
      ctx.lineWidth = 2;
      ctx.beginPath();
      ctx.arc(cx, cy, r, 0, Math.PI * 2);
      ctx.stroke();
    }

    // Compass Rose Canvas Renderer
    function drawCompass(hdg) {
      const canvas = document.getElementById('compassCanvas');
      const ctx = canvas.getContext('2d');
      const w = canvas.width;
      const h = canvas.height;
      const cx = w / 2;
      const cy = h / 2;
      const r = w / 2 - 3;

      ctx.clearRect(0, 0, w, h);

      ctx.save();
      ctx.translate(cx, cy);
      ctx.rotate(-THREE.MathUtils.degToRad(hdg));

      ctx.strokeStyle = '#1e485b';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.arc(0, 0, r, 0, Math.PI * 2);
      ctx.stroke();

      const cardinals = [
        { deg: 0, label: 'N', color: '#ff5252' },
        { deg: 90, label: 'E', color: '#8cd7f0' },
        { deg: 180, label: 'S', color: '#8cd7f0' },
        { deg: 270, label: 'W', color: '#8cd7f0' }
      ];

      for (let a = 0; a < 360; a += 10) {
        const rad = THREE.MathUtils.degToRad(a);
        const len = a % 90 === 0 ? 9 : (a % 30 === 0 ? 6 : 3);
        ctx.strokeStyle = a % 90 === 0 ? '#00e5ff' : '#28586c';
        ctx.lineWidth = a % 90 === 0 ? 2 : 1;
        ctx.beginPath();
        ctx.moveTo(Math.sin(rad) * (r - len), -Math.cos(rad) * (r - len));
        ctx.lineTo(Math.sin(rad) * r, -Math.cos(rad) * r);
        ctx.stroke();
      }

      ctx.font = 'bold 11px sans-serif';
      ctx.textAlign = 'center';
      ctx.textBaseline = 'middle';
      cardinals.forEach(c => {
        const rad = THREE.MathUtils.degToRad(c.deg);
        ctx.fillStyle = c.color;
        ctx.fillText(c.label, Math.sin(rad) * (r - 18), -Math.cos(rad) * (r - 18));
      });

      ctx.restore();

      // Lubber Line (Ship's Head Marker at top)
      ctx.strokeStyle = '#00e5ff';
      ctx.fillStyle = '#00e5ff';
      ctx.beginPath();
      ctx.moveTo(cx, cy - r);
      ctx.lineTo(cx - 5, cy - r + 10);
      ctx.lineTo(cx + 5, cy - r + 10);
      ctx.closePath();
      ctx.fill();

      document.getElementById('compassHdgReadout').textContent = `HDG: ${Math.round(hdg).toString().padStart(3, '0')}°`;
    }

    // Modal Handlers
    function showCollisionModal() {
      document.getElementById('collisionModal').style.display = 'flex';
    }

    function showSafePassModal(cpaAchieved) {
      document.getElementById('safePassScore').textContent = `${score} / 100`;
      document.getElementById('safePassModalDesc').innerHTML = `
        Hai tàu đã vượt qua nhau an toàn tuyệt đối với cự ly <b>CPA = ${cpaAchieved.toFixed(2)} NM</b>.<br/>
        Thao tác điều động chuẩn xác, tuân thủ xuất sắc các quy định tránh va hàng hải quốc tế!
      `;
      document.getElementById('safePassModal').style.display = 'flex';
    }

    function closeModals() {
      document.getElementById('collisionModal').style.display = 'none';
      document.getElementById('safePassModal').style.display = 'none';
    }

    // Animation Loop
    let lastTime = performance.now();
    function animate() {
      requestAnimationFrame(animate);

      const now = performance.now();
      const dt = Math.min((now - lastTime) / 1000, 0.1);
      lastTime = now;

      updatePhysics(dt);

      if (controls && controls.enabled) {
        if (ownShip.mesh) {
          controls.target.lerp(new THREE.Vector3(ownShip.x * NM_SCALE, 1.2, ownShip.z * NM_SCALE), 0.08);
        }
        controls.update();
      } else {
        updateCameraView();
      }

      // Handle screen shake on collision
      if (screenShake > 0) {
        camera.position.x += (Math.random() - 0.5) * screenShake * 0.4;
        camera.position.y += (Math.random() - 0.5) * screenShake * 0.4;
        camera.position.z += (Math.random() - 0.5) * screenShake * 0.4;
        screenShake = Math.max(0, screenShake - 0.02);
      }

      renderer.render(scene, camera);
    }

    function onWindowResize() {
      if (!camera || !renderer) return;
      camera.aspect = window.innerWidth / window.innerHeight;
      camera.updateProjectionMatrix();
      renderer.setSize(window.innerWidth, window.innerHeight);
    }

    // Initialize on page load
    window.addEventListener('DOMContentLoaded', () => {
      init3D();
      setTimeout(drawVisualRecognitionDiagram, 200);
    });
  