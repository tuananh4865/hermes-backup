---
name: daily-session-review
description: "Cron 0h: tong hop session logs 24h, extract research/thuc hien/khuyen nghi, gap, report + Telegram. Chi Content Creator context (filter: mic, den, gimbal, lens, flycam, action cam, TikTok Shop, Shopee Affiliate, review, test). Khong can external research."
trigger: "Khi cron job Daily Session Review chay 0h, hoac user yeu cau review session hom qua"
category: productivity
---

# Daily Session Review Workflow

> **Source:** Tuấn Anh cron job setup — 2026-06-18

## Trigger

- **Cron:** 0h00 mỗi ngày
- **Context filter:** Chỉ Content Creator keywords — `mic`, `đèn`, `gimbal`, `lens`, `flycam`, `action cam`, `TikTok Shop`, `Shopee Affiliate`, `review`, `test`, `body mist`, `pocket3`, `vợt cầu lông`, `yonex`, `gemma`, `whisper`, `máy hút bụi`
- **Additional CC research types to capture:**
  - AI tools cho content creation (Whisper, Gemma, translation, TTS)
  - Badminton gear (vợt, giày, phụ kiện)
  - Sản phẩm bán (body mist, máy hút bụi, case)
  - Video editing workflow research
- **Skip:** AI agent, coding, system admin sessions

## Workflow

### 1. Read previous day's review FIRST (primary data source)

```bash
# Read previous day's review — this is the cleanest source, no session DB parsing needed
cat ~/Workspace/Claude/Projects/Content\\ Creator/Research/$(date -v-1d +%Y-%m-%d)/daily-session-review.md
```

This gives you yesterday's sessions + gaps in ~4KB. **ALWAYS start here** — do NOT begin with `session_search` keyword queries.

**Why:** Keyword `session_search` returns the cron job's OWN prompt (which contains the keywords) plus previous cron runs. This pollutes results with self-referential entries instead of actual Content Creator sessions. The previous day's review file has clean, already-digested session summaries.

**Only use session_search if:** previous day's review file is missing/corrupt, OR you need to check for sessions that started AFTER the previous day's 0h cron ran (afternoon/evening sessions).

**⚠️ Long-running session bleed:** Session `20260718_071838_8d4cf9aa` started at 07:18 on Jul 18 but ran until 23:53 (~16.5h). Its `ended_at` was logged at Jul 19 00:00:09. The session appears in Jul 19's cron DB despite being entirely Jul 18 work.
- **Rule:** Cross-reference `started_at` (session window) with `ended_at` (actual completion). If `started_at` falls in yesterday's date but `ended_at` is in today's early hours, classify the session under yesterday's review.
- Use Unix timestamp range to convert date boundaries.

**⚠️ Keyword session_search returns cron prompts (2026-07-24):** A keyword search for `mic đèn gimbal...` returns the cron job's OWN system prompt text (which contains those keywords verbatim), plus previous cron run reviews. This creates 10+ self-referential results that swamp actual Content Creator sessions. ALWAYS start with the previous day's `daily-session-review.md` file — it has clean, already-digested summaries. session_search is a fallback only.

### 2. Search session logs (fallback only)

**Primary data source (2026-07-17):** The wiki transcript folder `/Volumes/Storage-1/Hermes/wiki/raw/transcripts/` is MORE RELIABLE than session_search. It contains complete session transcripts organized by date in subdirectories (`2026-07-14/`, `2026-07-16/`, `2026-07-17/`). Flat root files (`20260714_*.md`) appear when sessions cross midnight. Use `ls /Volumes/Storage-1/Hermes/wiki/raw/transcripts/` to discover date directories, then `grep -l -i KEYWORD` to filter.

**Step 0 (IMPORTANT — 2026-07-01):** Read previous day's review FIRST.

```bash
cat ~/Workspace/Claude/Projects/Content\ Creator/Research/{YYYY-MM-DD-1}/daily-session-review.md
ls ~/Workspace/Claude/Projects/Content\ Creator/Research/{YYYY-MM-DD-1}/
```

This gives you yesterday's sessions + gaps in ~4KB — no payload parsing. Do NOT start with session_search keyword queries; they return 200-600KB payloads that get persisted to temp files and show 0 lines when read via read_file.

**Fallback: session_search tool** (only if previous day's review is missing or insufficient):```python
import datetime, sqlite3

now_ts = int(datetime.datetime.now().timestamp())
ago_24h = now_ts - 86400  # 24 hours

conn = sqlite3.connect('/Users/tuananh4865/.hermes/state.db')
cursor = conn.cursor()

# Step A: Pre-filter sessions by title + message_count to avoid scanning every session
# (skip heartbeat/routing/audit sessions — they pollute keyword matches)
cursor.execute("""
    SELECT id, source, title, started_at, message_count 
    FROM sessions 
    WHERE started_at >= ? AND started_at < ?
    AND title NOT LIKE '%Heartbeat%'
    AND title NOT LIKE '%Routing Audit%'
    AND title NOT LIKE '%Quality Gate%'
    AND title NOT LIKE '%Vuln Scan%'
    AND title NOT LIKE '%Cleanup%'
    AND title NOT LIKE '%Backup%'
    AND title NOT LIKE '%Consolidation%'
    ORDER BY started_at DESC
""", (ago_24h, now_ts))
candidate_sessions = cursor.fetchall()

# Step B: For each candidate, search message content for keywords
# (keyword list: mic, đèn, gimbal, lens, flycam, action cam, TikTok Shop, Shopee Affiliate, review, test, content creator, quay dựng, thiết bị, ...)
keywords = ['mic', 'đèn', 'gimbal', 'lens', 'flycam', 'action cam', 'tiktok shop', 
            'shopee affiliate', 'review', 'test', 'content creator', 'quay dựng', 
            'thiết bị', 'mayanh', 'camera', 'ánh sáng']

matched = []
for sid, source, title, started_at, msg_count in candidate_sessions:
    placeholders = ','.join(['?' for _ in keywords])
    cursor.execute(f"""
        SELECT COUNT(*) FROM messages 
        WHERE session_id = ?
        AND (""" + " OR ".join([f"LOWER(content) LIKE ?" for _ in keywords]) + """)
    """, [sid] + [f'%{k}%' for k in keywords])
    count = cursor.fetchone()[0]
    if count > 0:
        matched.append((sid, source, title, started_at, msg_count, count))

conn.close()
# matched = sessions with keyword hits (sid, source, title, started_at, msg_count, hit_count)
```

**Convert Unix timestamps manually:**
```python
import datetime
now_ts = int(datetime.datetime.now().timestamp())  # e.g. 1781974919
ago_24h = now_ts - 86400                        # 24 hours = 86400 seconds
```

**Schema facts (CRITICAL):**
- `sessions.started_at` is Unix timestamp (REAL), NOT datetime string
- `messages.timestamp` is also Unix timestamp (REAL)
- `session_id` in messages references `sessions.id`
- `sessions` table does NOT have `ended_at` or `last_active` columns — use `message_count` instead
- Query: `WHERE started_at >= {ago_24h} AND started_at < {now_ts}`

**Example query for 24h window (simple — no pre-filter):**
```bash
sqlite3 ~/.hermes/state.db "SELECT id, source, title, started_at, message_count FROM sessions WHERE started_at >= 1781888400 AND started_at < 1781974800 ORDER BY started_at DESC;"
```

**Pitfall:** `datetime('now', '-24 hours')` does NOT work on Unix timestamp columns — returns empty results. Always use raw Unix timestamps.

**Pitfall (2026-06-29):** `sessions` table has NO `last_active` column. Use `message_count` instead. The query `"SELECT ... last_active ..."` will raise `sqlite3.OperationalError: no such column: last_active`.

**Pitfall (2026-07-10):** `sessions` table uses column `id`, NOT `session_id`. First query attempt using `session_id` fails with `Parse error: no such column: session_id`. Always use `id` when querying the sessions table directly.

**Timestamp boundary trap (2026-07-10):** Query `WHERE started_at >= 1783531200 AND started_at < 1783617600` returned empty even though the timestamp range (Jul 9 00:20 to Jul 10 00:20) should have captured the cron session. The correct working query that returned data: no upper bound `<` — just `WHERE started_at >= 1783531200 ORDER BY started_at DESC`. The cron session itself (cron_5aea298eb0a8_20260710_000005) runs for ~17 minutes, logging its own start at `started_at=1783616406.1830311` (Jul 10 00:00:06).

**Unix timestamp reference (2026-07-10):**
- `1783616406` = Jul 10 2026 00:00:06 +07
- `1783617600` = Jul 10 2026 00:20:00 +07
- `1783531200` = Jul 9 2026 00:20:00 +07
- To convert: `date -r <timestamp>` on macOS

**Performance pitfall:** Without title pre-filtering, keyword scanning across ALL sessions (including 40+ heartbeat/routing/audit sessions) wastes time and produces noise. Always pre-filter sessions by title patterns (skip Heartbeat, Routing Audit, Quality Gate, Vuln Scan, Cleanup, Backup, Consolidation) before keyword content search.

**Subagent sessions — skip untitled (2026-07-09):** Subagent background sessions spawned during parent sessions (e.g. at 11:50, 12:07 on 2026-07-08) have NO title and `source=system`. They appear in the session list as rows like `20260708_115025_1bbb8f||` with empty title. They are internal processing — never report on them. The tell: `source=system` OR `title=''` OR title matching pattern `^20260[0-9]{10}_[0-9a-f]{6}$` (raw cron ID format with no user-readable title).

**Empty-titled sessions with 0 messages (2026-07-14):** Session `20260714_155035` appeared in browse results with empty title and `message_count=0`. These are NOT subagent sessions (source=telegram, not system) — likely a Telegram session where the user sent a media-only message (photo/file without text) and the session was created but no text messages were exchanged. Skip these — they have no extractable content.

**Extract messages from sessions:**
```bash
sqlite3 ~/.hermes/state.db "SELECT session_id, role, substr(content, 1, 500) FROM messages WHERE session_id = '{session_id}' ORDER BY timestamp LIMIT 10;"
```

**Key columns:**
- `sessions.id` = `messages.session_id` (join key)
- `sessions.started_at` = Unix timestamp (REAL)
- `messages.content` = TEXT (user/assistant messages)
- `messages.role` = 'user' | 'assistant' | 'tool'

**Fallback — session_search tool (SLOW, use only when SQLite approach fails):**
- First: `session_search(limit=5, sort="newest")` — gets session list overview (fast, ~10 recent sessions)
- Then: `session_search(query="keywords", limit=5, sort="newest")` — keyword-filtered (returns 200KB+ payloads — slow)
- Finally: `session_search(session_id=ID, around_message_id=X, window=5)` — scroll into specific session

**Search sequentially:**
1. `session_search(limit=5, sort="newest")` — browse recent sessions (small payload, fast)
2. `session_search(query="mic đèn gimbal lens flycam action cam TikTok Shop Shopee Affiliate review test", limit=5, sort="newest")` — keyword search
3. If large payload: paginate with `offset` + `limit`, or scroll into specific session

**Pitfall:** Keyword query via session_search returns 200KB+ payloads. Always read preview snippet first, then use `session_search(session_id)` for targeted reads. Prefer SQLite direct query for speed.

### 3. Extract per session

**Step 0 (SKIP session_search for now):** Read `Content Creator/Research/{YYYY-MM-DD-1}/daily-session-review.md` FIRST. This gives you yesterday's sessions, gaps, and action items in clean 4KB — no payload parsing needed. Carry forward any un-resolved gaps.

**Step 1: Get session list via session_search browse mode (small payload)**

```python
session_search(limit=5, sort="newest")  # Fast — ~10 recent sessions, preview snippet only
```

**Step 2: Identify Content Creator sessions from the list**

Look for: `TikTok 5-Channel`, `YouTube Search`, `Nightly Monitor`, `Session Review`, `Autoresearch`, or Telegram sessions about video editing/equipment.

**Step 3: Read previous day's daily-session-review to identify specific session IDs to investigate**

The previous review lists which sessions to check. Use those session IDs directly.

**Step 4: Read specific session content via session_search read mode (targeted)**

```python
session_search(session_id="{session_id}", around_message_id={anchor}, window=5)
```

Only read sessions identified in the previous day's review — never try to read large session payloads blindly.

**Pitfall (2026-07-05):** Session search snippets are NOT sufficient for detailed extraction. Example: the 16:35 batch-edit session had 6 clips, CTA punch values (17.8s, 33.9s, etc.), and audio RMS values — none of this appeared in the 3-line snippet. You must scroll into the session with `session_search(session_id=..., around_message_id=anchor, window=10)` to get actual data. Snippets give you the session EXISTS; read the full transcript to extract what was actually done.

**Record per session:**
- Timestamp
- Topic
- Output (file path, size)
- Decision/recommendation made

### 4. Write report

**Primary path:** `~/Workspace/Claude/Projects/Content Creator/Research/{YYYY-MM-DD}/daily-session-review.md`

> Note: As of 2026-07-18, this is the confirmed working path (not `wiki/queries/`).

Format:
```markdown
# Daily Session Review — {YYYY-MM-DD}

## TL;DR
- {số session} | {top insight} | {gap hôm nay}

## Sessions liên quan
| Thời gian | Topic | Output | Decision |

## Research đã làm
- ...

## Gaps cần fill
- ...

## Action items
- [ ] ...
```

### 5. Telegram summary

```
📋 Daily Review — {YYYY-MM-DD}
{1 dòng tóm tắt}
{1 dòng gap quan trọng}
📁 {path}
```

Rules: <5 dòng, chỉ report từ logs, action items rõ ràng.

### 6. Loop Engineering state

```bash
python3 ~/.hermes/loop-engineering/profile_state.py run default "<goal>" 1 <PASS|FAIL>
```
Note: Do NOT pass a <score> argument — it will be rejected as unrecognized.

## Anti-patterns

- Không tổng hợp AI/coding/system sessions
- Không đưa khuyến nghị mới — chỉ report đã làm
- Không external research — chỉ internal logs
- Không delegate cho Researcher bot

## Verification

- [ ] File saved correct path
- [ ] Telegram <5 lines
- [ ] Data from session logs only
- [ ] Action items executable

## References

- `references/session-storage-layers-2026-07-27.md` — ⚠️ CRITICAL: 4 storage layers (sessions.db, sessions.json, request_dump, jsonl) + diagnosis protocol when session content is unreadable
- `references/session-2026-06-17.md` — Example run: 2026-06-17 (3 sessions, 5 research files created, gaps identified)
- `references/session-2026-07-06.md` — 06/07 review: 3 CC sessions (body mist V4 batch, Yonex script, Top Heroes analysis), file saved to wiki/queries/2026-07-06/
- `references/session-db-schema.md` — SQLite schema + query patterns for state.db (Unix timestamps, key columns, pitfalls)
- `references/session-2026-07-08.md` — 08/07 review: edit clip 0689/0682 + 3 clip bút iPad 0697/0699/0700 + sales psychology deep research; subagent sessions to skip at 11:50/12:07
- `references/session-2026-07-09.md` — 09/07 review: 3 CC sessions (edit 0689/0682, highlight cầu lồng); key lesson = session DB stores by START time not cron runtime
- `references/session-2026-07-14.md` — 14/07 review: 4 CC sessions (YouTube Shorts download, Google Flow method discovery, footage check); key lesson = cua-driver `insert_text` hoạt động với React Slate editors
- `references/session-timestamp-boundaries-2026-07-28.md` — Unix timestamp boundaries for Jul 2026 (verified correct values). Use `date -j -f` on macOS, NOT manually calculated integers. sessions.db recovered Jul 28 after being empty Jul 27.
- `references/session-storage-layers-2026-07-27.md` — ⚠️ CRITICAL: 4 storage layers + diagnosis protocol. Updated: sessions.db recovered next day; don't escalate on transient empty.

**⚠️ sessions.json = metadata only (2026-07-27):** `sessions.json` contains ONLY session metadata (session_id, created_at, input_tokens, output_tokens). It does NOT contain message content. If `input_tokens=0, output_tokens=0` for recent sessions, the actual conversation is NOT stored there — must use `session_search` (internal index) or `sessions.db` (SQLite). When all storage layers empty, report "NO SESSION DATA" honestly.

## Related

- [[hermes-cron-management]]
- [[hermes-autoresearch]]
- [[tiktok-viral-script]]
