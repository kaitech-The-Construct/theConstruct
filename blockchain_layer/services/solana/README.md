# SolanaService

SolanaService is a API Microservice designed to interact with the Solana blockchain. It leverages the Solana JSON RPC API to provide an easy-to-use interface for fetching account information, checking balances, retrieving transaction details, and more.

## What is Solana?

Solana is a high-performance blockchain supporting builders around the world creating crypto apps that scale today. It is known for its incredibly fast processing times and lower transaction costs, making it a favorable network for decentralized applications (dApps), crypto exchanges, and NFT marketplaces. 

## Purpose in the Project

In the marketplace of The Construct DEX, robot bodies and software licenses are tokenized as SPL (Solana Program Library) Tokens. Robot bodies possess non-fungible token (NFT) capabilities, while software licenses exhibit fungible token traits​​.

Tokenizing robot bodies as NFTs gives them an unique digital asset status, characterized by distinct features and individual ownership records on the blockchain. This distinction aligns with the variability among robot bodies within The Construct ecosystem, whether in terms of design, functionality, or collectible attributes.

 We use this service for the following:

- Fetching account balances and data for wallets to display to users.
- Monitoring transactions both sent and received by user accounts.
- Getting detailed information about token accounts, including balances and largest accounts.
- Querying the total supply of SPL tokens.
- Performing transaction broadcasting to send and receive assets.

The service plays a crucial role in allowing our application to provide real-time Solana network data and facilitates blockchain interactions necessary for the application's functionality.

## Getting Started

To use SolanaService, you need to have Python installed on your system along with the following dependencies:

- `requests` - For making HTTP requests to the Solana JSON RPC API.
  
Install them using pip:

```bash
pip install requests