---
name: hermes-memory-providers
description: Manage Hermes external memory providers (holographic, byterover, honcho, mem0, openviking, hindsight, retaindb, supermemory, wiki). Class-level skill covering activation (`hermes memory setup`), provider selection criteria, fact_store tool usage (add/search/probe/related/reason/contradict/list), migration between built-in MEMORY.md (hard cap 2,200 chars) and unlimited external providers, and SQLite/HRR internals. Load when user says "memory không đủ", "extend memory", "infinite memory", "lưu nhiều thứ", "mở rộng memory", "memory provider", or asks to switch/upgrade the memory backend.
---

# Hermes Memory Providers

## Why this skill exists

**User verbatim (2026-07-19):** *"Mở rộng memory thành vô hạn để có thể lưu trữ nhiều thứ quan trọng hơn"*

The pain point: Built-in `~/.hermes/memories/MEMORY.md` has a **hard cap of 2,200 chars** (configured via `memory_char_limit` in `~/.hermes/config.yaml`). Every `memory` tool call to add a fact checks this limit. When full, the tool returns an error like *"After applying all N operations, memory would be at 3,146/2,200 chars -- over the limit. Remove or shorten more entries..."* — forcing the agent to delete older entries to make room, which loses long-term context.

The fix: Hermes ships with **8 external memory provider plugins** (holographic, byterover, honcho, mem0, openviking, hindsight, retaindb, supermemory) that give **unlimited** persistent storage with semantic search. They run *alongside* the built-in memory (additive, never replacement).

## When to load

- User says "memory không đủ", "extend memory", "infinite memory", "mở rộng memory", "lưu nhiều thứ quan trọng", "vượt quá char limit"
- User asks "có memory provider nào không?", "memory unlimited?", "switch memory provider"
- Agent hits the 2,200 char cap and needs to migrate existing entries to an external store
- User wants semantic search / cross-session knowledge graph instead of substring matching
- A `fact_store` tool is available in the session and the agent needs to use it (add, search, probe, etc.)
- **Any write to `~/.hermes/memory_store.db`** — load BEFORE activating holographic. Hermes-Only-Folder-Rule says file lives at `/Volumes/Storage-1/Hermes/.hermes-data/`, symlinked back (Lesson 5 below).

## The 8 providers at a glance

| Provider | Backend | Needs API Key? | Setup | Best for |
|---|---|---|---|---|
| **holographic** | LOCAL SQLite + FTS5 + HRR | ❌ No | `hermes memory setup holographic` | **Default local choice** — unlimited, semantic search, no signup |
| wiki | LOCAL markdown mirror | ❌ No | (already active by default) | Wiki-as-memory mirror, but still hard-capped by MEMORY.md |
| byterover | Local or Cloud | Optional | `hermes memory setup byterover` | Hybrid (local cache + cloud sync) |
| hindsight | Local or Cloud | Optional | `hermes memory setup hindsight` | Self-improving recall |
| holographic | Local | ❌ No | (see above) | **Same as above — only one LOCAL option** |
| honcho | Cloud or self-hosted | Required | `hermes memory setup honcho` | Multi-agent peer modeling |
| mem0 | Cloud | Required | `hermes memory setup mem0` | Server-side fact extraction |
| openviking | Self-hosted server | Required | `hermes memory setup openviking` | Hierarchical knowledge, tiered reads |
| retaindb | Local | ❌ No | `hermes memory setup retaindb` | Retention-scored retrieval |
| supermemory | Cloud | Required | `hermes memory setup supermemory` | Cross-session user modeling |

**Rule of thumb:** If anh doesn't want to sign up for anything → **holographic** (only fully-local provider with unlimited + semantic search). If anh already has API keys for cloud providers → pick by use case (mem0 for fact extraction, honcho for peer modeling, etc.).

## Activation workflow

### Step 0 (MANDATORY) — Hermes-Only-Folder setup via symlink (do this BEFORE Step 1)

Per Hermes-Only-Folder-Rule (operational since 2026-07-19), the real DB MUST live at `/Volumes/Storage-1/Hermes/.hermes-data/memory_store.db` — not at the default `~/.hermes/memory_store.db`. Use the symlink pattern:

```bash
# Check existing DB (don't lose data)
if [[ -f ~/.hermes/memory_store.db && ! -L ~/.hermes/memory_store.db ]]; then
    mv ~/.hermes/memory_store.db ~/.hermes/memory_store.db.bak-$(date +%Y-%m-%d)
fi

# Place real DB at Hermes
mkdir -p /Volumes/Storage-1/Hermes/.hermes-data

# Symlink Hermes hardcoded path → real DB at Hermes
ln -sf /Volumes/Storage-1/Hermes/.hermes-data/memory_store.db ~/.hermes/memory_store.db

# Verify
ls -la ~/.hermes/memory_store.db  # should show symlink → /Volumes/Storage-1/Hermes/...
```

If you skip Step 0, `hermes memory setup holographic` will create the DB at `~/.hermes/` and anh will catch the violation (as happened 19/07).

### Step 1: Check current provider

```bash
hermes memory status
```

Output shows:
- Built-in: always active (MEMORY.md, 2,200 char cap)
- Provider: <name> or "none"
- Plugin: installed ✓ / available ✓

### Step 2: Activate holographic (the default local pick)

```bash
hermes memory setup holographic
# Or non-interactive:
hermes config set memory.provider holographic
```

Output: `Activation saved to config.yaml`

### Step 3: **Restart the gateway** — required for `fact_store` tool to appear in session

```bash
bash ~/.hermes/restart-hermes-gateway.sh  # run from Terminal macOS, not Telegram session
```

**Critical pitfall:** The gateway blocks self-restart with: *"Blocked: cannot restart or stop the gateway from inside the gateway process."* Always run from a separate shell. After restart, wait 30s, then `hermes memory status` again to confirm.

### Step 4: Verify `fact_store` tool is available

Send any message in the new Telegram session. The system prompt should now include `fact_store` as a tool. Test with a probe:

```
fact_store action=list
```

Should return facts (empty list if first use).

### Step 5 (optional): Migrate existing MEMORY.md entries to holographic DB

Use the Python API directly (works without gateway restart). Note the `db_path` parameter points to the symlink at `~/.hermes/`, but the underlying file is at Hermes:

```bash
~/.hermes/hermes-agent/.venv/bin/python <<'EOF'
import os
os.environ['HERMES_HOME'] = '/Users/tuananh4865/.hermes'
import sys
sys.path.insert(0, '/Users/tuananh4865/.hermes/hermes-agent')
sys.path.insert(0, '/Users/tuananh4865/.hermes/hermes-agent/.venv/lib/python3.12/site-packages')
from plugins.memory.holographic.store import MemoryStore

# Read via symlink → real DB at /Volumes/Storage-1/Hermes/.hermes-data/
store = MemoryStore(db_path='/Users/tuananh4865/.hermes/memory_store.db')

# Read existing entries from MEMORY.md (parse §-separated lines)
with open('/Users/tuananh4865/.hermes/memories/MEMORY.md') as f:
    content = f.read()

for entry in content.split('§'):
    entry = entry.strip()
    if not entry:
        continue
    # Extract date tag from [DD/MM ...] prefix
    import re
    tag_match = re.search(r'\[(\d+/\d+)\s+([^\]]+)\]', entry)
    tag = tag_match.group(2) if tag_match else 'misc'
    store.add_fact(
        content=entry,
        category='project' if 'rule' in tag.lower() else 'tool',
        tags=tag.lower().replace(' ', ',').replace('-', ','),
    )
    print(f'✅ Migrated: {tag}')
EOF
```

DB location: `/Volumes/Storage-1/Hermes/.hermes-data/memory_store.db` (SQLite, grows with usage, accessible via `~/.hermes/memory_store.db` symlink).

## `fact_store` tool actions (9 total)

Available after gateway restart with holographic active:

| Action | Params | Use case |
|---|---|---|
| **add** | `content` (required), `category`, `tags` | Store a fact — no char cap, unlimited entries |
| **search** | `query` (required), `limit`, `min_trust` | FTS5 keyword search → ranked results |
| **probe** | `entity` (required) | ALL facts about a person/thing/concept (entity resolution) |
| **related** | `entity` (required) | Structural adjacency — what's connected to X |
| **reason** | `entities` (list, required) | Compositional: facts that mention MULTIPLE entities simultaneously (HRR algebra) |
| **contradict** | (no extra params) | Memory hygiene — find facts making conflicting claims |
| **update** | `fact_id`, optional `trust_delta`, `content` | Update existing fact (e.g., adjust trust score after seeing it was helpful) |
| **remove** | `fact_id` (required) | Delete a fact |
| **list** | `limit`, `min_trust` | List all facts (newest first) |

Plus `fact_feedback` tool: rate a fact as `helpful`/`unhelpful` → trains trust score for future ranking.

### Fact schema (what each entry looks like)

```json
{
  "fact_id": 7,
  "content": "[19/07 HOOK-DISABLE-PATTERN] Disable hook = 5 chỗ...",
  "category": "tool",
  "tags": "hook,disable,backup,template",
  "trust_score": 0.5,
  "retrieval_count": 0,
  "helpful_count": 0,
  "created_at": "2026-07-19 16:10:52",
  "updated_at": "2026-07-19 16:10:52"
}
```

- `category`: `user_pref` | `project` | `tool` | `general` (used for filtering)
- `tags`: comma-separated, used for `probe`/`related` matching
- `trust_score`: 0.0–1.0, starts at 0.5, rises with `helpful` feedback, falls with `unhelpful`

## Daily workflow (after migration)

**When anh says something important worth remembering:**
```
fact_store action=add content="[YYYY-MM-DD TAG] Lesson..." category="project" tags="tag1,tag2"
```

**When anh asks "em đã biết gì về X?":**
```
fact_store action=probe entity="X"  # OR
fact_store action=search query="X"
```

**When a fact was useful, reinforce it:**
```
fact_feedback fact_id=<id> rating=helpful
```

**When anh wants to clean up:**
```
fact_store action=remove fact_id=<id>  # OR
fact_store action=contradict  # find duplicates
```

## Common pitfalls

- **Built-in memory is STILL 2,200 chars even with provider active** (Holographic is *additive*, not replacement). The `memory` tool still hits the cap for MEMORY.md. Use `fact_store` for unlimited storage, NOT the `memory` tool. Old `memory` tool calls will keep failing.

- **Gateway restart is required for `fact_store` tool to appear** — `hermes memory setup` only writes config. The tool is registered at gateway startup. Until restart, `fact_store` won't show up in the agent's tool list. (Same pattern as any daemon config change — see `hermes-cron-management` skill.)

- **`hermes memory reset` erases MEMORY.md AND USER.md** — irreversible. Use only when intentionally starting fresh. To migrate, copy entries first.

- **`hermes memory off` only disables external provider, leaves built-in intact** — safe revert. Use to temporarily turn off holographic if it's misbehaving.

- **Python venv matters** — use `~/.hermes/hermes-agent/.venv/bin/python` (Python 3.11/3.12), NOT system `python3`. System Python 3.9 lacks `ContextVar | type` syntax support → import error.

- **`auto_extract: false` by default** — holographic does NOT auto-extract facts at session end. You must explicitly call `fact_store action=add` for each important learning. Set `auto_extract: true` in config if you want automatic extraction (but expect noise).

- **Don't try to install multiple providers at once** — Hermes docs: *"Only one external provider can be active at a time."* Switch with `hermes memory setup <new>`, don't try to run two simultaneously.

- **DB path is hardcoded `~/.hermes/memory_store.db`** — Hermes reads from this exact path regardless of config. Per Hermes-Only-Folder-Rule (operational since 2026-07-19, verified), the real DB MUST live at `/Volumes/Storage-1/Hermes/.hermes-data/memory_store.db` with a symlink at the hardcoded path. See Lesson 5 below for the exact procedure.

## Linked files

- `references/provider-comparison.md` — Detailed feature matrix + when to pick each of the 8 providers
- `references/fact-store-api.md` — Full fact_store + fact_feedback schema, return types, error modes
- `references/migration-script.md` — Ready-to-run Python script to migrate MEMORY.md → holographic DB
- `references/holographic-internals.md` — How SQLite + FTS5 + HRR algebra actually work under the hood

## Lessons learned (vĩnh viễn — 19/07/2026)

### Lesson 1 — Memory cap is a SYSTEM-WIDE constraint, not a bug
**Trigger:** Em phải xóa entry cũ mỗi lần add mới vì 2,200 char cap. Tưởng là bug, nhưng thực tế là design decision: MEMORY.md được inject vào MỌI system prompt (per-conversation caching is sacred per Hermes AGENTS.md). Nếu unlimited → cache invalidation liên tục → cost explode.

**Rule:** Memory cap = trade-off giữa cache stability vs unlimited context. Hermes giải quyết bằng cách cho external provider (additive, không inject vào system prompt mỗi turn). Khi cần lưu unlimited → dùng `fact_store`, KHÔNG spam `memory` tool.

### Lesson 2 — `fact_store` ≠ replacement cho `memory` tool
**Trigger:** Em lúc đầu nghĩ activate holographic = memory unlimited. KHÔNG ĐÚNG. Built-in `memory` vẫn cap 2,200 chars. `fact_store` là TOOL MỚI với database riêng, dùng cho unlimited storage.

**Rule:** Sau khi activate holographic, agent có 2 tools song song:
- `memory` (built-in, 2,200 cap, always injected into context) → cho "always-on" critical rules
- `fact_store` (holographic, unlimited, on-demand lookup) → cho deep recall, history, facts ít dùng

**Rule of thumb:** Nếu fact CẦN luôn trong context (style rules, hard constraints) → dùng `memory`. Nếu fact chỉ cần khi search/probe → dùng `fact_store`.

### Lesson 3 — Provider choice driven by 1 question: API key willing?
**Trigger:** Em research 4 approaches (A: tăng cap, B: wiki provider, C: holographic, D: self-managed files). Pick C vì:
- LOCAL (no API key) → không cần đăng ký
- Unlimited (SQLite) → không bị disk cap
- Semantic search built-in (FTS5 + HRR) → không cần build riêng
- Hermes built-in → không cần install

**Rule:** Khi user muốn "memory unlimited" / "extend memory" mà KHÔNG nói gì về cloud → default `holographic`. Nếu user đã có cloud API keys → hỏi preference (mem0 cho fact extraction, honcho cho multi-agent, etc.).

### Lesson 4 — Activate BEFORE placing DB at Hermes = Hermes-Only-Folder violation
**Trigger:** Em `hermes memory setup holographic` → `setup` saved config AND immediately created `~/.hermes/memory_store.db` (Hermes's hardcoded default path). Then em migrate 7 facts in → facts stored at `~/.hermes/memory_store.db`, NOT at `/Volumes/Storage-1/Hermes/`. Anh catch lỗi: *"Anh đã nói tất cả path chuyển sang storage-1/Hermes mà"*. Em phải fix ngay.

**Rule (correct order):**
1. **PRE-FLIGHT** — check if `~/.hermes/memory_store.db` exists → back up to `~/.hermes/memory_store.db.bak-<date>`
2. **PLACE** real DB at `/Volumes/Storage-1/Hermes/.hermes-data/memory_store.db` (mkdir first)
3. **SYMLINK** `~/.hermes/memory_store.db` → `/Volumes/Storage-1/Hermes/.hermes-data/memory_store.db`
4. **ACTIVATE** provider (`hermes memory setup holographic`)
5. **MIGRATE** facts → `fact_store action=add` (read via symlink, write to Hermes path)
6. **VERIFY** with `fact_store action=list` (sau gateway restart)

**Symlink command (canonical):**
```bash
# Stop provider first to release any DB lock
hermes memory off

# Setup folders + create real DB at Hermes
mkdir -p /Volumes/Storage-1/Hermes/.hermes-data
touch /Volumes/Storage-1/Hermes/.hermes-data/memory_store.db

# Symlink Hermes system path → real DB
ln -sf /Volumes/Storage-1/Hermes/.hermes-data/memory_store.db ~/.hermes/memory_store.db

# Re-activate (now creates DB at the symlink target = Hermes)
hermes memory setup holographic

# Verify
ls -la ~/.hermes/memory_store.db  # should show symlink → Hermes path
```

**Why this matters:** Same pattern applies to ANY Hermes hardcoded path (`~/.hermes/config.yaml` is harder since YAML references break with symlinks — for those, the rule is "leave as-is in `~/.hermes/`"). For databases, symlinks work because DB is opaque blob. Apply per-file based on whether the format tolerates path indirection.

**Same pattern works for:** `~/.hermes/cron/output/<job-id>/` (mirror to `/Volumes/Storage-1/Hermes/cron-output/<job-id>/`), `~/.hermes/cache/` (mirror to `/Volumes/Storage-1/Hermes/.hermes-cache/`).

**Different pattern (NOT symlinkable):** `~/.hermes/config.yaml` (YAML parser follows symlink OK BUT many internal references like `$HERMES_HOME` resolve relative to the file's directory — symlinking causes double-resolution bugs). Rule: keep config in `~/.hermes/`, symlink only blob files (DBs, caches, outputs).

### Lesson 5 — Hermes-Only-Folder-Rule is OPERATIONAL (not aspirational)
**Trigger:** Even with proper symlink workflow (Lesson 4), em MUST check destination path TRƯỚC MỖI write_file / patch tool call. If destination starts with `/Users/tuananh4865/` AND not in approved symlinked list → STOP, redirect to `/Volumes/Storage-1/Hermes/`.

**Approved `~/.hermes/` exceptions (where files CAN live):**
- `~/.hermes/config.yaml` — YAML references break with symlinks, gateway reads at startup
- `~/.hermes/.env` and `.env.template` — contains API keys, gateway reads at startup
- `~/.hermes/.git/` — git internals (don't touch)
- `~/.hermes/hooks/` — gateway scans this dir for hook configs
- `~/.hermes/skills/` — registered at gateway startup, symlink-fragile
- `~/.hermes/profiles/` — multi-profile system
- `~/.hermes/state.db`, `.recent_session_context.txt` — runtime state
- `~/.hermes/<symlink>.db` or `<symlink>.sqlite` — DB blobs (use Lesson 4 pattern)

**Everything else** (new files, new logs, new scripts, new DBs) → **MUST go to `/Volumes/Storage-1/Hermes/`** with symlink back if Hermes hardcodes a path.

## Related skills

- `hermes-file-edit-logging` — Sibling skill for FILE EDIT audit. This is for MEMORY audit. Both use NDJSON-like append-only patterns.
- `hermes-cron-management` — Sibling for cron troubleshooting. Shares the gateway-restart pattern.
- `evidence-first-delivery` — When claiming "memory migration done", must show 5-evidence gate (count facts before/after, list sample, DB size).

---
*New class-level skill, 19/07/2026. Captures the infinite-memory migration: built-in MEMORY.md (2,200 char cap) → holographic provider (SQLite + FTS5 + HRR, unlimited).*
