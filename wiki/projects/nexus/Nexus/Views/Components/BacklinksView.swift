import SwiftUI
import SwiftData

struct BacklinksView: View {
    let currentNote: Note
    let onBacklinkTap: (Note) -> Void
    @Environment(\.modelContext) private var modelContext
    @State private var backlinks: [Note] = []
    @State private var isExpanded = true

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            // Header
            Button {
                withAnimation(.easeInOut(duration: 0.2)) {
                    isExpanded.toggle()
                }
            } label: {
                HStack {
                    Image(systemName: "arrow.left.arrow.right")
                        .font(.caption)
                        .foregroundColor(Color(hex: "A78BFA"))

                    Text("Linked to this note")
                        .font(.subheadline.weight(.semibold))
                        .foregroundColor(Color(hex: "A78BFA"))

                    Spacer()

                    Text("\(backlinks.count)")
                        .font(.caption.weight(.medium))
                        .foregroundColor(Color(hex: "8E8E9A"))
                        .padding(.horizontal, 8)
                        .padding(.vertical, 2)
                        .background(Color(hex: "252532"))
                        .clipShape(Capsule())

                    Image(systemName: isExpanded ? "chevron.up" : "chevron.down")
                        .font(.caption)
                        .foregroundColor(Color(hex: "8E8E9A"))
                }
                .padding(.horizontal, 16)
                .padding(.vertical, 12)
            }
            .buttonStyle(.plain)

            if isExpanded {
                if backlinks.isEmpty {
                    VStack(spacing: 8) {
                        Image(systemName: "link.badge.plus")
                            .font(.title2)
                            .foregroundColor(Color(hex: "8E8E9A").opacity(0.5))
                        Text("No notes link here yet")
                            .font(.caption)
                            .foregroundColor(Color(hex: "8E8E9A"))
                    }
                    .frame(maxWidth: .infinity)
                    .padding(.vertical, 24)
                } else {
                    VStack(spacing: 0) {
                        ForEach(backlinks) { note in
                            backlinkRow(note: note)

                            if note.id != backlinks.last?.id {
                                Divider()
                                    .background(Color(hex: "252532"))
                                    .padding(.leading, 16)
                            }
                        }
                    }
                }
            }
        }
        .background(Color(hex: "1A1A24"))
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .padding(.horizontal, 16)
        .onAppear {
            loadBacklinks()
        }
    }

    private func backlinkRow(note: Note) -> some View {
        HStack(spacing: 12) {
            Image(systemName: "doc.text")
                .font(.body)
                .foregroundColor(Color(hex: "6366F1"))
                .frame(width: 20)

            VStack(alignment: .leading, spacing: 2) {
                Text(note.displayTitle)
                    .font(.subheadline)
                    .foregroundColor(.white)
                    .lineLimit(1)

                if !note.previewText.isEmpty {
                    Text(note.previewText)
                        .font(.caption)
                        .foregroundColor(Color(hex: "8E8E9A"))
                        .lineLimit(1)
                }
            }

            Spacer()

            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundColor(Color(hex: "8E8E9A"))
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
        .contentShape(Rectangle())
        .onTapGesture {
            onBacklinkTap(note)
        }
    }

    private func loadBacklinks() {
        guard !currentNote.title.isEmpty else {
            backlinks = []
            return
        }

        let searchTitle = currentNote.title.lowercased()
        let pattern = #"\[\[([^\]]+)\]\]"#

        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
            backlinks = []
            return
        }

        let descriptor = FetchDescriptor<Note>()
        guard let allNotes = try? modelContext.fetch(descriptor) else {
            backlinks = []
            return
        }

        backlinks = allNotes.filter { note in
            guard note.id != currentNote.id else { return false }
            let content = note.content.lowercased()
            let range = NSRange(content.startIndex..., in: content)
            let matches = regex.matches(in: content, options: [], range: range)

            for match in matches {
                if let linkRange = Range(match.range(at: 1), in: content) {
                    let linkedTitle = String(content[linkRange]).lowercased()
                    if linkedTitle == searchTitle {
                        return true
                    }
                }
            }
            return false
        }
    }
}
