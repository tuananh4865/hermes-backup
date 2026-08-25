---
name: omnivoice-voice-clone
description: "Voice clone + TTS generation với OmniVoice 0.2.1 trên Mac M-series MPS. Trigger khi anh nói tạo voice, clone giọng, OmniVoice TTS, voice prompt, tổng hợp giọng nói, hoặc cần synthetic voice cho bất kỳ mục đích nào (video, narration, podcast, audiobook, content). Skill đã verify end-to-end: prompt save/load, batch generate, MPS workarounds, ref leak fix, amplitude bug fix, 13 non-verbal emotion tags, denoise workflow (ffmpeg afftdn). EMOTION TAGS BẮT BUỘC."
---

# OmniVoice Voice Clone — Hermes Skill

**Use when:** anh cần clone giọng thật từ audio 5-10s → tạo audio mới từ text bất kỳ. Phù hợp mọi use case cần synthetic voice: TikTok, YouTube narration, podcast, audiobook, video voiceover, v.v.

**Repo:** https://github.com/k2-fsa/OmniVoice
**Version verified:** 0.2.1 (master, 2026-07)
**Verified hardware:** Mac M-series (MPS), Python 3.11, torch 2.8.0
**Verified by:** Tuấn Anh, 2026-07-23 → 2026-07-24

**⚠️ TERMINOLOGY (24/07 — anh correct lần 1):**
- **ĐÚNG:** "file voice clone" / "file voice clone .pt" — file `VoiceClonePrompt` đã encode sẵn.
- **SAI:** "voice ref" — gợi ý raw audio, dễ nhầm với ref audio gốc.
- Khi viết memory hoặc report, LUÔN dùng "file voice clone .pt".

**⚠️ WORKFLOW ORDER (24/07 — anh correct lần 2):**
- **Bước 1: Dùng voice ref (audio gốc) ĐỂ CLONE** → save file voice clone `.pt`.
- **Bước 2: Dùng file voice clone .pt để GENERATE từ text script HOÀN TOÀN KHÁC ref.**
- Em đã sai khi dùng luôn text voice ref làm target input — đó là REF, không phải script test.

**⚠️ DENOISE WORKFLOW (24/07 — anh correct lần 3):**
- LUÔN denoise ref audio TRƯỚC khi save .pt.
- 3 mức: `afftdn=nf=-20` (light), `nf=-25` (medium), `nf=-30` (aggressive).
- Gửi anh check 3 mức → anh chọn → mới dùng.

---

## Quick Start (3 phút)

```bash
# 1. Setup (one-time)
cd /Volumes/Storage-1/Hermes/scratch/omnivoice-test
source .venv/bin/activate   # uv venv đã có sẵn từ session trước

# 2. Save voice clone (one-time, 5-10s ref audio)
#    a) Denoise ref audio TRƯỚC (anh yêu cầu 24/07)
ffmpeg -y -i ref_raw.wav \
  -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-20" \
  -ar 16000 -ac 1 -c:a pcm_s16le ref_denoised.wav

#    b) Check ref_rms — NẾU < 0.1 thì amplify
.venv/bin/python -c "
import soundfile as sf, numpy as np
audio, sr = sf.read('ref_denoised.wav')
r = np.sqrt(np.mean(audio.astype(np.float32)**2))
if r < 0.1:
    sf.write('ref_denoised_amp.wav', audio * (0.11/r), sr)
    print(f'amplified: {r:.4f} → 0.11')
"

#    c) Save .pt với ref_text NGẮN 1 câu ~100 chars
python3 scripts/save_voice_prompt.py save ref_denoised_amp.wav \
  "Câu đầu trong ref audio, khoảng 100 ký tự." \
  /Volumes/Storage-1/Hermes/voice-prompts/<name>.pt

# 3. Generate (mỗi lần dùng — instant, KHÔNG re-encode ref)
python3 scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/<name>.pt \
  --text "Text BẤT KỲ (KHÔNG phải ref text) — MỚI, có emotion tags" \
  --output out.wav
```

**Kết quả:** 24kHz mono WAV, 4-15s duration tùy text, voice giống ref audio.

---

## When to use this skill

| Scenario | Use this skill? |
|---|---|
| Tạo voice cho bất kỳ mục đích nào (TikTok, YouTube, podcast, audiobook, narration) | ✅ **YES** |
| Clone giọng thật của ai đó từ 5-10s audio ref | ✅ **YES** |
| Generate voice multilingual (Anh, Trung, Tây Ban Nha, v.v.) với giọng Việt làm anchor | ✅ **YES** |
| Voice design (không cần ref audio, describe attributes) | ✅ YES (xem Section 5) |
| Auto voice (không cần ref, no design) | ✅ YES — nhưng BẮT BUỘC thêm emotion tags |
| **Voice cần emotion/cảm xúc** (laugh, surprise, question) | ✅ **YES** — 13 non-verbal tags, xem Recipe 11. **EMOTION TAGS BẮT BUỘC** |
| 1 clip tiếng Việt bình thường, không cần authentic voice | ❌ Dùng `edge-tts NamMinh` thay (nhanh hơn 50x) |
| Realtime streaming TTS | ❌ OmniVoice không support |
| Production scale 1000+ file/giờ | ❌ Tốc độ MPS không đủ |

---

## 📚 7 LESSONS EMBEDDED FROM SESSION 2026-07-23/24

### L1: VoiceClonePrompt = Save Once, Reuse Forever (USER CORRECTION 23/07)

**Push-back:** *"Khoan, em import hết âm thanh này vào omnivoice để tạo template voice clone thôi chứ đâu cần lần nào cũng phải import lại âm thanh đâu"*

**Rule:** Luôn dùng `model.create_voice_clone_prompt()` → `prompt.save()` → `VoiceClonePrompt.load()` thay vì pass `ref_audio`/`ref_text` mỗi lần. **5x speedup (11s/file vs 18s/file)**.

### L2: Test Variants Trước Khi Conclude (USER CORRECTION 23/07)

**Push-back:** *"Tốt rồi! Nhưng Lúc em prompt omnivoice có vấn đề gì đó... chỉ cần fix prompt lại không inject câu đó vào nữa thôi!"*

**Rule:** Khi user nói "fix prompt/input, không workaround output" → test A/B/C/D variants of input trước khi conclude. 4 phút test saves hours debugging.

### L3: 13 Non-Verbal Tags = Free Emotion (USER DISCOVERY 23/07)

**Insight:** *"Anh thấy có phần Non-verbal & Pronunciation Control khá hay cộng thêm các key feature để thêm cảm xúc cho giọng đọc khiến cho giọng đọc giống người hơn!"*

**Verified:** 10/10 emotion variants PASS với prompt GOOJODOQ. Peak tăng rõ rệt (-2 to -3 dB vs -3.7 dB baseline).

**Rule:** Default to ZERO emotion/non-verbal tags. Any tag may create filler vocalizations such as “ựm, ờ, à, ồ, ờm, ừm” that Whisper can miss. Banned tags (verified 29/07 user rule): `[confirmation-en]`, `[question-en/ah/oh/ei/yi]`, `[surprise-ah/oh/wa/yo]`, `[dissatisfaction-hnn]`. Only `[laughter]` and `[sigh]` remain allowed if explicitly tested safe. Use a tag only when the user explicitly requests it and an A/B test proves it safe.

→ Xem `references/04-recipes.md` Recipe 11 cho full list 13 tags + voice template.

### L4: PHẢI Đọc Hết README + Follow Tất Cả Links (USER CORRECTION 23/07)

**Push-back:** *"Đọc hết phần readme của repo chưa?"*

**Rule:** Khi build skill từ GitHub repo:
1. Phase 1.5: Enumerate TẤT CẢ links trong README
2. Skip = explicit decision (ghi lý do trong SKILL.md "Beyond" section)
3. KHÔNG silent skip — user luôn đánh giá completeness

### L5: Concat Fade PHẢI NHẸ — 30ms (USER PREFERENCE 23/07)

**Push-back:** *"Khi em ghép batch lại với nhau thì để fadeout nhẹ thôi 30ms thôi"*

**Rule:** Dùng `concat_segments.py` của skill (đã verify trim 100ms lead/trail + 30ms fade out only). KHÔNG dùng `afade` đối xứng — tạo 60ms silent gap.

**Bonus:** Phase 4 dùng `pad_duration=0.0, fade_duration=0.0` → voice bắt đầu ngay sample 0, concat thẳng là mượt (no afade cần thiết).

### L6: Reader-Intent vs Writer-Intent (USER CORRECTION 24/07 — quan trọng)

**Push-back:** *"Voice này anh ghi âm lặp là do anh muốn thể hiện nhiều biểu cảm khác nhau!"*

**Anti-pattern:** Em nhìn voice lặp 1 cụm 5 lần → nghĩ là data không tốt → đề xuất ghi voice mới hoặc dùng clip khác. **SAI TO.**

**Correct pattern:** User CỐ Ý lặp cụm để model học **range emotion** khác nhau. Voice lặp KHÔNG phải lỗi — là design choice.

**Workflow:**
- (a) **Verify user intent** trước khi đề xuất fix
- (b) Nếu CỐ Ý → giữ, dùng emotion tags + instruct để amplify emotion range
- (c) Nếu data lỗi → chỉ đề xuất fix sau khi đã verify intent

**Pitfall #8 (mới):** Nếu user KHÔNG cố Ý lặp → model sẽ leak cụm đó vào MỌI output. Fix: ghi voice mới với nhiều câu KHÁC NHAU trong 5-10s.

### L7: Denoise Workflow CHỦ ĐỘNG (USER CORRECTION 24/07)

**Push-back:** *"Trước tiên em denoise cho voice ref trước rồi gửi anh check"*

**Anti-pattern:** Em jump thẳng vào generate voice mà KHÔNG denoise ref audio. Kết quả: voice có noise ẩn, peak thấp hơn dự kiến.

**Correct pattern:** LUÔN denoise ref audio TRƯỚC khi save `.pt`:
1. Denoise 3 mức: `afftdn=nf=-20` (light), `nf=-25` (medium), `nf=-30` (aggressive)
2. Gửi anh check 3 mức để anh chọn (mỗi mức là 1 file WAV)
3. Sau khi anh chọn → mới dùng để save .pt

**Denoise recipe (chuẩn):**
```bash
ffmpeg -y -i ref_raw.wav \
  -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-20" \
  -ar 16000 -ac 1 -c:a pcm_s16le ref_denoised.wav
```

### L8: Workflow Order (USER CORRECTION 24/07)

**Push-back:** *"Đầu tiên em phải dùng voice ref để clone! Sau khi clone xong mới dùng để tạo voice cho script chứ!"*

**Anti-pattern:** Em dùng luôn text voice ref (Whisper transcript) làm target input cho generate → tạo ra output nói lại CÂU REF (verify bằng test).

**Correct pattern:**
- Voice ref audio = INPUT để clone. Chỉ dùng 1 lần để save .pt.
- Script test = INPUT khác hoàn toàn. Đánh giá clone có generalize không.
- KHÔNG dùng Whisper transcript của ref audio làm target input.

### L9: SMOOTH CONFIG — Fix Jerky Voice (BẮT BUỘC 24/07)

**Symptom (anh complaint 24/07):** *"Giọng thì rõ nhưng ngắt quãng rất khó chịu"*

**Root cause:** `layer_penalty_factor=5.0` (default) → model over-penalize token → prosody ngắt quãng + Whisper transcript sai ("dòng colo" thay vì "giọng clone").

**Verified fix (A/B test 7 variants 24/07):**

| Param | Default | SMOOTH (FIX) | Effect |
|---|---|---|---|
| `layer_penalty_factor` | 5.0 | **1.0** | Smooth prosody, Whisper transcript đúng |
| `position_temperature` | 5.0 | **3.0** | Mượt hơn |
| `speed` (qua generate) | 1.0 | **0.95** | Chậm 5%, đời thường |

**Config chuẩn (đã hardcode trong `scripts/generate_voice.py`):**

```python
gc = OmniVoiceGenerationConfig(
    pad_duration=0.0,           # NO PADDING (concat mượt)
    fade_duration=0.0,          # NO FADE
    denoise=True,               # NGĂN leak ref text (Pitfall #9)
    layer_penalty_factor=1.0,   # ← KEY FIX: smooth prosody
    position_temperature=3.0,   # ← Mượt hơn
)
# Plus: speed=0.95 qua model.generate()
```

**Anti-pattern (NEVER):** Dùng `layer_penalty_factor=5.0` mặc định → voice ngắt quãng + Whisper transcript sai.

Xem `references/07-smooth-config-deep-dive.md` cho full A/B test matrix.

### L10: Workflow SIMPLE — KHÔNG cho setting gì vào prompt (USER PREFERENCE 24/07)

**Push-back:** *"Không cho setting gì vào prompt hết chỉ đơn giản gọi voice clone và nội dung kèm emotion tag thôi"*

**Anti-pattern:** Em default expose `--speed`, `--layer-penalty`, `--pos-temp`, `--with-padding` flags trong script CLI. → User phải đọc docs để biết dùng flag nào.

**Correct pattern (hardcode mọi setting bên trong):**

```bash
# SINGLE — chỉ cần 2 thứ
python3 scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/<name>.pt \
  --text "[emotion-tag] Nội dung[emotion-tag]" \
  --output out.wav

# BATCH
python3 scripts/generate_voice.py \
  --prompt <pt> \
  --jsonl inputs.jsonl \
  --output-dir batch/
```

**Config hardcoded bên trong (verified 24/07):**
- `pad_duration=0, fade_duration=0` (NO PADDING)
- `denoise=True` (Pitfall #9)
- `layer_penalty_factor=1.0` (L9 smooth)
- `position_temperature=3.0`
- `speed=0.95` qua generate()

**NẾU cần custom config** (rare) → dùng `--layer-penalty` `--pos-temp` `--speed` flags (đã có sẵn với default đúng).

### L11: Auto-Trim Trailing Silence (BUG FIX 24/07)

**Symptom (anh complaint 24/07):** *"Khi ghép ffmpeg có fade không mà bị mờ ở khúc đầu và khúc cuối voice vậy?"*

**Root cause:** KHÔNG phải ffmpeg fade (em không apply fade). Là do `postprocess_output=True` mặc định của OmniVoice → model tự sinh 16-35ms trailing silence:

| Segment | Trailing silence (verified) |
|---|---|
| 01_hook | 0.0ms ✅ |
| 02_pain | 16.7ms |
| 03_solution | 34.6ms |
| 04_usp | 22.7ms |
| 05_cta | 26.8ms |

Khi concat 5 file → trailing silence cộng dồn (~100ms gap) → nghe "mờ đầu/cuối".

**Fix (auto-trim trong script):**

```python
def trim_trailing_silence(path: str, threshold: float = 0.001) -> float:
    """Trim trailing silence >10ms. Keeps 240 samples (10ms at 24kHz) buffer."""
    audio, sr = sf.read(path)
    abs_audio = np.abs(audio)
    n = len(audio)
    last_active = n
    for i in range(n - 1, -1, -1):
        if abs_audio[i] > threshold:
            last_active = i + 1
            break
    trim_to = min(last_active + 240, n)  # Keep 10ms buffer
    if trim_to < n - int(0.01 * sr):  # Only trim if >10ms silent
        trimmed = audio[:trim_to]
        sf.write(path, trimmed, sr)
    return len(trimmed) / sr
```

**Verified (5 segments Lenspen TikTok):**

| File | Before trim | After trim |
|---|---|---|
| 02_pain | 16.7ms | 10.0ms ✂️ |
| 03_solution | 34.6ms | 10.0ms ✂️ |
| 04_usp | 22.7ms | 14.2ms (skipped) |
| 05_cta | 26.8ms | 19.5ms (skipped) |

**Rule:** Auto-trim trailing silence >10ms sau khi generate. Đã hardcode trong `scripts/generate_voice.py` — không cần config.

**Important:** KHÔNG touch leading silence (file bắt đầu ngay sample 0 từ `pad_duration=0`).

---

## 5-Phase Production Workflow

### Phase 1: Check file voice clone đã có sẵn chưa

**File voice clone = file `.pt` (VoiceClonePrompt) đã encode sẵn từ ref audio + ref_text. Lưu ở `/Volumes/Storage-1/Hermes/voice-prompts/`.**

```bash
ls /Volumes/Storage-1/Hermes/voice-prompts/
# Hiện tại:
#   - tuan_anh_5s_1sent_amp.pt (9.9KB, voice GOOJODOQ review, BEST)
#   - tuan_anh_v5_aggressive_denoise.pt (17.6KB, voice msg aggressive denoise)

# NẾU ĐÃ CÓ file .pt phù hợp → SKIP Phase 2-3, đi thẳng Phase 4 (Generate)
# NẾU CHƯA CÓ hoặc muốn voice MỚI → làm Phase 2-3 dưới đây
```

### Phase 2: Prepare & Denoise reference audio

**Requirements:**
- Format: WAV/MP3/M4A/OGG, bất kỳ sample rate nào
- Duration: **5-10 giây sweet spot** (3s tối thiểu, 20s degradation)
- Content: voice thật, **không nhạc nền**, **không tiếng ồn**
- **Critical: voice đó PHẢI LÀ VOICE NGƯỜI THẬT** — KHÔNG phải AI TTS outro hook

**Step 1: Extract 5-10s từ raw video:**
```bash
# Từ DJI Pocket 3 hoặc iPhone
ffmpeg -y -ss 10 -i raw_video.mov -t 5 -ar 16000 -ac 1 -c:a pcm_s16le ref_5s.wav

# Từ voice message Telegram
ffmpeg -y -i voice.ogg -t 5 -ar 16000 -ac 1 -c:a pcm_s16le ref_5s.wav

# Test verify: Whisper transcribe
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir ./verify/ ref_5s.wav
cat verify/ref_5s.txt
```

**Step 2: Denoise 3 mức, gửi anh chọn (Lesson L7):**
```bash
# Light: nf=-20
ffmpeg -y -i ref_5s.wav -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-20" \
  -ar 16000 -ac 1 ref_denoise_light.wav

# Medium: nf=-25
ffmpeg -y -i ref_5s.wav -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-25" \
  -ar 16000 -ac 1 ref_denoise_medium.wav

# Aggressive: nf=-30
ffmpeg -y -i ref_5s.wav -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-30" \
  -ar 16000 -ac 1 ref_denoise_aggressive.wav

# Gửi 3 file cho anh check → anh chọn 1
```

**Step 3: Amplify nếu ref_rms < 0.1 (Pitfall #2):**
```bash
.venv/bin/python -c "
import soundfile as sf, numpy as np
audio, sr = sf.read('ref_denoise_chosen.wav')
ref_rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
print(f'Current ref_rms: {ref_rms:.4f}')
if ref_rms < 0.1:
    audio_amp = audio * (0.11 / ref_rms)
    sf.write('ref_denoise_chosen_amp.wav', audio_amp, sr)
    print(f'Amplified → ref_denoise_chosen_amp.wav (new ref_rms: 0.11)')
"
```

### Phase 3: Save file voice clone (.pt) — one-time, 5s encode

```bash
# QUAN TRỌNG: ref_text phải NGẮN (~100 chars, 1 câu đầu)
# KHÔNG dùng full transcript — sẽ leak câu cuối vào output (Pitfall #3)
python3 scripts/save_voice_prompt.py save \
  ref_denoise_chosen_amp.wav \
  "Câu đầu tiên trong ref audio, khoảng 100 ký tự." \
  /Volumes/Storage-1/Hermes/voice-prompts/<name>.pt
```

Output: file `.pt` ~10KB, chứa `ref_audio_tokens` + `ref_text` + `ref_rms`. **Save 1 lần, dùng mãi mãi.**

### Phase 4: Generate từ file voice clone (.pt) — instant, ~12s/file, **BẮT BUỘC emotion tags**

**🔴 MANDATORY: Mỗi segment PHẢI có ≥1 emotion tag. Voice mặc định có emotion, baseline phẳng = chưa đạt chuẩn.**

**Generate bằng cách LOAD file `.pt` đã save (KHÔNG encode lại ref audio mỗi lần):**

```bash
# Single text — mặc định KHÔNG emotion tags
python3 scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh.pt \
  --text "Hôm nay mình giới thiệu sản phẩm mới" \
  --output out.wav

# Batch từ JSONL — mỗi entry mặc định KHÔNG có emotion tags
python3 scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh.pt \
  --jsonl 5_texts.jsonl \
  --output-dir batch_results/
```

**⚠️ LESSON L8 — Script test phải KHÁC HOÀN TOÀN ref text:**
- Voice ref audio là INPUT clone — chỉ dùng 1 lần để save .pt
- Script test là INPUT khác — đánh giá clone có generalize không
- KHÔNG dùng Whisper transcript của ref audio làm target input

**Output:** 24kHz mono WAV, 4-15s duration, voice giống ref.

### Phase 5: Verify (bắt buộc — đã catch 3 bugs trong session này)

```bash
# Verify 1: volumedetect (peak > -10 dB = không silent)
ffmpeg -i out.wav -af "volumedetect" -vn -f null - 2>&1 | grep max_volume

# Verify 2: Whisper transcript (clean content, không ref leak)
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir /tmp/verify/ out.wav
cat /tmp/verify/out.txt
# Phải chỉ chứa text đã generate, KHÔNG có câu ref audio

# Verify 3: emotion peak tăng (có emotion tags là peak cao hơn baseline)
# Baseline (no tag): -3.7 dB
# Tag nhẹ phù hợp nội dung: confirmation, question, sigh
```

### Phase 6: Concat (nếu N file) — DÙNG `concat_segments.py` CÓ SẴN

**QUAN TRỌNG — anh yêu cầu fadeout 30ms nhẹ. Skill đã verified tự động cắt gap (vì Phase 4 dùng `pad_duration=0`):**

```bash
python3 scripts/concat_segments.py \
  --inputs-dir batch_results/ \
  --output tiktok_FINAL.wav
# Default: 30ms fade out only (no padding từ generate)
```

**Inputs của Phase 6 PHẢI đã generate với `pad_duration=0` (NO PADDING), không cần afade ở concatenate step vì voice bắt đầu ngay sample 0.**

---

## Production Resources

### Voice clone files hiện có (`/Volumes/Storage-1/Hermes/voice-prompts/`)

| File | Size | ref_rms | Source | Note |
|---|---|---|---|---|
| `tuan_anh_5s_1sent_amp.pt` | 9.9KB | 0.1100 | 5s từ video GOOJODOQ review | **BEST — voice "reviewer chuyên nghiệp"** |
| `tuan_anh_v5_aggressive_denoise.pt` | 17.6KB | 0.1177 | 10s voice msg aggressive denoise | Voice "đời thường", emotion range |

**Recommendation:** Dùng `tuan_anh_5s_1sent_amp.pt` cho production content (TikTok, YouTube). Dùng voice msg chỉ khi cần casual tone.

### Scripts (5 scripts + 1 wrapper)

- `scripts/save_voice_prompt.py` — Encode ref audio → save .pt
- `scripts/generate_voice.py` — Load .pt → generate (NO PADDING default)
- `scripts/verify_audio.py` — 3-layer verify (ffprobe + volumedetect + Whisper)
- `scripts/concat_segments.py` — 30ms fade out only
- `scripts/test_emotion.py` — Test 10 emotion variants
- `scripts/with_venv.sh` — Auto-activate OmniVoice venv wrapper

### References (5 docs)

- `references/00-pitfalls.md` — 6 pitfalls + verified fixes
- `references/01-api-surface.md` — Full Python API + dataclasses
- `references/02-cli-commands.md` — 3 CLI entry points
- `references/03-known-issues.md` — GitHub issues + workarounds
- `references/04-recipes.md` — 11 recipes (incl. Non-Verbal emotions, voice template)
- `references/06-denoise-flag-findings-2026-07-24.md` — **Pitfall #9 investigation** (denoise flag A/B test, 6 variants, root cause)

---

## 📚 8 Critical Pitfalls (Quick Reference)

| # | Pitfall | Symptom | Fix |
|---|---|---|---|
| 1 | **ref_audio format/sr/channels** | WAV 16kHz mono | Convert từ M4A/MP3 bằng ffmpeg |
| 2 | **ref_rms ≥ 0.1** | Output bị giảm 1/6 amplitude | Amplify ref audio 0.11/rms trước save prompt |
| 3 | **ref_text ≤ 1 câu ~100 chars** | Output leak câu cuối ref_text | Whisper transcribe → lấy 1 câu đầu |
| 4 | **ZERO EMOTION TAG mặc định** | Tag có thể sinh “ựm, ờ, à, ồ, ờm, ừm” mà Whisper không bắt được | Chỉ dùng tag khi user yêu cầu và đã A/B test an toàn |
| 5 | **pad_duration=0, fade_duration=0** | Clip có gap silent 100-200ms | Set trong OmniVoiceGenerationConfig |
| 5b | **YouTube: pad=0.15, fade=0.03** | Bù đệm cho đầu/đuối câu, fade nhẹ không pop | Verified 29/07 pilot hố đen |
| 6 | **Sequential generate** (không dùng batch CLI) | MPS batch ≥5 silent output | for-loop 1-by-1 trong cùng process |
| 7 | **TikTok CDN audio WHISPER VERIFY FIRST** | Download có thể là watermark outro | Whisper transcribe → check voice thật |
| 8 | **Voice ref lặp 1 cụm → model leak cụm đó** (24/07) | Output có cụm từ ref audio | Verify user intent; nếu user CỐ Ý lặp → dùng emotion tags + instruct để đè, nếu data lỗi → ghi voice mới đa dạng câu |
| 9 | **`denoise=True` REQUIRED** (24/07) | Output bắt đầu bằng ref text echo khi `denoise=False` | LUÔN explicit set `denoise=True` trong `OmniVoiceGenerationConfig`. Echo 1-2 từ OK, leak cả câu = sai. Xem `references/06-denoise-flag-findings-2026-07-24.md` |

**Xem full detail:** `references/00-pitfalls.md`

---

## Performance benchmarks (Mac M-series, ref 5-10s)

| Operation | Time | RAM peak |
|---|---|---|
| Model load (cold) | 60s | 12.5GB |
| Model load (warm) | 1.7s | 12.5GB |
| Save prompt (one-time) | 5s | 12.5GB |
| Generate 1 file (12s ref) | 12-15s | 12.68GB |
| Generate 6 files (sequential) | 60s | 12.68GB |

---

## Anti-Patterns Summary (ĐỌC TRƯỚC KHI LÀM)

1. **KHÔNG dùng text voice ref làm target input** — voice ref = INPUT clone, script test = INPUT khác (L8)
2. **KHÔNG gọi "voice ref"** — gọi đúng là "file voice clone .pt" (terminology 24/07)
3. **KHÔNG skip denoise** — anh explicit yêu cầu denoise 3 mức, gửi check, rồi mới save (L7)
4. **KHÔNG nhìn voice lặp = data lỗi** — verify user intent trước (L6)
5. **KHÔNG skip emotion tags** — voice phẳng = chưa đạt chuẩn (L3)
6. **KHÔNG dùng omnivoice-infer-batch ≥5 MPS** — silent output bug
7. **KHÔNG trim/fade sau concat** — disable padding từ generate (L5)
8. **KHÔNG amplify trong OmniVoice config** — amplify ref audio trước save .pt
9. **KHÔNG dùng `layer_penalty_factor=5.0` default** — voice ngắt quãng, set `=1.0` (L9)
10. **KHÔNG expose nhiều CLI flags** — hardcode config bên trong, workflow chỉ cần `--prompt + --text` (L10)

---

## Community projects (16 third-party)

| Project | Use case | Relevant cho anh? |
|---|---|---|
| [ComfyUI-OmniVoice-TTS](https://github.com/Saganaki22/ComfyUI-OmniVoice-TTS) | ComfyUI node | ❌ Em không dùng ComfyUI |
| [pyVideoTrans](https://github.com/jianchang512/pyvideotrans) | Video translation dubbing | ✅ Có thể dùng cho dịch Vi→En |
| [OpenVoice](https://github.com/myshell-ai/OpenVoice) | Voice clone alternative | ❌ OmniVoice đã đủ |
| [GPT-SoVITS](https://github.com/RVC-Boss/GPT-SoVITS) | Voice clone với fine-tuning | ❌ Overkill cho use case |
| Xem thêm 12 projects khác trong `docs/community-projects.md` của repo |

---

## Roadmap (next steps)

- [ ] Auto-detect ref audio từ Pocket 3 raw clip + auto-extract 5s sweet spot
- [ ] Voice design mode (gender/age/pitch) without ref audio
- [ ] Cache model globally để skip load 1:30 mỗi session
- [ ] Cross-lingual clone test (ref Vi → text En)
- [ ] **Emotion tuning** — Test which non-verbal tag combination works best cho engagement (A/B test với audience)
- [ ] **omnivoice-server** integration — Replace sequential generation với HTTP API khi scale > 10 clips/giờ
- [ ] **OmniVoice-MLX** benchmark — So sánh MPS vs MLX speed khi cần scale
- [ ] **pyVideoTrans** integration — dịch Vi→En dubbing pipeline

- [ ] **Voice sample library** — Test 3+ voice tone styles (reviewer, casual, professional) từ nhiều ref audio khác nhau
- [ ] **Denoise auto-prompt** — Tự hỏi anh "denoise 3 mức trước?" thay vì jump thẳng vào save (L7)

---

## CHANGELOG

- **v1.4 (24/07/2026)** — Added Lessons L9 (SMOOTH config `layer_penalty_factor=1.0`, fix jerky voice), L10 (simple workflow — KHÔNG expose CLI flags, hardcode bên trong), L11 (auto-trim trailing silence 16-35ms từ `postprocess_output=True`). Added Pitfall #10 (default layer_penalty) + #11 (trailing silence). Created `references/07-smooth-config-deep-dive.md`. Tested với wiki script TikTok Lenspen (5 segments, 51.5s, Whisper transcript sạch).
- **v1.3 (24/07/2026)** — Added Lessons L6 (voice lặp = design choice), L7 (denoise workflow), L8 (workflow order). Added Pitfall #8 (ref leak from repeated phrases). Updated terminology from "voice ref" → "file voice clone .pt". Added Denoise 3-mức recipe. Verified `tuan_anh_v5_aggressive_denoise.pt` work với 6-câu test script.
- **v1.2 (23/07/2026)** — Initial production version. 6 pitfalls, 11 recipes, 5 scripts.

---

## Session 2026-07-24 — Wiki Script Test (Lenspen)

**Output:** `/Volumes/Storage-1/Hermes/voice-compare/2026-07-24-lenspen-wiki/FINAL_LENSPEN_TIKTOK.wav` (51.5s)

**Source script:** `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/scripts/lenspen-ve-sinh-ong-kinh-problem-solution.md` (VERSION A)

**5 segments:** HOOK → PAIN → SOLUTION → USP → CTA + emotion tags

**Key fix:** Auto-trim trailing silence >10ms trong `generate_voice.py` — see `wiki/concepts/omnivoice-trailing-silence-fix-2026-07-24.md`
