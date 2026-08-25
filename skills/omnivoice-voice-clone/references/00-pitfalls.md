# 00 — Critical Pitfalls (ĐÃ VERIFY, PHẢI ĐỌC TRƯỚC KHI DÙNG)

5 bug em catch được trong session test OmniVoice 23/07. Mỗi bug đều có fix cụ thể + verified.

---

## Pitfall #1 — MPS Batch Bug (CRITICAL)

**Symptom:** Khi dùng `omnivoice-infer-batch` với batch ≥5 texts có độ dài khác nhau, 4/5 file output gần silent (peak -20.8 dB thay vì 0 dB).

**Root cause:** GitHub issue #8 — MPS backend xử lý padding rows trong `_generate_iterative()` gây NaN trong attention. Patch `pad_diag` (PR #13) merge rồi nhưng chỉ fix partial.

**Repro:**
```python
# BUG: 4/5 silent
audio = model.generate(
    text=[t1, t2, t3, t4, t5],   # 5 different-length texts
    language=["vi"]*5,
    ref_audio=["ref.wav"]*5,
    ref_text=[...] * 5,
)
# Audio 1-3, 5: peak 0.15 (silent)
# Audio 4: peak 1.00 (OK)
```

**Fix:** Sequential 1-by-1 trong cùng process (model load 1 lần):
```python
for text in texts:
    audio = model.generate(text=text, voice_clone_prompt=prompt)[0]
    sf.write(f"{id}.wav", audio, model.sampling_rate)
```

**Performance:** Sequential 5 file = ~70s, Batch CLI = ~115s. **Sequential NHANH HƠN và KHÔNG BUG.**

---

## Pitfall #2 — Amplitude Bug (ref_rms < 0.1)

**Symptom:** Output audio bị giảm 1/6 amplitude so với baseline (-20 dB thay vì -5 dB).

**Root cause:** Line 898-903 trong `_post_process_audio`:
```python
if ref_rms is not None and ref_rms < 0.1:
    generated_audio = generated_audio * ref_rms / 0.1   # ← BUG: scale DOWN
```

**Khi nào trigger:** Voice audio thu trong quiet environment có `ref_rms` thường < 0.1.

**Fix:** Amplify ref audio trước khi save prompt:
```python
import soundfile as sf, numpy as np
audio, sr = sf.read("ref.wav")
ref_rms = np.sqrt(np.mean(audio.astype(np.float32)**2))
if ref_rms < 0.1:
    audio_amp = audio * (0.11 / ref_rms)
    sf.write("ref_amp.wav", audio_amp, sr)
```

**Verify:** Sau amplify, output peak = 0.45-0.87 (bình thường) thay vì 0.09-0.15 (silent).

---

## Pitfall #3 — Ref Text Leak (CRITICAL cho prompt)

**Symptom:** Output LUÔN leak câu cuối của `ref_text` vào đầu/giữa output, bất kể flags `denoise` hay `preprocess_prompt`.

**Repro:**
```python
ref_text = "Câu 1. Câu 2. Câu 3."  # 3 câu
audio = model.generate(text="Target text", ref_audio="ref.wav", ref_text=ref_text)
# Output Whisper: "Câu 3. Target text"   ← Câu 3 bị leak!
```

**Test matrix:**
| ref_text | Output | Verdict |
|---|---|---|
| Full 17s (3 câu, 122 chars) | "Câu 3 leak" | ❌ FAIL |
| 1 câu (39 chars) | Text lặp 2 lần | ⚠️ |
| **2 câu (77 chars)** | **Output sạch** | ✅ BEST |
| "Xin chào." (9 chars) | Model rác 71s | ❌ |

**Fix:** `ref_text` chỉ giữ 1-2 câu đầu (~100 chars). KHÔNG dùng full transcript.

```python
ref_text = "Câu đầu tiên trong ref audio, khoảng 100 ký tự."  # 1 câu, 100 chars
```

---

## Pitfall #4 — TikTok CDN Trả Audio Khác Expected

**Symptom:** Download clip TikTok qua `yt-dlp` → chỉ có voice outro "subscribe" lặp đi lặp lại, KHÔNG phải voice review.

**Repro:**
```bash
yt-dlp -f audio_best "https://vt.tiktok.com/ZSXGsWrMr/"
# → 192s audio, Whisper: "Hãy subscribe cho kênh Ghiền Mì Gõ" lặp 7 lần
# → Không có voice review thật
```

**Root cause:** TikTok CDN tách audio track watermark, hoặc link TikTok bị expired/private.

**Fix:** Luôn verify audio content trước khi dùng làm ref:
```bash
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir /tmp/check/ ref.wav
cat /tmp/check/ref.txt
# Phải có NỘI DUNG review thật, KHÔNG phải "subscribe" lặp
```

**Khi nghi ngờ:** Dùng voice message Telegram 5-10s thay vì link TikTok.

---

## Pitfall #5 — HiggsAudioV2Tokenizer Không Support MPS

**Symptom:** Model load bị crash trên MPS với error "output channels > 65536".

**Fix:** Code đã handle tự động — line 484 trong `from_pretrained`:
```python
tokenizer_device = "cpu" if str(model.device).startswith("mps") else model.device
```

→ Audio tokenizer load trên CPU ngay cả khi main model ở MPS. Verified OK, không cần fix gì.

---

## Bug Interdependencies (quan trọng)

| Bug | Trigger | Cần fix # | Cần fix # |
|---|---|---|---|
| Silent output (peak < -10 dB) | 1, 2, hoặc cả 2 | - | - |
| Ref leak | ref_text > 1 câu | 3 | - |
| Batch silent | batch_size ≥ 5 | 1 | - |
| Whisper hallucinate loop | ref audio < 5s hoặc silent | 4 | - |

**Verify protocol (BẮT BUỘC mỗi lần generate):**
```bash
# Layer 1: file valid
ffprobe -show_entries format=duration:stream=codec_name,sample_rate,channels out.wav
# Expect: pcm_s16le, 24000Hz, mono

# Layer 2: amplitude
ffmpeg -i out.wav -af volumedetect -vn -f null - 2>&1 | grep max_volume
# Expect: max_volume > -10 dB (peak > 0.3)

# Layer 3: content clean (nếu nghi ngờ)
mlx_whisper --model mlx-community/whisper-large-v3-mlx --language vi \
  --output-format txt --output-dir /tmp/verify/ out.wav
cat /tmp/verify/out.txt
# Expect: chỉ chứa target text, KHÔNG ref audio leak
```

---

## Lessons Codified

1. **Test variants trước khi conclude** — A/B/C/D matrix saves hours debugging
2. **Whisper word-level = ground truth** verify voice clone output
3. **Amplitude check BẮT BUỘC** — không tin `duration`+`size` alone
4. **Sequential > batch** trên MPS (counter-intuitive nhưng true)
5. **Anh hiểu model behavior hơn em** — listen to user hints

---

## Pitfall #6 — Concat Gap (ĐÃ FIX bằng generate-time config)

**Symptom (cũ):** Khi concat N file OmniVoice → clip có gap silent 100-200ms giữa các segment.

**Root cause:** OmniVoice mặc định thêm `pad_duration=0.1` (100ms) silence đầu + cuối mỗi output.

**❌ Fix sai #1 (afade in+out 30ms):** Tạo 60ms silent gap, peak audio ở boundary = 0 → nghe bị ngắt quãng.

**❌ Fix sai #2 (trim 100ms + fade out):** Workaround tốt nhưng vẫn có 30ms fade → voice bị fade out rồi vào ngay voice mới (hơi cụt).

**✅ Fix đúng (anh correct em 23/07):** Disable padding NGAY TỪ GENERATE:
```python
from omnivoice import OmniVoiceGenerationConfig
gc = OmniVoiceGenerationConfig(pad_duration=0.0, fade_duration=0.0)
audio = model.generate(text=text, voice_clone_prompt=prompt, generation_config=gc)
```

→ Audio segments **không có lead/trail silence**, voice bắt đầu ngay sample 0. Concat thẳng là mượt, KHÔNG cần trim/fade gì cả.

**Verified (Mac M-series, 5 segments GOOJODOQ):**

| Method | Boundary peak | First active audio | Last active audio | Whisper hallucinate? |
|---|---|---|---|---|
| afade in+out (cũ) | 0.00 | 104ms | 130ms | "tuần" → "tuổi" |
| trim + fade out | 0.03-0.11 | 0ms (after trim) | 30ms | OK |
| **NO PADDING (đúng)** | **0.65-0.77** | **0ms** | **0-31ms** | **OK + clean** |

**Updated PITFALL #81:** Khi concat audio TTS, **disable padding ngay từ generate** (`pad_duration=0`), KHÔNG BAO GIỜ trim/fade sau.
