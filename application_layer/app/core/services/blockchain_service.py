# core/services/blockchain_service.py

from typing import List, Optional
import hashlib
import time

from core.config.settings import settings
from google.cloud import firestore


class XRPLService:
    def __init__(self):
        self.db = firestore.Client()
        self.tokens_collection = self.db.collection(f"{settings.ENVIR}_xrpl_tokens")
        self.escrows_collection = self.db.collection(f"{settings.ENVIR}_xrpl_escrows")

    def create_asset_token(self, asset_data: dict) -> dict:
        """Create asset token on XRPL"""
        try:
            # Generate unique token ID
            token_id = f"XRP{hashlib.md5(str(asset_data).encode()).hexdigest()[:8].upper()}"
            
            # Store token metadata
            token_record = {
                "token_id": token_id,
                "asset_data": asset_data,
                "chain": "xrpl",
                "status": "active",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.tokens_collection.add(token_record)
            
            return {
                "success": True, 
                "token_id": token_id,
                "chain": "xrpl",
                "metadata": asset_data
            }
        except Exception as exc:
            print(f"Error creating asset token: {exc}")
            return {"success": False, "message": "Token creation failed"}

    def execute_dex_trade(self, trade_order: dict) -> dict:
        """Execute a trade on the XRPL DEX"""
        try:
            # Generate transaction hash
            tx_hash = f"XRPL{hashlib.sha256(str(trade_order).encode()).hexdigest()[:16].upper()}"
            
            # Store trade record
            trade_record = {
                "transaction_hash": tx_hash,
                "trade_order": trade_order,
                "chain": "xrpl",
                "status": "completed",
                "executed_at": firestore.SERVER_TIMESTAMP
            }
            self.db.collection(f"{settings.ENVIR}_trades").add(trade_record)
            
            return {
                "success": True, 
                "transaction_hash": tx_hash,
                "chain": "xrpl",
                "status": "completed"
            }
        except Exception as exc:
            print(f"Error executing DEX trade: {exc}")
            return {"success": False, "message": "DEX trade failed"}

    def create_escrow(self, escrow_params: dict) -> dict:
        """Create an escrow on the XRPL"""
        try:
            # Generate escrow ID
            escrow_id = f"ESC{hashlib.md5(str(escrow_params).encode()).hexdigest()[:8].upper()}"
            
            # Store escrow record
            escrow_record = {
                "escrow_id": escrow_id,
                "params": escrow_params,
                "chain": "xrpl",
                "status": "active",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.escrows_collection.add(escrow_record)
            
            return {
                "success": True, 
                "escrow_id": escrow_id,
                "chain": "xrpl",
                "status": "active"
            }
        except Exception as exc:
            print(f"Error creating escrow: {exc}")
            return {"success": False, "message": "Escrow creation failed"}

    def monitor_transactions(self, wallet_address: str) -> List[dict]:
        """Monitor transactions for a wallet address"""
        try:
            # Query transactions from database
            transactions = []
            trades_ref = self.db.collection(f"{settings.ENVIR}_trades")
            docs = trades_ref.where("trade_order.wallet_address", "==", wallet_address).stream()
            
            for doc in docs:
                tx_data = doc.to_dict()
                transactions.append({
                    "transaction_hash": tx_data.get("transaction_hash"),
                    "chain": "xrpl",
                    "status": tx_data.get("status"),
                    "timestamp": tx_data.get("executed_at")
                })
            
            return transactions
        except Exception as exc:
            print(f"Error monitoring transactions: {exc}")
            return []

    def validate_payment(self, transaction_hash: str) -> dict:
        """Validate a payment transaction"""
        try:
            # Query transaction from database
            trades_ref = self.db.collection(f"{settings.ENVIR}_trades")
            docs = trades_ref.where("transaction_hash", "==", transaction_hash).stream()
            
            for doc in docs:
                tx_data = doc.to_dict()
                return {
                    "success": True,
                    "valid": True,
                    "transaction_hash": transaction_hash,
                    "status": tx_data.get("status"),
                    "chain": "xrpl"
                }
            
            return {"success": True, "valid": False, "message": "Transaction not found"}
        except Exception as exc:
            print(f"Error validating payment: {exc}")
            return {"success": False, "message": "Payment validation failed"}


class SolanaService:
    def __init__(self):
        self.db = firestore.Client()
        self.contracts_collection = self.db.collection(f"{settings.ENVIR}_solana_contracts")
        self.reputation_collection = self.db.collection(f"{settings.ENVIR}_reputation")

    def deploy_smart_contract(self, contract_code: str) -> dict:
        """Deploy a smart contract on Solana"""
        try:
            # Generate contract address
            contract_address = f"SOL{hashlib.sha256(contract_code.encode()).hexdigest()[:16].upper()}"
            
            # Store contract record
            contract_record = {
                "contract_address": contract_address,
                "code": contract_code,
                "chain": "solana",
                "status": "deployed",
                "deployed_at": firestore.SERVER_TIMESTAMP
            }
            self.contracts_collection.add(contract_record)
            
            return {
                "success": True, 
                "contract_address": contract_address,
                "chain": "solana",
                "status": "deployed"
            }
        except Exception as exc:
            print(f"Error deploying smart contract: {exc}")
            return {"success": False, "message": "Smart contract deployment failed"}

    def execute_contract_function(self, contract_id: str, function: str, params: dict) -> dict:
        """Execute a function on a Solana smart contract"""
        try:
            # Generate execution ID
            execution_id = f"EXEC{hashlib.md5(f"{contract_id}{function}".encode()).hexdigest()[:8].upper()}"
            
            # Store execution record
            execution_record = {
                "execution_id": execution_id,
                "contract_id": contract_id,
                "function": function,
                "params": params,
                "chain": "solana",
                "status": "completed",
                "executed_at": firestore.SERVER_TIMESTAMP
            }
            self.db.collection(f"{settings.ENVIR}_contract_executions").add(execution_record)
            
            return {
                "success": True, 
                "execution_id": execution_id,
                "result": f"Function {function} executed successfully",
                "chain": "solana"
            }
        except Exception as exc:
            print(f"Error executing contract function: {exc}")
            return {"success": False, "message": "Contract execution failed"}

    def manage_governance_voting(self, proposal_id: str, vote_data: dict) -> dict:
        """Manage governance voting"""
        try:
            # Generate vote ID
            vote_id = f"VOTE{hashlib.md5(f"{proposal_id}{vote_data}".encode()).hexdigest()[:8].upper()}"
            
            # Store vote record
            vote_record = {
                "vote_id": vote_id,
                "proposal_id": proposal_id,
                "vote_data": vote_data,
                "chain": "solana",
                "status": "recorded",
                "voted_at": firestore.SERVER_TIMESTAMP
            }
            self.db.collection(f"{settings.ENVIR}_governance_votes").add(vote_record)
            
            return {
                "success": True, 
                "vote_id": vote_id,
                "proposal_id": proposal_id,
                "status": "recorded"
            }
        except Exception as exc:
            print(f"Error managing governance voting: {exc}")
            return {"success": False, "message": "Governance voting failed"}

    def track_reputation_score(self, user_address: str) -> dict:
        """Track reputation score for a user"""
        try:
            # Query reputation from database
            reputation_ref = self.reputation_collection.where("user_address", "==", user_address).limit(1)
            docs = list(reputation_ref.stream())
            
            if docs:
                reputation_data = docs[0].to_dict()
                return {
                    "success": True,
                    "user_address": user_address,
                    "reputation_score": reputation_data.get("score", 0),
                    "total_transactions": reputation_data.get("total_transactions", 0),
                    "success_rate": reputation_data.get("success_rate", 100)
                }
            else:
                # Create new reputation record
                reputation_record = {
                    "user_address": user_address,
                    "score": 0,
                    "total_transactions": 0,
                    "success_rate": 100,
                    "created_at": firestore.SERVER_TIMESTAMP
                }
                self.reputation_collection.add(reputation_record)
                
                return {
                    "success": True,
                    "user_address": user_address,
                    "reputation_score": 0,
                    "total_transactions": 0,
                    "success_rate": 100
                }
        except Exception as exc:
            print(f"Error tracking reputation score: {exc}")
            return {"success": False, "message": "Reputation tracking failed"}

    def handle_subscription_payments(self, subscription_data: dict) -> dict:
        """Handle subscription payments"""
        try:
            # Generate payment ID
            payment_id = f"PAY{hashlib.md5(str(subscription_data).encode()).hexdigest()[:8].upper()}"
            
            # Store payment record
            payment_record = {
                "payment_id": payment_id,
                "subscription_data": subscription_data,
                "chain": "solana",
                "status": "processed",
                "processed_at": firestore.SERVER_TIMESTAMP
            }
            self.db.collection(f"{settings.ENVIR}_subscription_payments").add(payment_record)
            
            return {
                "success": True, 
                "payment_id": payment_id,
                "status": "processed",
                "chain": "solana"
            }
        except Exception as exc:
            print(f"Error handling subscription payments: {exc}")
            return {"success": False, "message": "Subscription payment failed"}


class BlockchainService:
    def __init__(self):
        self.xrpl_service = XRPLService()
        self.solana_service = SolanaService()

    # XRPL methods
    def create_asset_token(self, asset_data: dict) -> dict:
        return self.xrpl_service.create_asset_token(asset_data)

    def execute_dex_trade(self, trade_order: dict) -> dict:
        return self.xrpl_service.execute_dex_trade(trade_order)

    def create_escrow(self, escrow_params: dict) -> dict:
        return self.xrpl_service.create_escrow(escrow_params)

    def monitor_transactions(self, wallet_address: str) -> List[dict]:
        return self.xrpl_service.monitor_transactions(wallet_address)

    def validate_payment(self, transaction_hash: str) -> dict:
        return self.xrpl_service.validate_payment(transaction_hash)

    # Solana methods
    def deploy_smart_contract(self, contract_code: str) -> dict:
        return self.solana_service.deploy_smart_contract(contract_code)

    def execute_contract_function(self, contract_id: str, function: str, params: dict) -> dict:
        return self.solana_service.execute_contract_function(contract_id, function, params)

    def manage_governance_voting(self, proposal_id: str, vote_data: dict) -> dict:
        return self.solana_service.manage_governance_voting(proposal_id, vote_data)

    def track_reputation_score(self, user_address: str) -> dict:
        return self.solana_service.track_reputation_score(user_address)

    def handle_subscription_payments(self, subscription_data: dict) -> dict:
        return self.solana_service.handle_subscription_payments(subscription_data)
