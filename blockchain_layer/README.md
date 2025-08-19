# Blockchain Layer

This repository contains the blockchain layer of our DeFi project, structured to support XRPL and Solana Protocol. This layer is designed with a microservices architecture for scalability, flexibility, and ease of maintenance. Making changes to listed protocols.

## Directory Structure

- `smart_contracts/`: Contains all smart contracts.
- `xrpl/` : 
- `solana_service/`: Responsible for direct Solana blockchain interactions, including transaction submissions and event listening.
- `spl_service/`: Responsible for direct blockchain interactions, including transaction submissions and event listening.
- `oracles/`: Fetch and relay external data required by smart contracts for operations such as pricing assets.
- `data_storage/`: Handles off-chain data storage needs and high-speed read operations.


Each microservice directory contains its source code and `Dockerfile` for containerization.

## Services Overview

- **Smart Contracts**: Core business logic of our DeFi project implemented on the blockchain.
- **Solana Service**: This service manages connections made to the Solana blockchain.
- **SPL Service**: The SPL Service is responsible for the creation and management of Solana programs within our DeFi project's ecosystem.
- **Oracles**: Provides reliable data feeds to smart contracts.
- **Data Storage**: Off-chain database services for additional data management needs.

## Getting Started

To get started with the blockchain layer:
1. Ensure you have Docker installed and running on your system.
2. Clone the repository and navigate into each microservice directory you wish to deploy.
3. Build the Docker image using the provided Dockerfile within each directory.
4. Run the Docker container as per the instructions in the service-specific README.



