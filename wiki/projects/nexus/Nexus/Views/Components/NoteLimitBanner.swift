import SwiftUI

struct NoteLimitBanner: View {
    let currentCount: Int
    let maxCount: Int
    let onUpgrade: () -> Void

    private var remaining: Int { maxCount - currentCount }

    var body: some View {
        VStack(spacing: 0) {
            HStack(spacing: 12) {
                Image(systemName: "exclamationmark.triangle.fill")
                    .foregroundColor(Color(hex: "F59E0B"))
                    .font(.body)

                VStack(alignment: .leading, spacing: 2) {
                    Text("Note limit reached")
                        .font(.subheadline.weight(.semibold))
                        .foregroundColor(.white)

                    Text("Upgrade to Pro for unlimited notes")
                        .font(.caption)
                        .foregroundColor(Color(hex: "8E8E9A"))
                }

                Spacer()

                Button {
                    onUpgrade()
                } label: {
                    Text("Upgrade")
                        .font(.caption.weight(.semibold))
                        .foregroundColor(.white)
                        .padding(.horizontal, 16)
                        .padding(.vertical, 8)
                        .background(Color(hex: "6366F1"))
                        .clipShape(Capsule())
                }
            }
            .padding(16)

            // Progress bar
            GeometryReader { geometry in
                ZStack(alignment: .leading) {
                    Rectangle()
                        .fill(Color(hex: "252532"))
                        .frame(height: 3)

                    Rectangle()
                        .fill(Color(hex: "EF4444"))
                        .frame(width: geometry.size.width, height: 3)
                }
            }
            .frame(height: 3)
        }
        .background(Color(hex: "1A1A24"))
    }
}

struct NoteApproachingBanner: View {
    let currentCount: Int
    let maxCount: Int
    let onUpgrade: () -> Void

    private var remaining: Int { maxCount - currentCount }

    var body: some View {
        HStack(spacing: 12) {
            Image(systemName: "chart.bar.fill")
                .foregroundColor(Color(hex: "F59E0B"))
                .font(.caption)

            Text("\(remaining) note\(remaining == 1 ? "" : "s") remaining")
                .font(.caption)
                .foregroundColor(Color(hex: "8E8E9A"))

            Spacer()

            Button {
                onUpgrade()
            } label: {
                Text("Upgrade")
                    .font(.caption.weight(.semibold))
                    .foregroundColor(Color(hex: "6366F1"))
            }
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 8)
        .background(Color(hex: "1A1A24").opacity(0.8))
    }
}

#Preview {
    VStack(spacing: 20) {
        NoteLimitBanner(currentCount: 50, maxCount: 50, onUpgrade: {})
        NoteApproachingBanner(currentCount: 45, maxCount: 50, onUpgrade: {})
    }
    .background(Color(hex: "0A0A0F"))
    .preferredColorScheme(.dark)
}
