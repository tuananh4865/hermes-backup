# Worker Stall Recovery — Detection & Response Playbook

> **When**: Worker cron jobs stop producing output. Detected by orchestrator during morning/evening check.
> **Status**: Detection ✅ working (May 14 confirmed) | Autonomous recovery ❌ not yet built

---

## Detection Commands

```bash
# Worker freshness check — run at start of every orchestrator session
WORKER="content-creator"
OUTPUT_DIR="/Users/tuananh4865/.hermes/workers/content-creator/outputs"

LAST_FILE=$(ls -t "$OUTPUT_DIR"/*.md 2>/dev/null | head -1)
if [ -z "$LAST_FILE" ]; then
    echo "⚠️ NO OUTPUT FILES — worker may never have run"
else
    LAST_DATE=$(date -r "$LAST_FILE" "+%Y-%m-%d" 2>/dev/null)
    TODAY=$(date "+%Y-%m-%d")
    FILE_AGE_DAYS=$(( ($(date +%s) - $(date -r "$LAST_FILE" +%s 2>/dev/null)) / 86400 ))
    
    echo "Worker: $WORKER"
    echo "Last output: $LAST_DATE (${FILE_AGE_DAYS}d ago)"
    
    if [ "$FILE_AGE_DAYS" -ge 1 ]; then
        echo "🚨 STALL DETECTED — $FILE_AGE_DAYS day(s) since last output"
    fi
fi
```

---

## Full Worker Health Check (all workers)

```bash
#!/bin/bash
# worker-health-check.sh — run at start of orchestrator morning/evening session

echo "=== WORKER HEALTH CHECK ==="
echo "Time: $(date '+%Y-%m-%d %H:%M:%S')"
echo ""

WORKERS=("content-creator" "research-agent")
BASE="/Users/tuananh4865/.hermes/workers"

for WORKER in "${WORKERS[@]}"; do
    OUTPUT_DIR="$BASE/$WORKER/outputs"
    echo "--- $WORKER ---"
    
    if [ ! -d "$OUTPUT_DIR" ]; then
        echo "❌ Output dir missing: $OUTPUT_DIR"
        continue
    fi
    
    LAST_FILE=$(ls -t "$OUTPUT_DIR"/*.md 2>/dev/null | head -1)
    
    if [ -z "$LAST_FILE" ]; then
        echo "⚠️ No output files ever"
    else
        LAST_DATE=$(date -r "$LAST_FILE" "+%Y-%m-%d %H:%M" 2>/dev/null)
        FILE_AGE=$(echo $(($(date +%s) - $(date -r "$LAST_FILE" +%s))) / 3600 | bc) 2>/dev/null || FILE_AGE=0
        echo "Last: $LAST_DATE (${FILE_AGE}h ago)"
        
        if [ "$FILE_AGE" -gt 36 ]; then
            echo "🚨 STALLED (${FILE_AGE}h)"
        elif [ "$FILE_AGE" -gt 12 ]; then
            echo "⚠️ LATE (>12h)"
        else
            echo "✅ OK"
        fi
    fi
    echo ""
done
```

---

## Orchestrator Response Protocol

### When stall detected (worker > 24h silent):

1. **Document the stall** — append to HEARTBEAT.md:
```bash
echo "- [⚠️] $(date '+%Y-%m-%d %H:%M') — $WORKER STALLED: no output since $LAST_DATE" >> /Users/tuananh4865/.hermes/workers/orchestrator/HEARTBEAT.md
```

2. **Produce fallback brief directly** — orchestrator does the work:
   - Run own research (web search)
   - Write content/analysis directly
   - Save to orchestrator's own output location
   - Flag in report: "Worker stalled — fallback production"

3. **Report to Anh** — NEVER silently suppress stall:
   - Include "Cần xử lý: [worker name]" in 3-bullet report
   - Do NOT send [SILENT] when workers are stalled

---

## Why Autonomous Restart Is Not Yet Available

Workers run via cron triggers → cron jobs invoke worker prompts → workers write output.

```
Cron fires
  → hermes-agent --prompt worker-prompt
  → Worker writes to outputs/
  → Worker exits
```

**Restart mechanism gap**: There's no listener process waiting for a "restart signal." The worker process exits after each run. A restart would need:
- A process that stays alive between runs (daemon), OR
- Cron job that can be re-triggered by orchestrator, OR  
- A file-based signal that next cron invocation reads and acts on

**Known workaround**: Human manually restarts worker via Hermes CLI.

---

## Files to Check

| Path | Purpose |
|------|---------|
| `/Users/tuananh4865/.hermes/workers/content-creator/outputs/` | Content creator output |
| `/Users/tuananh4865/.hermes/workers/research-agent/outputs/` | Research agent output |
| `/Users/tuananh4865/.hermes/cron/output/*/` | Cron job outputs (primary) |
| `/Users/tuananh4865/.hermes/workers/orchestrator/HEARTBEAT.md` | Stall log |
| `/Users/tuananh4865/.hermes/workers/memory/PENDING_TASKS.md` | Known blockers |

---

## Recovery Attempt Script (NOT YET BUILT)

```bash
#!/bin/bash
# attempt-worker-recovery.sh — placeholder for autonomous recovery
# Status: NOT IMPLEMENTED

WORKER="$1"
CRON_ID="$2"  # e.g., ce3701b4dcdd for content morning

echo "Attempting to restart $WORKER (cron: $CRON_ID)..."

# What we'd do if we had restart authority:
# 1. Kill any stuck hermes-agent processes for this worker
# 2. Touch a "restart signal" file
# 3. Next cron firing would read signal and reset state

echo "❌ Autonomous restart not yet implemented"
echo "➡️  Manual intervention required"
echo "➡️  Report 'Cần xử lý: $WORKER' to Anh"
```

---

**Last verified**: 2026-05-14
