# Insight-Driven Product Review (2026-06-17) — Khi Anh Reject "So sánh"

**Trigger:** User yêu cầu "viết bài review sản phẩm X" → agent viết dạng review/so sánh (dạng 2 hoặc 3 trong `8-dang-content-chi-dan.md`) → user phản hồi "không so sánh, thử dạng khác, cho người dùng biết điểm tiện dụng + tại sao nên mua thay vì [đối thủ chính hãng]".

**Real failure (16-17/06/2026):** Agent viết review Goojodoq GD14 → GD15 với dạng review + so sánh Apple Pencil 2. User phản hồi: *"Không làm so Sánh đâu phải chỉ mỗi dạng này thử dạng khác đi' cho người dùng biết điểm tiện dụng chỗ nào và tại sao nên mua thay vì phải mua pencil chính hãng"*.

## Workflow 6 bước (REWRITE workflow khi user reject "so sánh")

### Step 1: BÁO CÁO 4 vấn đề với dạng hiện tại
- ❌ So sánh kỹ thuật → quá chi tiết, người mới không cần
- ❌ Dùng đối thủ chính hãng làm anchor → tạo tâm lý "hàng fake không bằng hàng thật"
- ❌ Thiếu tiện ích thực tế → quá focus vào spec
- ❌ Không có insight từ kinh nghiệm thật → generic, không uy tín

### Step 2: HỎI USER chia sẻ insight thật (nếu chưa có)
Nếu user đã dùng sản phẩm + có kinh nghiệm với đối thủ chính hãng, hỏi:
- "Anh thấy điểm khác biệt thực tế giữa SP này và đối thủ là gì?"
- "Anh dùng SP này cho mục đích gì?"
- "Có điểm nào anh thấy 'tương đồng' không?"

**Mục đích:** Insight thật từ user = uy tín + viral. KHÔNG tự nghĩ insight.

### Step 3: CHỌN DẠNG THAY THẾ
Từ 8 dạng content (`8-dang-content-chi-dan.md`), loại trừ dạng 2 (review) + dạng 3 (so sánh). 6 dạng còn lại phù hợp:

| Dạng | Khi nào dùng |
|---|---|
| **4. Top list** ⭐ RECOMMEND | Khi có 5-7 tiện ích/tính năng muốn liệt kê |
| 7. Myth-bust | Khi muốn phá vỡ hiểu lầm phổ biến |
| 5. Before/After | Khi có visual proof rõ ràng |
| 1. Tutorial | Khi SP có cách dùng đặc biệt cần dạy |
| 6. Story | Khi có câu chuyện cá nhân |
| 8. Q&A | Khi user có câu hỏi cụ thể |

**Default nếu user không chỉ định:** DẠNG 4 (Top list) vì dễ viral + dễ lưu + dễ làm.

### Step 4: VIẾT SCRIPT với insight thật + tiện ích cụ thể

**Cấu trúc 60s (DẠNG 4 - Top list):**
```
[HOOK — 0-3s] Con số + Open loop
VD: "Bút iPad 500k. 5 tiện ích mà bạn chưa biết — đặc biệt số 3."

[TỪNG TIỆN ÍCH — 8-10s mỗi cái]
Mỗi tiện ích: lời nói + visual demo + text overlay
Công thức: [TÊN TIỆN ÍCH] + [CÁCH DÙNG] + [TIỆN DỤNG CHO AI]

[CTA — 5-8s] Tổng kết insight thật
VD: "Tương đồng 90%, rẻ hơn 4-5 lần. Mua về thử, không hợp vẫn quay lại Pencil."
```

**Nguyên tắc 3 điểm:**
1. **KHÔNG so sánh trực tiếp** với đối thủ chính hãng
2. **Mỗi tiện ích phải có "tiện dụng cho ai"** (target audience rõ)
3. **CTA dùng insight thật** của user (nếu có) → tạo tâm lý "thử trước, không mất gì"

### Step 5: CÓ NHƯỢC ĐIỂM TRUNG THỰC (theo Hiến pháp)
- Top list KHÔNG có nghĩa là chỉ liệt kê ưu điểm
- 1 tiện ích cuối (hoặc 1 dòng riêng) phải nêu nhược điểm thật
- VD: "Tuy nhiên, vẽ chuyên nghiệp kiểu họa sĩ digital thì Apple Pencil vẫn nhỉnh hơn"

### Step 6: UPDATE FILE + LOG
- Lưu file: `Operations/review-[brand]-[model].md`
- Update `hub.md` log
- Nếu user gửi qua Telegram: dùng `references/send-script-to-telegram.md`

## Real Example: Goojodoq GD15 (2026-06-17)

**Input từ user:**
> "Anh từng dùng qua nhiều dòng iPad và Pencil chính hãng rồi - chỉ thấy điểm Khác biệt giữa cây bút nàyvà cây bút chính hãng là phần luôn kết nối nhanh thao tácnhanh trên thân bút và cảm biến lực nhấn thôi còn lại cảm giác gần như tương đồng. Mà rẻ hơn gấp 4 gấp 5 lần"

**5 tiện ích em chọn (xoay quanh insight của anh):**
1. **Kết nối nhanh** — bật → đặt lên iPad → viết liền (insight: "kết nối nhanh")
2. **Phím tắt vật lý** — bấm 1 lần = tẩy, 2 lần = undo (insight: "thao tác nhanh trên thân bút")
3. **Sạc không dây từ tính** — hít vào cạnh iPad = sạc (tiện ích bổ sung)
4. **Cảm biến lực nhấn** — ấn nhẹ/mạnh → nét mỏng/dày (insight: "cảm biến lực nhấn")
5. **Find My + giá rẻ** — 1/4 Apple Pencil (insight: "rẻ hơn 4-5 lần")

**CTA dùng insight thật:**
> "Tương đồng 90%, rẻ hơn 4-5 lần. Mua về thử, không hợp vẫn quay lại Pencil."

**Kết quả:** Bài review này dùng insight thật làm trọng tâm → user không reject.

## Hard Rules

- **KHÔNG BAO GIỜ dùng format "vs" hoặc "A vs B"** trong hook + body khi user reject so sánh
- **Insight user = nguồn uy tín số 1** — nếu user chia sẻ insight, dùng insight đó làm cốt lõi
- **Dạng 4 (Top list) là default** khi user không chỉ định dạng cụ thể
- **CTA phải có "tiện ích cuối"** (Find My + giá) → tạo kết nối cảm xúc
- **VẪN giữ Hiến pháp 7 điều** (đặc biệt: nhược điểm thật + nhãn affiliate)

## Anti-pattern

- ❌ **Dùng "tương đương" / "ngang hàng"** với đối thủ chính hãng → ngầm thừa nhận sản phẩm mình đang review là "hàng fake"
- ❌ **Liệt kê 10 tiện ích** → quá dài, mất retention
- ❌ **Bỏ qua insight user** → viết generic, mất uy tín
- ❌ **Không có nhược điểm** → vi phạm Hiến pháp điều 2
