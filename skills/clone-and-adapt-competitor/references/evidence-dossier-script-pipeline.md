# Evidence Dossier → Script Pipeline (YouTube Edutainment Clone)

Reference for the workflow used to clone a YouTube edutainment channel's CONTENT STYLE (script structure, voice-over cadence, retention techniques) onto a new topic. Distinct from upstream `youtube-channel-audit` (visual/branding analysis) and from `clone-and-adapt-competitor` business-mode clones.

**Verified session:** 2026-07-29, @VuiVe astronomy pilot "Tất Cả Những Điều Kỳ Lạ Về Hố Đen Trong 20 Phút" (18–22 min). Saved under `wiki/projects/vuive-channel-research/`.

## When this reference applies

Trigger when ALL of these hold:
- Project = clone CONTENT formula (not brand/visual/mascot) of a specific YouTube creator.
- Topic is FACTS or EDUTAINMENT (science, history, psychology), not product review.
- User wants a pilot SCRIPT, not just a research report.

If user wants `clone business model` or `clone visual/brand`, load `clone-and-adapt-competitor` SKILL.md directly (Pitfall #9 separate-project-folder rule still applies).

## 5-phase pipeline

### Phase 1 — Inherit from prior channel audit

The Vui Vẻ research project already produced two reports:
- `wiki/concepts/youtube-channel-vuive-content-script-analysis-2026-07-11.md` (5-PART script, 4-PHASE segment, retention)
- `wiki/projects/vuive-channel-research/REPORT-CHUYEN-SAU-2026-07-24.md` (title formula, content direction, voice-over)

Read these BEFORE writing. They contain the formula to apply.

### Phase 2 — Scope the pilot

Ask for / decide ONE pilot topic. Document in evidence dossier §0:
- Duration target (18–22 min sweet spot, per Vui Vẻ formula).
- Chapter count (8–12 is the working range for long-form).
- Forbidden claims list (things NOT to say even if templating says to).

### Phase 3 — Evidence dossier FIRST (most important)

Before writing any script, build a dossier with these sections:

| Section | Required | Notes |
|---|---|---|
| 0. Scope | yes | duration, chapter count, tonal constraints |
| 1. Foundational claims | yes | each with Confidence HIGH/MEDIUM/LOW + source URL |
| 2. Sub-topic taxonomy | yes | chapter-by-chapter claim budget |
| 3–9. Per-phenomenon evidence | yes | numerical facts in their own tables |
| 10. Chapter map | yes | chapter → question → evidence → confidence |
| 11. Forbidden claim list | REQUIRED | claims the script MUST avoid; prevents LLM hallucinating myths |
| 12. Source URLs | yes | numbered [1]–[N] for in-script citation |
| 13. Status block | yes | "evidence collection: complete, script: not yet written" |

Rule: never cite a number higher than the dossier's confidence level. Use "có thể" / "nhiều khả năng" wording for MEDIUM claims. Skip a chapter outright if evidence is LOW-only.

Save to: `wiki/projects/<project>/research/<topic>-evidence-dossier-YYYY-MM-DD.md`

### Phase 4 — Script with citations

Each chapter ends with [N] citations matching dossier §12. Script includes a `## OUTRO` block + `## NGUỒN` block reprinting all URLs + `## CLAIM AUDIT` block (forbidden-claim checklist with rationale).

Do NOT copy wording from source video transcript. Re-derive the cadence (4-PHASE per segment), not the prose. Pitfall #21 of `youtube-channel-audit` (mascot/avatar analysis first) still applies for any visual assets.

Save to: `wiki/projects/<project>/scripts/pilot-NN-<slug>-v1.md`

### Phase 5 — Verify before declaring done

Three verification layers (run ALL):

1. **Structural QA (local):** script file exists, non-empty, exactly N chapters, ≥N in-script citations, has Hook + Outro + Sources + Claim Audit sections.
2. **Forbidden-claim scan:** literal grep against dossier §11 forbidden list. Must return 0 hits.
3. **Independent verifier subagent (background):** dispatch a leaf subagent with the dossier + script paths and ask for STRUCTURAL / SEMANTIC / FUNCTIONAL audit + VERDICT PASS/FAIL/PARTIAL_PASS. Spec them to look for: numbers not in dossier, hedging words missing on MEDIUM claims, mythological phrasings masquerading as fact.

If verifier returns FAIL on any layer: fix the specific issues they flagged, re-run only that layer, then ship.

## Lessons encoded from 2026-07-29 session

1. **Evidence dossier before script, every time.** Without dossier, LLM drifts into generic space-listicle tone and pulls uncertain claims from general "knowledge". With dossier + claim-audit, the LLM has firm rails.

2. **Forbidden-claim section is non-negotiable.** Document was the most-clicked section during writing. Examples that worked:
   - "Hố đen hút mọi thứ" (popular myth)
   - "Chân trời sự kiện là bề mặt rắn" (factual confusion)
   - "Ảnh M87* là ảnh bên trong" (semantic slip)
   - "Hố đen nguyên thủy đã được tìm thấy" (overclaim)
   - "Điểm kỳ dị chắc chắn có mật độ vô hạn" (overclaim)

3. **Independent verifier caught what self-check missed.** Local structural QA confirmed 10 chapters + 33 citations. The background subagent had the deeper job: did the WORDS actually say what the dossier said, or had the script drifted into colloquial overclaim?

4. **Citation hygiene:** keep all source URLs in dossier §12 numbered, then re-use the same [N] in the script. Don't paste URLs inline in the script body — keep them in the trailing source block for read-aloud flow.

5. **Duration budget must match cadence:** 10 chapters × 2 min each = 20 min sweet spot. If Vui Vẻ sweet spot was 18–23 min, pilot target should match, not stretch to "more thorough".

## Related files

- `wiki/projects/vuive-channel-research/research/black-holes-evidence-dossier-2026-07-29.md` — pilot dossier
- `wiki/projects/vuive-channel-research/scripts/pilot-01-tat-ca-dieu-ky-la-ve-ho-den-20-phut-v1.md` — pilot script
- `wiki/concepts/youtube-channel-vuive-content-script-analysis-2026-07-11.md` — upstream formula
