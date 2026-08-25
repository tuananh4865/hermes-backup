# Session 2026-07-21 02:00 — Gap-fill with set-diff discovery (43 concept + 3 entity missing)

## What happened

Forced gap-fill pass on the 07-20 cron under-delivery. 07-20 02:00 cron either silently failed or skipped Step 5b entirely. 35h+ staleness on all 3 always-mirror files when 07-21 fired.

**The new lesson (L52/L54/L55):** the 3-file mtime check passed/failed independently of how many concept/entity pages were missing from vault. Step 0 detection needed to be EXTENDED with a set-diff pre-flight to catch the third failure mode.

## Detection flow

```
NEW transcripts 2026-07-21: 0
NEW transcripts 2026-07-20: 0
NEW sessions since log.md: 0
3-file mtime check → ALL 3 stale (35h08m, 34h56m, 21h15m)
→ Mode: GAP-FILL
```

**The set-diff surprise (Step 0.5):**
```
Wiki concepts: 84
Vault concepts: 196
→ "vault has more" intuition WRONG
```

Running `comm -23`:
```
=== MISSING in vault (in wiki but not in vault) ===
43 pages including: drift-recovery-3-systems-2026-07-19,
builder-judge-manager-self-correcting-loop, tiktok-viral-script,
whisper-word-level-timestamps-fix-2026-07-18, hook-psychology-neuroscience,
sales-psychology-master-framework-2026-07-07, ...
```

**Root cause analysis:** 07-19 main-pass created 43 concept pages + 3 entity pages, mirrored the 3 always-mirror files, but never mirrored the N new pages. 07-20 cron under-delivered entirely (silent failure / iCloud EAGAIN / background-review toolset constraint). The 07-21 pass had to recover the entire wiki-side creation since 07-19.

## Mirror recovery scope (this pass)

- 3 always-mirror files (log.md, learned-about-tuananh.md, index.md): all byte-identical first-try
- 43 concept pages: 43/43 MD5 PASS first-try, zero EAGAIN escalations
- 3 entity pages: 3/3 PASS first-try
- 1 spot-check on pre-existing vault file (`adversarial-verifier-protocol-2026-07-12.md`) hit EAGAIN during md5 read → escalated to `sleep 30 + cat>tmp+mv` atomic-rename → MD5 byte-identical after recovery

**Total:** 49 files mirrored, 1 EAGAIN escalation (read-side), 48 first-try success.

## Lessons captured (L52-L56)

### L52 — Gap-fill scope can extend beyond the 3 always-mirror files
The Step 0 detection only checks 3 files. The recovery scope can be much larger (43 + 3 = 46 in this case). Codified as Step 0.5 set-diff pre-flight.

### L53 — cat>tmp+mv works for ANY EAGAIN'd file (bidirectional)
Pre-existing vault files can EAGAIN during md5 verification read, not just during mirror write. The atomic-rename pattern is a recovery mechanism, not a write-side fallback. Verified on `adversarial-verifier-protocol-2026-07-12.md` (existed in vault since 07-12, EAGAIN'd on 07-21 read).

### L54 — Third gap-fill failure mode
Beyond (a) skip-always-mirror [06-28] and (b) single-file-staleness [06-29]: (c) **scope-bounded-to-always-mirror** — pass mirrored 3 always-mirror but skipped N concept/entity pages. Detection requires set-diff, not mtime check.

### L55 — Set-diff > file-count comparison
Vault can have STALE files no longer in wiki inflating its count (vault 196 vs wiki 84, but 43 wiki files missing). Signal that matters is asymmetric set membership (`comm -23`), not subtraction.

### L56 — Silent cron under-delivery root cause
When 07-19 main-pass created pages but didn't mirror them, and 07-20 cron under-delivered entirely, the likely root causes are: (a) background-review toolset constraint (06-27 lesson) silently dropping the cron, OR (b) iCloud mid-day EAGAIN during 02:00 cron window. Future mitigation: detect via set-diff in Step 0; add cron liveness check via `output/<job-id>/` mtimes (06-28 lesson) to catch silent no-op early.

## Mass-mirror script template (07-21)

Captured at `/tmp/mirror_concepts.sh` during the 07-21 run. Pattern: pre-build the file list via set-diff → loop with `sleep 3` + `md5 -q` verify per file → escalate to `cat>tmp+mv` on mismatch. Handles 43 files in ~3 min with full MD5 verification, zero false-positives.

```bash
#!/bin/bash
WIKI="/Volumes/Storage-1/Hermes/wiki"
VAULT="$HOME/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain"

# Set-diff to build the mirror batch
WIKI_FILES=$(find "$WIKI/concepts" -maxdepth 1 -name "*.md" -type f ! -name "_*" ! -name "*.bak" ! -name "*.audit-backup" 2>/dev/null | xargs -I{} basename {} | sort)
VAULT_FILES=$(find "$VAULT/concepts" -maxdepth 1 -name "*.md" -type f 2>/dev/null | xargs -I{} basename {} | sort)
MISSING=$(comm -23 <(echo "$WIKI_FILES") <(echo "$VAULT_FILES"))

OK=0; FAIL=0
for f in $MISSING; do
    sleep 3
    cp -f "$WIKI/concepts/$f" "$VAULT/concepts/$f"
    if [ "$(md5 -q "$WIKI/concepts/$f")" = "$(md5 -q "$VAULT/concepts/$f")" ]; then
        OK=$((OK + 1))
    else
        sleep 20
        cat "$WIKI/concepts/$f" > "$VAULT/concepts/$f.tmp" && mv "$VAULT/concepts/$f.tmp" "$VAULT/concepts/$f"
        [ "$(md5 -q "$WIKI/concepts/$f")" = "$(md5 -q "$VAULT/concepts/$f")" ] && OK=$((OK + 1)) || FAIL=$((FAIL + 1))
    fi
done
```

## Verification gate (mandatory after this pass)

- 3 always-mirror files: `diff -q` returns empty
- 43 concept pages: full MD5 sweep → 43/43 PASS
- 3 entity pages: 3/3 PASS
- Pre-existing vault spot-check: 1 hit EAGAIN, escalated, recovered

## Key finding for the day

Vault was 35h+ stale across all 3 always-mirror files AND had 43 concept pages + 3 entity pages missing entirely. Root cause: 07-19 main-pass created the N pages but mirrored only the 3 always-mirror; 07-20 cron under-delivered silently. **Future-fix action item:** Step 0.5 set-diff pre-flight now codified in SKILL.md, so future gap-fill runs catch this on the FIRST attempt instead of waiting for the next 24h cron cycle.

## When to re-read this reference

- When the 3-file staleness check fires with non-trivial deltas (≥24h)
- When running any mass-mirror (≥5 files) — use the script template, don't iterate manually
- When an iCloud vault path returns `Resource deadlock avoided` on READ (not just write) — escalate to `cat>tmp+mv`
- When a curator entry ends with "iCloud mirror verification: Pending" — never accept that, run set-diff + md5