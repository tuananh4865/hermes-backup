---
title: X.com (Twitter) URL Extraction Workaround
created: 2026-06-18
updated: 2026-06-18
type: reference
tags: [x-twitter, x-com, url-extraction, workaround, social-media]
---

# X.com (Twitter) URL Extraction — Workaround Pattern

**Why this file exists:** X.com aggressively blocks most non-browser HTTP requests. Both `web_extract` (DuckDuckGo backend) and `mcp_exa_web_fetch_exa` fail. This reference documents the WORKING pattern found 2026-06-18.

## Working Pattern (3-step)

### Step 1: Try `mcp_exa_web_search_exa` with full URL as query

```python
mcp_exa_web_search_exa(
  query="<full x.com URL>",
  numResults=5
)
```

**Why this works:** Exa indexes X.com tweets via mirrors (threadreaderapp, instalker, nitter). Search engine returns highlights from these mirrors.

### Step 2: If Step 1 fails, try mirror sites (priority order)

```python
# Priority order (most likely to work)
"https://threadreaderapp.com/thread/<tweet_id>.html"
"https://instalker.org/<username>/status/<tweet_id>"
"https://xcancel.com/<username>/status/<tweet_id>"
"https://nitter.net/<username>/status/<tweet_id>"
```

**Use mcp_exa_web_fetch_exa on these mirrors** (not on x.com directly).

### Step 3: Fallback — search by username + topic

```python
mcp_exa_web_search_exa(
  query="@<username> <topic keyword>",
  numResults=3
)
```

## Output Format

When X.com URL extraction works through a mirror, output MUST:
1. **Acknowledge source:** "Đọc qua [mirror name]" (KHÔNG giả vờ đọc trực tiếp từ x.com)
2. **Cite the mirror link** in any analysis
3. **Note limitations:** Some content may be cached/delayed; engagement metrics may not be realtime

## Tested Cases (2026-06-18)

| URL | Method that worked | Notes |
|-----|---------------------|-------|
| `https://x.com/thedankoe/status/2010751592346030461` | `mcp_exa_web_search_exa` với URL làm query → tìm thấy qua instalker.org | Got full thread content + 1.6K likes, 187M impressions từ profile |
| `https://x.com/<user>/status/<id>` (general) | Mirror sites | thredreaderapp cho full thread, instalker cho individual tweet |

## Common Failures

| Tool | Error | Why |
|------|-------|-----|
| `web_extract` với X.com URL | "DuckDuckGo (ddgs) is a search-only backend" | DDG không fetch, chỉ search |
| `mcp_exa_web_fetch_exa` với X.com URL | "CRAWL_HTTP_400" | X.com chặn crawl |
| `web_extract` với mirror URL | OK nhưng nội dung ngắn | Mirror có thể không index đầy đủ |

## Related

- `telegram-video-analysis` SKILL Pitfall #35 (X.com URL extraction)
- Skill `agent-reach/agent_reach` — for platform-native analysis (nếu có)
- MCP `exa_web_search_exa` — tool reference
