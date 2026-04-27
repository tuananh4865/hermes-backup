---
title: "Wiki Master Plan — 15 Enhancement Ideas"
created: 2026-04-09
updated: 2026-04-09
type: concept
tags: [wiki, roadmap, planning]
---

# Wiki Master Plan — 15 Enhancement Ideas

## Executive Summary

Current wiki: 26 scripts, 4 skills, 56 pages — strong foundation but untapped potential.
Goal: Transform from "knowledge storage" to "intelligent knowledge agent" with learning, reasoning, and self-improvement capabilities.

---

## Architecture Vision

```
┌─────────────────────────────────────────────────────────────────────┐
│                        USER (Tuấn Anh)                               │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     INGESTION LAYER                                  │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐    │
│  │Articles │ │ Papers  │ │  RSS    │ │  Email  │ │ Telegram│    │
│  │(empty)  │ │ (empty) │ │(empty)  │ │(empty)  │ │ (hook)  │    │
│  └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘ └────┬────┘    │
│       └───────────┴───────────┴───────────┴───────────┘          │
│                           │                                         │
│                    ┌──────▼──────┐                                  │
│                    │   PARSER    │                                  │
│                    │  Extractor  │                                  │
│                    └──────┬──────┘                                  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    KNOWLEDGE PROCESSING                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                 │
│  │  Semantic   │ │  Temporal   │ │ Confidence  │                 │
│  │   Search    │ │   Graph     │ │  Scoring    │                 │
│  │ (embedding) │ │  (lineage)  │ │(uncertainty)│                 │
│  └─────────────┘ └─────────────┘ └─────────────┘                 │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐                 │
│  │ Contradic-  │ │  Duplicate  │ │  Priority   │                 │
│  │   tion      │ │  Detection  │ │  Weighting  │                 │
│  │  Resolver   │ │             │ │(user signal)│                 │
│  └─────────────┘ └─────────────┘ └─────────────┘                 │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    INTELLIGENCE LAYER                               │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    SELF-EVOLUTION AGENT                       │   │
│  │  OBSERVE → PLAN → ACT → LEARN → REFLECT (continuous)        │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │              CROSS-AGENT COORDINATION                         │   │
│  │  Scholar | Librarian | Scientist | Engineer                 │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    OUTPUT LAYER                                     │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐ ┌─────────┐                  │
│  │ Wiki    │ │Fine-tune│ │Weekly   │ │Dashboard│                  │
│  │ Chat    │ │ Pipeline│ │ Digest  │ │  (web)  │                  │
│  └─────────┘ └─────────┘ └─────────┘ └─────────┘                  │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Phase 1: Foundation Fixes (Week 1)

### 1.1 Wiki Health Fix — 6 Broken Links

**Problem:** 6 broken links remaining, 7 orphan pages

**Files:**
```
scripts/wiki_lint.py --auto-fix  # Fix what can be auto-fixed
scripts/wiki_self_heal.py --all --fix
```

**Manual fixes needed:**
1. `concepts/mistake-log.md` → `[[001-date-format-mismatch]]`
2. `skills/wiki-self-heal.md` → `[[skills/wiki-watchdog]]` (exists)
3. `skills/wiki-self-evolution.md` → `[[skills/wiki-watchdog]]` (exists)
4. `concepts/wiki-self-evolution.md` → `[[skills/wiki-watchdog]]` (exists)

**Action:**
```bash
cd ~/wiki
# Fix wikilinks manually
# Then verify
python3 scripts/wiki_lint.py
```

**Success criteria:** `wiki_lint.py` shows 0 broken links

---

### 1.2 Ingest Pipeline Foundation

**Problem:** `raw/articles/`, `raw/papers/`, `raw/rss/`, `raw/emails/` are empty

**Goal:** Create reusable parsers for each content type

#### 1.2.1 Article Ingest

**Input:** Web articles (HTML)
**Output:** `raw/articles/{slug}.md` with frontmatter

**Parser requirements:**
- Extract: title, author, date, url, content (main text only)
- Clean: remove ads, navigation, comments
- Frontmatter: `sources: [{url}]`

**Script:** `scripts/ingest_article.py`
```python
# Usage
python3 scripts/ingest_article.py --url "https://example.com/article"
python3 scripts/ingest_article.py --file article.html
```

#### 1.2.2 Paper Ingest

**Input:** arXiv PDFs, research papers
**Output:** `raw/papers/{arxiv-id}.md`

**Parser requirements:**
- Extract: title, authors, abstract, date, arxiv_id
- PDF → markdown (use web_extract for arxiv)
- Frontmatter: `type: paper`, `tags: [research, {topic}]`

**Script:** `scripts/ingest_paper.py`
```python
# Usage
python3 scripts/ingest_paper.py --arxiv 2504.12345
python3 scripts/ingest_paper.py --url "https://arxiv.org/pdf/..."
```

#### 1.2.3 RSS Ingest

**Input:** RSS/Atom feeds
**Output:** `raw/rss/{feed-name}/{item-slug}.md`

**Parser requirements:**
- Extract: title, link, date, summary, content
- Deduplication: don't re-ingest same item
- Frontmatter: `sources: [{link}]`, `tags: [{topic}]`

**Script:** `scripts/ingest_rss.py`
```python
# Usage
python3 scripts/ingest_rss.py --add "https://example.com/feed.xml"
python3 scripts/ingest_rss.py --fetch-all
python3 scripts/ingest_rss.py --list
```

#### 1.2.4 Email Ingest

**Problem:** Email forwarding not set up yet

**Prerequisite:** Email setup (see auto-ingest setup guides)

**Script:** `scripts/ingest_email.py`
```python
# Usage
python3 scripts/ingest_email.py --unread
python3 scripts/ingest_email.py --search "wiki"
```

**Files needed:**
- `auto-ingest/email-setup.md` — Setup email forwarding
- `auto-ingest/rss-setup.md` — Setup RSS feeds

---

## Phase 2: Intelligence Layer (Week 2-3)

### 2.1 Priority-Weighted Self-Evolution

**Problem:** Current gap analysis treats all gaps equally. Should prioritize based on user interest signals.

**Current behavior:**
```python
# All gaps scored equally
gaps = [
    {"topic": "transformer", "score": 5},
    {"topic": "attention", "score": 5},  # Equal priority
]
```

**New behavior:**
```python
# Weighted by signals
class PriorityScorer:
    def score(self, topic, signals):
        # User interest weight (40%): How often does user ask about this?
        user_weight = signals.topic_frequency.get(topic, 0)
        
        # Recency weight (20%): Is this topic currently relevant?
        recent_weight = signals.recent_mentions.get(topic, 0)
        
        # Breadth weight (20%): Does this connect many existing pages?
        breadth_weight = signals.connections.get(topic, 0)
        
        # Gap severity (20%): How missing is this?
        severity_weight = signals.existing_content_quality.get(topic, 0)
        
        return weighted_score
```

**New signals to track:**
1. **Topic frequency:** Count how many times Anh mentions topic in conversations
2. **Recent mentions:** Topics mentioned in last 7 days weighted higher
3. **Connection count:** How many pages link to/from this topic
4. **User correction rate:** If Anh frequently corrects content in this topic

**Files to create/modify:**
- `scripts/interest_signal_tracker.py` — Track user signals
- `scripts/priority_gap_analyzer.py` — Weighted gap scoring
- `scripts/wiki_self_evolution_agent.py` — Integrate priority scoring

**Usage:**
```bash
# Track signals from recent transcripts
python3 scripts/interest_signal_tracker.py --track

# Get prioritized gaps
python3 scripts/priority_gap_analyzer.py --top 10

# Run self-evolution with priority
python3 scripts/wiki_self_evolution_agent.py --priority-weighted
```

**Success criteria:**
- Top 3 gaps align with user's recent interests
- Gap ordering changes significantly from equal-weight version

---

### 2.2 Learning from Corrections

**Problem:** When Anh corrects Em, that correction is lost after session. Should learn from it.

**Concept:**
```
When Anh says "không phải" / "sai rồi" / "Nhầm" = Learning Signal
  → Update page quality score (decrease)
  → Add to mistake-log
  → If same mistake 3x = gap in knowledge → trigger self-evolution
```

**Hook needed:** `correction_detector.py`

**Signals to detect:**
- "không phải", "sai", "nhầm", "chờ", "đợi" (wait, not done yet)
- "em hiểu sai" / "em trả lời sai"
- User provides contradicting information

**Implementation:**
```python
class CorrectionDetector:
    CORRECTION_PATTERNS = [
        r"không phải",
        r"sai rồi",
        r"nhầm",
        r"chờ|đợi",
        r"em hiểu sai",
    ]
    
    def detect(self, message):
        """Return correction signal if detected"""
        
    def process_correction(self, correction):
        """Update mistake-log and quality scores"""
        # 1. Add to mistake-log
        # 2. Decrease page quality score
        # 3. If 3+ corrections on same page → trigger gap analysis
```

**Files to create:**
- `scripts/correction_detector.py`
- `skills/wiki-learning-from-corrections.md`

**Usage:**
```bash
# After each conversation, detect corrections
python3 scripts/correction_detector.py --session session_id

# Report corrections to user
python3 scripts/correction_detector.py --report
```

**Integration:**
- Run via watchdog hook after each session
- Updates `learned-about-user.md` with correction patterns
- Updates page quality scores in `wiki_self_critique.py` output

**Success criteria:**
- Corrections automatically logged
- Quality scores reflect correction frequency
- Repeated corrections trigger wiki improvement

---

### 2.3 Semantic Search

**Problem:** Current search is grep-based. Doesn't understand meaning.

**Goal:** Embedding-based search that finds conceptually related content

**Architecture:**
```
Query → Embed (local model) → Vector DB → Top-K results → Present
```

**Options:**

| Option | Pros | Cons |
|--------|------|------|
| **Local embeddings** (all-MiniLM via LM Studio) | Free, private | Slower, need model running |
| **ChromaDB** | Production-ready | Extra dependency |
| **FAISS** | Fast, Facebook-maintained | Pure indexing, no DB |
| **Simple cosine sim** | No extra deps | Good enough for small wiki |

**Recommended:** Simple cosine similarity first, upgrade to FAISS later

**Implementation:**
```python
# scripts/semantic_search.py
from pathlib import Path
import numpy as np

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"  # or local
CHUNK_SIZE = 512  # chars per chunk

class SemanticSearch:
    def __init__(self, wiki_path):
        self.wiki_path = wiki_path
        self.chunks = []  # List of (chunk_text, page_name, chunk_id)
        self.vectors = None  # N x 384 matrix
        
    def index(self):
        """Build index from all wiki pages"""
        chunks = self.chunk_all_pages()
        vectors = self.embed(chunks)
        self.chunks = chunks
        self.vectors = vectors
        
    def search(self, query, top_k=5):
        """Find most relevant chunks"""
        query_vec = self.embed([query])
        scores = cosine_similarity(query_vec, self.vectors)
        top_indices = np.argsort(scores)[-top_k:][::-1]
        return [self.chunks[i] for i in top_indices]
```

**Usage:**
```bash
# Build index
python3 scripts/semantic_search.py --index

# Search
python3 scripts/semantic_search.py --query "attention mechanism"
python3 scripts/semantic_search.py --query "làm sao để fine-tune model"

# Re-index when wiki changes
python3 scripts/semantic_search.py --reindex
```

**Integration:**
- `ask_wiki.py` uses semantic search instead of grep
- Watchdog triggers re-index on file changes (debounced)

**Success criteria:**
- "attention" finds pages about attention even if word not in title
- Vietnamese queries work
- Response time < 2s for 100-page wiki

---

## Phase 3: Advanced Intelligence (Week 3-4)

### 3.1 Fine-tune Pipeline Hoàn Chỉnh

**Already exists:**
- `scripts/generate_training_data.py`
- `scripts/fine_tune.py`
- `fine-tuned-wiki/` directory

**Problem:** Never actually ran the pipeline

**Pipeline:**
```
Wiki Content → Q&A Pairs → Training Data → Fine-tune → LoRA Adapter
```

#### Step 1: Generate Training Data

```python
# scripts/generate_training_data.py -- already exists, needs review
python3 scripts/generate_training_data.py --output training_data/wiki_qa.jsonl
```

**Output format:**
```json
{"messages": [{"role": "user", "content": "What is attention?"}, {"role": "assistant", "content": "Attention is..."}]}
```

**Issues to fix:**
- Check current script output format
- Ensure Vietnamese content handled properly
- Add more Q&A patterns (factual, conceptual, how-to)

#### Step 2: Fine-tune

```python
# Hardware: MacBook M3 with MLX
python3 scripts/fine_tune.py \
    --data training_data/wiki_qa.jsonl \
    --model qwen3.5-2b \
    --epochs 3 \
    --lora-rank 8

# Output: fine-tuned-wiki/adapters.safetensors
```

**Integration with ask_wiki.py:**
```python
# ask_wiki.py already supports --base vs fine-tuned
python3 scripts/ask_wiki.py  # Uses fine-tuned
python3 scripts/ask_wiki.py --base  # Uses base model
```

#### Step 3: Test

```python
# Compare base vs fine-tuned responses
python3 scripts/ask_wiki.py --query "What is Karpathy's wiki approach?"
python3 scripts/ask_wiki.py --base --query "What is Karpathy's wiki approach?"

# Measure: Does fine-tuned give better answers about Anh's wiki?
```

**Success criteria:**
- Fine-tuned model correctly answers "What is Anh's project about?"
- Fine-tuned model references specific pages from wiki
- Quality > base model on wiki-related queries

---

### 3.2 Test Infrastructure

**Problem:** 26 scripts, 0 tests. Any change could break anything.

**Framework:** pytest (Python standard)

**Structure:**
```
tests/
├── conftest.py           # Shared fixtures
├── test_wiki_lint.py     # Lint tests
├── test_wiki_heal.py     # Heal tests
├── test_self_evolution.py
├── test_semantic_search.py
├── test_transcript.py
├── test_coverage_map.py
└── fixtures/
    ├── sample_page.md
    ├── broken_links.md
    └── orphan_page.md
```

**Example test:**
```python
# tests/test_wiki_lint.py
import pytest
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from wiki_lint import WikiLinter

@pytest.fixture
def sample_wiki(tmp_path):
    """Create a minimal test wiki"""
    (tmp_path / "concepts").mkdir()
    (tmp_path / "concepts" / "test.md").write_text("""---
title: Test
---
# Test
Content here.
""")
    return tmp_path

def test_lint_finds_missing_frontmatter(sample_wiki):
    linter = WikiLinter(sample_wiki)
    issues = linter.check_frontmatter()
    assert len(issues) == 0  # Our fixture has frontmatter
    
def test_lint_finds_broken_links(sample_wiki):
    # Create page with broken link
    ...
```

**CI/CD:**
```yaml
# .github/workflows/test.yml
name: Wiki Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run tests
        run: pytest tests/ -v
```

**Usage:**
```bash
# Run all tests
pytest tests/

# Run specific test
pytest tests/test_wiki_lint.py -v

# Run with coverage
pytest tests/ --cov=scripts --cov-report=html
```

**Success criteria:**
- All existing scripts have tests
- New scripts require tests before merge
- CI passes on every PR

---

### 3.3 Weekly Digest

**Problem:** No passive summary of "what was learned this week"

**Goal:** Automatic weekly summary emailed or posted to Telegram

**Script:** `scripts/weekly_digest.py`

```python
class WeeklyDigest:
    def generate(self, days=7):
        """Generate digest for last N days"""
        # 1. Get all transcripts from last week
        transcripts = get_transcripts(days=7)
        
        # 2. Extract topics discussed
        topics = extract_topics(transcripts)
        
        # 3. Get pages created/updated
        changes = get_recent_changes(days=7)
        
        # 4. Get self-evolution actions taken
        evolution_report = load_report()
        
        # 5. Get quality metrics
        health = run_lint()
        
        # 6. Generate digest
        return f"""
## Weekly Digest — {date}

### Topics Discussed
- {topic1} ({count1} mentions)
- {topic2} ({count2} mentions)

### Wiki Changes
- Created: {pages_created}
- Updated: {pages_updated}
- Fixed: {issues_fixed}

### Self-Evolution
- Gaps filled: {gaps}
- Quality improvement: {old_avg} → {new_avg}

### Wiki Health
- Stale: {stale}
- Broken links: {broken}
- Quality avg: {quality}
"""
```

**Usage:**
```bash
# Generate digest
python3 scripts/weekly_digest.py

# Send to Telegram
python3 scripts/weekly_digest.py --send-telegram

# Save to wiki
python3 scripts/weekly_digest.py --save
```

**Cron:**
```
# Every Monday 9 AM
0 9 * * 1 python3 ~/wiki/scripts/weekly_digest.py --send-telegram
```

**Success criteria:**
- Digest contains accurate summary of week's work
- Telegram message format readable
- Saved to wiki for future reference

---

### 3.4 Wiki Dashboard

**Problem:** No visual overview of wiki health and metrics

**Goal:** Simple web UI showing wiki state

**Stack:**
- **Backend:** Python Flask or FastAPI
- **Frontend:** Simple HTML/CSS/JS (no framework needed)
- **Data:** JSON from lint scripts

**Pages:**

#### Dashboard Home (`/`)
```
┌─────────────────────────────────────────┐
│ Wiki Dashboard                    [↻]  │
├─────────────────────────────────────────┤
│ Health Score: ████████░░ 82%            │
│ Pages: 56  |  Broken: 0  |  Stale: 0   │
├─────────────────────────────────────────┤
│ [Graph: Quality over time]              │
│ [Graph: Topic distribution]             │
├─────────────────────────────────────────┤
│ Recent Changes                           │
│ • self-healing-wiki (2h ago)            │
│ • lm-studio (5h ago)                    │
│ • knowledge-base (1d ago)               │
└─────────────────────────────────────────┘
```

#### Pages List (`/pages`)
- Sortable by: name, quality, last updated, type
- Filter by: tag, type, stale/healthy
- Click to view/edit

#### Topics (`/topics`)
- Tag cloud visualization
- Coverage map
- Gap analysis

**Files:**
```
scripts/dashboard/
├── app.py              # Flask/FastAPI server
├── routes/
│   ├── api.py          # JSON endpoints
│   └── pages.py        # Page routes
├── static/
│   ├── style.css
│   └── dashboard.js
└── templates/
    ├── base.html
    ├── index.html
    └── pages.html
```

**Usage:**
```bash
# Start dashboard
cd ~/wiki/scripts/dashboard
python3 app.py

# Open browser
open http://localhost:5000
```

**Success criteria:**
- Shows real-time wiki health
- Updates when watchdog detects changes
- Mobile-friendly

---

## Phase 4: Advanced Features (Week 4-5)

### 4.1 Confidence Scoring

**Problem:** Wiki doesn't distinguish "high confidence facts" from "speculation"

**Goal:** Each fact has confidence score, propagated through relationships

**Concept:**
```markdown
# Attention (confidence: 0.95)
> High confidence: based on multiple sources, consistent across sessions

# Transformer Architecture (confidence: 0.7)  
> Medium confidence: single source, needs verification

# Speculative claim (confidence: 0.3)
> Low confidence: untested hypothesis, marked as uncertain
```

**Implementation:**
```python
class ConfidenceScorer:
    def score_page(self, page):
        factors = {
            "source_count": ...,      # +0.1 per source, max +0.3
            "cross_reference": ...,    # +0.1 per independent reference
            "recency": ...,           # +0.2 if updated recently
            "user_verified": ...,     # +0.2 if no corrections
            "contradiction_penalty": -0.3 if contradictory
        }
        return sum(factors.values())
```

**Visualization:**
- Green/Yellow/Red border on pages
- Confident pages get priority in search
- Low-confidence pages flagged for review

**Files:**
- `scripts/confidence_scorer.py`
- `skills/confidence-scoring.md`

**Success criteria:**
- Each page has confidence score in frontmatter
- Dashboard shows confidence distribution
- Low-confidence pages get auto-flagged for review

---

### 4.2 Relationship Strength

**Problem:** Wikilinks are binary (linked or not). Should have weights.

**Goal:** `topic (with strength weighting - planned feature)` — stronger connections = more related

**Use cases:**
- Search: Boost results for strongly connected pages
- Self-evolution: Strongly connected topics are core knowledge
- Quality: Orphan pages might just need stronger links

**Implementation:**
```python
class RelationshipStrength:
    def calculate(self, page_a, page_b):
        """How strong is the relationship between A and B?"""
        # 1. Explicit link (wikilink exists)
        explicit = 0.5
        
        # 2. Mentioned in same context (co-occurrence)
        co_occur = 0.2
        
        # 3. Temporal proximity (updated same day)
        temporal = 0.1
        
        # 4. Similar tags
        tag_overlap = 0.2
        
        return explicit + co_occur + temporal + tag_overlap
```

**Files:**
- `scripts/relationship_strength.py`
- Update `wiki_cross_ref.py` to suggest strengths

**Success criteria:**
- Cross-reference suggestions include strength scores
- Search results weighted by relationship strength
- Core topics have high aggregate connection strength

---

### 4.3 Temporal Knowledge Graph

**Problem:** Don't know "when" a fact was learned or how fresh it is

**Goal:** Every piece of knowledge has temporal metadata

**Metadata per fact/chunk:**
```yaml
learned_at: 2026-04-09
learned_from: transcript/2026-04-09-telegram.md
confidence: 0.8
last_verified: 2026-04-09
times_mentioned: 5
last_mentioned: 2026-04-10
```

**Use cases:**
- "What did I learn about LLM last week?"
- "When was the last time I updated the attention page?"
- "Which facts are getting stale (not mentioned in 30 days)?"

**Implementation:**
```python
class TemporalGraph:
    def add_fact(self, page, fact, source, timestamp):
        """Record new fact with temporal metadata"""
        
    def get_facts_since(self, date):
        """Get all facts learned since date"""
        
    def get_stale_facts(self, days=30):
        """Get facts not verified in N days"""
        
    def get_topic_timeline(self, topic):
        """Get when topic was learned/updated"""
```

**Files:**
- `scripts/temporal_knowledge_graph.py`
- New section in `learned-about-user.md`

**Success criteria:**
- Can answer "What did I learn about X in the last 7 days?"
- Staleness detected via temporal graph, not just page update date
- Timeline visualization available

---

## Phase 5: External Integration (Week 5-6)

### 5.1 Multi-modal Ingestion

**Problem:** Can only ingest text. What about images, PDFs, audio?

**Goal:** OCR images, extract text from PDFs, transcribe audio

#### Image → Text (OCR)
```python
# macOS: use system OCR
import subprocess

def ocr_image(image_path):
    result = subprocess.run([
        "sips", "-s", "format", "tiff", image_path, "--out", "/tmp/ocr.tiff"
    ])
    # Use tesseract if available, or Apple Vision via Python
```

#### PDF → Text
```python
# Use web_extract or pdfminer
from web_extract import extract_from_pdf
text = extract_from_pdf("paper.pdf")
```

#### Audio → Text (transcription)
```python
# Use Whisper via LM Studio or local
import whisper
model = whisper.load_model("base")
result = model.transcribe("recording.m4a")
```

**Files:**
- `scripts/ingest_image.py`
- `scripts/ingest_pdf.py`
- `scripts/transcribe_audio.py`

**Success criteria:**
- Can ingest scanned documents (OCR)
- Can extract text from research PDFs
- Can transcribe voice notes

---

### 5.2 External Knowledge Bridge

**Problem:** Wiki doesn't know things outside its content. ChatGPT/RAG have internet.

**Goal:** When wiki doesn't have answer, optionally search external sources

**Architecture:**
```
User Query
    │
    ▼
┌───────────────┐
│ Search Wiki   │ ← Local semantic search
│ (existing)    │
└───────┬───────┘
        │
        ▼ Found? ──No──► Search External
        │                  (web search)
        │ Yes
        ▼
    Present Answer
    (cite wiki sources)
```

**External search options:**
1. **Web search API** (Tavily, SerpAPI) — paid, good quality
2. **DuckDuckGo free** — rate limited
3. **Direct to search engine** — simple, no API key

**Implementation:**
```python
class ExternalKnowledgeBridge:
    def __init__(self, wiki_search):
        self.wiki_search = wiki_search
        self.web_search = DuckDuckGoSearch()  # or Tavily
        
    def query(self, question):
        # 1. Try wiki first
        wiki_results = self.wiki_search.search(question)
        
        if wiki_results:
            return wiki_results
        
        # 2. If no wiki results, search web
        web_results = self.web_search.search(question)
        
        return {
            "source": "web",
            "results": web_results,
            "warning": "This information is from external sources, not your wiki"
        }
```

**Files:**
- `scripts/external_knowledge_bridge.py`
- Update `ask_wiki.py` to use bridge

**Success criteria:**
- "What is the latest news about X?" returns web results
- External results clearly labeled
- User can disable external search if wanted

---

### 5.3 User Interest Signals

**Problem:** Self-evolution doesn't know what Anh cares about

**Goal:** Track interest signals passively

**Signals to track:**

| Signal | Source | Weight |
|--------|--------|--------|
| Topic mentions in conversation | Transcript analysis | High |
| Follow-up questions | "tell me more about X" | High |
| Time spent on topic | (hard to track) | Medium |
| Corrections | User correcting content | High |
| Direct questions | "what is X?" | High |
| Project relevance | Linked to active projects | Medium |

**Implementation:**
```python
class InterestSignalTracker:
    def track_from_transcript(self, transcript_path):
        """Extract interest signals from transcript"""
        signals = {
            "topics_mentioned": Counter(),
            "questions_asked": [],
            "corrections": [],
            "follow_ups": []
        }
        # NLP to extract signals
        return signals
        
    def get_top_interests(self, days=30):
        """Return ranked list of interests"""
        
    def get_interest_profile(self):
        """Return user interest profile for recommendations"""
```

**Storage:**
```yaml
# concepts/user-interest-profile.md
---
title: User Interest Profile
updated: 2026-04-09
interests:
  - topic: lm-studio
    score: 0.9
    last_mentioned: 2026-04-09
    mention_count: 47
  - topic: fine-tuning
    score: 0.7
    last_mentioned: 2026-04-08
    mention_count: 23
---
```

**Files:**
- `scripts/interest_signal_tracker.py` (extend existing)
- `skills/user-interest-tracking.md`

**Success criteria:**
- Top interests match user's actual questions
- Self-evolution prioritizes high-interest topics
- Profile updates weekly

---

### 5.4 Contradiction Resolver

**Problem:** When two pages contradict each other, wiki doesn't notice

**Goal:** Detect contradictions, propose resolution

**Detection:**
```python
class ContradictionDetector:
    def find_contradictions(self):
        """Find pairs of claims that contradict"""
        # 1. Find claims with confidence > 0.5
        claims = extract_claims(self.wiki)
        
        # 2. Group by topic
        by_topic = group_by_topic(claims)
        
        # 3. Check for negation patterns
        # "X is Y" vs "X is not Y"
        # "Do X" vs "Don't do X"
        
        # 4. Flag contradictions
        contradictions = []
        for topic, topic_claims in by_topic.items():
            if has_negation_conflict(topic_claims):
                contradictions.append({
                    "topic": topic,
                    "claims": topic_claims,
                    "confidence_diff": ...
                })
        
        return contradictions
```

**Resolution workflow:**
```markdown
## ⚠️ Contradiction Detected: Fine-tuning approach

### Claim A (confidence: 0.8)
From [[fine-tuning]]: "Use LoRA for small models"

### Claim B (confidence: 0.6)  
From [[lora]]: "LoRA works best for <1B parameters"

### Proposed Resolution
Both are correct. LoRA is preferred for small models (<1B),
but full fine-tuning may be needed for larger models.

### Action Required
- [ ] Update [[fine-tuning]] to clarify model size
- [ ] Update [[lora]] with confidence boost
```

**Files:**
- `scripts/contradiction_resolver.py` (extend existing `contradiction_detector.py`)
- `skills/contradiction-resolution.md`

**Success criteria:**
- Contradictions auto-detected weekly
- Resolution proposals logged for review
- Resolved contradictions marked in wiki

---

## Implementation Order

### Week 1 ✅ DONE
1. [x] Fix remaining 6 broken links
2. [x] Ingest pipeline: article + paper parsers
3. [x] RSS ingest setup

### Week 2 ✅ DONE
4. [x] Priority-weighted self-evolution
5. [x] Interest signal tracker
6. [x] Learning from corrections

### Week 3 ✅ DONE
7. [x] Semantic search
8. [x] Fine-tune pipeline (generation working)
9. [x] Test infrastructure (12/12 tests pass)

### Week 4 ✅ DONE
10. [x] Weekly digest
11. [ ] Wiki dashboard (web UI - skipped for now)
12. [x] Confidence scoring

### Week 5 ✅ DONE
13. [x] Temporal knowledge graph
14. [x] Relationship strength
15. [x] Multi-modal ingestion

### Week 6 ✅ DONE
16. [x] External knowledge bridge
17. [x] User interest signals (integrated)
18. [x] Contradiction resolver

---

## Dependencies

```
Article/Paper Ingest ─────┐
RSS Ingest ───────────────┼──► Self-Evolution ───┐
Email Ingest ─────────────┘                       │
                                                  │
Interest Signals ───────────────────────────────┐
                                                  │
Self-Evolution ──────────────────────────────────┼──► Weekly Digest
                                                  │
Semantic Search ─────────────────────────────────┤
                                                  │
Fine-tune Pipeline ──────────────────────────────┤──► Wiki Dashboard
                                                  │
Confidence Scoring ─────────────────────────────┤
                                                  │
Temporal Graph ──────────────────────────────────┼──► User Interest Profile
                                                  │
Relationship Strength ──────────────────────────┘
```

---

## Success Metrics

| Feature | Metric | Target |
|---------|--------|--------|
| Ingest pipeline | % raw content processed | >80% |
| Self-evolution | Gap coverage | >70% of top-20 topics |
| Semantic search | Relevance score | >0.8 avg |
| Fine-tune | Quality improvement vs base | >20% |
| Test coverage | % scripts tested | >90% |
| Confidence | % pages scored | 100% |
| Weekly digest | User satisfaction | "useful" feedback |

---

## Technical Debt

1. **Scripts are coupled** — refactor to shared library
2. **No type hints** — add gradually
3. **Error handling** — many scripts fail silently
4. **Logging** — inconsistent log formats
5. **Configuration** — hardcoded paths, should use config.yaml

---

## Related Pages

- [[wiki-enhancement-roadmap]] — Original roadmap
- [[self-healing-wiki]] — Current self-healing implementation
- [[wiki-self-evolution]] — Self-evolution concept
- [[intelligent-wiki-architecture]] — System design
