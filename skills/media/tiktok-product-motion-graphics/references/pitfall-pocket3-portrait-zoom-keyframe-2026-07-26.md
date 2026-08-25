# Pitfall: Pocket 3 Portrait Source + Linear Zoom Invisible (26/07/2026)

## Symptom
Apply zoompan `z='1.0+0.25*on/(d-1)':d=900:s=1080x1920` → zoom chỉ subtle, anh flag "không có hiệu ứng zoom, thay vào đó là bị lỗi".

## Root Cause
**Pocket 3 HEVC 1728×3072 (portrait 9:16) → output 1080×1920 (cũng 9:16):**
- Source ratio = 1728/3072 = 0.5625
- Output ratio = 1080/1920 = 0.5625 → **SAME**
- `scale=1080:1920:force_original_aspect_ratio=increase` → scale 0.625, output exact 1080×1920, **không crop**
- Mặt anh center trong source → output mặt cũng center, chiếm ~50%+ frame
- "Zoom in 1.25x" linear = mặt từ 50% → 60%, khó thấy

## Verify experiment (26/07, clip_0095 USP range 67-95s)
| Method | Scale progression | Visible? |
|---|---|---|
| Linear zoompan | 1.0 → 1.25 (uniform) | ❌ Subtle |
| Linear zoompan anchor y=0.6 | 1.0 → 1.2 | ❌ Subtle + giữ product |
| **KEYFRAME zoompan 1.0→1.3→1.4** | **breakpoint @ 40%** | **✅ RÕ (mặt 50→80%)** |

## FIX Recipe (KEYFRAME-based, đã verified)
```bash
# Source scale 1.4x trước (room cho zoom)
ffmpeg -y -ss {start} -t {dur} -i source.mp4 \
  -vf "scale={int(1080*1.4)}:{int(1920*1.4)}:flags=lanczos,\
zoompan=z='if(lt(on,{N_mid}),\
  1.0+0.3*on/{N_mid},\
  1.3+0.1*(on-{N_mid})/({N}-{N_mid}))':\
x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':\
d={N}:s=1080x1920:fps=30" \
  -c:v libx264 -preset medium -crf 20 -r 30 -an seg_zoom.mp4
```

Với:
- `N` = tổng frames của segment (dur × 30)
- `N_mid` = `int(N * 0.4)` — breakpoint ở 40%

Hiệu ứng:
- Frame 0–N_mid: zoom 1.0 → 1.3 (jump lớn đầu)
- Frame N_mid–N: zoom 1.3 → 1.4 (tinh tế cuối)
- Mặt chiếm 50% → 80%, sản phẩm vẫn visible ở góc

## Verification recipe
1. Render 1 segment riêng, extract 4 frames (start, 40%, 70%, end)
2. Visual compare side-by-side với source cùng timestamp
3. File size tăng từ 1198KB → 1388KB qua keyframes = zoom detect được
4. Nếu không thấy khác biệt → zoom fail, scale phải ≥1.4x

## Anti-pattern (Vision Verification Bias)
Vision model sẽ say "yes có zoom" nếu em hỏi **leading question** "có zoom không?". PHẢI hỏi open-ended "mô tả frame" rồi tự judge dựa vào:
- Mặt chiếm bao nhiêu % frame
- Sản phẩm ở vị trí nào
- Background đổ/tối/sáng thay đổi

## Áp dụng khi
- Source Pocket 3 portrait (1728×3072 hoặc tương đương 9:16 HEVC)
- Zoom effect cho USP/DETAIL range (>5s, có show SP)
- Anh feedback "không thấy zoom"
