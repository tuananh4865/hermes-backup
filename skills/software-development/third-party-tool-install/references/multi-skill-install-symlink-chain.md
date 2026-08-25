# Multi-Skill Install via `npx skills add` / `hyperframes skills update`

Class: third-party install where the package provides **N AI agent skills** (not a single CLI). Distinct from single-CLI installs covered in SKILL.md because:

- 1 package → N skill directories (e.g. 19 for HyperFrames)
- Files land in TWO locations (`~/.claude/skills/` AND `~/.hermes/skills/`) — must mirror
- Names may collide with user-protected overrides (e.g. `~/.hermes/skills/creative/hyperframes`)
- Materialization is a 3-hop symlink chain: `hermes` → `claude` → storage-side indirection
- Each skill has its own `SKILL.md` + `references/`, `scripts/`, `templates/` — bulk install

**Verified 2026-07-30** for `heygen-com/hyperframes` v0.7.83 (19 skills).

## Why This Pattern Exists

Hermes owns `~/.hermes/skills/` AND mounts many of the same skills that Claude Code does (`~/.claude/skills/`). A multi-skill install from a third-party repo produces a `.claude-plugin/skills/` or `skills/` directory full of self-contained skill folders. The agent that runs the install must decide:

1. **Where does the canonical content live?** — NEVER inside the source repo (it's read-only); never duplicate on system volume. Materialize under `/Volumes/Storage-1/Hermes/skills/<namespace>-vX.Y.Z/` (Hermes-Only Folder Rule from `hermes-file-edit-logging`).
2. **Where do the entry points point?** — `~/.claude/skills/<name>` AND `~/.hermes/skills/<name>` must both resolve to the storage-side dir. Hermes reads from its own root, but indirecting through `~/.claude/skills/` keeps both loaders in sync with one source of truth.
3. **What's protected?** — anything user-authored in `~/.hermes/skills/creative/<name>` or similar override dirs. NEVER touch.

## The 3-Hop Symlink Chain (canonical pattern)

```
~/.hermes/skills/<name>          symlink →  ~/.claude/skills/<name>
~/.claude/skills/<name>          symlink →  /Volumes/Storage-1/Hermes/skills/<namespace>-vX.Y.Z/<name>
                                                      ↑ REAL DIR (full skill content)
```

Why this works:
- Single source of truth = storage-side dir
- `npx skills add` (which writes to `~/.claude/skills/`) is intercepted by the existing symlink → materializes content at the storage-side dir IF we first delete the `~/.claude/skills/<name>` symlink before running the install. But the cleaner approach is: **materialize manually, then symlink both entry points**. Avoids the tool's clobber behavior.
- Hermes reads `~/.hermes/skills/<name>` → follows symlink to `~/.claude/skills/<name>` → follows symlink to real content. Both agents see the same files.
- User can `rm ~/.hermes/skills/<name>` and `rm ~/.claude/skills/<name>` independently to "uninstall" — storage-side dir remains as a backup.

## Decision Tree: When to Symlink vs Materialize

| Scenario | Decision | Reason |
|---|---|---|
| Skill name collides with `~/.hermes/skills/creative/<name>` or other user override | **Do NOT touch** the override. If new content needs to live elsewhere, materialize under a different name (e.g. `<name>-upstream`) | User overrides are sacred |
| Skill name exists as real dir at `~/.claude/skills/<name>` (from older install) | **Move aside, then symlink** | `rm` on non-empty real dir is destructive; `mv` preserves as `.pre-vX.Y.Z.bak.<ts>` |
| Skill name exists as symlink at `~/.claude/skills/<name>` (already correct) | **No-op** | Idempotent — running recovery script again is safe |
| Skill name doesn't exist anywhere | **Create symlink** | Standard install path |
| Source storage dir doesn't exist | **Create it first**, rsync from upstream repo, then symlink | Step B in main SKILL workflow |

## Pre-Flight Checks (BEFORE doing anything)

```bash
# 1. Source repo is real + has skills/ dir
test -d /Volumes/Storage-1/Hermes/research/<repo>/skills && echo "REPO_OK"

# 2. Storage volume mounted + writable + has space
mount | grep -q '/Volumes/Storage-1 ' && echo "MOUNTED"
[ -w /Volumes/Storage-1/Hermes ] && echo "WRITABLE"
[ $(df -k /Volumes/Storage-1 | tail -1 | awk '{print $4}') -gt 1048576 ] && echo "SPACE_OK"  # > 1 GiB

# 3. Identify ALL user-protected overrides FIRST
find ~/.hermes/skills -maxdepth 4 -name 'SKILL.md' -type f | \
  while read f; do dirname=$(dirname "$f"); \
    # real dir (not symlink) under ~/.hermes/skills/ = potential override
    [ ! -L "$dirname" ] && echo "PROTECTED: $dirname"; done

# 4. Identify current state at every hop
for hop in "~/.hermes/skills" "~/.claude/skills"; do
  for s in <list-of-canonical-skill-names>; do
    p=$(eval echo "$hop/$s")
    if [ -L "$p" ]; then echo "L  $hop -> $(readlink "$p")"
    elif [ -d "$p" ]; then echo "D  $hop"
    else echo "   $hop (missing)"
    fi
  done
done
```

**HARD STOP** if any pre-flight fails. Do NOT proceed with partial state — a dangling symlink breaks Hermes' skill loader silently.

## Recovery Workflow (Re-establish Layout)

Run if any hop is wrong, after `npx skills add` clobbered things, or after repo version bump.

### Step A: Backup current state
```bash
BACKUP=~/.hermes/state/backups/skills-pre-clobber-$(date +%Y%m%d-%H%M%S)
mkdir -p "$BACKUP"
cd ~/.hermes/skills
for s in <collision-candidates>; do
  [ -L "$s" ] && readlink "$s" > "$BACKUP/hermes.${s}.link" || echo "(real)" > "$BACKUP/hermes.${s}.link"
done
cd ~/.claude/skills
for s in <collision-candidates>; do
  [ -L "$s" ] && readlink "$s" > "$BACKUP/claude.${s}.link" || echo "(real)" > "$BACKUP/claude.${s}.link"
done
cp -a ~/.hermes/skills/creative/<override-name> "$BACKUP/" 2>/dev/null || true
echo "$BACKUP" > ~/.hermes/state/last-skills-backup.txt
```

### Step B: Materialize source on storage
```bash
SRC=/Volumes/Storage-1/Hermes/skills/<namespace>-vX.Y.Z
REPO=/Volumes/Storage-1/Hermes/research/<repo>

mkdir -p "$(dirname "$SRC")"
rsync -a --delete "$REPO/skills/" "$SRC/"
ls "$SRC" | wc -l   # expect N canonical skill dirs
```

### Step C: Re-establish `~/.claude/skills` symlinks (preserve any real-dir backups)
```bash
SRC=/Volumes/Storage-1/Hermes/skills/<namespace>-vX.Y.Z
for s in <canonical-names>; do
  link=~/.claude/skills/$s
  if [ -d "$link" ] && [ ! -L "$link" ]; then
    mv "$link" "$link.pre-vX.Y.Z.bak.$(date +%Y%m%d-%H%M%S)"
  fi
  rm -f "$link"
  ln -s "$SRC/$s" "$link"
done
ls -la ~/.claude/skills/<sample-name>  # verify symlink
```

### Step D: Re-establish `~/.hermes/skills` symlinks (NEVER touch creative/<name>)
```bash
SRC=/Volumes/Storage-1/Hermes/skills/<namespace>-vX.Y.Z
for s in <canonical-names>; do
  link=~/.hermes/skills/$s
  rm -f "$link"
  ln -s "../../.claude/skills/$s" "$link"
done

# Belt-and-suspenders: verify all user overrides still real (not symlinks)
find ~/.hermes/skills -maxdepth 4 -name 'SKILL.md' -type f | \
  while read f; do dirname=$(dirname "$f"); \
    [ ! -L "$dirname" ] && echo "OK_PROTECTED: $dirname"; done
```

### Step E: Sanity-check
```bash
# Functional: installer's own check command reports all-current
<installer> skills check   # expect: ✓ N current
hyperframes skills check   # example for hyperframes CLI

# Symlink resolution: readlink -f must point to storage-side dir
for s in <collision-candidates>; do
  final=$(readlink -f ~/.hermes/skills/$s)
  case "$final" in /Volumes/Storage-1/Hermes/skills/*) echo "OK  $s -> $final";; *) echo "FAIL $s -> $final";; esac
done

# Content integrity: source SKILL.md matches storage SKILL.md
diff -q "$SRC"/<sample>/SKILL.md ~/.hermes/skills/<sample>/SKILL.md
```

## Failure Modes (specific to multi-skill installs)

| # | Failure | Symptom | Mitigation |
|---|---|---|---|
| 1 | `npx skills add <repo>` (without `--full-depth`) | Pulls stale `skills.sh` blob lagging `main`; replaces symlink with fresh `npm install` real dir | Always pass `--full-depth`. Or use the installer's own update command (`hyperframes skills update`) which is registry-aware |
| 2 | `npx skills add` without `--skill` (non-interactive) | Installs all N skills as real dirs at `~/.claude/skills/`, breaks symlink chain | Re-run steps C+D to restore symlinks |
| 3 | Storage-1 unmounted | Recovery script aborts mid-chain → dangling symlinks | Pre-check mandatory (see above); HARD STOP if not mounted |
| 4 | Intermediate hop deleted but downstream survives | `~/.hermes/skills/hyperframes` (→ `.claude/skills/hyperframes`) becomes dangling; Hermes loader silently skips | Always delete + recreate in order: `~/.claude/skills` → `~/.hermes/skills`. Never leave orphan |
| 5 | Name collision with user override (`creative/<name>`) | Naïve `cp -r repo/skills/* ~/.hermes/skills/` puts `<name>/` at top level, shadowing the override | Plan NEVER copies to `~/.hermes/skills` directly — only via `.claude/skills` indirection. `<name>` is not in canonical N unless explicitly added |
| 6 | Older `~/.claude/skills/<name>` real dirs from prior installs | `rm -f` on real dir is no-op (rm refuses non-empty); recovery step C hangs | Step C checks `[ -d ] && [ ! -L ]` and MOVES (not deletes) old dir to `.pre-vX.Y.Z.bak.<ts>` |
| 7 | Installer CLI version lags repo (e.g. CLI v0.7.64 vs repo v0.7.83) | `<installer> skills check` may warn "update available" but doesn't break the install | Optional: `npm i -g <installer>@latest`. Not required for skill functionality |
| 8 | Repo gets `git pull`'d to new version | Hard-coded `vX.Y.Z` dir name goes stale | After bump: rename storage dir to new version, re-run B–E. NEVER write skills into the repo |
| 9 | Insufficient disk on Storage-1 | rsync fails | Pre-check ≥ 1 GiB free. Skill trees are typically 10–50 MB |
| 10 | Git LFS missing (golden test baselines in repo) | `git clone` shows LFS pointer files; doesn't affect skills (plain text) | Only relevant for repo dev; out of scope for skill install |

## Versioning Convention

Use **`<namespace>-vX.Y.Z`** for the storage-side dir name:
- `namespace` = upstream package/repo name (e.g. `heygen-hyperframes`, `gsd`, `ai-agent-frameworks`)
- `vX.Y.Z` matches upstream tag/commit (e.g. `v0.7.83`)

This makes the layout self-documenting AND makes `git pull` + dir rename + re-sync trivial.

## Diffing Strategy (when version bumps)

```bash
# Compare old storage dir vs new repo content
diff -qr /Volumes/Storage-1/Hermes/skills/<namespace>-v0.7.83 \
        /Volumes/Storage-1/Hermes/research/<repo>/skills/ \
  | head -50
# Look for: New skill dirs (added), removed skill dirs (deprecated), changed SKILL.md

# Specifically catch SKILL.md version drift
for d in /Volumes/Storage-1/Hermes/research/<repo>/skills/*/; do
  name=$(basename "$d")
  diff -q "$d/SKILL.md" \
          "/Volumes/Storage-1/Hermes/skills/<namespace>-v0.7.83/$name/SKILL.md" \
    2>/dev/null
done
```

If all diffs are silent → version is in sync. Otherwise archive old dir (`mv ... .archive/`) and materialize new.

## Why NOT to `npx skills add` Blindly

The third-party installer (`npx skills add`) does NOT know about:
- The 3-hop symlink chain → it creates real dirs in `~/.claude/skills/`, breaking the storage-side indirection
- User overrides at `~/.hermes/skills/creative/<name>` → it doesn't check before installing a top-level `<name>`
- The Hermes-Only Folder Rule → it scatters real content on the system volume (1–50 MB per skill)

**The installer is useful for verification (`<installer> skills check`)** but the actual materialization must be manual, following this skill's workflow.