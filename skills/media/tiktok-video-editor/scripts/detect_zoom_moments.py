#!/usr/bin/env python3
"""
detect_zoom_moments.py — Auto-detect zoom moments từ keep_plan + transcript (NO VISION)

Anh Tuấn Anh preference 26/07: "em không thể liên tục dùng vision để hiểu video
nên phải chuyển sang phân tích transcript xem đoạn nào cần zoom in"

Workflow:
  1. Auto slow zoom cho ranges USP/DETAIL/SHOW/DESC (range-name signal)
  2. Auto punch zoom nếu range có verbal cue: deictic (đây/nè/đó) + show verb (thấy/nhìn)
  3. Auto punch zoom nếu range có product detail mention (transcript lexical match)
  4. HOOK giữ wide (no zoom - context setting)

Usage: python3 detect_zoom_moments.py <clip_id>
Output: tmp/<clip_id>/zoom_plan.json
"""
import json, os, sys


def load_audio_words(base):
    """Load all words từ audio.json với timestamps."""
    audio_json = f"{base}/audio.json"
    if not os.path.exists(audio_json):
        return []
    data = json.load(open(audio_json))
    words = []
    for seg in data.get("segments", []):
        for w in seg.get("words", []):
            words.append({
                "start": w["start"],
                "end": w["end"],
                "text": w["word"].strip().lower(),
            })
    return words


def find_deictic_show_moments(words, words_window=5):
    """Detect verbal cues: deictic (đây/nè/đó) gần show verb (thấy/nhìn/show)."""
    DEICTIC = {"đây", "nè", "đó"}
    SHOW = {"thấy", "nhìn", "show"}
    moments = []
    seen = set()
    for i, w in enumerate(words):
        if w["text"] in DEICTIC:
            for j in range(i, min(i + words_window, len(words))):
                if words[j]["text"] in SHOW:
                    t = round(w["start"], 1)
                    if t not in seen:
                        seen.add(t)
                        moments.append({
                            "start": w["start"],
                            "end": words[j]["end"],
                            "type": "punch",
                            "trigger": f"deictic({w['text']})+show({words[j]['text']})",
                            "peak_scale": 1.4,
                        })
                    break
    return moments


def find_product_detail_moments(words, range_start, range_end):
    """Detect product detail mentions trong range."""
    PRODUCT_NOUNS = [
        "đầu chổi", "carbon fiber", "sợi carbon", "chổi lông",
        "ron", "ốp", "body", "kích thước", "pin", "nút bấm",
        "logo", "chỉ may", "khóa", "lỗ", "ngăn",
    ]
    range_words = [w for w in words if range_start <= w["start"] <= range_end]
    text_lower = " ".join(w["text"] for w in range_words)
    found = []
    for noun in PRODUCT_NOUNS:
        if noun in text_lower:
            found.append(noun)
    return found


def detect_zoom_plan(clip_id):
    """Detect zoom plan cho 1 clip dựa trên transcript + keep_plan (không dùng vision)."""
    base = f"/Volumes/Storage-1/Pocket3/Hermes-Edit/tmp/{clip_id}"
    keep_plan_file = f"{base}/keep_plan.json"
    if not os.path.exists(keep_plan_file):
        print(f"❌ keep_plan.json not found: {keep_plan_file}")
        sys.exit(1)

    kp = json.load(open(keep_plan_file))
    words = load_audio_words(base)

    verbal_moments = find_deictic_show_moments(words, words_window=5)

    zoom_plan = []

    for keep in kp["keeps"]:
        name = keep["name"]

        # HOOK: giữ wide cho context setting
        if name == "HOOK":
            continue

        s = keep.get("start_padded", keep["start"])
        e = keep.get("end_padded", keep["end"])

        action = None

        # Rule 1: Range name signal → slow zoom (USP/DETAIL/SHOW/DESC)
        if name in ("USP", "DETAIL", "SHOW", "DESC"):
            action = {
                "type": "slow",
                "range_name": name,
                "start": s,
                "end": e,
                "start_scale": 1.0,
                "end_scale": 1.25,
                "reason": f"Range {name} thường show chi tiết SP → zoom in",
            }

        # Rule 2: Verbal cue (deictic+show) trong range → punch zoom
        verbal_in_range = [v for v in verbal_moments if s <= v["start"] <= e]

        # Rule 3: Product detail mention → punch zoom
        product_mentions = find_product_detail_moments(words, s, e)

        if verbal_in_range or product_mentions:
            cues = []
            if verbal_in_range:
                cues.append(f"verbal:{verbal_in_range[0]['trigger']}")
            if product_mentions:
                cues.append(f"product:{','.join(product_mentions[:2])}")
            action = {
                "type": "punch",
                "range_name": name,
                "start": s,
                "end": e,
                "at_time": (s + e) / 2,
                "duration": min(2.0, e - s),
                "peak_scale": 1.4,
                "reason": " + ".join(cues),
            }

        if action:
            zoom_plan.append(action)

    out_file = f"{base}/zoom_plan.json"
    with open(out_file, "w") as f:
        json.dump({"clip_id": clip_id, "zooms": zoom_plan}, f, indent=2, ensure_ascii=False)

    print(f"✅ Zoom plan for {clip_id}: {len(zoom_plan)} zoom(s)")
    for z in zoom_plan:
        if z["type"] == "slow":
            print(f"  SLOW_ZOOM {z['range_name']} [{z['start']:.2f}→{z['end']:.2f}] 1.0→{z['end_scale']}")
        elif z["type"] == "punch":
            print(f"  PUNCH_ZOOM {z['range_name']} @ {z['at_time']:.2f}s peak={z['peak_scale']}")

    return out_file


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 detect_zoom_moments.py <clip_id>")
        sys.exit(1)
    detect_zoom_plan(sys.argv[1])
