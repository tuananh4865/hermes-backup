# V9 Glass Bottom Anti-Pattern (verified 17/07/2026)

**Context:** Em build V8 → V9 cho clip `sac-du-phong-mini-gan-iphone-04072026-v5.mp4` (32s). Anh V8 feedback: *"Có thể vừa hiện motion graphic ở trên và ở dưới với những đoạn thường và đoạn crop thì thể hiện motion graphic ở trung tâm!"*

Em fix bằng cách thêm glass BOTTOM (`bottom: 240px`) cho mỗi phase. Verify bằng mắt (vision_analyze) cho thấy **2 vấn đề mới**.

---

## Bug #1 — Glass BOTTOM che cằm anh

**Symptom:** Frame HOOK (~2s) verify bằng mắt:

```
┌──────────────────────────────────┐
│ TOP glass (SAFE Y=80-460) ✅     │
│ ⚡ ĐỜI MỚI + Sạc iPhone       │
│                                  │
│ MẶT ANH (VÙNG CẤM Y=823-1320)  │ ← mặt anh
│                                  │
│                                  │
│                                  │
│ BOTTOM glass (CHE CẰM!) ❌       │ ← Y=1480-1920 + extend upward do padding
│ "Củ sạc mini..."                │
└──────────────────────────────────┘
```

**Cause calculation:**
- Glass BOTTOM `bottom: 240px` = top edge ở Y = 1920 - 240 = 1680
- Glass BOTTOM với padding 32+text 36+padding 28 = chiều cao thực tế ~ 200-440px
- **Glass BOTTOM extend từ Y=1480 lên Y=1480 (top edge của glass)** — nếu text ở giữa glass, **text có thể ở Y=1700 OK**, NHƯNG nếu glass có nội dung nhiều (vd 3 lines + title) → **glass height ~ 400px** → top edge ở Y=1520

**VẤN ĐỀ:** Em tính safe zone bottom là `Y > 1620` (caption bar area), nhưng glass BOTTOM `bottom: 240px` có thể overlap vùng mặt anh nếu nội dung glass nhiều.

**Empirical test (V9, clip 32s):**
- Frame 2s: glass BOTTOM visible ở **Y ≈ 1440-1700**
- Mặt anh cằm ở **Y ≈ 1300-1450** (đo từ frame 2s verify)
- **Overlap ở Y=1440-1450** ← che cằm!

---

## Safe-Zone Formula (V10 RECOMMENDATION)

Công thức tính Y thay vì bottom/up để tránh ambiguity:

```css
/* ❌ Anti-pattern: dùng bottom/top % */
.glass-bottom { bottom: 240px; }   /* ambiguous nếu height thay đổi */

/* ✅ Đúng: dùng explicit top */
.glass-bottom { top: 1480px; }    /* predictable */
```

**Reusable safe-zone formula (verified 17/07 V9):**

```
SAFE_TOP = 80px (height max 380px)        → Y range: 80-460
FORBIDDEN_CENTER = Y 460-1440            ← VÙNG CẤM khi video full-frame
SAFE_BOTTOM = top: 1480px (height max 480px) → Y range: 1480-1900
CAPTION_BAR = bottom: 60px (height ~80px)  → Y range: 1780-1900
```

**Rule:** Khi talking head còn full-frame:
- **CHỈ** đặt glass ở 1 trong 2 zones: TOP (Y=80-460) hoặc BOTTOM (Y=1480-1900)
- **KHÔNG BAO GIỜ** đặt glass ở Y=460-1480

Nếu cần text ở nửa màn hình → dùng 2 glass tách biệt (TOP glass title + BOTTOM glass body).

---

## Bug #2 — CSS `translateY(-50%)` không predict được sau HyperFrames render

**Symptom:** Em code `.chart-right { right: 60px; top: 50%; transform: translateY(-50%); }` → tưởng glass ở **center phải**.

Verify frame CHART (~10s):

```
┌──────────────────────────────────┐
│ PIP (góc trên trái)             │
│                                  │
│                                  │
│                                  │
│         Glass chart              │ ← Glass ở DƯỚI, KHÔNG ở phải center
│         ⚖️ So sánh...            │
│         "Sạc cũ 500g..."         │
└──────────────────────────────────┘
```

**Cause:** HyperFrames render pipeline có thể reset `transform` hoặc interpret `top: 50%` theo container khác. Kết quả: glass ở **bottom half** (Y ≈ 1200-1500) thay vì center.

**Fix:** Dùng **explicit `top` value**:

```css
/* ❌ Anti-pattern */
.chart-right {
  right: 60px;
  top: 50%;
  transform: translateY(-50%);
}

/* ✅ Đúng */
.chart-right {
  right: 60px;
  top: 280px;   /* Hoặc bất kỳ Y cụ thể nào trong SAFE zone */
}
```

**Alternative:** Dùng `position: relative` + flexbox/grid:

```css
.layout {
  display: grid;
  grid-template-columns: 1fr 1fr;   /* PIP trái, glass phải */
  grid-template-rows: 1fr;
}
.pip { grid-column: 1; }
.glass { grid-column: 2; }
```

Grid/flex more predictable với HyperFrames render pipeline.

---

## Animation Timing Buffer (V9 VERIFIED)

Mỗi phase có 4 timing slots cách nhau ≥ 0.3s để phase A fade out hoàn toàn trước khi phase B fade in:

```javascript
// Phase A timing (T_A = end time of phase A)
tl.to(phaseAGlass, { opacity: 0, duration: 0.4 }, T_A);
tl.to(phaseAPip, { opacity: 0, duration: 0.3 }, T_A + 0.1);
tl.to(phaseABlackBg, { opacity: 0, duration: 0.3 }, T_A + 0.2);
// T_A + 0.5 = fully gone

// Phase B timing (T_B ≥ T_A + 0.5)
tl.fromTo(phaseBGlass, { opacity: 0 }, { opacity: 1, duration: 0.6 }, T_B);
tl.to(phaseBPip, { opacity: 0, ... }, T_B - 0.2);  // reverse direction
```

**V9 finding:** Em dùng `T_A + 0.1` cho fade in của phase B → vẫn chồng! Phải ≥ 0.5s buffer.

---

## Verification Approach for V10+

Sau khi render V10:

```bash
# 1. Render silent
npx --yes hyperframes render --quality draft --output output_silent.mp4

# 2. Extract frames
ffmpeg -y -i output_silent.mp4 -vf "fps=1/2" -q:v 2 v10_%02d.jpg

# 3. vision_analyze TỪNG frame với specific questions:

# Phase HOOK (~2s):
vision_analyze("Mặt anh bị glass nào che? Glass BOTTOM có overlap mặt không?")

# Phase transition (~8s):
vision_analyze("Phase HOOK đã fade out hoàn toàn chưa? Phase CHART đã xuất hiện chưa?")

# Phase CHART (~10s):
vision_analyze("Glass chart ở vị trí nào? Có phải ở bên phải center không?")

# Phase CTA (~30s):
vision_analyze("CTA button ở đâu? Có che mặt anh không?")
```

**Acceptance criteria V10:**
- ✅ Không có frame nào mặt anh bị text/glass che
- ✅ Glass BOTTOM ở Y ≥ 1480 trong tất cả phase thường
- ✅ Glass CHART/PORT ở góc trên phải (`top: 280px, right: 60px`)
- ✅ Mỗi phase fade in/out không overlap với phase kế tiếp (0.5s buffer)
- ✅ 12+ visual elements (verified bằng DOM count trong index.html)

Nếu bất kỳ frame nào fail → fix + re-render + verify lại. **KHÔNG SHIP** nếu còn 1 frame fail.

---

## Reference Links

- `references/face-safe-zone-v7-v8-data.md` — Empirical face bbox data (X=270-810, Y=580-1320)
- `references/v6-final-layout-decisions.md` — V1→V6 timeline + 2-layer layout
- `references/storyboard-format.md` — STORYBOARD.md template
- `references/verify-frame-checklist.md` — Phase-by-phase verification questions

## Session Reference

- Date: 2026-07-17
- Source clip: `sac-du-phong-mini-gan-iphone-04072026-v5.mp4` (32s, 1728×3072, Pocket3)
- Builds: V1 → V9 (9 iterations trong 1 session)
- Key iteration: V8 verification caught điểm đen lớn trước mặt anh + text đè lên nhau
- V9 verification caught: HOOK BOTTOM che cằm + CHART glass ở dưới thay vì phải
