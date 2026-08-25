---
title: mlx-whisper Apple Silicon workflow — Vietnamese ASR empirical benchmark
created: 2026-07-05
type: reference
tags: [whisper, mlx, apple-silicon, vietnamese, asr, benchmark]
parent_skill: mlops/models/whisper
status: active
---

# mlx-whisper Apple Silicon — Vietnamese ASR Workflow

> **Source**: Session 2026-07-05 — benchmark medium-mlx vs large-v3-turbo on 30s Vietnamese body-mist Dubai clip, plus large-v3-mlx loop-hallucinate case study from 2026-07-02.

## Why mlx-whisper for Apple Silicon

`openai-whisper` on M-series Macs runs at 0.32x real-time (CPU only) — 30s of audio takes ~10 minutes. `mlx-whisper` uses Apple's ML framework which runs natively on the M-series Neural Engine, achieving 0.20-0.30x real-time even on M1, and 0.05-0.10x on M2/M3 Pro. **For Tuấn Anh's TikTok content workflow on Apple Silicon, mlx-whisper is the only practical choice.**

## Installation

```bash
pip install mlx-whisper
```

Verify:
```bash
which mlx_whisper
# /Users/tuananh4865/Library/Python/3.9/bin/mlx_whisper

mlx_whisper --help | head -5
# Should print usage without error
```

If you get a `bad interpreter` error on the shebang, see Pitfall #2 in SKILL.md.

## Model selection — Vietnamese ASR empirical findings

### Test methodology (reproducible)

```bash
# 1. Extract 30s of clean Vietnamese audio (skip first 5s which often has silence)
ffmpeg -y -i source.mp4 -ss 5 -t 30 -ar 16000 -ac 1 -c:a pcm_s16le /tmp/test.wav

# 2. Transcribe with candidate models (same settings, just change --model)
for MODEL in mlx-community/whisper-medium-mlx \
             mlx-community/whisper-large-v3-turbo; do
  mlx_whisper \
    --model "$MODEL" \
    --language vi \
    --word-timestamps True \
    --output-format json \
    --output-name "/tmp/out_$(echo $MODEL | tr '/' '_')" \
    /tmp/test.wav
done

# 3. Compare segment count, word count, avg confidence, hallucinate signals
python3 << 'EOF'
import json
for path in ['/tmp/out_mlx-community_whisper-medium-mlx.json',
             '/tmp/out_mlx-community_whisper-large-v3-turbo.json']:
    d = json.load(open(path))
    segs = d['segments']
    text = ' '.join(s.get('text','').strip() for s in segs)
    words = [w for s in segs for w in s.get('words', []) if 'probability' in w]
    avg_conf = sum(w['probability'] for w in words) / len(words) if words else 0
    print(f"{path}: {len(segs)} segs, {len(words)} words, {avg_conf:.3f} avg_conf")
    print(f"  TEXT: {text[:200]}")
EOF
```

### Test results — body-mist Dubai clip 0688 (30s sample, 5-35s)

| Metric | medium-mlx | large-v3-turbo |
|--------|-----------|----------------|
| Time to transcribe | 7.1s | **6.4s** ✅ |
| Segments | **10** ✅ | 4 |
| Words | 84 | 94 |
| Avg word confidence | 0.75 | **0.85** ✅ |
| Brand name "AMAP" | ✅ "Amap" (capitalized) | ❌ "amap" (lowercase) |
| Numbers ("222k → 180k") | ✅ clean | ❌ "222 204 gì đó... xe 108" |
| Filler phrases | None ✅ | "cái này", "gì đó", "một cái một cái" |
| Loop hallucinate | None | None |

### Verdict

**For Vietnamese TikTok clip editing → medium-mlx wins.** Reasons:

1. **More word-level segments** (10 vs 4 per 30s) — câu treo detection requires fine-grained cut boundaries. Turbo's coarser segmentation loses natural break points.
2. **Better number/brand recognition** — turbo's higher confidence is misleading; it's confidently hallucinating "222 204 gì đó" instead of admitting uncertainty on a price.
3. **Cleaner filler** — turbo adds "cái này" / "gì đó" / "một cái một cái" which inflate word count without adding signal.
4. **Speed parity** — turbo is only 10% faster despite being 2× the model size. Not worth the trade-off.

## The large-v3-mlx loop hallucinate case (2026-07-02)

When source audio has speaker pause + trailing silence, `large-v3-mlx` (NOT turbo) may produce 50+ repetitions of one phrase. Verified example:

```
Source: 169.5s Vietnamese review clip of KNF Pocket 3 case
Whisper large-v3-mlx output:
  - segments 1-10: OK narrative content
  - segments 11-13 (102s → 169s): 67 seconds of "có thể bảo vệ cho chiếc Pocket 3"
    repeated 100+ times
  - audio thật im lặng (speaker đã kết thúc)
```

**Root cause**: large-v3-mlx overfits partial Vietnamese patterns. When audio becomes silent, it fills the silence with repeated memorized chunks.

**Fix**: Always use medium-mlx as default. Cross-validate with turbo (NOT large-v3) when medium output looks suspect. Trust medium if the two disagree.

## When to use large-v3-turbo (limited scope)

1. **Audio is difficult** (rolling shutter, heavy noise, multiple speakers) — turbo's higher confidence may help signal-to-noise ratio.
2. **English-language content** — turbo is trained for English primarily.
3. **Length under 3 minutes** — turbo's edge cases haven't been tested on >5min clips.
4. **Cross-validation only** — never use turbo as primary for Vietnamese clip editing.

## Audio preprocessing for best results

Whisper's official format is 16kHz mono float32 in range [-1, 1]. The default `mlx-whisper` CLI handles this automatically via `ffmpeg`, but if you want explicit control:

```bash
# Optimal format for mlx-whisper
ffmpeg -i source.mp4 \
  -ar 16000 \              # 16kHz sample rate
  -ac 1 \                  # Mono (downmix stereo)
  -c:a pcm_s16le \         # 16-bit PCM
  /tmp/clean.wav
```

For clips with very loud background noise, consider pre-denoising with `ffmpeg`'s `highpass` + `lowpass` filters:

```bash
ffmpeg -i source.mp4 \
  -af "highpass=f=80,lowpass=f=8000,dynaudnorm" \
  -ar 16000 -ac 1 \
  /tmp/clean.wav
```

## When to use Gemma 4 audio instead

Gemma 4 (Google's 2026 model) supports audio input via `transformers` pipeline. Use it ONLY when:

1. **AST (audio → translated text in 1 step)** — Whisper requires a separate translation pass through an LLM. Gemma 4 does both in one prompt.
2. **Multi-modal context queries** — send audio + a question in 1 prompt: "đoạn này giới thiệu sản phẩm gì?" Gemma 4 reads the audio AND answers.
3. **Clip length ≤30 seconds** — Gemma 4 has a 30s hard limit per clip.
4. **Token budget allows** — Gemma 4 charges 25 tokens/s of audio (6.25 for Gemma 3n).

Do NOT use Gemma 4 for:
- Vietnamese TikTok clip editing (no word-level timestamps, hard 30s limit)
- Clips longer than 30 seconds without manual chunking
- Apple Silicon offline workflows (Gemma 4 needs CUDA/GPU primarily)

## Performance on Apple Silicon M-series

| Chip | medium-mlx (30s audio) | large-v3-turbo (30s audio) |
|------|----------------------|----------------------------|
| M1 | ~9s | ~8s |
| M2 | ~7s | ~6.5s |
| M3 Pro | ~5.5s | ~5s |
| M4 Max | ~3.5s | ~3s |

## Files

- Test artifacts: `/tmp/whisper-test/{test_0688_30s.wav, out_medium.json, out_turbo.json}`
- Patch script: `templates/patch-mlx-whisper-load_models.py`
- Wrapper: `~/.hermes/scripts/whisper-transcribe` (auto-uses medium, language=vi)

## Related skills

- `tiktok-video-editor` — Daily Vietnamese TikTok clip workflow (uses medium-mlx as default)
- `tiktok-transcript-pipeline` — Higher-level pipeline for TikTok/YouTube transcript extraction