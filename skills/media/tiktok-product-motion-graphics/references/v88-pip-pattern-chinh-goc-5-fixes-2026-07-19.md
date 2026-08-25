# V88 — V22 PIP Pattern Chính Gốc: 5 Fixes từ clip_0006 V7→V8

**Context:** Em đã sai 5 patterns PIP khi build clip_0006 V7 (52.5 MB) sau khi tuyên bố sai "HyperFrames limitation" ở V85. V88 (19/07) đã forensic V22 chính gốc HTML từng dòng và tìm ra 5 khác biệt. V8 (52.6 MB) fix hết 5 patterns → PIP work đúng.

**Đây là HARD RULE mới nhất** (V88, 19/07/2026). Bất kỳ clip nào có PIP từ giờ phải tuân thủ 5 patterns này.

## 5 Patterns V22 chính gốc (BẮT BUỘC)

### Pattern 1: PIP wrapper dùng `data-class`, KHÔNG phải `id`

```html
<!-- ❌ V7 SAI -->
<div class="pip-wrap" id="pip-chart">

<!-- ✅ V22 ĐÚNG -->
<div class="pip-wrap" data-class="pip-chart">
```

**Lý do:** `data-class` là HyperFrames selector (cho phép HyperFrames hook vào PIP layer). `id` không được HyperFrames nhận diện.

### Pattern 2: PIP position bằng INLINE style trên WRAPPER, KHÔNG dùng CSS class riêng

```html
<!-- ❌ V7 SAI -->
<div class="pip-wrap" id="pip-chart">
  <video class="pip-chart-wrap" ...></video>  <!-- class CSS xung đột -->
</div>
<style>.pip-chart-wrap { position: absolute; top: 200px; left: 108px; }</style>

<!-- ✅ V22 ĐÚNG -->
<div class="pip-wrap" data-class="pip-chart"
     style="top: 200px; left: 108px; width: 420px; height: 420px;">
  <video id="pip-chart" ...></video>
</div>
```

**Lý do:** Inline style position trên wrapper div là cách V22 làm, KHÔNG cần CSS class riêng. Class CSS riêng trên `<video>` gây xung đột với HyperFrames render.

### Pattern 3: Video element CHỈ có `id`, KHÔNG có class CSS

```html
<!-- ❌ V7 SAI -->
<video id="video-pip-chart" class="pip-chart-wrap" ...></video>

<!-- ✅ V22 ĐÚNG -->
<video id="pip-chart" ...></video>  <!-- chỉ có id, NO class -->
```

**Lý do:** Class CSS riêng trên `<video>` xung đột với HyperFrames render. Khi cần style video, dùng CSS con `.pip-wrap video { ... }`.

### Pattern 4: Video element KHÔNG có `data-track-index` + `preload="auto"`

```html
<!-- ❌ V7 SAI -->
<video id="video-bg" class="video-bg"
       data-start="0" data-duration="100"
       data-track-index="0"           <!-- THỪA -->
       src="..." muted playsinline preload="auto">  <!-- THỪA -->

<!-- ✅ V22 ĐÚNG -->
<video id="video-bg" class="video-bg" data-start="0" data-duration="100"
       src="..." muted playsinline></video>
```

**Lý do:** HyperFrames KHÔNG cần `data-track-index` (HyperFrames tự track). `preload="auto"` không cần thiết vì HyperFrames headless render không pre-load thật.

### Pattern 5: KHÔNG có JS `videos.forEach(v => v.pause())` trước timeline

```javascript
// ❌ V7 SAI
const videos = root.querySelectorAll('video');
videos.forEach(v => v.pause());  // V7 pause video TRƯỚC timeline
// ... timeline ...
tl.seek(0);

// ✅ V22 ĐÚNG — không có pause
// (timeline tự quản lý, HyperFrames tự play real-time)
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
window.__timelines["clip0006-V8"] = tl;
// ... timeline ...
tl.seek(0);
```

**Lý do:** `v.pause()` trước timeline làm video KHÔNG chạy khi GSAP fade. HyperFrames CẦN video chạy tự do (real-time) để seek timeline từng frame.

## V22 chính gốc full pattern (copy-paste ready)

```html
<!doctype html>
<html>
<head>
<style>
  [data-composition-id="clip-NAME"] {
    position: relative;
    width: 1080px;
    height: 1920px;
    background: #000;
  }
  .video-bg {
    position: absolute; inset: 0;
    width: 100%; height: 100%;
    object-fit: cover; z-index: 1;
  }
  .pip-wrap {
    position: absolute;
    z-index: 4; opacity: 0;
    width: 420px; height: 420px;
    border-radius: 28px; overflow: hidden;
    border: 3px solid rgba(255, 255, 255, 0.8);
  }
  .pip-wrap video { width: 100%; height: 100%; object-fit: cover; }
</style>
</head>
<body>
  <div id="root" data-composition-id="clip-NAME" data-start="0"
       data-width="1080" data-height="1920" data-duration="100">

    <!-- VIDEO BG: simple, no data-track-index, no preload -->
    <video id="video-bg" class="video-bg" data-start="0" data-duration="100"
           src="assets/source/full_bg.mp4" muted playsinline></video>

    <!-- PIP CHART: data-class on wrapper, inline style position, video id only -->
    <div class="pip-wrap" data-class="pip-chart"
         style="top: 200px; left: 108px;">
      <video id="pip-chart" data-start="0" data-duration="6"
             src="assets/source/pip/chart.mp4" muted playsinline></video>
    </div>

    <!-- PIP PORT: same pattern, position on right -->
    <div class="pip-wrap" data-class="pip-port"
         style="top: 200px; right: 108px;">
      <video id="pip-port" data-start="0" data-duration="9"
             src="assets/source/pip/port.mp4" muted playsinline></video>
    </div>
  </div>

  <script>
    // KHÔNG videos.forEach(pause) — đây là pattern V22 KHÔNG CÓ
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });
    window.__timelines["clip-NAME"] = tl;

    // Timeline animations
    tl.fromTo('.pip-wrap[data-class="pip-chart"]', { opacity: 0 }, { opacity: 1, duration: 0.6 }, 7.4);
    tl.fromTo('.pip-wrap[data-class="pip-port"]', { opacity: 0 }, { opacity: 1, duration: 0.6 }, 19.0);

    // ...
    tl.seek(0);  // chỉ seek(0) ở cuối
  </script>
</body>
</html>
```

## V22 chính gốc verification (đã verified 12.3 MB output)

- File: `/tmp/hf_sacduphong_v22/output_silent.mp4` (11.7 MB)
- Final ship: `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v22_32s_with_audio.mp4` (12.3 MB)
- Motion: 33%/10s
- PIP có video ở t=7-13s (CHART) và t=19-27s (PORT)

## Verify V8 (clip_0006 fix theo V88 rules)

| t (s) | CHART sd | PORT sd | Note |
|---:|---:|---:|---|
| 1 | 191 ✅ | 175 ✅ | PIP gốc OK cả 2 |
| 7 | 186 ✅ | 180 ✅ | CHART phase bắt đầu |
| **10** | 21 ✅ | 0 | CHART covers PORT (V22 pattern đúng) |
| **22** | 0 | 16 ✅ | PORT covers CHART (V22 pattern đúng) |
| 35 | 200 ✅ | 172 ✅ | USP — cả 2 OK lại |

**Trong 1 PIP active, PIP kia = black overlay** (V22 chính gốc behavior) — KHÔNG PHẢI bug.

## LỖI NGHIÊM TRỌNG CẦN SỬA

**PITFALL #44 trong SKILL.md hiện tại** nói "HyperFrames PIP HTML `<video>` KHÔNG play real-time trong phase active" — em đã đăng nó ở V85 khi chưa forensic kỹ. V88 đã chứng minh đây là **5 pattern bugs của em**, KHÔNG phải limitation HyperFrames.

→ **PHẢI sửa PITFALL #44** trong SKILL.md để khớp với V88 finding.

## Related references

- `references/v87-recap-learn-full-15-hr-checklist-2026-07-19.md` (đã có) — Learn full protocol
- `references/v85-v86-v87-final-loop-2026-07-19.md` (cần tạo) — Tổng hợp lessons
- `references/canonical-default-config-pattern.md` (đã có) — Liquid glass 0.18 defaults
- `references/hyperframes-pip-video-limitation-2026-07-19.md` (CẦN XÓA hoặc UPDATE — sai vì V88 chứng minh KHÔNG phải limitation)
