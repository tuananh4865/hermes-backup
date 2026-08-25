# X Research Methodology — Hermes Autoresearch

> Critical lesson learned 2026-05-05: Direct Twitter/X posts are NOT accessible via normal web search.
> Individual user tweets, real-time discussions, and organic conversations do NOT appear in
> search engine results. The X Research job must use indirect sources.

## The Problem

Standard web search queries like `site:x.com "Hermes Agent"` return:
- Official accounts (@NousResearch, @teknium1)
- GitHub repository pages (which mirror README to X)
- News aggregator summaries (36kr, AIbase, etc.)
- Blog posts about X mentions
- YouTube video descriptions

**What they DON'T return:**
- Individual developer tweets
- Real-time discussions
- Organic user conversations
- Questions and answers in X threads

## Why This Happens

X/Twitter content is largely behind authentication walls and is not well-indexed by search engines.
Even with `site:x.com` filters, search engines crawl and index the platform's public-facing
pages and SEO-optimized profiles, not the firehose of individual tweets.

## Verified Approach for X Research

### Primary Strategy: Multi-Channel Indirect Collection

Instead of searching X directly, gather X-originated content from:

| Source Type | What You'll Find | Search Query Examples |
|-------------|-----------------|---------------------|
| News aggregators | Articles citing X posts | `"Hermes Agent" "twitter.com" 2026` |
| Chinese tech press | Translated/reported X discussions | `site:36kr.com Hermes Agent` |
| Blog summaries | People summarizing X conversations | `Hermes Agent X discussion 2026` |
| GitHub activity | Stars, forks, PRs (often announced on X) | `site:github.com NousResearch hermes-agent` |
| YouTube | Videos discussing X buzz | `Hermes Agent review 2026 site:youtube.com` |
| Reddit | Users discussing what they saw on X | `site:reddit.com Hermes Agent` |
| DEV.to | Developer posts often reference X threads | `site:dev.to Hermes Agent` |

### Secondary Strategy: GitHub as X Proxy

GitHub activity (stars, forks, issues, releases) is publicly announced on X by developers.
Track GitHub to reconstruct the X conversation:

```
# GitHub stars timeline (star-history.com)
https://www.star-history.com/nousresearch/hermes-agent

# Release announcements (usually preceded by X posts)
https://github.com/NousResearch/hermes-agent/releases

# Issue activity (developers discussing in issues)
https://github.com/NousResearch/hermes-agent/issues
```

### Third-Party Trackers

| Source | URL | Data Available |
|--------|-----|----------------|
| Hermes Atlas | hermesatlas.com | Ecosystem repos, growth metrics, community projects |
| OpenRouter stats | openrouter.ai/apps/hermes-agent | Usage stats, top models, token volume |
| Star-history | star-history.com | Star growth timeline |

## Recommended Search Queries (X Research)

```bash
# Core: Hermes Agent mentions
"Hermes Agent" NousResearch
"hermes-agent" github stars 2026
"Hermes Agent" review 2026

# Ecosystem: what people building
"hermes-agent" fork
site:github.com herm3x/hermes-agent
site:github.com OnlyTerp/hermes-optimization-guide

# News: X reactions
site:36kr.com Hermes Agent
site:dev.to Hermes Agent
site:reddit.com/r/LocalLLM Hermes Agent

# Growth tracking
"Hermes Agent" "github stars"
"Hermes Agent" "fastest growing"
```

## X Research Output Template

When synthesizing X research, structure as:

```
# Hermes Agent X Research — YYYY-MM-DD

## Overview
- Total sources found: N
- Date range: last 7 days
- Sentiment: positive/neutral/negative
- Key narrative: [what the community is talking about]

## Top Themes (by frequency)
1. [Theme] — N mentions
2. [Theme] — N mentions

## Use Cases People Describe
1. [Use case] — [context from sources]

## Techniques / Tips Found
1. [Technique] — [brief description]

## Frustrations / Issues Reported
- [Issue 1]
- [Issue 2]

## Comparisons Mentioned
- [vs Tool] — [what people say]

## Action Items
- [What to investigate]
- [What to fix based on complaints]
- [New features to consider]

## Raw Data
[List with sources — news articles, blog posts, GitHub activity]
```

## Important Notes

1. **50+ results target**: With indirect collection, 50+ sources is achievable via news aggregators,
   blog posts, GitHub activity, and third-party trackers. Direct X posts are not the target.

2. ** tuananh4865 / TyayUno accounts**: Neither account shows Hermes-specific X activity.
   tuananh4865 appears on GitHub (65 repos) but no Hermes posts detected.

3. **Crypto/VC concerns**: Some community concern about Nous Research's $70M crypto-adjacent
   fundraising (Paradigm + a16z). Core product remains MIT-licensed.

4. **OpenClaw migration**: Major theme — OpenClaw's March 2026 CVE crisis drove significant
   Hermes adoption as secure alternative.

## Related

- Skill: `hermes-autoresearch` — main autoresearch loop
- References: `self-improving-agents-2026.md` — broader AI agent research context
