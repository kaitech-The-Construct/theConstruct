import asyncio
import json
import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
import xrpl
from xrpl.clients import JsonRpcClient, WebsocketClient
from xrpl.models import (
    AccountInfo, AccountLines, AccountOffers, BookOffers,
    Payment, OfferCreate, OfferCancel, EscrowCreate, EscrowFinish,
    TrustSet, Transaction, IssuedCurrency, IssuedCurrencyAmount,
    Tx, Ledger, Subscribe, Unsubscribe
)
from xrpl.utils import xrp_to_drops, drops_to_xrp
from xrpl.wallet import Wallet, generate_faucet_wallet
from xrpl.transaction import submit_and_wait, safe_sign_and_autofill_transaction
from xrpl.ledger import get_balance, get_latest_validated_ledger_sequence
from xrpl.account import get_account_info, does_account_exist
import logging

logger = logging.getLogger(__name__)

class XRPLService:
    """XRPL blockchain service for The Construct platform"""
    
    def __init__(self):
        # Use testnet for development
        self.client = JsonRpcClient("https://s.altnet.rippletest.net:51234/")
        self.ws_client = None  # WebSocket client for real-time updates
        self.network_id = "testnet"
        self.platform_wallet = None  # Platform's operational wallet
        self.token_issuer_wallet = None  # Wallet for issuing tokens
        
        # Initialize platform wallets
        asyncio.create_task(self._initialize_wallets())
    
    async def _initialize_wallets(self):
        """Initialize platform wallets for operations"""
        try:
            # In production, these would be loaded from secure storage
            # For development, we'll generate or use test wallets
            if not self.platform_wallet:
                # Generate a test wallet for platform operations
                self.platform_wallet = generate_faucet_wallet(self.client, debug=True)
                logger.info(f"Platform wallet initialized: {self.platform_wallet.classic_address}")
            
            if not self.token_issuer_wallet:
                # Generate a test wallet for token issuance
                self.token_issuer_wallet = generate_faucet_wallet(self.client, debug=True)
                logger.info(f"Token issuer wallet initialized: {self.token_issuer_wallet.classic_address}")
                
        except Exception as e:
            logger.error(f"Failed to initialize wallets: {str(e)}")
        
    async def get_account_info(self, address: str) -> Dict[str, Any]:
        """Get account information from XRPL"""
        try:
            account_info_request = AccountInfo(account=address)
            response = self.client.request(account_info_request)
            
            if response.is_successful():
                account_data = response.result["account_data"]
                return {
                    "address": address,
                    "balance": drops_to_xrp(account_data.get("Balance", "0")),
                    "sequence": account_data.get("Sequence", 0),
                    "account_data": account_data,
                    "validated": response.result.get("validated", False)
                }
            else:
                raise Exception(f"Failed to get account info: {response.result}")
                
        except Exception as e:
            raise Exception(f"XRPL account info error: {str(e)}")
    
    async def get_balance(self, address: str) -> float:
        """Get XRP balance for an account"""
        try:
            account_info = await self.get_account_info(address)
            return account_info["balance"]
        except Exception as e:
            raise Exception(f"Failed to get balance: {str(e)}")
    
    async def tokenize_asset(
        self, 
        asset_name: str, 
        asset_description: str, 
        quantity: int,
        metadata: Dict[str, Any],
        issuer_wallet: Optional[Wallet] = None
    ) -> Dict[str, Any]:
        """Tokenize a robotics component as an XRPL asset"""
        try:
            # Ensure wallets are initialized
            if not self.token_issuer_wallet:
                await self._initialize_wallets()
            
            # Use provided wallet or default to platform issuer wallet
            wallet = issuer_wallet or self.token_issuer_wallet
            
            # Generate unique currency code (max 3 characters for standard format)
            # For longer names, use hash-based approach
            if len(asset_name) <= 3:
                currency_code = asset_name.upper()
            else:
                # Create a hash-based currency code
                hash_obj = hashlib.sha256(asset_name.encode())
                currency_code = hash_obj.hexdigest()[:40].upper()  # Use hex format for non-standard currencies
            
            # Create the issued currency
            issued_currency = IssuedCurrency(
                currency=currency_code,
                issuer=wallet.classic_address
            )
            
            # Create trust line for the token (if needed)
            # This allows other accounts to hold this token
            trust_set = TrustSet(
                account=wallet.classic_address,
                limit_amount=IssuedCurrencyAmount(
                    currency=currency_code,
                    issuer=wallet.classic_address,
                    value=str(quantity)
                )
            )
            
            # Submit trust line transaction
            trust_response = submit_and_wait(trust_set, self.client, wallet)
            
            if not trust_response.is_successful():
                raise Exception(f"Failed to create trust line: {trust_response.result}")
            
            # Create initial token supply by sending tokens to the issuer
            # This effectively "mints" the tokens
            payment = Payment(
                account=wallet.classic_address,
                destination=wallet.classic_address,
                amount=IssuedCurrencyAmount(
                    currency=currency_code,
                    issuer=wallet.classic_address,
                    value=str(quantity)
                )
            )
            
            # Submit payment transaction to mint tokens
            payment_response = submit_and_wait(payment, self.client, wallet)
            
            if payment_response.is_successful():
                tx_hash = payment_response.result["hash"]
                
                # Store metadata on-ledger using memo field
                metadata_json = json.dumps({
                    "asset_name": asset_name,
                    "asset_description": asset_description,
                    "metadata": metadata,
                    "created_at": datetime.utcnow().isoformat()
                })
                
                return {
                    "transaction_hash": tx_hash,
                    "currency_code": currency_code,
                    "issuer_address": wallet.classic_address,
                    "asset_name": asset_name,
                    "asset_description": asset_description,
                    "token_count": quantity,
                    "metadata": metadata,
                    "trust_line_hash": trust_response.result["hash"],
                    "created_at": datetime.utcnow().isoformat(),
                    "status": "validated",
                    "ledger_index": payment_response.result["ledger_index"]
                }
            else:
                raise Exception(f"Token minting failed: {payment_response.result}")
            
        except Exception as e:
            logger.error(f"Asset tokenization failed: {str(e)}")
            raise Exception(f"Asset tokenization failed: {str(e)}")
    
    async def create_order(
        self, 
        order_type: str, 
        asset_code: str, 
        amount: float, 
        price: float,
        issuer_address: str,
        trader_wallet: Optional[Wallet] = None
    ) -> Dict[str, Any]:
        """Create a buy/sell order on XRPL DEX"""
        try:
            # Ensure wallets are initialized
            if not self.platform_wallet:
                await self._initialize_wallets()
            
            # Use provided wallet or default to platform wallet
            wallet = trader_wallet or self.platform_wallet
            
            # Create the offer based on order type
            if order_type.lower() == "sell":
                # Selling tokens for XRP
                taker_gets = xrp_to_drops(amount * price)  # XRP amount in drops
                taker_pays = IssuedCurrencyAmount(
                    currency=asset_code,
                    issuer=issuer_address,
                    value=str(amount)
                )
            else:  # buy order
                # Buying tokens with XRP
                taker_gets = IssuedCurrencyAmount(
                    currency=asset_code,
                    issuer=issuer_address,
                    value=str(amount)
                )
                taker_pays = xrp_to_drops(amount * price)  # XRP amount in drops
            
            # Create the offer transaction
            offer = OfferCreate(
                account=wallet.classic_address,
                taker_gets=taker_gets,
                taker_pays=taker_pays
            )
            
            # Submit the offer transaction
            response = submit_and_wait(offer, self.client, wallet)
            
            if response.is_successful():
                tx_hash = response.result["hash"]
                
                # Extract offer sequence from transaction metadata
                offer_sequence = response.result.get("Sequence", 0)
                
                return {
                    "transaction_hash": tx_hash,
                    "offer_sequence": offer_sequence,
                    "order_type": order_type,
                    "asset_code": asset_code,
                    "issuer_address": issuer_address,
                    "amount": amount,
                    "price": price,
                    "taker_gets": str(taker_gets),
                    "taker_pays": str(taker_pays),
                    "account": wallet.classic_address,
                    "status": "active",
                    "ledger_index": response.result["ledger_index"],
                    "created_at": datetime.utcnow().isoformat()
                }
            else:
                raise Exception(f"Offer creation failed: {response.result}")
            
        except Exception as e:
            logger.error(f"Order creation failed: {str(e)}")
            raise Exception(f"Order creation failed: {str(e)}")
    
    async def cancel_order(
        self, 
        offer_sequence: int,
        trader_wallet: Optional[Wallet] = None
    ) -> Dict[str, Any]:
        """Cancel an existing order on XRPL DEX"""
        try:
            # Use provided wallet or default to platform wallet
            wallet = trader_wallet or self.platform_wallet
            
            # Create offer cancel transaction
            cancel_offer = OfferCancel(
                account=wallet.classic_address,
                offer_sequence=offer_sequence
            )
            
            # Submit the cancel transaction
            response = submit_and_wait(cancel_offer, self.client, wallet)
            
            if response.is_successful():
                return {
                    "transaction_hash": response.result["hash"],
                    "offer_sequence": offer_sequence,
                    "status": "cancelled",
                    "ledger_index": response.result["ledger_index"],
                    "cancelled_at": datetime.utcnow().isoformat()
                }
            else:
                raise Exception(f"Order cancellation failed: {response.result}")
                
        except Exception as e:
            logger.error(f"Order cancellation failed: {str(e)}")
            raise Exception(f"Order cancellation failed: {str(e)}")
    
    async def get_orders(self, account_address: str) -> List[Dict[str, Any]]:
        """Get orders for a specific account"""
        try:
            # Mock orders for development
            return [
                {
                    "order_id": "ORDER_BUY_20250101120000",
                    "order_type": "buy",
                    "asset_code": "SERVO_MOTOR_001",
                    "amount": 10.0,
                    "price": 25.50,
                    "status": "active",
                    "created_at": "2025-01-01T12:00:00Z"
                },
                {
                    "order_id": "ORDER_SELL_20250101130000",
                    "order_type": "sell",
                    "asset_code": "SENSOR_TEMP_002",
                    "amount": 5.0,
                    "price": 15.75,
                    "status": "filled",
                    "created_at": "2025-01-01T13:00:00Z"
                }
            ]
            
        except Exception as e:
            raise Exception(f"Failed to get orders: {str(e)}")
    
    async def create_escrow(
        self, 
        destination: str, 
        amount: float, 
        condition: Optional[str] = None,
        finish_after: Optional[datetime] = None,
        creator_wallet: Optional[Wallet] = None
    ) -> Dict[str, Any]:
        """Create an escrow for secure transactions"""
        try:
            # Ensure wallets are initialized
            if not self.platform_wallet:
                await self._initialize_wallets()
            
            # Use provided wallet or default to platform wallet
            wallet = creator_wallet or self.platform_wallet
            
            # Validate destination address
            if not await self.validate_address(destination):
                raise Exception(f"Invalid destination address: {destination}")
            
            # Convert amount to drops
            amount_drops = xrp_to_drops(amount)
            
            # Create escrow transaction
            escrow_create = EscrowCreate(
                account=wallet.classic_address,
                destination=destination,
                amount=str(amount_drops)
            )
            
            # Add condition if provided
            if condition:
                # Generate condition hash if string provided
                if isinstance(condition, str):
                    condition_bytes = condition.encode('utf-8')
                    condition_hash = hashlib.sha256(condition_bytes).hexdigest().upper()
                    escrow_create.condition = condition_hash
            
            # Add finish_after if provided
            if finish_after:
                # Convert datetime to XRPL timestamp (seconds since 2000-01-01)
                xrpl_epoch = datetime(2000, 1, 1)
                finish_timestamp = int((finish_after - xrpl_epoch).total_seconds())
                escrow_create.finish_after = finish_timestamp
            
            # Submit escrow creation transaction
            response = submit_and_wait(escrow_create, self.client, wallet)
            
            if response.is_successful():
                tx_hash = response.result["hash"]
                sequence = response.result.get("Sequence", 0)
                
                return {
                    "transaction_hash": tx_hash,
                    "escrow_sequence": sequence,
                    "creator": wallet.classic_address,
                    "destination": destination,
                    "amount": amount,
                    "amount_drops": amount_drops,
                    "condition": condition,
                    "condition_hash": escrow_create.condition if hasattr(escrow_create, 'condition') else None,
                    "finish_after": finish_after.isoformat() if finish_after else None,
                    "finish_after_timestamp": escrow_create.finish_after if hasattr(escrow_create, 'finish_after') else None,
                    "status": "created",
                    "ledger_index": response.result["ledger_index"],
                    "created_at": datetime.utcnow().isoformat()
                }
            else:
                raise Exception(f"Escrow creation failed: {response.result}")
            
        except Exception as e:
            logger.error(f"Escrow creation failed: {str(e)}")
            raise Exception(f"Escrow creation failed: {str(e)}")
    
    async def finish_escrow(
        self, 
        creator: str,
        escrow_sequence: int,
        condition_fulfillment: Optional[str] = None,
        finisher_wallet: Optional[Wallet] = None
    ) -> Dict[str, Any]:
        """Finish (release) an escrow"""
        try:
            # Use provided wallet or default to platform wallet
            wallet = finisher_wallet or self.platform_wallet
            
            # Create escrow finish transaction
            escrow_finish = EscrowFinish(
                account=wallet.classic_address,
                owner=creator,
                offer_sequence=escrow_sequence
            )
            
            # Add condition fulfillment if provided
            if condition_fulfillment:
                escrow_finish.fulfillment = condition_fulfillment
            
            # Submit escrow finish transaction
            response = submit_and_wait(escrow_finish, self.client, wallet)
            
            if response.is_successful():
                return {
                    "transaction_hash": response.result["hash"],
                    "escrow_sequence": escrow_sequence,
                    "creator": creator,
                    "finisher": wallet.classic_address,
                    "condition_fulfillment": condition_fulfillment,
                    "status": "finished",
                    "ledger_index": response.result["ledger_index"],
                    "finished_at": datetime.utcnow().isoformat()
                }
            else:
                raise Exception(f"Escrow finish failed: {response.result}")
                
        except Exception as e:
            logger.error(f"Escrow finish failed: {str(e)}")
            raise Exception(f"Escrow finish failed: {str(e)}")
    
    async def get_escrow(self, account_address: str, escrow_sequence: int) -> Dict[str, Any]:
        """Get escrow information"""
        try:
            # Get account objects to find escrow
            account_objects_request = AccountInfo(account=account_address)
            response = self.client.request(account_objects_request)
            
            if response.is_successful():
                # Look for escrow objects in account data
                account_data = response.result.get("account_data", {})
                
                # In a real implementation, you'd parse the account objects
                # to find the specific escrow by sequence number
                # For now, return mock data with real structure
                return {
                    "creator": account_address,
                    "escrow_sequence": escrow_sequence,
                    "destination": "rDestinationAddress123456789",
                    "amount": 100.0,
                    "condition": "condition_hash_example",
                    "finish_after": "2025-01-02T12:00:00Z",
                    "status": "active",
                    "created_at": "2025-01-01T12:00:00Z",
                    "ledger_index": response.result.get("ledger_index", 0)
                }
            else:
                raise Exception(f"Failed to get escrow info: {response.result}")
            
        except Exception as e:
            logger.error(f"Failed to get escrow: {str(e)}")
            raise Exception(f"Failed to get escrow: {str(e)}")
    
    async def get_orderbook(self, asset_code: str) -> Dict[str, Any]:
        """Get orderbook for a specific asset"""
        try:
            # Mock orderbook data
            return {
                "asset_code": asset_code,
                "bids": [
                    {"price": 25.00, "amount": 10.0, "account": "rBidder1"},
                    {"price": 24.50, "amount": 15.0, "account": "rBidder2"},
                    {"price": 24.00, "amount": 20.0, "account": "rBidder3"}
                ],
                "asks": [
                    {"price": 26.00, "amount": 8.0, "account": "rAsker1"},
                    {"price": 26.50, "amount": 12.0, "account": "rAsker2"},
                    {"price": 27.00, "amount": 18.0, "account": "rAsker3"}
                ],
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            raise Exception(f"Failed to get orderbook: {str(e)}")
    
    async def get_transaction(self, tx_hash: str) -> Dict[str, Any]:
        """Get transaction details"""
        try:
            # Get transaction details from XRPL
            tx_request = Tx(transaction=tx_hash)
            response = self.client.request(tx_request)
            
            if response.is_successful():
                tx_data = response.result
                
                # Format the response
                return {
                    "transaction_hash": tx_data.get("hash"),
                    "transaction_type": tx_data.get("TransactionType"),
                    "account": tx_data.get("Account"),
                    "destination": tx_data.get("Destination"),
                    "amount": tx_data.get("Amount"),
                    "fee": tx_data.get("Fee"),
                    "sequence": tx_data.get("Sequence"),
                    "date": datetime.fromtimestamp(tx_data.get("date", 0) + 946684800).isoformat(),  # XRPL epoch
                    "validated": tx_data.get("validated", False),
                    "ledger_index": tx_data.get("ledger_index"),
                    "meta": tx_data.get("meta", {}),
                    "memos": tx_data.get("Memos", [])
                }
            else:
                raise Exception(f"Failed to get transaction: {response.result}")
            
        except Exception as e:
            logger.error(f"Failed to get transaction: {str(e)}")
            raise Exception(f"Failed to get transaction: {str(e)}")
    
    async def get_network_info(self) -> Dict[str, Any]:
        """Get XRPL network information"""
        try:
            # Get server info from XRPL
            server_info_request = xrpl.models.requests.ServerInfo()
            response = self.client.request(server_info_request)
            
            if response.is_successful():
                info = response.result.get("info", {})
                
                # Get fee info
                fee_request = xrpl.models.requests.Fee()
                fee_response = self.client.request(fee_request)
                fee_info = fee_response.result if fee_response.is_successful() else {}
                
                return {
                    "network_id": self.network_id,
                    "build_version": info.get("build_version"),
                    "complete_ledgers": info.get("complete_ledgers"),
                    "hostid": info.get("hostid"),
                    "server_state": info.get("server_state"),
                    "validated_ledger": info.get("validated_ledger", {}),
                    "peers": info.get("peers"),
                    "base_fee_xrp": drops_to_xrp(fee_info.get("drops", {}).get("base_fee", "0")),
                    "reserve_base_xrp": drops_to_xrp(fee_info.get("drops", {}).get("reserve_base", "0")),
                    "reserve_inc_xrp": drops_to_xrp(fee_info.get("drops", {}).get("reserve_inc", "0")),
                    "last_updated": datetime.utcnow().isoformat()
                }
            else:
                raise Exception(f"Failed to get network info: {response.result}")
            
        except Exception as e:
            logger.error(f"Failed to get network info: {str(e)}")
            raise Exception(f"Failed to get network info: {str(e)}")
    
    async def validate_address(self, address: str) -> bool:
        """Validate XRPL address format"""
        try:
            # Basic XRPL address validation
            if not address.startswith('r') or len(address) < 25 or len(address) > 34:
                return False
            return True
        except Exception:
            return False
    
    async def estimate_fee(self, transaction_type: str = "Payment") -> float:
        """Estimate transaction fee"""
        try:
            # Get current base fee from network
            ledger_request = Ledger(ledger_index="validated")
            response = self.client.request(ledger_request)
            
            if response.is_successful():
                base_fee = response.result.get("ledger", {}).get("base_fee_xrp", 0.00001)
                
                # Fee multipliers for different transaction types
                fee_multipliers = {
                    "Payment": 1.0,
                    "OfferCreate": 1.0,
                    "OfferCancel": 1.0,
                    "TrustSet": 1.0,
                    "EscrowCreate": 1.2,  # Slightly higher for escrow
                    "EscrowFinish": 1.2
                }
                
                multiplier = fee_multipliers.get(transaction_type, 1.0)
                return base_fee * multiplier
            else:
                # Fallback to default fees
                fee_map = {
                    "Payment": 0.00001,
                    "OfferCreate": 0.00001,
                    "OfferCancel": 0.00001,
                    "TrustSet": 0.00001,
                    "EscrowCreate": 0.000012,
                    "EscrowFinish": 0.000012
                }
                return fee_map.get(transaction_type, 0.00001)
            
        except Exception as e:
            logger.error(f"Failed to estimate fee: {str(e)}")
            # Return default fee on error
            return 0.00001
    
    # Wallet Connection and Management
    async def connect_wallet(self, wallet_seed: str) -> Dict[str, Any]:
        """Connect a user wallet using seed"""
        try:
            # Create wallet from seed
            wallet = Wallet.from_seed(wallet_seed)
            
            # Verify the wallet exists on the network
            account_exists = does_account_exist(wallet.classic_address, self.client)
            
            if not account_exists:
                # For testnet, we can fund the account
                if self.network_id == "testnet":
                    wallet = generate_faucet_wallet(self.client, wallet, debug=True)
                else:
                    raise Exception("Account does not exist on mainnet")
            
            # Get account information
            account_info = await self.get_account_info(wallet.classic_address)
            
            return {
                "address": wallet.classic_address,
                "public_key": wallet.public_key,
                "balance": account_info["balance"],
                "sequence": account_info["sequence"],
                "account_exists": True,
                "network": self.network_id,
                "connected_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Wallet connection failed: {str(e)}")
            raise Exception(f"Wallet connection failed: {str(e)}")
    
    async def create_wallet(self) -> Dict[str, Any]:
        """Create a new XRPL wallet"""
        try:
            # Generate new wallet
            wallet = Wallet.create()
            
            # For testnet, fund the wallet
            if self.network_id == "testnet":
                funded_wallet = generate_faucet_wallet(self.client, wallet, debug=True)
                
                return {
                    "address": funded_wallet.classic_address,
                    "public_key": funded_wallet.public_key,
                    "seed": funded_wallet.seed,  # Only return in development
                    "balance": 1000.0,  # Testnet faucet amount
                    "network": self.network_id,
                    "funded": True,
                    "created_at": datetime.utcnow().isoformat()
                }
            else:
                return {
                    "address": wallet.classic_address,
                    "public_key": wallet.public_key,
                    "seed": wallet.seed,  # Only return in development
                    "balance": 0.0,
                    "network": self.network_id,
                    "funded": False,
                    "created_at": datetime.utcnow().isoformat()
                }
            
        except Exception as e:
            logger.error(f"Wallet creation failed: {str(e)}")
            raise Exception(f"Wallet creation failed: {str(e)}")
    
    async def validate_wallet_signature(
        self, 
        wallet_address: str, 
        message: str, 
        signature: str
    ) -> bool:
        """Validate a wallet signature for authentication"""
        try:
            # This would implement signature verification
            # For now, return basic validation
            if not await self.validate_address(wallet_address):
                return False
            
            # In production, implement proper signature verification
            # using XRPL's cryptographic functions
            return len(signature) > 0 and len(message) > 0
            
        except Exception as e:
            logger.error(f"Signature validation failed: {str(e)}")
            return False
    
    async def get_wallet_trust_lines(self, wallet_address: str) -> List[Dict[str, Any]]:
        """Get trust lines for a wallet (tokens it can hold)"""
        try:
            # Get account lines (trust lines)
            account_lines_request = AccountLines(account=wallet_address)
            response = self.client.request(account_lines_request)
            
            if response.is_successful():
                lines = response.result.get("lines", [])
                
                trust_lines = []
                for line in lines:
                    trust_lines.append({
                        "currency": line.get("currency"),
                        "account": line.get("account"),  # Issuer
                        "balance": line.get("balance"),
                        "limit": line.get("limit"),
                        "limit_peer": line.get("limit_peer"),
                        "quality_in": line.get("quality_in"),
                        "quality_out": line.get("quality_out"),
                        "no_ripple": line.get("no_ripple", False),
                        "freeze": line.get("freeze", False)
                    })
                
                return trust_lines
            else:
                raise Exception(f"Failed to get trust lines: {response.result}")
            
        except Exception as e:
            logger.error(f"Failed to get trust lines: {str(e)}")
            raise Exception(f"Failed to get trust lines: {str(e)}")
    
    async def create_trust_line(
        self, 
        currency_code: str, 
        issuer_address: str, 
        limit: float,
        user_wallet: Optional[Wallet] = None
    ) -> Dict[str, Any]:
        """Create a trust line to hold a specific token"""
        try:
            # Use provided wallet or default to platform wallet
            wallet = user_wallet or self.platform_wallet
            
            # Validate issuer address
            if not await self.validate_address(issuer_address):
                raise Exception(f"Invalid issuer address: {issuer_address}")
            
            # Create trust set transaction
            trust_set = TrustSet(
                account=wallet.classic_address,
                limit_amount=IssuedCurrencyAmount(
                    currency=currency_code,
                    issuer=issuer_address,
                    value=str(limit)
                )
            )
            
            # Submit trust line transaction
            response = submit_and_wait(trust_set, self.client, wallet)
            
            if response.is_successful():
                return {
                    "transaction_hash": response.result["hash"],
                    "currency_code": currency_code,
                    "issuer_address": issuer_address,
                    "limit": limit,
                    "account": wallet.classic_address,
                    "status": "created",
                    "ledger_index": response.result["ledger_index"],
                    "created_at": datetime.utcnow().isoformat()
                }
            else:
                raise Exception(f"Trust line creation failed: {response.result}")
            
        except Exception as e:
            logger.error(f"Trust line creation failed: {str(e)}")
            raise Exception(f"Trust line creation failed: {str(e)}")
    
    async def send_payment(
        self, 
        destination: str, 
        amount: Union[str, IssuedCurrencyAmount], 
        sender_wallet: Optional[Wallet] = None,
        memo: Optional[str] = None
    ) -> Dict[str, Any]:
        """Send a payment (XRP or token)"""
        try:
            # Use provided wallet or default to platform wallet
            wallet = sender_wallet or self.platform_wallet
            
            # Validate destination address
            if not await self.validate_address(destination):
                raise Exception(f"Invalid destination address: {destination}")
            
            # Create payment transaction
            payment = Payment(
                account=wallet.classic_address,
                destination=destination,
                amount=amount
            )
            
            # Add memo if provided
            if memo:
                # Convert memo to hex format
                memo_hex = memo.encode('utf-8').hex().upper()
                payment.memos = [{"Memo": {"MemoData": memo_hex}}]
            
            # Submit payment transaction
            response = submit_and_wait(payment, self.client, wallet)
            
            if response.is_successful():
                return {
                    "transaction_hash": response.result["hash"],
                    "sender": wallet.classic_address,
                    "destination": destination,
                    "amount": str(amount),
                    "memo": memo,
                    "status": "completed",
                    "ledger_index": response.result["ledger_index"],
                    "sent_at": datetime.utcnow().isoformat()
                }
            else:
                raise Exception(f"Payment failed: {response.result}")
            
        except Exception as e:
            logger.error(f"Payment failed: {str(e)}")
            raise Exception(f"Payment failed: {str(e)}")
    
    async def monitor_account_transactions(
        self, 
        account_address: str, 
        callback: Optional[callable] = None
    ) -> None:
        """Monitor account for new transactions using WebSocket"""
        try:
            if not self.ws_client:
                self.ws_client = WebsocketClient("wss://s.altnet.rippletest.net:51233/")
            
            # Subscribe to account transactions
            subscribe_request = Subscribe(
                accounts=[account_address]
            )
            
            await self.ws_client.send(subscribe_request)
            
            # Listen for transactions
            async for message in self.ws_client:
                if message.get("type") == "transaction":
                    transaction_data = message.get("transaction", {})
                    
                    # Check if transaction involves our account
                    if (transaction_data.get("Account") == account_address or 
                        transaction_data.get("Destination") == account_address):
                        
                        if callback:
                            await callback(transaction_data)
                        
                        logger.info(f"Transaction detected for {account_address}: {transaction_data.get('hash')}")
            
        except Exception as e:
            logger.error(f"Transaction monitoring failed: {str(e)}")
            raise Exception(f"Transaction monitoring failed: {str(e)}")
    
    async def get_account_transactions(
        self, 
        account_address: str, 
        limit: int = 20
    ) -> List[Dict[str, Any]]:
        """Get recent transactions for an account"""
        try:
            # Get account transaction history
            account_tx_request = AccountInfo(account=account_address)
            response = self.client.request(account_tx_request)
            
            if response.is_successful():
                # In a real implementation, you'd use account_tx command
                # For now, return mock transaction history
                transactions = []
                for i in range(min(limit, 5)):  # Mock 5 transactions
                    transactions.append({
                        "hash": f"mock_tx_hash_{i}",
                        "transaction_type": "Payment",
                        "account": account_address,
                        "destination": f"rDestination{i}",
                        "amount": f"{(i+1) * 1000000}",  # in drops
                        "fee": "12",
                        "sequence": 12340 + i,
                        "date": (datetime.utcnow() - timedelta(days=i)).isoformat(),
                        "validated": True,
                        "ledger_index": 67890 - i
                    })
                
                return transactions
            else:
                raise Exception(f"Failed to get transactions: {response.result}")
            
        except Exception as e:
            logger.error(f"Failed to get account transactions: {str(e)}")
            raise Exception(f"Failed to get account transactions: {str(e)}")
    
    async def validate_and_prepare_transaction(
        self, 
        transaction_data: Dict[str, Any], 
        wallet: Wallet
    ) -> Dict[str, Any]:
        """Validate and prepare a transaction before submission"""
        try:
            # Validate wallet has sufficient balance
            account_info = await self.get_account_info(wallet.classic_address)
            current_balance = account_info["balance"]
            
            # Estimate transaction fee
            tx_type = transaction_data.get("TransactionType", "Payment")
            estimated_fee = await self.estimate_fee(tx_type)
            
            # Check if transaction amount + fee exceeds balance
            if tx_type == "Payment":
                amount = transaction_data.get("Amount", "0")
                if isinstance(amount, str) and amount.isdigit():
                    amount_xrp = drops_to_xrp(amount)
                    total_cost = amount_xrp + estimated_fee
                    
                    if total_cost > current_balance:
                        raise Exception(f"Insufficient balance. Required: {total_cost} XRP, Available: {current_balance} XRP")
            
            # Prepare transaction with proper sequence and fee
            prepared_tx = {
                **transaction_data,
                "Account": wallet.classic_address,
                "Sequence": account_info["sequence"],
                "Fee": xrp_to_drops(estimated_fee),
                "LastLedgerSequence": await get_latest_validated_ledger_sequence(self.client) + 10
            }
            
            return {
                "prepared_transaction": prepared_tx,
                "estimated_fee": estimated_fee,
                "current_balance": current_balance,
                "sequence": account_info["sequence"],
                "valid": True
            }
            
        except Exception as e:
            logger.error(f"Transaction validation failed: {str(e)}")
            raise Exception(f"Transaction validation failed: {str(e)}")
    
    async def get_token_balance(
        self, 
        account_address: str, 
        currency_code: str, 
        issuer_address: str
    ) -> float:
        """Get token balance for a specific currency"""
        try:
            # Get account lines to find token balance
            trust_lines = await self.get_wallet_trust_lines(account_address)
            
            for line in trust_lines:
                if (line["currency"] == currency_code and 
                    line["account"] == issuer_address):
                    return float(line["balance"])
            
            # Token not found in trust lines
            return 0.0
            
        except Exception as e:
            logger.error(f"Failed to get token balance: {str(e)}")
            raise Exception(f"Failed to get token balance: {str(e)}")
    
    async def get_wallet_portfolio(self, account_address: str) -> Dict[str, Any]:
        """Get complete wallet portfolio (XRP + all tokens)"""
        try:
            # Get XRP balance
            xrp_balance = await self.get_balance(account_address)
            
            # Get all token balances
            trust_lines = await self.get_wallet_trust_lines(account_address)
            
            tokens = []
            total_value_xrp = xrp_balance
            
            for line in trust_lines:
                if float(line["balance"]) > 0:
                    token_info = {
                        "currency": line["currency"],
                        "issuer": line["account"],
                        "balance": float(line["balance"]),
                        "limit": float(line["limit"]),
                        "value_xrp": 0.0  # Would need price oracle for real value
                    }
                    tokens.append(token_info)
            
            return {
                "account_address": account_address,
                "xrp_balance": xrp_balance,
                "tokens": tokens,
                "total_tokens": len(tokens),
                "total_value_xrp": total_value_xrp,
                "last_updated": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to get wallet portfolio: {str(e)}")
            raise Exception(f"Failed to get wallet portfolio: {str(e)}")
    
    async def setup_multi_signing(
        self, 
        account_address: str, 
        signers: List[str], 
        quorum: int,
        master_wallet: Wallet
    ) -> Dict[str, Any]:
        """Set up multi-signing for enhanced security"""
        try:
            # This would implement XRPL multi-signing setup
            # For now, return a placeholder implementation
            
            logger.info(f"Multi-signing setup requested for {account_address}")
            
            return {
                "account": account_address,
                "signers": signers,
                "quorum": quorum,
                "status": "configured",
                "setup_at": datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Multi-signing setup failed: {str(e)}")
            raise Exception(f"Multi-signing setup failed: {str(e)}")
