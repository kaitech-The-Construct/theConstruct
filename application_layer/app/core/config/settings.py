# core/config/settings.py

import os
from pydantic_settings import BaseSettings
from google.cloud import secretmanager

# Initialize the Secret Manager client
client = secretmanager.SecretManagerServiceClient()


# Function to access secret from GCP Secrets Manager
def get_secret(name: str) -> str:
    """Get Secret"""

    project_id = os.environ.get("PROJECTID")
    secret_name = f"projects/{project_id}/secrets/{name}/versions/latest"
    response = client.access_secret_version(name=secret_name)
    # Decode payload and convert to a `str`
    return response.payload.data.decode("UTF-8")


# Application settings using secrets from GCP Secrets Manager
class Settings(BaseSettings):
    """Settings"""

    PROJECT_NAME: str = "The Construct DEX"
    PROJECT_VERSION: str = "1.0.0"
    API_PREFIX: str = "/api"

    # Injective 
    INJECTIVE_RPC_ENDPOINT_TESTNET: str = "https://testnet.sentry.tm.injective.network:443"
    INJECTIVE_RPC_ENDPOINT_MAINNET: str ="https://sentry.tm.injective.network:443"
    
    # Solana
    SOLANA_RPC_ENDPOINT_MAINNET: str = "https://api.mainnet-beta.solana.com"
    SOLANA_RPC_ENDPOINT_DEVNET: str = "https://api.devnet.solana.com"
    SOLANA_RPC_ENDPOINT_TESTNET: str = "https://api.testnet.solana.com"

    # Secrets retrieved from GCP Secrets Manager
    # DATABASE_URL: str = get_secret("database_url")
    DATABASE_URL: str = os.getenv("DATABASE_URL", "database.db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    FIREBASE_API_KEY: str = os.getenv("FIREBASE_API_KEY", "")

    # CORS settings
    ALLOWED_HOSTS: list = os.getenv("ALLOWED_HOSTS", "http://localhost:5173,http://localhost:8000,http://127.0.0.1:5173").split(",")

    ENVIR: str = "test" # options: test, stage, production. Changes firestore database
    
    class Config:
        """Config"""

        case_sensitive = True


settings = Settings()
