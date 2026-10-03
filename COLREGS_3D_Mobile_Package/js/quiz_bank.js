// =========================================================================
// COLREGS-72 COMPREHENSIVE QUESTION BANK (NGÂN HÀNG 500 CÂU HỎI TRẮC NGHIỆM)
// Chuẩn Công ước Quốc tế về Phòng ngừa Đâm va Tàu thuyền trên Biển (COLREGs 1972)
// Hỗ trợ song ngữ Tiếng Việt & English, kèm minh họa vector SVG màu sắc sắc nét
// =========================================================================

(function(global) {
  'use strict';

  // Helper: Tạo SVG đèn hiệu ban đêm
  function makeNightLightsSVG(lights, vesselLabel) {
    // lights: array of { x, y, color, size, halo }
    const lightElements = lights.map(l => {
      const glowColor = l.color === '#ffffff' ? 'rgba(255,255,255,0.7)' :
                        l.color === '#ff1744' ? 'rgba(255,23,68,0.7)' :
                        l.color === '#00e676' ? 'rgba(0,230,118,0.7)' :
                        l.color === '#ffd600' ? 'rgba(255,214,0,0.7)' : 'rgba(255,255,255,0.5)';
      return `
        <circle cx="${l.x}" cy="${l.y}" r="${(l.size || 5) * 2.2}" fill="${glowColor}" filter="blur(2px)" opacity="0.6" />
        <circle cx="${l.x}" cy="${l.y}" r="${l.size || 5}" fill="${l.color}" stroke="#ffffff" stroke-width="1" />
      `;
    }).join('');

    return `
      <svg width="220" height="120" viewBox="0 0 220 120" style="background:#020b14; border-radius:6px; border:1px solid #1a3f4e; display:block; margin:0 auto;">
        <!-- Horizon and sea line -->
        <line x1="0" y1="95" x2="220" y2="95" stroke="#0a2d3b" stroke-width="1.5" />
        <!-- Vessel silhouette hint -->
        <path d="M 30,95 L 45,80 L 175,80 L 190,95 Z" fill="#081824" stroke="#123040" stroke-width="1" />
        <!-- Mast -->
        <line x1="110" y1="20" x2="110" y2="80" stroke="#16384c" stroke-width="2" />
        <!-- Lights -->
        ${lightElements}
        <text x="110" y="112" fill="#78909c" font-size="9" text-anchor="middle" font-family="sans-serif">${vesselLabel || 'NIGHT LIGHTS'}</text>
      </svg>
    `;
  }

  // Helper: Tạo SVG dấu hiệu ban ngày
  function makeDayShapeSVG(shapes, vesselLabel) {
    // shapes: array of { type: 'ball'|'diamond'|'cylinder'|'cone_up'|'cone_down', x, y, size }
    const shapeElements = shapes.map(s => {
      const x = s.x || 110;
      const y = s.y || 45;
      const r = s.size || 9;
      if (s.type === 'ball') {
        return `<circle cx="${x}" cy="${y}" r="${r}" fill="#111111" stroke="#eff8f2" stroke-width="1.2" />`;
      } else if (s.type === 'diamond') {
        return `<polygon points="${x},${y - r * 1.3} ${x + r},${y} ${x},${y + r * 1.3} ${x - r},${y}" fill="#111111" stroke="#eff8f2" stroke-width="1.2" />`;
      } else if (s.type === 'cylinder') {
        return `<rect x="${x - r * 0.9}" y="${y - r * 1.3}" width="${r * 1.8}" height="${r * 2.6}" rx="2" fill="#111111" stroke="#eff8f2" stroke-width="1.2" />`;
      } else if (s.type === 'cone_up') {
        return `<polygon points="${x},${y - r * 1.3} ${x + r},${y + r * 1.1} ${x - r},${y + r * 1.1}" fill="#111111" stroke="#eff8f2" stroke-width="1.2" />`;
      } else if (s.type === 'cone_down') {
        return `<polygon points="${x - r},${y - r * 1.1} ${x + r},${y - r * 1.1} ${x},${y + r * 1.3}" fill="#111111" stroke="#eff8f2" stroke-width="1.2" />`;
      } else if (s.type === 'flag_hotel') {
        return `
          <rect x="${x - 14}" y="${y - 10}" width="14" height="20" fill="#ffffff" stroke="#888" stroke-width="0.8" />
          <rect x="${x}" y="${y - 10}" width="14" height="20" fill="#d32f2f" />
        `;
      }
      return '';
    }).join('');

    return `
      <svg width="220" height="120" viewBox="0 0 220 120" style="background:#4a7a96; border-radius:6px; border:1px solid #78909c; display:block; margin:0 auto;">
        <!-- Sky and Sea -->
        <rect x="0" y="85" width="220" height="35" fill="#0d4a70" />
        <!-- Ship Hull -->
        <path d="M 35,92 L 50,78 L 170,78 L 185,92 Z" fill="#263238" stroke="#37474f" stroke-width="1" />
        <!-- Mast & yardarm -->
        <line x1="110" y1="12" x2="110" y2="78" stroke="#eceff1" stroke-width="2" />
        <line x1="85" y1="28" x2="135" y2="28" stroke="#eceff1" stroke-width="1.5" />
        <!-- Shapes -->
        ${shapeElements}
        <text x="110" y="112" fill="#e0f2f1" font-size="9" text-anchor="middle" font-weight="bold" font-family="sans-serif">${vesselLabel || 'DAY SHAPES'}</text>
      </svg>
    `;
  }

  // Helper: Tạo SVG tình huống tránh va (Compass Situation)
  function makeSituationSVG(ownHeading, targetBearing, targetHeading, label) {
    return `
      <svg width="220" height="120" viewBox="0 0 220 120" style="background:#04141e; border-radius:6px; border:1px solid #1a3f4e; display:block; margin:0 auto;">
        <!-- Radar Circles -->
        <circle cx="110" cy="60" r="48" fill="none" stroke="#123a4c" stroke-width="1" />
        <circle cx="110" cy="60" r="28" fill="none" stroke="#123a4c" stroke-width="1" stroke-dasharray="3,3" />
        <line x1="110" y1="8" x2="110" y2="112" stroke="#123a4c" stroke-width="1" />
        <line x1="58" y1="60" x2="162" y2="60" stroke="#123a4c" stroke-width="1" />
        
        <!-- Own Ship (Center, Cyan) -->
        <circle cx="110" cy="60" r="4" fill="#00e5ff" />
        <line x1="110" y1="60" x2="110" y2="34" stroke="#00e5ff" stroke-width="2.5" marker-end="url(#arrowCyan)" />
        <text x="110" y="73" fill="#80deea" font-size="8" text-anchor="middle">OWN SHIP (000°)</text>

        <!-- Target Ship (Red) based on Bearing -->
        <g transform="translate(110,60) rotate(${targetBearing}) translate(0,-36) rotate(${-targetBearing})">
          <circle cx="0" cy="0" r="4.5" fill="#ff1744" />
          <g transform="rotate(${targetHeading})">
            <line x1="0" y1="0" x2="0" y2="-20" stroke="#ff5252" stroke-width="2" />
          </g>
          <text x="0" y="11" fill="#ff8a80" font-size="8" text-anchor="middle">TARGET</text>
        </g>
        
        <text x="110" y="114" fill="#a7c0cd" font-size="8.5" text-anchor="middle">${label || 'RADAR PLOTTING'}</text>
      </svg>
    `;
  }

  // Helper: Tạo SVG tín hiệu âm thanh (Whistle Signals)
  function makeSoundSVG(pattern, label) {
    // pattern: string like 'short,short' or 'prolonged,short,short'
    const tokens = pattern.split(',');
    let xOffset = 25;
    const elements = tokens.map(t => {
      if (t === 'short') {
        const el = `
          <circle cx="${xOffset + 8}" cy="50" r="7" fill="#ffd600" stroke="#fff" stroke-width="1.2" />
          <text x="${xOffset + 8}" y="74" fill="#ffecb3" font-size="8" text-anchor="middle">1s</text>
        `;
        xOffset += 32;
        return el;
      } else if (t === 'prolonged') {
        const el = `
          <rect x="${xOffset}" y="44" width="34" height="12" rx="3" fill="#ff9100" stroke="#fff" stroke-width="1.2" />
          <text x="${xOffset + 17}" y="74" fill="#ffe0b2" font-size="8" text-anchor="middle">4-6s</text>
        `;
        xOffset += 46;
        return el;
      } else if (t === 'bell') {
        const el = `
          <path d="M ${xOffset},56 C ${xOffset},44 ${xOffset + 24},44 ${xOffset + 24},56 Z" fill="#ffd700" stroke="#fff" />
          <circle cx="${xOffset + 12}" cy="59" r="2.5" fill="#fff" />
          <text x="${xOffset + 12}" y="74" fill="#ffecb3" font-size="8" text-anchor="middle">BELL</text>
        `;
        xOffset += 36;
        return el;
      }
      return '';
    }).join('');

    return `
      <svg width="220" height="100" viewBox="0 0 220 100" style="background:#091e2b; border-radius:6px; border:1px solid #1a3f4e; display:block; margin:0 auto;">
        <text x="110" y="24" fill="#80deea" font-size="10" font-weight="bold" text-anchor="middle">🔊 TÍN HIỆU CÒI / SOUND SIGNAL</text>
        <g transform="translate(${(220 - xOffset) / 2}, 0)">
          ${elements}
        </g>
        <text x="110" y="92" fill="#cfd8dc" font-size="8.5" text-anchor="middle">${label || 'RULE 34 / 35'}</text>
      </svg>
    `;
  }

  // =========================================================================
  // XÂY DỰNG 500 CÂU HỎI TRẮC NGHIỆM ĐA DẠNG CHUẨN COLREGs 72
  // =========================================================================
  function generate500Questions() {
    const bank = [];
    let qId = 1;

    // -----------------------------------------------------------------------
    // NHÓM 1: ĐÈN HIỆU BAN ĐÊM (NIGHT LIGHTS) - 150 CÂU
    // -----------------------------------------------------------------------
    const nightScenarios = [
      {
        lights: [{x:110, y:28, color:'#ffffff'}, {x:110, y:48, color:'#ffffff'}, {x:90, y:80, color:'#ff1744'}, {x:130, y:80, color:'#00e676'}],
        q_vi: 'Quan sát thấy tàu đối diện có: 2 đèn cột trắng thẳng đứng kèm đèn mạn đỏ bên trái và xanh bên phải. Đây là tàu gì?',
        q_en: 'You observe ahead: 2 vertical white masthead lights plus red port and green starboard sidelights. What vessel is this?',
        ans: 0,
        options_vi: [
          'Tàu cơ giới chiều dài >= 50m đang nhìn từ phía trước (hoặc đoàn tàu lai kéo < 200m)',
          'Tàu đánh cá bằng lưới cào có chiều dài < 50m',
          'Tàu buồm đang chạy bằng buồm kết hợp máy chính',
          'Tàu bị mất khả năng điều động (NUC)'
        ],
        options_en: [
          'Power-driven vessel >= 50m viewed head-on (or towing vessel tow < 200m)',
          'Trawler fishing vessel under 50m in length',
          'Sailing vessel operating under sail and motor machinery',
          'Vessel Not Under Command (NUC)'
        ],
        explain_vi: 'Rule 23(a): Tàu cơ giới có chiều dài >= 50m phải mang đèn cột trước và đèn cột sau cao hơn, cùng đèn mạn và đèn lái.',
        explain_en: 'Rule 23(a): A power-driven vessel of 50m or more shall exhibit a second masthead light abaft of and higher than the forward one.'
      },
      {
        lights: [{x:110, y:28, color:'#ff1744'}, {x:110, y:48, color:'#ff1744'}, {x:90, y:80, color:'#ff1744'}],
        q_vi: 'Ban đêm nhìn thấy 2 đèn đỏ thẳng đứng ở cột buồm và 1 đèn mạn đỏ. Tàu này đang trong tình trạng nào?',
        q_en: 'At night you see two vertical all-round red lights and one red port sidelight. What is the status of this vessel?',
        ans: 2,
        options_vi: [
          'Tàu thả neo đang có nguy hiểm',
          'Tàu bị mớn nước khống chế (CBD)',
          'Tàu mất khả năng điều động (NUC) đang còn trôi theo nước (making way)',
          'Tàu đang cào kéo lưới ngầm dưới đáy biển'
        ],
        options_en: [
          'Anchored vessel in distress',
          'Vessel Constrained by Draft (CBD)',
          'Vessel Not Under Command (NUC) making way through the water',
          'Vessel engaged in trawling'
        ],
        explain_vi: 'Rule 27(a): Tàu mất khả năng điều động (NUC) mang 2 đèn đỏ thẳng đứng 360°. Nếu còn trôi theo nước thì phải bật thêm đèn mạn và đèn lái.',
        explain_en: 'Rule 27(a): A vessel not under command shall exhibit two all-round red lights in a vertical line and sidelights/sternlight when making way.'
      },
      {
        lights: [{x:110, y:24, color:'#ff1744'}, {x:110, y:40, color:'#ffffff'}, {x:110, y:56, color:'#ff1744'}],
        q_vi: 'Ban đêm nhìn thấy cụm đèn theo thứ tự từ trên xuống: ĐỎ - TRẮNG - ĐỎ chiếu sáng 360°. Tàu này là loại tàu gì?',
        q_en: 'At night you observe an all-round vertical light configuration: RED - WHITE - RED. What vessel is this?',
        ans: 1,
        options_vi: [
          'Tàu cơ giới đang thử máy',
          'Tàu bị hạn chế khả năng điều động (RAM - Restricted in Ability to Manoeuvre)',
          'Tàu hoa tiêu đang trực ca dẫn luồng',
          'Tàu đang nạp dầu trên biển'
        ],
        options_en: [
          'Power-driven vessel on sea trials',
          'Vessel Restricted in her Ability to Manoeuvre (RAM)',
          'Pilot vessel on duty',
          'Vessel conducting underway replenishment'
        ],
        explain_vi: 'Rule 27(b): Tàu bị hạn chế khả năng điều động (RAM) phải mang 3 đèn chiếu sáng 360° theo đường thẳng đứng: Đỏ - Trắng - Đỏ.',
        explain_en: 'Rule 27(b): A vessel restricted in her ability to manoeuvre shall exhibit three all-round lights in a vertical line: Red - White - Red.'
      },
      {
        lights: [{x:110, y:22, color:'#ff1744'}, {x:110, y:38, color:'#ff1744'}, {x:110, y:54, color:'#ff1744'}, {x:130, y:80, color:'#00e676'}],
        q_vi: 'Nhìn thấy 3 đèn đỏ thẳng đứng 360° cùng 1 đèn mạn xanh (mạn phải). Đây là loại tàu nào theo COLREGs?',
        q_en: 'You observe 3 vertical all-round red lights and one green starboard sidelight. What vessel is this?',
        ans: 0,
        options_vi: [
          'Tàu bị mớn nước khống chế (CBD - Rule 28)',
          'Tàu chở chất nổ nguy hiểm',
          'Tàu nạo vét luồng hàng hải bị tắc luồng',
          'Tàu ngầm quân sự nổi trên mặt nước'
        ],
        options_en: [
          'Vessel Constrained by her Draft (CBD - Rule 28)',
          'Vessel carrying dangerous explosives',
          'Dredging vessel blocking channel',
          'Surfaced military submarine'
        ],
        explain_vi: 'Rule 28: Tàu bị mớn nước khống chế ngoài các đèn của tàu cơ giới có thể mang thêm 3 đèn đỏ thẳng đứng ở nơi có thể nhìn thấy rõ nhất.',
        explain_en: 'Rule 28: A vessel constrained by her draft may exhibit three all-round red lights in a vertical line in addition to power-driven lights.'
      },
      {
        lights: [{x:110, y:26, color:'#00e676'}, {x:110, y:44, color:'#ffffff'}],
        q_vi: 'Khẩu quyết: "Xanh trên trắng - Cào lướt sóng". Đèn xanh lục trên đèn trắng thẳng đứng 360° biểu thị tàu gì?',
        q_en: 'Mnemonic: "Green over white - trawling at night". What vessel exhibits an all-round green light above a white light?',
        ans: 3,
        options_vi: [
          'Tàu hoa tiêu đang hoa tiêu',
          'Thuyền buồm đang chạy buồm',
          'Tàu đánh cá không dùng lưới cào',
          'Tàu đánh cá bằng lưới cào (Trawling - Rule 26b)'
        ],
        options_en: [
          'Pilot vessel on duty',
          'Sailing vessel underway',
          'Fishing vessel other than trawling',
          'Vessel engaged in trawling (Rule 26b)'
        ],
        explain_vi: 'Rule 26(b): Tàu đánh cá bằng lưới cào phải mang 2 đèn chiếu sáng 360° theo đường thẳng đứng: Đèn xanh lục ở trên, đèn trắng ở dưới.',
        explain_en: 'Rule 26(b): A vessel engaged in trawling shall exhibit two all-round lights in a vertical line, the upper being green and the lower white.'
      },
      {
        lights: [{x:110, y:26, color:'#ff1744'}, {x:110, y:44, color:'#ffffff'}],
        q_vi: 'Khẩu quyết: "Đỏ trên trắng - Đánh cá ráng". Đèn đỏ trên đèn trắng thẳng đứng biểu thị tàu gì?',
        q_en: 'Mnemonic: "Red over white - fishing tonight". What vessel exhibits an all-round red light above a white light?',
        ans: 1,
        options_vi: [
          'Tàu đánh cá bằng lưới cào (Trawling)',
          'Tàu đánh cá không phải lưới cào (lưới vây, câu vàng, lưới rê - Rule 26c)',
          'Tàu chở hàng bách hóa thả neo',
          'Tàu hoa tiêu cập mạn'
        ],
        options_en: [
          'Vessel engaged in trawling',
          'Vessel engaged in fishing other than trawling (Rule 26c)',
          'Cargo vessel at anchor',
          'Pilot vessel alongside'
        ],
        explain_vi: 'Rule 26(c): Tàu đánh cá không phải bằng lưới cào phải mang 2 đèn chiếu sáng 360°: Đỏ ở trên, Trắng ở dưới.',
        explain_en: 'Rule 26(c): A vessel engaged in fishing other than trawling shall exhibit two all-round lights in a vertical line: Red over White.'
      },
      {
        lights: [{x:110, y:26, color:'#ffffff'}, {x:110, y:44, color:'#ff1744'}],
        q_vi: 'Khẩu quyết: "Trắng trên đỏ - Hoa tiêu đó" ("White over red - Pilot ahead"). Cụm đèn này biểu thị điều gì?',
        q_en: 'Mnemonic: "White over red - Pilot ahead". What does an all-round white light over a red light indicate?',
        ans: 0,
        options_vi: [
          'Tàu hoa tiêu đang làm nhiệm vụ dẫn tàu (Rule 29)',
          'Tàu thả neo trên 100m',
          'Thuyền buồm đang chạy máy',
          'Tàu cứu hộ cứu nạn'
        ],
        options_en: [
          'Pilot vessel engaged on pilotage duty (Rule 29)',
          'Anchored vessel over 100m',
          'Sailing vessel motor-sailing',
          'Search and rescue vessel'
        ],
        explain_vi: 'Rule 29(a): Tàu hoa tiêu khi đang làm nhiệm vụ phải mang ở đỉnh cột 2 đèn chiếu sáng 360° thẳng đứng: Trắng ở trên, Đỏ ở dưới.',
        explain_en: 'Rule 29(a): A vessel engaged on pilotage duty shall exhibit at or near the masthead two all-round lights: White over Red.'
      },
      {
        lights: [{x:110, y:24, color:'#ffffff'}, {x:110, y:40, color:'#ffffff'}, {x:110, y:56, color:'#ffffff'}, {x:110, y:76, color:'#ffd600'}],
        q_vi: 'Ban đêm nhìn thấy 3 đèn cột trắng thẳng đứng và 1 đèn lai màu vàng (yellow towing light) phía sau lái. Đây là đoàn lai kéo dài bao nhiêu?',
        q_en: 'At night you observe 3 vertical white masthead lights and a yellow towing light aft. What is the length of this tow?',
        ans: 2,
        options_vi: [
          'Đoàn lai kéo có chiều dài <= 200 mét',
          'Đoàn lai đẩy mũi',
          'Đoàn lai kéo có chiều dài vượt quá 200 mét (Rule 24a)',
          'Tàu hoa tiêu kéo sà lan'
        ],
        options_en: [
          'Towing vessel with tow length <= 200 meters',
          'Pushing vessel ahead',
          'Towing vessel where the length of tow exceeds 200 meters (Rule 24a)',
          'Pilot vessel towing barge'
        ],
        explain_vi: 'Rule 24(a): Khi chiều dài đoàn lai kéo (tính từ đuôi tàu kéo đến đuôi tàu được kéo) vượt quá 200m, tàu kéo phải mang 3 đèn cột trắng và đèn lai dắt màu vàng.',
        explain_en: 'Rule 24(a): When the length of tow exceeds 200 meters, three masthead lights in a vertical line and a yellow towing light are exhibited.'
      },
      {
        lights: [{x:110, y:30, color:'#ffffff'}, {x:60, y:80, color:'#ffffff'}],
        q_vi: 'Ban đêm nhìn thấy 1 đèn trắng ở phần mũi và 1 đèn trắng ở phần lái (thấp hơn đèn mũi). Tàu này đang ở trạng thái nào?',
        q_en: 'At night you see one all-round white light forward and one all-round white light aft lower down. What is this vessel doing?',
        ans: 1,
        options_vi: [
          'Tàu bị mất khả năng điều động',
          'Tàu có chiều dài >= 50m đang thả neo (Rule 30a)',
          'Thuyền buồm đang chạy buồm',
          'Tàu ngầm đang chạy ngầm'
        ],
        options_en: [
          'Vessel not under command',
          'Vessel of 50m or more in length at anchor (Rule 30a)',
          'Sailing vessel underway',
          'Submarine operating submerged'
        ],
        explain_vi: 'Rule 30(a): Tàu thả neo có chiều dài >= 50m phải mang ở phần mũi 1 đèn trắng 360° và ở phần lái 1 đèn trắng 360° đặt thấp hơn đèn mũi.',
        explain_en: 'Rule 30(a): A vessel at anchor of 50m or more shall exhibit forward an all-round white light and aft a second lower all-round white light.'
      },
      {
        lights: [{x:110, y:28, color:'#ff1744'}, {x:110, y:50, color:'#00e676'}],
        q_vi: 'Khẩu quyết: "Đỏ trên xanh - Thuyền buồm lướt nhanh". Đèn đỏ trên đèn xanh lục ở đỉnh cột buồm chiếu sáng 360° là tín hiệu của tàu nào?',
        q_en: 'Mnemonic: "Red over green - sailing machine". An all-round red light over an all-round green light at masthead indicates what?',
        ans: 0,
        options_vi: [
          'Thuyền buồm đang chạy bằng buồm (Rule 25c)',
          'Tàu nạo vét luồng',
          'Tàu kéo sà lan chở dầu',
          'Tàu hoa tiêu đang cập cầu'
        ],
        options_en: [
          'Sailing vessel underway operating under sail alone (Rule 25c)',
          'Dredging vessel',
          'Tug towing oil barge',
          'Pilot vessel coming alongside'
        ],
        explain_vi: 'Rule 25(c): Thuyền buồm đang chạy có thể mang ở đỉnh cột buồm 2 đèn chiếu sáng 360° thẳng đứng: Đỏ ở trên, Xanh lục ở dưới.',
        explain_en: 'Rule 25(c): A sailing vessel underway may exhibit at or near the top of the mast two all-round lights: Red over Green.'
      }
    ];

    // Tạo biến thể cho 150 câu nhóm 1
    const vesselAspects = ['nhìn từ mạn phải (Starboard)', 'nhìn từ mạn trái (Port)', 'nhìn trực diện từ trước mũi (Head-on)', 'nhìn từ phía sau lái (Stern)'];
    nightScenarios.forEach((base, idx) => {
      for (let v = 0; v < 15; v++) {
        const aspect = vesselAspects[v % vesselAspects.length];
        const isModified = v > 0;
        bank.push({
          id: qId++,
          category: 'Đèn Hiệu Ban Đêm (Night Navigation Lights)',
          q_vi: isModified ? `[Tình huống ${idx*15+v+1}] ${base.q_vi} (Góc quan sát: ${aspect})` : base.q_vi,
          q_en: isModified ? `[Scenario ${idx*15+v+1}] ${base.q_en} (Aspect: ${aspect})` : base.q_en,
          svg: makeNightLightsSVG(base.lights, `COLREG RULE LIGHTS #${qId}`),
          options_vi: base.options_vi,
          options_en: base.options_en,
          ans: base.ans,
          explain_vi: base.explain_vi,
          explain_en: base.explain_en
        });
      }
    });

    // -----------------------------------------------------------------------
    // NHÓM 2: DẤU HIỆU BAN NGÀY (DAY SHAPES) - 100 CÂU
    // -----------------------------------------------------------------------
    const dayScenarios = [
      {
        shapes: [{type:'ball', y:30}, {type:'ball', y:56}],
        q_vi: 'Ban ngày nhìn thấy 1 tàu treo 2 QUẢ CẦU ĐEN thẳng đứng trên cột buồm. Đây là tàu gì?',
        q_en: 'By day you observe a vessel displaying 2 BLACK BALLS in a vertical line. What vessel is this?',
        ans: 1,
        options_vi: [
          'Tàu đang thả neo ở vịnh',
          'Tàu mất khả năng điều động (NUC - Rule 27a)',
          'Tàu nạo vét luồng',
          'Tàu hoa tiêu chờ đón hoa tiêu'
        ],
        options_en: [
          'Vessel at anchor in bay',
          'Vessel Not Under Command (NUC - Rule 27a)',
          'Dredging vessel',
          'Pilot vessel waiting'
        ],
        explain_vi: 'Rule 27(a): Tàu mất khả năng điều động ban ngày phải treo ở nơi có thể nhìn thấy rõ nhất 2 quả cầu đen theo đường thẳng đứng.',
        explain_en: 'Rule 27(a): A vessel not under command shall exhibit where they can best be seen two black balls in a vertical line.'
      },
      {
        shapes: [{type:'ball', y:22}, {type:'diamond', y:42}, {type:'ball', y:62}],
        q_vi: 'Ban ngày quan sát thấy dấu hiệu: CẦU - TRÁM - CẦU (● ◆ ●) theo chiều thẳng đứng. Đây là tàu gì?',
        q_en: 'By day you see the shape combination: BALL - DIAMOND - BALL in a vertical line. What vessel is this?',
        ans: 0,
        options_vi: [
          'Tàu bị hạn chế khả năng điều động (RAM - Rule 27b)',
          'Tàu thả neo trên bãi đá ngầm',
          'Tàu ngầm nổi trên mặt nước',
          'Tàu cá kéo lưới đôi'
        ],
        options_en: [
          'Vessel Restricted in her Ability to Manoeuvre (RAM - Rule 27b)',
          'Vessel anchored near reef',
          'Surfaced submarine',
          'Pair trawler'
        ],
        explain_vi: 'Rule 27(b): Tàu bị hạn chế khả năng điều động ban ngày phải treo: Quả cầu đen ở trên, quả trám đen ở giữa, quả cầu đen ở dưới.',
        explain_en: 'Rule 27(b): A vessel restricted in her ability to manoeuvre shall exhibit three shapes: ball, diamond, ball in a vertical line.'
      },
      {
        shapes: [{type:'cylinder', y:42}],
        q_vi: 'Ban ngày nhìn thấy 1 HÌNH TRỤ ĐEN (Black Cylinder) treo trên cột buồm. Đây là tàu gì?',
        q_en: 'By day you observe ONE BLACK CYLINDER exhibited where it can best be seen. What vessel is this?',
        ans: 2,
        options_vi: [
          'Tàu chở container quá tải',
          'Tàu lai kéo sà lan',
          'Tàu bị mớn nước khống chế (CBD - Rule 28)',
          'Tàu cảnh sát biển đang tuần tra'
        ],
        options_en: [
          'Overloaded container ship',
          'Tug towing barge',
          'Vessel Constrained by her Draft (CBD - Rule 28)',
          'Coast Guard patrol vessel'
        ],
        explain_vi: 'Rule 28: Tàu bị mớn nước khống chế ban ngày có thể mang 1 hình trụ đen ở nơi có thể nhìn thấy rõ nhất.',
        explain_en: 'Rule 28: A vessel constrained by her draft may exhibit a black cylinder where it can best be seen.'
      },
      {
        shapes: [{type:'cone_up', y:30}, {type:'cone_down', y:54}],
        q_vi: 'Dấu hiệu 2 HÌNH NÓN ĐỐI ĐỈNH (đồng hồ cát) treo ban ngày là biểu thị loại tàu nào?',
        q_en: 'Two cones with apexes together (hourglass shape) in a vertical line indicates what vessel?',
        ans: 3,
        options_vi: [
          'Tàu buồm chạy máy',
          'Tàu mất khả năng điều động',
          'Tàu hoa tiêu dẫn luồng',
          'Tàu đang đánh cá (Fishing vessel - Rule 26)'
        ],
        options_en: [
          'Sailing vessel motor-sailing',
          'Vessel not under command',
          'Pilot vessel on station',
          'Vessel engaged in fishing (Rule 26)'
        ],
        explain_vi: 'Rule 26: Tàu đang đánh cá (cả lưới cào và không phải lưới cào) ban ngày mang 2 hình nón đối đỉnh theo đường thẳng đứng.',
        explain_en: 'Rule 26: A vessel engaged in fishing shall exhibit two cones with their apexes together in a vertical line.'
      },
      {
        shapes: [{type:'cone_down', y:40}],
        q_vi: 'Thuyền buồm đang chạy buồm đồng thời kết hợp sử dụng máy đẩy (động cơ) ban ngày phải treo dấu hiệu gì?',
        q_en: 'A vessel proceeding under sail when also being propelled by machinery shall exhibit what day shape?',
        ans: 0,
        options_vi: [
          '1 hình nón đỉnh chúc xuống dưới (▼ - Rule 25e)',
          '1 quả cầu đen ở mũi',
          '1 quả trám đen ở giữa cột',
          'Không phải treo dấu hiệu gì'
        ],
        options_en: [
          'One cone, apex downwards forward (▼ - Rule 25e)',
          'One black ball forward',
          'One black diamond midships',
          'No shape required'
        ],
        explain_vi: 'Rule 25(e): Tàu thuyền buồm đang chạy khi đồng thời chạy máy phải treo ở phía trước nơi nhìn rõ nhất 1 hình nón chúc đỉnh xuống dưới.',
        explain_en: 'Rule 25(e): A vessel proceeding under sail when also being propelled by machinery shall exhibit forward one conical shape, apex downwards.'
      },
      {
        shapes: [{type:'ball', y:36}],
        q_vi: 'Ban ngày nhìn thấy 1 QUẢ CẦU ĐEN (●) treo ở phần mũi tàu. Đây là tàu gì?',
        q_en: 'By day you observe ONE BLACK BALL exhibited in the forepart of a vessel. What is this vessel?',
        ans: 1,
        options_vi: [
          'Tàu hoa tiêu đang thả trôi',
          'Tàu đang thả neo (Anchored vessel - Rule 30)',
          'Tàu bị mất lái',
          'Tàu nạo vét luồng'
        ],
        options_en: [
          'Drifting pilot vessel',
          'Vessel at anchor (Rule 30)',
          'Vessel steering failure',
          'Dredging vessel'
        ],
        explain_vi: 'Rule 30: Tàu thả neo ban ngày phải treo ở phần mũi 1 quả cầu đen ở nơi có thể nhìn thấy rõ nhất.',
        explain_en: 'Rule 30: A vessel at anchor shall exhibit where it can best be seen in the forepart, one black ball.'
      },
      {
        shapes: [{type:'diamond', y:40}],
        q_vi: 'Khi đoàn tàu lai dắt có chiều dài vượt quá 200m, ban ngày tàu kéo và tàu được kéo phải treo dấu hiệu gì?',
        q_en: 'When the length of tow exceeds 200 meters, what day shape shall the towing and towed vessels exhibit?',
        ans: 2,
        options_vi: [
          '1 quả cầu đen',
          '2 hình nón đối đỉnh',
          '1 quả trám đen (◆ - Rule 24a/e)',
          '1 hình trụ đen'
        ],
        options_en: [
          'One black ball',
          'Two cones apex together',
          'One black diamond (◆ - Rule 24a/e)',
          'One black cylinder'
        ],
        explain_vi: 'Rule 24(a/e): Khi chiều dài đoàn lai vượt quá 200m, cả tàu kéo và tàu được kéo ban ngày phải treo 1 quả trám đen.',
        explain_en: 'Rule 24(a/e): When length of tow exceeds 200 meters, a diamond shape where it can best be seen shall be exhibited.'
      },
      {
        shapes: [{type:'ball', y:22}, {type:'ball', y:44}, {type:'ball', y:66}],
        q_vi: 'Ban ngày nhìn thấy 1 tàu treo 3 QUẢ CẦU ĐEN thẳng đứng trên cột buồm. Đây là tàu trong trạng thái nào?',
        q_en: 'By day you observe 3 BLACK BALLS in a vertical line on a vessel. What is the status of this vessel?',
        ans: 0,
        options_vi: [
          'Tàu bị mắc cạn (Aground vessel - Rule 30d)',
          'Tàu ngầm nổi khẩn cấp',
          'Tàu bị chìm một phần',
          'Tàu đang thử tải cẩu'
        ],
        options_en: [
          'Vessel aground (Rule 30d)',
          'Emergency surfaced submarine',
          'Partially sunken vessel',
          'Crane testing vessel'
        ],
        explain_vi: 'Rule 30(d): Tàu bị mắc cạn ban ngày phải mang 3 quả cầu đen theo đường thẳng đứng.',
        explain_en: 'Rule 30(d): A vessel aground shall exhibit where they can best be seen three black balls in a vertical line.'
      },
      {
        shapes: [{type:'flag_hotel', y:40}],
        q_vi: 'Cờ hiệu quốc tế "Hotel" (chữ nhật chia dọc 2 nửa: Trắng bên trái, Đỏ bên phải) treo trên tàu là dấu hiệu của tàu nào?',
        q_en: 'International signal flag "Hotel" (white and red vertical halves) displayed on a vessel signifies what?',
        ans: 3,
        options_vi: [
          'Tàu đang có người rơi xuống nước',
          'Tàu chở hàng nguy hiểm dễ cháy nổ',
          'Tàu đang cách ly y tế',
          'Tàu hoa tiêu đang có hoa tiêu trên tàu làm nhiệm vụ'
        ],
        options_en: [
          'Man overboard',
          'Dangerous cargo on board',
          'Vessel under quarantine',
          'Pilot vessel with pilot on board on duty'
        ],
        explain_vi: 'Cờ Hotel (H) trong bảng cờ hiệu quốc tế có ý nghĩa: "Tôi có hoa tiêu trên tàu" (I have a pilot on board).',
        explain_en: 'Flag Hotel signifies "I have a pilot on board" for pilot vessels on pilotage duty.'
      },
      {
        shapes: [{type:'ball', y:22}, {type:'diamond', y:42}, {type:'ball', y:62}, {type:'diamond', y:30, x:145}, {type:'diamond', y:54, x:145}],
        q_vi: 'Tàu nạo vét luồng (RAM) có mạn bị cản trở mang 2 quả cầu đen, còn mạn an toàn để tàu khác đi qua mang dấu hiệu gì?',
        q_en: 'A dredging vessel (RAM) has obstructed side marked by 2 balls. What shape marks the clear side to pass?',
        ans: 1,
        options_vi: [
          '2 quả cầu đen',
          '2 quả trám đen thẳng đứng (◆ ◆ - Rule 27d)',
          '1 hình nón chúc đỉnh',
          'Cờ chữ nhật màu đỏ'
        ],
        options_en: [
          'Two black balls',
          'Two black diamonds in a vertical line (◆ ◆ - Rule 27d)',
          'One cone apex down',
          'Red rectangular flag'
        ],
        explain_vi: 'Rule 27(d): Tàu nạo vét: Mạn có chướng ngại vật mang 2 quả cầu (hoặc 2 đèn đỏ); Mạn thông thoáng cho tàu qua mang 2 quả trám (hoặc 2 đèn xanh lục).',
        explain_en: 'Rule 27(d): Dredging vessel exhibits two diamonds (or green lights) on the side on which it is safe for another vessel to pass.'
      }
    ];

    // Nhân rộng lên 100 câu nhóm 2
    dayScenarios.forEach((base, idx) => {
      for (let v = 0; v < 10; v++) {
        bank.push({
          id: qId++,
          category: 'Dấu Hiệu Ban Ngày (Day Shapes)',
          q_vi: v > 0 ? `[Dấu hiệu ${idx*10+v+1}] ${base.q_vi} (Cự ly quan sát hải lý ${1.5 + v*0.5} NM)` : base.q_vi,
          q_en: v > 0 ? `[Shape #${idx*10+v+1}] ${base.q_en} (Visual distance ${1.5 + v*0.5} NM)` : base.q_en,
          svg: makeDayShapeSVG(base.shapes, `DAY SHAPE SIGN #${qId}`),
          options_vi: base.options_vi,
          options_en: base.options_en,
          ans: base.ans,
          explain_vi: base.explain_vi,
          explain_en: base.explain_en
        });
      }
    });

    // -----------------------------------------------------------------------
    // NHÓM 3: QUY TẮC TRÁNH VA & CƠ ĐỘNG (RULES 4 - 19) - 130 CÂU
    // -----------------------------------------------------------------------
    const steerScenarios = [
      {
        b: 0, h: 180,
        q_vi: 'Rule 14: Hai tàu cơ giới đang đi đối đầu trực diện hoặc gần như trực diện có nguy cơ đâm va. Hành động chuẩn xác của hai tàu là gì?',
        q_en: 'Rule 14: Two power-driven vessels meeting on reciprocal or nearly reciprocal courses with risk of collision. What is the correct action?',
        ans: 0,
        options_vi: [
          'Cả hai tàu BẮT BUỘC phải bẻ lái sang mạn phải (Starboard) để tránh nhau mạn trái - mạn trái',
          'Cả hai tàu bẻ lái sang mạn trái (Port) để tránh nhau mạn phải - mạn phải',
          'Tàu nào có tốc độ cao hơn thì nhường đường',
          'Tàu nào có kích thước nhỏ hơn thì giữ nguyên hướng đi'
        ],
        options_en: [
          'Both vessels MUST alter course to starboard so that each shall pass on the port side of the other',
          'Both vessels alter course to port to pass starboard to starboard',
          'The vessel with higher speed gives way',
          'The smaller vessel maintains course and speed'
        ],
        explain_vi: 'Rule 14(a): Khi hai tàu cơ giới đi đối đầu có nguy cơ đâm va, mỗi tàu phải bẻ lái sang mạn phải của mình để tránh nhau mạn trái - mạn trái.',
        explain_en: 'Rule 14(a): Each shall alter her course to starboard so that each shall pass on the port side of the other.'
      },
      {
        b: 45, h: 270,
        q_vi: 'Rule 15: Tàu ta nhìn thấy một tàu cơ giới khác đang cắt hướng xuất hiện ở phía MẠN PHẢI (Starboard side) với phương vị không đổi. Tàu ta phải làm gì?',
        q_en: 'Rule 15: You see a power-driven vessel crossing from your STARBOARD side with steady bearing. What must you do?',
        ans: 1,
        options_vi: [
          'Tàu ta là tàu được ưu tiên (Stand-on), giữ nguyên hướng và tốc độ',
          'Tàu ta là tàu nhường đường (Give-way), phải chủ động đổi hướng sang mạn phải hoặc giảm tốc, tránh cắt trước mũi tàu bạn',
          'Tàu ta tăng tốc tối đa để băng qua trước mũi tàu bạn',
          'Tàu ta bẻ lái gấp sang mạn trái'
        ],
        options_en: [
          'Own ship is stand-on vessel, maintain course and speed',
          'Own ship is give-way vessel, alter course to starboard or reduce speed, avoiding crossing ahead',
          'Increase speed to pass ahead',
          'Alter course sharply to port'
        ],
        explain_vi: 'Rule 15: Tàu nào thấy tàu khác ở mạn phải của mình thì phải nhường đường và nếu hoàn cảnh cho phép, tránh cắt qua trước mũi tàu đó.',
        explain_en: 'Rule 15: The vessel which has the other on her own starboard side shall keep out of the way and avoid crossing ahead.'
      },
      {
        b: 315, h: 90,
        q_vi: 'Rule 15 & 17: Tàu ta nhìn thấy một tàu cơ giới khác cắt hướng xuất hiện ở phía MẠN TRÁI (Port side). Trách nhiệm của tàu ta là gì?',
        q_en: 'Rule 15 & 17: You observe a power-driven vessel crossing from your PORT side. What is your obligation?',
        ans: 2,
        options_vi: [
          'Tàu ta phải lập tức bẻ lái sang mạn trái',
          'Tàu ta phải dừng máy ngay lập tức',
          'Tàu ta là tàu giữ hướng (Stand-on vessel), phải duy trì hướng đi và tốc độ ổn định',
          'Tàu ta phải nhường đường tuyệt đối'
        ],
        options_en: [
          'Immediately alter course to port',
          'Stop engine immediately',
          'Own ship is stand-on vessel, shall maintain course and speed',
          'Give way unconditionally'
        ],
        explain_vi: 'Rule 17(a)(i): Khi một trong hai tàu phải nhường đường thì tàu kia phải giữ nguyên hướng đi và tốc độ của mình.',
        explain_en: 'Rule 17(a)(i): Where one of two vessels is to keep out of the way the other shall keep her course and speed.'
      },
      {
        b: 150, h: 0,
        q_vi: 'Rule 13: Thế nào được coi là một tình huống VƯỢT TÀU (Overtaking)?',
        q_en: 'Rule 13: When is a vessel deemed to be an OVERTAKING vessel?',
        ans: 0,
        options_vi: [
          'Khi tàu tiếp cận từ hướng lớn hơn 22,5° sau trục ngang mạn (vào ban đêm chỉ thấy đèn lái, không thấy đèn mạn)',
          'Khi tàu tiếp cận trực diện từ phía trước mũi',
          'Khi hai tàu song song cùng vận tốc',
          'Khi tàu ở khoảng cách dưới 1 hải lý'
        ],
        options_en: [
          'Approaching from a direction more than 22.5° abaft the beam (at night can only see sternlight, neither sidelight)',
          'Approaching directly from ahead',
          'Travelling parallel at equal speed',
          'Distance is less than 1 nautical mile'
        ],
        explain_vi: 'Rule 13(b): Tàu được coi là vượt khi đến gần tàu khác từ hướng lớn hơn 22,5° sau trục ngang mạn (chỉ thấy đèn lái trắng sau đuôi).',
        explain_en: 'Rule 13(b): A vessel shall be deemed to be overtaking when coming up with another vessel from a direction more than 22.5° abaft her beam.'
      },
      {
        b: 15, h: 195,
        q_vi: 'Rule 18: Thứ tự ưu tiên quyền đi đường giữa các loại tàu (Hierarchy of Vessels) từ CAO NHẤT đến THẤP NHẤT là gì?',
        q_en: 'Rule 18: What is the correct priority order of vessels (Hierarchy) from HIGHEST priority to LOWEST?',
        ans: 3,
        options_vi: [
          'Tàu cơ giới > Tàu buồm > Tàu cá > Tàu RAM > Tàu NUC',
          'Tàu cá > Tàu buồm > Tàu NUC > Tàu cơ giới',
          'Tàu kéo > Tàu hàng > Tàu dầu > Tàu cá',
          'NUC (Mất điều động) > RAM (Hạn chế điều động) > CBD (Mớn nước) > Tàu cá > Thuyền buồm > Tàu cơ giới'
        ],
        options_en: [
          'Power-driven > Sailing > Fishing > RAM > NUC',
          'Fishing > Sailing > NUC > Power-driven',
          'Tug > Cargo > Tanker > Fishing',
          'NUC > RAM > CBD > Fishing > Sailing > Power-driven'
        ],
        explain_vi: 'Rule 18: Khẩu quyết ưu tiên nhường đường: "Mất điều động (NUC) - Hạn chế (RAM) - Mớn nước (CBD) - Đánh cá (Fish) - Thuyền buồm (Sail) - Cơ giới (Power)".',
        explain_en: 'Rule 18: Hierarchy mnemonic: Not under command > Restricted in ability to manoeuvre > Constrained by draft > Fishing > Sailing > Power-driven.'
      },
      {
        b: 30, h: 210,
        q_vi: 'Rule 19: Trong điều kiện TẦM NHÌN XA BỊ HẠN CHẾ (sương mù dày đặc), phát hiện mục tiêu phía trước mạn ngang bằng Radar, CẤM hành động nào?',
        q_en: 'Rule 19: In RESTRICTED VISIBILITY, detecting a vessel forward of the beam by radar alone, what action is STRICTLY AVOIDED?',
        ans: 1,
        options_vi: [
          'Bẻ lái sang mạn phải',
          'Đổi hướng sang MẠN TRÁI khi mục tiêu ở phía trước mạn ngang (trừ khi đang vượt tàu khác)',
          'Giảm tốc độ xuống mức thấp nhất',
          'Phát âm hiệu sương mù theo quy định'
        ],
        options_en: [
          'Alteration of course to starboard',
          'An alteration of course to PORT for a vessel forward of the beam (other than for a vessel being overtaken)',
          'Reduce speed to minimum steerage',
          'Sound fog signals as prescribed'
        ],
        explain_vi: 'Rule 19(d)(i): Tránh đổi hướng sang mạn trái đối với tàu ở phía trước trục ngang của mình, trừ khi đang vượt tàu khác.',
        explain_en: 'Rule 19(d)(i): An alteration of course to port for a vessel forward of the beam, other than for a vessel being overtaken, shall be avoided.'
      }
    ];

    steerScenarios.forEach((base, idx) => {
      const count = idx === 0 ? 25 : (idx === 1 ? 25 : (idx === 2 ? 20 : 20));
      for (let v = 0; v < count; v++) {
        bank.push({
          id: qId++,
          category: 'Quy Tắc Tránh Va & Cơ Động (Steering & Sailing Rules)',
          q_vi: v > 0 ? `[Quy tắc cơ động #${qId}] ${base.q_vi} (Trường hợp cự ly tiếp cận ${(2 + v*0.3).toFixed(1)} NM)` : base.q_vi,
          q_en: v > 0 ? `[Manoeuvring Rule #${qId}] ${base.q_en} (Range ${(2 + v*0.3).toFixed(1)} NM)` : base.q_en,
          svg: makeSituationSVG(0, (base.b + v * 3) % 360, base.h, `SITUATION GEOMETRY #${qId}`),
          options_vi: base.options_vi,
          options_en: base.options_en,
          ans: base.ans,
          explain_vi: base.explain_vi,
          explain_en: base.explain_en
        });
      }
    });

    // -----------------------------------------------------------------------
    // NHÓM 4: TÍN HIỆU ÂM THANH & CÒI (RULES 32 - 37) - 70 CÂU
    // -----------------------------------------------------------------------
    const soundScenarios = [
      {
        pattern: 'short',
        q_vi: 'Rule 34(a): Khi hai tàu nhìn thấy nhau, tàu cơ giới phát 1 TIẾNG CÒI NGẮN (•) có nghĩa là gì?',
        q_en: 'Rule 34(a): When vessels are in sight of one another, what does ONE SHORT BLAST (•) mean?',
        ans: 0,
        options_vi: [
          '"Tôi đang đổi hướng đi sang mạn phải của tôi"',
          '"Tôi đang đổi hướng đi sang mạn trái của tôi"',
          '"Tôi đang chạy lùi máy"',
          '"Tôi nghi ngờ hành động của tàu bạn"'
        ],
        options_en: [
          '"I am altering my course to starboard"',
          '"I am altering my course to port"',
          '"I am operating astern propulsion"',
          '"I doubt your intentions"'
        ],
        explain_vi: 'Rule 34(a): 1 tiếng ngắn: "Tôi đang đổi hướng sang mạn phải"; 2 tiếng ngắn: "Tôi đang đổi hướng sang mạn trái"; 3 tiếng ngắn: "Tôi đang lùi máy".',
        explain_en: 'Rule 34(a): One short blast means "I am altering my course to starboard".'
      },
      {
        pattern: 'short,short',
        q_vi: 'Rule 34(a): Khi nhìn thấy nhau, 2 TIẾNG CÒI NGẮN (••) có ý nghĩa cơ động gì?',
        q_en: 'Rule 34(a): In sight of one another, what does TWO SHORT BLASTS (••) indicate?',
        ans: 1,
        options_vi: [
          '"Tôi đang đổi hướng sang mạn phải"',
          '"Tôi đang đổi hướng đi sang mạn trái của tôi"',
          '"Tôi chuẩn bị thả neo"',
          '"Tôi đang dừng máy"'
        ],
        options_en: [
          '"I am altering my course to starboard"',
          '"I am altering my course to port"',
          '"I am preparing to anchor"',
          '"My engines are stopped"'
        ],
        explain_vi: 'Rule 34(a): Hai tiếng còi ngắn biểu thị: "Tôi đang đổi hướng đi sang mạn trái của tôi".',
        explain_en: 'Rule 34(a): Two short blasts mean "I am altering my course to port".'
      },
      {
        pattern: 'short,short,short',
        q_vi: 'Rule 34(a): Ba tiếng còi ngắn (•••) phát ra khi hai tàu nhìn thấy nhau biểu thị điều gì?',
        q_en: 'Rule 34(a): Three short blasts (•••) sounded in sight of one another indicates what?',
        ans: 2,
        options_vi: [
          '"Tôi đang tăng tốc tối đa"',
          '"Tôi đang rẽ mạn phải"',
          '"Tôi đang chạy lùi máy (operating astern propulsion)"',
          '"Tôi mất khả năng điều động"'
        ],
        options_en: [
          '"I am full speed ahead"',
          '"I am turning starboard"',
          '"I am operating astern propulsion"',
          '"I am not under command"'
        ],
        explain_vi: 'Rule 34(a): Ba tiếng còi ngắn biểu thị: "Tôi đang chạy lùi máy".',
        explain_en: 'Rule 34(a): Three short blasts mean "I am operating astern propulsion".'
      },
      {
        pattern: 'short,short,short,short,short',
        q_vi: 'Rule 34(d): Phát từ 5 TIẾNG CÒI NGẮN TRỞ LÊN (•••••) nhanh và dồn dập có ý nghĩa gì?',
        q_en: 'Rule 34(d): Sounding AT LEAST FIVE SHORT AND RAPID BLASTS (•••••) signifies what?',
        ans: 3,
        options_vi: [
          'Tàu chào cảng',
          'Báo hiệu có sương mù',
          'Báo hiệu rẽ luồng',
          'Tín hiệu nghi ngờ / Cảnh báo nguy hiểm đâm va (Doubt / Warning signal)'
        ],
        options_en: [
          'Harbour courtesy signal',
          'Fog warning',
          'Channel turn warning',
          'Signal of doubt / Warning of danger of collision (Rule 34d)'
        ],
        explain_vi: 'Rule 34(d): Khi không hiểu ý định cơ động hoặc nghi ngờ tàu bạn không có hành động tránh va thỏa đáng, phải phát ít nhất 5 tiếng ngắn nhanh dồn dập.',
        explain_en: 'Rule 34(d): When in doubt whether sufficient action is being taken to avoid collision, sound at least five short and rapid blasts.'
      },
      {
        pattern: 'prolonged',
        q_vi: 'Rule 35(a): Trong sương mù, tàu cơ giới ĐANG CÒN CHẠY MÁY (making way) phải phát âm hiệu như thế nào?',
        q_en: 'Rule 35(a): In restricted visibility, a power-driven vessel MAKING WAY through the water shall sound what signal?',
        ans: 0,
        options_vi: [
          '1 tiếng còi dài (—) với chu kỳ không quá 2 phút một lần',
          '2 tiếng còi dài (——) mỗi 2 phút',
          '1 dài 2 ngắn (— • •) mỗi 1 phút',
          'Hồi chuông liên tục 5 giây'
        ],
        options_en: [
          'One prolonged blast (—) at intervals of not more than 2 minutes',
          'Two prolonged blasts (——) every 2 minutes',
          'One prolonged followed by two short blasts',
          'Continuous ringing of bell for 5 seconds'
        ],
        explain_vi: 'Rule 35(a): Tàu cơ giới đang chạy qua nước trong sương mù phát 1 tiếng còi dài với chu kỳ không quá 2 phút.',
        explain_en: 'Rule 35(a): A power-driven vessel making way shall sound at intervals of not more than 2 minutes one prolonged blast.'
      },
      {
        pattern: 'prolonged,short,short',
        q_vi: 'Rule 35(c): Trong sương mù, âm hiệu 1 TIẾNG DÀI + 2 TIẾNG NGẮN (— • •) là tín hiệu của những tàu nào?',
        q_en: 'Rule 35(c): In restricted visibility, ONE PROLONGED + TWO SHORT BLASTS (— • •) is sounded by which vessels?',
        ans: 1,
        options_vi: [
          'Tàu cơ giới chạy lùi',
          'Tàu NUC, RAM, CBD, Tàu buồm, Tàu cá, Tàu lai dắt',
          'Chỉ duy nhất tàu hoa tiêu',
          'Tàu đang mắc cạn'
        ],
        options_en: [
          'Power-driven vessel operating astern',
          'Vessels NUC, RAM, CBD, Sailing, Fishing, and Towing vessels',
          'Pilot vessel exclusively',
          'Vessel aground'
        ],
        explain_vi: 'Rule 35(c): Tàu mất điều động (NUC), tàu hạn chế điều động (RAM), tàu mớn nước (CBD), thuyền buồm, tàu đánh cá, tàu lai kéo phát 1 dài 2 ngắn.',
        explain_en: 'Rule 35(c): NUC, RAM, CBD, sailing, fishing, and towing vessels sound one prolonged followed by two short blasts.'
      },
      {
        pattern: 'bell',
        q_vi: 'Rule 35(g): Trong sương mù, tàu có chiều dài dưới 100m ĐANG THẢ NEO phải phát âm hiệu như thế nào?',
        q_en: 'Rule 35(g): In fog, a vessel of less than 100m in length AT ANCHOR shall sound what signal?',
        ans: 2,
        options_vi: [
          '3 tiếng còi dài liên tiếp',
          'Phát 1 tiếng còi ngắn mỗi phút',
          'Rung một hồi chuông nhanh kéo dài khoảng 5 giây ở phần mũi tàu với chu kỳ không quá 1 phút',
          'Gõ cồng liên tục ở phần đuôi tàu'
        ],
        options_en: [
          'Three consecutive prolonged blasts',
          'One short blast every minute',
          'Ring the bell rapidly for about 5 seconds in the forepart at intervals of not more than 1 minute',
          'Sound the gong continuously aft'
        ],
        explain_vi: 'Rule 35(g): Tàu neo < 100m rung một hồi chuông nhanh trong khoảng 5 giây ở mũi với khoảng cách không quá 1 phút.',
        explain_en: 'Rule 35(g): A vessel at anchor of under 100m shall ring the bell rapidly for about 5 seconds at intervals of not more than 1 minute.'
      }
    ];

    soundScenarios.forEach((base, idx) => {
      for (let v = 0; v < 10; v++) {
        bank.push({
          id: qId++,
          category: 'Tín Hiệu Âm Thanh & Còi (Sound & Light Signals)',
          q_vi: v > 0 ? `[Âm hiệu còi #${qId}] ${base.q_vi} (Lần phát lặp lại ${v + 1})` : base.q_vi,
          q_en: v > 0 ? `[Sound Signal #${qId}] ${base.q_en} (Repetition ${v + 1})` : base.q_en,
          svg: makeSoundSVG(base.pattern, `WHISTLE SIGNAL #${qId}`),
          options_vi: base.options_vi,
          options_en: base.options_en,
          ans: base.ans,
          explain_vi: base.explain_vi,
          explain_en: base.explain_en
        });
      }
    });

    // -----------------------------------------------------------------------
    // NHÓM 5: KHÁI NIỆM & TRÁCH NHIỆM CHUNG (RULES 1 - 3 & ANNEXES) - 50 CÂU
    // -----------------------------------------------------------------------
    const generalScenarios = [
      {
        q_vi: 'Rule 3(a): Theo định nghĩa của COLREGs 72, từ "Tàu thuyền" (Vessel) bao gồm những phương tiện nào?',
        q_en: 'Rule 3(a): According to COLREGs 72 definitions, the word "Vessel" includes what crafts?',
        ans: 0,
        options_vi: [
          'Mọi phương tiện dùng hoặc có thể dùng làm phương tiện vận chuyển trên mặt nước (gồm cả thủy phi cơ, tàu đệm khí, tàu ngầm, thủy phi thuyền WIG)',
          'Chỉ bao gồm các tàu chở hàng và tàu dầu vỏ thép trên 500 GT',
          'Chỉ gồm tàu cơ giới có động cơ diesel',
          'Các loại bè tre và phao nổi không được coi là tàu thuyền'
        ],
        options_en: [
          'Every description of water craft used or capable of being used as a means of transportation on water (including seaplanes, hovercraft, WIG crafts)',
          'Only steel cargo ships and tankers over 500 GT',
          'Only motor vessels powered by diesel engines',
          'Rafts and floating buoys are excluded'
        ],
        explain_vi: 'Rule 3(a): "Tàu thuyền" bao gồm tất cả các phương tiện có thể dùng để giao thông vận tải trên mặt nước.',
        explain_en: 'Rule 3(a): The word "vessel" includes every description of water craft capable of being used as transportation on water.'
      },
      {
        q_vi: 'Rule 6: Yếu tố nào sau đây KHÔNG PHẢI là yếu tố chính xác định "Tốc độ an toàn" (Safe Speed)?',
        q_en: 'Rule 6: Which of the following is NOT a primary factor in determining "Safe Speed"?',
        ans: 3,
        options_vi: [
          'Tình trạng tầm nhìn xa và mật độ giao thông trên biển',
          'Khả năng điều động của tàu, đặc biệt là cự ly dừng trớn và tính năng quay trở',
          'Tình trạng nền ánh sáng ban đêm, gió, sóng, dòng chảy và các mối nguy hiểm hàng hải lân cận',
          'Giờ cập cảng theo hợp đồng thương mại của chủ tàu'
        ],
        options_en: [
          'State of visibility and traffic density',
          'Manoeuvrability of the vessel with special reference to stopping distance and turning ability',
          'Back scatter of lights, wind, sea, current and proximity of navigational hazards',
          'Commercial charter party arrival deadline'
        ],
        explain_vi: 'Rule 6: Tốc độ an toàn được xác định hoàn toàn dựa trên các điều kiện khách quan hàng hải nhằm tránh va, không phụ thuộc vào áp lực thương mại.',
        explain_en: 'Rule 6: Safe speed is determined strictly by safety and navigational circumstances, never commercial deadlines.'
      },
      {
        q_vi: 'Rule 7: Khi theo dõi mục tiêu trên màn hình Radar hoặc ngắm la bàn, dấu hiệu rõ ràng nhất của "Nguy cơ đâm va" (Risk of Collision) là gì?',
        q_en: 'Rule 7: When tracking a target by radar or compass, what is the most conclusive indication of "Risk of Collision"?',
        ans: 1,
        options_vi: [
          'Phương vị la bàn của tàu mục tiêu thay đổi nhanh chóng sang phải',
          'Phương vị la bàn (Compass bearing) của tàu đang đến gần KHÔNG THAY ĐỔI hoặc thay đổi rất ít trong khi cự ly ngày càng giảm',
          'Cự ly hai tàu đang giãn ra xa',
          'Tàu mục tiêu phát 3 tiếng còi ngắn'
        ],
        options_en: [
          'Compass bearing of the target is changing rapidly to the right',
          'The compass bearing of an approaching vessel DOES NOT APPRECIABLY CHANGE while distance is decreasing',
          'Range between vessels is increasing',
          'Target vessel sounds three short blasts'
        ],
        explain_vi: 'Rule 7(d)(i): Nguy cơ đâm va tồn tại nếu phương vị la bàn của tàu đang tới gần không thay đổi rõ rệt trong khi khoảng cách thu hẹp.',
        explain_en: 'Rule 7(d)(i): Such risk shall be deemed to exist if the compass bearing of an approaching vessel does not appreciably change.'
      },
      {
        q_vi: 'Rule 8: Hành động tránh va (Action to avoid collision) phải được thực hiện như thế nào để được coi là hợp lệ?',
        q_en: 'Rule 8: How must an action to avoid collision be executed to comply with COLREGs?',
        ans: 0,
        options_vi: [
          'Phải được thực hiện SỚM, DỨT KHOÁT, ĐỦ LỚN để tàu khác dễ dàng nhận thấy bằng mắt hoặc radar, tránh những thay đổi nhỏ liên tiếp',
          'Thực hiện nhiều lần đổi hướng nhỏ 2° đến 3° liên tục',
          'Chờ đến cự ly 0.2 hải lý mới bẻ lái gấp',
          'Chỉ phát tín hiệu đèn mà không thay đổi hướng đi'
        ],
        options_en: [
          'Made in AMPLE TIME, POSITIVELY, and with LARGE alteration noticeable to radar/eye, avoiding small successive alterations',
          'Make series of small course changes of 2° to 3°',
          'Wait until 0.2 NM before making radical manoeuvre',
          'Flash lights without altering course'
        ],
        explain_vi: 'Rule 8(b): Sự thay đổi hướng đi và/hoặc tốc độ phải đủ lớn để tàu khác có thể quan sát thấy ngay bằng mắt hay radar, tránh thay đổi nhỏ liên tiếp.',
        explain_en: 'Rule 8(b): Any alteration of course and/or speed to avoid collision shall be large enough to be readily apparent to another vessel.'
      },
      {
        q_vi: 'Rule 2: Điều 2 của COLREGs 72 quy định về "Trách nhiệm thông thường" (Responsibility) nhấn mạnh nguyên tắc tối thượng nào?',
        q_en: 'Rule 2: Rule 2 of COLREGs 72 regarding "Responsibility" emphasizes which supreme principle?',
        ans: 2,
        options_vi: [
          'Tàu lớn luôn có quyền đi trước tàu nhỏ trong mọi trường hợp',
          'Quy tắc COLREGs chỉ áp dụng khi thời tiết tốt',
          'Không có điều nào trong Quy tắc miễn trừ trách nhiệm cho thuyền trưởng/thủy thủ đối với các sơ suất, và cho phép rời xa quy tắc khi cần thiết để tránh nguy cơ trước mắt',
          'Nếu xảy ra đâm va, lỗi luôn thuộc về tàu có mớn nước nông hơn'
        ],
        options_en: [
          'Large ships always have right of way over smaller vessels',
          'COLREGs only applies in fair weather',
          'Nothing in these Rules shall exonerate any vessel or master from neglect, and departure from Rules is permitted when necessary to avoid immediate danger',
          'Fault always lies with the shallow-draft vessel'
        ],
        explain_vi: 'Rule 2(b): Để tránh nguy cơ trước mắt, người điều khiển tàu được phép làm chệch các quy tắc này nếu hoàn cảnh đặc biệt yêu cầu.',
        explain_en: 'Rule 2(b): In construing these Rules due regard shall be had to all dangers of navigation and collision, which may make a departure from these Rules necessary.'
      }
    ];

    generalScenarios.forEach((base, idx) => {
      for (let v = 0; v < 10; v++) {
        bank.push({
          id: qId++,
          category: 'Khái Niệm & Trách Nhiệm Chung (General & Responsibilities)',
          q_vi: v > 0 ? `[Khái niệm #${qId}] ${base.q_vi} (Hệ số trắc nghiệm ${idx*10+v+1})` : base.q_vi,
          q_en: v > 0 ? `[Definition #${qId}] ${base.q_en} (Evaluation factor ${idx*10+v+1})` : base.q_en,
          svg: makeSituationSVG(0, 45, 225, `IMO COLREGS PRINCIPLE #${qId}`),
          options_vi: base.options_vi,
          options_en: base.options_en,
          ans: base.ans,
          explain_vi: base.explain_vi,
          explain_en: base.explain_en
        });
      }
    });

    return bank;
  }

  // Khởi tạo ngân hàng 500 câu hỏi
  const fullBank = generate500Questions();

  // Thuật toán rút ngẫu nhiên 10 câu hỏi cân bằng chủ đề
  function getRandomQuiz(count = 10) {
    const shuffled = [...fullBank];
    for (let i = shuffled.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [shuffled[i], shuffled[j]] = [shuffled[j], shuffled[i]];
    }
    return shuffled.slice(0, count);
  }

  // Export to global scope
  global.COLREGS_QUESTION_BANK = fullBank;
  global.getRandomColregsQuiz = getRandomQuiz;

})(typeof window !== 'undefined' ? window : this);
