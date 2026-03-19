# The Construct: Application Layer (Modular Monolith)

This directory contains the FastAPI-based Application Layer for 'The Construct' Decentralized Robotics Exchange (DREX). 

## Architecture: Modular Monolith

The application is structured as a **Modular Monolith** to maximize development velocity while maintaining high internal cohesion. Each business domain is encapsulated within its own module.

### Core Structure

- `main.py`: The entry point for the FastAPI application.
- `modules/`: Domain-specific logic, routers, and schemas.
    - `identity/`: User management, authentication, and permissions.
    - `market/`: Trading, analytics, and supply chain management.
    - `robotics/`: Robot specs, designs, and manufacturing state.
    - `ledger/`: Blockchain abstraction and multi-chain orchestration.
    - `notifications/`: User and system notification logic.
    - `mcp/`: **Model Context Protocol** interface for AI agents.
    - `common/`: Shared samples, responses, and cross-domain logic.
- `core/`: Shared infrastructure (Middleware, Config, Base Models).
- `utils/`: Generic utility functions and security helpers.
- `static/` & `templates/`: Assets for the API's landing page and documentation.

## Key Principles

1. **Domain Encapsulation**: Each module is self-contained. Services and Schemas should be imported from their respective modules using relative imports.
2. **Blockchain Abstraction**: The `ledger` module provides a unified interface for blockchain operations (initially focusing on XRPL).
3. **Agent-Native**: The `mcp` module allows AI agents to interact with the platform using the Model Context Protocol.

## Running the Application

From the `application_layer` directory:
```bash
PYTHONPATH=app python3 -m app.main
```
or
```bash
uvicorn app.main:app --reload
```
