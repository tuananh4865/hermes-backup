#!/opt/homebrew/bin/python3.14
"""
Fine-tune a Small LLM on Wiki Knowledge

Uses MLX for Apple Silicon fine-tuning with LoRA.

Usage:
    python fine_tune.py                    # Run with defaults (500 iters)
    python fine_tune.py --test            # Quick test (50 iters)
    python fine_tune.py --iters 200      # Custom iterations
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIG — Edit these settings
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
TRAINING_DATA = WIKI_PATH / "training_data"
OUTPUT_DIR = WIKI_PATH / "fine-tuned-wiki"

# Model options:
#   mlx-community/SmolLM2-135M-Instruct   (fastest, lowest memory)
#   mlx-community/SmolLM2-360M-Instruct   (balanced)
#   mlx-community/Qwen2.5-0.5B-Instruct  (better quality)
MODEL = "mlx-community/SmolLM2-135M-Instruct"

# LoRA config
NUM_LAYERS = 4  # Number of layers to fine-tune (-1 for all)
BATCH_SIZE = 1
LEARNING_RATE = 1e-4

# Training config
ITERS = 500
VAL_BATCHES = 10
STEPS_PER_REPORT = 25
SAVE_EVERY = 100
MAX_SEQ_LENGTH = 2048

# ═══════════════════════════════════════════════════════════════

def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n{description}...")
    result = subprocess.run(cmd, shell=True, capture_output=False)
    return result.returncode == 0

def main():
    parser = argparse.ArgumentParser(description='Fine-tune LLM on wiki knowledge')
    parser.add_argument('--iters', type=int, default=ITERS, help=f'Training iterations (default: {ITERS})')
    parser.add_argument('--model', default=MODEL, help='Base model')
    parser.add_argument('--test', action='store_true', help='Quick test with 50 iters')
    args = parser.parse_args()
    
    print("Wiki Fine-Tuner")
    print("=" * 50)
    
    # Check training data
    if not TRAINING_DATA.exists():
        print(f"ERROR: Training data not found: {TRAINING_DATA}")
        print("Run generate_training_data.py first")
        sys.exit(1)
    
    # Count examples
    train_file = TRAINING_DATA / "train.jsonl"
    if not train_file.exists():
        print(f"ERROR: Training data not found: {train_file}")
        sys.exit(1)
    
    with open(train_file) as f:
        num_examples = sum(1 for _ in f)
    print(f"Training data: {TRAINING_DATA} ({num_examples} examples)")
    print(f"Base model: {args.model}")
    print(f"Output: {OUTPUT_DIR}")
    print()
    
    # Quick test mode
    iters = 50 if args.test else args.iters
    print(f"Training for {iters} iterations")
    print()
    
    # Build the mlx_lm lora command
    cmd = [
        "mlx_lm", "lora",
        "--model", args.model,
        "--train",
        "--data", str(TRAINING_DATA),
        "--fine-tune-type", "lora",
        "--optimizer", "adamw",
        "--num-layers", str(NUM_LAYERS),
        "--batch-size", str(BATCH_SIZE),
        "--iters", str(iters),
        "--val-batches", str(VAL_BATCHES),
        "--learning-rate", str(LEARNING_RATE),
        "--steps-per-report", str(STEPS_PER_REPORT),
        "--save-every", str(SAVE_EVERY),
        "--adapter-path", str(OUTPUT_DIR),
        "--max-seq-length", str(MAX_SEQ_LENGTH),
    ]
    
    if args.test:
        cmd.append("--test")
    
    # Print command
    print("Command:")
    print(" ".join(cmd))
    print()
    
    # Run training
    result = subprocess.run(cmd)
    
    if result.returncode == 0:
        print()
        print(f"✓ Fine-tuning complete!")
        print(f"✓ Adapter saved to: {OUTPUT_DIR}")
        print()
        print("To use the fine-tuned model:")
        print(f"  python ask_wiki.py")
    else:
        print()
        print(f"✗ Fine-tuning failed with return code {result.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
