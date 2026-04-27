import SwiftUI
import SwiftData

struct EditorView: View {
    @Environment(\.modelContext) private var modelContext
    @Environment(\.dismiss) private var dismiss
    @Bindable var note: Note
    @State private var isPreviewMode = false
    @FocusState private var isTitleFocused: Bool
    @State private var navigationPath = NavigationPath()
    @State private var showingFolderPicker = false

    var body: some View {
        NavigationStack(path: $navigationPath) {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                VStack(spacing: 0) {
                    // Title
                    TextField("Untitled", text: $note.title)
                        .font(.title.weight(.bold))
                        .foregroundColor(.white)
                        .padding(.horizontal, 16)
                        .padding(.top, 16)
                        .focused($isTitleFocused)

                    // Tags
                    TagInputView(tags: $note.tags)

                    Divider()
                        .background(Color(hex: "252532"))
                        .padding(.top, 8)

                    ScrollView {
                        VStack(spacing: 0) {
                            // Content
                            if isPreviewMode {
                                TappableMarkdownView(
                                    content: note.content,
                                    onWikiLinkTap: handleWikiLinkTap
                                )
                                .padding(16)
                            } else {
                                TextEditor(text: $note.content)
                                    .font(.body)
                                    .foregroundColor(.white)
                                    .scrollContentBackground(.hidden)
                                    .background(Color(hex: "0A0A0F"))
                                    .padding(16)
                                    .focused($isTitleFocused)
                            }

                            // Backlinks section
                            BacklinksView(currentNote: note, onBacklinkTap: handleBacklinkTap)
                                .padding(.top, 16)
                                .padding(.bottom, 100) // space for toolbar
                        }
                    }
                }

                // Toolbar
                VStack {
                    Spacer()
                    editorToolbar
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Done") {
                        note.modifiedAt = Date()
                        dismiss()
                    }
                    .foregroundColor(Color(hex: "6366F1"))
                }

                ToolbarItem(placement: .topBarTrailing) {
                    HStack(spacing: 16) {
                        Button {
                            isPreviewMode.toggle()
                        } label: {
                            Image(systemName: isPreviewMode ? "pencil" : "eye")
                                .foregroundColor(Color(hex: "8E8E9A"))
                        }

                        Menu {
                            Button {
                                showingFolderPicker = true
                            } label: {
                                Label(note.folder ?? "Move to Folder", systemImage: "folder")
                            }

                            Divider()

                            Button {
                                note.isPinned.toggle()
                                note.modifiedAt = Date()
                            } label: {
                                Label(note.isPinned ? "Unpin" : "Pin to Top", systemImage: note.isPinned ? "pin.slash" : "pin")
                            }

                            Divider()

                            Button(role: .destructive) {
                                deleteNote()
                            } label: {
                                Label("Delete", systemImage: "trash")
                            }
                        } label: {
                            Image(systemName: "ellipsis.circle")
                                .foregroundColor(Color(hex: "8E8E9A"))
                        }
                    }
                }
            }
            .navigationDestination(for: Note.self) { linkedNote in
                EditorView(note: linkedNote)
            }
        }
        .preferredColorScheme(.dark)
        .onAppear {
            isTitleFocused = note.title.isEmpty
        }
        .sheet(isPresented: $showingFolderPicker) {
            FolderPicker(selectedFolder: Binding(
                get: { note.folder },
                set: { note.folder = $0; note.modifiedAt = Date() }
            ))
        }
    }

    private func handleWikiLinkTap(noteTitle: String) {
        // Find existing note by title
        let descriptor = FetchDescriptor<Note>(
            predicate: #Predicate { $0.title == noteTitle }
        )

        if let existingNotes = try? modelContext.fetch(descriptor),
           let existingNote = existingNotes.first {
            // Navigate to existing note
            navigationPath.append(existingNote)
        } else {
            // Create new note with this title
            let newNote = Note(
                title: noteTitle,
                content: "",
                createdAt: Date(),
                modifiedAt: Date()
            )
            modelContext.insert(newNote)
            try? modelContext.save()
            navigationPath.append(newNote)
        }
    }

    private func handleBacklinkTap(note: Note) {
        navigationPath.append(note)
    }

    private var editorToolbar: some View {
        HStack(spacing: 24) {
            toolbarButton(icon: "bold", action: insertBold)
            toolbarButton(icon: "italic", action: insertItalic)
            toolbarButton(icon: "link", action: insertLink)
            toolbarButton(icon: "chevron.left.forwardslash.chevron.right", action: insertWikiLink)
            toolbarButton(icon: "checkmark.square", action: insertCheckbox)
            toolbarButton(icon: "chevron.left.slash.chevron.right", action: insertCode)
        }
        .padding(.horizontal, 24)
        .padding(.vertical, 12)
        .background(Color(hex: "1A1A24"))
        .clipShape(RoundedRectangle(cornerRadius: 16))
        .padding(.horizontal, 16)
        .padding(.bottom, 16)
    }

    private func toolbarButton(icon: String, action: @escaping () -> Void) -> some View {
        Button(action: action) {
            Image(systemName: icon)
                .font(.body)
                .foregroundColor(Color(hex: "8E8E9A"))
                .frame(width: 32, height: 32)
        }
    }

    private func insertBold() {
        note.content += "**bold**"
    }

    private func insertItalic() {
        note.content += "*italic*"
    }

    private func insertLink() {
        note.content += "[text](url)"
    }

    private func insertWikiLink() {
        note.content += "[[note-name]]"
    }

    private func insertCheckbox() {
        note.content += "\n- [ ] task"
    }

    private func insertCode() {
        note.content += "`code`"
    }

    private func deleteNote() {
        modelContext.delete(note)
        dismiss()
    }
}
