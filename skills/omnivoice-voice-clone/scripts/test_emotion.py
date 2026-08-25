#!/usr/bin/env python3
"""
Test OmniVoice Non-Verbal tags + Pronunciation control.

Usage:
  python3 test_nonverbal.py --prompt <pt> --out-dir ./emotion_test/
"""
import sys, os, time, argparse, subprocess

VENV_PY = "/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/bin/python"
PROMPT = "/Volumes/Storage-1/Hermes/voice-prompts/tuan_anh_5s_1sent_amp.pt"


# 13 non-verbal tags từ README + 4 demo recipes
TEST_CASES = [
    # (id, text, expected_emotion, language_hint)
    ("01_baseline", "Mình sẽ giới thiệu cho các bạn một sản phẩm rất hay.", "Bình thường", "vi"),
    ("02_laughter", "[laughter] Cái này hay quá các bạn ơi!", "Cười + hào hứng", "vi"),
    ("03_sigh", "[sigh] Giá hơi cao nhỉ.", "Thở dài", "vi"),
    ("04_question_ah", "Bạn nghĩ sao[question-ah] Mình cùng bình luận nhé.", "Câu hỏi ngạc nhiên", "vi"),
    ("05_surprise_oh", "Wow[surprise-oh] Deal hời quá!", "Ngạc nhiên thích thú", "vi"),
    ("06_dissatisfaction", "Sản phẩm này tệ quá[dissatisfaction-hnn] Mình không recommend.", "Không hài lòng", "vi"),
    ("07_multi_emo", "[laughter] Hôm nay vui quá! [sigh] Nhưng mà giá hơi cao [question-yi]", "Mixed: vui → tiếc → hỏi", "vi"),
    ("08_eng_confirm", "This deal is amazing[confirmation-en] you really should check it out.", "English: confirm", "en"),
    ("09_cmu_pron", "He plays the [B EY1 S] guitar while catching a [B AE1 S] fish.", "CMU pronunciation", "en"),
    ("10_tiktok_emo", "[laughter] Các bạn ơi! [surprise-oh] Hôm nay sale SỐC luôn! [question-ah] Mua không anh em?", "TikTok promo (3 emo)", "vi"),
]


def run_test(out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    print(f"=== Test Non-Verbal + Pronunciation Control ===", flush=True)
    print(f"Output dir: {out_dir}", flush=True)

    # Build inline code
    code = f'''
import sys, time, torch
import numpy as np, soundfile as sf
sys.path.insert(0, "/Volumes/Storage-1/Hermes/scratch/omnivoice-test/.venv/lib/python3.11/site-packages")
from omnivoice.models.omnivoice import OmniVoice, VoiceClonePrompt

print("Loading model...", flush=True)
t0 = time.time()
model = OmniVoice.from_pretrained("k2-fsa/OmniVoice", device_map="mps", dtype=torch.float16)
print(f"Model loaded in {{time.time()-t0:.1f}}s", flush=True)

prompt = VoiceClonePrompt.load("{PROMPT}")
print(f"Prompt loaded: ref_rms={{prompt.ref_rms:.4f}}", flush=True)

TESTS = {TEST_CASES!r}

for i, (sid, text, emo, lang) in enumerate(TESTS, 1):
    print(f"\\n--- [{{i}}/{{len(TESTS)}}] {{sid}} ({{emo}}) ---", flush=True)
    print(f"  Text: {{text[:80]}}...", flush=True)
    t0 = time.time()
    try:
        audio = model.generate(text=text, language=lang, voice_clone_prompt=prompt)[0]
        out_path = f"{out_dir}/{{sid}}.wav"
        sf.write(out_path, audio, model.sampling_rate)
        peak = float(np.abs(audio).max())
        dur = len(audio) / model.sampling_rate
        print(f"  ✅ {{dur:.2f}}s, peak={{peak:.3f}}, time={{time.time()-t0:.1f}}s", flush=True)
    except Exception as e:
        print(f"  ❌ {{type(e).__name__}}: {{e}}", flush=True)

print("\\nDone!", flush=True)
'''

    result = subprocess.run([VENV_PY, "-c", code], capture_output=False)
    return result.returncode == 0


def verify_and_report(out_dir: str):
    """Run volumedetect on each output"""
    print(f"\n=== VOLUMEDETECT REPORT ===", flush=True)
    for fname in sorted(os.listdir(out_dir)):
        if not fname.endswith(".wav"):
            continue
        path = os.path.join(out_dir, fname)
        r = subprocess.run(
            ["ffmpeg", "-i", path, "-af", "volumedetect", "-vn", "-f", "null", "-"],
            capture_output=True, text=True, timeout=5,
        )
        info = {}
        for line in r.stderr.split("\n"):
            if "max_volume" in line:
                info["max"] = line.split(":")[-1].strip()
            if "mean_volume" in line:
                info["mean"] = line.split(":")[-1].strip()
        size = os.path.getsize(path)
        print(f"  {fname:<25} {info.get('max', '?'):<10} {info.get('mean', '?'):<10} {size//1024}KB", flush=True)


def main():
    parser = argparse.ArgumentParser(description="Test OmniVoice Non-Verbal tags")
    parser.add_argument("--prompt", default=PROMPT)
    parser.add_argument("--out-dir", default="/Volumes/Storage-1/Hermes/scratch/omnivoice-test/emotion_test/")
    args = parser.parse_args()

    if run_test(args.out_dir):
        verify_and_report(args.out_dir)


if __name__ == "__main__":
    main()
