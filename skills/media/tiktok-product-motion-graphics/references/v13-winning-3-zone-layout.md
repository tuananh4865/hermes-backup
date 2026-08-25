# V13 Winning Layout — 3-Zone + 2-Column Crop

**Status:** VERIFIED PASS via `vision_analyze` on 17/07/2026 (after V1-V12 all failed)
**Source clip:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac-du-phong-mini-gan-iphone-04072026-v5.mp4` (32s, 1728×3072)
**Output:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v13_32s_with_audio.mp4` (13.0 MB)

## TL;DR — The Working Coordinates

```css
/* ZONE 1: TOP glass (Y = 80-460 px) */
.glass.p-top { top: 300px; left: 56px; right: 56px; padding: 24px 28px; }

/* ZONE 2: MIDDLE (Y = 540-1280) — MẶT ANH, KHÔNG BAO GIỜ có text khi video full-frame */

/* ZONE 3: BOTTOM glass (Y = 1320-1380 px, chỉ cao 60px hẹp) */
.glass.p-bottom { top: 1320px; left: 56px; right: 56px; padding: 14px 24px; }

/* Crop phase: PIP trái + Glass phải (2-column, tận dụng full width) */
.pip-wrap { top: 560px; left: 60px; width: 320px; height: 320px; }
.glass.crop-right  { top: 560px; left: 420px; right: 56px; }
.glass.crop-bottom { top: 1320px; left: 56px; right: 56px; }
```

## The 4 Hard Rules (verified V13 success)

1. **Padding = 56px both sides** (matches TikTok LEFT/RIGHT UI zones, NEVER overflow 1080px)
2. **Text only in Y < 460 OR Y > 1317** when no PIP (face zone Y=540-1280 is FORBIDDEN)
3. **Crop phase = 2-column song song** (PIP trái + Glass phải), NOT stacked or single-column
4. **Black bg fade for crop phases** (Pitfall 11 from V5) — `black-bg` opacity 0→1→0 đồng bộ với PIP

## 8-Phase Layout (V13 actual implementation)

| # | Phase | BG | Layout (V13) | Verified frame |
|---|---|---|---|---|
| 1 | HOOK | Video full | TOP glass "ĐỜI MỚI + Sạc iPhone không dây" + BOTTOM stats (80g/⚡/5K) | ✅ frame 2s |
| 2 | PROBLEM | Video full | TOP glass "Thời đại 2026" + BOTTOM 3 rows (01/02/03 nhỏ gọn) | ✅ frame 6s |
| 3 | CHART | ⚫ BLACK | PIP trái (320×320) + glass RIGHT (So sánh 500g vs 80g) + stats BOTTOM | ✅ frame 10s |
| 4 | STAMP | Video full | ☕ emoji TOP-center + glass BOTTOM "NẶNG!" | ✅ frame 16s |
| 5 | PRODUCT | Video full | TOP glass "Gochodoc pill + Củ sạc mini gắn iPhone" + BOTTOM tagline | ✅ frame 18s |
| 6 | PORT | ⚫ BLACK | PIP trái + glass RIGHT (🔌→📱→🔋 flow) + tag BOTTOM | ✅ frame 20s |
| 7 | USP | Video full | TOP glass "Tại sao chọn củ sạc này?" + BOTTOM 4 cards 2x2 grid | ✅ frame 28s |
| 8 | CTA | Video full | TOP glass "Sẵn sàng nhẹ hơn?" + BOTTOM MUA NGAY + price 499K | ✅ frame 30s |

## Why V13 Won (vs V1-V12 failures)

| Attempt | Major failure | V13 fix |
|---|---|---|
| V1-V3 | 3 elements only, dark gradient bg, no audio, no real PIP | 8+ visual elements, video full-frame + real PIP |
| V4 | PIP background = video gốc (rối mắt) | Black bg fade for crop phases |
| V5 | Layout: glass ở giữa cạnh PIP (nửa dưới trống) | 2-column song song (PIP + glass cạnh nhau) |
| V6 | Glass dưới che cằm anh (bottom:240px) | Glass BOTTOM exact top:1320px |
| V7 | face-protect gradient tạo "điểm đen" lớn trước mặt | BỎ HOÀN TOÀN — chỉ dùng backdrop-filter trong glass |
| V8 | Animation timing overlap (phase A chưa fade out khi phase B fade in) | Buffer 0.3s, verify visually |
| V9 | Glass BOTTOM che cằm + CSS translateY(-50%) không predict | Explicit top:1320, no translate center |
| V10 | 3-zone layout nhưng glass ở Y=1280+ đè TikTok UI | Glass BOTTOM top:1320 (TikTok-safe) |
| V11 | Padding overflow 1080px frame | Padding 56px both sides |
| V12 | Sub-composition wiring fail (chart phase MÀN HÌNH ĐEN) | Single index.html + flat GSAP timeline |
| **V13** | **PASS** | Single file, 3-zone + 2-column, verified by vision | ✅ |

## Reusable Detection Pipeline (run BEFORE writing layout)

```bash
DETECT=/tmp/aw3_video/detect_face

for sec in 0 4 8 12 16 20 24 28 32; do
  ffmpeg -y -ss $sec -i source.mp4 -frames:v 1 -vf "scale=864:1536" /tmp/fd_t${sec}.jpg
  $DETECT /tmp/fd_t${sec}.jpg
done
```

Output: `FACE x y w h` normalized 0-1, **y=0 is bottom (Vision framework convention)**.

Convert to 1080×1920 pixel coordinates:
```python
# Vision y=0 is bottom, y=1 is top
y_top_normalized = 1.0 - y - h
x_px = x * 1920  # or whatever your scaled width
y_px = y_top_normalized * 1080  # or scaled height
w_px = w * 1920 * 1.4  # 40% padding
h_px = h * 1080 * 1.4
```

Face bbox format for Pocket3 32s clip (validated):
```
t= 0s: face center Y=636-1145 in source 1728×3072 → Y=890-1257 in scaled 1080×1920 (off-center start)
t= 4s: Y=644-1251 → Y=900-1306
t= 8s: Y=577-1099 → Y=861-1231
t=12s: Y=552-1095 → Y=850-1230
t=16s: Y=654-1175 → Y=905-1280
t=20s: Y=625-1175 → Y=890-1280
t=24s: Y=614-1144 → Y=884-1268
t=28s: Y=625-1083 → Y=890-1257
t=32s: Y=612-1054 → Y=883-1238
```

**Universal face zone for this clip type: Y=850-1280 in 1080×1920** = use as starting coordinate.

## Animation Timing Buffer Rule (V13 safe)

Every phase transition uses 0.3s buffer between fade-out and fade-in:

```javascript
// Phase A fade out (T_A)
tl.to([phaseA, blackBgA, pipA], { opacity: 0, duration: 0.4 }, T_A);

// Buffer 0.3s — phase A opacity must reach 0 before phase B starts
// Phase B fade in (T_B ≥ T_A + 0.7s)
tl.to(blackBg, { opacity: 1, duration: 0.4 }, T_B);  // for crop phases
tl.fromTo(phaseB, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, T_B + 0.1);
```

**Verify:** `vision_analyze frame T_A + 0.3s` — both phase A and phase B should be opacity 0 (transition moment). If either shows content, buffer too short.

## Reusable Glass Card CSS (V13 - frosted white iOS 26)

```css
.glass {
  position: absolute;
  z-index: 20;
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border: 1.5px solid rgba(255, 255, 255, 0.4);
  border-radius: 28px;
  padding: 24px 28px;
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  position: relative;
  overflow: hidden;
}

/* iOS 26 signature corner shine */
.glass::before {
  content: "";
  position: absolute;
  inset: 0;
  border-radius: inherit;
  background:
    radial-gradient(circle at 15% 0%, rgba(255, 255, 255, 0.5), transparent 45%),
    radial-gradient(circle at 100% 100%, rgba(255, 255, 255, 0.25), transparent 35%);
  pointer-events: none;
}

.glass > * { position: relative; }  /* bring text above ::before */
```

For glass cards with DARK text (chart axes, product specs):
```css
.chart-glass {
  background: rgba(255, 255, 255, 0.22);  /* slightly brighter for contrast */
  color: #1a1a1a;
}
```

## When This Layout Breaks (and how to adapt)

| New source type | Adaptation |
|---|---|
| Wider face (face fills more screen) | Reduce PIP size to 280×280, move glass BOTTOM up to top:1360 |
| Different aspect ratio (16:9) | Recalculate 3 zones: TOP_Y = height × 0.15, BOTTOM_Y = height × 0.72 |
| Person moving more (e.g. walking) | Re-run face detection every 2s, take MAX bbox, use that for zones |
| Multiple speakers | Detect each person's bbox, use UNION as forbidden zone |

## Visual Verify Workflow (MANDATORY before ship)

```bash
# 1. Render silent via HyperFrames
npx --yes hyperframes render --quality draft --output output_silent.mp4

# 2. Extract frames at 1 frame per 2 seconds
ffmpeg -y -i output_silent.mp4 -vf "fps=1/2" -q:v 2 v13_%02d.jpg

# 3. MANDATORY vision_analyze on EVERY frame with phase-specific question
# Use these exact questions:
```

**Phase-specific vision_analyze questions:**

- **HOOK (frame 2s):** "Glass TOP có 'ĐỜI MỚI + title'? Glass BOTTOM có 3 stats (80g/⚡/5K)? Mặt anh ở giữa có bị che không? Padding có lọt ra ngoài khung 1080px không?"
- **PROBLEM (frame 6s):** "Glass TOP 'Thời đại 2026' + Glass BOTTOM 3 items? Mặt anh có bị che không?"
- **CHART (frame 10s):** "BLACK bg + PIP trái (X=60-380) + chart glass phải (X=420-1024)? Mặt anh trong PIP đầy đủ? Phần đen ở giữa có trống không?"
- **PORT (frame 20s):** "BLACK bg + PIP trái + port flow phải?"
- **USP (frame 28s):** "USP grid 4 cards + title?"
- **CTA (frame 30s):** "CTA button + price? Có chồng chữ không?"

If **ANY** frame fails the visual check → fix timeline and re-render. Do NOT ship until ALL frames pass.

## Reference: Full V13 file structure

```
/tmp/hf_sacduphong_v13/
├── index.html              (309 lines, 0 lint errors, single file)
├── output_silent.mp4       (HyperFrames render silent)
├── output/
│   └── sac_du_phong_v13_32s_with_audio.mp4  (ffmpeg audio mux)
└── assets/source/
    ├── full_bg.mp4         (1080×1920 scaled source)
    └── pip/
        ├── chart.mp4       (face-aware crop 7.5-13.5s)
        └── port.mp4        (face-aware crop 19-28s)
```

## Timeline gotchas (V13 specific)

```javascript
// IMPORTANT: scope GSAP selectors to current composition
tl.fromTo("[data-composition-id='sac-du-phong-v13'] [data-class='hook-top'] .title",
  { clipPath: "inset(0 100% 0 0)" },
  { clipPath: "inset(0 0% 0 0)", duration: 0.7 }, 0.5);
```

**Why:** HyperFrames bundles all compositions into one page → unscoped selectors like `.title` would target all compositions' titles. Always use full attribute selector chain.
