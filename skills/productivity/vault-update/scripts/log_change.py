#!/usr/bin/env python3
"""log_change.py — append exactly ONE line to wiki/CHANGELOG.md.

Part of the `vault-update` skill (EP @eptwts Post A Prompt 2, post 2080342488728904164).

EP P2 mandates one changelog line per filing action, append-only, never rewritten.
This script is the only sanctioned writer of that file from this skill.

Line format (fixed, parseable):

    [2026-08-13 14:30 ICT] vault-update | file=concepts/foo.md | action=create | reason="new mention in Telegram" | as_of=2026-08-13 | supersedes=null

Guardrails
----------
* append-only  : opens with mode "a", never reads-modifies-writes the file
* no invented date : --as-of must be YYYY-MM-DD; refuses today's date unless --allow-today
                     (EP P2: as_of is when the fact was ACTUALLY true, not when you logged it)
* atomic-ish  : single write() of one newline-terminated line
* idempotent header : header block written only when the file does not yet exist

Usage
-----
    python3 log_change.py --file concepts/booking-rate-2026-07-31.md \
        --action create --reason "new rate mentioned in passing on Telegram" \
        --as-of 2026-07-31 --supersedes concepts/booking-rate-2026-05-02.md

    # the paired supersede line for the old note
    python3 log_change.py --file concepts/booking-rate-2026-05-02.md \
        --action supersede --reason "replaced by 2026-07-31 rate" \
        --as-of 2026-05-02 --superseded-by concepts/booking-rate-2026-07-31.md

    python3 log_change.py ... --dry-run     # print the line, write nothing
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

DEFAULT_VAULT = Path("/Volumes/Storage-1/Hermes/wiki")
CHANGELOG_NAME = "CHANGELOG.md"
TZ = ZoneInfo("Asia/Ho_Chi_Minh")
TZ_LABEL = "ICT"

ACTIONS = ("create", "supersede", "append", "noop", "correct")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

HEADER = """# Vault Changelog

> Append-only ledger written by the `vault-update` skill (EP @eptwts Post A Prompt 2).
> One line per filing action. Never edit, reorder, dedupe, or delete lines in this file.
> Format: `[YYYY-MM-DD HH:MM ICT] vault-update | file=<rel path> | action=<action> | reason="..." | as_of=<date> | supersedes=<rel path|null>`
> Narrative history lives in `log.md`; this file is the machine-checkable audit trail.

"""


def clean(text: str) -> str:
    """Keep the line single-line and unambiguous for the pipe/quote format."""
    return " ".join(text.replace('"', "'").split())


def build_line(
    file_rel: str,
    action: str,
    reason: str,
    as_of: str,
    supersedes: str | None,
    superseded_by: str | None,
    now: dt.datetime,
) -> str:
    stamp = now.strftime("%Y-%m-%d %H:%M")
    parts = [
        f"[{stamp} {TZ_LABEL}] vault-update",
        f"file={file_rel}",
        f"action={action}",
        f'reason="{clean(reason)}"',
        f"as_of={as_of}",
        f"supersedes={supersedes or 'null'}",
    ]
    if superseded_by:
        parts.append(f"superseded_by={superseded_by}")
    return " | ".join(parts)


def normalise_rel(value: str, vault: Path) -> str:
    """Store paths relative to the vault root, no leading slash."""
    p = Path(value)
    if p.is_absolute():
        try:
            return str(p.relative_to(vault))
        except ValueError:
            return str(p)
    return str(p).lstrip("./")


def main() -> int:
    ap = argparse.ArgumentParser(description="Append one line to wiki/CHANGELOG.md (vault-update Step 6).")
    ap.add_argument("--file", required=True, help="note path, relative to vault root (or absolute)")
    ap.add_argument("--action", required=True, choices=ACTIONS)
    ap.add_argument("--reason", required=True, help="why this note was written / superseded")
    ap.add_argument("--as-of", required=True, dest="as_of",
                    help="YYYY-MM-DD when the fact was ACTUALLY true (not today, unless --allow-today)")
    ap.add_argument("--supersedes", default=None, help="note this one replaces (rel path)")
    ap.add_argument("--superseded-by", default=None, dest="superseded_by",
                    help="for action=supersede: the new current note")
    ap.add_argument("--vault", default=os.environ.get("HERMES_WIKI", str(DEFAULT_VAULT)))
    ap.add_argument("--allow-today", action="store_true",
                    help="permit as_of == today (only when the fact really became true today)")
    ap.add_argument("--dry-run", action="store_true", help="print the line, write nothing")
    args = ap.parse_args()

    vault = Path(args.vault).expanduser()
    if not vault.exists():
        print(f"ERROR: vault not found: {vault}", file=sys.stderr)
        return 2

    if not DATE_RE.match(args.as_of):
        print(f"ERROR: --as-of must be YYYY-MM-DD, got {args.as_of!r}. "
              "Never invent a date — ask the user or set needs_verification: true.", file=sys.stderr)
        return 2

    try:
        as_of_date = dt.date.fromisoformat(args.as_of)
    except ValueError:
        print(f"ERROR: --as-of is not a real calendar date: {args.as_of!r}", file=sys.stderr)
        return 2

    now = dt.datetime.now(TZ)
    today = now.date()

    if as_of_date > today:
        print(f"ERROR: --as-of {args.as_of} is in the future (today {today}). Refusing.", file=sys.stderr)
        return 2

    if as_of_date == today and not args.allow_today:
        print(
            f"ERROR: --as-of equals today ({today}). EP P2 hard rule: as_of is when the fact was "
            "ACTUALLY true, never the logging date.\n"
            "  -> pass the real date, or --allow-today if the fact genuinely began today.",
            file=sys.stderr,
        )
        return 3

    if args.action == "supersede" and not args.superseded_by:
        print("ERROR: action=supersede requires --superseded-by (links must point both ways).", file=sys.stderr)
        return 2

    file_rel = normalise_rel(args.file, vault)
    supersedes = normalise_rel(args.supersedes, vault) if args.supersedes else None
    superseded_by = normalise_rel(args.superseded_by, vault) if args.superseded_by else None

    line = build_line(file_rel, args.action, args.reason, args.as_of, supersedes, superseded_by, now)

    changelog = vault / CHANGELOG_NAME
    if args.dry_run:
        print("[dry-run] would append to", changelog)
        print(line)
        return 0

    new_file = not changelog.exists()
    with changelog.open("a", encoding="utf-8") as fh:   # append-only, never r+/w
        if new_file:
            fh.write(HEADER)
        fh.write(line + "\n")

    total = sum(1 for _ in changelog.open(encoding="utf-8"))
    print(f"appended -> {changelog}  ({total} lines total)")
    print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
