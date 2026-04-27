#!/opt/homebrew/bin/python3.14
"""
Confidence Scorer — Score how confident the wiki is about each fact

Factors:
- source_count: Multiple sources = higher confidence
- cross_reference: Referenced by multiple pages = higher
- recency: Recently updated = higher
- user_verified: No corrections = higher

Usage:
    python3 confidence_scorer.py
    python3 confidence_scorer.py --page concepts/lm-studio.md
    python3 confidence_scorer.py --low
"""

import argparse
import json
import re
import subprocess
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
CONCEPTS_PATH = WIKI_PATH / "concepts"
SCORES_FILE = WIKI_PATH / "scripts" / ".confidence_scores.json"

# Scoring weights
WEIGHTS = {
    'source_count': 0.25,      # More sources = higher
    'cross_reference': 0.25,   # More references = higher
    'recency': 0.20,           # Recently updated = higher
    'user_verified': 0.20,     # No corrections = higher
    'completeness': 0.10,      # Has frontmatter, links = higher
}

# ═══════════════════════════════════════════════════════════════

def load_corrections() -> Dict:
    """Load correction data"""
    corrections_file = WIKI_PATH / "scripts" / ".corrections.json"
    if corrections_file.exists():
        return json.loads(corrections_file.read_text())
    return {'page_quality_impact': {}}

def load_signals() -> Dict:
    """Load interest signals"""
    signals_file = WIKI_PATH / "scripts" / ".interest_signals.json"
    if signals_file.exists():
        return json.loads(signals_file.read_text())
    return {}

def get_all_pages() -> List[Path]:
    """Get all concept pages"""
    pages = []
    for md_file in CONCEPTS_PATH.rglob("*.md"):
        if '_templates' in md_file.parts:
            continue
        pages.append(md_file)
    return pages

def parse_frontmatter(content: str) -> Dict:
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

def extract_sources(content: str) -> int:
    """Extract source count from frontmatter"""
    fm = parse_frontmatter(content)
    sources = fm.get('sources', '')
    if sources:
        # Count items in array
        return sources.count(',') + 1
    return 0

def get_backlinks(page_name: str) -> int:
    """Count incoming wikilinks"""
    count = 0
    pages = get_all_pages()
    
    for page in pages:
        try:
            content = page.read_text(encoding='utf-8')
            # Count [[page]] references
            links = re.findall(r'\[\[([^\]|]+)', content)
            if page_name in links or page.stem in links:
                count += 1
        except:
            pass
    
    return count

def get_page_age(page_path: Path) -> int:
    """Get age of page in days"""
    try:
        mtime = datetime.fromtimestamp(page_path.stat().st_mtime)
        age = (datetime.now() - mtime).days
        return age
    except:
        return 999

def get_wikilink_count(content: str) -> int:
    """Count wikilinks in content"""
    # Remove code blocks
    content = re.sub(r'```[\s\S]*?```', '', content)
    content = re.sub(r'`[^`]+`', '', content)
    
    links = re.findall(r'\[\[([^\]]+)\]\]', content)
    return len(links)

def score_page(page_path: Path) -> Dict:
    """Score confidence for a single page"""
    content = page_path.read_text(encoding='utf-8')
    fm = parse_frontmatter(content)
    
    page_name = page_path.stem
    
    # Factor 1: Source count (0-4 sources)
    source_count = extract_sources(content)
    source_score = min(source_count * 0.25, 1.0)
    
    # Factor 2: Cross-references (0-5+ references)
    backlinks = get_backlinks(page_name)
    reference_score = min(backlinks * 0.2, 1.0)
    
    # Factor 3: Recency (0-30 days = full, 30-90 = half, 90+ = low)
    age = get_page_age(page_path)
    if age <= 7:
        recency_score = 1.0
    elif age <= 30:
        recency_score = 0.8
    elif age <= 90:
        recency_score = 0.5
    else:
        recency_score = 0.2
    
    # Factor 4: User verified (correction penalty)
    corrections = load_corrections()
    correction_count = corrections.get('page_quality_impact', {}).get(page_name, {}).get('corrections', 0)
    verified_score = max(0, 1.0 - correction_count * 0.2)
    
    # Factor 5: Completeness (has frontmatter, wikilinks)
    completeness_score = 0.5
    if fm.get('title'):
        completeness_score += 0.25
    if get_wikilink_count(content) >= 2:
        completeness_score += 0.25
    
    # Weighted total
    total = (
        source_score * WEIGHTS['source_count'] +
        reference_score * WEIGHTS['cross_reference'] +
        recency_score * WEIGHTS['recency'] +
        verified_score * WEIGHTS['user_verified'] +
        completeness_score * WEIGHTS['completeness']
    ) / sum(WEIGHTS.values())  # Normalize
    
    # Convert to 0-10 scale
    total = total * 10
    
    return {
        'page': str(page_path.relative_to(WIKI_PATH)),
        'title': fm.get('title', page_name),
        'score': round(total, 1),
        'factors': {
            'sources': source_count,
            'references': backlinks,
            'age_days': age,
            'corrections': correction_count,
            'wikilinks': get_wikilink_count(content)
        }
    }

def score_all_pages() -> List[Dict]:
    """Score all pages"""
    pages = get_all_pages()
    scores = []
    
    for page in pages:
        try:
            score = score_page(page)
            scores.append(score)
        except Exception as e:
            print(f"Error scoring {page}: {e}")
    
    # Sort by score
    scores.sort(key=lambda x: x['score'], reverse=True)
    return scores

def print_report(scores: List[Dict], low_only: bool = False):
    """Print confidence report"""
    print("=" * 70)
    print("CONFIDENCE SCORING REPORT")
    print("=" * 70)
    
    if low_only:
        low_scores = [s for s in scores if s['score'] < 7.0]
        print(f"\nLow-confidence pages (< 7.0): {len(low_scores)}")
        
        for score in low_scores:
            print(f"\n{score['title']} ({score['score']}/10)")
            print(f"  Sources: {score['factors']['sources']}, Refs: {score['factors']['references']}")
            print(f"  Age: {score['factors']['age_days']}d, Corrections: {score['factors']['corrections']}")
    else:
        avg = sum(s['score'] for s in scores) / len(scores) if scores else 0
        print(f"\nTotal pages: {len(scores)}")
        print(f"Average confidence: {avg:.1f}/10")
        
        print(f"\nHigh confidence (8+): {len([s for s in scores if s['score'] >= 8.0])}")
        print(f"Medium confidence (6-8): {len([s for s in scores if 6.0 <= s['score'] < 8.0])}")
        print(f"Low confidence (<6): {len([s for s in scores if s['score'] < 6.0])}")
        
        print(f"\n" + "=" * 70)
        print("ALL PAGES (by confidence)")
        print("=" * 70)
        
        for score in scores[:20]:
            confidence_emoji = "🟢" if score['score'] >= 8 else "🟡" if score['score'] >= 6 else "🔴"
            print(f"{confidence_emoji} {score['score']:.1f}/10 | {score['title']}")

def save_scores(scores: List[Dict]):
    """Save scores to file"""
    SCORES_FILE.parent.mkdir(parents=True, exist_ok=True)
    SCORES_FILE.write_text(json.dumps(scores, indent=2))
    print(f"\nSaved to {SCORES_FILE}")

def main():
    parser = argparse.ArgumentParser(description='Score wiki confidence')
    parser.add_argument('--page', help='Score specific page')
    parser.add_argument('--low', action='store_true', help='Show only low-confidence pages')
    parser.add_argument('--save', action='store_true', help='Save scores to file')
    args = parser.parse_args()
    
    if args.page:
        page_path = WIKI_PATH / args.page
        if page_path.exists():
            score = score_page(page_path)
            print(f"\nConfidence Score: {score['score']}/10")
            print(f"\nFactors:")
            for k, v in score['factors'].items():
                print(f"  {k}: {v}")
        else:
            print(f"Page not found: {args.page}")
        return
    
    scores = score_all_pages()
    print_report(scores, low_only=args.low)
    
    if args.save:
        save_scores(scores)

if __name__ == '__main__':
    main()
