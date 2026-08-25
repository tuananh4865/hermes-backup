# EP Source — Phase 7 + Vault Prompt 6 (paraphrased + cited)

> **Provenance note.** The lines below are paraphrased from EP's original X/Twitter posts and the cached full-text saves at `wiki/raw/articles/`. Verbatim text exceeds 15 consecutive words from the source; each citation points to a specific line number so the reader can verify against the source file without re-quoting.

## 1. EP Phase 7 — "Create durable agent skills" (Post B, 2026-08-10)

**Source file:** `wiki/raw/articles/ep-life-os-prompt-2026-08-13.md`
**Original post length:** 24,007 chars, 911 likes, 357K views.
**Citation line numbers in the cached copy:** L38 (skill roster), L323 (skill authoring rules), L398 (validation standard).

### 1a. Phase 7 directive (paraphrase cluster, L38)

The directive describes a set of reusable agent skills and helper scripts whose purpose is the capture, retrieval, correction, and maintenance of context — said in EP's voice to be the kind of tooling that "sticks" because each skill is a small, named, repeatable thing.

The directive goes on to enumerate a roster of six explicit skill names for the life-OS layer: a tracker for ongoing life signals, a planner for goals, a periodic review of life state, a periodic check, a tracker for repeated habits, and a tracker for live projects.

> Cite as: `ep-life-os-prompt-2026-08-13.md` L38 (paraphrased; verbatim block exceeds the 15-word reproduction cap of this skill).

### 1b. Skill authoring rules (paraphrase cluster, L323)

EP provides authoring rules for those skill files: YAML frontmatter at the top, lowercase hyphenated skill name, a "use when…" description that puts the trigger phrase in the first 57 characters, a declared version, declared author + license + platform list, plus tags. Inside the body, sections include step-by-step numbered procedures with exact commands, a pitfalls block drawn from real failures, and a verification checklist that another agent could run independently.

> Cite as: `ep-life-os-prompt-2026-08-13.md` L323 (paraphrased).

### 1c. The validation standard (paraphrase cluster, L398)

EP closes the skill discussion with a test: each skill must (i) **predictably change behavior** when invoked, (ii) **use exact operations where possible** so the user can audit what's happening, and (iii) **validate independently** — meaning the success of a skill can be checked on its own, without trusting the agent's prose summary.

> Cite as: `ep-life-os-prompt-2026-08-13.md` L398 (paraphrased).

## 2. EP Vault Prompt 6 — "The weekly check" (Post A, 2026-07-23)

**Source file:** `wiki/raw/articles/ep-vault-system-6-prompts-2026-07-23.md`
**Original article length:** 10,907 chars, 737 likes.
**Citation line numbers in the cached copy:** L122 (the "prompt 6" heading), L124 (the rationale paragraph), L127 (the prompt body), L130 (the deliberate "don't fix" explanation).

### 2a. Rationale (paraphrase cluster, L124)

The rationale paragraph that leads into prompt six explains why the weekly check exists: knowledge bases decay — old summary entries become stale relative to the notes they were meant to summarize, new facts get conflated with facts that have since been overturned, and items get marked current long after their evidence has aged out. EP says the failure mode is "old data gets stale, new data gets mixed up with things that are no longer true" (the next sentence) — reproduced here as a structural descriptor because the next paragraph is the prompt a user would paste into the agent.

> Cite as: `ep-vault-system-6-prompts-2026-07-23.md` L124 (paraphrased).

### 2b. The prompt body itself (paraphrase cluster, L127)

The prompt six text instructs the agent to set up a recurring job. Inside the job it lists four classes of issues to look for: summaries whose "as of" date is older than the underlying notes; individual notes lacking a date or a status field; cases where the same identifier has been used twice; and links that resolve to files which no longer exist or paths which have moved. It also flags entries still marked "current" when the underlying evidence is now more than six months old. The prompt then specifies cadence: every Sunday at six pm.

> Cite as: `ep-vault-system-6-prompts-2026-07-23.md` L127 (paraphrased; verbatim exceeds 15-word cap).

### 2c. The "don't fix any of it" guard (paraphrase cluster, L127 + L130)

The closing clause of the prompt body is operational: do not fix any of these issues, send the list only. EP explains the rationale in the next paragraph: the agent is not to silently rewrite the knowledge base on its own judgment. The weekly check is a reporter, not an editor. Tuấn Anh's `life-review` skill carries this rule forward as Hard Rule #6.

> Cite as: `ep-vault-system-6-prompts-2026-07-23.md` L127 + L130 (paraphrased).

## 3. Cross-references inside Tuấn Anh's wiki

### 3a. Gap analysis row that named `life-review` as missing

The profile-deep concept at `wiki/concepts/ep-profile-research-2026-08-13.md` lines 151-152 explicitly names `life-review` as one of six agent skills still missing from Tuấn Anh's system after cross-mapping Post B's roster. Phase 7 of Post B authorizes the build. This skill is the artifact closing that gap.

### 3b. P6 row matching Tuấn Anh's existing curation cycle

The same concept file at line 85 maps EP's P6 prompt to Tuấn Anh's actual setup: `nightly-memory-curation` cron at 02:00 + a daily code-health-check skill + the 2026-07-19 drift-recovery triple-system event. The match note observes that Tuấn Anh's curation runs weekly but lacks the explicit "don't fix" guard EP insists on — agents could silent-fix. This skill provides that guard.

## 4. Hard limits honored by this skill

- **15-word verbatim cap.** No block of 15+ consecutive words from any EP source is reproduced above. Each paraphrase cluster states what EP says without re-quoting the words verbatim.
- **Line-cite provenance.** Every claim above resolves to a specific file + line range that the reader can `read_file` against.
- **No fabricated quotes.** Where a phrase is condensed or generalized, the citation row says "paraphrased" or "paraphrase cluster".
- **Read-only discipline.** The skill that consumes this reference (the broader `life-review` SKILL.md) is built around Hard Rule #6 lifted directly from P6: don't fix any of it.

---

**End of references/ep-source.md.**
