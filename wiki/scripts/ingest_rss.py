#!/opt/homebrew/bin/python3.14
"""
RSS Ingest — Parse RSS/Atom feeds into wiki format

Usage:
    python ingest_rss.py --add "https://example.com/feed.xml"
    python ingest_rss.py --list
    python ingest_rss.py --fetch-all
    python ingest_rss.py --fetch <feed-name>
"""

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List
import urllib.request
import urllib.error
import json
import hashlib

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_RSS = WIKI_PATH / "raw" / "rss"
FEEDS_FILE = WIKI_PATH / "scripts" / ".rss_feeds.json"
PROCESSED_FILE = WIKI_PATH / "scripts" / ".rss_processed.json"

# ═══════════════════════════════════════════════════════════════

def load_feeds() -> Dict[str, str]:
    """Load saved feeds"""
    if FEEDS_FILE.exists():
        return json.loads(FEEDS_FILE.read_text())
    return {}

def save_feeds(feeds: Dict[str, str]):
    """Save feeds list"""
    FEEDS_FILE.parent.mkdir(parents=True, exist_ok=True)
    FEEDS_FILE.write_text(json.dumps(feeds, indent=2))

def load_processed() -> Dict[str, List[str]]:
    """Load processed items per feed"""
    if PROCESSED_FILE.exists():
        return json.loads(PROCESSED_FILE.read_text())
    return {}

def save_processed(processed: Dict[str, List[str]]):
    """Save processed items"""
    PROCESSED_FILE.write_text(json.dumps(processed, indent=2))

def fetch_feed(url: str) -> Optional[str]:
    """Fetch RSS/Atom feed"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=15) as response:
            return response.read().decode('utf-8', errors='ignore')
    except urllib.error.URLError as e:
        print(f"Error fetching feed {url}: {e}", file=sys.stderr)
        return None

def parse_feed_name(url: str) -> str:
    """Create feed name from URL"""
    # Extract domain and path
    match = re.search(r'://([^/]+)', url)
    domain = match.group(1) if match else 'unknown'
    
    # Remove www.
    domain = re.sub(r'^www\.', '', domain)
    
    # Get first path segment if exists
    path_match = re.search(r'/([^/]+)', url.split(domain)[1] if domain in url else url)
    path = path_match.group(1) if path_match else 'feed'
    
    return f"{domain}-{path}"

def parse_feed(xml_content: str) -> Dict:
    """Parse RSS or Atom feed"""
    try:
        # Try RSS first
        if '<rss' in xml_content.lower() or '<channel>' in xml_content.lower():
            return parse_rss(xml_content)
        
        # Try Atom
        if '<feed' in xml_content.lower() or '<entry>' in xml_content.lower():
            return parse_atom(xml_content)
        
        # Try to detect
        return parse_rss(xml_content)
    except Exception as e:
        print(f"Error parsing feed: {e}", file=sys.stderr)
        return None

def parse_rss(xml_content: str) -> Dict:
    """Parse RSS 2.0 feed"""
    try:
        # Register namespaces
        ET.register_namespace('', 'http://www.w3.org/2005/Atom')
        
        root = ET.fromstring(xml_content)
        channel = root.find('channel')
        
        if channel is None:
            return None
        
        feed_data = {
            'title': get_element_text(channel, 'title'),
            'description': get_element_text(channel, 'description'),
            'link': get_element_text(channel, 'link'),
            'items': []
        }
        
        for item in channel.findall('item'):
            entry = {
                'title': get_element_text(item, 'title'),
                'link': get_element_text(item, 'link'),
                'description': get_element_text(item, 'description'),
                'pub_date': get_element_text(item, 'pubDate'),
                'guid': get_element_text(item, 'guid') or get_element_text(item, 'link'),
            }
            feed_data['items'].append(entry)
        
        return feed_data
    except Exception as e:
        print(f"RSS parsing error: {e}", file=sys.stderr)
        return None

def parse_atom(xml_content: str) -> Dict:
    """Parse Atom feed"""
    try:
        root = ET.fromstring(xml_content)
        
        # Determine namespace
        ns = ''
        if 'http://www.w3.org/2005/Atom' in xml_content:
            ns = '{http://www.w3.org/2005/Atom}'
        
        feed_data = {
            'title': get_element_text(root, 'title', ns),
            'description': get_element_text(root, 'subtitle', ns),
            'link': None,
            'items': []
        }
        
        # Get link
        link = root.find(f'{ns}link')
        if link is not None:
            feed_data['link'] = link.get('href')
        
        for entry in root.findall(f'{ns}entry'):
            entry_data = {
                'title': get_element_text(entry, 'title', ns),
                'link': None,
                'description': get_element_text(entry, 'summary', ns) or get_element_text(entry, 'content', ns),
                'pub_date': get_element_text(entry, 'published', ns) or get_element_text(entry, 'updated', ns),
                'guid': None,
            }
            
            # Get link
            for link_el in entry.findall(f'{ns}link'):
                if link_el.get('rel') != 'alternate':
                    continue
                entry_data['link'] = link_el.get('href')
                break
            
            if not entry_data['link']:
                link_el = entry.find(f'{ns}link')
                if link_el is not None:
                    entry_data['link'] = link_el.get('href')
            
            # Get ID (guid)
            id_el = entry.find(f'{ns}id')
            if id_el is not None:
                entry_data['guid'] = id_el.text
            
            feed_data['items'].append(entry_data)
        
        return feed_data
    except Exception as e:
        print(f"Atom parsing error: {e}", file=sys.stderr)
        return None

def get_element_text(element, tag: str, ns: str = '') -> Optional[str]:
    """Get text from XML element safely"""
    if element is None:
        return None
    el = element.find(f'{ns}{tag}')
    if el is not None and el.text:
        return el.text.strip()
    return None

def slugify(text: str) -> str:
    """Create URL-safe slug"""
    if not text:
        return 'untitled'
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text[:60]

def get_item_hash(item: Dict) -> str:
    """Generate hash for item deduplication"""
    content = f"{item.get('guid', '')}{item.get('link', '')}{item.get('title', '')}"
    return hashlib.md5(content.encode()).hexdigest()[:12]

def save_feed_item(feed_name: str, item: Dict, feed_data: Dict) -> Optional[Path]:
    """Save a single feed item"""
    if not item.get('title'):
        return None
    
    # Create slug
    slug = slugify(item['title'])
    
    # Get date
    date = item.get('pub_date', '')
    if date:
        # Try to parse date
        try:
            # RFC 822 (RSS)
            from email.utils import parsedate
            dt = parsedate(date)
            if dt:
                date = datetime(*dt[:6]).strftime('%Y-%m-%d')
        except:
            date = date[:10] if len(date) >= 10 else date
    else:
        date = datetime.now().strftime('%Y-%m-%d')
    
    filename = f"{date}-{slug}.md"
    
    # Build content
    content_lines = [f"# {item['title']}\n"]
    
    if date:
        content_lines.append(f"**Published:** {date}\n")
    
    if item.get('link'):
        content_lines.append(f"**Link:** [{item['link']}]({item['link']})\n")
    
    if feed_data.get('title'):
        content_lines.append(f"**Source:** {feed_data['title']}\n")
    
    content_lines.append(f"\n{item.get('description', 'No description.')}\n")
    
    content = ''.join(content_lines)
    
    # Build frontmatter
    frontmatter = f"""---
title: "{item['title']}"
date: {date}
type: rss-item
tags: []
sources: [{item.get('link', '')}]
feed: {feed_name}
---

"""
    
    full_content = frontmatter + content
    
    # Save
    feed_dir = RAW_RSS / feed_name
    feed_dir.mkdir(parents=True, exist_ok=True)
    
    filepath = feed_dir / filename
    filepath.write_text(full_content, encoding='utf-8')
    
    return filepath

def fetch_feed_items(feed_name: str, url: str) -> int:
    """Fetch and save items from a single feed"""
    print(f"Fetching {feed_name}...")
    
    xml = fetch_feed(url)
    if not xml:
        return 0
    
    feed_data = parse_feed(xml)
    if not feed_data:
        print(f"  Failed to parse feed")
        return 0
    
    processed = load_processed()
    feed_processed = processed.get(feed_name, [])
    
    count = 0
    for item in feed_data.get('items', []):
        item_hash = get_item_hash(item)
        
        if item_hash in feed_processed:
            continue  # Already processed
        
        # Save item
        filepath = save_feed_item(feed_name, item, feed_data)
        if filepath:
            count += 1
            feed_processed.append(item_hash)
    
    # Update processed
    processed[feed_name] = feed_processed[-100:]  # Keep last 100
    save_processed(processed)
    
    return count

def main():
    parser = argparse.ArgumentParser(description='Ingest RSS/Atom feeds into wiki')
    parser.add_argument('--add', metavar='URL', help='Add a new RSS feed')
    parser.add_argument('--remove', metavar='NAME', help='Remove a feed')
    parser.add_argument('--list', action='store_true', help='List all feeds')
    parser.add_argument('--fetch', metavar='NAME', help='Fetch items from specific feed')
    parser.add_argument('--fetch-all', action='store_true', help='Fetch items from all feeds')
    args = parser.parse_args()
    
    feeds = load_feeds()
    
    if args.add:
        name = parse_feed_name(args.add)
        feeds[name] = args.add
        save_feeds(feeds)
        print(f"Added feed '{name}': {args.add}")
        return
    
    if args.remove:
        if args.remove in feeds:
            del feeds[args.remove]
            save_feeds(feeds)
            print(f"Removed feed '{args.remove}'")
        else:
            print(f"Feed '{args.remove}' not found")
        return
    
    if args.list:
        if not feeds:
            print("No feeds configured. Add one with --add URL")
            return
        
        print(f"Configured feeds ({len(feeds)}):")
        for name, url in feeds.items():
            print(f"  - {name}: {url}")
        
        # Show last fetch stats
        processed = load_processed()
        print(f"\nProcessed items:")
        for name in feeds:
            count = len(processed.get(name, []))
            print(f"  - {name}: {count} items")
        return
    
    if args.fetch:
        if args.fetch not in feeds:
            print(f"Feed '{args.fetch}' not found")
            sys.exit(1)
        
        count = fetch_feed_items(args.fetch, feeds[args.fetch])
        print(f"Saved {count} new items")
        return
    
    if args.fetch_all:
        if not feeds:
            print("No feeds configured")
            return
        
        total = 0
        for name, url in feeds.items():
            count = fetch_feed_items(name, url)
            if count > 0:
                print(f"  → {count} new items")
            total += count
        
        print(f"\nTotal: {total} new items saved")
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()
