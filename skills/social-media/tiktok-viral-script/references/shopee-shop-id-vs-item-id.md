---
title: Shopee URL — shop_id vs item_id (Critical Distinction)
description: Khi user share Shopee product link, 1 shop có thể bán NHIỀU sản phẩm. Phân biệt shop_id (cửa hàng) vs item_id (sản phẩm cụ thể) trước khi research. Real failure 17/06/2026: agent research sai vì chỉ dựa vào shop name.
type: reference
related: [tiktok-viral-script, product-review-research-protocol]
---

# Shopee URL — shop_id vs item_id (Critical Distinction)

> **Created:** 2026-06-17
> **Source:** Real failure khi user gửi 2 link cùng shop Goojodoq (i.958778013) nhưng 2 sản phẩm khác nhau (GD14 vs GD15)
> **Skill governing:** `tiktok-viral-script`

---

## 🚨 Trap: 1 Shop = NHIỀU sản phẩm

**Shopee URL format:**
```
https://shopee.vn/product/{shop_id}/{item_id}
```

| Phần | Ý nghĩa | Ví dụ |
|------|----------|-------|
| `shop_id` | ID CỬA HÀNG (shop) | `958778013` = Goojodoq Official |
| `item_id` | ID SẢN PHẨM cụ thể | `29283646497` = GD15 (khác `29904978002` = GD14) |

**Real failure (17/06/2026):**
- User gửi link 1: `i.958778013.29904978002` → sản phẩm GD14
- User gửi link 2: `i.958778013.29283646497` → sản phẩm GD15 (2025, KHÁC GD14)
- Agent chỉ dựa vào shop name "Goojodoq" → research theo GD14 (đã có data cũ) → viết review sai
- User phải nói: *"Đây mới đúng là sp anh đang có"* mới sửa
- → Mất 1 lượt + viết sai sản phẩm ban đầu

---

## ✅ Rule (BẮT BUỘC khi user share Shopee link)

### Bước 1: Extract cả 2 ID từ URL

```python
import re
url = "https://shopee.vn/product/958778013.29904978002"
match = re.search(r'product/(\d+)\.(\d+)', url)
shop_id = match.group(1)   # "958778013"
item_id = match.group(2)   # "29904978002"
```

**Nếu URL format khác** (vd `?item_id=...&shop_id=...`):
```python
import re
url = "https://shopee.vn/Bút-Cảm-Ứng...?item_id=29904978002&shop_id=958778013"
shop_id = re.search(r'shop_id=(\d+)', url).group(1)
item_id = re.search(r'item_id=(\d+)', url).group(1)
```

### Bước 2: Verify sản phẩm CỤ THỂ (KHÔNG chỉ dựa shop name)

**Phương pháp verify (chạy tuần tự):**

| # | Method | Cách làm | Khi fail |
|---|--------|----------|----------|
| 1 | **URL title decode** | Đọc slug trong URL (ví dụ: `Bút-Cảm-Ứng-Goojodoq-GD15-mới-2025-...` → GD15) | Shopee có thể đổi slug |
| 2 | **Web search theo item_id** | Search: `site:shopee.vn "<item_id>"` hoặc brand + item_id | Không có data |
| 3 | **Web search theo URL title** | Search: `"<tên SP từ slug>" review specifications` | Có thể trùng tên |
| 4 | **MCP web search** | `mcp_MiniMax_web_search(query="<brand> <item_id>")` | API block |
| 5 | **HỎI USER** (exception duy nhất) | "Link này là SP nào trong shop Goojodoq?" | User confirm |

### Bước 3: Nếu KHÔNG xác định được → HỎI USER

**Đây là EXCEPTION duy nhất trong URL-First Protocol được phép hỏi:**

> *"Anh ơi, link này có item_id `{item_id}` — em không rõ là sản phẩm nào trong shop `{shop_name}`. Anh confirm giúp em tên sản phẩm?"*

**KHÔNG hỏi** các câu chung chung kiểu "anh muốn gì?" hay "có cần research thêm không?" — vẫn vi phạm HARD RULE.

### Bước 4: Sau khi verify, document trong file review

Mỗi file review PHẢI có:
```yaml
product_url: <full URL>
product_shop_id: <shop_id>
product_item_id: <item_id>
product_name: <tên SP chính xác>
verified_at: <YYYY-MM-DD>
```

→ Nếu sau này Shopee đổi slug, vẫn còn item_id để search lại.

---

## 🛡️ Anti-patterns (TRÁNH)

### ❌ Anti-pattern 1: "Shop name = enough"
```
User: "review cho https://shopee.vn/product/958778013.29283646497"
Agent: "Goojodoq Official → assume là GD14 (sản phẩm phổ biến nhất)"
→ SAI: 1 shop có thể có 50+ sản phẩm
```

### ❌ Anti-pattern 2: "URL title đủ rõ rồi"
```
URL: shopee.vn/Bút-cảm-Ứng-Goojodoq-GD15-...-i.958778013.29283646497
Agent: "URL title nói GD15 → research GD15"
→ ĐÚNG nhưng: cần cross-check với search vì Shopee có thể đổi slug, dùng slug cũ cho SP mới
```

### ❌ Anti-pattern 3: "Có data GD14 rồi, dùng lại"
```
User share link GD15
Agent: "Goojodoq → reuse research GD14 → chỉnh số"
→ SAI: GD15 có tính năng KHÁC (sạc không dây) so với GD14 → không thể reuse
```

### ❌ Anti-pattern 4: "User nói 'Goojodoq' → research tất cả"
```
User: "review cho bút Goojodoq"
Agent: "Goojodoq có 5 dòng bút → research tất cả"
→ KHÔNG hiệu quả. Cần URL hoặc tên SP cụ thể
```

---

## ✅ Patterns (ĐÚNG)

### ✅ Pattern 1: Extract ID + verify
```
User: "https://shopee.vn/product/958778013.29283646497"
Agent:
  1. Extract: shop_id=958778013, item_id=29283646497
  2. URL title: "Bút-cảm-Ứng-Goojodoq-GD15-mới-2025-..." → GD15
  3. Search: "Goojodoq GD15 2025" → confirm GD15 mới 2025
  4. Research GD15 (ít data hơn GD14) → báo cáo trung thực
```

### ✅ Pattern 2: User cung cấp tên SP → trust user
```
User: "review cho GD14, link https://shopee.vn/product/958778013.29904978002"
→ User đã nói rõ GD14 → research GD14 (URL title cũng confirm)
```

### ✅ Pattern 3: Hỏi khi ambiguous
```
User: "review cho bút mới của Goojodoq"
User không share URL
→ Agent: "Anh dùng dòng nào? GD14, GD15, hay khác?"
→ User: "GD15"
→ Research GD15
```

---

## 📊 Mapping các Shop phổ biến (đã verify 17/06)

| Shop | shop_id | Nhiều SP? | Cần verify item_id? |
|------|---------|-----------|---------------------|
| Goojodoq Official | 958778013 | ✅ CÓ (GD13, GD14, GD15, GD16, GD17...) | **LUÔN** |
| Apple Flagship | (khác) | ✅ CÓ (nhiều SP) | **LUÔN** |
| Shopee Mall (lớn) | (khác) | ✅ CÓ | **LUÔN** |
| Shop cá nhân | (khác) | Thường 1-5 SP | Vẫn nên verify |

**Rule of thumb:** BẤT CỨ shop nào cũng có thể có nhiều SP. LUÔN verify item_id trước khi research.

---

## 🔗 Workflow tích hợp

Khi user share Shopee URL, kết hợp với `product-review-research-protocol.md`:

```
Bước 0: Extract shop_id + item_id
Bước 1: Verify sản phẩm (URL title + web search)
Bước 1.5: Nếu ambiguous → HỎI USER (exception duy nhất)
Bước 2-6: Protocol viết review (xem product-review-research-protocol.md)
```

---

## 🆕 FAILURE LOG

**2026-06-17 — Agent research sai sản phẩm (GD14 thay vì GD15):**
- Trigger: User share link mới `i.958778013.29283646497` (GD15) sau khi đã review GD14
- Failure: Agent không extract item_id, chỉ dựa vào "shop Goojodoq" → reuse research GD14 cũ
- Consequence: Mất 1 lượt (user phải nói "đây mới đúng là sp anh đang có")
- Fix: Add this reference file + patch product-review-research-protocol.md workflow

---

## Related

- `references/product-review-research-protocol.md` — Workflow 6 bước viết review
- `references/hien-phap-7-dieu-content-creator.md` — 7 quy tắc BẮT BUỘC
- `references/send-script-to-telegram.md` — Workflow gửi script qua Telegram
