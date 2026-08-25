# Lesson — Verify clip 0004 Doroto Air Luxe V3 (18/07/2026)

**Clip:** `clip_0004_Final_troncau_may-hut-bui-doroto-air-luxe-v3.mp4` (106 MB)
**Source duration:** 166.43s (Mode B cô đọng, không speed-up)
**Edited:** 1080×1920 H.264 yuv420p, AAC LC 44100Hz stereo, 5100 kbps
**Trigger:** User instruction 18/07 verbatim — *"Verify nhanh clip 0004 Doroto Air Luxe V3 - chỉ check 5 lỗi narrative + FALSE START (đặc biệt 2 cặp manual suspect: "Đây là mẫu" + "Cục binh của nó là 4000mAh"). Không verify motion, không verify audio."*
**Tool:** Custom Python analyzer (49 segments, mlx_whisper medium-mlx word-timestamps, không chạy verify_clip_full.py vì scope-narrowed)

---

## Tóm tắt case

Clip 0004 Doroto Air Luxe V3 — review máy hút bụi mini 25.000 Pa + 4000mAh. Single continuous narrative 166.4s. Có 2 manual suspect pair user flag sẵn + 1 false positive từ whisper hallucination.

**Verify kết quả: PARTIAL PASS** — Scope-narrowed PASS ngoại trừ PAIR A (Đây là mẫu) chưa cut — cần re-render để bỏ 1 take.

---

## Scope-narrowed verify (per user instruction)

```bash
# CHẠY:
python3 scripts/verify_narrative_only.py <clip>.mp4 <keeps>.json <verify>.json
# CHECK: FILLER + TREO + LẶP NGHĨA + HOOK LẶP + ỰM Ỡ + FALSE START Layer 3
# SKIP: Layer 1 TikTok spec (optional context), Layer 2 anchor-lap,
#        Layer 5 RMS first-3s, Layer 6 RMS delta, Layer 7 motion
```

Output report PHẢI mở đầu **"Scope: ..."** để user biết em chỉ check phạm vi.

---

## 5-Dim + Layer 3 (per user scope)

| Layer | Check | Result | Notes |
|---|---|---|---|
| **FILLER** | ơ/ờ/ừm/ừ/ó/à/á | ⚠️ 1 hit at 153.84s "á" | TRAILING sentence-end intonation = NOT filler (PITFALL #15 position rule) |
| **TREO 3+ từ** | 3+ bridge words without USP | ✅ 0 hits | |
| **LẶP NGHĨA** | 2+ word head + tail match between 2 segs | ⚠️ 1 REAL + 1 FP | PAIR A (10.56s↔14.62s) = REAL; 130.92s↔130.94s = whisper ghost (PITFALL #13) |
| **HOOK LẶP 3+** | 3+ word head match consecutive | ⚠️ 1 REAL + 2 FP | PAIR A + 2 whisper ghosts |
| **ỰM Ỡ** | 1 từ ờ/à/ừm/ơ đơn (whole seg) hoặc head câu | ✅ 0 hits | |
| **FALSE START Layer 3** | 5+/8 first-word match + gap<10s | ✅ 0 hits (auto) | Manual suspect = PAIR A (5 head match "Đây là mẫu hút bụi Dodoto") + PAIR B (Cục binh 4000mAh đã cắt) |

---

## PITFALL #13 (NEW) — Whisper near-zero-duration ghost segments FALSE POSITIVE cho LẶP NGHĨA + HOOK LẶP

### Vấn đề

Khi Whisper (mlx_whisper medium) gặp **silent gap ~0.3s** giữa 2 keep thật, model hallucinate 1-2 ghost segments:
- Duration ≈ 0 (seg.end ≈ seg.start, thường 130.94 → 130.94)
- 2 segments liên tiếp có text IDENTICAL hoặc near-identical
- Cả 2 đều có prob thấp (0.04-0.50 cho nhiều từ)
- word-timestamps cho tất cả từ trong ghost seg đều bằng nhau (= timestamp cuối seg trước)

**Real case clip 0004:**
- Seg 28 (127.88-130.92s) **REAL**: "Các bạn có thể thổi bụi trong những cái nhỏ ra xong bắt đầu dùng đầu hút để hút"
- Seg 29 (130.92-130.94s) **GHOST**: "Các bạn có thể thổi bụi trong cái khu vực nhỏ này nè, các bạn có thể thổi bụi trong cái khu vực nhỏ này nè" (text 2 lần, duration 0.02s)
- Seg 30 (130.94-131.00s) **GHOST**: cùng text với seg 29, duration 0.06s
- Seg 31 (131.24-138.24s) **REAL**: "Đây là cái đầu để bom phao nè…"

**Phantom hits tạo ra:**
- LẶP NGHĨA #2: seg 29 ↔ seg 30 (head_match=3, tail_match=3) — **FP**
- HOOK LẶP #2: seg 28 → seg 29 (head_match=3) — **FP** (vì seg 28 ≠ ghost, seg 29 = ghost)
- HOOK LẶP #3: seg 29 → seg 30 (head_match=3) — **FP** (cả 2 đều ghost)

### Heuristic phát hiện ghost segment

```python
def is_ghost_seg(seg):
    """Whisper ghost segment nếu duration ≈ 0 + text repetition bên trong."""
    dur = seg["end"] - seg["start"]
    if dur < 0.5:  # sub-half-second
        return True
    if "words" in seg:
        # Check timestamps equality
        timestamps = [w["end"] for w in seg["words"]]
        if len(set(round(t, 2) for t in timestamps)) <= 2:
            # All words share same end timestamp = whisper hallucination
            return True
    return False

def filter_ghosts(segments):
    return [s for s in segments if not is_ghost_seg(s)]
```

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**SAU khi scan LẶP NGHĨA / HOOK LẶP, PHẢI filter ghost segments trước khi flag fail:**

1. Detect ghost seg với 1 trong 3 dấu hiệu:
   - `seg.end - seg.start < 0.5s` (duration gần 0)
   - Word timestamps tất cả bằng nhau (≤ 2 unique timestamps)
   - Avg word probability < 0.5 (model uncertainty)
2. Filter **CẢ 2** segments liên quan nếu 1 trong 2 là ghost
3. Chỉ tính LẶP NGHĨA / HOOK LẶP trên segments KHÔNG phải ghost
4. Trong báo cáo PHẢI ghi rõ "X hits = REAL, Y hits = FP (whisper ghost @ Zs)"

### Anti-pattern VĨNH VIỄN

- ❌ Flag LẶP NGHĨA khi 1 trong 2 segs có duration < 0.5s mà KHÔNG check ghost
- ❌ Trim 1 trong 2 ghost segments "vì lặp" → không có audio thật để trim
- ❌ Re-render để fix ghost → ghost là Whisper artifact, không có trong source audio
- ❌ Trust `verify_clip.py` strict output cho ghost segments → strict script cũng flag nhầm

### Real case clip 0004 (sau khi áp dụng rule)

| Pair | Initial verdict | After filter | Action |
|---|---|---|---|
| seg 1 (10.56s) ↔ seg 2 (14.62s) "Đây là mẫu" | HOOK LẶP + LẶP NGHĨA | **REAL** (PAIR A) | Cần fix keep |
| seg 28 (127.88s) → seg 29 (130.92s) | HOOK LẶP | **FP (ghost seg 29)** | Skip |
| seg 29 (130.92s) ↔ seg 30 (130.94s) | LẶP NGHĨA + HOOK LẶP | **FP (cả 2 ghost)** | Skip |

→ Sau filter: chỉ còn **1 REAL hit (PAIR A)**. Báo cáo đúng.

---

## PITFALL #14 (NEW) — Manual suspect pair verification workflow

### Vấn đề

User có thể explicit flag 2+ cặp suspect phrase (e.g. "PAIR A: 'Đây là mẫu' + PAIR B: 'Cục binh 4000mAh'") → em phải verify từng pair độc lập với transcript rồi phân loại kết quả:

| Verdict | Ý nghĩa | Action |
|---|---|---|
| **BOTH_IN_CUT** | Cả 2 take (cũ + mới) đều còn trong cut | **FAIL** — phải cắt 1 |
| **TAKE_NEW_ONLY** | Chỉ 1 take (mới) trong cut, take cũ đã cắt | **PASS** |
| **TAKE_OLD_ONLY** | Chỉ 1 take (cũ) trong cut, take mới đã cắt | **PASS** (rare) |
| **NEITHER** | Không còn take nào | **FAIL** — content thiếu |

### Workflow verify pair suspect

```python
def verify_pair(segments, phrase_a, phrase_b=None):
    """phrase_a = exact text, phrase_b = variant (optional).
    Return dict with verdict + timestamps.
    """
    hits = []
    for i, seg in enumerate(segments):
        text = seg["text"]
        for phrase in [phrase_a, phrase_b]:
            if phrase and phrase.lower() in text.lower():
                hits.append({
                    "seg_id": i,
                    "start": round(seg["start"], 2),
                    "end": round(seg["end"], 2),
                    "phrase": phrase,
                    "text": text.strip()[:200],
                })
    
    if len(hits) == 0:
        return {"verdict": "NEITHER", "hits": []}
    elif len(hits) == 1:
        return {"verdict": "TAKE_NEW_ONLY", "hits": hits}
    else:
        # Multiple hits = both takes still in cut
        return {"verdict": "BOTH_IN_CUT", "hits": hits}
```

### Real case clip 0004 — 2 manual suspect pairs

#### PAIR A: "Đây là mẫu hút bụi Dodoto Air Luxe V3" vs "Đây là mẫu hút bụi Dodoto Luxe V3"

| Take | Timestamp | Text | Duration |
|---|---|---|---|
| **TAKE CŨ** | 10.56s → 14.62s | "Đây là mẫu hút bụi Dodoto Air Luxe V3" (đầy đủ tên model) | 4.06s |
| **TAKE MỚI** | 14.62s → 17.56s | "Đây là mẫu hút bụi Dodoto Luxe V3" (rút gọn "Air") | 2.94s |

**Verdict: BOTH_IN_CUT** ⚠️

**Action đề xuất:**
- Keep TAKE CŨ (10.56s) — đầy đủ tên "Air Luxe V3", giữ USP model name đầu clip
- Cut TAKE MỚI (14.62s)

ffmpeg range để cut TAKE MỚI:
```bash
# Identify timecode của seg 2 trong keeps.json
# If seg 2 starts at 14.62s and ends at 17.56s, cut từ keeps.json
# Standard workflow: edit keeps.json để loại take mới, re-render
```

#### PAIR B: "Cục binh của nó là 4000mAh nên là có thể hút bụi được một khu vực liên tục" vs "...nên là nó có thể hút bụi liên tục được"

| Take | Timestamp | Text | Status |
|---|---|---|---|
| **TAKE MỚI** | 96.94s → 101.24s | "Cục binh của nó là 4000mAh nên là có thể hút bụi được một khu vực liên tục" | ✅ IN CUT |
| TAKE CŨ | — | — | ❌ NOT IN CUT (đã cắt) |

**Verdict: TAKE_NEW_ONLY** ✅

→ Editor đã xử lý đúng PAIR B. Không cần action.

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Khi user explicit flag K cặp suspect phrase:**

1. Verify TỪNG cặp độc lập (KHÔNG gộp chung)
2. Phân loại verdict enum (BOTH_IN_CUT / TAKE_NEW_ONLY / TAKE_OLD_ONLY / NEITHER)
3. Báo cáo PHẢI list timestamp + text cho từng take để user verify thủ công nếu cần
4. Action đề xuất cho mỗi cặp:
   - BOTH_IN_CUT: "Cut [take cũ hoặc mới] tại [timestamp]" — recommend cũ (giữ USP)
   - TAKE_NEW_ONLY / TAKE_OLD_ONLY: "None — đã xử lý đúng"
   - NEITHER: "Content thiếu — kiểm tra keeps.json"

### Anti-pattern VĨNH VIỄN

- ❌ Report "PAIR A: OK" khi cả 2 take đều còn — KHÔNG check transcript chỉ dựa vào cảm tính
- ❌ Auto-trim take "vì lặp" → có thể mất USP quan trọng (tên model đầy đủ)
- ❌ Bỏ qua cặp nào user flag vì "không thấy ngay" — PHẢI verify hết
- ❌ Generic "không có vấn đề" → không có timestamp evidence = không verify

---

## PITFALL #15 (NEW) — FILLER position classifier (trailing intonation ≠ leading filler)

### Vấn đề

List filler `ơ/ờ/ừm/ừ/ó/à/á` có 2 vai trò khác hẳn nhau:

| Position | Vai trò | Có cắt? |
|---|---|---|
| **Đầu câu** (sentence-initial) hoặc sau dấu `,` | Filler lửng lơ (anh đang suy nghĩ) | ✅ CẮT |
| **Cuối câu** (sentence-final trước `,` hoặc `.`) | Intonation marker tự nhiên (nhấn nhá) | ❌ GIỮ (giọng tự nhiên) |
| **Đứng đơn** (1 từ = whole segment) | ỰM_Ỡ đã catch ở Layer riêng | ❌ Layer khác |
| **Sau anchor verb** ("thì", "là") | Bridge filler | ✅ CẮT |

**Real case clip 0004:**
- 153.84s: "**á**" trailing in seg 33 "Trời ơi, làm rất là đẹp nha, hoàn thiện nhìn sang lắm luôn **á**"
- Position: AFTER "luôn" + near sentence-end → **intonation marker**, KHÔNG phải filler

### Heuristic classifier

```python
FILLER_TRAILING_OK = True  # trailing "á" near sentence-end = intonation

def classify_filler_position(word_obj, segment_text):
    """Return: 'trailing_intonation' | 'leading_filler' | 'bridge_filler'
    word_obj = {'word', 'start', 'end'}
    """
    raw = word_obj["word"].strip()
    text = segment_text.lower()
    
    # Find position ratio
    word_pos = text.find(raw.lower())
    if word_pos < 0:
        return "unknown"
    total_len = len(text)
    pos_ratio = word_pos / total_len if total_len > 0 else 0
    
    # Trailing: last 15% of text or after "luôn/nhé/nha/nhé/á"
    is_trailing = pos_ratio >= 0.85
    # Check if preceding word is one of: luôn, nhé, nha, nè, nhe, ha
    trailing_pattern = bool(re.search(
        r"(luôn|nhé|nha|nè|nhe|ha|đó|nhé)\s*$", 
        text[:word_pos].strip()
    ))
    
    # Leading: first 15% of text
    is_leading = pos_ratio <= 0.15
    
    # Bridge: right after thì/là/vì/bởi vì
    bridge_pattern = bool(re.search(
        r"(thì|là|vì|bởi vì|nên|cho nên)\s+$",
        text[:word_pos].strip()
    ))
    
    if is_trailing or trailing_pattern:
        return "trailing_intonation"  # giữ
    if is_leading or bridge_pattern:
        return "leading_filler" if is_leading else "bridge_filler"  # cắt
    return "middle_filler"  # check manual
```

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Khi FILLER scan phát hiện hit, PHẢI classify position trước khi flag FAIL:**

1. Check `word_pos / len(text)` ratio
2. Check trailing patterns ("luôn", "nhé", "nha", "á" ở cuối câu)
3. Check leading patterns (head of sentence)
4. Check bridge patterns (sau `thì/là/vì`)
5. **Trailing intonation = SKIP (giữ)**; leading/bridge = flag

### Anti-pattern VĨNH VIỄN

- ❌ Flag tất cả "ơ/ờ/ừ/á" mà KHÔNG check position
- ❌ Trim trailing "á" ở cuối câu → mất intonation tự nhiên
- ❌ Trim "á" ở "lắm luôn á" / "rất tốt á" → câu nghe cứng
- ❌ Không phân biệt được leading vs trailing filler

### Real case clip 0004 — á @ 153.84s

- Text full: "Trời ơi, làm rất là đẹp nha, hoàn thiện nhìn sang lắm luôn **á**"
- "á" at position ratio = 0.91 (trailing)
- Preceding pattern: "lắm luôn" matches trailing regex
- **Verdict: TRAILING_INTONATION → SKIP, không fail**

→ Final FILLER count: **0 REAL hits** (sau filter trailing) thay vì 1 hit raw

---

## Report template (scope-narrowed)

```markdown
# VERIFY REPORT — <clip_name>

**Scope**: 5 lỗi narrative + FALSE START (motion + audio SKIP per user)
**Source**: mlx_whisper medium-mlx word-timestamps, <N> segments

## Kết quả

| Layer | REAL hits | FP (whisper ghost) | Status |
|---|---|---|---|
| FILLER | 0 | 1 (trailing intonation @ 153.84s) | ✅ PASS |
| TREO | 0 | 0 | ✅ PASS |
| LẶP NGHĨA | 1 (PAIR A) | 1 (ghost @ 130.92) | ⚠️ FAIL |
| HOOK LẶP | 1 (PAIR A) | 2 (ghost chain) | ⚠️ FAIL |
| ỰM Ỡ | 0 | 0 | ✅ PASS |

## Manual suspect pairs

| Pair | Verdict | Timestamp | Action |
|---|---|---|---|
| PAIR A "Đây là mẫu" | ⚠️ BOTH_IN_CUT | 10.56s + 14.62s | Cut TAKE MỚI |
| PAIR B "Cục binh 4000mAh" | ✅ TAKE_NEW_ONLY | 96.94s | None |

## VERDICT
⚠️ CẦN RE-RENDER — chỉ action duy nhất: cut 1 trong 2 take ở PAIR A.
```

---

## Changelog reference

- **v1.0.10 (18/07/2026)** (this session): PITFALL #13 (whisper ghost segments false positive) + PITFALL #14 (manual suspect pair verification workflow) + PITFALL #15 (FILLER position classifier: trailing intonation ≠ leading filler). Real case clip 0004 Doroto Air Luxe V3: PAIR A FAIL cần cut, PAIR B đã PASS đúng, ghost segments @ 130.92-131.00s filtered thành công.
