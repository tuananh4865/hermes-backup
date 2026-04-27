---
title: Smart Contracts
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [smart-contracts, blockchain, ethereum, solidity, web3, decentralized]
---

# Smart Contracts

## Overview

A smart contract is a self-executing program deployed on a [[blockchain]] that automatically enforces and executes the terms of an agreement between parties when predetermined conditions are met. Coined by cryptographer Nick Szabo in 1994, the concept predates Bitcoin, but it found its practical realization with the Ethereum [[blockchain]], which was specifically designed as a platform for running Turing-complete smart contracts.

Unlike traditional legal contracts that require intermediaries (lawyers, courts, banks) to enforce compliance, smart contracts encode the agreement in code and rely on the [[blockchain's]] distributed consensus mechanism to automatically execute the contract's logic. When the contract code says "transfer X tokens to party B when condition Y is met," the network validates that Y occurred and executes the transfer — no human intervention, no trusted intermediary required. This is sometimes called "trustless" execution because parties don't need to trust each other; they trust the code and the network.

## Key Concepts

**Immutability:** Once deployed, a smart contract's code cannot be modified. This is a deliberate design choice that provides trust and auditability — any party can inspect the contract code and know exactly what it will do. However, this immutability also means bugs cannot be patched directly; upgrades typically require deploying new contract versions and migrating data (via patterns like proxy contracts).

**Determinism:** Smart contracts must be deterministic — given the same inputs, they must produce the same outputs. This is critical for the network's nodes to reach consensus. Non-deterministic behavior (e.g., using the current time as a factor) requires special handling through trusted oracles.

**Gas:** On networks like Ethereum, executing contract code costs "gas" — a metering mechanism where each operation has a defined cost in gas units. Users pay gas fees (in the network's native token, ETH) to have their transactions included. This prevents infinite loops and DoS attacks by making expensive operations costly.

**Oracles:** Smart contracts cannot natively access external data (off-chain data like stock prices, weather, sports results). Oracles are services that feed external data into the blockchain in a trustworthy way. [[Chainlink]] is the leading decentralized oracle network. This is often called the "oracle problem."

**Account Types:** Ethereum has two types of accounts — Externally Owned Accounts (EOAs), controlled by private keys (human users), and Contract Accounts, controlled by code (smart contracts). Both can send and receive tokens.

## How It Works

When a developer writes a smart contract, they typically use a contract-oriented language like [[Solidity]] (the most popular) or Vyper. The code is compiled into bytecode and deployed to the blockchain via a transaction from an EOA, paying gas for the deployment. Each node in the network stores the contract's bytecode and will execute it when called.

```solidity
// Simple Solidity smart contract example
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleStorage {
    uint256 private storedValue;

    event ValueChanged(uint256 newValue);

    function set(uint256 _value) public {
        storedValue = _value;
        emit ValueChanged(_value);
    }

    function get() public view returns (uint256) {
        return storedValue;
    }
}
```

When someone calls `set(42)` on this contract:
1. The transaction is broadcast to the network
2. Miners/validators group it into a block
3. Each node executes the contract code locally
4. The network reaches consensus that `storedValue` is now 42
5. The state change is permanently recorded on the blockchain

## Practical Applications

- **Decentralized Finance (DeFi):** [[DeFi]] protocols use smart contracts for lending (Aave, Compound), decentralized exchanges (Uniswap), stablecoins (DAI), and yield farming. These eliminate traditional financial intermediaries.
- **NFTs:** Non-fungible tokens on Ethereum use smart contracts to define ownership and metadata of digital art, collectibles, and in-game assets.
- **DAOs:** Decentralized Autonomous Organizations use voting and governance smart contracts to make collective decisions without centralized leadership.
- **Supply Chain Tracking:** Smart contracts can record and trigger actions as goods move through supply chains (e.g., releasing payment when a shipment is confirmed received).
- **Insurance:** Parametric insurance uses oracle-fed data (weather, flight delays) to automatically trigger payouts when conditions are met.
- **Digital Identity:** Self-sovereign identity systems can use smart contracts for verifiable credentials and access control.

## Examples

- **Ethereum Name Service (ENS):** Smart contracts that map human-readable names to Ethereum addresses
- **Uniswap:** Decentralized exchange where the trading logic is entirely in smart contracts; no order book, no central operator
- **OpenSea:** NFT marketplace with smart contracts handling listing, bidding, and trading
- **Aave:** Decentralized lending protocol where interest rates are algorithmically set based on supply and demand
- **The DAO Hack (2016):** A vulnerability in a smart contract's recursive call pattern led to $60M theft, resulting in a controversial hard fork of Ethereum — a cautionary tale about the importance of smart contract security auditing

## Related Concepts

- [[Blockchain]] — The distributed ledger platform smart contracts run on
- [[Ethereum]] — The leading smart contract platform
- [[Solidity]] — Programming language for Ethereum smart contracts
- [[DeFi]] — Decentralized Finance ecosystem built on smart contracts
- [[Web3]] — The decentralized web paradigm smart contracts enable
- [[Chainlink]] — Decentralized oracle network for bringing off-chain data to contracts
- [[NFT]] — Non-fungible tokens implemented as smart contracts

## Further Reading

- Ethereum Documentation: https://ethereum.org/en/developers/docs/
- Solidity Documentation: https://docs.soliditylang.org/
- Smart Contract Security: https://consensys.io/blog/the-smart-contract-security-landscape

## Personal Notes

Smart contracts are revolutionary but often oversold. The "code is law" framing is seductive, but the 2016 DAO hack and numerous DeFi exploits show that buggy code is not law — it's just buggy code that people lost real money on. Formal verification (mathematically proving contract correctness) is gaining traction but isn't yet standard practice. The oracle problem remains underappreciated — a smart contract is only as trustworthy as the data fed to it. And the UX of interacting with smart contracts (wallet management, gas fees, complex addresses) remains a significant barrier to mainstream adoption.
