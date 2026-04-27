import SwiftUI
import SwiftData

@main
struct NexusApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: Note.self)
    }
}

struct ContentView: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \Note.modifiedAt, order: .reverse) private var notes: [Note]
    @State private var showGraph = false

    var body: some View {
        ZStack {
            HomeViewContent(showGraph: $showGraph)
                .opacity(showGraph ? 0 : 1)

            GraphView(notes: notes, isPresented: $showGraph)
                .opacity(showGraph ? 1 : 0)
        }
        .onAppear {
            loadSampleDataIfNeeded(context: modelContext)
            DispatchQueue.main.asyncAfter(deadline: .now() + 0.8) {
                showGraph = true
            }
        }
    }
}

struct HomeViewContent: View {
    @Environment(\.modelContext) private var modelContext
    @Query(sort: \Note.modifiedAt, order: .reverse) private var notes: [Note]
    @State private var appState = AppState()
    @State private var showingEditor = false
    @State private var selectedNote: Note?
    @Binding var showGraph: Bool

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
            }
            .navigationTitle("Nexus")
            .navigationBarTitleDisplayMode(.large)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarLeading) {
                    Button {
                        showGraph = true
                    } label: {
                        Image(systemName: "circle.hexagongrid.circle")
                            .foregroundColor(Color(hex: "6366F1"))
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
                ForEach(notes) { note in
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
        let newNote = Note(title: "", content: "")
        modelContext.insert(newNote)
        selectedNote = newNote
        showingEditor = true
    }
}
