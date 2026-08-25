# Security-Engineer Daily Sweep Protocol (2026-06-25)

## Scope of this file

The `multi-agent-heartbeat` SKILL.md covers the **wrapper** protocol — when the
orchestrator runs, what report shape to emit, how to integrate with state.md.
It does NOT cover the **specific scan recipe** the security-engineer profile
runs when its daily 03:00 cron fires.

This file is that recipe — a self-contained playbook that the security-engineer
agent loads on its own cron prompt ("Run daily vulnerability scan") and executes
end-to-end. It pairs with `references/h24-profiles-perm-blind-spot.md` (which
covers perm regression detection FROM the heartbeat side) by covering the
comprehensive sweep FROM the security-engineer side.

## Why this is a separate file

The security-engineer daily scan is NOT a generic chmod watch. It is a
**multi-category security audit** with severity classification, auto-fix
authority, and a state.md verdict log. The heartbeat's "security regression
watch" section (SKILL.md → "Security regression watch (the chmod pattern)")
covers only the perms category. The full sweep adds:

1. **Code-pattern scan** (shell=True, eval(), pickle.loads(), yaml.load())
2. **Hardcoded secret scan** (real VALUES, not just template placeholders)
3. **Hooks subdir + file perm audit** (recursive, not just parent dir)
4. **State-snapshot config.yaml sweep** (the H24 blind spot, again — these
   files keep regressing because the snapshot dir is touched by update
   scripts that write 644)
5. **Severity classification** (CRITICAL/HIGH/MEDIUM/LOW)
6. **Auto-fix policy** with pre-fix plaintext-secret check

## The 7-category checklist (the actual scan)

When the cron prompt says "Run daily vulnerability scan", the security-engineer
must run all 7 categories. Skipping any is a coverage gap.

| # | Category | What to check | Tools |
|---|----------|---------------|-------|
| 1 | Profile `.env` perms | 11 profile dirs, all `.env` files should be 600 | `stat -f "%Sp %N" ~/.hermes/profiles/*/.env` |
| 2 | Dangerous `.py` patterns | `shell=True`, `eval()`, `pickle.loads()`, `yaml.load()`, `os.system()` | `search_files pattern` over 413 .py files in profiles/ |
| 3 | Hardcoded API keys | Real VALUES of sk-..., ghp_..., xoxb-..., AIza..., AKIA..., hf_... | `grep -rEn "(sk-[A-Za-z0-9]{20,}\|ghp_[A-Za-z0-9]{30,}\|...)"` |
| 4 | Hooks perm (parent) | `~/.hermes/hooks/` should be 700 | `stat` |
| 4a | Hooks perm (subdirs) | Every subdir should be 700 (NOT 755) | `find ~/.hermes/hooks -mindepth 1 -maxdepth 1 -type d` |
| 4b | Hooks perm (handler.py files) | Every handler.py should be 600 (NOT 644) | `find ~/.hermes/hooks -name "*.py"` |
| 5 | State-snapshot perms | `config.yaml`, `auth.json` in `state-snapshots/*/pre-update/` should be 600 | `find ~/.hermes/state-snapshots -name "config.yaml" -o -name "auth.json"` |
| 6 | Hooks shell scripts | `node -e` with inline JS, `exec python3 << EOF` | grep + visual review |
| 7 | auth.json perms (root + profiles) | Every `auth.json` should be 600 | `find ~/.hermes -name "auth.json"` |

### The hooks subdir blind spot (2026-06-25 lesson)

**Pitfall:** Checking only `~/.hermes/hooks/` (parent dir) as 700 is NOT
sufficient. Subdirs were 755 in the 2026-06-25 sweep, leaking structure listing
to all local users on the Mac.

**Symptom:** `ls ~/.hermes/hooks/` returns no entries for a world user (parent
700 blocks list), but `ls ~/.hermes/hooks/transcript-saver-v2/` works (subdir
755 grants list+execute to world).

**Correct full check:**
```bash
find ~/.hermes/hooks -mindepth 1 -maxdepth 1 -type d -exec stat -f "%Sp %N" {} \;
# All must be drwx------
```

### The 3 handler.py 644 blind spot (2026-06-25 lesson)

**Pitfall:** Out of 8 hooks handler.py files, 4 were 600 (correct) and 4 were
644 (world-readable). The 644 ones process session transcripts and may touch
auth context. A partial `stat` of `~/.hermes/hooks/*/handler.py` catches them
all, but a `find ~/.hermes/hooks -name "handler.py" | xargs stat` works too.

**Fix recipe:** All 8 handler.py files must be 600. No exceptions.

### The state-snapshot config.yaml blind spot (H24 again, 2026-06-25)

**Why this regresses repeatedly:** The `state-snapshots/<date>-pre-update/`
dirs are written by update scripts that `cp -p` config.yaml from a 644 source
or write 644 by default. Every major Hermes update re-creates this regression.

**Fix recipe:** Always include state-snapshots in the daily sweep. The H24
find-based recipe (`find ~/.hermes -maxdepth 3 -name "config.yaml" ...`) DOES
catch state-snapshots if `-maxdepth 3` is used and the path is not excluded.

## Severity classification

| Severity | Triggers | Auto-fix? | Owner authority |
|----------|----------|-----------|-----------------|
| **CRITICAL** | Any perm drift on `.env`, `auth.json`, `config.yaml`, `*.db`, handler.py, hooks subdirs | YES if no plaintext secret found | security-engineer |
| **HIGH** | Real hardcoded API key VALUE (not placeholder) | NO — escalate to user, file has a real secret leak | user (security-engineer flags only) |
| **MEDIUM** | `shell=True` in `.archive/` or docs (not loaded), 0711 hook wrapper.sh, cosmetic perm quirks | NO — informational, document only | n/a |
| **LOW** | `.DS_Store` presence, doc placeholders like `sk-xxx...xxxx` | NO — informational | n/a |

## Pre-fix content check (CRITICAL — do not chmod blindly)

Before auto-fixing perms with `chmod 600` or `chmod 700`:

```bash
# Quick grep for plaintext secrets
grep -E "(api_key|api_secret|token|secret|password):" <file> | head -5
```

| Result | Action |
|--------|--------|
| Only `env:VAR_NAME` references, empty strings, or `no-key` | ✅ Safe to chmod |
| Literal `sk-cp-...`, `ghp_...`, `hf_...`, etc. | ❌ STOP — escalate to user. The file has a real secret AND wrong perms; user must rotate the secret AND fix perms. |
| `access_token: ***` (masked) | ✅ Safe — the system has already masked it; chmod fine |

## Auto-fix policy (the decision tree)

```
For each finding:
  Is severity CRITICAL?
    NO  → Document in MEDIUM/LOW section. Done.
    YES → Run pre-fix content check.
      Has plaintext secret?
        YES → Escalate to user. Do NOT chmod. Do NOT touch file.
        NO  → Auto-fix (chmod). Log in auto-fixes section.
```

**Why no auto-fix for HIGH:** A literal `sk-cp-...` in a config file means the
secret is leaked to any user who can read the file (which is everyone if the
file was 644). Chmod fixes the perms but the secret is already in shell
history, git log, backups, etc. User must rotate.

## State.md update format

The security-engineer `state.md` follows this exact template. The audit row
goes in `## Recent Audits`, then a new `## Daily Scan Findings (YYYY-MM-DD)`
section, then a `## PASS (N categories)` list, then `## Auto-fixes Applied`
section.

### Verdict row template

```
| # | Time | Target | Verdict | Score | Critical | High | Medium | Low |
|---|------|--------|---------|-------|----------|------|--------|-----|
| N | <ISO> | ~/.hermes daily sweep (<scope>) | <VERDICT> | <X>/10 | <C> | <H> | <M> | <L> |
```

Verdict semantics:
- `CLEAN` — 0 CRITICAL/HIGH, all PASS categories met
- `CLEAN_AFTER_FIX` — CRITICAL findings detected AND auto-fixed (most common)
- `CRITICAL_FOUND` — CRITICAL findings detected that require user action
- `PARTIAL` — Some categories skipped (e.g. cron interrupted, network unavailable)

### Daily Findings section template

```markdown
## Daily Scan Findings (<YYYY-MM-DD>)

### CRITICAL (<N> → AUTO-FIXED)
1. **<description>** — <impact>
   - **Files:** <list>
   - **FIXED:** <chmod command>. Verified.

### HIGH (0)
None.

### MEDIUM (<N>)
1. **<description>** — <impact>. **NOT FIXED** — <reason>.

### LOW (<N>)
None.

### Auto-fixes Applied (<YYYY-MM-DD>)
1. <N>× <path pattern> <old_mode>→<new_mode>
2. ...

### PASS (N categories)
- ✅ <category 1>
- ✅ <category 2>
...
```

## Tool-call ordering (the actual execution recipe)

The security-engineer daily sweep must run tool calls in this order to avoid
double-reading:

```
Round 1 (parallel):
  - ls -la ~/.hermes/profiles/                    # discover profile dirs
  - find ~/.hermes/profiles -name ".env*"         # discover .env files
  - find ~/.hermes/profiles -name "*.py"          # discover .py files
  - ls -la ~/.hermes/hooks/                       # discover hooks

Round 2 (parallel, after Round 1 results):
  - stat -f "%Sp %u %g %N" <all .env paths>       # perm check
  - find <hooks dir> -mindepth 1 -type d           # subdir perms
  - search_files pattern=shell=True ...           # dangerous code patterns
  - search_files pattern=eval(   ...
  - search_files pattern=pickle.loads? ...
  - terminal command for hardcoded key grep       # use real-value regex

Round 3 (after findings aggregated):
  - chmod commands (parallel)                      # auto-fix
  - verification stat commands (parallel)          # confirm fix

Round 4 (single):
  - patch state.md (frontmatter + verdict row + daily findings section)
  - chmod 600 the state.md after write             # protect the log itself
```

**Why this ordering matters:** Round 1 gives you the file lists. Round 2 needs
those lists to know what to stat. Round 3 needs the findings from Round 2 to
know what to fix. Round 4 must come AFTER all fixes are verified, because if
a fix verification fails, the state.md entry must reflect "fix attempted but
unverified" rather than "CLEAN_AFTER_FIX".

## Single-turn discipline

Per `multi-agent-heartbeat`'s "single-turn discipline" section, the daily sweep
should complete in 1 turn:

- 4 tool-call rounds (Round 1-4 above), all in the same response
- 1 final response with the report
- No polling, no re-validation
- If a check is ambiguous, note the ambiguity in the row and move on

If the sweep produces >50 findings, that's a signal the system has drifted
significantly — escalate to user in the response rather than trying to
auto-fix everything.

## Co-trigger with heartbeat

The security-engineer daily cron (03:00) and the qa-agent heartbeat (30m)
overlap on the perm regression watch. When the heartbeat's perm watch
catches a regression, it auto-fixes via the H11 owner-authority pattern
(LOW severity, reversible). The security-engineer's daily sweep then
**validates** the auto-fix is still holding AND catches the categories the
heartbeat doesn't watch (code patterns, secrets, hooks subdirs, snapshots).

This is intentional: the heartbeat is the **fast detector** (every 30m),
the security-engineer is the **deep validator** (once daily). The H11
owner-authority allows both to chmod without user approval, but the
security-engineer also documents WHY each chmod was needed in state.md.

## Related files

- `references/h24-profiles-perm-blind-spot.md` — the H24 lesson that originated
  the find-based perm sweep. The daily scan uses the same find pattern.
- `references/in-process-sweep-vs-delegate.md` — when the heartbeat detects
  the security-engineer daily scan is overdue, it runs the scan in-process
  via execute_code. The recipe in this file is what the in-process sweep
  implements.
- `SKILL.md` "Security regression watch" section — the heartbeat-side pattern
  this file complements.

## Real session this was derived from

- 2026-06-25 03:00 — security-engineer daily cron. Caught 2 CRITICAL findings
  (7 hooks subdirs at 755, 3 handler.py at 644), 1 MEDIUM (hook wrapper.sh at
  0711), 0 HIGH/LOW. Auto-fixed all CRITICAL. Final verdict: CLEAN_AFTER_FIX,
  9.0/10. Auto-fixed bonus: 2 state-snapshot config.yaml that the H24 find
  recipe caught but the previous day's sweep missed (because `state-snapshots`
  was in the `-not -path` exclusion list).
