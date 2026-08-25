---
title: V22 Canonical Workflow — Forensic Summary (1 page)
created: 2026-07-18
type: reference
tags: [v22, motion-graphics, hyperframes, liquid-glass, pitfall, canonical-workflow]
---

# V22 Canonical Workflow — Forensic Summary

> **⚠ QUAN TRỌNG:** Đây là 1-page forensic summary cho V22 workflow đã VERIFIED PASS
> 17/07/2026. Full skill ở `~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md`
> line 122-220. Đọc file này khi anh hỏi "check lại V22 em đã làm cách nào" hoặc cần
> reproduce pattern tương tự cho clip mới.

## 🎯 TÓM TẮT 1 CÂU

**V22 work vì HyperFrames TỰ play video bg trong headless Chrome + glass cards render
TRONG HTML, KHÔNG qua ffmpeg overlay.** Tất cả V72-V76 đã sai vì extract PIP/glass
riêng → overlay qua ffmpeg `format=yuva420p` → motion freeze (bit rate ~440 Kbps = static).

## ✅ V22 WORKFLOW — 3 BƯỚC CỐT LÕI

### Bước 1 — HTML composition: video bg direct child of root

```html
<!doctype html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=1080, height=1920">
  <title>Motion Graphic</title>
  <script src="https://cdn.jsdelivr.net/npm/gsap@3/dist/gsap.min.js"></script>
</head>
<body style="margin:0;background:#000;">
  <div id="root" data-composition-id="main"
       data-start="0" data-duration="32"
       data-width="1080" data-height="1920">

    <!-- V22 KEY: video bg DIRECT CHILD of root -->
    <video id="video-bg" muted playsinline preload="auto"
           data-start="0" data-duration="32"
           data-track-index="0">
      <source src="assets/source/full_bg.mp4">
    </video>

    <!-- Glass cards render TRONG HTML (KHÔNG qua ffmpeg) -->
    <div class="glass-card hook" data-start="2" data-duration="6" data-track-index="1">
      Củ sạc Lightning mini 20W
    </div>
    <div class="glass-card usp" data-start="10" data-duration="8" data-track-index="1">
      20W Power Delivery • 50% in 30 min
    </div>
  </div>

  <script>
    window.__timelines = window.__timelines || {};
    const tl = gsap.timeline({ paused: true });   // ← paused
    window.__timelines["main"] = tl;

    // V22 KEY: pause tất cả video + seek to 0
    const bgVideo = document.querySelector('#video-bg');
    bgVideo.pause();
    bgVideo.currentTime = 0;

    // Animation cho glass cards
    tl.from('.glass-card.hook', { opacity: 0, y: 30, duration: 0.6 }, 2);
    tl.to('.glass-card.hook', { opacity: 0, duration: 0.4 }, 7);
    tl.from('.glass-card.usp', { opacity: 0, scale: 0.9, duration: 0.5 }, 10);
  </script>
</body>
</html>
```

### Bước 2 — Render silent

```bash
# Render silent (no audio track) — HyperFrames tự play video bg trong headless Chrome
npx --yes hyperframes render --format mov --output /tmp/v22/output_silent.mov
```

### Bước 3 — ffmpeg ghép audio cuối (KHÔNG overlay video)

```bash
ffmpeg -y \
  -i /tmp/v22/output_silent.mov \
  -i /Volumes/Storage-1/Pocket3/Hermes-Edit/sac-du-phong-mini-iphone-04072026-v5.mp4 \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 128k -shortest \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v22_32s_with_audio.mp4
```

## 🔴 V72-V76 ANTI-PATTERNS (đã fail — đừng lặp lại)

| V | Em đã làm sai | Tại sao fail |
|---|---|---|
| V72 | PIP 420×750 portrait + `format=yuva420p` overlay | PIP crop thu nhỏ, glass nén qua ffmpeg |
| V73 | Fix PIP 420×420 vuông nhưng vẫn ffmpeg filter | Face tones tràn vào vùng đen |
| V74 | `<img>` PNG tĩnh thay `<video>` | HyperFrames không animate PNG → 1 frame tĩnh |
| V75 | Extract PIP mp4 riêng + overlay 4-layer | Audio drift, motion freeze |
| V76 | Background video full + black 420×420 overlay | Vẫn qua ffmpeg → static |

## 📐 LAYOUT BENCHMARK V22 (lưu cứng)

| Thông số | V22 verified |
|---|---|
| Composition size | 1080×1920 |
| Video bg source | 1728×3072 → scale 1080×1920 in HTML |
| Glass recipe | `rgba(255,255,255,0.15)` + `blur(40px) saturate(180%)` + border `0.4` |
| Box-shadow | `0 24px 64px rgba(0,0,0,0.4)` |
| Title font | 64px Inter Black |
| Padding | 30px 24px |
| Glass position HOOK/USP/PROBLEM | top 1288-1308px (NỬA DƯỚI, KHÔNG bottom) |
| Glass position CHART/PORT | top 680-720px (ngang hàng với PIP top-left 80,80) |
| Phase gap | ≥0.3s |
| Animation timing | fade in 0.6s ease back.out(1.5), fade out 0.4s linear |

## 📦 V22 SHIP FILE (verified trên disk)

| Spec | Giá trị |
|---|---|
| Path | `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v22_32s_with_audio.mp4` |
| Size | 12.30 MB |
| Duration | 32.000s |
| Codec | H.264 + AAC 48000Hz stereo |
| Resolution | 1080×1920 |
| Bit rate | 3,074,262 bps (~3 Mbps) — production quality |
| Source motion | face chin d(1-30) = 158-230 (PASS) |

## ⚠ LESSON VĨNH VIỄN (cho future session)

**V22 workflow đúng ≠ kết quả tốt nếu source clip KHÔNG có motion.**

V77 (18/07) đã dùng V22 workflow chính gốc 100% nhưng source `clip_0003_V3_..._speed13.mp4`
gần static (face chin d(1-30) ~45) → render ra bit rate 440 Kbps = static.

**Em PHẢI verify source motion TRƯỚC khi apply V22 workflow:**

```bash
# Verify source có motion không (TRƯỚC khi apply V22)
ffmpeg -y -i source.mp4 -vf "fps=2,scale=420:420" /tmp/source_frames/frame_%03d.jpg
# Đếm số frame có RGB diff > 30 giữa consecutive frames
# Nếu < 50% frames có motion → KHÔNG áp dụng V22, cần source khác
```

Hoặc đơn giản hơn — chạy script `motion_diff_check.py` đã có ở skill folder:

```bash
python3 ~/.hermes/skills/media/tiktok-product-motion-graphics/scripts/motion_diff_check.py \
  source.mp4 --t1 0.0 --t2 0.3
# >10% = có motion, dùng V22 OK
# <5% = gần static, KHÔNG dùng V22, tìm source khác
```

## 🔗 CROSS-REFERENCES

- Full skill: `~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md` (line 122-220)
- Case study 22 versions: `wiki/projects/content-creator/sac-du-phong-mini-iphone-22-versions-case-study.md`
- Layout benchmark: `wiki/projects/content-creator/layout-benchmark-vertical-tiktok-1080x1920.md` (28KB)
- Ship file: `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v22_32s_with_audio.mp4`
- Pipeline orchestrator: `~/.hermes/skills/tiktok-pipeline-studio/SKILL.md` (Stage 4-only quick path)