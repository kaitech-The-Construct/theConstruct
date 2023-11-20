# The Construct DEX Application Layer

Welcome to the repository for the Application Layer of The Construct, a groundbreaking DEX platform for robotics and AI - powered by blockchain technology.

## Overview

This directory contains the FastAPI application that acts as the backend for The Construct platform. It handles API requests for robot and software marketplace transactions, user management, as well as blockchain interactions.

## Prerequisites

Before running the FastAPI server, you will need:

- Python 3.8+
- [Pipenv](https://pipenv.pypa.io/en/latest/) for dependency management

## Project Structure

The project is structured as follows:

- `/api` - Contains definitions for the API routes, dependencies, and common responses.
- `/core` - Holds the core business logic, service layer, and database management.
- `/schemas` - Pydantic models for validating and serializing data.
- `/utils` - Utility functions and common helpers for the application.
- `main.py` - The entry point for the FastAPI application.

## Installation

To set up your development environment, follow these steps:

1. Clone the repository:

    ```bash
    git clone ...
    ```

2. Navigate to the application layer directory:

    ```bash
    cd path/to/app
    ```

3. Install dependencies using Pipenv:

    ```bash
    pipenv install
    ```

## Running the Server

To start the FastAPI server, run:

```bash
pipenv run uvicorn main:app --reload