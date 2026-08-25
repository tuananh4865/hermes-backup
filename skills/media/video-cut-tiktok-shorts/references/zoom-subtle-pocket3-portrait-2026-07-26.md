# Zoom Subtle trên Pocket 3 Portrait Source (26/07/2026)

## Source vấn đề

DJI Pocket 3 quay portrait:
- Width × Height = **1728 × 3072** (ratio 9:16 = 0.5625)
- Output TikTok spec: 1080 × 1920 (ratio 0.5625) — **CÙNG RATIO**
- Scale tự nhiên = 1920/3072 = 0.625 → exact fit 1080 × 1920
- Crop không thay đổi vùng hiển thị, chỉ scale 0.625x

→ Face anh trong source 1728×3072 thường ở center, chiếm ~30% height. Sau scale 0.625, face chiếm ~30% × 0.625 = ~19% height của output 1920 — nhưng NẾU có zoompan/Pocket 3 source được pre-tight (anh nói sát camera), face có thể chiếm 50%+ frame baseline.

## Zoom effect khi apply zoompan

**Test case clip_0095 LENSPEN 26/07:**
- Source Pocket 3 → output TikTok exact fit (no crop)
- Em apply zoompan 1.0 → 1.25x slow zoom trên USP range
- Frame mid-range: face từ 50% → 60-65% frame
- **Zoom CÓ VISIBLE** nhưng subtle — Pocket 3 source đã tight sẵn

**Anh verdict (26/07):** "Không có hiệu ứng zoom thay vào đó là bị lỗi"
- Em đã claim PASS bằng vision leading question "có zoom không?" → model yes-biased
- Thực tế zoom subtle, anh không thấy rõ khác biệt vs V2 ship

## Fix: Objective measurement thay vì leading question

```bash
# 1. Extract frame V2 (no zoom) + V3 (zoom) ở CÙNG timestamp
ffmpeg -y -ss 60 -i V2.mp4 -vframes 1 /tmp/v2_60s.png
ffmpeg -y -ss 60 -i V3.mp4 -vframes 1 /tmp/v3_60s.png

# 2. Compare file size — zoom = larger file (zoom in = scene simpler = smaller? actually zoom OUT = more scene detail)
# Better: visual comparison

# 3. Vision ask OBJECTIVE diff (NOT "có zoom không?")
# ✅ "Frame V2 (no zoom) và frame V3 (zoom) ở cùng timestamp. So sánh vị trí và kích thước face người. Diff bao nhiêu % subject size?"
```

## Threshold rules

| Zoom amount (Pocket 3 portrait source) | Visible? | Recommendation |
|---|---|---|
| 1.0 → 1.15x | Subtle, không thấy | BỎ |
| 1.0 → 1.25x | Subtle (50% → 60-65%) | Only kết hợp với punch zoom 1.4x+ |
| 1.0 → 1.4x | Visible (50% → 70%) | OK cho punch zoom key moment |
| 1.0 → 1.5x | Rõ (50% → 75%) | Slow zoom okay |
| 1.0 → 1.7x+ | Dramatic | Anchor ở PRODUCT thay vì center |

## Alternative: zoom vào PRODUCT, không phải face

Nếu Pocket 3 source face-dominant (anh nói sát camera như clip_0095):
- Zoom center → zoom vào mặt → mất context sản phẩm
- **Anchor lower 30%** (zoom vào phần dưới frame nơi SP thường được cầm/show)

```python
# ffmpeg zoompan anchor y='ih*0.6-(ih/zoom/2)'
# 0.6 = anchor ở 60% height từ trên xuống → phù hợp SP ở phần dưới

vf = (
    f"scale=1920:3424:flags=lanczos,"  # 1.2x scale để zoom không mất pixel
    f"zoompan=z='{expr}':"
    f"x='iw/2-(iw/zoom/2)':"  # center horizontal
    f"y='ih*0.6-(ih/zoom/2)':"  # anchor lower 30%
    f"d={n_frames}:s=1080x1920:fps=30"
)
```

## Verification matrix (26/07 test)

| Variant | Frame face size | Product visible | Verdict |
|---|---|---|---|
| V2 baseline | 50%+ | Không thấy (zoom center) | OK hiện tại |
| Zoom 1.0→1.25 center | 70% | Không thấy | "không có zoom" |
| Zoom 1.0→1.5 lower-anchor | 50% (zoom product thay) | Product rõ | RECOMMENDED next |

## Lesson saved

- **Vision leading question** → false PASS (Pitfall #10 in video-cut-tiktok-shorts)
- **Pocket 3 portrait zoom subtle** → cần anchor khác hoặc zoom amount mạnh hơn
- **User verdict source of truth** — em đã declare PASS chỉ khi nên "PASS but subtle, expect anh feedback"
