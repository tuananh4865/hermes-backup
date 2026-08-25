# V78 Fresh-From-Source Workflow — Forensic + Pattern (18/07/2026)

## Context

V72-V77 chain-edit của clip_0003 (Dodoto Lux Air V3) fail motion check. Em đã verify forensic:
- Source gốc `clip_0003_V3_troncau_may-hut-bui-cam-tay-2in1.mp4` (99.8 MB, 1080×1920, 106s) có motion 30.86%/5s ✅
- V77 output chỉ còn motion 9.56%/5s ❌ — HyperFrames partial freeze

Anh chọn "làm lại hoàn toàn từ clip gốc 0003 luôn không bắt đầu từ v77. làm đúng theo project v22 làm".

## Forensic Evidence (PIL pixel diff)

```
Source clip_0003_V3_troncau_may-hut-bui-cam-tay-2in1.mp4:
  - File size: 99,810,353 B
  - Bit rate: 7,515,061 bps = 7.5 Mbps
  - Resolution: 1080×1920
  - Duration: 106.25s

Motion (PIL ImageChops.difference @ frame 420×747):
  - t=0→5s: 30.87% pixels changed ✅ (đạt chuẩn ≥10%)
  - t=5→15s: 30.85% ✅
  - t=15→30s: 32.65% ✅

V77 output (HyperFrames fail):
  - File size: 4,499,546 B (-95.5%)
  - Bit rate: 440 Kbps (-94.1%)
  - Duration: 82s
  - Motion @ 0→5s: 6.75% ❌
  - Motion @ 5→15s: 12.38% ❌
```

## Root Cause

**HyperFrames partial freeze** — không phải 100% static, chỉ freeze ~70% frames. Em đã sai khi báo trước đó "source clip 0003 static 100%". Thực tế source motion 30%, V77 mới là partial freeze.

**Em cũng đã sai khi dùng `motion_diff_check.py` chỉ check 1 vùng** (top-left, mặc định). Source talking head nằm ở **giữa khung hình** (Y=540-1620) → top-left luôn là background → kết luận sai "static".

## Lesson vĩnh viễn: Multi-Region Motion Verify

**KHÔNG BAO GIỜ dùng `motion_diff_check.py` chỉ check 1 vùng.** PHẢI sample ≥3 vùng:

```python
from PIL import Image, ImageChops
import subprocess

# Extract 3 frames at strategic timestamps
for t in [0, 5, 15, 30]:
    subprocess.run(["ffmpeg", "-y", "-ss", str(t), "-i", video_path,
                    "-frames:v", "1", "-vf", "scale=420:-1",
                    f"/tmp/frame_t{t:02d}.jpg"], capture_output=True)

# Compute pixel diff per region
regions = {
    "face_mouth":  (540, 900),   # 1080x1920 → scale 420 → ratios preserved
    "face_chin":   (540, 1100),  # talking head motion zone
    "hand_mic":    (600, 1100),  # gesture zone
    "bg_top":      (210, 100),   # top-left (always background)
    "bg_bottom":   (210, 700),   # bottom (lower third, often static)
}

for label, (x, y) in regions.items():
    region_diffs = []
    for i in range(len(frames) - 1):
        diff = ImageChops.difference(frames[i], frames[i+1])
        # Sample at (x, y) ± 50px window
        region_diff = sum(diff.crop((x-50, y-50, x+50, y+50)).histogram()[1:256])
        region_diffs.append(region_diff)
    avg = sum(region_diffs) / len(region_diffs)
    print(f"{label}: avg={avg:.0f}")
    # ✅ PASS if face/chin/hand regions >100
    # ⚠️ WARNING if 50-100 (might be subtle motion)
    # ❌ FAIL if <50 (genuinely static)
```

**Threshold:** motion ≥10% pixels changed = talking head CÓ motion. <5% = static.

## V78 5 Bước Workflow (VERIFIED PASS)

**Step 1 — Copy source gốc (KHÔNG speed 1.3x) → `assets/source/full_bg.mp4`**
```bash
ffmpeg -y -i source_goc.mp4 -an -c:v copy assets/source/full_bg.mp4
```

**Step 2 — Extract 3 PIP từ source gốc (cùng timestamp phase)**
```bash
for label, ss, dur in [("pip_chart", 24, 13), ("pip_usp", 37, 15), ("pip_final", 55, 17)]:
  ffmpeg -y -ss $ss -i source_goc.mp4 -t $dur \
    -vf "crop=1080:1080:0:540,scale=420:420" \
    -an -c:v libx264 -preset fast -crf 23 \
    assets/source/pip/$label.mp4
```

**Step 3 — HTML composition: 4 video elements direct child of root**
```html
<video id="video-bg" data-start="0" data-duration="82" data-track-index="0"
       src="assets/source/full_bg.mp4" muted playsinline></video>
<video id="pip-chart" data-start="24" data-duration="13" data-track-index="1"
       src="assets/source/pip/pip_chart.mp4" muted playsinline></video>
<video id="pip-usp" data-start="37" data-duration="15" data-track-index="2"
       src="assets/source/pip/pip_usp.mp4" muted playsinline></video>
<video id="pip-final" data-start="55" data-duration="17" data-track-index="3"
       src="assets/source/pip/pip_final.mp4" muted playsinline></video>
```

**Step 4 — GSAP timeline register + pause videos (KHÔNG `currentTime = 0`)**
```js
window.__timelines["clip0003-V78"] = gsap.timeline({ paused: true });
const root = document.querySelector('[data-composition-id="clip0003-V78"]');
root.querySelectorAll('video').forEach(v => v.pause());
// KHÔNG set currentTime — HyperFrames tự seek qua timeline
```

**Step 5 — Render silent + ffmpeg ghép audio cuối**
```bash
npx hyperframes render --quality draft --output output_silent.mp4
ffmpeg -i output_silent.mp4 -i audio.aac -c:v copy -c:a aac -shortest FINAL.mp4
```

## V78 PASS Verify

| Spec | Value |
|---|---|
| File | `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip0003_V78_82s_FINAL_with_audio.mp4` |
| Size | **41.9 MB** (vs V77: 4.5 MB) |
| Duration | 82.0s exact |
| Codec | H.264 1080×1920, AAC 44100Hz stereo |
| Bit rate | **4.29 Mbps** (vs V77: 440 Kbps) |
| Motion @ 0→25s | **33.05%** pixels changed ✅ |
| Motion @ 25→55s | **32.95%** pixels changed ✅ |
| Motion @ 55→80s | **32.41%** pixels changed ✅ |

## Decision Rule: Khi nào fresh-from-source vs chain-edit

| Motion verify result | Action |
|---|---|
| Source motion ≥30% / 10s | Chain-edit OK (cẩn thận) |
| Source motion 10-30% / 10s | **Dùng V78 fresh-from-source** |
| Source motion <10% / 10s | **Dùng V78 fresh-from-source + consider Ken Burns slow zoom** |
| V_n motion output <10% / 10s | **FRESH FROM SOURCE** (chain-edit fail) |
| V_n motion output 10-25% / 10s | Consider fresh-from-source (50/50) |
| V_n motion output ≥25% / 10s | Chain-edit OK |

## Anti-patterns (đã fail 4 lần liên tiếp V72-V76)

- ❌ **Patch V_n HTML để fix motion** → chain-edit, motion vẫn yếu
- ❌ **Dùng `<video class="pip-vid" data-start="..." muted playsinline>` trong HyperFrames index.html** → HyperFrames KHÔNG play → render 1 frame tĩnh
- ❌ **Extract PIP mp4 riêng + overlay qua ffmpeg `format=yuva420p`** → 4-layer filter_complex phức tạp, motion freeze
- ❌ **Dùng `currentTime = 0`** thay vì `pause()` → HyperFrames không seek đúng frame
- ❌ **Chỉ extract 1 PIP rồi reuse cho 3 phase** → sai timing audio
- ❌ **Dùng `motion_diff_check.py` chỉ check 1 vùng** (top-left) → kết luận sai "static" khi talking head ở giữa