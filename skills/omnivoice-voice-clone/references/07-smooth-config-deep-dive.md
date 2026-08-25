# Smooth Config — Deep Dive (24/07 finding)

## Problem

Voice clone output ngắt quãng + Whisper transcript sai các từ quan trọng ("dòng colo" thay vì "giọng clone"). User complaint: *"Giọng thì rõ nhưng ngắt quãng rất khó chịu"*

## Root Cause: `layer_penalty_factor=5.0` (OmniVoice default)

Model token generation over-penalize → prosody jerky + ASR transcription errors.

## A/B Test Matrix (7 variants, all run on V6 file voice clone + 1-câu script)

| Variant | Config | Dur | Peak (dB) | Whisper transcript |
|---|---|---|---|---|
| A_default | `layer_pen=5.0` (default) | 6.93s | 0.541 | "Bạn ơi, hôm nay mình test thử **dòng colo** mới nha" ❌ |
| B_layer_pen_1 | `layer_pen=1.0` | 8.78s | 0.596 | "Ô bạn ơi, hôm nay mình test thử **giọng colon** mới nha" ⚠️ |
| C_class_temp_1 | `class_temp=1.0` | 8.58s | 0.606 | "Hôm nay mình test thử **giọng colon** mới nha" ⚠️ |
| D_speed_0.9 | `speed=0.9, layer_pen=1.0` | 9.68s | 0.648 | (slow, partial) |
| E_speed_1.1 | `speed=1.1, layer_pen=1.0` | 8.00s | 0.295 | (fast, low peak) |
| F_pos_temp_3 | `speed=0.95, layer=1, pos_t=3.0` | 6.77s | 0.649 | "Ồ bạn ơi hôm nay mình test thử **giọng colon** mới nha" ⚠️ |
| **G_combined** | `speed=0.95, layer=1, pos_t=3.0` | 6.17s | 0.635 | "Ồ, bạn ơi, hôm nay mình test thử **giọng Claw** mới nha" ✅ |

**Key finding:** layer_penalty=5.0 → Whisper sai từ nghiêm trọng ("colo" thay vì "clone"). layer_penalty=1.0 → "colon" gần đúng. Combined config (speed=0.95, layer=1.0, pos_temp=3.0) → "Claw" (model nghe gần giống nhưng vẫn OK).

## Recommended Smooth Config (verified 24/07)

```python
from omnivoice import OmniVoiceGenerationConfig

gc = OmniVoiceGenerationConfig(
    pad_duration=0.0,          # NO PADDING (no trim/fade cần)
    fade_duration=0.0,         # NO FADE
    denoise=True,              # ← BẮT BUỘC (Pitfall #9)
    layer_penalty_factor=1.0,  # ← KEY FIX (default 5.0 quá cao)
    position_temperature=3.0,  # ← smoother (default 5.0)
)

# Plus: speed=0.95 qua model.generate()
audio = model.generate(
    text=text,
    language="vi",
    voice_clone_prompt=prompt,
    generation_config=gc,
    speed=0.95,
)[0]
```

## Flag Reference (OmniVoiceGenerationConfig)

| Field | Default | Smooth value | Effect |
|---|---|---|---|
| `pad_duration` | 0.1 | **0.0** | Skip 100ms lead padding |
| `fade_duration` | 0.1 | **0.0** | Skip 100ms trail fade |
| `denoise` | True | **True** | Prepend `<|denoise|>` token (NGĂN leak) |
| `preprocess_prompt` | True | **True** | Process ref audio trước khi dùng |
| `postprocess_output` | True | **True** | Process output audio sau khi generate |
| `layer_penalty_factor` | 5.0 | **1.0** | Token penalty (5.0 → jerky, 1.0 → smooth) |
| `position_temperature` | 5.0 | **3.0** | Sampling temperature (5.0 → choppy, 3.0 → smooth) |
| `class_temperature` | 0.0 | 0.0 | Class token (0.0 = deterministic, OK) |
| `num_step` | 32 | 32 | Diffusion steps (default OK) |
| `guidance_scale` | 2.0 | 2.0 | CFG scale (default OK) |
| `audio_chunk_duration` | 15.0 | 15.0 | Chunk size (default OK) |
| `audio_chunk_threshold` | 30.0 | 30.0 | Threshold (default OK) |

**`speed` qua `model.generate(speed=0.95)` — KHÔNG phải field của GenerationConfig.**

## Why A/B Test is Required

**Lesson (L6):** A/B test với ≥3 variants khi gặp bug không rõ root cause. 4 phút test saves hours debugging.

**Applied 3 lần trong session 24/07:**
1. **ref_text variants** (Pitfall #3): full / 1-sent / 2-sent / minimal → 2-sent = BEST
2. **concat methods** (Pitfall #6): afade / acrossfade / fade-out-only / trim-first → disable padding TỪ GENERATE
3. **denoise flags** (Pitfall #9): default / no_denoise / no_preprocess / no_postprocess → denoise=True = KEY
4. **smooth config** (Pitfall #10): default / layer_pen_1 / class_temp_1 / speed / pos_temp / combined → combined = BEST

## Files Saved

- `voice_compare/v6_smoother/A_default.wav` (6.93s, jerky)
- `voice_compare/v6_smoother/B_layer_pen_1.wav` (8.78s, smoother)
- `voice_compare/v6_smoother/G_combined.wav` (6.17s, BEST)
- `voice_compare/v6_smooth_tiktok/FINAL_TIKTOK_SMOOTH.wav` (59.92s, full TikTok review với smooth config)

## Script Updates

`scripts/generate_voice.py` đã được update với 3 flags:
- `--layer-penalty` (default 1.0)
- `--pos-temp` (default 3.0)
- `--speed` (default 0.95)

Verify chạy: `python3 scripts/generate_voice.py --help`
