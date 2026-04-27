#!/opt/homebrew/bin/python3.14
"""
Priority Gap Analyzer — Find missing wiki topics weighted by user interest

Unlike wiki_gap_analyzer which treats all gaps equally,
this prioritizes gaps based on user interest signals.

Usage:
    python3 priority_gap_analyzer.py --top 10
    python3 priority_gap_analyzer.py --weights
    python3 priority_gap_analyzer.py --threshold 50
"""

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Optional

# Add parent dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

# Import interest signals
try:
    from interest_signal_tracker import load_signals, get_top_interests, TOPIC_KEYWORDS
except ImportError:
    # Fallback if import fails
    TOPIC_KEYWORDS = {
        'lm-studio': ['lm studio', 'lm-studio'],
        'fine-tuning': ['fine-tune', 'finetune', 'lora'],
        'models': ['model', 'llm'],
        'mlx': ['mlx', 'apple silicon'],
        'github': ['github', 'git'],
        'automation': ['automation', 'script'],
        'wiki': ['wiki', 'knowledge base'],
    }
    
    def load_signals():
        p = Path.home() / 'wiki' / 'scripts' / '.interest_signals.json'
        if p.exists():
            return json.loads(p.read_text())
        return {}

    def get_top_interests(signals, days=30, top_n=10):
        return []

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
CONCEPTS_PATH = WIKI_PATH / "concepts"
SIGNALS_FILE = WIKI_PATH / "scripts" / ".interest_signals.json"

# Gap scoring weights
WEIGHTS = {
    'user_interest': 0.40,      # How much user asks about this
    'recency': 0.20,            # Recently discussed
    'breadth': 0.20,            # Connects many pages
    'severity': 0.20,           # How missing the content is
}

# Standard gaps to check (topics that should probably exist)
STANDARD_TOPICS = [
    'attention', 'transformer', 'lora', 'qlora', 'rlhf', 'dpo',
    'embedding', 'vector-db', 'rag', 'fine-tuning',
    'whisper', 'tts', 'stt',
    'mlx', 'apple-silicon',
    'hermes', 'mcp',
    'obsidian', 'logseq',
    'lm-studio', 'ollama', 'llama.cpp',
    'agent', 'autonomous',
    'testing', 'ci-cd',
    'docker', 'kubernetes',
    'postgres', 'sqlite', 'database',
    'api', 'rest', 'graphql',
]

# ═══════════════════════════════════════════════════════════════

def get_existing_topics() -> set:
    """Get all existing topics from concepts/"""
    topics = set()
    
    if not CONCEPTS_PATH.exists():
        return topics
    
    for md_file in CONCEPTS_PATH.rglob("*.md"):
        # Extract words from filename
        name = md_file.stem.lower()
        # Split on various separators
        words = re.split(r'[-_\s/|\\]+', name)
        topics.update(words)
        
        # Also check content for keywords
        try:
            content = md_file.read_text(encoding='utf-8').lower()
            for topic, keywords in TOPIC_KEYWORDS.items():
                for kw in keywords:
                    if kw in content:
                        topics.add(topic)
        except:
            pass
    
    return topics

def find_related_keyword(topic: str) -> Optional[str]:
    """Find a keyword in TOPIC_KEYWORDS that matches the topic"""
    topic_lower = topic.lower()
    for key, keywords in TOPIC_KEYWORDS.items():
        if key == topic_lower:
            return key
        for kw in keywords:
            if kw in topic_lower or topic_lower in kw:
                return key
    return None

def calculate_gap_score(
    topic: str,
    existing_topics: set,
    signals: Dict,
    connections: Dict
) -> float:
    """Calculate priority score for a gap"""
    
    # User interest score (0-100)
    top_interests = get_top_interests(signals, top_n=20)
    interest_map = {item['topic']: item['score'] for item in top_interests}
    
    # Map topic to known interest
    mapped_topic = find_related_keyword(topic) or topic
    user_interest_score = interest_map.get(mapped_topic, 0)
    
    # Recency score (0-100)
    top_interests_by_recency = get_top_interests(signals, days=7, top_n=20)
    recent_map = {item['topic']: 100 - item['days_since'] * 5 for item in top_interests_by_recency}
    recency_score = recent_map.get(mapped_topic, 0)
    
    # Breadth score (0-100) - how many connections this topic would have
    breadth_score = connections.get(topic, 0) * 10  # Each connection = 10 points
    
    # Severity score (0-100) - how missing is this?
    # Based on how many related topics exist but this one doesn't
    severity_score = 50  # Default medium severity
    
    if topic.lower() in [t.lower() for t in existing_topics]:
        severity_score = 0  # Not actually a gap
    elif any(topic.lower() in t.lower() or t.lower() in topic.lower() for t in existing_topics):
        severity_score = 30  # Partial match exists
    
    # Weighted sum
    total = (
        user_interest_score * WEIGHTS['user_interest'] +
        recency_score * WEIGHTS['recency'] +
        breadth_score * WEIGHTS['breadth'] +
        severity_score * WEIGHTS['severity']
    )
    
    return round(total, 1)

def find_topic_connections(existing_topics: List[str]) -> Dict[str, int]:
    """Find how many connections each potential topic has"""
    connections = {}
    
    for topic in STANDARD_TOPICS:
        count = 0
        topic_lower = topic.lower()
        topic_keywords = TOPIC_KEYWORDS.get(topic, [topic])
        
        for existing in existing_topics:
            existing_lower = existing.lower()
            # Check direct match
            if topic_lower == existing_lower:
                count += 1
            # Check keyword match
            for kw in topic_keywords:
                if kw in existing_lower or existing_lower in kw:
                    count += 1
                    break
        
        connections[topic] = min(count, 10)  # Cap at 10
    
    return connections

def analyze_gaps(min_score: float = 0) -> List[Dict]:
    """Find and score all gaps"""
    signals = load_signals()
    existing = get_existing_topics()
    
    # Find all potential gaps
    all_topics = set(STANDARD_TOPICS)
    gaps = []
    
    for topic in all_topics:
        if topic.lower() not in [t.lower() for t in existing]:
            gaps.append(topic)
    
    # Find connections
    connections = find_topic_connections(list(existing))
    
    # Score gaps
    scored_gaps = []
    for topic in gaps:
        score = calculate_gap_score(topic, existing, signals, connections)
        if score >= min_score:
            mapped = find_related_keyword(topic)
            scored_gaps.append({
                'topic': topic,
                'score': score,
                'mapped_interest': mapped,
                'connections': connections.get(topic, 0),
                'user_interest': signals.get('topic_frequency', {}).get(mapped, 0) if mapped else 0
            })
    
    # Sort by score
    scored_gaps.sort(key=lambda x: x['score'], reverse=True)
    
    return scored_gaps

def print_report(gaps: List[Dict], top_n: int = 10):
    """Print gap analysis report"""
    print("=" * 70)
    print("PRIORITY GAP ANALYSIS")
    print("=" * 70)
    print(f"\nTotal gaps found: {len(gaps)}")
    
    if gaps:
        print(f"\nTop {top_n} Priority Gaps:")
        print(f"{'Rank':<5} {'Topic':<25} {'Score':<8} {'Interest':<10} {'Connections':<12}")
        print("-" * 70)
        
        for i, gap in enumerate(gaps[:top_n], 1):
            print(f"{i:<5} {gap['topic']:<25} {gap['score']:<8.1f} {gap['user_interest']:<10} {gap['connections']:<12}")
        
        # Show scoring breakdown for top 3
        print(f"\n" + "=" * 70)
        print("SCORING BREAKDOWN (Top 3)")
        print("=" * 70)
        
        for i, gap in enumerate(gaps[:3], 1):
            print(f"\n{i}. {gap['topic']}")
            print(f"   Score: {gap['score']}")
            print(f"   Mapped interest: {gap['mapped_interest'] or 'none'}")
            print(f"   User interest (freq): {gap['user_interest']}")
            print(f"   Connections: {gap['connections']}")
    else:
        print("\nNo gaps found above threshold!")

def main():
    parser = argparse.ArgumentParser(description='Priority gap analysis')
    parser.add_argument('--top', type=int, default=10, help='Show top N gaps (default: 10)')
    parser.add_argument('--threshold', type=float, default=0, help='Minimum score threshold')
    parser.add_argument('--weights', action='store_true', help='Show weight configuration')
    args = parser.parse_args()
    
    if args.weights:
        print("Gap Scoring Weights:")
        for name, weight in WEIGHTS.items():
            print(f"  {name}: {weight:.0%}")
        return
    
    gaps = analyze_gaps(min_score=args.threshold)
    print_report(gaps, top_n=args.top)
    
    # Save for other scripts
    output = WIKI_PATH / "scripts" / "priority_gaps.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(gaps, indent=2))
    print(f"\nSaved to {output}")

if __name__ == '__main__':
    main()
