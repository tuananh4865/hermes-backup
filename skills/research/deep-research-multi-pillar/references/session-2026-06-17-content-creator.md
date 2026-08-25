# Session Reference: Content Creator 3-Pillar Research (2026-06-17)

> **Use case:** Tuấn Anh cần deep research 3 trụ nội dung (EDIT + SETUP GÓC QUAY + ÁNH SÁNG CƠ BẢN) cho kênh TikTok giáo dục. Mục tiêu cuối: lộ trình 45 ngày để đạt 10k follow.

## Context

- **Project:** Content Creator tại `/Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/`
- **Pivot quan trọng:** 100% xây thương hiệu cá nhân trước khi bán hàng (45 ngày đầu KHÔNG bán)
- **3 trụ thu hẹp:** EDIT + SETUP GÓC QUAY + ÁNH SÁNG (bỏ GEAR REVIEW trong 45 ngày)
- **Target:** 10.000 follow TikTok trong 45 ngày = 222 follow/ngày
- **Voice:** Trung tính, chuyên nghiệp (KHÔNG "anh"+"mấy con vợ" — HARD RULE 13/06)

## Output structure

Lưu tất cả trong `Research/2026-06-17/`:
```
00-TONG-HOP-3-TRU-COT.md (13KB) — Ma trận tổng hợp, KPI
01-LO-TRINH-45-NGAY-NGUOI-MOI.md (14KB) — Lộ trình 5 giai đoạn cho người mới
deep-research-edit-co-ban.md (40KB) — 30 kịch bản EDIT (10+10+10)
deep-research-setup-goc-quay.md (30KB) — 25 kịch bản GÓC QUAY (5 nhóm)
deep-research-anh-sang-co-ban.md (45KB) — 30 kịch bản ÁNH SÁNG (6 nhóm)
```

## Subagent context template (đã dùng thành công)

```
Bối cảnh: Tuấn Anh là content creator Việt Nam đang xây kênh TikTok giáo dục, 3 trụ nội dung: EDIT + SETUP GÓC QUAY + ÁNH SÁNG CƠ BẢN. Đối tượng: người mới bắt đầu, dùng điện thoại, không cần đồ xịn. Mục tiêu: 45 ngày tới 10k follow bằng 100% nội dung hướng dẫn cơ bản.

Nhiệm vụ: Deep research về [TRỤ]...

Cần tìm: [8-10 items cụ thể + có số liệu]

Output format:
- Markdown tổng hợp 5.000-10.000 từ
- Chia section rõ: A, B, C, D, E, F...
- Ưu tiên nguồn uy tín: [domain cụ thể]
- Có số liệu cụ thể, KHÔNG bịa số
- Trích dẫn nguồn (link + ngày cập nhật)

CHÚ Ý: 
- Chỉ dùng mcp_MiniMax_web_search (KHÔNG dùng web_extract vì hay fail timeout)
- Tập trung 8-10 search queries quan trọng thay vì research quá rộng
- Lấy thông tin từ search snippets + description + title

Lưu file: /Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/Research/2026-06-17/[filename].md
```

## Logic sắp xếp lộ trình đã dùng

**Sắp xếp trụ theo thứ tự học:**
1. EDIT trước (dùng cho mọi video → ROI cao nhất)
2. ÁNH SÁNG tiếp (thấy kết quả ngay → motivation)
3. GÓC QUAY sau (cần video mẫu → chậm hơn)

**5 giai đoạn:**
- N1-7: 1 video/ngày, EDIT cơ bản (làm quen)
- N8-14: 2 video/ngày, EDIT + ÁNH SÁNG
- N15-21: 2 video/ngày, thêm GÓC QUAY
- N22-35: 2 video/ngày, kết hợp 3 trụ
- N36-45: 2-3 video/ngày + F-series (câu chuyện cá nhân)

**Checkpoint KPI:**
- N7: 50-200 follow
- N14: 400-800
- N21: 1.000-1.500 (mốc đầu tiên)
- N35: 3.000-5.000
- N45: 8.000-12.000 (đạt mục tiêu)

## Pitfalls gặp phải + fix

1. **Subagent SETUP GÓC QUAY timeout** → restart với context "CHỈ dùng mcp_MiniMax_web_search, 8-10 query, không web_extract" → thành công
2. **web_extract timeout** → dùng snippet từ search results (đủ thông tin cho research chất lượng)
3. **Output 4 file → cần thêm 1 file "lộ trình" riêng** → vì ma trận tổng hợp (file 00) khác lộ trình cho người mới (file 01). User thường xài file 01 nhiều hơn

## User preferences learned

- Thích em **tự research + tổng hợp + sắp xếp logic** trước khi hỏi → không hỏi từng bước
- Thích **ma trận trực quan** + **lộ trình theo ngày** (không thích "danh sách kịch bản chung chung")
- Sau khi có research, anh thường nói "**sắp xếp lại cho hợp lý người mới**" → đây là pattern lặp lại, cần nhớ
- Voice **trung tính chuyên nghiệp** trong mọi output
