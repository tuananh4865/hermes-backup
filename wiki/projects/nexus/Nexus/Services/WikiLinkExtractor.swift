import Foundation

struct WikiLinkExtractor {
    /// Extract all [[wiki-links]] from content
    static func extract(from content: String) -> [String] {
        let pattern = #"\[\[([^\]]+)\]\]"#
        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
            return []
        }

        let range = NSRange(content.startIndex..., in: content)
        let matches = regex.matches(in: content, options: [], range: range)

        return matches.compactMap { match -> String? in
            guard let linkRange = Range(match.range(at: 1), in: content) else {
                return nil
            }
            return String(content[linkRange])
        }
    }

    /// Find all broken wiki-links (pointing to titles that don't exist in notes)
    static func findBrokenLinks(in content: String, existingTitles: Set<String>) -> [String] {
        let links = extract(from: content)
        return links.filter { !existingTitles.contains($0) }
    }

    /// Replace wiki-link text with display text (strips [[ ]])
    static func extractDisplayText(_ link: String) -> String {
        link.trimmingCharacters(in: .whitespaces)
    }
}
