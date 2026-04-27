#!/opt/homebrew/bin/python3.14
"""
Contradiction Detector — Find Conflicting Claims Across Pages

Problem: Wiki may contain contradictory information across pages —
same fact stated differently, outdated claims, conflicting advice.

Solution: Detect contradictions using:
1. Semantic similarity of claims
2. Temporal conflicts ("recent X" vs dated info)
3. Explicit contradictions (negation patterns)
4. Fact comparison across pages

Usage:
    python contradiction_detector.py [--find-contradictions]
"""

import re
from pathlib import Path
from collections import defaultdict
from typing import Dict, List, Tuple, Set

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


def extract_body(content: str) -> str:
    """Extract body without frontmatter"""
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            return content[end+3:]
    return content


def extract_claims(content: str) -> List[Dict]:
    """Extract factual claims from content"""
    claims = []
    body = extract_body(content)
    
    # Patterns that indicate factual claims
    claim_patterns = [
        (r'(?i)(is|are|was|were)\s+([^.!?]*[a-z]{10,}[^.!?]*(?:\.|!|\?))', 'fact'),
        (r'(?i)(can|cannot|could|will|should|must)\s+([^.!?]*[a-z]{10,}[^.!?]*(?:\.|!|\?))', 'capability'),
        (r'(?i)(has|have|had|possesses)\s+([^.!?]*[a-z]{10,}[^.!?]*(?:\.|!|\?))', 'possession'),
        (r'(?i)(uses?|using|used)\s+([^.!?]*[a-z]{10,}[^.!?]*(?:\.|!|\?))', 'usage'),
    ]
    
    for pattern, claim_type in claim_patterns:
        matches = re.finditer(pattern, body)
        for match in matches:
            full_match = match.group(0).strip()
            if len(full_match) > 15:  # Filter short matches
                claims.append({
                    'text': full_match,
                    'type': claim_type,
                    'position': match.start()
                })
    
    return claims


def extract_dates(content: str) -> List[Tuple[str, str]]:
    """Extract dates and their context"""
    body = extract_body(content)
    dates = []
    
    # Date patterns
    date_patterns = [
        (r'(?i)(recent|recently|latest|new|updated)\s+([^.!?]*\d{4}[^.!?]*)', 'recent'),
        (r'(?i)(old|outdated|deprecated|legacy)\s+([^.!?]*\d{4}[^.!?]*)', 'old'),
        (r'(\d{4}-\d{2}-\d{2})', 'specific'),
        (r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', 'formal'),
    ]
    
    for pattern, date_type in date_patterns:
        matches = re.finditer(pattern, body, re.IGNORECASE)
        for match in matches:
            dates.append((match.group(0), date_type))
    
    return dates


def extract_negations(content: str) -> List[str]:
    """Extract negated statements (potential contradictions)"""
    body = extract_body(content)
    negations = []
    
    negation_patterns = [
        r'(?i)(isn\'t|aren\'t|wasn\'t|weren\'t)\s+([^.!?]*[a-z]{10,})',
        r'(?i)(doesn\'t|don\'t)\s+([^.!?]*[a-z]{10,})',
        r'(?i)(cannot|can\'t|couldn\'t)\s+([^.!?]*[a-z]{10,})',
        r'(?i)(will not|won\'t)\s+([^.!?]*[a-z]{10,})',
        r'(?i)(should not|shouldn\'t)\s+([^.!?]*[a-z]{10,})',
        r'(?i)(never|not always|not all)',
        r'(?i)(unlike|rather than|instead of)',
    ]
    
    for pattern in negation_patterns:
        matches = re.finditer(pattern, body, re.IGNORECASE)
        for match in matches:
            text = match.group(0).strip()
            if len(text) > 10:
                negations.append(text)
    
    return negations


def extract_topic_tags(content: str) -> List[str]:
    """Extract topic tags from frontmatter"""
    fm = extract_frontmatter(content)
    tags_str = fm.get('tags', '')
    
    if tags_str:
        # Parse [tag1, tag2] format
        tags = re.findall(r'(\w+)', tags_str)
        return tags
    
    return []


def load_all_pages() -> Dict[str, Dict]:
    """Load all pages with their claims and metadata"""
    pages = {}
    
    for page_file in CONCEPTS_PATH.glob("*.md"):
        content = page_file.read_text()
        title = extract_title(content)
        body = extract_body(content)
        claims = extract_claims(content)
        negations = extract_negations(content)
        tags = extract_topic_tags(content)
        
        pages[page_file.stem] = {
            'title': title,
            'content': content,
            'body': body,
            'claims': claims,
            'negations': negations,
            'tags': tags,
            'path': page_file
        }
    
    return pages


def find_temporal_conflicts(pages: Dict[str, Dict]) -> List[Dict]:
    """Find pages with conflicting temporal claims"""
    conflicts = []
    
    # Group pages by shared tags
    tag_pages = defaultdict(list)
    for stem, page in pages.items():
        for tag in page['tags']:
            tag_pages[tag].append((stem, page))
    
    # Check for recent/old conflicts within same tag
    for tag, tagged_pages in tag_pages.items():
        if len(tagged_pages) < 2:
            continue
        
        for i, (stem1, page1) in enumerate(tagged_pages):
            for stem2, page2 in tagged_pages[i+1:]:
                dates1 = [d[0] for d in extract_dates(page1['content'])]
                dates2 = [d[0] for d in extract_dates(page2['content'])]
                
                # Check for opposite temporal claims
                has_recent_1 = any('recent' in d.lower() or 'new' in d.lower() for d in dates1)
                has_old_1 = any('old' in d.lower() or 'outdated' in d.lower() for d in dates1)
                has_recent_2 = any('recent' in d.lower() or 'new' in d.lower() for d in dates2)
                has_old_2 = any('old' in d.lower() or 'outdated' in d.lower() for d in dates2)
                
                if (has_recent_1 and has_old_2) or (has_recent_2 and has_old_1):
                    conflicts.append({
                        'type': 'temporal',
                        'page1': stem1,
                        'page2': stem2,
                        'tag': tag,
                        'description': f"One says recent, other says old for '{tag}'"
                    })
    
    return conflicts


def find_negation_conflicts(pages: Dict[str, Dict]) -> List[Dict]:
    """Find pages with negated statements about same topics"""
    conflicts = []
    
    # Get topics from tags and titles
    all_topics = set()
    topic_pages = defaultdict(list)
    
    for stem, page in pages.items():
        topics = set(page['tags'])
        # Also add words from title
        title_words = re.findall(r'\b\w{4,}\b', page['title'].lower())
        topics.update(title_words)
        
        for topic in topics:
            if len(topic) > 3 and topic not in ['wiki', 'concept', 'page']:
                all_topics.add(topic)
                topic_pages[topic].append(stem)
    
    # Check pages with negations against pages with positive claims
    for topic, topic_stems in topic_pages.items():
        if len(topic_stems) < 2:
            continue
        
        pages_with_negation = []
        pages_with_positive = []
        
        for stem in topic_stems:
            page = pages[stem]
            if page['negations']:
                pages_with_negation.append(stem)
            if page['claims']:
                pages_with_positive.append(stem)
        
        if pages_with_negation and pages_with_positive:
            for neg_stem in pages_with_negation:
                for pos_stem in pages_with_positive:
                    if neg_stem != pos_stem:
                        conflicts.append({
                            'type': 'negation',
                            'page_neg': neg_stem,
                            'page_pos': pos_stem,
                            'topic': topic,
                            'negations': pages[neg_stem]['negations'][:3],
                            'description': f"'{neg_stem}' negates '{topic}' but '{pos_stem}' asserts it"
                        })
    
    return conflicts


def find_capability_conflicts(pages: Dict[str, Dict]) -> List[Dict]:
    """Find pages with conflicting capability claims"""
    conflicts = []
    
    # Extract capability claims: can/cannot, should/shouldn't
    capability_patterns = [
        (r'(?i)\bcan\b(.*)', 'can'),
        (r'(?i)\bcannot\b(.*)', 'cannot'),
        (r'(?i)\bshould\b(.*)', 'should'),
        (r'(?i)\bshould not\b(.*)', 'should not'),
        (r'(?i)\bmust\b(.*)', 'must'),
        (r'(?i)\bmust not\b(.*)', 'must not'),
    ]
    
    page_capabilities = {}
    for stem, page in pages.items():
        capabilities = []
        for pattern, cap_type in capability_patterns:
            matches = re.finditer(pattern, page['body'])
            for match in matches:
                text = match.group(0).strip()
                if len(text) > 5:
                    capabilities.append((cap_type, text))
        page_capabilities[stem] = capabilities
    
    # Compare pages with shared topics
    for stem1 in page_capabilities:
        for stem2 in page_capabilities:
            if stem1 >= stem2:
                continue
            
            caps1 = page_capabilities[stem1]
            caps2 = page_capabilities[stem2]
            
            if not caps1 or not caps2:
                continue
            
            # Check for opposite claims
            for type1, claim1 in caps1:
                for type2, claim2 in caps2:
                    # Simple opposite check
                    opposites = {
                        ('can', 'cannot'),
                        ('should', 'should not'),
                        ('must', 'must not'),
                    }
                    
                    if (type1, type2) in opposites or (type2, type1) in opposites:
                        conflicts.append({
                            'type': 'capability',
                            'page1': stem1,
                            'page2': stem2,
                            'claim1': claim1[:80],
                            'claim2': claim2[:80],
                            'description': f"Contradictory: {type1} vs {type2}"
                        })
    
    return conflicts[:10]  # Limit results


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Contradiction Detector")
    parser.add_argument('--find-contradictions', action='store_true',
                        help='Find all contradictions')
    parser.add_argument('--verbose', action='store_true',
                        help='Show detailed output')
    
    args = parser.parse_args()
    
    print("🔍 Loading wiki pages...")
    pages = load_all_pages()
    print(f"   Loaded {len(pages)} pages\n")
    
    print("📊 Analyzing for contradictions...\n")
    
    # Temporal conflicts
    print("⏰ Temporal Conflicts (recent vs old claims)...")
    temporal = find_temporal_conflicts(pages)
    if temporal:
        for conflict in temporal[:5]:
            print(f"  ⚠️  {conflict['description']}")
            print(f"      Pages: `{conflict['page1']}` ↔ `{conflict['page2']}` (tag: {conflict['tag']})")
    else:
        print("  ✅ No temporal conflicts found")
    
    print()
    
    # Capability conflicts
    print("⚡ Capability Conflicts (can vs cannot, should vs shouldn't)...")
    capabilities = find_capability_conflicts(pages)
    if capabilities:
        for conflict in capabilities[:5]:
            print(f"  ⚠️  {conflict['description']}")
            print(f"      `{conflict['page1']}`: {conflict['claim1']}")
            print(f"      `{conflict['page2']}`: {conflict['claim2']}")
    else:
        print("  ✅ No capability conflicts found")
    
    print()
    
    # Negation conflicts
    print("❌ Negation Conflicts (pages asserting vs negating same topic)...")
    negations = find_negation_conflicts(pages)
    if negations:
        for conflict in negations[:5]:
            print(f"  ⚠️  {conflict['description']}")
            print(f"      Negates: `{conflict['page_neg']}`")
            print(f"      Asserts: `{conflict['page_pos']}`")
            if args.verbose:
                for neg in conflict['negations'][:2]:
                    print(f"        - {neg[:60]}")
    else:
        print("  ✅ No negation conflicts found")
    
    print()
    
    # Summary
    total = len(temporal) + len(capabilities) + len(negations)
    print(f"📈 Summary: {total} potential contradictions found")
    if total > 0:
        print("   These need human review to confirm if they're actual conflicts")


if __name__ == "__main__":
    main()
