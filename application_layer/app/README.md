# Application Layer

This document provides an overview of the Application Layer for 'The Construct' DEX (Decentralized Exchange) platform, detailing the structure and responsibilities of various components within this layer.

## Structure

The Application Layer consists of several key components organized as follows:


## Responsibilities

- **API Routers**: Define the application endpoints, handle HTTP requests, and wire up service logic to corresponding routes.
- **Services**: Contain business logic for handling application operations, communicating with the database, and executing core functionalities.
- **Database Models**: Represent the application's data structure.
- **Schemas**: Pydantic models to define the structure of request and response data for validation and serialization.
- **Dependencies**: Reusable dependencies for injecting database sessions and current user information.
- **Utilities**: Functions and helpers that are commonly used across the application.

## Key Files

- `main.py`: The heart of the Application Layer, where the FastAPI `app` object is instantiated and configured.
- `core/services/*`: Individual service files where business rules and interactions are defined (e.g., `robot_service.py`).
- `core/config/settings.py`: Centralized configuration settings, including database URLs, secret keys, and other environment-specific variables.
- `core/models.py`: Models for entities such as robots, trades, users, and software.

## Usage

To start the application, run the following command from the project root directory