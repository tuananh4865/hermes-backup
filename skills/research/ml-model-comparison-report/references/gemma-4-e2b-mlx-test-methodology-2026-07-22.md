# Gemma 4 E2B — MLX Apple Silicon Test Methodology (2026-07-22)

Real test results + gotchas for running Gemma 4 E2B (and other Gemma 4 variants) on Mac Apple Silicon via `mlx-vlm`. Companion to `gemma-4-multimodal-2026-07-22.md`.

## Tested model + environment

- Model: `mlx-community/gemma-4-e2b-it-4bit` (3.3 GB on disk, 4-bit MLX quant)
- Hardware: MacBook Air M-class, 24 GB RAM, MPS backend
- Library versions: `mlx` 0.32.0, `mlx-vlm` 0.6.6, `transformers` 5.14.1, `mlx-audio` 0.4.4
- Test date: 2026-07-22
- Evidence: `/Volumes/Storage-1/Hermes/scratch/gemma4-e2b-test/` (test scripts + Whisper outputs + `results.json` + `README-test-results.md` + `README-video-test-results.md` + `README-translate-test-results.md`)

## Resource profile (real, peak RAM measured)

| Task | Peak RAM | Load time | Generation time | Tokens/sec |
|---|---:|---:|---:|---:|
| Audio ASR (6-10s clip, 4-bit E2B) | 4.15–4.19 GB | 2.1s | 0.96–1.16s | 56–62 gen-tps |
| Video understanding (8-10s 720p clip) | 4.45–5.34 GB | 3.0s | 5–7s total | 60–62 gen-tps |
| Translation EN↔VI combined (13.3s audio) | 4.28 GB | — | 2.66s | 55.4 gen-tps |
| ASR-only VI 5 consecutive runs (warm cache) | 3.96 GB | — | avg 1.03s, std 0.02s | 55.7 gen-tps |

**Verdict:** Chạy được trên máy 24 GB RAM. Audio + video peak combined ~5.4 GB. Không cần quantization thêm.

## mlx-vlm CLI entry point (CRITICAL gotcha)

`mlx-vlm` exposes TWO CLI scripts:

- `python -m mlx_vlm.generate` → dispatches to `generate/cli.py` (NO `--video` flag, args: `--image` + `--audio` only)
- `mlx_vlm.generate` (binary in venv `bin/`) → dispatches to `generate/dispatch.py` (HAS `--video` + `--fps`)

For Gemma 4 video input:

```bash
# ❌ DOES NOT WORK for video
python3 -m mlx_vlm.generate --video clip.mp4 --fps 1 --prompt "..."

# ✅ CORRECT — use the dispatch CLI binary
/Users/tuananh4865/.hermes/hermes-agent/venv/bin/mlx_vlm.generate \
  --model mlx-community/gemma-4-e2b-it-4bit \
  --video clip.mp4 \
  --fps 1 \
  --prompt "Describe this video in detail." \
  --max-tokens 300 \
  --temperature 0.7
```

Audit `mlx_vlm.generate --help` shows full arg list including `--video VIDEO [VIDEO ...]` + `--fps FPS`. The `cli.py` variant does not.

## Python API gotcha: `apply_chat_template(num_videos=1)` SILENTLY FAILS

If you call `apply_chat_template(processor, model.config, prompt, num_videos=1)` then pass `video=[path]` to `generate()`:

- The template inserts the text prompt only.
- Video frame embedding is NEVER inserted into the prompt.
- Model returns "Please provide the video you are referring to" — looks like the model is broken, but actually the chat template was missing the video slot.

**Correct pattern (messages list, not flat string):**

```python
from mlx_vlm import load, generate
from mlx_vlm.prompt_utils import apply_chat_template
import mlx.core as mx

model, processor = load("mlx-community/gemma-4-e2b-it-4bit")

# ✅ CORRECT — use messages list with type-tagged content
messages = [
    {
        "role": "user",
        "content": [
            {"type": "video", "video": "clip.mp4", "fps": 1.0},
            {"type": "text", "text": "Describe this video."},
        ],
    }
]
text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

# Process video → mlx arrays
from mlx_vlm.utils import load_video
frames = load_video("clip.mp4", fps=1.0)
inputs = processor(text=[text], videos=[frames], padding=True, return_tensors="pt")
input_ids = mx.array(inputs['input_ids'])
pixel_values = mx.array(inputs['pixel_values_videos'])
mask = mx.array(inputs['attention_mask'])
video_grid_thw = mx.array(inputs['video_grid_thw'])

result = generate(
    model, processor, prompt=text,
    temperature=0.7, max_tokens=300,
    input_ids=input_ids, pixel_values=pixel_values,
    mask=mask, image_grid_thw=video_grid_thw,
)
print(result.text)
```

The CLI bypasses this entire mess — it does the messages + frame loading internally.

For **audio**: the flat prompt signature works fine. `apply_chat_template(processor, model.config, prompt, num_audios=1)` + `audio=[path]` produces correct audio embedding. Same gotcha applies to `processor.config` vs `model.config` — use whichever has the attribute.

## Audio testing (verified)

4 tests done against Whisper medium baseline:

| Test | Gemma 4 E2B (4-bit) | Whisper medium | Verdict |
|---|---|---|---|
| EN journal1 (10s) | "I woke up a little today..." | "I woke up early today..." | ✅ Both PASS |
| VI simple (6.7s edge-tts) | Exact match | Exact match | ✅ Both PASS |
| VI silence-gap (9.6s with 5s silence) | "Câu 1. Đây là một chiếc máy ảnh rất tốt." | Same content + word timestamps | ✅ Both PASS, no hallucinate |
| VI tech+brand (DJI Pocket 3, CMOS...) | "**Jeremy** Pocket **ba**... **xe MOS**" | "**GDJI** Pocket 3... **Xe MoS**... **in**" | ⚠️ BOTH FAIL on brand/term |

**Key findings:**
- Gemma 4 E2B handles silence gap WITHOUT hallucinate (vs Whisper large-v3-mlx which loops)
- No word-level timestamps from Gemma → Whisper medium stays as primary transcript
- Both models hallucinate brand names + technical terms in Vietnamese at the same rate (~50% brand error)
- **Verdict:** Use Whisper medium as primary transcript, Gemma 4 as cross-check audio ≤30s only

## Translation + real-time pipeline (verified 2026-07-22, after anh pushed back)

### Pitfall #N+3 — "Audio max 30s" does NOT mean "max 30s audio total" — chunk it

Trigger: User asked "gemma e2B có phù hợp cho transcripts và dịch thuật real time không?" I initially said **NO** citing "audio max 30s per call". Anh pushed back: *"về audio mã 30s thì dịch thuật real time đâu bị gì? hoặc có thể chunk audio ra!"* — and he was right. Chunking is the obvious answer.

**Lesson for next session:** NEVER conclude a model is unsuitable for a use case based on a per-call input limit without checking whether the limit can be worked around with chunking. The bar is: can chunking + overlap get to acceptable quality + latency, yes/no? Test it before giving a verdict.

### Combined ASR + translate in 1 call (real-time verdict)

Gemma 4 E2B supports combined prompt per Google audio docs:

```
Transcribe the following speech segment in <SOURCE> into <SOURCE> text, 
then translate it into <TARGET>.
When formatting the answer, first output the transcription in <SOURCE>, 
then one newline, then output the string '<TARGET>: ', 
then the translation in <TARGET>.
```

**Verified wall times (in-memory model, Apple Silicon, 4-bit quant):**

| Task | Audio | Wall time | RTF* |
|---|---:|---:|---:|
| ASR-only VI | 6.7s | 1.05s | 0.16x |
| EN→VI combined | 13.3s | 2.66s | 0.20x |
| VI→EN combined | 10.3s | 2.36s | 0.23x |
| 5 consecutive ASR runs (warm cache) | 6.7s each | avg 1.03s, std ~0.02s | 0.15x |
| Chunked 14.78s (10s + 6.78s with 2s overlap) | 14.78s | 2.49s total | 0.17x |

**RTF (Real-Time Factor)** = processing_time / audio_duration. RTF < 0.5 = faster than real time, RTF > 1 = slower.

→ **Gemma 4 E2B runs 5-7x faster than real time** for audio ≤30s. Suitable for near-real-time transcription + translation.

### Chunked pipeline recipe (reusable for audio > 30s)

```python
import subprocess, time, wave
from pathlib import Path

def chunk_audio(input_path, output_pattern, chunk_sec=10, overlap_sec=2):
    """ffmpeg-based chunker with overlap."""
    with wave.open(str(input_path), 'rb') as w:
        duration = w.getnframes() / w.getframerate()
    chunks = []
    start, idx = 0.0, 0
    while start < duration:
        chunk_dur = min(chunk_sec, duration - start)
        out = Path(str(output_pattern).replace('.wav', f'_chunk{idx}.wav'))
        subprocess.run(['ffmpeg', '-y', '-i', str(input_path),
                       '-ss', str(start), '-t', str(chunk_dur),
                       '-ac', '1', '-ar', '16000', '-c:a', 'pcm_s16le',
                       str(out)], capture_output=True)
        chunks.append(out)
        start += chunk_sec - overlap_sec  # next chunk starts with overlap
        idx += 1
        if start >= duration: break
    return chunks

# Transcribe each chunk with in-memory model
for chunk in chunks:
    result = generate(model, processor, prompt=template, audio=[str(chunk)], ...)
    # Append result.text — text will overlap by ~overlap_sec
    # ⚠️ MUST dedup overlap region manually (see below)
```

**Overlap dedup gotcha:** When you chunk with 2s overlap, the same ~2 seconds of speech appear in BOTH chunks → naive concatenation duplicates the text. You need:

1. **Simple case**: keep chunk N's text, drop the first ~overlap_sec worth of words from chunk N+1
2. **Better**: use timestamp alignment (but Gemma 4 has no word-level timestamps!) → fall back to fuzzy word matching
3. **Pragmatic for <30s audio**: just don't chunk. Chunking overhead (~22% slowdown per test) is only worth it for >30s audio.

### Translation pipeline comparison (10.3s VI audio)

| Pipeline | Wall time | RTF | Quality |
|---|---:|---:|---|
| A: Whisper medium ASR + DeepL/Google API | 4.49s | 0.44x | ⭐⭐⭐⭐⭐ External API |
| B: Gemma 4 E2B combined (ASR+translate 1 call) | 2.61s | 0.25x | ⭐⭐⭐⭐ Integrated |
| C: Gemma 4 E2B ASR-only | 1.48s | 0.14x | ⭐⭐⭐⭐ ASR only |

→ Gemma combined (B) is **40% faster** than Whisper+API with acceptable translation quality. Trade-off: ~80-90% translation quality vs DeepL/Google. Choose B when you need offline + privacy, choose A when you need production-grade translation.

### When to recommend Gemma 4 E2B for real-time

| Use case | Fit? | Why |
|---|---|---|
| Voice memo → text ngay | ✅ | 1s wall time for 6.7s audio |
| Near-real-time subtitle generation (offline batch) | ✅ | 2-3s for clip ≤30s |
| Translation EN↔VI ≤15s | ✅ | 2.4s combined |
| Meeting notes (chunked 10s) | ✅ | Async, ~1s per chunk |
| Live caption <500ms | ❌ | RTF 0.16 = 800ms-1s for 5s audio, still too slow |
| Word-level timestamps | ❌ | Gemma 4 returns text only |
| Production-grade translation | ❌ | Use DeepL/Google API instead |

### Latency measurement gotcha

**Always measure wall time in-process (not subprocess CLI)** to get accurate numbers:

```python
# ❌ Includes Python startup + model reload (~6s overhead per call)
subprocess.run(['mlx_vlm.generate', '--model', ...], ...)

# ✅ Pure inference latency (1-2s for 6-10s audio)
from mlx_vlm import load, generate
model, processor = load('...')  # once
t0 = time.time()
result = generate(model, processor, prompt=..., audio=[...])
print(f'Pure latency: {time.time() - t0:.2f}s')
```

CLI subprocess adds ~6s of Python startup + model reload each call. Only use CLI for one-off testing. Production pipelines MUST load model once and call `generate()` in-process.

## Video testing (verified)

5 tests done on real DJI clips:

| Test | Result |
|---|---|
| DJI beach clip (8.4s 720p fps=1) — EN describe | ✅ Scene + temporal segmentation chính xác |
| DJI beach clip — product Q | ⚠️ Conservative "cannot confirm" (camera bị che) |
| DJI beach clip — VI describe | ✅ Tiếng Việt tự nhiên, segment đúng timestamps |
| TikTok review (10s 720p fps=1) — product detection | ⚠️ Hallucinate "camera/BORT" thay vì "case/QCY" |
| TikTok review (10s 720p fps=2) — brand detection | ❌ Hallucinate nặng "BOTAF"/"gaming controller" |

**Key findings:**
- Scene understanding + temporal segmentation rất tốt (sky→sea→waves→woman+child)
- Tiếng Việt output trực tiếp, không cần dịch qua Anh
- **fps=1 OK**, fps=2+ KHÔNG tự động tốt hơn — model bắt đầu interpolate gây hallucinate
- Brand/logo + small text OCR KHÔNG đáng tin (hallucinate nặng)
- Conservative khi uncertain (Test 2) — không bịa

## Pre-flight recipe (reusable)

```bash
# 1. Check MLX available + venv has mlx-vlm
/Users/tuananh4865/.hermes/hermes-agent/venv/bin/python -c "
import mlx.core as mx, mlx_vlm
print('mlx ok, mlx_vlm', mlx_vlm.__file__)
"

# 2. Disk check (model is 3.3 GB)
df -h / | tail -1

# 3. Download model
hf download mlx-community/gemma-4-e2b-it-4bit

# 4. Audio test (Vietnamese)
edge-tts --voice vi-VN-HoaiMyNeural --text "..." --write-media test.mp3
ffmpeg -y -i test.mp3 -ac 1 -ar 16000 -c:a pcm_s16le test_16k.wav
/Users/tuananh4865/.hermes/hermes-agent/venv/bin/mlx_vlm.generate \
  --model mlx-community/gemma-4-e2b-it-4bit \
  --audio test_16k.wav \
  --prompt "Transcribe the following speech segment in Vietnamese into Vietnamese text." \
  --max-tokens 256 --temperature 1.0 --top-p 0.95 --top-k 64

# 5. Video test (downscale 4K → 720p first for speed)
ffmpeg -y -i source.mp4 -vf "scale=1280:720" -c:v libx264 -preset ultrafast -crf 28 test_720p.mp4
/Users/tuananh4865/.hermes/hermes-agent/venv/bin/mlx_vlm.generate \
  --model mlx-community/gemma-4-e2b-it-4bit \
  --video test_720p.mp4 --fps 1 \
  --prompt "Describe this video in detail." \
  --max-tokens 300 --temperature 0.7

# 6. Translation test (combined ASR+translate in 1 call)
/Users/tuananh4865/.hermes/hermes-agent/venv/bin/mlx_vlm.generate \
  --model mlx-community/gemma-4-e2b-it-4bit \
  --audio audio_16k.wav \
  --prompt "Transcribe the following speech segment in Vietnamese into Vietnamese text, 
           then translate it into English. 
           When formatting the answer, first output the transcription in Vietnamese, 
           then one newline, then output the string 'English: ', 
           then the translation in English." \
  --max-tokens 512 --temperature 0.7
```

## Ground truth verification (mandatory before claiming model works)

Vision-ground-truth workflow for video test clips:

```bash
# Extract 5 sample frames
for t in 1 3 5 7 9; do
  ffmpeg -y -i test_720p.mp4 -ss $t -vframes 1 -q:v 2 frame_${t}s.jpg
done

# Use vision tool (mcp__MiniMax__understand_image or vision_analyze) on each frame
# to establish what the model SHOULD see, before asking Gemma 4 to describe it.
```

This is essential because:
- Whisper transcripts can hallucinate product names (PITFALL clip_0004 "Doroto" vs OTOBOP)
- Gemma 4 can hallucinate brands ("BORT", "BOTAF", "gaming controller" instead of actual product)
- Without ground truth, you cannot distinguish "model is right" from "model is confidently wrong"

## Gotchas to remember

1. **CLI entry point matters** — `mlx_vlm.generate` (binary) ≠ `python -m mlx_vlm.generate` for video. Check `--help` output to confirm `--video` flag exists.
2. **apply_chat_template flat signature silently fails for video** — always use `messages` list format with `type: video` content tag. Audio works with flat signature.
3. **Audio 30s hard limit per call** — chunk anything longer with 10s + 2s overlap (RTF stays 0.17x).
4. **Video 4K is too slow** — downscale to 720p before testing (4K is 4× pixel count, vision encoder scales linearly).
5. **fps=1 default is intentional** — bumping to fps=2 does NOT improve quality, increases hallucination due to model interpolation.
6. **Hallucination rate on brand/tech terms is ~50%** — never trust 1 model for product review transcripts. Always cross-check with vision + manual review.
7. **No word-level timestamps** — Gemma 4 cannot replace Whisper medium for edit-timestamp workflows.
8. **Whisper still handles silence gap better than Whisper large-v3-mlx** — but Gemma 4 + Whisper medium BOTH handle silence gap without hallucinate. The gap is between large-v3 (loops) and medium/E2B (clean).
9. **RTF = wall_time / audio_duration** — use this metric consistently. CLI subprocess adds ~6s Python startup overhead → measure in-process for real numbers.
10. **Don't overcautious verdict** — if the only blocker is a per-call input limit, test chunking before concluding "not suitable for real time".

## Reference

- Real test scripts: `/Volumes/Storage-1/Hermes/scratch/gemma4-e2b-test/test_v2.py` (audio), `test_translate.py` (translation), `test_latency.py` (RTF measurement), `test_chunked.py` (chunked pipeline), `test_compare.py` (3-pipeline comparison)
- For video, use `mlx_vlm.generate` CLI binary directly (not the deprecated Python API)
- Whisper outputs: `/Volumes/Storage-1/Hermes/scratch/gemma4-e2b-test/whisper_*/`
- Wiki concept page: `/Volumes/Storage-1/Hermes/wiki/concepts/gemma-4-toan-dien-2026-07-22.md`
- Translation results file: `/Volumes/Storage-1/Hermes/scratch/gemma4-e2b-test/README-translate-test-results.md`