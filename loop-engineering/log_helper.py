#!/usr/bin/env python3
"""
Loop Engineering Changelog Helper
Usage:
    from log_helper import log_step, log_file_change, log_qa

Hoặc CLI:
    python3 log_helper.py step "Tạo checker skill" --files ~/.hermes/skills/quality-checker/SKILL.md
    python3 log_helper.py qa PASS "Checker hoạt động đúng"
    python3 log_helper.py file ~/.hermes/skills/quality-checker/SKILL.md "create" "Initial creation"
"""
import os
import json
import argparse
from datetime import datetime, timezone, timedelta

# === Config ===
LOG_DIR = os.path.expanduser("~/.hermes/loop-engineering")
MD_LOG = os.path.join(LOG_DIR, "CHANGELOG.md")
JSON_LOG = os.path.join(LOG_DIR, "changelog.jsonl")

TZ_VN = timezone(timedelta(hours=7))


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


def log_step(step_num: int, title: str, files: list = None, status: str = "in_progress", details: str = ""):
    """Log một step lớn (ví dụ: STEP-1, STEP-2)."""
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
        "ts": iso,
        "type": "STEP",
        "step": step_num,
        "title": title,
        "status": status,
        "files": files or [],
        "details": details,
    })
    print(f"✅ Logged STEP-{step_num}: {title}")


def log_file_change(filepath: str, action: str, note: str = "", before: str = "", after: str = ""):
    """Log một thay đổi file cụ thể."""
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
        "ts": iso,
        "type": "FILE",
        "filepath": filepath,
        "action": action,
        "note": note,
        "has_before": bool(before),
        "has_after": bool(after),
    })
    print(f"✅ Logged file change: {filepath} ({action})")


def log_qa(verdict: str, note: str, step_num: int = None):
    """Log QA gate verdict."""
    ts = now_str()
    iso = now_iso()

    step_ref = f" (STEP-{step_num})" if step_num else ""

    md = f"""### [QA] {ts}{step_ref} — **{verdict}**

**Note:** {note}

---"""
    append_md(md)
    append_json({
        "ts": iso,
        "type": "QA",
        "step": step_num,
        "verdict": verdict,
        "note": note,
    })
    print(f"✅ Logged QA: {verdict} — {note[:60]}")


# === CLI ===
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Loop Engineering Changelog Helper")
    sub = parser.add_subparsers(dest="cmd", required=True)

    # step
    p_step = sub.add_parser("step", help="Log a major step")
    p_step.add_argument("title")
    p_step.add_argument("--num", type=int, required=True)
    p_step.add_argument("--files", nargs="*", default=[])
    p_step.add_argument("--status", default="in_progress")
    p_step.add_argument("--details", default="")

    # file
    p_file = sub.add_parser("file", help="Log a file change")
    p_file.add_argument("filepath")
    p_file.add_argument("action", help="create | edit | delete | move")
    p_file.add_argument("--note", default="")
    p_file.add_argument("--before", default="")
    p_file.add_argument("--after", default="")

    # qa
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
