# TTS Voice Workflow cho script TikTok (Vietnamese)

> **Source session:** 2026-07-23 (ULANZI MA66 V4 voice generation)
> **Status:** Reference cho TTS generation pipeline

## Khi nào dùng TTS

| Use case | Tool | Lý do |
|---|---|---|
| TikTok content authentic (giọng thật của anh) | **OmniVoice** clone | Voice authentic, 13 emotion tags |
| Quick test/demo, không cần voice thật | **edge-tts NamMinh** | Nhanh 12x, Microsoft voice OK |
| Voice thật + emotion mạnh | **OmniVoice** + emotion tags | Peak -2 dB (to hơn baseline) |

## Default config (updated 23/07)

**~/.hermes/config.yaml:**
```yaml
tts:
  provider: edge
  edge:
    voice: vi-VN-NamMinhNeural
    speed: 1.2  # Default 1.2x từ 23/07
```

**Lịch sử speed (anh chỉnh qua các session):**
| Ngày | Speed | Lý do |
|---|---|---|
| Default | 1.0 | Mặc định edge-tts |
| 21/07 | 1.5 | Lần đầu anh tăng |
| 21/07 | 1.4 | Anh chỉnh xuống |
| 21/07 | 1.3 | Anh chỉnh xuống tiếp |
| **23/07** | **1.2** | **Default vĩnh viễn** |

⚠️ Speed này **CHỈ áp dụng cho edge-tts**, KHÔNG áp dụng cho OmniVoice. OmniVoice tạo 1.0x raw, sau đó dùng ffmpeg atempo=1.2 riêng.

## Workflow OmniVoice cho script TikTok

### Bước 1: Lấy ref audio mới (BẮT BUỘC)
**Anh feedback 23/07 (verbatim):** *"Em dùng voice ref chứ không dùng file clone có sẵn à?"*

**Rule (FIRST-CLASS):**
- ❌ KHÔNG dùng file prompt cũ (`.pt` từ session trước)
- ✅ Mỗi session = 1 voice prompt MỚI từ raw clip mới nhất của anh

**Tìm raw clip mới nhất:**
```bash
# Scan Footages/ tìm file mới nhất
ls -t /Volumes/Storage-1/Pocket3/Footages/DJI_*.MP4 | head -1
```

**Extract 5-10s voice:**
```bash
ffmpeg -y -ss 10 -i <raw_clip.MP4> -t 5 \
  -ar 16000 -ac 1 -c:a pcm_s16le ref_5s.wav
```

### Bước 2: CHECK ref_rms (BẮT BUỘC)
```python
import soundfile as sf, numpy as np
audio, sr = sf.read('ref_5s.wav')
ref_rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
if ref_rms < 0.1:
    # Amplify lên 0.11
    audio_amp = audio * (0.11 / ref_rms)
    sf.write('ref_5s_amp.wav', audio_amp, sr)
```

**Ref audio tiếng Việt thường có ref_rms 0.05-0.08** → LUÔN amplify.

### Bước 3: Save voice prompt
```bash
# Direct venv python (không qua bash wrapper - vì wrapper bị lỗi)
/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python \
  /Users/tuananh4865/.hermes/skills/omnivoice-voice-clone/scripts/save_voice_prompt.py \
  save ref_5s_amp.wav \
  "Câu đầu tiên trong ref audio, khoảng 60-100 ký tự" \
  /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_session_YYYY-MM-DD.pt
```

**Ref_text rules:**
- ~60-100 chars (1 câu đầu tiên)
- KHÔNG full transcript (sẽ leak câu cuối)
- Dùng câu tự nhiên, không phải text công thức

### Bước 4: Generate voice với emotion tags
```bash
python3 /Users/tuananh4865/.hermes/skills/omnivoice-voice-clone/scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_session_YYYY-MM-DD.pt \
  --text "[surprise-oh] [laughter] Hook ngạc nhiên. [sigh] Pain point. [question-ah] Solution reveal. [confirmation-en] CTA" \
  --output /Volumes/Storage-1/Hermes/scratch/voice-messages/output-1x.wav
```

**13 emotion tags verified (từ `references/test_emotion.py`):**
- `[surprise-oh]` - loudest hook (-2 to -3 dB)
- `[laughter]` - vui vẻ
- `[sigh]` - chạm pain point
- `[question-ah]` - kết thúc lên cao
- `[confirmation-en]` - call action
- (xem `references/04-recipes.md` Recipe 11 cho full list)

### Bước 5: Speed 1.2x + verify
```bash
# Apply 1.2x speed
ffmpeg -y -i output-1x.wav \
  -filter:a "atempo=1.2" \
  -vn -c:a libmp3lame -b:a 192k \
  output-1.2x.mp3

# Verify (3 layers - BẮT BUỘC)
ffmpeg -i output-1.2x.mp3 -af volumedetect -vn -f null - 2>&1 | grep max_volume
# Expect: max_volume > -10 dB

mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-dir /tmp/verify/ output-1.2x.mp3
cat /tmp/verify/*.txt
# Expect: 
# 1. No ref leak (không có câu ref audio)
# 2. Content khớp script đã generate
```

### Bước 6: Edge-tts cho quick test
```bash
# Speed 1.2x auto từ config
edge-tts --voice vi-VN-NamMinhNeural \
  --text "Script test" \
  --write-media test.mp3
```

## Output location convention

```
/Volumes/Storage-1/Hermes/voice-prompts/         # Voice prompts (.pt) - HERMES-ONLY
/Volumes/Storage-1/Hermes/scratch/voice-messages/ # Generated audio (MP3/WAV)
```

**KHÔNG** save ở `/Users/tuananh4865/` (vi phạm HERMES-ONLY-FOLDER rule).

## Common issues & fixes

| Issue | Fix |
|---|---|
| `ModuleNotFoundError: omnivoice` | Dùng trực tiếp venv python: `/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python` |
| `with_venv.sh` broken (`can't open file 'python3'`) | Skip wrapper, gọi venv python trực tiếp |
| `edge-tts` rate limit (fail 2-3 lần liên tiếp) | Wait 15s, retry single text |
| Ref audio silent/quiet | ref_rms < 0.1 → amplify lên 0.11 |
| Whisper medium transcribe sai tiếng Việt | Verify peak volume trước (> -10 dB), check transcript đủ rõ |

## Performance (Mac M-series, 23/07)

- Model load (warm): ~2-3s
- Save voice prompt: ~5s
- Generate 18s audio (with emotion tags): ~40s
- Whisper verify: ~5-10s

## Related files

- `references/00-pitfalls.md` - 6 pitfalls đã verify (ref_rms, MPS batch, ref leak, etc.)
- `references/04-recipes.md` - Recipe 11: emotion tags + TikTok engagement
- `wiki/concepts/voice-script-product-context-2026-07-21.md` - Lesson nhắc Pocket 3

## Verified case (23/07)

ULANZI MA66 V3A voice generation:
- Ref audio: raw clip 0038 (21/07) → 5s extracted → amplify (ref_rms 0.0571 → 0.11)
- Voice prompt: `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_session_2026-07-23.pt` (9.7KB)
- Output: `/Volumes/Storage-1/Hermes/scratch/voice-messages/tiktok-V3A-newref-1.3x.mp3` (798KB · 40.79s · peak -0.4 dB)
- Whisper verify: ✅ no ref leak, content đầy đủ theo script