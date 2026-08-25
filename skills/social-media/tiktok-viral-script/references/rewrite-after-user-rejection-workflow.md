# Rewrite After User Rejection — Workflow chuẩn

**Trigger:** User nói `"viết lại" / "rewrite" / "đổi chủ đề" / "câu từ lủng cũng" / "không ổn"` sau khi em đã giao script.

**Why this workflow exists:** Trong 1 session 18/06/2026, user phải yêu cầu viết lại **3 LẦN** liên tiếp. Mỗi lần em mất 10-15 phút vì:
- Lần 1: Quên check file canonical → user phải nhắc "CapCut quá phổ biến"
- Lần 2: Quên self-review → user phải nhắc "câu từ lủng cũng"
- Lần 3: Quên cite file change → user phải nhắc "check hoàn thành"

Workflow này giúp em làm đúng ngay lần đầu.

## Workflow 4 bước (apply MỌI khi user nói "viết lại" / "không ổn")

### Step 1: Self-Diagnose (30 giây — ĐỪNG defensive)

Đọc lại script vừa viết. TỰ TÌM 3-5 chỗ chưa tốt:

| Anti-pattern | Dấu hiệu | Cách fix |
|--------------|-----------|----------|
| **Liệt kê khô** | "Một X, hai Y, ba Z" — không có câu chuyện | Wrap thành narrative: "3 năm trước, anh lần đầu mua... tưởng 'xịn'" |
| **Bullet thay câu** | "Bước 1/2/3" — đọc như manual | Conversational: "Làm thử đêm nay — sáng mai khác hẳn" |
| **Câu cuối yếu** | "...thì OK chứ" / "...thế thôi" | Strong close: "0 đồng thế này thì quá ngon" |
| **Từ Hán Việt cứng** | "Khắc phục" / "ngăn chặn" | Từ thuần Việt: "xử lý" / "chặn" |
| **Cliché** | "như ngày với đêm" / "rõ ràng" | Cụ thể hơn: "khác nhau 10 lần" |

### Step 2: Báo cáo cụ thể (ĐỪNG nói chung chung)

```markdown
Anh nói đúng — em thấy [N] chỗ chưa tự nhiên:
1. Câu "..." = [liệt kê khô / cliché / yếu close]
2. Câu "..." = [vấn đề cụ thể]
3. Câu "..." = [vấn đề cụ thể]
```

**ĐỪNG nói:** "Anh góp ý đi em sửa" → user phải tự tìm lỗi.

**PHẢI nói:** "Em đọc lại thấy [N] chỗ — để em fix luôn".

### Step 3: Viết lại + SO SÁNH trước/sau

Sau khi viết lại, list bảng TRƯỚC vs SAU cho user thấy rõ cải thiện:

| Câu cũ | Câu mới | Tại sao tốt hơn |
|--------|---------|------------------|
| "Anh từng mua mic Boya 500k, mic USB 1.5 triệu, mic DJI 2 triệu" | "3 năm trước, anh lần đầu mua mic Boya 500k — tưởng 'xịn'. Rồi mic USB 1.5 triệu, mic DJI 2 triệu. Tổng 4 triệu." | Có narrative + build-up |
| "Khác biệt rõ như ngày với đêm" | "khác nhau 10 lần" | Cụ thể hơn |
| "Bước 1: mở Control Center, bấm Mic Mode" | "Bước 1: mở Control Center, bật Voice Isolation" | Rút gọn |

### Step 4: Update checklist + log

**SAU khi user confirm "OK rồi" → tự động:**
1. Move task trong `Operations/CHECKLIST-PROJECT.md`: 🔴 ĐANG LÀM → 🟢 ĐÃ LÀM
2. Append entry vào `CHANGELOG.md` (format chuẩn)
3. Append entry vào `~/wiki/log.md`

**ĐỪNG để user nhắc "update checklist" — làm tự động.**

## Real Workflow Example (18/06/2026 — 3 lần viết lại Ngày 2)

| Lần | Trigger của user | Em sai gì | Em fix |
|-----|-------------------|----------|-------|
| 1 | "Viết tiếp ngày 2 đi" | Em tự pick E1.1 (CapCut) — KHÔNG check file canonical | Check `series-xay-kenh-0-dong.md` → đề xuất B1 Mic |
| 2 | "B1 thay vì mic tai nghe thì thay mic iPhone" | Em KHÔNG nghe rõ "thay vì mic tai nghe" | Đổi sang mic iPhone |
| 3 | "câu từ lủng cũng quá, kiểm tra và viết lại!" | Em gửi draft 1 lần không self-review | Self-review 4 bước → rewrite |

**Tổng thời gian lãng phí:** ~30 phút (3 lần × 10 phút).

**Nếu áp workflow này NGAY LẦN ĐẦU:**
- Lần 1: Check file canonical → B1 ngay (không cần ask)
- Lần 2: Nghe kỹ "thay vì mic tai nghe" → đổi sang iPhone ngay
- Lần 3: Self-review 4 bước → gửi bản final đúng

**Kết quả:** ~5 phút thay vì 30 phút.

## Anti-patterns của agent khi user nói "viết lại"

❌ **Defensive:** "Anh xem kỹ chưa?" / "Em thấy ổn mà?" — ĐỪNG bao giờ
❌ **Generic:** "Em sẽ cải thiện" — ĐỪNG nói chung chung
❌ **Tự đoán vấn đề:** "Có phải anh muốn thay đổi X không?" — ĐỪNG hỏi user phải tự tìm
❌ **Viết lại không thông báo:** User phải đoán xem em sửa gì
❌ **Quên update checklist:** User nhắc "check hoàn thành" mới update

✅ **ĐÚNG:**
- "Đọc lại em thấy [N] chỗ chưa tự nhiên — để em fix luôn"
- "Báo cáo: sửa 3/5 vấn đề, còn 2 cần user confirm"
- "Trước: A → Sau: B (tốt hơn vì X)"
- "Đã update checklist + CHANGELOG"

## Checklist TRƯỚC KHI viết script mới (gating)

```bash
SCRIPT_FILE="$1"

# Step 1: Check file canonical đã đọc chưa
echo "=== Check canonical files ==="
test -f "/Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/series-xay-kenh-0-dong.md" && echo "OK series-xay-kenh-0-dong.md" || echo "❌ Missing"
test -f "/Volumes/Storage-1/Workspace/Claude/Projects/Content Creator/Research/2026-06-17/02-CURRICULUM-NGUOI-MOI-BAT-DAU.md" && echo "OK curriculum" || echo "❌ Missing"

# Step 2: Check anti-patterns trong script
echo "=== Style check ==="
grep -cE "rõ ràng|như ngày với đêm|chắc chắn|không thể phủ nhắn|khắc phục|ngăn chặn" "$SCRIPT_FILE"
# Cần = 0

# Step 3: Check bullet liệt kê trong HOOK/SET UP/CTA (chỉ cho phép trong PAY OUT)
echo "=== Bullet check ==="
grep -cE "^(\d+\.|•|-) " "$SCRIPT_FILE"
# Cần ≤ số bullet trong Pay out (nếu hook có "5 điều" thì pay out phải có 5 bullet)

# Step 4: Check câu dài
echo "=== Long sentence check ==="
awk '{ if (length($0) > 100) print NR": "length($0)" chars" }' "$SCRIPT_FILE"
# Cần = 0 dòng > 100 chars

# Step 5: Check framework 4 tử huyệt + 5 phần
echo "=== Framework check ==="
grep -E "Tử huyệt:|Hook:|Set up:|Tension:|Pay out:|CTA:" "$SCRIPT_FILE" | wc -l
# Cần ≥ 6 matches
```

**Rule:** Chạy checklist TRƯỚC khi gửi script. Nếu fail → fix inline → re-check → gửi.

## Khi user nói "không hiểu" / "không rõ" / "nghe cứng"

Đây là dấu hiệu script cần **reformat**, KHÔNG rewrite hoàn toàn:

| Triệu chứng | Action |
|-------------|--------|
| "Câu từ lủng cũng" | Self-review → fix anti-patterns (Step 1-2) |
| "Không hiểu ý" | Re-read brief → clarify với user → viết lại |
| "Không ổn" | ĐỪNG defensive → hỏi user cụ thể: "Anh thấy chỗ nào chưa ổn?" |
| "Đổi chủ đề" | KHÔNG tự pick chủ đề mới → check file canonical trước |

## Lesson lớn nhất (18/06/2026)

**User thường "phản hồi bằng số" (1, 2, 3) khi có nhiều options.** Khi user nói "viết lại" mà KHÔNG nói rõ phải sửa gì → tự diagnose → báo cáo cụ thể → để user confirm.

User thường KHÔNG có thời gian đọc lại toàn bộ script và list 5 chỗ lỗi → em PHẢI tự tìm và báo cáo. 1 phút self-review = tiết kiệm 15 phút user phải đọc lại và nhắc lỗi.

**Rule cuối cùng:** MỖI lần user nói "viết lại" / "không ổn" → coi như có anti-pattern trong script → fix NGAY lần viết lại, KHÔNG để user phải nhắc lần 2.