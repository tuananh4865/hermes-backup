import Foundation
import StoreKit

/// StoreKit 2 subscription manager for Nexus Pro
@Observable
final class SubscriptionManager {
    static let shared = SubscriptionManager()
    
    private var updateListenerTask: Task<Void, Error>?
    
    var products: [Product] = []
    var purchasedProductIDs: Set<String> = []
    var isPro: Bool { purchasedProductIDs.contains(productID) }
    
    let productID = "com.nexus.app.pro.monthly"
    let yearlyProductID = "com.nexus.app.pro.yearly"
    
    private init() {
        updateListenerTask = listenForTransactions()
        Task { await loadProducts() }
    }
    
    deinit {
        updateListenerTask?.cancel()
    }
    
    // MARK: - Load Products
    
    func loadProducts() async {
        do {
            products = try await Product.products(for: [productID, yearlyProductID])
        } catch {
            print("Failed to load products: \(error)")
        }
    }
    
    // MARK: - Purchase
    
    @MainActor
    func purchase(_ product: Product) async throws -> Bool {
        let result = try await product.purchase()
        
        switch result {
        case .success(let verification):
            await handleVerifiedTransaction(verification)
            return true
            
        case .userCancelled:
            return false
            
        case .pending:
            return false
            
        @unknown default:
            return false
        }
    }
    
    // MARK: - Restore
    
    func restore() async {
        do {
            try await AppStore.sync()
            await updatePurchasedProducts()
        } catch {
            print("Failed to restore: \(error)")
        }
    }
    
    // MARK: - Check Entitlements
    
    func checkEntitlements() async {
        await updatePurchasedProducts()
    }
    
    // MARK: - Private
    
    private func listenForTransactions() -> Task<Void, Error> {
        Task.detached { [weak self] in
            for await result in Transaction.updates {
                guard let self = self else { return }
                await self.handleVerifiedTransaction(result)
            }
        }
    }
    
    private func handleVerifiedTransaction(_ result: VerificationResult<Transaction>) async {
        switch result {
        case .verified(let transaction):
            await updatePurchasedProducts()
            await transaction.finish()
        case .unverified:
            break
        }
    }
    
    private func updatePurchasedProducts() async {
        var purchased: Set<String> = []
        
        for await result in Transaction.currentEntitlements {
            if case .verified(let transaction) = result {
                if transaction.revocationDate == nil {
                    purchased.insert(transaction.productID)
                }
            }
        }
        
        purchasedProductIDs = purchased
    }
}
