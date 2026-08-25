---
title: YouTube long-narration final config — 29/07 black-hole pilot
created: 2026-07-29
updated: 2026-07-29
type: reference
tags: [omnivoice, config, youtube, vietnamese, narration]
relationships: [pitfall-21, pitfall-20, pitfall-23, hard-rules-summary]
---

# Final config — YouTube long Vietnamese narration (verified 29/07)

## The chosen config

```python
OmniVoiceGenerationConfig(
    pad_duration=0.15,
    fade_duration=0.02,
    denoise=True,
    layer_penalty_factor=2.0,
    position_temperature=2.5,
)
# Plus: model.generate(text=full_text, language="vi",
#                      voice_clone_prompt=prompt,
#                      generation_config=gc, speed=0.90)[0]
```

## Why this config (vs the 9-variant grid)

| Variant | layer | position | pad | fade | speed | Quality |
|---|---|---|---|---|---|---|
| Default (5.0/5.0) | 5.0 | 5.0 | 0.1 | 0.1 | 0.95 | Jerky + filler |
| L1.5/P3.5 | 1.5 | 3.5 | — | — | 0.90 | Soft, mid filler |
| L1.5/P3.7 | 1.5 | 3.7 | — | — | 0.90 | Slightly more lively |
| L2/P3.5 | 2.0 | 3.5 | — | — | 0.90 | OK, occasional filler |
| L3/P2.0 | 3.0 | 2.0 | — | — | 0.90 | Rougher |
| L3/P2.5 | 3.0 | 2.5 | — | — | 0.90 | "Dạ" filler mid-segment |
| L4/P2.5 | 4.0 | 2.5 | — | — | 0.90 | Slight filler |
| L4/P3.5 | 4.0 | 3.5 | 0.05 | 0.1 | 0.90 | "ay" filler at start |
| L3/P2.5/P0.1/F0.05 | 3.0 | 2.5 | 0.1 | 0.05 | 0.90 | OK with Dạ filler |
| **L2/P2.5/P0.15/F0.02** | 2.0 | 2.5 | 0.15 | 0.02 | 0.90 | **CHOSEN** |

## Verified file

- Path: `/Volumes/Storage-1/Hermes/output/vuive-black-hole-voice/HO_DEN_OMNI_FULL_L2P2.5P0.15F0.02_192K.mp3`
- Duration: 13:05
- Size: 18.4 MB
- Peak: -1.0 dB, mean -19.4 dB
- Render: 1 take, no concat, no atempo, no emotion tag
- QA: Whisper transcript covers full script, no filler artifacts

## Hard rules attached

- **ZERO emotion tag by default** (Pitfall #21, vĩnh viễn).
- **YouTube speed = 0.90, NEVER atempo** (Pitfall #20, vĩnh viễn).
- **One giant call for long narration** (Pitfall #23, vĩnh viễn).
- **3-segment A/B test BEFORE full render** — required when changing any generation_config param.

## Generation recipe (1-liner)

```bash
# Build single full-text entry
python3 -c "
import json
items=[json.loads(l)['text'].strip() for l in open('/Volumes/Storage-1/Hermes/output/vuive-black-hole-voice/segments-no-tags.jsonl') if l.strip()]
json.dump({'id':'FULL','language':'vi','text':' '.join(items)}, open('/tmp/full.jsonl','w'), ensure_ascii=False)
"

# Generate (one call, ~13 min WAV)
python3 ~/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt \
  --text "$(cat /tmp/full.jsonl | python3 -c 'import sys,json; print(json.load(sys.stdin)["text"])')" \
  --output HO_DEN_OMNI_FULL_L2P2.5P0.15F0.02_RAW.wav

# Encode MP3 44.1kHz 192kbps
ffmpeg -i HO_DEN_OMNI_FULL_L2P2.5P0.15F0.02_RAW.wav \
  -ar 44100 -ac 1 -c:a libmp3lame -b:a 192k \
  HO_DEN_OMNI_FULL_L2P2.5P0.15F0.02_192K.mp3
```

## What did NOT fix the filler

- `position_temperature=2.0` — too low, voice flat.
- `pad_duration=0.3` — too long silence, listener loses thread.
- `denoise=False` — leaks ref audio.
- `speed=0.85` — too slow for 13 min narration.
- Splitting into 17 chunks with `…` — chunks 2-17 still clipped first/last phonemes (Pitfall #22 fallback).
