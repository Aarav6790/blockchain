# Decentralised Digital Currency

This code tries to implement a simple crypto currency based on the working model of bitcoin. This project includes fundamental features such as making transactions, mining blocks, managing wallets etc. demonstrating core concepts of a decentralised digital currency

## Features

- **Transaction Handling:** Securely create and verify transactions using digital signatures.
- **Blockchain Mining:** Implement proof-of-work to mine new blocks and add them to the blockchain.
- **Wallet Functionality:** Create wallets with unique private and public keys, and manage balances.
- **Blockchain Validation:** Ensure the integrity and validity of the blockchain by verifying hashes.
- 
## Future updates

This project is a basic implementation and lacks several features found in more advanced cryptocurrencies. Future improvements include:

**P2P Network:** Implement a peer-to-peer network for decentralized transaction and block propagation.
**Broadcasting Transactions:** Implement a mechanism to broadcast transactions to all nodes in the network.
**Handle Forking:** Manage forks in the blockchain to ensure consensus across the network.
**Handle Double Spending:** Prevent double spending by verifying transaction authenticity and uniqueness.
**Better Manage Blockchains of Each Wallet:** Ensure each wallet maintains an up-to-date and accurate copy of the blockchain.


## Getting Started

### Prerequisites

- `ecdsa` library

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/simple-cryptocurrency.git

