# Reference: Step 8 Verify Fail (11/07/2026)

## Vấn đề

Em đã skip Step 8 verify TOÀN BỘ goal. Chỉ check FILLER mà bỏ qua:
- CÂU TREO (câu vô nghĩa/yếu nghĩa)
- LẶP NGHĨA (câu lặp nội dung)
- HOOK LẶP (câu lặp hook)
- ỰM Ỡ (người đang suy nghĩ)

## User feedback (verbatim)

> *"Câu treo, lặp, lỗi, ựm ở còn nhiều, hook lặp cũng còn, em không đọc transcript hả?"*

> *"Em không check câu treo, câu lặp nghĩa trong bước 8 à?"*

> *"Việc verify ở bước 8 là verify lại toàn bộ transcript xem đã đạt được goal yêu cầu của skill chưa chứ không phải chỉ một vài yêu cầu đơn lẻ nha"*

## Anti-pattern vĩnh viễn

❌ **KHÔNG BAO GIỜ** chỉ check 1-2 yêu cầu trong Step 8
❌ **KHÔNG BAO GIỜ** bỏ qua câu treo, lặp nghĩa, hook lặp
❌ **KHÔNG BAO GIỜ** tin tưởng auto-classify 100%

## Pattern BẮT BUỘC

✅ LUÔN check TOÀN BỘ goal (xem skill `tiktok-verify-protocol`)
✅ LUÔN dùng tool `scripts/verify_clip.py` để verify tự động
✅ LUÔN check cả SOURCE transcript và Whisper re-verify file output

## Bài học

Step 8 PHẢI check 5+ loại vấn đề:
1. Filler đứng đầu/cuối câu
2. ỰM Ỡ (1 từ đứng đơn hoặc đầu câu)
3. Câu treo (3-8 từ toàn bridge, không có USP)
4. Lặp nghĩa (2+ từ đầu giống giữa segs liên tiếp)
5. Hook lặp (3+ từ đầu giống cách <15 segs)
6. Spec TikTok (1080×1920, 44100Hz, duration 60-180s)

Nếu bất kỳ check nào fail → quay lại Step 3, sửa keeps, re-render, re-verify.

## Source của lỗi

Bắt nguồn từ việc em skip Bước 3 (ĐỌC-HIỂU-CẢM-XÚC) và tin tưởng auto-classify draft. Sau khi đọc kỹ transcript, em phát hiện rất nhiều:
- SOURCE-LOOP "Các bạn nhìn thấy không?" × 5 lần (C041 seg 13-26)
- HOOK LẶP × 4-5 lần (0713 seg 3-9-23-26)
- TREO dài 7.16s (0713 seg 29)
- ỰM Ỡ "Sao giọng chậm" (C043 seg 1)
- CTA hard-sell lặp 2-4 lần

## Solution

1. Luôn đọc `transcript_full.md` từng seg trước khi chọn keeps
2. Tạo tool `verify_clip.py` để check tự động 5 loại lỗi
3. Re-render và re-verify cho đến khi pass exit 0

## Kết quả fix

Sau fix: 5/5 clip V6 đều pass `verify_clip.py` exit 0
- 0704 V6 = 81.48s ✅
- 0710 V6 = 97.44s ✅
- 0713 V6 = 139.47s ✅
- C041 V6 = 122.19s ✅ (giảm duration từ 192.83s)
- C043 V6 = 101.03s ✅