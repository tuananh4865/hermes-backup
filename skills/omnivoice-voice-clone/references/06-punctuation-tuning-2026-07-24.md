# SCRIPT-TO-VOICE PUNCTUATION TUNING (session 2026-07-24)

## TL;DR

Anh corrected em **2 lần trong 1 phiên** về cùng 1 vấn đề (dấu câu trong prompt voice OmniVoice). Bài học: user correct chi tiết kỹ thuật = user đang calibrate rất sát, KHÔNG generalize. Mỗi correction thu hẹp range.

## Timeline 3 versions

| Version | Em làm | Kết quả | Reaction |
|---|---|---|---|
| **V1** | Dấu `.,` phân bố đều, mỗi câu 1-2 phẩy | Voice ngắt quãng nhiều, không liền mạch | ❌ Anh: "Option B rất ổn" (V4B baseline OK) → các version khác sai |
| **V2** | Bỏ HẲN dấu `.,`, thay bằng `—` và space | Whisper hallucinate "Tài năng tìm ra là..." loop | ❌ Anh: "Không phải là không bỏ dấu , mà giảm bớt" |
| **V3** | GIẢM vừa đủ dấu `.,`, calibrated theo V4B baseline | Voice liền mạch ✅ | ✅ Anh chưa correct thêm = ngầm OK |

## Calibration: V4B OK baseline (verbatim reference)

```
[surprise-oh] Cái tin nhắn nó gửi tối qua, mình đọc xong cười.       (1 phẩy, 11 từ)
Cô bạn mình đi Đà Lạt một mình tuần trước. Nó có DJI Pocket 3.      (0 phẩy, 15 từ)
[sigh] Hồi đó nó mang cây tripod to nặng. Đi du lịch, balo nặng,
vai mỏi cả ngày. Mà quay cũng không ra gì. Góc thấp, chỉ thấy
mặt thôi. Không mang theo thì tiếc. Mang theo thì mệt.             (1 phẩy, 38 từ)
```

**Stats:** 18 câu, avg 8.3 từ/câu, max 18 từ, 10 phẩy (0.6/câu), 5 fragments 3-5 từ, emotion tag paragraph 38 từ.

## Quy tắc calibrated (FIRST-CLASS vĩnh viễn)

| Metric | Target | Nguồn |
|---|---|---|
| Dấu phẩy/câu | **0.6-0.9 dấu/câu** (giảm vừa, KHÔNG bỏ) | V4B OK (anh thấy "rất ổn") |
| Words/câu | **8-15 từ**, max 18 (sweet spot 10-12) | V4B OK |
| Dấu chấm | Đặt tại CHUYỂN GIAI ĐOẠN, không giữa ý | Lần 1 correction |
| Emotion tag paragraph | **30-45 từ** (gộp 3-5 ý) | V4B OK (1 sigh = 6 ý liên quan) |
| Fragment 3-5 từ | **3-5/script** OK | V4B OK (5 fragments) |

## Anti-patterns (đã FAIL, không dùng lại)

1. **Bỏ HẲN dấu câu** → model hallucinate loop "Tài năng tìm ra là..." (Whisper verify catch)
2. **Thay dấu phẩy bằng em-dash `—`** → model vẫn pause, pauses tăng 19→24 short
3. **Paragraph dài 45 từ + bỏ dấu** → câu quá dài, model tự ngắt bậy
4. **0 dấu phẩy/câu** → câu mất nhịp, voice nghe 1 hơi không ngắt

## Self-check tool (chạy trước khi generate)

```python
import re

def check_script_punctuation(text):
    """Calibrated từ V4B OK baseline. Target ranges in comments."""
    clean = re.sub(r'\[[\w-]+\]', '', text)
    sentences = [s.strip() for s in re.split(r'[.!?]', clean) if s.strip()]
    
    wc = [len(s.split()) for s in sentences]
    cc = [s.count(',') for s in sentences]
    avg_wc = sum(wc) / len(wc)
    avg_cc = sum(cc) / len(cc)
    
    fragments = sum(1 for c in wc if 3 <= c <= 5)
    
    # Check emotion tag paragraph length
    paragraphs = text.split('\n')
    emotion_paras = []
    for i, p in enumerate(paragraphs):
        if re.match(r'\s*\[[\w-]+\]', p):
            words = len(re.sub(r'\[[\w-]+\]', '', p).split())
            emotion_paras.append((i, words))
    
    issues = []
    if avg_cc < 0.6:
        issues.append(f"⚠️ Too few commas: {avg_cc:.2f}/câu (target 0.6-0.9)")
    if avg_cc > 1.0:
        issues.append(f"⚠️ Too many commas: {avg_cc:.2f}/câu (target 0.6-0.9)")
    if avg_wc < 8:
        issues.append(f"⚠️ Avg too short: {avg_wc:.1f} từ/câu (target 8-15)")
    if avg_wc > 15:
        issues.append(f"⚠️ Avg too long: {avg_wc:.1f} từ/câu (target 8-15)")
    if max(wc) > 20:
        issues.append(f"⚠️ Max sentence too long: {max(wc)} từ (model sẽ tự ngắt)")
    if fragments > 8:
        issues.append(f"⚠️ Too many fragments: {fragments} (target 3-5)")
    
    for idx, w in emotion_paras:
        if w < 20:
            issues.append(f"⚠️ Emotion tag paragraph #{idx} too short: {w} từ (target 30-45)")
        elif w > 50:
            issues.append(f"⚠️ Emotion tag paragraph #{idx} too long: {w} từ (target 30-45)")
    
    print(f"Sentences: {len(sentences)}")
    print(f"Words/sentence: min={min(wc)}, max={max(wc)}, avg={avg_wc:.1f}")
    print(f"Commas/sentence: avg={avg_cc:.2f}")
    print(f"Fragments (3-5 words): {fragments}")
    print(f"Emotion paragraphs: {emotion_paras}")
    
    if issues:
        print("\n❌ ISSUES:")
        for issue in issues:
            print(f"  {issue}")
        return False
    print("\n✅ PASS")
    return True

# Usage
text = open("/path/to/script.txt").read()
check_script_punctuation(text)
```

## Verify bằng Whisper (ground-truth smoothness check)

```bash
# Whisper transcribe output WAV
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-dir /tmp/verify/ output.wav

# Đọc transcript - đánh giá:
# - Dòng dài liền mạch = voice smooth ✅
# - Nhiều dòng ngắn 1-2 từ = voice bị pause giữa các dấu ❌
cat /tmp/verify/output.txt
```

## Lesson lớn cho session sau

Khi user correct kỹ thuật chi tiết (punctuation, threshold, range) → KHÔNG generalize sang lĩnh vực khác. Mỗi correction = thu hẹp range, không mở rộng. Nếu user correct lần 2 về cùng vấn đề → em hiểu sai ở lần 1, KHÔNG defend current approach.

Pattern này áp dụng cho mọi skill có parameter cần calibrate (TTS speed, video length, file format thresholds...).
