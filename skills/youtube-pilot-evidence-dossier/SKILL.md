---
name: youtube-pilot-evidence-dossier
description: Evidence dossier before a YouTube pilot script.
title: YouTube Pilot — Evidence Dossier Builder
created: 2026-07-29
updated: 2026-07-29
type: skill
tags: [youtube, research, dossier, pilot, evidence, science, edutainment, vuive]
confidence: high
relationships: [youtube-channel-audit, youtube-content, psychology-viral-master-framework-2026, tiktok-viral-script]
---

# YouTube Pilot — Evidence Dossier Builder

You are building a **fact-checked research dossier** that another session (or you, later) will use as the only source of truth when writing a 18-23 minute edutainment script. Every claim the script will make must already exist in this dossier with a confidence tag, a source URL, and a place in a chapter map. No writing the script here.

## When to load this skill

- User says "nghiên cứu thu thập bằng chứng để viết script", "làm evidence dossier trước", "research kỹ trước khi viết", "build research dossier cho pilot YouTube".
- User has chosen a topic + chapter outline and now wants proof before drafting.
- A previous draft got flagged for a factual error and a re-build from sources is requested.
- Trigger phrases: "nghiên cứu thu thập bằng chứng", "evidence dossier", "research pilot YouTube", "build dossier", "pre-write research", "claim cấm".

**Do NOT use this skill when:**
- The user wants you to write the script now (use `youtube-channel-audit` findings + Vui Vẻ framework from existing wiki instead).
- The user wants a single topic researched but not yet outlined into chapters (too early — go to `youtube-channel-audit` or research workflow).
- The deliverable is short-form TikTok (use `tiktok-viral-script`).

## Output

A single markdown file at `wiki/projects/<project-name>/research/<topic>-evidence-dossier-<YYYY-MM-DD>.md` with frontmatter (`type: query`), ≥2 wikilinks, and these 13 sections in this exact order:

```
0. Phạm vi (scope, target duration, chapter count, exclusion list of myths to refuse)
1. Claim nền tảng đã xác nhận — HIGH-confidence foundational facts (definition, event horizon, "not vacuum cleaner", indirect detection)
2. Sub-categorization (the 4-PHASE-ready content buckets — for black holes: types, accretion disk, formation, tidal forces, detection methods, etc.)
3. Concrete evidence per chapter (numbers, dates, named objects, observations)
4. Open mysteries and unknowns (what's still hypothetical — IMBH, primordial, inside-horizon, etc.)
5. Chapter map with confidence per chapter → directly usable by the script writer
6. Claim cấm (forbidden phrasings) — explicit list of phrases/claims the script must NEVER make
7. Source list with URLs (each must be a real, fetchable page, with access date)
8. Status / next-step pointer (what this dossier is NOT yet — it's not the script)
9. Related wikilinks
```

Estimated length: **2,500-4,500 words.** Tighter than the eventual script writing brief — the dossier is a source map, not prose.

## Workflow (5 phases)

### Phase 1 — Lock scope with the user (3-5 minutes)
Before searching anything, confirm:
- Topic (e.g. "hố đen", "Big Bang", "hệ miễn dịch").
- Approximate chapter count (8-15 typical for 18-23 min).
- Target audience (general Vietnamese = use Vui Vẻ tone; specialist = skip 4-PHASE).
- Tone anchor — usually Vui Vẻ ("Gen Z casual, nguồn + disclaimer + scope-limit + 4-PHASE mỗi segment"), copy from existing wiki project.
- Forbidden territory (e.g. no sci-fi speculation, no "cổng không gian" claims).

Write the answers as Section 0 of the dossier before doing any research.

### Phase 2 — Parallel source pull (bulk, NOT serial)
Use `mcp__exa__web_search_exa` (or equivalent) **in parallel via one multi-tool message**, 5-10 queries that cover:
1. Foundational definition + common myths (the source likely debunks myths itself, which is gold).
2. Type classification (stellar / intermediate / supermassive / primordial analogs).
3. Detection methods + famous observation (EHT M87*, LIGO GW150914, etc.).
4. Formation / lifecycle (supernova, failed supernova, mergers).
5. Open questions and unknowns.
6. Numerical anchors (distances, masses, dates) — one targeted query like "NASA <topic> mass distance official figures".

Batch them in one assistant turn. The Hermes runtime runs them in parallel. **Serial queries waste a turn.**

### Phase 3 — Confidence grade every claim
For each claim that will appear in the script, tag it:

| Confidence | Use when |
|---|---|
| HIGH | Direct NASA/ESA/peer-reviewed source verbatim, retrieved within the session |
| MEDIUM | Sourced but with caveat ("likely", "approximately", or depends on model assumption) |
| LOW | Inference without direct source — must be flagged in dossier, **do not put in script** |

Cross-check against each other. If two sources disagree, surface the disagreement in the chapter row (don't pick a side silently).

### Phase 4 — Build the chapter map
For each of N chapters, write one row:

| Chapter | Question for viewer | Headline evidence | Confidence | Claim cấm relevant? |
|---|---|---|---|---|

This map becomes the table of contents the script writer works from.

### Phase 5 — "Claim cấm" list (non-negotiable section)
List 5-10 specific phrasings the script **must never contain**. Examples from the hố đen dossier:

- ❌ "Hố đen là cái lỗ / máy hút bụi vũ trụ."
- ❌ "Ảnh M87* là ảnh bên trong hố đen."
- ❌ "Hố đen nguyên thủy đã được tìm thấy."
- ❌ "Hố đen là cổng sang vũ trụ khác."
- ❌ "Điểm kỳ dị chắc chắn là một điểm vật lý có mật độ vô hạn."

Formulate as actionable negative claims so the writer can `grep` the draft for forbidden phrases.

## Pitfalls

1. **Don't write the script here.** The dossier is a *source map*. If the user says "bắt đầu viết", stop the dossier and hand back the chapter map asking them to confirm before transitioning to drafting.
2. **Don't cite a source you didn't fetch this session.** Reuse wiki-existing sources only if they were tagged with access date. Otherwise refetch — NASA's article URLs sometimes silently update.
3. **Don't fabricate confidence tags.** If you only have one source and it uses hedging language ("possibly", "may", "may have"), tag MEDIUM, do not upgrade to HIGH because the source is NASA.
4. **Don't confuse primordial/IMBH/supermassive mass ranges.** Each has its own confidently-stated range. If the dossier needs to imply a continuum, it must say so explicitly.
5. **Don't include 3rd-party blogs in the source list.** NASA, ESA, LIGO, Caltech, university press, arXiv — only first-party or peer-reviewed. Forbes/space.com/gizmodo get the title quoted in the dossier but NOT the citation slot.
6. **Don't skip the "open mysteries" section.** The script needs 2-3 curiosity loops for retention. Open questions are the cleanest loops (e.g. "what's inside the event horizon?").
7. **Don't exceed 12 chapters in the map.** Long-form YouTube 18-23 min comfortably fits 8-12 segments. Above 12, segment depth collapses.
8. **Don't ignore the user's already-loaded skills.** If user came from `youtube-channel-audit` or Vui Vẻ framework, link back to those in `relationships` so the next session connects the dossier to the script template.

## Verification before declaring done

- [ ] Dossier file exists at correct wiki path with frontmatter.
- [ ] Sections 0-9 all present and in order.
- [ ] Every claim in chapter map row has a confidence tag.
- [ ] "Claim cấm" list has ≥5 entries.
- [ ] Source list has ≥10 entries (NASA/ESA/LIGO or equivalent first-party), all URLs real (no `example.com`, no `t.co/`).
- [ ] Open mysteries section present (used as curiosity loops).
- [ ] Hub.md / index.md / log.md of the wiki project updated.
- [ ] Dossier cross-references the source Khi bạn load skill này, **DO NOT** start writing the script. Output the dossier, then wait for the user's confirm before transitioning to Phase 2 (script writing, governed by Vui Vẻ framework + `youtube-channel-audit` Style findings).

## Reference (recommended reading order)

- `references/black-holes-2026-07-29-dossier-brief.md` — condensed pattern of a completed dossier (chapter map structure, confidence-grading example, claim cấm template). Read this BEFORE starting Phase 2 to copy the structure.

## Related skills

- `youtube-channel-audit` — provides the Style findings + chapter formatting patterns the eventual script will follow.
- `youtube-content` — for transcript extraction during script polish, not for the dossier itself.
- `psychology-viral-master-framework-2026` — for the 4-PHASE per-segment reasoning the chapter map builds toward.
- `tiktok-viral-script` — for short-form sibling; do NOT mix into YouTube pilot.
