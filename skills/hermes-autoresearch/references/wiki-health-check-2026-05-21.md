# Wiki Health Check — 2026-05-21

**Source:** `/Volumes/Storage-1/Hermes/wiki` — 7,039 files  
**Health command:** `python3 scripts/wiki_semantic_health.py` (ran at 4AM)

## Issues Found

| Issue | Count | Severity |
|-------|-------|----------|
| Missing frontmatter | 0 | ✅ None |
| Stale pages (>30 days) | 0 | ✅ None |
| Broken wikilinks | 12 | ⚠️ Low |
| Orphan pages | 202 | ⚠️ Medium |
| **Duplicate titles** | **1,436** | 🔴 CRITICAL |
| Self-referential links | 20 | ⚠️ Low |
| Date inconsistencies | 0 | ✅ None |

**Total: 1,670 issues**

## Top Duplicate Title Examples

```
hermes dojo — 4 copies:
  projects/hermes-dojo/README.md
  projects/hermes-dojo/hub.md
  concepts/hermesdojo.md
  concepts/Hermes Dojo.md

nexus — 2 copies:
  projects/nexus/index.md
  projects/nexus/hub.md

wiki quality campaign — 4 copies:
  projects/wiki-quality-campaign/hub.md
  concepts/Wiki Quality Campaign.md
  concepts/wiki-quality-campaign.md
  concepts/wikiqualitycampaign.md

tiktok content strategy — 2 copies:
  projects/tiktok-content-strategy/hub.md
  concepts/tiktok-content-strategy.md

surgical change protocol — 2 copies:
  projects/hermes-dojo/skills/behavior/surgical-change-protocol/SKILL.md
  concepts/surgical-change-protocol.md

memory manage — 2 copies:
  projects/hermes-dojo/skills/memory/memory-manage/SKILL.md
  concepts/memory-manage.md
```

## Top Broken Wikilink Examples

```
projects/nexus/SPEC.md → [[...]]
concepts/Tun Tip Hon - 2026-04-18.md → [[entities/*]]
concepts/wikilink.md → [[./Sibling Document]] (path-separator links)
concepts/double-bracket-links.md → [[Note Title#Heading]]
```

## Orphan Pages (Top Examples)

```
WIKI_IMPROVEMENT_PLAN.md
learn/series-affiliate-thanh-tap-hoa/README.md
learn/tiktok-duy-muoi/README.md
references/x-research-hermes-2026-05-20.md
references/autoresearch-may-21-2026.md
```

## Cron Jobs Status (2026-05-21)

**Active (5):**
- a4b8e528983f — Autoresearch Nightly (2AM)
- a5c02f2f0d87 — Hermes X Research (7AM)
- 7cba6ba5f52a — Daily Backup (3AM)
- Wiki Health Daily (4AM)
- 5aea298eb0a8 — Daily Session Review (0AM)

**Paused (8):**
- Content Creator Morning + Evening
- Research Analyst Morning + Evening
- Orchestrator Morning + Nightly + Monitor
- ByteRover Health Check

**Error (2):**
- ByteRover Knowledge Sync Daily
- ByteRover Health Check Daily

## Recommended Actions

1. **1,436 duplicate titles** — Priority: HIGH
   - Category folders over individual files
   - Same content → merge, keep newest
   - Different content → rename + frontmatter note

2. **202 orphan pages** — Priority: MEDIUM
   - Many are Telegram transcript dumps with no inbound links
   - Low impact but clutters retrieval

3. **8 paused cron jobs** — Priority: MEDIUM
   - Workers (Content Creator, Research) more important than Orchestrator
   - Resume workers FIRST

4. **ByteRover errors** — Priority: LOW
   - Jobs already paused
   - Can investigate later
