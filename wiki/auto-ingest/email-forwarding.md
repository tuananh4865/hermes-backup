---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 Email (extracted)
  - 🔗 rss (extracted)
  - 🔗 automation (extracted)
relationship_count: 3
---

# Email Auto-Ingest Setup

## Overview

```
Any Email with Link → Forward to wiki@domain → Auto-save to raw/emails/
```

## Option A: Email Alias (Simplest)

### Step 1: Create Email Alias
In your email provider (Gmail, iCloud, Fastmail):

1. **Gmail**: Settings → See all settings → Filters → Create filter
2. **iCloud**: Create email alias in iCloud settings
3. **Fastmail**: Settings → Custom email addresses

Example: `wiki.anhtuan@gmail.com` or `wiki@anhtuan.io`

### Step 2: Create Filter/Rule
Create rule to auto-label (not auto-forward):
- **If**: Subject contains "CLIP:" or "WIKI:"
- **Then**: Add label "Wiki-Inbox", Mark as important

### Step 3: Forward to Yourself
Use your main email → Forward to the alias when you want to clip.

### Step 4: iOS Shortcut to Process
1. Create Shortcut: "Process Wiki Email"
2. When you forward email to wiki alias:
   - Shortcut detects new email with "CLIP:" prefix
   - Extracts URL from email body
   - Saves to `raw/emails/{date}-{subject}.md`
   - Git commits

---

## Option B: Dedicated Wiki Email (More Robust)

### Step 1: Set Up Dedicated Email
Register: `wiki@yourdomain.com` (costs ~$1/month)

Services:
- **Fastmail** ($3/month) - Best for privacy
- **Google Workspace** ($6/month) - If using Gmail
- **Cloudflare Email** (free) - Forward-only

### Step 2: Create Processing Script

```python
#!/usr/bin/env python3
"""
email_ingest.py - Process emails forwarded to wiki email
Requires: imapclient, python-dateutil
pip install imapclient python-dateutil
"""

import imaplib
import email
from email.header import decode_header
import os
from datetime import datetime
from pathlib import Path
import re

# Configuration
IMAP_SERVER = "imap.gmail.com"  # or your provider
EMAIL = "your-wiki-email@gmail.com"
PASSWORD = "your-app-password"  # Generate in: Google Account → Security → App Passwords
WIKI_PATH = Path.home() / "wiki"
RAW_PATH = WIKI_PATH / "raw" / "emails"

def decode_str(s):
    """Decode email header string"""
    if s is None:
        return ""
    parts = decode_header(s)
    result = []
    for part, enc in parts:
        if isinstance(part, bytes):
            result.append(part.decode(enc or 'utf-8'))
        else:
            result.append(part)
    return ''.join(result)

def extract_urls(text):
    """Extract URLs from text"""
    url_pattern = re.compile(r'https?://[^\s<>"{}|\\^`\[\]]+')
    return url_pattern.findall(text)

def process_email(msg):
    """Process single email"""
    subject = decode_str(msg.get('Subject', 'No Subject'))
    sender = decode_str(msg.get('From', 'Unknown'))
    date = msg.get('Date', '')
    
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
        return None
    
    # Create markdown file
    filename = datetime.now().strftime("%Y-%m-%d-%H%M%S")
    safe_subject = re.sub(r'[^\w\s-]', '', subject)[:50]
    filename = f"{filename}-{safe_subject}.md"
    
    content = f"""---
category: "[[Email]]"
title: "{subject}"
source: {urls[0] if urls else 'No URL'}
clipped: {datetime.now().strftime("%Y-%m-%d")}
from: {sender}
date: {date}
tags: [email]
---

# {subject}

From: {sender}
Date: {date}

{"=" * 50}

Original URLs:
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
    """Main loop"""
    RAW_PATH.mkdir(parents=True, exist_ok=True)
    
    # Connect to IMAP
    mail = imaplib.IMAP4_SSL(IMAP_SERVER)
    mail.login(EMAIL, PASSWORD)
    mail.select('inbox')
    
    # Search for unseen emails
    status, messages = mail.search(None, 'UNSEEN')
    email_ids = messages[0].split()
    
    print(f"Found {len(email_ids)} new emails")
    
    saved = []
    for email_id in email_ids:
        status, msg_data = mail.fetch(email_id, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])
        
        result = process_email(msg)
        if result:
            saved.append(result)
            print(f"  Saved: {result.name}")
            
            # Mark as read
            mail.store(email_id, '+FLAGS', '\\Seen')
    
    mail.logout()
    
    if saved:
        print(f"\n✓ Processed {len(saved)} emails")
        os.system(f'cd {WIKI_PATH} && git add raw/emails/')
        os.system(f'cd {WIKI_PATH} && git commit -m "Email ingest: {len(saved)} new items"')
        os.system(f'cd {WIKI_PATH} && git push')
    else:
        print("\nNo new emails to process")

if __name__ == "__main__":
    main()
```

### Step 3: Cron Job

```bash
# Run every 5 minutes
*/5 * * * * /usr/bin/python3 ~/wiki/scripts/email_ingest.py >> ~/wiki/logs/email_ingest.log 2>&1
```

---

## Option C: Gmail API (No App Password)

### Step 1: Enable Gmail API
1. Go to Google Cloud Console
2. Create project
3. Enable Gmail API
4. Create OAuth2 credentials

### Step 2: Use Quickstart Script

```python
#!/usr/bin/env python3
"""
gmail_ingest.py - Process wiki emails via Gmail API
Based on Google's quickstart.py
"""

import os
from pathlib import Path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API."""
    creds = None
    TOKEN_PATH = Path.home() / '.config' / 'wiki-agent' / 'token.json'
    
    if TOKEN_PATH.exists():
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        TOKEN_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(TOKEN_PATH, 'w') as token:
            token.write(creds.to_json())
    
    service = build('gmail', 'v1', credentials=creds)
    
    # Call the Gmail API
    results = service.users().messages().list(
        userId='me', 
        q='subject:CLIP OR subject:WIKI is:unread'
    ).execute()
    
    messages = results.get('messages', [])
    print(f"Found {len(messages)} new emails")

if __name__ == '__main__':
    main()
```

---

## Quick Setup Guide

### For iCloud Email

1. **Create alias**: Apple ID → Sign in → Profile → iCloud → Manage Account → Email Aliases
2. **Add to Shortcuts**: New rule triggers on new email to alias
3. **Extract URL**: Use "Match Text" to find URLs in email body

### For Gmail

1. **Enable 2FA** (required for app passwords)
2. **Generate app password**: Google Account → Security → App Passwords
3. **Run script**: Works immediately

---

## Security Notes

- **App passwords**: Store in `~/.bashrc` or `~/.zshrc` as environment variable
- **Credentials files**: Keep in `~/.config/wiki-agent/` with `chmod 600`
- **Don't commit** credentials to git

```bash
# In ~/.bashrc
export WIKI_EMAIL_USER="your-email@gmail.com"
export WIKI_EMAIL_PASS="xxxx xxxx xxxx xxxx"
```

## Related Concepts

- [[rss]] — RSS feed auto-ingest for comparison
- [[automation]] — General automation patterns for wiki maintenance
- [[obsidian-web-clipper]] — Browser bookmarklet for clipping web pages directly to Obsidian
