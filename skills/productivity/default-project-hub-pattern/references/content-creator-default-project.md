# Reference: Content Creator Project — Default Project Setup (2026-06-13)

This is the canonical example of the three-tier pattern. Tuấn Anh's Content Creator project at `/Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/` was set as the persistent default on 2026-06-13.

## What was created

### Tier 1: hub.md (in project root)

Path: `/Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/hub.md`

Key sections:
- **Goal**: Xây kênh TikTok ngách phụ kiện quay dựng phim cho người mới bắt đầu (lấy cảm hứng @hi.imdung)
- **3 Trụ Nội Dung**: SETUP + EDIT + GEAR REVIEW
- **Voice**: "anh" + "mấy con vợ" (CỐ ĐỊNH)
- **CTA ratio**: 70% value (0 đồng series) : 30% bán hàng (affiliate)
- **File map**: 14 files + 2 folders (Guidelines, Roadmap, Phân tích, Kịch bản, Trend_Updates, Transcripts)
- **Quy tắc BẮT BUỘC**: 5 hard rules (demo bằng thiết bị thật, series 0 đồng KHÔNG gắn giỏ, etc.)
- **Mục tiêu 90 ngày**: TikTok 10k, GMV 50-100tr/tháng, YouTube 5k
- **Workflow mỗi session mới**: 5-step checklist

### Tier 2: Wiki entity

Path: `/Volumes/Storage-1/Hermes/wiki/entities/content-creator-project.md`

Frontmatter:
```yaml
type: project
tags: [project, content-creator, tiktok]
relationships: [tiktok-content-guideline-hi-imdung-style, tiktok-channel-building-strategy-hi-imdung-style, learned-about-tuananh]
```

Also added:
- Row in `/Volumes/Storage-1/Hermes/wiki/index.md`
- Dated entry in `/Volumes/Storage-1/Hermes/wiki/log.md`

### Tier 3: Memory entry

```
Default project = Content Creator (set 2026-06-13). Path: /Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/. Hub: hub.md. Niche: phụ kiện quay dựng phim cho người mới. 3 trụ: SETUP + EDIT + GEAR REVIEW (lấy cảm hứng @hi.imdung). Voice cố định: "anh" + "mấy con vợ". Tỷ lệ 70% value : 30% bán hàng. Mỗi session mới tự load hub.md + Trend_Updates/ trước.
```

## Memory cleanup needed first

Memory was at 2,800/2,200 chars. Removed 11 stale one-off task entries to make room:
- "Task 'X' — N turns" entries from June 6/10/11 (no lasting value past 7 days)
- Kept durable facts: Telegram workflow, HEVC pattern, voice rules, learning about Tuấn Anh

## What to learn from this example

1. **Voice capture is the highest-value piece.** The single most important thing hub.md captures is the voice ("anh" + "mấy con vợ"). Without it, every future session reverts to default pronouns.

2. **The 70/30 ratio is project-specific policy.** Capturing it in hub.md + memory means the agent enforces it without re-asking.

3. **File map > file dump.** The hub.md structure is "Guidelines / Roadmap / Phân tích / Kịch bản / Trend_Updates / Transcripts" — a category structure, not a flat list. Future agents navigate by category.

4. **Three-tier is non-negotiable.** Without all three tiers, the next session can't find the project. Test: open a new session, mention the project by name — agent should load hub.md without being told the path.

## Failure modes to watch for

- **Voice drift**: a future session might say "anh chị em" or "các bạn" instead of "mấy con vợ" — voice rules in memory + hub.md are the fix, but worth a periodic check
- **Hub.md goes stale**: when new files are added (e.g. a new kịch bản file), update hub.md's file index + append a Log entry
- **Memory cap hits again**: keep the default-project entry concise (~500 chars max) so it doesn't crowd out other durable facts
