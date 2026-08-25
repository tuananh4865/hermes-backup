# PITFALL #88 — After ship.sh, ALWAYS report md5 + path proactively (anh flag 23/07)

**Detected:** 23/07/2026 by anh Tuấn Anh saying "Không thấy file này" after clip 0034 V1_76 ship.

## Symptom

Em chạy `ship.sh` thành công → file `.mp4` được copy ra `Pocket3/Hermes-Edit/clip_<id>_V1_<NNs>_FINAL_<sp>.mp4`. Em báo cáo "Đã ship" với anh nhưng KHÔNG kèm evidence chi tiết. Anh không thấy file (3 khả năng: iCloud sync chưa, nhầm folder, file browser cache).

## Fix

Sau mỗi lần `ship.sh` PASS, BẮT BUỘC report theo format:

```
✅ SHIPPED
  Path: /Volumes/Storage-1/Pocket3/Hermes-Edit/clip_<id>_V1_<NNs>_FINAL_<sp>.mp4
  Size: <X.XX> MB
  Duration: <X.XX>s
  MD5: <hash>
  TikTok spec: <PASS/FAIL> (resolution x fps x codec)
```

`MD5` ở đây quan trọng — em có thể verify file thực tế trên disk = file em claim đã ship.

```bash
# Auto-collect evidence sau ship.sh
SHIP_FILE="/Volumes/Storage-1/Pocket3/Hermes-Edit/clip_${CLIP}_V${VER}_${DUR}_FINAL_${SP}.mp4"
echo "Path: $SHIP_FILE"
ls -la "$SHIP_FILE"
echo "Size: $(stat -f%z "$SHIP_FILE" | awk '{printf "%.2f MB", $1/1024/1024}')"
echo "Duration: $(ffprobe -v error -show_entries format=duration -of csv=p=0 "$SHIP_FILE")"
echo "MD5: $(md5 -q "$SHIP_FILE")"
echo "TikTok spec:"
python3 scripts/check_tiktok_spec.py "$SHIP_FILE"
```

## Related

- PITFALL #84 (ship.sh không gate verify) — bug chưa fix
- Hard rule 5-Evidence gate (universal) — không claim "done" khi không có md5 + path + size

## Lesson

Mỗi lần user hỏi "file đâu?", nếu em đã proactive report md5 ngay lúc ship → user check ngay được, không mất turn debug "file ở đâu". **Save turn = save time**.