# V2 NDJSON Compact Format — Why + How

> Sub-document of `hermes-file-edit-logging` skill. Documents the NDJSON compact format choice (no space after `:`) so it can be reused for ANY audit log file in the future.

## What is NDJSON?

**NDJSON** (Newline-Delimited JSON) — one JSON object per line, separated by `\n`. Spec: http://ndjson.org/

**Compact form**: `json.dumps(obj, separators=(",", ":"))` → no whitespace between tokens.

```python
# Pretty (default) — INVALID for grep-friendly logs
{"key": "value", "list": [1, 2, 3]}

# Compact (NDJSON standard) — grep-friendly
{"key":"value","list":[1,2,3]}
```

## Why we picked compact (Stripe / CloudTrail / AWS audit log pattern)

| Criterion | Pretty JSON | NDJSON compact |
|-----------|-------------|----------------|
| Grep `"key":"value"` | ❌ breaks (space) | ✅ works |
| File size | 100% | ~50% (no whitespace) |
| 1 line per entry | ✅ | ✅ |
| `jq` parse | ✅ | ✅ |
| `awk`/`sed` per-line | ✅ | ✅ |
| Industry adoption | logs only | **Stripe, CloudTrail, AWS, GitHub Actions, GitLab CI** |

Decision: Compact wins on every dimension that matters for audit logs.

## The grep test that caught the bug

```bash
# V1 (pretty) — FAILS
echo '{"action": "create", "file": "x.py"}' | grep '"action":"create"'
# → no match (extra space after `:`)

# V2 (compact) — WORKS
echo '{"action":"create","file":"x.py"}' | grep '"action":"create"'
# → match
```

This was the actual bug V1 shipped on 2026-07-19 — `log_helper.py` used `json.dumps(entry)` default → format had spaces → `grep` failed in test 6 of verify. V2 fixed it with `separators=(",", ":")`.

## Canonical Python snippet (use in EVERY audit log script)

```python
import json
from datetime import datetime, timezone, timedelta

ICT = timezone(timedelta(hours=7))
ts = datetime.now(ICT).isoformat()

entry = {
    "ts": ts,
    "event": "file_edit",   # or "memory_add", "cron_run", "session_start", etc.
    "file": "Hermes/scripts/foo.py",
    "action": "create",
    "reason": "Init",
    "before": 0,
    "after": 10255,
}

# Compact + append (NDJSON)
with open("/path/to/audit.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(entry, ensure_ascii=False, separators=(",", ":")) + "\n")
```

Key points:
1. `ensure_ascii=False` — keeps Vietnamese chars as-is, not `\uXXXX` escapes (smaller + human-readable)
2. `separators=(",", ":")` — strips all inter-token whitespace
3. `\n` terminator per line — 1 entry per line
4. `open(..., "a")` — append mode, NEVER overwrite (audit logs must be append-only)
5. ISO 8601 timestamps with explicit timezone (`+07:00`) — no ambiguity

## Reusable for ANY audit log type

| Use case | File | Trigger |
|----------|------|---------|
| File edits | `logs/daily/YYYY-MM-DD.jsonl` | post_tool_call hook on write_file/patch |
| Memory facts | `~/.hermes/memory_store.db` | `fact_store` action=add (holographic DB, but concepts transfer) |
| Cron runs | `cron-output/<job-id>/YYYY-MM-DD.log` | wrapper script redirect stdout |
| Session start | `logs/sessions/YYYY-MM-DD-{session-id}.jsonl` | `on_session_start` hook |
| Errors | `logs/errors/YYYY-MM-DD-errors.jsonl` | try/except wrapper |
| Tool calls | `logs/tool-calls/YYYY-MM-DD.jsonl` | post_tool_call (not yet implemented) |

Same format, same grep pattern, same parsing — one mental model.

## Anti-patterns (refuse)

| Anti-pattern | Why it fails |
|---|---|
| Pretty-printed `json.dumps(...)` in append-only log | grep `'\"action\":\"x\"'` fails |
| Mixed format (some compact, some pretty) | Inconsistent — caller can't predict |
| Trailing newline missing | Last line breaks `awk 'NR==n'` |
| `ensure_ascii=True` (default) | Vietnamese chars become `\u1ec7` → unreadable |
| Sorting entries in file | Append-only means NEW = LAST, no sort |
| Compressing old NDJSON in-place | You can't decompress per-line; archive full files instead |

## Verification recipe

```bash
# File should be valid NDJSON (1 JSON per line, no trailing junk)
python3 -c "
import json, sys
with open('/path/to/audit.jsonl') as f:
    for i, line in enumerate(f, 1):
        try:
            json.loads(line)
        except json.JSONDecodeError as e:
            print(f'Line {i} INVALID: {e}')
            sys.exit(1)
print('✅ All lines valid JSON')
"

# Compactness check (should be 0 newlines within a single entry)
python3 -c "
import json
with open('/path/to/audit.jsonl') as f:
    entry = json.loads(f.readline())
    s = json.dumps(entry, ensure_ascii=False, separators=(',', ':'))
    assert s == f.readline().rstrip(), 'NOT compact'
    print('✅ Compact format verified')
"
```

## References

- NDJSON spec: http://ndjson.org/
- Stripe API log format: https://stripe.com/docs/api/events
- AWS CloudTrail log format: https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-event-reference.html
- jq manual (for parsing NDJSON): https://stedolan.github.io/jq/manual/

---

*Created 2026-07-19 after V1 grep bug discovery. Use as the canonical pattern for EVERY future audit log in the Hermes system.*
