# Two-Cron Architecture (2026-05-14)

> **Status**: CONFIRMED — May 14 midnight run confirmed the two-cron pattern
> **Lesson**: Orchestrator cron = monitoring, Daily Review = content production. Separate mandates.

## The Two Cron Jobs

| Cron | Job ID | Schedule | Mandate |
|------|--------|----------|---------|
| Orchestrator Monitor | `f1584a9a1d86` | 0 */2 * * * (every 2h) | Monitor worker health, status report |
| Daily Review | `5aea298eb0a8` | 0 0 * * * (daily midnight) | Fresh research + session review |

## May 14 Midnight Run — What Happened

**Both fired within 1 minute of each other (00:02 and 00:02:56)**

### Orchestrator Cron (00:02:10)
- Checked worker health: content-creator stalled (May 13 evening), research-agent stalled (May 12)
- Compiled status report (workers down, no direct content)
- Sent `[SILENT]` ✅ CORRECT — monitoring mandate only, no content to deliver

### Daily Review Cron (00:02:56)
- Did fresh research: Summer Cooling window, Neck Fan 64% margin, Gen Z slang update
- Produced actual content brief
- Delivered to Anh ✅ CORRECT — content production mandate

## Key Distinction

```
Orchestrator Cron = "Are workers healthy?" → [SILENT] if all clear
Daily Review Cron = "What new intelligence do we have?" → Always deliver
```

**Misconception**: "Workers stalled, orchestrator should produce content"
**Reality**: Orchestrator monitors; Daily Review produces. When workers are down, Daily Review fills the gap.

## What Each Cron Does

### Orchestrator Cron — Monitoring
- Check worker file timestamps
- Detect stalls (no output > 24h)
- Compile 3-bullet status: "Hoàn thành | Đang làm | Cần quyết định"
- [SILENT] if no worker issues AND no direct production
- Does NOT do fresh research

### Daily Review Cron — Production
- Review yesterday's session logs
- Fresh research on trends (TikTok Shop, Gen Z slang, product opportunities)
- Compile content brief with new intelligence
- ALWAYS deliver when research is done

## Source Files

| File | What it contains |
|------|-----------------|
| `cron/output/f1584a9a1d86/2026-05-14_00-02-10.md` | Orchestrator monitor output (SILENT) |
| `cron/output/5aea298eb0a8/2026-05-14_00-02-56.md` | Daily Review content brief |

## Rule for Future Sessions

When workers are stalled and you're deciding whether to send [SILENT]:

1. **Are you the orchestrator cron?** → Monitoring mandate. [SILENT] if no content to report.
2. **Are you the daily review cron?** → Production mandate. Deliver your research.
3. **Never confuse the mandates** — orchestrator doesn't produce content, it monitors workers.

## Related
- `references/worker-stall-recovery.md` — Worker stall detection and response
- `references/orchestrator-briefing.md` — Orchestrator decision logic
