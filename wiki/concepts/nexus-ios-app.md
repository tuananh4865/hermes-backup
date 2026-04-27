---
title: "Nexus iOS App"
created: 2026-04-14
updated: 2026-04-14
type: project
status: active
tags: [nexus, ios, swiftui, swiftdata, graph-view, wiki-links, storekit]
description: Native iOS note-taking app with graph view and AI wiki features — Obsidian competitor
source: raw/transcripts/2026-04-14/2026-04-14-tun-project-ang.md
---

# Nexus iOS App

**Status**: Active  
**Phase**: Phase 2 Core Navigation Flow (PASS)  
**Price Target**: $4.99/mo vs Obsidian $24/mo

## Overview

Nexus is a native iOS note-taking app that combines Obsidian's killer features (graph view, wiki-links, local files) with AI-powered knowledge management. Built with SwiftUI and SwiftData.

## Technical Stack

- **UI Framework**: SwiftUI
- **Data Persistence**: SwiftData
- **Graph Rendering**: Custom SwiftUI Canvas with force-directed physics
- **Subscriptions**: StoreKit 2
- **Platform**: iOS 17+ (iPhone 17 Simulator tested)

## Key Features Implemented

### Phase 1: MVP Build ✅
- [x] Create, edit, delete notes
- [x] Wiki-links `[[note-name]]` parsed and tappable
- [x] Graph view renders with sample notes
- [x] Search by title and content
- [x] Dark mode (#0A0A0F background, #6366F1 accent)
- [x] App builds and runs on iOS 17+ simulator

### Phase 2: Core Navigation Flow ✅
- [x] Home → tap note → Editor
- [x] Editor → toggle Preview → tappable wiki-links
- [x] Tap wiki-link → navigate to linked note (or create new)
- [x] Back navigation works
- [x] Note saves on Done

## Key Technical Patterns

### ZStack + Opacity for Auto-Show Graph

SwiftUI requires both views present in view hierarchy for smooth transitions:

```swift
ZStack {
    HomeViewContent(showGraph: $showGraph)
        .opacity(showGraph ? 0 : 1)
    GraphView(notes: notes, isPresented: $showGraph)
        .opacity(showGraph ? 1 : 0)
}
.onAppear {
    loadSampleDataIfNeeded(context: modelContext)
    DispatchQueue.main.asyncAfter(deadline: .now() + 1.0) {
        showGraph = true
    }
}
```

**Why this works**: `if/else` conditional removes view from hierarchy; ZStack keeps both views present with opacity control.

### Tappable Wiki-Links with UITextView

```swift
struct TappableMarkdownView: UIViewRepresentable {
    let content: String
    let onWikiLinkTap: (String) -> Void
    
    func makeUIView(context: Context) -> UITextView {
        let tv = UITextView()
        tv.isEditable = false
        tv.isScrollEnabled = false
        tv.linkTextAttributes = [
            .foregroundColor: UIColor.systemBlue,
            .underlineStyle: NSUnderlineStyle.single.rawValue
        ]
        tv.delegate = context.coordinator
        return tv
    }
    
    func updateUIView(_ uiView: UITextView, context: Context) {
        let attributedString = buildStyledText(content)
        uiView.attributedText = attributedString
    }
    
    private func buildStyledText(_ text: String) -> NSAttributedString {
        // Parse markdown + wiki-links, apply styling
        // Wiki-links get NSLinkAttributeName with callback
    }
}
```

### Wiki-Link Navigation Logic

```swift
private func handleWikiLinkTap(noteTitle: String) {
    let descriptor = FetchDescriptor<Note>(
        predicate: #Predicate { $0.title == noteTitle }
    )
    
    if let existingNotes = try? modelContext.fetch(descriptor),
       let existingNote = existingNotes.first {
        // Navigate to existing note
        navigationPath.append(existingNote)
    } else {
        // Create new note
        let newNote = Note(title: noteTitle, content: "", ...)
        modelContext.insert(newNote)
        navigationPath.append(newNote)
    }
}
```

### @Query for Reactive SwiftData

SwiftUI's `@Query` auto-updates when data changes — no manual state sync needed:

```swift
struct GraphViewWrapper: View {
    @Query(sort: \Note.modifiedAt, order: .reverse) private var notes: [Note]
    
    var body: some View {
        GraphView(notes: notes, isPresented: $showGraph)
    }
}
```

## Sample Data

21 interconnected sample notes with wiki-links for graph testing:
- Welcome to Nexus, Graph View, Markdown Features
- Bidirectional Links, AI Integration, Knowledge Management
- Obsidian Tips, Quick Capture, Mobile Sync, Version History
- And 11 more notes creating network clusters

## Build & Run Commands

```bash
# Generate Xcode project
xcodegen generate

# Build
xcodebuild -scheme Nexus -destination 'platform=iOS Simulator,name=iPhone 17' build

# Launch on simulator
xcrun simctl launch booted com.nexus.app

# Screenshot
xcrun simctl io booted screenshot PATH.png
```

## Related Concepts

- [[SwiftUI]] — UI framework
- [[SwiftData]] — Data persistence
- [[StoreKit 2]] — In-app subscriptions
- [[Graph View Pattern]] — Force-directed graph visualization
