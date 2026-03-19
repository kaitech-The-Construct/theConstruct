from typing import Any, Dict, Optional
from .xrpl_ledger import XRPLLedger

class BlockchainService:
    """
    Orchestrates blockchain interactions by leveraging ledger-specific
    implementations through the LedgerInterface abstraction.
    """

    def __init__(self, ledger_type: str = "xrpl"):
        # For the MVP, we only support XRPL.
        # This can easily be extended to support Solana or others.
        if ledger_type == "xrpl":
            self.ledger = XRPLLedger()
        else:
            raise ValueError(f"Unsupported ledger type: {ledger_type}")

    async def create_wallet(self) -> Dict[str, Any]:
        """Creates a new wallet on the configured ledger."""
        return await self.ledger.create_account()

    async def get_account_balance(self, address: str) -> float:
        """Retrieves the balance of an address."""
        return await self.ledger.get_balance(address)

    async def mint_robot_blueprint(self, wallet: Any, metadata_uri: str) -> str:
        """Mints a robot blueprint as an NFT."""
        return await self.ledger.mint_nft(wallet, metadata_uri)

    async def execute_trade_payment(self, wallet: Any, recipient: str, amount: float) -> str:
        """Executes a payment for a trade on-chain."""
        return await self.ledger.transfer_tokens(wallet, recipient, amount)

    async def secure_manufacturing_funds(self, wallet: Any, manufacturer_address: str, amount: float) -> str:
        """Locks funds in escrow for a manufacturing order."""
        return await self.ledger.create_escrow(wallet, manufacturer_address, amount)
