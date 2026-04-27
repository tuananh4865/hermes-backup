#!/opt/homebrew/bin/python3.14
"""
watchdog_processor.py — Event-Driven Wiki Self-Healing

Watches the wiki for file changes and triggers appropriate processing:
- New files in raw/ → trigger ingest workflow
- Modified wiki pages → verify frontmatter and links
- Deleted files → update index and log

Uses file modification times instead of OS-level watching (works cross-platform).

Usage:
    python3 watchdog_processor.py              # Run once (batch mode)
    python3 watchdog_processor.py --watch       # Continuous watching (requires watchdog lib)
    python3 watchdog_processor.py --daemon      # Run as background daemon
    python3 watchdog_processor.py --status       # Show watchdog status
    python3 watchdog_processor.py --check       # Verify dependencies

Cron setup (alternative to daemon):
    */15 * * * * cd ~/wiki && python3 scripts/watchdog_processor.py --batch >> logs/watchdog.log 2>&1

Note: For true event-driven watching, install watchdog:
    pip install watchdog
Then run with --watch or --daemon.
"""

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Optional

# ─── Configuration ────────────────────────────────────────────────────────────

WIKI_ROOT = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_DIR = WIKI_ROOT / "raw"
ENTITIES_DIR = WIKI_ROOT / "entities"
CONCEPTS_DIR = WIKI_ROOT / "concepts"
INDEX_FILE = WIKI_ROOT / "index.md"
LOG_FILE = WIKI_ROOT / "log.md"
STATE_FILE = WIKI_ROOT / "_meta" / "watchdog_state.json"

FRONTMATTER_REQUIRED = ['title', 'created', 'updated', 'type', 'tags']

# ─── State Management ─────────────────────────────────────────────────────────

def get_state() -> dict:
    """Load watchdog state."""
    try:
        if STATE_FILE.exists():
            return json.loads(STATE_FILE.read_text())
    except Exception:
        pass
    return {"file_hashes": {}, "last_run": None, "processed_today": []}


def save_state(state: dict) -> None:
    """Save watchdog state."""
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))


def file_hash(path: Path) -> str:
    """Get MD5 hash of file."""
    try:
        return hashlib.md5(path.read_bytes()).hexdigest()[:12]
    except Exception:
        return ""


# ─── Processing Functions ────────────────────────────────────────────────────

def process_new_raw_file(filepath: Path) -> dict:
    """Process a new file found in raw/ directory."""
    result = {
        "file": str(filepath.relative_to(WIKI_ROOT)),
        "action": "none",
        "changes": [],
    }
    
    # Determine subdirectory type
    subdir = filepath.parent.name  # 'articles', 'papers', 'transcripts'
    
    # Check if it's a new concept
    slug = filepath.stem
    
    # Look for corresponding concept page
    concept_file = CONCEPTS_DIR / f"{slug}.md"
    
    if not concept_file.exists():
        # New concept needed
        result["action"] = "create_concept"
        result["changes"].append(f"Would create concept: {slug}")
        
        # Auto-create concept page
        title = slug.replace('-', ' ').replace('_', ' ').title()
        frontmatter = f"""---
title: {title}
created: {datetime.now().strftime('%Y-%m-%d')}
updated: {datetime.now().strftime('%Y-%m-%d')}
type: concept
tags: [{subdir[:-1] if subdir.endswith('s') else subdir}, auto-generated]
sources: [{filepath.relative_to(WIKI_ROOT)}]
---

# {title}

*Auto-generated from [[{filepath.relative_to(WIKI_ROOT)}]]*

> This page was auto-created by [[watchdog-processor]] from a raw source file.
> Replace the TODOs below with synthesized, well-written content based on the source.
> Do not copy-paste from the source. Synthesize and rephrase in your own words.

## Summary

[TODO: Write a 2-3 sentence summary of what this concept is about.
 Synthesize from the source material — do not just copy the first paragraph.
 Focus on what makes this concept interesting and worth knowing.]

## Key Points

- [TODO: Point 1 — main insight from the source. What is the most important thing to know?]
- [TODO: Point 2 — another important insight. Why does this matter?]
- [TODO: Point 3 — a third relevant point. How does this connect to other knowledge?]
- [TODO: Point 4 — add more as needed for comprehensive coverage]

## Detailed Breakdown

### Background and Context

[TODO: Explain the background, history, or context this concept exists in.
 Why does this concept matter? What problem does it solve?
 Provide enough context that someone unfamiliar with the topic can follow along.
 This section should help ground the reader before diving into specifics.]

### How It Works

[TODO: Describe the mechanism or process in detail.
 Use concrete, specific language — not generic descriptions.
 Break down complex processes into clear, sequential steps.
 Anticipate questions a curious reader might have and address them here.]

### Practical Considerations

[TODO: Note important practical aspects of working with this concept.
 Consider: when is this approach most effective? When should it be avoided?
 What are common pitfalls and how can they be avoided?
 Include real-world trade-offs that practitioners face.]

## Examples

[TODO: Provide at least one concrete, real example.
 Show how this concept applies in a realistic scenario.
 Include code snippets, diagrams, or concrete details — not just abstract descriptions.
 Examples are most valuable when they come from real experience.]

### Example 1

[TODO: Describe a specific, real scenario where this concept was applied.
 Include enough detail that someone could apply it similarly in their own work.]

```python
# Example implementation or usage
# TODO: Replace with a real example relevant to this concept
def example():
    pass
```

### Example 2

[TODO: A second example illustrating a different aspect of the concept.
 Real examples from your own experience are most valuable here.]

## Related Concepts

Understanding this concept connects to several other areas:

- [[self-healing-wiki]] — the broader self-healing wiki ecosystem
- [[watchdog-processor]] — the system that generated this page
- [[learning]] — approaches to synthesizing and retaining new knowledge

[TODO: Replace the wikilinks above with links to actual related concepts.
 Use [[double brackets]] to link to relevant wiki pages.
 At least 3 wikilinks are required for quality scoring.]

## Sources

- [[{filepath.relative_to(WIKI_ROOT)}]] (primary source)
- [TODO: Add other relevant sources if applicable — external links, papers, documentation]

## Personal Notes

> Personal observations, questions, and insights about this concept.
> These notes are private to your wiki and help track your understanding over time.

[TODO: What did you learn from the source? What surprised you?
 What questions remain unanswered? What would you investigate next?]

---

*Auto-generated by [[watchdog-processor]]: {datetime.now().strftime('%Y-%m-%d')}*
"""
        concept_file.parent.mkdir(parents=True, exist_ok=True)
        concept_file.write_text(frontmatter)
        result["changes"].append(f"Created: {concept_file.relative_to(WIKI_ROOT)}")
    
    return result


def verify_page(filepath: Path) -> dict:
    """Verify a wiki page is properly formatted."""
    result = {
        "file": str(filepath.relative_to(WIKI_ROOT)),
        "issues": [],
        "fixed": [],
    }
    
    try:
        content = filepath.read_text()
        
        # Check frontmatter
        if not content.startswith('---'):
            result["issues"].append("Missing frontmatter")
        else:
            end = content.find('---', 3)
            if end <= 0:
                result["issues"].append("Malformed frontmatter")
            else:
                fm_text = content[3:end].strip()
                fm = {}
                for line in fm_text.split('\n'):
                    if ':' in line:
                        key = line.split(':', 1)[0].strip()
                        fm[key] = True
                
                for required in FRONTMATTER_REQUIRED:
                    if required not in fm:
                        result["issues"].append(f"Missing frontmatter field: {required}")
        
        # Check for wikilinks
        wikilinks = re.findall(r'\[\[([^\]]+)\]\]', content)
        if len(wikilinks) < 2:
            result["issues"].append(f"Few wikilinks ({len(wikilinks)}, minimum 2)")
        
        # Check for orphaned wikilinks (links to non-existent pages)
        for link in wikilinks:
            link_slug = link.lower().replace(' ', '-')
            target_exists = (
                (CONCEPTS_DIR / f"{link_slug}.md").exists() or
                (ENTITIES_DIR / f"{link_slug}.md").exists()
            )
            if not target_exists:
                result["issues"].append(f"Broken wikilink: [[{link}]]")
        
        # Check file size (flag very large pages)
        if len(content) > 50000:
            result["issues"].append(f"Large file ({len(content)} chars) — consider splitting")
        
    except Exception as e:
        result["issues"].append(f"Error reading file: {e}")
    
    return result


def scan_directory(dirpath: Path, state: dict) -> list[dict]:
    """Scan a directory for changes."""
    results = []
    file_hashes = state.get("file_hashes", {})
    
    if not dirpath.exists():
        return results
    
    for filepath in dirpath.rglob('*'):
        if not filepath.is_file() or filepath.suffix not in ['.md', '.txt']:
            continue
        
        rel_path = str(filepath.relative_to(WIKI_ROOT))
        
        # Skip meta and archive directories
        if any(x in rel_path for x in ['_meta', '_archive', '_drops', '.git']):
            continue
        
        current_hash = file_hash(filepath)
        old_hash = file_hashes.get(rel_path, "")
        
        if current_hash != old_hash:
            # Something changed
            if old_hash == "":
                # New file
                if 'raw/' in rel_path:
                    result = process_new_raw_file(filepath)
                else:
                    result = {"file": rel_path, "action": "new", "changes": [f"New file detected"]}
                    verify_result = verify_page(filepath)
                    if verify_result["issues"]:
                        result["changes"].extend(verify_result["issues"])
                results.append(result)
            else:
                # Modified file
                verify_result = verify_page(filepath)
                if verify_result["issues"]:
                    results.append({
                        "file": rel_path,
                        "action": "modified",
                        "changes": verify_result["issues"]
                    })
            
            # Update hash
            file_hashes[rel_path] = current_hash
    
    return results


def update_index_from_filesystem() -> dict:
    """Rebuild index.md from actual files."""
    if not INDEX_FILE.exists():
        return {"action": "none"}
    
    # Read current index
    current = INDEX_FILE.read_text() if INDEX_FILE.exists() else ""
    
    # Scan for all wiki pages
    pages = {"entities": [], "concepts": [], "comparisons": [], "queries": []}
    
    for section, dirpath in [
        ("entities", ENTITIES_DIR),
        ("concepts", CONCEPTS_DIR),
        ("comparisons", WIKI_ROOT / "comparisons"),
        ("queries", WIKI_ROOT / "queries"),
    ]:
        if not dirpath.exists():
            continue
        
        for f in dirpath.iterdir():
            if f.suffix == '.md' and not f.name.startswith('.'):
                # Try to extract title from frontmatter
                title = f.stem.replace('-', ' ').replace('_', ' ').title()
                try:
                    content = f.read_text()
                    tm = re.search(r'^title:\s*(.+)$', content, re.MULTILINE)
                    if tm:
                        title = tm.group(1).strip().strip('"').strip("'")
                except Exception:
                    pass
                
                pages[section].append((f.stem, title))
    
    return {"action": "scanned", "pages": pages}


def run_batch_scan() -> list[dict]:
    """Run a batch scan of the entire wiki."""
    state = get_state()
    all_results = []
    
    # Scan raw directory
    if RAW_DIR.exists():
        for subdir in RAW_DIR.iterdir():
            if subdir.is_dir():
                results = scan_directory(subdir, state)
                all_results.extend(results)
    
    # Scan wiki pages
    for dirpath in [ENTITIES_DIR, CONCEPTS_DIR, WIKI_ROOT / "comparisons", WIKI_ROOT / "queries"]:
        if dirpath.exists():
            results = scan_directory(dirpath, state)
            all_results.extend(results)
    
    # Update state
    state["last_run"] = datetime.now().isoformat()
    save_state(state)
    
    return all_results


def append_log(action: str, subject: str, details: str = "") -> None:
    """Append to wiki log."""
    if not LOG_FILE.exists():
        LOG_FILE.write_text("# Wiki Log\n\n> Chronological record.\n\n")
    
    date = datetime.now().strftime('%Y-%m-%d')
    entry = f"\n## [{date}] {action} | {subject}"
    if details:
        entry += f"\n{details}"
    
    LOG_FILE.write_text(entry + '\n', mode='a')


# ─── Daemon Mode ─────────────────────────────────────────────────────────────

def run_daemon(interval: int = 60):
    """Run as a continuous daemon."""
    print(f"Starting watchdog daemon (interval: {interval}s)")
    print(f"Press Ctrl+C to stop")
    
    try:
        while True:
            results = run_batch_scan()
            
            if results:
                print(f"\n[{datetime.now().strftime('%H:%M:%S')}] Changes detected:")
                for r in results[:10]:
                    print(f"  {r.get('file', 'unknown')}: {r.get('action', 'unknown')}")
                    for c in r.get('changes', [])[:5]:
                        print(f"    - {c}")
                
                # Log to wiki
                changes_summary = "; ".join([r.get('file', '') for r in results[:5]])
                if len(results) > 5:
                    changes_summary += f" (+{len(results) - 5} more)"
                append_log("watchdog", "File changes detected", changes_summary)
            
            time.sleep(interval)
    
    except KeyboardInterrupt:
        print("\nDaemon stopped")


# ─── CLI Interface ───────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Wiki Watchdog — Event-Driven Self-Healing")
    parser.add_argument('--watch', action='store_true', help='Continuous watching mode')
    parser.add_argument('--daemon', action='store_true', help='Run as background daemon')
    parser.add_argument('--batch', action='store_true', help='Batch scan mode (for cron)')
    parser.add_argument('--status', action='store_true', help='Show watchdog status')
    parser.add_argument('--check', action='store_true', help='Verify dependencies')
    parser.add_argument('--interval', type=int, default=60, help='Watch interval in seconds (default: 60)')
    
    args = parser.parse_args()
    
    # Check mode
    if args.check:
        print("Checking watchdog dependencies...")
        
        # Check Python version
        print(f"  Python: {sys.version_info.major}.{sys.version_info.minor} {'✓' if sys.version_info >= (3, 9) else '✗'}")
        
        # Check wiki
        if WIKI_ROOT.exists():
            print(f"  Wiki root: {WIKI_ROOT} ✓")
        else:
            print(f"  Wiki root: {WIKI_ROOT} ✗ NOT FOUND")
            sys.exit(1)
        
        # Check watchdog module
        try:
            import watchdog
            print(f"  watchdog module: ✓")
            has_watchdog = True
        except ImportError:
            print(f"  watchdog module: ✗ (install with: pip install watchdog)")
            print(f"    -> Will use polling mode instead")
            has_watchdog = False
        
        # Check scripts
        for script in ['wiki_self_heal.py', 'wiki_self_critique.py']:
            p = WIKI_ROOT / "scripts" / script
            print(f"  {script}: {'✓' if p.exists() else '✗'}")
        
        print("\nDependencies OK")
        sys.exit(0)
    
    # Status mode
    if args.status:
        state = get_state()
        print("=== Watchdog Status ===")
        print(f"Last run: {state.get('last_run', 'never')}")
        print(f"Tracked files: {len(state.get('file_hashes', {}))}")
        
        if STATE_FILE.exists():
            age = datetime.now() - datetime.fromtimestamp(STATE_FILE.stat().st_mtime)
            print(f"State file age: {age.total_seconds() / 3600:.1f} hours")
        
        sys.exit(0)
    
    # Daemon mode
    if args.daemon or args.watch:
        if not has_watchdog:
            print("watchdog module not installed — using polling mode")
            run_daemon(interval=args.interval)
        else:
            # Use proper watchdog
            from watchdog.observers import Observer
            from watchdog.events import FileSystemEventHandler
            
            class WikiHandler(FileSystemEventHandler):
                def __init__(self):
                    self.pending = []
                
                def on_any_event(self, event):
                    if not event.is_directory and event.src_path.endswith('.md'):
                        self.pending.append(event.src_path)
            
            handler = WikiHandler()
            observer = Observer()
            
            for path in [str(WIKI_ROOT)]:
                if RAW_DIR.exists():
                    observer.schedule(handler, str(RAW_DIR), recursive=True)
                observer.schedule(handler, str(CONCEPTS_DIR), recursive=True)
                observer.schedule(handler, str(ENTITIES_DIR), recursive=True)
            
            observer.start()
            print(f"Watching wiki at {WIKI_ROOT}")
            print("Press Ctrl+C to stop")
            
            try:
                while True:
                    time.sleep(args.interval)
                    if handler.pending:
                        print(f"\n[{datetime.now().strftime('%H:%M:%S')}] {len(handler.pending)} file(s) changed")
                        handler.pending.clear()
            except KeyboardInterrupt:
                observer.stop()
                print("\nDaemon stopped")
            
            observer.join()
        
        sys.exit(0)
    
    # Batch mode (default)
    print(f"=== Wiki Watchdog: {datetime.now().strftime('%Y-%m-%d %H:%M')} ===\n")
    
    results = run_batch_scan()
    
    if results:
        print(f"Found {len(results)} changes:\n")
        for r in results:
            print(f"  {r.get('file', 'unknown')}")
            print(f"    Action: {r.get('action', 'unknown')}")
            if r.get('changes'):
                for c in r.get('changes', []):
                    print(f"    - {c}")
            print()
        
        # Log summary
        append_log(
            "watchdog:batch",
            f"Batch scan: {len(results)} changes",
            "\n".join([f"- {r.get('file')}: {r.get('action')}" for r in results[:20]])
        )
    else:
        print("No changes detected")
    
    # Show state info
    state = get_state()
    print(f"\nTracked files: {len(state.get('file_hashes', {}))}")
    print(f"Last scan: {state.get('last_run', 'never')}")


if __name__ == '__main__':
    has_watchdog = False
    try:
        import watchdog
        has_watchdog = True
    except ImportError:
        pass
    
    main()
