from core.config.settings import settings
from solana.rpc.api import Client
from base58 import b58encode, b58decode as b58d

solana_client = Client(settings.SOLANA_RPC_ENDPOINT_TESTNET)


class SolanaService:
    """Solana Service class"""
    def __init__(self):
        self.client = solana_client

    def get_account_info(self, pub_key: str):
        """Get account information."""
        return self.client.get_account_info(pub_key)

    def get_balance(self, pub_key: str) -> dict:
        """Get the balance of a Solana account."""
        return self.client.get_balance(pub_key)

    def get_multiple_accounts(self, pub_keys: list) -> dict:
        """Get information about multiple Solana accounts."""
        return self.client.get_multiple_accounts([pub_keys])

    def get_program_accounts(self, program_pub_key: str) -> dict:
        """Get accounts associated with a program."""
        return self.client.get_program_accounts(program_pub_key)

    def get_supply(self) -> dict:
        """Get total supply of SOL."""
        return self.client.get_supply()

    def get_token_account_balance(self, pub_key: str) -> dict:
        """Get token balance for a specific SPL Token account."""
        return self.client.get_token_account_balance(pub_key)

    def get_token_accounts_by_delegate(
        self, delegate_pub_key: str, token_mint_pub_key: str
    ) -> dict:
        """Get SPL Token accounts by delegate."""
        return self.client.get_token_accounts_by_delegate(
            delegate_pub_key, token_mint_pub_key
        )

    def get_token_accounts_by_owner(
        self, owner_pub_key: str, token_mint_pub_key: str
    ) -> dict:
        """Get SPL Token accounts by owner."""
        return self.client.get_token_accounts_by_owner(
            owner_pub_key, token_mint_pub_key
        )

    def get_token_largest_accounts(self, token_mint_pub_key: str) -> dict:
        """Get largest accounts for a specific SPL Token."""
        return self.client.get_token_largest_accounts(token_mint_pub_key)

    def get_token_supply(self, token_mint_pub_key: str) -> dict:
        """Get total supply of an SPL Token."""
        return self.client.get_token_supply(token_mint_pub_key)

    def get_transaction(self, tx_signature: str) -> dict:
        """Get details of a specific transaction by its signature."""
        return self.client.get_transaction(tx_signature)

    def get_version(self) -> dict:
        """Get the version of Solana."""
        return self.client.get_version()

    def send_transaction(self, transaction: str) -> dict:
        """Send a signed transaction."""
        return self.client.send_transaction(transaction)
