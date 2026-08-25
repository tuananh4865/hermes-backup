# V22 8-Phase Pattern Template — Verified Motion Graphics

> **Status:** Verified PASS 18/07/2026 on clip_0003 V79 (20.4 MB, motion 33%/phase, 65s)
> **Source of truth:** `/tmp/hf_sacduphong_v22/index.html` (shipped V22 sac-du-phong, 12.3 MB, approved)
> **Anti-pattern source:** V72/V75/V78 all failed because they built without reading V22 final HTML first.

## When to use this template

ANY TikTok product review motion graphic 1080×1920 dọc, 30-90s duration. The 8-phase structure is the signature V22 pattern anh đã approved — don't deviate without explicit reason.

## The 8 Phases (canonical mapping)

| # | Phase | Time | Glass position | Nội dung | BG layer |
|---|---|---|---|---|---|
| 1 | HOOK | 0-3s | top 1308 + pill | Title + eyebrow pill | Video bg |
| 2 | PROBLEM | 3-7s | top 1288 | 3-5 pain points + underline | Video bg |
| 3 | **CHART** | 7-13s | top 720 (ngang hàng PIP top-left 80,80) | 4 chart bars animate stagger | **NỀN ĐEN** |
| 4 | STAMP | 13-16s | center | "CHÍNH HÃNG" stamp flash | Video bg |
| 5 | PRODUCT | 16-19s | top 1288 | Tên sản phẩm + brand | Video bg |
| 6 | **PORT** | 19-27s | top 720 (ngang hàng PIP) | 3-5 step flow | **NỀN ĐEN** |
| 7 | USP | 27-32s | top 1308 | 4 specs grid 2x2 | Video bg |
| 8 | **CTA-FINAL** | 32-end | **80% khung hình** (10% margin) | Giá + specs + BH info | Liquid glass full |

**Mandatory phases** (never skip): HOOK, PROBLEM, CTA-FINAL  
**Skippable phases** (only if content doesn't fit): STAMP, PORT  
**Conditional phases** (only if data exists): CHART, USP

## CSS Recipe (V22 verified)

```css
/* Black-bg overlay — REQUIRED for CHART + PORT phases */
#black-bg {
  position: absolute; inset: 0;
  background: #000;
  z-index: 1; opacity: 0;
}

/* Glass card — V22 base recipe (opacity 0.15 + blur 40px + border 0.4) */
.glass-card {
  background: rgba(255, 255, 255, 0.15);
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border: 1.5px solid rgba(255, 255, 255, 0.4);
  border-radius: 36px;
  padding: 40px 36px;
  box-shadow: 0 20px 56px rgba(0, 0, 0, 0.5);
  z-index: 5; opacity: 0;
}

/* Glass positions — nửa dưới (HOOK/PROBLEM/PRODUCT/USP) */
.hook-glass, .problem-glass, .product-glass, .usp-glass {
  top: 1288px; left: 60px; right: 60px;
}

/* Glass positions — ngang hàng PIP top-left (CHART/PORT) */
.chart-glass, .port-glass {
  top: 720px; left: 530px; max-width: 470px;
}

/* CTA-FINAL 80% — full screen liquid glass */
.cta-glass {
  position: absolute;
  top: 10%; left: 10%; right: 10%; bottom: 10%;
  width: 80%; height: 80%;
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(40px) saturate(180%);
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 48px;
  z-index: 20; opacity: 0;
}

/* PIP container — vuông 420×420, top-left */
.pip {
  position: absolute;
  top: 80px; left: 80px;
  width: 420px; height: 420px;
  border-radius: 24px; overflow: hidden;
  z-index: 3; opacity: 0;
  background: #000;
}
```

## Timeline Script (V22 verified — copy-paste skeleton)

```js
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
window.__timelines["<clip-id>"] = tl;

const root = document.querySelector('[data-composition-id="<clip-id>"]');
const videos = root.querySelectorAll('video');
videos.forEach(v => v.pause());  // ← KEY: pause only, NO currentTime = 0

// ===== PHASE 1: HOOK (0-3s) =====
tl.fromTo('#hook-pill', { opacity: 0, scale: 0.8 }, { opacity: 1, scale: 1, duration: 0.4, ease: 'back.out(1.5)' }, 0.3);
tl.fromTo('#hook-glass', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: 'power2.out' }, 0.4);
tl.to('#hook-pill', { opacity: 0, duration: 0.3 }, 2.9);
tl.to('#hook-glass', { opacity: 0, duration: 0.4 }, 2.9);

// ===== PHASE 2: PROBLEM (3-7s) =====
tl.fromTo('#problem-glass', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.5 }, 3.2);
// animate problem-row 1/2/3 + underline stagger
tl.to('#problem-glass', { opacity: 0, duration: 0.4 }, 6.8);

// ===== PHASE 3: CHART (7-13s) — PIP + nền đen =====
tl.to('#black-bg', { opacity: 1, duration: 0.4 }, 7.2);
tl.fromTo('#pip-chart', { opacity: 0, scale: 0.85, x: -60 }, { opacity: 1, scale: 1, x: 0, duration: 0.6, ease: 'back.out(1.5)' }, 7.4);
tl.fromTo('#chart-glass', { opacity: 0, y: 60, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: 'back.out(1.2)' }, 7.6);
// animate chart bars stagger (each +1s)
tl.to('#bar-good', { width: '100%', duration: 2.5, ease: 'power1.inOut' }, 8.2);
tl.to('#bar-bad-1', { width: '68%', duration: 2.5, ease: 'power1.inOut' }, 9.2);
// ...
tl.to('#chart-glass', { opacity: 0, duration: 0.4 }, 12.8);
tl.to('#pip-chart', { opacity: 0, duration: 0.3 }, 12.9);
tl.to('#black-bg', { opacity: 0, duration: 0.3 }, 13.0);  // tắt nền đen

// ===== PHASE 4: STAMP (13-16s) =====
tl.fromTo('#stamp-glass', { opacity: 0, scale: 1.8, rotation: 10 }, { opacity: 1, scale: 1, rotation: -8, duration: 0.5, ease: 'back.out(1.5)' }, 13.2);
tl.to('#stamp-glass', { scale: 1.1, duration: 0.15, yoyo: true, repeat: 1 }, 14.0);
tl.to('#stamp-glass', { opacity: 0, scale: 0.7, duration: 0.3 }, 16.0);

// ===== PHASE 5: PRODUCT (16-19s) =====
tl.fromTo('#product-glass', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: 'back.out(1.2)' }, 16.5);
tl.to('#product-glass', { opacity: 0, duration: 0.4 }, 18.5);

// ===== PHASE 6: PORT (19-27s) — PIP + nền đen + 3 step flow =====
tl.to('#black-bg', { opacity: 1, duration: 0.4 }, 18.8);
tl.fromTo('#pip-port', { opacity: 0, scale: 0.85, x: -60 }, { opacity: 1, scale: 1, x: 0, duration: 0.6, ease: 'back.out(1.5)' }, 19.0);
tl.fromTo('#port-glass', { opacity: 0, y: 60, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.6, ease: 'back.out(1.2)' }, 19.2);
// animate port-step 1→arrow→step 2→arrow→step 3 stagger
// subtle PIP rotation (3 steps, -2° → +2° → 0°)
tl.to('#pip-port', { rotation: -2, duration: 0.3 }, 23.0);
tl.to('#pip-port', { rotation: 2, duration: 0.3 }, 23.5);
tl.to('#pip-port', { rotation: 0, duration: 0.3 }, 24.0);
tl.to('#port-glass', { opacity: 0, duration: 0.4 }, 27.0);
tl.to('#pip-port', { opacity: 0, duration: 0.3 }, 27.1);
tl.to('#black-bg', { opacity: 0, duration: 0.3 }, 27.2);

// ===== PHASE 7: USP (27-32s) =====
tl.fromTo('#usp-glass', { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.6, ease: 'back.out(1.2)' }, 27.5);
// animate 4 usp items stagger +0.4s each
tl.to('#usp-glass', { opacity: 0, duration: 0.4 }, 32.0);

// ===== PHASE 8: CTA-FINAL (32-end) — liquid glass 80% =====
tl.fromTo('#cta-glass', { opacity: 0, y: 80, scale: 0.95 }, { opacity: 1, y: 0, scale: 1, duration: 0.7, ease: 'back.out(1.2)' }, 32.5);
// CTA giữ visible đến cuối clip — KHÔNG animate opacity 0
```

## HTML Structure Template

```html
<div id="root" data-composition-id="<clip-id>"
     data-start="0" data-duration="<total-seconds>"
     data-width="1080" data-height="1920">

  <video id="video-bg" class="video-bg"
         data-start="0" data-duration="<total-seconds>" data-track-index="0"
         src="assets/source/full_bg.mp4"
         muted playsinline preload="auto"></video>

  <div id="black-bg" class="black-bg"></div>

  <!-- PIP videos — MỖI video PHẢI có id (HyperFrames renderer requirement) -->
  <div class="pip" id="pip-chart">
    <video id="video-pip-chart" data-start="<chart-ss>" data-duration="<chart-dur>" data-track-index="1"
           src="assets/source/pip/pip_chart.mp4"
           muted playsinline preload="auto"></video>
  </div>

  <div class="pip" id="pip-port">
    <video id="video-pip-port" data-start="<port-ss>" data-duration="<port-dur>" data-track-index="2"
           src="assets/source/pip/pip_port.mp4"
           muted playsinline preload="auto"></video>
  </div>

  <!-- 8 phase glass cards ở đây (copy từ V79 working HTML) -->
</div>
```

## Workflow 6 bước (V79 đã verify)

1. **Copy source gốc** (KHÔNG speed 1.3x) → `assets/source/full_bg.mp4`
   ```bash
   ffmpeg -y -i source_goc.mp4 -an -c:v copy assets/source/full_bg.mp4
   ```
2. **Extract 2 PIP** (chart + port) crop vuông 1080×1080 từ Y=540 + scale 420×420
   ```bash
   for label, ss, dur in [("pip_chart", 15, 9), ("pip_port", 34, 16)]:
     ffmpeg -y -ss $ss -i source_goc.mp4 -t $dur \
       -vf "crop=1080:1080:0:540,scale=420:420" \
       -an -c:v libx264 -preset fast -crf 23 \
       assets/source/pip/$label.mp4
   ```
3. **HTML 8 phases** theo skeleton ở trên
4. **Black-bg overlay** bật/tắt trong timeline (CHART + PORT phases)
5. **CTA-FINAL 80%** ở 32s+ với giá + specs + BH info
6. **Render silent + ghép audio cuối**
   ```bash
   npx hyperframes render --quality draft --output output_silent.mp4
   ffmpeg -i output_silent.mp4 -i audio.aac -c:v copy -c:a aac -shortest FINAL.mp4
   ```

## Verification Checklist (trước khi ship)

| Check | Expected | How to verify |
|---|---|---|
| Motion @ 7 transitions | ≥30% pixels changed | `motion_diff_check.py --t1 <a> --t2 <b>` |
| Nền đen @ CHART (t=10s) | RGB (0,0,0) tại vùng PIP | `PIL.Image.getpixel()` at PIP center |
| CTA-FINAL @ t=55s | Liquid glass 80% present | Visual inspect frame extracted |
| Bit rate | ≥2.5 Mbps | `ffprobe -show_entries format=bit_rate` |
| File size | 15-25 MB cho 60-90s clip | `ls -la FINAL.mp4` |
| All 8 phases có glass content | Yes | Extract frames tại mỗi phase midpoint |

## Critical Anti-patterns (đã fail V72/V75/V78)

1. **❌ Build thiếu phase** — V78 chỉ 4 phases = clip thiếu info
2. **❌ Bỏ CTA-FINAL 80%** — signature quan trọng nhất của V22
3. **❌ Bỏ nền đen ở CHART/PORT** — PIP blend vào video bg, motion mờ
4. **❌ BG video ở phase CTA** — xung đột với liquid glass 80%
5. **❌ Build không đọc V22 final shipped HTML trước** — sai pattern → sai 3 lần liên tiếp

## See also

- `/tmp/hf_sacduphong_v22/index.html` — V22 final shipped HTML (31KB) — read this FIRST before any build
- `~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md` — main skill with V79 RECAP section
- `wiki/projects/tuan-anh-review-tiktok/layout-benchmark-vertical-tiktok-1080x1920.md` — 28KB layout spec

## Verification provenance

- **V22 PASS**: ship `sac_du_phong_v22_32s_with_audio.mp4` (12.3 MB, motion 33%/10s)
- **V79 PASS (clone V22 cho 0003)**: ship `clip0003_V79_65s_FINAL_with_audio.mp4` (20.4 MB, motion 32-33%/phase đồng đều 7 transitions, nền đen verified RGB (0,0,0))
- **V78 FAIL**: chỉ 4 phases, thiếu CTA-FINAL, BG video, không motion graphic → anh flag 18/07