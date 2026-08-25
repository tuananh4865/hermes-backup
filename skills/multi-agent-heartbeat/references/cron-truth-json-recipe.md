# Cron Truth — Direct JSON Recipe

> **The 1-call alternative to `hermes cron list`.** When the heartbeat needs only the cron ground-truth columns (name + last_run + status + schedule) and NOT the full job prompts (which can be 30KB+ per cron), parse `~/.hermes/cron/jobs.json` directly with python3. ~500ms vs `hermes cron list` + pagination (2-3 calls × 5-15KB output each).

## When to use this recipe vs `hermes cron list`

| Use case | Recipe | Reason |
|---|---|---|
| Sweep cron health (need just last_run + status for 18 jobs) | **Direct JSON** (this recipe) | 1 call, ~1KB output, no pagination |
| Investigate a specific cron's prompt/payload | `hermes cron list \| grep -A 30 "<name>"` | Need full prompt context |
| Modify a cron (`update`, `pause`, `resume`) | `hermes cron update ...` | CLI command required |
| Debug a cron delivery error | `hermes cron list` + look at `last_delivery_error` | JSON doesn't include this field by default |

**Rule of thumb:** if you're going to write a 5-7 row cron truth table to your sweep response, use the JSON recipe. If you need to investigate or modify, use the CLI.

## Recipe

```bash
python3 -c "
import json
with open('/Users/tuananh4865/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for job in data.get('jobs', []):
    last = job.get('last_run_at') or 'NEVER'
    status = job.get('last_status') or 'pending'
    err = job.get('last_error') or ''
    sched = job.get('schedule_display', '?')
    name = job.get('name', '?')[:42]
    print(f'{name:44} | last={last[:19] if last != \"NEVER\" else \"NEVER\":19} | {status:6} | err={err[:30] if err else \"\":30} | sched={sched}')
print(f'TOTAL: {len(data.get(\"jobs\", []))} jobs')
"
```

**Output format (fixed-width columns):**

```
Hermes Daily Backup                        | last=2026-06-28T03:04:08 | ok     | err=                               | sched=0 3 * * *
Hermes Autoresearch Nightly                | last=2026-06-28T07:09:03 | ok     | err=                               | sched=0 7 * * *
...
TOTAL: 18 jobs
```

This is the exact format that fits a 6-row status table in the sweep response. ~1KB total output vs `hermes cron list` which dumps 30KB+ of full job prompts.

## ⚠️ PITFALL: Don't guess field names — inspect schema first (V18 lesson, 2026-06-29 18:01)

**Symptom:** A sweep ran the JSON recipe but every cron showed `last=never`. With status still `ok` and enabled `True`, the agent's first instinct could be to escalate "all crons never run" — a false CRITICAL.

**Root cause:** First-cut python recipe used `last_run` (does NOT exist) and `lastStatus` / `lastRun` / `last_execution` (none exist either). The agent pattern-matched field names from intuition instead of inspecting the actual schema. Result: `.get()` returned `None` for all of them → "NEVER" output → phantom CRITICAL.

**Correct field names (verified from `~/.hermes/cron/jobs.json` schema, 2026-06-29 18:01):**

| Field | Type | Example | Notes |
|---|---|---|---|
| `id` | str | `"ace89e9ea119..."` | Cron UUID |
| `name` | str | `"QA Agent Quality Gate"` | |
| `prompt` | str | full prompt | OMIT from sweep output (huge) |
| `skill` / `skills` | list/str | `[]` | |
| `model`, `provider`, `base_url` | str | model config | |
| `script` | str/null | | |
| `schedule` | dict | `{"kind": "cron", "expr": "0 */6 * * *", "display": "0 */6 * * *"}` | Use `schedule_display` for human-readable |
| `repeat` | bool | `True` | |
| `enabled` | bool | `True` | |
| `state` | str | `"idle"` / `"running"` | |
| `paused_at`, `paused_reason` | str/null | | |
| `created_at` | ISO datetime | | |
| `next_run_at` | ISO datetime | | |
| **`last_run_at`** | ISO datetime | `"2026-06-29T12:00:18+07:00"` | **NOTE the `_at` suffix — not `last_run`!** |
| **`last_status`** | str | `"ok"` / `"error"` | |
| **`last_error`** | str/null | `""` | |
| **`last_delivery_error`** | str/null | `""` | Available here, not just CLI |
| `deliver` | dict | delivery config | |
| `origin` | str | `"loop-engineering"` etc. | |
| `fire_claim` | str/null | | |

**Schema inspection recipe (run this FIRST if uncertain — 1 call, ~500B output):**

```bash
python3 -c "
import json
with open('/Users/tuananh4865/.hermes/cron/jobs.json') as f:
    data = json.load(f)
print('SCHEMA:', list(data['jobs'][0].keys()))
print('SAMPLE:', json.dumps(data['jobs'][0], indent=2)[:500])
print('COUNT:', len(data['jobs']))
"
```

**Verified working recipe (V18 — used 2026-06-29 18:01 sweep, 18/18 crons correctly read):**

```bash
python3 -c "
import json
from datetime import datetime, timezone
with open('/Users/tuananh4865/.hermes/cron/jobs.json') as f:
    data = json.load(f)
now = datetime.now(timezone.utc)
for j in data['jobs']:
    name = j.get('name', '?')[:42]
    last_run = j.get('last_run_at')          # NOT last_run
    status = j.get('last_status', '?')        # NOT lastStatus
    err = j.get('last_error') or ''           # NOT lastError
    if last_run:
        lr = datetime.fromisoformat(last_run.replace('Z', '+00:00'))
        age_h = (now - lr).total_seconds() / 3600
        age_str = f'{age_h:.1f}h ago'
    else:
        age_str = 'NEVER'
    print(f'{name:44} | {age_str:12} | {status} | sched={j.get(\"schedule_display\", \"?\")}')
print(f'TOTAL: {len(data[\"jobs\"])} jobs')
"
```

**Quick validation (run after the sweep recipe):**

- `last_run_at` returns ISO datetimes for all enabled crons → expect 18 age values, not 18 "NEVER"
- If ANY cron shows `NEVER` despite being enabled with `last_status=ok` → schema mismatch, re-inspect
- `age_str` values should be in the range `0.5h-39h` (depending on cadence) — if all show "0.0h ago" you got the wrong field
- TOTAL count should match `hermes cron list` count (currently 18)

## Why the `which hermes` discovery matters

The `hermes-agent` skill's CLI Reference section mentions `hermes cron list` as the command. Running `which hermes` reveals:
- `/Users/tuananh4865/.local/bin/hermes` (symlink to venv binary)
- `/Users/tuananh4865/.hermes/hermes-agent/venv/bin/hermes` (actual binary)
- `/Users/tuananh4865/.hermes/hermes-agent/.venv/bin/hermes` (alt venv)
- `/Users/tuananh4865/.hermes/hermes-agent/hermes` (source dir)

The skill docs don't mention a specific path — `hermes` works from any of these. But for the JSON recipe, the absolute path matters less: `~/.hermes/cron/jobs.json` is fixed regardless of how `hermes` is invoked.

**Path note for cross-platform:** the JSON file path `~/.hermes/cron/jobs.json` is the same on all platforms (macOS, Linux, WSL). The CronTruth recipe is portable.

## When the JSON recipe was discovered

**Validation 10 — 2026-06-28 21:01** (this skill's V10 entry). Previous validations V1-V9 used `hermes cron list | head -80` (V6, V8) or `hermes cron list | grep "Last run"` (V3, V4) or 2 paginated calls (V7). The JSON recipe was discovered when `hermes cron list` failed because the binary at `~/.hermes/bin/hermes` (mentioned in the `hermes-agent` skill's "Key Paths & Config" section) doesn't exist — actual paths are the symlink at `~/.local/bin/hermes` or the venv at `~/.hermes/hermes-agent/venv/bin/hermes`.

**Fix for the skill docs:** the `hermes-agent` skill's "Key Paths & Config" section says `~/.hermes/hermes-agent/` is "Source code (if git-installed)" but doesn't list the venv location where the actual binary lives. This isn't the right skill to patch that — but the JSON recipe bypasses the CLI entirely, so it works regardless of which `hermes` binary is in PATH.

## Recipe variants

### Variant A: Filter by name pattern

```bash
python3 -c "
import json
with open('/Users/tuananh4865/.hermes/cron/jobs.json') as f:
    data = json.load(f)
for job in data.get('jobs', []):
    if 'orchestrator' in job.get('name', '').lower():
        last = job.get('last_run_at') or 'NEVER'
        status = job.get('last_status') or 'pending'
        print(f'{job[\"name\"]}: last={last[:19]} status={status}')
"
```

### Variant B: Find overdue crons (last_run > 2× expected cadence ago)

```bash
python3 -c "
import json
from datetime import datetime, timedelta, timezone

with open('/Users/tuananh4865/.hermes/cron/jobs.json') as f:
    data = json.load(f)
now = datetime.now(timezone.utc)
cadence_hours = {
    '0 * * * *': 1, '0 */6 * * *': 6, '0 3 * * *': 24,
    '*/30 8-22 * * *': 0.5, '0 0 * * *': 24
}
for job in data.get('jobs', []):
    sched = job.get('schedule_display', '?')
    expected_h = cadence_hours.get(sched, 24)
    last = job.get('last_run_at')
    if not last:
        print(f'NEVER: {job[\"name\"]}')
        continue
    last_dt = datetime.fromisoformat(last.replace('Z', '+00:00'))
    age_h = (now - last_dt).total_seconds() / 3600
    threshold = expected_h * 2  # 2× cadence = overdue
    if age_h > threshold:
        print(f'OVERDUE ({age_h:.1f}h, expected {expected_h}h): {job[\"name\"]}')
"
```

### Variant C: Count by status

```bash
python3 -c "
import json
from collections import Counter
with open('/Users/tuananh4865/.hermes/cron/jobs.json') as f:
    data = json.load(f)
statuses = Counter(j.get('last_status') or 'pending' for j in data.get('jobs', []))
print(dict(statuses))
# Expected: {'ok': 18} or {'ok': 17, 'error': 1}
"
```

## CLI fallback when JSON unavailable (V13 variant, validated V16 2026-06-29 12:01)

If `~/.hermes/cron/jobs.json` is missing, malformed, or you want a 1-call CLI alternative without Python:

```bash
hermes cron list 2>&1 | grep -E "Last run|Schedule" | paste - -
```

**How it works:** `grep -E "Last run|Schedule"` extracts two alternating lines per cron (schedule + last run), `paste - -` joins them side-by-side on each line. Output is a 2-column truth table in 1 call:

```
    Schedule:  0 3 * * *	    Last run:  2026-06-29T03:02:48.169523+07:00  ok
    Schedule:  0 7 * * *	    Last run:  2026-06-29T07:04:55.832241+07:00  ok
    Schedule:  30 7 * * *	    Last run:  2026-06-29T07:32:21.903945+07:00  ok
...
```

**When to use this over JSON recipe:**
- You want to read `last_delivery_error` field (JSON doesn't include it by default)
- `jobs.json` is missing or has an older schema
- 1-call budget is critical and you don't want to spawn Python
- The CLI's boxed-drawing chrome is what's causing head-N truncation

**Trade-off:** the CLI output is uglier (boxed drawing chars, indentation noise) but no Python invocation needed. Head-N pagination still applies if you wrap in `| head -N` — but the `paste` pattern strips the boxed-drawing chrome and works at any head-N cutoff.

**V13/V15/V16 lesson (validated across 3 sweeps 2026-06-28 → 2026-06-29):** `hermes cron list | head -60` truncates around the 6th cron (boxed-drawing chars consume the budget). The `grep + paste` pattern is the durable CLI fallback — it strips the chrome and extracts the truth columns in 1 call regardless of head-N cutoff. Used successfully in V16 sweep (12:01 today) after head-60 truncated at cron 6, extracted all 18 crons in 1 follow-up call.

## Historical usage

- **V10 (2026-06-28 21:01):** first recorded use in heartbeat sweep. Replaced V6-V9 `hermes cron list` paginated approach with single 1-call JSON parse. Saved 1-2 tool calls per sweep.
- **V13 (2026-06-28 ~22:00):** added `grep + paste` CLI fallback when JSON parse fails or `hermes cron list` pagination cuts off before the truth columns appear.
- **V15 (2026-06-29 10:30+):** confirmed the CLI pagination gotcha (head -120 + tail -80 hit the same 5-cron cutoff) — the `paste` pattern strips the boxed-drawing chrome and works at any head-N cutoff.
- **V16 (2026-06-29 12:01):** confirmed in production sweep — used `grep -E "Last run|Schedule" | paste - -` after head-60 truncated at cron 6. Extracted all 18 crons in 1 call, no second invocation needed.
- **Future:** expected to become the canonical cron-truth check recipe for all sweeps that need only summary columns.

## Cross-references

- `references/h38-mtime-vs-cron-truth-pattern.md` — the cron-list recipe that this JSON recipe replaces/supplements
- `references/h32b-validation-log.md` — V10 validation entry uses this recipe
- SKILL.md "H32b HARD GATE" — tool-call budget that this recipe helps stay within