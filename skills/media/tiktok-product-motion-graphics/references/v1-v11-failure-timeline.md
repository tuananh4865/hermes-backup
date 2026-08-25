# V1→V11 Failure Timeline — Sac-du-phong 32s Pocket3 layout lessons

Captured 2026-07-17 from an 11-iteration loop where agent built → user rejected → agent rebuilt → user rejected, all on the SAME 32-second talking-head product clip about a "củ sạc mini gắn iPhone" (small Lightning charger for iPhone). This document records the failure modes and the 4 hard rules that emerged.

## Source
`/Volumes/Storage-1/Pocket3/Hermes-Edit/sac-du-phong-mini-gan-iphone-04072026-v5.mp4`
- Duration: 32.6s
- Resolution: 1728×3072 portrait
- Speaker: single talking head, moody warm lighting
- Product: small white adapter plugged into Lightning port + powerbank attached to back, brand "Gochodoc"
- Transcript (7 segments): "Các bạn ơi → nhỏ gọn → sạc nặng → quán cafe → gochodoc → gắn iPhone → không cần cầm"

## Per-version failure summary

| Ver | Approach | User feedback | Root cause |
|---|---|---|---|
| V1 | 3 elements only (HOOK + CARD + CTA), dark bg | "chỉ làm có 3 text thôi vậy? Mọi thông tin phải có text/chart" | Pitfall 4 — V1 trap, không có STORYBOARD.md |
| V2 | 11 layers infographic + bar chart, video full bg | "sai gọi là MagSafe... background vẫn là talking head... không audio" | Pitfall 9 (spec guess) + Pitfall 1 (no audio mux) |
| V3 | Dark bg chỉ ở phase text-heavy + ảnh tĩnh talking head NHỎ | "Hiện tại chỉ là một tấm hình tĩnh được em crop và show lên" | Pitfall 8 — dùng ảnh tĩnh thay vì PIP video thật |
| V4 | Real video bg + 1 PIP crop 50% trái + 50% trên, audio có | "Khá ổn! Nhưng background phase PIP vẫn là video gốc full frame thay vì MÀU ĐEN... em crop mù quáng không nhận diện khuôn mặt" | Pitfall 11 (no black-bg swap) + Pitfall 12 (no face-aware crop) |
| V5 | Face-aware crop bằng Vision framework + black bg khi PIP | "Các chữ đang đè lên nhau và sắp xếp bố cục không chính xác" | Animation timing overlap giữa phase transitions |
| V6 | PIP góc trên + glass dưới | "Liquid glass cũng không còn... ở trung tâm trước mặt anh có một điểm đen lớn" | Dùng dark glass thay frosted white + `.face-protect` gradient tạo vệt đen lớn |
| V7 | Face-protect gradient + safe zones TOP only | "Điểm đen lớn trước mặt anh... Đoạn cuối bị chồng chữ" | Vẫn còn `.face-protect` radial-gradient tạo điểm đen lớn |
| V8 | TOP + BOTTOM glass (frosted white), NO face-protect | "Layout vẫn nằm lộn xộn nặng" + "có thể vừa hiện motion graphic ở trên và ở dưới" | Phase crop (CHART) liquid glass sai vị trí + animation timing |
| V9 | Animation buffer 0.5s giữa phases | "Layout vẫn nằm lộn xộn nặng" | Cùng pattern fail — text overlap mặt, phase crop sai vị trí |
| V10 | 3-zone layout (TOP/CENTER/BOTTOM phân bổ đều) | "Layout vẫn nằm lộn xộn nặng" | Vẫn đè mặt anh ở phase 1 HOOK BOTTOM + phase 2 PROBLEM UPPER |
| V11 | TikTok safe zones (ảnh anh gửi) + face data empirical + 4-zone layout | HOOK + PROBLEM PASS, CHART phase fail (chart glass height 180px không đủ chứa content) | Em chưa fix được phase crop CHART, đang STOP theo Pitfall 23 |

## 4 HARD RULES distilled from 11 versions of failure

### Rule A — TikTok safe zones are MANDATORY, not optional
Source: ảnh PNG anh 17/07 gửi. Layout content around the published video's UI, not just the recording canvas.

| Zone (1080×1920) | What | Verdict |
|---|---|---|
| 0-280px | TikTok TOP UI (status + Following/For tabs) | ❌ No text |
| 280-560px | Empty top zone | ✅ Eyebrow/title OK |
| 560-1280px | Speaker face | ❌❌ NEVER text/glass |
| 1280-1380px | Narrow bottom zone (caption area) | ✅ Tagline OK (max 1 line) |
| 1380-1920px | TikTok BOTTOM UI (sound + actions + nav) | ❌ No text |

### Rule B — Face position is empirically STATIC across 32s, but covers ~28% of frame
Verify by running Vision framework face detection on 5 sample frames (not all 32). Mặt anh center ~Y=890, size ~500-580px (28% chiều cao). Plan for face zone = Y=600-1300 in any future Pocket3 clip.

### Rule C — STOP after 3 consecutive same-pattern fails
After V1-V9, 9 versions trong cùng pattern "text/glass đè mặt anh" → **STOP và hỏi anh clarification**, đừng build tiếp V10/V11/V12. Build V10→V11 mà chưa có clarification chỉ tạo thêm waste.

3 options để break loop (anh chọn 1):
- (A) Anh cung cấp video TikTok/YouTube tham khảo cụ thể → em phân tích từng frame
- (B) Anh vẽ wireframe đơn giản (text + số vị trí) → em implement đúng
- (C) Anh tự edit, em không build thêm version

### Rule D — Verify by eyes ON EVERY FRAME, not just spec
"check pass + render success ≠ ship được". Vision analyze 16 extracted frames từ 32s clip, mỗi frame có phase-specific question:
- Mặt anh hiển thị đầy đủ?
- Text/glass ở vị trí hợp lý?
- Animation timing overlap?
- Liquid glass frosted white (không dark)?
- Layout phân bổ đều (không cluster 1 góc)?

If any frame fails → fix timeline + re-render + verify lại. KHÔNG ship khi có 1 frame fail.

## V11 what's verified vs what still fails

| Phase | Frame | Status |
|---|---|---|
| HOOK | ~2s | ✅ Verified bằng mắt — Glass TOP "ĐỜI MỚI + Sạc iPhone không dây" + Glass BOTTOM 3 stats — mặt anh rõ |
| PROBLEM | ~6s | ✅ Verified — Glass TOP "Thời đại 2026" + Glass BOTTOM "01/02/03 nhỏ gọn" — mặt anh rõ |
| CHART | ~10s | ❌ Chart glass cao 180px không đủ, caption bar đè lên — em cần feedback anh tiếp |
| STAMP | ~16s | Chưa verify |
| PRODUCT | ~17s | Chưa verify |
| PORT | ~20s | Chưa verify |
| USP | ~28s | Chưa verify |
| CTA | ~30s | Chưa verify |

## Lessons for future sessions

1. **Khi anh gửi ảnh PNG về TikTok UI safe zones**: dùng ngay từ đầu như Pitfall 22 inputs. Đừng estimate Y coordinates.
2. **5 sample frames** cho face detection là ĐỦ (không cần detect 32/32) — mặt người nói trong talking head gần như static.
3. **Sau 3 fails cùng pattern → STOP + ASK**, dù theo Rule C. Đây là mental model mới — em đã waste 9 versions trước khi nhận ra.
4. **Glass card height cần empirical**: HOOK phase chỉ cần ~140px height (eyebrow 40px + title 64px + padding 40px), CHART phase cần ~600px (title 60px + 2 bars × 80px + footer 60px + padding 100px). Dùng `max-height: 200px` ở TOP zone an toàn, but CHART ở CROP phase cần full center.

## Action items (recommendations for next session)

If anh muốn continue building V12:
- Discuss with anh trước: video reference (Option A) hoặc wireframe (Option B) hoặc anh tự edit (Option C)
- Nếu proceed V12: cần fix CHART phase layout (1 glass ngang từ X=80→X=1000 không đủ → chia thành 2 phần: TOP glass title (Y=80-260) + BOTTOM glass bars (Y=1310-1700))
- HOOK/PROBLEM/PRODUCT/USP/CTA → reuse V11 layout, chỉ thay text content
- PIP ở top:320px (Pitfall 21) cho phase crop

If anh muốn dừng: cleanup 11 file MP4 trong `/Volumes/Storage-1/Pocket3/Hermes-Edit/`, archive V11 HOOK/PROBLEM only.
