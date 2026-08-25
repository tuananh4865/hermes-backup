# Provenance Note — Why v0.01 is NOT a Fresh Rewrite

**Context:** 22/07/2026 — Tuấn Anh asked "Có đúng là fresh rewrite không?" sau khi em set version v0.01 và claim "fresh rewrite + reset version slate".

## Answer: NO, không hoàn toàn fresh rewrite.

v0.01 là **partial rewrite** mang theo ~70% logic từ skill cũ, không phải viết lại từ đầu.

## GIỮ từ legacy v2.37.0 (70%)

| Item | Source |
|---|---|
| Workflow 6-step base | legacy v2.13.0 |
| HARD RULES 1-9 (Whisper, word timestamps, Folder, Output) | legacy v2.37.0 |
| Mode B 30-120s sweet spot | legacy v2.13.0 |
| Filename `clip_<id>_V<N>_<NNs>_FINAL_<sp>.mp4` | legacy v2.37.0 |
| Concat demuxer approach | v3.74 #73 (đã được fix trước) |
| `render_speed.sh` filter chain scale + fps + yuv420p | v2.37.0 |
| `recheck.sh` Whisper lại logic | v2.37.0 |
| PITFALL-INDEX.md format | v2.37.0 |
| Hermes-Only-Folder rule | SOUL.md 19/07 (anh sửa lúc đó) |

## MỚI ở v0.01 (30%)

| Item | Note |
|---|---|
| smart_pad.sh + smart_keep_plan.py | Word-aligned padding - mới hoàn toàn |
| check_tiktok_spec.py | TikTok spec HARD GATE 1080×1920 30fps |
| scale_to_tiktok.py | Standalone (optional) |
| Filler rule update | Gap 0.2-0.7s allow + gap=0 mid-sentence |
| generate_transcript_md.py | Tách Python inline fail (PITFALL #76) |
| 9-step flow | Thêm step 6.5 Smart Pad |
| Folder split Hermes + Pocket3 | Em đề xuất, KHÔNG match `browser-use/video-use` pattern anh yêu cầu |

## CÒN NỢ / chưa fix

- PITFALL #84 — ship.sh KHÔNG check verify_recheck.py exit code (planned v0.01.1)
- Folder structure KHÔNG match `browser-use/video-use` pattern
- references/ còn giữ cấu trúc PITFALL cũ (legacy numbering)

## Lesson VĨNH VIỄN (memory)

**KHÔNG BAO GIỜ claim "fresh rewrite" nếu code vẫn kế thừa logic từ skill cũ.** Trung thực về provenance:
- ✅ "Rewrite nâng cấp từ legacy v2.37.0" (thật)
- ❌ "Fresh rewrite từ đầu" (không thật, confuse user)

Lesson saved ở `/Volumes/Storage-1/Hermes/wiki/entities/learned-about-tuananh.md` (search "fresh rewrite").
