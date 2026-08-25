#!/usr/bin/env python3
"""
Loop Engineering Changelog Helper — STANDARD SCRIPT.
Shipped with the loop-engineering-deployment skill. Copy to
~/.hermes/loop-engineering/log_helper.py on first deployment, then reuse.

Usage:
    # Python API
    from log_helper import log_step, log_file_change, log_qa
    log_step(1, "Create checker skill", ["/path/file"], "done")
    log_file_change("/path/file", "create", "Initial creation")
    log_qa("PASS", "Tests passed", step_num=1)

    # CLI
    python3 log_helper.py step "Create checker skill" --num 1 --files /path/file
    python3 log_helper.py file /path/file create --note "Initial"
    python3 log_helper.py qa PASS "Tests passed" --step 1

Files written:
    ~/.hermes/loop-engineering/CHANGELOG.md  — human-readable, append-only
    ~/.hermes/loop-engineering/changelog.jsonl — machine-readable, one JSON per line
"""
import os
import json
import argparse
from datetime import datetime, timezone, timedelta

# === Config ===
LOG_DIR = os.path.expanduser("~/.hermes/loop-engineering")
MD_LOG = os.path.join(LOG_DIR, "CHANGELOG.md")
JSON_LOG = os.path.join(LOG_DIR, "changelog.jsonl")
TZ_VN = timezone(timedelta(hours=7))  # Vietnam — adjust per user


def now_str():
    return datetime.now(TZ_VN).strftime("%Y-%m-%d %H:%M:%S %z")


def now_iso():
    return datetime.now(TZ_VN).isoformat()


def ensure_dir():
    os.makedirs(LOG_DIR, exist_ok=True)


def append_json(entry: dict):
    ensure_dir()
    with open(JSON_LOG, "a") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def append_md(md_block: str):
    ensure_dir()
    with open(MD_LOG, "a") as f:
        f.write("\n" + md_block + "\n")


def log_step(step_num, title, files=None, status="in_progress", details=""):
    """Log a major step. Use once per file-creation milestone."""
    ts = now_str()
    iso = now_iso()
    files_str = ", ".join(f"`{f}`" for f in (files or [])) or "_(chưa tạo file)_"
    md = f"""## [STEP-{step_num}] {ts} — {title}

**Status:** {status}
**Files affected:** {files_str}

{details}

---"""
    append_md(md)
    append_json({
        "ts": iso, "type": "STEP", "step": step_num,
        "title": title, "status": status,
        "files": files or [], "details": details,
    })
    print(f"✅ Logged STEP-{step_num}: {title}")


def log_file_change(filepath, action, note="", before="", after=""):
    """Log every individual file edit. Call this for EVERY file create/edit/delete."""
    ts = now_str()
    iso = now_iso()
    before_block = f"\n**Before:**\n```\n{before[:500]}\n```" if before else ""
    after_block = f"\n**After:**\n```\n{after[:500]}\n```" if after else ""
    md = f"""### [FILE] {ts} — `{filepath}`

- **Action:** {action}
- **Note:** {note or '_(no note)_'}
{before_block}
{after_block}
---"""
    append_md(md)
    append_json({
        "ts": iso, "type": "FILE", "filepath": filepath,
        "action": action, "note": note,
        "has_before": bool(before), "has_after": bool(after),
    })
    print(f"✅ Logged file change: {filepath} ({action})")


def log_qa(verdict, note, step_num=None):
    """Log QA gate verdict (PASS / FAIL / WARN). One per step."""
    ts = now_str()
    iso = now_iso()
    step_ref = f" (STEP-{step_num})" if step_num else ""
    md = f"""### [QA] {ts}{step_ref} — **{verdict}**

**Note:** {note}

---"""
    append_md(md)
    append_json({
        "ts": iso, "type": "QA", "step": step_num,
        "verdict": verdict, "note": note,
    })
    print(f"✅ Logged QA: {verdict} — {note[:60]}")


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loop Engineering Changelog Helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_step = sub.add_parser("step", help="Log a major step")
    p_step.add_argument("title")
    p_step.add_argument("--num", type=int, required=True)
    p_step.add_argument("--files", nargs="*", default=[])
    p_step.add_argument("--status", default="in_progress")
    p_step.add_argument("--details", default="")

    p_file = sub.add_parser("file", help="Log a file change")
    p_file.add_argument("filepath")
    p_file.add_argument("action", help="create | edit | delete | move")
    p_file.add_argument("--note", default="")
    p_file.add_argument("--before", default="")
    p_file.add_argument("--after", default="")

    p_qa = sub.add_parser("qa", help="Log QA gate")
    p_qa.add_argument("verdict", help="PASS | FAIL | WARN")
    p_qa.add_argument("note")
    p_qa.add_argument("--step", type=int, default=None)

    args = parser.parse_args()
    if args.cmd == "step":
        log_step(args.num, args.title, args.files, args.status, args.details)
    elif args.cmd == "file":
        log_file_change(args.filepath, args.action, args.note, args.before, args.after)
    elif args.cmd == "qa":
        log_qa(args.verdict, args.note, args.step)
