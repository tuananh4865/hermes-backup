---
name: video-download-yt-dlp
title: Media Download & Resend via Telegram
description: Download video/image files from known URLs (YouTube, TikTok, Facebook, Wikimedia Commons, direct image URLs) using yt-dlp or curl, verify with ffprobe/file AND vision tool, and resend as native Telegram media. Use when Tuấn Anh sends a media link and wants the file back (not just analysis). Covers video platforms via yt-dlp AND direct image/CDN URLs via curl — both end with the same MEDIA:/path resend pattern. ALWAYS pre-flight fact-check timeline (person active? object released?) AND vision-verify every image for multi-attribute matches (person + equipment + context) BEFORE sending to user. Filename is NOT content. Max 2 retry rounds on the same request — reframe with options if both fail. For multi-attribute "person + object" searches, refuse upfront if the combination doesn't exist (e.g. retired player + new product).
created: 2026-06-13
updated: 2026-07-14
type: skill
patch_count: 8
tags: [media, download, yt-dlp, curl, telegram, youtube, tiktok, image, wikimedia, facebook]
confidence: high
---

# Media Download & Resend Workflow

When Tuấn Anh gửi một media link (video từ YouTube/Shorts/TikTok/Facebook share/reel, HOẶC ảnh từ Wikimedia Commons / direct image URL), workflow chuẩn là:
**Download → Verify → Resend as Telegram media attachment** (KHÔNG chỉ analyze).

## Tại sao workflow này quan trọng

- Telegram gateway chỉ pass text/links, KHÔNG pass binary media. Em không "xem" được video/ảnh anh gửi attachment.
- Khi anh gửi **link**, em download được bằng yt-dlp (video) hoặc curl (ảnh) → gửi file về qua `MEDIA:/path` → anh xem trên Telegram.
- Đây là pattern anh dùng 100% mọi lần cho cả video và ảnh (xem memory: "yt-dlp → send MEDIA:/path → works 100%").
- Ảnh: dùng `curl` + verify bằng `file` command. Video: dùng `yt-dlp` + verify bằng `ffprobe`. Cùng chung verify-resend pipeline.

## Khi nào dùng tool nào

| Source | Tool | Verify command |
|---|---|---|
| YouTube, YouTube Shorts, TikTok, Facebook reel, generic streaming | `yt-dlp` | `ffprobe` |
| Wikimedia Commons, direct image URL, CDN image, GitHub avatar | `curl` | `file` (check `JPEG image data` / `PNG image data`) |
| Any URL with file extension (.jpg, .png, .mp4) | `curl` first, fall back to yt-dlp if `file` says HTML | `file` or `ffprobe` |

**Decision rule:** nếu URL có streaming token (m3u8, HLS, manifest) → yt-dlp. Nếu URL point thẳng tới file binary → curl.

---

# PART 1: VIDEO WORKFLOW (yt-dlp)

## Standard Workflow

### Step 1: Pick the right format
```bash
yt-dlp -F "URL"
```

**Decision matrix:**
- **Long video (regular YouTube)**: pick highest resolution with audio (e.g. `137+140` cho 1080p video-only + best audio, hoặc `22`/`18` cho combined)
- **YouTube Shorts**: thường chỉ có m3u8 HLS streams. Pick `96` (1080p) hoặc `95` (720p) — chọn variant có audio
- **TikTok**: thường có format `h264` + `aac` ready-to-play

### Step 2: Download
```bash
cd ~/Downloads
yt-dlp -f <FORMAT_ID> --merge-output-format mp4 \
  -o "VIDEO_ID.%(ext)s" "URL"
```

**Filename convention:** `VIDEO_ID.mp4` (11-char YouTube ID hoặc TikTok video ID). KHÔNG dùng tên dài.

### Step 3: Verify with ffprobe
```bash
ffprobe -v error \
  -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate \
  -of default=noprint_wrappers=1 FILE.mp4
```

**Sanity checks:**
- `duration` > 0 (tránh file rỗng)
- `width` x `height` hợp lý (Shorts = 1080x1920, normal YouTube = 1920x1080 hoặc 1280x720)
- Có `codec_name=h264` (video) và `aac` (audio) — Telegram play được

**Red flag:** Nếu file < 200KB mà video > 10s → có thể chỉ tải được 1-2 fragment của HLS. Re-download với format khác.

### Step 4: Resend via Telegram
```
MEDIA:/Users/tuananh4865/Downloads/VIDEO_ID.mp4
```

**Telegram limits:**
- Timeout > 50MB → luôn compress nếu file lớn
- 720p H.264 + AAC thường đủ nhẹ (< 50MB cho video < 10 phút)
- Shorts thường < 10MB, không cần compress

---

## Step 4b: iPhone-friendly format + canonical save folder (2026-07-12, NEW)

**Anh's verbatim rule (2026-07-12):** *"Luôn luôn lưu clip cầu lông vào folder tiktok-tuan-anh rồi gửi vào tele cho anh, convert thành định dạng phù hợp với iphone rồi hãy gửi nhé"*

### Canonical save folder
```
/Volumes/Storage-1/Tiktok-Tuan-Anh/
```
- **Canonical path** cho MỌI clip cầu lông / TikTok content anh muốn archive. Folder đã tồn tại (verified 2026-07-12, có 60+ items sẵn).
- KHÔNG save vào `~/Downloads/` rồi để đó — anh muốn mọi clip cầu lông centralized trong folder này để quản lý + upload TikTok Shop.
- Folder alternate case `/Volumes/Storage-1/tiktok-tuan-anh` (lowercase) CÓ THỂ tồn tại trên macOS APFS (case-insensitive volume) nhưng **canonical path phải dùng capital "T"** như đã verify.

### iPhone-friendly format spec
Anh mở clip trên iPhone (Photos app, CapCut, iMovie). Phải đúng chuẩn iOS native để play ngay, không cần convert lại:

| Field | Spec BẮT BUỘC | Lý do |
|---|---|---|
| **Video codec** | H.264 (libx264, `-c:v libx264`) | iOS native, KHÔNG phải AV1/HEVC |
| **Audio codec** | AAC (`-c:a aac -b:a 128k`) | iOS native, KHÔNG phải Opus/FLAC |
| **Container** | MP4 | iOS native, mở được trên Photos/CapCut |
| **`+faststart`** | `-movflags +faststart` | Stream-friendly, click play là chạy ngay |
| **Resolution** | Giữ nguyên source (1080×1920 cho Shorts, 1920×1080 cho landscape) | Không scale, giữ detail |
| **CRF** | 23 (default medium, balance size vs quality) | Reasonable file size cho Shorts |
| **Preset** | `fast` (encode nhanh, không cần `slow` cho mobile playback) | Trade-off nhỏ |

### Canonical yt-dlp command cho clip cầu lông / TikTok content

```bash
yt-dlp \
  -f "bv*[ext=mp4][vcodec^=avc]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b" \
  --merge-output-format mp4 \
  --remux-video mp4 \
  --postprocessor-args "ffmpeg:-c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -movflags +faststart" \
  -o "/Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO_ID>_iphone.%(ext)s" \
  "<URL>"
```

**Pipeline flow:**
1. yt-dlp tải source video + audio về `.f299.mp4` (video) + `.f140.m4a` (audio) ở folder canonical
2. Merge thành `<VIDEO_ID>_iphone.mp4` (H.264 + AAC, đúng spec iPhone)
3. Source files tự động bị xoá sau merge (clean disk)

**Filename convention:** `<VIDEO_ID>_iphone.mp4` — giữ ID gốc để trace + suffix `_iphone` để biết đã convert.

### Verify spec iPhone-friendly (PASS criteria)
```bash
ffprobe -v error -show_entries stream=codec_name,codec_type,width,height,sample_rate \
  -show_entries format=duration,size,bit_rate,format_name \
  -of default=nw=1 "/Volumes/Storage-1/Tiktok-Tuan-Anh/<FILE>.mp4"
```
**Expected output (PASS):**
```
codec_name=h264          # ✅ H.264, không phải av1/hevc
codec_type=video
width=1080
height=1920              # ✅ Vertical Shorts format
codec_name=aac           # ✅ AAC
codec_type=audio
sample_rate=44100        # ✅ 44.1kHz
format_name=mov,mp4,...  # ✅ MP4 container
```

**RED flag (FAIL):**
- `codec_name=av1` hoặc `hevc` → KHÔNG iPhone-friendly, phải re-encode
- `sample_rate=48000` hoặc khác 44100 → OK cho iPhone nhưng TikTok spec strict 44100
- `format_name=` không có `mp4` → container sai

### Anti-pattern (TUYỆT ĐỐI KHÔNG)
- ❌ Save clip cầu lông vào `~/Downloads/` rồi để đó — sai folder canonical
- ❌ Download AV1/HEVC rồi ship thẳng — iPhone không play native, phải convert
- ❌ Skip `-movflags +faststart` — Telegram/iPhone stream bị delay đầu
- ❌ Re-encode 720p khi source 1080p — mất quality không cần thiết
- ❌ Quên verify bằng ffprobe trước khi gửi — em bịa "đã iPhone-friendly" mà thực tế codec AV1
- ❌ **TỰ Ý crop banda đen sau khi vision-verify** — anh có thể muốn giữ nguyên bản gốc YouTube (xem Pitfall 5F). Workflow 5D chỉ apply khi anh explicit yêu cầu crop/scale/fill 9:16.

### 5D. ⚠️ Black bars / letterbox sau khi convert 16:9 → 9:16 (2026-07-12, NEW — FIRST-CLASS pitfall)

**⚠️ QUAN TRỌNG 2026-07-14:** Workflow 5D này **KHÔNG auto-apply**. Banda đen có thể là gốc YouTube Shorts (16:9 broadcast ép vào 9:16) — anh có thể muốn giữ nguyên. **DEFAULT: giữ bản gốc, chỉ convert codec iPhone-friendly.** Workflow 5D chỉ chạy khi anh explicit yêu cầu crop/scale/fill 9:16. Xem **Pitfall 5F** để biết scope decision tree trước khi apply 5D.

**Triệu chứng:** Em convert clip cầu lông YouTube Shorts sang iPhone-friendly format (H.264/AAC/+faststart, 1080×1920). ffprobe verify PASS: `width=1080 height=1920 display_aspect_ratio=9:16`. Em báo "đã đúng 9:16, anh mở file xem nhé". Anh mở file trên iPhone → **thấy 2 banda đen lớn ở trên + dưới** (chiếm ~15-20% chiều cao mỗi bên). Anh flag: *"Mỗi lần em convert nó lại thành định dạng vuông là sao"*.

**Root cause — Tại sao clip lại có banda đen:**

YouTube Shorts player nhận video 16:9 (landscape) gốc từ broadcast (badminton HSBC, YONEX Tour, v.v.) → ép vào container 9:16 (portrait) → tự động thêm 2 vùng đen trên/dưới để fit tỷ lệ mà KHÔNG crop content. Khi em tải về bằng yt-dlp, video source ĐÃ CÓ SẴN banda đen này. Re-encode qua H.264/AAC chỉ thay codec, không crop.

ffprobe báo 9:16 vì cả frame 1080×1920 BAO GỒM cả 2 vùng đen — display_aspect_ratio chỉ là ratio của toàn frame, không phải ratio của content bên trong.

**Workflow 5D (chỉ chạy khi anh explicit yêu cầu crop):**

**Bước 1: Detect vùng content thực sự (cropdetect)**
```bash
ffmpeg -i "<SOURCE>.mp4" -vf cropdetect -t 5 -f null - 2>&1 | grep "crop=" | head -3
# Output mẫu: crop=1072:1568:4:348
# → Content thực sự: w=1072, h=1568, bắt đầu từ x=4, y=348
# → Banda đen: trên 348px, dưới (1920-348-1568)=4px (gần như zero)
```

**Bước 2: Crop + scale to 9:16 chuẩn TikTok**
```bash
ffmpeg -y -i "<SOURCE>.mp4" \
  -vf "crop=1072:1568:4:348,scale=1080:1920:flags=lanczos" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a copy \
  -movflags +faststart \
  "<OUTPUT>_crop.mp4"
# Lưu ý: -c:a copy để giữ audio nguyên (đã AAC sẵn từ pipeline trước)
# scale 1.4% (1072→1080, 1568→1920) để fill chuẩn 9:16
```

**Bước 3: VISUAL VERIFY (không chỉ tin ffprobe!)**
```bash
# Extract 1 frame ở giây giữa
ffmpeg -y -i "<OUTPUT>_crop.mp4" -vframes 1 -ss 1 -update 1 "/tmp/aspect_check.png"

# Load qua vision_analyze
# Question: "Còn banda đen trên/dưới không? Hình đã fill full 9:16 chưa? Có content bị crop oan không?"
```
PASS khi vision confirm: "không còn banda đen, content fill full 9:16, không có nội dung chính bị crop".

**Cleanup & rename:**
```bash
# Xoá file cũ (có banda đen) để khỏi confuse anh
rm "<SOURCE>_iphone.mp4"
mv "<SOURCE>_iphone_crop.mp4" "<SOURCE>_iphone.mp4"
```

**Verify cuối (3-layer):**
| Layer | Tool | PASS criteria |
|---|---|---|
| Structural | `ffprobe` | width=1080 height=1920, h264+aac, 44100Hz |
| Aspect | `ffprobe display_aspect_ratio` | 9:16 |
| **Visual** | `vision_analyze` 1 frame extracted | Không còn banda đen, content fill 9:16 |

**Anti-pattern tuyệt đối KHÔNG:**
- ❌ Ship file ngay sau khi re-encode chỉ vì ffprobe PASS 9:16 — ffprobe metadata KHÔNG phát hiện banda đen bên trong frame
- ❌ Chỉ tin display_aspect_ratio — đó là ratio toàn frame, không phải ratio content
- ❌ Scale lên 1080×1920 mà KHÔNG crop trước → giữ nguyên banda đen
- ❌ Dùng `pad` filter thay vì `crop` → vẫn còn banda đen
- ❌ Bỏ qua bước visual verify → em bịa "đã hết banda đen" mà thực tế vẫn còn

**Khi nào KHÔNG áp dụng workflow này:**
- Source đã là 9:16 (YouTube Shorts từ mobile upload native) → không có banda đen, không cần crop
- Source 1:1 (Instagram square) → crop 2 bên trái/phải, không phải trên/dưới
- Source 16:9 + anh muốn giữ nguyên letterbox (artistic intent) → KHÔNG crop

**Real case 2026-07-12 (PaxRmpR_S-Y badminton clip):**
- Source: YouTube Shorts `PaxRmpR_S-Y` 46.88s — gốc 1080×1920 (16:9 broadcast ép vào 9:16, có banda đen trên+dưới ~348px mỗi bên)
- Workflow sai (lần 1): yt-dlp re-encode H.264/AAC → ffprobe báo 9:16 → em báo "đã đúng 9:16" → anh thấy vuông + banda đen
- Workflow đúng (lần 2): cropdetect → `crop=1072:1568:4:348` → scale `1080:1920` → ffprobe PASS 9:16 → vision_analyze frame trung tâm confirm "không còn banda đen, content badminton rõ ràng" → ship OK
- Final: `/Volumes/Storage-1/Tiktok-Tuan-Anh/PaxRmpR_S-Y_iphone.mp4` 28.97 MB, 1080×1920, H.264/AAC/+faststart, không banda đen

### 5E. ⚠️ Khi crop banda đen → gửi CẢ bản gốc + bản crop để anh so sánh (2026-07-12, NEW)

**Signal từ anh (verbatim 2026-07-12, Telegram):** *\"Thử gửi bản gốc không convert xem\"*

**Bối cảnh:** Sau khi em crop banda đen + scale 9:16 (fix 5D), anh muốn em **gửi cả bản gốc (không convert)** để tự so sánh. Đây là pattern: anh muốn xác nhận visual diff giữa 2 phiên bản trước khi accept.

**Workflow khi crop/scale:**

1. **KHÔNG xoá file gốc** ngay khi crop xong — anh có thể muốn so sánh.
2. **Đặt tên 2 file rõ ràng:**
   - `<VIDEO_ID>_ORIGINAL.mp4` — bản gốc từ YouTube (có banda đen nếu source 16:9)
   - `<VIDEO_ID>_iphone.mp4` — bản đã crop + scale + convert iPhone-friendly
3. **Khi ship, embed `MEDIA:` cho CẢ HAI trong cùng reply** + table so sánh spec:
   ```markdown
   MEDIA:/path/to/<VIDEO_ID>_ORIGINAL.mp4   ← bản gốc, có banda đen
   
   MEDIA:/path/to/<VIDEO_ID>_iphone.mp4     ← bản fix, fill 9:16 sạch
   ```
4. **Cleanup SAU khi anh confirm** (không tự xoá):
   - Nếu anh accept bản `_iphone` → giữ lại, xoá `_ORIGINAL` (đã đối chiếu xong)
   - Nếu anh vẫn thấy sai → giữ cả 2, hỏi approach khác

**Command reference để download bản gốc không re-encode:**
```bash
yt-dlp \
  -f "bv*+ba/b" \
  --merge-output-format mp4 \
  -o "/Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO_ID>_ORIGINAL.%(ext)s" \
  "<URL>"
# NOTE: KHÔNG có --postprocessor-args — giữ codec gốc (AV1/Opus), KHÔNG qua H.264
```

**Anti-pattern:**
- ❌ Xoá file gốc ngay sau khi có bản crop — mất evidence để debug khi anh flag
- ❌ Ship 1 file (bản crop) mà không hỏi anh muốn so sánh với gốc không
- ❌ Assume anh sẽ thấy khác biệt ngay → anh cần 2 file để đối chiếu trực tiếp
- ❌ Re-encode bản gốc (mất AV1/Opus gốc) khi ship "original" — gọi là "gốc" mà thực ra đã convert

**Khi nào KHÔNG cần ship cả 2:**
- Banda đen rất nhỏ (<5% chiều cao) → crop xong ship 1 file OK, không cần so sánh
- Source đã là 9:16 native (không qua player ép) → không có banda đen, ship 1 file
- Anh explicit "không cần gửi bản gốc" → ship bản crop thôi

**Kết hợp với Pitfall W10 (vision verify cho aspect):** Cả W10 và 5D đều nói "đừng tin metadata, PHẢI visual verify". W10 cho aspect ratio sai do QuickTime/Telegram preview; 5D cho banda đen bên trong frame. Cùng lesson: ffprobe = ground truth cho codec/spec, nhưng VISUAL là ground truth cho "anh thấy gì trên màn hình".

**Real case 2026-07-12 (clip PaxRmpR_S-Y YouTube Shorts)**
- Source: YouTube Shorts `PaxRmpR_S-Y`, 46.88s
- Command trên → output: `/Volumes/Storage-1/Tiktok-Tuan-Anh/PaxRmpR_S-Y_iphone.mp4`
- Size: 26.84 MB (1080×1920, H.264 60fps, AAC 44100Hz, +faststart)
- Verify PASS: h264 + aac + 44100Hz + mp4 container
- Resend: `MEDIA:/Volumes/Storage-1/Tiktok-Tuan-Anh/PaxRmpR_S-Y_iphone.mp4` → anh play ngay trên iPhone

### 5G. ⚠️ Banda đen ASYMMETRIC (chỉ trên hoặc chỉ dưới, không đối xứng) — cropdetect fail, cần pixel sampling workflow (2026-07-14, NEW)

**Triệu chứng:** Anh share YouTube Shorts clip → em vision-verify → thấy "bị bóp vuông" hoặc "có 1 vùng đen lớn". Em chạy `cropdetect=limit=0.18` → output `crop=1080:1920:0:0` (full frame, không detect gì) vì frame có scoreboard/text overlay ở giữa → cropdetect KHÔNG work.

**Root cause:** YouTube Shorts player ép video broadcast 16:9 (landscape) vào container 9:16 (portrait) bằng cách thêm 1 vùng đen lớn ở trên (hoặc dưới) để fit tỷ lệ — KHÔNG đối xứng. Scoreboard overlay (LEE C.W. vs SUGIARTO, "COLDEST MATCHPOINT EVER !?") chạy giữa frame → cropdetect tưởng đó là content chính, ignore vùng đen.

**Workflow 5G (BẮT BUỘC khi cropdetect fail ở case asymmetric):**

**Bước 1: Pixel sampling dọc trục Y tại X giữa frame (x=540 cho 1080-wide)**

```python
from PIL import Image
import subprocess

# Extract 1 frame
subprocess.run(["ffmpeg", "-y", "-ss", "1", "-i", SOURCE,
                "-vframes", "1", "-update", "1", "/tmp/frame.png"],
               capture_output=True)

img = Image.open("/tmp/frame.png").convert("RGB")
for row_pct in [0.02, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.50, 0.70, 0.80, 0.85, 0.90, 0.95]:
    row = int(img.size[1] * row_pct)
    r, g, b = img.getpixel((540, row))
    brightness = (r + g + b) / 3
    marker = "⬛ BLACK" if brightness < 30 else "  content"
    print(f"  {marker} row {row_pct*100:4.1f}% (y={row}): RGB({r},{g},{b})")
```

**Output mẫu từ ZGOu1-J8Vb0 case (1080×1920, banda đen top 10%):**
```
  ⬛ BLACK row  2.0% (y=38):  RGB(8,5,6)
  ⬛ BLACK row  5.0% (y=96):  RGB(12,12,18)
  ⬛ BLACK row 10.0% (y=192): RGB(16,16,22)
     content row 15.0% (y=288): RGB(231,238,11)   ← scoreboard "COLDEST MATCHPOINT"
     content row 20.0% (y=384): RGB(130,23,18)    ← red SENHENG logo
  ⬛ BLACK row 25.0% (y=480): RGB(8,8,8)           ← weird: gap giữa scoreboard và sân
     content row 30.0% (y=576): RGB(17,20,54)     ← edge sân
     content row 40.0% (y=768): RGB(53,82,65)     ← sân xanh
     content row 50.0% (y=960): RGB(83,136,101)   ← sân xanh
     content row 60.0% (y=1152): RGB(235,255,233) ← sân sáng
     ...
```

→ Phát hiện: top 10% (y=0-192) = pure black, nhưng pixel brightness < 30 chỉ có ở top. Có 1 gap nhỏ ở row 25% (transition giữa scoreboard và sân) nhưng đó là visual transition chứ không phải black bar.

**Bước 2: Tính crop region từ row boundaries**

Trong case ZGOu1-J8Vb0:
- Banda đen top: 0-10% = y=0-192 (192px)
- Padding thêm 5% (48px) để không crop sát scoreboard → crop bắt đầu từ y=240
- Content height: 1920 - 240 = 1680px
- Width: giữ full 1080

→ `crop=1080:1680:0:240`

**Bước 3: Crop + scale fill 9:16**

```bash
ffmpeg -y -i SOURCE \
  -vf "crop=1080:1680:0:240,scale=1080:1920:flags=lanczos" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a copy \
  -movflags +faststart \
  OUTPUT_crop.mp4
```

Scale từ 1080×1680 lên 1080×1920 = vertical scale 1.143 (1.4%) → fill full 9:16.

**Bước 4: Vision verify (mandatory, không tin ffprobe)**

```bash
ffmpeg -y -i OUTPUT_crop.mp4 -ss 1 -vframes 1 -update 1 /tmp/crop_verify.png
# vision_analyze /tmp/crop_verify.png
#   "Đã hết banda đen trên chưa? Aspect dọc 9:16 đầy đủ chưa?
#    Scoreboard (nếu có) hiển thị OK không, hay bị crop mất?"
```

**Trade-off:**
- ✅ Hết banda đen → nhìn clean, fill full 9:16
- ⚠️ Có thể crop mất 1 phần scoreboard overlay (chấp nhận được vì YouTube Shorts đã broken aspect ratio gốc)

**Khi nào KHÔNG apply workflow 5G:**
- Cropdetect limit=0.35 work → case symmetric, dùng 5D workflow cũ
- Pixel sampling không phát hiện black bar → frame đã là 9:16 native, không crop
- Anh chỉ muốn giữ nguyên → ship bản gốc (xem 5F)

**Real case (2026-07-14, ZGOu1-J8Vb0):**
- Source: YouTube Shorts `ZGOu1-J8Vb0`, 25.29s, 1080×1920
- Workflow 5G step 1: pixel sampling → phát hiện top 10% (y=0-192) = black, scoreboard overlay ở y=288-480, sân ở y=576+
- Workflow 5G step 3: crop=1080:1680:0:240 + scale 1080:1920 → output 16.17 MB
- Vision verify: ✅ fill 9:16, scoreboard "COLDEST MATCHPOINT" còn, content sạch
- Ship CẢ 2 bản (5E protocol): bản gốc + bản crop → anh tự so sánh

**Khi nào phát hiện case asymmetric:**
- Cropdetect trả về `crop=1080:1920:0:0` (full frame, không crop gì) → 90% case asymmetric, dùng 5G
- Cropdetect trả về `crop=1072:1568:4:348` (symmetric, có top+bottom black) → case 5D cũ, dùng workflow cũ
- Vision frame cho thấy "vuông" nhưng cropdetect không phát hiện gì → asymmetric → dùng 5G

**Decision tree tổng hợp 5D/5E/5F/5G:**
```
Anh share YouTube Shorts + yêu cầu download
  ↓
yt-dlp iPhone-friendly pipeline (Pitfall 5C)
  ↓
Vision-verify frame
  ↓
Banda đen phát hiện?
  ├─ KHÔNG → ship bản gốc, xong
  └─ CÓ → HỎI anh trước (Pitfall 5F):
       ├─ "Giữ nguyên" → ship bản gốc, xong
       └─ "Crop đi" → chạy crop workflow:
            ├─ Cropdetect work (output != full frame) → workflow 5D (symmetric)
            └─ Cropdetect fail (output = full frame) → workflow 5G (asymmetric)
                 ├─ Pixel sampling → find black row boundaries
                 ├─ Crop + scale → ship bản crop
                 └─ Ship CẢ 2 bản (5E) để anh so sánh
```

### 5F. ⚠️ Crop banda đen KHÔNG phải lúc nào cũng cần — hỏi scope trước khi apply 5D (2026-07-14, NEW — FIRST-CLASS)

**Signal từ anh (verbatim 2026-07-14, Telegram):** *"Không cần, giữ nguyên bản là được rồi!!! Chỉ cần tải phiên bản phù hợp với chuẩn đọc file của iphone là được!!!"*

**Bối cảnh session 2026-07-14:**
- Anh share `youtube.com/shorts/WJJhUbnhx4Q` + yêu cầu "tải clip về đúng chuẩn của iphone và gửi qua telegram cho anh"
- Em download → re-encode H.264/AAC → OK
- Em vision-verify → phát hiện 2 banda đen lớn trên+dưới (chiếm ~30% frame) → em TỰ Ý chạy cropdetect + crop + scale để fill full 9:16
- Em ship bản đã crop + báo "đã fix banda đen"
- Anh reply: **"Không cần, giữ nguyên bản là được rồi!"** → em revert lại bằng cách re-download bản gốc không crop
- → Mất thời gian vô ích vì over-automation

**Rule mới (FIRST-CLASS, override auto-apply của 5D):**

Khi phát hiện banda đen ở video YouTube Shorts → **KHÔNG tự động crop**. Phải hỏi anh trước với 2 lựa chọn rõ ràng:

```
Em thấy video có 2 vùng đen lớn ở trên+dưới (chiếm ~30% frame, do YouTube Shorts player ép 16:9 broadcast vào 9:16).

Anh muốn:
A. Giữ nguyên bản gốc (có banda đen) — em chỉ convert codec iPhone-friendly, không crop
B. Crop + scale để fill full 9:16 (sạch banda đen) — em áp workflow 5D
```

**Khi nào CHỌN A (giữ nguyên — DEFAULT):**
- ✅ Anh chỉ nói "tải về / convert / đọc được trên iPhone" → KHÔNG động vào frame
- ✅ Anh đang archive/reference, không phải reup TikTok
- ✅ Anh thường open trên iPhone Photos app để xem → banda đen không quan trọng
- ✅ Anh KHÔNG nói gì về aspect/crop/9:16

**Khi nào CHỌN B (crop + scale 5D):**
- ⚠️ Anh nói "crop đi / sạch 9:16 / fill full / không banda đen / ready để post TikTok / reup"
- ⚠️ Anh có intent reup lên TikTok → TikTok algo đôi khi xử lý banda đen xấu
- ⚠️ Anh explicit đã complain về banda đen TRƯỚC đó trong session khác

**Anti-pattern (TỰ Ý CROP là over-automation):**
- ❌ Phát hiện banda đen → tự crop + scale mà không hỏi
- ❌ Assume "sạch hơn = tốt hơn" → sai, anh có thể muốn nguyên bản
- ❌ Skip hỏi vì "đây là best practice" → best practice ≠ user preference
- ❌ Mất 1 turn download + 1 turn revert vì crop sai preference

**Real case đã capture (2026-07-14):**
- Source: `youtube.com/shorts/WJJhUbnhx4Q` 57.07s (1080×1920, có 2 banda đen mỗi bên ~486px)
- Workflow sai (lần 1): download → cropdetect → crop=1080:948:0:486 → scale 1080:1920 → ship bản crop 14.13 MB → anh flag revert
- Workflow đúng (lần 2): re-download bản gốc không crop → 8.79 MB → ship → anh OK
- → Lần sau khi thấy banda đen: HỎI trước, không tự crop

**Communication template khi phát hiện banda đen:**
```markdown
✅ Download xong + convert iPhone-friendly: <FILE>

⚠️ Visual check: file có 2 vùng đen lớn ở trên+dưới (~30% frame, do YouTube Shorts ép 16:9 vào 9:16).

Anh muốn:
A. Giữ nguyên bản gốc (có banda đen) — em ship file 8.79 MB
B. Crop + scale fill full 9:16 — em re-process, output 14.13 MB
```

→ Chờ anh pick A hoặc B rồi ship.

## Common Pitfalls (Video)

[See full pitfall list W1-W12 below in PART 3 edition; the original PITFALL section is preserved in this skill's git history but the canonical reference is now the curated list under PART 3.]

### 5B. ⚠️ YouTube Shorts format selector fallback chain (2026-07-10, NEW)

**Bài học từ 2 turn liên tiếp tải Shorts (`aq61zm10xus`, `MkAlimt7et0`):**

Thay vì list format rồi pick theo ID (`96`/`95`), dùng **fallback chain** work cho mọi Shorts (H.264 lẫn AV1/HEVC):

```bash
yt-dlp -f "bv*[ext=mp4][height<=1280]+ba[ext=m4a]/b[ext=mp4][height<=1280] / bv*[height<=1280]+ba/b[height<=1280]" \
  --merge-output-format mp4 \
  -o "<VIDEO_ID>_<PLATFORM_TAG>.%(ext)s" "URL"
```

**Phân tích format chain:**
- Filter 1: `bv*[ext=mp4][height<=1280]+ba[ext=m4a]` — best video ≤1280p mp4 + best audio m4a
- Filter 2: `b[ext=mp4][height<=1280]` — combined ≤1280p mp4 (fallback khi không có separate streams)
- Filter 3: `bv*[height<=1280]+ba` — best video + best audio without ext restriction
- Filter 4: `b[height<=1280]` — combined without ext restriction (last resort)

`--merge-output-format mp4` ép output thành MP4 container chuẩn (Telegram play được).

**Verify kết quả thực tế (10/07/2026):**
- `aq61zm10xus` (39.1s): 3.72 MB, codec AV1, 576×1020 → ✅ play OK
- `MkAlimt7et0` (43.5s): 2.37 MB, codec AV1, 720×1280 → ✅ play OK
- Cả 2 đều dùng `398+140` (auto-picked bởi fallback chain) — không cần list format manually

**Filename convention:** `<VIDEO_ID>_<PLATFORM_TAG>.mp4` — ví dụ `aq61zm10xus_YT_Shorts.mp4`, `MkAlimt7et0_YT_Shorts.mp4`. Tag giúp identify platform dễ khi có nhiều file cùng id-style trong `~/Downloads/`.

### 5C. ⚠️ Clip cầu lông / TikTok content PHẢI save canonical folder `Tiktok-Tuan-Anh` + convert iPhone-friendly (2026-07-12, NEW)

**Anh's verbatim rule (2026-07-12, Telegram):** *"Luôn luôn lưu clip cầu lông vào folder tiktok-tuan-anh rồi gửi vào tele cho anh, convert thành định dạng phù hợp với iphone rồi hãy gửi nhé"*

**Canonical path:** `/Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO_ID>_iphone.mp4`

**iPhone-friendly format spec (HARD RULE):**
- Video: H.264 (libx264) - iOS native
- Audio: AAC 44100Hz 128kbps - iOS native
- Container: MP4 với `+faststart` - stream ngay không delay
- Không re-scale (giữ source resolution)

**Anti-pattern:**
- ❌ Save vào `~/Downloads/` cho clip cầu lông — sai folder, anh sẽ phải move thủ công
- ❌ Ship file AV1/HEVC gốc từ YouTube — iPhone không play native, mất thời gian convert
- ❌ Skip verify codec sau download — em bịa "đã iPhone-friendly" mà thực tế vẫn AV1
- ❌ Quên `+faststart` — iPhone/Telegram stream bị delay đầu 2-3s

**Workflow canonical (1 command):**
```bash
yt-dlp \
  -f "bv*[ext=mp4][vcodec^=avc]+ba[ext=m4a]/bv*[ext=mp4]+ba[ext=m4a]/bv*+ba/b" \
  --merge-output-format mp4 --remux-video mp4 \
  --postprocessor-args "ffmpeg:-c:v libx264 -preset fast -crf 23 -c:a aac -b:a 128k -movflags +faststart" \
  -o "/Volumes/Storage-1/Tiktok-Tuan-Anh/<VIDEO_ID>_iphone.%(ext)s" \
  "<URL>"
```

**Verify PASS (BẮT BUỘC trước khi ship):**
```bash
ffprobe -v error -show_entries stream=codec_name,sample_rate \
  -of default=noprint_wrappers=1 "/Volumes/Storage-1/Tiktok-Tuan-Anh/<FILE>.mp4"
# Expected: h264, aac, 44100Hz
```

**Workflow khi chỉ nhận được MP4 từ session trước đã save ở ~/Downloads:**
1. Move file vào `/Volumes/Storage-1/Tiktok-Tuan-Anh/` với tên `<VIDEO_ID>_iphone.mp4`
2. Nếu codec không phải H.264 → re-encode qua ffmpeg với command iPhone-friendly
3. Verify bằng ffprobe → PASS → resend qua Telegram

**Khi nào KHÔNG apply rule này:**
- Clip KHÔNG phải cầu lông / TikTok content (vd Facebook reel cá nhân, ảnh từ web, etc.) → save `~/Downloads/` như workflow cũ vẫn OK
- Anh explicit "lưu vào chỗ khác" → override
- File đã có sẵn trong `/Volumes/Storage-1/Tiktok-Tuan-Anh/` từ trước → không move

**Real case 2026-07-12:** Anh share `youtube.com/shorts/PaxRmpR_S-Y` → em download 720×1280 AV1 gốc trước đó → anh flag rule mới → em re-download thẳng vào `/Volumes/Storage-1/Tiktok-Tuan-Anh/PaxRmpR_S-Y_iphone.mp4` (H.264/AAC/44100Hz/+faststart, 26.84 MB) → resend qua Telegram → anh play ngay trên iPhone ✅

---

# PART 2: IMAGE WORKFLOW (curl + file)

When anh muốn ảnh (player photo, product photo, Wikipedia image) gửi qua Telegram → dùng `curl` + verify bằng `file`.

## Standard Workflow

### Step 1: Identify image source
| Source | Pattern |
|---|---|
| **Wikimedia Commons** | `https://upload.wikimedia.org/wikipedia/commons/thumb/.../<file>.jpg` |
| Direct image URL | URL kết thúc bằng `.jpg` / `.png` / `.webp` |
| CDN image | bất kỳ URL nào serve binary (không phải HTML page) |

### Step 2: Pick thumbnail size (Wikimedia)

Wikimedia chỉ cho tối size thumbnail cố định. Allowlist đã verify: **250, 500, 1280 work. 220, 320, 640, 800, 1024 FAIL**.

### Step 3: Download với User-Agent bắt buộc

Wikimedia KHÔNG cho tải nếu thiếu User-Agent. LUÔN pass `-H "User-Agent: <name>/1.0 (<purpose>; <email>)"`.

### Step 4: Verify bằng `file` command

Expected: `JPEG image data`. RED FLAG: `HTML document text` → User-Agent missing hoặc size sai.

### Step 5: Cleanup + rename

```bash
mv "tmp_<original_name>" "descriptive_name.jpg"
rm -f test_*.jpg tmp_*.jpg
```

### Step 6: Resend via Telegram
```
MEDIA:/Users/tuananh4865/Downloads/<topic>/<descriptive_name>.<ext>
```

Telegram natively render ảnh `.jpg` / `.png` / `.webp`.

### Common Pitfalls (Image) — TOP 10

(Tất cả I1-I24 đã có trong skill trước đó; tóm tắt highest-leverage:
- **I7** — Filename ≠ content, PHẢI vision-verify mọi ảnh
- **I10** — Multi-attribute (person + equipment) → verify CẢ HAI
- **I11** — Pre-flight fact-check timeline TRƛC khi download
- **I12** — Max 2 round failure, fail-fast
- **I13** — "Person + Equipment không tồn tại" → refuse upfront
- **I14** — User nói "dùng browser" → switch to computer_use
- **I15** — Kết luận vội vàng = fabricated-completion pattern
- **I17** — "Dùng browser" → MUST try 3 paths before báo "no browser"
- **I21** — Vision prompt phải multi-attribute
- **I23** — `browser-harness --doctor` trước khi dùng)

---

# PART 3: POST-DOWNLOAD EDITING — Watermark / text overlay removal (2026-07-10, NEW)

Khi anh tải clip về rồi yêu cầu **xoá chữ / logo / watermark** trong video (thường gặp với clip YouTube Shorts / TikTok có channel branding), workflow chuẩn:

## Step 1: Xác định vị trí chữ cần xoá

```bash
# Extract frame để xem chữ ở đâu trong video
ffmpeg -i input.mp4 -vf "select=eq(n\,30)" -vframes 1 frame_at_3s.png
ffmpeg -i input.mp4 -vf "select=eq(n\,60)" -vframes 1 frame_at_6s.png
# Xem bằng vision tool hoặc open file
```

Anh thường gọi theo tên channel ("SMASH HUB", "POV Việt", v.v.) — đó là watermark overlay cần xoá.

## Step 2: Clarify scope trước khi xử lý

**Trước khi chạy ffmpeg, PHẢI clarify 1-2 điểm** (xem W1 dưới):
- Clip nào trong N clip đã tải?
- Xoá ở toàn video hay frame cụ thể?
- Chấp nhận blur hay cần inpaint?

## Step 3a: Blur region (đơn giản, recommended)

Với watermark fixed corner (bottom-right, top-right, v.v.) — dùng ffmpeg `delogo` filter:

```bash
# Cú pháp chung: detect rect (x, y, w, h) của watermark trong frame
# Sau đó blur vùng đó suốt video
ffmpeg -i input.mp4 \
  -vf "delogo=x=550:y=1150:w=150:h=100:show=0" \
  -c:a copy output_no_watermark.mp4
```

**`delogo` filter:** ffmpeg có sẵn, blur đơn giản, 0 deps thêm. Hide vùng rectangular. Phù hợp watermark logo/channel name ở góc.

**Trade-off:** blur sẽ thấy "vệt mờ" ở vùng đó. Nếu watermark nằm trên background phức tạp (player đang chuyển động) → blur trông ugly. Khi đó cần inpaint (xem Step 3b).

## Step 3b: Inpaint via drawbox solid color (alternative)

Khi blur không đủ đẹp, dùng `drawbox` filter (che đặc, không blur):

```bash
ffmpeg -i input.mp4 \
  -vf "drawbox=x=550:y=1150:w=150:h=100:color=black@0.95:t=fill" \
  -c:a copy output.mp4
```

Trade-off: solid box thường lộ liễu hơn blur, nhưng triệt watermark 100%.

## Step 4: Verify output

```bash
ffprobe -v error -show_entries format=duration,size -show_entries stream=codec_name \
  -of default=noprint_wrappers=1 output.mp4
# Duration phải match input (không bị trim nhầm)
# Codec phải match hoặc tương đương (note: AV1 → H.264 tự động re-encode, xem W6)

# Verify watermark đã sạch bằng cách extract frame ở giây giữa
ffmpeg -y -ss 13 -i output.mp4 -vframes 1 /tmp/verify_frame.png
# vision_verify /tmp/verify_frame.png "Còn thấy chữ <WATERMARK_TEXT> không?"
```

## Step 5: Resend qua Telegram

```
MEDIA:/Users/tuananh4865/Downloads/.../output_no_watermark.mp4
```

---

## Common Pitfalls (Post-download editing)

### W1. ⚠️ Nhảy thẳng vào ffmpeg mà KHÔNG clarify scope với anh (2026-07-10, NEW)

**Triệu chứng lỗi:** Anh nói "xoá chữ X trong video" → em assume watermark fixed corner → chạy `delogo` luôn → kết quả:
- Có thể sai vị trí (chữ ở giữa video chứ không phải góc)
- Có thể sai range (chữ chỉ hiện 0-3s đầu, blur cả 39s → vùng mờ thừa)
- Có thể sai clip (anh muốn xoá ở clip 3, em xoá nhầm clip 1)

**Rule bắt buộc TRƯỚC khi chạy ffmpeg:**

1. **Hỏi anh 1-2 câu clarify** (xem Step 2 ở trên):
   - Clip nào trong N clip đã tải?
   - Xoá ở toàn video hay frame cụ thể?
   - Chấp nhận blur hay cần inpaint?

2. **Extract 1 frame** để tự xác định vị trí watermark TRƯỚC khi hỏi (câu hỏi thông minh hơn khi em đã biết "chữ nằm ở góc dưới phải, fixed cả video")

3. **Nếu anh chỉ gửi "xoá chữ X trong video" mà KHÔNG có context clip nào** → check `~/Downloads/` gần đây xem clip nào có tên/channel match → propose 1-2 candidate clips rồi hỏi confirm.

**Anti-pattern:**
- ❌ Assume watermark fixed corner + blur cả video
- ❌ Xoá trên clip 1 vì là clip mới nhất (anh có thể muốn clip 2)
- ❌ Không verify frame trước khi xử lý
- ❌ Confirm "xong rồi anh" khi chưa vision-verify output

**Real case 2026-07-10 (SMASH HUB):** Anh hỏi "xoá chữ SMASH HUB trong video được không" sau khi tải 3 clip YouTube Shorts (`aq61zm10xus`, `MkAlimt7et0`, `UqdcgQ-_oN4`). Em đã phải hỏi lại clip nào (1, 2, hay 3) → anh pick clip số 3 → em xử lý. Acceptable 1-round clarify.

→ Upgrade: nếu trước khi hỏi em đã extract 1 frame từ 1 candidate clip + check channel name trên screen → câu hỏi sẽ thông minh hơn: "Em thấy chữ SMASH HUB ở góc dưới phải clip 3 (UqdcgQ-_oN4), cố định cả 27s — em blur vùng đó cho anh OK không?"

### W2. Watermark text MOVING theo player (overlay động)

Một số watermark bám theo player/ball (thường với watermark thể thao do hệ thống broadcast overlay). `delogo` static rectangle KHÔNG work vì vị trí thay đổi mỗi frame.

**Solution:** dùng skill `floating-watermark-remover` (OpenCV template matching + per-frame inpaint). Load `skill_view(name='floating-watermark-remover')` để có workflow + scripts. Workflow tổng quát:

1. Sample 9 frames evenly → vision_analyze từng frame → locate ALL distinct watermark positions
2. Extract all frames (ffmpeg -vsync 0, NO -r flag — ffmpeg reject combined)
3. Build 1 template per position (with 10px padding each side)
4. Track per frame bằng cv2.matchTemplate + TM_CCOEFF_NORMED (conf > 0.4)
5. Inpaint ROI per frame bằng cv2.inpaint(Telea, radius=7) với background-comparison mask
6. Re-encode bằng ffmpeg với FPS detected from ffprobe (NOT hardcoded)

**Real case 24/07 (clip 17si3J8buy, 16.39s, 30fps):** Watermark "CẨU LỒN VBL" jumped between bottom-left (132x103) and top-right (400x120). Tracked 489/490 frames. Final output needs more iteration on mask dilate for visual edge quality.

**Real case 24/07 (clip lGZQgDMMMac, 28.82s, 60fps):** Static logo "SB SMASHBERT" top-left → SAME skill (single template, no tracking needed) → clean output. **Lesson:** This skill handles BOTH static AND floating — but for visible-quality output, prefer it over `delogo` for static too (delogo leaves visible blur strip).

### W3. Watermark TRONG SUỐT (alpha < 1.0) → blur không đủ triệt

Watermark semi-transparent (alpha 30-50%) blend với background → blur làm mờ vẫn thấy "shadow" của chữ.

**Detection:** frame có chữ → check pixel intensity ratio giữa vùng chữ vs background. Nếu delta < 30% → semi-transparent.

**Solution:** dùng `drawbox` solid color thay vì blur (xem Step 3b ở trên).

### W4. Output > 50MB → Telegram timeout

Video gốc YouTube Shorts thường < 10MB, xử lý xong vẫn nhỏ. NHƯNG nếu ffmpeg re-encode (không copy codec) → size có thể tăng 2-3x.

**Workaround:**
```bash
# Re-encode 720p H.264 AAC cho file lớn
ffmpeg -i output.mp4 -vf "scale=-2:720" -c:v libx264 -preset medium -crf 23 \
  -c:a aac -b:a 128k -movflags +faststart output_compressed.mp4
```

### W5. ⚠️ Coordinate guess không trúng → loop vision-verify + adjust coords (2026-07-10, NEW)

**Triệu chứng lỗi:** Em estimate tọa độ watermark lần đầu → chạy `delogo=x=500:y=1100:w=210:h=120` → extract frame ở giây giữa → vision-verify → vẫn THẤY "SMASH HUB" còn mờ ở góc dưới phải.

**Root cause:** Guess tọa độ từ 1 frame mid-video thường lệch ~50-100px so với vị trí thật. Text nằm ở vị trí em không ngờ (ví dụ nằm sát mép hơn dự kiến, hoặc text chiếm vùng rộng hơn).

**Rule bắt buộc:** Sau MỖI `delogo` render → trích 1 frame ở giây giữa video → vision-verify → check xem text đã hết chưa. Nếu chưa → tăng vùng box (x giảm, y giảm, w/h tăng) → render lại. Lặp tới khi sạch.

```bash
# Loop 1: estimate
ffmpeg -i in.mp4 -vf "delogo=x=500:y=1100:w=210:h=120:show=0" -c:a copy v1.mp4

# Verify
ffmpeg -y -ss 13 -i v1.mp4 -vframes 1 /tmp/v1_verify.png

# vision_verify /tmp/v1_verify.png "Còn thấy chữ 'SMASH HUB' ở góc dưới phải không?"
# → "Vẫn còn, lệch phải +10px"
# → tăng vùng: x giảm 60, y giảm 20, w tăng 60, h tăng 60

# Loop 2: rộng hơn
ffmpeg -i in.mp4 -vf "delogo=x=440:y=1080:w=270:h=180:show=0" -c:a copy v2.mp4

# Verify lại → clean ✅ → ship
```

**Heuristic khi adjust:**
- Text vẫn lộ bên **phải** → `x` giảm (kéo box sang trái bao trùm text)
- Text vẫn lộ bên **trái** → `x` tăng
- Text vẫn lộ **trên** / **dưới** → adjust `y` tương ứng
- Text còn **rõ** (không phải lệch) → tăng `w` + `h` (mở rộng box)

**Max số lần retry:** 3. Nếu loop 3 mà vẫn còn text → escalate: trình bày cho anh xem + hỏi approach khác (inpaint model, hybrid, v.v.).

**Anti-pattern:**
- ❌ Render 1 lần rồi ship (không verify) — em bịa "đã xoá sạch" mà thực tế text vẫn còn
- ❌ Adjust tọa độ linh tinh không có evidence từ frame verify
- ❌ Over-blur (box quá to) → che mất content quan trọng (player/ball/scoreboard)

**Expected result với case real 2026-07-10 (SMASH HUB):**
- Loop 1 (`x=500:y=1100:w=210:h=120`): vẫn thấy text → fail
- Loop 2 (`x=440:y=1080:w=270:h=180`): text hoàn toàn sạch → ship ✅
- → 2 lần là đủ cho typical watermark góc cố định

### W8. ⚠️ Vision pixel coords KHÔNG map 1:1 sang video pixels (2026-07-10, NEW)

**Triệu chứng lỗi:** Em extract frame 720×1280 → load qua `vision_analyze` → vision tool có thể upscale/downscale ảnh trước khi hiển thị → tọa độ pixel em đọc từ vision response KHÔNG map 1:1 sang pixel coordinates của frame gốc.

**Real case (2026-07-10, SMASH HUB):** Vision trả lời text nằm ở "x: 380-510, y: 1020-1060" → em feed thẳng vào `delogo=x=370:y=1010:w=160:h=60` → render → text vẫn còn nguyên → mất 3 loops vì coord em dùng không khớp video pixel.

**Rule bắt buộc:** Vision output tọa độ CHỈ DÙNG LÀM GỢI Ý TƯƠNG ĐỐI (góc, khoảng cách từ mép), KHÔNG dùng pixel absolute.

**Cách lấy coord chính xác hơn:**

1. **Crop CHẶT từ video gốc + vision trên crop đó** — vision trên vùng crop nhỏ (~400×80) sẽ có ít sai số upscale hơn so với vision trên full 720×1280.
   ```bash
   ffmpeg -y -i in.mp4 -ss 13 -vf "crop=400:80:300:1080" -vframes 1 /tmp/text_region.png
   vision_analyze /tmp/text_region.png "Trong crop này (400×80) chữ SMASH HUB chiếm từ pixel x,y đến x,y nào?"
   # Sau đó ADD back offset của crop vào coords
   ```

2. **Dùng Python/PIL scan pixel** nếu cần pixel-perfect (cần pip install pillow + numpy):
   ```python
   from PIL import Image
   import numpy as np
   img = Image.open('/tmp/frame.png')
   arr = np.array(img.convert('RGB'))
   # Tìm pixel sáng (text trắng) trên nền tối hơn
   text_mask = (arr[:,:,0] > 200) & (arr[:,:,1] > 200) & (arr[:,:,2] > 200)
   rows = np.where(text_mask.any(axis=1))[0]
   cols = np.where(text_mask.any(axis=0))[0]
   print(f"y: {rows.min()}-{rows.max()}, x: {cols.min()}-{cols.max()}")
   ```

3. **Empirical loop is the ground truth** — vision gợi ý sai + crop+vision tốt hơn + Python scan chính xác nhất. Nhưng cuối cùng vẫn phải loop `delogo` → `ffmpeg -ss X -vframes 1 verify.png` → `vision_analyze verify.png` để confirm.

**Expected real-case result (2026-07-10 SMASH HUB):** Vision crop đúng → coord `x=380, y=1000, w=280, h=110` → render → text sạch. 5 loops total vì coord ban đầu (vision estimate) sai. Lần sau: BẮT ĐẦU với crop CHẶT → đỡ mất 2-3 loops.

### W9. User preference: precise cover, NOT wide blur (2026-07-10, NEW)

**Signal:** Sau khi em làm bản `boxblur` overlay rộng 320×200 (che cả vùng SMASH HUB + 1 phần sân), anh ngay lập tức reply: *"Che đúng vùng có chữ smash hub thôi"*.

**Rule:** Khi anh nói "che đúng vùng có chữ" / "đừng che thừa" / "giữ nguyên phần còn lại" → anh muốn **delogo rectangle vừa đủ bao chữ**, KHÔNG dùng boxblur rộng (320×200+) hoặc drawbox full-width.

**Trade-off matrix:**
| Approach | Khi nào dùng |
|---|---|
| `delogo` rectangle vừa đủ (W5+W8 iterative) | ✅ Default. Khi anh muốn "che đúng chỗ chữ", không phá content khác |
| `boxblur` overlay rộng (PART 3 mục cũ) | Khi text nằm trên background phức tạp (player động) và blur mượt hơn solid color. Clip Clean-up with motion = dùng boxblur |
| `drawbox` solid color | Khi text semi-transparent (W3) |

**Khi nào KHÔNG dùng delogo rectangle vừa đủ:**
- Text chuyển động nhiều (overlay dynamic) → cần inpaint/tracking
- Text ở nhiều vị trí khác nhau trong video → cần nhiều `delogo` instances

**Real case (2026-07-10 SMASH HUB):** Sau 5 loops cuối cùng em settle ở `delogo=x=380:y=1000:w=280:h=110:show=0` (chỉ bao chữ, hơi rộng 10px cho padding) → text sạch 100%, không động vào text khác (VICTOR, HSBC, CHANGZHOU) → ship OK.

### W6. AV1/H.265 source → `delogo` tự động re-encode sang H.264 (codec change side effect, 2026-07-10, NEW)

**Triệu chứng:** Source YouTube Shorts codec là AV1 (`codec_name=av1` trong `ffprobe`). Em chạy `ffmpeg -vf delogo=... -c:a copy` → output file là H.264 (`codec_name=h264`). Không mong đợi.

**Nguyên nhân:** `delogo` filter chạy trên video frame → ffmpeg tự chọn encoder mặc định cho filter graph = libx264 khi không có `-c:v` flag rõ ràng. `-c:a copy` chỉ copy audio stream, không liên quan video.

**Tác động:**
- File size tăng ~15-20% (H.264 ít hiệu quả hơn AV1)
- Codec change = phải re-encode ~3-10s cho clip 27s
- Quality loss: minor với default CRF 23

**Khi nào quan trọng:** Nếu anh cần clip gốc giữ codec (cho reup TikTok đòi codec spec cụ thể) → force `-c:v copy` KHÔNG work vì filter yêu cầu decode. Phải explicit `-c:v libx264 -crf 18` (quality cao) hoặc `-c:v libsvtav1` (giữ AV1 nếu libsvtav1 có sẵn).

**Khi nào KHÔNG quan trọng:** Telegram play được cả H.264 lẫn AV1 → for download-and-send workflow thì codec change OK. Chỉ note lại trong response để anh biết.

**Verify sau khi render:**
```bash
ffprobe -v error -show_entries stream=codec_name -of default=noprint_wrappers=1 v2.mp4
# → h264, aac (audio copy nguyên, video re-encode)
```

**Real case 2026-07-10:** Clip UqdcgQ-_oN4 source AV1 → output 4.52 MB H.264 (tăng từ 3.89 MB source do re-encode).

### W7. ⚠️ Watermark có channel name KHÁC (sport channel, news, custom branding) — cần xác nhận channel trước khi xoá (2026-07-10, NEW)

**Triệu chứng:** Anh chỉ nói tên watermark ("SMASH HUB", "POV Việt", "Yonex TV") → em không biết chính xác channel nào đang brand clip.

**Heuristic:** Anh thường nói đúng tên channel → assume đó là watermark overlay. KHÔNG cần confirm.

**Khi nào PHẢI hỏi anh:**
- Anh nói tên ambiguous (e.g. "logo", "watermark") → phải ask: cụ thể chữ gì, hình gì?
- Nhiều channel cùng tên branding trên cùng 1 clip (e.g. channel overlay + sponsor banner) → hỏi chỉ xoá overlay, không xoá sponsor
- Text có thể appear trong nhiều channel khác nhau → check frame xem channel context trước

**Workflow chuẩn:**
1. Extract 1 frame
2. Vision-verify: "Trong frame có chữ/Logo <TÊN> ở đâu? Mô tả kích thước, màu sắc, context xung quanh"
3. Nếu match → chạy `delogo`. Nếu không match → ASK ANH confirm.

**Real case 2026-07-10 (SMASH HUB):** Anh nói "xoá chữ SMASH HUB trong video" → em check `~/Downloads` không có file tên "smash" → em hiểu là watermark overlay trong 1 trong 3 clip đã tải → em hỏi anh chọn clip nào (1, 2, hay 3) → anh pick clip số 3 (UqdcgQ-_oN4) → em xử lý thành công.

### W10. ⚠️ "Convert thành vuông" — visual aspect mismatch dù ffprobe metadata đúng (2026-07-12, NEW)

**Triệu chứng lỗi:** Em convert clip xong, ffprobe verify width=1080 height=1920 display_aspect_ratio=9:16 PASS 100% → em báo "đã đúng aspect 9:16, file ở folder Tiktok-Tuan-Anh". Anh mở file → thấy **VUÔNG** (1:1) hoặc landscape ngang. Em confused vì metadata nói 9:16 mà visual nói vuông.

**Root cause — 3 nguyên nhân thường gặp:**

| # | Nguyên nhân | Cách verify | Cách fix |
|---|---|---|---|
| **1** | **QuickTime preview cache** | Mở file lần đầu → xem vuông → nhấn Space restart hoặc close + reopen | Restart app, không phải file lỗi |
| **2** | **Telegram thumbnail fit** | Telegram tự fit thumbnail vào khung chat (max 320×320) → 9:16 source bị fit thành 9:16 trong khung nhỏ nhưng vẫn trông tỷ lệ dọc OK; nếu browser/Telegram web render sai có thể thấy crop | Mở file gốc trên iPhone Photos app mới là ground truth |
| **3** | **Mac Finder preview bug** | Finder preview đôi khi cache metadata sai sau khi file vừa re-encode | Right-click → Get Info → check "Dimensions" trong More Info, KHÔNG tin Quick Look preview |

**Rule BẮT BUỘC trước khi báo "đã đúng aspect 9:16":**

1. **ffprobe verify (đã có W5/W8)** — check `display_aspect_ratio=9:16` PASS
2. **NEW: Extract frame PNG + load qua vision_analyze** — hỏi "Frame này có aspect 9:16 (dọc) hay 1:1 (vuông) hay 16:9 (ngang)?"
3. **NEW: Check pixel count** — file 1080×1920 có 2,073,600 pixels; nếu thấp hơn 50% (vd 800×800 = 640,000) → bị scale xuống → aspect sai thật
4. **NEW: Report 3 nguyên nhân trên cho anh** kèm hướng dẫn "mở trên iPhone Photos app là ground truth"

**Visual verification command:**
```bash
ffmpeg -y -i "<FILE>.mp4" -ss 5 -vframes 1 /tmp/aspect_check.png
# Load /tmp/aspect_check.png qua vision_analyze
# Question: "Frame này dọc (9:16), vuông (1:1), hay ngang (16:9)?"
```

**Anti-pattern:**
- ❌ Chỉ check ffprobe metadata rồi báo "đã đúng 9:16" mà KHÔNG visual verify
- ❌ Khi anh flag "thấy vuông" → argue ngược "ffprobe nói 9:16 mà" thay vì acknowledge + investigate 3 root causes
- ❌ Assume QuickTime/Telegram preview = ground truth (KHÔNG — iPhone Photos app mới là ground truth)

**Real case 2026-07-12 (PaxRmpR_S-Y):**
- Em convert xong: ffprobe PASS (1080×1920, display_aspect_ratio=9:16, H.264/AAC/44100Hz/+faststart) → 26.84 MB
- Em báo "đã đúng 9:16"
- Anh reply: "Mỗi lần em convert nó lại thành định dạng vuông là sao"
- Em check lại: ffprobe VẪN PASS 9:16, file thực sự dọc → nguyên nhân KHÔNG phải convert sai mà là preview/cache issue ở phía anh
- Lesson: anh cần được báo trước 3 nguyên nhân + hướng dẫn "mở trên iPhone Photos" thay vì em argue metadata đúng

**Communication template khi anh flag aspect sai:**
```
File ffprobe verify đúng 9:16 (width=1080, height=1920, 2,073,600 pixels, H.264/AAC). 
File thực sự DỌC.

Anh thấy vuông có thể do 1 trong 3 nguyên nhân:
1. QuickTime preview cache → close + reopen QuickTime
2. Telegram thumbnail fit → mở file gốc trên iPhone Photos app là ground truth
3. Mac Finder Quick Look bug → Get Info → Dimensions

Anh test trên iPhone Photos app giùm em — vẫn vuông hay đã dọc 9:16?
Nếu vẫn vuông trên iPhone Photos → có bug thật, em fix ngay.
```

### Quick "xoá watermark" CLI

**DEFAULT for visible-quality output** (24/07 signal: "tốt, tìm cách xoá logo tốt hơn đi"):
Load `floating-watermark-remover` skill — OpenCV inpaint per-frame tốt hơn delogo blur (no visible blur strip).

**FALLBACK for fast preview / non-critical clips** (when speed > quality):

```bash
# Khi đã biết vị trí (ví dụ góc dưới phải, 270x180 pixel, toàn video):
ffmpeg -i input.mp4 -vf "delogo=x=W-280:y=H-200:w=270:h=180:show=0" -c:a copy output.mp4
# x = W-280: cách mép phải 10px (W = width video)
# y = H-200: cách mép dưới 20px (H = height video)
# show=0: KHÔNG show debug box trong output (mặc định show=1)

# Sau khi render → verify bằng frame extract + vision_verify
ffmpeg -y -ss <MID_SEC> -i output.mp4 -vframes 1 /tmp/verify.png
# vision_verify /tmp/verify.png "Còn watermark không?"

# Nếu còn → loop W5 protocol (W8 lưu ý: coord từ vision là tương đối)

# Gửi
MEDIA:/Users/tuananh4865/Downloads/.../output.mp4
```

### W11. ⚠️ Chain 2 delogo liên tiếp trong cùng filtergraph FAIL với "Logo area is outside of the frame" (2026-07-14, NEW)

**Triệu chứng:** Em áp 2 `delogo` liên tiếp trong cùng 1 `-vf` chain để xoá 2 vùng watermark:
```bash
ffmpeg -i input.mp4 -vf "delogo=x=70:y=890:w=700:h=80:show=0,delogo=x=1010:y=0:w=65:h=950:show=0" ...
```
Em nhận `Exit: 234`, log `Logo area is outside of the frame` + `Failed to configure input pad on Parsed_delogo_1` + `Could not open encoder before EOF`. KHÔNG phải do tọa độ sai (verify: x=1010, w=65 → end=1075 ≤ 1080, y=0, h=950 → 950 ≤ 1920, đều trong frame).

**Root cause:** delogo thứ 2 nhận input pad từ delogo thứ 1, ffmpeg internal state mismatch khi chain 2 delogo liên tiếp → fail ở pad configuration.

**Workaround (verified 2026-07-14):**

Mix `delogo` (cho text → blur thành vệt mờ) + `drawbox` (cho shape đơn giản → che bằng hộp đen):
```bash
ffmpeg -i input.mp4 \
  -vf "delogo=x=70:y=890:w=700:h=80:show=0,drawbox=x=1010:y=0:w=65:h=950:color=black@0.95:t=fill" \
  -c:v libx264 -preset fast -crf 23 \
  -c:a aac -b:a 128k \
  -movflags +faststart output.mp4
```

**Trade-off:**
- `delogo` blur → vệt mờ, content xung quanh vẫn visible (cho watermark text nằm trên background phức tạp)
- `drawbox` solid color → che 100% (cho watermark text dọc, fixed shape, ít overlap với content quan trọng)

**Khi nào KHÔNG áp dụng:**
- Chỉ có 1 watermark → dùng 1 delogo OK
- Watermark là logo phức tạp (multi-color, gradient) → cần approach khác (inpaint model)

**Anti-pattern:**
- ❌ Chain N delogo liên tiếp khi biết có >1 watermark
- ❌ Retry với params khác khi gặp "Logo area is outside of the frame" — vấn đề không phải tọa độ
- ❌ Đổi sang `-filter_complex` filter graph mà KHÔNG thay đổi approach (vẫn chain 2 delogo → vẫn fail)
- ✅ Mix delogo + drawbox

**Real case (2026-07-14, clip 17si3J8buy Facebook Reel):**
- Watermark "CẨU LỒN VBL" ở y=890-960 (semi-transparent, blur được)
- Text dọc bên phải ở x=1010-1075, y=0-950 (cần che kín)
- Workflow sai (lần 1): 2 delogo liên tiếp → Exit: 234
- Workflow đúng (lần 2): delogo + drawbox → OK, file 6.76 MB, vision verify 5/5 timestamps clean ✅

## Quick decision tree cho anh muốn xoá watermark

1. **Anh nói "che đúng vùng có chữ" / "đừng che thừa"** → đi thẳng W5 (delogo vừa đủ) + W8 (crop CHẶT trước khi vision).
   - KHÔNG dùng boxblur rộng, KHÔNG dùng drawbox full-width.
2. **Anh chỉ nói "xoá watermark"** (không nói "đúng vùng") → vẫn default W5 delogo vừa đủ, nhưng box rộng hơn 1 chút ok (padding 30-50px).
3. **Text ở background phức tạp** (player động, lighting thay đổi) → dùng boxblur (PART 3 mục cũ) hoặc drawbox solid color.
4. **Text moving theo player** → load `floating-watermark-remover` skill (OpenCV tracking + inpaint).

**Anh signal "tốt, tìm cách xoá logo tốt hơn đi" (verbatim 24/07):**
Khi anh không hài lòng với blur artifact của delogo (`delogo` để lại vệt blur vertical visible), default path phải switch sang OpenCV `cv2.inpaint(Telea, radius=7)` per-frame — fill region với inferred background, không có vệt blur. Cùng skill `floating-watermark-remover` handles STATIC logos tốt hơn delogo too (không cần multi-template tracking cho static, chỉ 1 ROI áp dụng mỗi frame).

---

## Cross-cutting Pitfalls (Cả video + ảnh)

### C1. File > 50MB → Telegram timeout

Bot API timeout với file > 50MB. Workaround:
- Video: re-encode với ffmpeg (720p H.264 AAC)
- Ảnh: hầu như không bao giờ > 50MB, nhưng nếu raw TIFF/PSD → convert JPEG trước

### C2. Telegram 20MB hard limit cho bot `getFile` endpoint

KHÔNG apply cho `sendFile` (gửi đi) — chỉ apply cho `getFile` (nhận file từ user gửi lên). Nên download → send qua Telegram thường OK với file < 50MB.

Reference: `telegram-video-analysis` skill (đã document 20MB receive limit riêng).

---

## Related
- [[transcript-cleanup]] — Cleanup media files sau khi dùng xong (tránh đầy disk)
- [[youtube-transcript-extractor]] — Extract transcript (KHÁC: workflow này giữ video, gửi qua Telegram)
- [[telegram-video-analysis]] — Phân tích video user gửi (ngược với workflow này)

## References
- `references/momota-99pro-case-study.md` — Full case study of the 2026-06-30 multi-attribute image search failure (Momota + 99 Pro Gen 3) with 4-round timeline, root cause analysis, and trigger phrases to watch for.
- `references/pdf-vietnamese-workflow.md` — Step-by-step PDF generation workflow for Vietnamese research delivery (reportlab + Arial Unicode, uv venv setup, verification matrix). Use when user requests "gửi PDF" or research content > 4000 chars.
- `references/tiktok-hevc-workaround-2026-06-30.md` — TikTok HEVC video download workarounds (7 approaches tested, only audio-only works in many cases).
- `references/watermark-removal-coord-iteration.md` — **NEW 2026-07-10:** 5-loop coordinate iteration case study for SMASH HUB watermark. Documents why W8 (vision pixel coords ≠ video pixels) matters and why exact coord initial-guess fails 4/5 times. **Use when** removing watermark/text overlay where exact pixel position is unknown.
- `references/wikimedia-commons-source-discovery.md` — **NEW 2026-07-08:** Source discovery pattern for "fetch N images for N topics" tasks. Covers Wikimedia imageinfo API batching (`titles=A|B|C` to dodge rate-limit), the MD5-hash-prefix URL guessing pitfall (always 404 if you guess), vision-verify step, and markdown output format for parent agents. **Use this** instead of PART 2 when the task is "give me URL list with attribution", NOT "download and send to Telegram".
- `references/iphone-friendly-crop-vs-keep-2026-07-14.md` — **NEW 2026-07-14:** Decision tree cho crop banda đen vs giữ nguyên gốc khi convert iPhone-friendly. Real case WJJhUbnhx4Q: em tự ý crop → anh flag revert → lesson: mặc định giữ gốc, chỉ crop khi anh explicit yêu cầu.
- `references/asymmetric-black-bars-pixel-sampling-2026-07-14.md` — **NEW 2026-07-14:** Banda đen ASYMMETRIC (chỉ trên hoặc chỉ dưới, không đối xứng) — cropdetect limit=0.18/0.25/0.35 đều fail vì scoreboard overlay che middle. Pixel sampling workflow tại x=540 với brightness < 30 threshold → find row boundaries → crop+scale fill 9:16. Real case ZGOu1-J8Vb0: top 10% black, scoreboard 15-25%, sân 30-95%. Use khi cropdetect output = full frame.

## Quick trigger reference: which path to use?

| If the task is... | Use this |
|---|---|
| "Download this image and send to Telegram" | PART 2 + `MEDIA:/path` |
| "Find N CC-licensed images for N topics, give me URLs" | `references/wikimedia-commons-source-discovery.md` |
| "Save image to disk + verify with `file`" | PART 2 curl workflow |
| "Find player X photo + equipment Y (multi-attribute)" | PART 2 + pitfall I10/I21 vision prompts |
| "Remove watermark/text from downloaded clip" | PART 3 + W1/W5/W6/W7 pitfalls |
| "Both download clip + remove watermark" | PART 1 first → then PART 3 on output |
| **"Download clip cầu lông / TikTok content + iPhone-friendly + lưu canonical folder"** | **Step 4b + Pitfall 5C** (HARD RULE từ 2026-07-12) |
