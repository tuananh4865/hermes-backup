# Curator Anti-Patterns — 2026-07-29 batch (L74, L75, L77)

Three new anti-patterns captured in the 2026-07-29 02:00 curator pass. Each surfaced in real execution (not speculation) and was verified by `diff -q` + state.db cross-check.

## L74 — iCloud vault top-level listing hangs 30s+

**Symptom:** `os.listdir(VAULT)`, `subprocess.run(['ls','-1', VAULT])`, and `find "$VAULT"` all hang past 30s when iCloud Drive is actively syncing the directory listing. Subdirectory listings against the SAME vault succeed in 0.18s.

**Verified 2026-07-29 02:00:** vault root listing timed out 3x (5s, 15s, 30s timeouts all failed). `os.listdir(VAULT/entities)` returned 5 entries in 0.18s. `os.listdir(VAULT/concepts)` likewise succeeded.

**Pattern:** For any set-diff between wiki and vault, query SUBDIRECTORIES DIRECTLY (`os.listdir(VAULT/concepts)`, `os.listdir(VAULT/entities)`) rather than listing the vault root. Wrap the call in `signal.alarm(N)` so a slow listing doesn't blow the script timeout. Python `os.listdir` is faster than `subprocess.run(['ls', ...])` or `find` for this comparison — each subprocess spawn has its own latency.

```python
import signal
def handler(s, f): raise TimeoutError()
signal.signal(signal.SIGALRM, handler)

VAULT = "/Users/tuananh4865/Library/Mobile Documents/iCloud~md~obsidian/Documents/My-Brain"
try:
    signal.alarm(5)
    ents = os.listdir(f"{VAULT}/entities")
    signal.alarm(0)
except TimeoutError:
    pass  # fallback: skip set-diff or use subdirectory
```

**Why this matters:** Without the subdirectory-direct approach, the set-diff gate (L52/L54/L55) would have crashed the 29/07 pass entirely — the curator would have hit the script timeout before mirror recovery could begin.

## L75 — Per-session extraction when 2 sessions share a theme but lack a third

**Symptom:** The synthesis-over-fill pattern (07-04 L27, default for 3+ transcripts sharing a meta-lesson) does NOT trigger at exactly 2 sessions even if they share a surface-level theme. Trying to apply it inflates the synthesis page with two unrelated topics.

**Verified 2026-07-29 02:00:** 2 substantive Telegram sessions — ComfyUI feasibility check (10:00, 19 msg) + Google Flow rename via `computer_use` (10:17, 55 msg). Both touched "evaluating AI tooling for content workflow" but with different foci:
- ComfyUI = local gen video (verdict per model: SDXL/Flux/Wan/Hunyuan)
- Google Flow = remote browser AI suite (cua-driver AXUIElementPerformAction -25202 limitation)

A single synthesis page would have mixed two unrelated technical issues; filling 5-10 stubs was impossible (only 2 sessions).

**Right answer:** 2 per-session concept pages (`concepts/comfyui-m4-24gb-feasibility-2026-07-28.md`, `concepts/google-flow-rename-cua-driver-limitation-2026-07-28.md`), each with 4-5 wikilinks to existing siblings (`learned-about-tuananh`, `comfyui-skill`, `browser-harness`, `macos-computer-use`).

**Decision tree:**
```
substantive_sessions = SELECT COUNT(*) FROM state.db WHERE ... AND message_count > 10
if substantive_sessions >= 3 and same_meta_lesson:
    → synthesis-over-fill pattern (1-3 synthesis + N merged-into-main redirects)
elif substantive_sessions in [1, 2]:
    → per-session extraction (1 concept page per session, no synthesis)
else:  # 0
    → noop protocol
```

## L77 — Junk test files in `wiki/concepts/` skew set-diff overage

**Symptom:** Set-diff from L55 surfaced 1 "missing" file (`_test_audit_file.md`) that was actually a 91-byte stale test stub from 2026-07-19 (`title: Test Audit File` + 4 lines), not a missing mirror target. Without inspecting the missing file before mirroring, the pass would have wasted an MD5 cycle trying to copy a file that should be deleted.

**Pattern:** Before mirroring any set-diff "missing" entry, `cat` or `head` the source file. If content is `<100` bytes AND filename starts with `_test_` or matches a known stub pattern (`title: Test*`), DELETE the source file instead of mirroring it.

```bash
# In a Python loop:
missing = subprocess.check_output(['comm','-23',wiki_list,vault_list]).decode().strip().split('\n')
for f in missing:
    p = f"{WIKI}/concepts/{f}"
    sz = os.path.getsize(p)
    head = open(p).read(200)
    if sz < 100 and (f.startswith('_test_') or 'title: Test' in head):
        os.remove(p)
        print(f"DELETED junk: {f}")
    else:
        # normal mirror
        ...
```

**Verified 2026-07-29 02:00:** 1 deletion + 0 mirror cycles for `_test_audit_file.md`, set-diff cleanly resolved (vault 211→210 concepts, wiki 99→100 after creating 2 new pages).

**Origin:** watchdog-processor may have created the stub during a test run in 2026-07-19 and never cleaned up. Filename `_test_audit_file.md` is a clear signal it was never meant to be a permanent page.

---

**Total curator pass stats for this anti-pattern batch:**
- 2 new concept pages created (5+4 = 9 body wikilinks)
- 11 cross-reference delta (2 entity page relationships + 2 index catalog)
- 5 files mirrored byte-identical (3 always-mirror + 2 concepts)
- 1 junk file deleted
- 2 new L-numbered lessons captured (L75 + L76 in entity page; L74/L75/L77 here)
- Log entry appended BEFORE mirror per L51 ordering trap