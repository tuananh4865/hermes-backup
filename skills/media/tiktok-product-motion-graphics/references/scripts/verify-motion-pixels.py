# Verify Motion đúng cách - Pixel Diff Toolkit

**Toolkit chính xác để verify motion trong HyperFrames render tránh 4 lỗi fail của clip 0003.**

## Setup

```bash
# Extract 4-5 frames ở các thời điểm khác nhau
ffmpeg -y -i clip.mp4 -ss 1 -frames:v 1 -update 1 -q:v 2 /tmp/verify_t1.jpg
ffmpeg -y -i clip.mp4 -ss 20 -frames:v 1 -update 1 -q:v 2 /tmp/verify_t20.jpg
ffmpeg -y -i clip.mp4 -ss 45 -frames:v 1 -update 1 -q:v 2 /tmp/verify_t45.jpg
ffmpeg -y -i clip.mp4 -ss 65 -frames:v 1 -update 1 -q:v 2 /tmp/verify_t65.jpg
```

## Python script

```python
from PIL import Image

def verify_motion(frames_paths, regions=None):
    """Verify motion bằng pixel diff ở nhiều vị trí.

    Args:
        frames_paths: list of file paths, e.g. ['/tmp/v_t1.jpg', '/tmp/v_t30.jpg']
        regions: list of (label, x, y) tuples. Default: face/chin/hand.

    Returns:
        dict mapping region_label -> list of diffs between consecutive frames
    """
    if regions is None:
        regions = [
            ('Top background (Y=200 X=200)', 200, 200),
            ('Face mouth (Y=900)', 540, 900),
            ('Face chin (Y=1100)', 540, 1100),
            ('Hand mic (X=600 Y=1100)', 600, 1100),
            ('Glass card (Y=1308)', 540, 1308),
        ]

    imgs = [Image.open(p) for p in frames_paths]
    results = {}

    for label, x, y in regions:
        diffs = []
        for i in range(len(imgs) - 1):
            p1 = imgs[i].getpixel((x, y))
            p2 = imgs[i + 1].getpixel((x, y))
            d = sum(abs(a - b) for a, b in zip(p1, p2))
            diffs.append(d)
        results[label] = diffs

    return results


def report_motion(results, threshold=50):
    """Print motion report. PASS = diff > threshold ở face/chin/hand."""
    print(f"{'Region':<40} {' '.join(f'd{i}-i{i+1}' for i in range(len(results[list(results.keys())[0]]))):<25} {'Status':<12}")
    print("=" * 85)

    for label, diffs in results.items():
        status = "MOTION" if max(diffs) > threshold else "STATIC"
        diff_str = " ".join(f"{d:>5}" for d in diffs)
        print(f"{label:<40} {diff_str:<25} {status:<12}")

    print()
    print("Threshold: d > 50 = MOTION PASS, d < 10 = FAIL")
    print("Verify o face/chin/hand, KHONG o top background (thuong static OK)")
    print("Glass card area co animation GSAP nen diff se cao du source static")
```

## Cách dùng

```python
# Verify final clip sau khi ghép source + overlay
results = verify_motion(['/tmp/v_t1.jpg', '/tmp/v_t30.jpg', '/tmp/v_t60.jpg'])
report_motion(results)
```

Output mẫu (V5 final fix clip 0003):

```
Region                                   d0-1 d1-2  Status
=====================================================================================
Top background (Y=200 X=200)              2    8   STATIC
Face mouth (Y=900)                       158  109   MOTION
Face chin (Y=1100)                      230  165   MOTION
Hand mic (X=600 Y=1100)                 185  146   MOTION
Glass card (Y=1308)                      29   56   (CTA glass animate)
```

## Threshold chuẩn

| Diff value | Status | Action |
|---|---|---|
| > 50 | MOTION | PASS - ship OK |
| 10-50 | MARGINAL | Verify thêm ở nhiều vùng khác |
| < 10 | STATIC | FAIL - source clip bị đơ hoặc HyperFrames render sai |

## 4 lỗi cần tránh (lesson từ clip 0003 V4-V6)

1. Chi check o top-left corner - background thuong static, khong phat hien motion
2. Check vung co glass overlay - motion do GSAP animate, KHONG phai source
3. Chi check 1 frame - phai check NHIEU frame lien tiep (1s, 20s, 45s, 65s)
4. Skip verify - phai PASS 100% tat ca frame truoc khi ship

## Verify source motion TRƯỚC KHI render HyperFrames

```bash
# Check source video co motion that khong (talking head)
for src in source.mp4 V2.mp4 V3.mp4 V3_speed13.mp4; do
  ffmpeg -ss 1 -i "$src" -frames:v 1 -update 1 frame_t1.jpg
  ffmpeg -ss 30 -i "$src" -frames:v 1 -update 1 frame_t30.jpg
  python3 -c "
from PIL import Image
img1 = Image.open('frame_t1.jpg')
img30 = Image.open('frame_t30.jpg')
d_face = sum(abs(a-b) for a, b in zip(img1.getpixel((540, 900)), img30.getpixel((540, 900))))
d_chin = sum(abs(a-b) for a, b in zip(img1.getpixel((540, 1100)), img30.getpixel((540, 1100))))
status = 'MOTION' if d_face > 50 or d_chin > 50 else 'STATIC'
print('$src: face d=$d_face chin d=$d_chin $status')
"
done
```

Nếu source STATIC (diff < 50 ở mọi vùng):
- BAO CAO TRUNG THUC cho user: "Source talking head gan nhu static do micro-movement"
- VAN ship duoc vi glass overlay animate compensate
- KHONG noi "video bi do" khi source goc khong co motion nhieu
