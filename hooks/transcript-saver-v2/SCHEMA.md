# Transcript Entity Schema (v2.0)

> Mục tiêu: mỗi transcript file trở thành 1 **entity/concept page** trong wiki
> với wikilinks, frontmatter chuẩn SCHEMA, và Obsidian mirror real-time.

## Frontmatter chuẩn SCHEMA (8 fields)

```yaml
---
title: "<auto: timestamp + topic>"
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: transcript          # NEW type for v2.0
tags: [transcript, <auto: topics>]
sources: [<user>, <session_id>]
confidence: high
relationships: [<auto: entities found in message>]
transcript_id: <uuid>
platform: telegram
user_id: 1132914873
session_id: 20260601_103236_358b5947
goal: "<auto: extract goal from user message>"
verdict: PASS | WARN | FAIL | null   # from loop-engineering hook
duration_seconds: 0
word_count: 0
---
```

## Auto-extracted fields

### `title` (auto)
Format: `"{HH:MM} - {topic}"` (max 60 chars)
- Topic = first sentence / question in user message
- VD: `"20:14 - Check cách setup hook"`

### `tags` (auto-extract 3-5)
Pattern-based:
- Always: `transcript`
- Domain: `tiktok`, `youtube`, `wiki`, `hermes`, `agent`, `research`
- Action: `setup`, `review`, `analysis`, `fix`, `plan`, `code`
- People: `tuananh`, `<other people mentioned>`

### `relationships` (auto via NER)
- Scan for known entities trong `wiki/entities/` folder
- Scan for known concepts trong `wiki/concepts/` folder
- Auto-add wikilinks cho mỗi match
- Format: `[[entity-name]]`, `[[concept-name]]`

### `goal` (auto-extract)
Extract từ user message:
- "Tôi muốn X" → X
- "Anh muốn em Y" → Y
- "Check X" → Check X
- "Phân tích X" → Analyze X
- Max 100 chars

### `verdict` (từ loop-engineering hook)
Đọc từ state file của profile
- PASS | WARN | FAIL | null (nếu chưa check)

## Body structure

```markdown
# {title}

## User Message
> [{HH:MM}] {user_message}

## Assistant Response
{response}

## Entities Detected
- [[entity-1]] — context
- [[concept-2]] — context

## Related Transcripts
- [[{session_id}-earlier]]
- [[{session_id}-later]]

---
_Saved by transcript-saver v2.0 at {timestamp} | session: {session_id} | verdict: {verdict}_
```

## File organization

```
wiki/raw/transcripts/
├── {YYYY-MM-DD}/
│   ├── {HH-MM-SS}_{session_id}_<topic-slug>.md  (v2.0 format)
│   └── ...
└── conversations/
    └── {YYYY-MM-DD}-{topic-slug}.md  (full thread aggregation)
```

## Obsidian mirror

```
~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/
└── transcripts/
    └── {YYYY-MM-DD}/
        └── {HH-MM-SS}_{session_id}_<topic-slug>.md  (symlink or copy)
```

## Backward compatibility

- v1.0 format: `HH-MM-SS_telegram_<user-preview>.md` (raw transcript only)
- v2.0 format: `HH-MM-SS_{session_id}_<topic-slug>.md` (full entity with frontmatter)
- Migration: read both, prefer v2.0 if exists, fallback to v1.0
