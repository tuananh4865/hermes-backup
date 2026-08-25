# PITFALL #89 — Subagent/background process output goes stale after fix; user sees old report

**Detected:** 23/07/2026 by anh Tuấn Anh: "Anh thấy báo cáo này của subagent step 8 và 9 có lỗi nè và subagent có render lại clip mới mà không thấy"

## Symptom

Background process `proc_46f3d422e037` chạy end-to-end clip 0034:
- Output recheck step 8: `Expected (post-speed 1.3): 58.8s, Actual final: 76.3s, Delta 17.42s ❌`
- Output ship step 9: `Ship: clip_0034_V1_58_FINAL_VACUUM.mp4`

SAU ĐÓ em phát hiện `expected_duration=76.49s` (keep_plan V2) sai → update thành V3 với `expected_duration=99.22s` → re-render → ship file mới `clip_0034_V1_76_FINAL_VACUUM.mp4` (76.36s, đúng).

Nhưng báo cáo subagent V1_58 vẫn còn trong context. User đọc output cũ thấy:
- V1_58 ship file không tồn tại trên disk
- Báo cáo FAIL trong khi thực tế PASS
- Confused → "không thấy file này"

## Fix

Khi em UPDATE state sau background process đã finished:
1. **Verify md5 file thực tế** trên disk trước khi báo cáo
2. **Nói rõ "superseded"** khi output background không còn accurate
3. **Background process output = EVIDENCE tại thời điểm nó chạy**, không phải truth hiện tại

```bash
# Sau khi fix expected_duration và re-ship:
echo "File hiện tại (verified just now):"
ls -la /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0034_V*.mp4
md5 -q /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_0034_V*.mp4

echo ""
echo "Background process proc_46f3d422e037 output V1_58 đã STALE:"
echo "  - V1_58 file không còn trên disk (em đã rm + re-ship)"
echo "  - Current ship = V1_76 (em re-render sau khi fix expected_duration)"
echo ""
echo "V1_76 là phiên bản cuối cùng, verified end-to-end:"
echo "  - md5: <hash>"
echo "  - duration: 76.36s"
echo "  - TikTok spec: PASS"
```

## Related

- PITFALL #75 (`set -e` + Python exit) — exit code capture pattern
- Hard rule 5-Evidence gate — không claim done nếu không verify md5 actual file
- Hook auto-mirror (PITFALL #81) — silent mirror có thể mask inconsistencies

## Lesson

**Background process output = SNAPSHOT, không phải TRUTH.** Khi em fix lỗi SAU background finished → báo cáo mới phải:
1. Verify md5 actual file
2. Explicitly mark superseded
3. Show current state vs background state

User nói "subagent có render lại clip mới mà không thấy" → em hiểu là user confused vì output background vs output final khác nhau. **Communicate transition explicitly.**