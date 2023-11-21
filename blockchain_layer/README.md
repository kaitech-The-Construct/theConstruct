# Blockchain Layer

This repository contains the blockchain layer of our DeFi project, structured to support Ethereum EVM, Solana, and Injective Protocol. This layer is designed with a microservices architecture for scalability, flexibility, and ease of maintenance.

## Directory Structure

- `api_gateway/`: The entry point that handles incoming requests and routes them to the appropriate microservices.
- `smart_contracts/`: Contains all smart contracts, segregated by Ethereum, Solana, and Injective Protocol.
- `blockchain_interaction/`: Responsible for direct blockchain interactions, including transaction submissions and event listening.
- `oracles/`: Fetch and relay external data required by smart contracts for operations such as pricing assets.
- `data_storage/`: Handles off-chain data storage needs and high-speed read operations.
- `message_queue/`: Manages messaging and queueing for reliable inter-service communication.
- `config/`: Configuration files for networks and service setups.
- `lib/`: Shared libraries and utilities used across services.
- `docs/`: Documentation on architecture, usage, and development guidelines.
- `node_modules/`: Node.js dependencies for JavaScript/TypeScript-based tooling.

Each microservice directory contains its source code and `Dockerfile` for containerization.

## Services Overview

- **API Gateway**: Entrypoint for the system, authenticating and routing requests.
- **Smart Contracts**: Core business logic of our DeFi project implemented on the blockchain.
- **Blockchain Interaction**: Handles operations like wallet management and transaction processing.
- **Oracles**: Provides reliable data feeds to smart contracts.
- **Data Storage**: Off-chain database services for additional data management needs.
- **Message Queue**: Asynchronous communication infrastructure for microservices.

## Getting Started

To get started with the blockchain layer:
1. Ensure you have Docker installed and running on your system.
2. Clone the repository and navigate into each microservice directory you wish to deploy.
3. Build the Docker image using the provided Dockerfile within each directory.
4. Run the Docker container as per the instructions in the service-specific README.

## Development and Testing

Each microservice comes with its testing suite. To contribute or test:
1. Navigate to the specific microservice directory.
2. Install dependencies if required.
3. Run the test suite using the predefined scripts in `package.json` or the test framework specified in the service README.


