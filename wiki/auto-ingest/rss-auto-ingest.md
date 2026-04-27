---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 RSS (extracted)
  - 🔗 email (extracted)
  - 🔗 automation (extracted)
relationship_count: 3
---

# RSS Auto-Ingest Setup

## Overview

```
RSS Feed → iOS Shortcuts/IFTTT → Working Copy folder → Git sync → Auto-commit
```

## Option A: iOS Shortcuts + Fiery Feeds

### What You Need
- **Fiery Feeds** (RSS reader app, ~$5)
- **Working Copy** (Git client for iOS, ~$10)
- iOS Shortcuts (free, built-in)

### Step 1: Subscribe to RSS Feeds in Fiery Feeds
1. Download Fiery Feeds from App Store
2. Add your favorite blogs/newsletters:
   - Add URL + click "Subscribe"
   - Examples:
     - https://karpathy.ai/feed.xml
     - https://news.ycombinator.com/rss
     - Any blog's /feed or /rss.xml

### Step 2: Create iOS Shortcut
1. Open Shortcuts app
2. Create new shortcut: "Save RSS to Wiki"

```
Fiery Feeds → Get Latest Items → For Each Item:
    → Get URL
    → Get Title
    → Save to file: ~/wiki/raw/rss/{date}-{title}.md
```

### Step 3: Connect Fiery Feeds to Shortcuts
1. In Fiery Feeds → Settings → Actions
2. Enable "Run Shortcut" action
3. Configure to run "Save RSS to Wiki" on new items

### Step 4: Auto-Sync with Working Copy
1. In Working Copy → Repo Settings
2. Enable "Auto-pull" and "Auto-commit"
3. Set schedule: "Every hour"

---

## Option B: IFTTT (No Coding)

### What You Need
- IFTTT account (free)
- RSS feed subscription

### Applet: New RSS Item → Save to Dropbox
1. Create IFTTT account
2. New Applet:
   - **If**: RSS Feed item new
   - **Then**: Add to Dropbox folder `/Wiki/Raw/`

### Then: Dropbox → Working Copy
1. In Working Copy, add Dropbox as sync source
2. Files auto-appear

---

## Option C: Python Script (Mac Only)

### Prerequisites
- Python 3.8+
- `feedparser` library

### Setup

```bash
pip install feedparser requests

# Create scripts folder if not exists
mkdir -p ~/wiki/scripts
```

### Create Script

```python
#!/usr/bin/env python3
"""
rss_ingest.py - Auto-ingest RSS feeds to wiki
Run via: python rss_ingest.py
Or via cron: 0 * * * * /usr/bin/python3 ~/wiki/scripts/rss_ingest.py
"""

import feedparser
import os
import re
from datetime import datetime
from pathlib import Path

# Configuration
WIKI_PATH = Path.home() / "wiki"
RAW_PATH = WIKI_PATH / "raw" / "rss"
FEEDS = [
    "https://karpathy.ai/feed.xml",
    "https://news.ycombinator.com/rss",
    # Add more feeds here
]

def sanitize_filename(title):
    """Convert title to safe filename"""
    # Remove special characters
    safe = re.sub(r'[^\w\s-]', '', title)
    # Replace spaces with hyphens
    safe = re.sub(r'\s+', '-', safe)
    # Truncate to 100 chars
    return safe[:100]

def save_entry(entry):
    """Save single RSS entry to markdown file"""
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"{date}-{sanitize_filename(entry.title)}.md"
    filepath = RAW_PATH / filename
    
    # Skip if already exists
    if filepath.exists():
        return None
    
    content = f"""---
category: "[[RSS]]"
title: "{entry.title}"
source: {entry.link}
clipped: {date}
published: {entry.get('published', 'Unknown')}
tags: [rss]
---

# {entry.title}

Source: {entry.link}

{"=" * 50}

{entry.get('summary', entry.get('description', 'No content'))}
"""
    
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath

def main():
    """Main loop"""
    RAW_PATH.mkdir(parents=True, exist_ok=True)
    
    saved = []
    for feed_url in FEEDS:
        feed = feedparser.parse(feed_url)
        print(f"Processing: {feed_url} ({len(feed.entries)} items)")
        
        for entry in feed.entries[:5]:  # Last 5 items
            result = save_entry(entry)
            if result:
                saved.append(result)
                print(f"  Saved: {result.name}")
    
    if saved:
        print(f"\n✓ Saved {len(saved)} new items")
        # Auto-commit
        os.system(f'cd {WIKI_PATH} && git add raw/rss/')
        os.system(f'cd {WIKI_PATH} && git commit -m "RSS ingest: {len(saved)} new items"')
        os.system(f'cd {WIKI_PATH} && git push')
    else:
        print("\nNo new items")

if __name__ == "__main__":
    main()
```

### Cron Setup

```bash
# Add to crontab
crontab -e

# Run every hour
0 * * * * /usr/bin/python3 ~/wiki/scripts/rss_ingest.py >> ~/wiki/logs/rss_ingest.log 2>&1
```

---

## Recommended RSS Feeds for AI/ML

```python
FEEDS = [
    # AI/ML Research
    "https://karpathy.ai/feed.xml",           # Karpathy
    "https://lilianweng.github.io/lil-log/feed.xml",  # Lilian Weng
    "https://层次 feeds.com/feed/",           # Add your favorites
    
    # News
    "https://news.ycombinator.com/rss",       # Hacker News
    "https://www.theverge.com/rss/index.xml", # Tech news
    
    # Blogs
    "https://simonwillison.net/feed/",        # Simon Willison
    "https://blog.tensorflow.org/feed.xml",   # TensorFlow blog
]
```

---

## Testing

```bash
# Test the script manually
cd ~/wiki
python3 scripts/rss_ingest.py

# Check output
cat logs/rss_ingest.log

# Check saved files
ls -la raw/rss/
```

## Related Concepts

- [[email]] — Email auto-ingest for alternative content capture
- [[automation]] — General automation patterns for wiki maintenance
- [[obsidian-web-clipper]] — Browser bookmarklet for clipping web pages directly to Obsidian
