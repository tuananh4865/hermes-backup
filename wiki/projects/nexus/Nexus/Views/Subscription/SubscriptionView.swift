import SwiftUI

struct SubscriptionView: View {
    @Environment(\.dismiss) private var dismiss
    @State private var subscriptionManager = SubscriptionManager.shared
    @State private var selectedPlan: SubscriptionPlan = .yearly
    @State private var isPurchasing = false
    @State private var purchaseError: String?

    enum SubscriptionPlan {
        case monthly
        case yearly
    }

    var body: some View {
        NavigationStack {
            ZStack {
                Color(hex: "0A0A0F")
                    .ignoresSafeArea()

                ScrollView {
                    VStack(spacing: 32) {
                        // Hero
                        VStack(spacing: 16) {
                            Image(systemName: "star.circle.fill")
                                .font(.system(size: 64))
                                .foregroundStyle(
                                    LinearGradient(
                                        colors: [Color(hex: "6366F1"), Color(hex: "A78BFA")],
                                        startPoint: .topLeading,
                                        endPoint: .bottomTrailing
                                    )
                                )

                            Text("Unlock Nexus Pro")
                                .font(.title.weight(.bold))
                                .foregroundColor(.white)

                            Text("Get unlimited access to all features")
                                .font(.subheadline)
                                .foregroundColor(Color(hex: "8E8E9A"))
                        }
                        .padding(.top, 32)

                        // Features
                        VStack(alignment: .leading, spacing: 16) {
                            featureRow(icon: "doc.on.doc", text: "Unlimited notes")
                            featureRow(icon: "circle.hexagongrid.circle", text: "Unlimited graph views")
                            featureRow(icon: "brain", text: "AI semantic search")
                            featureRow(icon: "link.circle", text: "AI auto-linking suggestions")
                            featureRow(icon: "tag", text: "AI smart tags")
                            featureRow(icon: "icloud", text: "iCloud sync")
                            featureRow(icon: "person.fill.questionmark", text: "Priority support")
                        }
                        .padding(.horizontal, 32)

                        // Pricing
                        VStack(spacing: 12) {
                            // Monthly
                            Button {
                                selectedPlan = .monthly
                            } label: {
                                HStack {
                                    VStack(alignment: .leading, spacing: 4) {
                                        Text("Monthly")
                                            .font(.headline)
                                            .foregroundColor(.white)
                                        Text("$4.99/month")
                                            .font(.caption)
                                            .foregroundColor(Color(hex: "8E8E9A"))
                                    }
                                    Spacer()
                                    if selectedPlan == .monthly {
                                        Image(systemName: "checkmark.circle.fill")
                                            .foregroundColor(Color(hex: "6366F1"))
                                    } else {
                                        Circle()
                                            .stroke(Color(hex: "252532"), lineWidth: 2)
                                            .frame(width: 24, height: 24)
                                    }
                                }
                                .padding(16)
                                .background(selectedPlan == .monthly ? Color(hex: "6366F1").opacity(0.1) : Color(hex: "1A1A24"))
                                .clipShape(RoundedRectangle(cornerRadius: 12))
                            }

                            // Yearly
                            Button {
                                selectedPlan = .yearly
                            } label: {
                                HStack {
                                    VStack(alignment: .leading, spacing: 4) {
                                        HStack(spacing: 8) {
                                            Text("Yearly")
                                                .font(.headline)
                                                .foregroundColor(.white)
                                            Text("Save 50%")
                                                .font(.caption.weight(.semibold))
                                                .foregroundColor(Color(hex: "10B981"))
                                                .padding(.horizontal, 8)
                                                .padding(.vertical, 2)
                                                .background(Color(hex: "10B981").opacity(0.2))
                                                .clipShape(Capsule())
                                        }
                                        Text("$29.99/year")
                                            .font(.caption)
                                            .foregroundColor(Color(hex: "8E8E9A"))
                                    }
                                    Spacer()
                                    if selectedPlan == .yearly {
                                        Image(systemName: "checkmark.circle.fill")
                                            .foregroundColor(Color(hex: "6366F1"))
                                    } else {
                                        Circle()
                                            .stroke(Color(hex: "252532"), lineWidth: 2)
                                            .frame(width: 24, height: 24)
                                    }
                                }
                                .padding(16)
                                .background(selectedPlan == .yearly ? Color(hex: "6366F1").opacity(0.1) : Color(hex: "1A1A24"))
                                .clipShape(RoundedRectangle(cornerRadius: 12))
                            }
                        }
                        .padding(.horizontal, 32)

                        // Error message
                        if let error = purchaseError {
                            Text(error)
                                .font(.caption)
                                .foregroundColor(Color(hex: "EF4444"))
                                .padding(.horizontal, 32)
                        }

                        // CTA
                        VStack(spacing: 16) {
                            Button {
                                Task {
                                    await subscribe()
                                }
                            } label: {
                                if isPurchasing {
                                    ProgressView()
                                        .progressViewStyle(CircularProgressViewStyle(tint: .white))
                                        .frame(maxWidth: .infinity)
                                        .padding(.vertical, 16)
                                } else {
                                    Text("Subscribe Now")
                                        .font(.headline)
                                        .foregroundColor(.white)
                                        .frame(maxWidth: .infinity)
                                        .padding(.vertical, 16)
                                        .background(Color(hex: "6366F1"))
                                        .clipShape(RoundedRectangle(cornerRadius: 12))
                                }
                            }
                            .disabled(isPurchasing || subscriptionManager.isPro)

                            Button {
                                Task {
                                    await restore()
                                }
                            } label: {
                                Text("Restore Purchases")
                                    .font(.subheadline)
                                    .foregroundColor(Color(hex: "6366F1"))
                            }
                        }
                        .padding(.horizontal, 32)

                        // Footer
                        VStack(spacing: 4) {
                            Text("Cancel anytime")
                                .font(.caption)
                                .foregroundColor(Color(hex: "8E8E9A"))
                            Text("By subscribing, you agree to our Terms of Service and Privacy Policy")
                                .font(.caption2)
                                .foregroundColor(Color(hex: "8E8E9A"))
                                .multilineTextAlignment(.center)
                        }
                        .padding(.horizontal, 32)
                        .padding(.bottom, 32)
                    }
                }
            }
            .navigationBarTitleDisplayMode(.inline)
            .toolbarBackground(Color(hex: "0A0A0F"), for: .navigationBar)
            .toolbarColorScheme(.dark, for: .navigationBar)
            .toolbar {
                ToolbarItem(placement: .topBarTrailing) {
                    Button {
                        dismiss()
                    } label: {
                        Image(systemName: "xmark")
                            .foregroundColor(Color(hex: "8E8E9A"))
                    }
                }
            }
        }
        .preferredColorScheme(.dark)
    }

    private func featureRow(icon: String, text: String) -> some View {
        HStack(spacing: 12) {
            Image(systemName: icon)
                .font(.body)
                .foregroundColor(Color(hex: "6366F1"))
                .frame(width: 24)

            Text(text)
                .font(.body)
                .foregroundColor(.white)

            Spacer()

            Image(systemName: "checkmark")
                .font(.caption.weight(.semibold))
                .foregroundColor(Color(hex: "10B981"))
        }
    }

    @MainActor
    private func subscribe() async {
        isPurchasing = true
        purchaseError = nil

        let productID = selectedPlan == .monthly
            ? subscriptionManager.productID
            : subscriptionManager.yearlyProductID

        guard let product = subscriptionManager.products.first(where: { $0.id == productID }) else {
            // Products not loaded yet, try to load and retry
            await subscriptionManager.loadProducts()
            guard let product = subscriptionManager.products.first(where: { $0.id == productID }) else {
                purchaseError = "Unable to load products. Please try again."
                isPurchasing = false
                return
            }
            do {
                let success = try await subscriptionManager.purchase(product)
                if success {
                    dismiss()
                }
            } catch {
                purchaseError = "Purchase failed. Please try again."
            }
            isPurchasing = false
            return
        }

        do {
            let success = try await subscriptionManager.purchase(product)
            if success {
                dismiss()
            }
        } catch {
            purchaseError = "Purchase failed. Please try again."
        }
        isPurchasing = false
    }

    @MainActor
    private func restore() async {
        isPurchasing = true
        purchaseError = nil

        await subscriptionManager.restore()

        if subscriptionManager.isPro {
            dismiss()
        } else {
            purchaseError = "No previous purchases found."
        }
        isPurchasing = false
    }
}
