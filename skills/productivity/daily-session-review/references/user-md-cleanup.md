# USER.md Cleanup Reference

## When to clean

`~/.hermes/memories/USER.md` is corrupted by cron session review jobs that pass raw LLM scratchpad to the memory tool. Symptoms:

- File size > 1500 bytes
- Lines starting with `- [tool]`, `- [file]`, `- [model]`, `- [preference]` followed by fragments
- Unclosed quotes/parentheses
- Lines >200 chars that mix metadata tags
- Duplicate "2026-MM-DD:" entries

## Cleanup procedure (5 minutes)

### Step 1: Backup corrupted version
```bash
cp ~/.hermes/memories/USER.md ~/.hermes/memories/USER.md.bak.$(date +%s)
```

### Step 2: Apply canonical template

The canonical structure is 5 sections, each under 5 bullets, total <1500 bytes:

```markdown
§ [PREFERENCES] — explicit preferences discovered over sessions
- communication: Vietnamese casual
- response_style: concise, no fluff, no over-engineering
- tiktok_script_style: TRUNG TÍNH ("các bạn" / "mọi người" — banned 2026-06-13)
- ownership: own tasks end-to-end, no follow-up questions
- audit_style: tests BY HAND in browser, reads code rarely
§ [PROJECTS] — ongoing work
- tiktok-content: active (channel pivot Setup/Edit/Lighting — 45 days pure value)
- hermes-agent: system-wide mandates (Fable-5, Loop System, Read-Full-Request, Active-Checklist, Project-Init)
§ [FACTS] — durable facts about user, environment, tools
- Name: Tuấn Anh (tuananh4865), Vietnamese TikTok content creator
- Primary platform: TikTok Shop Vietnam + Shopee Affiliate
- Telegram bot: Hermes gateway, getFile API limit ≤20MB (verified 2026-06-24)
§ [SESSIONS] — session history summaries
§ [GROWTH_LOG] — how user/agent improved
```

### Step 3: Sync across profiles

```bash
# Repeat template write for all profile USER.md files
for profile in coder content-director research-lead qa-agent engineering-lead operations-manager; do
  if [ -f ~/.hermes/profiles/$profile/memories/USER.md ]; then
    cp ~/.hermes/memories/USER.md ~/.hermes/profiles/$profile/memories/USER.md
  fi
done
```

### Step 4: Verify

```bash
wc -c ~/.hermes/memories/USER.md
# Should be < 1500 bytes (canonical template = ~1100 bytes)
# If > 1500 → check for new corruption → repeat cleanup
```

## Root cause analysis (2026-05-21 and 2026-06-24 incidents)

**Trigger pattern:** The cron job prompt says:
> "Review the conversation above and update memory if appropriate."

When the LLM agent receives this, it interprets "memory" as the memory tool (`memory(action='add', content=...)`). It then extracts fragments from its OWN reasoning buffer (which contains `[tool]`, `[file]`, `[preference]` style scratchpad) and writes them verbatim.

**Why fragments leak:** The agent's internal reasoning has a "scratchpad" format that mirrors what would be useful to remember. When asked to "update memory", it copies the scratchpad thinking output rather than parsing the actual conversation. The result is meta-data about thinking, not facts from the conversation.

**Long-term fix (not done):** Either:
1. Rewrite cron job prompt to require structured output (JSON with clean fact strings only)
2. Add a memory-tool wrapper that validates content before writing
3. Replace raw LLM with a deterministic parser (regex extraction of `[preference] X` markers that match the schema)

## Prevention rules

When writing to USER.md:
- Each fact must be a complete sentence or self-contained clause
- No fragment that needs surrounding context
- No metadata tag prefixes (no `[tool]`, no `[HIGH]`, no `2026-MM-DD:`)
- Cap at 5 entries per section
- If file > 1500 bytes → cleanup before write

## Related

- `../hermes-agent-decision-guard/` — when to ask user vs decide
- `../wiki-maintenance/` — wiki cleanup patterns
- Parent SKILL.md: `../SKILL.md` — section "🔴 CRITICAL PITFALL — USER.md CORRUPTION"
