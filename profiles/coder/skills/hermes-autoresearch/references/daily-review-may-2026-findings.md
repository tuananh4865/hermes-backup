# Daily Review — May 9, 2026 Findings

## Overview
21 regular sessions + cron sessions processed from May 9, 2026. Key systemic discoveries.

---

## Critical Bug: Path Resolution in Cron Context

**SYMPTOM:** Cron jobs using `~/hermes/workers/*/outputs/` paths fail silently because tilde (`~`) does NOT resolve in cron environment.

**ROOT CAUSE:** Cron runs with a different shell context than interactive terminals. The `~` home directory expansion is NOT performed.

**AFFECTED PATHS:**
- `~/hermes/workers/*/outputs/`
- `~/.hermes/cron/output/`

**FIX:** Always use `$HOME` or absolute paths in cron scripts:
```bash
# WRONG in cron scripts:
~/hermes/workers/*/outputs/
~/.hermes/cron/output/

# CORRECT:
/Users/tuananh4865/hermes/workers/*/outputs/
/Users/tuananh4865/.hermes/cron/output/
```

**VERIFICATION:**
```bash
# Test if path resolves correctly
echo $HOME  # Should return /Users/tuananh4865
# In cron, tilde may not expand - use $HOME explicitly
```

---

## Critical: TRÁHN QA Gate Documentation ≠ Enforcement

**SYMPTOM:** Orchestrator cron delivered verbose (~800-char) content despite rules being documented in briefing doc.

**ROOT CAUSE:** Cron jobs run with a **frozen SOUL.md** system prompt. They CANNOT call `skill_view()` to load the briefing reference at runtime. The rules are documented but never actually invoked.

**KEY INSIGHT:** "Documentation in skill ≠ Enforcement in cron."

**IMPLICATION:** 
- Cron skills with briefing references only work for INTERACTIVE sessions
- For CRON sessions, enforcement rules must be BAKED INTO the prompt itself
- Or: enforcement must happen during skill compilation, not at runtime

**PATTERN FOR FUTURE:**
1. Interactive session → `skill_view()` loads briefing → rules enforced ✅
2. Cron session → briefing doc exists but never loaded → rules NOT enforced ❌

**WORKAROUND:** Cron prompts must contain the actual rules inline, not references to rules.

---

## Source Priority Discovery

**FINDING:** Two output locations exist:
1. **PRIMARY:** `~/.hermes/cron/output/{job_id}/` — cron job's direct output
2. **SECONDARY:** `~/.hermes/workers/{worker}/outputs/` — shared worker outputs

**PROBLEM:** Orchestrator was checking SECONDARY (worker outputs/) and finding empty, when PRIMARY (cron output/) had content. This caused false "gap" reporting.

**RULE:** When checking for worker output, check BOTH:
```bash
# Check cron job output (primary)
ls -la ~/.hermes/cron/output/{job_id}/

# AND check worker shared output (secondary)  
ls -la ~/.hermes/workers/{worker}/outputs/
```

---

## HEARTBEAT Staleness Issue

**FINDING:** `HEARTBEAT.md` shows "Today" content that may be stale. The timestamp on the file doesn't match actual today's date.

**RULE:** Cross-reference HEARTBEAT content with actual file timestamps. Don't trust the date in the filename or "Today" label — verify with `ls -la`.

---

## Skills Updated Today

| Skill | Update |
|-------|--------|
| `multi-agent-orchestrator` | Added PITFALL 15 (TRÁHN ≠ enforcement), PITFALL 16 (pre-flight not executed) |
| `tiktok-viral-script` | Added Gen Z ≠ Revenue finding (KOL beta=0.580 vs entertainment beta=0.014) |
| `research-analyst` | Created NEW skill covering Research Agent role |
| `hermes-autoresearch` | Added self-improving agents research (10 new arXiv techniques) |
| `hermes-github-backup` | Added GitHub Secret Scanning fix (auth.json block) |

---

## References

- `references/secret-scanning-fix-2026-05-09.md` — GitHub auth.json block fix
- `references/self-improving-agents-may-2026.md` — 10 new arXiv techniques
- `references/hermes-v0.13-tenacity-release.md` — v0.13 Tenacity Release
- `references/tiktok-algorithm-may-2026.md` — Commerce Signals > Entertainment
- `references/gen-z-slang-may-2026.md` — Gen Z slang update
- `references/orchestrator-morning-brief-2026-05-09.md` — Morning briefing findings

---

*Generated: 2026-05-10 | Session: cron daily_review_0am*
