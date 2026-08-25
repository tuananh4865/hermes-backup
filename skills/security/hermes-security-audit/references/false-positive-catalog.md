# False Positive Catalog — Real-World Patterns

Concrete patterns observed in past runs. When the scan regex fires, check this list FIRST before escalating to a finding. If it matches a known false positive pattern, classify as LOW informational and move on.

## Hardcoded-Key Regex False Positives

### Pattern: `MINIMAX_API_KEY: sk-cp-...hU9A` in `mcp_servers.*.env` blocks

**Where it appears:** `~/.hermes/profiles/*/config.yaml` at line 537 (varies by profile), inside the `mcp_servers.MiniMax.env` block:

```yaml
mcp_servers:
  MiniMax:
    command: uvx
    args: [minimax-coding-plan-mcp, -y]
    env:
      MINIMAX_API_KEY: sk-cp-...hU9A
      MINIMAX_API_HOST: https://api.minimax.io
```

**Why it's a placeholder:** The literal `...` in the middle of the key signals a masked value, not a real assignment. Real MiniMax API keys are 32+ chars without `...` between segments. This block is sample MCP server configuration, not an active credential.

**Affected profiles (verified 2026-06-28):**
- `~/.hermes/profiles/security-engineer/config.yaml:537`
- `~/.hermes/profiles/operations-manager/config.yaml:537`
- `~/.hermes/profiles/qa-agent/config.yaml:537`

**Action:** NONE. Informational only. If more profiles appear in the future, do not flag each one as a new finding — they all share the same placeholder source.

### Pattern: `ghp_xx...xxxx`, `sk-xxx...xxxx`, `Bearer sk-xxx...xxxx` in `references/*.md`

**Where it appears:** Skill reference docs in `~/.hermes/profiles/*/skills/*/references/*.md` — documentation examples showing how to set up GitHub PAT, OpenAI key, or Bearer auth.

**Why it's a placeholder:** `xx...xxxx` and `xxx...xxxx` are clearly mock tokens, not real ones.

**Affected files (verified 2026-06-28):**
- `~/.hermes/profiles/*/skills/autonomous-ai-agents/hermes-agent/references/native-mcp.md` (lines 266, 279, 301, 306) — appears in 4+ profile copies

**Action:** NONE. Documentation placeholders, expected.

### Pattern: Shell usage comments matching key-prefix regex substrings

**Where it appears:** Shell scripts that contain usage strings like `Usage: orchestrate.sh <workspace> "<task-name>"`. The hardcoded-key regex (e.g. `xox[abpr]-|` or `hf_[A-Za-z0-9]{30,}`) can accidentally match substrings in these comments.

**Why it's a false positive:** These are usage examples, not credentials. The match usually picks up 5–10 chars at the end of a long `Usage: <tool>` line.

**How to verify:** Read the matched line. If it contains `Usage:`, `Example:`, `# ` (comment), or `<placeholder>` syntax (angle brackets, ellipses), it's documentation, not a secret.

**Action:** NONE. Informational only. Note in report: "matches pattern: shell usage comment."

**Verified 2026-06-30:** `~/.hermes/profiles/coder/skills/multi-agent-orchestrator/scripts/orchestrate.sh` lines 4, 16 and `~/.hermes/profiles/content-director/skills/multi-agent-orchestrator/scripts/orchestrate.sh` lines 4, 16 — both contain `Usage: orchestrate.sh <workspace>...` and matched part of the API-key regex. Content is usage docs, not credentials.

### Heuristic: multi-profile replication = strong docs signal

If the same exact pattern (file path + line + token shape) appears in **3+ profile copies** of a skill, it's almost certainly documentation that was copied during `hermes skills install` / profile sync, NOT a real leak. Real leaked secrets appear in ONE place (the source), not replicated across profiles.

**Workflow when regex fires:**
1. Count: how many profiles contain the same file path + identical pattern?
2. If ≥3 → confirm via `diff` that the matches are byte-identical (docs) vs divergent (real)
3. Classify as LOW false positive, do NOT escalate
4. Optional: link to source repo to verify (e.g. `hermes-agent` skills come from NousResearch/hermes-agent)

**Verified 2026-06-29:** `references/native-mcp.md` `ghp_xx...xxxx` pattern appears identically in 6 profile copies (`security-engineer`, `operations-manager`, `qa-agent`, `memory-curator`, `code-reviewer`, `test-profile-runner-*`). All sourced from the same upstream `hermes-agent` skill bundle. Documented in hermes-agent skill, NOT a real key.

## Permission Anomaly Patterns (NOT False Positives — Auto-Fix)

### `hook_wrapper.sh` at 0o711

**Where it appears:** `~/.hermes/hooks/transcript-saver-v2/hook_wrapper.sh` (verified 2026-06-28).

**What 0o711 means:** `-rwx--x--x` — owner: rwx, group: --x, others: --x. Group/others can execute but NOT read. This is unusual; baseline is 0o755 (group/others: r-x) or 0o700 (owner only).

**Why it matters:** Even though `handler.py` is 600 (so the wrapper can't be used to read secrets), the 0o711 mode is a defense-in-depth violation and inconsistent with the rest of the hook system. A future script that happens to live in the same dir and get the same perms could expose data.

**Action:** `chmod 755 <wrapper>` to match sibling `session-auto-log/hook_wrapper.sh`. MEDIUM severity, auto-fix.

### `logs/agent.log` at 0o644

**Where it appears:** `~/.hermes/logs/agent.log` (verified 2026-06-30).

**What 0o644 means:** `-rw-r--r--` — owner can read/write, group/others can read.

**Why it matters:** `agent.log` is the agent conversation log — it contains:
- Full prompt content sent to LLMs (may include user PII, pasted secrets, code snippets)
- Full LLM responses (may echo user data in tool outputs)
- Tool call arguments and results
- Error traces that often dump the offending input (sometimes including API keys in error messages)

This is DIFFERENT from `gateway.log` (which is exempt from 644-fix because it only has the startup banner). `agent.log` is the sensitive log.

**Action:** `chmod 600 ~/.hermes/logs/agent.log`. LOW severity, auto-fix (defense-in-depth, owner-mandated). The running agent process keeps writing via file descriptor, so the live write path is unaffected.

### Profile `config.yaml` at 0o644 (one or more of `~/.hermes/profiles/*/config.yaml`)

**Where it appears:** Multiple profile directories. Common drift pattern — verified 2026-06-30 in:
- `~/.hermes/profiles/code-reviewer/config.yaml`
- `~/.hermes/profiles/engineering-lead/config.yaml`
- `~/.hermes/profiles/operations-manager/config.yaml`
- `~/.hermes/profiles/qa-agent/config.yaml`
- `~/.hermes/profiles/security-engineer/config.yaml`

**What 0o644 means:** World-readable config file containing provider names, base URLs, model IDs, and `mcp_servers.*.env` blocks (which contain masked API key placeholders).

**Why it matters:** Even though the masked placeholders are not real keys, the surrounding metadata (provider list, model list, MCP server config) is enough to fingerprint the install. A leaked config.yaml reveals the user's stack.

**Action:** `chmod 600` on every `~/.hermes/profiles/*/config.yaml` that is at 644 or higher. HIGH severity (defense-in-depth), auto-fix.

### `.env.example` at 0o644 in upstream `hermes-agent/`

**Where it appears:** `~/.hermes/hermes-agent/.env.example` (verified 2026-06-28).

**What it is:** A template file shipped from the upstream `hermes-agent` git source. Contains placeholder format like `MINIMAX_API_KEY=***`, no real keys.

**Why 0o644 is wrong:** `.env*` files should be 600 by default, even templates. The hermes-agent code does not read this file, so changing it has no functional impact, but defense-in-depth says 600.

**Action:** `chmod 600`. LOW severity, auto-fix. **Note:** This file may be reset by `hermes update` — fixing once is sufficient. Do not flag as recurring in subsequent runs.

## Permission Patterns That LOOK Like Findings But Are NOT (False Positives)

### World-writable `.lock` files in venvs at 0o666

**Where it appears:**
- `~/.hermes/hermes-agent/.venv/.lock`
- `~/.hermes/hermes-agent/venv/.lock`
- `~/.hermes/skills/agent-reach/.venv/.lock`

**What 0o666 means:** `-rw-rw-rw-` — world-writable empty file. Looks alarming in `find -perm -o+w` output.

**Why it's NOT a finding:**
1. Files are 0 bytes — no data to exfiltrate
2. Lock semantics only block concurrent creation, not data access
3. Lock file path is not stable across `uv` versions (may be removed in future releases)
4. venvs are local-only (not network-accessible)
5. macOS extended attributes (`@` flag) may break the lock semantics, but uv handles that gracefully

**Action:** NONE. Do not chmod — could break uv's lock detection. Add to FP catalog as informational only.

**Verified 2026-06-30:** 3 lock files flagged, all 0-byte, all skipped from auto-fix.

### `logs/gateway.log` at 0o644

**Where it appears:** `~/.hermes/logs/gateway.log`.

**What 0o644 means:** World-readable.

**Why it's NOT sensitive:** `gateway.log` only contains the gateway startup banner, platform connection status, and routine INFO-level connection events. No prompt content, no tool output, no user data.

**Action:** NONE. Exempt from 644-fix. Note: this is DIFFERENT from `logs/agent.log` (which IS sensitive — see above).

### `*.pem` CA certificates and `*.key` test fixtures at 0o644 in venvs

**Where it appears:**
- `~/.hermes/hermes-agent/.venv/lib/python3.12/site-packages/botocore/cacert.pem`
- `~/.hermes/hermes-agent/.venv/lib/python3.12/site-packages/pip/_vendor/certifi/cacert.pem`
- `~/.hermes/hermes-agent/.venv/lib/python3.12/site-packages/certifi/cacert.pem`
- `~/.hermes/hermes-agent/.venv/lib/python3.12/site-packages/tornado/test/test.key`
- (Same files for python3.11 venv)
- `~/.hermes/skills/agent-reach/.venv/lib/python3.12/site-packages/certifi/cacert.pem`

**Why they're at 644:** Public CA certificate bundles (cacert.pem) and Tornado's test fixture key (test.key) ship world-readable. They MUST be world-readable for TLS verification and library test suites to work.

**Action:** NONE. Library default, not user data, not sensitive.

## Files That ARE Sensitive at 644 (Owner-Authorized to Keep)

These top-level files at `~/.hermes/` are at 0o644 and contain cache/state data. They are NOT secret (no hardcoded keys, just internal IDs/process metadata) and the owner has not authorized auto-fixing them. Note in report as informational:

| File | Size | Content type | Risk |
|------|------|--------------|------|
| `gateway.log` | ~1-4KB | Gateway startup banner | None — no secrets |
| `gateway_state.json` | ~500B | Active platform connections | Low — platform names only |
| `gateway.lock` | 0B | Empty lock file | None |
| `auth.lock` | 0B | Empty lock file | None |
| `processes.json` | varies | Running PIDs + child processes | Low — internal process state |
| `trajectory_samples.jsonl` | ~890KB | Sample agent trajectories (prompt/response) | Medium — could contain user PII in conversations. Owner-acceptable at 644 because data is anonymized samples. |
| `autoresearch.jsonl` | ~5-6KB | Autoresearch run history | None — metric data only |
| `settings.json` | ~4KB | Hook config (SessionStart, etc.) | None — no secrets |
| `context_length_cache.yaml` | varies | Model context length cache | None |
| `state.md` | varies | Loop engineering state | None |
| `feishu_seen_message_ids.json` | 19B | Feishu message dedup IDs | None |
| `*.pid`, `*.lock` | 0-200B | Process/lock files | None |
| `config.yaml.bak.*` | varies | Config backups | **Should be 600** — these contain provider config including `mcp_servers.MiniMax.env` block with the masked placeholder. Owner has not authorized auto-fixing backups. Informational. |

**Verified 2026-06-28:** All 12 files inspected, no hardcoded keys, all consistent with above risk table.

## Re-Scan Strategy

Before reporting a new finding, check:
1. Does the file path match a known false positive in this catalog? → Skip, note "matches FP catalog N".
2. Is the regex match a masked placeholder (`...` in middle)? → Filter out, see Pitfall #8.
3. Is the regex match inside a `references/*.md` file? → Likely docs placeholder, filter out.
4. Is the regex match inside a shell `Usage:` / `Example:` / `#` comment? → Filter out, see Shell Usage Comments pattern above.
5. Is the perm a known acceptable variant (755, 700 for hook_wrapper.sh)? → Skip, false positive.
6. Is the perm a known anomaly (711, 0o744, etc.)? → Auto-fix per Pitfall #6.
7. Is the file a venv `.lock` at 0o666? → Skip, not exploitable, see World-writable .lock files above.
8. Is the file a venv `cacert.pem` / `test.key` at 0o644? → Skip, public certs/test fixtures, see *.pem CA certificates above.

If none of the above, classify per Step 6 severity table.
