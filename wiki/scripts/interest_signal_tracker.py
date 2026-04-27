#!/opt/homebrew/bin/python3.14
"""
Interest Signal Tracker — Track user interest signals from transcripts

Tracks:
- Topic frequency: How often does user ask about each topic
- Recent mentions: Topics mentioned in last 7 days
- Questions asked: Explicit questions
- Corrections: User corrections (high signal)

Usage:
    python3 interest_signal_tracker.py --track
    python3 interest_signal_tracker.py --report
    python3 interest_signal_tracker.py --top 10
"""

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_TRANSCRIPTS = WIKI_PATH / "raw" / "transcripts"
SIGNALS_FILE = WIKI_PATH / "scripts" / ".interest_signals.json"

# Topic keywords for detection
TOPIC_KEYWORDS = {
    'lm-studio': ['lm studio', 'lm-studio', 'lmstudio', 'lm studio'],
    'fine-tuning': ['fine-tune', 'finetune', 'fine tune', 'lora', 'qlora'],
    'models': ['model', 'llm', 'gpt', 'claude'],
    'mlx': ['mlx', 'apple silicon', 'mps'],
    'github': ['github', 'git', 'commit', 'branch'],
    'automation': ['automation', 'script', 'cron', 'watchdog'],
    'wiki': ['wiki', 'knowledge base', 'knowledge-base'],
    'transcript': ['transcript', 'conversation'],
    'hermes': ['hermes', 'agent', 'mcp'],
    'browser': ['browser', 'web', 'scrape'],
    'project': ['project', 'task', 'phase'],
    'mistake': ['mistake', 'bug', 'error', 'fix'],
    'retrospective': ['retro', 'lessons', 'review'],
    'paper': ['paper', 'research', 'arxiv'],
    'article': ['article', 'blog', 'post'],
    'rss': ['rss', 'feed'],
    'email': ['email', 'mail'],
    'whisper': ['whisper', 'transcribe', 'speech'],
    'attention': ['attention', 'transformer', 'self-attention'],
    'embedding': ['embedding', 'vector', 'similarity'],
}

# Correction patterns
CORRECTION_PATTERNS = [
    r'không phải',
    r'sai rồi',
    r'nhầm',
    r'chờ|đợi',
    r'em hiểu sai',
    r'không đúng',
    r'sửa',
    r'đừng',
    r'đợi đã',
]

# Question patterns
QUESTION_PATTERNS = [
    r'\?$',
    r'^.*\?\s',
    r'là gì',
    r'làm sao',
    r'có cách nào',
    r'how to',
    r'what is',
    r'how do',
    r'can i',
    r'thiếu',
]

# ═══════════════════════════════════════════════════════════════

def load_signals() -> Dict:
    """Load existing signals"""
    if SIGNALS_FILE.exists():
        return json.loads(SIGNALS_FILE.read_text())
    return {
        'topic_frequency': {},
        'topic_dates': {},
        'questions': [],
        'corrections': [],
        'last_updated': None
    }

def save_signals(signals: Dict):
    """Save signals"""
    signals['last_updated'] = datetime.now().isoformat()
    SIGNALS_FILE.parent.mkdir(parents=True, exist_ok=True)
    SIGNALS_FILE.write_text(json.dumps(signals, indent=2))

def extract_topics(text: str) -> List[str]:
    """Extract topics from text using keywords"""
    text = text.lower()
    found_topics = []
    
    for topic, keywords in TOPIC_KEYWORDS.items():
        for keyword in keywords:
            if keyword in text:
                found_topics.append(topic)
                break
    
    return found_topics

def detect_corrections(text: str) -> List[Dict]:
    """Detect user corrections in text"""
    corrections = []
    lines = text.split('\n')
    
    for i, line in enumerate(lines):
        line_lower = line.lower()
        for pattern in CORRECTION_PATTERNS:
            if re.search(pattern, line_lower):
                corrections.append({
                    'text': line.strip()[:100],
                    'line': i,
                    'pattern': pattern
                })
                break
    
    return corrections

def detect_questions(text: str) -> List[str]:
    """Detect explicit questions"""
    questions = []
    lines = text.split('\n')
    
    for line in lines:
        line_lower = line.lower()
        for pattern in QUESTION_PATTERNS:
            if re.search(pattern, line_lower):
                questions.append(line.strip()[:100])
                break
    
    return questions

def parse_transcript(filepath: Path) -> Dict:
    """Parse a transcript file"""
    try:
        content = filepath.read_text(encoding='utf-8')
    except:
        return {'topics': [], 'questions': [], 'corrections': []}
    
    # Remove frontmatter
    if content.startswith('---'):
        end = content.find('---', 3)
        if end != -1:
            content = content[end+3:]
    
    # Only look at user messages
    user_lines = []
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if '👤' in line or 'User:' in line or re.match(r'^[^:#]+:', line):
            # Extract message content
            msg = re.sub(r'^[^\n]*:', '', line)
            user_lines.append(msg)
    
    user_text = ' '.join(user_lines)
    
    return {
        'topics': extract_topics(user_text),
        'questions': detect_questions(user_text),
        'corrections': detect_corrections(user_text)
    }

def track_signals(days: int = 30) -> Dict:
    """Track interest signals from recent transcripts"""
    signals = load_signals()
    
    if not RAW_TRANSCRIPTS.exists():
        print("No transcripts found")
        return signals
    
    # Get recent transcripts
    cutoff = datetime.now() - timedelta(days=days)
    recent_files = []
    
    for date_dir in RAW_TRANSCRIPTS.iterdir():
        if date_dir.is_dir():
            for transcript_file in date_dir.glob("*.md"):
                mtime = datetime.fromtimestamp(transcript_file.stat().st_mtime)
                if mtime >= cutoff:
                    recent_files.append(transcript_file)
    
    print(f"Processing {len(recent_files)} recent transcripts...")
    
    # Aggregate signals
    topic_counter = Counter()
    topic_dates = defaultdict(list)
    all_questions = []
    all_corrections = []
    
    for transcript_file in recent_files:
        parsed = parse_transcript(transcript_file)
        
        # Track topics
        for topic in parsed['topics']:
            topic_counter[topic] += 1
            topic_dates[topic].append(transcript_file.stat().st_mtime)
        
        # Track questions
        all_questions.extend(parsed['questions'])
        
        # Track corrections
        all_corrections.extend(parsed['corrections'])
    
    # Update signals
    signals['topic_frequency'] = dict(topic_counter)
    signals['topic_dates'] = {k: max(v) for k, v in topic_dates.items()}
    signals['questions'] = all_questions[:50]  # Keep last 50
    signals['corrections'] = all_corrections[:50]
    
    save_signals(signals)
    
    return signals

def get_top_interests(signals: Dict, days: int = 30, top_n: int = 10) -> List[Dict]:
    """Get top interests weighted by recency and frequency"""
    if not signals.get('topic_frequency'):
        return []
    
    now = datetime.now()
    cutoff = now - timedelta(days=days)
    
    interests = []
    for topic, freq in signals['topic_frequency'].items():
        last_mentioned = signals['topic_dates'].get(topic)
        if last_mentioned:
            last_mentioned = datetime.fromtimestamp(last_mentioned)
            days_since = (now - last_mentioned).days
        else:
            days_since = 999
        
        # Calculate score
        # Frequency: 0-40 points
        freq_score = min(freq * 5, 40)
        
        # Recency: 0-30 points (decays after 7 days)
        if days_since <= 7:
            recency_score = 30
        elif days_since <= 14:
            recency_score = 20
        elif days_since <= 30:
            recency_score = 10
        else:
            recency_score = 0
        
        # Fresh signal bonus: 0-30 points
        fresh_bonus = 30 if days_since <= 7 else 0
        
        total_score = freq_score + recency_score + fresh_bonus
        
        interests.append({
            'topic': topic,
            'frequency': freq,
            'days_since': days_since,
            'score': total_score,
            'last_mentioned': last_mentioned.strftime('%Y-%m-%d') if last_mentioned else 'unknown'
        })
    
    # Sort by score
    interests.sort(key=lambda x: x['score'], reverse=True)
    
    return interests[:top_n]

def report(signals: Dict):
    """Print signal report"""
    print("=" * 60)
    print("INTEREST SIGNALS REPORT")
    print("=" * 60)
    
    if signals.get('last_updated'):
        print(f"Last updated: {signals['last_updated']}")
    
    print(f"\nTotal topics tracked: {len(signals.get('topic_frequency', {}))}")
    
    # Top interests
    top = get_top_interests(signals, top_n=10)
    if top:
        print(f"\nTop Interests (by score):")
        for i, item in enumerate(top, 1):
            print(f"  {i}. {item['topic']}: score={item['score']}, freq={item['frequency']}, days_since={item['days_since']}")
    
    # Corrections
    corrections = signals.get('corrections', [])
    if corrections:
        print(f"\nRecent Corrections ({len(corrections)}):")
        for c in corrections[:5]:
            print(f"  - {c['text'][:60]}...")
    
    # Questions
    questions = signals.get('questions', [])
    if questions:
        print(f"\nRecent Questions ({len(questions)}):")
        for q in questions[:5]:
            print(f"  - {q[:60]}...")

def main():
    parser = argparse.ArgumentParser(description='Track user interest signals')
    parser.add_argument('--track', action='store_true', help='Track signals from transcripts')
    parser.add_argument('--days', type=int, default=30, help='Days to look back (default: 30)')
    parser.add_argument('--report', action='store_true', help='Print signal report')
    parser.add_argument('--top', type=int, help='Show top N interests')
    args = parser.parse_args()
    
    signals = load_signals()
    
    if args.track:
        signals = track_signals(args.days)
        print(f"Tracked signals from {args.days} days")
        report(signals)
        return
    
    if args.report:
        report(signals)
        return
    
    if args.top:
        top = get_top_interests(signals, top_n=args.top)
        print(f"Top {args.top} Interests:")
        for i, item in enumerate(top, 1):
            print(f"  {i}. {item['topic']} (score={item['score']}, freq={item['frequency']}, last={item['last_mentioned']})")
        return
    
    parser.print_help()

if __name__ == '__main__':
    main()
