# Vietnamese Explainer Video — Case Study (2026-06-18)

## Source

**Video:** `p7d0k_QDFhs` — https://youtu.be/p7d0k_QDFhs
**Title:** "Bộ Não Điều Khiển Mọi AI Agent: Vòng Lặp ReAct"
**Channel:** **La La School** (verified từ Whisper cue 27: "Hãy subscribe cho kênh La La School")
**Duration:** 94.67s | **Views:** 1,182 | **Upload:** 2026-06-12

⚠️ **Hallucination trap (FIX 2026-06-18):** Visual style (kem + cam + bánh răng + minimalist) trông giống kênh "AI NEWS - AI Daily News" phổ biến → em đã hallucinate tên kênh này trong lần phân tích đầu. Whisper audio transcript cue 27 mới là source of truth: "Hãy subscribe cho kênh **La La School**".

**Rule:** Visual familiarity ≠ brand identity. Luôn verify tên kênh từ audio cue subscribe ở 3 cue cuối của SRT (thường chứa brand CTA). KHÔNG tự suy brand từ visual style quen thuộc.

## Pipeline Output

| File | Size | Purpose |
|---|---|---|
| `compressed.mp4` | 2.8MB | H.264 720p source |
| `summary.mp4` | 1.3MB | 95 frames @ 1fps + audio |
| `transcript.srt` | 3.1KB | Whisper Large v3, 31 segments |

## Visual Style (verified từ 6/12 frames)

- **Background:** Kem nhạt (off-white) — minimalism
- **Accent:** Cam đậm 1 tông duy nhất
- **Icon:** Vòng tròn cam + bánh răng trắng = AI Agent
- **Font:** Sans-serif đậm, viết hoa cho tiêu đề, thường cho sub
- **Highlight:** Keyword cam đậm trên nền kem
- **Animation:** Icon chuyển động theo vòng tròn, dashed line arrow, text fade in/out

## Narrative Arc (94.67s)

```
[0-5s]   HOOK         "AI TỰ CHẠY TỚI KHI XONG?" + icon file + gear + tick
[5-15s]  CONTEXT      "Bí mật = vòng lập ReAct" + diagram Reasoning + Acting
[15-25s] PROBLEM      "Trả lời 1 phát ăn ngay" + diagram Zero-shot (sai)
[25-50s] SOLUTION     Vòng tròn 3 nhịp NGHĨ → LÀM → QUAN SÁT
[50-65s] DEEP DIVE    "Nhịp LÀM = vươn ra ngoài" + 3 nhánh web/dữ liệu/$ chạy lệnh
[65-80s] INSIGHT      "Quan sát nối ngược về Nghĩ" + vòng lặp tự sửa sai
[80-95s] CTA          "Lưu video này để lần tới tự xây Agent"
```

## Transcript Excerpt (Whisper verified)

> "Bạn ra một câu lệnh, AI tự tìm kiếm, tự gọi công cụ, tự sửa sai cho tới khi xong việc."
> "Bí mật nằm ở một vòng lập tên là ReAct, ghép từ Reasoning và Acting."
> "ReAct bẻ cú trả lời một phát đó thành vòng lập ba nhịp: Nghĩ - Làm - Quan sát."
> "Lưu video này lại để lần tới tự xây Agent, bạn bắt đầu từ đúng cái vòng lập này."

## Key Lessons

1. **Hook câu hỏi 0-3s** + icon đơn giản → engagement cao dù channel nhỏ
2. **Visual tối giản** = dễ edit batch, nhất quán thương hiệu
3. **CTA cụ thể gắn use case** ("Lưu để lần sau làm X") tốt hơn CTA chung chung
4. **Không có talking head** → khó build parasocial bond (điểm yếu)

## VLM Rate-Limit Pattern

- 12 parallel calls → 6 success / 6 fail (Trace-Id `06827e...`)
- Retry với delay 5-15s giữa các batch → recovery rate ~50%
- Honest report: "Em phân tích được N/12 frames"
