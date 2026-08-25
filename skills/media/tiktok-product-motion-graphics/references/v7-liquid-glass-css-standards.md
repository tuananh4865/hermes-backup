# V7 Liquid Glass - CSS Standards Migration Guide (18/07/2026)

> **Status:** V7 là FINAL APPROVED version (anh approved 18/07/2026).
> **Use when:** Bắt đầu clip mới HOẶC update clip cũ từ V6 sang V7.

---

## 1. CSS Variables (dùng để DRY)

```css
:root {
  /* V7 liquid glass tokens */
  --glass-bg: rgba(255, 255, 255, 0.18);
  --glass-blur: blur(48px) saturate(200%);
  --glass-border: 1.5px solid rgba(255, 255, 255, 0.4);
  --glass-radius: 36px;
  --glass-shadow: 0 14px 42px rgba(0, 0, 0, 0.55), inset 0 2px 0 rgba(255, 255, 255, 0.22);
  --glass-padding: 40px 36px;
  
  /* V7 typography scale */
  --text-eyebrow: 36px;
  --text-title: 64px;
  --text-subtitle: 40px;
  --text-num-big: 128px;
  --text-cta-price: 160px;
  --text-cta-big-title: 80px;
  --text-cta-big-spec: 36px;
  
  /* V7 colors */
  --color-gold: #d4a017;
  --color-gold-bright: #FFD700;
  --color-text-dark: #1a1a1a;
  --color-text-white: #fff;
  --color-text-gray: #444;
}
```

---

## 2. Reusable .phase-glass (copy-paste cho mọi clip)

```css
.phase-glass {
  position: absolute;
  z-index: 20;
  left: 56px;
  right: 56px;
  padding: var(--glass-padding);
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: var(--glass-border);
  border-radius: var(--glass-radius);
  box-shadow: var(--glass-shadow);
  text-align: center;
  opacity: 0;
}

.phase-glass::before {
  content: '';
  position: absolute;
  inset: -8% -4%;
  background: var(--glass-bg);
  backdrop-filter: var(--glass-blur);
  -webkit-backdrop-filter: var(--glass-blur);
  border: var(--glass-border);
  border-radius: var(--glass-radius);
  z-index: -1;
}

.phase-glass::after {
  content: '';
  position: absolute;
  inset: -8% -4%;
  border-radius: var(--glass-radius);
  background: radial-gradient(
    circle at 15% 0%,
    rgba(255, 255, 255, 0.22),
    transparent 50%
  );
  z-index: -1;
  pointer-events: none;
}
```

---

## 3. Text motion stagger pattern (V7 core feature)

```js
/**
 * Stagger text reveal từng dòng với clipPath
 * @param {gsap.timeline} tl - GSAP timeline
 * @param {string} glassSelector - CSS selector cho glass card
 * @param {number} baseTime - Thời điểm bắt đầu stagger
 * @param {number} stagger - Khoảng cách giữa các dòng (default 0.12s)
 */
function staggerText(tl, glassSelector, baseTime, stagger = 0.12) {
  const lines = document.querySelectorAll(`${glassSelector} .text-line`);
  if (lines.length === 0) {
    console.warn(`[staggerText] No .text-line found in ${glassSelector}`);
    return;
  }
  lines.forEach((el, i) => {
    tl.fromTo(el,
      { clipPath: 'inset(0 100% 0 0)', opacity: 0 },
      { clipPath: 'inset(0 0% 0 0)', opacity: 1, 
        duration: 0.45, ease: 'power2.out' },
      baseTime + i * stagger, null);
  });
}

// Usage HOOK phase:
// 1. Card fade-in
tl.fromTo(hookGlass, { opacity: 0, y: 60 }, 
  { opacity: 1, y: 0, duration: 0.5, ease: 'back.out(1.5)' }, 0.3);

// 2. Stagger 3 text lines
staggerText(tl, '.hook-glass', 0.5);

// 3. Card fade-out
tl.to(hookGlass, { opacity: 0, duration: 0.4 }, 7.3);
```

---

## 4. CountUp pattern cho số lớn

```js
// Số nguyên (25.000)
tl.fromTo('.num-big', { textContent: 0 }, {
  textContent: 25000,
  duration: 1.5,
  ease: 'power2.out',
  snap: { textContent: 1 }
}, 0.5);

// Số có hậu tố "K" (495K)
tl.fromTo('.price-big', { textContent: 0 }, {
  textContent: 495,
  duration: 1.2,
  ease: 'power2.out',
  snap: { textContent: 1 },
  onUpdate: function() {
    this.targets()[0].textContent = Math.round(this.targets()[0].textContent) + 'K';
  }
}, 0.5);

// Số phần trăm (95%)
tl.fromTo('.percent-num', { textContent: 0 }, {
  textContent: 95,
  duration: 1.5,
  ease: 'power2.out',
  snap: { textContent: 1 },
  onUpdate: function() {
    this.targets()[0].textContent = Math.round(this.targets()[0].textContent) + '%';
  }
}, 0.5);

// Số nhân (6.2x)
tl.fromTo('.multiplier-num', { textContent: 0 }, {
  textContent: 6.2,
  duration: 1.2,
  ease: 'power2.out',
  snap: { textContent: 0.1 },
  onUpdate: function() {
    this.targets()[0].textContent = this.targets()[0].textContent.toFixed(1) + 'x';
  }
}, 0.5);
```

---

## 5. PIP auto-detect pattern

```js
/**
 * Phân tích Whisper transcript để quyết định phase nào cần PIP
 * @param {Array} segments - Whisper segments
 * @param {Object} phases - {phaseName: [start, end]}
 * @returns {Object} {phaseName: needsPIP}
 */
function detectPIPPhases(segments, phases) {
  const SPECS_REGEX = /\d+\s*(g|kg|w|pa|hz|inch|cm|mm|ml|%|x|lần|giờ|phút|inch|"|\')/gi;
  const result = {};
  
  for (const [phaseName, [start, end]] of Object.entries(phases)) {
    const phaseText = segments
      .filter(s => s.start >= start && s.end <= end)
      .map(s => s.text)
      .join(' ');
    
    const specsCount = (phaseText.match(SPECS_REGEX) || []).length;
    result[phaseName] = specsCount >= 2;
  }
  
  return result;
}

// Usage:
const phases = {
  HOOK: [0, 7],
  PROBLEM: [7, 15],
  SPECS: [24, 37],
  USP: [37, 52],
};
const pipNeeded = detectPIPPhases(whisperSegments, phases);
console.log('SPECS phase needs PIP:', pipNeeded.SPECS);  // true
```

---

## 6. HTML template cho mỗi phase (V7 standard)

```html
<!-- HOOK phase (0-7s) -->
<div class="phase-glass glass-hook" data-class="glass-hook">
  <div class="text-line eyebrow">⚡ Bạn nào đang tìm...</div>
  <div class="text-line title">Máy hút bụi cầm tay?</div>
  <div class="text-line subtitle">Hút góc phòng - hút ô tô - hút nhanh</div>
</div>

<!-- PROBLEM phase (7-15s) -->
<div class="phase-glass glass-problem" data-class="glass-problem">
  <div class="text-line problem-row">
    <span class="problem-num">01</span>
    <span class="problem-text">Bụi góc phòng khó vệ sinh</span>
  </div>
  <div class="text-line problem-row">
    <span class="problem-num">02</span>
    <span class="problem-text">Bụi ô tô - ghế ô tô</span>
  </div>
  <div class="text-line problem-row">
    <span class="problem-num">03</span>
    <span class="problem-text">Bụi bàn làm việc - góc nhỏ</span>
  </div>
</div>

<!-- INTRO phase (15-24s) -->
<div class="phase-glass glass-intro" data-class="glass-intro">
  <div class="text-line num-big">2 in 1</div>
  <div class="text-line title">Máy Hút VÀ Máy Thổi</div>
  <div class="text-line subtitle">⚡ Hộp đựng + nhiều đầu hút/thổi tặng kèm</div>
</div>

<!-- SPECS phase (24-37s) - CÓ PIP -->
<div class="phase-crop">
  <div class="pip-wrap" data-class="pip-specs">
    <video id="pip-specs" data-start="24" data-duration="13" muted playsinline preload="auto">
      <source src="assets/source/pip/specs.mp4" type="video/mp4" />
    </video>
  </div>
  <div class="phase-glass glass-specs" data-class="glass-specs">
    <div class="text-line num-big">25.000</div>
    <div class="text-line unit">Pa lực hút</div>
    <div class="text-line subtitle">⚡ Lực hút mạnh nhất trong máy cầm tay</div>
  </div>
</div>

<!-- CTA-FINAL phase (73-82s) - 80% khung hình -->
<div class="phase-glass glass-cta-big" data-class="glass-cta-big">
  <div class="text-line eyebrow">⚡ BẤM NGAY</div>
  <div class="text-line title">Anh bấm link phía dưới để mua nhé</div>
  <div class="text-line cta-big-spec">⚡ 25.000 Pa + 140W + 24 tháng bảo hành + 1 đổi 1</div>
  <div class="text-line cta-big-spec">⚡ 400g nhẹ - 2 in 1 hút + thổi</div>
  <div class="text-line cta-big-spec">⚡ Hộp đựng + nhiều đầu hút/thổi tặng kèm</div>
  <div class="text-line price-big">495K</div>
  <div class="text-line eyebrow">⚡ HÀNG CHÍNH HÃNG SHOP DODOTO</div>
</div>
```

---

## 7. CSS class names (chuẩn V7 - dùng nhất quán)

| Class | Dùng cho |
|---|---|
| `.text-line` | Bắt buộc cho MỌI dòng text cần stagger reveal |
| `.eyebrow` | Text phụ (màu gold, font 36px) |
| `.title` | Title chính (font 64px, weight 900) |
| `.subtitle` | Subtitle (font 40px) |
| `.num-big` | Số lớn cần CountUp (font 128px) |
| `.price-big` | Giá (font 160px) |
| `.cta-big-spec` | Spec trong CTA-FINAL (font 36px) |
| `.problem-num` | Số thứ tự 01/02/03 (font 40px, color gold) |
| `.problem-text` | Text trong problem row (font 26px) |
| `.phase-glass` | Glass card chung (áp dụng V7) |
| `.phase-crop` | Container cho phase có PIP |
| `.pip-wrap` | PIP video element wrapper |

---

## 8. Layout positions (V7 verified)

| Phase | Element | Top | Size |
|---|---|---|---|
| HOOK | glass-hook | 1308px | full-width |
| PROBLEM | glass-problem | 1288px | full-width |
| INTRO | glass-intro | 1308px | full-width |
| CHART | pip-wrap | 80px | 420×420 |
| CHART | glass-chart | 720px | full-width |
| PORT | pip-wrap | 80px | 420×420 |
| PORT | glass-port | 680px | full-width |
| USP | glass-usp | 1308px | full-width |
| USE-CASE | glass-usecase | 1308px | full-width |
| CTA-TEST | glass-cta | 1308px | full-width |
| CTA-FINAL | glass-cta-big | 192px + bottom 192px | 80% khung hình |

---

## 9. Verify checklist V7

```bash
# 1. Render silent với format mov
cd /tmp/hf_v*
npx --yes hyperframes render --quality draft --format mov --output output_silent.mov

# 2. Ghép source video + overlay với alpha
ffmpeg -y -i source.mp4 -i output_silent.mov \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS-STARTPTS[bg]; [1:v]scale=1080:1920,format=yuva420p,setpts=PTS-STARTPTS[v1]; [bg][v1]overlay=0:0:eof_action=pass[v]" \
  -map "[v]" -map 0:a -c:v libx264 -preset fast -crf 23 -c:a copy -shortest \
  output_FINAL.mp4

# 3. Verify motion ở 4 VÙNG (KHÔNG chỉ top)
python3 verify_motion_4regions.py output_FINAL.mp4

# 4. Verify glass card visible
python3 verify_glass_visibility.py output_FINAL.mp4

# 5. Verify text motion stagger
python3 verify_text_stagger.py output_FINAL.mp4
```

---

## 10. Lỗi thường gặp + cách fix

| Lỗi | Nguyên nhân | Fix |
|---|---|---|
| Glass card quá đục (mờ tịt, che talking head) | Opacity > 0.22 (override quá đà) | Hạ xuống **0.18** (DEFAULT 18/07/2026) |
| Glass card quá trong suốt (mất chữ) | Opacity < 0.15 | Tăng lên **0.18** (DEFAULT) — không bao giờ < 0.15 |
| Glass card không mờ nhám | blur(40px) | Tăng lên **blur(48px) saturate(200%)** |
| Title quá nhỏ | font 48px | Tăng lên **64-72px** |
| Text hiện cùng lúc | Chỉ motion cả card | Thêm **staggerText()** với clipPath |
| Không có PIP khi nhiều data | Quên check transcript specs | Chạy **detectPIPPhases()** |
| Background video bị đơ | HTML video element | `background: transparent` + `display: none` |
| Motion chỉ ở vùng glass | GSAP animate | Verify ở **4 vùng khác nhau** |

> **Lưu ý (18/07/2026):** DEFAULT opacity = **0.18** (supersedes V22 verified 0.15). Override allowed per-clip nếu context yêu cầu (chart phase đục hơn 0.22, CTA mỏng hơn 0.15). Xem SKILL.md section `## 🔴 PIP CROPPING PATTERN FOR TIKTOK VERTICAL (added 2026-07-18, FIRST-CLASS)` → `### 8 DEFAULT VALUES (liquid glass + typography)` table.

---

## Reference

- SKILL.md `tiktok-product-motion-graphics` - Main umbrella skill
- `clip-0003-v5-final-fix-transparent-overlay-2026-07-18.md` - V5 motion fix
- `clip-0003-v3-speed13-case-study-2026-07-18.md` - 18/07 V3 source STATIC
- `verify-frame-checklist.md` - Phase-by-phase verify questions