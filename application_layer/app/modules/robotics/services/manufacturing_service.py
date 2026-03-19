from typing import List, Optional, Any
import hashlib

from core.config.settings import settings
from google.cloud import firestore
from ...ledger.services.blockchain_service import BlockchainService

class ManufacturingService:
    def __init__(self):
        self.db = firestore.Client()
        self.rfq_collection = self.db.collection(f"{settings.ENVIR}_rfqs")
        self.orders_collection = self.db.collection(f"{settings.ENVIR}_manufacturing_orders")
        self.qc_reports_collection = self.db.collection(f"{settings.ENVIR}_qc_reports")
        self.blockchain = BlockchainService(ledger_type="xrpl")

    def process_quote_request(self, rfq_data: dict) -> dict:
        """Process a request for quote (RFQ)"""
        try:
            rfq_id = f"RFQ{hashlib.md5(str(rfq_data).encode()).hexdigest()[:8].upper()}"
            rfq_record = {
                "rfq_id": rfq_id,
                "data": rfq_data,
                "status": "open",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.rfq_collection.add(rfq_record)
            return {"success": True, "rfq_id": rfq_id, "status": "open"}
        except Exception as exc:
            print(f"Error processing RFQ: {exc}")
            return {"success": False, "message": "RFQ processing failed"}

    def manage_manufacturing_order(self, order_data: dict) -> dict:
        """Manage a manufacturing order"""
        try:
            order_id = f"MFG{hashlib.md5(str(order_data).encode()).hexdigest()[:8].upper()}"
            order_record = {
                "order_id": order_id,
                "data": order_data,
                "status": "contracted",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.orders_collection.add(order_record)
            return {"success": True, "order_id": order_id, "status": "contracted"}
        except Exception as exc:
            print(f"Error managing manufacturing order: {exc}")
            return {"success": False, "message": "Order management failed"}

    async def process_milestone_payment(self, order_id: str, milestone_id: str, wallet: Any, buyer_id: str = None) -> dict:
        """
        Processes an on-chain payment for a completed manufacturing milestone.
        """
        try:
            order_docs = self.orders_collection.where("order_id", "==", order_id).limit(1).get()
            if not order_docs:
                return {"success": False, "message": "Order not found"}
            
            order_ref = order_docs[0].reference
            order_data = order_docs[0].to_dict()
            
            # IDOR check
            if buyer_id and order_data.get("data", {}).get("buyer_id") != buyer_id:
                return {"success": False, "message": "Unauthorized to pay for this order"}

            milestones = order_data.get("data", {}).get("contract", {}).get("milestones", [])
            
            target_milestone = next((m for m in milestones if m.get("id") == milestone_id), None)
            if not target_milestone:
                return {"success": False, "message": "Milestone not found"}
            
            if target_milestone.get("status") != "completed":
                return {"success": False, "message": "Milestone is not marked as completed"}
            
            if target_milestone.get("paid"):
                return {"success": False, "message": "Milestone already paid"}

            # Execute on-chain payment
            manufacturer_address = order_data.get("data", {}).get("manufacturer_address")
            amount = target_milestone.get("payment_amount", 0)
            
            tx_hash = await self.blockchain.execute_trade_payment(wallet, manufacturer_address, amount)
            
            # Update milestone as paid
            for m in milestones:
                if m.get("id") == milestone_id:
                    m["paid"] = True
                    m["payment_tx_hash"] = tx_hash
            
            order_ref.update({"data.contract.milestones": milestones})
            
            return {"success": True, "tx_hash": tx_hash}
        except Exception as exc:
            print(f"Error processing milestone payment: {exc}")
            return {"success": False, "message": str(exc)}

    def track_production_milestones(self, order_id: str) -> List[dict]:
        """Track production milestones for an order"""
        try:
            docs = self.orders_collection.where("order_id", "==", order_id).stream()
            for doc in docs:
                order_data = doc.to_dict().get("data", {})
                return order_data.get("contract", {}).get("milestones", [])
            return []
        except Exception as exc:
            print(f"Error tracking milestones: {exc}")
            return []

    def handle_quality_control(self, order_id: str, qc_data: dict) -> dict:
        """Handle quality control for an order"""
        try:
            qc_id = f"QC{hashlib.md5(f'{order_id}{qc_data}'.encode()).hexdigest()[:8].upper()}"
            qc_record = {
                "qc_id": qc_id,
                "order_id": order_id,
                "data": qc_data,
                "status": "completed",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.qc_reports_collection.add(qc_record)
            
            docs = self.orders_collection.where("order_id", "==", order_id).stream()
            for doc in docs:
                doc.reference.update({"status": "quality_control"})
            
            return {"success": True, "qc_id": qc_id, "status": "completed"}
        except Exception as exc:
            print(f"Error handling quality control: {exc}")
            return {"success": False, "message": "Quality control failed"}

    def manage_supplier_network(self, supplier_data: dict) -> dict:
        """Manage supplier network"""
        try:
            supplier_id = f"SUP{hashlib.md5(str(supplier_data).encode()).hexdigest()[:8].upper()}"
            supplier_record = {
                "supplier_id": supplier_id,
                "data": supplier_data,
                "status": "verified",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.db.collection(f"{settings.ENVIR}_suppliers").add(supplier_record)
            return {"success": True, "supplier_id": supplier_id, "status": "verified"}
        except Exception as exc:
            print(f"Error managing supplier network: {exc}")
            return {"success": False, "message": "Supplier management failed"}

    def get_quotes_for_rfq(self, rfq_id: str) -> List[dict]:
        """Get quotes for a specific RFQ"""
        try:
            quotes = []
            quotes_ref = self.db.collection(f"{settings.ENVIR}_quotes")
            docs = quotes_ref.where("rfq_id", "==", rfq_id).stream()
            for doc in docs:
                quote_data = doc.to_dict()
                quotes.append({
                    "quote_id": quote_data.get("quote_id"),
                    "manufacturer_id": quote_data.get("manufacturer_id"),
                    "price": quote_data.get("price"),
                    "timeline": quote_data.get("timeline")
                })
            return quotes
        except Exception as exc:
            print(f"Error getting quotes for RFQ: {exc}")
            return []

    def update_milestone_status(self, order_id: str, milestone_id: str, status: str) -> dict:
        """Update milestone status for an order"""
        try:
            docs = self.orders_collection.where("order_id", "==", order_id).stream()
            for doc in docs:
                order_data = doc.to_dict()
                milestones = order_data.get("data", {}).get("contract", {}).get("milestones", [])
                for milestone in milestones:
                    if milestone.get("id") == milestone_id:
                        milestone["status"] = status
                        if status == "completed":
                            milestone["completedAt"] = firestore.SERVER_TIMESTAMP
                doc.reference.update({"data.contract.milestones": milestones})
                return {"success": True, "milestone_id": milestone_id, "status": status}
            return {"success": False, "message": "Order not found"}
        except Exception as exc:
            print(f"Error updating milestone status: {exc}")
            return {"success": False, "message": "Milestone update failed"}
