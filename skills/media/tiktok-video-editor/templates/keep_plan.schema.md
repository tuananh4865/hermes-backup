# keep_plan.json Schema — tiktok-video-editor v3.78.0

File `keep_plan.json` ở `work/keep_plan.json` của mỗi project. AI agent viết sau khi đọc `transcripts/transcript.md`.

## Schema đầy đủ

```json
{
  "project_id": "0036",
  "decision_strategy": "compact Mode B 30-120s, focus main points",
  "ranges": [
    {
      "start": 0.0,
      "end": 8.5,
      "action": "KEEP",
      "reason": "hook + intro"
    }
  ],
  "skipped_ranges": [
    {
      "start": 8.5,
      "end": 10.0,
      "action": "SKIP",
      "reason": "filler + dead space"
    }
  ],
  "expected_duration": 79.6,
  "expected_mode": "B",
  "target_duration_post_speed": 61.2,
  "version": 2,
  "notes": [
    "Source: DJI_20260721095156_0036_D.MP4 (raw 4K, 163.4s)",
    "Topic: Review lens macro NAMMINH",
    "Skip filler 'thì các bạn có thể' ở 42.0-46.3s (CTA duplicate)"
  ]
}
```

## Required fields

| Field | Type | Required | Description |
|---|---|:---:|---|
| `project_id` | string | ✅ | 4-digit clip ID (e.g. "0036") |
| `decision_strategy` | string | ✅ | 1-2 sentence strategy summary |
| `ranges` | array | ✅ | List of KEEP ranges |
| `expected_duration` | float | ✅ | Total seconds of KEEP (pre-speed) |
| `expected_mode` | string | ✅ | "A" (full) hoặc "B" (compact) |
| `skipped_ranges` | array | optional | List of SKIP ranges với reason |
| `target_duration_post_speed` | float | optional | Expected after speed 1.3x |
| `notes` | array | optional | Context cho future re-edit |
| `version` | int | optional | Version của keep_plan (increment sau mỗi re-edit) |

## Range object schema

```json
{
  "start": <float seconds>,
  "end": <float seconds>,
  "action": "KEEP" | "SKIP",
  "reason": "<why>"
}
```

`reason` nên ngắn gọn, dùng những tag này:
- `"hook"` — first 5-10s, intro
- `"key_insight"` — main USP
- `"demo"` — product demo
- `"cta"` — call to action
- `"filler"` — filler cluster
- `"treo"` — incomplete sentence
- `"silence"` — gap > 1.5s
- `"pricing"` — price/sale mention
- `"duplicate"` — same phrase xuất hiện nhiều lần
- `"off_topic"` — tangent không liên quan

## Decision logic (4 signals)

Khi chọn keep vs skip, scan transcript word-by-word:

1. **Filler đầu câu** (`Thì|Ờ|À|Rồi|Nhé|Nha`) → SKIP
2. **Câu treo** (kết conjunction: `và|với|của|là|thì|mà|rồi|nhưng|đó|nữa`) → SKIP
3. **Silent gap** > 1.5s giữa 2 segments → SKIP (nếu filler thì split)
4. **Pricing** (`giá|triệu|tiền|$|shopee|lazada|tiki`) → SKIP (CTA OK ≤ 2 mentions)

Ngoài ra:
- **Anchor cluster** (`Các bạn|Tức là|Thì` ở transition) → KEEP
- **Topic-centric distribution** (TÊN SP mentioned 5+ lần spread >10s) → OK (anti-FP PITFALL #54)

## Mode A vs Mode B

- **Mode A (full):** expected_duration ≈ source duration - 10%. KEEP everything quan trọng. KHÔNG speed 1.3x.
- **Mode B (compact):** expected_duration 30-120s. KEEP main points + speed 1.3x ÷ ≈ 23-92s final.

## Example (real test 22/07)

```json
{
  "project_id": "0036",
  "decision_strategy": "compact Mode B 30-120s — focus main points về lens macro NAMMINH. V2: removed filler CTA.",
  "ranges": [
    {"start": 10.7, "end": 21.5, "action": "KEEP", "reason": "Hook + problem statement"},
    {"start": 26.6, "end": 33.9, "action": "KEEP", "reason": "Giới thiệu lens macro + USP"},
    {"start": 46.3, "end": 51.0, "action": "KEEP", "reason": "Build quality nhôm CNC"},
    {"start": 53.9, "end": 57.5, "action": "KEEP", "reason": "Hít trực tiếp pocket bar"},
    {"start": 67.4, "end": 69.8, "action": "KEEP", "reason": "Ống kính siêu cận"},
    {"start": 74.5, "end": 89.2, "action": "KEEP", "reason": "Demo quay cận cây bút 3cm"},
    {"start": 93.2, "end": 98.2, "action": "KEEP", "reason": "Key insight: 3cm focus"},
    {"start": 122.3, "end": 147.5, "action": "KEEP", "reason": "USP + value proposition"},
    {"start": 152.1, "end": 162.2, "action": "KEEP", "reason": "CTA link mua + cảm ơn"}
  ],
  "skipped_ranges": [
    {"start": 0.0, "end": 10.7, "action": "SKIP", "reason": "filler intro"},
    {"start": 21.5, "end": 26.6, "action": "SKIP", "reason": "silence_gap"},
    {"start": 33.9, "end": 42.0, "action": "SKIP", "reason": "filler context"},
    {"start": 42.0, "end": 46.3, "action": "SKIP", "reason": "V2 CTA filler skip"},
    {"start": 51.0, "end": 53.9, "action": "SKIP", "reason": "transition"},
    {"start": 57.5, "end": 67.4, "action": "SKIP", "reason": "duplicate ngoại hình"},
    {"start": 69.8, "end": 74.5, "action": "SKIP", "reason": "silence_gap + filler"},
    {"start": 89.2, "end": 93.2, "action": "SKIP", "reason": "dead_space"},
    {"start": 98.2, "end": 122.3, "action": "SKIP", "reason": "treo + duplicate x4"},
    {"start": 147.5, "end": 152.1, "action": "SKIP", "reason": "silence_gap"},
    {"start": 162.2, "end": 163.4, "action": "SKIP", "reason": "treo kết bình luận"}
  ],
  "expected_duration": 75.0,
  "target_duration_post_speed": 57.7,
  "expected_mode": "B",
  "version": 2,
  "notes": [
    "Source: DJI_20260721095156_0036_D.MP4 (raw 4K, 163.4s)",
    "Skip filler CTA đầu câu (PITFALL #77)",
    "Max 2 re-edit cycles (loop tolerance)"
  ]
}
```

## Validation

`build_concat_list.py` will:
1. Parse JSON
2. Sum KEEP ranges
3. Generate ffmpeg concat demuxer input file
4. Print expected_duration + actual computed duration

`verify_recheck.py` will:
1. Load recheck JSON
2. Check filler (must be 0)
3. Check câu treo signals (must be < 3)
4. Check pricing (must be ≤ 2 mentions)
5. Check duration delta vs expected/1.3 (tolerance ±8s)
