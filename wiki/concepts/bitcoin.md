---
title: "Bitcoin"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [cryptocurrency, blockchain, digital-currency, decentralization]
---

# Bitcoin

## Overview

Bitcoin is the first and most widely recognized [[cryptocurrency]], created in 2009 by an anonymous person or group known as Satoshi Nakamoto. It introduced a revolutionary concept of decentralized digital money that operates without central authorities like governments or banks. Bitcoin enables peer-to-peer value transfer over the internet through a distributed ledger technology called [[blockchain]], which records all transactions transparently and immutably.

The total supply of Bitcoin is capped at 21 million coins, making it a deflationary currency by design. This scarcity model, combined with its decentralized nature, has made Bitcoin both a controversial alternative monetary system and a significant speculative asset. As of 2026, Bitcoin remains the largest cryptocurrency by market capitalization and continues to influence the entire digital currency ecosystem.

## Key Concepts

**Mining** is the process by which new Bitcoin transactions are verified and added to the blockchain. Miners use specialized computer hardware to solve complex mathematical puzzles in a process called Proof of Work. Successful miners receive newly created Bitcoin as a reward, which incentivizes them to secure the network. This mechanism ensures transaction validity while creating new coins in a predictable, controlled manner.

**Wallets** are software applications or hardware devices that store the private keys needed to access and manage Bitcoin. Each wallet is associated with a public address that can receive Bitcoin, similar to an email address. Users must protect their private keys carefully, as losing them means permanently losing access to their funds.

**Cryptographic Security** ensures that Bitcoin transactions are secure and irreversible. Once a transaction is confirmed and added to the blockchain, it cannot be reversed or tampered with. This eliminates chargebacks and fraud concerns that plague traditional payment systems.

## How It Works

Bitcoin operates on a decentralized network of computers (nodes) that collectively maintain the blockchain. When someone sends Bitcoin, the transaction is broadcast to the network where miners group it with others into a block. The block is then added to the chain after miners solve the cryptographic puzzle, creating a permanent record.

The Bitcoin protocol uses elliptic curve cryptography for digital signatures and SHA-256 hashing for block integrity. Nodes verify transactions against the protocol rules, ensuring no double-spending occurs. This trustless system allows participants to transact without needing to trust each other or any central authority.

## Practical Applications

Bitcoin serves multiple purposes in modern finance and technology:

- **Store of Value**: Often called "digital gold," Bitcoin is used as an investment asset and hedge against inflation
- **Remittances**: Cross-border payments with lower fees compared to traditional wire transfers
- **Payment System**: Merchants worldwide accept Bitcoin as payment for goods and services
- **Financial Inclusion**: Provides banking access to unbanked populations without traditional accounts

```javascript
// Example: Checking Bitcoin balance via API
async function getBitcoinBalance(address) {
  const response = await fetch(`https://blockstream.info/api/address/${address}`);
  const data = await response.json();
  return data.chain_stats.funded_txo_sum / 100000000; // Convert satoshis to BTC
}
```

## Examples

Notable Bitcoin implementations and milestones include:

- **El Salvador's Adoption** (2021): First country to make Bitcoin legal tender
- **Institutional Investment**: Major companies like MicroStrategy and Tesla holding Bitcoin on balance sheets
- **Lightning Network**: Layer 2 solution enabling fast, low-cost Bitcoin transactions
- **ETF Approvals**: SEC approval of Bitcoin futures and spot ETFs increasing retail access

## Related Concepts

- [[Cryptocurrency]] - The broader category of digital currencies including Bitcoin
- [[Blockchain]] - The distributed ledger technology powering Bitcoin
- [[Smart Contracts]] - Self-executing contracts that some cryptocurrencies support
- [[Ethereum]] - Second-largest blockchain platform with more advanced features
- [[DeFi]] - Decentralized finance applications built on blockchain technology

## Further Reading

- Bitcoin Whitepaper (Satoshi Nakamoto, 2008)
- "Mastering Bitcoin" by Andreas Antonopoulos
- Bitcoin.org official documentation
- Blockstream explorer for blockchain data

## Personal Notes

Bitcoin represents a fundamental shift in how we think about money and trust in financial systems. Its open-source nature and decentralized governance continue to attract both praise and criticism from economists and technologists alike. Watching how it evolves alongside [[cryptocurrency]] regulation will be important for understanding the future of digital finance.
