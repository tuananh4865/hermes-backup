# PITFALL #81 — `ship.sh` không gate trên `verify_recheck.py` exit code

**Context (22/07):** Background process `proc_ee4bef03550a` render file `final.mp4` chỉ **7.33s, 5.9 MB** (clip cụt do interrupt lúc ffmpeg encode hoặc keep_plan bị half-applied). `recheck.sh` exit 1 với duration delta 50.51s (expected 57.7s vs actual 7.2s, FAIL). Nhưng `ship.sh` được gọi ngay sau **mà không check exit code của recheck** → copy file 5.9MB incomplete ra `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0036_V1_64_FINAL_LENS_MACRO.mp4`. File hiện tại đã được re-render đúng (64.20s, 58 MB, TikTok spec ALL PASS) nhưng ship.sh bug vẫn tồn tại trong code.

**Repro:**
```bash
# Sequence:
bash build_pre_speed.sh 0036    # OK, file pre-speed 80s
bash render_speed.sh 0036       # OK nhưng file ngắn hơn expected (partial)
bash recheck.sh 0036            # Exit 1 (FAIL delta 50.51s)
echo "Recheck exit: $?"         # → 1
bash ship.sh 0036 V1 64         # ← silent copy dù recheck FAIL
ls -la /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0036_*.mp4
# → File ship 5.9MB (incomplete)
```

**Fix v0.01.1 (planned):**

`ship.sh` MUST re-call `verify_recheck.py` trước khi copy. Pattern:

```bash
#!/bin/bash
set -e

CLIP_ID="$1"
# ... existing arg parsing ...

# HARD GATE: recheck MUST PASS before ship
WORK="/Volumes/Storage-1/Hermes/Edit/$CLIP_ID"
RECHECK_GLOB="$WORK/work/recheck_dir/${CLIP_ID}_final_audio.json"

if [ ! -f "$RECHECK_GLOB" ]; then
    # Fallback to any .json in recheck_dir
    RECHECK_GLOB=$(ls "$WORK/work/recheck_dir"/*.json 2>/dev/null | head -1)
fi

if [ -n "$RECHECK_GLOB" ] && [ -f "$RECHECK_GLOB" ]; then
    if ! python3 "$SCRIPT_DIR/verify_recheck.py" \
        "$WORK/work/keep_plan.json" "$RECHECK_GLOB" > /tmp/ship_verify.txt 2>&1; then
        echo "❌ SHIP BLOCKED: recheck FAIL"
        cat /tmp/ship_verify.txt
        exit 1
    fi
else
    echo "⚠️  No recheck JSON found — proceeding without verify gate"
fi

# ... existing cp logic ...
```

**Lesson:**
- Step chain `render → recheck → ship` không tự động propagate exit code giữa các shell invocations
- Caller phải tự check `$?` giữa các step HOẶC mỗi script phải tự gate trên dependency của nó
- `set -e` không hoạt động xuyên script boundary — chỉ trong 1 process

**Verification:** Repro trên case 22/07 (clip 0036 V1 cũ). Sau khi áp fix, ship.sh với recheck exit 1 phải block copy.

**Related:** PITFALL #75 (set -e + Python exit code) — cùng pattern category về exit code misinterpretation.
