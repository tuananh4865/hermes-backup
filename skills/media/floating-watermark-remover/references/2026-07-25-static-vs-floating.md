# Session Detail: 24/07 Watermark Removal Cases

## Clip 1: lGZQgDMMMac (static logo, 60fps, SUCCESS)

**Source:** `lGZQgDMMMac_iphone.mp4` (28.82s, 60fps, 1724 frames, 4.06 MB)
**Watermark:** "SB SMASHBERT" channel logo at top-left (x=22-135, y=531-663, size 113x132, yellow color)
**Method:** OpenCV inpaint Telea per-frame, no tracking needed (static position)
**Output:** `lGZQgDMMMac_no_wm_v2.mp4` (3.80 MB)
**Voice overlay:** "có mấy bạn xem video này làm được như bạn ở trong video nào?" (3.8s, [question-ah] emotion)

### Result verification
- 3 timestamps sampled (2s, 14s, 28s) — vision_analyze confirms logo is gone in all
- Diff pixel test passed
- Spec: H.264 + AAC 44100Hz STEREO + 1080×1920 + duration 28.816s (within 5ms of source)

### Bugs caught during this session
- **First attempt hardcoded `FPS=30`** → re-encode produced 57.43s duration (2x). Fix: detect FPS from ffprobe.
- **First attempt used `-r 60 + -vsync 0`** → ffmpeg rejected: "non-CFR -vsync/-fps_mode contradictory". Fix: only `-vsync 0`.
- **First attempt used `delogo`** → visible vertical blur strip remained. Fix: OpenCV inpaint.

## Clip 2: 17si3J8buy (floating watermark, 30fps, PARTIAL)

**Source:** `17si3J8buy_iphone.mp4` (16.39s, 30fps, 490 frames, 6.96 MB)
**Watermark:** "CẨU LỒN VBL" (sometimes "CAU LONG VBL") floating between 2 positions:
- Position A: bottom-left (x=0-131, y=1600-1702, size ~132x103, semi-transparent)
- Position B: top-right (x=680-1079, y=40-159, size ~400x120, semi-transparent)
- Mid-transition positions: ~125 frames with "no-match" template

**Method:** OpenCV template matching + inpaint per frame
**Templates:** 2 (one per position, with 10px padding)
**Tracking:** 489/490 frames matched (conf > 0.4 threshold)

### Result verification
- Tracking: 489/490 frames matched (one frame at transition had no match)
- Logo at sampling frames (1s, 16s): partially removed — mask dilate params need further iteration
- Vision can hallucinate "watermark still visible" when only inpaint blur remains

### Files
- Script: `/tmp/track_wm_v6.py` (workflow verified, mask params need tuning)
- Intermediate outputs: deleted during cleanup

## Voice clone file used

**Path:** `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt`
**Size:** 9931 bytes
**Usage:** Loaded directly as `.pt` file (NOT re-encoded ref audio) — this is the standard pattern per omnivoice-skill conventions

## Voice prompt detection logic

`HSV (15-45, 50-100, 100-255)` for yellow watermark detection on `lGZQgDMMMac`:
```python
yellow_mask = cv2.inRange(hsv, (15, 50, 100), (45, 255, 255))
# Restrict to top-left of video area (y=531-720, x=0-200)
roi = yellow_mask[531:730, 0:200]
```

## References
- Concept page: `/Volumes/Storage-1/Hermes/wiki/concepts/video-watermark-removal-2026-07-25.md`
- Query page: `/Volumes/Storage-1/Hermes/wiki/queries/watermark-removal-comparison-static-vs-floating.md`
- Session log entry: `/Volumes/Storage-1/Hermes/wiki/log.md` (2026-07-25 session:watermark-removal)
