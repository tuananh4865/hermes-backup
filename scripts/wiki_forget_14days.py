#!/usr/bin/env python3
"""
Wiki Memory Forget Script — Xóa những wiki/memory không được nhắc đến trong 14 ngày
"""
import sqlite3
import os
import re
from datetime import datetime, timedelta
from pathlib import Path

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
SESSION_DB = Path.home() / ".hermes" / "state.db"
HERMES_HOME = Path.home() / ".hermes"

def get_referenced_topics(days=14):
    """Extract topics mentioned in sessions from last N days"""
    if not SESSION_DB.exists():
        print(f"[WARN] Session DB not found: {SESSION_DB}")
        return set()
    
    cutoff = datetime.now() - timedelta(days=days)
    cutoff_ts = int(cutoff.timestamp())
    
    try:
        conn = sqlite3.connect(str(SESSION_DB))
        cur = conn.cursor()
        
        cur.execute("""
            SELECT content FROM messages 
            WHERE timestamp > ? AND role = 'user'
            ORDER BY timestamp DESC
        """, (cutoff_ts,))
        
        content = " ".join([row[0] or "" for row in cur.fetchall()])
        
        # Extract wiki page references
        wiki_refs = set()
        
        # Pattern: [[page-name]] or wiki/page-name.md or entities/name.md or concepts/name.md
        patterns = [
            r'\[\[([^\]]+)\]\]',  # [[page-name]]
            r'concepts/([a-z0-9\-]+)',  # concepts/name
            r'entities/([a-z0-9\-]+)',  # entities/name
            r'references/([a-z0-9\-]+)',  # references/name
            r'(?:concepts/|entities/|references/)([a-z0-9\-]+)',  # generic
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for m in matches:
                normalized = m.lower().replace(" ", "-")
                wiki_refs.add(normalized)
        
        conn.close()
        print(f"[INFO] Found {len(wiki_refs)} referenced topics in last {days} days")
        return wiki_refs
        
    except Exception as e:
        print(f"[ERROR] Failed to read session DB: {e}")
        return set()

def get_existing_wiki_topics():
    """Get all existing wiki topics"""
    topics = set()
    
    if WIKI_PATH.exists():
        for folder in ['concepts', 'entities', 'references', 'projects']:
            folder_path = WIKI_PATH / folder
            if folder_path.exists():
                for f in folder_path.glob("*.md"):
                    topics.add(f.stem.lower())
                for f in folder_path.glob("*"):
                    if f.is_dir() and not f.name.startswith('.'):
                        topics.add(f.name.lower())
    
    return topics

def get_memory_files():
    """Get all memory files"""
    memory_files = set()
    
    for folder in ['memories', 'workers']:
        folder_path = HERMES_HOME / folder
        if folder_path.exists():
            for f in folder_path.rglob("*.md"):
                memory_files.add(str(f))
    
    return memory_files

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] === Wiki Memory Forget (14 days) ===")
    
    # Get referenced topics
    referenced = get_referenced_topics(days=14)
    print(f"[INFO] Referenced topics: {len(referenced)}")
    
    # Get existing wiki topics
    existing = get_existing_wiki_topics()
    print(f"[INFO] Existing wiki topics: {len(existing)}")
    
    # Find stale topics (not referenced in 14 days)
    stale = existing - referenced
    print(f"[INFO] Stale topics: {len(stale)}")
    
    return stale

def delete_stale_topics(stale):
    """Delete stale wiki topics"""
    deleted = []
    errors = []
    
    for topic in stale:
        for folder in ['concepts', 'entities', 'references', 'projects']:
            folder_path = WIKI_PATH / folder
            # Try exact match
            for ext in ['', '.md']:
                f = folder_path / f"{topic}{ext}"
                if f.exists():
                    try:
                        os.remove(f)
                        deleted.append(str(f))
                        print(f"[DELETE] {f}")
                    except Exception as e:
                        errors.append((str(f), str(e)))
    
    return deleted, errors

def main():
    print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] === Wiki Memory Forget (14 days) ===")
    
    delete_mode = os.environ.get("DELETE_MODE", "false").lower() == "true"
    
    if not delete_mode:
        print("[INFO] Dry-run mode (DELETE_MODE not set)")
    else:
        print("[WARN] DELETE MODE ENABLED — will delete stale content")
    
    # Get referenced topics
    referenced = get_referenced_topics(days=14)
    print(f"[INFO] Referenced topics: {len(referenced)}")
    
    # Get existing wiki topics
    existing = get_existing_wiki_topics()
    print(f"[INFO] Existing wiki topics: {len(existing)}")
    
    # Find stale topics (not referenced in 14 days)
    stale = existing - referenced
    print(f"[INFO] Stale topics to forget: {len(stale)}")
    
    if stale:
        print("\n[STALE TOPICS]:")
        for topic in sorted(stale):
            print(f"  - {topic}")
    
    if delete_mode and stale:
        print("\n[DELETING...]")
        deleted, errors = delete_stale_topics(stale)
        print(f"\n[DONE] Deleted {len(deleted)} files, {len(errors)} errors")
        for f, e in errors:
            print(f"  [ERROR] {f}: {e}")
        
        # Log to file
        log_path = HERMES_HOME / "cron" / "output" / f"wiki_forget_{datetime.now().strftime('%Y-%m-%d')}.md"
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "w") as f:
            f.write(f"# Wiki Forget Report — {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n")
            f.write(f"Referenced: {len(referenced)} topics\n")
            f.write(f"Deleted: {len(deleted)} stale topics\n\n")
            f.write("## Deleted:\n")
            for d in deleted:
                f.write(f"- {d}\n")
            if errors:
                f.write("\n## Errors:\n")
                for fn, e in errors:
                    f.write(f"- {fn}: {e}\n")
        print(f"[LOG] Saved to {log_path}")
    else:
        print("\n[DONE] Dry-run complete. Set DELETE_MODE=true to delete.")
    
    return stale


if __name__ == "__main__":
    main()

