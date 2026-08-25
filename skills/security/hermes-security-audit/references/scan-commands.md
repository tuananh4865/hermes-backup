# Scan Commands — Copy-Paste Ready

Drop-in bash blocks for the 7-step audit. Each block is idempotent — safe to re-run.

## Step 1 — Inventory

```bash
echo "=== PROFILE .ENV FILES ==="
find ~/.hermes/profiles -name ".env" -type f 2>/dev/null

echo "=== ALL .ENV* IN HERMES ==="
find ~/.hermes -maxdepth 4 -name ".env*" -type f 2>/dev/null

echo "=== AUTH.JSON FILES ==="
find ~/.hermes -name "auth.json" 2>/dev/null

echo "=== HOOK DIRECTORIES ==="
find ~/.hermes/hooks -maxdepth 1 -type d 2>/dev/null

echo "=== CONFIG.YAML FILES (main + profiles) ==="
ls -la ~/.hermes/config.yaml ~/.hermes/profiles/*/config.yaml 2>/dev/null

echo "=== LOG FILES ==="
ls -la ~/.hermes/logs/*.log 2>/dev/null
```

## Step 2 — File Permission Scan

```bash
echo "=== PROFILE .ENV PERMISSIONS (target: 600) ==="
find ~/.hermes/profiles -name ".env" -type f -exec stat -f "%Sp %Lp %u/%g %N" {} \; 2>/dev/null

echo "=== MAIN .ENV PERMISSIONS (target: 600) ==="
stat -f "%Sp %Lp %u/%g %N" ~/.hermes/.env

echo "=== MAIN CONFIG.YAML PERMISSIONS (target: 600, Pitfall #3) ==="
stat -f "%Sp %Lp %u/%g %N" ~/.hermes/config.yaml

echo "=== PROFILE CONFIG.YAML PERMISSIONS (target: 600, Pitfall #9) ==="
for f in ~/.hermes/profiles/*/config.yaml; do
  [ -f "$f" ] && stat -f "%Sp %Lp %u/%g %N" "$f"
done

echo "=== LOGS/AGENT.LOG PERMISSIONS (target: 600, Pitfall #10) ==="
[ -f ~/.hermes/logs/agent.log ] && stat -f "%Sp %Lp %u/%g %N" ~/.hermes/logs/agent.log
# NOTE: logs/gateway.log is exempt — only startup banner content, see FP catalog

echo "=== AUTH.JSON PERMISSIONS ==="
find ~/.hermes -name "auth.json" -exec stat -f "%Sp %Lp %u/%g %N" {} \; 2>/dev/null

echo "=== ROOT-LEVEL *.DB PERMISSIONS (target: 600) ==="
for f in ~/.hermes/state.db ~/.hermes/state.db-shm ~/.hermes/state.db-wal \
         ~/.hermes/kanban.db ~/.hermes/memory_store.db ~/.hermes/sessions.db \
         ~/.hermes/trajectory_index.db; do
  [ -f "$f" ] && stat -f "%Sp %Lp %N" "$f"
done
```

## Step 3 — Dangerous Pattern Scan

```bash
echo "=== shell=True ==="
grep -rn "shell=True" \
  ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/profiles/*/scripts/*.py \
  ~/.hermes/profiles/*/tools/*.py \
  ~/.hermes/hooks/*/*.py 2>/dev/null \
  | grep -v "__pycache__"

echo "=== eval() ==="
grep -rn "eval(" \
  ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/profiles/*/scripts/*.py \
  ~/.hermes/profiles/*/tools/*.py \
  ~/.hermes/hooks/*/*.py 2>/dev/null \
  | grep -v "__pycache__" \
  | grep -v "ast.literal_eval\|json.loads\|yaml.safe_load"

echo "=== exec() ==="
grep -rn "exec(" \
  ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/profiles/*/scripts/*.py \
  ~/.hermes/hooks/*/*.py 2>/dev/null \
  | grep -v "__pycache__"

echo "=== pickle.loads ==="
grep -rn "pickle\.loads\|pickle\.load(" \
  ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/profiles/*/scripts/*.py \
  ~/.hermes/hooks/*/*.py 2>/dev/null \
  | grep -v "__pycache__"
```

## Step 4 — Hardcoded Secret Scan

```bash
echo "=== KNOWN TOKEN PREFIXES ==="
grep -rEn "sk-[a-zA-Z0-9]{20,}|ghp_[a-zA-Z0-9]{20,}|glpat-[a-zA-Z0-9]{20,}|hf_[a-zA-Z0-9]{20,}|AKIA[0-9A-Z]{16}|anthropic-[a-zA-Z0-9]{20,}|sk-ant-[a-zA-Z0-9]{20,}|sk_live_[a-zA-Z0-9]+|xoxb-[a-zA-Z0-9-]+|xoxp-[a-zA-Z0-9-]+|Bearer eyJ[a-zA-Z0-9_-]+\.eyJ" \
  ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/profiles/*/scripts/*.py \
  ~/.hermes/hooks/*/*.py \
  ~/.hermes/hooks/*.sh \
  ~/.hermes/hooks/*.js 2>/dev/null \
  | grep -v "__pycache__"

echo "=== GENERIC SECRET LITERALS ==="
grep -rEn '(secret|token|api_key|password|passwd|apikey)\s*=\s*["\x27][A-Za-z0-9_\-/+=]{16,}' \
  ~/.hermes/profiles/*/hooks/*.py \
  ~/.hermes/profiles/*/scripts/*.py \
  ~/.hermes/hooks/*/*.py 2>/dev/null \
  | grep -v "__pycache__" \
  | grep -v "os.getenv\|os.environ\|environ\.\|config\.\|settings\.\|getenv("
```

## Step 5 — Hook Directory Permission Scan

```bash
echo "=== HOOK SUBDIRS NOT 700 ==="
find ~/.hermes/hooks -maxdepth 2 -type d ! -perm 700 2>/dev/null

echo "=== HOOK .PY FILES NOT 600 ==="
find ~/.hermes/hooks -maxdepth 2 -type f -name "*.py" ! -perm 600 2>/dev/null

echo "=== HOOK .PY FILES WITH +x BIT ==="
find ~/.hermes/hooks -maxdepth 2 -type f -name "*.py" -perm -u+x ! -path "*/__pycache__/*" 2>/dev/null

echo "=== HOOK_WRAPPER.SH FILES (informational) ==="
find ~/.hermes/hooks -name "hook_wrapper.sh" -exec stat -f "%Sp %Lp %u/%g %N" {} \; 2>/dev/null
```

## Step 6 — Auto-Fix Commands

```bash
echo "=== FIX: Hook subdirs to 700 ==="
find ~/.hermes/hooks -maxdepth 2 -type d ! -perm 700 -exec chmod 700 {} \;

echo "=== FIX: Hook .py files to 600 ==="
find ~/.hermes/hooks -maxdepth 2 -type f -name "*.py" ! -perm 600 -exec chmod 600 {} \;

echo "=== FIX: Strip +x from hook .py files ==="
find ~/.hermes/hooks -maxdepth 2 -type f -name "*.py" -perm -u+x ! -path "*/__pycache__/*" -exec chmod 600 {} \;

echo "=== FIX: Profile .env to 600 ==="
for f in $(find ~/.hermes/profiles -name ".env" -type f); do
  chmod 600 "$f"
done

echo "=== FIX: auth.json to 600 ==="
find ~/.hermes -name "auth.json" -exec chmod 600 {} \; 2>/dev/null

echo "=== FIX: Main config.yaml to 600 (Pitfall #3) ==="
chmod 600 ~/.hermes/config.yaml 2>/dev/null

echo "=== FIX: Profile config.yaml to 600 (Pitfall #9) ==="
for f in ~/.hermes/profiles/*/config.yaml; do
  [ -f "$f" ] && chmod 600 "$f"
done

echo "=== FIX: logs/agent.log to 600 (Pitfall #10) ==="
[ -f ~/.hermes/logs/agent.log ] && chmod 600 ~/.hermes/logs/agent.log
# NOTE: logs/gateway.log is NOT auto-fixed (only startup banner, FP catalog exempt)

echo "=== FIX: Root-level *.db to 600 ==="
for f in ~/.hermes/state.db ~/.hermes/state.db-shm ~/.hermes/state.db-wal \
         ~/.hermes/kanban.db ~/.hermes/memory_store.db ~/.hermes/sessions.db \
         ~/.hermes/trajectory_index.db; do
  [ -f "$f" ] && chmod 600 "$f"
done
```

## Step 7 — Verify After Fix

```bash
echo "=== VERIFY: All hook dirs now 700 ==="
find ~/.hermes/hooks -maxdepth 2 -type d ! -perm 700 2>/dev/null | wc -l
# expect 0

echo "=== VERIFY: All hook .py now 600 ==="
find ~/.hermes/hooks -maxdepth 2 -type f -name "*.py" ! -perm 600 2>/dev/null | wc -l
# expect 0

echo "=== VERIFY: All profile .env now 600 ==="
bad=$(for f in $(find ~/.hermes/profiles -name ".env" -type f); do stat -f "%Lp" "$f"; done | grep -v "^600$" | wc -l)
echo "$bad (expect 0)"

echo "=== VERIFY: All auth.json now 600 ==="
find ~/.hermes -name "auth.json" ! -perm 600 2>/dev/null | wc -l
# expect 0

echo "=== VERIFY: All config.yaml (main + profiles) now 600 ==="
bad=0
for f in ~/.hermes/config.yaml ~/.hermes/profiles/*/config.yaml; do
  [ -f "$f" ] && [ "$(stat -f %Lp $f)" != "600" ] && bad=$((bad+1))
done
echo "$bad (expect 0)"

echo "=== VERIFY: logs/agent.log now 600 ==="
[ -f ~/.hermes/logs/agent.log ] && stat -f "%Lp" ~/.hermes/logs/agent.log
# expect 600
```

## Quick One-Shot (entire audit)

For the cron job, run the steps in sequence:

```bash
# 1+2: permissions
bash -c "$(cat scan-commands.md | sed -n '/Step 1/,/Step 2/p')"

# 3+4: dangerous patterns + secrets
bash -c "$(cat scan-commands.md | sed -n '/Step 3/,/Step 4/p')"

# 5: hook dirs
bash -c "$(cat scan-commands.md | sed -n '/Step 5/,/Step 6/p')"

# 6: auto-fix (only if no CRITICAL findings)
bash -c "$(cat scan-commands.md | sed -n '/Step 6/,/Step 7/p')"

# 7: verify
bash -c "$(cat scan-commands.md | sed -n '/Step 7/,$p')"
```
