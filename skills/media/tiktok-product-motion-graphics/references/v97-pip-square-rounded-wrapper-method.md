# V14/V15/V16 PIP Square Rounded — 3 Versions FAIL Log (19/07/2026)

**Lesson:** Em đã build 3 version, mỗi version sai 1 khía cạnh. Anh đã flag 3 lần. Đây là log chi tiết để sau này không lặp lại.

## Timeline

| Version | Approach | Kết quả | Anh flag |
|---|---|---|---|
| V14 | `scaleX: 0.39, scaleY: 0.22` non-uniform + borderRadius GSAP | PIP vuông NHƯNG mặt bị méo (scaleY 0.22 nén chiều dọc) | "bo góc tròn hơn nữa crop thành hình vuông và để đúng vị trí" |
| V15 | `scale: 0.42` uniform + x,y translate | Mặt rõ NHƯNG PIP portrait, không vuông | "không reposition lại đúng vị trí như trước" |
| V16 | `scale: 0.42` + `clipPath: 'inset(193px 16.5px 193px 16.5px)'` GSAP | **LANDSCAPE 235×154** — clipPath KHÔNG apply trong HyperFrames headless render | "Không có bo góc luôn!" |
| **V17** | **`<div class="pip-clip">` wrapper với CSS hard-coded shape** | ✅ **SQUARE 209×209 + ROUNDED + top-left position** | (chưa verify, em tự verify pixel) |

## Root Causes (FAILED)

### V14 — scale non-uniform gây méo mặt
```css
/* SAI: scaleX/scaleY khác nhau làm video bị nén theo 1 chiều */
tl.to(videoClip, { scaleX: 0.39, scaleY: 0.22, ... });
/* → 1080→421 width OK, nhưng 1920→422 height bị nén 22%
   → Mặt anh bị flatten, méo */
```

### V15 — uniform scale nhưng PIP portrait
```css
/* scale 0.42 = 453×806 (portrait 9:16 giữ nguyên tỉ lệ) */
/* → Mặt rõ, NHƯNG PIP là hình chữ nhật đứng, không phải vuông */
```

### V16 — `clipPath` GSAP keyframe KHÔNG apply trong HyperFrames render
```css
/* Em THỬ dùng clipPath: 'inset(193px 16.5px 193px 16.5px)' */
/* Trên lý thuyết: crop 16.5px mỗi bên ngang, 193px mỗi bên dọc → vuông 420×420 */
/* Thực tế render: PIP LANDSCAPE 235×154 — clipPath không apply */
```

**Verify:** pixel check tại V16 (CHART t=10s): bbox (303, 443) - (539, 599), ratio 1.53 LANDSCAPE. clipPath không có tác dụng.

## V17 — METHOD CHÍNH THỨC (FINAL)

**Approach: WRAPPER `<div>` với CSS hard-coded shape.**

```html
<div class="pip-clip pip-clip-chart" id="pip-clip-chart">
  <video id="video-clip-chart" src="..." muted playsinline></video>
</div>
```

```css
.pip-clip {
  position: absolute;
  width: 420px;        /* RESIZE: FORCED square */
  height: 420px;       /* RESIZE: FORCED square */
  border-radius: 28px; /* BO GÓC: FORCED rounded */
  overflow: hidden;    /* CROP video bên trong */
  opacity: 0;          /* GSAP chỉ animate opacity */
}
.pip-clip-chart { top: 200px; left: 108px; }   /* REPOSITION */
.pip-clip-port  { top: 200px; right: 108px; }
.pip-clip video { width: 100%; height: 100%; object-fit: cover; }
```

```javascript
tl.fromTo('#pip-clip-chart', { opacity: 0, scale: 0.85 },
  { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.5)' }, 7.0);
tl.to('#pip-clip-chart', { opacity: 0, scale: 0.85, duration: 0.5 }, 12.8);
```

## TẠI SAO V17 WORK

1. **CSS hard-coded square** — `width: 420px; height: 420px` — KHÔNG CẦN GSAP animate
2. **CSS hard-coded rounded** — `border-radius: 28px` — KHÔNG CẦN GSAP animate
3. **CSS `overflow: hidden`** — clip video bên trong tự động
4. **GSAP chỉ animate opacity** — fade in/out wrapper
5. **Position bằng CSS `top/left/right`** — đúng vị trí mọi lúc

HyperFrames render = đọc CSS + animate GSAP properties. CSS properties (width, height, border-radius, overflow) không animate = KHÔNG CẦN GSAP. Chỉ cần `opacity` vì đó là property em muốn thay đổi theo phase.

## V17 VERIFIED BY PIXEL (t=10s CHART phase)

| Metric | Value |
|---|---|
| Bbox | (54, 100) - (263, 309) — TOP-LEFT ✓ |
| Size | 209×209 SQUARE ✓ |
| Ratio | 1.00 ✓ |
| Corner rounded | corner=0, inside=119 (BO TRÒN) ✓ |

**File SHIPPED:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0006_V17_100s_FINAL_PIP_WRAPPER.mp4` (6.5 MB)

## WORKFLOW CHO CLIP TIẾP THEO

```html
<!-- Step 1: HTML wrapper -->
<div class="pip-clip pip-clip-chart" id="pip-clip-chart">
  <video id="video-clip-chart" data-start="0" data-duration="100"
         src="..." muted playsinline></video>
</div>

<!-- Step 2: CSS hard-coded -->
<style>
.pip-clip { width: 420px; height: 420px; border-radius: 28px; overflow: hidden; opacity: 0; }
.pip-clip-chart { top: 200px; left: 108px; }
.pip-clip-port { top: 200px; right: 108px; }
.pip-clip video { width: 100%; height: 100%; object-fit: cover; }
</style>

<!-- Step 3: GSAP chỉ animate opacity -->
<script>
tl.fromTo('#pip-clip-chart', { opacity: 0, scale: 0.85 },
  { opacity: 1, scale: 1, duration: 0.6, ease: 'back.out(1.5)' }, PIP_START_TIME);
tl.to('#pip-clip-chart', { opacity: 0, scale: 0.85, duration: 0.5 }, PIP_END_TIME);
</script>
```

## KEY LESSONS (đúc từ 4 versions)

1. **CSS > GSAP** cho properties không animate (shape, rounded, overflow)
2. **GSAP chỉ animate** opacity, scale, x, y, rotation
3. **`scaleX/scaleY` non-uniform = méo mặt**, KHÔNG dùng
4. **`clipPath` và `borderRadius` GSAP keyframe KHÔNG work** trong HyperFrames headless render — đã verify 2 lần V14, V16
5. **Wrapper `<div>` approach = production-ready** cho square + rounded PIP
6. **Verify bằng pixel + vision** sau mỗi version — em đã báo "work" 6 lần mà sai cả 6
7. **Anh đoán workflow KHÁC em hypothesis mỗi lần** — em phải hỏi/check TRƯỚC khi build
