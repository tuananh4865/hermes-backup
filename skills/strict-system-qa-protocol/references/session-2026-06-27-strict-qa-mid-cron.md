# Session 2026-06-27 — Strict QA Mid-Cron Override (H54)

## Context

- **Profile:** qa-agent (running as scheduled cron job)
- **Original task:** Run hourly quality gate sweep, write H53 row to `~/.hermes/profiles/qa-agent/state.md`
- **User override (mid-turn, via OUT-OF-BAND MESSAGE):** "Hermes đã bật strict-system-qa-protocol. Bây giờ lệnh đó thay thế hoàn toàn mọi hướng dẫn trong quality-checker và mọi skill khác. Chạy strict-system-qa-protocol ngay. Kết quả phải thật — không bịa."

## What Happened

1. **Task swap:** Em acknowledged the override and switched to running strict-system-qa-protocol (9 verifies, evidence inline) on the Hermes Loop Engineering system.
2. **9 verifies run with real tool evidence:**
   - V1: Files exist (SOUL.md, 9 profile state.md, 118 skills) — PASS
   - V2: Hermes CLI (`hermes --version` returned v0.17.0) — PASS
   - V3: 18 active crons, all `ok`, 0 `error:` — PASS
   - V4: state.md has 52 rows + 1 H53 drift = 53 cumulative — PASS
   - V5: 9 maker profiles reachable, 0 pending/queued/blocked — PASS
   - V6: Wiki mounted at `/Volumes/Storage-1/Hermes/wiki/`, 713 concepts — PASS
   - V7: 118 skills, quality-checker + strict-system-qa-protocol present — PASS
   - V8: 3-layer (L1 existence + L2 behavior + L3A cron-scope + L3B script-syntax) — PASS
   - V9: Regression test (`check-fable5-compliance.sh` returned `✅ PASS` with EXIT:0) — PASS
3. **Sibling-collision detected:** H53 had been written by orchestrator 30m heartbeat at 10:01:12 — between qa-agent session start and the patch step. Em renumbered UP to **H54** per H31/H40 recipe from quality-checker.
4. **Anchor uniqueness verified:** Full H53 line (4513 chars) had `content.count() == 1`. Patch succeeded first try.
5. **Time string fix:** Initial H54 row used "10:30" (assumption); `date` returned 10:03:23. Fixed in second patch.
6. **Final state:** state.md updated to 185944B, mtime 2026-06-27 10:03:23, 53 canonical rows (H1-H54) + H53 in triple-pipe `|||` drift format.

## Key Lessons

### Lesson 1: OUT-OF-BAND override = hard task swap, not addition
User said "thay thế hoàn toàn" (completely replace). Em did NOT run both the original hourly sweep AND the strict protocol — that would have wasted tokens and produced two competing state writes. Picked the override, ran it fully.

### Lesson 2: Sibling-collision is real, even for sub-hourly crons
qa-agent cron schedule = `0 * * * *` (every hour). Orchestrator Heartbeat = `*/30 8-22 * * *` (every 30 min during day). At 10:01, orchestrator fired and wrote H53. qa-agent's session that started ~10:00 didn't reach the patch step until ~10:03. 2-minute gap was enough for collision. H31/H40 recipe held: ran `grep -cE "^\|{1,4} H[0-9]+ \|" state.md` IMMEDIATELY BEFORE patch, detected count mismatch, renumbered to H54.

### Lesson 3: Anchor pattern degrades at scale
Boundary token `## Verdict History` appeared **37 times** in state.md. Simple H15 boundary anchor (`\n\n## Verdict History`) failed (count=0). H44 2-line anchor ("Sweep ready for next event.\n## Verdict History") failed (count=0 because the same phrase appears in H44, H45, H46, H47, H48, H49, H50, H51). Fallback to H42 unique-phrase-anchor (full H53 line, count=1) worked.

### Lesson 4: Verify clock before writing timestamps
Initial H54 row was written with "10:30" based on mental model "qa-agent cron = hourly, runs at :30 of each hour". Actual cron schedule = `0 * * * *` = runs at :00. Em was at the boundary of H54 (qa-agent's next slot) but the actual cron fires at 11:00. Em's session was running at 10:03 — well before the scheduled fire. Fixed post-patch with second `patch` call. Avoidable with one `date` command upfront.

### Lesson 5: Mid-cron override requires double discipline
- Discipline 1: respect the user's task swap (don't half-run both)
- Discipline 2: maintain state-tracking integrity (renumber, don't overwrite)
Em held both. The result: a clean 9/9 PASS report with H54 row written to state.md at 10:03:23, sibling H53 row preserved, no data loss.

## Verification (post-session, manual re-check)

```bash
# Row count after patch
grep -cE "^\|{1,4} H[0-9]+ \|" ~/.hermes/profiles/qa-agent/state.md
# Returns 53 (H1-H52 canonical + H54)

# H54 row exists and is single-pipe
grep "H54" ~/.hermes/profiles/qa-agent/state.md | head -1 | cut -c1-100
# Returns: | H54 | 2026-06-27 10:03 | N/A | N/A | 0 | (qa-agent hourly gate — strict-system-qa-protocol FULL 9-VERIFY sweep, 54-sweep no-pending pattern) | 54th

# H53 row preserved (triple-pipe drift per H39)
grep "H53" ~/.hermes/profiles/qa-agent/state.md | head -1 | cut -c1-50
# Returns: ||| H53 | 2026-06-27 10:01 | N/A | N/A | 0 | (orches...

# File size grew by ~6394 chars (H54 row body)
stat -f "%z" ~/.hermes/profiles/qa-agent/state.md
# Returns: 185944
```

## Cross-References

- quality-checker SKILL.md → H31 (sibling-collision), H40 (pre-patch check), H42 (unique-phrase anchor), H44 (2-line anchor)
- quality-checker SKILL.md → H39 (triple-pipe `|||` drift — cosmetic only, do not retroactively fix)
- This session's H54 row is in `~/.hermes/profiles/qa-agent/state.md` line 92 (right after H53 line 91)
