# Worker Output Path Gap — CRITICAL (2026-05-08)

> **Discovered:** 2026-05-08 during autoresearch nightly run.
> **Severity:** CRITICAL — pipeline broken at aggregation step.

## The Problem

Workers (content-creator, research-agent) cron jobs ARE firing and producing output.
BUT the shared `outputs/` directories remain EMPTY.

```
~/.hermes/cron/output/ce3701b4dcdd/2026-05-07_08-05-07.md  (11KB) ← cron output EXISTS ✅
~/.hermes/workers/content-creator/outputs/                    ← EMPTY ❌

~/.hermes/cron/output/1c425ba42980/2026-05-07_18-50-31.md  (4KB) ← cron output EXISTS ✅
~/.hermes/workers/research-agent/outputs/                     ← EMPTY ❌
```

## Root Cause

Workers deliver response via cron → output goes to `~/.hermes/cron/output/{job_id}/YYYY-MM-DD_HH-MM-SS.md`
Workers do NOT write to shared `~/hermes/workers/{worker}/outputs/` directories

## Impact

- Orchestrator Monitor runs every 2h but finds nothing in shared outputs/ → can't aggregate
- Orchestrator Nightly consolidation finds empty outputs/ → reports [SILENT] even when workers fired
- Full content pipeline broken at aggregation step

## Verification Commands

```bash
# Check if cron job fired (should have recent files)
ls -la ~/.hermes/cron/output/{job_id}/

# Check shared worker outputs (SHOULD have files but currently EMPTY)
ls -la ~/.hermes/workers/content-creator/outputs/
ls -la ~/.hermes/workers/research-agent/outputs/

# Both needed:
# - cron output dir has files = cron fired ✅
# - shared outputs/ has files = worker wrote to shared dir ✅
```

## Fix Required

Worker SOUL.md must include explicit output requirement:

```markdown
## OUTPUT REQUIREMENT
After completing your task:
1. Write full output to ~/hermes/workers/{worker}/outputs/[YYYY-MM-DD]-[type].md
2. Also produce your response normally (for cron delivery)
Both are required — cron delivery AND shared file for orchestrator aggregation.
```

This is a SOUL.md / worker prompt change, NOT a cron change.

## Files to Update

1. `~/.hermes/workers/content-creator/SOUL.md` — add OUTPUT REQUIREMENT section
2. `~/.hermes/workers/research-agent/SOUL.md` — add OUTPUT REQUIREMENT section

After update, re-apply cron prompts:
```python
import subprocess, sys
for worker in ['content-creator', 'research-agent']:
    with open(f'/Users/tuananh4865/.hermes/workers/{worker}/SOUL.md', 'r') as f:
        prompt = f.read()
    # Get job_id for this worker and run cron edit
```

## Related

- `ai-agent-business` skill — has `references/worker-cron-2026-05-08.md` with same finding
- PITFALL 18 in hermes-autoresearch SKILL.md
