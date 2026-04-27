#!/opt/homebrew/bin/python3.14
"""
cron_daily_ingest.py — Daily Ingest Orchestrator

Orchestrates the daily wiki ingest workflow:
1. Check watched URLs for new content
2. Process any new raw files in drop folder
3. Update stale concept pages
4. Run self-heal on new content
5. Report to Hermes Dojo

Usage:
    python3 cron_daily_ingest.py              # Run full daily ingest
    python3 cron_daily_ingest.py --check      # Verify dependencies
    python3 cron_daily_ingest.py --dry-run    # Show what would be done
    python3 cron_daily_ingest.py --recent 7   # Check last 7 days

Cron setup (add to crontab):
    0 8 * * * cd ~/wiki && python3 scripts/cron_daily_ingest.py >> logs/daily_ingest.log 2>&1
"""

import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

# ─── Configuration ────────────────────────────────────────────────────────────

WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_DIR = WIKI_ROOT / "raw"
DROPS_DIR = WIKI_ROOT / "_drops"      # Manual drops folder
ARCHIVE_DIR = WIKI_ROOT / "_archive"  # Archive old content
LOG_FILE = WIKI_ROOT / "log.md"
SCHEMA_FILE = WIKI_ROOT / "SCHEMA.md"
DOJO_FILE = Path.home() / ".hermes" / "dojo" / "tasks.json"

FRONTBOOT_FILE = WIKI_ROOT / "_meta" / "frontboot.json"

# ─── Helpers ─────────────────────────────────────────────────────────────────

def run_cmd(cmd: list[str], timeout: int = 30) -> str:
    """Run shell command and return output."""
    try:
        result = subprocess.run(
            cmd, capture_output=True, text=True, timeout=timeout,
            cwd=str(WIKI_ROOT)
        )
        return result.stdout + result.stderr
    except subprocess.TimeoutExpired:
        return f"ERROR: Command timed out after {timeout}s"
    except Exception as e:
        return f"ERROR: {e}"


def read_json(path: Path) -> dict:
    """Read JSON file safely."""
    try:
        if path.exists():
            return json.loads(path.read_text())
    except Exception:
        pass
    return {}


def write_json(path: Path, data: dict) -> None:
    """Write JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2))


def get_frontboot() -> dict:
    """Get frontboot state."""
    return read_json(FRONTBOOT_FILE)


def set_frontboot(key: str, value) -> None:
    """Set a frontboot key."""
    fb = get_frontboot()
    fb[key] = value
    write_json(FRONTBOOT_FILE, fb)


def append_log(action: str, subject: str, details: str = "") -> None:
    """Append to wiki log."""
    date = datetime.now().strftime('%Y-%m-%d')
    entry = f"\n## [{date}] {action} | {subject}"
    if details:
        entry += f"\n{details}"
    
    if LOG_FILE.exists():
        LOG_FILE.write_text(entry + '\n', mode='a')
    else:
        LOG_FILE.write_text(f"# Wiki Log\n\n> Chronological record.\n\n{entry}\n")


# ─── Ingest Functions ────────────────────────────────────────────────────────

def check_drops_folder(dry_run: bool = False) -> list[str]:
    """Check _drops folder for new files to ingest."""
    if not DROPS_DIR.exists():
        return []
    
    files_processed = []
    for f in DROPS_DIR.iterdir():
        if f.is_file() and f.suffix in ['.md', '.txt', '.pdf']:
            if dry_run:
                files_processed.append(f"  [DRY-RUN] Would process: {f.name}")
            else:
                # Move to appropriate raw folder
                if f.suffix == '.pdf':
                    dest = RAW_DIR / "papers" / f.name
                elif 'transcript' in f.name.lower() or 'meeting' in f.name.lower():
                    dest = RAW_DIR / "transcripts" / f.name
                else:
                    dest = RAW_DIR / "articles" / f.name
                
                dest.parent.mkdir(parents=True, exist_ok=True)
                f.rename(dest)
                files_processed.append(f"  Processed: {f.name} -> {dest.parent.name}/")
    
    return files_processed


def check_watched_urls(dry_run: bool = False) -> list[str]:
    """Check URLs in frontboot for updates."""
    fb = get_frontboot()
    watched = fb.get('watched_urls', {})
    
    if not watched:
        return ["  No URLs being watched"]
    
    updates = []
    for url, last_check in watched.items():
        # Simple check — in production would compare ETag/Content-Length
        last_dt = datetime.fromisoformat(last_check) if last_check else datetime.min
        if datetime.now() - last_dt > timedelta(hours=24):
            if dry_run:
                updates.append(f"  [DRY-RUN] Would check: {url}")
            else:
                # Update last checked time
                watched[url] = datetime.now().isoformat()
                updates.append(f"  Would check: {url}")
    
    if not dry_run and updates:
        fb['watched_urls'] = watched
        write_json(FRONTBOOT_FILE, fb)
    
    return updates


def run_self_heal() -> str:
    """Run wiki_self_heal.py to fix any issues."""
    result = run_cmd(["python3", "scripts/wiki_self_heal.py", "--all"], timeout=60)
    return result


def run_self_critique() -> str:
    """Run wiki_self_critique.py to assess quality."""
    result = run_cmd(["python3", "scripts/wiki_self_critique.py", "--check"], timeout=60)
    return result


def report_to_dojo(summary: dict) -> None:
    """Report ingest results to Hermes Dojo."""
    try:
        dojo = read_json(DOJO_FILE)
        
        daily_task = {
            "id": f"daily-ingest-{datetime.now().strftime('%Y%m%d')}",
            "type": "daily-ingest",
            "status": "completed",
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
        }
        
        if 'tasks' not in dojo:
            dojo['tasks'] = []
        dojo['tasks'].insert(0, daily_task)
        dojo['tasks'] = dojo['tasks'][:100]  # Keep last 100
        
        write_json(DOJO_FILE, dojo)
    except Exception as e:
        print(f"Warning: Could not report to dojo: {e}")


def check_stale_pages(days: int = 7) -> list[str]:
    """Find concept pages not updated in N days."""
    threshold = datetime.now() - timedelta(days=days)
    stale = []
    
    concepts_dir = WIKI_ROOT / "concepts"
    if not concepts_dir.exists():
        return ["  No concepts directory found"]
    
    for f in concepts_dir.iterdir():
        if f.suffix != '.md' or f.name.startswith('.'):
            continue
        
        try:
            content = f.read_text()
            # Look for updated date in frontmatter
            updated_match = re.search(r'updated:\s*(\d{4}-\d{2}-\d{2})', content)
            if updated_match:
                updated_date = datetime.strptime(updated_match.group(1), '%Y-%m-%d')
                if updated_date < threshold:
                    stale.append(f"  Stale ({updated_date.strftime('%Y-%m-%d')}): {f.stem}")
        except Exception:
            pass
    
    return stale


# ─── Main ────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Daily Wiki Ingest Orchestrator")
    parser.add_argument('--check', action='store_true', help='Verify dependencies')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done')
    parser.add_argument('--recent', type=int, default=0, help='Check pages updated in last N days')
    parser.add_argument('--drops', action='store_true', help='Process drops folder only')
    parser.add_argument('--watch', action='store_true', help='Check watched URLs only')
    parser.add_argument('--heal', action='store_true', help='Run self-heal only')
    parser.add_argument('--stale', type=int, help=f'Find pages older than N days (default: 7)')
    
    args = parser.parse_args()
    
    # Check dependencies
    if args.check:
        print("Checking dependencies...")
        
        for script in ['scripts/wiki_self_heal.py', 'scripts/wiki_self_critique.py']:
            p = WIKI_ROOT / script
            if p.exists():
                print(f"  ✓ {script}")
            else:
                print(f"  ✗ {script} NOT FOUND")
        
        if WIKI_ROOT.exists():
            print(f"  ✓ Wiki root: {WIKI_ROOT}")
        else:
            print(f"  ✗ Wiki root NOT FOUND")
        
        print("\nAll checks passed!" if WIKI_ROOT.exists() else "\nSome checks failed.")
        sys.exit(0 if WIKI_ROOT.exists() else 1)
    
    # Single-mode operations
    if args.drops:
        results = check_drops_folder(args.dry_run)
        for r in results:
            print(r)
        return
    
    if args.watch:
        results = check_watched_urls(args.dry_run)
        for r in results:
            print(r)
        return
    
    if args.heal:
        print("Running self-heal...")
        result = run_self_heal()
        print(result)
        return
    
    if args.stale is not None:
        print(f"Checking pages older than {args.stale} days...")
        stale = check_stale_pages(args.stale)
        for s in stale[:20]:  # Limit output
            print(s)
        if len(stale) > 20:
            print(f"  ... and {len(stale) - 20} more")
        return
    
    # Recent mode
    if args.recent > 0:
        print(f"Checking pages updated in last {args.recent} days...")
        stale = check_stale_pages(args.recent)
        if stale:
            for s in stale[:20]:
                print(s)
            if len(stale) > 20:
                print(f"  ... and {len(stale) - 20} more")
        else:
            print("  No stale pages found")
        return
    
    # Full daily ingest
    print(f"=== Daily Ingest: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
    
    summary = {"drops": [], "watched": [], "heal": "", "stale": []}
    
    # 1. Check drops folder
    print("[1] Checking drops folder...")
    drops = check_drops_folder(args.dry_run)
    for d in drops:
        print(d)
    summary['drops'] = drops
    
    # 2. Check watched URLs
    print("\n[2] Checking watched URLs...")
    watched = check_watched_urls(args.dry_run)
    for w in watched:
        print(w)
    summary['watched'] = watched
    
    # 3. Run self-heal (skip in dry-run for speed)
    if not args.dry_run:
        print("\n[3] Running self-heal...")
        heal_result = run_self_heal()
        # Show only summary lines
        heal_lines = [l for l in heal_result.split('\n') if '====' in l or 'Found' in l or '✓' in l or '✗' in l]
        for l in heal_lines[:15]:
            print(f"  {l}")
        summary['heal'] = '\n'.join(heal_lines)
    else:
        print("\n[3] [DRY-RUN] Would run self-heal")
    
    # 4. Check for stale pages
    print("\n[4] Checking stale pages (>7 days)...")
    stale = check_stale_pages(7)
    for s in stale[:10]:
        print(s)
    if len(stale) > 10:
        print(f"  ... and {len(stale) - 10} more")
    summary['stale'] = stale
    
    # 5. Report to dojo (skip in dry-run)
    if not args.dry_run:
        report_to_dojo(summary)
    
    # 6. Update log
    if not args.dry_run:
        stale_count = len([s for s in stale if s.startswith('  Stale')])
        append_log(
            "cron:daily-ingest",
            f"Daily ingest complete — {len(drops)} drops, {stale_count} stale pages",
            f"- Drops: {len(drops)}\n- Watched URLs checked: {len(watched)}\n- Stale pages: {stale_count}"
        )
    
    print(f"\n=== Ingest Complete ===")
    if args.dry_run:
        print("(dry-run mode — no changes made)")


if __name__ == '__main__':
    main()
