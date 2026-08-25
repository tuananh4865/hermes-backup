# Gemma 4 — Research notes (2026-07-22)

Condensed reference for future sessions asking about Gemma 4. Full wiki page: `/Volumes/Storage-1/Hermes/wiki/concepts/gemma-4-toan-dien-2026-07-22.md`. This file = the agent's working notes; the wiki page = the user-facing synthesis.

## Sources (5, cross-checked 2026-07-22)

1. Google AI — Video understanding: https://ai.google.dev/gemma/docs/capabilities/vision/video?hl=vi
2. Google AI — Audio understanding: https://ai.google.dev/gemma/docs/capabilities/audio?hl=vi
3. Hugging Face — Gemma4 Transformers docs v5.14.0: https://huggingface.co/docs/transformers/v5.14.0/en/model_doc/gemma4
4. Google AI — Gemma 4 model card: https://ai.google.dev/gemma/docs/core/model_card_4
5. Gemma Team Google DeepMind — Technical Report: https://arxiv.org/html/2607.02770

## Architecture at a glance

| Variant | Arch | Total params | Effective params | Context | Audio | Vision encoder | Audio encoder |
|---|---|---:|---:|---:|---|---:|---:|
| E2B | Dense + PLE | 5.1B | 2.3B | 128K | ✅ | ~150M | ~305M |
| E4B | Dense + PLE | 8B | 4.5B | 128K | ✅ | ~150M | ~305M |
| 12B Unified | Dense, encoder-free | 11.95B | 11.95B | 256K | ✅ | none (35M matmul) | none (raw projection) |
| 26B-A4B | MoE (8 active / 128 total) | 25.2B | 3.8B | 256K | ❌ | ~550M | none |
| 31B | Dense | 30.7B | 30.7B | 256K | ❌ | ~550M | none |

Training data cutoff: **January 2025**.

## Known cross-source contradiction

**Audio support on 12B Unified:**
- HF docs: NOT mentioned as audio-capable.
- Google audio guide sample code: includes `gemma-4-12B-it` in `MODEL_ID` dropdown.
- Google model card: explicit "audio supported on E2B, E4B, and 12B models".

→ Trust **Google model card + audio guide** for "what was shipped"; trust **HF** for "what `AutoProcessor` exposes today". Empirical check = load checkpoint + test `processor.feature_extractor`.

## Vision token budgets (configurable)

| Tokens | Patches (pre-pool) | Pixels | Use case |
|---:|---:|---:|---|
| 70 | 630 | ~161K | Fast classification |
| 140 | 1,260 | ~323K | Caption |
| 280 | 2,520 | ~645K | Default |
| 560 | 5,040 | ~1.3M | OCR, small text |
| 1,120 | 10,080 | ~2.6M | Document detail |

Constraint: both H and W must be divisible by 48 (= patch 16 × pooling kernel 3). Variable aspect ratio supported (no square squash).

## Audio constraints (Gemma 4)

- Max 30 seconds per input.
- Mono, 16 kHz, float32, range `[-1, 1]`.
- Token cost: ~25 tokens/sec.
- ASR prompt template forces digit output and no-newline.
- AST requires 2-step prompt: transcribe source lang then translate to target lang.

## Video

- Max ~60 seconds at 1 fps (per Google guide).
- All variants accept video as frame sequences (no dedicated video encoder).
- 1 fps is the documented default — likely misses fast actions.

## Reasoning / thinking mode

- Toggle via `<|think|>` token in system prompt.
- Output structure: `<|channel>thought\n[reasoning]<channel|>` then final answer.
- E2B/E4B: when thinking disabled, still emit empty thought block.

## Quantization

- Mobile: 2/4-bit weight + 8-bit activation (int8 + QAT).
- Q4_0 GGUF for llama.cpp ecosystem.
- W8A8 vision encoder: 400MB → 200MB forward memory, ~44% latency drop vs Gemma 3n.
- MTP drafter head for speculative decoding (75–500M params depending on variant).

## Recommendation for Tuấn Anh's DJI TikTok pipeline

- **Start:** E4B QAT for visual QA + 30s audio cross-check.
- **Scale up:** 12B Unified if RAM/GPU allows.
- **Do not replace:** Whisper medium-mlx as primary transcript.
- **Always pair:** frame analysis + Whisper transcript + silencedetect — never trust any single signal.

## Workflow recipe (drop-in for future sessions)

```bash
# 1. Extract audio (mono 16kHz for Gemma)
ffmpeg -i source.mp4 -vn -ac 1 -ar 16000 -f wav source.wav

# 2. Split audio into <=30s chunks with small overlap
ffmpeg -i source.wav -f segment -segment_time 28 -c copy chunk_%03d.wav

# 3. Run Whisper medium-mlx for primary transcript
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-dir ./transcript source.wav

# 4. Sample video frames at chosen fps
ffmpeg -i source.mp4 -vf "fps=1" frames/%04d.jpg

# 5. Cross-check with Gemma 4 E4B (HuggingFace)
python -c "from transformers import AutoProcessor; \
  p = AutoProcessor.from_pretrained('google/gemma-4-E4B-it'); \
  print('audio support:', hasattr(p, 'feature_extractor'))"
```

## Key gotchas to remember

- HF docs lag — verify modality support via `AutoProcessor`.
- Audio 30s limit forces chunking for any TikTok clip (most are 60-120s).
- Video 60s + 1 fps → may miss fast actions; for TikTok use 2-4 fps if bandwidth allows.
- Vision tokens scale RAM quickly — budget 280 default, bump only for OCR.
- Thinking mode = slower + more tokens; use only for multi-frame reasoning tasks.
- Benchmark numbers are vendor-reported; do not extrapolate to user's data.
