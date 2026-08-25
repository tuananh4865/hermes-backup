# Delivery Report Pattern — N files researched must show concrete outputs separately

> Source session: 2026-07-20, 14 vt.tiktok.com URLs handed by Tuấn Anh. 10 cached + 4 new. 5 subagents dispatched.

## The anti-pattern that broke user trust

When subagent research finishes N files (M new + K verified), the natural reply is a single summary table showing **status** (e.g. "4 MỚI / 10 ĐÃ CÓ"). This table shows the WORK SCOPE but NOT the WORK OUTPUT. After 5-10 minutes of waiting, the user scans the table, sees "MỚI = CHƯA CÓ", and assumes nothing was done.

**User verbatim feedback 20/07:**
> "Chưa thấy sp này" — referring to PID 1733974507990517546 (Tấm kẹp nhanh Universal Arca Swiss)

The file `tam-kep-nhanh-arca-swiss-universal.md` had already been written by the subagent. The work was 100% done. But the status table made it look like work was 0% done for that PID.

## Vĩnh viễn rule

**Every delivery report for multi-file batch research must contain 2 separate concrete sections:**

1. **🆕 Files vừa tạo mới** — full absolute paths + 1-line description per file
2. **🔄 Files đã verify cập nhật** — full absolute paths + diff line per file (if any)
3. **📊 Summary table** — status only, AFTER the 2 concrete sections

The order matters: concrete outputs FIRST, summary table LAST. The user can confirm delivery by reading 1-3 section, not by parsing a status table.

## Template

```
## ✅ Files vừa tạo mới (N entries)
1. `/Volumes/.../products/<slug-1>.md` — 1-line description of what's in the file
2. `/Volumes/.../products/<slug-2>.md` — 1-line description
...

## 🔄 Files đã verify cập nhật (K entries)
1. `/Volumes/.../products/<slug-3>.md` — DIFF: was X, now Y (only if changed)
2. NO CHANGE for 9 entries (list filenames)

## 📊 Status summary
- Tổng: N + K = 14
- New wiki files: N
- Updated wiki files: K (with explicit diffs)
- No-change files: K - (updated count)
```

## Anti-patterns VĨNH VIỄN

- ❌ Single status table without absolute file paths
- ❌ "Đã research xong" without listing what was created
- ❌ Embedding file paths only at end after lots of preamble
- ❌ Trusting the user to grep `ls products/` themselves
- ❌ Showing subagent dispatch metadata instead of output paths

## Why this is a CLASS-level rule

This applies to ANY multi-file batch delivery, not just TikTok Shop research:
- Wiki batch sync (15 files mirroring)
- Subagent verify report (3-5 clips verified)
- Skill patch updates (3-5 SKILL.md files updated)
- Cron validation (10 jobs checked)

The shape is always **N file-outputs to surface**. The pattern holds.

## Pitfall № — single status table hides actual deliverables

Subagent system-wide pattern: subagent FINISHES writing files to disk, then returns "research complete" — but the orchestrating agent only relays "research complete" without enumerating file paths. User is left to guess which files exist.

Fix: orchestrating agent MUST enumerate every file the subagent created, with absolute path + 1-line content summary.
