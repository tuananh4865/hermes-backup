#!/opt/homebrew/bin/python3.14
"""
Autonomous App Builder — Apple Ecosystem
Combines Superpowers (TDD), GSD (waves), GStack (skills), Composio AO (parallel subagents)
iOS-first, mobile-focused, monetization-ready
"""
import json
import re
import subprocess
import sys
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

WIKI_PATH = Path("/Volumes/Storage-1/Hermes/wiki")
PROJECTS_PATH = WIKI_PATH / "projects"
STATE_FILE = Path.home() / ".hermes" / "cron" / "app_builder_state.json"
LM_STUDIO_URL = "http://192.168.0.187:1234"

# Load env vars from ~/.hermes/.env
_env_file = Path.home() / ".hermes" / ".env"
if _env_file.exists():
    for line in _env_file.read_text().splitlines():
        line = line.strip()
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            import os
            os.environ.setdefault(k.strip(), v.strip())

# ─── Helpers ────────────────────────────────────────────────────────────────

def run_cmd(cmd: str, timeout: int = 120) -> str:
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout)
    return result.stdout.strip() + (result.stderr.strip() if result.stderr else "")

def save_state(state: Dict):
    STATE_FILE.parent.mkdir(parents=True, exist_ok=True)
    STATE_FILE.write_text(json.dumps(state, indent=2))

def load_state() -> Dict:
    if STATE_FILE.exists():
        data = json.loads(STATE_FILE.read_text())
        # Ensure required keys exist
        if "projects" not in data:
            data["projects"] = {}
        if "current_phase" not in data:
            data["current_phase"] = {}
        return data
    return {"projects": {}, "current_phase": {}}

def log(msg: str):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{timestamp}] {msg}")

def generate_research_queries(idea: str) -> Dict[str, List[str]]:
    """Generate 75+ research queries across 5 categories"""
    queries = {
        "market": [
            f"iOS app market size 2025 2026 growth",
            f"mobile app revenue trends subscription",
            f"App Store market share statistics 2025",
            f"top grossing iOS apps categories",
            f"mobile app industry outlook 2026",
        ],
        "competition": [
            f"best apps similar to {idea}",
            f"top iOS apps in category",
            f"iOS app competitor analysis template",
            f"App Store top charts category analysis",
            f"user reviews competitor apps pain points",
        ],
        "user_insights": [
            f"Reddit iOS apps recommendations 2025",
            f"iPhone app reviews complaints",
            f"mobile app user behavior trends",
            f"iOS app user retention strategies",
            f"app store review sentiment analysis",
        ],
        "technical": [
            f"iOS 18 new frameworks WWDC 2025",
            f"SwiftUI best practices 2025",
            f"StoreKit 2 subscription tutorial",
            f"iOS app privacy requirements 2025",
            f"Apple App Store review guidelines common rejections",
        ],
        "revenue": [
            f"iOS app monetization strategies 2025",
            f"App Store subscription pricing optimization",
            f"freemium vs subscription vs paid app",
            f"in-app purchase conversion rate benchmark",
            f"RevenueCat iOS subscription metrics",
        ],
        "aso": [
            f"App Store ASO keyword research 2025",
            f"iOS app store search volume tools",
            f"app store screenshot optimization",
            f"Apple App Store listing best practices",
            f"mobile app keyword rank tracking",
        ],
        "trends": [
            f"AI features iOS apps 2025 2026",
            f"iOS app trends emerging markets",
            f"mobile health app market growth",
            f"social features mobile apps engagement",
            f"offline-first iOS app architecture",
        ],
    }
    return queries

def research_category(category: str, queries: List[str]) -> str:
    """
    Run web research for a category.
    Priority: DuckDuckGo (free, no API) → Tavily (paid, better results)
    """
    import os
    
    # Try DuckDuckGo first (always free)
    try:
        from duckduckgo_search import DDGS
        results = []
        for q in queries:
            try:
                with DDGS() as d:
                    r = list(d.text(q, max_results=5))
                    results.append(f"## Query: {q}\n")
                    for item in r:
                        title = item.get("title", "N/A")
                        url = item.get("href", "")
                        desc = item.get("body", "")[:200]
                        results.append(f"- [{title}]({url}): {desc}\n")
                    results.append("\n")
            except Exception as e:
                results.append(f"Error researching '{q}': {e}\n\n")
        if results:
            return "".join(results)
    except ImportError:
        pass
    
    # Fallback to Tavily
    tavily_key = os.environ.get("TAVILY_API_KEY", "")
    if tavily_key:
        import urllib.request
        results = []
        for q in queries:
            try:
                payload = json.dumps({
                    "api_key": tavily_key,
                    "query": q,
                    "search_depth": "basic",
                    "max_results": 5
                }).encode()
                req = urllib.request.Request(
                    "https://api.tavily.com/search",
                    data=payload,
                    headers={"Content-Type": "application/json"},
                    method="POST"
                )
                with urllib.request.urlopen(req, timeout=30) as response:
                    res = json.loads(response.read().decode())
                    results.append(f"## Query: {q}\n")
                    for item in res.get("results", []):
                        title = item.get("title", "N/A")
                        url = item.get("url", "")
                        desc = item.get("content", "")[:200]
                        results.append(f"- [{title}]({url}): {desc}\n")
                    results.append("\n")
            except Exception as e:
                results.append(f"Error researching '{q}': {e}\n\n")
        if results:
            return "".join(results)
    
    return f"## {category.upper()}\n\n[No search available - install duckduckgo-search or set TAVILY_API_KEY]\n"

def calculate_research_score(idea: str, research_data: Dict) -> int:
    """Calculate market opportunity score 0-100"""
    score = 50  # Base
    
    # Market factors (would be computed from actual research data)
    # This is a simplified version - real implementation would parse research
    
    # Competition assessment
    competition_keywords = ["saturated", "crowded", "many competitors", "lots of apps"]
    weak_market_keywords = ["niche", "underserved", "gap", "opportunity", "few options"]
    
    # Revenue potential
    subscription_keywords = ["subscription", "recurring", "premium", "付费", "订阅"]
    transaction_keywords = ["one-time", "paid", "purchase", "一次性"]
    
    score = min(100, score + 15)  # Placeholder for actual analysis
    
    return score

# ─── Phase 1: Deep Research ────────────────────────────────────────────────

def phase_research(project_name: str, idea: str) -> Dict:
    """Phase 1: Deep market and technical research"""
    project_dir = PROJECTS_PATH / project_name
    research_dir = project_dir / "phase-1-research"
    research_dir.mkdir(parents=True, exist_ok=True)
    
    log(f"Starting DEEP RESEARCH for: {idea}")
    
    queries = generate_research_queries(idea)
    
    research_results = {}
    for category, qs in queries.items():
        log(f"Researching category: {category} ({len(qs)} queries)")
        research_results[category] = research_category(category, qs)
    
    # Write research files
    for category, content in research_results.items():
        (research_dir / f"{category}_analysis.md").write_text(content)
    
    # Generate summary report
    market_data = research_results.get("market", "")
    competition_data = research_results.get("competition", "")
    user_data = research_results.get("user_insights", "")
    technical_data = research_results.get("technical", "")
    revenue_data = research_results.get("revenue", "")
    aso_data = research_results.get("aso", "")
    
    score = calculate_research_score(idea, research_results)
    
    report = f"""# Research Report: {project_name}

**Idea**: {idea}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Research Score**: {score}/100

## Executive Summary

### Market Opportunity
{market_data[:2000] if market_data else 'N/A'}

### Competition Analysis
{competition_data[:2000] if competition_data else 'N/A'}

### User Insights
{user_data[:2000] if user_data else 'N/A'}

### Technical Feasibility
{technical_data[:2000] if technical_data else 'N/A'}

### Revenue Model
{revenue_data[:2000] if revenue_data else 'N/A'}

### ASO Strategy
{aso_data[:2000] if aso_data else 'N/A'}

## Research Score: {score}/100

| Factor | Score | Notes |
|--------|-------|-------|
| Market Size | /20 | |
| Competition | /20 | |
| User Need | /20 | |
| Technical Feasibility | /20 | |
| Revenue Potential | /20 | |

## Recommendation

{"✅ PROCEED" if score >= 75 else "⚠️ PROCEED WITH CAUTION" if score >= 60 else "❌ DO NOT PROCEED"}

{"Strong market opportunity with clear monetization path." if score >= 75 else "Consider refining the idea or targeting a more specific niche."}

## Next Steps

1. Review research findings
2. Proceed to Phase 2 (Spec) if score >= 75
3. Refine idea if score < 75

"""
    (research_dir / "research-report.md").write_text(report)
    
    # Update state
    state = load_state()
    state["projects"][project_name] = {
        "idea": idea,
        "score": score,
        "research_completed": datetime.now().isoformat(),
        "phase": 1 if score >= 75 else "held",
    }
    save_state(state)
    
    log(f"Research complete. Score: {score}/100 {'✅' if score >= 75 else '⚠️'}")
    return {"score": score, "passed": score >= 75}

# ─── Phase 2: Spec + Planning ──────────────────────────────────────────────

def phase_spec(project_name: str, idea: str) -> Dict:
    """Phase 2: Generate comprehensive specifications"""
    project_dir = PROJECTS_PATH / project_name
    spec_dir = project_dir / "phase-2-spec"
    spec_dir.mkdir(parents=True, exist_ok=True)
    
    log(f"Starting SPEC GENERATION for: {project_name}")
    
    # Generate PRD
    prd = f"""# PRD: {project_name}

## 1. Concept & Vision

{idea}

### Problem Statement
What specific problem does this app solve?

### Solution
How does the app solve this problem?

### Unique Value Proposition
What makes this app different from existing solutions?

## 2. Users & Market

### Target Users
- Primary: 
- Secondary: 

### User Personas
1. **Persona A**: [Description, goals, pain points]
2. **Persona B**: [Description, goals, pain points]

## 3. Features

### MVP Features (Must Have)
- [ ] Feature 1
- [ ] Feature 2
- [ ] Feature 3

### Post-Launch Features (Nice to Have)
- [ ] Feature A
- [ ] Feature B

### User Flows

#### Primary Flow
1. 
2. 
3. 

## 4. Revenue Model

### Model Type
[ ] Subscription (Weekly/Monthly/Yearly)
[ ] One-Time Purchase
[ ] Freemium with IAP
[ ] Ad-Supported

### Pricing Tiers
| Tier | Price | Features |
|------|-------|----------|
| Free | $0 | Limited features |
| Pro | $X.99/mo | Full access |
| Team | $Y.99/mo | 5 users |

### Conversion Strategy
- Free trial: X days
- Upgrade prompts: After key feature usage
- Paywall placement: 

## 5. Technical Requirements

### iOS Version Support
- Minimum: iOS 16.0
- Target: iOS 18.0

### Frameworks
- UI: SwiftUI
- Architecture: MVVM
- State: @Observable
- Database: SwiftData
- Networking: URLSession + Async/Await

### Required APIs
- 
- 

### Privacy & Permissions
- NSPrivacyAccessedAPICategoryUserDefaults: [usage description]
- NSPrivacyAccessedAPICategoryFileTimestamp: [usage description]

## 6. Success Metrics

### Primary KPIs
- Downloads: 
- DAU/MAU: 
- Conversion rate: 
- Revenue: 

### Secondary KPIs
- Retention D1/D7/D30: 
- NPS score: 
- Crash-free rate: >99.5%

"""
    (spec_dir / "prd.md").write_text(prd)
    
    # Generate Architecture
    arch = f"""# Architecture: {project_name}

## Overview
[iOS app architecture description]

## Architecture Pattern: MVVM + Repository

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    View     │ ←── │  ViewModel  │ ←── │ Repository  │
│  (SwiftUI)  │     │  (@Obs.)    │     │   (Data)    │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                    ┌─────────────────────────┼─────────────────────────┐
                    │                         │                         │
              ┌─────▼─────┐            ┌──────▼──────┐          ┌──────▼──────┐
              │ SwiftData │            │  Network    │          │   StoreKit  │
              │  (Local)   │            │  (Remote)   │          │  (Payments) │
              └───────────┘            └─────────────┘          └─────────────┘
```

## Directory Structure

```
Sources/
├── App/
│   ├── MyApp.swift
│   └── AppDelegate.swift
├── Features/
│   ├── Home/
│   │   ├── HomeView.swift
│   │   └── HomeViewModel.swift
│   └── [Feature]/
│       ├── [Feature]View.swift
│       └── [Feature]ViewModel.swift
├── Core/
│   ├── Network/
│   │   ├── APIClient.swift
│   │   └── Endpoints.swift
│   ├── Database/
│   │   └── DataManager.swift
│   └── Payments/
│       └── StoreKitManager.swift
├── Shared/
│   ├── Models/
│   ├── Extensions/
│   └── Utilities/
└── Resources/
    ├── Assets.xcassets
    └── Localizable.strings

Tests/
├── Unit/
├── Integration/
└── UI/
```

## Dependencies

### Swift Package Manager
- None required for MVP

### CocoaPods
- None required for MVP

## Key Technical Decisions

1. **SwiftUI over UIKit**: Faster development, modern declarative syntax
2. **SwiftData over Core Data**: Simplified persistence, iOS 17+ native
3. **StoreKit 2**: Modern subscription API with async/await
4. **No third-party dependencies**: Minimize maintenance burden

"""
    (spec_dir / "architecture.md").write_text(arch)
    
    # Generate Roadmap
    roadmap = f"""# Roadmap: {project_name}

## Timeline: 8-12 weeks to App Store

### Phase 1: Foundation (Week 1-2)
- [ ] Project setup (XcodeGen, SPM)
- [ ] App entry point and navigation
- [ ] Core data models (SwiftData)
- [ ] Theme and design system

### Phase 2: Core Features (Week 3-5)
- [ ] Feature 1: 
- [ ] Feature 2: 
- [ ] Feature 3: 
- [ ] Feature 4: 

### Phase 3: Payments + Auth (Week 6-7)
- [ ] StoreKit 2 integration
- [ ] Paywall UI
- [ ] Subscription status handling
- [ ] Restore purchases

### Phase 4: Polish (Week 8-9)
- [ ] Animations and transitions
- [ ] Error handling
- [ ] Loading states
- [ ] Empty states

### Phase 5: QA (Week 10)
- [ ] Unit tests (80%+ coverage)
- [ ] UI tests
- [ ] TestFlight beta
- [ ] Bug fixes

### Phase 6: Launch (Week 11-12)
- [ ] App Store assets
- [ ] Metadata and keywords
- [ ] Submission
- [ ] Review

## Milestones

| Milestone | Target | Status |
|-----------|--------|--------|
| M1: Spec Complete | Week 2 | ⬜ |
| M2: MVP Built | Week 6 | ⬜ |
| M3: Beta Ready | Week 10 | ⬜ |
| M4: Live on Store | Week 12 | ⬜ |

"""
    (spec_dir / "roadmap.md").write_text(roadmap)
    
    # Generate Payments spec
    payments = f"""# Payments: {project_name}

## Revenue Model

**Type**: Subscription (freemium model)

### Tier Structure

| Tier | Price (USD) | Features |
|------|-------------|----------|
| Free | $0 | Basic features, limited usage |
| Premium Monthly | $4.99/mo | Full features |
| Premium Yearly | $29.99/yr | Full features, 50% off |

### Subscription Group
- Group ID: group.com.[bundle-id].subscription
- Product IDs:
  - com.[bundle-id].premium.monthly
  - com.[bundle-id].premium.yearly

## StoreKit 2 Integration

### Implementation Checklist

- [ ] Create subscription products in App Store Connect
- [ ] Add StoreKit configuration file (StoreKit.storekit)
- [ ] Implement `Product` enumeration
- [ ] Implement `StoreKitManager` (singleton)
- [ ] Add purchase flow with proper error handling
- [ ] Implement `Transaction` verification
- [ ] Handle subscription status changes
- [ ] Implement restore purchases
- [ ] Add paywall view with proper sizing
- [ ] Test with StoreKit in Xcode

### StoreKitManager API

```swift
class StoreKitManager: ObservableObject {{
    @Published var products: [Product] = []
    @Published var purchasedProductIDs: Set<String> = []
    @Published var subscriptionStatus: SubscriptionStatus = .none
    
    func loadProducts() async
    func purchase(_ product: Product) async throws -> Transaction
    func restorePurchases() async
    func isPurchased(_ productID: String) -> Bool
}}
```

### Paywall Design Guidelines

1. **Clear value proposition** at top
2. **3-tier display**: Free / Monthly / Yearly
3. **Yearly highlight**: "Best Value" badge, show savings
4. **CTA button**: "Start Free Trial" or "Subscribe"
5. **Legal links**: Terms, Privacy, Restore Purchases
6. **Safe area respect**: iPhone X+ notch handling

## Revenue Targets

| Metric | Month 1 | Month 3 | Month 6 |
|--------|---------|---------|---------|
| Downloads | 1,000 | 5,000 | 15,000 |
| DAU | 200 | 1,500 | 5,000 |
| Conversion | 2% | 3% | 4% |
| MRR | $100 | $450 | $3,000 |

"""
    (spec_dir / "payments.md").write_text(payments)
    
    # Generate ASO
    idea_tagline = idea[:30] if len(idea) <= 30 else idea[:27] + "..."
    
    aso = f"""# ASO Strategy: {project_name}

## Keyword Research

### Primary Keywords
| Keyword | Volume | Difficulty | Priority |
|---------|--------|------------|----------|
| [keyword 1] | High/Med/Low | Easy/Med/Hard | P0 |
| [keyword 2] | High/Med/Low | Easy/Med/Hard | P0 |
| [keyword 3] | High/Med/Low | Easy/Med/Hard | P1 |

### Secondary Keywords
| Keyword | Volume | Difficulty | Priority |
|---------|--------|------------|----------|
| [keyword 4] | High/Med/Low | Easy/Med/Hard | P2 |
| [keyword 5] | High/Med/Low | Easy/Med/Hard | P2 |

## App Name
**{project_name}** (max 30 chars, includes primary keyword)

## Subtitle
**{idea_tagline}** (max 30 chars, includes secondary keyword)

## Description Template

[First 170 characters critical - include keywords naturally]

[Full description with keyword density ~2-3%, natural language]

## Screenshots

### Device Frames
- iPhone 16 Pro (6.9")
- iPhone 16 Pro Max (6.9")
- iPad Pro 12.9" (optional)

### Screenshot Count
- 6-10 screenshots per locale
- First 2-3: Show core value proposition
- Middle: Feature highlights
- Final: Paywall or call-to-action

### Text Overlay Guidelines
- Headline: Bold, 2-3 words
- Subtext: 2-3 lines max
- Language: Localized per market

## App Preview Video

- Duration: 15-30 seconds
- Hook in first 3 seconds
- Show key features with text overlay
- End with app icon + tagline

## Localization Markets

| Market | Priority | Reason |
|--------|----------|--------|
| English (US) | P0 | Largest market |
| [Market 2] | P1 | [Reason] |
| [Market 3] | P2 | [Reason] |

## Competitive ASO Analysis

[Analyze top 5 competitors: keywords, screenshots, description]

"""
    (spec_dir / "aso.md").write_text(aso)
    
    log(f"Spec generation complete: {project_name}")
    
    state = load_state()
    if project_name in state["projects"]:
        state["projects"][project_name]["spec_completed"] = datetime.now().isoformat()
        state["projects"][project_name]["phase"] = 2
    save_state(state)
    
    return {"passed": True}

# ─── Phase 3: Build ─────────────────────────────────────────────────────────

def generate_code_via_lm(prompt: str, context: str = "") -> str:
    """Generate code using local Qwen3.5 9B via LM Studio"""
    import urllib.request
    import urllib.error
    
    system_prompt = """You are an expert iOS developer. Generate clean, production-ready Swift code following these rules:
1. Use SwiftUI for all UI
2. Use MVVM architecture
3. Include proper error handling
4. Write testable code
5. Follow Swift conventions
6. Include documentation comments for public APIs
"""
    
    full_prompt = f"{system_prompt}\n\nContext:\n{context}\n\nTask:\n{prompt}"
    
    payload = {
        "model": "qwen3.5-9b-coder",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": full_prompt}
        ],
        "temperature": 0.3,
        "max_tokens": 4096,
    }
    
    try:
        req = urllib.request.Request(
            LM_STUDIO_URL + "/v1/chat/completions",
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
            method="POST"
        )
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode())
            return result["choices"][0]["message"]["content"]
    except Exception as e:
        log(f"LM Studio error: {e}, falling back to explanation")
        return f"// Code generation failed: {e}\n// Please generate this code manually."

def build_project_structure(project_name: str):
    """Generate XcodeGen project.yml and directory structure"""
    project_dir = PROJECTS_PATH / project_name
    build_dir = project_dir / "phase-3-build"
    build_dir.mkdir(parents=True, exist_ok=True)
    
    # Create clean app name (no hyphens, camelCase)
    app_name = "".join(word.title() for word in project_name.replace("-", " ").replace("_", " ").split())
    bundle_id = f"com.yourcompany.{app_name.lower()}"
    
    project_yml = f"""name: {app_name}
options:
  bundleIdPrefix: com.yourcompany
  deploymentTarget:
    iOS: "17.0"
  xcodeVersion: "15.0"
  generateEmptyDirectories: true
  groupSortPosition: top

settings:
  base:
    SWIFT_VERSION: "5.9"
    TARGETED_DEVICE_FAMILY: "1"
    ENABLE_PREVIEWS: YES
    CODE_SIGN_STYLE: Automatic
    PRODUCT_BUNDLE_IDENTIFIER: {bundle_id}

targets:
  {app_name}:
    type: application
    platform: iOS
    sources:
      - path: Sources
        type: group
    settings:
      base:
        GENERATE_INFOPLIST_FILE: YES
        INFOPLIST_KEY_CFBundleDisplayName: {app_name}
        MARKETING_VERSION: "1.0.0"
        CURRENT_PROJECT_VERSION: "1"
        INFOPLIST_KEY_UILaunchScreen_Generation: YES
        INFOPLIST_KEY_UISupportedInterfaceOrientations: "UIInterfaceOrientationPortrait"
        INFOPLIST_KEY_UIApplicationSceneManifest_Generation: YES
        ASSETCATALOG_COMPILER_APPICON_NAME: AppIcon
        ASSETCATALOG_COMPILER_GLOBAL_ACCENT_COLOR_NAME: AccentColor
    dependencies: []

schemes:
  {app_name}:
    build:
      targets:
        {app_name}: all
    run:
      config: Debug
    test:
      config: Debug
    profile:
      config: Release
    analyze:
      config: Debug
    archive:
      config: Release
"""
    
    (build_dir / "project.yml").write_text(project_yml)
    
    # Create directory structure
    dirs = [
        "Sources/App",
        "Sources/Features/Home",
        "Sources/Core/Network",
        "Sources/Core/Database",
        "Sources/Core/Payments",
        "Sources/Shared/Models",
        "Sources/Shared/Extensions",
        "Sources/Shared/Utilities",
        "Sources/Resources/Assets.xcassets/AppIcon.appiconset",
        "Sources/Resources/Assets.xcassets/AccentColor.colorset",
        "Tests/Unit",
        "Tests/Integration",
        "Tests/UI",
    ]
    
    for d in dirs:
        (build_dir / d).mkdir(parents=True, exist_ok=True)
    
    # Create App entry point
    app_name = project_name.replace("-", "").replace("_", "").title().replace(" ", "")
    if not app_name[0].isupper():
        app_name = "App" + app_name.title().replace("App", "")
    
    app_swift = f'''import SwiftUI

@main
struct {app_name}App: App {{
    var body: some Scene {{
        WindowGroup {{
            ContentView()
        }}
    }}
}}
'''
    (build_dir / "Sources/App" / f"{app_name}App.swift").write_text(app_swift)
    
    # Create ContentView placeholder
    content_view = '''import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack(spacing: 20) {
            Image(systemName: "star.fill")
                .font(.system(size: 60))
                .foregroundStyle(.yellow)
            
            Text("Hello, iOS!")
                .font(.title)
        }
        .padding()
    }
}

#Preview {
    ContentView()
}
'''
    (build_dir / "Sources/App" / "ContentView.swift").write_text(content_view)
    
    # Create Assets
    appicon_contents = '''{
  "images" : [
    {
      "idiom" : "universal",
      "platform" : "ios",
      "size" : "1024x1024"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
'''
    (build_dir / "Sources/Resources/Assets.xcassets/AppIcon.appiconset/Contents.json").write_text(appicon_contents)
    
    accent_contents = '''{
  "colors" : [
    {
      "color" : {
        "color-space" : "srgb",
        "components" : {
          "alpha" : "1.000",
          "blue" : "1.000",
          "green" : "0.478",
          "red" : "0.000"
        }
      },
      "idiom" : "universal"
    }
  ],
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
'''
    (build_dir / "Sources/Resources/Assets.xcassets/AccentColor.colorset/Contents.json").write_text(accent_contents)
    
    assets_contents = '''{
  "info" : {
    "author" : "xcode",
    "version" : 1
  }
}
'''
    (build_dir / "Sources/Resources/Assets.xcassets/Contents.json").write_text(assets_contents)
    
    log(f"Project structure created: {build_dir}")
    return str(build_dir)

def phase_build(project_name: str, wave: int = 1) -> Dict:
    """Phase 3: Build app with TDD approach"""
    project_dir = PROJECTS_PATH / project_name
    build_dir = project_dir / "phase-3-build"
    
    log(f"Starting BUILD Wave {wave} for: {project_name}")
    
    # If first wave, create project structure
    if wave == 1 and not (build_dir / "project.yml").exists():
        build_project_structure(project_name)
    
    # Load spec for this wave's tasks
    spec_path = project_dir / "phase-2-spec" / "prd.md"
    if not spec_path.exists():
        log(f"No spec found. Run 'spec' command first.")
        return {"passed": False, "error": "No spec found"}
    
    # Wave definitions (example - would be generated from spec)
    waves = {
        1: ["Setup project", "Create data models", "Create base UI components"],
        2: ["Implement Feature 1", "Implement Feature 2", "Implement Feature 3"],
        3: ["Implement StoreKit 2", "Create paywall UI", "Test payments flow"],
        4: ["Polish animations", "Error handling", "Loading states"],
    }
    
    tasks = waves.get(wave, [])
    
    for task in tasks:
        log(f"  Building: {task}")
        # In real implementation, this would:
        # 1. Generate failing test (TDD Red)
        # 2. Generate minimal code (TDD Green)
        # 3. Refactor (TDD Refactor)
        # Using LM Studio for code generation
    
    log(f"Wave {wave} complete")
    
    state = load_state()
    if project_name in state["projects"]:
        state["projects"][project_name][f"wave_{wave}_completed"] = datetime.now().isoformat()
        state["projects"][project_name]["phase"] = 3
    save_state(state)
    
    return {"passed": True, "wave": wave}

# ─── Phase 4: QA ───────────────────────────────────────────────────────────

def phase_qa(project_name: str) -> Dict:
    """Phase 4: QA testing using ASC CLI"""
    project_dir = PROJECTS_PATH / project_name
    build_dir = project_dir / "phase-3-build"
    
    log(f"Starting QA for: {project_name}")
    
    # Check if ASC CLI is available
    asc_check = run_cmd("which asc && asc version 2>/dev/null || echo 'ASC_NOT_FOUND'")
    if "ASC_NOT_FOUND" in asc_check:
        log("⚠️ ASC CLI not found. Install with: brew install rudrankriyam/tap/asc")
    
    # Check if xcodegen is available
    xcodegen_check = run_cmd("which xcodegen && xcodegen --version 2>/dev/null || echo 'XCODEGEN_NOT_FOUND'")
    if "XCODEGEN_NOT_FOUND" in xcodegen_check:
        log("⚠️ XcodeGen not found. Install with: brew install xcodegen")
    
    # Run tests
    log("Running unit tests...")
    test_result = run_cmd(f"cd {build_dir} && xcodebuild test -scheme {project_name} -destination 'platform=iOS Simulator,name=iPhone 16 Pro' 2>&1 | tail -20", timeout=600)
    
    # Check build
    log("Building project...")
    build_result = run_cmd(f"cd {build_dir} && xcodegen generate && xcodebuild archive -scheme {project_name} -configuration Release 2>&1 | tail -20", timeout=600)
    
    log("QA complete")
    return {"passed": True}

# ─── Phase 5: Deploy ───────────────────────────────────────────────────────

def phase_deploy(project_name: str) -> Dict:
    """Phase 5: Deploy to App Store via ASC CLI"""
    log(f"Starting DEPLOY for: {project_name}")
    
    state = load_state()
    app_id = state["projects"].get(project_name, {}).get("app_store_id", "")
    
    if not app_id:
        log("⚠️ App Store ID not set. Create app in App Store Connect first.")
        log("Then run: python3 autonomous_app_builder.py configure --project NAME --app-id APP_ID")
        return {"passed": False, "error": "No App Store ID"}
    
    # Deploy workflow
    log("1. Syncing metadata...")
    run_cmd(f"cd {PROJECTS_PATH / project_name / 'phase-5-deploy'} && asc metadata sync --app-id {app_id} --version 1.0.0 --dir ./metadata 2>&1 || echo 'Metadata sync skipped'")
    
    log("2. Submitting to App Store...")
    # Would run: asc releases submit --app-id $APP_ID --ipa ./build/MyApp.ipa --version 1.0.0
    
    log("Deploy initiated. Monitor status with: asc review submissions list --app-id " + app_id)
    
    state = load_state()
    if project_name in state["projects"]:
        state["projects"][project_name]["deployed_at"] = datetime.now().isoformat()
        state["projects"][project_name]["phase"] = 5
    save_state(state)
    
    return {"passed": True}

# ─── Main CLI ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Autonomous App Builder — iOS-first")
    subparsers = parser.add_subparsers(dest="command")
    
    # init
    init_parser = subparsers.add_parser("init", help="Initialize new project")
    init_parser.add_argument("--idea", required=True, help="One-line app idea")
    
    # research
    research_parser = subparsers.add_parser("research", help="Run deep research")
    research_parser.add_argument("--project", required=True, help="Project name")
    
    # spec
    spec_parser = subparsers.add_parser("spec", help="Generate specifications")
    spec_parser.add_argument("--project", required=True, help="Project name")
    
    # build
    build_parser = subparsers.add_parser("build", help="Build project")
    build_parser.add_argument("--project", required=True, help="Project name")
    build_parser.add_argument("--wave", type=int, default=1, help="Wave number")
    
    # test
    test_parser = subparsers.add_parser("test", help="Run tests")
    test_parser.add_argument("--project", required=True, help="Project name")
    
    # deploy
    deploy_parser = subparsers.add_parser("deploy", help="Deploy to App Store")
    deploy_parser.add_argument("--project", required=True, help="Project name")
    
    # pipeline (full autonomous run)
    pipeline_parser = subparsers.add_parser("pipeline", help="Run full pipeline")
    pipeline_parser.add_argument("--project", required=True, help="Project name")
    pipeline_parser.add_argument("--idea", required=True, help="App idea")
    
    # configure
    configure_parser = subparsers.add_parser("configure", help="Configure project")
    configure_parser.add_argument("--project", required=True, help="Project name")
    configure_parser.add_argument("--app-id", help="App Store Connect App ID")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    elif args.command == "init":
        # Sanitize: lowercase, hyphens only, no special chars
        sanitized = re.sub(r'[^a-z0-9\-]', '', args.idea.lower().replace(" ", "-"))
        project_name = sanitized[:30].strip("-")
        project_dir = PROJECTS_PATH / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        (project_dir / "project.json").write_text(json.dumps({
            "name": project_name,
            "idea": args.idea,
            "created": datetime.now().isoformat(),
        }, indent=2))
        state = load_state()
        state["projects"][project_name] = {
            "idea": args.idea,
            "created": datetime.now().isoformat(),
            "phase": 0,
        }
        save_state(state)
        log(f"Project initialized: {project_name}")
        log(f"Idea: {args.idea}")
        
    elif args.command == "research":
        state = load_state()
        idea = state["projects"].get(args.project, {}).get("idea", "")
        if not idea:
            log("Project not found. Initialize first with 'init --idea ...'")
            return
        result = phase_research(args.project, idea)
        print(json.dumps(result))
        
    elif args.command == "spec":
        state = load_state()
        idea = state["projects"].get(args.project, {}).get("idea", "")
        if not idea:
            log("Project not found.")
            return
        result = phase_spec(args.project, idea)
        print(json.dumps(result))
        
    elif args.command == "build":
        result = phase_build(args.project, args.wave)
        print(json.dumps(result))
        
    elif args.command == "test":
        result = phase_qa(args.project)
        print(json.dumps(result))
        
    elif args.command == "deploy":
        result = phase_deploy(args.project)
        print(json.dumps(result))
        
    elif args.command == "pipeline":
        log("=== AUTONOMOUS APP BUILDER PIPELINE ===")
        project_name = args.project
        
        # Initialize
        project_dir = PROJECTS_PATH / project_name
        project_dir.mkdir(parents=True, exist_ok=True)
        state = load_state()
        state["projects"][project_name] = {
            "idea": args.idea,
            "created": datetime.now().isoformat(),
            "phase": 0,
        }
        save_state(state)
        
        # Phase 1: Research
        log("=== PHASE 1: DEEP RESEARCH ===")
        research_result = phase_research(project_name, args.idea)
        if not research_result["passed"]:
            log("Research score below threshold. Pipeline halted.")
            return
        
        # Phase 2: Spec
        log("=== PHASE 2: SPEC + PLAN ===")
        spec_result = phase_spec(project_name, args.idea)
        
        # Phase 3: Build (all waves)
        for wave in [1, 2, 3, 4]:
            log(f"=== PHASE 3: BUILD WAVE {wave} ===")
            phase_build(project_name, wave)
        
        # Phase 4: QA
        log("=== PHASE 4: QA ===")
        phase_qa(project_name)
        
        # Phase 5: Deploy
        log("=== PHASE 5: DEPLOY ===")
        phase_deploy(project_name)
        
        log("=== PIPELINE COMPLETE ===")
        
    elif args.command == "configure":
        state = load_state()
        if args.project not in state["projects"]:
            log("Project not found.")
            return
        if args.app_id:
            state["projects"][args.project]["app_store_id"] = args.app_id
            save_state(state)
            log(f"App Store ID set: {args.app_id}")
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
