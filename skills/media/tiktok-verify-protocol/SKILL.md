---
name: tiktok-verify-protocol
description: 'Verify protocol BẮT BUỘC cho MỌI video edit. 5 lỗi: FILLER (ơ/ờ/ừm/ừ/ó/à/á) + ỰM/Ờ + TREO + LẶP NGHĨA (2+ từ đầu) + HOOK LẶP (3+ từ đầu). Plus FALSE START Layer 3 (5+/8 từ đầu gap<10s) + scope-narrowed verify (user "chỉ check X+Y, không verify Z" → báo cáo phải mở đầu "Scope") + manual suspect pair workflow (user flag N cặp phrase → verify từng cặp, classify BOTH_IN_CUT / TAKE_NEW_ONLY). PITFALL #13 whisper ghost segments + #14 manual suspect pair verdict enum + #15 FILLER position classifier + #11 parallel-reason + #12 enumeration + #16 manual-subagent cross-check + #23 Layer 5 speed 1.3x indirect proof (Mode B keep_pct 30-80%) + #24 verify-context filename mismatch (verify disk reality + flag mismatch) + **#25 TECHNICAL SPEC VERIFY (encoding/integrity/pixel) — xem references/pitfall-25-technical-spec-verify.md**. Tool verify_clip.py + verify_clip_full.py 7-layer one-shot. Spec TikTok 1080×1920/44100Hz/Mode B 80-120s max 130s.'
version: 1.1.1
author: 'Tuấn Anh + Hermes Agent (v1.1.1 21/07/2026 — PITFALL #23 Layer 5 speed 1.3x indirect proof (Mode B keep_pct 30-80%, ratio source/final literal SAI) + PITFALL #24 verify-context filename mismatch (verify disk reality, flag mismatch, đánh giá theo disk evidence không auto-fail theo user input). Real case 21/07 batch 7 DJI clips 0029-0038: 0/7 ratio source/final = 1.3 (thực tế 1.42-2.30) nhưng 7/7 speed 1.3x verified gián tiếp; 2/7 file filename user-input sai (0034/0038 chưa rename theo actual duration). v1.1.0 19/07/2026 — Add 5-EVIDENCE pattern (PITFALL #42). v1.0.11 — 18/07 PITFALL #16. v1.0.10 — 18/07 PITFALL #13/14/15. v1.0.9 PITFALL #12. v1.0.8 PITFALL #10/11. v1.0.7 PITFALL #9. v1.0.6 PITFALL #7. v1.0.5 PITFALL #6. v1.0.4 PITFALL #5. v1.0.3 PITFALL #4. v1.0.2 PITFALL #3. v1.0.1 PITFALL #1/2. v1.0.0 12/07/2026.)'
license: MIT
platforms: [macos]
metadata:
  category: media
  class: video-editing-qa
  triggers: verify, check, đạt goal, có lỗi không, sau render, trước khi báo xong
---

# tiktok-verify-protocol

**Class-level umbrella** for the verification protocol that EVERY video edit MUST pass before delivery. Extracted from the tiktok-video-editor skill because verification is reusable across any TikTok clip workflow, not just this one skill.

---

## Trigger

Load this skill when:
- Any video edit workflow produces a final `.mp4` file
- User asks "verify", "check", "đạt goal", "có lỗi không"
- Before declaring a task complete
- After any change to `keeps.json`, source filter, or render command

---

## CORE PROTOCOL: Hard Check Mọi Thứ (FIRST-CLASS)

> **User verbatim feedback (11/07/2026):**
> *"phải hard check để đảm bảo mọi thứ thực sự hoạt động đúng với mục đích của nó không phải chỉ báo cho qua, cho có, cho xong!"*

## Anti-pattern tuyệt đối KHÔNG
- ❌ Báo "xong" khi chưa chạy verify
- ❌ Bỏ qua issues còn lại vì "nhỏ quá"
- ❌ Apply rule mà không nói tên rule ra
- ❌ Tạo artifact không dùng được / chỉ mang tính trưng bày
- ❌ **PASS verify_clip.py không có nghĩa là pass goal** — strict script bỏ sót semantic lap khi 2 keeps back-to-back cùng chứa 1 keyword (vd "nhãn hàng", "nhưng mà") nhưng prefix 2 từ đầu KHÁC nhau. Xem Pitfall #1 dưới đây.
- ❌ **Báo PASS khi scope-narrowed** mà KHÔNG ghi rõ scope (xem PITFALL #12 scope-narrowed verify workflow)
- ❌ **Báo FALSE START 0 hits** cho manual suspect pair (PITFALL #14) mà không verify từng cặp

### ✅ Pattern BẮT BUỘC
1. Sau khi tạo artifact → chạy verify tool NGAY
2. Nếu fail → fix → re-verify (loop đến khi pass)
3. Nếu fail 3 lần liên tiếp → escalate, KHÔNG bỏ qua
4. Trước khi báo "xong" → chạy qua checklist
5. **Nếu scope-narrowed** → báo cáo mở đầu `**Scope**: ...` (PITFALL #12)
6. **Nếu manual suspect pair** → verify từng cặp theo verdict enum PITFALL #14

---

## 5 Loại Lỗi BẮT BUỘC Check (v3.21.4)

| # | Loại | Quy tắc phát hiện |
|---|------|-------------------|
| 1 | **FILLER** | Từ `ơ, ờ, ừm, ừ, ó, à, á` đầu/cuối câu — **trailing intonation tự nhiên KHÔNG tính** (xem PITFALL #15 classifier) |
| 2 | **ỰM / Ờ** | 1 từ `ờ/à/ừm/ơ/uh/um` đứng đơn (cả seg) hoặc đứng đầu câu |
| 3 | **TREO** | Câu 3-8 từ toàn bridge words (thì, là, ờ, à, ừm, ơ, bởi, vì, thôi, nha, đó, cái, này...) KHÔNG có USP keyword (sẽ, có thể, giúp, cho, được, hơn, nhất, đặc biệt, 1m6, 90 độ, 360 độ, 3kg, gọn, bền, chắc, đa năng, thông minh) |
| 4 | **LẶP NGHĨA** | 2+ từ đầu giống nhau giữa 2 segs liên tiếp — **filter ghost segments trước** (xem PITFALL #13) |
| 5 | **HOOK LẶP** | 3+ từ đầu giống nhau giữa các segs cách nhau <15 segs — **filter ghost segments trước** (xem PITFALL #13) |

**LƯU Ý quan trọng về filler list v3.21.4:**
- ❌ KHÔNG bao gồm "đó" - vì "đó" là đại từ chỉ định ("cái tripod đó", "thời gian đó")
- ❌ KHÔNG bao gồm "thì" - vì "thì" có 2 vai trò: bridge filler đầu câu (cắt được) VÀ ngữ pháp nối vế "khi X thì Y"/"nếu X thì Y" (KHÔNG cắt được). Khó phân biệt tự động → bỏ luôn.

**Filler list cuối cùng (vĩnh viễn):** `ơ, ờ, ừm, ừ, ó, à, á`

**⚠️ Position classifier (PITFALL #15):** "á" cuối câu sau "luôn/nhé/nha/nè" = trailing intonation marker → GIỮ. Chỉ "á" đầu câu/sau "thì, là, vì" mới là filler cần cắt. Xem PITFALL #15 để có heuristic classifier.

---

## Spec TikTok BẮT BUỘC

| Spec | Yêu cầu |
|------|---------|
| Resolution | 1080×1920 |
| Sample rate | 44100 Hz |
| Codec video | h264 high profile, yuv420p |
| Codec audio | AAC, 192k |
| Duration | 60-180s (cho 1 video TikTok) |
| Container | MP4 với `-movflags +faststart` |

---

## Scope-narrowed verify workflow (PITFALL #12)

**Khi user explicit giới hạn scope** (vd "chỉ check 5 lỗi narrative + FALSE START, không verify motion, không verify audio"):

1. **CHẠY** các layer được chỉ định (Layer 1 + Layer 3 cho narrative + FALSE START)
2. **SKIP** các layer user không muốn (Layer 4 motion + Layer 5/6 RMS audio)
3. **Báo cáo mở đầu** bằng `**Scope**: [scope list]` để user biết em chỉ check phạm vi được yêu cầu
4. **KHÔNG** tự ý mở rộng scope "cho an toàn"
5. **VẪN** phải flag đầy đủ issues trong scope (không skip vì "scope-narrowed")

**Manual suspect pair workflow (PITFALL #14):** Khi user flag N cặp phrase suspect (vd "Đây là mẫu" + "Cục binh 4000mAh"), phải verify TỪNG cặp độc lập với 4 verdict enum:
- **BOTH_IN_CUT** (FAIL — cắt 1 take)
- **TAKE_NEW_ONLY** (PASS)
- **TAKE_OLD_ONLY** (PASS hiếm gặp)
- **NEITHER** (FAIL — content thiếu)

Xem PITFALL #14 để có verdict enum + workflow chi tiết.

---

## Tool BẮT BUỘC: `scripts/verify_clip.py`

```bash
# Usage
python3 scripts/verify_clip.py <audio.json> <keeps.json> [render.mp4]

# Output:
# ✅ ĐẠT GOAL - file có thể public!   (exit 0)
# ❌ CHƯA ĐẠT GOAL - N vấn đề:     (exit 1)
```

**Tool tự động check:**
- 5 loại lỗi trên (FILLER, ỰM/Ờ, TREO, LẶP NGHĨA, HOOK LẶP) — LƯU Ý: KHÔNG filter ghost segments (PITFALL #13), KHÔNG classify filler position (PITFALL #15)
- Spec TikTok (nếu truyền render.mp4)

**Source code:** `scripts/verify_clip.py` v3.21.4 (7.7KB, tại `~/.hermes/skills/media/tiktok-verify-protocol/scripts/verify_clip.py`)

---

## Workflow BẮT BUỘC (8-STEP v3.21.4)

```
1. WHISPER TRANSCRIBE
2. AUTO-CLASSIFY (DRAFT)
3. ⭐ ĐỌC-HIỂU-CẢM-XÚC (đọc kỹ từng seg)
4. ⭐ APPLY 7 KEY INSIGHTS
5. ⭐ FILLER + TREO + LẶP TRIM
   - Filler list: ơ, ờ, ừm, ừ, ó, à, á (KHÔNG có "đó", "thì")
   - Filler position classifier (PITFALL #15): trailing intonation = giữ
   - TREO/LẶP: giữ TAKE CUỐI (Insight 9)
   - CTA: KHÔNG bắt buộc xoá (giữ CTA)
6. ⭐ SPEED-UP 1.3x
7. RENDER → file .mp4
8. ⭐⭐⭐ VERIFY RE-READ ⭐⭐⭐ (BẮT BUỘC CẢ 2 LAYERS)
   - Layer 1: scripts/verify_clip.py (5-dim strict)
   - Layer 2: scripts/check_anchor_lap.py (semantic anchor)
   - Layer 3: FALSE START scan (PITFALL #10, gap<10s + 5+/8 first-word)
   - Layer 3b: Ghost segment filter (PITFALL #13)
   - Layer 3c: Manual suspect pair verification (PITFALL #14, nếu user flag pairs)
   - Layer 3d: Filler position classify (PITFALL #15)
   - Nếu CẢ 2 layers PASS → public được
   - Nếu 1 layer FAIL → fix keeps → re-render
   - 1 layer only = FALSE PASS (Pitfall #4)
```

---

## 🎯 Khẩu hiệu (System-Wide Rule 3)

> **User verbatim:** *"mỗi khi chạy cần có một khẩu hiệu bặt buộc em phải nói ra để anh biết em đang làm và đã làm việc theo các rule và system anh setup cho em bằng chính tên của các rules và hệ thống đó!!!!"*

**Format mới (consolidated 12/07/2026):** Mỗi task response có **1 dòng** 🎯 tổng hợp systems đã dùng. KHÔNG spam 🎯 mỗi tool call.

```
🎯 SYSTEMS USED: [tên systems ngắn gọn]
```

**Ví dụ ĐÚNG (1 dòng):**
```
🎯 SYSTEMS USED: Core #1 (perfect result) + Karpathy #3 (surgical) + Fable 5 §3 (skills-first) + Loop (verify)
```

**4 HỆ THỐNG BẮT BUỘC:**
1. **Core Philosophy** (4 rules SOUL.md) - gốc
2. **Karpathy System** (4 rules CLAUDE.md) - coding
3. **Fable 5 Patterns** (6 patterns: MCP, Persistent Storage, Skills-First, Search Discipline, Artifact Decision, Visual Decision)
4. **Loop Engineering** (3 loops: Verify / Self-learning / Wiki sync)

**Tại sao consolidate:** subagent verify SOUL.md 12/07 flag "1 task = 4-6 systems × 🎯 banner = output inflate 30-50%, vi phạm short/casual rule". 1 dòng tổng hợp vẫn khai báo hệ thống nhưng gọn hơn 80%.

---

## Checklist BẮT BUỘC trước khi báo "xong"

- [ ] verify_clip.py chạy exit 0 (Layer 1)
- [ ] check_anchor_lap.py chạy exit 0 (Layer 2)
- [ ] **CẢ 2 LAYERS PASS** — nếu chỉ 1 layer PASS = FALSE PASS (Pitfall #4)
- [ ] **Ghost segment filter đã chạy** (PITFALL #13) — segment duration <0.5s bị filter
- [ ] **Manual suspect pair verified** (PITFALL #14) — nếu user flag cặp suspect
- [ ] **Filler position classified** (PITFALL #15) — trailing intonation = SKIP
- [ ] File .mp4 tồn tại + đúng spec TikTok
- [ ] Duration trong khoảng 30-180s
- [ ] Wiki memory đã update (nếu có lesson mới)
- [ ] Skill version đã update (nếu rule thay đổi)
- [ ] Khẩu hiệu 🎯 đã nói trong output
- [ ] Không còn "❌ CHƯA ĐẠT" issues
- [ ] Đã đọc TOÀN BỘ Whisper verify transcript (không skip seg nào)

---

## 🚨 PITFALL #1 (FIRST-CLASS) — verify_clip.py PASS vẫn có thể FAIL goal

**Ngày phát hiện:** 13/07/2026 (clip 0740 "Body mist AMAP - tinh tế", 114.8s).

### Vấn đề
`verify_clip.py` v3.21.4 dùng **strict 2-word-prefix matcher** trên **chosen_segs** (chỉ lấy segments thỏa `seg['start'] >= s_start - 0.3 AND seg['end'] <= s_end + 0.5`). Nó BỎ SÓT 2 loại semantic lap_nghia:

**Loại A — cross-keep same-keyword with different prefix:**
- keep[0]: "**nhãn hàng** này làm ơn có thể gửi cho mình..."
- keep[1]: "tại vì mình thích những sản phẩm của **nhãn hàng** này quá"
- Strict matcher: 2 từ đầu `[nhãn, hàng]` vs `[tại, vì]` → match=0 → không flag
- Nhưng khi nghe: cùng anchor "nhãn hàng" lặp 2 take liên tiếp → người nghe thấy ngay

**Loại B — chosen_segs filter excludes spillage segments:**
- Strict `s_start - 0.3 / s_end + 0.5` window loại segments tràn biên keep → không còn "adjacent" trong chosen_segs → strict matcher không so sánh được

**Loại C — semantic "nhưng mà" lặp**: keep[12] src[46] "**nhưng mà** có người..." + keep[13] src[52] "**Nhưng mà** nếu mà trời mát lạnh..." → matcher strict thấy `[nhưng, mà]` vs `[Nhưng, mà]` lowercase-strip → match=2 → flag được. NHƯNG nếu các keeps khác chen giữa thì KHÔNG flag được vì không còn adjacent trong chosen_segs.

### Quy tắc BẮT BUỘC — bổ sung ngoài verify_clip.py

**SAU khi `verify_clip.py` exit 0**, PHẢI chạy thêm 3 bước semantic check TRƯỚC khi báo "xong":

1. **Whisper lại file output** (`clip_*_verify.wav` → `clip_*_verify.json`) — đọc text trực tiếp để TAI người ảo nghe thấy.
2. **Quét text verify cho anchor-keyword lặp**. Duyệt list keyword anchor thường gặp:
   `[nhãn hàng, nhưng mà, tuy nhiên, cho nên, vì vậy, do đó, bởi vì, nói chung, tóm lại, cuối cùng, kết luận, nhà mình, bên mình, các bạn, mọi người]`
   Với MỖI keyword, check nếu xuất hiện ≥2 lần trong các seg LIÊN TIẾP (cách nhau ≤1 seg trong verify transcript) → BÁO FAIL.
3. **Cross-check keeps gốc với chosen_segs** — nếu số keeps > số chosen_segs, nghĩa là filter đang drop segments tràn biên. Re-derive chosen_segs với tolerance rộng hơn (±1.0s thay vì ±0.3/0.5) rồi chạy lại strict matcher.

### Snippet check anchor-keyword (paste vào shell ngay sau verify_clip.py PASS)

```python
import json, sys
verify = json.load(open(sys.argv[1]))
segs = verify['segments']
ANCHORS = ['nhãn hàng', 'nhưng mà', 'tuy nhiên', 'cho nên', 'vì vậy',
           'do đó', 'bởi vì', 'nói chung', 'tóm lại', 'cuối cùng',
           'kết luận', 'nhà mình', 'bên mình']
fails = []
for i in range(len(segs)-1):
    t1, t2 = segs[i]['text'].lower(), segs[i+1]['text'].lower()
    for kw in ANCHORS:
        if kw in t1 and kw in t2 and segs[i+1]['start'] - segs[i]['end'] < 3:
            fails.append((segs[i]['id'], segs[i+1]['id'], kw, t1[:60], t2[:60]))
if fails:
    print("❌ ANCHOR-LAP detected:", fails); sys.exit(1)
print("✅ No anchor-lap")
```
### Tại sao đây là pitfall FIRST-CLASS

- Parent user đã flag trong task description của clip 0740 (seg[0]≈[1] "nhãn hàng" + seg[18]≈[23] "nhưng mà")
- Strict script vẫn PASS → con em sẽ tin script và báo "đạt goal" → user phải test thủ công mới bắt được
- Đây là vi phạm System-Wide Rule #2 (VERIFY) + "hard check mọi thứ" của anh: dùng tool 1 lớp, không có layer độc lập

### Xem thêm
`references/pitfall-strict-matcher-blind-spot-2026-07-13.md` — transcript đầy đủ + repro 3 case thực tế.

---

## 🚨 PITFALL #3 (FIRST-CLASS — 14/07/2026) — `check_anchor_lap.py` FALSE POSITIVE TRÊN KEEPS GHÉP

**Ngày phát hiện:** 14/07/2026 (clip 0751 body mist AMAP — anchor keywords "các bạn", "chúng ta", "thì đó" xuất hiện >10 lần trong source tự nhiên).

### Vấn đề

`check_anchor_lap.py` check **adjacent segments trong Whisper output**, KHÔNG phân biệt được:
- **Anchor TRONG keep GHÉP** (cùng 1 keep, multiple Whisper segments) → false positive
- **Anchor CROSS keep boundary** (2 keeps riêng, audio bị cắt giữa cụm từ) → real issue

**Real case clip 0751:** Source có "các bạn" 9 lần, "chúng ta" 5 lần, "thì đó" 2 lần (cách nói tự nhiên của anh). Khi trim keeps GHÉP nhiều source segments liên tiếp, Whisper sẽ output mỗi source segment thành 1 Whisper segment riêng → script báo 8 anchor-lap pairs dù audio thực tế liên tục.

### Quy tắc FIX bắt buộc — chia keeps NHỎ + cách ly anchor keywords

**Khi phát hiện anchor-lap từ `check_anchor_lap.py`, phải kiểm tra:**
1. Mở Whisper verify transcript, check `seg_a` và `seg_b` 
2. Nếu 2 segments có GAP TIME = 0.0s và CHUNG start-end với 1 keep range → FALSE POSITIVE (anchor nằm trong keep, không phải cross-boundary)
3. **Chỉ FAIL khi anchor xuất hiện ở 2 keep RIÊNG BIỆT** (giữa các keeps, không phải trong cùng keep)

**Cách tránh false positive khi build keeps:**
- Chia keeps NHỎ (max 5-10s) để mỗi keep chỉ chứa 1 instance của anchor keyword
- Tách keeps tại boundary có anchor keyword xuất hiện (VD: keep A chứa "các bạn" lần 1, keep B chứa "các bạn" lần 2, **KHÔNG đặt keep A liền kề keep B**)
- Insert gap/implicit silence giữa keeps có anchor keywords giống nhau

### Snippet fix: Whitelist keeps KHI script báo FAIL

```python
import json, subprocess

def verify_with_keep_awareness(audio_json, keeps_json, render_mp4):
    """Custom verifier respecting keep boundaries"""
    with open(audio_json) as f:
        verify = json.load(f)
    with open(keeps_json) as f:
        keeps = json.load(f)
    
    # Build set of (start, end) keep ranges
    keep_ranges = set()
    for k in keeps:
        keep_ranges.add((round(k['start'], 1), round(k['end'], 1)))
    
    issues = []
    v_segs = verify.get('segments', [])
    anchors = ['các bạn', 'nhưng mà', 'tuy nhiên', 'cho nên', 'vì vậy',
               'do đó', 'bởi vì', 'nói chung', 'tóm lại', 'cuối cùng',
               'nhà mình', 'bên mình', 'chúng ta']
    
    for i in range(len(v_segs) - 1):
        s1, s2 = v_segs[i], v_segs[i+1]
        gap = s2.get('start', 0) - s1.get('end', 0)
        t1 = (s1.get('text') or '').lower()
        t2 = (s2.get('text') or '').lower()
        
        for kw in anchors:
            if kw in t1 and kw in t2 and gap < 5.0:
                # Check if both segments are inside the SAME keep (false positive)
                s1_in_keep = any(s1.get('start', 0) >= ks - 0.5 and s1.get('end', 0) <= ke + 0.5 
                                    for ks, ke in keep_ranges)
                s2_in_keep = any(s2.get('start', 0) >= ks - 0.5 and s2.get('end', 0) <= ke + 0.5 
                                    for ks, ke in keep_ranges)
                
                if s1_in_keep and s2_in_keep:
                    continue  # Same keep, false positive
                
                issues.append({'i': i, 'kw': kw, 'gap': gap, 
                              'a': t1[:80], 'b': t2[:80]})
    
    return issues
```

### Thực hành tốt nhất: Trim keeps NHỎ + word-level cut

Khi anchor keyword xuất hiện nhiều lần tự nhiên trong source audio:
1. **Chia keeps tại boundary anchor keywords** — VD "các bạn thứ nhất" thuộc keep A, "các bạn thứ 2" thuộc keep C (insert keep B ở giữa với content khác anchor)
2. **Word-level cut** tại ký tự space ngay SAU anchor keyword nếu keep boundaries phải overlap với anchor — Whisper sẽ tách thành 2 segments riêng biệt
3. **Trim filler "á" cuối câu** (seg 7 trong nhiều clips) — đã là lệnh vĩnh viễn từ v3.21.4

### Real case 14/07 clip 0751

Source có "các bạn" 9 lần, "chúng ta" 5 lần, "thì đó" 2 lần. Cách fix tạm thời (khi chưa update skill):
- **Accept PARTIAL_PASS** khi anchor keywords đến từ source tự nhiên của speaker (anh Tuấn Anh hay dùng "các bạn"/"chúng ta" thường xuyên)
- KHÔNG ép fit anchor-lap = 0 nếu source natural có anchor keywords nhiều
- Trade-off: chấp nhận 1-2 anchor-lap FALSE POSITIVE (trong same keep) thay vì trim quá aggressive

### Xem thêm
`references/pitfall-anchor-lap-false-positive-2026-07-14.md` — repro case clip 0751 + test 3 strategies (giữ keeps GHÉP vs word-level cut vs accept partial).

---

## 🚨 PITFALL #4 (FIRST-CLASS — 14/07/2026) — Verify chỉ 1 layer = FALSE PASS

**User verbatim feedback 14/07/2026:**
> *"Anh thấy ở bước verify em làm đang không kĩ khiến cho các clip đầu ra vẫn còn lỗi lặp câu và các câu lỗi tồn tại trong clip!!! Hãy đảm bảo mọi lần sau ở bước verify phải thực sự kiểm tra thật kĩ toàn bộ transcript mà không bỏ qua bước nào!!!"*

### Vấn đề

Trước 14/07, em chỉ chạy **Layer 1 (5-dim strict)** trong Bước 8 verify, bỏ qua **Layer 2 (anchor-lap semantic)**. Kết quả:

**8/8 clip SHIP 14/07** mà khi chạy lại đầy đủ 2 layers:
- **4/8 clip FAIL Layer 2** (clip 0749, 0751, 0752, 0758)
- Tổng **22 anchor-lap pairs** bị miss (anchor keywords "các bạn", "chúng ta", "thì đó" lặp liên tiếp)

### Quy tắc vĩnh viễn (FIRST-CLASS)

**MỖI clip edit xong PHẢI chạy CẢ 2 verify layers trước khi báo "xong":**

```bash
# Layer 1: 5-dim strict (FILLER + ỰM/Ờ + TREO + LẶP NGHĨA + HOOK LẶP)
python3 scripts/verify_clip.py <audio.json> <keeps.json> [render.mp4]

# Layer 2: anchor-keyword semantic
python3 scripts/check_anchor_lap.py <verify.json>

# Nếu Layer 1 FAIL → fix keeps → re-render
# Nếu Layer 2 FAIL → check keep boundary (Pitfall #3) hoặc trim keeps
# Nếu CẢ 2 PASS → "xong" được phép
# Nếu 1 layer PASS, 1 layer FAIL → CHƯA XONG
```

### Anti-patterns VĨNH VIỄN

- ❌ Báo "xong" khi chỉ chạy 1 verify layer
- ❌ "Layer 1 PASS là đủ" — KHÔNG, layer 2 bắt buộc
- ❌ "Skip layer 2 vì clip quen" — KHÔNG
- ❌ "Verify xong cuối ngày" — PHẢI verify ngay sau mỗi render
- ❌ Để 8 clip ship xong mới chạy verify cuối session — quá trễ

### Best practice (áp dụng từ 14/07/2026)

1. **Verify 2 layers NGAY SAU MỖI render** (không batch cuối session)
2. Nếu Layer 2 FAIL vì false positive (anchor trong same keep) → dùng `verify_with_keep_awareness()` từ Pitfall #3
3. Nếu Layer 2 FAIL vì anchor cross keep → chia keeps NHỎ + word-level cut
4. Nếu anchor keywords tự nhiên trong source (anh hay dùng "các bạn"/"chúng ta") → accept PARTIAL_PASS với note giải thích
5. Báo cáo 2 layers trong output (PASS/PASS hoặc PASS/FAIL hoặc FAIL/PASS) — KHÔNG chỉ 1 layer

### Real case 14/07 (sau khi fix)

| Clip | Layer 1 | Layer 2 | Status |
|------|---------|---------|--------|
| 0746 | 2 issues | PASS | PARTIAL_PASS |
| 0747 | 2 filler | PASS | PARTIAL_PASS |
| 0749 | 0 | **PASS (sau V4)** | ✅ FIXED |
| 0751 | 2 | **FAIL (source natural)** | PARTIAL_PASS + skill fix |
| 0752 | 0 | **PASS (sau V2)** | ✅ FIXED |
| 0753 | 2 lap_nghia | PASS | PARTIAL_PASS |
| 0756 | 0 | PASS | ✅ |
| 0758 | 0 | **PASS (sau V5)** | ✅ FIXED |

---

## 🚨 PITFALL #6 (NEW 14/07/2026) — Keep boundaries phải match Whisper segment boundaries

**Ngày phát hiện:** 14/07/2026 (clip 0758 tripod — 3 anchor-lap pairs không fix bằng trim giữ chừng).

### Vấn đề

Khi build keep_plan từ source `audio.json` (Whisper ban đầu), keep boundaries có thể CẮT giữa 2 Whisper verify segments. Trong output, 2 keep liền kề này sẽ có 2 Whisper verify segments chứa anchor keywords → `check_anchor_lap.py` báo FAIL.

**Ngược lại**, khi keep boundaries match EXACTLY Whisper verify segment boundaries → mỗi keep = 1 Whisper verify segment → `check_anchor_lap.py` chỉ flag khi anchor thực sự cross keep boundary.

### Quy tắc BUILD keeps

**Workflow build keep_plan từ Whisper OUTPUT (không phải từ source audio.json):**

```python
# Step 1: Render file V1 từ keep_plan source-based (normal workflow)
# Step 2: Whisper lại file V1 → verify.json (có Whisper segments)
# Step 3: Build keep_plan V2 dựa trên Whisper verify segments (không phải source)
#   - Mỗi keep = 1 Whisper verify segment (hoặc nhiều Whisper segments)
#   - Keep boundaries = exact Whisper verify segment boundaries
# Step 4: Render V2 từ keep_plan V2
# Step 5: Verify 2 layers — sẽ pass vì keep boundaries = Whisper segments
```

### Real case 14/07 clip 0758

**V1 → V3 → V4 đều FAIL Layer 2** (anchor-lap "các bạn" 2 pairs):
- seg 0+1: "giới thiệu với các bạn" → "bình thường các bạn"
- seg 20+21: "Các bạn có thể dùng nó để quay" → "các bạn có thể dùng..."
- seg 31+32: "Các bạn chuẩn bị xe vụ tháng" → "Vậy nên các bạn..."

**V5 PASS Layer 2** bằng cách build keep_plan từ Whisper verify V4 (chứ không phải source):
- Skip seg 0, 21, 31 (chứa anchor keywords đầu/cuối)
- Mỗi keep = 1 Whisper segment
- Keep boundaries align với Whisper verify segments → không có fake boundary trong Whisper output

### Trade-off

**Ưu điểm:** Pass Layer 2 anchor-lap ngay từ keep_plan, không cần trim nhiều lần
**Nhược điểm:** Bỏ một số content có anchor keywords (giảm 5-10% features) — chấp nhận được cho Mode B cô đọng

### Khi nào nên dùng PITFALL #6

- Source có nhiều anchor keywords TỰ NHIÊN (cách nói của anh: "các bạn", "chúng ta" xuất hiện 5+ lần)
- Trim giữ chừng vẫn còn anchor-lap (PITFALL #3 false positive)
- Chấp nhận bỏ 5-10% features để pass Layer 2

### Alternative strategy (PITFALL #6 + verify_with_keep_awareness)

Nếu KHÔNG muốn bỏ features → combine PITFALL #6 với PITFALL #3:
1. Build keep_plan với keeps GHÉP (để giữ features)
2. Dùng `verify_with_keep_awareness()` để phân biệt same-keep vs cross-keep anchor
3. Same-keep anchor = FALSE POSITIVE (accept)
4. Cross-keep anchor = REAL (fix bằng PITFALL #6: skip seg đó)

---

## 🚨 PITFALL #7 (NEW 16/07/2026) — Source-natural anchor keywords = PATTERN, không phải bug

**Ngày phát hiện:** 16/07/2026 — 6 clip edit trong 1 ngày (3 sáng + 3 trưa). Stats: **1/6 SHIP CLEAN, 5/6 PARTIAL_PASS** (anchor keywords tự nhiên).

### Vấn đề

Anh Tuấn Anh nói chuyện với audience theo pattern tự nhiên:
- "**Các bạn**" 5-10 lần / clip (cách xưng hô quen thuộc với audience)
- "**Chúng ta**" 3-5 lần / clip (cách kể chuyện inclusive)
- "**Bởi vì**" 3-5 lần / clip (logic flow)
- "**Vậy**" / "**Nó**" 5+ lần / clip (filler tự nhiên)

Khi áp dụng `check_anchor_lap.py`, Layer 2 báo FAIL vì anchor keywords xuất hiện 2+ lần trong các seg liên tiếp. Nhưng thực tế đây là **SOURCE-LEVEL pattern**, không phải lỗi edit.

### Cách phân biệt SOURCE-LEVEL vs KEEP-BOUNDARY anchor-lap

**Mở Whisper verify transcript**, check từng pair anchor-lap:
- **SOURCE-LEVEL pair**: 2 seg có anchor keyword + seg giữa chúng NẰM TRONG CÙNG 1 KEEP → FALSE POSITIVE, accept PARTIAL_PASS
- **KEEP-BOUNDARY pair**: 2 seg có anchor keyword + seg giữa chúng NẰM Ở 2 KEEP RIÊNG BIỆT → REAL, phải fix (chia keeps NHỎ + word-level cut theo PITFALL #6)

### Quy tắc SHIP Decision Matrix (FIRST-CLASS)

| Layer 1 | Layer 2 | Duration | Decision | Note |
|---------|---------|----------|----------|------|
| 0-2 issues | 0 pairs | 30-130s | ✅ **SHIP CLEAN** | Hiếm với source-natural clips |
| 0-2 issues | 0 pairs | 130-180s | ✅ **SHIP CLEAN** | Accept edge case duration > 130s |
| 0-2 issues | 1-2 SOURCE-LEVEL pairs | 30-130s | ✅ **SHIP PARTIAL_PASS** | Document anchor keywords tự nhiên |
| 0-2 issues | 1-2 SOURCE-LEVEL pairs | 130-180s | ✅ **SHIP PARTIAL_PASS** | Content depth justifies |
| 0-2 issues | 3+ SOURCE-LEVEL pairs | 30-180s | ✅ **SHIP PARTIAL_PASS** | OK nếu content depth justifies (multiple anchor keywords) |
| 3+ issues | Any | Any | ⚠️ FIX THÊM → re-render | |
| 0-2 issues | 1+ KEEP-BOUNDARY pairs | Any | ⚠️ FIX THÊM | Insert keeps or word-level cut |

### Best practice: Pre-edit source-natural anchor detection

**TRƯỚC khi build keeps, đọc Whisper transcript text và identify anchor keywords tự nhiên:**

```python
# Đếm anchor keyword frequency trong source
ANCHOR_KEYWORDS = ['các bạn', 'chúng ta', 'bởi vì', 'vậy', 'nó', 'thì', 'mọi người']
transcript_text = open('transcript_full.md').read()
for kw in ANCHOR_KEYWORDS:
    count = transcript_text.lower().count(kw)
    print(f"  {kw}: {count} lần")
# Nếu anchor > 5 lần → expect PARTIAL_PASS, plan accept ship
```

**EXPECT 1-3 SOURCE-LEVEL anchor-lap pairs** cho mỗi clip 200s+ của anh Tuấn Anh.

### Workflow tối ưu (đã verify 16/07)

**Clip đầu tiên trong batch:** V1-V3 iterate (học pattern)
- 30 phút cho 1 clip (3 versions)
- Document V1-V3 vào keep_plan + analyze anchor pattern

**Clip thứ 2+ trong batch:** 1 attempt (apply pattern)
- 8-10 phút cho 1 clip
- 70% time savings so với clip đầu

### Real case 16/07 batch 2 (3 clip buổi trưa)

| Clip | KEEPS | Final | Speed | Layer 1 | Layer 2 (pairs) | Status |
|------|------|-------|-------|---------|-----------------|--------|
| 0003 | 6 | 89.57s | 1.3x | 8 | 2 SOURCE | ⚠️ PARTIAL_PASS |
| 0004 | 6 | 166.43s | 1.3x | 7 | 1 SOURCE | ⚠️ PARTIAL_PASS + duration > 130s |
| 0005 | 8 | 251.80s | 1.3x | 6 | 3 SOURCE | ⚠️ PARTIAL_PASS + duration > 130s |

**Key learning:** 3 clip buổi trưa = 0 SHIP CLEAN. Pattern từ 3 clip sáng đã học được → drop keeps chứa 3+ anchor keywords + accept PARTIAL_PASS. Time savings: clip 0003 = 15 phút (V1-V3 iterate), clip 0004+0005 = 5-10 phút (1 attempt).

### Khi nào KHÔNG accept PARTIAL_PASS (vẫn phải fix)

- Layer 2 fail vì **KEEP-BOUNDARY** pairs (cross keep) → fix theo PITFALL #6
- Layer 1 fail với 3+ issues không phải anchor → fix keeps (trim filler/treo/lặp)
- Duration > 180s (TikTok hard limit) → trim keeps (giảm nội dung) hoặc speed 1.5x MAX

---

## 🚨 PITFALL #5 (NEW 14/07/2026) — Whisper medium hallucination @ speed 1.3x concat

**Ngày phát hiện:** 14/07/2026 (clip 0731 V5 verify).

### Vấn đề
Khi concat nhiều source segments qua speed 1.3x, Whisper medium model thỉnh thoảng nghe thừa từ — đặc biệt với cụm có keyword liền kề pattern "X và Y":
- Source: "**và nó là 1 đầu hút và 1 đầu thổi**" (seg[17])
- Whisper output: "**Và nó là 1 đầu hút, 1 đầu hút và 1 đầu thổi**" (lặp "1 đầu hút")
- Root cause: speed 1.3x dồn các âm tiết từ 2 source segments liền kề thành 1 nhịp nhanh hơn, Whisper decode sai thành nhân đôi keyword.

### Quy tắc phân biệt vs anchor-lap (Pitfall #1)
- **Anchor-lap REAL**: 2 instance keyword CÓ TRONG nhiều source segments thật → Layer 2 báo FAIL → phải fix keeps
- **Whisper hallucination**: keyword chỉ có 1 lần trong source nhưng Whisper output 2 lần → KHÔNG phải lỗi keep → KHÔNG tái edit

### Cách verify nhanh
Mở source `audio.json`, dùng `grep` text source. Nếu source chỉ có 1 instance keyword mà Whisper verify output có 2 → CHẤP NHẬN, ghi note "Whisper decode artifact @ 1.3x" trong transcript report, KHÔNG fix keep/rerender.

### Real case clip 0731
- Source seg[17]: "và nó là 1 đầu hút và 1 đầu thổi"
- Whisper output seg[10]: "Và nó là 1 đầu hút, 1 đầu hút và 1 đầu thổi"
- Source OK → ghi note, pass.
- Câu này KHÔNG trigger Layer 2 vì "1 đầu hút" không phải anchor keyword.

### Xem thêm
`references/pitfall-success-pattern-clip-0731-v3-v5-fix-2026-07-14.md` — full case study + 3-pattern fix (bỏ keep anchor + trim keep dài + drop CTA trade-off).

---

## 🚨 PITFALL #2 — Source `.MOV` cleaned up sau workflow

**Ngày phát hiện:** 13/07/2026.

`scripts/workflow_edit.sh` chỉ tạo `tmp/<clip>/source.MOV` SYMLINK nếu chưa có, không bao giờ backup. Sau khi render xong, parent cleanup xóa `tmp/<clip>/source.MOV` (chỉ giữ `audio.json/wav` + `keeps.json`). Nếu sau đó cần V2 re-render, **KHÔNG CÒN source để trím**.

**Fix bắt buộc cho V2 workflow:**
1. Trước khi bắt đầu V2, `find` source gốc dựa trên `audio.wav` duration (±2s tolerance) trong: `/Volumes/Storage-1/Pocket3/Hermes-Edit/`, `iPhone Sources/`, `Footages/`, `tmp/legacy-sources-*`, `tmp/C0XX/source.MOV`.
2. Nếu không tìm được: log warning rõ ràng, KHÔNG tự ý dùng source khác duration.
3. Alternative: yêu cầu parent `ln -s` lại source trước khi fix.

---

## 🚨 PITFALL #9 (NEW 18/07/2026) — Motion verify trên source DARK ≠ FREEZE frame (dual-signal detector)

**Ngày phát hiện:** 18/07/2026 (clip 0006 ngạc tripod diverse-motion verify).

### Vấn đề

DJI Pocket 3 quay trong điều kiện ánh sáng yếu → frame mean RGB < 30 → nền đen chiếm đa số pixel. Khi dùng `pixel-diff` với **threshold mặc định 15** (chuẩn chống JPEG noise), gần như MỌI cặp frame trả về `<1% changed pixels` → dễ kết luận nhầm "freeze frame" trong khi source có camera motion thật nhưng contrast thấp.

**Real case clip 0006 diverse-motion verify:**
- Source DJI 190.9s, thiếu sáng, mean RGB ≈ 25 (rất tối)
- Pixel-diff threshold 15: 21/21 windows đều <5% → kết luận SAI "freeze toàn clip"
- Mean RGB delta: 18/21 windows có Δ > 0.05 (mean) hoặc ≥1.6 tại fade-in/fade-out → CÓ motion thật
- Vision check frame tại 75s: hiện overlay "Bước 2: Bỏ vô + nhấn xuống" → text animation, không phải freeze

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Khi verify motion cho video có source DJI / GoPro / iPhone quay thiếu sáng (mean RGB < 50), LUÔN dùng dual-signal motion detector — KHÔNG dùng pixel-diff threshold 15 đơn lẻ:**

```python
# Snippet dùng cho verify motion (paste vào Python sau khi extract 22+ frames mỗi 5s)
from PIL import Image, ImageChops, ImageStat

def pixel_diff_pct(p1, p2, thresh=5):  # ← threshold 5 thay vì 15
    a = Image.open(p1).convert('RGB')
    b = Image.open(p2).convert('RGB')
    if a.size != b.size:
        b = b.resize(a.size)
    diff = ImageChops.difference(a, b).convert('L')
    px = list(diff.getdata())
    return sum(1 for p in px if p > thresh) / len(px) * 100

def mean_rgb_delta(p1, p2):
    s1 = ImageStat.Stat(Image.open(p1).convert('RGB')).mean
    s2 = ImageStat.Stat(Image.open(p2).convert('RGB')).mean
    return sum(abs(s1[i] - s2[i]) for i in range(3)) / 3

# Verdict: MOVING nếu (pixel_diff ≥ 5%) HOẶC (mean ΔRGB ≥ 3)
moving = (pixel_diff_pct(a, b) >= 5) or (mean_rgb_delta(a, b) >= 3)
```

### Phase-by-phase matrix (BẮT BUỘC cho diverse-motion clip)

Với clip diverse-motion 8-phase, **phải** verify motion theo phase boundaries (HOOK/PROBLEM/INTRO/FEATURE/DEMO/COMPARE/PROOF/CTA), không chỉ overall average:

| Phase | Window | Expected Motion | Verdict |
|---|---|---|---|
| HOOK | 0-4s | fade-in mạnh (ΔRGB ≥ 1.0) | PASS nếu ΔRGB ≥ 1.0 |
| PROBLEM | 4-18s | camera shake nhẹ + text overlay | MARGINAL OK |
| INTRO | 18-32s | peak motion (peak Pdiff ≥ 10%) | PASS nếu peak ≥ 8% |
| FEATURE | 32-46s | text overlay "Bước 1/2/3" | MARGINAL OK |
| DEMO | 46-60s | tay cầm sản phẩm | PASS nếu Pdiff ≥ 5% |
| COMPARE | 60-74s | so sánh slow-mo | MARGINAL OK |
| PROOF | 74-88s | peak motion (peak Pdiff ≥ 10%) | PASS nếu peak ≥ 8% |
| CTA | 88-110s | scene change lớn + "Bấm link mua ngay" | PASS nếu ΔRGB ≥ 1.0 |

**Rule:** ≥4/8 phase PASS mới SHIP. 1-3 phase LOW + ≥18/21 motion windows ≥5% = CONDITIONAL PASS.

### Anti-patterns VĨNH VIỄN

- ❌ Dùng `pixel-diff threshold 15` (mặc định chống JPEG noise) cho source dark → false freeze
- ❌ Kết luận "freeze frame" khi pixel-diff <1% mà KHÔNG check mean RGB delta
- ❌ Bỏ qua text overlay animation (Bước 1/2/3, Bấm link) khi đánh giá diverse motion
- ❌ Verify motion overall average mà KHÔNG phase-by-phase cho clip 8-phase
- ❌ Dùng ffprobe `-vf cropdetect` / `mpdecimate` — không phân biệt được dark source + motion

### Real case 18/07 clip 0006 diverse-motion verify

| Method | Threshold | 21 windows | Verdict |
|---|---|---|---|
| pixel-diff | 15 (default) | 21/21 < 5% | ❌ FALSE "freeze" |
| pixel-diff | 5 (relax) | 18/21 ≥ 5% | ✓ MOVING majority |
| mean RGB Δ | (always) | 6/21 ≥ 0.5 (scene changes) | ✓ scene changes detected |
| **DUAL-SIGNAL** | **5 OR Δ≥3** | **18/21 MOVING** | **✓ CORRECT verdict** |

### Tool reusable: `scripts/verify_motion.py`

Dùng cho MỌI diverse-motion clip verify — chạy standalone hoặc tích hợp vào `verify_clip.py`:

```bash
python3 scripts/verify_motion.py <video.mp4> [--frames 22] [--interval 5] [--phases 8]
# Output: phase-by-phase matrix + dual-signal verdict
```

### Xem thêm

`references/pitfall-motion-verify-dark-source-2026-07-18.md` — transcript đầy đủ + repro case + dual-signal algorithm.

---

## 🚨 PITFALL #10 (NEW 18/07/2026) — Layer 3 FALSE START scan (gap < 10s + 5+/8 first-word match)

**Ngày phát hiện:** 18/07/2026 (clip 0007 KNF carbon fiber bộ vệ sinh — first time ran Layer 3 scan explicitly per user brief "verify false start + lặp câu + filler").

**Nguồn gốc:** Từ `tiktok-video-editor` skill v3.24.0 PITFALL #21 (Layer 3 FALSE START scan) — đã được phát hiện trong real case clip 0003 V1 ngày 17/07 (2 HOOK lặp 11 từ + 7 từ). Layer 1 + Layer 2 của verify-protocol KHÔNG catch được case này → cần Layer 3 riêng.

### Vấn đề

Khi edit xong, nếu em chỉ chạy:
- Layer 1: `scripts/verify_clip.py` (5-dim strict — FILLER/TREO/LẶP NGHĨA/HOOK LẶP/ỰM_Ỡ)
- Layer 2: `scripts/check_anchor_lap.py` (anchor-keyword semantic)

→ KHÔNG đủ. Cả 2 layers đều check pattern lặp **trong** transcript, không check **take cũ + take mới cùng tồn tại** ở 2 segments LIỀN KỀ (gap < 10s). Đây là failure mode riêng của edit: em cắt giữa 2 take và quên bỏ take cũ.

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Sau khi Layer 1 + Layer 2 PASS, PHẢI chạy Layer 3 FALSE START scan:**

```python
import json
with open("verify.json") as f:
    segments = json.load(f)["segments"]
candidates = []
for i in range(len(segments) - 1):
    seg_i = segments[i]
    seg_j = segments[i + 1]
    gap = seg_j["start"] - seg_i["end"]
    if gap > 10:
        continue
    words_i = seg_i["text"].strip().split()[:8]
    words_j = seg_j["text"].strip().split()[:8]
    match = sum(1 for a, b in zip(words_i, words_j) if a == b)
    if match >= 5:
        candidates.append({
            "seg_old": i, "seg_new": i+1, "gap": gap, "match": match,
            "old_text": seg_i["text"], "new_text": seg_j["text"]
        })
# Nếu candidates > 0 → FALSE START detected (HOẶC parallel-reason — xem PITFALL #11)
```

### RMS CHECK FIRST 3s — catch silent take cũ

Khi Layer 3 phát hiện candidate, PHẢI check RMS first 3s của clip:

```bash
ffmpeg -i verify.wav -t 3 -af "volumedetect" -f null - 2>&1 | grep "mean_volume"
# Nếu RMS < -50 dB ở first 3s → likely silent take cũ (false start)
# Real case 17/07: clip 0003 first 3s RMS = -61 dB (gần silent) → seg 0 suspect.
```

### Workflow fix khi phát hiện

1. **Cut range**: `[seg_old.start - 0.3s → seg_new.start + 0.3s]` (padding 0.3s để tách hẳn)
2. **Re-render** → Whisper lại → re-scan false start protocol
3. **Nếu 3 lần fail liên tiếp**: re-build keep_plan từ SOURCE transcript (Pitfall #24 tiktok-video-editor)

### Anti-pattern VĨNH VIỄN

- ❌ Chỉ tin Layer 1 + Layer 2 PASS mà KHÔNG scan Layer 3 → miss false start
- ❌ Giữ CẢ take cũ + take mới vì "nghe cả 2 đều hay" → giọng đọc lặp
- ❌ Cắt lệch keep boundary → tạo jump cut giữa câu

### Khi KHÔNG phải false start (xem PITFALL #11)

- Match 4 từ = connector tự nhiên (KHÔNG đủ signature)
- Gap > 10s = true anchor tự nhiên (PITFALL #7 cover)
- Text khác phần sau = parallel-reason rhetorical structure (xem PITFALL #11 bên dưới)

### Tool tích hợp: `scripts/verify_clip_full.py`

Layer 4 của tool này implement sẵn protocol trên. Chạy 1 lệnh → full 7 layers:

```bash
python3 ~/.hermes/skills/media/tiktok-verify-protocol/scripts/verify_clip_full.py \
  /path/to/clip.mp4 \
  --source /path/to/source.mp4 \
  --report /path/to/report.md
# Output: SHIP CLEAN / PARTIAL PASS / FAIL + verdict + recommended action
```

### Real case 18/07 clip 0007 KNF carbon fiber

- Layer 3 phát hiện 1 candidate: seg 21↔22, gap=0.00s, match=5/8 ("Bởi vì những cái...này")
- Phân tích kỹ: 5 từ đầu "Bởi vì những cái...này" là **connector scaffolding** (Bởi vì + demonstrative), content phần sau phân kỳ rõ ("vết suốt" vs "hạt bụi") → **parallel-reason rhetoric, KHÔNG phải false start**
- RMS first 3s = -26.6 dB (audible, không silent take cũ)
- → PASS PITFALL #10 với flag PITFALL #11 false positive
- → Xem PITFALL #11 bên dưới để hiểu false positive trap

### Xem thêm

- `references/lesson-2026-07-18-verify-clip-0007.md` — full transcript verify clip 0007 với 7 layers chi tiết + 3-keep detection workflow
- `tiktok-video-editor` skill v3.24.0 PITFALL #21 references — protocol đầy đủ + Python detection script

---

## 🚨 PITFALL #11 (NEW 18/07/2026) — Parallel-reason rhetorical structure FALSE POSITIVE cho PITFALL #10

**Ngày phát hiện:** 18/07/2026 (clip 0007 KNF carbon fiber — flag candidate seg 21↔22 match=5/8 phân tích chi tiết).

### Vấn đề

Vietnamese speakers dùng **liên từ nhân-quả song song** cực kỳ phổ biến trong narration:
- "**Bởi vì** A... **Bởi vì** B..." (vì lý do A, vì lý do B)
- "**Thì** X... **thì** Y..." (thì X, thì Y)
- "**Vậy nên** P... **vậy nên** Q..." (do đó P, do đó Q)
- "**Tuy nhiên** U... **tuy nhiên** V..." (tuy nhiên U, tuy nhiên V)
- "**Do đó** M... **do đó** N..." (do đó M, do đó N)

Khi scan FALSE START Layer 3 (PITFALL #10) với threshold 5+/8 từ đầu giống → 5 từ đầu giống có thể là **3-4 connector scaffolding words** + **1-2 demonstrative filler** ("những cái...này"). Phần content thực sự (sau connector) PHÂN KỲ rõ rệt → KHÔNG phải false start take-retry, mà là **discourse marker + parallel enumeration**.

### Heuristic phân biệt FALSE START vs PARALLEL-REASON

```python
# Scan FALSE START Layer 3 — phát hiện candidate
candidates = []  # như PITFALL #10

# Phân loại candidate
CONNECTOR_SCAFFOLDING = {
    "bởi", "vì", "thì", "vậy", "nên", "tuy", "nhiên", "do", "đó",
    "bởi vì", "vì vậy", "do đó", "vậy nên", "tuy nhiên", "cho nên"
}
DEMONSTRATIVE_FILLER = {"những", "cái", "con", "chiếc", "cây", "đó", "này"}

def classify_false_start(candidate):
    old_words = candidate["old_text"].strip().split()[:8]
    new_words = candidate["new_text"].strip().split()[:8]
    
    # Đếm số từ đầu là connector scaffolding
    n_connector_old = sum(1 for w in old_words if w.lower() in CONNECTOR_SCAFFOLDING)
    n_connector_new = sum(1 for w in new_words if w.lower() in CONNECTOR_SCAFFOLDING)
    
    # Lấy phần content SAU connector scaffold (skip 3 từ đầu nếu là connector)
    content_old = old_words[3:] if n_connector_old >= 2 else old_words[2:]
    content_new = new_words[3:] if n_connector_new >= 2 else new_words[2:]
    
    # Check content phân kỳ (signature of parallel-reason)
    content_match = sum(1 for a, b in zip(content_old, content_new) if a == b)
    content_total = min(len(content_old), len(content_new))
    
    # Nếu content match < 50% → parallel-reason, KHÔNG phải false start
    if content_total > 0 and content_match / content_total < 0.5:
        return "PARALLEL_REASON (FALSE POSITIVE - accept SOURCE-NATURAL)"
    return "FALSE_START (REAL - cần fix keep boundary)"
```

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Khi Layer 3 phát hiện candidate, TRƯỚC KHI flag FALSE START, phải chạy classify:**
1. Nếu ≥2 từ đầu ∈ CONNECTOR_SCAFFOLDING ("bởi vì", "thì", "vậy nên"...) → nghi ngờ parallel-reason
2. Check content SAU connector (skip 2-3 từ đầu) có phân kỳ không
3. **Nếu content phân kỳ ≥50%** → FALSE POSITIVE, accept SOURCE-NATURAL (Pitfall #7)
4. **Nếu content giống ≥50%** (cả phần sau) → REAL FALSE START, fix keep boundary

### Anti-pattern VĨNH VIỄN

- ❌ Match 5/8 → tự động flag FALSE START mà KHÔNG check content phân kỳ
- ❌ Trim 1 trong 2 segments "vì lặp" → mất narrative flow + discourse marker
- ❌ Insert gap 2-3s giữa 2 segments vì "nghe gần giống" → unnatural pacing

### Real case 18/07 clip 0007 KNF carbon fiber

- Candidate seg 21↔22, gap=0.00s, match=5/8
- Old: "**Bởi vì** những cái **vết suốt này** trung vi nó khá nhỏ"
- New: "**Bởi vì** những cái **hạt bụi này** chúng ta không nhìn thấy..."
- Connector scaffolding: "Bởi vì" (1 từ) + "những cái" (2 từ demonstrative) = 3 từ đầu là connector/filler
- Content phân kỳ từ từ thứ 4: "vết suốt" vs "hạt bụi" → 0/5 match trong content
- **Verdict: PARALLEL_REASON FALSE POSITIVE — KHÔNG fix**
- Whisper transcripts gốc cũng confirm: speaker đang giải thích "vì vết xước nhỏ + vì hạt bụi không thấy được" = 2 lý do song song hoàn toàn tự nhiên

### Tool tích hợp

`scripts/verify_clip_full.py` Layer 4 in DUMP candidate raw (chưa classify) → user verify thủ công hoặc chạy classify script riêng. Future version sẽ integrate classify trực tiếp vào Layer 4.

### Xem thêm

- `references/lesson-2026-07-18-verify-clip-0007.md` — transcript chi tiết clip 0007 với classify workflow + 7-layer output table

---

## 🚨 PITFALL #8 (NEW 18/07/2026) — Verify motion pixel diff ở vùng KHÔNG có glass overlay

**Ngày phát hiện:** 18/07/2026 (clip 0003 Dodoto Lux Air V3 motion graphic V4/V5/V6 verify).

### Vấn đề

Khi verify motion cho video motion graphic (có glass overlay + GSAP animation), nếu em so sánh pixel diff ở **vùng có glass overlay**, motion sẽ LUÔN cao (vì GSAP animate opacity/y/scale của glass) → em kết luận "motion OK" trong khi **background video thực sự STATIC**.

**Real case clip 0003 V5:** Em check pixel diff 0.5s vs 5s = 17,914 ở vùng `y=100-600` (CÓ chứa glass animation) → em báo "✅ MOTION" → nhưng thực tế video gốc (talking head clip_0003) gần như static. Khi check lại ở vùng **KHÔNG có glass**, diff chỉ 85-443 = STATIC.

**Real case V22 verified PASS (contrast):** Source sac-du-phong-mini-iphone = talking head có motion thật. Pixel diff 0.5s vs 1.5s = 36,203 → V22 work vì source có motion. V6 fail vì clip 0003 source gần như static.

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Khi verify motion cho video motion graphic, LUÔN so sánh pixel diff ở vùng KHÔNG CÓ GLASS OVERLAY:**

```python
from PIL import Image

# Frame ở thời điểm KHÁC NHAU
img_t1 = Image.open('frame_t1.jpg')
img_t2 = Image.open('frame_t2.jpg')

# ✅ VÙNG ĐÚNG: chỉ check top area (Y=100-500) - nơi KHÔNG có glass phase thường
diff_clean = 0
for x in range(100, 980, 50):
    for y in range(100, 500, 50):  # TOP HALF - NO GLASS
        diff_clean += sum(abs(a-b) for a, b in zip(img_t1.getpixel((x,y)), img_t2.getpixel((x,y))))

# ❌ VÙNG SAI: check vùng glass (Y=1288-1500) - sẽ luôn có diff do GSAP animation
diff_dirty = 0
for x in range(100, 980, 50):
    for y in range(1300, 1500, 50):  # BOTTOM - HAS GLASS OVERLAY
        diff_dirty += sum(abs(a-b) for a, b in zip(img_t1.getpixel((x,y)), img_t2.getpixel((x,y))))

# QUY TẮC:
# diff_clean > 5000 = source video thực sự có motion → MOTION OK
# diff_clean < 500 = source video STATIC → báo cáo trung thực "clip source không có motion nhiều"
# diff_dirty > diff_clean * 1.5 = có GSAP animation (motion giả) → KHÔNG tính là motion
```

**Quy tắc áp dụng:**
1. **ALWAYS** check vùng TOP (Y=100-500) hoặc vùng KHÔNG có glass trong bất kỳ phase nào
2. **NEVER** báo "motion OK" chỉ dựa trên diff toàn frame
3. **BÁO CÁO TRUNG THỰC** khi source clip talking head ít motion — chấp nhận, không cố fake bằng animation
4. **VERIFY bằng mắt thật** extract frame từ final MP4 (KHÔNG chỉ dựa vào silent overlay render)

### Anti-patterns VĨNH VIỄN

- ❌ So sánh pixel diff ở vùng có glass overlay → motion giả từ GSAP
- ❌ Báo "video motion OK" chỉ dựa trên diff toàn frame
- ❌ Bỏ qua fact "source clip talking head gần như static" khi source thực tế không có motion
- ❌ Dùng `tl.call(() => video.play())` để force play trong GSAP → vẫn không work headless (Pitfall 52)

### Real case 18/07 clip 0003 motion verify

| Version | Pixel diff (vùng clean) | Motion thực | Status |
|---|---|---|---|
| V5 final (ffmpeg overlay) | 85-443 (vùng TOP) | **Source gần như STATIC** | ⚠️ Em báo sai "motion OK" |
| V5 final (vùng glass) | 17,914 (Y=1308) | GSAP animation giả | ❌ Verify SAI vùng |
| V6 silent (HyperFrames) | 0-1500 (vùng TOP) | Render chỉ 1 frame tĩnh | ❌ Headless video không play |

**Kết luận đúng:** clip 0003 source gần như static (talking head ít motion). Em PHẢI báo cáo trung thực, không fake verify bằng pixel diff ở vùng glass.

### Xem thêm

- `references/pitfall-verify-motion-pixel-diff-clean-zone-2026-07-18.md` (TODO nếu cần — transcript đầy đủ + repro)
- Skill `tiktok-product-motion-graphics` Pitfall 51-53 (clip 0003 V4/V5/V6 chain)
- Skill `tiktok-product-motion-graphics` Pitfall 52 (HyperFrames headless video trap)

---

## 🚨 PITFALL #12 (NEW 18/07/2026) — Enumeration pattern FALSE POSITIVE cho HOOK LẶP Layer 1

**Ngày phát hiện:** 18/07/2026 (clip 0005 V2 máy phun tinh dầu LED RGB — verify nhanh chỉ 5 lỗi narrative + FALSE START, 1 cặp hook-lặp candidate #10/#11 "chế độ thứ nhất / chế độ thứ hai").

**Nguồn gốc:** Real case 18/07 clip 0005 V2 — speaker enumeration 4 chế độ phun (5/10/20 phút + liên tục) với head-3 identical "chế độ thứ". User explicit: "Verify nhanh clip 0005 NEW V2 - chỉ check 5 lỗi narrative + FALSE START. Không verify motion, không verify audio." — scope-narrowed verify workflow first time xuất hiện rõ ràng.

### Vấn đề

Vietnamese product narration hay dùng **enumeration pattern** để liệt kê tính năng:
- "**chế độ thứ nhất** là X, **chế độ thứ hai** là Y, **số 3** là Z, **số 4** là W" (4 modes)
- "**tính năng 1** là A, **tính năng 2** là B, **tính năng 3** là C" (3 features)
- "**bước 1** X, **bước 2** Y, **bước 3** Z" (3 steps)
- "**loại 1**, **loại 2**, **loại 3**" (3 categories)
- "**điểm cộng thứ nhất**, **điểm cộng thứ hai**..." (pros enumeration)

Khi scan HOOK LẶP Layer 1 (3+ từ đầu giống liên tiếp), 2-3 segment liên tiếp có cùng enumeration prefix → script flag HOOK LẶP. NHƯNG phần content SAU prefix PHÂN KỲ rõ rệt (5 phút vs 10 phút vs 20 phút vs liên tục) → enumeration có chủ đích, KHÔNG phải lặp nghĩa hay take-retry. Đây là failure mode RIÊNG của product narration Mode B template (PITFALL #25 9-keep Problem→Solution).

### Heuristic phân biệt ENUMERATION vs LẶP NGHĨA / TAKE-RETRY

```python
ENUMERATION_PREFIXES = {
    "chế độ thứ", "chế độ số",       # modes: 5/10/20 phút + liên tục
    "tính năng", "feature",            # USP liệt kê
    "bước",                            # step-by-step
    "loại", "kiểu",                    # variants
    "điểm cộng", "điểm trừ",          # pros/cons
    "ưu điểm", "nhược điểm",          # pros/cons
    "lý do thứ", "lý do số",          # reasons enumeration
    "cách thứ", "cách số",            # methods
    "trường hợp", "case",              # use cases
}

def classify_hook_lap(seg_i_text, seg_j_text):
    """Return ENUMERATION (FALSE POSITIVE) hoặc REAL_HOOK_LAP"""
    words_i = seg_i_text.strip().split()[:3]
    words_j = seg_j_text.strip().split()[:3]
    head = ' '.join([w.lower() for w in words_i])

    # Check xem head-3 có thuộc enumeration prefix không
    is_enum = any(head.startswith(p) for p in ENUMERATION_PREFIXES)
    if not is_enum:
        return "REAL_HOOK_LAP (cần fix)"

    # Check content SAU prefix có phân kỳ không (5 từ đầu sau prefix)
    prefix_word_count = len(head.split())
    content_i = ' '.join(seg_i_text.split()[prefix_word_count:][:5]).lower()
    content_j = ' '.join(seg_j_text.split()[prefix_word_count:][:5]).lower()
    words_content_i = content_i.split()
    words_content_j = content_j.split()
    content_match = sum(1 for a, b in zip(words_content_i, words_content_j) if a == b)

    # Nếu content KHÁC nhau ≥2 từ trong 5 từ đầu → enumeration, KHÔNG phải lặp
    if len(words_content_i) >= 2 and len(words_content_j) >= 2 and content_match < 2:
        return "ENUMERATION (FALSE POSITIVE - accept SOURCE-NATURAL)"
    return "REAL_HOOK_LAP (cần fix)"
```

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Khi Layer 1 HOOK LẶP phát hiện candidate, TRƯỚC KHI flag FAIL, phải check enumeration prefix:**

1. Lấy head-3 của 2 segments
2. Check xem head-3 có match với `ENUMERATION_PREFIXES` không
3. **Nếu CÓ** → check content phần sau prefix phân kỳ ≥2 từ khác nhau trong 5 từ đầu → **ENUMERATION (FALSE POSITIVE — accept)**
4. **Nếu KHÔNG** (head-3 không phải enumeration prefix) → REAL HOOK LẶP, fix keeps
5. **Nếu CÓ enumeration prefix** nhưng content giống ≥2 từ trong 5 từ đầu → REAL HOOK LẶP (take-retry hoặc anchor lặp)

### Anti-pattern VĨNH VIỄN

- ❌ Flag HOOK LẶP khi head-3 = "chế độ thứ" mà KHÔNG check enumeration pattern
- ❌ Trim 1 trong 2 enumeration segments → mất thông tin (vd mất chế độ phun thứ 2)
- ❌ Insert gap/implicit silence giữa 2 enumeration segments → nghe giả tạo
- ❌ Skip vì "chắc là feature enumeration" mà KHÔNG verify content phân kỳ → pass false HOOK LẶP

### Scope-narrowed verify workflow (NEW 18/07/2026)

User instruction 18/07 cho clip 0005 V2: *"Verify nhanh clip 0005 NEW V2 - chỉ check 5 lỗi narrative + FALSE START. Không verify motion, không verify audio."*

Đây là **scope-narrowed verify pattern** (KHÔNG chạy full 7-layer protocol mà chỉ check 1 subset theo user chỉ định):
- **Layer 1** (5-dim strict): BẮT BUỘC chạy theo scope
- **Layer 3** (FALSE START): BẮT BUỘC chạy theo scope (user explicit + false start cross-cuts narrative)
- **Layer 2, 4, 5, 6, 7** (anchor-lap, RMS, audio delta, motion, spec): SKIP theo scope (user explicit "không verify motion, không verify audio")
- **Báo cáo PHẢI mở đầu**: "**Scope**: [scope list]" để user biết em chỉ check phạm vi được yêu cầu, KHÔNG mở rộng

### Real case 18/07 clip 0005 V2 (máy phun tinh dầu LED RGB) — CLEAN PASS

**Scope**: 5 lỗi narrative + FALSE START (motion + audio SKIP per user instruction)

| Check | Result | Notes |
|---|---|---|
| TikTok spec | ✅ PASS | 1080×1920, H.264, AAC 44100Hz, 119.65s Mode B (context only) |
| FILLER (ơ/ờ/ừm/ừ/ó/à/á) | ✅ 0 hits | |
| TREO 3+ từ | ✅ 0 hits | |
| LẶP NGHĨA 2+ | ✅ 1 intentional enumeration (#10/#11) | CHẾ ĐỘ PATTERN — 4 chế độ liệt kê |
| HOOK LẶP 3+ | ✅ 1 same enumeration (pass enumeration rule) | |
| ỰM Ỡ | ✅ 0 hits | |
| FALSE START Layer 3 | ✅ 0 hits | no "nãy", no echo 5-gram, no take-restart |

**CHẾ ĐỘ PATTERN** (4 modes intentional, PITFALL #12 enumeration):
- seg 9 (28.20-30.42s): "kiểu nó có **4 chế độ**"
- seg 10 (30.42-33.52s): "**chế độ thứ nhất** là 5 phút một lần"
- seg 11 (33.52-36.40s): "**chế độ thứ hai** là 10 phút một lần"
- seg 12 (36.40-41.46s): "**chế độ số 3** là 20 phút một lần"
- seg 13 (41.46-44.38s): "**chế độ số 4** là phun liên tục"

→ 4 chế độ liệt kê TUẦN TỰ, content phân kỳ rõ (5/10/20 phút/liên tục). Đây là enumeration **CÓ CHỦ ĐÍCH** từ speaker + Mode B 9-keep template (#25) — KHÔNG phải lỗi edit.

**VERDICT**: **PASS — SẴN SÀNG XUẤT BẢN** ✅

### Tool tích hợp (next version)

`scripts/verify_clip_full.py` Layer 2 (5-dim strict) hiện scan HOOK LẶP raw → cần update để integrate `classify_hook_lap()` từ PITFALL #12 (parallel với `classify_false_start()` từ PITFALL #11). Version tiếp theo sẽ integrate. Cho đến khi integrate, manual verification vẫn cần check enumeration pattern khi candidate xuất hiện.

### Xem thêm

- `references/lesson-2026-07-18-verify-clip-0005-V2-clean-pass.md` — **TODO** full transcript verify clip 0005 V2 với CHẾ ĐỘ PATTERN phân tích + scope-narrowed verify workflow. Reference file này sẽ được tạo trong session tiếp theo nếu cần reproduce workflow.
- User instruction 18/07 verbatim: "Verify nhanh clip 0005 NEW V2 - chỉ check 5 lỗi narrative + FALSE START. Không verify motion, không verify audio." — scope-narrowed verify pattern lần đầu xuất hiện rõ ràng trong task description.

---

## 🚨 PITFALL #13 (NEW 18/07/2026) — Whisper near-zero-duration ghost segments FALSE POSITIVE cho LẶP NGHĨA + HOOK LẶP

**Ngày phát hiện:** 18/07/2026 (clip 0004 Doroto Air Luxe V3 — segments 29 & 30 có duration ≈ 0 và text identical tạo LẶP NGHĨA + HOOK LẶP false positive).

### Vấn đề

Khi Whisper (mlx_whisper medium) gặp **silent gap ~0.3s** giữa 2 keep thật trong clip Mode B cô đọng, model **hallucinate** 1-2 ghost segments:
- Duration ≈ 0 (seg.end ≈ seg.start, thường cả 2 đầu đều ở 1 timestamp)
- 2 segments liên tiếp có text IDENTICAL hoặc near-identical
- Cả 2 đều có word probability thấp (0.04-0.50 cho nhiều từ)
- Word-level timestamps cho tất cả từ đều bằng nhau (= timestamp cuối seg trước)

**Real case clip 0004:**
- Seg 28 (127.88-130.92s) **REAL**: "Các bạn có thể thổi bụi trong những cái nhỏ ra xong bắt đầu dùng đầu hút để hút"
- Seg 29 (130.92-130.94s) **GHOST**: "Các bạn có thể thổi bụi trong cái khu vực nhỏ này nè, các bạn có thể thổi bụi trong cái khu vực nhỏ này nè" (text 2 lần, duration 0.02s, tất cả word timestamps = 130.94)
- Seg 30 (130.94-131.00s) **GHOST**: cùng text với seg 29, duration 0.06s
- Seg 31 (131.24-138.24s) **REAL**: "Đây là cái đầu để bom phao nè…"

**Phantom hits tạo ra nếu KHÔNG filter:**
- LẶP NGHĨA #2: seg 29 ↔ seg 30 (head_match=3, tail_match=3) — **FP**
- HOOK LẶP #2: seg 28 → seg 29 (head_match=3) — **FP** (vì seg 28 = real, seg 29 = ghost)
- HOOK LẶP #3: seg 29 → seg 30 (head_match=3) — **FP** (cả 2 ghost)

→ 3 hits false positive từ cùng 1 ghost cluster. Real hits chỉ còn 1 (PAIR A) sau filter.

### Heuristic phát hiện ghost segment

```python
def is_ghost_seg(seg):
    """Whisper ghost segment nếu duration ≈ 0 HOẶC word timestamps đồng nhất."""
    dur = seg["end"] - seg["start"]
    if dur < 0.5:  # sub-half-second
        return True
    if "words" in seg and seg["words"]:
        # Check timestamps equality
        timestamps = [round(w["end"], 2) for w in seg["words"]]
        unique_ts = len(set(timestamps))
        # Nếu ≤ 2 unique end timestamps trong ≥ 5 từ → hallucination
        if len(timestamps) >= 5 and unique_ts <= 2:
            return True
    return False

def filter_ghosts(segments):
    return [s for s in segments if not is_ghost_seg(s)]
```

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**SAU khi scan LẶP NGHĨA / HOOK LẶP, PHẢI filter ghost segments trước khi flag fail:**

1. Detect ghost seg với 1 trong 3 dấu hiệu:
   - `seg.end - seg.start < 0.5s` (duration gần 0)
   - Word timestamps tất cả bằng nhau (≤ 2 unique timestamps) cho ≥5 từ
   - Avg word probability < 0.5 (model uncertainty)
2. Filter **CẢ 2** segments liên quan nếu 1 trong 2 là ghost
3. Chỉ tính LẶP NGHĨA / HOOK LẶP trên segments KHÔNG phải ghost
4. Trong báo cáo PHẢI ghi rõ "X hits = REAL, Y hits = FP (whisper ghost @ timestamp)"

### Anti-pattern VĨNH VIỄN

- ❌ Flag LẶP NGHĨA / HOOK LẶP khi 1 trong 2 segs có duration < 0.5s mà KHÔNG check ghost
- ❌ Trim 1 trong 2 ghost segments "vì lặp" → không có audio thật để trim
- ❌ Re-render để fix ghost → ghost là Whisper artifact, không có trong source audio
- ❌ Trust `verify_clip.py` strict output cho ghost segments → strict script cũng flag nhầm

### Real case clip 0004 (sau khi áp dụng filter)

| Pair | Initial verdict | After filter | Action |
|---|---|---|---|
| seg 1 (10.56s) ↔ seg 2 (14.62s) "Đây là mẫu" | HOOK LẶP + LẶP NGHĨA | **REAL** (PAIR A) | Cần fix keep |
| seg 28 (127.88s) → seg 29 (130.92s) | HOOK LẶP | **FP (ghost seg 29)** | Skip |
| seg 29 (130.92s) ↔ seg 30 (130.94s) | LẶP NGHĨA + HOOK LẶP | **FP (cả 2 ghost)** | Skip |

→ Sau filter: chỉ còn **1 REAL hit (PAIR A)**. Báo cáo đúng → 1 action duy nhất (cut 1 take PAIR A).

### Tool tích hợp (next version)

`scripts/verify_clip_full.py` Layer 2 (5-dim strict) hiện scan LẶP NGHĨA / HOOK LẶP raw → cần update để integrate `is_ghost_seg()` filter từ PITFALL #13. Version tiếp theo sẽ integrate. Cho đến khi integrate, manual verification vẫn cần check ghost pattern khi candidate duration < 0.5s xuất hiện.

### Xem thêm

- `references/lesson-2026-07-18-verify-clip-0004.md` — transcript chi tiết clip 0004 Doroto Air Luxe V3 verify với 3 ghost segments @ 130.92-131.00s phân tích + PAIR A/PAIR B manual suspect workflow.

---

## 🚨 PITFALL #14 (NEW 18/07/2026) — Manual suspect pair verification workflow

**Ngày phát hiện:** 18/07/2026 (clip 0004 Doroto Air Luxe V3 — user explicit flag 2 cặp suspect phrase "Đây là mẫu" + "Cục binh 4000mAh", verify từng cặp độc lập).

### Vấn đề

User có thể explicit flag K cặp phrase suspect (e.g. "PAIR A: 'Đây là mẫu' + PAIR B: 'Cục binh 4000mAh'") → em phải verify từng cặp độc lập với transcript rồi phân loại kết quả theo 4 verdict enum:

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

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Khi user explicit flag K cặp suspect phrase trong instruction:**

1. Verify TỪNG cặp độc lập (KHÔNG gộp chung)
2. Phân loại verdict enum (BOTH_IN_CUT / TAKE_NEW_ONLY / TAKE_OLD_ONLY / NEITHER)
3. Báo cáo PHẢI list timestamp + text cho từng take để user verify thủ công nếu cần
4. Action đề xuất cho mỗi cặp:
   - BOTH_IN_CUT: "Cut [take cũ hoặc mới] tại [timestamp]" — mặc định recommend cắt TAKE MỚI (giữ TAKE CŨ có USP đầy đủ hơn)
   - TAKE_NEW_ONLY / TAKE_OLD_ONLY: "None — đã xử lý đúng"
   - NEITHER: "Content thiếu — kiểm tra keeps.json"

### Anti-pattern VĨNH VIỄN

- ❌ Report "PAIR A: OK" khi cả 2 take đều còn — KHÔNG check transcript chỉ dựa vào cảm tính
- ❌ Auto-trim take "vì lặp" → có thể mất USP quan trọng (tên model đầy đủ)
- ❌ Bỏ qua cặp nào user flag vì "không thấy ngay" — PHẢI verify hết
- ❌ Generic "không có vấn đề" → không có timestamp evidence = không verify

### Real case 18/07 clip 0004 — 2 manual suspect pairs

#### PAIR A: "Đây là mẫu hút bụi Dodoto Air Luxe V3" vs "Đây là mẫu hút bụi Dodoto Luxe V3"

| Take | Timestamp | Text | Duration |
|---|---|---|---|
| **TAKE CŨ** | 10.56s → 14.62s | "Đây là mẫu hút bụi Dodoto Air Luxe V3" (đầy đủ tên model) | 4.06s |
| **TAKE MỚI** | 14.62s → 17.56s | "Đây là mẫu hút bụi Dodoto Luxe V3" (rút gọn "Air") | 2.94s |

**Verdict: BOTH_IN_CUT** ⚠️

**Action đề xuất:**
- Keep TAKE CŨ (10.56s) — đầy đủ tên "Air Luxe V3", giữ USP model name đầu clip
- Cut TAKE MỚI (14.62s)

#### PAIR B: "Cục binh của nó là 4000mAh nên là có thể hút bụi được một khu vực liên tục" vs "...nên là nó có thể hút bụi liên tục được"

| Take | Timestamp | Text | Status |
|---|---|---|---|
| **TAKE MỚI** | 96.94s → 101.24s | "Cục binh của nó là 4000mAh nên là có thể hút bụi được một khu vực liên tục" | ✅ IN CUT |
| TAKE CŨ | — | — | ❌ NOT IN CUT (đã cắt) |

**Verdict: TAKE_NEW_ONLY** ✅ → Editor đã xử lý đúng, không cần action.

### Xem thêm

- `references/lesson-2026-07-18-verify-clip-0004.md` — transcript chi tiết clip 0004 Doroto Air Luxe V3 với 2 manual suspect pairs + ghost segments filter.

---

## 🚨 PITFALL #15 (NEW 18/07/2026) — FILLER position classifier (trailing intonation ≠ leading filler)

**Ngày phát hiện:** 18/07/2026 (clip 0004 Doroto Air Luxe V3 — 1 filler hit "á" trailing ở cuối câu 153.84s, không phải filler lửng lơ).

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
    import re
    raw = word_obj["word"].strip()
    text = segment_text.lower()
    
    # Find position ratio
    word_pos = text.find(raw.lower())
    if word_pos < 0:
        return "unknown"
    total_len = len(text)
    pos_ratio = word_pos / total_len if total_len > 0 else 0
    
    # Trailing: last 15% of text or after "luôn/nhé/nha/nè/nhe/ha"
    is_trailing = pos_ratio >= 0.85
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
2. Check trailing patterns ("luôn", "nhé", "nha", "á" ở cuối câu) — trailing = GIỮ
3. Check leading patterns (head of sentence) — leading = CẮT
4. Check bridge patterns (sau `thì/là/vì`) — bridge = CẮT
5. **Trailing intonation = SKIP (giữ)**; leading/bridge = flag FAIL

### Anti-pattern VĨNH VIỄN

- ❌ Flag tất cả "ơ/ờ/ừ/á" mà KHÔNG check position
- ❌ Trim trailing "á" ở cuối câu → mất intonation tự nhiên
- ❌ Trim "á" ở "lắm luôn á" / "rất tốt á" → câu nghe cứng
- ❌ Không phân biệt được leading vs trailing filler

### Real case clip 0004 — á @ 153.84s

- Text full: "Trời ơi, làm rất là đẹp nha, hoàn thiện nhìn sang lắm luôn **á**"
- Position ratio = 0.91 (trailing)
- Preceding pattern: "lắm luôn" matches trailing regex
- **Verdict: TRAILING_INTONATION → SKIP, không fail**

→ Final FILLER count: **0 REAL hits** (sau filter trailing) thay vì 1 hit raw

### Cập nhật FILLER_LIST v3.22.0 (effective)

Bổ sung classifier cho từng filler theo position:

| Filler | Leading role | Trailing role |
|---|---|---|
| `ơ` | Filler lửng lơ | (hiếm trailing) |
| `ờ` | Filler lửng lơ | (hiếm trailing) |
| `ừm` | Filler lửng lơ | (không trailing) |
| `ừ` | Filler lửng lơ | (hiếm trailing) |
| `ó` | Bridge emphasis | Intonation cuối |
| `à` | Filler lửng lơ | Intonation cuối (sau luôn/nhé/nha) |
| `á` | Filler lửng lơ | **Intonation cuối** (sau luôn/nhé/nha) — GIỮ |

→ **Trước khi flag "á" ở cuối câu là filler**, PHẢI check `classify_filler_position()` heuristic.

### Xem thêm

- `references/lesson-2026-07-18-verify-clip-0004.md` — transcript chi tiết clip 0004 với "á" classifier case + 5-dim filter log.

---

## 🚨 PITFALL #16 (NEW 18/07/2026) — Manual suspect pair PHẢI cross-check với subagent (timestamp evidence)

**Ngày phát hiện:** 18/07/2026 (clip 0004 Doroto Air Luxe V3 — manual scan flag 2 cặp suspect: PAIR A "Dodoto Air Luxe V3" + PAIR B "Pin 4000mAh". Subagent check timestamp word-level cho thấy PAIR B = TAKE_NEW_ONLY, KHÔNG phải BOTH_IN_CUT như em manual confirm sai).

### Vấn đề

Manual scan text transcript KHÔNG có timestamp chi tiết → dễ nhầm 2 segments giống nhau là "take lặp" khi thực tế editor đã cắt đúng 1 take từ trước. Real case clip 0004:

**Em manual scan (KHÔNG có timestamp):**
- PAIR A: "Đây là mẫu hút bụi Dodoto Air Luxe V3" + "Đây là mẫu hút bụi Dodoto Luxe V3" → manual confirm FALSE START
- PAIR B: "Cục binh của nó là 4000mAh... khu vực liên tục" + "Cục binh của nó là 4000mAh... liên tục được" → manual confirm FALSE START

**Subagent check timestamp word-level:**
- PAIR A: seg 1 (10.56s) + seg 2 (14.62s) → cả 2 take CÒN trong cut → **BOTH_IN_CUT (FAIL thật)** ✓
- PAIR B: chỉ có 1 occurrence ở 96.94s (TAKE MỚI) → TAKE CŨ đã bị editor cắt đúng từ trước → **TAKE_NEW_ONLY (PASS thật)** ✗

→ Manual confirm sai 1 cặp. Nếu em không cross-check với subagent → ship 1 cặp với action sai.

### Quy tắc VĨNH VIỄN (FIRST-CLASS)

**Khi manual scan flag K cặp suspect phrase, PHẢI cross-check với subagent (hoặc script có timestamp) trước khi báo verdict chính thức:**

1. **Manual scan** text → list K cặp suspect (initial verdict: BOTH_IN_CUT cho mỗi cặp)
2. **Re-dispatch subagent** (scope gọn: chỉ check K cặp + cho timestamp + verdict enum từng cặp)
3. **Subagent verdict** mới là CHÍNH THỨC
4. **Manual verdict** chỉ là INITIAL HINT, ghi rõ "manual pending subagent confirmation"
5. **KHÔNG BÁO verdict manual** như chính thức cho đến khi subagent confirm

### Workflow cập nhật (validate 18/07)

```python
def verify_manual_suspect_pairs(clips, suspect_pairs):
    """Bước 1: Manual scan list K cặp suspect (initial hint)
       Bước 2: Re-dispatch subagent scope GỌN
       Bước 3: Cross-check verdict enum từng cặp
    """
    # Step 1: Manual scan
    manual_verdicts = {}
    for pair in suspect_pairs:
        manual_verdicts[pair.id] = "BOTH_IN_CUT (initial hint - manual)"
    
    # Step 2: Re-dispatch subagent
    subagent_verdicts = dispatch_subagent_scope_gon(
        clips=clips,
        scope="CHECK_K_SUSPECT_PAIRS",
        suspect_pairs=suspect_pairs  # gồm phrase + timestamp hint
    )
    
    # Step 3: Cross-check
    final_verdicts = {}
    for pair in suspect_pairs:
        sub_verdict = subagent_verdicts.get(pair.id, "UNKNOWN")
        manual_verdict = manual_verdicts.get(pair.id, "UNKNOWN")
        if manual_verdict != sub_verdict:
            # Flag conflict
            final_verdicts[pair.id] = f"CONFLICT: manual={manual_verdict}, subagent={sub_verdict}"
        else:
            final_verdicts[pair.id] = sub_verdict
    
    return final_verdicts
```

### Anti-pattern VĨNH VIỄN

- ❌ Manual confirm "BOTH_IN_CUT" cho K cặp mà KHÔNG cross-check với subagent
- ❌ Báo verdict manual như chính thức → có thể ship action sai (giống PAIR B case)
- ❌ Tin tưởng 100% vào cảm tính "rõ ràng là take lặp" mà KHÔNG verify bằng timestamp
- ❌ Bỏ qua subagent confirmation vì "manual đã đủ chính xác" → false positive risk cao
- ❌ Báo cáo "PAIR B: FALSE START (manual)" khi subagent confirm "PAIR B: PASS (TAKE_NEW_ONLY)"

### Real case 18/07 clip 0004 (PAIR B lesson)

**Initial manual verdict (sai):**
- PAIR B = FALSE START (2 take lặp)

**Subagent verdict (đúng):**
- PAIR B = PASS (TAKE_NEW_ONLY)
- Editor đã cắt TAKE CŨ từ trước, chỉ còn TAKE MỚI ở 96.94s

**Lesson vĩnh viễn:** Manual scan text KHÔNG CÓ timestamp → FALSE POSITIVE rate cao (1/2 trong case này). PHẢI re-dispatch subagent với context "đặc biệt check K cặp này" trước khi báo verdict chính thức.

### Trade-off matrix

| Method | Time | False Positive Risk | When to use |
|---|---|---|---|
| Manual scan text only | 1-2 phút | ⚠️ Cao (1/2 PAIR B case) | Initial hint, KHÔNG báo verdict |
| Subagent scope GỌN (check K cặp) | 90-180s | ✅ Thấp | Verdict chính thức |
| Subagent scope FULL (7 layers) | 5-10 phút | ✅ Rất thấp | Multi-clip batch lớn |

→ **Best practice:** Manual scan → list suspect pairs → re-dispatch subagent scope GỌN với context "check K cặp này" → verdict chính thức.

### Khi nào KHÔNG cần subagent cross-check

- Pair có timestamp evidence rõ ràng (vd seg 5 ở 12.34s vs seg 7 ở 16.78s, gap > 5s) → manual đủ
- Single take không có cặp để compare
- Đã chạy script check_anchor_lap.py với keep awareness → có timestamp rõ

### Xem thêm

- `references/pitfall-manual-vs-subagent-cross-check-2026-07-18.md` (TODO nếu cần) — full transcript lesson về PAIR B false positive
- PITFALL #14 (Manual suspect pair verdict enum) — workflow chi tiết verify từng cặp
- PITFALL #11 (Parallel-reason false positive) — phân biệt false start vs parallel-reason rhetoric

### Reference

---

## 🚨 PITFALL #17 (NEW 18/07/2026) — Subagent TIMEOUT → re-dispatch SCOPE GỌN (KHÔNG full scope)

**Ngày phát hiện:** 18/07/2026 (5 subagents parallel verify 6 clips → 3 TIMEOUT ở 600s, em manual fallback cho 2 cái).

**Nguyên nhân TIMEOUT:**
- Mỗi subagent chạy 6 layers: extract audio → Whisper → frame extract → 5-section verify → write report
- API calls quá nhiều (extract WAV, Whisper mlx, motion pixel diff, audio waveform)
- Re-render HEVC 4K source chậm → 600s không đủ

**Quy tắc VĨNH VIỄN (FIRST-CLASS):**
1. **5 subagents parallel** verify 6 layers → 3 TIMEOUT ở 600s = BÌNH THƯỜNG (chấp nhận 50% TIMEOUT rate khi full scope)
2. **KHÔNG retry full scope** → re-dispatch với **SCOPE GỌN** (chỉ 5 narrative + FALSE START, bỏ motion/audio/RMS)
3. **Scope GỌN → done trong 90-180s** → tỉ lệ success >95%

**Scope gọn template (validated 18/07):**
- CHẠY: extract audio → Whisper word-level → 5-dim narrative → FALSE START Layer 3 → spec quick (1 line)
- BỎ: motion pixel diff → audio waveform → RMS delta vs source → contact sheet
- Kết quả: 2/2 re-dispatched subagents done trong 90-180s

**Anti-patterns:**
- ❌ Retry full scope sau TIMEOUT → sẽ TIMEOUT lại (60% chance)
- ❌ Bỏ luôn subagent và báo "đã verify thủ công" khi chưa có evidence thật
- ❌ Poll /tmp folders mỗi 5s (poll 30s OK, không poll 5s — gây noise)
- ❌ Đợi TẤT CẢ subagent xong mới báo cáo → mất 10-15 phút

**Pattern đúng (validated 18/07):**
- Dispatch 5 parallel → đợi 8 phút → 3/5 done
- Nếu manual thấy cặp suspect → re-dispatch scope GỌN với context "đặc biệt check 2 cặp này"
- Re-dispatch sẽ trả report trong 90-180s thay vì TIMEOUT 600s

---

## 🚨 PITFALL #18 (NEW 18/07/2026) — Manual suspect pair PHẢI cross-check subagent (PAIR B case study)

**Ngày phát hiện:** 18/07/2026 (clip 0004 Doroto Air Luxe V3 — em manual flag PAIR B "Pin 4000mAh" = FALSE START, subagent check timestamp word-level confirm = TAKE_NEW_ONLY (PASS thật). Manual sai 1/2).

**Real case 18/07 clip 0004:**
- **PAIR A** (TÊN SẢN PHẨM lặp): "Dodoto Air Luxe V3" + "Dodoto Luxe V3" tại 10.56s + 14.62s
- **PAIR B** (PIN lặp): "Cục binh của nó là 4000mAh... khu vực liên tục" + "...liên tục được"

**Em manual verdict (SAI 1/2):**
- PAIR A: BOTH_IN_CUT (đúng)
- PAIR B: BOTH_IN_CUT (sai - thực tế TAKE_NEW_ONLY)

**Subagent verdict (đúng 2/2):**
- PAIR A: BOTH_IN_CUT (FAIL)
- PAIR B: TAKE_NEW_ONLY (PASS) - editor đã cắt TAKE CŨ từ trước, chỉ còn TAKE MỚI ở 96.94s

**Bài học VĨNH VIỄN:**
1. **Manual scan text KHÔNG CÓ timestamp chi tiết** → FALSE POSITIVE rate cao
2. **Subagent có quyền truy cập word-level timestamps** → check chính xác từng take
3. **LUÔN cross-check manual với subagent khi user flag suspect pairs**
4. **Manual verdict chỉ là INITIAL HINT** — verdict chính thức phải từ subagent

**Anti-patterns VĨNH VIỄN:**
- ❌ Manual confirm "BOTH_IN_CUT" cho K cặp mà KHÔNG cross-check subagent
- ❌ Báo verdict manual như chính thức → có thể ship action sai
- ❌ Tin tưởng 100% vào cảm tính "rõ ràng là take lặp"
- ❌ Bỏ qua subagent confirmation vì "manual đã đủ chính xác"

**Workflow update:**
```python
def verify_manual_suspect_pairs(clips, suspect_pairs):
    # Step 1: Manual scan → list K cặp suspect (initial hint)
    manual_verdicts = {pair.id: "BOTH_IN_CUT (initial hint)" for pair in suspect_pairs}
    
    # Step 2: Re-dispatch subagent scope GỌN (PITFALL #17)
    subagent_verdicts = dispatch_subagent_scope_gon(
        clips=clips, scope="CHECK_K_SUSPECT_PAIRS", suspect_pairs=suspect_pairs
    )
    
    # Step 3: Cross-check
    final_verdicts = {}
    for pair in suspect_pairs:
        sub_verdict = subagent_verdicts.get(pair.id, "UNKNOWN")
        if manual_verdicts[pair.id] != sub_verdict:
            final_verdicts[pair.id] = f"CONFLICT: manual={manual_verdicts[pair.id]}, subagent={sub_verdict}"
        else:
            final_verdicts[pair.id] = sub_verdict
    return final_verdicts
```

---

## 🚨 PITFALL #19 (NEW 18/07/2026) — Mỗi clip fail PHẢI fix ngay + verify lại (USER EXPLICIT)

**Ngày phát hiện:** 18/07/2026 (anh dặn verbatim: *"cái nào fail thì fix lại và thiếu speed thì speed lên!"*)

**Quy tắc VĨNH VIỄN (USER EXPLICIT FIRST-CLASS):**
1. **Verify N clips** → phát hiện fail
2. **Fix NGAY từng cái một** (KHÔNG báo cáo fail rồi đợi xác nhận)
3. **Verify lại** sau khi fix
4. **Move file đã fix** vào `_shipped/<DATE>/` ngay khi PASS

**Real case 18/07:**
- Verify 6 clip → 3 fail (0005 OLD 2 FALSE START, 0004 PAIR A + duration, 0007 duration)
- Em fix 3/3 → tất cả PASS → move 5 file (3 fix + 1 ship cũ + 1 V2 LED RGB) vào `pipeline/output/_shipped/2026-07-18/`

**Anti-patterns:**
- ❌ Báo cáo fail rồi đợi user xác nhận mới fix
- ❌ Fix 1 clip xong mới qua clip tiếp (khi anh đã explicit "cái nào fail thì fix")
- ❌ Bỏ qua fix vì "fail không nghiêm trọng"
- ❌ KHÔNG apply speed 1.3x khi duration > 130s (PITFALL #26)

---

## 🚨 PITFALL #20 (NEW 18/07/2026) — Re-render dùng file Final_ làm input, KHÔNG dùng RAW HEVC 4K

**Ngày phát hiện:** 18/07/2026 (clip 0005 OLD re-render từ RAW ra 207s sai duration vs re-render từ Final_ ra 69s đúng).

**Lý do:** Subagent EDL timestamps được tính trên file Final_ đã edit (1080×1920), KHÔNG phải file RAW DJI (1728×3072 HEVC 4K).

**Comparison:**
- RAW HEVC 4K (1728×3072): 1.5 GB cho 222s → ffmpeg decode chậm 5-10×
- Final_ (1080×1920): 87 MB cho 166s → ffmpeg decode nhanh

**Quy tắc VĨNH VIỄN:**
- Khi re-render clip dựa trên EDL → **dùng file Final_ đã edit làm input**
- Verify timestamp trong EDL có nằm trong range của file Final_ hay RAW

**Real case 18/07:**
- Source RAW 0004 = 222.8s
- File Final_ = 166.4s
- Subagent EDL timestamps (14.62-17.56s) là trong Final_, KHÔNG phải RAW
- Nếu dùng RAW làm input + apply EDL từ Final_ → cắt sai vị trí (RAW chưa qua edit)

---

## 🚨 PITFALL #21 (NEW 18/07/2026) — Concat filter_complex CÙNG source + `-ss -to` SILENT DURATION BUG

**Ngày phát hiện:** 18/07/2026 (3 lần fail liên tiếp khi re-render 3 clip fail).

**Vấn đề:** Dùng 1 source file làm N input với `-ss -to` khác nhau + concat filter → FFmpeg dùng FULL duration input đầu tiên → output duration = source full duration.

**Real case 18/07:**
- Source 0005 OLD = 225.7s
- EDL 5 ranges tổng = 311.48s
- Concat filter output = 207.8s (= source - 18s, chỉ cắt 1 range)
- Same bug với clip 0004: expected 125.8s, concat filter ra 169.2s

**Fix VĨNH VIỄN (HARD RULE):**
1. **KHÔNG BAO GIỜ** dùng `filter_complex concat` với CÙNG source + N input
2. **PHẢI extract từng segment thành file RIÊNG** trước, rồi dùng `concat demuxer`
3. Verify duration ngay sau concat bằng `ffprobe -show_entries format=duration`

**Workflow chuẩn:**
```bash
# Step 1: Extract từng segment riêng
for range_str in "0.72:36.14" "40.98:46.36" "50.02:225.7"; do
  ffmpeg -y -ss $start -to $end -i SOURCE -c:v libx264 -preset medium -crf 18 segment.mp4
done

# Step 2: Concat demuxer
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final.mp4
```

---

## 🚨 PITFALL #22 (NEW 18/07/2026) — Tiktok-pipeline-studio migrate folder structure (LESSON)

**Context:** Em migrate 123 files / 11.7 GB từ flat folder sang cấu trúc `pipeline/{drafts, output/{_shipped, _ready_to_ship}}/, _archive/, _verify/, logs/` theo pattern của repo `browser-use/video-use`.

**Pattern từ video-use:**
- **Skill code immutable** + **output mutable**
- **EDL JSON schema** cho LLM↔renderer
- **3 quality ladder**: draft / preview / final
- **30ms audio fade** mọi cut boundary
- **Subtitles apply LAST**
- **Self-eval** với timeline PNG
- **12 hard rules** tách rõ với artistic freedom

**Reference:** `Hermes-Edit/_docs_video_use_vs_tiktok_comparison.md` (13KB so sánh chi tiết)

**Action items cho tiktok-verify-protocol:**
- [ ] Update `scripts/verify_clip.py` để tích hợp ghost segment filter (PITFALL #13)
- [ ] Update `scripts/verify_clip_full.py` để tích hợp `classify_hook_lap()` enumeration (PITFALL #12)
- [ ] Update `scripts/verify_clip_full.py` để tích hợp `classify_false_start()` parallel-reason (PITFALL #11)
- [ ] Update `scripts/verify_clip_full.py` để tích hợp `classify_filler_position()` trailing intonation (PITFALL #15)
- [ ] Update `scripts/verify_clip_full.py` để tích hợp `is_ghost_seg()` filter (PITFALL #13)
- [ ] Tạo `scripts/verify_with_keep_awareness.py` cho manual suspect pair verify (PITFALL #14)
- [ ] Tạo `scripts/dispatch_subagent_scope_gon.py` cho PITFALL #17 re-dispatch workflow
- [ ] Tạo `scripts/verify_manual_suspect_pairs.py` cho PITFALL #18 cross-check workflow

## 🚨 PITFALL #25 (NEW 21/07/2026) — Exit code behind pipe = filter's exit, NOT script's

**Ngày phát hiện:** 21/07/2026 (clip 0031 V1 verify 6 layers — báo `EXIT_L6=0` do `| tail`, script thật exit 1 → sai verdict).

**Vấn đề**: Khi verify bằng `python3 script.py ... | tail -40; echo "EXIT=$?"`, biến `$?` là exit code của `tail` (luôn = 0 nếu tail chạy được), KHÔNG phải của script Python. Case 0031: scan_false_start.py thật exit 1 (FAIL "pocket bar × 7") nhưng report ghi "EXIT_L6=0" → verdict PASS sai.

**Fix BẮT BUỘC**: redirect stdout+stderr ra file trước, `$?` mới phản ánh script thật:

```bash
python3 script.py video.mp4 >/tmp/scan_out.txt 2>&1
REAL_EXIT=$?      # ← đây mới là exit code của script
cat /tmp/scan_out.txt
```

Hoặc `set -o pipefail` đầu shell session. Nhưng redirect-to-file vẫn an toàn nhất cho evidence logging vì có cả output riêng để grep/cite.

**Áp dụng**: MỌI script có exit code semantics khi user yêu cầu "evidence THẬT" / "tool THẬT" — scan_false_start.py, check_audio_fade.py, verify_clip.py, ffprobe ngôn ngữ exit-code khác.

---

## 🚨 PITFALL #26 (NEW 21/07/2026) — Layer 5 speed ratio: verify ACTUAL trước khi verdict

**Ngày phát hiện:** 21/07/2026 (clip 0031 V1 — task brief nói "speed 1.3x ratio hợp lý", verify mới thấy actual src/clip = 2.0142x ≈ 2.0x, không phải 1.3x).

**Vấn đề**: User có thể gợi ý speed trong task brief, nhưng clip thực tế đã apply speed khác. Nếu chỉ check "speed X.x có hợp lý không" mà không tính actual ratio → verdict vô nghĩa / sai.

**Workflow L5 đúng**:

```bash
SRC_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 source.mp4)
CLIP_DUR=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 final.mp4)
RATIO=$(python3 -c "print(f'{$SRC_DUR/$CLIP_DUR:.4f}')")
echo "src=$SRC_DUR clip=$CLIP_DUR ratio=$RATIO"
```

Sau đó compare `RATIO` với task's claimed speed:
- Ratio nằm ngoài range plausible TikTok Mode B (1.0x-3.0x) → REJECT, flag.
- Ratio nằm trong range nhưng lệch brief → report "actual=Xx, task nói Yx — MISMATCH", để user quyết định.
- KHÔNG tự ý verdict PASS/FAIL với giả thuyết sai.

---

**PITFALL cụ thể:**
- ❌ KHÔNG dùng `ffmpeg signalstats` filter để check brightness trên PNG đã extract — output im lặng. Dùng PIL/Python.
- ❌ KHÔNG trust vision model 100% — luôn có fallback pixel stats (vision có thể strip output).
- ❌ KHÔNG fail chỉ vì duration off <100ms (1-3 frames ở 30fps).
- ✅ LUÔN parallel batch: L1 hash + L2 ffprobe + L7-prep `ffmpeg -f null -` song song turn đầu.

Xem chi tiết + repro recipe: `references/pitfall-25-technical-spec-verify.md`.

## 🚨 PITFALL #23 (NEW 21/07/2026) — Layer 5 "speed 1.3x applied" literal criteria SAI với Mode B

**Ngày phát hiện:** 21/07/2026 (batch 7 DJI clips 0029-0038 verify — 0/7 clip pass theo literal ratio source/final = 1.3 nhưng TẤT CẢ đều có speed 1.3x verified gián tiếp).

**Tóm tắt:** Literal `source_duration / final_duration ≈ 1.3` chỉ đúng cho Mode A (giữ 100% source). Mode B workflow (cắt 25-50% source + speed 1.3x) → ratio = 1.3 / keep_coverage = **1.3-2.6**. Áp dụng literal cho mọi Mode B edit → false FAIL.

**Correct criteria:** `keep_coverage_pct = (final × 1.3) / source × 100%` thuộc `[30%, 80%]` cho Mode B (cut 20-70%); `[90%, 110%]` cho Mode A; `< 30%` accept nếu source > 200s (PITFALL #49 aggressive cut).

**Anti-pattern:** ❌ Báo FAIL Layer 5 vì `source/final ≠ 1.3` trong khi `keep_coverage ∈ [30%, 80%]` → false FAIL. ❌ Require raw kept evidence (keeps.json) để chứng minh speed 1.3x — KHÔNG cần, indirect proof đủ.

**Xem thêm:** `references/lesson-2026-07-21-verify-7-clip-batch-dji-0029-0038.md` (full 7-clip matrix + Python verify function).

---

## 🚨 PITFALL #24 (NEW 21/07/2026) — Verify-context filename mismatch

**Ngày phát hiện:** 21/07/2026 (batch 7 DJI clips 0029-0038 verify — user input 7 file paths nhưng 2/7 paths KHÔNG tồn tại trên disk: clip 0034 + 0038 đã được rename theo actual duration sau render).

**Tóm tắt:** User cung cấp input path dựa trên expected duration. File trên disk có thể khác vì PITFALL #48 (rename theo actual duration). Khi path user đưa KHÔNG tồn tại → KHÔNG auto-fail, mà tìm file similar trên disk theo clip_id pattern (`clip_XXXX_V*_FINAL*.mp4`), verify file đó, flag mismatch trong report.

**Correct workflow:**
1. Try user-input path → nếu tồn tại: verify trực tiếp
2. Nếu KHÔNG tồn tại: search disk theo `clip_id` pattern (e.g., `clip_0034_V1_*FINAL*.mp4`)
3. Verify file trên disk + flag mismatch trong report rõ ràng
4. Đánh giá PASS/FAIL theo disk evidence, KHÔNG auto-fail theo user input

**Anti-pattern:** ❌ Báo FAIL vì path user input sai mà KHÔNG check disk (false FAIL). ❌ Rename file để khớp user input — vi phạm PITFALL #48. ❌ Skip verify vì path mismatch. ❌ Hỏi user "file ở đâu?" — user đã ship, có thể không nhớ exact name.

**Xem thêm:** `references/lesson-2026-07-21-verify-7-clip-batch-dji-0029-0038.md` (real case 0034 + 0038 mismatch + disk-search bash snippet).

---

## Reference Files

- `references/6-layer-clip-verify-recipe.md` — L1-L6 quick recipe với exit-code-safe commands cho L3/L6 (PITFALL #25), L5 actual-ratio script (PITFALL #26), verdict table format. Case study: clip 0031 V1 (21/07/2026).
- `references/pitfall-95-tts-audio-container-vs-content.md` — PITFALL #95: TTS/AI-generated audio cần `volumedetect` (max/rms) chứ không chỉ `ffprobe` container. Case 23/07 OmniVoice batch 5 — 4/5 file gần silent mà em report PASS.
- `references/session-2026-07-12-verify-clip-tool.md` - chi tiết tạo tool verify_clip.py + test 5 clip
- `references/session-2026-07-11-step8-verify-fail.md` - lesson khi Step 8 verify sai (Pitfall #6)
- `references/session-2026-07-12-system-wide-rule.md` - System-Wide Verify Rule + khẩu hiệu
- `references/pitfall-verify-2-layers-required-2026-07-14.md` - Real case 8 clip 4 fail + fix strategy
- `references/pitfall-anchor-lap-false-positive-2026-07-14.md` - PITFALL #3 false positive + verify_with_keep_awareness fix
- `references/pitfall-keep-boundaries-match-whisper-segments-2026-07-14.md` - **NEW 14/07** PITFALL #6 keep boundaries = Whisper verify segment boundaries workaround (real case clip 0758 V3→V5 fix)
- `references/pitfall-success-pattern-clip-0731-v3-v5-fix-2026-07-14.md` - PITFALL #5 case study + 3-pattern fix (bỏ keep + trim + drop CTA)
- `references/lesson-source-natural-anchor-lap-pattern-2026-07-16.md` - **NEW 16/07** Source-natural anchor-lap decision tree + 3 clip case study V1→V5 (clip 0005/0006/0007) + SHIP decision matrix (1/3 SHIP CLEAN, 2/3 PARTIAL_PASS)
- `references/lesson-source-natural-anchor-lap-batch-3-3-2026-07-16.md` - **NEW 16/07 BATCH 2** 3 clip buổi trưa (clip 0003/0004/0005) — lesson: source-natural anchor là PATTERN recurring, 1 attempt sau khi học pattern từ batch 1 (time savings 70% V1→V3), SHIP Decision Matrix updated với edge case duration 130-180s.
- `references/pitfall-motion-verify-dark-source-2026-07-18.md` - **NEW 18/07** PITFALL #9 dual-signal motion detector cho dark source (real case clip 0006 diverse-motion verify, mean RGB ≈ 25 → false freeze với pixel-diff threshold 15, dual-signal 18/21 MOVING)
- `references/lesson-2026-07-18-verify-clip-0007.md` - **NEW 18/07** Lesson clip 0007 KNF carbon fiber verify: 7-layer one-shot workflow với verify_clip_full.py, Layer 3 FALSE START scan phát hiện 1 candidate seg 21↔22 match=5/8 ("Bởi vì những cái...này") phân tích parallel-reason rhetoric (PITFALL #11 false positive), 3-keep detection từ 47 silences (single continuous narrative), RMS first-3s = -26.6 dB (no silent take cũ), RMS delta vs source = 0.4 dB (loudness match), motion 41.46% pixel diff (sản phẩm được cầm/xoay rõ). VERDICT: 7/7 PASS ngoại trừ duration 137.3s > 130s Mode B max → cần apply Pitfall #26 speed 1.3x.
- `references/lesson-2026-07-18-verify-clip-0004.md` - **NEW 18/07 v1.0.10** Lesson clip 0004 Doroto Air Luxe V3 verify: scope-narrowed (5 narrative + FALSE START, motion + audio SKIP per user), 2 manual suspect pairs (PAIR A "Đây là mẫu" BOTH_IN_CUT cần cut; PAIR B "Cục binh 4000mAh" TAKE_NEW_ONLY PASS), 3 ghost segments @ 130.92-131.00s (whisper hallucination false positive LẶP NGHĨA + HOOK LẶP — PITFALL #13), "á" filler @ 153.84s trailing intonation (PITFALL #15 classifier SKIP). VERDICT: PARTIAL PASS — chỉ action duy nhất: cut TAKE MỚI 14.62s trong PAIR A.
- `references/lesson-2026-07-21-verify-7-clip-batch-dji-0029-0038.md` - **NEW 21/07 v1.1.1** Lesson batch 7 DJI clips 0029-0038 verify: 5-layer evidence per clip (file/spec/fade/duration/speed); Layer 5 PITFALL #23 indirect proof via keep_coverage 56-92%; Layer 4 PITFALL #24 filename mismatch handling (2/7 files 0034+0038 chưa rename theo actual, flag nhưng đánh giá theo disk); 7/7 SHIP-READY verdict với Mode B hợp lý.
- `scripts/verify_with_keep_awareness.py` - PITFALL #3 Layer 2 verifier với keep boundary awareness
- `scripts/verify_motion.py` - **NEW 18/07** PITFALL #9 dual-signal motion verifier (pixel-diff threshold 5 + mean RGB delta) cho diverse-motion 8-phase clip
- `scripts/verify_clip_full.py` - **NEW 18/07** PITFALL #10/11 7-layer one-shot verifier (spec + 5-dim strict + anchor-lap + FALSE START Layer 3 + RMS first-3s + RMS delta vs source + motion check). Dùng cho mọi clip verify cuối cùng trước khi ship theo user instruction 18/07 "verify clip N".

---

## Real case 12/07 - 5 clip verify & fix

| Clip | V5 issues | V6 final | Fix |
|------|-----------|----------|-----|
| 0704 | 1 LẶP | ✅ 81.48s | Bỏ keep AUTHORITY_HÚT_SÂU (seg 20 lặp với seg 21) |
| 0710 | 2 issues | ✅ 97.44s | Tách AUTHORITY_ỔN_ĐỊNH thành 3 keep nhỏ |
| 0713 | 0 (giữ V5) | ✅ 139.47s | (đã đạt từ V5) |
| C041 | 7 issues | ✅ 122.19s | Trim duration 192→122s + bỏ 3 HOOK_LẶP |
| C043 | 3 issues | ✅ 101.03s | Bỏ seg 4 LẶP + cắt "á" cuối seg 38 |

**Kết quả: 5/5 file V6 đều pass verify_clip.py exit 0** ✓

---

## Changelog

**v1.1.1 (21/07/2026):**
- **PITFALL #23 (NEW)**: Layer 5 "speed 1.3x applied" criteria theo literal `source_duration / final_duration ≈ 1.3` là **SAI** với Mode B workflow (cắt ~25-50% source + speed 1.3x). Real case 21/07 batch 7 DJI clips 0029-0038 verify: 0/7 clip có ratio source/final = 1.3 (thực tế 1.42-2.30) nhưng TẤT CẢ đều có speed 1.3x verified gián tiếp qua `keep_pct = (final × 1.3) / source × 100%` range 56-92% (reasonable Mode B keep coverage). **Correct criteria**: `final_duration × 1.3 ≈ total_kept_raw_duration` (KHÔNG phải source) + `keep_pct ∈ [30%, 80%]` cho Mode B (cut ~20-70%). Anti-pattern: ❌ báo FAIL Layer 5 vì ratio source/final ≠ 1.3 trong khi keep_pct reasonable → false FAIL.
- **PITFALL #24 (NEW)**: VERIFY-CONTEXT FILENAME MISMATCH (extension của tiktok-video-editor PITFALL #48 cho render context). Khi user input filename ≠ disk filename → BOTH verifications cần chạy: (1) check file có tồn tại tại path user đưa không, (2) check disk có file nào similar không (cùng clip number/category). Real case 21/07 batch 7: user input `clip_0034_V1_100s_FINAL_DOROTO_VACUUM.mp4` + `clip_0038_V1_95s_FINAL_POCKETBAR_OPP_KNET.mp4` nhưng disk thực tế = `clip_0034_V1_122s_FINAL_DOROTO_VACUUM.mp4` (122.5s) + `clip_0038_V1_107s_FINAL_POCKETBAR_OPP_KNET.mp4` (107.2s). Filename suffix mismatch = PITFALL #48 (chưa rename theo actual duration). **Correct verify pattern**: verify file THỰC TẾ trên disk (evidence-gate: prove it exists rồi prove it good) + flag mismatch trong report + đánh giá PASS/FAIL theo disk evidence, KHÔNG auto-fail theo user input. Anti-pattern: ❌ báo FAIL vì file không tại path user input mà KHÔNG check disk; ❌ rename file để khớp user input (vi phạm PITFALL #48 — rename theo actual, không ngược lại).
- Reference mới `references/lesson-2026-07-21-verify-7-clip-batch-dji-0029-0038.md` — full 7-clip batch verify case study với Layer 5 indirect proof + Layer 4 filename-mismatch handling workflow + tổng kết 7/7 SHIP-READY evidence.
- Skill version bumped 1.1.0 → 1.1.1

**v1.0.11 (18/07/2026):**
- **PITFALL #13 (NEW)**: Whisper near-zero-duration ghost segments FALSE POSITIVE cho LẶP NGHĨA + HOOK LẶP. Heuristic `is_ghost_seg()` detect seg với `duration < 0.5s` HOẶC word timestamps đồng nhất (≤2 unique end ts trong ≥5 từ). Real case clip 0004 @ 130.92-131.00s: 3 phantom hits từ 1 ghost cluster (seg 29 + seg 30 đều có text identical "Các bạn có thể thổi bụi trong cái khu vực nhỏ này nè" 2 lần). Sau filter: 1 REAL hit (PAIR A) + 0 FP. Anti-pattern: ❌ flag HOOK LẶP khi 1 trong 2 segs duration < 0.5s mà KHÔNG check ghost, ❌ trim 1 trong 2 ghost segments "vì lặp" → không có audio thật để trim, ❌ re-render để fix ghost → ghost là Whisper artifact.
- **PITFALL #14 (NEW)**: Manual suspect pair verification workflow. User flag K cặp phrase suspect (vd clip 0004: PAIR A "Đây là mẫu" + PAIR B "Cục binh 4000mAh") → verify TỪNG cặp độc lập với 4 verdict enum (BOTH_IN_CUT / TAKE_NEW_ONLY / TAKE_OLD_ONLY / NEITHER). Mỗi cặp cần timestamp + text cho cả 2 take để user verify thủ công. Action đề xuất: BOTH_IN_CUT = recommend cut TAKE MỚI (giữ TAKE CŨ USP đầy đủ). Anti-pattern: ❌ report "PAIR A: OK" khi cả 2 take đều còn mà KHÔNG check transcript, ❌ generic "không có vấn đề" → không có timestamp evidence = không verify.
- **PITFALL #15 (NEW)**: FILLER position classifier — trailing intonation ≠ leading filler. Từ `ơ/ờ/ừm/ừ/ó/à/á` có 2 vai trò: leading = filler lửng lơ cần CẮT, trailing sau "luôn/nhé/nha/nè" = intonation marker tự nhiên cần GIỮ. Real case clip 0004 @ 153.84s "á" trailing "Trời ơi, làm rất là đẹp nha, hoàn thiện nhìn sang lắm luôn **á**" → TRAILING_INTONATION SKIP. Heuristic `classify_filler_position()` check `word_pos / len(text)` ratio + preceding pattern. Anti-pattern: ❌ flag tất cả "ơ/ờ/ừ/á" mà KHÔNG check position, ❌ trim trailing "á" → mất intonation tự nhiên, ❌ trim "á" ở "lắm luôn á" → câu nghe cứng.
- Reference mới `references/lesson-2026-07-18-verify-clip-0004.md` — full transcript clip 0004 verify với 5-dim + FALSE START scope-narrowed + 2 manual suspect pairs + ghost segments filter log + filler classifier case.
- Anti-pattern bổ sung (general verify): ❌ Báo PASS khi scope-narrowed mà KHÔNG ghi rõ scope, ❌ Báo FALSE START 0 hits cho manual suspect pair mà không verify từng cặp.
- Workflow Step 8 update → MANDATORY chạy: Layer 1 (5-dim strict với ghost filter + filler position classify) + Layer 3 (FALSE START + manual suspect pair nếu user flag). Layer 2/4/5/6/7 = optional theo scope.

**v1.0.9 (18/07/2026):**
- **PITFALL #12 (NEW)**: Enumeration pattern FALSE POSITIVE cho HOOK LẶP Layer 1. Real case 18/07 clip 0005 V2 máy phun tinh dầu LED RGB: speaker enumeration 4 chế độ phun (5/10/20 phút + liên tục) với head-3 identical "chế độ thứ" → script flag HOOK LẶP #10/#11 → phân tích thấy content phân kỳ (5 phút vs 10 phút vs 20 phút vs liên tục) → enumeration CÓ CHỦ ĐÍCH, KHÔNG phải take-retry hay lặp nghĩa. Heuristic `classify_hook_lap()` với `ENUMERATION_PREFIXES = {chế độ thứ, chế độ số, tính năng, bước, loại, kiểu, điểm cộng, ưu điểm, lý do thứ, cách thứ, trường hợp, ...}` + check content phân kỳ ≥2 từ trong 5 từ đầu sau prefix. Anti-pattern: ❌ flag HOOK LẶP khi head-3 = "chế độ thứ" mà KHÔNG check enumeration, ❌ trim 1 enumeration segment → mất thông tin. Kết hợp với PITFALL #25 9-keep Problem→Solution Mode B template (enumeration rất phổ biến trong product feature listing).
- **Scope-narrowed verify workflow (NEW)**: Pattern mới first time xuất hiện trong task description 18/07 — "Verify nhanh clip 0005 NEW V2 - chỉ check 5 lỗi narrative + FALSE START. Không verify motion, không verify audio." Khi user explicit giới hạn scope: (a) chỉ chạy các layer được chỉ định (Layer 1 + Layer 3 cho narrative + FALSE START), (b) SKIP các layer user không muốn (Layer 4 motion + Layer 5/6 RMS audio), (c) báo cáo PHẢI mở đầu "**Scope**: [scope list]" để user biết em chỉ check phạm vi được yêu cầu, KHÔNG tự ý mở rộng. Anti-pattern: ❌ chạy full 7-layer khi user chỉ request subset → "over-verify" làm mất time + dilute focus.

**v1.0.8 (18/07/2026):**
- **PITFALL #10 (NEW)**: Layer 3 FALSE START scan (từ tiktok-video-editor v3.24.0 PITFALL #21) — protocol quét cặp segments liền kề (gap < 10s) cho 5+/8 từ đầu giống hệt. Real case 18/07 clip 0007 KNF carbon fiber: phát hiện 1 candidate seg 21↔22 match=5/8 ("Bởi vì những cái...này") nhưng phân tích kỹ thấy là **parallel-reason rhetorical structure** (Bởi vì A... Bởi vì B...) — false positive. RMS first-3s check = -26.6 dB (không silent take cũ). PHẢI phân biệt FALSE START vs PARALLEL-REASON: nếu 5 từ đầu giống là **connector scaffolding** ("Bởi vì", "Thì", "Vậy nên") + content phân kỳ ngay sau → KHÔNG phải false start.
- **PITFALL #11 (NEW)**: Parallel-reason rhetorical structure false positive trap. Vietnamese speakers dùng liên từ nhân-quả song song cực kỳ phổ biến: "Bởi vì A... Bởi vì B...", "Thì X... thì Y...", "Vậy nên P... vậy nên Q...". Khi scan FALSE START Layer 3, nếu 5 từ đầu giống là **connector scaffolding** (3-4 từ đầu là filler/connector) + content phần sau PHÂN KỲ → FALSE POSITIVE. Heuristic: nếu match 5/8 mà 3 từ đầu ∈ {bởi vì, thì, vậy nên, tuy nhiên, do đó, cho nên} → KHÔNG tính false start, accept SOURCE-NATURAL anchor-lap.
- **Tool mới `scripts/verify_clip_full.py`** (~430 lines): 7-layer one-shot verifier. Layer 1 spec (ffprobe), Layer 2 5-dim strict, Layer 3 anchor-lap semantic, **Layer 4 FALSE START Layer 3 (PITFALL #21)**, Layer 5 RMS first-3s silent-take detector, Layer 6 audio RMS delta vs source (threshold 0.5dB), Layer 7 motion check (pixel-diff t=5s vs t=10s ≥ 10%). Output SHIP CLEAN / PARTIAL PASS / FAIL + verdict. Dùng cho clip cuối cùng trước khi ship (BẮT BUỘC theo user instruction 18/07 "verify clip N").
- Reference mới `references/lesson-2026-07-18-verify-clip-0007.md` — transcript đầy đủ clip 0007 verify với 7/7 layers chi tiết + 3-keep detection workflow.

**v1.0.7 (18/07/2026):**
- **PITFALL #9 (NEW)**: Motion verify trên source DARK ≠ FREEZE frame. Dual-signal detector bắt buộc cho DJI/GoPro/iPhone thiếu sáng (mean RGB < 50). Pixel-diff threshold 15 cho false freeze → dùng threshold 5 + mean RGB delta. Real case clip 0006 diverse-motion (110s, source DJI mean RGB ≈ 25): 21/21 windows <5% với threshold 15 → 18/21 MOVING với dual-signal. Phase-by-phase 8-phase matrix bắt buộc (HOOK/PROBLEM/INTRO/FEATURE/DEMO/COMPARE/PROOF/CTA). Tool `scripts/verify_motion.py` (190 lines) extract frames + dual-signal + phase verdict. Kết hợp với PITFALL #8 (vùng clean cho motion graphic) để verify motion toàn diện.
- Reference `pitfall-motion-verify-dark-source-2026-07-18.md` — transcript đầy đủ + repro recipe.

**v1.0.6 (16/07/2026):**
- **PITFALL #7 (NEW)**: Source-natural anchor keywords là PATTERN recurring (anh hay dùng "các bạn"/"chúng ta"/"bởi vì" 5-10+ lần / clip). Stats 16/07: 1/6 SHIP CLEAN, 5/6 PARTIAL_PASS. SHIP Decision Matrix updated với SOURCE-LEVEL vs KEEP-BOUNDARY pair distinction. Real case 16/07 batch 2: clip 0003 (1 attempt 15 phút) → clip 0004+0005 (1 attempt 5-10 phút, 70% time savings). Accept duration 130-180s khi content depth justifies.
- Reference `lesson-source-natural-anchor-lap-batch-3-3-2026-07-16.md` — 3 clip buổi trưa case study.

**v1.0.5 (14/07/2026):**
- **PITFALL #6 (NEW)**: Keep boundaries phải match Whisper verify segment boundaries. Real case clip 0758: trim V3/V4 vẫn fail anchor-lap 3 pairs (seg 0+1, 20+21, 31+32 "các bạn" lặp). Fix bằng build keep_plan từ Whisper V4 output (skip seg 0, 21, 31 chứa anchor keywords) → V5 PASS Layer 2 ngay. Trade-off: bỏ 5-10% features chứa anchor keywords tự nhiên, chấp nhận được cho Mode B cô đọng. Combine với PITFALL #3 (`verify_with_keep_awareness`) cho phép keep GHÉP features mà vẫn pass.

**v1.0.4 (14/07/2026):**
- **PITFALL #5 (NEW)**: Whisper medium hallucination @ speed 1.3x concat — đặc biệt với cụm "X và Y" liền kề, Whisper nghe thành "X, X và Y" nhân đôi keyword. Phân biệt vs anchor-lap bằng cách grep source audio.json: source có 1 instance → Whisper decode artifact, KHÔNG tái edit.
- Thêm `references/pitfall-success-pattern-clip-0731-v3-v5-fix-2026-07-14.md` — case study V3→V5 fix thành công với 3-pattern:
  1. Bỏ HẲN keep chứa anchor-lap liền kề (không trim — trim vẫn còn nguy cơ)
  2. Trim keep dài giàu bridge words trước khi render (giảm treo risk dù strict rule miss)
  3. CTA hard-sell nằm cùng keep gây lap → CHẤP NHẬN DROP CTA (ưu tiên anchor-free)

**v1.0.3 (14/07/2026):**
- **PITFALL #4 FIRST-CLASS** (NEW): User feedback verbatim 14/07 về verify kém — "verify phải thật kĩ toàn bộ transcript không bỏ qua bước nào". 8/8 clip ship mà 4/8 fail Layer 2 (anchor-lap).
- **2-LAYER VERIFY BẮT BUỘC** for EVERY clip: Layer 1 (`verify_clip.py` 5-dim strict) + Layer 2 (`check_anchor_lap.py` semantic). 1 layer only = FALSE PASS.
- Workflow Step 8 update → MANDATORY: chạy CẢ 2 layers
- Checklist update: 2 layers BẮT BUỘC check, đọc TOÀN BỘ transcript
- Real case 14/07: 8 clip ship, 4 fail Layer 2 → re-render 4 clip + skill fix
- Bổ sung ANCHOR keywords list: `các bạn, chúng ta, mọi người, nhà mình, bên mình, chúng ta` (từ real case 14/07)

**v1.0.2 (14/07/2026):**
- **PITFALL #3 (FIRST-CLASS)** — `check_anchor_lap.py` FALSE POSITIVE TRÊN KEEPS GHÉP
- Snippet `verify_with_keep_awareness()` trong SKILL.md
- Best practice: chia keeps NHỎ (max 5-10s) + word-level cut tại anchor boundaries

**v1.0.1 (13/07/2026):**
- **PITFALL #1 FIRST-CLASS**: verify_clip.py v3.21.4 PASS vẫn miss semantic lap (cross-keep same anchor keyword với prefix 2 từ đầu KHÁC nhau). Real case clip 0740 "Body mist AMAP - tinh tế": "nhãn hàng" + "nhưng mà" lặp nhưng script PASS.
- Thêm `scripts/check_anchor_lap.py` — semantic layer độc lập, chạy SAU verify_clip.py PASS để spot anchor keywords lặp trong Whisper verify transcript.
- Thêm `references/pitfall-strict-matcher-blind-spot-2026-07-13.md` — transcript đầy đủ + repro recipe + analysis tại sao strict matcher miss.
- **PITFALL #2**: source.MOV symlink trong `tmp/<clip>/` bị cleanup sau workflow → V2 re-render mất source. Bắt buộc find source duration khớp ±2s trước khi re-render.
- Quy tắc mới: mọi clip PHẢI chạy ≥2 verify layer (strict + semantic spot-check) trước khi báo "đạt goal".

**v0.0.0 (12/07/2026):**
- Initial skill scaffold
- Tách verify protocol thành class-level skill riêng
- Tool `scripts/verify_clip.py` v3.21.4 (check 5 loại lỗi + spec)
- Filler list cuối: `ơ, ờ, ừm, ừ, ó, à, á` (bỏ "đó" và "thì")
- Quy tắc verify mới: Lặp nghĩa 2+, Hook lặp 3+, Ựm ờ đứng đơn, Treo 3+ từ
- System-Wide Rule 3: phải nói tên rule khi apply
- 5/5 clip test re-edit pass verify_clip.py"
