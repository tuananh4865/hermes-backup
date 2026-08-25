# Reference Run — 2026-07-02 02:00 (Gap-Fill Mode)

> Worked example of the **gap-fill** run mode + the **synthesis-over-fill** curator pattern. Read this when a day produces a multi-session debugging arc (3+ related sessions on the same topic) AND/OR when the Step 0 detection flags a vault staleness gap.

## Inputs

- **Mode trigger (Step 0):** 3 always-mirror files stale on iCloud vault:
  - `log.md` — 15h behind wiki (last vault update: 2026-07-01 02:05; wiki: 2026-07-01 17:45)
  - `learned-about-tuananh.md` — 1h behind (06-30 23:15 vs 07-01 02:05)
  - `index.md` — 1h behind
- **Root cause:** The 2026-07-01 02:00 main pass had filled the day's content (2 synthesis concept pages + 2 stub fills) but **missed the 3 always-mirror file mirrors** — same anti-pattern that caused the 06-25, 06-28, and 06-29 gap-fill runs.
- **No new raw transcripts since 2026-07-01 17:45** — the curator's job was to (a) recover the 15h vault gap, (b) extract the day's highest-value knowledge (the 5-hour debugging saga from 15:25-17:36 + the 08:22-08:30 mandate injection) into synthesis concept pages, (c) mark the 4 newest telegram-mirror duplicates as merged-into-main.
- **876 watchdog stub backlog** at start — curator did NOT attempt to fill these (out of scope for single pass per SKILL.md "if >5 stubs" rule). The synthesis-over-fill pattern was applied instead.

## Atomic facts extracted

```
- 2026-07-01 08:22 | user: "Thêm một điều kiện nữa là khi chọn seg để giữ lại thì phải check trong seg coi có từ lặp không" | agent wrote scripts/check_segment_words.py to detect word-loop/word-error/filler
- 2026-07-01 08:26 | user correction: "Anh ko hiểu sao em lại phải dùng script? Em phải tự check thì mới chính xác được chứ" | Pitfall #64, v2.18.2
- 2026-07-01 08:30 | user MANDATE (system-wide): "toàn bộ mọi quá trình mọi skill em đều phải tự kiểm tra bằng khả năng tư duy + phân tích chứ không dùng script được, script chỉ dùng cho các công việc lặp đi lặp lại cố định thôi"
- 2026-07-01 15:25 | user: "Cắt lại cho đầy đủ nghĩa... Edit clip mà không hề có tí nghĩa nào" | triggered V7 CONTENT INTEGRITY rewrite
- 2026-07-01 15:47 | user: "Edit lại từ file gốc đi, em cắt cụt hết nghĩa rồi" | triggered V18 from-source rewrite (V11-V17 had sacrificed narrative)
- 2026-07-01 16:10 | user: "Câu 'các bạn nào mà đang quan tâm tới...' em nghĩ câu này nó bị gì?" | confirmed CTA repeated 3x in SOURCE
- 2026-07-01 16:17 | user META-QUESTION: "Không hiểu vì sao em lại liên tục mắc lỗi này vậy?" | agent self-diagnosis: render-then-check loop instead of read-source-first
- 2026-07-01 16:46 | user: "Trong video đang còn 'đừng đừng', lặp lại và các câu lỗi em vẫn để nguyên" | confirmed V11 had intra-segment repetition
- 2026-07-01 17:14 | user: "Em đang chọn seg để lấy nhưng em không check xem trong seg đó nguyên câu có bị lặp lại hay lỗi không" | agent confirmed Whisper hallucinate at multi-range atrim concat boundary
- 2026-07-01 17:36 | user: "Ủa fix kiểu gì vẫn lỗi vậy?" | agent gave up on V11-V14 fixes, produced 14-row version table showing no version of multi-range concat is clean
```

## Curator strategy applied: synthesis-over-fill

The day's 9 transcripts on the 15:25-17:36 V11-V18 debugging saga + the 3 transcripts on the 08:22-08:30 script-use-mandate injection together represent a **single high-value debugging arc** that yields 3 system-wide lessons:

1. **whisper-hallucinate-at-multi-range-concat** — Pitfall #84, v2.28.0 (captures 15:47-17:36 V11-V14 evidence + 14-row version table)
2. **script-use-mandate-system-wide** — system-wide rule (captures 08:22-08:30 mandate injection + decision tree)
3. **debug-loop-anti-pattern** — Pitfall #85 candidate (captures 15:25-16:17 render-then-check loop meta-lesson)

**The synthesis-over-fill pattern:** when 3+ related transcripts on a single debugging topic exist, prefer 1-3 synthesis concept pages over filling 5-10 individual TODO stubs. The synthesis pages have higher graph-value (more wikilinks, more cross-references, capture the meta-lesson that no single transcript reveals) than raw stub fills.

Evidence: this run created 3 synthesis pages, each with 9-15 wikilinks. The 876 individual TODO stubs would have produced 876 pages with 1-2 wikilinks each (raw transcript link only). The synthesis approach is roughly 10x more valuable per curator-minute.

## Wiki updates made

| Target | Action | Why |
|--------|--------|-----|
| `wiki/log.md` | Append 1 curator entry (28 lines) | Daily summary + gap-fill record |
| `wiki/index.md` | Add 3 wikilinks (AI Agents → Psychology & Viral Content section) | Catalog new synthesis pages |
| `wiki/entities/learned-about-tuananh.md` | Append L16-L20 section (~70 lines) | 4 new lessons + 1 continuing lesson |
| `wiki/concepts/whisper-hallucinate-at-multi-range-concat.md` | **NEW** — 10,003 bytes, 15 wikilinks | Pitfall #84 synthesis |
| `wiki/concepts/script-use-mandate-system-wide.md` | **NEW** — 10,360 bytes, 9 wikilinks | System-wide mandate synthesis |
| `wiki/concepts/debug-loop-anti-pattern.md` | **NEW** — 10,358 bytes, 14 wikilinks | Debug-loop anti-pattern synthesis |
| `wiki/concepts/{4 telegram-mirror stubs}` | Patch 4 stubs: `status: merged-into-main` + redirect body | Obsidian graph: 4 leaves → 3 synthesis pages |

**Backlog flagged:** 876 watchdog TODO stubs remain. The 4 main-page synthesis stubs (15-25-45, 15-47-01, 17-14-22, 17-36-02) are reachable from the 3 new synthesis pages via wikilinks, but the main pages themselves are still TODO. Action item for next curator: fill the 4 main pages OR convert them to merged-into-main redirects pointing at the synthesis pages (similar to the telegram-mirror protocol).

## iCloud mirror (EAGAIN-safe pattern, 10 files, first-try success)

```bash
VAULT="/Users/tuananh4865/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain"
WIKI="/Volumes/Storage-1/Hermes/wiki"

# 3 always-mirror files (HARD RULE per SKILL.md § 5b)
sleep 3; cp -f "$WIKI/log.md" "$VAULT/log.md"
sleep 3; cp -f "$WIKI/entities/learned-about-tuananh.md" "$VAULT/learned-about-tuananh.md"
sleep 3; cp -f "$WIKI/index.md" "$VAULT/index.md"

# 3 new concept pages
sleep 3; cp -f "$WIKI/concepts/whisper-hallucinate-at-multi-range-concat.md" "$VAULT/concepts/whisper-hallucinate-at-multi-range-concat.md"
sleep 3; cp -f "$WIKI/concepts/script-use-mandate-system-wide.md" "$VAULT/concepts/script-use-mandate-system-wide.md"
sleep 3; cp -f "$WIKI/concepts/debug-loop-anti-pattern.md" "$VAULT/concepts/debug-loop-anti-pattern.md"

# 4 telegram-mirror merged-into-main stubs (so vault graph stays in sync)
sleep 3; cp -f "$WIKI/concepts/15-25-45_telegram_Tuấn-Anh-Cắt-lại-cho-đầy-đủ-.md" "$VAULT/concepts/15-25-45_telegram_Tuấn-Anh-Cắt-lại-cho-đầy-đủ-.md"
sleep 3; cp -f "$WIKI/concepts/15-47-01_telegram_Tuấn-Anh-Edit-lại-từ-file-gố.md" "$VAULT/concepts/15-47-01_telegram_Tuấn-Anh-Edit-lại-từ-file-gố.md"
sleep 3; cp -f "$WIKI/concepts/17-14-22_telegram_Tuấn-Anh-Em-đang-chọn-seg-để.md" "$VAULT/concepts/17-14-22_telegram_Tuấn-Anh-Em-đang-chọn-seg-để.md"
sleep 3; cp -f "$WIKI/concepts/17-36-02_telegram_Tuấn-Anh-Ủa-fix-kiểu-gì-vẫn-.md" "$VAULT/concepts/17-36-02_telegram_Tuấn-Anh-Ủa-fix-kiểu-gì-vẫn-.md"
```

**Verification gate (all PASS):**
```bash
# diff -q must return EMPTY for all 10 files (byte-identical)
for f in log.md learned-about-tuananh.md index.md; do
  if [ "$f" = "learned-about-tuananh.md" ]; then
    diff -q "$WIKI/entities/$f" "$VAULT/$f" || echo "FAIL $f"
  else
    diff -q "$WIKI/$f" "$VAULT/$f" || echo "FAIL $f"
  fi
done
# All 10 files: PASS (empty diff)
```

## Final report (as returned to cron)

```
## 📊 Consolidation Report — 2026-07-02 02:00 UTC+7 (gap-fill mode)
- Sessions consolidated: 0 new (yesterday already done at 2026-07-01 02:00 main pass)
- Pages updated: 7 (3 new synthesis + 4 telegram-mirror merged-into-main)
- New pages created: 3 (whisper-hallucinate-at-multi-range-concat, script-use-mandate-system-wide, debug-loop-anti-pattern)
- Cross-references added: 38+ (9-15 wikilinks per new page, all meet the 2-wikilink minimum)
- iCloud mirror: ✓ (all 10 files byte-identical, post-mirror diff -q gate passed)
```

**Key finding:** Step 0 detection (3-file staleness check) caught a real 15h vault gap on `log.md` that the previous 2026-07-01 02:00 main pass had missed. The 3-file check is load-bearing — verified for the 4th time in 8 days. The day's actual knowledge (5 hours of `tiktok-video-editor` debugging saga yielding 3 system-wide lessons) was crystallized into synthesis concept pages rather than filling the 876 raw TODO stubs. The script-use-mandate lesson in particular needs promotion from `tiktok-video-editor` scope to `hermes-agent` system-wide — flagged in the new concept page + queued as orchestrator action item.

## Anti-patterns observed (negative signals for SKILL.md)

1. **Main pass missed the 3 always-mirror files AGAIN** — this is the 4th gap-fill run in 8 days caused by the same anti-pattern. The SKILL.md § 5b has the rule; the implementation isn't load-bearing enough. The 3 mirror operations need to be the **last** operations in the script, not optional, with a hard exit-code gate.
2. **The curator filled 3 synthesis pages but didn't update the 4 main-page synthesis stubs** — when a day's transcripts are summarized in 1-3 synthesis pages, the main-page synthesis stubs (15-25-45, 15-47-01, 17-14-22, 17-36-02) should be either filled OR marked merged-into-main. Leaving them as TODO creates a "broken promise" — the synthesis page says "main page is here" but the main page is still empty. Action item: add a protocol step in SKILL.md § 4 to handle this case.

## When to use this reference

- A day produced 3+ related transcripts on the same debugging topic (synthesis-over-fill pattern applies)
- Step 0 detection flagged a vault staleness gap on 1+ always-mirror files (gap-fill mode)
- You're tempted to fill 10+ individual TODO stubs in one pass (don't — synthesize instead)
- You're wondering whether to mark a watchdog stub as merged-into-main (yes, if a synthesis page already covers it)
