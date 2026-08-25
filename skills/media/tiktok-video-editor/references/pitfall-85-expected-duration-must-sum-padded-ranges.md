# PITFALL #85 — expected_duration MUST equal SUM of padded KEEP ranges

**Detected:** 23/07/2026 by anh Tuấn Anh testing clip 0034 (creative-arrange test)

## Symptom

When writing `keep_plan.json` manually (or via LLM), it's tempting to estimate
`expected_duration` by gut feel ("should be ~80s"). But the verify gate
compares actual final duration against `expected_duration / 1.3` with ±8s
tolerance. If your estimate is wrong by even 20-30s, the verify FAILS even
though the audio+video themselves are perfect.

Real case (clip 0034 V1):
- I wrote `expected_duration: 80` for 6 KEEP ranges
- Actual padded sum = 126.92s
- Final = 97.66s post-speed 1.3x
- Delta = 36s → FAIL verify_recheck.py
- Spent extra cycle re-running everything before realizing the math mistake

## Fix

**Always compute `expected_duration` from the ranges themselves AFTER smart_pad:**

```python
# Correct workflow:
1. Write ranges in keep_plan.json (start, end, action)
2. Run smart_pad.sh → adds start_padded, end_padded
3. Compute expected_duration = SUM(end_padded - start_padded) for KEEP ranges
4. Update keep_plan.json with computed value
5. target_duration_post_speed = expected_duration / 1.3
```

**Or use a helper:**

```bash
python3 -c "
import json
with open('keep_plan.json') as f: p = json.load(f)
total = sum(
    (r.get('end_padded', r['end']) - r.get('start_padded', r['start']))
    for r in p['ranges'] if r.get('action') == 'KEEP'
)
print(f'expected_duration = {round(total, 2)}')
print(f'target_duration_post_speed = {round(total/1.3, 2)}')
"
```

## Related

- Fix recorded in `wiki/entities/learned-about-tuananh.md` 23/07 entry
