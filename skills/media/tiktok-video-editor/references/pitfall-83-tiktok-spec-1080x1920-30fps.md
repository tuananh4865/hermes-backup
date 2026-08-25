# PITFALL #83 — TikTok spec 1080×1920 30fps mandatory (v0.01)

## User verbatim feedback (22/07)
> "Mặc định convert xuống 1080x1920 30fps cho phù hợp với tiktok"

## Context
- Source thường 4K từ DJI Pocket 3 (1728×3072 HEVC) hoặc iPhone (1080×1920+ HEVC variable fps)
- TikTok algorithm optimize cho `1080×1920 @ 30fps` H.264 + AAC 44100Hz stereo
- Variable frame rate DJI (24/30/60) → 30fps ép cứng để TikTok playback optimal

## HARD GATE (v0.01)

`scripts/check_tiktok_spec.py` chạy sau step 7b render, **BEFORE** step 8 recheck:

```python
WIDTH_REQUIRED = 1080
HEIGHT_REQUIRED = 1920
FPS_REQUIRED = 30
CODEC = "h264"
PIX_FMT = "yuv420p"
AUDIO_CODEC = "aac"
AUDIO_RATE = 44100
```

Exit code 0 = PASS, 1 = FAIL (auto-block recheck).

## Render command (filter_complex)
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

Filter chain giải thích:
1. `setpts=PTS/1.3` — speed 1.3x
2. `scale=1080:1920:force_original_aspect_ratio=decrease` — scale giữ aspect, không upscale nếu đã đúng
3. `pad=1080:1920:...:color=black` — letterbox nếu aspect khác 9:16
4. `fps=30` — ép 30fps từ variable frame rate source
5. `format=yuv420p` — pixel format TikTok yêu cầu
6. `atempo=1.3` — speed audio 1.3x (chỉ 0.5-2.0 range)
7. `aresample=44100` — sample rate TikTok
8. `aformat=...stereo` — 2-channel audio
9. `libx264 high 4.0` — codec + profile TikTok optimal
10. `+faststart` — streaming-friendly moov atom

## Aspect ratio Edge cases

| Source AR | Target | Pad strategy |
|---|---|---|
| 9:16 (TikTok chuẩn) | 1080×1920 | scale only, no pad |
| 16:9 (landscape) | 1080×1920 | scale đến height=1920, pad left/right |
| 4:3 or other (portrait narrow) | 1080×1920 | scale đến width=1080, pad top/bottom |
| 9:21.6 (TikTok vertical max) | 1080×1920 | scale, top/bottom pad |

`scale=...force_original_aspect_ratio=decrease,pad=...:color=black` tự handle mọi AR.

## Test
```bash
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/check_tiktok_spec.py <output>.mp4
```

Expected:
```
Width × Height: 1080×1920
Frame rate: 30.00 fps (30/1)
Video codec: h264 (profile: High)
Pixel format: yuv420p
Audio codec: aac @ 44100Hz
Duration: <X>s
✅ ALL PASS — TikTok spec: 1080×1920 30fps h264 aac
```

## Verified
- clip_0036 V3 final.mp4: 1080×1920, 30fps, AAC 44100Hz → ALL PASS
- Duration delta vs expected: 5.59s < 8s tolerance

## Bài học
Default render phải produce TikTok-spec MP4. KHÔNG BAO GIỜ skip `check_tiktok_spec.py` — exit 0 là required before recheck. Quality control pipe: render → HARD GATE spec → recheck → ship.
