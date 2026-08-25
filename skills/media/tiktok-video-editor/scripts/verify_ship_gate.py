#!/usr/bin/env python3
"""
verify_ship_gate.py — Verify final.mp4 ship-ready trước khi copy ra Pocket3 root.

Đây là checker cứng: nếu FAIL → exit 1, ship.sh KHÔNG được copy.

Usage:
  python3 scripts/verify_ship_gate.py <clip_id>

Exit 0 = ship OK, exit 1 = ship BLOCKED.

Kiểm tra:
  1. final.mp4 tồn tại ở Pocket3/Hermes-Edit/<clip_id>/
  2. recheck.json tồn tại ở Hermes/Edit/<clip_id>/work/recheck_dir/
  3. verify_recheck.py PASS trên keep_plan + recheck transcript
  4. check_tiktok_spec.py PASS (1080×1920 30fps h264 yuv420p aac)
  5. Duration trong Mode B sweet spot (30-120s) — warning nếu ngoài

Nếu PASS → stdout OK + exit 0 → ship.sh copy ra Pocket3 root filename convention.
Nếu FAIL → stdout chi tiết fail reasons + exit 1 → ship.sh block.

See also: references/pitfall-81-ship-no-verify-gate.md
"""
import sys
import subprocess
from pathlib import Path


def main():
    if len(sys.argv) != 2:
        print("Usage: verify_ship_gate.py <clip_id>", file=sys.stderr)
        sys.exit(2)  # 2 = bad args, distinct from 1 = fail

    clip_id = sys.argv[1]

    HERMES_WORK = Path(f"/Volumes/Storage-1/Hermes/Edit/{clip_id}")
    POCKET_EDIT = Path(f"/Volumes/Storage-1/Pocket3/Hermes-Edit/{clip_id}")
    FINAL_MP4 = POCKET_EDIT / "final.mp4"
    KEEP_PLAN = HERMES_WORK / "work" / "keep_plan.json"
    RECHECK_DIR = HERMES_WORK / "work" / "recheck_dir"
    SKILL_SCRIPTS = Path(__file__).parent

    failures = []
    warnings = []

    # 1. final.mp4 tồn tại
    if not FINAL_MP4.exists():
        failures.append(f"final.mp4 not found at {FINAL_MP4}")
        print(f"❌ BLOCKED: {failures[0]}")
        sys.exit(1)

    # 2. recheck.json tồn tại
    recheck_json = None
    if RECHECK_DIR.exists():
        candidates = list(RECHECK_DIR.glob("*.json"))
        if candidates:
            recheck_json = candidates[0]  # primary

    if not recheck_json or not recheck_json.exists():
        warnings.append(f"recheck.json missing at {RECHECK_DIR} — using TikTok spec check only")

    # 3. verify_recheck.py PASS (nếu có recheck)
    if recheck_json and KEEP_PLAN.exists():
        verify_script = SKILL_SCRIPTS / "verify_recheck.py"
        if verify_script.exists():
            proc = subprocess.run(
                ["python3", str(verify_script), str(KEEP_PLAN), str(recheck_json)],
                capture_output=True, text=True
            )
            if proc.returncode != 0:
                failures.append(f"verify_recheck.py FAIL (exit {proc.returncode})")
                # show tail of output for debugging
                if proc.stdout:
                    print("--- verify_recheck.py stdout (last 30 lines) ---")
                    print('\n'.join(proc.stdout.strip().split('\n')[-30:]))
                    print("--- end ---")
                if proc.stderr:
                    print("--- stderr ---")
                    print(proc.stderr)
        else:
            warnings.append(f"verify_recheck.py not found at {verify_script}")

    # 4. check_tiktok_spec.py PASS
    tiktok_script = SKILL_SCRIPTS / "check_tiktok_spec.py"
    if tiktok_script.exists():
        proc = subprocess.run(
            ["python3", str(tiktok_script), str(FINAL_MP4)],
            capture_output=True, text=True
        )
        if proc.returncode != 0:
            failures.append(f"check_tiktok_spec.py FAIL (exit {proc.returncode})")
            if proc.stdout:
                print("--- check_tiktok_spec.py stdout ---")
                print(proc.stdout.strip())
        else:
            # Extract duration from output for Mode B check
            duration = None
            for line in proc.stdout.split('\n'):
                if 'Duration:' in line:
                    try:
                        duration = float(line.split('Duration:')[1].split('s')[0].strip())
                    except (ValueError, IndexError):
                        pass

            # 5. Mode B sweet spot
            if duration is not None:
                if duration < 30:
                    warnings.append(f"Duration {duration:.1f}s < 30s (Mode B min) — may be too short")
                elif duration > 120:
                    warnings.append(f"Duration {duration:.1f}s > 120s (Mode B max) — may be too long")
                else:
                    print(f"✅ Duration {duration:.1f}s in Mode B sweet spot (30-120s)")
    else:
        failures.append(f"check_tiktok_spec.py not found at {tiktok_script}")

    # Summary
    print("\n═══════════════════════════════════════════════════════════════")
    if failures:
        print(f"🚫 SHIP BLOCKED — {len(failures)} critical failure(s):")
        for f in failures:
            print(f"  ❌ {f}")
        if warnings:
            print(f"\n⚠️  {len(warnings)} warning(s):")
            for w in warnings:
                print(f"  ⚠️  {w}")
        sys.exit(1)

    print(f"✅ SHIP OK — {len(warnings)} warning(s)")
    for w in warnings:
        print(f"  ⚠️  {w}")
    sys.exit(0)


if __name__ == "__main__":
    main()
