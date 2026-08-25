# Pitfall: Trailing Vowel Repeat vs Ellipsis (`…`)

**Discovered:** 2026-07-26 by Tuấn Anh feedback (verbatim, real use case VXgN3KtMt0M).

---

## 🚨 ROOT CAUSE: "Tộiiiiiiii" → "goalllll"

### Anh dạy (verbatim 26/07/2026):

> **"tội là câu cảm thán kiểu thở dài thấy thương đồ á chứ hiện tại đang giống goalllll hơn"**

> User intent: **"Tội…"** phải là câu cảm thán THỞ DÀI thương xót, KHÔNG reo hào hứng như "goalllll" (goal celebration).

---

## ❌ ANTI-PATTERN: Kéo dài âm cuối bằng ký tự vowel lặp

```text
[amazement-oh] Máy dập Lin Đan 2008 dập Ly Chong Quây 2 hiệp teo người luôn mà! 
[surprise-oh] Chắc là anh Ly Chong Quây ám ảnh từ đây! 
[sigh] Tộiiiiiiii…
```

**Kết quả:**
- Whisper transcript cuối câu: "Tối" 0.4s (hallucinate do phoneme nén)
- Energy profile last 1.5s: RMS 5775 → 7346 (peak rất cao = HÉT kéo dài)
- Nghe giống "GOALLLL" — celebration reo

**Root cause:** OmniVoice model đọc ký tự lặp `iiii` thành phoneme kéo dài với amplitude cao → không phải "thở dài buông", mà là "hét kéo dài".

---

## ✅ CORRECT PATTERN: Ellipsis `…` + emotion tag

```text
[amazement-oh] Máy dập Lin Đan 2008 dập Ly Chong Quây 2 hiệp teo người luôn mà! 
[surprise-oh] Chắc là anh Ly Chong Quây ám ảnh từ đây! 
[sigh] Tội…
```

**Kết quả:**
- Whisper transcript cuối câu: "Tội" 0.4s (vẫn hallucinate nén, nhưng tone đúng)
- Energy profile last 1.5s: RMS 1262 → 3073 (peak mềm = THỞ DÀI buông)
- Nghe đúng cảm xúc "thở dài thương xót"

---

## 📊 BẢNG TRA CỨU NHANH: Emotion + Extension Pattern

| User intent | Pattern | Peak RMS (last 1.5s) | Tone | Example |
|---|---|---|---|---|
| **Hét kéo dài / reo hào hứng** | `[surprise-oh]` + vowel repeat | 5000-8000 (to) | Hét, năng lượng cao | `"GOALLLL[surprise-oh]!"` |
| **Kéo dài âm cuối (sốc, ngạc nhiên)** | Ellipsis `…` + `[amazement-oh]` | 3500-4500 (vừa) | Ngạc nhiên kéo dài | `"Wow…[amazement-oh]"` |
| **Thở dài thương xót** | Ellipsis `…` + `[sigh]` | 2000-3500 (soft, buông) | Buồn, thương tiếc | `"Tội…[sigh]"` |
| **Thở dài đồng cảm (chê nhẹ)** | Ellipsis `…` + `[dissatisfaction-hnn]` | 2500-3500 | Chê, không hài lòng | `"Giá hơi cao…[dissatisfaction-hnn]"` |
| **Ngạc nhiên reo (đồng minh)** | Ellipsis `…` + `[surprise-oh]` | 4000-5500 | Sốc, bất ngờ | `"Deal hời quá…[surprise-oh]"` |
| **Câu hỏi lên cao** | `[question-ah]` (không kéo dài) | 2500-4000 | Hỏi, lên giọng | `"Bạn nghĩ sao[question-ah]?"` |

---

## 🛠️ VERIFY BẰNG WAVEFORM RMS

Dùng Python `wave` + `numpy` để check RMS energy profile last 1.5s:

```python
import wave, numpy as np

with wave.open("voice.wav", "rb") as wav:
    frames = wav.getnframes()
    rate = wav.getframerate()
    channels = wav.getnchannels()
    raw = wav.readframes(frames)

audio = np.frombuffer(raw, dtype=np.int16)
samples_per_sec = rate * channels

# Last 1.5s
last_15 = int(frames / rate - 1.5) * samples_per_sec
end = len(audio)

chunk_size = int(0.1 * samples_per_sec)  # 100ms chunks
for i in range(last_15, end, chunk_size):
    chunk = audio[i:i+chunk_size]
    if len(chunk) > 0:
        t = i / samples_per_sec
        rms = np.sqrt(np.mean(chunk.astype(np.float32) ** 2))
        print(f"  t={t:.2f}s: rms={rms:.1f}")
```

**Đọc kết quả:**
- Peak RMS 5000-8000 → HÉT kéo dài (anti-pattern)
- Peak RMS 2000-3500 → THỞ DÀI tự nhiên ✅
- Peak RMS 3500-4500 → NGẠC NHIÊN kéo dài (OK nếu intent)

---

## ⚠️ Whisper Transcript KHÔNG Phản Ánh Duration Kéo Dài

Whisper thường **hallucinate nén** các phoneme cuối câu thành 1 âm duy nhất (vd "Tộiiiiiiii" → Whisper báo "Tội" 0.4s thay vì 0.6s). Đây KHÔNG phải lỗi voice model — chỉ là Whisper không phân biệt được.

→ **Luôn verify bằng RMS energy profile**, KHÔNG tin Whisper transcript về duration extension.

---

## 🎯 VERIFIED CASES (26/07)

| Case | Pattern | RMS Peak | Verdict |
|---|---|---|---|
| `"Tộiiiiiiii…"` + `[sigh]` | VOWEL REPEAT | 7346 | ❌ "goalllll" |
| `"Tội…"` + `[sigh]` | ELLIPSIS | 3073 | ✅ "thở dài thương xót" |
| `"GOALLLL"` + `[surprise-oh]` | VOWEL REPEAT | ~7000 | ✅ (intent = reo) |
| `"Wow…"` + `[amazement-oh]` | ELLIPSIS | ~4000 | ✅ (intent = ngạc nhiên) |

---

## Related

- Skill: `omnivoice-voice-clone` (PITFALL #N+8 — emotion tag fit content + ellipsis vs trailing vowel)
- Memory rule: emotion tags BẮT BUỘC 1 tag tối thiểu / segment
- Pattern from `omnivoice-smooth-config-and-leak-prevention` (Pitfall #13, #14)