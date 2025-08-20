# core/services/analytics_service.py

from typing import List, Optional
from datetime import datetime, timedelta

from core.config.settings import settings
from google.cloud import firestore


class AnalyticsService:
    def __init__(self):
        self.db = firestore.Client()

    def generate_marketplace_metrics(self) -> dict:
        """Generate real-time marketplace metrics"""
        try:
            # Get total products
            products_count = len(list(self.db.collection(f"{settings.ENVIR}_robots").stream()))
            
            # Get total users
            users_count = len(list(self.db.collection(f"{settings.ENVIR}_users").stream()))
            
            # Get total orders
            orders_count = len(list(self.db.collection(f"{settings.ENVIR}_orders").stream()))
            
            return {
                "success": True,
                "metrics": {
                    "total_products": products_count,
                    "total_users": users_count,
                    "total_orders": orders_count,
                    "last_updated": datetime.utcnow()
                }
            }
        except Exception as exc:
            print(f"Error generating marketplace metrics: {exc}")
            return {"success": False, "message": "Metrics generation failed"}

    def track_user_behavior(self, user_id: str) -> dict:
        """Track user behavior and activity"""
        try:
            # Get user activity history
            activities_ref = self.db.collection(f"{settings.ENVIR}_activities")
            docs = activities_ref.where("userId", "==", user_id).stream()
            
            activity_summary = {
                "total_logins": 0,
                "products_viewed": 0,
                "orders_placed": 0
            }
            
            for doc in docs:
                activity = doc.to_dict()
                if activity.get("type") == "login":
                    activity_summary["total_logins"] += 1
                elif activity.get("type") == "view_product":
                    activity_summary["products_viewed"] += 1
                elif activity.get("type") == "place_order":
                    activity_summary["orders_placed"] += 1
            
            return {"success": True, "behavior_summary": activity_summary}
        except Exception as exc:
            print(f"Error tracking user behavior: {exc}")
            return {"success": False, "message": "Behavior tracking failed"}

    def create_financial_reports(self, date_range: dict) -> dict:
        """Create financial reports"""
        try:
            start_date = date_range.get("start_date")
            end_date = date_range.get("end_date")
            
            # Query orders within date range
            orders_ref = self.db.collection(f"{settings.ENVIR}_orders")
            docs = orders_ref.where("created_at", ">=", start_date).where("created_at", "<=", end_date).stream()
            
            total_revenue = 0
            total_orders = 0
            
            for doc in docs:
                order = doc.to_dict()
                total_revenue += order.get("total_price", 0)
                total_orders += 1
            
            return {
                "success": True,
                "report": {
                    "date_range": date_range,
                    "total_revenue": total_revenue,
                    "total_orders": total_orders,
                    "average_order_value": total_revenue / total_orders if total_orders > 0 else 0
                }
            }
        except Exception as exc:
            print(f"Error creating financial reports: {exc}")
            return {"success": False, "message": "Financial report creation failed"}
