# Session Timestamp Boundaries — 2026-07-28

## Lesson
Incorrect Unix timestamp calculation caused first query to return 0 results. Must use `date -j -f` on macOS to get correct boundaries.

## Wrong approach (returned 0 sessions)
```python
# INCORRECT — these are wrong Unix timestamps
yesterday_start = 1750966800  # off by ~3.9 years
today_start = 1751053200
```

## Correct approach (verified 2026-07-28)
```python
import subprocess

result = subprocess.run(
    ['date', '-j', '-f', '%Y-%m-%d %H:%M:%S %z', '2026-07-27 00:00:00 +0700', '+%s'],
    capture_output=True, text=True
)
yesterday_start = int(result.stdout.strip())  # 1785085200

result = subprocess.run(
    ['date', '-j', '-f', '%Y-%m-%d %H:%M:%S %z', '2026-07-28 00:00:00 +0700', '+%s'],
    capture_output=True, text=True
)
today_start = int(result.stdout.strip())  # 1785171600
```

## Known good timestamps (Jul 2026)
| Boundary | Unix | Human (+07) |
|----------|------|-------------|
| Jul 27 00:00 +07 | 1785085200 | 2026-07-27 00:00 |
| Jul 28 00:00 +07 | 1785171600 | 2026-07-28 00:00 |
| Jul 26 19:07 +07 | ~1785036420 | Jul 26 evening |

## Session window bleed (from Jul 18 session)
Session `20260718_071838_8d4cf9aa` started Jul 18 07:18 but ran until Jul 19 00:00 (~16.5h).
Its `ended_at` was logged in Jul 19 cron DB.
**Rule:** Cross-reference `started_at` vs `ended_at`. If `started_at` is in yesterday but `ended_at` in today's early hours, classify under yesterday.
