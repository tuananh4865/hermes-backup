# CRITICAL — GSAP Fade-in Initial State Rule (V90 — 19/07/2026)

**Bối cảnh:** Em đã sai 5 lần (V85/V87/V88/V89) báo "HyperFrames limitation" về clip_0006 PIP. Anh đã đoán ĐÚNG từ đầu: "Có khi nào em đang để phần nền đen nằm đè lên trên clip không?" → CTA-glass thiếu opacity:0 che full timeline.

## Rule VĨNH VIỄN

**MỌI element có GSAP `tl.fromTo()` PHẢI có `opacity: 0` initial trong CSS:**

```css
.cta-glass, .chart-glass, .port-glass, .usp-glass, .testimonial-glass,
.feature-glass, .usecase-glass, .product-glass, .problem-glass, .hook-glass,
.pip-wrap, .chart-row, .port-step, .usp-item, .usecase-item {
  opacity: 0;  /* ← BẮT BUỘC */
}
```

## Tại sao GSAP `tl.fromTo()` KHÔNG tự apply initial state?

```javascript
// Code:
tl.fromTo('#cta-glass', { opacity: 0 }, { opacity: 1, scale: 1 }, 90);

// Timeline execution:
// t=0 to t=90 → element ở STATE MẶC ĐỊNH (opacity:1 từ CSS)
// t=90 → GSAP apply "from" state (opacity:0) ngay lập tức + animate to "to" state
//
// → Trước t=90, element visible = CHE PIP!
```

## Real case V8/V9/V10 FAIL (clip_0006)

```css
/* CSS BUG: thiếu opacity:0 initial */
.cta-glass {
  top: 50%; left: 50%;
  transform: translate(-50%, -50%);
  width: 80%; height: 80%;
  z-index: 25;
  background: rgba(0, 0, 0, 0.92);
  border: 2px solid rgba(255, 215, 0, 0.5);
  /* opacity: 0 ← THIẾU */
}
```

CTA 80% + z-index 25 + bg đen 92% = ĐÈ full màn hình từ t=0 → t=90s.

**Fix V11:** Thêm `opacity: 0` → CTA invisible → PIP work (95%+ bright ở mọi phase).

## Root Cause Investigation Checklist

Khi anh flag "có gì đó bị che" hoặc "có gì đó bị overlap":

1. **List z-index stack của TẤT CẢ elements.** Element có z-index cao (≥25) + full màn hình = che tất cả.
2. **Check opacity initial state.** Element có `opacity: 0` CSS không? Hay chỉ dựa vào GSAP `tl.fromTo()`?
3. **Check position absolute.** `top: 50% left: 50% transform translate(-50%, -50%) width: 80% height: 80%` = full màn hình từ frame 0.
4. **Check background opacity.** `background: rgba(0,0,0,0.92)` với 92% opacity = gần đặc → che visual content.
5. **Verify bằng cách trích PNG từ file final, sample pixel bounds TRỰC TIẾP.** KHÔNG dựa vào std pixel ở vùng khác (có thể là bg video).

## Verify Pre-Ship Command

```bash
# Check tất cả glass classes có opacity:0
grep -E '^\.[a-z-]+(glass|wrap|pill).*\{' index.html
grep -E 'opacity:' index.html | head -20
```

**Phải có:** mỗi glass class có `opacity: 0` line trong CSS block.

## Test pattern (để confirm rule)

```javascript
// Test 1: Element không có CSS opacity:0 → fail
const div = document.querySelector('.cta-glass');
console.log(div.style.opacity); // "" → opacity mặc định = 1

// Test 2: Element có CSS opacity:0 → success
const div2 = document.querySelector('.cta-glass');
console.log(getComputedStyle(div2).opacity); // "0"
```

## Apply khi nào

- Mọi element có `tl.fromTo(selector, { opacity: 0 }, ...)` PHẢI có CSS `opacity: 0`
- Đặc biệt quan trọng với element full màn hình (CTA 80%) hoặc z-index cao
- KHÔNG skip opacity:0 vì nghĩ GSAP sẽ handle — GSAP không tự apply initial state

## Em đã sai 5 lần trước đó

| Version | Báo cáo của em | Thực tế |
|---|---|---|
| V85 | "PIP limitation HyperFrames scrub" | ❌ CTA đè |
| V87 | "14/15 HR pass + 1 limitation" | ❌ CTA đè |
| V88 | "5 patterns V22 chính gốc" | ❌ V22 patterns đúng, CTA thiếu opacity |
| V89 | "Timeline length > 32s = FAILURE" | ❌ V10 work 32s vì CTA scale kèm |
| **V90** | **Anh đoán ĐÚNG — CTA đè** | ✅ |

## Lesson vĩnh viễn

1. **Khi element che full màn hình + z-index cao + background đậm → PHẢI có opacity:0 initial**
2. **GSAP tl.fromTo KHÔNG apply initial state trước render** — cần CSS hoặc GSAP set() trước
3. **Anh đoán z-index overlap → thường ĐÚNG** — check CSS z-index + opacity trước khi đoán pattern
4. **Verify bằng cách PNG extract + sample pixel bounds** — KHÔNG dựa std ở vùng khác
5. **Khi memory compacted, READ skill RECAP nhưng verify với FILE FINAL, không tin recap**
6. **Khi anh gợi ý root cause → verify nghiêm túc thay vì defend hypothesis cũ**