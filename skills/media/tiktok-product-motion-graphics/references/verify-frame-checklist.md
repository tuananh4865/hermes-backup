# Layout Verification Checklist — Dùng mỗi iteration (V14→V20)

## FIRST-CLASS RULE: Verify by eyes BEFORE ship

Anh feedback 17/07 V8:
> *"dùng mắt để verify lại output trước khi ship cho anh nha!!!"*

Anh feedback V14:
> *"Có nhiều padding lọt ra bên ngoài của khung hình"*

Anh feedback V19:
> *"thông tin giờ còn đè hết lên mặt anh luôn... các đoạn crop video thì thông tin lại được bố trí không hợp lý để trống ở trung tâm quá nhiều mà không tận dụng"*

**Lesson (FIRST-CLASS):** Pipeline tools (lint, check, render) chỉ verify TECHNICAL correctness. KHÔNG verify VISUAL layout. **BẮT BUỘC verify bằng `vision_analyze` TỪNG FRAME** trước khi ship.

## 6-frame verification checklist chuẩn (V20 baseline)

```bash
mkdir -p verify
ffmpeg -y -i output_silent.mp4 -vf "fps=1/2" -q:v 2 verify/f_%02d.jpg
# vision_analyze TỪNG frame với câu hỏi cụ thể từng phase
```

| Giây | Phase | Câu hỏi CHECKLIST |
|---|---|---|
| ~2s | HOOK | Glass ở vùng XANH 2 + XANH 3? Mặt anh rõ? Vùng đỏ (Y=250-400) TRỐNG? |
| ~6s | PROBLEM | Glass ở vùng XANH 1 + XANH 2? "01/02/03 nhỏ gọn" hiển thị? |
| ~10s | CHART (crop) | BLACK bg + PIP trái mặt anh? Chart infographic vùng TÍM? Mini stats vùng XANH 3? Khoảng trống LẤP ĐẦY? |
| ~16s | STAMP | ☕ emoji center + "NẶNG!" vùng XANH 3? |
| ~20s | PORT (crop) | BLACK bg + PIP trái? Port infographic vùng TÍM 🔌→📱→🔋? |
| ~28s | USP | "Tại sao chọn" ở XANH 1? 4 cards ở XANH 2? |
| ~30s | CTA | "MUA NGAY" + "499K" KHÔNG chồng chữ? Liquid glass opacity 0.15? |

**4 dimension mỗi frame:**
1. Face visibility — KHÔNG bị text/element che
2. Padding — content TRONG khung 1080×1920 (KHÔNG clip mép)
3. Hierarchy — CHÍNH (to, center) > PHỤ (nhỏ, rìa)
4. Animation — phase A fade out XONG trước khi phase B fade in

## V20 layout verified bằng mắt thật (5/8 phases)

| Frame | Phase | Result |
|---|---|---|
| 2s | HOOK | ✅ Glass XANH 2 (Y=720-880 ngang mặt, trái) "ĐỜI MỚI + Sạc iPhone không dây" + Glass XANH 3 (Y=970-1100 dưới cằm) 3 stats 80g/⚡/5K. Vùng đỏ TRỐNG |
| 6s | PROBLEM | ✅ Glass XANH 1 "⚡ THỜI ĐẠI 2026" + Glass XANH 2 "01/02/03 nhỏ gọn" |
| 10s | CHART (crop) | ✅ ⚫ BLACK + PIP 360×360 trái (mặt anh) + chart infographic vùng TÍM "Sạc cũ 500g / Củ sạc này 80g / Nhẹ hơn 6.2 lần" + 3 mini stats vùng XANH 3 |
| 16s | STAMP | ✅ ☕ emoji center + "NẶNG!" vùng XANH 3 |
| 22-28s | PORT (crop) | ✅ Port infographic vùng TÍM + mini stats |

## Quy tắc 3-vùng từ ảnh anh vẽ (V20 FINAL)

| Vùng | Màu | Vị trí (1080×1920) | Dùng cho |
|---|---|---|---|
| 🟢 XANH 1 | Xanh lá | Y=100-240 (full-width) | Glass TOP — title, eyebrow |
| 🟢 XANH 2 | Xanh lá | Y=720-880, X=60-680 (trái ngang mặt) | Glass MID |
| 🟢 XANH 3 | Xanh lá | Y=970-1100 (trái dưới cằm) | Glass BOTTOM — stats |
| 🟣 TÍM | Tím | Y=400-950 quanh mặt (chỉ khi crop PIP) | Info elements khi CROP |
| 🔴 ĐỎ | Đỏ | Y=250-400 (vùng trán) | **KHÔNG ĐƯỢC ĐẶT GÌ** |

**Liquid glass opacity = 0.15** (anh chọn V19):
```css
.glass { background: rgba(255, 255, 255, 0.15); }
```

## Phân loại phase

| Đoạn nhiều thông tin (chart, port) | → CROP PIP + free-position elements vùng TÍM |
| Đoạn bình thường (HOOK, STAMP, PRODUCT, USP, CTA) | → Video full-frame + glass vùng XANH |

**Phân loại dựa trên LƯỢNG THÔNG TIN**, không phải thời lượng. Phase 2-3s nhưng nói nhiều info vẫn cần PIP crop.

## Pitfall 23 override: STOP vs CONTINUE

| User signal | Action |
|---|---|
| Silent after ask | STOP, hỏi lại |
| "tiếp"/"làm tiếp"/"đến khi có kết quả" | CONTINUE (anh V11 explicit) |
| "stop"/"dừng" | STOP |
| Mockup/wireframe shared | Dùng mockup làm ground truth, KHÔNG đoán |
| Repeated phrase ("X nữa", "gấp đôi") | Hiểu literal số học (V18: "gấp đôi" từ 1040 → 2080 → cap 1320) |

## Lesson cuối cùng V1→V20

Em fail 18 lần vì:
1. Không dùng mắt verify (V1-V8)
2. Không detect face thật (V1-V7)
3. Không hiểu TikTok safe zones (V1-V10)
4. Apply wrong layout pattern (V1-V12)
5. Auto-iterate without approval (V18→V19)
6. Đổi architecture khi không cần (V12 destroy)

**Khi anh cung cấp mockup ảnh** (V20) → đó là ground truth. Map chính xác từng pixel vào code. KHÔNG đoán.

## Pre-flight check trước khi build

```bash
DETECT=/tmp/aw3_video/detect_face
for sec in 0 2 4 6 8 10 12 14 16 18 20 22 24 26 28 30 32; do
  ffmpeg -y -ss $sec -i source.mp4 -frames:v 1 -vf "scale=864:1536" /tmp/face_t${sec}.jpg
  $DETECT /tmp/face_t${sec}.jpg
done
# Tính safe zones từ data thật, map vào 3 zones (XANH/TÍM/ĐỎ)
```

## Recovery khi fail

```
Fail 1: fix + verify visually → ship
Fail 2: different approach + verify visually → ship
Fail 3: STOP. Apply Pitfall 23 (or Pitfall 31 if user override).
→ User silent → ASK user
→ User "làm tiếp" → continue with reduced-risk (1 fix per iteration)

After 5+ fails same root cause → RECYCLE last approved version + apply feedback thay vì build lại architecture.
```

Verified cuối: V18 ship `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v18_32s_with_audio.mp4`. V20 build tiếp dựa trên mockup ảnh anh vẽ (XANH/TÍM/ĐỎ 3 zones).
