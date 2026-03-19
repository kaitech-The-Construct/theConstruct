# core/services/supply_chain_service.py

from typing import List, Optional
import hashlib

from core.config.settings import settings
from google.cloud import firestore


class SupplyChainService:
    def __init__(self):
        self.db = firestore.Client()
        self.shipments_collection = self.db.collection(f"{settings.ENVIR}_shipments")
        self.inventory_collection = self.db.collection(f"{settings.ENVIR}_inventory")

    def create_shipment(self, shipment_data: dict) -> dict:
        """Create a new shipment"""
        try:
            # Generate shipment ID
            shipment_id = f"SHP{hashlib.md5(str(shipment_data).encode()).hexdigest()[:8].upper()}"
            
            # Store shipment record
            shipment_record = {
                "shipment_id": shipment_id,
                "data": shipment_data,
                "status": "processing",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.shipments_collection.add(shipment_record)
            
            return {"success": True, "shipment_id": shipment_id, "status": "processing"}
        except Exception as exc:
            print(f"Error creating shipment: {exc}")
            return {"success": False, "message": "Shipment creation failed"}

    def track_shipment(self, tracking_number: str) -> dict:
        """Track a shipment"""
        try:
            # Query shipment from database
            docs = self.shipments_collection.where("data.tracking_number", "==", tracking_number).stream()
            
            for doc in docs:
                shipment_data = doc.to_dict()
                return {
                    "success": True,
                    "shipment_id": shipment_data.get("shipment_id"),
                    "status": shipment_data.get("status"),
                    "details": shipment_data.get("data")
                }
            
            return {"success": False, "message": "Shipment not found"}
        except Exception as exc:
            print(f"Error tracking shipment: {exc}")
            return {"success": False, "message": "Shipment tracking failed"}

    def manage_inventory(self, inventory_data: dict) -> dict:
        """Manage inventory for a manufacturer"""
        try:
            # Generate inventory ID
            inventory_id = f"INV{hashlib.md5(str(inventory_data).encode()).hexdigest()[:8].upper()}"
            
            # Store inventory record
            inventory_record = {
                "inventory_id": inventory_id,
                "data": inventory_data,
                "last_updated": firestore.SERVER_TIMESTAMP
            }
            self.inventory_collection.add(inventory_record)
            
            return {"success": True, "inventory_id": inventory_id}
        except Exception as exc:
            print(f"Error managing inventory: {exc}")
            return {"success": False, "message": "Inventory management failed"}

    def update_shipment_status(self, shipment_id: str, status: str, location: str = None) -> dict:
        """Update shipment status and location"""
        try:
            # Query and update shipment
            docs = self.shipments_collection.where("shipment_id", "==", shipment_id).stream()
            
            for doc in docs:
                update_data = {"status": status}
                if location:
                    update_data["data.current_location"] = location
                    update_data["data.last_updated"] = firestore.SERVER_TIMESTAMP
                
                doc.reference.update(update_data)
                
                return {"success": True, "shipment_id": shipment_id, "status": status}
            
            return {"success": False, "message": "Shipment not found"}
        except Exception as exc:
            print(f"Error updating shipment status: {exc}")
            return {"success": False, "message": "Shipment update failed"}

    def confirm_delivery(self, shipment_id: str, delivery_data: dict) -> dict:
        """Confirm delivery of a shipment"""
        try:
            # Query and update shipment
            docs = self.shipments_collection.where("shipment_id", "==", shipment_id).stream()
            
            for doc in docs:
                update_data = {
                    "status": "delivered",
                    "data.delivered_at": firestore.SERVER_TIMESTAMP,
                    "data.delivery_confirmation": delivery_data
                }
                doc.reference.update(update_data)
                
                return {"success": True, "shipment_id": shipment_id, "status": "delivered"}
            
            return {"success": False, "message": "Shipment not found"}
        except Exception as exc:
            print(f"Error confirming delivery: {exc}")
            return {"success": False, "message": "Delivery confirmation failed"}

    def get_supplier_performance(self, supplier_id: str) -> dict:
        """Get supplier performance analytics"""
        try:
            # Query supplier orders and calculate performance metrics
            orders_ref = self.db.collection(f"{settings.ENVIR}_manufacturing_orders")
            docs = orders_ref.where("data.manufacturerId", "==", supplier_id).stream()
            
            total_orders = 0
            completed_orders = 0
            on_time_deliveries = 0
            
            for doc in docs:
                order_data = doc.to_dict()
                total_orders += 1
                
                if order_data.get("status") == "completed":
                    completed_orders += 1
                    
                    # Check if delivery was on time (simplified logic)
                    production_data = order_data.get("data", {}).get("production", {})
                    estimated = production_data.get("estimatedCompletion")
                    actual = production_data.get("actualCompletion")
                    
                    if estimated and actual and actual <= estimated:
                        on_time_deliveries += 1
            
            # Calculate performance metrics
            completion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
            on_time_rate = (on_time_deliveries / completed_orders * 100) if completed_orders > 0 else 0
            
            return {
                "success": True,
                "supplier_id": supplier_id,
                "performance": {
                    "total_orders": total_orders,
                    "completed_orders": completed_orders,
                    "completion_rate": completion_rate,
                    "on_time_deliveries": on_time_deliveries,
                    "on_time_rate": on_time_rate
                }
            }
        except Exception as exc:
            print(f"Error getting supplier performance: {exc}")
            return {"success": False, "message": "Performance analytics failed"}

    def automated_procurement(self, procurement_data: dict) -> dict:
        """Handle automated procurement workflows"""
        try:
            # Generate procurement ID
            procurement_id = f"PROC{hashlib.md5(str(procurement_data).encode()).hexdigest()[:8].upper()}"
            
            # Store procurement record
            procurement_record = {
                "procurement_id": procurement_id,
                "data": procurement_data,
                "status": "initiated",
                "created_at": firestore.SERVER_TIMESTAMP
            }
            self.db.collection(f"{settings.ENVIR}_procurements").add(procurement_record)
            
            return {"success": True, "procurement_id": procurement_id, "status": "initiated"}
        except Exception as exc:
            print(f"Error in automated procurement: {exc}")
            return {"success": False, "message": "Automated procurement failed"}
