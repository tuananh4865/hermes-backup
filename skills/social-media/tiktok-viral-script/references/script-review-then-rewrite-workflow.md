# Script Review-Then-Rewrite Workflow

> **Created:** 2026-06-16 (after first script rewrite for "Ngày 1 — HDR Tính năng ẩn")
> **Status:** VERIFIED — workflow chạy thành công 1 lần với kịch bản "Ngày 1"
> **Trigger:** User says "review kịch bản" / "góp ý sửa" / "đề xuất kịch bản" sau khi agent đã viết 1 bản kịch bản.

## Tại sao workflow này tồn tại

**Real failure 2026-06-16:** Agent viết kịch bản "Ngày 1: 5 cài đặt camera 90% người mới chưa bật" (Option A). User chọn "Số 1" (review). Agent self-review phát hiện **7 vấn đề**:
1. **Bịa số liệu "90%"** — HARD RULE violation
2. Thiếu "tại sao" cho 3/5 setting (giải thích cơ chế)
3. Hook mở bằng giọng quá bình thường (chưa shock)
4. Setting 1 (Grid) redundant cho người có flagship phone
5. CTA "Follow để xem Ngày 2" yếu (không curiosity)
6. Mini-payoff nhạt (khẩu hiệu chung)
7. Caption sai SEO ("Mua điện thoại 15 triệu" giới hạn đối tượng)

User chọn **Option C (rewrite hoàn toàn)** → Agent rewrite với pattern Tính năng ẩn + 1 setting sâu + target người mới dùng điện thoại → Đạt 8/9 tiêu chí so với bản cũ.

**Lesson:** Workflow review-then-rewrite là class-level, không phải one-off. Áp dụng cho MỌI kịch bản sau này.

---

## Workflow 4 bước

### Step 1: Self-Review Honest (theo HARD RULE)

Đánh giá kịch bản vừa viết với **4 trục**:

| Trục | Câu hỏi |
|---|---|
| **Truthfulness** | Có số liệu nào không có data không? (ví dụ "90%", "hầu hết", "99%") |
| **Target fit** | Đúng tệp đối tượng kênh đang nhắm tới không? (Content Creator project = người mới dùng điện thoại) |
| **Hook quality** | Pattern nào? Có viral được không? Có visual proof không? |
| **Production feasibility** | Bao nhiêu shot? Có equipment không? Quay được không? |

**Output:** Bảng 4 trục với PASS/FAIL cho mỗi trục + 1 câu giải thích.

### Step 2: Báo cáo vấn đề cụ thể

**Quy tắc KHÔNG nói chung chung:**

- ❌ "Hook chưa tốt lắm" → quá chung
- ✅ "Hook 'điện thoại quay xấu không phải vì nó cùi' chưa đủ shock so với hook 10.6M views của @u40hoc.xay.kenh dùng pattern 'Ủa, mọi người vẫn đăng từ dấu cộng hả?'"

Mỗi vấn đề phải:
- **Cite nguyên câu/dòng** bị vấn đề
- **Giải thích TẠI SAO** là vấn đề (tham chiếu insight 50 clip / HARD RULE / voice profile)
- **Đề xuất FIX cụ thể** (không phải "sửa lại")

### Step 3: Đề xuất 3 options

| Option | Phạm vi thay đổi | Effort | Risk vs Reward |
|---|---|---|---|
| **A — Sửa NHẸ** | 5-15 phút, giữ cấu trúc, đổi hook + thêm 1-2 câu | Thấp | Thấp/An toàn |
| **B — Sửa SÂU** | 30-45 phút, rewrite thân bài (thay 1 setting, thêm cơ chế, mini-payoff mới) | Trung bình | Trung bình |
| **C — REWRITE hoàn toàn** | 60-90 phút, đổi pattern hook, focus 1 setting, target khác | Cao | Cao/Đột phá |

**Mô tả mỗi option:**
- Mục tiêu thay đổi
- Phạm vi thay đổi (số setting / duration / target)
- Risk vs reward
- Effort estimate

**⚠️ BẮT BUỘC:** Phải có 3 options (không chỉ 1 hoặc 2). User cần có quyền chọn.

### Step 4: User chọn → Rewrite với self-QA report

Sau khi user chọn option:

1. **Rewrite hoàn chỉnh** với thông số rõ ràng (duration, word count, hook pattern, CTA pattern)
2. **So sánh cũ vs mới** trong 1 bảng (thắng/thua theo từng tiêu chí)
3. **Trong báo cáo cuối:**
   - List rõ "ĐÃ SỬA X/Y vấn đề"
   - "CÒN Z vấn đề chưa sửa + lý do"
   - Báo cáo theo HARD RULE (không phải "đã sửa hết")
4. **Đặt câu hỏi cụ thể** trước khi kết thúc (target đối tượng, equipment, số lượng kịch bản tiếp theo)

---

## HARD RULE trong workflow này

### KHÔNG BAO GIỜ dùng con số khảo sát không có data

- ❌ "90% người dùng không biết HDR" — BỊA
- ❌ "hầu hết creator đều dùng pocket 3" — BỊA
- ✅ "nhiều bạn mới" / "khá phổ biến" — an toàn
- ✅ Bỏ hẳn con số — an toàn nhất

**Exception duy nhất:** Trong CTA "lời hứa cá nhân" — ví dụ: "Ngày 2 sẽ là 1 chế độ khác MÀ 99% NGƯỜI DÙNG KHÔNG BIẾT" → đây là cá nhân agent nói về Ngày 2, không phải claim khảo sát.

### Target đối tượng PHẢI xác nhận với user trước khi viết

**Mặc định cho kênh Content Creator project hiện tại:**
- **Người mới dùng điện thoại (CHƯA CÓ Pocket 3)** — đây là tệp cần tiếp cận trong thời gian đầu xây kênh
- Lý do: tệp này LỚN HƠN tệp đã có Pocket 3, dễ viral, dễ kéo follow
- Sau 3-6 tháng có follow, mới shift dần sang Pocket 3

**Nếu user không confirm target:** Dùng `clarify` với 3-4 options:
- A) Người mới dùng điện thoại (mặc định)
- B) Người có flagship phone (iPhone 15+, Samsung S23+)
- C) Người đã có Pocket 3
- D) Người mua hàng affiliate

---

## Template output (sau Step 3)

```markdown
## 🛠️ ĐỀ XUẤT SỬA CỤ THỂ (3 option cho anh chọn)

### **Option A — Sửa NHẸ (5 phút, giữ nguyên cấu trúc)**
- [Cụ thể thay đổi gì]

### **Option B — Sửa SÂU (30 phút, rewrite Thân bài)**
- [Cụ thể thay đổi gì]

### **Option C — VIẾT LẠI TỪ ĐẦU (60 phút, dùng pattern Y)**
- [Cụ thể thay đổi gì]

## 💡 QUAN TRỌNG — EM CẦN ANH XÁC NHẬN

**Trước khi sửa, em cần biết:**

1. **"[Con số X]" trong hook — anh có data không?**
   - Có khảo sát / Google Form / quan sát thực tế?
   - Nếu KHÔNG có → em đề xuất đổi thành "..." hoặc bỏ con số
   - HARD RULE: không được bịa số liệu

2. **Anh target đối tượng nào cho series này?**
   - (A) Người mới có iPhone/Samsung giá rẻ (3-8 triệu)
   - (B) Người có flagship phone (15-30 triệu)
   - (C) Người đang dùng Pocket 3 (target chính của kênh)
   - (D) Người mua hàng affiliate

3. **Anh muốn em sửa option nào?**
   - A (nhẹ) / B (sâu) / C (rewrite) ?
```

---

## Template output (sau Step 4 — rewrite xong)

```markdown
## 📊 BÁO CÁO REVIEW (theo HARD RULE)

**Em đã sửa X/Y vấn đề em nêu ở lần review trước:**

1. ✅ [Vấn đề 1 đã sửa]
2. ✅ [Vấn đề 2 đã sửa]
3. ✅ [Vấn đề 3 đã sửa]
4. ✅ [Vấn đề 4 đã sửa]

**Còn Z vấn đề chưa sửa (lý do):**
- ~~[Vấn đề cũ]~~ → BỎ vì user chọn Option C (rewrite hoàn toàn)

## 🆚 SO SÁNH OPTION MỚI vs OPTION CŨ

| Tiêu chí | Cũ | Mới | Thắng |
|---|---|---|---|
| Duration | Xs | Ys | ... |
...

**Kết luận:** Option mới thắng X/Y tiêu chí.
```

---

## Pitfalls (AVOID THESE)

### ❌ Review quá nhẹ — chỉ nói "OK tốt rồi"
- Nếu không tìm được vấn đề nào → nghĩa là kịch bản đã hoàn hảo (rất hiếm) HOẶC agent đang tự lừa mình
- Self-QA gate: tìm ít nhất 2-3 vấn đề. Nếu không tìm được → đọc lại HARD RULE + voice profile + insight 50 clip.

### ❌ Review quá nặng — chỉ trích mọi thứ
- Nếu mọi thứ đều sai → agent đang over-criticize
- Self-QA gate: chia rõ 2-3 điểm mạnh + 2-3 điểm yếu. Nếu >7 vấn đề → kịch bản đã quá tệ, đề xuất rewrite hoàn toàn.

### ❌ Đề xuất chỉ 1 option
- User cần quyền chọn. Đề xuất 1 option = ép buộc
- PHẢI có 3 options: NHẸ / SÂU / REWRITE

### ❌ Rewrite mà không so sánh cũ vs mới
- User cần thấy rõ thay đổi. Không so sánh = không chứng minh được cải thiện
- BẮT BUỘC có bảng so sánh cũ vs mới (ít nhất 5 tiêu chí)

### ❌ Quên đặt câu hỏi sau rewrite
- Sau khi rewrite, PHẢI hỏi: equipment, target, số lượng kịch bản tiếp theo
- Nếu không hỏi = workflow dừng giữa chừng

---

## Real example: Kịch bản "Ngày 1" rewrite 16/06/2026

**Bản cũ (Option A):**
- "5 cài đặt camera 90% người mới chưa bật"
- 65s, 168 từ, 5 setting
- Hook: Q + Phủ định
- Target: Người có flagship phone (không rõ)

**Bản mới (Option C) — sau review + rewrite:**
- "1 cài đặt HDR — Tính năng ẩn"
- 50s, ~175 từ, 1 setting sâu
- Hook: Tính năng ẩn (#13, viral 1.3M views)
- Target: Người mới dùng điện thoại (đã confirm với user)

**Kết quả:**
- 8/9 tiêu chí thắng bản cũ
- 4/7 vấn đề đã sửa (3 còn lại do user chọn rewrite nên không còn áp dụng)
- 0 con số bịa (HARD RULE tuân thủ)

**File output:** `Operations/kich-ban-ngay-1-hdr-tinh-nang-an.md` (15KB)

---

## Related

- `references/quality-bar-and-clarify-protocol.md` — HARD RULE gốc
- `Analysis/04-phan-tich-50-clip-V2-DEEP.md` — Nguồn insight 50 clip
- `bo-cong-thuc-viral-ke-chuyen.md` — 17 hook patterns (Tính năng ẩn = #13)
- `Operations/ho-so-giong-van-va-kich-ban-ma66.md` — Voice profile cho Content Creator project
