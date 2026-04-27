#!/opt/homebrew/bin/python3.14
"""
Correction Detector — Detect and learn from user corrections

When user corrects the AI, this tracks:
- What was corrected
- Which page was wrong
- Pattern detection (repeated mistakes)

Usage:
    python3 correction_detector.py --session session_id
    python3 correction_detector.py --report
    python3 correction_detector.py --track
"""

import argparse
import json
import re
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
CORRECTIONS_FILE = WIKI_PATH / "scripts" / ".corrections.json"
TRANSCRIPTS_PATH = WIKI_PATH / "raw" / "transcripts"

# Correction patterns (Vietnamese + English)
CORRECTION_PATTERNS = [
    # Vietnamese
    (r'không phải', 'negation'),
    (r'sai rồi', 'error'),
    (r'nhầm', 'mistake'),
    (r'chờ|đợi', 'wait'),
    (r'không đúng', 'incorrect'),
    (r'em hiểu sai', 'misunderstanding'),
    (r'sửa', 'fix'),
    (r'đừng', 'dont'),
    (r'đợi đã', 'wait'),
    (r'anh muốn', 'preference'),
    (r'không cần', 'unnecessary'),
    (r'bỏ', 'remove'),
    (r'thừa', 'extra'),
    (r'thiếu', 'missing'),
    (r'chưa', 'not_yet'),
    # English
    (r'not quite', 'error'),
    (r'that\'s wrong', 'error'),
    (r'incorrect', 'incorrect'),
    (r'mistake', 'mistake'),
    (r'fix this', 'fix'),
    (r'wait', 'wait'),
    (r'no,? actually', 'correction'),
]

# Topic extraction patterns
TOPIC_PATTERNS = [
    (r'(?:về|about|concerning)\s+(\w+)', 'topic'),
    (r'(?:trên|dưới|trong|at|in)\s+(?:wiki|github|git|lm[- ]?studio)', 'system'),
    (r'model', 'models'),
    (r'fine[- ]?tune', 'fine-tuning'),
    (r'LM Studio', 'lm-studio'),
    (r'(?:tạo|mở|xóa|hành động)', 'action'),
]

# ═══════════════════════════════════════════════════════════════

def load_corrections() -> Dict:
    """Load existing corrections"""
    if CORRECTIONS_FILE.exists():
        return json.loads(CORRECTIONS_FILE.read_text())
    return {
        'corrections': [],
        'mistake_patterns': {},
        'page_quality_impact': {},
        'last_updated': None
    }

def save_corrections(data: Dict):
    """Save corrections data"""
    data['last_updated'] = datetime.now().isoformat()
    CORRECTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
    CORRECTIONS_FILE.write_text(json.dumps(data, indent=2))

def extract_topic(text: str) -> Optional[str]:
    """Extract topic from correction text"""
    text_lower = text.lower()
    
    # Look for topic keywords
    topic_keywords = {
        'lm-studio': ['lm studio', 'lm-studio', 'lmstudio'],
        'fine-tuning': ['fine-tune', 'finetune', 'fine tune'],
        'models': ['model', 'models'],
        'github': ['github', 'git'],
        'wiki': ['wiki'],
        'transcript': ['transcript'],
        'project': ['project'],
        'script': ['script'],
        'automation': ['automation'],
    }
    
    for topic, keywords in topic_keywords.items():
        for kw in keywords:
            if kw in text_lower:
                return topic
    
    # Try to extract noun after preposition
    for pattern, _ in TOPIC_PATTERNS:
        m = re.search(pattern, text_lower)
        if m:
            return m.group(1)
    
    return None  # Return None if no topic found

def detect_correction_type(text: str) -> str:
    """Detect type of correction"""
    text_lower = text.lower()
    
    for pattern, ctype in CORRECTION_PATTERNS:
        if re.search(pattern, text_lower):
            return ctype
    
    return 'unknown'

def extract_corrected_info(text: str) -> Dict:
    """Extract what was corrected"""
    info = {
        'original_claim': '',
        'corrected_to': '',
        'topic': extract_topic(text),
        'type': detect_correction_type(text)
    }
    
    # Try to extract "X -> Y" pattern
    m = re.search(r'([^.!?]+)\s*(?:->|→)\s*([^.!?]+)', text)
    if m:
        info['original_claim'] = m.group(1).strip()
        info['corrected_to'] = m.group(2).strip()
    
    return info

def process_transcript(filepath: Path) -> List[Dict]:
    """Find corrections in a transcript"""
    corrections = []
    
    try:
        content = filepath.read_text(encoding='utf-8')
    except:
        return corrections
    
    # Remove frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            content = content[end+3:]
    
    lines = content.split('\n')
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        
        # Check each correction pattern
        for pattern, _ in CORRECTION_PATTERNS:
            if re.search(pattern, line_lower):
                # Found a correction
                correction = {
                    'text': line.strip()[:200],
                    'line': i,
                    'type': _,
                    'pattern': pattern,
                    'topic': extract_topic(line),
                    'timestamp': datetime.fromtimestamp(filepath.stat().st_mtime).isoformat()
                }
                corrections.append(correction)
                break
    
    return corrections

def track_corrections(days: int = 30) -> Dict:
    """Track corrections from recent transcripts"""
    data = load_corrections()
    
    if not TRANSCRIPTS_PATH.exists():
        print("No transcripts found")
        return data
    
    from datetime import timedelta
    cutoff = datetime.now() - timedelta(days=days)
    
    # Find recent transcripts
    recent_files = []
    for date_dir in TRANSCRIPTS_PATH.iterdir():
        if date_dir.is_dir():
            for transcript_file in date_dir.glob("*.md"):
                mtime = datetime.fromtimestamp(transcript_file.stat().st_mtime)
                if mtime >= cutoff:
                    recent_files.append(transcript_file)
    
    print(f"Processing {len(recent_files)} transcripts...")
    
    new_corrections = []
    topic_counter = Counter()
    type_counter = Counter()
    
    for transcript_file in recent_files:
        found = process_transcript(transcript_file)
        new_corrections.extend(found)
        
        for c in found:
            if c['topic']:  # Only count if topic was identified
                topic_counter[c['topic']] += 1
            type_counter[c['type']] += 1
    
    # Update corrections
    data['corrections'] = (data.get('corrections', []) + new_corrections)[-100:]  # Keep last 100
    
    # Update patterns
    for topic, count in topic_counter.items():
        if topic not in data['mistake_patterns']:
            data['mistake_patterns'][topic] = 0
        data['mistake_patterns'][topic] += count
    
    # Update page quality impact (corrections lower quality)
    for c in new_corrections:
        topic = c['topic']
        if topic not in data['page_quality_impact']:
            data['page_quality_impact'][topic] = {'corrections': 0, 'last_corrected': None}
        data['page_quality_impact'][topic]['corrections'] += 1
        data['page_quality_impact'][topic]['last_corrected'] = c['timestamp']
    
    save_corrections(data)
    
    return data

def find_repeated_mistakes(data: Dict) -> List[Dict]:
    """Find topics that are repeatedly corrected"""
    patterns = data.get('mistake_patterns', {})
    quality = data.get('page_quality_impact', {})
    
    repeated = []
    for topic, count in patterns.items():
        if count >= 2:  # Corrected 2+ times
            q = quality.get(topic, {})
            repeated.append({
                'topic': topic,
                'count': count,
                'quality_impact': q.get('corrections', 0),
                'last_corrected': q.get('last_corrected', 'unknown')
            })
    
    repeated.sort(key=lambda x: x['count'], reverse=True)
    return repeated

def get_quality_scores(data: Dict) -> Dict[str, float]:
    """Get adjusted quality scores based on corrections"""
    base_score = 10.0
    quality_impact = data.get('page_quality_impact', {})
    
    adjusted = {}
    for topic, info in quality_impact.items():
        corrections = info.get('corrections', 0)
        # Each correction reduces quality by 0.5
        adjusted[topic] = max(1.0, base_score - corrections * 0.5)
    
    return adjusted

def report(data: Dict):
    """Print correction report"""
    print("=" * 60)
    print("CORRECTION DETECTION REPORT")
    print("=" * 60)
    
    if data.get('last_updated'):
        print(f"Last updated: {data['last_updated']}")
    
    corrections = data.get('corrections', [])
    print(f"\nTotal corrections tracked: {len(corrections)}")
    
    # By topic
    patterns = data.get('mistake_patterns', {})
    if patterns:
        print(f"\nCorrections by Topic:")
        for topic, count in sorted(patterns.items(), key=lambda x: x[1], reverse=True)[:10]:
            print(f"  {topic}: {count}")
    
    # By type
    type_counts = Counter()
    for c in corrections:
        type_counts[c['type']] += 1
    if type_counts:
        print(f"\nCorrections by Type:")
        for ctype, count in type_counts.most_common(10):
            print(f"  {ctype}: {count}")
    
    # Repeated mistakes
    repeated = find_repeated_mistakes(data)
    if repeated:
        print(f"\nRepeated Mistakes (2+ times):")
        for r in repeated[:5]:
            print(f"  {r['topic']}: {r['count']} corrections")
    
    # Quality impact
    quality = get_quality_scores(data)
    low_quality = [(t, s) for t, s in quality.items() if s < 8.0]
    if low_quality:
        print(f"\nPages with Quality Impact:")
        for topic, score in low_quality[:10]:
            print(f"  {topic}: {score:.1f}/10")
    
    # Recent corrections
    if corrections:
        print(f"\nRecent Corrections:")
        for c in corrections[-5:]:
            print(f"  [{c['type']}] {c['text'][:60]}...")

def main():
    parser = argparse.ArgumentParser(description='Detect and learn from user corrections')
    parser.add_argument('--track', action='store_true', help='Track corrections from recent transcripts')
    parser.add_argument('--days', type=int, default=30, help='Days to look back (default: 30)')
    parser.add_argument('--report', action='store_true', help='Print correction report')
    parser.add_argument('--repeated', action='store_true', help='Show only repeated mistakes')
    args = parser.parse_args()
    
    data = load_corrections()
    
    if args.track:
        data = track_corrections(args.days)
        report(data)
        return
    
    if args.report:
        report(data)
        return
    
    if args.repeated:
        repeated = find_repeated_mistakes(data)
        if repeated:
            print("Repeated Mistakes:")
            for r in repeated:
                print(f"  {r['topic']}: {r['count']} corrections, last: {r['last_corrected']}")
        else:
            print("No repeated mistakes found")
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()
