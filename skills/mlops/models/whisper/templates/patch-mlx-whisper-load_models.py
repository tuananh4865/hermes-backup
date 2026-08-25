#!/usr/bin/env python3
"""
Patch mlx_whisper/load_models.py to support modern HuggingFace Whisper configs.

PROBLEM:
mlx_whisper==0.4.3 calls `whisper.ModelDimensions(**config)` where `config` is
the raw JSON from `config.json` of a HuggingFace Whisper model. Modern HF configs
include extra fields like `_name_or_path`, `activation_dropout`, `attention_dropout`,
`architectures`, `_commit_hash`, `transformers_version` that `ModelDimensions.__init__`
doesn't accept.

Additionally, modern HF configs use new key names:
  - `num_mel_bins` instead of `n_mels` (large-v3 uses 128 instead of 80)
  - `d_model` instead of `n_audio_state`
  - `max_source_positions` instead of `n_audio_ctx`
  - `encoder_attention_heads` instead of `n_audio_head`
  - `encoder_layers` instead of `n_audio_layer`
  - `vocab_size` instead of `n_vocab`
  - `max_target_positions` instead of `n_text_ctx`
  - `decoder_attention_heads` instead of `n_text_head`
  - `decoder_layers` instead of `n_text_layer`

SYMPTOMS:
  TypeError: __init__() got an unexpected keyword argument '_name_or_path'
  TypeError: __init__() got an unexpected keyword argument 'activation_dropout'
  TypeError: __init__() missing 1 required positional argument: 'n_mels'

USAGE:
  python3 templates/patch-mlx-whisper-load_models.py
  # Or with explicit path:
  python3 templates/patch-mlx-whisper-load_models.py --path /path/to/mlx_whisper/load_models.py

VERIFICATION:
  After running this script, the patched load_models.py should accept:
    - mlx-community/whisper-medium-mlx (already works)
    - mlx-community/whisper-large-v3-turbo (NEW)
    - openai/whisper-large-v3-turbo (after config mapping)

REVERT:
  Backup is written to load_models.py.bak. To revert:
    mv load_models.py.bak load_models.py

Date: 2026-07-05
Author: Hermes Agent (session test mlx-whisper large-v3-turbo)
"""

import argparse
import shutil
import sys
from pathlib import Path

# The exact code we want to insert, with proper indentation.
PATCH_OLD = '''    with open(str(model_path / "config.json"), "r") as f:
        config = json.loads(f.read())
        config.pop("model_type", None)
        quantization = config.pop("quantization", None)

    model_args = whisper.ModelDimensions(**config)'''

PATCH_NEW = '''    with open(str(model_path / "config.json"), "r") as f:
        raw_config = json.loads(f.read())
        raw_config.pop("model_type", None)
        raw_config.pop("quantization", None)

    # Whisper ModelDimensions only accepts these 10 fields.
    # New HF configs include extra fields (activation_dropout, attention_dropout,
    # architectures, transformers_version, etc.) that break ModelDimensions(**).
    # Map modern HF keys back to whisper.ModelDimensions expected names.
    _KEYMAP = {
        "n_mel_bins": "n_mels",
        "max_source_positions": "n_audio_ctx",
        "d_model": "n_audio_state",
        "encoder_attention_heads": "n_audio_head",
        "encoder_layers": "n_audio_layer",
        "vocab_size": "n_vocab",
        "max_target_positions": "n_text_ctx",
        "decoder_attention_heads": "n_text_head",
        "decoder_layers": "n_text_layer",
    }
    config = {}
    for k, v in raw_config.items():
        if k in {"n_mels", "n_audio_ctx", "n_audio_state", "n_audio_head",
                 "n_audio_layer", "n_vocab", "n_text_ctx", "n_text_state",
                 "n_text_head", "n_text_layer"}:
            config[k] = v
        elif k in _KEYMAP:
            config[_KEYMAP[k]] = v
    # n_text_state must equal n_audio_state for whisper
    if "n_text_state" not in config and "n_audio_state" in config:
        config["n_text_state"] = config["n_audio_state"]

    model_args = whisper.ModelDimensions(**config)
    quantization = None'''


def find_load_models_path(explicit: str | None) -> Path:
    """Locate mlx_whisper/load_models.py on the system."""
    if explicit:
        path = Path(explicit).expanduser()
        if path.exists():
            return path
        raise SystemExit(f"--path does not exist: {path}")

    try:
        import mlx_whisper
        pkg_dir = Path(mlx_whisper.__file__).parent
        candidate = pkg_dir / "load_models.py"
        if candidate.exists():
            return candidate
    except ImportError:
        pass

    # Fallback: try common Python user site
    candidates = [
        Path.home() / "Library/Python/3.9/lib/python/site-packages/mlx_whisper/load_models.py",
        Path.home() / "Library/Python/3.10/lib/python/site-packages/mlx_whisper/load_models.py",
        Path.home() / "Library/Python/3.11/lib/python/site-packages/mlx_whisper/load_models.py",
        Path.home() / "Library/Python/3.12/lib/python/site-packages/mlx_whisper/load_models.py",
    ]
    for c in candidates:
        if c.exists():
            return c

    raise SystemExit(
        "Could not locate mlx_whisper/load_models.py automatically. "
        "Pass --path /full/path/to/load_models.py"
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--path", help="Explicit path to mlx_whisper/load_models.py")
    parser.add_argument("--dry-run", action="store_true", help="Show diff without writing")
    parser.add_argument("--force", action="store_true", help="Patch even if already patched")
    args = parser.parse_args()

    path = find_load_models_path(args.path)
    print(f"[patch] Target file: {path}")

    original = path.read_text()

    if "Modern HF keys back to whisper.ModelDimensions" in original:
        if not args.force:
            print(f"[patch] Already patched (found sentinel comment). Use --force to re-apply.")
            sys.exit(0)
        print(f"[patch] --force set, re-applying patch.")

    if PATCH_OLD not in original:
        print("[patch] ERROR: Could not find the original 4-line block to patch.")
        print("[patch] The mlx_whisper source may have changed. Expected:")
        print("---")
        print(PATCH_OLD)
        print("---")
        sys.exit(1)

    patched = original.replace(PATCH_OLD, PATCH_NEW, 1)

    if args.dry_run:
        print("[patch] DRY RUN — would write:")
        print("---")
        # Show first 20 lines of the patched region for inspection
        patched_lines = patched.split("\n")
        # Find the start of the patched region (line containing "raw_config = json.loads")
        for i, line in enumerate(patched_lines):
            if "raw_config = json.loads" in line:
                for j in range(max(0, i - 2), min(len(patched_lines), i + 40)):
                    marker = ">>" if j == i else "  "
                    print(f"{marker} {j+1:4d}: {patched_lines[j]}")
                break
        print("---")
        sys.exit(0)

    # Backup
    backup = path.with_suffix(path.suffix + ".bak")
    if not backup.exists():
        shutil.copy2(path, backup)
        print(f"[patch] Backup: {backup}")
    else:
        print(f"[patch] Backup already exists: {backup} (skipped)")

    path.write_text(patched)
    print(f"[patch] Wrote {path} ({len(original)} → {len(patched)} bytes)")
    print(f"[patch] Done. Verify with:")
    print(f"          mlx_whisper --model mlx-community/whisper-large-v3-turbo --language vi --output-format json /tmp/test.wav")


if __name__ == "__main__":
    main()