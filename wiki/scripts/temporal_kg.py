#!/opt/homebrew/bin/python3.14
"""
Temporal Knowledge Graph — Track when knowledge was learned

Stores temporal metadata per topic:
- learned_at: When first added
- last_verified: Last time confirmed
- mention_count: How many times referenced
- relationships: Connections to other topics

Usage:
    python3 temporal_kg.py --learn topic-name
    python3 temporal_kg.py --timeline topic
    python3 temporal_kg.py --stale
    python3 temporal_kg.py --report
"""

import argparse
import json
import re
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
KG_FILE = WIKI_PATH / "scripts" / ".temporal_kg.json"

# ═══════════════════════════════════════════════════════════════

def load_kg() -> Dict:
    """Load knowledge graph"""
    if KG_FILE.exists():
        return json.loads(KG_FILE.read_text())
    return {
        'topics': {},
        'relationships': [],
        'last_updated': None
    }

def save_kg(kg: Dict):
    """Save knowledge graph"""
    kg['last_updated'] = datetime.now().isoformat()
    KG_FILE.parent.mkdir(parents=True, exist_ok=True)
    KG_FILE.write_text(json.dumps(kg, indent=2))

def slugify_topic(topic: str) -> str:
    """Normalize topic name"""
    return topic.lower().replace(' ', '-').replace('_', '-')

def add_topic(kg: Dict, topic: str, source: str = None, verified: bool = True):
    """Add or update a topic"""
    slug = slugify_topic(topic)
    now = datetime.now().isoformat()
    
    if slug not in kg['topics']:
        kg['topics'][slug] = {
            'learned_at': now,
            'last_verified': now,
            'first_source': source,
            'mention_count': 0,
            'aliases': [topic],
            'tags': []
        }
    else:
        kg['topics'][slug]['last_verified'] = now
        if topic not in kg['topics'][slug]['aliases']:
            kg['topics'][slug]['aliases'].append(topic)
    
    if verified:
        kg['topics'][slug]['mention_count'] = kg['topics'][slug].get('mention_count', 0) + 1
    
    return kg['topics'][slug]

def add_relationship(kg: Dict, from_topic: str, to_topic: str, rel_type: str = 'related'):
    """Add relationship between topics"""
    from_slug = slugify_topic(from_topic)
    to_slug = slugify_topic(to_topic)
    
    # Ensure both topics exist
    if from_slug not in kg['topics']:
        add_topic(kg, from_topic, verified=False)
    if to_slug not in kg['topics']:
        add_topic(kg, to_topic, verified=False)
    
    # Check if relationship exists
    for rel in kg['relationships']:
        if rel['from'] == from_slug and rel['to'] == to_slug:
            rel['strength'] = min(rel.get('strength', 1.0) + 0.1, 1.0)
            rel['last_seen'] = datetime.now().isoformat()
            return
    
    # Add new relationship
    kg['relationships'].append({
        'from': from_slug,
        'to': to_slug,
        'type': rel_type,
        'strength': 0.5,
        'learned_at': datetime.now().isoformat(),
        'last_seen': datetime.now().isoformat()
    })

def build_from_wiki(kg: Dict) -> Dict:
    """Build knowledge graph from wiki pages"""
    concepts_path = WIKI_PATH / "concepts"
    
    if not concepts_path.exists():
        return kg
    
    topics_found = set()
    
    for md_file in concepts_path.rglob("*.md"):
        if '_templates' in md_file.parts:
            continue
        
        try:
            content = md_file.read_text(encoding='utf-8')
            topic_name = md_file.stem
            
            # Add topic
            add_topic(kg, topic_name, source=str(md_file.relative_to(WIKI_PATH)))
            topics_found.add(slugify_topic(topic_name))
            
            # Extract wikilinks for relationships
            links = re.findall(r'\[\[([^\]|]+)', content)
            for link in links:
                link_slug = slugify_topic(link)
                if link_slug != slugify_topic(topic_name):  # No self-links
                    add_relationship(kg, topic_name, link)
                    topics_found.add(link_slug)
            
            # Extract frontmatter for tags
            if content.startswith('---'):
                end = content.find('---', 3)
                if end != -1:
                    fm_text = content[3:end]
                    tags_match = re.search(r'tags:\s*\[([^\]]+)\]', fm_text)
                    if tags_match:
                        tags = [t.strip() for t in tags_match.group(1).split(',')]
                        for tag in tags:
                            if tag and tag != 'untagged':
                                add_topic(kg, f"tag:{tag}", verified=False)
                                add_relationship(kg, topic_name, f"tag:{tag}", 'has_tag')
        except:
            pass
    
    return kg

def get_timeline(kg: Dict, topic: str) -> List[Dict]:
    """Get timeline for a topic"""
    slug = slugify_topic(topic)
    
    if slug not in kg['topics']:
        return []
    
    topic_data = kg['topics'][slug]
    
    timeline = [
        {'event': 'learned', 'date': topic_data['learned_at']},
        {'event': 'last_verified', 'date': topic_data['last_verified']},
    ]
    
    # Add relationship events
    for rel in kg['relationships']:
        if rel['from'] == slug or rel['to'] == slug:
            timeline.append({
                'event': f"related_to_{rel['to'] if rel['from'] == slug else rel['from']}",
                'date': rel['last_seen']
            })
    
    return sorted(timeline, key=lambda x: x['date'], reverse=True)

def get_stale_topics(kg: Dict, days: int = 30) -> List[Dict]:
    """Find topics not verified in N days"""
    stale = []
    cutoff = datetime.now() - timedelta(days=days)
    
    for slug, data in kg['topics'].items():
        last_verified = datetime.fromisoformat(data['last_verified'])
        if last_verified < cutoff:
            stale.append({
                'topic': slug,
                'last_verified': data['last_verified'],
                'days_ago': (datetime.now() - last_verified).days,
                'mentions': data.get('mention_count', 0)
            })
    
    stale.sort(key=lambda x: x['days_ago'], reverse=True)
    return stale

def get_related_topics(kg: Dict, topic: str, depth: int = 1) -> List[Dict]:
    """Get topics related to this topic"""
    slug = slugify_topic(topic)
    
    related = []
    for rel in kg['relationships']:
        if rel['from'] == slug:
            related.append({
                'topic': rel['to'],
                'strength': rel['strength'],
                'type': rel['type']
            })
        elif rel['to'] == slug:
            related.append({
                'topic': rel['from'],
                'strength': rel['strength'],
                'type': rel['type']
            })
    
    related.sort(key=lambda x: x['strength'], reverse=True)
    return related

def print_report(kg: Dict):
    """Print knowledge graph report"""
    print("=" * 70)
    print("TEMPORAL KNOWLEDGE GRAPH")
    print("=" * 70)
    
    print(f"\nTopics tracked: {len(kg['topics'])}")
    print(f"Relationships: {len(kg['relationships'])}")
    
    # Most mentioned
    mentioned = [(s, d) for s, d in kg['topics'].items() if d.get('mention_count', 0) > 0]
    mentioned.sort(key=lambda x: x[1].get('mention_count', 0), reverse=True)
    
    if mentioned[:5]:
        print(f"\nMost mentioned topics:")
        for slug, data in mentioned[:5]:
            print(f"  - {slug}: {data.get('mention_count', 0)} mentions")
    
    # Recently learned
    learned = sorted(kg['topics'].items(), key=lambda x: x[1]['learned_at'], reverse=True)
    if learned[:5]:
        print(f"\nRecently learned:")
        for slug, data in learned[:5]:
            print(f"  - {slug}: {data['learned_at'][:10]}")
    
    # Stale
    stale = get_stale_topics(kg, days=7)
    if stale:
        print(f"\nStale topics (7+ days):")
        for s in stale[:10]:
            print(f"  - {s['topic']}: {s['days_ago']} days ago")
    
    # Most connected
    connection_count = defaultdict(int)
    for rel in kg['relationships']:
        connection_count[rel['from']] += 1
        connection_count[rel['to']] += 1
    
    connected = sorted(connection_count.items(), key=lambda x: x[1], reverse=True)
    if connected[:5]:
        print(f"\nMost connected topics:")
        for slug, count in connected[:5]:
            print(f"  - {slug}: {count} connections")

def main():
    parser = argparse.ArgumentParser(description='Temporal knowledge graph')
    parser.add_argument('--build', action='store_true', help='Build kg from wiki')
    parser.add_argument('--learn', metavar='TOPIC', help='Learn a new topic')
    parser.add_argument('--timeline', metavar='TOPIC', help='Show topic timeline')
    parser.add_argument('--related', metavar='TOPIC', help='Show related topics')
    parser.add_argument('--stale', action='store_true', help='Show stale topics')
    parser.add_argument('--days', type=int, default=30, help='Stale threshold days')
    parser.add_argument('--report', action='store_true', help='Print full report')
    args = parser.parse_args()
    
    kg = load_kg()
    
    if args.build:
        kg = build_from_wiki(kg)
        save_kg(kg)
        print(f"Built KG with {len(kg['topics'])} topics and {len(kg['relationships'])} relationships")
        return
    
    if args.learn:
        add_topic(kg, args.learn)
        save_kg(kg)
        print(f"Learned: {args.learn}")
        return
    
    if args.timeline:
        timeline = get_timeline(kg, args.timeline)
        if timeline:
            print(f"\nTimeline for {args.timeline}:")
            for event in timeline:
                print(f"  [{event['date'][:10]}] {event['event']}")
        else:
            print(f"Topic not found: {args.timeline}")
        return
    
    if args.related:
        related = get_related_topics(kg, args.related)
        if related:
            print(f"\nRelated to {args.related}:")
            for r in related:
                print(f"  - {r['topic']} ({r['type']}, strength: {r['strength']:.2f})")
        else:
            print(f"No related topics found for: {args.related}")
        return
    
    if args.stale:
        stale = get_stale_topics(kg, days=args.days)
        if stale:
            print(f"\nStale topics ({args.days}+ days):")
            for s in stale:
                print(f"  - {s['topic']}: {s['days_ago']} days ago")
        else:
            print(f"No stale topics found")
        return
    
    if args.report:
        print_report(kg)
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()
