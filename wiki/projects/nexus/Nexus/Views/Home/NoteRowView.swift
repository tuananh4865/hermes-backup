import SwiftUI

struct NoteRowView: View {
    let note: Note

    var wikiLinkCount: Int {
        WikiLinkExtractor.extract(from: note.content).count
    }

    var body: some View {
        HStack(spacing: 12) {
            VStack(alignment: .leading, spacing: 4) {
                Text(note.displayTitle)
                    .font(.headline)
                    .foregroundColor(.white)
                    .lineLimit(1)

                if !note.previewText.isEmpty {
                    Text(note.previewText)
                        .font(.caption)
                        .foregroundColor(Color(hex: "8E8E9A"))
                        .lineLimit(2)
                }

                HStack(spacing: 8) {
                    if note.isPinned {
                        Image(systemName: "pin.fill")
                            .font(.caption2)
                            .foregroundColor(Color(hex: "F59E0B"))
                    }

                    if let folder = note.folder {
                        HStack(spacing: 2) {
                            Image(systemName: "folder.fill")
                                .font(.caption2)
                            Text(folder)
                                .font(.caption2)
                        }
                        .foregroundColor(Color(hex: "6366F1"))
                    }

                    Text(note.modifiedAt.formatted(date: .abbreviated, time: .shortened))
                        .font(.caption2)
                        .foregroundColor(Color(hex: "8E8E9A"))

                    if wikiLinkCount > 0 {
                        HStack(spacing: 2) {
                            Image(systemName: "link")
                                .font(.caption2)
                            Text("\(wikiLinkCount)")
                                .font(.caption2)
                        }
                        .foregroundColor(Color(hex: "A78BFA"))
                    }
                }
            }

            Spacer()

            Image(systemName: "chevron.right")
                .font(.caption)
                .foregroundColor(Color(hex: "8E8E9A"))
        }
        .padding(.vertical, 8)
    }
}
