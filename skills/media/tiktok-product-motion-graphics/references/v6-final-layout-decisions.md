# V6 Final Layout — Decisions + Cost of Failure (17/07)

> Captured for posterity. This is the 6th iteration in 1 session of the same clip (sac-du-phong-mini-gan-iphone). V1→V6 happened in ~75 minutes. Use it as a study of what NOT to do — and what finally landed.

## Chronological failure + fix timeline

| V# | What was tried | User feedback | Lesson |
|---|---|---|---|
| V1 | 3 text elements (HOOK pill + hook glass + bottom CTA). Video gốc full. No liquid glass, no chart, no PIP. | "Có điểm nào em xem là vượt trội hơn so với cái gốc?" + "Em có thực sự tư duy khi làm việc không vậy?" | **3 elements = fail.** User demands 8+ elements. |
| V2 | 11 elements. Built iOS 26 liquid glass cards + bar chart + iPhone mockup + coffee stamp + 4 USP cards. Video gốc full. Chart 480px right of face. | "Âm thanh đâu? Rồi sao nói quá trời mà chỉ làm có 3 text thôi vậy?" + "đè lên mặt" never said but implied | "Audio missing + elements too few → must show MORE info PER INFO MOMENT, especially on heavy-info phases." Triggered audio mux step. |
| V3 | Rebuilt with chart/port-USP centered right of face (480px). PIP only as talking-head IMAGE (static). Dark gradient bg. | "Hiện tại chỉ là một tấm hình tĩnh được em crop và show lên thôi, còn lại phải là motion graphic style liquid grass." + "Sạc này không phải sạc magsafe mà chỉ là một sạc nhỏ gọn gắn vào công sạc trực tiếp cho iphone thôi!" | **Major course-correction.** (1) Static image ≠ video — must use real video PIP. (2) Wrong product spec (MagSafe) → must vision_verify product name before shipping. (3) Dark bg kills "life energy" of clip. |
| V4 | Video gốc full-frame as background. PIP cropped video at góc trên trái (360×640). All other phases: text/motion graphic overlay on video full. 8 phases with whisper transcript → caption bar sync. | "Những đoạn crop video vào góc thì background phải đổi thành màu đen chỉ chứ, hiện tại bg đang vẫn là clip anh đang nói. Và khi em crop phải nhận diện khu vực mặt của anh nằm ở đâu để crop không cắt mặt anh chứ!" | (1) When PIP active → black-bg behind it, NOT video bg. (2) Face detection before crop — never blind percentage. |
| V5 | Black-bg swap behind PIP ✓. Face-aware crop via Vision framework ✓. But layout: chart glass ngay cạnh PIP (bên phải), nửa dưới talking head = TRỐNG. | "Liquid glass của anh đâu khi em crop thì thông tin phải show ở dưới trung tâm chứ show thông tin song song với video crop của anh làm gì rồi để trống ở dưới nhìn kì vậy?" + "Và hạn chế show thông tin đè lên mặt anh nữa." | (1) PIP góc trên trái + info card nửa dưới. (2) NEVER overlay text/chart on face. |
| **V6** | PIP 420×420 small góc trên trái. Glass cards ở NỬA DƯỚI TRUNG TÂM (top: 680-720). Mặt anh không bao giờ bị che. Audio muxed. | **(SHIPPED)** — file `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v6_32s_with_audio.mp4` (11.4 MB, 1080×1920, AAC 48000Hz stereo, 32s) | **FINAL LAYOUT 2-LAYER:** PIP trên + Info card dưới. |

## V6 layout code (canonical, copy from `index.html`)

```html
<!-- LAYER 1: Video gốc full-frame (always present) -->
<video id="video-bg" class="video-bg" data-start="0" data-duration="32"
       src="assets/source/full_bg.mp4" muted playsinline></video>

<!-- LAYER 2: Black background (only visible during PIP phases) -->
<div class="black-bg" data-class="black-bg"></div>

<!-- LAYER 3: Subtle vignette -->
<div class="vignette" data-class="vignette"></div>

<!-- LAYER 4: Watermark top-right -->
<div class="watermark" data-class="watermark">@tuancuaban</div>

<!-- LAYER 5: PIP cropped video — 420×420 GÓC TRÊN TRÁI -->
<div class="pip-wrap" data-class="pip-chart">
  <video id="pip-chart" data-start="7.3" data-duration="6"
         src="assets/source/pip/chart.mp4" muted playsinline></video>
</div>
<div class="pip-rec" data-class="pip-rec-chart">● ANH ĐANG NÓI</div>

<!-- LAYERS 6+: Liquid glass cards — NỬA DƯỚI TRUNG TÂM -->
<div class="hook-glass" data-class="hook-glass"><!-- top: 720px --></div>
<div class="chart-glass" data-class="chart-glass"><!-- top: 720px --></div>
<div class="port-glass" data-class="port-glass"><!-- top: 680px --></div>
<!-- ... other phases ... -->
```

```css
.pip-wrap {
  position: absolute; z-index: 4;
  top: 80px; left: 80px;     /* GÓC TRÊN TRÁI, không thay đổi */
  width: 420px; height: 420px;
  border-radius: 28px; border: 3px solid rgba(255,255,255,0.8);
}
.pip-rec {
  position: absolute; z-index: 5;
  top: 510px; left: 80px;    /* DƯỚI PIP, không che PIP */
}

.chart-glass, .port-glass, .usp-glass, .product-glass {
  position: absolute; z-index: 20;
  left: 80px; right: 80px;
  top: 680-720px;            /* NỬA DƯỚI TRUNG TÂM */
  /* Không overlap với PIP zone (top: 80-500) */
}
```

## 7 hard rules learned the expensive way (1 session)

1. **Minimum 8 visual elements.** Below 8 = "em có tư duy không vậy". Use STORYBOARD.md template to pre-count.
2. **Verify product spec via vision_analyze.** Wrote "MagSafe" without checking — user caught. Always `ffmpeg -ss T -i SRC -frames:v 1 OUT.jpg` + vision_analyze before commit. Sạc Gochodoc = củ sạc Lightning adapter, KHÔNG MagSafe.
3. **Crop = video PIP, not static image.** Extract image → fail. ffmpeg crop with `data-start` + `data-duration` on `<video>` element → pass.
4. **Crop must be face-aware.** Vision framework Swift script = ground truth. OpenCV CascadeClassifier không có trong venv mặc định. Vision native trên macOS, không cần pip install.
5. **When PIP active, swap to BLACK bg.** Video bg staying full creates visual noise. Fade in/out 0.3s đồng bộ với PIP.
6. **Liquid glass info ở DƯỚI TRUNG TÂM khi có PIP.** PIP ở góc → info ở nửa dưới. NEVER layout info beside PIP — trống dưới talking head = kì.
7. **Never overlay text on face.** Mặt anh = trust + voice sync. Che mặt = mất trust.

## 7 lessons learned costs (per session iteration cost estimate)

| Issue | Build time | Render time | Cost |
|---|---|---|---|
| V1 (3 elements) | 5 min | 21s | "fail Thầy's bar" |
| V2 (11 elements + audio missing) | 18 min | 21s + 5s audio mux = 26s | "âm thanh đâu?" |
| V3 (dark + image + MagSafe) | 22 min | 32s | "ảnh tĩnh + sai spec" |
| V4 (video bg + face crop blind) | 25 min | 32s | "bg vẫn là clip + crop sai mặt" |
| V5 (face-aware + black-bg) | 35 min (Vision compile + verify) | 32s | "info để trống dưới" |
| V6 (PIP trên + info dưới) | 25 min | 32s | ✅ |

**Total time: 6 iterations × 25 min average = 150 min for 32s output.**

The lesson is brutal: **load the right skill + check pre-flight before rendering** could have compressed this to 2 iterations (~45 min total). But the iteration loop was useful — every failure made the spec concrete.

## What this means for the agent

If you're about to render a talking-head product motion graphic for Tuấn Anh:

1. Read this skill first, load STORYBOARD template, write the spec.
2. Pre-flight check (5 min):
   - Count visual elements ≥ 8
   - Verify product spec via vision_analyze
   - Identify heavy-info phases (≥ 5 tokens/second in transcript → PIP needed)
3. Set up PIP crop pipeline (5 min):
   - Build `detect_face.swift` + compile
   - Run face detect on heavy-info frames
   - Crop with 40% padding, clamp to source bounds
4. Compose index.html with 2-layer layout (PIP top + info bottom)
5. Render + mux audio
6. Verify visually with vision_analyze 4-6 keyframes

Skip the "let me try and see what happens" loop. **Tuấn Anh will give you at most 5 chances before escalating to "stop doing this, just rewrite from scratch".**
