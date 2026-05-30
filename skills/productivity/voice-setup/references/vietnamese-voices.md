# Vietnamese TTS Voice Reference

## Available Vietnamese Voices (Edge TTS)

| Voice ID | Gender | Style | Notes |
|----------|--------|-------|-------|
| `vi-VN-HoaiMyNeural` | Female | Friendly, Positive | ✅ Working (2026-05-30) |
| `vi-VN-NamMinhNeural` | Male | Friendly, Positive | ✅ Working (2026-05-30) |

## Tested Configs

### HoaiMyNeural (Female) — CURRENT DEFAULT
```yaml
tts:
  provider: edge
  edge:
    voice: vi-VN-HoaiMyNeural  # KEY IS "voice" NOT "voice_id"
    speed: 1.0
    # pitch: '+0Hz'  # Optional
```

### NamMinhNeural (Male)
```yaml
tts:
  provider: edge
  edge:
    voice: vi-VN-NamMinhNeural
    speed: 1.0
```

## MiniMax TTS (Limited)
- Model: `speech-02-hd`
- Voice: `English_expressive_narrator` (English only)
- Limit: 5 hours/day, resets at ~10PM Vietnam time
- Issue: Does NOT support emotion parameter (causes API error 2056)
- Issue: Does NOT support emotion parameter (causes API error 2056)

## STT: faster-whisper

- Vietnamese model: works locally
- No API key needed
- Config:
```yaml
stt:
  provider: faster-whisper
  faster-whisper:
    model_size: small
    compute_type: float32
```
