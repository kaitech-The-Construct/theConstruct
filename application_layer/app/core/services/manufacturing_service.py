# core/services/manufacturing_service.py

from typing import List, Optional
import hashlib

from core.config.settings import settings
from google.cloud import firestore


class ManufacturingService:
    def __init__(self):
        self.db = firestore.Client()
        self.rfq_collection = self.db.collection(f"{settings.ENVIR}_rfqs")
        self.orders_collection = self.db.collection(f"{settings.ENVIR}_manufacturing_orders")
        self.qc_reports_collection = self.db.collection(f"{settings.ENVIR}_qc_reports")

    def process_quote_request(self, rfq_data: dict) -> dict:
        """Process a request for quote (RFQ)"""
        try:
            # Generate RFQ ID
            rfq_id = f"RFQ{hashlib.md5(str(rfq_data).encode()).hexdigest()[:8].upper()}"
            
            # Store RFQ record
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
            # Generate order ID
            order_id = f"MFG{hashlib.md5(str(order_data).encode()).hexdigest()[:8].upper()}"
            
            # Store order record
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

    def track_production_milestones(self, order_id: str) -> List[dict]:
        """Track production milestones for an order"""
        try:
            # Query milestones from database
            milestones = []
            docs = self.orders_collection.where("order_id", "==", order_id).stream()
            
            for doc in docs:
                order_data = doc.to_dict().get("data", {})
                milestones = order_data.get("contract", {}).get("milestones", [])
                break
            
            return milestones
        except Exception as exc:
            print(f"Error tracking milestones: {exc}")
            return []

    def handle_quality_control(self, order_id: str, qc_data: dict) -> dict:
        """Handle quality control for an order"""
        try:
            # Generate QC report ID
            qc_id = f"QC{hashlib.md5(f'{order_id}{qc_data}'.encode()).hexdigest()[:8].upper()}"
            
            # Store QC report
            qc_record = {
                "qc_id": qc_id,
                "order_id": order_id,
                "data": qc_data,
                "status": "completed",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.qc_reports_collection.add(qc_record)
            
            # Update order status
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
            # Generate supplier ID
            supplier_id = f"SUP{hashlib.md5(str(supplier_data).encode()).hexdigest()[:8].upper()}"
            
            # Store supplier record
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
            # Query quotes from database
            quotes = []
            quotes_ref = self.db.collection(f"{settings.ENVIR}_quotes")
            docs = quotes_ref.where("rfq_id", "==", rfq_id).stream()
            
            for doc in docs:
                quote_data = doc.to_dict()
                quotes.append({
                    "quote_id": quote_data.get("quote_id"),
                    "manufacturer_id": quote_data.get("manufacturer_id"),
                    "price": quote_data.get("price"),
                    "timeline": quote_data.get("timeline"),
                    "capabilities": quote_data.get("capabilities", []),
                    "certifications": quote_data.get("certifications", [])
                })
            
            return quotes
        except Exception as exc:
            print(f"Error getting quotes for RFQ: {exc}")
            return []

    def update_milestone_status(self, order_id: str, milestone_id: str, status: str) -> dict:
        """Update milestone status for an order"""
        try:
            # Query order and update milestone
            docs = self.orders_collection.where("order_id", "==", order_id).stream()
            
            for doc in docs:
                order_data = doc.to_dict()
                milestones = order_data.get("data", {}).get("contract", {}).get("milestones", [])
                
                # Update specific milestone
                for milestone in milestones:
                    if milestone.get("id") == milestone_id:
                        milestone["status"] = status
                        if status == "completed":
                            milestone["completedAt"] = firestore.SERVER_TIMESTAMP
                
                # Update the document
                doc.reference.update({
                    "data.contract.milestones": milestones
                })
                
                return {"success": True, "milestone_id": milestone_id, "status": status}
            
            return {"success": False, "message": "Order not found"}
        except Exception as exc:
            print(f"Error updating milestone status: {exc}")
            return {"success": False, "message": "Milestone update failed"}
