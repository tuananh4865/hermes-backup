---
name: content-creator-script-style
description: Quy tắc viết kịch bản TikTok cho kênh Content Creator của Tuấn Anh (3 trụ EDIT+SETUP+ÁNH SÁNG, series 0đ, framework 4 tử huyệt + 5 phần). Load trước khi viết bất kỳ script nào.
---

# Quy tắc viết kịch bản — Kênh Content Creator (Tuấn Anh)

## NGUYÊN TẮC CỨNG (từ feedback 18/06)

### 0. PREFERENCES 13/06/2026 — VOICE + 45-DAY VALUE RULE (HARD)

**Voice pronouns — TUYỆT ĐỐI TUÂN THỦ:**
- ✅ Dùng: "mình" / "bạn" / "chúng ta"
- ❌ CẤM: "anh" + "mấy con vợ", "anh" + "em", "mấy đứa", "mấy chị", "mấy má", "các bạn", "anh em"

**Câu mở đầu mỗi script phải check:**
```bash
! grep -E "mấy con vợ|anh + mấy|các bạn" scripts.md
# → PHẢI trả về 0 match. Nếu >0 → VI PHẠM, fix ngay.
```

**45-day value rule (Phase 01 only, 17/06 - 01/08/2026):**
- ✅ 100% hướng dẫn cơ bản (setup, edit, ánh sáng)
- ❌ 0% bán hàng, 0% "Mua ủng hộ", 0% "Link bio"
- ❌ 0% affiliate link, 0% gear review
- CTA = specific action thuần value: "Bắt đầu bằng cách X", "Lưu lại rồi thử Y"

**Self-verify before deliver:**
```bash
! grep -E "Mua.*ủng hộ|Mua.*đi mấy|Mua ủng hộ|link bio|affiliate" scripts.md
# → PHẢI trả về 0 match.
```

**Anti-pattern phát hiện 18/06/2026:** Session trước viết 15 scripts dùng voice cũ ("anh + mấy con vợ") + CTA bán hàng — phải REWRITE toàn bộ bằng 3 sub-agent parallel (SETUP/EDIT/ÁNH SÁNG). Lý do vi phạm: sub-agent không load skill `content-creator-script-style` (vì nó không tồn tại lúc đó) + không đọc `learned-about-tuananh.md`.

**Rule cứng cho sub-agent:** Khi delegate script generation, MUST include đoạn này trong context:
> "Voice phải là 'mình + bạn' (trung tính), KHÔNG 'anh + mấy con vợ' (deprecated 13/06/2026). 45-day value rule: 0% bán hàng, 0% affiliate, 100% hướng dẫn cơ bản. CTA = specific action thuần value, KHÔNG 'mua', 'ủng hộ', 'preset bán'."

### 0b. CONFESSION HOOK CHO VIDEO MỞ ĐẦU KÊNH — DATA FABRICATION RULE

Khi viết script kể chuyện cá nhân (Confession Hook, Story Arc) cho video mở đầu kênh:

- **Em KHÔNG có data cá nhân** (tuổi, năm sinh, quê quán, con số doanh thu thật, lý do sâu pivot)
- **ĐỪNG bịa** con số chi tiết (200 video, 12 đơn, 2 triệu doanh thu) rồi nói đó là "câu chuyện thật của anh"
- **ĐÚNG CÁCH:** dùng placeholder mơ hồ ("rất nhiều video", "không ra đơn", "không đủ sống") HOẶC mark rõ trong script "Cần anh verify/điền vào chỗ này"

**Template disclaimer mở đầu mỗi confession script:**
```
⚠️ CẦN ANH VERIFY: [list các chỗ em dùng placeholder/generic — VD: "số đơn hàng thật", "doanh thu thật", "lý do pivot cá nhân"]
```

**Self-check trước khi deliver:**
```markdown
- [ ] Mỗi con số cụ thể có nguồn (memory/wiki/session) HOẶC marked "verify"
- [ ] Mỗi chi tiết cá nhân sâu (lý do pivot, family context) marked "verify"
- [ ] Script KHÔNG pretend biết thông tin em không có
```

### 1. CÂU TỪ PHẢI MƯỢT
Anh check kỹ lời thoại. Bỏ ngay:
- "Anh từng...", "Hóa ra...", "Sau X năm làm content..."
- Liệt kê khô (A thì B, B thì C, C thì D)
- "Khác biệt rõ như ngày với đêm" (cliché)

**Thay bằng:** câu chuyện có nhân vật + cảm xúc:
- "3 năm trước, anh lần đầu mua mic cài áo 500k — tưởng xịn. Rồi mic USB 1.5 triệu, mic không dây DJI 2 triệu. Tổng 4 triệu. Hóa ra mic iPhone mình đang có đã đủ xài."

### 2. TRÁNH CHỦ ĐỀ QUÁ PHỔ BIẾN
- CapCut, iPhone cơ bản, mic rẻ tiền → ai cũng biết → không có giá trị mới
- Phải có **case thực tế** (A/B test, số liệu cụ thể, câu chuyện thật)

### 3. TENSION KHÔNG LIỆT KÊ KHÔ
- KHÔNG: "Lỗi 1... Lỗi 2... Lỗi 3..." (liệt kê khô, mất giá trị)
- PHẢI: 3 case thực tế có số liệu + aha moment
- Ví dụ ĐÚNG: "Case 1: Video TikTok 9 giây — tua đi tua lại 3 lần. Cắt giữa động tác rắc tiêu, não bị giật."

### 4. TỬ HUYỆT CẢM XÚC (chọn TRƯỚC khi viết)
- **DANH** (sợ mất mặt): "90% người mới sai điều này"
- **TIỀN** (tiết kiệm): "Cửa sổ = đèn 5 triệu"
- **TÌNH** (cô đơn): "Mình cũng từng bỏ cuộc"
- **LỢI ÍCH** (nhanh): "5 phút - gấp 3"

Mỗi video CHỈ chạm 1 tử huyệt.

### 5. iPHONE MIC + VOICE ISOLATION ĐỦ DÙNG
Anh gợi ý: mic iPhone có Voice Isolation lọc ồn ngang mic xịn. 0 đồng. Đây là chủ đề "B1" trong series 0đ.

## 5 PHẦN KỊCH BẢN
```
HOOK (3-5s)       = Trigger cảm xúc từ tử huyệt + Lời hứa cụ thể
SET UP (10-15s)   = Đẩy nỗi đau cụ thể, hình ảnh
TENSION (30-60s)  = 3 case thực tế có số liệu
PAY OUT (10-20s)  = Đáp án ĐÚNG + ĐỦ cho Hook
CTA (3-5s)        = 1 hành động cụ thể + open loop Ngày sau
```

## CHECKLIST 7 CÂU HỎI (apply MỌI video)
1. Tôi đang chạm tử huyệt **DANH/TIỀN/TÌNH/LỢI ÍCH** nào?
2. Hook có **trigger cảm xúc** từ tử huyệt?
3. Hook có **lời hứa cụ thể** (số lượng, kết quả)?
4. Set up có **đẩy nỗi đau lên cụ thể**?
5. Tension có **case thực tế** + aha moment?
6. Pay out trả lời **ĐÚNG + ĐỦ** lời hứa ở Hook?
7. CTA chỉ **1 hành động cụ thể**?

## SWEET SPOT
- Duration: 30-69s (55s tối ưu)
- Word count: 150-200 từ
- Tỉ lệ: ~3 từ/giây
- Hook: 3-5s đầu (quyết định 70% retention)
- **Anh ưu tiên: dưới 1 phút** (TikTok thuật toán ưu tiên completion rate 70%+ — clip ngắn = retention cao = viral)

## EDIT RULE — KHI CẮT VIDEO CÓ RE-START PATTERN (2026-06-26, NEW)

Anh nói về cách edit raw footage: khi nói sai, anh sẽ **lặp lại câu đầy đủ hơn ở câu sau** → em phải **giữ câu đầy đủ, cắt câu trước** (câu bị sai/lặp). Logic này cũng apply cho TikTok script writing:

**Khi viết script có thể bị "lặp ý" → tránh ngay từ đầu:**
- Hook: 1 câu DUY NHẤT, không viết 2 version
- Set up: 1 ví dụ cụ thể, không list A rồi B rồi C
- Tension: 3 case KHÁC NHAU hoàn toàn (khác scenario, khác số liệu, khác aha moment)
- Pay out: 1 đáp án rõ ràng

**Anti-pattern "re-start" cần tránh trong script:**
- ❌ "Mình đã thử cách A. À không, cách A không được. Cách B mới đúng" → lặp, mất 5-7s
- ❌ "Nhiều bạn hỏi X. Thực ra X cũng không hẳn. Y mới đúng." → vòng vo
- ❌ "Đầu tiên làm X. Tiếp theo làm Y. À mà quên, X cũng cần làm trước." → lủng củng

**ĐÚNG:**
- ✅ Mỗi câu là final version, không có "à", "ờ", "ừm", "thực ra"
- ✅ Nếu cần sửa ý → viết lại từ đầu hook, không insert "correction" giữa video
- ✅ Transition mượt: "Bước 1 là X. Bước 2 là Y. Bước 3 là Z." (mỗi bước unique value)

**Khi EDIT raw footage (post-production):**
- Detect re-start: cùng 1 phrase lặp 2 lần trong 5-10s → giữ lần 2, cắt lần 1
- Pattern: speaker nói câu cụt → dừng → nói lại câu đầy đủ → cut phần cụt, nối trực tiếp vào câu đầy đủ
- KHÔNG cắt câu đầy đủ (kể cả khi nó có vẻ "lặp" vì content flow cần nó)

## VOICE / TTS PREFERENCES (NEW 21/07/2026 — from MA66 voice session)

Khi user yêu cầu tạo voice/script TTS cho TikTok (text_to_speech, file MP3 cho voice-over):

1. **Voice mặc định:** `vi-VN-NamMinhNeural` (nam, friendly/positive). KHÔNG dùng `vi-VN-HoaiMyNeural` (nữ, default cũ) trừ khi user explicit yêu cầu khác.
2. **Speed mặc định:** 1.3x. KHÔNG cần hỏi "speed bao nhiêu" — đã có default.
3. **Script rules cho voice (HARD):**
   - **KHÔNG nêu giá** trong voice (599k, 67k/tháng → để visual overlay)
   - **KHÔNG gọi mã SP** (MA66, K17, ARMAF) — gọi tên gọi chung "chiếc tripod này", "chai body mist này"
   - **PHẢI nhắc tên SP tương thích** (DJI Pocket 3, iPhone 15, Samsung S24) 2-3 lần trong script
   - **Storytelling > listing** — Hook intrigue ("Hai năm mình ước biết") KHÔNG phải USP liệt kê
4. **Authentic voice option:** Nếu user yêu cầu "giọng thật của anh" → dùng OmniVoice skill (`omnivoice-voice-clone`), prompt ở `/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_*.pt`.

User verbatim 21/07: *"Sản phẩm là tripod thì gọi nó là chiếc tripod này thôi không gọi mã ma66 ai hiểu?"* + *"Sản phẩm này chỉ dùng được với dji osmo pocket 3/4/4P thôi. Phải xem kĩ thông tin sản phẩm chứ"*

Xem `references/voice-script-tts-workflow.md` trong skill `tiktok-product-script` để thấy workflow chuẩn 2 bước (edge-tts → ffmpeg atempo) + self-check trước khi generate.

## FILE THAM KHẢO
- Framework chi tiết: `~/wiki/queries/2026-06-18-4-tu-huyet-5-phan-FINAL.md`
- Curriculum 71 bài: `Content Creator/Research/2026-06-17/02-CURRICULUM-NGUOI-MOI-BAT-DAU.md`
- Series 0đ: `Content Creator/series-xay-kenh-0-dong.md`
- Bài mẫu 0đ (mic iPhone): `Content Creator/Operations/kich-ban-ngay-2-mic-iphone.md`
- Voice TTS workflow: `~/.hermes/skills/content/tiktok-product-script/references/voice-script-tts-workflow.md`