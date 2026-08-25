# Session 2026-06-17: Final 5-Agent E2E Chain

> **Date:** 2026-06-17 10:30-10:50
> **Author:** Hermes Agent (Orchestrator, default profile)
> **Context:** Final session in the "create agentic company" series. Created security-engineer and demonstrated full 4-stage chain.

## Summary

Created the 5th and final profile (`security-engineer`) per the `agentic-company-setup` skill's 8-agent architecture. Demonstrated the full **4-stage verification chain** end-to-end: engineering-lead → code-reviewer → security-engineer → qa-agent. All 5 profiles verified via 3-layer (L1 code exists + L2 behavior + L3 future-proof + E2E).

## Profiles Created in This Session

| # | Profile | Role | Model | SOUL Size | E2E Test |
|---|---------|------|-------|-----------|----------|
| 3 | operations-manager | Pure task router | M2.7 | 7.1KB | Routed TikTok scraper task correctly |
| 4 | code-reviewer | 6-axis code review | M2.7 | 6.5KB | APPROVED 9.0/10 on stats.py |
| 5 | security-engineer | 7-cat security audit | M2.7 | 7.0KB | DO_NOT_SHIP on vuln.py, SHIP_OK on secure.py |

## 4-Stage Verification Chain (NEW pattern, 2026-06-17)

```
engineering-lead (build)
    ↓
code-reviewer (style: correctness, style, error handling, type safety, security, testability)
    ↓
security-engineer (vulns: injection, secrets, path traversal, deserialization, perms, CVEs, auth)
    ↓
qa-agent (functionality: independent runtime verification)
    ↓
SHIP (only if all 3 say PASS/APPROVED/SHIP_OK)
```

**Why 4 stages, not 3?**
- code-reviewer catches **style + correctness** issues that security-engineer won't
- security-engineer catches **vulnerability + attack surface** issues that code-reviewer won't
- qa-agent catches **runtime + integration** issues that neither will
- Three separate concerns → three separate agents (no single agent can do all three objectively)

**Trade-off**: 4-stage chain takes longer than 1-stage self-verify. Use it for code that matters (pre-merge, production, security-sensitive). For quick prototypes, 1-stage (just qa-agent) is enough.

## E2E Test Recipe (validated 2026-06-17)

```bash
# Step 1: engineering-lead writes code
~/.local/bin/engineering-lead chat --yolo -q "Create /tmp/el-test/secure.py with read_user_file() that blocks path traversal. Test with 'test.txt' and '../etc/passwd'."

# Step 2: code-reviewer reviews style
~/.local/bin/code-reviewer chat --yolo -q "Review /tmp/el-test/secure.py. Use 6-axis rubric. Output: Verdict, Score, Issues."

# Step 3: security-engineer audits security
~/.local/bin/security-engineer chat --yolo -q "Audit /tmp/el-test/secure.py. Use 7-category checklist. Output: Verdict (SHIP_OK or DO_NOT_SHIP), Score, Findings."

# Step 4: qa-agent verifies functionality
~/.local/bin/qa-agent chat --yolo -q "Verify /tmp/el-test/secure.py functionality. Run it. Output: VERDICT + SCORE + evidence."

# All 4 must say PASS/APPROVED/SHIP_OK to ship.
```

**Observed results** (2026-06-17):
- engineering-lead: wrote correct code, blocked traversal ✓
- code-reviewer: APPROVED 9.0/10 (1 PEP 585 suggestion) ✓
- security-engineer: SHIP_OK 9.0/10 (noted theoretical TOCTOU) ✓
- qa-agent: PASS 9.5/10 (independently verified) ✓

## Separation of Concerns (final matrix)

| Agent | Concern | Output | Verifies |
|-------|---------|--------|----------|
| engineering-lead | Make it work | Code, scripts, hooks | Nothing (creates) |
| code-reviewer | Make it clean | Style/best-practice report | Style, correctness, error handling, type safety, testability |
| security-engineer | Make it safe | Security audit report | Injection, secrets, path traversal, deserialization, perms, CVEs, auth |
| qa-agent | Make it verified | PASS/WARN/FAIL verdict | Functional correctness via independent runtime execution |
| operations-manager | Route it right | Task decomposition + routing | Nothing (routes) |

**Key insight**: Each agent has EXACTLY ONE concern. No agent tries to do another's job. This is the "Maker ≠ Checker" principle applied per concern.

## Pitfalls (2026-06-17)

### 1. M3 timeout on long prompts
**Symptom**: `engineering-lead chat --yolo -q "Write handoff message following your SOUL.md format..."` → timeout 120s.
**Fix**: Switch to M2.7 for code/multi-tool tasks. M3 is fine for fast Q&A but chokes on long generation tasks.
**Rule**: After copying config.yaml, test with PONG. If timeout > 60s on a single-tool task, switch model.

### 2. .env partial copy → 401
**Symptom**: `qa-agent` returned "401 login fail" with valid API key.
**Cause**: Copied only API key + TELEGRAM_*, but not FAL_KEY, AUXILIARY_VISION_*, etc.
**Fix**: `cp ~/.hermes/profiles/coder/.env ~/.hermes/profiles/<agent>/.env` (full file, not grep'd).
**Rule**: When copying .env between profiles, copy the WHOLE file, not just the variables you think you need.

### 3. Don't batch-create profiles
**Tuấn Anh's rule (2026-06-17)**: "Bắt đầu từng cái, làm xong tới đâu check verify lại tới đó đảm bảo mọi thứ hoạt động từng bước."
**Translation**: Create ONE profile, verify it works end-to-end (L1 + L2 + L3), THEN move to the next.
**Anti-pattern**: Create 5 profiles in one batch, verify at the end. If profile 2 has a bug, you have to debug all 5.

## Decision-Style Rules (Tuấn Anh 2026-06-17)

1. **"Khi nào loop kích hoạt?"** — Lead with TRIGGER CONDITIONS and WHEN NOT TO FIRE. Don't propose 3+ profiles preemptively.
   - Good: "Loop activates when: session ends, output > 1 deliverable, or explicit goal set. Does NOT activate for: simple Q&A, conversation, single-file output."
   - Bad: "Should we use A or B or C?" (forces user to choose)
2. **"Tự check không khách quan"** — Self-verification bias is real. ALWAYS route work to a different profile for verification.
3. **"Loop = DO → VERIFY → FIX → LOOP"** — Don't claim done until verified. Verification is part of the loop, not a separate step.

## Architecture Diagram (final state, 2026-06-17)

```
Tuấn Anh (CEO, Telegram: @TyayUno)
    │
    ├── Hermes (default profile, Orchestrator, M3)
    │   │
    │   └── operations-manager (router, M2.7) — pure routing, no work
    │       │
    │       ├── engineering-lead (build, M2.7) — code
    │       │   ↓
    │       │   ├── code-reviewer (style, M2.7) — 6-axis
    │       │   ├── security-engineer (audit, M2.7) — 7-cat
    │       │   └── qa-agent (verify, M3) — INDEPENDENT FINAL GATE
    │       │
    │       ├── content-director (TikTok, M2.7) — content
    │       │   ↓
    │       │   └── qa-agent (verify)
    │       │
    │       ├── research-lead (research, M2.7) — research
    │       │   ↓
    │       │   └── qa-agent (verify)
    │       │
    │       └── memory-curator (wiki, M2.7) — memory
    │           ↓
    │           └── qa-agent (verify)
    │
    └── (future: Telegram bots per profile, cron jobs per profile)
```

## What's Next (post 5-agent setup)

- [ ] Set up cron jobs per profile (auto-run scheduled tasks)
- [ ] Add Telegram bot tokens per profile (channel per agent)
- [ ] Memory-curator integration (track all profiles' state in wiki)
- [ ] Persist state to iCloud (cross-device sync)
- [ ] Real Hermes work via profiles (not /tmp tests)

## Files Changed

- `~/.hermes/profiles/qa-agent/SOUL.md` (8KB) + `state.md`
- `~/.hermes/profiles/engineering-lead/SOUL.md` (7.6KB) + `state.md`
- `~/.hermes/profiles/operations-manager/SOUL.md` (7.1KB) + `state.md`
- `~/.hermes/profiles/code-reviewer/SOUL.md` (6.5KB) + `state.md`
- `~/.hermes/profiles/security-engineer/SOUL.md` (7KB) + `state.md`
- All profiles: `config.yaml` + `.env` + skills (17 categories)

## Test Files Created

- `/tmp/el-test/calc.py` (3 functions: add, subtract, multiply) — qa-agent PASS 10.0
- `/tmp/el-test/avg.py` (calculate_average with type hints) — qa-agent PASS 10.0
- `/tmp/el-test/stats.py` (median + std_dev from statistics module) — code-reviewer 9.0, qa-agent 9.5
- `/tmp/el-test/vuln.py` (intentional vulnerabilities) — security-engineer DO_NOT_SHIP 2.0
- `/tmp/el-test/secure.py` (read_user_file with path traversal guard) — 4-stage chain all PASS

## Verification Summary

**3-layer verify on all 5 profiles**:
- L1 (Code exists): ✅ All 5 profiles have SOUL.md + state.md + config.yaml + .env
- L2 (Behavior works): ✅ All 5 passed real-task tests
- L3 (Future-proof + E2E): ✅ All 5 participated in multi-agent E2E chains

**Total verdicts**:
- 5 profile SOUL.md created
- 5 files written by engineering-lead
- 2 files reviewed by code-reviewer
- 2 files audited by security-engineer
- 4 files verified by qa-agent
- 0 failures (only the intentional vuln.py failed as expected)
