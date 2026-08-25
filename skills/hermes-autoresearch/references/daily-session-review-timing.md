# Daily Session Review — Timing & Data Mapping

**Created:** 2026-06-07
**Purpose:** Clarify cron timing vs data date for future agents

## Cron Schedule

| Job | Schedule | Actual Fire | Data Coverage |
|-----|----------|-------------|---------------|
| Daily Session Review | `0 0 * * *` (midnight) | ~00:07 (+7min delay) | **PREVIOUS day** (H-1) |

**Key insight:** June 7 00:07 cron reviews June 6 data. NOT June 7.

## Session Path Conventions

**Session files by date:**
```
~/.hermes/sessions/
├── session_cron_*20260606*.json   ← Cron sessions from June 6
├── session_cron_*20260607*.json   ← Cron sessions from June 7 (none yet at 00:07)
├── request_dump_*20260606*.json   ← Failed requests from June 6
└── sessions.json                  ← Session manifest (updated_at shows recency)
```

**Manifest session ordering:**
```python
# sessions.json sessions sorted by updated_at:
sessions.sort(key=lambda x: x.get('updated_at',''))
# Most recent last = current state
```

## Data Extraction Flow

```
00:07 cron fires → reads sessions from ~/.hermes/sessions/
                 → filter by date (H-1 = June 6 when running on June 7)
                 → extract decisions, revenue, learnings, blockers
                 → update wiki/log.md
                 → generate daily_review_YYYY-MM-DD.md
                 → update entities/learned-about-tuananh.md if new prefs
```

## Session Database

**Path:** `~/.hermes/state.db` (NOT `~/Library/Application Support/hermes-agent/sessions/`)

**Verified (2026-06-01):** sessions.db has 545 sessions (325 cron, 190 telegram, 30 cli)

## Report Output Location

```
~/.hermes/cron/output/daily_review_YYYY-MM-DD.md
```

**Naming:** Report for June 6 data = `daily_review_2026-06-06.md` (generated June 7 00:07)

## Failure Pattern

When a DM request fails (non_retryable_client_error), the request dump is at:
```
~/.hermes/sessions/request_dump_{session_id}_{timestamp}.json
```

Example: `request_dump_20260606_142557_c7a13bb5_20260606_235512_810928.json`
- Session: 20260606_142557_c7a13bb5
- Timestamp: 2026-06-06 23:55:12
- Content: TikTok content research request (failed)

## Related

- `references/daily-session-review.md` — Original methodology
- `references/daily-review-2026-05-10.md` — May findings