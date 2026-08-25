---
title: V83-V84-V85 Final Loop + Face-Safe-Zone Pixel Scan Protocol
created: 2026-07-18
type: reference
version: 1.0
applies-to: Mọi clip TikTok dọc 1080×1920 có mặt người nói/cầm sản phẩm
priority: SECOND-CLASS — đọc sau v84-face-safe-zone-pre-build-pixel-scan.md nếu đã có
---

# V83-V84-V85 Final Loop — Face-Safe-Zone Hard Rule Vĩnh Viễn

> **Context:** Em đã loop 7 versions (V78→V84) để đạt được final. V85 RECAP với vùng cấm mặt vĩnh viễn là kết quả cuối cùng. File này lưu lại CHI TIẾT từng version fix gì, tại sao fail, fix bằng cách nào.

## BẢNG TỔNG HỢP 7 VERSIONS

| V | Trigger | Lỗi | Fix | Status |
|---|---------|-----|----|--------|
| V78 | Chain-edit qua V77 | Thiếu 4 phase | Build 8 phase đầy đủ | FAIL→V79 |
| V79 | Build 8 phase | PIP không hiển thị | `.pip-wrap` thay vì `.pip` | FAIL→V80 |
| V80 | PIP visible | 3 lỗi (sát lề/lệch/CTA 33s) | Hạ PIP top 200, CTA 55-65s | FAIL→V81 |
| V81 | CTA 10s cuối | 4 lỗi (lệch/cạnh PIP/thập phân/che mặt) | Nâng testimonial/feature, Math.floor | FAIL→V82 |
| V82 | Fix testimonial/feature | Không có vùng cấm global | Hard rule safe zone 10% | FAIL→V83 |
| V83 | Safe zone 10% | testimonial/feature vẫn che mặt | Nâng tới đỉnh đầu top 200/220 | FAIL→V84 |
| **V84** | Final fix | **KHÔNG** | **Final approved** | **APPROVED** |

## V85 VĨNH VIỄN — VÙNG CẤM MẶT ANH

**Ảnh khoanh đỏ anh gửi 591×1280 → scaled 1920×1920:**

| Property | Value (scaled 1920) |
|---|---|
| Top | **547px** (= y_top of HEAD) |
| Bottom | **1140px** (= y_bottom of FACE) |
| Left | 308px |
| Right | 1526px |
| Width × Height | 1218 × 592 |
| Center | (917, 843) |

```css
:root {
  /* Vùng cấm mặt vĩnh viễn từ khoanh đỏ 18/07/2026 */
  --face-zone-top: 547px;
  --face-zone-bottom: 1140px;
  --face-zone-left: 308px;
  --face-zone-right: 1526px;
}

/* RULE: Glass card ở vùng mặt → CHỈ khi phase có PIP background */
```

## DECISION TABLE V85 VĨNH VIỄN (anh approved V84)

| # | Phase | t (s) | Card top | Vùng mặt (547-1140)? | Exception | Status |
|---|---|---:|---:|---|---|---|
| 1 | HOOK | 0-3 | 1308 | KHÔNG (y > 1140) | OK | ✅ |
| 2 | PROBLEM | 3-7 | 1288 | KHÔNG (y > 1140) | OK | ✅ |
| 3 | **CHART** | 7-13 | 966 | CÓ (y < 1140) | **CÓ PIP + nền đen** | ✅ |
| 4 | **STAMP** | 13-16 | 50% center | CÓ (y ≈ 960) | 1.5s flash, nền đen | ✅ ngoại lệ |
| 5 | PRODUCT | 16-19 | 1380 | KHÔNG (y > 1140) | OK | ✅ |
| 6 | **PORT** | 19-27 | 966 | CÓ (y < 1140) | **CÓ PIP + nền đen** | ✅ |
| 7 | USP | 27-32 | 1280 | KHÔNG (y > 1140) | OK | ✅ |
| 8 | **TESTIMONIAL** | 32-37 | **200** | KHÔNG (y < 547) | OK (tới đỉnh đầu) | ✅ |
| 9 | **FEATURE (countUp)** | 37-44 | **220** | KHÔNG (y < 547) | OK (tới đỉnh đầu) | ✅ |
| 10 | USE-CASE | 44-55 | 1280 | KHÔNG (y > 1140) | OK | ✅ |
| 11 | **CTA-FINAL 80%** | 55-65 | center 80%×80% | CÓ (full màn hình) | 10s cuối, tổng hợp | ✅ ngoại lệ |

## 11 SCREENSHOT FRAMES — CHỨNG CỨ V85

Em đã chụp 11 frame ở `/tmp/v84_frames/`:

| # | Phase | t (s) | File | Y card (scaled) | Vùng mặt? |
|---|---|---:|---|---:|---|
| 1 | HOOK | 1 | `HOOK_01s.jpg` | 1308 | KHÔNG |
| 2 | PROBLEM | 5 | `PROBLEM_05s.jpg` | 1288 | KHÔNG |
| 3 | CHART | 10 | `CHART_10s.jpg` | 966 | CÓ (PIP exception) |
| 4 | STAMP | 14 | `STAMP_14s.jpg` | 960 | CÓ (1.5s ngoại lệ) |
| 5 | PRODUCT | 17 | `PRODUCT_17s.jpg` | 1380 | KHÔNG |
| 6 | PORT | 22 | `PORT_22s.jpg` | 966 | CÓ (PIP exception) |
| 7 | USP | 29 | `USP_29s.jpg` | 1280 | KHÔNG |
| 8 | TESTIMONIAL | 34 | `TESTIMONIAL_34s.jpg` | 200 | KHÔNG ✅ |
| 9 | FEATURE | 40 | `FEATURE_40s.jpg` | 220 | KHÔNG ✅ |
| 10 | USE-CASE | 49 | `USE-CASE_49s.jpg` | 1280 | KHÔNG |
| 11 | CTA-FINAL | 60 | `CTA-FINAL_60s.jpg` | 80%×80% | full (ngoại lệ) |

## KEY INSIGHT TỪ 7 LẦN FAIL

**Nguyên nhân gốc (V78→V83):** Em đoán vị trí card dựa trên cảm tính, KHÔNG pixel scan screenshot anh gửi trước khi build.

**Fix đúng (V84 → V85):**
1. Pixel scan ảnh khoanh đỏ → tìm face zone chính xác (y=547-1140 scaled)
2. Apply decision tree: card nào ở face zone → phải có PIP background
3. Card testimonial/feature (text dài) → LUÔN ở đỉnh đầu (y < 547)
4. CTA-FINAL 80% → ngoại lệ duy nhất, OK che mặt (10s cuối, tổng hợp thông tin chính)
5. STAMP 1.5s flash → ngoại lệ, OK che mặt 1.5s

## LIÊN KẾT VỚI CÁC SKILL KHÁC

- **Hard rule V22 PIP + GLASS**: `## V22 PIP + GLASS WORKFLOW CHÍNH GỐC` ở SKILL.md
- **Liquid glass CSS**: `## V7.1 NATE HERK ALIGNMENT` ở SKILL.md
- **Pixel scan protocol**: `references/v84-face-safe-zone-pre-build-pixel-scan-2026-07-18.md`
- **Safe zone 10%**: `references/v78-v82-iteration-loop-safe-zone-lesson-2026-07-18.md`

## KHI NÀO DÙNG V85 vs V22

**V22** (sac-du-phong 32s):
- Product showcase KHÔNG talking head
- 8 phase đơn giản: HOOK + PROBLEM + CHART + STAMP + PRODUCT + PORT + USP + CTA
- Card CHART/PORT ở top 720 (ngang hàng PIP)
- Opacity 0.15

**V85** (clip 0003 65s):
- Talking head review
- 11 phase với TESTIMONIAL + FEATURE + USECASE ở giữa
- Card CHART/PORT ở top 966 (dưới PIP — vùng trống giữa PIP 620 và CTA 1280)
- Opacity 0.18

## ANTI-PATTERN VĨNH VIỄN (đúc từ 7 versions)

- **Build mà không pixel scan TRƯỚC** → 80% khả năng card che mặt
- **Card TESTIMONIAL/FEATURE ở vùng mặt (y=547-1140)** khi không có PIP background
- **Đoán vị trí từ V22 baseline** khi clip có talking head khác (cần pixel scan lại)
- **CTA 80% ở top < 50s** → mất motion graphic info, phải ở 8-10s cuối
- **Build nhiều version chain-edit** thay vì fresh-from-source khi motion fail
- **Dùng `currentTime = 0`** thay vì `pause()` → HyperFrames không seek đúng frame
- **Bỏ qua Step 1-2 (scan screenshot)** vì "đã biết vị trí rồi" → false sense of security

## KẾT LUẬN

**Loop V78-V84 KẾT THÚC tại V84.** Em đã đúc 7 lessons vĩnh viễn + vùng cấm mặt vĩnh viễn. Nếu anh có clip mới:
1. Pixel scan screenshot TRƯỚC (nếu có) HOẶC estimate face zone y=547-1140 nếu clip talking head
2. Apply decision tree V85
3. Render + verify bằng cách scan rows ở các timestamp phase
4. Ship khi pass

**KHÔNG BAO GIỜ build >2 versions** cho cùng 1 clip. Nếu V_n fail, refresh từ source gốc + apply V85 protocol trước khi build V_{n+1}.
