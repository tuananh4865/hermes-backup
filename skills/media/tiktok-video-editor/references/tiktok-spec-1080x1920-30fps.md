# TikTok Spec 1080×1920 30fps — Reference Card

> Nguồn: anh yêu cầu 22/07 ("Mặc định convert xuống 1080x1920 30fps cho phù hợp với tiktok")

## Tại sao 1080×1920 30fps?

| Field | Value | Reason |
|---|---|---|
| Width | 1080 | TikTok portrait standard — backend optimize |
| Height | 1920 | 9:16 aspect ratio (1.778 vs 1.0) |
| FPS | 30 | TikTok playback best at 30fps; 60fps chỉ cho slow-mo |
| Codec | H.264 | Universal phone support, không phải H.265/HEVC |
| Profile | high (Level 4.0) | Phù hợp mobile decode |
| Pixel format | yuv420p | Required cho Android, iOS auto |
| Audio | AAC 44100Hz stereo | iPhone + Android universal |
| Container | MP4 | Standard, +faststart cho web streaming |

## Render command (working v0.01)

```bash
ffmpeg -y -i "$PRE_SPEED" \
    -filter_complex \
        "[0:v]setpts=PTS/1.3,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,fps=30,format=yuv420p[v];
         [0:a]atempo=1.3,aresample=44100,aformat=sample_fmts=fltp:channel_layouts=stereo[a]" \
    -map "[v]" -map "[a]" \
    -c:v libx264 -preset medium -crf 18 \
    -profile:v high -level 4.0 \
    -c:a aac -b:a 192k \
    -movflags +faststart \
    "$FINAL"
```

## HARD GATE verify (check_tiktok_spec.py)

Mọi output PHẢI pass check trước khi ship. Nếu fail → re-render với scale đúng.

```python
# check_tiktok_spec.py exits:
#   0 = all specs match (PASS, can ship)
#   1 = any spec mismatch (FAIL, re-render required)
```

Expected output:
```
✅ ALL PASS — TikTok spec: 1080×1920 30fps h264 aac
```

## Common errors khi source ≠ 1080×1920

| Source | Issue | Fix |
|---|---|---|
| 1728×3072 raw DJI 4K | Scale aspect | `force_original_aspect_ratio=decrease` + `pad=1080:1920` (black bars ngang) |
| 1920×1080 (landscape) | Aspect ratio khác | Letterbox (top/bottom black bars) |
| 1280×720 | Scale lên | `scale=1080:1920` không crop |
| Variable fps DJI (24/30/60) | Fps drift | `fps=30` ép cứng |
| AAC khác sample_rate | Audio sync sai | `aresample=44100` ép |

## Sub-rule for recheck step

Recheck phải check duration delta trong tolerance ±8s sau speed 1.3x:
- expected_pre_speed / 1.3 ≈ actual_post_speed
- |delta| > 8s → FAIL → quay lại step 6 (re-pick keep_plan)

## Performance budget

Trên Apple Silicon M-series 24GB:
- Source 4K 60fps 5min → render 1080×1920 30fps + scale + concat: ~30-60s
- Pre-speed không scale (raw concat): ~10-15s
- Whisper re-transcript final (~60s clip): ~36s with large-v3

## Khi nào KHÔNG dùng TikTok spec?

- YouTube Shorts (9:16 vẫn OK, nhưng 60fps được bonus)
- Instagram Reels (9:16 OK)
- Twitter video (đa aspect)
- Khi anh edit khác platform → check spec từng platform

Anh đã OK giữ nguyên v0.01 sau khi em thừa nhận không phải fresh rewrite. Lesson: PHẢI embed provenance trong skill docs.
