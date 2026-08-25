---
name: whisper
description: OpenAI's general-purpose speech recognition model. Supports 99 languages, transcription, translation to English, and language identification. Six model sizes from tiny (39M params) to large (1550M params). Use for speech-to-text, podcast transcription, or multilingual audio processing. Best for robust, multilingual ASR.
version: 1.1.0
author: Orchestra Research + Hermes Agent (v1.1.0 — added mlx-whisper Apple Silicon workflow + Vietnamese ASR empirical findings + HF config patch recipe)
license: MIT
dependencies: [openai-whisper, transformers, torch]
metadata:
  hermes:
    tags: [Whisper, Speech Recognition, ASR, Multimodal, Multilingual, OpenAI, Speech-To-Text, Transcription, Translation, Audio Processing, Apple-Silicon, MLX]

---

# Whisper - Robust Speech Recognition

OpenAI's multilingual speech recognition model.

## When to use Whisper

**Use when:**
- Speech-to-text transcription (99 languages)
- Podcast/video transcription
- Meeting notes automation
- Translation to English
- Noisy audio transcription
- Multilingual audio processing

**Metrics**:
- **72,900+ GitHub stars**
- 99 languages supported
- Trained on 680,000 hours of audio
- MIT License

**Use alternatives instead**:
- **AssemblyAI**: Managed API, speaker diarization
- **Deepgram**: Real-time streaming ASR
- **Google Speech-to-Text**: Cloud-based
- **mlx-whisper** (Apple Silicon) — see `references/mlx-whisper-apple-silicon.md` for the MLX workflow that runs 4-8× faster than openai-whisper on M-series chips, plus the Vietnamese ASR empirical benchmark (medium vs large-v3-turbo) and the HF-config patch recipe

## Quick start

### Installation

```bash
# Requires Python 3.8-3.11
pip install -U openai-whisper

# Requires ffmpeg
# macOS: brew install ffmpeg
# Ubuntu: sudo apt install ffmpeg
# Windows: choco install ffmpeg
```

### Basic transcription

```python
import whisper

# Load model
model = whisper.load_model("base")

# Transcribe
result = model.transcribe("audio.mp3")

# Print text
print(result["text"])

# Access segments
for segment in result["segments"]:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
```

## Model sizes

```python
# Available models
models = ["tiny", "base", "small", "medium", "large", "turbo"]

# Load specific model
model = whisper.load_model("turbo")  # Fastest, good quality
```

| Model | Parameters | English-only | Multilingual | Speed | VRAM |
|-------|------------|--------------|--------------|-------|------|
| tiny | 39M | ✓ | ✓ | ~32x | ~1 GB |
| base | 74M | ✓ | ✓ | ~16x | ~1 GB |
| small | 244M | ✓ | ✓ | ~6x | ~2 GB |
| medium | 769M | ✓ | ✓ | ~2x | ~5 GB |
| large | 1550M | ✗ | ✓ | 1x | ~10 GB |
| turbo | 809M | ✗ | ✓ | ~8x | ~6 GB |

**Recommendation**: Use `turbo` for best speed/quality, `base` for prototyping

## Transcription options

### Language specification

```python
# Auto-detect language
result = model.transcribe("audio.mp3")

# Specify language (faster)
result = model.transcribe("audio.mp3", language="en")

# Supported: en, es, fr, de, it, pt, ru, ja, ko, zh, and 89 more
```

### Task selection

```python
# Transcription (default)
result = model.transcribe("audio.mp3", task="transcribe")

# Translation to English
result = model.transcribe("spanish.mp3", task="translate")
# Input: Spanish audio → Output: English text
```

### Initial prompt

```python
# Improve accuracy with context
result = model.transcribe(
    "audio.mp3",
    initial_prompt="This is a technical podcast about machine learning and AI."
)

# Helps with:
# - Technical terms
# - Proper nouns
# - Domain-specific vocabulary
```

### Timestamps

```python
# Word-level timestamps
result = model.transcribe("audio.mp3", word_timestamps=True)

for segment in result["segments"]:
    for word in segment["words"]:
        print(f"{word['word']} ({word['start']:.2f}s - {word['end']:.2f}s)")
```

### Temperature fallback

```python
# Retry with different temperatures if confidence low
result = model.transcribe(
    "audio.mp3",
    temperature=(0.0, 0.2, 0.4, 0.6, 0.8, 1.0)
)
```

## Command line usage

```bash
# Basic transcription
whisper audio.mp3

# Specify model
whisper audio.mp3 --model turbo

# Output formats
whisper audio.mp3 --output_format txt     # Plain text
whisper audio.mp3 --output_format srt     # Subtitles
whisper audio.mp3 --output_format vtt     # WebVTT
whisper audio.mp3 --output_format json    # JSON with timestamps

# Language
whisper audio.mp3 --language Spanish

# Translation
whisper spanish.mp3 --task translate
```

## Batch processing

```python
import os

audio_files = ["file1.mp3", "file2.mp3", "file3.mp3"]

for audio_file in audio_files:
    print(f"Transcribing {audio_file}...")
    result = model.transcribe(audio_file)

    # Save to file
    output_file = audio_file.replace(".mp3", ".txt")
    with open(output_file, "w") as f:
        f.write(result["text"])
```

## Real-time transcription

```python
# For streaming audio, use faster-whisper
# pip install faster-whisper

from faster_whisper import WhisperModel

model = WhisperModel("base", device="cuda", compute_type="float16")

# Transcribe with streaming
segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print(f"[{segment.start:.2f}s -> {segment.end:.2f}s] {segment.text}")
```

## GPU acceleration

```python
import whisper

# Automatically uses GPU if available
model = whisper.load_model("turbo")

# Force CPU
model = whisper.load_model("turbo", device="cpu")

# Force GPU
model = whisper.load_model("turbo", device="cuda")

# 10-20× faster on GPU
```

## Integration with other tools

### Subtitle generation

```bash
# Generate SRT subtitles
whisper video.mp4 --output_format srt --language English

# Output: video.srt
```

### With LangChain

```python
from langchain.document_loaders import WhisperTranscriptionLoader

loader = WhisperTranscriptionLoader(file_path="audio.mp3")
docs = loader.load()

# Use transcription in RAG
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(docs, OpenAIEmbeddings())
```

### Extract audio from video

```bash
# Use ffmpeg to extract audio
ffmpeg -i video.mp4 -vn -acodec pcm_s16le audio.wav

# Then transcribe
whisper audio.wav
```

## Best practices

1. **Use turbo model** - Best speed/quality for English
2. **Specify language** - Faster than auto-detect
3. **Add initial prompt** - Improves technical terms
4. **Use GPU** - 10-20× faster
5. **Batch process** - More efficient
6. **Convert to WAV** - Better compatibility
7. **Split long audio** - <30 min chunks
8. **Check language support** - Quality varies by language
9. **Use faster-whisper** - 4× faster than openai-whisper
10. **Monitor VRAM** - Scale model size to hardware

## Performance

| Model | Real-time factor (CPU) | Real-time factor (GPU) |
|-------|------------------------|------------------------|
| tiny | ~0.32 | ~0.01 |
| base | ~0.16 | ~0.01 |
| turbo | ~0.08 | ~0.01 |
| large | ~1.0 | ~0.05 |

*Real-time factor: 0.1 = 10× faster than real-time*

## Language support

Top-supported languages:
- English (en)
- Spanish (es)
- French (fr)
- German (de)
- Italian (it)
- Portuguese (pt)
- Russian (ru)
- Japanese (ja)
- Korean (ko)
- Chinese (zh)

Full list: 99 languages total

## Limitations

1. **Hallucinations** - May repeat or invent text
2. **Long-form accuracy** - Degrades on >30 min audio
3. **Speaker identification** - No diarization
4. **Accents** - Quality varies
5. **Background noise** - Can affect accuracy
6. **Real-time latency** - Not suitable for live captioning

## Resources

- **GitHub**: https://github.com/openai/whisper ⭐ 72,900+
- **Paper**: https://arxiv.org/abs/2212.04356
- **Model Card**: https://github.com/openai/whisper/blob/main/model-card.md
- **Colab**: Available in repo
- **License**: MIT

---

## Apple Silicon MLX workflow (mlx-whisper) — 2026 ADDITION

For M1/M2/M3/M4 Macs, `mlx-whisper` (Apple's ML framework) runs Whisper 4-8× faster than openai-whisper on the same hardware. **This is the recommended path for Tuấn Anh's TikTok content workflow** (Vietnamese clips, Apple Silicon Mac, word-level timestamps needed for câu treo detection).

### Installation

```bash
pip install mlx-whisper
```

### Model variants on HuggingFace

| HF repo | Size | Speed (30s audio) | Vietnamese quality |
|---------|------|-------------------|--------------------|
| `mlx-community/whisper-medium-mlx` | ~1.5GB | ~7s | ✅ Safety net / fallback — no loop hallucinate risk |
| `mlx-community/whisper-large-v3-mlx` | ~3GB | ~12s | ✅⭐ **Default since 2026-07-22** — catches CNC / focus / 3cm / Anh-Vi technical terms |
| `mlx-community/whisper-large-v3-turbo` | ~1.6GB | ~6.5s | ⚠️ Fewer word-level segments (4 vs 10 per 30s) — bad for câu treo detection |

### Vietnamese ASR empirical findings (verified 2026-07-05 on 30s of body-mist Dubai clip)

Test: same audio, same `--language vi --word-timestamps True`, two model variants.

| Metric | medium-mlx | large-v3-turbo |
|--------|-----------|----------------|
| **Time to transcribe 30s** | 7.1s | **6.4s** ✅ |
| **Segments produced** | **10** ✅ | 4 |
| **Total words captured** | 84 | 94 |
| **Avg word confidence** | 0.75 | **0.85** ✅ |
| **Brand name "AMAP" correctly capitalized** | ✅ "Amap" | ❌ "amap" |
| **Number accuracy ("222k → 180k")** | ✅ clean | ❌ "222 204 gì đó... xe 108" |
| **Filler phrases introduced** | None ✅ | "cái này", "gì đó", "một cái một cái" |

**Verdict for Vietnamese TikTok clip editing (updated 2026-07-22)**: **large-v3-mlx wins for technical accuracy**, but use the `whisper-transcribe` wrapper's auto-fallback to handle the legacy loop risk.

| Metric | medium-mlx | large-v3-mlx |
|--------|-----------|--------------|
| Time to transcribe 115s | 19.3s | 36.0s |
| RTF (real-time factor) | 0.17x | 0.31x |
| Segments produced (115s) | **13** ✅ clean grouping | 39 over-segmented |
| Catches technical term "CNC" | ❌ missed | ✅ caught |
| Catches technical term "focus" | ❌ "phó kết" hallucinate | ✅ exact |
| Catches "3cm" / "15cm" specs | ❌ missed | ✅ caught |
| "đặc thùng" hallucinate (PITFALL #69) | ⚠️ present | cleaner |
| Loop hallucinate on trailing silence | Very low | Medium → auto-fallback covers it |

**Decision rule**: Use **`mlx-community/whisper-large-v3-mlx`** as default via `~/.hermes/scripts/whisper-transcribe`. The wrapper auto-detects any 5-word phrase repeating ≥5 times and re-runs with medium-mlx as safety net (covers the 2026-07-02 DRIVE2 loop case). Manual override: `MLX_WHISPER_MODEL=mlx-community/whisper-medium-mlx whisper-transcribe input.mp4`.

### CLI workflow

```bash
# Standard transcribe (word-level timestamps = MANDATORY for Vietnamese câu treo detection)
mlx_whisper \
  --model mlx-community/whisper-medium-mlx \
  --language vi \
  --word-timestamps True \
  --output-format json \
  --output-dir ./transcripts \
  input.wav

# Cross-validate when medium output looks suspect (loop, missing segments, hallucinate)
mlx_whisper \
  --model mlx-community/whisper-large-v3-turbo \
  --language vi \
  --word-timestamps True \
  --output-format json \
  --output-dir ./transcripts-cross \
  input.wav

# Compare: which model has more complete narrative?
diff <(jq -r '.segments[].text' transcripts/out.json) \
     <(jq -r '.segments[].text' transcripts-cross/out.json)
```

### Common pitfalls

**Pitfall #1 — HF config mismatch on `mlx-community/whisper-large-v3-turbo`**

If you get:
```
TypeError: __init__() got an unexpected keyword argument '_name_or_path'
```
or
```
TypeError: __init__() missing 1 required positional argument: 'n_mels'
```

Cause: `mlx_whisper==0.4.3` was written before HuggingFace added modern fields like `_name_or_path`, `activation_dropout`, `_commit_hash`, `transformers_version`. HF models on `openai/whisper-large-v3-turbo` use the modern config format which `whisper.ModelDimensions(**config)` cannot parse.

Fix: patch `/path/to/site-packages/mlx_whisper/load_models.py` to whitelist the 10 fields `ModelDimensions` accepts. See `templates/patch-mlx-whisper-load_models.py` for the exact diff.

**Pitfall #2 — shebang broken after Xcode update**

```
/bin/bash: /Users/tuananh4865/Library/Python/3.9/bin/mlx_whisper: /Applications/Xcode.app/Contents/Developer/usr/bin/python3: bad interpreter
```

Cause: `pip install` from Xcode Python writes shebang pointing at Xcode's Python. When Xcode updates or is removed, the shebang breaks.

Fix: re-write the shebang to use Apple-supported CommandLineTools Python:
```bash
sed -i '' '1s|.*|#!/Library/Developer/CommandLineTools/usr/bin/python3|' \
    /Users/tuananh4865/Library/Python/3.9/bin/mlx_whisper
```

**Pitfall #3 — large-v3-mlx can loop on Vietnamese clips with trailing silence (legacy 2026-07-02 risk, now auto-mitigated by wrapper)**

When source audio has speaker pause + trailing silence, `large-v3-mlx` may produce 50+ repetitions of one phrase (e.g. "có thể bảo vệ cho chiếc Pocket 3" × 100 lần in 67s). Discovered 2026-07-02 on the KNF Pocket 3 DRIVE2 clip.

**Mitigation (since 2026-07-22)**: `~/.hermes/scripts/whisper-transcribe` wraps `mlx_whisper` calls with auto-detection. If any 5-word phrase appears ≥5 times in the output, it:
1. Backs up the bad transcript to `<basename>_large_v3_LOOP.txt`
2. Re-runs with `mlx-community/whisper-medium-mlx`
3. Logs the fallback reason so the agent can see what happened

Verified 2026-07-22 on `clip_0036 v9` (clean transcript) and on the same clip with 20s of trailing silence appended (large-v3 itself returned clean — fallback armed but inert). Force the medium model for clips known to be loop-sensitive: `MLX_WHISPER_MODEL=mlx-community/whisper-medium-mlx whisper-transcribe input.mp4`. Backup of the pre-change medium-default wrapper lives at `~/.hermes/scripts/whisper-transcribe.bak-medium-2026-07-22` for rollback.

### Why not Gemma 4 audio for this workflow?

Google's Gemma 4 (2026) supports audio input via `transformers` pipeline. Compared to Whisper:

| Capability | Whisper medium-mlx | Gemma 4 audio |
|-----------|-------------------|----------------|
| Max clip length | No hard limit (sliding window) | **30s hard limit** |
| Word-level timestamps | ✅ (`--word-timestamps True`) | ❌ None (text only) |
| Vietnamese support | ✅ Verified clean | ✅ Multilingual, untested on VN |
| Apple Silicon | ✅ MLX native | ❌ GPU/CUDA primarily |
| Token cost | N/A (offline) | 25 tokens/s × duration |
| Speed (30s clip) | 6-7s | Comparable |

**Use Whisper** for any workflow needing word-level cut boundaries (câu treo detection, word-level removal). **Use Gemma 4 audio** only for: (a) AST (audio → translated text in 1 step), (b) multi-modal context queries ("what does this audio describe?"), (c) clips ≤30s.

### When to use each model

| Situation | Model |
|-----------|-------|
| Default Vietnamese TikTok clip transcription | `mlx-community/whisper-large-v3-mlx` via `~/.hermes/scripts/whisper-transcribe` (auto-fallback medium on loop) ⭐ |
| English clip, want higher confidence, length ≤3min | `mlx-community/whisper-large-v3-turbo` |
| Cross-validate when large-v3 output has loop/missing segments | `mlx-community/whisper-medium-mlx` (auto-handled by wrapper) |
| Audio + question in 1 prompt (multi-modal) | Gemma 4 via `transformers` |
| Long-form audio (>30 min) | openai/whisper large-v3 with chunking |
| Real-time streaming | faster-whisper with `beam_size=5` |

### Related references

- `references/mlx-whisper-apple-silicon.md` — Deep dive on MLX workflow, CUDA-free path, Vietnamese benchmark methodology
- `references/large-v3-default-2026-07-22.md` — Session-detail for the wrapper default flip (medium → large-v3 + auto-fallback). Includes 3-clip verification matrix and surviving hallucinate caveats.
- `templates/patch-mlx-whisper-load_models.py` — The patch script for HF config mismatch
- Skill `tiktok-video-editor` — Daily Vietnamese TikTok clip workflow that uses this default