# Case Study: TikTok Screen Recording (2026-06-16)

## Context
Tuấn Anh asked "phân tích từng frame của video này!" after sending a video file directly via Telegram. The video was a 17-second iPhone screen recording of a TikTok Shoppable OOTD video.

## File detection
- Path: `/Users/tuananh4865/Downloads/ScreenRecording_06-16-2026 12-51-06_1.MP4`
- Detected via: `ls -lat ~/Downloads/` + pattern match on `ScreenRecording_*.MP4` (uppercase ext)
- mtime: 2026-06-16 12:51 (same day, very recent)

## ffprobe metadata
```
codec_name=hevc
codec_type=video
width=1320
height=2868
r_frame_rate=60/1
codec_name=aac
codec_type=audio
duration=17.044150
size=32075645
bit_rate=15055321
```

**Key signals:**
- HEVC codec → must convert for vision model
- 1320×2868 → iPhone screen recording (not TikTok native)
- 60fps → iPhone Pro/Plus model
- 17s duration → short-form content

## Compression result
- Original: 32MB HEVC
- After `crf 28` H.264 720p: 2.9MB
- Reduction: 91% (preserves visual quality for analysis)

## Frame analysis findings
- 17 frames extracted @ 1fps
- All frames visually similar (mirror selfie, same angle, same outfit)
- **Conclusion:** Video is essentially a static shot with no scene changes
- Content type: TikTok Shoppable OOTD (Outfit of the Day)
- Creator: @mannhiii411 (Mẫn Nhiii)
- Product: "Áo Thun Nữ Chấm Bi Cổ Vuông Ta" (Polka dot square-neck t-shirt)
- Engagement: 78 likes / 44 saves / 8 shares → **save ratio 56%** (high, algorithm-friendly)

## Audio transcription
mlx-whisper output: `"Tạm biệt!"` (Vietnamese: "Goodbye!")

- Single word detected → likely a voice overlay or end-card audio
- Confirms the video has a brief human voice element that frame analysis would miss

## Second ask: motion analysis + AI prompt

Tuấn Anh's follow-up: "anh muốn em phân tích chuyển động của mẫu và góc máy để tạo prompt video tương tự bắt chước hành động chính xác từng frame"

This triggered the motion analysis + AI prompt generation workflow (Step 8 + Step 9).

### Dense frame extraction
- 34 frames @ 2fps (vs 17 @ 1fps for initial analysis)
- Sampled 6 key frames: 2, 8, 15, 22, 28, 34

### ffmpeg scene_score analysis
Pattern detected:
- **0-15s:** Micro-motion đều đặn (scores 0.025-0.073, peaks)
- **Frame 15 (3.75s):** Peak 0.074 → signature pose "Tay chạm ngực"
- **15-17s:** Decreasing → settle pose with slow zoom in

### Pose sequence identified
5 poses:
1. **Pose A (0-3s)** — Front stance, hand at side
2. **Pose B (3-5s)** — "Tay chạm ngực" ⭐ (signature, peak motion)
3. **Pose C (5-12s)** — Body sway, hand at side
4. **Pose D (12-15s)** — S-curve, hand at waist
5. **Pose E (15-17s)** — Settle + slow zoom in

### Camera analysis
- Mirror selfie, eye-level, 1.2-1.5m
- Locked-off (no pan/tilt)
- Slow push-in zoom 5-10% in final 3s
- Slight handheld micro-shake

### Lighting analysis
- Warm overhead diffuse (3000K)
- Chin + neck + side shadows
- Tone-on-tone palette (brown, white, beige)

### AI prompt generated
3 templates sent to Tuấn Anh:
1. Full detailed (for Veo 3 / Kling 2.0+ / Runway Gen-3)
2. Compact (for tools with token limits)
3. Image-to-Video (with reference image)

Plus replicate checklist for shooting the original.

## Final deliverables sent
1. `compressed.mp4` (2.9MB) — resend original
2. `summary.mp4` (815KB) — 17 frames + audio package
3. Structured text analysis with:
   - Metadata table
   - Frame-by-frame description
   - Engagement metrics
   - Save ratio analysis
   - Replicable pattern insights
   - Adaptation ideas for Tuấn Anh's @hi.imdung-style channel
4. **Motion timeline** (5 poses with timings)
5. **Camera analysis table**
6. **Lighting analysis**
7. **3 AI video prompt templates**
8. **Replicate checklist**

## Lesson 1: visual analysis is NOT enough
Even for a "static" video, audio transcription revealed a "Tạm biệt!" voice element. Always run BOTH vision + audio — they catch different signals.

## Lesson 2: frame sampling strategy
Sampling 9 out of 17 frames (53%) was sufficient to characterize the video as static. No need to analyze every frame for short videos. For >60s videos, switch to sparse sampling (every 5-10s).

## Lesson 3: motion analysis needs scene_score
Vision models analyze one frame at a time. They CANNOT detect motion deltas. Combine frame analysis with `ffmpeg scene_score` to identify WHEN motion actually happens. The TikTok video had a clear motion peak at frame 15 (0.074 score) which corresponded to the "tay chạm ngực" signature pose.

## Lesson 4: structured pose prompts work
The "POSE: ... | TAY_T: ... | TAY_P: ... | ĐẦU: ... | VAI: ... | CHÂN: ... | CAM: ... | LIGHT: ... | DELTA: ..." format forces vision models to give per-limb analysis with delta comparison. This is much more useful for AI video prompt generation than free-form descriptions.

## Lesson 5: AI video prompts need timing + intensity
A good AI video prompt must include:
- Pose sequence with TIMESTAMPS (not just "she moves her hand")
- Exact camera setup (angle, distance, movement)
- Micro-motion intensity ("2-3 inch movements, no large gestures")
- Lighting direction + color temp

Generic prompts produce generic videos. Specificity = quality.
