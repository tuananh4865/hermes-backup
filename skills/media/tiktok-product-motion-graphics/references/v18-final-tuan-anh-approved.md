# V18 FINAL — Tuấn Anh Approved (verified 17/07/2026)

## What happened

Sau 17 versions (V1-V17), Tuấn Anh emit 3 FINAL refinements lên V17 → V18:

**Anh V18 verbatim (3 requests trong 1 turn):**
> *"Bỏ "@tuancuaban" đi. Di chuyển card xuống thêm một khoảng gấp đôi lúc nãy nữa. Cụm text motion ở dưới cùng thì di chuyển lên trên cách lề trên 25%"*

Translation:
1. **BỎ watermark** `@tuancuaban` hoàn toàn
2. **Glass card phase thường xuống GẤP ĐÔI** từ V17 → `top: 1320px` (= V17 1040 + ~280px = "gấp đôi khoảng cách xuống")
3. **Caption bar dưới cùng → lên trên TOP 25%** = `top: 480px` (= 25% × 1920)
4. **Padding chính xác `left/right: 56px`** (không 80px)

## V18 EXACT coords (verified PASS vision_analyze)

| Phase | V17 → **V18 FINAL** | Lý do |
|---|---|---|
| HOOK glass | `top: 1040` → **`top: 1320`** | "gấp đôi" từ V17 |
| PROBLEM glass | `top: 1020` → **`top: 1320`** | Same |
| STAMP | center | (no change) |
| PRODUCT glass | `top: 1020` → **`top: 1320`** | Same |
| USP glass | `top: 1040` → **`top: 1320`** | Same |
| CTA | bottom: 100 | (no change, anchored) |
| **CHART (crop)** | `top: 720` | **GIỮ V6** (V17 unchanged) |
| **PORT (crop)** | `top: 680` | **GIỮ V6** (V17 unchanged) |
| **PIP** | `top: 80, left: 80, 420×420` | GIỮ V6 |
| **Caption bar** | `bottom: 60` → **`top: 480`** | "lên trên cách lề trên 25%" |
| **Watermark** | YES → **REMOVED** | "Bỏ @tuancuaban đi" |
| **Padding** | `left/right: 56px` | (no change từ V14) |

## Implementation (copy-paste ready CSS)

```css
/* ===== V18 LAYOUT ===== */

/* Phase thường - motion XUỐNG DƯỚI GẤP ĐÔI (Y=1320) */
.hook-glass    { top: 1320px; left: 56px; right: 56px; }
.hook-pill     { top: 1240px; }                          /* pill eyebrow */

.problem-glass { top: 1320px; left: 56px; right: 56px; }
.product-glass { top: 1320px; left: 56px; right: 56px; }
.usp-glass     { top: 1320px; left: 56px; right: 56px; }

/* Phase crop - GIỮ V6 (top: 720 / 680) */
.chart-glass   { top: 720px; left: 56px; right: 56px; }
.port-glass    { top: 680px; left: 56px; right: 56px; }

/* PIP góc trên trái - GIỮ V6 */
.pip-wrap      { top: 80px; left: 80px; width: 420px; height: 420px; }

/* Caption bar - LÊN TRÊN 25% = 480px từ trên */
.caption-bar   { top: 480px; left: 60px; right: 60px; }

/* Watermark — BỎ HOÀN TOÀN (không render .watermark element) */
```

## Why V18 is the FINAL version (anh đã ưng)

1. **Talking head full-frame `Y=0-1320`** — 69% màn hình cho mặt anh rõ ràng, không bị glass che
2. **Glass ở `Y=1320-1600`** (280px height) — chỉ chiếm nửa dưới cùng, **không** sát mép TikTok BOTTOM UI (1380-1640)
3. **Caption bar ở `Y=480`** — caption text ở khoảng TRÁN anh (Y=480 ≈ 25% từ trên = 480/1920). An toàn cho talking head, KHÔNG ở dưới cằm (Y=1280+) gây chồng chữ như V8 đã fail
4. **Padding 56px** — content width 968px fits 1080px, không tràn (Pitfall 28 verified)
5. **Phase crop GIỮ V6** (CHART top 720 / PORT top 680) — phần đã được verify vision_analyze trong V6 đến V17, không thay đổi
6. **Không có watermark** — `@tuancuaban` ẩn hoàn toàn trong render output

## Verify V18 (vision_analyze thật)

| Frame | Verify |
|---|---|
| 2s HOOK | ✅ Mặt anh CỰC RÕ cầm iPhone (Lightning port). "⚡ ĐỜI MỚI" eyebrow NO — pill bỏ, chỉ glass Y=1320. No watermark. Caption Y=480 "Các bạn ơi, các bạn ơi". |
| 6s PROBLEM | ✅ Same pattern — "Thời đại 2026 eyebrow" ABOVE glass. Glass Y=1320 "01 Thời đại này / 02 Cái gì cũng phải / 03 nhỏ gọn". Caption "Thời đại này cái gì cũng phải nhỏ gọn" |
| 10s CHART (crop) | ✅ ⚫ BLACK bg + PIP trái (mặt anh cầm củ sạc trắng) + chart glass Y=720 "500g vs 80g → Nhẹ hơn 6.2 lần". NO watermark. |
| 22s PORT (crop) | ✅ BLACK bg + PIP trái + port flow Y=680 "🔌 Củ sạc → 📱 iPhone → 🔋 Sạc đầy" |
| 28s USP | ✅ "Tại sao chọn củ sạc này?" eyebrow ABOVE + 4 cards glass Y=1320 |
| 30s CTA | ✅ "Sẵn sàng nhẹ hơn chưa?" (CTA title) + "Mua ngay gold" + price 499K |

## Source

V18 output: `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v18_32s_with_audio.mp4` (12.0 MB, 1080×1920, AAC 48000Hz stereo)

V18 index.html: `/tmp/hf_sacduphong_v18/index.html` (single file, base = V17 + 4 surgical patches)

## Approval signal — Lesson về "OK đẹp" / "khá ưng"

Khi Tuấn Anh nói **`"OK đẹp"` / `"khá ưng"` / `"ưng nhất"`** trong motion-graphics review → **APPROVED**. STOP building, don't auto-iterate to a "better" version.

Distinct from **`"rất tốt"` / `"phiên bản hoàn thiện"`** (calibration marker — anh nói vậy không có nghĩa mọi thứ xong, mà có nghĩa bar đang ở mức cao, giữ không relax).

Verified V18 — anh đã ưng sau 3 message refinement. Khi đã ưng, KHÔNG tự động build thêm version. Hỏi: "Anh có muốn em chỉnh gì thêm không?" thay vì tự ý next iteration.

## Khi nào dùng V18 (FINAL)

| Điều kiện | Dùng |
|---|---|
| Talking head là focus chính, cần full-screen 0-1320 mặt | **V18** (FINAL anh approved) |
| Cần element ở giữa màn hình không phải talking head | V16 (3-zone split) |
| Phase crop cần nhiều info ở center | V13 (2-column crop) |

## Anti-pattern cảnh báo

```css
/* ❌ Watermark vẫn còn — sai yêu cầu "Bỏ @tuancuaban đi" */
.watermark { display: block; opacity: 1; }

/* ❌ Glass chưa xuống đủ — sai "gấp đôi" */
.hook-glass { top: 1040px; }   /* V17 value, chưa "gấp đôi" */

/* ❌ Caption bar chưa lên — sai "lên cách lề trên 25%" */
.caption-bar { bottom: 60px; }

/* ❌ Padding 80px — sai yêu cầu chính xác từ V14 */
.glass { left: 80px; right: 80px; }
```

## Related

- `references/v17-phase-thuong-motion-xuong-duoi.md` — V17 base (Y=1020+ motion xuống dưới)
- `references/v13-winning-3-zone-layout.md` — V13 SUCCESS layout (3-zone + 2-column crop)
- `references/v6-final-layout-decisions.md` — V6 origin (PIP top + info bottom)
- SKILL.md Pitfall 31 (continue iterating) + Pitfall 33 (V17/V18 coords)
