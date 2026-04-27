#!/opt/homebrew/bin/python3.14
"""
Chat with your Wiki Knowledge Base

Ask questions and get answers grounded in your wiki content.

Usage:
    python ask_wiki.py                                    # Use fine-tuned model
    python ask_wiki.py --base                            # Use base model (no fine-tune)
    python ask_wiki.py --model mlx-community/SmolLM2-135M-Instruct  # Custom model
"""

import argparse
from pathlib import Path

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
ADAPTER_PATH = WIKI_PATH / "fine-tuned-wiki"
BASE_MODEL = "qwen3.5-2b"

# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description='Chat with your wiki')
    parser.add_argument('--base', action='store_true', help='Use base model instead of fine-tuned')
    parser.add_argument('--model', default=BASE_MODEL, help='Base model to use with LoRA adapter')
    args = parser.parse_args()
    
    print("Wiki Chat - Your Personal Knowledge Assistant")
    print("=" * 50)
    
    # Check if adapter exists
    adapter_file = ADAPTER_PATH / "adapters.safetensors"
    has_adapter = adapter_file.exists()
    
    model_path = args.model
    
    if args.base:
        print(f"Mode: Base model only (no fine-tuning)")
        print(f"Model: {model_path}")
    elif has_adapter:
        print(f"Mode: Base model + LoRA adapter")
        print(f"Base: {model_path}")
        print(f"Adapter: {adapter_file}")
    else:
        print(f"Mode: Base model only (no fine-tuned adapter found)")
        print(f"Model: {model_path}")
        print(f"\nHint: Run fine_tune.py first to create a fine-tuned adapter")
    
    print()
    print("Type 'quit' to exit")
    print()
    
    # Chat loop
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
        
        print()
        
        # Build mlx_lm generate command
        import subprocess
        
        cmd = [
            "mlx_lm", "generate",
            "--model", model_path,
        ]
        
        if has_adapter and not args.base:
            cmd.extend(["--adapter-path", str(ADAPTER_PATH)])
        
        prompt = f"""You are an AI assistant with deep knowledge of the user's personal wiki.
Answer questions based on what you know from the wiki. Be specific and accurate.

Question: {question}

Answer:"""
        
        # Run generation
        try:
            result = subprocess.run(
                cmd,
                input=prompt,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode == 0:
                answer = result.stdout.strip()
                print(f"Wiki: {answer}")
            else:
                print(f"Error: {result.stderr}")
        
        except subprocess.TimeoutExpired:
            print("Timeout: Generation took too long")
        except Exception as e:
            print(f"Error: {e}")
        
        print()

if __name__ == "__main__":
    main()
