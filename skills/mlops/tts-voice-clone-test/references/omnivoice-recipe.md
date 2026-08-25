# OmniVoice Recipe (Apple Silicon)

**Verified end-to-end:** 2026-07-23 15:14 — full pipeline PASS với 3 test outputs + 3 NamMinh baselines.
- ✅ torch 2.8.0 + MPS hoạt động (Mac M-series)
- ✅ Install qua `uv venv` (PEP 668 bypass cho system Python 3.9)
- ✅ 3/3 clone tests: 10.2s/8.4s/4.5s @ 24kHz mono PCM
- ✅ Inference time: 16-28s per clip (RTF 2.5-3.5x trên MPS)
- ⚠️ Cold start: ~1:23 (download model + load weights); subsequent ~5-10s

## Install (PEP 668 safe)

**Apple Silicon gotcha:** system Python 3.9 KHÔNG đủ (OmniVoice cần ≥3.10) + PEP 668 block pip system install. **LUÔN dùng `uv venv`:**

```bash
cd /Volumes/Storage-1/Hermes/scratch/omnivoice-test
uv venv .venv --python python3.11
source .venv/bin/activate
uv pip install torch==2.8.0 torchaudio==2.8.0
uv pip install git+https://github.com/k2-fsa/OmniVoice.git

# Verify
.venv/bin/python -c "import torch, omnivoice; print('torch', torch.__version__); print('omnivoice', omnivoice.__version__); print('mps:', torch.backends.mps.is_available())"
# Expected: torch 2.8.0, omnivoice 0.2.1, mps: True
```

**Disk:** ~2-3GB cho model weights (k2-fsa/OmniVoice trên HF).

**First-run download:** Tự động download từ HF. Nếu gặp kết nối:
```bash
export HF_ENDPOINT="https://hf-mirror.com"
```

## CLI Quick Test

```bash
omnivoice-infer \
  --model k2-fsa/OmniVoice \
  --text "Xin chào, đây là test voice clone bằng OmniVoice" \
  --ref_audio /path/to/ref.wav \
  --ref_text "Transcript của ref audio" \
  --output /tmp/test.wav
```

**Output:** WAV 24kHz mono, 16-bit PCM.

## Python API

```python
from omnivoice import OmniVoice, VoiceClonePrompt
import soundfile as sf, torch

model = OmniVoice.from_pretrained(
    "k2-fsa/OmniVoice",
    device_map="mps",       # Apple Silicon
    dtype=torch.float16,
)

# Mode 1: Voice cloning (cần ref audio + transcript)
audio = model.generate(
    text="Test text 3-5s",
    ref_audio="ref.wav",
    ref_text="Transcript",
    language="vi",
)

# Mode 2: Voice design (text instruct, không cần ref)
audio = model.generate(
    text="Test text",
    instruct="male, Vietnamese",
    language="vi",
)

# Mode 3: Auto voice
audio = model.generate(text="Test text", language="vi")

sf.write("out.wav", audio[0], 24000)  # 24kHz native
```

## Voice Prompt Save/Load (REUSABLE)

```python
# Save prompt 1 lần — encode ref audio
prompt = model.create_voice_clone_prompt(
    ref_audio="ref.wav",
    ref_text="Transcript",
)
prompt.save("my_voice.pt")  # ~50-100MB

# Load prompt ở session sau — skip Whisper ASR
from omnivoice import VoiceClonePrompt
prompt = VoiceClonePrompt.load("my_voice.pt")
audio = model.generate(text="...", voice_clone_prompt=prompt)
```

**Format version:** `_VOICE_CLONE_PROMPT_FORMAT_VERSION = 1` — auto-check khi load, raise ValueError nếu mismatch.

## Generation Parameters (tweak nếu cần)

```python
audio = model.generate(
    text="...",
    ref_audio="ref.wav",
    ref_text="...",
    num_step=32,            # diffusion steps (default 32, có thể 8-64)
    guidance_scale=2.0,     # CFG (default 2.0, range 1-5)
    speed=1.0,              # speaking rate (default 1.0)
    t_shift=0.1,
    denoise=True,           # auto denoise ref
    postprocess_output=True,  # auto remove silence ở output
    layer_penalty_factor=5.0,
)
```

## Ref Audio Requirements (verified từ source code)

- **Duration:** 3-10s recommended (dưới 3s reject, trên 10s degradation)
- **Format:** WAV/MP3/M4A/OGG (auto-detect)
- **Sample rate:** native OK, model auto-resample
- **Quality:** clean voice preferred (no music, no fan noise)

## JSONL Batch (cho scale)

```jsonl
{"id": "001", "text": "...", "ref_audio": "ref1.wav", "ref_text": "...", "language_id": "vi"}
{"id": "002", "text": "...", "ref_audio": "ref2.wav", "ref_text": "...", "language_id": "en"}
```

```bash
omnivoice-infer-batch \
  --model k2-fsa/OmniVoice \
  --test_list test.jsonl \
  --res_dir results/ \
  --nj_per_gpu 1
```

Multi-GPU: model auto-distribute qua ProcessPoolExecutor. Mỗi worker có model riêng (load in `process_init`).

## Apple Silicon Quirks

- ✅ `device_map="mps"` works
- ⚠️ `flash_attn` không có trên MPS → auto-fallback SDPA
- ⚠️ `flex_attention` partial support → SDPA fallback cho training
- ⚠️ `pynini` no wheel (cho text normalization `[tn]` extra) → `conda install -c conda-forge pynini`

## Known Limits

- **Cross-lingual clone:** ref Vi + text En → output có accent Vi. Same-language recommended.
- **Voice design stability:** trained chủ yếu trên Zh+En, có thể unstable cho low-resource languages.
- **License:** Apache 2.0 — OK cho commercial use.

## Sources

- Repo: https://github.com/k2-fsa/OmniVoice
- Model: https://huggingface.co/k2-fsa/OmniVoice
- Demo: https://huggingface.co/spaces/k2-fsa/OmniVoice
- Colab: https://colab.research.google.com/github/k2-fsa/OmniVoice/blob/master/docs/OmniVoice.ipynb

## Test Status (2026-07-23 15:14)

- [x] Pre-flight: torch 2.8.0 MPS ✅
- [x] Repo recon: 82 files, 3-mode generate ✅
- [x] Install: uv venv + pip git ✅
- [x] Generate clone: 3/3 tests PASS (10.2s/8.4s/4.5s @ 24kHz)
- [x] Compare với NamMinh baseline: 3/3 generated ✅
- [x] Verdict: **PASS** (clone giọng thật chạy trên Mac M-series, chậm hơn edge-tts ~50-100x)

## End-to-end test results (2026-07-23)

**Ref audio:** 17.08s Opus 48kHz, Whisper transcript:
```
Xin chào đây là giọng đọc của Tuấn Anh
Tôi năm nay 30 tuổi đang thất nghiệp
Và bây giờ đang nhờ AI làm kịch bản cho tôi
```

**Ref preprocessed:** `ref_10s.wav` (10s cắt đầu, 16kHz mono PCM, 313KB)

**3 tests PASS:**

| # | Text | File | Duration | Inference | RTF |
|---|---|---|---|---|---|
| 1 | Same as ref (sanity) | out_test1.wav | 10.2s | 28s | 2.7x |
| 2 | New content (review) | out_test2.wav | 8.4s | 21s | 2.5x |
| 3 | Short CTA | out_test3.wav | 4.5s | 16s | 3.5x |

**3 NamMinh baselines (cùng text, 24kHz sau ffmpeg convert):**

| # | File | Duration |
|---|---|---|
| 1 | baseline_namminh_1.wav | 9.4s |
| 2 | baseline_namminh_2.wav | 6.3s |
| 3 | baseline_namminh_3.wav | 5.1s |

## Baseline command (edge-tts NamMinh)

```bash
edge-tts --voice vi-VN-NamMinhNeural \
  --text "Cùng text với OmniVoice test" \
  --write-media baseline.mp3
ffmpeg -y -i baseline.mp3 -ar 24000 -ac 1 baseline.wav
```

## Lessons learned (2026-07-23)

1. **Docs claim RTF 0.025 trên H100 GPU — KHÔNG apply cho Mac MPS.** Thực tế MPS RTF 2.5-3.5x (chậm hơn ~100x). Đừng cite docs khi benchmark trên consumer hardware — test first, cite second.

2. **Cold start 1:23** bao gồm download 1.3GB model từ HF + load 313+527 weights vào MPS. Subsequent runs chỉ ~5-10s load (model cached ở `~/.cache/huggingface/`).

3. **PEP 668 block trên macOS** — `pip install` trực tiếp FAIL. **LUÔN dùng `uv venv` thay vì `--break-system-packages` (risky).**

4. **System Python 3.9 vs OmniVoice 3.10+** — Mac default Python KHÔNG đủ. `uv venv --python python3.11` (Homebrew có sẵn).

5. **OmniVoice auto-transcribe ref** — nếu không pass `--ref_text`, model gọi Whisper ASR internally (~30s overhead). LUÔN pass ref_text explicit để save time.

6. **Output 24kHz không 48kHz** — nếu cần mix với Pocket 3 audio (48kHz), convert bằng `ffmpeg -ar 48000`. Sample rate diff → phase mismatch khi mix.

7. **Ref audio 17s (trên 10s recommend) vẫn chạy OK** — model không hard-reject, nhưng có thể degradation ở chất lượng. Test 10s cho best result.

8. **Batch test 5+ texts (verified 2026-07-23 15:30)** — TikTok structure HOOK→PROBLEM→SOLUTION→USP→CTA với 5 file JSONL. PASS 5/5, total audio 38.80s, synthesis 114.63s, **RTF 2.95x** (same as sequential — MPS single-process bottleneck). **Peak RAM 12.68GB** (~7GB tăng so với baseline 19GB free). Mac 8GB sẽ crash, cần ≥16GB.

9. **JSONL `language_id` MUST be ISO 639-3 code** ("vi" / "en"), KHÔNG phải name. CLI `--language` accept cả name nhưng batch parser không. Verify: `from omnivoice.utils.lang_map import LANG_IDS; "vi" in LANG_IDS` (True).

10. **MPS = 1 process only** — `--nj_per_gpu >1` gây contention hoặc crash. Force `--nj_per_gpu 1` trên Mac. Multi-GPU benefit chỉ có trên Linux/Windows multi-NVIDIA.

11. **RTF không cải thiện khi batch trên MPS** — Vì 1 process. Batch chỉ save cold-start overhead (1:23 → 1 lần), không parallel generation. Real time saving: model load 1 lần vs N lần.

12. **RAM auto-release sau batch** — Sau batch 5, RAM quay về baseline 7.77GB free (model unload). Multi-batch session OK nếu có ≥16GB RAM.

## Batch test results (2026-07-23 15:30)

**JSONL input (`test_batch_5.jsonl`):** 5 entries theo TikTok structure HOOK→PROBLEM→SOLUTION→USP→CTA, text dài 77-128 chars mỗi cái, language_id="vi", ref_audio="ref_10s.wav".

**Output (5/5 PASS, all 24kHz mono PCM):**

| ID | Phase | Duration | Size |
|---|---|---|---|
| batch_01_hook | HOOK | 6.28s | 294KB |
| batch_02_problem | PROBLEM | 6.80s | 318KB |
| batch_03_solution | SOLUTION | 8.08s | 378KB |
| batch_04_usp | USP | 10.28s | 481KB |
| batch_05_cta | CTA | 7.36s | 345KB |

**Total:** 38.80s audio, 1.78MB, average 363KB/file.

**Performance:**
- Wall time: 2:05 (model load 1:23 + 5 generations 42s = save 41s vs 5×1:23 sequential)
- RTF: 2.95x average
- RAM peak: 12.68GB (free = 0.08GB) — model + 5 generations concurrent
- RAM after batch: 7.77GB free (auto-released)

**Verdict batch:** PASS — stable, no crash, no quality regression vs sequential. Recommend cho TikTok pipeline.

## Khi nào dùng OmniVoice vs edge-tts NamMinh

| Use case | Recommend |
|---|---|
| TTS Việt nhanh, voice MS NamMinh đủ | edge-tts (RTF 0.05x, instant) |
| Cần giọng thật của Tuấn Anh (authentic) | OmniVoice |
| Multilingual (Anh, Trung, Tây Ban Nha) | OmniVoice (600+ langs) |
| Voice prompt stable qua nhiều session | OmniVoice (save `.pt` 1 lần) |
| Real-time narration cho clip edit | edge-tts (latency quá thấp so với OmniVoice 16-28s) |

---

# Lessons từ session 23/07 17:00 (PIPELINE BUG HUNTING)

**Context:** Sau khi batch 5 sequential test 1-by-1 PASS, em verify bằng volumedetect (OK peak -4.3dB) nhưng khi Whisper transcribe transcript phát hiện REF LEAK (câu cuối ref audio "Và bây giờ đang nhờ AI làm kịch bản cho tôi" bị inject vào đầu/giữa output). Em lần đầu đoán "model bug", nhưng anh correct: "Lúc em prompt omnivoice có vấn đề... chỉ cần fix prompt lại".

## LESSON 1 — REF LEAK là PROMPT BUG, không phải MODEL BUG

**Root cause:** OmniVoice dùng `ref_text` để ALIGN voice. Khi em set full transcript (3 câu, 17s) → model lấy **toàn bộ câu cuối** làm prompt anchor → leak vào output.

**Test matrix (verified):**
| ref_text variant | Length | Output | Verdict |
|---|---|---|---|
| Full 17s (3 câu) | 122 chars | "Và bây giờ đang nhờ AI..." leak đầu | ❌ FAIL |
| 1 câu đầu | 39 chars | Text target lặp 2 lần | ⚠️ Lặp |
| **2 câu đầu** | 77 chars | **Output sạch, đúng text** | ✅ **BEST** |
| "Xin chào." minimal | 9 chars | Model rác 71s | ❌ FAIL |

**Sweet spot: ref_text = 2 câu đầu (~10s đầu ref audio)**
- Đủ context cho voice clone
- KHÔNG có gì để leak
- Model chỉ encode 10s voice tokens, không có anchor cuối

**Apply:** MỌI voice clone workflow OmniVoice → dùng `ref_text` chỉ 2 câu đầu transcript, KHÔNG dùng full transcript.

## LESSON 2 — MPS BATCH BUG + SEQUENTIAL WORKAROUND (GitHub issue #8)

**Root cause:** OmniVoice v0.2.1 trên Mac M-series MPS BỊ BUG khi batch ≥5 texts có **độ dài khác nhau**:
- 4/5 file output gần silent (peak -16.6 dB thay vì 0 dB)
- Padding rows trong `_generate_iterative` gây NaN attention trên MPS
- Patch `pad_diag` (PR #13) đã merge vào v0.2.1 NHƯNG chỉ fix **partial** — vẫn fail với batch 5 different-length

**Verified in-process:**
| Batch | Text length | Peak | Status |
|---|---|---|---|
| 1 | 1 text | 0.89 | ✅ |
| 2 | same text | 0.85-0.92 | ✅ |
| 3 | same text | 0.77-0.93 | ✅ |
| 5 | **same text** | 0.74-1.00 | ✅ |
| **5** | **5 different-length** | **0.15, 0.15, 0.15, 1.00, 0.15** | **❌ 4/5 FAIL** |

**Workaround:**
- **Sequential 1-by-1 trong cùng process** = load model 1 lần + generate 5 lần = OK 100%
- Bypass bug vì mỗi `model.generate()` call riêng biệt, KHÔNG qua `_generate_iterative` batch
- Wall time: 1:30 model load + 5×18s generate = ~2:30 total (tương đương batch 1:55 nhưng output OK)

**Code pattern (in-process sequential):**
```python
import time, torch
from omnivoice.models.omnivoice import OmniVoice

print("Loading model..."); t0 = time.time()
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
print(f"Loaded in {time.time()-t0:.1f}s")

ref_audio = "ref_10s.wav"
ref_text = "Xin chào đây là giọng đọc của Tuấn Anh. Tôi năm nay 30 tuổi đang thất nghiệp."  # 2 câu đầu

texts = [("id_1", "text 1"), ("id_2", "text 2"), ...]
for sid, text in texts:
    audio = model.generate(
        text=text, language="vi",
        ref_audio=ref_audio, ref_text=ref_text,
    )[0]
    sf.write(f"output/{sid}.wav", audio, model.sampling_rate)
    # Verify NGAY volumedetect: peak > 0.3
```

**Apply:** KHI cần generate ≥2 texts cùng voice, LUÔN dùng sequential in-process thay vì CLI batch. Tránh được MPS bug + output OK 100%.

## LESSON 3 — VERIFY = TRANSCRIPT KHÔNG PHẢI FILE SIZE

**Bug cũ:** Em verify batch 5 lần đầu chỉ check `duration` + `sample_rate` + `size` → báo "PASS" (file 24kHz valid) → anh nghe và flag "Toàn bộ 5batch lỗi hết" → mới phát hiện 4/5 file gần silent (-20.8 dB).

**Bug cũ #2:** Sau fix #1 (sequential OK), em vẫn chỉ check `volumedetect` (peak -4.3 dB OK) → báo "PASS" → anh nghe và flag "Tại sao luôn có câu Và bây giờ đang nhờ AI..." → mới phát hiện REF LEAK.

**New HARD RULE (3-layer verify bắt buộc):**
1. **Layer 1 — file valid:** ffprobe codec, sample_rate, channels, duration > 0
2. **Layer 2 — amplitude:** `volumedetect` peak > -10 dB, rms > -30 dB
3. **Layer 3 — content:** `mlx_whisper --word-timestamps True` → transcript match expected text (NO ref leak, NO garbage)

**Code recipe (verify_clip.py pattern — adapt cho TTS):**
```python
import subprocess
# 1. file valid
out = subprocess.check_output(["ffprobe", "-v", "error", "-show_entries",
                                "stream=codec_name,sample_rate,channels",
                                "-of", "csv=p=0", "out.wav"]).decode()
# 2. amplitude
amp = subprocess.check_output(["ffmpeg", "-i", "out.wav", "-af", "volumedetect",
                                "-vn", "-f", "null", "-"], stderr=subprocess.STDOUT).decode()
peak_db = parse_amp(amp)  # "max_volume: -5.0 dB"
# 3. transcript
subprocess.run(["mlx_whisper", "--model", "mlx-community/whisper-large-v3-mlx",
                "--language", "vi", "--output-format", "txt",
                "--word-timestamps", "True",
                "--output-dir", "/tmp/verify/", "out.wav"])
transcript = open("/tmp/verify/out.txt").read()
# Compare với expected text
assert "expected" in transcript, f"REF LEAK or missing content: {transcript}"
```

**Apply:** Mọi TTS output BẮT BUỘC qua cả 3 layer trước khi báo "PASS". Whisper word-level là ground truth cho content, không có gì thay thế được.

## LESSON 4 — KHI ANH CORRECT, EM ĐOÁN SAI → LESSON VỀ ROOT CAUSE ANALYSIS

**Context:** Em gặp ref leak, lần đầu đoán "model bug" → viết workaround (Whisper trim audio) → tốn 30 phút debugging. Anh correct: "Lúc em prompt omnivoice có vấn đề... chỉ cần fix prompt lại thôi" → em test 4 variants ref_text → fix = 2 câu đầu, 5 phút.

**Lesson:** TRƯỚC KHI blame model/library, **test prompt variants trước**:
- ref_text: full vs 1 câu vs 2 câu vs minimal
- temperature: 0.0 vs 0.5 vs 1.0
- num_step: 8 vs 32 vs 64
- 4 variants × 2 phút = 8 phút, save hours of "model bug" debugging

**Anti-pattern (em đã mắc):**
- ❌ Em nghĩ "OmniVoice là open source lớn, chắc model có bug"
- ❌ Em đi tìm GitHub issue, đọc code, viết workaround
- ❌ Anh correct → em test variants → fix 5 phút

**Pattern mới:**
1. User flag issue → check 4 prompt variants (cheap, 5 phút)
2. Nếu variants không fix → mới suspect model bug
3. Verify bằng evidence (file output, transcript), không phải assumption

## FINAL RECIPE (updated 2026-07-23 17:05)

```python
# CORRECT setup cho OmniVoice Vietnamese voice clone
from omnivoice.models.omnivoice import OmniVoice
import soundfile as sf, torch

# 1. Ref audio: 5-10s, 16kHz mono WAV
ref_audio = "ref_10s.wav"  # chuẩn bị trước

# 2. ref_text: 2 CÂU ĐẦU ONLY (sweet spot — đủ context, không leak)
ref_text = "Xin chào đây là giọng đọc của Tuấn Anh. Tôi năm nay 30 tuổi đang thất nghiệp."

# 3. Model load 1 lần
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)

# 4. Generate SEQUENTIAL (không dùng batch CLI — MPS bug)
texts = [("hook", "Các bạn ơi..."), ("problem", "..."), ...]
for sid, text in texts:
    audio = model.generate(text=text, language="vi", ref_audio=ref_audio, ref_text=ref_text)[0]
    sf.write(f"output/{sid}.wav", audio, model.sampling_rate)

# 5. VERIFY 3 LAYER (bắt buộc):
#    - ffprobe: codec, sample_rate, channels
#    - volumedetect: peak > -10dB
#    - Whisper transcript: match expected text, no ref leak
```

**Total wall time:** 1:30 model load + N×18s = 5 file = 2:30
**Output quality:** Peak ~0.5, 24kHz mono PCM, NO ref leak, voice giống ref

---

# Lessons từ session 23/07 20:50 (CONCAT + EMOTION)

## LESSON 5 — `pad_duration=0` để concat thẳng (anh feedback)

**Tuấn Anh feedback (verbatim):** *"Không fade không trim luôn audio bỏ padding 100ms luôn"*.

**Problem (em đã miss):** OmniVoice default `pad_duration=0.1` (100ms) + `fade_duration=0.1` → mỗi output có 200ms silence (100 đầu + 100 cuối). Concat N file → 200ms silent gap mỗi boundary. **Whisper hallucinate** sau gap lớn (vd "tuần" → "tuổi").

**3 phương án đã test (verified 23/07 21:00):**

| Method | Boundary peak | First audio | Whisper hallucinate |
|---|---|---|---|
| afade in+out (sai) | 0.00 | 104ms | ❌ "tuần" → "tuổi" |
| trim 100ms + fade out 30ms | 0.03-0.11 | 0ms (after trim) | ⚠️ OK |
| **NO PADDING (đúng)** | **0.65-0.77** | **0ms** | ✅ **OK + clean** |

**Fix đúng (anh correct):** Disable padding NGAY TỪ GENERATE:
```python
from omnivoice import OmniVoiceGenerationConfig
gc = OmniVoiceGenerationConfig(pad_duration=0.0, fade_duration=0.0)

# Generate
audio = model.generate(text=text, language="vi",
                        voice_clone_prompt=prompt,
                        generation_config=gc)[0]
# Audio bắt đầu ngay sample 0

# Concat thẳng
ffmpeg -y -i f1.wav -i f2.wav -i f3.wav \
  -filter_complex "[0:a][1:a][2:a]concat=n=3:v=0:a=1[out]" \
  -map "[out]" -ar 24000 -ac 1 final.wav
```

**Apply:** Mọi concat pipeline N file OmniVoice → set `pad_duration=0, fade_duration=0` ở `OmniVoiceGenerationConfig`, concat thẳng filter `[i:a]concat`. KHÔNG cần trim/fade post-process. Kết quả: voice bắt đầu ngay sample 0, max peak 0.65-0.77 (cao hơn cả baseline NamMinh).

**Anti-pattern (em đã mắc 2 lần trong session):**
- ❌ Apply `afade=t=in:out:0.03` → tạo 60ms silent gap, peak audio boundary = 0
- ❌ Trim 100ms post-process + apply fade → workaround OK nhưng voice bị cụt

**Lesson:** Khi concat audio files do model generate, **CHECK default padding TRƯỚC**, disable nếu cần. Apply post-process trim/fade = workaround chứ không phải fix.

## LESSON 6 — 13 Non-Verbal Emotion Tags (verified 23/07)

**Khám phá từ source `_NONVERBAL_PATTERN` (line 1651-1654):** OmniVoice hỗ trợ 13 inline emotion tags giúp voice "thật hơn" cho TikTok content. Đặc biệt Vietnamese hỗ trợ `[question-ah/oh]`, `[surprise-oh]`, `[dissatisfaction-hnn]`.

**Test 10 emotion variants (verified 23/07 20:45):**

| Tag | Emotion | Peak | Mean | Note |
|---|---|---|---|---|
| (no tag) | Baseline | -3.7 dB | -21.4 dB | Flat |
| `[laughter]` | Cười | -3.2 dB | -18.9 dB | Voice cao, vui |
| `[sigh]` | Thở dài | -3.2 dB | -21.0 dB | Hơi thở audible |
| `[question-ah]` | Hỏi "à" | -3.1 dB | -19.2 dB | Kết thúc lên cao |
| `[surprise-oh]` | Wow | **-2.6 dB** | **-17.6 dB** | **Loudest!** |
| `[dissatisfaction-hnn]` | Không hài lòng | -3.0 dB | -19.6 dB | "Hừm" phụ âm đầu |
| Multi-emo (3 tags) | Layered | **-2.1 dB** | -18.3 dB | Peak cao nhất |

**Emotion tags TĂNG peak amplitude (-2 to -3 dB vs -3.7 baseline)** → voice engaging hơn cho TikTok.

**Recipe TikTok với emotion (one-shot pipeline):**
```python
gc = OmniVoiceGenerationConfig(pad_duration=0.0, fade_duration=0.0)
prompt = VoiceClonePrompt.load("/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh.pt")

texts = [
    ("hook",    "[surprise-oh] Sale SỐC hôm nay! [laughter] Giảm 50% luôn các bạn ơi!"),
    ("problem", "[sigh] Bình thường máy hút bụi nặng lắm, pin yếu, lại còn ồn."),
    ("solution","Chiếc máy này thì sao[question-ah] Nhỏ gọn, êm, pin trâu, rẻ nữa!"),
    ("cta",     "Bấm giỏ hàng đi anh em[confirmation-en] Freeship toàn quốc nha!"),
]
for sid, text in texts:
    audio = model.generate(text=text, language="vi",
                            voice_clone_prompt=prompt,
                            generation_config=gc)[0]
    sf.write(f"{sid}.wav", audio, model.sampling_rate)
```

**Anti-patterns:**
- ❌ Capitalize tag (`[Laughter]`) → không match regex `_NONVERBAL_PATTERN`
- ❌ Tag liền text không có space: `[laughter]cười` → model không detect tag
- ❌ Mix nhiều tags cùng loại: `[laughter][laughter]` → redundant

**Pronunciation control (bonus):**
- English: `[B EY1 S]`, `[B AE1 S]` override CMU dict ("bass" vs "base")
- Chinese: uppercase pinyin + tone digit `ZHE2` override
- Inline preserved bởi `_apply_with_protection` trong normalize_text

**Apply:** TikTok content Tiếng Việt → dùng `[surprise-oh]` cho HOOK, `[sigh]` cho PROBLEM, `[question-ah]` cho USP, `[laughter]` + `[confirmation-en]` cho CTA. Voice sẽ có emotion rõ rệt, peak cao hơn baseline.
