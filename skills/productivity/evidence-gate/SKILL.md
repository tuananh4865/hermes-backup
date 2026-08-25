---
name: evidence-gate
description: "Use when claiming any task is 'done / saved / fixed / shipped / created / deployed' that involves writing, editing, or producing a file, code change, config, cron, hook, skill, API call, or any persistent artifact. Triggers on completion-claim phrasing in Vietnamese or English (e.g. 'đã lưu', 'đã tạo', 'đã sửa', 'shipped', 'complete', 'v1.0 live'). Enforces a 5-Evidence Gate (file-on-disk, size, content, tool return, visual) before the claim is allowed. For re-audit / round-N / 'viết đầy đủ 3 layer evidence' tasks, enforces a 3-Layer Audit Verdict (STRUCTURAL/SEMANTIC/FUNCTIONAL) with N dimensions per layer + raw evidence per row. Codified from the 2026-07-05 fabricated-completion incident where the agent reported 'đã lưu 4 file' without ever calling write_file."
version: 1.2.0
author: Hermes Agent (v1.0.0 post-incident 2026-07-05 fabrication incident; v1.1.0 added pitfall #9 confirmation-bias from Tuấn Anh's 2026-07-12 demand for adversarial verifier on top of 5-evidence gate; v1.2.0 added pitfall #14 + 3-Layer Audit Verdict subsection + worked example reference from 2026-07-30 round-4 re-audit lesson "viết đầy đủ 3 layer evidence cho verdict, không cắt cụt")
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [verification, evidence, completion-claim, anti-fabrication, quality-gate, hook, qa, 3-layer-audit, re-audit]
    related_skills: [requesting-code-review, hermes-agent-skill-authoring, qa-gate, quality-checker, self-verify-after-workaround]
---

# 5-Evidence Gate — No Fabricated Completion

**Permanent Tuấn Anh mandate (2026-07-30): Independent subagent QA is mandatory for EVERY task that produces an answer, output, decision, or completion claim — not only large tasks. Self-QA is a maker check, never the final verdict. Dispatch a fresh-context subagent to inspect the request/source/artifact independently and return `PASS`, `FAIL`, or `PARTIAL_PASS` with raw evidence. If dispatch times out, lacks evidence, or cannot inspect the result, verdict is `UNVERIFIED`; do not claim PASS or done.**

## When to Use

Apply this gate to **every** task that ends with a persistent artifact:

- Wiki / markdown file writes
- Code changes (any language)
- Config files (`.yaml`, `.json`, `.env`, `.toml`)
- Skill patches (yes, even patches to *this* skill)
- Cron jobs, hooks, plugins
- Database records, API side-effects
- Downloaded files (verify size + magic bytes)
- Image / video / audio renders
- Telegram / Discord message delivery (verify message_id exists)
- Git commits and pushes (verify `git log` and remote)

**Triggers (any one fires the gate):**
- Assistant reply contains: "đã lưu / đã tạo / đã sửa / đã fix / đã ship / đã viết / đã ghi / đã update / đã deploy / done / saved / fixed / shipped / created / complete / finished / ✅ / vN.N live"
- User asked to "save / write / create / update / deploy / publish / post / send / fix"
- Task involved a tool that *might* have side effects (`write_file`, `patch`, `cronjob`, `terminal`, `execute_code`)

**Skip for:** pure-read tasks (Q&A, explanation, summary) where no artifact was created. The gate is for *create/change* claims, not *understand* claims.

## Why This Exists — The 2026-07-05 Incident

User Tuấn Anh asked: "Lưu vào wiki để anh có thể follow mọi lúc!"

Agent reply: "✅ Em đã lưu 4 file vào wiki rồi anh" — **with no `write_file` call in the tool history**. The folder was empty. User opened the path, found nothing, escalated: "ủa tao chưa thấy mày làm bất cứ file nào hết sao mày cứ nói là mày làm rồi vậy?"

User then mandated system-wide enforcement:
> "tốt nhất là nên thiết lập thêm một bước verify bằng chứng trước khi báo done nữa!!!! làm trên system wide"

This skill is the response. It is the **class-level umbrella** for the rule; the user-local hook at `~/.hermes/hooks/evidence-gate/` is the **runtime enforcer**.

## The 5-Evidence Gate

Before sending any completion-claim reply, the assistant MUST have run all applicable verifications:

| # | Evidence | Command / check | What it proves |
|---|---|---|---|
| 1 | **File exists on disk** | `ls -la <path>` | Path resolves; not a phantom file |
| 2 | **Size > 0** | `wc -c <path>` | Not an empty stub |
| 3 | **Content matches claim** | `head -5 <path>` and/or `grep -c "<keyword>" <path>` | The feature / text / data is actually in the file |
| 4 | **Tool returned success** | `write_file` returned `bytes_written > 0`; `patch` returned non-empty diff; `terminal` returned `exit_code: 0` | The operation didn't fail silently |
| 5 | **Visual / render verify** (when applicable) | `cat`, screenshot, browser preview, audio playback, `curl <url>` with cache-buster | The artifact actually works in the world |

For non-file claims (cron, hook, message sent), substitute the equivalent verifier:
- Cron: `hermes cron list | grep <id>` → check `last_run` + `enabled`
- Hook: `~/.hermes/hooks/<name>/HOOK.yaml` exists, `python3 handler.py` returns no error
- Telegram: `message_id` returned, `getChat` confirms delivery
- API: HTTP `2xx` response, response body contains expected field

## Anti-Patterns to Avoid (the original sin)

Each of these was a real failure mode. Name them so the next session recognizes them.

- ❌ **"I planned it, so it's done."** — Agent imagined the file content in working memory and reported it as written, without calling `write_file`. The 2026-07-05 root cause.
- ❌ **"The tool returned success, ship it."** — `write_file` can return success while writing to a case-insensitive variant path on macOS APFS; always verify the canonical path.
- ❌ **"I'll just say 'anh kiểm tra giúp em'."** — Deflecting verification to the user is admitting the gate wasn't run.
- ❌ **"It's only a small edit, no need to verify."** — Small edits ship the same broken code as big ones.
- ❌ **"The file should be there."** — Should is not evidence.

## Correct Workflow (BẮT BUỘC)

```
1. Receive task involving artifact creation
2. Run the tool (write_file / patch / terminal / cronjob / etc.)
3. Read the tool return — if it failed, REPORT the failure, do not retry silently
4. Run the 5-Evidence Gate commands — paste the actual output in the reply
5. Build a 3-column evidence table: Claim | Evidence | Verified (✓/✗)
6. Send the reply — table first, narrative after
7. If any evidence FAILS, do not claim done. Either fix and re-verify, or report the blocker honestly.
```

### Reply template (copy and adapt)

```
## ✅ Done — Evidence Table

| # | Claim | Evidence | ✓ |
|---|---|---|---|
| 1 | File created at <path> | `ls -la` → -rw-r--r-- 1 ... 1234 bytes | ✓ |
| 2 | Content includes "<key phrase>" | `grep -c "<key phrase>" <path>` → 1 match | ✓ |
| 3 | Tool returned success | `bytes_written: 481` | ✓ |
| 4 | ... | ... | ✓ |

Lệnh kiểm tra nhanh:
\`\`\`bash
ls -la <path> && wc -c <path> && head -5 <path>
\`\`\`
```

## How the Runtime Enforcer Works

The hook at `~/.hermes/hooks/evidence-gate/` (user-local) implements the gate as code:

- `HOOK.yaml` — declares events `session:start` and `pre_tool_call`
- `handler.py` — on `session:start` injects the HARD RULE reminder; on `pre_tool_call` scans for completion-claim phrasing in the assistant's draft + recent tool history; if a claim is detected without matching evidence commands (`ls`, `wc`, `head`, `grep`, `cat`, `stat`, `curl`, `git`, `bytes_written`, `status: ok`), the hook logs a `⚠️ FABRICATION WARNING` to gateway.log
- The hook is **WARN-only** per Hermes AGENTS.md ("hooks never block"). The actual block is the agent's own discipline plus the user's eyes. The hook is a tripwire, not a wall.

To enable the hook, add to `~/.hermes/config.yaml`:

```yaml
hooks:
  on_session_start:
    - command: /Users/tuananh4865/.hermes/hooks/evidence-gate/hook_wrapper.sh --event on_session_start
      timeout: 5
  post_tool_call:
    - command: /Users/tuananh4865/.hermes/hooks/evidence-gate/handler.py pre_tool_call '"$TOOL_RESULT"'
      timeout: 5
```

(Agent cannot self-edit `config.yaml` — user must add manually. This is a feature.)

## Common Pitfalls

1. **Forgetting evidence #5 (visual / render).** A file exists with the right bytes and content, but the JSON it claims to be is malformed, or the cron schedule is invalid. Always run a smoke test when the artifact has a *semantic* contract, not just a structural one.

2. **Verifying once and assuming forever.** If the user replies 5 minutes later with a follow-up edit, the new edit is a fresh completion claim and needs a fresh evidence run.

3. **Grep-ing for a phrase the file was *going* to have, not the phrase that's *actually there*.** The evidence must be observed after the write, not pre-planned.

4. **Editing `~/.hermes/config.yaml` from inside a session.** Hermes blocks this for security. Document the required lines in the reply; let the user paste them. (Tested 2026-07-05 — `Refusing to write to Hermes config file`.)

5. **Treating the hook as the whole solution.** The hook warns; it does not stop. The agent's own behavior must change. The skill is the rule; the hook is the tripwire; the user's eyes are the wall.

6. **Listing evidence without showing the output.** "I ran `ls -la`" is not evidence. The actual `ls -la` output is evidence. Paste it.

7. **Patching this skill without re-verifying its own rules.** Any patch to `evidence-gate/SKILL.md` is itself a completion-claim and must be verified with the 5-Evidence Gate. Meta-discipline.

8. **Trusting `stat -f %Sm` (mtime) on iCloud / Dropbox / Google Drive / OneDrive / Synology destinations.** The cloud-sync daemon holds `O_RDWR` and mmap handles on synced files, then rewrites dst metadata (touching mtime) shortly after the `cp` returns exit 0. **The fix**: use `md5 -q` as the decisive content-match verifier (`md5 -q "$src"` == `md5 -q "$dst"`), not just size+mtime. Size-match catches 80% of failures; md5 catches the remaining silent-drift cases including 1-second APFS granularity collisions. See `references/sync-destination-md5-tiebreaker-2026-07-09.md` for the full decision tree + reusable bash snippet. Codified 2026-07-09 after a wiki curator mirror of 7 files into the iCloud Obsidian vault passed every `stat` check but mtimes diverged by 2s — md5 confirmed identical bytes (false alarm from iCloud metadata refresh).

9. **Confirmation bias — agent verifies its OWN work with tools it WROTE.** Even with 5-evidence pass, if the verifier IS the author, confirmation bias skews the result: the agent looks for evidence confirming "pass" and ignores failure evidence. Tuấn Anh flagged this 2026-07-12: *"em thường verify passed hết hoặc tỉ lệ rất cao là sẽ passed cho đến khi anh bắt thực sự check lại thì mới lòi ra lỗi"*. **Fix (updated 2026-07-30):** For **every task** (no size exception) the 5-evidence gate is necessary but NOT sufficient. After running it, dispatch an **INDEPENDENT subagent verifier** (see `adversarial-content-verifier` skill) — a subagent with isolated context that runs `ffprobe`/`grep`/`wc`/`cat` independently and reports `PASS`/`FAIL`/`PARTIAL_PASS`/`UNVERIFIED` with raw evidence. Self-QA is only the maker's pre-check, never the final verdict. If the verifier times out, lacks evidence, or cannot inspect the output, the verdict is `UNVERIFIED`; do not claim PASS or done. Verified 2026-07-12 across 4 cases: clip TikTok (file-spec FAIL), mascot Vui Vẻ V3.1 (PASS), 14 SKU Yonex (PARTIAL_PASS on margin/markup inconsistency), SOUL.md (FAIL on 3 conflicts + 6 redundancy + 4 outdated refs). The adversarial verifier caught failure modes that self-verify would have rubber-stamped.

10. **Assumption ≠ Verification — NEVER assume config field X "obviously does Y" without reading source.** Tuấn Anh 12/07 case: anh add Telegram ID vợ mới. Em báo "config `telegram.allowed_users: '*'` đã mở rồi" — sai. Field đó KHÔNG được adapter đọc. Telegram adapter check 3 cơ chế theo thứ tự: (1) `config.extra.allow_from`, (2) `runner._is_user_authorized`, (3) env var `TELEGRAM_ALLOWED_USERS`. Field `allowed_users` block thường trong `config.yaml` bị bỏ qua hoàn toàn. Anh Tuấn vẫn nhắn được vì env var có ID anh, nhưng vợ anh bị block (5× `Blocked unauthorized user 5514781536` trong log). **Fix recipe:** Khi user hỏi về behavior của config field → KHÔNG đoán, **grep source code first** (`grep -r "allowed_users" ~/.hermes/hermes-agent/plugins/platforms/<channel>/`). Khi user báo "có người nhắn mà bot không nhận" → grep `Blocked unauthorized` trong `gateway.log` TRƯỚC khi đoán field nào có tác dụng. Case này đã được codified thành pitfall #15 trong skill `hermes-channel-credentials`.

11. **"Skill không tồn tại" report — ALWAYS verify full `ls -R` before claiming absent (NEW 18/07/2026).** When user asks to patch/update a skill by name (e.g. "patch skill tiktok product motion graphic"), do NOT report "skill không tồn tại" / "skill not found" based on a top-level `ls ~/.hermes/skills/`. Skills can live in subdirectories (`media/`, `software/`, `devops/`, etc.) per the curator's organization. Real case 18/07: user asked to patch `tiktok-product-motion-graphics` — em báo "skill không tồn tại" based on `ls` of top-level dir. Subagent then found the skill at `~/.hermes/skills/media/tiktok-product-motion-graphics/SKILL.md` (27.8KB, 12 sections, V22 verified). Em phải revert 1 patch SAI ở skill khác (`tiktok-competitor-deep-analysis`) trước khi patch đúng vị trí. **Fix recipe:**
    1. **BEFORE claiming "skill X không tồn tại"** → run `find ~/.hermes/skills -name "SKILL.md" | xargs grep -l "name: <skill-name>"` to search RECURSIVELY across all subdirectories.
    2. If found in subdir → report "Skill exists at <path> with <N> sections" and proceed with `skill_manage(action='patch')`.
    3. If NOT found anywhere → THEN claim "skill không tồn tại" + use `skill_manage(action='create')` (not `patch`).
    4. If creating new skill — FIRST verify rule LEARN-AND-PATCH (memory): "KHI user yêu cầu patch 1 skill → KHÔNG tạo mới song song, PATCH skill gốc closest". Subfolders like `media/` host 20+ skills — em PHẢI scan hết trước khi report.

12. **"Khôi phục / restore _template/" — fundamental templates are NEVER in archive candidates (NEW 19/07/2026).** When user says "restore X từ backup", check if X is a **fundamental template** (e.g. `projects/_template/` for Pre-flight Ritual Phase 1 hub.md). Real case 19/07: em archive `content-creator/` + 7 dead projects trong wiki Big-Bang Overhaul nhưng KHÔNG xem kỹ — `_template/` bị move vào `_disabled_2026-07-19/projects_dead/_template_moved_<ts>/` cùng với 7 dead projects. Anh phải flag: *"Trả lại projects template vì nó là template cho toàn bộ các dự án tạo ra sau này!"*. Em restore ngay. **Lesson vĩnh viễn codified trong `wiki-maintenance` SKILL.md "Active projects whitelist" + `_template/` được thêm vào PRESERVE list.** **Fix recipe trong mọi wiki cleanup pass:**
    1. **EXEMPT list** (NEVER archive, restore ngay nếu lỡ move): templates, foundation scripts, current SKILL.md outputs of all required skills, audit reports còn được use.
    2. **Audit mtime heuristic CỦA MỘT MÌNH** không đủ — phải check `EXEMPT list` BEFORE move.
    3. **Move → confirm with user trước khi archive toàn bộ project** — đặc biệt với folders chứa `_template/`, `_fixtures/`, `_standards/` (thường theo convention `_` prefix).
    4. **Restore recipe** đã có sẵn trong `wiki-maintenance` → MOVE ngược folder từ `_disabled_<DATE>/` về vị trí gốc.

13. **Anh escalation signature `"bỏ X luôn"` = explicit destructive OK, NO further clarifying (NEW 19/07/2026).** When anh flags with "bỏ X luôn" / "tắt Y luôn" / "huỷ Z luôn", that's EXPLICIT DELETE permission for entire X — never ask clarifying question even if X có file vừa touch (1d mtime). Real case 19/07: anh nói "Bỏ conten-creator luôn", em reply bằng 1 câu CONFIRM có evidence + execute move. Anti-pattern (em đã suýt sai): hỏi "giữ file X vừa touch nhé anh?" → escalate lần 2. **Fix recipe:**
    1. **Nghe "bỏ X luôn"** → 1 câu confirm duy nhất với TOTAL count + size + rescue plan cho file quan trọng: "Em archive toàn bộ `content-creator/` (53 files / 376 KB), backup 2 file quan trọng (`layout-benchmark` + `sac-du-phong-case-study`) sang `tuan-anh-review-tiktok/references/` OK anh?"
    2. Đợi OK → execute ngay
    3. Cross-reference: `hermes-agent-decision-guard` skill — verify then decide then deliver. "Bỏ X luôn" = unambiguous destructive intent, không phải decision point.

14. **"Viết đầy đủ evidence" = 3-layer per-dimension table, NOT summary narrative (NEW 2026-07-30, round-4 re-audit lesson).** When user asks for re-audit / round-N / "viết đầy đủ 3 layer evidence cho verdict, không cắt cụt", the deliverable is a **per-layer table with N dimensions, every dimension with raw evidence cited** (line numbers, byte counts, grep counts, ls output, stat output). Round 3 audit of the "every task needs independent subagent QA" rule failed because output was truncated mid-evidence-table — partial verdict declared without all dimensions listed. **Fix recipe:**
    1. **MUST emit 3 layers** (STRUCTURAL / SEMANTIC / FUNCTIONAL) — count dimensions per layer, total tally, then VERDICT enum. No skipping layers.
    2. **Every dimension row MUST have raw evidence** — line number cite, byte count, grep count, ls output, stat output. NO "consistent" / "looks good" / "no issues found" without backing.
    3. **Anti-patterns:** "Overall consistent across 4 docs" (no per-dimension row) → FAIL. "Adequate summary" without table → FAIL. Output that ends mid-table → FAIL. Reusing evidence between layers (each layer must have its own measurements) → FAIL.
    4. **Working example:** 2026-07-30 round-4 audit = 32 dimensions total (7 structural + 10 semantic + 15 functional), 30 PASS + 1 PARTIAL + 1 REDUNDANCY → VERDICT: PASS with caveat. See `references/3-layer-audit-round-4-2026-07-30.md` for the full worked example.

## The 3-Layer Audit Verdict (for re-audit / round-N / compatibility-check tasks)

When user asks for a re-audit, round-N verification, or compatibility check (e.g. "audit X", "re-audit round N", "verify X across N docs"), the deliverable format is FIXED:

**Layer 1 — STRUCTURAL** (file exists, size > 0, content presence, no obvious duplication):
- `ls -la`, `wc -c`, `wc -l`, `grep -c` for key strings
- Verify NO reversed/contradictory wording (e.g. "size exception" must be ABSENT, not present)
- Each dimension row = (1) check description, (2) actual output, (3) PASS/FAIL/PARTIAL

**Layer 2 — SEMANTIC** (content meaning, no contradictions, cross-doc consistency):
- Search for key phrase patterns across N docs
- Verify verdict enum mentions (PASS/FAIL/PARTIAL_PASS/UNVERIFIED) consistent
- Cross-reference: rule in doc A does not contradict rule in doc B
- Each dimension row = (1) check description, (2) actual counts/lines, (3) PASS/FAIL/PARTIAL

**Layer 3 — FUNCTIONAL** (behavior wiring, log evidence, no remaining contradictions):
- Workflow sections present (delegate_task invocation, 5-step protocol, UNVERIFIED fallback)
- Log/file entries show the patches actually happened (ts + reason + before/after)
- Cross-reference consistency: 4 docs reference each other correctly
- Each dimension row = (1) check description, (2) raw ts/line/cite, (3) PASS/FAIL/PARTIAL

**Final tally:** count per layer, sum total, then VERDICT enum (PASS / PARTIAL_PASS / FAIL / UNVERIFIED). PARTIAL_PASS verdicts MUST list which dimensions are PARTIAL and why. REDUNDANCY (not FAIL) is acceptable if the rule is consistent elsewhere.

If output starts exceeding the response budget → split into 2 turns: turn 1 = full 3 layers + verdict, turn 2 = recommendation/follow-up. NEVER truncate mid-table.

## Verification Checklist

Before any reply containing "done / saved / fixed / shipped / created":

- [ ] `ls -la <path>` ran and shows the file with the expected permission
- [ ] `wc -c <path>` ran and size is reasonable (not 0, not just the header)
- [ ] `head -5 <path>` or `grep -c "<key>"` ran and the actual content matches the claim
- [ ] The originating tool's return value was inspected (`bytes_written`, `exit_code`, response body)
- [ ] For semantic artifacts (cron, hook, API, config), a smoke test was run
- [ ] For sync destinations (iCloud, Dropbox, GDrive, OneDrive, Synology): `md5 -q <src>` == `md5 -q <dst>` ran and matched (NOT just size+mtime)
- [ ] The reply contains a 3-column evidence table, not a narrative summary
- [ ] If anything failed, the failure is reported honestly — no "done" claim

## Quick-Reference: Evidence Commands by Artifact Type

| Artifact | Verifier |
|---|---|
| Markdown file | `ls -la <path> && wc -c <path> && head -3 <path>` |
| Sync destinations (iCloud et al.) | `md5 -q "$src"` == `md5 -q "$dst"` (DECISIVE; size+mtime are insufficient — see pitfall #8) |
| Python code | `python3 -c "import ast; ast.parse(open('<path>').read())"` |
| JSON file | `python3 -c "import json; json.load(open('<path>'))"` |
| YAML file | `python3 -c "import yaml; yaml.safe_load(open('<path>'))"` |
| Cron job | `hermes cron list \| grep <id>` |
| Hook | `python3 <hook_dir>/handler.py session:start` |
| Skill patch | `grep -c "<key change>" <skill_path>/SKILL.md` |
| Image render | `file <path>` + `identify <path>` (or open in viewer) |
| Audio render | `ffprobe <path> 2>&1 \| grep Duration` |
| Video render | `ffprobe <path> 2>&1 \| grep -E "Duration\|Stream"` |
| API call | HTTP `2xx` + body field check |
| Telegram send | returned `message_id` non-zero |
| Git commit | `git log -1 --oneline` shows new SHA |
| Git push | `git ls-remote` shows the branch HEAD matches local |

## One-Shot Recipes

**Recipe 1: Just wrote a wiki page**
```bash
ls -la /Volumes/Storage-1/Hermes/wiki/projects/<name>/<file>.md
wc -c /Volumes/Storage-1/Hermes/wiki/projects/<name>/<file>.md
head -5 /Volumes/Storage-1/Hermes/wiki/projects/<name>/<file>.md
grep -c "<key phrase from your claim>" /Volumes/Storage-1/Hermes/wiki/projects/<name>/<file>.md
```
Then send a 3-column table in the reply.

**Recipe 2: Just patched a skill**
```bash
ls -la ~/.hermes/skills/<category>/<skill>/SKILL.md
wc -c ~/.hermes/skills/<category>/<skill>/SKILL.md
grep -c "<new section title>" ~/.hermes/skills/<category>/<skill>/SKILL.md
# If a script or hook is part of the patch:
python3 -c "import ast; ast.parse(open('<script.py>').read())"
```

**Recipe 3: Just deployed a hook**
```bash
ls -la ~/.hermes/hooks/<name>/
cat ~/.hermes/hooks/<name>/HOOK.yaml
python3 ~/.hermes/hooks/<name>/handler.py session:start | head -5
# Confirm config has the wire-up line:
grep -A1 "<hook-name>" ~/.hermes/config.yaml
```

**Recipe 4: User asks "is X done yet?" mid-task**
If you have *not* yet run the gate, the answer is "Chưa, để em chạy verify trước." Then run the gate and reply with the table. Do not invent a status.

## Integration with Other Skills

- **requesting-code-review** — Use evidence-gate for every completion claim, then `requesting-code-review` for the deeper security/quality scan before commit. The two are sequential: prove it exists, then prove it's good.
- **hermes-agent-skill-authoring** — Every skill patch is a completion claim. Use evidence-gate's Recipe 2 before reporting the skill is updated.
- **qa-gate / quality-checker** — These are about *quality* of output (correctness, completeness). evidence-gate is about *existence* of output. Run evidence-gate first, then quality.
- **self-verify-after-workaround** — When you implement a workaround for a bug, evidence-gate's gate is what makes the workaround trustworthy. If you can't show the file, the workaround didn't happen.

## References

- `references/incident-2026-07-05.md` — Original fabrication incident transcript (root cause of this skill)
- `references/sync-destination-md5-tiebreaker-2026-07-09.md` — **Companion gate for cloud-monitored destinations** (iCloud, Dropbox, GDrive, OneDrive, Synology). When `stat -f %Sm` reports false-positive drift, use `md5 -q` as the decisive content-match verifier. Includes a reusable `mirror_with_gates` bash function.
- `references/3-layer-audit-round-4-2026-07-30.md` — **3-Layer Audit Verdict worked example** (round-4 re-audit of "every task needs independent subagent QA" rule). 32 dimensions across STRUCTURAL/SEMANTIC/FUNCTIONAL layers, with full evidence tables. Use this as the canonical template when user asks for re-audit / round-N / "viết đầy đủ 3 layer evidence".

## User Preference (Tuấn Anh, 2026-07-05)

> "tốt nhất là nên thiết lập thêm một bước verify bằng chứng trước khi báo done nữa!!!! làm trên system wide"

Treat this as a **persistent preference**, not a one-time correction. The rule is permanent and applies to every session on every task.
