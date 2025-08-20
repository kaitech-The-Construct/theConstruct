# core/services/trade_service.py

from typing import List, Optional

from core.config.settings import settings
from google.cloud import firestore
from schemas.trade import OrderCreate, OrderUpdate


class TradeService:
    def __init__(self):
        self.db = firestore.Client()
        self.orders_collection = self.db.collection(f"{settings.ENVIR}_orders")

    def create_order(self, order_data: OrderCreate) -> dict:
        """Create Order Item"""
        try:
            order_dict = order_data.dict()
            order_dict["status"] = "created"
            order_dict["created_at"] = firestore.SERVER_TIMESTAMP
            doc_ref = self.orders_collection.document()
            doc_ref.set(order_dict)
            order_dict["id"] = doc_ref.id
            return order_dict
        except Exception as exc:
            print(f"Error creating order: {exc}")

    def get_order_by_id(self, order_id: str) -> Optional[dict]:
        """Get Order by ID"""
        try:
            order_ref = self.orders_collection.document(order_id)
            order = order_ref.get()
            if not order.exists:
                return None
            order_dict = order.to_dict()
            order_dict["id"] = order.id
            return order_dict
        except Exception as exc:
            print(f"Error retrieving order by ID: {exc}")

    def get_orders_by_user(self, user_id: str) -> List[dict]:
        """Get all orders for a user"""
        try:
            orders = []
            docs = self.orders_collection.where("buyer_id", "==", user_id).stream()
            for doc in docs:
                order_dict = doc.to_dict()
                order_dict["id"] = doc.id
                orders.append(order_dict)
            return orders
        except Exception as exc:
            print(f"Error retrieving orders by user: {exc}")

    def update_order_status(
        self, order_id: str, order_update_data: OrderUpdate
    ) -> Optional[dict]:
        """Update Order Status"""
        try:
            order_ref = self.orders_collection.document(order_id)
            order_data = order_update_data.dict(exclude_unset=True)
            order_ref.update(order_data)
            order = order_ref.get()
            if not order.exists:
                return None
            order_dict = order.to_dict()
            order_dict["id"] = order.id
            return order_dict
        except Exception as exc:
            print(f"Error updating order by ID: {exc}")

    def process_payment(self, order_id: str, payment_method: str) -> dict:
        """Process payment for an order"""
        try:
            order_ref = self.orders_collection.document(order_id)
            order = order_ref.get()
            if not order.exists:
                return {"success": False, "message": "Order not found"}
            
            # Update order with payment information
            payment_data = {
                "payment.method": payment_method,
                "payment.status": "completed",
                "payment.processedAt": firestore.SERVER_TIMESTAMP,
                "status": "paid"
            }
            order_ref.update(payment_data)
            
            return {"success": True, "message": "Payment processed successfully"}
        except Exception as exc:
            print(f"Error processing payment: {exc}")
            return {"success": False, "message": "Payment processing failed"}

    def manage_escrow(self, order_id: str, escrow_data: dict) -> dict:
        """Manage escrow for an order"""
        try:
            order_ref = self.orders_collection.document(order_id)
            order = order_ref.get()
            if not order.exists:
                return {"success": False, "message": "Order not found"}
            
            # Create escrow record
            escrow_ref = self.db.collection(f"{settings.ENVIR}_escrows")
            escrow_record = {
                "order_id": order_id,
                "amount": escrow_data.get("amount"),
                "status": "active",
                "created_at": firestore.SERVER_TIMESTAMP,
                **escrow_data
            }
            escrow_doc = escrow_ref.add(escrow_record)
            
            # Update order with escrow information
            order_ref.update({
                "payment.escrowId": escrow_doc[1].id,
                "payment.method": "escrow",
                "status": "escrowed"
            })
            
            return {"success": True, "escrow_id": escrow_doc[1].id}
        except Exception as exc:
            print(f"Error managing escrow: {exc}")
            return {"success": False, "message": "Escrow management failed"}

    def track_order_status(self, order_id: str) -> dict:
        """Track order status and history"""
        try:
            order = self.get_order_by_id(order_id)
            if not order:
                return {"status": "not_found"}
            
            # Get order history/milestones
            milestones = order.get("milestones", [])
            
            return {
                "order_id": order_id,
                "current_status": order.get("status"),
                "milestones": milestones,
                "created_at": order.get("created_at"),
                "estimated_delivery": order.get("shipping", {}).get("estimatedDelivery")
            }
        except Exception as exc:
            print(f"Error tracking order status: {exc}")
            return {"status": "error"}

    def handle_disputes(self, order_id: str, dispute_data: dict) -> dict:
        """Handle order disputes"""
        try:
            # Create dispute record
            disputes_ref = self.db.collection(f"{settings.ENVIR}_disputes")
            dispute_record = {
                "order_id": order_id,
                "status": "open",
                "created_at": firestore.SERVER_TIMESTAMP,
                **dispute_data
            }
            dispute_doc = disputes_ref.add(dispute_record)
            
            # Update order status
            order_ref = self.orders_collection.document(order_id)
            order_ref.update({
                "status": "disputed",
                "dispute_id": dispute_doc[1].id
            })
            
            return {"success": True, "dispute_id": dispute_doc[1].id}
        except Exception as exc:
            print(f"Error handling dispute: {exc}")
            return {"success": False, "message": "Dispute handling failed"}
