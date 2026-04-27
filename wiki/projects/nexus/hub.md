---
title: "Nexus — Obsidian Competitor"
created: 2026-04-11
updated: 2026-04-14
type: project
status: active
phase: phase-2-core-features
tags: [nexus, ios, notes, graph-view, swiftui]
confidence: high
relationships:
  - autonomous-app-builder
---

# Nexus — Obsidian Competitor

**Status**: Active
**Started**: 2026-04-11
**Updated**: 2026-04-14
**Target**: iOS native note-taking app with graph view + AI wiki
**Price**: $4.99/mo vs Obsidian $24/mo

---

## Mission

Build Nexus — native iOS note-taking app that combines Obsidian's killer features (graph view, wiki-links, local files) with AI-powered knowledge management. Target: Obsidian power users frustrated with iOS experience.

---

## Phase 1: MVP Build

### Goals
- [x] Can create, edit, delete a note
- [x] Wiki-links `` are parsed and tappable
- [x] Graph view renders with sample notes
- [ ] Graph supports pinch-zoom and pan
- [x] Search finds notes by title and content
- [x] Dark mode renders correctly
- [x] App builds successfully with xcodebuild
- [x] App runs on iOS 17+ simulator

### Progress
|| Date | Milestone | Status ||
||------|-----------|--------|
|| 2026-04-11 | Research + Brainstorm | ✅ Done ||
|| 2026-04-12 | Product Spec (SPEC.md) | ✅ Done ||
|| 2026-04-12 | Code scaffolding (SwiftUI views) | ✅ Done ||
|| 2026-04-14 | Build verified (iPhone 17 Simulator) | ✅ SUCCEEDED ||
|| 2026-04-14 | App running on simulator | ✅ Running ||
|| 2026-04-14 | Sample notes loaded (10 notes) | ✅ Done ||
|| 2026-04-14 | StoreKit 2 subscription flow | ✅ Done ||
|| 2026-04-14 | Tappable wiki-links in preview | ✅ Done ||
|| 2026-04-14 | 21 sample notes with wiki-links | ✅ Done ||
|| 2026-04-14 | Wiki-link navigation (create note on tap) | ✅ Done ||

### New Files Added (2026-04-14)
- `Nexus/Services/SampleDataLoader.swift` — Seeds 21 sample notes for graph testing
- `Nexus/Services/SubscriptionManager.swift` — StoreKit 2 subscription management
- `Nexus/Models/Folder.swift` — SwiftData folder model
- `Nexus/Views/Editor/TappableMarkdownView.swift` — Tappable wiki-links using UITextView

---

## Tech Stack

```
iOS:        17.0+
Swift:      5.9+
SwiftUI:    iOS 17+
SwiftData:  iOS 17+
Xcode:      15.0+
StoreKit:   StoreKit 2
```

---

## Key Files
- `SPEC.md` — Full product specification
- `brainstorm.md` — Market research + competitive analysis
- `Nexus/` — SwiftUI source code
- `project.yml` — XcodeGen configuration

---

## Next Steps

1. [x] Verify graph view renders with sample notes
2. [x] Test wiki-link navigation (tap [[link]] → open note)
3. [x] Test editor with wiki-link insertion
4. [ ] Set up App Store Connect for TestFlight
5. [ ] Physical iPhone testing
6. [ ] ASC validation before submission

### ASC Setup Required
1. Go to https://appstoreconnect.apple.com/access/integrations/api
2. Generate API key for Nexus app
3. Run `asc auth init` to configure
4. Run `asc auth login` with key credentials

### App Store Connect Info
- Bundle ID: `com.nexus.app`
- App Name: Nexus
- Category: Productivity
- Pricing: Free tier + $4.99/mo Pro subscription

---

## Links
- [[SPEC]] — Full specification
- [[brainstorm]] — Research
