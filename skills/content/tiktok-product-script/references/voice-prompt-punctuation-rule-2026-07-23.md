---
title: Voice prompt punctuation rule (dấu câu cho prompt OmniVoice)
created: 2026-07-23
type: reference
severity: high
applies-to: mọi prompt OmniVoice / voice clone / TTS generation
---

# Voice Prompt Punctuation Rule

> **User feedback verbatim 23/07/2026:** *"Vấn đề ngắt nghỉ nhiều là do dấu "." Và dấu "," em đang phân bố dày và bất hợp lý quá, muôn voice clone nói được liền mạch một câu phải giảm bớt dấu "," trong câu và dấu "." Cũng cần đặt đúng điểm để chuyển giai đoạn. Dấu chỉ đặt khi thực sự muốn nhấn mạnh vào vấn đề hoặc câu nói đó thôi"*

## 🎯 RULE CỐT LÕI

### Dấu "," trong câu: GIẢM, KHÔNG BỎ

| ❌ BỎ HẲN (FAIL case) | ✅ GIẢM VỪA PHẢI (PASS case - V4B OK) |
|---|---|
| Bỏ hết dấu "," → model hallucinate "Tài năng tìm ra là" loop | 0.6-0.9 dấu/câu, mỗi dấu nối 2 ý liên quan |
| Thay bằng "—" em-dash → model vẫn pause | Dấu "," giảm, emotion tags đầu paragraph dài |

### Dấu "." trong câu: ĐẶT ĐÚNG ĐIỂM CHUYỂN GIAI ĐOẠN

- KHÔNG phải để ngắt giữa ý
- CHỈ đặt khi chuyển sang ý MỚI (giai đoạn mới trong narrative)

## 📊 PATTERN V4B (anh thấy OK)

| Metric | V4B (OK) | V4A (bị chê) | V4B OK reflow |
|---|---|---|---|
| Số câu | 18 | 20 | 18 |
| Avg words/câu | 8.3 | 7.4 | 8.3 |
| Dấu "," | 10 | 11 | 10 |
| Phẩy/câu (avg) | 0.6 | 0.6 | 0.6 |
| Dấu "." | 18 | 20 | 18 |
| Emotion tag paragraph | 38 từ | 15 từ | 38 từ |

## 🧠 4 CÁCH EM ĐÃ THỬ (3 FAIL → 1 PASS)

### FAIL 1: Bỏ hẳn dấu câu
```
Văn bản: "Hai năm làm video có một thứ mình ước biết sớm hơn đấy"
         → Model hallucinate "Tài năng tìm ra là Tài năng tìm ra là"
```
- Whisper verify: 100% hallucinate loop
- Em KHÔNG dùng approach này

### FAIL 2: Em-dash "—"
```
Văn bản: "Hai năm làm video—có một thứ mình ước biết—sớm hơn đấy"
         → Model vẫn pause tại "—", không khác gì dấu ","
```
- Đếm pauses TĂNG so với bản có dấu ","
- Em KHÔNG dùng approach này

### FAIL 3: Paragraph dài (45 từ) + bỏ dấu
```
Văn bản: "Hồi mới quay mình đặt điện thoại lên bàn đấy góc thấp chỉ thấy cằm..."
         → 45 từ liền nhau → model tự ngắt quãng không đúng chỗ
```
- User feedback 23/07: "câu dài quá omnivoice tự ngắt quãng còn bất hợp lý hơn"
- Em KHÔNG dùng approach này

### PASS: Cân bằng theo V4B (anh OK)
- 8-15 từ/câu (không quá ngắn, không quá dài)
- 0.6-0.9 dấu phẩy/câu (giảm so với bình thường, KHÔNG bỏ)
- 1 dấu chấm/câu cuối (chuyển giai đoạn)
- Emotion tag đầu paragraph 30-45 từ (gộp 3-5 ý)
- Fragments 3-5 từ OK (đặc trưng văn nói, V4B có 5)

## ✅ CHECKLIST VIẾT VOICE PROMPT

```python
text = prompt_for_omnivoice

# 1. Câu phải 8-15 từ (không quá dài)
sentences = split_into_sentences(text)
lengths = [len(s.split()) for s in sentences]
assert all(3 <= l <= 18 for l in lengths), f"Câu quá ngắn/dài: {lengths}"

# 2. Dấu phẩy 0.6-0.9/câu (giảm so với bình thường, KHÔNG bỏ)
total_commas = sum(s.count(',') for s in sentences)
ratio = total_commas / len(sentences)
assert 0.4 <= ratio <= 1.0, f"Comma ratio {ratio:.2f} ngoài range 0.4-1.0"

# 3. Dấu chấm = số câu - emotion tags
# (mỗi câu kết thúc bằng ".", emotion tag tách riêng)

# 4. Emotion tag đầu paragraph 30-45 từ
for paragraph in split_into_paragraphs(text):
    if has_emotion_tag(paragraph):
        words = count_words_after_emotion_tag(paragraph)
        assert 25 <= words <= 50, f"Emotion paragraph quá ngắn/dài: {words}"
```

## 📝 EXAMPLE TRANSFORMATIONS

### ❌ V4A V1 (bị chê)
```
Hồi mới quay, mình toàn đặt điện thoại lên bàn đấy. Góc thấp, chỉ thấy cằm thôi. Mình cứ tưởng ổn ấy.
```

### ❌ V4A V2 (FAIL - em-dash)
```
Hồi mới quay, mình—đặt điện thoại—lên bàn đấy—góc thấp—chỉ thấy cằm
```

### ❌ V4A V3 (FAIL - paragraph quá dài, 45 từ)
```
Hồi mới quay mình đặt điện thoại lên bàn đấy góc thấp chỉ thấy cằm thôi mình cứ tưởng ổn ấy xong đi cafe một mình không ai cầm máy giùm mua cây tripod to nặng balo thêm 2 ký luôn lắm chuyện nhỉ
```

### ✅ V4A FINAL (PASS - pattern V4B)
```
Hồi mới quay, mình đặt điện thoại lên bàn đấy. Góc thấp, chỉ thấy cằm thôi. Mình cứ tưởng ổn ấy.
Xong đi cafe một mình. Không ai cầm máy giùm. Mua cây tripod to nặng, balo thêm 2 ký luôn.
[question-ah] Rồi mình thử chiếc tripod này, chuyên cho DJI Osmo Pocket 3 đấy.
Nó gấp lại bằng cái bút, bỏ vào ngăn phụ của balo. Nặng 75 gam thôi, balo thêm có 75 gam không khác gì không có.
```

## 🎤 GENERATE VOICE VỚI CONFIG NÀO

```python
from omnivoice import OmniVoice, VoiceClonePrompt, OmniVoiceGenerationConfig

gc = OmniVoiceGenerationConfig(
    audio_chunk_threshold=90.0,    # Text <90s không chunk
    audio_chunk_duration=30.0,     # Chunk 30s thay vì 15s mặc định
    pad_duration=0.0,              # Không padding
    fade_duration=0.0,             # Không fade
)
```

## 📂 RELATED FILES

- `wiki/concepts/tiktok-script-natural-voice-2026-07-21.md` - 8 bài học văn nói
- `wiki/projects/tuan-anh-review-tiktok/scripts/ulanzi-ma66-tripod-pocket-3-natural-voice.md` - V4 (anh nói "rất ổn" về V4B)
- `wiki/projects/tuan-anh-review-tiktok/scripts/ulanzi-ma66-tripod-pocket-3-first-person.md` - V5 first-person

---

*Created 23/07/2026 từ user feedback "Vấn đề ngắt nghỉ nhiều là do dấu "." Và dấu "," em đang phân bố dày và bất hợp lý quá". Severity: HIGH — đây là core rule cho MỌI voice prompt.*
