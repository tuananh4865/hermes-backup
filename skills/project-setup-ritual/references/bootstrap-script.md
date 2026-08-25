# Bootstrap Script — Quick Reference

## Usage

```bash
bash ~/.hermes/scripts/bootstrap-project.sh {project_id} "{Project Name}" [owner]
```

**Default owner:** `Tuấn Anh` (no need to pass)

**Examples:**
```bash
# Content Creator
bash ~/.hermes/scripts/bootstrap-project.sh content-creator "Content Creator Project"

# TikTok Shop Research
bash ~/.hermes/scripts/bootstrap-project.sh tiktok-shop-research "TikTok Shop Research"

# Custom owner
bash ~/.hermes/scripts/bootstrap-project.sh saas-app "SaaS App Build" "Anh Tuấn"
```

## What it creates (idempotent)

```
wiki/projects/{project_id}/
├── hub.md                  ← From _template/hub.md (placeholders auto-filled)
├── phases/                 ← Empty (will add phase-01-{name}.md)
├── tasks/                  ← Empty
├── research/               ← Empty
├── actions/                ← Empty
└── logs/                   ← Empty (hook will auto-fill on session end)
```

## Idempotency guarantee

- ✅ Safe to run multiple times — won't overwrite existing files
- ✅ Existing folders: prints `⚠️ Exists: {path}` and skips
- ✅ Existing hub.md: prints `⚠️ Exists: hub.md (skip)`
- ⚠️ Compliance check runs anyway (will fail for empty project — expected)

## Post-bootstrap checklist

After bootstrap completes:

1. **Edit `hub.md`** — fill NORTH STAR, TEAM, KPI (placeholders still `{XXX}`)
2. **Create phase-01-{name}.md** in `phases/`
3. **Create first task-{T-01.1}-{name}.md** in `tasks/` (copy from `_template/task.md`)
4. **Log setup** in `actions/{YYYY-MM-DD}-setup-{project_id}.md`
5. **Run compliance**: `bash ~/.hermes/scripts/check-project-compliance.sh {project_id}`

## Verifying bootstrap succeeded

```bash
# Check folder structure
ls wiki/projects/{project_id}/

# Check hub.md has filled placeholders (no {XXX} left)
grep -E "\{[A-Z_]+\}" wiki/projects/{project_id}/hub.md
# → should return nothing (all placeholders filled)

# Check compliance
bash ~/.hermes/scripts/check-project-compliance.sh {project_id} | tail -3
```

## Common pitfalls

1. **Don't run with empty args** — script exits with usage message
2. **Don't put project_id with spaces** — use hyphens: `my-project` not `my project`
3. **Project Name with spaces is OK** — pass in quotes: `"My Project Name"`
4. **Permission denied** — chmod +x the script first: `chmod +x ~/.hermes/scripts/bootstrap-project.sh`