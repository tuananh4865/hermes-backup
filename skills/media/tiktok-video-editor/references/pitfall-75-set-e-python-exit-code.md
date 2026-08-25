# PITFALL #75 — `set -e` + Python exit code (v0.01)

## Reproducible shell bug
Trong `recheck.sh`, em viết:
```bash
#!/bin/bash
set -e  # Exit on first error
...
python3 verify_recheck.py "$JSON" "$PLAN" 2>&1 | tee /tmp/report.txt
VERIFY_EXIT=$?  # ⚠️ Capture exit of tee, NOT Python
```

Khi `verify_recheck.py` exit code 1 (FAIL), `tee` vẫn exit 0 → `VERIFY_EXIT=0` → shell nghĩ PASS.

Bug: User flag `recheck.sh` returns exit code 0 mặc dù output báo FAIL.

## Fix v0.01
```bash
#!/bin/bash
# KHÔNG dùng `set -e` vì verify_recheck.py cần exit 1 signal FAIL

python3 verify_recheck.py "$JSON" "$PLAN" 2>&1 > /tmp/report.txt
VERIFY_EXIT=$?

cat /tmp/report.txt  # Display nội dung cho user

if [ $VERIFY_EXIT -eq 0 ]; then
    echo "✅ VERIFY PASS"
    exit 0
else
    echo "❌ VERIFY FAIL"
    exit $VERIFY_EXIT
fi
```

Key changes:
1. **Remove `set -e`** at top — interferes with intentional exit-1 signals
2. **Redirect stdout to file** with `> /tmp/report.txt` (not pipe to tee) — capture Python's actual exit code
3. **Cat file after** — separate output writing from exit code capture
4. **Explicit `exit $VERIFY_EXIT`** — propagate Python's exit code to caller

## Bài học (universal shell pattern)
Khi shell script capture exit code của subprocess:
- ❌ `cmd | tee file ; exit=$?` — capture tee (luôn 0 nếu stdin OK)
- ✅ `cmd > file ; exit=$?` — capture cmd thật
- ✅ Hoặc dùng `${PIPESTATUS[0]}` cho pipe cuối cùng: `cmd | tee file ; exit=${PIPESTATUS[0]}`

`set -e` kết hợp với multi-step pipeline cần careful planning. Default ON, khi cần exit code từ pipeline thì OFF locally.
