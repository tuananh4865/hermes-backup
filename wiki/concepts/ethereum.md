---
title: "Ethereum"
created: 2026-04-13
updated: 2026-04-13
type: concept
tags: [ethereum, blockchain, cryptocurrency, smart-contracts, web3, defi, solidity]
---

# Ethereum

## Overview

Ethereum is a decentralized, open-source blockchain platform launched in 2015 by Vitalik Buterin and a team of co-founders. While Bitcoin pioneered digital scarcity and decentralized value transfer, Ethereum extended the blockchain concept to enable arbitrary program execution through smart contracts. This innovation transformed Ethereum from a single cryptocurrency into a global platform for decentralized applications (dApps), decentralized finance (DeFi), non-fungible tokens (NFTs), and much more. Ethereum's native cryptocurrency, Ether (ETH), is the second-largest cryptocurrency by market capitalization after Bitcoin. The network uses a virtual machine called the Ethereum Virtual Machine (EVM) to execute smart contracts, and developers write these contracts in Solidity or Vyper programming languages. Ethereum's transition from Proof-of-Work to Proof-of-Stake consensus (called "The Merge" in 2022) reduced energy consumption by approximately 99.95%.

## Key Concepts

**Smart Contracts** are self-executing programs deployed on the Ethereum blockchain. Once deployed, a smart contract's code cannot be modified — it executes exactly as written. This "code is law" property makes smart contracts powerful for trustless agreements, escrow, governance, and automated financial instruments. Smart contracts have an address on the blockchain just like external accounts, and can send transactions, hold balances, and interact with other contracts.

**Ethereum Virtual Machine (EVM)** is the runtime environment for all smart contracts on Ethereum. The EVM is Turing-complete, meaning it can compute any computable function given enough resources (gas). It operates as a stack-based virtual machine, processing opcodes that manipulate stack, memory, and storage. Every node in the Ethereum network runs the EVM to validate smart contract execution, ensuring consensus.

**Gas** is the metering mechanism for Ethereum computation. Every operation in the EVM consumes a specific amount of gas, which users must pay in Ether. Gas prices fluctuate based on network demand — during periods of high activity, users bid higher gas prices to have their transactions included quickly. The introduction of EIP-1559 in 2021 changed the fee market, with a base fee that is burned and a priority fee that goes to validators.

**Accounts** — Ethereum has two types of accounts:
- **Externally Owned Accounts (EOAs)** — Controlled by private keys, used to initiate transactions
- **Contract Accounts** — Controlled by their smart contract code, can only respond to transactions

**Proof-of-Stake (PoS)** — Since The Merge, Ethereum uses PoS consensus where validators stake 32 ETH to participate in block production. Validators are randomly selected to propose and attest to blocks, and malicious behavior results in penalty (slashing) of staked ETH. PoS enables sharding and is vastly more energy-efficient than PoW.

## How It Works

Ethereum's transaction lifecycle:

1. **Transaction Creation** — A user (EOA) creates a transaction specifying: target address, value (ETH amount), data (for contract calls), gas limit, and max priority fee per gas.
2. **Broadcasting** — The transaction is sent to an Ethereum node, which validates the signature and propagates it to peers.
3. **Mempool** — Valid transactions wait in the mempool (a waiting area) until a validator picks them up.
4. **Block Proposal** — Validators are randomly selected to propose blocks. A validator bundles transactions from the mempool into a block.
5. **Execution** — All nodes independently execute the transactions in the proposed block using the EVM to verify the result.
6. **Consensus** — validators attest to the block's correctness. Once enough attestations accumulate (2/3 of total stake), the block is finalized.
7. **State Update** — The canonical state of Ethereum is updated, and the block becomes immutable.

## Practical Applications

- **DeFi (Decentralized Finance)** — Uniswap, Aave, Compound — lending, borrowing, and trading without intermediaries
- **NFTs** — ERC-721 and ERC-1155 tokens representing digital art, collectibles, and in-game assets
- **DAOs** — Decentralized Autonomous Organizations using on-chain governance
- **Gaming** — Play-to-earn games with in-game assets as tokens
- **Identity** — Self-sovereign identity systems using ENS (Ethereum Name Service)
- **Cross-border payments** — Fast, low-cost international transfers via stablecoins
- **DAOs and Governance** — On-chain voting and treasury management

## Examples

A simple Solidity smart contract for an ERC-20 token:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract SimpleToken {
    string public name;
    string public symbol;
    uint8 public decimals;
    uint256 public totalSupply;
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;

    event Transfer(address indexed from, address indexed to, uint256 value);
    event Approval(address indexed owner, address indexed spender, uint256 value);

    constructor(
        string memory _name,
        string memory _symbol,
        uint8 _decimals,
        uint256 _initialSupply
    ) {
        name = _name;
        symbol = _symbol;
        decimals = _decimals;
        totalSupply = _initialSupply * (10 ** uint256(_decimals));
        balanceOf[msg.sender] = totalSupply;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "Insufficient balance");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;
        emit Approval(msg.sender, spender, amount);
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        require(balanceOf[from] >= amount, "Insufficient balance");
        require(allowance[from][msg.sender] >= amount, "Allowance exceeded");
        balanceOf[from] -= amount;
        allowance[from][msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }
}
```

## Related Concepts

- [[Blockchain]] — The underlying distributed ledger technology Ethereum uses
- [[Smart Contracts]] — Self-executing programs on Ethereum
- [[Solidity]] — The primary language for writing Ethereum smart contracts
- [[DeFi]] — Decentralized Finance applications built on Ethereum
- [[NFT]] — Non-Fungible Tokens, a prominent Ethereum use case
- [[Proof-of-Stake]] — Ethereum's current consensus mechanism

## Further Reading

- [ethereum.org](https://ethereum.org/) — Official Ethereum documentation
- [Ethers.js Documentation](https://docs.ethers.org/) — JavaScript library for Ethereum interaction
- [OpenZeppelin Contracts](https://www.openzeppelin.com/contracts/) — Battle-tested smart contract libraries
- [Ethereum Yellow Paper](https://ethereum.github.io/yellowpaper/paper.pdf) — Formal specification

## Personal Notes

Ethereum represents a fundamental shift in how I think about trust and coordination. The idea that you can write a financial agreement in code and have it execute automatically without any bank, lawyer, or arbitrator in the middle is genuinely revolutionary. That said, the ecosystem is not without problems — network congestion can make transaction fees (gas) prohibitively expensive during peak times, and smart contract bugs have led to billions of dollars in losses. The move to Proof-of-Stake was a remarkable engineering achievement. Layer 2 solutions like Arbitrum and Optimism have done a lot to address the scalability issues by processing transactions off the main Ethereum chain while inheriting its security.
