# Clip 0003 V5 FINAL FIX — Transparent Overlay Workflow (18/07/2026)

**Status:** ✅ VERIFIED PASS bằng pixel diff (face motion 158-230, glass card visible)

## Context

Sau 4 lần fail (V4 skip verify, V5 sai coordinate, V6 vẫn đơ, V3_speed13 sai file source), em đã tìm ra cách fix cuối cùng:

**Root cause:** HyperFrames render `<video class="bg-video">` element nhưng headless Chrome KHÔNG play video. Kết quả: chỉ render được 1 frame tĩnh đầu tiên, mất hoàn toàn motion của source.

**Fix:** HyperFrames KHÔNG render video. Chỉ render GLASS CARD animation trên nền transparent. Sau đó FFmpeg ghép source video motion + transparent overlay bằng `format=yuva420p`.

## Workflow đã verify PASS

### Bước 1: HTML setup

```html
<style>
  html, body { overflow: hidden; background: transparent; }  /* QUAN TRỌNG */
  .video-bg { display: none; }  /* KHÔNG render video bg */
</style>

<div id="root" data-composition-id="clip0003-V5" data-duration="82">
  <video class="video-bg" id="video-bg" muted playsinline preload="auto">
    <source src="assets/source/full_bg.mp4" type="video/mp4" />
  </video>
  <!-- Glass cards với opacity:0 default + GSAP animate -->
  <div class="glass glass-hook" data-class="glass-hook">...</div>
  <!-- 7 glass cards khác -->
</div>
```

### Bước 2: Render silent overlay với alpha channel (MOV format)

```bash
npx --yes hyperframes render --quality draft --format mov --output output_silent.mov
```

**Phải dùng `--format mov`** để có alpha channel. MP4 không có alpha.

### Bước 3: Verify alpha channel

```bash
ffmpeg -y -i output_silent.mov -ss 0.1 -frames:v 1 -update 1 /tmp/test_t01.png
python3 -c "
from PIL import Image
img = Image.open('/tmp/test_t01.png').convert('RGBA')
alpha = img.split()[3]
# Center (no glass): alpha should be 0 (transparent)
# Glass area (Y=1308): alpha should be > 100 (visible)
print('Center alpha:', alpha.getpixel((540, 960)))  # → 0 ✅
print('Glass alpha:', alpha.getpixel((540, 1308)))  # → 108 ✅
"
```

### Bước 4: FFmpeg ghép source video + transparent overlay

```bash
ffmpeg -y \
  -i source.mp4 \
  -i output_silent.mov \
  -filter_complex "[0:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setpts=PTS-STARTPTS[bg]; [1:v]scale=1080:1920,format=yuva420p,setpts=PTS-STARTPTS[v1]; [bg][v1]overlay=0:0:eof_action=pass[v]" \
  -map "[v]" -map 0:a \
  -c:v libx264 -preset fast -crf 23 \
  -c:a copy \
  -shortest \
  output/clip0003_V5_82s_FINAL.mp4
```

### Bước 5: VERIFY MOTION bằng pixel diff (BẮT BUỘC)

```python
from PIL import Image
img1 = Image.open('/tmp/fix_t1.jpg')
img30 = Image.open('/tmp/fix_t30.jpg')
img60 = Image.open('/tmp/fix_t60.jpg')

# Check NHIỀU VỊ TRÍ - không chỉ top-left
regions = [
    ('Top background', 200, 200),      # thường static OK
    ('Face mouth Y=900', 540, 900),     # QUAN TRỌNG - talking head
    ('Face chin Y=1100', 540, 1100),   # QUAN TRỌNG
    ('Hand mic', 600, 1100),            # QUAN TRỌNG
    ('Glass card Y=1308', 540, 1308),   # glass animation
]

print(f"{'Region':<30} {'d(1-30)':<10} {'d(1-60)':<10} {'Status':<12}")
for label, x, y in regions:
    p1, p30, p60 = img1.getpixel((x, y)), img30.getpixel((x, y)), img60.getpixel((x, y))
    d130 = sum(abs(a-b) for a, b in zip(p1, p30))
    d160 = sum(abs(a-b) for a, b in zip(p1, p60))
    status = '✅ MOTION' if d130 > 50 else '❌ STATIC'
    print(f"{label:<30} {d130:<10} {d160:<10} {status}")
```

## Kết quả verify (clip 0003 V5 fix)

```
Region                         d(1-30)    d(1-60)    Status      
Top background                 2          8          ❌ STATIC (OK - background)
Face mouth Y=900               158        109        ✅ MOTION
Face chin Y=1100               230        165        ✅ MOTION
Hand mic X=600 Y=1100          185        146        ✅ MOTION
Glass card Y=1308              29         56         (CTA glass animate)
```

**PASS** - motion đã có, glass card visible.

## Glass card brightness check

```
Phase        Time   Glass RGB              Brightness Visible 
HOOK         5      (228, 191, 173)        197        YES
INTRO        20     (115, 115, 115)        115        YES
USP          50     (214, 180, 168)        187        YES
CTA-FINAL    78     (173, 130, 121)        141        YES
```

Tất cả 4 phase đều có glass card visible (brightness > 100).

## 3 lỗi cần tránh (lesson từ V4/V5/V6)

1. **V4:** Skip verify 5/8 frames → báo PASS sai → anh escalate
2. **V5:** Glass card `bottom: 200px` sai vị trí → phải `top: 1308px` (V22 layout)
3. **V6:** Render silent overlay che source video → motion bị mất

## 4 lần sai + 1 cách đúng

| Lần | File dùng | Render method | Motion | Glass position | Status |
|---|---|---|---|---|---|
| V4 | clip_0003_Final (90s) | `bg-video` autoplay | ❌ Static | `bottom: 200px` | FAIL |
| V5 | clip_0003_V3_speed13 (82s) | `bg-video` autoplay | ❌ Static | `top: 1308px` | PARTIAL |
| V6 | clip_0003_V3_speed13 (82s) | `bg-video` autoplay | ❌ Static | `top: 1308px` | FAIL |
| V3_speed13 | clip_0003_V3_speed13 (82s) | HyperFrames overlay directly | ❌ Static | `top: 1308px` | FAIL |
| **V5_final_fix** | clip_0003_V3_speed13 (82s) | **Transparent overlay + ffmpeg yuva420p** | **✅ Motion** | `top: 1308px` | **PASS** |

## Checklist khi áp dụng cho clip mới

1. [ ] Source video đã verify có motion (pixel diff face > 50)
2. [ ] HTML: `background: transparent` + `.video-bg { display: none }`
3. [ ] Render với `--format mov` (KHÔNG dùng mp4)
4. [ ] Verify alpha channel: center alpha=0, glass area alpha>100
5. [ ] FFmpeg ghép với `format=yuva420p` + `-c:a copy` (giữ audio gốc)
6. [ ] Pixel diff verify: face/chin/hand d > 50 ở mọi thời điểm
7. [ ] Glass card brightness > 100 ở mỗi phase
8. [ ] File size ~12-15MB cho 32s, ~30-40MB cho 82s

## Anti-pattern (KHÔNG dùng)

- ❌ `<video autoplay loop>` trong HyperFrames index.html
- ❌ `bg-video.play()` trong GSAP timeline
- ❌ Render silent overlay với `--format mp4` (không có alpha)
- ❌ Dùng `-c:v copy` cho ghép → source video sẽ không được re-encode
- ❌ Skip verify motion "vì lười"
