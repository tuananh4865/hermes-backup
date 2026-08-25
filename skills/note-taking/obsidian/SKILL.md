---
name: obsidian
description: Read, search, create, and edit notes in the Obsidian vault.
platforms: [linux, macos, windows]
---

# Obsidian Vault

Use this skill for filesystem-first Obsidian vault work: reading notes, listing notes, searching note files, creating notes, appending content, and adding wikilinks.

## Vault path

Use a known or resolved vault path before calling file tools.

The documented vault-path convention is the `OBSIDIAN_VAULT_PATH` environment variable, for example from `${HERMES_HOME:-~/.hermes}/.env`. If it is unset, fall back to `~/Documents/Obsidian Vault`.

File tools do not expand shell variables. Do not pass paths containing `$OBSIDIAN_VAULT_PATH` to `read_file`, `write_file`, `patch`, or `search_files`; resolve the vault path first and pass a concrete absolute path. Vault paths may contain spaces, which is another reason to prefer file tools over shell commands.

If the vault path is unknown, `terminal` is acceptable for resolving `OBSIDIAN_VAULT_PATH` or checking whether the fallback path exists. Once the path is known, switch back to file tools.

### Tuấn Anh's actual vault (macOS, 2026-06-23 verified)

Primary vault: `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/`

- Always quote this path because it contains spaces — even in `terminal`, prefer single quotes.
- The vault already contains `Loop-Engineering-System.md`, `Transcript-Saver-v2.md`, `Welcome.md`, `index.md`, `log.md`, `transcripts/`, and `concepts/` (mirror of `/Volumes/Storage-1/Hermes/wiki/concepts/`).
- When mirroring wiki pages here, copy into a category-named subfolder (e.g. `concepts/`, `comparisons/`) — Obsidian's graph view picks them up automatically.
- Use `find "~/Library/Mobile Documents/iCloud~md~obsidian" -name "*.md" -maxdepth 5` to verify the vault exists before mirroring; iCloud Drive sometimes takes a moment to mount.

### iCloud Drive sync deadlock (Tuấn Anh's vault, 2026-06-26 verified)

When mirroring files INTO the iCloud vault path (`~/Library/Mobile Documents/iCloud~md~obsidian/...`), `cp` and `rsync` may fail with `Resource deadlock avoided` (errno 35 / EAGAIN) — this happens when iCloud Drive is actively syncing that exact file (e.g. right after Obsidian on another device edited it, or during initial upload). It is NOT a permissions or path issue.

**Symptoms:**
- `cp: <path>: Resource deadlock avoided` — first 1-2 attempts fail
- `rsync: error: <file>: mmap: Resource deadlock avoided` — rsync can also hit it on mmap-based reads
- Exit code 0 sometimes returned by `cp` even when error printed — always check with `stat -f "%Sm %N"` to confirm mtime actually changed

**Recovery (verified pattern, ordered by escalation):**
1. Wait 5-10 seconds (`sleep 10`) — iCloud usually finishes its current sync within that window
2. Retry the copy once. If still fails, wait longer (30s+) and try again
3. **Try a different write surface** — `cp` and `rsync` both hold the destination open via mmap/open(2). Use `cat src > dst.tmp && mv dst.tmp dst` (write to a fresh inode, then atomic-rename onto the locked file). This bypasses the open-file lock that mmap-based sync holds. Verified working 2026-06-27 on `read-full-request-mandate.md` after 3 `cp` + 1 `rsync` retries all failed with EAGAIN.
4. After 3 failed attempts with **all** approaches, **skip the file and log it** — do NOT give up on the whole sync batch
5. **Verify** with `stat -f "%Sm %z %N"` that BOTH mtime AND size match the source. mtime granularity is 1 second on HFS+/APFS — two operations in the same second look identical even when one failed. Size is the tiebreaker.

**Recovery cheat sheet:**
```bash
# Try 1: cp with retry
sleep 10 && cp -f "$src" "$dst" || true

# Try 2: longer wait
sleep 30 && cp -f "$src" "$dst" || true

# Try 3: cat to tmp + atomic rename (this is the one that works)
sleep 30 && cat "$src" > "$dst.tmp" && mv "$dst.tmp" "$dst"

# Verify: mtime + size must match
[ "$(stat -f %Sm "$src")" = "$(stat -f %Sm "$dst")" ] && \
[ "$(stat -f %z "$src")" = "$(stat -f %z "$dst")" ] \
  && echo "OK" || echo "STILL OUT OF SYNC"
```

**Pitfall — silent failure:** A `cp` that prints the error and exits 1 is obvious. A `cp -f` that prints error but exits 0 is dangerous — the file is NOT updated. Always confirm with `stat` or `md5 -q`.

**Why `rsync` is not safer:** `rsync -a` mmap-reads the destination first; if iCloud has the file open, mmap EAGAINs. Same root cause, different surface. A sleep + retry works for both.

**For scripted sync**, see `scripts/sync-to-icloud-vault.sh` — handles the retry loop and verification.

**Run it directly:** `bash ~/.hermes/skills/note-taking/obsidian/scripts/sync-to-icloud-vault.sh` (syncs the 4 default wiki files + `entities/` + `comparisons/` to the vault, with EAGAIN retry).

**Session log for the cat>tmp+mv escalation pattern:** `references/icloud-eagain-recovery-2026-06-27.md` — read this if 3 cp/rsync retries all fail; the atomic-rename fallback is the only thing that breaks a persistent iCloud file lock.

**Session log for the merge-into-main curator pattern (2026-07-01):** `references/session-2026-07-01-curator-telegram-mirror-and-batch-cp.md` — documents how to handle telegram-mirror duplicate stubs (the watchdog creates 2 stubs per Telegram session) + the batch-mirror success pattern (sequential `cp` with `sleep 3-5`). Read this when filling watchdog stubs and when mirroring multiple files in one curator pass.

### Known subfolder convention in this vault

| Subfolder | Mirrors from | Notes |
|-----------|--------------|-------|
| `concepts/` | `wiki/concepts/` | One file per concept; cross-refs via `[[wikilinks]]` |
| `transcripts/` | `wiki/raw/transcripts/{date}/` | Auto-populated by transcript-saver-v2 hook |
| `comparisons/` | `wiki/comparisons/` | Side-by-side concept comparisons (e.g. mandates, frameworks) |
| `index.md` | `wiki/index.md` | Catalog; updated nightly by Felix curation |

## Read a note

Use `read_file` with the resolved absolute path to the note. Prefer this over `cat` because it provides line numbers and pagination.

## List notes

Use `search_files` with `target: "files"` and the resolved vault path. Prefer this over `find` or `ls`.

- To list all markdown notes, use `pattern: "*.md"` under the vault path.
- To list a subfolder, search under that subfolder's absolute path.

## Search

Use `search_files` for both filename and content searches. Prefer this over `grep`, `find`, or `ls`.

- For filenames, use `search_files` with `target: "files"` and a filename `pattern`.
- For note contents, use `search_files` with `target: "content"`, the content regex as `pattern`, and `file_glob: "*.md"` when you want to restrict matches to markdown notes.

## Create a note

Use `write_file` with the resolved absolute path and the full markdown content. Prefer this over shell heredocs or `echo` because it avoids shell quoting issues and returns structured results.

## Append to a note

Prefer a native file-tool workflow when it is not awkward:

- Read the target note with `read_file`.
- Use `patch` for an anchored append when there is stable context, such as adding a section after an existing heading or appending before a known trailing block.
- Use `write_file` when rewriting the whole note is clearer than constructing a fragile patch.

For an anchored append with `patch`, replace the anchor with the anchor plus the new content.

For a simple append with no stable context, `terminal` is acceptable if it is the clearest safe option.

## Targeted edits

Use `patch` for focused note changes when the current content gives you stable context. Prefer this over shell text rewriting.

## Wikilinks

Obsidian links notes with `[[Note Name]]` syntax. When creating notes, use these to link related content.

### Watchdog-processor auto-TODOs (Tuấn Anh setup)

The transcript-saver-v2 hook fires `on_session_end` and writes transcripts to `wiki/raw/transcripts/{date}/`. A separate `watchdog-processor` then scans those transcripts and creates stub concept pages in `wiki/concepts/` for each unique goal/title — these stubs have a TODO template with empty `Summary`, `Key Points`, `Detailed Breakdown`, `Examples`, `Related Concepts`, `Personal Notes` sections.

**When you encounter a watchdog stub during a curation pass:**

- Read the corresponding raw transcript to understand what the user actually said.
- Fill the TODO sections with synthesized content (paraphrased, not copy-pasted — the stub template explicitly forbids verbatim).
- Add at least 3 wikilinks to related concepts in `## Related Concepts`.
- Replace the source `raw/transcripts/...` wikilink with the synthesized version once content is filled.

**Do NOT:**

- Skip filling TODOs because they look tedious — these are the agent's own queue of "things I noticed but didn't have time to write up."
- Delete the stubs; the cross-reference graph depends on them existing.
- Copy-paste from the raw transcript; the template forbids it explicitly and Obsidian graph view will show duplicates.

**Quality bar:** Each stub has 5 TODO blocks. A real fill replaces each with ≥2 sentences of synthesized content.

### Telegram-mirror duplicate stubs (lesson 2026-07-01)

The `transcript-saver-v2` hook fires twice per Telegram session: once on `on_message` (writes `telegram_Tuấn-Anh-...md`) and once on `on_session_end` (writes `{YYYYMMDD}_...md`). Both raw transcripts feed the `watchdog-processor`, which then creates **two parallel concept stubs** for the same session — one under each filename. Result: 2x node-count in the Obsidian graph for one event.

**Detection:** Two stubs in `wiki/concepts/` with the same `session_id` in their corresponding `raw/transcripts/.../{date}_*.md` source files.

**Curator protocol (verified 2026-07-01 02:00):**

1. **Pick the dated-prefix variant as the main page** (matches the `session_id` naming convention).
2. **Write the synthesized content there** — full 5-section fill per the quality bar.
3. **Mark the telegram variant** with `status: merged-into-main` in its YAML frontmatter, and replace the body with a thin redirect:
   ```markdown
   # Telegram Variant — {title} (pointer to synthesized page)

   > Telegram channel mirror of session `{session_id}`. Same content as the main page — the synthesized write-up lives at [[{dated-prefix-filename}]].

   ## Summary
   Telegram-mirror duplicate. The main synthesized page covers {one-line topic}. No new information on this page.

   {2-3 sentences explaining why two files exist + redirect to the main page}
   ```
4. **Add cross-refs** to the main page only — the redirect page should have 1-2 wikilinks (main page + the hook skill that created the duplicates).

**Do NOT:**
- ❌ Fill both stubs with full content — duplicates 5x the work and creates 2 graph nodes for 1 event
- ❌ Delete the telegram variant — the cross-reference graph depends on the wikilink existing
- ❌ Skip the `status: merged-into-main` frontmatter — future agents need the signal that the page is a redirect, not a synthesis

**Future fix (out of scope for this skill — track in transcript-saver-v2):** the hook should dedupe by `session_id` so only one raw transcript is written per session. Until that lands, the curator pattern above is the workaround.

### Filled-stub wikilink count (lesson 2026-07-01)

Quality bar: each filled stub should have **≥3 wikilinks** to related concepts, not just the source `raw/transcripts/...` link. Verified 2026-07-01 fills:
- 4-7 wikilinks in today's filled stubs (tiktok-video-editor, psychology-viral-master-framework-2026, hook-psychology-neuroscience, persuasion-neuromarketing-2026, content-creator-project, etc.)
- 2 new synthesis concepts (padding-flexibility-rule-v2.13, transcript-first-viral-workflow) had 4-7 unique wikilinks each

Below 3 wikilinks = the page is a leaf node; Obsidian graph view will show it as disconnected.

### Mirror success pattern: sequential cp with sleep (lesson 2026-07-01)

For batch mirroring multiple files from `/Volumes/Storage-1/Hermes/wiki/` → `~/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain/`, the following pattern succeeded first-try for 7 files in one run:

```bash
VAULT="/Users/tuananh4865/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain"
SRC="/Volumes/Storage-1/Hermes/wiki"

for f in concepts/padding-flexibility-rule-v2.13.md concepts/transcript-first-viral-workflow.md \
         concepts/00-12-03_20260630_anh-thấy-v3fix-ngắn-và-thông-điệp-gãy-gọ.md \
         concepts/00-12-03_telegram_Tuấn-Anh-Anh-thấy-v3fix-ngắn.md \
         concepts/00-50-16_20260701_httpsdrivegooglecomfiled1kj_vd5luu571tlw.md \
         concepts/00-50-16_telegram_Tuấn-Anh-httpsdrivegoogl.md; do
  sleep 3  # Let iCloud finish any in-flight sync of the destination
  cp -f "$SRC/$f" "$VAULT/$f"
done

# Always-mirror files (3 hard rule — see nightly-memory-curation skill § 5b)
sleep 5
cp -f "$SRC/entities/learned-about-tuananh.md" "$VAULT/learned-about-tuananh.md"
sleep 3
cp -f "$SRC/log.md" "$VAULT/log.md"
sleep 3
cp -f "$SRC/index.md" "$VAULT/index.md"
```

**Why it works:** 3-5s sleep between `cp` calls lets iCloud finish any open-file-lock on the destination. This is the **happy path** for the 02:00 cron window when iCloud Drive is typically idle — no EAGAIN encountered, no `cat>tmp+mv` escalation needed. The escalation patterns in the iCloud EAGAIN section above are still correct for the failure case (mid-day syncs, active editing on another device), but for batch overnight mirrors, sequential `cp` with sleep is the right default.

**Pitfall:** Do NOT parallelize the `cp` calls with `&` — concurrent writes to iCloud targets can re-introduce the open-file-lock contention that the 3-5s sleep is designed to avoid. Sequential is correct.
