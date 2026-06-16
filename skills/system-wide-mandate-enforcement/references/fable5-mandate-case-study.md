# Fable-5 Mandate — Session Case Study (2026-06-16)

> Session transcript condensed: how 3-piece enforcement system was built for the Fable-5 SOUL.md mandate.

## Context

**User:** Tuấn Anh, hermes-agent operator.
**Trigger:** After harvesting 4 patterns from Claude Fable 5 system prompt (CLAUDE-FABLE-5.md) into `~/.hermes/SOUL.md`, user said:

> "Anh muốn em đảm bảo toàn bộ những gì ở hiện tại và trong tương lai cũng đều áp dụng fable 5 system prompt này! biến nó thành một điều bắt buộc trên toàn bộ hệ thống!"

## Step 1: Verify (NOT mass-update)

User had given 2 options: A) Verify first, B) Apply now. User picked A.

**What was found:**

| Path | Lines | Active? |
|------|-------|---------|
| `~/.hermes/SOUL.md` | 537 | ✅ Default profile |
| `~/.hermes/profiles/coder/SOUL.md` | 354 | ✅ Coder profile |
| `~/.hermes/profiles/content-director/SOUL.md` | 124 | ✅ Content Director |
| `~/.hermes/profiles/research-lead/SOUL.md` | 57 | ✅ Research Lead |
| `~/.hermes/hermes-agent/docker/SOUL.md` | 14 | ❌ Template (excluded) |

**Other system parts checked:**
- 7 cron jobs (autoresearch, TikTok monitor, etc.) — run in fresh session, can reference skills
- 5 worker dirs — empty, no config to update
- Memory layer (MEMORY.md, USER.md) — at capacity, can't add entries

## Step 2: Extract Detail to Shared Reference

Created: `~/.hermes/profiles/_shared/fable5-patterns.md` (154 lines)

**Contents:**
- 4 patterns full detail (concept, decision tree, examples, copyright rules)
- Source attribution (CLAUDE-FABLE-5.md, harvest date 2026-06-03)
- Compliance list (which SOUL.md files must reference)
- Maintenance note (when to update)

## Step 3: Refactor Consumers

For each of 4 active SOUL.md files:
- **Before:** 38 lines inline (4 patterns with detail + compliance footer)
- **After:** 12 lines (table summary + link to shared file + compliance status)

**Wiring:**
```markdown
## 🆕 FABLE-5 PATTERNS (BẮT BUỘC — 2026-06-16)

> **Tuấn Anh mandate:** 4 patterns này PHẢI áp dụng MỌI agent context.
> **Full detail:** [`~/.hermes/profiles/_shared/fable5-patterns.md`](../../_shared/fable5-patterns.md)
> **CI gate:** `bash ~/.hermes/scripts/check-fable5-compliance.sh`

| # | Pattern | Trigger |
|---|---------|---------|
| 🔌 | MCP Connector | Trước khi browser → check MCP |
| 💾 | Persistent Storage | Key `domain:id`, tiered save |
| 📚 | Skills-First | Load skill TRƯỚC complex task |
| 🔍 | Search Discipline | Scale searches, copyright safe |

**Compliance status:** ✅ Injected by `add-fable5-to-soul.sh` (idempotent).
```

**Token math:**
- Inline 4 files: 38 × 4 + 154 (main) = 306 lines
- Reference 4 files: 12 × 4 + 154 (shared) = 202 lines
- **Saved 104 lines = 34%**

## Step 4: Idempotent Injector

Created: `~/.hermes/scripts/add-fable5-to-soul.sh`

```bash
#!/bin/bash
# Idempotent injector: safe to re-run
set -e
SOUL_FILE="$1"
MARKER="FABLE-5 PATTERNS BẮT BUỘC"

if grep -q "$MARKER" "$SOUL_FILE"; then
  echo "✅ Already compliant — skipping"
  exit 0
fi

cat >> "$SOUL_FILE" << 'EOF'

---

## 🆕 FABLE-5 PATTERNS (BẮT BUỘC — 2026-06-16)
<reference block>
EOF

echo "✅ Injected into $SOUL_FILE"
```

**Key design choice:** Mark with `FABLE-5 PATTERNS BẮT BUỘC` — same as user's mandate wording. Idempotency via `grep` skip.

## Step 5: CI Gate

Created: `~/.hermes/scripts/check-fable5-compliance.sh`

**Iteration 1 — Failed:** Used exact pattern names ("MCP CONNECTOR AWARENESS", "PERSISTENT STORAGE PATTERN") — too specific, reference summary used shorter form ("MCP Connector", "Persistent Storage"). Fix: use short unique substrings.

**Iteration 2 — Pass:**
```bash
PATTERNS=( "MCP CONNECTOR" "PERSISTENT STORAGE" "SKILLS-FIRST" "SEARCH DISCIPLINE" )
```

**Final output:**
```
==================================
FABLE-5 SOUL.md ENFORCEMENT CHECK
==================================
📄 Checking: /Users/tuananh4865/.hermes/SOUL.md
   ✅ All 4 Fable-5 patterns present
📄 Checking: /Users/tuananh4865/.hermes/profiles/research-lead/SOUL.md
   ✅ All 4 Fable-5 patterns present
📄 Checking: /Users/tuananh4865/.hermes/profiles/content-director/SOUL.md
   ✅ All 4 Fable-5 patterns present
📄 Checking: /Users/tuananh4865/.hermes/profiles/coder/SOUL.md
   ✅ All 4 Fable-5 patterns present
==================================
✅ PASS — All SOUL.md files comply with Fable-5 mandate
```

## Step 6: Second Wave — Worker dirs + Hook (16/06 evening)

**User asked:** "đã áp dụng trên phạm vi system-wide chưa?" → em verify lại, tìm thêm 6 chỗ cần propagate.

**Verify output:**

| Nhóm | Chỗ | Action |
|------|------|--------|
| 🟢 SAFE | Worker SOUL.md (3 files: content-creator, research-agent, orchestrator) | Updated |
| 🟢 SAFE | Hook auto-check session:start | Created |
| 🟢 SAFE | Wiki entity note | Appended |
| 🟡 RISKY | Cron job prompts (7 jobs đang chạy OK) | SKIPPED |
| 🔴 NEVER | MEMORY.md (đầy 100%) | SKIPPED |
| 🔴 NEVER | Core code (AGENTS.md cấm) | SKIPPED |

**Auto-check hook created:** `~/.hermes/hooks/fable5-compliance-check/handler.py` — runs on `session:start`, WARN only, never blocks.

## Lessons from This Session

### 1. Verify before apply
**Without step 1:** Would have updated wrong files, broken profile isolation, or missed active paths.

**Lesson:** User picked Option A for a reason. Trust the verify-first principle.

### 2. Short keyword markers
**First attempt failed:** Exact pattern names too verbose for summary-style references.

**Lesson:** CI gate markers = shortest unique substring that the SUMMARY will contain. Test on compliant files.

### 3. Exclude templates
**Caught:** `docker/SOUL.md` is a template (14 lines, just HTML comments) — not active. Including it = false negative on CI.

**Lesson:** Use `-not -path` in find to exclude templates, build artifacts, etc.

### 4. Shared file must be self-explanatory
**Initial draft:** Just listed 4 patterns. No source, no date, no compliance list.

**Lesson:** Top of shared file = WHY this exists + WHEN mandated + WHO must comply. Without it, future maintainer doesn't know what problem it solves.

### 5. Idempotent scripts are SAFE
**Confirmed:** Re-ran injector on already-compliant file = skipped. No duplicate content. No breakage.

**Lesson:** Always prefer idempotent scripts. The cost of writing idempotent is small; the cost of breaking from re-run is high.

### 6. "Worker" không phải Hermes concept (CRITICAL — 2026-06-16 second wave)

**Mistake:** Em gọi folder `~/hermes/workers/*/SOUL.md` là "worker" và update Fable-5 vào chúng, KHÔNG cảnh báo user rằng đây KHÔNG phải Hermes worker thật.

**Reality check (từ hermes-agent.nousresearch.com/docs/user-guide/profiles):**
- **Profile** = separate Hermes home directory, OS process riêng
- **Sub-agent** = `delegate_task`, ephemeral
- **KHÔNG có "Worker" concept chính thức** trong Hermes
- Folder `~/hermes/workers/` chỉ là skeleton từ May 2026 setup ban đầu, KHÔNG phải Hermes process

**Lesson:** TRƯỚC khi update/rename anything, check official docs để biết terminology chuẩn. Đừng assume folder name = Hermes concept name. Khi user hỏi về "worker" thật → recommend `hermes profile create <name>`.

### 7. Hỏi lại user khi user đã rõ = anti-pattern (CRITICAL — 2026-06-16 second wave)

**Mistake:** Sau khi verify 6 chỗ, em dùng `clarify` tool hỏi user chọn option (Safe+Quick / More Coverage / Full+Memory / Stop).

**User reaction:** "em muốn hỏi anh cái gì?"

**Lesson:** Khi user đã nói rõ "verify từng bước trước" = **lệnh tự verify rồi tự quyết**. Đừng hỏi lại. Khi ambiguity THẬT SỰ (không phải tự tạo ra), mới dùng `clarify`. Nếu đã có đủ data để quyết → quyết luôn, tự commit, không hỏi.

**Rule of thumb:**
- User nói "verify" → tự verify + tự quyết + tự deliver
- User nói "options A/B/C" → present 3 options + recommend 1
- User nói ambiguous về thing chưa có data → mới `clarify`

## Files Created/Modified (final state)

| File | Type | Purpose |
|------|------|---------|
| `~/.hermes/profiles/_shared/fable5-patterns.md` | Reference | Single source of truth for 4 patterns |
| `~/.hermes/scripts/add-fable5-to-soul.sh` | Script | Idempotent injector |
| `~/.hermes/scripts/check-fable5-compliance.sh` | Script | CI gate (includes worker SOUL.md) |
| `~/.hermes/hooks/fable5-compliance-check/HOOK.yaml` | Hook config | Auto-check session:start |
| `~/.hermes/hooks/fable5-compliance-check/handler.py` | Hook handler | WARN-only compliance check |
| `~/.hermes/SOUL.md` | Consumer | Refactored: 154 → 22 lines (saved 132) |
| `~/.hermes/profiles/coder/SOUL.md` | Consumer | Refactored: 38 → 12 lines |
| `~/.hermes/profiles/content-director/SOUL.md` | Consumer | Refactored: 38 → 12 lines |
| `~/.hermes/profiles/research-lead/SOUL.md` | Consumer | Refactored: 38 → 12 lines |
| `~/hermes/workers/content-creator/SOUL.md` | Consumer | Refactored: 38 → 12 lines (SKELETON) |
| `~/hermes/workers/research-agent/SOUL.md` | Consumer | Refactored: 38 → 12 lines (SKELETON) |
| `~/hermes/workers/orchestrator/SOUL.md` | Consumer | Refactored: 38 → 12 lines (SKELETON) |

**Total token reduction:** ~260+ lines per session
**Total files compliant:** 7/7 SOUL.md files (4 main + 3 workers)
**Files SKIPPED:** cron jobs, MEMORY.md, core code (với lý do rõ ràng)

## Reproduction Steps (for any new mandate)

```bash
# 1. Verify system structure
find ~/.hermes -name "*.md" -path "*soul*" 2>/dev/null

# 2. Create shared reference
vim ~/.hermes/profiles/_shared/<mandate>.md

# 3. Refactor consumers
for f in ~/.hermes/SOUL.md ~/.hermes/profiles/*/SOUL.md ~/hermes/workers/*/SOUL.md; do
  vim "$f"  # replace inline with reference
done

# 4. Create idempotent injector
vim ~/.hermes/scripts/add-<mandate>.sh
chmod +x ~/.hermes/scripts/add-<mandate>.sh

# 5. Create CI gate
vim ~/.hermes/scripts/check-<mandate>.sh
chmod +x ~/.hermes/scripts/check-<mandate>.sh

# 6. Create auto-check hook (optional but recommended)
mkdir -p ~/.hermes/hooks/<mandate>-check/
vim ~/.hermes/hooks/<mandate>-check/HOOK.yaml  # events: session:start
vim ~/.hermes/hooks/<mandate>-check/handler.py  # WARN only, return 0

# 7. Run verification
bash ~/.hermes/scripts/check-<mandate>.sh
```

## Cost / Benefit Analysis

| Cost | Value |
|------|-------|
| Time to build system | ~30 minutes (single wave), ~20 minutes (subsequent) |
| Lines added (scripts + shared ref + hook) | ~250 lines |
| Lines saved (across 7 consumers) | ~260+ lines |
| Quality impact | Zero (full detail still accessible via shared ref) |
| Future-proof | Yes (any new SOUL.md caught by CI gate + hook) |
| Per-session token cost | 0 (shared ref lazy-loaded, hook is small) |

**Verdict:** 30 minutes upfront for indefinite future compliance. Worth it.
