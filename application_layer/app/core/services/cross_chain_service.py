# core/services/cross_chain_service.py

from typing import List, Optional
import hashlib

from core.config.settings import settings
from core.services.blockchain_service import BlockchainService
from google.cloud import firestore


class CrossChainService:
    def __init__(self):
        self.blockchain_service = BlockchainService()
        self.db = firestore.Client()
        self.bridges_collection = self.db.collection(f"{settings.ENVIR}_asset_bridges")
        self.portfolios_collection = self.db.collection(f"{settings.ENVIR}_portfolios")

    def bridge_assets(self, source_chain: str, target_chain: str, asset_data: dict) -> dict:
        """Bridge assets between chains"""
        try:
            # Generate bridge ID
            bridge_id = f"BRIDGE{hashlib.md5(f"{source_chain}{target_chain}{asset_data}".encode()).hexdigest()[:8].upper()}"
            
            # Validate supported chains
            supported_chains = ["xrpl", "solana"]
            if source_chain not in supported_chains or target_chain not in supported_chains:
                return {"success": False, "message": "Unsupported chain"}
            
            # Store bridge record
            bridge_record = {
                "bridge_id": bridge_id,
                "source_chain": source_chain,
                "target_chain": target_chain,
                "asset_data": asset_data,
                "status": "pending",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.bridges_collection.add(bridge_record)
            
            # Simulate bridge processing
            # In a real implementation, this would involve:
            # 1. Locking assets on source chain
            # 2. Minting wrapped assets on target chain
            # 3. Updating bridge status
            
            return {
                "success": True, 
                "bridge_id": bridge_id,
                "source_chain": source_chain,
                "target_chain": target_chain,
                "status": "pending"
            }
        except Exception as exc:
            print(f"Error bridging assets: {exc}")
            return {"success": False, "message": "Asset bridging failed"}

    def aggregate_portfolio(self, user_address: str) -> dict:
        """Aggregate user portfolio across chains"""
        try:
            # Get XRPL transactions
            xrpl_transactions = self.blockchain_service.monitor_transactions(user_address)
            
            # Get Solana reputation (as a proxy for activity)
            solana_reputation = self.blockchain_service.track_reputation_score(user_address)
            
            # Calculate portfolio summary
            portfolio_data = {
                "user_address": user_address,
                "chains": {
                    "xrpl": {
                        "address": user_address,
                        "transaction_count": len(xrpl_transactions),
                        "recent_transactions": xrpl_transactions[:5],  # Last 5 transactions
                        "status": "active" if xrpl_transactions else "inactive"
                    },
                    "solana": {
                        "address": user_address,
                        "reputation_score": solana_reputation.get("reputation_score", 0),
                        "total_transactions": solana_reputation.get("total_transactions", 0),
                        "success_rate": solana_reputation.get("success_rate", 100),
                        "status": "active" if solana_reputation.get("total_transactions", 0) > 0 else "inactive"
                    }
                },
                "summary": {
                    "total_chains": 2,
                    "active_chains": sum([
                        1 if len(xrpl_transactions) > 0 else 0,
                        1 if solana_reputation.get("total_transactions", 0) > 0 else 0
                    ]),
                    "total_transactions": len(xrpl_transactions) + solana_reputation.get("total_transactions", 0)
                }
            }
            
            # Store/update portfolio record
            portfolio_record = {
                "user_address": user_address,
                "portfolio_data": portfolio_data,
                "last_updated": firestore.SERVER_TIMESTAMP
            }
            
            # Check if portfolio exists
            existing_portfolio = self.portfolios_collection.where("user_address", "==", user_address).limit(1).stream()
            existing_docs = list(existing_portfolio)
            
            if existing_docs:
                # Update existing portfolio
                existing_docs[0].reference.update(portfolio_record)
            else:
                # Create new portfolio
                self.portfolios_collection.add(portfolio_record)
            
            return {
                "success": True,
                "portfolio": portfolio_data
            }
        except Exception as exc:
            print(f"Error aggregating portfolio: {exc}")
            return {"success": False, "message": "Portfolio aggregation failed"}

    def sync_transaction_history(self, user_id: str) -> List[dict]:
        """Sync transaction history across chains"""
        try:
            transaction_history = []
            
            # Get XRPL transactions
            xrpl_transactions = self.blockchain_service.monitor_transactions(user_id)
            for tx in xrpl_transactions:
                transaction_history.append({
                    "chain": "xrpl",
                    "transaction_hash": tx.get("transaction_hash"),
                    "status": tx.get("status"),
                    "timestamp": tx.get("timestamp"),
                    "type": "trade"
                })
            
            # Get Solana contract executions
            contract_executions = self.db.collection(f"{settings.ENVIR}_contract_executions").where("params.user_id", "==", user_id).stream()
            for execution in contract_executions:
                exec_data = execution.to_dict()
                transaction_history.append({
                    "chain": "solana",
                    "execution_id": exec_data.get("execution_id"),
                    "contract_id": exec_data.get("contract_id"),
                    "function": exec_data.get("function"),
                    "status": exec_data.get("status"),
                    "timestamp": exec_data.get("executed_at"),
                    "type": "contract_execution"
                })
            
            # Get governance votes
            governance_votes = self.db.collection(f"{settings.ENVIR}_governance_votes").where("vote_data.user_id", "==", user_id).stream()
            for vote in governance_votes:
                vote_data = vote.to_dict()
                transaction_history.append({
                    "chain": "solana",
                    "vote_id": vote_data.get("vote_id"),
                    "proposal_id": vote_data.get("proposal_id"),
                    "status": vote_data.get("status"),
                    "timestamp": vote_data.get("voted_at"),
                    "type": "governance_vote"
                })
            
            # Sort by timestamp (most recent first)
            transaction_history.sort(key=lambda x: x.get("timestamp") or 0, reverse=True)
            
            return transaction_history
        except Exception as exc:
            print(f"Error syncing transaction history: {exc}")
            return []

    def validate_cross_chain_transaction(self, tx_data: dict) -> dict:
        """Validate cross-chain transaction"""
        try:
            chain = tx_data.get("chain")
            transaction_id = tx_data.get("transaction_id")
            
            if not chain or not transaction_id:
                return {"success": False, "message": "Chain and transaction ID required"}
            
            if chain == "xrpl":
                # Validate XRPL transaction
                result = self.blockchain_service.validate_payment(transaction_id)
                return {
                    "success": True,
                    "valid": result.get("valid", False),
                    "chain": "xrpl",
                    "transaction_id": transaction_id,
                    "details": result
                }
            elif chain == "solana":
                # Validate Solana transaction (check if execution exists)
                executions = self.db.collection(f"{settings.ENVIR}_contract_executions").where("execution_id", "==", transaction_id).stream()
                execution_exists = len(list(executions)) > 0
                
                return {
                    "success": True,
                    "valid": execution_exists,
                    "chain": "solana",
                    "transaction_id": transaction_id,
                    "details": {"exists": execution_exists}
                }
            else:
                return {"success": False, "message": "Unsupported chain"}
                
        except Exception as exc:
            print(f"Error validating cross-chain transaction: {exc}")
            return {"success": False, "message": "Transaction validation failed"}
