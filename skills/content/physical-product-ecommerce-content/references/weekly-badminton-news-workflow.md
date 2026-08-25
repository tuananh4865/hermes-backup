# Weekly Badminton News + Image Collection Workflow

> **Workflow:** Viết bài Facebook tổng hợp tin tức cầu lông tuần qua cho Tuấn Anh Badminton (page cầu lông), kèm hình ảnh.
> **Verified:** 2026-07-08 from first successful run.
> **Distinct from:** `tiktok-viral-script` (60s video), `tiktok-product-script` (single product), `content-creator-script-style` (3 trụ EDIT/SETUP/ÁNH SÁNG).

## Trigger

User asks any of:
- "Viết bài tổng hợp tin tức cầu lông tuần qua"
- "Tin tức cầu lông hot nhất tuần"
- "Tổng hợp badminton news tuần"
- "Tìm tin cầu lông + hình ảnh + viết bài"

## Output

1. **Markdown file** lưu vào `wiki/projects/tuan-anh-badminton/news/weekly-news-YYYY-MM-DD-to-YYYY-MM-DD.md`
2. **Facebook post ready** (~500-700 chữ, 5 tin tức, kèm ảnh Wikimedia Commons)
3. **Telegram embed** (gửi qua Telegram để anh review ngay trên điện thoại)

## ⚠️ HARD RULE — Pitfall #41: Series-target check TRƯỚC khi gọi giá (Tuấn Anh mandate 08/07/2026)

**Bài học từ session 08/07:** Em viết bài "Astrox 88S PRO" đầu tiên với giá **5,239K** (88S PRO), tưởng đó là flagship Pro. → Sai. Flagship Pro là **Astrox 99 PRO (5,599K, margin 19.6%)**.

**Rule trước khi viết bất kỳ content Tuấn Anh Badminton:**
```
1. CHECK wiki/products-inventory.md → biết cây nào có trong kho
2. CHECK cây nào là FLAGSHIP (margin cao nhất + tier Pro cao nhất + giá cao nhất)
3. NẾU viết về series Pro → MẶC ĐỊNH flagship, không phải cây Pro đầu tiên em nghĩ tới
```

## Workflow 4 bước (đã verified 08/07/2026)

### Bước 1: Xác định khoảng thời gian "tuần qua"

- **Nếu user không nói rõ:** Mặc định "tuần trước so với hôm nay" (7 ngày trước → hôm qua)
- **Ví dụ:** Hôm nay 08/07/2026 → tuần qua = 28/06 - 04/07/2026
- **Ghi rõ trong output:** "Period: YYYY-MM-DD → YYYY-MM-DD"

### Bước 2: Parallel dispatch 2 subagents

**Subagent A — Research tin tức:**
```
INPUT:
- Period: [ngày bắt đầu] → [ngày kết thúc]
- Output: 5 tin nổi bật
- Mỗi tin cần: tiêu đề VN, tóm tắt 1-2 câu, nguồn chính thức, hashtag, ngày

NGUỒN ƯU TIÊN:
- bwfbadminton.com (BWF official)
- vnexpress.net/the-thao/cau-long (VnExpress)
- thethao.thanhnien.vn (Thanh Niên)
- tuoitre.vn/the-thao (Tuổi Trẻ)
- thestar.com.my/sport/badminton (The Star - rất nhiều tin BWF)
- en.wikipedia.org/wiki/2026_BWF_season

LƯU Ý:
- Tin "HOT" = sự kiện lớn (giải đấu, VĐV VN, Yonex news, viral)
- Ưu tiên: VĐV VN (Hải Đăng, Thùy Linh, Đức Phát, Tiến Minh), Yonex, giải BWF Super Series, US Open
- MỖI TIN cần ≥1 nguồn VN + ≥1 nguồn quốc tế (verify)
- KHÔNG lấy tin cũ hơn [ngày bắt đầu]
```

**Subagent B — Fetch ảnh:**
```
INPUT:
- 5 chủ đề ảnh (1 cho mỗi tin)
- Mỗi ảnh cần: URL trực tiếp (không thumbnail), JPEG/PNG ≥800x600, caption VN, license

NGUỒN ƯU TIÊN:
1. Wikimedia Commons (CC-BY-SA / Public Domain)
2. BWF official photos
3. Reuters / Getty Images via Wikipedia
4. Yonex official
5. Báo VN (VnExpress, Thanh Niên, Tuổi Trẻ) — cho phép download

LƯU Ý:
- TUYỆT ĐỐI KHÔNG fabricate URL
- Nếu không tìm được → báo "Không tìm được ảnh cho chủ đề này" + gợi ý
- Verify URL accessible trước khi return
- Wikimedia rate-limit sau nhiều calls → sleep giữa requests
```

### Bước 3: Tổng hợp + viết bài Facebook (parent agent)

**Cấu trúc bài tổng hợp 5 tin:**
```markdown
## Tin 1: [Tiêu đề ngắn gọn, có tên VĐV/giải]
[Tóm tắt 2-3 câu, đủ ý cho người đọc nắm nhanh]
📷 *[Ảnh kèm — caption VN]*

## Tin 2: ...
```

**Quy tắc viết bài tổng hợp:**
- **Xưng hô "bạn - mình"** nhất quán (Pitfall #40)
- **Max 500-700 chữ** cho toàn bài (5 tin)
- **Mỗi tin 2-3 câu tóm tắt** + 1 câu context cho người đọc VN
- **CTA cuối bài:** "Comment bên dưới nhé! Inbox mình nếu cần tư vấn vợt Yonex 🏸"
- **Hashtag cuối bài:** #cầulông #badminton #Yonex #BWF #cầulôngVN (chọn 5-7 phù hợp)

### Bước 4: Save wiki + embed Telegram

**Save wiki:**
```bash
# Path
/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/news/weekly-news-YYYY-MM-DD-to-YYYY-MM-DD.md

# Frontmatter
---
title: Weekly News YYYY-MM-DD to YYYY-MM-DD
created: YYYY-MM-DD
type: project
tags: [project, badminton, news, weekly]
sources: [list of URLs]
---
```

**Telegram embed (cho anh review trên điện thoại):**
- Hiển thị đầy đủ 5 tin trong 1 message
- Bảng ảnh kèm URL ở cuối
- Bảng nguồn (verify) ở cuối
- "Anh copy post Facebook nha!" CTA

## Subagent output verification (Evidence Gate)

Sau khi 2 subagents xong:

| Subagent | Check |
|---|---|
| A (tin tức) | File `badminton_news_weekly_*.md` tồn tại + 5 tin có nguồn + ≥1 nguồn VN/tin |
| B (ảnh) | 5 URLs accessible (curl test) + license rõ ràng |

**Nếu subagent A fail (web_extract broken):** Fallback dùng `mcp__exa__web_search_advanced_exa` + `mcp__exa__web_fetch_exa`.

**Nếu subagent B fail (Wikimedia rate-limited):** Fallback:
1. Sleep + retry
2. BWF official photo gallery (không có direct URL public → dùng venue shot thay thế)
3. Báo VN (VnExpress, Thanh Niên) — cho phép download

## Pitfalls đã verified

| # | Pitfall | Fix |
|---|---|---|
| #41 | Series-target check trước giá (gọi nhầm 88S PRO thay vì 99 PRO flagship) | CHECK inventory wiki + flagship = margin cao nhất |
| #42 | "Subaxia Wide" không tồn tại — phải là Subaxia GT Wide (Pitfall #37 đã có) | Verify SKU trên us.yonex.com |
| #43 | Wikimedia Commons API rate-limit sau nhiều calls | Sleep 2-3s giữa requests |
| #44 | web_extract fail với DuckDuckGo backend | Fallback Exa web_fetch_exa |
| #45 | Không tìm được ảnh cho 1 chủ đề | Báo trung thực + đề xuất thay thế (venue shot / VĐV liên quan) |

## Files created during 2026-07-08 run

- Source data: `/Users/tuananh4865/badminton_news_weekly_2026-06-28_07-04.md` (subagent A output, 5.6 KB)
- Wiki output: `/Volumes/Storage-1/Hermes/wiki/projects/tuan-anh-badminton/news/weekly-news-2026-06-28-to-07-04.md` (6.9 KB)
- Folder mới: `news/` trong project wiki

## Subagent delegation template

Em đã dispatch với template này cho session 08/07 — anh có thể dùng lại cho tuần sau:

```python
delegate_task(tasks=[
    {
        "goal": "Research 5 tin tức cầu lông hot nhất tuần [DATE_RANGE]",
        "context": "[full tin research brief ở Bước 2]"
    },
    {
        "goal": "Fetch 5 ảnh chất lượng cao cho 5 tin tức cầu lông",
        "context": "[full ảnh brief ở Bước 2]"
    }
])
```

## Khi nào KHÔNG dùng workflow này

- ❌ User muốn tin trong NGÀY (không phải tuần) → research trực tiếp, không cần workflow
- ❌ User muốn tin về 1 VĐV cụ thể → research focused, không phải tổng hợp
- ❌ User muốn phân tích chuyên sâu 1 sự kiện (không phải tổng hợp)
- ❌ User muốn viết blog post dài về lịch sử cầu lông → khác format hoàn toàn