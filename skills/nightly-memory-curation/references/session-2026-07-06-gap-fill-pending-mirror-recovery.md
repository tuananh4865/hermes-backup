# Session 2026-07-06 02:00 — Gap-Fill Mirror Recovery + L29-followup Pattern Codification

**Mode:** GAP-FILL (7th of 13 days — 54% gap-fill rate, dominant pattern per L21)
**Trigger:** 3-file staleness check caught log.md 21h stale + index.md 12.1h stale + learned-about-tuananh.md 1.9h stale. Root cause: previous curator (2026-07-05 02:00) explicitly wrote "iCloud mirror verification: Pending" then exited without running the byte-identical check.

## Why this session matters

This is the **L29-followup gap-fill** — codifying the lesson that "Pending" + exit = broken curator pass. The 07-05 run did everything else correctly (3 synthesis pages + 20 merged-into-main redirects + 3 new L-numbered lessons), but the mirror verification step was deferred. The 07-06 cron fired 24h later with vault still lagging. The recovery was straightforward (all 3 mirrors + 13 new files recovered first-try), but the 21h gap exposed a procedural gap in how curator passes close themselves.

## Key Patterns Codified

### 1. "Pending" mirror verification = broken pass (NEW anti-pattern, L29-followup)

**Trigger:** A curator entry ends with `iCloud mirror verification: Pending` or `Mirror recovered: see end of entry` without actually running `diff -q` for the 3 always-mirror files.

**Fix:** Curator entry MUST contain an `iCloud mirror verification` section with actual `diff -q` outputs that returned empty. If verification can't run, re-attempt mirror before ending, OR skip declaring done entirely. Never write "Pending" + walk away.

**Why this matters:** Yesterday's curator (07-05) was 95% complete. The synthesis work was excellent (3 pages, 20 redirects, L29-L31 lessons). But the missing 5% — the byte-identical verification — caused 21h of vault staleness. The agent that runs curator must close the loop on EVERY step, not just the content steps.

### 2. Operational transcripts don't need concept pages (NEW anti-pattern)

**Trigger:** A watchdog stub contains operational work (V2 render, CTA fix, cleanup command, memory-write) that executes an already-codified mandate.

**Test:** Would filling this stub produce ≥2 unique wikilinks AND capture a meta-lesson that doesn't already exist in another synthesis?

- If NO: leave as-is (TODO stub stays) or mark `status: merged-into-main` pointing at the synthesis that contains the mandate being executed.
- If YES: fill with proper synthesis discipline.

**Verified at 2026-07-06:** 11 operational transcripts (09:50, 13:08, 13:54, 13:59, 14:14, 14:23, 14:55, 15:10, 16:20, 16:36, 23:24) — all CTA-fix/flow-match/batch-scale/cleanup commands that execute L29-L31 mandates already in [[tiktok-edit-iteration-4-clip-v1-v2-v4-length-calibration-2026-07-04-05]] and [[pocket3-edit-iteration-4-clip-2026-07-05]]. None needed new concept pages. Left as operational TODOs.

### 3. Track A mirror recovery is mandatory FIRST (verified 07-06)

The 07-06 run executed mirror recovery as Step 1 (before any content updates). This worked first-try with zero EAGAIN escalation:
- log.md: 458604B → 466011B (after curator entry appended)
- learned-about-tuananh.md: 129721B → 137895B (after L32-L34 appended)
- index.md: 41014B → 41468B (after 2 new synthesis entries added)

All 3 mirrored via `sleep 3 + cp -f` pattern, byte-identical verified via `diff -q` returning empty. iCloud was idle at 02:00, so no contention.

### 4. Synthesis-over-fill applied to 2 NEW themes

Today's 17 NEW transcripts (post-07-05 02:00) clustered into 2 NEW themes that warranted synthesis pages:

| Theme | Transcripts | Synthesis page | New L lesson |
|---|---|---|---|
| Whisper model architecture comparison | 5 (13:26, 13:30, 13:38, 13:41, 14:10) | [[whisper-model-architecture-comparison-2026-07-05]] | L32: Decoder-pruning insight |
| Product-selling content workflow | 1 (14:29) | [[content-creator-product-selling-yonex-astrox-2026-07-05]] | (none — covered by L23 advisor-tone preference) |

The 11 operational transcripts were correctly identified as NOT needing synthesis pages (test from pattern #2 above).

### 5. Cross-session pattern list extended (4 patterns, was 3)

The 07-06 synthesis pages + L32-L34 lessons extended yesterday's 3-pattern iteration list to 4 patterns:

| Pattern | Trigger | Optimal response | Lesson |
|---|---|---|---|
| V8→V9 single-rebuild recovery | Source recall contradicts output | Rebuild from source once | L25 |
| V5-V17 chain iteration | Target spec unclear | Iterate to converge | (implicit, 07-01) |
| V1→V4→V1 FRESH | Chain edits feel off | Rebuild V1 fresh from source | L29+L30 |
| V1 FRESH → batch-scale → V2 final + cleanup | Pattern accepted | Scale to N clips + binary delete V_old | L33+L34 |

Future editing sessions can be classified into one of these 4 patterns at the start, which determines the right iteration strategy upfront + cleanup protocol at the end.

## Mirror Verification Pattern (canonical, updated 2026-07-06)

```bash
# Always-mirror files (mandatory every run)
for f in "log.md" "entities/learned-about-tuananh.md" "index.md"; do
  wiki_path="$WIKI/$f"
  vault_path="$VAULT/$(basename $f)"
  
  wiki_size=$(stat -f "%z" "$wiki_path")
  vault_size_before=$(stat -f "%z" "$vault_path" 2>/dev/null || echo 0)
  
  # Try 1: cp with 3s sleep (works for 02:00 cron when iCloud idle)
  sleep 3
  cp -f "$wiki_path" "$vault_path" 2>/tmp/cp_err.log
  sleep 1
  
  new_vault_size=$(stat -f "%z" "$vault_path" 2>/dev/null || echo 0)
  if [ "$new_vault_size" != "$wiki_size" ]; then
    # Escalate: cat to tmp + atomic mv (bypasses mmap lock)
    sleep 20
    cat "$wiki_path" > "$vault_path.tmp" && mv "$vault_path.tmp" "$vault_path"
  fi
  
  # Byte-identical verification (THE GATE)
  if diff -q "$wiki_path" "$vault_path" > /dev/null 2>&1; then
    echo "[OK] $vault_path byte-identical"
  else
    echo "[FAIL] $vault_path NOT IDENTICAL — re-mirror required"
  fi
done

# Concept pages + redirects (batch with sleep 2-3 between each)
for src in /Volumes/Storage-1/Hermes/wiki/concepts/{new-or-changed}.md; do
  name=$(basename "$src")
  sleep 2
  cp -f "$src" "$VAULT/concepts/$name"
done
```

## Verified outcomes (2026-07-06 02:00)

- **Mirror recovery:** All 3 always-mirror files recovered first-try (zero EAGAIN)
- **Synthesis pages created:** 2 (whisper-architecture, content-creator-product-selling)
- **Redirect stubs created:** 11 (10 whisper-architecture + 1 product-selling telegram mirror)
- **L-numbered lessons added:** 3 (L32 decoder-pruning, L33 batch-scale, L34 binary cleanup)
- **Operational stubs left as-is:** 11 (correctly identified as not needing concept pages)
- **New graph edges:** ~56 unique wikilinks across the 2 new pages
- **iCloud mirror verification:** All 17 mirrored files byte-identical (`diff -q` returned empty)

## Lessons for next curator pass

1. **Operational transcripts may accumulate** if a heavy edit day produces 11+ CTA-fix/flow-match/batch-scale commands. The next curator can either leave them as-is (TODOs) or mark them `merged-into-main` with thin redirects pointing at [[tiktok-edit-iteration-4-clip-v1-v2-v4-length-calibration-2026-07-04-05]] and [[pocket3-edit-iteration-4-clip-2026-07-05]] (which contain the L29-L31 mandates being executed). Recommend (a) leave as-is unless user requests cleanup — TODOs are harmless and Obsidian graph shows them as low-value leaves.

2. **Pending skill patches** (out of scope for curator, flagged for coder): 5 tiktok-video-editor mandates need to be codified in the skill: L29 (Mode B 110-120s sweet spot), L30 (fresh-source edit), L31 (4-dim verify), L33 (batch-scale trigger), L34 (binary cleanup). These are 5 mandates accumulated over 2 curator passes that the agent knows but the skill doesn't formally encode.

3. **Cross-domain insight (L32 followup):** The decoder-pruning insight generalizes beyond speech models to Stable Diffusion, GPT variants, vision-language models. The next time a new speech/image/LLM model is released, the right framework is "which axis was optimized?" not "which is bigger?". This framework should be added to a system-wide "model-evaluation" skill eventually — not in scope for curator but flagged.

## When to re-read this reference

- Running a curator pass where the previous entry ended with "Pending" or had a known mirror step deferred
- Facing 10+ operational transcripts that all execute the same mandate — need to decide leave-as-is vs merged-into-main
- Extending the cross-session iteration pattern list (now 4 patterns, will grow as new lifecycle stages emerge)
- Verifying byte-identical mirror state — canonical script above