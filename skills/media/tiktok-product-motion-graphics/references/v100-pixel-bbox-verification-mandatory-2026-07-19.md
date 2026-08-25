# PITFALL #100 — Pixel Bbox Verification MANDATORY (Em đã sai 5 lần 19/07)

> **Ngày**: 2026-07-19
> **Anh feedback**: *"Có khi nào em đang để phần nền đen nằm đè lên trên clip không? ... Vẫn chưa được!"*

---

## 🚨 ROOT CAUSE: Em đã báo "work" 5 lần dựa trên PIXEL STATS — ĐỀU SAI

Trong 19/07, em đã verify PIP work bằng cách check `bright%` hoặc `non-black%` ở vùng rộng (200×200 sample). Kết quả trông "OK" nhưng thực tế PIP vẫn blank hoặc che mặt.

**VÍ DỤ FAIL (V14-V16):**

| Metric V8 (báo work) | Thực tế anh check ảnh |
|---|---|
| bg brightness = 137 | Nhưng CTA-GLASS 80%×80% z-index:25 che toàn bộ |
| non-black 100% ở scale 0.42 | Nhưng CTA đè, scale 0.42 không work như mong đợi |
| borderRadius 28 set | Nhưng KHÔNG render trong HyperFrames |

**Bài học:**
- Stats có thể pass trong khi visual fail
- Pixel brightness sample ở vùng WRONG → false positive
- borderRadius GSAP keyframe KHÔNG render trong HyperFrames headless Chrome
- clipPath GSAP keyframe KHÔNG apply

---

## ✅ CORRECT VERIFICATION PROTOCOL

### Bước 1: Extract frame PNG ở các phase quan trọng

```bash
TIMES="1 5 8 10 12 15 18 20 22 25 27 30 35 45 55 70 85 95"
for t in $TIMES; do
  ffmpeg -y -ss $t -i output_final.mp4 \
    -frames:v 1 -vf scale=540:-1 \
    /tmp/v_verify/t$(printf "%02d" $t).jpg
done
```

### Bước 2: Find PIP bbox bằng pixel scan (KHÔNG dựa std)

```python
from PIL import Image
img = Image.open("/tmp/v_verify/t10.jpg")  # CHART phase

all_x, all_y = [], []
for y in range(50, 400):
    for x in range(20, 540):
        p = img.getpixel((x, y))
        if isinstance(p, tuple) and (p[0] > 30 or p[1] > 30 or p[2] > 30):
            all_x.append(x); all_y.append(y)

bbox = (min(all_x), min(all_y), max(all_x), max(all_y))
w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
ratio = w / h if h > 0 else 0

# Verify:
# bbox[0] nên ở góc trên-trái (~50 trong 540×960) nếu CHART top-left
# ratio nên ≈ 0.6-0.7 cho portrait shape (KHÔNG phải 1.0 vì scale 0.42 → portrait PIP)
assert bbox[0] < 100, "PIP không ở top-left!"
assert 0.5 < ratio < 0.8, "PIP ratio sai!"
```

### Bước 3: VISION_ANALYZE từ PNG

```python
image_analyze("/tmp/v_verify/t10_CHART.png",
    question="PIP ở vị trí nào? Có mặt người không? Bên trong có gì?")
```

→ Vision trả lời phải đúng:
- "PIP ở góc trên-trái"
- "Có mặt người rõ ràng"
- "Có glass card"

---

## ❌ ANTI-PATTERNS (đừng bao giờ verify bằng cách này)

### ❌ Không check std ở giữa khung hình
```python
# SAI: Center pixel có std cao không có nghĩa PIP work
center_std = ...
assert center_std > 30  # ← sai vì có thể CTA đè
```

### ❌ Không dựa borderRadius hoặc clipPath trong GSAP
```javascript
// SAI: borderRadius KHÔNG render trong HyperFrames headless Chrome
tl.to(videoClip, { scale: 0.42, x: -222, y: -540, borderRadius: 28, ... });
// Visual sẽ KHÔNG có bo góc dù borderRadius set

// SAI: clipPath KHÔNG apply
tl.to(videoClip, { clipPath: 'inset(193px 16.5px 193px 16.5px)', ... });
// Visual sẽ KHÔNG được crop vuông dù clipPath set
```

### ❌ Không báo "work" khi chỉ sample 1 region
```python
# SAI: 1 region duy nhất
sample = img.crop((100, 800, 200, 900))  # bg + face border
avg = sum(sum(p) for p in sample) / ...
# Nếu region này OK → chỉ chứng minh region này OK, KHÔNG chứng minh PIP work
```

---

## ✅ CORRECT VERIFICATION CHECKLIST

Trước khi ship clip, PHẢI:

- [ ] Extract PNG ở ≥ 12 timestamps (đặc biệt phase PIP active + phase ngoài)
- [ ] VISION_ANALYZE mỗi PNG để verify visually
- [ ] PIXEL BBOX SCAN ở PIP bounds — verify bbox nằm ở đúng vị trí mong đợi
- [ ] Verify mặt hiện rõ (vision confirm)
- [ ] Verify phần ngoài PIP = background đen (nếu V13 method)
- [ ] Verify CTA 80% chỉ che ở 90-100s, KHÔNG che full video

---

## 🚨 ROOT CAUSE INVESTIGATION CHECKLIST (khi anh flag lạ)

Khi anh nói "có gì đó bị che/overlap/lạ":

1. **List z-index của TẤT CẢ elements**
   - Element z-index cao + full màn hình = che tất cả
   - CTA 80%×80% + z-index 25 = che full

2. **Check opacity initial state**
   - KHÔNG chỉ dựa GSAP tl.fromTo()
   - PHẢI có `opacity: 0` trong CSS initial

3. **Check position absolute**
   - `top:50% left:50% transform translate(-50%,-50%)` + `width:80% height:80%` = full màn hình từ frame 0

4. **Check background opacity**
   - `rgba(0,0,0,0.92)` = gần đặc → che visual content

5. **Verify by PNG extract + sample PIXEL BOUNDS (TRỰC TIẾP bên trong element)**
   - KHÔNG dựa std pixel ở vùng khác

6. **ĐỪNG kết luận "limitation" khi chưa forensic source**
   - Em đã sai ở V85, V87, V88, V89 vì kết luận vội
   - ALWAYS đọc source HTML/JS trước khi báo limitation

---

## 📋 LEARNINGS TỪ 5 LẦN FAIL

| Version | Em báo | Thực tế | Sai ở đâu |
|---|---|---|---|
| V85 | "HyperFrames scrub 1 frame" | V22 work, em sai pattern | Không đọc source HTML |
| V87 (V7) | "14/15 HR pass + 1 limitation" | CTA đè mọi phase | Không check z-index |
| V88 (V8) | "5 patterns V22 chính gốc fix" | Patterns đúng, CTA đè vẫn | Không verify bằng ảnh |
| V89 (V10) | "Timeline > 32s = FAIL" | V10 work 32s, V8 fail do CTA | Không empirical test trước |
| V90 (V11) | "CTA fix work" | Work! Anh đoán đúng từ đầu | OK |

---

## ✅ CORRECT FINAL VERIFICATION

```python
# Bước 1: Extract PNG
subprocess.run(["ffmpeg", "-y", "-ss", str(t), "-i", video_path,
                "-frames:v", "1", "-vf", "scale=540:-1",
                f"/tmp/v_{t}.jpg"])

# Bước 2: Pixel bbox scan
img = Image.open(f"/tmp/v_{t}.jpg")
# Find PIP bounds by scanning top portion
bbox = scan_top_for_pip(img)

# Bước 3: Visual verification
result = vision_analyze(f"/tmp/v_{t}.jpg",
    "Mô tả chi tiết: PIP ở đâu? Có mặt người không? Bên trong có gì?")

# Bước 4: Cross-verify
expected = {
    10: "PIP top-left + mặt rõ",
    22: "PIP top-right + mặt rõ",
    95: "CTA 80% covers",
}
assert result.contains(expected[t]), f"MISMATCH at t={t}"
```

---

## 🎯 ANTI-PATTERN: Std theater

```python
# ❌ Em đã làm 5 lần — KHÔNG BAO GIỜ nữa
def is_pip_work(brightness_at_center):
    return brightness_at_center > 100  # ← FALSE POSITIVE

# ✅ ĐÚNG
def is_pip_work(pip_bbox, expected_position):
    """Verify by exact bbox match expected position"""
    x_center = (pip_bbox[0] + pip_bbox[2]) / 2
    y_center = (pip_bbox[1] + pip_bbox[3]) / 2
    expected_x, expected_y = expected_position
    distance = ((x_center - expected_x)**2 + (y_center - expected_y)**2) ** 0.5
    return distance < 50  # within 50 pixels of expected
```

---

## 📚 RELATED FILES

| File | Purpose |
|---|---|
| `references/v18-pip-method-chinh-thuc.md` | V18 method spec - chi tiết pattern |
| `references/v97-pip-square-rounded-wrapper-method.md` | Wrapper approach cho PIP vuông |
| `references/v90-gsap-fadein-opacity-zero-rule-2026-07-19.md` | GSAP fade-in opacity:0 rule |
| `references/v88-pip-pattern-chinh-goc-5-fixes-2026-07-19.md` | 5 patterns V22 PIP chính gốc |

---

*PITFALL #100 — pixel bbox verification mandatory. Em đã sai 5 lần dựa std theater. NEVER báo "work" khi chưa VISION_ANALYZE PNG thực tế + verify bbox bằng pixel scan.*
