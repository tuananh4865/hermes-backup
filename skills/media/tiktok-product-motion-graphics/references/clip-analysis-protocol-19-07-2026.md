# 🎬 CLIP ANALYSIS PROTOCOL — Eyes + Ears + Brain (verified 19/07/2026)

> **Anh dặn (verbatim 19/07/2026):** *"Đọc transcript dùng mắt và tư duy của chính em để suy nghĩ. Chụp hình clip để phân tích kĩ diễn biến trong video!"*

> **Tested 19/07/2026 với clip_0004_V3_85s_FINAL_DJI_source (71.2 MB, 85.9s, H.264 1080×1920 + AAC).** File này tổng hợp HARD RULE mới + case study thực tế.

---

## 🎯 MỤC ĐÍCH

Trước khi lên plan motion cho bất kỳ clip nào, **BẮT BUỘC** thực hiện 6 bước phân tích. Đây là **Key #1 để tránh build motion sai sản phẩm / sai vị trí / sai visual context.**

## ⚠️ BÀI HỌC LỚN TỪ CLIP_0004 CASE

Em test quy trình mới với `clip_0004_V3_85s_FINAL_DJI_source.mp4`. Phát hiện:

| Source | Báo | Thực tế |
|---|---|---|
| Tên file | "DJI_source" | Không phải DJI |
| Whisper (TAI) | "máy hút bụi Doroto E Luxe V3, 25.000 bát canh" | **SAI** — visual thấy máy sấy tóc OTOBOP |
| Mắt em | OTOBOP máy sấy tóc (màu đen + đồng, có logo "otobob") | **ĐÚNG** |
| Wiki (Key #1) | Có wiki Doroto Lux Air V3 (nhưng clip không phải Doroto) | Khớp với Whisper (cùng sai) |

→ **3 nguồn disagree** = phải dừng lại verify với anh trước khi build motion.

**Lesson vĩnh viễn:** Whisper có thể SAI với tiếng Việt (model hallucinate hoặc nghe nhầm). Visual (MẮT) là GROUND TRUTH khi có mâu thuẫn.

---

## 6 BƯỚC BẮT BUỘC

### Bước 1: XEM clip + Extract frames (MẮT)

```bash
# Extract 5-10 frames tại các timestamp quan trọng
# Rule: mỗi 10s extract 1 frame, hoặc tại các đoạn chính (0s, 10s, 20s, ...)
ffmpeg -y -ss 0 -i source.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/frame_00s.jpg
ffmpeg -y -ss 10 -i source.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/frame_10s.jpg
ffmpeg -y -ss 20 -i source.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/frame_20s.jpg
ffmpeg -y -ss 30 -i source.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/frame_30s.jpg
ffmpeg -y -ss 40 -i source.mp4 -frames:v 1 -vf "scale=540:-1" /tmp/frame_40s.jpg
```

**5-10 frames tuỳ clip dài.** Lưu vào `/tmp/<clip_name>_frames/`.

### Bước 2: MẮT phân tích từng frame

Dùng `vision_analyze` cho từng frame, note:
- (a) Mặt anh đang làm gì? Cầm gì? Chỉ vào đâu?
- (b) Background là gì? Có sản phẩm nào trong frame?
- (c) Logo / chữ trên sản phẩm (nếu có)
- (d) Cử chỉ / biểu cảm

**GROUND TRUTH** — nếu mâu thuẫn giữa Whisper và Mắt → Mắt thắng.

### Bước 3: CHECK WIKI (Key #1)

```bash
# List wiki products
ls /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/

# Read product file (nếu có)
cat /Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/<slug>.md
```

**3 trường hợp:**

| Trường hợp | Action |
|---|---|
| ✅ Có wiki, khớp với visual | Dùng wiki specs (citation [N]) |
| ❌ KHÔNG có wiki | **DỪNG LẠI**, tạo wiki mới trước (dùng `wiki-product-ground-truth` skill) |
| ⚠️ Có wiki nhưng KHÔNG khớp visual | DỪNG LẠI, verify với anh |

### Bước 4: TAI nghe audio (Whisper hoặc ear)

```bash
# Whisper Vietnamese
mlx_whisper --model mlx-community/whisper-medium-mlx \
  --language vi --output-format json \
  --output-dir /tmp/<clip_name>_whisper source.mp4
```

**LƯU Ý:** Whisper có thể SAI với tiếng Việt (hallucinate). Sau khi có transcript, **CROSS-VERIFY với MẮT + WIKI**. Nếu 3 nguồn disagree → DỪNG LẠI hỏi anh.

### Bước 5: TƯ DUY đặt câu hỏi + lên plan motion

Dựa trên 4 bước trên:
- (a) Đoạn nào cần show sản phẩm rõ? (visual + audio cue)
- (b) Đoạn nào dùng mặt anh nói? (cần glass card)
- (c) Đoạn nào nên có CTA? (audio cue: "bấm link", "mua")
- (d) Animation nào phù hợp với cảm xúc? (kinh ngạc? hài? cảm xúc?)

### Bước 6: CHỤP ảnh motion verify

Sau khi build, extract frames từ output để verify visually:
```bash
ffmpeg -y -ss 10 -i final.mp4 -frames:v 1 /tmp/verify_t10s.jpg
```

Dùng `vision_analyze` xác nhận: face visible, PIP đúng vị trí, mặt rõ.

---

## 🎯 CASE STUDY: CLIP_0004 (test 19/07/2026)

### Step-by-step:

1. **Find file**: `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0004_V3_85s_FINAL_DJI_source.mp4` (71.2 MB, 85.9s)
2. **FFprobe**: H.264 1080×1920 + AAC 44100Hz, duration 85.9s
3. **Wiki check** (Key #1): Tìm `wiki/projects/tuan-anh-review-tiktok/products/` — KHÔNG CÓ OTOBOP
4. **Extract 9 frames** tại 0s/8s/15s/25s/35s/45s/60s/75s/85s
5. **MẮT phân tích**:
   - t=15s: **OTOBOP máy sấy tóc** (màu đen + đồng, logo "otobob" rõ)
   - t=35s: OTOBOP cầm ngang, có phụ kiện
   - t=45s: OTOBOP cầm lên cao
   - t=75s: OTOBOP close-up
6. **TAI nghe** (Whisper): "máy hút bụi Doroto E Luxe V3, 25.000 bát canh"
7. **Cross-check**: 3 nguồn DISAGREE
   - Visual: OTOBOP
   - Whisper: Doroto
   - Wiki: chỉ có Doroto (match Whisper)
8. **Action**: **DỪNG LẠI verify với anh trước khi build motion**

### Phát hiện quan trọng:

- **Tên file sai**: `clip_0004_V3_85s_FINAL_DJI_source` — KHÔNG phải DJI Pocket 3
- **Whisper sai**: nghe nhầm "OTOBOP" thành "Doroto" (âm thanh giống nhau?)
- **Clip có thể chứa nhiều sản phẩm** (nhưng visual chỉ thấy 1)

---

## ⚠️ ANTI-PATTERN (KHÔNG ĐƯỢC LÀM)

- ❌ Đọc transcript text thuần rồi build motion mà KHÔNG xem video
- ❌ Tin Whisper 100% (hallucinate với tiếng Việt)
- ❌ Dùng template "mọi clip đều có CHART/PORT/USP/TESTIMONIAL" mà không phân tích transcript cụ thể
- ❌ Skip bước chụp frame → bỏ lỡ visual cues quan trọng
- ❌ Build motion ngay khi có 3 nguồn (mắt + tai + wiki) DISAGREE
- ❌ Tự ý dùng wiki khác sản phẩm (vì chỉ có 1 wiki match Whisper)
- ❌ Bỏ qua vì "tên file clip đã rõ" — tên file có thể sai (như clip_0004)

---

## 🎯 CHECKLIST TRƯỚC MỖI CLIP

```
□ 1. Find file + ffprobe (duration, codec, resolution)
□ 2. CHECK WIKI (Key #1) — sản phẩm có trong wiki không?
□ 3. EXTRACT 5-10 frames tại các timestamp quan trọng
□ 4. MẮT phân tích từng frame (visual cues)
□ 5. WHISPER audio → transcript text
□ 6. CROSS-VERIFY mắt + tai + wiki — nếu 3 nguồn disagree → DỪNG verify với anh
□ 7. TƯ DUY đặt câu hỏi (đoạn nào cần card, animation gì)
□ 8. Lên plan motion (số phase, loại card, timing)
□ 9. Build HTML + GSAP với 8 KEY CHÍNH check
□ 10. Render + CHỤP ảnh verify visually
```

---

## 📝 TÍCH HỢP VỚI 8 KEY CHÍNH (MASTER PHILOSOPHY)

- **Key #1 (WIKI)**: check thông tin sản phẩm trong wiki
- **Key #2 (TRANSCRIPT)**: đọc transcript text + cross-verify với mắt
- **Key #3 (SÁNG TẠO)**: dùng mắt + tai + tư duy để tạo điểm sáng tạo
- **Key #4-#8 (KỸ THUẬT)**: face zone, safe zone, card zone, PIP method, HyperFrames

→ **Nâng cấp Key #1 + #2 + #3**: không chỉ đọc text, mà PHẢI:
- MẮT xem video
- TAI nghe audio
- TƯ DUY hỏi câu hỏi
- CROSS-VERIFY 3 nguồn
- DỪNG LẠI khi disagree

→ **Key #9 mới (đề xuất)**: CROSS-VERIFY mắt + tai + wiki trước khi build. Nếu 3 nguồn disagree → STOP + verify với anh.

---

## 🛠️ TOOLS CẦN DÙNG

- **ffmpeg** — extract frames, ffprobe
- **vision_analyze** — phân tích visual
- **mlx_whisper** — transcribe audio
- **wiki-product-ground-truth skill** — tạo wiki mới khi cần
- **tiktok-product-motion-graphics skill** — main skill

---

## 🔗 RELATED REFERENCES

- `references/v18-pip-method-chinh-thuc.md` — V18 PIP method (chính thức)
- `references/v84-face-safe-zone-pre-build-pixel-scan-2026-07-18.md` — Face zone protocol
- `references/v100-pixel-bbox-verification-mandatory-2026-07-19.md` — Pixel bbox verification
- Skill `wiki-product-ground-truth` — Tạo wiki product mới

---

*Compiled from clip_0004 case study 19/07/2026 + 8 KEY CHÍNH master philosophy.*
