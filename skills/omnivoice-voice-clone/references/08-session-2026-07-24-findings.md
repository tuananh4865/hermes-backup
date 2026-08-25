# Pitfall #9 — denoise flag prevents ref-text echo (CRITICAL, 24/07)

**Symptom:** Output bắt đầu bằng câu/đoạn ref text echo trước khi đến target text. Whisper sẽ catch cụm từ đầu giống ref text.

**Root cause:** `OmniVoiceGenerationConfig.denoise` flag controls prepend `<|denoise|>` token. Khi CÓ token → model skip echo ref text. Khi KHÔNG có → model conditioning bị lệch, output bắt đầu bằng ref text echo.

**Verified 24/07 (6-variant A/B test):**
| Flag | Output start | Verdict |
|---|---|---|
| `denoise=True` (default) | target text only | ✅ CLEAN |
| `denoise=False` | "ref text echo" + target text | ❌ LEAK |
| `preprocess_prompt=False` | target text (1-2 từ echo nhỏ OK) | ✅ acceptable |
| `postprocess_output=False` | target text | ✅ acceptable |
| `denoise=False + preprocess_prompt=False` | "à à à..." loop | ❌ NO TARGET |
| `denoise=False + preprocess_prompt=False + postprocess_output=False` | echo + target | ❌ LEAK |

**Anti-pattern:**
```python
# ❌ SAI — leak ref text
gc = OmniVoiceGenerationConfig(denoise=False)

# ✅ ĐÚNG — keep default
gc = OmniVoiceGenerationConfig()  # denoise=True implicit
# OR explicit:
gc = OmniVoiceGenerationConfig(
    denoise=True,
    preprocess_prompt=True,
    postprocess_output=True,
)
```

**Cross-reference:** Section "When to use" in SKILL.md docs MUST never recommend `denoise=False`. Default config has 3 layers of safety (denoise + preprocess + postprocess) — leave all on.

---

# Pitfall #8 — Repeated-phrase ref audio causes leak (24/07)

**Symptom:** Output có cụm từ xuất hiện nhiều lần trong target text, hoặc output echo cả 1 cụm dài từ ref audio.

**Root cause:** Voice ref audio có 1 cụm từ lặp lại 5+ lần (vd "Xin chào tôi là Tuấn Anh đây" × 5). Model học cụm đó as primary phrase, dễ leak vào output.

**Verified 24/07:**
- Ref audio "Xin chào tôi là Tuấn Anh đây" × 5 → output luôn có leak cụm này ở các segment khác nhau
- Ref audio 3-4 câu KHÁC NHAU (vd hỏi game, giới thiệu, kết thúc) → output sạch, không leak

**Anti-pattern:**
```python
# ❌ SAI — ref audio 1 cụm lặp 5 lần
ref_audio = "xin_chao_toi_la_tuan_anh_5x.ogg"

# ✅ ĐÚNG — ref audio 3-5 câu khác nhau
ref_audio = "voice_msg_3_questions.ogg"  # 3 câu hỏi khác nhau
```

**Lưu ý:** Nếu user CỐ Ý ghi nhiều lần 1 cụm để thể hiện emotion range (24/07 confirmed) → vẫn leak cụm đó, nhưng model capture emotion range tốt hơn. Workaround: dùng emotion tags + instruct để đè, hoặc yêu cầu user ghi lại với nhiều câu KHÁC NHAU.

---

# Pitfall #10 — Test script must differ from ref text (24/07)

**Symptom:** Khi test voice clone output, dùng chính ref text làm test input → kết quả WHISPER transcript giống với ref text, không biết clone có work hay không.

**Root cause:** Test scope sai. Ref text đã được encode trong .pt file. Test phải dùng text MỚI hoàn toàn để verify clone có generalize được.

**Anti-pattern:**
```python
# ❌ SAI — test với text giống ref (ref_text đã có trong .pt)
ref_text = "Xin chào, tôi là Tuấn Anh đây"
test_text = "Xin chào, tôi là Tuấn Anh đây"  # WHISPER = pass giả

# ✅ ĐÚNG — test với text KHÁC hoàn toàn
ref_text = "Xin chào, tôi là Tuấn Anh đây"
test_text = "Hôm nay mình sẽ chia sẻ về cách sử dụng OmniVoice"  # WHISPER = pass thật
```

**Workaround:** Sau khi save .pt, test ngay với 1-2 câu test script ĐÃ CHUẨN BỊ TRƯỚC, không phải text có sẵn.

---

# Pitfall #11 — Amplify without clipping (24/07)

**Symptom:** Ref audio có rms < 0.1 (theo Pitfall #2 rule phải amplify), nhưng amplify quá peak > 1.0 → audio clip, distortion.

**Verified 24/07:** Pure 0.11/rms scale có thể push peak > 1.0 (vd rms=0.0719 × 1.53 = peak 1.33).

**Fix:** Scale = min(0.11/rms, 0.95/peak) — chọn min để hit BOTH rms≥0.1 AND peak≤0.95.

```python
import soundfile as sf
import numpy as np

audio, sr = sf.read("ref.wav")
rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
peak = np.abs(audio).max()

# Clip-safe amplify
scale = min(0.11 / rms, 0.95 / peak)
audio_amp = audio * scale
sf.write("ref_amp.wav", audio_amp, sr)

# Verify
new_rms = np.sqrt(np.mean(audio_amp.astype(np.float32)**2))
new_peak = np.abs(audio_amp).max()
assert new_rms >= 0.1, f"rms too low: {new_rms}"
assert new_peak <= 0.95, f"peak too high: {new_peak}"
```

**Note:** Nếu rms vẫn < 0.1 sau cả 2 limit → chấp nhận rms thấp, KHÔNG clip. Script save_voice_prompt.py sẽ warn nhưng vẫn tạo .pt.
