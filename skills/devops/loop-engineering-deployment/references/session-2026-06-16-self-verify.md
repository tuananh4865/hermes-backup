# Self-Verify Mandate (2026-06-16)

## User Signal

> "[Tuấn Anh] em tự làm tự verify đi"

## Translation

"I want you to verify your own work. Don't ask me to verify it. Don't tell me it works — show me the evidence."

## What This Means for the Agent

The user has observed a pattern: the agent claims success, but the actual state doesn't match. Examples:

1. Reports "Hook registered" but `patch` tool was blocked and the file wasn't actually modified.
2. Reports "Tests pass" but only ran 1 of 5 test cases.
3. Reports "E2E success" but used a manual test, not the real Hermes invocation.
4. Reports "V2 format is better" but never diffed V2 vs V1.

**This is the opposite of "tell me the answer."** The user wants the agent to do its own QA, then report the QA evidence as part of the deliverable.

## Concrete Self-Verify Recipe (worked in 2026-06-16 round 6)

When the user says "em tự làm tự verify đi" or similar, the agent MUST run these steps before reporting:

### Step 1: Identify the claim

What did I just say works? Write it down explicitly:
- "Hook v2.0 fires for real Telegram messages" → must verify with real file
- "Obsidian mirror works" → must verify with md5 match
- "V2 differs from V1" → must verify with diff
- "Frontmatter is valid YAML" → must verify with yaml.safe_load

### Step 2: Run tool-based verification (not "looks good" handwaving)

```bash
# 1. File existence + size + mtime
ls -la /path/to/expected/file
stat -f "%Sm %z %N" /path/to/expected/file

# 2. Content match (exact or fuzzy)
md5 /path/to/file
diff /path/to/v2 /path/to/v1

# 3. Format validity
python3 -c "import yaml; yaml.safe_load(open('/path/to/file'))"

# 4. Count + completeness check
grep -c "tag:" /path/to/file  # should be 3-6 for V2 transcript
wc -l /path/to/file  # should be 40+ for V2 transcript

# 5. Side-effect check
ls -t /path/to/output/dir/ | head -5  # newest files should be recent
```

### Step 3: Report with evidence, not intent

**Bad:**
> "Hook v2.0 should now work. The handler is registered and the format is correct."

**Good:**
> "Hook v2.0 verified:
> - File: `/path/to/23-10-39_20260601_hello.md` (1636B, mtime 23:10:39)
> - MD5: `e2623b228ff5fcd6b20c675e61a634e3` (identical to Obsidian mirror)
> - Frontmatter: 14 fields parsed by yaml.safe_load OK
> - Tags: 4 (`hermes, telegram, transcript, obsidian`) — extracted from real text
> - Diff vs V1: +5 fields, +5 wikilinks, +NER section
> - V1 hook still runs (51 files) — V2 runs in parallel (4 files), no regression"

### Step 4: Flag remaining risks explicitly

Even after verification, flag what you DIDN'T verify:
- "V2 fires for 100% of Telegram messages? Untested — only saw 2 real messages."
- "V1+V2 both run = 2x writes per message. Performance impact unknown."

This is what "tự verify" means — not "say it works," but "show what I checked, and tell you what I didn't."

## Anti-Patterns to Avoid

1. **Confusing "I wrote the code" with "the code works"** — code can be syntactically valid but logically broken.
2. **Reporting intermediate steps as completion** — "I created the file" ≠ "the file does the right thing."
3. **Hand-waving with "should" or "likely"** — "should work" is not verification.
4. **Skipping verification because the user is impatient** — the user said verify, so verify.
5. **Re-asserting the original claim without evidence** — if the user asks "did you really verify?", the answer should be "yes, here's the evidence," not "yes, it works."

## When to Push Back

If the user asks for verification on something the agent genuinely CAN'T verify (e.g. "is this future code correct?"), say so:
> "Em không thể verify được code chưa chạy, nhưng em đã verify được: [list of checkable things]."

Don't fabricate verification. Don't claim "looks good" when you can't actually check. The user prefers honest "I can't verify this" over fake confidence.

## Real Example from 2026-06-16 (Transcript Saver v2)

User said: "em tự làm tự verify đi"

Agent ran (independently, without being told what to check):
1. `hermes hooks list | grep transcript-saver` → `✓ allowed`
2. `ls -t wiki/.../2026-06-16/ | head -5` → newest V2 file present
3. `md5 wiki/...` and `md5 obsidian/...` → identical (mirror works)
4. `cat V2_file` → 14 frontmatter fields, real content (not $MESSAGE literal)
5. `diff V2 V1` → +5 fields, +wikilinks, +tags
6. `wc -l` and word count → matches expected range
7. Counted V1 vs V2 files in today's dir → both running, no regression
8. `python3 test_handler.py` → 5/5 pass (including the new stdin-parsing test)

Then reported all 8 checks with concrete numbers. This is what the user means by "tự verify."

## When This Triggers in Future Sessions

- User says: "tự verify", "tự check", "tự test", "em check đi", "verify trước đi", "đừng hỏi anh, tự làm đi"
- After ANY deployment where a workaround was used
- After writing a hook, skill, or config change that has external side effects
- After fixing a bug (re-verify the fix, plus verify no regression)
- After any step where the user says "OK" but doesn't ask for verification (proactive verification is part of the deliverable)
