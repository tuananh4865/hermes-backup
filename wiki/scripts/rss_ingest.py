#!/opt/homebrew/bin/python3.14
"""
RSS Auto-Ingest — Fetch RSS feeds and save to wiki raw/rss/

Usage:
    python rss_ingest.py              # Run once
    python rss_ingest.py --watch     # Watch mode (cron-friendly)
"""

import argparse
import os
import re
import sys
from datetime import datetime
from pathlib import Path

# Try to import feedparser, install if missing
try:
    import feedparser
except ImportError:
    print("Installing feedparser...")
    os.system(f"{sys.executable} -m pip install feedparser -q")
    import feedparser

# ═══════════════════════════════════════════════════════════════
# CONFIG — Edit these settings
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_PATH = WIKI_PATH / "raw" / "rss"

FEEDS = [
    "https://karpathy.ai/feed.xml",
    "https://news.ycombinator.com/rss",
    # Add more feeds here
]

MAX_ITEMS_PER_FEED = 5  # Only save last N items

# ═══════════════════════════════════════════════════════════════

def sanitize_filename(title: str) -> str:
    """Convert title to safe filename."""
    # Remove special characters, keep spaces and hyphens
    safe = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with hyphens
    safe = re.sub(r'\s+', '-', safe)
    # Lowercase
    safe = safe.lower()
    # Truncate to 80 chars
    return safe[:80]

def save_entry(entry, feed_title: str = "") -> Path | None:
    """Save single RSS entry to markdown file. Returns path if saved."""
    date = datetime.now().strftime("%Y-%m-%d")
    filename_base = f"{date}-{sanitize_filename(entry.title)}"
    filepath = RAW_PATH / f"{filename_base}.md"
    
    # Skip if already exists
    if filepath.exists():
        return None
    
    # Extract content
    title = entry.get('title', 'No Title')
    link = entry.get('link', '')
    published = entry.get('published', entry.get('updated', 'Unknown'))
    summary = entry.get('summary', entry.get('description', 'No content'))
    
    # Clean HTML from summary
    summary = re.sub(r'<[^>]+>', '', summary)
    summary = summary.strip()[:1000]
    
    content = f"""---
category: "[[RSS]]"
title: "{title}"
source: {link}
clipped: {date}
published: {published}
feed: "{feed_title}"
tags: [rss]
---

# {title}

Source: [{link}]({link})

{"=" * 50}

Published: {published}

{"=" * 50}

{summary}
"""
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath

def process_feed(feed_url: str) -> list[Path]:
    """Process single RSS feed."""
    feed = feedparser.parse(feed_url)
    feed_title = feed.feed.get('title', feed_url)
    
    saved = []
    for entry in feed.entries[:MAX_ITEMS_PER_FEED]:
        result = save_entry(entry, feed_title)
        if result:
            saved.append(result)
    
    return saved

def main():
    parser = argparse.ArgumentParser(description='RSS Auto-Ingest')
    parser.add_argument('--watch', action='store_true', help='Watch mode (for cron)')
    args = parser.parse_args()
    
    print(f"RSS Auto-Ingest — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Wiki: {WIKI_PATH}")
    print()
    
    # Ensure directory exists
    RAW_PATH.mkdir(parents=True, exist_ok=True)
    
    total_saved = 0
    for feed_url in FEEDS:
        print(f"Processing: {feed_url}")
        try:
            saved = process_feed(feed_url)
            if saved:
                for path in saved:
                    print(f"  + {path.name}")
                total_saved += len(saved)
            else:
                print(f"  No new items")
        except Exception as e:
            print(f"  ERROR: {e}")
    
    print()
    if total_saved > 0:
        print(f"Saved {total_saved} new items")
        # Auto-commit
        os.system(f'cd {WIKI_PATH} && git add raw/rss/ 2>/dev/null')
        os.system(f'cd {WIKI_PATH} && git commit -m "RSS ingest: {total_saved} new items" 2>/dev/null')
        os.system(f'cd {WIKI_PATH} && git push origin main 2>/dev/null')
    else:
        print("No new items")

if __name__ == "__main__":
    main()
