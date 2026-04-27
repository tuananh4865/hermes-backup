import SwiftUI

struct MarkdownPreviewView: View {
    let content: String

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 12) {
                ForEach(parseLines()) { line in
                    renderLine(line)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    private func parseLines() -> [ParsedLine] {
        content.components(separatedBy: .newlines).enumerated().map { index, line in
            ParsedLine(id: index, text: line, style: detectStyle(line))
        }
    }

    private func detectStyle(_ line: String) -> LineStyle {
        let trimmed = line.trimmingCharacters(in: .whitespaces)
        if trimmed.hasPrefix("### ") {
            return .h3
        } else if trimmed.hasPrefix("## ") {
            return .h2
        } else if trimmed.hasPrefix("# ") {
            return .h1
        } else if trimmed.hasPrefix("- [ ] ") {
            return .checkbox(false)
        } else if trimmed.hasPrefix("- [x] ") || trimmed.hasPrefix("- [X] ") {
            return .checkbox(true)
        } else if trimmed.hasPrefix("- ") || trimmed.hasPrefix("* ") {
            return .bullet
        } else if trimmed.first?.isNumber == true && trimmed.dropFirst().hasPrefix(". ") {
            return .numbered
        } else if trimmed.hasPrefix("> ") {
            return .blockquote
        } else if trimmed.hasPrefix("```") {
            return .codeBlock
        } else if trimmed.hasPrefix("---") || trimmed.hasPrefix("***") {
            return .horizontalRule
        }
        return .body
    }

    @ViewBuilder
    private func renderLine(_ line: ParsedLine) -> some View {
        switch line.style {
        case .h1:
            Text(String(line.text.dropFirst(2)))
                .font(.title.weight(.bold))
                .foregroundColor(.white)
        case .h2:
            Text(String(line.text.dropFirst(3)))
                .font(.title2.weight(.bold))
                .foregroundColor(.white)
        case .h3:
            Text(String(line.text.dropFirst(4)))
                .font(.title3.weight(.bold))
                .foregroundColor(.white)
        case .checkbox(let checked):
            HStack(spacing: 8) {
                Image(systemName: checked ? "checkmark.square.fill" : "square")
                    .foregroundColor(checked ? Color(hex: "10B981") : Color(hex: "8E8E9A"))
                Text(String(line.text.dropFirst(7)))
                    .strikethrough(checked)
                    .foregroundColor(checked ? Color(hex: "8E8E9A") : .white)
            }
        case .bullet:
            HStack(alignment: .top, spacing: 8) {
                Text("•")
                    .foregroundColor(Color(hex: "6366F1"))
                Text(String(line.text.dropFirst(2)))
                    .foregroundColor(.white)
            }
        case .numbered:
            Text(line.text)
                .foregroundColor(.white)
        case .blockquote:
            HStack(spacing: 12) {
                Rectangle()
                    .fill(Color(hex: "6366F1"))
                    .frame(width: 3)
                Text(String(line.text.dropFirst(2)))
                    .foregroundColor(Color(hex: "8E8E9A"))
                    .italic()
            }
        case .codeBlock:
            Text(line.text)
                .font(.system(.body, design: .monospaced))
                .foregroundColor(Color(hex: "A78BFA"))
                .padding(.vertical, 4)
        case .horizontalRule:
            Divider()
                .background(Color(hex: "252532"))
                .padding(.vertical, 8)
        case .body:
            renderBodyWithWikiLinks(line.text)
        }
    }

    private func renderBodyWithWikiLinks(_ text: String) -> some View {
        buildStyledText(text)
    }

    private func buildStyledText(_ text: String) -> Text {
        let pattern = #"\[\[([^\]]+)\]\]|\*\*(.+?)\*\*|\*(.+?)\*|`([^`]+)`"#
        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
            return Text(text).font(.body).foregroundColor(.white)
        }

        let nsString = text as NSString
        let range = NSRange(location: 0, length: nsString.length)
        let matches = regex.matches(in: text, options: [], range: range)

        if matches.isEmpty {
            return Text(text).font(.body).foregroundColor(.white)
        }

        var result = Text("")
        var currentIndex = text.startIndex

        for match in matches {
            guard let matchRange = Range(match.range, in: text) else { continue }

            // Text before match
            if currentIndex < matchRange.lowerBound {
                let beforeText = String(text[currentIndex..<matchRange.lowerBound])
                result = result + Text(beforeText).font(.body).foregroundColor(.white)
            }

            // Determine what was matched
            let matchText = String(text[matchRange])

            if matchText.hasPrefix("[[") && matchText.hasSuffix("]]") {
                // Wiki-link
                let linkContent = String(matchText.dropFirst(2).dropLast(2))
                result = result + Text(linkContent)
                    .font(.body)
                    .foregroundColor(Color(hex: "A78BFA"))
                    .underline()
            } else if matchText.hasPrefix("**") && matchText.hasSuffix("**") {
                // Bold
                let boldContent = String(matchText.dropFirst(2).dropLast(2))
                result = result + Text(boldContent)
                    .font(.body.weight(.bold))
                    .foregroundColor(.white)
            } else if matchText.hasPrefix("*") && matchText.hasSuffix("*") {
                // Italic
                let italicContent = String(matchText.dropFirst(1).dropLast(1))
                result = result + Text(italicContent)
                    .font(.body.italic())
                    .foregroundColor(.white)
            } else if matchText.hasPrefix("`") && matchText.hasSuffix("`") {
                // Code
                let codeContent = String(matchText.dropFirst(1).dropLast(1))
                result = result + Text(codeContent)
                    .font(.system(.body, design: .monospaced))
                    .foregroundColor(Color(hex: "A78BFA"))
            }

            currentIndex = matchRange.upperBound
        }

        // Remaining text
        if currentIndex < text.endIndex {
            let remainingText = String(text[currentIndex...])
            result = result + Text(remainingText).font(.body).foregroundColor(.white)
        }

        return result
    }
}

struct ParsedLine: Identifiable {
    let id: Int
    let text: String
    let style: LineStyle
}

enum LineStyle {
    case body, h1, h2, h3, bullet, numbered, checkbox(Bool), blockquote, codeBlock, horizontalRule
}
