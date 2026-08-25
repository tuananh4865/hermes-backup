---
title: Nightly Curator — Gap-Fill Worked Example 2026-06-28 02:00
created: 2026-06-28
type: reference
tags: [nightly-memory-curation, gap-fill, mirror-fail, 2026-06-28, operational-lesson]
confidence: high
relationships: [nightly-memory-curation, references/session-2026-06-25-gap-fill, references/session-2026-06-27-structural-pitfalls]
---

# Nightly Curator — Gap-Fill Worked Example 2026-06-28 02:00

> **Run context:** 2nd nightly firing of `memory-curator` cron, 2026-06-28 02:00 +07
> **Input state:** 0 new transcripts since previous pass, 1 session.json index entry from 2026-06-27 20:40
> **Classification:** **GAP-FILL** (not main, not noop)
> **Why this reference exists:** Captures the concrete failure mode that Step 0's noop check ALONE would have missed, plus the operational fix that prevents recurrence.

---

## 🚨 The Gap

### Detection (Step 0 — gap-fill triggers correctly)

```bash
$ ICLOUD_LOG_MTIME=$(stat -f "%m" "$VAULT/log.md" 2>/dev/null || echo 0)
$ WIKI_LOG_MTIME=$(stat -f "%m" "$WIKI/log.md")
$ echo "Wiki log.md: $WIKI_LOG_MTIME"
$ echo "Vault log.md: $ICLOUD_LOG_MTIME"
Wiki log.md: 1782567659
Vault log.md: 1782414197
$ [ "$ICLOUD_LOG_MTIME" -lt "$WIKI_LOG_MTIME" ] && echo "GAP-FILL"
GAP-FILL
$ # Delta calculation
$ DIFF_SEC=$((WIKI_LOG_MTIME - ICLOUD_LOG_MTIME))
$ echo "Delta: $DIFF_SEC seconds = ~$((DIFF_SEC/3600))h"
Delta: 153462 seconds = ~42h
```

**The 06-27 main pass (02:00) had:**
- Mirrored 3 new concept pages (`fable-5-base-architecture.md`, `karmavid-project.md`, `wikimemory-atomic-write-fix.md`) — concept mirror OK ✅
- **Skipped** the 3 always-mirror files (`log.md`, `learned-about-tuananh.md`, `index.md`) entirely
- The 06-27 03:00 follow-up cron likely ran in `background review` mode and silently under-delivered (per W3 lesson in the 06-27 23:00 Orchestrator reflection)

**The cost:** iCloud vault `log.md` went 42 hours stale. The 06-27 23:00 Orchestrator reflection made a large update to `learned-about-tuananh.md` (W1-W4 issues, L1-L3 lessons, "Tomorrow's priorities" section — file grew from 50,846B → 71,543B) that **never reached iCloud** until tonight's run.

---

## ✅ The Recovery

### What the 06-28 02:00 gap-fill pass did

1. **Verified** wiki state: 3 new concept pages from 06-27 02:00 already in vault (concept mirror OK, no re-mirror needed)
2. **Mirrored** the 3 always-mirror files using EAGAIN-safe pattern:
   - `log.md` (177,315B → 179,366B after this run's gap-fill entry appended)
   - `learned-about-tuananh.md` (71,543B, +20,697B from 06-26 02:03)
   - `index.md` (33,076B, +1,754B from 06-26 02:03)
3. **Verified byte-identical** with `diff -q` for all 3 files — all passed first try (iCloud was idle, no EAGAIN retries needed)
4. **Discovered and resolved** the 06-27 23:00 Orchestrator reflection's iCloud gap (now mirrored)
5. **Logged the gap-fill pass** with root cause analysis in `log.md`

### iCloud EAGAIN reality check

This run got lucky — iCloud was idle, so the simple `cp` succeeded on first try for all 3 files. The 06-27 EAGAIN recovery skill (in `obsidian` skill § "iCloud Drive sync deadlock") documented that `cp` + `rsync` both fail with EAGAIN when iCloud has the destination open. The escalation pattern (cat > tmp + atomic mv) was **not** needed this run, but it's the only known fallback. Future runs in active-sync windows should expect EAGAIN.

---

## 🛠 Operational Hard Rule (codified in SKILL.md Step 5b)

The 06-25 miss (1 day) + 06-27 miss (42h) prove that "always mirror log.md/learned-about-tuananh.md/index.md" buried in a pitfall note is **not load-bearing**. The rule needs to be operationalized.

**The new hard rule (SKILL.md § 5b):**
1. **Pre-mirror state check**: `stat -f "%m" "$VAULT/log.md" < "$WIKI/log.md"` → triggers gap-fill, not noop
2. **EAGAIN-safe mirror pattern** (codified in `scripts/safe-mirror.sh`): cp → verify size → cat>tmp+mv if needed → 60s wait if still failing
3. **Post-mirror gate** (mandatory): `diff -q "$WIKI/$f" "$VAULT/$f"` must return empty for all 3 files
4. **Every run mirrors the 3 files** — no exceptions for noop mode

**Why this is a "hard rule" not a "pitfall":** The 06-25 + 06-27 misses cost 42h of vault staleness combined. A "pitfall" reads as advisory. A "hard rule" reads as the curator's job description — fail the curator, not the vault.

---

## 📊 Concrete numbers from this run

| Metric | Value | Notes |
|--------|-------|-------|
| Sessions consolidated | 0 | Yesterday (6/27) had 1 routine Facebook-reel download, already in log.md |
| Pages updated | 0 | No new content beyond the 06-27 23:00 Orchestrator reflection already in wiki |
| New pages created | 0 | Pure gap-fill run |
| Cross-references added | 0 | N/A — no new pages |
| Files mirrored | 3 | log.md, learned-about-tuananh.md, index.md (all byte-identical) |
| EAGAIN retries needed | 0 | iCloud idle, cp succeeded first try |
| Staleness recovered | 42h | From 06-26 02:03 to 06-28 02:03 |
| New log.md entries | 1 | This gap-fill pass |
| Pre-mirror trigger fired | YES | `$VAULT_LOG_MTIME < $WIKI_LOG_MTIME` correctly classified as gap-fill |

---

## 🧠 Pattern to remember (for future curators)

**The "noop" classification is the most dangerous default.** A curator that sees "0 new transcripts, 0 new sessions" is tempted to declare noop and exit. But the vault can be stale even when the wiki isn't getting new content — because the previous curator skipped the mirror.

**Always run the vault-staleness check FIRST, before the content check.** If vault mtime < wiki mtime, it's a gap-fill regardless of how much new content exists.

```bash
# CORRECT priority order (Step 0):
1. Check vault staleness: $VAULT_LOG_MTIME < $WIKI_LOG_MTIME → gap-fill
2. Check pending work: grep "Pending work" $WIKI/log.md | tail -1 > 0 → gap-fill
3. Check new content: NEW_TRANSCRIPTS == 0 && NEW_SESSIONS == 0 → noop
4. Otherwise → main pass
```

**Anti-pattern:** A curator that runs `find -newer log.md` first and decides "noop" without checking vault staleness will silently let the vault drift indefinitely. This is the failure mode that the 2026-06-28 gap-fill run was designed to prevent.

---

## 📚 Related references

- `references/session-2026-06-25-gap-fill.md` — original gap-fill pattern, smaller scale (1 day staleness)
- `references/session-2026-06-27-structural-pitfalls.md` — background-review toolset constraint + SKILL.md 100K limit (related operational constraints)
- `obsidian` skill § "iCloud Drive sync deadlock" — EAGAIN recovery details (cat>tmp+mv pattern origin)

---

*Reference for nightly-memory-curation skill. Distilled from 2026-06-28 02:00 +07 gap-fill pass.*
*See [[nightly-memory-curation]] SKILL.md § "Step 5b. Always-Mirror Hard Rule" for the operational protocol.*
