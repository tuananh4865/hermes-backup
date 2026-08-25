---
name: video-cut-tiktok-shorts
title: Cut Long Video to TikTok/Shorts Clip with Re-start Detection
description: End-to-end workflow for cutting a long source video (review, podcast, vlog) into a TikTok/Shorts clip under 2 minutes (ideally under 1 min). Covers transcript extraction with Whisper large-v3, re-start + filler + pause detection, TikTok formula (hook 5s + body + CTA), 9:16 conversion with rotation handling, visual verification before delivery. Use when user says "cắt clip", "edit video", "làm short", "TikTok format", "9:16", "ngắn gọn hơn", "truyền tải nội dung ngắn gọn", "công thức TikTok", or shares a video with edit instructions. v2.36 — added Pitfall #10 (vision leading question → false PASS), #11 (Pocket 3 portrait zoom subtle), #12 (clean-delete policy khi user "bỏ X đi"). v2.37 — added OVERLAP AUTO-TRIM (keep_plan overlap → audio/frame lặp 2 lần, filter_complex phải clip end = min(end_padded, next.start_padded)).
created: 2026-06-30
updated: 2026-07-28
type: skill
tags: [video, ffmpeg, tiktok, shorts, editing, cut, whisper, re-start-detection, 9-16, orientation, google-drive, marked-before-cut, sentence-reasoning, understand-first, emotional-arc, customer-psychology, keep-plan-overlap, auto-trim, v2.37]  # added keep-plan-overlap, auto-trim tags
confidence: high
related_skills:
  - telegram-video-analysis
  - video-download-yt-dlp
  - tiktok-transcript-pipeline
  - capcut-cli
  - tiktok-video-editor
---

# Cut Long Video to TikTok/Shorts Clip

Workflow chuẩn cắt video dài (review, podcast, vlog) thành clip TikTok/Shorts < 2 phút, áp dụng công thức TikTok viral.

## When to use

Trigger phrases:
- "cắt clip" / "edit video" / "làm short" / "TikTok format"
- "9:16" / "ngắn gọn hơn" / "dưới 2 phút" / "dưới 1 phút"
- "truyền tải nội dung ngắn gọn" / "công thức TikTok"
- "cắt ụm ờ" / "bỏ khoảng nghĩ" / "cắt lặp"

User shares video (file hoặc link) + edit intent → trigger skill này.

## 8-Step Workflow (Step 3.5 added 2026-07-02)

> **CHANGE 2026-07-02:** Added Step 3.5 `KEEP_PLAN APPROVAL GATE` (Tuấn Anh's explicit rule: "Trước khi cắt thì em gửi cho anh keep plan trước để anh duyệt"). Agent MUST send keep_plan + receive approval BEFORE any ffmpeg render. Plus Step 3.4 self-review to catch own bugs before sending. Both are missing from old workflows — V22 case showed agent wrote plan with 4 bugs (wrong mute_ranges, missing hallucinate skip, missing mute for câu treo) that user had to catch manually.

### Step 1: Extract Audio + Transcribe với Whisper large-v3

Source video bất kỳ (HEVC, H.264, MOV, MP4):

```bash
# 1. Extract audio WAV (16kHz mono cho Whisper)
ffmpeg -y -i input.mov -vn -ac 1 -ar 16000 -c:a pcm_s16le audio.wav

# 2. Transcribe với large-v3 + flags chống hallucinate
# ALTERNATIVE: dùng wrapper system-wide (auto large-v3 + medium fallback nếu loop)
~/.hermes/scripts/whisper-transcribe audio.wav
# → tạo audio.json + audio.srt + audio.vtt + audio.tsv + audio.txt
# → auto-detect loop pattern (5-word phrase ≥5 lần) → fallback medium nếu cần

# HOẶC direct large-v3 + flags chống hallucinate:
/Users/tuananh4865/whisper-env/bin/mlx_whisper audio.wav \
  --model mlx-community/whisper-large-v3-mlx \
  --language vi \
  --output-format json \
  --output-name transcript-large \
  --condition-on-previous-text False \
  --compression-ratio-threshold 2.0 \
  --no-speech-threshold 0.6 \
  --logprob-threshold -0.5
```

Tại sao large-v3 (not medium), verified 2026-07-22 trên clip_0036_V9 (anh verdict "transcript chuẩn nhất"):
- Medium hallucinate loop "Các bạn có thể dùng cái góc này" × 72 lần ở giữa video (đã verify bằng short-segment re-transcribe)
- Large-v3 segment count 148 vs medium 94 cho 7 phút audio → re-start detection chính xác hơn
- Catch "CNC", "focus", "3cm", "15cm" (technical terms) — medium miss hết + hallucinate "đặc thùng", "phó kết"
- Performance: cache warm = 75s cho 7 phút audio (acceptable). Slowdown 4x so với medium (19s) nhưng vẫn acceptable.
- Auto-fallback safety net trong wrapper nếu large-v3 hallucinate loop → revert medium
- See `~/.hermes/skills/media/tiktok-video-editor/references/whisper-large-v3-default-2026-07-22.md` for full rationale

### Step 2: Detect Re-starts + Fillers + Pauses

Re-start pattern (Vietnamese TikTok): Khi nói sai, user thường lặp lại câu đầy đủ ở câu sau. Em cắt câu CỤT, giữ câu ĐẦY ĐỦ.

```python
# Cluster consecutive segments với word overlap > 0.4
for i in range(len(segments) - 1):
    words1 = set(segments[i]['text'].split())
    words2 = set(segments[i+1]['text'].split())
    overlap = len(words1 & words2) / max(len(words1), len(words2))
    if overlap > 0.4:
        # Re-start detected! Compare completeness
        if len(words1) < len(words2):
            cut_list.append(('cut_i', segments[i]['start'], segments[i]['end']))
        else:
            cut_list.append(('cut_i+1', segments[i+1]['start'], segments[i+1]['end']))
```

Common re-start patterns cần detect:
- "Tức là sao" (filler) + actual restatement
- "nó gọi là gì" (lắp) + actual term
- Câu cụt cuối segment (no ending verb) + câu đầy đủ sau

Filler words/segments cần cắt:
- Orphan ngắn < 1.5s (single word: "ở", "một", "đây", "à")
- Repeated syllables ("nguồn nguồn nguồn..." = hallucination từ whisper medium)
- Filler Vietnamese: "ừm", "ờ", "à", "kiểu", "thì là", "nó gọi là gì"

Pause detection (silence > 1.5s):
```bash
# Detect silence ranges
ffmpeg -i audio.wav -af "silencedetect=noise=-30dB:d=1.5" -f null - 2>&1 | grep silence

# Cut pauses > 1.5s nếu nằm giữa content (KHÔNG cut intro/outro)
```

### Step 3: Build TikTok Script với Formula

Công thức TikTok chuẩn:

```
[0:00-0:05] HOOK: 1 câu gây tò mò, claim mạnh
[0:05-0:25] BODY: 1-3 features ngắn gọn, mỗi cái 5-10s
[0:25-0:40] PAYOFF: kết quả / emotional reward
[0:40-0:50] CTA: like / follow / bấm mua
[Total: 45-60s]
```

Chọn segments theo impact score:
- HOOK: câu có claim mạnh nhất (e.g. "cực kỳ đa di năng", "không tháo ra khỏi Pocket 3")
- Feature 1-3: mỗi feature 1 insight cụ thể + visual demo
- Payoff: "kết quả thực tế" / "tại sao tốt"
- CTA: outro nguyên vẹn từ source

Target duration:
- Tối đa 2 phút theo mặc định user
- Lý tưởng < 1 phút (TikTok algorithm ưu tiên clips có completion rate cao)
- Bỏ filler/pause/re-starts KHÔNG cần thiết

### Step 4: Cut Segments với Stream Copy (preserves HEVC quality)

```bash
# Cut từng keep segment (no re-encode, giữ 4K HEVC chất lượng gốc)
for s in script_segments:
    outname = f"seg_{int(s['start']*10)}_{int(s['end']*10)}.mov"
    ffmpeg -y -ss $START -to $END -i input.mov -c copy $outname

# Concat các segments
cat > concat.txt <<EOF
file 'seg_X_Y.mov'
file 'seg_X_Y.mov'
...
EOF

ffmpeg -y -f concat -safe 0 -i concat.txt -c copy -movflags +faststart output.mov
```

Lưu ý: `-c copy` chỉ work nếu timestamps trên keyframes. Nếu cut chính xác không có re-encode thì vẫn OK. Nếu gặp DTS warning → re-encode bằng libx264.

### Step 5: CRITICAL — Video Orientation + 9:16 Conversion

iPhone videos thường có rotation side data KHÔNG có trong width/height metadata. Phải check trước khi crop:

```bash
# 1. Check rotation flag
ffprobe -v error -show_entries stream=width,height \
  -show_entries stream_side_data \
  -of default input.mov
# → tìm "rotation=" trong side data
```

Cách đúng convert 16:9 sang 9:16 (1080x1920):

```bash
ffmpeg -y -i input.mov \
  -metadata:s:v:0 rotate=0 \
  -vf "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920" \
  -c:v libx264 -preset medium -crf 22 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  output-9x16.mp4
```

Crop formula giải thích:
- `ih*9/16` = new width = height × 9/16 (cho 9:16 ratio từ height-based crop)
- `ih` = giữ height nguyên
- `(iw-ih*9/16)/2` = X offset = (orig_width - new_width) / 2 (center crop)

CÁCH SAI — KHÔNG DÙNG:
- transpose=1 hoặc transpose=2 rồi không scale: pixel transpose nhưng metadata width/height không update, vision vẫn thấy sideways
- Chỉ dùng scale không crop: scale 3840x2160 thành 1080x1920 vẫn 16:9, không phải 9:16
- Trust width/height metadata mà không check rotation

### Step 6: MANDATORY Visual Verification

BẮT BUỘC extract frame + vision verify trước khi gửi:

```bash
# Extract frame từ output
ffmpeg -y -i output-9x16.mp4 -ss 5 -frames:v 1 -update 1 preview.jpg
file preview.jpg
# → phải báo "JPEG image data, 1080x1920"
```

Vision check checklist:
1. Orientation: "Người đứng thẳng đúng chiều, không bị xoay"
2. Tỉ lệ: "9:16 (portrait/dọc)"
3. Content: thấy sản phẩm/người rõ ràng, không bị crop mất chi tiết quan trọng
4. Sản phẩm/subject ở trung tâm frame

Nếu vision báo orientation sai: KHÔNG fix bằng transpose. Quay lại Step 5, kiểm tra `rotate=0` đã set chưa.

### Step 7: Compress + Deliver

Compress nếu file > 20MB (Telegram limit):
```bash
# H.264 1080p at crf 22, AAC 128k → ~10-30MB cho 60s
ffmpeg -y -i output.mov \
  -vf "scale=-2:1080" \
  -c:v libx264 -preset medium -crf 22 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  output-1080p.mp4
```

Deliver qua Telegram:
```
MEDIA:/path/to/output-1080p.mp4
```

File sizes tham khảo:
- 60s 4K HEVC ≈ 250 MB
- 60s 1080p H.264 crf 22 ≈ 12-30 MB
- 60s 720p H.264 crf 28 ≈ 5-10 MB

## Source Acquisition: Google Drive (no gdown required)

When user shares a Google Drive link (`https://drive.google.com/file/d/<FILE_ID>/view?usp=drivesdk`):

```bash
# 1. Get confirm UUID from the warning page (HTML body)
FILE_ID="1hlmtEy1syTSI67IbHWRn2dQLb6tzIqpU"
curl -sLc cookies.txt "https://drive.google.com/uc?export=download&id=${FILE_ID}" -o confirm.html

# 2. Extract the uuid form input value (NOT the cookie confirm token — that's different)
grep -oE 'value="[a-f0-9-]{36}"' confirm.html | head -1
# → value="a1438a0f-b564-4b0f-86cd-da35252b60e9"

# 3. Download via drive.usercontent.google.com (skips virus scan warning)
CONFIRM_UUID="a1438a0f-b564-4b0f-86cd-da35252b60e9"
curl -L "https://drive.usercontent.google.com/download?id=${FILE_ID}&export=download&confirm=t&uuid=${CONFIRM_UUID}" \
  -o clip.mp4 -s -w "HTTP: %{http_code} | Size: %{size_download} bytes\n"

# 4. Verify it's actually a video, not an HTML error page
file clip.mp4
# → MUST say "ISO Media, MP4 Base Media" or similar
```

**Why not `gdown`:** It's often not installed (`pip install gdown` would fail in whisper-env which doesn't have pip; system Python has PEP 668 protection). The curl-based approach works in any environment.

**Why the `confirm=t&uuid=...` URL works:** Google Drive shows virus scan warning for files >100MB. The form contains `<input name="uuid" value="...">` which is the actual download authorization. Using `drive.usercontent.google.com` with that UUID bypasses the warning UI entirely.

## 🚨 MARKED-BEFORE-CUT Workflow (mandatory for "cắt clip" tasks)

**User's explicit rule (2026-06-30):** *"khi dùng transcript phải đánh dấu đúng đoạn cần cắt TRƯỚC khi vào cắt clip, tránh bị lặp ừm ờ, à và thừa câu từ!"*

**The pattern:** Always produce a decision table (KEEP/PARTIAL/CUT per segment) BEFORE running any ffmpeg command. This catches:
- Repeated voice (câu lặp → giữ đoạn đầy đủ nhất)
- Filler words ("ờ", "ừm", "à", "nên là", "kiểu")
- Pauses > 0.5s between content segments
- **Internal-segment filler/lặp** (e.g., "đây là đây là" / "là đây là" / "với đầy với đầy đủ") — see `media/tiktok-video-editor` Pitfall #64. **Em TỰ LLM reasoning** trên transcript (KHÔNG dùng script): đọc transcript, identify phrase "đây là đây là" → câu đầu bị cắt, giữ câu "đây là" thứ 2. Nguyên tắc vàng: **LUÔN ƯU TIÊN giữ câu ở SAU**, cắt phần lặp/lỗi ở đầu.

**Decision table template:**
```markdown
| Seg | Time range | Duration | KEEP/CUT | Reason |
|-----|------------|----------|----------|--------|
| 1 | 0.00-7.28s | 7.28s | KEEP | HOOK — intro mạnh |
| 4 | 24.82-31.16s | 6.34s | CUT | TRÙNG Ý với seg 3 |
| 5 | 31.16-41.96s | 10.80s | KEEP-PARTIAL | Cắt bớt filler 'tùy theo thời tiết' |
| 12 | 82.98-86.08s | 3.10s | CUT | Filler: 'không chuyên nước hoa' |
```

**Refinement loop:** If total KEEP > 60s target → tighten further by trimming within segments (not whole-segment cuts). E.g. shorten seg 5 from 10.80s → 7.0s by trimming filler tail.

**Why this matters:** Skipping the marked-before-cut step = agent cuts filler wrong → mất emotional peak → user repeats request 3x. The decision table is the audit trail that prevents "I thought you said to cut ờ".

## 🎯 Aspect Ratio: PRESERVE original 9:16 (don't crop square)

**User's explicit rule (2026-06-30):** *"Giữ đúng tỉ lệ gốc của clip nhưng em gửi đang bị bóp lại thành hình vuông rồi!"*

When source video is ALREADY 9:16 (portrait, e.g. 1728×3072):
- **DON'T** apply the Step 5 crop filter (`crop=ih*9/16:ih:...`) — it's already correct
- **DON'T** transpose (rotation metadata was stripped or was never present)
- **DO** verify with `ffprobe` first:

```bash
ffprobe -v error -select_streams v:0 -show_entries stream=width,height -of default=noprint_wrappers=1 input.mp4
# → width=1728, height=3072
# → AR check: 1728/3072 = 0.5625 = 9/16 ✓
```

Then just trim + concat + encode at the source resolution — NO re-crop:

```bash
ffmpeg -y -i input.mp4 -filter_complex "[0:v]trim=...,setpts=...[v0];..." \
  -map "[outv]" -map "[outa]" \
  -c:v libx264 -preset medium -crf 23 -c:a aac -b:a 192k \
  -movflags +faststart \
  output.mp4
```

**Detection heuristic for "bị bóp vuông":** If source shows side-by-side content squished into center with black bars → user preview tool rendered it as square → real file is 9:16 → DON'T re-crop.

### 10. Vision leading question → false PASS (2026-07-26 session)

Triệu chứng: Em hỏi vision "frame có zoom không?" → model trả "có" vì leading question → em claim PASS mà thật ra zoom subtle, không visible.

Fix: **Objective measurement, NOT leading question:**
- ❌ "Frame này có zoom không?" → leading, model yes-biased
- ✅ "So sánh 2 frame cùng timestamp. Frame V2 có gì khác vs zoom test? Zoom visible bao nhiêu %?"
- ✅ Compare V2_no_zoom vs V3_zoom tại cùng timestamp, đo kích thước face/feature (pixel % frame)

Verify protocol khi ship zoom/visual effect:
1. Extract frame từ V2 (no effect) + V3 (with effect) ở CÙNG timestamp
2. Compute file size diff (zoom = file size tăng) — quick heuristic
3. Vision ask về OBJECTIVE diff (vị trí, kích thước, có/không element)
4. Pass = diff > 10% visible threshold

### 11. Pocket 3 portrait source already tight → zoom effect subtle (2026-07-26 session)

Triệu chứng: Source DJI Pocket 3 quay portrait 1728×3072 (ratio 9:16 = 0.5625). Output TikTok 1080×1920 CÙNG ratio. Scale = 0.625 → face center tự nhiên chiếm 50%+ frame VỚI KHÔNG CẦN ZOOM. Khi em apply zoompan 1.0→1.25x, zoom tăng từ 50% → 60-70% face — visible nhưng subtle.

User verdict (Tuấn Anh 26/07): "Không có hiệu ứng zoom thay vào đó là bị lỗi" — em đã claim PASS nhưng anh thấy zoom không rõ.

Fix:
- Pocket 3 portrait source = baseline đã tight, chỉ zoom 1.5x+ mới thật sự visible
- Nếu zoom < 1.3x trên Pocket 3 source → claim effect nhẹ, expect user feedback "không thấy gì"
- Test trước: extract 2 frame V2 vs V3, vision confirm diff > 15% subject size
- Alternative: anchor zoom ở PRODUCT thay vì center (face) — detect SP location bằng frame analysis

Real case clip_0095 (LENSPEN 26/07): zoompan 1.0→1.25x trên Pocket 3 portrait source → từ 50% face → 70% face. Visible nhưng subtle. Anh chưa duyệt.

### 12. Clean-delete policy khi user nói "bỏ X đi" (2026-07-26 session)

**User verbatim (26/07):** *"Nói bỏ thì bỏ hẳn ra khỏi skill luôn chứ để comment lại làm gì?"*

Triệu chứng: Lần 1 em patch file `build_pre_speed.sh` thành HARD CUT nhưng vẫn để comment "REMOVED afade 30ms theo Tuấn Anh feedback" + section SKILL.md "HARD RULE v0.04 NO FADE" + tạo helper script `/tmp/build_clip_no_fade.py`. Anh flag → em mới xóa hẳn.

Fix khi user nói "bỏ X đi" / "làm gì X" / "remove X":
1. **REMOVE HẲN khỏi code** — không giữ comment "deprecated" / "REMOVED" / "v0.x đã bỏ"
2. **REMOVE section khỏi SKILL.md** — không thêm section mới nói "X đã được thay bằng Y"
3. **DELETE helper files thừa** (helper scripts, references cũ)
4. **CLEAN entry memory** — gộp với entry khác hoặc xóa hẳn
5. **VERIFY bằng grep** — `grep -nE "X|REMOVED|deprecated" <file>` = 0 match (ngoại trừ 1 comment giải thích behavior)

Anti-pattern:
- ❌ "X đã bỏ, không dùng nữa, anh xem code ở v0.x"
- ❌ Comment `// REMOVED: old approach was X, see v0.01` 
- ❌ Helper script "build_clip_NO_FADE.py" chỉ để reference

Real case 26/07 lesson saved: `wiki/concepts/clean-delete-policy-2026-07-26.md`

## Common Pitfalls

### 1. Cut nhầm wrap-up/CTA vì hallucinate transcript (2026-06-26)

Triệu chứng: Whisper medium thấy "Các bạn có thể dùng cái góc này" × 72 lần ở 264-408s. Em cut toàn bộ → mất luôn outro "bấm mua hàng".

Fix: Luôn verify bằng short-segment re-transcribe trước khi cut range nào có 50+ segments lặp.

### 2. Vision báo "orientation sai" dù metadata 2160x3840 (2026-06-30)

Triệu chứng: Em apply transpose=1 rồi scale → ffprobe báo 2160x3840 (9:16) nhưng vision vẫn thấy sideways.

Nguyên nhân: Pixel đã transpose nhưng width/height metadata không update. Vision tool đọc theo visual → thấy sai.

Fix: KHÔNG dùng transpose. Dùng `-metadata:s:v:0 rotate=0` + `crop=ih*9/16:ih:...:0` để vừa strip rotation vừa crop center.

### 3. Hero shot không có sản phẩm trong 3 giây đầu

Triệu chứng: Hook segment chọn được vì câu punchy, nhưng visual ở giây đầu không thấy sản phẩm chính → người xem lướt.

Fix: Vision-verify frame từng segment trước khi include. Bỏ segment có visual yếu dù audio tốt.

### 4. Concat bị DTS warning / audio desync

Triệu chứng: Concat segments từ source có re-starts cắt giữa chừng → ffmpeg warning "Non-monotonic DTS".

Fix: Re-encode lúc concat (bỏ `-c copy`):
```bash
ffmpeg -y -f concat -safe 0 -i concat.txt \
  -c:v libx264 -preset medium -crf 22 \
  -c:a aac -b:a 128k \
  -movflags +faststart \
  output.mov
```

### 5. Re-start detection quá aggressive → mất content

Triệu chứng: Em cut "Các bạn có thể" vì nghĩ là filler, nhưng nó là hook quan trọng.

Fix: Chỉ cut câu có ≥ 50% word overlap với câu trước/sau. Đừng cut câu unique chỉ vì ngắn.

### 6. Cut whole segment when word-level precision needed (2026-06-30)

Triệu chứng: Em mark KEEP 31.16-38.0s cho câu "giữ 30 phút tới 1 tiếng" → cắt 4s thừa cuối. Nhưng 38.0s thực ra cắt vào giữa câu, làm câu bị cụt ngữ nghĩa. User feedback: *"Clip thành phẩm không tốt phải fix lại, có các đoạn ậm ờ không được cắt gọn, câu không đủ nghĩa đã bị cắt rồi!"*

Fix: **ALWAYS use word-level timestamps** (whisper-large-v3 returns `words[].start/end`). KEEP ranges must align with word boundaries — never cut mid-word. Use `atrim` with start/end at exact word timestamps:

```python
# BAD — cuts mid-word, breaks sentence
keep_range = (31.16, 38.0)  # loses end of "1 tiếng thôi"

# GOOD — aligns with word boundaries
keep_range = (31.16, 38.68)  # ends at end of "thôi," word
keep_range = (31.16, 36.30)  # skips "30 phút" stretched portion entirely
```

**Detection heuristic after build:** For each KEEP segment, check `words[-1].word` against abrupt-end list ['mình', 'cái', 'của', 'nó', 'là', 'thì', 'thể', 'có', 'được', 'những', 'lại', 'một']. If hit → re-cut to next word boundary OR extend to natural-ending word.

### 7. Stretched vowel sounds (ngân dài) — Vietnamese TikTok speakers

Triệu chứng: User says "sạng khoái" but `sạng` duration = 1.36s instead of normal 0.3s. Common Vietnamese filler-stretches that LOOK like content but should be cut:

| Word | Normal duration | Stretched | Reason |
|------|----------------|-----------|--------|
| `sạng`, `chơi` | 0.3s | 1.0-1.4s | Slow pronunciation / thinking pause |
| `đang`, `tìm`, `là` | 0.2-0.3s | 0.7-1.7s | Hesitation / re-start |
| Number words (`30`, `một`) | 0.2s | 1.0-2.3s | Counting pause |

Fix: **Detect stretched vowels** by scanning word timestamps > 0.6s for short common words. Either skip the word entirely (preferred) OR use mid-word boundary to trim duration to ~0.3s.

```python
# Detect all stretched short words
STRETCHED_THRESHOLD = 0.6
STRETCHED_COMMON = ['nó', 'mà', 'thì', 'là', 'ờ', 'ừm', 'à', 'á', 'ạ', 'sạng', 'chơi', 'đang', 'tìm']
for w in all_words:
    if w['word'].lower().strip(',.!?') in STRETCHED_COMMON and (w['end']-w['start']) > STRETCHED_THRESHOLD:
        # Mark for trimming — either skip or use mid-word cut
        print(f"  STRETCHED: {w['start']:.2f}s ({w['end']-w['start']:.2f}s) '{w['word']}'")
```

**Common stretches seen in real sessions:**
- `sạng` 1.36s in "sạng khoái" → cut at start of next word
- `chơi` 1.34s in "chơi thể thao" → trim to 0.5s
- `30` 2.30s hesitation before "phút" → cut or skip
- `đang` 1.40s + `tìm` 1.66s in "đang tìm một cái" → cut both, start at "một"

### 8. Stutter pattern (lắp) — "nó nó nó"

Triệu chứng: Speaker stutters "nó" 3 lần trong 4s: "Cái mùi hương **của nó** **thì nó** không có giữ... đâu, **nó** khoảng 30 phút" → 3x "nó" close together = stutter.

Fix: **Detection** — search for same word appearing 3+ times in 2s window:

```python
for i in range(len(all_words)):
    word = all_words[i]['word'].lower().strip(',.!?')
    if len(word) < 2: continue
    matches = [all_words[i]]
    for j in range(i+1, len(all_words)):
        if all_words[j]['start'] - all_words[i]['start'] > 2.0: break
        if all_words[j]['word'].lower().strip(',.!?') == word:
            matches.append(all_words[j])
    if len(matches) >= 3 and (max(m['start'] for m in matches) - min(m['start'] for m in matches) < 1.5):
        print(f"  STUTTER cluster: '{word}' {[f'{m[\"start\"]:.2f}s' for m in matches]}")
```

**REMOVAL risk:** Removing stuttered pronouns often breaks grammar (Vietnamese uses "nó" as generic pronoun, hard to remove without losing subject). **Better approach:** Accept the stutter — it's authentic speech. Only fix if user explicitly escalates about it.

**Verified result from 2026-06-30 session:** After 5 iterations, user said "khá ok rồi" with stretched vowels fixed but stutter still present. **Lesson:** word-level precision > stretched vowel removal > stutter removal (priority order).

### 9. Output path: VERSIONED, never overwrite (2026-06-30)

Triệu chứng: Multiple iterations produce v1, v2, v3, v4, v5c... user may want to compare. Overwriting destroys comparison ability.

Fix: Save with version suffix. NEVER overwrite previous version.

```bash
# ALWAYS increment version
cp /tmp/clip-edit/clip_edited.mp4 /Volumes/Storage-1/Pocket3/Hermes-edit/clip_edited_v1.mp4
cp /tmp/clip-edit/clip_edited.mp4 /Volumes/Storage-1/Pocket3/Hermes-edit/clip_edited_v2.mp4
# ... etc

# Folder can contain all versions for A/B comparison
ls /Volumes/Storage-1/Pocket3/Hermes-edit/
# → clip_edited_v1.mp4, clip_edited_v2.mp4, clip_edited_v3.mp4...
```

User told agent to clean up after choosing final version, OR keep all versions as iteration history.

### 6. Vision tool timeout 300s (2026-06-30)

Triệu chứng: `mcp_MiniMax_understand_image` timeout 300s, không trả kết quả.

Fix: Retry 1 lần. Nếu vẫn fail, dùng `vision_analyze` (LM Studio local, cần load model trước) HOẶC skip vision check và explicit warn user "em không verify được visual orientation, anh tự check trên Telegram". KHÔNG skip verify hoàn toàn.

## Output Spec chuẩn

| Property | Target |
|----------|--------|
| Duration | 45-60s (lý tưởng) / max 120s |
| Resolution | 1080x1920 (9:16) |
| Codec | H.264 + AAC |
| File size | < 20 MB (Telegram bot limit) / < 50 MB (premium) |
| Orientation | Portrait (verified bằng vision) |
| FPS | 30 |

## 🚨 KEEP_PLAN OVERLAP CHECK + AUTO-TRIM (added 2026-07-28)

**Critical pitfall missed by adversarial verify:** If `keep_plan.json` has overlapping keep ranges in source (e.g. keep N end_padded > keep N+1 start_padded), `filter_complex` trim+concat will **render the overlap region twice** in output — both audio AND video frames. User hears "lặp" và sees "đè frame".

### Detection (run BEFORE render)

```python
import json
kp = json.load(open("tmp/clip_XXXX/keep_plan.json"))
keeps = kp["keeps"]
for i in range(len(keeps) - 1):
    s, e = keeps[i]["start_padded"], keeps[i]["end_padded"]
    ns = keeps[i+1]["start_padded"]
    if e > ns:
        print(f"  ⚠️ OVERLAP: {keeps[i]['name']} [{s:.2f}-{e:.2f}] vs {keeps[i+1]['name']} start={ns:.2f}  overlap={e-ns:.2f}s")
        # User thấy "lặp" nếu không fix
```

**Real case 28/07:** 6/7 Pocket 3 clips có overlap trong keep_plan (0.5s–2.22s). clip_0088 RECAP [69.090–84.730] + DETAIL [83.750–93.310] overlap 0.98s. Subagent adversarial verify chỉ check frame SSIM tại boundary ±0.5s → KHÔNG thấy overlap bên trong keep. Phải check `sum(end_padded - start_padded)` khớp `actual_duration / 1.3` mới phát hiện.

### Fix (always apply when trim)

Trim vùng overlap khi build filter_complex: `end = min(end_padded, next_start_padded)` cho mỗi keep (trừ keep cuối).

```python
import json
kp = json.load(open("tmp/clip_XXXX/keep_plan.json"))
keeps = kp["keeps"]
n = len(keeps)
v_parts, a_parts, v_labels, a_labels = [], [], [], []
for i, k in enumerate(keeps):
    s = k["start_padded"]
    e = k["end_padded"]
    # Trim overlap with next keep
    if i < len(keeps) - 1:
        e = min(e, keeps[i+1]["start_padded"])
    vl, al = f"v{i}", f"a{i}"
    v_labels.append(f"[{vl}]"); a_labels.append(f"[{al}]")
    v_parts.append(f"[0:v]trim=start={s}:end={e},setpts=PTS-STARTPTS,scale=1080:1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2:black,fps=30[{vl}]")
    a_parts.append(f"[0:a]atrim=start={s}:end={e},asetpts=PTS-STARTPTS,aresample=44100[{al}]")
v_concat = "".join(v_labels) + f"concat=n={n}:v=1:a=0[vout]"
a_concat = "".join(a_labels) + f"concat=n={n}:v=0:a=1[aout]"
fs = ";".join(v_parts + a_parts + [v_concat, a_concat])
```

### Verify (duration match)

```bash
# Compute expected pre-speed WITHOUT overlap
python3 -c "
import json
k = json.load(open('tmp/clip_XXXX/keep_plan.json'))['keeps']
total = 0
for i, x in enumerate(k):
    s = x['start_padded']
    e = min(x['end_padded'], k[i+1]['start_padded'] if i+1 < len(k) else x['end_padded'])
    total += e - s
print(f'expected pre-speed (no overlap): {total:.3f}s')
"
# Compare with actual pre-speed duration
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 tmp/clip_XXXX/v4_pre_speed.mp4
# Nếu 2 số match → đã trim đúng
# Nếu actual > expected → còn overlap
```

**Anti-patterns vĩnh viễn:**
- ❌ Trust `keep_plan.json expected_duration` field — nó tính theo `sum(end_padded - start_padded)` CÓ overlap, không phản ánh output thực tế
- ❌ Chỉ check 1 boundary frame trong adversarial verify — overlap có thể nằm giữa keep, không tại boundary
- ❌ Apply filter_complex không auto-trim → audio + frame lặp 2 lần tại vùng overlap, user nghe "giống bị delay/echo"

**Khi nào KHÔNG cần trim:** Nếu keep_plan đã được author manual với `end_padded = next.start_padded` chính xác (overlap = 0) → filter_complex thông thường OK. Tốt nhất vẫn auto-trim để an toàn.

## 🚨 SOURCE-LENGTH → TRỌN-CÂU RULE (patched 2026-07-08)

**User's verbatim rule** (after session clip 0689 210s + clip 0682 354s): *"Cô đọng nhưng phải phân tích transcript kĩ để biết đoạn nào với đoạn nào là một câu đầy đủ nghĩa và giữ lại chứ không phải cô đọng là cắt cụt nghĩa của câu!!! Phải đọc transcript xong chọn toàn bộ những câu dài có nghĩa xuyên suốt câu đó và loại bỏ các câu treo không nghĩa đi chứ"*

**Escalation signal:** If output clip > 200s and source > 300s → user will say **"Ủa edit gì mà 4-5 phút không vậy? Quên mất cách edit rồi hả?"** Default = "preserve narrative" (v3.12 NARRATIVE-PRESERVATION) is WRONG when source has 20+ features.

### Decision matrix (run BEFORE Step 3 — Build TikTok Script)

| Source duration | # features (sentences with predicate) | Default Mode | Target output |
|-----------------|----------------------------------------|--------------|---------------|
| < 200s | < 15 | Mode A (preserve all) | 90% source, ~180s |
| 200-300s | 15-20 | Mode B-light | 130-150s |
| **> 300s** | **> 20** | **TRỌN-CÂU selection + Mode B-strict** | **110-120s (accept 60-80% features)** |
| Any | Has SOURCE-LOOP region (seg with same phrase repeated 5+ times) | Skip LOOP region entirely | Verify CTA from source transcript |

### TRỌN-CÂU selection algorithm

```python
def classify_seg(seg, siblings=[]):
    """Phân loại mỗi Whisper seg thành TRỌN/TREO/FILLER"""
    text = seg['text'].strip()
    words = text.split()
    last_word = words[-1] if words else ""
    
    # TREO: kết thúc bằng conjunction/prep, không có predicate
    is_treo = last_word in ['và', 'thì', 'là', 'nữa', 'thôi', '...', 'mình', 'đó', 'rồi', 'nha']
    
    # FILLER: single-word, "kiểu" patterns
    is_filler = text in ['ờ', 'ờ gọi là', 'kiểu mình', 'thì...', 'nó...']
    
    # LOOP: same phrase repeated 5+ times → SOURCE-LOOP region
    is_loop = sum(1 for s in siblings if s['text'] == text) >= 5
    
    # TRỌN: predicate complete, ≥ 8 words, ends with verb/noun
    is_tron = len(words) >= 8 and last_word not in ['và', 'thì', 'là', 'nữa', 'thôi', '...', 'mình']
    
    if is_loop: return 'FILLER_LOOP'  # DROP ENTIRE SEGMENT + ALL DUPLICATES
    if is_filler: return 'FILLER'
    if is_treo: return 'TREO'
    if is_tron: return 'TRỌN'
    return 'EDGE'  # judgment call
```

**Trade-off acceptance:** Source 400s + 21 features → 110-120s with 14 features (67%) is BETTER than 354s with all 21 features. User explicitly accepted 67% coverage in clip 0682 V6 re-edit.

### Anti-pattern: trusting re-Whisper for CTA

**Real case clip 0689 V3 (cũ):** V3 had CTA "đừng bỏ lỡ cơ hội" + "màu sắc" → kept in plan → but source transcript had ZERO instances of these phrases. CTA was HALLUCINATE from SOURCE-LOOP region (seg 53-80 "thì mình đem cái ốp này" × 50+).

**Fix:** Always verify CTA candidates by grepping SOURCE transcript (medium, `--condition-on-previous-text False`), NOT re-Whisper output. If source has no CTA keyword → don't add one even if re-Whisper shows it.

```bash
# GOOD — source transcript verification
python3 -c "
import json
src = json.load(open('audio.json'))
text = ' '.join(s['text'] for s in src['segments'])
for kw in ['đừng bỏ lỡ', 'bấm mua', 'mua hàng', 'link dưới', 'màu sắc']:
    print(f'{kw}: {text.count(kw)} lần trong source')
"
```

### 2-PART-RENDER + concat demuxer for multi-gap keep_plan

**When:** Keep_plan has gap > 5s between 2 keeps (source filler region with no TRỌN sentences).

```bash
# Part 1: keeps 0..gap
ffmpeg -y -i source.mp4 -filter_complex "$(cat filter_p1.txt)" \
  -map "[v]" -map "[a1]" -c:v libx264 -preset fast -crf 20 \
  -c:a aac -b:a 192k -movflags +faststart p1.mp4

# Part 2: keeps gap+1..end
ffmpeg -y -i source.mp4 -filter_complex "$(cat filter_p2.txt)" \
  -map "[v]" -map "[a1]" -c:v libx264 -preset fast -crf 20 \
  -c:a aac -b:a 192k -movflags +faststart p2.mp4

# Concat demuxer `-c copy` (instant, no re-encode)
cat > concat.txt <<EOF
file 'p1.mp4'
file 'p2.mp4'
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy -movflags +faststart output.mp4
```

### SEQUENTIAL-EDIT for multi-clip tasks

**User's verbatim rule** (2026-07-08): *"lần lượt từng clip thôi đừng cố làm song song"*

- N clip in 1 task → process clip A (build + render + verify + ship) BEFORE starting clip B
- KHÔNG parallelize via `delegate_task` or background render
- Verify clip A pass trước khi start clip B
- Parallel OK only when user explicit ("làm song song đi") or for cron batch jobs

## Pitfall NSP-100%-NOT-HALLUCINATE (Pocket 3 clips)

DJI Pocket 3 microphone + reverb → Whisper NSP > 0.3 cho 100% segs even when source audio is clean (RMS > -23 dB).

**Don't:** Re-Whisper repeatedly with large-v3 (lãng phí, vẫn NSP 100%).

**Verify:**

```python
# Check 1: audio RMS
src_rms = volumedetect(source.mp4)['mean_volume']
if src_rms > -50:
    # Check 2: Jaccard text overlap
    re_text = ' '.join(s['text'] for s in re_segs)
    src_text = ' '.join(s['text'] for s in source_segs)
    jaccard = jaccard_similarity(re_text, src_text)
    if jaccard > 0.7:
        return 'NSP_FALSE_POSITIVE_PASS'  # Whisper text sạch, dùng được
```

Real case clip 0689 V5: 48/48 segs NSP > 0.3, but RMS -23.2 dB + Jaccard 77% → NSP là false positive, transcript dùng được.

## 🧠 UNDERSTAND-FIRST EDITING (v2.35 — 2026-07-10 session, applies BEFORE Step 3)

**Trigger:** User flagged in the 10/07 session that the agent had been auto-editing (running classify + apply patterns) WITHOUT actually reading the transcript. Three verbatim corrections from Tuấn Anh:

1. *"Em phải thực sự đọc đầy đủ transcript và hiểu được nội dung sau đó phân tích điểm nào giữ điểm bào thừa bỏ đi được"*
2. *"không hiểu được nội dung clip thì làm sao cắt thành công được"*
3. *"Ủa là từ trước tới giờ em vẫn không tự đọc hiểu ngữ cảnh của transcript để đưa ra lựa chọn chính xác à?"*

**Compiled lesson (also documented as `tiktok-video-editor` v3.19.1):** *Edit thành công = ĐỌC HIỂU nội dung + ĐÁNH ĐÚNG tâm lý/cảm xúc khách hàng.*

### What this ADDS to the 3-LAYER framework above

The 3-LAYER framework (v2.34) filtered every sentence through 3 reasoning gates — Grammar → Product purpose → Framework position. The user's complaint was that the agent had been **skipping the reading step entirely**. v2.35 adds a STEP-0 mandate applied to every edit task:

**BẮT BUỘC trước Step 3 (Build TikTok Script), insert the 4-question gate:**

1. **"Câu này nói gì?"** — Phải tóm tắt được nội dung câu. Nếu KHÔNG → câu LỖI / filler cứng.
2. **"Phục vụ cảm xúc nào trong emotional arc?"** — HOOK (gây tò mò) / PROBLEM (đánh nỗi đau) / SOLUTION (hy vọng) / USP (thuyết phục) / AUTHORITY (tin tưởng) / CTA (hành động).
3. **"Câu nào khác nói ý này ngắn hơn không?"** — Nếu có → keep câu ngắn hơn, drop câu này.
4. **"Nếu bỏ câu này, emotional arc có gap không?"** — Nếu KHÔNG → drop.

If the agent cannot answer all 4 for a candidate keep → the agent was pattern-matching, not understanding. STOP and re-read the source transcript.

### Emotional arc template (default — adapt per clip)

```
[0:00-0:03] HOOK — 1 câu gây tò mò, claim mạnh, dừng scroll
[0:03-0:10] PROBLEM — đánh đúng nỗi đau khách hàng đang gặp
[0:10-0:30] SOLUTION + USP — sản phẩm giải quyết + điểm khác biệt
[0:30-0:50] AUTHORITY — uy tín / kinh nghiệm / đã qua nhiều lựa chọn
[0:50-0:60] CTA hoặc emotional close
```

A câu có USP tốt nhưng emotional-arc mismatch (e.g. USP chứng minh ở đầu clip thay vì giữa) → DROP hoặc MOVE. A câu filler ngắn nhưng emotional-essential (closing reassurance, "trust me on this") → KEEP.

### Real metrics từ 10/07 incident (user re-edited 3 clips của em)

| Clip | Source | Agent V1 auto-edit | User re-edit | User saved thêm |
|------|--------|-------------------|--------------|-----------------|
| 0706 Lens macro KNF | 250.92s | 163.24s | 94.48s | **-68.76s (-42%)** |
| 0705 KNF cleaning pen | 216.18s | 197.30s | 117.10s | **-80.20s (-41%)** |
| 0715 Tripod ULANZI 1.6m | 267.27s | 236.91s | 90.40s | **-146.51s (-62%)** |

User edit không phải "cut thêm" — user cut **different things** vì hiểu narrative arc và emotional beats cần serve.

### Anti-patterns v2.35 (vĩnh viễn)

❌ **Run `classify_segs.py` và trust output verbatim** — script output là DRAFT only, không phải edit
❌ **Apply 7 patterns blind** (BRIDGE_NGAN, USP_LAP, CTA_HARDSELL, DEMO_DAI, INTRO_DAI, TREO_FILLER, NARRATIVE_COMPACT) — patterns chỉ là TOOL hỗ trợ, không phải quy tắc
❌ **Skip đọc `transcript_full.md`** — nơi hiểu narrative sống, không phải `keep_plan_troncau.txt`
❌ **"It's just filler/loop, drop it"** mà không hỏi "phục vụ emotional beat nào? Cái gì khác serve nó tốt hơn không?"
❌ **Auto-detect output là FINAL** không narrative review

### Cross-reference

- **`tiktok-video-editor` v3.19.1** (in-play umbrella skill 10/07) — full UNDERSTAND-FIRST workflow ở đó. Section tên "🎯 UNDERSTAND-FIRST EDITING v3.19.1".
- Hai skill giờ chia sẻ lesson — `video-cut-tiktok-shorts` focus 4-question gate trước Step 3; `tiktok-video-editor` focus STEP 3/4 của 5-step workflow. Load cả hai khi edit Vietnamese TikTok clips.

## Reference

- `references/ulanzi-cut-case-study.md` — Full case study của video Ulanzi ChaiBot 7 phút → 60s TikTok. Documents Whisper medium hallucinate → switch large-v3, 4 lần fail orientation trước khi vision catch, re-start detection bằng word overlap, TikTok script với 5 segments.
- `references/keep-plan-overlap-auto-trim-2026-07-28.md` — KEEP_PLAN overlap detection + auto-trim pattern. Critical: overlap trong source giữa các keep khiến filter_complex render 2 lần audio+frame. Adversarial verify KHÔNG thấy được vì check boundary frames only. (NEW 2026-07-28, real case 7 clip Pocket 3)
- `references/creative-arrange-demo-frameworks-2026-07-28.md` — 4 CREATIVE ARRANGE frameworks verified (Emotional HOOK / Counter-intuitive HOOK / PROBLEM→SOLUTION+OmniVoice PAIN / PROBLEM→SOLUTION from source). Decision matrix để chọn framework theo source characteristic. Whisper loop hallucinate anti-pattern. Mode B target 75-110s HARD RULE. Use khi anh yêu cầu demo kỹ thuật sắp xếp lại nội dung video.
- `references/google-drive-download-pattern.md` — Step-by-step curl workflow for Google Drive links without `gdown`. UUID extraction + drive.usercontent.google.com bypass for virus scan warning.
- `references/zoom-subtle-pocket3-portrait-2026-07-26.md` — Pocket 3 portrait 1728×3072 → 1080×1920 already tight. Zoom < 1.3x subtle. Objective verify protocol.
- `references/clean-delete-policy-2026-07-26.md` — User "bỏ X đi" → REMOVE HẲN khỏi code + docs. Anti-pattern leading-comment + helper files thừa.

## Related

- `telegram-video-analysis` — Phân tích video user gửi (vision + Whisper)
- `video-download-yt-dlp` — Download video từ YouTube/TikTok/Drive
- `tiktok-transcript-pipeline` — Extract transcript + script analysis
- `capcut-cli` — Alternative editor đọc draft_content.json (cho CapCut projects, không phải raw video)
- **`tiktok-video-editor`** — Skill chuyên edit TikTok clips. Có **3 LỚP TƯ DUY REASONING** từ v2.30 → v2.34: Lớp 1 ngữ pháp (#85 v2.30), Lớp 2 mục đích sản phẩm (#88 v2.33), Lớp 3 framework position (#89 v2.34) — mỗi câu phải pass qua 3 lớp này trước khi KEEP/SKIP. Cộng với #86 SENTENCE-COMPLETENESS, #87 SENTENCE-TREE ANALYSIS, 30+ pitfalls về Whisper hallucinate, boundary stitch, narrative preservation. **LOAD CẢ HAI SKILL** khi edit Vietnamese TikTok clips.

---

## 📋 CONSOLIDATION NOTE (for curator)

**Overlap warning:** `video-cut-tiktok-shorts` (umbrella, workflow-focused) ↔ `tiktok-video-editor` (companion, pitfalls-focused). Currently cross-referenced, NOT consolidated.

**Two skill consolidation plan (NOT YET EXECUTED):**
- `tiktok-video-editor` giữ 30+ Pitfall details + reference files
- `video-cut-tiktok-shorts` giữ 7-step workflow + 9-aspect-ratio Step 5 + Google Drive download
- Future merge: `tiktok-clip-editor` umbrella = workflow + 3-layer reasoning + numbered pitfalls. Sau đó `tiktok-video-editor` archive.

## 🧠 3-LAYER REASONING FRAMEWORK (link to tiktok-video-editor Pitfalls #85 + #88 + #89)

**⚠️ QUAN TRỌNG:** Mỗi câu trong source phải được kiểm tra qua **3 LỚP TƯ DUY** theo thứ tự trước khi giữ/bỏ. Lớp sau KHÔNG thay thế lớp trước — chúng stack lên nhau.

### Lớp 1: NGỮ PHÁP (Pitfall #85 v2.30)
3 câu test cho cấu trúc câu:
1. **Paraphrase được không?** — Tóm tắt 1 câu ngắn? Nếu KHÔNG → câu LỖI
2. **Hiểu độc lập không?** — Người xem chỉ nghe câu này hiểu ý? Nếu KHÔNG → câu TREO
3. **Predicate mấy lần?** — Nếu ≥ 2 lần trong cùng câu → câu LẶP LỖI

### Lớp 2: MỤC ĐÍCH SẢN PHẨM (Pitfall #88 v2.33)
3 câu test cho mục đích bán hàng:
1. **"Câu này nói về SẢN PHẨM gì?"** — sản phẩm cụ thể + đặc điểm, hay small talk/filler?
2. **"Thuộc vai trò nào trong 5?"** — HOOK/USP/PROBLEM/PROOF/CTA/NGOÀI
3. **"Có GIÚP MUA HÀNG không?"** — thuyết phục + bấm link, hay filler/self-repair?

Test mạnh: "Câu này có giúp người xem hiểu TẠI SAO họ nên mua sản phẩm không?" Nếu KHÔNG → BỎ kể cả khi câu có cấu trúc ngữ pháp đầy đủ.

### Lớp 3: FRAMEWORK POSITION (Pitfall #89 v2.34)
Workflow bắt buộc trước khi edit:
1. **B0**: Đọc sản phẩm + USP
2. **B1**: Đọc psychology viral framework master (5 biến HOOK/EMOTION/AUTHORITY/STORY/PRACTICAL VALUE + 6 hook types + Viral Journey Map 0-3s/3-15s/15-60s/60-90s/CTA)
3. **B2**: CHỌN framework phù hợp (VD: AUTHORITY+SOCIAL PROOF cho brand Dubai, CURIOSITY GAP nếu cần giữ bí mật, BEFORE-AFTER-BRIDGE cho transformation)
4. **B3**: VẼ phases của framework đã chọn
5. **B4**: Đọc source word-level
6. **B5**: ĐẶT MỖI CÂU vào đúng phase
7. **B6**: Verify framework completeness đủ các phases → B7: render

Câu nào KHÔNG map được vào phase nào → BỎ. Phase nào thiếu câu → tìm thêm hoặc chấp nhận gọn.

### Tại sao phải 3 lớp (lỗi em đã mắc 02/07)

**Sai Lớp 1 (ngữ pháp pure):** em giữ câu "hiệu này đây là thương hiệu amap này" vì nó CÓ chủ ngữ + vị ngữ → người xem nghe rối, gây mất tập trung.
**Sai Lớp 2 (sản phẩm pure):** em giữ câu đó vì nó thuộc AUTHORITY → vẫn lặp "thương hiệu" 2 lần gây khó chịu, người xem không tin là authority thật.
**Đúng Lớp 3 (framework):** câu đó KHÔNG map đúng vào phase AUTHORITY của framework AUTHORITY+SOCIAL PROOF → volume=0 từ đầu câu X đến đầu câu Y.

### Tổng hợp 3 lớp + 2 pitfall cú

```
[Source transcript] →
  ↓ LỚP 1 — split theo CÂU + 3 câu test ngữ pháp
  ↓ LỚP 2 — đánh dấu 5 vai trò HOOK/USP/PROBLEM/PROOF/CTA
  ↓ LỚP 3 — map vào phases của framework đã chọn
  ↓
[KEEP plan] = câu pass qua cả 3 lớp
[SKIP plan] = câu NGOÀI vai trò hoặc KHÔNG map phase
[VOLUME=0 plan] = filler/self-repair trong câu ĐÚNG (giữ audio KEEP dài)
  ↓
[Render] + verify
```

### References mới (v2.34.0)

- `references/sentence-boundary-rule-v2.30.md` — Pitfall #85 (Lớp 1 ngữ pháp)
- `references/sentence-completeness-rule-v2.31.md` — Pitfall #86 (CÂU TREO)
- `references/product-centric-reasoning-v2.33.md` — Pitfall #88 (Lớp 2 mục đích)
- `references/framework-driven-reasoning-v2.34.md` — Pitfall #89 (Lớp 3 framework) — MỚI
- `references/structural-sentence-reasoning-v2.32.md` — Pitfall #87 (SENTENCE-TREE — anti Lớp 1 pure)

---

## 🧠 STRUCTURAL SENTENCE-REASONING (link to tiktok-video-editor Pitfall #87)

**⚠️ QUAN TRỌNG:** Whisper segment KHÔNG = 1 sentence. 1 seg có thể chứa NHIỀU câu, HOẶC 1 câu lặp lỗi bị Whisper transcribe nguyên. Em KHÔNG được "lấy từng seg rồi ghép lại" mà phải phân tích TỪNG CÂU trong seg.

**3 câu test bắt buộc trước khi KEEP 1 câu:**

1. **Paraphrase được không?** — Em tóm tắt 1 câu ngắn? Nếu KHÔNG → câu LỖI
2. **Hiểu độc lập không?** — Người xem chỉ nghe câu này hiểu ý? Nếu KHÔNG → câu TREO
3. **Predicate mấy lần?** — Nếu ≥ 2 lần trong cùng câu → câu LẶP LỖI

**Workflow tổng hợp từ Pitfall #85, #86, #87:**

```
[Source transcript] → 
  ↓
[SPLIT into sentences per seg] (KHÔNG lấy từng seg)
  ↓
[For each sentence] → check 3 questions:
  - Q1: Paraphrase được? (ĐÚNG/LỖI)
  - Q2: Hiểu độc lập? (ĐỦ/TREO)
  - Q3: Predicate mấy lần? (1=OK, ≥2=LỖI)
  ↓
[Build KEEP plan] from ĐÚNG + ĐỦ sentences
  ↓
[Apply word-level cut] for LỖI/TREO if needed
```

**V19 evidence (clip3 phone stand, 23 source segs):**
- Skip 9 câu LỖI ("vô từ cái con chai bót" unclear, "hai con ốc hai con ốc" lặp, "tu viết điều chỉnh" lặp, "ví dụ như là cái cái cái" hallucinate loop, "không bao giờ bị" lặp, "sơn tẩn điện ở bên ngoài" lặp, "à à à" cuối clip)
- Word-level cut tại câu hoàn chỉnh (sau "nặng hơn" 86.32, KHÔNG cut tại seg boundary 87.28)
- 11 KEEPs narrative trọn vẹn, 0 hallucinate, CTA "bấm vào link phía dưới để mua hàng nhé" đầy đủ

**Anti-pattern (đã gây V11-V18 fail):**
- "Lấy từng seg rồi ghép lại" → NHẦM LẪN giữa "có text trong seg" vs "seg chứa câu hoàn chỉnh"
- Whisper hallucinate KHÔNG phải MLX bug — verified parallel test MLX vs Turbo (cả 2 đều 0 lặp khi KEEP boundary tính theo CÂU)

**Reference:** `media/tiktok-video-editor/references/structural-sentence-reasoning-v2.32.md`
