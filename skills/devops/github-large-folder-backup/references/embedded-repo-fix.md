# Embedded Git Repo Fix — Worked Example

**Source session:** Hermes daily backup cron job, 2026-06-13.

## Symptom
`git add .` inside `~/.hermes` (a parent repo backing up the whole Hermes tree) emitted:

```
hint: You've added another git repository inside your current repository.
hint: Submodules in git are not supported on filesystems that don't have
hint: the ability to ignore the contents of the .git directory.
hint: If you'd like to add this path anyway, use:
hint:
hint: 	git rm --cached skills/agent-reach
hint:
hint: See "git help submodule" for more information.
```

`git submodule status` confirmed:
```
fatal: no submodule mapping found in .gitmodules for path 'skills/agent-reach'
```

## Diagnosis
`skills/agent-reach` is an **installed Hermes skill bundle** — a real git repo
with its own `.git/` history that the parent backup repo had once tracked as a
subtree. The parent repo's `.gitmodules` no longer has a mapping for it (stale
state), so git refuses to re-add it as a regular tracked directory.

## Why NOT to use the skill's default fix
`github-large-folder-backup` Step 1 prescribes:
```bash
find /path/to/folder -name ".git" -type d -exec rm -rf {} \;
```
**DO NOT run this on `skills/agent-reach`.** The bundle's `.git/` is part of
the skill install — deleting it breaks the skill (loses version pinning, makes
the skill un-updatable via `hermes skills update`). This fix is only safe for
disposable nested clones (e.g. old wiki snapshots, throwaway checkouts).

## Correct fix — untrack, don't destroy
```bash
cd ~/.hermes
git rm --cached -r skills/agent-reach   # untrack from parent index
git add .                                 # retry — succeeds, dir kept locally
git commit -m "Backup hermes full: $(date +%Y-%m-%d)"
git push origin main
```

After this, the directory still exists on disk and the skill still works.
It is simply not in the parent backup repo's tracked set.

## Optional: silence the advisory permanently
The warning fires on every `git add` for that path. To stop it:
```bash
git config set advice.addEmbeddedRepo false   # repo-scoped, not global
```

## Verify
```bash
git ls-remote origin main
# Local HEAD SHA should match the SHA returned for refs/heads/main.
# Catches silent auth-fail or non-fast-forward that `git push` exit-0
# doesn't always surface.
```

## When to apply this fix (decision rule)
| Path is under... | Use `git rm --cached` | Use `find -delete .git` |
|------------------|----------------------|-------------------------|
| `skills/`, `plugins/`, `profiles/*/skills/` | ✅ yes | ❌ never — breaks install |
| Throwaway clones, old snapshots, scratch dirs | ❌ no | ✅ yes |
| Unknown / can't tell | ✅ `git rm --cached` is always safe | only if you're sure it's disposable |

## Related
- Pitfall #5 in SKILL.md — the rule encoded from this session.
- Pitfall #6 — silencing the warning after untrack.
- Pitfall #7 — push verification via `git ls-remote`.
