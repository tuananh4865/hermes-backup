#!/opt/homebrew/bin/python3.14
"""
Duplicate Detector — Find Pages with Similar/Overlapping Content

Problem: Wiki accumulates duplicate pages over time — same topic,
different names, or content overlap.

Solution: Detect duplicates using:
1. Title similarity (Levenshtein distance)
2. Content overlap (common lines/ngrams)
3. Circular links (pages linking to each other)

Usage:
    python duplicate_detector.py [--find-merges] [--merge PAGE1 PAGE2]
"""

import re
from pathlib import Path
from collections import Counter
from difflib import SequenceMatcher
from typing import Dict, List, Tuple, Set

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
CONCEPTS_PATH = WIKI_PATH / "concepts"


def normalize_text(text: str) -> str:
    """Normalize text for comparison"""
    text = text.lower()
    text = re.sub(r'[\s\-_]+', ' ', text)
    text = re.sub(r'[^\w\s]', '', text)
    return text.strip()


def levenshtein_distance(s1: str, s2: str) -> int:
    """Calculate Levenshtein distance between two strings"""
    if len(s1) < len(s2):
        return levenshtein_distance(s2, s1)
    if len(s2) == 0:
        return len(s1)
    
    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row
    
    return previous_row[-1]


def title_similarity(title1: str, title2: str) -> float:
    """Calculate similarity between two titles (0-1)"""
    norm1 = normalize_text(title1)
    norm2 = normalize_text(title2)
    return SequenceMatcher(None, norm1, norm2).ratio()


def extract_title(content: str) -> str:
    """Extract title from content"""
    # From frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            fm_text = content[3:end]
            title_match = re.search(r'^title:\s*(.+)$', fm_text, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip().strip('"\'')
    
    # From H1
    h1_match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    return ""


def extract_content(body: str) -> str:
    """Extract body content without frontmatter"""
    if body.startswith('---'):
        end = body.find('---', 3)
        if end != -1:
            return body[end+3:]
    return body


def get_page_words(content: str) -> Set[str]:
    """Get normalized words from page content"""
    body = extract_content(content)
    words = re.findall(r'\b\w{3,}\b', body.lower())
    return set(words)


def content_overlap(page1_words: Set[str], page2_words: Set[str]) -> float:
    """Calculate content overlap between two pages (0-1)"""
    if not page1_words or not page2_words:
        return 0.0
    
    intersection = len(page1_words & page2_words)
    union = len(page1_words | page2_words)
    
    return intersection / union if union > 0 else 0.0


def find_circular_links(all_pages: Dict[str, List[str]]) -> List[Tuple[str, str]]:
    """Find pairs of pages that link to each other"""
    circular = []
    
    for page, links in all_pages.items():
        for link in links:
            if link in all_pages and page in all_pages[link]:
                pair = tuple(sorted([page, link]))
                if pair not in circular:
                    circular.append(pair)
    
    return circular


def find_title_similarities(all_pages: Dict[str, Tuple[str, str]], threshold: float = 0.6) -> List[Dict]:
    """Find pages with similar titles"""
    pages = list(all_pages.keys())
    similarities = []
    
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            page1, (title1, _) = pages[i], all_pages[pages[i]]
            page2, (title2, _) = pages[j], all_pages[pages[j]]
            
            if title1 and title2:
                sim = title_similarity(title1, title2)
                if sim >= threshold:
                    # Calculate Levenshtein for short names
                    lev_dist = levenshtein_distance(
                        normalize_text(title1),
                        normalize_text(title2)
                    )
                    similarities.append({
                        'page1': page1,
                        'page2': page2,
                        'title1': title1,
                        'title2': title2,
                        'similarity': sim,
                        'levenshtein_distance': lev_dist
                    })
    
    return sorted(similarities, key=lambda x: x['similarity'], reverse=True)


def find_content_overlaps(
    all_pages: Dict[str, Tuple[str, Set[str]]], 
    threshold: float = 0.3
) -> List[Dict]:
    """Find pages with overlapping content"""
    pages = list(all_pages.keys())
    overlaps = []
    
    for i in range(len(pages)):
        for j in range(i + 1, len(pages)):
            page1, (_, words1) = pages[i], all_pages[pages[i]]
            page2, (_, words2) = pages[j], all_pages[pages[j]]
            
            if words1 and words2:
                overlap = content_overlap(words1, words2)
                if overlap >= threshold:
                    overlaps.append({
                        'page1': page1,
                        'page2': page2,
                        'overlap': overlap,
                        'common_words': len(words1 & words2)
                    })
    
    return sorted(overlaps, key=lambda x: x['overlap'], reverse=True)


def get_all_wikilinks(content: str) -> List[str]:
    """Extract wikilinks from content"""
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', content)


def load_all_pages() -> Dict[str, Tuple[str, str, Set[str], List[str]]]:
    """Load all pages with their metadata"""
    pages = {}
    
    for page_file in CONCEPTS_PATH.glob("*.md"):
        content = page_file.read_text()
        title = extract_title(content)
        words = get_page_words(content)
        links = get_all_wikilinks(content)
        
        pages[page_file.stem.lower()] = (title, content, words, links)
    
    return pages


def generate_merge_plan(title_duplicates: List[Dict], content_overlaps: List[Dict]) -> str:
    """Generate merge plan for duplicate pages"""
    plan = ["# Duplicate Pages Merge Plan\n"]
    
    if title_duplicates:
        plan.append("\n## Title Similarities (>60% similar)\n")
        for dup in title_duplicates[:10]:
            plan.append(f"- **{dup['title1']}** ({dup['similarity']:.0%} similar to {dup['title2']})")
            plan.append(f"  - Pages: `{dup['page1']}` ↔ `{dup['page2']}`")
            plan.append(f"  - Edit distance: {dup['levenshtein_distance']}")
    
    if content_overlaps:
        plan.append("\n## Content Overlaps (>30% word overlap)\n")
        for dup in content_overlaps[:10]:
            plan.append(f"- `{dup['page1']}` ↔ `{dup['page2']}` ({dup['overlap']:.0%} overlap, {dup['common_words']} common words)")
    
    return '\n'.join(plan)


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Duplicate Detector")
    parser.add_argument('--threshold', type=float, default=0.6,
                        help='Title similarity threshold (default: 0.6)')
    parser.add_argument('--content-threshold', type=float, default=0.3,
                        help='Content overlap threshold (default: 0.3)')
    parser.add_argument('--find-merges', action='store_true',
                        help='Find potential merges')
    parser.add_argument('--merge', nargs=2, metavar=('PAGE1', 'PAGE2'),
                        help='Merge two pages (creates redirect)')
    
    args = parser.parse_args()
    
    print("🔍 Loading wiki pages...")
    all_pages = load_all_pages()
    print(f"   Loaded {len(all_pages)} pages\n")
    
    if args.find_merges or (not args.merge):
        print("📊 Finding duplicates...\n")
        
        # Build lookup by title
        page_titles = {stem: data[0] for stem, data in all_pages.items()}
        page_words = {stem: data[2] for stem, data in all_pages.items()}
        page_links = {stem: data[3] for stem, data in all_pages.items()}
        
        # Title similarities
        combined = {
            stem: (page_titles.get(stem, ""), page_words.get(stem, set()))
            for stem in all_pages.keys()
        }
        
        title_sims = find_title_similarities(
            {stem: (page_titles.get(stem, ""), page_words.get(stem, set())) 
             for stem in all_pages.keys()},
            threshold=args.threshold
        )
        
        # Content overlaps
        content_ov = find_content_overlaps(combined, threshold=args.content_threshold)
        
        # Circular links
        circular = find_circular_links(page_links)
        
        print(f"🔤 Title similarities (>{args.threshold:.0%}): {len(title_sims)}")
        print(f"📄 Content overlaps (>{args.content_threshold:.0%}): {len(content_ov)}")
        print(f"🔄 Circular links: {len(circular)}\n")
        
        if title_sims:
            print("\n## Top Title Similarities\n")
            for dup in title_sims[:5]:
                print(f"  [{dup['similarity']:.0%}] {dup['title1']}")
                print(f"         ↔ {dup['title2']}")
                print(f"         Pages: `{dup['page1']}` ↔ `{dup['page2']}`")
                print()
        
        if content_ov:
            print("\n## Top Content Overlaps\n")
            for dup in content_ov[:5]:
                print(f"  [{dup['overlap']:.0%}] `{dup['page1']}` ↔ `{dup['page2']}`")
                print(f"          ({dup['common_words']} common words)")
                print()
        
        if circular:
            print("\n## Circular Links (bidirectional)\n")
            for p1, p2 in circular:
                print(f"  `{p1}` ↔ `{p2}`")
        
        # Save merge plan
        plan = generate_merge_plan(title_sims, content_ov)
        plan_file = WIKI_PATH / "concepts" / ".merge-plan.md"
        plan_file.write_text(plan)
        print(f"\n💾 Merge plan saved to: {plan_file}")
    
    elif args.merge:
        page1, page2 = args.merge
        print(f"🔀 Merge {page1} + {page2} (not yet implemented)")
        print("   For now, manually copy content and create redirect")


if __name__ == "__main__":
    main()
