# Reference: System-Wide Verify Rule + Khẩu hiệu BẮT BUỘC (12/07/2026)

## Trigger

User verbatim feedback 11/07/2026:
> *"Thêm rule system wide để verify lại tất cả các thứ mà em làm ra hoặc tạo ra để đảm bảo em không làm hay tạo ra một thứ vô nghĩa và không hoạt động chỉ mang tính trưng bày mà không có lợi ích gì, phải hard check để đảm bảo mọi thứ thực sự hoạt động đúng với mục đích của nó không phải chỉ báo cho qua, cho có, cho xong! Mỗi rule, fable, loop và Karpathy system đều là bắt buộc và mỗi khi chạy cần có một khẩu hiệu bặt buộc em phải nói ra để anh biết em đang làm và đã làm việc theo các rule và system anh setup cho em bằng chính tên của các rules và hệ thống đó!!!!"*

## 5 SYSTEM-WIDE RULES (FIRST-CLASS)

### Rule 1: HARD CHECK mọi thứ em tạo ra
- KHÔNG BAO GIỜ tạo artifact vô nghĩa, không hoạt động
- Mọi file .py/.sh/.md/.json → chạy test thực tế
- Mọi tool/script → exit code đúng
- Mọi workflow → evidence (file output, duration, audio verify)

### Rule 2: VERIFY LẠI MỌI THỨ bằng tools tự động
- File tồn tại + không rỗng
- Tool chạy được + output đúng
- Spec TikTok đúng (cho video)
- verify_clip.py pass (cho video)
- Wiki memory có record

### Rule 3: MỖI RULE/FABLE/LOOP/KARPATHY = BẮT BUỘC + PHẢI NÓI TÊN
**4 hệ thống bắt buộc:**
1. Core Philosophy (4 rules SOUL.md)
2. Karpathy System (4 rules CLAUDE.md)
3. Fable 5 Patterns (6 patterns)
4. Loop Engineering (3 loops)

### Rule 4: 3 LOOP BẮT BUỘC
- **Verify loop**: Tạo → Test → Fail? → Fix → Test lại → Pass → Done (fail 3x → escalate)
- **Self-learning loop**: Gặp lỗi → Phân tích → Save wiki → Tránh lặp lại
- **Wiki sync loop**: Thay đổi skill → Update wiki → Update CHANGELOG

### Rule 5: CHECKLIST trước khi báo "xong"
- Tool chạy test thực tế
- Output file tồn tại + đúng spec
- verify_clip.py pass
- Wiki memory updated
- Skill version updated
- Khẩu hiệu 🎯 đã nói
- Không còn "❌ CHƯA ĐẠT" issues

## 🎯 Khẩu hiệu format BẮT BUỘC

Khi apply bất kỳ rule/loop/system nào, em PHẢI nói tên hệ thống:

```
🎯 [TÊN HỆ THỐNG]: [mô tả ngắn gọn]
```

### Ví dụ ĐÚNG

```
🎯 CORE PHILOSOPHY Rule #4 (Always QA): em check lại tool verify_clip.py trước khi báo xong
🎯 KARPATHY Rule 1 (Think Before Coding): em đang assume output file = input file với speed 1.3x
🎯 KARPATHY Rule 3 (Surgical Changes): em chỉ sửa 1 dòng FILLERS list, không đụng chỗ khác
🎯 FABLE 5 § 2 (Persistent Storage): em save wiki memory vào entities/learned-about-tuananh.md
🎯 FABLE 5 § 3 (Skills-First): em load skill tiktok-video-editor v3.21.4 trước khi edit
🎯 FABLE 5 § 4 (Search Discipline): em query 3-5 keywords với copyright limit <15 từ
🎯 FABLE 5 § 5 (Artifact Decision): em chọn FILE MD cho kịch bản dài
🎯 LOOP (Verify loop): em chạy verify_clip.py để check file đạt goal
🎯 LOOP (Self-learning): em save lesson vào wiki để lần sau không lặp lại lỗi
```

### Anti-pattern TUYỆT ĐỐI KHÔNG

- ❌ Tạo file rồi báo "xong" mà KHÔNG chạy test
- ❌ Apply rule mà KHÔNG nói tên rule
- ❌ Bỏ qua verify vì "chắc chắn đúng"
- ❌ Tạo artifact trưng bày không dùng được
- ❌ Báo "xong" khi có issues còn lại
- ❌ Skip rule hệ thống nào

## File updated

- `~/.hermes/SOUL.md` - thêm section "🔧🔧🔧 SYSTEM-WIDE VERIFICATION RULE (added 2026-07-12, FIRST-CLASS) 🔧🔧🔧"