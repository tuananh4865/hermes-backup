# Session 24/07/2026 Updates — Critical Lessons Learned

**Context:** Anh extended testing với voice message mới, exposed 3 gaps trong skill ban đầu (23/07).

## L7 (NEW): ref_text SWEET SPOT = 2 cau ~80-100 chars (verified 24/07)

**Background:** Anh gui voice message Telegram 12.9s, em save file voice clone voi `ref_text` chi 1 cau ~26 chars → output bi **hallucinate LOOP** 8-10 lan, file 76.96s thay vi 13s binh thuong.

**Verified matrix (4 variants):**

| ref_text | Length | Output behavior | Use case |
|---|---|---|---|
| QUA NGAN (1 cau ~25 chars) | 26 chars | LOOP 8-10 lan, hallucinate | KHONG DUNG |
| 1 cau day du | 99 chars | Sach nhung peak thap hon baseline | OK cho simple cases |
| **2 cau ~80-100 chars** | 81 chars | SACH + peak cao | **SWEET SPOT** |
| Full transcript (~185 chars) | 185+ chars | LEAK cau cuoi vao output | KHONG DUNG |

**Rule:** `ref_text = 2 cau dau trong Whisper transcript, ~80-100 chars`

```python
# DUNG
REF_TEXT = "Xin chao toi la Tuan Anh day. Toi la Tuan Anh day, voice nay dung de test clone."
# = 81 chars

# SAI (qua ngan -> LOOP)
REF_TEXT = "Xin chao toi la Tuan Anh day."

# SAI (qua dai -> LEAK)
REF_TEXT = "Xin chao toi la Tuan Anh day. Troi oi toi la Tuan Anh day. ..."
```

**Update SKILL.md:**
- Phase 3: thay "1 cau ~100 chars" → "2 cau ~80-100 chars"
- Pitfall #3 → split thanh 3a (leak) + 3b (loop)
- L7 lesson added

---

## L8 (NEW): Terminology correction — voice ref → file voice clone (.pt)

**Background:** Em da dung thuat ngu voice ref trong memory + SKILL.md → gay hieu lam vi:
- voice ref goi y raw audio can import moi lan (sai)
- Thuc te: skill nay xu ly **file .pt da encode san** = file voice clone

**Verified prompts hien tai o `/Volumes/Storage-1/Hermes/voice-prompts/`:**

| File | Size | ref_rms | ref_text | Source |
|---|---|---|---|---|
| `tuan_anh_5s_1sent_amp.pt` | 9.9KB | 0.1100 | 99 chars (1 cau) | GOOJODOQ video review |
| `tuan_anh_v3_voice_msg_10s.pt` | 17.5KB | 0.1026 | 81 chars (2 cau) | Telegram voice message |
| `tuan_anh_session_2026-07-23.pt` | ~10KB | - | - | Session 23/07 |
| `tuan_anh_goojodoq_5s_short.pt` | 10.2KB | - | 185 chars | Test (CON leak nhe) |
| `tuan_anh_goojodoq_8s.pt` | 14.5KB | - | 122 chars | Test (ref_rms < 0.1, FAIL) |

**Terminology mapping:**

| SAI | DUNG |
|---|---|
| voice ref | **file voice clone (.pt)** |
| voice prompt | **file voice clone (.pt)** |
| ref_audio moi lan | **load file .pt da save** |
| TikTok voice | **voice cho moi use case** |

**Update SKILL.md:**
- Description them: "file voice clone (.pt)"
- New section "TERMINOLOGY" o dau SKILL.md
- Phase 1 doi ten: "Check file voice clone (.pt) da co san"
- Phase 3 doi: "Save file voice clone (.pt)"
- Phase 4: "Generate tu file voice clone (.pt)"

---

## L8 (CONT): Scope mo rong — KHONG chi TikTok

**Push-back:** "Bo chu tiktok di chi can anh noi tao voice la em dung omnivoice tao voice cho anh"

**Update SKILL.md:**
- Description them trigger: "tao voice" / "clone giong" / "OmniVoice TTS" / "tong hop giong noi" — KHONG chi TikTok
- "Use when" mo rong: "Phu hop moi use case can synthetic voice: TikTok, YouTube narration, podcast, audiobook, video voiceover, v.v."
- "When to use" table: tat ca rows doi scope
- references/04-recipes.md: Recipe 12 doi tu "TikTok Template" → "Voice Template"

---

## Verify sessions (verified 24/07)

### Session 24/07 — compare 3 file voice clone

**Voice msg source:** `/Users/tuananh4865/.hermes/audio_cache/audio_1d2f805ee2e3.ogg` (12.9s, 48kHz Opus)

| Version | ref_text | Output dur | Peak | Whisper | Verdict |
|---|---|---|---|---|---|
| v1 GOOJODOQ | 99 chars | 13.28s | -2.6 dB | Sach | OK |
| v2 voice_msg (5s ref, 1 cau) | 26 chars | 76.96s | -1.2 dB | LOOP 8-10 lan FAIL | FAIL |
| v3 voice_msg (10s ref, 2 cau) | 81 chars | 22.32s | -2.0 dB | OK (voi target text co repetition) | OK |

**Conclusion:** ref_text 81 chars (2 cau) la SWEET SPOT — du anchor, khong loop, khong leak.

---

## Production decision: Keep BOTH file voice clone

- `tuan_anh_5s_1sent_amp.pt` (v1 GOOJODOQ) — cho content marketing/review (nang luong cao)
- `tuan_anh_v3_voice_msg_10s.pt` (v3 voice_msg) — cho content doi thuong/casual (thu gian)

Anh co the switch giua 2 file `.pt` bang cach doi `--prompt` flag khi generate.

---

## Related: emotion tags interaction with target text repetition

**Tested:** v3 file voice clone voi target text co REPETITION (cau "Toi la Tung Anh" lap 4 lan).

**Result:**
- Whisper STILL detects repetition (vi target text that nhien)
- Peak -2.0 dB (tot, khong co silent bug)
- Duration 22.32s (vi target text dai)

**Conclusion:** v3 file voice clone OK cho target text co repetition. Neu muon tranh lap, dung v1 (target text khong lap).

---

## Quick reference: 3 prompt files khi nao dung

| Use case | File voice clone | ref_audio source |
|---|---|---|
| Content marketing (review, TikTok video) | `tuan_anh_5s_1sent_amp.pt` | 5s tu GOOJODOQ video |
| Content casual/storytelling (voice message style) | `tuan_anh_v3_voice_msg_10s.pt` | 10s tu Telegram voice |
| Multi-speaker hoac nuoc ngoai | TODO — clone them | (anh can gui voice moi) |
