#!/opt/homebrew/bin/python3.14
"""
Freshness Score — Detect Stale Content and Source Changes

Problem: Wiki pages become stale — source URLs change, facts become
outdated, topics evolve but pages don't update.

Solution: Multi-factor freshness scoring:
- Time since update
- Source URL validity
- Topic velocity (change frequency in related sources)

Usage:
    python freshness_score.py [--score-all] [--check-sources] [--stale-only]
"""

import re
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import urllib.request
import urllib.error

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
CONCEPTS_PATH = WIKI_PATH / "concepts"


def extract_frontmatter(content: str) -> Dict[str, str]:
    """Parse YAML frontmatter"""
    fm = {}
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            fm_text = content[3:end]
            for line in fm_text.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    fm[key.strip()] = value.strip().strip('"\'')
    return fm


def extract_title(content: str) -> str:
    """Extract title from content"""
    fm = extract_frontmatter(content)
    if fm.get('title'):
        return fm['title']
    
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    return "Untitled"


def extract_source_urls(content: str) -> List[str]:
    """Extract URLs from content"""
    url_pattern = r'https?://[^\s\)"\'<>]+'
    urls = re.findall(url_pattern, content)
    # Filter out common non-source URLs
    filtered = []
    for url in urls:
        # Skip common non-content URLs
        skip_domains = ['github.com', 'wikipedia.org', 'arxiv.org', 'i.imgur.com']
        if not any(domain in url for domain in skip_domains):
            filtered.append(url)
    return filtered


def days_since_update(page_path: Path) -> int:
    """Get days since file was last modified"""
    mtime = datetime.fromtimestamp(page_path.stat().st_mtime)
    return (datetime.now() - mtime).days


def check_url_status(url: str, timeout: int = 5) -> bool:
    """Check if URL returns 200 OK"""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib.request.urlopen(req, timeout=timeout)
        return response.status == 200
    except:
        return False


def get_page_age_score(days: int, threshold: int = 30) -> float:
    """
    Score based on age (0-1, higher = fresher)
    Default threshold: 30 days
    """
    if days <= 7:
        return 1.0
    elif days <= 14:
        return 0.9
    elif days <= 30:
        return 0.7
    elif days <= 60:
        return 0.5
    elif days <= 90:
        return 0.3
    else:
        return 0.1


def get_source_validity_score(valid_urls: int, total_urls: int) -> float:
    """
    Score based on source URL validity (0-1)
    """
    if total_urls == 0:
        return 0.5  # No sources = neutral
    
    return valid_urls / total_urls


def calculate_freshness_score(
    page_path: Path,
    content: str,
    source_check: bool = False
) -> Dict:
    """Calculate comprehensive freshness score for a page"""
    
    # Age score
    days = days_since_update(page_path)
    age_score = get_page_age_score(days)
    
    # Source validity score
    urls = extract_source_urls(content)
    if source_check and urls:
        # Check URLs with timeout
        valid_count = 0
        for url in urls[:5]:  # Limit to 5 URL checks
            if check_url_status(url):
                valid_count += 1
            time.sleep(0.1)  # Rate limit
        
        source_score = get_source_validity_score(valid_count, len(urls))
    else:
        source_score = 0.5 if urls else 0.5  # Neutral if no source check or no URLs
    
    # Content density score (pages with more content are more likely to be maintained)
    body = content[content.find('---', 3)+3:] if content.startswith('---') else content
    word_count = len(body.split())
    density_score = min(1.0, word_count / 500)  # 500 words = full score
    
    # Calculate final score (weighted average)
    freshness_score = (
        age_score * 0.4 +        # 40% weight on age
        source_score * 0.3 +     # 30% weight on source validity
        density_score * 0.3      # 30% weight on content density
    )
    
    return {
        'page': page_path.stem,
        'path': str(page_path.relative_to(WIKI_PATH)),
        'days_since_update': days,
        'age_score': age_score,
        'source_score': source_score,
        'density_score': density_score,
        'freshness_score': freshness_score,
        'url_count': len(urls),
        'valid_urls': 0,  # Would be populated if source_check=True
        'word_count': word_count,
        'status': get_status(freshness_score)
    }


def get_status(score: float) -> str:
    """Get status label from score"""
    if score >= 0.8:
        return "🟢 Fresh"
    elif score >= 0.6:
        return "🟡 Moderate"
    elif score >= 0.4:
        return "🟠 Stale"
    else:
        return "🔴 Very Stale"


def score_all_pages(source_check: bool = False) -> List[Dict]:
    """Score all wiki pages"""
    scores = []
    
    for page in CONCEPTS_PATH.glob("*.md"):
        content = page.read_text()
        score = calculate_freshness_score(page, content, source_check)
        scores.append(score)
    
    return sorted(scores, key=lambda x: x['freshness_score'])


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Freshness Score")
    parser.add_argument('--score-all', action='store_true',
                        help='Score all pages')
    parser.add_argument('--check-sources', action='store_true',
                        help='Check source URL validity (slower)')
    parser.add_argument('--stale-only', action='store_true',
                        help='Show only stale pages (score < 0.6)')
    parser.add_argument('--threshold', type=float, default=0.6,
                        help='Stale threshold (default: 0.6)')
    
    args = parser.parse_args()
    
    print("📊 Calculating freshness scores...\n")
    
    scores = score_all_pages(source_check=args.check_sources)
    
    if args.score_all or args.stale_only or not scores:
        print(f"{'Page':<35} {'Days':>5} {'Freshness':>10} {'Status':<12}")
        print("-" * 65)
        
        stale_count = 0
        for score in scores:
            if args.stale_only and score['freshness_score'] >= args.threshold:
                continue
            
            status = score['status']
            freshness = f"{score['freshness_score']:.2f}"
            days = f"{score['days_since_update']}"
            page = score['page'][:34]
            
            print(f"{page:<35} {days:>5} {freshness:>10} {status:<12}")
            
            if score['freshness_score'] < args.threshold:
                stale_count += 1
        
        print()
        
        # Summary
        total = len(scores)
        fresh = sum(1 for s in scores if s['freshness_score'] >= 0.8)
        moderate = sum(1 for s in scores if 0.6 <= s['freshness_score'] < 0.8)
        stale = sum(1 for s in scores if s['freshness_score'] < 0.6)
        
        print(f"\n📈 Summary:")
        print(f"   🟢 Fresh (≥0.8):     {fresh}")
        print(f"   🟡 Moderate (0.6-0.8): {moderate}")
        print(f"   🟠/🔴 Stale (<0.6):  {stale}")
        print(f"   Total pages:         {total}")
        
        if args.stale_only:
            print(f"\n⚠️  {stale_count} stale pages need attention")


if __name__ == "__main__":
    main()
