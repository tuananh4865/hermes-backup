# PITFALL #84 — ship.sh không gate trên verify_recheck.py exit code

> **Status:** ⚠️ UNFIXED in v0.01. Planned cho v0.01.1.

## Symptom

Background process `proc_ee4bef03550a` ngày 22/07:
- `build_pre_speed.sh` → OK (83.44s, 193.53MB)
- `render_speed.sh` → final.mp4 chỉ **7.33s, 5.9 MB** (clip quá ngắn — file incomplete do interrupt)
- `check_tiktok_spec.py` → PASS (chỉ check resolution, KHÔNG check duration)
- `recheck.sh` → exit 1 (FAIL duration delta 50.51s)
- `ship.sh` → **VẪN COPY** 5.9 MB incomplete file ra `/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0036_V1_64_FINAL_LENS_MACRO.mp4`

**Root cause:** `ship.sh` không phụ thuộc `recheck.sh` exit code. Caller chạy `ship.sh` độc lập → cp file FAIL.

## Reproduction recipe

```bash
cd /Volumes/Storage-1/Hermes/Edit/0036

# Force a bad render
rm -f /Volumes/Storage-1/Pocket3/Hermes-Edit/0036/final.mp4
# (don't re-render; keep old final.mp4 fake)
ffmpeg -y -f lavfi -i color=size=1920x1080:duration=7.3 -i sine=frequency=440:duration=7.3 \
    -c:v libx264 -preset ultrafast -c:a aac /Volumes/Storage-1/Pocket3/Hermes-Edit/0036/final.mp4

bash scripts/recheck.sh 0036
# → Exit code: 1 (FAIL)

bash scripts/ship.sh 0036 V1 7 LENS_MACRO
# → ⚠️ VẪN SHIP! 5.9 MB ra Pocket3 root
```

## Expected behavior (v0.01.1)

`ship.sh` phải là HARD GATE cuối cùng:
- Caller chạy `recheck.sh` trước, exit 0 mới được gọi `ship.sh`
- HOẶC `ship.sh` tự re-call `verify_recheck.py` trước khi cp, exit 1 nếu FAIL

```bash
# ship.sh v0.01.1 plan
SHIP_FILE="$SHIP_DIR/clip_${CLIP_ID}_${VERSION}_${DURATION}_FINAL_${SP_NAME}.mp4"

# Re-verify trước khi ship (đảm bảo hard gate)
if ! python3 "$SCRIPT_DIR/verify_recheck.py" \
        "$WS/work/keep_plan.json" \
        "$WS/work/recheck_dir/$(ls $WS/work/recheck_dir/ | grep .json | head -1)" \
        > /tmp/ship_verify.txt 2>&1; then
    echo "❌ ship.sh BLOCKED — verify FAIL"
    cat /tmp/ship_verify.txt
    exit 1
fi

cp "$FINAL" "$SHIP_FILE"
echo "✅ SHIPPED: ${SZ_MB} MB"
```

## Why this matters

- User nhận output FAIL trên iPhone, không biết clip cụt
- Background process sai → render aborted → file incomplete
- Silent fail (file exists, looks fine, but content wrong)

## Verified fix (planned)

| Field | Current | Required |
|---|---|---|
| ship.sh gate | KHÔNG | CÓ (re-run verify_recheck.py) |
| Error message nếu FAIL | KHÔNG | "❌ ship.sh BLOCKED — verify FAIL" |
| Exit code nếu FAIL | 0 | 1 |
| Caller convention | Run ship.sh directly | Run recheck.sh first, then ship.sh |

See: `/Volumes/Storage-1/Hermes/logs/bugs/2026-07-22-ship-no-verify-gate.md` for original bug log.
