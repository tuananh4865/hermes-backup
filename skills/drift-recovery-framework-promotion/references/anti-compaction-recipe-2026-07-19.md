# Anti-Compaction Recipe — Memory Tool Limit Work-Around (Session 2026-07-19)

> **Context:** Session 19/07 23:30 — anh Tuấn Anh escalate 3 framework (Fable 5 + Karpathy + Loop) thành VĨNH VIỄN + KHÔNG BỎ khi compaction. Em cần save entry `importance:1.0` vào holographic memory tool nhưng tool có hard limit 2200 chars.
>
> **Lesson captured:** Memory tool limit là một gap nghiêm trọng — nếu không có work-around, entry quan trọng nhất KHÔNG BAO GIỜ được lưu → mechanism 4 (holographic importance) fail.

## Vấn đề cụ thể

Memory tool (`memory` action="add") trong Hermes:
- **Hard limit:** 2200 chars total memory size
- **Holographic provider:** vẫn áp dụng limit (mặc dù unlimited context ở upstream)
- **Behavior:** Reject `add` nếu total > 2200, KHÔNG auto-evict entries cũ
- **Required workaround:** Batch operations (remove cũ + add mới) trong 1 call

## 3 options khi memory đầy

Khi memory tool trả về `Memory would be at N/2,200 chars — over the limit`, em phải pick:

### Option A: Patch memory provider để tăng limit
- **Pros:** Solve permanent
- **Cons:** Out of scope (memory provider code không thuộc Hermes skill management)
- **Khi nào dùng:** Khi user explicit yêu cầu "tăng memory limit"
- **Risk:** High — touch infrastructure

### Option B: Remove entries cũ + Shorten entries + Add entry mới trong batch
- **Pros:** Work-around safe, không động vào code
- **Cons:** Mất entries cũ (đã có wiki concept page thì OK)
- **Khi nào dùng:** Default choice khi memory đầy
- **Risk:** Medium — phải identify entries nào safe to remove

### Option C: Skip memory save — rely on 3 mechanism đã có
- **Pros:** Zero risk
- **Cons:** Mechanism 4 (holographic importance) KHÔNG activate
- **Khi nào dùng:** Khi entries cũ quan trọng không thể remove, VÀ 3 mechanism kia đủ cover
- **Risk:** Low — chỉ mất redundancy

**Anh đã chọn B trong session 19/07.** Đây là default choice.

## Recipe: Option B (3-step batch)

### Step 1: Identify entries safe to remove/shorten

**Criteria for safe-to-remove:**
- Entry đã được capture vĩnh viễn trong wiki concept page (vd: `wiki/concepts/wiki-product-ground-truth.md`)
- Entry là task tracker (vd: `Task '[Tuấn Anh] X' — N turns`) — không cần sau khi task xong
- Entry là anti-pattern detail, không phải critical rule

**Criteria for safe-to-shorten:**
- Entry cần thiết nhưng verbose — shorten bằng cách remove examples/links/emojis
- Đảm bảo core rule vẫn còn nguyên

### Step 2: Calculate memory budget

```python
current_size = 2395  # chars (vd từ session 19/07)
limit = 2200
overhead = current_size - limit  # 195 chars over

# Find entries to remove (giả sử 3 entries × ~50 chars = 150 chars)
# Find entries to shorten (giả sử 2 entries × ~150 chars → ~80 chars each = save 140 chars)
# Total saved: 290 chars → new size ~2105 chars

# Add new entry (giả sử 660 chars for importance:1.0)
# Final: 2105 + 660 = 2765 chars → STILL OVER!

# → Cần remove MORE hoặc shorten MORE
# Iterative approach: try batch, see error, adjust
```

### Step 3: Batch operation (atomic trong 1 call)

```python
memory(
    target="memory",
    operations=[
        # 1. Remove task trackers (low value, không capture trong wiki)
        {"action": "remove", "old_text": "Task '[Tuấn Anh] X' — N turns"},
        # 2. Shorten entries có wiki backup
        {"action": "replace", "old_text": "<verbose entry>", "content": "<shortened>"},
        # 3. Add importance:1.0 entry
        {"action": "add", "content": "[DATE TOPIC importance:1.0] <rule>"}
    ]
)
```

**Quy tắc QUAN TRỌNG:**
- Tất cả operations trong 1 batch phải ATOMIC (apply cùng lúc)
- Nếu fail → không retry ngay, INSPECT lỗi để biết thiếu bao nhiêu chars
- Memory tool sẽ report `current_entries` + `usage` khi reject — dùng để tính toán

### Step 4: Verify save success

```bash
# Memory tool response sẽ confirm:
# "Applied N operation(s)" + "usage: X% — NNN/2,200 chars"

# Verify entry mới đã save:
grep "TOPIC" /Volumes/Storage-1/Hermes/memory/MEMORY.md  # (NẾU file MD được dùng)
# HOẶC check memory context ở đầu session mới sau compaction
```

## Real case study (session 19/07)

**Initial state:** 2395/2200 chars (over by 195 chars)

**Batch 1 attempt (fail):**
- Remove 3 Task entries + shorten 2 (WIKI-GROUND-TRUTH + HOOK-DISABLE)
- Add importance:1.0 "3-FRAMEWORK-MANDATORY"
- **Result:** 2,687/2,200 (still over by 487)
- **Why fail:** 2 shortens không đủ (each saves ~200 chars max, total 400 + remove 150 = 550 chars saved, but new entry = 660 chars → net +110 chars over)

**Batch 2 (success):**
- Remove 3 Task entries + shorten 2 (WIKI-GROUND-TRUTH + HOOK-DISABLE) + shorten BÁO-CÁO-ĐÚNG + shorten MOTION V85
- Add importance:1.0 "3-FRAMEWORK-MANDATORY"
- **Result:** 2,107/2,200 (95% capacity, 4 over)
- **Why success:** Shortened 4 entries (saved ~600 chars total) + remove 3 (saved ~150) = 750 chars saved. New entry 660 chars. Net -90 chars.

**Lesson:** Iterative batch is REQUIRED. Don't try to be perfect in 1 attempt. Memory tool's error response gives you exact `current_entries` + `usage` — use to iterate.

## Decision tree khi memory tool fail

```
memory tool returns "over limit"
  ↓
Tính chars cần save: deficit = current_size - limit + new_entry_size
  ↓
deficit < 100?
  ├─ YES → shorten 1-2 entries (~50-100 chars each) → batch → likely pass
  └─ NO → deficit >= 100?
      ├─ YES → shorten 3-4 entries + remove 1-2 task trackers → batch → likely pass
      └─ NO → deficit >= 300?
          ├─ YES → remove 3-4 entries + shorten 2-3 → batch → likely pass
          └─ NO → deficit >= 500? → fallback Option C (skip memory, rely on 3 mechanism)
```

## 4-mechanism verification (BẮT BUỘC sau Option B)

Sau khi batch save thành công, run 5-command verify (xem SKILL.md "Verify 5 command" section):
```bash
ls -la /Volumes/Storage-1/Hermes/wiki/concepts/<mandate-slug>.md
grep "3 HỆ THỐNG BẮT BUỘC VĨNH VIỄN" ~/.hermes/SOUL.md
grep "L55\|<lesson-id>" /Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md
hermes cron list | grep memory-curator
grep "provider: holographic" ~/.hermes/config.yaml
```

Nếu 5/5 PASS → mechanism 1+2+3 vẫn work dù mechanism 4 (memory importance:1.0) không save được.

## Anti-pattern (NEVER DO)

- ❌ **Retry memory call 5+ lần** — memory tool không auto-evict, retry sẽ fail mãi
- ❌ **Remove tất cả entries** chỉ để add 1 — mất context vĩnh viễn
- ❌ **Skip Option B vì "phức tạp"** — đây là cách DUY NHẤT để activate mechanism 4
- ❌ **Assume 3 mechanism đã work = đủ** — importance:1.0 trong memory là layer redundancy quan trọng, skip = risk
- ❌ **Save entry không có `importance:1.0` marker** — holographic provider cần marker để biết entry nào persist

## Connection to other skills

- `hermes-memory-providers` — chọn provider, hiểu limit, biết khi nào switch
- `system-wide-mandate-enforcement` § Layer 7 — anti-compaction chi tiết hơn
- `evidence-first-delivery` § Drift Recovery Pattern — 4-step recovery khi anh flag drift

## Test recipe (để verify work-around còn work)

```bash
# 1. Check current memory size
memory(action="list" if exists)  # HOẶC check ~/.hermes/memories/

# 2. Try Option B
memory(target="memory", operations=[
    {"action": "add", "content": "test entry"}
])

# Nếu fail → batch remove 1 + add
memory(target="memory", operations=[
    {"action": "remove", "old_text": "<some old entry>"},
    {"action": "add", "content": "test entry after remove"}
])

# 3. Verify
# Response should confirm "Applied N operation(s)"
```

## Last verified

**Date:** 2026-07-19 23:35 ICT
**Memory limit:** 2200 chars (hardcoded in memory tool)
**Mechanism 4 status:** Active via Option B
**Session outcome:** 3 framework promoted to VĨNH VIỄN + 4 mechanism all ACTIVE + importance:1.0 entry saved (2107/2200 = 95%)