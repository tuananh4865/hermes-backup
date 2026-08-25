---
title: iOS 26 Liquid Glass Talking-Head PiP — Nate Herk reference
created: 2026-07-17
source: https://youtu.be/Aw3BkmhYu4I
tags: [motion-graphics, hyperframes, talking-head, liquid-glass, reference]
---

# iOS 26 Liquid Glass + Talking-Head PiP — Nate Herk style reference

## Source

- YouTube: `https://youtu.be/Aw3BkmhYu4I`
- Title: **"Claude Video Editing Just Became Unrecognizable"** — Nate Herk | AI Automation
- Published: 2026-04-23, 26 min, AV1/H.264 1280×720
- Workflow context: Claude Code orchestrates `video-use` (cut fillers) → **HyperFrames** (motion graphics) → render
- Anh verdict: "rất đẹp và đúng ý anh"

## 5 visual anchors (verified via 5 frames)

Em xem trực tiếp video bằng `vision_analyze` qua 5 frame đã extract (`aw3_intro.mp4` from `yt-dlp --download-sections "*0:00-1:30"`). 5 đặc điểm style đáng học:

### 1. iOS 26 Liquid Glass cards

- Frosted white panel, **backdrop-filter: blur(...)** rõ ràng
- Bo góc lớn ~16-20px
- Bóng đổ nhẹ
- Cảm giác "thẻ kính nổi trên nền"
- Phù hợp với iPhone 17 / iOS 26 — modern, premium

### 2. Talking-head PiP góc phải dưới

- Crop từ 16:9 gốc → 1:1 hoặc 4:5 ở góc phải
- Rounded corner ~12-16px
- Không che talking head — để lại 60-70% frame trống cho graphics
- Layout giống **podcast talking head** — creator đang giải thích tools

### 3. Subtle backdrop dim khi card hiện

- Talking head **KHÔNG bị crop/move** — chỉ **dim 30-40%** để card nổi
- Animation: card slide-in từ trái + backdrop dim cùng lúc (~600ms ease-out)
- Hiệu ứng: cảm giác "lớp kính" overlay lên video

### 4. Hand-drawn font + pill buttons (workflow explainer)

- Font: **Caveat / Kalam / Patrick Hand** (Google Fonts hand-drawn style)
- Viền trắng dày 3-4px bo góc ~20px
- Mỗi pill 1 màu đặc trưng (không gradient, không drop shadow)
- Dùng cho tên bước trong workflow (Raw File / Trim-Edit / Animate / Render)

### 5. Manual corner badge

- Chữ "Manual" nhỏ ở góc phải trên talking head PiP
- Font nhỏ, màu trắng, không viền
- Đánh dấu "phần này là manual, phần kia là AI"

## 4-phase adapt cho workflow của anh

Khi anh làm video TikTok style "dạy setup/edit/ánh sáng", em có thể build HyperFrames composition theo công thức sau:

```html
<!-- Layer 1: full-bg talking head video -->
<video id="a-roll" src="assets/anhtalkinghead.mp4"
       style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover;z-index:0;"></video>

<!-- Layer 2: dim overlay (animated) -->
<div id="dim-overlay"
     style="position:absolute;inset:0;background:rgba(0,0,0,0);z-index:1;
            transition:background 0.6s ease-out;"></div>

<!-- Layer 3: liquid glass card (animated slide-in) -->
<div id="glass-card"
     style="position:absolute;top:50%;left:-440px;transform:translateY(-50%);
            width:400px;padding:24px 32px;
            background:rgba(255,255,255,0.16);
            backdrop-filter:blur(40px) saturate(180%);
            border:1px solid rgba(255,255,255,0.25);
            border-radius:20px;
            box-shadow:0 8px 32px rgba(0,0,0,0.3);
            z-index:2;color:white;
            transition:left 0.6s ease-out;">
  <div style="font-size:14px;font-weight:600;letter-spacing:0.15em;
              color:rgba(255,255,255,0.7);text-transform:uppercase;">
    ANH TUẤN ANH
  </div>
  <div style="font-size:42px;font-weight:900;margin-top:8px;line-height:1.1;
              text-shadow:0 2px 12px rgba(0,0,0,0.5);">
    Edit video<br/>siêu đẹp
  </div>
</div>

<!-- Layer 4: talking-head PiP (always visible) -->
<div id="pip-talking-head"
     style="position:absolute;bottom:60px;right:60px;
            width:260px;height:260px;border-radius:14px;overflow:hidden;
            box-shadow:0 6px 24px rgba(0,0,0,0.4);
            z-index:3;">
  <video id="pip-video" src="assets/anhtalkinghead_crop.mp4"
         style="width:100%;height:100%;object-fit:cover;"></video>
</div>

<!-- GSAP timeline -->
<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });
window.__timelines["talking-head-card"] = tl;

// Card slide-in từ trái tại 1.5s
tl.to("#glass-card", { left: "60px", duration: 0.6, ease: "power3.out" }, 1.5);
// Backdrop dim đồng thời
tl.to("#dim-overlay", { background: "rgba(0,0,0,0.32)", duration: 0.6 }, 1.5);
</script>
```

## Lưu ý khi adapt cho anh

1. **talking-head phải được quay riêng** (PiP asset không crop từ full video). Nếu chỉ có 1 take 16:9 → dùng CSS `object-position: 80% center` + clip-path thay vì PiP thật.
2. **Liquid glass chỉ work khi backdrop có blur source** (ảnh, video, gradient phức tạp). Nếu nền đen tuyền → glass card mất hiệu ứng, đổi sang dark glass `rgba(0,0,0,0.6) + border rgba(255,255,255,0.1)`.
3. **Pill buttons hand-drawn font** cần load Caveat/Kalam từ Google Fonts — NHƯNG HyperFrames headless Chrome block Google Fonts (`ERR_BLOCKED_BY_ORB` xem Pitfall HF-TikTok-Subtitle 2). Workaround: bundle woff2 vào project `assets/` + dùng `@font-face { src: url('./fonts/caveat.woff2'); }`.
4. **4 phases đã verify**: Liquid glass card / PiP góc phải / dim backdrop / pill button workflow — đều work trong HyperFrames V1+.

## Source links (đã verify)

- Source transcript URL: `https://www.youtube.com/watch?v=Aw3BkmhYu4I`
- Created by: Nate Herk (Skool AI Automation Society, nate@smoothmedia.co)
- 6 chapter timestamps (from video): 0:00 Intro | 1:07 Pipeline | 3:06 Setup | 5:59 Trim | 7:21 HyperFrames vs Remotion | 9:45 Style | 14:37 Prompting | 21:37 Preview | 25:06 Final Render

## Status (2026-07-17)

- Em đã propose apply cho anh: build prototype `talking-head-pip-liquid-glass-v1.html`
- Đang đợi anh confirm → bắt đầu build
- Sau khi anh OK → lưu template vào `templates/talking-head-pip-liquid-glass.html`
