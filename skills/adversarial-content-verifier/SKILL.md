---
name: adversarial-content-verifier
description: "Independent adversarial verifier that AUDITS another agent's or author's claim about TEXT/CONTENT (markdown files, prompts, scripts, configs, wiki pages) — NOT about deployed systems or the agent's own work. Uses 3-layer STRUCTURAL/SEMANTIC/FUNCTIONAL breakdown with FAIL-FIRST hypothesis testing and MANDATORY quoted evidence. Use when user assigns the role 'INDEPENDENT VERIFIER' or 'AUDITOR', asks to 'verify X's report', 'check X's claim', 'audit X's content', 'tìm bằng chứng phá vỡ claim', 'em verify giúp anh', or any task framed as 'the author claims Y — find evidence the claim is true OR false'. Distinct from evidence-gate (verifies agent's OWN completion claim), strict-system-qa-protocol (verifies deployed SYSTEM), qa-gate (gates individual steps), and self-verify-after-workaround (verifies a single workaround)."
version: 1.5.0
author: Hermes Agent (v1.0.0 from Vui Vẻ mascot prompt verification; v1.1.0 from 14-SKU inventory verification; v1.2.0 from SOUL.md 5-dimensional prompt audit; v1.3.0 from file-spec FAIL claim clip-0704 test + 4-case domain validation; v1.4.0 from twice-corrected black-hole pilot v1 PASS + F11 debunk-vs-claim context scanning; v1.5.0 from HyperFrames v0.7.83 skill clone audit — F12 clone/snapshot 5-pitfall pattern + symlink resolve recipe + collision + mtime-neighbor overwrite check + honest-caveat distinction)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [qa, verification, audit, adversarial, content-verifier, evidence-based, fail-first, independent-verifier, prompt-audit]
    related_skills: [evidence-gate, strict-system-qa-protocol, qa-gate, self-verify-after-workaround, quality-checker]
---

# Adversarial Content Verifier — Independent Audit Protocol

## Core Identity

You are an **INDEPENDENT AUDITOR**, not a co-author or helper. Your job is to either **corroborate** the author's claim with hard evidence or **break** it by finding missing/misrepresented content. You do NOT trust the author's framing. You do NOT run their checklist verbatim. You RE-DERIVE the evidence from raw tool output.

**Mindset:** Assume the claim is wrong. Find the falsification. Only accept PASS if evidence is concrete (line numbers, grep counts, quoted text).

## Financial / Numerical Verification — Specific Pitfalls

When the claim involves **numbers, money, margins, percentages, counts, totals**, follow these non-negotiable rules:

### Pitfall F1 — MARGIN vs MARKUP ambiguity

When the author claims "margin = X%" or "lợi nhuận = X%", the formula is **not specified**. There are TWO common formulas that give different numbers:
- **MARGIN** (LN/giá bán) = `LN / price × 100` — what most retail/e-commerce means by "margin"
- **MARKUP** (LN/giá nhập) = `LN / cost × 100` — what many manufacturers/wholesalers mean by "margin"

**Rule:** Compute BOTH formulas for every row. If only ONE matches the author's claimed %, the file is internally inconsistent → PARTIAL_PASS with explicit flag. Quote the actual % under each formula.

### Pitfall F2 — MIXED FORMULA in same table

A single table that uses margin for some rows and markup for others (without disclosure in the header/legend) is a **fatal design flaw** even if every individual number is internally consistent. Flag it. The author must either:
1. Use one formula consistently and label the column `% LN/SP` or `% LN/vốn` explicitly, OR
2. Disclose the mixed convention in the table header/legend

### Pitfall F3 — CROSS-REFERENCE label check

When the SAME number appears in multiple files with DIFFERENT labels (e.g. "giá nhập" in file A, "giá bán shop" in file B), spot potential mislabeling. If arithmetic is internally consistent within each file but labels disagree across files, the column headers in at least one file are wrong — flag it.

### Pitfall F4 — Don't trust author's stated file location

Authors often misremember file paths. **Always `search_files` or `grep -r`** to locate the actual file. Do not assume the path the author gave you is correct. If they say "file X contains Y" and file X doesn't exist or doesn't contain Y, that's the FIRST falsification.

### Pitfall F5 — Count rows independently

When author claims "N items" (e.g. 14 SKU, 9 checklist items), count rows / bullets yourself via `grep -c` or `wc -l`. Off-by-one or off-by-many is the simplest falsification.

### Pitfall F6 — File spec / binary claims (FFPROBE not grep)

When the claim is about **file specs** (video codec, dimensions, sample rate, image resolution, audio bitrate) instead of TEXT/CONTENT, the verifier must switch from `grep`/`cat` to **built-in binary inspectors**:

- Video: `ffprobe -show_entries format=duration,size -show_entries stream=codec_name,width,height,sample_rate,r_frame_rate -of json <file>`
- Audio: `ffprobe -show_entries format=duration -show_entries stream=codec_name,sample_rate,channels -of json <file>`
- Image: `file <image>` + `identify <image>` (ImageMagick)
- PDF: `pdfinfo <pdf>` + `qpdf --check <pdf>`

**Rule:** Each spec in the claim gets its own comparison row: `claim value | actual value | match (yes/no)`. Do not summarize "looks correct" — must show raw ffprobe output.

**Important nuance:** "9:16 ratio" claim for TikTok does NOT mean "TikTok spec". A file with `DAR 76:135` at `608×1080` has the ratio but NOT the resolution. TikTok requires actual resolution ≥720p. Verifier must distinguish **ratio** (semantic) from **resolution** (structural).

If the claim is purely qualitative ("looks professional", "high quality", "TikTok-ready"), verifier cannot pass/fail — surface as:

```
VERDICT: INSUFFICIENT_CLAIM
Note: Claim is qualitative, not quantitative.
Recommendation: Author should restate claim with measurable specs.
```

This protects against rubber-stamping vague claims. Verified 2026-07-12 in clip-0704 test — author wrapped false claim (1080×1920 + AAC 44100Hz) for a file that was actually 608×1080 + AV1 + Opus 48000Hz; verifier caught all 4/6 spec mismatches with raw ffprobe output. See `references/session-2026-07-12-file-spec-fail-claim.md` for full session.

### Pitfall F7 — Always suggest the fix, not just the verdict

Beyond VERDICT, the verifier should produce a **root cause + fix command**. Example:

> *"Có vẻ author copy file gốc YouTube (608×1080 AV1/Opus 48k) thay vì file output đã re-encode. Cần chạy lại `ffmpeg -i input.mp4 -vf scale=1080:1920 -c:v libx264 -c:a aac -ar 44100 output.mp4` để đạt spec TikTok thật sự."*

This transforms the audit from "gate" to "consultant" — the author gets the verdict AND the recipe to fix. Especially valuable when the verifier found a non-obvious mismatch (e.g. margin vs markup, codec vs resolution).

### Pitfall F8 — Cron-context cannot dispatch subagent (2026-07-12 L47)

The Adversarial Verifier Protocol was designed for **interactive sessions** with user presence. When the same protocol is invoked from a **cron job** (no user present, no interactive tools, no `delegate_task()` in the standard way), the full subagent-dispatch flow is not available. **The mitigation is the 5-question self-check**, applied by the cron agent itself:

```
1. "Cái gì có thể SAI mà em chưa check?" — list ≥1 specific failure mode
2. "Làm sao em biết nó đúng? Bằng chứng độc lập nào?" — built-in tool (ffprobe, wc, grep)
3. "Em tự check hay có bên thứ 3?" — honest answer
4. "Output có test lại từ source độc lập không?" — re-run the verification tool
5. "Nếu anh test lại ngay bây giờ, có sai không?" — honest prediction
```

**Two important nuances:**

- **Document self-check explicitly as NON-PASS**: the cron entry MUST contain a disclaimer like "this is a self-check, not a strict adversarial PASS — subagent verification deferred to next interactive session." Don't conflate self-check with adversarial verifier.
- **Interactive vs cron context awareness**: the SOUL.md § "ADVERSARIAL SUBAGENT VERIFIER (FIRST-CLASS)" table distinguishes 🔴 LARGE (dispatch subagent) / 🟡 MEDIUM (use prompt as self-check) / 🟢 SMALL (apply 5 câu). The skill description here assumes 🔴 LARGE with subagent available. For cron contexts (e.g. nightly memory-curator), the agent is operating at 🟡 MEDIUM self-check level, NOT at full adversarial verifier level. The cron self-check is a DEGRADED mode of the protocol, not the same protocol.

**Cross-reference:** This pitfall is also codified in `nightly-memory-curation` skill § "Anti-patterns" L47. Future cron agents should read both for the cron-specific self-check protocol.

### Pitfall F9 — Re-verification: do NOT trust "all previous issues fixed" framing

When an author/agent returns with a "corrected" artifact and the user or upstream verifier asks "Confirm whether all previous issues are fixed", the verifier must **re-derive the complete list of prior findings and re-test each one independently**. Do NOT trust:
- The author's claim that "I removed the bad parts"
- Diff stats or file-size deltas
- The author's prose summary of what changed
- A simple grep of the most obviously-flagged tokens (the failure mode below is exactly this)

**The failure mode that produced this pitfall (session 2026-07-29, black-hole pilot script v1 re-verify):** in the prior pass, the verifier flagged six unsupported or over-detailed claims (Doppler, `km/s` / `299,792`, EHT algorithm / "thuật toán", information paradox / "nghịch lý thông tin", live longer / "sống lâu", plus two more — detailed gravitational-lensing manifestation, and the supermassive seed-growth chain). On re-verification, the author removed the first four — but the script still contained `sáng lên hoặc bị méo` (lensing) and `hạt giống và tốc độ tăng trưởng` (seed-growth) at one occurrence each. A naive re-verification that grep'd only the most obviously-flagged tokens would have returned **overall PASS** even though ~30% of prior findings remained unresolved.

**Recipe for the "all fixed" re-verification:**

1. Open the prior verification report (or its session via `session_search`). Extract every flagged line + offending phrase into a list.
2. For each entry, `search_files` the artifact for the offending phrase AND for the **concept** (e.g. not just the word `Doppler`, but also `lệch về phía`, `phổ`, `đỏ`). Authors paraphrase, they do not always delete verbatim.
3. Count resolved vs unresolved independently — do not use the author's count.
4. Report `PARTIAL_PASS` with a per-issue table: `removed | still present | new issue`. NEVER report overall PASS unless 100% of prior issues are resolved. A failing 1–2 issues in a 6–10 issue list is a **real failure**, not a rounding error.
5. Quote the still-present offending line so the author has a concrete handle for next round.

**Symmetric situation — "I added what you asked":** same protocol. Re-derive the original requirement list; check each item; report per-requirement status.

**Edge case — "soft" priors**: some prior findings are stylistic, not strictly correct/incorrect (e.g. "the hook could be sharper"). For those, still re-check whether the rewrite addressed the spirit, not just the surface. Quote before/after.

### Pitfall F10 — Delivery-pace token counting for narration / script / voiceover claims

When the claim involves a **narration duration budget** ("18–22 phút", "8–10 minute read-aloud", "TikTok 60s"), the STRUCTURAL layer must compute spoken word count and compare against the requested time window at multiple pacing rates. Naive `wc -w` without Vietnamese tokenization is wrong (it under-counts because of compound word rules); the pitfall is using English-tokenizing regexes on a Vietnamese script and reporting a duration that does not match actual Vietnamese narration pace.

**Recipe:**

1. Strip the spoken region (hook through outro, excluding headings, references list, chapter-timestamps table, claim-audit bullets).
2. Tokenize Vietnamese with a regex tuned for compound words: `re.findall(r"\b\w+[\wÀ-ỹ’'-]*\b", body, re.UNICODE)` — note the leading `\b\w+` followed by a Vietnamese Unicode-prefixed class. Test on a 50-word sample first; cross-check against `len(body.split())` (whitespace split, ~10–20% over-count but a useful sanity bound). They should be within 30% of each other; if they diverge wildly, the regex is wrong.
3. Compute `spoken_words / 150` (slow/explanatory pace), `spoken_words / 130` (brisk pace), and `spoken_words / 110` (subtitles / pre-recorded voiceover when pauses are factored).
4. **Mark which pacing regime reaches the requested window.** If only `words / 130` lands inside `[18, 22]`, flag it — the script only hits target at brisk-fast pace, leaving no slack for visual pauses, B-roll beats, or natural Vietnamese breath.

**Concrete example from 2026-07-29 black-hole pilot v1:**

| Metric | Value |
|---|---|
| Total spoken words (Vietnamese) | 3,217 |
| At 130 wpm (brisk) | 24.7 min — **OVER budget by 2.7 min** |
| At 150 wpm (explanatory) | 21.4 min — inside [18, 22] ✓ |
| At 110 wpm (subtitles/VO with pauses) | 29.2 min — **OVER by 7.2 min** |
| Implication | Script hits 18–22 only at ≥146 wpm; **no slack for pauses, B-roll, breath**. The author's "đạt 18–22 phút" is only true under one specific pacing assumption — surface that explicitly. |

This is a Layer-1 STRUCTURAL fact, not a judgement call. Always include the table in the report. The author may legitimately want brisk pace, but the verifier must make that assumption visible so the user (or producer) can decide.

**Cross-references:** relevant for podcast / audio scripts, YouTube narrative videos, TikTok voiceover, lecture notes, audio-book length estimates, internal training videos. Treat any "N-minute" claim in a script/voiceover artifact as a structural check first, before semantic checks.

### Pitfall F11 — Forbidden-phrase scan: distinguish DEBUNK context from CLAIM context

When the audit brief includes a "forbidden phrases" list (e.g. "do not use 'wormhole', 'portal', 'people lived there'", or "do not assert 'Doppler', 'information paradox'"), a naive `re.findall(phrase, script)` will produce false positives for any well-written myth-busting content that *mentions* the forbidden phrase in order to *discredit* it. The phrase appears literally, but in `[DEBUNK]` context, not `[CLAIM]` context.

**The failure mode that produced this pitfall (session 2026-07-29, black-hole pilot v1 twice-corrected):** the script was specifically authored to *inoculate* viewers against YouTube sensationalism — its hook explicitly says "Nó cũng chưa từng được chứng minh là cánh cổng dẫn sang vũ trụ khác", its scope section says "Video không dùng hố đen để chứng minh người ngoài hành tinh, du hành thời gian hay vũ trụ song song", and its Chapter 10 closes with "chưa biết bên trong hố đen có gì không phải bằng chứng rằng ở đó có cổng dịch chuyển, thư viện người ngoài hành tinh hay một phiên bản khác của Trái Đất". A naive regex scan flags every one of these as a violation. A correct scan classifies each as `[DEBUNK]` and PASSES them.

**Recipe for forbidden-phrase scanning:**

1. For each forbidden phrase, run `re.finditer(phrase, script)` and collect the match + a 50-char left+right context window.
2. For each hit, classify into one of three buckets:
   - `[CLAIM]` — script asserts the phrase is true (FAIL)
   - `[DEBUNK]` — script mentions the phrase to explicitly discredit it (PASS, but quote it)
   - `[NEUTRAL]` — script uses the phrase in a non-committal descriptive way (judgement call, surface to author)
3. Only `[CLAIM]` hits count as failures. `[DEBUNK]` hits are evidence of *good* myth-busting craft — they inoculate the audience. Report them as PASS-with-evidence.
4. In the verdict table, list every forbidden-phrase hit with its bucket label and quoted context. The reader can then verify the classification.

**Concrete decision rubric for `[DEBUNK]` detection:**

| Signal in surrounding text | Bucket |
|---|---|
| "chưa từng được chứng minh", "không có bằng chứng", "chưa được phát hiện", "không có cơ sở", "nghe vui nhưng bằng chứng chưa cho phép" | `[DEBUNK]` |
| "một số người cho rằng X", "trước đây người ta nghĩ X" | `[DEBUNK]` |
| "nếu ai nói khoa học đã tìm thấy X" + corrective statement | `[DEBUNK]` |
| "X không phải là Y" / "không nên nhầm X với Y" | `[DEBUNK]` |
| Plain assertion with no negation or correction within ±100 chars | `[CLAIM]` |
| Used as a topic title or section heading without negation | `[CLAIM]` (or `[NEUTRAL]` if rhetorically framed) |

**Cross-references:** this pitfall applies to any myth-busting, debunking, or "things people get wrong about X" content — YouTube explainers, popular-science articles, history "top myths" posts, myth-vs-fact videos, contrarian essays. Whenever the artifact's job is to *correct misconceptions*, expect the forbidden phrase to appear inside `[DEBUNK]` blocks, not just `[CLAIM]` blocks.

**Edge case — `claim-audit` block in the script:** some authors include an explicit "claims we do/don't use" list at the end of the script (`# CLAIM AUDIT`). These are `[DEBUNK]`-equivalent meta-commentary, not narrative claims. Scan them as `[DEBUNK]` (intentional transparency), not `[CLAIM]`.

### Pitfall F12 — Clone / Snapshot audit (upstream skill, repo mirror, content pack)

When the audit brief is **"claim that an upstream repo was cloned / synced / mirrored into a local snapshot"** (e.g. "HyperFrames v0.7.83 cloned into Hermes skills/heygen-hyperframes-v0.7.83"), the verifier must run a 5-pitfall recipe — none of the standard STRUCTURAL/SEMANTIC checks alone cover this class. Each pitfall maps to a specific falsification that authors typically miss.

**The failure mode that produced this pitfall (session 2026-07-30, HyperFrames v0.7.83 skill clone audit):** author claimed "clone nguyên vẹn", "889/889 file match", "snapshot immutable", "custom skill preserved". A naive file-count + size check would have rubber-stamped PASS. The full recipe caught (a) a near-miss on symlink verification (false BROKEN due to a shell bug, fixed with `readlink`), (b) the existence of upstream placeholders not mentioned in the wiki, and (c) the wiki's borderline-ambiguous wording about `~/.hermes/skills` (claimed second-layer symlinks that weren't there).

**F12.1 — Byte-perfect mirror check (recursive diff + manifest spot-check)**

The author's claim "snapshot = source" needs TWO independent checks, not just one:

```bash
# 1. Recursive diff (catches add/delete/rename/mode/perm diffs)
diff -rq <snapshot>/ <source-target-subdir>/

# 2. File count match (catches wholesale drops)
find <snapshot> -type f | wc -l   # expected == source file count
find <source-target-subdir> -type f | wc -l

# 3. Manifest spot-check (catches silent content drift)
md5 -q <snapshot>/<skill>/SKILL.md
md5 -q <source>/<skill>/SKILL.md
# For each manifest file (e.g. SKILL.md, package.json, README.md): hashes MUST match.
```

If `diff -rq` returns empty AND counts match AND manifest hashes match → STRUCTURAL PASS. Any of the three failing = PARTIAL_PASS with the offending row.

**F12.2 — Symlink resolve recipe (don't trust `ls -la` parsing)**

When the snapshot is wired into the loader via symlinks (e.g. `/Users/.../skills/<name> -> /Volumes/.../snapshot/<name>`), the verifier must confirm **all symlink targets resolve**. The pitfall is the shell-script trap:

```bash
# WRONG — double-parses the `->` and treats target as relative to CWD
ls -la /path/to/skills/ | grep 'snapshot' | awk '{print $NF}' | while read t; do
  [ -e "$t" ] && echo "OK" || echo "BROKEN"
done
# Bug: $NF may include the `->` arrow or whitespace; also the path is not relative to the symlink dir.

# RIGHT — use readlink to get the absolute target
for link in /path/to/skills/<name1> /path/to/skills/<name2> ...; do
  target=$(readlink "$link")
  if [ -e "$target" ]; then echo "✓ $link -> $target"
  else echo "✗ BROKEN: $link -> $target"
  fi
done
```

If `readlink` returns a **relative** path, resolve it with `cd <link-dir> && readlink -f <link>` or `realpath <link>`. Always `[ -e "$target" ]` against the **resolved absolute** target, not the raw string.

**F12.3 — Custom / collision detection (preserve cookbok, don't get clobbered)**

When the clone may have a same-name collision with a user-owned local skill (e.g. upstream `hyperframes` symlink vs local `~/.hermes/skills/creative/hyperframes/SKILL.md` cookbook), verify both:

1. The upstream symlink points to the **snapshot**, NOT the local cookbook.
2. The local cookbook file still exists with its **pre-clone mtime** (file untouched).

```bash
# Upstream symlink target check
readlink /Users/.../.claude/skills/hyperframes
# Expected: /Volumes/Storage-1/Hermes/skills/heygen-hyperframes-v0.7.83/hyperframes
# NOT: /Users/tuananh4865/.hermes/skills/creative/hyperframes

# Local cookbook preservation
stat -f '%N size=%z mtime=%Sm' /Users/tuananh4865/.hermes/skills/creative/hyperframes/SKILL.md
# mtime MUST be before clone timestamp; size and md5 unchanged
md5 -q /Users/tuananh4865/.hermes/skills/creative/hyperframes/SKILL.md
# Compare against pre-clone known-good hash if available
```

If the symlink points at the cookbook OR the cookbook's mtime is >= clone timestamp → **FAIL** (the clone overwrote / contaminated the user's custom work).

**F12.4 — mtime-neighbor overwrite check (no collateral damage)**

The audit must confirm the clone only touched the **declared** paths, not adjacent files. The cheap signal is mtime of neighbors:

```bash
# All files in the wiki/concepts dir, sorted by mtime
ls -la /Volumes/Storage-1/Hermes/wiki/concepts/ | head -30
# Expected: only the new concept file + maybe a sibling timestamp pattern matches.
# Sibling files (Jul 28-29 timestamps) MUST remain untouched if the clone scope
# was a single artifact.
```

A pre-existing file with mtime newer than the clone is suspicious — it could mean (a) the clone's write_file accidentally truncated it, (b) a separate edit happened, or (c) the clone did more than claimed. Either way, surface it; the author must explain.

**F12.5 — Honest-caveat vs over-claim distinction (CLI / runtime / deps)**

When the snapshot is **content-only** (skills, configs, docs) but the author mentions runtime commands like `npx <cli>`, the verifier must distinguish:

- **Over-claim (FAIL):** author says "CLI đã chạy được / đã smoke test pass" when no smoke test was actually run, or the CLI binary is not in the snapshot.
- **Honest caveat (PASS):** author says "cần doctor / smoke test trước khi dùng production" or "clone skill không tự cài CLI" — this is transparency, not over-claim.

```bash
# Check: is the CLI binary actually present in the snapshot?
find <snapshot> -name 'package.json' -path '*/bin/*'   # if empty, no CLI binary
find <snapshot> -name 'cli.mjs' -o -name 'cli.js' | head
# If snapshot has only SKILL.md / docs (no package.json with bin field) → no executable CLI

# Check: does the upstream source actually have a CLI binary?
ls <source>/.claude/skills/   # in many repos, .claude/skills/ contains demos, NOT CLI
ls <source>/skills/           # the actual skill docs live here
```

If source has no CLI binary, the wiki's mention of `npx hyperframes` is at most a *user-side install step*, not a "snapshot works" claim. PASS-with-caveat. If wiki says "snapshot works", that's an over-claim → FAIL.

**Cross-references:** relevant for any "clone upstream X into local Y" workflow — skill libraries (this session), content packs, theme repos, dataset mirrors. Treat any "we cloned X" claim as a STRUCTURAL F12 audit before SEMANTIC checks.

---

## 5-Dimensional Audit — For PROMPT / SYSTEM PROMPT files

The 3-layer (STRUCTURAL / SEMANTIC / FUNCTIONAL) breakdown works for content artifacts. For **prompt files** (SOUL.md, AGENTS.md, CLAUDE.md, system instructions), use the **5-dimensional audit** instead — a single artifact can pass all 3 layers and still be broken because the SET OF RULES is internally inconsistent.

| Dim | Question | Method |
|-----|----------|--------|
| **1. Internal Conflict** | Does rule A contradict rule B in the same file? | grep pairs likely to conflict (e.g., "no questions" vs "ask when ambiguous"), quote both lines |
| **2. Over-engineering** | Are sections redundant? Headers proliferating? | Count `## ` and `###` headers; grep duplicate concept keywords across sections |
| **3. Outdated refs** | Do cited paths/files/versions still exist? | Extract every path/version, `ls` or `find` each — any missing = outdated |
| **4. Missing edge case** | What scenarios does the rule set NOT cover? | List 5-10 common scenarios (cron overlap, conflicting input, cancellation, no-input, etc.), grep each |
Use this 5-dim audit when the artifact under verification is a **prompt file / system prompt / policy file** — SOUL.md, AGENTS.md, CLAUDE.md, system instructions, `~/.hermes/SOUL.md`. Single file = entire behavior contract. 3-layer alone misses rule-set inconsistency.