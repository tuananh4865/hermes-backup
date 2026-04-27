#!/opt/homebrew/bin/python3.14
"""
Transcript Summarizer — Progressive Summarization for Old Transcripts

Problem: Old transcripts (30+ days) still take full token space when building context.
Solution: Progressive summarization that compresses old transcripts.

Day 0-7:    Full transcript (raw/transcripts/{date}/)
Day 8-30:   Condensed (200 word summary + key decisions)
Day 31+:    Indexed only (title, date, key outcomes, linked concepts)
"""

import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
SUMMARIZED_DIR = WIKI_PATH / "raw" / ".summarized"


def extract_title(transcript_content: str) -> str:
    """Extract title from transcript"""
    # Try frontmatter first
    if transcript_content.startswith('---'):
        end = transcript_content.find('---', 3)
        if end != -1:
            fm_text = transcript_content[3:end]
            title_match = re.search(r'^title:\s*(.+)$', fm_text, re.MULTILINE)
            if title_match:
                return title_match.group(1).strip().strip('"\'')
    
    # Try first H1
    h1_match = re.search(r'^#\s+(.+)$', transcript_content, re.MULTILINE)
    if h1_match:
        return h1_match.group(1).strip()
    
    return "Untitled Transcript"


def extract_date(transcript_path: Path) -> str:
    """Extract date from filename or frontmatter"""
    # From filename: 2026-04-09-topic.md
    filename_match = re.search(r'(\d{4}-\d{2}-\d{2})', transcript_path.name)
    if filename_match:
        return filename_match.group(1)
    return ""


def extract_messages(transcript_content: str) -> List[Dict]:
    """Parse transcript into messages"""
    messages = []
    
    # Remove frontmatter
    if transcript_content.startswith('---'):
        end = transcript_content.find('---', 3)
        if end != -1:
            transcript_content = transcript_content[end+3:]
    
    # Split by message patterns
    # Pattern: "User/Assistant:" at start of line
    parts = re.split(r'^((?:User|Anh|Assistant|Em|Guest):?\s*)', 
                     transcript_content, 
                     flags=re.MULTILINE | re.IGNORECASE)
    
    # Reassemble messages
    i = 1
    while i < len(parts) - 1:
        role_marker = parts[i].strip().rstrip(':')
        content = parts[i + 1] if i + 1 < len(parts) else ""
        
        # Normalize role
        role = "user" if role_marker.lower() in ['user', 'anh'] else "assistant"
        
        messages.append({
            'role': role,
            'content': content.strip()
        })
        i += 2
    
    return messages


def extract_key_decisions(messages: List[Dict]) -> List[str]:
    """Extract key decisions from conversation"""
    decisions = []
    
    decision_patterns = [
        r'được rồi', r'okay', r'xong', r'done', r'xoá', r'xóa',
        r'✅', r'✓', r'confirm', r'approved', r'go ahead',
        r'commit', r'push', r'merge', r'fix', r'create', r'update'
    ]
    
    for msg in messages:
        content = msg['content'].lower()
        for pattern in decision_patterns:
            if pattern in content:
                # Extract the relevant line
                lines = msg['content'].split('\n')
                for line in lines:
                    if pattern in line.lower():
                        decisions.append(line.strip()[:100])
                        break
    
    return decisions[:10]  # Limit to 10


def extract_topics(messages: List[Dict]) -> List[str]:
    """Extract topics discussed"""
    topics = set()
    
    topic_keywords = [
        'wiki', 'lm studio', 'github', 'transcript', 'project',
        'automation', 'script', 'model', 'memory', 'knowledge',
        'refactor', 'cleanup', 'merge', 'fix', 'cron', 'hook'
    ]
    
    for msg in messages:
        content = msg['content'].lower()
        for topic in topic_keywords:
            if topic in content:
                topics.add(topic)
    
    return sorted(topics)


def extract_outcomes(messages: List[Dict]) -> List[str]:
    """Extract outcomes from conversation"""
    outcomes = []
    
    for msg in messages[-5:]:  # Last 5 messages often contain outcomes
        content = msg['content']
        if any(word in content.lower() for word in ['done', 'xong', 'finished', 'completed', '✅', '✓']):
            lines = content.split('\n')
            for line in lines[:3]:
                if len(line.strip()) > 10:
                    outcomes.append(line.strip()[:100])
                    break
    
    return outcomes[:5]


def extract_links(transcript_content: str) -> List[str]:
    """Extract wikilinks from transcript"""
    return re.findall(r'\[\[([^\]|]+)(?:\|[^\]]+)?\]\]', transcript_content)


def summarize_transcript(transcript_path: Path) -> Dict:
    """Generate condensed summary from full transcript"""
    content = transcript_path.read_text()
    
    messages = extract_messages(content)
    
    summary = {
        "title": extract_title(content),
        "date": extract_date(transcript_path),
        "key_decisions": extract_key_decisions(messages),
        "topics_discussed": extract_topics(messages),
        "outcomes": extract_outcomes(messages),
        "linked_concepts": extract_links(content),
        "message_count": len(messages),
        "word_count": len(content.split()),
        "summarized_at": datetime.now().isoformat()
    }
    
    return summary


def save_summary(transcript_path: Path, summary: Dict):
    """Save summary to .summarized directory"""
    summarized_dir = transcript_path.parent / ".summarized"
    summarized_dir.mkdir(parents=True, exist_ok=True)
    
    summary_file = summarized_dir / f"{transcript_path.stem}.summary"
    
    # Format as readable text
    lines = [
        f"# {summary['title']}",
        f"Date: {summary['date']}",
        f"Messages: {summary['message_count']} | Words: {summary['word_count']}",
        "",
        "## Topics",
        ", ".join(summary['topics_discussed']),
        "",
        "## Key Decisions",
    ]
    
    for decision in summary['key_decisions']:
        lines.append(f"- {decision}")
    
    lines.extend(["", "## Outcomes"])
    for outcome in summary['outcomes']:
        lines.append(f"- {outcome}")
    
    lines.extend(["", "## Linked Concepts"])
    for link in summary['linked_concepts']:
        lines.append(f"- [[{link}]]")
    
    lines.extend(["", f"_Summarized: {summary['summarized_at']}_"])
    
    summary_file.write_text('\n'.join(lines))
    print(f"✓ Summarized: {summary_file}")


def process_old_transcripts(days_threshold: int = 30) -> List[Path]:
    """Process transcripts older than threshold"""
    transcripts_path = WIKI_PATH / "raw" / "transcripts"
    if not transcripts_path.exists():
        return []
    
    processed = []
    cutoff = datetime.now() - timedelta(days=days_threshold)
    
    for transcript_file in transcripts_path.rglob("*.md"):
        # Skip summarized directory
        if ".summarized" in str(transcript_file):
            continue
        
        mtime = datetime.fromtimestamp(transcript_file.stat().st_mtime)
        if mtime < cutoff:
            # Check if already summarized
            summary_file = transcript_file.parent / ".summarized" / f"{transcript_file.stem}.summary"
            if not summary_file.exists():
                summary = summarize_transcript(transcript_file)
                save_summary(transcript_file, summary)
                processed.append(transcript_file)
    
    return processed


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description="Transcript Summarizer")
    parser.add_argument('--process-old', action='store_true',
                        help='Process transcripts older than 30 days')
    parser.add_argument('--days', type=int, default=30,
                        help='Days threshold for --process-old')
    parser.add_argument('file', nargs='?',
                        help='Specific transcript file to summarize')
    
    args = parser.parse_args()
    
    if args.file:
        transcript_path = Path(args.file)
        if transcript_path.exists():
            summary = summarize_transcript(transcript_path)
            print(f"Title: {summary['title']}")
            print(f"Date: {summary['date']}")
            print(f"Topics: {', '.join(summary['topics_discussed'])}")
            print(f"Decisions: {len(summary['key_decisions'])} found")
            print(f"Outcomes: {len(summary['outcomes'])} found")
            print(f"Links: {', '.join(summary['linked_concepts'])}")
        else:
            print(f"File not found: {transcript_path}")
    
    elif args.process_old:
        print(f"Processing transcripts older than {args.days} days...")
        processed = process_old_transcripts(args.days)
        print(f"✓ Processed {len(processed)} transcripts")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
