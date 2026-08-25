---
name: anh-tu-anh-editing-style
description: Tuấn Anh's editing preferences and review style for the tiktok-video-editor workflow. Captures the lesson learned across 10-11/07/2026 sessions and 22-version iteration cycles (17/07/2026).
---

## Verification habit
Tuấn Anh often asks "verify xem đã update thật chưa" — wants concrete evidence (version number, file paths, line counts, script outputs), not just claim that I patched something. Always run a verify command sequence after patches.

## Calibration: do the literal minimum, then offer to elaborate
When anh gives a simple rule ("chỉ cần bỏ từ filler thôi"), default to the absolute minimum interpretation. If I add complexity (e.g. 4-step rule when he asked for 1), he flags it: "2 và 4 là sao anh không hiểu. em đang yêu cầu chỉ cần cắt bỏ các từ mà anh vừa nêu ra ở trên thôi mà". Fix: state the simplest rule, give 1-2 examples, stop.

## Test edge cases when he asks
When anh asks "em thư phán đoán và chạy test trong một môi trường ảo xem có bao nhiêu khả năng có thể xảy ra" — he wants me to enumerate ALL plausible cases (6 filler scenarios), verify each against real data (1708 Whisper segs), and only THEN confirm I covered everything. Don't just say "I covered it" — show the matrix of input/output for each case.

## Explicit praise = quality bar marker
When anh says "tuyệt vời", "em đã làm rất tốt", "đăng luôn được", or "phiên bản gần như hoàn thiện" — that's the calibration point for the current task type. Don't relax the bar in next iteration; he will re-raise it.

## Iteration cadence
Anh builds workflows iteratively: simple ask → edge case test → full prediction coverage → validation on real data. Don't try to jump to the end state in one turn.

## Review style
He re-edits clips himself and drops the result in `/Volumes/Storage-1/Tiktok-Tuan-Anh/`. He then demands gap analysis: "Anh cần em phân tích sâu hơn xem anh đã làm gì và em đã làm gì, khác nhau chỗ nào". Always compare em's output against anh's reference with concrete numbers (duration, RMS, keeps count).

## Communication
- Vietnamese casual for user-facing
- English in scripts/logs
- Direct — flag mistakes explicitly with "X là sao", "em quên không...", "Ủa là..."
- Sometimes missing diacritics — follow intent, not exact form

## Iteration rules for motion-graphic product edits (verified V13→V22, 17/07/2026)

Anh's iteration pattern across 22 versions of a single 32s product clip (sac-du-phong mini gan iPhone) established these reusable rules — apply to ANY product clip edit, not just this one.

### Rule 1 — "% of canvas" semantics (X% = X% × canvas_height, not % of current distance)

When anh says "**nâng X%**" / "**hạ X%**" / "**cách lề X%**":
- Default: X% × canvas height (1920px for 1080×1920 portrait)
- Formula: `delta_px = X × 19.2`
- Verified examples (V18, V21, V22):
  - "nâng 5%" (V21) → 1020 − (5 × 19.2) = **924**
  - "hạ 20%" (V22) → 924 + (20 × 19.2) = **1308**
  - "cách lề trên 25%" → 25 × 19.2 = **480** from top
- Exception: "gấp đôi" / "gấp ba" = calculate from previous distance, NOT from canvas
- When ambiguous → verify with 1 frame after patching

### Rule 2 — "Back về X" = recycle X version NGUYÊN TRẠNG, không phải version mới nhất (V20→V21)

Anh said verbatim: "**Back về v17 không đổi layout nữa**".
- "Approved version" ≠ "version gần nhất"
- V19 was latest but V18 was approved → recycle V18 layout, not V19
- Workflow: copy approved/index.html → V21/index.html → apply surgical patches
- When unsure which version to recycle → ask explicitly: "V17 (phase xuống) hay V18 (gấp đôi + caption 25%)?"

### Rule 3 — CHÍNH/PHỤ distinction (V13 feedback leading to V16 PASS)

Anh said verbatim: *"mục chính thì cho xuất hiện ở trung tâm scale lớn hoặc ở khu vực trống không đè mặt còn cụm phụ thì xuất hiện ở rìa"*

| Element type | Position | Size | When to use |
|---|---|---|---|
| **MỤC CHÍNH** (title, chart, port flow) | Center / SAFE zone (NOT over face) | Large (50%+ width) | Single most important per phase |
| **CỤM PHỤ** (stats, caption, mini-tags) | Edge / rìa (top or bottom strip) | Small (≤30% width) | Supporting context |
| ❌ Anti-pattern | Đặt stats trong center → che mặt | |

### Rule 4 — Approved ≠ Frozen (anh vẫn iterate sau approval)

V18 was approved. V19-V22 still had 4 more iterations based on new feedback:
- "Approved" = "current state passes" not "tối ưu rồi, đừng đụng"
- New feedback from anh → continue iterating
- Stop iterating only when anh dừng feedback

### Rule 5 — Phase-classification = crop strategy (verified V14→V22)

Before writing any phase motion graphic, classify it:

| Phase type | Examples | Layout pattern |
|---|---|---|
| **Phase thường** (less info density) | HOOK, PROBLEM, STAMP, PRODUCT, USP | Video full + liquid glass card ở rìa |
| **Phase crop nhiều info** (CHART, PORT) | bar chart, port flow, comparison | BLACK bg + PIP top-left + infographic right |
| **Ending cap CTA** | cuối | Big card 70-80% với 4 specs grid |

Thông tin nhiều → crop PIP. Thông tin ít → full video + glass.

### Rule 6 — Liquid glass opacity sweet spot = 0.15 (verified V19 0.08 fail, V21 0.15 PASS)

| Opacity | Result |
|---|---|
| 0.08 | Too transparent, text hard to read (V19 fail) |
| **0.15** | **Sweet spot — subtle frosted, text readable** |
| 0.18 | Too opaque, lost "liquid" feel |

### Rule 7 — Bỏ noise elements by default (verified V19-V22 PASS)

Anh explicitly removed across iterations:
- ❌ `@tuancuaban` watermark (V19+ removed)
- ❌ "● ANH ĐANG NÓI" red label under PIP (V21+ removed)
- ❌ Caption bar (V21+ removed, redundant with glass)
- ❌ "Mua Ngay" button when ending card is large (V23+ removed)

### Rule 8 — Single-file composition only (V12 FAILed)

V12 tried splitting into `compositions/*.html` + mounting via `data-composition-src`.
- Result: 26 lint errors (unscoped GSAP), frames rendered BLACK
- Single-file index.html with `data-class` selectors = correct pattern
- Sub-compositions only for true multi-document scale (rare, mostly cloud renders)

### Rule 9 — Structural change → write_file fresh, not cp + patch (verified V24 FAIL)

V24 FAIL root cause: copied V23 → patched 8 spots → render → big card 80% didn't appear.
- **Structural change** (new CSS class, new layout section, new animation flow) → `write_file` fresh with read_file base
- **Small patch** (single top, single color) → `cp + patch` is fine
- **NEVER use `!important`** in CSS — triggers specificity wars
- On fail after patching: rollback + write_file fresh, NOT patch again

### Rule 10 — VERIFY NEVER SKIP (FIRST-CLASS — 18/07/2026 feedback)

Anh chất vấn 2 lần trong 1 session (18/07 clip_0003 V4→V5→V6) khi em skip verify:
- *"Ủa verify kiểu gì vậy mày? Mày làm qua loa cho xong phải không? Mày làm không được chỗ nào thì mày phải thử lại chỗ đó cho tới khi xong chứ ai cho phép mày tự ý skip verify ?"*
- *"Video vẫn đơ, ủa chứ clip v22 trước mày làm kiểu gì mà giờ mày làm lại bị lỗi này"*

**Anti-pattern vĩnh viễn:**
- ❌ Báo "3/8 frame PASS, còn 5 frame chưa verify được" rồi SHIP → **FALSE PASS**
- ❌ "Vision tool trả về error, không xem được" → **KHÔNG ĐƯỢC SKIP** — phải thử cách khác
- ❌ Bỏ qua frame vì lười / hết giờ / context sắp đầy / "chắc OK rồi"

**Pattern BẮT BUỘC khi vision_analyze fail (5 step waterfall):**

1. **Thử lại 2 lần** bằng cách khác:
   - Pixel analysis bằng PIL (`getpixel((x,y))`) so sánh RGB
   - Motion check bằng diff giữa các frames
2. **Nếu 2 lần đều fail** → dùng `ffmpeg` extract frame cụ thể rồi analyze lại
3. **Nếu vẫn fail** → dùng `terminal` để gọi `ffmpeg -i ... -ss X -vframes 1 ...` rồi vision_analyze từng frame MỘT
4. **Loop Verify**: FAIL → fix 1 issue → re-render → re-verify → loop cho đến khi PASS HẾT
5. **Verify ở vùng KHÔNG có glass** — vì GSAP animation tạo motion giả ở vùng glass → pixel diff ở vùng có glass = motion giả, KHÔNG phản ánh video thật

**QUY TẮC ĐẾM:**
- 1 frame fail = KHÔNG ship
- 2-3 lần fail liên tiếp = escalate hoặc write_file fresh
- Chỉ ship khi TẤT CẢ frame PASS (đếm bằng tay, không ước lượng)

### Rule 11 — Layout benchmark saved permanently to wiki (18/07/2026)

Sau clip 0003 failure, em đã save 1 file wiki CỘT MỐC để dùng cho MỌI clip dọc TikTok sắp tới:

**File:** `wiki/projects/content-creator/layout-benchmark-vertical-tiktok-1080x1920.md` (19.8KB)

**Trước khi build motion graphic cho clip dọc** → ĐỌC FILE NÀY TRƯỚC. Copy V22 coordinates table chính xác. KHÔNG tự sáng tác position/font.

**Key tọa độ cứng:**
- Resolution: 1080×1920 portrait (KHÔNG dùng square/landscape)
- Padding: 56px (TikTok safe zone)
- Phase thường glass: top 1288/1308 (KHÔNG bottom: 200px)
- Phase crop glass: top 680/720 (ngang hàng với PIP)
- CTA-FINAL: top 192 + bottom 192 (80% khung hình)
- Glass: opacity 0.15, blur 40px, saturate 180%, border 1.5px
- KHÔNG watermark / caption bar / "ANH ĐANG NÓI" / "Mua Ngay"

### Rule 12 — "Back về V" + apply patches = recycle base, NEVER create new mockup (verified 18/07)

Khi anh nói "back về V17" HOẶC "không đổi layout" (verbatim 18/07: "Back về v17 không đổi layout nữa"):
1. **RECYCLE X version NGUYÊN TRẠNG** (copy index.html base + apply patches)
2. **KHÔNG dùng mockup ảnh NEW làm base architecture**
3. **KHÔNG dùng 3-zone XANH/TÍM/ĐỎ** (anh vẽ mockup 18/07) làm layout mới — đó chỉ là "vùng gợi ý" không phải "vị trí cứng"
4. Workflow: `cp V17/index.html V21/index.html` → apply 5-6 patches LÊN V21 → verify từng patch
5. Nếu cần áp dụng mockup mới → HỎI anh trước

**Lesson V20:** Em build FULL architecture mới theo mockup 3 vùng màu → sai → phải back về V17. Mockup chỉ là visual aid, không phải source of truth.
