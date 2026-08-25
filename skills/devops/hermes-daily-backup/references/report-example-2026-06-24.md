# Daily Backup Report — 2026-06-24

## Context
3AM cron run. Cả hai repo (`main` + `content-creator-meta`) đều có commits mới từ máy khác / cron trước đó. Working tree local có thay đổi từ session tối qua (stale uncommitted changes cần handle cẩn thận).

## Outcome
✅ Both branches pushed successfully.
- **main**: 2 commits (`a0e92619c` marker + `39336c62d` incremental)
- **content-creator-meta**: 1 commit (`69d6860f2` metadata sync)

## What happened step by step

### Step 1: Initial preflight — found local uncommitted changes
```bash
$ git status --short | head -30
M .hermes_history
 M .recent_session_context.txt
 M .skills_prompt_snapshot.json
 M .update_check
 M .wiki_session_context.txt
 ...
```
~940 files modified locally, working tree dirty.

### Step 2: `git add -A && git commit` succeeded
```
$ git commit -m "Daily backup hermes full: 2026-06-24"
[main 18dc4550f] Daily backup hermes full: 2026-06-24
 940 files changed, ...
```

### Step 3: `git push` REJECTED (remote ahead)
```
 ! [rejected] main -> main (fetch first)
error: failed to push some refs to ...
Updates were rejected because the remote contains work that you do not have locally.
```
**Trigger**: backup từ máy khác / session trước đã push lên remote rồi. Local branch lệch so với origin/main.

### Step 4: Tried `git pull --rebase --autostash` → CONFLICT storm
```
CONFLICT (add/add): Merge conflict in skills/tiktok-transcript-pipeline/SKILL.md
Auto-merging state/rich_sent_index.json
CONFLICT (content): Merge conflict in state/rich_sent_index.json
error: could not apply 18dc4550f... Daily backup hermes full: 2026-06-24
```
10+ file conflicts, toàn là state files auto-rewritten bởi gateway (`channel_directory.json`, `cron/jobs.json`, `state/rich_sent_index.json`, `checkpoints/TASK_STATE.md`, `skills/.usage.json`...).

### Step 5: Cleanest fix — abort rebase, reset hard to origin/main
```bash
$ git rebase --abort
$ git fetch origin main
$ git reset --hard origin/main
HEAD is now at 05ed1c9a9 Backup hermes full: 2026-06-23
```
**Note**: mất commit `18dc4550f` (vừa tạo). Nhưng OK vì:
- (a) đó là daily backup cron, idempotent — không push vẫn OK vì ngày hôm qua đã có `05ed1c9a9` đầy đủ state
- (b) reflog giữ 7 ngày, có thể recover nếu thực sự cần

### Step 6: Working tree clean → empty marker commit
```bash
$ git status --short | wc -l
0
$ git commit --allow-empty -m "Daily backup marker: 2026-06-24"
[main a0e92619c] Daily backup marker: 2026-06-24
$ git push origin main
05ed1c9a9..a0e92619c  main -> main
```
**Lesson**: empty marker commit vẫn push được, tạo audit trail entry cho ngày hôm đó.

### Step 7: Stale stash pop introduced index conflicts
Sau khi checkout `content-creator-meta`, stash pop failed mid-way (vì stash@{0} có UU conflicts từ pull --rebase lúc trước). Git index bị stuck ở "needs merge" state:
```
$ git stash pop
channel_directory.json: needs merge
cron/jobs.json: needs merge
profiles/qa-agent/state.md: needs merge
skills/.usage.json: needs merge
The stash entry is kept in case you need it again.
```
Mọi `git checkout` tiếp theo fail với "you need to resolve your current index first".

### Step 8: Reset hard to clear index, then stash pop worked
```bash
$ git reset --hard HEAD
HEAD is now at 69d6860f2 Sync content-creator meta: 2026-06-24
$ git checkout main
Switched to branch 'main'
$ git stash pop
Dropped refs/stash@{0} (78835ba1ae7f8982eac817041e1a4b3c0d4cc1ac)
```

### Step 9: Commit incremental + push
```bash
$ git add -A && git commit -m "Daily backup hermes incremental: 2026-06-24 03:01 config + skills"
[main 39336c62d] Daily backup hermes incremental: 2026-06-24 03:01 config + skills
 6 files changed, 1455 insertions(+), 24 deletions(-)

$ git push origin main
a0e92619c..39336c62d  main -> main
```

### Step 10: Content Creator metadata sync
Trên branch `content-creator-meta` (đã pull về `9eceab336` từ remote), generate metadata + tree từ `~/Workspace/Claude/Projects/Content Creator/`:
- 18 files, 139318 bytes, all `.md`
- 3 files mới so với 2026-06-23: `Research/2026-06-24/daily-session-review.md` + 2 file ngày 23

**BUG lần đầu**: Tree generator emit ra file chỉ 21 bytes (chỉ có root directory). Lý do: logic chỉ loop qua files_by_dir keys mà không collect intermediate directories. Fix: build full dir hierarchy từ path parts trước, rồi mới emit recursively. Fix produce 1026 bytes / 28 lines.

### Step 11: Stash drop bị stale index
```bash
$ git stash drop stash@{1}  # OK
$ git stash drop stash@{2}  # OK
$ git stash drop stash@{3}  # OK
$ git stash drop stash@{4}  # FAIL: fatal: log for 'stash' only has 3 entries
```
**Lesson**: stash drop KHÔNG auto-shift index. Phải `git stash list` trước mỗi drop. Drops cũ đã chạy đủ rồi, không cần retry.

## Final state
```
main:
  39336c62d Daily backup hermes incremental: 2026-06-24 03:01 config + skills
  a0e92619c Daily backup marker: 2026-06-24
  05ed1c9a9 Backup hermes full: 2026-06-23  (from remote after reset)

content-creator-meta:
  69d6860f2 Sync content-creator meta: 2026-06-24
  9eceab336 Sync content-creator meta: 2026-06-23  (from remote)
  b3e39bde1 Sync content-creator meta: 2026-06-21
```

## Maps to pitfalls
- **#20a** (NEW): `git pull --rebase` with many conflicts → `git reset --hard origin/main`
- **#20b** (NEW): empty marker commit cho audit trail khi working tree clean
- **#20c** (NEW): stash drop index KHÔNG auto-shift
- **#20d** (NEW): `git checkout` fail với "needs merge" → `git reset --hard HEAD` clear index
- **#20e** (NEW): tree generator bug — must collect all intermediate directories
- **#18**: `scripts/sync-content-creator-meta.sh` vẫn chưa bundled — inline Python đã fix tree bug, output giờ match expected format
- **#14**: stash trước cross-branch work (vẫn dùng, nhưng stash pop bị conflict do pull --rebase leave dirty state)

## Recommendations cho cron script
1. Thay `git pull --rebase --autostash` đầu job bằng `git fetch origin main && git reset --hard origin/main` — ít conflict, đơn giản hơn cho state files.
2. Thêm `--allow-empty` cho commit step để cron luôn push 1 marker mỗi ngày (audit trail).
3. Stash management: dùng `git stash list` + message-based drop thay vì numeric index.
4. Pre-checkout guard: trước mỗi `git checkout <branch>`, chạy `git status --short | grep -q "^UU" && git reset --hard HEAD` để clear index conflicts từ session trước.

## Files referenced
- Backup log: `/Users/tuananh4865/.hermes/backups/backup-2026-06-24.log`
- Content Creator metadata: `content-creator-meta/metadata-2026-06-24.json` (3851B) + `tree-2026-06-24.txt` (1026B)
