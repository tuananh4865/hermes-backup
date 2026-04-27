---
title: last30days
created: 2026-04-11
updated: 2026-04-11
type: concept
tags: [research, social-search, reddit, hacker-news, polymarket]
confidence: high
---

# last30days

Multi-source social search skill — researches topics across Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, and the web.

## Quick Reference

- **Skill**: `skills/last30days-skill/SKILL.md`
- **Script**: `~/.claude/skills/last30days-3/scripts/last30days.py`
- **Config**: `~/.config/last30days/.env`
- **Setup**: `SETUP_COMPLETE=true` in config

## Sources

| Source | Status | Auth |
|--------|--------|------|
| Reddit | Always on | None |
| Hacker News | Always on | None |
| Polymarket | Always on | None |
| GitHub | Auto (if `gh` CLI) | None |
| X/Twitter | Optional | Browser cookies or xAI API |
| YouTube | Optional | yt-dlp |
| TikTok | Optional | ScrapeCreators API |
| Instagram | Optional | ScrapeCreators API |

## Usage

```bash
python3 scripts/last30days.py "topic" --emit=compact --save-dir=~/Documents/Last30Days
```

## Related

- [[deep-research]] — Deep research workflow
- [[search-fallback-chain-ddg-tavily]] — Web search fallback chain
