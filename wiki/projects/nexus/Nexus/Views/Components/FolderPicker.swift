import SwiftUI
import SwiftData

struct FolderPicker: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var modelContext
    @Binding var selectedFolder: String?
    @Query(sort: \Folder.name) private var folders: [Folder]
    @State private var showingNewFolder = false
    @State private var newFolderName = ""

    var body: some View {
        NavigationStack {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                List {
                    // Root (no folder) option
                    folderRow(name: nil, isSelected: selectedFolder == nil)

                    // Folders
                    ForEach(folders) { folder in
                        folderRow(name: folder.name, isSelected: selectedFolder == folder.name)
                    }
                    .listRowBackground(Color(hex: "1A1A24"))
                    .listRowSeparator(.hidden)
                }
                .listStyle(.plain)
                .scrollContentBackground(.hidden)
            }
            .navigationTitle("Move to Folder")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button("Cancel") {
                        dismiss()
                    }
                    .foregroundColor(Color(hex: "8E8E9A"))
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        showingNewFolder = true
                    } label: {
                        Image(systemName: "folder.badge.plus")
                            .foregroundColor(Color(hex: "6366F1"))
                    }
                }
            }
            .alert("New Folder", isPresented: $showingNewFolder) {
                TextField("Folder name", text: $newFolderName)
                Button("Cancel", role: .cancel) {
                    newFolderName = ""
                }
                Button("Create") {
                    createAndSelect()
                }
            }
        }
        .presentationDetents([.medium])
        .preferredColorScheme(.dark)
    }

    private func folderRow(name: String?, isSelected: Bool) -> some View {
        HStack(spacing: 12) {
            Image(systemName: name == nil ? "tray" : "folder.fill")
                .foregroundColor(Color(hex: "6366F1"))
                .font(.body)

            Text(name ?? "Root (No Folder)")
                .font(.body)
                .foregroundColor(.white)

            Spacer()

            if isSelected {
                Image(systemName: "checkmark")
                    .foregroundColor(Color(hex: "6366F1"))
                    .font(.body.weight(.semibold))
            }
        }
        .padding(.vertical, 4)
        .contentShape(Rectangle())
        .onTapGesture {
            selectedFolder = name
            dismiss()
        }
        .listRowBackground(Color(hex: "1A1A24"))
    }

    private func createAndSelect() {
        let name = newFolderName.trimmingCharacters(in: .whitespaces)
        guard !name.isEmpty else { return }

        let folder = Folder(name: name)
        modelContext.insert(folder)
        try? modelContext.save()

        selectedFolder = name
        newFolderName = ""
        dismiss()
    }
}

#Preview {
    FolderPicker(selectedFolder: .constant(nil))
        .modelContainer(for: [Note.self, Folder.self], inMemory: true)
}
