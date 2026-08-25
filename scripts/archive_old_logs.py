#!/usr/bin/env python3
"""
Archive old log files (monthly cron task).

- daily/*.jsonl > 90 days → move to archive/{YYYY}/{YYYY-MM}/{filename}
- archive/*.jsonl > 365 days → compress .gz (optional, see flag)

Usage:
    python3 archive_old_logs.py           # dry-run (show what would move)
    python3 archive_old_logs.py --apply   # actually move files
    python3 archive_old_logs.py --gzip    # also gzip files >365 days

Runs monthly via cron (1st day of month, 02:30 ICT).
"""
import argparse
import gzip
import shutil
import sys
from datetime import datetime, timedelta
from pathlib import Path

LOGS_ROOT = Path("/Volumes/Storage-1/Hermes/logs")
DAILY = LOGS_ROOT / "daily"
ARCHIVE = LOGS_ROOT / "archive"

DAILY_TTL_DAYS = 90
ARCHIVE_TTL_DAYS = 365


def parse_date_from_filename(path: Path) -> datetime:
    """Extract YYYY-MM-DD from filename like '2026-07-19.jsonl'."""
    try:
        return datetime.strptime(path.stem, "%Y-%m-%d")
    except ValueError:
        return None


def move_to_archive(file_path: Path, dry_run: bool) -> str:
    """Move file to archive/{YYYY}/{YYYY-MM}/{filename}."""
    date = parse_date_from_filename(file_path)
    if not date:
        return None
    year = date.strftime("%Y")
    month = date.strftime("%Y-%m")
    dest_dir = ARCHIVE / year / month
    dest_file = dest_dir / file_path.name
    if dest_file.exists():
        return None  # skip duplicate
    if dry_run:
        return f"  DRY: {file_path} → {dest_file}"
    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.move(str(file_path), str(dest_file))
    return f"  MOVED: {file_path.name} → {dest_file.relative_to(LOGS_ROOT)}"


def gzip_old_file(file_path: Path, dry_run: bool) -> str:
    """Gzip a file in-place if not already gzipped."""
    if file_path.suffix == ".gz":
        return None
    gz_path = file_path.with_suffix(file_path.suffix + ".gz")
    if gz_path.exists():
        return None
    if dry_run:
        return f"  DRY-GZIP: {file_path}"
    with open(file_path, "rb") as f_in:
        with gzip.open(gz_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)
    file_path.unlink()
    return f"  GZIPPED: {gz_path.relative_to(LOGS_ROOT)}"


def main():
    parser = argparse.ArgumentParser(description="Archive old Hermes logs")
    parser.add_argument("--apply", action="store_true", help="Actually move/gzip (default: dry-run)")
    parser.add_argument("--gzip", action="store_true", help="Also gzip files >365 days")
    args = parser.parse_args()
    dry_run = not args.apply

    if dry_run:
        print("🔍 DRY RUN (use --apply to actually move/gzip):\n")
    else:
        print("🚀 APPLYING changes:\n")

    today = datetime.now()
    daily_cutoff = today - timedelta(days=DAILY_TTL_DAYS)
    archive_cutoff = today - timedelta(days=ARCHIVE_TTL_DAYS)

    moved = 0
    gzipped = 0

    # 1. Move daily/*.jsonl > 90 days to archive/
    if DAILY.exists():
        for log_file in sorted(DAILY.glob("*.jsonl")):
            date = parse_date_from_filename(log_file)
            if not date:
                continue
            if date < daily_cutoff:
                result = move_to_archive(log_file, dry_run)
                if result:
                    print(result)
                    moved += 1

    # 2. Optionally gzip archive files > 365 days
    if args.gzip and ARCHIVE.exists():
        for log_file in ARCHIVE.rglob("*.jsonl"):
            mtime = datetime.fromtimestamp(log_file.stat().st_mtime)
            if mtime < archive_cutoff:
                result = gzip_old_file(log_file, dry_run)
                if result:
                    print(result)
                    gzipped += 1

    print(f"\n📊 Summary: {moved} moved, {gzipped} gzipped")
    if dry_run:
        print("   (dry run — pass --apply to execute)")


if __name__ == "__main__":
    main()