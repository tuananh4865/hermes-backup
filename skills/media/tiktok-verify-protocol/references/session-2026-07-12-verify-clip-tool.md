# Reference: Session 2026-07-12 - Verify Tool Creation + 5 Clip Fix

## Context

Session tạo tool `scripts/verify_clip.py` v3.21.4 để check TOÀN BỘ goal của video edit (5 loại lỗi + spec TikTok). Trước đây chỉ check filler → fail.

## Vấn đề gặp phải

User feedback 11/07 (verbatim):
> *"Em không check câu treo, câu lặp nghĩa trong bước 8 à?"*
> *"Việc verify ở bước 8 là verify lại toàn bộ transcript xem đã đạt được goal yêu cầu của skill chưa chứ không phải chỉ một vài yêu cầu đơn lẻ nha"*
> *"Lặp nghĩa tính từ 2+ từ, hook lặp tính thừ 3+ từ, "ựm" và "ờ" chỉ cần một từ đứng đơn hoặc đứng đầu câu là phải cắt, câu treo là câu vô nghĩa hoặc câu yếu nghĩa từ 3+ từ"*
> *"Update skill luôn + bỏ "đó" và "thì" trong filter"*
> *"Thêm rule system wide để verify lại tất cả các thứ mà em làm ra hoặc tạo ra để đảm bảo em không làm hay tạo ra một thứ vô nghĩa và không hoạt động chỉ mang tính trưng bày... Mỗi rule, fable, loop và Karpathy system đều là bắt buộc và mỗi khi chạy cần có một khẩu hiệu bặt buộc em phải nói ra để anh biết em đang làm"*

## Bài học lớn nhất

**Step 8 KHÔNG ĐƯỢC check từng yêu cầu riêng lẻ** - phải check TOÀN BỘ goal. Trước đây em chỉ check FILLER → 4/5 clip V5 fail vì còn câu treo, lặp nghĩa, hook lặp, Ựm ỡ.

## Tool implementation

```python
# scripts/verify_clip.py v3.21.4
# Check 5 loại lỗi:
# 1. FILLER: ơ, ờ, ừm, ừ, ó, à, á (đầu/cuối câu)
# 2. ỰM/Ờ: 1 từ ờ/à/ừm/ơ đứng đơn hoặc đầu câu
# 3. TREO: câu 3-8 từ toàn bridge không có USP
# 4. LẶP NGHĨA: 2+ từ đầu giống giữa segs liên tiếp
# 5. HOOK LẶP: 3+ từ đầu giống giữa segs cách <15

# Spec TikTok (nếu có render.mp4):
# - 1080×1920
# - 44100Hz
# - Duration 60-180s
```

Source code: 7.7KB tại `~/.hermes/skills/media/tiktok-video-editor/scripts/verify_clip.py`

## Real case 5 clip test

| Clip | V5 issues | V6 final | Status |
|------|-----------|----------|--------|
| 0704 | 1 LẶP NGHĨA (seg 20-21 "Hạt bụi") | 81.48s | ✅ pass |
| 0710 | 1 LẶP + 1 HOOK LẶP | 97.44s | ✅ pass |
| 0713 | 0 (đã đạt từ V5) | 139.47s | ✅ pass |
| C041 | 7 issues (duration >180s + 2 LẶP + 4 HOOK LẶP) | 122.19s | ✅ pass |
| C043 | 1 FILLER "á" + 1 LẶP + 1 HOOK LẶP | 101.03s | ✅ pass |

## Pattern fix từng loại

### LẶP NGHĨA (2+ từ đầu giống)
- **Strategy 1**: Bỏ keep có seg lặp
- **Strategy 2**: Tách keep thành nhiều keep nhỏ hơn

### HOOK LẶP (3+ từ đầu giống)
- **Strategy 1**: Bỏ keep có seg lặp
- **Strategy 2**: Dùng take CUỐI (giữ take mới nhất)
- **Strategy 3**: Đổi bridge filler đầu câu sang cách diễn đạt khác

### Duration > 180s
- **Strategy 1**: Bỏ keep AUTHORITY dài
- **Strategy 2**: Bỏ keep LESS IMPORTANT (PROBLEM bridge, USP tương tự)
- **Strategy 3**: Tăng speed lên 1.4x hoặc 1.5x (cẩn thận với chất lượng audio)

### FILLER "á" cuối câu
- **Strategy**: Cắt keep sớm hơn trước khi "á" xuất hiện (cần word timestamps)

## Filler list v3.21.4 FINAL

```
ơ, ờ, ừm, ừ, ó, à, á
```

**KHÔNG bao gồm:**
- "đó" - đại từ chỉ định ("cái tripod đó", "thời gian đó")
- "thì" - có 2 vai trò (bridge filler + ngữ pháp nối vế "khi X thì Y")

## System-Wide Rule 3: Khẩu hiệu BẮT BUỘC

Format: `🎯 [TÊN HỆ THỐNG]: [mô tả]`

**4 hệ thống bắt buộc:**
1. **Core Philosophy** (4 rules SOUL.md)
2. **Karpathy System** (4 rules CLAUDE.md)
3. **Fable 5 Patterns** (6 patterns)
4. **Loop Engineering** (3 loops)

**3 loops:**
- Verify loop: Tạo → Test → Fail? → Fix → Test lại → Pass
- Self-learning loop: Gặp lỗi → Phân tích → Save wiki → Tránh lặp lại
- Wiki sync loop: Thay đổi skill → Update wiki → Update CHANGELOG

## Lesson vĩnh viễn

1. **KHÔNG BAO GIỜ skip Step 8 verify** - check TOÀN BỘ goal, không phải 1-2 yêu cầu
2. **KHÔNG BAO GIỜ cắt "đó"** - đại từ chỉ định quan trọng
3. **KHÔNG BAO GIỜ cắt "thì" tự động** - khó phân biệt bridge vs ngữ pháp
4. **LUÔN hard check mọi artifact** trước khi báo "xong"
5. **LUÔN nói tên rule** khi apply để anh biết em đang làm gì