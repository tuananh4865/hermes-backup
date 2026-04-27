#!/opt/homebrew/bin/python3.14
"""
Email Auto-Ingest — Process emails forwarded to wiki email alias

Requires: imapclient, python-dateutil
pip install imapclient python-dateutil

Usage:
    python email_ingest.py
"""

import imaplib
import email
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from email.header import decode_header

# ═══════════════════════════════════════════════════════════════
# CONFIG — Edit these settings
# ═══════════════════════════════════════════════════════════════

IMAP_SERVER = "imap.gmail.com"  # or your IMAP provider
EMAIL = os.getenv("WIKI_EMAIL_USER", "your-email@gmail.com")
PASSWORD = os.getenv("WIKI_EMAIL_PASS", "")  # Use app password, not regular password
WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
RAW_PATH = WIKI_PATH / "raw" / "emails"

# Only process emails with this prefix in subject
SUBJECT_PREFIX = ["CLIP:", "WIKI:"]

# ═══════════════════════════════════════════════════════════════

def decode_str(s):
    """Decode email header string."""
    if s is None:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or 'utf-8', errors='ignore'))
        else:
            result.append(part)
    return ''.join(result)

def extract_urls(text):
    """Extract URLs from text."""
    url_pattern = re.compile(r'https?://[^\s<>"\_{}]+|www\.[^\s<>"\_{}]+')
    return url_pattern.findall(text)

def process_email(msg):
    """Process single email. Returns filepath if saved."""
    subject = decode_str(msg.get('Subject', 'No Subject'))
    sender = decode_str(msg.get('From', 'Unknown'))
    date_str = msg.get('Date', '')
    
    # Check prefix
    if not any(subject.startswith(p) for p in SUBJECT_PREFIX):
        return None
    
    # Get body
    body = ""
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            if content_type == "text/plain":
                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                break
    else:
        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
    
    # Extract URLs
    urls = extract_urls(body)
    
    if not urls:
        # No URLs, save anyway
        urls = ["No URL found"]
    
    # Create filename
    safe_subject = re.sub(r'[^\w\s-]', '', subject)[:50]
    filename = f"{datetime.now().strftime('%Y-%m-%d-%H%M%S')}-{safe_subject}.md"
    
    content = f"""---
category: "[[Email]]"
title: "{subject}"
clipped: {datetime.now().strftime('%Y-%m-%d')}
from: {sender}
date: {date_str}
tags: [email]
---

# {subject}

From: {sender}
Date: {date_str}

{"=" * 50}

URLs found:
{chr(10).join(f'- {url}' for url in urls)}

{"=" * 50}

Email Body:

{body[:2000]}{'...' if len(body) > 2000 else ''}
"""
    
    filepath = RAW_PATH / filename
    with open(filepath, 'w') as f:
        f.write(content)
    
    return filepath

def main():
    print(f"Email Auto-Ingest — {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Email: {EMAIL}")
    
    if not PASSWORD:
        print("ERROR: Set WIKI_EMAIL_PASS environment variable")
        print("  export WIKI_EMAIL_PASS='xxxx xxxx xxxx xxxx'")
        sys.exit(1)
    
    RAW_PATH.mkdir(parents=True, exist_ok=True)
    
    try:
        # Connect to IMAP
        mail = imaplib.IMAP4_SSL(IMAP_SERVER)
        mail.login(EMAIL, PASSWORD)
        mail.select('inbox')
        
        # Search for all emails (we'll filter by prefix in process_email)
        status, messages = mail.search(None, 'ALL')
        email_ids = messages[0].split()
        
        print(f"Found {len(email_ids)} total emails")
        
        saved = []
        for email_id in email_ids[-50:]:  # Check last 50 to avoid infinite loops
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            msg = email.message_from_bytes(msg_data[0][1])
            
            result = process_email(msg)
            if result:
                saved.append(result)
                print(f"  + {result.name}")
                # Mark as read
                mail.store(email_id, '+FLAGS', '\\Seen')
        
        mail.logout()
        
        print()
        if saved:
            print(f"Processed {len(saved)} emails")
            os.system(f'cd {WIKI_PATH} && git add raw/emails/ 2>/dev/null')
            os.system(f'cd {WIKI_PATH} && git commit -m "Email ingest: {len(saved)} new items" 2>/dev/null')
            os.system(f'cd {WIKI_PATH} && git push origin main 2>/dev/null')
        else:
            print("No new emails to process")
    
    except imaplib.IMAP4.error as e:
        print(f"IMAP Error: {e}")
        print("Check EMAIL/PASSWORD and IMAP settings")
        sys.exit(1)

if __name__ == "__main__":
    main()
