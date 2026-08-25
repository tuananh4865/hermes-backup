# hermes update Failure: "Not a git repository"

## Symptom

```
✗ Not a git repository. Please reinstall:
  curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

`hermes update` fails because `~/.hermes/hermes-agent/` exists but is NOT a git repo (e.g., cloned without git, or corrupted).

## Root Cause

The install script checks if `~/.hermes/hermes-agent/` exists and is a git repo. If it's a plain directory (no `.git/`), it refuses to update.

## Fix Workflow

```bash
# Step 1: Remove corrupted directory
rm -rf ~/.hermes/hermes-agent

# Step 2: Clone fresh (HTTPS, --depth 1 for speed)
git clone --depth 1 https://github.com/NousResearch/hermes-agent.git ~/.hermes/hermes-agent

# Step 3: Run install script
cd ~/.hermes/hermes-agent && bash scripts/install.sh
```

If clone times out (HTTPS fetch-pack disconnect), retry — network flakiness on first fetch.

## When `hermes update` Works Normally

When the directory IS a valid git repo, `hermes update` does `git pull` internally and succeeds without needing the manual workflow above.

## Verification

```bash
# Check if it's a valid git repo
ls -la ~/.hermes/hermes-agent/.git  # should exist

# Or:
cd ~/.hermes/hermes-agent && git status

# Version check (may timeout if gateway is running — check process instead)
ps aux | grep hermes | grep -v grep
```
