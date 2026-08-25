# Deep Research 3-Pillar Saturation — Workflow Nghiên Cứu Sâu Song Song

> **Created:** 2026-06-17 (session deep research 3 trụ EDIT+SETUP+ÁNH SÁNG)
> **Trigger:** User says "deep research về N trụ cột" / "nghiên cứu sâu N mảng song song" / "cần kho chữ dày cho N giai đoạn tới"
> **Use case:** Khi cần kho chữ đủ cho 60-100 video/30-45 ngày, nghiên cứu nhiều trụ cùng lúc.

---

## TẠI SAO WORKFLOW NÀY TỒN TẠI

Session 17/06: Anh pivot sang 3 trụ EDIT+SETUP GÓC QUAY+ÁNH SÁNG CƠ BẢN với mục tiêu 10.000 follow/45 ngày. Cần kho chữ đủ cho 90 video. Workflow chạy 3 subagent song song → tạo ra 3 file research (40KB + 30KB + 45KB) tổng cộng 115KB markdown, 85+ kịch bản, ma trận 90 video/45 ngày.

## WORKFLOW 5 BƯỚC

### Bước 1: Xác định trụ cột + kho chữ mục tiêu
- Mỗi trụ = 1 mảng nội dung cần research độc lập
- Kho chữ mục tiêu: ~30 kịch bản/trụ × N trụ = N×30 kịch bản
- Mỗi trụ cần ≥5 nguồn uy tín quốc tế + 2-3 nguồn Việt Nam (nếu áp dụng tại VN)
- Output: 1 file `00-TONG-HOP-N-TRU-COT.md` (ma trận) + N file `deep-research-[ten-tru].md` (chi tiết)

### Bước 2: Chạy song song N subagent (mỗi trụ 1 subagent)
- Dùng `delegate_task(tasks=[...])` với max_concurrent = 3
- Mỗi subagent có:
  - `goal`: rõ ràng, đo đếm được (VD: "Tổng hợp 30 kịch bản + 8 kỹ thuật + 12 lỗi thường gặp")
  - `context`: bối cảnh, đối tượng, mục tiêu ứng dụng
  - `output path`: absolute path
  - `format yêu cầu`: markdown, section cụ thể, nguồn có URL
- Mỗi subagent chỉ dùng `mcp_MiniMax_web_search` (KHÔNG dùng `web_extract` — hay timeout)

### Bước 3: Handle timeout (NẾU có subagent fail)
- Nếu 1/N subagent timeout → ĐỪNG retry cả batch
- Restart riêng subagent đó với context tóm tắt từ output trước
- Trong subagent restart, **ÉP RÕ** "KHÔNG dùng web_extract, chỉ dùng mcp_MiniMax_web_search với 8-10 query chất lượng, lấy snippet thay vì full page"
- Subagent restart thường chạy nhanh hơn vì đã biết topic

### Bước 4: Verify output đủ chất lượng
Check từng file:
- [ ] File có tồn tại đúng path?
- [ ] Line count > 300 (tương đương 20-30KB)?
- [ ] Có section "KỊCH BẢN CỤ THỂ" hoặc tương đương với ≥20 kịch bản?
- [ ] Có nguồn tham khảo có URL + ngày?
- [ ] Có số liệu cụ thể (không bịa)?
- [ ] Có case study hoặc ví dụ thực tế?

Nếu thiếu → yêu cầu subagent bổ sung section đó (KHÔNG viết lại từ đầu).

### Bước 5: Tổng hợp + tạo file ma trận
Tạo file `00-TONG-HOP-N-TRU-COT.md` với:
- Bản đồ N trụ + kho chữ (ma trận)
- Phân bổ video theo ngày/tuần/3-giai-đoạn
- Checkpoint KPI theo mốc (N7, N15, N30, N45)
- Ưu tiên khai thác + lý do (cạnh tranh, lợi thế, dễ viral)
- Action items cho session tiếp theo

**Cập nhật đồng thời (KHÔNG hỏi user):**
- `00-ban-do-tong.md` — đổi đích N ngày
- `hub.md` — thêm section pivot + link file research
- `CHANGELOG.md` — ghi nhận session

---

## ⚠️ PITFALLS (BÀI HỌC SESSION 17/06)

### 1. `web_extract` trong subagent hay timeout
- **Triệu chứng:** Subagent chạy 600s rồi fail, không có output
- **Nguyên nhân:** `web_extract` thường timeout với long URLs hoặc paywall sites
- **Fix:** ÉP subagent chỉ dùng `mcp_MiniMax_web_search` với snippet là đủ
- **Verify:** Subagent chạy < 500s, output đủ dùng

### 2. Subagent timeout KHÔNG phải là fail
- **Triệu chứng:** 1/N subagent timeout, các subagent khác OK
- **Xử lý ĐÚNG:** Restart riêng subagent đó với context tóm tắt
- **Xử lý SAI:** Retry toàn bộ batch (lãng phí thời gian, lặp lại việc đã xong)
- **Verify:** Sau restart, tất cả N/N file đều có, không cần chạy lại subagent OK

### 3. Đừng quá tham lam về kích thước file
- 1 file 30-50KB là đủ cho 25-30 kịch bản
- Ép subagent viết 100KB+ thường dẫn đến lặp content hoặc bịa số
- Nếu cần nhiều hơn → chia thành 2 subagent cho cùng trụ

### 4. Phải tạo "ma trận phân bổ" chứ không chỉ list kịch bản
- 85+ kịch bản list thẳng → khó áp dụng
- Ma trận 90 video × 45 ngày × 3 trụ → actionable
- Ma trận phải có: video nào, ngày nào, giai đoạn nào, tỷ lệ trụ bao nhiêu

### 5. Update file pivot (hub.md, 00-ban-do-tong.md) NGAY trong session
- **ĐỪNG** chờ user confirm rồi mới update
- **NÊN** update song song với việc tạo file research
- User sẽ tự check hub.md ở session sau, không cần hỏi lại "đã update chưa"

---

## OUTPUT PATHS CHUẨN (CONTENT CREATOR PROJECT)

```
Research/
└── YYYY-MM-DD/
    ├── 00-TONG-HOP-N-TRU-COT.md       (ma trận, ~13KB)
    ├── deep-research-[ten-tru-1].md   (chi tiết trụ 1, ~30-50KB)
    ├── deep-research-[ten-tru-2].md   (chi tiết trụ 2, ~30-50KB)
    └── ...                            (trụ N)
```

**Đặt tên file:**
- `ten-tru` = kebab-case, không dấu, mô tả rõ (VD: `edit-co-ban`, `setup-goc-quay`, `anh-sang-co-ban`)
- File ma trận bắt đầu bằng `00-` để sort trước

---

## OUTPUT MẪU SESSION 17/06

**Input:** User yêu cầu "deep research về 3 trụ cột nội dung để khai thác sâu và chuẩn được toàn bộ 3 trụ cột nội dung đó"

**Quy trình:**
1. Xác định 3 trụ: EDIT + SETUP GÓC QUAY + ÁNH SÁNG CƠ BẢN
2. Kho chữ mục tiêu: 30+25+30 = 85 kịch bản
3. Chạy 3 subagent song song (max 3 concurrent)
4. Kết quả: 2/3 OK, 1 timeout (SETUP GÓC QUAY)
5. Restart subagent timeout với chỉ dẫn "KHÔNG dùng web_extract"
6. Verify: 3/3 file có, 115KB tổng, 85+ kịch bản
7. Tạo ma trận: 90 video/45 ngày, checkpoint N7/N15/N30/N45
8. Update pivot files: hub.md + 00-ban-do-tong.md + CHANGELOG.md

**Lợi thế cạnh tranh phát hiện được:** ÁNH SÁNG ít người dạy đúng → đây là rare competitive advantage cho kênh giáo dục.

**Thời gian:** ~10 phút cho 3 subagent (1 restart) + 5 phút tổng hợp + 2 phút update pivot files = ~17 phút tổng.

---

## CÔNG THỨC REUSE

Khi user yêu cầu "deep research N trụ / mảng nội dung" trong tương lai:

1. **Confirm N trụ + mục tiêu kho chữ** (1 câu hỏi duy nhất nếu ambiguous)
2. **Chạy N subagent song song** (max 3 concurrent)
3. **Restart timeout với chỉ dẫn rõ** (KHÔNG dùng web_extract)
4. **Verify từng file** (checklist 6 tiêu chí)
5. **Tạo ma trận** (90+ video × checkpoint KPI)
6. **Update pivot files NGAY** (hub.md, 00-ban-do-tong.md, CHANGELOG.md)

**KHÔNG** hỏi user confirm từng bước. Workflow này đã verify 17/06.
