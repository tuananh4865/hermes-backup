# V13→V16 Final Passing Layout — 17/07/2026

After 16 iterations on the same Pocket3 sac-du-phong clip (32s, source 1728×3072), **V16 finally passed `vision_analyze` verification on all 8 phases**. This document codifies the exact working layout — read before starting any Vietnamese talking-head + product motion graphics build.

## Final V16 file (verified PASS via vision_analyze)

**Source:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac-du-phong-mini-gan-iphone-04072026-v5.mp4`  
**Working files:** `/tmp/hf_sacduphong_v14/index.html` (cumulative patches V14 + V15 caption-bar fix + V16 port-flow de-clip + CTA timing)  
**Output:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v16_32s_with_audio.mp4` (12.9 MB, 1080×1920, H.264 + AAC 48000Hz stereo)

## 6 hard rules ANH established (after V11-V14 feedback)

### Rule 1: Padding chính xác trong khung 1080×1920

| Edge | Padding | Source |
|---|---|---|
| Left | 56px | TikTok safe zone (anh shared UI overlay image) |
| Right | 56px | 1080 − 120 (TikTok action buttons) = right edge at 1024 |
| Top | 300px (start) | TT_TOP 280 + 20 buffer |
| Bottom | 1340px (end) | TT_BOTTOM 1380 − 20 buffer |

**Glass max width = 1080 − 56 × 2 = 968px**

**Anh V14 verbatim:** *"Có nhiều padding lọt ra bên ngoài của khung hình, xác định rõ kích thước vùng an toàn để làm cho chính xác chứ."*

Anti-pattern: `left: 80px right: 80px` → content wider than 1024px, chữ bị clip ở mép phải.

### Rule 2: 3-zone safe layout (face avoidance + TikTok UI)

Empirical face bbox data (Vision framework `VNDetectFaceRectanglesRequest`, 16 samples mỗi 2s qua 32s):

| Time | Face center (X, Y) | Size (W×H) |
|---|---|---|
| 0s | (577, 890) | 508×508 |
| 4s | (598, 894) | 521×521 |
| 8s | (489, 838) | 522×522 |
| 12s | (547, 823) | 542×542 |
| 16s | (508, 913) | 521×521 |
| 20s | (597, 900) | 550×550 |
| 24s | (619, 878) | 530×530 |
| 28s | (350, 854) | 458×458 |

**Key insight:** Face ALWAYS at Y=823-913, size ~500-580px → **face zone = Y=540-1280 (mid 43%) is FORBIDDEN** when video full-frame (no PIP).

**Safe zones (V14 verified):**
- **TOP**: Y = 56-500 → text ở đây (eyebrow + title)
- **MIDDLE**: Y = 540-1280 → **MẶT ANH = NEVER TEXT** (unless PIP swap)
- **BOTTOM**: Y = 1317-1380 (63px hẹp) → caption/sub tag only

### Rule 3: CHÍNH/PHỤ visual hierarchy

**Anh V14 verbatim:** *"Các thành phần motion cũng vậy, cũng cần nhận biết cái nào chính cái nào phụ, mục chính thì cho xuất hiện ở trung tâm scale lớn hoặc ở khu vực trống không đè mặt còn cụm phụ thì xuất hiện ở rìa"*

**Implementation:**
- **MỤC CHÍNH**: scale LỚN (56pt+), ở **TRUNG TÂM phần trống** (Y=540-1280 mid-screen if PIP, or TOP Y=300-460 for video-full frames)
- **CỤM PHỤ**: ở **RÌA** (4 cạnh), text nhỏ 12-22pt, thống kê phụ trợ

| Phase | MỤC CHÍNH (scale lớn, trung tâm) | CỤM PHỤ (rìa, nhỏ) |
|---|---|---|
| HOOK | "Sạc iPhone không dây" 56pt TOP | 3 stats (80g/⚡/5K) 22pt BOTTOM |
| PROBLEM | "Thời đại 2026" 22pt TOP | 3 rows "01/02/03" 16pt BOTTOM |
| CHART (crop) | Chart glass RIGHT (X=420-1024) | PIP LEFT (X=56-376) + caption BOTTOM |
| PORT (crop) | Port flow glass RIGHT | PIP LEFT + caption BOTTOM |
| STAMP | ☕ emoji 100pt trung tâm | "NẶNG!" 50pt BOTTOM |
| PRODUCT | "Củ sạc mini gắn iPhone" 56pt TOP | "80 gram · Gắn vào cổng Lightning" 16pt BOTTOM |
| USP | "Tại sao chọn củ sạc này?" 32pt TOP | 4 cards 18pt BOTTOM |
| CTA | "Mua ngay" 28pt gold TOP | "499K" 20pt BOTTOM |

### Rule 4: 2-column layout cho phase crop (CHART/PORT)

**Layout 2-column verified V14-V16:**

- **PIP trái**: X=56-376 (width 320px), top: 540px, height: 320px → face full + "ANH ĐANG NÓI" red label dưới (Y=870-900)
- **Glass phải (CHÍNH)**: X=420-1024 (width 604px), top: 540px → chart/port flow scale lớn
- **Caption bar**: Y=1370 (BOTTOM rìa, ngắn 580px, KHÔNG che chart)
- **Black BG**: fade in/out đồng bộ với PIP

**Critical:** If chart/port glass content vượt quá 604px width → text bị clip. Fix V16: padding 24→20px, font-size 22pt→18pt, arrow 22pt→18pt cho port.

```css
.pip-wrap {
  top: 540px;
  left: 56px;
  width: 320px;
  height: 320px;
  border-radius: 24px;
  border: 3px solid rgba(255, 255, 255, 0.85);
}

.glass.crop-main {
  top: 540px;
  left: 420px;
  right: 56px;
  padding: 20px 22px;  /* Tight padding to fit content */
}
```

### Rule 5: Animation timing buffer 0.3s giữa phases

**Anh V14 verbatim:** *"em dùng mắt để verify lại output trước khi ship cho anh nha!!!"*

```javascript
// Phase A fade out (T_A)
tl.to(phaseA, { opacity: 0, duration: 0.4 }, T_A);
tl.to([pipA, blackBgA], { opacity: 0, duration: 0.3 }, T_A + 0.1);

// Buffer 0.3s
// Phase B fade in (T_B ≥ T_A + 0.7s)
tl.fromTo(phaseB, { opacity: 0, y: 30 }, { opacity: 1, y: 0, duration: 0.5 }, T_A + 0.7);
```

USP→CTA transition pitfall: USP fade out 30s + CTA fade in 30.1s → CTA invisible at frame 30s. Fix: USP fade out 29.7s + CTA fade in 29.8s (overlap buffer 0.1s).

**Verification:** vision_analyze frame `T_A + 0.3s` — phase A opacity phải = 0, phase B opacity = 0 (chưa fade in). Nếu 1 trong 2 visible → fix timing.

### Rule 6: Caption bar ở BOTTOM rìa, KHÔNG che chart

Caption bar ở `top:950px` chồng chart ở `top:540-820` → fix V15 dời xuống `top:1370px`.

```css
.caption-bar {
  position: absolute;
  z-index: 25;
  left: 420px;        /* Start sau PIP để không che chart/port phase */
  right: 76px;
  top: 1370px;       /* DƯỚI cùng frame, KHÔNG đè chart ở Y=540-820 */
  background: rgba(0, 0, 0, 0.85);
  backdrop-filter: blur(16px);
  border-left: 4px solid #FFD700;
  padding: 8px 12px;
}
```

## V16 verified frames (vision_analyze output thật)

| Phase | Frame | Verify |
|---|---|---|
| HOOK (2s) | "ĐỜI MỚI + Sạc iPhone **không dây**" (TOP) + "80g / ⚡ / 5K" (BOTTOM) | ✅ Mặt anh hiện đầy đủ, KHÔNG che |
| PROBLEM (6s) | "⚡ THỜI ĐẠI 2026" (TOP) + "01 Thời đại này / 02 Cái gì cũng / 03 **nhỏ gọn**" (BOTTOM) | ✅ Mặt anh rõ |
| CHART (10-12s) | BLACK bg + **PIP 320×320 trái** (mặt anh cầm củ sạc) + **Chart glass phải** (500g vs 80g → Nhẹ hơn **6.2 lần**) | ✅ Caption "Thay vì cầm 1 củ sạc nặng nửa ký" ở Y=1370 (bottom) |
| PORT (22s) | BLACK bg + PIP trái (mặt anh) + Port glass phải (🔌 Củ sạc → 📱 iPhone) + "Gắn thẳng cổng sạc → **không cần dây**" | ✅ |
| STAMP (14s) | ☕ trung tâm + "NẶNG!" BOTTOM glass | ✅ |
| PRODUCT (17s) | "Củ sạc mini gắn iPhone" TOP + "80 gram · Lightning · Sạc ngay" BOTTOM | ✅ |
| USP (28s) | "Tại sao chọn củ sạc này?" TOP + 4 cards BOTTOM | ✅ |
| CTA (30s) | "Sẵn sàng nhẹ hơn" TOP + "MUA NGAY" + "499K" BOTTOM | ✅ |

## CSS template copy-paste (V16 final)

```css
/* === PADDING CHÍNH XÁC ===
   Width = 1080 - 56 - 56 = 968 max
   Top safe start: 300px
   Bottom safe end: 1340px
*/

.glass {
  position: absolute;
  z-index: 20;
  background: rgba(255, 255, 255, 0.18);
  backdrop-filter: blur(40px) saturate(180%);
  -webkit-backdrop-filter: blur(40px) saturate(180%);
  border: 1.5px solid rgba(255, 255, 255, 0.4);
  border-radius: 28px;
  padding: 20px 28px;
  box-shadow:
    0 24px 64px rgba(0, 0, 0, 0.4),
    inset 0 1px 0 rgba(255, 255, 255, 0.6);
  opacity: 0;
  position: relative;
  overflow: hidden;
}
.glass::before {
  content: "";
  position: absolute; inset: 0;
  border-radius: 28px;
  background: radial-gradient(circle at 15% 0%, rgba(255, 255, 255, 0.5), transparent 45%);
  pointer-events: none;
}

/* === Phase thường (HOOK, PROBLEM, STAMP, PRODUCT, USP, CTA) === */
.p-top    { top: 300px; left: 56px; right: 56px; }
.p-bottom { top: 1290px; left: 56px; right: 56px; padding: 12px 20px; }

/* === Phase crop (CHART, PORT) - 2-column === */
.crop-main {
  top: 540px;
  left: 420px;
  right: 56px;
  padding: 20px 22px;
}
```

## Distance from V12 (sub-comp disaster) → V16 (pass)

- **V13**: Single-file approach restored (rejected sub-comps — see Pitfall 26 in SKILL.md).
- **V14**: Tightened padding to 56px, separated CHÍNH/PHỤ zones, 2-column for crop.
- **V15**: Moved caption-bar from `top:950px` → `top:1370px` (fix overlap with chart glass).
- **V16**: Port flow font-size 22→18px, padding 24→20px (de-clipped emoji arrows), timing fix for CTA fade-in.

**Key takeaway:** When iterating layouts, **fix one issue at a time and re-verify by vision_analyze each cycle**. Don't compound fixes.

## Anomaly: anh Phá STOP rule (Pitfall 23)

Pitfall 23 mandates STOP after 3 consecutive fails cùng pattern. But at iteration V11, anh override: *"Nhận ra thì làm tiếp cho đến khi có kết quả đi chứ"*.

**When to apply this override:**
- User explicitly says "tiếp"/"làm tiếp"/"đến khi có kết quả" → continue, NOT stop.
- User says "STOP and ask" or stays silent on asks → apply STOP.
- The 3-fails-STOP heuristic applies to *default* behavior; respect explicit user override.

**Lesson:** Pitfall 23 is default behavior. When user explicitly countermands, continue iterating but add safety: re-verify EVERY iteration by `vision_analyze`, don't compound fixes into a single big change.

## Lessons extracted for future Pocket3-product / talking-head clips

1. **Run `swiftc detect_face.swift -o detect_face` first** — measure face bbox mỗi 2s, compute safe zones from data.
2. **Use the 6 hard rules above** as starting point for any Vietnamese talking-head + product clip.
3. **Verify by eyes EVERY iteration** — not just `npx hyperframes lint/check` (automated gates false-positive pass on layout errors).
4. **Fix one issue per iteration** — don't compound fixes that mask what the real issue is.
5. **TikTok safe zones ≠ afterthought** — they're the starting constraint, design AROUND them, not after.
6. **Liquid glass = frosted white iOS 26** — NOT dark glass, NOT static overlay, NOT face-protect gradient.
7. **Crop phase PIP + black BG** (Pitfall 11) — video gốc full-frame standalone is not enough for info-dense phases.

**These 6 rules + the 6-stage verification protocol above are now the contract for any "product + talking head + TikTok" composition build.**
