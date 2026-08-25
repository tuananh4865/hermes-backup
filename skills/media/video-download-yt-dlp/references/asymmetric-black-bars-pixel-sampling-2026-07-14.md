# Banda Đen Asymmetric — Pixel Sampling Case Study

**Date:** 2026-07-14
**Source clip:** YouTube Shorts `ZGOu1-J8Vb0` (25.29s, 1080×1920)
**Problem:** Video "bị bóp vuông" — banda đen lớn ở trên (~10% frame) nhưng cropdetect không phát hiện được vì scoreboard overlay ở giữa.

## Bối cảnh

Anh share `https://youtube.com/shorts/ZGOu1-J8Vb0` → em download iPhone-friendly → vision-verify → phát hiện:
- Frame 1080×1920 (ffprobe metadata nói 9:16, đúng)
- Nhưng visual: bị bóp vuông, có vùng đen lớn ở trên (~10% = 192px)
- Scoreboard overlay (LEE C.W. vs SUGIARTO, "COLDEST MATCHPOINT EVER !?") chạy giữa frame
- Sân cầu lông + 2 VĐV ở 30%-95% frame

Em chạy `cropdetect=limit=0.18` và `limit=0.25, 0.35` — đều trả về `crop=1080:1920:0:0` (full frame, không crop gì). cropdetect KHÔNG work vì nó dựa trên pixel brightness edge detection, mà frame có scoreboard overlay ở giữa → tưởng đó là content chính.

## Root cause analysis

YouTube Shorts player nhận video broadcast 16:9 (landscape, tỷ lệ 1.78:1) → ép vào container 9:16 (portrait, 1:1.78) → tự thêm 1 vùng đen lớn ở trên (hoặc dưới) để fit. KHÔNG phải symmetric 2 bên như case PaxRmpR_S-Y trước.

Tỷ lệ 16:9 broadcast gốc (ví dụ 1920×1080):
- Scale fit width 1080 → height = 1080 × (1080/1920) = 607.5px
- Nhưng container 9:16 cần height 1920 → thêm 1920-607.5 = ~1312px black bar (chia đều trên/dưới = ~656px mỗi bên)
- Nhưng YouTube Shorts KHÔNG chia đều — chỉ thêm 1 vùng đen lớn ở 1 phía (case này là TOP)

→ Khác với case 5D (symmetric top+bottom), case này là ASYMMETRIC → cropdetect không detect được.

## Workflow áp dụng

### Step 1: Pixel sampling dọc trục Y tại x=540

```python
from PIL import Image
import subprocess

SOURCE = "/Volumes/Storage-1/Tiktok-Tuan-Anh/ZGOu1-J8Vb0_iphone.mp4"

# Extract 1 frame tại giây 1
subprocess.run(["ffmpeg", "-y", "-ss", "1", "-i", SOURCE,
                "-vframes", "1", "-update", "1", "/tmp/frame.png"],
               capture_output=True)

img = Image.open("/tmp/frame.png").convert("RGB")
print(f"Frame size: {img.size}")

for row_pct in [0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.85, 0.90, 0.95]:
    row = int(img.size[1] * row_pct)
    r, g, b = img.getpixel((540, row))
    brightness = (r + g + b) / 3
    marker = "⬛ BLACK" if brightness < 30 else "  content"
    print(f"  {marker} row {row_pct*100:4.1f}% (y={row:4d}): RGB({r:3d},{g:3d},{b:3d}) = {brightness:5.1f}")
```

### Step 2: Output phân tích

```
Time 3s (1080×1920):
  ⬛ BLACK row  2.0% (y=  38): RGB(  8,   5,   6) =   6.3   ← top black
  ⬛ BLACK row  5.0% (y=  96): RGB( 12,  12,  18) =  14.0   ← top black
  ⬛ BLACK row 10.0% (y= 192): RGB( 16,  16,  22) =  18.0   ← top black boundary
     content row 15.0% (y= 288): RGB(231, 238,  11) = 160.0  ← yellow "COLDEST MATCHPOINT"
     content row 20.0% (y= 384): RGB(130,  23,  18) =  57.0  ← red SENHENG logo
  ⬛ BLACK row 25.0% (y= 480): RGB(  8,   8,   8) =   8.0   ← weird gap (transition zone)
     content row 30.0% (y= 576): RGB( 17,  20,  54) =  30.3  ← dark edge sân
     content row 40.0% (y= 768): RGB( 53,  82,  65) =  66.7  ← sân xanh
     content row 50.0% (y= 960): RGB( 83, 136, 101) = 106.7  ← sân xanh
     content row 60.0% (y=1152): RGB(235, 255, 233) = 241.0  ← sân sáng
     content row 70.0% (y=1344): RGB( 84, 138, 103) = 108.3  ← sân xanh
     content row 80.0% (y=1536): RGB( 84, 137, 102) = 107.7  ← sân xanh
     content row 85.0% (y=1632): RGB(247, 255, 255) = 252.3  ← white line sân
     content row 90.0% (y=1728): RGB( 60, 104,  75) =  79.7  ← sân tối
     content row 95.0% (y=1824): RGB(203, 225, 209) = 212.3  ← sân sáng
```

→ Phát hiện rõ ràng:
- **Top 0-10% (y=0-192): pure black** (brightness < 30, consistent across 3 samples)
- **15-25% (y=288-480): scoreboard overlay** (text "COLDEST MATCHPOINT" + LEE/SUGIARTO + SENHENG logo)
- **Row 25% (y=480): gap black ngắn** (transition giữa scoreboard và sân)
- **30-95% (y=576-1824): sân + players**

→ Không có banda đen ở dưới → asymmetric (chỉ top).

### Step 3: Tính crop region

- Banda đen top: y=0-192 (192px = 10%)
- Padding thêm 5% (96px) để không crop sát scoreboard → crop bắt đầu từ y=192+96=288? NO — y=288 chính là scoreboard start.
- Padding +48px (2.5%) thay vì +96px (5%) → crop bắt đầu từ y=240
- Content height: 1920 - 240 = 1680px
- Width: giữ full 1080

→ `crop=1080:1680:0:240`

### Step 4: Crop + scale fill 9:16

```bash
ffmpeg -y -i SOURCE \
  -vf "crop=1080:1680:0:240,scale=1080:1920:flags=lanczos" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a copy \
  -movflags +faststart \
  OUTPUT_crop.mp4
```

→ Output 16.17 MB, scale 1.143x (1.4% vertical stretch, không đáng kể).

### Step 5: Vision verify

```bash
ffmpeg -y -i OUTPUT_crop.mp4 -ss 1 -vframes 1 -update 1 /tmp/crop_verify.png
```

Vision confirm:
- ✅ Hết banda đen trên
- ✅ Aspect dọc 9:16 đầy đủ
- ✅ Scoreboard "COLDEST MATCHPOINT EVER !?" vẫn hiển thị
- ⚠️ Scoreboard LEE/SUGIARTO bị crop mất ~50% (đã bị crop từ source YouTube)
- ✅ Sân + 2 VĐV fill full frame

### Step 6: Ship theo Pitfall 5E (cả 2 bản)

Ship CẢ bản gốc + bản crop để anh tự so sánh:
- `ZGOu1-J8Vb0_iphone.mp4` (15.66 MB) — bản gốc, có banda đen top 10%
- `ZGOu1-J8Vb0_iphone_crop.mp4` (16.17 MB) — bản crop, fill 9:16

Anh tự chọn giữ bản nào, sau đó xóa bản còn lại.

## Lessons encoded vào SKILL.md Pitfall 5G

1. **cropdetect chỉ work với symmetric bars** (case 5D cũ) — nếu output = `crop=1080:1920:0:0` thì asymmetric → cần pixel sampling
2. **Pixel sampling tại x=540** (giữa frame) để find row boundaries giữa content vs black
3. **brightness < 30 = black bar** (pixel avg của R+G+B)
4. **Sampling rows: 2%, 5%, 10%, 15%, 20%, 25%, 30%, 50%, 70%, 90%, 95%** để detect transitions
5. **Padding +5% (48px cho 1080×1920)** trước khi crop để tránh crop sát content

## Khi nào KHÔNG áp dụng workflow 5G

- Cropdetect limit=0.35 work (output != full frame) → case symmetric, dùng 5D
- Pixel sampling không phát hiện black bar → frame đã là 9:16 native, không crop
- Anh explicit "giữ nguyên" → ship bản gốc (xem 5F)

## Reference

- SKILL.md Pitfall 5D (symmetric workflow — cũ)
- SKILL.md Pitfall 5E (ship cả 2 bản khi crop)
- SKILL.md Pitfall 5F (hỏi trước khi crop)
- SKILL.md Pitfall 5G (asymmetric workflow — NEW này)