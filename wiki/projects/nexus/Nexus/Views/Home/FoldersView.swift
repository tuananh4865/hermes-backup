import SwiftUI
import SwiftData

struct FoldersView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var modelContext
    @State private var folders: [Folder] = []
    @State private var showingNewFolderSheet = false
    @State private var newFolderName = ""
    @State private var editingFolder: Folder?
    @State private var editFolderName = ""
    @State private var showingDeleteAlert = false
    @State private var folderToDelete: Folder?

    var body: some View {
        NavigationStack {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                if folders.isEmpty {
                    emptyState
                } else {
                    folderList
                }
            }
            .navigationTitle("Folders")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Done") {
                        dismiss()
                    }
                    .foregroundColor(Color(hex: "6366F1"))
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showingNewFolderSheet = true
                    } label: {
                        Image(systemName: "folder.badge.plus")
                            .foregroundColor(Color(hex: "6366F1"))
                    }
                }
            }
            .sheet(isPresented: $showingNewFolderSheet) {
                newFolderSheet
            }
            .sheet(item: $editingFolder) { folder in
                editFolderSheet(folder: folder)
            }
            .alert("Delete Folder?", isPresented: $showingDeleteAlert) {
                Button("Cancel", role: .cancel) { }
                Button("Delete", role: .destructive) {
                    if let folder = folderToDelete {
                        deleteFolder(folder)
                    }
                }
            } message: {
                Text("Notes in this folder will be moved to the root (no folder).")
            }
        }
        .onAppear {
            loadFolders()
        }
        .preferredColorScheme(.dark)
    }

    private var emptyState: some View {
        VStack(spacing: 16) {
            Image(systemName: "folder")
                .font(.system(size: 64))
                .foregroundColor(Color(hex: "6366F1").opacity(0.6))
            Text("No folders yet")
                .font(.title3.weight(.medium))
                .foregroundColor(.white)
            Text("Create folders to organize your notes")
                .font(.subheadline)
                .foregroundColor(Color(hex: "8E8E9A"))
                .multilineTextAlignment(.center)
            Button {
                showingNewFolderSheet = true
            } label: {
                Text("Create Folder")
                    .font(.subheadline.weight(.semibold))
                    .foregroundColor(.white)
                    .padding(.horizontal, 24)
                    .padding(.vertical, 12)
                    .background(Color(hex: "6366F1"))
                    .clipShape(Capsule())
            }
            .padding(.top, 8)
        }
        .padding(32)
    }

    private var folderList: some View {
        List {
            ForEach(folders) { folder in
                HStack(spacing: 12) {
                    Image(systemName: "folder.fill")
                        .foregroundColor(Color(hex: "6366F1"))
                        .font(.body)

                    Text(folder.name)
                        .font(.body)
                        .foregroundColor(.white)

                    Spacer()

                    Image(systemName: "chevron.right")
                        .font(.caption)
                        .foregroundColor(Color(hex: "8E8E9A"))
                }
                .padding(.vertical, 4)
                .contentShape(Rectangle())
                .listRowBackground(Color(hex: "1A1A24"))
                .onTapGesture {
                    editingFolder = folder
                    editFolderName = folder.name
                }
                .swipeActions(edge: .trailing, allowsFullSwipe: false) {
                    Button(role: .destructive) {
                        folderToDelete = folder
                        showingDeleteAlert = true
                    } label: {
                        Label("Delete", systemImage: "trash")
                    }
                }
            }
            .listRowSeparator(.hidden)
        }
        .listStyle(.plain)
        .scrollContentBackground(.hidden)
    }

    private var newFolderSheet: some View {
        NavigationStack {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                VStack(spacing: 24) {
                    TextField("Folder name", text: $newFolderName)
                        .textFieldStyle(.plain)
                        .font(.body)
                        .foregroundColor(.white)
                        .padding(16)
                        .background(Color(hex: "1A1A24"))
                        .clipShape(RoundedRectangle(cornerRadius: 12))

                    Spacer()
                }
                .padding(24)
            }
            .navigationTitle("New Folder")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Cancel") {
                        showingNewFolderSheet = false
                        newFolderName = ""
                    }
                    .foregroundColor(Color(hex: "8E8E9A"))
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Create") {
                        createFolder()
                    }
                    .foregroundColor(Color(hex: "6366F1"))
                    .disabled(newFolderName.trimmingCharacters(in: .whitespaces).isEmpty)
                }
            }
        }
        .presentationDetents([.height(200)])
        .preferredColorScheme(.dark)
    }

    private func editFolderSheet(folder: Folder) -> some View {
        NavigationStack {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                VStack(spacing: 24) {
                    TextField("Folder name", text: $editFolderName)
                        .textFieldStyle(.plain)
                        .font(.body)
                        .foregroundColor(.white)
                        .padding(16)
                        .background(Color(hex: "1A1A24"))
                        .clipShape(RoundedRectangle(cornerRadius: 12))

                    Spacer()
                }
                .padding(24)
            }
            .navigationTitle("Rename Folder")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Cancel") {
                        editingFolder = nil
                        editFolderName = ""
                    }
                    .foregroundColor(Color(hex: "8E8E9A"))
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Save") {
                        renameFolder(folder)
                    }
                    .foregroundColor(Color(hex: "6366F1"))
                    .disabled(editFolderName.trimmingCharacters(in: .whitespaces).isEmpty)
                }
            }
        }
        .presentationDetents([.height(200)])
        .preferredColorScheme(.dark)
    }

    private func createFolder() {
        let name = newFolderName.trimmingCharacters(in: .whitespaces)
        guard !name.isEmpty else { return }

        let folder = Folder(name: name)
        modelContext.insert(folder)
        try? modelContext.save()

        newFolderName = ""
        showingNewFolderSheet = false
        loadFolders()
    }

    private func renameFolder(_ folder: Folder) {
        let name = editFolderName.trimmingCharacters(in: .whitespaces)
        guard !name.isEmpty else { return }

        folder.name = name
        folder.modifiedAt = Date()
        try? modelContext.save()

        editingFolder = nil
        editFolderName = ""
        loadFolders()
    }

    private func loadFolders() {
        let descriptor = FetchDescriptor<Folder>(sortBy: [SortDescriptor(\.name)])
        folders = (try? modelContext.fetch(descriptor)) ?? []
    }

    private func deleteFolder(_ folder: Folder) {
        // Move notes in this folder to root
        let folderName = folder.name
        let descriptor = FetchDescriptor<Note>()
        if let allNotes = try? modelContext.fetch(descriptor) {
            for note in allNotes where note.folder == folderName {
                note.folder = nil
            }
        }

        modelContext.delete(folder)
        try? modelContext.save()

        folderToDelete = nil
    }
}

#Preview {
    FoldersView()
        .modelContainer(for: [Note.self, Folder.self], inMemory: true)
}
