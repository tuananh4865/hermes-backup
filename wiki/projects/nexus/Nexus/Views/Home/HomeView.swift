import SwiftUI
import SwiftData

struct HomeView: View {
    @Environment(\.modelContext) private var modelContext
    @Query private var notes: [Note]

    var sortedNotes: [Note] {
        let pinned = notes.filter { $0.isPinned }
        let unpinned = notes.filter { !$0.isPinned }

        let sortedUnpinned: [Note]
        switch selectedSort {
        case .modified:
            sortedUnpinned = unpinned.sorted { $0.modifiedAt > $1.modifiedAt }
        case .title:
            sortedUnpinned = unpinned.sorted { $0.title.lowercased() < $1.title.lowercased() }
        case .created:
            sortedUnpinned = unpinned.sorted { $0.createdAt > $1.createdAt }
        }

        return pinned + sortedUnpinned
    }
    @State private var appState = AppState()
    @State private var showingEditor = false
    @State private var selectedNote: Note?
    @State private var showingGraph = false
    @State private var selectedSort: SortOption = .modified
    @State private var subscriptionManager = SubscriptionManager.shared

    enum SortOption: String, CaseIterable {
        case modified = "Last Modified"
        case title = "Title"
        case created = "Created"
    }

    var body: some View {
        NavigationStack {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                if notes.isEmpty {
                    emptyState
                } else {
                    notesList
                }

                // FAB
                VStack {
                    Spacer()
                    HStack {
                        Spacer()
                        Button {
                            createNewNote()
                        } label: {
                            Image(systemName: "plus")
                                .font(.title2.weight(.semibold))
                                .foregroundColor(.white)
                                .frame(width: 56, height: 56)
                                .background(Color(hex: "6366F1"))
                                .clipShape(Circle())
                                .shadow(color: Color(hex: "6366F1").opacity(0.4), radius: 8, x: 0, y: 4)
                        }
                        .padding(.trailing, 24)
                        .padding(.bottom, 24)
                    }
                }

                // Graph overlay
                if showingGraph {
                    GraphView(notes: notes, isPresented: $showingGraph)
                        .transition(.opacity)
                        .zIndex(100)
                }
            }
            .navigationTitle("Nexus")
            .navigationBarTitleDisplayMode(.large)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button {
                        appState.isShowingFolders = true
                    } label: {
                        Image(systemName: "folder")
                            .foregroundColor(Color(hex: "6366F1"))
                    }
                }
                ToolbarItem(placement: .topBarLeading) {
                    Button {
                        withAnimation {
                            showingGraph = true
                        }
                    } label: {
                        Image(systemName: "circle.hexagongrid.circle")
                            .foregroundColor(Color(hex: "6366F1"))
                    }
                }
                ToolbarItem(placement: .topBarTrailing) {
                    Menu {
                        ForEach(SortOption.allCases, id: \.self) { option in
                            Button {
                                selectedSort = option
                            } label: {
                                HStack {
                                    Text(option.rawValue)
                                    if selectedSort == option {
                                        Image(systemName: "checkmark")
                                    }
                                }
                            }
                        }
                    } label: {
                        Image(systemName: "arrow.up.arrow.down")
                            .foregroundColor(Color(hex: "8E8E9A"))
                    }
                }
                ToolbarItem(placement: .topBarTrailing) {
                    HStack(spacing: 16) {
                        Button {
                            appState.isShowingSearch = true
                        } label: {
                            Image(systemName: "magnifyingglass")
                                .foregroundColor(Color(hex: "8E8E9A"))
                        }
                        Button {
                            appState.isShowingSettings = true
                        } label: {
                            Image(systemName: "gearshape")
                                .foregroundColor(Color(hex: "8E8E9A"))
                        }
                    }
                }
            }
            .onAppear {
                loadSampleDataIfNeeded(context: modelContext)
                if !notes.isEmpty {
                    withAnimation(.easeIn(duration: 0.3)) {
                        showingGraph = true
                    }
                }
            }
            .sheet(isPresented: $showingEditor) {
                if let note = selectedNote {
                    EditorView(note: note)
                }
            }
            .sheet(isPresented: $appState.isShowingSearch) {
                SearchView(notes: notes)
            }
            .sheet(isPresented: $appState.isShowingSettings) {
                SettingsView()
            }
            .sheet(isPresented: $appState.isShowingFolders) {
                FoldersView()
            }
            .sheet(isPresented: $appState.isShowingSubscription) {
                SubscriptionView()
            }
        }
        .preferredColorScheme(.dark)
    }

    private var emptyState: some View {
        VStack(spacing: 16) {
            Image(systemName: "link.circle")
                .font(.system(size: 64))
                .foregroundColor(Color(hex: "6366F1").opacity(0.6))
            Text("Start your first note")
                .font(.title3.weight(.medium))
                .foregroundColor(.white)
            Text("Tap + to create a note with [[wiki-links]]")
                .font(.subheadline)
                .foregroundColor(Color(hex: "8E8E9A"))
                .multilineTextAlignment(.center)
        }
        .padding(32)
    }

    private var notesList: some View {
        ScrollView {
            LazyVStack(spacing: 0) {
                    ForEach(sortedNotes) { note in
                    NoteRowView(note: note)
                        .contentShape(Rectangle())
                        .onTapGesture {
                            selectedNote = note
                            showingEditor = true
                        }
                        .padding(.horizontal, 16)
                        .padding(.vertical, 12)

                    Divider()
                        .background(Color(hex: "252532"))
                }
            }
        }
    }

    private func createNewNote() {
        if !subscriptionManager.isPro && notes.count >= 50 {
            appState.isShowingSubscription = true
            return
        }

        let newNote = Note(title: "", content: "")
        modelContext.insert(newNote)
        selectedNote = newNote
        showingEditor = true
    }
}

#Preview {
    HomeView()
        .modelContainer(for: Note.self, inMemory: true)
}
