import Foundation
import SwiftData

/// Seeds sample notes for graph testing on first launch
@MainActor
func loadSampleDataIfNeeded(context: ModelContext) {
    let descriptor = FetchDescriptor<Note>()
    let existingCount = (try? context.fetchCount(descriptor)) ?? 0
    
    guard existingCount == 0 else { return }
    
    let samples = createSampleNotes()
    for note in samples {
        context.insert(note)
    }
    try? context.save()
}

private func createSampleNotes() -> [Note] {
    let now = Date()
    
    // Note 1: Welcome
    let welcome = Note(
        title: "Welcome to Nexus",
        content: """
        # Welcome to Nexus
        
        This is a sample note to demonstrate [[wiki-links]] and the [[Graph View]].
        
        Try tapping on any [[wiki-link]] to navigate between notes.
        
        ## Getting Started
        - Create notes with the **+** button
        - Link notes using [[wiki-links]]
        - View your knowledge graph in [[Graph View]]
        
        Check out [[Markdown Features]] for formatting tips.
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 2: Graph View
    let graphView = Note(
        title: "Graph View",
        content: """
        # Graph View
        
        The [[Graph View]] shows all your notes as interconnected nodes.
        
        Each [[wiki-link]] becomes an edge connecting two notes.
        
        Larger nodes have more connections — they're your most connected ideas.
        
        See also: [[Welcome to Nexus]], [[Knowledge Management]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 3: Knowledge Management
    let knowledge = Note(
        title: "Knowledge Management",
        content: """
        # Knowledge Management
        
        The art of organizing connected information.
        
        Key concepts:
        - [[Bidirectional Links]] — connections that work both ways
        - [[Graph View]] — visual representation of your knowledge
        - [[Zettelkasten]] — a method for building knowledge
        
        Related: [[Welcome to Nexus]], [[Note Taking]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 4: Bidirectional Links
    let bidirectional = Note(
        title: "Bidirectional Links",
        content: """
        # Bidirectional Links
        
        Unlike regular links, bidirectional links work both directions.
        
        If Note A links to Note B, Note B automatically shows Note A as a [[Backlinks|backlink]].
        
        This creates a web of connected knowledge — see [[Graph View]] for visualization.
        
        Core concept: [[Knowledge Management]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 5: Note Taking
    let noteTaking = Note(
        title: "Note Taking",
        content: """
        # Note Taking
        
        Effective note taking combines:
        - Quick capture of ideas
        - Easy retrieval later
        - Connections to existing knowledge
        
        Features in Nexus:
        - [[Markdown Features]] for rich formatting
        - [[Wiki Links]] for connecting ideas
        - [[Graph View]] for visualization
        
        Related: [[Knowledge Management]], [[Zettelkasten]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 6: Markdown Features
    let markdown = Note(
        title: "Markdown Features",
        content: """
        # Markdown Features
        
        Nexus supports standard Markdown plus special [[Wiki Links]]:
        
        ## Formatting
        - **Bold** and *italic*
        - `code` and code blocks
        - Lists and checkboxes
        
        ## Wiki Links
        Use [[wiki-links]] to connect to other notes.
        
        Example: [[Welcome to Nexus]] links to the welcome note.
        
        Learn more: [[Note Taking]], [[Bidirectional Links]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 7: Zettelkasten
    let zettelkasten = Note(
        title: "Zettelkasten",
        content: """
        # Zettelkasten
        
        A knowledge management method developed by Niklas Luhmann.
        
        Key principles:
        - Atomic notes (one idea per note)
        - Unique identifiers for each note
        - Extensive [[Bidirectional Links]]
        - Emergent structure through connections
        
        Nexus is inspired by Zettelkasten — see [[Knowledge Management]]
        
        Related: [[Note Taking]], [[Graph View]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 8: Backlinks
    let backlinks = Note(
        title: "Backlinks",
        content: """
        # Backlinks
        
        Backlinks show which notes link TO the current note.
        
        When you create a [[Wiki Links|wiki-link]] from Note A to Note B,
        Note B gains a backlink pointing back to Note A.
        
        This is the foundation of [[Bidirectional Links]]
        
        See: [[Graph View]], [[Knowledge Management]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 9: Wiki Links
    let wikiLinks = Note(
        title: "Wiki Links",
        content: """
        # Wiki Links
        
        Wiki links connect notes using [[wiki-link]] syntax.
        
        Type `[[` followed by a note title to create a link.
        
        Example: [[Welcome to Nexus]] creates a link to the welcome note.
        
        When a linked note doesn't exist, tapping the link creates it.
        
        Core feature: [[Bidirectional Links]], [[Backlinks]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 10: Search
    let search = Note(
        title: "Search",
        content: """
        # Search
        
        Find any note instantly with Search.
        
        Nexus supports:
        - Full-text search across all notes
        - Filter by [[Note Taking|title]] or content
        - Semantic search (Pro feature)
        
        Quick tip: Use [[Wiki Links]] to connect related notes for easier discovery.
        
        Related: [[Graph View]], [[Knowledge Management]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 11: AI Integration
    let aiIntegration = Note(
        title: "AI Integration",
        content: """
        # AI Integration
        
        Nexus Pro includes powerful AI features:
        
        ## Semantic Search
        Find notes by meaning, not just keywords.
        Related: [[Search]]
        
        ## Auto-linking Suggestions
        AI suggests relevant connections as you write.
        Related: [[Wiki Links]], [[Knowledge Management]]
        
        ## Smart Tags
        AI automatically tags your notes.
        Related: [[Note Taking]], [[Zettelkasten]]
        
        See also: [[Welcome to Nexus]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 12: Mobile Sync
    let mobileSync = Note(
        title: "Mobile Sync",
        content: """
        # Mobile Sync
        
        Access your notes anywhere with iCloud sync.
        
        ## Features
        - Automatic sync across all devices
        - Offline-first design
        - Conflict resolution
        
        Related: [[Knowledge Management]], [[Note Taking]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 13: Quick Capture
    let quickCapture = Note(
        title: "Quick Capture",
        content: """
        # Quick Capture
        
        Capture ideas instantly before they slip away.
        
        ## Tips
        - Use the **+** button on home screen
        - Start with a title, add content later
        - Link to existing notes using [[Wiki Links]]
        
        Related: [[Note Taking]], [[Welcome to Nexus]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 14: Version History
    let versionHistory = Note(
        title: "Version History",
        content: """
        # Version History
        
        Never lose a previous version of your notes.
        
        ## Features
        - Automatic versioning
        - Restore previous versions
        - Compare changes
        
        Related: [[Note Taking]], [[Markdown Features]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 15: Obsidian Tips
    let obsidianTips = Note(
        title: "Obsidian Tips",
        content: """
        # Obsidian Tips
        
        Coming from Obsidian? Here are key differences:
        
        ## Similarities
        - [[Wiki Links]] work the same way
        - [[Graph View]] similar visualization
        - Markdown-based notes
        
        ## Differences
        - Native iOS app — better performance
        - [[AI Integration]] built-in
        - [[Mobile Sync]] via iCloud
        
        See: [[Welcome to Nexus]], [[Graph View]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 16: Daily Notes
    let dailyNotes = Note(
        title: "Daily Notes",
        content: """
        # Daily Notes
        
        Keep a daily journal alongside your main notes.
        
        ## Benefits
        - Capture daily thoughts
        - Link daily entries to permanent notes
        - Track progress over time
        
        Related: [[Note Taking]], [[Quick Capture]], [[Knowledge Management]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 17: Tags and Tags
    let tags = Note(
        title: "Tags",
        content: """
        # Tags
        
        Organize notes with tags.
        
        ## Usage
        - Add tags to any note
        - Filter by tag in search
        - Tag-based [[Graph View]] coming soon
        
        Related: [[Note Taking]], [[Search]], [[Knowledge Management]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 18: Import Export
    let importExport = Note(
        title: "Import Export",
        content: """
        # Import Export
        
        Bring your existing notes into Nexus.
        
        ## Import
        - Obsidian vault import
        - Markdown file import
        - Plain text import
        
        ## Export
        - Full vault export
        - Individual note export
        - [[Markdown Features]] compatible output
        
        Related: [[Obsidian Tips]], [[Note Taking]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 19: Keyboard Shortcuts
    let keyboardShortcuts = Note(
        title: "Keyboard Shortcuts",
        content: """
        # Keyboard Shortcuts
        
        Work faster with keyboard shortcuts.
        
        ## Editor
        - `Cmd+B` for **bold**
        - `Cmd+I` for *italic*
        - `Cmd+K` for [[Wiki Links]]
        
        Related: [[Markdown Features]], [[Note Taking]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 20: Pro Features
    let proFeatures = Note(
        title: "Pro Features",
        content: """
        # Pro Features
        
        Unlock Nexus Pro for:
        
        ## Unlimited
        - Unlimited notes
        - Unlimited [[Graph View]]
        - [[AI Integration]]
        
        ## Advanced
        - [[Mobile Sync]]
        - [[Version History]]
        - Priority support
        
        See: [[Welcome to Nexus]], [[Subscription]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    // Note 21: Subscription
    let subscription = Note(
        title: "Subscription",
        content: """
        # Subscription
        
        Nexus Free vs Pro:
        
        ## Free Tier
        - 50 notes max
        - Basic [[Graph View]]
        - [[Search]] by keyword
        
        ## Pro ($4.99/mo or $29.99/yr)
        - Unlimited notes
        - [[AI Integration]]
        - [[Mobile Sync]]
        - [[Pro Features]]
        
        Related: [[Welcome to Nexus]], [[Graph View]]
        """,
        createdAt: now,
        modifiedAt: now
    )
    
    return [
        welcome, graphView, knowledge, bidirectional,
        noteTaking, markdown, zettelkasten, backlinks,
        wikiLinks, search, aiIntegration, mobileSync,
        quickCapture, versionHistory, obsidianTips,
        dailyNotes, tags, importExport, keyboardShortcuts,
        proFeatures, subscription
    ]
}
