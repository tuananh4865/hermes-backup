---
confidence: high
last_verified: 2026-04-11
relationships:
  - 🔗 automation (extracted)
  - 🔗 workflow (extracted)
  - 🔗 imap (extracted)
  - 🔗 smtp (extracted)
last_updated: 2026-04-11
tags:
  - productivity
  - automation
  - email
  - tools
---

# Email

> Email management, automation, and AI integration.

## Overview

Email remains a critical communication channel. AI can help with:
- **Sorting**: Automatically categorize incoming emails
- **Drafting**: Generate responses from brief prompts
- **Summarizing**: Get quick overviews of long threads
- **Scheduling**: Extract meeting times and create calendar events

## Email Automation

### IMAP/SMTP Basics

Email clients connect via:
- **IMAP** (Port 993): Reading emails, syncs across devices
- **SMTP** (Port 587/465): Sending emails

### Python Email Libraries

```python
import imaplib
import smtplib
from email.mime.text import MIMEText

# Connect via IMAP
mail = imaplib.IMAP4_SSL('imap.gmail.com', 993)
mail.login('user@gmail.com', 'app_password')

# Send via SMTP
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login('user@gmail.com', 'app_password')
    server.send_message(msg)
```

## Email with AI

### Hermes Email Skill

Our [[hermes-agent]] can manage emails via himalaya CLI:

```bash
# List recent emails
himalaya list

# Read specific email
himalaya read 123

# Compose and send
himalaya compose --to "recipient@example.com" --subject "Hello"
```

### AI Email Agents

Build agents that:
1. Read emails via IMAP
2. Generate context-aware responses
3. Send via SMTP
4. Update labels/flags

## Email Management Patterns

### Labeling Strategy

```
INBOX/
├── action/        # Requires response
├── waiting/       # Waiting for others
├── archive/       # Read and done
├── spam/          # Junk
└── newsletters/   # Optional reading
```

### Response Templates

```python
TEMPLATES = {
    "acknowledgment": "Thanks for reaching out. I'll review and get back to you within 48 hours.",
    "meeting_request": "I'm available {times}. Which works for you?",
    "decline": "Thank you for thinking of me, but I'm unable to commit at this time."
}
```

## Email Security

### App Passwords
Never use your main password. Use app-specific passwords:
- Gmail: myaccount.google.com/apppasswords
- Outlook: account.microsoft.com/security

### 2FA
Always enable two-factor authentication.

### SMTP Settings by Provider

| Provider | IMAP | SMTP | Notes |
|----------|------|------|-------|
| Gmail | imap.gmail.com:993 | smtp.gmail.com:587 | Needs app password |
| Outlook | outlook.office365.com | smtp.office365.com | OAuth recommended |
| iCloud | imap.mail.me.com | smtp.mail.me.com | App password |

## Email Automation Tools

### Mailgun, SendGrid, Postmark
Transactional email APIs for applications.

### Zapier, Make
No-code automation between email and other services.

### procmail, maildrop
Server-side email filtering.

## Related Concepts

- [[automation]] — General automation patterns
- [[workflow]] — Workflow optimization
- [[himalaya]] — Terminal email client we use

## External Resources

- [Python email library docs](https://docs.python.org/3/library/email.html)
- [himalaya email CLI](https://github.com/soywod/himalaya)
