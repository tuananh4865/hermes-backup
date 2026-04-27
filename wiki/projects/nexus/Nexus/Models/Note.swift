import Foundation
import SwiftData

@Model
final class Note {
    var id: UUID
    var title: String
    var content: String
    var createdAt: Date
    var modifiedAt: Date
    var folder: String?
    var tags: [String]
    var isPinned: Bool

    init(
        id: UUID = UUID(),
        title: String = "",
        content: String = "",
        createdAt: Date = Date(),
        modifiedAt: Date = Date(),
        folder: String? = nil,
        tags: [String] = [],
        isPinned: Bool = false
    ) {
        self.id = id
        self.title = title
        self.content = content
        self.createdAt = createdAt
        self.modifiedAt = modifiedAt
        self.folder = folder
        self.tags = tags
        self.isPinned = isPinned
    }

    var displayTitle: String {
        title.isEmpty ? "Untitled" : title
    }

    var previewText: String {
        let lines = content.components(separatedBy: .newlines)
        let preview = lines.prefix(2).joined(separator: " ")
        if preview.count > 100 {
            return String(preview.prefix(100)) + "..."
        }
        return preview
    }
}
