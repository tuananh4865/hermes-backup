# Telegram Document Batch Flood Control (2026-06-26)

## TL;DR

Telegram Bot API rate-limits `sendDocument` calls. Sending **>1 file in <30s** triggers `RetryAfter: Flood control exceeded. Retry in 34 seconds`. Retries succeed, but UX lags. **Cron-driven tools that deliver >1 file per run should batch with 3-5s delay between sends.**

## The failure mode (KarmaVid 19:30, 2026-06-26)

A Telegram user session `20260626_153010_e08f968d` completed KarmaVid Phase 01-03 work, then on user prompt *"Gửi file đây cho anh"* tried to send 4 research files via `send_document`:

| File | Size | Order |
|------|------|-------|
| T-02.1-karmavid-universe.md | 14KB | 1 |
| T-03.1-karmavid-script-template.md | 12.8KB | 2 |
| T-01.1-herocat2309-analysis.md | 11KB | 3 |
| T-03.2-karmavid-script-samples.md | 11.8KB | 4 |

Total ~52KB across 4 files. Sends were fired in rapid succession. The 3rd or 4th triggered:

```
WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Failed to send document: Flood control exceeded. Retry in 34 seconds
Traceback (most recent call last):
  ...
  raise RetryAfter(retry_after)
telegram.error.RetryAfter: Flood control exceeded. Retry in 34 seconds
2026-06-26 19:30:35,164 WARNING hermes_plugins.telegram_platform.adapter: [Telegram] Telegram flood control on send (attempt 1/3), retrying in 33.0s
```

The adapter retried automatically (built-in flood-control retry with 33s backoff). All 4 files eventually delivered. But:
- The user perceived a 30+ second lag with no status update.
- If the user was on mobile, the chat might have scrolled past the first 2 files by the time the last 2 arrived.
- If the retry budget (3 attempts) had been exhausted, files 3-4 would have failed silently with the user never knowing.

## The Telegram limits

From Telegram Bot API docs (2026-06-26 verified):

| Direction | Limit |
|-----------|-------|
| Receive (`getFile`) | 20 MB max per file |
| Send (`sendDocument`/`sendVideo`) | 50 MB max per file |
| **Send rate** | **~30 sends/minute to same chat** (broadcast) |
| **Burst tolerance** | **~5 sends/second before flood-control kicks in** |
| Same-chat flood | `RetryAfter: <N>` returned, agent MUST wait N seconds |

The flood-control is per-chat, not global. Other chats won't be affected, but the same chat's outbound queue throttles.

## The fix (3 options, ranked)

### Option 1: Batch with 3-5s delay between sends (RECOMMENDED for 2-5 files)

Add `time.sleep(4.0)` between consecutive `send_document` calls:

```python
import time
from hermes_tools import send_message

files = ["/path/to/T-02.1-karmavid-universe.md",
         "/path/to/T-03.1-karmavid-script-template.md",
         "/path/to/T-01.1-herocat2309-analysis.md",
         "/path/to/T-03.2-karmavid-script-samples.md"]

for f in files:
    send_message(action="send", target="telegram", message=f"MEDIA:{f}\n")
    time.sleep(4.0)  # 4-second delay between sends
```

**Trade-off:** 4 files × 4s = 16s total delivery time. Still much better than 33s flood-control retry. User sees files arriving 1-by-1 with clear timestamps.

### Option 2: Use HERMES_TELEGRAM_TEXT_BATCH_SPLIT_DELAY_SECONDS (env var, when set)

The Hermes gateway already supports a delay setting for text message splitting (introduced 06-25 in the same flood-control fix batch). If `HERMES_TELEGRAM_TEXT_BATCH_SPLIT_DELAY_SECONDS` is set, the gateway applies it. Verify:

```bash
hermes config get telegram.batch_split_delay_seconds
# or check ~/.hermes/config.yaml for telegram.batch_split_delay_seconds
```

If unset, add via:

```bash
hermes config set telegram.batch_split_delay_seconds 4.0
```

**Trade-off:** Affects ALL Telegram sends globally, not just multi-file. If set too high (>10s), normal single-message sessions feel sluggish.

### Option 3: Embed summary + link to iCloud/Drive (RECOMMENDED for >5 files)

For >5 files, embed a summary in chat and link to a single archive:

```python
import shutil
shutil.make_archive("/tmp/karmavid-phase-01-03", "zip",
                    "/Volumes/Storage-1/Hermes/wiki/projects/karmavid")
# Then send 1 file (the zip) + summary embed
send_message(action="send", target="telegram",
             message=f"""📦 KarmaVid Phase 01-03 archive (52KB):
MEDIA:/tmp/karmavid-phase-01-03.zip

1. T-02.1 Universe (14KB)
2. T-03.1 Script Template (12.8KB)
3. T-01.1 herocat2309 Analysis (11KB)
4. T-03.2 Script Samples (11.8KB)
""")
```

**Trade-off:** User has to unzip to read individual files. Best when files are part of a coherent deliverable (project archive, batch research output). NOT recommended for files user expects to consume individually.

## When this fires (decision tree)

| Scenario | Recommended option |
|----------|-------------------|
| 1 file | No delay needed (singleton send never triggers flood control) |
| 2-5 files, related to one task | Option 1 (4s delay) |
| 2-5 files, distinct deliverables | Option 1 (4s delay) + 1 summary message before/after |
| 5-10 files | Option 1 (4s delay) OR Option 3 (zip archive) |
| >10 files | Option 3 (zip archive) — delays add up |
| Files >20MB each | Option 3 + Drive/iCloud (Telegram receive limit on user's side) |
| Files split for parallel users (DM + group) | OK to send parallel; flood control is per-chat |

## Detecting retry failures in cron-driven flows

Cron jobs that send files should ALWAYS check for `RetryAfter` errors and log them. If a file delivery silently fails after exhausting retries, the cron should:

```python
result = send_message(action="send", target="telegram", message=f"MEDIA:{f}\n")
if "error" in result and "Flood control" in result["error"]:
    # Log to errors.log with the file path
    with open("~/.hermes/logs/errors.log", "a") as log:
        log.write(f"{timestamp} FAILED: {f} - {result['error']}\n")
    # Don't crash the cron; continue with next file
    time.sleep(35)  # Honor the RetryAfter interval
```

## Cross-references

- 06-18 flood control fix: `~/Library/LaunchAgents/ai.hermes.gateway.plist` env vars + `~/.hermes/.env` rich_messages=false — this is the receive-side fix
- 06-25 Telegram Embed-Deliver Rule: for >5KB files, embed summary in chat instead of just sending the file
- This file: outbound batch delivery (multiple files per cron run)
- `telegram-video-analysis` skill Pitfall #34: 20MB receive limit (different concern — file size, not rate)

## Provenance

Captured 2026-06-26 nightly reflection. Triggered by KarmaVid Phase 01-03 file delivery at 19:30 (session `20260626_153010_e08f968d`). The Hermes adapter's built-in retry (3 attempts with 33s backoff) recovered automatically — the user got all 4 files — but the 30s lag was noticeable. Compounding with the Telegram Embed-Deliver Rule (06-25): when sending multiple research files, both rules apply — embed summary AND batch with delay.