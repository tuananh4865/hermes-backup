---
title: "Nexus — Product Specification"
created: 2026-04-12
updated: 2026-04-12
type: spec
tags: [nexus, ios, spec]
phase: spec
---

# Nexus — Product Specification

## Objective

Build Nexus, a native iOS note-taking app with graph view and AI wiki features. Target: Obsidian power users who hate the iOS experience. Price: $4.99/mo vs Obsidian's $24/mo.

**Core promise**: "Obsidian's killer features — graph view, wiki-links, local files — with an iOS app that actually works, plus built-in AI."

**Assumptions I'm making:**
1. iOS-only first, iPad later (not cross-platform Mac initially)
2. SwiftUI for UI (not UIKit)
3. SwiftData for note storage (not Core Data / SQLite)
4. iCloud for sync (not custom backend)
5. StoreKit 2 for subscriptions
6. Graph rendering: custom SwiftUI Canvas (not a library)
7. Markdown: custom parser (not a library)
8. AI features: Apple ML frameworks + optional cloud fallback
9. App name confirmed: **Nexus**

→ Correct me now or I'll proceed with these.

---

## 1. Product Vision

### What We're Building
- **Native iOS app** (SwiftUI) for note-taking with graph visualization
- **Obsidian-compatible**: reads/writes `.md` files with ``
- **AI-powered**: semantic search, auto-linking suggestions, smart tags
- **Local-first**: all data on device, optional iCloud sync

### Target User
- Obsidian power user frustrated with iOS app (2.3★ rating)
- Note-taking enthusiasts wanting better mobile experience
- Apple ecosystem users who want native iOS performance

### Success Criteria
- [ ] Graph view renders 500+ nodes at 60fps
- [ ] Wiki-links `` parsed and clickable in < 100ms
- [ ] iCloud sync works across iPhone + iPad
- [ ] Subscription flow works with StoreKit 2
- [ ] App Store submission passes review

---

## 2. UI/UX Specification

### Color Palette
```
Background Primary:   #0A0A0F (near black)
Background Secondary: #1A1A24 (dark navy)
Surface:             #252532 (card background)
Text Primary:         #FFFFFF
Text Secondary:       #8E8E9A
Accent Primary:       #6366F1 (indigo — graph nodes, links)
Accent Secondary:      #818CF8 (lighter indigo)
Success:              #10B981 (green)
Warning:              #F59E0B (amber)
Error:                #EF4444 (red)
Wiki-link:            #A78BFA (violet — distinct from accent)
```

### Typography
```
Font Family: SF Pro (system)
Title Large:   34pt Bold
Title:         28pt Bold
Headline:      17pt Semibold
Body:          17pt Regular
Caption:       12pt Regular
Code/Mono:     SF Mono 15pt
```

### Spacing System (8pt grid)
```
xxs:  4pt
xs:   8pt
sm:  12pt
md:  16pt
lg:  24pt
xl:  32pt
xxl: 48pt
```

### Screen Structure

#### 1. Home Screen (Notes List)
- **Navigation**: Single column, scrollable list
- **Header**: "Nexus" title + search icon + settings icon
- **List Items**:
  - Note title (17pt semibold)
  - Preview text (12pt, 2 lines max, #8E8E9A)
  - Last modified date (12pt, #8E8E9A)
  - Wiki-link count badge (if any)
- **FAB**: "+" button bottom-right, creates new note
- **Empty State**: "Start your first note" with link icon illustration

#### 2. Note Editor Screen
- **Navigation**: Back button, share button, more (...) menu
- **Title Field**: 28pt bold, editable, placeholder "Untitled"
- **Content Area**: Full-screen Markdown editor
  - Live rendering of `` in violet (#A78BFA)
  - `` are tappable → navigate to linked note (or create if missing)
  - **Editor modes**: Write mode (plain text) / Preview mode (rendered)
  - Toggle via toolbar button
- **Toolbar** (bottom):
  - Bold | Italic | Link | Wiki-link | Checkbox | Code
  - Mode toggle (Write/Preview)
- **Auto-save**: Every keystroke (debounced 500ms)

#### 3. Graph View Screen
- **Navigation**: Back, fullscreen toggle, filter button
- **Canvas**: Full-screen force-directed graph
  - **Nodes**: Circles, size = number of connections (min 8pt, max 40pt)
  - **Node color**: Accent gradient based on connection count
  - **Edges**: Lines between linked notes, 0.5pt, #6366F1 at 40% opacity
  - **Labels**: Note title below node, 10pt, only shown when zoomed in
  - **Interactions**:
    - Pinch to zoom (0.5x to 3x)
    - Pan to scroll
    - Tap node → highlight connections + show note preview popup
    - Double-tap node → open note
    - Long-press node → quick actions (open, delete, pin)
- **Filter Panel** (bottom sheet):
  - Filter by folder
  - Filter by tag
  - Filter by date range
  - Show orphan notes toggle

#### 4. Search Screen
- **Navigation**: Cancel button
- **Search Bar**: Auto-focus on appear, "Search notes..." placeholder
- **Results**: List view, same as Home list items
- **Filters** (below search bar):
  - All / Title / Content / Tags
- **AI Toggle**: "Semantic Search" (Pro only) — searches by meaning

#### 5. Settings Screen
- **Sections**:
  - **Account**: Subscription status, upgrade button
  - **Sync**: iCloud on/off, last sync time
  - **Appearance**: Dark/Light/System (default: Dark)
  - **Editor**: Font size, line spacing
  - **Graph**: Node size scaling, show labels toggle
  - **Data**: Import Obsidian vault, Export all notes
  - **About**: Version, privacy policy, terms

#### 6. Subscription Screen
- **Hero**: "Unlock Nexus Pro"
- **Feature List**:
  - ✓ Unlimited notes
  - ✓ Unlimited graph views
  - ✓ AI semantic search
  - ✓ AI auto-linking suggestions
  - ✓ AI smart tags
  - ✓ iCloud sync
  - ✓ Priority support
- **Pricing**:
  - Monthly: $4.99/mo
  - Yearly: $29.99/yr (Save 50%)
- **CTA**: "Subscribe Now" / "Start Free Trial"
- **Footer**: "Cancel anytime",Restore purchases link

---

## 3. Functionality Specification

### Core Features

#### F1: Note Management
- Create note with title + content
- Edit note with live Markdown preview
- Delete note (with confirmation)
- Duplicate note
- Move note to folder
- Sort: Last modified / Title / Created date

#### F2: Wiki-links (``)
- Parser detects `[[...]]` pattern in note content
- Rendered as violet tappable text
- Tapping navigates to linked note
- If note doesn't exist → create new note with that title
- Backlinks section shows all notes linking TO current note
- Broken links (pointing to deleted notes) shown in red

#### F3: Graph View
- Force-directed layout algorithm (custom Swift implementation)
- Nodes = notes, Edges = wiki-links
- Real-time updates when notes change
- Performance target: 60fps with 500+ nodes
- Minimap in corner (small, toggleable)

#### F4: Markdown Editor
- Full Markdown support:
  - Headings (H1-H6)
  - Bold, Italic, Strikethrough
  - Bullet lists, Numbered lists, Checkboxes
  - Code blocks (inline and fenced)
  - Blockquotes
  - Horizontal rules
  - Images (from Photos or URL)
- Tappable wiki-links within editor
- Keyboard shortcuts (external keyboard)

#### F5: Search
- Full-text search (title + content)
- Filter by: All / Title / Content / Tags
- Recent searches saved
- **Pro AI feature**: Semantic search (meaning-based, not keyword)

#### F6: iCloud Sync
- Automatic sync via iCloud Documents
- Conflict resolution: Last-write-wins
- Offline-first: Works without internet
- Sync status indicator in settings

#### F7: Subscription (StoreKit 2)
- Free tier: 50 notes max, 3 graph views/day
- Pro: $4.99/mo or $29.99/yr
- Paywall on: Unlimited notes, AI features, sync
- Restore purchases supported

### Architecture Pattern: MVVM + Repository

```
Views (SwiftUI)
    ↓
ViewModels (@Observable)
    ↓
Repositories (NotesRepository, SyncRepository)
    ↓
Services (MarkdownService, GraphLayoutEngine, SyncService)
    ↓
Data Layer (SwiftData, iCloud)
```

### Data Model

```swift
@Model
class Note {
    @Attribute(.unique) var id: UUID
    var title: String
    var content: String          // Raw markdown
    var createdAt: Date
    var modifiedAt: Date
    var folder: String?          // nil = root
    var tags: [String]
    var isPinned: Bool
    
    // Computed (not stored)
    var wikiLinks: [String]      // Extracted 
    var backlinks: [Note]         // Notes linking to this
    var connectionCount: Int      // For graph node sizing
}
```

### Error Handling
- Sync failures → Show banner, retry with exponential backoff
- iCloud unavailable → Local-only mode, prompt user
- Broken wiki-link → Show red link, offer to create note
- StoreKit failure → Show error, allow retry

---

## 4. Technical Specification

### Tech Stack
```
iOS:        17.0+
Swift:      5.9+
SwiftUI:    iOS 17+
SwiftData:  iOS 17+
Xcode:      15.0+
StoreKit:   StoreKit 2
```

### Key Dependencies (Swift Package Manager)
```
1. SplashSwiftUI     — Markdown syntax highlighting
   URL: https://github.com/JohnSundell/SplashSwiftUI
   Purpose: Code block syntax highlighting

2. (No other external deps — build everything native)
```

### Project Structure
```
Nexus/
├── App/
│   ├── NexusApp.swift           # @main, SwiftData container
│   └── AppState.swift           # @Observable global state
├── Models/
│   ├── Note.swift               # SwiftData @Model
│   ├── Folder.swift             # SwiftData @Model
│   └── Subscription.swift       # StoreKit state
├── Views/
│   ├── Home/
│   │   ├── HomeView.swift
│   │   └── NoteRowView.swift
│   ├── Editor/
│   │   ├── EditorView.swift
│   │   ├── MarkdownEditorView.swift
│   │   ├── MarkdownPreviewView.swift
│   │   └── WikiLinkTextView.swift
│   ├── Graph/
│   │   ├── GraphView.swift
│   │   ├── GraphCanvasView.swift
│   │   └── GraphNodeView.swift
│   ├── Search/
│   │   └── SearchView.swift
│   ├── Settings/
│   │   └── SettingsView.swift
│   ├── Subscription/
│   │   └── SubscriptionView.swift
│   └── Components/
│       ├── WikiLinkText.swift
│       └── EmptyStateView.swift
├── ViewModels/
│   ├── HomeViewModel.swift
│   ├── EditorViewModel.swift
│   ├── GraphViewModel.swift
│   └── SearchViewModel.swift
├── Services/
│   ├── MarkdownParser.swift     # Parse markdown → attributed string
│   ├── WikiLinkExtractor.swift  # Extract  from content
│   ├── GraphLayoutEngine.swift # Force-directed layout algorithm
│   └── SubscriptionManager.swift # StoreKit 2 wrapper
├── Repositories/
│   ├── NotesRepository.swift    # SwiftData CRUD operations
│   └── SyncRepository.swift     # iCloud sync logic
└── Resources/
    ├── Assets.xcassets
    └── Preview Content/
```

### Commands
```bash
# Generate Xcode project
xcodegen generate

# Build for iOS Simulator
xcodebuild -project Nexus.xcodeproj -scheme Nexus -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 16' build

# Build with XcodeGen + ASC
xcodegen generate && xcodebuild -project Nexus.xcodeproj -scheme Nexus -configuration Debug -destination 'platform=iOS Simulator,name=iPhone 16' build

# ASC upload (after build)
asc upload --path build/Nexus.ipa --app nexus
```

### Testing Strategy
- **Unit tests**: MarkdownParser, WikiLinkExtractor, GraphLayoutEngine
- **UI tests**: Navigation, note creation, graph interaction
- **StoreKit tests**: Subscription flow (use StoreKit Testing in Xcode)

---

## 5. Boundaries

### Always Do
- Use SwiftData for persistence
- Commit to git after every feature/task completion
- Test on physical iPhone before submission
- Run ASC validation before upload

### Ask First
- Adding external dependencies (first preference: native implementation)
- Changing color palette or typography
- Adding new screens (need spec update)
- Modifying subscription pricing

### Never Do
- Use UIKit for new screens (SwiftUI only)
- Store notes in custom backend (iCloud only for sync)
- Hard-code strings (use StringCatalog)
- Submit without testing on physical device

---

## 6. Success Criteria — MVP Check

Before calling MVP done, verify ALL:
- [ ] Can create, edit, delete a note
- [ ] Wiki-links `` are parsed and tappable
- [ ] Graph view renders with at least 20 sample notes
- [ ] Graph supports pinch-zoom and pan
- [ ] Search finds notes by title and content
- [ ] Dark mode renders correctly
- [ ] App builds successfully with xcodebuild
- [ ] App runs on iOS 17+ simulator

---

## 7. Open Questions

1. **App icon** — Who designs? Stock image for now?
2. **Onboarding** — Skip or 3-screen walkthrough?
3. **Widget** — Home screen widget? (Future v2)
4. **Watch app** — Apple Watch quick capture? (Future v2)
5. **Localization** — Vietnamese + English only for now?

---

*Last updated: 2026-04-12*
