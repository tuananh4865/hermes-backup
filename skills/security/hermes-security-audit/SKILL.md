---
name: hermes-security-audit
description: Cron-driven vulnerability scan of Hermes Agent — file permissions, dangerous Python patterns, hardcoded secrets, hook directory perms, with severity ratings and auto-fix authority. Use when a cron job says "run daily vulnerability scan", "security audit", "scan .env perms", "check shell=True usage", or when the user says "scan hooks for vulnerabilities", "tìm hardcoded API keys", "check hook file permissions".
---

# Hermes Security Audit

Daily cron-driven vulnerability scan for a deployed Hermes Agent install (`~/.hermes/`). Covers file permission drift, dangerous Python patterns in hooks and profile code, hardcoded secrets, and hook directory hygiene. Emits a severity-rated report and auto-fixes CRITICAL/MEDIUM findings under owner authority.

## When to Use

- A cron job invokes the security-engineer profile with "daily vulnerability scan" / "security audit"
- User asks to scan hooks for `shell=True` / `eval()` / `pickle.loads()`
- User asks to verify `.env` and `auth.json` permissions across all profiles
- User asks to grep for hardcoded API keys in their Hermes install

## Scope

In-scope (must scan):
- `~/.hermes/profiles/*/.env` (file perms)
- `~/.hermes/.env` (file perms)
- `~/.hermes/config.yaml` (file perms — provider names/base URLs are sensitive enough to warrant 600; see Pitfall #3)
- `~/.hermes/profiles/*/config.yaml` (file perms — SAME rationale as main config.yaml; see Pitfall #9)
- `~/.hermes/auth.json` + `~/.hermes/profiles/*/auth.json` (file perms)
- `~/.hermes/hooks/**/*.py` (dangerous patterns + perms)
- `~/.hermes/profiles/*/hooks/*.py` and `scripts/*.py` (dangerous patterns + perms)
- `~/.hermes/hooks/` directory perms + nested hook subdir perms
- `~/.hermes/logs/*.log` file perms (especially `agent.log` — see Pitfall #10; `gateway.log` is exempt, see FP catalog)
- Hardcoded API key patterns in hook/profile code (NOT in `.env` content — that is correct usage)
- **Awareness scan** of `~/.hermes/profiles/*/skills/*/scripts/*.py` for `shell=True`/`eval`/`exec` — REPORT ONLY, classify by SKILL.md intent (red-team tools like `godmode` use `exec()` deliberately; see Pitfall #2)

Out-of-scope (do NOT scan):
- `~/.hermes/profiles/*/skills/*/scripts/*.py` PERMISSIONS — these are third-party Hermes Hub skill content, not security-engineer's own code. They will show world-readable perms; that's expected.
- `.env` content for "is this a real secret?" — `.env` SHOULD contain real secrets; check perms, not content.
- macOS Spotlight `.DS_Store` files
- Hermes Agent source code at `~/.hermes/hermes-agent/` (vendored, not user code)
- `.archive/` directories under `profiles/*/skills/.archive/` (excluded by Hermes skill loader; see Pitfall #1)

## The 7-Step Audit

Run these in order. Each step has a deterministic exit state.

### Step 1 — Inventory

```bash
find ~/.hermes/profiles -name ".env" -type f 2>/dev/null
find ~/.hermes -maxdepth 4 -name ".env*" -type f 2>/dev/null
find ~/.hermes -name "auth.json" 2>/dev/null
ls -la ~/.hermes/config.yaml 2>/dev/null
ls -la ~/.hermes/*.db ~/.hermes/*.db-shm ~/.hermes/*.db-wal 2>/dev/null
```

Expected: every profile has one `.env`, main `~/.hermes/.env` exists, auth files exist for OAuth-enabled profiles, config.yaml exists, root-level DB files exist.

### Step 2 — File Permission Scan

```bash
# .env files MUST be 600
for f in $(find ~/.hermes/profiles -name ".env" -type f); do
  stat -f "%Sp %Lp %u/%g %N" "$f"
done
stat -f "%Sp %Lp %u/%g %N" ~/.hermes/.env

# config.yaml MUST be 600 (defense-in-depth — may contain provider names/base URLs)
stat -f "%Sp %Lp %u/%g %N" ~/.hermes/config.yaml

# profile config.yaml MUST be 600 (SAME rationale — provider config; see Pitfall #9)
for f in ~/.hermes/profiles/*/config.yaml; do
  [ -f "$f" ] && stat -f "%Sp %Lp %u/%g %N" "$f"
done

# logs/agent.log MUST be 600 (contains prompt/response history; see Pitfall #10)
# NOTE: logs/gateway.log is exempt — only startup banner content, see FP catalog
[ -f ~/.hermes/logs/agent.log ] && stat -f "%Sp %Lp %u/%g %N" ~/.hermes/logs/agent.log

# auth.json files MUST be 600
find ~/.hermes -name "auth.json" -exec stat -f "%Sp %Lp %u/%g %N" {} \;

# Hot DBs at ~/.hermes root — MUST be 600 (state.db can be 900MB+ with session messages)
for f in ~/.hermes/state.db ~/.hermes/state.db-shm ~/.hermes/state.db-wal \
         ~/.hermes/kanban.db ~/.hermes/memory_store.db ~/.hermes/sessions.db \
         ~/.hermes/trajectory_index.db; do
  [ -f "$f" ] && stat -f "%Sp %Lp %N" "$f"
done
```

Expected: all `.env`, `config.yaml`, `auth.json`, and root-level `*.db` files show `600`.

### Step 3 — Dangerous Pattern Scan

```bash
# shell=True in hook/profile .py (CRITICAL if found)
grep -rn "shell=True" ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/profiles/*/scripts/*.py ~/.hermes/hooks/*/*.py 2>/dev/null \
  | grep -v "__pycache__"

# eval() (exclude safe wrappers)
grep -rn "eval(" ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/profiles/*/scripts/*.py ~/.hermes/hooks/*/*.py 2>/dev/null \
  | grep -v "__pycache__" \
  | grep -v "ast.literal_eval\|json.loads\|yaml.safe_load"

# exec() (CRITICAL if found in hook code)
grep -rn "exec(" ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/hooks/*/*.py 2>/dev/null | grep -v "__pycache__"

# pickle.loads (CRITICAL — arbitrary code execution on untrusted input)
grep -rn "pickle\.loads\|pickle\.load(" ~/.hermes/hooks/*/*.py \
  ~/.hermes/profiles/*/hooks/*.py 2>/dev/null | grep -v "__pycache__"
```

Expected: zero matches in all four scans. If any match, classify as CRITICAL.

### Step 4 — Hardcoded Secret Scan

```bash
# Known token prefixes
grep -rEn "sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|glpat-[a-zA-Z0-9]{20,}|hf_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|anthropic-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}|xoxb-[a-zA-Z0-9-]+|xoxp-[a-zA-Z0-9-]+|Bearer eyJ[a-zA-Z0-9_-]+\.eyJ" \
  ~/.hermes/profiles/*/hooks/*.py ~/.hermes/profiles/*/scripts/*.py \
  ~/.hermes/hooks/*/*.py ~/.hermes/hooks/*.sh ~/.hermes/hooks/*.js 2>/dev/null \
  | grep -v "__pycache__"

# Generic secret = "..." literals
grep -rEn '(secret|token|api_key|password|passwd|apikey)\s*=\s*["\x27][A-Za-z0-9_\-/+=]{16,}' \
  ~/.hermes/profiles/*/hooks/*.py ~/.hermes/profiles/*/scripts/*.py \
  ~/.hermes/hooks/*/*.py 2>/dev/null \
  | grep -v "__pycache__" \
  | grep -v "os.getenv\|os.environ\|environ\.\|config\.\|settings\.\|getenv("
```

Expected: zero matches in both scans. If any match, classify as CRITICAL and report file:line.

### Step 5 — Hook Directory Permission Scan

```bash
# Hook subdirs MUST be 700
find ~/.hermes/hooks -maxdepth 2 -type d ! -perm 700 2>/dev/null

# Hook .py files MUST be 600 (no +x, world-unreadable)
find ~/.hermes/hooks -maxdepth 2 -type f -name "*.py" ! -perm 600 2>/dev/null

# .py files with +x bit (unusual — handler.py should NOT be executable)
find ~/.hermes/hooks -maxdepth 2 -type f -name "*.py" -perm -u+x ! -path "*/__pycache__/*"
```

Expected: zero non-700 dirs, zero non-600 .py files, zero .py with +x bit. Anything wrong = MEDIUM.

### Step 6 — Classify Findings

| Pattern | Severity | Action |
|---------|----------|--------|
| `.env` / `auth.json` not 600 | HIGH | Auto-fix `chmod 600` |
| `config.yaml` (main OR profile) not 600 | HIGH | Auto-fix `chmod 600` (see Pitfall #3 and Pitfall #9) |
| `logs/agent.log` not 600 | LOW | Auto-fix `chmod 600` (see Pitfall #10 — `logs/gateway.log` is exempt, FP catalog) |
| Root-level `*.db` not 600 (state.db, kanban.db, etc.) | HIGH | Auto-fix `chmod 600` |
| `shell=True` in hook/profile code | CRITICAL | Report only — manual fix needed |
| `eval(` not in safe wrapper list | CRITICAL | Report only — manual fix needed |
| `exec(` in hook code | CRITICAL | Report only — manual fix needed |
| `pickle.loads` in hook code | CRITICAL | Report only — manual fix needed |
| Hardcoded API key/token | CRITICAL | Report only — manual review for rotate |
| `shell=True` / `exec()` in `skills/*/scripts/*.py` (e.g. godmode) | MEDIUM | Report with SKILL.md intent context (see Pitfall #2) |
| Hook dir not 700 | MEDIUM | Auto-fix `chmod 700` |
| Hook .py not 600 | MEDIUM | Auto-fix `chmod 600` |
| Hook .py has +x bit | MEDIUM | Auto-fix `chmod 600` (strips +x) |
| Third-party skill .py at 644 (in `skills/*/scripts/`) | NONE | Out of scope — Hermes Hub layout |
| `.archive/` skill content with dangerous patterns | LOW | Informational — excluded by loader (see Pitfall #1) |
| `__pycache__/*.pyc` at 644 in hook subdirs | LOW | Informational — bytecode cache, regenerates |
| `hook_wrapper.sh` at 711 | LOW | Informational — intentional or cleanup candidate |
| gsd-*.sh / gsd-*.js at 755 | LOW | Informational — invoked as executables by Claude Code |

### Step 7 — Auto-Fix & Report

For every CRITICAL/HIGH/MEDIUM, apply the auto-fix command and capture before/after count. Then write the report to `~/.hermes/profiles/security-engineer/state.md` (NOT `state/state.md` — see Pitfall #4) AND emit a severity-rated summary in the cron delivery channel.

**Hard rule:** NEVER auto-fix CRITICAL findings (shell=True, eval, exec, pickle, hardcoded secrets) — those need human review to confirm the fix doesn't break legitimate functionality. Only auto-fix HIGH/MEDIUM (permission drift).

**Scoring convention:** The cron delivery uses a 0–10 score (8.5 = clean, 8.7 = clean with minor findings, 2.0 = critical vulns, 9.0 = perfect). Don't conflate with the C/H/M/L severity buckets — they're orthogonal. Score = base 9.0, minus 1 per unresolved MEDIUM, minus 2 per unresolved HIGH, minus 3 per unresolved CRITICAL, plus/minus 0.2 for clean-vs-noisy context. (See Pitfall #5.)

## Owner Authority — Auto-Fix Bounds

The security-engineer profile runs as a cron job with full filesystem authority over `~/.hermes/`. Auto-fix scope:

| Action | Authorized? | Why |
|--------|-------------|-----|
| `chmod 600` on `.env` / `auth.json` / `config.yaml` (main AND profile) | ✅ Yes | Owner mandate — these MUST be 600 |
| `chmod 600` on `logs/agent.log` | ✅ Yes | Owner mandate — contains prompt/response history (Pitfall #10) |
| `chmod 600` on root-level `*.db` (state.db, kanban.db, etc.) | ✅ Yes | Owner mandate — these contain session/trajectory data |
| `chmod 700` on hook dirs | ✅ Yes | Owner mandate — hook dirs MUST be 700 |
| `chmod 600` on hook .py files | ✅ Yes | Owner mandate — handler code not world-readable |
| `chmod 600` on `.py` with stray `+x` | ✅ Yes | Owner mandate — handlers don't need exec bit |
| Edit/delete `.py` content to remove shell=True | ❌ NO | Could break legitimate hooks — human must review |
| Edit `.env` content (rotate secrets) | ❌ NO | Could lock user out — human must rotate manually |
| Block / disable a hook | ❌ NO | Owner decides which hooks are active |

### Pitfall #6 — `hook_wrapper.sh` at 0o711 (NOT 0o755) is an anomaly
The skill's Common False Positives section only exempts `hook_wrapper.sh` at **0o755** (the normal case for sibling `session-auto-log/hook_wrapper.sh`). A `hook_wrapper.sh` at **0o711** (`-rwx--x--x`) is **NOT** a normal case — group/others can execute but not read. This is unusual and likely the result of a partial `chmod` operation, a copy from a chmod-misconfigured source, or a deploy script that over-permissioned the wrapper. **Auto-fix to 755** (match sibling convention) or **700** (least-privilege). Treat as MEDIUM, not LOW.

**Distinguishing:**
- `0o755` (`-rwxr-xr-x`) = `hook_wrapper.sh` baseline, world-executable. False positive, skip.
- `0o700` (`-rwx------`) = owner-only. Equally fine, false positive, skip.
- `0o711` (`-rwx--x--x`) = world can execute but NOT read. Anomalous. MEDIUM, auto-fix to 755.
- `0o700` with no exec bit = non-executable wrapper, broken. HIGH (handler won't run), auto-fix to 755.
- Any other variant (`0o744`, `0o722`, etc.) = anomaly. MEDIUM, normalize to 755.

**Verified 2026-06-28:** `~/.hermes/hooks/transcript-saver-v2/hook_wrapper.sh` at 0o711 — auto-fixed to 755.

### Pitfall #7 — `.env*` files at 644 in upstream `hermes-agent/` source
`~/.hermes/hermes-agent/.env.example` (vendored from upstream `hermes-agent` repo) ships at 0o644. Not user data, contains only placeholder format like `MINIMAX_API_KEY=sk-your-key-here`. Auto-fix to 600 anyway (defense-in-depth, no harm). Note in report: this file lives in upstream source and may be reset by `hermes update` — fixing once is sufficient, do not flag as recurring.

**Verified 2026-06-28:** `~/.hermes/hermes-agent/.env.example` 644→600, no real keys, no impact on hermes-agent code (it doesn't read this file).

### Pitfall #8 — Masked placeholders trigger hardcoded-secret regex false positives
A real secret never contains literal `...` or repeated `x` in the middle. The Step 4 regex (`sk-[a-zA-Z0-9]{20,}`) matches masked values like `sk-cp-...hU9A` because `-` is in the character class. To avoid noise, exclude these placeholder patterns from the report:

```bash
# After Step 4 grep, filter obvious placeholders:
... | grep -vE "\.{3,}|x{2,}|\\*\\*\\*|<.*>|your[-_ ]?(api[-_ ]?key|token|secret)|example|placeholder|REPLACE_ME|YOUR_|sk-xxx"
```

Real-world examples to recognize:
- `MINIMAX_API_KEY: sk-cp-...hU9A` — masked MiniMax key inside `mcp_servers.MiniMax.env` block (sample MCP server config, not a real assignment). Real MiniMax keys are 32+ chars without `...`.
- `ghp_xx...xxxx`, `sk-xxx...xxxx` — Hermes docs placeholders.
- `Bearer sk-xxx...xxxx` — placeholder auth header in MCP setup docs.

When the regex hits, always inspect file:line and check: (a) is the value inside an `mcp_servers.*.env` sample block? (b) does it contain `...`? (c) is it in a `references/` markdown file? If any of these, classify as LOW false positive, do not auto-escalate.

**Verified 2026-06-28:** 3 `config.yaml` files (`security-engineer`, `operations-manager`, `qa-agent`) at line 537 inside `mcp_servers.MiniMax.env` block contained `MINIMAX_API_KEY: sk-cp-...hU9A` — flagged by Step 4 regex, confirmed as masked placeholder after file:line inspection. False positive, no action.

### Pitfall #9 — `~/.hermes/profiles/*/config.yaml` files drift to 644 (often missed)
The original Step 2 scan only checked `~/.hermes/config.yaml`. Profile-level `config.yaml` files (one per active profile) carry the SAME risk: they contain provider names, base URLs, model IDs, and `mcp_servers.*.env` blocks with masked API key placeholders. Defense-in-depth: they MUST also be 600. Owner-mandated auto-fix.

**Why this gets missed:** Profile directories each have their own `config.yaml` that is created when the profile is provisioned but is NOT touched by every update path that resets the main `~/.hermes/config.yaml`. The main file stays at 600 because every `hermes config set` operation re-saves it with the correct perms, but profile configs are only written when the profile is first created or explicitly edited.

**Affected files in real scans:**
- `~/.hermes/profiles/code-reviewer/config.yaml`
- `~/.hermes/profiles/engineering-lead/config.yaml`
- `~/.hermes/profiles/operations-manager/config.yaml`
- `~/.hermes/profiles/qa-agent/config.yaml`
- `~/.hermes/profiles/security-engineer/config.yaml`

**Action:** Loop over `~/.hermes/profiles/*/config.yaml` in Step 2 scan, not just the main file. Auto-fix any at 644 to 600. Add to Step 7 owner-authority table (same row as main `config.yaml`).

**Verified 2026-06-30:** 5 profile `config.yaml` files at 644, all auto-fixed to 600.

### Pitfall #10 — `~/.hermes/logs/agent.log` is SENSITIVE at 644 (gateway.log is NOT)
The false-positive catalog currently lists `gateway.log` as "exempt at 644" because it only contains the startup banner. `agent.log` is a DIFFERENT log file and is NOT exempt — it contains:
- Full prompt content sent to LLMs (may include user PII, pasted secrets, code snippets)
- Full LLM responses (may include user data in tool outputs)
- Tool call arguments and results
- Error traces that often dump the offending input (sometimes including API keys in error messages)

**Why this gets missed:** A casual `ls -la ~/.hermes/logs/` shows both `agent.log` and `gateway.log` and the auditor assumes both are similar. They are not. `agent.log` is the conversation log; `gateway.log` is the connection-layer log.

**Size at last scan:** `agent.log` was 4MB+ — large enough to be a meaningful exfiltration target.

**Action:** Add `~/.hermes/logs/agent.log` to Step 2 scan. Auto-fix to 600 (LOW severity — defense-in-depth, owner-mandated). Do NOT add `gateway.log` to the scan (false positive per FP catalog).

**Verified 2026-06-30:** `~/.hermes/logs/agent.log` 644→600, no functional impact (only the read permission changed; the running agent process still writes via file descriptor).

### Pitfall #11 — World-writable `.lock` files in venvs are NOT exploitable
`uv` and `pip` venvs create 0-byte `.lock` files at the venv root for concurrency control. Library default perms is `0o666` (world-writable). On macOS this also gets the `@` extended-attribute flag (xattr quarantine).

**Why this is NOT a finding:**
1. Files are 0 bytes — no data to exfiltrate
2. Lock semantics only block concurrent creation, not data access
3. The lock file path is not stable across `uv` versions
4. venvs are local-only (not network-accessible)
5. macOS extended attributes may break the lock semantics, but uv handles that gracefully

**Why it shows up in audits:** Any `find -perm -o+w` sweep flags them. They look alarming because 666 is "world-writable" but in practice they're inert.

**Action:** Add to FP catalog as "informational only, no fix needed." Do not chmod — could break uv's lock detection.

**Affected paths in real scans (2026-06-30):**
- `~/.hermes/hermes-agent/.venv/.lock`
- `~/.hermes/hermes-agent/venv/.lock`
- `~/.hermes/skills/agent-reach/.venv/.lock`

## Pitfalls (verified empirically — June 2026)

### Pitfall #1 — `.archive/` is excluded by Hermes skill loader
Skills under `~/.hermes/profiles/*/skills/.archive/` (leading dot) are NOT loaded by the Hermes skill discovery code, even though they have a valid `SKILL.md`. When you see `shell=True` or `exec()` in `.archive/` paths, classify as **LOW informational** — the files are not loaded, not exploitable through normal use. Do NOT flag as CRITICAL.

**Verified:** 2026-06-27, `coder/skills/.archive/playwright-automation/{playwright_auto.py,scripts.py,export_x_cookies.py}` all contain `shell=True` / `exec()` but are not loaded.

### Pitfall #2 — `skills/red-teaming/godmode/` uses `exec()` intentionally
The `godmode` red-team skill (`research-lead`, `content-director`, `coder` all have it) uses `exec(compile(open(...).read(), ..., 'exec'), ns)` to load sister scripts in the same module — load_godmode.py loads parseltongue.py + godmode_race.py at runtime. This is INTENTIONAL design for the jailbreak research use case. Classify as **MEDIUM with intent context**, not CRITICAL. Always cite the SKILL.md `tags: [jailbreak, red-teaming, ...]` to justify the exception.

**Verified:** 2026-06-27, `load_godmode.py:5,29`, `auto_jailbreak.py:9,52,54`, `godmode_race.py:10`, `parseltongue.py:14`.

### Pitfall #3 — `~/.hermes/config.yaml` is often at 644 (and should be 600)
A bare `chmod 600 ~/.hermes/config.yaml` is a clean fix. `config.yaml` contains provider names, base URLs, and sometimes API key names (never values, but enough to fingerprint the install). Defense-in-depth: 600 is the right target. **Earlier versions of this skill omitted config.yaml from Step 2 — patched 2026-06-27.**

### Pitfall #4 — `state.md` path is `state.md`, NOT `state/state.md`
The actual state file lives at `~/.hermes/profiles/security-engineer/state.md`. The original `references/state-format.md` documented the path as `state/state.md` (with a `state/` subdirectory) — that path does not exist on this install. Always write to `state.md` at the profile root. **Earlier versions of this skill pointed to the wrong path — patched 2026-06-27.**

### Pitfall #5 — Two severity systems in use simultaneously
The skill classifies findings as CRITICAL/HIGH/MEDIUM/LOW. The cron delivery also emits a 0–10 score. These are NOT redundant — they answer different questions:
- **C/H/M/L** = "what's the security severity" (drives auto-fix decision)
- **0–10** = "how healthy is the install overall" (one-line trend tracking across runs)

Base score: 9.0 (clean). Deductions: −3 per unresolved CRITICAL, −2 per unresolved HIGH, −1 per unresolved MEDIUM, +0.2 for "no false positives this run", −0.3 for "no false negatives this run (heuristic)". Don't collapse them.

## State File Format

Every run writes to `~/.hermes/profiles/security-engineer/state.md` (see Pitfall #4). Schema:

```markdown
# Security Engineer — Daily Scan State

**Profile:** security-engineer
**Owner:** Tuấn Anh
**Cron schedule:** Daily

## Last Run: YYYY-MM-DD

**Status:** ✅ PASS — N CRITICAL, N HIGH, N MEDIUM (auto-fixed), N LOW
**Score:** X.X/10

### Scans Performed
(table)

### Findings
#### CRITICAL/HIGH/MEDIUM/LOW (severity, auto-fixed or not)
- **N files** at wrong perms:
  - `<path>` (was X, fixed to Y)
- **Action:** `chmod XXX` on N files
- **Risk:** <one-line>

### Out of Scope (not scanned)
- Third-party Hermes Hub skill scripts (Hub layout)
- macOS Spotlight `.DS_Store`
- `.archive/` skills (excluded by Hermes loader)

### Notes
- No CRITICAL findings this run. / Found N CRITICAL — see findings above.
- All N profile `.env` files consistently at 0o600 — `env-permission-guard` hook is doing its job.

## Run History

| Date | Score | CRITICAL | HIGH | MEDIUM | LOW | Auto-Fixed |
|------|-------|----------|------|--------|-----|------------|
| YYYY-MM-DD | 8.7/10 | 0 | 0 | 2 | 1 | ✅ Yes |
```

## Common False Positives — Exclude These

- `hook_wrapper.sh` at `0o755` OR `0o700` — INTENTIONAL. Must be executable for Hermes gateway. Both baseline and least-privilege are fine.
- `hook_wrapper.sh` at `0o711` (`-rwx--x--x`) — ANOMALOUS, NOT a false positive. Group/others can execute but not read. Auto-fix to 755. See Pitfall #6.
- `gsd-*.sh` / `gsd-*.js` at `0o755` — INTENTIONAL. GSD hooks invoked by Claude Code as executables.
- `eval()` wrapped in `ast.literal_eval` / `json.loads` / `yaml.safe_load` — safe, exclude.
- Third-party skill .py files at `0o644` — out of scope (Hub layout).
- `~/.hermes/.DS_Store` — not a security risk.
- `__pycache__/*.pyc` at 644 in hook subdirs — bytecode cache, regenerates.
- `skills/*/scripts/*.py` with `exec()`/`shell=True` IF the parent `SKILL.md` tags include `red-teaming` / `jailbreak` / `security-research` — intentional design (see Pitfall #2).
- `skills/.archive/*` with dangerous patterns — excluded by loader (see Pitfall #1).
- `logs/gateway.log` at `0o644` — INTENTIONAL. Only contains startup banner + connection status, no user data. Do NOT auto-fix.
- `*.lock` at `0o666` in venvs (e.g. `~/.hermes/hermes-agent/.venv/.lock`) — INTENTIONAL. uv/pip library default. 0-byte, no data. Do NOT auto-fix (see Pitfall #11).
- `*.pem` / `cacert.pem` / `test.key` at `0o644` in venvs — INTENTIONAL. Public CA certs and library test fixtures. World-readable is required.

## Verification

After auto-fix:

```bash
# Re-run the failing scan; count should be 0
find ~/.hermes/hooks -maxdepth 2 -type d ! -perm 700 2>/dev/null | wc -l  # expect 0
find ~/.hermes/hooks -maxdepth 2 -type f -name "*.py" ! -perm 600 2>/dev/null | wc -l  # expect 0
for f in $(find ~/.hermes/profiles -name ".env"); do stat -f "%Lp" "$f"; done | sort -u  # expect "600"
stat -f "%Lp" ~/.hermes/config.yaml  # expect "600"
for f in ~/.hermes/profiles/*/config.yaml; do stat -f "%Lp" "$f"; done | sort -u  # expect "600"
[ -f ~/.hermes/logs/agent.log ] && stat -f "%Lp" ~/.hermes/logs/agent.log  # expect "600"
for f in ~/.hermes/state.db ~/.hermes/state.db-shm ~/.hermes/state.db-wal \
         ~/.hermes/kanban.db ~/.hermes/memory_store.db ~/.hermes/sessions.db \
         ~/.hermes/trajectory_index.db; do
  [ -f "$f" ] && stat -f "%Lp" "$f"  # expect "600"
done
```

Then update `~/.hermes/profiles/security-engineer/state.md` run history table.

## See Also

- `references/scan-commands.md` — copy-paste ready commands for each scan step
- `references/state-format.md` — full state.md template (note: path corrected to `state.md`, not `state/state.md`)
- `references/false-positive-catalog.md` — known false positive patterns (masked placeholders, permission anomalies, sensitive-at-644 cache files) AND a multi-profile replication heuristic (3+ copies = docs not leak) — check BEFORE escalating a new finding
