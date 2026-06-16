---
title: Loop Engineering System — Changelog
created: 2026-06-16T19:15:01.542192+07:00
updated: 2026-06-16T19:15:01.542192+07:00
type: system-log
status: in-progress
scope: system-wide
---

# Loop Engineering System — Changelog

> Log mọi thay đổi cho Loop Engineering pattern (Addy Osmani) áp dụng system-wide.
> Mỗi entry: timestamp, file affected, before/after, QA gate, status.

---

## [INIT] 2026-06-16 19:15:01 +0700 — Khởi tạo log

**Context:** Anh Tuấn Anh yêu cầu áp dụng Loop Engineering system-wide trên Hermes Agent.
- Action 1: Checker sub-agent (universal quality gate)
- Action 2: /goal primitive (universal loop runner)
- Action 3: State file template (universal)
- Action 4: Hermes gateway hook (auto-invoke)
- Action 5: Wiki integration

**Quy tắc log:**
- Mỗi file edit → append entry mới
- Mỗi step done → `## [STEP-N] timestamp — tên action`
- Mỗi QA gate → `### [QA] timestamp — verdict`
- Format: append-only, KHÔNG bao giờ xóa entry cũ

---
### [FILE] 2026-06-16 19:20:58 +0700 — `/Volumes/Storage-1/Hermes/wiki/concepts/Loop-Engineering-System.md`

- **Action:** create
- **Note:** Wiki page cho Loop Engineering system-wide (mirror sang iCloud Obsidian vault)


---

### [FILE] 2026-06-16 19:20:58 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/CHANGELOG.md`

- **Action:** edit
- **Note:** Wiki page link + cross-reference đã thêm vào changelog


---

### [FILE] 2026-06-16 19:20:58 +0700 — `/Volumes/Storage-1/Hermes/wiki/index.md`

- **Action:** edit
- **Note:** Thêm [[Loop-Engineering-System]] vào Hermes Agent section


---

### [FILE] 2026-06-16 19:20:58 +0700 — `/Volumes/Storage-1/Hermes/wiki/log.md`

- **Action:** edit
- **Note:** Append entry ngày 2026-06-16 cho loop-engineering


---

## [STEP-1] 2026-06-16 19:31:24 +0700 — Tạo Checker skill (quality-checker)

**Status:** in_progress
**Files affected:** `/Users/tuananh4865/.hermes/skills/quality-checker/SKILL.md`, `/Users/tuananh4865/.hermes/skills/quality-checker/references/check-criteria.md`, `/Users/tuananh4865/.hermes/skills/quality-checker/templates/verdict-format.yaml`

Universal quality gate — verify mọi output từ maker agent trước khi deliver cho user. Apply cho system-wide Hermes workflow.

---

### [FILE] 2026-06-16 19:32:10 +0700 — `/Users/tuananh4865/.hermes/skills/quality-checker/SKILL.md`

- **Action:** create
- **Note:** Main skill spec — 6 universal check categories, verdict format, integration với loop engineering


---

### [QA] 2026-06-16 19:34:02 +0700 (STEP-1) — **FAIL**

**Note:** Quality checker test suite — unexpected verdicts: 1=WARN 2=WARN 3=FAIL

---

### [QA] 2026-06-16 19:34:15 +0700 (STEP-1) — **PASS**

**Note:** Quality checker test suite — 3/3 cases verdicts match expectations

---

### [FILE] 2026-06-16 19:34:25 +0700 — `/Users/tuananh4865/.hermes/skills/quality-checker/references/check-criteria.md`

- **Action:** create
- **Note:** Chi tiết 6 check categories với checklists, banned patterns, scoring


---

### [FILE] 2026-06-16 19:34:25 +0700 — `/Users/tuananh4865/.hermes/skills/quality-checker/templates/verdict-format.yaml`

- **Action:** create
- **Note:** YAML schema cho output verdict (PASS/FAIL/WARN + scores + issues + suggestions)


---

### [FILE] 2026-06-16 19:34:25 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/checker-config.yaml`

- **Action:** create
- **Note:** Centralized config cho quality-checker: thresholds, project rules, banned patterns


---

### [FILE] 2026-06-16 19:34:25 +0700 — `/Users/tuananh4865/.hermes/skills/quality-checker/test.py`

- **Action:** create
- **Note:** Test suite với 3 test cases (good/bad voice/no sources) — all pass


---

### [FILE] 2026-06-16 19:34:25 +0700 — `/Users/tuananh4865/.hermes/skills/quality-checker/test.py`

- **Action:** edit
- **Note:** Fix verdict logic: critical issue = FAIL bất kể score


---

## [STEP-1] 2026-06-16 19:34:25 +0700 — Tạo Checker skill (quality-checker) - DONE

**Status:** done
**Files affected:** `/Users/tuananh4865/.hermes/skills/quality-checker/SKILL.md`, `/Users/tuananh4865/.hermes/skills/quality-checker/references/check-criteria.md`, `/Users/tuananh4865/.hermes/skills/quality-checker/templates/verdict-format.yaml`, `/Users/tuananh4865/.hermes/loop-engineering/checker-config.yaml`, `/Users/tuananh4865/.hermes/skills/quality-checker/test.py`

Skill hoàn chỉnh: 6 check categories, verdict YAML schema, config file, test suite (3/3 pass).

---

## [STEP-2] 2026-06-16 19:35:40 +0700 — Implement /goal primitive (loop-goal)

**Status:** in_progress
**Files affected:** `/Users/tuananh4865/.hermes/skills/loop-goal/SKILL.md`, `/Users/tuananh4865/.hermes/skills/loop-goal/run.sh`, `/Users/tuananh4865/.hermes/skills/loop-goal/condition-parser.py`, `/Users/tuananh4865/.hermes/skills/loop-goal/test.sh`

Universal loop runner — chạy task lặp lại tới khi đạt verified condition. Pattern từ Addy Osmani /goal primitive.

---

### [FILE] 2026-06-16 19:38:14 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/SKILL.md`

- **Action:** create
- **Note:** Skill spec — API, examples, state tracking, configuration


---

### [FILE] 2026-06-16 19:38:14 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/condition-parser.py`

- **Action:** create
- **Note:** Python AST-based safe condition evaluator (whitelist operators, no eval)


---

### [FILE] 2026-06-16 19:38:14 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/condition-parser.py`

- **Action:** edit
- **Note:** Fix safety test: dangerous code returning False is also 'safe' (nothing executed)


---

### [FILE] 2026-06-16 19:38:14 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/condition-parser.py`

- **Action:** edit
- **Note:** Add CLI mode (--check + --condition) for shell integration


---

### [FILE] 2026-06-16 19:38:14 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/run.sh`

- **Action:** create
- **Note:** Main loop runner — bash script, runs maker → checker → condition check → re-run or deliver


---

### [FILE] 2026-06-16 19:38:14 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/run.sh`

- **Action:** edit
- **Note:** chmod +x for executable


---

### [FILE] 2026-06-16 19:38:14 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/test.sh`

- **Action:** create
- **Note:** Test suite 6 cases: parser unit, CLI, loop success/fail, state persistence


---

### [QA] 2026-06-16 19:38:14 +0700 (STEP-2) — **PASS**

**Note:** /goal loop test suite — 6/6 pass (parser + CLI + loop + state)

---

## [STEP-2] 2026-06-16 19:38:14 +0700 — Implement /goal primitive (loop-goal) - DONE

**Status:** done
**Files affected:** `/Users/tuananh4865/.hermes/skills/loop-goal/SKILL.md`, `/Users/tuananh4865/.hermes/skills/loop-goal/run.sh`, `/Users/tuananh4865/.hermes/skills/loop-goal/condition-parser.py`, `/Users/tuananh4865/.hermes/skills/loop-goal/test.sh`

Universal loop runner hoàn chỉnh: bash script + safe condition parser (AST-based, no eval risk) + 6/6 tests pass. Loop chạy tới khi đạt verified condition, ví dụ: 'Viết script viral' lặp 3 lần đến score=9.3 mới pass.

---

## [STEP-3] 2026-06-16 19:48:32 +0700 — AUDIT: Hermes profiles đã có sẵn - chuyển từ 'worker' → 'profile'

**Status:** in_progress
**Files affected:** `/Users/tuananh4865/.hermes/profiles/content-director/SOUL.md`, `/Users/tuananh4865/.hermes/profiles/research-lead/SOUL.md`, `/Users/tuananh4865/.hermes/profiles/coder/SOUL.md`

Audit phát hiện: Hermes đã có 3 profiles (content-director, research-lead, coder). Folder ~/.hermes/workers/ là sai terminology — em đã design nhưng chưa tạo file nào ở đó. Bây giờ chuyển sang ~/.hermes/profiles/{name}/ theo Hermes chuẩn. 3 skills (quality-checker, loop-goal) là GLOBAL — đặt ở ~/.hermes/skills/ (default profile's home) — mọi profile dùng được.

---

### [FILE] 2026-06-16 19:48:47 +0700 — `/Users/tuananh4865/.hermes/skills/quality-checker/SKILL.md`

- **Action:** edit
- **Note:** Worker → Profile terminology. Thêm Profile-Aware section. Global skill, mọi Hermes profile dùng được.


---

### [FILE] 2026-06-16 19:48:54 +0700 — `/Users/tuananh4865/.hermes/skills/quality-checker/test.py`

- **Action:** edit
- **Note:** worker_name → profile_name (test scripts)


---

### [QA] 2026-06-16 19:48:54 +0700 (STEP-1) — **PASS**

**Note:** Quality checker test suite — 3/3 cases verdicts match expectations

---

### [FILE] 2026-06-16 19:49:08 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/SKILL.md`

- **Action:** edit
- **Note:** Worker → Profile terminology. Profile-aware behavior. Path: ~/.hermes/profiles/


---

### [FILE] 2026-06-16 19:49:08 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/run.sh`

- **Action:** edit
- **Note:** WORKER → PROFILE variable. Path: profiles/ instead of workers/


---

### [FILE] 2026-06-16 19:49:08 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/test.sh`

- **Action:** edit
- **Note:** worker → profile terminology


---

### [FILE] 2026-06-16 19:49:16 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/test.sh`

- **Action:** edit
- **Note:** Fix test 6 path: workers → profiles


---

### [FILE] 2026-06-16 19:49:59 +0700 — `/Users/tuananh4865/.hermes/skills/loop-goal/run.sh`

- **Action:** edit
- **Note:** Fix arg parsing: --worker → --profile. Worker: → Profile: in output.


---

### [QA] 2026-06-16 19:50:08 +0700 (STEP-4) — **PASS**

**Note:** Loop-goal test suite (profile-aware) — 6/6 pass sau khi fix --worker → --profile

---

## [STEP-3] 2026-06-16 19:50:08 +0700 — Tạo profile state template + helper script

**Status:** in_progress
**Files affected:** `/Users/tuananh4865/.hermes/profiles/_template/state.md`, `/Users/tuananh4865/.hermes/loop-engineering/profile_state.py`, `/Users/tuananh4865/.hermes/loop-engineering/profile_state_test.py`

Profile-aware state file template (HERMES_HOME-aware). Helper script + tests.

---

### [FILE] 2026-06-16 19:50:33 +0700 — `/Users/tuananh4865/.hermes/profiles/_template/state.md`

- **Action:** create
- **Note:** Universal state file template cho mọi Hermes profile. HERMES_HOME-aware.


---

### [FILE] 2026-06-16 19:51:05 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/profile_state.py`

- **Action:** create
- **Note:** HERMES_HOME-aware profile state helper (CLI + Python API). Append verdict/run rows, ensure state, list profiles.


---

### [FILE] 2026-06-16 19:51:32 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/profile_state_test.py`

- **Action:** create
- **Note:** 7 test cases cho profile_state.py — HERMES_HOME-aware, ensure/append/list/state_path all work


---

### [QA] 2026-06-16 19:51:32 +0700 (STEP-3) — **PASS**

**Note:** Profile state helper test suite — 7/7 pass

---

## [STEP-3] 2026-06-16 19:51:32 +0700 — Tạo profile state template + helper script - DONE

**Status:** done
**Files affected:** `/Users/tuananh4865/.hermes/profiles/_template/state.md`, `/Users/tuananh4865/.hermes/loop-engineering/profile_state.py`, `/Users/tuananh4865/.hermes/loop-engineering/profile_state_test.py`

Profile-aware state management. Template tại ~/.hermes/profiles/_template/state.md. Helper resolve HERMES_HOME tự động. 7/7 tests pass.

---

## [STEP-5] 2026-06-16 19:53:26 +0700 — Verify profiles thật + check global skills

**Status:** in_progress
**Files affected:** _(chưa tạo file)_

Audit: 3 profiles thật (content-director, research-lead, coder) + default. Global skills ở ~/.hermes/skills/ (default profile home) — accessible từ mọi profile. Loop Engineering skills (quality-checker, loop-goal) là global — OK.

---

### [FILE] 2026-06-16 19:53:38 +0700 — `~/.hermes/profiles/{content-director,research-lead,coder,default}/state.md`

- **Action:** create
- **Note:** Init state.md cho 3 profiles (content-director, research-lead, coder) + default. Copy từ template.


---

### [QA] 2026-06-16 19:53:50 +0700 (STEP-5) — **PASS**

**Note:** State.md init cho 3 profiles + default. append_verdict works.

---

### [FILE] 2026-06-16 19:54:19 +0700 — `~/.hermes/profiles/{content-director,research-lead,coder,default}/state.md`

- **Action:** create
- **Note:** Re-init state files từ concrete template (có tables + sections thật)


---

## [STEP-6] 2026-06-16 19:54:26 +0700 — Tạo Hermes gateway hook (HERMES_HOME-aware, applies cho mọi profile)

**Status:** in_progress
**Files affected:** `/Users/tuananh4865/.hermes/loop-engineering/hook.py`, `/Users/tuananh4865/.hermes/loop-engineering/hook_config.yaml`, `/Users/tuananh4865/.hermes/loop-engineering/hook_test.py`

Hook detect task type, auto-invoke quality-checker, run /goal loop nếu có, update state file. HERMES_HOME-aware — mỗi profile có state riêng.

---

### [FILE] 2026-06-16 19:55:48 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/hook.py`

- **Action:** create
- **Note:** Main gateway hook — auto quality-checker + /goal detection + state update. HERMES_HOME-aware.


---

### [FILE] 2026-06-16 19:55:48 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/hook_config.yaml`

- **Action:** create
- **Note:** Hook config: thresholds, per-profile banned words, skip conditions


---

### [QA] 2026-06-16 19:55:48 +0700 (STEP-6) — **PASS**

**Note:** Hook tests — GOOD=PASS, BAD(voice)=FAIL, Q&A=SKIP. 3/3 pass.

---

## [STEP-6] 2026-06-16 19:55:48 +0700 — Tạo Hermes gateway hook - DONE

**Status:** done
**Files affected:** `/Users/tuananh4865/.hermes/loop-engineering/hook.py`, `/Users/tuananh4865/.hermes/loop-engineering/hook_config.yaml`

Hook 3 events: agent:end (run quality-checker), cron:job:done (log to state), session:start (load state). HERMES_PROFILE-aware. 3/3 tests pass.

---

### [QA] 2026-06-16 19:56:10 +0700 (STEP-7) — **PASS**

**Note:** E2E test — quality-checker correctly distinguishes PASS vs FAIL across iterations, state.md gets logged.

---

## [STEP-7] 2026-06-16 19:56:10 +0700 — E2E test + report

**Status:** done
**Files affected:** _(chưa tạo file)_

End-to-end test: research-lead profile, 2 iterations (FAIL → PASS). Hook detect task type, run quality-checker, log verdict to state.md. Working as designed.

---

### [FILE] 2026-06-16 19:56:29 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/hook.py`

- **Action:** edit
- **Note:** Fix quality severity: research tasks = critical severity for chung chung phrases (no data = no research)


---

### [QA] 2026-06-16 19:56:29 +0700 (STEP-7) — **PASS**

**Note:** E2E test (fixed) — Iteration 1 now FAIL (critical severity), Iteration 2 PASS, state.md logged

---

## [STEP-ACTIVATE-1] 2026-06-16 19:58:58 +0700 — Register Loop Engineering hook vào Hermes gateway

**Status:** in_progress
**Files affected:** `/Users/tuananh4865/.hermes/hooks/loop-engineering/HOOK.yaml`, `/Users/tuananh4865/.hermes/hooks/loop-engineering/handler.py`

Copy hook.py + tạo HOOK.yaml theo format Hermes (folder + HOOK.yaml + handler.py). Restart gateway để load. Auto-fire trên agent:end, cron:job:done, session:start.

---

### [FILE] 2026-06-16 20:00:05 +0700 — `/Users/tuananh4865/.hermes/hooks/loop-engineering/HOOK.yaml`

- **Action:** create
- **Note:** Loop engineering hook metadata: 3 events (agent:end, cron:job:done, session:start)


---

### [FILE] 2026-06-16 20:00:05 +0700 — `/Users/tuananh4865/.hermes/hooks/loop-engineering/handler.py`

- **Action:** create
- **Note:** Handler với format chuẩn Hermes: def handle(event_type, context). Quality-checker embedded. HERMES_HOME-aware.


---

### [QA] 2026-06-16 20:00:05 +0700 — **PASS**

**Note:** Loop engineering hook registered at ~/.hermes/hooks/loop-engineering/ — Hermes will auto-discover on next gateway restart

---

### [FILE] 2026-06-16 20:03:30 +0700 — `/Users/tuananh4865/.hermes/hooks/loop-engineering/HOOK.yaml`

- **Action:** edit
- **Note:** Removed cron:job:done (not in Hermes event list). Hermes supports: agent:start, agent:end, session:start, etc.


---

### [QA] 2026-06-16 20:03:30 +0700 — **PASS**

**Note:** ACTIVATE-1 done — hook registered tại ~/.hermes/hooks/loop-engineering/ với format Hermes chuẩn

---

## [STEP-ACTIVATE-1] 2026-06-16 20:07:48 +0700 — Activate shell hooks trong Hermes config.yaml

**Status:** in_progress
**Files affected:** `/Users/tuananh4865/.hermes/config.yaml`

Format Hermes chuẩn: hooks: { event_name: [ { command, timeout } ] }. Subscribe agent:end + session:start để auto-invoke quality-checker + load state.

---

### [FILE] 2026-06-16 20:08:03 +0700 — `/Users/tuananh4865/.hermes/config.yaml`

- **Action:** edit
- **Note:** Added hooks: { agent:end, session:start, session:end } with shell commands invoking hook.py


---

### [FILE] 2026-06-16 20:08:03 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/hook_wrapper.sh`

- **Action:** create
- **Note:** Wrapper bash script — set HERMES_HOME + HERMES_PROFILE, exec python3 hook.py with args


---

### [FILE] 2026-06-16 20:09:33 +0700 — `/Users/tuananh4865/.hermes/config.yaml`

- **Action:** edit
- **Note:** Fix event names: agent:end/session:start/session:end → on_session_start/on_session_end/post_tool_call (Hermes VALID_HOOKS)


---

### [QA] 2026-06-16 20:09:33 +0700 — **PASS**

**Note:** Hermes hooks registered với event names chuẩn (on_session_start, on_session_end, post_tool_call)

---

### [FILE] 2026-06-16 20:09:50 +0700 — `/Users/tuananh4865/.hermes/loop-engineering/hook.py`

- **Action:** edit
- **Note:** Accept new Hermes event names: on_session_start, on_session_end, post_tool_call


---

## [STEP-ACTIVATE-1] 2026-06-16 20:10:14 +0700 — Activate shell hooks trong Hermes config.yaml - DONE

**Status:** done
**Files affected:** `~/.hermes/config.yaml`, `~/.hermes/loop-engineering/hook.py`, `~/.hermes/loop-engineering/hook_wrapper.sh`

3 hooks registered với Hermes VALID_HOOKS names: on_session_start, on_session_end, post_tool_call. Test pass với exit 0. Hermes sẽ auto-fire các hooks này cho mọi session.

---

### [QA] 2026-06-16 20:10:14 +0700 — **PASS**

**Note:** ACTIVATE-1: 3 hooks registered + test exit 0. Hook fired successfully.

---

### [QA] 2026-06-16 20:11:39 +0700 — **PASS**

**Note:** ACTIVATE-1 DONE: 3 hooks (on_session_start, on_session_end, post_tool_call) all healthy + allowlisted + valid JSON

---

## [STEP-ACTIVATE-2] 2026-06-16 20:12:06 +0700 — Tạo memory-curator profile (nếu cần)

**Status:** in_progress
**Files affected:** _(chưa tạo file)_

Check current profiles: content-director (TikTok), research-lead (Research), coder (Code). No dedicated memory/wiki profile. Tạo memory-curator để offload wiki ingestion + memory updates.

---

### [FILE] 2026-06-16 20:12:51 +0700 — `/Users/tuananh4865/.hermes/profiles/memory-curator/SOUL.md`

- **Action:** create
- **Note:** Memory Curator persona — wiki + memory expert. 6 sections: identity, mission, workflow, voice, tools, anti-patterns


---

### [FILE] 2026-06-16 20:12:51 +0700 — `/Users/tuananh4865/.hermes/profiles/memory-curator/state.md`

- **Action:** create
- **Note:** Init state.md từ template cho memory-curator profile


---

### [QA] 2026-06-16 20:12:51 +0700 — **PASS**

**Note:** memory-curator profile created với 73 skills, SOUL.md, state.md. Ready to use.

---

## [STEP-ACTIVATE-2] 2026-06-16 20:12:59 +0700 — Tạo memory-curator profile - DONE

**Status:** done
**Files affected:** `/Users/tuananh4865/.hermes/profiles/memory-curator/SOUL.md`, `/Users/tuananh4865/.hermes/profiles/memory-curator/state.md`

memory-curator profile: wiki + memory expert. 73 skills synced. Wrapper: memory-curator chat. Description: 'Manages wiki, ingests content, updates memory...'.

---

## [STEP-ACTIVATE-3] 2026-06-16 20:13:10 +0700 — Hook vào cron jobs - tự động update state mỗi lần cron chạy

**Status:** in_progress
**Files affected:** _(chưa tạo file)_

Found 7 cron jobs. Strategy: wrap each job's prompt với hook call. Or: tạo cron wrapper script.

---

### [FILE] 2026-06-16 20:14:00 +0700 — `/Users/tuananh4865/.hermes/cron/jobs.json`

- **Action:** edit
- **Note:** Append Loop Engineering hook section to 7 cron job prompts


---

### [QA] 2026-06-16 20:14:00 +0700 — **PASS**

**Note:** ACTIVATE-3: 7/7 cron jobs updated với Loop Engineering hook

---

## [STEP-ACTIVATE-3] 2026-06-16 20:14:07 +0700 — Hook vào cron jobs - DONE

**Status:** done
**Files affected:** `/Users/tuananh4865/.hermes/cron/jobs.json`

7/7 cron jobs updated với Loop Engineering hook section. Mỗi job: backup→default, autoresearch→research-lead, X research→research-lead, session review→default, wiki health→memory-curator, memory forget→memory-curator, TikTok monitor→content-director.

---

### [FILE] 2026-06-16 20:14:26 +0700 — `/Users/tuananh4865/.hermes/profiles/content-director/state.md`

- **Action:** edit
- **Note:** Fix timestamp: replace concatenated timestamps với single value


---

### [QA] 2026-06-17 00:32:31 +0700 (STEP-1) — **PASS**

**Note:** Quality checker test suite — 3/3 cases verdicts match expectations

---
