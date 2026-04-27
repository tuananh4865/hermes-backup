import SwiftUI

struct TagInputView: View {
    @Binding var tags: [String]
    @State private var inputText = ""
    @State private var isEditing = false
    @FocusState private var isFocused: Bool

    private let suggestedTags = ["work", "personal", "ideas", "todo", "important", "research"]

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            // Tag display + input
            VStack(alignment: .leading, spacing: 8) {
                Text("Tags")
                    .font(.caption.weight(.semibold))
                    .foregroundColor(Color(hex: "8E8E9A"))

                ScrollView(.horizontal, showsIndicators: false) {
                    HStack(spacing: 8) {
                        ForEach(tags, id: \.self) { tag in
                            tagChip(tag: tag, isRemovable: true)
                        }

                        if isEditing {
                            TextField("Add tag", text: $inputText)
                                .textFieldStyle(.plain)
                                .font(.subheadline)
                                .foregroundColor(.white)
                                .frame(width: 100)
                                .padding(.horizontal, 12)
                                .padding(.vertical, 6)
                                .background(Color(hex: "252532"))
                                .clipShape(Capsule())
                                .focused($isFocused)
                                .onSubmit {
                                    addTag()
                                }
                        } else {
                            Button {
                                isEditing = true
                                isFocused = true
                            } label: {
                                HStack(spacing: 4) {
                                    Image(systemName: "plus")
                                        .font(.caption)
                                    Text("Add")
                                        .font(.caption)
                                }
                                .foregroundColor(Color(hex: "8E8E9A"))
                                .padding(.horizontal, 12)
                                .padding(.vertical, 6)
                                .background(Color(hex: "252532"))
                                .clipShape(Capsule())
                            }
                        }
                    }
                }

                // Suggestions
                if !isEditing && !suggestedTags.filter({ !tags.contains($0) }).isEmpty {
                    ScrollView(.horizontal, showsIndicators: false) {
                        HStack(spacing: 6) {
                            ForEach(suggestedTags.filter { !tags.contains($0) }, id: \.self) { suggestion in
                                Button {
                                    tags.append(suggestion)
                                } label: {
                                    Text(suggestion)
                                        .font(.caption)
                                        .foregroundColor(Color(hex: "A78BFA"))
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 4)
                                        .background(Color(hex: "A78BFA").opacity(0.15))
                                        .clipShape(Capsule())
                                }
                            }
                        }
                    }
                }
            }
        }
        .padding(.horizontal, 16)
        .padding(.top, 12)
        .onChange(of: isFocused) { _, newValue in
            if !newValue && inputText.isEmpty {
                isEditing = false
            }
        }
    }

    private func tagChip(tag: String, isRemovable: Bool) -> some View {
        HStack(spacing: 4) {
            Text(tag)
                .font(.caption)
                .foregroundColor(.white)

            if isRemovable {
                Button {
                    withAnimation(.easeInOut(duration: 0.15)) {
                        tags.removeAll { $0 == tag }
                    }
                } label: {
                    Image(systemName: "xmark")
                        .font(.caption2)
                        .foregroundColor(Color(hex: "8E8E9A"))
                }
            }
        }
        .padding(.horizontal, 10)
        .padding(.vertical, 6)
        .background(Color(hex: "6366F1").opacity(0.3))
        .clipShape(Capsule())
    }

    private func addTag() {
        let tag = inputText.trimmingCharacters(in: .whitespaces).lowercased()
        guard !tag.isEmpty, !tags.contains(tag) else {
            inputText = ""
            isEditing = false
            return
        }
        tags.append(tag)
        inputText = ""
        // Stay in edit mode for more tags
    }
}

#Preview {
    VStack {
        TagInputView(tags: .constant(["work", "ideas"]))
    }
    .frame(maxWidth: .infinity)
    .background(Color(hex: "0A0A0F"))
    .preferredColorScheme(.dark)
}
