# The Construct: Decentralized Robotics Exchange (DREX)

The Construct is a groundbreaking decentralized robotics exchange (DREX) that revolutionizes how robot manufacturing and software development coalesce. It empowers manufacturers to showcase robot bodies and components while providing developers with a platform for bespoke software solutions—all powered by a high-performance blockchain infrastructure.

---

## 🚀 MVP Strategy: Modular & Agent-Native

To maximize development velocity and market validation, The Construct has transitioned to a **Modular Monolith** architecture focusing on an **XRPL-First** implementation for its MVP.

### Key Architectural Shifts:
- **Modular Monolith:** Consolidated fragmented microservices into a single, high-cohesion FastAPI application.
- **XRPL-First:** Leveraging the native speed, DEX, and tokenization capabilities of the XRP Ledger for all core marketplace functions.
- **Agent-Native (MCP):** Integrated the **Model Context Protocol (MCP)** to allow AI agents to autonomously interact with the marketplace, search designs, and craft transactions.

---

## 🏗️ Project Structure

### `application_layer/` (Active MVP)
The heart of the platform, built with **Python & FastAPI**.
- **`app/modules/`**: Encapsulated business domains.
    - `identity/`: User management & Auth.
    - `market/`: Trading, Analytics, & Supply Chain.
    - `robotics/`: Robot Specs & Manufacturing state.
    - `ledger/`: Blockchain Abstraction (currently XRPL-focused).
    - `mcp/`: **AI Agent Bridge** (Model Context Protocol).
    - `common/`: Shared resources and sample data.
- **`app/core/`**: Shared infrastructure (Middleware, Config).

### `presentation_layer/`
- **`svelte_the_construct/`**: Modern SvelteKit web application.
- **`the_construct/`**: Flutter-based mobile application.

### `archive/` (Legacy & Scaling)
Contains the original microservices and multi-chain (Solana) logic, preserved for future scaling and reference.
- `blockchain_layer/`: Original TS/Node.js blockchain services.
- `services/`: Standalone microservices (API Gateway, Notifications, etc.).

---

## 🤖 AI Agent Integration (MCP)

The Construct is one of the first marketplaces designed for the **Agentic Web**. By exposing an MCP server, we allow agents to:
- **Search Resources:** `mcp://theconstruct/robotics/designs`
- **Use Tools:** `search_designs(query, manufacturer)`
- **Future:** Crafting complex purchase transactions for human approval.

---

## 🛠️ Technology Stack

- **Backend:** Python 3.12, FastAPI, Pydantic v2.
- **Blockchain:** XRP Ledger (XRPL) for high-speed DEX and Tokenization.
- **AI Bridge:** Model Context Protocol (MCP) SDK.
- **Frontend:** SvelteKit (Web), Flutter (Mobile).
- **Infrastructure:** Docker, Google Cloud Platform (Firestore/Cloud Run).

---

## 🚦 Getting Started (MVP)

### Prerequisites
- Python 3.12+
- An XRPL Testnet account (for ledger interactions)

### Installation
```bash
# Navigate to the application layer
cd application_layer

# Install dependencies
pip install -r requirements.txt

# Run the Modular Monolith
PYTHONPATH=app python3 -m app.main
```

The API will be available at `http://localhost:8080`. Explore the interactive docs at `/docs`.

---

## 🗺️ Roadmap

1. **Phase 1: Foundation (Current)** - Modular Monolith setup, Identity, and MCP Bridge.
2. **Phase 2: XRPL Ledger** - Native DEX integration and Robot Blueprint (NFT) minting.
3. **Phase 3: Web Frontend** - SvelteKit marketplace interface.
4. **Phase 4: Scaling** - Re-introducing Solana for complex manufacturing logic and extracting microservices as needed.

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for our standards and process.

- **Documentation**: [REVISED_ARCHITECTURE_AND_MVP_STRATEGY.md](REVISED_ARCHITECTURE_AND_MVP_STRATEGY.md)
- **Discord**: [Join the Community](https://discord.gg/theConstruct)
