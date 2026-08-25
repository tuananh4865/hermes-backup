#!/usr/bin/env python3
"""
Rotate + prune Hermes activity logs.

- gzip any daily JSONL older than KEEP_PLAIN_DAYS
- delete archives older than KEEP_TOTAL_DAYS
Idempotent; safe to run from cron daily.

Usage: python3 rotate_activity_logs.py [--dry-run]
"""

import argparse
import gzip
import shutil
from datetime import datetime, timedelta, timezone
from pathlib import Path

ICT = timezone(timedelta(hours=7))
LOG_DIRS = [
    Path("/Volumes/Storage-1/Hermes/logs/activity"),
    Path.home() / ".hermes" / "logs" / "activity",
]
KEEP_PLAIN_DAYS = 14   # keep raw JSONL grep-able for 2 weeks
KEEP_TOTAL_DAYS = 180  # analyzer supports --days 90; keep 180 for headroom


def day_of(path: Path):
    stem = path.name.split(".")[0]
    try:
        return datetime.strptime(stem, "%Y-%m-%d").replace(tzinfo=ICT)
    except ValueError:
        return None


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    now = datetime.now(ICT)
    gz_cut = now - timedelta(days=KEEP_PLAIN_DAYS)
    rm_cut = now - timedelta(days=KEEP_TOTAL_DAYS)
    gzipped = deleted = 0
    freed = 0

    for directory in LOG_DIRS:
        if not directory.is_dir():
            continue
        for path in sorted(directory.iterdir()):
            day = day_of(path)
            if day is None:
                continue
            if path.suffix == ".gz":
                if day < rm_cut:
                    freed += path.stat().st_size
                    print(f"{'[dry] ' if args.dry_run else ''}delete  {path}")
                    if not args.dry_run:
                        path.unlink()
                    deleted += 1
                continue
            if path.suffix == ".jsonl" and day < gz_cut:
                target = path.with_suffix(".jsonl.gz")
                print(f"{'[dry] ' if args.dry_run else ''}gzip    {path.name} -> {target.name}")
                if not args.dry_run:
                    with open(path, "rb") as src, gzip.open(target, "wb", compresslevel=9) as dst:
                        shutil.copyfileobj(src, dst)
                    path.unlink()
                gzipped += 1

    print(f"\ngzipped={gzipped} deleted={deleted} freed={freed/1024:.1f} KB")


if __name__ == "__main__":
    main()
