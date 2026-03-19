from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class LedgerInterface(ABC):
    """
    Abstract Base Class for blockchain ledger interactions.
    Ensures that multiple chains (XRPL, Solana, etc.) can be supported
    via a unified interface.
    """

    @abstractmethod
    async def create_account(self) -> Dict[str, Any]:
        """Create a new account/wallet on the ledger."""
        pass

    @abstractmethod
    async def get_balance(self, address: str) -> float:
        """Get the native asset balance of an address."""
        pass

    @abstractmethod
    async def mint_nft(self, address: str, metadata_uri: str) -> str:
        """Mint a unique NFT (e.g., for a Robot Blueprint)."""
        pass

    @abstractmethod
    async def transfer_tokens(self, sender: Any, recipient: str, amount: float, asset_code: Optional[str] = None) -> str:
        """Transfer native or fungible tokens."""
        pass

    @abstractmethod
    async def create_escrow(self, sender: Any, recipient: str, amount: float, condition: Optional[str] = None) -> str:
        """Create a trustless escrow for manufacturing orders."""
        pass
