---
title: Social Media Research — Platform-Native with last30days + Agent-Reach
name: social-media-research
version: "1.0.0"
description: Research topics across YouTube, X/Twitter, Reddit, TikTok, and other social platforms using last30days + Agent-Reach. Platform-native data, not web-search articles about platforms.
argument-hint: YouTube trends this week | OpenClaw vs Hermes comparison | Reddit AI tools discussion | trending TikTok sounds this month
trigger: research YouTube | research X/Twitter | research Reddit | research social media | trending content | platform-native research
allowed-tools: Bash, Read, Write, AskUserQuestion, WebSearch
user-invocable: true
metadata:
  requires:
    bins:
      - python3.13
      - yt-dlp
    env: []
    optionalEnv:
      - XAI_API_KEY
      - BRAVE_API_KEY
      - SCRAPECREATORS_API_KEY
      - RDT_TOKEN
---

# Social Media Research — Platform-Native

## Core Principle

**Use platform-native tools BEFORE web search.**

When Anh asks to "research YouTube" or "search X" or "find Reddit discussions":
→ Use `last30days` + `Agent-Reach` first
→ Web search is ONLY the fallback

**Why:** Web search finds ARTICLES ABOUT platforms — not platform data. The difference is critical for content decisions.

---

## Setup (CRITICAL — Python 3.13 Required)

### last30days
```bash
# Location
~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py

# IMPORTANT: Requires Python 3.12+, NOT python3.11
# Use: /opt/homebrew/bin/python3.13

# Test:
/opt/homebrew/bin/python3.13 ~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py --help

# YouTube transcripts (yt-dlp):
brew install yt-dlp
```

### Agent-Reach (supplementary, for specific platforms)
```bash
# Status check
cd ~/.hermes/skills/agent-reach && python3 -m agent_reach.cli doctor

# YouTube/Bilibili subtitle:
yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "URL"
```

---

## Usage Patterns

### Basic research (last30days)
```bash
/opt/homebrew/bin/python3.13 ~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py "TOPIC" --emit=compact --search=reddit,youtube --days=7
```

### With web backend override
```bash
/opt/homebrew/bin/python3.13 ~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py "TOPIC" --search=reddit,youtube,twitter --days=30 --web-backend=brave
```

### Agent-Reach YouTube transcript
```bash
yt-dlp --write-auto-sub --skip-download -o "/tmp/%(id)s" "VIDEO_URL"
# Then read the .vtt or .json file
```

### Agent-Reach Reddit
```bash
rdt search "TOPIC" --limit=10
rdt read POST_ID
```

---

## Platforms & Tools Matrix

| Platform | Primary Tool | Secondary Tool |
|----------|-------------|----------------|
| YouTube | last30days (transcripts) | Agent-Reach (yt-dlp) |
| Reddit | last30days (via rdt-cli) | Agent-Reach (rdt) |
| X/Twitter | last30days (needs XAI_API_KEY) | - |
| TikTok | last30days (needs SCRAPECREATORS_API_KEY) | - |
| Bilibili | Agent-Reach (yt-dlp) | - |
| Hacker News | last30days (free, no key) | - |
| Polymarket | last30days (free, no key) | - |
| GitHub | last30days (free, no key) | Agent-Reach (gh cli) |

---

## Output Format for Anh

When delivering research, use Vietnamese with:
- Key findings as bold lead-ins
- Engagement numbers (views, upvotes, likes)
- Platform-specific insights
- Actionable for TikTok affiliate content

No trailing `Sources:` block — emoji-tree footer from last30days is the citation.

---

## Common Traps

1. **Python version** — last30days v3.3.1 requires 3.12+. Using python3.11 gets "requires Python 3.12+" error. Always use `/opt/homebrew/bin/python3.13`.

2. **Reddit 403** — Public Reddit search API returns 403. last30days falls back to RSS tier (22 posts, score-only). Works fine for research.

3. **YouTube transcript failure** — yt-dlp fails for ~1/6 videos. last30days has direct HTTP fallback. 5/6 success rate is normal.

4. **No X/Twitter auth** — Without XAI_API_KEY, last30days uses Digg (1000 AI accounts, no auth required). Good enough for most research.

---

## Related Skills

- `tiktok-viral-script` — Content creation (uses research output)
- `hermes-autoresearch` — Nightly skill improvement (uses last30days for AI agent landscape research)
- `youtube-content` — YouTube transcript extraction and content repurposing

---

## Reference

Full setup notes: `references/last30days-agent-reach-setup.md`