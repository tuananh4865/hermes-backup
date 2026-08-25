# 04 — Common Recipes

Task-oriented cookbook. Mỗi recipe = 1 use case + command.

---

## Recipe 1: Save voice prompt từ 5s voice message Telegram

```bash
# 1. Voice message từ Telegram → ~/.hermes/audio_cache/audio_XXXX.ogg
# 2. Extract 5s đầu
ffmpeg -y -i ~/.hermes/audio_cache/audio_XXXX.ogg \
  -t 5 -ar 16000 -ac 1 -c:a pcm_s16le /tmp/ref.wav

# 3. Verify content (Whisper)
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir /tmp/verify/ /tmp/ref.wav
cat /tmp/verify/ref.txt

# 4. Nếu ref_rms < 0.1, amplify (xem PITFALL #2)
python3 scripts/save_voice_prompt.py info <prompt.pt>  # check ref_rms

# 5. Save (ref_text NGẮN: 1 câu ~100 chars)
python3 scripts/save_voice_prompt.py save \
  /tmp/ref.wav \
  "Câu đầu tiên trong ref audio, khoảng 100 ký tự." \
  /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_v1.pt
```

---

## Recipe 2: Generate 5 segments TikTok (HOOK→CTA)

```python
# 5_texts.jsonl
cat > /tmp/5_texts.jsonl << 'EOF'
{"id": "hook",    "text": "Các bạn ơi, hôm nay mình giới thiệu một sản phẩm cực kỳ hot trên TikTok Shop.", "language": "vi"}
{"id": "problem", "text": "Nhiều anh em phản hồi là máy hút bụi cũ quá ồn, pin yếu, lại còn nặng nữa. Đúng không?", "language": "vi"}
{"id": "solution","text": "Chiếc máy hút bụi này nhỏ gọn, nhẹ tay, pin sạc nhanh, lại còn siêu êm.", "language": "vi"}
{"id": "usp",     "text": "Điểm mình thích nhất là nó có ba đầu hút khác nhau, dùng được cho mọi ngóc ngách.", "language": "vi"}
{"id": "cta",     "text": "Anh em nào thích thì bấm giỏ hàng bên dưới đi nhé. Freeship toàn quốc.", "language": "vi"}
EOF

python3 scripts/generate_voice.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_v1.pt \
  --jsonl /tmp/5_texts.jsonl \
  --output-dir /tmp/5_segments/

# Verify
python3 scripts/verify_audio.py /tmp/5_segments/

# Concat với 30ms afade
python3 scripts/concat_segments.py \
  --inputs-dir /tmp/5_segments/ \
  --output /tmp/tiktok_final.wav
```

---

## Recipe 3: Mix voice với Pocket 3 video (48kHz)

```bash
# OmniVoice output 24kHz, Pocket 3 video 48kHz
# Cần convert voice → 48kHz trước khi mix

ffmpeg -y -i voice.wav -ar 48000 -ac 2 voice_48k.wav

# Mix với video (audio của Pocket 3 thay bằng voice clone)
ffmpeg -y -i pocket3_video.mp4 -i voice_48k.wav \
  -map 0:v -map 1:a \
  -c:v copy -c:a aac -b:a 192k \
  -shortest output.mp4
```

---

## Recipe 4: Speed 1.3x (TikTok 30s từ clip 40s)

```bash
# Sau khi generate 5 segments, concat → 38s. Speed up 1.3x → 29s
ffmpeg -y -i tiktok_final.wav \
  -af "atempo=1.3" \
  -ar 24000 -ac 1 \
  tiktok_final_30s.wav
```

**Note:** Speed up 1.3x có thể làm voice nghe unnatural. Alternative: dùng `--speed 1.3` flag khi generate (giữ duration estimate tự nhiên).

---

## Recipe 5: Voice Design (không cần ref audio)

```python
# Male, British accent
import subprocess
subprocess.run([
    "python3", "/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python", "-c", '''
import torch
from omnivoice import OmniVoice
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
audio = model.generate(
    text="Hello, this is a test for voice design.",
    instruct="male, young adult, high pitch, british accent",
)
import soundfile as sf
sf.write("out.wav", audio[0], model.sampling_rate)
print("Done")
'''
])
```

**Supported attributes (xem `references/01-api-surface.md` Section Voice Design):**
- Gender: male, female
- Age: child, teenager, young adult, middle-aged, elderly
- Pitch: very low / low / moderate / high / very high pitch
- Style: whisper
- English accent: american, british, australian, canadian, indian, chinese, korean, japanese, portuguese, russian
- Chinese dialect: 河南话, 陕西话, 四川话, 贵州话, 云南话, 桂林话, 济南话, 石家庄话, 甘肃话, 宁夏话, 青岛话, 东北话

**Tip:** Kết hợp `ref_audio` + `instruct` cho Chinese dialect (cải thiện stability):
```python
audio = model.generate(
    text="你好",
    ref_audio="sichuan_sample.wav",
    instruct="四川话",
)
```

---

## Recipe 6: Cross-lingual clone (ref Vi + text En)

```python
audio = model.generate(
    text="Hello everyone, today I'm reviewing an amazing product.",
    ref_audio="vietnamese_ref.wav",   # Vietnamese
    ref_text="Xin chào...",
    language="en",                     # English text
)
# ⚠️ Accent sẽ leak (Vietnamese accent trong English output)
# Workaround: dùng voice design với "american accent" thay vì ref Vi
```

---

## Recipe 7: Auto-detect + re-amplify ref audio (batch)

```bash
# Scan tất cả raw video trong Pocket 3, tìm đoạn voice 5-10s clean
# (Em chưa viết tool này — sẽ thêm sau)
```

---

## Recipe 8: Convert 24kHz voice → 16kHz cho ESPnet/Whisper

```bash
ffmpeg -y -i voice_24k.wav -ar 16000 -ac 1 voice_16k.wav
```

---

## Recipe 9: Plot waveform + transcript alignment

```python
# Dùng torchaudio + matplotlib
import torchaudio
import matplotlib.pyplot as plt
waveform, sr = torchaudio.load("voice.wav")
plt.figure(figsize=(12, 4))
plt.plot(waveform.t().numpy())
plt.title(f"Voice clone output ({sr}Hz)")
plt.xlabel("Sample")
plt.ylabel("Amplitude")
plt.savefig("waveform.png", dpi=150)
```

---

## Recipe 10: Backup voice prompts (git commit)

```bash
cd /Volumes/Storage-1/Hermes/voice-prompts/
git init
git add *.pt
git commit -m "Voice prompts backup"
# Lưu ý: .pt files chứa voice fingerprint cá nhân — KHÔNG push lên public repo
```

---

## Recipe 11: Non-Verbal Tags — Thêm cảm xúc cho giọng

**13 non-verbal tags supported** (từ source `_NONVERBAL_PATTERN`):

| Tag | Emotion |
|---|---|
| `[laughter]` | Cười |
| `[sigh]` | Thở dài |
| `[confirmation-en]` | Xác nhận (English) |
| `[question-en]` | Câu hỏi (English intonation) |
| `[question-ah]` | Hỏi, kết thúc "à" |
| `[question-oh]` | Hỏi, kết thúc "ô" |
| `[question-ei]` | Hỏi, kết thúc "êy" |
| `[question-yi]` | Hỏi, kết thúc "ỳ" |
| `[surprise-ah]` | Ngạc nhiên, "á" |
| `[surprise-oh]` | Ngạc nhiên, "ô" |
| `[surprise-wa]` | Ngạc nhiên, "wa" |
| `[surprise-yo]` | Ngạc nhiên, "yo" |
| `[dissatisfaction-hnn]` | Không hài lòng, "hừm" |

### Test nhanh 10 emotion variants

```bash
python3 scripts/test_emotion.py \
  --prompt /Volumes/Storage-1/Hermes/voice-prompts/tuan_anh.pt \
  --out-dir ./emotion_test/
```

Output: 10 WAV files (1 baseline + 6 single-emo + 1 multi-emo + 2 cross-lingual) + volumedetect report.

### Đã verified kết quả (Mac M-series, voice prompt GOOJODOQ)

| Emotion tag | Peak | Mean | Note |
|---|---|---|---|
| Baseline | -3.7 dB | -21.4 dB | Flat |
| `[laughter]` | -3.2 dB | -18.9 dB | Voice tăng cao, vui |
| `[sigh]` | -3.2 dB | -21.0 dB | Hơi thở audible |
| `[question-ah]` | -3.1 dB | -19.2 dB | Kết thúc lên cao "à" |
| `[surprise-oh]` | -2.6 dB | **-17.6 dB** | Loudest, ngạc nhiên nhất |
| `[dissatisfaction-hnn]` | -3.0 dB | -19.6 dB | Tone phẳng, có "hừm" |
| Multi-emo (3 tags) | -2.1 dB | -18.3 dB | Emotion layering |

**Peak tăng rõ rệt khi dùng tags** (-2 to -3 dB vs -3.7 baseline) → voice thật hơn, engaging hơn.

### Recipe TikTok: Hook + CTA có emotion

```python
import torch, soundfile as sf
from omnivoice.models.omnivoice import OmniVoice, VoiceClonePrompt

model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
prompt = VoiceClonePrompt.load("/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh.pt")

# HOOK — surprise + laughter (dừng scroll)
audio_hook = model.generate(
    text="[surprise-oh] Sale SỐC hôm nay! [laughter] Giảm 50% luôn các bạn ơi!",
    language="vi",
    voice_clone_prompt=prompt,
)[0]

# PROBLEM — sigh (chạm pain point)
audio_problem = model.generate(
    text="[sigh] Bình thường máy hút bụi nặng lắm, pin yếu, lại còn ồn.",
    language="vi",
    voice_clone_prompt=prompt,
)[0]

# SOLUTION — question (engagement)
audio_solution = model.generate(
    text="Chiếc máy này thì sao[question-ah] Nhỏ gọn, êm, pin trâu, rẻ nữa!",
    language="vi",
    voice_clone_prompt=prompt,
)[0]

# CTA — confirm (call action)
audio_cta = model.generate(
    text="Bấm giỏ hàng đi anh em[confirmation-en] Freeship toàn quốc nha!",
    language="vi",
    voice_clone_prompt=prompt,
)[0]
```

### Recipe CMU Pronunciation (English fix)

```python
# Pronounce "bass" 2 cách khác nhau trong cùng câu
audio = model.generate(
    text="He plays the [B EY1 S] guitar while catching a [B AE1 S] fish.",
    language="en",
    voice_clone_prompt=prompt,
)[0]
# → "B EY1 S" = "base", "B AE1 S" = "bass" (cá)
```

### Recipe Pinyin Pronunciation (Chinese fix)

```python
audio = model.generate(
    text="这批货物打ZHE2出售后他严重SHE2本了，再也经不起ZHE1腾了。",
    language="zh",
    voice_clone_prompt=prompt,
)[0]
# → Tone numbers (1-5) override mặc định
```

### Lưu ý

1. **Tags có case-sensitive**: phải đúng `[laughter]`, không `[Laughter]`
2. **Combine nhiều tag OK**: `[laughter] vui! [sigh] buồn. [question-ah]`
3. **Vietnamese tags**: dùng `[question-ah]`, `[question-oh]`, `[surprise-oh]`, `[dissatisfaction-hnn]`
4. **English tags**: `[confirmation-en]`, `[question-en]`
5. **Không có** tag cho joy/excited specifically — dùng `[laughter]` thay thế

### Đã concat thành demo clip

`emotion_demo.wav` (~17s, max -2.1 dB) — 6 emotion variants:
- `[laughter] Cái này hay quá các bạn ơi!`
- `[sigh] Giá hơi cao nhỉ.`
- `Bạn nghĩ sao[question-ah] Mình cùng bình luận nhé.`
- `Wow[surprise-oh] Deal hời quá!`
- `[laughter] Hôm nay vui quá! [sigh] Nhưng mà giá hơi cao [question-yi]`
- `[laughter] Các bạn ơi! [surprise-oh] Hôm nay sale SỐC luôn! [question-ah] Mua không anh em?`

→ Anh có thể nghe và quyết định tags nào phù hợp voice TikTok.

---

## Quick reference: commands

| Task | Command |
|---|---|
| Save prompt | `python3 scripts/save_voice_prompt.py save <wav> "<text>" <pt>` |
| Generate 1 | `python3 scripts/generate_voice.py --prompt <pt> --text "..." --output <wav>` |
| Generate batch | `python3 scripts/generate_voice.py --prompt <pt> --jsonl <jsonl> --output-dir <dir>` |
| Verify | `python3 scripts/verify_audio.py <file_or_dir> [--whisper]` |
| Concat | `python3 scripts/concat_segments.py --inputs-dir <dir> --output <wav>` |
| Test emotion (13 non-verbal tags) | `python3 scripts/test_emotion.py --prompt <pt> --out-dir <dir>` |
| Show prompt info | `python3 scripts/save_voice_prompt.py info <pt>` |
| Mix với video | `ffmpeg -i video.mp4 -i voice_48k.wav -map 0:v -map 1:a -c:v copy -c:a aac output.mp4` |
| Speed up 1.3x | `ffmpeg -i voice.wav -af "atempo=1.3" voice_30s.wav` |
| Lower sample rate | `ffmpeg -i voice_24k.wav -ar 16000 voice_16k.wav` |
