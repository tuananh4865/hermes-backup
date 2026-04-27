#!/opt/homebrew/bin/python3.14
"""
Wiki Lint Script — Dead Knowledge Detection

Performance: ~3350 files in <10s (was timing out before).
"""

import os
import re
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Optional
from concurrent.futures import ThreadPoolExecutor, as_completed

# CONFIG
WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
STALE_THRESHOLD_DAYS = 30
MAX_WORKERS = 8
SKIP_DIRS = {'_templates', '.obsidian', '__pycache__', 'raw', 'transcripts',
             'node_modules', 'finance-tracker', '.pytest_cache', '.git'}


def parse_frontmatter(content: str) -> Dict:
    frontmatter = {}
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            for line in content[3:end].strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    frontmatter[key.strip()] = value.strip().strip('"\'"')
    return frontmatter


def extract_wikilinks(content: str) -> List[str]:
    content_no_code = re.sub(r'```[\s\S]*?```', '', content)
    content_no_code = re.sub(r'`[^`]+`', '', content_no_code)
    content_no_code = re.sub(r'<!--[\s\S]*?-->', '', content_no_code)
    content_no_code = re.sub(r'\]\([^)]+\)', ']', content_no_code)
    return re.findall(r'\[\[([^\]]+)\]\]', content_no_code)


class WikiIndex:
    """Cached wiki file index — scans once, reuses across all checks"""
    
    def __init__(self, recent_days: Optional[int] = None):
        self.files: List[Path] = []
        self.contents: Dict[Path, str] = {}
        self.wikilinks: Dict[Path, List[str]] = {}
        self.page_names: Dict[str, Path] = {}
        self._build(recent_days)
    
    def _build(self, recent_days: Optional[int]):
        cutoff = None
        if recent_days:
            cutoff = datetime.now() - timedelta(days=recent_days)
        
        all_files = []
        for f in WIKI_PATH.rglob("*.md"):
            if any(skip in f.parts for skip in SKIP_DIRS):
                continue
            if cutoff:
                try:
                    if datetime.fromtimestamp(f.stat().st_mtime) < cutoff:
                        continue
                except:
                    pass
            all_files.append(f)
        
        self.files = all_files
        
        def load_file(path: Path) -> tuple:
            try:
                return path, path.read_text()
            except:
                return path, ""
        
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as ex:
            for path, content in ex.map(load_file, self.files):
                self.contents[path] = content
                self.wikilinks[path] = extract_wikilinks(content)
        
        for p in self.files:
            rel = str(p.relative_to(WIKI_PATH).with_suffix('')).lower().replace('\\', '/')
            self.page_names[rel] = p
            self.page_names[p.stem.lower()] = p
            hyphenated = re.sub(r'[\s\-_]+', '-', p.stem.lower())
            if hyphenated != p.stem.lower():
                self.page_names[hyphenated] = p
            self.page_names[re.sub(r'[\s\-_]+', '-', rel)] = p
    
    def is_raw(self, path: Path) -> bool:
        return str(path.relative_to(WIKI_PATH)).startswith('raw/')
    
    def get_backlinks(self, page_stem: str) -> List[Path]:
        pattern = re.compile(r'\[\[' + re.escape(page_stem) + r'\]\]', re.IGNORECASE)
        return [p for p, c in self.contents.items() if pattern.search(c)]


def detect_missing_frontmatter(index: WikiIndex) -> List[Dict]:
    missing = []
    for path, content in index.contents.items():
        if not content.startswith('---'):
            missing.append({
                'path': path,
                'name': path.stem,
                'relative_path': path.relative_to(WIKI_PATH)
            })
    return missing


def detect_stale_pages(index: WikiIndex) -> List[Dict]:
    stale = []
    threshold = datetime.now() - timedelta(days=STALE_THRESHOLD_DAYS)
    for path in index.files:
        try:
            file_date = datetime.fromtimestamp(path.stat().st_mtime)
            if file_date < threshold:
                stale.append({
                    'path': path,
                    'name': path.stem,
                    'last_modified': file_date.strftime('%Y-%m-%d'),
                    'days_ago': (datetime.now() - file_date).days
                })
        except:
            pass
    return stale


def detect_broken_links(index: WikiIndex) -> List[Dict]:
    broken = []
    for path in index.files:
        if index.is_raw(path):
            continue
        for link in index.wikilinks.get(path, []):
            raw_target = link.split('|')[0].strip()
            target = re.sub(r'[\s\-_]+', '-', raw_target).lower()
            if target not in index.page_names:
                broken.append({
                    'source': path.relative_to(WIKI_PATH),
                    'broken_link': link,
                    'type': 'missing_target'
                })
    return broken


def detect_orphan_pages(index: WikiIndex) -> List[Dict]:
    orphans = []
    for path in index.files:
        if index.is_raw(path):
            continue
        outgoing = index.wikilinks.get(path, [])
        incoming = index.get_backlinks(path.stem)
        if len(outgoing) == 0 and len(incoming) == 0:
            orphans.append({
                'path': path,
                'name': path.stem,
                'relative_path': path.relative_to(WIKI_PATH)
            })
    return orphans


def main():
    parser = argparse.ArgumentParser(description='Wiki Lint')
    parser.add_argument('--fast', action='store_true',
                        help='Skip slow checks (broken links, orphans)')
    parser.add_argument('--recent', type=int, metavar='N',
                        help='Only scan files modified in last N days')
    parser.add_argument('--stale-days', type=int, default=30, metavar='N')
    args = parser.parse_args()
    
    global STALE_THRESHOLD_DAYS
    STALE_THRESHOLD_DAYS = args.stale_days
    
    print(f"\n{'='*70}")
    print(f"WIKI LINT — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*70}")
    if args.recent:
        print(f"Mode: recent {args.recent} days only")
    elif args.fast:
        print(f"Mode: fast (no broken links, no orphans)")
    print()
    
    print("Scanning wiki... ", end='', flush=True)
    index = WikiIndex(recent_days=args.recent)
    print(f"{len(index.files)} files")
    
    # Missing frontmatter
    print(f"\n[1] MISSING FRONTMATTER")
    print("-" * 70)
    missing_fm = detect_missing_frontmatter(index)
    if missing_fm:
        for item in missing_fm[:20]:
            print(f"  • {item['relative_path']}")
        if len(missing_fm) > 20:
            print(f"  ... and {len(missing_fm) - 20} more")
    else:
        print("  None found ✓")
    
    # Stale
    print(f"\n[2] STALE PAGES (>{STALE_THRESHOLD_DAYS} days)")
    print("-" * 70)
    stale = detect_stale_pages(index)
    if stale:
        for item in sorted(stale, key=lambda x: x['days_ago'], reverse=True)[:30]:
            print(f"  {item['days_ago']:3d}d | {item['name']} | {item['last_modified']}")
        if len(stale) > 30:
            print(f"  ... and {len(stale) - 30} more")
    else:
        print("  None found ✓")
    
    # Broken links
    if args.fast:
        print(f"\n[3] BROKEN WIKILINKS (skipped in --fast mode)")
        print("-" * 70)
        print("  Skipped")
        broken = []
    else:
        print(f"\n[3] BROKEN WIKILINKS")
        print("-" * 70)
        broken = detect_broken_links(index)
        if broken:
            for item in broken[:20]:
                print(f"  • {item['source']} → [[{item['broken_link']}]]")
            if len(broken) > 20:
                print(f"  ... and {len(broken) - 20} more")
        else:
            print("  None found ✓")
    
    # Orphans
    if args.fast:
        print(f"\n[4] ORPHAN PAGES (skipped in --fast mode)")
        print("-" * 70)
        print("  Skipped")
        orphans = []
    else:
        print(f"\n[4] ORPHAN PAGES")
        print("-" * 70)
        orphans = detect_orphan_pages(index)
        if orphans:
            for item in orphans[:20]:
                print(f"  • {item['relative_path']}")
            if len(orphans) > 20:
                print(f"  ... and {len(orphans) - 20} more")
        else:
            print("  None found ✓")
    
    total = len(stale) + len(missing_fm) + len(broken) + len(orphans)
    print(f"\n{'='*70}")
    print(f"SUMMARY: {total} issues ({len(stale)} stale, {len(missing_fm)} no-fm, "
          f"{len(broken)} broken, {len(orphans)} orphans)")
    print(f"{'='*70}")
    
    if total == 0:
        print("  🎉 Wiki is clean!")
    else:
        print("  ⚠️  Run self-heal to fix issues")


if __name__ == "__main__":
    main()
