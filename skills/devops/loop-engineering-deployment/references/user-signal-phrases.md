# User Signal Phrases — When to Deploy Loop Engineering System-Wide

When Tuấn Anh drops any of these phrases, he means the pattern should run as
infrastructure, not as a one-time task. Load `loop-engineering-deployment` immediately.

## Vietnamese

| Phrase | Meaning |
|--------|---------|
| "áp dụng ở quy mô hệ thống" | Apply system-wide, not per-project |
| "toàn bộ hệ thống" | Whole Hermes Agent instance |
| "anh không cần nhắc lại" | Don't ask me to remind you |
| "từ nay về sau" | From now on — persistent behavior |
| "hoàn toàn tự động" | Fully automatic, no manual trigger |
| "cho log vào wiki nữa" | Mirror to wiki (Obsidian + Hermes wiki) |
| "lưu vào file log" / "check logback" | Create an append-only changelog |
| "từng bước từng file" | Per-file logging, not per-step |
| "để khi cần check lại" | Auditability requirement |
| "anh OK em chạy" | Explicit confirmation — proceed |

## English

| Phrase | Meaning |
|--------|---------|
| "apply system-wide" | Whole system, not one project |
| "I shouldn't have to remind you" | Persistent behavior |
| "from now on" | Forever |
| "fully automatic" | No manual trigger |
| "log to wiki" / "logback" | Audit trail required |
| "log every step" | Per-step entries, not summary |
| "do it step by step" | Sequenced with QA gates between |

## What This Triggers

When you see these signals, deploy the 5 components:

1. `~/.hermes/loop-engineering/CHANGELOG.md` (changelog FIRST)
2. `~/.hermes/skills/quality-checker/` (universal quality gate)
3. `~/.hermes/skills/loop-goal/` (loop runner with safe condition parser)
4. `~/.hermes/workers/_template/state.md` (state file template)
5. `~/.hermes/hermes-agent/hooks/<name>-hook.py` (gateway auto-invoke)

PLUS:
- Wiki page in `/Volumes/Storage-1/Hermes/wiki/concepts/<name>-system.md`
- Mirror to iCloud Obsidian vault
- Append to `wiki/log.md`
- Update `wiki/index.md` with `[[<PageName>]]`

## Anti-Signals (don't deploy system-wide)

- "thử xem" (try it) → test, don't deploy
- "cho task này" (for this task) → one-off
- "tạm thời" (temporary) → one-off
- "cho project X" (for project X) → project-specific, not system-wide
- "gửi anh xem trước" (send me to review first) → preview, not deploy

## Confirmation Pattern

Before deploying, ALWAYS confirm scope. Don't assume "system-wide" when "for this project"
might be intended. Ask in Vietnamese:

> "Anh muốn áp dụng CHỈ cho project này, hay cho TOÀN BỘ hệ thống Hermes (từ nay về sau
> mọi task tự động)?"

If user says "toàn bộ" / "system-wide" / "anh không cần nhắc lại" → deploy all 5 components
with full wiki mirror.

## Pre-Deploy Question (always ask)

```python
# Quick check before triggering 5-component deployment
def should_deploy_system_wide(user_message: str) -> bool:
    triggers_vi = [
        "quy mô hệ thống", "toàn bộ hệ thống", "không cần nhắc lại",
        "từ nay về sau", "hoàn toàn tự động", "lưu vào file log",
        "check logback", "log vào wiki",
    ]
    triggers_en = [
        "system-wide", "from now on", "automatically",
        "no need to remind", "audit log", "log every",
    ]
    msg_lower = user_message.lower()
    return any(t in msg_lower for t in triggers_vi + triggers_en)
```

If the user uses any of these phrases, the deployment is a 5-component system-wide
rollout with mandatory changelog + wiki mirror — NOT a one-off task.
