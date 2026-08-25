# Real Daily Backup Run — 2026-06-15

## Setup
- Source repo: `~/.hermes` (branch `main`)
- Remote: `https://github.com/tuananh4865/hermes-backup.git`
- Trigger: cron job, scheduled run
- Time: Mon Jun 15 2026

## Pre-flight output
```
$ git status --short 2>&1 | head -30
 M .skills_prompt_snapshot.json
 D .update_check
 M .wiki_session_context.txt
 M channel_directory.json
 M cron/dojo/state.json
 M cron/jobs.json
 M cron/last_task_check.json
 M cron/proactive_research.json
 M cron/tiktok-monitor/lessons/cta.md
 M cron/tiktok-monitor/lessons/hooks.md
 M cron/tiktok-monitor/lessons/storytelling.md
 M cron/tiktok-monitor/lessons/tiktok-shop.md
 M cron/tiktok-monitor/seen-videos.json
 M disk-cleanup/tracked.json
 M dojo/tasks.json
 M gateway.pid
 M gateway_state.json
 M hermes-agent/.dockerignore
 M hermes-agent/.github/workflows/deploy-site.yml
 M hermes-agent/.github/workflows/docker-publish.yml
 M hermes-agent/.github/workflows/docs-site-checks.yml
 M hermes-agent/.github/workflows/nix-lockfile-fix.yml
 M hermes-agent/.github/workflows/skills-index.yml
 M hermes-agent/.github/workflows/supply-chain-audit.yml
 M hermes-agent/.github/workflows/tests.yml
 M hermes-agent/.gitignore
 M hermes-agent/AGENTS.md
 M hermes-agent/Dockerfile
 M hermes-agent/MANIFEST.in
 M hermes-agent/README.md

$ git remote -v
origin	https://github.com/tuananh4865/hermes-backup.git (fetch)
origin	https://github.com/tuananh4865/hermes-backup.git (push)
upstream	https://github.com/NousResearch/hermes-agent.git (fetch)
upstream	https://github.com/NousResearch/hermes-agent.git (push)

$ git branch --show-current
main
```

Notable: `.update_check` shows as **deleted** (` D`) — file was removed between
sessions. This is normal for a rolling-state repo.

## Stage + commit + push
```
$ git add . && git commit -m "Backup hermes full: 2026-06-15"
delete mode 100644 skills/.curator_backups/2026-05-10T02-07-37Z/manifest.json
create mode 100644 skills/.curator_backups/2026-06-14T05-27-06Z/cron-jobs.json
create mode 100644 skills/.curator_backups/2026-06-14T05-27-06Z/manifest.json
create mode 100644 skills/devops/hermes-daily-backup/SKILL.md
create mode 100644 skills/devops/hermes-daily-backup/references/report-example.md
create mode 100644 skills/github/github-operations/templates/bug-report.md
create mode 100644 skills/github/github-operations/templates/feature-request.md
create mode 100644 skills/mcp/mcp-integration/SKILL.md
rename skills/mcp/{mcporter => mcp-integration}/references/exa-mcp-advanced-tools.md (100%)
create mode 100644 skills/software-development/simplify-code/SKILL.md
delete mode 100644 state-snapshots/20260606-171845-pre-update/gateway_state.json
rename state-snapshots/{20260606-171845-pre-update => 20260614-151134-pre-update}/.env (100%)
rename state-snapshots/{20260606-171845-pre-update => 20260614-151134-pre-update}/channel_directory.json (97%)
rename state-snapshots/{20260606-171845-pre-update => 20260614-151134-pre-update}/config.yaml (93%)
rename state-snapshots/{20260606-171845-pre-update => 20260614-151134-pre-update}/cron/jobs.json (76%)
create mode 100644 state-snapshots/20260614-151134-pre-update/gateway_state.json
rename state-snapshots/{20260606-171845-pre-update => 20260614-151134-pre-update}/manifest.json (55%)
rename state-snapshots/{20260606-171845-pre-update => 20260614-151134-pre-update}/platforms/pairing/_rate_limits.json (100%)
rename state-snapshots/{20260606-171845-pre-update => 20260614-151134-pre-update}/platforms/pairing/discord-pending.json (100%)
rename state-snapshots/{20260606-171845-pre-update => 20260614-151134-pre-update}/processes.json (100%)

$ git diff --shortstat HEAD~1 HEAD
1530 files changed, 162371 insertions(+), 29718 deletions(-)

$ git push origin main
To https://github.com/tuananh4865/hermes-backup.git
   19e75f53d..d872c369f  main -> main
```

## Report delivered
```
✅ Hermes Daily Backup — 2026-06-15
Trạng thái: Thành công
Commit: d872c369f
Push: 19e75f53d..d872c369f main -> main (github.com/tuananh4865/hermes-backup)
Thống kê: 1530 files changed, 162371 insertions(+), 29718 deletions(-)
Nội dung nổi bật:
- Skills mới: devops/hermes-daily-backup, mcp/mcp-integration, software-development/simplify-code
- Skill rename: skills/mcp/mcporter → mcp-integration
- State snapshots: rotate 20260606-171845 → 20260614-151134 (mature cleanup)
- Curator backups: thêm snapshot 2026-06-14T05-27-06Z, xóa snapshot cũ 2026-05-10
- Cron jobs: cập nhật jobs.json, tiktok-monitor/seen-videos.json, 4 lessons (cta/hooks/storytelling/tiktok-shop)
- Hermes-agent repo: cập nhật workflows, AGENTS.md, Dockerfile, README, .gitignore
- File xóa: .update_check (rolling state)
Lỗi: Không có.
```

## Notes for next run
- Lượng insertions/deletions LỚN (162K/29K) là bình thường khi có state-snapshot
  rotation hoặc curator backup rotation. Không phải dấu hiệu corruption.
- Skill `mcp/mcp-integration` (rename từ `mcporter`) là thay đổi cấu trúc —
  scripts nào reference path cũ sẽ cần update.
- File `hermes-daily-backup/SKILL.md` mới xuất hiện trong chính output backup
  của nó — không phải lỗi, đây là kết quả của session trước tạo skill này.
  Self-referential, harmless.
- Backup identity là NGÀY (`2026-06-15`) — nếu cron chạy 2 lần/ngày, commit
  message trùng nhau nhưng SHA khác. Không cần thêm timestamp.
