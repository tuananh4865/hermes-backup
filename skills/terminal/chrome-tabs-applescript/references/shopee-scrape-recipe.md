# Shopee VN Product Scraping Recipe

**Verified:** 2026-06-17, session 2026-06-17
**Target:** Bút cảm ứng Goojodoq GD15 (Shop ID 958778013, Item ID 29283646497)
**Source URL:** https://shopee.vn/product/958778013/29283646497

## Why this recipe

Shopee VN aggressively blocks every standard scraping path:

| Path tried | Error observed |
|------------|----------------|
| `web_extract` (Hermes built-in) | "DuckDuckGo is search-only" |
| `curl` with browser UA | Empty `<body>` — page is SPA, JS-rendered |
| Shopee API `/api/v4/pdp/get_pc` | `{"error": 90309999}` — missing auth token |
| Shopee API `/api/v4/pdp/product/get` | `{"error":"error_not_found"}` — needs proper cookie |
| `mcp_exa_web_fetch_exa` | "MCP server not connected" |
| `mcp_MiniMax_web_search` | No match for specific item ID (only generic shopee.vn results) |

The **only path that works** is: ask the user's real Chrome (which is already logged into Shopee)
to run JavaScript and return `document.body.innerText`.

## Full recipe

```bash
# 1. Open URL in a new tab in the user's real Chrome
osascript -e 'tell application "Google Chrome"
    activate
    tell front window
        make new tab with properties {URL:"https://shopee.vn/product/958778013/29283646497"}
    end tell
end tell'

# 2. Wait for Shopee SPA to render (8s is safe, sometimes 12s if Shopee shows captcha)
sleep 10

# 3. Find the new tab and extract its body text via JS injection
SCRIPT='
tell application "Google Chrome"
    tell front window
        set cnt to count of tabs
        repeat with j from 1 to cnt
            if (name of tab j) contains "Goojodoq" then
                set active tab index to j
                tell tab j
                    return execute javascript "document.body.innerText"
                end tell
                exit repeat
            end if
        end repeat
    end tell
end tell'
PAGE_TEXT=$(osascript -e "$SCRIPT" 2>&1)
echo "$PAGE_TEXT"
```

## What you get

`document.body.innerText` returns the rendered product page as plain text, in this order:

1. Site nav chrome (skip these lines)
2. **Product title** — single line
3. **Rating** — e.g. `4.8\n771\nĐánh Giá` (rating, count, label)
4. **Price** — e.g. `468.280₫` and `Giá Sau Voucher` + voucher pills (8%/6%/5%/30k/60k)
5. **Shop info** — `ShopName\nOnline X Phút Trước\nChat Ngay\nXem Shop`
6. **Shop metrics** — `233,3k\nTỉ Lệ Phản Hồi\n100%\nTham Gia\n3 năm trước\nSản Phẩm\n316\nThời Gian Phản Hồi\ntrong vài phút\nNgười Theo Dõi\n457,6k`
7. **CHI TIẾT SẢN PHẨM** block — `Danh Mục`, `Thương hiệu`, `Tính năng`, `Loại bảo hành`, `Gửi từ`
8. **MÔ TẢ SẢN PHẨM** block — multi-paragraph product description, each paragraph prefixed with `✔️`
9. **ĐÁNH GIÁ SẢN PHẨM** block — rating distribution (`5 Sao (695)`, `4 Sao (36)`, ...)
10. **Customer reviews** — `[username]\n[date] [time] | Phân loại hàng: [variant]\n[review text]\n0:0N\nPhản Hồi Của Người Bán\n[seller reply]`

## Parsing tips

- **Price:** regex `r'(\d{1,3}(?:\.\d{3})+|\d+)₫'` or split on lines containing `₫`
- **Rating:** first number after the title (usually `4.7`, `4.8`, `4.9`)
- **Shop followers:** look for `Người Theo Dõi\n<number with k/M>`
- **Product description:** everything after `MÔ TẢ SẢN PHẨM` until `ĐÁNH GIÁ SẢN PHẨM`
- **Reviews:** each entry starts with a username, ends with a seller reply (`Phản Hồi Của Người Bán`)

## Pitfalls specific to Shopee

1. **Tab may NOT appear in `front window` if Chrome was not active when `make new tab` ran.**
   Always enumerate `every window` to find the new tab:
   ```bash
   osascript -e 'tell application "Google Chrome"
       set output to ""
       set wc to count of windows
       repeat with i from 1 to wc
           set w to window i
           set tc to count of tabs of w
           repeat with j from 1 to tc
               if (name of tab j of w) contains "Goojodoq" then
                   set output to output & "FOUND W" & i & "T" & j & linefeed
               end if
           end repeat
       end repeat
       return output
   end tell'
   ```

2. **Shopee may show a CAPTCHA challenge** ("Xác minh bạn là người" puzzle) instead of the
   product page. In that case, `innerText` will contain "Xác minh" and no product data.
   The user must solve it in their real Chrome; you cannot bypass from the script side.

3. **Two consecutive `osascript` calls for the same tab may fail** if the tab is mid-navigation.
   Always `sleep 2-3s` between `make new tab` and the JS extraction, even if you've already
   slept 8s once. AppleScript ↔ Chrome communication is not synchronous.

4. **The product page sometimes shows 0 reviews initially** if Shopee's lazy-load hasn't fired.
   The `innerText` is correct but incomplete. If you need real review counts, parse the review
   block and check that the bracket-counters (`5 Sao (695)`) are present.

5. **`open location` reuses the active tab** — it does NOT open a new tab. To open a new tab,
   use `make new tab` with the `with properties {URL:...}` clause, NOT `open location`.

6. **Shopee variant tracking.** Product detail block has `Tính năng: Bút cảm ứng riêng biệt`
   — this is the variant type. Reviews have `Phân loại hàng: Trắng` etc. — extract these to
   build a per-variant review breakdown.

## Same recipe works for TikTok Shop, Lazada VN, Tiki

The same AppleScript + JS-injection approach works for all major VN e-commerce sites. The
`site:` operator is irrelevant — what matters is that the user is logged into their Chrome
on that site, and that you enumerate tabs by title to find the right one.
