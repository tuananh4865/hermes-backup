---
confidence: high
last_verified: 2026-04-10
relationships:
  - 🔗 fine-tuning (extracted)
  - 🔗 synthetic-data (extracted)
  - 🔗 lora (extracted)
relationship_count: 3
---

# Synthetic Fine-tuning Setup

## Overview

Fine-tune a small LLM on your wiki content to create a "personal knowledge model" that knows everything in your wiki.

## Workflow

```
Wiki Content → Generate Q&A Pairs → Fine-tune Model → "Ask Wiki" Chatbot
```

## Prerequisites

- Mac with Apple Silicon
- MLX installed (`pip install mlx mlx-lm`)
- ~10GB disk space for training
- At least 8GB RAM (16GB recommended)

## Step 1: Install Training Dependencies

```bash
pip install datasets huggingface_hub
```

## Step 2: Generate Q&A Training Data

Create `generate_training_data.py`:

```python
#!/usr/bin/env python3
"""
Generate synthetic Q&A training data from wiki content.
"""

import os
import glob
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict

def extract_content(filepath: str) -> str:
    """Extract main content from markdown file"""
    with open(filepath, 'r') as f:
        content = f.read()
    
    # Remove frontmatter
    if content.startswith('---'):
        parts = content.split('---', 2)
        if len(parts) >= 3:
            content = parts[2]
    
    # Remove markdown formatting
    import re
    content = re.sub(r'\[([^\]]+)\]\([^\)]+\)', r'\1', content)  # Links
    content = re.sub(r'#+ ', '', content)  # Headers
    content = re.sub(r'\*\*([^*]+)\*\*', r'\1', content)  # Bold
    content = re.sub(r'\*([^*]+)\*', r'\1', content)  # Italic
    content = re.sub(r'```.*?```', '', content, flags=re.DOTALL)  # Code blocks
    content = re.sub(r'[=-]{3,}', '', content)  # Separators
    
    return content.strip()

def generate_qa_prompt(content: str, title: str) -> str:
    """Generate prompt for Q&A pair creation"""
    return f"""Based on the following wiki content, generate 5 question-answer pairs.
Each Q&A should test understanding of a key concept from the content.

TITLE: {title}
CONTENT:
{content[:3000]}

Generate Q&A pairs in this exact format:
Q1: [Question about a key concept]
A1: [Clear, accurate answer]

Q2: [Question about another key concept]
A2: [Clear, accurate answer]

Continue with Q3, Q4, Q5 following the same pattern.
"""

def parse_qa_pairs(output: str) -> List[Dict[str, str]]:
    """Parse generated Q&A pairs from output"""
    import re
    
    pairs = []
    q_pattern = r'Q\d+:\s*(.+)'
    a_pattern = r'A\d+:\s*(.+)'
    
    questions = re.findall(q_pattern, output)
    answers = re.findall(a_pattern, output)
    
    for q, a in zip(questions, answers):
        pairs.append({
            "messages": [
                {"role": "user", "content": q.strip()},
                {"role": "assistant", "content": a.strip()}
            ]
        })
    
    return pairs

def main():
    WIKI_PATH = Path.home() / "wiki"
    CONCEPTS_PATH = WIKI_PATH / "concepts"
    OUTPUT_FILE = WIKI_PATH / "training_data.jsonl"
    
    print("Generating training data from wiki...")
    
    # Get all concept files
    concept_files = glob.glob(str(CONCEPTS_PATH / "*.md"))
    print(f"Found {len(concept_files)} concept files")
    
    all_pairs = []
    
    for i, filepath in enumerate(concept_files):
        title = Path(filepath).stem.replace('-', ' ').title()
        content = extract_content(filepath)
        
        if len(content) < 100:
            continue
        
        print(f"[{i+1}/{len(concept_files)}] Processing: {title}")
        
        # Generate Q&A pairs using teacher model
        try:
            from mlx_lm import generate, load
            
            model_path, tokenizer = load("mlx-community/Qwen2.5-1.5B-Instruct")
            
            prompt = generate_qa_prompt(content, title)
            output = generate(model_path, tokenizer, prompt=prompt, max_tokens=1024)
            
            pairs = parse_qa_pairs(output)
            all_pairs.extend(pairs)
            
            print(f"  Generated {len(pairs)} Q&A pairs")
            
        except Exception as e:
            print(f"  Error: {e}")
            continue
    
    # Save to JSONL
    print(f"\nSaving {len(all_pairs)} Q&A pairs to {OUTPUT_FILE}")
    
    with open(OUTPUT_FILE, 'w') as f:
        for item in all_pairs:
            f.write(json.dumps(item) + '\n')
    
    print("Done!")

if __name__ == "__main__":
    main()
```

Run it:

```bash
python3 scripts/synthetic-finetune/generate_training_data.py
```

## Step 3: Fine-tune the Model

Create `fine_tune.py`:

```python
#!/usr/bin/env python3
"""
Fine-tune a small LLM on wiki knowledge using MLX.
"""

import os
from pathlib import Path
from mlx_lm.tune import train, TrainingArgs

def main():
    WIKI_PATH = Path.home() / "wiki"
    TRAINING_DATA = WIKI_PATH / "training_data.jsonl"
    OUTPUT_DIR = WIKI_PATH / "fine-tuned-wiki"
    
    print("Starting fine-tuning...")
    print(f"Training data: {TRAINING_DATA}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Training configuration
    args = TrainingArgs(
        model="mlx-community/SmolLM2-360M-Instruct",
        train_data=str(TRAINING_DATA),
        output_dir=str(OUTPUT_DIR),
        
        # LoRA configuration
        lora_layers=4,
        lora_rank=8,
        lora_alpha=16,
        lora_dropout=0.05,
        
        # Training hyperparameters
        batch_size=1,
        learning_rate=1e-4,
        iters=500,
        val_iters=50,
        eval_interval=100,
        
        # Misc
        save_every=100,
        quicktest=True,
    )
    
    # Run training
    train(args)
    
    print(f"\n✓ Fine-tuned model saved to: {OUTPUT_DIR}")

if __name__ == "__main__":
    main()
```

Run it:

```bash
python3 scripts/synthetic-finetune/fine_tune.py
```

## Step 4: Use the Fine-tuned Model

Create `ask_wiki.py`:

```python
#!/usr/bin/env python3
"""
Chat with your wiki knowledge base.
"""

from mlx_lm import generate, load

MODEL_PATH = "~/wiki/fine-tuned-wiki"

def ask_wiki(question: str) -> str:
    """Ask a question to the fine-tuned wiki model"""
    
    model, tokenizer = load(MODEL_PATH)
    
    prompt = f"""You are an AI assistant with deep knowledge of the user's wiki. 
Answer questions based on what you know from the wiki.

Question: {question}

Answer:"""
    
    response = generate(model, tokenizer, prompt=prompt, max_tokens=512, temp=0.7)
    
    return response

def chat():
    """Interactive chat loop"""
    print("Wiki Chat - Type 'quit' to exit")
    print("="*50)
    
    while True:
        question = input("\nYou: ")
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        answer = ask_wiki(question)
        print(f"\nWiki: {answer}")

if __name__ == "__main__":
    chat()
```

Run it:

```bash
python3 scripts/synthetic-finetune/ask_wiki.py
```

## Alternative: Use MLX Fine-tuning Library

There's a library called `mlx-tune` that simplifies this:

```bash
pip install mlx-tune
```

```bash
# Fine-tune with one command
mlx tune \
    --model mlx-community/SmolLM2-360M-Instruct \
    --data training_data.jsonl \
    --output ./fine-tuned-wiki \
    --lora-layers 4 \
    --batch-size 1 \
    --iters 500
```

## Training Tips

### Model Selection
- **SmolLM2 360M**: Fastest, good for quick experiments
- **Qwen2.5 0.5B**: Better quality, still fast
- **Qwen2.5 1.5B**: Best quality, slower training

### LoRA Settings
- `lora_layers=4`: Start with this, increase if underfitting
- `lora_rank=8`: Higher = more capacity, slower
- `lora_alpha=16`: Usually 2x lora_rank

### Training Duration
- 500 iterations: Quick test
- 1000 iterations: Good quality
- 2000+ iterations: High quality (slower)

### Memory Issues?
- Reduce batch_size to 1
- Use smaller model
- Close other apps

## Expected Results

After fine-tuning:
- Model "knows" your wiki content
- Answers questions about your topics
- Can summarize concepts in your style

Without fine-tuning (RAG approach):
- Same knowledge, but requires context loading
- Slower per-query
- More accurate (no hallucination risk)

## Related Concepts

- [[fine-tuning]] — General fine-tuning approaches
- [[synthetic-data]] — Synthetic data generation for training
- [[lora]] — LoRA fine-tuning technique
