---
name: tiktok-product-motion-graphics
description: Class-level umbrella for building TikTok Shop / product-review videos where a person talks on camera AND motion graphics sync to their voice. Use when Tuấn Anh shares a talking-head product clip + asks for motion graphics / liquid glass / charts / kinetic text overlay. NOT for pure-fullscreen brand promos or pure subtitle/vlog track.
tags:
  - tiktok
  - hyperframes
  - motion-graphics
  - product-video
  - liquid-glass
  - v22-verified-layout
  - v71-default-opacity-018
  - canonical-default-config
  - v84-face-safe-zone
  - v84-pixel-scan-pre-build
related_skills:
  - tiktok-video-editor
  - tiktok-verify-protocol
  - tiktok-product-script
  - transcript-cleanup
  - telegram-video-analysis
  - hyperframes-cli
  - hyperframes-core
  - hyperframes-animation
  - hyperframes-creative
  - wiki-product-ground-truth
---

# TikTok Product Motion Graphics

## ⭐ START HERE — Quick Load Order

1. **`references/master-philosophy-8-key-chinh.md`** — Tổng hợp 8 KEY CHÍNH (load trước mọi build)
2. **`references/clip-analysis-protocol-19-07-2026.md`** — 6 bước HARD RULE (mắt + tai + wiki)
3. **`references/case-study-clip_0004-audio-video-mismatch-detect-2026-07-19.md`** — PITFALL #50 (file bị ghép nhầm audio)
4. **`references/case-study-clip_0004-voice-goc-vs-tts-2026-07-19.md`** — PITFALL #99 (luôn voice gốc)
5. **`references/v13-pip-position-method.md`** — V13 PIP method (single source-of-truth)

---

## ⭐ MASTER PHILOSOPHY — 10 KEY CHÍNH (load this first)

> **Anh đã dạy (19/07/2026):** *"Face zone, safe zone, card zone, PIP method + quy trình HyperFrames + ffmpeg là các key chính. Trước khi làm motion phải check wiki/products. Card phải xác định từ transcript video, không copy-paste giữa các clip. Đề cao sáng tạo, dùng mắt + tai + tư duy!"*

### 🎯 10 KEY CHÍNH (BẮT BUỘC — KHÔNG ĐƯỢC THAY ĐỔI)

| # | Key | Source | Why cứng |
|---|---|---|---|
| **1** | **WIKI PRODUCT RESEARCH FIRST** | [18/07 WIKI-PRODUCT-GROUND-TRUTH] | Check `wiki/projects/tuan-anh-review-tiktok/products/[name].md` TRƯỚC khi viết script/motion. Citation [N] map về wiki. Sai specs = mất trust khách. |
| **2** | **CARD CONTENT TỪ TRANSCRIPT** | [19/07 SÁNG TẠO] | Mỗi card phải xác định từ transcript video. KHÔNG template "mọi clip đều có CHART/PORT/USP". |
| **3** | **SÁNG TẠO + ĐA DẠNG** | [19/07 SÁNG TẠO] | Dùng MẮT + TAI + TƯ DUY. Mỗi clip có 1-3 điểm sáng tạo riêng. KHÔNG lặp lại. |
| **4** | **FACE ZONE** (vùng cấm mặt) | V85 RECAP | y=547-1140, x=308-1526. KHÔNG đặt card ở vùng mặt trừ khi có PIP. |
| **5** | **SAFE ZONE 10%** mỗi cạnh | V83 RECAP | Mọi element trong margin 10% (top/bottom 192px, left/right 108px ở 1080×1920). |
| **6** | **CARD ZONE** (vị trí glass card) | V82 + V84 RECAP | HOOK/PROBLEM/PRODUCT/USP → bottom (y > 1280). TESTIMONIAL/FEATURE → top (y < 547). CHART/PORT → giữa (y = 966). CTA → center 80%. |
| **7** | **PIP METHOD** (V18/V13 chính thức) | V96 RECAP | 1 video + GSAP keyframe `scale: 0.42, x: ±222, y: -540, borderRadius: 28`. CHART top-left, PORT top-right. |
| **8** | **QUY TRÌNH HYPERFRAMES + FFMPEG** | V22 + V96 | Render silent mp4 → ffmpeg ghép audio cuối. KHÔNG BAO GIỜ dùng `format=yuva420p` overlay cho glass. |
| **9** | **CROSS-VERIFY MẮT + TAI + WIKI** | [19/07 KEY #9] | Khi 3 nguồn disagree → DỪNG, HỎI ANH. Whisper có thể SAI về cả sản phẩm. |
| **10** | **VERIFY FILE SOURCE TỪ RAW FOOTAGES** | [19/07 KEY #10] | Tìm file RAW từ `/Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4`. File Final_ có thể bị ghép nhầm audio. |
| **11** | **CLEAN DELETE — REMOVE HẲN khỏi code + skill + memory** | [26/07 NO-FADE-CLEAN-DELETE] | Khi anh nói "bỏ X đi" → REMOVE hẳn KHÔNG để comment "REMOVED"/"deprecated". Verify: `grep -nE 'X'` chỉ còn 1 mention giải thích HARD RULE. |
| **12** | **ZOOM EFFECT = KEYFRAME-BASED ≥1.4x** | [26/07 ZOOM-FRAMEWORK-3-TESTS] | Pocket 3 portrait source = tight baseline (mặt 50%+). Zoom linear 1.25x INVISIBLE. Dùng keyframe `1.0→1.3→1.4` với breakpoint @ 40%, mới visible. Verify bằng objective frame compare + file size delta. |

### 🎨 CÁC THỨ KHÁC (OPTIONAL — CÓ THỂ THAY ĐỔI)

| Thứ | Ai quyết |
|---|---|
| Số phase, thứ tự phase | Transcript video |
| Loại card (chart/port/testimonial/feature/usecase/cta) | Transcript + sáng tạo |
| Pop up timing | Transcript cues |
| Content card | Wiki research + sáng tạo |
| Màu glass card (border, opacity) | Anh |
| Glass recipe (blur, shadow, border-radius) | Nate Herk style |
| Font (SF Pro, Inter, Caveat) | Anh / brand |
| Easing (back.out, power2.out, sine.inOut) | Edit style |
| PIP scale (0.42) | Edit style |
| PIP position (x ±222, y -540) | Edit style |

### 🚦 DECISION TREE KHI BẮT ĐẦU CLIP MỚI

```
Anh gửi clip raw + brief (optional)
    ↓
1. ⭐ CHECK WIKI PRODUCT RESEARCH (Key #1)
   - Sản phẩm gì? → check wiki/products/[name].md
    ↓
2. ⭐ TÌM FILE SOURCE TỪ RAW FOOTAGES (Key #10)
   - /Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4
   - File này có video + audio cùng 1 nguồn
   - File Final_ trong Hermes-Edit có thể đã bị ghép nhầm audio
    ↓
3. ⭐ ĐỌC TRANSCRIPT BẰNG MẮT + TAI (Key #2, #3, #9)
   - MẮT xem video: mặt anh làm gì? cầm gì? logo gì?
   - TAI nghe audio: keyword nào? nhấn mạnh chỗ nào?
   - Nếu MẮT vs TAI disagree → DỪNG, hỏi anh
    ↓
4. Source video có talking head motion?
   - CÓ → V22 workflow
   - GẦN static → **KEYFRAME zoom 1.0→1.3→1.4** (xem `references/pitfall-pocket3-portrait-zoom-keyframe-2026-07-26.md`). Linear zoom 1.25x INVISIBLE trên Pocket 3 source — phải keyframe + scale ≥1.4x.
    ↓
5. ⭐ ĐỀ XUẤT PLAN MOTION (Key #3 - sáng tạo)
   - Cần thông số kỹ thuật? → CHART (NHƯNG chỉ khi transcript có spec)
   - Cần quy trình sử dụng? → PORT (chỉ khi transcript có steps)
   - KHÔNG ép tất cả phase vào 1 clip
    ↓
6. VẼ layout timeline (anh duyệt)
    ↓
7. Build HTML + GSAP timeline với 6 CHECK:
   - Wiki (Key #1), Transcript (Key #2), Sáng tạo (Key #3)
   - Cross-verify (Key #9), Source file (Key #10)
   - Face zone (Key #4), Safe zone (Key #5), Card zone (Key #6)
   - PIP method (Key #7), HyperFrames workflow (Key #8)
    ↓
8. ⭐ DÙNG VOICE GỐC từ source (không TTS)
   - Extract audio từ source.mp4
   - Stretch bằng atempo nếu duration mismatch
    ↓
9. Render silent → ffmpeg ghép voice gốc → ship
   - Verify file ở Hermes-Edit
```

---

## 🔴 PITFALL #46 — WHISPER SAI VỀ SẢN PHẨM (added 19/07/2026)

| Sai lầm | Ví dụ clip_0004 |
|---|---|
| Whisper nghe "Doroto" nhưng thật ra là "Dodoto" | Sai brand name |
| Whisper nói "máy hút bụi" nhưng thật ra là "tấm tháo lắp nhanh" | **Sai cả sản phẩm** |
| Whisper nói "25.000 bát canh" nhưng thật ra là "25.000 Pa" | Sai đơn vị + brand |
| Whisper nói "4000 mAh" đúng | (Đôi khi vẫn đúng về spec) |

**Quy tắc:**
1. **WIKI = ground truth** (đã có citation [N])
2. **VISUAL = mắt thấy** (anh confirm)
3. **WHISPER = chỉ tham khảo audio cues** — KHÔNG TIN SẢN PHẨM
4. **Nếu 3 nguồn disagree** → HỎI ANH, KHÔNG ARGUE

## 🔴 PITFALL #49 — KHI ANH KHÔNG RESPOND, DỪNG LẠI (added 19/07/2026)

**Khi em clarify hỏi anh mà anh KHÔNG RESPOND trong 10 phút:**

1. ❌ **KHÔNG** tự ý build dựa trên 1 nguồn
2. ❌ **KHÔNG** build "draft" để "xem thử"
3. ❌ **KHÔNG** xóa version cũ khi chưa có confirm
4. ✅ **DỪNG LẠI** + giữ nguyên trạng thái hiện tại
5. ✅ **Log vào wiki/queries/** với status "ĐANG CHỜ ANH CONFIRM"
6. ✅ **Hỏi lại** sau 10-15 phút nếu anh vẫn không respond

## 🔴 PITFALL #50 — FILE BỊ GHÉP NHẦM AUDIO + VIDEO (added 19/07/2026)

**Context (clip_0004 case study 19/07):** Em verify bằng 3 nguồn độc lập:

| Nguồn | Sản phẩm |
|---|---|
| Whisper audio (40 segments) | "Dodoto Luxe V3" (máy hút bụi) |
| Visual RAW frame t=80s | **"otobob"** máy sấy tóc |
| Visual RAW frame t=200s | **"otobob"** máy sấy tóc close-up |

→ **3 nguồn DISAGREE 100%** — file gốc đã bị ghép nhầm audio từ clip khác.

### WORKFLOW KHI NGHI NGỜ AUDIO ≠ VISUAL:

```bash
# Step 1: Verify MD5 file
md5 file_hermes_edit.mp4 file_pipeline_copy.mp4
# Nếu khác → 2 version khác nhau

# Step 2: Extract voice gốc từ cả 2 file
ffmpeg -y -i file_a.mp4 -vn -c:a aac -b:a 192k audio_a.aac
ffmpeg -y -i file_b.mp4 -vn -c:a aac -b:a 192k audio_b.aac
md5 audio_a.aac audio_b.aac

# Step 3: Visual verify 10+ frames
for t in 0 10 20 30 40 50 60 70 80 90; do
  ffmpeg -y -ss $t -i file.mp4 -frames:v 1 frame_t${t}.jpg
  # vision_analyze mỗi frame
done
```

### BÀI HỌC:

1. **VERIFY 3 NGUỒN** (WIKI + MẮT + TAI) trước khi build
2. **MẮT > TAI** khi conflict
3. **File có thể bị ghép nhầm audio** từ clip khác
4. **DÙNG VOICE GỐC** (PITFALL #99)
5. **DỪNG LẠI** khi không chắc chắn

## 🔴 PITFALL #99 — LUÔN DÙNG VOICE GỐC KHI BUILD MOTION TỪ RAW CLIP (added 19/07/2026)

**Anh dặy (verbatim 19/07/2026):** *"Dùng voice gốc của anh luôn đâu cần dùng edge tts đâu"*

```bash
# Extract voice gốc từ source
ffmpeg -y -i source.mp4 -vn -c:a aac -b:a 192k -ar 44100 audio_goc.aac

# Stretch bằng atempo nếu duration mismatch
# Audio 86.95s, video 85.0s → atempo = 1.023
ffmpeg -y -i audio_goc.aac -filter:a "atempo=1.023" -c:a aac -b:a 192k audio.aac

# Verify
ffprobe -v error -show_entries format=duration audio.aac
# Phải = video duration
```

**KHÔNG tự ý thay Edge TTS khi:**
- Audio gốc vẫn dùng được
- Build motion từ raw clip

**Edge TTS chỉ dùng khi:**
- Test demo ngắn
- Edit audio cho content khác
- Audio gốc bị lỗi
- Anh explicit yêu cầu TTS

### CASE STUDY: clip_0004 V19 → V20 → V21

| Version | Audio | Sản phẩm | Đúng? |
|---|---|---|---|
| V19 | Whisper audio gốc (sai nội dung) | otobob | ❌ |
| V20 | Edge TTS (đoán lung) | otobob | ❌ |
| V21 | **Voice gốc** + ULANZI MA66 đúng | otobob | ⚠️ |

## 🔴 KEY #10 — VERIFY FILE SOURCE TỪ RAW FOOTAGES (added 19/07/2026)

**Anh dặn:** *"...dùng voice gốc của anh luôn đâu cần dùng edge tts đâu"* + *"Tìm lại đúng tên clip này để làm motion lại từ đâu"*

### WORKFLOW BẮT BUỘC TRƯỚC MỌI BUILD:

```
1. Tìm RAW source từ /Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4
2. Verify audio + visual + wiki KHỚP NHAU
3. Nếu 3 nguồn DISAGREE → DỪNG, hỏi anh
4. Nếu đã có file Final_ mà nghi ngờ sai:
   - Verify MD5 vs pipeline copy
   - Extract audio từ Hermes-Edit
   - Extract audio từ RAW DJI Footages/
   - Compare MD5
```

### BẮT BUỘC KHI BUILD MOTION:

```bash
# Bước 1: Tìm source gốc
ls /Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4 | grep "0004"

# Bước 2: Compare MD5
md5 file_hermes.mp4 file_pipeline.mp4

# Bước 3: Whisper audio
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi ...

# Bước 4: Visual verify 10+ frames
```

---

## 🔴 HARD RULES (existing, verified by multiple V*_recap)

### V13 PIP METHOD (chính thức — anh approved)
```javascript
// 1 video element duy nhất + GSAP keyframe scale + position
tl.to(videoClip, { scale: 0.42, x: -222, y: -540, borderRadius: 28, duration: 0.6 }, 7.0);   // CHART top-left
tl.to(videoClip, { scale: 0.42, x: 222, y: -540, borderRadius: 28, duration: 0.6 }, 19.0);    // PORT top-right
tl.to(videoClip, { scale: 1, x: 0, y: 0, borderRadius: 0, duration: 0.5 }, 12.8);            // Reset
```

**V18 VERIFY (pixel check):**
- CHART bbox (45,50)-(272,399) TOP-LEFT ✅
- PORT bbox (267,50)-(494,399) TOP-RIGHT ✅
- Mặt + glass card hiển thị CÙNG LÚC ✅
- Phần ngoài PIP = nền đen (V13 đúng)

**❌ ANTI-PATTERNS (đã fail):**
- ❌ `scaleX/scaleY` non-uniform (V14) - méo mặt
- ❌ `x: -16, y: -130` (V15) - sai vị trí
- ❌ `clipPath: 'inset(...)'` (V16) - KHÔNG apply
- ❌ `<div class="pip-wrap">` wrapper (V17/V95) - dư

### GSAP FADE-IN INITIAL STATE (CRITICAL #0)
```css
.cta-glass, .chart-glass, .port-glass, .usp-glass, .testimonial-glass,
.feature-glass, .usecase-glass, .product-glass, .problem-glass, .hook-glass {
  opacity: 0;  /* BẮT BUỘC - GSAP tl.fromTo() không tự set initial */
}
```

### SHIP-VERIFY-OR-LIE
Sau MỌI ffmpeg/cp/render: `ls -la final.mp4` + `ffprobe` confirm. `subprocess.run` returncode=0 ≠ file tồn tại.

### ROOT CAUSE INVESTIGATION (khi anh flag "có gì đó bị che/overlap")
1. List `z-index` TẤT CẢ elements
2. Check opacity initial state
3. Check position absolute
4. Check background opacity
5. PNG extract + sample pixel bounds TRỰC TIẾP

---

## 📁 CRITICAL REFERENCES (linked)

**Canonical:**
- `references/master-philosophy-8-key-chinh.md` ⭐ — 8 KEY CHÍNH tổng hợp
- `references/v13-pip-position-method.md` ⭐ — V13 PIP source-of-truth
- `references/v18-pip-method-chinh-thuc.md` — V18 historical

**NEW (added 26/07):**
- `references/clean-delete-pattern-2026-07-26.md` ⭐ — Khi anh nói "bỏ X đi" → REMOVE hẳn, không để comment "REMOVED"
- `references/pitfall-pocket3-portrait-zoom-keyframe-2026-07-26.md` ⭐ — Zoom linear 1.25x INVISIBLE trên Pocket 3 portrait source, dùng keyframe 1.0→1.3→1.4
- `references/case-study-clip_0004-audio-video-mismatch-detect-2026-07-19.md` — PITFALL #50 case study
- `references/case-study-clip_0004-voice-goc-vs-tts-2026-07-19.md` — PITFALL #99 case study
- `references/clip-analysis-protocol-19-07-2026.md` — 6 bước HARD RULE

**CRITICAL pre-build reads:**
- `references/v84-face-safe-zone-pre-build-pixel-scan-2026-07-18.md`
- `references/motion-static-video-pitfall.md`
- `references/verify-protocol-multi-region.md`

---

## 🟢 SHIPPED FILES (verified 19/07/2026)

| File | Status | Note |
|---|---|---|
| `clip_0006_V18_100s_FINAL_V13_METHOD.mp4` (54.6 MB) | ✅ anh approved V18 | 1 video + GSAP keyframe, voice gốc |
| `clip_0004_V21_85s_FINAL_ULANZI_MA66.mp4` (46.4 MB) | ⚠️ voice gốc nhưng SP cuối là otobob | Sẽ rebuild khi anh confirm SP thật |

---

## 🛠️ WORKSPACE CONVENTION (PITFALL #91)

| Loại | Path |
|---|---|
| **Work** (HyperFrames projects) | `/Volumes/Storage-1/Hermes/scratch/hf_<name>/` |
| **Final** (shipped MP4) | `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_*.mp4` |
| **Source RAW** (Pocket3) | `/Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4` |
| **Wiki** | `/Volumes/Storage-1/Hermes/wiki/` |
| **Skill** | `~/.hermes/skills/media/` |

**KHÔNG dùng /tmp** vì disk cap 228GB, đầy nhanh.

---

## 📚 VERSION-SPECIFIC HISTORICAL RECAPS

(V18-V95 đã archive trong references, KHÔNG dùng cho build mới)
