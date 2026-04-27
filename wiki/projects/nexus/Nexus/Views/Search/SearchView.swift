import SwiftUI
import SwiftData

struct SearchView: View {
    @Environment(\.dismiss) private var dismiss
    @Environment(\.modelContext) private var modelContext
    let notes: [Note]
    @State private var searchText = ""
    @State private var searchFilter: SearchFilter = .all
    @FocusState private var isSearchFocused: Bool

    enum SearchFilter: String, CaseIterable {
        case all = "All"
        case title = "Title"
        case content = "Content"
    }

    var filteredNotes: [Note] {
        if searchText.isEmpty {
            return notes
        }

        let query = searchText.lowercased()
        return notes.filter { note in
            switch searchFilter {
            case .all:
                return note.title.lowercased().contains(query) ||
                       note.content.lowercased().contains(query)
            case .title:
                return note.title.lowercased().contains(query)
            case .content:
                return note.content.lowercased().contains(query)
            }
        }
    }

    var body: some View {
        NavigationStack {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                VStack(spacing: 0) {
                    // Search bar
                    HStack(spacing: 12) {
                        Image(systemName: "magnifyingglass")
                            .foregroundColor(Color(hex: "8E8E9A"))

                        TextField("Search notes...", text: $searchText)
                            .foregroundColor(.white)
                            .focused($isSearchFocused)

                        if !searchText.isEmpty {
                            Button {
                                searchText = ""
                            } label: {
                                Image(systemName: "xmark.circle.fill")
                                    .foregroundColor(Color(hex: "8E8E9A"))
                            }
                        }
                    }
                    .padding(12)
                    .background(Color(hex: "1A1A24"))
                    .clipShape(RoundedRectangle(cornerRadius: 12))
                    .padding(.horizontal, 16)
                    .padding(.top, 16)

                    // Filters
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 8) {
                            ForEach(SearchFilter.allCases, id: \.self) { filter in
                                Button {
                                    searchFilter = filter
                                } label: {
                                    Text(filter.rawValue)
                                        .font(.subheadline)
                                        .foregroundColor(searchFilter == filter ? .white : Color(hex: "8E8E9A"))
                                        .padding(.horizontal, 16)
                                        .padding(.vertical, 8)
                                        .background(searchFilter == filter ? Color(hex: "6366F1") : Color(hex: "1A1A24"))
                                        .clipShape(Capsule())
                                }
                            }
                        }
                        .padding(.horizontal, 16)
                        .padding(.vertical, 12)
                    }

                    Divider()
                        .background(Color(hex: "252532"))

                    // Results
                    if filteredNotes.isEmpty {
                        Spacer()
                        VStack(spacing: 12) {
                            Image(systemName: "magnifyingglass")
                                .font(.system(size: 48))
                                .foregroundColor(Color(hex: "8E8E9A").opacity(0.5))
                            Text("No results found")
                                .font(.headline)
                                .foregroundColor(Color(hex: "8E8E9A"))
                        }
                        Spacer()
                    } else {
                        ScrollView {
                            LazyVStack(spacing: 0) {
                                ForEach(filteredNotes) { note in
                                    NoteRowView(note: note)
                                        .padding(.horizontal, 16)
                                        .padding(.vertical, 12)

                                    Divider()
                                        .background(Color(hex: "252532"))
                                }
                            }
                        }
                    }
                }
            }
            .navigationTitle("Search")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Cancel") {
                        dismiss()
                    }
                    .foregroundColor(Color(hex: "6366F1"))
                }
            }
        }
        .preferredColorScheme(.dark)
        .onAppear {
            isSearchFocused = true
        }
    }
}
