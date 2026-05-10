# Hermes External Skills Directory Setup

How to add external skills directories to Hermes Agent via config.yaml.

## The Problem

By default `skill_manage(action='create')` creates skills in `~/.hermes/skills/`. To use a different path (e.g., `/Volumes/Storage-1/Hermes/skills/`), there are two approaches:

### Approach 1: Symlink (OLD — Complex)

```bash
# Move skills to new path
mv ~/.hermes/skills/hermes-autoresearch /Volumes/Storage-1/Hermes/skills/

# Remove old dir and create symlink
rm -rf ~/.hermes/skills
ln -s /Volumes/Storage-1/Hermes/skills ~/.hermes/skills
```

**Drawback:** Symlink is one-directional; `skill_manage` still doesn't know the new path.

### Approach 2: external_dirs config (CORRECT — Recommended) ✅

Add to `~/.hermes/config.yaml`:

```yaml
skills:
  external_dirs:
    - /Volumes/Storage-1/Hermes/skills
```

**Benefits:**
- Hermes automatically scans both local and external dirs
- No symlink needed
- `skill_manage(action='create')` works normally
- Safe, no system impact

## How to do it

### 1. Create skills directory at new path

```bash
mkdir -p /Volumes/Storage-1/Hermes/skills
```

### 2. Add to config.yaml

```yaml
skills:
  external_dirs:
    - /Volumes/Storage-1/Hermes/skills
  creation_nudge_interval: 5
```

### 3. Verify

```bash
hermes skills list
```

Skills from both paths will appear:
- `~/.hermes/skills/` (local)
- `/Volumes/Storage-1/Hermes/skills/` (external)

## Creating new skills after config

Use `skill_manage(action='create')` normally — skill will be created in `~/.hermes/skills/`. Can then be moved to external directory if needed.

## Notes

- `external_dirs` supports multiple paths
- Paths can use `~` or environment variables
- Duplicate paths are automatically skipped
- Local skills (`~/.hermes/skills/`) are unaffected by external_dirs config
