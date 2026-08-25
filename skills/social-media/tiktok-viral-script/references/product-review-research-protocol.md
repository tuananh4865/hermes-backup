---
title: Product Review Research Protocol
description: Workflow 6 bước viết review sản phẩm cho Content Creator project (TikTok + YouTube). Cộng thêm format preference (16/06): GỌN > DETAIL.
type: reference
related: [tiktok-viral-script, hien-phap-7-dieu-content-creator, universal-vs-niche-topic-research]
---

# Product Review Research Protocol

> **Tạo:** 2026-06-16 (sau review Goojodoq GD14)
> **Skill governing:** `tiktok-viral-script`
> **Output path:** `Operations/review-[brand]-[model].md` (root) hoặc `Operations/review-[brand]-[model]-v1-chitiet.md` (bản chi tiết archive)

---

## Workflow 6 bước viết review sản phẩm

### Bước 1: URL-First Protocol (EXTENDED 2026-06-17)

Khi user share link Shopee/TikTok Shop, **đừng đoán nội dung**:

**Ladder 7 bước (chạy tuần tự, 1 lần mỗi bước, KHÔNG loop):**

| # | Method | Khi nào fail | Note |
|---|--------|--------------|------|
| 1 | `web_extract(urls=[link])` | DDG-only backend, Shopee blocked | Verify backend trước |
| 2 | `curl -A "Mozilla/5.0 ..." <url>` → grep `"name":"..."` | HTML render JS, tĩnh rỗng | Shopee không có OG meta trong SSR |
| 3 | `POST /api/v4/pdp/get_pc` với `{item_id, shop_id}` | Trả 90309999 (token thiếu) | Cần session cookie + csrf token thật |
| 4 | `mcp_exa_web_fetch_exa(urls=[link])` | MCP thường disconnected | Switch sang `mcp_MiniMax_*` |
| 5 | `mcp_MiniMax_web_search(query="<item_id>")` | Không match sp cụ thể | Chỉ trả shop chung, không trả sp |
| 6 | `computer_use(action="capture")` → navigate | Mac locked, 0x0 capture | Cần Mac unlocked, app foreground |
| 7 | **URL title decode** + domain knowledge | ALWAYS WORKS | Last reliable fallback |

**HARD RULE: KHÔNG DỪNG Ở BƯỚC 6 ĐỂ HỎI USER.**

Sau khi cả 6 methods fail → BẮT BUỘC sang bước 7 ngay, KHÔNG hỏi user "gửi screenshot giúp em". Decode URL title + áp dụng product knowledge → deliver best-effort analysis với caveat "Live data chưa verify được" → đưa 4 options A/B/C/D cho user chọn next step.

**Anti-pattern (17/06/2026, lần 1):** Thử 5 methods rồi BÁO FAIL + xin user gửi screenshot. → Vi phạm HARD RULE "research → verify → deliver, không hỏi". Fix: Nếu URL có cấu trúc rõ (Shopee, TikTok Shop, Amazon) → URL title decode LUÔN THÀNH CÔNG vì slug chứa brand + type + spec + compat. Phải chạy method 7 trước khi considered "fail".

**Tool-specific notes (cập nhật 17/06):**
- `web_extract` với Shopee → DDG search-only, KHÔNG extract được. Nếu `web.extract_backend` để mặc định (ddg) → fail ngay. Phải đổi backend `firecrawl/tavily/exa/parallel` (cần config).
- `mcp_exa_*` thường disconnected trong profile này → KHÔNG retry, switch `mcp_MiniMax_*`.
- `computer_use` cần Mac UNLOCKED. Nếu capture trả về 0x0 với `app: BetterDisplay` → screen locked, không phải tool broken. Dừng method này, decode URL.
- `mcp_MiniMax_web_search` KHÔNG có `site:` operator (MCP block 1027-error) → dùng brand name plain keyword.

### Bước 2: Research 3-5 nguồn uy tín (PARALLEL)

Mỗi nguồn cần URL + ngày truy cập. Đối chiếu ≥2 nguồn cho mỗi thông số chính.

**Nguồn ưu tiên cho review sản phẩm tech/gadget VN:**
- **Tinhte.vn** — review tiếng Việt chất lượng cao, cộng đồng lớn
- **Parka Blogs** — review chuyên sâu tiếng Anh (Singapore)
- **Reddit** (r/<relevant>) — user experience thật
- **YouTube reviews** (yt-dlp transcript) — visual + audio
- **DHgate/AliExpress product page** — spec chính hãng
- **Shopee VN listing** — giá chính thức VN

### Bước 3: Verify spec ≥2 nguồn

Mỗi spec phải có 2+ nguồn đồng ý. Spec chỉ có 1 nguồn → ghi "theo [nguồn]" hoặc bỏ.

### Bước 4: Tìm nhược điểm THẬT (HARD RULE)

Đây là khác biệt giữa creator uy tín vs spam affiliate.

**Cách tìm nhược điểm thật:**
- Đọc review 1-2 sao trên Shopee/Lazada/Tiki
- Hỏi Reddit: "any downsides?" hoặc "should I buy?"
- So sánh với đối thủ cùng tầm giá
- Đọc comments Tinhte.vn (cộng đồng VN rất thẳng thắn)
- Nếu sản phẩm thực sự không có nhược điểm → KHÔNG review

### Bước 5: So sánh ngoại hình TRỰC TIẾP với đối thủ chính

**Bắt buộc cho sản phẩm Apple/Apple-alternative:** so sánh bảng ngoại hình với Apple Pencil (màu, chất liệu, hình dáng, cổng sạc, nút bấm, magnetic, Find My, pressure).

**Cấu trúc bảng:**
| Tiêu chí | [Sản phẩm review] | [Apple Pencil 2 / đối thủ chính] |
|---|---|---|

### Bước 6: Viết script 60s + checklist

**Script 60s formula (BAB hoặc PAS):**
- Hook (0-3s): So sánh giá sốc HOẶC câu hỏi
- Before (3-10s): Pain point của đối tượng
- After (10-40s): 5-6 tính năng chính (đã verify)
- Bridge (40-50s): 2-3 nhược điểm thật (HARD RULE)
- CTA (50-60s): "Mua về dùng thử rồi kể mình nghe nha"

**Checklist 10 điểm trước đăng** (xem `bo-cong-thuc-viral-ke-chuyen.md` Phần 5)

---

## ⚠️ HARD RULE bắt buộc (theo Hiến pháp 7 điều)

Khi viết review, PHẢI thừa nhận:
- Nếu em CHƯA tự mua + test → ghi rõ "phân tích dựa trên review uy tín, chưa tự test"
- Recommend user mua + dùng 1 tuần trước khi quay
- KHÔNG bịa cảm nhận cá nhân ("mình thấy mượt lắm") khi chưa dùng
- ≥1 nhược điểm thật trong video (Hiến pháp điều 2)
- Gắn nhãn tiếp thị liên kết (Hiến pháp điều 3)
- Lời hứa hook phải khớp nội dung (Hiến pháp điều 4)

---

## 🆕 FORMAT PREFERENCE — GỌN > DETAIL (16/06, verified)

**User explicitly trimmed detailed review (v1) → minimal review (v2).** Quoted feedback:

> *"em chỉ cần dựa vào điểm mạnh và nhước điểm để làm bài review thôi! ngoại hình thì xem ảnh trong link để đánh giá với bút apple pencil"*

**Rule for product reviews (apply by DEFAULT unless user asks for detail):**

| Section | KEEP | DROP |
|---|---|---|
| Research | 3-5 nguồn uy tín, URL + date | Không cần 5+ nguồn (3 đủ) |
| Specs | ❌ BỎ bảng thông số đầy đủ | Pin, weight, dimensions, full spec table |
| Điểm mạnh | ✅ 5-7 verified ≥2 nguồn | |
| Nhược điểm | ✅ 5-7 thật (verify ≥1 nguồn) | |
| Ngoại hình | ✅ BẢNG SO SÁNH TRỰC TIẾP với Apple Pencil (cho sản phẩm Apple) hoặc đối thủ chính (cho Android) | |
| Script | ✅ 60s, gọn | |
| V1 vs V2 | Nếu đã viết bản detail trước → KHÔNG xóa, archive `*-v1-chitiet.md` tham khảo | |

**Trigger signals để viết GỌN (mặc định):**
- User nói "chỉ cần" / "gọn" / "bỏ specs" / "chỉ X và Y"
- User share link Shopee mà KHÔNG nói "research kỹ" / "viết chi tiết"
- User share link Shopee kèm tên SP rõ ràng (không phải niche mới)

**Trigger signals để viết CHI TIẾT:**
- User nói "research kỹ" / "phân tích sâu" / "viết chi tiết"
- User nói "đánh giá toàn diện"
- Sản phẩm thuộc niche mới mà user chưa biết

**Anti-pattern (đã fail 1 lần 16/06):** Sau khi research 5 nguồn, viết bản review 15KB với 7 sections + bảng specs đầy đủ → user phải yêu cầu viết lại gọn. Mất 1 lượt. Bài học: nếu user share URL Shopee/TikTok Shop mà KHÔNG nói "research kỹ" → MẶC ĐỊNH viết gọn.

**Trade-off:** V1 hữu ích cho deep research; V2 tốt cho hành động. Mặc định V2, trừ khi user nói "nghiên cứu sâu" / "phân tích kỹ".

**Real session example (16/06):**
- V1 = 15KB với research 5 nguồn + 7 điểm mạnh + 7 nhược + 7 spec rows + 9 shot list
- V2 = 14KB chỉ giữ: research 3 nguồn + 7 điểm mạnh + 7 nhược + 1 bảng so sánh ngoại hình 11 dòng + 7 shot list
- V1 archive thành `review-goojodoq-gd14-v1-chitiet.md`

---

## Failure log

**2026-06-17 — Agent stopped at 5 methods + asked user for screenshot (HARD RULE violation):**
- User share `https://shopee.vn/product/958778013/29283646497` link (no context).
- Agent tried 5 methods: `web_extract` (DDG fail) → `curl` (empty HTML) → Shopee API 90309999 → `mcp_exa_web_fetch_exa` (MCP disconnected) → `mcp_MiniMax_web_search` (no match) → `computer_use` (Mac locked, 0x0) → STOPPED + asked user to send screenshot.
- **VIOLATION:** HARD RULE 1 (research → verify → deliver) + decision-guard (don't ask "anh muốn gì?").
- **FIX APPLIED:** Bước 1 protocol extended to 7-step ladder. After method 6 fail → MUST proceed to method 7 (URL title decode + product knowledge) and deliver best-effort analysis. NO-ASK fallback.
- **Lesson:** Stopping to ask user for screenshot = same class of error as "em cần hỏi thêm để hiểu yêu cầu". Both violate ownership. URL title decode is the always-works fallback — must use it before considered "failed".

**2026-06-16 — User explicitly trimmed V1 → V2 (saves 1 turn):**
- V1 mặc định quá verbose (7 sections + specs + nhiều bảng)
- User feedback: "em chỉ cần dựa vào điểm mạnh và nhước điểm"
- Fix: Khi share link Shopee + không nói "research kỹ" → mặc định V2 format (gọn, ưu + nhược + so ngoại hình + script ngắn)

**2026-06-16 — Topic fail (HDR):**
- Viết review cho "Bút cảm ứng HDR" → user feedback: "không phải điện thoại nào cũng có, không phải ai cũng cần"
- Fix: Universal topic filter (xem `universal-vs-niche-topic-research.md`)

**2026-05-13 — Assumed URL content without reading:**
- Assumed @ecom_linus tweet was about "TikTok algorithm" without reading — actually about AI UGC + affiliate
- Fix: Always URL-First Protocol (Bước 1) trước khi research

---

## Reference

- **Source gốc:** Session 16/06/2026 (review Goojodoq GD14)
- **Skill governing:** `tiktok-viral-script` (umbrella)
- **Related references:**
  - `hien-phap-7-dieu-content-creator.md` — 7 quy tắc BẮT BUỘC
  - `universal-vs-niche-topic-research.md` — Topic filter (cho series "0 đồng")
  - `script-review-then-rewrite-workflow.md` — Workflow review + rewrite
  - `competitor-u40hoc-xaykenh-analysis.md` — Pattern viral cho Content Creator niche
- **Real example files:**
  - V1: `Operations/review-goojodoq-gd14-v1-chitiet.md` (15.4KB, 320 dòng, archived)
  - V2: `Operations/review-goojodoq-gd14.md` (14KB, 288 dòng, active)
