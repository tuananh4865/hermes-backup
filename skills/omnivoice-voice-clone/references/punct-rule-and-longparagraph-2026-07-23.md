# Punct Rule + Long Paragraph Pattern cho OmniVoice prompt
**Discovered: 2026-07-23 bởi Tuấn Anh feedback (verbatim)**

---

## 🚨 ROOT CAUSE: voice bị ngắt quãng

### Anh dạy (verbatim 23/07/2026):

> **"Vấn đề ngắt nghỉ nhiều là do dấu "." Và dấu "," em đang phân bố dày và bất hợp lý quá, muốn voice clone nói được liền mạch một câu phải giảm bớt dấu "," trong câu và dấu "." Cũng cần đặt đúng điểm để chuyển giai đoạn. Dấu chỉ đặt khi thực sự muốn nhấn mạnh vào vấn đề hoặc câu nói đó thôi"**

### 3 RULE CỨNG (FIRST-CLASS, vĩnh viễn):

1. **Dấu `,` trong câu → 0 dấu**. Nếu thực sự cần nhấn mạnh vấn đề, dùng:
   - Em-dash `—` (NHƯNG đã test — OmniVoice vẫn pause)
   - Hoặc tách thành 2 paragraph riêng (mỗi paragraph 1 emotion tag)
   
2. **Dấu `.` chỉ đặt khi CHUYỂN GIAI ĐOẠN** (1 paragraph = 1 giai đoạn). KHÔNG dùng `.` giữa các ý trong cùng giai đoạn.

3. **Emotion tag đứng đầu paragraph DÀI (30-45 từ)** — gộp 3-5 ý vào 1 đoạn để emotion tag tạo 1 pause duy nhất, sau đó voice chạy liền mạch.

---

## ✅ PATTERN ĐÚNG (đã verify 23/07)

### V4B (anh thấy "rất ổn"):
```text
[surprise-oh] Cái tin nhắn nó gửi tối qua, mình đọc xong cười.

Cô bạn mình đi Đà Lạt một mình tuần trước. Nó có DJI Pocket 3.

[sigh] Hồi đó nó mang cây tripod to nặng. Đi du lịch, balo nặng, vai mỏi cả ngày. Mà quay cũng không ra gì. Góc thấp, chỉ thấy mặt thôi. Không mang theo thì tiếc. Mang theo thì mệt.

Mình gửi cho nó chiếc tripod chuyên cho Pocket 3 này.

[question-ah] Nó về kể, đi cả ngày balo vẫn 8 ký đấy. Quay chân dung ở đồi hoa, đẹp lắm.

Có lần quán cafe nó gài lên cửa sắt, Pocket 3 dính chặt, quay tay không cần cầm. Nó bảo, sao hồi trước mình không biết nhỉ.

Mấy nghìn người mua rồi. Sáu nghìn mấy người mua lại luôn. Freeship với hoàn tiền 14%.

[confirmation-en] Anh em nào hay đi du lịch, inbox chiếc tripod này nhé.
```

**Đặc điểm:**
- Emotion tag `[sigh]` đứng đầu paragraph **38 từ** (gộp nhiều ý)
- Emotion tag `[question-ah]` đứng đầu paragraph **19 từ**
- Mỗi emotion tag = 1 pause DUY NHẤT, sau đó voice liền mạch đến hết paragraph

### V4A (cũ - bị chê ngắt quãng):
```text
[surprise-oh] [laughter] Hai năm làm video, có một thứ mình ước biết sớm hơn đấy.
[sigh] Hồi mới quay, mình đặt điện thoại lên bàn đấy. Góc thấp, chỉ thấy cằm thôi. Mình cứ tưởng ổn ấy.
[sigh] Xong đi cafe một mình. Không ai cầm máy giùm. Mua cây tripod to nặng, balo thêm 2 ký luôn. Lắm chuyện nhỉ.
```

**Vấn đề:** emotion tag `[sigh]` đứng đầu paragraph **15 từ** (chỉ 2-3 ý) → sigh + 1 pause + ngắt

### V4A V4 (NEW - đã fix):
```text
[surprise-oh] [laughter] Hai năm làm video có một thứ mình ước biết sớm hơn đấy.

[sigh] Hồi mới quay mình đặt điện thoại lên bàn đấy góc thấp chỉ thấy cằm thôi mình cứ tưởng ổn ấy. Xong đi cafe một mình không ai cầm máy giùm mua cây tripod to nặng balo thêm 2 ký luôn lắm chuyện nhỉ.

[question-ah] Rồi tình cờ mình thử chiếc tripod này chuyên cho DJI Osmo Pocket 3 đấy nó gấp lại bằng cái bút bỏ vào ngăn phụ của balo nặng 75 gam thôi balo thêm có 75 gam không khác gì không có.

Ngồi cafe xong lấy ra gài máy quay vào một cái là dính một giây xong.

Mấy nghìn người mua rồi đấy 4.9 sao trên 96 review freeship luôn hoàn tiền 14% nữa.

[confirmation-en] Anh em nào đi cafe quay TikTok Pocket 3 inbox chiếc tripod này giùm mình nhé.
```

**Fix:** emotion tag `[sigh]` đứng đầu paragraph **44 từ** (gộp 5-6 ý). Bỏ dấu `,` giữa ý, chỉ giữ `.` cuối paragraph.

---

## ❌ 3 APPROACH SAI (đã test, không dùng)

| Approach | Kết quả | Lý do |
|---|---|---|
| Thay `,` bằng em-dash `—` | ❌ Tăng pauses (V4B: 336 → 516) | OmniVoice vẫn pause tại `—` |
| Bỏ HẲN dấu câu (chỉ space) | ❌ Hallucinate 100% | Model không hiểu text → loop "Tài năng tìm ra là..." |
| Chỉ giảm `,` xuống còn 0.3/câu | ⚠️ Cải thiện nhẹ nhưng không triệt để | Vấn đề không phải số dấu, mà là emotion tag đứng đầu paragraph ngắn |

---

## 🔧 VERIFY RECIPE

Sau khi generate voice, verify smooth bằng Whisper transcript:

```bash
mlx_whisper --model mlx-community/whisper-medium-mlx --language vi \
  --output-dir /tmp/verify output.wav
```

**PASS criteria:**
- No hallucinate loop (5-gram repeat > 5 lần = FAIL)
- Transcript liền mạch (câu Whisper trả ra = 1 dòng text dài, KHÔNG bị ngắt giữa chừng)
- Emotion tag có tác dụng (peak volume tăng so với baseline)

**Whisper transcript V4A V4 (PASS):**
```
Hồi mới quay mình đặt điện thoại lên bàn đấy, góc thấp chỉ thấy cầm thôi
mình cứ tưởng ổn ấy
Xong đi cafe 1 mình không ai cầm máy dùm mua cây tripod to nặng, ba lô thêm 2kg luôn
lắm chuyện gì
```

→ Câu 1 dài liền mạch "Hồi mới quay... cầm thôi mình cứ tưởng ổn ấy" không có pause.

---

## 📚 RELATED

- Skill `tiktok-product-script` v0.10.0 (đã update với 8 bài học văn nói)
- Concept: `wiki/concepts/tiktok-script-natural-voice-2026-07-21.md`
- Skill memory: [EMOTION-MANDATORY], [VAN-NOI-TU-NHIEN-RULE importance:1.0]
