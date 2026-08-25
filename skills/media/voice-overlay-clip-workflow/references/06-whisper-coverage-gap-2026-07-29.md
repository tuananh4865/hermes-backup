# 06 — Whisper Transcript Coverage Gap

## TL;DR
`Whisper` (large-v3-mlx, language=vi) cho tỷ lệ **ordered exact word coverage ~98.7%** so với source text, nhưng KHÔNG bắt được:
- **Filler vocalizations** từ non-verbal emotion tags: `ờ`, `ừm`, `à`, `ồ`, `ờm`, `ựm`
- **Trailing-vowel elongation**: `Tộiiiii` Whisper transcribe thành `Tối` (0.4s) trong khi waveform thực tế là 0.6s RMS-active
- **Hallucinated numbers**: `2 hiệp` → `2 không lẻ 8`

→ Coverage 98.7% không guarantee voice "sạch". Whisper chỉ verify **TỪ có nghĩa**, không verify **âm thanh đệm**.

## Nguyên nhân
- Model Whisper được train ASR (speech → text), không phải filler-tagger.
- Filler `ờ`, `ừm` không phải content (low semantic weight) → decoder skip.
- Emotion tags prepend phoneme đơn lẻ mà Whisper map về silence hoặc text gần nhất.

## QA bắt buộc bổ sung
1. **Audio RMS scan** đầu/cuối segment — phát hiện filler vocalization.
2. **Listen test** — Whisper không thay thế tai người.
3. **Segment-by-segment analysis** — aggregate transcript PASS nhưng segment đơn lẻ FAIL.

## Emotion tags risk matrix
| Tag | Risk | Note |
|---|---|---|
| `[question-ah]` | HIGH | Phoneme "à" đầu đoạn |
| `[question-oh]` | HIGH | Phoneme "ô" đầu đoạn |
| `[surprise-ah/oh/wa/yo]` | HIGH | Phoneme đầu đoạn |
| `[laughter]` | LOW-MEDIUM | Không filler thường |
| `[sigh]` | LOW | Hơi thở, acceptable |
| `[confirmation-en]` | LOW | Ngắn |

## Default rule (codified in SKILL.md, verified 2026-07-29)

**ZERO emotion tags** unless user explicitly requests a tag that has been A/B-tested safe.

User verbatim 2026-07-29:
> *"Anh thấy có ựm ờ trong voice mà"*
> *"Chung quy anh muốn loại bỏ hoàn toàn ựm ờ à ồ ờm ừm đi và từ nay không được phép chèn các emotional tag có thể tạo ra các từ đó nữa"*

## Verification recipe
```bash
# RMS scan cho filler ở 0.5s đầu/cuối segment
for f in segments/*.wav; do
  head_rms=$(ffmpeg -nostats -hide_banner -i $f -af "atrim=start=0:end=0.5,asetnsamples=1" -f null - 2>&1 | grep -oP 'rms=\K[0-9.]+' | head -1)
  echo "$f: head_rms=$head_rms (caution if >1500)"
done

# Transcript score
whisper-transcribe output.mp3 | head
# difflib.SequenceMatcher autojunk=False for ordered coverage %
```

## Anti-pattern
Tin Whisper transcript pass → ship. Sai. Bắt buộc listen test trước khi giao MP3 cho user.

## Related
- SKILL.md Pitfall #13 (trailing vowel)
- SKILL.md Pitfall #15 (number hallucination)
- SKILL.md Pitfall #16 (RMS verification mandatory)
