#!/opt/homebrew/bin/python3.14
"""
Discover new content from the web based on configured topics

Usage:
    python3 scripts/discover.py                    # Run discovery for all topics
    python3 scripts/discover.py --topic "AI Agents"  # Run for specific topic
    python3 scripts/discover.py --limit 5         # Limit results per topic
    python3 scripts/discover.py --dry-run          # Preview without saving
"""

import argparse
import json
import os
import re
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse

import requests

# Config
TAVILY_API_KEY = os.environ.get("TAVILY_API_KEY", "")
RAW_DIR = Path("raw")
DISCOVERIES_DIR = Path(".discoveries")
MAX_RESULTS_PER_TOPIC = 10
DELAY_BETWEEN_REQUESTS = 1.0  # Rate limiting


def load_topics_config() -> Dict:
    """Load topics from config file"""
    config_path = Path("config/topics.yaml")
    
    if not config_path.exists():
        # Fallback to inline config
        return {
            "topics": [
                {"name": "AI Agents", "keywords": ["agentic AI", "autonomous AI", "AI agent"]},
                {"name": "Local LLM", "keywords": ["LM Studio", "Ollama", "local AI"]},
                {"name": "Self-Healing", "keywords": ["self-healing AI", "autonomous repair"]},
            ]
        }
    
    import yaml
    with open(config_path) as f:
        return yaml.safe_load(f)


def get_existing_sources() -> set:
    """Get URLs already in raw/ directory"""
    existing = set()
    
    if not RAW_DIR.exists():
        return existing
    
    for ext in ["*.md", "*.txt", "*.html"]:
        for f in RAW_DIR.rglob(ext):
            # Check for URL in frontmatter or content
            content = f.read_text()
            urls = re.findall(r'https?://[^\s\)\"\'\>\]]+', content)
            existing.update(urls)
            
            # Also check filename for URLs
            if f.stem.startswith("http"):
                existing.add(f.stem)
    
    return existing


def save_discovery_state(topic: str, urls: List[str]) -> None:
    """Save discovered URLs to state file"""
    DISCOVERIES_DIR.mkdir(exist_ok=True)
    state_file = DISCOVERIES_DIR / f"{topic.lower().replace(' ', '_')}.json"
    
    state = {
        "topic": topic,
        "last_run": datetime.now().isoformat(),
        "discovered_urls": urls,
        "count": len(urls)
    }
    
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


def search_tavily(query: str, max_results: int = 10) -> List[Dict]:
    """Search using Tavily API"""
    if not TAVILY_API_KEY:
        print("  ⚠️ TAVILY_API_KEY not set, skipping Tavily search")
        return []
    
    url = "https://api.tavily.com/search"
    headers = {"Content-Type": "application/json"}
    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "search_depth": "advanced",
        "max_results": max_results,
        "include_answer": True,
        "include_raw_content": False
    }
    
    try:
        resp = requests.post(url, json=payload, headers=headers, timeout=30)
        resp.raise_for_status()
        data = resp.json()
        
        results = []
        for item in data.get("results", []):
            results.append({
                "url": item.get("url", ""),
                "title": item.get("title", ""),
                "description": item.get("description", ""),
                "content": item.get("content", "")[:500],  # First 500 chars
                "source": "tavily"
            })
        
        if data.get("answer"):
            results.insert(0, {
                "url": "",
                "title": "Tavily AI Answer",
                "description": data["answer"],
                "content": data["answer"],
                "source": "tavily_answer"
            })
        
        return results
        
    except Exception as e:
        print(f"  ⚠️ Tavily error: {e}")
        return []


def search_duckduckgo(query: str, max_results: int = 10) -> List[Dict]:
    """Fallback search using DuckDuckGo"""
    try:
        from duckduckgo_search import DDGS
        
        results = []
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "url": r.get("href", ""),
                    "title": r.get("title", ""),
                    "description": r.get("body", ""),
                    "content": r.get("body", "")[:500],
                    "source": "duckduckgo"
                })
        
        return results
        
    except ImportError:
        print("  ⚠️ duckduckgo-search not installed")
        return []
    except Exception as e:
        print(f"  ⚠️ DuckDuckGo error: {e}")
        return []


def is_valid_url(url: str) -> bool:
    """Check if URL is valid and crawlable"""
    if not url:
        return False
    
    parsed = urlparse(url)
    if not parsed.scheme or not parsed.netloc:
        return False
    
    # Skip certain domains
    skip_domains = ["twitter.com", "x.com", "facebook.com", "instagram.com"]
    if any(d in parsed.netloc.lower() for d in skip_domains):
        return False
    
    return True


def fetch_content(url: str) -> Optional[str]:
    """Fetch content from URL"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; WikiBot/1.0)"
        }
        resp = requests.get(url, headers=headers, timeout=15, allow_redirects=True)
        resp.raise_for_status()
        
        content_type = resp.headers.get("Content-Type", "")
        if "text/html" not in content_type and "text/plain" not in content_type:
            return None
        
        return resp.text[:50000]  # Limit to 50k chars
        
    except Exception:
        return None


def save_to_raw(content: str, url: str, title: str, topic: str, source: str) -> Path:
    """Save discovered content to raw/ directory"""
    # Determine subdirectory
    domain = urlparse(url).netloc.replace("www.", "").replace(".com", "")
    
    # Create topic subdirectory
    topic_dir = RAW_DIR / topic.lower().replace(" ", "-")
    topic_dir.mkdir(exist_ok=True)
    
    # Create filename from URL
    url_hash = str(abs(hash(url)))[:8]
    filename = f"{url_hash}_{domain}"
    
    # Save as markdown
    filepath = topic_dir / f"{filename}.md"
    
    frontmatter = f"""---
source: {source}
url: {url}
title: {title}
discovered: {datetime.now().strftime("%Y-%m-%d")}
topic: {topic}
---

# {title}

{content}
"""
    
    filepath.write_text(frontmatter)
    return filepath


def discover_topic(topic: Dict, existing: set, limit: int, dry_run: bool) -> List[Dict]:
    """Discover new content for a topic"""
    topic_name = topic["name"]
    keywords = topic.get("keywords", [topic_name])
    
    print(f"\n🔍 Discovering: {topic_name}")
    print(f"   Keywords: {', '.join(keywords)}")
    
    all_results = []
    seen_urls = set()
    
    for keyword in keywords:
        # Try Tavily first
        results = search_tavily(keyword, max_results=limit)
        
        if not results:
            # Fallback to DuckDuckGo
            results = search_duckduckgo(keyword, max_results=limit)
        
        for r in results:
            if r["url"] and r["url"] not in seen_urls and r["url"] not in existing:
                if is_valid_url(r["url"]):
                    seen_urls.add(r["url"])
                    all_results.append(r)
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
    
    # Filter out duplicates
    unique_results = []
    for r in all_results:
        if r["url"] not in seen_urls:
            seen_urls.add(r["url"])
            unique_results.append(r)
    
    print(f"   Found {len(unique_results)} new sources")
    
    if dry_run:
        for r in unique_results[:5]:
            print(f"   - {r['title'][:60]}...")
            print(f"     {r['url'][:80]}")
        return unique_results
    
    # Save to raw/
    saved = 0
    for r in unique_results:
        try:
            filepath = save_to_raw(
                r.get("content", r.get("description", "")),
                r["url"],
                r["title"],
                topic_name,
                r["source"]
            )
            print(f"   ✓ Saved: {r['title'][:50]}...")
            saved += 1
        except Exception as e:
            print(f"   ✗ Failed: {r['url'][:50]}... - {e}")
    
    # Save state
    save_discovery_state(topic_name, [r["url"] for r in unique_results])
    
    print(f"   💾 {saved} sources saved to raw/{topic_name.replace(' ', '-')}/")
    
    return unique_results


def main():
    parser = argparse.ArgumentParser(description="Discover new content from web")
    parser.add_argument("--topic", help="Specific topic to discover")
    parser.add_argument("--limit", type=int, default=MAX_RESULTS_PER_TOPIC, 
                       help="Max results per keyword")
    parser.add_argument("--dry-run", action="store_true", help="Preview without saving")
    parser.add_argument("--config", default="config/topics.yaml", help="Config file path")
    args = parser.parse_args()
    
    print(f"📡 Graphify Discover — {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    
    # Load existing sources
    existing = get_existing_sources()
    print(f"📂 {len(existing)} existing sources in raw/")
    
    # Load topics
    config = load_topics_config()
    topics = config.get("topics", [])
    
    if not topics:
        print("❌ No topics found in config")
        return
    
    # Filter by topic if specified
    if args.topic:
        topics = [t for t in topics if args.topic.lower() in t["name"].lower()]
        if not topics:
            print(f"❌ Topic '{args.topic}' not found")
            return
    
    # Discover for each topic
    total_new = 0
    for topic in topics:
        results = discover_topic(topic, existing, args.limit, args.dry_run)
        total_new += len(results)
        existing.update(r["url"] for r in results)
    
    print("\n" + "=" * 60)
    print(f"✅ Discovery complete: {total_new} new sources")
    
    if args.dry_run:
        print("🔍 (dry-run — no files saved)")
    
    # Generate discovery report
    report = f"""# Discovery Report — {datetime.now().strftime('%Y-%m-%d')}

## Summary
- **Topics scanned:** {len(topics)}
- **New sources found:** {total_new}
- **Mode:** {"dry-run" if args.dry_run else "live"}

## Topics
"""
    
    for topic in topics:
        report += f"- {topic['name']}: {topic.get('keywords', [])}\n"
    
    report += f"""
## Next Steps

1. Run ingest to process new sources:
   ```
   python3 scripts/ingest.py
   ```

2. Or manually review raw/ directory

*Generated at {datetime.now().isoformat()}*
"""
    
    report_path = Path("outputs/discovery_report.md")
    report_path.parent.mkdir(exist_ok=True, exist_ok=True)
    report_path.write_text(report)
    
    print(f"\n📄 Report: {report_path}")


if __name__ == "__main__":
    main()
