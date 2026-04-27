---
title: "Nexus — Phase 2: Core Features"
created: 2026-04-16
updated: 2026-04-16
type: concept
tags: [auto-filled]
---

# Nexus — Phase 2: Core Features

**Started**: 2026-04-15
**Status**: In Progress
**Phase**: phase-2-core-features

---

## Goals

Phase 1 MVP xong → Phase 2 tập trung features làm app dùng được thực sự:

### F1: Backlinks (Editor)
- [ ] Section "Linked to this note" trong EditorView
- [ ] Hiện danh sách notes có ``
- [ ] Tap backlink → navigate tới note đó

### F2: Folders
- [ ] Folder model đã có (Folder.swift tồn tại)
- [ ] Folder list view
- [ ] Move note to folder
- [ ] Filter notes by folder

### F3: Tags
- [ ] Add/view tags trên note
- [ ] Tag input in editor
- [ ] Filter notes by tag
- [ ] Tag overview section

### F4: Sort + Pin
- [ ] Sort options: Last Modified, Title, Created
- [ ] Pin/unpin notes
- [ ] Pinned notes always on top

### F5: StoreKit Paywall Enforcement
- [ ] Count notes — if > 50 and not Pro, block creation
- [ ] Show upsell banner when approaching limit
- [ ] Upgrade button → SubscriptionView

---

## Implementation Notes

### Backlinks
- Need computed backlink list in EditorView
- Query all notes, find those whose content contains ``
- Show as collapsible section at bottom of editor
- Tap → navigate to that note

### Folders
- `Folder.swift` model exists but no views use it yet
- Need `FoldersView.swift` and folder picker in editor
- Notes have `folder: String?` already

### Tags
- Notes have `tags: [String]` already
- Need tag input UI and tag filtering
- Simple `#tag` syntax or comma-separated input

### Sort/Pin
- HomeView @Query needs custom sort binding
- Pinned flag already exists on Note model
- Filter pinned first, then sort remainder

### StoreKit Limit
- SubscriptionManager.shared.isPro check
- If !isPro && notes.count >= 50 → block creation + show paywall

---

## Progress

| Task | Status | Date |
|------|--------|------|
| Backlinks in Editor | ✅ Done | 2026-04-15 |
| Folders UI | ✅ Done | 2026-04-15 |
| Tags system | ✅ Done | 2026-04-15 |
| Sort + Pin | ✅ Done | 2026-04-15 |
| StoreKit paywall enforcement | ✅ Done | 2026-04-15 |
| Build verification | ✅ Done | 2026-04-15 |

---

## Phase 2 Complete — Summary

### Files Created
- `Nexus/Views/Components/BacklinksView.swift` — backlinks section
- `Nexus/Views/Home/FoldersView.swift` — folder management
- `Nexus/Views/Components/FolderPicker.swift` — move note to folder
- `Nexus/Views/Components/TagInputView.swift` — tag editor with suggestions
- `Nexus/Views/Components/NoteLimitBanner.swift` — paywall banner

### Files Modified
- `Nexus/Views/Editor/EditorView.swift` — backlinks, folder picker, pin, tags
- `Nexus/Views/Home/HomeView.swift` — sort, folder button, paywall check
- `Nexus/Views/Home/NoteRowView.swift` — pin badge, folder badge
- `Nexus/App/AppState.swift` — isShowingFolders, isShowingSubscription
- `Nexus/Models/Folder.swift` — already existed

---

## Files to Modify/Create

### Modify
- `Nexus/Views/Editor/EditorView.swift` — add backlinks section
- `Nexus/Views/Home/HomeView.swift` — sort + pin
- `Nexus/Views/Settings/SettingsView.swift` — folder management

### Create
- `Nexus/Views/Home/FoldersView.swift` — folder list
- `Nexus/Views/Home/TagInputView.swift` — tag editor
- `Nexus/Views/Components/BacklinksView.swift` — backlinks section
- `Nexus/Views/Components/NoteLimitBanner.swift` — paywall banner
