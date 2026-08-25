# 03 — Known Issues & Workarounds

Verified v0.2.1 (commit master, 2026-07). Tracking GitHub issues.

---

## Issue #8 — MPS Batch Inference Broken (CRITICAL)

**Status:** Partially fixed (PR #13 merged)
**Severity:** High — affects all MPS users doing batch TTS

**Symptom:** `omnivoice-infer-batch` with batch_size ≥ 5 different-length texts → 4/5 outputs silent (peak -20 dB)

**Root cause:** Apple Silicon MPS backend has known issues with fully-masked attention rows in CFG path. `_generate_iterative()` builds attention mask with all-False padding rows → `softmax(-inf, -inf, ...) = NaN` on MPS → tokens corrupted → silent output.

**Patch (PR #13):**
```python
# omnivoice/models/omnivoice.py - _generate_iterative()
if max_c_len > u_len:
    pad_diag = torch.arange(u_len, max_c_len, device=self.device)
    batch_attention_mask[B + i, :, pad_diag, pad_diag] = True
```

**Status:** Patch merged, nhưng vẫn FAIL với batch ≥ 5 + text dài khác nhau (verified 23/07).

**Workarounds:**
1. **Sequential 1-by-1** (recommended) — `scripts/generate_voice.py` của skill này
2. Use `--device cpu` (slower 5-10x)
3. Wait for upstream fix (track issue #8)

**Affected versions:** 0.2.1, 0.2.0, 0.1.x

---

## Issue #10 — Apple Silicon Support Completely Broken (CLOSED as dup)

**Status:** Closed (duplicate of #8)
**Same root cause:** MPS corruption with voice clone

---

## Issue #139 — Output Sounds "Muffled"

**Status:** Open, by-design
**Severity:** Low — quality perception

**Symptom:** Generated audio sounds slightly muffled, especially consonants. 24kHz sample rate → Nyquist 12kHz → missing high-freq harmonics above 8kHz.

**Workarounds:**
1. EQ boost 8-12kHz trong audio editor (Audacity/Logic)
2. Use neural audio super-resolution (AudioSR) to upsample 24kHz → 48kHz
3. Accept limitation — OmniVoice intentionally trained on 24kHz data

**Quote (model author):**
> "We adopted the 24 kHz sampling rate because we lack a large amount of training data with higher sampling rates, and 24 kHz is actually the default choice for most TTS systems."

---

## Issue #180 — ASR model cannot be moved off default GPU (FIXED in current code)

**Status:** Fixed in current main (commit e3439e3)
**Symptom:** `model.load_asr_model()` ignores `asr_device` arg, loads ASR on default GPU

**Fix:** Use `device=` instead of `device_map=` in pipeline():
```python
self._asr_pipe = hf_pipeline(
    "automatic-speech-recognition",
    model=model_name,
    dtype=asr_dtype,
    device=device,    # ← single-device placement
)
```

---

## Issue — TikTok Watermark Audio (not OmniVoice specific)

**Status:** yt-dlp limitation
**Severity:** Medium — affects voice clone ref sourcing

**Symptom:** Download TikTok clip via `yt-dlp -f audio_best` → only get watermark/outro track, NOT original voice.

**Workarounds:**
1. Send voice message directly via Telegram (5-10s)
2. Record fresh voice audio
3. Use `yt-dlp` with `--cookies` to authenticate (TikTok private)
4. Try `snaptik` or `savefrom` services

**Verify before use:**
```bash
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir /tmp/check/ ref.wav
cat /tmp/check/ref.txt
# Phải có NỘI DUNG review, không phải "subscribe" lặp
```

---

## Issue — HiggsAudioV2Tokenizer MPS crash (HANDLED)

**Status:** Auto-handled in code
**Severity:** None (no user action needed)

**Symptom:** Model load crash on MPS with "output channels > 65536"

**Fix (line 484 in `from_pretrained`):**
```python
tokenizer_device = (
    "cpu" if str(model.device).startswith("mps") else model.device
)
```

→ Audio tokenizer always on CPU on MPS. **Trade-off:** slight CPU↔MPS data transfer overhead, but stable.

---

## Issue — Pyannote/s3prl dependencies for eval (NOT relevant for inference)

**Optional dep:** `pip install "omnivoice[eval]"` for WER/MOS/speaker-similarity metrics
**Includes:** jiwer, s3prl, funasr, zhconv, zhon, unidecode

Chỉ cần cho training/evaluation, KHÔNG cần cho inference.

---

## Issue — flash_attn not on XPU (HANDLED)

**Status:** Auto-fallback
**Affected:** Intel Arc GPU users

**Symptom:** `flash_attn` not available on XPU
**Fix:** Model auto-falls back to SDPA on XPU

---

## Tracking: Upstream Issues

| Issue | Title | Status | Affects skill? |
|---|---|---|---|
| #8 | MPS batch broken | Partial fix (PR #13) | YES — workaround via sequential |
| #10 | Apple Silicon broken | Closed (dup #8) | Same as #8 |
| #139 | Output muffled | Open, by-design | NO — quality limitation |
| #180 | ASR device | Fixed | NO |

**New issues to watch:**
- MPS iterative unmasking corruption (root cause of #8) — may need more patches
- Long-form generation VRAM spikes (unconfirmed)
