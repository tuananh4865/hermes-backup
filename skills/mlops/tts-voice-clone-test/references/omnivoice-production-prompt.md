# OmniVoice Production Voice Clone — Reference

**Date:** 2026-07-23 19:53 (verified on Mac M-series MPS)
**OmniVoice version:** 0.2.1
**Use case:** TikTok voice clone production — generate N files cùng voice anh nhanh nhất có thể.

## Tại sao VoiceClonePrompt?

**Problem:** Gọi `model.generate(ref_audio=..., ref_text=...)` MỖI LẦN → model phải:
1. Load ref audio
2. Encode audio tokens (~3-5s)
3. Whisper ASR (nếu ref_text=None)
4. Tokenize ref_text
→ Mất ~7-10s overhead/file

**Solution:** `VoiceClonePrompt` encode 1 LẦN, save `.pt`, load lại gần như instant (0.00s).

## Full pipeline (5 bước)

### Step 1 — Ref audio prep (1 lần, ~30s)

```bash
# 1.1 Extract 5-10s từ video/voice (peak voice, no intro/outro)
ffmpeg -y -ss <start> -i source.mov -t <duration> \
  -ar 16000 -ac 1 -c:a pcm_s16le ref_raw.wav

# 1.2 Whisper transcribe (RAW, không cleanup)
mlx_whisper --model mlx-community/whisper-large-v3-mlx \
  --language vi --output-format txt \
  --output-dir . ref_raw.wav
# Output: ref_raw.txt — chính xác transcript
```

### Step 2 — Amplify ref_rms > 0.1 (CRITICAL)

```python
import soundfile as sf, numpy as np
import torchaudio

audio, sr = sf.read("ref_raw.wav")
ref_rms_orig = np.sqrt(np.mean(audio.astype(np.float32) ** 2))
print(f"ref_rms orig: {ref_rms_orig:.4f}")

# Target = 0.11 (sweet spot vừa trên threshold 0.1)
target_rms = 0.11
amp = target_rms / ref_rms_orig
print(f"amp: {amp:.3f}")

audio_amp = audio * amp
peak = np.abs(audio_amp).max()
print(f"peak after amp: {peak:.4f} ({'CLIP' if peak > 1.0 else 'OK'})")

sf.write("ref_amp.wav", audio_amp, sr, subtype='PCM_16')

# Verify
wav, _ = torchaudio.load("ref_amp.wav")
ref_rms_new = torch.sqrt(torch.mean(wav.float() ** 2)).item()
print(f"ref_rms new: {ref_rms_new:.4f} ({'PASS' if 0.10 < ref_rms_new < 0.20 else 'FAIL'})")
```

**Expected output:** `amp: ~1.8-2.5`, `ref_rms new: 0.11`, `peak: 0.8-0.95` (no clip).

### Step 3 — Trim ref_text xuống 2 câu đầu (CRITICAL)

```python
# Edit ref_raw.txt — chỉ GIỮ 2 câu đầu của ref audio
# Sweet spot: 77-99 chars, ~10s đầu ref audio
ref_text_short = "Các bạn nào bây giờ đi cà phê mà còn cầm theo những cái cục sạc dừa phòng to và nặng như thế này á, thì hãy dẹp ngay đi nha. Dạo này thì mình có tìm hiểu được cái cục sạc dừa phòng này."
print(f"ref_text len: {len(ref_text_short)} chars")
```

**Sweet spot: 2 câu đầu, KHÔNG dùng full transcript.**

### Step 4 — Save prompt (.pt, 1 lần duy nhất)

```python
import torch
import sys
sys.path.insert(0, "/path/to/.venv/lib/python3.11/site-packages")

from omnivoice.models.omnivoice import OmniVoice

print("Loading model...")
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)

print("Creating voice clone prompt...")
prompt = model.create_voice_clone_prompt(
    ref_audio="ref_amp.wav",
    ref_text=ref_text_short,
    preprocess_prompt=True,
)
print(f"  ref_rms: {prompt.ref_rms:.4f}")
print(f"  ref_audio_tokens shape: {prompt.ref_audio_tokens.shape}")

prompt_path = "/Volumes/Storage-1/Hermes/voice-prompts/<name>.pt"
prompt.save(prompt_path)
print(f"✅ Saved {prompt_path} ({os.path.getsize(prompt_path) / 1024:.1f}KB)")
```

**Output:** `.pt` file ~10-15KB chứa `ref_audio_tokens` (8, T) tensor + ref_text + ref_rms.

### Step 5 — Mỗi lần generate (load + run)

```python
import torch
from omnivoice.models.omnivoice import OmniVoice, VoiceClonePrompt

print("Loading model...")
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)

print("Loading voice prompt...")
prompt = VoiceClonePrompt.load("/Volumes/Storage-1/Hermes/voice-prompts/<name>.pt")
# 0.00s — instant load từ .pt cache

# Generate target text
audio = model.generate(
    text="<target text>",
    language="vi",
    voice_clone_prompt=prompt,  # ← skip re-encode
)
sf.write("out.wav", audio[0], model.sampling_rate)
```

## Speed benchmark (verified 23/07 trên Mac M-series, 5 file)

| Workflow | Time/file | Cache |
|---|---|---|
| `ref_audio` + `ref_text` mỗi lần | ~18s | None |
| `voice_clone_prompt` (load .pt) | **~11s** | -40% |
| Model đã cached (no cold start) | ~11s | -1:30 |

**Wall time cho 5 file TikTok:** 1:30 (cold start) + 55s (5×11s) = ~2:30.

## Production file structure (HERMES-ONLY-FOLDER)

```
/Volumes/Storage-1/Hermes/
├── voice-prompts/                         # ← VoiceClonePrompt .pt files
│   ├── tuananh_review_goojodoq_5s.pt     # 10KB
│   ├── tuananh_review_body_mist.pt       # 10KB
│   └── tuananh_review_tripod.pt          # 10KB
└── scratch/
    └── tuananh-tiktok-voice-test/         # outputs per project
        ├── PLAN.md
        ├── ref_amp.wav
        ├── out_test_*.wav
        └── tiktok_FINAL.wav
```

## 2 critical workarounds (must do)

### 1. `ref_rms > 0.1` (BYPASS amplitude bug)

```python
# Line 898-903 of models/omnivoice.py (v0.2.1):
if ref_rms is not None and ref_rms < 0.1:
    generated_audio = generated_audio * ref_rms / 0.1
```

Nếu ref_rms < 0.1 → output scale xuống → gần silent (-20dB). Amplify ref để bypass:

```python
target_rms = 0.11  # sweet spot
audio_amp = audio * (target_rms / ref_rms_orig)
```

### 2. `ref_text ≤ 2 câu đầu` (BYPASS ref leak)

```python
# Model luôn inject câu cuối ref_text vào output.
# Full transcript (17s) → output có leak câu cuối ở đầu/giữa.
# 2 câu đầu (~10s, ~100 chars) → output sạch.
```

## 3-layer verify (BẮT BUỘC trước khi ship)

```python
import subprocess

# Layer 1: file valid
out = subprocess.check_output(["ffprobe", "-v", "error",
    "-show_entries", "stream=codec_name,sample_rate,channels,duration",
    "-of", "csv=p=0", "out.wav"]).decode()
assert "pcm_s16le" in out and "24000" in out

# Layer 2: amplitude (peak > -10dB)
amp = subprocess.run(["ffmpeg", "-i", "out.wav", "-af", "volumedetect",
    "-vn", "-f", "null", "-"], capture_output=True).stderr.decode()
peak_db = float(amp.split("max_volume: ")[1].split(" dB")[0])
assert peak_db > -10, f"audio too quiet: {peak_db} dB"

# Layer 3: content (no ref leak, expected text present)
subprocess.run(["mlx_whisper", "--model", "mlx-community/whisper-large-v3-mlx",
    "--language", "vi", "--output-format", "json",
    "--word-timestamps", "True",
    "--output-dir", "/tmp/check/", "out.wav"])
data = json.load(open("/tmp/check/out.json"))

# Check NO ref leak
ref_words = set(ref_text_short.lower().split())
for seg in data.get("segments", []):
    for w in seg.get("words", []):
        wt = w.get("word", "").lower().strip(".,!?")
        assert wt not in ref_words, f"REF LEAK: '{wt}'"

# Check expected text CÓ mặt
transcript = " ".join(s.get("text", "") for s in data.get("segments", []))
assert expected_target_phrase in transcript.lower(), f"missing: '{expected_target_phrase}'"

print("✅ 3-layer PASS")
```

## Anti-patterns (em đã mắc trong session này)

1. **❌ Chạy thẳng `ref_audio + ref_text` cho N file** — bỏ qua `voice_clone_prompt` API, mất 40% speed. User phải correct: *"Khoan, em import hết âm thanh này vào omnivoice để tạo template voice clone thôi"*.

2. **❌ Dùng ref_text full transcript (122 chars, 3 câu)** — gây ref leak, output có câu cuối ở đầu. Sweet spot = 2 câu đầu (~100 chars).

3. **❌ Không amplify ref audio** — ref_rms = 0.06 (natural) trigger bug line 898-903, output -20dB. PHẢI amp để ref_rms = 0.11.

4. **❌ Verify chỉ bằng ffprobe file size/duration** — đó là container check, không phải content check. PHẢI 3-layer (file + amplitude + Whisper transcript).

5. **❌ Trust user-provided ref text thay vì Whisper transcript** — Khi user cung cấp file audio + gõ text khác nhau, LUÔN dùng Whisper (audio = source of truth). Real case 23/07: user gõ "dọng độc của Tung Anh... 30 tụi đang thức nghiệp" (sai chính tả) nhưng audio đúng.

## Verbatim user feedback (embed này vào memory + skill)

> "Khoan, em import hết âm thanh này vào omnivoice để tạo template voice clone thôi chứ đâu cần lần nào cũng phải import lại âm thanh đâu" — Tuấn Anh, 23/07/2026 19:46

**Lesson: KHÔNG bao giờ assume user muốn re-encode mỗi lần. KHI user nói "dùng voice này cho N file" → check `voice_clone_prompt`/cache API TRƯỚC khi loop.**
