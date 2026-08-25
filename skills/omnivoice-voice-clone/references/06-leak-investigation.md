# Leak Investigation — Reference

Reference doc for `omnivoice-voice-clone` skill. Captures:

1. **Finding #9** — root cause of ref-text leak (`denoise=False` → `<|denoise|>` token stripped → model echoes ref text)
2. **A/B test methodology** — 6-variant controlled experiment to isolate which `OmniVoiceGenerationConfig` flag causes the leak
3. **Denoise recipe** — ffmpeg `afftdn` filter chain + highpass/lowpass for cleaning voice-ref audio BEFORE saving `.pt`
4. **SHA256 dedup pattern** — verify Telegram-cache voice files are not duplicates before reusing
5. **Terminology correction** — "voice ref" ≠ "file voice clone" (the .pt, not the raw audio)

---

## Finding #9 — `denoise=False` CASUES ref-text leak

**Verified:** 24/07/2026, Mac M-series MPS, OmniVoice 0.2.1, voice clone prompt v5 (aggressive denoised Telegram audio), single-segment test text.

### Mechanism

OmniVoice architecture uses the `<|denoise|>` token as a conditioning signal:

```
Input:  [<|denoise|>] + ref_audio_tokens + ref_text + target_text
Output: ref_text echo + target_text audio   (NO <|denoise|> token)
Output: target_text audio only              (<|denoise|> token present)
```

`OmniVoiceGenerationConfig.denoise=True` (default) prepends the `<|denoise|>` token. Switching it to `False` removes the token → model interprets the conditioning differently and echoes the ref text as a prefix.

### Evidence (Whisper transcript)

| Variant | Config | Whisper transcript |
|---|---|---|
| **A_default** | `OmniVoiceGenerationConfig()` | "Trài Trồi **Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng OmniVoice trên máy mát nhé**" |
| B_no_denoise | `denoise=False` | "**Trời ơi là Tuấn Anh đây Trời ơi Tôi là Tuấn Anh đây nè** Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng Omnivoice trên máy mát nhé" |
| C_no_preprocess | `preprocess_prompt=False` | "**Mình sẽ hướng dẫn chi tiết cách sử dụng Omni Voice trên máy mát nhé**" |
| D_no_postprocess | `postprocess_output=False` | "**Chào! Anh Mắc đây nè! Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng Omni Voice trên máy mát nhé!**" |
| E_no_denoise_preproc | `denoise=False, preprocess_prompt=False` | "à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à à" (LOOP) |
| F_all_off | `denoise=False, preprocess_prompt=False, postprocess_output=False` | "**Tui Tuấn Ao, tui là Tuấn Anh đây nè**. Hôm nay mình sẽ hướng dẫn chi tiết cách sử dụng Omnivoice trên máy Mac nhé" |

### Rule

> **BẮT BUỘC keep `denoise=True` (default). Nếu cần custom, swap `preprocess_prompt=False` thay vì `denoise=False`.**

Also: `denoise=False + preprocess_prompt=False` together causes the model to produce a meaningless "à" loop with no target text — never combine both flags off.

---

## A/B Test Methodology — 6-variant diagnostic

When OmniVoice output exhibits an unexpected behavior (silent, leaked, off-topic, clipped), run all 6 variants in one script and compare Whisper transcripts. The variant that differs from `A_default` identifies the responsible flag.

Test recipe (cùng `voice_clone_prompt`, cùng `text`, cùng `language`, chỉ đổi `OmniVoiceGenerationConfig`):

```python
configs = [
    ("A_default",        OmniVoiceGenerationConfig()),
    ("B_no_denoise",     OmniVoiceGenerationConfig(denoise=False)),
    ("C_no_preprocess",  OmniVoiceGenerationConfig(preprocess_prompt=False)),
    ("D_no_postprocess", OmniVoiceGenerationConfig(postprocess_output=False)),
    ("E_no_denoise_preproc", OmniVoiceGenerationConfig(denoise=False, preprocess_prompt=False)),
    ("F_all_off",        OmniVoiceGenerationConfig(denoise=False, preprocess_prompt=False, postprocess_output=False)),
]
for label, gc in configs:
    audio = model.generate(text=TEXT, language="vi", voice_clone_prompt=prompt, generation_config=gc)[0]
    sf.write(f"{OUT}/{label}.wav", audio, model.sampling_rate)
```

Then classify each output's Whisper transcript against the target text + known ref-text phrases. The variant that fails classification reveals the responsible flag.

---

## Denoise Recipe — ffmpeg filter chain

When voice-ref audio has background noise (room tone, hiss, hum), apply this chain BEFORE saving `.pt`:

```bash
# Light denoise (default recommendation)
ffmpeg -i ref_raw.wav -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-20" \
  -ar 16000 -ac 1 -c:a pcm_s16le ref_denoised.wav

# Aggressive denoise (Telegram voice messages, noisy rooms)
ffmpeg -i ref_raw.wav -af "highpass=f=80,lowpass=f=12000,afftdn=nf=-30" \
  -ar 16000 -ac 1 -c:a pcm_s16le ref_denoised.wav
```

| Filter | Purpose | Default |
|---|---|---|
| `highpass=f=80` | Remove low-frequency rumble (HVAC, mic handling noise) | always |
| `lowpass=f=12000` | Remove high-frequency hiss (cheap mics, encode artifacts) | always |
| `afftdn=nf=-20` | FFT-based spectral denoise, noise floor -20 dB | light |
| `afftdn=nf=-25` | Medium denoise | medium |
| `afftdn=nf=-30` | Aggressive denoise (use only when ref audio is genuinely noisy) | aggressive |

**Verify after denoise:** `ref_rms` should still be ≥ 0.1 (else apply `* (0.11 / ref_rms)` amplify before saving `.pt`). If `ref_rms` drops below 0.05 after denoise, the audio is too damaged — use a different source.

---

## SHA256 Dedup Pattern

Telegram voice-message cache may store duplicate files under different filenames. Before re-processing a "new" voice message, compare hashes:

```bash
shasum -a 256 /Users/tuananh4865/.hermes/audio_cache/audio_*.ogg
```

If two files have identical SHA256, they are the same recording — pick one and skip the other. This prevents wasted encode time on duplicates and surfaces accidental gateway caching.

---

## Terminology — "voice ref" ≠ "file voice clone"

| Wrong term | Correct term | What it is |
|---|---|---|
| "voice ref" | **file voice clone** (`.pt`) | The `VoiceClonePrompt` artifact saved to `/Volumes/Storage-1/Hermes/voice-prompts/*.pt` |
| "voice ref" | ref audio (raw) | The 5-10s source audio file (wav/ogg/mp3) used to CREATE the `.pt` |

When Tuấn Anh says "use the voice ref", he means **load the `.pt` file and pass it to `model.generate(voice_clone_prompt=...)`**, NOT re-import the raw audio. The `.pt` is the cached, fast-load artifact — re-encoding raw audio every session is 5× slower.

Workflow:
1. **One-time:** raw audio → `model.create_voice_clone_prompt()` → `prompt.save("X.pt")`
2. **Every session after:** `VoiceClonePrompt.load("X.pt")` → `model.generate(text=..., voice_clone_prompt=prompt)`

---

## Invocation Pattern (when memory fact 10 fires)

When user says "tạo voice" / "clone giọng" / "voice clone" / "OmniVoice TTS", execute this sequence:

1. **Check** `/Volumes/Storage-1/Hermes/voice-prompts/` for existing `.pt` files
2. **If exists:** load + generate immediately (skip phases 3-4)
3. **If creating new:**
   - Extract 5-10s from raw audio (skip 1.5s head + 1.5s tail)
   - Apply denoise filter chain (this reference)
   - Verify `ref_rms ≥ 0.1` (amplify if needed)
   - Transcribe 2 sentences → `ref_text`
   - `save_voice_prompt.py save ref_denoised.wav "<ref_text>" <name>.pt`
4. **Generate:** `OmniVoiceGenerationConfig(pad_duration=0.0, fade_duration=0.0)` — keep `denoise=True` default
5. **Verify:** Whisper transcript clean + volumedetect peak > -10 dB
