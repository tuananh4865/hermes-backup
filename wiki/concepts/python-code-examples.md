---
title: "Python Code Examples"
confidence: high
last_verified: 2026-04-18
type: concept
tags: [python, code-examples, programming]
related:
  - [[transcript-processing-guide]]
  - [[local-llm-agents]]
  - [[vibe-coding]]
sources:
  - Real Python (speech recognition)
  - FastAPI best practices (GitHub)
---

# Python Code Examples

## Overview

Curated collection of practical Python patterns for AI agent development. These examples are production-tested and focused on real-world AI workflows.

## Audio Transcription Pipeline

```python
from faster_whisper import WhisperModel
import subprocess
from pathlib import Path

def transcribe_audio(audio_path: str, model_size: str = "large-v3") -> list[dict]:
    """Transcribe audio file with timestamps."""
    model = WhisperModel(model_size, device="cuda", compute_type="float16")
    
    segments, info = model.transcribe(
        audio_path,
        beam_size=5,
        word_timestamps=True,
        condition_on_previous_text=True
    )
    
    results = []
    for segment in segments:
        results.append({
            "start": segment.start,
            "end": segment.end,
            "text": segment.text.strip()
        })
    
    return results

# Usage
audio_file = "recording.mp3"
results = transcribe_audio(audio_file, "small")
for r in results:
    print(f"[{r['start']:.1f}s] {r['text']}")
```

## Local LLM with Ollama

```python
import subprocess
import json

def generate_with_ollama(prompt: str, model: str = "qwen3-8b") -> str:
    """Generate text using local Ollama model."""
    cmd = [
        "ollama", "generate",
        model,
        "-p", prompt,
        "--verbose"
    ]
    
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=300
    )
    
    return result.stdout

# Vietnamese content generation
prompt = """Bạn là trợ lý AI. Viết một bài blog ngắn về:
1. Lợi ích của việc chạy LLM trên local (máy tính cá nhân)
2. So sánh chi phí: local vs cloud
3. Cách bắt đầu với Ollama trên Mac M4

Viết bằng tiếng Việt, giọng văn thân thiện."""
```

## Multi-Agent with CrewAI

```python
from crewai import Agent, Task, Crew

# Define agents with roles and goals
researcher = Agent(
    role="Research Analyst",
    goal="Find latest developments in AI agents",
    backstory="Expert at finding and synthesizing technical information",
    verbose=True
)

writer = Agent(
    role="Technical Writer",
    goal="Create clear documentation from research",
    backstory="Skilled at explaining complex AI concepts simply",
    verbose=True
)

# Define tasks
research_task = Task(
    description="Research Claude Code vs Cursor AI",
    agent=researcher
)

write_task = Task(
    description="Write comparison guide based on research",
    agent=writer
)

# Run crew
crew = Crew(agents=[researcher, writer], tasks=[research_task, write_task])
result = crew.kickoff()
```

## LangGraph State Graph

```python
from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

class AgentState(TypedDict):
    messages: list
    current_task: str
    agent_outcome: str | None

def should_continue(state: AgentState) -> str:
    """Determine if we continue or end."""
    if state["agent_outcome"] == "complete":
        return END
    return "act"

graph = StateGraph(AgentState)

graph.add_node("research", research_node)
graph.add_node("act", act_node)
graph.add_edge("__start__", "research")
graph.add_conditional_edges("research", should_continue)
graph.add_edge("act", END)

app = graph.compile()
```

## Async Pipeline

```python
import asyncio
import aiohttp
from typing import list

async def fetch_url(session: aiohttp.ClientSession, url: str) -> dict:
    """Async HTTP fetch with timeout."""
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=30)) as response:
            return {
                "url": url,
                "status": response.status,
                "content": await response.text()
            }
    except Exception as e:
        return {"url": url, "error": str(e)}

async def parallel_fetch(urls: list[str]) -> list[dict]:
    """Fetch multiple URLs concurrently."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_url(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Usage
urls = ["https://api.example.com/1", "https://api.example.com/2"]
results = asyncio.run(parallel_fetch(urls))
```

## File Processing Utilities

```python
from pathlib import Path
import re

def extract_wikilinks(content: str) -> list[str]:
    """Extract [[wikilink]] targets from markdown."""
    pattern = r'\[\[([^\]|]+?)(?:\|[^\]]+?)?\]\]'
    return re.findall(pattern, content)

def slugify(text: str) -> str:
    """Convert text to URL-safe slug."""
    text = text.lower().strip()
    text = re.sub(r'[\s\-_]+', '-', text)
    text = re.sub(r'[^a-z0-9\-]', '', text)
    return text

def process_markdown_files(directory: Path, callback) -> None:
    """Process all markdown files in directory recursively."""
    for md_file in directory.rglob("*.md"):
        if md_file.is_file():
            content = md_file.read_text(encoding="utf-8")
            callback(md_file, content)

# Example: find broken links
def find_wikilinks(md_path: Path, content: str):
    links = extract_wikilinks(content)
    for link in links:
        slug = slugify(link)
        target = md_path.parent / f"{slug}.md"
        if not target.exists():
            print(f"Broken: {md_path} -> {link}")
```

## Environment & Config

```python
from pathlib import Path
from dotenv import load_dotenv
import os

def setup_environment() -> dict:
    """Load environment variables and validate setup."""
    project_root = Path(__file__).parent.parent
    env_file = project_root / ".env"
    
    if env_file.exists():
        load_dotenv(env_file)
    
    required = ["OPENAI_API_KEY", "ANTHROPIC_API_KEY"]
    missing = [k for k in required if not os.getenv(k)]
    
    if missing:
        raise EnvironmentError(f"Missing env vars: {missing}")
    
    return {k: os.getenv(k) for k in required}

# Usage
config = setup_environment()
api_key = config["OPENAI_API_KEY"]
```

## Streaming LLM Responses

```python
import openai
from typing import Generator

def stream_openai(prompt: str, model: str = "gpt-4") -> Generator[str, None, None]:
    """Stream OpenAI responses token by token."""
    client = openai.OpenAI()
    
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        stream=True
    )
    
    for chunk in stream:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content

# Usage
for token in stream_openai("Explain quantum computing in 3 sentences"):
    print(token, end="", flush=True)
```

## Related

- [[transcript-processing-guide]] — Full pipeline examples
- [[local-llm-agents]] — Local LLM patterns
- [[vibe-coding]] — AI-assisted coding practices
