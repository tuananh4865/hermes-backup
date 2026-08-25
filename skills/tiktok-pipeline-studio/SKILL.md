---
name: tiktok-pipeline-studio
description: >
  End-to-end TikTok video pipeline: raw footage → cut filler → motion graphic → final MP4.
  Orchestrates 4 skills in sequence: (1) video-use for raw editing, (2) tiktok-video-editor
  for MODE B 95-120s trim/speed, (3) tiktok-product-motion-graphics or hyperframes for motion,
  (4) tiktok-verify-protocol for QA gate. v1.2.0 (19/07) — EDIT-ONLY mode (PITFALL #41): SKIP Stage 4 khi anh yêu cầu "edit thôi" / "không cần subtitle/motion". EDIT-FROM-DJI-SOURCE workflow (PITFALL #42) + 5-EVIDENCE subagent parallel. v1.1.0 (18/07) — 9 video-use tools.
author: 'Tuấn Anh + Hermes Agent (v1.2.0 19/07/2026 — Add EDIT-ONLY mode (PITFALL #41): SKIP Stage 4 khi anh yêu cầu "edit thôi" / "không cần subtitle/motion". v1.1.1 19/07/2026 — Add 5-EVIDENCE subagent parallel + EDIT-FROM-DJI-SOURCE (PITFALL #42). v1.1.0 18/07/2026 — 9 video-use tools + Hermes-Edit migration. v1.0.0 18/07/2026 — first validation.)'
license: MIT
platforms: [macos]
metadata:
  category: media
  tags: [pipeline, orchestration, tiktok, video-edit, motion-graphics, v3.21.5, video-use-inspired, edl-json, audio-fade-check, quality-ladder, folder-migration, edit-only, edit-from-dji-source, 5-evidence]
---

# TikTok Video Pipeline Studio (v1.2.0 — 19/07/2026)

> **🎯 USE THIS SKILL WHEN (4 trigger patterns):**
> 1. **Full pipeline:** Anh drops a raw video file vào một folder rồi nói
>    "edit clip này + thêm motion graphic + xuất final MP4" — pipeline tự động end-to-end
>    từ raw → final.
> 2. **HyperFrames motion graphic alone:** Anh hỏi "làm motion graphic bằng HyperFrames như thế nào"
>    hoặc "dùng HyperFrames để add animation vào clip" → CHỈ chạy Stage 4 + 5 (skip Stage 2-3),
>    xem section "Stage 4-only quick path" bên dưới.
> 3. **Câu hỏi forensic về version đã ship:** Anh hỏi "check lại V22 / V77 / clip_xxx em đã làm
>    cách nào" → đọc skill `tiktok-product-motion-graphics` section "V22 PIP + GLASS WORKFLOW
>    CHÍNH GỐC" + reference `references/v22-canonical-workflow-summary.md` (1 trang forensic).
> 4. **EDIT-ONLY mode (PITFALL #41 — NEW 19/07):** Anh nói "edit thôi" / "chỉ cần edit" / "không cần subtitle"
>    / "không cần motion graphic" → SKIP Stage 4 entirely. CHỈ chạy Stage 1+2+3+5.

> **⚠ MỤC ĐÍCH:** Single entry point orchestrate 4 skills đã có. KHÔNG duplicate
> logic của các skill con. Mỗi skill con vẫn là source-of-truth cho stage của nó.

## Pipeline Overview — 5 Stages

```
┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌─────────────┐   ┌──────────────┐
│ STAGE 1     │   │ STAGE 2     │   │ STAGE 3     │   │ STAGE 4     │   │ STAGE 5      │
│ INVENTORY   │──▶│ TRANSCRIBE  │──▶│ EDIT        │──▶│ MOTION      │──▶│ VERIFY + SHIP│
│             │   │ + CUT       │   │ (MODE B)    │   │ GRAPHIC     │   │              │
│ Source:     │   │ Source:     │   │ Source:     │   │ Source:     │   │ Source:      │
│ raw.mp4     │   │ video-use + │   │ tiktok-     │   │ tiktok-     │   │ tiktok-      │
│ (Pocket3,   │   │ tiktok-     │   │ video-      │   │ product-    │   │ verify-      │
│ iPhone, etc)│   │ video-editor│   │ editor      │   │ motion-     │   │ protocol     │
│             │   │             │   │             │   │ graphics    │   │              │
│ Output:     │   │ Output:     │   │ Output:     │   │ Output:     │   │ Output:      │
│ ~/raw/      │   │ ~/stage2/   │   │ ~/stage3/   │   │ ~/stage4/   │   │ ~/stage5/    │
│ edit-ready  │   │ transcript  │   │ cut 95-120s │   │ motion MP4  │   │ final MP4    │
└─────────────┘   └─────────────┘   └─────────────┘   └─────────────┘   └──────────────┘
                                  SKIP IF ANH DA                    SKIP IF anh
                                  CHON "EDIT MODE A"               KHONG CAN MOTION
```

## Stage 1 — INVENTORY (2 calls)

**Làm gì:** Survey raw footage, xác định format (resolution, codec, duration, audio),
xác định chất lượng motion (pixel diff tại 4 vùng).

```bash
ffprobe -v error -show_format -show_streams raw.mp4
```

Verify:
- 1080×1920 hoặc 1728×3072 source (portrait)
- H.264 + AAC
- ≥30fps
- Duration bất kỳ

**Output flag:** Nếu source là HEVC 1728×3072 (Pocket 3 chế độ chân dung 4K) → flag
cho Stage 3 (cần Pitfall #23 HEVC scale).

## Stage 2 — TRANSCRIBE + FILLER CUT (5 calls)

**Skill:** `~/.hermes/skills/media/tiktok-video-editor/` (v3.29.0 anh dặn 17/07 — Mode B default)

**Workflow:**
1. `mlx_whisper --model mlx-community/whisper-medium-mlx --language vi --word-timestamps True --output-dir ./whisper_out source.mp4`
2. Auto-classify transcript đầy đủ ra `transcript_full.md`
3. Manual review — đọc 5 nhóm lỗi narrative: HOOK lặp 3+ từ, SOURCE-LOOP, TREO >5s, ỰM Ỡ, FILLER dài nối
4. Apply 7 KEY INSIGHTS (v3.20.0) self-check cho MỖI keep: BRIDGE 0.5-3s, USP riêng 1 keep, USP_PROOF, LẶP CỐ Ý emphasis, SILENT GAP 5-10s, HOOK take punchy nhất, SỐ LIỆU CỤ THỂ
5. FILLER TRIM (ơ, ờ, ừm, ừ, ó, à, á) + TREO + LẶP keep cuối

**Optional video-use integration:** Nếu anh muốn dùng video-use thay vì tiktok-video-editor
cho Stage 2, xem section "video-use integration" bên dưới. Trade-off:

| Mode | Skill | Strength | Weakness |
|---|---|---|---|
| Quick cut filler nhanh | `video-use` (ElevenLabs Scribe + LLM EDL) | 1 hỏi LLM → tự build EDL → render | Cần ElevenLabs API key, không customize được 7 KEY INSIGHTS |
| Deep edit đúng gu anh | `tiktok-video-editor` v3.29.0 | 7 KEY INSIGHTS + 26 Pitfall + 5 phase templates | Phải transcribe manually với Whisper |

**Default = tiktok-video-editor.** Chỉ switch sang video-use khi anh explicit "dùng
video-use" hoặc "AI tự edit cho anh" (lazy mode).

## Stage 3 — MODE B CUT (5 calls)

**Skill:** `~/.hermes/skills/media/tiktok-video-editor/` (tiếp)

**Workflow:**
1. Render V1 trim từ keep_plan (Pitfall #24 — dùng SOURCE timestamps, không V1 timestamps)
2. Apply SPEED 1.3x (Pitfall #26 — MANDATORY bước cuối) với `setpts=PTS/1.3` + `atempo=1.3`
3. Render tên file: `clip_<id>_V<N>_troncau_<ten-san-pham>_speed13.mp4`
4. Whisper lại OUTPUT (re-Whisper verify) — check HOOK_LAP, NSP, câu treo
5. Adjust nếu cần

**Target:** 95-120s (Mode B sweet spot). Nếu source > 300s + > 20 features
→ TRỌN-CÂU selection (Pitfall #41) + accept 20-40% feature loss.

## Stage 4 — MOTION GRAPHIC (10-50 calls)

**3 options:**

### Option A — LIQUID GLASS V22 (skill `tiktok-product-motion-graphics`, v3.21.5)

Best for: TikTok product review dọc 1080×1920, có PIP + glass cards show specs.

```bash
# Workflow V22 chính gốc (verified):
# 1. source mp4 no audio → assets/source/full_bg.mp4
# 2. 4 video elements direct child of root (video-bg + pip-chart + pip-usp + pip-final)
# 3. HTML có glass cards (KHÔNG qua ffmpeg overlay)
# 4. JS: pause videos + paused timeline + seek(0)
# 5. npx hyperframes render --format mov --output output_silent.mov
# 6. ffmpeg ghép audio cuối (KHÔNG overlay video)
```

Xem full spec ở `wiki/projects/content-creator/layout-benchmark-vertical-tiktok-1080x1920.md`
(19.8KB) + skill tiktok-product-motion-graphics v3.21.5.

### Option B — TIKTOK SUBTITLE/MOTION TEXT (skill creative/hyperframes)

Best for: TikTok talking-head video, cần word-level subtitle sync voice.

Xem skill creative/hyperframes § "TikTok Subtitle Workflow" / "TikTok Motion Text Workflow".

```bash
# 5-step pipeline:
# 1. Whisper word-level JSON
# 2. Build phrases.json (4 words/phrase, 1-word overlap)
# 3. npx hyperframes init --example=blank
# 4. Author sub-composition tiktok-subtitle.html (in host root + data-composition-src)
# 5. npx hyperframes render --quality draft
```

⚠ HyperFrames silent crash nếu >40 phrases DOM (Pitfall § HF-TikTok-Subtitle 1).

### Option C — SKIP STAGE 4

Nếu clip đã đủ tốt ở Stage 3 V1 speed 1.3x (95-120s, không lỗi verify), ship thẳng
vào Hermes-Edit. Motion graphic chỉ cần khi:
- Cần show specs (chart/USP details)
- Cần hook 3s đầu nổi bật
- Cần brand watermark + text motion

## Stage 4-only Quick Path (khi anh hỏi HyperFrames workflow alone)

**Trigger:** Anh đã có clip edit sẵn (Stage 3 output) hoặc có raw source, muốn CHỈ thêm
motion graphic qua HyperFrames. Skip Stage 2-3.

### 🔴 BẮT BUỘC TRƯỚC KHI BẮT ĐẦU: LEARN-FULL PROTOCOL (anh explicit 19/07)

> **Anh flag 19/07/2026:** *"Hôm qua em làm 0003_v84 được mà sao hôm nay lại không làm được, hôn qua anh đã bảo em phải learn full rồi mà"*
> **Anh command 19/07/2026:** *"Learn full và biến mọi rule thành hard rule"*

**BẮT BUỘC** trước mọi Stage 4 motion graphic build:

```bash
# Step 0 — LEARN FULL: ĐỌC SKILL TRƯỚC KHI BUILD
cat ~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md | head -200
# → Tìm tất cả "V## RECAP" sections trong skill
# → Extract HARD RULE checklist (15 rules từ V85-V87: safe zone, vùng cấm mặt,
#    countUp integer, CTA canh giữa, PIP structure, opacity 0.18, STAMP, etc.)
```

**Workflow:**
1. **ĐỌC skill TRƯỚC** — không đoán, không patch shortcut
2. **EXTRACT checklist** các hard rule từ RECAP sections (V78→V87)
3. **VERIFY source** bằng ffprobe + sample 3 frames motion ≥ 10%
4. **BUILD HTML** theo checklist từng rule một
5. **VERIFY từng rule** bằng pixel diff + scan rows + face region
6. **SHIP** chỉ sau khi tất cả rule pass

**Anti-pattern (em đã waste 3 versions vì skip step 0):**
- ❌ Build trước, check skill sau → V5/V6 fail
- ❌ Dùng memory cũ (compacted) thay vì đọc skill
- ❌ Skip checklist, patch ngay khi fail

**Real case 19/07 clip_0006:** V5 (35.3 MB) fail, V6 (29.1 MB) fail. V7 (52.5 MB) pass 14/15 HR chỉ sau khi em đọc V86 RECAP → extract 15 HR checklist → build theo từng rule.

### 7-step workflow (verified từ V22 thực chiến 17/07)

```bash
# Step 1 — INIT PROJECT (must use --example flag in non-interactive mode v0.7.60+)
mkdir -p /tmp/hf_<tên-clip> && cd /tmp/hf_<tên-clip>
npx --yes hyperframes init --non-interactive --example=blank
# Options: blank / kinetic-type / ios26-liquid-glass

# Step 2 — CHUẨN BỊ ASSET (relative path required, headless Chrome can't access file://)
mkdir -p assets/source
cp /Volumes/Storage-1/Pocket3/Hermes-Edit/<clip>_speed13.mp4 assets/source/full_bg.mp4

# Step 3 — AUTHOR HTML (~30-100 dòng, có 4 video elements direct child of root)
# Xem template ở skill tiktok-product-motion-graphics/templates/ hoặc copy từ
# case study V22 (wiki/projects/content-creator/sac-du-phong-mini-iphone-22-versions-case-study.md)

# Step 4 — LINT + CHECK (2 gates bắt buộc)
npx hyperframes lint        # 0 errors / 0 warnings
npx hyperframes check --snapshots   # visual gate

# Step 5 — PREVIEW (HyperFrames bắt buộc pause ở đây — KHÔNG render merely because checks pass)
npx hyperframes preview      # Studio mở browser, hỏi anh duyệt

# Step 6 — RENDER SILENT
npx hyperframes render --quality high --output final_silent.mp4

# Step 7 — GHÉP AUDIO + SHIP (ffmpeg chỉ ghép audio cuối, KHÔNG overlay video)
ffmpeg -y \
  -i final_silent.mp4 \
  -i /Volumes/Storage-1/Pocket3/Hermes-Edit/<clip>_speed13.mp4 \
  -c:v copy -c:a aac -b:a 128k -shortest \
  /Volumes/Storage-1/Pocket3/Hermes-Edit/<clip>_FINAL_motion.mp4

# Verify motion (anh đã dặn 17/07: mọi pixel phải move)
python3 ~/.hermes/skills/media/tiktok-product-motion-graphics/scripts/motion_diff_check.py \
  <clip>_FINAL_motion.mp4 --t1 0.0 --t2 0.3
# >30% = excellent motion, <5% = FAIL (frozen content)
```

**5 hard rules (verified từ 22 versions V1-V22):**
1. `<video>` PHẢI có `id="..."` (không chỉ class) → renderer cần `getElementById`
2. Timeline PHẢI register `window.__timelines["<id>"] = tl` với id trùng `data-composition-id`
3. Pause + seek(0) video TRƯỚC KHI render — HyperFrames KHÔNG play HTML video bg nếu không pause
4. Glass card recipe V22: `rgba(255,255,255,0.15)` + `blur(40px) saturate(180%)` + border `0.4`
5. Source 1728×3072 HEVC (Pocket 3 4K chân dung) → scale 1080×1920 TRONG `filter_complex` per-segment,
   KHÔNG mix `-vf scale` với `-filter_complex` output

**Workflow compare — 3 options tại Stage 4:**

| Option | Pattern | Best for | Sub-skill |
|---|---|---|---|
| Liquid Glass V22 | HTML `<video>` direct child + glass cards trong HTML + ffmpeg ghép audio cuối | TikTok product review dọc 1080×1920 với PIP + specs | `tiktok-product-motion-graphics` v3.21.5 |
| Subtitle/Motion Text | Sub-composition với word-level highlight theo Whisper | TikTok talking-head cần subtitle sync voice | `creative/hyperframes` |
| Diverse Motion 8-Phase | 8 phase × 1 style riêng (font/color/position/animation) | Long-form 110s video đa dạng visual | `creative/hyperframes` |
| 3D Trailer Cyberpunk | V1→V5 progression CSS-FX → Three.js PBR | Cinematic trailer 30s với bloom + perspective | `creative/hyperframes` |

## Forensic V22 — Cách em đã làm để được kết quả đó (reference cho turn-3 câu hỏi)

**Trigger:** Anh hỏi "check lại V22 / V77 em đã làm cách nào để được kết quả đó?"

**Workflow V22 verified PASS 17/07/2026** (canonical pattern cho MỌI clip motion graphics):

```html
<!-- V22 KEY: video bg là DIRECT CHILD of root, KHÔNG có overlay qua ffmpeg -->
<div id="root" data-composition-id="main"
     data-start="0" data-duration="32"
     data-width="1080" data-height="1920">
  <video id="video-bg" muted playsinline preload="auto"
         data-start="0" data-duration="32"
         data-track-index="0">
    <source src="assets/source/full_bg.mp4">
  </video>
  <!-- Glass cards render TRONG HTML (KHÔNG qua ffmpeg overlay) -->
  <div class="glass-card hook" data-start="2" data-duration="6" data-track-index="1">
    Củ sạc Lightning mini 20W
  </div>
</div>

<script>
window.__timelines = window.__timelines || {};
const tl = gsap.timeline({ paused: true });   // ← paused
window.__timelines["main"] = tl;

// V22 KEY: pause tất cả video + seek to 0
const bgVideo = root.querySelector('#video-bg');
bgVideo.pause();
bgVideo.currentTime = 0;
</script>
```

**Tại sao V22 PASS (12.3 MB, 3 Mbps, face motion 158-230):**
1. HyperFrames TỰ play video bg trong headless Chrome (vì pause + seek(0) cho phép seek-driven playback)
2. Glass cards render trong HTML composition → không qua ffmpeg filter → không bị nén
3. ffmpeg chỉ ghép audio cuối từ source gốc (KHÔNG overlay video track)

**Tại sao V72-V76 FAIL (anh đã chửi em 18/07):**

| V72-V76 anti-pattern | Tại sao fail |
|---|---|
| Extract PIP/glass riêng + overlay qua `format=yuva420p` ffmpeg | Glass bị nén qua ffmpeg → mờ + quá trong |
| `<img>` PNG tĩnh cho PIP thay vì `<video>` | HyperFrames KHÔNG play `<img>` animated → render 1 frame tĩnh |
| PIP size 420×750 portrait | Bị crop thu nhỏ, sai format TikTok dọc |
| Dùng `crop=ih*9/16` cho source 1080×1920 | Chỉ lấy Y=0-720 → background đen |
| 4-layer filter_complex phức tạp | Audio drift, motion freeze, bit rate ~440 Kbps = static |

**Lesson vĩnh viễn:** V22 workflow đúng ≠ kết quả tốt nếu source clip KHÔNG có motion.
V77 (sau này) dùng V22 workflow chính gốc 100% nhưng source `clip_0003_V3_..._speed13.mp4`
gần static (face chin d(1-30) ~45) → render ra bit rate 440 Kbps = static. **Em PHẢI verify
source motion TRƯỚC khi apply V22 workflow.**

**Full evidence files:**
- Case study: `wiki/projects/content-creator/sac-du-phong-mini-iphone-22-versions-case-study.md` (16.7KB)
- Layout benchmark: `wiki/projects/content-creator/layout-benchmark-vertical-tiktok-1080x1920.md` (28KB)
- Skill V22 section: `~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md` line 122-220
- Ship file: `/Volumes/Storage-1/Pocket3/Hermes-Edit/sac_du_phong_v22_32s_with_audio.mp4` (12.3 MB)

## Stage 5 — VERIFY + SHIP (5 calls — added 18/07 audio fade check)

**Skill:** `~/.hermes/skills/media/tiktok-verify-protocol/` (skill tiktok-video-editor cũng có verify_clip.py)

**Workflow (PITFALL #38 audio fade MANDATORY):**
1. `python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/check_audio_fade.py output.mp4` (PITFALL #38 — anh yêu cầu 18/07)
   - exit 0 = PASS (audio fade OK ở mọi cut boundary)
   - exit 1 = FAIL → RE-RENDER với `afade=t=in:st=0:d=0.03,afade=t=out:st={dur-0.03}:d=0.03` → check lại
2. `python3 scripts/verify_clip.py <audio.json> <keeps.json> [output.mp4]`
3. `python3 scripts/check_anchor_lap.py` (Pitfall #21 FALSE START scan)
4. `ffprobe -v error -show_entries format=duration,bit_rate,size output.mp4` để confirm spec TikTok
5. Copy file vào `/Volumes/Storage-1/Pocket3/Hermes-Edit/pipeline/output/_shipped/<DATE>/` (canonical ship path)
6. Báo cáo anh với table 9 cột (Clip / Duration / Source RMS / Output RMS / Loop / Hallucinate / Câu treo / Size / Status + **Audio Fade PASS/FAIL**)

> **⚠ PITFALL #38 (NEW 18/07 — anh yêu cầu):** Mọi cut boundary PHẢI có 30ms audio fade. Real case: clip V78 (đã SHIP 13/07) có 50/52 boundaries missing fade. **KHÔNG BAO GIỜ skip audio fade check.** Pattern from browser-use/video-use HARD RULE #3. Reference: `references/audio-fade-check-pitfall-38-2026-07-18.md`

**Ship path theo ngữ cảnh:**

| Loại clip | Canonical path |
|---|---|
| Anh TikTok motion-graphic (Pocket3, etc.) | `/Volumes/Storage-1/Pocket3/Hermes-Edit/` |
| Anh TikTok review lifestyle | `/Volumes/Storage-1/Tiktok-Tuan-Anh/` |
| Anh TikTok review badminton (Yonex) | `/Volumes/Storage-1/Pocket3/Hermes-Edit/` (chung) |
| Anh teardown / debug clip | `/Volumes/Storage-1/Hermes/Hermes-Edit/` |

## Quick Start — One Command Per Stage

```bash
# Stage 1 — inventory
ffprobe -v error -show_format -show_streams raw.mp4

# Stage 2 — transcribe + filler cut (skill tiktok-video-editor)
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --word-timestamps True --output-dir ./whisper_out raw.mp4
# → manual review script → build keep_plan.txt

# Stage 3 — speed 1.3x render (skill tiktok-video-editor)
ffmpeg -y -i source.mp4 -filter_complex "[0:v]setpts=PTS/1.3[v];[0:a]atempo=1.3[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset slow -crf 18 -c:a aac -b:a 128k \
  output_troncau_speed13.mp4

# Stage 4 — motion graphic (skill tiktok-product-motion-graphics OR creative/hyperframes)
# Option A: V22 glass cards
npx --yes hyperframes init project --non-interactive --example=ios26-liquid-glass
# → edit compositions/tiktok-liquid-glass.html
npx --yes hyperframes render --quality high --output final.mp4

# Stage 5 — verify + ship
python3 ~/.hermes/skills/media/tiktok-video-editor/scripts/verify_clip.py \
  keeps.json output_troncau_speed13.mp4
cp final.mp4 /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<id>_V<n>_troncau_<ten>_FINAL.mp4
```

## video-use Integration (Alternative path cho Stage 2-3)

**Khi nào dùng video-use thay vì tiktok-video-editor:**
- Anh muốn "AI tự edit" mà không cần đọc kỹ transcript
- Clip ngắn < 60s (video-use self-eval loop rẻ)
- Anh cần speed (không cần độ chính xác 100% từng câu)

**Setup 1 lần:**
```bash
git clone https://github.com/browser-use/video-use ~/Developer/video-use
ln -sfn ~/Developer/video-use ~/.claude/skills/video-use
cd ~/Developer/video-use
uv sync
brew install ffmpeg
cp .env.example .env
# Paste ELEVENLABS_API_KEY vào .env
```

**Workflow khi dùng:**
```bash
cd /path/to/raw/videos/
# Paste vào Hermes:
# "Set up https://github.com/browser-use/video-use for me. Read install.md first..."
# Sau khi setup xong:
# "edit these into a launch video"
```

**Trade-off vs tiktok-video-editor:**

| Dimension | tiktok-video-editor (manual) | video-use (AI) |
|---|---|---|
| Customize 7 KEY INSIGHTS | ✅ Manual rõ ràng | ❌ AI tự quyết |
| V3.21.5 26 Pitfall coverage | ✅ Apply systematic | ❌ AI may miss Vietnamese filler |
| Speed 1.3x MANDATORY | ✅ Step bắt buộc | ❌ Không enforce |
| ELEVENLABS_API_KEY cost | Free (Whisper medium) | $0.10-0.30/clip |
| Self-eval tại cut boundary | ✅ verify_clip.py + check_anchor_lap.py | ✅ built-in (3 retries max) |
| Vietnamese dialect | ✅ medium-mlx verified ANH NỚI rõ ràng | ⚠ ElevenLabs trained trên multi-lang |

**Recommendation:** Default `tiktok-video-editor` cho mọi clip VK Anh đang edit. Switch
`video-use` chỉ khi:
1. Anh muốn test xem AI edit có ra same quality không (A/B test)
2. Anh muốn pipeline tự động không cần manual review

## Khi nào KHÔNG dùng skill này

- Anh chỉ cần cut filler nhanh 1 clip → dùng `tiktok-video-editor` v3.29.0 trực tiếp
- Anh chỉ cần thêm motion graphic, không edit lại → dùng `tiktok-product-motion-graphics` v3.21.5
- Anh chỉ cần verify final MP4 → dùng `tiktok-verify-protocol`
- Anh muốn hyperframes trailer cinematic (cyberpunk, 3D) → dùng `creative/hyperframes` + skill `hyperframes`
- Anh muốn phân tích kênh competitor → dùng `tiktok-competitor-deep-analysis`

## Sub-Skill Maintenance Map

| Sub-skill | Khi nào patch | Owner |
|---|---|---|
| `tiktok-video-editor` v3.29.0 | Pitfall mới (đã có #20-#26), workflow 7-step chuẩn | Editor session |
| `tiktok-product-motion-graphics` v3.21.5 | Liquid glass config update, V22 layout fix | Motion session |
| `tiktok-verify-protocol` v?.?.? | Verify rule mới, anchor-lap pattern mới | QA session |
| `creative/hyperframes` (motion graphic) | Three.js pattern, "no static pixel" rule | Trailer session |
| `skills/hyperframes` (router) | HyperFrames version update (v0.7.61) | HyperFrames session |
| `video-use` (alternative) | Khi anh explicit yêu cầu | Lazy-load khi cần |

## Real Validation Cases (sẽ update sau)

| # | Date | Input | Output | Pipeline | Result |
|---|---|---|---|---|---|
| — | — | — | — | — | (chưa validate — first runtime sẽ add vào) |

## Pitfalls — Hard Rules

| # | Pitfall | Fix |
|---|---|---|
| 1 | Skip Stage 1 ffprobe → Stage 2 Whisper fail vì codec/format khác | LUÔN ffprobe TRƯỚC |
| 2 | Build keep_plan từ V1 output timestamps (Pitfall #24) | LUÔN từ source timestamps |
| 3 | Skip Speed 1.3x (Pitfall #26) | Apply ở Stage 3 bước 2 |
| 4 | HyperFrames > 40 phrases DOM crash | Merge phrases trước khi render (skill creative/hyperframes HF-TikTok-Subtitle 1) |
| 5 | `--motion-graphics` route KHÔNG nhận diện được talking-head với designs | Dùng `/talking-head-recut` thay vì `/motion-graphics` |
| 6 | `concat demuxer -c copy` cascade hallucinate (Pitfall #22) | Dùng `-filter_complex concat` |
| 91 | **`concat demuxer -c copy` FRAME OVERLAP at segment boundary** (NEW 27/07 real case, 7 clips batch 0085/0086/0088/0091/0093/0094/0095 BODY_MIST_AMAP/LENSPEN/OP_POCKET3) — `ffmpeg -f concat -safe 0 -c copy output.mp4` stream-copy frame boundary tại GOP gốc KHÔNG tại `end_padded` keep_plan → frame N hiển thị THÊM 1-2s trước frame N+1 → user nghe "đè frame" / "frame bị lặp lại". Hard rule: render multi-segment TikTok LUÔN dùng `filter_complex` re-encode từng segment + concat (KHÔNG BAO GIỜ `concat demuxer -c copy`). **Verify protocol**: extract frame tại boundary ±0.1s pre-speed → MD5 phải KHÁC nhau 100% (nếu giống = fail, frame bị đè); đối chiếu vision 1 case boundary rõ rệt (clip_0086 verified: 15.85s 1 tay cầm Lenspen → 16.05s 2 tay miệng mở rộng). Pattern template: `/tmp/render_7clips_final.sh` (`filter_complex` per segment + `concat=n=N:v=1:a=0[vout]` + audio atrim/aresample tương tự). 7 V2 cũ backup ở `_archive/v2_overlapped/` (496MB) | Render bằng `filter_complex` re-encode, verify boundary frame MD5 ≠, backup V2 cũ trước khi overwrite. Reference: `references/pitfall-91-concat-demuxer-frame-overlap-2026-07-27.md` |
| 7 | HEVC source 1728×3072 không scale trước | Scale TRONG filter_complex (Pitfall #23) |
| 8 | Ship file vào `~/Downloads/` thay vì `Hermes-Edit/` | Anh đã explicit dặn 17/07 — luôn `/Volumes/Storage-1/Pocket3/Hermes-Edit/` |
| 43 | **Build TRƯỚC khi LEARN FULL → wasted 3 versions (V5/V6/V7 đầu fail)** | **LEARN FULL trước build = `cat ~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md` → đọc V78→V87 RECAP sections → extract HARD RULE checklist → apply từng rule. Anh explicit 19/07: *"Hôm qua em làm 0003_v84 được mà sao hôm nay lại không làm được, hôn qua anh đã bảo em phải learn full rồi mà"* → mọi session build motion graphic PHẢI mở skill trước** |

## See Also — Related Skills

| Skill | Vai trò |
|---|---|
| [[hyperframes]] | Router chính cho HyperFrames create/edit/render (skills/) |
| [[creative/hyperframes]] | Motion graphic + TikTok subtitle/motion text workflow |
| [[hyperframes-cli]] | CLI dev loop (init/lint/check/render/cloud) |
| [[media-use]] | Agent Media OS — resolve bgm/sfx/voice/grade/lut/image |
| [[tiktok-video-editor]] | Mode B 95-120s edit workflow (Stage 2+3) |
| [[tiktok-product-motion-graphics]] | Liquid glass V22 motion graphic (Stage 4 Option A) |
| [[tiktok-verify-protocol]] | 2-layer QA gate (Stage 5) |
| [[folder-worktree-convention]] | Folder standard để store raw + edit files |

## Pitfall: HyperFrames skill collision (skills/ vs creative/)

`~/.hermes/skills/hyperframes/` (router) và `~/.hermes/skills/creative/hyperframes/`
(motion-graphics) collide khi gọi bare name. Fix: load bằng full path
`skill_view(name="creative/hyperframes")` hoặc merge cả 2 vào 1 skill duy nhất.

**Trạng thái 18/07/2026:** CHƯA MERGE. Hai skill vẫn phục vụ 2 use case khác nhau:
- `skills/hyperframes/` = router cho HyperFrames create/edit/render (generic)
- `creative/hyperframes/` = concrete motion-graphic + TikTok subtitle pattern (specific)

Nếu anh thấy collision phiền → tạo task merge 2 skill thành 1.

**Full workaround guide:** `references/hyperframes-skill-collision-workaround-2026-07-18.md`

---

## 📦 Hermes-Edit Folder Migration (NEW 18/07/2026) — Pattern từ browser-use/video-use

**Context:** Em migrate 123 files / 11.7 GB từ flat folder sang cấu trúc pipeline/{drafts, output/{_shipped, _ready_to_ship}}/, _archive/, _verify/, logs/ theo pattern của repo `browser-use/video-use` (https://github.com/browser-use/video-use).

**Pattern từ video-use:**
- **Skill code immutable** + **output mutable** (tách core ra 1 nơi stable)
- **EDL JSON schema** cho LLM↔renderer giao tiếp (sources/ranges/grade/overlays/subtitles)
- **3 quality ladder**: draft (CRF 28 ultrafast), preview (CRF 22), final (CRF 18)
- **30ms audio fade** mọi cut boundary (HARD RULE tránh pop)
- **Subtitles apply LAST** trong filter chain
- **Self-eval** với timeline PNG tại mọi cut boundary
- **12 hard rules** tách rõ với artistic freedom

**Hermes-Edit structure SAU migration:**
```
/Volumes/Storage-1/Pocket3/Hermes-Edit/
├── README.md                       # File hướng dẫn
├── migrate_hermes_edit.py          # Script migration (8.6KB)
├── _docs_video_use_research.md     # Research notes 13KB
├── _archive/                       # Legacy V1-V_n-1 cũ (4.9GB)
├── _verify/                        # Verify reports + cache wav/json
│   ├── _verify_0004_report.md
│   ├── _verify_0005o_report.md
│   └── ...
├── logs/                           # Migration manifest
│   └── migration_manifest.json
├── pipeline/
│   ├── drafts/clip_<ID>/          # Intermediate V1-V_n-1 (2.3GB)
│   └── output/
│       ├── _shipped/<DATE>/        # Đã ship OK (1.5GB, 21 files)
│       │   ├── 2026-07-14/
│       │   ├── 2026-07-16/
│       │   └── 2026-07-18/        # 5 file mới nhất
│       └── _ready_to_ship/         # Conditional (cần review)
├── scripts/                        # Edit scripts (giữ nguyên)
├── tools/                          # Tools (giữ nguyên)
└── tmp/                            # Working files (giữ nguyên)
```

**13 files per video edit** (theo video-use pattern):
- `transcripts/<stem>.json` (cache Whisper)
- `takes_packed.md` (phrase-level cho LLM)
- `edl.json` (LLM→renderer schema)
- `project.md` (append-only session memory)
- `master.srt` (subtitles)
- `clips_graded/seg_NN_*.mp4` (per-segment)
- `base.mp4` (lossless concat)
- `final.mp4` (final composite)
- `animations/slot_*/` (parallel sub-agents)
- `verify/*.png` (self-eval timeline PNG)

**Workflow mới cho mỗi clip edit:**
1. User drop raw vào `pipeline/input/` (TODO: symlink từ `/Volumes/Storage-1/Pocket3/Footages/`)
2. Stage 2+3: transcribe + edit → save draft vào `pipeline/drafts/clip_<ID>/`
3. Stage 5: verify → nếu PASS, move `final.mp4` sang `pipeline/output/_shipped/<DATE>/`
4. Stage 5: nếu conditional, move sang `pipeline/output/_ready_to_ship/` chờ review
5. Cleanup: xóa V_old sau khi V_new ship (binary cleanup rule từ PITFALL #27)

**Action items cho tiktok-pipeline-studio v1.1.0:**
- [ ] Update Stage 5 SHIP path từ `/Volumes/Storage-1/Pocket3/Hermes-Edit/` (flat) → `pipeline/output/_shipped/<DATE>/` (organized)
- [ ] Update Stage 5 README reference link tới `Hermes-Edit/README.md`
- [ ] Thêm verification bước "check file đã ở `_shipped/<DATE>/` chưa"
- [ ] Bump version v1.0.0 → v1.1.0 với note "Hermes-Edit folder migration pattern"

**Reference:** `/Volumes/Storage-1/Pocket3/Hermes-Edit/_docs_video_use_vs_tiktok_comparison.md` (13KB so sánh chi tiết)

**Real case 18/07:** 5 file mới nhất đã move vào `pipeline/output/_shipped/2026-07-18/`:
- `clip0003_V78_82s_FINAL_with_audio.mp4` (41.9 MB)
- `clip_0004_Final_..._V2_speed13.mp4` (87.6 MB) ⭐ FIX MỚI
- `clip_0005_Final_..._V2_speed13.mp4` (50.0 MB) ⭐ FIX MỚI
- `clip_0005_V2_..._led-rgb.mp4` (116.1 MB)
- `clip_0007_Final_..._speed13.mp4` (88.3 MB) ⭐ FIX MỚI

---

## 📋 Quy tắc mới bổ sung (NEW 18/07/2026)

**Pitfall #14 — Subagent scope GỌN retry khi TIMEOUT:**
- 5 subagent parallel verify 6 layers → 3 TIMEOUT ở 600s = bình thường
- Re-dispatch với scope GỌN (chỉ 5 narrative + FALSE START, bỏ motion/audio) → done trong 90-180s

**Pitfall #15 — Manual suspect pair PHẢI cross-check subagent:**
- Manual scan text KHÔNG có timestamp → FALSE POSITIVE rate cao
- LUÔN re-dispatch subagent scope GỌN với context "đặc biệt check K cặp này" trước khi báo verdict chính thức
- Real case 18/07 clip 0004: manual confirm sai 1/2 cặp (PAIR B "Pin 4000mAh" = BOTH_IN_CUT nhưng thực tế TAKE_NEW_ONLY)

**Pitfall #16 — Mỗi clip fail PHẢI fix ngay + verify lại (USER EXPLICIT):**
- Anh dặn verbatim 18/07: *"cái nào fail thì fix lại và thiếu speed thì speed lên!"*
- Workflow: verify → fail → fix NGAY từng cái → re-verify → move to `_shipped/<DATE>/`

**Pitfall #17 — Re-render dùng file Final_ làm input, KHÔNG dùng RAW HEVC 4K:**
- Subagent EDL timestamps được tính trên file Final_ đã edit (1080×1920)
- RAW HEVC 4K (1728×3072) chậm 5-10× + sai vị trí cắt
- Real case 18/07 clip 0004: RAW = 222.8s, Final_ = 166.4s, EDL từ Final_

**Pitfall #18 — Concat filter_complex CÙNG source + `-ss -to` SILENT DURATION BUG:**
- KHÔNG BAO GIỜ dùng `filter_complex concat` với CÙNG source + N input
- PHẢI extract từng segment thành file RIÊNG trước, rồi concat demuxer
- Real case 18/07: source 225.7s, EDL 5 ranges tổng 311.48s → concat filter output = 207.8s (sai) → fix = extract + concat demuxer = 207.78s (đúng)

**Pitfall #19 — Speed 1.3x MANDATORY:**
- Mode B 110-120s → speed 1.3x → 88-92s (sweet spot strict)
- Verify ngay sau concat bằng `ffprobe -show_entries format=duration`
- Anti-pattern: skip speed → clip dài 110-180s

**Pitfall #20 — Output folder convention:**
- Move shipped file vào `pipeline/output/_shipped/<DATE>/` (KHÔNG root)
- Move legacy file (có "Final_" trong tên nhưng duration > 2× Mode B) vào `_archive/`
- Anti-pattern: ship trực tiếp vào root → gây nhầm với legacy

---

## Support Files (references/)

- `references/hyperframes-skill-collision-workaround-2026-07-18.md` — Decision tree cho khi nào load `skills/hyperframes/` vs `creative/hyperframes/` + pending action items
- `references/edit-engine-trade-off-2026-07-18.md` — `video-use` vs `tiktok-video-editor` deep comparison (cost, quality, time, khi nào dùng cái nào, hybrid pattern, setup instructions cho video-use)
- `references/audio-fade-check-pitfall-38-2026-07-18.md` — Historical (DEPRECATED 26/07 bởi PITFALL #90 HARD CUT)
- `references/hard-cut-default-concat-2026-07-26.md` — PITFALL #90: HARD CUT default, CLEAN DELETE protocol
- `references/learn-full-hard-rule-checklist-2026-07-19.md` — 15 hard rule checklist cho HyperFrames motion graphic build
- `references/pitfall-38-audio-fade-stage-5-workflow-2026-07-18.md` — Historical audio fade workflow (deprecated)
- `references/pitfall-91-concat-demuxer-frame-overlap-2026-07-27.md` — **PITFALL #91 (NEW 27/07)**: `concat demuxer -c copy` gây frame overlap tại segment boundary. Real case 7 clip batch 0085-0095. Fix bằng filter_complex per-segment re-encode. Verify chain: ffprobe + MD5 boundary frames + vision check. **LOAD TRƯỚC KHI render multi-segment TikTok** nếu suspect stream-copy hoặc user flag "đè frame".
