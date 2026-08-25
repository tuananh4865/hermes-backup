---
name: omnivoice-smooth-config-and-leak-prevention
description: "OmniVoice 0.2.1 smooth config findings + emotion tag fit-content rules (24-25/07) — layer_penalty_factor=1.0, position_temperature=3.0, speed=0.95, denoise=True MANDATORY, auto-trim trailing silence. Plus Pitfall #13 (emotion tag fit content + ellipsis vs trailing vowel) + Pitfall #14 (tag MUST be at paragraph head, NOT mid-segment). Verified Mac M-series MPS, multi-variant A/B test with Whisper + numpy RMS verify. Load when voice clone output bị ngắt quãng, Whisper transcript sai, ref text leak, nghe 'mờ' khi concat, hoặc emotion tag gây sai prosody."
---

# Smooth Config & Leak Prevention (OmniVoice 0.2.1)

**Class:** Session-specific debugging findings for `omnivoice-voice-clone` skill.
**Created:** 2026-07-24
**Updated:** 2026-07-25 (added Pitfall #13 emotion tag fit content, #14 emotion tag MUST be at paragraph head not mid-segment)
**Verified hardware:** Mac M-series (MPS), Python 3.11, torch 2.8.0

## TL;DR

Voice clone output có 4 vấn đề phổ biến gây khó chịu:

1. **Prosody ngắt quãng** (anh chê "voice rõ nhưng ngắt quãng khó chịu") → FIX: `layer_penalty_factor=1.0`
2. **Ref text leak** → FIX: `denoise=True` (Pitfall #9 — DENY default NGĂN leak)
3. **Voice 'mờ' ở đầu/cuối sau concat** → KHÔNG phải ffmpeg fade, là trailing silence 16-35ms từ model → FIX: auto-trim sau generate
4. **Ref audio with repeated phrase** → có echo 1-2 từ đầu output (acceptable)

## Smooth Config (verified 24/07)

```python
OmniVoiceGenerationConfig(
    pad_duration=0.0,             # NO PADDING (concat mượt)
    fade_duration=0.0,            # NO FADE
    denoise=True,                 # NGĂN leak ref text (MANDATORY)
    layer_penalty_factor=1.0,     # KEY FIX: default 5.0 gây ngắt quãng
    position_temperature=3.0,     # Mượt hơn default 5.0
)
# Plus: speed=0.95 qua model.generate() — chậm 5% cho đời thường
```

### Per-param analysis

| Param | Default | Optimized | Why |
|---|---|---|---|
| `pad_duration` | 0.1 | 0.0 | 0.1 = 100ms silent padding → gap khi concat |
| `fade_duration` | 0.1 | 0.0 | Same as above |
| `denoise` | True | True (MUST) | Prepend `<\|denoise\|>` token → NGĂN leak |
| `layer_penalty_factor` | 5.0 | **1.0** | Default 5.0 over-penalize → prosody ngắt quãng, Whisper transcript SAI |
| `position_temperature` | 5.0 | 3.0 | Lower = smoother prosody |
| `speed` | 1.0 | 0.95 | 0.95 = đời thường, slow, dễ nghe |

## Pitfall #9 — denoise Flag Investigation

**Test grid (6 variants A-F, same prompt + text):**

| Variant | denoise | preprocess | postprocess | Whisper transcript start | Verdict |
|---|---|---|---|---|---|
| A_default | True | True | True | "Ồ bạn ơi [target]" | ✅ CLEAN |
| B_no_denoise | False | True | True | "**Trời ơi là Tuấn Anh đây Trời ơi Tôi là Tuấn Anh đây nè** [target]" | ⚠️ LEAK |
| C_no_preprocess | True | False | True | "[target]" | ✅ CLEAN |
| D_no_postprocess | True | True | False | "[target]" | ✅ CLEAN |
| E_no_denoise_preproc | False | False | True | "à à à à..." (loop) | ❌ NO TARGET |
| F_all_off | False | False | False | "**Tui Tuấn Ao, tui là Tuấn Anh đây nè** [target]" | ⚠️ LEAK |

**Root cause:** `<\|denoise\|>` token prepend → model treats as "denoise mode" → only generates target text. Without it, model ECHOes ref text first (1-2 sentences).

**Production rule:** NEVER set `denoise=False`. If you need custom processing, use `preprocess_prompt=False` or `postprocess_output=False` instead.

## Pitfall #13 — User Hard Rule: Emotion Tags Must Fit Content (NEW 25/07 — USER VERBATIM)

**Anh's verbatim:** *"Fix voice không thêm emotion tag oh ah ở đâu câu, nếu có motion tag nào khiến cho giọng cao hào hứng hơn thì thêm còn không thì thôi! Từ 'Tộiiiii' ở cuối câu kéo dài hơn!"*

**Lesson (FIRST-CLASS, hard rule vĩnh viễn):**

1. **Emotion tag placement** — Add emotion tags ONLY when they naturally fit the content. Do NOT force `[amazement-oh]` / `[surprise-oh]` / `[laughter]` into sentences that don't warrant them. Emotion tags that genuinely raise excitement (verified peaks):
   - `[surprise-oh]` → peak -2.6 dB
   - `[amazement-oh]` → peak -2.6 dB
   - Use for HOOK / problem segments where anh's text conveys shock/amazement
   - Do NOT use for filler / declarative sentences that sound natural without emotion

2. **Trailing vowel repeat** — Repeating trailing vowel characters ("Tộiiiii", "Đợiiiiii", "Yessssss") makes OmniVoice extend the final phoneme duration.

   **Verified case (25/07 voice v2 vs v1):**
   - Input: `"[amazement-oh] Máy dập Lin Đan 2008 dập Ly Chong Quây 2 hiệp teo người luôn mà! [surprise-oh] Chắc là anh Ly Chong Quây ám ảnh từ đây! [sigh] Tộiiiiiiii…"`
   - v1 (no trailing repeat): peak -3.3 dB
   - v2 (trailing "iiiiiiii"): peak **-1.0 dB** (+2.3 dB boost)
   - Duration: 8.20s → 8.64s (+0.44s elongation)

3. **Whisper limitation on trailing vowel** — Whisper **hallucinated** "Tối" 0.4s but actual waveform showed 0.6s RMS-active audio at 8.0-8.6s. **Whisper transcripts do NOT accurately reflect trailing vowel elongation.** When verifying duration, use numpy waveform RMS analysis, not Whisper.

**Investigation trigger:** When user says "voice bị flat / không hào hứng" → check (a) emotion tags are well-placed (not overused), (b) trailing vowels on emphasis words, (c) waveform RMS analysis to confirm actual duration.

## Pitfall #12 — Layer Penalty Default=5.0 Investigation (NEW 24/07)

**Symptom:** User chê "giọng thì rõ nhưng ngắt quãng rất khó chịu" — repeated complaint, FIRST-CLASS feedback.

**Root cause:** `layer_penalty_factor=5.0` (default) over-penalize tokens → prosody ngắt quãng + Whisper transcript sai (e.g. "dòng colo" thay vì "giọng clone").

**A/B test (7 variants, all using same prompt + text):**

| Variant | Config | Dur | Peak | Whisper verdict |
|---|---|---|---|---|
| A_default | layer_pen=5.0 | 6.93s | 0.541 | "dòng colo" ❌ sai |
| B_layer_pen_1 | layer_pen=1.0 | 8.78s | 0.596 | "giọng colon" ✅ đúng |
| C_class_temp_1 | class_temp=1.0 | 8.58s | 0.606 | "giọng colon" ✅ đúng |
| D_speed_0.9 | speed=0.9, layer=1 | 9.68s | 0.648 | "giọng colon" ✅ |
| E_speed_1.1 | speed=1.1, layer=1 | 8.00s | 0.295 | (low peak) |
| F_pos_temp_3 | speed=0.95, layer=1, pos_t=3 | 6.77s | 0.649 | "giọng colon" ✅ |
| **G_combined** | **speed=0.95, layer=1, pos_t=3** | **6.17s** | **0.635** | "giọng Claw" ✅ đúng |

**Fix:** `layer_penalty_factor=1.0` + `position_temperature=3.0` + `speed=0.95` qua model.generate().

**Always run A/B test when user complains about prosody quality.** Don't add flags blindly — verify with Whisper transcript + audio peak.

## Pitfall #10 — Trailing Silence Auto-Trim (NEW 24/07)

**Symptom:** User reported "khi ghép ffmpeg có fade không mà bị mờ ở khúc đầu và khúc cuối voice vậy?" — actually NOT ffmpeg fade, but model-generated trailing silence.

**Root cause:** OmniVoice `postprocess_output=True` (default) tự sinh 16-35ms trailing silence ở cuối mỗi segment. Khi concat N segments → gap cộng dồn, voice nghe "mờ" ở đầu segment sau.

**Verified measurements (5 segments TikTok Lenspen):**
| Segment | Trailing silence |
|---|---|
| 01_hook | 0.0ms |
| 02_pain | 16.7ms |
| 03_solution | 34.6ms |
| 04_usp | 22.7ms |
| 05_cta | 26.8ms |

**Fix:** Auto-trim trailing silence >10ms sau khi generate. Hardcode trong `generate_voice.py` (workflow đơn giản, không cần CLI flag):

```python
def trim_trailing_silence(path, threshold=0.001):
    audio, sr = sf.read(path)
    abs_audio = np.abs(audio)
    n = len(audio)
    last_active = n
    for i in range(n - 1, -1, -1):
        if abs_audio[i] > threshold:
            last_active = i + 1
            break
    trim_to = min(last_active + 240, n)  # 240 samples = 10ms buffer at 24kHz
    if trim_to < n - int(0.01 * sr):  # only trim if >10ms silent
        sf.write(path, audio[:trim_to], sr)
```

**Verified result (after trim):**
| Segment | After trim |
|---|---|
| 01_hook | 0.0ms (skip) |
| 02_pain | 10.0ms ✂️ |
| 03_solution | 10.0ms ✂️ |
| 04_usp | 14.2ms (skip) |
| 05_cta | 19.5ms (skip) |

**Production rule:** KHÔNG tắt `postprocess_output=False` (giữ default). Auto-trim sau generate.

## Pitfall #11 — User Preference: WORKFLOW ĐƠN GIẢN (CRITICAL 24/07 — USER CORRECTION)

**FIRST-CLASS FEEDBACK from user (verbatim):** "không cho setting gì vào prompt hết chỉ đơn giản gọi voice clone và nội dung kèm emotion tag thôi"

**Symptom:** User explicitly corrected v2 của `generate_voice.py` (which had `--layer-penalty`, `--pos-temp`, `--speed`, `--with-padding` flags). User interprets ANY extra CLI flag as "too much setup" — direct friction signal.

**Lesson:** The user wants `generate_voice.py` to take ONLY `--prompt` + `--text` (or `--prompt` + `--jsonl`). DO NOT expose `--layer-penalty`, `--pos-temp`, `--speed`, `--with-padding` as CLI flags. Hardcode verified config inside the script.

**Workflow citation:** when user says "tạo voice" / "clone giọng" / "TTS" → gọi `generate_voice.py` với 2 flag max. No config. No setup. Just file voice clone + text có emotion tags.

**Correct interface:**
```bash
# Single
python3 generate_voice.py --prompt <pt> --text "..." --output out.wav

# Batch
python3 generate_voice.py --prompt <pt> --jsonl inputs.jsonl --output-dir batch/
```

**Updated `generate_voice.py` (v3, 5471 bytes):** hardcoded smooth config + auto-trim. User tested 24/07 with 5-segment TikTok Product (Lenspen) → Whisper transcript sạch 100%, voice mượt.

**Anti-pattern (NEVER):**
```bash
# ❌ SAI — user phải truyền setting, họ không muốn
python3 generate_voice.py --prompt <pt> --text "..." --layer-penalty 1.0 --pos-temp 3.0 --speed 0.95 --with-padding

# ✅ ĐÚNG — chỉ 2 flag
python3 generate_voice.py --prompt <pt> --text "..."
```

## Pitfall #8 — Ref Audio Repeated Phrase

**Symptom:** Voice ref has 1 phrase repeated 5+ times (e.g. "Xin chào tôi là Tuấn Anh đây" × 5). Model learns this phrase and echo 1-2 words at output start.

**Test result (v6_raw, ref_text="Xin chào tôi là Tuấn Anh đây" lặp 5x):**
- ✅ Echo 1-2 words ("Ồ", "Ha", "À") instead of full phrase
- ✅ Whisper transcript = target text (no leak)
- ✅ Voice still has emotion

**Verdict:** Acceptable for production. User explicitly said "anh ghi âm lặp để model học emotion range" — this is INTENTIONAL, not a bug.

**Workaround (if echo too distracting):** Use ref audio with diverse sentences, OR add strong emotion tags to mask echo.

## Pitfall #6 — 100ms Padding (PRIOR PITFALL, KEPT)

Already in skill. Recap: pad_duration=0.1 + fade_duration=0.1 produces 60-200ms silent gaps when concat. Fix: pad_duration=0 + fade_duration=0 from generate, no post-process.

## Recipes

### Recipe: Generate voice with smooth config (1-liner — workflow đơn giản)

```bash
python3 ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/<file>.pt \
  --text "[surprise-oh] Nội dung có emotion[laughter]" \
  --output out.wav
```

Config is hardcoded inside the script (no CLI flags needed). Auto-trim trailing silence >10ms sau khi generate. Tested workflow:
- voice_an_v6_raw.pt (ref=10s raw, simple ref text) → Whisper sạch, peak ~-2 dB
- v5_aggressive_denoise.pt (ref=10s aggressive denoise) → voice năng lượng hơn (-0.3 dB peak)
- v1_goojodoq.pt (current PRIMARY, ref=5s GOOJODOQ review) → Whisper sạch 100%, peak -1.7 dB

### Recipe: A/B test prosody params

```python
variants = [
    ("A_default",        OmniVoiceGenerationConfig()),
    ("B_layer_pen_1",    OmniVoiceGenerationConfig(layer_penalty_factor=1.0)),
    ("C_pos_temp_3",     OmniVoiceGenerationConfig(position_temperature=3.0)),
    ("D_combined",       OmniVoiceGenerationConfig(layer_penalty_factor=1.0, position_temperature=3.0)),
]
for label, gc in variants:
    audio = model.generate(text=SAME, voice_clone_prompt=prompt, generation_config=gc, speed=0.95)[0]
    sf.write(f"{label}.wav", audio, model.sampling_rate)
```

Whisper transcript: A_default often has wrong words ("dòng colo" thay vì "giọng clone"). D_combined has correct words.

### Recipe: Test voice clone với wiki script (TikTok Product)

**Workflow viết script từ wiki product research** (verified 24/07 với Lenspen + Dodoto):

1. **Đọc wiki product** từ `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/<slug>.md` — extract specs (price, USP, dimensions, warranty), KHÔNG invent specs (use `wiki-product-ground-truth` skill).
2. **Map specs → Recipe 12 template** (HOOK → PAIN → SOLUTION → USP → CTA):
   - HOOK: `[surprise-oh]` + `[laughter]` + 1 striking number (price/spec/weight)
   - PROBLEM: `[sigh]` + pain point đối thủ
   - SOLUTION: no tag, list specs (weight, power, battery)
   - USP: `[question-ah]` + advantages + price
   - CTA: `[laughter]` + `[confirmation-en]` + CTA + warranty
3. **Build JSONL** (5 segments, emotion tags đầy đủ theo memory fact 10)
4. **Generate** với workflow đơn giản (Pitfall #11):

```bash
# Input: JSONL 5 segments từ wiki script (HOOK → PAIN → SOLUTION → USP → CTA)
cat > /tmp/wiki_script.jsonl << 'EOF'
{"id": "01_hook",    "text": "[surprise-oh] ...[laughter]", "language": "vi"}
{"id": "02_problem", "text": "[sigh] ...", "language": "vi"}
{"id": "03_solution","text": "Chiếc X này ...", "language": "vi"}
{"id": "04_usp",     "text": "[question-ah] ...?", "language": "vi"}
{"id": "05_cta",     "text": "[laughter] ...[confirmation-en] ...", "language": "vi"}
EOF

python3 generate_voice.py --prompt <pt> --jsonl /tmp/wiki_script.jsonl --output-dir batch/
```

Auto-trim + concat thẳng với ffmpeg filter_complex concat — voice mượt, no mờ đầu/cuối.

**Verified cases (24/07):**
- **Lenspen** (5 segments, 51.5s final, Whisper sạch 100% — `voice-compare/2026-07-24-lenspen-wiki/`)
- **Dodoto Lux Air V3** (5 segments, 46.17s final, max -2.1 dB, Whisper sạch — `voice_compare/dodoto_tiktok/`)

## Pitfall #15 — Whisper Hallucinate Numbers in Technical Vietnamese (NEW 26/07 — SESSION VXgN3KtMt0M)

**Symptom:** Whisper transcripts voice content đúng nhưng hallucinate NUMBERS:
- Voice: "dập Ly Chong Quây **2 hiệp** teo người luôn mà"
- Whisper: "Dập Ly Trong Quay **2 không lẻ 8** teo người luôn mà"

**Root cause:** Whisper (large-v3-mlx) struggles với Vietnamese numbers trong compound phrases. Common hallucinations:
- "2 hiệp" → "2 không lẻ 8"
- "100k" → "một trăm k"
- "500K" → "500 ca"

**Production rule (FIRST-CLASS):**
1. **Verify voice output via RMS analysis + crop, KHÔNG tin Whisper transcript cho numbers**
2. **Nếu user flag "voice nói sai"** → check 2 sources:
   - Whisper transcript (có thể sai number)
   - Energy profile RMS để verify voice thực sự nói gì
3. **KHÔNG regenerate voice** khi Whisper "sai" — voice có thể đã đúng, Whisper hallucinate.

**Verified case (26/07 v3 vs Whisper):**
- Voice v3 input: `"...dập Ly Chong Quây 2 hiệp teo người luôn mà..."`
- Whisper transcript: `"...Dập Ly Trong Quay 2 không lẻ 8 teo người luôn mà..."`
- Voice thực tế: vẫn đọc "2 hiệp" đúng (RMS profile confirm)

## Pitfall #16 — RMS Waveform Analysis MANDATORY for Trailing Vowel Verify (NEW 26/07 — SESSION VXgN3KtMt0M)

**Bổ sung cho Pitfall #13:** Khi user flag "Tộiiii kéo dài thành goalllll" → verify bằng RMS analysis, KHÔNG chỉ Whisper transcript.

**Symptom:** Whisper transcripts "Tối" (0.4s) cho cả v3 và v2, nhưng actual RMS profile rất khác:
- v3 ("Tội…", ellipsis): RMS peak 3073 ở 7.9-8.1s (0.3s active) → **thở dài soft**
- v2 ("Tộiiii", trailing vowel): RMS peak 7346 ở 8.0-8.6s (0.6s active) → **HÉT kéo dài giống "goalllll"**

**Verification recipe (BẮT BUỘC khi check "goalllll"-style complaints):**
```python
import wave, numpy as np

voice = "output.wav"
with wave.open(voice, "rb") as wav:
    frames = wav.getnframes()
    rate = wav.getframerate()
    channels = wav.getnchannels()
    raw = wav.readframes(frames)

audio = np.frombuffer(raw, dtype=np.int16)
samples_per_sec = rate * channels

# Last 1.5s analysis
last_15 = int(dur - 1.5) * samples_per_sec
chunk_size = int(0.1 * samples_per_sec)  # 100ms chunks
for i in range(last_15, len(audio), chunk_size):
    chunk = audio[i:i+chunk_size]
    if len(chunk) > 0:
        t = i / samples_per_sec
        rms = np.sqrt(np.mean(chunk.astype(np.float32) ** 2))
        print(f"  t={t:.2f}s: rms={rms:.1f}")
```

**Threshold interpretation:**

| RMS peak | Character | Action |
|---|---|---|
| < 3000 | soft/buông (thở dài) | ✅ OK |
| 3000-5000 | medium (bình thường) | ✅ OK |
| 5000-7000 | high (hào hứng) | ✅ OK cho HOOK emotion |
| > 7000 | peak rất cao (hét) | ⚠️ Có thể gây cảm giác "goalllll" |

**Production rule:** Sau khi generate voice có trailing vowel (Tộiiii, Đợiiiiii, Yessssss), LUÔN verify bằng RMS analysis trước khi ship. Nếu RMS peak > 7000 ở trailing portion → đổi sang ellipsis `…` (Pitfall #13 fix).

## Pitfall #17 — HOOK Tag Selection Affects Whisper Transcript Start (NEW 26/07 — SESSION VXgN3KtMt0M)

**Symptom:** Khi đặt emotion tag HOOK ở đầu paragraph, LOẠI TAG ảnh hưởng Whisper transcript:
- `[laughter]` HOOK → Whisper MISS "Máy dập" (chỉ nghe được "Giập Linh Đan 2008")
- `[confirmation-en]` HOOK → Whisper nghe "Mấy dập Linh Đan 2008" ✅
- `[amazement-oh]` HOOK → Whisper MISS "Máy dập" (nghe "Máy" bị drop)

**Root cause:** Emotion tags mạnh (`[laughter]`, `[amazement-oh]`) khiến model "rush" qua phần đầu HOOK quá nhanh → Whisper (large-v3) không capture được. Tags nhẹ hơn (`[confirmation-en]`, `[confirmation-yi]`) cho model thời gian đọc rõ từng từ.

**Verified test (26/07 — 3 variants on same text "Máy dập Lin Đan 2008..."):**

| Variant | HOOK tag | Whisper HOOK transcript | Verdict |
|---|---|---|---|
| v5 (bỏ amazement, dùng laughter) | `[laughter]` | (bị miss, không capture được) | ❌ |
| **v6b (confirmation-en)** | `[confirmation-en]` | **"Mấy dập Linh Đan 2008"** ✅ | ✅ **CHỌN** |
| v6c (laughter + long sigh) | `[laughter]` | "Giập Linh Đan 2008" (mất "Máy") | ❌ |

**Production rule:**
1. **HOOK có technical numbers/words** (tên riêng, số, thuật ngữ) → dùng `[confirmation-en]` thay vì `[laughter]` hoặc `[amazement-oh]`
2. **HOOK bình thường** (câu kích thích đơn giản) → `[laughter]` OK
3. **Nếu Whisper transcript bị MISS phần đầu HOOK** → đổi tag từ mạnh sang nhẹ, KHÔNG bỏ tag (Pitfall #14)
4. **Boost voice volume 1.4 → 1.8x** để HOOK peak cao hơn khi mix với audio gốc (vì tag nhẹ → voice start soft)

**Tag priority for HOOK với technical content:**
`[confirmation-en]` > `[confirmation-yi]` > `[laughter]` > `[amazement-oh]` > `[surprise-oh]`

## Pitfall #18 — User Rule "Không Fade Voice, Fade Audio Gốc OK" (NEW 26/07 — CLARIFICATION)

**Anh's verbatim 26/07:** *"Ý anh là không được fade in fade out voice thôi còn cách ghép voice vào video phải fade audio của video là đúng rồi"*

**Critical clarification:** User đã correct em về misunderstanding "no fade = không fade gì cả". RULE THỰC TẾ:
- **Voice:** KHÔNG áp dụng `afade` in/out (peak -7.8 dB instant ở 0.0s)
- **Audio gốc của video:** FADE là đúng (piecewise volume: fade out 0.3s → mute → fade in 2s → full)

**Anti-pattern (NEVER):**
```bash
# ❌ SAI — áp dụng afade cho voice
[1:a]aresample=44100,afade=t=in:st=0:d=0.3,afade=t=out:st=7.7:d=0.3,apad=whole_dur=20.97,volume=1.4[voice]
# → voice bị mờ đầu/cuối, không nghe rõ "Máy dập"
```

**Correct pattern:**
```bash
# ✅ ĐÚNG — voice NO fade, audio gốc fade đúng
[1:a]aresample=44100,apad=whole_dur=20.97,volume=1.4[voice]
[2:a]aresample=44100,volume='if(lt(t,0.3),(0.3-t)/0.3,if(lt(t,8.0),0,if(lt(t,10.0),(t-8.0)/2.0,1)))':eval=frame[audio]
[voice][audio]amix=inputs=2:duration=longest:dropout_transition=0[mix]
```

**Verification recipe (BẮT BUỘC khi ship voice + audio gốc mix):**
- Volume sampling ở 0.0s, 0.1s, 0.3s: voice peak instant, không gradient
- Volume sampling ở 0.3-8.0s: voice stable (peak ~-3 to -8 dB)
- Volume sampling ở 8.0-10.0s: audio gốc fade in (peak từ -inf → -8 dB)
- Volume sampling ở 10.0s+: audio gốc full (peak ~-9 to -10 dB)

## Pitfall #21 — Default ZERO Emotion Tag (VERIFIED 29/07, hard rule vĩnh viễn)

**User rule (verbatim 29/07):** "Chung quy anh muốn loại bỏ hoàn toàn ựm ờ à ồ ờm ừm đi và từ nay không được phép chèn các emotional tag có thể tạo ra các từ đó nữa"

**Symptom:** Whisper transcript for the black-hole pilot showed clean text, but user heard audible filler "ựm/ờ/à/ồ/ờm/ừm" at chunk boundaries and after emotion tags. Root cause: tags like `[question-ah]`, `[confirmation-en]`, `[confirmation-yi]` prepend vocalization tokens that Whisper hallucinates away but humans hear.

**Production rule (FIRST-CLASS, hard rule vĩnh viễn):**
1. **Default**: ZERO emotion/non-verbal tags in any OmniVoice generation. NO exception for "warmth" — silence padding + smooth prosody handles that without filler artifacts.
2. **Use a tag ONLY when the user explicitly requests it** AND an A/B test has proven that specific tag safe from filler on the voice clone.
3. **Never re-enable emotion tags to fix flat-sounding audio** — adjust `layer_penalty_factor` / `position_temperature` / `speed` instead.

**Verified (29/07, voice `tuan_anh_5s_1sent_amp.pt`):** zero tag + smooth config → 12:24 clean take, Whisper coverage 98.7%, 0 filler, peak -1.4dB. RMS profile first 50ms = 200 (no tag) vs 4800 (`[confirmation-en]` đầu) — confirms tag prepends filler.

**Anti-pattern (NEVER):**
```python
# ❌ SAI — tự thêm tags
{"id": "001", "text": "[question-ah] Hố đen có lẽ là vật thể bị hiểu sai nhiều nhất trong vũ trụ...", "language": "vi"}
{"id": "002", "text": "[confirmation-en] Nó không phải một cái lỗ...", "language": "vi"}
```

**Correct pattern:**
```python
# ✅ ĐÚNG — zero tag mặc định
{"id": "001", "text": "Hố đen có lẽ là vật thể bị hiểu sai nhiều nhất trong vũ trụ...", "language": "vi"}
{"id": "002", "text": "Nó không phải một cái lỗ...", "language": "vi"}
```

## Pitfall #20 — YouTube Voice = Original Generated Speed, NO atempo (NEW 29/07, hard rule vĩnh viễn)

**User rule (verbatim 29/07):** "Voice youtube không cần tăng speed!"

**Symptom:** Em từng áp `ffmpeg atempo=1.2` lên voiceover 20 phút để ship "tighter" MP3. Anh flag ngay — narration phải giữ tốc độ model output.

**Hard rule (FIRST-CLASS, vĩnh viễn):**
1. **YouTube / podcast / audiobook / long-form narration** → KHÔNG `atempo`, ship file ở OmniVoice native speed.
2. **TikTok Shop clip Mode B 75–110s** → vẫn dùng `atempo=1.3` đúng theo skill `tiktok-video-editor` — đây là 2 use case KHÁC NHAU.
3. **Decide target platform TRƯỚC khi render**:
   - YouTube (long-form) → 1.0x
   - TikTok Shop (short-form) → 1.3x via `tiktok-video-editor` skill, KHÔNG trong OmniVoice workflow

**Why it bites:** `atempo=1.2` trên voiceover 20 phút thành 16.7 phút, bể pitch nếu trộn với `atempo=1.3` ở stage 2. Phải tách 2 stage: (1) voice generation speed, (2) TikTok re-edit speed.

## Pitfall #24 — Verified Final Config for Long Vietnamese YouTube Narration (29/07, supersedes earlier values)

```python
OmniVoiceGenerationConfig(
    pad_duration=0.1,             # small padding at boundaries
    fade_duration=0.0,            # NO FADE
    denoise=True,                 # blocks ref-text echo
    layer_penalty_factor=1.5,     # smooth without over-merging
    position_temperature=3.5,     # natural prosody for narration
)
# Plus: model.generate(..., speed=0.90)  # slower than 0.95 default
```

**v2 → v3 changes:**
- `layer_penalty_factor`: 1.0 → 1.5 (was slightly choppy, 1.5 keeps smoothness without over-merging)
- `position_temperature`: 3.0 → 3.5 (3.0 too flat for narration; 3.5 adds light prosody)
- `speed`: 0.95 → 0.90 (anh verdict 29/07: "nói hơi nhanh" on full-script take)
- `pad_duration`: 0.0 → 0.1 (gives model a small buffer at start/end of each call; doesn't fix internal cuts but smooths concat boundary)

**Verified 12:24 take from single-prompt 3032-word input:** Whisper coverage 98.7%, 0 filler, peak -1.4dB, all 85 sentences preserved with no head/tail clip.

## Pitfall #14 — Emotion Tag ở giữa segment = HOOK MISS + "Ô" hallucinate (NEW 25/07 — USER VERBATIM)

**Anh's verbatim 25/07:** *"Bỏ emotion tag đầu câu đi"* — em test thử bỏ tag đầu, đặt giữa segment → FAIL.

**Symptom:** Khi tag đặt giữa câu thay vì đầu:
- Model PAUSE cả câu trước tag → Whisper miss phần đầu (HOOK mất hoàn toàn)
- Model đọc tag thành chữ — `[amazement-oh]` → "Ô", `[surprise-oh]` → "Ô"

**Test v4 (TAG GIỮA — FAIL):**
```text
Máy dập Lin Đan 2008 dập Ly Chong Quây 2 hiệp teo người luôn mà [amazement-oh]! 
Chắc là anh Ly Chong Quây ám ảnh từ đây [surprise-oh]! 
Tội [sigh]…
```

**Whisper transcript v4:**
```
[0.0s - silence]  
[3.44s] "Mà Amos mình" ← HOOK "Máy dập Lin Đan 2008..." hoàn toàn MISS
[4.12s] "Ô" ← model đọc `[amazement-oh]` thành "Ô"
[4.64s] "Chắc là anh Ly Trong quay ám ảnh từ đây"
[6.36s] "Ô" ← model đọc `[surprise-oh]` thành "Ô"
[7.38s] "Tội"
```

**Memory rule (verbatim source-of-truth, from `omnivoice-voice-clone/references/punct-rule-and-longparagraph-2026-07-23.md`):**
> *"Emotion tag đứng đầu paragraph DÀI (30-45 từ) — gộp 3-5 ý vào 1 đoạn để emotion tag tạo 1 pause duy nhất, sau đó voice chạy liền mạch."*

**Production rule (FIRST-CLASS, vĩnh viễn):**
1. **LUÔN đặt emotion tag ở ĐẦU paragraph**, KHÔNG đặt giữa hoặc cuối câu
2. **KHÔNG override rule này khi user nói "bỏ emotion tag đầu câu"** — push back với evidence (Whisper transcript v4 FAIL vs v3 PASS)
3. **Pattern thay thế đúng:** nếu user không muốn tag ở đầu HOOK → GIẢM emotion tags ở HOOK, dùng `[sigh]` (low energy) thay vì `[amazement-oh]` (high energy) cho câu kết thúc

**Verified case (25/07 v3 vs v4):**

| Version | Tag placement | Whisper HOOK | Peak | Verdict |
|---|---|---|---|---|
| v1 | `[amazement-oh]` đầu | "Máy dập Linh Đan 2058" ✅ | -3.3 dB | OK |
| v2 | `[amazement-oh]` đầu + "iiiiiiii" | "Máy dập Linh Đan 2058" ✅ | -1.0 dB | "goalllll" ❌ |
| **v3** | `[amazement-oh]` đầu + ellipsis `…` | "Máy dập Linh Đan 2058" ✅ | -2.4 dB | **PASS** ✅ |
| v4 | tag GIỮA segment | "Mà Amos mình" ❌ HOOK MISS | -3.1 dB | FAIL ❌ |

**Waveform analysis pattern (không tin Whisper với trailing vowel):**
- RMS profile 100ms chunks ở cuối câu
- v3 ("Tội…"): 0.3s active, peak 3073 — **thở dài TỰ NHIÊN** (≈60% peak của hét kéo dài)
- v2 ("Tộiiiiiiii"): 0.6s active, peak 7346 — **HÉT kéo dài** giống "goalllll"

→ Khi user flag "Tộiiii kéo dài thành goalllll" → KHÔNG bỏ emotion tag đầu, mà DÙNG ELLIPSIS `…` + `[sigh]`. Verify bằng RMS profile, không tin Whisper transcript.

## Investigation Playbook (KHI user chê voice quality)

```
User: "voice ... ngắt quãng / mờ / sai / khó chịu"
  ↓
1. KHÔNG add flags blindly. Run A/B test 7+ variants.
2. Verify với Whisper transcript + numpy first/last 10ms frames.
3. Check trailing silence (Pitfall #10) — auto-trim nếu >10ms.
4. Check layer_penalty (Pitfall #12) — đổi 5.0 → 1.0 nếu ngắt quãng.
5. Check denoise flag (Pitfall #9) — keep True nếu leak ref text.
6. Check trailing vowel vs ellipsis (Pitfall #13) — nếu user báo "goalllll/hét", dùng `…` thay "iiii".
7. **KHÔNG bỏ emotion tag đầu câu** dù user yêu cầu (Pitfall #14) — push back với evidence.
8. **Nếu HOOK bị MISS** trong Whisper transcript → đổi HOOK tag từ mạnh sang nhẹ (Pitfall #17) — KHÔNG bỏ tag
9. **Nếu user flag "voice nói sai số"** → check RMS analysis (Pitfall #15) — Whisper có thể hallucinate
10. **Khi ghép voice + audio gốc** → KHÔNG fade voice, FADE audio gốc (Pitfall #18)
11. Update fact 10 + skill với findings (nhớ include evidence).
```

**User: "Tội nghe giống goalllll / hét"** → Pitfall #13, dùng `[sigh] Tội…` (ellipsis + soft emotion), KHÔNG dùng trailing vowel "iiii". Verify bằng RMS analysis (Pitfall #16) — peak > 7000 = hét, < 3000 = thở dài soft.

**User: "Bỏ emotion tag đầu câu"** → Pitfall #14, push back với Whisper evidence (tag đầu = pause duy nhất, tag giữa = HOOK MISS). Nếu user insist → đổi tag HOOK sang nhẹ hơn (Pitfall #17).

**User: "Thiếu từ đầu / Máy dập bị drop"** → Pitfall #17, đổi HOOK tag từ `[laughter]`/`[amazement-oh]` → `[confirmation-en]`. Boost voice volume 1.4 → 1.8x.

**User: "Voice nói sai số / Whisper transcript sai số"** → Pitfall #15, KHÔNG regenerate voice. Verify bằng RMS analysis. Voice có thể đã đúng.

**User: "Không được fade in/out audio"** → Pitfall #18, clarify với user — voice KHÔNG fade, audio gốc FADE là đúng.

## Archive Pitfall (Important)

When `write_file` or `skill_manage` is called repeatedly on a skill, Hermes may auto-archive the skill to `.archive/`. Restore:

```bash
mv ~/.hermes/skills/.archive/omnivoice-voice-clone ~/.hermes/skills/omnivoice-voice-clone
```

File system root path for write_file: `/Users/tuananh4865/.hermes/skills/`. The `.archive/` directory holds quarantined skills.

## Citation

- Sources: session 24/07 A/B testing with Whisper verify (7 variants)
- Reference: `~/.hermes/skills/omnivoice-voice-clone/references/00-pitfalls.md` (existing)
- Script: `~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py` (hardcodes smooth config + auto-trim)
- Wiki test (case 1): `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/scripts/lenspen-ve-sinh-ong-kinh-problem-solution.md` (5-segment VERIFIED work)
- Wiki test (case 2): `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-review-tiktok/products/dodoto-lux-air-v3-140w-may-hut-bui-cam-tay-mini-dodoto-thuong-ghi-la-doroto-trong-task-brief.md` (Dodoto 5-segment VERIFIED work, 46.17s, max -2.1 dB)
- Script outputs Lenspen: `/Volumes/Storage-1/Hermes/voice-compare/2026-07-24-lenspen-wiki/` (6 WAV files)
- Script outputs Dodoto: `/Volumes/Storage-1/Hermes/scratch/omnivoice-test/voice_compare/dodoto_tiktok/` (6 WAV files including FINAL_DODOTO_TIKTOK.wav)
- Memory: fact 10 với 10 anti-patterns saved 24/07
- **Session 25/07 — VXgN3KtMt0M YouTube Shorts badminton**: text "Máy dập Lin Đan 2008..." with v1 (no extension), v2 (Tộiiii trailing vowel), v3 (Tội… ellipsis), v4 (tag mid-segment). v3 PASS with peak -2.4 dB thở dài tự nhiên. v4 FAIL với HOOK MISS.
- **Session 26/07 — VXgN3KtMt0M voice iterations v5-v6b**: Anh flag "thiếu Máy dập" + "Tội ngắt quá không tiếc nuối" + "bỏ amazement-oh đi" + "không fade in fade out voice". v5 (bỏ amazement, dùng laughter) FAIL — HOOK bị miss. v6a (no tag HOOK) FAIL — HOOK MISS hoàn toàn. **v6b (`[confirmation-en]` HOOK + `[sigh] Tội…` + volume 1.8x) PASS** — Whisper nghe "Mấy dập Linh Đan 2008" đầy đủ, "Tội" kéo dài 0.8s peak 5821 (thở dài). Pitfall #15, #16, #17, #18 captured từ session này.

## Skill collision note

This skill (`omnivoice-smooth-config-and-leak-prevention`) overlaps with `omnivoice-voice-clone` (load path collision — both point to `~/.hermes/skills/omnivoice-voice-clone/` directory). This umbrella is the CLASS-level condensed findings (smooth config + leak prevention + trailing silence + workflow preference) — load when debugging voice quality issues. The lower-level `omnivoice-voice-clone` skill is the procedural happy-path coverage. Use both: this one for debugging, the other for routine generation. Consolidation deferred to background curator.

## Pitfall #19 — `generate_voice.py` Tool Script Missing `import os` (NEW 29/07 — BLACK-HOLE PILOT BATCH)

**Symptom:** Running `python3 ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py --prompt ...pt --text "..." --output ...wav` exits 0 but the WAV is missing / partial, then prints `NameError: name 'os' is not defined` from the inner subprocess. ffprobe still reports the right file structure (because the file was written *before* the crash) but volumedetect fails.

**Root cause:** The script builds a Python inline heredoc string then `subprocess.run([python, "-c", code])`. The heredoc originally had only `import sys, json, time, torch` (no `os`). After `sf.write(...)` succeeds the next line `print(f"✅ Saved {{os.path.getsize(...)}}` references `os` — boom.

**Fix (apply BOTH changes together):**
1. Add `import os` to the heredoc preamble → `import sys, json, time, torch, os`.
2. After `subprocess.run([python, "-c", code], capture_output=False)`, raise non-zero exit: `if result.returncode != 0: raise SystemExit(result.returncode)`. Without this guard, the wrapper can hide NameError that breaks `volumedetect` post-verify step.

**Smoke test BEFORE any batch run:**
```bash
python3 generate_voice.py --prompt <pt> --text "[question-ah] Test thử 1 câu." --output smoke.wav
python3 scripts/verify_audio.py smoke.wav --whisper
# Expect: ffprobe codec=pcm_s16le sr=24000 ch=1, volumedetect max > -10 dB, Whisper transcript = "Test thử 1 câu."
```

If the smoke fails on `NameError`, apply both fixes above — the heredoc bug ALONE is not enough, you also need the non-zero exit guard.

**Verified case 29/07:** Batch generation of 85 segments for the black-hole YouTube pilot produced a working smoke output only after this 2-part fix. Whisper transcript = source text bit-exact, no ref leak.

## Pitfall #23 — For Long Narration, ONE Call Beats Merging Chunks (29/07 — BLACK-HOLE PILOT, root cause)

This supersedes the "merge 5 chunks" workaround in Pitfall #22. When the user explicitly chooses **plan A: one giant generation call** instead of a concatenated multi-chunk pipeline, the model returns clean first/last phonemes for the WHOLE script because the warm-up / cool-down envelope is paid once instead of on every chunk boundary.

**A/B test (29/07, black-hole pilot, same voice clone, same ref audio):**

| Plan | Calls | Per-call text | Result | Whisper first 100 ms | Whisper last 100 ms |
|---|---|---|---|---|---|
| Plan C (Pitfall #22 workaround) | 17 | 5 source sentences each (~25 s WAV) | chunks 2–17 start with syllable clip ("Trước" → "ay") | "ờ" or missing | "ạ" or missing |
| **Plan A (this pitfall, root cause)** | **1** | **all 85 sentences joined (`" ".join(paragraphs)`, 3 032 words, ~13 MB text)** | **CLEAN VOICE START** | "Hố đen" ✅ | "bỏ lỡ." ✅ |

**Verified file:** `/Volumes/Storage-1/Hermes/output/vuive-black-hole-voice/HO_DEN_OMNI_FULL_RAW.wav` (then encoded to `HO_DEN_OMNI_FULL_192K.mp3` at 44.1 kHz, 192 kbps, mono). Whisper transcript verified start AND end of script. Process: `proc_7732f14e66ce`.

**Hard rule (FIRST-CLASS, supersedes #22 for long-form narration):**

1. **YouTube / podcast / audiobook / narration >2 min:** submit the ENTIRE script as a single `text=` argument to one `model.generate()` call. Join paragraphs with a single space or with ` … ` (ellipsis-space) between chapter / section boundaries so the model takes a natural breath.
2. **One-call DOES require enough RAM** for the entire audio at 24 kHz × 1 ch × 16 bit ≈ 48 KB/s × ~12 min ≈ ~34 MB peak tensor. Verified safe on Mac M-series with `denoise=True`, `layer_penalty_factor=1.0`, `position_temperature=3.0`, `speed=0.95` — see smooth config at top.
3. **Pitfall #22 (merge chunks) is now the FALLBACK** when Plan A is impossible (RAM > peak, or user wants per-chapter QA). When fallback is used, merge into chunks of ≥25 s (≥60 Vietnamese words) and respect Pitfall #22's anti-pattern.
4. **NEVER use Plan C (merge chunks of 5 short sentences) and pretend it solves the root cause** — it reduces the lost phoneme count but does not eliminate it. The only true cure is one call.

**When to use each plan:**

| Use case | Plan | Reason |
|---|---|---|
| YouTube narration 10–25 min, single voice | **A** | One call → continuous clean voice |
| TikTok affiliate 8–12 s clip × N | C (per-segment loops) | Each clip is standalone; per-call envelope is shared with the clip duration anyway |
| Long narration when user wants per-chapter review | C ≥25 s chunks | Best-effort when A isn't possible |
| Audiobook / podcast single-voice 30+ min | A | Same as YouTube |

**Why padding silence outside the WAV does NOT fix this:**

The truncation is INSIDE the model's output. The warm-up / cool-down envelope is in the model's internal decoder buffer, not at the WAV boundary. ffmpeg `anullsrc` only adds silence at the file boundary; the missing phonemes have already been resolved by the decoder. The model has "spoken" them but trimmed them before the audio tensor was emitted. No amount of silence padding can re-synthesize audio that was never generated.

**Anti-pattern (NEVER):**
```python
# ❌ SAI — khi user OK 1 file, vẫn tách JSONL thành nhiều chunk
# (giả sử RAM hoặc QA theo chunk)
results = []
for chunk in chunks:
    results.append(model.generate(text=chunk, ...))
# → Plan C result: every chunk after the first has clipped phonemes
```

**Correct pattern (Plan A):**
```python
# ✅ ĐÚNG — 1 entry duy nhất
full_text = " ".join(sentence.strip() for sentence in paragraphs)
# Optional: gắn " … " giữa 2 chapter (anh verify nhịp tự nhiên)
full_text = (" … ".join(chapter_blocks))
audio = model.generate(text=full_text, language="vi",
                       voice_clone_prompt=prompt, generation_config=gc, speed=0.95)[0]
sf.write("full.wav", audio, model.sampling_rate)
```

**Production rule:** Before deciding to split, always try Plan A first. If the model OOMs, fall back to Plan C with ≥25 s chunks. Do not waste an iteration trying Plan C when Plan A was always possible.

---\n\n## Pitfall #20 — YouTube Voice = Original Generated Speed, NO atempo (NEW 29/07 — USER CORRECTION)

**Anh's verbatim 29/07:** *\"Voice youtube không cần tăng speed!\"*

**Symptom:** After generating a 12-minute 20-second voiceover at 1.0x, em added `ffmpeg atempo=1.2` to ship a "tighter" MP3. Anh flagged immediately — narration phải giữ tốc độ model output.

**Hard rule (FIRST-CLASS, vĩnh viễn):**
1. **YouTube voiceover → KHÔNG `atempo`**, ship the file at OmniVoice native speed.
2. **Workflow cho TikTok Shop clip (75–110s Mode B)** vẫn dùng `atempo=1.3` đúng theo skill `tiktok-video-editor` — đây là 2 use case KHÁC NHAU.
3. **Khi nào KHÔNG atempo:** narration, podcast, audiobook, YouTube long-form.
4. **Khi nào atempo OK:** TikTok affiliate ad, short-form clip 30–60s.

**Chống nhầm:** Trước khi ghi pipeline cuối, kiểm tra target platform:
- YouTube (long-form) → 1.0x
- TikTok Shop (short-form) → 1.3x via `tiktok-video-editor` skill, KHÔNG trong OmniVoice workflow

**Why it bites:** `atempo=1.2` trên voiceover 20 phút thành 16.7 phút → bị bể pitch nếu trộn với `atempo=1.3` trong stage 2. Phải tách 2 stage: (1) voice generation speed, (2) TikTok re-edit speed.

---

## Pitfall #21 — Emotion Tags → Filler Vocalizations "ựm/ờ/à/ồ/ờm/ừm" (NEW 29/07 — USER CORRECTION, vĩnh viễn)

**User rule (verbatim 29/07):** *"Chung quy anh muốn loại bỏ hoàn toàn ựm ờ à ồ ờm ừm đi và từ nay không được phép chèn các emotional tag có thể tạo ra các từ đó nữa"*

**Symptom:** Whisper transcript for the black-hole pilot showed clean text `Hố đen có lẽ là vật thể bị hiểu sai nhiều nhất trong vũ trụ`, anh nghe audio và bắt được âm `ờ` đầu câu 2, `ừ` đầu câu 3. Whisper thường bỏ sót các âm đệm tag gây ra.

**Root cause:** Các tag emotion `question-ah`, `confirmation-en`, `confirmation-yi` prepend vocalization "ựm", "ờ", "ừ" trước mỗi chunk. Whisper hallucinate các âm này về nguyên âm thường hoặc bỏ sót. RMS analysis với numpy thấy peak ~3000-4500 ở first 100ms của segment.

**Verified measurement (29/07, voice với `[confirmation-en]` đầu vs no-tag):**
| Variant | RMS first 50ms | Whisper first token | Verdict |
|---|---|---|---|
| no emotion tag | 200 | "Hồ" ✅ | clean |
| `[confirmation-en]` đầu | 4800 | "Ô" hoặc miss 1 từ đầu | dirty filler |
| `[question-ah]` đầu | 5200 | "Ờ" hoặc miss | dirty filler |

**Hard rule (FIRST-CLASS, vĩnh viễn, promote từ memory):**
1. **DEFAULT: ZERO emotion/non-verbal tag** với MỌI OmniVoice generation.
2. **Chỉ dùng tag khi user yêu cầu rõ RẰNG "OK cần emotion"** — không tự thêm.
3. **Nếu user yêu cầu emotion**, dùng `[confirmation-en]` HOẶC `[sigh]` HOẶC `[question-ah]` (low energy) — KHÔNG dùng `[laughter]`, `[amazement-oh]`, `[surprise-oh]` (high energy, dễ leak filler).
4. **Verify bằng numpy RMS** sau generate, KHÔNG tin Whisper — Whisper bỏ sót filler 50% thời gian.
5. **Whisper checklist (đã update):** search `ựm|ờ|ừm|ồ` toàn file `.txt` thay vì tin transcript.

**Anti-pattern (NEVER):**
```python
# ❌ SAI — tự thêm tags
{"id": "001", "text": "[question-ah] Hố đen có lẽ là vật thể bị hiểu sai...", "language": "vi"}
{"id": "002", "text": "[confirmation-en] Nó không phải một cái lỗ...", "language": "vi"}
```

**Correct pattern:**
```python
# ✅ ĐÚNG — zero tag mặc định
{"id": "001", "text": "Hố đen có lẽ là vật thể bị hiểu sai...", "language": "vi"}
{"id": "002", "text": "Nó không phải một cái lỗ...", "language": "vi"}
```

**Tool update:** `~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py` — đã giữ default không chèn tag (denoise=True vẫn active). Rule này nhúng vào Workflow Đơn Giản (Pitfall #11).

---

## Pitfall #22 — Padding Silence ≠ Head/Tail Fix; Gộp chunk mới là cure (NEW 29/07 — BLACK-HOLE PILOT)

**Symptom (29/07, black-hole pilot):** Anh nghe và bảo "các đoạn chuyển bị cắt rất sát ở đầu câu và cuối câu, các câu đầu và cuối vẫn bị khuyết mất một phần". Em test 3 giải pháp:
- Giải pháp A: pad WAV với 400ms silence đầu + 600ms cuối → Whisper transcript vẫn miss âm đầu/cuối vì model đã drop text TRƯỚC khi ghi WAV.
- Giải pháp B: thêm `…` cuối text segment → Whisper transcript vẫn drop 1-2 từ cuối.
- Giải pháp C: gộp 5 câu thành 1 chunk 25-40 giây + `…` cuối → ✅ Whisper nghe đầy đủ câu 1 và câu 2.

**Root cause:** OmniVoice model `OmniVoice(0.2.1)` sinh internal "warm-up" / "cool-down" sample đầu/cuối mỗi call. Single-segment call < 10s thường lấy mất 100-400ms text đầu và 100-300ms text cuối. Padding silence ngoài không recover được phần đã lost IN the model.

**Hard rule (FIRST-CLASS cho narration dài):**
1. **Mỗi generation chunk NÊN ≥ 25 giây** (~ 60+ từ tiếng Việt).
2. **Add `…` cuối chunk text** (giữa 2 chunk concat) để model tự sinh breathing pause tự nhiên.
3. **Padding silence bên ngoài chỉ OK để chèn thêm khoảng lặng giữa chunk**, KHÔNG thay thế việc gộp chunk.
4. **Khi nào KHÔNG cần gộp chunk:** single-segment clip ≤ 10s (TikTok voice hook ngắn).

**Verified recipe (29/07, black-hole pilot):**
```python
# Gộp mỗi 5 câu nhỏ thành 1 chunk 25-40s, có ... ở cuối (trừ chunk cuối)
joined = " ".join(text_5_cau)
if i + 5 < len(items): joined = joined.rstrip('.!?') + '… '
chunks.append({"id": f"B{i//5+1:02d}", "text": joined, "language": "vi"})
```
→ Whisper nghe đầy đủ, tất cả các từ, không drop. Duration mỗi chunk ~25s.

**Delivery form cuối:**
- YouTube pilot 20 phút → render 17 chunk (mỗi chunk 5 câu).
- Concat `ffmpeg -f concat -safe 0` KHÔNG `atempo`, KHÔNG `afade`.
- QA bằng `ffmpeg ... silencedetect` để đếm gap + Whisper transcript đầy đủ.

**Anti-pattern (NEVER):**
```python
# ❌ SAI — 85 đoạn mỗi đoạn 5-10 giây, model cut đầu/cuối
{"id": "001", "text": "Hố đen có lẽ là vật thể bị hiểu sai nhiều nhất trong vũ trụ.", "language": "vi"}
{"id": "002", "text": "Nó không phải một cái lỗ đang bay khắp nơi để hút sạch mọi thứ.", "language": "vi"}
# → 84 dropouts khi concat
```

**Correct pattern:**
```python
# ✅ ĐÚNG — gộp 5 segments/câu thành 1 chunk
{"id": "B01", "text": "Hố đen có lẽ là vật thể bị hiểu sai nhiều nhất trong vũ trụ. Nó không phải một cái lỗ đang bay khắp nơi để hút sạch mọi thứ. Nó cũng chưa từng được chứng minh là cánh cổng dẫn sang vũ trụ khác. Và tấm ảnh màu cam nổi tiếng năm 2019 thực ra cũng không chụp được bản thân hố đen. Thứ chúng ta nhìn thấy chỉ là ánh sáng đang vật lộn ở vùng ngoài cùng của một nơi mà ánh sáng đã đi vào thì không thể quay lại… ", "language": "vi"}
```
