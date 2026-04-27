import SwiftUI
import UIKit

/// Tappable markdown renderer - wiki-links are clickable, other markdown is styled
struct TappableMarkdownView: View {
    let content: String
    let onWikiLinkTap: (String) -> Void

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
            TappableTextLine(text: line.text, onWikiLinkTap: onWikiLinkTap)
        }
    }
}

/// A single line of text with tappable wiki-links
struct TappableTextLine: View {
    let text: String
    let onWikiLinkTap: (String) -> Void

    var body: some View {
        TappableTextRepresentable(
            text: text,
            onWikiLinkTap: onWikiLinkTap
        )
    }
}

/// UIViewRepresentable wrapper for UITextView with tappable NSLinkAttributeName
struct TappableTextRepresentable: UIViewRepresentable {
    let text: String
    let onWikiLinkTap: (String) -> Void

    func makeUIView(context: Context) -> UITextView {
        let textView = UITextView()
        textView.isEditable = false
        textView.isScrollEnabled = false
        textView.backgroundColor = .clear
        textView.textContainerInset = .zero
        textView.textContainer.lineFragmentPadding = 0
        textView.setContentHuggingPriority(.defaultHigh, for: .horizontal)
        textView.setContentCompressionResistancePriority(.defaultHigh, for: .horizontal)
        textView.delegate = context.coordinator
        return textView
    }

    func updateUIView(_ uiView: UITextView, context: Context) {
        let attributedString = buildAttributedString()
        uiView.attributedText = attributedString
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(onWikiLinkTap: onWikiLinkTap)
    }

    private func buildAttributedString() -> NSAttributedString {
        let result = NSMutableAttributedString()
        let fullRange = NSRange(location: 0, length: text.utf16.count)

        // Pattern matches: [[wiki-link]], **bold**, *italic*, `code`
        let pattern = #"\[\[([^\]]+)\]\]|\*\*(.+?)\*\*|\*(.+?)\*|`([^`]+)`"#
        guard let regex = try? NSRegularExpression(pattern: pattern, options: []) else {
            return NSAttributedString(string: text, attributes: defaultAttributes())
        }

        let matches = regex.matches(in: text, options: [], range: fullRange)

        if matches.isEmpty {
            return NSAttributedString(string: text, attributes: defaultAttributes())
        }

        var currentIndex = 0

        for match in matches {
            let matchRange = match.range

            // Text before match
            if matchRange.location > currentIndex {
                let beforeRange = NSRange(location: currentIndex, length: matchRange.location - currentIndex)
                let beforeText = (text as NSString).substring(with: beforeRange)
                result.append(NSAttributedString(string: beforeText, attributes: defaultAttributes()))
            }

            // Matched content
            if matchRange.location == currentIndex {
                let matchText = (text as NSString).substring(with: matchRange)

                if matchText.hasPrefix("[[") && matchText.hasSuffix("]]") {
                    // Wiki-link — tappable with custom attributes
                    let linkContent = String(matchText.dropFirst(2).dropLast(2))
                    let linkAttributes: [NSAttributedString.Key: Any] = [
                        .font: UIFont.systemFont(ofSize: 17),
                        .foregroundColor: UIColor(Color(hex: "A78BFA")),
                        .underlineStyle: NSUnderlineStyle.single.rawValue,
                        .link: "wikilink://\(linkContent)"
                    ]
                    result.append(NSAttributedString(string: matchText, attributes: linkAttributes))
                } else if matchText.hasPrefix("**") && matchText.hasSuffix("**") {
                    let boldContent = String(matchText.dropFirst(2).dropLast(2))
                    let boldAttributes: [NSAttributedString.Key: Any] = [
                        .font: UIFont.boldSystemFont(ofSize: 17),
                        .foregroundColor: UIColor.white
                    ]
                    result.append(NSAttributedString(string: boldContent, attributes: boldAttributes))
                } else if matchText.hasPrefix("*") && matchText.hasSuffix("*") {
                    let italicContent = String(matchText.dropFirst(1).dropLast(1))
                    let italicAttributes: [NSAttributedString.Key: Any] = [
                        .font: UIFont.italicSystemFont(ofSize: 17),
                        .foregroundColor: UIColor.white
                    ]
                    result.append(NSAttributedString(string: italicContent, attributes: italicAttributes))
                } else if matchText.hasPrefix("`") && matchText.hasSuffix("`") {
                    let codeContent = String(matchText.dropFirst(1).dropLast(1))
                    let codeAttributes: [NSAttributedString.Key: Any] = [
                        .font: UIFont.monospacedSystemFont(ofSize: 17, weight: .regular),
                        .foregroundColor: UIColor(Color(hex: "A78BFA"))
                    ]
                    result.append(NSAttributedString(string: codeContent, attributes: codeAttributes))
                } else {
                    result.append(NSAttributedString(string: matchText, attributes: defaultAttributes()))
                }

                currentIndex = matchRange.location + matchRange.length
            }
        }

        // Remaining text
        if currentIndex < text.utf16.count {
            let remainingRange = NSRange(location: currentIndex, length: text.utf16.count - currentIndex)
            let remainingText = (text as NSString).substring(with: remainingRange)
            result.append(NSAttributedString(string: remainingText, attributes: defaultAttributes()))
        }

        return result
    }

    private func defaultAttributes() -> [NSAttributedString.Key: Any] {
        [
            .font: UIFont.systemFont(ofSize: 17),
            .foregroundColor: UIColor.white
        ]
    }

    class Coordinator: NSObject, UITextViewDelegate {
        let onWikiLinkTap: (String) -> Void

        init(onWikiLinkTap: @escaping (String) -> Void) {
            self.onWikiLinkTap = onWikiLinkTap
        }

        func textView(_ textView: UITextView, shouldInteractWith URL: URL, in characterRange: NSRange, interaction: UITextItemInteraction) -> Bool {
            if URL.scheme == "wikilink" {
                let linkContent = URL.host ?? ""
                if !linkContent.isEmpty {
                    onWikiLinkTap(linkContent)
                }
                return false
            }
            return true
        }
    }
}
