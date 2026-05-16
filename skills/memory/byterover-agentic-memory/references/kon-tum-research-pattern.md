# Kon Tum Research Pattern — Vietnamese Local Business Research

**Date:** 2026-05-16  
**Session:** `session_20260516_202416_ef3a9243`  
**Trigger:** User asked for local Kon Tum brands/businesses with many reviews

---

## Key Finding

**Google Maps browser approach FAILS for Vietnamese local business research.**  
Web search (MiniMax MCP) is MORE RELIABLE.

### What Failed
```bash
browser_navigate → Google Maps → "Thương hiệu địa phương Kon Tum"
# Result: empty pages, limited view warnings, no useful data
```

### What Worked
```bash
mcp_MiniMax_web_search → parallel searches for:
- "Quán ăn ngon Kon Tum nổi tiếng"
- "Cà phê Kon Tum địa phương nổi tiếng"
- "Đặc sản Kon Tum"
```

---

## Verified Kon Tum Establishments (May 2026)

### Coffee Shops (most lack websites)
| Name | Reviews | Rating | Website |
|------|---------|--------|---------|
| Eva Cafe | 156 | 4.8★ | ❌ None |
| Tiệm Cà Phê Gác Xép | - | - | ❌ None |
| Xô Xôn Café | - | - | ❌ None |
| Indochine Coffee | - | - | ❌ None |
| Your Coffee | - | - | ❌ None |
| Lynn Coffee | - | - | ❌ None |
| Dream Coffee | - | - | ❌ None |
| Mandela Coffee | - | - | ❌ None |
| Passion Coffee | - | - | ❌ None |
| Chang Coffee & Homestay | - | - | ❌ None |

### Restaurants
| Name | Notes |
|------|-------|
| Gỏi lá Yến Vy | Top 10 VN specialty |
| Nhà hàng Thủy Tạ | |
| Sân Vườn Đồi Tuyết | |
| Hội Ngộ Quán | |

### Local Specialties
- **Bún đỏ cao nguyên** — Highland red noodles
- **Gỏi lá Kon Tum** — Top 10 Vietnamese dish
- **Heo Măng Đen quay** — Roasted Măng Đen pig
- **Cá chua** — Sour fish
- **Rượu vang sim Măng Đen** — Măng Đen sim wine

### Other
- Vincom Plaza Kon Tum
- Sakura KonTum Spa & Wellness

---

## Pattern for Future Vietnamese Local Research

**Rule:** For Vietnamese local business/brand research:
1. Skip Google Maps browser — returns limited views for Vietnamese queries
2. Use `mcp_MiniMax_web_search` (or similar web search MCP) — more reliable
3. Most Vietnamese provincial establishments (cafes, restaurants) lack websites — only Facebook/Google Maps/TripAdvisor

**Verified paths (May 2026):**
- Web search: MiniMax MCP `web_search` tool
- Fallback: browser with web search engine directly

---

## Research Request Template

When user asks for "local [province/city] brands/businesses with many reviews":

```python
# 1. Try web search first (not Google Maps browser)
results = web_search([
    "Thương hiệu địa phương [PROVINCE]",
    "Quán ăn ngon [PROVINCE] nổi tiếng",
    "Cà phê [PROVINCE] địa phương nổi tiếng",
    "Đặc sản [PROVINCE]"
])

# 2. Compile results by category (food, coffee, specialties)
# 3. Note which establishments lack websites
```

---

**Source:** session_20260516_202416_ef3a9243 (Telegram session, May 16 2026)
