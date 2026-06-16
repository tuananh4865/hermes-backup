---
title: MCP Web Search — Content Moderation Quirks
created: 2026-06-16
type: reference
tags: [mcp, search, workaround, content-moderation, 1027-error]
---

# MCP Web Search — Content Moderation Quirks

**Scope:** This reference covers MCP web search tool quirks specific to the `mcp_MiniMax_*` and `mcp_exa_*` family of tools. These are backend-level behaviors of the search provider, not MCP protocol issues.

## Quirk 1: `site:` Operator Triggers `1027-output new_sensitive`

**Symptom:**

```python
mcp_MiniMax_web_search("TikTok Shop Vietnam trending products site:findniche.com OR site:fastmoss.net")
# Returns: Failed to perform search: API Error: 1027-output new_sensitive Trace-Id: 0680b2245062cb2578c69633bda9f792
```

**Root cause:** The MCP backend's content moderation layer flags Google `site:` operator combined with certain product/trending keywords as potentially sensitive query. This is a backend filter, not a query syntax error.

**Workaround (3-step fallback):**

### Step 1: Plain keyword search

```python
# Instead of: site:findniche.com
# Use: "findniche" as a regular keyword
mcp_MiniMax_web_search("findniche tiktok shop vietnam trending products")
# Returns 10 organic results including findniche.com URLs
```

### Step 2: Add language-specific terms

For Vietnamese sources, include Vietnamese keywords to bias the search:

```python
mcp_MiniMax_web_search("findniche tiktok shop vietnam sản phẩm viral tháng 6 2026")
# Returns 10 results with mix of VN + international
```

### Step 3: Date-specific keywords (replaces `maxAgeHours` parameter)

MCP backend may not support `maxAgeHours` parameter for some implementations. Use natural language date hints:

```python
mcp_MiniMax_web_search("vietnamese internet slang 2026 words guide june")
# Returns 10 results, all with "2026" in title
```

## Quirk 2: Date Metadata Missing on ~30% Results

**Symptom:** Some search results return `date: ""` (empty) even when the page is recent. This is a backend scraping issue, not a query issue.

**Workaround:**

- Don't rely on date field for recency filtering
- Cross-check by parsing title/snippet for date hints
- For "last 30 days" filtering, use date-keyword queries (Step 3 above)
- Treat missing dates as "unknown recency" — flag for human review

## Quirk 3: Stale Results Mixed in "Last 30 Days" Queries

**Symptom:** Even with date-keyword queries, 1-2 results with "10 months ago" can appear in the top 10.

**Workaround:**

- Always filter results by `date` field in post-processing (Python list comprehension or jq)
- Don't trust "best match" ranking alone for recency
- For critical research, run 2 queries with different date ranges and diff the results

## Quirk 4: Mixed-Language Results Bias

**Symptom:** Vietnamese-specific queries return mostly English results (findniche.com English pages, printify.com, quicksync.pro).

**Workaround:**

- Add Vietnamese keywords explicitly: "sản phẩm", "viral", "tháng 6 2026"
- Look for `.vn` TLD or Vietnamese-language snippets
- For TikTok Shop Vietnam specifically, prefer chartex.com, tokchart.com, or Vietnam-based seller data

## Verification (tested 2026-06-16)

| Query type | Result | Notes |
|------------|--------|-------|
| `site:findniche.com` | ❌ 1027 error | Use keyword fallback |
| `findniche tiktok shop` | ✅ 10 results | Includes findniche.com URLs |
| `findniche tiktok shop vietnam sản phẩm viral` | ✅ 10 results | 2 from findniche, 8 from related |
| Plain query with date keyword | ✅ 10 results | All dated 2026 |
| Date filter via maxAgeHours | ⚠️ Ignored | Backend doesn't honor parameter |

## When to Use This Reference

- Before running multi-source research with `mcp_MiniMax_web_search` or `mcp_exa_*`
- When user asks for "find Vietnamese sources" or "last 30 days" data
- When `site:` operator in query throws `1027-output new_sensitive`
- When date-filtered research returns too many stale results

## Related

- [[mcp-integration]] — Main MCP skill (Troubleshooting section)
- [[self-verify-after-workaround]] — Pattern for verifying workarounds
- `references/exa-mcp-advanced-tools.md` — Exa-specific config
