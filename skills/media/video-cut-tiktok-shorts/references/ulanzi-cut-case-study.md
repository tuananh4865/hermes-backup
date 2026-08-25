---
title: Ulanzi ChaiBot Cut Case Study (2026-06-30)
created: 2026-06-30
updated: 2026-06-30
type: reference
tags: [video, ffmpeg, tiktok, re-start-detection, orientation, 9-16, ulanzi, case-study]
confidence: high
related_skills:
  - video-cut-tiktok-shorts
  - telegram-video-analysis
  - tiktok-transcript-pipeline
---

# Ulanzi ChaiBot Cut Case Study

> Source: 7 phút video review Ulanzi ChaiBot tripod cho DJI Pocket 3 (Google Drive file ID 1UE0Wo__loAnagQ_32-BPcdsEvCy0Z_PN)
> Goal: cắt thành clip TikTok < 2 phút, công thức TikTok viral
> Final: 52.8s, 1080×1920, H.264, 27 MB

## Timeline workflow

### Turn 1: Download + first transcribe

1. Download via `yt-dlp` (hỗ trợ Google Drive): 1.76 GB MOV (3840×2160 HEVC, 416.87s, 30fps)
2. Extract audio WAV
3. **Whisper large-v3 timeout 600s** (lần đầu, model chưa cache) → kill
4. **Whisper medium chạy 540s** → output 94 segments
5. Phân tích thấy "Các bạn có thể dùng cái góc này" × 72 lần ở 264-408s → dự định CUT toàn bộ

### Turn 2: User nhắc "cắt ừm ờ + re-start"

1. User: "Cắt các đoạn lặp voice, khi nói sai sẽ lặp lại ở câu sau cho giữ được cảm xúc"
2. Em transcribe lại với `--condition-on-previous-text False` → vẫn hallucinate 1 range (0-61s thấy "Hãy đăng ký kênh" lặp 3 lần)
3. Em verify bằng short-segment re-transcribe (60-75s riêng) → phát hiện 264-408s hallucinate
4. Cut based on verified transcript: 6 segments → 399s (6:39)

### Turn 3: User nhắc "ngắn gọn hơn dưới 2 phút, dưới 1 phút càng tốt, theo công thức TikTok"

1. Em build TikTok script với 5 segments: HOOK (5s) + F1 (11s) + F2 (15s) + F3 (5s) + PAYOFF (3s) + CTA (12s) = 51s
2. Cut segments, concat
3. Vision check: ❌ bị bóp vuông do 16:9 → 9:16 sai

### Turn 4: User pushback "clip 9:16 bị bóp thành hình vuông + còn filler + còn lặp"

1. Re-transcribe với **Whisper large-v3** (cache warm, 75s) → 148 segments chi tiết
2. Re-detect re-starts với word overlap > 0.4: 6 clusters
3. Build script refined: 6 segments, 49.5s
4. Cut + concat + scale 9:16

### Turn 5-7: Vision verification loop (4 lần fail orientation)

1. **Lần 1:** `transpose=1` → ffprobe báo 2160×3840 nhưng vision báo "sideways"
2. **Lần 2:** `transpose=2` → tương tự, vẫn sideways
3. **Lần 3:** Strip rotation flag + `crop=ih*9/16:ih:...:0` + `scale=1080:1920` → vision báo "OK đứng thẳng, 9:16 đúng"

## Key learnings

### 1. Whisper large-v3 quan trọng cho audio dài tiếng Việt

Medium hallucinate "Các bạn có thể dùng cái góc này" × 72 lần ở range 264-408s dù đã có `--condition-on-previous-text False`. Large-v3 segment count 148 vs medium 94 → phát hiện re-start chính xác hơn.

Trade-off: Lần đầu timeout 600s, lần sau cache warm = 75s cho 7 phút audio.

### 2. Re-start detection với word overlap

Cluster consecutive segments với > 40% word overlap → phát hiện câu cụt và câu đầy đủ. Cắt câu cụt, giữ câu đầy đủ.

Code snippet:
```python
for i in range(len(segments) - 1):
    words1 = set(segments[i]['text'].split())
    words2 = set(segments[i+1]['text'].split())
    overlap = len(words1 & words2) / max(len(words1), len(words2))
    if overlap > 0.4:
        if len(words1) < len(words2):
            cut_list.append((segments[i]['start'], segments[i]['end']))
```

### 3. Video orientation trap

iPhone videos có `rotation=-90` side data. Metadata `width=3840, height=2160` (landscape) nhưng thực tế pixel layout có thể khác. Em đã:
- transpose=1 → ffprobe báo 2160×3840 nhưng vision thấy sideways
- transpose=2 → tương tự
- CÁCH ĐÚNG: `-metadata:s:v:0 rotate=0` + `crop=ih*9/16:ih:...:0` + `scale=1080:1920`

Vision confirm: "OK đứng thẳng, không cần xoay hay crop thêm".

### 4. Vision check TRƯỚC khi gửi

Mỗi lần scale/crop/rotate, vision-verify frame. User catch được 3 lần orientation sai trước khi em fix đúng. Công cụ vision tool là ground truth, không phải ffprobe metadata.

### 5. Workflow tối ưu cuối cùng

```bash
# 1. Whisper large-v3
mlx_whisper audio.wav --model mlx-community/whisper-large-v3-mlx \
  --condition-on-previous-text False --logprob-threshold -0.5

# 2. Detect re-starts + fillers
# (script v3 trong bài)

# 3. Cut segments với -c copy (HEVC preserved)
for s in script: ffmpeg -ss $s.start -to $s.end -i raw.mov -c copy seg_*.mov

# 4. Concat
ffmpeg -f concat -i concat.txt -c copy -movflags +faststart output.mov

# 5. Convert 9:16 với strip rotation
ffmpeg -i output.mov -metadata:s:v:0 rotate=0 \
  -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 22 -c:a aac -b:a 128k \
  -movflags +faststart output-9x16.mp4

# 6. Vision verify
mcp_MiniMax_understand_image frame.jpg "Orientation đúng? 9:16?"
```

## Pitfalls cụ thể đã gặp

| # | Pitfall | Fix |
|---|---------|-----|
| 1 | Whisper medium hallucinate loop | Switch to large-v3 + verify short segments |
| 2 | Whisper large-v3 timeout 600s lần đầu | Pre-warm cache (chạy medium trước) hoặc retry |
| 3 | Cắt nhầm 264-408s vì tin transcript hallucinate | Re-transcribe đoạn ngắn 30-60s để verify |
| 4 | `transpose=1` không fix orientation | KHÔNG dùng transpose, dùng `-metadata:s:v:0 rotate=0` + crop |
| 5 | Vision tool timeout 300s | Retry 1 lần hoặc fall back to vision_analyze |
| 6 | Vision báo "sideways" nhưng metadata đúng 9:16 | Tin vision, KHÔNG tin metadata |
| 7 | cut from HEVC source dùng -c copy mà bị DTS warning | Re-encode lúc concat |
| 8 | Hero shot không có sản phẩm (người cầm gimbal không phải tripod) | Vision-verify từng segment trước khi include |

## File outputs

| File | Size | Purpose |
|------|------|---------|
| `raw-video.mov` | 1.8 GB | Original 4K HEVC source |
| `audio.wav` | 13 MB | Extracted for Whisper |
| `transcript-large.json` | ~50 KB | Whisper large-v3 transcript với word-level timestamps |
| `transcript-clean.json` | ~30 KB | Whisper medium với `--condition-on-previous-text False` (có hallucinate 1 range) |
| `tiktok-v3-9x16-fixed.mp4` | 27 MB | **Final deliverable** |

## Script structure (final)

```
0:00-0:03  HOOK       "cực kỳ đa năng"
0:03-0:14  F1         quick-release ngàm
0:14-0:30  F2         500N magnet
0:30-0:35  F3         ốp chính hãng, không cấn
0:35-0:39  PAYOFF     "không cần tháo khỏi Pocket 3"
0:39-0:53  CTA        "bấm vào phía dưới để mua"
```

Total: 53s, dưới 1 phút theo yêu cầu user.
