# V22 Canonical Workflow — Verified 17/07/2026, Reinforced 18/07/2026

**Status:** ✅ VERIFIED PASS by anh Tuấn Anh's eye + verified face motion d(1-30) = 158-230.
**Anh verdict (18/07):** "Hôm qua em làm là em lấy video không âm thanh bỏ vào hyperframe để làm motion mà dùng ffmpeg để render cùng âm thanh ở bước cuối thôi."

## V22 Workflow — 4 bước chính gốc

### Bước 1: Source video (không audio)
```bash
ffmpeg -y -i source.mp4 -an -c:v copy assets/source/full_bg.mp4
```

### Bước 2: HTML — `<video>` element làm DIRECT CHILD of root
**HyperFrames framework owns playback** (KHÔNG gọi `video.play()` trong script):

```html
<div id="root" data-composition-id="..." data-start="0" data-width="1080" data-height="1920" data-duration="82">
  <video id="video-bg" class="video-bg" data-start="0" data-duration="82"
         muted playsinline preload="auto">
    <source src="assets/source/full_bg.mp4" type="video/mp4" />
  </video>

  <!-- PIP: <div> wrap <video>, KHÔNG dùng <img> -->
  <div class="pip-wrap">
    <video id="pip-chart" data-start="24" data-duration="13" muted playsinline preload="auto">
      <source src="assets/source/pip/pip_chart.mp4" type="video/mp4" />
    </video>
  </div>

  <!-- Glass cards (KHÔNG qua ffmpeg overlay) -->
  <div class="phase-glass glass-hook">...</div>
</div>
```

```js
const root = document.querySelector('[data-composition-id="..."]');
const bgVideo = root.querySelector('#video-bg');
const pipChart = root.querySelector('#pip-chart');

[bgVideo, pipChart].forEach(v => v.pause());  // KHÔNG gọi play()

const tl = gsap.timeline({ duration: 82, paused: true });
tl.fromTo(hookGlass, { opacity: 0, y: 60 }, { opacity: 1, y: 0, duration: 0.5 }, 0.3);

window.__timelines[COMPOSITION_ID] = tl;
window.__seekTo = (time) => tl.seek(time);
tl.seek(0);
```

### Bước 3: Render silent
```bash
npx hyperframes render --quality draft --format mov --output output_silent.mov
```

### Bước 4: FFmpeg ghép audio cuối (KHÔNG overlay video)
```bash
ffmpeg -y \
  -i output_silent.mov -i audio.aac \
  -c:v libx264 -crf 18 -preset slow \
  -c:a aac -b:a 128k -shortest \
  final.mp4
```

## Kết quả V22
- ✅ Background motion thật (~6 Mbps, KHÔNG phải ~400 Kbps = static)
- ✅ Glass card rõ (KHÔNG qua ffmpeg `format=yuva420p` → KHÔNG bị nén)
- ✅ Face motion: d(1-30) > 100 ở face mouth / face chin / hand mic
- ✅ PIP = video crop scale down (mp4 420×420 từ Y=540)
- ✅ Glass card 0.18 opacity + blur(48px) saturate(200%)

## 7 Sai lầm đã fix (V72-V76 → V77 chính gốc)

| Version | Sai lầm | V77 fix |
|---|---|---|
| V72 | PIP `<video>` element + crop=ih*9/16 → background đen + face bị crop | Crop 1080×1080 từ Y=540 + scale 420×420 |
| V73 | PIP `<video>` 420×420 → nền video lộ (anh: "nền vẫn là video") | V22 workflow KHÔNG overlay video qua ffmpeg |
| V74 | PIP `<img>` PNG tĩnh + nền đen → ảnh tĩnh (anh: "ảnh tỉnh") | PIP `<video>` element direct child of root |
| V75 | PIP video + nền video full toàn clip → em tưởng "nền video" = toàn bộ | V22 workflow: HyperFrames own playback |
| V76 | PIP + nền đen ở vùng PIP qua ffmpeg filter_complex 4-layer | V22 workflow KHÔNG qua ffmpeg filter |
| V77 | Workflow đúng V22 nhưng source clip 0003 gần static → clip motion yếu | Cần source có motion RÕ như sac-du-phong |

## 4 Anti-pattern TUYỆT ĐỐI KHÔNG

1. ❌ `format=yuva420p` overlay glass qua ffmpeg → glass bị nén, mờ + quá trong
2. ❌ Extract PIP mp4 riêng + overlay bằng ffmpeg filter_complex → motion sai, glass quá trong
3. ❌ `<img>` PNG tĩnh cho PIP → ảnh tĩnh không motion
4. ❌ Dùng `<video class="pip-vid" data-start="..." muted playsinline>` cho PIP trong HyperFrames HTML → chỉ render 1 frame tĩnh

## PIP Rules (anh feedback 18/07)

- PIP chỉ ở đoạn cần chèn chart/nhiều thông tin (KHÔNG mọi phase)
- PIP = video crop scale down (mp4 crop 420×420 từ Y=540)
- PIP cùng timestamp với audio đoạn đó (KHÔNG ghép đoạn khác vào)
- Nền ở vùng PIP = nền đen để show thông tin cho rõ (dùng `.black-bg-pip` div HTML, KHÔNG qua ffmpeg)

## Source clip requirements

- **Source talking head cần có motion RÕ** (face cử chỉ, miệng chuyển động rõ) như `sac-du-phong-mini-iphone.mp4` (V22 source) → ra được motion thật
- **Source talking head gần static** như `clip_0003_V3_..._speed13.mp4` (V77 source) → render ra clip motion yếu (~440 Kbps = static) dù workflow đúng
- **Verify source motion TRƯỚC KHI BUILD**: pixel diff face chin Y=1100 d(1-30) > 100 = source OK; < 50 = source gần static → KHÔNG dùng workflow V22 này

## Verify criteria (multi-region pixel diff)

```python
from PIL import Image
# 30 frames distributed across clip duration
# Sample 3 vùng có motion (KHÔNG sample top-left = background)
for region, x, y in [('face_mouth', 540, 900), ('face_chin', 540, 1100), ('hand_mic', 600, 1100)]:
    diffs = ...
    # ✅ PASS if avg > 100 (motion thật)
    # ❌ FAIL if avg < 50 (static frozen)

# Bit rate check: ~6000 kbps = PASS, ~400 kbps = FAIL (static)
```

## Cross-reference

- SKILL.md: section `## 🔴 V22 PIP + GLASS WORKFLOW CHÍNH GỐC`
- 8-Phase breakdown (clip 80s+): section `## 🔴 8-PHASE BREAKDOWN CHO CLIP 80s+`
- PIP cropping math: section `## 🔴 PIP CROPPING PATTERN FOR TIKTOK VERTICAL`
- V7.1 Nate Herk alignment: section `## 🔴 V7.1 NATE HERK ALIGNMENT`
- DEFAULT CONFIG 0.18: section `## 🔴 PIP CROPPING PATTERN ... — DEFAULT CONFIG`
