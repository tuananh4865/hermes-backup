#!/opt/homebrew/bin/python3.14
"""
Weekly Digest — Auto-generate weekly summary of wiki activity

Usage:
    python3 weekly_digest.py
    python3 weekly_digest.py --days 7
    python3 weekly_digest.py --send-telegram
    python3 weekly_digest.py --save
"""

import argparse
import json
import re
import subprocess
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_TRANSCRIPTS = WIKI_PATH / "raw" / "transcripts"
DIGESTS_DIR = WIKI_PATH / "concepts" / "digests"

# ═══════════════════════════════════════════════════════════════

def get_recent_transcripts(days: int = 7) -> List[Dict]:
    """Get transcripts from last N days"""
    transcripts = []
    
    if not RAW_TRANSCRIPTS.exists():
        return transcripts
    
    cutoff = datetime.now() - timedelta(days=days)
    
    for date_dir in RAW_TRANSCRIPTS.iterdir():
        if not date_dir.is_dir():
            continue
        
        date_str = date_dir.name
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            if date < cutoff:
                continue
        except:
            continue
        
        for transcript_file in date_dir.glob("*.md"):
            try:
                content = transcript_file.read_text(encoding='utf-8')
                # Extract title from frontmatter
                title = date_str
                m = re.search(r'^title:\s*"([^"]+)"', content, re.MULTILINE)
                if m:
                    title = m.group(1)
                
                transcripts.append({
                    'file': str(transcript_file.relative_to(WIKI_PATH)),
                    'title': title,
                    'date': date_str,
                    'size': len(content)
                })
            except:
                pass
    
    return sorted(transcripts, key=lambda x: x['date'], reverse=True)

def extract_topics(transcripts: List[Dict]) -> Dict[str, int]:
    """Extract topics from recent transcripts"""
    from collections import Counter
    
    # Topic keywords
    TOPICS = {
        'lm-studio': ['lm studio', 'lm-studio', 'lmstudio'],
        'fine-tuning': ['fine-tune', 'finetune', 'lora'],
        'models': ['model', 'llm'],
        'wiki': ['wiki', 'knowledge base'],
        'github': ['github', 'git'],
        'automation': ['automation', 'script'],
        'project': ['project', 'task'],
        'hermes': ['hermes', 'agent'],
        'mlx': ['mlx'],
        'transcript': ['transcript'],
    }
    
    topic_counter = Counter()
    
    for transcript in transcripts:
        try:
            content = Path(WIKI_PATH / transcript['file']).read_text(encoding='utf-8')
            content_lower = content.lower()
            
            for topic, keywords in TOPICS.items():
                for kw in keywords:
                    if kw in content_lower:
                        topic_counter[topic] += 1
                        break
        except:
            pass
    
    return dict(topic_counter.most_common(10))

def get_wiki_changes(days: int = 7) -> Dict:
    """Get wiki changes from last N days"""
    changes = {
        'created': [],
        'modified': [],
        'deleted': []
    }
    
    # Use git to find changes
    try:
        since = (datetime.now() - timedelta(days=days)).strftime('%Y-%m-%d')
        
        result = subprocess.run(
            ['git', 'log', f'--since={since}', '--oneline', '--name-status'],
            capture_output=True,
            text=True,
            cwd=str(WIKI_PATH),
            timeout=10
        )
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('A\t'):
                    changes['created'].append(line[2:])
                elif line.startswith('M\t'):
                    changes['modified'].append(line[2:])
                elif line.startswith('D\t'):
                    changes['deleted'].append(line[2:])
    except:
        pass
    
    return changes

def run_scripts() -> Dict:
    """Run wiki health scripts and collect results"""
    results = {}
    
    scripts = [
        ('freshness', ['python3', 'scripts/freshness_score.py', '--stale-only']),
        ('quality', ['python3', 'scripts/wiki_self_critique.py', '--summary']),
    ]
    
    for name, cmd in scripts:
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(WIKI_PATH),
                timeout=60
            )
            results[name] = {
                'success': result.returncode == 0,
                'output': result.stdout[:500]
            }
        except Exception as e:
            results[name] = {'success': False, 'error': str(e)}
    
    return results

def generate_digest(days: int = 7) -> str:
    """Generate weekly digest content"""
    today = datetime.now()
    
    # Gather data
    transcripts = get_recent_transcripts(days)
    topics = extract_topics(transcripts)
    changes = get_wiki_changes(days)
    script_results = run_scripts()
    
    # Count stale pages
    stale_count = 0
    if script_results.get('freshness', {}).get('success'):
        output = script_results['freshness']['output']
        m = re.search(r'(\d+)\s+stale', output)
        if m:
            stale_count = int(m.group(1))
    
    # Build digest
    lines = [
        f"# Weekly Digest — {today.strftime('%Y-%m-%d')}",
        "",
        f"**Period:** Last {days} days",
        "",
        "## Topics Discussed",
        "",
    ]
    
    if topics:
        for topic, count in topics.items():
            lines.append(f"- **{topic}**: {count} conversations")
    else:
        lines.append("_No topics tracked_")
    
    lines.extend([
        "",
        "## Wiki Changes",
        "",
    ])
    
    created = [c for c in changes['created'] if c.endswith('.md') and not c.startswith('raw/')]
    modified = [c for c in changes['modified'] if c.endswith('.md') and not c.startswith('raw/')]
    
    if created:
        lines.append(f"**Created ({len(created)}):**")
        for c in created[:10]:
            lines.append(f"  - {c}")
        if len(created) > 10:
            lines.append(f"  - ... and {len(created) - 10} more")
    
    if modified:
        lines.append(f"\n**Modified ({len(modified)}):**")
        for c in modified[:10]:
            lines.append(f"  - {c}")
        if len(modified) > 10:
            lines.append(f"  - ... and {len(modified) - 10} more")
    
    if not created and not modified:
        lines.append("_No changes_")
    
    lines.extend([
        "",
        "## Wiki Health",
        "",
    ])
    
    if stale_count > 0:
        lines.append(f"- ⚠️ **{stale_count} stale pages** need refresh")
    else:
        lines.append("- ✅ **No stale pages**")
    
    lines.extend([
        "",
        "## Conversations",
        "",
    ])
    
    if transcripts:
        lines.append(f"_{len(transcripts)} conversations this period_")
        for t in transcripts[:5]:
            lines.append(f"- [[{t['file']}]] ({t['date']})")
    else:
        lines.append("_No conversations_")
    
    lines.extend([
        "",
        "---",
        f"*Generated: {today.isoformat()}*",
    ])
    
    return '\n'.join(lines)

def save_digest(digest: str, days: int = 7) -> Path:
    """Save digest to file"""
    today = datetime.now()
    filename = f"{today.strftime('%Y-%m-%d')}-weekly-digest.md"
    
    DIGESTS_DIR.mkdir(parents=True, exist_ok=True)
    
    filepath = DIGESTS_DIR / filename
    filepath.write_text(digest, encoding='utf-8')
    
    return filepath

def print_digest(digest: str):
    """Print digest to stdout"""
    print(digest)

def main():
    parser = argparse.ArgumentParser(description='Generate weekly wiki digest')
    parser.add_argument('--days', type=int, default=7, help='Days to summarize (default: 7)')
    parser.add_argument('--save', action='store_true', help='Save digest to wiki')
    parser.add_argument('--send-telegram', action='store_true', help='Send to Telegram (future)')
    args = parser.parse_args()
    
    digest = generate_digest(args.days)
    
    if args.save:
        filepath = save_digest(digest, args.days)
        print(f"Saved to {filepath}")
    else:
        print_digest(digest)

if __name__ == '__main__':
    main()
