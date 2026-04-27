#!/opt/homebrew/bin/python3.14
"""
Realtime Transcript Handler — Wiki Brain

Appends conversation messages to wiki transcripts in real-time using local model.

Usage:
    python transcript_handler.py --add "message content" --topic "lm-studio"
    python transcript_handler.py --list
    python transcript_handler.py --view "2026-04-09-lm-studio"
"""

import argparse
import json
import re
import sys
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_TRANSCRIPT_PATH = WIKI_PATH / "raw" / "transcripts"
TRANSCRIPT_PATH = RAW_TRANSCRIPT_PATH  # Consolidated to raw/transcripts
INDEX_PATH = TRANSCRIPT_PATH / "index.md"
PROCESSED_PATH = WIKI_PATH / ".processed_transcripts"

# LM Studio API settings
LM_STUDIO_URL = "http://192.168.0.187:1234/v1"
API_KEY = "***"  # Dummy key for LM Studio

# Default model for wiki transcription
DEFAULT_MODEL = "qwen3.5-2b"

# Prompt template for transcript formatting
TRANSCRIPT_PROMPT = """Bạn là trợ lý ghi chép wiki. Chuyển đổi transcript dưới đây thành format wiki chuẩn.

## Yêu cầu
1. Tạo YAML frontmatter với: title, date, participants, topics, tags, summary
2. Giữ nguyên nội dung conversation theo format đẹp
3. Trích xuất topics/tags từ nội dung
4. Viết summary 1-2 câu về cuộc trò chuyện

## Rules
- Output ONLY the markdown. No intro text, no explanation.
- Tags: 3-5 relevant tags from content
- Summary: 1-2 sentences in Vietnamese
- Giữ nguyên nội dung của user và assistant

## Transcript:
{content}

## Output Format
```yaml
---
title: "[Topic Title]"
date: "{date}"
participants: [Anh, Em]
topics: [topic1, topic2, topic3]
tags: [tag1, tag2, tag3]
summary: "1-2 câu tóm tắt conversation"
---

# [Topic Title]

[Formatted conversation content]
```
"""

# ═══════════════════════════════════════════════════════════════
# PATH HELPERS
# ═══════════════════════════════════════════════════════════════

def get_topic_file(topic: str, date: str = None) -> Path:
    """Get file path for a topic. Merges if topic exists on same date."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    safe_topic = re.sub(r'[<>:"/\\|?*]', '-', topic.lower().strip())
    filename = f"{date}-{safe_topic}.md"
    
    return TRANSCRIPT_PATH / date / filename


def get_raw_file(topic: str, date: str = None) -> Path:
    """Get raw transcript file path."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    safe_topic = re.sub(r'[<>:"/\\|?*]', '-', topic.lower().strip())
    filename = f"{date}-{safe_topic}.md"
    
    return RAW_TRANSCRIPT_PATH / date / filename


def ensure_dirs():
    """Ensure required directories exist."""
    today = datetime.now().strftime('%Y-%m-%d')
    RAW_TRANSCRIPT_PATH.mkdir(exist_ok=True)
    TRANSCRIPT_PATH.mkdir(exist_ok=True)
    (TRANSCRIPT_PATH / today).mkdir(exist_ok=True, parents=True)
    (RAW_TRANSCRIPT_PATH / today).mkdir(exist_ok=True, parents=True)
    PROCESSED_PATH.mkdir(exist_ok=True)


# ═══════════════════════════════════════════════════════════════
# RAW TRANSCRIPT STORAGE
# ═══════════════════════════════════════════════════════════════

def append_to_raw(content: str, role: str, topic: str, date: str = None) -> Path:
    """Append a message to the raw transcript file."""
    ensure_dirs()
    raw_file = get_raw_file(topic, date)
    
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # Format role display
    role_display = "👤 Anh" if role == "user" else "🤖 Em"
    
    entry = f"\n[{timestamp}] {role_display}: {content}"
    
    with open(raw_file, 'a', encoding='utf-8') as f:
        f.write(entry)
    
    return raw_file


def get_raw_transcript(topic: str, date: str = None) -> str:
    """Read raw transcript content."""
    raw_file = get_raw_file(topic, date)
    if raw_file.exists():
        return raw_file.read_text(encoding='utf-8')
    return ""


# ═══════════════════════════════════════════════════════════════
# MODEL PROCESSING
# ═══════════════════════════════════════════════════════════════

def list_models() -> List[Dict]:
    """List available models in LM Studio."""
    try:
        response = requests.get(f"{LM_STUDIO_URL}/models", timeout=5)
        if response.status_code == 200:
            return response.json().get("data", [])
        return []
    except:
        return []


def format_transcript(raw_content: str, model: str, max_retries: int = 3) -> str:
    """Format raw transcript into wiki format using local model."""
    
    if not raw_content.strip():
        return None
    
    # Clean up raw content for processing
    clean_content = raw_content.strip()
    
    prompt = TRANSCRIPT_PROMPT.format(
        content=clean_content,
        date=datetime.now().strftime('%Y-%m-%d')
    )
    
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {API_KEY}"
    }
    
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 2000,
        "temperature": 0.3,
        "stream": False
    }
    
    for attempt in range(max_retries):
        try:
            response = requests.post(
                f"{LM_STUDIO_URL}/chat/completions",
                headers=headers,
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                result = response.json()
                content = result["choices"][0]["message"]["content"]
                
                # Extract just the markdown portion
                if "```yaml" in content:
                    start = content.find("```yaml") + 7
                    end = content.find("```", start)
                    if end > start:
                        content = content[start:end].strip()
                elif "```" in content:
                    start = content.find("```") + 3
                    end = content.rfind("```")
                    if end > start:
                        content = content[start:end].strip()
                
                return content
            
        except Exception as e:
            last_error = str(e)
            if attempt < max_retries - 1:
                import time
                time.sleep(2 ** attempt)
    
    raise Exception(f"Failed after {max_retries} attempts: {last_error}")


# ═══════════════════════════════════════════════════════════════
# PROCESSED TRANSCRIPT STORAGE
# ═══════════════════════════════════════════════════════════════

def save_formatted_transcript(formatted_content: str, topic: str, date: str = None) -> Path:
    """Save formatted transcript to wiki."""
    ensure_dirs()
    output_file = get_topic_file(topic, date)
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(formatted_content)
    
    return output_file


def mark_processed(topic: str, date: str = None):
    """Mark a transcript as processed."""
    ensure_dirs()
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    safe_topic = re.sub(r'[<>:"/\\|?*]', '-', topic.lower().strip())
    key = f"{date}-{safe_topic}"
    
    processed_file = PROCESSED_PATH / f"{key}.json"
    processed_file.write_text(json.dumps({
        'topic': topic,
        'date': date,
        'processed': datetime.now().isoformat()
    }))


def is_processed(topic: str, date: str = None) -> bool:
    """Check if a topic has been processed."""
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    safe_topic = re.sub(r'[<>:"/\\|?*]', '-', topic.lower().strip())
    key = f"{date}-{safe_topic}"
    
    processed_file = PROCESSED_PATH / f"{key}.json"
    return processed_file.exists()


# ═══════════════════════════════════════════════════════════════
# INDEX MANAGEMENT
# ═══════════════════════════════════════════════════════════════

def update_index(topic: str, date: str = None):
    """Update the transcripts index."""
    ensure_dirs()
    if date is None:
        date = datetime.now().strftime('%Y-%m-%d')
    
    safe_topic = re.sub(r'[<>:"/\\|?*]', '-', topic.lower().strip())
    filename = f"{date}-{safe_topic}.md"
    relative_path = f"raw/transcripts/{date}/{filename}"
    
    # Read existing index
    index_content = ""
    if INDEX_PATH.exists():
        index_content = INDEX_PATH.read_text(encoding='utf-8')
    
    # Check if entry already exists
    entry_link = f"- [[{topic}]] ({date})"
    if entry_link in index_content:
        return  # Already in index
    
    # Add new entry
    if index_content:
        # Find insertion point (after last entry, before footer)
        lines = index_content.split('\n')
        insert_idx = len(lines)
        for i, line in enumerate(lines):
            if line.startswith('---'):
                insert_idx = i + 1
                break
        
        new_lines = lines[:insert_idx] + [f"- [[{topic}]] ({date})"] + lines[insert_idx:]
        index_content = '\n'.join(new_lines)
    else:
        index_content = f"""---
title: "Transcript Index"
type: index
---

# Transcript Index

- [[{topic}]] ({date})
"""
    
    INDEX_PATH.write_text(index_content, encoding='utf-8')


# ═══════════════════════════════════════════════════════════════
# MAIN FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def add_message(content: str, role: str, topic: str, model: str = DEFAULT_MODEL, 
                auto_process: bool = True):
    """Add a message to transcript and optionally process."""
    
    # Append to raw transcript
    raw_file = append_to_raw(content, role, topic)
    print(f"Appended to raw: {raw_file.name}")
    
    # Check if should process
    if not auto_process:
        return raw_file
    
    # Check if already processed recently
    if is_processed(topic):
        print(f"Topic '{topic}' already processed. Run with --reprocess to update.")
        return raw_file
    
    # Get full raw content
    raw_content = get_raw_transcript(topic)
    
    if len(raw_content.split('\n')) < 3:
        print("Need more content before formatting...")
        return raw_file
    
    # Process with model
    print(f"Calling model {model}...")
    try:
        formatted = format_transcript(raw_content, model)
        if formatted:
            output_file = save_formatted_transcript(formatted, topic)
            mark_processed(topic)
            update_index(topic)
            print(f"Saved: {output_file.name}")
    except Exception as e:
        print(f"Processing error: {e}")
    
    return raw_file


def list_transcripts():
    """List all transcripts."""
    if not TRANSCRIPT_PATH.exists():
        print("No transcripts found.")
        return
    
    print("\n📚 Transcripts:\n")
    for date_dir in sorted(TRANSCRIPT_PATH.iterdir()):
        if date_dir.is_dir() and date_dir.name.startswith('202'):
            for f in sorted(date_dir.glob('*.md')):
                print(f"  {f.name}")
    print()


def view_transcript(name: str):
    """View a specific transcript."""
    # Try to find the file
    for date_dir in TRANSCRIPT_PATH.iterdir():
        if date_dir.is_dir():
            match = date_dir / f"{name}.md"
            if match.exists():
                print(match.read_text(encoding='utf-8'))
                return
            # Also try partial match
            for f in date_dir.glob(f"*{name}*.md"):
                print(f.read_text(encoding='utf-8'))
                return
    
    print(f"Transcript '{name}' not found.")


def reprocess_topic(topic: str, model: str = DEFAULT_MODEL):
    """Reprocess a topic from raw transcript."""
    raw_content = get_raw_transcript(topic)
    
    if not raw_content:
        print(f"No raw transcript found for '{topic}'")
        return
    
    print(f"Reprocessing '{topic}' with {model}...")
    try:
        formatted = format_transcript(raw_content, model)
        if formatted:
            output_file = save_formatted_transcript(formatted, topic)
            mark_processed(topic)
            update_index(topic)
            print(f"Updated: {output_file.name}")
    except Exception as e:
        print(f"Error: {e}")


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Wiki Transcript Handler')
    parser.add_argument('--add', help='Message content to add')
    parser.add_argument('--role', choices=['user', 'assistant'], default='assistant',
                        help='Role: user (Anh) or assistant (Em)')
    parser.add_argument('--topic', help='Topic name for the transcript')
    parser.add_argument('--list', action='store_true', help='List all transcripts')
    parser.add_argument('--view', metavar='NAME', help='View a specific transcript')
    parser.add_argument('--reprocess', metavar='TOPIC', help='Reprocess a topic')
    parser.add_argument('--model', default=DEFAULT_MODEL, help='Model to use')
    parser.add_argument('--no-auto-process', action='store_true', 
                        help='Skip auto-processing after adding')
    parser.add_argument('--raw', action='store_true', help='Show raw transcript')
    args = parser.parse_args()
    
    print("=" * 60)
    print("WIKI TRANSCRIPT HANDLER")
    print("=" * 60)
    
    if args.list:
        list_transcripts()
        return
    
    if args.view:
        view_transcript(args.view)
        return
    
    if args.reprocess:
        reprocess_topic(args.reprocess, args.model)
        return
    
    if args.add:
        if not args.topic:
            print("Error: --topic required when using --add")
            sys.exit(1)
        add_message(args.add, args.role, args.topic, args.model, 
                    not args.no_auto_process)
        return
    
    # Default: show help
    parser.print_help()


if __name__ == "__main__":
    main()
