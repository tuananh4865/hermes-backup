---
title: last30days + Agent-Reach Setup Reference
created: 2026-06-01
updated: 2026-06-01
type: reference
tags: [research, setup, youtube, reddit]
---

# last30days + Agent-Reach Setup Reference

## Quick Start

```bash
# last30days - research topic (Python 3.13 required!)
/opt/homebrew/bin/python3.13 ~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py "TOPIC" --emit=compact --search=reddit,youtube --days=7

# Agent-Reach - check status
python3 -m agent_reach.cli doctor

# Agent-Reach YouTube transcript
yt-dlp --write-sub --skip-download -o "/tmp/%(id)s" "URL"
```

## Python Version Issue

**last30days v3.3.1 requires Python 3.12+. NOT python3.11.**

Homebrew python3.13 location: `/opt/homebrew/bin/python3.13`

Error if wrong version:
```
last30days v3 requires Python 3.12+.
Detected Python 3.11.15.
```

## Verified Working (2026-06-01)

### last30days
| Component | Status | Notes |
|-----------|--------|-------|
| YouTube search | ✅ | 8 videos per query, transcripts 5/6 |
| YouTube transcripts | ✅ | yt-dlp + direct HTTP fallback |
| Reddit keyless | ✅ | RSS tier, 22 posts, score-only |
| Reddit public API | ❌ | 403 forbidden — use keyless tier |
| Hacker News | ✅ | Free, no key |
| Polymarket | ✅ | Free, no key |
| GitHub | ✅ | Free, no key |
| X/Twitter | ⚠️ | Needs XAI_API_KEY or browser cookies |
| TikTok | ⚠️ | Needs SCRAPECREATORS_API_KEY |

### Agent-Reach doctor output (6/16 channels)
```
✅ GitHub 仓库和代码 — 完整可用
✅ YouTube 视频和字幕 — 可提取视频信息和字幕
✅ Reddit 帖子和评论 — rdt-cli 可用（已登录：Conscious-Chance1567）
✅ V2EX 节点、主题与回复 — 公开 API 可用
✅ 任意网页 — 通过 Jina Reader 读取（curl https://r.jina.ai/URL）
[X] Twitter/X 推文 — 需要认证
[X] 小红书 — 需要配置
[X] 微博 — 需要配置
[X] RSS — 需要 feedparser: pip install feedparser
```

## last30days SKILL.md Path

**CRITICAL:** The last30days SKILL.md is at:
```
~/.hermes/skills/last30days/skills/last30days/SKILL.md
```

NOT at the repo root. When the skill runs, it reads SKILL.md from that path and executes the engine at:
```
~/.hermes/skills/last30days/skills/last30days/scripts/last30days.py
```

The cloned repo root (`~/.hermes/skills/last30days/`) contains docs, tests, fixtures — but the actual skill is nested one level deeper.

## Agent-Reach Structure

```
~/.hermes/skills/agent-reach/
├── agent_reach/
│   ├── cli.py          # Main CLI (doctor, install, etc.)
│   ├── channels/       # One file per platform
│   ├── skill/          # OpenClaw/Claude Code skill files
│   └── integrations/   # MCP server
├── config/             # YAML config files
└── docs/               # Guides
```

## YouTube Transcript Fix (1/6 failure rate)

When yt-dlp fails for a video, last30days has a direct HTTP fallback that tries to fetch captions from YouTube's caption API. If that also fails, the video is skipped.

To manually extract:
```bash
# Get best available caption
yt-dlp --write-auto-sub --skip-download -o "/tmp/%(id)s" "VIDEO_URL"

# List available formats
yt-dlp --list-subs "VIDEO_URL"
```

## Environment Setup for Research

```bash
# Python 3.13 (for last30days)
/opt/homebrew/bin/python3.13

# yt-dlp (for YouTube transcripts)
brew install yt-dlp

# Agent-Reach deps (already installed via uv)
uv pip install loguru rich

# Optional: Brave API key (for web search fallback)
# BRAVE_API_KEY=*** in last30days .env
```

## last30days vs Agent-Reach — When to Use Which

| Use Case | Tool |
|----------|------|
| Research topic across multiple platforms | last30days |
| YouTube video transcript | last30days or yt-dlp directly |
| Reddit post + comments | last30days (rdt-cli) |
| X/Twitter without API key | last30days (Digg mode) |
| GitHub repo info | last30days or Agent-Reach (gh) |
| Bilibili video | Agent-Reach (yt-dlp) |
| Web page content | Agent-Reach (Jina Reader: `curl -s https://r.jina.ai/URL`) |
| Specific platform diagnosis | Agent-Reach doctor |

## Common last30days Commands

```bash
# Basic research
last30days "TOPIC" --emit=compact --search=reddit,youtube --days=7

# Deep research (more sources)
last30days "TOPIC" --emit=compact --search=reddit,youtube,twitter,hackernews --days=30 --deep

# Competitor comparison
last30days "OpenClaw vs Hermes" --emit=compact --search=reddit,youtube --competitors=2

# With web backend
last30days "TOPIC" --web-backend=brave --search=web

# Diagnose setup
last30days --diagnose
```