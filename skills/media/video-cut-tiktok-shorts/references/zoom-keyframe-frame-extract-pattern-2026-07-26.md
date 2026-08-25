---
title: ZOOM Keyframe via Frame-Extract Pattern — PITFALL #91 (complement to #10/#11)
created: 2026-07-26
updated: 2026-07-26
type: reference
tags: [pitfall-91, zoom, keyframe, frame-extract, scale-crop, technique-verified, ffmpeg-8.1]
confidence: high
relationships: [zoom-subtle-pocket3-portrait-2026-07-26 (#11), vision-leading-question-false-pass (#10), tiktok-video-editor]
---

# ZOOM Keyframe via Frame-Extract Pattern

> **Status:** Verified WORK trên DJI Pocket 3 source 1728×3072 (Pocket 3 portrait) với ffmpeg 8.1.2 macOS. Anh đã dùng "hyperframe" để test keyframe zoom. Hai approach: (A) zoompan filter (LOẠI - có bug với video input), (B) frame-extract + scale-per-frame + concat (WORK).

## 🚨 Vấn đề với zoompan filter

**zoompan KHÔNG work với video input trong ffmpeg 8.1.2:**
- zoompan designed cho IMAGE input (single frame → zoom từ đầu)
- Khi input là video stream, zoompan chỉ zoom frame đầu + loop vô hạn → output 1 frame tĩnh (md5 identical giữa mọi frame extract)
- `ffmpeg -i src.mp4 -vf "zoompan=z='1+0.4*on/(d-1)':d=N:s=1080x1920:fps=30"` → output dài 120-270s (loop vô tận) thay vì d
- Verify: `ffprobe dur` > 10s cho input 2-3s

**Test ảnh hưởng MD:** 5 lần test thất bại với zoompan (md5 identical 0/3 frames extracted, file size 1.3MB mỗi frame, content tĩnh)

## 🎯 APPROACH WORK: Frame-Extract + Scale-Per-Frame + Concat

**Approach:** Bypass zoompan hoàn toàn. Extract frames riêng lẻ từ source → render MỖI FRAME với scale khác nhau → concat lại thành video segment có zoom progressive.

### 3-step pipeline

**Step 1 — Extract frames PNG sequence:**

```bash
# Tại segment cần zoom, extract frame sequence (30 fps)
mkdir -p /tmp/clip_frames
ffmpeg -y -ss <segment_start> -t <segment_duration> \
  -i <source.MOV> -vf "fps=30" -start_number 0 \
  /tmp/clip_frames/frame_%04d.png -an
```

**Step 2 — Render per-frame với scale keyframe:**

```bash
# Loop N frames, mỗi frame scale thay đổi theo progression
mkdir -p /tmp/clip_zoomed
for j in $(seq 0 $((N-1))); do
  # Linear scale 1.0 → 1.4 (slow zoom)
  # HOẶC Punch: scale_peak sau 15%, hold 35%, giảm 35%, hold 15%
  scale=$(python3 -c "print($START_SCALE + ($END_SCALE - $START_SCALE) * $j / $((N-1)))")
  
  src_w=$(python3 -c "print(int(1728 * $scale))")
  src_h=$(python3 -c "print(int(3072 * $scale))")
  crop_x=$(( (src_w - 1080) / 2 ))
  crop_y=$(( (src_h - 1920) / 2 ))
  
  ffmpeg -y -loop 1 -i /tmp/clip_frames/frame_$(printf "%04d" $j).png \
    -t 0.04 \
    -vf "scale=${src_w}:${src_h}:flags=lanczos,crop=1080:1920:${crop_x}:${crop_y}" \
    -an -c:v libx264 -preset ultrafast -crf 23 -r 30 \
    /tmp/clip_zoomed/z_$(printf "%04d" $j).mp4
done
```

**Cú pháp quan trọng:**
- **`-loop 1 -i PNG -t 0.04`** → loop PNG thành 1 frame video (chính xác = 1/30 = 0.033s)
- **`scale=src_w:src_h:flags=lanczos`** → scale SOURCE (không phải output) theo factor dynamic
- **`crop=1080:1920:offset_x:offset_y`** → crop từ center (offset_x/y = (scaled - output)/2)
- **Tại sao scale source thay vì output?** Scale source lên → source to hơn output → crop 1080x1920 ở center → ZOOM IN. Scale output xuống → crop từ source = ZOOM OUT. Cùng hiệu ứng, khác approach.

**Step 3 — Concat frames thành segment video:**

```bash
# Concat demuxer -c copy (no re-encode, instant)
cat > /tmp/concat.txt <<EOF
file '/tmp/clip_zoomed/z_0000.mp4'
file '/tmp/clip_zoomed/z_0001.mp4'
...
file '/tmp/clip_zoomed/z_0089.mp4'
EOF

ffmpeg -y -f concat -safe 0 -i /tmp/concat.txt -c copy \
  /tmp/zoom_final_segment.mp4
```

### Verify bằng `select='eq(n,N)'` MD5 diff

**⚠️ CRITICAL PITFALL:** `ffmpeg -ss X -i file -update 1 output.png` **LUÔN trả frame đầu tiên**, không phải frame tại timestamp X. Verify zoom bằng:

```bash
# ĐÚNG — extract frame N bằng select filter
ffmpeg -i zoom_final_segment.mp4 -vf "select=eq(n\,0)" -vsync vfr /tmp/frame_0.png
ffmpeg -i zoom_final_segment.mp4 -vf "select=eq(n\,15)" -vsync vfr /tmp/frame_15.png
ffmpeg -i zoom_final_segment.mp4 -vf "select=eq(n\,29)" -vsync vfr /tmp/frame_29.png

md5 /tmp/frame_*.png
# → 3 MD5 KHÁC NHAU = zoom work thật sự (frame đầu → mid → cuối khác nhau)
```

**SAI — leading to false PASS:**
```bash
# KHÔNG dùng cách này để verify
ffmpeg -ss 0.5 -i zoom.mp4 -update 1 /tmp/0.5.png
# → luôn extract frame đầu, MD5 identical cho mọi timestamp
# → em từng declare "zoom không work" vì verify sai
```

### Real case (clip_0095 LENSPEN, 26/07)

| Metric | Result |
|---|---|
| Source range | 67.19-95.77s (USP zoom test) |
| Linear scale | 1.0 → 1.4 (40% zoom progression) |
| Frames extracted | 30 frames trong 1s test (full range 30s × 30fps = 900 frames) |
| Render time | 30 segments × ~3s = 90s |
| Output verify | Frame 0 vs Frame 15 vs Frame 29 → MD5 KHÁC NHAU |
| Visual verify (frame 0 vs 29) | Face từ 50% → 20% frame, ngón tay + SP chiếm 70% |

**Kết luận:** Approach WORK. Zoom visible rõ ràng (face scale giảm 30%, SP scale tăng 50%, anchor ở giữa-dưới).

## Performance notes

- HEVC decode chậm (5-7s cho 30 frames) → chấp nhận được cho clip 30-90s
- Render per-frame + concat nhanh hơn filter_complex `zoompan` do mỗi frame encode 1 file 0.04s
- Total time cho 30s USP segment: extract 30s, render 900 frames = ~45 phút (acceptable nhưng KHÔNG scale cho segment dài > 2 phút)
- Alternative optimization: render 15-30 zoom keyframes (giảm 95% frames) nếu segment dài → linear interpolation giữa 2 keyframes (visual gap khó nhận ra khi < 30 frame interval)

## Khi nào KHÔNG dùng approach này

- Segment > 90s × full zoom continuous → time rendering không acceptable → patch skill tiktok-video-editor với optimized version (chưa built)
- Cần zoom giữa transition segments (zoom vào segment B bắt đầu từ segment A) → dùng `transcode` filter_complex với blend
- Khi user chỉ cần "zoom subtle" 1.0→1.2 → chỉ 1.2x scale không đáng effort, output tự nhiên V2 đã OK (Pocket 3 portrait có sẵn 50% baseline)

## Real verify evidence (26/07)

```
Frame 0 (scale=1.0): MD5=8c1f726555fcc4caa774f873390080f5
  → mặt toàn diện + K8E Concept + áo đen + background rõ

Frame 15 (scale=1.20): MD5=3b3c6f5b154dfc612e54c68dd8248ce6
  → zoom 20% vào ngón tay + SP

Frame 29 (scale=1.4): MD5=306b2d752402935c9b553d1fcba441b7
  → zoom 40% vào ngón tay + thân bút, mặt mất 70%
```

## Khi nào ship approach này vào skill tiktok-video-editor

**Patch conditions (cần đủ cả 3):**
1. ✅ Anh explicit approve keyframe approach (đã có 26/07, "hyperframe" word)
2. ⏳ Approach optimized để không 30-45 phút render cho 30s segment (target ≤ 5 phút)
3. ⏳ Verify protocol tự động (md5 frame + vision compare) thay vì manual

Hiện tại: APPROACH ĐÃ VERIFIED WORK, scale-up cần optimization. Có thể ship V3 cho clip 0095 để anh visual approve trước khi patch skill.

## Related

- `references/zoom-subtle-pocket3-portrait-2026-07-26.md` — V2 baseline đã tight, zoom 1.0→1.25 subtle. Approach này dùng zoom 1.0→1.4 → visible rõ.
- `references/clean-delete-policy-2026-07-26.md` — Khi ship approach mới → KHÔNG để comment tham chiếu approach cũ.
- Skill `tiktok-video-editor` — đang patch v0.06 (zoom approach) sau khi anh approve visual.
