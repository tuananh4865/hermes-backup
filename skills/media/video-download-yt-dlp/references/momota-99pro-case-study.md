# Case Study: Multi-Attribute Image Search — Momota + 99 Pro Gen 3 (2026-06-30)

> Real failure mode that cost 3 retry rounds + user frustration. Read this when a user asks for an image with **multiple specific attributes** (person + equipment, person + event, object + version + color).

## The Request

User asked (in 4 escalating rounds):

1. **R1:** "Tìm hiểu cho anh vợt yonex astrox 99 pro 2025, thông số chi tiết, hình ảnh và hình ảnh các vận động viên nổi tiếng đã sử dụng nó!"
2. **R2:** "Tìm và tải về hình ảnh kento momota cầm vợt 99pro gen 3 sau đó gửi vào telegram cho anh"
3. **R3:** "Tìm hình ảnh kento momota ở giải kingcup 2025 đi"
4. **R4:** "Dùng browser để tìm và xem kĩ ảnh nào momota có cầm 99 pro gen 3 thì hãy tải về gửi anh! Nãy giờ em toàn tải sai ảnh"

User picked **Option 1** from reframe: "ảnh sản phẩm 99 Pro Gen 3 đen/xanh (không cần Momota)".

## The Failures (4 rounds, all sub-optimal)

### R1: Generic research answer
- ✅ Compiled good specs sheet (weight, balance, string tension, etc.)
- ❌ Did NOT include any actual image of the racket itself
- ❌ Did NOT explicitly call out which VĐV currently uses 99 Pro Gen 3 in 2025 active play

### R2: Download wrong racket generation
- Searched Wikimedia Commons for "Kento Momota" → downloaded 1 image
- Vision-verified: ✅ đúng Momota, ❌ nhưng vợt là **Gen 2 White Tiger** (cam/đỏ) — KHÔNG phải Gen 3 (đen/xanh) như user yêu cầu
- **User pushback:** none yet (R2 was a one-shot ask)

### R3: Download wrong people (filename misleading)
- User: "Momota ở King Cup 2025"
- Searched BadmintonPlanet → 5 image URLs with Momota-related filenames
- Downloaded all 5 → vision-verified:
  - 1: Real (Momota + Lin Dan group photo)
  - 2: Real (Momota + Lin Dan on stage with "2025 NIGHT OF THE KING" banner)
  - 3: **WRONG** — Indonesia VĐV, not Momota
  - 4: **WRONG** — 2 people at dinner with pink hair, unrecognizable
  - 5: **WRONG** — small thumbnail, could not verify
- Deleted 3 bad images, sent 2 verified
- **User pushback:** none yet (R3 was delivered)

### R4: Three rounds in, finally said "this image doesn't exist"
- User: "Dùng browser để tìm kĩ ảnh Momota cầm 99 Pro Gen 3"
- Tried `computer_use` → Mac in lock screen, no Safari → fallback to curl + grep
- After MORE research, finally realized the **root cause**:
  - Momota retired: **2024-05**
  - 99 Pro Gen 3 launched: **2025-09**
  - → 16-month gap → Momota NEVER played competitive match with Gen 3
  - → EquipmentStack.com: "Seen in post-retirement exhibition" (only source for that combo)
- **User pushback:** "Nãy giờ em toàn tải sai ảnh" — frustrated, called out the pattern
- **My response:** Honest report + 3 options (product only / Gen 2 / stock photo)
- User picked Option 1 (product only) → I delivered 4 verified images

## What I Should Have Done at R1

If I had run pre-flight fact-check at the very first round, I would have noticed:

1. "99 Pro 2025" = Gen 3 (đen/xanh, launch 2025-09)
2. "VĐV nổi tiếng sử dụng" = need VĐV currently active in 2025
3. **Momota retired 2024-05** → NOT eligible
4. Active 2025 players with 99 Pro Gen 3: Alex Lanier (switched Oct 2025), Kodai Naraoka

If user had wanted Momota specifically, I should have noted: *"Momota đã giải nghệ 2024-05, trước khi Gen 3 ra mắt 2025-09. Ảnh Momota cầm Gen 3 chỉ có ở exhibition hậu trường. Anh muốn ảnh (a) Momota + 99 Pro đời cũ, hay (b) 99 Pro Gen 3 với VĐV đang thi đấu 2025?"*

## The 4-Lesson Takeaway

### Lesson 1: Pre-flight fact-check is non-negotiable

For any multi-attribute image search, the **FIRST** 30 seconds should be:
- "Does this combination exist?" (timeline check: retirement date vs launch date, event date vs object era, person vs sport)
- "What's the closest approximation if it doesn't?" (Gen 2 instead of Gen 3, current player instead of retired legend)

If the combination doesn't exist, **refuse upfront** with honest framing — not after 4 rounds.

### Lesson 2: Vision-verify EVERY image, even if filename matches

Filename `momota_shiyuqi_drinks.jpg` ≠ image of Momota and Shi Yuqi drinking. Filename is editorial metadata, not content guarantee.

Rule: download → vision-verify → delete mismatches → send verified. Always.

### Lesson 3: Max 2 round failure on the same request

If Round 1 fails (wrong person, wrong object, wrong event), don't just retry with same approach. **Reframe** with options.

If Round 2 still fails, **stop downloading**. Report status + propose alternatives. Get user buy-in before continuing.

### Lesson 4: "Dùng browser" means switch tool, not pretend

User saying "browser" is a **direct instruction** to use `computer_use`. If `computer_use` is blocked (lock screen, no GUI), tell the user immediately. Don't silently fall back to curl and call it the same.

## When This Pattern Repeats

Watch for these **trigger phrases** that signal a high-risk multi-attribute image search:

- "ảnh [người] cầm [vật]" (image of person holding object)
- "ảnh tại [giải/sự kiện]" (image at event)
- "[vật] màu [color] [version]" (object with specific color/version)
- "[brand] [model] [year]" (specific product)
- "logo/poster của [công ty] [năm]" (brand asset by year)

For all of these: **pre-flight fact-check FIRST**, download SECOND, vision-verify THIRD, report LAST.

## Related Skill Sections

- `I5`: Ảnh đúng người nhưng vợt KHÔNG đúng đời
- `I7`: Filename từ search results LIE về content
- `I10`: Multi-attribute match required (Person + Equipment/Object)
- `I11`: Pre-flight fact-check TRƯỚC khi tải
- `I12`: Max 2 round failure (fail-fast)
- `I13`: When combination doesn't exist, refuse upfront
- `I14`: User says "browser" → use `computer_use`, don't fake it

## User Preference Reference

See `~/.hermes/memories/USER.md` section: `[PREFERENCES - IMAGE SEARCH/DOWNLOAD TASKS]` for the user-level rule. (Note: as of 2026-06-30, the user-side memory file had drift corruption; this skill carries the equivalent rule independently until memory is restored.)
