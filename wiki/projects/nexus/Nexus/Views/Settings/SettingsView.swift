import SwiftUI

struct SettingsView: View {
    @Environment(\.dismiss) private var dismiss
    @AppStorage("appearanceMode") private var appearanceMode: String = "dark"
    @AppStorage("editorFontSize") private var editorFontSize: Double = 17
    @AppStorage("showGraphLabels") private var showGraphLabels: Bool = true
    @State private var subscriptionManager = SubscriptionManager.shared
    @State private var showSubscription = false

    var body: some View {
        NavigationStack {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                ScrollView {
                    VStack(spacing: 24) {
                        // Account Section
                        settingsSection(title: "Account") {
                            Button {
                                showSubscription = true
                            } label: {
                                HStack {
                                    settingsRowContent(icon: "star.circle", title: "Subscription") {
                                        Text(subscriptionManager.isPro ? "Pro Plan" : "Free Plan (50 notes)")
                                            .font(.subheadline)
                                            .foregroundColor(Color(hex: "8E8E9A"))
                                    }
                                    Spacer()
                                    if !subscriptionManager.isPro {
                                        Text("Upgrade")
                                            .font(.subheadline.weight(.semibold))
                                            .foregroundColor(Color(hex: "6366F1"))
                                            .padding(.trailing, 16)
                                    }
                                }
                            }
                            .buttonStyle(.plain)
                        }

                        // Appearance Section
                        settingsSection(title: "Appearance") {
                            VStack(spacing: 0) {
                                settingsRow(icon: "paintbrush", title: "Theme") {
                                    Picker("Theme", selection: $appearanceMode) {
                                        Text("Dark").tag("dark")
                                        Text("Light").tag("light")
                                        Text("System").tag("system")
                                    }
                                    .pickerStyle(.menu)
                                    .tint(Color(hex: "8E8E9A"))
                                }

                                Divider()
                                    .background(Color(hex: "252532"))
                                    .padding(.leading, 52)

                                settingsRow(icon: "textformat.size", title: "Editor Font Size") {
                                    HStack(spacing: 12) {
                                        Text("\(Int(editorFontSize))pt")
                                            .foregroundColor(Color(hex: "8E8E9A"))
                                        Slider(value: $editorFontSize, in: 12...24, step: 1)
                                            .frame(width: 120)
                                            .tint(Color(hex: "6366F1"))
                                    }
                                }

                                Divider()
                                    .background(Color(hex: "252532"))
                                    .padding(.leading, 52)

                                settingsRow(icon: "tag", title: "Show Graph Labels") {
                                    Toggle("", isOn: $showGraphLabels)
                                        .tint(Color(hex: "6366F1"))
                                }
                            }
                        }

                        // Sync Section
                        settingsSection(title: "Sync") {
                            VStack(spacing: 0) {
                                settingsRow(icon: "icloud", title: "iCloud Sync") {
                                    Toggle("", isOn: .constant(true))
                                        .tint(Color(hex: "6366F1"))
                                }

                                Divider()
                                    .background(Color(hex: "252532"))
                                    .padding(.leading, 52)

                                settingsRow(icon: "clock", title: "Last Synced") {
                                    Text("Just now")
                                        .foregroundColor(Color(hex: "8E8E9A"))
                                }
                            }
                        }

                        // Data Section
                        settingsSection(title: "Data") {
                            VStack(spacing: 0) {
                                settingsRow(icon: "square.and.arrow.down", title: "Import from Obsidian") {
                                    Image(systemName: "chevron.right")
                                        .font(.caption)
                                        .foregroundColor(Color(hex: "8E8E9A"))
                                }

                                Divider()
                                    .background(Color(hex: "252532"))
                                    .padding(.leading, 52)

                                settingsRow(icon: "square.and.arrow.up", title: "Export All Notes") {
                                    Image(systemName: "chevron.right")
                                        .font(.caption)
                                        .foregroundColor(Color(hex: "8E8E9A"))
                                }
                            }
                        }

                        // About Section
                        settingsSection(title: "About") {
                            VStack(spacing: 0) {
                                settingsRow(icon: "info.circle", title: "Version") {
                                    Text("1.0.0")
                                        .foregroundColor(Color(hex: "8E8E9A"))
                                }

                                Divider()
                                    .background(Color(hex: "252532"))
                                    .padding(.leading, 52)

                                settingsRow(icon: "lock.shield", title: "Privacy Policy") {
                                    Image(systemName: "chevron.right")
                                        .font(.caption)
                                        .foregroundColor(Color(hex: "8E8E9A"))
                                }

                                Divider()
                                    .background(Color(hex: "252532"))
                                    .padding(.leading, 52)

                                settingsRow(icon: "doc.text", title: "Terms of Service") {
                                    Image(systemName: "chevron.right")
                                        .font(.caption)
                                        .foregroundColor(Color(hex: "8E8E9A"))
                                }
                            }
                        }
                    }
                    .padding(.vertical, 24)
                }
            }
            .navigationTitle("Settings")
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button("Done") {
                        dismiss()
                    }
                    .foregroundColor(Color(hex: "6366F1"))
                }
            }
            .sheet(isPresented: $showSubscription) {
                SubscriptionView()
            }
        }
        .preferredColorScheme(.dark)
    }

    private func settingsSection(title: String, @ViewBuilder content: () -> some View) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            Text(title.uppercased())
                .font(.caption.weight(.semibold))
                .foregroundColor(Color(hex: "8E8E9A"))
                .padding(.horizontal, 16)

            VStack(spacing: 0) {
                content()
            }
            .background(Color(hex: "1A1A24"))
            .clipShape(RoundedRectangle(cornerRadius: 12))
            .padding(.horizontal, 16)
        }
    }

    private func settingsRow<Content: View>(
        icon: String,
        title: String,
        @ViewBuilder trailing: () -> Content
    ) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.body)
                .foregroundColor(Color(hex: "6366F1"))
                .frame(width: 28)

            Text(title)
                .font(.body)
                .foregroundColor(.white)

            Spacer()

            trailing()
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
    }

    private func settingsRowContent<Content: View>(
        icon: String,
        title: String,
        @ViewBuilder trailing: () -> Content
    ) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.body)
                .foregroundColor(Color(hex: "6366F1"))
                .frame(width: 28)

            Text(title)
                .font(.body)
                .foregroundColor(.white)

            Spacer()

            trailing()
        }
        .padding(.horizontal, 16)
        .padding(.vertical, 12)
    }
}
