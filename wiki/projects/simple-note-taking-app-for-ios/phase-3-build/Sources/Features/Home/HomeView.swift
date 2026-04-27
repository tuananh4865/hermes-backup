import SwiftUI
import SwiftData

// MARK: - Models

@Model
final class Note {
    var id: UUID
    var title: String
    var content: String
    var folder: String
    var tags: [String]
    var createdAt: Date
    var updatedAt: Date

    init(title: String = "", content: String = "", folder: String = "Inbox", tags: [String] = []) {
        self.id = UUID()
        self.title = title
        self.content = content
        self.folder = folder
        self.tags = tags
        self.createdAt = Date()
        self.updatedAt = Date()
    }
}

// MARK: - ViewModels

@MainActor
final class NotesViewModel: ObservableObject {
    @Published var notes: [Note] = []
    @Published var searchText: String = ""
    @Published var selectedFolder: String = "Inbox"
    @Published var selectedTags: Set<String> = []
    @Published var showingNewNote: Bool = false
    @Published var selectedNote: Note?

    let folders = ["Inbox", "Work", "Personal", "Archive"]
    let allTags = ["important", "quick", "follow-up", "idea", "urgent"]

    var filteredNotes: [Note] {
        notes.filter { note in
            let matchesFolder = selectedFolder == "All" || note.folder == selectedFolder
            let matchesTags = selectedTags.isEmpty || !selectedTags.isDisjoint(with: Set(note.tags))
            let matchesSearch = searchText.isEmpty ||
                note.title.localizedCaseInsensitiveContains(searchText) ||
                note.content.localizedCaseInsensitiveContains(searchText)
            return matchesFolder && matchesTags && matchesSearch
        }
    }

    func addNote(title: String, content: String, folder: String, tags: [String]) {
        let note = Note(title: title, content: content, folder: folder, tags: tags)
        notes.append(note)
    }

    func deleteNote(_ note: Note) {
        notes.removeAll { $0.id == note.id }
    }
}

// MARK: - Views

struct ContentView: View {
    var body: some View {
        NavigationStack {
            SidebarView()
                .navigationSplitViewStyle(.balanced)
        }
    }
}

struct SidebarView: View {
    @StateObject private var viewModel = NotesViewModel()
    @State private var selectedSection: String? = "Inbox"

    var body: some View {
        List(selection: $selectedSection) {
            Section("Folders") {
                ForEach(viewModel.folders, id: \.self) { folder in
                    NavigationLink(value: folder) {
                        Label(folder, systemImage: folderIcon(folder))
                    }
                }
            }

            Section("Tags") {
                ForEach(viewModel.allTags, id: \.self) { tag in
                    Label(tag, systemImage: "tag")
                        .foregroundStyle(.secondary)
                }
            }
        }
        .navigationDestination(for: String.self) { folder in
            NotesListView(viewModel: viewModel, folder: folder)
        }
        .navigationTitle("Notes")
        .toolbar {
            ToolbarItem(placement: .primaryAction) {
                Button {
                    viewModel.showingNewNote = true
                } label: {
                    Image(systemName: "square.and.pencil")
                }
            }
        }
        .sheet(isPresented: $viewModel.showingNewNote) {
            NoteEditorView(viewModel: viewModel, note: nil)
        }
    }

    private func folderIcon(_ folder: String) -> String {
        switch folder {
        case "Inbox": return "tray"
        case "Work": return "briefcase"
        case "Personal": return "person"
        case "Archive": return "archivebox"
        default: return "folder"
        }
    }
}

struct NotesListView: View {
    @ObservedObject var viewModel: NotesViewModel
    let folder: String

    var body: some View {
        Group {
            if viewModel.filteredNotes.isEmpty {
                ContentUnavailableView {
                    Label("No Notes", systemImage: "note.text")
                } description: {
                    Text("Tap + to create your first note")
                } actions: {
                    Button("New Note") {
                        viewModel.showingNewNote = true
                    }
                    .buttonStyle(.borderedProminent)
                }
            } else {
                List {
                    ForEach(viewModel.filteredNotes) { note in
                        NavigationLink {
                            NoteEditorView(viewModel: viewModel, note: note)
                        } label: {
                            NoteRowView(note: note)
                        }
                    }
                    .onDelete { indexSet in
                        for index in indexSet {
                            viewModel.deleteNote(viewModel.filteredNotes[index])
                        }
                    }
                }
                .searchable(text: $viewModel.searchText, prompt: "Search notes")
            }
        }
        .navigationTitle(folder)
    }
}

struct NoteRowView: View {
    let note: Note

    var body: some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(note.title.isEmpty ? "Untitled" : note.title)
                .font(.headline)
                .lineLimit(1)

            if !note.content.isEmpty {
                Text(note.content)
                    .font(.subheadline)
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }

            HStack {
                if !note.tags.isEmpty {
                    ForEach(note.tags.prefix(3), id: \.self) { tag in
                        Text(tag)
                            .font(.caption2)
                            .padding(.horizontal, 6)
                            .padding(.vertical, 2)
                            .background(.blue.opacity(0.1))
                            .foregroundStyle(.blue)
                            .clipShape(Capsule())
                    }
                }

                Spacer()

                Text(note.updatedAt, style: .relative)
                    .font(.caption)
                    .foregroundStyle(.tertiary)
            }
        }
        .padding(.vertical, 4)
    }
}

struct NoteEditorView: View {
    @ObservedObject var viewModel: NotesViewModel
    let note: Note?
    @Environment(\.dismiss) private var dismiss

    @State private var title: String = ""
    @State private var content: String = ""
    @State private var folder: String = "Inbox"
    @State private var selectedTags: Set<String> = []

    var body: some View {
        NavigationStack {
            Form {
                Section {
                    TextField("Title", text: $title)
                        .font(.title2.bold())
                }

                Section("Content") {
                    TextEditor(text: $content)
                        .frame(minHeight: 200)
                }

                Section("Folder") {
                    Picker("Folder", selection: $folder) {
                        ForEach(viewModel.folders, id: \.self) { f in
                            Text(f).tag(f)
                        }
                    }
                    .pickerStyle(.menu)
                }

                Section("Tags") {
                    ForEach(viewModel.allTags, id: \.self) { tag in
                        Toggle(tag, isOn: Binding(
                            get: { selectedTags.contains(tag) },
                            set: { isOn in
                                if isOn { selectedTags.insert(tag) }
                                else { selectedTags.remove(tag) }
                            }
                        ))
                    }
                }
            }
            .navigationTitle(note == nil ? "New Note" : "Edit Note")
            .navigationBarTitleDisplayMode(.inline)
            .toolbar {
                ToolbarItem(placement: .cancellationAction) {
                    Button("Cancel") { dismiss() }
                }
                ToolbarItem(placement: .confirmationAction) {
                    Button("Save") {
                        if let existing = note {
                            existing.title = title
                            existing.content = content
                            existing.folder = folder
                            existing.tags = Array(selectedTags)
                            existing.updatedAt = Date()
                        } else {
                            viewModel.addNote(title: title, content: content, folder: folder, tags: Array(selectedTags))
                        }
                        dismiss()
                    }
                    .fontWeight(.semibold)
                }
            }
            .onAppear {
                if let note = note {
                    title = note.title
                    content = note.content
                    folder = note.folder
                    selectedTags = Set(note.tags)
                }
            }
        }
    }
}

#Preview {
    ContentView()
}
