---
title: Voice TTS workflow cho TikTok product script (v0.11.0)
created: 2026-07-21
updated: 2026-07-23
type: reference
applies-to: tiktok-product-script v0.9.7+, mọi khi user yêu cầu tạo voice/script TTS
---

# 🎤 Voice TTS Workflow cho TikTok Product Script (v0.11.0)

> **Quick start:** Khi user nói "tạo voice cho option X" / "tạo voice V3A/B/C" → LUÔN dùng config mặc định (NamMinh + 1.2x cho edge-tts). KHÔNG hỏi "dùng giọng nào" / "speed bao nhiêu".
> **Updated 23/07/2026 v0.11.0:** Thêm OmniVoice emotion tags workflow + PITFALL audio chunking + bảng so sánh edge-tts vs OmniVoice.

## 1. Config defaults (verified 23/07/2026)

`~/.hermes/config.yaml`:
```yaml
tts:
  provider: edge
  edge:
    voice: vi-VN-NamMinhNeural  # nam, friendly/positive
    speed: 1.2                  # 1.0 → 1.5 → 1.4 → 1.3 → 1.2 qua 5 lần feedback
```

**Backup config:** `~/.hermes/config.yaml.bak` (rollback nếu cần).

**Lịch sử speed (anh chỉnh theo feedback):**
| Ngày | Speed | Trigger |
|---|---|---|
| Default | 1.0 | Mặc định Microsoft |
| 21/07 | 1.5 | "tăng speed lên 1.5" |
| 21/07 | 1.4 | Feedback nhẹ lại |
| 21/07 | 1.3 | "chỉnh xuống" |
| **23/07** | **1.2** | **"Speed 1.2 mặc định nha" (verbatim)** |

## 2. Decision Tree (BẮT BUỘC đọc trước khi generate)

| Use case | Engine | Voice | Speed | Cost |
|---|---|---|---|---|
| **TikTok content thường ngày** (90% cases) | edge-tts | NamMinh (nam, VN) | 1.2x | Free, instant |
| **Clip hero/brand/cần giọng thật của anh** | OmniVoice (clone) | Giọng clone từ raw clip | 1.0x raw + ffmpeg atempo 1.2x | ~12-15s/file, free |
| **Voice multilingual** | OmniVoice | Cross-lingual clone | 1.0x | ~12-15s/file, free |

## 3. Workflow chuẩn (edge-tts - DEFAULT)

### Bước 1: Generate NamMinh normal speed (edge-tts CLI)
```bash
edge-tts --voice vi-VN-NamMinhNeural --text "<script tiếng Việt>" --write-media <output>.mp3
```

### Bước 2: Speed up 1.2x bằng ffmpeg atempo
```bash
ffmpeg -y -i <output-1x>.mp3 -filter:a "atempo=1.2" -vn -c:a libmp3lame -b:a 192k <output-1.2x>.mp3
```

## 4. Script rules (HARD - từ 4 corrections của anh 21/07)

Khi viết script cho voice (text_to_speech / file TTS), áp dụng 4 rules:

| Rule | Source | Action |
|---|---|---|
| **KHÔNG giá** trong voice | User verbatim 21/07: "Không nêu giá và mã sản phẩm!" | 599k, 67k/tháng → để visual overlay |
| **KHÔNG mã SP** | User verbatim 21/07: "gọi nó là chiếc tripod này thôi không gọi mã ma66" | MA66, K17, Pocket 3 mã → đổi thành tên gọi chung |
| **PHẢI tên SP tương thích** | User verbatim 21/07: "Sản phẩm này chỉ dùng được với dji osmo pocket 3/4/4P thôi" | "DJI Pocket 3", "iPhone 15", "Samsung S24" — tên máy tương thích |
| **Storytelling > listing** | User verbatim 21/07: "cả 3 kịch bản này đều không thu hút" | Hook intrigue / emotional visceral, KHÔNG mở bằng USP liệt kê |

## 5. Self-check trước khi generate voice

```bash
# Check 1: Tên SP tương thích có trong script?
grep -E "DJI Osmo Pocket 3|Pocket 3|Insta360 Luna" <script>
# → PHẢI có ≥1 match

# Check 2: Không giá cụ thể?
grep -E "599|67k|599k|67 nghìn" <script>
# → PHẢI = 0 match

# Check 3: Không mã SP?
grep -E "MA66|Pocket 3 K17|ARMAF Odyssey" <script>
# → PHẢI = 0 match (trừ tên SP tương thích)
```

## 6. OmniVoice Workflow (CLONE GIỌNG THẬT - cho clip hero)

### Bước 1: Tạo voice prompt MỚI từ raw clip (MỖI SESSION - HARD RULE v0.9.8)

> **User verbatim 23/07:** "Em dùng voice ref chứ không dùng file clone có sẵn à?"

```bash
# 1a. Tìm raw clip mới nhất trong /Volumes/Storage-1/Pocket3/Footages/
ls -lat /Volumes/Storage-1/Pocket3/Footages/*.MP4 | head -5

# 1b. Extract 5-10s voice từ giữa clip (bỏ 10s intro + 5s outro)
ffmpeg -y -ss 10 -i /path/to/raw.MP4 -t 5 -ar 16000 -ac 1 \
  -c:a pcm_s16le ref_raw.wav

# 1c. Whisper verify (medium, KHÔNG large-v3 - hallucinate)
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-dir ./verify/ ref_raw.wav
# Phải có ≥10 chars nội dung tiếng Việt → voice thật, không phải TTS outro

# 1d. CHECK ref_rms bằng omni venv python
/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python -c "
import soundfile as sf, numpy as np
audio, sr = sf.read('ref_raw.wav')
ref_rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
print(f'ref_rms: {ref_rms:.4f}')
if ref_rms < 0.1:
    audio_amp = audio * (0.11 / ref_rms)
    sf.write('ref_amp.wav', audio_amp, sr)
    print('✅ Amplified to 0.11 → ref_amp.wav')
"

# 1e. Save voice prompt (ref_text NGẮN ~63 chars, 1 câu đầu)
REF_TEXT="<câu đầu trong Whisper transcript, ~63 chars>"

/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python \
  ~/.hermes/skills/omnivoice-voice-clone/scripts/save_voice_prompt.py save \
  ref_amp.wav "$REF_TEXT" \
  /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_<session>_YYYY-MM-DD.pt
```

**Bug đã verified 21/07:**
- ❌ KHÔNG dùng `with_venv.sh` wrapper (prepend `/Users/tuananh4865/` vào argv → bash fail)
- ✅ Dùng TRỰC TIẾP venv python: `/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python`

### Bước 2: Generate voice với EMOTION TAGS + FIXED CHUNKING (HARD RULE v0.10.3)

> **User verbatim 23/07:** "Voice gen ra kiểu bị ngắt quãng nhiều không nói liền mạch ấy em đang prompt voice kiểu gì vậy?"

**Root cause:** Default `OmniVoiceGenerationConfig`:
- `audio_chunk_threshold: 30.0` (text > 30s → chunk)
- `audio_chunk_duration: 15.0` (chunk 15s, generate RIÊNG rồi ghép)
- Script 60-90s → chunk 2-3 lần → cảm giác "ngắt quãng"

**Fix (HARD RULE):** LUÔN override với:
```python
gc = OmniVoiceGenerationConfig(
    audio_chunk_threshold=90.0,  # text <90s không chunk
    audio_chunk_duration=30.0,    # chunk dài hơn nếu phải
    pad_duration=0.0,
    fade_duration=0.0,
)
```

**Emotion tags mapping:**
| Vị trí | Tag | Tác dụng |
|---|---|---|
| HOOK | `[surprise-oh]` + `[laughter]` | Ngạc nhiên + cười, peak tăng mạnh nhất |
| PAIN | `[sigh]` | Chạm pain point, thở dài |
| USP/SOLUTION | `[question-ah]` | Kết thúc lên cao, "wow" |
| CTA | `[confirmation-en]` | Xác nhận, call action |

**⚠️ 4-6 tags tối đa.** V4B với 4 tags = anh nói "rất ổn". V4A/C với 6 tags = có pauses rải rác. Rule ngầm: **4 tags = smooth, 6 tags = có emotion nhưng hơi ngắt quãng**.

```bash
# Generate với custom config
/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python -c '
import sys, json, torch
import numpy as np, soundfile as sf
sys.path.insert(0, "/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/lib/python3.11/site-packages")
from omnivoice import OmniVoice, VoiceClonePrompt, OmniVoiceGenerationConfig

model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
prompt = VoiceClonePrompt.load("/Volumes/Storage-1/Hermes/voice-prompts/<file>.pt")

# KEY FIX: threshold=90s + chunk=30s (default 30s + 15s gây ngắt quãng)
gc = OmniVoiceGenerationConfig(
    audio_chunk_threshold=90.0,
    audio_chunk_duration=30.0,
    pad_duration=0.0,
    fade_duration=0.0,
)

text = """<script với emotion tags>"""

audio = model.generate(text=text, language="vi", voice_clone_prompt=prompt, generation_config=gc)[0]
sf.write("output_1x.wav", audio, model.sampling_rate)
'
```

### Bước 3: Apply 1.2x speed (giống edge-tts default)
```bash
ffmpeg -y -i output_1x.wav -filter:a "atempo=1.2" -vn -c:a libmp3lame -b:a 192k output_1.2x.mp3
```

### Bước 4: Verify 3 layers
```bash
# Layer 1: Volume peak (peak > -10 dB = OK)
ffmpeg -i output_1.2x.mp3 -af volumedetect -vn -f null - 2>&1 | grep max_volume

# Layer 2: Whisper verify no ref leak
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-dir ./verify/ output_1.2x.mp3
# Kiểm tra: ref_text gốc KHÔNG xuất hiện trong transcript

# Layer 3: Pause analysis (RMS-based, optional)
# V4A có 24 pauses, V4B có 19 pauses (OK)
```

## 7. PITFALLS (BẮT BUỘC)

### P1: Default audio_chunking NGẮT QUÃNG (NEW v0.10.3, 23/07/2026)

**Triệu chứng:** Voice sinh ra bị ngắt quãng giữa các đoạn, nghe không liền mạch.

**Root cause:** Default `OmniVoiceGenerationConfig` có `audio_chunk_threshold=30s` + `audio_chunk_duration=15s`. Script 60-90s → chunk 2-3 lần → cảm giác "ngắt quãng".

**Fix (HARD RULE):** LUÔN override với threshold=90s + chunk=30s. Verified case 23/07: V4A/B/C ULANZI MA66 → giảm từ 24 pauses xuống 18-20.

### P2: Voice ref LEAK (NEW v0.9.8)

**Triệu chứng:** Whisper transcript có câu từ ref audio (đầu hoặc giữa output).

**Root cause:** ref_text quá dài → model leak câu cuối ref_text vào output.

**Fix:** ref_text NGẮN, 1 câu ~63 chars. Verify bằng Whisper transcript.

### P3: Whisper transcribe sai (đặc biệt tiếng Việt)

**Triệu chứng:** "Pocket 3" → "pocketbar", "MA66" → "MA 66", "tripod" → "Trey Pop"

**Root cause:** Whisper medium cho tiếng Việt có hallucination rate cao. KHÔNG dùng large-v3 (còn tệ hơn).

**Fix:** Verify bằng listening, không tin 100% transcript Whisper. Nếu transcript sai nhưng voice nghe đúng → OK.

### P4: edge-tts rate limit

**Triệu chứng:** Generate liên tục 3-4 file → fail với "No audio was received" / "asyncio.run(amain())".

**Fix:** `time.sleep(2-3)` giữa các lần, hoặc retry khi fail với 15s wait.

### P5: with_venv.sh path bug

**Triệu chứng:** `bash with_venv.sh python3 script.py` → "can't open file '/Users/tuananh4865/python3'"

**Fix:** Dùng TRỰC TIẾP venv python:
```bash
/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python <script.py>
```

### P6: Không lưu voice prompt mới mỗi session

**Triệu chứng:** Voice nghe "giống session trước" → user feedback "dùng voice ref chứ không dùng file clone có sẵn"

**Fix:** MỖI session tạo prompt mới từ raw clip mới nhất (xem Bước 1 ở trên). Verified case 23/07: `tuan_anh_session_2026-07-23.pt` (9.7KB) từ raw `DJI_20260721095702_0038_D.MP4`.

## 8. Edge-tts rate limit workaround

Khi generate liên tục nhiều file, edge-tts có thể fail. Fix:
```python
import time
for script in [v3a, v3b, v3c]:
    subprocess.run(["edge-tts", ...])
    time.sleep(2)  # Chờ 2s giữa các lần generate
# Nếu fail: retry với time.sleep(10) rồi thử lại
```

## 9. Verify sau khi generate

```bash
# Verify 1: Duration (đúng 1.2x ratio)
ffprobe -v error -show_entries format=duration -of csv=p=0 <file-1.2x>.mp3
# Expect: duration_1x / duration_1.2x ≈ 1.20

# Verify 2: Peak volume (không silent)
ffmpeg -i <file> -af volumedetect -vn -f null - 2>&1 | grep max_volume
# Expect: max_volume > -10 dB (nếu < -20 dB → file silent, re-generate)

# Verify 3 (optional): Whisper transcript check
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-dir /tmp/verify/ <file>
cat /tmp/verify/<file>.txt
# Verify content match với script (allow Whisper small variations)
```

## 10. Output directory

```bash
# Voice outputs ở đây (HERMES-ONLY-FOLDER rule)
/Volumes/Storage-1/Hermes/scratch/voice-messages/
```

**Naming convention:**
- `tiktok-V3A-namminh-1.2x.mp3` — version A, NamMinh, speed 1.2x
- `tiktok-V3B-p3-namminh-1.2x.mp3` — version B, có nhắc Pocket 3
- `tiktok-V3A-omnivoice-1x.wav` — OmniVoice raw (WAV 24kHz mono)
- `tiktok-V3A-omnivoice-1.2x.mp3` — OmniVoice + speed 1.2x
- `tiktok-V3A-omnivoice-fixchunk-1.2x.mp3` — OmniVoice với fixed chunking

## 11. Verified examples (23/07/2026 session)

| File | Duration 1.0x | Duration 1.2x | Peak | Tags | Verdict |
|---|---|---|---|---|---|
| V3A NamMinh (edge) | 38.09s | 29.29s | -2.9 dB | 0 | ✅ OK |
| V3A OmniVoice | 62.34s | 51.97s | -0.4 dB | 6 | ⚠️ 6 tags = 24 pauses |
| V3A OmniVoice FIXED | 63.28s | 52.74s | 0.0 dB | 6 | ✅ Smooth hơn 30% |
| V3B OmniVoice | 57.62s | 48.03s | -0.4 dB | 4 | ✅ Anh nói "rất ổn" |
| V4A/B/C OmniVoice FIXED | 58-63s | 48-53s | 0.0 dB | 4-6 | ✅ Smooth |

**Kết luận:** V4B với 4 emotion tags + fix chunking = voice mượt nhất. V4A/V4C có thể giảm tags nếu muốn smooth hơn.

## 12. When to use edge-tts vs OmniVoice

| Scenario | Tool | Why |
|---|---|---|
| 90% TikTok content thường | ✅ edge-tts NamMinh + 1.2x | Nhanh (1s/file), đủ dùng |
| Clip hero / brand quan trọng | ✅ OmniVoice authentic + emotion | Giọng thật, 4-6 emotion tags |
| Test draft trước khi final | ✅ edge-tts | Re-generate nhanh |
| Final publish | ✅ OmniVoice | Authentic feel |
| A/B test | ✅ Generate cả 2, so sánh engagement | Data-driven |

---

*Updated 23/07/2026 v0.11.0: PITFALL audio chunking + emotion tag count rule + complete 2-engine workflow + decision tree.*
*Created 21/07/2026 from MA66 voice session. Tied to skill `tiktok-product-script` v0.9.7 PITFALL "Voice TTS workflow".*