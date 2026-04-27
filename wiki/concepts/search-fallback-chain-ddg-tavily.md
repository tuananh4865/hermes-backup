---
title: Search Fallback Chain — ddgs, duckduckgo_search, Searx, Brave, Tavily
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [automation, search, research, api]
sources: [raw/transcripts/2026-04-11/2026-04-11-thy-cron-wiki.md]
confidence: high
---

# Search Fallback Chain — ddgs, duckduckgo_search, Searx, Brave, Tavily

## Executive Summary

Both `deep_research.py` and `autonomous_app_builder.py` failed because they relied solely on Tavily API, which hit usage limits (HTTP 432). A multi-source fallback chain was implemented: ddgs (python3.14) → duckduckgo_search (python3.9) → Searx → Brave Search → Tavily.

## The Problem

```
Status: 432
{"detail": {"error": "This request exceeds your plan's set usage limit."}}
```

Tavily API key `tvly-dev-j...e2qV0c` exceeded usage quota. Scripts using Tavily as the only search source returned empty results, causing research to fail silently.

## The Solution — Fallback Chain

```python
# Source 1: ddgs with python3.14 (SSL fix for Python 3.9 TLS issues)
python14_bins = ["python3.14", "python3.13"]
for pybin in python14_bins:
    result = subprocess.run([
        pybin, "-c",
        f"from ddgs import DDGS; ..."
    ])

# Source 2: duckduckgo_search (older package, Python 3.9)
from duckduckgo_search import DDGS as _DDGS

# Source 3: Searx (privacy-friendly metasearch, public instances)
https://searxng.site/search?q=...

# Source 4: Brave Search (requires API key)
# Source 5: Tavily (last resort when key available)
```

## Why Multiple Python Versions?

ddgs uses TLS 1.3 which fails on Python 3.9 (compiled with LibreSSL 2.8.3):
```
ValueError: Unsupported protocol version 0x304
```

Solution: Run ddgs via python3.14 which has compatible SSL.

## Search Source Comparison

| Source | Free | API Key | Reliability | Speed |
|--------|------|---------|-------------|-------|
| ddgs (python3.14) | ✅ | No | High | Fast |
| duckduckgo_search | ✅ | No | Medium | Fast |
| Searx | ✅ | No | Medium | Slow |
| Brave Search | ❌ | Yes | High | Fast |
| Tavily | ❌ | Yes | High | Fast |

## last30days Integration

Round 8 added to deep research for social trends:
- Uses `last30days` skill for Reddit, HN, X/Twitter
- Runs via: `python3 scripts/last30days.py "query" --emit=compact`
- Alternative: use `python3.14` for better compatibility

## Bypass Strategies for Blocked Search

Research found these approaches for sites that block bots:

1. **Rotate User-Agent** — ddgs doesn't accept headers param in constructor
2. **Searx** — Privacy-friendly, doesn't block bots aggressively
3. **Multi-source fallback** — When one fails, try next automatically
4. **Residential proxy** — Paid, high effort

## Implementation Status

- `deep_research.py` — ✅ Updated with fallback chain
- `autonomous_app_builder.py` — ✅ Updated (DuckDuckGo primary, Tavily fallback)

## Related

- [[deep-research]] — Research workflow
- [[last30days]] — Social trends skill
